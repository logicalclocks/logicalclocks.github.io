---
description: Start the Hopsworks terminal with its resources, an optional Spark cluster, and the LLM provider its coding agents use
---

# Start the Terminal

The terminal panel opens on a **Start** button, with keyboard focus on it.
Its settings are kept in your browser, so the next visit starts the same terminal without entering them again.

## Resources and Spark Cluster

**Settings**, then **Resources**, sets the terminal's CPU cores and memory, and its GPUs when the cluster has GPU nodes.
With more than 0 GPUs the GPU terminal starts; otherwise the Python terminal.
While a terminal runs, **Apply & Restart** restarts it with the new resources.

**Settings**, then **Spark Cluster**, starts a Spark cluster with the terminal when **Start a Spark cluster with the terminal** is checked; it is unchecked by default.
The terminal pod is then the Spark driver, with the driver cores and memory set there, and runs the given number of executors, with Spark Connect optional.
A Spark terminal has no GPUs.

## LLM Provider

**LLM Provider**, under **Start**, shows the provider the terminal's coding agents use; **Subscription**, the default, leaves `claude`, `codex`, `copilot` and `opencode` on their own logins.
Clicking it shows the providers as cards, each saying whether its key is saved: Kimi, DeepMind, Berget, GLM, Anthropic, OpenAI, Meta, OpenRouter and Grok.
For a provider, pick a model or type a model id, enter its API key and press **Save key**, then **Test**, which checks the key against the provider's model list without spending tokens and says whether the model is listed.

The key is saved as a private secret in your Hopsworks account, `llm_<provider>_api_key`, not in the browser; the provider and model are kept in the browser.
When the terminal starts, the key is set as the provider's own variable (for example `KIMI_API_KEY`), and:

- `codex` and `opencode` use the provider and model: every provider is written into `~/.codex/config.toml` as `model_providers.hops-<provider>`, so switching needs only that provider's key, and codex gets the model settings the provider's guide gives, such as Meta's and Kimi's 1M-token context window.
- `claude` uses them for providers with an Anthropic-compatible API (Kimi, GLM, Anthropic, Meta and OpenRouter), through `ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_MODEL` and the model variables each provider's Claude Code guide sets (for Kimi, `kimi-k3[1m]` with its 1M-token context and `kimi-k2.7-code` for the background tier); for the others it keeps its own login.
  An `env` block in `~/.claude/settings.json` overrides these, so the terminal warns at start when it sets any of them.
- `copilot` keeps its GitHub login.

A provider with no saved key disables **Start** until you save one or pick **Subscription**.
