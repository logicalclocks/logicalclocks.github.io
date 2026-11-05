---
description: How the Hopsworks Helm chart installs Agent Router on top of Envoy Gateway to give every project one OpenAI-compatible endpoint, which deployments it serves, its images on an airgapped cluster, and how it is turned on and off
---

# Agent Router { #agent-router }

## Introduction

Agent Router, the renamed Envoy AI Gateway, runs on top of [Envoy Gateway][envoy-gateway] and gives every project one OpenAI-compatible endpoint, its LLM gateway, on the same inference endpoint as the deployments:

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

`enabled` installs the CRDs, the controller and the AI Gateway, publishes the LLM gateway, and rendering fails when it is on without `envoyGateway.enabled`.
The values are listed in [Envoy Gateway values][helm-values-hw-envoy-gateway] and under `kserve.envoyGateway.aiGateway` in [KServe values][helm-values-kserve].

## What the chart installs { #agent-router-components }

- In the `hw-envoy-gateway` subchart, the Agent Router controller, with templates vendored from the upstream `ai-gateway-helm` chart 1.2, its mutating webhook with a cert-manager Certificate, and the Envoy Gateway configuration that lets Envoy Gateway call the controller (`extensionManager` with `failOpen: true`, and `extensionApis.enableBackend`).
- In the `kserve` subchart, a dedicated AI Gateway, `kserve-ai-gateway` (`aiGateway.gatewayName`): its own Gateway on the same GatewayClass, an EnvoyProxy with a `ClusterIP` Service, a GatewayConfig that sizes the ext_proc sidecar, a SecurityPolicy that checks every request with `model-serving-authenticator`, a BackendTrafficPolicy with no request timeout and a ClientTrafficPolicy with a 50Mi connection buffer (`kserve.envoyGateway.aiGateway.bufferLimit`).
- The ConfigMap `envoy-ai-gateway-config`, which the backend and `model-serving-authenticator` read to learn the Gateway and whether the LLM gateway is published.
  The ConfigMap is absent, and both do nothing, while `enabled` is false.
- Prometheus scraping of the controller (port 8080) and of the ext_proc sidecar (port 1064, through the Service `kserve-ai-gateway-extproc-metrics`).
  The sidecar's metrics follow the OpenTelemetry generative AI conventions, for example `gen_ai_client_token_usage` and `gen_ai_server_request_duration_seconds`, labelled with the model and the backend, `<Hopsworks namespace>/<project namespace>-<deployment>-aibackend`.
  Prometheus sets their `namespace` label to the project's namespace, so token usage can be summed per project and per deployment.
  Grafana shows them in the ModelServing folder: the dashboard LLM Gateway (Agent Router) has tokens, requests, errors and latency per project and deployment, for one project at a time, and the vLLM Deployment Metrics dashboard has an LLM gateway row for each deployment.
- In the `hw-envoy-gateway` subchart, a Redis for the rate limiter, which runs Superset's Redis image, and Envoy Gateway's rate-limit service (`envoyproxy/ratelimit`), which Envoy Gateway deploys from its own configuration and which keeps its counters in that Redis.
  Redis keeps no data on disk, and every counter key expires, as described under [Rate limits and token quotas][agent-router-rate-limits].
  A NetworkPolicy lets only the rate-limit service connect to Redis.
- In the `hopsworks` chart, the trace collector `agent-router-otlp`, a Deployment and Service on port 4318 that stores the spans of the ext_proc sidecar in the table `agent__router.spans`, and a Job that creates that table, as described under [Tracing][agent-router-tracing].
  A NetworkPolicy lets only the AI Gateway's Envoy pods send to it.
- A branch in the Istio Lua filter that rewrites `/v1/<project>/v1/<rest>` to the host `v1.<namespace>.<domain>` and the path `/v1/<rest>`, and a first route in the Istio forward VirtualService that sends that host to the AI Gateway.
  With `enabled` off, the Lua filter is the one of a chart without the feature, so an existing deployment named `v1` keeps its path.
- The six CustomResourceDefinitions (CRDs) of Agent Router, 2 MB together, shipped in the `envoy-ai-gateway-crds` image and applied by a second `pre-install, pre-upgrade` hook Job, `envoy-ai-gateway-crd-install`, for the reason the Envoy Gateway ones are, as described in [CustomResourceDefinitions][envoy-gateway-crds].

The AI Gateway is separate from `kserve-ingress-gateway` on purpose.
The controller injects the ext_proc sidecar into the Envoy pods of the Gateway that carries AI routes, and rolls them when the first route attaches, when the last one goes and whenever the sidecar's image, resources or GatewayConfig change.
Starting or stopping an LLM deployment while another one is running rolls nothing.
Only the AI Gateway's Envoy pods roll: the Hopsworks Gateway, Knative and the predictive routes are not touched, and the controller's webhook (`failurePolicy: Fail`) selects the AI Gateway's pods in the release namespace only, so a controller that is down blocks no other pod.

The AI Gateway admits routes from the release namespace only, and every AI object lives there.
The filter chain runs `ext_authz` before the ext_proc, so `GET /v1/models` needs a valid key as well.

## Access to the LLM gateway { #agent-router-access }

Two switches control what the LLM gateway serves, and both are on by default:

- The project switch turns the LLM gateway off for a whole project, so it answers `404` there.
- The deployment switch keeps one LLM deployment off the endpoint while the others stay on it.
  The deployment is still reachable on its per-deployment path.

Only Data Owners of the project change either switch, and a change takes effect without restarting a deployment: the backend adds or removes the project's routes.

Project members with an allowed role can use the LLM gateway.
A deployment's External access groups, described in [External access][serving-external-access], also grant its use through the LLM gateway, by model name: an external user whose groups are listed for a deployment can send requests with that deployment as the `model`, and no others.
External users can call these operations only: chat completions (`/v1/chat/completions`), completions (`/v1/completions`), embeddings (`/v1/embeddings`), responses (`/v1/responses`) and Anthropic messages (`/anthropic/v1/messages`).
Every listing, `GET .../v1/models` under any prefix, and every other path are refused for them with `403`.
The check is made by `model-serving-authenticator` on the request body, which the AI Gateway sends to it up to the AI Gateway's 50Mi buffer limit (`kserve.envoyGateway.aiGateway.bufferLimit`).

## Reserved deployment names { #agent-router-reserved-names }

From 5.3, `v1` is a reserved deployment name, whether or not the LLM gateway is on.
The backend refuses to create a deployment with such a name.
An existing deployment with such a name stays editable and restartable, and while `aiGateway.enabled` is off it works as before.
Only a started deployment with such a name matters once the LLM gateway is on: a stopped one does not block anything.
While one is started, the backend leaves the project route out of that project, saying so in its deployments' status notes and in the LLM gateway card of the project settings.
A deployment named `v1` is not served by the LLM gateway.
Through the Istio ingress it answers `404` on both its path and its host, since the AI Gateway takes `/v1/<project>/v1/` and `v1.<namespace>.<domain>` for every project.
It keeps its routes on the Envoy Gateway, and answers there.
Stop the deployment or recreate it under another name to have the LLM gateway in that project.
Starting it again later has the same effect.

## Identity headers { #agent-router-identity }

For a request that passes the check, `model-serving-authenticator` returns three headers that Envoy adds to the request: `x-hopsworks-user`, the username, `x-hopsworks-project`, the project's namespace, and `x-hopsworks-project-id`, its numeric id.
Members and external users get all three.
The rate limits, the traces, the access logs and the usage metrics are keyed on them.
Clients cannot set them: the AI Gateway's ClientTrafficPolicy removes them from the incoming request before the check runs, so a client that sends them has them dropped, and only the authenticator's values reach the backend.
The id comes from the label `serving.hops.works/project-id` of the ConfigMap `<namespace>-project-teams`, which the Hopsworks backend writes when it creates the ConfigMap and on every rebuild of a project's routes.
When the label is missing, the id header is empty, the authenticator logs a warning and the request is still allowed, so the request is still limited, because the per-user rule keys on `x-hopsworks-user`, the per-deployment rule on the model and the project rule is per project.
What is lost is that request's span, which the collector drops without a project id, and its access-log line, which Logstash routes only for a numeric id, until the next rebuild writes the label.

## Rate limits and token quotas { #agent-router-rate-limits }

Administrators limit the LLM gateway at three scopes:

- `PROJECT`: all requests to the project's endpoint share one bucket.
- `USER`: each user has a bucket of their own, keyed on `x-hopsworks-user`.
- `DEPLOYMENT`: each deployment has a bucket of its own, keyed on the request's `model`.

Each scope takes a limit on `TOKENS`, the input and output tokens of a request together, or on `REQUESTS`, with a unit of `MINUTE`, `HOUR` or `DAY`.
A rule is shared by every route of a project, so a project with several routes still has one bucket per rule.
Limits are admin-only, because they cap what a project can spend on shared GPUs and a project owner could otherwise lift their own cap.

There are two places to set them:

- The cluster default of each scope and kind is a Hopsworks variable holding `VALUE/UNIT`, for example `1000000/HOUR`.
  The value is from 1 to 4294967295, like an override below, and an empty, unset or `-1` value means no limit for that scope and kind.

    | Variable | Limits |
    | --- | --- |
    | `llm_gateway_project_token_limit` | `PROJECT` `TOKENS` |
    | `llm_gateway_project_request_limit` | `PROJECT` `REQUESTS` |
    | `llm_gateway_user_token_limit` | `USER` `TOKENS` |
    | `llm_gateway_user_request_limit` | `USER` `REQUESTS` |
    | `llm_gateway_deployment_token_limit` | `DEPLOYMENT` `TOKENS` |
    | `llm_gateway_deployment_request_limit` | `DEPLOYMENT` `REQUESTS` |

  The variables are seeded empty, and an upgrade keeps the values an administrator set.
  Saving a value that does not parse is refused with `422`.
  An administrator edits them in the cluster settings, on the Quotas and Rate Limits page, in the LLM gateway section.
  A change reaches the existing projects at the backend's next full pass, about 10 minutes later.
- An override per project is set on the admin page that edits the project, under LLM gateway limits, with the same scopes, kinds and units, and applies immediately.
  A value is from 1 to 4294967295, because Envoy Gateway holds a rate-limit value as an unsigned 32-bit integer and cannot express a larger one, and `-1` makes the scope unlimited for that project.
  Removing the override makes the cluster default apply again.
  The same limits are available as `llmGatewayLimits` of `projectQuotas` in `PUT /admin/projects/{id}`, and `GET /admin/projects/{id}?expand=quotas` returns the effective ones with a `source` of `DEFAULT` or `PROJECT`.

The backend turns the effective limits into one BackendTrafficPolicy per project, `<namespace>-llmratelimit`, in the release namespace, and updates it when a limit or a deployment changes, with no restart.
Project members see the limits of their project, read-only, in the quotas of the project settings and on the LLM gateway card.

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
The collector writes them to the table `agent__router.spans` in RonDB, through the `hopsworksroot` credential from the Secret `mysql-users-secrets`.
It drops a span that has no `hopsworks.project.id`, and counts the drops in its log, because a span of no project cannot be shown to anyone.
The columns `messages`, `attributes` and `events` are `MEDIUMTEXT`.
The collector caps each of them at `OTEL_MAX_TEXT_BYTES` of UTF-8, 262144 by default, by dropping or shortening JSON elements so the value stays valid JSON, and adds the attribute `hopsworks.truncated: true` to `attributes` when it clipped anything.
Both trace pages mark such a span as truncated, and also a span whose column does not parse.

The table is in the online feature store's disk tablespace, `featurestore_online_tablespace` or else the cluster's NDB tablespace, `ts_1`, which feature groups with disk columns and the traces of model deployments share.
Every span stays for the whole TTL, so keeping most of it on disk keeps the table's share of RonDB DataMemory, which every online feature group needs, small.
The keys, the indexed columns, `created_at` and the columns the trace pages filter on (`deployment`, `username`, `session_id` and `parent_span_id`) stay in memory, because RonDB keeps keys and indexed columns there and requires the TTL column there.
The other columns, `messages`, `attributes` and `events` included, are on disk, apart from the first 256 bytes of each text column and a small key for each part of the text beyond them, which RonDB keeps in memory.
On a cluster without a tablespace, the Job creates the table in memory and logs a warning.
The Job fails when `featurestore_online_tablespace` names a tablespace that does not exist, or a name with characters other than letters, digits and underscores.
The Job never drops or moves an existing table: changing the tablespace, or adding one after the table was created in memory, leaves the table where it is, with a warning in the Job's log, until it is dropped by hand.

The chart creates `ts_1` at install with the size of the disk-column volume, `rondb.rondb.resources.requests.storage.diskColumnGiB` (2 GiB by default), or `InitialTablespaceSizeGiB` when that is set.
Size it for the spans one TTL keeps, next to what feature groups and deployment traces store there.
On an installed cluster, a larger volume does not grow the tablespace: add a data file with `ALTER TABLESPACE ... ADD DATAFILE`.
When the tablespace has no free extent left, inserts that need new space fail, and the collector logs the failure and drops those spans, which adding space later does not bring back.
Spans the TTL purge has deleted free space for later spans in the same table, not in the tablespace.
The purge runs in the RonDB REST API servers, and `rondb.rondb.rdrs.ttlPurge` controls it.
The `LowDiskDataFileExtents` alert fires when less than 20% of `ts_1` is free for 5 minutes; it does not watch another tablespace named in `featurestore_online_tablespace`.

Two values control it:

- `hopsworks.agentRouter.tracing.ttlSeconds`, 604800 (seven days) by default, is the age after which RonDB's native TTL deletes a span row, from the column `created_at`.
  The table is created by a Job when `aiGateway.enabled` is on, and the Job runs again when the value changes, with `ALTER TABLE ... ALGORITHM=INPLACE`.
  The collector and the table Job are sized under `hopsworks.agentRouter.tracing.collector` and `.tableJob`.
- `kserve.envoyGateway.aiGateway.tracing.captureContent`, `false` by default, decides whether prompts and responses are stored.
  While it is false, the sidecar gets `OPENINFERENCE_HIDE_INPUTS`, `OPENINFERENCE_HIDE_OUTPUTS` and `OPENINFERENCE_HIDE_EMBEDDINGS_TEXT` set to `true`, so the message contents, the output text and the embedding inputs are left out of the spans, and the `messages` column keeps the role of each message with its content replaced by `__REDACTED__`.
  The collector keeps only `Error code: <status>` of the span status and its exception event unless the span carries captured content.
  Model name, token counts, status, timing, user and session stay, because they are what usage and debugging need.
  Prompts carry user data, so turn it on only when the users of the cluster have agreed to the retention.

Two audiences read the table:

- Administrators, in Cluster Settings, LLM Gateway Traces, which lists the traces of every project, filtered by project and deployment, with the project, deployment, user, session, status and timing of each.
  The backend never returns prompt or answer content on this page: it does not read the `messages` column, it keeps only an allowlist of span attributes (model, token counts, session, user, project, operation and HTTP status), it keeps events without their attributes, and of a span's status it returns only `Error code: <status>`, without the upstream error response.
- Project members with the role Data Owner or Data Scientist, in Project settings, LLM Gateway Traces, which shows only their project's traces, with a filter on the deployment, and in the Overview of each exposed deployment, which shows that deployment's traces.
  The backend returns only the project's own spans.

No Grafana datasource is provisioned for the traces table.

Turning the feature off leaves the table `agent__router.spans` and its rows in RonDB, where the TTL keeps deleting them.
Drop `agent__router.spans` by hand when it is no longer wanted.

## Access logs { #agent-router-access-logs }

The AI Gateway's Envoy writes one JSON line per request to its standard output, without bodies and without the `authorization` header.
The fields are `log_type` (`agent_router_access`), `start_time`, `method`, `path`, `status`, `duration_ms`, `response_flags`, `request_id`, `traceparent`, `project_id`, `project`, `user`, `model`, `backend`, `input_tokens`, `output_tokens`, `total_tokens` and `upstream_host`.
Filebeat collects them with the other pods of the release namespace, and Logstash writes the lines that carry a `project_id` to the index `agentrouter_<project id>-YYYY.MM.dd`, and drops the others.
Members of a project with the role Data Owner or Data Scientist read their project's indices, `agentrouter_<project id>-*`, in OpenSearch Dashboards, which is created as an index pattern with the project.
The service log viewer role reads all of them.
The `OpenSearchCleaner` deletes an index older than `elastic_logs_index_expiration`, the setting that applies to the project's other logs.

## Usage attribution { #agent-router-usage }

The `gen_ai_*` metrics of the sidecar carry the label `hopsworks_user`, taken from `x-hopsworks-user`, next to the model and the backend.
The number of values is bounded by the number of project members and of external users granted access to a deployment.
The Agent Router dashboard has a `user` variable and panels for tokens and requests per user, and a table of usage by project, user and model over the dashboard's time range.
The access logs carry the same user, model and token counts per request, for audits.

## Limitations { #agent-router-limitations }

- Knative-mode LLM deployments and Standard-mode ones behind the KEDA HTTP interceptor are not served by the LLM gateway, because the interceptor does not wake a deployment reached this way.
  A Standard-mode deployment is behind the interceptor when it scales to zero when idle, which is the case for a minimum of 0, or when it autoscales on a request metric, concurrency or requests per second.
  They stay on their per-deployment path, and the backend says so in the deployment's status note.
- While the LLM gateway is published, a vLLM deployment created without a minimum number of instances gets a minimum of 1, so it does not scale to zero when idle and the LLM gateway serves it.
  An explicit minimum of 0 is allowed, and a deployment with it is not served by the LLM gateway.
- Any member of the project can reach every one of its deployments through the LLM gateway, unless a Data Owner turns it off for the project or for a deployment, as described under [Access to the LLM gateway][agent-router-access].
- External providers, MCP and `InferencePool` backends are not part of it.
- The span table relies on RonDB's native TTL, which deletes rows by the age of `created_at`, and its `messages`, `attributes` and `events` columns hold up to `OTEL_MAX_TEXT_BYTES` each, so the rows of one span can be large when `captureContent` is on.
  A shorter `ttlSeconds` keeps fewer spans for the same traffic, once the TTL purge has deleted the expired ones, but does not give back space the table already holds in the tablespace.
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
- A network plugin that enforces NetworkPolicies.
- With `rbac.useExistingRole`, the chart renders no backend role.
  Grant the backend's service account, in the release namespace, `get, list, watch, create, update, patch, delete` on `aigatewayroutes` and `aiservicebackends` of `aigateway.envoyproxy.io` and on `backends` and `backendtrafficpolicies` of `gateway.envoyproxy.io`, on top of the Envoy Gateway permissions listed under [Cluster requirements][envoy-gateway-requirements].
  The chart grants them with a namespaced Role in the release namespace, the only namespace where the backend writes these objects.

## Turning it on { #agent-router-enable }

An upgrade that leaves `aiGateway` alone changes nothing: the Istio Lua filter is the same, no object is added, and the backend finds no `envoy-ai-gateway-config` ConfigMap and does nothing.

Before enabling:

1. List the started deployments with a [reserved name][agent-router-reserved-names] and stop them or recreate them under another name first.
   A started deployment has an InferenceService and a stopped one has none, and only started ones count: `kubectl get isvc -A --field-selector metadata.name=v1`.
   The projects with a deployment named `v1`, started or not, are listed by this query on the Hopsworks database:

   ```sql
   SELECT p.projectname FROM serving s JOIN project p ON s.project_id = p.id WHERE s.name = 'v1';
   ```

2. Check the [cluster requirements][agent-router-requirements]: Envoy Gateway, cert-manager, the backend role.
3. On an airgapped cluster, mirror the four [images][agent-router-images].
4. Two more hook Jobs run before the templates: the CRD Job `envoy-ai-gateway-crd-install` and the existing `kserve-ingress-gateway-apply`, which now also applies the AI Gateway; a few seconds each.

Enable with one `helm upgrade` (`aiGateway.enabled: true`).
The CRD Job applies the six CRDs, the controller and the AI Gateway come up, the Envoy Gateway controller restarts once for its new configuration, the Istio Lua filter and the forward rule change without a pod restart, and the backend's next pass creates the backends and routes of the started Standard-mode vLLM deployments that are not behind the KEDA interceptor.
The AI Gateway's Envoy pods roll once when the first route attaches, and again whenever the last LLM deployment of the cluster stops and another one starts later.
No predictive pod, Knative pod or `kserve-ingress-gateway` pod restarts.
Check that `kubectl get gateways.gateway.networking.k8s.io -n <namespace> <AI Gateway name>` reports `Programmed` (the name is `aiGateway.gatewayName`, `kserve-ai-gateway` by default), and that `kubectl get aigatewayroutes.aigateway.envoyproxy.io,aiservicebackends.aigateway.envoyproxy.io,backends.gateway.envoyproxy.io -n <namespace> -l serving.hops.works/gateway-route` lists one AIGatewayRoute per served LLM deployment, named `<project namespace>-<deployment>-llmroute`, with its AIServiceBackend and Backend.

If the controller goes down while Envoy Gateway runs, `extensionManager.failOpen: true` keeps the predictive routes translating: Envoy Gateway ignores the failed hook and builds its configuration without the controller's changes.
The AI routes depend on those changes, so they can stop answering until the controller is back.
A freshly started Envoy Gateway controller is different: until it has reached the AI Gateway controller once, it sends the Envoys no configuration updates at all, so the proxies keep their last configuration and endpoint changes behind the Gateway (a rolled pod, a scaled deployment) do not reach them.
In a cluster test where `model-serving-authenticator` rolled in that window, the Envoys kept checking requests against the old pod and refused Standard-mode requests for about two minutes, until the AI Gateway controller was back and Envoy Gateway's reconnect backoff had passed, so avoid restarting Envoy Gateway while the AI Gateway controller is down.
The webhook refuses to create new Envoy pods for the AI Gateway only, so a restart of those pods waits for the controller, and nothing else does.

## Turning it off { #agent-router-disable }

Disable in one upgrade with `aiGateway.enabled: false`.
The `kserve-ingress-gateway-apply` hook first deletes the ConfigMap `envoy-ai-gateway-config`, so the backend stops publishing routes and `model-serving-authenticator` reads the LLM gateway as off, and removes the LLM gateway's forward routes from the Hopsworks Gateway.
It then deletes the AI routes and backends, waits for the controller to remove them, clearing a finalizer that is still there after two minutes, and deletes the Gateway, waiting for its proxies to go, and the subchart removes the controller.
Requests in flight on the AI Gateway are cut when its Envoy pods terminate, up to the 60 s drain.
An upgrade that fails part way is run again as it was, because every hook step is idempotent.

`aiGateway.enabled: false` leaves the six CRDs and the filter-config Secrets the controller wrote in the release namespace for each Gateway there, named `<Gateway name>-<namespace>-<hash>` and `...-part-<n>`, for the AI Gateway and the Hopsworks Gateway alike.
An uninstall with the feature on removes those Secrets.
After a disable, remove them by hand when no longer wanted, checking the list before deleting it:

```bash
# aiGateway.gatewayName (kserve-ai-gateway by default) and the Hopsworks Gateway (kserve-ingress-gateway)
NS=<namespace>; GWS='kserve-ai-gateway|kserve-ingress-gateway'
kubectl get secret -n "$NS" -o name | grep -E "^secret/($GWS)-$NS-[0-9a-f]{12}(-part-[0-9]{3})?$"
kubectl get secret -n "$NS" -o name | grep -E "^secret/($GWS)-$NS-[0-9a-f]{12}(-part-[0-9]{3})?$" | xargs -r kubectl delete -n "$NS"
```

`hw-envoy-gateway.cleanupOnUninstall.deleteCrds` removes the six CRDs only on an uninstall while `aiGateway.enabled` is still true, so an uninstall after the feature was turned off leaves them too.

Roll the feature back with `helm upgrade`, never `helm rollback`, for the reason given under [Envoy Gateway][upgrade-envoy-gateway] in the upgrade guide.
A `helm rollback` or an `--atomic` failure that first enabled the feature removes what the chart renders as plain templates: the controller, its webhook configuration and the webhook's Certificate and Issuer.
What stays behind is the cert-manager Secret of the webhook, `ai-gateway-controller-webhook-cert`, and what the hook Jobs and the backend created: the AI Gateway with its policies and GatewayConfig, the DestinationRule, the AI routes and backends, the forward HTTPRoutes and SecurityPolicy on the Hopsworks Gateway, the rate-limit BackendTrafficPolicies, the Istio forward VirtualService rule and the AI branch of the Lua filter.
Upgrade again with the value off, which removes the objects the hook Jobs applied, or remove them by hand:

```bash
# aiGateway.gatewayName, kserve-ai-gateway by default
NS=<namespace>; AIGW=<AI Gateway name>
kubectl delete -n "$NS" aigatewayroutes.aigateway.envoyproxy.io,aiservicebackends.aigateway.envoyproxy.io,backends.gateway.envoyproxy.io -l serving.hops.works/gateway-route --wait=false
# the controller is gone, so clear the finalizer of what is left
for o in $(kubectl get aigatewayroutes.aigateway.envoyproxy.io,aiservicebackends.aigateway.envoyproxy.io,backends.gateway.envoyproxy.io -n "$NS" -l serving.hops.works/gateway-route -o name); do
  kubectl patch -n "$NS" "$o" --type=merge -p '{"metadata":{"finalizers":null}}'
done
# the forward routes of the LLM gateway on the Hopsworks Gateway, and the rate limits of the projects
kubectl delete -n "$NS" httproutes.gateway.networking.k8s.io -l 'serving.hops.works/gateway-route in (ai-path,ai-host)'
kubectl delete -n "$NS" securitypolicies.gateway.envoyproxy.io -l serving.hops.works/gateway-route=ai-path
kubectl delete -n "$NS" backendtrafficpolicies.gateway.envoyproxy.io -l serving.hops.works/gateway-route=ai-ratelimit
kubectl delete -n "$NS" destinationrules.networking.istio.io "$AIGW-forward" --ignore-not-found
kubectl delete -n "$NS" gateways.gateway.networking.k8s.io "$AIGW" --ignore-not-found
kubectl delete -n "$NS" securitypolicies.gateway.envoyproxy.io,backendtrafficpolicies.gateway.envoyproxy.io,clienttrafficpolicies.gateway.envoyproxy.io,envoyproxies.gateway.envoyproxy.io "$AIGW" --ignore-not-found
kubectl delete -n "$NS" gatewayconfigs.aigateway.envoyproxy.io "$AIGW" --ignore-not-found
# the HTTPRouteFilters the controller created, which name an AIGatewayRoute as their owner
for o in $(kubectl get httproutefilters.gateway.envoyproxy.io -n "$NS" -o jsonpath='{range .items[?(@.metadata.ownerReferences[0].kind=="AIGatewayRoute")]}{.metadata.name}{"\n"}{end}'); do kubectl delete -n "$NS" httproutefilters.gateway.envoyproxy.io "$o"; done
kubectl delete secret -n "$NS" ai-gateway-controller-webhook-cert --ignore-not-found
```

The Istio forward rule and the Lua AI branch are not removed by the commands above: only an upgrade with the value off, which re-renders them, does.
If the backend is rolled back as well, nothing removes the forward objects either, and they answer with a 5xx, and a deployment named `v1` gets `503`, until the next upgrade with the value off.

The six CRDs are `aigatewayroutes`, `aiservicebackends`, `backendsecuritypolicies`, `gatewayconfigs`, `mcproutes` and `quotapolicies`, all in the group `aigateway.envoyproxy.io`.
Delete them by hand with `kubectl delete crd <plural>.aigateway.envoyproxy.io`, which also deletes every object of that kind.
