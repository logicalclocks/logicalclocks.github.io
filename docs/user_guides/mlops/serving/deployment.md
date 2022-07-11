# How To Create A Deployment

## Introduction

In this guide, you will learn how to create a new deployment for a trained model.

!!! warning
    This guide assumes that a model has already been trained and saved into the Model Registry. To learn how to create a model in the Model Registry, see [Model Registry Guide](../registry/frameworks/tf.md)

Deployments are used to unify the different components involved in making one or more trained models online and accessible to compute predictions on demand. In each deployment, there are three main components to consider:

!!! info ""
    1. [Model artifact](#model-artifact)
    2. [Predictor](#predictor)
    3. [Transformer](#transformer)

## GUI

### Step 1: Create a deployment

If you have at least one model already trained and saved in the Model Registry, navigate to the deployments page by clicking on the `Deployments` tab on the navigation menu on the left.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployments_tab_sidebar.png" alt="Deployments navigation tab">
    <figcaption>Deployments navigation tab</figcaption>
  </figure>
</p>

Once in the deployments page, click on `New deployment` if there are not existing deployments or on `Create new deployment` at the top-right corner to open the deployment creation form.

### Step 2: Basic deployment configuration

A simplified creation form will appear including the most common deployment fields among all the configuration possible. We provide default values for the rest of the fields, adjusted to the type of deployment you want to create.

In the simplified form, select the model framework used to train your model (i.e., _Tensorflow serving_ or _Python_). Then, select the model you want to deploy from the list of available models under `pick a model`.

After selecting the model, the rest of fields are filled automatically. We pick the last model version and model artifact version available in the Model Registry. Moreover, we infer the deployment name from the model name.

!!! notice "Deployment name validation rules"
    A valid deployment name can only contain characters a-z, A-Z and 0-9.

!!! info "Predictor script for Python models" 
    For Python models, you can select a custom [predictor script](#predictor) to load and run the trained model by clicking on `From project` or `Upload new file`, to choose an existing script in the project file system or upload a new script, respectively.

If you prefer, change the name of the deployment, model version or [artifact version](#model-artifact). Then, click on `Create new deployment` to create the deployment for your model.

<p align="center">
  <figure>
    <img style="float: left; width: 45%; margin-right: 12px" src="../../../../assets/images/guides/mlops/serving/deployment_simple_form_tf.png" alt="Simplified deployment form for Tensorflow">
    <img style="width: 45%;" src="../../../../assets/images/guides/mlops/serving/deployment_simple_form_py.png" alt="Simplified deployment form for Python">
    <figcaption>Simplified deployment creation forms for Tensorflow models (left) and Python models (right)</figcaption>
  </figure>
</p>

### Step 3 (Optional): Advanced configuration

Optionally, you can access and adjust other parameters of the deployment configuration by clicking on `Advanced options`.

<p align="center">
  <figure>
    <img  style="max-width: 85%; margin: 0 auto" src="../../../../assets/images/guides/mlops/serving/deployment_simple_form_adv_options.png" alt="Advance options">
    <figcaption>Advanced options. Go to advanced deployment creation form</figcaption>
  </figure>
</p>

You will be redirected to a full-page deployment creation form where you can see all the default configuration values we selected for your deployment and adjust them according to your use case. Apart from the aforementioned simplified configuration, in this form you can setup the following components:

!!! info "Deployment advanced options"
    1. [Predictor](#predictor)
    2. [Transformer](#transformer)
    3. [Inference logger](#inference-logger)
    4. [Inference batcher](#inference-batcher)
    5. [Resources](#resources)

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

```python
import hopsworks

connection = hopsworks.connection()

project = connection.get_project("my_project")

# get Hopsworks Model Registry handle
mr = project.get_model_registry()
```

### Step 2: Create deployment

Retrieve the trained model you want to deploy.

```python

my_model = mr.get_model("my_model", version=1)
```

#### Option A: Using the model object 

```python

my_deployment = my_model.deploy()
```

#### Option B: Using the Model Serving handle

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

[Model Serving](https://docs.hopsworks.ai/hopsworks-api/dev/generated/api/deployment/)

## Model Artifact

A model artifact is a package containing all of the necessary files for the deployment of a model. It includes the model file(s) and/or custom scripts for loading the model (predictor script) or transforming the model inputs at inference time (the transformer script).

When a new deployment is created, a model artifact is generated in two cases:

- the artifact version in the predictor is set to `CREATE` (see [Artifact Version](../predictor/#artifact_version))
- no model artifact with the same files has been created before.

## Predictor

Predictors are responsible for running the model server that loads the trained model, listens to inference requests and returns prediction results. To learn more about predictors, see the [Predictor Guide](predictor.md)

!!! note
    Currently, only one predictor is supported in a deployment. Support for multiple predictors (the inference graphs) is coming soon.

!!! info
    Model artifacts are assigned an incremental version number, being `0` the version reserved for model artifacts that do not contain predictor or transformer scripts (i.e., shared artifacts containing only the model files).

## Transformer

Transformers are used to apply transformations on the model inputs before sending them to the predictor for making predictions using the model. To learn more about transformers, see the [Transformer Guide](transformer.md).

!!! warning
    Transformers are only supported in KServe deployments.

## Inference logger

Inference loggers are deployment components that log inference requests into a Kafka topic for later analysis. To learn about the different logging modes, see the [Inference Logger Guide](inference-logger.md)

## Inference batcher

Inference batcher are deployment component that apply batching to the incoming inference requests for a better throughput-latency trade-off. To learn about the different configuration available for the inference batcher, see the [Inference Batcher Guide](inference-batcher.md).

## Resources

Resources include the number of replicas for the deployment as well as the resources (i.e., memory, CPU, GPU) to be allocated per replica. To learn about the different combinations available, see the [Resources Guide](resources.md).

## Conclusion

In this guide you learned how to create a deployment.