---
description: Documentation on how to configure scheduling options for a model deployment
---

# How To Configure Scheduling For A Model Deployment

## Introduction

Scheduling configuration determines how and where your model deployment pods are placed in the Kubernetes cluster.
Hopsworks supports Kubernetes scheduler abstractions such as [node affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#node-affinity), [anti-affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#inter-pod-affinity-and-anti-affinity), and [priority classes](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/), as well as advanced scheduling with [Kueue queues](https://kueue.sigs.k8s.io/docs/concepts/local_queue/) and [topologies](https://kueue.sigs.k8s.io/docs/concepts/topology_aware_scheduling/).

!!! tip "Scheduling available for all workloads"
    In addition to model deployments, all scheduling options are also available for jobs, Jupyter notebooks, and Python deployments.

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
Scheduling is part of the advanced options of a deployment.
To navigate to the advanced creation form, click on `Advanced options`.

<p align="center">
  <figure>
    <img  style="max-width: 55%; margin: 0 auto" src="../../../../assets/images/guides/mlops/serving/deployment_simple_form_adv_options.png" alt="Advance options">
    <figcaption>Advanced options. Go to advanced deployment creation form</figcaption>
  </figure>
</p>

### Step 3: Configure scheduling

In the advanced creation form, go to the **Scheduler** section to set up scheduling options for your deployment. Here, you can specify [affinity, anti-affinity, and priority classes](#affinity-anti-affinity-and-priority-classes) to control how your deployment pods are scheduled within the cluster.

<p align="center">
  <figure>
    <img  style="margin: 0 auto" src="../../../../assets/images/guides/project/scheduler/job_configuration.png" alt="Affinity and Priority Classes">
    <figcaption>Configure affinity and priority classes for the model deployment</figcaption>
  </figure>
</p>

If Kueue is ==enabled==, you can also select a [queue and topology](#queues-and-topologies) for your deployment.

<p align="center">
  <figure>
    <img  style="margin: 0 auto" src="../../../../assets/images/guides/project/scheduler/job_queue.png" alt="Select a queue for the deployment">
    <figcaption>Select a queue for the model deployment</figcaption>
  </figure>
</p>

<p align="center">
  <figure>
    <img  style="margin: 0 auto" src="../../../../assets/images/guides/project/scheduler/job_topology_unit.png" alt="Select a topology unit for the deployment">
    <figcaption>Select a topology unit for the model deployment</figcaption>
  </figure>
</p>

Once you are done with the changes, click on `Create new deployment` at the bottom of the page to create the deployment for your model.

## Affinity, Anti-Affinity, and Priority Classes

You can configure [node affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#node-affinity), [anti-affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#inter-pod-affinity-and-anti-affinity), and [priority classes](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/) to control pod placement and scheduling priority for your deployment.

- **Affinity**: Constrains which nodes the deployment pods can run on based on node labels (e.g., GPU nodes, specific zones).
- **Anti-Affinity**: Prevents pods from running on nodes with specific labels.
- **Priority Class**: Determines the scheduling and eviction priority of pods. Higher priority pods are scheduled first and can preempt lower priority pods.

## Queues and Topologies

!!! warning "Kueue is required"
    This feature requires Kueue to be enabled in your cluster. If Kueue is not available, queue and topology options will not be accessible.

If the cluster has Kueue enabled, you can select a queue for your deployment. [Queues](https://kueue.sigs.k8s.io/docs/concepts/local_queue/) control resource allocation and scheduling priority across the cluster. Administrators define quotas on how many resources a queue can use, and queues can be grouped in cohorts to borrow resources from each other.

You can also select a [topology](https://kueue.sigs.k8s.io/docs/concepts/topology_aware_scheduling/) unit to control how deployment pods are co-located. For example, you can require all pods to run on the same host to minimize network latency.

## Learn more

For detailed documentation on scheduling abstractions and cluster-level configuration, see the following guides:

- [Scheduler](../../projects/scheduling/kube_scheduler.md) — Affinity, anti-affinity, priority classes, and project-level defaults
- [Kueue Details](../../projects/scheduling/kueue_details.md) — Queues, cohorts, topologies, and resource flavors
