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

## Web UI

### Step 1: Create a deployment

If you have at least one model already trained and saved in the Model Registry, navigate to the model deployments page by clicking on `Model Deployments` in the navigation menu on the left.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployments_tab_sidebar.png" alt="Deployments navigation tab">
    <figcaption>Deployments navigation tab</figcaption>
  </figure>
</p>

Once in the model deployments page, click on `New model deployment` at the top of the page to open the deployment creation form.

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

!!! info "Deployment name validation rules"
    A valid deployment name can only contain characters a-z, A-Z and 0-9.

!!! info "Predictor script for Python models"
    For Python models, you must select a custom [predictor script](#predictor) that loads and runs the trained model by clicking on `From project`, `Upload new file` or `Create new file`, to choose an existing script in the project file system, upload a new script, or write one in place, respectively.

!!! info "Server configuration file for vLLM"
    For vLLM deployments, a server configuration file is required.
    See the [Predictor Guide](predictor.md#server-configuration-file) for more details.

Lastly, click on `Create` to create the deployment for your model.

### Step 3 (Optional): Advanced configuration

Optionally, you can access and adjust other parameters of the deployment configuration by clicking on `advanced options`.

<p align="center">
  <figure>
    <img style="max-width: 55%; margin: 0 auto" src="../../../../assets/images/guides/mlops/serving/deployment_simple_form_adv_options.png" alt="Advance options">
    <figcaption>Advanced options. Go to advanced deployment creation form</figcaption>
  </figure>
</p>
You will be redirected to a full-page deployment creation form, where you can review all default configuration values and customize them to fit your requirements.
In addition to the basic settings, this form allows you to further configure the [Predictor](#predictor) and [Transformer](#transformer) KServe components of your model deployment.

Once you are done with the changes, click on `Create new model deployment` at the bottom of the page to create the deployment for your model.

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

Create a deployment for your model by calling `.deploy()` on the model metadata object.
This will create a deployment for your model with default values.

=== "Python"

  ```python
  my_deployment = my_model.deploy()

  # optionally, start your model deployment
  my_deployment.start()
  ```

!!! info "Predictor script and server configuration file"
    You can provide a predictor script and a server configuration file directly in the `.deploy()` method using the `script_file` and `config_file` parameters. See the [Predictor Guide](predictor.md) for more details.

### Step 3b: Deploy a model with its feature view

A Python model registered with `feature_view=` deploys without a predictor script.
The default predictor looks up and transforms the features by serving key, runs the model, logs the request when the feature view has logging enabled, and validates every request against the deployment schema, which the client infers from the feature view.
Clients send only the serving keys and the features named in `passed_features`.

=== "Python"

    ```python
    fs = project.get_feature_store()
    feature_view = fs.get_feature_view("transactions", version=1)

    # register the trained model with the feature view it was trained on
    fraud_model = mr.python.create_model(name="fraud", feature_view=feature_view)
    fraud_model.save("model_dir")  # one .pkl or .joblib file inside

    fraud_deployment = fraud_model.deploy(
        name="fraud",
        passed_features=["amount"],  # sent by the client, not read from the online store
    )
    fraud_deployment.start(await_running=600)

    fraud_deployment.schema.describe()  # the request contract
    fraud_deployment.predict(inputs=[{"cc_num": 4473593503484549, "amount": 12.5}])
    ```

See the [Deployment Schema Guide][deployment-schema] for the request contract, the error codes, feature logging, and custom predictor scripts that subclass the default predictor.

### Step 3c: Deploy a feature view without a model

A feature view deploys on its own and returns the transformed feature vectors, for callers that run the model elsewhere.
The deployment pins the training dataset whose statistics the transformations use.

=== "Python"

    ```python
    feature_view = fs.get_feature_view("transactions", version=1)
    X_train, X_test, y_train, y_test = feature_view.train_test_split(test_size=0.2)

    fv_deployment = feature_view.deploy(
        name="transactionsfv",
        passed_features=["amount"],
    )
    fv_deployment.start(await_running=600)

    response = fv_deployment.predict(inputs=[{"cc_num": 4473593503484549, "amount": 12.5}])
    print(response["columns"], response["predictions"])
    ```

See the [Feature View Deployment Guide][feature-view-deployment].

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-method"></code> [`ModelRegistry.get_model`][hsml.model_registry.ModelRegistry.get_model]
    - <code class="doc-symbol doc-symbol-method"></code> [`Model.deploy`][hsml.model.Model.deploy]
    - <code class="doc-symbol doc-symbol-class"></code> [`Deployment`][hsml.deployment.Deployment]
        - <code class="doc-symbol doc-symbol-method"></code> [`start`][hsml.deployment.Deployment.start]
        - <code class="doc-symbol doc-symbol-method"></code> [`predict`][hsml.deployment.Deployment.predict]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>

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

Each deployment tracks its artifact files through a ==deployment version==, an integer (1, 2, 3...) that is incremented whenever the artifact content changes (e.g., updating a predictor script or configuration file).

Inside a model deployment, the local path to the artifact files is stored in the `ARTIFACT_FILES_PATH` environment variable (see [environment variables](../serving/predictor.md#environment-variables)).

Deployments with a deployment schema also keep the schema documents under `/Deployments/<deployment-name>/resources/schema/`, one set of files per schema content id.
These files are never modified, so a deployment revision always finds the schema it was created with; see [Revisions in the Deployment Schema Guide][deployment-schema-revisions].

!!! warning
    All files under `/Models` and `/Deployments` are managed by Hopsworks.
    Manual changes to these files cannot be reverted and can have an impact on existing model deployments.

## Predictor

Predictors are responsible for running the model server that loads the trained model, handles inference requests and returns prediction results.
To learn more about predictors and how to configure them, including [environment variables](predictor.md#environment-variables), [resources](predictor.md#resources), and [autoscaling](predictor.md#autoscaling), see the [Predictor (KServe) Guide](predictor.md).

## Transformer

Transformers are used to apply transformations on the model inputs before sending them to the predictor for making predictions using the model.
To learn more about transformers and how to configure them, including [environment variables](transformer.md#environment-variables), [resources](transformer.md#resources), and [autoscaling](transformer.md#autoscaling), see the [Transformer (KServe) Guide](transformer.md).

!!! warning
    Transformers are not available for vLLM deployments.
