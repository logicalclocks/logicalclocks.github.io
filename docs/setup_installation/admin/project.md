---
description: Guide on how to manage projects and quotas as a Hopsworks administrator
---

# Manage Projects

Hopsworks provides an administrator with a view of the projects in a Hopsworks cluster.

A Hopsworks administrator is not automatically a member of all the projects in a cluster.
However, they can see which projects exist, who is the project owner, and they can limit the storage quota and compute quota for each project.

## Prerequisites

You need to be an administrator on a Hopsworks cluster.

## Changing project quotas

You can find the Project management page by clicking on your name, in the top right corner of the navigation bar, and choosing _Cluster Settings_ from the dropdown menu and going to the _Project_ tab.

<figure>
  <img src="../../../assets/images/admin/projects/project_list.png" alt="Project page" />
  <figcaption>Project page</figcaption>
</figure>

This page will list all the projects in a cluster, their name, owner and when its quota was last updated.
By clicking on the _edit configuration_ link of a project you will be able to edit the quotas of that project.

<figure>
  <img src="../../../assets/images/admin/projects/project_quotas.png" alt="Project quotas" />
  <figcaption>Project quotas</figcaption>
</figure>

### Storage

Storage quota represents the amount of data a project can store.
The storage quota is broken down in three different areas:

- **Feature Store**: This represents the storage quota for files and directories stored in the `_featurestore.db` dataset in the project.
This dataset contains all the feature group offline data for the project.
- **Hive DB**: This represents the storage quota for files and directories stored in the `[projectName].db` dataset in the project.
This is a general purpose Hive database for the project that can be used for analytics.
- **Project**: This represents the storage quota for all the data stored on any other dataset.

Each storage quota is divided into space quota, i.e., how much space the files can consume, and namespace quota, i.e., how many files and directories there can be.
If Hopsworks is deployed on-premise using hard drives to store the data, i.e., Hopsworks is not configured to store its data in a S3-compliant storage system, the data is replicated across multiple nodes (by default 3) and the space quota takes the replication factor into consideration.
As an example, a 100MB file stored with a replication factor of 3, will consume 300MB of space quota.

By default, all storage quotas are disabled and not enforced.
Administrators can change this default by changing the following configuration in the [Configuration](../admin/variables.md) UI and/or the cluster definition:

```
hopsworks:
    featurestore_default_quota: [default quota in bytes, -1 to disable]
    hdfs_default_quota: [default quota in bytes, -1 to disable]
    hive_default_quota: [default quota in bytes, -1 to disable]
```

The values specified will be set during project creation and administrators will be able to customize each project using this UI.

### Compute

Compute quotas represents the amount of compute a project can use to run Spark and Flink applications as well as Tez queries.
Quota is expressed as number of seconds a container of size 1 CPU and 1GB of RAM can run for.

If the Hopsworks cluster is connected to a Kubernetes cluster, Python jobs, Jupyter notebooks and KServe models are not subject to the compute quota.
Currently, Hopsworks does not support defining quotas for compute scheduled on the connected Kubernetes cluster.

By default, the compute quota is disabled.
Administrators can change this default by changing the following configuration in the [Configuration](../admin/variables.md) UI and/or the cluster definition:

```
hopsworks:
    yarn_default_payment_type: [NOLIMIT to disable the quota, PREPAID to enable it]
    yarn_default_quota: [default quota in seconds]
```

The values specified will be set during project creation and administrators will be able to customize each project using this UI.

### Kakfa Topics

Kafka is used within Hopsworks to enable users to write data to the feature store in Real-Time and from a variety of different frameworks.
If a user creates a feature group with the stream APIs enabled, then a Kafka topic will be created for that feature group.
By default, a project can have up to 100 Kafka topics.
Administrators can increase the number of Kafka topics a project is allowed to create by increasing the quota in the project admin UI.

## Force deleting a project

Administrators have the option to force delete a project.
This is useful if the project was not created or deleted properly, e.g., because of an error.

## Controlling who can create projects

Every user on Hopsworks can create projects.
By default, each user can create up to 10 projects.
For production environments, the number of projects should be limited and controlled for resource allocation purposes as well as closer control over the data.
Administrators can control how many projects a user can provision by setting the following configuration in the [Configuration](../admin/variables.md) UI and/or cluster definition:

```
hopsworks:
    max_num_proj_per_user: [Maximum number of projects each user can create]
```

This value will be set when the user is provisioned.
Administrators can grant additional projects to a specific user through the [User Administration](../admin/user.md) UI.
