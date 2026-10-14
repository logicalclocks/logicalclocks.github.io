# Analytics Guides

Analytics is the SQL and dashboard layer over the feature store: Trino queries the offline data, Superset charts it.
Start with a query, then turn it into a dashboard.

<!-- markdownlint-disable MD030 -->
<div class="grid cards hops-start" markdown>

-   :material-chart-box-outline:{ .lg .middle } **Start here**

    ---

    Open the Query Engine from the project sidebar and run SQL against a feature group.
    One catalog per table format, so pick `delta`, `iceberg` or `hudi` first.

    ```sql
    SELECT customer_id, avg(amount) AS avg_amount
    FROM delta.fraud_featurestore.transactions_1
    GROUP BY customer_id
    ORDER BY avg_amount DESC
    LIMIT 10
    ```

    [Query engine](../projects/trino/query_engine.md) · [Superset](../projects/superset/superset.md)

</div>
<!-- markdownlint-enable MD030 -->

<div class="hops-task-index" markdown>

<div class="hops-task-group" markdown>
:material-database-search-outline:{ .hops-role-ico } Query
{ .hops-role-cap }

- [Query engine](../projects/trino/query_engine.md)
  Run interactive SQL over feature groups, with query history and cluster status.
- [Trino catalogs](../projects/trino/catalogs.md)
  Expose a data source as a catalog so external tables join feature data.
- [External BI tools](../../concepts/mlops/bi_tools.md)
  How a BI tool connects to the offline store through Trino.

</div>

<div class="hops-task-group" markdown>
:material-view-dashboard-outline:{ .hops-role-ico } Visualize
{ .hops-role-cap }

- [Superset](../projects/superset/superset.md)
  SQL Lab, datasets, charts and dashboards inside the project.
- [Share a dashboard](../projects/superset/superset.md#sharing-and-collaboration)
  Give project members access to a dashboard.
- [Enable Superset](../../setup_installation/admin/superset.md)
  Administrator setup, users and roles.

</div>

</div>
