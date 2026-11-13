---
description: The Hopsworks Semantic Layer service, its control plane and semantic gateway, the APIs it serves, and what a semantic project, a build and a metric are.
---

# Semantic Layer Overview { #semantic-layer-overview }

The Hopsworks Semantic Layer reads metric definitions written in YAML over feature groups, and answers metric queries with SQL it generates for Trino.
A query names metrics and the dimensions to group them by; the semantic layer writes the joins and the aggregations.

## The service { #semantic-overview-service }

The semantic layer is a Hopsworks service with two parts:

- the control plane, in Hopsworks: semantic projects, their builds, the definitions editor, tags, metric exports and the query history;
- the semantic gateway, a Deployment of its own, which compiles the definitions, plans every metric query and runs it on Trino as the caller.

--8<-- "user_guides/analytics/semantic_layer/overview/semantic-gateway.html"

| The gateway serves | To | Guide |
| --- | --- | --- |
| REST, JSON, Arrow and CSV | The Python client, the `hops` CLI, the query workbench in the UI, the agent tools, Superset, Excel's From Web | [Query metrics][semantic-query-metrics], [Excel and ODBC][semantic-excel-odbc] |
| GraphQL, dbt's Semantic Layer API: metadata and `compileSql` | dbt-sl-sdk's metadata calls, GraphQL clients | [Connect dbt clients][semantic-connect-clients] |
| Arrow Flight SQL, dbt's JDBC dialect | dbt-sl-sdk queries, ADBC, the Arrow Flight SQL JDBC driver | [Connect dbt clients][semantic-connect-clients] |
| Arrow Flight SQL, tables | Superset, DBeaver, JDBC and ODBC tools, Excel, dbt's Tableau and Power BI connectors | [Connect BI tools][semantic-bi-tools], [Excel and ODBC][semantic-excel-odbc] |

Around the queries:

| Feature | Guide |
| --- | --- |
| A repeated query answered from the gateway's memory | [Result cache][semantic-result-cache] |
| A saved query written into a feature group by a scheduled job, and queries answered from it | [Metric exports][semantic-exports] |
| Every query recorded, for its members and Data Owners | [Query history][semantic-query-history] |
| The YAML edited in the UI, validated as you type | [Edit definitions in the UI][semantic-editor] |
| Dashboards from metrics on Superset 7.0 | [Dashboards in Superset][semantic-superset-dashboards] |
| The semantic layer tools of the Hopsworks MCP server | [Agent tools][semantic-agent-tools] |
| Turning it on and configuring it | [Semantic Layer administration][semantic-admin] |

## Semantic projects { #semantic-overview-projects }

A semantic project is a folder of definitions in the project's file system, registered under a name.
The folder is usually a dbt project in a git repository, holding semantic models, dimensions, entities, measures and metrics.
The name is unique in the Hopsworks project, and is made of lowercase letters, digits and underscores, starting with a letter.

| Setting | Values |
| --- | --- |
| Root path | The folder of the definitions; for a dbt project, the folder that holds `dbt_project.yml` |
| Format | `AUTO` (default), `DBT`, `NATIVE` or `MANIFEST_JSON` |
| Deployment mode | `FOLLOW` (default) or `PINNED`, see [Serving modes][semantic-overview-serving-modes] |
| Git repository | The Hopsworks git repository that holds the root path, filled in from the path |
| Owner | The Data owner its export jobs run as: the member who registers it, until a Data owner transfers it, see [The owner of a semantic project][semantic-builds-owner] |

`DBT` reads dbt project YAML, `NATIVE` reads MetricFlow YAML, and `MANIFEST_JSON` reads a dbt `semantic_manifest.json`.
With `AUTO`, a `dbt_project.yml` at the root selects `DBT`, otherwise a `semantic_manifest.json` selects `MANIFEST_JSON`, and anything else is read as `NATIVE`.

Deleting a semantic project deletes its builds and leaves the YAML files in place.

## Builds { #semantic-overview-builds }

A compile reads the definitions under the root path, checks them against the feature groups, and records the result as a build.
A build does not change once its compile ends, and has one of four statuses:

| Status | Meaning |
| --- | --- |
| `COMPILING` | The compile is running. |
| `VALID` | The definitions compiled without errors, so the build can answer queries. |
| `INVALID` | The definitions have errors, each reported at its file and line. |
| `FAILED` | The compile could not run. |

A build records the git commit it was read at, when the root path is inside a Hopsworks git repository.
Compiling files that have not changed returns their existing build.
A semantic project keeps its 20 newest builds and the build that answers queries; the `semantic_layer_builds_retained` cluster setting changes the number.

## Metrics and group-bys { #semantic-overview-metrics }

A semantic model reads one feature group.
A measure aggregates a column or an expression of a semantic model, and a metric is a named calculation over measures: a simple metric, a ratio of two metrics, an expression over other metrics, a cumulative metric over a time window, or a conversion metric between two events, see [Metric types][semantic-metric-types].

A query groups metrics by group-bys:

- dimensions, categorical or time, named `<entity>__<dimension>`, such as `customer__country`;
- entities, the keys that join semantic models;
- `metric_time`, the time axis of every metric, taken from the time dimension its measures aggregate over.

A time group-by takes a grain suffix, such as `metric_time__month`, or a custom granularity of the [time spine][semantic-time-spine], a feature group with one row per period.
The semantic layer joins feature groups along their entities, so `revenue` from `orders` can be grouped by `customer__country` from `customers`.
A [saved query][semantic-saved-queries] is a metric query defined by name in the YAML, which every client runs by name.

## Serving modes { #semantic-overview-serving-modes }

The build that answers queries is the semantic project's current build.
An `INVALID` or `FAILED` build never becomes current: queries keep the last valid build and report that it is stale.

| Mode | Current build | Suits |
| --- | --- | --- |
| `FOLLOW` | Each new valid build, as soon as it compiles. | Your own clone, on a feature branch. |
| `PINNED` | The last build promoted; a new valid build waits for a promote. | A production repository that only CI or an owner pulls. |

A promote works in both modes.
In `FOLLOW` mode a promote of an older valid build rolls back until the next valid compile.
[Compile and builds][semantic-compile-builds] has the commands.

## How a query runs { #semantic-overview-query-path }

1. A client sends the query to the semantic gateway, with the caller's own credential: an API key, or the session of the UI.
2. The gateway generates the SQL for the query from the current build.
3. The SQL runs on Trino as the caller's own Trino user, `<project>__<user>`, so a query reads only the data that member can read, unless the gateway's [result cache][semantic-result-cache] holds the result of the same query by the same user over the same feature group commits.
4. The rows come back as an Arrow stream or as JSON.

The Python client, the `hops` CLI, the UI and the agent tools all query through the gateway, from inside and outside the cluster.
dbt Semantic Layer clients read metadata over GraphQL and run queries over Arrow Flight SQL, see [Connect dbt clients][semantic-connect-clients], and BI tools read it as tables, see [Connect BI tools][semantic-bi-tools].
A saved query's exports write its rows into feature groups on a schedule, and the gateway answers the saved query from them while they hold its exact rows, see [Metric exports][semantic-exports].
The gateway records every query it runs in the [query history][semantic-query-history].
Superset charts query through the gateway too, over Arrow Flight SQL on one database connection of each member per Hopsworks project, see [Who can see what][semantic-superset-access].
The semantic layer reads the offline feature store.

## Prerequisites { #semantic-overview-prerequisites }

- An administrator turns the semantic layer on with the Helm value `global._hopsworks.semanticLayer.enabled: true`, which installs the semantic gateway and adds **Semantic Layer** to the project sidebar, see [Semantic Layer administration][semantic-admin].
  While it is off, the semantic layer endpoints answer 404 `SEMANTIC_LAYER_DISABLED`.
- Data owners and data scientists of a project create, compile, promote and delete semantic projects; every member can list them and query their metrics.
- Only data owners run [metric exports][semantic-exports] by hand, and an export's job runs as the semantic project's [owner][semantic-builds-owner], who must be a data owner.
- An API key needs the `FEATURESTORE` scope for semantic projects and builds.
  Everything the gateway answers, from listing metrics to running a query, also needs the `TRINO` scope, since the gateway connects to Trino as the key's user.
