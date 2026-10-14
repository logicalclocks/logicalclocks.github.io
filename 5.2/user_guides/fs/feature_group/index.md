# Feature Group User Guides

A feature group is a table of features with a primary key and, usually, an event time.
These guides cover creating one, keeping its data correct, and managing it over time.

<!-- markdownlint-disable MD030 -->
<div class="grid cards hops-start" markdown>

-   :material-table-plus:{ .lg .middle } **Start here**

    ---

    Create a feature group and insert a DataFrame.
    The schema is inferred from the DataFrame on the first insert.

    ```python
    fg = fs.get_or_create_feature_group(
        name="transactions",
        version=1,
        primary_key=["tid"],
        event_time="datetime",
    )
    fg.insert(df)
    ```

    [Create a feature group](create.md) · [Data types and schema](data_types.md) · [Statistics](statistics.md)

</div>
<!-- markdownlint-enable MD030 -->

<div class="hops-task-index" markdown>

<div class="hops-task-group" markdown>
:material-table-plus:{ .hops-role-ico } Create and write
{ .hops-role-cap }

- [Create a feature group](create.md)
  Offline and online tables, primary keys, event time, partitioning.
- [External feature groups](create_external.md)
  Read data that stays in a warehouse or object store.
- [Spine groups](create_spine.md)
  Supply keys, event times and labels without storing features.
- [Ingest with dltHub](ingest_with_dlthub.md)
  Load from external sources through dlt pipelines.
- [Data types and schema](data_types.md)
  Type mapping, adding features, schema versions.

</div>

<div class="hops-task-group" markdown>
:material-check-decagram-outline:{ .hops-role-ico } Trust
{ .hops-role-cap }

- [Statistics](statistics.md)
  What is computed on insert and how to configure it.
- [Data validation](data_validation.md)
  Great Expectations on insert, then the advanced guide and best practices.
- [Feature monitoring](feature_monitoring.md)
  Scheduled statistics and comparison to a reference window.
- [Online ingestion observability](online_ingestion_observability.md)
  Track rows arriving in the online store.

</div>

<div class="hops-task-group" markdown>
:material-cog-outline:{ .hops-role-ico } Manage
{ .hops-role-cap }

- [On-demand transformations](on_demand_transformations.md)
  Compute features at request time from request parameters.
- [Notifications](notification.md)
  Emit change events to a Kafka topic.
- [Time to live](ttl.md)
  Expire rows after a retention period.
- [Deprecate](deprecation.md)
  Mark a group as retired without deleting it.

</div>

</div>
