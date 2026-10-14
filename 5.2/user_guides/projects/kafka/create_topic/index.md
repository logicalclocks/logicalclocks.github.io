# How To Create A Kafka Topic

## Introduction

A Topic is a queue to which records are stored and published.
Producer applications write data to topics and consumer applications read from topics.

## Prerequisites

This guide requires that you have 'Data owner' role and have previously created a [Kafka Schema](create_schema.md) to be used for the topic.

## Code

In this guide, you will learn how to create a Kafka Topic.

### Step 1: Get the Kafka API

```python
import hopsworks


project = hopsworks.login()

kafka_api = project.get_kafka_api()
```

### Step 2: Define the schema

```python
TOPIC_NAME = "topic_example"
SCHEMA_NAME = "schema_example"

my_topic = kafka_api.create_topic(
    TOPIC_NAME, SCHEMA_NAME, 1, replicas=1, partitions=1
)
```

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-class"></code> [`KafkaApi`][hopsworks_common.core.kafka_api.KafkaApi]
        - <code class="doc-symbol doc-symbol-method"></code> [`create_topic`][hopsworks_common.core.kafka_api.KafkaApi.create_topic]
    - <code class="doc-symbol doc-symbol-class"></code> [`KafkaTopic`][hopsworks_common.kafka_topic.KafkaTopic]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>
