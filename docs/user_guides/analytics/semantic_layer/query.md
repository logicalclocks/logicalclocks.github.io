---
description: How to find metrics and query them by dimension and time grain from Python, the hops CLI, the UI query workbench and the REST API, and the limits that apply.
---

# Query Metrics { #semantic-query-metrics }

A metric query names metrics, the group-bys to split them by, and optional filters, ordering and a row limit.
The semantic layer generates the SQL from the current build and runs it on Trino as the caller, or answers a repeated query from its [result cache][semantic-result-cache].
The examples query the `sales` semantic project from [Compile and builds][semantic-compile-builds].
dbt Semantic Layer clients, such as dbt-sl-sdk and the Arrow Flight SQL JDBC driver, query the same metrics, see [Connect dbt clients][semantic-connect-clients], and so do BI tools, through tables, see [Connect BI tools][semantic-bi-tools].
A query can also run on your own Spark session, see [Query metrics on Spark][semantic-spark].

## Group-by names { #semantic-query-names }

| Group-by | Example |
| --- | --- |
| A dimension, `<entity>__<dimension>` | `customer__country`, `order__status` |
| A time dimension with a grain | `order__order_ts__week` |
| The metric time with a grain | `metric_time__day`, `metric_time__month` |
| A date part | `metric_time__extract_dow` |
| A custom granularity of the [time spine][semantic-time-spine-custom] | `metric_time__fiscal_quarter` |

A time group-by takes the `time_granularity` of its time dimension or any coarser grain, up to `year`.
The date parts are `year`, `quarter`, `month`, `day`, `dow` and `doy`.
A group-by is its column name in the result.
A cumulative metric with a window and a metric read at an offset need `metric_time` in every query, see [Metric types][semantic-metric-types-requirements].

## Find metrics and dimensions { #semantic-query-discover }

=== "CLI"

    ```bash
    hops semantic metrics sales
    hops semantic metrics sales --group-by customer__country
    hops semantic dimensions sales --metrics revenue,revenue_per_order
    hops semantic entities sales
    hops semantic dimension-values sales customer__country --limit 20
    hops search --type metric revenue
    ```

=== "Python"

    ```python
    import hopsworks


    project = hopsworks.login()
    sales = project.get_semantic_layer_api().get_project("sales")
    print([m.name for m in sales.list_metrics()])
    print([g.name for g in sales.group_bys(metrics=["revenue"])])
    print(sales.compatible_metrics(["customer__country"]))
    print(sales.dimension_values("customer__country", limit=100))
    ```

`dimensions` and `group_bys` list only what every listed metric can be grouped by, and `metrics --group-by` lists only the metrics that can be grouped by every listed group-by.
`hops search --type metric` finds metrics by name, label and description, each with its semantic project, as does the search box in the UI header.

## Query from the CLI { #semantic-query-cli }

```bash
hops semantic query sales --metrics revenue,orders --group-by customer__country --order-by -revenue
```

```text
customer__country  revenue  orders
-----------------  -------  ------
SE                 190.75   4
US                 125.75   2
DE                 75.5     2
```

```bash
hops semantic query sales --metrics revenue_per_order,completed_revenue_per_order \
  --group-by customer__country --order-by customer__country -o csv
```

```text
customer__country,revenue_per_order,completed_revenue_per_order
DE,37.75,7.75
SE,47.6875,35.0625
US,62.875,27.875
```

| Option | Meaning |
| --- | --- |
| `--metrics` | Metric names, comma-separated or repeated. |
| `--saved-query` | A [saved query][semantic-saved-queries] to run in place of `--metrics`. |
| `--group-by` | Group-bys, comma-separated or repeated. |
| `--where` | A filter in the call syntax, repeated for `AND`: `--where "{{ Dimension('customer__country') }} = 'SE'"`. |
| `--order-by` | Metric or group-by names; a leading `-` sorts descending. |
| `--limit` | The most rows to return. |
| `--start-time`, `--end-time` | Bounds on `metric_time`, both inclusive, each truncated to the query's time grain. |
| `-o` | `table` (default), `json` or `csv`. |
| `--explain` | Print the SQL instead of running it. |
| `--no-cache` | Run the query on Trino even when the [result cache][semantic-result-cache] holds it. |

`hops semantic sql` takes the same options except `-o` and `--explain`, and prints the SQL without running it.
A monthly query with `--end-time 2026-02-01` includes all of February, since the bound is truncated to the month.
NULLs sort last.

## Query from Python { #semantic-query-python }

```python
import hopsworks


project = hopsworks.login()
sales = project.get_semantic_layer_api().get_project("sales")

df = sales.query(
    metrics=["revenue", "revenue_per_order"],
    group_by=["metric_time__month", "customer__country"],
    filters=[("order__status", "IN", ["completed", "shipped"])],
    having=[("revenue", ">", 100)],
    order_by=["-revenue"],
    time_range=("2026-01-01", "2026-03-31"),
    group_limit={"group_by": ["customer__country"], "top": 2, "metric": "revenue"},
    dataframe_type="pandas",
)
sql = sales.sql(metrics=["revenue"], group_by=["metric_time__month"])
```

| Argument | Meaning |
| --- | --- |
| `where` | Text filters in the call syntax, combined with `AND`. |
| `filters` | Structured filters, `(group_by, op, value)`, with `op` one of `=`, `!=`, `<`, `<=`, `>`, `>=`, `IN`, `NOT IN`, `IS NULL`, `IS NOT NULL` and `LIKE`. The values are bound as literals and never parsed as SQL. |
| `having` | Filters on metric values, `(metric, op, value)`. |
| `order_by` | Metric or group-by names; a leading `-` sorts descending. |
| `limit`, `offset` | The most rows to return, and the rows to skip. |
| `time_range` | `(start, end)` bounds on `metric_time`, both inclusive, each truncated to the query's time grain; either may be `None`. |
| `group_limit` | Keep the top groups by a metric, such as the two countries with the most revenue. |
| `dataframe_type` | `pandas` (default), `polars`, `pyarrow`, or `python` for a list of dicts. |
| `saved_query` | A [saved query][semantic-saved-queries] to run in place of `metrics`. |
| `read_cache` | `False` runs the query on Trino even when the [result cache][semantic-result-cache] holds it; `True` by default. |
| `engine` | `trino` (default), or `spark` to run the query on your Spark session and get a PySpark DataFrame, see [Query metrics on Spark][semantic-spark]. |
| `spark` | The Spark session for `engine="spark"`; the active one by default. |

A group-by can also be a dict, `{"name": "metric_time", "grain": "month"}` or `{"name": "metric_time", "date_part": "dow"}`.
Results come back as an Arrow stream when `pyarrow` is installed, which keeps the column types, and as JSON otherwise.
The client works from outside the cluster with an API key, through the same host as `hopsworks.login()`.

### Query without metrics { #semantic-query-no-metrics }

A query without metrics returns the distinct values of its group-bys under its filters:

```python
import hopsworks


project = hopsworks.login()
sales = project.get_semantic_layer_api().get_project("sales")
print(
    sales.query(
        group_by=["customer__country", "order__status"],
        order_by=["customer__country", "order__status"],
    )
)
```

```text
  customer__country order__status
0                DE     completed
1                DE       shipped
2                SE     cancelled
3                SE     completed
4                SE       shipped
5                US     cancelled
6                US     completed
```

The rows come from the semantic model that reaches every group-by and filter with the fewest joins, and `metric_time` from the time spine.
Over REST, the query body takes `"minMaxOnly": true` for the smallest and largest value of its one group-by, and `"applyGroupBy": false` for every row instead of the distinct ones.
The CLI's `hops semantic query` needs `--metrics` or `--saved-query`; `hops semantic dimension-values` lists the values of one group-by.

## Query in the UI { #semantic-query-ui }

Open **Semantic Layer** in the project sidebar, pick a semantic project, and click **Query metrics**.
The **Metrics** card of the overview lists the metrics of the current build; clicking a metric shows its definition, its type, and what it can be grouped by.
The **Saved queries** card lists the [saved queries][semantic-saved-queries], each with **Run**, which opens the query workbench on it.

The query workbench takes:

- **Metrics**, one or more;
- **Group by**, offered only from what every picked metric can be grouped by, with a **Grain** for each time group-by; picking a metric that needs `metric_time` puts it first, at the metric's grain;
- **Filters**, a group-by, an operator and a value each; numbers and `true` or `false` are sent as such, a quoted value is sent as text, and `IN` values are separated with commas;
- **Order by**, a metric or group-by and a direction;
- **Limit**, from 1 to 1,000 rows, 100 by default.

**Run** shows the rows under **Results**, and **Show SQL** shows the generated SQL under **SQL** without running it.
The rows are read on Trino as you.

## Query over REST { #semantic-query-rest }

Other clients query the gateway at `https://<hopsworks host>/semantic-layer/v1/projects/<semantic project id>/`, with an API key:

```bash
curl -H "Authorization: ApiKey $HOPSWORKS_API_KEY" \
  "https://<hopsworks host>/semantic-layer/v1/projects/7/metrics"

curl -X POST -H "Authorization: ApiKey $HOPSWORKS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"metrics": ["revenue"], "groupBy": ["customer__country"], "orderBy": [{"name": "revenue", "descending": true}]}' \
  "https://<hopsworks host>/semantic-layer/v1/projects/7/query"
```

| Method | Path | Returns |
| --- | --- | --- |
| GET | `metrics` | The metrics of the current build. |
| GET | `dimensions?metrics=a,b` | The dimensions every listed metric can be grouped by. |
| GET | `entities?metrics=a,b` | The entities every listed metric can be grouped by. |
| GET | `group-bys?metrics=a,b` | Dimensions, entities and `metric_time`. |
| POST | `compatible-metrics` | The metrics that can be grouped by every group-by in `{"groupBy": [...]}`. |
| POST | `sql` | The SQL of a query, without running it. |
| POST | `query` | The rows of a query: JSON by default, or an Arrow IPC stream with `Accept: application/vnd.apache.arrow.stream`. |
| POST | `dimension-values` | The distinct values of `{"groupBy": ..., "limit": 1000}`. |
| GET | `saved-queries` | The [saved queries][semantic-saved-queries-list] of the current build. |

The query body takes `metrics`, `savedQuery`, `groupBy`, `where`, `filters`, `having`, `timeRange`, `orderBy`, `limit`, `offset` and `groupLimit`, in the camel case of the Python arguments, and `minMaxOnly` and `applyGroupBy` for a [query without metrics][semantic-query-no-metrics].
`"cache": false` in a `query` or `dimension-values` body skips the [result cache][semantic-result-cache].
`"useExports": false` in a `query` body computes the rows from the sources even when an [export][semantic-exports-serving] holds them.
`"engine": "SPARK"` in a `sql` body answers Spark SQL and the views it reads, see [Over REST][semantic-spark-rest]; `query` runs on Trino only.
A JSON result carries `columns`, `rows`, `rowCount`, `truncated` and `sql`.
Every response carries the `buildId` that answered and whether it is `stale`; an Arrow result carries them in the `X-Semantic-Build` and `X-Semantic-Stale` headers.

| Header | On | Value |
| --- | --- | --- |
| `X-Semantic-Max-Rows` | Arrow `query` | The row cap of an Arrow result. |
| `X-Semantic-Truncated` | `query` | `true` when the row cap cut the result. An Arrow result carries it only when the cut is known before the first rows are sent, so treat one with `X-Semantic-Max-Rows` rows as cut. |
| `X-Semantic-Feature-Groups` | `query`, `sql` | The ids of the feature groups the query reads through its semantic models, comma-separated. |
| `X-Semantic-Sql-Base64` | Arrow `query` | The SQL that ran, base64 encoded. |
| `X-Semantic-Cache` | JSON `query` | `hit`, `miss` or `bypass`, see [Result cache][semantic-result-cache-never]. |
| `X-Semantic-Served-From`, `X-Semantic-Export-Feature-Group` | `query` | The export, and its feature group, an answer was read from, see [Answer queries from an export][semantic-exports-serving]. |
| `X-Semantic-Source-Versions` | `query` | The Delta version of each source feature group the rows were computed from, on an answer read from an export. |
| `X-Semantic-Definition` | `query` | The definition fingerprint of the saved query the request names. |

## Limits { #semantic-query-limits }

| Limit | Default | When it is reached |
| --- | --- | --- |
| Rows of an Arrow result | 1,000,000 | The result stops there; the Python client logs a warning when a result fills the cap. |
| Rows of a JSON result | 100,000 | The result stops there and sets `truncated`. |
| Query time | 300 seconds | 504 `SEMANTIC_LAYER_TIMEOUT`. |
| Queries running at once, per gateway replica | 16 | A query waits up to 30 seconds for a slot, then gets 503 `SEMANTIC_LAYER_BUSY`. |
| Request body | 1 MiB | The request is refused. |
| Rows in the UI workbench | 1,000 | The limit field accepts no more. |

The `semantic-gateway` Helm values `maxRows`, `maxJsonRows`, `queryTimeoutSeconds` and `queryConcurrency` change the first four limits.
Add a `limit`, a filter or fewer group-bys to stay under the row caps.
The limits of GraphQL and Arrow Flight SQL are in [Connect dbt clients][semantic-connect-limits].

## Errors { #semantic-query-errors }

| Error | Status | Meaning | Fix |
| --- | --- | --- | --- |
| `SEMANTIC_LAYER_NO_VALID_BUILD` | 409 | No build has compiled valid yet. | `hops semantic compile <name> --wait`, and fix the issues. |
| `SEMANTIC_LAYER_INVALID_QUERY` | 400 | An unknown metric, group-by or filter, a group-by the metrics cannot reach, a metric that needs `metric_time` without it, or a shape under [Limits][semantic-metric-types-limits]. | `hops semantic dimensions <name> --metrics ...` lists what they can reach. |
| `SEMANTIC_LAYER_EXECUTION_FAILED` | 502 | Trino refused or failed the generated SQL; its message follows. | `hops semantic sql` shows the SQL. |
| `SEMANTIC_LAYER_FORBIDDEN` | 403 | Not a member of the project, or an API key without the `FEATURESTORE` and `TRINO` scopes. | Add the member or the scopes. |
| `SEMANTIC_LAYER_NOT_FOUND` | 404 | No semantic project with that id, or no saved query of that name. | `hops semantic list`, `hops semantic saved-queries <name>`. |

In Python, each is a `SemanticLayerException` with the code in `error_code`.

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-class"></code> [`SemanticProject`][hopsworks_common.semantic_layer.SemanticProject]
        - <code class="doc-symbol doc-symbol-method"></code> [`query`][hopsworks_common.semantic_layer.SemanticProject.query]
        - <code class="doc-symbol doc-symbol-method"></code> [`sql`][hopsworks_common.semantic_layer.SemanticProject.sql]
        - <code class="doc-symbol doc-symbol-method"></code> [`list_metrics`][hopsworks_common.semantic_layer.SemanticProject.list_metrics]
        - <code class="doc-symbol doc-symbol-method"></code> [`list_saved_queries`][hopsworks_common.semantic_layer.SemanticProject.list_saved_queries]
        - <code class="doc-symbol doc-symbol-method"></code> [`dimensions`][hopsworks_common.semantic_layer.SemanticProject.dimensions]
        - <code class="doc-symbol doc-symbol-method"></code> [`entities`][hopsworks_common.semantic_layer.SemanticProject.entities]
        - <code class="doc-symbol doc-symbol-method"></code> [`group_bys`][hopsworks_common.semantic_layer.SemanticProject.group_bys]
        - <code class="doc-symbol doc-symbol-method"></code> [`compatible_metrics`][hopsworks_common.semantic_layer.SemanticProject.compatible_metrics]
        - <code class="doc-symbol doc-symbol-method"></code> [`dimension_values`][hopsworks_common.semantic_layer.SemanticProject.dimension_values]
        - <code class="doc-symbol doc-symbol-method"></code> [`serving`][hopsworks_common.semantic_layer.SemanticProject.serving]
    - <code class="doc-symbol doc-symbol-class"></code> [`SemanticMetric`][hopsworks_common.semantic_layer.SemanticMetric]
    - <code class="doc-symbol doc-symbol-class"></code> [`SemanticGroupBy`][hopsworks_common.semantic_layer.SemanticGroupBy]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>
