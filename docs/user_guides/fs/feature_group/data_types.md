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
or a [Pandas](https://pandas.pydata.org/) DataFrame, or a [Polars](https://pola.rs/) DataFrame in a Python-only environment (P) the following default mapping to offline feature types applies:

| Spark Type (S) | Pandas Type (P)                    |Polars Type (P)                    | Offline Feature Type          | Remarks                                                        |
|----------------|------------------------------------|-----------------------------------|-------------------------------|----------------------------------------------------------------|
| BooleanType    | bool, object(bool)                 |Boolean                            | BOOLEAN                       |                                                                |
| ByteType       | int8, Int8                         |Int8                               | TINYINT or INT                | INT when time_travel_type="HUDI"                               |
| ShortType      | uint8, int16, Int16                |UInt8, Int16                       | SMALLINT or INT               | INT when time_travel_type="HUDI"                               |
| IntegerType    | uint16, int32, Int32               |UInt16, Int32                      | INT                           |                                                                |
| LongType       | int, uint32, int64, Int64          |UInt32, Int64                      | BIGINT                        |                                                                |
| FloatType      | float, float16, float32            |Float32                            | FLOAT                         |                                                                |
| DoubleType     | float64                            |Float64                            | DOUBLE                        |                                                                |
| DecimalType    | decimal.decimal                    |Decimal                            | DECIMAL(PREC, SCALE)          | Not supported in PO env. when time_travel_type="HUDI"          |
| TimestampType  | datetime64[ns], datetime64[ns, tz] |Datetime                           | TIMESTAMP                     | s. [Timestamps and Timezones](#timestamps-and-timezones)       |
| DateType       | object (datetime.date)             |Date                               | DATE                          |                                                                |
| StringType     | object (str), object(np.unicode)   |String, Utf8                       | STRING                        |                                                                |
| ArrayType      | object (list), object (np.ndarray) |List                               | ARRAY&lt;TYPE&gt;             |                                                                |
| StructType     | object (dict)                      |Struct                             | STRUCT&lt;NAME: TYPE, ...&gt; |                                                                |
| BinaryType     | object (binary)                    |Binary                             | BINARY                        |                                                                |
| MapType        | -                                  |-                                  | MAP&lt;String,TYPE&gt;        | Only when time_travel_type!="HUDI"; Only string keys permitted |

When registering a Pandas DataFrame in a PySpark environment (S) the Pandas DataFrame is first converted to a Spark DataFrame, using Spark's [default conversion](https://spark.apache.org/docs/3.1.1/api/python/reference/api/pyspark.sql.SparkSession.createDataFrame.html).
It results in a less fine-grained mapping between Python and Spark types:

| Pandas Type (S)                                       | Spark Type    | Remarks                                                  |
|-------------------------------------------------------|---------------|----------------------------------------------------------|
| bool                                                  | BooleanType   |                                                          |
| int8, uint8, int16, uint16, int32, int, uint32, int64 | LongType      |                                                          |
| float, float16, float32, float64                      | DoubleType    |                                                          |
| object (decimal.decimal)                              | DecimalType   |                                                          |
| datetime64[ns], datetime64[ns, tz]                    | TimestampType | s. [Timestamps and Timezones](#timestamps-and-timezones) |
| object (datetime.date)                                | DateType      |                                                          |
| object (str), object(np.unicode)                      | StringType    |                                                          |
| object (list), object (np.ndarray)                    | -             | Not supported                                            |
| object (dict)                                         | StructType    |                                                          |
| object (binary)                                       | BinaryType    |                                                          |

### Online data types

The online data type is determined based on the offline type according to the following mapping, regardless of which environment the data originated from.
Only a subset of the data types can be used as primary key, as indicated in the table as well:

| Offline Feature Type          | Online Feature Type  | Primary Key | Remarks                                                  |
|-------------------------------|----------------------|-------------|----------------------------------------------------------|
| BOOLEAN                       | TINYINT              | x           |                                                          |
| TINYINT                       | TINYINT              | x           |                                                          |
| SMALLINT                      | SMALLINT             | x           |                                                          |
| INT                           | INT                  | x           | Also supports: TINYINT, SMALLINT                         |
| BIGINT                        | BIGINT               | x           |                                                          |
| FLOAT                         | FLOAT                |             |                                                          |
| DOUBLE                        | DOUBLE               |             |                                                          |
| DECIMAL(PREC, SCALE)          | DECIMAL(PREC, SCALE) |             | e.g. DECIMAL(38, 18)                                     |
| TIMESTAMP                     | TIMESTAMP            |             | s. [Timestamps and Timezones](#timestamps-and-timezones) |
| DATE                          | DATE                 | x           |                                                          |
| STRING                        | VARCHAR(100)         | x           | Also supports: TEXT                                      |
| ARRAY&lt;TYPE&gt;             | VARBINARY(100)       | x           | Also supports: BLOB                                      |
| STRUCT&lt;NAME: TYPE, ...&gt; | VARBINARY(100)       | x           | Also supports: BLOB                                      |
| BINARY                        | VARBINARY(100)       | x           | Also supports: BLOB                                      |
| MAP&lt;String,TYPE&gt;        | VARBINARY(100)       | x           | Also supports: BLOB                                      |

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
The serialization happens when calling the [save()](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/api/feature_group_api/#save),
[insert()](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/api/feature_group_api/#insert) or [insert_stream()](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/api/feature_group_api/#insert_stream) methods.
The deserialization will be executed when calling the [get_serving_vector()](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/api/training_dataset_api/#get_serving_vector) method to retrieve data from the online feature store.
If users query directly the online feature store, for instance using the `fs.sql("SELECT ...", online=True)` statement, it will return a binary blob.

On the feature store UI, the online feature type for complex features will be reported as *VARBINARY*.

If the binary size exceeds 100 bytes, a larger type (e.g. VARBINARY(500)) can be specified via an [explicit schema definition](#explicit-schema-definition).
If the binary size is unknown of if it exceeds the maximum row size, then the [BLOB type](https://docs.rondb.com/blobs/) can be used instead.

Binary data that exceeds the specified VARBINARY size will lead to an error when data gets written to the online feature store.
When in doubt, use the BLOB type instead, but note that it comes with a potential performance overhead.

#### Online restrictions for primary key data types

When a feature is being used as a primary key, certain types are not allowed.
Examples of such types are *FLOAT*, *DOUBLE*, *TEXT* and *BLOB*.
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


#### Pre-insert schema validation for online feature groups

The input dataframe can be validated for schema as per the valid online schema data types before online ingestion. The most important checks are mentioned below along with possible corrective actions. It is enabled by setting the keyword argument `validation_options={'run_validation':True}` in the `insert()` API of feature groups.



| Error type                    | Requirement                                                                                                                                                                                                                                             | Suggested corrections                                                   |
|-------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|
| Primary key contains null values       | Primary key column should not cannot any null values. If the primary key is composite key then all columns of primary key are checked for null.                                                                                                                       | Remove the null rows from dataframe. OR impute the null values as applicable. |
| Primary key column is missing | The dataframe to be inserted must contain all the features of the defined the primary key as per the feature group schema.                                                                                                                              | Add all the primary key columns in the dataframe.                             |
| Event time column is missing  | The dataframe to be inserted must contain an event time column if it was specified in the schema while feature group creation.                                                                                                                          | Add the event time column in the dataframe.                                   |
| String length exceeded        | The character length of a string row exceeds the maximum length specified in feature online schema. However, if the feature group is not created and if no explicit schema was provided during feature group creation, then the length will be auto-increased to the maximum length found in a string column. This is handled during the first data ingestion and no user action is needed in this case. **Note:** The maximum row size in bytes should be less than 30000. | Trim the string values to fit within maximum set during feature group creation. OR remove the invalid rows. If the lengths are very long consider changing the feature schema to **TEXT** or **BLOB.**            |


### Timestamps and Timezones

All timestamp features are stored in Hopsworks in UTC time. Also, all timestamp-based functions (such as [point-in-time joins](../../../concepts/fs/feature_view/offline_api.md#point-in-time-correct-training-data)) use UTC time.
This ensures consistency of timestamp features across different client timezones and simplifies working with timestamp-based functions in general.
When ingesting timestamp features, the [Feature Store Write API](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/api/feature_group_api/#insert) will automatically handle the conversion to UTC, if necessary.
The following table summarizes how different timestamp types are handled:

| Data Frame (Data Type)                | Environment             | Handling                                                 |
|---------------------------------------|-------------------------|----------------------------------------------------------|
| Pandas DataFrame (datetime64[ns])     | Python-only and PySpark | interpreted as UTC, independent of the client's timezone |
| Pandas DataFrame (datetime64[ns, tz]) | Python-only and PySpark | timezone-sensitive conversion from 'tz' to UTC            |
| Spark (TimestampType)                 | PySpark and Spark       | interpreted as UTC, independent of the client's timezone |

Timestamp features retrieved from the Feature Store, e.g. using the [Feature Store Read API](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/api/feature_group_api/#read), use a timezone-unaware format:

| Data Frame (Data Type)                | Environment             | Timezone               |
|---------------------------------------|-------------------------|------------------------|
| Pandas DataFrame (datetime64[ns])     | Python-only             | timezone-unaware (UTC) |
| Spark (TimestampType)                 | PySpark and Spark       | timezone-unaware (UTC) |

Note that our PySpark/Spark client automatically sets the Spark SQL session's timezone to UTC. This ensures that Spark SQL will correctly interpret all timestamps as UTC. The setting will only apply to the client's session, and you don't have to worry about setting/unsetting the configuration yourself.

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
    fg.save(features)
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
