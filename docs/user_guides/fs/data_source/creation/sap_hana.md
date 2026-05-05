# How-To set up a SAP HANA Data Source

## Introduction

SAP HANA is an in-memory relational database used by many enterprises as the system of record for ERP, CRM, and analytics workloads.

A SAP HANA Data Source in Hopsworks stores the connection details required to read tables and views from a HANA tenant database.
Once configured, you can use the same data source as the basis for an external (on-demand) Feature Group, or as the source for a dltHub-driven ingestion job that materialises HANA data into a managed Feature Group.

In this guide, you will configure a Data Source in Hopsworks that holds the authentication information needed to connect to your SAP HANA database.

!!! note
    Currently, it is only possible to create data sources in the Hopsworks UI.
    You cannot create a data source programmatically.

## Prerequisites

Before you begin this guide you'll need to retrieve the following information from your SAP HANA tenant.
The following options are **mandatory**:

- **Host**: The hostname of the SAP HANA endpoint, for example `hxehost.example.com` for an on-premise instance or the endpoint shown in SAP BTP for SAP HANA Cloud.
- **Port**: The SQL port of the tenant database.
The default is `39015`, the SQL port for the first tenant database on a default
multi-tenant or HANA Express (HXE) install (instance number 90).
For a non-tenant single-host install (instance 00) use `30015`.
SAP HANA Cloud typically uses `443`.
Consult your DBA if you are unsure.
- **User**: The HANA database user that the connector authenticates as.
- **Password**: The password for that user.

These are a few additional **optional** arguments:

- **Database**: The tenant database name.
Use this when your SAP HANA system hosts more than one tenant database and you need to target a specific one.
- **Schema**: The default schema applied to unqualified queries on the connection.
If you leave this empty, queries must fully qualify table names with the schema prefix.
- **Table**: The default table the connector points at when no SQL query is provided.
- **Application**: A short identifier surfaced in HANA's session tracing (`APPLICATION` session variable).
This makes it easier to attribute load to Hopsworks in HANA monitoring tools.
- **Additional arguments**: Free-form key/value options forwarded to the underlying SAP HANA Python driver (`hdbcli`) and the Spark JDBC reader.

!!! note "Authentication"
    The SAP HANA data source currently supports username and password authentication.
    Certificate-based and JWT authentication are tracked as follow-up work.

!!! info "Drivers"
    Hopsworks ships the SAP HANA drivers needed to read from HANA out of the box.
    The Hopsworks Spark image bundles the SAP `ngdbc` JDBC driver for Spark JDBC reads, and the dlt ingestion image and Arrow Flight server bundle SAP's `hdbcli` Python DBAPI driver.
    You do not need to install or upload the drivers yourself.

## Creation in the UI

### Step 1: Set up new Data Source

Head to the Data Source View on Hopsworks and start the creation flow for a new data source.

<figure markdown>
  ![Data Source Creation](../../../../assets/images/guides/fs/data_source/data_source_overview.png)
  <figcaption>The Data Source View in the User Interface</figcaption>
</figure>

### Step 2: Enter SAP HANA Settings

Enter the details for your SAP HANA connector.
Start by giving it a **name** and an optional **description**.

01. Select "SAP HANA" as storage.
02. Specify the **Host** of your SAP HANA endpoint.
03. Specify the **Port** the tenant SQL service listens on (default `39015`).
04. Provide the **User** name of the HANA database user.
05. Provide the **Password** for that user.
06. Optionally fill in **Database**, **Schema**, **Table**, and **Application**.
07. Optionally add additional key/value arguments.
These are forwarded both to the Python driver used by the on-demand read path and to the Spark JDBC reader used by notebook jobs.
08. Click on "Save Credentials".

## Use it as an ingestion source

Once the SAP HANA data source exists, you can also use it with the dltHub-based ingestion workflow described in [Ingest Data with dltHub](../../feature_group/ingest_with_dlthub.md).
SAP HANA is treated as a SQL-like source, so the ingestion job supports both full and incremental loading.

## Next Steps

Move on to the [usage guide for data sources](../usage.md) to see how you can use your newly created SAP HANA connector.
