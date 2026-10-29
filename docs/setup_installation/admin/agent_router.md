---
description: How the Hopsworks Helm chart installs Agent Router on top of Envoy Gateway to give every project one OpenAI-compatible endpoint, which deployments it serves, its images on an airgapped cluster, and how it is turned on and off
---

# Agent Router { #agent-router }

## Introduction

Agent Router, the renamed Envoy AI Gateway, runs on top of [Envoy Gateway][envoy-gateway] and gives every project one OpenAI-compatible endpoint, on the same inference endpoint as the deployments:

```text
<inference endpoint>/v1/<project>/v1/chat/completions
<inference endpoint>/v1/<project>/v1/completions
<inference endpoint>/v1/<project>/v1/embeddings
<inference endpoint>/v1/<project>/v1/models
```

`<project>` is the project's namespace, and the project name works wherever it works for deployments today.
The request's `model` field selects the project's Standard-mode vLLM deployment with that served name, the deployment name, and `GET .../v1/models` lists the project's started LLM deployments.
The list can trail the routes by up to about a minute after a deployment starts or stops, since the Agent Router reads it from a mounted Secret that the kubelet refreshes on its own schedule.
The Hopsworks backend creates and removes the AIGatewayRoutes, AIServiceBackends and Backends with the deployment lifecycle.
The per-deployment paths, `/v1/<project>/<deployment>/v1/...`, keep working.

The feature is new in 5.3 and off by default, and one value on top of the Envoy Gateway ones turns it on:

```yaml
global:
  _hopsworks:
    envoyGateway:
      enabled: true
      aiGateway:
        enabled: true
```

`enabled` installs the CRDs, the controller and the AI Gateway, publishes the project endpoint, and rendering fails when it is on without `envoyGateway.enabled`.
The values are listed in [Envoy Gateway values][helm-values-hw-envoy-gateway] and under `kserve.envoyGateway.aiGateway` in [KServe values][helm-values-kserve].

## What the chart installs { #agent-router-components }

- In the `hw-envoy-gateway` subchart, the Agent Router controller, with templates vendored from the upstream `ai-gateway-helm` chart 1.2, its mutating webhook with a cert-manager Certificate, and the Envoy Gateway configuration that lets Envoy Gateway call the controller (`extensionManager` with `failOpen: true`, and `extensionApis.enableBackend`).
- In the `kserve` subchart, a dedicated AI Gateway, `kserve-ai-gateway` (`aiGateway.gatewayName`): its own Gateway on the same GatewayClass, an EnvoyProxy with a `ClusterIP` Service, a GatewayConfig that sizes the ext_proc sidecar, a SecurityPolicy that checks every request with `model-serving-authenticator`, a BackendTrafficPolicy with no request timeout and a ClientTrafficPolicy with a 50Mi connection buffer (`kserve.envoyGateway.aiGateway.bufferLimit`).
- The ConfigMap `envoy-ai-gateway-config`, which the backend and `model-serving-authenticator` read to learn the Gateway and whether the project endpoint is published.
  The ConfigMap is absent, and both do nothing, while `enabled` is false.
- Prometheus scraping of the controller (port 8080) and of the ext_proc sidecar (port 1064, through the Service `kserve-ai-gateway-extproc-metrics`).
  The sidecar's metrics follow the OpenTelemetry generative AI conventions, for example `gen_ai_client_token_usage` and `gen_ai_server_request_duration_seconds`, labelled with the model and the backend, `<Hopsworks namespace>/<project namespace>-<deployment>-aibackend`.
  Prometheus sets their `namespace` label to the project's namespace, so token usage can be summed per project and per deployment, and a user who is not an administrator sees in Grafana only the projects they are a member of.
  Grafana shows them in the ModelServing folder: the dashboard Agent Router (Project Endpoints) has tokens, requests, errors and latency per project and deployment, or across all projects, and the vLLM Deployment Metrics dashboard has a Project endpoint row for each deployment.
- A branch in the Istio Lua filter that rewrites `/v1/<project>/v1/<rest>` to the host `v1.<namespace>.<domain>` and the path `/v1/<rest>`, and a first route in the Istio forward VirtualService that sends that host to the AI Gateway.
  With `enabled` off, the Lua filter is the one of a chart without the feature, so an existing deployment named `v1` keeps its path.
- The six CustomResourceDefinitions (CRDs) of Agent Router, 2 MB together, shipped in the `envoy-ai-gateway-crds` image and applied by a second `pre-install, pre-upgrade` hook Job, `envoy-ai-gateway-crd-install`, for the reason the Envoy Gateway ones are, as described in [CustomResourceDefinitions][envoy-gateway-crds].

The AI Gateway is separate from `kserve-ingress-gateway` on purpose.
The controller injects the ext_proc sidecar into the Envoy pods of the Gateway that carries AI routes, and rolls them when the first route attaches, when the last one goes and whenever the sidecar's image, resources or GatewayConfig change.
Starting or stopping an LLM deployment while another one is running rolls nothing.
Only the AI Gateway's Envoy pods roll: the Hopsworks Gateway, Knative and the predictive routes are not touched, and the controller's webhook (`failurePolicy: Fail`) selects the AI Gateway's pods in the release namespace only, so a controller that is down blocks no other pod.

The AI Gateway admits routes from the release namespace only, and every AI object lives there.
The filter chain runs `ext_authz` before the ext_proc, so `GET /v1/models` needs a valid key as well.

## Access to the project endpoint { #agent-router-access }

Two switches control what the project endpoint serves, and both are on by default:

- The project switch turns the endpoint off for a whole project, so it answers `404` there.
- The deployment switch keeps one LLM deployment off the endpoint while the others stay on it.
  The deployment is still reachable on its per-deployment path.

Only Data Owners of the project change either switch, and a change takes effect without restarting a deployment: the backend adds or removes the project's routes.

Project members with an allowed role can use the endpoint.
A deployment's External access groups, described in [External access][serving-external-access], also grant its use through the project endpoint, by model name: an external user whose groups are listed for a deployment can send requests with that deployment as the `model`, and no others.
External users cannot list the project's models, so `GET .../v1/models` is refused for them.
The check is made by `model-serving-authenticator` on the request body, which the AI Gateway sends to it up to the AI Gateway's 50Mi buffer limit (`kserve.envoyGateway.aiGateway.bufferLimit`).

## Reserved deployment names { #agent-router-reserved-names }

From 5.3, `v1` is a reserved deployment name, and so is any name containing `aiproject`, the infix of the project endpoint's gateway objects, whether or not the project endpoint is on.
The backend refuses to create a deployment with such a name.
An existing deployment with such a name stays editable and restartable, and while `aiGateway.enabled` is off it works as before.
With the project endpoint on, the backend leaves the project route out of a project that has one, saying so in its deployments' status notes, and a deployment named `v1` stops answering on its per-deployment path, because the Istio rewrite sends `/v1/<project>/v1/...` to the AI Gateway and `model-serving-authenticator` then checks `v1` as the project endpoint.
Recreate it under another name before enabling the feature.

## Limitations { #agent-router-limitations }

- Knative-mode LLM deployments and Standard-mode ones that scale to zero through the KEDA interceptor are not served by the project endpoint, because the interceptor does not wake a deployment reached this way.
  They stay on their per-deployment path, and the backend says so in the deployment's status note.
- Any member of the project can reach every one of its deployments through the endpoint, unless a Data Owner turns the endpoint off for the project or for a deployment, as described under [Access to the project endpoint][agent-router-access].
- Token limits, external providers, MCP and `InferencePool` backends are not part of it.
- OpenShift: `values.openshift.yaml` leaves both values off, like Envoy Gateway itself.
- The controller logs `Failed to add finalizer to object` once per ReferenceGrant it sees, the per-project grants of the Hopsworks Gateway included.
  The chart's Role refuses that write on purpose: a finalizer of the controller on those grants would block their deletion once the controller is gone, and the AI routes and backends never cross a namespace, so the controller needs nothing from the grants.

## Images { #agent-router-images }

- `docker.hops.works/envoyproxy/ai-gateway-controller`: the controller.
- `docker.hops.works/envoyproxy/ai-gateway-extproc`: the ext_proc sidecar.
  It runs in no pod until the first route exists, and is named by the controller's `--extProcImage` argument.
- `docker.hops.works/hopsworks/envoy-ai-gateway-crds`: the CRDs, read by the hook.

Like the Envoy Gateway images, the two `envoyproxy` images are mirrors of the Docker Hub images at the same path, and the CRD image is a Hopsworks image under the `hopsworks` project.
An airgapped install overrides all three, as the chart's `values.airgap.yaml` shows.

## Cluster requirements { #agent-router-requirements }

- Envoy Gateway, enabled already or in the same upgrade, as described in [Envoy Gateway][envoy-gateway].
- cert-manager, because the controller's webhook certificate is a cert-manager Certificate.
  The `kserve` subchart installs cert-manager unless the platform brings its own.
- With `rbac.useExistingRole`, the chart renders no backend role.
  Add to the existing one `get, list, watch, create, update, patch, delete` on `aigatewayroutes` and `aiservicebackends` of `aigateway.envoyproxy.io` and on `backends` of `gateway.envoyproxy.io`, on top of the Envoy Gateway permissions listed under [Cluster requirements][envoy-gateway-requirements].

## Turning it on { #agent-router-enable }

An upgrade that leaves `aiGateway` alone changes nothing: the Istio Lua filter is the same, no object is added, and the backend finds no `envoy-ai-gateway-config` ConfigMap and does nothing.

Before enabling:

1. List the deployments with a [reserved name][agent-router-reserved-names] and recreate them under another name first: `kubectl get isvc -A --field-selector metadata.name=v1`, and `kubectl get isvc -A --no-headers -o custom-columns=NS:.metadata.namespace,NAME:.metadata.name | grep aiproject`.
2. Check the [cluster requirements][agent-router-requirements]: Envoy Gateway, cert-manager, the backend role.
3. On an airgapped cluster, mirror the three [images][agent-router-images].
4. Two more hook Jobs run before the templates: the CRD Job `envoy-ai-gateway-crd-install` and the existing `kserve-ingress-gateway-apply`, which now also applies the AI Gateway; a few seconds each.

Enable with one `helm upgrade` (`aiGateway.enabled: true`).
The CRD Job applies the six CRDs, the controller and the AI Gateway come up, the Envoy Gateway controller restarts once for its new configuration, the Istio Lua filter and the forward rule change without a pod restart, and the backend's next pass creates the backends and routes of the running Standard-mode vLLM deployments.
The AI Gateway's Envoy pods roll once when the first route attaches, and again whenever the last LLM deployment of the cluster stops and another one starts later.
No predictive pod, Knative pod or `kserve-ingress-gateway` pod restarts.
Check that `kubectl get gateway -n <namespace> kserve-ai-gateway` reports `Programmed`, and that `kubectl get aigatewayroutes,aiservicebackends,backends -n <namespace> -l serving.hops.works/gateway-route` lists one route per project with a started LLM deployment.

If the controller goes down while Envoy Gateway runs, `extensionManager.failOpen: true` keeps the predictive routes translating: Envoy Gateway ignores the failed hook and builds its configuration without the controller's changes.
The AI routes depend on those changes, so they can stop answering until the controller is back.
A freshly started Envoy Gateway controller is different: until it has reached the AI Gateway controller once, it sends the Envoys no configuration updates at all, so the proxies keep their last configuration and endpoint changes behind the Gateway (a rolled pod, a scaled deployment) do not reach them.
In a cluster test where `model-serving-authenticator` rolled in that window, the Envoys kept checking requests against the old pod and refused Standard-mode requests for about two minutes, until the AI Gateway controller was back and Envoy Gateway's reconnect backoff had passed, so avoid restarting Envoy Gateway while the AI Gateway controller is down.
The webhook refuses to create new Envoy pods for the AI Gateway only, so a restart of those pods waits for the controller, and nothing else does.

## Turning it off { #agent-router-disable }

Disable in one upgrade with `aiGateway.enabled: false`.
The `kserve-ingress-gateway-apply` hook first deletes the ConfigMap `envoy-ai-gateway-config`, so the backend stops publishing routes and `model-serving-authenticator` reads the project endpoint as off, and removes the project endpoint's forward routes from the Hopsworks Gateway.
It then deletes the AI routes and backends, waits for the controller to remove them, clearing a finalizer that is still there after two minutes, and deletes the Gateway, waiting for its proxies to go, and the subchart removes the controller.
The CRDs stay unless `hw-envoy-gateway.cleanupOnUninstall.deleteCrds` is set.
Requests in flight on the AI Gateway are cut when its Envoy pods terminate, up to the 60 s drain.
An upgrade that fails part way is run again as it was, because every hook step is idempotent.

`aiGateway.enabled: false` leaves the six CRDs, the Gateway API ones, the GatewayClass and the filter-config Secrets the controller wrote in the release namespace, named `kserve-ai-gateway-<namespace>-<hash>` and `...-part-<n>`.
They are inert.
Remove them by hand when no longer wanted; with the feature off the subchart's uninstall cleanup is no longer part of the release, so an uninstall leaves them too.

Roll the feature back with `helm upgrade`, never `helm rollback`, for the reason given under [Envoy Gateway][upgrade-envoy-gateway] in the upgrade guide.
After a `helm rollback` or an `--atomic` failure that first enabled the feature, the AI Gateway objects and the webhook stay behind; upgrade again with the value off, or remove them by hand:

```bash
NS=<namespace>; AIGW=kserve-ai-gateway
kubectl delete -n "$NS" aigatewayroutes.aigateway.envoyproxy.io,aiservicebackends.aigateway.envoyproxy.io,backends.gateway.envoyproxy.io -l serving.hops.works/gateway-route --wait=false
# the controller is gone, so clear the finalizer of what is left
for o in $(kubectl get aigatewayroutes.aigateway.envoyproxy.io,aiservicebackends.aigateway.envoyproxy.io,backends.gateway.envoyproxy.io -n "$NS" -l serving.hops.works/gateway-route -o name); do
  kubectl patch -n "$NS" "$o" --type=merge -p '{"metadata":{"finalizers":null}}'
done
kubectl delete -n "$NS" destinationrule "$AIGW-forward" --ignore-not-found
kubectl delete -n "$NS" gateway "$AIGW" --ignore-not-found
kubectl delete -n "$NS" securitypolicy,backendtrafficpolicy,clienttrafficpolicy,envoyproxy "$AIGW" --ignore-not-found
kubectl delete -n "$NS" gatewayconfigs.aigateway.envoyproxy.io "$AIGW" --ignore-not-found
# the HTTPRouteFilters the controller created, which name an AIGatewayRoute as their owner
for o in $(kubectl get httproutefilters.gateway.envoyproxy.io -n "$NS" -o jsonpath='{range .items[?(@.metadata.ownerReferences[0].kind=="AIGatewayRoute")]}{.metadata.name}{"\n"}{end}'); do kubectl delete -n "$NS" httproutefilters.gateway.envoyproxy.io "$o"; done
kubectl delete mutatingwebhookconfiguration "envoy-ai-gateway-gateway-pod-mutator.$NS" --ignore-not-found
kubectl delete certificates.cert-manager.io -n "$NS" ai-gateway-controller-webhook --ignore-not-found
kubectl delete secret -n "$NS" ai-gateway-controller-webhook-cert --ignore-not-found
```

The CRDs are named in the chart's `charts/hw-envoy-gateway/templates/_helpers.tpl` (`aiGatewayCrds`).
