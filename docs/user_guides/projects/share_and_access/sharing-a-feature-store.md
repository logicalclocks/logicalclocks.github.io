# Sharing a Feature Store

## Introduction

In hopsworks it is possible to share feature stores among projects, so even if you have a connection to one project,
you can retireve a handle to any feature store shared with that project

## UI

### Step 1: Open the project of the feature store that you would like to share on Hopsworks.

In the `Project Settings` navigate to `Shared with other projects` section.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/project/share_with_other_projects.png" alt="Share Project">
  </figure>
</p>

### Step 2: Share current feature store   

Click `Share feature store` to bring up the dialog for sharing.

In `Project` section choose feature store project you wish to share feature store with.

In `Access rights` section select the permissions level that the project user members should have on the feature store and click Share.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/project/share_dialog.png" alt="Share Project Dialog">
  </figure>
</p>

### Step 3: Accept Invitation

In the project where feature store was shared (step 2) go to `Project Settings` and navigate to `Shared from other projects` section.
Click `accept`.


<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/project/accept.png" alt="Accept">
  </figure>
</p>

Now shared feature stores and corresponding access rights will be listed under `Shared from other projects` section.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/project/list_of_shared_projects.png" alt="List of shared projects">
  </figure>
</p>

## Fetch feature groups from shared feature store and join with feature groups from current feature store   

### Step 1: Get feature store handles 

```python
import hsfs

connection = hsfs.connection()

current_feature_store = connection.get_feature_store(name="name_of_current_feature_store")
shared_feature_store = connection.get_feature_store(name="name_of_shared_feature_store")
```

### Step 2: Fetch feature groups from shared and current feature stores

```python
# fetch feature group object from shared feature store
shared_fg = shared_feature_store.get_or_create_feature_group(
    name="shared_fg_name",
    version="1")

# fetch feature group object from current feature store
fg_a = current_feature_store.get_or_create_feature_group(
    name="feature_group_name",
    version=1)
```

### Step 3: Join feature groups

```python
# join above feature groups
query = shared_fg.select_all().join(fg_a.select_all())
```

## Conclusion

In this guide you learned how to share feature store between projects and join feature groups.