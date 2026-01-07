# Azure - Getting started with AKS

Kubernetes and Helm are used to install & run Hopsworks and the Feature Store
in the cloud.
They both integrate seamlessly with third-party platforms such as Databricks,
SageMaker and KubeFlow.
This guide shows how to set up the Hopsworks platform in your organization's Azure account.

## Prerequisites

To follow the instruction on this page you will need the following:

- Kubernetes Version: Hopsworks can be deployed on AKS clusters running Kubernetes >= 1.27.0.
- An Azure resource group in which the Hopsworks cluster will be deployed.
- The [azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) installed and [logged in](https://docs.microsoft.com/en-us/cli/azure/authenticate-azure-cli).
- kubectl (to manage the AKS cluster)
- helm (to deploy Hopsworks)

### Permissions

The deployment requires cluster admin access to create ClusterRoles, ServiceAccounts, and ClusterRoleBindings in AKS.

A namespace is also required for deploying the Hopsworks stack.
If you don’t have permissions to create a namespace, ask your AKS administrator to provision one for you.

To run all the commands on this page the user needs to have at least the following permissions on the Azure resource group:

You will also need to have a role such as *Application Administrator* on the Azure Active Directory to be able to create the hopsworks.ai service principal.

## Step 1: Azure Kubernetes Service (AKS) Setup

### Step 1.1: Create an Azure Blob Storage Account

Create a storage account to host project data.
Ensure that the storage account is in the same region as the AKS cluster for performance and cost reasons:

```bash
az storage account create --name $STORAGE_ACCOUNT_NAME --resource-group $RESOURCE_GROUP --location $REGION
```

Also, create the corresponding container:

```bash
az storage container create --account-name $STORAGE_ACCOUNT_NAME --name $CONTAINER_NAME
```

### Step 1.2: Create an Azure Container Registry (ACR)

Create an ACR to store the images used by Hopsworks:

```bash
az acr create --resource-group $RESOURCE_GROUP --name $CONTAINER_REGISTRY_NAME --sku Basic --location $REGION

export ACR_ID=`az acr show --name $CONTAINER_REGISTRY_NAME --resource-group $RESOURCE_GROUP --query "id" --output tsv`
```

### Step 1.3: Create a User-Assigned Managed Identity

Create a user-assigned managed identity to grant AKS access to the storage account and container registry:

```bash
az identity create --name $UA_IDENTITY_NAME --resource-group $RESOURCE_GROUP

export UA_IDENTITY_PRINCIPAL_ID=`az identity show --name $UA_IDENTITY_NAME --resource-group $RESOURCE_GROUP --query principalId --output tsv`
export UA_IDENTITY_CLIENT_ID=`az identity show --name $UA_IDENTITY_NAME --resource-group $RESOURCE_GROUP --query clientId --output tsv`
export UA_IDENTITY_RESOURCE_ID=`az identity show --name $UA_IDENTITY_NAME --resource-group $RESOURCE_GROUP --query id --output tsv`
```

### Step 1.4: Grant permissions to the User-Assigned Managed Identity

Create a custom role definition with the minimum permissions needed to read and write to the storage account:

```bash
export STORAGE_ID=`az storage account show --name $STORAGE_ACCOUNT_NAME --resource-group $RESOURCE_GROUP --query "id" --output tsv`

az role definition create --role-definition '{
  "Name": "hopsfs-storage-permissions",
  "IsCustom": true,
  "Description": "Allow HopsFS to access the storage container",
  "Actions": [
    "Microsoft.Storage/storageAccounts/blobServices/containers/write",
    "Microsoft.Storage/storageAccounts/blobServices/containers/read",
    "Microsoft.Storage/storageAccounts/blobServices/write",
    "Microsoft.Storage/storageAccounts/blobServices/read",
    "Microsoft.Storage/storageAccounts/listKeys/action"
  ],
  "NotActions": [],
  "DataActions": [
    "Microsoft.Storage/storageAccounts/blobServices/containers/blobs/delete",
    "Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read",
    "Microsoft.Storage/storageAccounts/blobServices/containers/blobs/move/action",
    "Microsoft.Storage/storageAccounts/blobServices/containers/blobs/write"
  ],
  "AssignableScopes": [
    "'$STORAGE_ID'"
  ]
}'

az role assignment create --role hopsfs-storage-permissions --assignee-object-id $UA_IDENTITY_PRINCIPAL_ID --assignee-principal-type ServicePrincipal --scope $STORAGE_ID
```

### Step 1.5: Create Service Principal for Hopsworks services

Create a service principal to grant Hopsworks applications with access to the container registry.
For example, Hopsworks uses this service principal to push new Python environments created via the Hopsworks UI.

```bash
export SP_PASSWORD=`az ad sp create-for-rbac --name $SP_NAME --scopes $ACR_ID --role AcrPush --years 1 --query "password" --output tsv`
export SP_USER_NAME=`az ad sp list --display-name $SP_NAME --query "[].appId" --output tsv`
export SP_RESOURCE_ID=`az ad sp list --display-name $SP_NAME --query "[].id" --output tsv`

az role assignment create --role AcrDelete --assignee-object-id $SP_RESOURCE_ID --assignee-principal-type ServicePrincipal --scope $ACR_ID
```

### Step 1.6: Create an AKS Kubernetes Cluster

Provision an AKS cluster with a number of nodes:

```bash
az aks create --resource-group $RESOURCE_GROUP --name $KUBERNETES_CLUSTER_NAME --network-plugin azure \
    --enable-cluster-autoscaler --min-count 1 --max-count 4 --node-count 3 --node-vm-size Standard_D8_v4 \
    --attach-acr $CONTAINER_REGISTRY_NAME \
    --assign-identity $UA_IDENTITY_RESOURCE_ID --assign-kubelet-identity $UA_IDENTITY_RESOURCE_ID \
    --enable-managed-identity --generate-ssh-keys
```

## Step 2: Configure kubectl

```bash
az aks get-credentials --resource-group $RESOURCE_GROUP --name $KUBERNETES_CLUSTER_NAME --file ~/my-aks-kubeconfig.yaml
export KUBECONFIG=~/my-aks-kubeconfig.yaml
kubectl config current-context
```

## Step 3: Create Secret for the Service Principal

### Step 3.1: Create Hopsworks namespace

```bash
kubectl create namespace hopsworks
```

### Step 3.2: Create secret

```bash
kubectl create secret docker-registry azregcred \
    --namespace hopsworks \
    --docker-server=$CONTAINER_REGISTRY_NAME.azurecr.io \
    --docker-username=$SP_USER_NAME \
    --docker-password=$SP_PASSWORD
```

## Step 4: Setup Hopsworks for Deployment

### Step 4.1: Add the Hopsworks Helm repository

To obtain access to the Hopsworks helm chart repository, please [obtain](https://www.hopsworks.ai/try) an evaluation/startup licence.

Once you have the helm chart repository URL, replace the environment
variable $HOPSWORKS_REPO in the following command with this URL.

```bash
helm repo add hopsworks $HOPSWORKS_REPO
helm repo update hopsworks
```

### Step 4.2: Create helm values file

Below is a simplifield values.azure.yaml file to get started which can be updated for improved performance and further customisation.

```yaml
global:
  _hopsworks:
    storageClassName: null
    cloudProvider: "AZURE"
    managedDockerRegistery:
      enabled: true
      domain: "CONTAINER_REGISTRY_NAME.azurecr.io"
      namespace: "hopsworks"
      credHelper:
        enabled: false
        secretName: ""

    minio:
      enabled: false

hopsworks:
  variables:
    docker_operations_managed_docker_secrets: &azregcred "azregcred"
    docker_operations_image_pull_secrets: *azregcred
  dockerRegistry:
    preset:
      usePullPush: false
      secrets:
        - *azregcred

hopsfs:
  objectStorage:
    enabled: true
    provider: "AZURE"
    azure:
      storage:
        account: "STORAGE_ACCOUNT_NAME"
        container: "STORAGE_ACCOUNT_CONTAINER_NAME"
        identityClientId: "UA_IDENTITY_CLIENT_ID"

```

## Step 5: Deploy Hopsworks

Deploy Hopsworks in the created namespace.

```bash
helm install hopsworks hopsworks/hopsworks --namespace hopsworks --values values.azure.yaml --timeout=600s
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

## Step 6: Next steps

Check out our other guides for how to get started with Hopsworks and the Feature Store:

- Get started with the [Hopsworks Feature Store](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/quickstart.ipynb){:target="_blank"}
- Follow one of our [tutorials](../../tutorials/index.md)
- Follow one of our [Guide](../../user_guides/index.md)
