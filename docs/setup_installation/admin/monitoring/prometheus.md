# Prometheus namespace scope and memory

## Namespace scope

For a shared Kubernetes cluster, list the Hopsworks namespace and every project namespace in the Helm values used for installation and upgrades:

```yaml
prometheus:
  prometheus:
    kube-state-metrics:
      namespaces:
        - hopsworks
        - hopsworks-project-1
        - hopsworks-project-2
```

Use namespace names, not label selectors or regular expressions.
Update this list when adding project namespaces, otherwise their pod and service metrics will be missing from dashboards.
An empty list, `[]`, preserves cluster-wide collection.

The list limits Kubernetes pod and service discovery in `serverFiles.prometheus.yml.scrape_configs` and `extraScrapeConfigs`, and sets kube-state-metrics' `--namespaces` argument.
Existing job namespace selections are intersected with this list, including `own_namespace` selections.
A discovery entry with no matching namespaces is omitted; other discovery entries and static targets in the same job remain configured.
Jobs using Kubernetes node discovery retain samples for the listed namespaces and samples without a namespace label, preserving node metrics regardless of the job name.
Node discovery and node metrics remain cluster-wide.
The Kueue metrics job continues to discover only the configured Kueue namespace.
Static scrape targets and federation jobs retain their configured scope.
Jobs supplied through additional scrape files or an external server ConfigMap need their own namespace restrictions.

Keep this setting in your installation's values file so Helm upgrades preserve it.
The setting controls metrics collection; it does not replace Kubernetes RBAC or provide namespace access isolation.

## Memory sizing

The chart defaults are starting points, not capacity guarantees:

| Component | Memory request | Memory limit |
| --- | --- | --- |
| Prometheus server | `512Mi` | `3072Mi` |
| kube-state-metrics | `400Mi` | `600Mi` |

With a nonempty namespace list, size for the selected namespaces' pods, containers, exported labels and scrape frequency, plus cluster-wide node metrics.
With an empty list, size for workloads and label cardinality across the entire Kubernetes cluster, including workloads outside Hopsworks.
A fixed memory limit can be insufficient on a large shared cluster even when Hopsworks itself is small.

Measure Prometheus `process_resident_memory_bytes`, `prometheus_tsdb_head_series` and `prometheus_tsdb_head_chunks` through normal load and restart recovery.
Set requests to reserve the memory the workloads need and leave limit headroom for peak ingestion, queries and write-ahead log replay.
Measure kube-state-metrics separately, since its resource requirements depend on the objects and labels it exports.
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
Changing the namespace list reduces future collection but does not remove existing data or the write-ahead log.
An instance that is already restarting during log replay can still need temporary additional memory to complete recovery.
Check restart recovery before reducing that memory again.
