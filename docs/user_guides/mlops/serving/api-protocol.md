# How to Select the API protocol for a Deployment

## Introduction

Hopsworks supports both REST and gRPC as API protocols for sending inference requests to model deployments. While REST API protocol is supported in all types of model deployments, support for gRPC is only available for models served with [KServe](predictor.md#serving-tool).

!!! warning
    At the moment, the gRPC API protocol is only supported for **Python model deployments** (e.g., scikit-learn, xgboost). Support for Tensorflow model deployments is coming soon.

## GUI

### Step 1: Create a new deployment

If you have at least one model already trained and saved in the Model Registry, navigate to the deployments page by clicking on the `Deployments` tab on the navigation menu on the left.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployments_tab_sidebar.png" alt="Deployments navigation tab">
    <figcaption>Deployments navigation tab</figcaption>
  </figure>
</p>

Once in the deployments page, you can create a new deployment by either clicking on `New deployment` (if there are no existing deployments) or on `Create new deployment` it the top-right corner. Both options will open the deployment creation form.

### Step 2: Go to advanced options

A simplified creation form will appear including the most common deployment fields from all available configurations. Resource allocation is part of the advanced options of a deployment. To navigate to the advanced creation form, click on `Advanced options`.

<p align="center">
  <figure>
    <img  style="max-width: 85%; margin: 0 auto" src="../../../../assets/images/guides/mlops/serving/deployment_simple_form_adv_options.png" alt="Advance options">
    <figcaption>Advanced options. Go to advanced deployment creation form</figcaption>
  </figure>
</p>

### Step 3: Select the API protocol

Enabling gRPC as the API protocol for a model deployment requires KServe as the serving platform for the deployment. Make sure that KServe is enabled by activating the corresponding checkbox.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployment_adv_form_kserve.png" alt="KServe enabled in advanced deployment form">
    <figcaption>Enable KServe in the advanced deployment form</figcaption>
  </figure>
</p>

Then, you can select the API protocol to be enabled in your model deployment.

!!! info "Only one API protocol can be enabled for a model (they cannot support both gRPC and REST)"
    Currently, KServe model deployments are limited to one API protocol at a time. Therefore, only one of REST or gRPC API protocols can be enabled at the same time on the same model deployment. You can change the API protocol of existing deployments.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployment_grpc_select.png" alt="Select gRPC API protocol">
    <figcaption>Select gRPC API protocol</figcaption>
  </figure>
</p>

Once you are done with the changes, click on `Create new deployment` at the bottom of the page to create the deployment for your model.

## Code

### Step 1: Connect to Hopsworks

```python
import hopsworks

project = hopsworks.login()

# get Hopsworks Model Registry handle
mr = project.get_model_registry()

# get Hopsworks Model Serving handle
ms = project.get_model_serving()
```

### Step 2: Create a deployment with a specific API protocol

```python

my_model = mr.get_model("my_model", version=1)

my_predictor = ms.create_predictor(my_model,
                                   api_protocol="GRPC"  # defaults to "REST"
                                   )
my_predictor.deploy()

# or

my_deployment = ms.create_deployment(my_predictor)
my_deployment.save()
```

### API Reference

[API Protocol](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/model-serving/deployment_api/#api_protocol)
