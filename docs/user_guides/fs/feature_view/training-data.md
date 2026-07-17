# Training data

Training data can be created from the feature view and used by different ML libraries for training different models.

You can read [training data concepts](../../../concepts/fs/feature_view/offline_api.md) for more details.
To see a full example of how to create training data, you can read [this notebook](https://github.com/logicalclocks/hopsworks-tutorials/blob/master/batch-ai-systems/fraud_batch/2_fraud_batch_training_pipeline.ipynb).

For Python-clients, handling small or moderately-sized data, we recommend enabling the [ArrowFlight Server with DuckDB](../../../setup_installation/common/arrow_flight_duckdb.md) service,
which will provide significant speedups over Spark/Hive for reading and creating in-memory training datasets.

## Creation

It can be created as in-memory DataFrames or materialised as `tfrecords`, `parquet`, `csv`, or `tsv` files to HopsFS or in all other locations, for example, S3, GCS.
If you materialise a training dataset, a `PySparkJob` will be launched.
By default, `create_training_data` waits for the job to finish.
However, you can run the job asynchronously by passing `write_options={"wait_for_job": False}`.
You can monitor the job status in the [jobs overview UI](../../projects/jobs/pyspark_job.md#step-1-jobs-overview).

```python
# create a training dataset as dataframe
feature_df, label_df = feature_view.training_data(
    description="transactions fraud batch training dataset",
)

# materialise a training dataset
version, job = feature_view.create_training_data(
    description="transactions fraud batch training dataset",
    data_format="csv",
    write_options={"wait_for_job": False},
)  # By default, it is materialised to HopsFS
print(job.id)  # get the job's id and view the job status in the UI
```

### Extra filters {#training-data-extra-filters}

Sometimes data scientists need to train different models using subsets of a dataset.
For example, there can be different models for different countries, seasons, and different groups.
One way is to create different feature views for training different models.
Another way is to add extra filters on top of the feature view when creating training data.

In the [transaction fraud example](https://github.com/logicalclocks/hopsworks-tutorials/blob/master/batch-ai-systems/fraud_batch/1_fraud_batch_feature_pipeline.ipynb), there are different transaction categories, for example: "Health/Beauty", "Restaurant/Cafeteria", "Holliday/Travel" etc.
Examples below show how to create training data for different transaction categories.

```python
# Create a training dataset for Health/Beauty
df_health = feature_view.training_data(
    description="transactions fraud batch training dataset for Health/Beauty",
    extra_filter=trans_fg.category == "Health/Beauty",
)
# Create a training dataset for Restaurant/Cafeteria and Holliday/Travel
df_restaurant_travel = feature_view.training_data(
    description="transactions fraud batch training dataset for Restaurant/Cafeteria and Holliday/Travel",
    extra_filter=trans_fg.category == "Restaurant/Cafeteria"
    and trans_fg.category == "Holliday/Travel",
)
```

### Lookback window for PIT joins {#training-data-lookback}

When training data is materialised from a Feature View that joins multiple Feature Groups, the PIT join scans every historical partition of the root and every joined Feature Group.
The `lookback` argument caps how far back the join is allowed to consider rows from the root and each joined Feature Group, so the engine can prune partitions before reading any files.
Apply the same window uniformly with `FeatureGroupLookback`, or use `Lookback` for per-Feature-Group control; the argument shape mirrors the one accepted by `get_batch_data` (see [the batch-data lookback section][batch-data-lookback]).

```python
import datetime
from hsfs.constructor.lookback import FeatureGroupLookback

version, job = feature_view.create_training_data(
    start_time=datetime.date(2026, 5, 10),
    end_time=datetime.date(2026, 5, 17),
    description="fraud batch training data, weekly partition pruning",
    lookback=FeatureGroupLookback(
        key="PARTITION_KEY",
        start=datetime.date(2026, 5, 10),
        end=datetime.date(2026, 5, 17),
    ),
)
```

Equivalent dict form (no `FeatureGroupLookback` import, but `datetime` is still required for the bound values):

```python
import datetime

version, job = feature_view.create_training_data(
    start_time=datetime.date(2026, 5, 10),
    end_time=datetime.date(2026, 5, 17),
    description="fraud batch training data, weekly partition pruning",
    lookback={
        "key": "PARTITION_KEY",
        "start": datetime.date(2026, 5, 10),
        "end": datetime.date(2026, 5, 17),
    },
)
```

For different lookbacks per joined Feature Group, pass a `Lookback` — see the [per-feature-group lookback section][batch-data-lookback] of the batch-data guide for the full shape.

The resolved window is persisted with the training dataset, so re-reading the same training dataset version reconstructs the same per-join predicate.
The same parameter is accepted by `create_train_test_split` and `create_train_validation_test_split`.

### Train/Validation/Test Splits

In most cases, ML practitioners want to slice a dataset into multiple splits, most commonly train-test splits or train-validation-test splits, so that they can train and test their models.
Feature view provides a sklearn-like API for this purpose, so it is very easy to create a training dataset with different splits.

Create a training dataset (as in-memory DataFrames) or materialise a training dataset with train and test splits.

```python
# create a training dataset
X_train, X_test, y_train, y_test = feature_view.train_test_split(test_size=0.2)

# materialise a training dataset
version, job = feature_view.create_train_test_split(
    test_size=0.2,
    description="transactions fraud batch training dataset",
    data_format="csv",
)
```

Create a training dataset (as in-memory DataFrames) or materialise a training dataset with train, validation, and test splits.

```python
# create a training dataset as DataFrame
X_train, X_val, X_test, y_train, y_val, y_test = (
    feature_view.train_validation_test_split(
        validation_size=0.3, test_size=0.2
    )
)

# materialise a training dataset
version, job = feature_view.create_train_validation_test_split(
    validation_size=0.3,
    test_size=0.2,
    description="transactions fraud batch training dataset",
    data_format="csv",
)
```

If the [ArrowFlight Server with DuckDB](../../../setup_installation/common/arrow_flight_duckdb.md) service is enabled,
and you want to create a particular in-memory training dataset with Hive instead, you can set `read_options={"use_hive": True}`.

```python
# create a training dataset as DataFrame with Hive
X_train, X_test, y_train, y_test = feature_view.train_test_split(
    test_size=0.2, read_options={"use_hive": True}
)
```

## Appending to a Training Dataset

A materialized training dataset can grow incrementally: `insert_training_data` appends a new batch of data to an existing training dataset version instead of rewriting it.
Only the new batch is computed and written, as a separate increment under the same version, so a large (multi-terabyte) training dataset can grow with, for example, a new daily batch, without rewriting the data already materialized.
The training dataset version and its metadata stay the same, and `get_training_data` returns all increments together by default.

The materialized data is partitioned by each row's UTC event date (a human-readable `YYYYMMDD` value), truncated to the `partition_precision` parameter — `day` by default, or `month`/`year` for coarser layouts with fewer partitions over long histories.
This makes the training dataset time-addressable: `get_training_data` can read just a time range, as shown in [Reading a time range](#reading-a-time-range-of-an-incremental-training-dataset).
All materializations of a training dataset version must use the same precision.
Because rows land in the day partitions they belong to, batches may be appended in any order: backfills and late-arriving events are supported.
Note that appends are not deduplicated — re-appending a batch that was already materialized adds its rows again, as with feature group inserts.

```python
# append yesterday's batch to training dataset version 1
job = feature_view.insert_training_data(
    training_dataset_version=1,
    start_time="2026-07-01 00:00:00",
    end_time="2026-07-01 23:59:59",
)
```

Passing `overwrite=True` rewrites the entire training dataset version for the given time range instead of appending.
From a Python client, the append is executed by the [ArrowFlight Server with DuckDB][arrowflight-server-with-duckdb] service if enabled, otherwise a `PySparkJob` is launched, as for `create_training_data`.

!!! note "Requirements and behavior"
    - Appending is only supported for the `parquet` data format.
    - Statistics are not recomputed on append by default, since that reads the whole dataset back every time. Pass `compute_statistics=True` to `insert_training_data` to refresh the descriptive statistics over all increments after the batch is written, or call `feature_view.compute_training_dataset_statistics(training_dataset_version)` explicitly when fresh statistics are needed, for example periodically or right before retraining.
    - Model-dependent transformation functions transform each appended batch with the statistics computed when the training dataset version was created, so all increments and serving stay consistent with each other. To refit those statistics, rebuild the version with `overwrite=True` or create a new training dataset version.
    - Randomly split training datasets are appended per split: each batch is re-split (for example 80/20), which stays sound over many appends.
    - Appending to a time-series-split training dataset is not supported and raises an error: the batch would land entirely in the last split (for example, test) while the earlier splits stay frozen, skewing the dataset. For time-series data, grow an unsplit training dataset and derive the train and test sets at read time instead, as shown in [Reading a time range](#reading-a-time-range-of-an-incremental-training-dataset).
    - Training datasets materialized with an older Hopsworks version are not appendable; recreate the training dataset once, after which it can be appended to.

### Reading a time range of an incremental training dataset

The materialized data is stored in Hive partitions keyed by each row's UTC event date, truncated to the dataset's partition precision, so `get_training_data` can read only the rows whose event date falls inside a given range, without scanning the rest of the data.
This replaces materialized time-series splits for growing datasets: the train/test boundary is chosen at read time, so both windows grow or shift automatically as new batches arrive — for example, a sliding training window after detecting model drift, or a test set that is always the most recent 30 days.

```python
# train on everything up to 30 days ago
X_train, y_train = feature_view.get_training_data(
    training_dataset_version=1,
    end_time="2026-06-01",
)

# test on the most recent 30 days
X_test, y_test = feature_view.get_training_data(
    training_dataset_version=1,
    start_time="2026-06-02",
)
```

!!! note "Range semantics"
    - Both bounds are inclusive and select whole partitions by the rows' UTC event date at the dataset's partition precision; finer bounds do not filter rows within a partition, so align the bounds with the precision (day boundaries for `day`, month boundaries for `month`, and so on).
    - Only data materialized with an event time can be matched by a time range; if the feature view's left feature group defines no event-time column, the dataset stays appendable but cannot be read by time range.

## Read Training Data

Once you have created a training dataset, all its metadata are saved in Hopsworks.
This enables you to reproduce exactly the same dataset at a later point in time.
This holds for training data as both DataFrames or files.
That is, you can delete the training data files (for example, to reduce storage costs), but still reproduce the training data files later on if you need to.

```python
# get a training dataset
feature_df, label_df = feature_view.get_training_data(
    training_dataset_version=1
)

# get a training dataset with train and test splits
X_train, X_test, y_train, y_test = feature_view.get_train_test_split(
    training_dataset_version=1
)

# get a training dataset with train, validation and test splits
X_train, X_val, X_test, y_train, y_val, y_test = (
    feature_view.get_train_validation_test_split(training_dataset_version=1)
)
```

For an incrementally grown training dataset, `get_training_data` also accepts `start_time`/`end_time` to read only a time range of increments — see [Reading a time range](#reading-a-time-range-of-an-incremental-training-dataset).

## Passing Context Variables to Transformation Functions

Once you have [defined a transformation function using a context variable](../transformation_functions.md#passing-context-variables-to-transformation-function), you can pass the required context variables using the `transformation_context` parameter when generating IN-MEMORY training data or materializing a training dataset.

!!! note
    Passing context variables for materializing a training dataset is only supported in the PySpark Kernel.

!!! example "Passing context variables while creating training data."
    === "Python"

        ```python
        # Passing context variable to IN-MEMORY Training Dataset.
        X_train, X_test, y_train, y_test = feature_view.get_train_test_split(
            training_dataset_version=1,
            primary_key=True,
            event_time=True,
            transformation_context={"context_parameter": 10},
        )

        # Passing context variable to Materialized Training Dataset.
        version, job = feature_view.get_train_test_split(
            training_dataset_version=1,
            primary_key=True,
            event_time=True,
            transformation_context={"context_parameter": 10},
        )
        ```

## Read training data with primary key(s) and event time

For certain use cases, e.g., time series models, the input data needs to be sorted according to the primary key(s) and event time combination.
Primary key(s) and event time are not usually included in the feature view query as they are not features used for training.
To retrieve the primary key(s) and/or event time when retrieving training data, you need to set the parameters `primary_key=True` and/or `event_time=True`.

```python
# get a training dataset
X_train, X_test, y_train, y_test = feature_view.get_train_test_split(
    training_dataset_version=1,
    primary_key=True,
    event_time=True,
)
```

!!! note
    All primary and event time columns of all the feature groups included in the feature view will be returned.
    If they have the same names across feature groups and the join prefix was not provided then reading operation will fail with ambiguous column exception.
    Make sure to define the join prefix if primary key and event time columns have the same names across feature groups.

    To use primary key(s) and event time column with materialized training datasets it needs to be created with `primary_key=True` and/or `with_event_time=True`.

## Deletion

To clean up unused training data, you can delete all training data or for a particular version.
Note that all metadata of training data and materialised files stored in HopsFS will be deleted and cannot be recreated anymore.

```python
# delete a training data version
feature_view.delete_training_dataset(training_dataset_version=1)

# delete all training datasets
feature_view.delete_all_training_datasets()
```

It is also possible to keep the metadata and delete only the materialised files.
Then you can recreate the deleted files by just specifying a version, and you get back the exact same dataset again.
This is useful when you are running out of storage.

```python
# delete files of a training data version
feature_view.purge_training_data(training_dataset_version=1)

# delete files of all training datasets
feature_view.purge_all_training_data()
```

To recreate a training dataset:

```python
feature_view.recreate_training_dataset(training_dataset_version=1)
```

## Tags

Similar to feature view, You can attach, get, and remove tags.
You can learn more in [Tags Guide](../tags/tags.md).

```python
# attach
feature_view.add_training_dataset_tag(
    training_dataset_version=1, name="tag_schema", value={"key": "value"}
)

# get
feature_view.get_training_dataset_tag(
    training_dataset_version=1, name="tag_schema"
)

# remove
feature_view.delete_training_dataset_tag(
    training_dataset_version=1, name="tag_schema"
)
```

## Next

Once you have created a training dataset and trained your model, you can deploy your model in a "batch"  or "online" setting.
Next, you can learn how to create [batch data](./batch-data.md) and get [feature vectors](./feature-vectors.md).
