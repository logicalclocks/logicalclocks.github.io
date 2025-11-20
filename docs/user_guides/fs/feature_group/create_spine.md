---
description: Documentation on how to create Spine Group in Hopsworks and the different APIs available to interact with them.
---

# How to create Spine Group

### Introduction

In this guide you will learn how to create and register a Spine Group with Hopsworks.

## Prerequisites

Before you begin this guide we suggest you read the [Spine Group](../../../concepts/fs/feature_group/spine_group.md) concept page to understand what a Spine Group is and how it fits in the ML pipeline.

## Create using the HSFS APIs

### Create a Spine Group

Instead of using a feature group to save the label, you can also use a spine to use a Dataframe containing the labels on the fly.
A spine is essentially a metadata object similar to a Feature Group, which tells the feature store the relevant event time column and primary key columns to perform point-in-time correct joins.

Additionally, apart from primary key and event time information, a Spark dataframe is required in order to infer the schema of the group from.

=== "Python"

    ```python
    trans_spine = fs.get_or_create_spine_group(
        name="spine_transactions",
        version=1,
        description="Transaction data",
        primary_key=['cc_num'],
        event_time='datetime',
        dataframe=trans_df
    )
    ```

Once created, note that you can inspect the dataframe in the Spine Group:

=== "Python"

    ```python
    trans_spine.dataframe.show()
    ```

And you can always also replace the dataframe contained within the Spine Group.
You just need to make sure it has the same schema.

=== "Python"

    ```python
    trans_spine.dataframe = new_df
    ```

### Limitations

!!! warning "Python support"

    Currently the HSFS library does not support usage of Spine Groups for training data creation or batch data retrieval in the Python engine.
    However, it is supported to create Spine Groups from the Python engine.

### API Reference

[SpineGroup](<https://docs.hopsworks.ai/hopsworks-api/{{{hopsworks_version}}}/generated/api/spine_group_api/#spinegroup)
