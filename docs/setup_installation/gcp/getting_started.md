# Getting started with Hopsworks.ai (Google Cloud Platform)

[Hopsworks.ai](https://managed.hopsworks.ai/) is our managed platform for running Hopsworks and the Feature Store
in the cloud. It integrates seamlessly with third-party platforms such as Databricks,
SageMaker and KubeFlow. This guide shows how to set up [Hopsworks.ai](https://managed.hopsworks.ai/) with your organization's Google Cloud Platform's (GCP) account.

## Prerequisite

To follow the instruction of this page you will need the following:
- A GCP project in which the hopsworks cluster will be deployed.
- The [gcloud CLI](https://cloud.google.com/sdk/gcloud)
- The [gsutil tool](https://cloud.google.com/storage/docs/gsutil)


## Step 1: Connecting your GCP account

[Hopsworks.ai](https://managed.hopsworks.ai/) deploys Hopsworks clusters to a project in your GCP account. [Hopsworks.ai](https://managed.hopsworks.ai/) uses service account keys to connect to your GCP project. To enable this, you need to create a service account in your GCP project. Assign to the service account the required permissions. And, create a service account key JSON. For more details about creating and managing service accounts steps in GCP, see [documentation](https://cloud.google.com/iam/docs/creating-managing-service-accounts).

In [Hopsworks.ai](https://managed.hopsworks.ai/) click on *Connect to GCP* or go to *Settings* and click on *Configure* next to *GCP*. This will direct you to a page with the instructions needed to create the service account and set up the connection. Follow the instructions.

!!! note 
    it is possible to limit the permissions that step up during this phase. For more details see [restrictive-permissions](restrictive_permissions.md).


<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/gcp/connect-gcp.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/gcp/connect-gcp.png" alt="GCP configuration page">
    </a>
    <figcaption>GCP configuration page</figcaption>
  </figure>
</p>

## Step 2: Creating and configuring a storage

The Hopsworks clusters deployed by [Hopsworks.ai](https://managed.hopsworks.ai/) store their data in a bucket in your GCP account. To enable this you need to create a bucket and to create a service account with permissions to access the storage.

### Step 2.1: Creating a custom role for accessing storage 

Create a file named *hopsworksai_instances_role.yaml* with the following content:

```yaml
title: Hopsworks AI Instances
description: Role that allows Hopsworks AI Instances to access resources
stage: GA
includedPermissions:
- storage.buckets.get
- storage.buckets.update
- storage.multipartUploads.abort
- storage.multipartUploads.create
- storage.multipartUploads.list
- storage.multipartUploads.listParts
- storage.objects.create
- storage.objects.delete
- storage.objects.get
- storage.objects.list
- storage.objects.update
```

!!! note 
    it is possible to limit the permissions that set up during this phase. For more details see [restrictive-permissions](restrictive_permissions.md#limiting-the-instances-service-account-permissions).

Execute the following gcloud command to create a custom role from the file. Replace \[PROJECT_ID\] with your GCP project id:

```
gcloud iam roles create hopsworksai_instances \
  --project=[PROJECT_ID] \
  --file=hopsworksai_instances_role.yaml
```

### Step 2.2: Creating a service account 

Execute the following gcloud command to create a service account for Hopsworks AI instances. Replace \[PROJECT_ID\] with your GCP project id:

```
gcloud iam service-accounts create hopsworks-ai-instances \
  --project=[PROJECT_ID] \
  --description="Service account for Hopsworks AI instances" \
  --display-name="Hopsworks AI instances"
```

Execute the following gcloud command to bind the custom role to the service account. Replace all occurrences \[PROJECT_ID\] with your GCP project id:

```
gcloud projects add-iam-policy-binding [PROJECT_ID] \
  --member="serviceAccount:hopsworks-ai-instances@[PROJECT_ID].iam.gserviceaccount.com" \
  --role="projects/[PROJECT_ID]/roles/hopsworksai_instances"
```

### Step 2.3: Creating a Bucket

Execute the following gsutil command to create a bucket. Replace all occurrences \[PROJECT_ID\] with your GCP project id and \[BUCKET_NAME\] by the name you want to give to your bucket:

```
gsutil mb -p [PROJECT_ID] gs://[BUCKET_NAME]
```

!!! note 
    The hopsworks cluster created by [Hopsworks.ai](https://managed.hopsworks.ai/) must be in the same region as the bucket. The above command will create the bucket in the US so in the following steps, you must deploy your cluster in a US region. If you want to deploy your cluster in another part of the word us the *-l* option of *gsutil md*. For more detail about creating buckets with gsutil see the [documentation](https://cloud.google.com/storage/docs/creating-buckets)

## Step 4: Deploying a Hopsworks cluster

In [Hopsworks.ai](https://managed.hopsworks.ai/), select *Create cluster*:

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common//create-instance.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/common/create-instance.png" alt="Create a Hopsworks cluster">
    </a>
    <figcaption>Create a Hopsworks cluster</figcaption>
  </figure>
</p>

Select the *Project* (1) in which you created your *Bucket* and *Service Account* (see above).

!!! note
    If the *Project* does not appear in the drop-down, make sure that you properly [Connected your GCP account](#step-1-connecting-your-gcp-account) for this project.

Name your cluster (2). Choose the *Region*(3) and *Zone*(4) in which to deploy the cluster.

!!! warning
    The cluster must be deployed in a region having access to the bucket you created above.

Select the *Instance type* (5) and *Local storage* (6) size for the cluster *Head node*.

Enter the name of the bucket you created [above](#step-23-creating-a-bucket) in *Cloud Storage Bucket* (7)

Press *Next*:

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/gcp/create-instance-general.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/gcp/create-instance-general.png" alt="General configuration">
    </a>
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
    <a  href="../../../assets/images/setup_installation/managed/common/create-instance-workers-static.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/common/create-instance-workers-static.png" alt="Create a Hopsworks cluster, static workers configuration">
    </a>
    <figcaption>Create a Hopsworks cluster, static workers configuration</figcaption>
  </figure>
</p>

Enter *Email* of the instances *service account* that you created [above](#step-22-creating-a-service-account). If you followed the instruction it should be *hopsworks-ai-instances@\[PROJECT_ID\].iam.gserviceaccount.com* with \[PROJECT_ID\] the name of your project:

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/gcp/create-instance-service-account.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/gcp/create-instance-service-account.png" alt="Set the instance service account">
    </a>
    <figcaption>Set the instance service account</figcaption>
  </figure>
</p>

To backup the storage bucket data when taking a cluster backup we need to set a retention policy for the bucket. You can deactivate the retention policy by setting this value to 0 but this will block you from taking any backup of your cluster. Choose the retention period in days and click on *Review and submit*.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/gcp/create-instance-backup.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/gcp/create-instance-backup.png" alt="Choose the backup retention policy">
    </a>
    <figcaption>Choose the backup retention policy</figcaption>
  </figure>
</p>

Review all information and select *Create*:

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/gcp/create-instance-review.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/gcp/create-instance-review.png" alt="Review cluster information">
    </a>
    <figcaption>Review cluster information</figcaption>
  </figure>
</p>

!!! note
    We skipped cluster creation steps that are not mandatory.

The cluster will start. This will take a few minutes:

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/booting.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/common/booting.png" alt="Booting Hopsworks cluster">
    </a>
    <figcaption>Booting Hopsworks cluster</figcaption>
  </figure>
</p>

As soon as the cluster has started, you will be able to log in to your new Hopsworks cluster. You will also be able to stop, restart or terminate the cluster.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/running.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/common/running.png" alt="Running Hopsworks cluster">
    </a>
    <figcaption>Running Hopsworks cluster</figcaption>
  </figure>
</p>

## Step 5: Next steps

Check out our other guides for how to get started with Hopsworks and the Feature Store:

* Make Hopsworks services [accessible from outside services](../common/services.md)
* Get started with the [Hopsworks Feature Store](https://docs.hopsworks.ai/feature-store-api/latest/quickstart)
* Get started with Machine Learning on Hopsworks: [HopsML](https://hopsworks.readthedocs.io/en/stable/hopsml/index.html#hops-ml)
* Get started with Hopsworks: [User Guide](https://hopsworks.readthedocs.io/en/stable/user_guide/user_guide.html#userguide)
* Code examples and notebooks: [hops-examples](https://github.com/logicalclocks/hops-examples)
