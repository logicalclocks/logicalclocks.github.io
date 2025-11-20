# Hopsworks Model Serving REST API

## Introduction

Hopsworks provides model serving capabilities by leveraging [KServe](https://kserve.github.io/website/) as the model serving platform and [Istio](https://istio.io/) as the ingress gateway to the model deployments.

This document explains how to interact with a model deployment via REST API.

## Base URL

Deployed models are accessible through the Istio ingress gateway.
The URL to interact with a model deployment is provided on the model deployment page in the Hopsworks UI.

The URL follows the format `http://<ISTIO_GATEWAY_IP>/<RESOURCE_PATH>`, where `RESOURCE_PATH` depends on the [model server](https://docs.hopsworks.ai/latest/user_guides/mlops/serving/predictor/#model-server) (e.g., vLLM, TensorFlow Serving, SKLearn ModelServer).

<p align="center">
  <figure>
    <img  style="max-width: 100%; margin: 0 auto" src="../../../../assets/images/guides/mlops/serving/deployment_endpoints.png" alt="Endpoints">
    <figcaption>Deployment Endpoints</figcaption>
  </figure>
</p>

## Authentication

All requests must include an API Key for authentication.
You can create an API by following this [guide](../../projects/api_key/create_api_key.md).

Include the key in the Authorization header:

```text
Authorization: ApiKey <API_KEY_VALUE>
```

## Headers

| Header          | Description                                 | Example Value                        |
| --------------- | ------------------------------------------- | ------------------------------------ |
| `Host`          | Model’s hostname, provided in Hopsworks UI. | `fraud.test.hopsworks.ai` |
| `Authorization` | API key for authentication.                 | `ApiKey <your_api_key>`              |
| `Content-Type`  | Request payload type (always JSON).         | `application/json`                   |

## Request Format

The request format depends on the model sever being used.

For predictive inference (i.e., for Tensorflow or SkLearn or Python Serving).
The request must be sent as a JSON object containing an `inputs` or `instances` field.
You can find more information on the request format [here](https://kserve.github.io/website/docs/concepts/architecture/data-plane/v1-protocol#request-format).
An example for this is given below.

=== "Python"

    !!! example "REST API example for Predictive Inference (Tensorflow or SkLearn or Python Serving)"
        ```python
        import requests

        data = {
            "inputs": [
                [
                    4641025220953719,
                    4920355418495856
                ]
            ]
        }

        headers = {
            "Host": "fraud.test.hopsworks.ai",
            "Authorization": "ApiKey 8kDOlnRlJU4kiV1Y.RmFNJY3XKAUSqmJZ03kbUbXKMQSHveSBgMIGT84qrM5qXMjLib7hdlfGeg8fBQZp",
            "Content-Type": "application/json"
        }

        response = requests.post(
            "http://10.87.42.108/v1/models/fraud:predict",
            headers=headers,
            json=data
        )
        print(response.json())
        ```

=== "Curl"

    !!! example "REST API example for Predictive Inference (Tensorflow or SkLearn or Python Serving)"
        ```bash
        curl -X POST "http://10.87.42.108/v1/models/fraud:predict" \
          -H "Host: fraud.test.hopsworks.ai" \
          -H "Authorization: ApiKey 8kDOlnRlJU4kiV1Y.RmFNJY3XKAUSqmJZ03kbUbXKMQSHveSBgMIGT84qrM5qXMjLib7hdlfGeg8fBQZp" \
          -H "Content-Type: application/json" \
          -d '{
                "inputs": [
                  [
                    4641025220953719,
                    4920355418495856
                  ]
                ]
              }'
        ```

For generative inference (i.e vLLM) the response follows the [OpenAI specification](https://platform.openai.com/docs/api-reference/chat/create).

## Response

The model returns predictions in a JSON object.
The response depends on the model server implementation.
You can find more information regarding specific model servers in the [Kserve documentation](https://kserve.github.io/website/docs/intro).
