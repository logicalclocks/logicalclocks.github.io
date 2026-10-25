---
description: How to write, deploy and talk to a conversational agent on Hopsworks, and the chat contract it answers by.
---

# How To Run An Agent Deployment

## Introduction

An agent deployment is a long-running service that answers people: a chat assistant, a tool-using agent, or an LLM workflow behind an endpoint.
You write it as ordinary Python with the framework you prefer, such as LangGraph, LlamaIndex, the OpenAI Agents SDK, or none.
Hopsworks runs it, gives it an endpoint, and connects it to the rest of the platform.

An agent built on `AgentApp` answers by the [chat contract][the-chat-contract], a small HTTP contract that tells Hopsworks how to talk to it.
That is what makes everything around the agent work with no per-agent configuration:

- the chat panel in the UI finds the agent, streams its replies and shows its progress;
- the Python client talks to it by name and threads conversations for you;
- traces, feedback, evaluation and memory key on the ids the contract carries, so a turn can be found, judged and replayed afterwards.

For a fire-and-forget run that does a job and exits, use [Agent Tasks][how-to-run-an-agent-task] instead.

## Where to find it in the UI

In the project sidebar, go to **Agents** and then **Agent Deployments**.
Each agent's page shows its status, logs and configuration, a chat panel to talk to it, its traces, and an **Evaluation** tab for its suites, monitors and analysis.

## Write the agent

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

`my_agent` stands for whatever does the work: a LangGraph graph, a LlamaIndex agent, a plain function.
`AgentApp` is a FastAPI application that serves the chat contract around your handler, so the file above is a complete agent.

!!! warning "The entrypoint has to serve"
    Hopsworks runs your entrypoint with `python <file>`.
    Without the `uvicorn.run(...)` block the script defines the app, exits successfully, and the deployment never becomes ready.

## Deploy and manage it

```python
import hopsworks


project = hopsworks.login()
agents = project.get_agent_serving()

agent = agents.deploy_agent(
    "support_agent.py",
    name="support_agent",
    requirements="requirements.txt",
    environment="support_agent",
    tracing={"enabled": True},
)
agent.start()

reply = agent.chat("Where is my order?")
print(reply.text)
```

The entry is a `.py` file, or a directory with a `pyproject.toml` that is built as a package.
`deploy_agent` creates the agent on the first call and updates it on the next ones.
It leaves the agent's running state alone, so after changing the code call `agent.restart()` to roll a running agent onto it.
`requirements` are installed into `environment`, a Python environment of the project that is created when it does not exist yet.

The same lifecycle from the terminal:

```bash
hops agent list                      # what agents exist
hops agent create support_agent.py --name support_agent \
  --requirements requirements.txt --environment support_agent
hops agent start support_agent       # waits until it is running
hops agent info support_agent        # status, endpoint, source and commit
hops agent logs support_agent        # startup and request errors
hops agent stop support_agent
hops agent delete support_agent --yes
```

Run `hops agent list` first to confirm that authentication and serving are reachable.

### Deploy from a Git repository

An agent can be served from a Git repository instead of a project file.
The repository is cloned every time the deployment starts, so a restart picks up whatever the branch points at, and every file beside the entry comes along with it.

Supported providers are GitHub, GitLab and BitBucket.
Configure the provider credentials once under project settings, see [Configure a Git Provider](../../projects/git/configure_git_provider.md).

```python
agent = agents.deploy_agent(
    "src/agent.py",  # a path inside the repository
    name="support_agent",
    git_url="https://github.com/my-org/my-agent.git",
    git_provider="GitHub",
    git_branch="main",
    environment="support_agent",
)
```

The entry is relative to the repository root rather than a HopsFS path.
Without `git_branch` the clone follows the repository's default branch.

### Auto-redeploy on new commits

With `git_auto_redeploy=True`, a Git-backed agent rolls itself onto the branch head whenever a new commit is pushed.
Hopsworks polls the branch and rolls the deployment when it moves, and the running version keeps answering until the new one is ready.
Hopsworks rejects the flag for an agent deployed from a project file, because there is no branch to follow.
A stopped agent is not rolled; it clones the branch head on its next start.

The agent's **Artifact files** card shows the repository, the branch, the commit it is running, and whether auto-redeploy is on.

## The chat contract

You do not implement the contract by hand: `AgentApp` serves these routes around your handler.

| Route | Purpose |
| --- | --- |
| `GET /.well-known/hopsworks-agent.json` | The manifest: what this agent is and what it can do |
| `POST /v1/chat` | One turn, one reply |
| `POST /v1/chat/stream` | The same turn, streamed as server-sent events |
| `GET /health` | Liveness, the process is up |
| `GET /ready` | Readiness, a handler is registered and memory, if configured, is reachable |

### The manifest

The manifest is how a client discovers an agent rather than assuming it.
It carries the agent's name, description and version, the welcome message and suggested prompts the chat panel shows, the modalities it accepts and returns, the routes it serves, and its capabilities.

This is what the agent above publishes, abridged to the keys this page talks about:

```json
{
  "protocol": "hopsworks-agent",
  "agent": {
    "name": "Support agent",
    "description": "Answers questions about orders"
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
    "suggested_prompts": ["Where is my order?"]
  }
}
```

Each capability is read by something.
The chat panel hides the stream toggle, the transcript view and the feedback control when they are false, and the evaluation runner refuses to grade an agent whose `trace_correlation` is false.
Registering a `@agent_app.stream` handler turns `streaming` on and adds a `stream` endpoint, and configuring [memory][agent-memory] turns `conversation_history` on.

### One turn

A request carries the new message and, optionally, the conversation it belongs to and who it is for.
A reply carries the ids, the message, and what the turn cost:

```json
{
  "id": "response_01HZ...",
  "conversation_id": "conv_01HZ...",
  "message": {"id": "msg_01HZ...", "role": "assistant", "content": []},
  "usage": {"input_tokens": 13, "output_tokens": 7},
  "status": "completed"
}
```

In the handler, `request.text` is the message text, and `request.to_framework_messages()` returns the `[{"role", "content"}]` shape that LangChain, LangGraph and LlamaIndex accept.
`request.conversation_id` is always set, generated on the first turn, so it can be passed straight to a LangGraph checkpointer or a LlamaIndex chat store as a thread id.
Returning a plain `str` from the handler is shorthand for `AgentResponse.text(...)`.

### Conversations

The request carries only the new message.
Pass the `conversation_id` from a reply into the next request and the turns belong to one conversation; leave it out and a new conversation starts.
With [memory][agent-memory] configured, Hopsworks keeps the transcript and hands the handler the recent turns.
Without it, the conversation id is a thread key your own framework uses.

### Streaming

Register an async generator and the agent streams:

```python
@agent_app.stream
async def stream(request):
    async for delta in my_agent.astream(request.text):
        yield delta
```

`/v1/chat/stream` then emits the reply as it is produced, and `/v1/chat` still works by collecting the stream.
An agent that registers only a `@chat` handler still answers the streaming route, as a single completed event, so a caller never has to ask which handler was written.

### Refusals

Raise `AgentError` for anything the agent declines to do:

```python
from hopsworks_agents.protocol import AgentError


@agent_app.chat
async def chat(request):
    if not request.text:
        raise AgentError("Say something first.", code="empty_message", status_code=400)
    return await my_agent.ainvoke(request.text)
```

The caller receives the error in `detail`, with a code it can branch on, a message for a person, and whether a retry is worth it, under the handler's `status_code`.
That status defaults to `500`, so pass a 4xx for anything the agent declined rather than failed at.
A client tells a refusal from a breakage by that status, and an evaluation run uses the same distinction when it decides whether the agent failed a task or did not answer it.

### Who a turn is for

A turn may name the person it is for:

```python
reply = agent.chat("Where is my order?", subject="customer-7")
```

The subject travels with each request rather than with the deployment, because one deployment serves everybody, and it is what long-term memory is keyed by.
A turn that names nobody falls back to its own conversation, and `ctx.subject_source` says which happened: `client` when the caller named someone, `conversation` when it fell back, and `app` when the agent worked it out during the turn.

!!! warning "Identification, not authentication"
    The endpoint authenticates whoever calls the agent, not the person using it.
    A subject is only as trustworthy as whatever your agent derived it from, so do not treat it as proof of identity.

### Progress events

With `AgentApp(tool_events=True)`, the steps an agent takes reach the caller as progress chips while it works:

```python
@agent_app.chat
async def chat(request, ctx):
    await ctx.emit_event("retrieve", status="running", event_id="step-1")
    answer = await my_agent.ainvoke(request.text)
    await ctx.emit_event("retrieve", status="done", event_id="step-1")
    return AgentResponse.text(text=answer)
```

Pass the same `event_id` for a step's start and end, so the client shows one chip that updates rather than two.
When tracing is on and the framework is instrumented, tool calls are reported this way with no code in the agent.

### The handler context

Declare a second parameter and the SDK passes the turn's context:

```python
@agent_app.chat
async def chat(request, ctx):
    ctx.logger.info("turn for %s", ctx.conversation_id)
    return AgentResponse.text(text="ok")
```

`ctx` exposes the conversation, message and turn ids, the deployment id, the subject, a logger, and `emit_event`.
When the deployment configures memory it also exposes `history`, `summary`, `state()`, `recall`, `remember`, `forget` and `system_context()`, see [Agent Memory][agent-memory].

### Talking to an agent from Python

```python
agent = agents.get_agent("support_agent")
print(agent.manifest()["capabilities"])

reply = agent.chat("Where is my order?", subject="customer-7")
print(reply.text, reply.conversation_id, reply.trace_id)

agent.chat(
    "And the second one?",
    conversation_id=reply.conversation_id,
    subject="customer-7",
)

for frame in agent.chat_stream("Tell me more").events():
    print(frame.type, frame.text or "")
```

`reply.trace_id` is the thread back to everything else: the turn's trace, the feedback given on it, and the evaluation trials that replayed it.
`chat` waits 120 seconds by default; pass `timeout=` for an agent whose turns take longer.

## Tracing

With `tracing={"enabled": True}`, every turn is traced with OpenTelemetry: the turn, each model call with its tokens, and each tool call with its arguments and result.
Hopsworks injects the `OTEL_EXPORTER_OTLP_*` settings into the deployment, so the agent needs no exporter configuration.
The traces appear on the agent's page, and feedback, evaluation and monitoring read them.

The first traced deployment in a project creates four feature groups in its feature store:

- `otel_spans`, root spans and trace summary fields;
- `otel_span_attributes`, span attributes as key-value pairs;
- `otel_events`, span events;
- `otel_event_attributes`, event attributes as key-value pairs.

`otel_tracing_storage` chooses where traces are written:

- `online`, the default, writes them to the online store, where the UI reads them;
- `offline` writes them only offline, so the UI shows no trace summaries, but they can be read from the offline feature groups with the Python API;
- `both` writes them to both, so they show in the UI and are kept cost-effectively for long-term retention, which is the recommended choice for a production agent.

Set the model's prices so each trace carries its cost:

```python
agent = agents.deploy_agent(
    "support_agent.py",
    name="support_agent",
    tracing={
        "enabled": True,
        "otel_tracing_storage": "both",
        "input_token_price_per_million_tokens": 3.0,
        "output_token_price_per_million_tokens": 15.0,
    },
)
```

Without prices every turn reports a cost of zero.

### Finding a trace

The **Traces** card on the agent's page lists the most recent traces, grouped by conversation, with their session, subject, status and execution time.
To filter the list, pick the field to search in the dropdown beside the search box and type a value:

- **Input or output** matches words said in the conversation, by the person or by the agent;
- **Subject** matches the person a turn was for, exactly, so a partial value finds nothing;
- **Session** matches a conversation id;
- **Trace ID** matches one trace.

Clicking a subject or a session in the list fills in the same search, so one click shows every conversation with that person, or every turn of that conversation.
Changing the field clears the box, because a value typed for one field rarely means anything in another.

Once a trace is open, the search box above its span tree filters the spans by any of their fields: name, type, status, messages, attributes and events.
A span that matches keeps its ancestors in view, so it stays in context.

The same search is available from Python:

```python
for trace in agent.traces(search="customer-7", search_field="subject", limit=20):
    print(trace.trace_id, trace.session_id, trace.status_code)
```

`search_field` is `messages` (the default), `subject`, `session_id` or `trace_id`.

## Next steps

- [Agent Memory][agent-memory]: conversation history, a rolling summary, facts that outlive a conversation, and search over earlier conversations.
- [Feedback][feedback-on-what-an-agent-answered]: verdicts on what the agent answered, from reviewers and from end users.
- [Evaluation][evaluating-an-agent]: suites of tasks graded by checks, and the gate a release reads.
- [Monitoring][monitoring-live-traffic]: grading the traffic the agent served, on a schedule.
- [Failure Analysis][from-feedback-to-a-regression-suite]: turning failures into regression tasks.

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-method"></code> [`Project.get_agent_serving`][hopsworks_common.project.Project.get_agent_serving]
    - <code class="doc-symbol doc-symbol-method"></code> [`ModelServing.deploy_agent`][hsml.model_serving.ModelServing.deploy_agent]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>
