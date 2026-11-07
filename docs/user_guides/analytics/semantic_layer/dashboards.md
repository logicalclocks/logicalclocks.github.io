---
description: How to build Superset 7.0 dashboards from the metrics of a semantic project, open a metric in Explore, chart a semantic view, and who can see what.
---

# Dashboards in Superset { #semantic-superset-dashboards }

Superset 7.0 reads metrics through the Hopsworks semantic layer: each semantic project is a semantic view in Superset, and a chart on a view names metrics and group-bys, which the semantic layer answers as a metric query.
Hopsworks keeps the views in step with the project, builds a dashboard from a semantic project's metrics, and opens a metric in Superset's Explore view.
The examples use the `sales` semantic project from [Define metrics][semantic-define-metrics].

## Prerequisites { #semantic-superset-prerequisites }

- Superset 7.0 with the Hopsworks semantic layer extension, which the Hopsworks Superset image ships.
  Semantic layers and views are an extension point that Superset added in 7.0; on Superset 6.0, chart metrics through datasets, see [Superset 6.0][semantic-superset-6].
- The semantic layer and Superset enabled on the cluster, and the `superset_semantic_enabled` cluster setting on, which it is by default, see [For administrators][semantic-superset-admin].
- The Superset service in the project.
- A semantic project with a valid build, see [Compile and builds][semantic-compile-builds].
- The Data owner or Data scientist role in the project.
  An API key needs the `FEATURESTORE` scope to create a dashboard or an Explore link.

## What a dashboard holds { #semantic-superset-layout }

A dashboard from metrics reads the semantic project's view, and holds, top to bottom:

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

In a metric's sheet, **Open in Superset** opens Superset's Explore view in a new tab, with a line chart of the metric over `metric_time` on the semantic project's view, at the grain a dashboard would use.
Nothing is saved in Superset until you save the chart there.

```python
import hopsworks


project = hopsworks.login()
sales = project.get_semantic_layer_api().get_project("sales")
print(sales.explore_url("revenue"))
```

The URL has the form `https://<hopsworks host>/hopsworks-api/superset/explore/?form_data=<chart>&projectId=<project id>`, where `<chart>` is the URL-encoded chart definition.
An Explore link fails for the same reasons as a dashboard, see [Errors][semantic-superset-errors].

## Build charts on a semantic view { #semantic-superset-charts }

Each semantic project is a view in Superset with the semantic project's name.
**Datasets** lists it with the type **Semantic View**, and the dataset picker of a new chart tags it **Semantic View**.
Create a chart on it as on a dataset, see [Creating Charts][creating-charts].

A chart on a view:

- picks metrics from the metrics of the semantic project's current build, with their labels and descriptions;
- groups by the semantic project's dimensions and entities, named as in queries, such as `customer__country`, and by `metric_time`;
- takes the grain of `metric_time`, or of another time dimension, from the grains the metrics can be queried at, in the chart's time grain control;
- filters on dimensions, and on time with a time range;
- keeps the top series by a metric with a series limit.

Superset sends each chart to the semantic layer as a metric query at the chart's own group-bys and grain, so the semantic layer computes every metric at that grain.
The view reports a simple metric with the aggregation of its measure, and a percentile and every other metric, such as a ratio, a derived, a cumulative or a conversion metric, with the aggregation `OTHER`, so Superset does not aggregate their values again.
A native filter lists its options with a query without metrics, so it offers every value of its dimension.

Each [saved query][semantic-saved-queries-superset-view] is a view too, named `<semantic project>.<saved query>`, which offers only the saved query's metrics and group-bys and runs every chart as the saved query.

## Who can see what { #semantic-superset-access }

Hopsworks keeps these Superset objects per project:

| Object | Name | What it does |
| --- | --- | --- |
| Semantic layer | `HopsworksSemantic__<project>` | Connects Superset to the project's semantic projects. Hopsworks creates it as the Superset admin, once the project has a semantic project. |
| Semantic view | The semantic project's name, and `<semantic project>.<saved query>` | One per semantic project of the project, and one per saved query of its build that answers queries. |
| Role | `HW_semantic_<project>` | Read access to the layer and its views. Its users are the Superset accounts of the project's data owners and data scientists. |
| API key | `superset-semantic-<project>` | An API key of the project owner, with the `FEATURESTORE` and `TRINO` scopes, kept as the owner's secret `superset_semantic_<project>`. The layer sends every chart's query with it. |

Hopsworks brings them in line with the project when a member is added, removed or changes role, when a semantic project is created or deleted, before every dashboard or Explore request, and every ten minutes.
A member who has no Superset account yet joins the role once the account exists; creating a dashboard or an Explore link creates the caller's account first.
When the project changes owner, Hopsworks creates a key for the new owner, writes it into the layer and deletes the old key, so the layer keeps its views and charts.
Deleting a semantic project deletes its view, and deleting the project deletes the layer, its views, the role and the key.

Charts on the layer run on Trino as the project owner, through the layer's API key, so every member in the role sees the same rows, read from the feature groups of the project and those shared with it.
Metric queries from Python, the CLI, the query workbench and the agent tools run as the caller instead, see [How a query runs][semantic-overview-query-path].

A dashboard from metrics belongs to the member who created it: Hopsworks builds it through that member's own Superset account, so Superset makes them the editor of the dashboard and of its charts.
The dashboard is published with no viewers set, so Superset lists it to every user who can read its view, which is every member in the project's semantic role.

## Limits { #semantic-superset-limits }

| Limit | Why |
| --- | --- |
| A chart cannot filter on a metric value. | Superset 7.0 passes a view only the filters on its dimensions and drops a filter on a metric, so the chart shows the unfiltered rows. Filter on metric values with `having` in [Python][semantic-query-python]. |
| Group-bys are the semantic project's dimensions and entities, and `metric_time`. | The semantic layer generates the SQL from metric and group-by names, so a view takes no custom SQL column, custom SQL metric, or SQL `WHERE` or `HAVING` clause. |
| A generated dashboard holds at most 8 metrics and 3 filters. | A dashboard request with more metrics is refused; build a second dashboard for the others. |
| Superset never aggregates a ratio or another non-additive metric again. | Summing ratios or distinct counts across groups gives a wrong number, so the view reports them with the aggregation `OTHER` and every chart asks the semantic layer at its own grain. |
| `ILIKE`, `NOT LIKE` and `NOT ILIKE` match case-insensitively through `LOWER(...) LIKE LOWER(...)`, and a pattern cannot contain `{{`. | Trino has no `ILIKE`, and the semantic layer reads `{{` as the start of a dimension reference. |
| A chart of a metric that needs `metric_time`, such as a cumulative metric with a window, groups by `metric_time`. | The semantic layer refuses the query of a chart without it, such as a table you build without `metric_time`, see [Metric types][semantic-metric-types-requirements]. |
| A filter offers at most 10,000 values of a dimension. | Superset asks a view for at most 10,000 values of a column. |
| A series limit cannot group the other series, or rank them over another time range than the chart's. | The semantic layer ranks the groups under the query's own filters and returns the top groups only, with no group for the rest. |
| The rows and the query time of a chart follow the [query limits][semantic-query-limits]. | Each chart is a metric query on the gateway. The line charts of a generated dashboard read up to 10,000 rows, and its table up to 1,000. |

## Superset 6.0 { #semantic-superset-6 }

A cluster on Superset 6.0 has no semantic views, so a dashboard or Explore request is refused with `SEMANTIC_LAYER_DASHBOARDS_DISABLED`, and the message says that Superset has no `extensions.hopsworks.semantic-layer.hopsworks` semantic layer type.
Chart a metric there through a virtual dataset over the SQL of a metric query, which [`hops semantic sql`][semantic-query-cli] prints:

```bash
hops semantic sql sales --metrics revenue,orders --group-by metric_time__month,customer__country
```

Create the dataset from that SQL on the project's Trino connection with **Create dataset from SQL query**, see [Creating Datasets][creating-datasets].

- The SQL names its tables in full, so the connection's default catalog does not matter.
- The dataset keeps the SQL it was created with: create it again after the definitions change.
- It has a column per group-by and per metric, one row per group, so chart a ratio or a distinct count at the dataset's own grain; summing it over coarser groups gives a wrong number.

## Errors { #semantic-superset-errors }

| Error | Code | Status | Meaning |
| --- | --- | --- | --- |
| `SEMANTIC_LAYER_ILLEGAL_ARGUMENT` | 590004 | 400 | No metric or more than eight, a blank name, a title longer than 500 characters, or metrics or group-bys given with a saved query. |
| `SEMANTIC_LAYER_INVALID_QUERY` | 590012 | 400 | An unknown metric, a group-by that is not a categorical dimension or entity every metric can be grouped by, or metrics that share no `metric_time`. |
| `SEMANTIC_LAYER_NOT_FOUND` | 590001 | 404 | No semantic project with that id, or no saved query of that name. |
| `SEMANTIC_LAYER_NO_VALID_BUILD` | 590013 | 409 | The semantic project has no valid build; compile it and fix its errors. |
| `SEMANTIC_LAYER_DASHBOARDS_DISABLED` | 590014 | 503 | `superset_semantic_enabled` is off, Superset is not enabled, the project has no Superset service, or Superset has no Hopsworks semantic layer type. |
| `SEMANTIC_LAYER_GATEWAY_ERROR` | 590010 | 502 | The semantic layer gateway could not be reached, or failed to list the metrics and group-bys. |
| `SEMANTIC_LAYER_SUPERSET_ERROR` | 590015 | 503 | Superset refused a request or did not answer, or has no view of the semantic project. |

In Python, each is a `SemanticLayerException` with the numeric code in `error_code`.

## For administrators { #semantic-superset-admin }

The `superset_semantic_enabled` cluster setting, `true` by default, turns on the Superset semantic layers, the dashboard and Explore requests, and the buttons in the UI.
It takes effect only while the semantic layer and Superset are enabled.
Set to `false`, Hopsworks stops keeping the layers in step and refuses dashboard and Explore requests with 503; the layers, views and dashboards already in Superset stay.
Change it under **Cluster Settings** > **Configuration**, see [Cluster Configuration][cluster-configuration].

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-class"></code> [`SemanticProject`][hopsworks_common.semantic_layer.SemanticProject]
        - <code class="doc-symbol doc-symbol-method"></code> [`create_dashboard`][hopsworks_common.semantic_layer.SemanticProject.create_dashboard]
        - <code class="doc-symbol doc-symbol-method"></code> [`explore_url`][hopsworks_common.semantic_layer.SemanticProject.explore_url]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>
