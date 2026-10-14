# How To Produce To A Topic

## Introduction

A Producer is a process which produces messages to a Kafka topic.
In Hopsworks, only users with the 'Data owner' role are capable of performing the 'Write' action on Kafka topics within the project that they are a member of.

## Prerequisites

This guide requires that you have 'Data owner' role and have previously created a [Kafka Topic](create_topic.md).

## Code

In this guide, you will learn how to produce messages to a kafka topic.

### Step 1: Get the Kafka API

```python
import hopsworks


project = hopsworks.login()

kafka_api = project.get_kafka_api()
```

### Step 2: Configure confluent-kafka client

```python
producer_config = kafka_api.get_default_config()

from confluent_kafka import Producer

producer = Producer(producer_config)
```

### Step 3: Produce messages to topic

```python
import json
import uuid

# Send a few messages
for i in range(0, 10):
    producer.produce(
        "my_topic", json.dumps({"id": i, "data": str(uuid.uuid1())}), "key"
    )

# Trigger the sending of all messages to the brokers, 10 sec timeout
producer.flush(10)
```

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-class"></code> [`KafkaApi`][hopsworks_common.core.kafka_api.KafkaApi]
        - <code class="doc-symbol doc-symbol-method"></code> [`get_default_config`][hopsworks_common.core.kafka_api.KafkaApi.get_default_config]
    - <code class="doc-symbol doc-symbol-class"></code> [`KafkaTopic`][hopsworks_common.kafka_topic.KafkaTopic]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>

## Going Further

Now you can create a [Consumer](consume_messages.md) to read the messages from the topic.
