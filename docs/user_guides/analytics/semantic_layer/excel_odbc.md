---
description: How to read a semantic project's metrics in Excel and ODBC tools, through the Apache Arrow Flight SQL ODBC driver or the REST API as CSV, with the connection strings, the Power Query steps and what is refused.
---

# Excel and ODBC { #semantic-excel-odbc }

Excel and other ODBC tools read metrics in two ways:

- **ODBC:** the Apache Arrow Flight SQL ODBC driver connects to the semantic gateway's Arrow Flight SQL port and shows each semantic project as [tables][semantic-bi-tables], which plain SQL queries.
- **REST as CSV:** a `GET` of the [query endpoint][semantic-query-rest] with the query in the URL answers CSV, which Excel reads with no driver: through **From Web** on Windows, and through the [Power Query template][semantic-excel-power-query] elsewhere.

Both authenticate with an API key with the `FEATURESTORE` and `TRINO` scopes, and both run each query as a metric query of the key's user, see [Who a query runs as][semantic-overview-identity].

## The ODBC driver { #semantic-odbc-driver }

| Platform | Install |
| --- | --- |
| Windows | `Apache-Arrow-Flight-SQL-ODBC-<version>-win64.msi` from the assets of an [Apache Arrow release](https://github.com/apache/arrow/releases) (25.0.0 and later). The driver is named `Apache Arrow Flight SQL ODBC Driver`. |
| Linux (RHEL, AlmaLinux, Rocky 9) | The `arrow-flight-sql-odbc-devel` package from the Apache Arrow repository, with unixODBC, see below. |
| macOS | No released installer yet. |

On AlmaLinux 9:

```bash
sudo dnf install -y epel-release dnf-plugins-core
sudo dnf config-manager --set-enabled crb
sudo dnf install -y https://packages.apache.org/artifactory/arrow/almalinux/9/apache-arrow-release-latest.rpm
sudo dnf install -y unixODBC arrow-flight-sql-odbc-devel
```

The library is `/usr/lib64/libarrow_flight_sql_odbc.so.2600.1.0` for Arrow 26.0.1, and `/usr/share/arrow/flight/sql/odbc/arrow-flight-sql-odbc-template.ini` registers it in `odbcinst.ini`.

### Connection string { #semantic-odbc-connection-string }

```text
Driver={Apache Arrow Flight SQL ODBC Driver};host=semantic.hopsworks.example.com;port=18446;environmentId=7;token=<api key>;useEncryption=true;trustedCerts=C:\certs\hopsworks_semantic_119_7_ca.pem;useSystemTrustStore=false
```

| Key | Value |
| --- | --- |
| `host`, `port` | The gateway's Arrow Flight SQL address, which `hops semantic connect <project>` prints, see [Connection details][semantic-connect-details]. |
| `environmentId` | The semantic project's id. The driver sends keys it does not know as headers, which is how the gateway reads it. |
| `token` | The API key, sent as `Authorization: Bearer`. |
| `trustedCerts` | The cluster's CA as a PEM file, which `hops semantic connect <project> --ca-path <file>` writes. Leave it and `useSystemTrustStore=false` out when the system already trusts the gateway's certificate. |

A DSN in `odbc.ini` holds the same keys:

```ini
[hopsworks-sales]
Driver = Apache Arrow Flight SQL ODBC Driver
host = semantic.hopsworks.example.com
port = 18446
environmentId = 7
useEncryption = true
trustedCerts = /home/me/hopsworks_semantic_119_7_ca.pem
useSystemTrustStore = false
```

### Query { #semantic-odbc-query }

The tables are in the catalog `semantic_layer`, under the schema named by the environment id, as views: `metrics` and one table per saved query.
From Python with pyodbc:

```python
import os

import pyodbc


api_key = os.environ["HOPSWORKS_API_KEY"]
conn = pyodbc.connect("DSN=hopsworks-sales;token=" + api_key, autocommit=True)
cursor = conn.cursor()
print([row.table_name for row in cursor.tables(catalog="semantic_layer")])
cursor.execute(
    'SELECT metric_time__month, SUM(bookings) FROM semantic_layer."7".metrics '
    "GROUP BY metric_time__month ORDER BY metric_time__month"
)
print(cursor.fetchall())
```

```text
['metrics']
[(datetime.datetime(2019, 12, 1, 0, 0), 31), (datetime.datetime(2020, 1, 1, 0, 0), 15), ...]
```

The driver passes SQL through unchanged, so a statement holding dbt's query call also works:

```sql
select * from {{ semantic_layer.query(metrics=['bookings'], group_by=[Dimension('metric_time').grain('month')]) }}
```

Time columns come back as `TIMESTAMP` (ODBC type 93), metrics as `BIGINT` or `DOUBLE`, and categorical columns as `VARCHAR`.

### What the driver does and does not do { #semantic-odbc-limits }

Tested with the driver of Apache Arrow 26.0.1 (driver version 00.09.0000), through unixODBC 2.3.12 and pyodbc on AlmaLinux 9:

| Works | Refused |
| --- | --- |
| Listing catalogs, schemas, tables, table types and columns | A parameter marker, `?`: parameters are not supported yet |
| `SELECT` of group-by columns and metric columns, with or without `SUM(...)` | ODBC function escapes such as `{fn CONVERT(...)}` |
| Quoted names, table aliases such as `"$Table"`, and a group-by over a derived table that only selects columns, as Power Query writes them | `SELECT *` over the `metrics` table, when its metrics do not share every group-by: it asks for every metric by every group-by at once |
| `TOP n`, read as `LIMIT n`, and `LIMIT`, `OFFSET` | `SELECT DISTINCT metric_time__<grain>` without a [time spine][semantic-time-spine] at that grain |
| `DATE_TRUNC`, `WHERE` on group-bys, ODBC timestamp literals such as `{ts '2020-01-01 00:00:00'}` | Anything else outside the [BI grammar][semantic-bi-refused], with a message naming it |
| `SELECT DISTINCT` of a categorical column, a `{{ semantic_layer.query(...) }}` statement, `{{ semantic_layer.metrics() }}` | |

`SELECT *` reads every column of a saved query's table, so an import of a whole table picks a saved query's table, or the `metrics` table with the columns chosen.

## Excel through ODBC { #semantic-excel-odbc-steps }

With the driver installed on Windows:

1. **Data** > **Get Data** > **From Other Sources** > **From ODBC**.
2. Under **Data source name (DSN)**, pick the DSN, or **(None)** with the connection string under **Advanced options**.
3. To import a fixed query, type it under **SQL statement (optional)** in **Advanced options**, for example `SELECT metric_time__month, SUM(bookings) AS bookings FROM metrics GROUP BY 1`.
4. Without a statement, the **Navigator** lists the tables under `semantic_layer` and the environment id; pick a saved query's table, or the `metrics` table and then **Transform Data** > **Choose Columns** before loading.
5. **Load** imports the rows; **Data** > **Refresh All** runs the query again.

Excel imports a copy of the rows: each refresh is one metric query.
Not yet tested in Excel itself.

## Excel from the web, no driver { #semantic-excel-web }

`GET` on the query endpoint takes the query as URL parameters and answers CSV with `format=csv`:

```text
https://<hopsworks host>/semantic-layer/v1/projects/7/query?metrics=bookings,booking_value&groupBy=metric_time__month&orderBy=metric_time__month&format=csv
```

```text
metric_time__month,bookings,booking_value
2019-12-01 00:00:00,31,13859.849999999999
2020-01-01 00:00:00,15,5378.810000000001
```

In Excel on Windows:

1. **Data** > **From Web**, then **Advanced**.
2. Put the URL in **URL parts**.
3. Under **HTTP request header parameters**, add `Authorization` with the value `ApiKey <api key>`.
4. When Excel asks how to sign in to the site, choose **Anonymous**: the header carries the key.
5. **Load** the table; **Refresh All** queries again.

Excel for Mac has no **Advanced** dialog under **From Web**; there, the [Power Query template][semantic-excel-power-query] goes into **Get Data** > **Blank Query** > **Advanced Editor**, untested.
Excel checks the gateway's certificate against the computer's trust store, so a cluster whose certificate comes from the Hopsworks CA needs that CA trusted on the computer.
Not yet tested in Excel itself.

### Power Query template { #semantic-excel-power-query }

The same query as a POST from Power Query's **Advanced Editor**, for a query too long for a URL:

```text
let
    ApiKey = "<api key>",
    Body = "{""metrics"": [""bookings""], ""groupBy"": [""metric_time__month""], ""orderBy"": [""metric_time__month""]}",
    Response = Web.Contents(
        "https://<hopsworks host>/semantic-layer/v1/projects/7/query",
        [
            Headers = [Authorization = "ApiKey " & ApiKey, #"Content-Type" = "application/json", Accept = "text/csv"],
            Content = Text.ToBinary(Body)
        ]
    ),
    Rows = Csv.Document(Response, [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Table = Table.PromoteHeaders(Rows, [PromoteAllScalars = true])
in
    Table
```

The URL takes `metrics`, `groupBy` and `orderBy` comma-separated or repeated (`-name` sorts descending), `where` repeated, `limit`, `offset`, `savedQuery`, `cache`, `useExports` and `format`; any other parameter is refused, see [Query over REST][semantic-query-rest].

A CSV answer holds at most the gateway's JSON row cap, 100,000 rows by default, and 64 MiB counted as JSON text; a larger answer is refused with 413 `SEMANTIC_LAYER_INVALID_QUERY`, see [Limits][semantic-query-limits].
A cut answer carries the header `X-Semantic-Truncated: true`, which Excel does not show: a query that may return more rows needs a `limit`, a coarser grain or fewer group-bys.

## dbt's Excel add-in { #semantic-excel-dbt-addin }

dbt's Semantic Layer add-in for Excel asks for a host, an environment id and a token, like dbt's other connectors.
Whether it works against Hopsworks is not yet known: dbt does not document what it sends.
A browser page such as an add-in can call the gateway's GraphQL API only from an origin an administrator allows with `semantic-gateway.cors.allowedOrigins`, see [For administrators][semantic-bi-admin].
