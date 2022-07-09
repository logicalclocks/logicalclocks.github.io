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

The full method documentation is available [here](https://docs.hopsworks.ai/feature-store-api/dev/generated/api/feature_group_api/#featuregroup). `name` is the only mandatory parameter of the `create_feature_group` and represents the name of the feature group. 

In the example above we created the first version of a feature group named *weather*, we provide a description to make it searchable to the other project members, as well as making the feature group available online. 

Additionally we specify which columns of the DataFrame will be used as primary key, partition key and event time. Composite primary key and multi level partitioning is also supported. 

The version number is optional, if you don't specify the version number the APIs will create a new version by default with a version number equals to the the highest existing version number plus one. 

The last parameter used in the examples above is `stream`. The `stream` parameter controls whether to enable the streaming write APIs to the online and offline feature store. When using the APIs in a Python environment this behavior is the default. 

### Register the metadata and save the feature data

The snippet above only created the metadata object on the Python interpreter running the code. To register the feature group metadata and to save the feature data with Hopsworks, you should invoke the `save` method:

```python 
fg.save(df)
```

The save method takes in input a Pandas or Spark DataFrame. HSFS will use the DataFrame columns and types to determine the name and types of features, primary key, partition key and event time. 

The DataFrame *must* contains the columns specified as primary keys, partition key and event time in the `create_feature_group` call.

If a feature group is online enabled, the `save` method will store the feature data to both the online and offline storage.

### API Reference 

[FeatureGroup](https://docs.hopsworks.ai/feature-store-api/dev/generated/api/feature_group_api/#featuregroup)

## Create using the UI

You can also create a new feature group through the UI.
