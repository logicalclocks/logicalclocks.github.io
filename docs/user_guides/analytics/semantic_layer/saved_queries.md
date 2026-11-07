---
description: How to define saved queries in semantic YAML, list and run them from the CLI, Python, the UI and an agent, refine them, show their SQL, and chart them in Superset.
---

# Saved Queries { #semantic-saved-queries }

A saved query is a metric query defined by name in the semantic project's YAML: its metrics, group-bys, filters, order and limit.
It compiles with the build, and every client runs it by name, refined with its own group-bys, filters or limit.
The examples use the `sales` semantic project of [Define metrics][semantic-define-metrics].

## Define a saved query { #semantic-saved-queries-define }

Saved queries go under `saved_queries:` in any YAML file under `model-paths`:

```yaml
saved_queries:
  - name: revenue_by_country
    label: Revenue by country
    description: Monthly revenue and orders per country, cancelled orders left out.
    query_params:
      metrics:
        - revenue
        - orders
      group_by:
        - TimeDimension('metric_time', 'month')
        - Dimension('customer__country')
      where:
        - "{{ Dimension('order__status') }} != 'cancelled'"
      order_by:
        - TimeDimension('metric_time', 'month')
        - Metric('revenue').descending(True)
    config:
      meta:
        hopsworks:
          tags:
            domain: "sales"
```

| Key | Value |
| --- | --- |
| `name` | Lower case letters, digits and underscores, unique among the saved queries. |
| `label`, `description` | Shown in the UI and in the listings; the label is the name when not set. |
| `query_params.metrics` | Metric names. |
| `query_params.group_by` | `Dimension('<entity>__<dimension>')`, `TimeDimension('<name>', '<grain>')` or `Entity('<entity>')`; a call takes `.grain('<grain>')` and `.date_part('<part>')`. |
| `query_params.where` | Filters in the call syntax of queries, combined with `AND`. |
| `query_params.order_by` | Metrics, as `Metric('<metric>')`, and group-bys of the saved query; `.descending(True)` sorts descending. |
| `query_params.limit` | The most rows to return. |
| `config.meta.hopsworks.tags` | Tags, tag schema name to value, checked against their schemas as the [tags of a metric][semantic-tags-metrics] are. |

A compile checks each saved query, its metrics, group-bys, order and filters, under the `SAVED_QUERY` and `WHERE_FILTER` [rules][semantic-validation-rules], then plans it once, so a saved query that would fail is an error at its file and line.
A saved query's `exports` write its rows into feature groups, see [Export to a feature group][semantic-saved-queries-exports].

## List the saved queries { #semantic-saved-queries-list }

=== "CLI"

    ```bash
    hops semantic saved-queries sales
    ```

    ```text
    NAME                LABEL               METRICS         GROUP-BYS
    ------------------  ------------------  --------------  ------------------------------------
    revenue_by_country  Revenue by country  revenue,orders  metric_time__month,customer__country
    ```

=== "Python"

    ```python
    import hopsworks


    project = hopsworks.login()
    sales = project.get_semantic_layer_api().get_project("sales")
    for saved in sales.list_saved_queries():
        print(saved.name, saved.metrics, saved.group_by, saved.order_by)
    ```

    ```text
    revenue_by_country ['revenue', 'orders'] ['metric_time__month', 'customer__country'] [{'name': 'metric_time__month', 'descending': False}, {'name': 'revenue', 'descending': True}]
    ```

The listing names each group-by and order-by as a query does, such as `metric_time__month`.
`hops semantic saved-queries sales --json` prints every field, and the gateway lists them at `GET saved-queries`:

```json
{
  "buildId": 12,
  "stale": false,
  "savedQueries": [
    {
      "name": "revenue_by_country",
      "label": "Revenue by country",
      "description": "Monthly revenue and orders per country, cancelled orders left out.",
      "metrics": ["revenue", "orders"],
      "groupBy": ["metric_time__month", "customer__country"],
      "where": ["{{ Dimension('order__status') }} != 'cancelled'"],
      "orderBy": [{"name": "metric_time__month"}, {"name": "revenue", "descending": true}],
      "limit": null,
      "tags": {"domain": "sales"},
      "exports": []
    }
  ]
}
```

In the UI, the **Saved queries** card of the semantic project's overview lists them; clicking one shows its metrics, group-bys, filters, order, limit and tags, and the status of its exports.

## Run a saved query { #semantic-saved-queries-run }

=== "CLI"

    ```bash
    hops semantic query sales --saved-query revenue_by_country -o csv
    ```

    ```text
    metric_time__month,customer__country,revenue,orders
    2026-01-01,SE,140.25,2
    2026-01-01,DE,60.0,1
    2026-02-01,SE,30.0,1
    2026-02-01,DE,15.5,1
    2026-03-01,US,55.75,1
    ```

=== "Python"

    ```python
    import hopsworks


    project = hopsworks.login()
    sales = project.get_semantic_layer_api().get_project("sales")
    df = sales.query(saved_query="revenue_by_country")
    ```

`--saved-query` takes the place of `--metrics`, and `saved_query=` of `metrics`; giving both is refused.
An unknown saved query is 404 `SEMANTIC_LAYER_NOT_FOUND`:

```text
Error: Semantic layer request on 'sales' failed (HTTP 404, SEMANTIC_LAYER_NOT_FOUND): no saved query 'revenue_by_region'
```

In the UI, **Run** in the saved query's sheet opens the query workbench on the saved query and runs it.
Its metrics are fixed and its filters shown; the group-bys, order and limit picked there replace its own, and added filters narrow it.

Over REST, the query body takes `"savedQuery": "<name>"` and no `metrics`, see [Query over REST][semantic-query-rest].

## Refine a saved query { #semantic-saved-queries-refine }

A query of a saved query can change it:

| Part | A query that gives it |
| --- | --- |
| Group-bys | Replace the saved ones. An empty list of group-bys asks for totals; leaving them out keeps the saved ones. |
| Order | Replaces the saved order. A saved order by a group-by the query's group-bys leave out is dropped. |
| Limit | Replaces the saved limit. |
| `where` and structured filters | Are added to the saved filters, combined with `AND`. |
| `having`, time range, offset, group limit | Apply as in any query; a saved query has none of its own. |
| Metrics | Are refused: a saved query's metrics are its own. |

```bash
hops semantic query sales --saved-query revenue_by_country --group-by customer__country -o csv
```

```text
customer__country,revenue,orders
SE,170.25,3
DE,75.5,2
US,55.75,1
```

The saved order by month is dropped with the month, and the order by revenue, descending, stays.

```bash
hops semantic query sales --saved-query revenue_by_country \
  --where "{{ Dimension('customer__country') }} = 'SE'" -o csv
```

```text
metric_time__month,customer__country,revenue,orders
2026-01-01,SE,140.25,2
2026-02-01,SE,30.0,1
```

The totals of a saved query need an empty list of group-bys, which the CLI cannot send, so they are a Python or REST query:

```python
import hopsworks


project = hopsworks.login()
sales = project.get_semantic_layer_api().get_project("sales")
print(sales.query(saved_query="revenue_by_country", group_by=[]))
```

```text
   revenue  orders
0    301.5       6
```

Over REST, the body is `{"savedQuery": "revenue_by_country", "groupBy": []}`.

## Show the SQL { #semantic-saved-queries-sql }

=== "CLI"

    ```bash
    hops semantic sql sales --saved-query revenue_by_country
    hops semantic query sales --saved-query revenue_by_country --explain
    ```

=== "Python"

    ```python
    import hopsworks


    project = hopsworks.login()
    sales = project.get_semantic_layer_api().get_project("sales")
    print(sales.sql(saved_query="revenue_by_country"))
    ```

Both print the Trino SQL of the saved query, refined by the same options as a query, without running it.
In the UI, **Show SQL** in the saved query's sheet shows it under the saved query's definition.

## Export to a feature group { #semantic-saved-queries-exports }

An export writes a saved query's rows into a feature group, which a job refreshes on a schedule or when a Data Owner runs it:

```yaml
saved_queries:
  - name: daily_revenue_by_country
    query_params:
      metrics:
        - revenue
      group_by:
        - TimeDimension('metric_time', 'day')
        - Dimension('customer__country')
    exports:
      - name: revenue_by_country_daily
        config:
          export_as: table
    config:
      meta:
        hopsworks:
          exports:
            revenue_by_country_daily:
              schedule: "0 0 2 * * ?"
              lookback: 7 days
```

The feature group is keyed by `customer__country`, with `metric_time__day` as its event time.
[Metric exports][semantic-exports] covers the settings, the refreshes, who the job runs as, and the statuses.

## From an agent { #semantic-saved-queries-agent }

The Hopsworks MCP server has two READ tools for saved queries, among its [semantic layer tools][semantic-agent-tools-list]:

| Tool | Arguments | Returns |
| --- | --- | --- |
| `list_saved_queries` | `semantic_project` | CSV with the columns name, label, description, metrics and group_by, the last two space-separated. |
| `query_saved_query` | `semantic_project`, `name`, then `group_by`, `where` and `limit` (optional) | CSV of the rows. `group_by` replaces the saved group-bys, `where` adds to the saved filters, and `limit`, 100 by default, replaces the saved limit. |

```json
{"semantic_project": "sales", "name": "revenue_by_country", "group_by": ["customer__country"]}
```

```text
customer__country,revenue,orders
SE,170.25,3
DE,75.5,2
US,55.75,1
```

## Dashboards from a saved query { #semantic-saved-queries-dashboards }

A Superset dashboard can chart a saved query instead of a list of metrics, see [Dashboards in Superset][semantic-superset-dashboards] for the prerequisites:

=== "CLI"

    ```bash
    hops semantic dashboard sales --saved-query revenue_by_country
    ```

    ```text
    Created dashboard 14 "sales: Revenue by country": https://<hopsworks host>/hopsworks-api/superset/dashboard/14/?projectId=119
    ```

=== "Python"

    ```python
    import hopsworks


    project = hopsworks.login()
    sales = project.get_semantic_layer_api().get_project("sales")
    dashboard = sales.create_dashboard(saved_query="revenue_by_country")
    print(dashboard["url"])
    ```

The dashboard has the layout of a dashboard of metrics, over the saved query's metrics, and is built on the saved query's view, so every chart runs as the saved query, with its filters.
The breakdown table and the filters use the saved query's categorical dimensions and entities, `customer__country` here.
The title is `<semantic project>: <saved query label>` unless `--title` or `title=` gives one.

In the UI, **Create dashboard** in the saved query's sheet opens the **Create a Superset dashboard** dialog on the saved query.
Over REST, the dashboard request takes `{"savedQuery": "<name>", "title": "<title>"}` in place of `metrics` and `groupBy`.

| Error | Status | Meaning |
| --- | --- | --- |
| `SEMANTIC_LAYER_NOT_FOUND` | 404 | No saved query of that name in the build that answers queries. |
| `SEMANTIC_LAYER_ILLEGAL_ARGUMENT` | 400 | Metrics or group-bys given with the saved query, or a saved query with no metrics or more than eight. |

The other errors are those of [a dashboard of metrics][semantic-superset-errors].

## The Superset view of a saved query { #semantic-saved-queries-superset-view }

Each saved query of a semantic project is a semantic view in Superset, named `<semantic project>.<saved query>`, such as `sales.revenue_by_country`, next to the semantic project's own view.
A chart on it can pick:

- the saved query's metrics, and no others;
- its group-bys, a time group-by at every grain its metrics share;
- `metric_time` at every grain its metrics share, even when the saved query does not group by it, for the time range filter and a temporal x-axis.

Every query of a chart on the view runs as the saved query, by the rules of [Refine a saved query][semantic-saved-queries-refine]: with the chart's group-bys, its filters added to the saved ones, its order, and its row limit, or the saved limit when the chart has none.
A filter on the view lists the values the saved query has rows for, under its own filters.
Hopsworks adds and removes the views with the saved queries of the build that answers queries, as it keeps the semantic project's views, see [Who can see what][semantic-superset-access].

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-class"></code> [`SemanticProject`][hopsworks_common.semantic_layer.SemanticProject]
        - <code class="doc-symbol doc-symbol-method"></code> [`list_saved_queries`][hopsworks_common.semantic_layer.SemanticProject.list_saved_queries]
        - <code class="doc-symbol doc-symbol-method"></code> [`query`][hopsworks_common.semantic_layer.SemanticProject.query]
        - <code class="doc-symbol doc-symbol-method"></code> [`sql`][hopsworks_common.semantic_layer.SemanticProject.sql]
        - <code class="doc-symbol doc-symbol-method"></code> [`create_dashboard`][hopsworks_common.semantic_layer.SemanticProject.create_dashboard]
    - <code class="doc-symbol doc-symbol-class"></code> [`SemanticSavedQuery`][hopsworks_common.semantic_layer.SemanticSavedQuery]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>
