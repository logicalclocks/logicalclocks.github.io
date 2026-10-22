---
description: What uninstalling a Hopsworks Helm release deletes, how to keep data, the settings to check first, and what is left on the Kubernetes cluster afterwards
---

# Uninstalling Hopsworks { #uninstalling-hopsworks }

## Introduction

`helm uninstall` deletes the release's resources, and hooks in the chart clean up what Helm does not track.
Two settings decide how much data goes with it, and both are off only when you turn them off.
Read [Before you uninstall][uninstall-before] first: on a default installation, an uninstall deletes the data volumes and the project namespaces that Hopsworks created.

## Before you uninstall { #uninstall-before }

- **`hopsworks.wipeWhenUninstall`** lists resource kinds.
  After the uninstall, a post-delete Job deletes every resource of those kinds, in every namespace, that belongs to the release or carries the `hopsworks.ai/project` label, and clears its finalizers.
  Hopsworks puts that label on the project namespaces it creates and on the network policy of every project.
  The default list includes namespaces, so the project namespaces that Hopsworks created go too, with everything in them.
  Namespaces provisioned in advance (`hopsworks.variables.kube_skip_namespace_creation: true`) carry no label and stay; only their project network policies go.
  The label does not name the installation.
  On a Kubernetes cluster with more than one Hopsworks installation, the Job therefore also deletes the project namespaces that the other installations created, with everything in them, and the network policies of their projects, which those installations restore on their next reconcile.
  Set the list empty (`hopsworks.wipeWhenUninstall: []`) to turn the Job off, on every installation of such a cluster.
- **`global._hopsworks.wipeDataOnUninstall`** (default `true`) lets the cleanup hooks of the subcharts delete the data volumes their StatefulSets leave behind: HopsFS DataNodes, Kafka, OpenSearch, Consul, MinIO, the Spark shuffle servers, the Superset database and the BuildKit daemon.
  A volume labelled `hopsworks.ai/keep=true` is skipped.
  The label protects a volume from these hooks only, not from `wipeWhenUninstall`, from a StatefulSet that deletes its own volumes, or from deleting the namespace.
- **`hopsworks.dropDatabase`** (default `false`) drops the Hopsworks databases on uninstall.

Helm runs the hooks of the deployed revision, so a change to any of these takes effect only once a `helm upgrade` has applied it.
Back up what you need first, as described in [Disaster Recovery][disaster-recovery].

## Uninstall { #uninstall-steps }

```bash
helm uninstall <release> -n <namespace> --timeout=900s
```

Delete the namespace only when nothing in it has to survive.
Deleting it deletes every persistent volume claim left in it, including those labelled `hopsworks.ai/keep=true` or kept by `wipeDataOnUninstall: false`, and with the reclaim policy `Delete` also the storage behind them.
To keep data volumes, leave the namespace in place.

```bash
kubectl delete namespace <namespace>
```

Each hook has to finish within the timeout.
Two pre-delete hooks wait up to 120 seconds each for an operator to finalize its resources: the TLS certificates and KEDA.

## What the hooks clean up { #uninstall-hooks }

Before the release's resources are deleted, while the operators still run:

- every `HopsworksCert` is deleted, so that the certificate operator releases its finalizers (`certs-operator.gracefulCertTeardown`);
- every KEDA resource is deleted and finalized, as described in [KEDA Autoscaling][keda-uninstall];
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
- **Everything the hooks would delete, after `helm uninstall --no-hooks`.**
  Delete the HopsFS CSIDriver and SCC by hand then, as described in [HopsFS CSI Driver][hopsfs-csi-uninstall].
- **Volumes no hook deletes.**
  List them with `kubectl get pvc -n <namespace>` before you delete the namespace.

## Under ArgoCD { #uninstall-argocd }

ArgoCD runs `pre-delete` hooks as `PreDelete` hooks from ArgoCD 3.3 only, and `post-delete` hooks as `PostDelete` hooks from 2.10.
From 2.10 to 3.2 the steps before the deletion do not run:

- a post-delete hook clears the finalizers of the `HopsworksCert` resources instead;
- KEDA's resources are not finalized first, which needs a step before you delete the Application, as described in [KEDA Autoscaling][keda-uninstall].
