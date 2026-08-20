---
description: Guide on how to make a data source queryable from the query engine with Trino catalogs
---

# Trino Catalogs

A Trino catalog makes an external data source queryable from the query engine.
Each catalog names a Trino connector and the properties that connector needs to reach the source, such as a connection URL and credentials.
Once a catalog is live, its databases and tables can be queried from the SQL runner alongside your feature groups.

Creating, updating, or deleting a catalog records the change immediately, but the change only takes effect once the query engine restarts and reloads its catalogs.
Every screen that changes a catalog therefore tells you when that will happen: at the next scheduled restart, or immediately if a cluster administrator restarts the query engine.

## Creating a catalog from a data source

The recommended way to create a catalog is from a data source, because the data source already holds everything the catalog needs: the host, the database, and the credential.
Hopsworks derives the connector type and properties for you, so you do not need to know the property names of the underlying Trino connector.

When you browse a data source's databases and tables to create an external feature group or ingest data, there are two ways in:

- A standalone **Add Trino Catalog** button on the configuration screen, which creates the catalog on its own, without creating or ingesting any feature group.
- An **Add Trino Catalog** checkbox on the review step, checked by default, which creates the catalog as the first step of setting up the feature groups.

Both are disabled with the reason when the data source cannot be mapped to a Trino connector, and show an **Already added** state when a catalog for this source already exists.

The catalog is created first, so you can review its properties before the feature groups and their ingestion are set up.
The **Create Trino Catalog** dialog opens pre-filled with:

- A suggested catalog name, prefixed with your project name in lowercase.
  The prefix is required, so catalogs from different projects cannot collide on one query engine.
- The Trino connector type derived from the data source.
- The connector properties derived from the data source's settings.
  You can edit them and add any property the connector supports that the data source does not carry.

### Credentials are references, not copies

Credential properties are pre-filled as references rather than values:

- `${HOPSWORKS_SECRET:<name>}` references a Hopsworks secret.
  When the catalog is created, the credential is read from the data source and stored as a secret owned by you, and the catalog keeps only the reference.
- `${HOPSWORKS_MOUNT:<bundle>}` references a credential-file bundle, used when the credential is a file rather than a value.
  An Oracle data source that authenticates with a wallet is delivered this way: the bundle is built from the data source's own wallet, and the catalog's `TNS_ADMIN` property points at it.

No credential is ever sent to the browser, and rotating a credential stays a single operation on the secret rather than an edit of every catalog that uses it.

### Test connection

The **Create** button is enabled only after **Test connection** succeeds, where the cluster supports it, so a catalog that cannot reach its source is caught now rather than after a restart.
A failed test shows the query engine's own error message inline.

### When the catalog goes live

After creation, the **Catalog created** dialog shows the current query engine activity and when the catalog becomes queryable:

- The next scheduled restart, in your own timezone, when the cluster has one configured.
- A **Restart now** action, if you are a cluster administrator, together with the number of queries currently running and queued.
  Restarting cancels those queries everywhere on the cluster, so the dialog shows the activity to let you judge whether restarting now is safe.
- Otherwise, a note to ask an administrator if the catalog is needed sooner.

## Managing catalogs

Navigate to **Query Engine** → **Catalogs** in your project to see the project's catalogs together with the cluster's shared default catalogs.
Each catalog shows its status: pending until the next restart, live, or quarantined.

From this page you can also:

- **Create a catalog by hand**, choosing the connector type and writing the properties yourself.
  This is the path for a source that has no Hopsworks data source, and the same validation, connection test, and restart handling apply.
- **Edit a catalog.**
  Secret-bearing property values come back masked, and a masked value left unchanged keeps the stored secret, so you do not retype credentials to change an unrelated property.
- **Delete a catalog.**
  The catalog stays queryable until the query engine restarts and unloads it, and the dialog tells you when that is, with the same restart-now option for administrators.

### Quarantined catalogs

The query engine refuses to start when a catalog cannot be loaded.
If that happens during a restart, the offending catalog is quarantined so the query engine can recover, and the catalog's page carries the load error.
A quarantined catalog is not applied; fix its properties and save it to try again.

## Creating a catalog from the Python client

The same operations are available from the Python client, so making a data source queryable can be scripted from a job or a notebook.

```python
import hopsworks


project = hopsworks.login()
fs = project.get_feature_store()

sc = fs.get_data_source("my_snowflake_db").storage_connector

template = sc.get_trino_catalog_template()
if template["supported"]:
    catalog = sc.create_trino_catalog()
    print(catalog["name"], catalog["status"])
else:
    print("cannot be mapped:", template["reason"])
```

`get_trino_catalog_template()` returns the proposal without creating anything, so it can be reviewed or adjusted first.
`create_trino_catalog()` accepts an optional `name` and a `properties` override, and tests the connection before creating where the cluster supports it, so an unreachable source raises before the catalog exists.
Credentials are resolved server-side into references exactly as in the UI path.

The full catalog lifecycle is available on the project:

```python
import hopsworks


project = hopsworks.login()
catalogs = project.get_trino_catalog_api()

for catalog in catalogs.get_catalogs():
    print(catalog["name"], catalog["status"])

print(catalogs.get_capabilities()["nextScheduledRestart"])
```

A cluster administrator can apply every pending catalog change immediately instead of waiting for the schedule:

```python
import hopsworks


project = hopsworks.login()
catalogs = project.get_trino_catalog_api()

result = catalogs.restart()
print(result["restarted"], result["quarantined"])
```

The restart interrupts queries running anywhere on the cluster, so prefer waiting for the scheduled restart unless the change is needed sooner.

## When changes take effect

A cluster administrator configures a scheduled restart that applies pending catalog changes on its own, so a catalog goes live without anyone holding cluster rights.
The schedule does nothing at all unless a catalog change is actually pending, so a cluster with no changes is never interrupted, and a due restart waits for a quiet moment (no query running, queued, or blocked) for up to an hour before going ahead.
Administrators can also enable an eager restart, which applies pending changes the moment the query engine goes idle, so a catalog may go live earlier than the scheduled time; the dialogs tell you when the cluster does this.
Administrators can instead require approval for all catalog changes, in which case nothing goes live until they apply the pending requests, and the dialogs say to ask an administrator.
The schedule's configuration is described in the [administrator guide][catalogs-and-the-scheduled-restart].
