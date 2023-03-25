---
description: Documentation on how to create an external feature group in Hopsworks and the different APIs available to interact with them.
---

# How to create an External Feature Group

### Introduction

In this guide you will learn how to create and register an external feature group with Hopsworks. This guide covers creating an external feature group using the HSFS APIs as well as the user interface.

## Prerequisites

Before you begin this guide we suggest you read the [External Feature Group](../../../concepts/fs/feature_group/external_fg.md) concept page to understand what a feature group is and how it fits in the ML pipeline.

## Create using the HSFS APIs

### Retrieve the storage connector

To create an external feature group using the HSFS APIs you need to provide an existing [storage connector](../storage_connector/index.md).

=== "Python"

    ```python
    connector = feature_store.get_storage_connector("connector_name")
    ```

### Create an External Feature Group

The first step is to instantiate the metadata through the `create_external_feature_group` method. Once you have defined the metadata, you can 
[persist the metadata and create the feature group](#register-the-metadata) in Hopsworks by calling `fg.save()`.

#### SQL based external feature group

=== "Python"

    ```python
    query = """
        SELECT TO_NUMERIC(ss_store_sk) AS ss_store_sk
            , AVG(ss_net_profit) AS avg_ss_net_profit
            , SUM(ss_net_profit) AS total_ss_net_profit 
            , AVG(ss_list_price) AS avg_ss_list_price
            , AVG(ss_coupon_amt) AS avg_ss_coupon_amt
            , sale_date
            , ss_store_sk
        FROM STORE_SALES
        GROUP BY ss_store_sk, sales_date
    """

    fg = feature_store.create_external_feature_group(name="sales",
        version=1,
        description="Physical shop sales features",
        query=query,
        storage_connector=connector,
        primary_key=['ss_store_sk'],
        event_time='sale_date'
    )

    fg.save()
    ```

#### Data Lake based external feature group 

=== "Python"

    ```python
    fg = feature_store.create_external_feature_group(name="sales",
        version=1,
        description="Physical shop sales features",
        data_format="parquet",
        storage_connector=connector,
        primary_key=['ss_store_sk'],
        event_time='sale_date'
    )

    fg.save()
    ```

The full method documentation is available [here](https://docs.hopsworks.ai/feature-store-api/{{{ hopsworks_version }}}/generated/api/external_feature_group_api/#externalfeaturegroup). `name` is a mandatory parameter of the `create_external_feature_group` and represents the name of the feature group.

The version number is optional, if you don't specify the version number the APIs will create a new version by default with a version number equals to the highest existing version number plus one.

If the storage connector is defined for a data warehouse (e.g. JDBC, Snowflake, Redshift) you need to provide a SQL statement that will be executed to compute the features. If the storage connector is defined for a data lake, the location of the data as well as the format need to be provided.

Additionally we specify which columns of the DataFrame will be used as primary key, and event time. Composite primary keys are also supported. 

### Register the metadata

In the snippet above it's important that the created metadata object gets registered in Hopsworks. To do so, you should invoke the `save` method:

=== "Python"

    ```python 
    fg.save()
    ```

### Limitations 

Hopsworks Feature Store does not support time-travel capabilities for external feature groups. Moreover, as the data resides on external systems, external feature groups cannot be made available online for low latency serving. To make data from an external feature group available online, users need to define an online enabled feature group and have a job that periodically reads data from the external feature group and writes in the online feature group.

!!! warning "Python support"

    Currently the HSFS library does not support calling the read() or show() methods on external feature groups. Likewise it is not possible to call the read() or show() methods on queries containing external feature groups. Nevertheless, external feature groups can be used from a Python engine to create training datasets.


### API Reference 

[External FeatureGroup](https://docs.hopsworks.ai/feature-store-api/{{{ hopsworks_version }}}/generated/api/external_feature_group_api/#externalfeaturegroup)

## Create using the UI

You can also create a new feature group through the UI. For this, navigate to the `Feature Groups` section and press the `Create` button at the top-right corner.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/feature_group/no_feature_group_list.png" alt="List of Feature Groups">
  </figure>
</p>

Subsequently, you will be able to define its properties (such as name, mode, features, and more). Refer to the documentation above for an explanation of the parameters available, they are the same as when you create a feature group using the SDK. Finally, complete the creation by clicking `Create New Feature Group` at the bottom of the page.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/feature_group/create_feature_group.png" alt="Create new Feature Group">
  </figure>
</p>
