# How To Create A Kafka Schema

## Introduction

## Code

In this guide, you will learn how to create a Kafka Avro Schema in the Hopsworks Schema Registry.

### Step 1: Get the Kafka API

```python
import hopsworks


project = hopsworks.login()

kafka_api = project.get_kafka_api()
```

### Step 2: Define the schema

Define the Avro Schema, see [types](https://avro.apache.org/docs/current/spec.html#schema_primitive) for the format of the schema.

```python
schema = {
    "type": "record",
    "name": "tutorial",
    "fields": [
        {"name": "id", "type": "int"},
        {"name": "data", "type": "string"},
    ],
}
```

### Step 3: Create the schema

Create the schema in the Schema Registry.

```python
SCHEMA_NAME = "schema_example"

my_schema = kafka_api.create_schema(SCHEMA_NAME, schema)
```

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-class"></code> [`KafkaApi`][hopsworks_common.core.kafka_api.KafkaApi]
        - <code class="doc-symbol doc-symbol-method"></code> [`create_schema`][hopsworks_common.core.kafka_api.KafkaApi.create_schema]
    - <code class="doc-symbol doc-symbol-class"></code> [`KafkaSchema`][hopsworks_common.kafka_schema.KafkaSchema]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>
