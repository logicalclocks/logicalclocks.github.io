---
description: Documentation on how to configure and run an Agent Deployment on Hopsworks.
---

# How To Run An Agent Deployment

## Introduction

Agent Deployments are **server-only KServe deployments with no model attached**.
You ship an entry script or package that exposes a predictor, and Hopsworks
serves it behind an endpoint. Use Agent Deployments for interactive agents and
LLM workflows, where the service needs to stay up and answer requests.

If you need a fire-and-forget background run, use [Agent Tasks](../tasks/index.md)
instead.

Common use cases:

- **Interactive assistants** - a chat or tool-using agent that stays online
- **LLM workflows** - a deterministic sequence of retrieval, reasoning, and
  generation steps that you want to expose as a service
- **RAG-backed services** - an agent that reads Feature Store context and uses
  it to answer questions

## Where to find it in the UI

In the project sidebar, go to **Agents** and then **Agent Deployments**.
The list page shows the agent deployments in the project, along with the same
type of detail page you use for model deployments.

## Create and manage an agent deployment

The most common way to create one is with the SDK or the CLI:

```bash
hops agent list
hops agent create my_agent.py --name my_agent --requirements requirements.txt --environment my_agent
hops agent start my_agent
hops agent query my_agent --data '{"prompt": "hello"}'
hops agent logs my_agent
hops agent info my_agent
hops agent stop my_agent
hops agent delete my_agent --yes
```

Use `hops agent list` first to confirm auth and serving are reachable.

```python
import hopsworks

project = hopsworks.login()
ms = project.get_model_serving()

deployment = ms.deploy_agent(
    entry="my_agent.py",                 # .py file or a dir with pyproject.toml
    name="my_agent",
    requirements="requirements.txt",
    environment="my_agent",
    upload_dir="Resources/agents",       # default
)
deployment.start(await_running=600)
print(deployment.predict(inputs={"prompt": "hello"}))
# After editing the code: re-create, then deployment.restart()
```

After creation, the deployment appears in the Agent Deployments list where you
can inspect its status, logs, endpoints, and configuration.

## Small example

The file below shows a compact agent program that uses LlamaIndex, FastAPI,
and OpenTelemetry.

Set `ANTHROPIC_API_KEY` in the deployment environment. Hopsworks injects the
`OTEL_EXPORTER_OTLP_*` environment variables for the deployment, so the
OpenTelemetry exporter can stay configuration-free.

```python
import asyncio
import os

from fastapi import FastAPI
from llama_index.core.agent.workflow import ReActAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.anthropic import Anthropic
from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
import uvicorn


def add(a: float, b: float) -> float:
  """Adds two numbers."""
  return a + b


def subtract(a: float, b: float) -> float:
  """Subtracts two numbers."""
  return a - b


def multiply(a: float, b: float) -> float:
  """Multiplies two numbers."""
  return a * b


def divide(a: float, b: float) -> float:
  """Divides two numbers."""
  if b == 0:
    raise ValueError("Cannot divide by zero.")
  return a / b


def build_tracer_provider():
  endpoint = os.environ.get(
    "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT",
    "http://localhost:4318/v1/traces",
  )

  tracer_provider = trace_sdk.TracerProvider()
  tracer_provider.add_span_processor(
    SimpleSpanProcessor(OTLPSpanExporter(endpoint=endpoint))
  )
  return tracer_provider


class AgentPredictor:
  def __init__(self):
    self.tracer_provider = build_tracer_provider()

    LlamaIndexInstrumentor().instrument(
      tracer_provider=self.tracer_provider
    )

    llm = Anthropic(
      model="claude-haiku-4-5-20251001",
      max_tokens=1024,
      temperature=0.0,
    )

    tools = [
      FunctionTool.from_defaults(add),
      FunctionTool.from_defaults(subtract),
      FunctionTool.from_defaults(multiply),
      FunctionTool.from_defaults(divide),
    ]

    self.agent = ReActAgent(
      tools=tools,
      llm=llm,
    )

  async def _predict_async(self, inputs):
    prompt = inputs.get("prompt", "")
    result = await self.agent.run(prompt)
    return {"answer": str(result)}

  def predict(self, inputs):
    return asyncio.run(self._predict_async(inputs))


predictor = AgentPredictor()

agent_app = FastAPI()

FastAPIInstrumentor.instrument_app(
  agent_app,
  tracer_provider=predictor.tracer_provider,
)


@agent_app.post("/query")
def query(payload: dict):
  return predictor.predict(payload)


if __name__ == "__main__":
  uvicorn.run(agent_app, host="0.0.0.0", port=8080)
```

## Tracing

Agent Deployments can be configured with OpenTelemetry tracing.

When tracing is enabled, Hopsworks automatically provisions four online,
Delta-backed feature groups in the project's Feature Store:

- `otel_spans` - root spans and trace summary fields
- `otel_span_attributes` - span attributes as key-value pairs
- `otel_events` - span events
- `otel_event_attributes` - event attributes as key-value pairs

The Traces UI reads from these feature groups, and the first traced deployment
in a project creates them automatically if they do not already exist.

After that, choose one of these storage modes:

- `online` - the default; writes traces to only online
- `offline` - writes traces to only offline. You will no be able to see the traces summaries in the UI, but you can
  use the hopsworks-api to read the offline feature groups and reconstruct the traces from there.
- `both` - export traces to both online and offline feature groups. This is the recommended option for production deployments, as it allows you to see the traces in the UI and also have them stored cost-effectively for long-term retention.

## Next steps

- Scheduled, non-interactive coding agent: [Agent Tasks](../tasks/index.md)
- Model-backed online predictor: use the Model Deployments guides under MLOps
- Agent-serving dependencies: see the environment guides for cloning Python
  environments and installing requirements
