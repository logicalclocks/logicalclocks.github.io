## Compute Engines

In order to execute a feature pipeline to write to the Feature Store, as well as to retrieve data from the Feature Store, you need a compute engine.
Hopsworks Feature Store APIs are built around dataframes, that means feature data is inserted into the Feature Store from a Dataframe and likewise when reading data from the Feature Store, it is returned
as a Dataframe.

As such, Hopsworks supports five computational engines:

1. [Apache Spark](https://spark.apache.org): Spark Dataframes and Spark Structured Streaming Dataframes are supported, both from Python environments (PySpark) and from Scala environments.
2. [Python](https://www.python.org/): For pure Python environments without dependencies on Spark, Hopsworks supports [Pandas Dataframes](https://pandas.pydata.org/) and [Polars Dataframes](https://pola.rs/).
3. [Apache Flink](https://flink.apache.org): Flink Data Streams are currently supported as an experimental feature from Java/Scala environments.
4. [Apache Beam](https://beam.apache.org/) *experimental*: Beam Data Streams are currently supported as an experimental feature from Java/Scala environments.
5. [Java](https://www.java.com): For pure Java environments without dependencies on Spark, Hopsworks supports writing using List of POJO Objects. 

Hopsworks supports running [compute on the platform itself](../../concepts/dev/inside.md) in the form of [Jobs](../projects/jobs/pyspark_job.md) or in [Jupyter Notebooks](../projects/jupyter/python_notebook.md).
Alternatlively, you can also connect to Hopsworks using Python or Spark from [external environments](../../concepts/dev/outside.md), given that there is network connectivity.

## Functionality Support

Hopsworks is aiming to provide functional parity between the computational engines, however, there are certain Hopsworks functionalities which are exclusive to the engines.

| Functionality                                                     | Method                                                                                                                                                                          | Spark              | Python             | Flink                  | Beam               | Java               | Comment                                                                                                                                                                                                                                                                                                    |
| ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | ------------------ | ---------------------- | ------------------ | ------------------ |------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Feature Group Creation from dataframes                            | [`FeatureGroup.create_feature_group()`](https://docs.hopsworks.ai/feature-store-api/{{{ hopsworks_version }}}/generated/api/feature_group_api/#create_feature_group)            | :white_check_mark: | :white_check_mark: | -                      | -                  | -                  | Currently Flink/Beam/Java doesn't support registering feature group metadata. Thus it needs to be pre-registered before you can write real time features computed by Flink/Beam.                                                                                                                           |
| Training Dataset Creation from dataframes                         | [`TrainingDataset.save()`](https://docs.hopsworks.ai/feature-store-api/{{{ hopsworks_version }}}/generated/api/training_dataset_api/#save)                                     | :white_check_mark: | -                  | -                      | -                  | -                  | Functionality was deprecated in version 3.0                                                                                                                                                                                                                                                                |
| Data validation using Great Expectations for streaming dataframes | [`FeatureGroup.validate()`](https://docs.hopsworks.ai/feature-store-api/{{{ hopsworks_version }}}/generated/api/feature_group_api/#validate) <br/> [`FeatureGroup.insert_stream()`](https://docs.hopsworks.ai/feature-store-api/{{{ hopsworks_version }}}/generated/api/feature_group_api/#insert_stream) | -                  | -                  | -                      | -                  | -                  | `insert_stream` does not perform any data validation even when a expectation suite is attached.                                                                                  |
| Stream ingestion                                                  | [`FeatureGroup.insert_stream()`](https://docs.hopsworks.ai/feature-store-api/{{{ hopsworks_version }}}/generated/api/feature_group_api/#insert_stream)                          | :white_check_mark: | -                  | :white_check_mark:     | :white_check_mark: | :white_check_mark: | Python/Pandas/Polars has currently no notion of streaming.                                                                                                                                                                                                                                                 |
| Reading from Streaming Storage Connectors                         | [`KafkaConnector.read_stream()`](https://docs.hopsworks.ai/feature-store-api/{{{ hopsworks_version }}}/generated/api/storage_connector_api/#read_stream)                        | :white_check_mark: | -                  | -                      | -                  | -                  | Python/Pandas/Polars has currently no notion of streaming. For Flink/Beam/Java only write operations are supported                                                                                                                                                                                         |
| Reading training data from external storage other than S3         | [`FeatureView.get_training_data()`](https://docs.hopsworks.ai/feature-store-api/{{{ hopsworks_version }}}/generated/api/feature_view_api/#get_training_data)                    | :white_check_mark: | -                  | -                      | -                  | -                  | Reading training data that was written to external storage using a Storage Connector other than S3 can currently not be read using HSFS APIs, instead you will have to use the storage's native client.                                                                                                    |
| Reading External Feature Groups into Dataframe                    | [`ExternalFeatureGroup.read()`](https://docs.hopsworks.ai/feature-store-api/{{{ hopsworks_version }}}/generated/api/external_feature_group_api/#read)                           | :white_check_mark: | -                  | -                      | -                  | -                  | Reading an External Feature Group directly into a Pandas/Polars Dataframe is not supported, however, you can use the [Query API](https://docs.hopsworks.ai/feature-store-api/{{{ hopsworks_version }}}/generated/api/query_api/) to create Feature Views/Training Data containing External Feature Groups. |
| Read Queries containing External Feature Groups into Dataframe    | [`Query.read()`](https://docs.hopsworks.ai/feature-store-api/{{{ hopsworks_version }}}/generated/api/query_api/#read)                                                           | :white_check_mark: | -                  | -                      | -                  | -                  | Reading a Query containing an External Feature Group directly into a Pandas/Polars Dataframe is not supported, however, you can use the Query to create Feature Views/Training Data and write the data to a Storage Connector, from where you can read up the data into a Pandas/Polars Dataframe.         |

## Python

### Inside Hopsworks

If you are using Spark or Python within Hopsworks, there is no further configuration required. Head over to the [Getting Started Guide](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/quickstart.ipynb){:target="_blank"}.

### Outside Hopsworks

Connecting to the Feature Store from any Python environment, such as your local environment or Google Colab, requires setting up an API Key and installing the HSFS Python client library. The [Python integration guide](../integrations/python.md) explains step by step how to connect to the Feature Store from any Python environment.

## Spark

### Inside Hopsworks

If you are using Spark or Python within Hopsworks, there is no further configuration required. Head over to the [Getting Started Guide](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/quickstart.ipynb){:target="_blank"}.

### Outside Hopsworks

Connecting to the Feature Store from an external Spark cluster, such as Cloudera or Databricks, requires configuring it with the Hopsworks client jars, configuration and certificates. The [Spark integration guide](../integrations/spark.md) explains step by step how to connect to the Feature Store from an external Spark cluster.

## Flink

### Inside Hopsworks

If you are using Flink within Hopsworks, there is no further configuration required. For more details head over to the [Getting Started Guide](https://github.com/logicalclocks/hopsworks-tutorials/tree/master/integrations/java/flink).

### Outside Hopsworks

Connecting to the Feature Store from an external Flink cluster, such as GCP DataProc or AWS EMR, requires configuring the Hopsworks certificates. The [Flink integration guide](../integrations/flink.md) explains step by step how to connect to the Feature Store from an external Flink cluster.

## Beam

### Inside Hopsworks

Beam is only supported as an external client. 

### Outside Hopsworks

Connecting to the Feature Store from Beam DataFlowRunner, requires configuring the Hopsworks certificates. The [Beam integration guide](../integrations/beam.md) explains step by step how to connect to the Feature Store from Beam Dataflow Runner.

!!! warning

Apache Beam integration with Hopsworks feature store was only tested using Dataflow Runner.


For more details head over to the [Getting Started Guide](https://github.com/logicalclocks/hopsworks-tutorials/tree/master/integrations/java/beam).

## Java
It is also possible to interact to Hopsworks feature store using  pure Java environments without dependencies on Spark, Flink or Beam.

For more details head over to the [Getting Started Guide](https://github.com/logicalclocks/hopsworks-tutorials/tree/master/java).