---
description: How an agent deployment speaks A2A, the Agent2Agent protocol, so other agents and A2A clients can discover it and delegate work to it: the Agent Card, messages and tasks, streaming, artifacts, questions for a person, and calling one from Python.
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

### Questions for a person

`ctx.interrupt` pauses the task as `INPUT_REQUIRED`, or as `AUTH_REQUIRED` when every open question was asked with `reason="auth_required"`.
The questions ride in a `data` part of the status message, and the answer comes back as a message on the same task: a `data` part naming the question, `{"<interrupt id>": <payload>}`, or plain text when one question is open.
An answer that names a question the task did not ask, or leaves one open, is refused as an invalid-params error and the task stays paused.
A question that expired, or whose record is gone because the pod restarted or the paused task was dropped past the store's budget, fails the task, with `interrupt_expired` or `nothing_to_resume` under `metadata.hopsworks.status`.
A task that is running the action a person approved cannot be cancelled: `CancelTask` is refused and the task finishes.

Do not put a credential in a message: every message is kept in the task's history.
An `auth_required` question describes what is needed in its `metadata`, and the answer is a reference the handler resolves itself, such as the name of a project secret.

### Several tasks on one context

A client may open a second task on a context while the first runs.
Each turn reads the conversation as it was when the turn first read it, and the store keeps every turn's rows together, in the order the turns started.
An agent that wants one task at a time per context sets `AgentApp(a2a=A2AConfig(serialize_context=True))`, with `from hopsworks_agents.protocol.a2a import A2AConfig`, and the next task waits as `SUBMITTED` until the running one ends or pauses.
`A2AConfig` also takes `max_tasks` and `max_task_bytes`, the budget of the task store, and `task_store="memory"`, the only store in this release.

Tasks are kept in memory by the replica that runs them, so `GetTask`, `ListTasks`, `CancelTask`, `SubscribeToTask` and an answer to a question must reach that replica, and `serialize_context` orders tasks within one replica only.
An agent whose tasks are polled, cancelled or paused on a question therefore needs a deployment with one instance for now.

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

Tasks are kept in memory, per replica, and dropped oldest first past a count and a byte budget; the manifest says `task_store: memory` under `capabilities.custom.hopsworks.a2a`, and `a2a: {enabled: false, reason: "sdk_missing"}` when the `a2a-sdk` package is not installed.
Push notifications, card signatures, gRPC, per-agent hostnames and a client for calling other agents from a handler are not in this release.

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
