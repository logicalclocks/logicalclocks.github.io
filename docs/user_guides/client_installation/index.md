---
description: Documentation on how to install the Hopsworks Python and Java library.
---
# Client Installation Guide

## Hopsworks Python library

The Hopsworks Python client library is required to connect to Hopsworks from your local machine or any other Python environment such as Google Colab or AWS Sagemaker.
Execute the following command to install the Hopsworks client library in your Python environment:

!!! note "Virtual environment"
    It is recommended to use a virtual python environment instead of the system environment used by your operating system, in order to avoid any side effects regarding interfering dependencies.

!!! attention "Windows/Conda Installation"

    On Windows systems you might need to install twofish manually before installing hopsworks, if you don't have the Microsoft Visual C++ Build Tools installed.
    In that case, it is recommended to use a conda environment and run the following commands:

    ```bash
    conda install twofish
    pip install hopsworks[python]
    ```

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

Supported versions of Python: 3.10, 3.11, 3.12, 3.13 ([PyPI ↗](https://pypi.org/project/hopsworks/))

### Profiles

The Hopsworks library has several profiles that bring additional dependencies and enable additional functionalities:

| Profile Name | Description |
| --- | --- |
| No Profile | This is the base installation. Supports interacting with the feature store metadata, model registry and deployments. It also supports reading and writing from the feature store from PySpark environments. |
| `python` | This profile enables reading and writing from/to the feature store from a Python environment |
| `great-expectations` | Installs [Great Expectations](https://greatexpectations.io/) and enables data validation on feature pipelines. Supports 0.18.12 and 1.17.1; 1.17.1 is recommended |
| `polars` | This profile installs the [Polars](https://pola.rs/) library and enables reading and writing Polars DataFrames |

You can install all the above profiles with the following command:

```bash
uv pip install "hopsworks[python,great-expectations,polars]"
```

## Skills and instructions for coding agents

The Hopsworks Python library ships a set of skills for coding agents: Claude Code, Codex, GitHub Copilot and OpenCode.
Inside a Hopsworks terminal they are available to every agent automatically.
On your own machine, two commands make them available in the repository you are working in.

### Authenticate and write the agent instructions

```bash
uv pip install "hopsworks[python]"
cd <your-repository>
hops setup --host https://<your-cluster>
```

Without `--host`, `hops setup` asks for the host and proposes `https://eu-west.cloud.hopsworks.ai`, the Hopsworks serverless endpoint; press Enter to accept it or type the address of your cluster.
`hops setup` opens a browser page where you choose a project, creates an API key for it, and stores the key in `~/.hops.toml`.
It then writes the following files into the current directory:

| Path | Purpose |
| --- | --- |
| `AGENTS.md` | Instructions for the agent: the project you are connected to, where the `hopsworks` library is installed on this machine, and how to use the `hops` CLI and the skills. |
| `.claude/skills/hops/SKILL.md` | A reference for the `hops` CLI. |
| `.claude/commands/hops.md` | The `/hops` slash command for Claude Code: a fast menu to explore data, build or edit a Superset dashboard (`/hops dashboard`) or a Python app (`/hops app`), and show status. It runs on Haiku; the building is done by the agents below. |
| `.claude/commands/hops-ml.md` | The `/hops-ml` slash command: an ML system interview inside Claude Code, on Haiku, recorded in `system.yaml` as you answer. |
| `.claude/commands/hops-build.md` | The `/hops-build` slash command: completes the specification the interview recorded and builds the ML system to a pull request, on your session's model. |
| `.claude/agents/hops-dashboard-builder.md` | The Claude Code sub-agent `/hops` runs to build, edit or delete a dashboard. |
| `.claude/agents/hops-app-builder.md` | The Claude Code sub-agent `/hops` runs to build, edit or delete an app and fix it until it serves. |
| `.claude/agents/hops-train-agent.md` | The Claude Code sub-agent `/hops-build` runs to train a model until it meets its target. |
| `.claude/agents/hops-infer-agent.md` | The Claude Code sub-agent `/hops-build` runs to build inference until it meets its SLA. |
| `.claude/settings.local.json` | Allows `Bash(hops *)`, so Claude Code can run the CLI without asking before each command. |

`AGENTS.md` is read by Claude Code, Codex, GitHub Copilot and OpenCode.
The files under `.claude/` are read by Claude Code only.
Running `hops setup` again in a directory that already has these files updates the files you have not edited and leaves the ones you have edited unchanged.
A file an earlier version wrote and this one no longer ships, such as `.claude/agents/hops-fti.md`, is removed when you have not edited it and reported otherwise.
Pass `--no-scaffold` to authenticate without writing any files.

### Add the Hopsworks skills

```bash
hops skills install
```

`hops skills install` copies the Hopsworks skills into `.claude/skills/`, one directory per skill, which is where Claude Code discovers them.
For another agent, pass `--agent`, which can be repeated:

```bash
hops skills install --agent codex
hops skills install --agent copilot
hops skills install --agent opencode
```

The skills are written to `.codex/skills/`, `.agents/skills/` and `.opencode/skills/` respectively, and for OpenCode the path is also registered in `opencode.json`.
An agent loads only the name and description of each skill when it starts and reads a skill in full when a task calls for it, so adding all of them costs a few kilobytes of context rather than the size of the skills themselves.

Running `hops skills install` again after upgrading the `hopsworks` library updates the skills you have not edited, keeps the skills you have edited, and removes skills that the new version no longer ships.
Pass `--force` to overwrite edited skills as well.

To read the skills without adding them to a repository:

```bash
hops skills list
hops skills show hops-fg
```

### Build an ML system

```bash
hops factory run ml-batch        # or ml-realtime, ml-agent
```

`hops factory run <factory>` asks the factory's questions in the terminal, section by section, with the factory's defaults: for `ml-batch` the system's name, what it should predict, its cadence and run time, its data (feature groups in the project, synthetic data described in a sentence, and files), how its predictions are used, and its monitoring.
`--answers answers.json` takes the answers from a file instead, as the **Factory** page writes it, and `--preset <id>` starts from one of the factory's examples (`churn-example`, `recs-example`, `fraud-example`, `gis-example`, `helpdesk-example` or `run-example`, as `hops factory get <factory>` lists them under `presets`).
The help desk agent answers from documents you upload to `Resources/helpdesk-docs` (PDF, text, Markdown, Word or OpenDocument), which a job cuts into passages and embeds with a sentence-transformers model downloaded into the Model Registry, and from the customer's recent events; it is a LangGraph agent deployment with a JavaScript chat app.
For an agentic system, `hops factory run ml-agent` asks for an OpenAI-compatible LLM endpoint, model and API key (read without echo), unless your account already has them, and saves them as your account environment variables `LLM_URL`, `LLM_MODEL` and `LLM_API_KEY`, which the agent reads.
The answers are written to `<slug>/system.yaml` in the current directory, and what they leave out, such as where the code goes, is asked next.

A new data source is created with `hops datasource create`, and its password or key is read without echo and passed to it in an environment variable, so it never appears on the command line or in `system.yaml`.

`hops factory run` then starts Claude Code with `/hops-build <slug>`, which completes the specification and builds the feature, training and inference pipelines.
Each system's directory holds an `AGENTS.md` saying the system is built from `system.yaml`; `hops factory run` and the **Factory** page start Claude Code in that directory, so it reads it, checks what a change to `system.yaml` means for the pipelines and the assets they create, and finds what a changed component affects downstream with `hops fg lineage`, `hops fv lineage`, `hops td lineage`, `hops model lineage` and `hops deployment lineage`.
Inside tmux, as in the Hopsworks terminal, it opens a new tmux window named after the system, so several systems can be built at once.
Pass `--no-launch` to record the system only.
`hops factory run <factory> <slug>`, or `hops factory run <factory>` inside the system's directory, resumes a system: its `system.yaml` records the factory, the factory version and every answer, so it needs no answers file.

`hops factory run` registers each system with the project, by the HopsFS directory of its code, or by its GitHub repository when you build from an external client.
A GitHub repository the build creates, an example's included, is named `hops-<slug>`, or `hops-<slug>-<project>` when you already have one of that name.
**Factory**, in the project menu below Catalog, opens on a box: describe the system you want, and Platform Intelligence finds the project's factories that could build it, up to five.
They show as buttons below the box, the most likely highlighted in the middle; a box above them says why the selected factory fits and what it would build, and picking another factory explains that one.
The green **Build** button opens the selected factory's form, at its blueprint when the description is one, filled in with what the description says, for you to check and press **Create**.
This needs Platform Intelligence configured on the cluster; without it, pick a factory from **From Template**.
A factory's form has a chat beside it for filling in the requirements.
The chat's first message writes a draft `system.yaml` in `factory-drafts/<factory>` of your HopsFS home, with the form's answers, and starts Claude Code there; it reads the project's data, asks what it needs, and writes the answers into the draft, which the form shows as it changes.
What you type in the form goes to Claude Code with your next message.
Say in the chat that you want to create the system, and Claude Code checks the required answers and the page creates it, as **Create** does; **Back** and **Create** are at the top right of the page.
**From Template** lists the factories without the description: **ML System** holds **Batch ML system**, **Real-time ML system** and **Agentic system**, **Analytics** the analytics layer factories, and each has a **Blueprints** submenu of its examples, each opening its factory's form filled in.
The cogwheel opens **Manage factories**.
**Existing Systems**, shown once a factory has built a system, lists the project's systems for every member: each with its factory, type, status, phases done, owner and last update, and an open folder for the ones whose code you can open, a lock for the ones you cannot, and a link for the ones in a Git repository; the box above it filters the list.
**Login to GitHub** runs `github-login` in a Terminal tab; the page shows whether the terminal's GitHub CLI is logged in, which the build needs to create the repository.
Each ML system form asks for the system's name, which is also its directory's and, as `hops-<name>`, its GitHub repository's (lowercase letters, digits and hyphens), what it should predict, its targets (a batch system's cadence and run time, a real-time or agentic system's latency and throughput), its data (feature groups in the project, synthetic data described in a sentence, and files), and how its predictions are used.
Every form starts with **Create new GitHub repo**, checked; unchecked, it asks for the URL of an existing GitHub, GitLab, Bitbucket or other Git repository, which the build pushes to with git alone.
Sections with defaults show a one-line summary of their answers, with **Edit** to change them.
For an agentic system the LLM's endpoint, model and key are saved as your account environment variables, `LLM_URL`, `LLM_MODEL` and `LLM_API_KEY`.
For a batch or real-time system, **Monitoring** (collapsed) sets whether every prediction logs the features it used (on by default) and, in your own words, what to monitor and alert on, such as drift in a feature against the training data or a failed job.
The build turns them into feature logging on the feature view, feature monitoring checks and alerts, and sends a failure alert for every job the system owns to the project's alert receiver.
**Create** runs `hops factory run ml-batch --answers` (or `ml-realtime`, `ml-agent`) in a Terminal tab named after the system, which records it and starts Claude Code on `/hops-build <name>`; the page opens the system once it is registered.

A system's page is a chat beside the system.
The chat is the conversation of the Claude Code in the system's Terminal tab, the build while it runs: its replies, its tool calls folded to one line, and its questions and permission requests as cards whose options answer them.
A message you send is typed into that tab; when no Claude Code runs there, the first one starts it with the system's `system.yaml` and asks for an overview of the system.
The Terminal panel closes and the project menu collapses while the chat is shown, and the Terminal must be running for the chat to reach Claude Code.
Beside the chat, **App** shows the system's app or dashboards in the page; while the app is stopped, **Start app** starts the deployments it calls and then the app, and while it is starting or redeploying the button says so instead.
**Assets** shows the system with its status, repository, files, phases and actions, then what it has made in three columns, the feature, training and inference pipelines, each asset linked to its page with its state, and its jobs below.
**System Details** shows the specification, `system.yaml`, at the top, then the phases, what is done and what is left, and the requirements, locked.
**Open in Terminal** brings the system's Terminal tab to the front, or opens one with Claude Code started in its directory.
**Architecture** opens the system's architecture: its data sources, feature, training and inference pipelines and app, with the data flowing between them, redrawn as `system.yaml` changes.
A box whose part of the specification changed since you last looked is marked until you click it; clicking a box shows that part of `system.yaml`, which you can edit and save, and boxes can be dragged.
**Status**, a view after **Assets** once every phase is done, shows the last status report.
Pick how far back it looks, **1 day**, **7 days** or **Custom** (a number of days or hours), and press **Generate Report**: it checks the system's jobs, what its feature pipelines wrote, and its deployments and app over that window, shows the report, and sends its findings to the chat, where Claude Code summarizes them and suggests fixes.
The browser remembers the window you picked.
For each feature pipeline the report sets the rows it read against the rows it wrote in the window, and checks each output for columns with nulls and for hours or days with no rows.
A Hopsworks administrator can turn the chat off with `hopsworks.factory_chat_enabled: false` in the Helm values, the `factory_chat_enabled` variable: a system's page then shows its views at the full width, and **Status** is a button among the system's actions that opens the report on a page of its own.
A system whose directory is deleted disappears from the list.
**Delete** asks what to delete: the system's entry in the list only, that and every asset the system created (its app, deployments, jobs, models, feature view and training data, the feature groups it writes, the data sources it created and its cloned environments; feature groups it only reads are kept), or those and its GitHub repository, which is deleted only when the build created it for this system alone. The assets are deleted in the terminal, downstream first, and the entry last, so a delete that fails part way leaves the system in the list to be deleted again. Deleting the assets also deletes the code directory; deleting the entry only keeps it.

```bash
hops factory list                                   # the factories and how many systems each built
hops factory run <factory> [--answers F] [--preset P]  # a new system, then build it with Claude Code
hops factory run <factory> <slug>                   # resume a system from its system.yaml
hops factory system list [--factory <factory>]      # the project's systems and whether you can open their code
hops factory system register <dir> [--name N]       # register or refresh one by hand
hops factory system status <system>                 # write its health report, status/report.html
hops factory system remove <system>                 # remove it from the list; its code is kept
hops factory system delete <system> --assets [--repo]  # also delete what it created, and its repository
```

### Build a silver analytics layer

An analytics layer organizes tables as bronze (raw data as it arrived), silver (cleansed and conformed) and gold (consumption-ready).
Hopsworks installs an archived schematized tag, `analytics_table`, whose `layer` is `bronze`, `silver` or `gold` and whose `lifecycle` is `dev`, `staging` or `prod`; every change of a table's value is kept in the tag history.
When you ingest data with a dltHub data source, **Tag as bronze tables** in the review, off by default, tags every feature group it creates as bronze.

**From Template > Analytics**, in the Factory, lists two factories, **Silver layer** and **Data Mart**; the silver one builds a silver layer from the project's bronze feature groups.
A project without feature groups has nothing to build from: ingest raw data as bronze tables first, or build the example bronze layer.

**Blueprints** in the same menu lists example layers. **Synthetic clickstream (bronze)** builds a bronze layer of generated web shop data with `hops factory run analytics-bronze --preset clickstream-example`, which copies the generator into `clickstream-bronze/` and starts Claude Code on `/hops-bronze clickstream-bronze`.
It writes four offline Delta feature groups tagged `layer: bronze`: `clickstream_customers`, `clickstream_products`, `clickstream_orders` and `clickstream_clicks`.
A backfill job writes the 30 days up to the last midnight: 10,000 customers, 1,000 products, 20,000 orders and 1,000,000 clicks.
An hourly job writes 10,000 clicks an hour, and a daily job writes the day's new customers, products and orders and its changes: profile updates, price changes, discontinued products and order status changes.
The data is raw on purpose, for a silver layer to cleanse: about 0.001% of clicks arrive twice under a new `ingest_id`, and an order's lines are a JSON array in its `items` column.
The page asks for the bronze tables to build from (only those tagged bronze are shown while any are), the silver tasks (deduplicate, cast types, standardize values, handle nulls, validate with a rejects table, protect personal data, conform entities, surrogate keys, referential checks), additional tasks in your own words, the engine, the refresh cadence and the lifecycle.
The engine is dbt on Trino unless an additional task needs code SQL does not express well, when PySpark is suggested.
Each bronze table has its own refresh, hourly, daily or weekly; a silver table refreshes as often as its most frequently updated source, and the layer gets one job per refresh, each with its own schedule and freshness target.
It also asks how the tables behave, with defaults: history (`latest`, one row per key, or `full`, every version by time), deletes in bronze (`ignore` or `propagate`), bronze schema changes (`fail`, or `evolve` by adding new columns), a late-data lookback re-read before each window (none, a day or a week), the share of rejected rows above which a run fails, with an alert when one fails, and a freshness target.
**Create** runs `hops factory run analytics-silver --answers` in a Terminal tab named after the layer, which records its specification in `<name>/system.yaml` and starts Claude Code on `/hops-silver <name>`.

The build profiles the bronze tables, designs the silver tables, writes and tests the code, backfills the whole bronze history once, schedules the job and tags the silver feature groups `layer: silver`, and verifies one window.
Silver tables are feature groups, materialized, never views, and in third normal form: one table per entity or event, every column depending on its table's key alone, lookups in tables of their own, and no aggregates, which belong in gold.
Each scheduled run processes only the bronze rows that arrived in its window, `[HOPS_START_TIME, HOPS_END_TIME)`, which Hopsworks sets for every scheduled run, so the silver tables are refreshed incrementally; running a window again changes nothing.
`system.yaml` drives the layer's lifecycle, as an ML system's does: when it changes after the build (its bronze tables, tasks, engine, refresh or lifecycle), the layer's page says what changed and **Apply changes** runs `/hops-silver <name> apply`, which retags for a new lifecycle, reschedules for a new refresh, and for a changed task, engine or source writes a new version of each silver table whose content changes, backfilled from the whole bronze history, and switches the job to it; earlier versions are kept.
Every silver table records its bronze tables as its parents, so the lineage shows them; its partitioning (none, or by hour, day or week) is decided from the volume and time span of the bronze table's files; and the job is scheduled with catch-up, so windows missed while the scheduler was down are replayed.
A layer's page shows its requirements as they were filled in.
**Status** on a built layer's page reports the job's runs and each table's rows, last write against the freshness target, rejected share against the limit, and file layout, with a box for asking Claude Code anything about the report, filled in with a request to fix the problems it found; **Backfill** reprocesses every bronze row into the silver tables, running each job.
A layer's page shows its phases, the silver tables and jobs it made, the bronze tables it reads, and its tasks, with links to the layer's GitHub repository and to its dbt code in the file browser.
An analytics pipeline's silver and gold layers share one GitHub repository, `hops-<prefix>`, where the prefix is the layer's name without `-silver` or `-gold`: each layer is a directory in it, a gold layer joins the repository of the silver layer it reads, and the build uses the repository when it exists, creates it when it does not, and pushes every commit to it.
Every job has a delete icon that asks whether to also delete the feature groups only that job writes; **Add tables** adds bronze tables, each with its refresh, and describes the silver tables wanted from them, which Claude Code designs and builds with the rest.
**Delete** removes the layer from the Factory, or deletes it with its jobs, tables and directory; the tables a layer reads are never deleted.

### Build a gold analytics layer of data marts

**From Template > Analytics > Data Mart** builds a gold layer from silver tables: a Kimball dimensional model, a star or snowflake schema, for the queries the layer will serve.
The page asks for those queries, the model, the first data mart's refresh and freshness target, and the silver tables to read.
On a cluster with Platform Intelligence, **Suggest** selects the silver tables the answers so far call for, and drafts answers to the folded questions below that are still blank; change any of them as you like.
The standards every data mart follows (naming, modeling, documentation and quality, proposed and editable) and the first data mart's requirements below are folded away: anything left blank is drafted by the build from the layer's questions and the silver tables, for you to confirm, and recorded in `system.yaml`, where you can edit it later.
The first data mart is named after the layer.

A gold layer is a set of data marts, each added, changed and deleted on its own, with its own fact and dimension tables and its own jobs, `<layer>-<mart>-<refresh>`, at its own refresh.
A data mart's requirements are:

- **Business purpose**: who the analysts are, the decisions and reports it supports, and who approves its business definitions.
- **Existing tables**: the gold tables it can reuse, or new ones built from silver.
- **Row grain**: what one row represents, what identifies it, and whether rows are individual events, periodic snapshots or aggregates.
- **Metrics**: each metric's exact formula, exclusions, filters, currency and unit.
- **Freshness and changes**: the refresh and freshness target, how late arrivals, updates and deletes are processed, and whether corrections restate published results.
- **Verification**: example questions with the answers expected, in plain English; the totals that must reconcile, and with what; and how refreshes and reruns are proven correct. The build runs every check after the backfill and again after a refresh, records the results, and does not mark the mart built until each passes.
- **Quality and access**: the invariants to test, what happens when a check fails (fail the run, quarantine the failing rows, or warn), who may read which rows and columns, and the projects it is shared with.
- **Dashboards**: in plain text, the dashboards to build from the mart: for each, who reads it, the questions it answers, and the charts and filters wanted. Optional.

**Create** runs `hops factory run analytics-gold --answers` and starts Claude Code on `/hops-gold <name>`, which builds each mart: its requirements, the design of its facts and dimensions (a dimension used by several marts is built once and shared), the dbt models with their tests, the backfill with the verification, the schedule and tags (`layer: gold`, the silver tables as parents), a verified refresh, and last the Superset dashboards the mart asks for, each over its gold tables and checked against the mart's verified numbers.
The layer's page shows each mart with its phases, tables, jobs, verification results and links to its dashboards: **Edit** changes its requirements and applies the change, **Add data mart** adds one, and deleting a mart deletes its jobs and, if asked, its tables that no other mart lists.

```bash
hops factory run analytics-bronze --preset clickstream-example  # build the example bronze layer of generated data
hops factory run analytics-silver [--answers answers.json]   # record a silver layer and build it with Claude Code
hops factory run analytics-gold [--answers answers.json]     # record a gold layer and its first data mart
hops factory run analytics-gold <layer> --change add-mart [--answers mart.json]     # add a data mart to a gold layer
hops factory run analytics-gold <layer> --change edit-mart [--answers mart.json]    # change a data mart's requirements
hops factory run analytics-gold <layer> --change delete-mart  # delete a data mart's jobs, and if asked its own tables
hops factory run analytics-gold <layer> --change delete-job   # delete one job, and if asked the tables only it writes
hops factory run analytics-silver <layer> --change add-tables [--answers new.json]  # add bronze tables to a silver layer
hops factory system status <layer>                  # write the layer's health report, status/report.html
hops job run <job> --start-time 1970-01-01 --end-time <now> --wait  # backfill: recompute a job's tables from the whole history
hops factory system delete <layer> --assets         # delete the layer, its jobs and tables; never what it reads
```

A change to a built system, a layer's or any other, is one of its factory's `changes`: **Change** on the system's page lists them, and the layer pages' **Add data mart**, **Edit**, **Add tables** and delete icons open them.
Each opens the change's form; saving records the request in the system's `system.yaml` (`changes`, `status: pending`) with `hops factory run <factory> <system> --change <id>`, and resumes the build in a Terminal tab, which carries out the pending requests first.
A build deletes jobs and feature groups only with `hops factory system delete-assets`, which refuses a table the system reads or one of a lower analytics layer.

### Build a data pipeline

**From Template > Analytics > Data pipeline** builds one scheduled pipeline that reads data sources, transforms them and writes the results to feature groups or files.
The form asks for its name, the repository, the engine (PySpark, DuckDB, Polars, or dbt on Trino), and in your own words its data sources, its transformations and its outputs, with how often it runs.
**Create** runs `hops factory run analytics-pipeline --answers` in a Terminal tab named after the pipeline and starts Claude Code on `/hops-factory-analytics-pipeline <name>`; the page opens the pipeline with the chat beside it.

The first phase settles the requirements with you in the chat.
Claude Code looks at the feature groups, data sources and files you named, then asks what it cannot tell, with options drawn from what it found: the exact sources and how they join, each transformation's rules, each output's name, primary key, event time and whether it is online, whether a run reads only its window or all the data, how much history to backfill before the first scheduled run (a number of days, or of hours for an hourly pipeline, all of it, or none), the columns that must never be null, alerting, and whether you want a dashboard to inspect the outputs: Superset, a custom dashboard app, or none.
For alerting it recommends what usually works: alert on failed and killed runs as critical and on long-running ones as a warning, to a channel someone watches (Slack, PagerDuty or email); no alert on every success, which gets ignored, unless a downstream team needs the signal; a warning when a run writes no rows or breaks the quality rules; and alerts that carry the pipeline and job, the window, rows in and out, the error with the last log lines, the link to the run's logs, and the next step.
It writes the answers to `system.yaml`, says back what the pipeline will read, do and write, and builds only once you confirm.

The pipeline's `system.yaml` holds only a `features` block, the feature pipeline section an ML system has, with no training or inference pipeline:

```yaml
features:
  pipelines:
    - name: orders
      engine: polars
      reads: [{feature_group: raw_orders, version: 1}, {data_source: crm, table: customers}]
      transformations: [drop test orders, join customers on customer_id, revenue per customer and day]
      writes: [{feature_group: orders_daily, version: 1, primary_key: [customer_id], event_time: day}]
      quality: {max_null_pct: 5, not_null: [customer_id, day]}
      backfill: {last: 30d}
      alerts: {receiver: {name: data-oncall, slack: ["#data-alerts"]}, on: [{status: failed, severity: critical}]}
      job: {name: orders-pipeline-orders, schedule: {cron: "0 0 2 * * ?"}}
dashboard: {kind: superset, dashboards: [{name: Orders, url: <url>}]}
```

The build then writes and tests the code, backfills the days or hours you asked for, schedules the job, sets up its alerts, builds the dashboard, which the system's **App** view shows, and verifies one run with `hops factory system status`.
A Polars or DuckDB pipeline is a Python job that never starts a Spark job: the feature groups it writes have statistics off.

### Create your own factory

A factory is a YAML definition: the questions of its creation form, the phases of its build, and the instructions Claude Code follows to build what the answers describe.
The project's own factories are listed under **From Template** with the built-in ones of their kind, each opening the form it generates.
The seven built-in factories, `ml-batch`, `ml-realtime`, `ml-agent`, `analytics-bronze`, `analytics-silver`, `analytics-gold` and `analytics-pipeline`, are read-only; clone one to change it.
A form has no conditions: every question of a section is shown, and a section with defaults can be collapsed to a summary of its answers with **Edit**.

**Factory > Manage factories** lists every factory with its version and how many systems it built.
A data owner can create a factory, clone any factory, import a YAML file, export one, enable or disable a project factory, and delete one that has no systems left.
The editor changes the questions, phases and build instructions as a form or as YAML, previews the form beside it, and saves each change as a new version; a system keeps the version it was built with.
Importing shows the factory's build instructions in full first: Claude Code follows them in your Terminal, with your credentials.

A clone of a built-in keeps the built-in's questions and build; answers the built-in build does not read are recorded in `requirements.extra` and the clone's instructions in `factory.instructions` of each system's `system.yaml`, which the built-in build follows too.
A definition's questions can be text, numbers, checkboxes, one or some of a list of options, one or several feature groups, a list of entries each with its own questions, and account variables, which are saved in your account and never in `system.yaml`; presets are named sets of starting answers, listed as the factory's **Blueprints**.

```yaml
apiVersion: hopsworks.ai/factory/v1
kind: Factory
name: churn-review
title: Churn review
form:
  sections:
    - id: basics
      title: Basics
      fields:
        - {id: name, type: slug, label: Name, required: true}
        - {id: question, type: textarea, label: "What should it answer?", required: true}
phases:
  - {key: build, label: Build, minutes: 20}
build:
  skills: [hops-superset]
  instructions: Build a dashboard that answers requirements.question.
```

```bash
hops factory validate churn-review.yaml      # check a definition without a cluster
hops factory import churn-review.yaml        # review it, then add it to the project
hops factory clone ml-batch fraud-ml         # start from a built-in
hops factory export churn-review             # write churn-review.factory.yaml
hops factory run churn-review                # answer its questions, then build with Claude Code
hops factory delete churn-review             # refused while it has systems
```

The `hops-factory` skill lists every field type and rule.

## Hopsworks Java Library

If you want to interact with the Hopsworks Feature Store from environments such as Spark or Beam, you can use the Hopsworks Feature Store (Hopsworks) Java library.

!!! note "Feature Store Only"

    The Java library only allows interaction with the Feature Store component of the Hopsworks platform.
    Additionally each environment might restrict the supported API operation.
    You can see which API operation is supported by which environment [here](../fs/compute_engines.md)

The Hopsworks library is available on the Hopsworks' Maven repository.
If you are using Maven as build tool, you can add the following in your `pom.xml` file:

```xml
<repositories>
    <repository>
        <id>Hops</id>
        <name>Hops Repository</name>
        <url>https://archiva.hops.works/repository/Hops/</url>
        <releases>
            <enabled>true</enabled>
        </releases>
        <snapshots>
            <enabled>true</enabled>
        </snapshots>
    </repository>
</repositories>
```

The library has different builds targeting different environments:

### Hopsworks Java

The `artifactId` for the Hopsworks Java build is `hsfs`, if you are using Maven as build tool, you can add the following dependency:

```xml
<dependency>
    <groupId>com.logicalclocks</groupId>
    <artifactId>hsfs</artifactId>
    <version>${hsfs.version}</version>
</dependency>
```

### Spark

The `artifactId` for the Spark build is `hsfs-spark-spark{spark.version}`, if you are using Maven as build tool, you can add the following dependency:

```xml
<dependency>
    <groupId>com.logicalclocks</groupId>
    <artifactId>hsfs-spark-spark3.1</artifactId>
    <version>${hsfs.version}</version>
</dependency>
```

Hopsworks provides builds for Spark 3.1, 3.3 and 3.5. The builds are also provided as JAR files which can be downloaded from [Hopsworks repository](https://repo.hops.works/master/hsfs)

### Beam

The `artifactId` for the Beam build is `hsfs-beam`, if you are using Maven as build tool, you can add the following dependency:

```xml
<dependency>
    <groupId>com.logicalclocks</groupId>
    <artifactId>hsfs-beam</artifactId>
    <version>${hsfs.version}</version>
</dependency>
```

## Next Steps

If you are using a local python environment and want to connect to Hopsworks, you can follow the [Python Guide](../integrations/python.md#generate-an-api-key) section to create an API Key and to get started.
If you use a coding agent, see [Skills and instructions for coding agents][skills-and-instructions-for-coding-agents] to give it the Hopsworks skills.

## Other environments

The Hopsworks Feature Store client libraries can also be installed in external environments, such as Databricks, AWS Sagemaker, or Azure Machine Learning.
For more information, see [Client Integrations](../integrations/index.md).
