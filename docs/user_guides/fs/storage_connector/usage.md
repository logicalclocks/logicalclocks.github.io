# Storage Connector Usage
Here, we look at how to use a storage connector after its created. 
Storage connectors provide an important first step of integrating to an external source.
The 3 fundamental functionalities where storage connectors are used are
    
1. Reading data into spark dataframe
2. Creating an external feature group
3. Writing training data

We look at each case in below sections. 

## Retrieving a Storage Connector
We retrieve a storage connector simply by its unique name.

=== "PySpark"
    ```python
    import hsfs
    # Connect to the Hopsworks feature store
    hsfs_connection = hsfs.connection()
    # Retrieve the metadata handle
    feature_store = hsfs_connection.get_feature_store()
    # Retrieve storage connector
    connector = feature_store.get_storage_connector('connector_name')
    ```

=== "Scala"
    ```scala
    import com.logicalclocks.hsfs._
    val connection = HopsworksConnection.builder().build();
    val featureStore = connection.getFeatureStore();
    // get directly via connector sub-type class e.g. for GCS type
    val connector = featureStore.getGcsConnector("gcs_test")
    ```

## Reading a Spark Dataframe from a Storage Connector

One of the most common usage of a storage connector is to read data directly into a spark dataframe.
Its achieved via the `read` API of the connector object, which hides all the complexity of authentication and integration 
with a data storage source. 
The `read` API primarily has two parameters for specifying the data source, `path` and `query`, depending on the storage connector type.
The exact behaviour could change depending on the storage connector type, but broadly they could be classified as below
### Data lake/object based connectors

For data sources based on object/file storage such as AWS S3, ADLS, GCS, we set the full object path to the `path` argument
and should pass a spark data format to `data_format` argument.

=== "PySpark"
    ```python
    # read data into dataframe using path 
    df = connector.read(data_format='csv',path='path/to/object')   
    ```

=== "Scala"
    ```scala 
    // read data into dataframe using path     
    val df = connector.read("", "csv" , new HashMap(),"gs://bucket/test/")  
    ```
    

### Data warehouse/SQL based connectors

For data sources based on SQL or data warehouses such as Redshift, Snowflake, BigQuery, JDBC, we set a SQL to the `query` 
argument. Depending on the connector type, we can set the table path on connector and read the whole table without explicitly 
passing any SQL to `query` argument, e.g. BigQuery.

=== "PySpark"
    ```python
    # read results from a SQL 
    df = connector.read(query='SQL')    
    # or directly read a table if set on connector
    df = connector.read()
    ```

=== "Scala"
    ```scala 
    // read results from a SQL 
    val df = connector.read("SQL", "csv" , new HashMap(),"")    
    ```

### Streaming based connector

For reading data streams, the Kafka storage connector supports reading a kafka topic into spark streaming dataframe 
instead of a static dataframe as in other connector types.

=== "PySpark"

    ```python
    df = connector.read_stream(topic='kafka_topic_name')
    ```

## Creating an External Feature Group

Another important aspect of a storage connector is its ability to facilitate creation of external feature groups with 
the [Connector API](../../../concepts/fs/feature_group/external_fg.md). [External feature groups](../feature_group/create_external.md)  are basically offline feature groups
and essentially stored as tables on external data sources. 
`Connector API` relies on storage connectors behind the scene to integrate with external datasource.
This enables seamless integration with any data source as long as there is a storage connector defined.

To create an external feature group, we use the `create_on_demand_feature_group` API, also known as `Connector API`, 
and simply pass the storage connector created before to the `storage_connector` argument. 

=== "Python"
    ```python
    fg = feature_store.create_on_demand_feature_group(name="sales",
        version=1
        description="Physical shop sales features",
        data_format="parquet",
        storage_connector=connector,
        primary_key=['ss_store_sk'],
        event_time='sale_date'
    )
    ```


## Writing Training Data

Storage connectors are also used while writing training data to external sources. While calling the 
[Feature View](../../../concepts/fs/feature_view/fv_overview.md) API `create_training_data` , we can pass the `storage_connector` argument which is necessary to materialise 
the data to external sources, as shown below.

=== "Python"

    ```python
    # materialise a training dataset
    version, job = feature_view.create_training_data(
        description = 'transactions_dataset',
        data_format = 'csv',
        write_options = {"wait_for_job": False},
        storage_connector = connector
    ) 
    ```

Read more about training data creation [here](../feature_view/training-data.md)

We have gone through the basic use cases of a storage connector. 
For more details about the API functionality for any specific connector type, 
checkout the [API section](https://docs.hopsworks.ai/feature-store-api/3.1.0-SNAPSHOT/generated/api/storage_connector_api/#storage-connector).

