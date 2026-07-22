---
description: Administrator guide for configuring the Hopsworks-managed OnlineFS service that ingests data into the online feature store.
---

# OnlineFS Service

The Online Feature Store service (OnlineFS in short) consumes feature data from Kafka and writes it to the online feature store (RonDB).
This guide covers the cluster-level OnlineFS instance, which consumes from the Kafka cluster embedded in Hopsworks.
For the per-project OnlineFS instances used with an external Kafka cluster, see the [external Kafka cluster guide](../on_prem/external_kafka_cluster.md).

## Helm-managed vs. Hopsworks-managed

The cluster-level OnlineFS instance can be deployed in two ways, and only one is active at a time:

- **Deployed by the `onlinefs` Helm chart.** This is the traditional deployment method and continues to be fully supported. If the `onlinefs` chart is installed, Hopsworks detects the resulting deployment and leaves it alone entirely: Hopsworks never creates, modifies or removes it, and the configuration described below is unavailable — configure the instance through the Helm chart's own values instead.
- **Deployed and managed by Hopsworks itself.** If no `onlinefs` Helm release is present, Hopsworks deploys and reconciles the cluster-level instance automatically, using the configuration described below.

Because of this precedence, installing the `onlinefs` Helm chart on a cluster where Hopsworks was previously managing the instance (or vice versa) is safe: whichever one is Helm-managed always wins, so the two never run at the same time.

Cluster Settings → `OnlineFS Service` (and the `/admin/onlinefs/status` REST endpoint) shows which mode is currently active.

## The Hopsworks-managed deployment

When there is no Helm-managed instance, Hopsworks deploys the cluster-level OnlineFS instance itself, on by default. It can be paused with the `Enabled` toggle in its configuration (see below).

Hopsworks creates and reconciles all resources the service needs in the Hopsworks namespace: the deployment, its configuration, the metrics service scraped by Prometheus, the TLS material used to connect to the internal Kafka cluster, and the API key the service uses to call the Hopsworks REST API.
Configuration changes roll the OnlineFS pods automatically.
A periodic reconciler additionally converges the deployment against the stored configuration, so manual changes to the Kubernetes resources are reverted; the same reconciler also re-checks whether a Helm-managed instance has appeared or disappeared, and defers to it or takes over accordingly.

## Configuration

The cluster-level OnlineFS instance is configured from the admin UI under `Cluster Settings` → `OnlineFS Service`, or through the `/admin/onlinefs/config` REST endpoint.
This is only available while Hopsworks is managing the cluster-level instance itself (see above); while a Helm-managed instance is active, these settings have no effect.
Empty fields use the platform defaults.

<p align="center">
  <figure>
    <img src="../../../assets/images/guides/onlinefs/cluster_onlinefs.png" alt="Cluster-level OnlineFS Service configuration in Cluster Settings">
    <figcaption>Cluster-level OnlineFS Service configuration in Cluster Settings</figcaption>
  </figure>
</p>

The same set of settings is available for the per-project OnlineFS instances deployed when using an external Kafka cluster, under `Project Settings` → `OnlineFS Service`.
Unlike the cluster-level instance, which is enabled by default, per-project instances are opt-in: `Enabled` defaults to off and a Data Owner must turn it on before the instance is deployed.
See the [external Kafka cluster guide](../on_prem/external_kafka_cluster.md#online-feature-store-service-configuration) for details.

<p align="center">
  <figure>
    <img src="../../../assets/images/guides/onlinefs/project_onlinefs.png" alt="Per-project OnlineFS Service configuration in Project Settings">
    <figcaption>Per-project OnlineFS Service configuration in Project Settings</figcaption>
  </figure>
</p>

| Field | Description |
| --- | --- |
| Enabled | Turning this off removes the OnlineFS deployment and pauses all ingestion; the configuration and consumer offsets are kept. Defaults to on for the cluster-level instance, off for per-project instances. |
| VectorDB ingestion | Also ingest embeddings into the vector database (OpenSearch). |
| Replicas | Number of OnlineFS pods (0-10). Instances coordinate through a shared Kafka consumer group. |
| CPU/Memory request and limit | Kubernetes resource quantities for the OnlineFS container, e.g. `500m` or `2Gi`. |
| Service settings | Free-form overrides for `onlinefs-site.xml` as `section.key` entries, e.g. `service.threadNumber`, `rondb.batchSize` or `kafkaConsumer.topicPattern`. See the [reference table](#service-settings-reference) below for every available key. |
| Kafka consumer properties | Free-form Kafka client properties appended to the consumer configuration, e.g. `max.poll.records`. |
| Kafka producer properties | Free-form Kafka client properties appended to the notification producer configuration, e.g. `batch.size`. |
| Kafka vectorDB consumer properties | Free-form Kafka client properties for the vectorDB consumer; only used when vectorDB ingestion is enabled. |

The override entries take precedence over the values generated by Hopsworks, so every OnlineFS setting is configurable.

### Service settings reference

`Service settings` entries are `section.key` pairs written into `onlinefs-site.xml`. Below is every key OnlineFS reads, grouped by section, with its default value.

**`service`**

| Key | Default | Description |
| --- | --- | --- |
| `service.threadNumber` | `10` | Number of threads used for reporting metadata/status back to Hopsworks and for sending CDC notifications. |
| `service.ronDbThreadNumber` | `10` | Number of Kafka consumer threads ingesting into RonDB. |
| `service.vectorDbThreadNumber` | `5` | Number of Kafka consumer threads ingesting into the vector database (OpenSearch); only relevant when VectorDB ingestion is enabled. |
| `service.reportingQueueSizePerThread` | `100` | Queue size per reporting/notification thread. |
| `service.getSessionRetrySleepMs` | `100` | Milliseconds to sleep between retries when acquiring a RonDB (ClusterJ) session. |
| `service.maxBlacklistSize` | `100` | Max size of the blacklist cache used by the Hopsworks helper. |
| `service.maxFeatureGroupCacheSize` | `1000` | Max entries kept in the feature group metadata cache. |
| `service.maxFeatureStoreCacheSize` | `1000` | Max entries kept in the feature store metadata cache. |
| `service.maxFeatureViewCacheSize` | `1000` | Max entries kept in the feature view metadata cache. |
| `service.featureGroupCacheExpire` | `30` | Feature group cache entry expiry, in minutes. |
| `service.featureStoreCacheExpire` | `30` | Feature store cache entry expiry, in minutes. |
| `service.featureViewCacheExpire` | `10` | Feature view cache entry expiry, in minutes. |
| `service.region` | _(none)_ | Cloud region reported in CDC notification payloads, identifying where this OnlineFS instance runs. |
| `service.pauseRetrySleepMs` | `5000` | Milliseconds to sleep between attempts while ingestion is paused waiting for a transient failure (e.g. a RonDB or Hopsworks upgrade) to resolve. |

**`rondb`**

| Key | Default | Description |
| --- | --- | --- |
| `rondb.connectionString` | `127.0.0.1:1186` | RonDB (NDB) cluster connect string. |
| `rondb.batchSize` | `1000` | Max batch size when committing rows to RonDB. |
| `rondb.maxRetries` | `3` | Max retries for a RonDB commit operation. |
| `rondb.poolSize` | `1` | ClusterJ connection pool size. |
| `rondb.maxCachedSessions` | `20` | Max ClusterJ sessions cached per connection. |
| `rondb.reconnectTimeout` | `5` | ClusterJ connection reconnect timeout, in seconds. |
| `rondb.maxTransactions` | `1024` | Max concurrent ClusterJ transactions. |
| `rondb.maxCachedInstances` | `1024` | Max ClusterJ cached instances. |
| `rondb.useDynamicObjectCache` | `true` | Whether ClusterJ uses a dynamic object cache. |
| `rondb.useSessionCache` | `true` | Whether ClusterJ uses a session cache. |

**`kafka`**

| Key | Default | Description |
| --- | --- | --- |
| `kafka.propertiesFile` | `onlinefs-kafka.properties` | Kafka client properties file used for the RonDB ingestion consumer. |
| `kafka.propertiesFileVectorDb` | `onlinefs-kafka-vector-db.properties` | Kafka client properties file used for the VectorDB ingestion consumer. |
| `kafka.propertiesFileNotification` | `producer.properties` | Kafka client properties file used for the CDC notification producer. |

**`kafkaConsumer`**

| Key | Default | Description |
| --- | --- | --- |
| `kafkaConsumer.topicPattern` | `.*_onlinefs` | Regex pattern used to subscribe to Kafka topics. |
| `kafkaConsumer.topicList` | _(empty)_ | Comma-separated list of explicit topics to consume, in addition to the topic pattern. |
| `kafkaConsumer.pollTimeoutMs` | `1000` | Kafka consumer poll timeout, in milliseconds. |

**`hopsworks`**

| Key | Default | Description |
| --- | --- | --- |
| `hopsworks.url` | `https://hopsworks.glassfish.service.consul:8182` | Base URL of the Hopsworks REST API. |
| `hopsworks.trustStoreLocation` | `trustStore.jks` | Path to the trust store used for TLS to Hopsworks (and to OpenSearch). |
| `hopsworks.tokenLocation` | `token` | Path to the file containing the Hopsworks API key used by this instance. |

**`opensearch`** (VectorDB ingestion)

| Key | Default | Description |
| --- | --- | --- |
| `opensearch.host` | `https://elastic.service.consul:9200` | OpenSearch endpoint URL. |
| `opensearch.userName` | `onlinefs` | OpenSearch auth username. |
| `opensearch.password` | `onlinefs` | OpenSearch auth password. |
| `opensearch.batchSize` | `1000` | Max batch size when committing embeddings to OpenSearch. |
| `opensearch.maxRetries` | `10` | Max retries for an OpenSearch commit operation. |

**`metrics`**

| Key | Default | Description |
| --- | --- | --- |
| `metrics.port` | `12800` | Port for the Prometheus metrics HTTP server. |

The Hopsworks-managed deployment provisions `hopsworks.*` and `opensearch.*` automatically (URL, trust store, token, OpenSearch endpoint and credentials); overriding them is rarely needed outside of troubleshooting.

## VectorDB ingestion

When vectorDB ingestion is enabled, OnlineFS runs an additional set of consumers that write embedding features to the vector database (OpenSearch).
The OpenSearch endpoint and credentials are provisioned automatically from the cluster.
The vectorDB consumers use their own Kafka consumer group and track their own offsets, so enabling vectorDB ingestion on an existing deployment starts consuming from the earliest available offset.
