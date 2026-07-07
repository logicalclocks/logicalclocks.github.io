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
2. Choose the connector type, for example `postgresql`, `mysql`, `bigquery`, or `mongodb`.
3. Enter the connector properties, one `key=value` per line.

Reference a Hopsworks secret with `${HOPSWORKS_SECRET:<name>}` instead of typing the value inline to keep the secret out of the stored catalog definition.
Type `${HOPSWORKS_SECRET:` in the properties editor to pick from your own secrets.

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

<figure>
  <img src="../../../../assets/images/guides/trino/catalog-pending-sync.png" alt="Catalog pending sync" />
  <figcaption>A created catalog waits in Pending sync until an administrator applies it</figcaption>
</figure>

### Access to Catalog Tables

Access to a user-created catalog is granted at the catalog level per project: a project's Data Owners can read and write, and Data Scientists can read.
Trino's file-based access control provides no per-schema or per-table restriction for these catalogs, so access is all-or-nothing within the catalog.
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
