---
description: Documentation on Change Data Capture for feature groups in Hopsworks.
---

# Change Data Capture for feature groups

## Introduction

Changes to online-enabled feature groups can be captured by listening to events on specified topics.
This optimizes the user experience by allowing users to proactively make predictions as soon as there is an update on the features.

In this guide you will learn how to enable Change Data Capture (CDC) for online feature groups within Hopsworks, showing examples in HSFS APIs as well as the user interface.

## Prerequisites

Before you begin this guide we suggest you read the [Feature Group](../../../concepts/fs/feature_group/fg_overview.md) concept page to understand what a feature group is and how it fits in the ML pipeline.
Subsequently [create a Kafka topic](../../projects/kafka/create_topic.md), this topic will be used for storing Change Data Capture events.

## Using HSFS APIs

### Create a Feature Group with Change Data Capture using Python

To enable Change Data Capture for an online-enabled feature group using the HSFS APIs you need to [create a feature group](./create.md) and set the `notification_topic_name` properties value to the previously created topic.

=== "Python"

    ```python
    fg = fs.create_feature_group(
        name="feature_group_name",
        version=feature_group_version,
        primary_key=feature_group_primary_keys,
        online_enabled=True,
        notification_topic_name="notification_topic_name",
    )
    ```

### Update Feature Group with Change Data Capture topic using Python

The notification topic name can be changed after the creation of the feature group.
By setting the `notification_topic_name` value to `None` or empty string notification will be disabled.
With the default configuration, it can take up to 30 minutes for these changes to take place since the onlinefs service internally caches feature groups.

=== "Python"

    ```python
    fg.update_notification_topic_name(
        notification_topic_name="new_notification_topic_name"
    )
    ```

## Using UI

### Create a Feature Group with Change Data Capture using UI

During the creation of the feature group enable online feature serving.
When enabled you will be able to set the `CDC topic name` property.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/feature_group/create_online_enabled_feature_group.png" alt="Create online enabled feature group">
  </figure>
</p>

### Update Feature Group with Change Data Capture topic using UI

The notification topic name can be changed after creation by editing the feature group.
By setting the `CDC topic name` value to empty the notifications will be disabled.
With the default configuration, it can take up to 30 minutes for these changes to take place since the onlinefs service internally caches feature groups.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/feature_group/edit_online_enabled_feature_group.png" alt="Edit online enabled feature group">
  </figure>
</p>

## Example of Change Data Capture event

Once properly set up the online feature store service will produce events to the provided topic when data ingestion is completed for records.

Here is an example output:

```jsonc
{
  "projectName":"project_name",  // name of the project the feature group belongs to
  "projectId":119,  // id of the project the feature group belongs to
  "featureStoreId":67,  // feature store where changes took place
  "featureGroupId":14,  // id of the feature group
  "featureGroupName":"fg_name",  // name of the feature group
  "featureGroupVersion":1,  // version of the feature group
  "entry":{ // values of the affected feature group entry
    "id":"15",
    "text":"test"
  },
  "featureViews":[  // list of feature views affected
    {
      "projectName":"project_name", // name of the project the feature view belongs to
      "id":9,  // id of the feature view
      "name":"test",  // name of the feature view
      "version":1,  // version of the feature view
      "featurestoreId":67  // feature store where feature view resides
    }
  ]
}
```

The list of `featureViews` in the event could be outdated for up to 10 minutes, due to internal logging in onlinefs service.
