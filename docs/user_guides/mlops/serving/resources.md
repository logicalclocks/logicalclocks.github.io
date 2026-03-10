---
description: Documentation on how to allocate resources to a model deployment
---

# How To Allocate Resources To A Model Deployment

## Introduction

Resource allocation can be configured ==per component== (predictor and transformer) in a deployment, allowing you to specify how many CPUs, GPUs, and memory are allocated. For each component, you can set minimum (requests) and maximum (limits) resources, as well as the number of instances.

??? info "Resource defaults"

    | Field              | Default Request | Default Limit  | Validation                                         |
    | ------------------ | --------------- | -------------- | -------------------------------------------------- |
    | CPU (cores)        | 0.2             | -1 (unlimited) | Request cannot exceed limit (unless -1, unlimited) |
    | Memory (MB)        | 32              | -1 (unlimited) | Request cannot exceed limit (unless -1, unlimited) |
    | GPUs               | 0               | 0              | Request must equal limit                           |
    | Shared Memory (MB) | 128             | —              | —                                                  |

!!! tip "Automatic downscale of inactive instances"
    Setting the number of instances to **0** for a component (predictor or transformer) enables **scale-to-zero**. This means that all instances of the component will automatically scale down to zero after a default period of inactivity of 30 seconds.

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
Resource allocation is part of the advanced options of a deployment.
To navigate to the advanced creation form, click on `Advanced options`.

<p align="center">
  <figure>
    <img  style="max-width: 55%; margin: 0 auto" src="../../../../assets/images/guides/mlops/serving/deployment_simple_form_adv_options.png" alt="Advance options">
    <figcaption>Advanced options. Go to advanced deployment creation form</figcaption>
  </figure>
</p>

### Step 3: Configure resources

In the `Resource allocation` section of the form, you can optionally set the resources to be allocated to the predictor and/or the transformer (if available).
Moreover, you can choose the minimum number of replicas for each of these components.

!!! note "Scale-to-zero capabilities"
    Set the number of instances to **0** to enable scale-to-zero on the component.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployment_adv_form_res.png" alt="Resource allocation for the predictor and transformer components">
    <figcaption>Resource allocation for the predictor and transformer</figcaption>
  </figure>
</p>

Once you are done with the changes, click on `Create new deployment` at the bottom of the page to create the deployment for your model.

## Code

### Step 1: Connect to Hopsworks

=== "Python"

  ```python
  import hopsworks

  project = hopsworks.login()

  # get Hopsworks Model Registry handle
  mr = project.get_model_registry()

  # get Hopsworks Model Serving handle
  ms = project.get_model_serving()
  ```

### Step 2: Define the predictor resource configuration

=== "Python"

  ```python
  from hsml.resources import PredictorResources, Resources

  minimum_res = Resources(cores=1, memory=128, gpus=1)
  maximum_res = Resources(cores=2, memory=256, gpus=1)

  predictor_res = PredictorResources(
      num_instances=1, requests=minimum_res, limits=maximum_res
  )
  ```

### Step 3 (Optional): Define the transformer resource configuration

=== "Python"

  ```python
  from hsml.resources import TransformerResources

  minimum_res = Resources(cores=1, memory=128, gpus=1)
  maximum_res = Resources(cores=2, memory=256, gpus=1)

  transformer_res = TransformerResources(
      num_instances=2, requests=minimum_res, limits=maximum_res
  )

  ```

### Step 4: Create a deployment with the resource configuration

=== "Python"

  ```python
  my_model = mr.get_model("my_model", version=1)

  my_predictor = ms.create_predictor(
      my_model,
      resources=predictor_res,
      # transformer=Transformer(script_file,
      #                         resources=transformer_res)
  )
  my_predictor.deploy()

  # or

  my_deployment = ms.create_deployment(my_predictor)
  my_deployment.save()

  ```

### API Reference

[`Resources`][hsml.resources.Resources]

## Autoscaling

Deployments can be configured to automatically scale the number of replicas based on traffic.
To learn about the different autoscaling parameters, see the [Autoscaling Guide](autoscaling.md).
