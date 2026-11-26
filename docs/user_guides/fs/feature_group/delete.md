---
description: Documentation on how to delete a feature group in Hopsworks, and how to keep its data on an S3, GCS or Glue data source.
---

# How to delete a Feature Group

## Introduction

Deleting a feature group removes this version of it from Hopsworks: its metadata, online data, Kafka topic, commits, statistics, validation reports and the jobs that write to it.
By default its offline data is deleted too.
A feature group that stores its offline data on an S3, GCS or Glue data source can keep that data instead, for example when the bucket holds data you manage outside Hopsworks.

In this guide you will learn how to delete a feature group, showing examples in Hopsworks APIs as well as the user interface.

## Prerequisites

Before you begin this guide it is expected that there is an existing feature group in your project.
You can familiarize yourself with [the creation of a feature group](./create.md) in the user guide.

## Delete using the Hopsworks APIs

### Retrieve the feature group

To delete a feature group using the Hopsworks APIs you need to provide a [Feature Group](../../../concepts/fs/feature_group/fg_overview.md).

=== "Python"

    ```python
    fg = fs.get_feature_group(
        name="feature_group_name", version=feature_group_version
    )
    ```

### Delete the feature group

=== "Python"

    ```python
    fg.delete()
    ```

A feature group that a feature view uses cannot be deleted, since the feature view would stop working.
Pass `force=True` to delete it anyway and leave the feature views in place, or `delete_feature_views=True` to delete those feature views first, along with their training data.

### Keep the data on the data source

=== "Python"

    ```python
    fg.delete(delete_data=False)
    ```

With `delete_data=False`, the objects under the feature group's path on its S3, GCS or Glue data source stay in the bucket, and so does its Glue table.
Everything else is deleted as with `fg.delete()`.

A feature group whose offline data is stored in Hopsworks cannot keep it, so the deletion fails.
Keeping the data needs Hopsworks 5.3 or later: an older cluster ignores the option and would delete the data, so the client refuses the call.

From the command line, `hops fg delete <name> --version <version> --keep-data` does the same.

### Recreate a feature group on the kept data

A feature group created later with the same name, version and data source reads and writes the kept table.
To start with an empty table, give the new feature group another `path` on S3 or GCS.
On Glue, the location of an existing catalog table takes precedence over the path, so give it another table name instead.

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-method"></code> [`FeatureStore.get_feature_group`][hsfs.feature_store.FeatureStore.get_feature_group]
    - <code class="doc-symbol doc-symbol-class"></code> [`FeatureGroup`][hsfs.feature_group.FeatureGroup]
        - <code class="doc-symbol doc-symbol-method"></code> [`delete`][hsfs.feature_group.FeatureGroup.delete]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>

## Delete using the UI

Navigate to the `Feature Groups` section, select the feature group and the version to delete, and click the delete icon in the top right corner.
Type `confirm` in the dialog to enable the delete button.

The dialog offers the options of the API:

- **Force delete** deletes the feature group even though feature views use it.
- **Cascade delete** deletes those feature views first, along with their training data.
- **Keep data on** the data source keeps the offline data in the bucket.
  It is shown only for a feature group that stores its offline data on an S3, GCS or Glue data source.

## Delete a data source

Deleting a data source deletes the feature groups that use it, see [Deleting a Data Source][deleting-a-data-source].
