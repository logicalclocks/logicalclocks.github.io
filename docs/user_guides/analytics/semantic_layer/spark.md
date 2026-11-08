---
description: How to run a metric query on your own Spark session with engine="spark", get a PySpark DataFrame, drop its views, and which feature groups, sessions and metric shapes Spark supports.
---

# Query Metrics on Spark { #semantic-spark }

A metric query can run on the caller's Spark session instead of Trino, and return a PySpark DataFrame that a Spark job or notebook transforms further.
The semantic gateway plans the query as for Trino, renders it as Spark SQL, and names the feature groups it reads; the Python client registers each of them as a temporary view and runs the SQL.
The examples use the `sales` semantic project of [Define metrics][semantic-define-metrics].

## Run a query { #semantic-spark-run }

In a Spark job or a Jupyter notebook on Spark, with the hsfs engine connected:

```python
import hopsworks


project = hopsworks.login()
sales = project.get_semantic_layer_api().get_project("sales")
df = sales.query(
    metrics=["revenue", "orders"],
    group_by=["metric_time__month"],
    engine="spark",
)
df.orderBy("metric_time__month").show()
sales.drop_views(df)
```

```text
+-------------------+-------+------+
| metric_time__month|revenue|orders|
+-------------------+-------+------+
|2026-01-01 00:00:00| 220.75|     4|
|2026-02-01 00:00:00| 115.50|     3|
|2026-03-01 00:00:00|  55.75|     1|
+-------------------+-------+------+
```

- `query(..., engine="spark")` takes the arguments of every [query][semantic-query-python], and returns a lazy `pyspark.sql.DataFrame`; `dataframe_type` and `read_cache` do not apply.
- `spark=` names the session; by default it is the active session.
- Each feature group the query reads, time spines included, is a temporary view of this call, `sl_<8 hex digits>_<feature group id>`, such as `sl_1a2b3c4d_11`.
- The views live as long as the session; `drop_views(df)` drops the views of the call that returned `df`, after which `df`, and every DataFrame derived from it, cannot be read.
- Each view reads its feature group whole, at its latest commit: the scheduler's `HOPS_START_TIME` and `HOPS_END_TIME` do not filter it, as they filter `fg.read()` in a scheduled job.
- The [result cache][semantic-result-cache] and [answers from exports][semantic-exports-serving] are Trino's, and the [query history][semantic-query-history] records Trino queries only.

## What Spark supports { #semantic-spark-support }

| | Supported | Refused |
| --- | --- | --- |
| Session | The session the hsfs engine holds, with `spark.sql.session.timeZone` set to `UTC` before hsfs starts its engine. | Another session; another time zone. The client checks the time zone before hsfs starts its engine, which would set it, and never changes it. |
| Spark | Classic Spark and Spark Connect. | |
| Feature groups | Delta on classic Spark and Spark Connect; Hudi on classic Spark. | Hudi on Spark Connect; any other format, or a table that is not a feature group. |
| Access | Feature groups of the project, and feature groups shared with it whole. | A feature group shared with only some of its features, no longer shared, or that a Trino row filter, column mask or denied column applies to: Spark reads the files whole. |
| Metrics | Every metric type, at every grain from `microsecond` to `year`, date parts, decimals, NULLs, exact percentiles, cumulative metrics, offsets, `join_to_timespine` and `fill_nulls_with`, SCD Type II dimensions and semi-additive measures. | Approximate percentiles; conversion metrics grouped by another time than their agg time; filters that call `DAY_OF_WEEK`, `JSON_EXTRACT_SCALAR` or `DATE_FORMAT`, which are Trino functions. |

The MetricFlow integration cases and a case for each type and grain above were run on Spark 4.1.1 in ANSI mode with a UTC session, and their rows compared with the expected ones; the gateway refuses a shape outside them when it plans the query.

| Refusal | Raised by | Message |
| --- | --- | --- |
| Not a Spark engine | The client, `FeatureStoreException` | `engine='spark' runs the query on Spark: connect to Hopsworks with a Spark engine, from a Spark job or notebook.` |
| Time zone | The client, `FeatureStoreException` | `spark.sql.session.timeZone is 'Europe/Stockholm'; semantic queries on Spark need UTC, which this session must already use.` |
| Session | The client, `FeatureStoreException` | `The Spark session is not the one the hsfs engine holds, which registers the views; pass that session, or none.` |
| Format | The client, `FeatureStoreException` | `Feature group <name> version <v> is HUDI on Spark Connect; semantic queries on Spark read Delta feature groups, and Hudi ones on classic Spark.` |
| Access | The gateway, `SemanticLayerException` 400 `SEMANTIC_LAYER_INVALID_QUERY` | `feature group <store>.<table> (id <id>) cannot be read on Spark: ...; run the query on Trino` |
| Metric shape | The gateway, `SemanticLayerException` 400 `SEMANTIC_LAYER_INVALID_QUERY` | Names the case, such as `approximate percentiles are not supported on Spark (measure <measure>); an exact percentile is`. |

Set `spark.sql.session.timeZone` to `UTC` in the Spark configuration of the job or notebook, so the session starts with it.

## Over REST { #semantic-spark-rest }

The gateway's `sql` endpoint takes `"engine": "SPARK"` and answers the Spark SQL and the views it reads; the `query` endpoint runs on Trino only, and refuses `SPARK`:

```bash
curl -X POST -H "Authorization: ApiKey $HOPSWORKS_API_KEY" -H "Content-Type: application/json" \
  -d '{"metrics": ["revenue"], "groupBy": ["customer__country"], "engine": "SPARK"}' \
  "https://hopsworks.example.com/semantic-layer/v1/projects/7/sql"
```

```json
{
  "sql": "SELECT `sl_1a2b3c4d_12`.`country` AS `customer__country`, SUM(`sl_1a2b3c4d_11`.`amount`) AS `revenue` FROM ...",
  "views": [
    {"alias": "sl_1a2b3c4d_11", "featureGroupId": 11, "name": "orders", "version": 1, "featureStore": "demo_featurestore"},
    {"alias": "sl_1a2b3c4d_12", "featureGroupId": 12, "name": "customers", "version": 1, "featureStore": "demo_featurestore"}
  ],
  "buildId": 34,
  "stale": false
}
```

A client that registers each view over its feature group's data, read whole, can run the SQL on its own Spark session.

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-class"></code> [`SemanticProject`][hopsworks_common.semantic_layer.SemanticProject]
        - <code class="doc-symbol doc-symbol-method"></code> [`query`][hopsworks_common.semantic_layer.SemanticProject.query]
        - <code class="doc-symbol doc-symbol-method"></code> [`drop_views`][hopsworks_common.semantic_layer.SemanticProject.drop_views]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>
