---
description: Documentation on how notifications work for feature groups in Hopsworks.
---

# How notifications work for a Feature Group

### Introduction

Changes to online-enabled feature groups can be captured by listening to events on specified topics.
This optimizes the user experience by allowing users to proactively make predictions as soon as there is an update on the features.

In this guide you will learn how to enable notifications for online feature groups within Hopsworks, showing examples in HSFS APIs as well as the user interface.

## Prerequisites

Before you begin this guide we suggest you read the [Feature Group](../../../concepts/fs/feature_group/fg_overview.md) concept page to understand what a feature group is and how it fits in the ML pipeline.

## Create notification topic

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

## Create Feeature Group with notification topic in HSFS APIs

To enable notifications for an online-enabled feature group using the HSFS APIs you need to [create a feature group](./create.md) and set the `notification_topic_name` properties value to the create topic.

=== "Python"

    ```python
    fg = fs.create_feature_group(name="feature_group_name", version=feature_group_version, primary_key=feature_group_primary_keys, online_enabled=True, notification_topic_name="notification_topic_name")
    ```

## Create a Feeature Group with a notification topic using the UI

TODO write stuff here

## Example of notification event structure

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