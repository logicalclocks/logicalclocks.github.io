---
description: How to write, deploy and talk to a conversational agent on Hopsworks, and the AG-UI chat contract it answers by.
---

# How To Run An Agent Deployment

## Introduction

An agent deployment is a long-running service that answers people: a chat assistant, a tool-using agent, or an LLM workflow behind an endpoint.
You write it as ordinary Python with the framework you prefer, such as LangGraph, LlamaIndex, the OpenAI Agents SDK, or none.
Hopsworks runs it, gives it an endpoint, and connects it to the rest of the platform.

An agent built on `AgentApp` answers by the [chat contract][the-chat-contract]: AG-UI, the open agent–user protocol, with a few Hopsworks extensions.
That is what makes everything around the agent work with no per-agent configuration:

- the chat panel in the UI finds the agent, streams its replies and shows its progress;
- the Python client talks to it by name and threads conversations for you;
- traces, feedback, evaluation and memory key on the ids the contract carries, so a turn can be found, judged and replayed afterwards.

For a fire-and-forget run that does a job and exits, use [Agent Tasks][how-to-run-an-agent-task] instead.

## Where to find it in the UI

In the project sidebar, go to **Agents** and then **Agent Deployments**.
Each agent's page shows its status, logs and configuration, its traces, and an **Evaluation** tab for its suites, monitors and analysis.
**Chat in panel** at the top opens a chat panel beside the page to talk to it, and **Open in chat app** opens its [chat app][share-an-agent-through-a-chat-app].

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

An agent built on `AgentApp` speaks [AG-UI](https://docs.ag-ui.com), the open protocol between an agent and the interface a person uses.
Any AG-UI client, such as a [CopilotKit](https://www.copilotkit.ai) page, can talk to it with no adapter, and so do the Hopsworks chat panel and Python client.
What Hopsworks adds rides in AG-UI's own extension points, under a `hopsworks` key, so a client that knows nothing of it ignores it.

You do not implement the contract by hand: `AgentApp` serves these routes around your handler.

| Route | Purpose |
| --- | --- |
| `GET /.well-known/hopsworks-agent.json` | The manifest: what this agent is and what it can do |
| `POST /v1/run` | One AG-UI run: a `RunAgentInput` in, AG-UI events out as server-sent events |
| `POST /v1/chat` | The same turn as one JSON reply, for a caller that does not stream |
| `GET /health` | Liveness, the process is up |
| `GET /ready` | Readiness, a handler is registered and memory, if configured, is reachable |

### The manifest

AG-UI has no way for a client to discover an agent, so the manifest is how the chat panel finds it.
It carries the agent's name and description, the welcome message and suggested prompts the chat panel shows, the routes it serves, and its capabilities.
The capabilities are AG-UI's `AgentCapabilities`, and what only Hopsworks reads is under `capabilities.custom.hopsworks`.

This is what the agent above publishes, abridged to the keys this page talks about:

```json
{
  "protocol": "ag-ui",
  "protocol_version": "1.0",
  "agent": {"name": "Support agent", "description": "Answers questions about orders"},
  "endpoints": {"run": "/v1/run", "chat": "/v1/chat", "feedback": "/v1/feedback"},
  "capabilities": {
    "transport": {"streaming": true},
    "humanInTheLoop": {"feedback": true},
    "custom": {
      "hopsworks": {
        "streaming": false,
        "conversation_history": false,
        "tool_events": false,
        "feedback": true,
        "trace_correlation": false
      }
    }
  },
  "ui": {"welcome_message": "How can I help?", "suggested_prompts": ["Where is my order?"]}
}
```

Each Hopsworks capability is read by something.
`streaming` says the answer arrives token by token rather than whole, which is what the chat panel's stream toggle is about.
The chat panel hides the transcript view and the feedback control when theirs are false, and the evaluation runner refuses to grade an agent whose `trace_correlation` is false.
Registering a `@agent_app.stream` handler turns `streaming` on, and configuring [memory][agent-memory] turns `conversation_history` on.

### One run

A run sends the new message, as an AG-UI `RunAgentInput`:

```json
{
  "threadId": "conv_01HZ...",
  "runId": "run_01HZ...",
  "messages": [{"id": "msg_1", "role": "user", "content": "Where is my order?"}],
  "tools": [],
  "context": [],
  "forwardedProps": {"hopsworks": {"subject": "customer-7"}}
}
```

The reply is a stream of AG-UI events:

| Event | What it carries |
| --- | --- |
| `RUN_STARTED` | The thread and the run, and the trace id under `metadata.hopsworks` |
| `TEXT_MESSAGE_START`, `_CONTENT`, `_END` | The answer, piece by piece |
| `TOOL_CALL_START`, `_ARGS`, `_END`, `_RESULT` | A tool call the agent made, with its arguments and its result |
| `STEP_STARTED`, `STEP_FINISHED` | A step the agent reported, see [progress events][progress-events] |
| `CUSTOM` named `hopsworks.media` | An image, file or audio part of the answer |
| `RUN_FINISHED` | Token usage, and the trace id, subject and citations under `result.hopsworks`, plus `text` when the agent's final answer rewrote the text it streamed; an `outcome` of `interrupt` when the agent [asks a person first][asking-a-person-first] |
| `RUN_ERROR` | Why the run failed, see [refusals][refusals] |

The trace id is in `RUN_STARTED` so that a client still has it when the run fails.

In the handler, `request.text` is the message text, and `request.to_framework_messages()` returns the `[{"role", "content"}]` shape that LangChain, LangGraph and LlamaIndex accept.
`request.conversation_id` is the run's thread, generated on the first turn, so it can be passed straight to a LangGraph checkpointer or a LlamaIndex chat store as a thread id.
Returning a plain `str` from the handler is shorthand for `AgentResponse.text(...)`.

### Conversations

Send the `threadId` from a run's `RUN_STARTED` with the next run, and the turns belong to one conversation; send an empty one and a new conversation starts.
An AG-UI client may also resend the conversation's earlier messages.
With [memory][agent-memory] configured, Hopsworks keeps the transcript, hands the handler the recent turns, and ignores the resent messages, so a client cannot rewrite what was said.
Without it, the resent messages reach the handler as `request.prior_messages`, and `to_framework_messages()` returns them before the new message.

### Streaming

Register an async generator and the answer streams token by token:

```python
@agent_app.stream
async def stream(request):
    async for delta in my_agent.astream(request.text):
        yield delta
```

Each piece goes out as a `TEXT_MESSAGE_CONTENT` event, and `/v1/chat` still works by collecting the stream.
An agent that registers only a `@chat` handler answers a run with one text message, so a caller never has to ask which handler was written.

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

A run ends in `RUN_ERROR` with the error's `message` and `code`, and with the handler's `status_code` and whether a retry is worth it under `metadata.hopsworks`.
On `/v1/chat` the same error is the HTTP status, with `detail` as the body.
The status defaults to `500`, so pass a 4xx for anything the agent declined rather than failed at.
A client tells a refusal from a breakage by that status, and an evaluation run uses the same distinction when it decides whether the agent failed a task or did not answer it.

### Who a turn is for

A turn may name the person it is for:

```python
reply = agent.chat("Where is my order?", subject="customer-7")
```

On the wire it is `forwardedProps.hopsworks.subject`.
The subject travels with each request rather than with the deployment, because one deployment serves everybody, and it is what long-term memory is keyed by.
A turn that names nobody falls back to its own conversation, and `ctx.subject_source` says which happened: `client` when the caller named someone, `conversation` when it fell back, and `app` when the agent worked it out during the turn.

!!! warning "Identification, not authentication"
    The endpoint authenticates whoever calls the agent, not the person using it.
    A subject is only as trustworthy as whatever your agent derived it from, so do not treat it as proof of identity.

### Asking a person first

An agent can pause a turn to ask a person, and go on with their answer, for an action that should not happen without approval:

```python
@agent_app.chat
async def chat(request, ctx):
    order = await find_order(request.text)
    answer = ctx.interrupt(
        f"Refund {order.amount} to order {order.id}?",
        key=f"refund-{order.id}",
        response_schema={
            "type": "object",
            "properties": {"approved": {"type": "boolean"}},
            "required": ["approved"],
        },
    )
    if answer.cancelled or not answer.payload.get("approved"):
        return "Understood, no refund."
    await refund(order)
    return "Refunded."
```

The first time, `ctx.interrupt` ends the run with an AG-UI interrupt: `RUN_FINISHED` whose `outcome` names the question, its reason and the JSON Schema of the answer.
The chat panel shows it as a card: Approve and Reject for a yes or no question, a form built from the schema otherwise, and Dismiss to decline to answer.
The answer resumes the turn with a new run on the same thread whose `resume` answers the question; the turn runs again from the start, and this time `ctx.interrupt` returns the answer.

- Everything before the call runs again when the turn resumes, so ask before acting, never after.
- `key` names the question the same way on every run of the turn; without it the question is named by its place in the turn.
- The agent keeps the paused turn's request and what it asked, so a resume carries only the answers and the turn runs again with the same message and context. A resume that answers a question that was not asked, or one that has expired, is refused, and so is one on a conversation that is not waiting on a question (answered already): send the message again instead.
- With agent memory, the open questions are stored with it, so any replica can take the answer and a restart forgets nothing; two replicas given the same answer do not both act on it. Without memory they are kept by the replica that asked, and an answer that reaches another one is refused.
- The stored question is deleted once it is answered, when a new message moves the conversation on instead, or when the conversation is deleted.
- A turn may ask several times; each pause asks one question, and the client answers only what is open.
- `answer.cancelled` is a person declining to answer; a refusal to go ahead is an answer with a payload that says so.

From Python, a paused reply has `reply.interrupted` and `reply.interrupts`, and `agent.chat(None, conversation_id=reply.conversation_id, resume={"refund-42": {"approved": True}})` answers it.
In an evaluation run nobody is there to answer: the runner answers from the task context's `interrupt_answers`, by question id, and cancels the rest.

### Progress events

With `AgentApp(tool_events=True)`, what the agent does reaches the caller while it works, and the chat panel shows it as progress chips.
Tool calls need no code: when tracing is on and the framework is instrumented, each tool call goes out as AG-UI tool-call events, with its arguments and its result.
Other steps, such as a retrieval or a plan, the agent reports itself:

```python
@agent_app.chat
async def chat(request, ctx):
    await ctx.emit_event("retrieve", status="running", event_id="step-1")
    answer = await my_agent.ainvoke(request.text)
    await ctx.emit_event("retrieve", status="done", event_id="step-1")
    return AgentResponse.text(text=answer)
```

Each report is an AG-UI `STEP_STARTED` or `STEP_FINISHED` event, with the status, message and data under its `metadata.hopsworks`.
Pass the same `event_id` for a step's start and end, so the client shows one chip that updates rather than two.

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
`request` also carries what the run sent beyond the message: `run_id`, `messages`, `tools`, `state` and `forwarded_props`.

### Talking to an agent from Python

```python
agent = agents.get_agent("support_agent")
print(agent.manifest()["capabilities"]["custom"]["hopsworks"])

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

`chat_stream` sends an AG-UI run and reads its events; each frame keeps the event it came from in `frame.raw`.
`reply.trace_id` is the thread back to everything else: the turn's trace, the feedback given on it, and the evaluation trials that replayed it.
`chat` waits 120 seconds by default; pass `timeout=` for an agent whose turns take longer.

## Share an agent through a chat app

The chat panel is for project members working in Hopsworks.
To put an agent in front of other people, such as support staff, a pilot customer, or a colleague trying it out, create its **chat app**: a ready-made chat page, run as a Hopsworks [app][apps], that speaks AG-UI to the agent.

Create it in any of three places:

- tick **Create a chat app** when you deploy the agent;
- select **Open in chat app** at the top of the agent's page, next to **Chat in panel**: it creates the app when the agent has none, and afterwards opens it in a new tab;
- call it from Python:

```python
agent = project.get_agent_serving().get_agent("support_agent")
app = agent.create_chat_app()  # named support_agent_chat; pass name= for another
print(app.app_url)

agent.chat_app()  # the app, or None when the agent has none
```

The app streams the agent's replies and shows its tool calls, takes attachments, shows the agent's questions as an approval card, and lets people rate a reply.
Its page is [CopilotKit](https://github.com/CopilotKit/CopilotKit)'s open-source chat, served with CopilotKit's runtime by the app itself: nothing is sent to CopilotKit.
It is an ordinary app otherwise: its logs, settings and resources are on its page under **Apps**, and it scales to zero when nobody uses it.

**Who can open it.**
Project members open it with their Hopsworks login.
To share it with people who have no Hopsworks account, turn on the app's public link on its page, or with `app.make_public()`; anyone holding the link can then chat with the agent, until you turn the link off.
Public links need public apps to be enabled on the cluster.

**Who is chatting.**
The app decides, never the page.
A project member chats as their Hopsworks user, the same subject the chat panel uses, so the agent's [memory][agent-memory] of them is the same in both, and the page says who they are signed in as.
Hopsworks tells the app who the member is with a signature only the app can check, so nobody else can claim to be them.
Anyone who opened the public link is anonymous: the app sets a cookie with a random id in their browser and derives their subject from it, so each visitor has their own memory.
Conversations belong to whoever started them: the app refuses a turn on anyone else's conversation.
No serving key reaches the browser: the app's server talks to the agent inside the cluster, and only forwards turns and feedback, never the routes that read or erase memory.

**What people thought of the answers.**
A thumbs up or down given in the app reaches the agent's **Feedback** tab marked **via chat app**, and `Feedback.given_via` is `chat-app` in Python, so you can tell it from feedback given in the chat panel.

**Changing it.**
Set these as the app's environment variables:

| Variable | Effect |
| --- | --- |
| `CHAT_TITLE` | The page title; the agent's name by default |
| `CHAT_WELCOME` | The first thing the page says |
| `CHAT_SHOW_TOOL_CALLS` | `false` hides tool calls and steps from visitors |
| `CHAT_ACCENT_COLOR` | The accent colour, such as `#0b5fff` |
| `CHAT_LOGO_URL` | An `https://` image for the header |
| `CHAT_THEME_DIR` | A folder of the project, such as `Resources/chat-theme`, with your own styles and logo |
| `CHAT_MAX_RUNS_PER_MINUTE` | Turns per visitor per minute; 20 by default |

For a theme folder, upload a `theme.css` and a logo named `logo.svg`, `logo.png`, `logo.jpg` or `logo.webp` to it, set `CHAT_THEME_DIR`, and restart the app.
`theme.css` is loaded after the page's own styles, so it can change anything they set; the page's colours are CSS variables such as `--accent`, `--bg` and `--surface`, so a theme can be as small as one line:

```css
:root { --accent: #0b5fff; --bg: #f4f7ff; }
```

The app's code comes with the platform, so it is updated with Hopsworks rather than copied into your project.
For a page of your own design, write an AG-UI client against [the chat contract][the-chat-contract] instead.

Deleting the agent deletes its chat app.

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
