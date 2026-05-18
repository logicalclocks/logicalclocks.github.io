# How-To set up a MongoDB Data Source { #data-source-mongodb }

## Introduction

MongoDB is a document database widely used as the operational store behind web and mobile applications.
Documents are stored in collections and grouped into databases on a MongoDB server or Atlas cluster.

A MongoDB Data Source in Hopsworks stores the connection details required to read collections from a MongoDB deployment.
Once configured, you can use the same data source as the basis for an external (on-demand) Feature Group, or as the source for a dltHub-driven ingestion job that materialises MongoDB documents into a managed Feature Group.

In this guide, you will configure a Data Source in Hopsworks that holds the authentication information needed to connect to your MongoDB deployment.

!!! note
    Currently, it is only possible to create data sources in the Hopsworks UI.
    You cannot create a data source programmatically.

## Prerequisites

Before you begin this guide you'll need to retrieve the following information from your MongoDB deployment (self-hosted or Atlas).
The following options are **mandatory**:

- **Connection String**: The MongoDB connection URI without embedded credentials, for example `mongodb+srv://my-cluster.abcde.mongodb.net` for an Atlas cluster or `mongodb://mongo.example.com:27017` for a self-hosted deployment.
    The username and password live in separate fields so the URI itself can be checked into project metadata without leaking credentials.
- **User**: The MongoDB user the connector authenticates as.
- **Password**: The password for that user.

These are a few additional **optional** arguments:

- **Database**: The default database the connector points at when no database is explicitly selected.
    The picker can target any database the user has access to, regardless of this default.
- **Collection**: The default collection used when no collection is provided at read time.
- **Auth Source**: The authentication database for the user (typically `admin`).
    Required when the user is created in a database other than the one being read from — typical for Atlas.
- **Auth Mechanism**: The MongoDB authentication mechanism, e.g. `SCRAM-SHA-256`.
    Leave empty to let the server negotiate the default.

!!! info "Drivers"
    Hopsworks ships the MongoDB drivers needed to read from MongoDB out of the box.
    The Hopsworks Spark image bundles the `mongo-spark-connector` for Spark reads, and the dlt ingestion image and Arrow Flight server bundle `pymongo` for the on-demand read path.
    You do not need to install or upload the drivers yourself.

## Creation in the UI

### Step 1: Set up new Data Source

Head to the Data Source View on Hopsworks and start the creation flow for a new data source.

<figure markdown>
  ![Data Source Creation](../../../../assets/images/guides/fs/data_source/data_source_overview.png)
  <figcaption>The Data Source View in the User Interface</figcaption>
</figure>

### Step 2: Enter MongoDB Settings

Enter the details for your MongoDB connector.
Start by giving it a **name** and an optional **description**.

01. Select "MongoDB" as storage.
02. Specify the **Connection String** of your MongoDB cluster.
03. Provide the **User** name of the MongoDB database user.
04. Provide the **Password** for that user.
05. Optionally set a default **Database** and **Collection**.
06. Optionally set an **Auth Source** (typically `admin` for Atlas) and an **Auth Mechanism**.
07. Click on "Save Credentials".

## Use it as an ingestion source

Once the MongoDB data source exists, you can use it with the dltHub-based ingestion workflow described in [Ingest Data with dltHub][ingest-data-with-dlthub].
MongoDB is treated as a NoSQL document source, so the ingestion job runs a `pymongo` aggregation pipeline against the chosen collection and materialises the result into a managed Feature Group.

## Type mapping

MongoDB collections are schemaless: documents in the same collection can have different fields and different types per field.
When you browse a collection in the data source picker, Hopsworks samples a small batch of documents and infers a per-field type by classifying each observed value and applying promotion rules — `int + float → float`, `date + timestamp → timestamp`, `list` or nested document → `string` (JSON).
The inferred types are then projected to Hopsworks offline feature types using the table below.

| Python value type (Compass-style) | Hopsworks offline feature type |
| --- | --- |
| `int` | `bigint` |
| `float` | `double` |
| `Decimal128` | `decimal(38,18)` |
| `bool` | `boolean` |
| `datetime` | `timestamp` |
| `date` | `date` |
| `ObjectId` / `str` / `UUID` | `string` |
| `bytes` / `Binary` | `binary` |
| `list` / nested `dict` | `string` (JSON-encoded) |

You can also override the inferred type for any column in the Feature Group creation form.

## Known limitations

### Schemaless collections

The picker's schema inference walks a sampled batch of documents, not the full collection.
If a rare field type appears only in documents outside the sample, it may not be reflected in the inferred Feature Group schema.
You can override or extend the schema in the Feature Group creation form before saving.

### Nested documents and arrays

Nested documents and arrays are read as JSON-encoded `string` features.
If you need to expose nested fields as individual features, project them out at the source by writing a custom aggregation pipeline as the data source `query`.

### Online ingestion requires non-null primary keys

When you create a managed Feature Group fed from MongoDB via DLT and enable online serving, online ingestion validates that every row has a non-null value in the Feature Group's primary-key column.
If the source documents can carry `null` (or omit the field entirely) in that column, either filter them out at source, pick a different primary key on the Feature Group, or disable online serving for the Feature Group.

### `_id` is renamed

MongoDB's reserved `_id` field starts with an underscore, which Hopsworks' feature-name rule (`^[a-z][a-z0-9_]*$`) does not accept.
The data-source flow surfaces it as the feature `id` by default; you can rename it in the Feature Group creation form before saving.

## Next Steps

Move on to the [usage guide for data sources][data-source-usage] to see how you can use your newly created MongoDB connector.
