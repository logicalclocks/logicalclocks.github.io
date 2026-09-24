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

```bash
pip install hopsworks[python]
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
pip install hopsworks[python,great-expectations,polars]
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
| `.claude/commands/hops-ml.md` | The `/hops-ml` slash command: a fast interview on Haiku for a new ML system (what to predict, batch, real-time or agentic, how often, which data, how predictions are used), recorded in `system.yaml` as you answer. |
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

## Hopsworks Java Library

If you want to interact with the Hopsworks Feature Store from environments such as Spark, Flink or Beam, you can use the Hopsworks Feature Store (Hopsworks) Java library.

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

### Flink

The `artifactId` for the Flink build is `hsfs-flink`, if you are using Maven as build tool, you can add the following dependency:

```xml
<dependency>
    <groupId>com.logicalclocks</groupId>
    <artifactId>hsfs-flink</artifactId>
    <version>${hsfs.version}</version>
</dependency>
```

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
