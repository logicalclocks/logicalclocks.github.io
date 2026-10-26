---
description: How the Hopsworks Helm chart installs Envoy Gateway to serve Standard-mode model deployments through the Kubernetes Gateway API next to Istio, what it needs from the cluster, its images on an airgapped cluster, and how it is removed
---

# Envoy Gateway { #envoy-gateway }

## Introduction

Inference traffic enters through the Istio ingress gateway.
A Lua filter rewrites `/v1/<project>/<deployment>/...` to the deployment's host, an `ext_authz` filter asks `model-serving-authenticator` whether the API key may reach that deployment, and the request is routed by host: through Knative for Knative-mode deployments, and through an Istio-class Ingress that KServe creates for Standard-mode ones.
KServe's Standard mode and its generative-AI features (`LLMInferenceService`, llm-d, the agent router) are built on the Kubernetes Gateway API instead of Ingresses.

From 5.3 the chart can serve Standard-mode deployments through the Gateway API on Envoy Gateway, installed next to Istio and Knative, which keep working as they are.
Istio stays the external front door and forwards the Standard-mode hosts to the Gateway inside the cluster, so clients keep the same endpoint, ports and URL shapes, and Knative traffic never leaves Istio.
The feature is off by default, and two values stage it:

```yaml
global:
  _hopsworks:
    envoyGateway:
      enabled: true
      kserveStandardMode: true
```

`enabled` installs Envoy Gateway and the Gateway, and routes nothing on its own.
`kserveStandardMode` moves the Standard-mode deployments to it, and defaults to `true`, so `enabled: true` alone does both stages in one upgrade.
On a cluster with running deployments, set `kserveStandardMode: false` for the first upgrade and follow [Envoy Gateway][upgrade-envoy-gateway] in the upgrade guide, which lists the checks between the stages and the staged rollback.
The values are listed in [Envoy Gateway values][helm-values-hw-envoy-gateway] and under `kserve.envoyGateway` in [KServe values][helm-values-kserve].

## What the chart installs { #envoy-gateway-components }

- The Envoy Gateway 1.9 controller, through the `hw-envoy-gateway` subchart, a vendored copy of the upstream `gateway-helm` chart, in the Hopsworks namespace.
  It watches every namespace, because the HTTPRoutes KServe creates live in the project namespaces.
- A GatewayClass named `<release>-envoy-gateway`.
- In the `kserve` subchart, the Gateway `kserve-ingress-gateway` with the Envoy proxies the controller deploys for it, a SecurityPolicy that checks every request with `model-serving-authenticator` the way Istio's `ext_authz` filter does, with the CORS origins of `kserve.istio.envoyFilter.corsAllowedOrigins`, a BackendTrafficPolicy with no request timeout, and a lowest-precedence Istio VirtualService that forwards to the Gateway any host Istio does not route itself.
- The eighteen CustomResourceDefinitions (CRDs): eight of Envoy Gateway and the ten of the Gateway API standard channel 1.6, applied by a hook as described in [CustomResourceDefinitions][envoy-gateway-crds].

The GatewayClass and the Gateway objects are applied by `pre-install, pre-upgrade` hook Jobs rather than templates, for the reason the Knative gateways are: Helm checks every kind in the manifest against the API server before any hook runs, so on a fresh cluster a template of a kind whose CRD the release's own hooks create would stop the install.
The `kserve-ingress-gateway-apply` Job also removes the objects when `enabled` is turned off, and waits for the controller to take the Envoy proxies down before Helm removes the subchart.

With `kserveStandardMode` on, the chart sets `enableGatewayApi` in KServe's `inferenceservice-config`, and the KServe controller restarts, without restarting any deployment pod.
From then on Standard-mode InferenceServices get HTTPRoutes on the Gateway instead of Istio-class Ingresses.
The Hopsworks backend creates the routes and policies it owns for each deployment, the `/v1/<project>/<deployment>` path route and the idle scale-to-zero route, and deletes the deployment's Istio Ingress only once they are accepted, so both paths serve the same pods during the switch and no request fails.

Standard-mode traffic that comes through Istio is checked by `model-serving-authenticator` twice, by Istio and by the Gateway's policy, with the same result.
Knative traffic is checked once, by Istio, as before.

## Images { #envoy-gateway-images }

- `docker.hops.works/docker.io/envoyproxy/gateway`: the controller, which also runs the certificate generation Job and the shutdown manager sidecar of each proxy.
- `docker.hops.works/docker.io/envoyproxy/envoy`: the data plane.
- `docker.hops.works/hopsworks/envoy-gateway-crds`: the CRDs, read by the hook.

The two `envoyproxy` images are mirrors at the upstream path under the registry root, like the `kube-rbac-proxy` image, not under the `hopsworks` project.
An airgapped install overrides them under `hw-envoy-gateway.controller.image`, `hw-envoy-gateway.envoyProxy.image` and `hw-envoy-gateway.crdImage`, as the chart's `values.airgap.yaml` shows.
The data plane image and the pull secrets reach the Envoy proxies through the controller's configuration, so the same override covers the proxies the controller deploys.

## CustomResourceDefinitions { #envoy-gateway-crds }

The CRDs do not ship in the chart.
They are 3.8 MB together, and Helm stores a release's chart files in a Secret capped at 1 MiB, which installing the upstream CRD chart as a release of its own already exceeds.
A `pre-install, pre-upgrade` hook Job applies them server-side from the `envoy-gateway-crds` image, the way the Istio CRDs come from the `istioctl` image.

The Gateway API CRDs are cluster-wide and may belong to someone else, so the Job applies its bundle only where there is none, or where it applied it itself.
It keeps an experimental or newer bundle of another owner as it is, and fails the install or upgrade on an older bundle of another owner, which only that owner can upgrade.
Read what is on the cluster with:

```bash
kubectl get crd gateways.gateway.networking.k8s.io -o jsonpath='{.metadata.annotations}'
```

On OpenShift 4.19 and later, and on GKE, the platform owns the Gateway API CRDs.
`values.openshift.yaml` sets `hw-envoy-gateway.gatewayApiCrds.enabled: false`, so the Job applies the Envoy Gateway set only and checks that the kinds it needs exist; set the same value on GKE.
Installing with the feature on is verified on OKD 4.21, against the Gateway API CRDs the platform ships.

## Cluster requirements { #envoy-gateway-requirements }

- **Namespaces that may attach routes.**
  The Gateway admits routes only from namespaces labelled `serving.hops.works/gateway-routes=<release namespace>`: the project namespaces, for KServe's host routes, and the release namespace, for the backend's path and idle routes.
  The apply hook labels the release namespace on each install and upgrade, and the backend labels each project namespace before it moves a deployment of that project to the Gateway.
  An HTTPRoute anywhere else, another Hopsworks release's included, cannot claim a deployment's host or path, or see its callers' keys.
  Each release's Envoy Gateway controller manages only its own GatewayClass, by a controller name that carries the release namespace (`gateway.envoyproxy.io/hopsworks-<release namespace>`).
- **Backend permissions with `rbac.useExistingRole`.**
  The chart then renders no backend role.
  Add to the existing one `get, list, watch, create, update, patch, delete` on `httproutes` and `referencegrants` of `gateway.networking.k8s.io` and on `securitypolicies` of `gateway.envoyproxy.io`, and `get, list, watch` on `gateways`.
  The backend also labels the namespaces it routes, which needs `get` and `patch` on `namespaces`, and checks the Gateway Service's endpoints, which needs `get` and `list` on `endpointslices` of `discovery.k8s.io` (the default role has it through `rbac.extraRoleRules`).
  With the feature off the backend runs without these grants, also on a cluster that carries the Gateway API CRDs.
- **The Gateway Service.**
  It is `ClusterIP` by default, and Istio forwards to it.
  `kserve.envoyGateway.service.type: NodePort`, with ports under `kserve.envoyGateway.service.nodePorts` distinct from Istio's, or `LoadBalancer`, exposes it directly next to Istio.
  That is where the path-based routes and their policies are reached from outside, and the end state once Istio is deprecated.
  It is not supported yet on AWS with unmanaged load balancers, because the chart has no target-group binding for it.
- **`model-serving-authenticator` 5.3 or later.**
  The path-based routes of a directly exposed Gateway authorize on its second listener, Service port 81, where the deployment comes from a path the policy sets rather than from the client's Host.
- **OpenShift.**
  The Envoy Gateway pods run with the platform-assigned user and group ids, and `values.openshift.yaml` removes the fixed ids the upstream chart sets.

## Uninstalling { #envoy-gateway-uninstall }

A `post-delete` hook removes the Envoy proxies the controller created, the Gateway objects the hooks and the backend wrote (routes, policies, the per-project ReferenceGrants and the namespace labels), releases the GatewayClass and deletes the certificate Secrets.
The CRDs stay unless `hw-envoy-gateway.cleanupOnUninstall.deleteCrds` is set, because the Gateway API ones may be in use by something else on the cluster.

With the feature turned off before the uninstall, the subchart and its cleanup are no longer part of the release, and the uninstall leaves the GatewayClass, the CRDs and the certificate Secrets behind, as described under [Envoy Gateway][upgrade-envoy-gateway] in the upgrade guide.

Roll the feature back with `helm upgrade`, never `helm rollback`.
The objects are written and removed by `pre-install` and `pre-upgrade` hooks, which a rollback does not run; the upgrade guide lists what to remove by hand if it happened.
