---
description: Guide on how to use Query Engine as a Hopsworks user
---

# Query Engine (Trino)

The Query Engine in Hopsworks is powered by Trino, a distributed SQL query engine that allows you to run interactive analytics on your data. Use it to explore feature groups, run ad-hoc queries, and analyze data across your project.

## Accessing the Query Engine

Navigate to the Query Engine from your project's left sidebar. The Query Engine interface provides access to the SQL runner, cluster information, and query history.

<figure>
  <img src="../../../../assets/images/guides/trino/query-engine.png" alt="Query Engine" />
  <figcaption>Query Engine</figcaption>
</figure>

## SQL Runner

The SQL runner is where you write and execute SQL queries against your data.

**To run a query:**

1. Write your SQL query in the editor
2. Select the database/catalog you want to query
3. Click "Run" to execute the query
4. View results in the table below the editor

The SQL runner supports standard SQL syntax and provides auto-completion for databases, tables, and columns.

<figure>
  <img src="../../../../assets/images/guides/trino/sql-runner.png" alt="SQL runner" />
  <figcaption>SQL runner</figcaption>
</figure>

### SQL Statement Syntax Help

Need help with SQL syntax? Click the help icon in the SQL runner to access the complete reference of all allowed SQL statement syntax. This includes SELECT statements, functions, data types, operators, and more. The syntax reference is readily available without leaving the query interface.

<figure>
  <img src="../../../../assets/images/guides/trino/sql-statement-syntax.png" alt="SQL statement syntax" />
  <figcaption>SQL statement syntax</figcaption>
</figure>

## Cluster Overview

The cluster overview shows the health and status of your Trino cluster. Here you can monitor:

- **Active workers**: Number of workers currently processing queries
- **Running queries**: Queries currently being executed
- **Resource utilization**: CPU and memory usage across the cluster
- **Worker status**: Health status of individual worker nodes

This information helps you understand cluster performance and capacity.

<figure>
  <img src="../../../../assets/images/guides/trino/cluster-overview.png" alt="cluster overview" />
  <figcaption>Query Engine cluster overview</figcaption>
</figure>

## Managing Catalogs

Catalogs connect the Query Engine to external data sources such as PostgreSQL, MySQL, BigQuery, or MongoDB.
Project Data Owners can create, edit, and delete catalogs for their project from the Catalogs tab.
A catalog you create is named `<project>__<name>` and is only queryable within your own project.

<figure>
  <img src="../../../../assets/images/guides/trino/catalogs-list.png" alt="Catalogs list" />
  <figcaption>The Catalogs tab lists the shared default catalogs and your project's catalogs</figcaption>
</figure>

### Creating a Catalog

Click "Create catalog", then provide the catalog details:

1. Enter a name. The `<project>__` prefix is added automatically, so you type only the short name.
2. Choose the connector type from the list.
3. Enter the connector properties, one `key=value` per line.

The picker offers every connector installed in the Query Engine, so a connector it does not list cannot be used:

`bigquery`, `cassandra`, `clickhouse`, `delta_lake`, `druid`, `duckdb`, `elasticsearch`, `exasol`, `faker`, `gsheets`, `hive`, `hudi`, `iceberg`, `ignite`, `kafka`, `lakehouse`, `loki`, `mariadb`, `mongodb`, `mysql`, `opensearch`, `oracle`, `pinot`, `postgresql`, `prometheus`, `redis`, `redshift`, `singlestore`, `snowflake`, `sqlserver`, `trino_thrift`.

Connectors that expose no external data source are rejected, because a catalog on one would either read the Query Engine's own internals or hold nothing: `system`, `jmx`, `memory`, `blackhole`, `datasketches`, `ai`, and the `tpch` and `tpcds` sample generators.
The last two are already available to every project as shared catalogs, so there is no reason to create your own.

Reference a Hopsworks secret with `${HOPSWORKS_SECRET:<name>}` instead of typing the value inline to keep the secret out of the stored catalog definition.
Type `${HOPSWORKS_SECRET:` in the properties editor to pick from your own secrets.

A reference resolves against the secrets of the person who created the catalog, so you can only reference your own: naming a colleague's secret does not work, even if you can both see the catalog.
Two consequences follow. A referenced secret cannot be deleted while a catalog still uses it, and the catalog keeps working after you leave the project only if the secret still exists.
If a catalog needs to outlive your account, have someone recreate it under theirs, or use a literal value instead of a reference.

!!! warning "Only secrets created from typed text can be referenced"
    A secret created by uploading a file holds the base64 encoding of that file's contents, not the contents themselves.
    A reference to such a secret puts that base64 text into the catalog, and the connector then fails, because it receives an encoded string where it expects a password, a key, or a JSON document.
    Nothing records how a secret was created, so Hopsworks cannot detect the case and decode it for you, and the resulting error comes from the connector rather than from Hopsworks: an authentication failure, or a complaint that a value is malformed.

    Create the secret by typing or pasting the value as text when you intend to reference it from a catalog.
    For a credential that is naturally a file, such as a service account JSON, paste the file's contents rather than uploading the file.

Properties must address the data source over the network, for example `jdbc:`, `thrift:`, `https:` or `s3:`.
A property that points at a file path on the query engine's own machines is rejected, because you cannot place files there and the only files such a path could reach belong to the cluster itself.
If a connector you need requires a local file, ask an administrator to provide it.

Two limits apply, because every project's catalogs share a fixed amount of storage in the cluster.
A project may create a set number of catalogs, five by default, and a single definition may not exceed a set size, 16 KiB by default, measured after any secret references are resolved.
Both are cluster settings an administrator can raise, and neither is close to what an ordinary catalog needs: a few hundred bytes is typical, and even one carrying a service account JSON stays a few KiB.
Property values must also be latin1 text, which is what the definition is stored as, so a credential containing characters outside it has to come from a Hopsworks secret rather than being typed into a property.

<figure>
  <img src="../../../../assets/images/guides/trino/create-catalog.png" alt="Create catalog" />
  <figcaption>Creating a catalog with the auto-prefixed name and connector properties</figcaption>
</figure>

### Testing the Connection

Click "Test connection" to validate the configuration against the backing system before you save.
The test creates a temporary catalog, lists its schemas, and reports the result, so you catch a wrong host, port, or credential immediately.

When the connection cannot be established, the connector's own error is shown.

<figure>
  <img src="../../../../assets/images/guides/trino/test-connection-failed.png" alt="Test connection failed" />
  <figcaption>A failed test reports the underlying connector error</figcaption>
</figure>

When the configuration is correct, the test confirms that the catalog connects.

<figure>
  <img src="../../../../assets/images/guides/trino/test-connection-success.png" alt="Test connection succeeded" />
  <figcaption>A successful connection test</figcaption>
</figure>

### Availability After Creation

A newly created catalog has the status Pending sync, meaning it is saved but not yet loaded by the running Query Engine.
It becomes queryable only after an administrator syncs it and restarts Trino, because Trino reads catalogs only at startup.
Until then the catalog is listed with its pending status and does not appear as a target in the SQL runner.

Administrators are not notified when you create a catalog, and you are not notified when they apply it.
There is no service level on this step, so contact your administrator if a catalog has been pending longer than you expect, and watch the status on this page to see when it becomes Synced.

<figure>
  <img src="../../../../assets/images/guides/trino/catalog-pending-sync.png" alt="Catalog pending sync" />
  <figcaption>A created catalog waits in Pending sync until an administrator applies it</figcaption>
</figure>

### When a Catalog Fails to Load

A catalog can be valid to save and still be rejected by the Query Engine, for example when a connector requires a property the definition does not set.
Trino reads catalogs only at startup and refuses to start if it cannot load one, so such a catalog is removed from the engine automatically and marked Failed to keep the Query Engine available for everyone.

The status shows the error the Query Engine reported, which says what to correct.
Edit the catalog to fix the definition: it returns to Pending sync and follows the normal flow again.
Use "Test connection" before saving to catch most of these earlier.

<figure>
  <img src="../../../../assets/images/guides/trino/catalog-failed.png" alt="Failed catalog" />
  <figcaption>A catalog the Query Engine could not load, with the reason it reported</figcaption>
</figure>

### Access to Catalog Tables

Access to a user-created catalog is granted at the catalog level per project: a project's Data Owners can read and write, and Data Scientists can read.
The project's roles are granted the whole catalog; there is no per-schema or per-table configuration for these catalogs.
To limit what a catalog exposes, scope the database user in the connection credentials at the source database, since Trino reads the external system as that user and can only ever see what those credentials allow.

## Queries

The Queries tab displays a history of all executed queries. For each query, you can see:

- **Query ID**: Unique identifier for the query
- **Status**: Completed, failed, or running
- **Duration**: How long the query took to execute
- **User**: Who submitted the query
- **Timestamp**: When the query was run

Click on any query to view detailed execution information.

<figure>
  <img src="../../../../assets/images/guides/trino/queries.png" alt="queries" />
  <figcaption>Queries</figcaption>
</figure>

## Query Details

Clicking on a query opens the detailed view with comprehensive execution information.

### Overview

The overview tab shows query metadata, execution timeline, and performance metrics including:

- Query text
- Execution time
- Data processed
- Rows returned
- Resource consumption

<figure>
  <img src="../../../../assets/images/guides/trino/query-details.png" alt="Query details" />
  <figcaption>Query details</figcaption>
</figure>

### Live Plan

The live plan visualizes the query execution plan in real-time, showing how Trino processes your query across different stages and operators.

<figure>
  <img src="../../../../assets/images/guides/trino/query-details-live-plan.png" alt="Query details live plan" />
  <figcaption>Query details: live plan</figcaption>
</figure>

### Stages

The stages view breaks down query execution into individual stages, showing:

- Stage dependencies
- Data flow between stages
- Resource usage per stage
- Execution time for each stage

This helps identify performance bottlenecks in complex queries.

<figure>
  <img src="../../../../assets/images/guides/trino/query-details-stage.png" alt="Query details stages" />
  <figcaption>Query details: stages</figcaption>
</figure>

### Splits

Splits show how Trino parallelizes query execution. Each split represents a portion of data processed by a worker. View split-level metrics to understand query parallelism and data distribution.

<figure>
  <img src="../../../../assets/images/guides/trino/query-details-split.png" alt="Query details split" />
  <figcaption>Query details: split</figcaption>
</figure>

### References

The references tab lists all tables and data sources accessed by the query, helping you understand data dependencies.

<figure>
  <img src="../../../../assets/images/guides/trino/query-details-ref.png" alt="Query details references" />
  <figcaption>Query details: references</figcaption>
</figure>

### JSON

The JSON view provides the complete query execution plan and statistics in JSON format, useful for programmatic analysis or debugging.

<figure>
  <img src="../../../../assets/images/guides/trino/query-details-json.png" alt="Query details json" />
  <figcaption>Query details: json</figcaption>
</figure>

## Best Practices

- **Limit result sets**: Use `LIMIT` clauses for exploratory queries to reduce resource usage
- **Filter early**: Apply `WHERE` clauses to reduce data scanned
- **Monitor query performance**: Check the Queries tab to identify slow or failed queries
- **Use the live plan**: For complex queries, review the execution plan to optimize performance
- **Check cluster status**: Ensure adequate resources are available before running large queries
