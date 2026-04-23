# How-To set up a Unity Catalog Data Source

## Introduction

A Unity Catalog data source provides integration to [Databricks Unity Catalog](https://docs.databricks.com/aws/en/data-governance/unity-catalog/).
Unity Catalog is Databricks' unified governance layer for data and AI assets, organised as a catalog → schema → table hierarchy.

In this guide, you will configure a Data Source in Hopsworks that points at a Databricks workspace.
Once configured, you can browse catalogs, schemas, and tables, and mount Delta tables as external Feature Groups whose data is read through the Arrow Flight query service.

!!! note
    Only Delta-formatted Unity Catalog tables are supported in this release.
    Managed non-Delta tables are filtered out when browsing.

!!! note
    Currently, it is only possible to create data sources in the Hopsworks UI.
    You cannot create a data source programmatically.

!!! warning
    Direct Spark reads from Unity Catalog are not supported in this release.
    Reads flow through the Arrow Flight query service, which uses DuckDB's `unity_catalog` and `delta` extensions.

## Prerequisites

Before you begin, you need:

- **Databricks workspace URL**, for example `https://<workspace>.cloud.databricks.com`.
- **Personal access token** with at least `USE CATALOG`, `USE SCHEMA`, and `SELECT` privileges on the catalogs, schemas, and Delta tables you want to expose.
- **A catalog name** containing Delta tables you want to mount, optionally set as the default catalog on the connector.

The personal access token is stored encrypted in the Hopsworks secrets table — it is never written to the connector table in plaintext.
Rotation is a manual operation in this release: when the token expires, edit the connector and paste in a fresh one.

## Feature flag

Unity Catalog connectors are gated by the `enable_unity_catalog_storage_connectors` Hopsworks variable.
An administrator must set it to `true` in the admin variables UI before the connector type appears in the create form.

## Creation in the UI

### Step 1: Set up new Data Source

Head to the Data Source view in Hopsworks (1) and set up a new data source (2).

<figure markdown>
  ![Data Source Creation](../../../../assets/images/guides/fs/data_source/data_source_overview.png)
  <figcaption>The Data Source view in the user interface</figcaption>
</figure>

### Step 2: Enter source details

Enter the details for your Unity Catalog workspace.
Start by giving it a unique **name** and an optional **description**.

1. Select "Databricks Unity Catalog" as the storage type.
2. **Databricks Workspace URL** — the full `https://` URL of your workspace.
3. **Access Token** — a Databricks personal access token; the field is masked and stored encrypted.
4. **Default Catalog** — optional; the Unity Catalog catalog to pre-select when browsing.
5. **Arguments** — optional key/value pairs passed through to the query service.
6. Click "Save Credentials".

On save, Hopsworks calls the Unity Catalog `/catalogs` endpoint using the provided token; an HTTP 2xx response is required for the connector to be accepted.

### Step 3: Browse and mount a table

After saving, open the connector and click **Configure**.
The "Catalog" dropdown lists catalogs visible to your token; pick one and the schema/table browser lists Delta tables grouped by schema.
Select a table to create an external Feature Group pointing at it — reads will flow through the Arrow Flight query service.

## Next Steps

Move on to the [usage guide for data sources](../usage.md) to see how you can use your newly created Unity Catalog connector.
