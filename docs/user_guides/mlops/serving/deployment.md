---
description: Documentation on how to deployment Machine Learning (ML) models and Large Language Models (LLMs)
---

# How To Create A Model Deployment

## Introduction

In this guide, you will learn how to create a new deployment for a trained model.

!!! info
    This guide covers model deployments, which require a model saved in the Model Registry.
    To learn how to create a model in the Model Registry, see [Model Registry Guide](../registry/index.md#exporting-a-model).
    For Python deployments (running a Python script without a model artifact), see [Python Deployments](../../projects/python-deployment/python-deployment.md).

Model deployments are used to unify the different components involved in making one or more trained models online and accessible to compute predictions on demand.
For each model deployment, there are four concepts to understand:

!!! info ""
    1. [Model files](#model-files)
    2. [Artifact files](#artifact-files)
    3. [Predictor](#predictor)
    4. [Transformer](#transformer)

## GUI

### Step 1: Create a deployment

If you have at least one model already trained and saved in the Model Registry, navigate to the deployments page by clicking on the `Deployments` tab on the navigation menu on the left.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployments_tab_sidebar.png" alt="Deployments navigation tab">
    <figcaption>Deployments navigation tab</figcaption>
  </figure>
</p>

Once in the deployments page, you can create a new deployment by either clicking on `New deployment` (if there are no existing deployments) or on `Create new deployment` it the top-right corner.
Both options will open the deployment creation form.

### Step 2: Basic deployment configuration

A simplified creation form will appear including the most common deployment fields from all available configurations.
We provide default values for the rest of the fields, adjusted to the type of deployment you want to create.

In the simplified form, choose the model server that will be used to serve your model.

<p align="center">
  <figure>
    <img style="max-width: 55%; margin: 0 auto" src="../../../../assets/images/guides/mlops/serving/deployment_simple_form_1.png" alt="Select the model server">
    <figcaption>Select the model server</figcaption>
  </figure>
</p>

Then, select the model you want to deploy from the list of available models under `pick a model`.

<p align="center">
  <figure>
    <img style="max-width: 55%; margin: 0 auto" src="../../../../assets/images/guides/mlops/serving/deployment_simple_form_2.png" alt="Select the model">
    <figcaption>Select the model</figcaption>
  </figure>
</p>

After selecting the model, select a model version and give your model deployment a name.

!!! notice "Deployment name validation rules"
    A valid deployment name can only contain characters a-z, A-Z and 0-9.

!!! info "Predictor script for Python models"
    For Python models, you must select a custom [predictor script](#predictor) that loads and runs the trained model by clicking on `From project` or `Upload new file`, to choose an existing script in the project file system or upload a new script, respectively.

!!! info "Server configuration file for vLLM"
    For vLLM deployments, a server configuration file is required.
    See the [Predictor Guide](predictor.md#server-configuration-file) for more details.

Lastly, click on `Create new deployment` to create the deployment for your model.

### Step 3 (Optional): Advanced configuration

Optionally, you can access and adjust other parameters of the deployment configuration by clicking on `Advanced options`.

<p align="center">
  <figure>
    <img style="max-width: 55%; margin: 0 auto" src="../../../../assets/images/guides/mlops/serving/deployment_simple_form_adv_options.png" alt="Advance options">
    <figcaption>Advanced options. Go to advanced deployment creation form</figcaption>
  </figure>
</p>
You will be redirected to a full-page deployment creation form, where you can review all default configuration values and customize them to fit your requirements. In addition to the basic settings, this form allows you to further configure the [Predictor](#predictor) and [Transformer](#transformer) KServe components of your model deployment.

Once you are done with the changes, click on `Create new deployment` at the bottom of the page to create the deployment for your model.

### Step 4: Deployment creation

Wait for the deployment creation process to finish.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployment_creating.png" alt="Creating new deployment">
    <figcaption>Deployment creation in progress</figcaption>
  </figure>
</p>

### Step 5: Deployment overview

Once the deployment is created, you will be redirected to the list of all your existing deployments in the project.
You can use the filters on the top of the page to easily locate your new deployment.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployments_list.png" alt="List of deployments">
    <figcaption>List of deployments</figcaption>
  </figure>
</p>

After that, click on the new deployment to access the overview page.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployment_overview.png" alt="Deployment overview">
    <figcaption>Deployment overview</figcaption>
  </figure>
</p>

## Code

### Step 1: Connect to Hopsworks

=== "Python"

  ```python
  import hopsworks

  project = hopsworks.login()

  # get Hopsworks Model Registry handle
  mr = project.get_model_registry()
  ```

### Step 2: Retrieve your trained model

Retrieve the trained model you want to deploy using the Model Registry handle.

=== "Python"

  ```python
  my_model = mr.get_model("my_model", version=1)

  ```

### Step 3: Deploy your trained model

Create a deployment for your model by calling `.deploy()` on the model metadata object. This will create a deployment for your model with default values.

=== "Python"

  ```python
  my_deployment = my_model.deploy()

  # optionally, start your model deployment
  my_deployment.start()
  ```

!!! info "Predictor script and server configuration file"
    You can provide a predictor script and a server configuration file directly in the `.deploy()` method using the `script_file` and `config_file` parameters. See the [Predictor Guide](predictor.md) for more details.

### API Reference

[`ModelServing`][hsml.model_serving.ModelServing]

## Model Files

Model files are the files exported when a specific version of a model is saved to the model registry (see [Model Registry](../registry/index.md)).
These files are ==unique for each model version, but shared across model deployments== created for the same version of the model.

Inside a model deployment, the local path to the model files is stored in the `MODEL_FILES_PATH` environment variable (see [environment variables](../serving/predictor.md#environment-variables)).
Moreover, you can explore the model files under the `/Models/<model-name>/<model-version>/Files` directory using the File Browser.

!!! warning
    All files under `/Models` and `/Deployments` are managed by Hopsworks.
    Manual changes to these files cannot be reverted and can have an impact on existing model deployments.

## Artifact Files

Artifact files are essential for the proper initialization and operation of a model deployment. The most critical artifact files are the **predictor** and **transformer scripts**. The predictor script loads the trained model and handles prediction requests, while the transformer script applies any necessary input transformations before inference.
Predictor and transformer scripts run on separate components and, therefore, scale independently of each other.

!!! tip
    Whenever you provide a predictor script, you can include the transformations of model inputs in the same script as far as they don't need to be scaled independently from the model inference process.

Additionally, artifact files can also contain a **server configuration file** that helps detach configuration used within the model deployment from the model server or the implementation of the predictor and transformer scripts.
Inside a model deployment, the local path to the configuration file is stored in the `CONFIG_FILE_PATH` environment variable (see [environment variables](../serving/predictor.md#environment-variables)).

Each deployment tracks its artifact files through a ==deployment version== — an integer (1, 2, 3...) that is incremented whenever the artifact content changes (e.g., updating a predictor script or configuration file).

Inside a model deployment, the local path to the artifact files is stored in the `ARTIFACT_FILES_PATH` environment variable (see [environment variables](../serving/predictor.md#environment-variables)).

!!! warning
    All files under `/Models` and `/Deployments` are managed by Hopsworks.
    Manual changes to these files cannot be reverted and can have an impact on existing model deployments.

!!! tip "vLLM omni mode"
    For vLLM deployments, the server configuration file supports a `#HOPSWORKS omni: true` directive to enable omni mode.

## Predictor

Predictors are responsible for running the model server that loads the trained model, handles inference requests and returns prediction results.
To learn more about predictors, see the [Predictor (KServe) Guide](predictor.md)

## Transformer

Transformers are used to apply transformations on the model inputs before sending them to the predictor for making predictions using the model.
To learn more about transformers, see the [Transformer (KServe) Guide](transformer.md).

!!! warning
    Transformers are not available for vLLM deployments.
