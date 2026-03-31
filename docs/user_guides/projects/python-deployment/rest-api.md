---
description: Documentation on how to interact with a Python deployment via REST API
---

# Python Deployment REST API

## Introduction

Python deployments are accessible via REST API through the [Istio](https://istio.io/) ingress gateway.

This document explains how to send requests to a Python deployment.

!!! tip "Tutorials"
    End-to-end examples are available in the [hopsworks-tutorials](https://github.com/logicalclocks/hopsworks-tutorials/tree/master) repository.

## Sending Requests through Istio Ingress

The full URL path is constructed by combining a base path with a resource path available in the Python server.
See [URL Paths](#url-paths) for the complete URL format and examples.

### Authentication

All requests must include an API Key for authentication.
You can create an API key by following this [guide](../../projects/api_key/create_api_key.md).

Include the key in the `authorization` header:

```text
authorization: ApiKey <API_KEY_VALUE>
```

### Headers

| Header          | Description                 | Example Value           |
| --------------- | --------------------------- | ----------------------- |
| `authorization` | API key for authentication. | `ApiKey <your_api_key>` |
| `content-type`  | Request payload type.       | `application/json`      |

## URL Paths

Python deployments are accessible through the ==Istio ingress gateway== using **path-based** routing.
The full URL is constructed by combining the base URL with the paths defined in your Python server.

!!! example ""
    **`<base_url>/<path>`**

Where `<path>` depends entirely on the routes defined in your Python server implementation (e.g., `/echo`, `/predict`, `/health`).

### Base URL

The base URL is composed of the **Istio ingress gateway IP**, the **project name**, and the **deployment name**.

!!! example ""
    **`https://<ISTIO_GATEWAY_IP>/v1/<project_name>/<deployment_name>`**

!!! warning "Host-based routing (legacy)"
    Prior to path-based routing, requests were routed using a `Host` header matching the deployment hostname, and **`https://<ISTIO_GATEWAY_IP>`** as base url.

    ```
    Host: <deployment-name>.<project-name>.<knative-domain-name>
    ```

    Each deployment gets its own Knative-generated hostname, and routing depends on the `Host` header matching Istio ingress gateway rules.

    Path-based routing (described above) is the preferred method for external access.

!!! tip "Hopsworks Python API"

    The endpoint URL can be retrieved using the `Deployment` class.

    ```python
    # Returns: https://<istio-host>/v1/<project>/<deployment>
    endpoint_url = deployment.get_endpoint_url()
    ```

## Request Format

The request format depends entirely on your Python server implementation.
There are no framework or protocol constraints — your server defines the expected HTTP methods, paths, and payload format.

!!! example "REST API example"
    === "Python"

        ```python
        import requests

        url = deployment.get_endpoint_url()

        response = requests.post(f"{url}/echo", json={"key": "value"})
        print(response.json())
        ```

    === "Curl"

        ```bash
        curl -X POST "https://<ISTIO_GATEWAY_IP>/v1/my_project/pyserver/echo" \
          -H "authorization: ApiKey <your_api_key>" \
          -H "content-type: application/json" \
          -d '{"key": "value"}'
        ```

## CORS

The Istio EnvoyFilter handles CORS preflight (`OPTIONS`) requests automatically.
Allowed origins can be configured via `istio.envoyFilter.corsAllowedOrigins` in the Helm chart configuration.

## Response

The response format depends on your Python server implementation.
