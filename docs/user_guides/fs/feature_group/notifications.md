---
description: Documentation on how notifications work for feature groups in Hopsworks.
---

# How notifications work for a Feature Group

## Introduction

Changes to online-enabled feature groups can be captured by listening to events on specified topics.
This optimizes the user experience by allowing users to proactively make predictions as soon as there is an update on the features.

In this guide you will learn how to enable notifications for online feature groups within Hopsworks, showing examples in HSFS APIs as well as the user interface.

## Prerequisites

Before you begin this guide we suggest you read the [Feature Group](../../../concepts/fs/feature_group/fg_overview.md) concept page to understand what a feature group is and how it fits in the ML pipeline.

### Create notification topic

To begin with, you will need to have a topic where the notifications will be sent.
To create a topic you can navigate to the `Kafka` subsection of project `settings` and click on `Add a new topic`.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/feature_group/manage_kafka.png" alt="Manage Kafka">
  </figure>
</p>

After specifying topic details it can be created by clicking on the `Create Topic` button.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/feature_group/create_kafka_topic.png" alt="Create kafka topic">
  </figure>
</p>

## Using HSFS APIs

### Create a Feeature Group with a notification topic

To enable notifications for an online-enabled feature group using the HSFS APIs you need to [create a feature group](./create.md) and set the `notification_topic_name` properties value to the previously created topic.

=== "Python"

    ```python
    fg = fs.create_feature_group(name="feature_group_name", version=feature_group_version, primary_key=feature_group_primary_keys, online_enabled=True, notification_topic_name="notification_topic_name")
    ```

### Update Feature Group notification topic

The notification topic name can be changed after the creation of the feature group.
It can take some time for these changes to take place since the onlinefs service internally caches feature groups for a set amount of time.
By setting the `notification_topic_name` value to `None` or empty string notification will be disabled.

=== "Python"

    ```python
    fg.update_notification_topic_name(notification_topic_name="new_notification_topic_name")
    ```

## Using UI

### Create a Feeature Group with a notification topic

During the creation of the feature group enable online feature serving.
When enabled you will be able to set the notification topic name property.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/feature_group/create_online_enabled_feature_group.png" alt="Create online enabled feature group">
  </figure>
</p>

### Update Feeature Group with notification topic

The notification topic name can be changed after creation by editing the feature group.
It can take some time for notifications to be posted to the new topic.
By setting the `Notification topic name` value empty notifications will be disabled.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/feature_group/edit_online_enabled_feature_group.png" alt="Edit online enabled feature group">
  </figure>
</p>

## Example of notification event

The online feature store service will produce events to the provided notification topic when data ingestion is completed.
Here is an example output:

```
{
  "projectId":119,
  "featureStoreId":67,
  "featureGroupId":14,
  "entry":{
    "id":"15",
    "text":"test"
  },
  "featureViews":[
    {
      "id":9,
      "name":"test",
      "version":1,
      "featurestoreId":67
    }
  ]
}
```