# Prometheus namespace scope and memory

## Namespace scope { #prometheus-namespace-scope }

Prometheus collects metrics only from the Hopsworks installation namespace, the project namespaces that `prometheus.namespaceScope.selector` selects, and the platform namespaces.
A platform namespace carries none of the labels the selector reads, and holds a Service annotated with `prometheus.io/scrape: "true"` or `prometheus.io/scrape_slow: "true"`; the NVIDIA GPU operator's DCGM exporter, for example, keeps reporting GPU metrics this way.
A helper container in the Prometheus pod evaluates the selector, `hopsworks.ai/project` by default, finds the platform namespaces, and writes the Prometheus configuration for these namespaces.
Project creation, deletion and label changes update monitoring automatically; no namespace list or Helm upgrade is needed.
The helper checks the namespaces and Services every 30 seconds by default, and the configuration reload adds a few seconds.

When multiple Hopsworks installations share a cluster, include a tenant label in the selector, and label each installation's namespace with its tenant, `kubectl label namespace <namespace> hopsworks.ai/tenant=tenant-a`.
Otherwise every installation's namespace is a platform namespace for the others, and each Prometheus collects the other installations.
For example, add the following to `my-values.yaml`:

```yaml
prometheus:
  namespaceScope:
    selector: hopsworks.ai/project,hopsworks.ai/tenant=tenant-a
hopsworks:
  variables:
    project_namespace_labels: hopsworks.ai/tenant=tenant-a
```

Hopsworks adds `project_namespace_labels` when it creates project namespaces.
Existing and externally provisioned project namespaces must also carry the selector's labels.
For externally provisioned namespaces, a tenant selector such as `hopsworks.ai/tenant=tenant-a` can be used on its own when that label identifies exactly the intended project namespaces.
Testing only for the presence of `hopsworks.ai/project` includes labelled projects from every Hopsworks installation in the cluster.
A project namespace the selector misses loses its metrics, including the model deployment metrics that autoscaling reads.

Namespace changes reload the configuration without restarting Prometheus.
If the Kubernetes API is unavailable, the helper keeps the last configuration and retries.
When the pod starts, Prometheus waits for the helper's first configuration instead of starting with cluster-wide collection, so a pod that starts while the Kubernetes API is unavailable waits for the API.
An empty selector result still includes the installation namespace.

The namespace selection limits pod and service discovery in `serverFiles.prometheus.yml.scrape_configs` and templated `extraScrapeConfigs`.
Existing per-job namespace selections are intersected with the discovered namespaces, including `own_namespace` selections.
A discovery entry with no matching namespaces is omitted; other discovery entries and static targets remain configured.
Node-discovery jobs retain samples for the selected namespaces and samples without a namespace label, preserving node metrics.
Node discovery and node metrics remain cluster-wide.
kube-state-metrics keeps collecting the whole cluster, and Prometheus stores its series only for the selected namespaces.
Container resource requests and limits are kept for every namespace, together with node allocatable and capacity, so cluster utilisation counts the resources other workloads hold.
Series without a namespace, such as those of nodes, are kept.
The Kueue metrics job keeps discovering in its configured Kueue namespace, and its series are scoped like those of kube-state-metrics.
When Kueue is enabled (`global._hopsworks.kueue.enabled`), the kube-state-metrics and container series of its namespace are kept, so the alerts on pods and workloads keep covering Kueue, which Hopsworks jobs depend on.
Platform dependencies that no annotated Service announces are discovered cluster-wide by label through `namespaceScope.dependencies`.
The default finds OpenCost, whose pods are labelled `app.kubernetes.io/name=opencost`, in any namespace, so the cost metrics the admin Costs page reads back remain available.
Each entry gets a scrape job of its own, a copy of the scrape job it names that discovers only the entry's label selection outside the selected namespaces; if you replace the scrape jobs, adjust or empty the list.
The copy does not add the target's namespace to its series, so a dependency's series without a namespace of their own, such as OpenCost's node costs, are kept, while its series that name a namespace are filtered like any other.
Static scrape targets and federation jobs retain their configured scope.
Jobs supplied through additional scrape files need their own namespace restrictions.
Only node metrics and the kube-state-metrics and Kueue series are filtered by the namespace they describe; an exporter that watches the whole cluster, such as KEDA, cert-manager or Knative, reports on every namespace it serves.
Cluster-wide views therefore cover the selected namespaces only: the alerts on pods and workloads, the totals of the Kubernetes overview dashboard, and the costs OpenCost attributes to namespaces outside the selection.
The namespace selector controls metrics collection; it does not replace Kubernetes RBAC or provide namespace access isolation.

The helper generates the Prometheus configuration from the chart's values, so the chart requires the Prometheus ConfigMap reloader and the default Prometheus config-file flags, and refuses `server.configFromSecret` and `server.configMapOverrideName`.
Rendering also fails when the selector, or a dependency's label selector, is not a valid Kubernetes label selector, since the Kubernetes API would reject it on every refresh.
The chart grants the Prometheus service account permission to list namespaces and Services.
The helper is wired through the Prometheus chart's `server.extraInitContainers`, `server.extraVolumes`, `server.extraVolumeMounts`, `configmapReload.prometheus.extraVolumeMounts` and `configmapReload.prometheus.extraVolumeDirs`.
Helm replaces lists instead of merging them, so values that set one of these lists must restate the chart's entries; rendering fails otherwise.

## Memory sizing

The chart defaults are starting points, not capacity guarantees:

| Component | Memory request | Memory limit |
| --- | --- | --- |
| Prometheus server | `512Mi` | `3072Mi` |
| kube-state-metrics | `400Mi` | `600Mi` |
| Namespace scope helper, in the Prometheus pod | `64Mi` | `256Mi` |

Size Prometheus for the selected namespaces' pods, containers, exported labels and scrape frequency, plus cluster-wide node metrics and container resource requests and limits.
The scope reduces Prometheus memory but does not bound it: Prometheus still reads the whole cluster's kube-state-metrics and kubelet output on every scrape and keeps a small cache entry for each series it drops, so its memory still grows with the cluster, only more slowly.
A fixed memory limit can be insufficient on a large shared cluster even when Hopsworks itself is small.

Measure Prometheus `process_resident_memory_bytes`, `prometheus_tsdb_head_series` and `prometheus_tsdb_head_chunks` through normal load and restart recovery.
Set requests to reserve the memory the workloads need and leave limit headroom for peak ingestion, queries and write-ahead log replay.
Measure kube-state-metrics separately, since its resource requirements depend on the objects and labels it exports.
It collects the whole cluster, so its memory grows with the cluster's pods.
Adjust the defaults through Helm values:

```yaml
prometheus:
  prometheus:
    server:
      resources:
        requests:
          memory: 2Gi
        limits:
          memory: 4Gi
    kube-state-metrics:
      resources:
        requests:
          memory: 400Mi
        limits:
          memory: 600Mi
```

These example overrides illustrate the configuration paths; choose values from measurements of your installation.
Restricting the namespace selector reduces future collection but does not remove existing data or the write-ahead log.
An instance that is already restarting during log replay can still need temporary additional memory to complete recovery.
Check restart recovery before reducing that memory again.
