---
description: The semantic layer tools of the Hopsworks MCP server, and the hops-semantic skill for coding agents.
---

# Semantic Layer Agent Tools { #semantic-agent-tools }

The Hopsworks MCP server gives an agent tools to discover the metrics of a project's semantic projects, query them, and compile their definitions.
The discovery and query tools have the names of the semantic layer tools of the dbt MCP server.

## Run the MCP server { #semantic-agent-tools-server }

The server ships with the Hopsworks Python library, in the `mcp` extra:

```bash
pip install "hopsworks[python,mcp]"
hopsworks-mcp --transport stdio --hopsworks_host my.hopsworks.ai --project demo \
  --api_key_file ~/.hopsworks/api_key
```

Without `--transport stdio`, the server listens over HTTP on `127.0.0.1:8000`; `--host` and `--port` change the address, and a non-loopback address needs `--auth-token`.
The tools act on the project the server is logged in to, from the start options or the `login` tool.
The API key needs the `FEATURESTORE` and `TRINO` scopes for the semantic layer tools, since queries run on Trino as the key's user.

## Tools { #semantic-agent-tools-list }

| Tool | Tag | Arguments | Returns |
| --- | --- | --- | --- |
| `list_semantic_projects` | READ | | Each semantic project's name, root path, mode, serving build, and whether it is stale. |
| `list_metrics` | READ | `semantic_project`, `tag` (optional) | CSV of the metrics: name, type, label, description and tags. `tag` keeps the metrics that set that tag schema. |
| `get_dimensions` | READ | `semantic_project`, `metrics` | CSV of the dimensions the metrics can be grouped by: name, type, grains and entity path. |
| `get_entities` | READ | `semantic_project`, `metrics` (optional) | CSV of the entities. |
| `get_dimension_values` | READ | `semantic_project`, `dimension`, `metrics` and `limit` (optional) | CSV of the distinct values of a dimension. |
| `query_metrics` | READ | `semantic_project`, `metrics`, then `group_by`, `where`, `order_by` and `limit` (optional) | CSV of the rows, 100 rows unless `limit` says otherwise. |
| `get_metrics_compiled_sql` | READ | The arguments of `query_metrics` | The SQL the query compiles to. |
| `get_semantic_project_tags` | READ | `semantic_project` | The semantic project's tags, name and value. |
| `validate_semantic_project` | WRITE | `semantic_project` | The build's status and its issues. |
| `compile_semantic_project` | WRITE | `semantic_project` | The build id, its status and its issues. |

Group-bys and filters take the forms of [Query metrics][semantic-query-metrics]: `customer__country`, `metric_time__month` and `{{ Dimension('order__status') }} = 'completed'`.
The CSV of `query_metrics` is capped in length, so a large result needs a `limit` or a filter.

`validate_semantic_project` and `compile_semantic_project` both compile the definitions and report the build.
A compile of files that have not changed returns their existing build, so a validate of unchanged files changes nothing.
In `FOLLOW` mode a new valid build answers queries at once, see [Serving modes][semantic-overview-serving-modes].

## Coding agents { #semantic-agent-tools-skill }

A coding agent that runs the `hops` CLI uses the `hops-semantic` skill: authoring semantic YAML over feature groups, compiling, testing metrics, and querying them with `hops semantic`.
`hops skills list` lists it, and the [project terminal][terminal] has Claude Code and Codex preinstalled with `hops` connected.
The [Hopsworks CLI][hopsworks-cli] guide covers installing the skills into a repository with `hops init`.
