# 3.0 Migration Guide

## Breaking Changes

### Feature View

Feature View is a new core abstraction introduced in version 3.0. The Feature View extends and replaces the old Training Dataset. Feature views are now the gateway for users to access feature data from the feature store.

=== "Pre-3.0"
    ```python
    td = fs.create_training_dataset()
    ```

=== "3.0"
    First create the feature view using a Query object:
    ```python
    fv = fs.create_feature_view()
    ```

    You can then create training data from the feature view by writing it as new files with `.create_` methods:
    ```python
    td_df = fv.create_training_data()
    fv.create_train_test_split()
    fv.create_train_validation_test_split()
    ```

    Or you can directly create the training data in memory by below methods:
    ```python
    fv.training_data()
    fv.train_test_split()
    fv.train_validation_test_split()
    ```

This means that the process for generating training data changes slightly and training data is grouped by feature views.
This has the following advantages:

1. It will be easier to create new versions of training data for re-training of models in the future.
2. You do not have to keep references to training data in your model serving code, instead you use the Feature View object.
3. The feature view offers the same interface for retrieving batch data for batch scoring, so you don’t have to execute SQL against the feature store explicitly anymore.

A feature view uses the Query abstraction to define the schema of the view, and therefore, the Query is a mandatory argument, this effectively removes the possibility to create a training dataset directly from a Spark Dataframe.

#### Required changes
After the upgrade all existing training datasets will be located under a Feature View with the same name. The versions of the training datasets stay untouched. You can use `feature_view.get_training_data` to get back existing training datasets. Except that training datasets created directly from Spark Dataframe are not migrated to feature view. In this case, you can use the old APIs for retrieving these training datasets, so that your existing training pipelines are still functional. 

However, if you have any pipelines, that automatically create training datasets, you will have to adjust these to the above workflow. `fs.create_training_dataset()` has been removed.

To learn more about the new Feature View, have a look at the dedicated [concept](../../concepts/fs/feature_view/fv_overview.md) and [guide](../fs/feature_view/overview.md) section in the documentation.

### Deequ-based Data Validation in favour of Great Expectations
Unfortunately, the [Deequ data validation library](https://github.com/awslabs/deequ) is no longer actively maintained which makes it impossible for us to maintain the functionality within Hopsworks. Therefore, we are dropping the entire support for Deequ as validation engine in Hopsworks 3.0 in favour of [Great Expectations](https://greatexpectations.io/) (GE).

This has the following advantages:

1. Great Expectations has become the defacto standard for data validation within the community.
2. Hopsworks is fully compatible with GE native objects, that means you can bring your existing expectation suites without the need for rewriting them.
3. GE is both available for Spark and for Pandas Dataframes, whereas Deequ was only supporting Spark.

#### Required changes
All APIs regarding data validation have been redesigned to accommodate the functionality of GE. This means that you will have to redesign your previous expectations in the form of GE expectation suites that you can attach to Feature Groups. Please refer to the [data validation guide](../fs/feature_group/data_validation.md) for a full specification of the functionality.

#### Limitations
GE is a Python library and therefore we can support synchronous data validation only in Python and PySpark kernels and not on Java/Scala Spark kernels. However, you have the possibility to launch a job asynchronously after writing with Java/Scala in order to perform data validation.

## Deprecated Features

These changes or new features introduce changes in APIs which might break your pipelines in the future. We try to keep old APIs around until the next major release in order to give you some time to adapt your pipelines, however, this is not always possible, and these methods might be removed in any upcoming release, so we recommend addressing these changes as soon as possible. For this reason, we list some of the changes as breaking change, even though they are still backwards compatible.

### On-Demand Feature Groups are now called External Feature Groups

Most data engineers but also many data scientists have a background where they at least partially where exposed to database terminology. Therefore, we decided to rename On-Demand Feature Groups to simply External Feature Groups. We think this makes the abstraction clearer, as practitioners are usually familiar with the concept of External Tables in a database.

This lead to a change in HSFS APIs:

=== "Pre-3.0"
    ```python
    fs.create_on_demand_feature_group()
    fs.get_on_demand_feature_group()
    fs.get_on_demand_feature_groups()
    ```

=== "3.0"
    ```python
    fs.create_external_feature_group()
    fs.get_external_feature_group()
    fs.get_external_feature_groups()
    ```

Note, pre-3.0 methods are marked as deprecated and still available in the library for backwards compatibility.

### Streaming API for writing becomes the Python Default

Hopsworks provides [three write APIs](../../concepts/fs/feature_group/write_apis.md) to the Feature Store to accommodate the different use cases:

1. **Batch Write:** This was the default mode prior to version 3.0. It involves writing a DataFrame in batch either to the offline feature store, or the online one, or both. This mode is still the default when you are writing Spark DataFrames on Hopsworks.
2. **External connectors:** This mode allows users to mount external tables existing in DataWarehouses like Snowflake, Redshift and BigQuery as feature groups in Hopsworks. In this case the data is not moved and remains on the external data storage.
3. **Stream Write:** This mode was introduced in version 2.0 and expanded in version 3.0. This mode has a "Kappa-style" architecture, where the DataFrame gets streamed into a Kafka topic and, as explained later in the post, the data is picked up from Kafka by Hopsworks and written into the desired stores. In Hopsworks 3.0 this is the default mode for Python clients.

With 3.0 the stream API becomes the default for Feature Groups created from pure Python environments with Pandas Dataframes.

This has the following advantages:

1. **Reduced write amplification:** Instead of uploading data to Hopsworks and subsequently starting a Spark job to upsert the data on offline storage and writing it to Kafka for the online storage upsert, the data is directly written to Kafka and from there it’s being upserted directly to offline and/or online.

2. **Fresher features:** Since new data gets written to Kafka directly without prior upload, the data ends up in the online feature store with subsecond latency, which is a massive improvement given it is written from Python without any Streaming framework.

3. **Batching of offline upserts:** You can control now yourself how often the Spark application that performs the upsert on the offline feature store is running. Either you run it synchronously with every new Dataframe ingestion, or you batch multiple Dataframes by launching the job less regularly.

#### Required changes
Your existing feature groups will not be affected by this change, that means all existing feature groups will continue to use the old upload path for ingestion. However, we strongly recommend creating new versions of your existing feature groups that use ingest to using Python, in order to leverage the above advantages.

### Built-in transformation functions don’t have to be registered explicitly for every project
In Hopsworks 2.5 users had to register the built-in transformation functions (min-max scaler, standard scaler, label encoder and robust scaler) explicitly for every project by calling `fs.register_builtin_transformation_functions()`. This is no longer necessary, as all new projects will have the functions registered by default.

### Hive installation extra deprecated in favour of Python extra
In the past when using HSFS in pure Python environments without PySpark, users had to install the hive extra when installing the PyPi package. This extra got deprecated and users now have to install an extra called python to reflect the environment:

=== "Pre-3.0"
    ```bash
    pip install hsfs[hive]
    ```

=== "3.0"
    ```bash
    pip install hsfs[python]
    ```

### More restrictive feature types
With Hopsworks 3.0 we made feature types more strict and therefore made ingestion pipelines more robust. Both Spark and Pandas are quite forgiving when it comes to types, which often led to schema incompatibilities when ingesting to a feature group.

In this release we narrowed down the allowed Python types, and defined a clear mapping to Spark and Online Feature Store types. Please refer to the [feature type guide](../fs/feature_group/data_types.md) in the documentation for the exact mapping.

#### Required Changes
The most common Python/Pandas types are still supported, we recommend you double check your feature groups with the type mapping above.

### Deprecation of .save methods in favour of .insert together with .get_or_create_
The `.save()` methods to create feature store entities has been deprecated in favour of `.insert()`. That means if there is no metadata for an entity in the feature store, a call to `.insert()` will create it.

Together with the new `.get_or_create_ APIs` this will avoid that users have to change their code between creating entities and deploying the same code into production.

=== "Pre-3.0"
    ```bash
    try:
        fg = fs.get_feature_group(...)
        fg.insert(df)
    except RESTError as e:
        fg = fs.create_feature_group(...)
        fg.save(df)
    ```

=== "3.0"
    ```bash
    fg = fs.get_or_create_feature_group(...)
    fg.insert(df)
    ```

### hops python library superseded by Hopsworks library

The [hops](https://pypi.org/project/hops/) python library is now deprecated and is superseded by the [hopsworks](https://pypi.org/project/hopsworks/) python library. `hopsworks` is essentially a reimplementation of `hops`, but with an object-oriented API, similar in style with [hsfs](https://pypi.org/project/hsfs/). For guides on how to use the API follow the [Projects guides](../../user_guides/projects/index.md).

Furthermore, the functionality provided by the `model` and `serving` module in `hops`, is now ported to the [hsml](https://pypi.org/project/hsml/) python library. To create models and serving follow the [MLOps guides](../../user_guides/mlops/index.md).

## New Feature Highlights

This list is meant to serve as a starting point to explore the new features of the Hopsworks 3.0 release, which can significantly improve your workflows.

### Added new Data Sources: GCS, BigQuery and Kafka
With the added support for Google Cloud, we added also two new [data sources](../fs/data_sources/index.md): [Google Cloud Storage](../fs/data_sources/creation/gcs.md) and [Google BigQuery](../fs/data_sources/creation/bigquery.md). Users can use these connectors to create external feature groups or write out training data.

Additionally, to make it easier for users to get started with Spark Streaming applications, we added a [Kafka connector](../fs/data_sources/creation/kafka.md), which let’s you easily read a Kafka topic into a Spark Streaming Dataframe.

### Optimized Default Hudi Options
By default, Hudi tends to over-partition input, and therefore the layout of Feature Groups. The default parallelism is 200, to ensure each Spark partition stays within the 2GB limit for inputs up to 500GB. The new default is the following for all insert/upsert operations:

```python
extra_write_options = {
  'hoodie.bulkinsert.shuffle.parallelism': '5',
  'hoodie.insert.shuffle.parallelism': '5',
  'hoodie.upsert.shuffle.parallelism': '5'
}
```

In most of the cases, you will not have to change this default. For very large inputs you should bump this up accordingly, by passing it to the `write_options` argument of the Feature Group `.insert()` method:

```python
fg.insert(df, write_options=extra_write_options)
```

We recommend having shuffle parallelism `hoodie.[insert|upsert|bulkinsert].shuffle.parallelism` such that its at least input_data_size/500MB.

### Feature View passed features
With the introduction of the [Feature View abstraction](../../concepts/fs/feature_view/fv_overview.md), we added APIs to allow users to overwrite features with so-called [passed features](../fs/feature_view/feature-vectors.md#passed-features) when calling `fv.get_feature_vector()`:

```python
# get a single vector
feature_view.get_feature_vector(
    entry = {"pk1": 1, "pk2": 2},
    passed_features = {"feature_a": "value_a"}
)
# get multiple vectors
feature_view.get_feature_vectors(
    entry = [
        {"pk1": 1, "pk2": 2},
        {"pk1": 3, "pk2": 4},
        {"pk1": 5, "pk2": 6}
    ],
    passed_features = [
        {"feature_a": "value_a"},
        {"feature_a": "value_b"},
        {"feature_a": "value_c"},
    ]
)
```

This is useful, if some of the features values are only known at prediction time and cannot be computed and cached in the online feature store, you can provide those values as `passed_features` option. The `get_feature_vector` method is going to use the passed values to construct the final feature vector to submit to the model, it will also apply any transformations to the passed features attached to the respective features.

### Reading Training Data directly from HopsFS in Python environments

In Hopsworks 3.0 we added support for [reading training data](../fs/feature_view/training-data.md#read-training-data) from Hopsworks directly into external Python environments. Previously, users had to write the training data to external storage like S3 in order to access it from external environment.
