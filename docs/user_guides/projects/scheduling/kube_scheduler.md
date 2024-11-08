# Scheduler

This page explains how we provide the user with access to Kubernetes properties when running Hopsworks computation on top of Kubernetes. Currently these capabilities include:

- [Affinity](https://kubernetes.io/docs/tasks/configure-pod-container/assign-pods-nodes-using-node-affinity/)
- [Priority Classes](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/#priorityclass)

These capabilities require some configuration from a Hopsworks Admin - as can be seen in the [Cluster configuration](#cluster-configuration), [Default Project configuration](#default-project-configuration) and [Custom Project configuration](#custom-project-configuration) section. Some further configuration on defaults can be done by Hopsworks data owners - as can be seen in the [Project defaults](#project-defaults) section. Finally, these capabilities can be used by all members of a project within:

- Jobs
- Jupyter Notebooks
- Model Deployments

## Node Labels, Node Affinity and Node Anti-Affinity

Labels in Kubernetes are key-value pairs used to organize and select resources. In this particular page we will show how labels applied to nodes can be used for pod-node affinity to determine where the pod can (or cannot) run.

Some base uses cases where labels and affinity can be used:

- Hardware constraints (GPU, SSD)
- Environment separation (prod/dev)
- Co-locating related pods
- Spreading pods for high availability

In Hopsworks we make use of the node affinity `IN` operator for the Hopsworks Node Affinity and the `NOT IN` operator for the Hopsworks Node Anti Affinity.

For more information on Kubernetes Affinity, you can check the Kubernetes [Affinity documentation](https://kubernetes.io/docs/tasks/configure-pod-container/assign-pods-nodes-using-node-affinity/) page.

## Priority Classes

PriorityClasses in Kubernetes determine the scheduling and eviction priority of pods.

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

The first step in configuring Affinity and Priority Classes is by a Hopsworks Admin through the page found under: `Cluster Settings -> Scheduler` as we can see in the image below.

![Cluster Configuration - Node Labels and Priority Classes](../../../assets/images/guides/project/scheduler/admin_cluster_scheduler.png)

When we want to configure the use of labels and priority classes there are a number of levels which require filtering: `kubernetes -> hopsworks cluster -> hopsworks project`

The Hopsworks Cluster tipycally runs inside a Kubernets Cluster and is not always the only inhabitant. So the first configuration level is to limit the subset of node labels and priority classes that can be used within the Hopsworks Cluster. This can be done from the `Available in Hopsworks` sub-section.

In order to be able to list all the Kubernetes Node Labels, Hopsworks requires this cluster role:

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

If the roles above are configured properly (by default configured with the Hopsworks installation) the Admin can only select values from the drop down menu. If the roles are missing, the Admin would require to enter them as free text and should be careful about typos. Any typos here will be propagated in the other configuration and use levels leading to errors or missbehaviour when running computation.

## Default Project Configuration

The second level of configuration we can do is project configuration. At this level, the Hopsworks Admin restricts the Node Labels and Priority Classes that can be used within a project. This will be a subset of the ones configured for Hopsworks.
In the figure above, in the sub-section `Available in Project` the Hopsworks Admin can configure the Node Labels and Priority Classes available by default in any Hopsworks Project.

## Custom Project Configuration

The Project level configuration, can be customised further and the Hopsworks Admin can configure per project Node Labels and Priority Classes selection in the menu option: `Cluster Settings -> Project -> <ProjectName> -> edit configuration`

![Custom Project Configuration - Node Labels and Priority Classes](../../../assets/images/guides/project/scheduler/admin_project_scheduler.png)

## Project defaults

Every Member of a project with the role `Data Owner` can then set the default values for the project. These defaults will be set in the Advanced configuration of Jobs, Notebooks, and Deployments, but they can of course be modified if so required.
The default Label will be used for the default Node Affinity for Jobs, Nodes, and Deployments.

![ Project Default - Labels and Priority Classes](../../../assets/images/guides/project/scheduler/project_default.png)

## Configuration of Jobs, Notebooks, and Deployments

In the Advance configuration of Job, Notebook, and Deployments, we can set Affinity, Anti Affinity, and Priority Class. The Affinity and Anti Affinity can be selected from the list of allowed labels.

`Affinity` configures on which nodes this pod can run. If a node has any of the labels present in the Affinity option, the pod can be scheduler to run to run there.

`Anti Affinity` configures on which nodes this pod will not run on. If a node has any of the labels present in the Anti Affinity option, the pod will not be scheduler to run there.

`Priority Class` specifies with which priority a pod will run.

![ Job Configuration - Affinity and Priority Classes](../../../assets/images/guides/project/scheduler/job_configuration.png)
