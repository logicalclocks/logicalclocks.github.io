# Sharing

## Introduction

Machine Learning Operations (MLOps) is a process that applies DevOps principles to automate the building, testing, and 
deployment of machine learning (ML) models through its entire life cycle. The Feature Store has become the defacto building block for MLOps.
For more details check our blog [MLOps with a Feature Store](https://www.hopsworks.ai/post/mlops-with-a-feature-store).

Enterprise MLOps process usually follow established release management guidelines and includes the following distinct stages:
Development, Testing, Staging and Production.

Thus, enterprises may have separate feature stores for each of this stage and data scientist may need to access feature groups
from production feature store and join with newly developed feature groups in development feature store. 

In Hopsworks it is possible to share feature stores among projects, so even if you have a connection to one project,
you can fetch a handle to any feature store shared with that project:


### Step 1: Open the project of the feature store that you would like to share on Hopsworks.

In the `Project Settings` navigate to `Shared with other projects` section.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/project/share_with_other_projects.png" alt="Share Project">
  </figure>
</p>

### Step 2: Share

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

After accepting the share, the feature store and corresponding access rights are listed under the 
`Shared from other projects` section.

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

## Conclusion

In this guide you learned how to share a feature store and how to join features from different feature stores.