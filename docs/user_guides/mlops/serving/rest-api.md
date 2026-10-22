# Hopsworks Model Serving REST API

## Introduction

Hopsworks provides ==model serving capabilities== by leveraging [KServe](https://kserve.github.io/website/) as the model serving platform and [Istio](https://istio.io/) as the ingress gateway to the model deployments.

This document explains how to interact with a model deployment via REST API.

!!! tip "Tutorials"
    End-to-end examples are available in the [hopsworks-tutorials](https://github.com/logicalclocks/hopsworks-tutorials/tree/master) repository.

## Sending Inference Requests through Istio Ingress

The full inference URL is constructed by combining a base path with a model server-specific suffix.
See [URL Paths](#url-paths) for the complete URL format and examples.

### Authentication

All requests must include an API Key for authentication.
You can create an API key by following this [guide](../../projects/api_key/create_api_key.md).

Include the key in the `authorization` header:

```text
authorization: ApiKey <API_KEY_VALUE>
```

### Headers

| Header          | Description                         | Example Value           |
| --------------- | ----------------------------------- | ----------------------- |
| `authorization` | API key for authentication.         | `ApiKey <your_api_key>` |
| `content-type`  | Request payload type (JSON).        | `application/json`      |

Triton deployments also accept Triton's binary tensor extension on the Istio path, see [Binary tensor data](#binary-tensor-data).

## URL Paths

Deployed models are accessible through the ==Istio ingress gateway== using **path-based** routing.
The full URL is constructed by combining the base path with a model server-specific suffix.
This URL is also provided on the model deployment page in the Hopsworks UI.

!!! example ""
    **`<base_url>/<server-specific_suffix>`**

Where `server-specific_suffix` depends on the model server type (see [ML Inference Paths](#ml-inference), [Open Inference Protocol (v2) Paths][open-inference-protocol-v2] or [OpenAI-compatible Paths](#openai-compatible)).

### Base URL

The base URL is composed of the **Istio ingress gateway IP**, the **project name**, and the **deployment name**.

!!! example ""
    **`https://<ISTIO_GATEWAY_IP>/v1/<project_name>/<deployment_name>`**

!!! warning "Host-based routing (legacy)"
    Prior to path-based routing, requests were routed using a `Host` header matching the model deployment hostname, and **`https://<ISTIO_GATEWAY_IP>`** as base url.

    ```
    Host: <deployment-name>.<project-name>.<knative-domain-name>
    ```

    Each model deployment gets its own Knative-generated hostname, and routing depends on the `Host` header matching Istio ingress gateway rules.

    Path-based routing (described above) is the preferred method for external access.

### ML Inference

For model deployments using Python, KServe sklearnserver, or TensorFlow Serving, the URL follows the KServe V1 inference protocol.

!!! info "Supported verbs and path format"
    | Model Server         | Supported Verbs                  | Path Format                          |
    | -------------------- | -------------------------------- | ------------------------------------ |
    | Python               | `predict`                        | `<base_url>/v1/models/<name>:<verb>` |
    | KServe sklearnserver | `predict`                        | `<base_url>/v1/models/<name>:<verb>` |
    | TensorFlow Serving   | `predict`, `classify`, `regress` | `<base_url>/v1/models/<name>:<verb>` |

!!! tip "Hopsworks Python API"

    ML inference urls can be retrieved using the `Deployment` class.

    ```python
    # Returns: https://<istio-host>/v1/<project>/<deployment>/v1/models/<name>:predict
    inference_url = deployment.get_inference_url()
    ```

### Open Inference Protocol (v2) { #open-inference-protocol-v2 }

==Triton deployments== follow the [Open Inference Protocol](https://kserve.github.io/website/docs/concepts/architecture/data-plane/v2-protocol), also called the KServe V2 protocol.
The model name in the path is the deployment name.

!!! info "Supported verbs and path format"
    | Model Server | Method | Path Format                         | Purpose          |
    | ------------ | ------ | ----------------------------------- | ---------------- |
    | Triton       | `POST` | `<base_url>/v2/models/<name>/infer` | Inference        |
    | Triton       | `GET`  | `<base_url>/v2/models/<name>/ready` | Model readiness  |
    | Triton       | `GET`  | `<base_url>/v2/models/<name>`       | Model metadata   |

The model metadata response lists the input and output tensors from `config.pbtxt`, with their names, data types and shapes.

!!! tip "Hopsworks Python API"

    The inference url of a Triton deployment is retrieved the same way.

    ```python
    # Returns: https://<istio-host>/v1/<project>/<deployment>/v2/models/<name>/infer
    inference_url = deployment.get_inference_url()
    ```

Requests can also go through the Hopsworks REST API, which forwards them to the deployment, with the `infer` verb in place of `predict`:

!!! example ""
    **`POST https://<HOPSWORKS_HOST>/hopsworks-api/api/project/<project_id>/inference/serving/<deployment_name>:infer`**

The Hopsworks REST API accepts JSON bodies only, so binary tensor data works only on the Istio path.

### Deployment schema discovery

Deployments that carry a deployment schema describe their request and response contract as JSON Schema and OpenAPI, and validate every request against it before any predictor code runs.
The documents are served by the Hopsworks REST API (not the Istio ingress), with an API key that has the `SERVING` scope:

!!! example ""
    **`GET https://<HOPSWORKS_HOST>/hopsworks-api/api/project/<project_id>/serving/<serving_id>/schema?format=openapi`**

`format` is `schema` (default), `jsonschema`, or `openapi`; `schemaId=<id>` returns the contract of an earlier revision.
The serving id is the `id` field of `GET .../project/<project_id>/serving?name=<deployment_name>`.
A deployment without a schema, or an unknown id, answers `404` with error code `240037`.
Feature view deployments answer on the same `<base_url>/v1/models/<name>:predict` route as Python model deployments.
See the [Deployment Schema Guide][deployment-schema].

### OpenAI-compatible

==vLLM deployments== provide an OpenAI API-compatible endpoint at `<base_url>/v1/`, allowing you to send any standard OpenAI API request to the vLLM server.

!!! example "e.g., Chat Completions endpoint"
    **`<base_url>/v1/chat/completions`**

Refer to the official [vLLM OpenAI-compatible server documentation](https://docs.vllm.ai/en/v0.28.0/serving/openai_compatible_server.html) for details about the available APIs.

!!! tip "Hopsworks Python API"

    OpenAI-compatible urls can be retrieved using the `Deployment` class.

    ```python
    # Returns: https://<istio-host>/v1/<project>/<deployment>/v1
    # Append /chat/completions or /completions for specific endpoints
    openai_url = deployment.get_openai_url()
    ```

## Request Format

The request format depends on the model server being used.

For predictive inference (TensorFlow, sklearn, or Python model server), the request must be sent as a JSON object containing an `inputs` or `instances` field.
See [more information on the request format](https://kserve.github.io/website/docs/concepts/architecture/data-plane/v1-protocol#request-format).

!!! example "REST API example for Predictive Inference (Tensorflow or SkLearn or Python Serving)"
    === "Python"

        ```python
        import requests


        data = {"inputs": [[4641025220953719, 4920355418495856]]}

        headers = {"authorization": "ApiKey <your_api_key>", "content-type": "application/json"}

        response = requests.post(
            "https://<ISTIO_GATEWAY_IP>/v1/my_project/fraud/v1/models/fraud:predict",
            headers=headers,
            json=data,
        )
        print(response.json())
        ```

    === "Curl"

        ```bash
        curl -X POST "https://<ISTIO_GATEWAY_IP>/v1/my_project/fraud/v1/models/fraud:predict" \
          -H "authorization: ApiKey <your_api_key>" \
          -H "content-type: application/json" \
          -d '{
                "inputs": [
                  [4641025220953719, 4920355418495856]
                ]
              }'
        ```

For Triton deployments, the request follows the [Open Inference Protocol](https://kserve.github.io/website/docs/concepts/architecture/data-plane/v2-protocol) and is sent to the `infer` path.
The body is a JSON object with an `inputs` list holding one tensor per model input named in `config.pbtxt`:

| Field                 | Description                                                                      |
| --------------------- | -------------------------------------------------------------------------------- |
| `inputs[].name`       | Input name from `config.pbtxt`.                                                  |
| `inputs[].shape`      | Tensor shape, with the batch size first when the model has `max_batch_size > 0`. |
| `inputs[].datatype`   | Tensor data type, such as `FP32`, `INT64` or `BYTES`.                            |
| `inputs[].data`       | Tensor values, flattened in row-major order.                                     |
| `inputs[].parameters` | Optional input parameters.                                                       |
| `outputs`             | Optional list of `{"name": ...}` objects selecting the outputs to return.        |
| `parameters`          | Optional request parameters.                                                     |

!!! example "REST API example for Triton"
    === "Python"

        ```python
        import requests


        data = {
            "inputs": [
                {
                    "name": "input",
                    "shape": [1, 4],
                    "datatype": "FP32",
                    "data": [5.1, 3.5, 1.4, 0.2],
                }
            ],
            "outputs": [{"name": "label"}],
        }

        headers = {"authorization": "ApiKey <your_api_key>", "content-type": "application/json"}

        response = requests.post(
            "https://<ISTIO_GATEWAY_IP>/v1/my_project/irisonnx/v2/models/irisonnx/infer",
            headers=headers,
            json=data,
        )
        print(response.json())
        ```

    === "Curl"

        ```bash
        curl -X POST "https://<ISTIO_GATEWAY_IP>/v1/my_project/irisonnx/v2/models/irisonnx/infer" \
          -H "authorization: ApiKey <your_api_key>" \
          -H "content-type: application/json" \
          -d '{
                "inputs": [
                  {"name": "input", "shape": [1, 4], "datatype": "FP32", "data": [5.1, 3.5, 1.4, 0.2]}
                ],
                "outputs": [{"name": "label"}]
              }'
        ```

    === "Hopsworks REST API"

        ```bash
        curl -X POST "https://<HOPSWORKS_HOST>/hopsworks-api/api/project/<project_id>/inference/serving/irisonnx:infer" \
          -H "authorization: ApiKey <your_api_key>" \
          -H "content-type: application/json" \
          -d '{
                "inputs": [
                  {"name": "input", "shape": [1, 4], "datatype": "FP32", "data": [5.1, 3.5, 1.4, 0.2]}
                ]
              }'
        ```

    === "Hopsworks Python API"

        ```python
        response = deployment.predict(
            inputs=[
                {
                    "name": "input",
                    "shape": [1, 4],
                    "datatype": "FP32",
                    "data": [5.1, 3.5, 1.4, 0.2],
                }
            ]
        )
        ```

Triton answers with the v2 response:

```json
{
  "model_name": "irisonnx",
  "model_version": "1",
  "outputs": [
    {"name": "label", "datatype": "INT64", "shape": [1], "data": [0]}
  ]
}
```

`model_version` is the Triton version folder that served the request, which is independent of the Hopsworks model version.

For generative inference (vLLM), the request follows the [OpenAI specification](https://docs.vllm.ai/en/v0.28.0/serving/openai_compatible_server.html) supported by the vLLM OpenAI-compatible server.

!!! example "vLLM chat completions"
    === "Python"

        ```python
        import requests


        data = {
            "model": "my-llm",
            "messages": [{"role": "user", "content": "Hello, how are you?"}],
        }

        headers = {"authorization": "ApiKey <your_api_key>", "content-type": "application/json"}

        response = requests.post(
            "https://<ISTIO_GATEWAY_IP>/v1/my_project/my-llm/v1/chat/completions",
            headers=headers,
            json=data,
        )
        print(response.json())
        ```

    === "Curl"

        ```bash
        curl -X POST "https://<ISTIO_GATEWAY_IP>/v1/my_project/my-llm/v1/chat/completions" \
        -H "authorization: ApiKey <your_api_key>" \
        -H "content-type: application/json" \
        -d '{
                "model": "my-llm",
                "messages": [
                    {"role": "user", "content": "Hello, how are you?"}
                ]
            }'
        ```

### Binary tensor data

Triton's [binary tensor data extension](https://github.com/triton-inference-server/server/blob/main/docs/protocol/extension_binary_data.md) sends tensors as raw bytes after the JSON header, with the `Inference-Header-Content-Length` header giving the length of the JSON part.
Send such requests to the Istio path only.
The Hopsworks REST API takes the request body as JSON text, so it cannot forward binary tensor data.

## CORS

The Istio EnvoyFilter handles CORS preflight (`OPTIONS`) requests automatically. Allowed origins can be configured via `istio.envoyFilter.corsAllowedOrigins` in the Helm chart configuration.

## Response

The model returns predictions in a JSON object.
The response depends on the model server implementation.
Triton deployments return the v2 response shown in [Request Format](#request-format).
