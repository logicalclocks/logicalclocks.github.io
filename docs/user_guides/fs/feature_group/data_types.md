# How to manage schema and feature data types 

### Introduction

In this guide, you will learn how to manage the feature group schema and control the data type of the features in a feature group.

## Prerequisites

Before you begin this guide we suggest you read the [Feature Group](../../../concepts/fs/feature_group/fg_overview.md) concept page to understand what a feature group is and how it fits in the ML pipeline. 
We also suggest you familiarize yourself with the APIs to [create a feature group](./create.md).

## Feature group schema 

When a feature is stored in both the online and offline feature stores, it will be stored in a data type native to each store.

* **[Offline data type](#offline-data-types)**: The data type of the feature when stored on the offline feature store. The offline feature store is based on Apache Hudi and Hive Metastore, as such,
  [Hive Data Types](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+Types) can be leveraged.
* **[Online data type](#online-data-types)**: The data type of the feature when stored on the online feature store. The online storage is based on RonDB and hence,
  [MySQL Data Types](https://dev.mysql.com/doc/refman/8.0/en/data-types.html) can be leveraged. 

The offline data type is always required, even if the feature group is stored only online. On the other hand, if the feature group is not *online_enabled*, its features will not have an online data type.

The offline and online types for each feature are automatically inferred from the Spark or Pandas types of the input DataFrame as outlined in the following two sections.
The default mapping, however, can be overwritten by using an [explicit schema definition](#explicit-schema-definition).

### Offline data types 

When registering a [Spark](https://spark.apache.org/docs/latest/sql-ref-datatypes.html) DataFrame in a PySpark environment (S),
or a [Pandas](https://pandas.pydata.org/) DataFrame in a Python-only environment (P) the following default mapping to offline feature types applies:

| Spark Type (S) | Pandas Type (P)                    | Offline Feature Type          | Remarks                                                        |
|----------------|------------------------------------|-------------------------------|----------------------------------------------------------------|
| BooleanType    | bool                               | BOOLEAN                       |                                                                |
| ByteType       | int8                               | TINYINT or INT                | INT when time_travel_type="HUDI"                               |
| ShortType      | uint8, int16                       | SMALLINT or INT               | INT when time_travel_type="HUDI"                               |
| IntegerType    | uint16, int32                      | INT                           |                                                                |
| LongType       | int, uint32, int64                 | BIGINT                        |                                                                |
| FloatType      | float, float16, float32            | FLOAT                         |                                                                |
| DoubleType     | float64                            | DOUBLE                        |                                                                |
| DecimalType    | decimal.decimal                    | DECIMAL(PREC, SCALE)          | Not supported in PO env. when time_travel_type="HUDI"          |
| TimestampType  | datetime64[ns], datetime64[ns, tz] | TIMESTAMP                     |                                                                |
| DateType       | object (datetime.date)             | DATE                          |                                                                |
| StringType     | object (str), object(np.unicode)   | STRING                        |                                                                |
| ArrayType      | object (list), object (np.ndarray) | ARRAY&lt;TYPE&gt;             |                                                                |
| StructType     | object (dict)                      | STRUCT&lt;NAME: TYPE, ...&gt; |                                                                |
| BinaryType     | object (binary)                    | BINARY                        |                                                                |
| MapType        | -                                  | MAP&lt;String,TYPE&gt;        | Only when time_travel_type!="HUDI"; Only string keys permitted |

When registering a Pandas DataFrame in a PySpark environment (S) the Pandas DataFrame is first converted to a Spark DataFrame, using Spark's [default conversion](https://spark.apache.org/docs/3.1.1/api/python/reference/api/pyspark.sql.SparkSession.createDataFrame.html).
It results in a less fine-grained mapping between Python and Spark types:

| Pandas Type (S)                                       | Spark Type    | Remarks       |
|-------------------------------------------------------|---------------|---------------|
| bool                                                  | BooleanType   |               |
| int8, uint8, int16, uint16, int32, int, uint32, int64 | LongType      |               |
| float, float16, float32, float64                      | DoubleType    |               |
| object (decimal.decimal)                              | DecimalType   |               |
| datetime64[ns], datetime64[ns, tz]                    | TimestampType |               |
| object (datetime.date)                                | DateType      |               |
| object (str), object(np.unicode)                      | StringType    |               |
| object (list), object (np.ndarray)                    | -             | Not supported |
| object (dict)                                         | StructType    |               |
| object (binary)                                       | BinaryType    |               |

### Online data types 

The online data type is determined based on the offline type according to the following mapping, regardless of which environment the data originated from. 
Only a subset of the data types can be used as primary key, as indicated in the table as well:

| Offline Feature Type          | Online Feature Type  | Primary Key | Remarks                          | 
|-------------------------------|----------------------|-------------|----------------------------------|
| BOOLEAN                       | TINYINT              | x           |                                  | 
| TINYINT                       | TINYINT              | x           |                                  | 
| SMALLINT                      | SMALLINT             | x           |                                  | 
| INT                           | INT                  | x           | Also supports: TINYINT, SMALLINT | 
| BIGINT                        | BIGINT               | x           |                                  | 
| FLOAT                         | FLOAT                |             |                                  | 
| DOUBLE                        | DOUBLE               |             |                                  | 
| DECIMAL(PREC, SCALE)          | DECIMAL(PREC, SCALE) |             | e.g. DECIMAL(38, 18)             | 
| TIMESTAMP                     | TIMESTAMP            |             |                                  | 
| DATE                          | DATE                 |             |                                  | 
| STRING                        | VARCHAR(100)         | x           | Also supports: TEXT              | 
| ARRAY&lt;TYPE&gt;             | VARBINARY(100)       | x           | Also supports: BLOB              | 
| STRUCT&lt;NAME: TYPE, ...&gt; | VARBINARY(100)       | x           | Also supports: BLOB              | 
| BINARY                        | VARBINARY(100)       | x           | Also supports: BLOB              | 
| MAP&lt;String,TYPE&gt;        | VARBINARY(100)       | x           | Also supports: BLOB              | 

More on how Hopsworks handles [string types](#string-online-data-types),  [complex data types](#complex-online-data-types) and the online restrictions for [primary keys](#online-restrictions-for-primary-key-data-types) and [row size](#online-restrictions-for-row-size) in the following sections.

#### String online data types

String types are stored as *VARCHAR(100)* by default. This type is fixed-size, meaning it can only hold as many characters as specified in the argument (e.g. VARCHAR(100) can hold up to 100 unicode characters).
The size should thus be within the maximum string length of the input data. Furthermore, the VARCHAR size has to be in line with the [online restrictions for row size](#online-restrictions-for-row-size).

If the string size exceeds 100 characters, a larger type (e.g. VARCHAR(500)) can be specified via an [explicit schema definition](#explicit-schema-definition). 
If the string size is unknown or if it exceeds the maximum row size, then the [TEXT type](https://docs.rondb.com/blobs/) can be used instead.

String data that exceeds the specified VARCHAR size will lead to an error when data gets written to the online feature store.
When in doubt, use the TEXT type instead, but note that it comes with a potential performance overhead.

#### Complex online data types

Hopsworks allows users to store complex types (e.g. *ARRAY<INT>*) in the online feature store. Hopsworks serializes the complex features transparently and stores them as VARBINARY in the online feature store.
The serialization happens when calling the [save()](https://docs.hopsworks.ai/feature-store-api/3.0/generated/api/feature_group_api/#save), 
[insert()](https://docs.hopsworks.ai/feature-store-api/3.0/generated/api/feature_group_api/#insert) or [insert_stream()](https://docs.hopsworks.ai/feature-store-api/3.0/generated/api/feature_group_api/#insert_stream) methods. 
The deserialization will be executed when calling the [get_serving_vector()](https://docs.hopsworks.ai/feature-store-api/3.0/generated/api/training_dataset_api/#get_serving_vector) method to retrieve data from the online feature store.
If users query directly the online feature store, for instance using the `fs.sql("SELECT ...", online=True)` statement, it will return a binary blob. 

On the feature store UI, the online feature type for complex features will be reported as *VARBINARY*.

If the binary size exceeds 100 bytes, a larger type (e.g. VARBINARY(500)) can be specified via an [explicit schema definition](#explicit-schema-definition).
If the binary size is unknown of if it exceeds the maximum row size, then the [BLOB type](https://docs.rondb.com/blobs/) can be used instead.

Binary data that exceeds the specified VARBINARY size will lead to an error when data gets written to the online feature store.
When in doubt, use the BLOB type instead, but note that it comes with a potential performance overhead.

#### Online restrictions for primary key data types

When a feature is being used as a primary key, certain types are not allowed. 
Examples of such types are *FLOAT*, *DOUBLE*, *DATE*, *TEXT* and *BLOB*. 
Additionally, the size of the sum of the primary key online data types storage requirements **should not exceed 4KB**.

#### Online restrictions for row size

The online feature store supports **up to 500 columns** and all column types combined **should not exceed 30000 Bytes**. 
The byte size of each column is determined by its data type and calculated as follows: 

| Online Data Type                | Byte Size    |
|---------------------------------|--------------|
| TINYINT                         | 1            |
| SMALLINT                        | 2            |
| INT                             | 4            |
| BIGINT                          | 8            |
| FLOAT                           | 4            |
| DOUBLE                          | 8            |
| DECIMAL(PREC, SCALE)            | 16           |
| TIMESTAMP                       | 8            |
| DATE                            | 8            |
| VARCHAR(LENGTH)                 | LENGTH * 4   |
| VARCHAR(LENGTH) charset latin1; | LENGTH * 1   |
| TEXT                            | 256          |
| VARBINARY(LENGTH)               | LENGTH / 1.4 |
| BLOB                            | 256          |
| other                           | 8            |

### Timestamps and Timezones

Timestamp features are stored in Hopsworks without an associated time zone. 
All timestamp features and all timestamp-based functions (such as [point-in-time joins](../../../concepts/fs/feature_view/offline_api.md#point-in-time-correct-training-data)) use UTC time. 
This ensures consistency of data across different 
time zones and simplifies working with timestamp data. When ingesting timestamp features,
the [Feature Store Write API](https://docs.hopsworks.ai/feature-store-api/{{{ hopsworks_version }}}/generated/api/feature_group_api/#insert) ensures that timestamps are correctly injected as UTC 
timestamps. Input data is interpreted as follows, independent of the client's time zone:

| Data Frame (Data Type)                | Engines                 | Handling                            |
|---------------------------------------|-------------------------|-------------------------------------|
| Pandas DataFrame (datetime64[ns])     | Python-only and PySpark | interpretation as UTC               |
| Pandas DataFrame (datetime64[ns, tz]) | Python-only and PySpark | timzone-sensitive conversion to UTC |
| Spark (TimestampType)                 | PySpark and Spark       | interpretation as UTC                    |

Data retrieved from the Feature Store, e.g. using the [Feature Store Read API](https://docs.hopsworks.ai/feature-store-api/{{{ hopsworks_version }}}/generated/api/feature_group_api/#read), will always be in UTC time and in the following formats:

| Data Frame (Data Type)                | Engines                 | Timezone |
|---------------------------------------|-------------------------|----------|
| Pandas DataFrame (datetime64[ns])     | Python-only and PySpark | UTC      |
| Spark (TimestampType)                 | PySpark and Spark       | UTC      |

Note that our PySpark/Spark client automatically sets the relevant [Spark SQL session configuration](https://spark.apache.org/docs/latest/configuration.html#runtime-sql-configuration) ("spark.sql.session.timeZone"="UTC"). 
This ensures that Spark SQL will interpret all timestamps as UTC timestamps. The settings will only apply to the current session, and you don't have to worry about setting/unsetting the configuration yourself.

## Explicit schema definition

When creating a feature group it is possible for the user to control both the offline and online data type of each column. If users explicitly define the schema for the feature group, Hopsworks is going to use that schema to create the feature group, without performing any type mapping.
You can explicitly define the feature group schema as follows:

=== "Python"
    ```python
    from hsfs.feature import Feature
    
    features = [
        Feature(name="id",type="int",online_type="int"),
        Feature(name="name",type="string",online_type="varchar(20)")
    ]
    
    fg = fs.create_feature_group(name="fg_manual_schema",
                                 features=features,
                                 online_enabled=True)
    fg.save(df)
    ```

## Append features to existing feature groups 

Hopsworks supports appending additional features to an existing feature group. Adding additional features to an existing feature group is not considered a breaking change.

=== "Python"
    ```python
    from hsfs.feature import Feature
    
    features = [
        Feature(name="id",type="int",online_type="int"),
        Feature(name="name",type="string",online_type="varchar(20)")
    ]
    
    fg = fs.get_feature_group(name="example", version=1)
    fg.append_features(features)
    ```

When adding additional features to a feature group, you can provide a default values for existing entries in the feature group. You can also backfill the new features for existing entries by running an `insert()` operation and update all existing combinations of *primary key* - *event time*. 