---
description: How an agent deployment speaks A2A, the Agent2Agent protocol, so other agents and A2A clients can discover it and delegate work to it: the Agent Card, messages and tasks, streaming, artifacts, questions for a person, where tasks are kept, who may see them, push notifications, the signed card, and calling one from Python.
---

# A2A on Hopsworks

## Introduction

The [chat contract][the-chat-contract] is how a person, through the chat panel or the Python client, talks to an agent.
A2A, the [Agent2Agent protocol](https://a2a-protocol.org), is how another agent talks to it.
An agent written in Google ADK, LangGraph, the Microsoft Agent Framework or anything with an A2A client resolves the agent's Agent Card, sends it a message, and receives a task that moves through a lifecycle, streams its progress, and carries named artifacts.

Every agent built on `AgentApp` speaks A2A 1.0 with nothing to add to the handler.
The same deployment answers the chat panel over the chat contract and other agents over A2A, on the same URL and with the same credential.
Only an agent on an image with this SDK serves a card; an agent on an older image answers the chat contract only, and its deployment page shows no A2A section.

## What is served

| Route | Purpose |
| --- | --- |
| `GET /.well-known/agent-card.json` | The Agent Card: name, skills, media types, security schemes and the interface URLs |
| `POST /a2a` | The JSON-RPC binding: `SendMessage`, `SendStreamingMessage`, `GetTask`, `ListTasks`, `CancelTask`, `SubscribeToTask` |
| `/a2a/rest/...` | The HTTP+JSON binding of the same operations, for example `POST /a2a/rest/message:send` and `GET /a2a/rest/tasks/{id}` |
| `GET /a2a/artifacts/{task}/{digest}` | A [large part][a2a-large-artifacts] of a task, for whoever may read the task |

The routes sit under the deployment's URL, behind the same gateway as the chat routes, so an A2A client authenticates exactly as the chat panel does: `Authorization: ApiKey <serving api key>` or a bearer session token.
The card says so in its security schemes.

A client of your own must send the header `A2A-Version: 1.0` on every request, as the official clients do.
A request without it is taken for the 0.3 protocol and refused.

## The Agent Card

The card is built from the fields you already give `AgentApp`.
Its skills are the ones you declare, or one `chat` skill derived from the name, the description and the suggested prompts.
Its media types come from the modalities, listed one by one because the agent's own input validator checks each inbound part's type by exact membership against the card.

```python
from hopsworks_agents.protocol import AgentApp, AgentSkill


agent_app = AgentApp(
    name="Churn analyst",
    description="Answers questions about customer churn from the feature store",
    suggested_prompts=["Which segments churned most last quarter?"],
    skills=[
        AgentSkill(
            id="churn-report",
            name="Churn report",
            description="Monthly churn by segment as text and a CSV",
            tags=["churn", "analytics"],
            output_modes=["text/plain", "text/csv"],
        )
    ],
)
```

`input_media_types=` and `output_media_types=` replace the derived lists when an agent takes more or less than its modalities say.
`a2a=False` removes the card and the routes.

The interface URLs in the card are the deployment's public URL, which Hopsworks sets on the pod.
An agent run locally derives them from each request instead.
The card also carries the 0.3 `url`, `preferredTransport` and `protocolVersion` fields, so a client of the previous protocol version can discover the agent.

## A message becomes a turn, a turn becomes a task

An A2A message reaches your handler as the same `ChatRequest` a chat turn does.

- `contextId` is the conversation: memory, the subject index and the trace all key on it.
- `text` parts are the text; `raw` parts become image, audio or file content by media type; `data` parts land in `request.context`; `url` parts reach the handler as `request.urls`, untouched, unless the author set `AgentApp(fetch_urls=[...])` for their host.
- `metadata.hopsworks` on the message carries `subject`, `context` and `metadata`, the same three things the chat contract carries.

The turn's answer is a task.
The reply text is always the artifact named `response`, streamed chunk by chunk when the agent has a stream handler, and the task's final status message carries the answer with `metadata.hopsworks` holding the trace id, the citations, the usage and the subject.
A step reported with `ctx.emit_event` goes out as a working status with the step under `metadata.hopsworks.step`.
A refusal raised as `AgentError` fails the task with the agent's code under `metadata.hopsworks.status`; content the agent does not take is refused before any task exists.

### Artifacts

Named outputs beyond the reply are artifacts, returned whole or streamed while the handler works.

```python
from hopsworks_agents.protocol import AgentResponse, Artifact, TextContent


@agent_app.chat
async def chat(request, ctx):
    await ctx.emit_artifact("log", TextContent(text="fetching segments..."))
    summary, csv_b64 = await churn_report(request.text)
    return AgentResponse.text(
        summary,
        artifacts=[Artifact(name="churn.csv", media_type="text/csv", data=csv_b64)],
    )
```

The first chunk of an artifact creates it; a later chunk appends to it only when sent with `append=True`, otherwise it replaces it, and `last=True` closes the artifact.
Artifacts whose media type the caller did not accept are left out, and their names are listed under `metadata.hopsworks.dropped_artifacts` on the final status.

#### Large artifacts { #a2a-large-artifacts }

A stored task keeps small parts inline and large ones beside the database.
A `raw` part larger than 256 KiB is written to the deployment's artifact storage when its task is saved.
The stored task then carries a `url` part in its place, pointing at `/a2a/artifacts/...` under the deployment's URL, with the size and the SHA-256 digest of the bytes under `metadata.hopsworks`.
The 2 MiB cap applies to everything a task holds, as stored: its artifacts, its history, its status and its metadata.
When a task is larger, its largest remaining parts are stored the same way, large text and `data` parts included.
When it still does not fit, its oldest history messages are dropped first, then the content of its largest parts is omitted and replaced by a line that gives the size, and then any metadata other than `metadata.hopsworks`.
The task's `metadata.hopsworks` then says `truncated: true`, with the counts in `dropped_history_messages` and `omitted_parts`.
A task that still does not fit is stored without its artifacts and history, with a status message that says so.
An administrator can change both limits, see [cluster settings][a2a-cluster-settings].

A streaming caller receives the bytes inline in the events.
A caller that reads the task afterwards receives the URL, and fetches it with the credential it reads the task with:

```python
from a2a.types import GetTaskRequest


async def download(client, http, task_id):
    task = await client.get_task(GetTaskRequest(id=task_id))
    files = {}
    for artifact in task.artifacts:
        for part in artifact.parts:
            if part.WhichOneof("content") == "url":
                response = await http.get(part.url)
                response.raise_for_status()
                files[artifact.name] = response.content
    return files
```

Here `client` and `http` are the A2A client and the `httpx` client of the [Python example](#calling-an-agent-over-a2a-from-python) below.

### Questions for a person

`ctx.interrupt` pauses the task as `INPUT_REQUIRED`, or as `AUTH_REQUIRED` when every open question was asked with `reason="auth_required"`.
The questions ride in a `data` part of the status message, and the answer comes back as a message on the same task: a `data` part naming the question, `{"<interrupt id>": <payload>}`, or plain text when one question is open.
An answer that names a question the task did not ask, or leaves one open, is refused as an invalid-params error and the task stays paused.
A question that expired, or whose record is gone, fails the task, with `interrupt_expired` or `nothing_to_resume` under `metadata.hopsworks.status`.
A record is gone when the conversation was erased, or when the agent keeps its memory or its tasks in the process and the pod restarted.
An agent with [memory turned on from the deployment][agent-memory] keeps its open questions in the project's database, so a paused task is answered on any replica, and after a restart.
A task that is running the action a person approved cannot be cancelled: `CancelTask` is refused and the task finishes.

Do not put a credential in a message: every message is kept in the task's history.
An `auth_required` question describes what is needed in its `metadata`, and the answer is a reference the handler resolves itself, such as the name of a project secret.

### Several tasks on one context

A client may open a second task on a context while the first runs.
Each turn reads the conversation as it was when the turn first read it, and the store keeps every turn's rows together, in the order the turns started.
An agent that wants one task at a time per context sets `AgentApp(a2a=A2AConfig(serialize_context=True))`, with `from hopsworks_agents.protocol.a2a import A2AConfig`, and the next task waits as `SUBMITTED` until the running one ends or pauses.
`serialize_context` orders the tasks of one replica: two replicas may still each run a task on the same context.

## Where tasks are kept { #a2a-task-store }

On a deployment, tasks are kept in the project's online database, in tables Hopsworks creates when the deployment is created or started.
The tables are readable by the deployment's own database user and by the project's Data Owners.
Any replica reads, lists, cancels, answers or follows (`SubscribeToTask`) a task, whichever replica ran it, and a task outlives the pod that ran it.
A deployment with several instances needs no setting for this.
Finished tasks are deleted after a retention period, 30 days by default, see [cluster settings][a2a-cluster-settings].
The large parts a task kept beside the database, under `Resources/agents/a2a/` in the project, are deleted with it.

An agent can choose to keep its tasks in the process instead:

```python
from hopsworks_agents.protocol import AgentApp
from hopsworks_agents.protocol.a2a import A2AConfig


agent_app = AgentApp(name="Churn analyst", a2a=A2AConfig(task_store="memory"))
```

Tasks are then per replica and gone with the pod, so `GetTask`, `ListTasks`, `CancelTask`, `SubscribeToTask` and an answer to a question must reach the replica that ran the task.
Run such an agent with one instance.
`A2AConfig(max_tasks=..., max_task_bytes=...)` is the budget of the in-memory store: finished and paused tasks count, and the oldest are dropped first.

The in-memory store is only used when the author chose it.
A deployment that cannot reach a database, and whose author did not choose memory, serves no card and no A2A routes.
Its manifest then says `a2a: {enabled: false, reason: "no_database"}`, or `no_database_driver` when the image lacks the `agents-memory` extra of the `hopsworks` package.
A project without an online feature store has no such database.

A local run keeps tasks in the process.
Set `HOPSWORKS_AGENT_A2A_DATABASE_URL` to an async SQLAlchemy URL, for example `sqlite+aiosqlite:///tasks.db`, to run locally with the database store.

The manifest says which store is in use, as `task_store: "database"` or `task_store: "memory"` under `capabilities.custom.hopsworks.a2a`.

## Who may see a task

By default every holder of the deployment's credential sees every task of the deployment, the same way the conversation routes work, see [Agent Memory][agent-memory].

An agent built with `memory_routes=False` is **private**:

```python
from hopsworks_agents.protocol import AgentApp


agent_app = AgentApp(name="Support agent", memory_routes=False)
```

In a private agent a task, a conversation, its memory, its open questions and its push notification configs belong to the caller.
The caller is the principal the gateway verified from the request's credential and passed to the agent in the `x-hopsworks-principal` header.
This holds over A2A and over the chat routes alike.
Private mode separates the callers of the agent's API; the tasks stay in the project's online database, as [above][a2a-task-store].

- Another caller's task is answered as `TaskNotFoundError`, for `GetTask` and `CancelTask`, and `ListTasks` lists only the caller's own.
- A new task by another caller on the same `contextId` starts an empty conversation.
- The handler and the wire still see the plain ids; the caller is added where tasks and memory are stored.

Behind the gateway a private agent refuses a request that names no caller, with HTTP `401` and the code `principal_required`.
A local run has no gateway and treats every caller as `anonymous`.

The principal is the credential's owner, so callers that share one credential are one caller.
An application that calls the agent with one key on behalf of many people keeps those people apart itself.

The manifest says `private: true` for such an agent.

## A task whose replica is lost

A running task holds a lease in the database, which its replica renews with a heartbeat every 10 seconds.
The heartbeat also carries a cancel to the replica that runs the task: `CancelTask` may reach any replica, and the handler stops within one interval, with `ctx.cancelled` set.

When a replica stops renewing a lease for 30 seconds, a surviving replica takes the lease, or Hopsworks does when no replica is left.
The task then ends as `FAILED`, with this under `metadata.hopsworks` on its final status:

```json
{"status": "executor_lost", "outcome": "unknown", "retryable": true}
```

`outcome: unknown` means that nothing is known about how far the handler got.
The caller decides whether to send the message again.

A deployment that is stopped, restarted or scaled down ends its tasks in order instead.
The replica takes no new work and gives every accepted task a drain window, 10 minutes by default, to finish.
A task still running at the end of the window ends as `FAILED` with `status: "executor_shutdown"` and `retryable: true`.

A task sent with `returnImmediately` keeps running after the caller disconnected, so nothing but its replica holds it.
Keep at least one instance running for an agent with long detached tasks, rather than letting the deployment scale to zero while they run.

An agent whose handler is safe to run twice can have a lost task run again instead of failed:

```python
from hopsworks_agents.protocol import AgentApp
from hopsworks_agents.protocol.a2a import A2AConfig


agent_app = AgentApp(
    name="Churn analyst",
    a2a=A2AConfig(idempotent=True, retry_lost_tasks=1),
)
```

A surviving replica then runs the task again from the start, up to `retry_lost_tasks` times, with `attempt` counted in the task's metadata.
The task stays `WORKING` until it ends or the retries run out.
Hopsworks applies the same limit when it finds the lost task first: it hands the task back to the deployment's replicas, and fails it as `executor_lost` only when no replica takes it within 90 seconds.
`retry_lost_tasks` needs `idempotent=True`, and such an agent needs at least one replica left to run the task again.

## Push notifications

A caller that does not want to hold a stream open or poll registers a webhook, and the task's events are posted to it.
The webhook is registered with the message, as `configuration.taskPushNotificationConfig`, or later with the protocol's push notification config operations.

```python
import uuid

from a2a.types import (
    Message,
    Part,
    Role,
    SendMessageConfiguration,
    SendMessageRequest,
    TaskPushNotificationConfig,
)

request = SendMessageRequest(
    message=Message(
        message_id=str(uuid.uuid4()),
        role=Role.ROLE_USER,
        parts=[Part(text="Build the quarterly churn report")],
    ),
    configuration=SendMessageConfiguration(
        return_immediately=True,
        task_push_notification_config=TaskPushNotificationConfig(
            url="https://hooks.example.com/a2a/notifications",
            token=notification_token,
            authentication={"scheme": "Bearer", "credentials": receiver_token},
        ),
    ),
)
```

Each notification is an HTTP `POST` of one event of the task, as JSON, for example `{"statusUpdate": {"taskId": "...", "contextId": "...", "status": {...}}}`.

| Header | Value |
| --- | --- |
| `X-A2A-Notification-Token` | The `token` of the config, when one was given |
| `Authorization` | `<scheme> <credentials>` from the config's `authentication`, when one was given |

The push config is stored encrypted, with a key per deployment.
A deployment serves push notifications only when Hopsworks gave it its encryption key.
Otherwise its card says `pushNotifications: false` and its manifest says `push_notifications: false`.

### Where a webhook may be

The URL is checked when the webhook is registered and again when a notification is sent.
A URL that is not allowed is refused at registration as an invalid-params error (`-32602`).

- The URL must be HTTPS.
- A host with a public address is allowed.
- A host with a private address is allowed only when an administrator listed the host or its network.
- Loopback, link-local, multicast and cloud metadata addresses are never allowed.
- When an administrator set a list of allowed hosts, only those hosts are allowed.

Both lists are [cluster settings][a2a-cluster-settings].
The cluster's own inference gateway is always listed, so one agent deployment can notify another when the gateway is served over HTTPS.
For that, give the push config a callback key of the receiving deployment as its credential, `{"scheme": "ApiKey", "credentials": "<callback key>"}`.
A callback key is issued by `POST /hopsworks-api/api/project/{projectId}/serving/{servingId}/agents/callback-key`, which answers `{"key": "...", "expiresAt": "..."}`.
The key opens only `POST /a2a/notifications` of that deployment, and expires after the task retention period.
Redirects are not followed.

### Delivery

Delivery is queued, so a slow receiver does not hold the task's own stream.
A notification times out after 10 seconds.
It is tried again three times, after 1, 4 and 16 seconds, on a connection error or a `5xx` answer.
It is not tried again on a redirect or a `4xx` answer.

Events before the last one are best effort, and may be dropped when the receiver is slower than the task.
The terminal event is owed until it was delivered: when the replica could not deliver it, Hopsworks does.
A receiver may therefore see the same event twice.
Write the receiver to tolerate duplicates, and to read the task with `GetTask` for its current state rather than rebuild it from notifications.

## The extended card, and the signature

`GetExtendedAgentCard` returns the card with what the agent's manifest knows, for a caller that authenticated.
The memory tiers, the conversation and feedback endpoints, tool events and the graph are under the `agent` parameter of the [Hopsworks extension](#the-hopsworks-extension).
The public card sets `capabilities.extendedAgentCard`, and does not carry the `agent` parameter.

On a deployment the card served at the deployment's public URL carries a signature.
Hopsworks signs the card when the deployment starts, with a key the cluster holds, and only signs a card whose interface URLs are the deployment's own.
The cluster publishes the matching public keys as a JSON Web Key Set at `https://<hopsworks>/hopsworks-api/api/agents/jwks.json`, which needs no credential.
The signature is ES256, and the previous key stays listed after a rotation.
The signature's protected header names the project, the deployment and the serving id the card was signed for, as `hw_project`, `hw_deployment` and `hw_serving_id`.
The manifest says whether the card is signed, as `signed: true` or `signed: false`; a card built for a local run is not signed.

A client verifies the card with the official SDK and [PyJWT](https://pyjwt.readthedocs.io), reading the keys from the address of the cluster it trusts:

```python
import httpx
from a2a.client import A2ACardResolver
from a2a.utils.signing import create_signature_verifier
from jwt import PyJWKClient

base = "https://<inference-lb>/v1/<project-namespace>/<deployment>"
headers = {"Authorization": f"ApiKey {serving_key}"}
keys = PyJWKClient("https://<hopsworks>/hopsworks-api/api/agents/jwks.json")


def key_for(kid, jku):
    return keys.get_signing_key(kid)


verify = create_signature_verifier(key_for, ["ES256"])


async def verified_card():
    async with httpx.AsyncClient(headers=headers) as http:
        resolver = A2ACardResolver(http, base)
        return await resolver.get_agent_card(signature_verifier=verify)
```

`get_agent_card` raises when the card carries no signature that verifies against the cluster's keys.

## Cluster settings { #a2a-cluster-settings }

An administrator sets these variables on the [Cluster Configuration][cluster-configuration] page.
A deployment reads them when it starts, so restart a running deployment to apply a change.
Hopsworks reads the reaper interval when it starts.

| Variable | Default | Meaning |
| --- | --- | --- |
| `agent_deployment_push_internal_allow` | empty | Comma-separated host names and networks (CIDR) with private addresses that agents may post notifications to, and fetch `url` parts from. The inference gateway's addresses are always included. |
| `agent_deployment_push_allowed_hosts` | empty | Comma-separated host names. When set, a webhook is accepted only on one of these hosts. Empty means any host the rules above allow. |
| `agent_deployment_artifact_inline_bytes` | `262144` | The size in bytes above which a `raw` part of a task is stored beside the database and served by URL. |
| `agent_deployment_task_max_bytes` | `2097152` | The most a stored task holds inline, in bytes, all parts together. |
| `agent_deployment_task_retention_days` | `30` | How many days a finished task is kept, with its events and its push notification configs. |
| `agent_deployment_task_reaper_interval_ms` | `15000` | How often, in milliseconds, Hopsworks ends the tasks whose lease nobody renews and delivers the terminal notifications a replica could not. |

## Calling an agent over A2A from Python

Any A2A client works.
With the official Python SDK, against the same URL and credential the chat panel uses:

```python
import uuid

import httpx
from a2a.client import A2ACardResolver, ClientConfig, ClientFactory
from a2a.types import Message, Part, Role, SendMessageRequest

base = "https://<inference-lb>/v1/<project-namespace>/<deployment>"
headers = {"Authorization": f"ApiKey {serving_key}"}


async def ask():
    async with httpx.AsyncClient(headers=headers) as http:
        card = await A2ACardResolver(http, base).get_agent_card()
        config = ClientConfig(httpx_client=http, streaming=False)
        client = ClientFactory(config).create(card)
        request = SendMessageRequest(
            message=Message(
                message_id=str(uuid.uuid4()),
                role=Role.ROLE_USER,
                parts=[Part(text="Which segments churned most last quarter?")],
            )
        )
        async for event in client.send_message(request):
            print(event.task.status.state)
```

The base URL is the one the deployment page shows under *A2A*, and the key is an [API key][how-to-create-an-api-key] with the `SERVING` scope.

## What this release covers

The manifest describes the agent's A2A face under `capabilities.custom.hopsworks.a2a`: the bindings, `task_store`, `private`, `push_notifications`, `extended_card`, `signed`, `serialize_context` and `retry_lost_tasks`.
It says `a2a: {enabled: false, reason: "sdk_missing"}` when the `a2a-sdk` package is not installed, and `reason: "no_database"` when the deployment has [no database for its tasks][a2a-task-store].
gRPC, per-agent hostnames and a client for calling other agents from a handler are not in this release.

!!! note "Not yet available"

    - Completing an OAuth authorization that an agent asked for with `AUTH_REQUIRED` through a Hopsworks callback.
    - Callback keys on clusters whose inference gateway is Envoy Gateway.
    - Tooling to rotate the card signing key.

## The Hopsworks extension

The card declares one extension, `https://hopsworks.ai/a2a/extensions/hopsworks/v1`, which is not required: it only names what `metadata.hopsworks` carries, and a client that never asks for it gets a conforming response.
Its `params` on the card are the keys below, with the same one-line descriptions.

| Key | Direction | What it carries |
| --- | --- | --- |
| `subject` | In, on the message | Who the agent is talking to, for its memory |
| `context` | In, on the message | Anything the handler should see with the request |
| `metadata` | In, on the message | Free-form metadata for the handler |
| `trace_id` | Out | The turn's trace, for feedback and evaluation |
| `citations` | Out, on the final status | The sources the reply cites |
| `usage` | Out, on the final status | Token counts |
| `step` | Out, on a working status | A step the agent reported |
| `tool_call` | Out, on a working status | A tool call the agent made |
| `interrupts` | Out, on an input- or auth-required status | The questions asked |
| `status` | Out, on a failed status | The agent's error code |
| `retryable` | Out, on a failed status | Whether a retry is worth it |

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-method"></code> [`Project.get_agent_serving`][hopsworks_common.project.Project.get_agent_serving]
    - <code class="doc-symbol doc-symbol-docs"></code> [A2A protocol specification](https://a2a-protocol.org/latest/specification/)

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>
