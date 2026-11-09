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

Supported versions of Python: 3.10, 3.11, 3.12, 3.13, 3.14 ([PyPI ↗](https://pypi.org/project/hopsworks/))

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

The Hopsworks Python library ships a set of skills for coding agents: Claude Code, Codex, GitHub Copilot, OpenCode, pi and Hermes Agent.
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

`AGENTS.md` is read by Claude Code, Codex, GitHub Copilot, OpenCode, pi and Hermes Agent.
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
hops skills install --agent pi
hops skills install --agent hermes
```

The skills are written to `.codex/skills/` for Codex, `.opencode/skills/` for OpenCode, where the path is also registered in `opencode.json`, and `.agents/skills/` for GitHub Copilot, pi and Hermes Agent, which share that directory.
pi asks whether to trust the repository the first time it starts there, and loads the skills once you do.
Hermes Agent loads a repository's skills only in a git repository you have trusted, so run `hermes skills trust <your-repository>` once after installing them.
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
hops factory run ml-batch        # or ml-realtime, ml-streaming, ml-agent
```

The Factory and every `hops factory` command are available only on a cluster whose `factory_enabled` variable is `true`; elsewhere the commands stop with `The Factory is not enabled for this Hopsworks cluster.`
The Factory builds in the Terminal, so it also needs the Terminal enabled: the Helm chart sets `factory_enabled` only when `terminal.enabled` is true, and the menu hides the Factory while the Terminal is off. On a cluster where `factory_enabled` is not `true`, the Factory and ML system REST endpoints answer `403` with error code `150115`.
`hops factory run <factory>` asks the factory's questions in the terminal, section by section, with the factory's defaults: for `ml-batch` the system's name, what it should predict, its cadence and run time, its data (feature groups in the project, synthetic data described in a sentence, and files), how its predictions are used, and its monitoring.
`--answers answers.json` takes the answers from a file instead, as the **Factory** page writes it, and `--preset <id>` starts from one of the factory's examples (`churn-example`, `recs-example`, `fraud-example`, `debitcard-example`, `gis-example`, `helpdesk-example` or `run-example`, as `hops factory get <factory>` lists them under `presets`).
`ml-streaming` builds a real-time system whose batch features are dbt models run in Trino on a schedule and whose streaming features are a Spark Structured Streaming job; it also asks how often the dbt models run and the streaming window in minutes.
Its `debitcard-example` generates a year of synthetic debit card authorisations, 1,000,000 by default, streams more on the same cards, and scores each card's last hour against its spending baseline with an Isolation Forest deployment and a JavaScript fraud console.
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
A GitHub repository the build creates, an example's included, is named `hops-<slug>`. When you already have a repository of that name, it is `hops-<slug>-<project>`, and when that is taken too, `hops-<slug>-<project>-2`, `hops-<slug>-<project>-3` and so on.
**Factory**, in the project menu below Catalog, opens on a box: describe the system you want, and Platform Intelligence finds the project's factories that could build it, up to five.
They show as buttons below the box, the most likely highlighted in the middle; a box above them says why the selected factory fits and what it would build, and picking another factory explains that one.
The green **Build** button opens the selected factory's form, at its blueprint when the description is one, filled in with what the description says, for you to check and press **Create**.
This needs Platform Intelligence configured on the cluster; without it the box is not shown, and you pick a factory from **From Template**.
A factory's form has a chat beside it for settling the requirements, and it starts on its own when the form opens.
It writes a draft `system.yaml` in `factory-drafts/<factory>` of your HopsFS home, with the form's answers, and starts Claude Code there, which says in a few lines what will be built and asks only the few questions that change it: the data, what it produces and for whom, how often and how much history, a dashboard or app, and who hears about failures; technical details are left to the build.
It writes your answers into the draft, which the form shows as it changes, and notes what the form has no field for, which the build receives too; then it summarizes again and asks whether to create the system or change something.
What you type in the form goes to Claude Code with your next message.
Say in the chat that you want to create the system, and Claude Code checks the required answers and the page creates it, as **Create** does; **Back** and **Create** are at the top right of the page.
The form's chat tab in the Terminal closes once the system is created.
**From Template** lists the factories without the description: **ML System** holds **Batch ML system**, **Real-time ML system**, **Batch and streaming ML system**, **Agentic system** and **Ontology and text-to-SQL**, **Analytics** the analytics layer factories, and each has a **Blueprints** submenu of its examples, each opening its factory's form filled in.
The cogwheel opens **Manage factories**.
**Existing Systems**, shown once a factory has built a system, lists the project's systems for every member: each with its factory, type, status, phases done, owner and last update, and an open folder for the ones whose code you can open, a lock for the ones you cannot, and a link for the ones in a Git repository; the box above it filters the list.
**Login to GitHub** runs `github-login` in a Terminal tab; the page shows whether the terminal's GitHub CLI is logged in, which the build needs to create the repository.
With the chat on, the tab stays hidden and the chat shows GitHub's one-time code with **Open GitHub's device page**, which copies the code and opens the page, and **Copy code**; without the chat, the device page opens on the click and the Terminal tab shows the code.
The tab closes once the login succeeds.
Each ML system form asks for the system's name, which is also its directory's and, as `hops-<name>`, its GitHub repository's unless that name is taken (lowercase letters, digits and hyphens), what it should predict, its targets (a batch system's cadence and run time, a real-time or agentic system's latency and throughput), its data (feature groups in the project, synthetic data described in a sentence, and files), and how its predictions are used.
Every form starts with **Create new GitHub repo**, checked; unchecked, it asks for the URL of an existing GitHub, GitLab, Bitbucket or other Git repository, which the build pushes to with git alone.
Checked, **Create** tells the build that you confirm the creation of the system's new private repository under your GitHub account, `hops-<name>` or the next free name above, so Claude Code does not stop to ask for that confirmation.
Sections with defaults show a one-line summary of their answers, with **Edit** to change them.
For an agentic system the LLM's endpoint, model and key are saved as your account environment variables, `LLM_URL`, `LLM_MODEL` and `LLM_API_KEY`.
For a batch or real-time system, **Monitoring** (collapsed) sets whether every prediction logs the features it used (on by default) and, in your own words, what to monitor and alert on, such as drift in a feature against the training data or a failed job.
The build turns them into feature logging on the feature view, feature monitoring checks and alerts, and sends a failure alert for every job the system owns to the project's alert receiver.
For a real-time system, **Prediction latency tracing** (collapsed, off by default) creates the deployment with tracing: the share of requests recorded as traces, from 0.01% to 100% (10% by default), and the days tracing stays on (7 by default).
The deployment then times every request's feature lookup, transformations, model predict and feature logging, shown under X-ray latencies on its page, and can be switched off and on there without a restart; it serves one worker per replica, which the build's latency benchmark runs with.
**Create** runs `hops factory run ml-batch --answers` (or `ml-realtime`, `ml-streaming`, `ml-agent`) in a Terminal tab named after the system, which records it and starts Claude Code on `/hops-build <name>`; the page opens the system once it is registered.
**Location**, above the form of every factory, sets the folder the system's directory goes in, which holds its code and is its git repository: your home folder in the project by default, or another folder of the project you can write to, such as one in `Resources` so every member can open the code; from the CLI, run `hops factory run` in that folder.

A system's page is a chat beside the system.
The chat is the conversation of the Claude Code in the system's Terminal tab, the build while it runs: its replies, its tool calls folded to one line, and its questions and permission requests as cards whose options answer them.
A message you send is typed into that tab; when no Claude Code runs there, the first one starts it with the system's `system.yaml` and asks for an overview of the system.
The Terminal panel closes and the project menu collapses while the chat is shown, on a factory's form and on a system's page; the menu stays collapsed when the Terminal opens, and its toggle opens it again. The Terminal must be running for the chat to reach Claude Code.
When Claude Code in the Terminal is not logged in, the chat says so with **Log in to Claude Code**, which runs `/login`: the chat shows **Open the sign-in page** and a box for the code the page shows once you authorize.
After the login Claude Code waits for Enter, and the chat shows `Logged in to Claude Code. Press Enter to continue.` with **Press Enter**.
While Claude Code works, the line that says so has **Press Enter**, which sends Enter for a prompt Claude Code waits on in the Terminal outside the conversation, and **Show the Terminal**, which shows the Terminal's last lines with **Enter** and **Esc**.
Beside the chat, **App** shows the system's app or dashboards in the page; while the app is stopped, **Start app** starts the deployments it calls and then the app, and while it is starting or redeploying the button says so instead.
**Assets** shows the system with its status, repository, files, phases and actions, then what it has made in three columns, the feature, training and inference pipelines, each asset linked to its page with its state, and its jobs below.
A feature group shows when it last changed and the rows that commit appended, updated and deleted.
A job shows its schedule (cron in UTC) and its next run, with **Edit** for its settings; a job that backfills has **Backfill**, which runs it once over a start and end time you choose, starting where its last backfill ended, and any other job has **Run**.
An app, deployment or feature group that `system.yaml` records but the project does not have shows as missing once the phase that builds it is done, or the system is built; the system's pages then say it is not fully built, with a button that asks Claude Code to rebuild it. While a build runs, an asset its phase has not built yet is not reported.
**System Details** shows the specification, `system.yaml`, at the top, then the phases, what is done and what is left, and the requirements, locked.
`system.yaml` shows what changed since your last message in the chat: added lines are highlighted and removed lines struck through, with the count of each; **Edit the file** opens the editor, and **Mark as seen** clears the highlights.
**Open in Terminal** brings the system's Terminal tab to the front, or opens one with Claude Code started in its directory.
**Architecture** opens the system's architecture: its data sources, feature, training and inference pipelines and app, with the data flowing between them, redrawn as `system.yaml` changes.
A box whose part of the specification changed since you last looked is marked until you click it; clicking a box shows that part of `system.yaml`, which you can edit and save, and boxes can be dragged.
**Status**, a view after **Assets** once every phase is done, shows the last status report.
Pick how far back it looks, **1 day**, **7 days** or **Custom** (a number of days or hours), and press **Generate Report**: it checks the system's jobs, what its feature pipelines wrote, and its deployments and app over that window, shows the report, and sends its findings to the chat, where Claude Code summarizes them and suggests fixes.
The browser remembers the window you picked.
For each feature pipeline the report sets the rows it read against the rows it wrote in the window, and checks each output for columns with nulls and for hours or days with no rows.
A Hopsworks administrator can turn the chat off with `hopsworks.factory_chat_enabled: false` in the Helm values, the `factory_chat_enabled` variable: a system's page then shows its views at the full width, and **Status** is a button among the system's actions that opens the report on a page of its own.
A system whose directory is deleted shows as unavailable, and leaves the list 24 hours later.
Registering a directory needs write access to it, and refreshing a registered system needs its owner or a Data owner, so a member cannot claim another member's system.
A system records the factory version and the digest of the definition it was built from, and keeps them when it is refreshed.
**Delete** asks what to delete: the system's entry in the list only, that and every asset the system created (its app, deployments, jobs, models, feature view and training data, the feature groups it writes, the data sources it created and its cloned environments; feature groups it only reads are kept), or those and its GitHub repository, which is deleted only when the build created it for this system alone. The assets are deleted in the terminal, downstream first, and the entry last, so a delete that fails part way leaves the system in the list to be deleted again. Deleting the assets also deletes the code directory; deleting the entry only keeps it.
Deleting the assets or the repository needs a Data owner, since only a Data owner can delete apps, deployments and jobs; other members can delete the entry only.
An asset another system in the project also names is kept, and so is an asset whose name does not contain the system's name unless its description names the system: a system made from an example starts from the example's `system.yaml`, and its delete must not remove the example's app or tables.
The delete lists each asset it kept and why.
**Delete** closes the system's Terminal tab, which stops its Claude Code, and the tab of its form's chat; while the assets are deleted, a notice shows that the delete is in progress.

```bash
hops factory list                                   # the factories and how many systems each built
hops factory run <factory> [--answers F] [--preset P]  # a new system, then build it with Claude Code
hops factory run <factory> <slug>                   # resume a system from its system.yaml
hops factory system list [--factory <factory>]      # the project's systems and whether you can open their code
hops factory system register <dir> [--name N]       # register or refresh one by hand
hops factory system status <system>                 # write its health report, status/report.html
hops factory system remove <system>                 # remove it from the list; its code is kept
hops factory system delete <system> --assets [--repo]  # also delete what it created, and its repository
hops factory system write-doc <system> --expected-sha256 H --from F  # replace system.yaml unless it changed since it was read
hops factory system lease show|acquire|renew|release <system>  # the build lease that keeps two builds off one system
```

### Build a silver analytics layer

An analytics layer organizes tables as bronze (raw data as it arrived), silver (cleansed and conformed) and gold (consumption-ready).
Hopsworks installs an archived schematized tag, `analytics_table`, whose `layer` is `bronze`, `silver` or `gold` and whose `lifecycle` is `dev`, `staging` or `prod`; every change of a table's value is kept in the tag history.
When you ingest data with a dltHub data source, **Tag as bronze tables** in the review, off by default, tags every feature group it creates as bronze.

**From Template > Analytics**, in the Factory, lists **Silver layer**, **Data Mart**, **Data pipeline** and **Data ingestion**; the bronze layer is built from its blueprint. **Silver layer** builds a silver layer from the project's bronze feature groups.
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
A build deletes jobs and feature groups only with `hops factory system delete-assets`, which refuses a table the system reads or one of a lower analytics layer, anything another system names, and anything this system's `system.yaml` does not record or its name does not carry.
A table with several versions needs `NAME:VERSION`.

### Build a data pipeline

**From Template > Analytics > Data pipeline** builds one scheduled pipeline that reads data sources, transforms them and writes the results to feature groups or files.
The form asks for its name, the repository, the engine (PySpark, DuckDB, Polars, or dbt on Trino), and in your own words its data sources, its transformations and its outputs, with how often it runs.
**Create** runs `hops factory run analytics-pipeline --answers` in a Terminal tab named after the pipeline and starts Claude Code on `/hops-factory-analytics-pipeline <name>`; the page opens the pipeline with the chat beside it.

The requirements are settled in the form's chat before the pipeline is created, as for every factory, including how much history to backfill, alerting and a dashboard to inspect the outputs (Superset, a custom dashboard app, or none).
The build's first phase does not ask them again: it profiles the sources and decides the technical details with best practice, the exact sources and joins, output keys, the incremental window, quality rules, the backfill and the alerts (failed and killed runs as critical and long-running ones as a warning, no alert per success, a warning when a run writes nothing or breaks its quality rules), as the chat's notes say or by default, and asks only when something essential is missing.

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

### Ingest data with dlt

**From Template > Analytics > Data ingestion** copies data from databases, warehouses, object stores, SaaS apps and REST APIs into feature groups with dlt (DLTHub), on a schedule.
Its chat settles the ingestion with you in rounds until you say it is final.
Say where your data is and what should land in Hopsworks, and the chat fills in the data sources: each with its name, its kind, where it is, the tables to ingest, and whether it is available for real-time ML, which also loads the online feature store.
For a data source the project already has, the chat lists its tables and asks which to ingest; a new one is created.
**Credentials** takes the passwords, keys and tokens the new data sources need, each as a name, such as `CRM_PASSWORD`, and a hidden value: on **Create** each is saved as a private variable of your account, the build stores it in its data source, which keeps it as Hopsworks keeps every data source's secrets, and then deletes the variable; only the names reach `system.yaml` and the chat.

The chat previews each table and suggests, with its reason, the columns not to ingest, the columns to pseudonymize, which keep a keyed hash of each value so joins still work, and the rows to filter out.
For each table the chat finds, from the source, the primary key and the event time, which become the feature group's, and whether the table is append-only: rows only added, never updated or deleted, as in events, logs and transactions, which are written with plain appends, much faster than the upserts a table whose rows change needs.
It estimates each table's volume, in total and per day, and proposes partitioning and ordering only where it pays: none for a small table, a partition on the event time's hour, day or week for a large table written by time, and ordering by key for an entity table, in the format's own terms (a partition column or liquid clustering for Delta Lake, hidden partitioning with a sort order or z-order for Iceberg, partitioning with z-order for Hudi).
**Tables, columns and rows** holds those choices and the transformations applied to every table; every column is cast to a type feature groups hold offline (Hive) and online (MySQL), and the default transformations make each table a valid feature group: column names as lowercase snake_case of at most 63 characters, timestamps in UTC, nested JSON flattened, and one non-null primary key per row.
No load-time column is added: every write is a commit, whose time the table format keeps.
**Schedule and history** sets how often it runs, whether to backfill all history, a window from a start to an end time, or nothing, and how rows arrive where a table does not say: append-only, changing (upserted by primary key), or replaced each run.
**Storage and inspection** sets the table format, Delta Lake by default, Apache Iceberg or Apache Hudi, a Superset dashboard to inspect the ingested data, and whether the tables are tagged as bronze for a silver layer.

The build creates the data sources and one feature group per table with its primary key and event time, then decides how the ingestion runs: the ingestion jobs Hopsworks runs in the shared `dlthub-ingestion-pipeline` environment by default, with a transform script for the transformations a column mapping cannot do, or its own dlt program when the source needs it.
It clones the environment, as `<name>-dlt`, only when the ingestion needs a Python library the shared environment lacks.
It records the result in `system.yaml`:

```yaml
ingestion:
  sources:
    - name: crm
      kind: sql
      reused: false
      credentials: [CRM_PASSWORD]
      tables:
        - source: public.customers
          ingested: {feature_group: crm_customers, version: 1}
          primary_key: [customer_id]
          online: true
          write_mode: merge
          cursor: updated_at
  environment: {name: dlthub-ingestion-pipeline, cloned: false}
  program: transform
  job: {name: crm-ingestion-ingest, type: ingestion, schedule: {cron: "0 0 2 * * ?"}}
```

The chat stays open while it builds: it shows the rows each table loaded, with the dropped and pseudonymized columns as they are, and asks whether they are right before it schedules the job, builds the dashboard and verifies a run against the source's row counts.

### Build an ontology and text-to-SQL app

The `ontology` factory builds an ontology of the tables in the project's SQL data sources, and an app that answers questions about their data by writing and running SQL.
Its jobs read the sources' metadata (schemas, tables, columns, keys and views) into a catalog, and an LLM compiles the catalog into business terms: concepts such as Customer or Invoice Line, with descriptions and synonyms, mapped to tables, columns, joins and SQL expressions.
Members review and edit the terms in the app, and its chat answers a question with the SQL it ran and the rows it returned.

**From Template > ML System > Ontology and text-to-SQL** opens the factory's form, and **From Template > ML System > Blueprints > Example: sales database** opens it filled in for the sales example.
From a terminal:

```bash
hops factory run ontology                        # answer the form's questions in the terminal
hops factory run ontology --preset wwi-example   # the sales example, named sales-ontology
```

Both start Claude Code on `/hops-factory-ontology <name>` in the system's directory, which builds the system phase by phase.
A project can hold several ontology systems, and each one builds:

| Part | Name |
| --- | --- |
| App: the HTTP API, the web UI and the chat | `<name>`, a custom app in the `ontology-pipeline` environment |
| App tables: the catalog, the ontology, conversations and settings | `<table prefix><table>`, in the project's online database |
| Jobs, in the `ontology-pipeline` environment | `<name>-ingest`, `<name>-compile`, `<name>-embed`, `<name>-reset`, `<name>-import` |
| Online feature groups, each with an embedding index | `<name_>_data_objects` (tables and columns), `<name_>_semantic` (the ontology) |
| Models in the Model Registry, imported from Hugging Face | `Nemotron_3_5_Embed_1B_BF16`, `NVIDIA_Nemotron_3_5_Lightning_30B_A3B_FP8` |
| vLLM deployments | `nemotronembed`, `nemotronllm` |

`<name_>` is the name with hyphens replaced by underscores, and `<table prefix>` is the app's table prefix.
The models and the deployments are shared by the project's ontology systems: a second system reuses those the first one made, and a system with an external model makes neither that model nor its deployment.
Each embedding index holds vectors of the dimension chosen in the form, compared by cosine similarity.
The system's directory holds `ontology.yaml`, the system's configuration and the only file written from the answers, and the launchers of the app (`app.py`) and of the jobs (`jobs/`), which run the Auto-Ontology runtime that the `ontology-pipeline` environment ships.

#### Before you build an ontology

- **Data sources**: each source is a data source of the project with SHARED credentials, of type MySQL, PostgreSQL or ClickHouse ([SQL][how-to-set-up-an-sql-data-source]), [Snowflake][how-to-set-up-a-snowflake-data-source] or Databricks ([Unity Catalog][how-to-set-up-a-unity-catalog-data-source]).
  The build refuses a source with PROVIDED credentials, because those answer with one member's credentials while the app and the jobs serve every member.
  Two sources cannot read the same database.
- **A GPU, for local models**: the LLM and the embedding model run as two vLLM deployments that share one GPU, each requesting one `nvidia.com/gpu`.
  This needs the NVIDIA device plugin on the GPU node configured for time-slicing with `replicas: 2` and `renameByDefault: false`; neither the Helm chart nor Hopsworks configures it.
  The LLM takes 80% of the GPU's memory and the embedding model 12%, and the LLM's checkpoint, which the build downloads from Hugging Face, is about 32 GB.
  A Hugging Face token is needed only when Hugging Face asks for a login or a license acceptance.
- **External models, instead of a GPU**: an OpenAI-compatible endpoint for the LLM, the embedding model, or both, set in the form's **Models** section.
  Their URLs, model names and keys are saved as your [account environment variables][account-level-environment-variables] `LLM_URL`, `LLM_MODEL`, `LLM_API_KEY`, `EMBEDDING_URL`, `EMBEDDING_MODEL` and `EMBEDDING_API_KEY`, never in `system.yaml`.
  Hopsworks sets a member's account variables in every job and app that member starts, and a scheduled run starts as its job's creator.
  The embeddings endpoint must return vectors of the dimension chosen in the form.
- **`hopsable_proxy_enabled`, for the CLI and MCP**: `hops ontology` and the MCP tools reach the app with a proxy token, which Hopsworks mints only when the cluster variable `hopsable_proxy_enabled` is `true` (`hopsworks.variables.hopsable_proxy_enabled` in the Helm values, `false` by default); otherwise it refuses the token with error code `120012`.
  The app's pages in Hopsworks do not need it.
- **A Data owner**: a Data owner builds the system: the sales example creates tables, which a Data scientist cannot, and deleting a system's assets needs a Data owner.

#### The ontology form

- **Basics**: **Name**, which is also the system's directory, the app's name, the prefix of its jobs, feature groups and tables, and, as `hops-<name>`, its new GitHub repository; **Create new GitHub repo**; and **Who asks questions, and about what?**, such as "sales managers ask about orders, customers and stock levels", from which the build draws its test questions.
- **Data sources**: one entry per source, with **Data source name**, **Schemas**, an optional comma-separated allowlist (empty reads every schema the credentials can read), and **Table name pattern**, an optional regular expression a table's name must match.
- **Models**, collapsed: **LLM**, Nemotron 3.5 Lightning 30B (FP8) served in the project with vLLM (the default) or an OpenAI-compatible endpoint; **Embedding model**, Nemotron 3.5 Embed 1B served in the project with vLLM (the default) or an OpenAI-compatible endpoint; **Embedding dimension**, 2048 (the default) or 1024, which halves the vector index's memory; the endpoints, model names and keys of external models; and the **Hugging Face token**.
- **Schedule**, collapsed: when ingest and compile run, **Every day** (the default, at 02:00 and 03:00 UTC), **Every week** (Mondays at the same times) or **Only when started by hand or from the app**; and **Detect personal data**, off by default, which tags the columns that hold personal data and leaves their sample values out of the catalog and the embeddings.

The build runs these phases:

| Phase | What the build does |
| --- | --- |
| Check the sources and write ontology.yaml | Checks that every source exists, has a supported type and SHARED credentials, and that an external model's account variables are set, then writes `ontology.yaml` |
| Import the models and deploy them with vLLM | Imports each local model from Hugging Face at a pinned revision and deploys it, or reuses what another ontology system made; skipped when both models are external |
| Ontology app | Creates and starts the app, which creates its tables |
| Jobs, and ingest the sources' metadata | Creates the five jobs, schedules ingest and compile, and runs ingest |
| Compile the ontology | Runs compile and embed, then checks that every table has a term, except a table whose columns are all foreign keys, and that every ontology row has its vector in `<name_>_semantic` |
| Verify | Asks three questions drawn from **Who asks questions, and about what?**, or the sales example's five, records each answer, its SQL and its time in `system.yaml`, and runs `hops factory system status` |

Compiling sends many LLM calls: on one GPU it takes tens of minutes for a few dozen tables.

`--preset wwi-example`, or **Blueprints > Example: sales database**, builds the system `sales-ontology` over generated data.
Its first phase runs a script that creates six tables, `sales_state_provinces`, `sales_cities`, `sales_customers`, `sales_products`, `sales_orders` and `sales_order_lines`, in the project's online database, fills them from a fixed seed, and creates the MySQL data source `sales_mysql` over them with SHARED credentials, the system's only source.
The tables carry the `sales_` prefix because a member can create tables only in the project's online database, not in a database of their own.
Its last phase asks five questions and compares each answer with the one the data gives:

| Question | Answer |
| --- | --- |
| How many orders were placed in March 2025? | 14 |
| What was the total revenue of delivered orders? | 107467.00 |
| Which state has the most customers? | Georgia, with 7 |
| Which products have fewer than 20 units in stock? | Build your own robot kit, Office desk toy, Ride on toy sedan car |
| Which salesperson brought in the most revenue from delivered orders? | Archer Lamble, with 33722.00 |

#### Roles in the ontology app

The Hopsworks app proxy signs the caller's name into every request, and the app reads the caller's role from the project's members, cached for 60 seconds.

| Project role | In the app |
| --- | --- |
| Data owner | Everything: chat, edits to the catalog and the ontology, saved analyses, **Analytics** and **Settings** |
| Data scientist | Chat, edits to the catalog and the ontology, and saved analyses |
| Observer, Feature store restricted | The catalog, the terms, tags and saved analyses, read-only and without sample values; no chat |
| Not a member | Refused |

Observers and Feature store restricted members get no chat because the chat runs SQL on the data sources, and no sample values because they cannot preview data sources in Hopsworks.
Only Data owners and Data scientists can mint the proxy token, so only they can use `hops ontology` and the MCP tools; an API key needs the `JOB` scope.
The app, and the jobs it starts, run as the member who last started or redeployed the app.

#### Use an ontology

The app is the system's **App** view on its Factory page, served at `/hopsworks-api/pythonapp/<project>/<name>/`; `hops app url <name>` prints its address, and **Start app** starts the system's deployments and then the app.
Its pages:

- **Chat**: ask a question in plain language; the answer shows the SQL that ran, the rows and, when the result has one, a chart.
  Conversations are saved per member, and a follow-up question resolves against its conversation's earlier questions.
- **Discovery**: search the catalog and the ontology.
  Members without chat open the app here.
- **Terms**: the business terms with their descriptions, synonyms, columns and SQL expressions, to review and edit.
- **Analysis**: saved SQL analyses, which the chat uses as examples.
- **Exploration**: the graph of the terms and the joins between them.
- **Data**: the catalog of databases, schemas, tables and columns.
- **Analytics**, for Data owners: the questions asked in the last 30 days, and who asked them.
- **Settings**, for Data owners: **Sources**, **Tags**, **Rules**, **PII Settings**, **Semantic Input**, **Semantic Compilation**, **Agent Settings** and **Import / Export**.

**Sources** lists the data sources the ontology reads, with their schemas and table filter.
**Add Source** takes a data source's name, optional schemas and an optional table filter, connects to the source once, and starts the ingest job for it.
It refuses, with HTTP 422, a source of an unsupported type, one with PROVIDED credentials, and one that reads a database another source already reads, and, with HTTP 502, one it cannot reach.
**Remove** starts the reset job, which deletes what was ingested from that source: its catalog, its part of the ontology, and their vectors.
The `sources` of `ontology.yaml` seed a new system only: once the app has a source, **Sources** is the record, so a source removed there stays removed.

**Semantic Compilation** has **Enable Semantic Compilation**: the compile job compiles only while it is on, and switching it on starts a compile run.
A new system starts with it on, from `semantic_compilation: true` in its `ontology.yaml`; the `pii_detection` and `distinct_value_probing` answers set **PII Settings** and **Semantic Input** the same way, and a later change in **Settings** stays.
**Reset** there deletes the ontology of every database and compiles it again.
An edit in the app re-embeds the edited object, so it shows in the catalog and in the vector search at once; an edit whose embedding fails is embedded again by the next compile or embed run.
**Import / Export** exports the catalog and the ontology as YAML, in the native format or Apache Ossie's, and imports such a file.

The app answers at most four questions at a time; past that it answers HTTP 429 with `Retry-After`.
The chat runs only single `SELECT` or `WITH` statements, with the source's credentials, and on MySQL, PostgreSQL and ClickHouse in a read-only session.

From a terminal:

```bash
hops ontology status sales-ontology                                      # can it answer, and what stops it; exits 1 when it cannot
hops ontology ask sales-ontology "Which state has the most customers?"   # the answer, its SQL and up to 100 rows
hops ontology ask sales-ontology "How many orders did they place?" --conversation-id <uuid>  # a follow-up in a saved conversation
```

`hops ontology ask` prints each step the agent takes as it takes it, then the answer, its SQL and up to 100 rows, and says how many rows the query returned when it returned more.
With `--json` it prints `answer`, `sql`, `rows`, `row_count`, `truncated`, `reasoning` and `chart` instead.
Without `--conversation-id` a question is answered on its own: no history, nothing saved and no chart.
It waits 900 seconds for the answer, which `--timeout` changes.

`hops ontology status` prints the app's state, whether it is serving, its URL, whether the ontology is compiled, whether a source is configured to run SQL on, whether a database is ingested, and the ingested databases, then a `blocker:` line for each thing that stops the system from answering:

- **The app is `<state>`; start it with `hops app start <name>`**: read `hops app logs <name>` when it does not start.
- **No database is ingested yet**: run `hops job run <name>-ingest --wait`; its log names the source that failed.
- **The ontology is not compiled yet**: switch on **Enable Semantic Compilation** in the app's **Settings**, which starts a compile run, or run the compile job with `--force`.
- **No data source is configured**: add one with **Add Source** on the app's **Sources** page.

When an answer comes back empty, `hops ontology status` separates a system that is not ready from a question the ontology does not cover.

The Hopsworks MCP server, `hopsworks-mcp`, which ships with the `hopsworks` library, has the same reads as tools; each takes the system's name as `system`:

| Tool | Returns |
| --- | --- |
| `check_readiness` | Whether the system can answer, and what stops it |
| `search_terms` | The terms whose name contains a string |
| `get_term` | One term, with its description, synonyms and related terms |
| `get_term_columns` | The columns a term maps to |
| `get_term_sql_attributes` | The SQL expressions under a term, such as a margin or a ratio |
| `get_sql_attribute` | One SQL expression, with its term and its purpose |
| `describe_table` | One table, with its columns, the terms that reference it and the SQL expressions over it |
| `check_answerable` | How well the ontology covers the entities of a question, without running the agent |
| `ask_question` | The answer, its SQL and up to 100 rows; it takes tens of seconds and reports each step as progress |

#### Ontology jobs

The five jobs run in the `ontology-pipeline` environment with 2 cores, 4096 MB and no GPU.
Their default arguments name the system's configuration, `--config <dir>/ontology.yaml`, where `<dir>` is the system's directory relative to the project, such as `Users/<user>/sales-ontology`.
One job works on the ontology at a time: a job that starts while another runs fails with `another ontology pipeline job is running`.

- `<name>-ingest [--source <data source>]` reads the sources' metadata into the catalog and embeds the tables and columns into `<name_>_data_objects`, then starts the compile job when compilation is switched on.
  `--source` ingests one source.
  It runs on its schedule, and **Add Source** starts it for the new source; it exits 1 when a source fails.
- `<name>-compile [--force]` compiles the catalog into terms, joins and SQL expressions, and embeds them into `<name_>_semantic`.
  It compiles only while **Enable Semantic Compilation** is on, and `--force` compiles regardless.
  It runs on its schedule, after ingest, and when compilation is switched on, and exits 1 when the compilation fails.
- `<name>-embed [--database <database>]` embeds every ontology row whose text changed since it was last embedded, of one database with `--database`.
  It fails when a row is left without its vector.
- `<name>-reset --semantic [--database <database>]` deletes the ontology and its vectors, of one database with `--database`, and compiles it again; **Reset** starts it.
  `<name>-reset --all --database <database>` deletes a database's catalog, ontology and vectors; **Remove** on **Sources** starts it.
- `<name>-import --file <path> [--merge]` imports an export, native or Apache Ossie YAML, from a file in the project, for a file too large to upload on **Import / Export**, and embeds it.
  The file's definitions replace the existing ones, and `--merge` keeps the ones the file does not mention.

An execution runs with the arguments it is given instead of the job's default arguments, so arguments given by hand repeat `--config`:

```bash
hops job run sales-ontology-ingest --wait   # the default arguments
hops job run sales-ontology-ingest --wait --args "--config Users/<user>/sales-ontology/ontology.yaml --source sales_mysql"
```

A scheduled run starts as its job's creator, which `system.yaml` records for each job.

#### Delete an ontology

**Delete** on the system's page, or `hops factory system delete <name> --assets`, deletes the app with its tables, the jobs, the two feature groups and the system's directory; it needs a Data owner.
The models and the deployments the project's ontology systems share are kept while another system names them.
A deployment's description names the system that created it, so it is deleted with that system when no other system names it, and otherwise stays until you delete it with `hops deployment delete <deployment>`.
A model's description names the Hugging Face commit it came from and no system, so the models are kept; `hops model delete <model> --version <version>` deletes one.
The data sources the system reads, the sales example's tables, and the vLLM configurations in `Resources/ontology-vllm` are kept.

```bash
hops factory system delete sales-ontology --assets   # the app and its tables, the jobs, the feature groups and the directory
```

### Create your own factory

A factory is a YAML definition: the questions of its creation form, the phases of its build, and the instructions Claude Code follows to build what the answers describe.
The project's own factories are listed under **From Template** with the built-in ones of their kind, each opening the form it generates.
The ten built-in factories, `ml-batch`, `ml-realtime`, `ml-streaming`, `ml-agent`, `ontology`, `analytics-bronze`, `analytics-silver`, `analytics-gold`, `analytics-pipeline` and `analytics-ingestion`, are read-only; clone one to change it.
A form has no conditions: every question of a section is shown, and a section with defaults can be collapsed to a summary of its answers with **Edit**.

**Factory > Manage factories** lists every factory with its version and how many systems it built.
A data owner can create a factory, clone any factory, import a YAML file, export one, enable or disable a project factory, and delete one that has no systems left.
The editor changes the questions, phases and build instructions as a form or as YAML, previews the form beside it, and saves each change as a new version; a system keeps the version it was built with.
Importing shows the factory's build instructions in full first: Claude Code follows them in your Terminal, with your credentials.

A clone of a built-in keeps the built-in's questions and build; answers the built-in build does not read are recorded in `requirements.extra` and the clone's instructions in `factory.instructions` of each system's `system.yaml`, which the built-in build follows too.
A definition's questions can be text, numbers, dates and times in UTC, checkboxes, one or some of a list of options, one or several feature groups, a list of entries each with its own questions, account variables, which are saved in your account and never in `system.yaml`, and credentials, named secrets saved the same way whose names alone reach `system.yaml`; presets are named sets of starting answers, listed as the factory's **Blueprints**.

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

Every command but `validate`, which checks a local file without a cluster, needs a logged-in session on a cluster whose `factory_enabled` variable is `true`.

```bash
hops factory validate churn-review.yaml      # check a definition
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
