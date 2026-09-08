---
description: Guide to the Hopsworks CLI, hops, for people, CI pipelines and coding agents.
---

# Hopsworks CLI

`hops` is the Hopsworks command line.
It ships with the Hopsworks Python library, so anywhere the library is installed the command is available.
The same commands run from your laptop, from a CI pipeline, from a coding agent, or inside the [project terminal][terminal], where it is already connected.

--8<-- "user_guides/client_installation/cli/one-cli-two-seats.html"

## Install and connect

Install the library with the `python` profile and the CLI comes with it.
The profile brings the Arrow and Kafka dependencies the data commands (`fg preview`, `fv get`, `sql`) read and write through.

=== "uv"

    ```bash
    uv venv && source .venv/bin/activate
    uv pip install "hopsworks[python]"
    ```

=== "pip"

    ```bash
    python3 -m venv .venv && source .venv/bin/activate
    pip install "hopsworks[python]"
    ```

On your own machine, `hops setup` opens a browser, lets you pick a project, creates an API key and caches it in `~/.hops.toml`:

```bash
hops setup --host https://my.hopsworks.ai
```

Non-interactive environments such as CI use an existing API key instead:

```bash
hops login --host https://my.hopsworks.ai --api-key "$HOPSWORKS_API_KEY" --project fraud_detection
```

Inside the [project terminal][terminal] no login is needed, `hops` is pointed at the project you opened it from.

## Explore and use the feature store

Every asset type has a subcommand: `project`, `fg`, `fv`, `td`, `model`, `deployment`, `job`, `datasource`, `sql`.
`hops <command> --help` lists the verbs.

```bash
hops project use fraud_detection
hops fg list
hops fg info transactions
hops fg preview transactions --n 5
hops fv create transactions_fraud --feature-group transactions
hops fv get transactions_fraud --entry "cc_num=4532015112830366"
hops sql "select count(*) from transactions_1"
```

Add `--json` to any command for machine-readable output:

```bash
hops fg info transactions --json
```

```json
{
  "id": 1080,
  "name": "transactions",
  "version": 1,
  "type": "cached",
  "online_enabled": false,
  "primary_key": ["tid"],
  "event_time": "datetime",
  "features": [
    {"name": "tid", "type": "bigint", "primary": true}
  ]
}
```

## For coding agents

The CLI is the simplest way to give an agent access to Hopsworks: allow it to run `hops` and it can read and write the project.
`hops init` scaffolds the Hopsworks skill, slash command and sub-agent for Claude Code into a repository and allows `Bash(hops *)` there:

```bash
hops init --dir .
```

`hops skills list` shows the Hopsworks skills the agent can load, feature groups, feature views, training, online inference, monitoring and more.
The [project terminal][terminal] has Claude Code and Codex preinstalled with `hops` already connected, and the [Wizard][wizard] uses exactly this path to build a system end to end.
