# Storage Connector Usage
Here, we look at how to use a Storage Connector after it has been created.
Storage Connectors provide an important first step for integrating with external data sources.
The 3 fundamental functionalities where storage connectors are used are:

1. Reading data into Spark Dataframes
2. Creating external feature groups
3. Writing training data

We will walk through each functionality in the sections below.

## Retrieving a Storage Connector
We retrieve a storage connector simply by its unique name.

=== "PySpark"
    ```python
    import hopsworks 
    # Connect to the Hopsworks feature store
    project = hopsworks.login()
    feature_store = project.get_feature_store()
    # Retrieve storage connector
    connector = feature_store.get_storage_connector('connector_name')
    ```

=== "Scala"
    ```scala
    import com.logicalclocks.hsfs._
    val connection = HopsworksConnection.builder().build();
    val featureStore = connection.getFeatureStore();
    // get directly via connector sub-type class e.g. for GCS type
    val connector = featureStore.getGcsConnector("connector_name")
    ```

## Reading a Spark Dataframe from a Storage Connector

One of the most common usages of a Storage Connector is to read data directly into a Spark Dataframe.
It's achieved via the `read` API of the connector object, which hides all the complexity of authentication and integration
with a data storage source.
The `read` API primarily has two parameters for specifying the data source, `path` and `query`, depending on the storage connector type.
The exact behaviour could change depending on the storage connector type, but broadly they could be classified as below

### Data lake/object based connectors

For data sources based on object/file storage such as AWS S3, ADLS, GCS, we set the full object path in the `path` argument
and users should pass a Spark data format (parquet, csv, orc, hudi, delta) to the `data_format` argument.

=== "PySpark"
    ```python
    # read data into dataframe using path
    df = connector.read(data_format='data_format', path='fileScheme://bucket/path/')
    ```

=== "Scala"
    ```scala
    // read data into dataframe using path
    val df = connector.read("", "data_format", new HashMap(), "fileScheme://bucket/path/")
    ```

#### Prepare Spark API

Additionally, for reading file based data sources, another way to read the data is using the `prepare_spark` method. This method
can be used if you are reading the data directly through Spark.

Firstly, it handles the setup of all Spark configurations or properties necessary for a particular type of connector and
prepares the absolute path to read from, along with bucket name and the appropriate file scheme of the data source. A Spark session can handle only one configuration setup at a time, so HSFS cannot set the Spark configurations when retrieving the connector since it would lead to only always initialising the last connector being retrieved.
Instead, user can do this setup explicitly with the `prepare_spark` method and therefore potentially
use multiple connectors in one Spark session. `prepare_spark` handles only one bucket associated with that particular connector, however, it is possible to set up multiple connectors with different types as long as their Spark properties do not interfere with each other.
So, for example a S3 connector and a Snowflake connector can be used in the same session, without calling `prepare_spark` multiple times, as the properties don’t interfere with each other.

If the storage connector is used in another API call, `prepare_spark` gets implicitly invoked, for example,
when a user materialises a training dataset using a storage connector or uses the storage connector to set up an External Feature Group.
So users do not need to call `prepare_spark` every time they do an operation with a connector, it is only necessary when reading directly using Spark . Using `prepare_spark` is also
not necessary when using the `read` API.

For example, to read directly from a S3 connector, we use the `prepare_spark` as follows

=== "PySpark"
    ```python
    connector.prepare_spark()
    spark.read.format("json").load("s3a://[bucket]/path")
    # or
    spark.read.format("json").load(connector.prepare_spark("s3a://[bucket]/path"))
    ```

### Data warehouse/SQL based connectors

For data sources accessed via SQL such as data warehouses and JDBC compliant databases, e.g. Redshift, Snowflake, BigQuery, JDBC, users pass the SQL query to read the data to the `query`
argument. In most cases, this will be some form of a `SELECT` query. Depending on the connector type, users can also just set the table path and read the whole table without explicitly
passing any SQL query to the `query` argument. This is mostly relevant for Google BigQuery.

=== "PySpark"
    ```python
    # read results from a SQL
    df = connector.read(query="SELECT * FROM TABLE")
    # or directly read a table if set on connector
    df = connector.read()
    ```

=== "Scala"
    ```scala
    // read results from a SQL
    val df = connector.read("SELECT * FROM TABLE", "" , new HashMap(),"")
    ```

### Streaming based connector

For reading data streams, the Kafka Storage Connector supports reading a Kafka topic into Spark Structured Streaming Dataframes
instead of a static Dataframe as in other connector types.

=== "PySpark"

    ```python
    df = connector.read_stream(topic='kafka_topic_name')
    ```

## Creating an External Feature Group

Another important aspect of a storage connector is its ability to facilitate creation of external feature groups with
the [Connector API](../../../concepts/fs/feature_group/external_fg.md). [External feature groups](../feature_group/create_external.md) are basically offline feature groups
and essentially stored as tables on external data sources.
The `Connector API` relies on storage connectors behind the scenes to integrate with external datasource.
This enables seamless integration with any data source as long as there is a storage connector defined.

To create an external feature group, we use the `create_external_feature_group` API, also known as `Connector API`,
and simply pass the storage connector created before to the `storage_connector` argument.
Depending on the external data source, we should set either the `query` argument for data warehouse based data sources, or
the `path` and `data_format` arguments for data lake based sources, similar to reading into dataframes as explained in above section.

Example for any data warehouse/SQL based external sources, we set the desired SQL to `query` argument, and set the `storage_connector`
argument to the storage connector object of desired data source.
=== "PySpark"
    ```python
    fg = feature_store.create_external_feature_group(name="sales",
        version=1
        description="Physical shop sales features",
        query="SELECT * FROM TABLE",
        storage_connector=connector,
        primary_key=['ss_store_sk'],
        event_time='sale_date'
    )
    ```

`Connector API` (external feature groups) only stores the metadata about the features within Hopsworks,
while the actual data is still stored externally. This enables users to create feature groups within Hopsworks without the hassle of data migration.
For more information on `Connector API`, read detailed guide about [external feature groups](../feature_group/create_external.md).

## Writing Training Data

Storage connectors are also used while writing training data to external sources. While calling the
[Feature View](../../../concepts/fs/feature_view/fv_overview.md) API `create_training_data` , we can pass the `storage_connector` argument which is necessary to materialise
the data to external sources, as shown below.

=== "PySpark"
    ```python
    # materialise a training dataset
    version, job = feature_view.create_training_data(
        description = 'describe training data',
        data_format = 'spark_data_format', # e.g. data_format = "parquet" or data_format = "csv"
        write_options = {"wait_for_job": False},
        storage_connector = connector
    )
    ```

Read more about training data creation [here](../feature_view/training-data.md).

## Next Steps
We have gone through the basic use cases of a storage connector.
For more details about the API functionality for any specific connector type,
checkout the [API section](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/api/storage_connector_api/#storage-connector).

