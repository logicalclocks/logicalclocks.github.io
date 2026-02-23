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
  <img src="../../../../assets/images/guides/trino/query-details-ref.png" alt="Query details referances" />
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