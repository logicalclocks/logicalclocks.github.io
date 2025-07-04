---
description: Documentation on how to deployment Machine Learning (ML) models and Large Language Models (LLMs)
---

# How To Create A Model Deployment

## Introduction

In this guide, you will learn how to create a new deployment for a trained model.

!!! warning
    This guide assumes that a model has already been trained and saved into the Model Registry. To learn how to create a model in the Model Registry, see [Model Registry Guide](../registry/index.md#exporting-a-model)

Deployments are used to unify the different components involved in making one or more trained models online and accessible to compute predictions on demand. For each deployment, there are four concepts to consider:

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

Once in the deployments page, you can create a new deployment by either clicking on `New deployment` (if there are no existing deployments) or on `Create new deployment` it the top-right corner. Both options will open the deployment creation form.

### Step 2: Basic deployment configuration

A simplified creation form will appear including the most common deployment fields from all available configurations. We provide default values for the rest of the fields, adjusted to the type of deployment you want to create.

In the simplified form, select the model framework used to train your model. Then, select the model you want to deploy from the list of available models under `pick a model`.

After selecting the model, the rest of fields are filled automatically. We pick the last model version and model artifact version available in the Model Registry. Moreover, we infer the deployment name from the model name.

!!! notice "Deployment name validation rules"
    A valid deployment name can only contain characters a-z, A-Z and 0-9.

!!! info "Predictor script for Python models"
    For Python models, you must select a custom [predictor script](#predictor) that loads and runs the trained model by clicking on `From project` or `Upload new file`, to choose an existing script in the project file system or upload a new script, respectively.

If you prefer, change the name of the deployment, model version or [artifact version](#model-artifact). Then, click on `Create new deployment` to create the deployment for your model.

<p align="center">
  <figure>
    <img style="max-width: 55%; margin: 0 auto" src="../../../../assets/images/guides/mlops/serving/deployment_simple_form_1.png" alt="Select the model framework">
    <figcaption>Select the model framework</figcaption>
  </figure>
</p>

<p align="center">
  <figure>
    <img style="max-width: 55%; margin: 0 auto" src="../../../../assets/images/guides/mlops/serving/deployment_simple_form_2.png" alt="Select the model">
    <figcaption>Select the model</figcaption>
  </figure>
</p>

### Step 3 (Optional): Advanced configuration

Optionally, you can access and adjust other parameters of the deployment configuration by clicking on `Advanced options`.

<p align="center">
  <figure>
    <img style="max-width: 55%; margin: 0 auto" src="../../../../assets/images/guides/mlops/serving/deployment_simple_form_adv_options.png" alt="Advance options">
    <figcaption>Advanced options. Go to advanced deployment creation form</figcaption>
  </figure>
</p>

You will be redirected to a full-page deployment creation form where you can see all the default configuration values we selected for your deployment and adjust them according to your use case. Apart from the aforementioned simplified configuration, in this form you can setup the following components:

!!! info "Deployment advanced options"
    1. [Predictor](#predictor)
    2. [Transformer](#transformer)
    3. [Inference logger](predictor.md#inference-logger)
    4. [Inference batcher](predictor.md#inference-batcher)
    5. [Resources](predictor.md#resources)
    6. [API protocol](predictor.md#api-protocol)

Once you are done with the changes, click on `Create new deployment` at the bottom of the page to create the deployment for your model.

### Step 4: (Kueue enabled) Select a Queue

If the cluster is installed with Kueue enabled, you will need to select a queue in which the deployment should run. This can be done from `Advance configuration -> Scheduler section`.

![Default queue for job](../../../assets/images/guides/project/scheduler/job_queue.png)

### Step 5: Deployment creation

Wait for the deployment creation process to finish.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployment_creating.png" alt="Creating new deployment">
    <figcaption>Deployment creation in progress</figcaption>
  </figure>
</p>

### Step 6: Deployment overview

Once the deployment is created, you will be redirected to the list of all your existing deployments in the project. You can use the filters on the top of the page to easily locate your new deployment.

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

### Step 2: Create deployment

Retrieve the trained model you want to deploy.

=== "Python"
  ```python
  my_model = mr.get_model("my_model", version=1)
  ```

#### Option A: Using the model object

=== "Python"
  ```python
  my_deployment = my_model.deploy()
  ```

#### Option B: Using the Model Serving handle

=== "Python"
  ```python
  # get Hopsworks Model Serving handle
  ms = project.get_model_serving()

  my_predictor = ms.create_predictor(my_model)
  my_deployment = my_predictor.deploy()

  # or
  my_deployment = ms.create_deployment(my_predictor)
  my_deployment.save()
  ```

### API Reference

[Model Serving](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/model-serving/model_serving_api/)

## Model Files

Model files are the files exported when a specific version of a model is saved to the model registry (see [Model Registry](../registry/index.md)). These files are ==unique for each model version, but shared across model deployments== created for the same version of the model.

Inside a model deployment, the local path to the model files is stored in the `MODEL_FILES_PATH` environment variable (see [environment variables](../serving/predictor.md#environment-variables)). Moreover, you can explore the model files under the `/Models/<model-name>/<model-version>/Files` directory using the File Browser.

!!! warning
    All files under `/Models` are managed by Hopsworks. Changes to model files cannot be reverted and can have an impact on existing model deployments.

## Artifact Files

Artifact files are files involved in the correct startup and running of the model deployment. The most important files are the **predictor** and **transformer scripts**. The former is used to load and run the model for making predictions. The latter is typically used to apply transformations on the model inputs at inference time before making predictions. Predictor and transformer scripts run on separate components and, therefore, scale independently of each other.

!!! tip
    Whenever you provide a predictor script, you can include the transformations of model inputs in the same script as far as they don't need to be scaled independently from the model inference process.

Additionally, artifact files can also contain a **server configuration file** that helps detach configuration used within the model deployment from the model server or the implementation of the predictor and transformer scripts. Inside a model deployment, the local path to the configuration file is stored in the `CONFIG_FILE_PATH` environment variable (see [environment variables](../serving/predictor.md#environment-variables)).

Every model deployment runs a specific version of the artifact files, commonly referred to as artifact version. ==One or more model deployments can use the same artifact version== (i.e., same predictor and transformer scripts). Artifact versions are unique for the same model version.

When a new deployment is created, a new artifact version is generated in two cases:

- the artifact version in the predictor is set to `CREATE` (see [Artifact Version](../predictor/#artifact_version))
- no model artifact with the same files has been created before.

Inside a model deployment, the local path to the artifact files is stored in the `ARTIFACT_FILES_PATH` environment variable (see [environment variables](../serving/predictor.md#environment-variables)). Moreover, you can explore the artifact files under the `/Models/<model-name>/<model-version>/Artifacts/<artifact-version>` directory using the File Browser. 

!!! warning
    All files under `/Models` are managed by Hopsworks. Changes to artifact files cannot be reverted and can have an impact on existing model deployments.

!!! tip "Additional files"
    Currently, the artifact files can only include predictor and transformer scripts, and a configuration file. Support for additional files (e.g., other resources) is coming soon.

## Predictor

Predictors are responsible for running the model server that loads the trained model, listens to inference requests and returns prediction results. To learn more about predictors, see the [Predictor Guide](predictor.md)

!!! note
    Only one predictor is supported in a deployment.

!!! info
    Model artifacts are assigned an incremental version number, being `0` the version reserved for model artifacts that do not contain predictor or transformer scripts (i.e., shared artifacts containing only the model files).

## Transformer

Transformers are used to apply transformations on the model inputs before sending them to the predictor for making predictions using the model. To learn more about transformers, see the [Transformer Guide](transformer.md).

!!! warning
    Transformers are only supported in KServe deployments.
