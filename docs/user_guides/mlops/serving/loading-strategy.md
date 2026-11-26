# How to Select the Loading Strategy of a Deployment { #loading-strategy-guide }

## Introduction

The loading strategy decides how a deployment's pods get the model files and the deployment's own files, such as the predictor script.
Every strategy puts them at the same paths, `/mnt/models` and `/mnt/artifacts`, so scripts work unchanged.

| Strategy         | In the UI              | How the pods get the files                                                                                        | Model servers               |
| ---------------- | ---------------------- | ----------------------------------------------------------------------------------------------------------------- | --------------------------- |
| `RUNAI_STREAMER` | Stream to GPU          | Mounted from HopsFS; vLLM streams the weights to the GPUs with the [Run:ai Model Streamer][runai-model-streamer]. | vLLM on GPUs, not vLLM-Omni |
| `DOWNLOAD`       | Download to local disk | Copied to the pod's local disk before the model server starts.                                                    | All                         |
| `MOUNT`          | Stream from HopsFS     | Mounted read-only from HopsFS and read in place.                                                                  | All                         |

The two mount strategies need the [HopsFS CSI driver][hopsfs-csi-driver].
Without it, `DOWNLOAD` is the only strategy, and a deployment that mounts fails to start until it is switched to `DOWNLOAD`.

A new deployment without a strategy gets `RUNAI_STREAMER` when it runs vLLM, not vLLM-Omni, on GPUs, the driver is enabled and the model has safetensors files at the top of its files.
Every other deployment gets `DOWNLOAD`, as do the deployments that existed before loading strategies.
Saving a deployment without a strategy keeps the one it has, and saving a new one on a running deployment replaces its pods right away.

If an update removes all GPUs or selects a model without top-level safetensors files, a deployment using `RUNAI_STREAMER` must switch strategies.
The Python SDK gained the `loading_strategy` setting in 5.3, so if you use an older SDK, make the change in the web UI or upgrade to SDK 5.3 or later and save the update with `DOWNLOAD` or `MOUNT`.

### Which strategy to choose

- **`RUNAI_STREAMER`** loads vLLM models fastest, especially on several GPUs: each GPU reads a share of the files and passes it to the others, so the model is read from HopsFS once.
  It needs safetensors weights and vLLM's GPU image; the official `vllm/vllm-openai` images include the streamer, and a custom image needs `vllm[runai]`.
- **`DOWNLOAD`** is usually faster than `MOUNT`: the copy reads the files at full speed, and the model server then loads them from local disk.
  It needs local disk at least as large as the model.
- **`MOUNT`** needs no copy and no local disk, but usually starts a deployment more slowly than `DOWNLOAD`.
  For plain vLLM, Hopsworks adds `--safetensors-load-strategy eager` by default because vLLM's lazy loading reads a mount more slowly.
  Hopsworks skips this flag for vLLM-Omni, and when the vLLM configuration file sets `safetensors-load-strategy`, enables `enable_multithread_load` in `model-loader-extra-config`, or cannot be read.
  With eager loading, each file being loaded is held in host memory and counts against the deployment's memory limit, so a CPU-only deployment needs room for its largest weight file in addition to the model.

Each pod that mounts runs its own HopsFS mount container, which the [Resources Guide](resources.md) shows how to size.

!!! warning "A mounted deployment needs its HopsFS mount for as long as it runs"
    A model server reads files it has not loaded yet from the mount, so it fails when the mount does.
    The [failure modes][hopsfs-csi-failure-modes] of the driver describe how to recover.

### Run:ai Model Streamer settings { #run-ai-model-streamer-settings }

With `RUNAI_STREAMER`, Hopsworks starts vLLM with the defaults below, and the deployment's configuration file or environment variables override each of them.

- **`--load-format runai_streamer`** loads the weights with the streamer.
  A `load-format` in the configuration file, or an option only vLLM's default loader takes such as `enable_multithread_load`, keeps vLLM's own loader instead; choose `DOWNLOAD` or `MOUNT` then, since that loader reads a mount slowly.
- **`--model-loader-extra-config '{"distributed": true}'`**, with more than one GPU, streams the model once for all GPUs.
  A `model-loader-extra-config` in the configuration file replaces it, so add `distributed: true` to it to keep this.
- **`RUNAI_STREAMER_MEMORY_LIMIT=0`** stages one tensor at a time in host memory.
  A larger limit in bytes lets the streamer read ahead, and counts against the deployment's memory limit.

## Web UI

### Step 1: Create a new deployment

Navigate to `Model Deployments` in the menu on the left and click on `New model deployment`.

### Step 2: Select the loading strategy

Choose the strategy in the `Model loading` field of the `Deployment configuration` card.
The field offers only the strategies the deployment can use, with its default selected.
Click on `Create new model deployment` to create the deployment.

## Code

### Step 1: Connect to Hopsworks

=== "Python"

  ```python
  import hopsworks


  project = hopsworks.login()

  # get Hopsworks Model Registry handle
  mr = project.get_model_registry()

  # get Hopsworks Model Serving handle
  ms = project.get_model_serving()
  ```

### Step 2: Create a deployment with a specific loading strategy

=== "Python"

  ```python
  my_model = mr.get_model("my_model", version=1)

  my_predictor = ms.create_predictor(
      my_model,
      loading_strategy="MOUNT",  # or "RUNAI_STREAMER" for vLLM, or "DOWNLOAD"
  )
  my_deployment = my_predictor.deploy()

  # change it on an existing deployment: a running one rolls out new pods right away
  my_deployment.loading_strategy = "DOWNLOAD"
  my_deployment.save()
  ```

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-method"></code> [`ModelServing.create_predictor`][hsml.model_serving.ModelServing.create_predictor]
    - <code class="doc-symbol doc-symbol-method"></code> [`Predictor.deploy`][hsml.predictor.Predictor.deploy]
    - <code class="doc-symbol doc-symbol-class"></code> [`Deployment`][hsml.deployment.Deployment]
        - <code class="doc-symbol doc-symbol-attribute"></code> [`loading_strategy`][hsml.deployment.Deployment.loading_strategy]
        - <code class="doc-symbol doc-symbol-method"></code> [`save`][hsml.deployment.Deployment.save]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>

[runai-model-streamer]: https://github.com/run-ai/runai-model-streamer
