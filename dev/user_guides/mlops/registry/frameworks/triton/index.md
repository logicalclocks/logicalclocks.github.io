# How To Export a Triton Model { #triton-model-guide }

## Introduction

In this guide you will learn how to package a model for [NVIDIA Triton Inference Server](https://github.com/triton-inference-server/server), register it in the Model Registry, deploy it and send it inference requests.

!!! info "Triton is enabled per cluster"
    Triton deployments are available only on clusters where the administrator has enabled Triton and configured its image, see [Triton Inference Server][triton-admin].
    On other clusters `ms.get_triton_image_tags()` returns an empty list, the UI does not offer the Triton model server, and the API rejects Triton deployments.

!!! warning "Python client 5.3 or later"
    Triton models need the Hopsworks Python client 5.3 or later, in the jobs and notebooks that read the model registry too.
    An older client raises `ValueError: framework TRITON is not a supported framework` whenever it reads a Triton model, for example when it lists the models of a registry that holds one.

## Model directory { #triton-model-directory }

A Triton model in Hopsworks is one Triton model directory per model version.
`save()` uploads the contents of the directory you pass to it, so `config.pbtxt` sits at the top of that directory:

```text
iris_onnx/
├── config.pbtxt
└── 1/
    └── model.onnx
```

- `config.pbtxt` is the [Triton model configuration](https://github.com/triton-inference-server/server/blob/main/docs/user_guide/model_configuration.md).
- Each numeric folder (`1/`, `2/`, ...) is a Triton model version and holds the model file of the backend, such as `model.onnx`, `model.pt`, `model.plan` or `model.py`.
- A Python backend model can add a packed environment next to `config.pbtxt`, see [Python backend][triton-python-backend].

Hopsworks rejects a Triton deployment whose model files have no `config.pbtxt` or no numeric version folder.
In the predictor, the files are placed at `/mnt/models/<deployment-name>/`, and Triton serves the model under the name of the deployment.

A minimal `config.pbtxt` for an ONNX model that takes four features and returns a label:

```text
backend: "onnxruntime"
max_batch_size: 0
input [
  {
    name: "input"
    data_type: TYPE_FP32
    dims: [ -1, 4 ]
  }
]
output [
  {
    name: "label"
    data_type: TYPE_INT64
    dims: [ -1 ]
  }
]
```

### Model name

Omit `name` in `config.pbtxt`.
Triton then takes the model name from the directory, which is the deployment name, so the same model version can be deployed under any deployment name.
A `name` that differs from the deployment name makes Triton fail to load the model, and the deployment fails to start.

### Versions

The Hopsworks model version and the numeric Triton version folders are independent of each other.
Triton serves the highest numeric folder only, unless `version_policy` in `config.pbtxt` selects other versions:

```text
version_policy: { all: { } }
```

Hopsworks starts Triton with `--model-control-mode=none`.
Triton loads the model at startup, and the model repository load and unload requests return errors.
To serve a different model, register a new model version and deploy it.

### Dynamic batching

Triton batches requests in its own scheduler, configured in `config.pbtxt`.
The KServe [inference batcher](../../serving/inference-batcher.md) is not available for Triton deployments, because Triton's scheduler already does this inside the model server.

```text
max_batch_size: 32
dynamic_batching {
  max_queue_delay_microseconds: 1000
}
```

With `max_batch_size` above 0, `dims` leave out the batch dimension, and the first entry of `shape` in a request is the batch size.

### GPUs

Request GPUs in the deployment's [resources](../../serving/resources.md); Hopsworks gives Triton deployments no GPU by default.
Which backends run on a GPU depends on the Triton image the administrator configured.
Use `instance_group` in `config.pbtxt` to place model instances:

```text
instance_group [
  {
    count: 1
    kind: KIND_GPU
  }
]
```

## Python backend { #triton-python-backend }

A [Python backend](https://github.com/triton-inference-server/python_backend) model keeps its code in `model.py` inside the version folder.
Dependencies that the Triton image does not contain ship as a [conda-pack](https://conda.github.io/conda-pack/) archive in the model directory:

```text
text_classifier/
├── config.pbtxt
├── environment.tar.gz
└── 1/
    └── model.py
```

Point `EXECUTION_ENV_PATH` in `config.pbtxt` at the archive:

```text
backend: "python"
max_batch_size: 0
input [
  {
    name: "text"
    data_type: TYPE_STRING
    dims: [ -1 ]
  }
]
output [
  {
    name: "scores"
    data_type: TYPE_FP32
    dims: [ -1, 2 ]
  }
]
parameters: {
  key: "EXECUTION_ENV_PATH"
  value: { string_value: "$$TRITON_MODEL_DIRECTORY/environment.tar.gz" }
}
```

Pack the environment with the same Python version as the Python backend of the Triton image, for example Python 3.12 for the NVIDIA 26.x images.
The backend runs `model.py` with the interpreter of the archive, and a model whose archive has another Python version fails to load.

```bash
conda create -y -n triton-env python=3.12
conda run -n triton-env pip install numpy torch transformers
conda install -y -n base -c conda-forge conda-pack
conda pack -n triton-env -o text_classifier/environment.tar.gz
```

A `model.py` implements `TritonPythonModel`:

=== "Python"

    ```python
    import numpy as np
    import triton_python_backend_utils as pb_utils


    class TritonPythonModel:
        def initialize(self, args):
            # args["model_repository"] and args["model_version"] locate the files
            self.model = ...

        def execute(self, requests):
            responses = []
            for request in requests:
                texts = pb_utils.get_input_tensor_by_name(request, "text").as_numpy()
                scores = self.model([t.decode("utf-8") for t in texts])
                output = pb_utils.Tensor("scores", np.asarray(scores, dtype=np.float32))
                responses.append(pb_utils.InferenceResponse(output_tensors=[output]))
            return responses
    ```

The Python backend hands input tensors to `model.py` on the CPU by default, so move them to the GPU in `model.py` when the model runs there.
Hopsworks mounts a memory-backed `/dev/shm` in Triton predictors, which the Python backend uses to pass tensors between Triton and the model process.
It counts against the memory of the deployment, so size the memory request for the tensors of the largest batch as well as the model.

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

### Step 2: Register the model directory

Use the `ModelRegistry.triton.create_model(..)` function to register a model as a Triton model, then invoke `save()` with the path to the local Triton model directory.

=== "Python"

    ```python
    triton_model = mr.triton.create_model("irisonnx")

    triton_model.save("iris_onnx")
    ```

### Step 3: Deploy the model

The image version is the tag of the Triton image the deployment runs, see [Triton image version](../../serving/predictor.md#triton-image-version).
`ms.get_triton_image_tags()` lists the tags the cluster advertises, highest first.
Without `triton_image_tag`, the deployment gets the highest one.

=== "Python"

    ```python
    from hsml.resources import PredictorResources, Resources


    print(ms.get_triton_image_tags())

    triton_deployment = triton_model.deploy(
        name="irisonnx",
        triton_image_tag="26.09-py3",
        resources=PredictorResources(
            num_instances=1,
            requests=Resources(cores=1, memory=2048, gpus=0),
            limits=Resources(cores=2, memory=4096, gpus=0),
        ),
    )
    triton_deployment.start(await_running=600)
    ```

The deployment name is also the Triton model name, so it follows the deployment name rules: letters and digits only.

!!! warning "Knative mode and large images"
    Triton images are large: NVIDIA's `26.09-py3` image is 8.4 GiB compressed for amd64.
    In [Knative mode](../../serving/autoscaling.md#deployment-mode) a deployment that scales up from zero on a node that has not pulled the image yet waits for the pull before it answers.

### Step 4: Send an inference request

Triton deployments use the Open Inference Protocol (KServe v2), over REST or gRPC.
Pass one tensor per input named in `config.pbtxt`, with its `shape`, `datatype` and the values flattened in row-major order in `data`.

=== "Python"

    ```python
    response = triton_deployment.predict(
        inputs=[
            {
                "name": "input",
                "shape": [1, 4],
                "datatype": "FP32",
                "data": [5.1, 3.5, 1.4, 0.2],
            }
        ]
    )
    print(response["outputs"])
    ```

The response is the v2 response of Triton:

```json
{
  "model_name": "irisonnx",
  "model_version": "1",
  "outputs": [
    {"name": "label", "datatype": "INT64", "shape": [1], "data": [0]}
  ]
}
```

See the [REST API guide][open-inference-protocol-v2] for the inference URL, the request through the Hopsworks REST API, and `curl` examples.

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-method"></code> [`Model.deploy`][hsml.model.Model.deploy]
    - <code class="doc-symbol doc-symbol-class"></code> [`PredictorResources`][hsml.resources.PredictorResources]
    - <code class="doc-symbol doc-symbol-class"></code> [`Deployment`][hsml.deployment.Deployment]
        - <code class="doc-symbol doc-symbol-method"></code> [`start`][hsml.deployment.Deployment.start]
        - <code class="doc-symbol doc-symbol-method"></code> [`predict`][hsml.deployment.Deployment.predict]
    - <code class="doc-symbol doc-symbol-docs"></code> [Triton model configuration](https://github.com/triton-inference-server/server/blob/main/docs/user_guide/model_configuration.md)
    - <code class="doc-symbol doc-symbol-docs"></code> [Triton Python backend](https://github.com/triton-inference-server/python_backend)

    <a class="hops-api-cta" href="../../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>

## Supported features

| Feature | Triton deployments | Why |
| ------- | ------------------ | --- |
| REST | Open Inference Protocol v2, JSON | Triton's HTTP endpoint |
| gRPC | Open Inference Protocol v2 | Triton's gRPC endpoint, see [API protocol](../../serving/api-protocol.md) |
| Binary tensor extension | Direct requests to the Istio gateway only | The Hopsworks REST API forwards JSON bodies only |
| CPU and GPU | Yes, no GPU by default | The backends that run on a GPU depend on the image |
| Standard and Knative modes | Yes | See [Deployment mode](../../serving/autoscaling.md#deployment-mode) |
| Dynamic batching | `dynamic_batching` in `config.pbtxt` | Triton batches in its own scheduler |
| KServe inference batcher | No | Triton batches in its own scheduler |
| Predictor script | No | The model directory holds the model code, for example `model.py` |
| Transformer | No | Over REST the transformer forwards requests in the KServe v1 format, which Triton does not serve; pre-process in the model directory, for example in `model.py` |
| Inference logging and feature logging | No | The logger parses JSON only, and Triton requests can carry binary tensors or use gRPC |
| Disk logging | No | The upload runs the Hopsworks library inside the serving container, which the Triton image does not have |
| Several models or ensembles per deployment | No | A deployment serves one Triton model, named after the deployment |
| Model load and unload requests | No | Triton runs with `--model-control-mode=none` |
