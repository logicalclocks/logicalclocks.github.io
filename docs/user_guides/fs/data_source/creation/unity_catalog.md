# How-To set up a Unity Catalog Data Source

## Introduction

A Unity Catalog data source provides integration with [Databricks Unity Catalog](https://docs.databricks.com/aws/en/data-governance/unity-catalog/).
Unity Catalog is Databricks' unified governance layer for data and AI assets, organised as a catalog → schema → table hierarchy.

In this guide, you will configure a Data Source in Hopsworks that points at a Databricks workspace.
Once configured, you can browse catalogs, schemas, and tables, and mount Delta tables as external Feature Groups whose data is read through the Arrow Flight query service.

!!! warning "Databricks on AWS only"
    Unity Catalog is currently only supported on **Databricks on AWS**.
    Databricks on Azure and Databricks on GCP are not supported in this release — their Unity Catalog temporary-table-credentials responses use cloud-specific credential shapes (Azure SAS tokens, GCP service-account tokens) that the Hopsworks Arrow Flight read path does not yet handle.
    If you point this connector at a non-AWS Databricks workspace the browse flow may succeed but every preview and feature-group read will fail.

!!! note
    Only Delta-formatted Unity Catalog tables are supported in this release.
    Managed non-Delta tables, Iceberg tables, views, streaming tables, and materialised views are filtered out when browsing.

!!! note
    Currently, it is only possible to create data sources in the Hopsworks UI.
    You cannot create a data source programmatically.

!!! warning
    Direct Spark reads from Unity Catalog are not supported in this release.
    Reads flow through the Arrow Flight query service, which resolves each Delta table via the Unity Catalog REST API and reads it using the `deltalake` Python package (delta-rs) against the S3 location that Databricks returns.

## Prerequisites

Before you begin you need all of the following — the first three are on the Databricks side and are the most common source of 400 / 403 errors from the read path.

### Databricks side

- **External Data Access enabled on the metastore.**
  In the Databricks account console, go to Catalog → the metastore backing your workspace → Details, and turn on "External data access".
  Without this toggle, every call to `/api/2.1/unity-catalog/temporary-table-credentials` returns `403 Forbidden` for any principal.
  This is an account-admin setting — workspace admin alone cannot flip it.
- **`EXTERNAL USE SCHEMA` grant on the schemas you want to read.** In Databricks SQL:

  ```sql
  GRANT EXTERNAL USE SCHEMA ON SCHEMA <catalog>.<schema> TO `<principal>`;
  ```

  where `<principal>` is the user (or service principal) that owns the PAT you are about to paste into Hopsworks. Without this grant the temporary-table-credentials endpoint returns `400 Bad Request`.
- **`USE CATALOG`, `USE SCHEMA`, and `SELECT` grants** on the specific catalog / schema / tables you want to mount.
- **Delta format.** Unity Catalog tables backed by Iceberg, non-Delta file formats, views, or streaming / materialised views cannot be read through this connector in v1.

### Hopsworks side

- **Databricks workspace URL**, for example `https://<workspace>.cloud.databricks.com`.
- **Personal access token** for the principal to which the grants above were issued.
- **A catalog name** containing the Delta tables you want to mount. It is optional but recommended to set this as the default catalog on the connector so the UI opens the browse view directly.
- Optional: an **AWS region** (for example `us-west-2`). If you omit it, the backend guesses the region by parsing the STS session-token returned with the table credentials. For FIPS regions or for any workspace where the guess has been wrong once, set the region explicitly on the connector.

The personal access token is stored encrypted in the Hopsworks `secrets` table — it is never written to the connector table in plaintext.
PAT rotation is manual in this release: when the token expires, edit the connector and paste in a fresh one. Unity Catalog PATs are typically short-lived (hours to a few days), so expect to do this periodically.

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
5. **AWS Region** — optional; set explicitly (for example `us-west-2`) when the backend's region guess from the STS session-token is wrong or your workspace is in a FIPS region. Leave empty to use the guess.
6. **Arguments** — optional key/value pairs passed through to the query service.
7. Click "Save Credentials".

On save, Hopsworks calls the Unity Catalog `/catalogs` endpoint using the provided token; an HTTP 2xx response is required for the connector to be accepted.

### Step 3: Browse and mount a table

After saving, open the connector and click **Configure**.
The "Catalog" dropdown lists catalogs visible to your token; pick one and the schema/table browser lists Delta tables grouped by schema.
Select a table to create an external Feature Group pointing at it — reads will flow through the Arrow Flight query service.

## Next Steps

Move on to the [usage guide for data sources](../usage.md) to see how you can use your newly created Unity Catalog connector.
