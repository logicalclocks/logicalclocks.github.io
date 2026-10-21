---
description: The chat contract a conversational agent deployment answers by: the manifest it publishes, the shape of a turn, streaming, threaded conversations, refusals, and who a turn is for.
---

# The Chat Contract For Conversational Agents

## Introduction

An agent deployment can serve anything you like on its endpoint.
A *conversational* agent is one that answers by the chat contract, a small HTTP contract that tells Hopsworks how to talk to it.

Answering by it is what makes the rest of the platform work with no per-agent configuration.
The chat panel in the UI finds the agent, knows whether it streams, and renders its progress and its transcript.
The Python client talks to it by name and threads conversations for you.
Traces, feedback and evaluation key on the ids the contract carries, so a turn can be found, judged and replayed afterwards.

You do not implement the contract by hand.
`AgentApp` is a FastAPI subclass that publishes it for you, and your agent stays ordinary Python.

!!! note "Which kind of agent do I have?"
    An agent that serves `/predict` is a plain agent deployment, reached with `deployment.predict(...)`.
    An agent built on `AgentApp` also speaks this contract, so it is reached with `agent.chat(...)` and by the chat panel.
    Both are created and run the same way, see [How To Run An Agent Deployment][how-to-run-an-agent-deployment].

## The smallest agent that speaks it

Serving an agent needs the `agents` extra, `pip install 'hopsworks[agents]'`.

```python
from hopsworks_agents.protocol import AgentApp, AgentResponse

agent_app = AgentApp(
    name="Support agent",
    description="Answers questions about orders",
    welcome_message="How can I help?",
    suggested_prompts=["Where is my order?"],
)


@agent_app.chat
async def chat(request):
    answer = await my_agent.ainvoke(request.text)
    return AgentResponse.text(text=answer)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(agent_app, host="0.0.0.0", port=8080)
```

Deploy the file as an agent deployment and the chat panel works with nothing further to configure.

!!! warning "The entrypoint has to serve"
    Hopsworks runs your entrypoint with `python <file>`.
    Without the `uvicorn.run(...)` block the script defines the app, exits successfully, and the deployment never becomes ready.

## What the contract is

| Route | Purpose |
| --- | --- |
| `GET /.well-known/hopsworks-agent.json` | The manifest: what this agent is and what it can do |
| `POST /v1/chat` | One turn, one reply |
| `POST /v1/chat/stream` | The same turn, streamed as server-sent events |
| `GET /health` | Liveness, the process is up |
| `GET /ready` | Readiness, a handler is registered and memory, if configured, is reachable |

### The manifest

The manifest is how a client discovers an agent rather than assuming it.
It carries the agent's name, description and version, the welcome message and suggested prompts the panel shows, the modalities it accepts and returns, the routes it serves, and the capabilities it has.

This is what the agent above publishes, abridged to the keys this page talks about.

```json
{
  "protocol": "hopsworks-agent",
  "protocol_version": "1.4",
  "agent": {
    "name": "Support agent",
    "description": "Answers questions about orders",
    "version": "1.0.0",
    "framework": "custom"
  },
  "endpoints": {"chat": "/v1/chat", "feedback": "/v1/feedback"},
  "capabilities": {
    "streaming": false,
    "conversation_history": false,
    "tool_events": false,
    "feedback": true,
    "trace_correlation": false
  },
  "ui": {
    "welcome_message": "How can I help?",
    "suggested_prompts": ["Where is my order?"],
    "allow_markdown": true
  }
}
```

The agent above registers a `chat` handler and nothing else, so most capabilities are reported `false` and `endpoints` has no `stream`.
Registering a `@agent_app.stream` handler adds both; configuring memory turns `conversation_history` on.

Each capability is read by something.
The chat panel hides the stream toggle, the transcript view and the feedback control when they are false, and the evaluation runner refuses to grade an agent whose `trace_correlation` is false.
The routes matter for the same reason: a client that cannot find them falls back to the protocol's defaults, which is how an agent served on a custom path becomes unreachable without an error anywhere.

### One turn

A request carries the new message and, optionally, the conversation it belongs to and who it is for.
A reply carries the ids, the message, and what the turn cost.

```json
{
  "id": "response_01HZ...",
  "conversation_id": "conv_01HZ...",
  "message": {"id": "msg_01HZ...", "role": "assistant", "content": []},
  "citations": [],
  "usage": {"input_tokens": 13, "output_tokens": 7},
  "metadata": {},
  "status": "completed"
}
```

Three things are worth knowing when writing the handler.

`request.conversation_id` is always set, generated on the first turn, so it can be passed straight to a LangGraph checkpointer or a LlamaIndex chat store as a thread id.
`request.text` is the plain message text, and `request.to_framework_messages()` returns the `[{"role", "content"}]` shape that LangChain, LangGraph and LlamaIndex accept.
Returning a plain `str` from the handler is shorthand for `AgentResponse.text(...)`.

### Conversations are threaded server-side

The request carries only the new message.
Pass the `conversation_id` from a reply into the next request and the turns belong to one conversation.
Leave it out and a new conversation starts clean.

What history means depends on whether the deployment configures memory.
Without it, the conversation id is a thread key your own framework uses.
With it, Hopsworks keeps the transcript and hands the handler the recent turns.

### Streaming

Register an async generator and the manifest advertises `streaming: true` automatically.

```python
@agent_app.stream
async def stream(request):
    async for delta in my_agent.astream(request.text):
        yield delta
```

`/v1/chat/stream` then emits the reply as it is produced, and `/v1/chat` still works by collecting the stream.
An agent that registers only a `@chat` handler still answers the streaming route, as a single completed event, so a caller never has to ask which handler was written.

### A refusal arrives as a refusal

Raise `AgentError` for anything the agent declines to do.

```python
from hopsworks_agents.protocol import AgentError


@agent_app.chat
async def chat(request):
    if not request.text:
        raise AgentError("Say something first.", code="empty_message", status_code=400)
```

The caller receives the protocol's error envelope in `detail` — a code it can branch on, a message for a person, and whether a retry is worth it — under the handler's `status_code`.
That status defaults to `500`, so pass a 4xx for anything the agent declined rather than failed at.
A client tells *the agent declined* from *the agent broke* by that status, and an evaluation run uses the same distinction when it decides whether a task failed or the harness did.

### Who a turn is for

A turn may name the person it is for.

```python
reply = agent.chat("where is my order?", subject="customer-7")
```

The subject travels per request rather than per deployment, because one deployment serves everybody.
A turn that names nobody falls back to its own conversation, and `ctx.subject_source` says which happened: `client` when the caller asserted one, `conversation` when it fell back, and `app` when the agent worked it out during the turn.

!!! warning "Identification, not authentication"
    The transport authenticates the agent, not the person using it.
    A subject is only as trustworthy as whatever your agent derived it from, so do not treat it as proof of identity.

## Progress events

With `AgentApp(tool_events=True)`, the steps an agent takes reach the caller as progress chips while it works.

```python
@agent_app.chat
async def chat(request, ctx):
    await ctx.emit_event("retrieve", status="running", event_id="step-1")
    answer = await my_agent.ainvoke(request.text)
    await ctx.emit_event("retrieve", status="done", event_id="step-1")
    return AgentResponse.text(text=answer)
```

Pass the same `event_id` for a step's start and end so the client shows one chip that updates rather than two chips.
When tracing is on and the framework is instrumented, tool events are emitted automatically with no code in the agent.

## The handler context

Declare a second parameter and the SDK passes the turn's context.

```python
@agent_app.chat
async def chat(request, ctx):
    ctx.logger.info("turn for %s", ctx.conversation_id)
    return AgentResponse.text(text="ok")
```

`ctx` exposes the conversation, message and turn ids, the deployment id, a logger, and `emit_event`.
When the deployment configures memory it also exposes `history`, `summary`, `state()`, `recall`, `remember`, `forget` and `system_context()`.

## Calling a conversational agent from Python

```python
import hopsworks


project = hopsworks.login()
agents = project.get_agent_serving()

agent = agents.get_agent("support_agent")
print(agent.manifest()["capabilities"])

reply = agent.chat("where is my order?", subject="customer-7")
print(reply.text, reply.conversation_id, reply.trace_id)

agent.chat(
    "and the second one?",
    conversation_id=reply.conversation_id,
    subject="customer-7",
)

for frame in agent.chat_stream("tell me more").events():
    print(frame.type, frame.text or "")
```

`reply.trace_id` is the thread back to everything else: the turn's trace, the feedback given on it, and the evaluation trials that replayed it.

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-method"></code> [`Project.get_agent_serving`][hopsworks_common.project.Project.get_agent_serving]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>
