# How To Create A Kafka Topic

## Introduction

A Topic is a queue to which records are stored and published. Producer applications write data to topics and consumer applications read from topics.

## Prerequisites

This guide requires that you have previously created a [Kafka Schema](create_schema.md) to be used for the topic.


## Code

In this guide, you will learn how to create a Kafka Topic.

### Step 1: Get the Kafka API

```python

import hopsworks

connection = hopsworks.connection()

project = connection.get_project()

kafka_api = project.get_kafka_api()

```

### Step 2: Define the schema

```python

TOPIC_NAME="topic_example"
SCHEMA_NAME="schema_example"

my_topic = kafka_api.create_topic(TOPIC_NAME, SCHEMA_NAME, 1, replicas=1, partitions=1)

```

### API Reference

[KafkaTopic](https://docs.hopsworks.ai/hopsworks-api/dev/generated/api/kafka_topic/)

## Conclusion

In this guide you learned how to create a Kafka Topic.