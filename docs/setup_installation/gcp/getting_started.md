# GCP - Getting started with GKE

Kubernetes and Helm are used to install & run Hopsworks and the Feature Store
in the cloud.
They both integrate seamlessly with third-party platforms such as Databricks,
SageMaker and KubeFlow.
This guide shows how to set up the Hopsworks platform in your organization's Google Cloud Platform's (GCP) account.

## Prerequisites

To follow the instruction on this page you will need the following:

- Kubernetes Version: Hopsworks can be deployed on GKE clusters running Kubernetes >= 1.27.0.
- [gcloud CLI](https://cloud.google.com/sdk/gcloud) to provision the GCP resources
- [gke-gcloud-auth-plugin](https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke) to manage authentication with the GKE cluster
- [helm](https://helm.sh/) to deploy Hopsworks

### Permissions

- The deployment requires cluster admin access to create ClusterRoles, ServiceAccounts, and ClusterRoleBindings.

- A namespace is required to deploy the Hopsworks stack.
If you don’t have permissions to create a namespace, ask your GKE administrator to provision one.

## Step 1: GCP GKE Setup

### Step 1.1: Create a Google Cloud Storage (GCS) bucket

Create a bucket to store project data.
Ensure the bucket is in the same region as your GKE cluster for performance and cost optimization.

```bash
gsutil mb -l $region gs://$bucket_name
```

### Step 1.2: Create Service Account

Create a file named `hopsworksai_role.yaml` with the following content:

```bash
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
- artifactregistry.repositories.create
- artifactregistry.repositories.get
- artifactregistry.repositories.uploadArtifacts
- artifactregistry.repositories.downloadArtifacts
- artifactregistry.tags.list
- artifactregistry.tags.delete
```

Execute the following gcloud command to create a custom role from the file.
Replace $PROJECT_ID with your GCP project id:

```bash
gcloud iam roles create hopsworksai_instances \
  --project=$PROJECT_ID \
  --file=hopsworksai_role.yaml
```

Execute the following gcloud command to create a service account for Hopsworks AI instances.
Replace $PROJECT_ID with your GCP project id:

```bash
gcloud iam service-accounts create hopsworksai_instances \
  --project=$PROJECT_ID \
  --description="Service account for Hopsworks AI instances" \
  --display-name="Hopsworks AI instances"
```

Execute the following gcloud command to bind the custom role to the service account.
Replace all occurrences $PROJECT_ID with your GCP project id:

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:hopsworks-ai-instances@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="projects/$PROJECT_ID/roles/hopsworksai_instances"
```

### Step 1.3: Create a GKE Cluster

```bash
gcloud container clusters create <cluster-name> \
  --zone <zone> \
  --machine-type n2-standard-8 \
  --num-nodes 1 \
  --enable-ip-alias \
  --service-account my-service-account@my-project.iam.gserviceaccount.com
```

Once the creation process is completed, you should be able to access the cluster using the kubectl CLI tool:

```bash
kubectl get nodes
```

### Step 1.4: Create GCR repository

Hopsworks allows users to customize images for Python jobs, Jupyter Notebooks, and (Py)Spark applications.
These images should be stored in Google Container Registry (GCR).
The GKE cluster needs access to a GCR repository to push project images.

Enable Artifact Registry and create a GCR repository to store images:

```bash
gcloud artifacts repositories create <repo-name> \
  --repository-format=docker \
  --location=<region>
```

## Step 3: Setup Hopsworks for Deployment

### Step 3.1: Add the Hopsworks Helm repository

To obtain access to the Hopsworks helm chart repository, please obtain
an evaluation/startup licence [here](https://www.hopsworks.ai/try).

Once you have the helm chart repository URL, replace the environment
variable $HOPSWORKS_REPO in the following command with this URL.

```bash
helm repo add hopsworks $HOPSWORKS_REPO
helm repo update hopsworks
```

### Step 3.2: Create Hopsworks namespace

```bash
kubectl create namespace hopsworks
```

### Step 3.3: Create helm values file

Below is a simplifield values.gcp.yaml file to get started which can be updated for improved performance and further customisation.

```bash
global:
  _hopsworks:
    storageClassName: null
    cloudProvider: "GCP"
    managedDockerRegistery:
      enabled: true
      domain: "europe-north1-docker.pkg.dev"
      namespace: "PROJECT_ID/hopsworks"
      credHelper:
        enabled: true
        secretName: &gcpregcred "gcpregcred"

    managedObjectStorage:
      enabled: true
      s3:
        bucket:
          name: &bucket "hopsworks"
        region: &region "europe-north1"
        endpoint: &gcpendpoint "https://storage.cloud.google.com"
        secret:
          name: &gcpcredentials "gcp-credentials"
          acess_key_id: &gcpaccesskey "access-key-id"
          secret_key_id: &gcpsecretkey "secret-access-key"
    minio:
      enabled: false
```

## Step 4: Deploy Hopsworks

Deploy Hopsworks in the created namespace.

```bash
helm install hopsworks hopsworks/hopsworks \
  --namespace hopsworks \
  --values values.gcp.yaml \
  --timeout=600s
```

Check that Hopsworks is installing on your provisioned AKS cluster.

```bash
kubectl get pods --namespace=hopsworks

kubectl get svc -n hopsworks -o wide
```

Upon completion (circa 20 minutes), setup a load balancer to access Hopsworks:

```bash
kubectl expose deployment hopsworks --type=LoadBalancer --name=hopsworks-service --namespace <namespace>
```

## Step 5: Next steps

Check out our other guides for how to get started with Hopsworks and the Feature Store:

- Get started with the [Hopsworks Feature Store](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/quickstart.ipynb){:target="_blank"}
- Follow one of our [tutorials](../../tutorials/index.md)
- Follow one of our [Guide](../../user_guides/index.md)
