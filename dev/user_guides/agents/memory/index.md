# Agent Memory

## Introduction

A conversational agent is only as useful as what it remembers.
Hopsworks keeps a deployment's memory server-side, so an agent gets history, a rolling summary, durable facts and search over past conversations without running a database of its own.

Memory is one store with four tiers, each switched on independently.

| Tier | Holds | Read it with |
| --- | --- | --- |
| Working memory | The turns of this conversation the agent sees verbatim | `ctx.history` |
| Short-term memory | The rest of this conversation, compacted into a rolling summary rather than dropped | `ctx.summary` |
| Semantic memory | Facts the agent decided to keep about a person, across conversations | `ctx.recall`, `ctx.state()` |
| Episodic memory | What was said in that person's earlier conversations | the `search` tool, or `ctx.memory.search(query, subject=ctx.subject)` |

Two terms that look alike are not the same thing.
*Semantic memory* is the facts an agent stores, while *semantic search* is one way episodic memory retrieves past turns.

This guide assumes an agent that speaks the chat contract, see [The Chat Contract For Conversational Agents][the-chat-contract-for-conversational-agents].

## Turning memory on

### From the deployment

A deployment carries a memory policy, set in its form and injected into the agent as `AGENT_MEMORY_CONFIG`.
Nothing is written in the agent for this.

```python
import hopsworks


project = hopsworks.login()
ms = project.get_model_serving()

deployment = ms.deploy_agent(
    entry="my_agent.py",
    name="support_agent",
    environment="support_agent",
    memory={
        "enabled": True,
        "summarize": {"provider": "openai"},
        "long_term": True,
        "search": {"enabled": True},
        "max_messages": 20,
    },
)
```

A policy switches on every tier it does not mention, so `{"enabled": True}` gives semantic and episodic memory as well as the conversation itself.
Set `"long_term": False` to leave semantic memory out.
The summarizer is the exception: there is nothing to fold with until a provider is named.

`"search": {"enabled": False}` turns off *semantic* search: there is no vector store and nothing is embedded.
Episodic memory stays readable, because `search` falls back to a keyword query over the stored turns and the model-facing `search` tool still calls it.
To keep earlier conversations out of an answer altogether, leave the `search` tool out of the agent's tools.

A policy that cannot be honoured in full degrades to the part that can be, and says so in the deployment log, rather than refusing to start.

### In code

An agent can configure its own store instead, which is what you want when the agent is developed outside Hopsworks or needs a summarizer the form does not offer.

```python
from hopsworks_agents.protocol import AgentApp, ManagedMemoryService, openai_summarizer


agent_app = AgentApp(
    name="Support agent",
    memory=ManagedMemoryService(
        summarize=openai_summarizer(),
        long_term=True,
    ),
)
```

**Code wins.** The deployment's policy is applied only when the agent passed no `memory=` of its own, and an explicit `memory=None` stays off however the deployment is configured.
The manifest reports which it was under `capabilities.memory.source`, as `code` or `deployment`.

Inside a deployment `ManagedMemoryService()` needs no arguments: the project database URL comes from the platform-injected environment and the table names are derived from the deployment id.
Outside one, pass any SQLAlchemy URL and install the extra, `pip install 'hopsworks[agents-memory]'`.

!!! warning "Do not keep two sources of truth"
    If your framework already persists conversation state, such as a LangGraph checkpointer or a LlamaIndex chat store, key it by `conversation_id` and leave `memory=` off.
    Two stores holding the same history diverge, and the one the model reads is the one that decides what the agent knows.

## Reading memory in a handler

The platform records turns whether or not the agent reads them.
Switching memory on cannot make an agent use it, so these lines stay yours to write.

```python
@agent_app.chat
async def chat(request, ctx):
    system = MY_PROMPT + ctx.system_context()
    messages = ctx.history + [{"role": "user", "content": request.text}]
    answer = await my_agent.ainvoke(messages, system=system)
    return answer
```

`ctx.system_context()` assembles the rolling summary and this person's stored facts into a block for your system prompt.
It returns an empty string when there is nothing yet, so it is safe to concatenate unconditionally.
The SDK builds it every turn but never places it, because where context belongs is a property of your prompt.

!!! danger "`ctx.history` is not the whole conversation once summarizing is on"
    It is the turns since the last fold.
    Everything older lives in `ctx.summary`, so passing `ctx.history` alone silently drops the compacted part of the conversation.
    Use `ctx.system_context()`, or read both.

In an `async def` handler the memory accessors have awaitable forms, `await ctx.ahistory()`, `await ctx.arecall(...)`, `await ctx.aremember(...)` and `await ctx.aforget(...)`, which keep the event loop free while the store is read.

## Durable facts and their scope

Three scopes decide who a fact belongs to.

```python
ctx.remember("preferred_language", "Swedish")        # the person, across conversations
ctx.remember("cart_id", cart.id, scope="session")    # this conversation only
ctx.recall("cart_id", scope="session")               # one key, None when absent
ctx.forget("cart_id", scope="session")               # one key, or the scope with no key
```

The owner is the point.
`user` scope is keyed by the subject and `session` scope by the conversation, so state written under the wrong one is never read back and never reports an error.

`app` scope is agent-wide and **cannot be written from a turn**.
It is injected into every person's context, so one conversation writing it is how a prompt injection reaches everybody.
Operators write it out of band instead.

A fact written by the agent is recorded as the agent's: cut to the store's cap, given an expiry, and listed as agent-written in the person's own audit view, with a reference to the turn it came from.

### Letting the agent decide what to remember

With long-term memory on, the SDK ships `remember`, `recall`, `forget` and `search` as tools the agent's own model calls when it judges something worth keeping.
There is no extraction model in the SDK guessing on its behalf.

```python
from hopsworks_agents.protocol import memory_tools

agent = create_react_agent(llm, [*my_tools, *memory_tools("langgraph")])
```

The same helper exists for `llamaindex`, `openai_agents`, `claude_agents`, and `plain` functions.
They are registered by you rather than appended to your tool list automatically, because reaching into an arbitrary framework's tools behind your back would be worse than asking.

## Who the memory belongs to

Long-term memory is keyed by the `subject` on the request.
A turn that names nobody falls back to the conversation, so memory degrades to per-conversation durability rather than failing.

An agent that learns who it is talking to mid-conversation can bind the memory to that person with `ctx.rebind_subject(...)`, which restamps the turn so the question and the answer are filed under one person.
From the next turn on, the conversation is already bound and the subject is read back from the store.

!!! warning "A subject is a claim, not a credential"
    The ingress authenticates a project-wide serving key, not a person, so the agent cannot verify a subject.
    It is fine between project members and is not a security boundary.
    An agent that acts on an identity should verify the claim itself before calling `ctx.rebind_subject(...)`.

## What a person can see and erase

With memory configured, the deployment serves routes over its own memory, which is what the chat panel's memory view calls.

| Route | Answers |
| --- | --- |
| `GET /v1/conversations` | Every conversation this deployment holds, with its subject, message count and last activity |
| `GET /v1/conversations/{id}/messages` | The human-facing transcript, including turns that have been folded into the summary |
| `DELETE /v1/conversations/{id}` | Erase a conversation and its session-scoped state |
| `DELETE /v1/conversations/{id}/summary` | Drop the rolling summary and keep the conversation |
| `GET /v1/subjects/{subject}/state` | Every durable fact held about a person, with its provenance and expiry |
| `DELETE /v1/subjects/{subject}/state` | Erase one fact, or everything held about that person |

The transcript route is deliberately not what the model sees.
Once turns are folded they leave `ctx.history` but stay in the transcript, with `summarized_through` marking where the two diverge, so a person reading their own conversation is not shown a gap the agent created for its own convenience.

A summary is written by a model out of what a user typed and then lands in every later system prompt, so a user who talks an agent into a false summary has put it somewhere that outlives the turn.
Deleting it brings the folded turns back and the next fold writes a fresh one.

Erasing a conversation leaves durable facts about the person alone, because starting a new chat must not erase what the agent knows about you.

### Where the access boundary is

The boundary is **the project's agents**.
These routes sit behind the same ingress as chat, and the credential that opens them is a serving key scoped to the project.
Anyone holding it can list the conversations, read any transcript, and delete any conversation or any subject's facts.
A caller entitled to talk to the agent is entitled to its memory.

There is no narrower key: a second serving key is another project-scoped key and opens the same routes.
If a client should not have that reach, such as a browser or a public end-user app holding the key, either put your own service in front of the agent and let it authenticate its own users, or stop serving the routes.

```python
agent_app = AgentApp(name="Support agent", memory_routes=False)
```

The agent still remembers; it no longer answers questions about what it remembers.
The chat panel's memory view and a client's "new session" call go with them, so leave the routes on for an agent whose callers are your own team.

Above that line nothing crosses.
Every statement is filtered by deployment and the embedding feature group is per deployment, so neither another project nor another agent in the same project is reachable, whatever a caller sends.

## Retention

Memory is bounded by default so it does not grow without end.

| Setting | Default | What it bounds |
| --- | --- | --- |
| `max_messages` | 50 | How many of a conversation's messages the agent is handed on a turn |
| `summarize_after_messages` | 20 | When older turns are folded into the summary |
| `keep_recent_messages` | 10 | How many turns a fold leaves verbatim |
| `message_retention_days` | Kept | How long a recorded conversation is kept |
| `state_ttl_days` | 90 | How long an agent-written fact lives unless it is confirmed |
| `max_state_value_chars` | 4096 | The size of one durable value |

Summarizing runs after the reply has streamed and is awaited before the request returns, so it costs request duration every Nth turn and never time to first token.

## Summarizers

A summarizer is any callable taking the previous summary and the turns to fold and returning the new summary, sync or async.
Three are shipped.

```python
from hopsworks_agents.protocol import (
    anthropic_summarizer,
    hopsworks_summarizer,
    openai_summarizer,
)


summarize = openai_summarizer()  # OPENAI_API_KEY, or a Hopsworks secret
summarize = anthropic_summarizer()
summarize = hopsworks_summarizer("my-llm")  # an LLM deployed in this project
```

`openai_summarizer` also speaks to anything with the same chat-completions shape through `base_url`, such as a vLLM or Ollama instance in the cluster, a LiteLLM proxy, or Azure.
`hopsworks_summarizer` needs no key at all: it reaches an LLM deployment in the project through the inference gateway with the credential the agent pod already holds.

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-method"></code> [`ModelServing.deploy_agent`][hsml.model_serving.ModelServing.deploy_agent]
    - <code class="doc-symbol doc-symbol-class"></code> [`DeploymentMemoryConfig`][hsml.deployment_memory_config.DeploymentMemoryConfig]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>
