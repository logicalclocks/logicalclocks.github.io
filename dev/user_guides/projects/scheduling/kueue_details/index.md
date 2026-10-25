# Kueue

## Introduction

Hopsworks provides the integration with Kueue to provide the additional scheduling abstractions.
Hopsworks currently acts only as a "reader" to the Kueue abstractions and currently does not manage the lifecycle of Kueue abstraction with the exception of the default localqueue for each namespace.
All the other abstractions are expected to be managed by the administrators of Hopsworks, directly on the Kubernetes cluster.

Kueue schedules Python and Ray jobs, Spark jobs, notebooks and model deployments.
The same queues are also used for Hopsworks internal jobs (zipping, git operations, python library installation).

### Spark jobs

Spark jobs run as Spark Operator `SparkApplication`s, which Kueue admits through its SparkApplication integration.
They go to the project's default queue unless the job selects another; a Spark job saved without a queue, as all were before Kueue managed Spark, gets the default queue when it starts.
Kueue reserves quota for the driver and a fixed number of executors, so on a cluster with Kueue a Spark job runs with static executors:

- `spark.dynamicAllocation.enabled` must be `false`. A Spark job with dynamic allocation is refused when it is saved and when it is started (error code 130082).
- `spark.executor.instances` sets the number of executors Kueue reserves quota for.
- New Spark jobs default to static executors, as many as the dynamic-allocation maximum.
- Spark jobs created before Kueue was enabled have dynamic allocation on, the earlier default. Turn it off and set the number of executors before running them.

Spark in Jupyter notebooks runs in client mode and is not managed by Kueue, so it keeps dynamic allocation.

### Resource flavors

When trying to define queues in Kueue, the first abstraction that needs to be defined is a [Resource Flavor](https://kueue.sigs.k8s.io/docs/concepts/resource_flavor/).
The resource flavor defines the resources that a queue will later manage.
Hopsworks helm chart installs and uses a default ResourceFlavor

```yaml
apiVersion: kueue.x-k8s.io/v1beta2
kind: ResourceFlavor
metadata:
  name: default-flavor
spec:
  nodeLabels:
    cloud.provider.com/region: europe
```

Node labels filter the available nodes to this resource flavor.
A flavor that names a topology with `topologyName` makes Kueue place pods by that [topology](#topologies).

### Cluster Queues

[Cluster Queues](https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/) are the actual queues for submitting jobs and model deployments to.
The default hopsworks queue looks like:

```yaml
apiVersion: kueue.x-k8s.io/v1beta2
kind: ClusterQueue
metadata:
  name: other
spec:
  cohortName: cluster
  namespaceSelector: {}
  preemption:
    borrowWithinCohort:
      policy: Never
    reclaimWithinCohort: Never
    withinClusterQueue: Never
  queueingStrategy: BestEffortFIFO
  resourceGroups:
  - coveredResources:
    - cpu
    - memory
    - pods
    - nvidia.com/gpu
    flavors:
    - name: default-flavor
      resources:
      - name: cpu
        nominalQuota: "0"
      - name: memory
        nominalQuota: "0"
      - name: pods
        nominalQuota: "0"
      - name: nvidia.com/gpu
        nominalQuota: "0"
```

The [preemption](https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/#preemption) and [nominal quotas](https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/#flavors-and-resources) are set to the minimal as this queue is designed to have lowest priority in getting resources allocated.
If a cluster is underutilized and there are resources available, it can still borrow up to the maximum resources present in the parent cohort, but by design this queue has no dedicated resources.
The presumption is that other, more important queues, defined by the cluster administrator will have higher preference in getting resources.

### Local Queues

[Local Queues](https://kueue.sigs.k8s.io/docs/concepts/local_queue/) are the mechanism to provide access to a queue (cluster queue) to a specific project in Hopsworks (Kubernetes namespace).

Every new project gets automatic access to the default Hopsworks queue.
An administrator can define the default queue for projects user jobs and system jobs.

![Default queue for user and system jobs](../../../assets/images/guides/project/scheduler/default_queue.png)

### Cohorts

[Cohorts](https://kueue.sigs.k8s.io/docs/concepts/cohort/) are groupings of cluster queues that have some meaning together and can share resources.
Hopsworks defines a default `cluster` cohort

```yaml
apiVersion: kueue.x-k8s.io/v1beta2
kind: Cohort
metadata:
  name: cluster
spec:
  resourceGroups:
  - coveredResources:
    - cpu
    - memory
    - pods
    - nvidia.com/gpu
    flavors:
    - name: default-flavor
      resources:
      - name: cpu
        nominalQuota: 100
      - name: memory
        nominalQuota: 200Gi
      - name: pods
        nominalQuota: 100
      - name: nvidia.com/gpu
        nominalQuota: 50
```

Cohorts can contain other cohorts, through `parentName`, and thus you can create a hierarchy of cohorts.
Cohorts can set [fair sharing weight](https://kueue.sigs.k8s.io/docs/concepts/admission_fair_sharing/) where using

```yaml
  fairSharing:
    weight
```

in the definition of a cohort, the user can control a priority towards borrowing resources from other cohorts.

### Topologies

[Topologies](https://kueue.sigs.k8s.io/docs/concepts/topology_aware_scheduling/) defines a way of grouping together pods belonging to the same job/deployment so that they are colocated within the same topology unit.
Hopsworks defines a default topology:

```yaml
apiVersion: kueue.x-k8s.io/v1beta2
kind: Topology
metadata:
  name: default
spec:
  levels:
  - nodeLabel: cloud.provider.com/region
  - nodeLabel: cloud.provider.com/zone
  - nodeLabel: kubernetes.io/hostname
```

A Cluster Queue uses a topology through the `topologyName` of its Resource Flavor; the default flavor names none.

When creating a new job, the user can select a topology unit for the job to run in and thus decide if all pods of a job should run on the same hostname, in the same zone or in the same region.
The user can select the topology for jobs, notebooks and deployments from `Advanced options`, in the `Scheduler` section of the full configuration page.

![Default queue for user and system jobs](../../../assets/images/guides/project/scheduler/job_topology_unit.png)
