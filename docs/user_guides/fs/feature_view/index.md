# Feature View User Guides

A feature view is a query over feature groups plus the metadata a model needs to read it consistently.
These guides cover creating one, reading training and inference data, and keeping the two aligned.

<!-- markdownlint-disable MD030 -->
<div class="grid cards hops-start" markdown>

-   :material-eye-plus-outline:{ .lg .middle } **Start here**

    ---

    Select features from one or more feature groups and save the selection as a feature view.

    ```python
    query = trans_fg.select_all().join(profile_fg.select(["age"]))
    fv = fs.get_or_create_feature_view(
        name="transactions_fraud",
        version=1,
        query=query,
        labels=["fraud_label"],
    )
    ```

    [Create a feature view](overview.md) · [Training data](training-data.md) · [Feature vectors](feature-vectors.md)

</div>
<!-- markdownlint-enable MD030 -->

<div class="hops-task-index" markdown>

<div class="hops-task-group" markdown>
:material-eye-plus-outline:{ .hops-role-ico } Create
{ .hops-role-cap }

- [Create a feature view](overview.md)
  Select, join, filter and label, then save a version.
- [Query](query.md)
  Joins, filters and point-in-time correctness.
- [Helper columns](helper-columns.md)
  Columns for training or inference logic that are not model inputs.
- [Spines](spine-query.md)
  Bring your own keys and labels at read time.
- [Model-dependent transformations](model-dependent-transformations.md)
  Scaling and encoding fitted on training data, applied on read.

</div>

<div class="hops-task-group" markdown>
:material-database-export-outline:{ .hops-role-ico } Read
{ .hops-role-cap }

- [Training data](training-data.md)
  Splits by ratio or time, materialised or in memory.
- [Batch data](batch-data.md)
  Inference data for a time range, with transformations applied.
- [Feature vectors](feature-vectors.md)
  Single or batched online lookups by serving key.
- [Feature server](feature-server.md)
  Online lookups over REST, without the Python client.

</div>

<div class="hops-task-group" markdown>
:material-monitor-eye:{ .hops-role-ico } Observe
{ .hops-role-cap }

- [Feature monitoring](feature_monitoring.md)
  Compare new data against a training dataset.
- [Feature logging](feature_logging.md)
  Log the features a model actually saw at inference.

</div>

</div>
