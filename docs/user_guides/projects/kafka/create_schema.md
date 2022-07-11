# How To Create A Kafka Schema

## Introduction



## Code

In this guide, you will learn how to create a Kafka Avro Schema in the Hopsworks Schema Registry.

### Step 1: Get the Kafka API

```python

import hopsworks

connection = hopsworks.connection()

project = connection.get_project()

kafka_api = project.get_kafka_api()

```

### Step 2: Define the schema

Define the Avro Schema, see [types](https://avro.apache.org/docs/current/spec.html#schema_primitive) for the format of the schema.

```python

schema = {
    "type": "record",
    "name": "tutorial",
    "fields": [
        {
            "name": "id",
            "type": "int"
        },
        {
            "name": "data",
            "type": "string"
        }
    ]
}




```

### Step 3: Create the schema

Create the schema in the Schema Registry.

```python

SCHEMA_NAME="schema_example"

my_schema = kafka_api.create_schema(SCHEMA_NAME, schema)

```

### API Reference

[KafkaSchema](https://docs.hopsworks.ai/hopsworks-api/dev/generated/api/kafka_schema/)

## Conclusion

In this guide you learned how to create a Kafka Schema.