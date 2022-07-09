# Upgrade existing clusters on Hopsworks.ai from version 2.4 or newer (Azure)
This guide shows you how to upgrade your existing Hopsworks cluster to a newer version of Hopsworks.

## Step 1: Make sure your cluster is running

It is important that your cluster is **Running**. Otherwise you will not be able to upgrade. As soon as a new version is available an upgrade notification will appear:

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/azure/azure-notification-running-2.4.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/azure-notification-running-2.4.png" alt="New version notification">
    </a>
    <figcaption>A new Hopsworks version is available</figcaption>
  </figure>
</p>

## Step 2: Add backup permissions to your role connected to Hopsworks.ai

We require extra permission to be added to the role you used to connect to Hopsworks.ai, the one that you have created in [Getting started Step 1.2](../getting_started/#step-12-creating-a-custom-role-for-hopsworksai).  These permissions are required to create a snapshot of your cluster before proceeding with the upgrade. 

```json
"actions": [
    "Microsoft.Compute/snapshots/write",
    "Microsoft.Compute/snapshots/read",
    "Microsoft.Compute/snapshots/delete",
    "Microsoft.Compute/disks/beginGetAccess/action",
  ]
```

If you don't remember the name of the role that you have created in [Getting started Step 1.2](../getting_started/#step-12-creating-a-custom-role-for-hopsworksai), you can navigate to your Resource group, (1) click on *Access Control*, (2) navigate to the *Check Access* tab, (3) search for *hopsworks.ai*, (4) click on it, (5) now you have the name of your custom role used to connect to hopsworks.ai. 

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/azure/azure-get-connected-hopswork.ai-role.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/azure-get-connected-hopswork.ai-role.png" alt="Get your connected role to hopsworks.ai">
    </a>
    <figcaption>Get your role connected to hopsworks.ai</figcaption>
  </figure>
</p>

To edit the permissions associated with your role, stay on the same *Access Control* page, (1) click on the *Roles* tab, (2) search for your role name (the one you obtained above), (3) click on **...**, (4) click on *Edit*.


<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/azure/azure-edit-connected-hopsworks.ai-role.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/azure-edit-connected-hopsworks.ai-role.png" alt="Edit your connected role to hopsworks.ai">
    </a>
    <figcaption>Edit your role connected to hopsworks.ai</figcaption>
  </figure>
</p>

You will arrive at the *Update a custom role* page as shown below:

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/azure/azure-edit-connected-hopsworks.ai-role-1.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/azure-edit-connected-hopsworks.ai-role-1.png" alt="Edit your connected role to hopsworks.ai 1">
    </a>
    <figcaption>Edit your role connected to hopsworks.ai</figcaption>
  </figure>
</p>

Navigate to the *JSON* tab, then click on *Edit*, as shown below:

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/azure/azure-edit-connected-hopsworks.ai-role-2.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/azure-edit-connected-hopsworks.ai-role-2.png" alt="Edit your connected role to hopsworks.ai 2">
    </a>
    <figcaption>Edit your role connected to hopsworks.ai</figcaption>
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
    <a  href="../../../assets/images/setup_installation/managed/azure/azure-edit-connected-hopsworks.ai-role-3-2.4.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/azure-edit-connected-hopsworks.ai-role-3-2.4.png" alt="Edit your connected role to hopsworks.ai 3">
    </a>
    <figcaption>Add missing permissions to your role connected to hopsworks.ai</figcaption>
  </figure>
</p>

## Step 3: Run the upgrade process

You need to click on *Upgrade* to start the upgrade process. You will be prompted with the screen shown below to confirm your intention to upgrade: 

!!! note
    No need to worry about the following message since this is done already in [Step 2](#step-2-add-backup-permissions-to-your-role-connected-to-hopsworksai)

    **Make sure that your custom role which you have connected to Hopsworks.ai has the following permissions:
    [ "Microsoft.Compute/snapshots/write", "Microsoft.Compute/snapshots/read", "Microsoft.Compute/snapshots/delete", "Microsoft.Compute/disks/beginGetAccess/action", ]**

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/azure/azure-upgrade-prompt_2.4.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/azure-upgrade-prompt_2.4.png" alt="Azure Upgrade Prompt">
    </a>
    <figcaption>Upgrade confirmation</figcaption>
  </figure>
</p>

Check the *Yes, upgrade cluster* checkbox to proceed, then the *Upgrade* button will be activated as shown below:

!!! warning
    Currently, we only support upgrade for the head node and you will need to recreate your workers once the upgrade is successfully completed. 


<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/azure/azure-upgrade-prompt-1_2.4.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/azure-upgrade-prompt-1_2.4.png" alt="Azure Upgrade Prompt">
    </a>
    <figcaption>Upgrade confirmation</figcaption>
  </figure>
</p>


Depending on how big your current cluster is, the upgrade process may take from 1 hour to a few hours until completion.

!!! note
    We don't delete your old cluster until the upgrade process is successfully completed. 


<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/azure/azure-upgrade-start_2.4.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/azure-upgrade-start_2.4.png" alt="Azure Upgrade starting">
    </a>
    <figcaption>Upgrade is running</figcaption>
  </figure>
</p>

Once the upgrade is completed, you can confirm that you have the new Hopsworks version by checking the version number on the *Details* tab of your cluster.

## Error handling
There are two categories of errors that you may encounter during an upgrade. First, a permission error due to a missing permission in your role connected to Hopsworks.ai, see [Error 1](#error-1-missing-permissions-error). Second, an error during the upgrade process running on your cluster, see [Error 2](#error-2-upgrade-process-error).

### Error 1: Missing permissions error

If one or more backup permissions are missing, or if the resource is not set correctly, you will be notified with an error message as shown below:

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/azure/azure-upgrade-permission-error_2.4.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/azure-upgrade-permission-error_2.4.png" alt="Azure upgrade permission error">
    </a>
    <figcaption>Missing permission error</figcaption>
  </figure>
</p>


Update your cross custom role as described in [Step 2](#step-2-add-backup-permissions-to-your-role-connected-to-hopsworksai), then click *Start*. Once the cluster is up and running, you can try running the upgrade again.

### Error 2: Upgrade process error

If an error occurs during the upgrade process, you will have the option to rollback to your old cluster as shown below: 

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/azure/azure-upgrade-error_2.4.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/azure-upgrade-error_2.4.png" alt="Error during upgrade">
    </a>
    <figcaption>Error occurred during upgrade</figcaption>
  </figure>
</p>

Click on *Rollback* to recover your old cluster before upgrade.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/azure/azure-rollback-prompt-1_2.4.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/azure-rollback-prompt-1_2.4.png" alt="Rollback prompt">
    </a>
    <figcaption>Upgrade rollback confirmation</figcaption>
  </figure>
</p>

Check the *Yes, rollback cluster* checkbox to proceed, then the *Rollback* button will be activated as shown below:

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/azure/azure-rollback-prompt-2_2.4.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/azure/azure-rollback-prompt-2_2.4.png" alt="Rollback prompt">
    </a>
    <figcaption>Upgrade rollback confirmation</figcaption>
  </figure>
</p>

Once the rollback is completed, you will be able to continue working as normal with your old cluster.

!!! note
    The old cluster will be **stopped** after the rollback. You have to click on the *Start* button.

