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
- In the `hw-envoy-gateway` subchart, a Redis for the rate limiter, which runs Superset's Redis image, and Envoy Gateway's rate-limit service (`envoyproxy/ratelimit`), which Envoy Gateway deploys from its own configuration and which keeps its counters in that Redis.
  Redis keeps no data on disk, and every counter key expires, as described under [Rate limits and token quotas][agent-router-rate-limits].
- In the `kserve` subchart, the trace collector `agent-router-otlp`, a Deployment and Service on port 4318 that stores the spans of the ext_proc sidecar in the table `agent_router.spans`, and a Job that creates that table, as described under [Tracing][agent-router-tracing].
  The Grafana datasource `agent-router-traces` and the dashboard Agent Router traces in the AgentRouter folder are provisioned with them.
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

## Identity headers { #agent-router-identity }

For a request that passes the check, `model-serving-authenticator` returns three headers that Envoy adds to the request: `x-hopsworks-user`, the username, `x-hopsworks-project`, the project's namespace, and `x-hopsworks-project-id`, its numeric id.
Members and external users get all three.
The rate limits, the traces, the access logs and the usage metrics are keyed on them.
Clients cannot set them: the AI Gateway's ClientTrafficPolicy removes them from the incoming request before the check runs, so a client that sends them has them dropped, and only the authenticator's values reach the backend.
The id comes from the label `serving.hops.works/project-id` of the ConfigMap `<namespace>-project-teams`, which the Hopsworks backend writes when it creates the ConfigMap and on every rebuild of a project's routes.
When the label is missing, the id header is empty, the authenticator logs a warning and the request is still allowed, so the request is still limited, because the per-user rule keys on `x-hopsworks-user`, the per-deployment rule on the model and the project rule is per project.
What is lost is that request's span, which the collector drops without a project id, and its access-log line, which Logstash routes only for a numeric id, until the next rebuild writes the label.

## Rate limits and token quotas { #agent-router-rate-limits }

Administrators limit the project endpoint at three scopes:

- `PROJECT`: all requests to the project's endpoint share one bucket.
- `USER`: each user has a bucket of their own, keyed on `x-hopsworks-user`.
- `DEPLOYMENT`: each deployment has a bucket of its own, keyed on the request's `model`.

Each scope takes a limit on `TOKENS`, the input and output tokens of a request together, or on `REQUESTS`, with a unit of `MINUTE`, `HOUR` or `DAY`.
A rule is shared by every route of a project, so a project with several routes still has one bucket per rule.
Limits are admin-only, because they cap what a project can spend on shared GPUs and a project owner could otherwise lift their own cap.

There are two places to set them:

- The cluster default is the Hopsworks variable `project_endpoint_rate_limits`, a comma-separated list of `SCOPE:KIND=VALUE/UNIT`, for example `PROJECT:TOKENS=1000000/HOUR,USER:REQUESTS=60/MINUTE`.
  When it is empty or unset, there are no limits.
  The variable is seeded empty, and an upgrade keeps the value an administrator set.
  An administrator edits it in the admin UI under Settings, Quotas & rate limits, in the Project endpoint section.
  A change reaches the existing projects at the backend's next full pass, about 10 minutes later.
- An override per project is set on the admin page that edits the project, under Project endpoint limits, with the same scopes, kinds and units, and applies immediately.
  A value is from 1 to 4294967295, because Envoy Gateway holds a rate-limit value as an unsigned 32-bit integer and cannot express a larger one, and `-1` makes the scope unlimited for that project.
  Removing the override makes the cluster default apply again.
  The same limits are available as `projectEndpointLimits` of `projectQuotas` in `PUT /admin/projects/{id}`, and `GET /admin/projects/{id}?expand=quotas` returns the effective ones with a `source` of `DEFAULT` or `PROJECT`.

The backend turns the effective limits into one BackendTrafficPolicy per project, `<namespace>-aiproject-ratelimit`, in the release namespace, and updates it when a limit or a deployment changes, with no restart.
Project members see the limits of their project, read-only, in the quotas of the project settings and on the Project endpoint card.

A request over a limit gets `429` with the `x-ratelimit-*` headers.
A token limit charges the request after the response: the sidecar reads the token counts from the response, and Envoy subtracts them from the bucket then.
A stream that is running is therefore never cut when it crosses the limit, and the next request gets the `429`.
For the same reason, a request is refused only after the bucket has already gone empty, so a single request can overshoot the limit.

The rate limiter fails open.
When Redis or the rate-limit service is down, requests are let through, because a rate limiter that is down must not take down model serving.
The counters live in Redis memory only, so they reset when the Redis pod restarts, and the limits are not exact across that restart.

## Tracing { #agent-router-tracing }

The ext_proc sidecar writes an OpenTelemetry span for every request.
The Agent Router controller, with the arguments under `hw-envoy-gateway.aiGateway.requestHeaderAttributes.span` and `.metrics`, adds `hopsworks.user`, `hopsworks.project.id` and `session.id`, from `x-hopsworks-user`, `x-hopsworks-project-id` and `agent-session-id`, to every span, and the sidecar sends them over OTLP/HTTP to the collector `agent-router-otlp`.
The collector writes them to the table `agent_router.spans` in RonDB, through the `hopsworksroot` credential from the Secret `mysql-users-secrets`.
It drops a span that has no `hopsworks.project.id`, and counts the drops in its log, because a span of no project cannot be shown to anyone.

Two values control it:

- `hopsworks.agentRouter.tracing.ttlSeconds`, 604800 (seven days) by default, is the age after which RonDB's native TTL deletes a span row, from the column `created_at`.
  The table is created by a Job when `aiGateway.enabled` is on, and the Job runs again when the value changes, with `ALTER TABLE ... ALGORITHM=INPLACE`.
  The collector and the table Job are sized under `hopsworks.agentRouter.tracing.collector` and `.tableJob`.
- `kserve.envoyGateway.aiGateway.tracing.captureContent`, `false` by default, decides whether prompts and responses are stored.
  While it is false, the sidecar gets `OPENINFERENCE_HIDE_INPUTS`, `OPENINFERENCE_HIDE_OUTPUTS` and `OPENINFERENCE_HIDE_EMBEDDINGS_TEXT` set to `true`, so the message contents, the output text and the embedding inputs are left out of the spans, and the `messages` column is empty.
  Model name, token counts, status, timing, user and session stay, because they are what usage and debugging need.
  Prompts carry user data, so turn it on only when the users of the cluster have agreed to the retention.

Two audiences read the table:

- Administrators, in Grafana: the MySQL datasource `agent-router-traces` and the dashboard Agent Router traces, in the AgentRouter folder, list the spans of every project, filtered by project, deployment, user and time.
  The Hopsworks Grafana proxy refuses these queries to anyone who is not an administrator, because the table holds every project's spans.
- Project members with the role Data Owner or Data Scientist, in Project settings, Agent Router traces, which shows only their project's traces, with a filter on the deployment.
  The backend adds the project's id to every query, so a member cannot read another project's spans.

Turning the feature off leaves the table `agent_router.spans` and its rows in RonDB, where the TTL keeps deleting them.
Drop `agent_router.spans` by hand when it is no longer wanted.

## Access logs { #agent-router-access-logs }

The AI Gateway's Envoy writes one JSON line per request to its standard output, without bodies and without the `authorization` header.
The fields are `log_type` (`agent_router_access`), `start_time`, `method`, `path`, `status`, `duration_ms`, `response_flags`, `request_id`, `traceparent`, `project_id`, `project`, `user`, `model`, `backend`, `input_tokens`, `output_tokens`, `total_tokens` and `upstream_host`.
Filebeat collects them with the other pods of the release namespace, and Logstash writes the lines that carry a `project_id` to the index `agentrouter_<project id>-YYYY.MM.dd`, and drops the others.
Members of a project with the role Data Owner or Data Scientist read their project's indices, `agentrouter_<project id>-*`, in OpenSearch Dashboards, which is created as an index pattern with the project.
The service log viewer role reads all of them.
The `OpenSearchCleaner` deletes an index older than `elastic_logs_index_expiration`, the setting that applies to the project's other logs.

## Usage attribution { #agent-router-usage }

The `gen_ai_*` metrics of the sidecar carry the label `hopsworks_user`, taken from `x-hopsworks-user`, next to the model and the backend.
The number of values is bounded by the number of project members.
The Agent Router dashboard has a `user` variable and panels for tokens and requests per user, and a table of usage by project, user and model over the dashboard's time range, which serves as the basis for charging usage back.
The access logs carry the same user, model and token counts per request, for audits.

## Limitations { #agent-router-limitations }

- Knative-mode LLM deployments and Standard-mode ones that scale to zero through the KEDA interceptor are not served by the project endpoint, because the interceptor does not wake a deployment reached this way.
  They stay on their per-deployment path, and the backend says so in the deployment's status note.
- Any member of the project can reach every one of its deployments through the endpoint, unless a Data Owner turns the endpoint off for the project or for a deployment, as described under [Access to the project endpoint][agent-router-access].
- External providers, MCP and `InferencePool` backends are not part of it.
- The span table relies on RonDB's native TTL, which deletes rows by the age of `created_at`, and it has `TEXT` columns for messages, attributes and events, so the rows of one span can be large when `captureContent` is on, and a shorter `ttlSeconds` bounds the table's size.
- Enabling the feature, or changing `captureContent` or the tracing endpoint, changes the GatewayConfig environment, which rolls the AI Gateway's Envoy pods once, for the reason given under [What the chart installs][agent-router-components].
- OpenShift: `values.openshift.yaml` leaves both values off, like Envoy Gateway itself.
- The controller logs `Failed to add finalizer to object` once per ReferenceGrant it sees, the per-project grants of the Hopsworks Gateway included.
  The chart's Role refuses that write on purpose: a finalizer of the controller on those grants would block their deletion once the controller is gone, and the AI routes and backends never cross a namespace, so the controller needs nothing from the grants.

## Images { #agent-router-images }

- `docker.hops.works/envoyproxy/ai-gateway-controller`: the controller.
- `docker.hops.works/envoyproxy/ai-gateway-extproc`: the ext_proc sidecar.
  It runs in no pod until the first route exists, and is named by the controller's `--extProcImage` argument.
- `docker.hops.works/envoyproxy/ratelimit`: Envoy Gateway's rate-limit service.
- `docker.hops.works/hopsworks/envoy-ai-gateway-crds`: the CRDs, read by the hook.

Like the Envoy Gateway images, the three `envoyproxy` images are mirrors of the Docker Hub images at the same path, and the CRD image is a Hopsworks image under the `hopsworks` project.
The Redis of the rate limiter uses Superset's Redis image, and the trace collector uses the `otlp-sidecar` image of the agent sidecar, so an airgapped cluster that mirrors those already has them.
An airgapped install overrides the four images above, as the chart's `values.airgap.yaml` shows.

## Cluster requirements { #agent-router-requirements }

- Envoy Gateway, enabled already or in the same upgrade, as described in [Envoy Gateway][envoy-gateway].
- cert-manager, because the controller's webhook certificate is a cert-manager Certificate.
  The `kserve` subchart installs cert-manager unless the platform brings its own.
- With `rbac.useExistingRole`, the chart renders no backend role.
  Add to the existing one `get, list, watch, create, update, patch, delete` on `aigatewayroutes` and `aiservicebackends` of `aigateway.envoyproxy.io` and on `backends` and `backendtrafficpolicies` of `gateway.envoyproxy.io`, on top of the Envoy Gateway permissions listed under [Cluster requirements][envoy-gateway-requirements].

## Turning it on { #agent-router-enable }

An upgrade that leaves `aiGateway` alone changes nothing: the Istio Lua filter is the same, no object is added, and the backend finds no `envoy-ai-gateway-config` ConfigMap and does nothing.

Before enabling:

1. List the deployments with a [reserved name][agent-router-reserved-names] and recreate them under another name first: `kubectl get isvc -A --field-selector metadata.name=v1`, and `kubectl get isvc -A --no-headers -o custom-columns=NS:.metadata.namespace,NAME:.metadata.name | grep aiproject`.
2. Check the [cluster requirements][agent-router-requirements]: Envoy Gateway, cert-manager, the backend role.
3. On an airgapped cluster, mirror the four [images][agent-router-images].
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
