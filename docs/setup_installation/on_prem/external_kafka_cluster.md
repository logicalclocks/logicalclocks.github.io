---
description: Administrator guide on how to integrate Hopsworks with an external Kafka cluster to handle data ingestion into the feature store.
---

# External Kafka cluster

Hopsworks uses [Apache Kafka](https://kafka.apache.org/) to ingest data to the feature store.
Streaming applications and external clients send data to the Kafka cluster for ingestion to the online and offline feature store.
By default, Hopsworks comes with an embedded Kafka cluster managed by Hopsworks itself, however, users can configure Hopsworks to leverage an existing external cluster.
This guide will cover how to configure an Hopsworks cluster to leverage an external Kafka cluster.

## Configure the external Kafka cluster integration

To enable the integration with an external Kafka cluster, you should set the `enable_bring_your_own_kafka` [configuration option](../admin/variables.md) to `true`.
This can also be achieved in the cluster definition by setting the following attribute:

```yaml
hopsworks:
  enable_bring_your_own_kafka: "true"
```

### Online Feature Store service configuration

With the external Kafka cluster integration enabled and a project's `kafka_connector` data source configured (see below), Hopsworks can deploy a dedicated Online Feature Store service (OnlineFS in short) instance in that project's namespace.
Unlike the cluster-level instance, which is deployed by default, a per-project instance is opt-in: a Data Owner must explicitly enable it under `Project Settings` → `OnlineFS Service` (`Enabled` toggle) before it is deployed and starts ingesting.
Once enabled, the instance consumes the project's feature store topics from the external Kafka cluster using the connection settings, credentials, and options of the data source, and it is updated automatically whenever the data source changes.
Deleting the data source removes the instance again.

Each project instance only subscribes to its own project's topics, so multiple projects can safely share the same external Kafka cluster.
Additional Kafka client settings, such as SASL authentication options, can be provided as additional options on the data source and are applied to both the producers and the OnlineFS consumers.

Project members with the Data Owner role can enable and further tune their project's OnlineFS instance under `Project Settings` → `OnlineFS Service`, including pausing ingestion, changing the number of replicas and resources, enabling vectorDB ingestion, and overriding any OnlineFS service or Kafka client setting.
The available settings are the same as for the cluster-level instance, documented in the [OnlineFS service guide](../admin/onlinefs.md#configuration).
Per-project instances are always managed by Hopsworks, independently of whether the cluster-level instance is Helm-managed or Hopsworks-managed.

!!! note "Hopsworks will not provision topics"
    Please note that when using an external Kafka cluster, Hopsworks will not provision the topics for the different projects.
    Users are responsible for provisioning the necessary topics and configure the projects accordingly (see next section).
    The OnlineFS instance discovers matching topics automatically; if a feature group uses a custom topic name that does not follow the default naming scheme, the subscription can be widened with a `kafkaConsumer.topicPattern` service setting override in `Project Settings` → `OnlineFS Service`.

### Project configuration

#### Topic configuration

As mentioned above, when configuring Hopsworks to use an external Kafka cluster, Hopsworks will not provision the topics for the different projects.
Instead, when creating a project, users will be asked to provide the topic name to use for the feature store operations.

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
