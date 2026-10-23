# KEDA Autoscaling { #keda-autoscaling }

## Introduction

Standard-mode model deployments run behind a plain Kubernetes Deployment, which Knative's request-based autoscaler does not see.
KEDA scales them on CPU and memory, on the requests at the gateway, and for LLM deployments on the vLLM engine metrics, and its HTTP add-on scales them to zero when idle.
What a deployment can do with it is described in [How To Configure Scaling For A Deployment][how-to-configure-scaling-for-a-deployment].

The Hopsworks Helm chart installs KEDA by default, through the `hw-keda` subchart.
One value both installs the subchart and tells the Hopsworks backend that KEDA is there, so the backend never offers KEDA-backed scaling on a cluster without the operator.
To leave KEDA out:

```yaml
hopsworks:
  variables:
    kube_keda_installed: false
```

Without KEDA, Standard-mode deployments fall back to KServe's own Horizontal Pod Autoscaler on CPU and memory, without the engine metrics and without scale to zero.
The values are listed in [KEDA values][helm-values-hw-keda].

## What the chart installs { #keda-components }

- KEDA 2.21: the operator, the metrics API server and the admission webhooks, in the Hopsworks namespace.
  The operator watches every namespace, because the ScaledObjects live in the project namespaces.
  Upstream tests KEDA 2.21 on Kubernetes 1.34 to 1.36.
- The KEDA HTTP add-on 0.16: its operator, interceptor and external scaler, next to KEDA.
- The eight `keda.sh`, `http.keda.sh` and `eventing.keda.sh` CustomResourceDefinitions (CRDs).

The images are mirrors of `ghcr.io/kedacore/*` under `docker.hops.works/ghcr.io/`.
An airgapped install overrides them under `hw-keda.keda.image` and `hw-keda.keda-add-ons-http.images`, as the chart's `values.airgap.yaml` shows.
From 5.2.2 the CRD upgrade hook also pulls `hopsworks/keda-crds`, as described in [CustomResourceDefinitions][keda-crds].
It is pulled from `global._hopsworks.imageRegistry` like every Hopsworks image, so mirror `hopsworks/keda-crds` next to the other Hopsworks images; an airgap overlay needs nothing more for it.

The chart ships Hopsworks rebuilds of the KServe controller and of the HTTP add-on images, under the upstream image names with a `-h<revision>` tag: `kserve/kserve-controller:0.21.0-h1` and `ghcr.io/kedacore/http-add-on-*:0.16.0-h2`.
These tags exist only on `docker.hops.works` and its public ECR mirrors, not on ghcr.io or Docker Hub, so an airgapped install mirrors them from there.

## CustomResourceDefinitions { #keda-crds }

The CRDs ship in the subchart's `crds/` directory, which Helm creates only on install and never updates.
A `pre-upgrade` hook, `keda-crd-upgrade`, therefore applies the same CRDs server-side on every upgrade: it creates them on a release upgraded from a chart without KEDA, and updates them when the KEDA version moves.
Under ArgoCD it runs as a PreSync hook on every sync.

From 5.2.2 the hook reads the CRDs from the `hopsworks/keda-crds` image (`hw-keda.crdUpgradeJob.image`) and checks each file against the chart's own copy before it applies anything, so an image built for another KEDA version fails the hook, naming the expected versions.
5.2.0 and 5.2.1 passed the CRDs to the hook in a ConfigMap, `keda-crd-upgrade-crds`, which a failed upgrade can leave behind and later charts neither create nor delete.
Delete a leftover by hand:

```bash
kubectl -n <namespace> delete configmap keda-crd-upgrade-crds --ignore-not-found
```

## Cluster requirements { #keda-requirements }

- **One external metrics provider per Kubernetes cluster.**
  KEDA registers the `v1beta1.external.metrics.k8s.io` APIService, which only one provider can hold.
  Remove a KEDA that is already installed first, including the Custom Metrics Autoscaler operator on OpenShift, a KEDA fork that claims the same APIService, or leave the subchart off.
  The `prometheus-adapter` that the chart ships serves `custom.metrics.k8s.io` only and does not conflict.
- **Egress to Prometheus.**
  The scalers query the Hopsworks Prometheus (`<release>-prometheus-server`, port 80, without authentication) with the operator's own service account.
  A cluster that denies egress by default sets `hw-keda.keda.networkPolicy.enabled: true`, the upstream policy that admits the operator's egress to every pod.
- **OpenShift.**
  The KEDA pods run under `restricted-v2` unchanged: non-root, without a fixed UID, with all capabilities dropped, a read-only root filesystem and the `RuntimeDefault` seccomp profile.
  No SecurityContextConstraints are shipped or needed.
  `values.openshift.yaml` removes the HTTP add-on's `podSecurityContext.fsGroup: 1000`, so its pods are admitted with the namespace's UID range.

## Idle scale to zero { #keda-http-add-on }

KEDA alone cannot scale a deployment to zero, because a request that arrives at zero replicas has nothing to land on.
The HTTP add-on puts an interceptor in the request path, which holds the first request while KEDA starts a replica.
It is part of `hw-keda`, not a separate switch, and the chart gives the backend the addresses of its interceptor and scaler (`kube_keda_http_interceptor_address`, `kube_keda_http_scaler_address`).

- For a deployment with idle scale to zero on, Hopsworks owns the ScaledObject, an `InterceptorRoute`, and an Istio Ingress in the project namespace that sends the deployment's hosts to the interceptor through an ExternalName Service.
  KServe runs no autoscaler and creates no Ingress for that deployment.
- The interceptor is in the request path of those deployments only; all other traffic goes straight to the Istio gateway.
- The interceptor scales with its own load, from 1 to 10 replicas by default (`hw-keda.keda-add-ons-http.interceptor.replicas`).
- Its request timeouts default to 600 seconds, so a cold start that loads a model does not fail the request that woke the deployment.

## Uninstalling { #keda-uninstall }

Helm never deletes the CRDs in `crds/`, and every ScaledObject carries a finalizer that only the KEDA operator clears.
A cleanup hook, `keda-cleanup`, therefore runs twice on `helm uninstall`:

- Before the release's resources are deleted (`pre-delete`), while the operators still run, it deletes every `keda.sh`, `http.keda.sh` and `eventing.keda.sh` resource.
  It waits up to `hw-keda.cleanupOnUninstall.finalizeTimeoutSeconds` (120 seconds) for the operators to finalize them, then clears the finalizer from whatever is left.
  An uninstall that waits for every resource to be gone, such as `helm uninstall --wait` or an ArgoCD deletion, then finishes.
- After the release is deleted (`post-delete`), it deletes anything created in between, the TLS Secret the operator generated, and the CRDs themselves.
  Set `hw-keda.cleanupOnUninstall.deleteCrds: false` to keep the CRDs, for example for a KEDA installed by other means next.
  The Hopsworks backend recreates its ScaledObjects when a deployment starts.

Allow for the first pass in the uninstall timeout.
Turn the hook off with `hw-keda.cleanupOnUninstall.enabled: false` only when something else removes those resources.
Without it the KEDA objects stay behind under a finalizer that nothing clears once the operators are gone, and deleting the CRDs later leaves them `Terminating`, which blocks the next install.

Under an ArgoCD that runs no pre-delete hooks, as described in [Under ArgoCD][uninstall-argocd], the first pass does not run, and deleting the Application can wait on CRDs stuck in `Terminating`.
There, delete the Standard-mode deployments, or the `keda.sh` objects, before you delete the Application.
