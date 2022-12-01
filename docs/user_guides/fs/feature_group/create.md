# How to create a Feature Group 

### Introduction

In this guide you will learn how to create and register a feature group with Hopsworks. This guide covers creating a feature group using the HSFS APIs as well as the user interface.

## Prerequisites

Before you begin this guide we suggest you read the [Feature Group](../../../concepts/fs/feature_group/fg_overview.md) concept page to understand what a feature group is and how it fits in the ML pipeline.

## Create using the HSFS APIs

To create a feature group using the HSFS APIs, you need to provide a Pandas or Spark DataFrame. The DataFrame will contain all the features you want to register within the feature group, as well as the primary key, event time and partition key.

### Create a Feature Group 

The first step to create a feature group is to create the API metadata object representing a feature group. Using the HSFS API you can execute:

#### Streaming Write API

=== "Python"

    ```python
    fg = feature_store.create_feature_group(name="weather",
        version=1,
        description="Weather Features",
        online_enabled=True,
        primary_key=['location_id'],
        partition_key=['day'],
        event_time='event_time'
    )
    ```

=== "PySpark"

    ```python
    fg = feature_store.create_feature_group(name="weather",
        version=1,
        description="Weather Features",
        online_enabled=True,
        primary_key=['location_id'],
        partition_key=['day'],
        event_time='event_time',
        stream=True
    )
    ```

#### Batch Write API

=== "PySpark"

    ```python
    fg = feature_store.create_feature_group(name="weather",
        version=1,
        description="Weather Features",
        online_enabled=True,
        primary_key=['location_id'],
        partition_key=['day'],
        event_time='event_time',
    )
    ```

The full method documentation is available [here](https://docs.hopsworks.ai/feature-store-api/{{{ hopsworks_version }}}/generated/api/feature_group_api/#featuregroup). `name` is the only mandatory parameter of the `create_feature_group` and represents the name of the feature group. 

In the example above we created the first version of a feature group named *weather*, we provide a description to make it searchable to the other project members, as well as making the feature group available online. 

Additionally we specify which columns of the DataFrame will be used as primary key, partition key and event time. Composite primary key and multi level partitioning is also supported. 

The version number is optional, if you don't specify the version number the APIs will create a new version by default with a version number equals to the highest existing version number plus one. 

The last parameter used in the examples above is `stream`. The `stream` parameter controls whether to enable the streaming write APIs to the online and offline feature store. When using the APIs in a Python environment this behavior is the default and it requires the time travel format to be set to 'HUDI'.  

##### Primary key

A primary key is required when using the default Hudi file format to store offline feature data. When inserting data in a feature group on the offline feature store, the DataFrame you are writing is checked against the existing data in the feature group. If a row with the same primary key is found in the feature group, the row will be updated. If the primary key is not found, the row is appended to the feature group.
When writing data on the online feature store, existing rows with the same primary key will be overwritten by new rows with the same primary key.

##### Event time

The event time column represent the time at which the event was generated. For example, with transaction data, the event time is the time at which a given transaction was made. 

The event time is added to the primary key when writing to the offline feature store. This will make sure that the offline feature store has the entire history. As an example, if a user has done multiple purchases on a website, the event time being part of the primary key, will ensure that all the purchases for each user (user_id) will be saved in the feature group.

The event time **is not** part of the primary key when writing to the online feature store. This will ensure that the online feature store has the most recent version of the feature vector for each primary key.

##### Partition key

It is best practice to add a partition key. When you specify a partition key, the data in the feature group will be stored under multiple directories based on the value of the partition column(s).
All the rows with a given value as partition key will be stored in the same directory. 

Choosing the correct partition key has significant impact on the query performance as the execution engine (Spark) will be able to skip listing and reading files belonging to partitions which are not included in the query. 
As an example, if you have partitioned your feature group by day and you are creating a training dataset that includes only the last year of data, Spark will read only 365 partitions and not the entire history of data.
On the other hand, if the partition key is too fine grained (e.g. timestamp at millisecond resolution) - a large number of small partitions will be generated. This will slow down query execution as Spark will need to list and read a large amount of small directories/files.

If you do not provide a partition key, all the feature data will be stored as files in a single directory.
The system has a limit of 10240 direct children (files or other subdirectories) per directory. This means that, as you add new data to a non-partitioned feature group, new files will be created and you might reach the limit. If you do reach the limit, your feature engineering pipeline will fail with the following error:

```sh
MaxDirectoryItemsExceededException - The directory item limit is exceeded: limit=10240 items=10240
```

By using partitioning the system will write the feature data in different subdirectories, thus allowing you to write 10240 files per partition.

### Register the metadata and save the feature data

The snippet above only created the metadata object on the Python interpreter running the code. To register the feature group metadata and to save the feature data with Hopsworks, you should invoke the `save` method:

```python 
fg.save(df)
```

The save method takes in input a Pandas or Spark DataFrame. HSFS will use the DataFrame columns and types to determine the name and types of features, primary key, partition key and event time. 

The DataFrame *must* contain the columns specified as primary keys, partition key and event time in the `create_feature_group` call.

If a feature group is online enabled, the `save` method will store the feature data to both the online and offline storage.

### API Reference 

[FeatureGroup](https://docs.hopsworks.ai/feature-store-api/{{{ hopsworks_version }}}/generated/api/feature_group_api/#featuregroup)

## Create using the UI

You can also create a new feature group through the UI. For this, navigate to the `Feature Groups` section and press the `Create` button at the top-right corner.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/feature_group/no_feature_group_list.png" alt="List of Feature Groups">
  </figure>
</p>

Subsequently, you will be able to define its properties (such as name, mode, features, storage connector, and more) and finish by clicking `Create New Feature Group` at the bottom of the page.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/feature_group/create_feature_group.png" alt="Create new Feature Group">
  </figure>
</p>
