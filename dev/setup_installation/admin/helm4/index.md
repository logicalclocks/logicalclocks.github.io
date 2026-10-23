# Upgrading with Helm 4 { #upgrading-with-helm-4 }

## Which apply mode you get { #helm4-apply-mode }

Helm 4 applies manifests server-side.
Under server-side apply (SSA) the API server records, per field, which manager last set it, and refuses an apply that would change a field another manager owns.
Helm 3's client-side apply has no notion of field ownership.

| Operation | Apply mode |
| --------- | ---------- |
| `helm install` with Helm 4 | server-side |
| `helm upgrade` with Helm 4 | `--server-side=auto`, which inherits the mode of the previous release |
| `helm upgrade` with Helm 4 on a release installed by Helm 3 | client-side, until you pass `--server-side=true` |
| anything with Helm 3 | client-side |

A release installed by Helm 3 and upgraded with Helm 4 therefore stays client-side.
It never meets the server-side behaviour described below, and it never gets the server-side fixes either.

From 5.2.0 the chart no longer competes with in-cluster controllers over three sets of fields.
It no longer declares two of them at all: `.spec.replicas` on workloads that have a HorizontalPodAutoscaler (HPA), and the `.webhooks[].rules` of the two Knative Serving webhooks.
The third, the controller-computed properties of the RSS ConfigMap, it still declares, but it now renders exactly what the Uniffle operator computes, so the two managers never disagree about the content.
The two migrations below happen once, on the first upgrade to 5.2.0 or later of a release that ran an earlier chart.
Charts before 5.2.0, 5.1.x included, still declare these fields.

## `.spec.replicas` on workloads scaled by an HPA { #helm4-hpa-replicas }

This affects `arrowflight`, `docker-registry`, `hopsworks-ca`, `onlinefs`, `logstash` and the Hopsworks worker Deployment, whenever the chart renders an HPA for them.
The chart drops `replicas` exactly when it renders the workload's HPA.
`arrowflight` and `docker-registry` are therefore not affected while a VerticalPodAutoscaler targets them (`global._hopsworks.vpaEnabled` together with `autoscalers.arrowflight.enabled` or `autoscalers.docker.enabled`), because that suppresses their HPA and the chart keeps declaring `replicas`.

Charts before 5.2.0 declared `replicas` and shipped an HPA for the same workload.
The first upgrade to 5.2.0 or later removes the field, and Kubernetes defaults a workload without `replicas` to 1.
Measured on k3s v1.33.4 with an autoscaler holding the workload at 5 replicas:

| Upgrade path | Live replicas after the first upgrade |
| ------------ | ------------------------------------- |
| Helm 3 to Helm 3 | 5 to 1 |
| Helm 3 install, Helm 4 upgrade (`auto`, so client-side) | 5 to 1 |
| Helm 4 (SSA) to Helm 4 (SSA) | 5 preserved |
| any path, second and later upgrades | live count preserved |

The HPA restores the count within one sync, about 15 seconds in that test, and the workload climbs back to its scaled size only as the metric drives it there.
It returns to the HPA's `minReplicas`, which for five of the six workloads is the configured `replicas` value: `arrowflight.deployment.replicas`, `onlinefs.deployment.replicas`, `hopsworks.hopsworksCA.ca_count`, `hopsworks.replicaCount.worker` and `olk.logstash.replicas`.
`docker-registry` is the exception: its HPA takes its own `docker-registry.hpa.minReplicas` (default 1), so a registry configured with `replicas: 2` and `hpa.minReplicas: 1` settles at 1, not 2.
Its PodDisruptionBudget is rendered from that same floor, so a registry whose floor is 1 gets no PodDisruptionBudget rather than a `minAvailable: 1` budget that would block every drain of its node.

Take the first upgrade of an HPA-scaled release with Helm 4 and `--server-side=true`, which keeps the live count, unless a RonDB autoscaler holds its StatefulSet at another size than the chart's, as described in [RonDB][helm4-rondb].
For a release installed by Helm 3 this is inferred rather than measured: a server-side apply that omits the field is not expected to remove the copy that the earlier client-side applies recorded.
That works because `kube-controller-manager` co-owns `.spec.replicas` once the HPA has actually rescaled the workload.
On a release whose HPA is enabled but has never fired, Helm is still the only owner and removes the field, so that release drops to 1 like the client-side path.
If you upgrade client-side, expect one dip to a single replica per affected workload, and plan it like any other rolling change.

A fresh install starts at the same place: the workload is created without `.spec.replicas`, so Kubernetes defaults it to 1 and the HPA raises it to `minReplicas` on its next sync.
With `--wait`, `helm install` can therefore return while a workload configured for more replicas still runs one.

Charts before 5.2.0 were not neutral here either.
On every client-side upgrade they reset an autoscaled workload to the chart's `replicas` value (5 to 3 in the same test), and on Helm 4 with SSA they failed with `conflict with "kube-controller-manager" with subresource "scale"`.

Turning an HPA off after it has scaled its workload still conflicts under SSA, because the chart starts declaring `replicas` again while `kube-controller-manager` owns the field.
Pass `--force-conflicts` for that one upgrade, or scale the workload to the configured value first.

## The RSS ConfigMap { #helm4-rss-configmap }

This only affects a release that ran a chart before 5.2.0 under Helm 4 with SSA.
There, the Uniffle operator rewrote `.data.coordinator.conf` and `.data.server.conf` of the `rss-configuration` ConfigMap and took ownership of those fields away from Helm.
From 5.2.0 the chart renders exactly what the operator computes, so on a fresh install the operator's write changes nothing and Helm stays the only owner.
On a release that already lost the fields, ownership has to be handed back once.

`helm upgrade --force-conflicts` does not do that.
Applying the new, byte-identical content leaves the field co-owned by `helm` and the operator's `controller` manager, and the force has nothing to conflict with.
The next real change of an RSS value then fails with `conflict with "controller" using v1: .data.server.conf`.
Forcing a changed value reclaims only the key that changed and leaves the other one conflicting.

Hand ownership back explicitly, once, before or after the upgrade:

```bash
NS=hopsworks   # your release namespace

# Build a JSON patch that drops every non-Helm manager entry from managedFields.
# Highest index first, so the removals do not renumber each other.
kubectl -n "$NS" get configmap rss-configuration --show-managed-fields -o json \
  | jq '[.metadata.managedFields | to_entries[] | select(.value.manager != "helm") | .key]
        | sort | reverse
        | map({op: "remove", path: ("/metadata/managedFields/" + (. | tostring))})' > /tmp/strip.json

kubectl -n "$NS" patch configmap rss-configuration --type=json --patch-file /tmp/strip.json
```

Check that only `helm` remains:

```bash
kubectl -n "$NS" get configmap rss-configuration --show-managed-fields -o yaml
```

Under ArgoCD the applying manager is `argocd-controller`, not `helm`, so keep that entry instead.
Whether ArgoCD applies server-side at all is decided by the `syncOptions` of the Application, which the chart does not control.
Later `helm upgrade` runs that change an RSS value then apply cleanly, and the operator's next reconcile writes identical bytes, so it never takes the field back.

Do not use a release-wide `helm upgrade --force-conflicts` instead.
It is not limited to the ConfigMap: a forced apply also takes `.spec.replicas` back from `kube-controller-manager` and resets an autoscaled workload to the chart's value, for Hopsworks' own workloads and for the RonDB subchart alike.

Resetting `managedFields` as a whole (`kubectl patch -p '{"metadata":{"managedFields":[{}]}}'`) is no substitute either.
It attributes every field to a synthetic `before-first-apply` manager, and the same conflict comes back one apply later.

## Knative Serving webhooks { #helm4-knative-webhooks }

From 5.2.0 the chart no longer renders `.webhooks[].rules` for the Knative Serving mutating and validating webhook configurations.
The Knative webhook controller owns them and rewrites them from its own resource registry.

On the first client-side upgrade to 5.2.0 or later the rules are removed from the object until that controller reconciles them back.
The controller watches the object, so the window is short, but only while the controller is running.
While the rules are absent no Knative resource is intercepted, so Knative resources created or updated in that window skip Knative's defaulting and validation.
If the Knative webhook Deployment is down or cannot be scheduled, the window lasts until it recovers.

An upgrade with Helm 4 and SSA does not go through this window: the chart stops declaring the field, and the controller keeps ownership.

## CRDs applied by a 5.0.x release { #helm4-retained-crds }

Helm never deletes CRDs, and the KServe CRD upgrade Job applies the cert-manager, Knative and KServe CRDs server-side under its own field manager, so it owns their `app.kubernetes.io/version` label.
A fresh Helm 4 install fails within seconds when that label on the CRDs differs from the value the chart installs.
CRDs last applied by a 5.0.x release, whose CRD upgrade Job ships an older bundle, carry such a value.
Before a fresh Helm 4 install into a Kubernetes cluster that still runs a 5.0.x release, upgrade that release with `helm upgrade` to a chart of 5.1.0 or later, so that its CRD upgrade Job applies the current CRDs.

## RonDB { #helm4-rondb }

The RonDB subchart (rondb-helm 26.2.21 in Hopsworks 5.2 and 5.3) still declares `replicas` alongside an HPA for its `rdrs` StatefulSet, and for `mysqld` at the RonDB chart's own default values.
Every client-side upgrade therefore resets those StatefulSets to their configured `replicas`, and a Helm 4 upgrade with SSA conflicts with `kube-controller-manager` on them.

With the Hopsworks defaults, an HPA scales `rdrs` between `rondb.rondb.clusterSize.minNumRdrs` (1) and `maxNumRdrs` (2).
A server-side upgrade fails on that StatefulSet while its HPA holds it at another size than the chart's `replicas`, which `kubectl get hpa -n hopsworks` shows.
Upgrade that release client-side instead (`--server-side=false` on a release installed with Helm 4), and accept the reset of the RonDB StatefulSets and the one-time dip of the Hopsworks workloads described above.
Do not pass a release-wide `--force-conflicts` instead, for the reasons given under [The RSS ConfigMap][helm4-rss-configmap].
