---
description: The semantic layer tools of the Hopsworks MCP server, and the hops-semantic skill for coding agents.
---

# Semantic Layer Agent Tools { #semantic-agent-tools }

The Hopsworks MCP server gives an agent tools to discover the metrics and saved queries of a project's semantic projects, query them, compile their definitions, and build Superset dashboards of them.
The discovery and query tools have the names of the semantic layer tools of the dbt MCP server.
`list_exports` lists the feature groups that saved queries keep filled, which an agent can then read like any feature group.

## Run the MCP server { #semantic-agent-tools-server }

The server ships with the Hopsworks Python library, in the `mcp` extra:

```bash
pip install "hopsworks[python,mcp]"
hopsworks-mcp --transport stdio --hopsworks_host my.hopsworks.ai --project demo \
  --api_key_file ~/.hopsworks/api_key
```

Without `--transport stdio`, the server listens over HTTP on `127.0.0.1:8000`; `--host` and `--port` change the address, and a non-loopback address needs `--auth-token`.
The tools act on the project the server is logged in to, from the start options or the `login` tool.
The API key needs the `FEATURESTORE` and `TRINO` scopes for the semantic layer tools, since their queries run as the key's user, see [Who a query runs as][semantic-overview-identity].

## Tools { #semantic-agent-tools-list }

| Tool | Tag | Arguments | Returns |
| --- | --- | --- | --- |
| `list_semantic_projects` | READ | | Each semantic project's name, root path, mode, serving build, and whether it is stale. |
| `list_metrics` | READ | `semantic_project`, `tag` (optional) | CSV of the metrics: name, type, label, description and tags. `tag` keeps the metrics that set that tag schema. |
| `list_saved_queries` | READ | `semantic_project` | CSV of the [saved queries][semantic-saved-queries-agent]: name, label, description, metrics and group-bys. |
| `list_exports` | READ | `semantic_project` | CSV of the [exports][semantic-exports-list]: name, saved query, feature group, version, schedule (empty for an export run on demand only), lookback, enabled, last status, last run, last rows and last message. |
| `list_query_history` | READ | `semantic_project`, then `limit`, 20 by default, `status` and `user` (optional) | CSV of the [query history][semantic-query-history], newest first: started at, user, surface, status, duration, rows, cache outcome, error, request and execution id. A Data Owner's server reads every member's records, and `user` picks one member's. |
| `get_dimensions` | READ | `semantic_project`, `metrics` | CSV of the dimensions the metrics can be grouped by: name, type, grains and entity path. |
| `get_entities` | READ | `semantic_project`, `metrics` (optional) | CSV of the entities. |
| `get_dimension_values` | READ | `semantic_project`, `dimension`, `metrics` and `limit` (optional) | CSV of the distinct values of a dimension. |
| `query_metrics` | READ | `semantic_project`, `metrics`, then `group_by`, `where`, `order_by` and `limit` (optional) | CSV of the rows, 100 rows unless `limit` says otherwise. |
| `query_saved_query` | READ | `semantic_project`, `name`, then `group_by`, `where` and `limit` (optional) | CSV of the rows of a saved query; `group_by` and `limit` replace its own, `where` adds to its filters. 100 rows unless `limit` says otherwise. |
| `get_metrics_compiled_sql` | READ | The arguments of `query_metrics` | The SQL the query compiles to. |
| `get_semantic_project_tags` | READ | `semantic_project` | The semantic project's tags, name and value. |
| `validate_semantic_project` | READ | `semantic_project` | The status the definitions would compile to, `VALID` or `INVALID`, and their issues; no build is made. |
| `compile_semantic_project` | WRITE | `semantic_project` | The build id, its status and its issues. |
| `create_dashboard_from_metrics` | WRITE | `semantic_project`, `metrics`, then `group_by` and `title` (optional) | The id, title and URL of a Superset dashboard of the metrics, see [Dashboards in Superset][semantic-superset-create-agent]. |

Group-bys and filters take the forms of [Query metrics][semantic-query-metrics]: `customer__country`, `metric_time__month` and `{{ Dimension('order__status') }} = 'completed'`.
The CSV of `query_metrics` and `query_saved_query` is capped in length, so a large result needs a `limit` or a filter.
A metric that needs `metric_time`, such as a cumulative metric with a window, needs it in `group_by`, see [Metric types][semantic-metric-types-requirements].

`validate_semantic_project` checks the definitions as they are in HopsFS, as a compile would, and stores nothing: the build that answers queries stays the one it was.
`compile_semantic_project` makes them a build: files that have not changed return their existing build.
In `FOLLOW` mode the resulting `VALID` build answers queries at once, which undoes a promote of an older build; in `PINNED` mode only promoted builds are served, see [Serving modes][semantic-overview-serving-modes].

## Coding agents { #semantic-agent-tools-skill }

A coding agent that runs the `hops` CLI uses the `hops-semantic` skill: authoring semantic YAML over feature groups, with every metric type, the time spine and saved queries, compiling, testing metrics, and querying them with `hops semantic`.
The `hops-semantic-views` skill scopes a semantic project to one business domain and keeps it small enough for an agent to read whole.
`hops skills list` lists both, and the [project terminal][terminal] has Claude Code and Codex preinstalled with `hops` connected.

## Size a semantic project for agents { #semantic-agent-tools-size }

Keep each semantic project under 100k tokens, so that it does not swamp an agent's context window.
Count the semantic YAML under its root path and the four lists an agent reads before it queries: metrics, dimensions, entities and saved queries.
YAML and CSV of snake_case names run at about 3 characters per token, so 100k tokens is about 300,000 characters.
The tools above cut each list at 50,000 characters and say so on a last line, so a list longer than that hides the metrics or dimensions past the cut.

```bash
hops semantic show sales                                   # the root path; a terminal mounts /Projects/<project>/<dir> at /hopsfs/<dir>
grep -rlE --include='*.yml' '^(semantic_models|metrics|saved_queries):' /hopsfs/Resources/semantic/sales | xargs -r cat | wc -c
for list in metrics dimensions entities saved-queries; do hops semantic $list sales --json | wc -c; done
```

To stay under it, give each business domain its own semantic project with only the feature groups its questions need, leave out dimensions nobody groups or filters by, and add saved queries for the most-asked questions.
Two semantic projects can model the same feature group, so splitting a large project by domain loses no data.
The [Hopsworks CLI][hopsworks-cli] guide covers installing the skills into a repository with `hops init`.
