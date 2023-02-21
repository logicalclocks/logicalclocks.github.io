# Upgrade existing clusters on managed.hopsworks.ai from version 3.0 or newer (Azure)
This guide shows you how to upgrade your existing Hopsworks cluster to a newer version of Hopsworks.

## Step 1: Make sure your cluster is running

It is important that your cluster is **Running**. Otherwise you will not be able to upgrade. As soon as a new version is available an upgrade notification will appear:

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/azure-notification-running-3.0.png" alt="New version notification">
    <figcaption>A new Hopsworks version is available</figcaption>
  </figure>
</p>

## Step 2: Add backup permissions to your role connected to managed.hopsworks.ai

We require extra permission to be added to the role you used to connect to [managed.hopsworks.ai](https://managed.hopsworks.ai), the one that you have created in [Getting started Step 1.2](../getting_started/#step-12-creating-a-custom-role-for-hopsworksai).  These permissions are required to create a snapshot of your cluster before proceeding with the upgrade. 

```json
"actions": [
    "Microsoft.Compute/snapshots/write",
    "Microsoft.Compute/snapshots/read",
    "Microsoft.Compute/snapshots/delete",
    "Microsoft.Compute/disks/beginGetAccess/action",
  ]
```

If you don't remember the name of the role that you have created in [Getting started Step 1.2](../getting_started/#step-12-creating-a-custom-role-for-hopsworksai), you can navigate to your Resource group, (1) click on *Access Control*, (2) navigate to the *Check Access* tab, (3) search for *hopsworks.ai*, (4) click on it, (5) now you have the name of your custom role used to connect to [managed.hopsworks.ai](https://managed.hopsworks.ai). 

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/azure-get-connected-hopswork.ai-role.png" alt="Get your connected role to managed.hopsworks.ai">
    <figcaption>Get your role connected to managed.hopsworks.ai</figcaption>
  </figure>
</p>

To edit the permissions associated with your role, stay on the same *Access Control* page, (1) click on the *Roles* tab, (2) search for your role name (the one you obtained above), (3) click on **...**, (4) click on *Edit*.


<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/azure-edit-connected-hopsworks.ai-role.png" alt="Edit your connected role to managed.hopsworks.ai">
    <figcaption>Edit your role connected to managed.hopsworks.ai</figcaption>
  </figure>
</p>

You will arrive at the *Update a custom role* page as shown below:

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/azure-edit-connected-hopsworks.ai-role-1.png" alt="Edit your connected role to managed.hopsworks.ai 1">
    <figcaption>Edit your role connected to managed.hopsworks.ai</figcaption>
  </figure>
</p>

Navigate to the *JSON* tab, then click on *Edit*, as shown below:

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/azure-edit-connected-hopsworks.ai-role-2.png" alt="Edit your connected role to managed.hopsworks.ai 2">
    <figcaption>Edit your role connected to managed.hopsworks.ai</figcaption>
  </figure>
</p>

Now, add the following permissions to the list of actions, then click on *Save*, click on *Review + update*, and finally click on *Update*.

```json
    "Microsoft.Compute/snapshots/write",
    "Microsoft.Compute/snapshots/read",
    "Microsoft.Compute/snapshots/delete",
    "Microsoft.Compute/disks/beginGetAccess/action",
```

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/azure-edit-connected-hopsworks.ai-role-3-2.4.png" alt="Edit your connected role to managed.hopsworks.ai 3">
    <figcaption>Add missing permissions to your role connected to managed.hopsworks.ai</figcaption>
  </figure>
</p>

## Step 3: Create an ACR Container Registry
We have enforced using managed docker registry (ECR) starting from Hopsworks version 3.1.0, so you need to create an ACR container registry and configure your managed identity to allow access to the container registry. First, get the name of the managed identity used in your cluster by clicking on the *Details* tab and check the name shown infront of *Managed Identity*. Then, follow [this guide](../getting_started/#step-31-create-an-acr-container-registry) to create and configure an ACR container registry.

## Step 4: Run the upgrade process

You need to click on *Upgrade* to start the upgrade process. You will be prompted with the screen shown below to confirm your intention to upgrade: 

!!! note
    No need to worry about the steps shown below if you have already completed [Step 2](#step-2-add-backup-permissions-to-your-role-connected-to-hopsworksai) and [Step 3](#step-3-create-an-acr-container-registry)

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/azure-upgrade-prompt_3.0.png" alt="Azure Upgrade Prompt">
    <figcaption>Upgrade confirmation</figcaption>
  </figure>
</p>

Enter the name of your ACR container registry that you have created in [Step 3](#step-3-create-an-acr-container-registry) and check the *Yes, upgrade cluster* checkbox to proceed, then the *Upgrade* button will be activated as shown below:

!!! warning
    Currently, we only support upgrade for the head node and you will need to recreate your workers once the upgrade is successfully completed. 


<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/azure-upgrade-prompt-1_3.0.png" alt="Azure Upgrade Prompt">
    <figcaption>Upgrade confirmation</figcaption>
  </figure>
</p>


Depending on how big your current cluster is, the upgrade process may take from 1 hour to a few hours until completion.

!!! note
    We don't delete your old cluster until the upgrade process is successfully completed. 


<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/azure-upgrade-start_3.0.png" alt="Azure Upgrade starting">
    <figcaption>Upgrade is running</figcaption>
  </figure>
</p>

Once the upgrade is completed, you can confirm that you have the new Hopsworks version by checking the version number on the *Details* tab of your cluster.

For more details about error handling check [this guide](../upgrade_2.4/#error-handling)