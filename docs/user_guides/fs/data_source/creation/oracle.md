# How-To set up an Oracle Data Source

## Introduction

Oracle Database is a widely used enterprise relational database management system.
Using the Oracle Data Source, you can query tables and views in your Oracle database directly from Hopsworks, enabling you to build feature engineering pipelines on top of enterprise data.

In this guide, you will configure a Data Source in Hopsworks to securely store the authentication information needed to connect to your Oracle database instance.
When you're finished, you'll be able to query the database using HSFS APIs.

!!! note
    Currently, it is only possible to create data sources in the Hopsworks UI.
    You cannot create a data source programmatically.

## Prerequisites

Before you begin, ensure you have the following information from your Oracle database instance:

- **Host:** The hostname or IP address of the Oracle database server.
- **Port:** The listener port (default is `1521`).
- **Database (Service Name):** The Oracle service name to connect to (e.g. `ORCL` or a TNS alias).
- **Username and Password:** Credentials with the necessary permissions to access the required schemas and tables.

### Optional: Wallet for mTLS Authentication

If your Oracle database requires mutual TLS (mTLS) authentication — common with Oracle Autonomous Database and Oracle Cloud — you will also need:

- **Wallet file:** A `.zip` file containing the wallet credentials (e.g. `cwallet.sso`, `tnsnames.ora`, `sqlnet.ora`).
  Upload the wallet zip to your project's resources in HopsFS before creating the data source.
- **Wallet password:** The password for the wallet, if using a PKCS12 wallet (`ewallet.p12`).
  Auto-login wallets (`cwallet.sso`) do not require a password.

!!! tip
    You can download the wallet zip from the Oracle Cloud Console under your Autonomous Database's **DB Connection** page.
    Upload the zip file to your Hopsworks project (e.g. to `Resources/`) before creating the data source.

## Creation in the UI

### Step 1: Set up a new Data Source

Head to the Data Source View on Hopsworks (1) and set up a new data source (2).

<figure markdown>
  ![Data Source Creation](../../../../assets/images/guides/fs/data_source/data_source_overview.png)
  <figcaption>The Data Source View in the User Interface</figcaption>
</figure>

### Step 2: Enter Oracle Settings

Enter the details for your Oracle database.
Start by giving the connector a **name** and an optional **description**.

1. Select "SQL" as the storage.
2. Select "Oracle" as the database type.
3. Enter the host endpoint.
4. Enter the service name (used as the database field).
5. Specify the port (default `1521`).
6. Provide the username and password.
7. Optionally, upload the wallet zip file and provide the wallet password.
8. Click on "Save Credentials".

## Reading Data

Once the data source is created, you can read data using a SQL query.

### Python Engine

When running outside of Spark (e.g. in a Hopsworks notebook or an external Python client), the Python engine reads data via the Hopsworks Arrow Flight service.
The server handles the Oracle connection — including wallet-based authentication — so no JDBC driver or wallet files are needed on the client side.

```python
import hopsworks

project = hopsworks.login()
feature_store = project.get_feature_store()
ds = feature_store.get_data_source("my_oracle_source")

df = ds.read(query="SELECT * FROM my_schema.my_table", dataframe_type="pandas")
```

You can also request Polars DataFrames:

```python
df = ds.read(query="SELECT * FROM my_schema.my_table", dataframe_type="polars")
```

### Spark Engine

When running with PySpark, the data is read using the Spark JDBC DataSource with the Oracle JDBC thin driver.
If a wallet is configured, the wallet zip is automatically downloaded from HopsFS and extracted on the Spark driver.

```python
import hopsworks

project = hopsworks.login()
feature_store = project.get_feature_store()
ds = feature_store.get_data_source("my_oracle_source")

df = ds.read(query="SELECT * FROM my_schema.my_table")
```

!!! note
    The Oracle JDBC driver JAR (e.g. `ojdbc11.jar`) must be available on the Spark classpath.
    Upload it via the [Jupyter configuration](../../../projects/jupyter/spark_notebook.md) or [Job configuration](../../../projects/jobs/pyspark_job.md) in `Additional Jars`.

## Limitations

### Spark JDBC

!!! warning "Spark JDBC limitations"
    Be aware of the following limitations when reading Oracle data via Spark:

    - **Single-partition reads only.**
      All data is fetched through a single JDBC connection from the Spark driver.
      Spark's parallel JDBC read (via `numPartitions` / `partitionColumn`) is not supported for Oracle data sources.
      For very large tables, consider filtering with a `WHERE` clause in your query.
    - **Wallet available on the driver only.**
      When using wallet-based authentication, the wallet zip is downloaded from HopsFS and extracted on the Spark driver node.
      This is sufficient because reads are single-partition (driver-only).
    - **Timestamp precision.**
      Spark JDBC supports timestamp precision up to seconds only.
      Sub-second precision from Oracle `TIMESTAMP` columns may be truncated.

### Python Engine

The Python engine reads data via the Hopsworks Arrow Flight service, which handles the Oracle connection server-side.
There are no client-side limitations specific to Oracle — wallet authentication, connection pooling, and query execution are all managed by the server.

## Next Steps

Move on to the [usage guide for data sources](../usage.md) to see how you can use your newly created Oracle connector.
