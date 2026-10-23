# Uninstalling Hopsworks { #uninstalling-hopsworks }

## Introduction

`helm uninstall` deletes the release's resources, and hooks in the chart clean up what Helm does not track.
An uninstall is destructive: the only way to bring an installation's data back is to restore it from a backup, as described in [Disaster Recovery][disaster-recovery].
Read [Before you uninstall][uninstall-before] first.

## Before you uninstall { #uninstall-before }

- **Back up first.**
  Every uninstall deletes the volumes of the RonDB data and management nodes and of the Superset database, whatever the settings below say, because their StatefulSets delete their volumes when they are deleted.
- **`hopsworks.wipeWhenUninstall`** lists resource kinds.
  After the uninstall, a post-delete Job deletes every resource of those kinds, in every namespace, that carries this release's name in `meta.helm.sh/release-name` or carries the `hopsworks.ai/project` label, and clears its finalizers.
  The release name is matched in any namespace, so installations that share a Kubernetes cluster need different release names.
  Hopsworks puts the `hopsworks.ai/project` label on the project namespaces it creates and on the network policy of every project.
  The default list includes namespaces, so the project namespaces that Hopsworks created go too, with everything in them.
  Namespaces provisioned in advance (`hopsworks.variables.kube_skip_namespace_creation: true`) carry no label unless you added `hopsworks.ai/project` yourself, for example so that 5.0 and 5.1 collect their logs; without it they stay, and only their project network policies go.
  The label does not name the installation either.
  On a Kubernetes cluster with more than one Hopsworks installation, the Job therefore also deletes the project namespaces that the other installations created, with everything in them, and the network policies of their projects, which those installations restore on their next reconcile.
  Set the list empty (`hopsworks.wipeWhenUninstall: []`) to turn the Job off, on every installation of such a cluster.
- **`global._hopsworks.wipeDataOnUninstall`** (default `true`) lets the cleanup hooks of the subcharts delete the data volumes their StatefulSets leave behind: HopsFS DataNodes, Kafka, OpenSearch, Consul, MinIO, the Spark shuffle servers and the BuildKit daemon, and the Superset database on clusters whose Superset StatefulSet predates its volume retention policy.
  A volume labelled `hopsworks.ai/keep=true` is skipped.
  The label protects a volume from these hooks only, not from `wipeWhenUninstall`, from a StatefulSet that deletes its own volumes, or from deleting the namespace.
  Turning the setting off, or labelling a volume, leaves those volumes on the cluster; it is not a way to recover the installation.
- **`hopsworks.dropDatabase`** (default `false`) drops the Hopsworks databases on uninstall.

Helm runs the hooks of the deployed revision, so a change to any of these takes effect only once a `helm upgrade` has applied it.

## Uninstall { #uninstall-steps }

```bash
helm uninstall <release> -n <namespace> --timeout=900s
```

Delete the namespace only when nothing in it has to stay.
Deleting it deletes every persistent volume claim left in it, including those labelled `hopsworks.ai/keep=true` or kept by `wipeDataOnUninstall: false`, and with the reclaim policy `Delete` also the storage behind them.

```bash
kubectl delete namespace <namespace>
```

Each hook has to finish within the timeout.
Two pre-delete hooks wait up to 120 seconds each for an operator to finalize its resources, the TLS certificates and KEDA, and a third calls the Hopsworks API.

## What the hooks clean up { #uninstall-hooks }

Before the release's resources are deleted, while the operators and Hopsworks still run:

- every `HopsworksCert` in the release namespace is deleted, so that the certificate operator releases its finalizers (`certs-operator.gracefulCertTeardown`);
- every KEDA resource is deleted and finalized, as described in [KEDA Autoscaling][keda-uninstall];
- the API key of OnlineFS is deleted through the Hopsworks API;
- the Spark remote shuffle service and the Knative validating webhook are removed.

After the release's resources are deleted:

- Secrets and ConfigMaps that services and setup Jobs created at runtime, such as webhook certificates and Consul tokens, are deleted;
- the data volumes listed under `wipeDataOnUninstall` are deleted, and so are the Kafka node pools;
- the KEDA CustomResourceDefinitions are deleted;
- the HopsFS CSIDriver object and, on OpenShift, the SCC the chart ships are deleted, as described in [HopsFS CSI Driver][hopsfs-csi-uninstall];
- the `wipeWhenUninstall` Job runs last.

## What stays { #uninstall-leftovers }

- **CustomResourceDefinitions.**
  Helm never deletes CRDs.
  Apart from KEDA's, the CRDs the chart installs, such as Strimzi's, KServe's and the certificate operator's, stay on the Kubernetes cluster, and a reinstall uses them.
- **The `wipeWhenUninstall` Job's own ClusterRole and ClusterRoleBinding**, both named `<release>-uninstall-job`, after every uninstall with that Job on.
  They keep cluster-wide delete rights on the kinds the Job deletes, so delete them:

    ```bash
    kubectl delete clusterrole,clusterrolebinding <release>-uninstall-job
    ```

- **Everything the hooks would delete, after `helm uninstall --no-hooks`.**
  That includes the KEDA CRDs, and the Kafka node pools, whose brokers and controllers keep running with their volumes bound until you delete the pools:

    ```bash
    kubectl delete kafkanodepool -n <namespace> -l strimzi.io/cluster=<kafka cluster>
    ```

    `HopsworksCert` resources stay too, under a finalizer that nothing clears once the certificate operator is gone, and keep the namespace from being deleted.
    Clear their finalizers:

    ```bash
    kubectl -n <namespace> get hopsworkscerts.certs.hopsworks.ai -o name \
      | xargs -I{} kubectl -n <namespace> patch {} --type=merge -p '{"metadata":{"finalizers":[]}}'
    ```

    Delete the HopsFS CSIDriver and SCC by hand as well, as described in [HopsFS CSI Driver][hopsfs-csi-uninstall].
- **Volumes no hook deletes.**
  List them with `kubectl get pvc -n <namespace>` before you delete the namespace.

## Under ArgoCD { #uninstall-argocd }

ArgoCD runs `pre-delete` hooks as `PreDelete` hooks from ArgoCD 3.3 only, and `post-delete` hooks as `PostDelete` hooks from 2.10.
From 2.10 to 3.2 the steps before the deletion do not run:

- a post-delete hook clears the finalizers of the `HopsworksCert` resources instead;
- KEDA's resources are not finalized first, which needs a step before you delete the Application, as described in [KEDA Autoscaling][keda-uninstall].
