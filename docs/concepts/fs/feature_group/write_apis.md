You write to feature groups, and read from feature views.

There are 3 APIs for writing to feature groups, as shown in the table below:

|  | Stream API | Batch API  | Connector API  |
|---|---|---|---|
| Python | X  | -  | - |
| Spark | X | X | - |
| Flink | X  | -  | - |
| External Table | - | - | X |


## Stream API

The Stream API is the only API for Python and Flink clients, and is
the preferred API for Spark, as it ensures consistent features between offline and online feature stores.
The Stream API first writes data to be ingested to a Kafka topic, and then Hopsworks ensures that the data is synchronized to the Online and Offline Feature Groups through the OnlineFS service and Hudi DeltaStreamer jobs, respectively. The data in the feature groups is guaranteed to arrive at-most-once, through idempotent writes to the online feature group (only the latest values of features are stored there, and duplicates in Kafka only cause idempotent updates) and duplicate removal by Apache Hudi for the offline feature group.

<img src="../../../../assets/images/concepts/fs/fg-stream-api.svg">


## Batch API

For very large updates to feature groups, such as when you are backfilling large amounts of data to an offline feature group, it is often preferential to write directly to the Hudi tables in Hopsworks, instead of via Kafka - thus reducing write amplification. Spark clients can write directly to Hudi tables on Hopsworks with Hopsworks libraries and certificates using a HDFS API. This requires network connectivity between the Spark clients and the datanodes in Hopsworks.

<img src="../../../../assets/images/concepts/fs/fg-batch-api.svg">


## Connector API

Hopsworks supports external tables as feature groups. You can mount a table from an external database as an offline feature group using the Connector API - you create an external table using the connector. This enables you to use features from your external data source (Snowflake, Redshift, Delta Lake, etc) as you would any feature in an offline feature group in Hopsworks. You can, for example, join features from different feature groups (external or not) together to create feature views and training data for models.

<img src="../../../../assets/images/concepts/fs/fg-connector-api.svg">
