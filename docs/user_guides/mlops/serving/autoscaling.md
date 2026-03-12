# How To Configure Scaling For A Deployment

## Introduction

This guide explains how to set up **autoscaling** for model deployments using either the [web UI](#web-ui) or the [Python API](#code).

Deployments use [Knative Pod Autoscaler (KPA)](https://knative.dev/docs/serving/autoscaling/) to automatically scale the number of replicas based on traffic.
Autoscaling enables the deployment to use resources more efficiently, by growing and shrinking the allocated resources according to its actual, real-time usage.

See [Scale metrics](#scale-metrics) and [Scaling parameters](#scaling-parameters) for details on the available scaling options.

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
Autoscaling is part of the advanced options of a deployment.
To navigate to the advanced creation form, click on `Advanced options`.

<p align="center">
  <figure>
    <img  style="max-width: 55%; margin: 0 auto" src="../../../../assets/images/guides/mlops/serving/deployment_simple_form_adv_options.png" alt="Advance options">
    <figcaption>Advanced options. Go to advanced deployment creation form</figcaption>
  </figure>
</p>

### Step 3: Configure autoscaling

In the `Autoscaling` section of the advanced form, you can configure the scaling parameters for the predictor and/or the transformer (if available).
You can set the scale metric, target value, minimum and maximum instances, as well as the panic and stable window parameters.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployment_adv_form_scaling.png" alt="Autoscaling configuration for the predictor and transformer components">
    <figcaption>Autoscaling configuration for the predictor and transformer</figcaption>
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

### Step 2: Define the predictor scaling configuration

You can use the [`PredictorScalingConfig`][hsml.scaling_config.PredictorScalingConfig] class to configure the scaling options according to your preferences. Default values for scaling metrics and parameters are listed in the [Scale metrics](#scale-metrics) and [Scaling parameters](#scaling-parameters) sections above.

=== "Python"

  ```python
  from hsml.scaling_config import PredictorScalingConfig

  predictor_scaling = PredictorScalingConfig(
      min_instances=1, max_instances=5, scale_metric="RPS", target=100
  )
  ```

### Step 3 (Optional): Define the transformer scaling configuration

If a transformer script is also provided, you can use the [`TransformerScalingConfig`][hsml.scaling_config.TransformerScalingConfig] class to configure the scaling options according to your preferences. Default values for scaling metrics and parameters are listed in the [Scale metrics](#scale-metrics) and [Scaling parameters](#scaling-parameters) sections above.

=== "Python"

  ```python
  from hsml.scaling_config import TransformerScalingConfig

  transformer_scaling = TransformerScalingConfig(
      min_instances=1, max_instances=3, scale_metric="CONCURRENCY", target=50
  )
  ```

### Step 4: Create a deployment with the scaling configuration

=== "Python"

  ```python
  my_model = mr.get_model("my_model", version=1)

  # optional
  my_transformer = ms.create_transformer(
      script_file="Resources/my_transformer.py",
      scaling_configuration=transformer_scaling
  )

  my_deployment = my_model.deploy(
    scaling_configuration=predictor_scaling,
    # optional:
    transformer=my_transformer
  )
  ```

### API Reference

[`PredictorScalingConfig`][hsml.scaling_config.PredictorScalingConfig]

[`TransformerScalingConfig`][hsml.scaling_config.TransformerScalingConfig]

## Scale metrics

The autoscaler supports two metrics to determine when to scale. See [Knative autoscaling metrics](https://knative.dev/docs/serving/autoscaling/autoscaling-metrics/) for more details.

| Scale Metric | Default Target | Description                     |
| ------------ | -------------- | ------------------------------- |
| RPS          | 200            | Requests per second per replica |
| CONCURRENCY  | 100            | Concurrent requests per replica |

## Scaling parameters

The following parameters can be used to fine-tune the autoscaling behavior. See [scale bounds](https://knative.dev/docs/serving/autoscaling/scale-bounds/), [autoscaling concepts](https://knative.dev/docs/serving/autoscaling/autoscaling-concepts/) and [scale-to-zero](https://knative.dev/docs/serving/autoscaling/scale-to-zero/) in the Knative documentation for more details.

| Parameter                     | Default | Range  | Description                                 |
| ----------------------------- | ------- | ------ | ------------------------------------------- |
| `minInstances`                | —       | ≥ 0    | Minimum replicas (0 enables scale-to-zero)  |
| `maxInstances`                | —       | ≥ 1    | Maximum replicas (cannot be less than min)  |
| `panicWindowPercentage`       | 10.0    | 1–100  | Panic window as percentage of stable window |
| `stableWindowSeconds`         | 60      | 6–3600 | Stable window duration in seconds           |
| `panicThresholdPercentage`    | 200.0   | > 0    | Traffic threshold to trigger panic mode     |
| `scaleToZeroRetentionSeconds` | 0       | ≥ 0    | Time to retain pods before scaling to zero  |

!!! note "Cluster-level constraints"
    ==Administrators== can set cluster-wide limits on the maximum and minimum number of instances. When the minimum is set to 0, scale-to-zero is enforced for all deployments.
