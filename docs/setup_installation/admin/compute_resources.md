---
description: Cluster configuration for the per-project Compute Resources Usage view
---

# Configure the Compute Resources Usage view

## Introduction

This page is for cluster administrators.
It explains how the per-project node list in the **Compute Resources Usage** card is derived, and the RBAC required for that derivation to work.
For the end-user view of the same card, see [Compute Resources Usage][compute-resources-usage].

When Kueue is installed, the card limits the node list to nodes a given project can actually schedule on.
The mapping is driven entirely by standard Kueue objects: **LocalQueue → ClusterQueue → ResourceFlavor**.
There is no Hopsworks-specific configuration on top.

## How project → node visibility is derived

For each project, Hopsworks walks the queue hierarchy bound to the project's Kubernetes namespace.

- Start from every `LocalQueue` in the project's namespace.
- Follow each `LocalQueue.spec.clusterQueue` to its `ClusterQueue`.
- For each `ClusterQueue`, collect the `ResourceFlavor`s named in `spec.resourceGroups[].flavors[].name`.

The resulting set of `ResourceFlavor`s is the project's "reachable flavors".
A node is included in the project's Node Resources view only if it matches at least one reachable flavor.

The per-queue node filter in the UI is built from the same walk, but kept keyed by `LocalQueue` name so users can narrow the view to a single queue.

## How a ResourceFlavor matches a node

A node matches a `ResourceFlavor` when both of these hold.

- **Labels:** every key/value in `ResourceFlavor.spec.nodeLabels` is present on the node with the same value.
  Extra labels on the node are fine — the flavor's label set must be a subset of the node's labels.
- **Taints:** every taint on the node with effect `NoSchedule` or `NoExecute` is covered, either by a matching entry in `ResourceFlavor.spec.nodeTaints` or by a matching entry in `ResourceFlavor.spec.tolerations`.
  Taints with effect `PreferNoSchedule` are soft and do not block matching.

Both rules mirror Kueue's own admission logic, so the view reflects exactly which nodes Kueue would dispatch work to for that flavor.

Cordoned nodes (`spec.unschedulable: true`) and nodes the metrics server cannot report on are dropped from the view regardless of flavor matching, because no useful capacity figure can be produced for them.

## Required RBAC

Hopsworks needs read access to the Kueue CRDs in order to walk the queue hierarchy.
The Hopsworks Helm chart ships a `ClusterRole` and binding that grant these permissions, so a default install needs no extra action.

If you are managing RBAC manually (e.g. an externally provisioned `hopsworks` service account), grant at least the following:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: hopsworks-kueue-reader
rules:
  - apiGroups: ["kueue.x-k8s.io"]
    resources: ["localqueues", "clusterqueues", "resourceflavors"]
    verbs: ["get", "list"]
```

Bind this role to the service account Hopsworks runs as.
The walk uses `get` and `list` only; no `watch`, `create`, `update`, or `delete` is needed.

## Troubleshooting

The view surfaces several distinct situations.
Use the table below to map a symptom to a likely cause.

| Symptom | Likely cause |
| --- | --- |
| Node Resources sub-section is empty and the access notice says *"None of the queues available in this project currently match any nodes in the cluster."* | The project's LocalQueues resolve to flavors that don't match any node — check `ResourceFlavor.spec.nodeLabels` and `nodeTaints`/`tolerations` against the actual node labels and taints. |
| Node Resources lists every schedulable node and there is no Queue filter or Queue Resources sub-section | Kueue is not installed, the project namespace has no LocalQueues, or Hopsworks lacks the Kueue RBAC above. All three cases fall through to the legacy non-Kueue path, with no access notice. To distinguish: `kubectl get crd resourceflavors.kueue.x-k8s.io` (absent means Kueue isn't installed), then `kubectl auth can-i list localqueues.kueue.x-k8s.io -n <project-ns> --as=system:serviceaccount:<hopsworks-ns>:<hopsworks-sa>` (`no` means apply the `ClusterRole` and binding above). The `-n` flag is required because `LocalQueue` is namespaced; `--as=` requires the caller to have ServiceAccount impersonation rights (granted by `cluster-admin`). |
| A node you expect to see is missing | The node is either cordoned, missing from the metrics server, or not matched by any reachable flavor — check `kubectl describe node` for `Unschedulable: true` and confirm node labels/taints satisfy the flavor rules above. |

## See also

- [Compute Resources Usage][compute-resources-usage] — the end-user view this configuration drives.
- [Kueue][kueue-details] — overview of the Kueue abstractions referenced above.
