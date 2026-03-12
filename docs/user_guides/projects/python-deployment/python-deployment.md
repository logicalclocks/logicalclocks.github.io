---
description: Documentation on how to create Python deployments
---

# Python Deployment

## Introduction

Python deployments allow you to deploy a Python script as a service without requiring a model artifact in the Model Registry.
This is useful for custom inference pipelines, feature view deployments, or any Python-based program that needs to be served behind an HTTP endpoint.

!!! warning "Incoming requests are directed to port 8080"
    Python deployments run your script directly on port 8080.
    Therefore, make sure your implementation listens to 8080 port for handling incoming requests.

!!! info "gRPC protocol not supported"

!!! tip "Use your favourite HTTP server"
    There are no constraints on the framework or library used — you can use Flask, FastAPI, or any other HTTP server.

In each Python deployment, you can configure the following:

!!! info ""
    1. [Python environments](#python-environments)
    2. [Resources](#resources)
    3. [Autoscaling](#autoscaling)
    4. [Scheduling](#scheduling)

## Web UI

### Step 1: Create new deployment

Navigate to the deployments page by clicking on the `Deployments` tab on the navigation menu on the left.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployments_tab_sidebar.png" alt="Deployments navigation tab">
    <figcaption>Deployments navigation tab</figcaption>
  </figure>
</p>

Then, click on `New Python deployment`.

### Step 2: Configure the deployment

Choose a name for your Python deployment. Then, provide the script for you Python program by clicking on `From project` or `Upload new file`.

### Step 3 (Optional): Change Python environment

Python deployments run the scripts in one of the [Python Environments](../../projects/python/python_env_overview.md) available in your project. This environment must have all the necessary dependencies for your Python program.

Hopsworks provide a collection of built-in environments like `minimal-inference-pipeline`, `pandas-inference-pipeline` or `torch-inference-pipeline` with different sets of libraries pre-installed.
By default, the `pandas-inference-pipeline` Python environment is used in Python deployments.

To create your own environment it is recommended to [clone](../../projects/python/python_env_clone.md) the `minimal-inference-pipeline` or `pandas-inference-pipeline` environment and install additional dependencies needed for your Python program.

<p align="center">
  <figure>
    <img style="max-width: 55%; margin: 0 auto" src="../../../../../assets/images/guides/mlops/serving/deployment_simple_form_py_endp_env.png" alt="Python script in the simplified deployment form">
    <figcaption>Select an environment for the Python program</figcaption>
  </figure>
</p>

### Step 4 (Optional): Advanced configuration

Click on `Advanced options` to configure your Python deployment further, including:

!!! info ""
    1. [Resources](#resources)
    2. [Autoscaling](#autoscaling)
    3. [Scheduling](#scheduling)

Once you are done with the changes, click on `Create new Python deployment` at the bottom of the page to create the Python deployment.

## Code

### Step 1: Connect to Hopsworks

=== "Python"

    ```python
    import hopsworks

    project = hopsworks.login()

    # get Hopsworks Model Serving handle
    ms = project.get_model_serving()
    ```

### Step 2: Implement a Python script

=== "Python"

    ```python
    import uvicorn
    from fastapi import FastAPI

    app = FastAPI()


    @app.get("/ping")
    async def ping():
        return {"status": "ready"}


    @app.post("/echo")
    async def echo(data: dict):
        return data


    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8080)
    ```

!!! info "Jupyter magic"
    In a jupyter notebook, you can add `%%writefile python_server.py` at the top of the cell to save it as a local file.

### Step 3: Upload the script to your project

=== "Python"

    ```python
    import os

    dataset_api = project.get_dataset_api()

    uploaded_file_path = dataset_api.upload("python_server.py", "Resources", overwrite=True)
    script_path = os.path.join("/Projects", project.name, uploaded_file_path)
    ```

### Step 4: Create a deployment

=== "Python"

    ```python
    py_server = ms.create_endpoint(
        name="pyserver",
        script_file=script_path
    )
    py_deployment = py_server.deploy()
    ```

### Step 5: Send requests

=== "Python"

    ```python
    import requests

    url = py_deployment.get_endpoint_url()

    response = requests.post(f"{url}/echo", json={"key": "value"})
    print(response.json())
    ```

## Environment variables

A number of different environment variables is available in the Python deployment to ease its implementation.

!!! tip "Available environment variables"

    === "Deployment"

        These variables are available in all deployments.

        | Name                  | Description                      |
        | --------------------- | -------------------------------- |
        | `DEPLOYMENT_NAME`     | Name of the current deployment   |
        | `DEPLOYMENT_VERSION`  | Version of the deployment        |
        | `ARTIFACT_FILES_PATH` | Local path to the artifact files |

    === "Python deployment"

        These variables are specific to Python deployments.

        | Name               | Description                                        |
        | ------------------ | -------------------------------------------------- |
        | `SCRIPT_PATH`      | Full path to the Python script                     |
        | `SCRIPT_NAME`      | Prefixed filename of the Python script             |
        | `CONFIG_FILE_PATH` | Local path to the configuration file (if provided) |

    === "Others"

        These variables are available in all deployments.

        | Name                     | Description                                        |
        | ------------------------ | -------------------------------------------------- |
        | `REST_ENDPOINT`          | Hopsworks REST API endpoint                        |
        | `HOPSWORKS_PROJECT_ID`   | ID of the project                                  |
        | `HOPSWORKS_PROJECT_NAME` | Name of the project                                |
        | `HOPSWORKS_PUBLIC_HOST`  | Hopsworks public hostname                          |
        | `API_KEY`                | API key for authenticating with Hopsworks services |
        | `PROJECT_ID`             | Project ID (for Feature Store access)              |
        | `PROJECT_NAME`           | Project name (for Feature Store access)            |
        | `SECRETS_DIR`            | Path to secrets directory (`/keys`)                |
        | `MATERIAL_DIRECTORY`     | Path to TLS certificates (`/certs`)                |
        | `REQUESTS_VERIFY`        | SSL verification setting                           |

## Python environments

Python deployments run in one of the `*-inference-pipeline` Python environments available in your project.
Hopsworks provides built-in environments like `minimal-inference-pipeline`, `pandas-inference-pipeline` or `torch-inference-pipeline` with different sets of libraries pre-installed. By default, the `pandas-inference-pipeline` environment is used.

To create your own environment, it is recommended to [clone](../../projects/python/python_env_clone.md) the `minimal-inference-pipeline` or `pandas-inference-pipeline` environment and install additional dependencies needed for your Python program.
To learn more about Python environments, see [Python Environments](../../projects/python/python_env_overview.md).

## Resources

Configure CPU, memory, and GPU allocation for your Python deployment. Each deployment component has separate request and limit values.

For full details on resource configuration, see the [Resources Guide](../../mlops/serving/resources.md).

## Autoscaling

Deployments use **Knative Pod Autoscaler (KPA)** to automatically scale the number of replicas based on traffic. You can configure the minimum and maximum number of instances as well as the scale metric (requests per second or concurrency).

For full details on autoscaling parameters, see the [Autoscaling Guide](../../mlops/serving/autoscaling.md).

## Scheduling

!!! info "Kueue is required"
    This feature requires Kueue to be enabled in your cluster. If Kueue is not available, queue and topology options will not be accessible.

If the cluster has Kueue enabled, you can select a queue for your deployment from the advanced configuration. Queues control resource allocation and scheduling priority across the cluster.

For full details on scheduling configuration, see the [Scheduling Guide](../../mlops/serving/scheduling.md).
