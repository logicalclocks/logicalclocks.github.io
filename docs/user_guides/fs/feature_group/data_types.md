# How to manage schema and feature data types 

### Introduction

In this guide you will learn how to manage the feature group schema and control the data type of the features in a feature group.

## Prerequisites

Before you begin this guide we suggest you read the [Feature Group](../../../concepts/fs/feature_group/fg_overview.md) concept page to understand what a feature group is and how it fits in the ML pipeline. 
We also suggest you familiarize with the APIs to [create a feature group](./create.md).

## Feature group schema 

When a feature is stored in the both the online and offline feature stores, it will be stored in a data type native to each store.

* **Offline data type**: The data type of the feature when stored on the offline feature store
* **Online data type**: The data type of the feature when stored on the online feature store.

The offline data type is always required, even if the feature group is stored only online. On the other hand, if the feature group is not *online_enabled*, its features will not have an online data type.

The offline and online types for each feature are identified based on the types of the columns in the Spark or Pandas DataFrame, and those types are then mapped to the online and offline data types.

In the case of a Spark DataFrame, the [Spark types](https://spark.apache.org/docs/latest/sql-ref-datatypes.html) will be mapped to the corresponding Hive Metastore type and used as offline data type. 

When registering a [Pandas](https://pandas.pydata.org/) DataFrame as a feature group, the following mapping rules are applied:

| Pandas Type        | Offline Feature Type|
| ------------------ | ------------------- |
| int32              | INT                 |
| int64              | BIGINT              |
| float32            | FLOAT               |
| float64            | DOUBLE              |
| datetime64[ns]     | TIMESTAMP           
| object             | STRING              |

If the feature group is online enabled, Hopsworks will then map the offline data type to the corresponding online data type. The mapping is based on the following rules:

* If the offline data type is also supported on the online feature store (e.g. INT, FLOAT, DATE, TIMESTAMP), the online data type will be the same as the offline data type
* If the offline data type is *boolean*, the online data type is going to be set as *tinyint*
* If the offline data type is *string*, the online data type is going to be set as *varchar(100)*
* If the offline data type is not supported by the online feature store and it is not one of the above exception, the online data type will be set as *varbinary(100)* to handle complex types.

### Offline data types

The offline feature store is based on Apache Hudi and Hive Metastore, as such, any
[Hive Data Type](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+Types)
can be leveraged.

Potential *offline* types are:

```SQL
"TINYINT", "SMALLINT", "INT", "BIGINT", "FLOAT", "DOUBLE",
"DECIMAL", "TIMESTAMP", "DATE", "STRING", "BOOLEAN", "BINARY",
"ARRAY <TINYINT>", "ARRAY <SMALLINT>", "ARRAY <INT>", "ARRAY <BIGINT>",
"ARRAY <FLOAT>", "ARRAY <DOUBLE>", "ARRAY <DECIMAL>", "ARRAY <TIMESTAMP>",
"ARRAY <DATE>", "ARRAY <STRING>",
"ARRAY <BOOLEAN>", "ARRAY <BINARY>", "ARRAY <ARRAY <FLOAT> >",
"ARRAY <ARRAY <INT> >", "ARRAY <ARRAY <STRING> >",
"MAP <FLOAT, FLOAT>", "MAP <FLOAT, STRING>", "MAP <FLOAT, INT>",
"MAP <FLOAT, BINARY>", "MAP <INT, INT>", "MAP <INT, STRING>",
"MAP <INT, BINARY>", "MAP <INT, FLOAT>", "MAP <INT, ARRAY <FLOAT> >",
"STRUCT < label: STRING, index: INT >", "UNIONTYPE < STRING, INT>"
```

### Online data types

The online storage is based on RonDB and hence, any
[MySQL Data Type](https://dev.mysql.com/doc/refman/8.0/en/data-types.html)
can be leveraged.

Potential *online* types are:

```SQL
"None", "INT(11)", "TINYINT(1)", "SMALLINT(5)", "MEDIUMINT(7)", "BIGINT(20)",
"FLOAT", "DOUBLE", "DECIMAL", "DATE", "DATETIME", "TIMESTAMP", "TIME", "YEAR",
"CHAR", "VARCHAR(n)", "BINARY", "VARBINARY(n)", "BLOB", "TEXT", "TINYBLOB",
"TINYTEXT", "MEDIUMBLOB", "MEDIUMTEXT", "LONGBLOB", "LONGTEXT", "JSON"
```

#### Complex online data types

Additionally to the *online* types above, Hopsworks allows users to store complex types (e.g. *ARRAY<INT>*) on the online feature store.
Hopsworks serializes the complex features transparently and stores them as VARBINARY in the online feature store. The serialization happens when calling the [save()](https://docs.hopsworks.ai/feature-store-api/3.0/generated/api/feature_group_api/#save), [insert()](https://docs.hopsworks.ai/feature-store-api/3.0/generated/api/feature_group_api/#insert) or [insert_stream()](https://docs.hopsworks.ai/feature-store-api/3.0/generated/api/feature_group_api/#insert_stream) methods. The deserialization will be executed when calling the [get_serving_vector()](https://docs.hopsworks.ai/feature-store-api/3.0/generated/api/training_dataset_api/#get_serving_vector) method to retrieve data from the online feature store.
If users query directly the online feature store, for instance using the `fs.sql("SELECT ...", online=True)` statement, it will return a binary blob.

On the feature store UI, the online feature type for complex features will be reported as *VARBINARY*.

#### Online restrictions for primary key data types:

When a feature is being used as a primary key, certain types are not allowed. Examples of such types are *Float*, *Double*, *Date*, *Text*, *Blob* and *Complex Types*  (e.g. Array<>). Additionally the size of the sum of the primary key online data types storage requirements should not exceed 3KB.

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

Hopsworks supports appending additional features to an existing feature group. Adding a additional features to an existing feature group is not considered a breaking change.

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