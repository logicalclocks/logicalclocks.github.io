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

The Hopsworks Python library ships the `hops` CLI and a set of skills for coding agents.
Inside a Hopsworks terminal the skills are available to Claude Code, Codex, GitHub Copilot and OpenCode automatically.

### Authenticate

```bash
uv pip install "hopsworks[python]"
hops setup --host https://<your-cluster>
```

Without `--host`, `hops setup` asks for the host and proposes `https://c.app.hopsworks.ai`; press Enter to accept it or type the address of your cluster.
`hops setup` opens a browser page where you choose a project, creates an API key for it, and stores the key in `~/.hops.toml`.
Running it again checks that the stored key still works and exits; pass `--force` to create a new key.
On a machine without a browser, pass `--no-browser` and open the printed URL yourself.

### Add the Claude Code files to a repository

```bash
cd <your-repository>
hops init
```

`hops init` writes the following files into the current directory:

| Path | Purpose |
| --- | --- |
| `.claude/skills/hops/SKILL.md` | A reference for the `hops` CLI. |
| `.claude/commands/hops.md` | The `/hops` slash command for Claude Code. |
| `.claude/agents/hops-fti.md` | A Claude Code sub-agent that reviews a project against the feature, training and inference pipeline pattern. |
| `.claude/settings.local.json` | Allows `Bash(hops *)`, so Claude Code can run the CLI without asking before each command. |

These files are read by Claude Code only.
Running `hops init` again leaves the files you have edited unchanged and lists them; pass `--force` to overwrite them.

### Browse the Hopsworks skills

```bash
hops skills list
hops skills show hops-fg
```

Inside a Hopsworks terminal these commands list the skills the agents there load.
The `hopsworks` package does not include the skills themselves, so on your own machine point `HOPS_SKILLS_DIR` at the `skills` directory of a [hopsworks-api](https://github.com/logicalclocks/hopsworks-api/tree/branch-5.1/skills) checkout.

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
If you use a coding agent, see [Skills and instructions for coding agents][skills-and-instructions-for-coding-agents] to connect it to Hopsworks.

## Other environments

The Hopsworks Feature Store client libraries can also be installed in external environments, such as Databricks, AWS Sagemaker, or Azure Machine Learning.
For more information, see [Client Integrations](../integrations/index.md).
