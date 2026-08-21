---
description: Guide on how to use Query Engine as a Hopsworks user
---

# Query Engine (Trino)

The Query Engine in Hopsworks is powered by Trino, a distributed SQL query engine that allows you to run interactive analytics on your data. Use it to explore feature groups, run ad-hoc queries, and analyze data across your project.

## Accessing the Query Engine

Open **Queries** under **Analytics** in your project's left sidebar.
The page carries four tabs: **SQL Runner**, **Cluster Overview**, **Catalogs** and **Queries**.

<figure>
  <img src="../../../../assets/images/guides/trino/query-engine.png" alt="Query Engine" />
  <figcaption>The Query Engine, open on the SQL Runner tab</figcaption>
</figure>

## SQL Runner

The SQL runner is where you write and execute SQL queries against your data.

**To run a query:**

1. Pick a **Catalog** and a **Schema**.
   The tables in that schema are then listed below, and you can write the query against bare table names instead of qualifying every one.
2. Write the query in the editor, or click a table to start from `SELECT * FROM <table>`.
3. Choose a row limit, which is appended to the query as a `LIMIT`.
4. Click **Run**.

Results appear below the editor on two tabs: **Results** holds the rows, and **Table** holds the column names and types.
The editor auto-completes catalogs, schemas, tables and columns, and **Add query** opens a second tab so several queries can be kept side by side.

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

The cluster overview reports the query engine's version, environment and uptime, then a tile per metric, each with a sparkline of its recent history:

- **Running queries**, **Queued queries** and **Blocked Queries**
- **Active workers** and **Worker Parallelism**
- **Runnable drivers**, **Input Rows/s** and **Input Bytes/s**
- **Reserved Memory**

Together they say whether the cluster is busy and whether a slow query is competing for capacity.

<figure>
  <img src="../../../../assets/images/guides/trino/cluster-overview.png" alt="cluster overview" />
  <figcaption>Query Engine cluster overview</figcaption>
</figure>

## Managing Catalogs

The Catalogs tab is where a project makes an external data source queryable from the SQL runner.
Creating a catalog from a data source or by hand, referencing credentials, testing the connection, and when a change reaches the query engine are all covered in [Trino Catalogs][trino-catalogs].

## Queries

The Queries tab lists the queries the project has run, filterable by state and sortable, with the query text alongside each entry.
A card carries its id and state with a progress bar, the user and source that submitted it, the resource group, its split counts, wall, total and CPU time, and its reserved, peak and cumulative memory.
A query that is still running is listed the same way and updates in place.

Click a query id to open its details.

<figure>
  <img src="../../../../assets/images/guides/trino/queries.png" alt="queries" />
  <figcaption>The project’s query history</figcaption>
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

The live plan draws the query's stages and the operators inside them, with each stage's state and its CPU time, memory, drivers and tasks, updating while the query runs.
The graph is usually taller than the page, so it can be laid out **Vertical** or **Horizontal**, panned by dragging, and zoomed by scrolling.

<figure>
  <img src="../../../../assets/images/guides/trino/query-details-live-plan.png" alt="Query details live plan" />
  <figcaption>Query details: live plan</figcaption>
</figure>

### Stage performance

This view takes one stage at a time, chosen with the **Stage** selector, and draws its pipelines operator by operator.
Each operator reports its throughput, output rows and bytes, driver count, and CPU, wall and blocked time, which is what locates a bottleneck inside a stage rather than merely between stages.

<figure>
  <img src="../../../../assets/images/guides/trino/query-details-stage.png" alt="Query details stages" />
  <figcaption>Query details: stage performance</figcaption>
</figure>

### Splits

Splits show how Trino parallelizes query execution. Each split represents a portion of data processed by a worker. View split-level metrics to understand query parallelism and data distribution.

<figure>
  <img src="../../../../assets/images/guides/trino/query-details-split.png" alt="Query details split" />
  <figcaption>Query details: split</figcaption>
</figure>

### References

The references tab lists the tables the query read, each with the user it was authorized as and whether the query named it directly, and the routines it called.

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
