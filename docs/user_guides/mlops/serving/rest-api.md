# Hopsworks Model Serving REST API

## Introduction

Hopsworks provides model serving using [KServe](https://kserve.github.io/website/) as the deployment framework and [Istio]() as the ingress gateway to the Kubernetes cluster. 

This document explains how to interact with a deployed model endpoint via REST.

## Base URL

The deployed model is accessible through the Istio ingress gateway. The URL to access the model is provided on the deployment page inside the Hopsworks UI. 

The URL follows this format:
```text
http://<ISTIO_GATEWAY_IP>/v1/models/<DEPLOYMENT_NAME>:predict
```

- `<ISTIO_GATEWAY_IP>`: External IP address of the Istio ingress gateway.
- `<DEPLOYMENT_NAME>`: The name of the deployment.

<p align="center">
  <figure>
    <img  style="max-width: 100%; margin: 0 auto" src="../../../../assets/images/guides/mlops/serving/deployment_endpoints.png" alt="Endpoints">
    <figcaption>Deployment Endpoints</figcaption>
  </figure>
</p>


## Authentication

All requests must include an API Key for authentication. You can create an API by following this [guide](../../projects/api_key/create_api_key.md). 

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

The request must be sent as a JSON object containing an `inputs` or `instances` field. You can find more information on the request format [here](https://kserve.github.io/website/docs/concepts/architecture/data-plane/v1-protocol#request-format).

=== "Python"
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

## Example Response

The model returns predictions in a JSON object. You can find more information [here](https://kserve.github.io/website/docs/concepts/architecture/data-plane/v1-protocol#response-format).

```json
{
  "predictions": [
    "some_prediction_result"
  ]
}
```