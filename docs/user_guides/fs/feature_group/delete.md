---
description: Documentation on how to delete a feature group in Hopsworks, and how to keep its data on an S3, GCS or Glue data source.
---

# How to delete a Feature Group

## Introduction

Deleting a feature group removes this version of it from Hopsworks: its metadata, online data, commits, statistics, validation reports and the jobs that write to it.
Its Kafka topic is deleted too, unless it is the project's shared topic, or another feature group or a model deployment uses it.
By default the offline data of a cached or stream feature group is deleted too, whether Hopsworks stores it or it sits on an S3, GCS or Glue data source.
A feature group on such a data source can keep that data instead, for example when the bucket holds data you manage outside Hopsworks.
An external feature group only reads its data source, so deleting it never deletes the data there.

In this guide you will learn how to delete a feature group, showing examples in Hopsworks APIs as well as the user interface.

## Prerequisites

Before you begin this guide it is expected that there is an existing feature group in your project.
You can familiarize yourself with [the creation of a feature group][create-feature-group] in the user guide.

## Delete using the Hopsworks APIs

### Retrieve the feature group

To delete a feature group using the Hopsworks APIs you need to provide a [Feature Group][features-and-feature-groups].

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

A feature group created later at the same table location, with the original table format, schema, primary key, event time and partition key, reads and writes the kept table.
An upsert matches rows on the primary key, event time and partition key, so changing any of them changes which kept rows it updates.
On S3 or GCS, the same name and version reach that location only when the original feature group used the default path; otherwise pass the original `path`.
On Glue, the location of an existing catalog table takes precedence over the path, so the same database and table name reach it.

!!! warning "Hopsworks metadata is not restored"

    The recreated feature group starts without commit history, statistics or online data.
    `commit_details()` is empty, and `as_of` and incremental reads fail until an insert registers a commit, because Hopsworks resolves them against its own commits.
    The Delta or Iceberg history stays in the table, so a later incremental read can span changes made before the recreate.

`insert()` upserts into the kept table by default.
`operation="insert"` appends to it instead, except on a stream feature group written from Python, whose client does not pass `operation` on to the materialization job.
`insert(overwrite=True)` deletes the kept table and its history before writing.

To start with an empty table instead, give the new feature group an unused `path` on S3 or GCS, or another table name on Glue.

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-method"></code> [`FeatureStore.get_feature_group`][hsfs.feature_store.FeatureStore.get_feature_group]
    - <code class="doc-symbol doc-symbol-class"></code> [`FeatureGroup`][hsfs.feature_group.FeatureGroup]
        - <code class="doc-symbol doc-symbol-method"></code> [`delete`][hsfs.feature_group.FeatureGroup.delete]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>

## Delete using the UI

Navigate to the `Catalog` section of the project sidebar, select the feature group and the version to delete, and click the delete icon in the top right corner.
Type `confirm` in the dialog to enable the delete button.

The dialog offers the options of the API:

- **Force delete** deletes the feature group even though feature views use it.
- **Cascade delete** deletes those feature views first, along with their training data.
- **Keep data on** the data source keeps the offline data in the bucket.
  It is shown only for a feature group that stores its offline data on an S3, GCS or Glue data source.

## Delete a data source

Deleting a data source deletes the feature groups that use it.
[Deleting a Data Source][deleting-a-data-source] describes how to keep their data.
