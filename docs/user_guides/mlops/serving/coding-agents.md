---
description: Documentation on how to use coding agents such as opencode, Codex, Claude Code and Copilot CLI with an LLM deployed in Hopsworks, from the Terminal or from your own machine
---

# Use coding agents with Hopsworks LLMs { #serving-coding-agents }

## Introduction

A vLLM deployment in Hopsworks serves the three APIs that coding agents use: Chat Completions, Responses and Anthropic Messages.
A coding agent only needs a base URL, an API key and the name of the deployment as the model.
This guide lists what the deployment needs, the two routes an agent can take, and the configuration of each agent.
Use the [Terminal][terminal] with the provider **This project** to have the agents configured for you.

## Requirements for the deployment

- The deployment is a **vLLM** deployment in **Standard mode**.
  Knative mode deployments do not serve these routes as described here.
- **Tool calling** is enabled in its vLLM configuration file.
  Coding agents work through tool calls, and vLLM only returns them when `enable_auto_tool_choice` is `true` and a `tool_call_parser` that matches the model family is set:

    ```yaml
    enable_auto_tool_choice: true
    tool_call_parser: qwen3_coder
    max_model_len: 65536
    gpu_memory_utilization: 0.92
    ```

    When Hopsworks generates the vLLM configuration file of a model, from a Hugging Face import or from the configuration generator, it adds `enable_auto_tool_choice` and `tool_call_parser` for the model families it knows.
    A value that the file already sets is kept.
    The families and parsers are Qwen3-Coder (`qwen3_coder`), Qwen2.5 and Qwen3 (`hermes`), Llama 3.x (`llama3_json`), Mistral and Devstral (`mistral`), gpt-oss (`openai`, with `reasoning_parser: openai_gptoss`) and GLM-4.5 and later (`glm45`, with `reasoning_parser: glm45`).
    Only Qwen3-Coder is verified end to end with the agents on this page; the others follow the [vLLM tool calling documentation](https://docs.vllm.ai/en/v0.28.0/features/tool_calling.html) and are unverified.
    For any other model, and for a configuration file that already exists, set the two keys yourself.
- The **context window** is large.
    Agents send the system prompt, the tool schemas and the history on every turn, and a short task can reach tens of thousands of input tokens.
    Set `max_model_len` accordingly (65536 fits Qwen3-Coder-30B-A3B in FP8 on one 48 GB GPU), and tell the agent the window as shown in the recipes below.

See [Server configuration file][server-configuration-file] for the configuration file.

## The two routes { #serving-coding-agents-routes }

An agent reaches a deployment through the LLM gateway or through the deployment's own path.
`<inference endpoint>` is the address of the Hopsworks inference endpoint, and `<project>` the namespace of the project.

| | LLM gateway route | Deployment route |
| --- | --- | --- |
| OpenAI base URL | `<inference endpoint>/v1/<project>/v1` | `<inference endpoint>/v1/<project>/<deployment>/v1` |
| Anthropic base URL | `<inference endpoint>/v1/<project>/v1/anthropic` | `<inference endpoint>/v1/<project>/<deployment>` |
| Model | the deployment name, in the `model` field | the deployment name |
| Rate limits | yes | no |
| Usage attributed per user | yes | no |
| Authorization | project members, and external users with a grant on the deployment | the same |
| vLLM version | any | v0.28.0 or later for the Anthropic API |

The LLM gateway route is served by the [Agent Router][agent-router].
It applies when the cluster publishes the LLM gateway, the deployment is served by it, and both [switches][rest-api-llm-gateway] are on: the project switch and the deployment switch.
It answers the Anthropic API by translating it to the OpenAI API of the model server, so Claude Code works through it with any vLLM version.
The `count_tokens` operation of the Anthropic API answers `422` on it, which Claude Code does not need.
The deployment route goes straight to the vLLM server, which serves the Chat Completions, Responses and Anthropic Messages APIs itself, the last one from vLLM v0.28.0.
It does not pass through the Agent Router, so no rate limit applies and no usage is attributed to the user.
Use it for a deployment that the LLM gateway does not serve, for example one with the LLM gateway switch off or with a minimum of 0 instances.

The two routes check the same things: a valid API key with the **serving** scope, and a user that is a member of the project or an external user with a grant on the deployment.
The deployment route does not widen who can reach a deployment.

Both URLs can be read from the Python client, see [Python client][serving-coding-agents-python].

## Credentials { #serving-coding-agents-credentials }

Create an [API key][how-to-create-an-api-key] with the **serving** scope, and send it in one of two headers:

- `Authorization: Bearer <api key>`, which every OpenAI-compatible client and `ANTHROPIC_AUTH_TOKEN` use.
- `x-api-key: <api key>`, which the Anthropic SDK and `ANTHROPIC_API_KEY` use.

A request that carries both headers with different keys is refused with `401`.

## Recipes { #serving-coding-agents-recipes }

The recipes were run against a Qwen3-Coder-30B-A3B-Instruct-FP8 deployment on vLLM v0.28.0, in the Terminal, with the versions in the table.
Each agent completed a two-turn task: read a file, write a script, run it, then change the script in the same session.

| Agent | Version | Protocol | Route tested |
| --- | --- | --- | --- |
| opencode | 1.19.5 | Chat Completions | LLM gateway |
| Codex CLI | 0.166.0 | Responses | LLM gateway |
| Claude Code | 2.1.316 | Anthropic Messages | deployment route, and the LLM gateway through the Agent Router's Anthropic prefix |
| Copilot CLI | 1.0.105 | Chat Completions | LLM gateway |

The variables below are `HOST` for the inference endpoint, `P` for the project namespace, `D` for the deployment name and `KEY` for the API key.
The agents are updated often, and a newer version can differ from what is shown here.
Replace `65536` with the `max_model_len` of the deployment.

### opencode

opencode needs the Chat Completions adapter `@ai-sdk/openai-compatible`.
Put this in `opencode.json`, and export `HOPSWORKS_SERVING_KEY`:

```json
{
  "provider": {
    "hopsworks": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Hopsworks",
      "options": {
        "baseURL": "https://<HOST>/v1/<P>/v1",
        "apiKey": "{env:HOPSWORKS_SERVING_KEY}"
      },
      "models": {
        "<D>": {
          "name": "<D>",
          "tool_call": true,
          "limit": { "context": 65536, "output": 8192 }
        }
      }
    }
  },
  "model": "hopsworks/<D>"
}
```

### Codex CLI

Codex uses the Responses API.
In `~/.codex/config.toml`, the root keys must come before any `[table]`.
Keys added after a table belong to it, and Codex then falls back to its default provider without an error:

```toml
model = "<D>"
model_provider = "hopsworks"
model_context_window = 65536

[model_providers.hopsworks]
name = "Hopsworks"
base_url = "https://<HOST>/v1/<P>/v1"
wire_api = "responses"
env_key = "HOPSWORKS_SERVING_KEY"
```

Codex reads the key from the variable that `env_key` names:

```bash
export HOPSWORKS_SERVING_KEY="<KEY>"
```

### Claude Code

Claude Code uses the Anthropic Messages API.
Set the base URL of the LLM gateway route or of the deployment route, the key, and the deployment as the model of every tier, since Claude Code uses a different model for sub-tasks and for background work:

```bash
export ANTHROPIC_BASE_URL="https://<HOST>/v1/<P>/v1/anthropic"   # or "https://<HOST>/v1/<P>/<D>"
export ANTHROPIC_AUTH_TOKEN="<KEY>"                                # or ANTHROPIC_API_KEY, sent as x-api-key
export ANTHROPIC_MODEL="<D>"
export ANTHROPIC_DEFAULT_OPUS_MODEL="<D>"
export ANTHROPIC_DEFAULT_SONNET_MODEL="<D>"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="<D>"
export CLAUDE_CODE_SUBAGENT_MODEL="<D>"
export CLAUDE_CODE_MAX_CONTEXT_TOKENS=65536
```

Without `CLAUDE_CODE_MAX_CONTEXT_TOKENS`, Claude Code warns that it does not recognize the model and assumes a context window of 200k tokens.
The `env` block of `~/.claude/settings.json` overrides the environment, so a provider or model set there wins over the variables above.
Remove those entries from the file to use the variables.

Claude Code 2.1.318 was run on both routes with `ANTHROPIC_AUTH_TOKEN` and with `ANTHROPIC_API_KEY`.

### Copilot CLI

Copilot CLI takes its own model provider (bring your own key) from environment variables:

```bash
export COPILOT_PROVIDER_BASE_URL="https://<HOST>/v1/<P>/v1"
export COPILOT_PROVIDER_BEARER_TOKEN="<KEY>"
export COPILOT_MODEL="<D>"
export COPILOT_PROVIDER_WIRE_API=completions
export COPILOT_OFFLINE=true
export COPILOT_PROVIDER_MAX_PROMPT_TOKENS=57344
```

These variables were verified on Copilot CLI 1.0.105 and are not part of GitHub's current documentation of provider configuration.
Check the documentation of your version if they have no effect.

### Aider, Cline, Continue and Cursor

!!! warning "Not verified"
    These agents were not run against a Hopsworks deployment.
    They speak the Chat Completions API, which the LLM gateway route serves, so the configuration below is the generic OpenAI-compatible one.

Set an OpenAI-compatible provider with the base URL `https://<HOST>/v1/<P>/v1`, the API key and the deployment name as the model.
For Aider:

```bash
export OPENAI_API_BASE="https://<HOST>/v1/<P>/v1"
export OPENAI_API_KEY="<KEY>"
aider --model openai/<D>
```

Aider cannot be installed in the Terminal image.
Cursor is understood to send the requests of a custom endpoint through its own servers, which a cluster that is only reachable from a private network does not allow; this was not checked.

### pi and Hermes

The Terminal configures pi and Hermes when you choose **This project**: pi through a provider in `~/.pi/agent/models.json`, Hermes through a managed provider configuration.
Outside the Terminal, configure an OpenAI-compatible provider with the base URL of the route and the deployment name as the model, on the Responses API (pi `openai-responses`, Hermes `codex_responses` transport), or on Chat Completions where the Responses API is not available.

## External users { #serving-coding-agents-external }

An external user with a grant on a deployment can call it, but cannot list models: `GET /v1/models` and `GET /anthropic/v1/models` are refused for them.
They set the model name explicitly, and turn off the agent's model discovery where it has one.
Claude Code, for example, needs `ANTHROPIC_MODEL` and the tier variables above.

## The Terminal { #serving-coding-agents-terminal }

When you start a [Terminal][terminal], the LLM provider selector lists **This project**, next to the external providers.
It needs no API key: the Terminal already holds one for the project, and uses it.
Pick a running vLLM deployment of the project from the model list.

Each deployment in the list has a badge with the route it will use:

- **LLM gateway**: the deployment is served by the LLM gateway.
- **Direct: no rate limits**: the deployment is not served by the LLM gateway, and hovering the badge gives the reason, for example that the switch is off for the deployment.

The route is chosen when the Terminal starts, and a request is never retried through the other route after an error.
A change of the switches, or of the deployment's scaling, applies to the next Terminal start.
The Terminal sets `HOPS_LLM_ROUTE` to `llm-gateway` or `direct`.

The provider configures Codex, opencode, Copilot CLI and Claude Code, and pi and Hermes, with the base URLs of the route, the deployment as the model and the context window of the deployment when it is known.
On the direct route, Claude Code is configured only when the deployment runs vLLM v0.28.0 or later.
Otherwise the selector says why, and the other agents still work.

On the direct route, the agents use the Responses API only when the deployment runs vLLM v0.10.0 or later, and Chat Completions otherwise, which Codex does not support.

The agents in the table below completed a two-step coding task with no configuration of their own, on both routes, with Qwen3-Coder-30B-A3B-Instruct-FP8 on vLLM v0.32.0:

| Agent | Version |
| --- | --- |
| Claude Code | 2.1.318 |
| Codex | 0.166.0 |
| opencode | 1.19.5 |
| Copilot CLI | 1.0.105 |
| pi | 1.5.0 |
| Hermes | 0.22.7 |

If `~/.claude/settings.json` sets `ANTHROPIC_` or `CLAUDE_CODE_` variables in its `env` block, they override the provider, and the Terminal prints a warning when it starts.

## Python client { #serving-coding-agents-python }

`ModelServing` and `Deployment` return the base URLs of each route:

```python
ms = project.get_model_serving()

# LLM gateway route
ms.get_openai_url()  # https://<host>/v1/<project>/v1
ms.get_anthropic_url()  # https://<host>/v1/<project>/v1/anthropic

# Deployment route
deployment = ms.get_deployment("my_llm_deployment")
deployment.get_openai_url()  # https://<host>/v1/<project>/<deployment>/v1
deployment.get_anthropic_url()  # https://<host>/v1/<project>/<deployment>
```

`ANTHROPIC_BASE_URL` takes the value of `get_anthropic_url()`.

## TLS

The inference endpoint is served with the certificate of the cluster's Istio ingress.
When it is self-signed, point the agent at its certificate authority: `NODE_EXTRA_CA_CERTS` for the agents that run on Node.js, such as Claude Code, opencode and Copilot CLI, and `SSL_CERT_FILE` for Python ones such as Aider.
Codex CLI is a native binary: add the certificate authority to the trust store of the operating system.
