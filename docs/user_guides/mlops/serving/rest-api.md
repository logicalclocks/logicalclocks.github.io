# Hopsworks Model Serving REST API

## Introduction

Hopsworks provides ==model serving capabilities== by leveraging [KServe](https://kserve.github.io/website/) as the model serving platform and [Istio](https://istio.io/) as the ingress gateway to the model deployments.

This document explains how to interact with a model deployment via REST API.

!!! tip "Tutorials"
    End-to-end examples are available in the [hopsworks-tutorials](https://github.com/logicalclocks/hopsworks-tutorials/tree/master) repository.

## Sending Inference Requests through Istio Ingress

The full inference URL is constructed by combining a base path with a model server-specific suffix. See [URL Paths](#url-paths) for the complete URL format and examples.

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
| `content-type`  | Request payload type (always JSON). | `application/json`      |

## URL Paths

Deployed models are accessible through the ==Istio ingress gateway== using **path-based** routing. The full URL is constructed by combining the base path with a model server-specific suffix.
This URL is also provided on the model deployment page in the Hopsworks UI.

!!! example ""
    **`<base_url>/<server-specific_suffix>`**

Where `server-specific_suffix` depends on the model server type (see [ML Inference Paths](#ml-inference) or [OpenAI-compatible Paths](#openai-compatible)).

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

### OpenAI-compatible

==vLLM deployments== provide an OpenAI API-compatible endpoint at `<base_url>/v1/`, allowing you to send any standard OpenAI API request to the vLLM server.

!!! example "e.g., Chat Completions endpoint"
    **`<base_url>/v1/chat/completions`**

Refer to the official [vLLM OpenAI-compatible server documentation](https://docs.vllm.ai/en/v0.10.2/serving/openai_compatible_server.html) for details about the available APIs.

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

For generative inference (vLLM), the request follows the [OpenAI specification](https://docs.vllm.ai/en/v0.10.2/serving/openai_compatible_server.html) supported by the vLLM OpenAI-compatible server.

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

## CORS

The Istio EnvoyFilter handles CORS preflight (`OPTIONS`) requests automatically. Allowed origins can be configured via `istio.envoyFilter.corsAllowedOrigins` in the Helm chart configuration.

## Response

The model returns predictions in a JSON object.
The response depends on the model server implementation.
