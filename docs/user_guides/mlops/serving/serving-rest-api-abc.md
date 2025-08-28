---
description: Using Deployment REST API Server for inference
---
# Hopsworks Model Serving REST API Documentation

Hopsworks provides model serving using **KServe** as the deployment framework and **Istio** as the ingress gateway to the Kubernetes cluster.  

This document explains how to interact with a deployed model endpoint via REST.

---

## Base URL

The model is accessible through the Istio ingress gateway. The url to access the model is provided in the Hopsworks UI. The URL avaiable is in the following format.

```text
http://<ISTIO_GATEWAY_IP>/v1/models/<MODEL_NAME>:predict
```

- <ISTIO_GATEWAY_IP>: External IP address of the Istio ingress gateway (visible in Hopsworks UI).
- <MODEL_NAME>: The name of the deployed model in Hopsworks.


## Authentication

All requests must include an API Key for authentication.

Add the key to the Authorization header:

```text
Authorization: ApiKey <API_KEY>
```

```text
Example:
Authorization: ApiKey DqlLkPY8M2t3qvxx.YC2VsCnmPb6SuNOfY55sFgbJNf2o4bBeQHBC5ke0YMOieObL25pakIfs4F9BeW9x
```

## Headers

| Header          | Description                                 | Example Value                        |
| --------------- | ------------------------------------------- | ------------------------------------ |
| `Host`          | Model’s hostname, provided in Hopsworks UI. | `searchmodellookup.mfp.hopsworks.ai` |
| `Authorization` | API key for authentication.                 | `ApiKey <your_api_key>`              |
| `Content-Type`  | Request payload type (always JSON).         | `application/json`                   |

## Request Format

The request must be sent as a JSON object containing an instances field.

{
  "instances": [
    [
      "a3335a58-a3c8-4e8d-8232-40a047e5accc",
      "03ac1afa-9593-4979-becf-c310a0f56610"
    ]
  ]
}


import requests

data = {
    "instances": [
        [
            "a3335a58-a3c8-4e8d-8232-40a047e5accc",
            "03ac1afa-9593-4979-becf-c310a0f56610"
        ]
    ]
}

headers = {
    "Host": "searchmodellookup.mfp.hopsworks.ai",
    "Authorization": "ApiKey DqlLkPY8M2t3qvxx.YC2VsCnmPb6SuNOfY55sFgbJNf2o4bBeQHBC5ke0YMOieObL25pakIfs4F9BeW9x",
    "Content-Type": "application/json"
}

response = requests.post(
    "http://135.125.247.6/v1/models/searchmodellookup:predict",
    headers=headers,
    json=data
)

print(response.json())


curl -X POST "http://135.125.247.6/v1/models/searchmodellookup:predict" \
  -H "Host: searchmodellookup.mfp.hopsworks.ai" \
  -H "Authorization: ApiKey DqlLkPY8M2t3qvxx.YC2VsCnmPb6SuNOfY55sFgbJNf2o4bBeQHBC5ke0YMOieObL25pakIfs4F9BeW9x" \
  -H "Content-Type: application/json" \
  -d '{
        "instances": [
          [
            "a3335a58-a3c8-4e8d-8232-40a047e5accc",
            "03ac1afa-9593-4979-becf-c310a0f56610"
          ]
        ]
      }'


## Example Response

{
  "predictions": [
    "some_prediction_result"
  ]
}

