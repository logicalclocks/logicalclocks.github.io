---
description: Guides for the Hopsworks Semantic Layer, metrics defined in dbt semantic YAML over feature groups and queried by name.
---

# Semantic Layer Guides { #semantic-layer-guides }

The semantic layer compiles metric definitions written in dbt semantic YAML over feature groups, and answers metric queries with SQL it generates for Trino.
Define the metrics, compile them into a build, then query them from Python, the CLI, the UI, Spark, an agent, a dbt Semantic Layer client or a BI tool, chart them in Superset, or export them into feature groups.
Administrators turn the service on as in [Semantic Layer administration][semantic-admin].

<!-- markdownlint-disable MD030 -->
<div class="grid cards hops-start" markdown>

-   :material-sigma:{ .lg .middle } **Start here**

    ---

    Register a folder of semantic YAML, compile it, and query a metric by a dimension of another feature group.

    ```bash
    hops semantic create sales --path Resources/semantic/sales
    hops semantic compile sales --wait
    hops semantic query sales --metrics revenue --group-by customer__country
    ```

    [Overview][semantic-layer-overview] · [Define metrics][semantic-define-metrics] · [Query metrics][semantic-query-metrics]

</div>
<!-- markdownlint-enable MD030 -->

<div class="hops-task-index" markdown>

<div class="hops-task-group" markdown>
:material-file-code-outline:{ .hops-role-ico } Define
{ .hops-role-cap }

- [Overview][semantic-layer-overview]
  The service, semantic projects, builds, metrics and the serving modes.
- [Get started][semantic-init]
  Scaffold a semantic project from feature groups, optionally in a new GitHub repository.
- [Define metrics][semantic-define-metrics]
  Semantic models over feature groups, and the fields every metric has.
- [Metric types][semantic-metric-types]
  Cumulative and conversion metrics, offsets, filled gaps, semi-additive measures and SCD dimensions.
- [Time spine][semantic-time-spine]
  The feature group with one row per period that windows and offsets join to.

</div>

<div class="hops-task-group" markdown>
:material-check-decagram-outline:{ .hops-role-ico } Check
{ .hops-role-cap }

- [Edit definitions in the UI][semantic-editor]
  The YAML in the browser, validated as you type, saved without overwriting another edit.
- [Compile and builds][semantic-compile-builds]
  When builds happen, FOLLOW and PINNED, promote, and errors at file and line.
- [Validation rules][semantic-validation-rules]
  Every check of a compile, and what it reports.
- [Tags][semantic-tags]
  Schematised tags on semantic projects, metrics and saved queries, and mandatory tags.

</div>

<div class="hops-task-group" markdown>
:material-play-circle-outline:{ .hops-role-ico } Query
{ .hops-role-cap }

- [Query metrics][semantic-query-metrics]
  The Python client, the CLI, the query workbench in the UI, and the limits.
- [Saved queries][semantic-saved-queries]
  Named metric queries, run and refined from every client.
- [Query metrics on Spark][semantic-spark]
  A PySpark DataFrame of a metric query, computed on your Spark session.
- [Result cache][semantic-result-cache]
  Repeated queries answered from memory, and what makes a result fresh.
- [Query history][semantic-query-history]
  Every query on every API, who ran it, how long it took and why it failed.

</div>

<div class="hops-task-group" markdown>
:material-connection:{ .hops-role-ico } Connect
{ .hops-role-cap }

- [Connect dbt clients][semantic-connect-clients]
  dbt-sl-sdk, the Arrow Flight SQL JDBC driver, ADBC and GraphQL, with dbt's APIs.
- [Connect BI tools][semantic-bi-tools]
  Semantic projects as tables for DBeaver, JDBC and ODBC tools, Tableau and Power BI.
- [Excel and ODBC][semantic-excel-odbc]
  The Arrow Flight SQL ODBC driver, and metrics as CSV for Excel's From Web.
- [Metric exports][semantic-exports]
  Saved queries written into feature groups by scheduled jobs, and answered from them.
- [Dashboards in Superset][semantic-superset-dashboards]
  Superset 7.0 dashboards and charts from metrics, and Explore links.
- [Agent tools][semantic-agent-tools]
  The semantic layer tools of the Hopsworks MCP server.

</div>

</div>
