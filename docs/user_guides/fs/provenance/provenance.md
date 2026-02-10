# Provenance

## Introduction

Hopsworks allows users to track provenance (lineage) between:

- data sources
- feature groups
- feature views
- training datasets
- models

In the provenance pages we will call a provenance artifact or shortly artifact, any of the five entities above.

With the following provenance graph:

```plaintext
data source -> feature group -> feature group -> feature view -> training dataset -> model
```

we will call the parent, the artifact to the left, and the child, the artifact to the right.
So a feature view has a number of feature groups as parents and can have a number of training datasets as children.

Tracking provenance allows users to determine where and if an artifact is being used.
You can track, for example, if feature groups are being used to create additional (derived) feature groups or feature views, or if their data is eventually used to train models.

You can interact with the provenance graph using the UI or the APIs.

## Step 1: Data Source lineage

The relationship between data sources and feature groups is captured automatically when you create an external feature group.
You can inspect the relationship between data sources and feature groups using the APIs.

=== "Python"

    ```python
    # Retrieve the data source
    ds = fs.get_data_source("snowflake_sc")
    ds.query = "SELECT * FROM USER_PROFILES"

    # Create the user profiles feature group
    user_profiles_fg = fs.create_external_feature_group(
        name="user_profiles",
        version=1,
        data_source=ds
    )
    user_profiles_fg.save()
    ```

### Step 1, Using Python

Starting from a feature group metadata object, you can traverse upstream the provenance graph to retrieve the metadata objects of the data sources that are part of the feature group.
To do so, you can use the [`FeatureGroup.get_data_source_provenance`][hsfs.feature_group.FeatureGroup.get_data_source_provenance] method.

=== "Python"

    ```python
    # Returns all data sources linked to the provided feature group
    lineage = user_profiles_fg.get_data_source_provenance()

    # List all accessible parent data sources
    lineage.accessible

    # List all deleted parent data sources
    lineage.deleted

    # List all the inaccessible parent data sources
    lineage.inaccessible
    ```

=== "Python"

    ```python
    # Returns an accessible data source linked to the feature group (if it exists)
    user_profiles_fg.get_data_source()
    ```

To traverse the provenance graph in the opposite direction (i.e., from the data source to the feature group), you can use the [`StorageConnector.get_feature_groups_provenance`][hsfs.storage_connector.StorageConnector.get_feature_groups_provenance] method.
When navigating the provenance graph downstream, the `deleted` feature groups are not tracked by provenance, as such, the `deleted` property will always return an empty list.

=== "Python"

    ```python
    # Returns all feature groups linked to the provided data source
    lineage = snowflake_sc.get_feature_groups_provenance()

    # List all accessible downstream feature groups
    lineage.accessible

    # List all the inaccessible downstream feature groups
    lineage.inaccessible
    ```

=== "Python"

    ```python
    # Returns all accessible feature groups linked to the data source (if any exists)
    snowflake_sc.get_feature_groups()
    ```

## Step 2: Feature group lineage

### Assign parents to a feature group

When creating a feature group, it is possible to specify a list of feature groups used to create the derived features.
For example, you could have an external feature group defined over a Snowflake or Redshift table, which you use to compute the features and save them in a feature group.
You can mark the external feature group as parent of the feature group you are creating by using the `parents` parameter in the [`FeatureStore.get_or_create_feature_group`][hsfs.feature_store.FeatureStore.get_or_create_feature_group] or [`FeatureStore.create_feature_group`][hsfs.feature_store.FeatureStore.create_feature_group] methods:

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

You can query the provenance graph of a feature group using the UI and the APIs.
From the APIs you can list the parent feature groups by calling the method [`FeatureGroup.get_parent_feature_groups`][hsfs.feature_group.FeatureGroup.get_parent_feature_groups]

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

A parent is marked as `deleted` (and added to the deleted list) if the parent feature group was deleted. `inaccessible` if you no longer have access to the parent feature group (e.g., the parent feature group belongs to a project you no longer have access to).

To traverse the provenance graph in the opposite direction (i.e., from the parent feature group to the child), you can use the [`FeatureGroup.get_generated_feature_groups`][hsfs.feature_group.FeatureGroup.get_generated_feature_groups] method.
When navigating the provenance graph downstream, the `deleted` feature groups are not tracked by provenance, as such, the `deleted` property will always return an empty list.

=== "Python"

    ```python
    lineage = transaction_fg.get_generated_feature_groups()

    # List all accessible child feature groups
    lineage.accessible

    # List all the inaccessible child feature groups
    lineage.inaccessible
    ```

You can also visualize the relationship between the parent and child feature groups in the UI.
In each feature group overview page you can find a provenance section with the graph of parent data source/feature groups and child feature groups/feature views.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/fs/provenance/provenance_fg.png" alt="Derived feature group provenance graph">
    <figcaption>Provenance graph of derived feature groups</figcaption>
  </figure>
</p>

## Step 3: Feature view lineage

The relationship between feature groups and feature views is captured automatically when you create a feature view.
You can inspect the relationship between feature groups and feature views using the APIs or the UI.

### Step 3, Using Python

Starting from a feature view metadata object, you can traverse upstream the provenance graph to retrieve the metadata objects of the feature groups that are part of the feature view.
To do so, you can use the [`FeatureView.get_parent_feature_groups`][hsfs.feature_view.FeatureView.get_parent_feature_groups] method.

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

You can also traverse the provenance graph in the opposite direction.
Starting from a feature group you can navigate downstream and list all the feature views the feature group is used in.
As for the derived feature group example above, when navigating the provenance graph downstream `deleted` feature views are not tracked.
As such, the `deleted` property will always be empty.

=== "Python"

    ```python
    lineage = transaction_fg.get_generated_feature_views()

    # List all accessible downstream feature views
    lineage.accessible

    # List all the inaccessible downstream feature views
    lineage.inaccessible
    ```

Users can call the [`FeatureView.get_models_provenance`][hsfs.feature_view.FeatureView.get_models_provenance] method which will return a [provenance Link object](#provenance-links).

You can also retrieve directly the accessible models, without the need to extract them from the provenance links object:
=== "Python"

    ```python
    #List all accessible models
    models = fraud_fv.get_models()

    #List accessible models trained from a specific training dataset version
    models = fraud_fv.get_models(training_dataset_version: 1)
    ```

Also we added a utility method to retrieve from the user's accessible models, the last trained one.
Last is determined based on timestamp when it was saved into the model registry.
=== "Python"

    ```python
    #Retrieve newest model from all user's accessible models based on this feature view
    model = fraud_fv.get_newest_model()
    #Retrieve newest model from all user's accessible models based on this training dataset version
    model = fraud_fv.get_newest_model(training_dataset_version: 1)
    ```

### Step 3, Using UI

In the feature view overview UI you can explore the provenance graph of the feature view:

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/fs/provenance/provenance_fv.png" alt="Feature view provenance graph">
    <figcaption>Feature view provenance graph</figcaption>
  </figure>
</p>

## Provenance Links

All the `_provenance` methods return a `Link` dictionary object that contains `accessible`, `inaccessible`, `deleted` lists.

- `accessible` - contains any artifact from the result, that the user has access to.
- `inaccessible` - contains any artifacts that might have been shared at some point in the past, but where this sharing was retracted.
Since the relation between artifacts is still maintained in the provenance, the user will only have access to limited metadata and the artifacts will be included in this `inaccessible` list.
- `deleted` - contains artifacts that are deleted with children still present in the system.
There is minimum amount of metadata for the deleted allowing for some limited human readable identification.
