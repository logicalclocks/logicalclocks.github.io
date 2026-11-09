---
description: How BI tools and SQL clients read a semantic project as tables over Arrow Flight SQL, the SQL the gateway translates into metric queries, what it refuses, and how to connect DBeaver, JDBC, ODBC and dbt's Tableau and Power BI connectors.
---

# Connect BI Tools { #semantic-bi-tools }

Over Arrow Flight SQL, the semantic gateway shows each semantic project as tables: a `metrics` table with every group-by and every metric as columns, and one table per [saved query][semantic-saved-queries].
A BI tool or SQL client that browses tables lists them, and the gateway translates the SQL it sends over them into one metric query, which runs on Trino as the caller, as every metric query does.
Statements in [dbt's JDBC dialect][semantic-connect-dialect], `{{ semantic_layer.<call>(...) }}`, keep working on the same port; a statement without such a call is read as SQL over the tables.

The examples use the `sales` semantic project of [Define metrics][semantic-define-metrics], with id 7, and the Flight SQL host `semantic.hopsworks.example.com` of [Connect dbt clients][semantic-connect-clients].

!!! warning "Experimental"

    The tables are tested with the Apache Arrow Flight SQL JDBC driver 19.0.0: its `DatabaseMetaData` calls, schema probes, prepared statements and the SQL shapes Tableau generates, which DBeaver and other JDBC tools use too.
    dbt's Tableau connector 1.3.0 and Power BI connector 1.0.0 are not tested against Hopsworks yet, and the SQL they generate can hold shapes the gateway refuses.
    An administrator can turn the tables off, see [For administrators][semantic-bi-admin].

## The tables { #semantic-bi-tables }

| Level | Name |
| --- | --- |
| Catalog | `semantic_layer` |
| Schema | The environment id, the semantic project's id: `7` |
| Tables | `metrics`, and one table per saved query, named as the saved query |

- Every table has the type `VIEW`; a tool that lists only `TABLE` objects finds none.
- A caller sees only the schema of the environment id it connects with.
- The tables have no primary or foreign keys.
- They are the tables of the semantic project's current build, and a [prepared statement][semantic-connect-handles] keeps the build it was prepared on.

### Columns of `metrics` { #semantic-bi-columns }

In this order:

1. `metric_time` at each grain some metric can be queried at, from the finest: `metric_time__day`, `metric_time__week`, `metric_time__month`, `metric_time__quarter`, `metric_time__year`.
2. The other group-bys, named as in [queries][semantic-query-names]: entities such as `customer`, dimensions such as `customer__country`, and each time dimension at each of its grains, such as `order__order_ts__day` to `order__order_ts__year`.
3. Every metric, such as `revenue`, `orders` and `revenue_per_order`.

- Date parts are not columns: `EXTRACT` reads them from a time column, see [The SQL][semantic-bi-sql].
- Each column has the type the planner gives it when it plans the column alone, such as `TIMESTAMP` for `metric_time__day`, `VARCHAR` for `customer__country` and `DOUBLE` for `revenue`, and every column is nullable.
  Discovery, a schema probe, a prepared statement and the result all declare that type.
- Each column carries its description as its remarks, and the Arrow field metadata `semantic.kind`, `metric` or `group_by`.
- A column the planner cannot type alone is left out, and so is a metric whose name a group-by has; the gateway logs which and why.

A saved query's table has the saved query's columns: `revenue_by_country` has `metric_time__month`, `customer__country`, `revenue` and `orders`.
Its rows are the saved query's metrics and group-bys under the saved query's filters; the saved query's order and limit do not apply, the statement's do.
A saved query named `metrics` has no table.

## A metric column is the metric { #semantic-bi-metric-columns }

!!! warning "Aggregates around a metric column mean the metric itself"

    `SUM`, `AVG`, `MIN`, `MAX`, `COUNT` and `ANY_VALUE` around a metric column all return the metric, computed by its definition at the grain of the `GROUP BY`.
    `AVG(revenue)` returns `revenue`, and `COUNT(revenue)` returns `revenue` too, not a count.
    dbt's Semantic Layer connectors work the same way: Tableau always wraps a metric in `SUM`, and Power BI sends the aggregate picked in the report.

```sql
SELECT customer__country, AVG(revenue) AS avg_revenue, AVG(revenue_per_order) AS rpo
FROM semantic_layer."7".metrics
GROUP BY customer__country
ORDER BY 2 DESC
```

```text
customer__country  avg_revenue  rpo
SE                 190.75       47.6875
US                 125.75       62.875
DE                 75.5         37.75
```

`avg_revenue` is the `revenue` of each country, the same rows as `SELECT customer__country, SUM(revenue) ...`, and `rpo` is `revenue_per_order` computed per country.
A statement selects each column once, so `SUM(revenue)` and `AVG(revenue)` in one statement are refused.

A statement over one table is one metric query:

- the metrics are the metric columns it references, with or without an aggregate around them;
- the group-bys are the `GROUP BY` list;
- without `GROUP BY` and without an aggregate, the group-by columns it selects are the group-bys, so `SELECT * FROM revenue_by_country` returns the saved query's rows, and `SELECT customer__country, revenue FROM metrics` returns revenue per country;
- without `GROUP BY`, `SELECT SUM(revenue) FROM metrics` returns the total.

A ratio or a count of distinct customers is right at every grain, since the gateway computes the metric for the grain asked for, and never adds up the rows of a finer one.

## The SQL { #semantic-bi-sql }

```sql
SELECT customer__country,
       DATE_TRUNC('month', CAST(order__order_ts__day AS DATE)) AS m,
       SUM(revenue)
FROM semantic_layer."7".metrics
WHERE customer__country IN ('SE', 'US')
GROUP BY customer__country, DATE_TRUNC('month', CAST(order__order_ts__day AS DATE))
HAVING SUM(revenue) > 100
ORDER BY 3 DESC
LIMIT 50
```

is the metric query `metrics=[revenue]`, `group_by=[customer__country, order__order_ts__month]`, the filter `customer__country IN ('SE', 'US')`, `having=[revenue > 100]`, `order_by=[-revenue]` and `limit=50`, with the column `order__order_ts__month` returned as `m`.

| Clause | Accepted |
| --- | --- |
| `FROM` | One table: `metrics`, `"7".metrics`, `semantic_layer."7".metrics` or a saved query's table, with an optional alias; or one derived table that only renames the columns of one table. |
| `SELECT` | Group-by columns, metric columns, the aggregates above around a metric column, `*`, and aliases. `SELECT DISTINCT` over group-bys returns their distinct values. |
| Time | `DATE_TRUNC('<grain>', x)` and Tableau's `DATE_TRUNC(CAST(x AS DATE), '<grain>')` over a time column, to that grain or a coarser one whose periods each hold whole periods of the column (a `week` column truncates only to `week`); `EXTRACT(<part> FROM x)` with `YEAR`, `QUARTER`, `MONTH`, `DAY`, `ISODOW` or `DOY`, the date parts `year`, `quarter`, `month`, `day`, `dow` and `doy`, from a column whose periods each fall in one period of the part (`MONTH` from a `month` column, not `DAY`). |
| `CAST` | Only casts that keep every value: `DATE` to `TIMESTAMP`; `TIMESTAMP` to `DATE` for a column at day grain or coarser; `TINYINT`, `SMALLINT` and `INTEGER` to a wider integer, to `DOUBLE`, or to `DECIMAL(p, 0)` with enough digits; `BIGINT` to `DECIMAL(p, 0)` with `p` of at least 19; `VARCHAR(n)` to `VARCHAR(m)` with `m` of at least `n`, or to `VARCHAR`; a column to its own type. |
| `WHERE` | Comparisons, `IN`, `NOT IN`, `BETWEEN`, `LIKE`, `IS NULL` and `IS NOT NULL` over group-bys and literals, joined with `AND`, `OR` and `NOT`. Literals are PostgreSQL style, such as `DATE '2026-01-01'` and `TIMESTAMP '2026-01-01 00:00:00'`. |
| `GROUP BY` | Group-by columns and the time expressions above, by expression, alias or position. |
| `HAVING` | Comparisons, `IN`, `BETWEEN`, `LIKE`, `IS NULL` and `IS NOT NULL` over metric columns, with or without an aggregate, and over group-bys. A metric only in `HAVING` is computed and not returned. |
| `ORDER BY` | Columns, aggregates, aliases and positions, `ASC` or `DESC`; `NULLS LAST` is the order already. A metric only in `ORDER BY` is computed and not returned. |
| `LIMIT`, `OFFSET` | Numbers. |

- Names match without regard to case; quote an identifier with `"`.
- `HAVING` runs before `LIMIT`, in the metric query, so a limited result holds the groups that pass the `HAVING`.
- `WHERE 1=0` and `LIMIT 0`, the schema probes of BI tools, are answered from the table's columns without running a query.
- A statement runs as a metric query: it uses the [result cache][semantic-result-cache], its rows stop at the row cap of [Limits][semantic-connect-limits], and its time values are UTC wall time, see [Timestamps][semantic-connect-timestamps].
  It is recorded in the [query history][semantic-query-history] with the surface `BI`, and is never answered from an [export][semantic-exports-serving].

## What is refused { #semantic-bi-refused }

Anything outside the grammar above is refused before it runs, with the Flight SQL status `INVALID_ARGUMENT` and a message that names the construct:

```text
INVALID_ARGUMENT: the BI tables do not support joins; a statement over a BI table is one semantic query: group-by columns, metric columns (SUM, AVG, MIN, MAX, COUNT and ANY_VALUE around one mean the metric), DATE_TRUNC, EXTRACT and lossless CASTs of group-bys, WHERE on group-bys, GROUP BY, HAVING, ORDER BY, LIMIT and OFFSET
```

| Statement | The message names |
| --- | --- |
| A join | `joins` |
| `UNION`, `INTERSECT`, `EXCEPT` | `UNION`, and so on |
| A subquery in `SELECT`, `WHERE` or `IN` | `subqueries` |
| A window function, `WINDOW`, `QUALIFY` | `window functions`, `WINDOW clauses`, `QUALIFY` |
| A derived table that filters, groups or sorts, or two derived tables | `derived tables other than one that renames columns`, `more than one derived table` |
| Another table, or another schema than the environment id | `other tables (...)`, followed by the tables there are |
| An expression over columns, such as `revenue * 2` or `UPPER(customer__country)` | `* (expressions over columns)`, `UPPER (expressions over columns)` |
| `COUNT(*)`, `COUNT(DISTINCT revenue)` | `COUNT(*)`, `COUNT(DISTINCT ...)` |
| An aggregate around a group-by column | `SUM over the group-by column customer__country` |
| A metric column in `WHERE` | `metric columns in WHERE (revenue): filter metrics in HAVING` |
| A metric column in `GROUP BY` | `GROUP BY a metric column (revenue)` |
| `SELECT DISTINCT` with a metric column | `SELECT DISTINCT with metric columns` |
| `ROLLUP`, `CUBE`, `GROUPING SETS` | `ROLLUP`, and so on |
| A cast that can change values, such as `BIGINT` to `DOUBLE` | `CAST of <column> from BIGINT to DOUBLE, which can change values` |
| `DATE_TRUNC` to a finer grain than the column, or over a column that is not a time column | `DATE_TRUNC to day, finer than metric_time__month` |
| `DATE_TRUNC` over a column whose periods can straddle the target, such as a week into a month | `DATE_TRUNC to month over metric_time__week, whose periods can straddle two months` |
| `EXTRACT` of a part that varies within the column's periods, such as the day of a month | `EXTRACT(DAY) over metric_time__month, whose periods do not each fall in one day` |
| `EXTRACT(DOW FROM x)` | `EXTRACT(DOW), whose Sunday is 0 (ISODOW is supported)` |
| `NULLS FIRST` | `NULLS FIRST: NULL sorts last` |
| A column selected twice, such as `SUM(revenue), AVG(revenue)` | `selecting revenue twice` |
| A parameter marker, `?` | `parameter markers (?): prepared statements with parameters are not supported yet` |

A statement the grammar accepts can still fail as a metric query, with `INVALID_ARGUMENT` and the reason: an unknown column, a group-by column selected but missing from `GROUP BY`, a group-by the metrics cannot reach, or a statement that does not parse.

## Connect a tool { #semantic-bi-connect }

Every tool authenticates as dbt's clients do, with the environment id and an API key with the `FEATURESTORE` and `TRINO` scopes, see [Endpoints][semantic-connect-endpoints].

### DBeaver and other JDBC tools { #semantic-bi-jdbc }

Add the Apache Arrow Flight SQL JDBC driver, `org.apache.arrow:flight-sql-jdbc-driver` 19.0.0, as a driver:

| Setting | Value |
| --- | --- |
| Driver class | `org.apache.arrow.driver.jdbc.ArrowFlightJdbcDriver` |
| URL | `jdbc:arrow-flight-sql://semantic.hopsworks.example.com:18446?environmentId=7&useEncryption=true&tlsRootCerts=/home/me/hopsworks_semantic_119_7_ca.pem` |
| Driver property `token` | The API key |

- `tlsRootCerts` is the cluster's CA, which `hops semantic connect sales --ca-path <file>` writes, see [Connection details][semantic-connect-details]; leave it out when the client already trusts the certificate.
- In DBeaver, the tables show under the catalog `semantic_layer`, the schema `7`, and **Views**.
- Run the client JVM with `-Duser.timezone=UTC` to see the time values as stored, see [Timestamps][semantic-connect-timestamps].

### ODBC: Power BI, Excel and other ODBC tools { #semantic-bi-odbc }

The Apache Arrow Flight SQL ODBC driver, shipped as a Windows installer with Apache Arrow releases since 25.0.0, takes a connection string:

```text
Driver={Apache Arrow Flight SQL ODBC Driver};host=semantic.hopsworks.example.com;port=18446;environmentId=7;token=<api key>;useEncryption=true;trustedCerts=C:\certs\hopsworks_semantic_119_7_ca.pem;useSystemTrustStore=false
```

The driver sends connection properties it does not know, such as `environmentId`, as headers.
In Power BI and Excel, **Get Data** > **ODBC** with this connection string imports the tables, or the result of a SQL statement given under **Advanced options**, in Import mode.
Not tested against Hopsworks.

### dbt's Tableau and Power BI connectors { #semantic-bi-dbt-connectors }

dbt's connectors reach Arrow Flight SQL on port 443 of one host, the way they reach dbt Cloud, which the [dbt-compatible endpoint layout][semantic-bi-dbt-layout] serves.
An administrator turns it on with a host name, such as `semantic.example.com`.

| Connector field | Value |
| --- | --- |
| Host | The layout's host. dbt's Tableau connector adds `:443` after `.com`, so type `<host>:443` for a host that does not end in `.com`. dbt's Power BI connector uses TLS on port 443 only for a host that contains `.com`. |
| Environment ID | The semantic project's id, `7`. |
| Token | The API key. |

- dbt's Tableau connector does not check the server certificate.
  dbt's Power BI connector checks it against the Windows trust store, so the layout's TLS Secret needs a certificate Windows trusts.
- The connectors list the `metrics` table and one table per saved query; dbt Cloud names its `metrics` table `ALL`.
- Tableau sends every metric as `SUM(<metric>)`, which [means the metric][semantic-bi-metric-columns].
- dbt's Power BI connector works in DirectQuery mode only.

### Other tools { #semantic-bi-other }

| Tool | How |
| --- | --- |
| Tableau, without dbt's connector | **Other Databases (JDBC)** with the JDBC driver and URL above, browsing the tables, or with Custom SQL holding a `{{ semantic_layer.query(...) }}`. Tableau aggregates a Custom SQL result again, which is wrong for ratios and other metrics that do not add up; the tables do not have this problem. Not tested. |
| Dot | Its GraphQL URL is `https://<hopsworks host>/semantic-layer/api/graphql`, or `https://<layout host>/api/graphql` with the dbt-compatible layout. Not tested. |
| Mode, Hex | They send dbt's JDBC dialect to a host, which the dbt-compatible layout serves. Not tested. |

A tool that runs as a service, such as Tableau Cloud, Dot, Mode or Hex, reaches the gateway from the internet, and needs a certificate from a public CA.

## The dbt-compatible endpoint layout { #semantic-bi-dbt-layout }

dbt's Semantic Layer serves Arrow Flight SQL and GraphQL on port 443 of one host, with GraphQL at `/api/graphql`.
The `hopsworks` chart serves the gateway the same way on a host of your choice, through the cluster's ingress-nginx controller:

```yaml
hopsworks:
  semanticLayer:
    dbtCompatibleLayout:
      enabled: true
      host: semantic.example.com
      tlsSecret: semantic-example-com-tls
      timeoutSeconds: 300
```

| `hopsworks.semanticLayer.dbtCompatibleLayout` value | Default | Meaning |
| --- | --- | --- |
| `enabled` | `false` | Render the two Ingresses below. Needs `global._hopsworks.semanticLayer.enabled`. |
| `host` | `""` | The host name the connectors are given; required when `enabled`. dbt's Power BI connector accepts only names that contain `.com`. |
| `tlsSecret` | `null` | A `kubernetes.io/tls` Secret with the certificate and key for `host`. Null serves the ingress controller's default certificate. |
| `timeoutSeconds` | `300` | Seconds nginx waits on a Flight call or a GraphQL request. Keep it at least `semantic-gateway.queryTimeoutSeconds`, or nginx ends long queries first. |

nginx annotations apply to a whole Ingress, so the layout is two Ingresses on `host`, both with `tlsSecret`:

| Ingress | Path | Routes to |
| --- | --- | --- |
| `<release>-semantic-layer-dbt-flight` | `/arrow.flight.protocol.FlightService/`, implementation specific, the path type ingress-nginx's path validation allows a dot in | The gateway's Flight port over gRPC with TLS, with gRPC read and send timeouts of `timeoutSeconds`. |
| `<release>-semantic-layer-dbt-graphql` | `/api/graphql`, exact | The gateway's GraphQL handler at `/semantic-layer/api/graphql`, over HTTPS, hashed by the `Authorization` header so the polls of a query reach the replica that holds its result. |

`<release>` is the full name of the `hopsworks` release, `hopsworks` by default.
Point the host's DNS name at the ingress controller.
Arrow Flight SQL clients then connect to `grpc+tls://semantic.example.com:443`, and dbt-sl-sdk with `host="semantic.example.com"` and without `DBT_SL_GRAPHQL_URL_FORMAT` and `DBT_SL_ADBC_URL_FORMAT`, since its defaults are dbt's layout.

## For administrators { #semantic-bi-admin }

| `semantic-gateway` value | Default | Meaning |
| --- | --- | --- |
| `biTables.enabled` | `true` | Serve the tables, `BI_TABLES_ENABLED` in the gateway. |

```yaml
semantic-gateway:
  biTables:
    enabled: false
```

With `false`, the gateway lists no schemas, tables or table types, and refuses a statement without a `{{ semantic_layer.<call>(...) }}` with `the statement must hold one {{ semantic_layer.<call>(...) }}`; dbt's JDBC dialect works as before.
