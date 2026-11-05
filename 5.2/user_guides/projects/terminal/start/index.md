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

**LLM Provider**, under **Start**, shows the provider the terminal's coding agents use; **Subscription**, the default, leaves `claude`, `codex`, `copilot`, `opencode`, `pi` and `hermes` on their own logins.
Clicking it shows the providers as cards, each saying whether its key is saved: Kimi, DeepMind, Berget, Mistral, GLM, Anthropic, OpenAI, Meta and OpenRouter.
For a provider, pick a model or type a model id, enter its API key and press **Save key**, then **Test**, which checks the key against the provider's model list without spending tokens and says whether the model is listed.

The key is saved as a private secret in your Hopsworks account, `llm_<provider>_api_key`, not in the browser; the provider and model are kept in the browser.
When the terminal starts, the key is set as the provider's own variable (for example `KIMI_API_KEY`), and:

- `codex` and `opencode` use the provider and model: every provider is written into `~/.codex/config.toml` as `model_providers.hops-<provider>`, so switching needs only that provider's key, and codex gets the model settings the provider's guide gives, such as Meta's and Kimi's 1M-token context window.
- `claude` uses them for providers with an Anthropic-compatible API (Kimi, GLM, Anthropic, Meta and OpenRouter), through `ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_MODEL` and the model variables each provider's Claude Code guide sets (for Kimi, `kimi-k3[1m]` with its 1M-token context and `kimi-k2.7-code` for the background tier); for the others it keeps its own login.
  An `env` block in `~/.claude/settings.json` overrides these, so the terminal warns at start when it sets any of them.
- `pi` and `hermes`, which only the Python terminal has, take them as follows.
  `pi` uses the provider and model: the provider is written into `~/.pi/agent/models.json` as `hops-<provider>`, and `pi` starts on it unless you pass `--model`, `--provider` or `--models`.
  `hermes` uses the provider and model, set in the managed configuration Hermes Agent reads on top of `~/.hermes/config.yaml`.
  Every provider is there as `custom:hops-<provider>`, so `/model <model> --provider custom:hops-<provider>` switches a session to another provider whose key the terminal has.
  Hermes Agent runs its sessions in a background gateway that the first `hermes` starts, with the environment of that shell, so after exporting another provider's key run `hermes gateway stop` before the next `hermes`.
  While a provider is chosen, `hermes model` cannot save a different default model, because the managed configuration sets it; pick **Subscription** to choose the model in Hermes Agent instead.
- `copilot` keeps its GitHub login.

A provider with no saved key disables **Start** until you save one or pick **Subscription**.
