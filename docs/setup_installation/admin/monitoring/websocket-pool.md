# WebSocket Proxy Pool

## Introduction

Jupyter, terminals, and Streamlit apps are reached through Hopsworks by way of a WebSocket-aware proxy on the `hopsworks-instance` pods.
Each browser WebSocket that flows through that proxy is bridged to its upstream (the kernel, shell, or app pod) for the full lifetime of the connection, and every open bridge counts as one session against a per-pod cap.
When a pod reaches that cap, the next upgrade is rejected and the user-facing component (for example, JupyterLab) cannot reach its kernel.

This page describes how to monitor the proxy through Grafana, how to read the metrics that the platform exposes, and how to tune the cap from the Helm chart when the cluster has more concurrent notebook users than the defaults can serve.
The same counts drive the user-visible capacity badges described in [Session Capacity Warnings][session-capacity-warnings]; admin tuning here shifts the threshold those badges report against.

## Prerequisites

To access the Grafana dashboards described here, follow [Services Dashboards](./grafana.md) and confirm that you can open the `Hopsworks` dashboard under the `Hops` folder.
To change the session cap or the proxy buffers, you need to be able to edit the Helm values file used to install the chart and run `helm upgrade`.

## How the cap relates to concurrent users

Each open browser WebSocket the proxy is bridging counts as one in-flight session, and all three WebSocket-backed components — Jupyter kernels, terminals, and Streamlit apps — draw from the same per-pod budget.
The pod saturates at `maxSessionsPerApp` concurrent connections, which defaults to `800`.
Unlike the previous proxy, there is no two-threads-per-connection accounting: the cap is a direct count of open sessions, not a derived thread number.

There is no queue.
Once a pod is at the cap, the next upgrade is closed immediately with a WebSocket `1013 TRY_AGAIN_LATER` close, and the platform surfaces a "Maximum number of WebSocket connections reached" error rather than blocking the user on a connection that will never attach.
Rejecting cleanly protects the pod from connection-driven memory growth.

## Grafana panels

The WebSocket panels live at the bottom of the `Hopsworks` dashboard.
All read directly from metrics emitted by Payara on the `hopsworks-instance` pods.

- **WebSocket - rejection rate** plots `sum(rate(ws_connection_rejections_total[1m]))`.
  Any non-zero value means at least one user was turned away from a Jupyter, terminal, or Streamlit session in the last minute.
  This is the alertable signal for "the cap is too low."

- **WebSocket - duration (sliding-window percentiles)** plots p50, p95, and p99 of the duration of WebSocket connections after they close.
  Values come from an exponentially-decaying sample reservoir with a roughly five-minute half-life, so closed long-lived sessions decay out of the percentiles quickly rather than dominating them forever.

- **WebSocket - sessions** plots the current open-connection count per `hopsworks-instance` pod as solid lines, plus a single dashed red `Pool max (per instance)` line that shows the per-pod saturation point.
  A pod whose solid line meets the dashed line is rejecting new sessions.

- **WebSocket - pool CPU** plots `ws_pool_cpu_cores` per pod, in CPU cores.
  A value of `1.0` means the proxy's forwarding threads are consuming one full CPU core on that pod.
  Compare against the pod's CPU request or limit to judge whether to scale the pod's CPU allocation up.

- **WebSocket - pool allocation rate (GC pressure)** plots `ws_pool_alloc_bytes_per_second` per pod.
  This is heap allocation rate, not residency.
  A high rate means the forwarding threads are producing garbage, which translates to GC pressure on the JVM; it does not mean the proxy is holding that much memory.
  For "is the JVM heap getting full?" use the `Memory` panel above; for "is the pod approaching its k8s memory limit?" use the Kubernetes / Pods dashboard.

The per-pod panels carry the pod short identifier in the legend (the `<replicaset-hash>-<pod-hash>` tail; the `hopsworks-instance-` prefix is stripped because every series on this dashboard comes from an instance pod by construction).

## Prometheus metric reference

The metrics are emitted on the standard Payara MicroProfile Metrics endpoint (`/metrics`) under the `application` scope.
They are scraped by the in-cluster Prometheus server alongside the other Hopsworks service metrics, so federation and `remote_write` (see [Exporting Hopsworks metrics](./export-metrics.md)) cover them automatically.

The metric names are unchanged from the previous proxy implementation, so existing dashboards and alerts keep working; only the data source moved.

| Metric | Type | Meaning |
| --- | --- | --- |
| `ws_connection_in_flight_count` | gauge | Inbound WebSocket sessions currently open on this pod, one per browser leg the proxy is bridging. Tracked directly from the bridge's session open/close, not derived from a thread count. |
| `ws_connection_in_flight_max_age_seconds` | gauge | Age, in seconds, of the oldest currently open connection. |
| `ws_pool_max_connections` | gauge | Configured saturation point for one pod: the `maxSessionsPerApp` cap above which new upgrades are rejected with `1013 TRY_AGAIN_LATER`. |
| `ws_connection_rejections_total` | counter | Cumulative count of connections rejected because the cap was reached. |
| `ws_connection_duration_seconds` | summary | Count, sum, max, mean, and quantile values for the duration of closed connections, in seconds. |
| `ws_pool_cpu_cores` | gauge | CPU cores currently in use by the proxy's shared client transport threads. Computed from per-thread `ThreadMXBean.getThreadCpuTime` deltas divided by wall-clock dt; `1.0` means one full CPU core. `0` if the JVM does not support per-thread CPU accounting or on the first scrape after startup. |
| `ws_pool_alloc_bytes_per_second` | gauge | Heap allocation rate, in bytes per second, summed over the proxy's client transport threads. Computed from per-thread `getThreadAllocatedBytes` deltas divided by wall dt. This is GC pressure produced by the forwarding work, not the memory it currently holds; per-thread heap residency is not measurable through standard `ThreadMXBean` APIs. `0` on JVMs without `com.sun.management.ThreadMXBean`. |

All metrics carry the standard Kubernetes pod labels added by Prometheus during scraping (`pod_name`, `namespace`, `node`).
Dashboard queries that need to disambiguate per-pod series rewrite `pod_name` to a `pod_short` label that drops the `hopsworks-instance-` prefix.
Cluster-wide aggregates (`sum()`, `max()`) collapse pod labels and present one line per metric.

## Tuning the proxy

The proxy is configured at install time through `values.yaml`:

```yaml
hopsworks:
  payara:
    websocketProxy:
      maxSessionsPerApp: 800        # concurrent inbound WS sessions per pod
      incomingBufferBytes: 33554432 # max single received frame, in bytes (32 MiB)
      grizzlyWorkerPoolMaxSize: 200 # cap on the shared client transport workers
      sessionIdleTimeoutMs: 0       # 0 = no idle reaper (sessions are long-lived)
```

Raise `maxSessionsPerApp` to serve more concurrent notebook, terminal, and Streamlit users per pod.
The cap is a direct connection count, so the value is the number of concurrent connections you want each pod to serve — there is no longer a factor-of-two thread conversion.

The dominant resource cost of raising the cap is the memory held by the in-flight connections and the CPU spent forwarding their traffic, not thread overhead.
`grizzlyWorkerPoolMaxSize` bounds the shared client transport worker pool that carries the upstream-to-browser leg; leave it at the default unless the CPU panel shows the transport starved.
`incomingBufferBytes` is the ceiling a single received WebSocket frame (for example, a large Jupyter cell output) must fit under; it is grown on demand rather than pre-allocated, and should stay at or above Jupyter's iopub rate-limit budget.

After changing the cap, watch four panels on the `Hopsworks` dashboard:

- **Memory**: confirm the `Used heap` line stays comfortably below the dashed `Max heap (-Xmx)` line after each GC.
- **WebSocket - pool CPU**: confirm the proxy's CPU draw stays below the pod's CPU request or limit.
- **WebSocket - pool allocation rate (GC pressure)**: check whether the higher session count is producing enough allocation to drive GC time up.
- **GC**: confirm GC time stays within budget after the allocation rate moves.

For pod-vs-Kubernetes-limit context (working set vs request and limit) see the `Kubernetes / Pods` dashboard.

## Idle connections

By default `sessionIdleTimeoutMs` is `0`, which disables the proxy's idle reaper: proxied sessions are legitimately long-lived (an open notebook can sit idle for hours), so the proxy does not close them on inactivity.
Set a positive value (in milliseconds) only if you want the proxy itself to drop idle connections; JupyterLab and the terminal client both reconnect transparently after such a close, and the kernel, shell, or Streamlit process running in its own pod is unaffected by the disconnect.
