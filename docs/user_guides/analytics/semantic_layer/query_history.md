---
description: The query history of a semantic project, what each record holds, who reads which records, how to read them from the CLI, Python, the UI, REST and GraphQL, and how long they are kept.
---

# Query History { #semantic-query-history }

The semantic gateway records each metric query it runs, over every API, and Hopsworks keeps the records with the semantic project.
The history is best effort: it is for seeing what ran, how long it took and why it failed, and is not an audit log.
The examples use the `sales` semantic project of [Define metrics][semantic-define-metrics], with id 7, in the project with id 119.

## What is recorded { #semantic-query-history-recorded }

One record per execution attempt of a query that runs, or would run, on Trino:

| Surface | Recorded |
| --- | --- |
| `REST` | `query` and `dimension-values`: the Python client, the `hops` CLI, the query workbench in the UI, the agent tools, Superset charts and [export][semantic-exports] runs. |
| `GRAPHQL` | `createQuery` and `createDimensionValuesQuery`. |
| `FLIGHT` | Statements in [dbt's JDBC dialect][semantic-connect-dialect] that run a query: dbt-sl-sdk queries, ADBC and JDBC. |
| `BI` | SQL over the [BI tables][semantic-bi-tools]. |

- Queries that fail to plan, fail on Trino, or are cancelled are recorded too, with their error.
- Listings of metrics, dimensions and saved queries, requests for the SQL of a query, schema probes such as `WHERE 1=0`, and GraphQL polls are not recorded.
- A query answered from the [result cache][semantic-result-cache] is recorded, with the cache outcome `hit`.
- A record holds no credential and no header.

| Field | Value |
| --- | --- |
| `executionId` | The gateway's id of the execution, a UUID. |
| `user` | The user name of the caller. |
| `surface` | `REST`, `GRAPHQL`, `FLIGHT` or `BI`. |
| `engine` | `TRINO`. |
| `buildId` | The build that planned the query. |
| `status` | `SUCCEEDED`, `FAILED` or `CANCELLED`. |
| `error` | The error of a failed or cancelled query. |
| `rows` | The rows returned. |
| `startedAt`, `finishedAt`, `durationMs` | When the query started and ended, in UTC, and how long it took. |
| `cache` | `hit`, `miss` or `bypass`, as the `X-Semantic-Cache` header of [Result cache][semantic-result-cache-never]. |
| `servedFrom` | `export:<export>` for an answer read from an [export][semantic-exports-serving]; null otherwise. |
| `trinoQueryId` | The id of the query on Trino. |
| `request` | The metric query as the gateway normalised it, as JSON. |
| `sql` | The SQL that ran. |

The gateway sends its records to Hopsworks in batches, every 5 seconds or every 200 records, under the credential of the caller whose queries they are, and Hopsworks takes the user from that credential.
A record can be lost: when the gateway's queue is full, when a batch keeps failing after retries, when the caller's credential expires before the batch is sent, or when a gateway replica stops abruptly.
The gateway's metrics port counts sent records in `semantic_query_records_sent_total`, and lost ones in `semantic_query_records_dropped_total` by reason: `full`, `oversized`, `credential`, `failed` and `rejected`.

## Who reads which records { #semantic-query-history-access }

| Role in the project | Reads |
| --- | --- |
| Data Owner | Every member's records, and one member's with the `user` filter. |
| Data Scientist | Their own records; the `user` filter is ignored. |

GraphQL's `queryRecords` returns the caller's own records, whatever the role.

## Read the history { #semantic-query-history-read }

=== "CLI"

    ```bash
    hops semantic history sales --limit 3
    ```

    ```text
    STARTED                           USER      SURFACE  STATUS     MS   ROWS  CACHE   QUERY                                ERROR
    --------------------------------  --------  -------  ---------  ---  ----  ------  -----------------------------------  -----------------------------
    2026-11-08T10:02:11.404000+00:00  meb10000  BI       SUCCEEDED  412  3     miss    revenue by customer__country         -
    2026-11-08T10:01:57.120000+00:00  meb10000  REST     SUCCEEDED  9    3     hit     revenue,orders by customer__country  -
    2026-11-08T10:01:30.018000+00:00  meb10000  FLIGHT   FAILED     35   -     bypass  revenue by order__state              unknown group-by order__state
    ```

=== "Python"

    ```python
    import hopsworks


    project = hopsworks.login()
    sales = project.get_semantic_layer_api().get_project("sales")
    df = sales.query_history(limit=100, status="FAILED")
    print(df[["started_at", "user", "surface", "duration_ms", "error"]])
    ```

| CLI option | Python argument | Meaning |
| --- | --- | --- |
| `--limit` | `limit` | The most records, newest first: 50 in the CLI, 100 in Python. |
| `--status` | `status` | `SUCCEEDED`, `FAILED` or `CANCELLED`; repeat the option, or pass a list, for several. |
| `--user` | `user` | A member's user name; Data Owners only. |

`hops semantic history sales --json` prints every field.
`query_history` returns a pandas DataFrame with one row per record, the fields in snake case, `started_at` and `finished_at` as UTC timestamps.

In the UI, the **Query history** card of the semantic project's overview lists the records, newest first, with **Started**, **User** for Data Owners, **Query**, **Surface**, **Status**, **Duration**, **Rows** and **Cache**.
**Succeeded**, **Failed** and **Cancelled** filter it, and **Newer** and **Older** page through it.

### Over REST { #semantic-query-history-rest }

```bash
curl -H "Authorization: ApiKey $HOPSWORKS_API_KEY" \
  "https://hopsworks.example.com/hopsworks-api/api/project/119/semantic/projects/7/queries?limit=1&status=FAILED,CANCELLED"
```

```json
{
  "items": [
    {
      "executionId": "3f8c2a52-6a1e-4c2f-9d7b-0c5e2b1d9a41",
      "user": "meb10000",
      "surface": "FLIGHT",
      "engine": "TRINO",
      "buildId": 34,
      "status": "FAILED",
      "error": "unknown group-by order__state",
      "rows": null,
      "startedAt": "2026-11-08T10:01:30.018Z",
      "finishedAt": "2026-11-08T10:01:30.053Z",
      "durationMs": 35,
      "cache": "bypass",
      "servedFrom": null,
      "trinoQueryId": null,
      "request": {"metrics": ["revenue"], "groupBy": [{"name": "order__state"}]},
      "sql": null
    }
  ],
  "nextCursor": "MTc5NDEyNjQ5MDAxODoxMjM0"
}
```

| Parameter | Meaning |
| --- | --- |
| `limit` | 1 to 1000 records, 50 by default. |
| `cursor` | The `nextCursor` of the previous page; `nextCursor` is null on the last page. |
| `status` | `SUCCEEDED`, `FAILED` or `CANCELLED`, comma-separated. |
| `surface` | `REST`, `GRAPHQL`, `FLIGHT` or `BI`. |
| `user` | A member's user name; Data Owners only. |
| `from`, `to` | ISO-8601 instants on the start time; `from` is inclusive. |

Records come newest first.
Data Owners and Data Scientists read the endpoint; an API key needs the `FEATURESTORE` scope.
An invalid filter or cursor answers 400 `SEMANTIC_LAYER_ILLEGAL_ARGUMENT`.

### Over GraphQL { #semantic-query-history-graphql }

`queryRecords` follows the shape of dbt's Semantic Layer API, and returns the caller's own records:

```graphql
query {
  queryRecords(environmentId: 7, pageNum: 1, pageSize: 20, statuses: [FAILED]) {
    totalItems
    items {
      queryId
      status
      startTime
      endTime
      error
      connectionDetails
      queryDetails {
        ... on SemanticLayerQueryDetails {
          params { type metrics { name } groupBy { name grain } savedQuery }
        }
      }
    }
  }
}
```

- `queryId` is the execution id; `startTime` and `endTime` filter on the start time as ISO-8601 instants.
- `status` is `SUCCESSFUL` for `SUCCEEDED`, and `FAILED` for `FAILED` and `CANCELLED`, a cancelled query's `error` being `cancelled`.
- `connectionDetails` is JSON with the surface, engine, build, cache outcome, rows, the export served from, and the Trino query id.
- `params.type` is `METRICS` for a metric query and `DIMENSION_VALUES` for the values of a group-by.
- `queryDetails` is null once the record's details are removed, see [Retention][semantic-query-history-retention].

## Retention { #semantic-query-history-retention }

An hourly job on Hopsworks applies two cluster settings, see [Cluster Configuration][cluster-configuration]:

| Variable | Default | Effect |
| --- | --- | --- |
| `semantic_query_delete_after_days` | `30` | Records that started earlier are deleted. |
| `semantic_query_strip_details_after_days` | `7` | Records that started earlier lose `request`, `sql` and `error`; who ran the query, its status, rows and duration stay until the record is deleted. |
| `semantic_query_cleaner_batch_size` | `1000` | Records the job deletes or strips per statement. |

Deleting a semantic project, its project, or a user deletes their records.
Hopsworks keeps the records in RonDB's disk tablespace, see [Query history storage][semantic-admin-history-storage].

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-class"></code> [`SemanticProject`][hopsworks_common.semantic_layer.SemanticProject]
        - <code class="doc-symbol doc-symbol-method"></code> [`query_history`][hopsworks_common.semantic_layer.SemanticProject.query_history]
    - <code class="doc-symbol doc-symbol-docs"></code> [dbt Semantic Layer GraphQL API](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-graphql)

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>
