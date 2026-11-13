---
description: How to connect dbt Semantic Layer clients to a Hopsworks semantic project, dbt-sl-sdk, the Arrow Flight SQL JDBC driver and ADBC for queries, GraphQL for metadata, and the limits of each.
---

# Connect dbt Semantic Layer Clients { #semantic-connect-clients }

The semantic gateway serves the two APIs of dbt's Semantic Layer: Arrow Flight SQL with dbt's JDBC dialect, which runs queries, and GraphQL, which answers metadata and the SQL of a query.
A client written for dbt's Semantic Layer connects with a host, an API key, and an environment id, which in Hopsworks is the id of a semantic project.
Every query runs on Trino as the API key's user, as a query from Python or the CLI does, see [How a query runs][semantic-overview-query-path].
BI tools and SQL clients that browse tables read the same port as tables, see [Connect BI tools][semantic-bi-tools].

The examples use the `sales` semantic project of [Define metrics][semantic-define-metrics], with id 7, in the project with id 119.
The Hopsworks host is `hopsworks.example.com`, and the load balancer of the Flight SQL port is `semantic.hopsworks.example.com`.

## Endpoints { #semantic-connect-endpoints }

| API | Address | Used by |
| --- | --- | --- |
| GraphQL | `https://<hopsworks host>/semantic-layer/api/graphql` | dbt-sl-sdk for metadata and `compile_sql`, GraphQL clients |
| Arrow Flight SQL | `grpc+tls://<flight host>:18446` | dbt-sl-sdk for queries, ADBC, the Arrow Flight SQL JDBC driver, [BI tools][semantic-bi-tools] |
| Both, dbt's layout | `https://<layout host>/api/graphql` and `grpc+tls://<layout host>:443` | dbt's Tableau and Power BI connectors, and tools that take a dbt host, when an administrator turns on the [dbt-compatible endpoint layout][semantic-bi-dbt-layout] |

- The environment id is the semantic project's id, which `hops semantic list` prints under `ID`.
- The Flight SQL host is the load balancer of the semantic gateway, see [For administrators][semantic-connect-admin].
  Inside the cluster, it is `semantic-gateway.service.consul` or `semantic-gateway.<namespace>.svc`, on the same port.
- Both APIs take an API key with the `FEATURESTORE` and `TRINO` scopes, as `Authorization: Bearer <api key>`, the form dbt's clients send, or as `Authorization: ApiKey <api key>`.
  The caller must be a member of the semantic project's project.
- Both APIs use TLS.
  The Flight SQL port presents a certificate issued by the cluster's CA, so a client outside the cluster needs that CA unless it already trusts it.

## Connection details { #semantic-connect-details }

Hopsworks hands out what a client needs, apart from the API key.

=== "CLI"

    ```bash
    hops semantic connect sales
    ```

    ```text
    Environment id: 7
    GraphQL (metadata, compileSql): https://hopsworks.example.com/semantic-layer/api/graphql
    ADBC (queries): grpc+tls://semantic.hopsworks.example.com:18446
    JDBC (queries): jdbc:arrow-flight-sql://semantic.hopsworks.example.com:18446?environmentId=7
    CA certificate: /tmp/hopsworks_semantic_119_7_ca.pem
    export DBT_SL_GRAPHQL_URL_FORMAT='https://{server_host}/semantic-layer/api/graphql'
    export DBT_SL_ADBC_URL_FORMAT=grpc+tls://semantic.hopsworks.example.com:18446
    export SSL_CERT_FILE=/tmp/hopsworks_semantic_119_7_ca.pem
    export REQUESTS_CA_BUNDLE=/tmp/hopsworks_semantic_119_7_ca.pem
    ```

=== "Python"

    ```python
    import hopsworks


    project = hopsworks.login()
    sales = project.get_semantic_layer_api().get_project("sales")
    info = sales.connection_info()
    print(info["environment_id"], info["jdbc_url"])
    print(info["env"])
    ```

    ```text
    7 jdbc:arrow-flight-sql://semantic.hopsworks.example.com:18446?environmentId=7
    {'DBT_SL_GRAPHQL_URL_FORMAT': 'https://{server_host}/semantic-layer/api/graphql', 'DBT_SL_ADBC_URL_FORMAT': 'grpc+tls://semantic.hopsworks.example.com:18446', 'SSL_CERT_FILE': '/tmp/hopsworks_semantic_119_7_ca.pem', 'REQUESTS_CA_BUNDLE': '/tmp/hopsworks_semantic_119_7_ca.pem'}
    ```

`hops semantic connect` prints the `export` lines on standard output and the rest on standard error, so `eval "$(hops semantic connect sales)"` sets the variables in the shell.
It writes the cluster's CA to `/tmp/hopsworks_semantic_<project id>_<semantic project id>_ca.pem`, or to `--ca-path`, and `connection_info(ca_path=...)` does the same.
`hops semantic connect sales --json` prints every field.

`DBT_SL_ADBC_URL_FORMAT` is a template with `{server_host}` only when the Flight SQL port is on the Hopsworks host, and that host has no port; otherwise it is the full URL of the load balancer.

In the UI, open the semantic project and click **Connect a client**, next to **Query metrics**.
The dialog shows the **Environment ID**, the **GraphQL URL**, the **ADBC URL**, the **JDBC URL**, the `export` lines for dbt-sl-sdk under **dbt-sl-sdk environment**, and the **Cluster CA** with **Download ca.pem**.

Over REST, `GET /hopsworks-api/api/project/<project id>/semantic/projects/<semantic project id>/connection` answers:

```json
{
  "environmentId": 7,
  "graphqlUrl": "https://hopsworks.example.com/semantic-layer/api/graphql",
  "adbcUrl": "grpc+tls://semantic.hopsworks.example.com:18446",
  "jdbcUrl": "jdbc:arrow-flight-sql://semantic.hopsworks.example.com:18446?environmentId=7",
  "flightHost": "semantic.hopsworks.example.com",
  "flightPort": 18446,
  "env": {
    "DBT_SL_GRAPHQL_URL_FORMAT": "https://{server_host}/semantic-layer/api/graphql",
    "DBT_SL_ADBC_URL_FORMAT": "grpc+tls://semantic.hopsworks.example.com:18446"
  },
  "caPem": "-----BEGIN CERTIFICATE-----\n..."
}
```

Data owners and data scientists of the project read it; an API key needs the `FEATURESTORE` scope.
`caPem` is null when Hopsworks could not read the CA.

## dbt-sl-sdk { #semantic-connect-dbt-sl-sdk }

dbt-sl-sdk reads metadata over GraphQL and runs queries over ADBC, on Arrow Flight SQL.
It reads `DBT_SL_GRAPHQL_URL_FORMAT` and `DBT_SL_ADBC_URL_FORMAT` when it is imported, so set them before the Python process starts:

```bash
pip install "dbt-sl-sdk[sync]==0.13.4"
eval "$(hops semantic connect sales)"
export HOPSWORKS_API_KEY=<api key>
python sales_metrics.py
```

`sales_metrics.py`:

```python
import os

from dbtsl import SemanticLayerClient


client = SemanticLayerClient(
    environment_id=7,
    auth_token=os.environ["HOPSWORKS_API_KEY"],
    host="hopsworks.example.com",
)
with client.session():
    print([m.name for m in client.metrics()])
    table = client.query(
        metrics=["revenue", "orders"],
        group_by=["customer__country"],
        order_by=["-revenue"],
    )
print(table.to_pandas())
```

```text
['revenue', 'orders', 'revenue_per_order', 'completed_revenue_per_order', 'cancelled_orders']
  customer__country  revenue  orders
0                SE   190.75       4
1                US   125.75       2
2                DE    75.50       2
```

- `host` is the Hopsworks host, with its port when it has one.
- dbt-sl-sdk has no option for a CA.
  With a private CA, ADBC reads it from `SSL_CERT_FILE` and the GraphQL client from `REQUESTS_CA_BUNDLE`, which the `eval` sets.
  Each variable replaces the client's default trust store, so the file must also hold the CA of the Hopsworks host's certificate when another CA issued it.
- `client.query(..., read_cache=False)` runs the query on Trino even when the gateway's [result cache][semantic-result-cache] holds it.
- `query`, `query(saved_query=...)` and `dimension_values` run over ADBC; `metrics`, `dimensions`, `entities`, `measures`, `saved_queries` and `compile_sql` are answered over GraphQL.
- dbt-sl-sdk's GraphQL client used on its own, `SyncGraphQLClient`, reads metadata and `compile_sql`; its `create_query` and `query` are refused, see [GraphQL][semantic-connect-graphql].

The GraphQL API follows the metadata operations of dbt-sl-sdk 0.13.4, and the examples use it with `adbc-driver-flightsql` 1.13.0.

## Arrow Flight SQL JDBC driver { #semantic-connect-jdbc }

The Apache Arrow Flight SQL JDBC driver, `org.apache.arrow:flight-sql-jdbc-driver`, connects with dbt's JDBC URL:

```text
jdbc:arrow-flight-sql://semantic.hopsworks.example.com:18446?environmentId=7&token=<api key>
```

With a private CA, add the CA file:

```text
jdbc:arrow-flight-sql://semantic.hopsworks.example.com:18446?environmentId=7&token=<api key>&useEncryption=true&tlsRootCerts=/tmp/hopsworks_semantic_119_7_ca.pem
```

The driver sends `environmentId` as the `environmentid` header and `token` as `Authorization: Bearer <token>`.
The examples use version 19.0.0 of the driver.
Every statement is a `{{ semantic_layer.<call>(...) }}` of [dbt's JDBC dialect][semantic-connect-dialect]:

```sql
select * from {{
  semantic_layer.query(metrics=['revenue', 'orders'],
                       group_by=[Dimension('metric_time').grain('month'), 'customer__country'],
                       where="{{ Dimension('order__status') }} != 'cancelled'",
                       order_by=['-revenue'],
                       limit=10)
}}
```

The driver's `DatabaseMetaData` lists the catalog `semantic_layer`, the semantic project's id as its schema, and the `metrics` table and a table per saved query in it, which a statement without `{{ }}` queries with plain SQL, see [Connect BI tools][semantic-bi-tools].

## ADBC { #semantic-connect-adbc }

`adbc-driver-flightsql` connects to `grpc+tls://<flight host>:18446`, with the API key and the environment id as headers:

```bash
pip install "adbc-driver-flightsql==1.13.0" pyarrow
export SSL_CERT_FILE=/tmp/hopsworks_semantic_119_7_ca.pem
export HOPSWORKS_API_KEY=<api key>
```

```python
import os

import adbc_driver_flightsql.dbapi as flight_sql
from adbc_driver_flightsql import DatabaseOptions


conn = flight_sql.connect(
    "grpc+tls://semantic.hopsworks.example.com:18446",
    db_kwargs={
        DatabaseOptions.AUTHORIZATION_HEADER.value: "Bearer "
        + os.environ["HOPSWORKS_API_KEY"],
        DatabaseOptions.RPC_CALL_HEADER_PREFIX.value + "environmentid": "7",
    },
)
with conn.cursor() as cur:
    cur.execute(
        "select * from {{ semantic_layer.query(metrics=['revenue'], "
        "group_by=['customer__country'], order_by=['-revenue']) }}"
    )
    print(cur.fetch_arrow_table().to_pandas())
conn.close()
```

```text
  customer__country  revenue
0                SE   190.75
1                US   125.75
2                DE    75.50
```

ADBC reads a private CA from `SSL_CERT_FILE`.

## dbt's JDBC dialect { #semantic-connect-dialect }

A statement holds exactly one `{{ semantic_layer.<call>(...) }}`, alone or inside SQL around it.
The arguments are Python literals as dbt writes them: strings in single or double quotes, numbers, `True`, `False`, `None`, lists, and the calls `Dimension(...)`, `TimeDimension(...)`, `Entity(...)` and `Metric(...)`.

| Call | Arguments | Columns |
| --- | --- | --- |
| `metrics()` | `page_number`, `page_size` | `NAME`, `DESCRIPTION`, `TYPE`, `TYPE_PARAMS`, `FILTER`, `DIMENSIONS`, `QUERYABLE_GRANULARITIES`, `LABEL`, `REQUIRES_METRIC_TIME` |
| `dimensions(metrics=[...])` | `metrics`, paging | `NAME`, `DESCRIPTION`, `TYPE`, `TYPE_PARAMS`, `IS_PARTITION`, `EXPR`, `LABEL`, `QUALIFIED_NAME`, `QUERYABLE_GRANULARITIES` |
| `entities(metrics=[...])` | `metrics`, paging | `NAME`, `DESCRIPTION`, `TYPE`, `EXPR`, `ROLE` |
| `measures(metrics=[...])` | `metrics`, paging | `NAME`, `AGG`, `EXPR` |
| `queryable_granularities(metrics=[...])` | `metrics` | `QUERYABLE_GRANULARITIES`, the grains of `metric_time` |
| `metrics_for_dimensions(group_by=[...])` | `group_by`, paging | as `metrics()` |
| `saved_queries()` | paging | `NAME`, `DESCRIPTION`, `LABEL`, `METRICS`, `GROUP_BY`, `WHERE_FILTER`, `EXPORTS` |
| `dimension_values(metrics=[...], group_by='...')` | `metrics`, one `group_by` | The group-by's distinct values |
| `query(...)` | `metrics`, `group_by`, `where`, `order_by`, `limit`, `compile`, `saved_query`, `read_cache` | One column per group-by and metric; with `compile=True`, one row `SQL` |

- `page_number` starts at 1; without `page_size`, a call returns every row.
- `DIMENSIONS`, `QUERYABLE_GRANULARITIES`, `METRICS`, `GROUP_BY` and `WHERE_FILTER` are lists of strings; `TYPE_PARAMS` and `EXPORTS` are JSON text.
- In `query`, a metric is a name or `Metric('revenue', alias='sales')`, which names its column `sales`.
- A group-by is a name such as `'metric_time__month'`, `Dimension('metric_time').grain('month')`, `TimeDimension('metric_time', 'month')` or `Entity('customer')`.
- `where` is a filter, or a list of filters combined with `AND`, in the call syntax of [queries][semantic-query-cli].
- An order-by is a metric or group-by name, with a leading `-` for descending, or `Metric('revenue').descending(True)` or `Dimension('customer__country').descending(True)`.
- `saved_query` runs a [saved query][semantic-saved-queries], refined by the other arguments as in [Refine a saved query][semantic-saved-queries-refine].
- `read_cache=False` runs the query on Trino even when the [result cache][semantic-result-cache] holds it.

Refused statements fail with `INVALID_ARGUMENT` and the reason:

| Statement | Message |
| --- | --- |
| `semantic_layer.query_with_all_group_bys(...)` | `query_with_all_group_bys is not supported` |
| Any other call | `unknown call semantic_layer.<call>` |
| An argument the call does not take | `semantic_layer.<call> takes no argument <name>` |
| No call, or a call without `{{ }}`, with the [BI tables][semantic-bi-admin] off | `the statement must hold one {{ semantic_layer.<call>(...) }}` |
| Two calls | `a statement holds exactly one {{ semantic_layer.<call>(...) }}` |

### SQL around a call { #semantic-connect-outer-sql }

```sql
select customer__country, revenue
from {{ semantic_layer.query(metrics=['revenue'], group_by=['customer__country']) }}
where revenue > 100
order by revenue desc
```

- The SQL is one `SELECT`, with an optional `ORDER BY`.
- It reads the call's result and nothing else: a table name is refused, as the call's result is the only relation it can see.
- Column names are matched without regard to case.
- Around a `query`, the whole statement runs on Trino, with standard SQL functions and `TRY_CAST`, `IF`, `REGEXP_LIKE`, `SPLIT_PART`, `DAY_OF_WEEK`, `JSON_EXTRACT_SCALAR`, `DATE_FORMAT` and `APPROX_PERCENTILE`.
- Around a metadata call, it runs in the gateway, with standard SQL functions.

A statement that does not parse, or names another relation, fails with `the SQL around the semantic_layer call ...` and the parser's or validator's message.

## GraphQL { #semantic-connect-graphql }

The GraphQL API is dbt's, for metadata and the SQL of a query: the operations dbt-sl-sdk 0.13.4 sends for them, plus the paginated listings and `queryableGranularities`.
Queries run over Arrow Flight SQL, with [ADBC][semantic-connect-adbc], the [JDBC driver][semantic-connect-jdbc] or dbt-sl-sdk, or over [REST][semantic-query-rest].

| Kind | Operations |
| --- | --- |
| Query | `environmentInfo`, `metrics`, `metricsPaginated`, `dimensions`, `dimensionsPaginated`, `measures`, `entities`, `entitiesPaginated`, `savedQueries`, `savedQueriesPaginated`, `queryableGranularities` |
| Mutation | `compileSql` |

Every operation takes `environmentId`, the semantic project's id.
`compileSql` answers the SQL of a query without running it:

```bash
curl -s -X POST "https://hopsworks.example.com/semantic-layer/api/graphql" \
  -H "Authorization: Bearer $HOPSWORKS_API_KEY" -H "Content-Type: application/json" \
  -d '{"query": "mutation($metrics: [MetricInput!], $groupBy: [GroupByInput!]) { compileSql(environmentId: 7, metrics: $metrics, groupBy: $groupBy) { sql } }",
       "variables": {"metrics": [{"name": "revenue"}], "groupBy": [{"name": "customer__country"}]}}'
```

```json
{"data": {"compileSql": {"sql": "SELECT ..."}}}
```

- `compileSql` takes `metrics`, `groupBy`, `where`, `orderBy`, `limit` and `savedQuery`; it also takes `readCache`, as dbt's clients send it, which has no effect.
- `createQuery`, `query`, `createDimensionValuesQuery`, `cancelQuery`, `queryRecords` and `metricsForDimensions` are not in the schema, and a request for one answers a GraphQL validation error.
  `semantic_layer.metrics_for_dimensions(...)` of [dbt's JDBC dialect][semantic-connect-dialect] lists the metrics of group-bys over Arrow Flight SQL.
- An operation selects at most 500 fields, each alias counted; a larger one is refused before it runs.
- A refused request answers with HTTP 200 and an `errors` entry whose `extensions.code` is the gateway's error code, such as `SEMANTIC_LAYER_INVALID_QUERY`; a refused API key is `User is not authorized`.

## Timestamps { #semantic-connect-timestamps }

`metric_time` and the time dimensions come back as timestamps without a time zone, Arrow `timestamp[ms]`, holding UTC wall time: the queries run on Trino in UTC.
pyarrow and pandas show them as they are.
The Arrow Flight SQL JDBC driver 19.0.0 shows them shifted by the client JVM's offset from UTC, such as `2019-12-31 23:00` for `2020-01-01 00:00` on a client in CET; run the client JVM with `-Duser.timezone=UTC` to read the values as stored.

## Query handles { #semantic-connect-handles }

A Flight SQL ticket and a prepared statement are signed handles that carry the query, the build it was planned on, the user and the semantic project.
Any replica of the gateway serves a handle, so a client can fetch from another replica than the one that planned the statement.

| Handle | Valid for | When it ends |
| --- | --- | --- |
| Flight SQL ticket, prepared statement | 1 hour after it was issued | `UNAUTHENTICATED: the query handle expired, prepare the statement again`. |
| Flight SQL handle whose build was deleted | | `NOT_FOUND: the query handle expired, prepare the statement again`; a semantic project keeps its 20 newest builds. |

- A prepared statement answers from the build it was prepared on, even after a newer build answers queries, so its columns do not change under a client.
- A handle used by another user, or with another environment id, is refused with `UNAUTHENTICATED`.

## Limits { #semantic-connect-limits }

| API | Most rows | When a result is larger |
| --- | --- | --- |
| Arrow Flight SQL: dbt-sl-sdk queries, ADBC, JDBC | 1,000,000 | The result stops at 1,000,000 rows, with no signal: treat a result of exactly that many rows as cut. |
| REST, JSON | 100,000 | The result stops there, with `truncated: true` and the `X-Semantic-Truncated: true` header. |
| REST, Arrow | 1,000,000 | The result stops there; `X-Semantic-Truncated: true` is set when the cut is known before the first rows are sent, and `X-Semantic-Max-Rows` gives the cap. |

- Every API shares the query slots of a gateway replica, 16 by default, and the query time, 300 seconds, of [Query metrics][semantic-query-limits].
  Through the dbt-compatible layout, nginx also ends a call after `hopsworks.semanticLayer.dbtCompatibleLayout.timeoutSeconds`, 300 by default, see [The dbt-compatible endpoint layout][semantic-bi-dbt-layout].
- A replica's Arrow buffers are bounded, half the JVM heap by default; a query that finds them full fails with 503 `SEMANTIC_LAYER_BUSY`, or `UNAVAILABLE` over Flight SQL.
- A statement whose handle would be larger than 64 KiB is refused with `the statement is too large`.

## For administrators { #semantic-connect-admin }

The semantic gateway is installed with `global._hopsworks.semanticLayer.enabled: true`.
GraphQL needs nothing more: the `hopsworks` chart adds an Ingress for `/semantic-layer/api/graphql` on the ingress hosts.
Clients outside the cluster reach the Flight SQL port through a load balancer.

```yaml
semantic-gateway:
  externalLoadBalancer:
    enabled: true
    hostname: semantic.hopsworks.example.com
  signingKey:
    existingSecret: semantic-gateway-signing-key

hopsworks:
  variables:
    loadbalancer_external_domain_semantic_gateway: semantic.hopsworks.example.com
```

### The Flight SQL load balancer { #semantic-connect-admin-lb }

- `semantic-gateway.externalLoadBalancer` makes the Service `semantic-gateway-external` on `flightPort`, 18446, as the other external load balancers of the chart do: `enabled`, `class` and `annotations`, `managed: false` for a NodePort Service with an optional `nodePort`, and on AWS a TargetGroupBinding to `global.unmanagedLoadBalancers.semanticGateway.targetGroupId`.
- Clients check the name they dial against the gateway's certificate, so put the load balancer's DNS name, or IP address, in `externalLoadBalancer.hostname`.
  The chart adds it to the gateway's certificate, which otherwise holds only the names inside the cluster.
  Set it at install: the names of the certificate do not change on an upgrade unless the HopsworksCert `semantic-gateway` is deleted first.
- Set `hopsworks.variables.loadbalancer_external_domain_semantic_gateway` to the same name, so the connection details carry it.
  Left unset, the `hopsworks-update-lb-domains` job sets it from the load balancer's address, which is not in the certificate.
- `hopsworks.variables.semantic_gateway_flight_port`, `"18446"`, is the port the connection details carry; change it with `flightPort`, or when the load balancer listens on another port.

### The signing key { #semantic-connect-admin-signing-key }

The gateway signs query handles with a key from a Secret, under `current`, and also accepts a key under `previous`.
Each key is at least 32 characters.

- With `signingKey.existingSecret: null` and `global._hopsworks.mode: auto`, the chart creates the Secret `semantic-gateway-signing` with a random key and keeps it across upgrades.
- In any other mode, such as under ArgoCD, the chart cannot read the Secret back, so the render fails until `existingSecret` names a Secret you create:

```bash
kubectl -n hopsworks create secret generic semantic-gateway-signing-key \
  --from-literal=current="$(openssl rand -hex 32)"
```

Rotate the key in two rollouts, restarting the gateway after each change of the Secret with `kubectl -n hopsworks rollout restart deployment/semantic-gateway`:

1. Add the new key under `previous`, so every replica accepts it.
2. Move the new key to `current` and the old key to `previous`.

Handles signed with the old key keep working until they expire, after `handleTtlSeconds`; then the old key can be removed.

### Gateway values { #semantic-connect-admin-values }

| `semantic-gateway` value | Default | Meaning |
| --- | --- | --- |
| `flightPort` | `18446` | The Flight SQL port. |
| `handleTtlSeconds` | `3600` | How long a Flight SQL ticket or prepared statement stays valid. |
| `arrowMemoryLimitBytes` | `null` | The Arrow buffers a replica's queries hold at once; null is half the JVM heap. |
| `maxRows` | `1000000` | The rows of an Arrow result, over Flight SQL and REST. |

`hopsworks.semanticLayer.graphqlIngress.annotations` sets the annotations of the GraphQL Ingress.
The [result cache][semantic-result-cache-admin] has its own values, and [Semantic Layer administration][semantic-admin] lists every value of the service.
[The dbt-compatible endpoint layout][semantic-bi-dbt-layout] serves both APIs on port 443 of one host, for dbt's Tableau and Power BI connectors.

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-class"></code> [`SemanticProject`][hopsworks_common.semantic_layer.SemanticProject]
        - <code class="doc-symbol doc-symbol-method"></code> [`connection_info`][hopsworks_common.semantic_layer.SemanticProject.connection_info]
        - <code class="doc-symbol doc-symbol-method"></code> [`query`][hopsworks_common.semantic_layer.SemanticProject.query]
    - <code class="doc-symbol doc-symbol-docs"></code> [dbt Semantic Layer APIs](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-api-overview)

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>
