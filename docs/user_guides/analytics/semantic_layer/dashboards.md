---
description: How to build Superset dashboards from the metrics of a semantic project, open a metric in Explore, chart the tables of your semantic connection, and who can see what.
---

# Dashboards in Superset { #semantic-superset-dashboards }

Superset reads metrics over Arrow Flight SQL, through one database connection of your own per Hopsworks project: the connection shows each semantic project of the project as a schema, with a `metrics` table and one table per saved query, the [BI tables][semantic-bi-tables].
A chart on a dataset of those tables names metrics and group-bys, which the semantic layer answers as a metric query.
Hopsworks keeps the connections in step with the project, builds a dashboard from a semantic project's metrics, and opens a metric in Superset's Explore view.
The examples use the `sales` semantic project from [Define metrics][semantic-define-metrics].

## Prerequisites { #semantic-superset-prerequisites }

- Superset 7.0, in the Hopsworks Superset image, which ships the driver of the connections.
- The semantic layer and Superset enabled on the cluster, and the `superset_semantic_enabled` cluster setting on, which it is by default, see [For administrators][semantic-superset-admin].
- The Superset service in the project.
- A semantic project with a valid build, see [Compile and builds][semantic-compile-builds].
- The Data owner or Data scientist role in the project.
  An API key needs the `FEATURESTORE` scope to create a dashboard or an Explore link.

## What a dashboard holds { #semantic-superset-layout }

A dashboard from metrics reads a dataset of the `metrics` table in the semantic project's schema on your connection, and holds, top to bottom:

- a big number with a trendline of the first metric, beside a line chart of the first metric;
- a line chart of each further metric over `metric_time`, two to a row;
- a table of every metric broken down by the group-bys, sorted by the first metric, descending;
  when one of the metrics needs `metric_time`, such as a cumulative metric with a window, the table also breaks down by `metric_time` at the dashboard's grain;
- a multi-select filter on each group-by, at most three, applied to every chart.

| Choice | Value |
| --- | --- |
| Metrics | One to eight, of the semantic project's current build. |
| Group-bys | The ones given, each a categorical dimension or an entity that every metric can be grouped by. Without them, the table breaks down by the first categorical dimension the metrics share, and the filters cover up to three of those dimensions. |
| Grain of `metric_time` | A day when every metric can be grouped by day, else the finest grain they share. |
| Title | The one given, or `<semantic project>: <metric labels>`, such as `sales: Revenue, Orders`. |

The charts are named after the labels of the metrics and group-bys, or their names where they have no label: `Revenue` for the big number, `Revenue over time` for a line chart, and `Revenue, Orders by customer__country` for the table.
When the metrics share no categorical dimension and no group-by is given, the dashboard has no table and no filters.
A table that also breaks down by `metric_time` has "over time" added to its name, such as `Revenue, Revenue 7d by customer__country over time`.
The metrics must share a `metric_time`, so metrics aggregated over time dimensions of different grains do not go on one dashboard.

Creating a dashboard with the title of one you created before rebuilds that dashboard in place: it keeps its id and URL, and its charts are replaced.
Every chart that was on it is taken off, and deleted when it is on no other dashboard, so a chart you added to a generated dashboard by hand goes with the rebuild unless another dashboard holds it too.
The same title from another member creates that member's own dashboard.

## Create a dashboard { #semantic-superset-create }

### In the UI { #semantic-superset-create-ui }

Open **Semantic Layer** in the project sidebar and pick a semantic project.
On the **Metrics** card of its overview, tick the metrics and click **Create dashboard**, or click a metric and then **Create dashboard** in its sheet.
The **Create a Superset dashboard** dialog takes:

- **Metrics**, at most 8;
- **Break down by**, one categorical dimension that every picked metric shares, optional;
- **Title**, optional.

**Create** builds the dashboard and opens it in a new tab, and the notification that follows links it.
**Create dashboard** in a saved query's sheet opens the dialog on the saved query, see [Dashboards from a saved query][semantic-saved-queries-dashboards].
The buttons show when the semantic layer, Trino and Superset are enabled, `superset_semantic_enabled` is on, and the project has the Superset service.

### From the CLI { #semantic-superset-create-cli }

```bash
hops semantic dashboard sales --metrics revenue,orders --group-by customer__country --title "Sales overview"
```

```text
Created dashboard 12 "Sales overview": https://<hopsworks host>/hopsworks-api/superset/dashboard/12/?projectId=119
```

```bash
hops semantic dashboard sales --metrics revenue,revenue_per_order --json
```

```text
{
  "id": 13,
  "title": "sales: Revenue, Average order value",
  "url": "https://<hopsworks host>/hopsworks-api/superset/dashboard/13/?projectId=119"
}
```

| Option | Meaning |
| --- | --- |
| `--metrics` | Metric names, one to eight, comma-separated or repeated; required unless `--saved-query` is given. |
| `--group-by` | Categorical dimensions or entities for the table and the filters, comma-separated or repeated. |
| `--saved-query` | A [saved query][semantic-saved-queries-dashboards] to chart, in place of `--metrics` and `--group-by`. |
| `--title` | The dashboard title. |
| `--json` | Print the id, title and URL as JSON. |

A refused request prints one line with the HTTP status, the error code and the reason, and exits 1, see [Errors][semantic-superset-errors].

### From Python { #semantic-superset-create-python }

```python
import hopsworks


project = hopsworks.login()
sales = project.get_semantic_layer_api().get_project("sales")
dashboard = sales.create_dashboard(
    ["revenue", "orders"], group_by=["customer__country"], title="Sales overview"
)
print(dashboard["id"], dashboard["url"])
```

```text
12 https://<hopsworks host>/hopsworks-api/superset/dashboard/12/?projectId=119
```

`create_dashboard` returns a dict with the dashboard's Superset `id`, its `title`, and the `url` that opens it through Hopsworks.
`create_dashboard(saved_query="revenue_by_country")` charts a saved query instead.
A refusal raises `SemanticLayerException`.
The client works from outside the cluster with an API key, since Hopsworks builds the dashboard.

### From an agent { #semantic-superset-create-agent }

The Hopsworks MCP server has the tool `create_dashboard_from_metrics`, tagged WRITE, among its [semantic layer tools][semantic-agent-tools-list]:

```json
{"semantic_project": "sales", "metrics": ["revenue", "orders"], "group_by": ["customer__country"], "title": "Sales overview"}
```

```json
{"id": 12, "title": "Sales overview", "url": "https://<hopsworks host>/hopsworks-api/superset/dashboard/12/?projectId=119"}
```

The dashboard belongs to the user the server is logged in as.
Coding agents that run the `hops` CLI build dashboards with `hops semantic dashboard`, as the `hops-semantic` and `hops-superset` skills describe.

## Open a metric in Explore { #semantic-superset-explore }

In a metric's sheet, **Open in Superset** opens Superset's Explore view in a new tab, with a line chart of the metric over `metric_time` on the dataset of the semantic project's `metrics` table on your connection, at the grain a dashboard would use.
Nothing is saved in Superset until you save the chart there.

```python
import hopsworks


project = hopsworks.login()
sales = project.get_semantic_layer_api().get_project("sales")
print(sales.explore_url("revenue"))
```

The URL has the form `https://<hopsworks host>/hopsworks-api/superset/explore/?form_data=<chart>&projectId=<project id>`, where `<chart>` is the URL-encoded chart definition.
An Explore link fails for the same reasons as a dashboard, see [Errors][semantic-superset-errors].

## Your semantic connection { #semantic-superset-connections }

Each Data owner and Data scientist of a project with at least one semantic project has one Superset database connection to the semantic layer for the project:

| Property | Value |
| --- | --- |
| Name | `Semantic__<superset user>`, where the Superset user is `<project>__<username>_superset`, such as `Semantic__demo__meb10000_superset`. |
| Schemas | One per semantic project of the project, named as the semantic project, such as `sales`. |
| Tables | In each schema, `metrics`, and one table per saved query, named as the saved query, see [The tables][semantic-bi-tables]. |
| SQL Lab | The connection is listed in SQL Lab. |

**Settings** > **Database connections** lists your connection, next to your Trino connection.
Creating or deleting a semantic project changes the schemas of the connection, not the connection.

## Build charts on the tables { #semantic-superset-charts }

Create a dataset on your connection, with the semantic project's name as the schema and `metrics` or a saved query as the table, see [Creating Datasets][creating-datasets].
A dashboard from metrics creates the dataset of the tables it charts, and reuses it afterwards.
Create a chart on the dataset as on any other, see [Creating Charts][creating-charts].

A chart on the dataset:

- reads a metric as `SUM(<metric>)`, such as `SUM(revenue)`: an aggregate around a metric column returns the metric itself, computed by its definition at the chart's group-bys, see [A metric column is the metric][semantic-bi-metric-columns];
- groups by the semantic project's dimensions and entities, named as in queries, such as `customer__country`;
- puts time on a time column, such as `metric_time__day`, at the grain of the chart's time grain control;
- filters on dimensions, and on time with a time range.

On a dataset that Hopsworks created, each metric is a saved metric of the dataset, named after the metric, and the time columns are marked as temporal.
On a dataset you create yourself, add each metric as a metric with the SQL expression `SUM("<metric>")`.

Superset sends each chart as one SQL statement over the table, which the semantic layer runs as a metric query at the chart's own group-bys and grain.
A ratio or a count of distinct customers is right at every grain, since the semantic layer computes the metric for the grain asked for and never adds up the rows of a finer one.

A [saved query's table][semantic-saved-queries-superset-table] has only the saved query's metrics and group-bys, and its rows are under the saved query's filters.

SQL Lab runs the same statements on the connection, with each table named with its schema, such as `SELECT customer__country, SUM(revenue) FROM "sales"."metrics" GROUP BY customer__country`; see [The SQL][semantic-bi-sql] for what the tables accept.

## Who can see what { #semantic-superset-access }

Hopsworks keeps these per member and project:

| Object | Name | What it does |
| --- | --- | --- |
| Database connection | `Semantic__<superset user>` | One per Data owner and Data scientist of a project with a semantic project. The member's own Superset role, `HW_role_<superset user>`, has access to it, as to the member's Trino connection. |
| API key | `superset-semantic-<project>` | An API key of the member, with the `FEATURESTORE` and `TRINO` scopes, kept as the member's secret `superset_semantic_<project>`. The member's semantic connection sends its queries with it, and Superset stores it encrypted. |

Feature store restricted members keep their Superset account and Trino connection, and have no semantic connection.
Observers have no Superset account.

Hopsworks brings the connections in line with the project when a member is added, removed or changes role, when the project's first semantic project is created or its last one deleted, and every ten minutes.
Creating a dashboard or an Explore link creates the caller's connection first when it is missing.

| Event | Effect |
| --- | --- |
| The project's first semantic project is created | A connection for each Data owner and Data scientist. |
| Another semantic project is created or deleted | Its schema appears or goes; the connections stay as they are. |
| The project's last semantic project is deleted | The connections, and each member's key and secret, are deleted. |
| A member is removed, or gets a role other than Data owner or Data scientist | The member's key and secret are deleted, and so is their connection, except one that holds datasets, which Superset keeps with the revoked key. The Superset account of a removed member is deleted, or deactivated when it created datasets, charts or dashboards, which Superset keeps. |
| A member's key is deleted, or loses a scope | Hopsworks creates a new key and writes it into the member's connection. |
| The project is deleted | The connections, keys and secrets are deleted. |

A chart runs with the access of the member whose connection its dataset is on, not of the member who views it.
Charts you build on your connection run on Trino as you, as metric queries from Python, the CLI, the query workbench and the agent tools do, see [Who a query runs as][semantic-overview-identity].

A dashboard from metrics belongs to the member who created it: Hopsworks builds it through that member's own Superset account, on datasets of that member's connection, so Superset makes them the editor of the dashboard and of its charts.
A dashboard shared in the project, with another project or made public shows its author's view of the data to every viewer, as a shared dashboard on a Trino connection does, see [Sharing Dashboards][sharing-dashboards].

## Limits { #semantic-superset-limits }

| Limit | Why |
| --- | --- |
| Row count is not available on the tables. | A table has no rows of its own to count: each statement is a metric query. `COUNT(*)` is refused, and the datasets offer no row count metric. |
| A chart takes no custom SQL over columns. | The semantic layer generates the SQL from metric and group-by names, so an expression such as `revenue * 2`, a join and a subquery are refused, see [What is refused][semantic-bi-refused]. Define the calculation as a metric instead. |
| A metric is selected once per chart. | `SUM(revenue)` and `AVG(revenue)` both mean `revenue`, and a statement with both is refused. |
| A generated dashboard holds at most 8 metrics and 3 filters. | A dashboard request with more metrics is refused; build a second dashboard for the others. |
| A chart of a metric that needs `metric_time`, such as a cumulative metric with a window, groups by a `metric_time` column. | The semantic layer refuses the query of a chart without it, such as a table you build without `metric_time`, see [Metric types][semantic-metric-types-requirements]. |
| The rows and the query time of a chart follow the [query limits][semantic-query-limits]. | Each chart is a metric query on the gateway. |

## Errors { #semantic-superset-errors }

| Error | Code | Status | Meaning |
| --- | --- | --- | --- |
| `SEMANTIC_LAYER_ILLEGAL_ARGUMENT` | 600004 | 400 | No metric or more than eight, a blank name, a title longer than 500 characters, or metrics or group-bys given with a saved query. |
| `SEMANTIC_LAYER_INVALID_QUERY` | 600012 | 400 | An unknown metric, a group-by that is not a categorical dimension or entity every metric can be grouped by, or metrics that share no `metric_time`. |
| `SEMANTIC_LAYER_NOT_FOUND` | 600001 | 404 | No semantic project with that id, or no saved query of that name. |
| `SEMANTIC_LAYER_FORBIDDEN` | 600003 | 403 | The caller's role has no semantic connection: only Data owners and Data scientists have one. |
| `SEMANTIC_LAYER_NO_VALID_BUILD` | 600013 | 409 | The semantic project has no valid build; compile it and fix its errors. |
| `SEMANTIC_LAYER_DASHBOARDS_DISABLED` | 600014 | 503 | `superset_semantic_enabled` is off, Superset is not enabled, or the project has no Superset service. |
| `SEMANTIC_LAYER_GATEWAY_ERROR` | 600010 | 502 | The semantic layer gateway could not be reached, or failed to list the metrics and group-bys. |
| `SEMANTIC_LAYER_SUPERSET_ERROR` | 600015 | 503 | Superset refused a request or did not answer. |

In Python, each is a `SemanticLayerException` with the numeric code in `error_code`.

## For administrators { #semantic-superset-admin }

The `superset_semantic_enabled` cluster setting, `true` by default, turns on the members' semantic connections in Superset, the dashboard and Explore requests, and the buttons in the UI.
It takes effect only while the semantic layer and Superset are enabled.
Set to `false`, or with the semantic layer or Superset turned off, Hopsworks refuses dashboard and Explore requests with 503, and within ten minutes deletes every member's semantic key and secret and the semantic connections.
A connection that holds datasets stays, with its key revoked, so its charts fail; the datasets, charts and dashboards stay in Superset.
Superset pods reach the gateway's Arrow Flight SQL port inside the cluster, see [What runs where][semantic-admin-components].
Change it under **Cluster Settings** > **Configuration**, see [Cluster Configuration][cluster-configuration].

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-class"></code> [`SemanticProject`][hopsworks_common.semantic_layer.SemanticProject]
        - <code class="doc-symbol doc-symbol-method"></code> [`create_dashboard`][hopsworks_common.semantic_layer.SemanticProject.create_dashboard]
        - <code class="doc-symbol doc-symbol-method"></code> [`explore_url`][hopsworks_common.semantic_layer.SemanticProject.explore_url]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>
