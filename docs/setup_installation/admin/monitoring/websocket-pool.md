# WebSocket Proxy Pool

## Introduction

Jupyter, terminal, RStudio, Streamlit, the Ray dashboard, and the Spark driver UI are reached through Hopsworks by way of a WebSocket-aware HTTP proxy.
Every WebSocket connection that flows through that proxy holds two threads in a single managed executor pool on Payara, named `concurrent/websocketsExecutorService`, for the full lifetime of the connection.
When the pool fills, new connections are rejected and the user-facing component (for example, JupyterLab) cannot reach its kernel.

This page describes how to monitor the pool through Grafana, how to read the metrics that the platform exposes, and how to tune the pool from the Helm chart when the cluster has more concurrent notebook users than the defaults can serve.
The same pool drives the user-visible capacity badges described in [Session Capacity Warnings][session-capacity-warnings]; admin tuning here shifts the threshold those badges report against.

## Prerequisites

To access the Grafana dashboards described here, follow [Services Dashboards](./grafana.md) and confirm that you can open the `Hopsworks` dashboard under the `Hops` folder.
To change pool sizing or Grizzly timeouts, you need to be able to edit the Helm values file used to install the chart and run `helm upgrade`.

## How the pool relates to concurrent users

Each WebSocket connection consumes two threads in `concurrent/websocketsExecutorService` (one per stream direction).
The pool therefore saturates at `maximumPoolSize / 2` concurrent connections.
At the default sizing — `corePoolSize: 100`, `maximumPoolSize: 200`, `taskQueueCapacity: 0` — that is 100 concurrent WebSocket connections.

The task queue is intentionally zero-length.
Threads in this pool are long-lived (often hours, in the case of an open notebook), so a queue would only let users keep clicking _Connect_ on a kernel that never actually attaches.
Once the pool is full, the platform surfaces a "Maximum number of WebSocket connections reached" error on the next attempted connection rather than blocking the user indefinitely.

## Grafana panels

The WebSocket panels live at the bottom of the `Hopsworks` dashboard.
All read directly from metrics emitted by Payara on the `hopsworks-instance` pods.

- **WebSocket - rejection rate** plots `sum(rate(ws_connection_rejections_total[1m]))`.
  Any non-zero value means at least one user was turned away from a Jupyter, terminal, or Streamlit session in the last minute.
  This is the alertable signal for "the pool is too small."

- **WebSocket - duration (sliding-window percentiles)** plots p50, p95, and p99 of the duration of WebSocket connections after they close.
  Values come from an exponentially-decaying sample reservoir with a roughly five-minute half-life, so closed long-lived sessions decay out of the percentiles quickly rather than dominating them forever.

- **WebSocket - sessions** plots the current open-connection count per `hopsworks-instance` pod as solid lines, plus a single dashed red `Pool max (per instance)` line that shows the per-pod saturation point.
  A pod whose solid line meets the dashed line is rejecting new sessions.

- **WebSocket - pool CPU** plots `ws_pool_cpu_cores` per pod, in CPU cores.
  A value of `1.0` means the pool is consuming one full CPU core on that pod.
  Compare against the pod's CPU request or limit to judge whether to scale the pod's CPU allocation up.

- **WebSocket - pool allocation rate (GC pressure)** plots `ws_pool_alloc_bytes_per_second` per pod.
  This is heap allocation rate, not residency.
  A high rate means the pool is producing garbage, which translates to GC pressure on the JVM; it does not mean the pool is holding that much memory.
  For "is the JVM heap getting full?" use the `Memory` panel above; for "is the pod approaching its k8s memory limit?" use the Kubernetes / Pods dashboard.

The per-pod panels carry the pod short identifier in the legend (the `<replicaset-hash>-<pod-hash>` tail; the `hopsworks-instance-` prefix is stripped because every series on this dashboard comes from an instance pod by construction).

## Prometheus metric reference

The metrics are emitted on the standard Payara MicroProfile Metrics endpoint (`/metrics`) under the `application` scope.
They are scraped by the in-cluster Prometheus server alongside the other Hopsworks service metrics, so federation and `remote_write` (see [Exporting Hopsworks metrics](./export-metrics.md)) cover them automatically.

| Metric | Type | Meaning |
| --- | --- | --- |
| `ws_connection_in_flight_count` | gauge | Currently open WebSocket connections. Derived from the executor's `getActiveCount` divided by two so it reflects orphan pump threads from rejected half-success connections, not only the in-process session map. |
| `ws_connection_in_flight_max_age_seconds` | gauge | Age, in seconds, of the oldest currently open connection. |
| `ws_pool_max_connections` | gauge | Configured saturation point for one pod: `maximumPoolSize / 2`. Reported as `-1` if Payara internals could not be introspected at startup. |
| `ws_connection_rejections_total` | counter | Cumulative count of connections rejected because the pool was full. |
| `ws_connection_duration_seconds` | summary | Count, sum, max, mean, and quantile values for the duration of closed connections, in seconds. |
| `ws_pool_cpu_cores` | gauge | CPU cores currently in use by the pool. Computed from per-thread `ThreadMXBean.getThreadCpuTime` deltas divided by wall-clock dt; `1.0` means one full CPU core. `0` if the JVM does not support per-thread CPU accounting or on the first scrape after startup. |
| `ws_pool_alloc_bytes_per_second` | gauge | Heap allocation rate, in bytes per second, summed over alive pool threads. Computed from per-thread `getThreadAllocatedBytes` deltas divided by wall dt. This is GC pressure produced by the pool, not the memory it currently holds; per-thread heap residency is not measurable through standard `ThreadMXBean` APIs. `0` on JVMs without `com.sun.management.ThreadMXBean`. |

All metrics carry the standard Kubernetes pod labels added by Prometheus during scraping (`pod_name`, `namespace`, `node`).
Dashboard queries that need to disambiguate per-pod series rewrite `pod_name` to a `pod_short` label that drops the `hopsworks-instance-` prefix.
Cluster-wide aggregates (`sum()`, `max()`) collapse pod labels and present one line per metric.

## Tuning the pool

The pool is configured at install time through `values.yaml`:

```yaml
hopsworks:
  payara:
    executorService:
      websockets:
        corePoolSize: 100      # threads kept alive
        maximumPoolSize: 200   # hard ceiling = 2x maxConcurrentConnections
        taskQueueCapacity: 0   # do not queue; reject when full
        threadPriority: 8      # above default so pumps are not starved
```

Bump `corePoolSize` and `maximumPoolSize` together.
`maximumPoolSize` must remain twice the number of concurrent WebSocket connections you want to serve, because of the two-threads-per-connection rule.
Leave `taskQueueCapacity` at `0`.
A non-zero queue with this workload causes users to wait on connections that will never become active threads; rejection is the safer behavior.

Each thread is otherwise idle (it blocks on stream I/O), so the dominant resource cost of raising these numbers is JVM thread overhead in `hopsworks-instance` pods.
A few hundred extra threads add a few tens of megabytes of stack memory at `-Xss512k`, which is small relative to the Payara JVM heap.
After changing the sizing, watch four panels on the `Hopsworks` dashboard:

- **Memory**: confirm the `Used heap` line stays comfortably below the dashed `Max heap (-Xmx)` line after each GC.
- **WebSocket - pool CPU**: confirm the pool's CPU draw stays below the pod's CPU request or limit.
- **WebSocket - pool allocation rate (GC pressure)**: check whether the higher session count is producing enough allocation to drive GC time up.
- **GC**: confirm GC time stays within budget after the allocation rate moves.

For pod-vs-Kubernetes-limit context (working set vs request and limit) see the `Kubernetes / Pods` dashboard.

## Grizzly timeouts

The chart leaves Payara / Grizzly `request-timeout-seconds` and `websockets-timeout-seconds` at their defaults.
The first governs the HTTP request lifecycle (the Upgrade handshake through the 101 response); once a WebSocket is established the framing layer takes over, where `websockets-timeout-seconds` is the idle timer.
A WebSocket session that sits idle past that default closes; JupyterLab and the terminal client both reconnect transparently, and the kernel / shell / Streamlit process running in its own pod is unaffected by the disconnect.

If your users need a longer idle window, raise `network-config.protocols.protocol.http-listener-2.http.websockets-timeout-seconds` via a post-boot `asadmin` override or a future chart value — that attribute (note the plural) is what governs the established-WebSocket idle clock on Payara 6.
