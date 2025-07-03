---
description: Documentation on how to configure a Databricks cluster to read and write features from the Hopsworks Feature Store
---
# Databricks Integration

Users can configure their Databricks clusters to write the results of feature engineering pipelines in the Hopsworks Feature Store using HSFS.
Configuring a Databricks cluster can be done from the Hopsworks Feature Store UI. This guide explains each step.

## Prerequisites

In order to be able to configure a Databricks cluster to use the Feature Store of your Hopsworks instance, it is necessary to ensure networking is setup correctly between the instances and that the Databricks cluster has access to the Hopsworks API key to perform requests with HSFS from Databricks to Hopsworks.

### Networking

If you haven't done so already, follow the networking guides for either [AWS](networking.md#aws) or [Azure](networking.md#azure) for instructions on how to configure networking properly between Databricks' VPC (or Virtual Network on Azure) and the [managed.hopsworks.ai](https://managed.hopsworks.ai) VPC/VNet.

### Hopsworks API key

In order for the Feature Store API to be able to communicate with the user's Hopsworks instance, the client library (HSFS) needs to have access to a previously generated API key from Hopsworks. For ways to setup and store the Hopsworks API key, please refer to the [API key guide for Databricks](api_key.md).

## Databricks API key

Hopsworks uses the Databricks REST APIs to communicate with the Databricks instance and configure clusters on behalf of users.
To achieve that, the first step is to register an instance and a valid API key in Hopsworks.

Users can get a valid Databricks API key by following the [Databricks Documentation](https://docs.databricks.com/dev-tools/api/latest/authentication.html#generate-a-personal-access-token)

!!! warning "Cluster access control"

    If users have enabled [Databricks Cluster access control](https://docs.databricks.com/security/access-control/cluster-acl.html#cluster-access-control), it is important that the users running the cluster configuration (i.e. the user generating the API key) has `Can Manage` privileges on the cluster they are trying to configure.

## Register a new Databricks Instance

To register a new Databricks instance, first navigate to `Project settings`, which can be found on the left-hand side of a Project's landing page, then select the `Integrations` tab.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/integrations/databricks/databricks-integration.png" alt="Hopsworks's Integrations page">
    <figcaption>Hopsworks's Integrations page</figcaption>
  </figure>
</p>

Registering a Databricks instance requires adding the instance address and the Databricks API key.

The instance name corresponds to the address of the Databricks instance and should be in the format `[UUID].cloud.databricks.com` (or `adb-[UUID].19.azuredatabricks.net` for Databricks on Azure), essentially the same web address used to reach the Databricks instance from the browser.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/integrations/databricks/databricks-integration-popup.png" alt="Register a Databricks Instance along with a Databricks API key">
    <figcaption>Register a Databricks Instance along with a Databricks API key</figcaption>
  </figure>
</p>

The API key will be stored in the Hopsworks secret store for the user and will be available only for that user.  If multiple users need to configure Databricks clusters, each has to generate an API key and register an instance. The Databricks instance registration does not have a project scope, meaning that once registered, the user can configure clusters for all projects they are part of.

## Databricks Cluster

A cluster needs to exist before users can configure it using the Hopsworks UI. The cluster can be in any state prior to the configuration.

!!! warning "Runtime limitation"

    Currently Runtime 12.2 LTS is suggested to be able to use the full suite of Hopsworks Feature Store capabilities.

## Configure a cluster

Clusters are configured for a project user, which, in Hopsworks terms, means a user operating within the scope of a project.
To configure a cluster, click on the `Configure` button. By default the cluster will be configured for the user making the request. If the user doesn't have `Can Manage` privilege on the cluster, they can ask a project `Data Owner` to configure it for them. Hopsworks `Data Owners` are allowed to configure clusters for other project users, as long as they have the required Databricks privileges.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/integrations/databricks/databricks-integration-cluster.png" alt="Configure a Databricks Cluster from Hopsworks">
    <figcaption>Configure a Databricks Cluster from Hopsworks</figcaption>
  </figure>
</p>

During the cluster configuration the following steps will be taken:

- Upload an archive to DBFS containing the necessary Jars for HSFS and HopsFS to be able to read and write from the Hopsworks Feature Store
- Add an initScript to configure the Jars when the cluster is started
- Install `hsfs` python library
- Configure the necessary Spark properties to authenticate and communicate with the Feature Store

!!! note "HopsFS configuration"
    It is not necessary to configure HopsFS if data is stored outside the Hopsworks file system. To do this define [Data Sources](../../fs/data_source/index.md) and link them to [Feature Groups](../../fs/feature_group/create.md) and [Training Datasets](../../fs/feature_view/training-data.md).

When a cluster is configured for a specific project user, all the operations with the Hopsworks Feature Store will be executed as that project user. If another user needs to re-use the same cluster, the cluster can be reconfigured by following the same steps above.

## Connecting to the Feature Store

At the end of the configuration, Hopsworks will start the cluster.
Once the cluster is running users can establish a connection to the Hopsworks Feature Store from Databricks:

```python
import hopsworks 
project = hopsworks.login(
    host='my_instance',                 # DNS of your Hopsworks instance
    port=443,                           # Port to reach your Hopsworks instance, defaults to 443
    project='my_project',               # Name of your Hopsworks project
    api_key_value='apikey',             # The API key to authenticate with Hopsworks
)
fs = project.get_feature_store()           # Get the project's default feature store
```

## Next Steps

For more information about how to connect, see the [Login API](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/api/login/) API reference. Or continue with the Data Source guide to import your own data to the Feature Store.
