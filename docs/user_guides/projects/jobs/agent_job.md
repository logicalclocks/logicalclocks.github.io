---
description: Documentation on how to configure and execute an Agent Job on Hopsworks.
---

# How To Run An Agent Job

## Introduction

Agent Jobs are **fire-and-forget AI agents** that run as first-class Hopsworks jobs.
You write a prompt, select a provider (Claude Code or OpenAI Codex), grant the
agent a set of permissions, point it at the project resources it needs, and
launch it.
The agent runs to completion inside a Kubernetes pod, writes its results to
HopsFS, and the pod terminates.
No interactive UI, no WebSocket — the same lifecycle as a Python or Spark job.

Common use cases:

- **Scheduled data-quality audits** — point the agent at a Feature Group and ask
  it to look for null spikes, schema drift, or freshness issues each night
- **Model evaluation** — give it a Model + Deployment ref and have it grade
  recent predictions against a reference dataset
- **Operational runbooks** — turn the wiki page you'd hand a new on-call into a
  prompt the agent runs whenever a `LONG_RUNNING` alert fires on a pipeline
- **Ad-hoc exploration** — fire one off from the CLI with `hops job start`
  whenever you'd otherwise open Jupyter for a one-shot question

Because Agent Jobs use the existing Jobs subsystem, you get the same scheduling,
alerts, log capture, and execution history you do for any other Hopsworks job.

## Prerequisites

1. **Feature flag** — agent jobs are gated cluster-wide. An admin must set:

      ```sql
      UPDATE variables SET value='true' WHERE id='agent_jobs_enabled';
      ```

2. **Authentication credentials** for whichever provider you choose. The agent
    can pick these up from three sources (see [Authentication](#authentication)
    below) — the simplest is to log in to Claude or Codex once from an
    interactive Hopsworks Terminal session; the credentials persist into HopsFS
    and every subsequent Agent Job in any of your projects reuses them.

3. **The `agent-job` Python environment** (or a clone of it) — this is the
    runtime base image. It's installed by default; clone it in
    Project Settings → Python Environments if you need to layer additional
    libraries on top.

## UI

### Step 1: Open Jobs and create a new Agent Job

Click **Jobs** in the project sidebar, then **New Job**, and pick `AGENT` as the
job type.

### Step 2: Write the prompt

The prompt is the task description — what you want the agent to do.
Be explicit about the inputs (which Feature Group, which Model) and the
expected output (a report file at `${AGENT_OUTPUT_PATH}/result.md`, a Slack
message, etc).

```text
Inspect feature group `transactions` v3 for null spikes in the `amount` and
`merchant_id` columns over the last 7 days. Report findings as Markdown at
${AGENT_OUTPUT_PATH}/result.md. If you find a column with more than 1% nulls,
post a Slack alert.
```

### Step 3: Pick the provider

| Provider | When to use |
|---|---|
| **Claude** (default) | Most tasks; supports hooks, max-turns and max-budget controls. |
| **Codex** | When you want OpenAI's coding agent. Supports free-form CLI flag overrides via `cliArgs`. |

Codex-only fields (`cliArgs`) appear when you select Codex; Claude-only fields
(`maxTurns`, `maxBudgetUsd`, `hooks`) are hidden in that case.

### Step 4: Configure permissions

Permissions are an explicit allowlist of tools the agent may invoke — they map
directly to the underlying CLI's tool patterns. Pick a preset for most jobs:

| Preset | Effect |
|---|---|
| `READ_ONLY` (default) | Inspect feature groups, feature views, models — no writes. |
| `OPERATOR` | Run any `hops` CLI command + `python *`, plus write under `/hopsfs/*`. |
| `FULL` | A curated allowlist of common shell commands (`ls`, `cat`, `grep`, `find`, `curl`, `wget`, `echo`, `mkdir`, `cp`, `mv`), plus `Read(*)` and `Write(/hopsfs/*)`. **Not** unrestricted shell access — pick **Custom** if you need that. |
| `Custom` | A list of patterns you provide explicitly (e.g. `Bash(hops fg info *)`, `Read(*)`, `Write(/hopsfs/Resources/*)`). |

The agent runs with project-scoped JWT auth, so any data access still goes
through normal Hopsworks ACLs — permissions just bound what the *agent* is
allowed to attempt.

### Step 5: Attach resource references (optional)

Refs inject Hopsworks resource metadata into the agent pod as JSON files under
`/context/`. The agent can `cat` these to know which resources to operate on
without you having to spell every detail out in the prompt:

| Ref type | Required version? | Context file |
|---|---|---|
| `feature_group` | yes | `/context/fg_<name>_v<version>.json` |
| `feature_view` | yes | `/context/fv_<name>_v<version>.json` |
| `model` | yes | `/context/model_<name>_v<version>.json` |
| `deployment` | no | `/context/deployment_<name>.json` |
| `job` | no | `/context/job_<name>.json` |

Refs are resolved server-side at launch time by the platform — you don't need
to write any glue code.

### Step 6: Environment variables (optional)

Use this card to supply credentials and other env vars the agent needs at
runtime. Vars set here are merged on top of:

1. Platform-injected vars (project ID, JWT path, HopsFS user home, …) — these
    are reserved and rejected if you try to set them
2. AI-provider secrets (from your AI provider secrets table, if any)
3. Your **account-level env vars** (visible across all your runtimes — manage
    them under Account → Environment variables)

So a per-job `ANTHROPIC_API_KEY` overrides the account-level value, which in
turn overrides anything in the secrets table.

Reserved-name prefixes that you may **not** set: `HOPS_`, `HOPSWORKS_`,
`HOPSFS_`, `AGENT_`.
The platform injects several `AGENT_*` variables that you can *read* from
your prompt — most usefully `AGENT_OUTPUT_PATH` (where your final
artifact must be written). They are reserved for the platform, so you
can't override them, but referencing them inside the prompt (e.g.
`${AGENT_OUTPUT_PATH}/result.md`) is the intended pattern.

### Step 7: Resources, environment, alerts

The bottom of the form is shared with other job types:

- **Environment** — defaults to `agent-job`. Pick a clone if you've added
  Python libraries on top.
- **Resource configuration** — CPU cores, memory, GPU count. Default is 0.5
  cores / 1024 MB / 0 GPU; bump this for heavier tasks.
- **Schedule** — same as other jobs. Cron expressions or interval runs.
- **Alerts** — FINISHED / FAILED / KILLED / LONG_RUNNING, routed to a Slack
  / webhook / email receiver. Setting `passToAgent: true` on a Slack alert
  injects `SLACK_WEBHOOK_URL` and `SLACK_CHANNEL` into the agent pod's env so
  the agent can post during execution via the bundled `slack-post` helper.

### Step 8: Run it

Click **Save**, then **Run**. The execution lands in the same Executions table
as Python and Spark jobs. Click an execution to see its state, logs, and output.

## Authentication

The agent pod resolves provider credentials in this priority order:

1. **Reused terminal-login credentials.** If you've opened a Hopsworks Terminal
   in any of your projects and run `claude login` (or `codex login`), the
   credentials persist in HopsFS at `/hopsfs/Users/<you>/.claude/.credentials.json`
   and `/hopsfs/Users/<you>/.codex/auth.json`. The agent pod symlinks `~/.claude`
   and `~/.codex` to those paths automatically — no API key needed.
2. **`ANTHROPIC_API_KEY` / `OPENAI_API_KEY` from env.** If terminal credentials
   are missing or invalid, the agent falls back to these env vars. Set them
   under Account → Environment variables (applies to all your jobs) or in this
   job's Environment variables section (applies just to this job).
3. **AI provider secrets table.** If you've configured AI providers under
   Project Settings, those keys are also injected. Per-job env vars override
   them.

Most users only need to do step 1 once.

## CLI

You can also create and run agent jobs via the `hops` CLI:

```bash
# Create from a JSON config
cat > my-agent.json <<EOF
{
  "type": "agentJobConfiguration",
  "appName": "data-quality-check",
  "prompt": "Check all feature groups for nulls and report findings",
  "model": "claude-sonnet-4-5",
  "maxTurns": 25,
  "permissionPreset": "READ_ONLY",
  "refs": [
    {"type": "feature_group", "name": "transactions", "version": 3}
  ],
  "envVars": [
    "PYTHONUNBUFFERED=1"
  ]
}
EOF

hops job create -f my-agent.json
hops job start data-quality-check
hops job logs data-quality-check --tail
```

The `hops` CLI is available inside the agent pod too, so the agent can launch
or query other jobs as long as you grant it `Bash(hops *)`.

## REST API

Agent Jobs use the existing Jobs REST API; the only difference is the
configuration payload, where `type` is `"agentJobConfiguration"` and the
fields are:

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `type` | string | yes | — | Must be `"agentJobConfiguration"` |
| `appName` | string | yes | — | Job name |
| `prompt` | string | yes | — | The task |
| `provider` | string | no | `"claude"` | `"claude"` or `"codex"` |
| `cliArgs` | string | no | — | Extra codex CLI flags (codex only) |
| `model` | string | no | `claude-sonnet-4-5` | Provider-specific model ID |
| `maxTurns` | int | no | 50 | Claude only |
| `maxBudgetUsd` | float | no | — | Claude only, max 100 |
| `permissionPreset` | string | no | `READ_ONLY` | `READ_ONLY` / `OPERATOR` / `FULL` |
| `permissions` | string[] | no | — | Custom — overrides preset if set |
| `refs` | AgentRef[] | no | — | Resource refs (see [Step 5](#step-5-attach-resource-references-optional)) |
| `hooks` | AgentHook[] | no | — | Pre/post tool-use hooks (claude only) |
| `skillsRef` | string | no | — | Path to a `.md` skills file on HopsFS |
| `envVars` | string[] | no | — | `"KEY=VALUE"` strings |
| `environmentName` | string | no | `agent-job` | Must be `agent-job` or a clone of it |
| `resourceConfig` | object | no | default | `{ cores, memory, gpus }` |
| `outputPath` | string | no | auto | Where to write results in HopsFS |

Full reference: see the `[HWORKS-2667]` PR description and the
`docs/features/agent-jobs/` directory in `hopsworks-ee` for the developer-side
spec.

## Output

By default the agent writes to:

```text
/hopsfs/Resources/agent-jobs/<job-name>/<execution-id>/
├── result.md         # primary, human-readable result — rendered by the UI
├── metadata.json     # { "exit_code": 0, "completed_at": "<ISO8601>" }
└── (any other files the agent chose to write)
```

The agent's stdout and stderr are captured by the standard execution-log path,
visible via the Logs button on the execution row.

## Limitations

- **Non-interactive only.** The agent cannot ask follow-up questions — the
  prompt is the whole input. If you need interactive iteration, use a Terminal
  session instead.
- **`maxTurns` is a hard safety net** (claude only) — set it high enough that
  reasonable runs don't trip it. Default 50.
- **The image must be `agent-job` or a clone** — other Python environments
  don't ship the Claude/Codex CLIs and will be rejected at job-create time.
- **Reserved env-var prefixes** — see [Step 6](#step-6-environment-variables-optional);
  `HOPS_`, `HOPSWORKS_`, `HOPSFS_`, and `AGENT_` are owned by the platform.
