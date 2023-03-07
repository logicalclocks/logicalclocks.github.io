# Getting started with managed.hopsworks.ai (Azure)

[Managed.hopsworks.ai](https://managed.hopsworks.ai) is our managed platform for running Hopsworks and the Feature Store
in the cloud. It integrates seamlessly with third-party platforms such as Databricks,
SageMaker and KubeFlow. This guide shows how to set up [managed.hopsworks.ai](https://managed.hopsworks.ai) with your organization's Azure account.

## Prerequisites

To follow the instruction on this page you will need the following:

- An Azure resource group in which the Hopsworks cluster will be deployed. 
- The [azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) installed and [logged in](https://docs.microsoft.com/en-us/cli/azure/authenticate-azure-cli).

### Permissions
To run all the commands on this page the user needs to have at least the following permissions on the Azure resource group:

```json
Microsoft.Authorization/roleDefinitions/write
Microsoft.Authorization/roleAssignments/write
Microsoft.Compute/sshPublicKeys/generateKeyPair/action
Microsoft.Compute/sshPublicKeys/read
Microsoft.Compute/sshPublicKeys/write
Microsoft.ContainerRegistry/registries/operationStatuses/read
Microsoft.ContainerRegistry/registries/read
Microsoft.ContainerRegistry/registries/write
Microsoft.ManagedIdentity/userAssignedIdentities/write
Microsoft.Resources/subscriptions/resourcegroups/read
Microsoft.Storage/storageAccounts/write
```

You will also need to have a role such as *Application Administrator* on the Azure Active Directory to be able to create the hopsworks.ai service principal.

### Resource providers
For [managed.hopsworks.ai](https://managed.hopsworks.ai) to deploy a cluster the following resource providers need to be registered on your Azure subscription.

```json
Microsoft.Network
Microsoft.Compute
Microsoft.Storage
Microsoft.ManagedIdentity
```
This can be done by running the following commands:

!!!note
    To run these commands you need to have the following permission on your subscription: *Microsoft.Network/register/action*

```bash
az provider register --namespace 'Microsoft.Network'
az provider register --namespace 'Microsoft.Compute'
az provider register --namespace 'Microsoft.Storage'
az provider register --namespace 'Microsoft.ManagedIdentity'
```

### Other
All the commands have been written for a Unix system. These commands will need to be adapted to your terminal if it is not directly compatible.

All the commands use your default location. Add the *--location* parameter if you want to run your cluster in another location. Make sure to create the resources in the same location as you are going to run your cluster.

## Step 1: Connect your Azure account

[Managed.hopsworks.ai](https://managed.hopsworks.ai) deploys Hopsworks clusters to your Azure account. To enable this, you have to
create a service principal and a custom role for [managed.hopsworks.ai](https://managed.hopsworks.ai) granting access to your resource group.

<p align="center">
  <iframe
    title="Azure information video"
    style="width:700px; height: 370px;"
    src="https://www.youtube.com/embed/Pfx2b3UTt88"
    frameBorder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowFullScreen
  >
  </iframe>
</p>


### Step 1.1: Connect your Azure account

In [managed.hopsworks.ai](https://managed.hopsworks.ai/) click on *Connect to Azure* or go to *Settings* and click on *Configure* next to *Azure*. This will direct you to a page with the instructions needed to create the service principal and set up the connection. Follow the instructions.

!!! note 
    it is possible to limit the permissions that are set up during this phase. For more details see [restrictive-permissions](restrictive_permissions.md).
<p align="center">
  <figure>
    <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/azure/connect-azure-0.png" alt="Cloud account settings">
    <figcaption>Cloud account settings</figcaption>
  </figure>
</p>

## Step 2: Create a storage

!!! note 
    If you prefer using terraform, you can skip this step and the remaining steps, and instead, follow [this guide](../common/terraform.md#getting-started-with-azure).

The Hopsworks clusters deployed by [managed.hopsworks.ai](https://managed.hopsworks.ai) store their data in a storage container in your Azure account. To enable this you need to create a storage account.
This is done by running the following command, replacing *$RESOURCE_GROUP* with the name of your resource group.

```bash
az storage account create --resource-group $RESOURCE_GROUP --name hopsworksstorage$RANDOM
```

## Step 3: Create an ACR Container Registry

The Hopsworks clusters deployed by [managed.hopsworks.ai](https://managed.hopsworks.ai) store their docker images in a container registry in your Azure account. 
To create this storage account run the following command, replacing *$RESOURCE_GROUP* with the name of your resource group.

```bash
az acr create --resource-group $RESOURCE_GROUP --name hopsworksecr --sku Premium
```

To prevent the registry from filling up with unnecessary images and artifacts you can enable a retention policy. A retention policy will automatically remove untagged manifests after a specified number of days. To enable a retention policy, run the following command, replacing *$RESOURCE_GROUP* with the name of your resource group.

```bash
az acr config retention update --resource-group $RESOURCE_GROUP --registry hopsworksecr --status Enabled --days 7 --type UntaggedManifests
```

## Step 4: Create a managed identity
To allow the hopsworks cluster instances to access the storage account and the container registry, [managed.hopsworks.ai](https://managed.hopsworks.ai) assigns a managed identity to the cluster nodes. To enable this you need to:

- Create a managed identity
- Create a role with appropriate permission and assign it to the managed identity

### Step 4.1: Create a managed identity
You create a managed identity by running the following command, replacing *$RESOURCE_GROUP* with the name of your resource group.

```bash
identityId=$(az identity create --name hopsworks-instance --resource-group $RESOURCE_GROUP --query principalId -o tsv)
```

### Step 4.2: Create a role for the managed identity
To create a new role for the managed identity, first, create a file called *instance-role.json* with the following content. Replace *SUBSCRIPTION_ID* by your subscription id and *RESOURCE_GROUP* by your resource group

```json
{
  "Name": "hopsworks-instance",
  "IsCustom": true,
  "Description": "Allow the hopsworks instance to access the storage and the docker repository",
  "Actions": [
      "Microsoft.Storage/storageAccounts/blobServices/containers/write",
      "Microsoft.Storage/storageAccounts/blobServices/containers/read",
      "Microsoft.Storage/storageAccounts/blobServices/write",
      "Microsoft.Storage/storageAccounts/blobServices/read",
      "Microsoft.Storage/storageAccounts/listKeys/action",
      "Microsoft.ContainerRegistry/registries/artifacts/delete",
      "Microsoft.ContainerRegistry/registries/pull/read",
      "Microsoft.ContainerRegistry/registries/push/write"
  ],
  "NotActions": [

  ],
  "DataActions": [
      "Microsoft.Storage/storageAccounts/blobServices/containers/blobs/delete",
      "Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read",
      "Microsoft.Storage/storageAccounts/blobServices/containers/blobs/move/action",
      "Microsoft.Storage/storageAccounts/blobServices/containers/blobs/write"
  ],
  "AssignableScopes": [
    "/subscriptions/SUBSCRIPTION_ID/resourceGroups/RESOURCE_GROUP"
  ]
}
```
Then run the following command, to create the new role.

```bash
az role definition create --role-definition instance-role.json
```

Finally assign the role to the managed identity by running the following command, replacing *$RESOURCE_GROUP* with the name of your resource group.

```bash
az role assignment create --resource-group $RESOURCE_GROUP --role hopsworks-instance --assignee $identityId
```

!!!note 
    It takes several minutes between the time you create the managed identity and the time a role can be assigned to it. So if we get an error message starting by the following wait and retry: *Cannot find user or service principal in graph database*

## Step 5: Add an ssh key to your resource group

When deploying clusters, [managed.hopsworks.ai](https://managed.hopsworks.ai) installs an ssh key on the cluster's instances so that you can access them if necessary. For this purpose, you need to add an ssh key to your resource group.

To create an ssh key in your resource group run the following command, replacing *$RESOURCE_GROUP* with the name of your resource group.

```bash
az sshkey create --resource-group $RESOURCE_GROUP --name hopsworksKey 
```

!!!note
    the command returns the path to the private and public keys associated with this ssh key. You can also create a key from an existing public key as indicated in the [Azure documentation](https://learn.microsoft.com/en-us/cli/azure/sshkey?view=azure-cli-latest#az-sshkey-create)

## Step 6: Deploy a Hopsworks cluster

In [managed.hopsworks.ai](https://managed.hopsworks.ai), select *Create cluster*:

<p align="center">
  <figure>
    <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/common/create-instance.png" alt="Create a Hopsworks cluster">
    <figcaption>Create a Hopsworks cluster</figcaption>
  </figure>
</p>

Select the *Resource Group* (1) in which you created your *storage account* and *managed identity* (see above).

!!! note
    If the *Resource Group* does not appear in the drop-down, make sure that you properly [created and set the custom role](#step-12-creating-a-custom-role-for-hopsworksai) for this resource group.

Name your cluster (2). Your cluster will be deployed in the *Location* of your *Resource Group* (3).

Select the *Instance type* (4) and *Local storage* (5) size for the cluster *Head node*.

Check if you want to *Use customer-managed encryption key* (6)

Select the *storage account* (7) you created above in *Azure Storage account name*. The name of the container in which the data will be stored is displayed in *Azure Container name* (8), you can modify it if needed.

!!! note
    You can choose to use a container already existing in your *storage account* by using the name of this container, but you need to first make sure that this container is empty.

Enter the *Azure container registry name* (9) of the ACR registry created in [Step 3.1](#step-31-create-an-acr-container-registry)

Press *Next*:

<p align="center">
  <figure>
    <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/azure/create-instance-general.png" alt="General configuration">
    <figcaption>General configuration</figcaption>
  </figure>
</p>

Select the number of workers you want to start the cluster with (2).
Select the *Instance type* (3) and *Local storage* size (4) for the *worker nodes*.

!!! note
    It is possible to [add or remove workers](../common/adding_removing_workers.md) or to [enable autoscaling](../common/autoscaling.md) once the cluster is running.

Press *Next*:

<p align="center">
  <figure>
    <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/common/create-instance-workers-static.png" alt="Create a Hopsworks cluster, static workers configuration">
    <figcaption>Create a Hopsworks cluster, static workers configuration</figcaption>
  </figure>
</p>

Select the *SSH key* that you want to use to access cluster instances:

<p align="center">
  <figure>
    <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/azure/connect-azure-12.png" alt="Choose SSH key">
    <figcaption>Choose SSH key</figcaption>
  </figure>
</p>

Select the *User assigned managed identity* that you created above:

<p align="center">
  <figure>
    <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/azure/connect-azure-identity.png" alt="Choose the User assigned managed identity">
    <figcaption>Choose the User assigned managed identity</figcaption>
  </figure>
</p>


To backup the Azure blob storage data when taking a cluster backup we need to set a retention policy for the blob storage. You can deactivate the retention policy by setting this value to 0 but this will block you from taking any backup of your cluster. Choose the retention period in days and click on *Review and submit*.

<p align="center">
  <figure>
    <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/azure/connect-azure-backup.png" alt="Choose the backup retention policy">
    <figcaption>Choose the backup retention policy</figcaption>
  </figure>
</p>

Review all information and select *Create*:

<p align="center">
  <figure>
    <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/azure/connect-azure-17.png" alt="Review cluster information">
    <figcaption>Review cluster information</figcaption>
  </figure>
</p>

!!! note
    We skipped cluster creation steps that are not mandatory. You can find more details about these steps [here](cluster_creation.md)

The cluster will start. This will take a few minutes:

<p align="center">
  <figure>
    <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/common/booting.png" alt="Booting Hopsworks cluster">
    <figcaption>Booting Hopsworks cluster</figcaption>
  </figure>
</p>

As soon as the cluster has started, you will be able to log in to your new Hopsworks cluster. You will also be able to stop, restart or terminate the cluster.

<p align="center">
  <figure>
    <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/common/running.png" alt="Running Hopsworks cluster">
    <figcaption>Running Hopsworks cluster</figcaption>
  </figure>
</p>

## Step 7: Next steps

Check out our other guides for how to get started with Hopsworks and the Feature Store:

* Make Hopsworks services [accessible from outside services](../common/services.md)
* Get started with the [Hopsworks Feature Store](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/quickstart.ipynb){:target="_blank"}
* Follow one of our [tutorials](../../tutorials/index.md)
* Follow one of our [Guide](../../user_guides/index.md)
* Code examples and notebooks: [hops-examples](https://github.com/logicalclocks/hops-examples)
