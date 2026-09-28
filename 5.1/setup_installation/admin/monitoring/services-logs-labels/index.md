# Service Log Labels

## Introduction

Filebeat attaches Kubernetes metadata to every service log document before Logstash forwards it to OpenSearch.
Only an explicit set of pod, namespace and node labels is kept.

The set is bounded because every distinct label key becomes a field in the shared `.services-*` index mapping.
OpenSearch rejects documents once an index exceeds `index.mapping.total_fields.limit`, which defaults to 1000 fields.
A cluster that attaches every pod and node label, including the label sets that cloud providers and node feature discovery add, reaches that limit and then stops indexing service logs.

In this guide you will learn which labels are kept by default, and how to append to or replace that set.

## Default pod labels

| Label | Purpose |
| --- | --- |
| `name` | Excludes Filebeat's own logs from collection. |
| `app` | Service identification, read by most pipelines. |
| `app.kubernetes.io/name` | Service identification for charts using the recommended Kubernetes labels. |
| `service` | Service name. |
| `component` | Component within a service. |
| `rondbService` | RonDB process type. |
| `user` | Owner of a job, notebook or serving instance. |
| `job-type` | Job type. |
| `job-id` | Job identifier. |
| `job-name` | Job name. |
| `execution` | Execution identifier of a job run. |
| `jupyter` | Marks a Jupyter pod. |
| `jupyter-id` | Jupyter instance identifier. |
| `jupyter-settings-id` | Jupyter settings identifier. |
| `kernel-id` | Jupyter kernel identifier. |
| `spark-role` | Driver or executor. |
| `spark-app-selector` | Spark application identifier. |
| `sparkoperator.k8s.io/launched-by-spark-operator` | Marks pods created by the Spark operator. |
| `serving.hops.works/id` | Deployment identifier. |
| `serving.hops.works/name` | Deployment name. |
| `serving.hops.works/tool` | Serving tool. |
| `serving.hops.works/model-name` | Model name. |
| `serving.hops.works/model-version` | Model version. |
| `serving.hops.works/model-server` | Model server. |
| `serving.hops.works/project-id` | Project that owns the deployment. |

## Default namespace labels

| Label | Purpose |
| --- | --- |
| `hopsworks.ai/project` | Marks a project namespace. |
| `hopsworks.ai/onlinefs-cluster` | Marks an online feature store namespace. |

Filebeat collects logs from the release namespace, from namespaces carrying either of these two labels, and from any namespace listed in `olk.filebeat.extraNamespaces`.

## Default node labels

| Label | Purpose |
| --- | --- |
| `kubernetes.io/hostname` | Node name, read by the services, Spark, Python and serving pipelines. |

## How labels appear in a log document

```json
{
  "kubernetes": {
    "labels": { "app": "namenode", "app_kubernetes_io/name": "hopsfs" },
    "namespace_labels": { "hopsworks_ai/project": "demo" },
    "node": { "labels": { "kubernetes_io/hostname": "worker-1" } }
  }
}
```

Dots in a label key are replaced by underscores.
In OpenSearch Dashboards, search for `kubernetes.labels.app_kubernetes_io/name`, not `kubernetes.labels.app.kubernetes.io/name`.

## Labels Hopsworks' log filtering reads

Four defaults are unioned into the effective set whatever the lists below say, because losing one breaks log collection rather than degrading a field:

| Label | Dimension | What breaks without it |
| --- | --- | --- |
| `name` | pod | Filebeat collects its own logs. It logs every OpenSearch rejection with the document embedded, so this feeds back on itself. |
| `hopsworks.ai/project` | namespace | Project namespaces are no longer collected. |
| `hopsworks.ai/onlinefs-cluster` | namespace | Online feature store namespaces are no longer collected. |
| `kubernetes.io/hostname` | node | The services, Spark, Python and serving pipelines lose the node field. |

`name` and `hopsworks.ai/onlinefs-cluster` are read by the chart's own Filebeat configuration rather than by a pipeline.
`hopsworks.ai/project` is read by both: the Filebeat namespace gate and the `discriminator.conf` pipeline, which derives the project field from it.
They cost eight fields of the 1000-field budget, not four: a dynamically mapped string label is indexed as `text` plus a `.keyword` sub-field, so every key counts twice.
The same doubling applies to any label you append, which halves the effective budget.

Every default is in this category: the audit of the shipped set found no key that is collected without something reading it.
They live in the `logFiltering*` values, so the set is visible and auditable:

```yaml
olk:
  filebeat:
    kubernetesMetadata:
      logFilteringPodLabels: [ ... ]
      logFilteringNamespaceLabels:
        - "hopsworks.ai/project"
        - "hopsworks.ai/onlinefs-cluster"
      logFilteringNodeLabels:
        - "kubernetes.io/hostname"
```

The effective set for a dimension is `logFiltering*` plus `extra*`, de-duplicated.
Removing a key from `logFiltering*` is possible, since Helm cannot make a value read-only, and breaks whatever reads it: the four above stop log collection, and the rest stop a Logstash routing or enrichment branch from matching.
A location that genuinely needs different metadata should set `addKubernetesMetadata: false` and supply its own processors instead.

A log location that genuinely needs different metadata should instead set `addKubernetesMetadata: false` and supply its own processors, as described below.

## Metadata collection per log location

Collection is switched on per entry of `olk.filebeat.logs_locations`:

```yaml
olk:
  filebeat:
    logs_locations:
      - name: containerd
        path: /var/log/containers
        mountPaths:
          - /var/log/containers
          - /var/log/pods
        logtype: log
        glob: "/*.log"
        addKubernetesMetadata: true
        processors: []
```

Helm replaces lists instead of merging them, so overriding `logs_locations` replaces the chart's entry in full, `addKubernetesMetadata` included.

!!! warning

    An override that omits `addKubernetesMetadata` and does not supply its own `add_kubernetes_metadata` processor collects no Kubernetes metadata at all.
    Log lines still reach OpenSearch, but every pipeline branch that routes on `kubernetes.*` stops matching, and nothing reports an error.

Set `addKubernetesMetadata: false` only for a location that supplies its own `add_kubernetes_metadata` in `processors`, which keeps two metadata processors from running on the same location.

## Append a label

Use the `extra` lists to keep the defaults and add to them:

```yaml
olk:
  filebeat:
    kubernetesMetadata:
      extraPodLabels:
        - "my.corp/team"
      extraNamespaceLabels:
        - "my.corp/cost-center"
      extraNodeLabels:
        - "topology.kubernetes.io/zone"
```

The extra lists are appended to the defaults and de-duplicated, so repeating a default is harmless.
Label keys named by `olk.logstash.extendServicesPipeline` are added automatically and do not need an entry here.

An appended label is stored on the log document and is searchable and aggregatable in OpenSearch Dashboards.
Routing and field extraction are done by the Logstash pipelines, which read a fixed set of keys, so an appended label does not change how a log line is parsed.

## Replace the filtering set

Override `logFiltering*` to replace the set that Hopsworks' filtering reads. Only do this if you know what stops working:

```yaml
olk:
  filebeat:
    kubernetesMetadata:
      logFilteringPodLabels:
        - "app"
        - "my.corp/team"
```

The `logFiltering*` lists hold the keys Hopsworks' own log filtering reads, so removing one silently breaks whatever reads it.

## Collect annotations

Annotations are not collected by default.
Add the keys you need:

```yaml
olk:
  filebeat:
    kubernetesMetadata:
      podAnnotations:
        - "my.corp/owner"
      namespaceAnnotations: []
      nodeAnnotations: []
```

!!! warning

    Annotations count towards the same 1000-field limit as labels.
    List individual keys rather than collecting all annotations.

## Deployment and cron job names

Two toggles control whether `kubernetes.deployment.name` and `kubernetes.cronjob.name` are attached:

```yaml
olk:
  filebeat:
    kubernetesMetadata:
      deployment: true
      cronjob: true
```

Set a toggle to `true` to add the field, `false` to drop it, or leave it unset to keep Filebeat's own default.

!!! note

    Set the toggle explicitly if you depend on the field.
    Elastic documents the default inconsistently: the `add_kubernetes_metadata` processor reference says the name is added unless disabled, while the autodiscover provider reference says it is not added unless enabled.
    To see what your cluster does, look for `kubernetes.deployment.name` on a service log document in Dashboards.

## Going Further

See [Services Logs](services-logs.md) for accessing the collected logs in OpenSearch Dashboards.
