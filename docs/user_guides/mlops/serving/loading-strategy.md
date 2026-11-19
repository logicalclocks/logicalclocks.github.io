# How to Select the Loading Strategy of a Deployment { #loading-strategy-guide }

## Introduction

Before a model server can answer requests, the pods of a deployment need the model version's files and the deployment's own files, such as the predictor script and the configuration file.
The loading strategy decides how they get them.

| Strategy         | How the pods get the files                                                                                        | Model servers                      |
| ---------------- | ----------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| `MOUNT`          | Mounted read-only from HopsFS and read in place.                                                                  | All                                |
| `RUNAI_STREAMER` | Mounted read-only from HopsFS, and vLLM loads the weights with the [Run:ai Model Streamer][runai-model-streamer]. | vLLM, but not vLLM-Omni            |
| `DOWNLOAD`       | Downloaded to the pod's local disk before the model server starts.                                                | All                                |

Either way the files are at the same paths, `/mnt/models` and `/mnt/artifacts`, so predictor and transformer scripts do not depend on the strategy.

The two mount strategies need the [HopsFS CSI driver][hopsfs-csi-driver]; without it, `DOWNLOAD` is the only strategy.
A deployment with a mount strategy fails to start if the driver is disabled later, until its strategy is changed to `DOWNLOAD`.
The strategy is set per deployment.
Saving a new strategy on a running deployment rolls it out right away and replaces its pods; a stopped deployment uses it the next time it starts.
A deployment created without a strategy gets `RUNAI_STREAMER` for vLLM and `MOUNT` for every other model server and for vLLM-Omni when the driver is enabled, and `DOWNLOAD` without it or for a vLLM model the streamer cannot load.
Updating a deployment without a strategy keeps the one it has, and a deployment created before loading strategies existed keeps downloading its files.

### Which strategy to choose

- **`MOUNT`** starts the model server without copying the model first and needs no local disk for it.
  The model server reads the files from HopsFS as it needs them.
  Hopsworks starts vLLM and vLLM-Omni with `--safetensors-load-strategy eager`, so they read each safetensors file whole before loading its weights, unless the configuration file sets `safetensors-load-strategy`.
  Their own default, `lazy`, maps the files into memory and reads them out of order, which is several times slower from a mount: loading a 16 GB model that way took 524 s, against 202 s with `RUNAI_STREAMER`.
  Reading a file whole holds it in host memory while its weights load, once per GPU, and that counts against the deployment's memory limit.
  For vLLM-Omni it is the only way to read a mounted model.
- **`RUNAI_STREAMER`** is how vLLM reads a mounted model.
  The streamer reads the safetensors files in large chunks, several at once.
  vLLM's default loader maps the files into memory instead and reads a mount several times slower.
  Loading a 16 GB model with the streamer takes about as long as downloading it, without the local disk.
  The weights must be in safetensors format, and the vLLM image must include the streamer: the official `vllm/vllm-openai` images do, and a custom image needs `vllm[runai]`.
  Saving `RUNAI_STREAMER` for a model without safetensors weights at the top of its files is rejected.
  vLLM-Omni cannot use it: the streamer hands over tensors in the order it reads them, and vLLM-Omni's model loaders need them in file order.
  See [Run:ai Model Streamer settings][run-ai-model-streamer-settings] for how it is configured.
- **`DOWNLOAD`** needs local disk at least as large as the model, and then reads the files at disk speed.
  Use it when the cluster has no HopsFS CSI driver, when a vLLM model has no safetensors weights, when the vLLM image does not include the streamer, or when the configuration file sets its own `load-format`.

### Run:ai Model Streamer settings { #run-ai-model-streamer-settings }

With `RUNAI_STREAMER`, Hopsworks starts vLLM with the defaults below.
Each one is only a default: setting it in the deployment's configuration file or environment variables takes precedence.

- **`--load-format runai_streamer`** makes vLLM load the weights with the streamer.
  A `load-format` in the configuration file replaces the streamer, and that loader then reads the model from the mount; for vLLM's default loader that is several times slower, so choose `DOWNLOAD` to load from a local copy instead.
- **Distributed streaming**, when a vLLM deployment has more than one GPU: each GPU reads a share of the files and passes it to the others, so the model is read from HopsFS once instead of once per GPU.
  Hopsworks turns it on with `--model-loader-extra-config '{"distributed": true}'`, unless the configuration file sets `model-loader-extra-config`, whose value then replaces it: add `distributed: true` to it to keep distributed streaming.
- **`RUNAI_STREAMER_MEMORY_LIMIT=0`**, the host memory the streamer stages tensors in: a single buffer the size of the largest tensor.
  A limit in bytes gives the streamer more buffers to read ahead with, but a limit smaller than the largest tensor fails the load.
  A `memory_limit` in `model-loader-extra-config`, or the variable set in the deployment's environment variables, replaces it.

The staging memory counts against the deployment's memory limit, unlike the page cache a download fills, so when you raise the limit, give the deployment that much memory beyond what vLLM itself uses.

!!! warning "A mounted deployment needs its HopsFS mount for as long as it runs"
    A model server that reads its files lazily also needs the mount after it started, so a failed mount stops it from reading files it has not loaded yet.
    The [failure modes][hopsfs-csi-failure-modes] of the driver describe how to recover.

## Web UI

### Step 1: Create a new deployment

If you have at least one model already trained and saved in the Model Registry, navigate to the deployments page by clicking on the `Deployments` tab on the navigation menu on the left.
Once in the deployments page, you can create a new deployment by either clicking on `New deployment` (if there are no existing deployments) or on `Create new deployment` in the top-right corner.

### Step 2: Go to advanced options

A simplified creation form will appear including the most common deployment fields from all available configurations.
To navigate to the advanced creation form, click on `Advanced options`.

### Step 3: Select the loading strategy

Select the strategy in the `Loading strategy` field.
It lists the strategies the model server of the deployment supports, with its default already selected: `RUNAI_STREAMER` for vLLM and `MOUNT` for the other model servers, or `DOWNLOAD` when the cluster has no HopsFS CSI driver.

Once you are done with the changes, click on `Create new deployment` at the bottom of the page to create the deployment for your model.

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
      loading_strategy="MOUNT",  # "DOWNLOAD", or "RUNAI_STREAMER" for vLLM
  )
  my_deployment = my_predictor.deploy()

  # change it on an existing deployment: a running one rolls out new pods right away
  my_deployment.loading_strategy = "DOWNLOAD"
  my_deployment.save()
  ```

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-method"></code> [`ModelServing.create_predictor`][hsml.model_serving.ModelServing.create_predictor]
    - <code class="doc-symbol doc-symbol-class"></code> [`Deployment`][hsml.deployment.Deployment]
        - <code class="doc-symbol doc-symbol-attribute"></code> [`loading_strategy`][hsml.deployment.Deployment.loading_strategy]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>

[runai-model-streamer]: https://github.com/run-ai/runai-model-streamer
