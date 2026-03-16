---
description: Documentation on how to configure a KServe transformer for a model deployment
---

# How To Configure A Transformer

## Introduction

In this guide, you will learn how to configure a transformer script in a model deployment.

Transformer scripts are used to apply transformations on the model inputs before sending them to the predictor for making predictions using the model.
They are user-provided Python scripts (`.py` or `.ipynb`) implementing the [Transformer class](#step-2-implement-transformer-script).

!!! info "Transformer scripts are not supported in vLLM deployments."

!!! tip "Independent scaling"
    The transformer has independent resources and autoscaling configuration from the predictor.
    This allows you to scale the pre/post-processing separately from the model inference.

A transformer has the following configurable components:

!!! info ""
    1. [Transformer script](#transformer-script)
    2. [Resources](#resources)
    3. [Autoscaling](#autoscaling)
    4. [Python environments](#python-environments)
    5. [Environment variables](#environment-variables)

See examples of transformer scripts in the serving [example notebooks](https://github.com/logicalclocks/hops-examples/blob/master/notebooks/ml/serving).

## Web UI

### Step 1: Create new deployment

If you have at least one model already trained and saved in the Model Registry, navigate to the deployments page by clicking on the `Deployments` tab on the navigation menu on the left.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployments_tab_sidebar.png" alt="Deployments navigation tab">
    <figcaption>Deployments navigation tab</figcaption>
  </figure>
</p>

Once in the deployments page, you can create a new deployment by either clicking on `New deployment` (if there are no existing deployments) or on `Create new deployment` it the top-right corner.
Both options will open the deployment creation form.

### Step 2: Go to advanced options

A simplified creation form will appear including the most common deployment fields from all available configurations.
Transformers are part of the advanced options of a deployment.
To navigate to the advanced creation form, click on `Advanced options`.

<p align="center">
  <figure>
    <img style="max-width: 55%; margin: 0 auto" src="../../../../assets/images/guides/mlops/serving/deployment_simple_form_adv_options.png" alt="Advance options">
    <figcaption>Advanced options. Go to advanced deployment creation form</figcaption>
  </figure>
</p>

### Step 3: Select a transformer script

If the transformer script is already located in Hopsworks, click on `From project` and navigate through the file system to find your script.
Otherwise, you can click on `Upload new file` to upload the transformer script now.

<p align="center">
  <figure>
    <img style="max-width: 85%; margin: 0 auto" src="../../../../assets/images/guides/mlops/serving/deployment_adv_form_trans.png" alt="Transformer script in advanced deployment form">
    <figcaption>Choose a transformer script in the advanced deployment form</figcaption>
  </figure>
</p>

After selecting the transformer script, you can optionally configure resources and autoscaling for your transformer (see [Step 4](#step-4-optional-other-advanced-options)).
Otherwise, click on `Create new deployment` to create the deployment for your model.

### Step 4 (Optional): Other advanced options

In this page, you can also configure the [resources](resources.md) to be allocated for the transformer, as well as the [autoscaling](autoscaling.md) parameters to control how the transformer scales based on traffic.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployment_adv_form_res_trans.png" alt="Resource allocation for the transformer">
    <figcaption>Resource allocation for the transformer</figcaption>
  </figure>
</p>

Once you are done with the changes, click on `Create new deployment` at the bottom of the page to create the deployment for your model.

## Code

### Step 1: Connect to Hopsworks

=== "Python"

  ```python
  import hopsworks


  project = hopsworks.login()

  # get Dataset API instance
  dataset_api = project.get_dataset_api()

  # get Hopsworks Model Registry handle
  mr = project.get_model_registry()
  ```

### Step 2: Implement transformer script

=== "Transformer"

    ```python
    class Transformer:
        def __init__(self):
            """Initialization code goes here"""
            # Optional __init__ params: project, deployment, model, async_logger
            pass

        def preprocess(self, inputs):
            """Transform the requests inputs here. The object returned by this method will be used as model input to make predictions."""
            return inputs

        def postprocess(self, outputs):
            """Transform the predictions computed by the model before returning a response"""
            return outputs
    ```

!!! tip "Optional `__init__` parameters"
    The `__init__` method supports optional parameters that are automatically injected at runtime:

    | Parameter      | Class                | Description                                            |
    | -------------- | -------------------- | ------------------------------------------------------ |
    | `project`      | `Project`            | Hopsworks project handle                               |
    | `deployment`   | `Deployment`         | Current model deployment handle                        |
    | `model`        | `Model`              | Model handle                                           |
    | `async_logger` | `AsyncFeatureLogger` | Async feature logger for logging features to Hopsworks |

    You can add any combination of these parameters to your `__init__` method:

    ```python
    class Transformer:
        def __init__(self, project, model):
            # Access the project and model directly
            self.project = project
            self.model_metadata = model
    ```

!!! info "Jupyter magic"
    In a jupyter notebook, you can add `%%writefile my_transformer.py` at the top of the cell to save it as a local file.

### Step 3: Upload the script to your project

!!! info "You can also use the UI to upload your transformer script. See [above](#step-3-select-a-transformer-script)"

=== "Python"

  ```python
  uploaded_file_path = dataset_api.upload(
      "my_transformer.py", "Resources", overwrite=True
  )
  transformer_script_path = os.path.join(
      "/Projects", project.name, uploaded_file_path
  )
  ```

### Step 4: Define a transformer

=== "Python"

  ```python
  my_transformer = ms.create_transformer(script_file=uploaded_file_path)

  # or

  from hsml.transformer import Transformer

  my_transformer = Transformer(script_file)
  ```

### Step 5: Create a deployment with the transformer

Use the `transformer` parameter to set the transformer configuration when creating the model deployment.

=== "Python"

  ```python
  my_model = mr.get_model("my_model", version=1)

  my_deployment = my_model.deploy(
      transformer=my_transformer
  )
  ```

### API Reference

[`Transformer`][hsml.transformer.Transformer]

## Transformer script

A transformer script is a custom Python script to apply pre/post-processing on the model inputs and outputs.
This script is included in the [artifact files](../serving/deployment.md#artifact-files) of the deployment.
The script must implement the `Transformer` class, as shown in [Step 2](#step-2-implement-transformer-script).

!!! info "Transformer scripts are not supported in vLLM deployments."

## Resources

Resources include the number of replicas for the deployment as well as the resources (i.e., memory, CPU, GPU) to be allocated per replica.

To learn about the different combinations available, see the [Resources Guide](resources.md).

## Autoscaling

The transformer has independent autoscaling from the predictor.
Deployments use Knative Pod Autoscaler (KPA) to automatically scale the number of replicas based on traffic, including scale-to-zero.

To learn about the different autoscaling parameters, see the [Autoscaling Guide](autoscaling.md).

## Environment variables

A number of different environment variables is available in the transformer to ease its implementation.

!!! tip "Available environment variables"

    === "Deployment"

        These variables are available in all deployments.

        | Name                  | Description                      |
        | --------------------- | -------------------------------- |
        | `DEPLOYMENT_NAME`     | Name of the current deployment   |
        | `DEPLOYMENT_VERSION`  | Version of the deployment        |
        | `ARTIFACT_FILES_PATH` | Local path to the artifact files |

    === "Transformer"

        These variables are set for transformer components.

        | Name               | Description                                        |
        | ------------------ | -------------------------------------------------- |
        | `SCRIPT_PATH`      | Full path to the transformer script                |
        | `SCRIPT_NAME`      | Prefixed filename of the transformer script        |
        | `CONFIG_FILE_PATH` | Local path to the configuration file (if provided) |
        | `IS_TRANSFORMER`   | Set to `true` for transformer components           |

    === "Model"

        | Name            | Description                                                 |
        | --------------- | ----------------------------------------------------------- |
        | `MODEL_NAME`    | Name of the model being served by the current deployment    |
        | `MODEL_VERSION` | Version of the model being served by the current deployment |

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

Transformer scripts always run on `*-inference-pipeline` Python environments.
To create a new Python environment see [Python Environments](../../projects/python/python_env_overview.md).

!!! note
    For **Python model deployments**, the same Python environment is used for both predictor and transformer.

!!! info "Supported Python environments"

    | Model server         | Predictor                        | Transformer                      |
    | -------------------- | -------------------------------- | -------------------------------- |
    | Python               | any `*-inference-pipeline` image | any `*-inference-pipeline` image |
    | KServe sklearnserver | `sklearnserver`                  | any `*-inference-pipeline` image |
    | TensorFlow Serving   | `tensorflow/serving`             | any `*-inference-pipeline` image |
    | vLLM                 | `vllm-openai`                    | Not supported                    |
