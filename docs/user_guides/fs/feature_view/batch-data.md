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

## Extra filters

`get_batch_data` accepts an `extra_filter` argument that lets you apply an arbitrary filter on top of the feature view's own query filter and any training-dataset filter inherited from `init_batch_scoring`.
Filters are combined with `AND`, pushed down to the storage layer, and apply equally to `get_batch_data`, `get_batch_query`, and `get_batch_query_string`.

The simplest form uses a feature group handle to build the predicate:

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

The feature view's own query filter and any training-dataset filter from `init_batch_scoring` are AND-combined with `extra_filter` before the read.
This is the same parameter that [training-data extra filters](./training-data.md#extra-filters) exposes on training-data creation, so a filter expression works the same way in both APIs.

### Building filters from the feature view alone

When you do not have the feature group handle in scope (for example when reading a feature view in an inference script), use `feature_view.get_feature(name)` to obtain a `Feature` directly from the feature view's query.
The returned `Feature` supports the same comparison operators (`==`, `!=`, `<`, `<=`, `>`, `>=`) and helper methods (`.like`, `.isin`, `.contains`), so it slots into `extra_filter` the same way:

```python
df = feature_view.get_batch_data(
    extra_filter=(feature_view.get_feature("amount") > 100),
)
```

For feature views built from a join, `get_feature` accepts either the bare name or the prefixed name produced by the join.
Bare names resolve against the left feature group when more than one side has the column; the prefixed form forces resolution against the joined feature group:

```python
df = feature_view.get_batch_data(
    # `category` exists on both sides of the join — `sec_` selects the joined FG.
    extra_filter=(feature_view.get_feature("sec_category") == "A"),
)
```

If a bare name is ambiguous and no prefix is supplied, `get_feature` raises a `FeatureStoreException` listing the matching feature groups.

## Creation with transformation

If you have specified transformation functions when creating a feature view, you will get back transformed batch data as well.
If your transformation functions require statistics of training dataset, you must also provide the training data version. `init_batch_scoring` will then fetch the statistics and initialize the functions with required statistics.
Then you can follow the above examples and create the batch data.
Please note that transformed batch data can only be returned in the python client but not in the java client.

```python
feature_view.init_batch_scoring(training_dataset_version=1)
```

It is important to note that in addition to the filters defined in feature view, [extra filters](./training-data.md#extra-filters) will be applied if they are defined in the given training dataset version.

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
