# Prometheus namespace scope and memory

## Namespace scope

For a shared Kubernetes cluster, apply the chart package's `values.prometheus-scope.yaml` preset together with your installation values.
From an unpacked chart:

```bash
helm upgrade --install hopsworks ./hopsworks --namespace hopsworks \
  -f my-values.yaml -f ./hopsworks/values.prometheus-scope.yaml
```

The preset enables a namespace watcher and the scoped Prometheus ConfigMap.
It selects namespaces with the `hopsworks.ai/project` label by default and always includes the Hopsworks installation namespace.
Project creation, deletion and label changes update monitoring automatically; no namespace list or Helm upgrade is needed.
The watcher checks the selector every 30 seconds by default.
Kubernetes ConfigMap projection and configuration reloads add propagation time.

When multiple Hopsworks installations share a cluster, include a tenant label in the selector.
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

Enabling the preset changes the mounted server ConfigMap, rolling the Prometheus server on upgrade while preserving its data volume.
It also limits the pod labels kube-state-metrics exports to `compute-type` and `job-type`, the ones Hopsworks reads, which rolls kube-state-metrics.
If your own dashboards use other pod labels, set `prometheus.prometheus.kube-state-metrics.metricLabelsAllowlist` after the preset with every entry you need, because Helm replaces lists.
Later namespace changes reload the configuration without rolling the pod.
The watcher owns the generated ConfigMap so GitOps reconciliation does not overwrite its contents.
If the Kubernetes API is unavailable, it retains the last published configuration and retries.
Before the first successful refresh, the ConfigMap is absent and the Prometheus server waits for it instead of starting with cluster-wide collection.
An empty selector result still includes the installation namespace.

The namespace selection limits pod and service discovery in `serverFiles.prometheus.yml.scrape_configs` and templated `extraScrapeConfigs`.
Existing per-job namespace selections are intersected with the discovered namespaces, including `own_namespace` selections.
A discovery entry with no matching namespaces is omitted; other discovery entries and static targets remain configured.
Node-discovery jobs retain samples for the selected namespaces and samples without a namespace label, preserving node metrics.
Node discovery and node metrics remain cluster-wide.
kube-state-metrics keeps collecting the whole cluster, and Prometheus stores its series only for the selected namespaces.
Container resource requests and limits are kept for every namespace, together with node allocatable and capacity, so cluster utilisation counts the resources other workloads hold.
Series without a namespace, such as those of nodes, are kept.
The Kueue metrics job retains its configured Kueue namespace.
Platform dependencies that run outside the selected namespaces are discovered cluster-wide by label through `namespaceScope.dependencies`.
The default finds the NVIDIA GPU operator's DCGM exporter, labelled `app.kubernetes.io/component=nvidia-dcgm-exporter`, in any namespace, so GPU metrics remain available.
Each entry adds a Kubernetes service discovery configuration with label selectors to an existing scrape job; if you replace the scrape jobs, adjust or empty the list.
Static scrape targets and federation jobs retain their configured scope.
Jobs supplied through additional scrape files or an external server ConfigMap need their own namespace restrictions.
The namespace selector controls metrics collection; it does not replace Kubernetes RBAC or provide namespace access isolation.

The preset requires the Prometheus ConfigMap reloader and the default Prometheus config-file flags.
The Prometheus service account must have permission to watch the selected namespaces; the preset preserves its existing RBAC.

To opt out, omit the preset and reset the release values using your complete normal installation values:

```bash
helm upgrade hopsworks ./hopsworks --namespace hopsworks --reset-values \
  -f my-values.yaml
```

Keep all required installation overrides in `my-values.yaml` when resetting values.
This restores the upstream ConfigMap and the kube-state-metrics label allowlist, and removes the watcher.
Without the preset, existing installations keep their current collection behavior.

## Memory sizing

The chart defaults are starting points, not capacity guarantees:

| Component | Memory request | Memory limit |
| --- | --- | --- |
| Prometheus server | `512Mi` | `3072Mi` |
| kube-state-metrics | `400Mi` | `600Mi` |
| Namespace watcher, when enabled | `64Mi` | `256Mi` |

With automatic namespace scope, size for the selected namespaces' pods, containers, exported labels and scrape frequency, plus cluster-wide node metrics.
Without scoped Prometheus collection, size for workloads and label cardinality across the entire Kubernetes cluster, including workloads outside Hopsworks.
A fixed memory limit can be insufficient on a large shared cluster even when Hopsworks itself is small.

Measure Prometheus `process_resident_memory_bytes`, `prometheus_tsdb_head_series` and `prometheus_tsdb_head_chunks` through normal load and restart recovery.
Set requests to reserve the memory the workloads need and leave limit headroom for peak ingestion, queries and write-ahead log replay.
Measure kube-state-metrics separately, since its resource requirements depend on the objects and labels it exports.
It collects the whole cluster with or without the preset, so its memory grows with the cluster's pods; the preset's shorter pod label list reduces it.
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
