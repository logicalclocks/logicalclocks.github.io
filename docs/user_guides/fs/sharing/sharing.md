# Sharing

## Introduction

Hopsworks allows artifacts (e.g. feature groups, feature views) to be shared between projects.
There are two main use cases for sharing features between projects:

- If you have multiple teams working on the same Hopsworks deployment. Each team works within its own set of projects. 
  If team A wants to leverage features built by team B, they can do so by sharing the feature groups from a team A project to a team B project.

- By creating different projects for the different stages of the development lifecycle (e.g. a dev project, a testing project, and a production project), 
  you can make sure that changes on the development project don't impact the features in the production project. At the same time, you might want to 
  leverage production features to develop new models or additional features. In this case, you can share the production feature store with the 
  development feature store in `read-only` mode.

### Step 1: Open the project of the feature store that you would like to share on Hopsworks.

In the `Project Settings` navigate to the `Shared with other projects` section.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/project/share_with_other_projects.png" alt="Share Project">
  </figure>
</p>

### Step 2: Share

Click `Share feature store` to bring up the dialog for sharing.

In the `Project` section choose project you wish to share the feature store with.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/project/share_dialog.png" alt="Share Project Dialog">
  </figure>
</p>

Feature stores can be shared exclusively using `read-only` permission. This means that a member is not capable of enacting any changes on the shared project.

### Step 3: Accept the Invitation

In the project where the feature store was shared (step 2) go to `Project Settings` and navigate to the `Shared from other projects` section.
Click `accept`.


<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/project/accept.png" alt="Accept">
  </figure>
</p>

After accepting the share, the shared feature store is listed under the `Shared from other projects` section.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/project/list_of_shared_projects.png" alt="List of shared projects">
  </figure>
</p>

## Use features from a shared feature store 

### Step 1: Get feature store handles 
To access features from a shared feature store you need to first retrieve the handle for the shared feature store. 
To retrieve the handle use the get_feature_store() method and provide the name of the shared feature store

```python
import hsfs

connection = hsfs.connection()

project_feature_store = connection.get_feature_store()
shared_feature_store = connection.get_feature_store(name="name_of_shared_feature_store")
```

### Step 2: Fetch feature groups

```python
# fetch feature group object from shared feature store
shared_fg = shared_feature_store.get_feature_group(
    name="shared_fg_name",
    version="1")

# fetch feature group object from project feature store
fg_a = project_feature_store.get_or_create_feature_group(
    name="feature_group_name",
    version=1)
```

### Step 3: Join feature groups

```python
# join above feature groups
query = shared_fg.select_all().join(fg_a.select_all())
```
