# How To Produce To A Topic

## Introduction

A Producer is a process which produces messages to a kafka topic.

## Prerequisites

This guide requires that you have previously created a [Kafka Topic](create_topic.md).

## Code

In this guide, you will learn how to produce messages to a kafka topic.

### Step 1: Get the Kafka API

```python

import hopsworks

connection = hopsworks.connection()

project = connection.get_project()

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

import uuid
import json

# Send a few messages
for i in range(0, 10):
    producer.produce("my_topic", json.dumps({"id": i, "data": str(uuid.uuid1())}), "key")

# Trigger the sending of all messages to the brokers, 10 sec timeout
producer.flush(10)

```

### API Reference

[KafkaTopic](https://docs.hopsworks.ai/hopsworks-api/dev/generated/api/kafka_topic/)

## Conclusion

In this guide you learned how to produce messages to a Kafka Topic. Next step is to create a [Consumer](consume_messages.md) to read the messages from the topic.