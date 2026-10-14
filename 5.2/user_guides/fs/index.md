# Feature Store Guides

Feature pipelines write to feature groups, training and inference pipelines read through feature views.
The guides below follow that order: connect a source, write, validate, read, transform.

<!-- markdownlint-disable MD030 -->
<div class="grid cards hops-start" markdown>

-   :material-database-plus-outline:{ .lg .middle } **Start here**

    ---

    Create a feature group from a DataFrame and insert it.
    Everything else in this section builds on a feature group that exists.

    ```python
    fg = fs.get_or_create_feature_group(
        name="transactions",
        version=1,
        primary_key=["tid"],
        event_time="datetime",
        online_enabled=True,
    )
    fg.insert(df)
    ```

    [Create a feature group](feature_group/create.md) · [Create a feature view](feature_view/overview.md) · [Training data](feature_view/training-data.md)

</div>
<!-- markdownlint-enable MD030 -->

<div class="hops-task-index" markdown>

<div class="hops-task-group" markdown>
:material-database-import-outline:{ .hops-role-ico } Write
{ .hops-role-cap }

- [Data sources](data_source/index.md)
  Register warehouses, object stores and databases to read from and write to.
- [Feature groups](feature_group/index.md)
  Create, insert, evolve the schema, set time to live, deprecate.
- [External and spine groups](feature_group/create_external.md)
  Point at data that stays where it is, or supply keys and labels without storing them.
- [Ingest with dltHub](feature_group/ingest_with_dlthub.md)
  Load from hundreds of sources through dlt pipelines.

</div>

<div class="hops-task-group" markdown>
:material-check-decagram-outline:{ .hops-role-ico } Trust
{ .hops-role-cap }

- [Statistics](feature_group/statistics.md)
  Descriptive statistics on every insert, configurable per group.
- [Data validation](feature_group/data_validation.md)
  Great Expectations suites run on insert, with a policy on failure.
- [Feature monitoring](feature_monitoring/index.md)
  Scheduled statistics and drift detection against a reference window.
- [Notifications and observability](feature_group/notification.md)
  Change notifications and online ingestion status.

</div>

<div class="hops-task-group" markdown>
:material-database-export-outline:{ .hops-role-ico } Read
{ .hops-role-cap }

- [Feature views](feature_view/index.md)
  Select features across groups and read them the same way for training and inference.
- [Training data](feature_view/training-data.md)
  Materialise splits as files or read them straight into memory.
- [Batch and online reads](feature_view/batch-data.md)
  Batch inference data by time range, single vectors from the online store.
- [Feature server](feature_view/feature-server.md)
  Serve feature vectors over REST without the Python client.

</div>

<div class="hops-task-group" markdown>
:material-function-variant:{ .hops-role-ico } Transform and run
{ .hops-role-cap }

- [Transformation functions](transformation_functions.md)
  Model-independent functions applied on write, model-dependent on read.
- [Compute engines](compute_engines.md)
  Which operations run on Python, Spark or Flink.
- [Client integrations](../integrations/index.md)
  Databricks, SageMaker, EMR, Azure ML, Flink, Beam and more.
- [Vector similarity search](vector_similarity_search.md)
  Embeddings in a feature group, nearest-neighbour queries.

</div>

</div>
