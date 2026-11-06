---
description: Guides for the Hopsworks Semantic Layer, metrics defined in dbt semantic YAML over feature groups and queried by name.
---

# Semantic Layer Guides { #semantic-layer-guides }

The semantic layer compiles metric definitions written in dbt semantic YAML over feature groups, and answers metric queries with SQL it generates for Trino.
Define the metrics, compile them into a build, then query them from Python, the CLI, the UI or an agent, or chart them in Superset.

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
  Semantic projects, builds, metrics and the serving modes.
- [Get started][semantic-init]
  Scaffold a semantic project from feature groups, optionally in a new GitHub repository.
- [Define metrics][semantic-define-metrics]
  Semantic models over feature groups, and simple, ratio and derived metrics.
- [Tags][semantic-tags]
  Schematised tags on semantic projects and metrics, and mandatory tags.

</div>

<div class="hops-task-group" markdown>
:material-play-circle-outline:{ .hops-role-ico } Run
{ .hops-role-cap }

- [Compile and builds][semantic-compile-builds]
  When builds happen, FOLLOW and PINNED, promote, and errors at file and line.
- [Query metrics][semantic-query-metrics]
  The Python client, the CLI, the query workbench in the UI, and the limits.
- [Dashboards in Superset][semantic-superset-dashboards]
  Superset 7.0 dashboards and charts from metrics, and Explore links.
- [Agent tools][semantic-agent-tools]
  The semantic layer tools of the Hopsworks MCP server.

</div>

</div>
