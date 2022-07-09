# How To Consume Message From A Topic

## Introduction

A Consumer is a process which reads messages from a kafka topic.

## Prerequisites

This guide requires that you have previously [produced](produce_messages.md) messages to a kafka topic.

## Code

In this guide, you will learn how to consume messages from a kafka topic.

### Step 1: Get the Kafka API

```python

import hopsworks

connection = hopsworks.connection()

project = connection.get_project()

kafka_api = project.get_kafka_api()

```

### Step 2: Configure confluent-kafka client

```python

consumer_config = kafka_api.get_default_config()
consumer_config['default.topic.config'] = {'auto.offset.reset': 'earliest'}

from confluent_kafka import Consumer

consumer = Consumer(consumer_config)

```

### Step 3: Consume messages from a topic

```python

# Subscribe to topic
consumer.subscribe(["my_topic"])

for i in range(0, 10):
    msg = consumer.poll(timeout=10.0)
    print(msg.value())

```

### API Reference

[KafkaTopic](https://docs.hopsworks.ai/hopsworks-api/dev/generated/api/kafka_topic/)

## Conclusion

In this guide you learned how to consume messages from a Kafka Topic.