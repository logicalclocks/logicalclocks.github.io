# HopsFS CSI Driver { #hopsfs-csi-driver }

## Introduction

Hopsworks mounts HopsFS into Airflow, Trino, and the jobs, notebooks and deployments it launches through a CSI driver, which the `hopsfs-csi` subchart installs.
A privileged node plugin, run as a DaemonSet, performs the FUSE mount for each pod's inline volume and hands the connection to a `hopsfs-fuse` sidecar in the pod, which runs unprivileged and as a non-root user.
The pods that mount HopsFS therefore carry no privileged container.

The driver is on by default (`global._hopsworks.csi.enabled: true`).
The node plugin is installed whenever something needs it: `global._hopsworks.full_platform`, Airflow or Trino.
The values are listed in [HopsFS CSI driver values][helm-values-hopsfs-csi].

## The node plugin { #hopsfs-csi-node-plugin }

- A node without the plugin cannot start any pod that mounts HopsFS.
  The DaemonSet therefore tolerates every taint, ignores `global._hopsworks.nodeSelector`, and runs at the `system-node-critical` priority.
  Narrow its `nodeSelector` or `tolerations` only for nodes that will never run such a pod.
- The plugin image is named once, in `global._hopsworks.csi.image`, with the registry from `global._hopsworks.imageRegistry`.
  The plugin and every sidecar are built from it, because the two ends of the handoff speak one protocol and must not differ on a node.
  The sig-storage helper images are pulled from the same registry under their upstream `registry.k8s.io` paths, so an airgapped install only sets the registry.
- Before it builds a pod that mounts HopsFS, the Hopsworks backend checks that the driver is registered, so the Hopsworks ClusterRole gets `get` on `csidrivers`.
  An install that sets `hopsworks.rbac.useExistingRole` adds that grant to its own role, or every such pod build fails with a 403.

## The driver name { #hopsfs-csi-driver-name }

Each release registers its own driver, named `<namespace>.hopsfs.csi.logicalclocks.com` after the release namespace.
Kubelet routes CSI calls by driver name alone, so the name per release is what lets two Hopsworks installations share a Kubernetes cluster.
Each gets its own node plugin, socket, registration and CSIDriver object, also on the nodes both use, and with different release names uninstalling one never touches the other's mounts or node plugin, as described in [Before you uninstall][uninstall-before].

Kubernetes caps a CSI driver name at 63 characters, so a namespace longer than 34 characters needs a shorter name in `global._hopsworks.csi.driverName`.
The render fails and names that value when it is needed.
A name set there must be unique in the Kubernetes cluster: two releases with one name share one socket and one registration on every node they share, and uninstalling either one breaks the other.

## Failure modes { #hopsfs-csi-failure-modes }

- **A crashed or restarted `hopsfs-fuse` sidecar leaves the pod's mount dead until the pod is recreated.**
  Reads and writes fail with `ENOTCONN`, and the restarted sidecar cannot resume the connection, so it crash-loops.
  Delete the pod.
- **A sidecar that never serves the mount**, for example because of bad certificates or an unreachable NameNode, leaves the pod's other containers in `ContainerCreating`.
  Read the sidecar's log with `kubectl logs <pod> -c hopsfs-fuse`.
- **A node without the plugin** cannot start any pod that mounts HopsFS, as described in [The node plugin][hopsfs-csi-node-plugin].

## OpenShift { #hopsfs-csi-openshift }

The node plugin needs `privileged`, `hostPath` volumes and `Bidirectional` mount propagation, none of which `restricted-v2` admits.
`values.openshift.yaml` ships SecurityContextConstraints (SCC) for it through `hopsfs-csi.openshift.securityContextConstraints`, which `global._hopsworks.openshift.enabled` also turns on.
The SCC is granted to the plugin's service account only, is named after the release and its namespace, and is installed as a `pre-install,pre-upgrade,pre-rollback` hook so that it exists before the plugin pods are admitted.
Its name, `<release>-<namespace>-hopsfs-csi-node-plugin`, is cut to 63 characters, so with a long release name and namespace find it with `oc get scc | grep hopsfs-csi-node-plugin`.
The `hopsfs-fuse` sidecars run under `restricted-v2` with the user and group IDs from the namespace's range that the overlay sets.

The CSIDriver carries the CSI volume admission profile `restricted` (`hopsfs-csi.openshift.csiEphemeralVolumeProfile`).
Leave it unless a cluster policy demands `baseline` or `privileged`, and never set it empty: without the profile, OpenShift requires `enforce=privileged` of every namespace that mounts the driver and rejects every Airflow and Trino pod.

### When the cluster administrators own the SCC { #hopsfs-csi-admin-scc }

Where whoever runs `helm install` may not create cluster-scoped SCCs, the cluster administrators create it, and the chart is told its name:

```yaml
hopsfs-csi:
  openshift:
    existingSecurityContextConstraints:
      name: <the SCC they created>
```

The chart then renders no SCC, and its uninstall cleanup leaves that one alone.
Give the administrators the chart's own SCC as the reference:

```bash
helm template <release> hopsworks/hopsworks --version <version> -n <namespace> \
  --set hopsfs-csi.openshift.securityContextConstraints=true \
  --show-only charts/hopsfs-csi/templates/scc.yaml
```

Whatever they derive from it must grant `system:serviceaccount:<release namespace>:hopsfs-csi-node-sa`, in its `users` list or through an RBAC `use` grant.

A missing or wrong SCC would otherwise fail silently: the DaemonSet gets no pod, and every pod that mounts HopsFS stays in `ContainerCreating` with no event that names the cause.
In this mode a `pre-install,pre-upgrade` hook Job therefore checks, before anything is installed:

- that the SCC exists;
- that it is the SCC that admits the plugin's pod template for the plugin's service account;
- that a representative pod that mounts HopsFS passes a server-side dry-run create in the release namespace.

When a check fails, the release fails, and the Job's log names the reason: a missing SCC, another SCC that admits the plugin first, or what the SCC lacks.

Switching an existing release to this mode leaves the SCC that the chart created before in place, because it is a Helm hook and the upgrade does not remove it.
The check fails while it exists, since it would keep admitting the plugin and hide a broken administrator SCC.
Delete it once the administrators' SCC is in place.
Running plugin pods are not affected, because an SCC is only consulted when a pod is admitted.
An administrator SCC that keeps the chart's generated name is theirs and passes the check.

```bash
oc delete scc <release>-<namespace>-hopsfs-csi-node-plugin
```

## Uninstalling { #hopsfs-csi-uninstall }

Kubelet can only unmount a CSI volume through the node plugin of its driver, so the plugin has to outlive the pods that mount HopsFS.
On `helm uninstall`, or when the release namespace is deleted, the plugin keeps serving unmounts until none of its own mounts is left, and exits then.
When it is only replaced, by a rollout or an eviction, it exits at once.
`hopsfs-csi.node.terminationGracePeriodSeconds` (default 300) bounds the wait: keep it above the longest `terminationGracePeriodSeconds` of any pod that mounts HopsFS.

A pod left in `Terminating` after an uninstall means the plugin stopped before kubelet unmounted the pod's volume.
Force-delete the pod, and remove its `fuse.hopsfs` mount on the node with `nsenter --mount=/proc/1/ns/mnt umount -l <path>`.

The CSIDriver object, which a pre-install hook creates on a first install so that it exists before the Deployments that mount it, and on OpenShift the SCC that the chart ships, are not release resources, so `helm uninstall` itself does not remove them.
A post-delete hook (`hopsfs-csi.cleanupOnUninstall.enabled`, on by default) deletes both, best effort.
After `helm uninstall --no-hooks`, delete them by hand:

```bash
kubectl delete csidriver <namespace>.hopsfs.csi.logicalclocks.com --ignore-not-found   # or your driverName
oc delete scc <release>-<namespace>-hopsfs-csi-node-plugin --ignore-not-found          # OpenShift only
```

A reinstall does not depend on either: Helm replaces a CSIDriver or SCC that is still there.

## Turning the driver off { #hopsfs-csi-off }

Trino requires the driver: its password file, group file, access-control rules, user catalogs and mountable secrets reach its pods only through inline volumes of it.
`global._hopsworks.csi.enabled: false` therefore renders only together with `global._hopsworks.trino.enabled: false`, and the render fails otherwise, rather than leaving every Trino pod in `ContainerCreating`.

With the driver off, Airflow and the workloads Hopsworks launches go back to mounting HopsFS from a privileged container in the pod.
On OpenShift the chart grants no SCC for that container, because the SCC it ships is for the node plugin only.
The Airflow pods are then admitted only if the cluster already grants the Airflow service account `privileged`; without that grant `restricted-v2` rejects them and the Airflow Deployments stay at zero replicas.
The same holds for the workloads Hopsworks launches.
