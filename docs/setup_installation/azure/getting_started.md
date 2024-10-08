# Azure - Getting started with AKS

Kubernetes and Helm are used to install & run Hopsworks and the Feature Store
in the cloud. They both integrate seamlessly with third-party platforms such as Databricks,
SageMaker and KubeFlow. This guide shows how to set up the Hopsworks platform in your organization's Azure account.

## Prerequisites

To follow the instruction on this page you will need the following:

- Kubernetes Version: Hopsworks can be deployed on AKS clusters running Kubernetes >= 1.27.0.
- An Azure resource group in which the Hopsworks cluster will be deployed. 
- The [azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) installed and [logged in](https://docs.microsoft.com/en-us/cli/azure/authenticate-azure-cli).
- kubectl (to manage the AKS cluster)
- helm (to deploy Hopsworks)

### Permissions

The deployment requires cluster admin access to create ClusterRoles, ServiceAccounts, and ClusterRoleBindings in AKS.

A namespace is also required for deploying the Hopsworks stack. If you don’t have permissions to create a namespace, ask your AKS administrator to provision one for you.
	
To run all the commands on this page the user needs to have at least the following permissions on the Azure resource group:

You will also need to have a role such as *Application Administrator* on the Azure Active Directory to be able to create the hopsworks.ai service principal.

## Step 1: Azure AKS Setup

### Step 1.1: Create an Azure Blob Storage Account

Create a storage account to host project data. Ensure that the storage account is in the same region as the AKS cluster for performance and cost reasons:

```bash
az storage account create --name $storage_account_name --resource-group $resource_group --location $region
```

Also create a corresponding container:

```bash
az storage container create --account-name $storage_account_name --name $container_name
```


### Step 1.2: Create an Azure Container Registry (ACR)

Create an ACR to store the images used by Hopsworks:

```bash
az acr create --resource-group $resource_group --name $registry_name --sku Basic --location $region
```

### Step 1.3: Create an AKS Kubernetes Cluster

Provision an AKS cluster with a number of nodes:

```bash
az aks create --resource-group $resource_group --name $cluster_name --enable-cluster-autoscaler --min-count 1 --max-count 4 --node-count 3 --node-vm-size Standard_D16_v4 --network-plugin azure --enable-managed-identity --generate-ssh-keys
```

### Step 1.4: Retrieve setup Identifiers

Create a set of environment variables for use in later steps.

```bash
export managed_id=`az aks show --resource-group $resource_group --name $cluster_name --query "identity.principalId" --output tsv`

export storage_id=`az storage account show --name $storage_account_name --resource-group $resource_group --query "id" --output tsv`

export acr_id=`az acr show --name $registry_name --resource-group $resource_group --query "id" --output tsv`
```

### Step 1.5: Assign Roles to Managed Identity

```bash
az role assignment create --assignee $managed_id --role "Storage Blob Data Contributor" --scope $storage_id

az role assignment create --assignee $managed_id --role AcrPull --scope $acr_id
az role assignment create --assignee $managed_id --role "AcrPush" --scope $acr_id
az role assignment create --assignee $managed_id --role "AcrDelete" --scope $acr_id
```

### Step 1.6: Allow AKS cluster access to ACR repository.

```bash
az aks update --resource-group $resource_group --name $cluster_name --attach-acr $registry_name
```

## Step 2: Configure kubectl

```bash
az aks get-credentials --resource-group $resource_group --name $cluster_name --file ~/my-aks-kubeconfig.yaml
export KUBECONFIG=~/my-aks-kubeconfig.yaml
kubectl config current-context
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

Below is a simplifield values.azure.yaml file to get started which can be updated for improved performance and further customisation.

```bash
global:
  _hopsworks:
    storageClassName: null
    cloudProvider: "AWS"
    managedDockerRegistry:
      enabled: true
      domain: "rchopsworksrepo.azurecr.io"
      namespace: "hopsworks"
    
    managedObjectStorage:
      enabled: true
      endpoint: "https://rchopsworksbucket.blob.core.windows.net"
    minio:
      enabled: false
```

## Step 4: Deploy Hopsworks

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



## Step 5: Next steps

Check out our other guides for how to get started with Hopsworks and the Feature Store:

* Get started with the [Hopsworks Feature Store](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/quickstart.ipynb){:target="_blank"}
* Follow one of our [tutorials](../../tutorials/index.md)
* Follow one of our [Guide](../../user_guides/index.md)

