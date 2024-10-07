# AWS - Getting started

Kubernetes and Helm are used to install & run Hopsworks and the Feature Store
in the cloud. They both integrate seamlessly with third-party platforms such as Databricks,
SageMaker and KubeFlow. This guide shows how to set up the Hopsworks platform in your organization's AWS account.

## Prerequisites

To follow the instruction on this page you will need the following:

- Kubernetes Version: Hopsworks can be deployed on AKS clusters running Kubernetes >= 1.27.0.
- [aws-cli](https://aws.amazon.com/cli/) to provision the AWS resources 
- [eksctl](https://eksctl.io/) to interact with the AWS APIs and provision the EKS cluster
- [helm](https://helm.sh/) to deploy Hopsworks

## ECR Registry

Hopsworks allows users to customize the images used by Python jobs, Jupyter Notebooks and (Py)Spark applications running in their projects. The images are stored in ECR. Hopsworks needs access to an ECR repository to push the project images.

## Permissions

By default, the deployment requires cluster admin level access to be able to create a set of ClusterRoles, ServiceAccounts and ClusterRoleBindings. If you don’t have cluster admin level access, you can ask your administrator to provision the necessary ClusterRoles, ServiceAccounts and ClusterRoleBindings as described in the section below.

A namespace is required to deploy the Hopsworks stack. If you don’t have permissions to create a namespace you should ask your K8s administrator to provision one for you.


## EKS Deployment

The following steps describe how to deploy an EKS cluster and related resources so that it’s compatible with Hopsworks.


## Step 1: AWS EKS Setup

### Step 1.1: Create S3 Bucket

```bash
aws s3 mb s3://BUCKET_NAME --region REGION --profile PROFILE
```

### Step 1.2: Create ECR Repository

Create the repository to host the projects images. 

```bash
aws --profile PROFILE ecr create-repository --repository-name NAMESPACE/hopsworks-base --region REGION
```

### Step 1.3: Create IAM Policies

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "hopsworksaiInstanceProfile",
      "Effect": "Allow",
      "Action": [
        "S3:PutObject",
        "S3:ListBucket",
        "S3:GetObject",
        "S3:DeleteObject",
        "S3:AbortMultipartUpload",
        "S3:ListBucketMultipartUploads",
        "S3:PutLifecycleConfiguration",
        "S3:GetLifecycleConfiguration",
        "S3:PutBucketVersioning",
        "S3:GetBucketVersioning",
        "S3:ListBucketVersions",
        "S3:DeleteObjectVersion"
      ],
      "Resource": [
        "arn:aws:s3:::BUCKET_NAME/*",
        "arn:aws:s3:::BUCKET_NAME"
      ]
    },
    {
      "Sid": "AllowPushandPullImagesToUserRepo",
      "Effect": "Allow",
      "Action": [
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:CompleteLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:InitiateLayerUpload",
        "ecr:BatchCheckLayerAvailability",
        "ecr:PutImage",
        "ecr:ListImages",
        "ecr:BatchDeleteImage",
        "ecr:GetLifecyclePolicy",
        "ecr:PutLifecyclePolicy",
        "ecr:TagResource"
      ],
      "Resource": [
        "arn:aws:ecr:REGION:ECR_AWS_ACCOUNT_ID:repository/*/hopsworks-base"
      ]
    }
  ]
}
```

```bash
aws --profile PROFILE iam create-policy --policy-name POLICY_NAME --policy-document file://policy.json
```

### Step 1.4: Create EKS cluster using eksctl

When creating the cluster using eksctl the following parameters are required in the cluster configuration YAML file (eksctl.yaml):

- amiFamily should either be AmazonLinux2023 or Ubuntu2404

- Instance type should be Intel based or AMD (i.e not ARM)

- The following policies are required: [IAM policies - eksctl](https://eksctl.io/usage/iam-policies/#attaching-policies-by-arn)


```bash
- arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy
- arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy
- arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly
```

The following is required if you are using the EKS AWS Load Balancer Controller to grant permissions to the controller to provision the necessary load balancers [Welcome: AWS Load Balancer Controller](https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/)

```bash
      withAddonPolicies:
        awsLoadBalancerController: true 
```

You need to update the CLUSTER NAME and the POLICY ARN generated above

```bash
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: CLUSTER_NAME
  region: REGION
  version: "1.29" 

iam:
  withOIDC: true

managedNodeGroups:
  - name: ng-1
    amiFamily: AmazonLinux2023
    instanceType: m6i.2xlarge
    minSize: 1
    maxSize: 4
    desiredCapacity: 4
    volumeSize: 100
    ssh:
      allow: true # will use ~/.ssh/id_rsa.pub as the default ssh key
    iam:
      attachPolicyARNs:
        - arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy
        - arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy
        - arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly
        - arn:aws:iam::827555229956:policy/POLICYNAME
      withAddonPolicies:
        awsLoadBalancerController: true
addons:
  - name: aws-ebs-csi-driver
    wellKnownPolicies:      # add IAM and service account
      ebsCSIController: true
```

You can create the EKS cluster using the following eksctl command:

```bash
eksctl create cluster -f eksctl.yaml --profile PROFILE
```

Once the creation process is completed, you should be able to access the cluster using the kubectl CLI tool:

```bash
kubectl get nodes
```

You should see the list of nodes provisioned for the cluster.

### Step 1.4: Install the AWS LoadBalancer Addon

For Hopsworks to provision the necessary network and application load balancers, we need to install the AWS LoadBalancer plugin (See [AWS Documentation](https://docs.aws.amazon.com/eks/latest/userguide/lbc-helm.html) )
```bash
helm repo add eks https://aws.github.io/eks-charts
helm repo update eks
helm install aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system --set clusterName=CLUSTER_NAME
```

### Step 1.5: (Optional) Create GP3 Storage Class

By default EKS comes with GP2 as storage class. GP3 is more cost effective, we can use it with Hopsworks by creating the storage class

```bash
kubectl apply -f - <<EOF
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ebs-gp3
provisioner: ebs.csi.aws.com
parameters:
  csi.storage.k8s.io/fstype: xfs
  type: gp3
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
EOF
```

## Step 2: Hopsworks Deployment

This section describes the steps required to deploy the Hopsworks stack using Helm.

### Step 2.1: Add the Hopsworks Helm repository

- Configure Repo

```bash
helm repo add hopsworks-dev https://nexus.hops.works/repository/hopsworks-helm-dev --username NEXUS_USER --password NEXUS_PASS
helm repo update hopsworks-dev
```

- Create Hopsworks namespace 

```bash
kubectl create namespace hopsworks
```

- Create Hopsworks secrets 

```bash
kubectl create secret docker-registry regcred \
    --namespace=hopsworks \
    --docker-server=docker.hops.works \
    --docker-username=NEXUS_USER \
    --docker-password=NEXUS_PASS \
    --docker-email=NEXUS_EMAIL_ADDRESS
```

- Update values.aws.yml

```bash
global:
  _hopsworks:
    storageClassName: ebs-gp3
    cloudProvider: "AWS"
    managedDockerRegistery:
      enabled: true
      domain: "ECR_AWS_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com"
      namespace: "NAMESPACE"
      credHelper:
        enabled: true
        secretName: &awsregcred "awsregcred"
    minio:
      hopsfs:
        enabled: false
    externalLoadBalancers:
      enabled: true
      class: null
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-scheme: internet-facing

hopsworks:
  variables:
  ﻿  kube_kserve_installed: false
    docker_operations_managed_docker_secrets: *awsregcred
    docker_operations_image_pull_secrets: "regcred"
  dockerRegistry:
    preset:
      usePullPush: false
      secrets:
        - "regcred"
        - *awsregcred
  service:
    worker:
      external:
        http:
          type: NodePort
  ingress:
    enabled: true
    ingressClassName: alb
    annotations:
      alb.ingress.kubernetes.io/scheme: internet-facing
   
hopsfs:
  objectStorage:
    enabled: true
    provider: "S3"
    s3:
      bucket: 
        name: "BUCKET_NAME"
      region: "REGION"

consul:
  consul:
    server:
      storageClass: ebs-gp3
```


- Run the Helm install 

```bash
helm install hopsworks hopsworks-dev/hopsworks --namespace hopsworks --values values.aws.yaml --timeout=600s
```


Using the kubectl CLI tool, you can track the deployment process. You can use the command below to track which pods are running and which ones are in the process of being provisioned. You can also use the command below to detect any failure.

```bash
kubectl -n hopsworks get pods
```


## Step 3: Resources Created

Using the Helm chart and the values files the following resources are created:

Load Balancers:
```bash
    externalLoadBalancers:
      enabled: true
      class: null
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-scheme: internet-facing
```

Enabling the external load balancer in the values.yml file provisions the following load balancers for the following services:

- arrowflight : This load balancer is used to send queries from external clients to the Hopsworks Query Service

- kafka : This load balancer is used to send data to the Apache Kafka brokers for ingestion to the online feature store.

- rdrs: This load balancer is used to query online feature store data using the REST APIs

- mysql: This load balancer is used to query online feature store data using the MySQL APIs

- opensearch : This load balancer is used to query the Hopsworks vector database


On EKS using the AWS Load Balancers, the AWS controller deployed above will be responsible to provision the necessary load balancers. You can configure the load balancers using the annotations documented in the [AWS Load Balancer controller guide](https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/guide/ingress/annotations/)

You can enable/disable individual load balancers provisioning using the following values in the values.yml file:

- kafka.externalLoadBalancer.enabled

- opensearch.externalLoadBalancer.enabled

- rdrs.externalLoadBalancer.enabled

- mysql.externalLoadBalancer.enabled

Other load balancer providers are also supported by providing the appropriate controller, class and annotations.

Ingress:

```bash
  ingress:
    enabled: true
    ingressClassName: alb
    annotations:
      alb.ingress.kubernetes.io/scheme: internet-facing
```

Hopsworks UI and REST interface is available outside the K8s cluster using an Ingress. On AWS this is implemented by provisioning an application load balancer using the AWS load balancer controller.
As per the load balancer above, the controller checks for the following annotations: [Annotations - AWS Load Balancer Controller](https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/guide/ingress/annotations/)

HTTPS is required to access the Hopsworks UI, therefore you need to add the following annotation:

```bash
alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:us-west-2:xxxxx:certificate/xxxxxxx
```

To configure the TLS certificate the Application Load Balancer should use to terminate the connection. The certificate should be available in the [AWS Certificate Manager](https://aws.amazon.com/certificate-manager/)

Cluster Roles and Cluster Role Bindings:

By default a set of cluster roles are provisioned, if you don’t have permissions to provision cluster roles or cluster role bindings, you should reach out to your K8s administrator. You should then provide the appropriate resource names as value in the values.yml file.


## Step 4: Next steps

Check out our other guides for how to get started with Hopsworks and the Feature Store:

* Get started with the [Hopsworks Feature Store](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/quickstart.ipynb){:target="_blank"}
* Follow one of our [tutorials](../../tutorials/index.md)
* Follow one of our [Guide](../../user_guides/index.md)
