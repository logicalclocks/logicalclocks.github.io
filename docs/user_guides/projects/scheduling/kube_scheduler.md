---
description: Documentation on how to configure Kubernetes scheduling options for Hopsworks workloads.
---
# Scheduler

## Introduction

Hopsworks allows users to configure [Affinity](https://kubernetes.io/docs/tasks/configure-pod-container/assign-pods-nodes-using-node-affinity/) and [Priority Classes](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/#priorityclass) when running workloads on Hopsworks, this includes jobs, jupyter notebooks and model deployments.

Hopsworks Admins can control which labels and priority classes can be used the cluster (see [Cluster configuration](#cluster-configuration) section) and by which project (see [Default Project configuration](#default-project-configuration) section) 

Within a project, data owners can set defaults for jobs and Jupyter notebooks running within that project (see: [Project defaults](#project-defaults) section). 

### Node Labels, Node Affinity and Node Anti-Affinity

Labels in Kubernetes are key-value pairs used to organize and select resources. Hopsworks relies on labels applied to nodes for pod-node affinity to determine where the pod can (or cannot) run.
Some uses cases where labels and affinity can be used include:

- Hardware constraints (GPU, SSD)
- Environment separation (prod/dev)
- Co-locating related pods
- Spreading pods for high availability

Hopsworks uses the node affinity `IN` operator for the Hopsworks Node Affinity and the `NOT IN` operator for the Hopsworks Node Anti Affinity.

For more information on Kubernetes Affinity, you can check the Kubernetes [Affinity documentation](https://kubernetes.io/docs/tasks/configure-pod-container/assign-pods-nodes-using-node-affinity/) page.

### Priority Classes

Priority classes in Kubernetes determine the scheduling and eviction priority of pods.

Pods with higher priority:

- Get scheduled first
- Can preempt (evict) lower priority pods
- Less likely to be evicted under resource pressure

Common uses:

- Protecting critical workloads
- Ensuring core services stay running
- Managing resource competition
- Guaranteeing QoS for important applications

For more information on Priority Classes, you can check the Kubernetes [Priority Classes documentation](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/#priorityclass) page.

## Cluster Configuration

Hopsworks admins can control the affinity labels and priority classes available on the Hopsworks cluster from the `Cluster Settings -> Scheduler` page:

![Cluster Configuration - Node Labels and Priority Classes](../../../assets/images/guides/project/scheduler/admin_cluster_scheduler.png)

Hopsworks Cluster can run within a shared Kubernets Cluster. The first configuration level is to limit the subset of labels and priority classes that can be used within the Hopsworks Cluster. This can be done from the `Available in Hopsworks` sub-section.

!!! note "Permissions"

    In order to be able to list all the Kubernetes Node Labels, Hopsworks requires the following cluster role:

    ```
        - apiGroups: [""]
        resources: ["nodes"]
        verbs: ["get", "list"]
    ```

    In order to be able to list all the Kubernetes Cluster Priority Classes, Hopsworsk requires this cluster role:

    ```
        - apiGroups: ["scheduling.k8s.io"]
        resources: ["priorityclasses"]
        verbs: ["get", "list"]
    ```

    If the roles above are configured properly (default behaviour), admins can only select values from the drop down menu. If the roles are missing, admins would be required to enter them as free text and should be careful about typos. Any typos here will be propagated in the other configuration and use levels leading to errors or missbehaviour when running computation.

## Project Configuration

Hopsworks admins can configure the labels and priority classes that can be used by default within a project. This will be a subset of the ones configured for Hopsworks.
In the figure above, in the sub-section `Available in Project` Hopsworks admins can configure the labels and priority classes available by default in any Hopsworks Project.

Hopsworks admins can also override the default project configuration on a per-project basis. That is, Hopsworks admins can make certain labels and priority classes available only to certain projects. This can be achieved from the `Cluster Settings -> Project -> <ProjectName> -> edit configuration` configuration page:

![Custom Project Configuration - Node Labels and Priority Classes](../../../assets/images/guides/project/scheduler/admin_project_scheduler.png)

## Project defaults

Within a project, different jobs, Jupyter notebooks and model deployments can run with different labels and/or priority classes. `Data Owners` in a project can specify the default values from the project settings:
The default Label will be used for the default Node Affinity for jobs, notebooks, and model deployments.

![ Project Default - Labels and Priority Classes](../../../assets/images/guides/project/scheduler/project_default.png)

## Configuration of Jobs, Notebooks, and Deployments

In the advanced configuration sections for job, notebook, and model deployments, users can set affinity, anti affinity and priority class. The Affinity and Anti Affinity can be selected from the list of allowed labels.

`Affinity` configures on which nodes this pod can run. If a node has any of the labels present in the Affinity option, the pod can be scheduler to run to run there.

`Anti Affinity` configures on which nodes this pod will not run on. If a node has any of the labels present in the Anti Affinity option, the pod will not be scheduler to run there.

`Priority Class` specifies with which priority a pod will run.

![ Job Configuration - Affinity and Priority Classes](../../../assets/images/guides/project/scheduler/job_configuration.png)
