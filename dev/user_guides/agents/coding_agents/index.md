# Coding Agents On Hopsworks LLMs { #coding-agents }

## Introduction

Coding agents such as Claude Code, Codex, opencode and Copilot CLI can run on an LLM deployed in your project instead of on an external provider.
A vLLM deployment serves the three APIs they use: Chat Completions, Responses and Anthropic Messages.
An agent needs a base URL, an API key and the deployment name as its model.

The quickest start is the [Terminal][coding-agents-terminal]: choose the **Hopsworks** provider and the agents start configured.
To run an agent on your own machine, see [Configure an agent][coding-agents-recipes].

## Prepare the deployment { #coding-agents-deployment }

A deployment works with coding agents when it:

- is a vLLM deployment;
- has tool calling enabled in its vLLM configuration file;
- has a context window large enough for an agent's prompts.

### Tool calling { #coding-agents-tool-calling }

Agents act through tool calls, and vLLM returns them only when the [configuration file][server-configuration-file] enables them with the parser of the model family:

```yaml
enable_auto_tool_choice: true
tool_call_parser: qwen3_coder
max_model_len: 65536
```

When Hopsworks generates the file, from a Hugging Face import or the configuration generator, it adds these keys for the families below and keeps any value the file already sets.
For a file that already exists, or a model of another family, set them yourself.

| Model family                                          | `tool_call_parser` | `reasoning_parser` |
| ----------------------------------------------------- | ------------------ | ------------------ |
| Qwen3-Coder                                           | `qwen3_coder`      |                    |
| Qwen3.5                                               | `qwen3_coder`      | `qwen3`            |
| Qwen3                                                 | `hermes`           | `qwen3`            |
| Qwen2.5                                               | `hermes`           |                    |
| QwQ, DeepSeek-R1-Distill-Qwen                         | `hermes`           | `deepseek_r1`      |
| Llama 3.1 and later                                   | `llama3_json`      |                    |
| Mistral v0.3, Nemo, Small, Large, Codestral, Devstral | `mistral`          |                    |
| gpt-oss                                               | `openai`           | `openai_gptoss`    |
| GLM-4.5 and later                                     | `glm45`            | `glm45`            |

Qwen3-Coder is verified end to end with the agents on this page.
The other rows follow the [vLLM tool calling documentation](https://docs.vllm.ai/en/v0.28.0/features/tool_calling.html).

### Context window { #coding-agents-context-window }

Agents send their system prompt, tool schemas and history on every turn, so a short task can already reach tens of thousands of input tokens.
Set `max_model_len` as large as the GPU memory allows: 65536 fits Qwen3-Coder-30B-A3B in FP8 on one 48 GB GPU.
Claude Code and Copilot CLI need at least 32768 tokens, because their system prompt and tool schemas alone take 11k to 14k.

## Routes { #coding-agents-routes }

An agent reaches the deployment through the project's [LLM Gateway][llm-gateway] or directly, on the deployment's own path.
In the URLs below, `<host>` is the Hopsworks inference endpoint, `<project>` the project namespace and `<deployment>` the deployment name.

### LLM Gateway { #coding-agents-llm-gateway }

```text
OpenAI:    https://<host>/v1/<project>/v1
Anthropic: https://<host>/v1/<project>/v1/anthropic
```

The LLM Gateway applies the project's rate limits and attributes token usage to each user.
It translates the Anthropic API to the OpenAI API of the model server, so Claude Code works with any vLLM version.
The Anthropic `count_tokens` operation answers `422`, which Claude Code does not need.

The LLM Gateway serves a deployment when the cluster has it and both its project and deployment [switches][rest-api-llm-gateway] are on.
A deployment in Knative mode or one that scales to zero is not served by it.

### Direct { #coding-agents-direct }

```text
OpenAI:    https://<host>/v1/<project>/<deployment>/v1
Anthropic: https://<host>/v1/<project>/<deployment>
```

The direct route goes straight to the vLLM server, with no rate limits and no per-user usage.
Use it for a deployment that the LLM Gateway does not serve.
Claude Code needs vLLM v0.28.0 or later on this route, the first version it was verified with.

## Access { #coding-agents-access }

Both routes accept the same callers: members of the project, and external users whose groups have [external access][serving-external-access] to the deployment.
Each request needs an [API key][how-to-create-an-api-key] with the **serving** scope, in one of two headers:

- `Authorization: Bearer <key>`, which OpenAI-compatible clients and Claude Code's `ANTHROPIC_AUTH_TOKEN` send.
- `x-api-key: <key>`, which the Anthropic SDK and Claude Code's `ANTHROPIC_API_KEY` send.

Set only one of the two: a request carrying a different API key in each header is refused with `401`.

External users cannot list models, so `GET /v1/models` answers `403` for them.
They set the model explicitly and turn off model discovery in agents that have it.

## In the Terminal { #coding-agents-terminal }

When you [start a Terminal][start-the-terminal], choose **Hopsworks** as the LLM provider and pick a running vLLM deployment of the project.
No API key is needed, because the Terminal already holds one.
Claude Code, Codex, opencode, Copilot CLI, pi and Hermes then start configured for the deployment and its context window.

Each deployment in the list shows the route the agents will take:

- **LLM gateway**: the agents go through the LLM Gateway.
- **Direct: no rate limits**: the LLM Gateway does not serve the deployment, so the agents call it directly.

The route is chosen when the Terminal starts and exported as `HOPS_LLM_ROUTE`, `llm-gateway` or `direct`.
A change to the switches or to the deployment's scaling applies at the next start.

Some deployments do not suit every agent, and the selector says when an agent is left unconfigured:

- Without tool calling, the deployment is listed with the reason and the Terminal does not start on it.
- Claude Code needs a known context window of at least 32768 tokens, and vLLM v0.28.0 or later on the direct route.
- Copilot CLI needs a context window of at least 32768 tokens.
- opencode, pi and Copilot CLI need a known context window, since they would otherwise ask for more output than a small window holds.
- Codex needs the Responses API, which vLLM streams tool calls on from v0.18.0; with an older version Codex keeps its own login, and pi and Hermes use Chat Completions instead.

pi gets a provider named `hops-hopsworks-<project>` in `~/.pi/agent/models.json`, so Terminals in different projects keep their own.
If the `env` block of `~/.claude/settings.json` sets `ANTHROPIC_` or `CLAUDE_CODE_` variables, they override the provider, and the Terminal warns about it when it starts.

## Configure an agent { #coding-agents-recipes }

On your own machine, configure the agent with a base URL from [Routes][coding-agents-routes] and an API key.
The examples use the LLM Gateway route, with `<key>` for the API key, and `65536` stands for the deployment's `max_model_len`.
Agents change often, so a newer version can differ from what is shown here; the [verified versions][coding-agents-verified] are listed below.

### Claude Code

Claude Code uses the Anthropic Messages API.
Set the deployment as the model of every tier, since Claude Code uses other models for sub-agents and background work:

```bash
export ANTHROPIC_BASE_URL="https://<host>/v1/<project>/v1/anthropic"
export ANTHROPIC_AUTH_TOKEN="<key>"
export ANTHROPIC_MODEL="<deployment>"
export ANTHROPIC_DEFAULT_OPUS_MODEL="<deployment>"
export ANTHROPIC_DEFAULT_SONNET_MODEL="<deployment>"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="<deployment>"
export ANTHROPIC_DEFAULT_FABLE_MODEL="<deployment>"
export CLAUDE_CODE_SUBAGENT_MODEL="<deployment>"
export CLAUDE_CODE_MAX_CONTEXT_TOKENS=65536
export CLAUDE_CODE_MAX_OUTPUT_TOKENS=16384
```

Without `CLAUDE_CODE_MAX_CONTEXT_TOKENS`, Claude Code assumes a 200k-token window.
`CLAUDE_CODE_MAX_OUTPUT_TOKENS` leaves room for the prompt, because vLLM refuses a request whose `max_tokens` does not fit in the window, and v0.20 to v0.28 count the prompt too.
The Terminal sets it to a quarter of the window, up to 32768.

The `env` block of `~/.claude/settings.json` overrides these variables, so remove any provider or model entries from it.

### Codex CLI

Codex uses the Responses API.
In `~/.codex/config.toml`, put the root keys before any `[table]`: a key after a table belongs to it, and Codex then silently falls back to its default provider.

```toml
model = "<deployment>"
model_provider = "hopsworks"
model_context_window = 65536

[model_providers.hopsworks]
name = "Hopsworks"
base_url = "https://<host>/v1/<project>/v1"
wire_api = "responses"
env_key = "HOPSWORKS_SERVING_KEY"
```

Codex reads the API key from the variable that `env_key` names:

```bash
export HOPSWORKS_SERVING_KEY="<key>"
```

### opencode

opencode uses Chat Completions through the `@ai-sdk/openai-compatible` adapter.
Put this in `opencode.json` and export `HOPSWORKS_SERVING_KEY`:

```json
{
  "provider": {
    "hopsworks": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Hopsworks",
      "options": {
        "baseURL": "https://<host>/v1/<project>/v1",
        "apiKey": "{env:HOPSWORKS_SERVING_KEY}"
      },
      "models": {
        "<deployment>": {
          "name": "<deployment>",
          "tool_call": true,
          "limit": { "context": 65536, "output": 8192 }
        }
      }
    }
  },
  "model": "hopsworks/<deployment>"
}
```

### Copilot CLI

Copilot CLI takes a model provider of your own from environment variables:

```bash
export COPILOT_PROVIDER_BASE_URL="https://<host>/v1/<project>/v1"
export COPILOT_PROVIDER_BEARER_TOKEN="<key>"
export COPILOT_MODEL="<deployment>"
export COPILOT_OFFLINE=true
export COPILOT_PROVIDER_MAX_PROMPT_TOKENS=57344
```

`COPILOT_PROVIDER_MAX_PROMPT_TOKENS` is the context window minus the tokens kept for the answer, here 65536 - 8192.
GitHub documents this variable and `COPILOT_PROVIDER_BEARER_TOKEN` only as their `providers.json` equivalents, `maxPromptTokens` and `bearerToken`, so check the documentation of your version if they have no effect.

### pi and Hermes

Configure an OpenAI-compatible provider with a base URL from [Routes][coding-agents-routes] and the deployment as the model.
Use the Responses API (pi `openai-responses`, Hermes `codex_responses`), or Chat Completions with vLLM older than v0.18.0.

### Other agents

!!! warning "Not verified"
Aider, Cline, Continue and Cursor were not run against a Hopsworks deployment.
They use the Chat Completions API, so the generic OpenAI-compatible configuration below should apply.

Set an OpenAI-compatible provider with the base URL `https://<host>/v1/<project>/v1`, the API key, and the deployment as the model.
For Aider:

```bash
export OPENAI_API_BASE="https://<host>/v1/<project>/v1"
export OPENAI_API_KEY="<key>"
aider --model openai/<deployment>
```

Aider cannot be installed in the Terminal image.
Cursor is reported to send the requests of a custom endpoint through its own servers, which cannot reach a cluster on a private network.

## Python client { #coding-agents-python }

`ModelServing` returns the base URLs of the LLM Gateway route, and `Deployment` those of the direct route:

```python
ms = project.get_model_serving()

ms.get_openai_url()  # https://<host>/v1/<project>/v1
ms.get_anthropic_url()  # https://<host>/v1/<project>/v1/anthropic

deployment = ms.get_deployment("my_llm_deployment")
deployment.get_openai_url()  # https://<host>/v1/<project>/<deployment>/v1
deployment.get_anthropic_url()  # https://<host>/v1/<project>/<deployment>
```

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-class"></code> [`ModelServing`][hsml.model_serving.ModelServing]
        - <code class="doc-symbol doc-symbol-method"></code> [`get_openai_url`][hsml.model_serving.ModelServing.get_openai_url]
        - <code class="doc-symbol doc-symbol-method"></code> [`get_anthropic_url`][hsml.model_serving.ModelServing.get_anthropic_url]
    - <code class="doc-symbol doc-symbol-class"></code> [`Deployment`][hsml.deployment.Deployment]
        - <code class="doc-symbol doc-symbol-method"></code> [`get_openai_url`][hsml.deployment.Deployment.get_openai_url]
        - <code class="doc-symbol doc-symbol-method"></code> [`get_anthropic_url`][hsml.deployment.Deployment.get_anthropic_url]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>

## TLS { #coding-agents-tls }

When the inference endpoint uses a self-signed certificate, point the agent at the cluster's certificate authority:

- `NODE_EXTRA_CA_CERTS` for agents that run on Node.js, such as Claude Code, opencode and Copilot CLI.
- `SSL_CERT_FILE` for Python agents, such as Aider.
- The operating system's trust store for Codex CLI, which is a native binary.

## Verified versions { #coding-agents-verified }

Each agent below completed a two-step coding task, configured by the Terminal, on both routes: read a file, write and run a script, then change it in the same session.
The deployment ran Qwen3-Coder-30B-A3B-Instruct-FP8 on vLLM v0.32.0.

| Agent       | Version | API                |
| ----------- | ------- | ------------------ |
| Claude Code | 2.1.318 | Anthropic Messages |
| Codex CLI   | 0.166.0 | Responses          |
| opencode    | 1.19.5  | Chat Completions   |
| Copilot CLI | 1.0.105 | Chat Completions   |
| pi          | 1.5.0   | Responses          |
| Hermes      | 0.22.7  | Responses          |

The configurations under [Configure an agent][coding-agents-recipes] were first run on vLLM v0.28.0.
