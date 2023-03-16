# Limiting GCP permissions

[Managed.hopsworks.ai](https://managed.hopsworks.ai) requires a set of permissions to be able to manage resources in the user’s GCP project.
By default, these permissions are set to easily allow a wide range of different configurations and allow
us to automate as many steps as possible. While we ensure to never access resources we shouldn’t,
we do understand that this might not be enough for your organization or security policy.
This guide explains how to lock down access permissions following the IT security policy principle of least privilege.

## Default permissions 
This is the list of default permissions that are required by [managed.hopsworks.ai](https://managed.hopsworks.ai). If you prefer to limit these permissions, then proceed to the [next section](#limiting-the-account-service-account-permissions).

```yaml
{!setup_installation/gcp/gcp_permissions.yml!}
```

## Limiting the Account Service Account permissions

Some of the permissions set up when connection your GCP account to [managed.hopsworks.ai](https://managed.hopsworks.ai) ([here](getting_started.md#step-1-connecting-your-gcp-account)) can be removed under certain conditions.

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
The following permissions are only needed if you want [managed.hopsworks.ai](https://managed.hopsworks.ai) to create VPC and subnet for you.

```yaml
- compute.networks.create
- compute.networks.delete
- compute.networks.get
- compute.subnetworks.create
- compute.subnetworks.delete
- compute.subnetworks.get
- compute.firewalls.create
- compute.firewalls.delete
```

You can remove these permissions by creating your own VPC, subnet, and firewalls and selecting them during cluster creation. For the VPC to be accepted you will need to associate it with firewall rules with the following constraints:

- One firewall rule associated with the VPC must allow ingress communication on all ports for communication between sources with the [service account you will attach to the cluster nodes](getting_started.md#step-3-creating-a-service-account-for-your-cluster-instances) (source and target). To create such a rule, run the following command replacing *\$NETWORK* with the name of your VPC, *\$SERVICE_ACCOUNT* with the email of your service account, and *\$PROJECT_ID* with the id of your project:

```bash
gcloud compute firewall-rules create nodetonode --network=$NETWORK --allow=all --direction=INGRESS --target-service-accounts=$SERVICE_ACCOUNT --source-service-accounts=$SERVICE_ACCOUNTT --project=$PROJECT_ID
```

- We recommend that you have a firewall rule associated with the VPC allowing TCP ingress communication to ports 443 and 80. If you don't have a rule opening port 443 the cluster will not be accessible from the internet. If you don't have a rule opening port 80 your cluster will be created with a self-signed certificate. You will have to acknowledge it by checking the *Continue with self-signed certificate* check box during [subnet selection](cluster_creation.md#step-6-vpc-and-subnet-selection). If you have no rule, at cluster creation, allowing ingress communication on specific TCP ports [managed.hopsworks.ai](https://managed.hopsworks.ai) will not be able to open or close ports on your cluster. To create this rule, run the following command replacing *\$NETWORK* with the name of your VPC, *\$SERVICE_ACCOUNT* with the email of your service account and *\$PROJECT_ID* with the id of your project:

```bash
gcloud compute firewall-rules create inbound --network=$NETWORK --allow=all --direction=INGRESS --target-service-accounts=$SERVICE_ACCOUNT --allow=tcp:80,tcp:443 --source-ranges="0.0.0.0/0" --project=$PROJECT_ID
```

### Update Firewall

The following permission is only needed to open and close service ports on the cluster. If you are not intending to open and close these ports from [managed.hopsworks.ai](https://managed.hopsworks.ai) you can remove the permission.

```yaml
- compute.firewalls.update
```

## Limiting the Instances Service Account permissions

Some of the permissions set up for the instances service account used during cluster creation ([here](cluster_creation.md#step-4-select-the-service-account)) can be removed under certain conditions.

### Backups

If you do not intend to take backups or if you do not have access to this Enterprise feature you can remove the permissions that are only used by the backup feature when configuring your instances service account.
For this remove the following permission from [your instances service account](getting_started.md#step-21-creating-a-custom-role-for-accessing-storage):

```yaml
  storage.buckets.update
```