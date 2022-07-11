# Limiting GCP permissions

Hopsworks.ai requires a set of permissions to be able to manage resources in the user’s GCP project.
By default, these permissions are set to easily allow a wide range of different configurations and allow
us to automate as many steps as possible. While we ensure to never access resources we shouldn’t,
we do understand that this might not be enough for your organization or security policy.
This guide explains how to lock down access permissions following the IT security policy principle of least privilege.

## Limiting the Account Service Account permissions

Some of the permissions set up when connection your GCP account to Hopsworks.ai ([here](getting_started.md#step-1-connecting-your-gcp-account)) can be removed under certain conditions.

### Backup permissions

The following permissions are only needed for the backup feature. If you are not going to create backups or if you do not have access to this Enterprise feature, you can limit the permission of the Service Account by removing them.

```yaml
- compute.disks.createSnapshot
- compute.snapshots.create
- compute.snapshots.delete
- compute.snapshots.setLabels
- compute.snapshots.get
- compute.snapshots.useReadOnly
```

### Instance type modification permissions

The following permission is only needed to be able to change the head node and RonDB nodes instance type on an existing cluster ([documentation](../common/scalingup.md)). If you are not going to use this feature, you can limit the permission of the Service Account by removing it.

```yaml
- compute.instances.setMachineType
```
### Create a VPC permissions
The following permissions are only needed if you want Hopsworks.ai to create VPC and subnet for you.
If you choose an existing VPC and subnet, you can limit the permission of the Service Account by removing them. 

```yaml
- compute.networks.create
- compute.networks.delete
- compute.networks.get
...
- compute.subnetworks.create
- compute.subnetworks.delete
- compute.subnetworks.get
```

## Limiting the Instances Service Account permissions

Some of the permissions set up for the instances service account used during cluster creation ([here](cluster_creation.md#step-4-select-the-service-account)) can be removed under certain conditions.

### Backups

If you do not intend to take backups or if you do not have access to this Enterprise feature you can remove the permissions that are only used by the backup feature when configuring your instances service account.
For this remove the following permission from [your instances service account](getting_started.md#step-21-creating-a-custom-role-for-accessing-storage):

```yaml
  storage.buckets.update
```