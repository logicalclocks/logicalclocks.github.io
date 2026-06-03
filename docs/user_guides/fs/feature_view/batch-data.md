# Batch data (analytical ML systems)

## Creation

It is very common that ML models are deployed in a "batch" setting where ML pipelines score incoming new data at a regular interval, for example, daily or weekly.
Feature views support batch prediction by returning batch data as a DataFrame over a time range, by `start_time` and `end_time`.
The resultant DataFrame (or batch-scoring DataFrame) can then be fed to models to make predictions.

=== "Python"

    ```python
    # get batch data
    df = feature_view.get_batch_data(
        start_time="20220620", end_time="20220627"
    )  # return a dataframe
    ```

=== "Java"

    ```java
    Dataset<Row> ds = featureView.getBatchData("20220620", "20220627")
    ```

## Retrieve batch data with primary keys and event time

For certain use cases, e.g., time series models, the input data needs to be sorted according to the primary key(s) and event time combination.
Or one might want to merge predictions back with the original input data for postmortem analysis.
Primary key(s) and event time are not usually included in the feature view query as they are not features used for training.
To retrieve the primary key(s) and/or event time when retrieving batch data for inference, you need to set the parameters `primary_key=True` and/or `event_time=True`.

=== "Python"

    ```python
    # get batch data
    df = feature_view.get_batch_data(
        start_time="20220620",
        end_time="20220627",
        primary_key=True,
        event_time=True,
    )  # return a dataframe with primary keys and event time
    ```
!!! note
    All primary and event time columns of all the feature groups included in the feature view will be returned.
    If they have the same names across feature groups and the join prefix was not provided then reading operation will fail with ambiguous column exception.
    Make sure to define the join prefix if primary key and event time columns have the same names across feature groups.

For Python-clients, handling small or moderately-sized data, we recommend enabling the [ArrowFlight Server with DuckDB](../../../setup_installation/common/arrow_flight_duckdb.md), which will provide significant speedups over Spark/Hive for reading batch data.
If the service is enabled, and you want to read this particular batch data with Hive instead, you can set the read_options to `{"use_hive": True}`.

```python
# get batch data with Hive
df = feature_view.get_batch_data(
    start_time="20220620", end_time="20220627", read_options={"use_hive": True}
)
```

## Extra filters {#batch-data-extra-filters}

`get_batch_data` accepts an `extra_filter` argument that lets you apply an arbitrary filter on top of the Feature View's own query filter and any training-dataset filter inherited from `init_batch_scoring`.
Filters are combined with `AND`, pushed down to the storage layer, and apply equally to `get_batch_data`, `get_batch_query`, and `get_batch_query_string`.

The simplest form uses a Feature Group handle to build the predicate:

```python
df = feature_view.get_batch_data(
    start_time="20220620",
    end_time="20220627",
    extra_filter=(trans_fg.category == "Health/Beauty"),
)
```

Combine multiple predicates with `&` (AND) and `|` (OR):

```python
df = feature_view.get_batch_data(
    extra_filter=(trans_fg.amount > 100) & (trans_fg.country.isin(["SE", "NO"])),
)
```

The Feature View's own query filter and any training-dataset filter from `init_batch_scoring` are AND-combined with `extra_filter` before the read.
This is the same parameter that [training-data extra filters][training-data-extra-filters] exposes on training-data creation, so a filter expression works the same way in both APIs.

### Building filters from the Feature View alone

When you do not have the Feature Group handle in scope (for example when reading a Feature View in an inference script), use `feature_view.get_feature(name)` to obtain a `Feature` directly from the Feature View's query.
The returned `Feature` supports the same comparison operators (`==`, `!=`, `<`, `<=`, `>`, `>=`) and helper methods (`.like`, `.isin`, `.contains`), so it slots into `extra_filter` the same way:

```python
df = feature_view.get_batch_data(
    extra_filter=(feature_view.get_feature("amount") > 100),
)
```

For Feature Views built from a join, `get_feature` accepts either the bare name or the prefixed name produced by the join.
Bare names resolve against the left Feature Group when more than one side has the column; the prefixed form forces resolution against the joined Feature Group:

```python
df = feature_view.get_batch_data(
    # `category` exists on both sides of the join — `sec_` selects the joined FG.
    extra_filter=(feature_view.get_feature("sec_category") == "A"),
)
```

If a bare name is ambiguous and no prefix is supplied, `get_feature` raises a `FeatureStoreException` listing the matching Feature Groups.

## Lookback window for PIT joins {#batch-data-lookback}

Point-in-time (PIT) joins use the condition `feature_fg.event_time <= root_fg.event_time` to pick the latest matching record from each joined Feature Group.
That predicate is a range comparison, not an equality, so partition pruning is defeated and every historical partition of every joined Feature Group is scanned on every read.
As Feature Groups grow with daily ingestion, this scan grows unboundedly.

The `lookback` argument lets you cap how far back the join is allowed to consider rows from each joined Feature Group.
Hopsworks turns the window into a constant-bound predicate on the joined Feature Group so the ArrowFlight Server with DuckDB and Spark Catalyst pushdown can prune partitions before opening any files.

### Uniform lookback

Apply the same window to every joined Feature Group with a `FeatureGroupLookback` instance from `hsfs.constructor.lookback`, or the equivalent dict.
Both forms accept `date` and `datetime` values.

```python
import datetime
from hsfs.constructor.lookback import FeatureGroupLookback

df = feature_view.get_batch_data(
    start_time=datetime.date(2026, 5, 10),
    end_time=datetime.date(2026, 5, 17),
    lookback=FeatureGroupLookback(
        key="PARTITION_KEY",
        start=datetime.date(2026, 5, 10),
        end=datetime.date(2026, 5, 17),
    ),
)
```

Equivalent dict form, no `FeatureGroupLookback` import required (you still need `datetime` for the bound values):

```python
import datetime

df = feature_view.get_batch_data(
    start_time=datetime.date(2026, 5, 10),
    end_time=datetime.date(2026, 5, 17),
    lookback={
        "key": "PARTITION_KEY",
        "start": datetime.date(2026, 5, 10),
        "end": datetime.date(2026, 5, 17),
    },
)
```

`key` selects which column the predicate is emitted against.
`"PARTITION_KEY"` targets the Feature Group's partition column so the engine can prune partitions before reading files; the Feature Group must have a single DATE partition column.
`"EVENT_TIME"` targets the Feature Group's `event_time` column and guarantees row-level correctness but offers only engine-dependent file pruning (Hudi or Delta column-stats indexing).

`start` is required and emits a `>=` predicate.
`end` is optional and emits a `<=` predicate when present.
When `end` is omitted, only the lower bound is emitted, making the short form below valid: the root Feature Group and every joined Feature Group get `<partition_column> >= '2026-05-10'` (where `<partition_column>` is each Feature Group's own DATE partition column) and nothing else.

```python
import datetime

df = feature_view.get_batch_data(
    lookback={
        "key": "PARTITION_KEY",
        "start": datetime.date(2026, 5, 10),
    },
)
```

### Per-feature-group lookback

When different Feature Groups need different windows, use `Lookback` to bind a `FeatureGroupLookback` to specific joined Feature Groups.
An optional `default` applies to every Feature Group not listed in `feature_group_lookbacks`.

```python
import datetime
from hsfs.constructor.lookback import FeatureGroupLookback, Lookback

df = feature_view.get_batch_data(
    start_time=datetime.date(2026, 5, 11),
    end_time=datetime.date(2026, 5, 17),
    lookback=Lookback(
        default=FeatureGroupLookback(
            key="PARTITION_KEY",
            start=datetime.date(2026, 5, 5),
            end=datetime.date(2026, 5, 17),
        ),
        feature_group_lookbacks={
            "transactions": FeatureGroupLookback(
                key="EVENT_TIME",
                start=datetime.datetime(2026, 5, 1, tzinfo=datetime.timezone.utc),
            ),
        },
    ),
)
```

Skip the `default` to apply lookbacks only to the listed Feature Groups; unlisted Feature Groups receive no lookback for that call.

```python
df = feature_view.get_batch_data(
    start_time=datetime.date(2026, 5, 11),
    end_time=datetime.date(2026, 5, 17),
    lookback=Lookback(
        feature_group_lookbacks={
            "transactions": FeatureGroupLookback(
                key="PARTITION_KEY", start=datetime.date(2026, 5, 5)
            ),
        }
    ),
)
```

`feature_group_lookbacks` keys identify a Feature Group in one of two ways: by name (a bare string matches every version of the named Feature Group at any join site in the Feature View) or by passing the Feature Group instance itself (matches the exact `(name, version)` so a specific version can be targeted when multiple versions of the same Feature Group are joined).
When both forms are supplied for the same name, the instance entry wins at its specific join site and the bare-string entry still applies elsewhere.

Equivalent dict form:

```python
import datetime

df = feature_view.get_batch_data(
    start_time=datetime.date(2026, 5, 11),
    end_time=datetime.date(2026, 5, 17),
    lookback={
        "default": {
            "key": "PARTITION_KEY",
            "start": datetime.date(2026, 5, 5),
            "end": datetime.date(2026, 5, 17),
        },
        "feature_group_lookbacks": {
            "transactions": {
                "key": "EVENT_TIME",
                "start": datetime.datetime(2026, 5, 1, tzinfo=datetime.timezone.utc),
            },
        },
    },
)
```

### Combining `lookback` with other filters

The `lookback` predicate combines with filters declared on the Query, but where the filter is attached changes whether the engine can prune partitions on the root Feature Group.

Filters attached to a sub-query (`fg.select(...).filter(...)`) always prune on that Feature Group regardless of which Feature Group they reference.
Filters attached to the outer query (`query.filter(...)` after the join, or `extra_filter` on `get_batch_data`) prune the root only when every referenced feature belongs to the root Feature Group.
A mixed-Feature-Group outer filter still produces correct results — the predicates apply at the outer level — but the root's partitions are no longer pruned at file-listing time.

```python
# Root sub-query filter — lookback prunes both root and joined Feature Groups.
query = root.select_all().filter(root.amount > 100).join(dim.select_all())

# Joined sub-query filter — lookback still prunes both sides.
query = root.select_all().join(dim.select_all().filter(dim.category == "X"))

# Outer filter referencing a joined Feature Group — root pruning is lost;
# joined Feature Groups still prune via their own predicates.
query = root.select_all().join(dim.select_all()).filter(dim.category == "X")
```

For best pruning, keep call-site filters at the sub-query level when their predicate references only one Feature Group.

The same `lookback` argument is supported on `create_training_data` (see [the training-data section][training-data-lookback]).
Both `extra_filter` and `lookback` can be combined.

## Creation with transformation

If you have specified transformation functions when creating a feature view, you will get back transformed batch data as well.
If your transformation functions require statistics of training dataset, you must also provide the training data version. `init_batch_scoring` will then fetch the statistics and initialize the functions with required statistics.
Then you can follow the above examples and create the batch data.
Please note that transformed batch data can only be returned in the python client but not in the java client.

```python
feature_view.init_batch_scoring(training_dataset_version=1)
```

It is important to note that in addition to the filters defined in Feature View, [extra filters][training-data-extra-filters] will be applied if they are defined in the given training dataset version.

## Retrieving untransformed batch data

By default, the `get_batch_data` function returns batch data with model-dependent transformations applied.
However, you can retrieve untransformed batch data—while still including on-demand features—by setting the `transform` parameter to `False`.

!!! example "Returning untransformed batch data"
    === "Python"

        ```python
        # Fetching untransformed batch data.
        untransformed_batch_data = feature_view.get_batch_data(transform=False)
        ```

## Passing Context Variables to Transformation Functions

After [defining a transformation function using a context variable](../transformation_functions.md#passing-context-variables-to-transformation-function), you can pass the necessary context variables through the `transformation_context` parameter when fetching batch data.

!!! example "Passing context variables while fetching batch data."
    === "Python"

        ```python
        # Passing context variable to IN-MEMORY Training Dataset.
        batch_data = feature_view.get_batch_data(
            transformation_context={"context_parameter": 10}
        )
        ```
