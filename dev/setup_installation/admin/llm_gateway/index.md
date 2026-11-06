# LLM Gateway { #llm-gateway }

The LLM Gateway gives every project one OpenAI-compatible endpoint for all its LLM deployments.
A client sends every request to the same URL and picks the deployment with the request's `model`, the deployment name:

```text
<inference endpoint>/v1/<project>/v1/chat/completions
<inference endpoint>/v1/<project>/v1/completions
<inference endpoint>/v1/<project>/v1/embeddings
<inference endpoint>/v1/<project>/v1/models
```

`<project>` is the project's namespace, and the project name works wherever it works for deployments.
`GET .../v1/models` lists the project's started LLM deployments.
It runs on top of [Envoy Gateway][envoy-gateway], and the Hopsworks backend adds and removes its routes as deployments start and stop.

--8<-- "setup_installation/admin/llm_gateway/request-flow.html"

!!! note "Built on Agent Router"

    The LLM Gateway is built on [Agent Router](https://theagentrouter.ai), previously known as Envoy AI Gateway, an open source project on top of Envoy and Envoy Gateway.

The model list can trail the routes by up to about a minute after a deployment starts or stops, since the LLM Gateway reads it from a mounted Secret that the kubelet refreshes on its own schedule.

## How to enable it { #llm-gateway-enable }

One value on top of the Envoy Gateway ones turns the feature on:

```yaml
global:
  _hopsworks:
    envoyGateway:
      enabled: true
      aiGateway:
        enabled: true
```

`aiGateway.enabled` installs the CRDs, the controller and the AI Gateway, and publishes the LLM Gateway.
Rendering fails when it is on without `envoyGateway.enabled`.
All values are listed in [Envoy Gateway values][helm-values-hw-envoy-gateway] and under `kserve.envoyGateway.aiGateway` in [KServe values][helm-values-kserve].

Before enabling:

1. Stop the started deployments with a [reserved name][llm-gateway-reserved-names], or recreate them under another name.
   A started deployment has an InferenceService and a stopped one has none, and only started ones count: `kubectl get isvc -A --field-selector metadata.name=v1`.
   This query on the Hopsworks database lists the projects with a deployment named `v1`, started or not:

   ```sql
   SELECT p.projectname FROM serving s JOIN project p ON s.project_id = p.id WHERE s.name = 'v1';
   ```

2. Check the [cluster requirements][llm-gateway-requirements]: Envoy Gateway, cert-manager, the backend role.
3. On an airgapped cluster, mirror the four [images][llm-gateway-images].

Then enable with one `helm upgrade`.
Two hook Jobs run before the templates, a few seconds each: `envoy-ai-gateway-crd-install`, which applies the six CRDs, and the existing `kserve-ingress-gateway-apply`, which now also applies the AI Gateway.
The controller and the AI Gateway come up, the Envoy Gateway controller restarts once for its new configuration, and the Istio Lua filter and the forward rule change without a pod restart.
The backend's next pass then creates the routes of the started Standard-mode vLLM deployments that the LLM Gateway serves.
No predictive pod, Knative pod or `kserve-ingress-gateway` pod restarts.
The AI Gateway's Envoy pods roll once when the first route attaches, and again whenever the last LLM deployment of the cluster stops and another one starts later.

To check the result:

- `kubectl get gateways.gateway.networking.k8s.io -n <namespace> kserve-ai-gateway` reports `Programmed` (the name is `aiGateway.gatewayName`).
- `kubectl get aigatewayroutes.aigateway.envoyproxy.io,aiservicebackends.aigateway.envoyproxy.io,backends.gateway.envoyproxy.io -n <namespace> -l serving.hops.works/gateway-route` lists one AIGatewayRoute per served LLM deployment, named `<project namespace>-<deployment>-llmroute`, with its AIServiceBackend and Backend.

??? note "When the LLM Gateway controller is down"

    While Envoy Gateway runs, `extensionManager.failOpen: true` keeps the predictive routes translating when the controller is down: Envoy Gateway ignores the failed hook and builds its configuration without the controller's changes.
    The AI routes depend on those changes, so they can stop answering until the controller is back.

    A freshly started Envoy Gateway controller is different: until it has reached the LLM Gateway controller once, it sends the Envoys no configuration updates at all.
    The proxies keep their last configuration, and endpoint changes behind the Gateway, such as a rolled pod or a scaled deployment, do not reach them.
    In a cluster test where `model-serving-authenticator` rolled in that window, the Envoys kept checking requests against the old pod and refused Standard-mode requests for about two minutes, until the controller was back and Envoy Gateway's reconnect backoff had passed.
    Avoid restarting Envoy Gateway while the LLM Gateway controller is down.

    The controller's webhook refuses to create new Envoy pods for the AI Gateway only, so a restart of those pods waits for the controller, and nothing else does.

## What gets installed { #llm-gateway-components }

- The LLM Gateway controller, in the `hw-envoy-gateway` subchart, with templates vendored from the upstream `ai-gateway-helm` chart 1.2, its mutating webhook with a cert-manager Certificate, and the Envoy Gateway configuration that lets Envoy Gateway call it (`extensionManager` with `failOpen: true`, and `extensionApis.enableBackend`).
- A dedicated AI Gateway, `kserve-ai-gateway` (`aiGateway.gatewayName`), in the `kserve` subchart: its own Gateway on the same GatewayClass, an EnvoyProxy with a `ClusterIP` Service, a GatewayConfig that sizes the ext_proc sidecar, a SecurityPolicy that checks every request with `model-serving-authenticator`, a BackendTrafficPolicy with no request timeout and a ClientTrafficPolicy with a 50Mi connection buffer (`kserve.envoyGateway.aiGateway.bufferLimit`).
- The ConfigMap `envoy-ai-gateway-config`, which tells the backend and `model-serving-authenticator` which Gateway to use, whether the LLM Gateway is published and whether [tracing][llm-gateway-tracing] is on.
  While `aiGateway.enabled` is false the ConfigMap is absent, and both do nothing.
- A Redis and Envoy Gateway's rate-limit service (`envoyproxy/ratelimit`) for the [rate limits][llm-gateway-rate-limits], in the `hw-envoy-gateway` subchart.
  Redis runs Superset's Redis image and keeps no data on disk, and only the rate-limit service may connect to it.
- With tracing on, the trace collector `agent-router-otlp` and a Job that creates its table, in the `hopsworks` chart, as described under [Tracing][llm-gateway-tracing].
  Only the AI Gateway's Envoy pods may send to the collector.
- Prometheus scraping of the controller (port 8080) and of the ext_proc sidecar (port 1064, through the Service `kserve-ai-gateway-extproc-metrics`), and Grafana dashboards, as described under [Usage attribution][llm-gateway-usage].
- A branch in the Istio Lua filter that rewrites `/v1/<project>/v1/<rest>` to the host `v1.<namespace>.<domain>` and the path `/v1/<rest>`, and a first route in the Istio forward VirtualService that sends that host to the AI Gateway.
  With the feature off, the Lua filter is the one of a chart without it, so an existing deployment named `v1` keeps its path.
- The six CustomResourceDefinitions (CRDs) of the LLM Gateway, 2 MB together, shipped in the `envoy-ai-gateway-crds` image and applied by the `envoy-ai-gateway-crd-install` hook Job, for the reason given under [CustomResourceDefinitions][envoy-gateway-crds].

The AI Gateway is separate from `kserve-ingress-gateway` on purpose.
The controller injects the ext_proc sidecar into the Envoy pods of the Gateway that carries AI routes, and rolls them when the first route attaches, when the last one goes and whenever the sidecar's image, resources or GatewayConfig change.
Only the AI Gateway's Envoy pods roll: the Hopsworks Gateway, Knative and the predictive routes are not touched.
Starting or stopping an LLM deployment while another one is running rolls nothing.
The controller's webhook (`failurePolicy: Fail`) selects the AI Gateway's pods in the release namespace only, so a controller that is down blocks no other pod.

The AI Gateway admits routes from the release namespace only, and every AI object lives there.
Its filter chain checks the API key before anything else, so `GET /v1/models` needs a valid key too.

## Access to the LLM Gateway { #llm-gateway-access }

Project members with an allowed role can use their project's LLM Gateway.
Two switches, both on by default, narrow what it serves:

- The project switch turns the LLM Gateway off for a whole project, which then answers `404`.
- The deployment switch keeps one LLM deployment off the LLM Gateway while the others stay on it.
  The deployment is still reachable on its per-deployment path.

Only the project's Data Owners change either switch.
A change takes effect without restarting a deployment: the backend adds or removes the project's routes.

External users reach a deployment through its External access groups, described in [External access][serving-external-access], and those groups also grant its use through the LLM Gateway.
An external user whose groups are listed for a deployment can send requests with that deployment as the `model`, and no others, to these operations only:

- Chat completions, `/v1/chat/completions`
- Completions, `/v1/completions`
- Embeddings, `/v1/embeddings`
- Responses, `/v1/responses`
- Anthropic messages, `/anthropic/v1/messages`

Every listing, `GET .../v1/models` under any prefix, and every other path are refused for them with `403`.
`model-serving-authenticator` makes the check on the request body, which the AI Gateway sends to it up to its 50Mi buffer limit (`kserve.envoyGateway.aiGateway.bufferLimit`).

## Reserved deployment names { #llm-gateway-reserved-names }

`v1` is a reserved deployment name, whether or not the LLM Gateway is on, because the LLM Gateway takes `/v1/<project>/v1/` and `v1.<namespace>.<domain>` in every project.
The backend refuses to create a deployment named `v1`.
An existing one stays editable and restartable, and works as before while `aiGateway.enabled` is off.

Once the LLM Gateway is on, only a started deployment named `v1` matters; a stopped one blocks nothing.
While one is started:

- The backend leaves the LLM Gateway out of that project, and says so in its deployments' status notes and in the LLM Gateway card of the project settings.
- The deployment itself is not served by the LLM Gateway, and answers `404` through the Istio ingress on both its path and its host.
  It keeps its routes on the Envoy Gateway, and answers there.

Stop the deployment, or recreate it under another name, to get the LLM Gateway in that project.
Starting it again later has the same effect again.

## Identity headers { #llm-gateway-identity }

For a request that passes the check, `model-serving-authenticator` returns three headers that Envoy adds to the request, for members and external users alike:

- `x-hopsworks-user`, the username.
- `x-hopsworks-project`, the project's namespace.
- `x-hopsworks-project-id`, its numeric id.

The rate limits, the traces, the access logs and the usage metrics are keyed on them.
Clients cannot set them: the AI Gateway removes them from the incoming request before the check runs, so only the authenticator's values reach the backend.

The id comes from the label `serving.hops.works/project-id` of the ConfigMap `<namespace>-project-teams`, which the backend writes when it creates the ConfigMap and on every rebuild of a project's routes.
When the label is missing, the id header is empty, the authenticator logs a warning and the request is still allowed.
The request is still rate limited, because the per-user rule keys on `x-hopsworks-user`, the per-deployment rule on the model and the project rule is per project.
What is lost until the next rebuild writes the label is that request's span, which the collector drops without a project id, and its access-log line, which Logstash routes only for a numeric id.

## Rate limits and token quotas { #llm-gateway-rate-limits }

Administrators can cap what a project spends through the LLM Gateway, in tokens or in requests.
Limits are admin-only, because they cap what a project can spend on shared GPUs and a project owner could otherwise lift their own cap.

Each limit has a scope:

| Scope        | Bucket                                                    |
| ------------ | --------------------------------------------------------- |
| `PROJECT`    | One bucket for all requests to the project's endpoint     |
| `USER`       | One bucket per user, keyed on `x-hopsworks-user`          |
| `DEPLOYMENT` | One bucket per deployment, keyed on the request's `model` |

It also has a kind, `TOKENS` (the input and output tokens of a request together) or `REQUESTS`, and a unit, `MINUTE`, `HOUR` or `DAY`.
A rule is shared by every route of a project, so a project with several routes still has one bucket per rule.

### Cluster defaults

The cluster default of each scope and kind is a Hopsworks variable holding `VALUE/UNIT`, for example `1000000/HOUR`.
An administrator edits them in the cluster settings, on the Quotas and Rate Limits page, in the LLM Gateway section.

| Variable                               | Limits                  |
| -------------------------------------- | ----------------------- |
| `llm_gateway_project_token_limit`      | `PROJECT` `TOKENS`      |
| `llm_gateway_project_request_limit`    | `PROJECT` `REQUESTS`    |
| `llm_gateway_user_token_limit`         | `USER` `TOKENS`         |
| `llm_gateway_user_request_limit`       | `USER` `REQUESTS`       |
| `llm_gateway_deployment_token_limit`   | `DEPLOYMENT` `TOKENS`   |
| `llm_gateway_deployment_request_limit` | `DEPLOYMENT` `REQUESTS` |

- The value is from 1 to 4294967295, because Envoy Gateway holds a rate-limit value as an unsigned 32-bit integer and cannot express a larger one.
- An empty or unset variable, or `-1` with a unit such as `-1/HOUR`, means no limit for that scope and kind.
  A value without a unit, such as `-1` alone, is refused, and so is any value that does not parse, with `422`.
- The variables are seeded empty, and an upgrade keeps the values an administrator set.
- A change reaches the existing projects at the backend's next full pass, about 10 minutes later.

### Per-project overrides

An override per project is set on the admin page that edits the project, under LLM Gateway limits, with the same scopes, kinds and units, and applies immediately.
The value range is the same, and `-1` makes the scope unlimited for that project.
Removing the override makes the cluster default apply again.
The same limits are available as `llmGatewayLimits` of `projectQuotas` in `PUT /admin/projects/{id}`, and `GET /admin/projects/{id}?expand=quotas` returns the effective ones with a `source` of `DEFAULT` or `PROJECT`.

The backend turns the effective limits into one BackendTrafficPolicy per project, `<namespace>-llmratelimit`, in the release namespace, and updates it with no restart when a limit or a deployment changes.
Project members see their project's limits, read-only, in the quotas of the project settings and on the LLM Gateway card.

### When a request is over a limit

A request over a limit gets `429` with the `x-ratelimit-*` headers.
A token limit charges a request after its response: the sidecar reads the token counts from the response, and Envoy subtracts them from the bucket then.
So a running stream is never cut when it crosses the limit, and the next request gets the `429`.
For the same reason, a request is refused only once the bucket is already empty, so a single request can overshoot the limit.

!!! note "The rate limiter fails open"

    When Redis or the rate-limit service is down, requests are let through, because a rate limiter that is down must not take down model serving.
    The counters live in Redis memory only, so they reset when the Redis pod restarts, and the limits are not exact across that restart.

## Tracing { #llm-gateway-tracing }

With tracing on, the LLM Gateway records an OpenTelemetry span for every request, and administrators and project members browse them on the trace pages.

!!! warning "Off by default, and keep it off on RonDB 26.02"

    On RonDB 26.02 the queries behind the trace pages can stop a RonDB data node, as described under [Limitations][llm-gateway-limitations].
    That is why tracing is off by default.

Tracing has its own switch next to `aiGateway.enabled`:

```yaml
global:
  _hopsworks:
    envoyGateway:
      aiGateway:
        enabled: true
        tracing:
          enabled: true
```

While it is off:

- The ext_proc sidecar gets `OTEL_TRACES_EXPORTER=none` and exports no spans.
- The chart renders neither the trace collector nor the Job that creates its table.
- The `envoy-ai-gateway-config` ConfigMap carries `tracing: "false"`, so the backend answers both trace pages with no traces and never queries the table.

The sidecar's Prometheus metrics, the access logs and the rate limits work the same either way.
Turning tracing off stops new spans and empties the trace pages, and the table and its rows stay until the TTL deletes them.

### What a span holds

The LLM Gateway adds `hopsworks.user`, `hopsworks.project.id` and `session.id` to every span, from the headers `x-hopsworks-user`, `x-hopsworks-project-id` and `agent-session-id`, with the controller arguments under `hw-envoy-gateway.aiGateway.requestHeaderAttributes.span` and `.metrics`.
The sidecar sends the spans over OTLP/HTTP to the collector `agent-router-otlp`, which writes them to the RonDB table `agent__router.spans` with the `hopsworksroot` credential from the Secret `mysql-users-secrets`.
The collector drops a span that has no `hopsworks.project.id`, and counts the drops in its log, because a span of no project cannot be shown to anyone.

The columns `messages`, `attributes` and `events` are `MEDIUMTEXT`.
The collector caps each of them at `OTEL_MAX_TEXT_BYTES` of UTF-8, 262144 by default, by dropping or shortening JSON elements so the value stays valid JSON, and adds `hopsworks.truncated: true` to `attributes` when it clipped anything.
Both trace pages mark such a span as truncated, and also a span whose column does not parse.

### Prompts and responses

`kserve.envoyGateway.aiGateway.tracing.captureContent`, `false` by default, decides whether prompts and responses are stored.
While it is false:

- The sidecar gets `OPENINFERENCE_HIDE_INPUTS`, `OPENINFERENCE_HIDE_OUTPUTS` and `OPENINFERENCE_HIDE_EMBEDDINGS_TEXT` set to `true`, so message contents, output text and embedding inputs are left out of the spans.
- The `messages` column keeps the role of each message, with its content replaced by `__REDACTED__`.
- The collector keeps only `Error code: <status>` of a span's status and of its exception event.

Model name, token counts, status, timing, user and session stay, because they are what usage and debugging need.

!!! tip "Turn content capture on only with the users' agreement"

    Prompts carry user data, so turn `captureContent` on only when the users of the cluster have agreed to the retention.

### Who can read the traces

- Administrators, in Cluster Settings, LLM Gateway Traces, which lists the traces of every project, filtered by project and deployment, with the project, deployment, user, session, status and timing of each.
  This page never returns prompt or answer content: the backend does not read the `messages` column, keeps only an allowlist of span attributes (model, token counts, session, user, project, operation and HTTP status), keeps events without their attributes, and returns only `Error code: <status>` of a span's status, without the upstream error response.
- Project members with the role Data Owner or Data Scientist, in Project settings, LLM Gateway Traces, which shows their project's traces with a filter on the deployment, and in the Overview of each exposed deployment, which shows that deployment's traces.
  The backend returns only the project's own spans.

No Grafana datasource is provisioned for the traces table.

### Retention and storage

`hopsworks.agentRouter.tracing.ttlSeconds`, 604800 (seven days) by default, is the age after which RonDB's native TTL deletes a span row, counted from the column `created_at`.
The table is created by a Job while `aiGateway.enabled` and `aiGateway.tracing.enabled` are on, and the Job runs again when the TTL changes, with `ALTER TABLE ... ALGORITHM=INPLACE`.
The collector and the Job are sized under `hopsworks.agentRouter.tracing.collector` and `.tableJob`.

Turning the feature or its tracing off leaves `agent__router.spans` and its rows in RonDB, where the TTL keeps deleting them.
Drop the table by hand when it is no longer wanted.

??? note "Where the spans are stored and how to size it"

    The table is in the online feature store's disk tablespace, `featurestore_online_tablespace`, or else the cluster's NDB tablespace, `ts_1`, which feature groups with disk columns and the traces of model deployments share.
    Every span stays for the whole TTL, so keeping most of it on disk keeps the table's share of RonDB DataMemory small, which every online feature group needs.

    - In memory: the keys, the indexed columns, `created_at`, and the columns the trace pages filter on (`deployment`, `username`, `session_id` and `parent_span_id`), because RonDB keeps keys and indexed columns there and requires the TTL column there.
    - On disk: the other columns, `messages`, `attributes` and `events` included, apart from the first 256 bytes of each text column and a small key for each part of the text beyond them, which RonDB keeps in memory.

    The Job:

    - creates the table in memory, and logs a warning, on a cluster without a tablespace;
    - fails when `featurestore_online_tablespace` names a tablespace that does not exist, or contains characters other than letters, digits and underscores;
    - never drops or moves an existing table: changing the tablespace, or adding one after the table was created in memory, leaves the table where it is, with a warning in the Job's log, until it is dropped by hand.

    The chart creates `ts_1` at install with the size of the disk-column volume, `rondb.rondb.resources.requests.storage.diskColumnGiB` (2 GiB by default), or `InitialTablespaceSizeGiB` when that is set.
    Size it for the spans one TTL keeps, next to what feature groups and deployment traces store there.
    On an installed cluster, a larger volume does not grow the tablespace: add a data file with `ALTER TABLESPACE ... ADD DATAFILE`.

    When the tablespace has no free extent left, inserts that need new space fail, and the collector logs the failure and drops those spans, which adding space later does not bring back.
    Spans the TTL purge has deleted free space for later spans in the same table, not in the tablespace.
    The purge runs in the RonDB REST API servers, and `rondb.rondb.rdrs.ttlPurge` controls it.
    The `LowDiskDataFileExtents` alert fires when less than 20% of `ts_1` is free for 5 minutes; it does not watch another tablespace named in `featurestore_online_tablespace`.

## Access logs { #llm-gateway-access-logs }

The AI Gateway's Envoy writes one JSON line per request to its standard output, without bodies and without the `authorization` header.
The fields are `log_type` (`agent_router_access`), `start_time`, `method`, `path`, `status`, `duration_ms`, `response_flags`, `request_id`, `traceparent`, `project_id`, `project`, `user`, `model`, `backend`, `input_tokens`, `output_tokens`, `total_tokens` and `upstream_host`.

Filebeat collects them with the other pods of the release namespace, and Logstash writes the lines that carry a `project_id` to the index `agentrouter_<project id>-YYYY.MM.dd`, and drops the others.
Project members with the role Data Owner or Data Scientist read their project's indices, `agentrouter_<project id>-*`, in OpenSearch Dashboards, where the index pattern is created with the project.
The service log viewer role reads all of them.
The `OpenSearchCleaner` deletes an index older than `elastic_logs_index_expiration`, the setting that applies to the project's other logs.

## Usage attribution { #llm-gateway-usage }

The ext_proc sidecar's metrics follow the OpenTelemetry generative AI conventions, for example `gen_ai_client_token_usage` and `gen_ai_server_request_duration_seconds`.
They are labelled with the model, the backend, `<Hopsworks namespace>/<project namespace>-<deployment>-aibackend`, and `hopsworks_user`, taken from `x-hopsworks-user`.
Prometheus sets their `namespace` label to the project's namespace, so token usage can be summed per project, per deployment and per user.
The number of `hopsworks_user` values is bounded by the number of project members and of external users granted access to a deployment.

Grafana shows them in the ModelServing folder:

- The LLM Gateway (Agent Router) dashboard has tokens, requests, errors and latency per project and deployment, for one project at a time, a `user` variable with panels for tokens and requests per user, and a table of usage by project, user and model over the dashboard's time range.
- The vLLM Deployment Metrics dashboard has an LLM Gateway row for each deployment.

The access logs carry the same user, model and token counts per request, for audits.

## Limitations { #llm-gateway-limitations }

- Knative-mode LLM deployments and Standard-mode ones behind the KEDA HTTP interceptor are not served by the LLM Gateway, because the interceptor does not wake a deployment reached this way.
  A Standard-mode deployment is behind the interceptor when it scales to zero when idle, which is the case for a minimum of 0, or when it autoscales on a request metric, concurrency or requests per second.
  They stay on their per-deployment path, and the backend says so in the deployment's status note.
- While the LLM Gateway is published, a vLLM deployment created without a minimum number of instances gets a minimum of 1, so it does not scale to zero when idle and the LLM Gateway serves it.
  An explicit minimum of 0 is allowed, and a deployment with it is not served by the LLM Gateway.
- Any member of the project can reach every one of its deployments through the LLM Gateway, unless a Data Owner turns it off for the project or for a deployment, as described under [Access to the LLM Gateway][llm-gateway-access].
- External providers, MCP and `InferencePool` backends are not part of it.
- On RonDB 26.02 (26.02.11 and 26.02.13 tested), the queries behind the trace pages can stop a RonDB data node with error 2341, `DBQACC (Line: 2154) Check m_curr_acc->oprec_pool.getValidPtr(loopPtr) failed`.
  It happens when one statement reads the `messages` column and looks up parent spans by primary key, which the project trace list, the session view and the message search do, with the table in memory or on disk alike.
  That is why [tracing][llm-gateway-tracing] is off by default.
- The rows of one span can be large when `captureContent` is on, since `messages`, `attributes` and `events` hold up to `OTEL_MAX_TEXT_BYTES` each.
  A shorter `ttlSeconds` keeps fewer spans for the same traffic, once the TTL purge has deleted the expired ones, but does not give back space the table already holds in the tablespace.
- Enabling the feature, or changing `tracing.enabled`, `captureContent` or the tracing endpoint, changes the GatewayConfig environment, which rolls the AI Gateway's Envoy pods once, for the reason given under [What gets installed][llm-gateway-components].
- On OpenShift, `values.openshift.yaml` leaves both `envoyGateway.enabled` and `aiGateway.enabled` off.
- The controller logs `Failed to add finalizer to object` once per ReferenceGrant it sees, the per-project grants of the Hopsworks Gateway included.
  The chart's Role refuses that write on purpose: a finalizer of the controller on those grants would block their deletion once the controller is gone, and the AI routes and backends never cross a namespace, so the controller needs nothing from the grants.

## Images { #llm-gateway-images }

| Image                                                | Used for                                                         |
| ---------------------------------------------------- | ---------------------------------------------------------------- |
| `docker.hops.works/envoyproxy/ai-gateway-controller` | The LLM Gateway controller                                       |
| `docker.hops.works/envoyproxy/ai-gateway-extproc`    | The ext_proc sidecar, named by the controller's `--extProcImage` |
| `docker.hops.works/envoyproxy/ratelimit`             | Envoy Gateway's rate-limit service                               |
| `docker.hops.works/hopsworks/envoy-ai-gateway-crds`  | The CRDs, read by the hook Job                                   |

The ext_proc sidecar runs in no pod until the first route exists.
Like the Envoy Gateway images, the three `envoyproxy` images are mirrors of the Docker Hub images at the same path, and the CRD image is a Hopsworks image.
An airgapped install overrides these four images, as the chart's `values.airgap.yaml` shows.
The Redis of the rate limiter uses Superset's Redis image, and the trace collector the `otlp-sidecar` image of agent deployments, so an airgapped cluster that mirrors those already has them.

## Cluster requirements { #llm-gateway-requirements }

- Envoy Gateway, enabled already or in the same upgrade, as described in [Envoy Gateway][envoy-gateway].
- cert-manager, because the controller's webhook certificate is a cert-manager Certificate.
  The `kserve` subchart installs cert-manager unless the platform brings its own.
- A network plugin that enforces NetworkPolicies.

??? note "Permissions for `rbac.useExistingRole`"

    With `rbac.useExistingRole`, the chart renders no backend role.
    Grant the backend's service account, in the release namespace, `get, list, watch, create, update, patch, delete` on `aigatewayroutes` and `aiservicebackends` of `aigateway.envoyproxy.io` and on `backends` and `backendtrafficpolicies` of `gateway.envoyproxy.io`, on top of the Envoy Gateway permissions listed under [Cluster requirements][envoy-gateway-requirements].
    The chart grants them with a namespaced Role in the release namespace, the only namespace where the backend writes these objects.

## Turn it off { #llm-gateway-disable }

Disable in one upgrade with `aiGateway.enabled: false`.
The `kserve-ingress-gateway-apply` hook then:

1. Deletes the ConfigMap `envoy-ai-gateway-config`, so the backend stops publishing routes and `model-serving-authenticator` reads the LLM Gateway as off.
2. Removes the LLM Gateway's forward routes from the Hopsworks Gateway.
3. Deletes the AI routes and backends, waits for the controller to remove them, and clears a finalizer that is still there after two minutes.
4. Deletes the Gateway and waits for its proxies to go.

The subchart then removes the controller.
Requests in flight on the AI Gateway are cut when its Envoy pods terminate, after up to the 60 s drain.
An upgrade that fails part way is run again as it was, because every hook step is idempotent.

!!! warning "Use `helm upgrade`, not `helm rollback`"

    Roll the feature back with `helm upgrade`, for the reason given under [Envoy Gateway][upgrade-envoy-gateway] in the upgrade guide.
    A `helm rollback`, or an `--atomic` failure, of the upgrade that first enabled the feature removes only what the chart renders as plain templates, and leaves the rest behind, as listed below.

??? note "What stays after turning the feature off"

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
    The six CRDs are `aigatewayroutes`, `aiservicebackends`, `backendsecuritypolicies`, `gatewayconfigs`, `mcproutes` and `quotapolicies`, all in the group `aigateway.envoyproxy.io`.
    Delete them by hand with `kubectl delete crd <plural>.aigateway.envoyproxy.io`, which also deletes every object of that kind.

??? note "Clean up after a `helm rollback`"

    A `helm rollback` or an `--atomic` failure that first enabled the feature removes the controller, its webhook configuration and the webhook's Certificate and Issuer.
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
    # the forward routes of the LLM Gateway on the Hopsworks Gateway, and the rate limits of the projects
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

    The Istio forward rule and the Lua AI branch are not removed by these commands: only an upgrade with the value off, which re-renders them, does.
    If the backend is rolled back as well, nothing removes the forward objects either, and they answer with a 5xx, and a deployment named `v1` gets `503`, until the next upgrade with the value off.
