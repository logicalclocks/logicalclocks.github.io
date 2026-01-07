---
description: Documentation on how to troubleshoot a model deployment
---

# How To Troubleshoot A Model Deployment

## Introduction

In this guide, you will learn how to troubleshoot a deployment that is having issues to serve a trained model.
But before that, it is important to understand how [deployment states](deployment-state.md) are defined and the possible transitions between conditions.

When a deployment is starting, it follows an ordered sequence of [states](deployment-state.md#deployment-conditions) before becoming ready for serving predictions.
Similarly, it follows an ordered sequence of states when being stopped, although with fewer steps.

## GUI

### Step 1: Inspect deployment status

If you have at least one deployment already created, navigate to the deployments page by clicking on the `Deployments` tab on the navigation menu on the left.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployments_tab_sidebar_with_list.svg" alt="Deployments navigation tab">
    <figcaption>Deployments navigation tab</figcaption>
  </figure>
</p>

Once in the deployments page, find the deployment you want to inspect.
Next to the actions buttons, you can find an indicator showing the current status of the deployment.
For a more descriptive representation, this indicator changes its color based on the status.

To inspect the condition of the deployment, click on the name of the deployment to open the deployment overview page.

### Step 2: Inspect condition

At the top of page, you can find the same status indicator mentioned in the previous step.
Below it, a one-line message is shown with a more detailed description of the deployment status.
This message is built using the current status [condition](deployment-state.md#deployment-conditions) of the deployment.

Oftentimes, the status and the one-line description are enough to understand the current state of a deployment.
For instance, when the cluster lacks enough allocatable resources to meet the deployment requirements, a meaningful error message will be shown with the root cause.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployment_condition_fail_schedule.svg" alt="Deployment failed to schedule condition">
    <figcaption>Condition of a deployment that cannot be scheduled</figcaption>
  </figure>
</p>

However, when the deployment fails to start futher details might be needed depending on the source of failure.
For example, failures in the initialization or starting steps will show a less relevant message.
In those cases, you can explore the deployments logs in search of the cause of the problem.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployment_condition_fail_predictor.svg" alt="Deployment failed to start condition">
    <figcaption>Condition of a deployment that fails to start</figcaption>
  </figure>
</p>

### Step 3: Explore transient logs

Each deployment is composed of several components depending on its configuration and the model being served.
Transient logs refer to component-specific logs that are directly retrieved from the component itself.
Therefore, these logs can only be retrieved as long as the deployment components are reachable.

!!! info ""
    Transient logs are informative and fast to retrieve, facilitating the troubleshooting of deployment components at a glance

Transient logs are convenient when access to the most recent logs of a deployment is needed.

!!! info
    When a deployment is in idle state, there are no components running (i.e., scaled to zero) and, thus, no transient logs are available.

!!! note
    In the current version of Hopsworks, transient logs can only be accessed using the Hopsworks Machine Learning Python library.
    See [an example](#step-4-explore-transient-logs).

### Step 4: Explore historical logs

Transient logs are continuously collected and stored in OpenSearch, where they become historical logs accessible using the integrated OpenSearch Dashboards.
Therefore, historical logs contain the same information than transient logs.
However, there might be cases where transient logs could not be collected in time for a specific component and, thus, not included in the historical logs.

!!! info ""
    Historical logs are persisted transient logs that can be queried, filtered and sorted using OpenSearch Dashboards, facilitating a more sophisticated exploration of past records.

Historical logs are convenient when a deployment fails occasionally, either at inference time or without a clear reason.
In this case, narrowing the inspection of component-specific logs at a concrete point in time and searching for keywords can be helpful.

To access the OpenSearch Dashboards, click on the `See logs` button at the top of the deployment overview page.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployment_condition_see_logs.svg" alt="See logs button">
    <figcaption>Access to historical logs of a deployment</figcaption>
  </figure>
</p>

!!! note
    In case you are not familiar with the interface, you may find the [official documentation](https://opensearch.org/docs/latest/dashboards/index/) useful.

Once in the OpenSearch Dashboards, you can search for keywords, apply multiple filters and sort the records by timestamp.

??? info "Show available filters"

    | Filter         | Description                                                                                              |
    | -------------- | -------------------------------------------------------------------------------------------------------- |
    | component      | Name of the deployment component (i.e., predictor or transformer)                                        |
    | container_name | Name of the container within a component (i.e., kserve-container, storage-initializer, inference-logger) |
    | serving_name   | Name of the deployment                                                                                   |
    | model_name     | Name of the model being served                                                                           |
    | model_version  | Version of the model being served                                                                        |
    | timestamp      | Timestamp when the record was reported                                                                   |

## Code

### Step 1: Connect to Hopsworks

=== "Python"

  ```python
  import hopsworks

  project = hopsworks.login()

  # get Hopsworks Model Serving handle
  ms = project.get_model_serving()
  ```

### Step 2: Retrieve an existing deployment

=== "Python"

  ```python
  deployment = ms.get_deployment("mydeployment")
  ```

### Step 3: Get current deployment's predictor state

=== "Python"

  ```python
  state = deployment.get_state()

  state.describe()
  ```

### Step 4: Explore transient logs

=== "Python"

  ```python
  deployment.get_logs(component="predictor|transformer", tail=10)
  ```

### API Reference

[`Deployment`][hsml.deployment.Deployment]

[`PredictorState`][hsml.predictor_state.PredictorState]
