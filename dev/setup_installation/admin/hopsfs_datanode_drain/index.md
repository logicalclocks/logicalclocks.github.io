# HopsFS DataNode drain { #hopsfs-datanode-drain }

## Introduction

With asynchronous cloud upload, a HopsFS DataNode finalizes a block on its local volume and uploads it to object storage in the background.
A DataNode that stops before its upload queue is empty leaves the blocks it has not uploaded yet on its local volume only.
Draining a DataNode suspends it and waits until its queue is empty, so every finalized block is in object storage before the DataNode stops.

The values on this page belong to the `hopsfs` subchart: set them under `hopsfs:` in the values of the Hopsworks chart.

When `objectStorage.asyncUpload.enabled` is `true` and `datanode.gracefulDrain.enabled` is `true` (its default), every DataNode pod gets a `preStop` hook that runs `hdfs dfsadmin -drainAndSuspendDatanode`, and a `terminationGracePeriodSeconds` sized for the worst-case upload backlog.
The hook covers routine pod deletions with no operator action: rolling restarts, pods recreated by `helm upgrade`, `kubectl drain`, and any eviction that respects the PodDisruptionBudget.

Asynchronous upload is off by default (`objectStorage.asyncUpload.enabled: false`).
Then the chart installs no `preStop` hook and keeps the default grace period of 30 seconds, because every finalized block is already in object storage when it is finalized.

## Before you enable asynchronous upload

The `preStop` hook is bounded by `terminationGracePeriodSeconds`, which is sized from `queueCapacity * blockSizeMiB / uploadThroughputMiBps`, as described in [Sizing the drain budget][hopsfs-drain-sizing].
For typical workloads that budget exceeds the backlog and the drain completes before the grace period ends.
If the backlog exceeds the budget, the kubelet stops the DataNode in the middle of the drain, and the blocks it has not uploaded stay on its volume only, as described in [Reading the outcome of a drain][hopsfs-drain-outcome].
Size the budget for your workload's worst case.
The most common adjustment is raising `datanode.gracefulDrain.uploadThroughputMiBps` when the actual upload throughput exceeds its conservative default of 35 MiB/s.

Operators should know how to run `hdfs dfsadmin -drainAndSuspendDatanode` against a DataNode pod even when the hook does the work day to day: it is how you check a drain before you delete a pod, and how you diagnose a slow or stuck drain.
If your environment does not let operators run it at all, for example where `kubectl exec` into DataNode pods is forbidden and no Hadoop client host exists outside the cluster, the hook still handles routine deletions.
You then cannot diagnose a stuck drain or recover from one, so if the sized budget turns out too small and you cannot change it quickly, keep asynchronous upload off.
Without it there is no upload backlog, and stopping a DataNode directly is safe in any environment.

## Draining a DataNode by hand { #hopsfs-drain-manual }

Drain by hand when you want explicit control: to drain before deleting a pod and check the result while the pod still exists, to run the drain from another pod so you can keep watching after the DataNode exits, or to debug a slow or stuck drain.
The manual command and the hook call the same RPC and produce the same status line, JMX state and termination behaviour; only the hook ignores the command's exit code, as described below.

1. Run the drain from a DataNode pod, or from any pod with `hdfs` on its path:

    ```bash
    kubectl exec -n hopsworks -it datanode-0 -- /srv/hops/hadoop/bin/hdfs \
      dfsadmin -drainAndSuspendDatanode <pod-fqdn>:50020 -timeout <seconds>
    ```

    Replace `<pod-fqdn>` with the headless DNS name of the DataNode to drain, for example `datanode-1.datanode-headless.hopsworks.svc.cluster.local`, and `<seconds>` with the drain budget, usually the value the chart calculates for `terminationGracePeriodSeconds`.

2. Wait for the final status line, which starts with `DRAINED`.
    While the drain runs, the line starts with `DRAINING`.
    The exit code is `0` for a completed drain, `1` for a timeout and `2` when the DataNode cannot be reached.

3. Delete the pod once it reports `DRAINED`:

    ```bash
    kubectl delete pod -n hopsworks datanode-1
    ```

    The `preStop` hook then runs against a DataNode that is already suspended and returns at once.

## How the preStop hook works

On every voluntary pod termination, including a `kubectl delete pod` after a manual drain, the kubelet runs the hook before it sends `SIGTERM`.
The hook:

- Runs `hdfs dfsadmin -drainAndSuspendDatanode localhost:50020 -timeout <seconds>`, where `<seconds>` is `datanode.gracefulDrain.timeoutSecs`, or the calculated budget when that is not set.
- Writes the full output of the command to `/tmp/drain-status.txt`, which you can read with `kubectl exec` while the pod is terminating.
- Writes one line ending in `drain-exit=<code>` to `/dev/termination-log`, the container's termination message.
- Always exits 0, so the kubelet sends `SIGTERM` after a timed-out or failed drain too.
  A block counts as safe only once it is in object storage, which a `DRAINED` status confirms for every finalized block; the exit of the DataNode process says nothing about it.

## Reading the outcome of a drain { #hopsfs-drain-outcome }

A deleted DataNode pod takes its termination message with it, and the pod that replaces it starts without one.
To keep the outcome of a drain, drain the DataNode by hand before you delete the pod, as described in [Draining a DataNode by hand][hopsfs-drain-manual], and read the command's own output.
While the hook runs, follow its output in the terminating pod:

```bash
kubectl exec -n hopsworks datanode-1 -- tail -f /tmp/drain-status.txt
```

| Final status line and exit code | Meaning |
| ------------------------------- | ------- |
| `DRAINED`, exit code `0` | The drain completed: every finalized block reached object storage. |
| `DRAINING`, exit code `1` | The drain timed out; some finalized blocks may not be in object storage yet. |
| no status line, exit code `2` | The command could not reach the DataNode's IPC port, usually because the DataNode was already shutting down. |

The blocks a timed-out drain did not upload remain on the DataNode's persistent volume.
A DataNode that starts again on that volume uploads them.
They are lost if the volume is lost first, for example with its node when the storage is local to the node, or when the volume is deleted before a DataNode starts on it again.

## Sizing the drain budget { #hopsfs-drain-sizing }

The default `terminationGracePeriodSeconds` is `queueCapacity * blockSizeMiB / uploadThroughputMiBps`.
With the defaults (`objectStorage.datanode.asyncUpload.queueCapacity: 1000`, `namenode.blockSizeMiB: 128`, `datanode.gracefulDrain.uploadThroughputMiBps: 35`) that is `ceil(1000 * 128 / 35) = 3658` seconds, about 61 minutes.
The calculation reads `namenode.blockSizeMiB` directly, so changing the block size keeps the budget consistent.

- **Faster object storage:** raise `datanode.gracefulDrain.uploadThroughputMiBps`.
  Doubling it halves the budget.
- **A larger expected backlog:** raise `objectStorage.datanode.asyncUpload.queueCapacity`.
  The budget grows linearly with it.
- **A fixed budget:** set `datanode.gracefulDrain.timeoutSecs` (the drain RPC) and `datanode.gracefulDrain.terminationGracePeriodSecs` (the pod grace period).
  Each can be set on its own.

## Turning the hook off

To remove the `preStop` hook while keeping asynchronous upload on:

```yaml
hopsfs:
  datanode:
    gracefulDrain:
      enabled: false
```

The chart then omits both the `lifecycle` block and `terminationGracePeriodSeconds` from the DataNode pod, so the kubelet sends `SIGTERM` as soon as the pod is deleted and kills the DataNode after the default 30-second grace period, whatever its upload backlog.
Use this only when the drain itself misbehaves.
For an emergency shutdown without draining, the regular `shutdownDatanode` RPC is still available.

## PodDisruptionBudget

The DataNode PodDisruptionBudget sets `maxUnavailable: 1`, so evictions, such as those of a node drain, take down one DataNode at a time.
It does not limit pods you delete yourself, so do not delete DataNode pods while a node drain is evicting another one.
It protects client writes, not the drain budget.
When two or more DataNodes are unavailable at once, a write that loses a member of its pipeline asks the NameNode for a replacement within a bounded number of retries, and fails if no healthy DataNode is available in time.
The PodDisruptionBudget therefore applies whether asynchronous upload is on or off.

With `datanode.count: 1`, the default, the chart renders no PodDisruptionBudget.
