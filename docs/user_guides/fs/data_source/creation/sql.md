# How-To set up an SQL Data Source

## Introduction

The SQL Data Source connects Hopsworks to a Relational Database Service.
Supported database types are **MySQL**, **PostgreSQL**, and **Oracle**.
Using this connector, you can query and update data in your relational database from Hopsworks.

In this guide, you will configure a Data Source in Hopsworks to securely store the authentication information needed to set up a connection to your database instance.
When you're finished, you'll be able to query your SQL database using Hopsworks APIs.

!!! note
    Currently, it is only possible to create data sources in the Hopsworks UI.
    You cannot create a data source programmatically.

## Prerequisites

Before you begin, ensure you have the following information from your database instance:

- **Host:** The endpoint for your database instance.

    Example from AWS:
      1. Go to the AWS Console → `Aurora and RDS`
      2. Click on your DB instance.
      3. Under `Connectivity & security`, you'll find the endpoint, e.g.:
        `mydb.abcdefg1234.us-west-2.rds.amazonaws.com`

- **Database:** The name of the database to connect to.
  For Oracle, this is the **service name** (e.g. `ORCL` or a TNS alias).

- **Port:** The port to connect to (e.g. `3306` for MySQL, `5432` for PostgreSQL, `1521` for Oracle).

- **Username and Password:** A username and password with the necessary permissions to access the required tables.

### Optional: Oracle Wallet for mTLS Authentication

If your Oracle database requires mutual TLS (mTLS) authentication, which is common with Oracle Autonomous Database and Oracle Cloud, you will also need:

- **Wallet file:** A `.zip` file containing the wallet credentials (e.g. `cwallet.sso`, `tnsnames.ora`, `sqlnet.ora`).
- **Wallet password:** The password for the wallet, if using a PKCS12 wallet (`ewallet.p12`).
  Auto-login wallets (`cwallet.sso`) do not require a password.

!!! tip
    You can download the wallet zip from the Oracle Cloud Console under your Autonomous Database's **DB Connection** page.
    Upload the zip file to your Hopsworks project (e.g. to `Resources/`) before creating the data source.

!!! warning "Leave the host empty when using a wallet"
    A host and a wallet are alternatives, not a pair.
    The wallet's `tnsnames.ora` supplies the host and port, and the database field is the alias to look up there.
    Supplying a host as well makes the driver connect directly, past the wallet, which a wallet-protected database refuses with a connection error that names neither the cause nor the fix.
    Hopsworks therefore refuses to save a data source with both a host and a wallet.

## Creation in the UI

### Step 1: Set up a new Data Source

Head to the `Data Sources` view on Hopsworks (1) and click `New data source` (2).
The `Add a data source` catalog lists the available sources, grouped under `Object storage`, `Data warehouse`, `Database`, `Streaming` and `API & SaaS`.
Pick the `SQL` card to open the creation form.

<figure markdown>
  ![Data Source Creation](../../../../assets/images/guides/fs/data_source/data_source_overview.png)
  <figcaption>The Data Source View in the User Interface</figcaption>
</figure>

### Step 2: Enter SQL Settings

Enter the details for your database.
Start by giving the connector a **name** and an optional **description**.

1. The form opens with `Source` set to `SQL`.
   Click `Change source` to pick a different one.
2. Select the database type (MySQL, PostgreSQL, or Oracle).
3. Enter the host endpoint.
   Leave it empty when using an Oracle wallet: the wallet supplies the connection details, and the database field names the TNS alias to use.
4. Enter the database name (service name for Oracle).
5. Specify the port.
6. For Oracle, choose under `Credentials` whether they are `Stored with the data source` (the default) or `Provided by each user`.
   With `Provided by each user` the username, password and wallet fields disappear and every member adds their own later, see [provided credentials][data-source-provided-credentials].
7. Provide the username and password.
8. For Oracle with mTLS, upload the wallet zip file and provide the wallet password (if required).
9. Click on "Save Credentials".

<figure markdown>
  ![SQL Connector Creation](../../../../assets/images/guides/fs/data_source/sql_creation.png)
  <figcaption>SQL Connector Creation Form</figcaption>
</figure>

## Oracle-Specific Notes

The generic read, external feature group, and training data workflows are covered in the [usage guide for data sources][data-source-usage].
The following notes apply only to Oracle.

### JDBC driver on the Spark classpath

The Oracle JDBC driver JAR (e.g. `ojdbc11.jar`) must be available on the Spark classpath.
Upload it via the [Jupyter configuration][how-to-run-a-pyspark-notebook] or [Job configuration][how-to-run-a-pyspark-job] in `Additional Jars`.
The MySQL and PostgreSQL drivers are included in Hopsworks by default.

### Spark JDBC limitations

!!! warning "Oracle Spark JDBC limitations"
    - **Single-partition reads only.**
      All data is fetched through a single JDBC connection from the Spark driver.
      Spark's parallel JDBC read (via `numPartitions` / `partitionColumn`) is not supported.
      For very large tables, filter with a `WHERE` clause in your query.
    - **Wallet available on the driver only.**
      When using wallet-based authentication, the wallet zip is downloaded from HopsFS and extracted on the Spark driver node.
      This is sufficient because reads are single-partition (driver-only).
    - **Timestamp precision.**
      Spark JDBC supports timestamp precision up to seconds only.
      Sub-second precision from Oracle `TIMESTAMP` columns may be truncated.

### Python engine

The Python engine reads Oracle via the Hopsworks Arrow Flight service, which handles the database connection server-side.
No JDBC driver or wallet files are needed on the client, and the Spark JDBC limitations above do not apply.

## Provided credentials for Oracle { #data-source-provided-credentials }

A data source has a credentials mode.
The Data owner chooses it when creating the data source, and it cannot be changed afterwards, because a switch would invalidate every member's setup at once.

| Mode | Who enters the credentials | Who reads with them |
| --- | --- | --- |
| `Stored with the data source` (`SHARED`, the default) | The Data owner, once, in the data source form | Every project member |
| `Provided by each user` (`PROVIDED`) | Each project member, for themselves | That member only |

`PROVIDED` is available for the Oracle database type of the SQL data source.
A provided data source stores the host or the wallet alias, the port and the service name, and nothing else.
Creating one with a username, a password or a wallet is refused with `INVALID_CREDENTIALS_MODE_ARGS` (270339).
The Python client raises the error itself, before sending the request, when a new provided `SqlConnector` carries any of them; each member adds credentials with `set_credentials()` once the data source exists.
Reads run with the credentials of the member who makes them, so a Data owner who creates a provided data source adds their own credentials before browsing its tables or mounting feature groups; the UI opens the dialog for them right after the data source is saved.

```bash
hops datasource create sql oracle_sales --database-type ORACLE --host db.example.com --port 1521 --database ORCL --credentials-mode provided
```

### Adding your credentials

Each member adds their credentials once per data source.
Hopsworks tests them by opening a connection and running `SELECT 1 FROM DUAL`, and saves nothing when the database rejects them.

In the UI, open `Data Sources`, find the data source in the list and pick `My credentials` from its row actions.
The `Credentials` column of the list shows `Shared`, or `Provided` with `Yours: set` or `Yours: missing`.
In the dialog, type a username and a password, or pick an env var and a secret you already keep in your account.
For a database behind mTLS, upload the wallet zip and give its password.
The upload is staged as a new file, see [replacing a wallet][data-source-provided-credentials-wallet].
Click `Validate`, then `Save`.
`Save` stays disabled until `Validate` has passed for the values in the dialog, and editing a field disables it again.
`Remove my credentials` in the same dialog deletes your binding.

From Python, the same operations are methods on the SQL connector:

```python
import hopsworks


project = hopsworks.login()
fs = project.get_feature_store()
sc = fs.get_data_source("oracle_sales").storage_connector

if sc.validate_credentials(user="SCOTT", password="..."):
    sc.set_credentials(user="SCOTT", password="...")

# a database behind mTLS also takes a wallet, uploaded to a new file in your home
wallet = f"{project.home_path}/.datasources/oracle_sales/wallet-7f3a9c.zip"
sc.set_credentials(
    user="SCOTT", password="...", wallet_path=wallet, wallet_password="..."
)

# reuse a secret you already keep in your account
sc.set_credentials(user="SCOTT", password_secret="my_oracle_pwd")

sc.get_credentials()
sc.delete_credentials()
```

`set_credentials` raises a `FeatureStoreException` carrying the database's own error when the credentials are rejected.
`get_credentials` returns the names of the account entries your binding references, never their values.

From the CLI, `hops datasource credentials` has `set`, `validate`, `show` and `delete`.
`--password -` and `--wallet-password -` read the value from stdin, and without either flag the `HOPSWORKS_DS_CREDENTIALS_PASSWORD` and `HOPSWORKS_DS_CREDENTIALS_WALLET_PASSWORD` environment variables are read.
`--wallet` takes a local zip and stages it as a new wallet file for you.

```bash
hops datasource credentials set oracle_sales --user SCOTT --password - --wallet ./Wallet_ORCL.zip --wallet-password -
hops datasource credentials show oracle_sales --json
```

```json
{
  "status": "VALID",
  "username_env_var": "DS_ORACLE_SALES_67_USER",
  "password_secret_name": "ds_oracle_sales_67_password",
  "wallet_path": "/Projects/sales/Users/scott/.datasources/oracle_sales/wallet-7f3a9c.zip",
  "wallet_password_secret_name": "ds_oracle_sales_67_wallet_password",
  "validated_at": "2026-10-07T09:12:44Z"
}
```

`hops datasource list` shows the mode in its `CREDENTIALS` column: `shared`, `provided: yours set`, `provided: missing` or `provided: incomplete`.

### Where your credentials are stored

| Credential | Stored as | Default name |
| --- | --- | --- |
| Username | Env var in your account, private | `DS_<NAME>_<feature store id>_USER` |
| Password | Secret in your account, private | `ds_<name>_<feature store id>_password` |
| Wallet zip | File in your home directory in the project | `/Projects/<project>/Users/<username>/.datasources/<name>/wallet-<random>.zip` |
| Wallet password | Secret in your account, private | `ds_<name>_<feature store id>_wallet_password` |

`<NAME>` is the data source name upper-cased with every character outside `A-Z`, `0-9` and `_` replaced by `_`; `<name>` is the same in lower case.
The feature store id is part of the default names because your account entries are not scoped to a project, so two data sources with the same name in different feature stores would otherwise share one entry.
The names are editable in the dialog and through the `user_env_var`, `password_secret` and `wallet_password_secret` arguments, so an existing entry can be reused instead of creating one.
Your home directory is readable by you alone, so the wallet is too.

The data source keeps a reference to these entries, not a copy.
Deleting the secret or the env var from your account leaves the binding `INCOMPLETE`, and the data source refuses to read until you set your credentials again.
Removing your credentials deletes the binding and the wallet file and keeps the secret and the env var, since you may use them elsewhere.

### Replacing a wallet { #data-source-provided-credentials-wallet }

Every wallet upload, from the dialog or with `hops datasource credentials set --wallet`, is staged as a new file, `<home>/.datasources/<name>/wallet-<random>.zip`, so it never overwrites the wallet your binding points at.
A wallet that fails validation, or a save the database rejects, leaves your binding and its wallet unchanged.
When the save succeeds, the binding points at the new file and Hopsworks deletes the wallet it pointed at before.
From Python, upload the wallet under a name of your own that is not in use, and pass that path as `wallet_path`.

### Runtime variables

Every runtime you start in the project (a job, a Jupyter server, a terminal, an app or a Ray cluster) receives your credentials for each provided data source you have set them for:

| Variable | Value |
| --- | --- |
| `HOPS_DS_<NAME>_CONNECTOR_ID` | The id of the data source these variables belong to |
| `HOPS_DS_<NAME>_USER` | Your username |
| `HOPS_DS_<NAME>_PASSWORD` | Your password |
| `HOPS_DS_<NAME>_WALLET_PATH` | `/hopsfs/Users/<username>/.datasources/<name>/wallet-<random>.zip`, when you set a wallet |
| `HOPS_DS_<NAME>_WALLET_PASSWORD` | Your wallet password, when you set one |

```python
import os


user = os.environ["HOPS_DS_ORACLE_SALES_USER"]
password = os.environ["HOPS_DS_ORACLE_SALES_PASSWORD"]
wallet = os.environ.get("HOPS_DS_ORACLE_SALES_WALLET_PATH")
```

Model deployments do not receive these variables.
A deployment is shared by the project and serves every caller with the same environment, so one member's credentials would answer everyone's requests.

The `HOPS_` prefix is reserved for the platform, so an account env var cannot shadow these.
Two provided data sources in one feature store cannot map to the same `<NAME>`; the second one is refused at creation.
The Hopsworks client reads these variables itself inside a runtime, so a `read()` through the data source needs no further configuration there.
It uses them only for the data source whose id is in `HOPS_DS_<NAME>_CONNECTOR_ID`.
A data source with the same name in another feature store, such as one shared with the project, maps to the same variable names, so for it the client uses the credentials Hopsworks resolves for you when the data source is fetched.

The `/hopsfs` path in `HOPS_DS_<NAME>_WALLET_PATH` is not mounted in Spark.
When that path does not exist, the client downloads your wallet from HopsFS to the Spark driver instead, so a Spark read needs no further configuration either.

### Access to mounted tables

Only Data owners mount external feature groups, and a Data owner's database user may read tables that another member's may not.
Hopsworks therefore keeps, per member and per external feature group on a provided data source, whether that member can read the backing table or query:

| State | Meaning |
| --- | --- |
| `PENDING` | A check is queued and runs within about a minute |
| `OK` | Your credentials read the backing table |
| `NO_CREDENTIALS` | You have not set complete credentials for the data source |
| `INVALID_CREDENTIALS` | The database rejected the login, for example `ORA-01017` or `ORA-28000` |
| `NO_ACCESS` | The login works but the table or query cannot be read: `ORA-00942`, which Oracle also returns for a missing privilege, or `ORA-01031` |
| `ERROR` | Anything else, such as a network or TNS error or a timeout; the message is kept |

A check runs for you on every feature group of the data source when you set or remove your credentials, and for every member with credentials when a Data owner mounts a new feature group.
The state is shown in the feature group catalog and in the feature group's [Data Source submenu][external-feature-group-data-source].
It informs you and does not gate reads: a read in `NO_ACCESS` still goes to Oracle and fails there with the database error.

### Test Connection

`Test Connection`, on the Data Source submenu of a feature group and on greyed-out feature groups in the catalog, runs the check for you now, as you, with a limit of one row, and stores the result.
It takes up to a minute.
Use it after a privilege was granted on the database side, since Hopsworks learns about grants only through the events above and this button.
On a feature group whose data source has shared credentials it tests the shared credentials and stores nothing.

### Trino catalogs { #data-source-provided-credentials-trino }

A provided Oracle data source can back a [Trino catalog][trino-catalogs], and each query through the catalog runs as the member who sends it.
The catalog stores no login.
Its properties name the Trino extra credentials that carry the username and password with each query:

```properties
user-credential-name=hops_ds_<data source id>_user
password-credential-name=hops_ds_<data source id>_password
oracle.connection-pool.enabled=false
```

The connection pool is off because a pooled connection keeps the login of the member who opened it.
Metadata caching is refused for the same reason: a cached table list would show one member what another member's database user can see.

Which clients send the extra credentials:

| Client | Extra credentials |
| --- | --- |
| SQL runner in the UI | Added by Hopsworks for the member running the query |
| `project.get_trino_api().connect()` and `create_engine()` | Fetched by the Python client for the caller |
| JDBC, the Trino CLI, Superset and other Trino clients | Sent by the client, or the Oracle login fails |

A client that is not listed fetches your values from `GET /hopsworks-api/api/project/<project id>/trino/extra-credentials`, with an API key that has the `TRINO` scope, and sends each entry as a Trino extra credential, for example with the CLI's `--extra-credential hops_ds_<data source id>_user=<username>` or the JDBC `extraCredentials` property.
A member who has not set credentials for the data source has nothing to send, and the Oracle login fails.

Creating the catalog requires you to have set your own credentials for the data source.
For a database behind mTLS, the catalog's wallet (`TNS_ADMIN`) is built from your wallet; it only secures the transport, and every query still logs in with the querying member's username and password.
`Test connection` on the catalog runs with the credentials of the member testing it.
The catalog becomes queryable after the query engine restarts, as described in [When the catalog goes live][when-the-catalog-goes-live].

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-method"></code> [`FeatureStore.get_data_source`][hsfs.feature_store.FeatureStore.get_data_source]
    - <code class="doc-symbol doc-symbol-method"></code> [`ExternalFeatureGroup.test_data_source_access`][hsfs.feature_group.ExternalFeatureGroup.test_data_source_access]

    <a class="hops-api-cta" href="../../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>

## Next Steps

Move on to the [usage guide for data sources][data-source-usage] to see how you can use your newly created SQL connector.
You can also make the database queryable from the query engine by adding a [Trino catalog][trino-catalogs] derived from this data source.
