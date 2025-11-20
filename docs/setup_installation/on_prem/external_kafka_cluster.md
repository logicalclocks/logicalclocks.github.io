---
description: Administrator guide on how to integrate Hopsworks with an external Kafka cluster to handle data ingestion into the feature store. 
---

# External Kafka cluster

Hopsworks uses [Apache Kafka](https://kafka.apache.org/) to ingest data to the feature store. Streaming applications and external clients send data to the Kafka cluster for ingestion to the online and offline feature store.
By default, Hopsworks comes with an embedded Kafka cluster managed by Hopsworks itself, however, users can configure Hopsworks to leverage an existing external cluster.
This guide will cover how to configure an Hopsworks cluster to leverage an external Kafka cluster.

## Configure the external Kafka cluster integration

To enable the integration with an external Kafka cluster, you should set the `enable_bring_your_own_kafka` [configuration option](../admin/variables.md) to `true`.
This can also be achieved in the cluster definition by setting the following attribute:

```
hopsworks:
  enable_bring_your_own_kafka: "true"
```

### Online Feature Store service configuration

In addition to the configuration changes above, you should also configure the Online Feature Store service (OnlineFS in short) to connect to the external Kafka cluster.
This can be achieved by provisioning the necessary credentials for OnlineFS to subscribe and consume messages from Kafka topics used by the Hopsworks feature store.

OnlineFs can be configured to use these credentials by adding the following configurations to the cluster definition used to deploy Hopsworks:

```
  onlinefs:
    config_dir: "/home/ubuntu/cluster-definitions/byok"
    kafka_cosumers:
      topic_list: "comma separated list of kafka topics to subscribe to"
```

In particular, the `onlinefs/config_dir` should contain the credentials necessary for the Kafka consumers to authenticate.
Additionally the directory should contain a file name `onlinefs-kafka.properties` with the Kafka consumer configuration.
The following is an example of the `onlinefs-kafka.properties` file:

```
bootstrap.servers=cluster_identifier.us-east-2.aws.confluent.cloud:9092
security.protocol=SASL_SSL
sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required username="username" password="password";
sasl.mechanism=PLAIN
```

!!! note "Hopsworks will not provision topics"
    Please note that when using an external Kafka cluster, Hopsworks will not provision the topics for the different projects. Users are responsible for provisioning the necessary topics and configure the projects accordingly (see next section).
    Users should also specify the list of topics OnlineFS should subscribe to by providing the `onlinefs/kafka_consumers/topic_list` option in the cluster definition.

### Project configuration

#### Topic configuration

As mentioned above, when configuring Hopsworks to use an external Kafka cluster, Hopsworks will not provision the topics for the different projects. Instead, when creating a project, users will be asked to provide the topic name to use for the feature store operations.

<p align="center">
  <figure>
    <img src="../../../assets/images/setup_installation/on_prem/byok_project_configuration.png" alt="Example project creation when using an external Kafka cluster">
    <figcaption>Example project creation when using an external Kafka cluster</figcaption>
  </figure>
</p>

#### Data Source configuration

Users should create a [Kafka Data Source](../../user_guides/fs/data_source/creation/kafka.md) named `kafka_connector` which is going to be used by the feature store clients to configure the necessary Kafka producers to send data.
The configuration is done for each project to ensure its members have the necessary authentication/authorization.
If the data source is not found in the project, default values referring to Hopsworks managed Kafka will be used.
