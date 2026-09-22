---
description: Documentation on how to configure and change the Kafka topic used to ingest data into a feature group in Hopsworks.
---

# How to configure the ingestion topic of a Feature Group { #feature-group-ingestion-topic }

## Introduction

Feature groups written with the [streaming write API][streaming-write-api] do not write to the online and offline feature store directly.
Every insert produces the rows to a Kafka topic, from which the OnlineFS service writes them to the online feature store and the offline materialization job writes them to the offline feature store.

By default all feature groups in a project share a single topic.
That works well until one feature group writes enough that the offline materialization jobs of the others spend their runs reading and discarding its records; [the choice of topic for data ingestion][the-choice-of-topic-for-data-ingestion] covers when a dedicated topic is worth it.
In this guide you will learn how to give a feature group a topic of its own, and how to change that topic after the feature group has been created.

## Prerequisites

Before you begin this guide we suggest you read the [create feature group][create-feature-group] guide, which covers the `topic_name` parameter.

## Which topic a feature group uses

Hopsworks resolves the ingestion topic of a feature group in the following order:

1. The `topic_name` of the feature group, if one is set.
2. The topic of the project, if one is set.
3. The project default, which is `<project_name>_onlinefs` for online-enabled feature groups and `<project_name>` otherwise.

Setting `topic_name` to an empty string clears the feature group override, so the feature group falls back to the project topic.

!!! note "Topics of online-enabled feature groups must end in `_onlinefs`"
    The OnlineFS service subscribes to the topics matching the `.*_onlinefs` pattern, so a topic whose name does not match it is never consumed into the online feature store.
    Administrators can change the pattern with the `onlinefs/kafka_consumer/topic_pattern` configuration option, or replace it with an explicit topic list as described in the [external Kafka cluster][external-kafka-cluster] guide.

## Before you change the topic

Changing the topic of a feature group that already holds data is not a migration, and there are two consequences to plan for.

!!! warning "Pending data is not migrated automatically"
    Rows that were already inserted into the old topic but not yet consumed are never materialized to the new topic.
    Wait until all in-flight processing has completed before switching, for example by following the [online ingestion observability][online-ingestion-observability] of the feature group and letting the offline materialization job finish.

!!! warning "Offline materialization restarts from the earliest offset"
    The offline materialization job stores the Kafka offsets it has consumed together with the name of the topic they belong to.
    When it detects that the topic has changed, those offsets are meaningless, so it starts from the earliest available offset of the new topic.
    This reprocesses everything the new topic still retains and can produce duplicates in the offline feature store.

## Using Hopsworks APIs

### Set the topic when creating the feature group

Pass `topic_name` to `create_feature_group` to give the feature group its own topic from the start:

=== "Python"

    ```python
    fg = fs.create_feature_group(
        name="feature_group_name",
        version=1,
        primary_key=["id"],
        online_enabled=True,
        topic_name="feature_group_name_onlinefs",
    )
    ```

### Change the topic of an existing feature group

Use [`FeatureGroup.update_topic_name`][hsfs.feature_group.FeatureGroup.update_topic_name] to point an existing feature group at a different topic:

=== "Python"

    ```python
    fg = fs.get_feature_group("feature_group_name", version=1)

    fg.update_topic_name(topic_name="feature_group_name_onlinefs")
    ```

The call emits the two warnings above as Python warnings before sending the request, and updates your local metadata object only once the backend has accepted the change.

## Using the UI

### Change the feature group topic

Open the feature group, click `Edit`, and set the `Topic name` field.
The field is shown for stream feature groups and for online-enabled feature groups, because those are the ones that ingest through Kafka.
Saving a changed topic name asks you to confirm the two consequences described above before the update is sent.

The topic a feature group currently uses is shown on its overview page.

### Change the project topic

The project topic is the default for every feature group in the project that does not set its own.
Navigate to `Project Settings` → `Kafka` and use `Edit project topic` in the `Project Topic` card.
As with a feature group topic, you are asked to confirm before the change is applied.

!!! note
    The `Project Topic` card is only shown when the cluster is configured to use an [external Kafka cluster][external-kafka-cluster], since that is the case in which the topic is not managed by Hopsworks.

## Topic creation

When you set a topic that does not exist yet, Hopsworks creates it in the project with the cluster defaults for feature store topics.
Topics count against the project's Kafka topic quota, which an administrator can raise as described in the [Kafka topics][kafka-topics] administration guide.

When the cluster is configured to use an external Kafka cluster, Hopsworks does not provision topics.
Create the topic in the external cluster first, otherwise ingestion fails as soon as the feature group starts producing to it.

## API Reference

[`FeatureGroup`][hsfs.feature_group.FeatureGroup]
