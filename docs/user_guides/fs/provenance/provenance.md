# Provenance

## Introduction

Hopsworks feature store allows users to track provenance (lineage) between storage connectors, feature groups, feature views, training datasets and models. Tracking lineage allows users to determine where/if a feature group is being used. You can track if feature groups are being used to create additional (derived) feature groups or feature views.

You can interact with the provenance graph using the UI and the APIs.

## Step 1: Storage connector lineage

The relationship between storage connectors and feature groups is captured automatically when you create an external feature group. You can inspect the relationship between storage connectors and feature groups using the APIs.

=== "Python"

    ```python
    # Retrieve the storage connector
    snowflake_sc = fs.get_storage_connector("snowflake_sc")

    # Create the user profiles feature group
    user_profiles_fg = fs.create_external_feature_group(
        name="user_profiles",
        version=1,
        storage_connector=snowflake_sc,
        query="SELECT * FROM USER_PROFILES"
    )
    user_profiles_fg.save()
    ```

### Using the APIs

Starting from a feature group metadata object, you can traverse upstream the provenance graph to retrieve the metadata objects of the storage connectors that are part of the feature group. To do so, you can use the [get_storage_connector_provenance](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/api/feature_group_api/#get_storage_connector_provenance) method.

=== "Python"

    ```python
    # Returns all storage connectors linked to the provided feature group
    lineage = user_profiles_fg.get_storage_connector_provenance()

    # List all accessible parent storage connectors
    lineage.accessible

    # List all deleted parent storage connectors
    lineage.deleted

    # List all the inaccessible parent storage connectors
    lineage.inaccessible
    ```

=== "Python"

    ```python
    # Returns an accessible storage connector linked to the feature group (if it exists)
    user_profiles_fg.get_storage_connector()
    ```

To traverse the provenance graph in the opposite direction (i.e. from the storage connector to the feature group), you can use the [get_feature_groups_provenance](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/api/storage_connector_api/#get_feature_groups_provenance) method. When navigating the provenance graph downstream, the `deleted` feature groups are not tracked by provenance, as such, the `deleted` property will always return an empty list.

=== "Python"

    ```python
    # Returns all feature groups linked to the provided storage connector
    lineage = snowflake_sc.get_feature_groups_provenance()

    # List all accessible downstream feature groups
    lineage.accessible

    # List all the inaccessible downstream feature groups
    lineage.inaccessible
    ```

=== "Python"

    ```python
    # Returns all accessible feature groups linked to the storage connector (if any exists)
    snowflake_sc.get_feature_groups()
    ```

## Step 2: Feature group lineage

### Assign parents to a feature group

When creating a feature group, it is possible to specify a list of feature groups used to create the derived features. For example, you could have an external feature group defined over a Snowflake or Redshift table, which you use to compute the features and save them in a feature group. You can mark the external feature group as parent of the feature group you are creating by using the `parents` parameter in the [get_or_create_feature_group](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/api/feature_group_api/#get_or_create_feature_group) or [create_feature_group](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/api/feature_group_api/#create_feature_group) methods:

=== "Python"

    ```python
    # Retrieve the feature group
    profiles_fg = fs.get_external_feature_group("user_profiles", version=1)

    # Do feature engineering
    age_df = transaction_df.merge(profiles_fg.read(), on="cc_num", how="left")
    transaction_df["age_at_transaction"] = (age_df["datetime"] - age_df["birthdate"]) / np.timedelta64(1, "Y")

    # Create the transaction feature group
    transaction_fg = fs.get_or_create_feature_group(
        name="transaction_fraud_batch",
        version=1,
        description="Transaction features",
        primary_key=["cc_num"],
        event_time="datetime",
        parents=[profiles_fg]
    )
    transaction_fg.insert(transaction_df)
    ```

Another example use case for derived feature group is if you have a feature group containing features with daily resolution and you are using the content of that feature group to populate a second feature group with monthly resolution:

=== "Python"

    ```python
    # Retrieve the feature group
    daily_transaction_fg = fs.get_feature_group("daily_transaction", version=1)
    daily_transaction_df = daily_transaction_fg.read()

    # Do feature engineering
    cc_group = daily_transaction_df[["cc_num", "amount", "datetime"]] \
                    .groupby("cc_num") \
                    .rolling("1M", on="datetime")
    monthly_transaction_df  = pd.DataFrame(cc_group.mean())

    # Create the transaction feature group
    monthly_transaction_fg = fs.get_or_create_feature_group(
        name="monthly_transaction_fraud_batch",
        version=1,
        description="Transaction features - monthly aggregates",
        primary_key=["cc_num"],
        event_time="datetime",
        parents=[daily_transaction_fg]
    )
    monthly_transaction_fg.insert(monthly_transaction_df)
    ```

### List feature group parents

You can query the provenance graph of a feature group using the UI and the APIs. From the APIs you can list the parent feature groups by calling the method [get_parent_feature_groups](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/api/feature_group_api/#get_parent_feature_groups)

=== "Python"

    ```python
    lineage = transaction_fg.get_parent_feature_groups()

    # List all accessible parent feature groups
    lineage.accessible

    # List all deleted parent feature groups
    lineage.deleted

    # List all the inaccessible parent feature groups
    lineage.inaccessible
    ```

A parent is marked as `deleted` (and added to the deleted list) if the parent feature group was deleted. `inaccessible` if you no longer have access to the parent feature group (e.g. the parent feature group belongs to a project you no longer have access to).

To traverse the provenance graph in the opposite direction (i.e. from the parent feature group to the child), you can use the [get_generate_feature_groups](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/api/feature_group_api/#get_generated_feature_groups) method. When navigating the provenance graph downstream, the `deleted` feature groups are not tracked by provenance, as such, the `deleted` property will always return an empty list.

=== "Python"

    ```python
    lineage = transaction_fg.get_generated_feature_groups()

    # List all accessible child feature groups
    lineage.accessible

    # List all the inaccessible child feature groups
    lineage.inaccessible
    ```

You can also visualize the relationship between the parent and child feature groups in the UI. In each feature group overview page you can find a provenance section with the graph of parent storage connectors/feature groups and child feature groups/feature views.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/fs/provenance/provenance_fg.png" alt="Derived feature group provenance graph">
    <figcaption>Provenance graph of derived feature groups</figcaption>
  </figure>
</p>

## Step 3: Feature view lineage

The relationship between feature groups and feature views is captured automatically when you create a feature view. You can inspect the relationship between feature groups and feature views using the APIs or the UI.

### Using the APIs

Starting from a feature view metadata object, you can traverse upstream the provenance graph to retrieve the metadata objects of the feature groups that are part of the feature view. To do so, you can use the [get_parent_feature_groups](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/api/feature_view_api/#get_parent_feature_groups) method.

=== "Python"

    ```python
    lineage = fraud_fv.get_parent_feature_groups()

    # List all accessible parent feature groups
    lineage.accessible

    # List all deleted parent feature groups
    lineage.deleted

    # List all the inaccessible parent feature groups
    lineage.inaccessible
    ```

You can also traverse the provenance graph in the opposite direction. Starting from a feature group you can navigate downstream and list all the feature views the feature group is used in. As for the derived feature group example above, when navigating the provenance graph downstream `deleted` feature views are not tracked. As such, the `deleted` property will always be empty.

=== "Python"

    ```python
    lineage = transaction_fg.get_generated_feature_views()

    # List all accessible downstream feature views
    lineage.accessible

    # List all the inaccessible downstream feature views
    lineage.inaccessible
    ```

### Using the UI

In the feature view overview UI you can explore the provenance graph of the feature view:

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/fs/provenance/provenance_fv.png" alt="Feature view provenance graph">
    <figcaption>Feature view provenance graph</figcaption>
  </figure>
</p>
