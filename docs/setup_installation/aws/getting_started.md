# AWS - Getting started with EKS

Kubernetes and Helm are used to install and run Hopsworks and the Feature Store in the cloud.
They both integrate seamlessly with third-party platforms such as Databricks, SageMaker and Kubeflow.
This guide shows how to set up the Hopsworks platform on Amazon EKS in your organization's AWS account.

## Prerequisites

To follow the instructions on this page you will need the following:

- Kubernetes version: Hopsworks supports EKS clusters running Kubernetes >= 1.27.0 and < 1.35.0 (the chart's supported range, enforced by its `kubeVersion` constraint).
  Pick a version in that range that is also under [AWS standard support](https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html), for example 1.33.
- [aws-cli](https://aws.amazon.com/cli/) to provision the AWS resources.
- [eksctl](https://eksctl.io/) to create and manage the EKS cluster.
- [kubectl](https://kubernetes.io/docs/tasks/tools/) to interact with the cluster.
- [helm](https://helm.sh/) to deploy Hopsworks.

### Permissions

- The deployment requires cluster admin access to create ClusterRoles, ServiceAccounts, and ClusterRoleBindings.
- A namespace is required to deploy the Hopsworks stack.
  If you don't have permissions to create a namespace, ask your EKS administrator to provision one.

## Step 1: AWS EKS setup

The following steps describe how to deploy an EKS cluster and the related resources so that it is compatible with Hopsworks.

### Step 1.1: Create an S3 bucket

Create a bucket to store project data.

```bash
aws s3 mb s3://BUCKET_NAME --region REGION --profile PROFILE
```

Enable versioning on the bucket.
The RonDB and OpenSearch backups, and HopsFS, write to this bucket and rely on object versioning, so backups do not work correctly without it:

```bash
aws s3api put-bucket-versioning --bucket BUCKET_NAME --versioning-configuration Status=Enabled --profile PROFILE
```

### Step 1.2: Create an ECR repository

Hopsworks allows users to customize the images used by Python jobs, Jupyter notebooks and (Py)Spark applications running in their projects.
These images are stored in ECR, so Hopsworks needs access to an ECR repository to push the project images.

Create the repository to host the project images:

```bash
aws --profile PROFILE ecr create-repository --repository-name NAMESPACE/hopsworks-base --region REGION
```

### Step 1.3: Create IAM policies

Create a policy that grants access to the S3 bucket and the ECR repository.
Save the following document as `policy.json`, replacing BUCKET_NAME, REGION, and ECR_AWS_ACCOUNT_ID with your values:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "hopsworksaiInstanceProfile",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:ListBucket",
        "s3:GetObject",
        "s3:DeleteObject",
        "s3:AbortMultipartUpload",
        "s3:ListBucketMultipartUploads",
        "s3:PutLifecycleConfiguration",
        "s3:GetLifecycleConfiguration",
        "s3:PutBucketVersioning",
        "s3:GetBucketVersioning",
        "s3:ListBucketVersions",
        "s3:DeleteObjectVersion"
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

Create the policy:

```bash
aws --profile PROFILE iam create-policy --policy-name POLICY_NAME --policy-document file://policy.json
```

This single policy grants both S3 (bucket) and ECR (repository) access.
Because the Helm values do not store any S3 access keys, Hopsworks and HopsFS reach the bucket through the AWS default credential provider chain, which on EKS resolves to the worker node instance IAM role.
Attaching this policy to the node group (Step 1.4) is therefore how Hopsworks is granted access to S3 and ECR — no access key or secret is stored in Kubernetes.

### Step 1.4: Create the EKS cluster using eksctl

When creating the cluster with eksctl, the following are required in the cluster configuration file (`eksctl.yaml`):

- `amiFamily` should be either `AmazonLinux2023` or `Ubuntu2404`.
  Amazon Linux 2 reaches end of support on June 30, 2026, so do not use it.
- The instance type should be Intel or AMD based (that is, not ARM/Graviton).
- The following managed policies are required (see [attaching policies by ARN](https://eksctl.io/usage/iam-policies/#attaching-policies-by-arn)):

```bash
- arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy
- arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy
- arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly
```

To let Hopsworks provision the necessary load balancers through the [AWS Load Balancer Controller](https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/), grant the controller permissions by enabling the add-on policy on the node group:

```bash
      withAddonPolicies:
        awsLoadBalancerController: true
```

Update CLUSTER_NAME, REGION, ECR_AWS_ACCOUNT_ID, and the policy name (POLICY_NAME) created above, then create the configuration file:

```yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: CLUSTER_NAME
  region: REGION
  version: "1.33"

iam:
  withOIDC: true

managedNodeGroups:
  - name: ng-1
    amiFamily: AmazonLinux2023
    instanceType: m6i.2xlarge
    minSize: 1
    maxSize: 5
    desiredCapacity: 5
    volumeSize: 100
    # ssh:                              # optional: enable SSH access to the nodes
    #   allow: true
    #   publicKeyPath: ~/.ssh/id_ed25519.pub
    iam:
      attachPolicyARNs:
        - arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy
        - arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy
        - arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly
        - arn:aws:iam::ECR_AWS_ACCOUNT_ID:policy/POLICY_NAME
      withAddonPolicies:
        awsLoadBalancerController: true
addons:
  - name: aws-ebs-csi-driver
    wellKnownPolicies:      # add IAM role and service account
      ebsCSIController: true
```

Create the EKS cluster:

```bash
eksctl create cluster -f eksctl.yaml --profile PROFILE
```

Once the cluster is created, verify that you can access it with the kubectl CLI tool:

```bash
kubectl get nodes
```

You should see the list of nodes provisioned for the cluster.

### Step 1.5: Install the AWS Load Balancer Controller

For Hopsworks to provision the network and application load balancers it needs, install the AWS Load Balancer Controller (see the [AWS documentation](https://docs.aws.amazon.com/eks/latest/userguide/lbc-helm.html)):

```bash
helm repo add eks https://aws.github.io/eks-charts
helm repo update eks
helm install aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system --set clusterName=CLUSTER_NAME
```

The controller uses the IAM permissions attached to the node group through the `awsLoadBalancerController` add-on policy enabled above.
Alternatively, you can run it with a dedicated service account using [IAM Roles for Service Accounts (IRSA)](https://docs.aws.amazon.com/eks/latest/userguide/lbc-helm.html).
If the controller cannot auto-detect the VPC, pass `--set region=REGION` and `--set vpcId=VPC_ID`.

### Step 1.6: Create a GP3 storage class

EKS clusters typically provide `gp2` as the default storage class.
`gp3` is more cost effective and is the storage class referenced by the Helm values below (`storageClassName: ebs-gp3`), so create it:

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
allowVolumeExpansion: true
EOF
```

If you prefer to keep the default `gp2` storage class, set `storageClassName` to `gp2` in the Helm values and skip this step.

### Step 1.7: Request an ACM certificate for your domain

HTTPS is required to access the Hopsworks UI.
The application load balancer that the AWS Load Balancer Controller provisions terminates TLS using a certificate from AWS Certificate Manager (ACM), and its ARN must already exist when you set the `alb.ingress.kubernetes.io/certificate-arn` annotation in the Helm values (Step 2.3).
The chart does not create this certificate, so request (or import) one in the same region as the cluster, covering the domain you will use as `HOST_DOMAIN`:

```bash
aws acm request-certificate --domain-name HOST_DOMAIN --validation-method DNS --region REGION --profile PROFILE
```

Complete the DNS validation in ACM, then note the certificate ARN.
The end-to-end order is: create and validate the certificate first, set its ARN in the values file (Step 2.3), install the chart (Step 2.4) which provisions the load balancer, then point the `HOST_DOMAIN` DNS record at that load balancer (Step 3.1).

## Step 2: Deploy Hopsworks

This section describes how to deploy the Hopsworks stack using Helm.

### Step 2.1: Add the Hopsworks Helm repository

To obtain access to the Hopsworks Helm chart repository, please [obtain](https://www.hopsworks.ai/try) an evaluation/startup licence.

Once you have the Helm chart repository URL, replace the environment variable $HOPSWORKS_REPO in the following command with this URL:

```bash
helm repo add hopsworks $HOPSWORKS_REPO
helm repo update hopsworks
```

### Step 2.2: Create the Hopsworks namespace

```bash
kubectl create namespace hopsworks
```

### Step 2.3: Create the Helm values file

Create a `values.aws.yaml` file with the following content.
This example covers the values needed for a basic deployment; see the [Helm chart values reference][helm-chart-values-reference] for the full list of configurable values.
Update the placeholders (ECR_AWS_ACCOUNT_ID, REGION, NAMESPACE, BUCKET_NAME, the certificate ARN from Step 1.7, and HOST_DOMAIN) with your values:

```yaml
global:
  _hopsworks:
    storageClassName: &storageClass ebs-gp3
    cloudProvider: "AWS"

    managedDockerRegistery:
      enabled: true
      domain: "ECR_AWS_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com"
      namespace: "NAMESPACE"
      credHelper:
        enabled: true
        secretName: &awsregcred "awsregcred"

    managedObjectStorage:
      enabled: true
      s3:
        bucket:
          name: "BUCKET_NAME"
        region: "REGION"

    minio:
      enabled: false

    externalLoadBalancers:
      enabled: true
      class: null
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-scheme: internet-facing

hopsworks:
  # RonDB and OpenSearch back up automatically to the S3 bucket above; Kubernetes
  # resource backups instead use Velero, which needs a separate install. Disable
  # the Velero backup so the chart's Velero prerequisite check does not fail the
  # install. See the Disaster Recovery guide to install Velero and enable it.
  velero:
    backup:
      enabled: false
  variables:
    # awsregcred Secret contains the docker configuration to use Cloud
    # specific docker login helper method instead of username/password
    # Currently only AWS and GCP support this method
    # Azure has deprecated it
    docker_operations_managed_docker_secrets: *awsregcred
    # We *need* to put awsregcred here because this is the list of
    # Secrets that are copied from hopsworks namespace to Projects namespace
    # during project creation.
    docker_operations_image_pull_secrets: "awsregcred"
  dockerRegistry:
    preset:
      usePullPush: false
      secrets:
        - *awsregcred
  ingress:
    enabled: true
    ingressClassName: alb
    annotations:
      alb.ingress.kubernetes.io/scheme: internet-facing
      alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:REGION:ACCOUNT_ID:certificate/CERTIFICATE_ID
      alb.ingress.kubernetes.io/target-type: ip
      alb.ingress.kubernetes.io/target-group-attributes: stickiness.enabled=true,stickiness.lb_cookie.duration_seconds=300

    host: &host HOST_DOMAIN
    hosts:
      - *host
    tls:
      - hosts:
        - *host

kafka:
  cluster:
    kafka:
      externalLoadBalancer:
        # The AWS Load Balancer Controller uses this finalizer to deprovision
        # the Kafka network load balancers on teardown. Strimzi manages the
        # broker and bootstrap Services, so the finalizer must be set here to
        # avoid orphaned load balancers when the release is uninstalled.
        finalizers:
        - service.k8s.aws/resources

rondb:
  rondb:
    resources:
      requests:
        storage:
          classes:
            default: *storageClass

consul:
  consul:
    server:
      storageClass: *storageClass

prometheus:
  prometheus:
    server:
      persistentVolume:
        storageClass: *storageClass
```

RonDB and OpenSearch back up automatically to the S3 bucket, which is why versioning must be enabled on it (Step 1.1).
Kubernetes-resource backups instead use Velero, which requires a separate installation, so they are disabled above (`hopsworks.velero.backup.enabled: false`) to keep the chart's Velero prerequisite check from failing the install.
To enable them, follow the [Disaster Recovery guide][disaster-recovery] to install Velero with the AWS plugin.

The `awsregcred` Docker registry secret referenced above is generated by the chart, because `cloudProvider` is `AWS` and `credHelper.enabled` is `true`.
You do not create it manually (unlike on Azure, where the credential helper is not available).

If you use model serving (KServe), update the allowed CORS origin to your domain, otherwise the browser is blocked from calling the model serving endpoints from the Hopsworks UI.
The allowlist defaults to a placeholder host, so add your domain to `values.aws.yaml`:

```yaml
kserve:
  istio:
    envoyFilter:
      corsAllowedOrigins:
        - https://HOST_DOMAIN
```

### Step 2.4: Install the Helm chart

```bash
helm install hopsworks hopsworks/hopsworks --namespace hopsworks --values values.aws.yaml --timeout=3600s
```

A first install pulls and syncs large base images and provisions stateful services, so allow up to an hour to complete; the chart's own deployment examples use `--timeout=3600s`.
A Helm timeout does not roll back the release — the deployment keeps reconciling in the background — so if it times out, track progress with kubectl rather than reinstalling:

```bash
kubectl -n hopsworks get pods
```

The command above shows which pods are running and which are still being provisioned.

## Step 3: Access Hopsworks

Once all pods in the `hopsworks` namespace are running, the Hopsworks UI is reachable over HTTPS at the `HOST_DOMAIN` you configured in the Ingress.
Before that hostname resolves, you have to point it at the application load balancer that the AWS Load Balancer Controller provisioned.

### Step 3.1: Find the load balancer hostname and create a DNS record

Get the address of the application load balancer created for the Ingress:

```bash
kubectl get ingress -n hopsworks
```

The `ADDRESS` column shows the load balancer DNS name, for example `k8s-hopsworks-xxxxxxxxxx.REGION.elb.amazonaws.com`.
If `ADDRESS` is empty, wait a minute and retry, because the controller provisions the load balancer asynchronously.

In your DNS provider, create a record mapping `HOST_DOMAIN` to this load balancer DNS name (a CNAME on most providers, or an alias/A record to the load balancer in Route 53).
The `HOST_DOMAIN` must be covered by the ACM certificate from Step 1.7, otherwise the browser rejects the TLS connection.

### Step 3.2: Log in

Open `https://HOST_DOMAIN` in your browser and log in with the default administrator account:

- Username: `admin@hopsworks.ai`
- Password: `admin`

Change this password immediately after the first login, because these defaults are public and identical across every installation.
To start with a different password, set `hopsworks.variables.admin_password` (and `hopsworks.variables.admin_email`) in the values file before installing.

## Resources created

Using the Helm chart and the values file, the following resources are created.

### Load balancers

```yaml
    externalLoadBalancers:
      enabled: true
      class: null
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-scheme: internet-facing
```

Enabling the external load balancers in the values file provisions a load balancer for each of the following services:

- arrowflight: sends queries from external clients to the Hopsworks Query Service.
- kafka: sends data to the Apache Kafka brokers for ingestion into the online feature store.
- rdrs: queries online feature store data using the REST APIs.
- mysql: queries online feature store data using the MySQL APIs.
- opensearch: queries the Hopsworks vector database.
- namenode and datanode: external access to the HopsFS file system.

On EKS, the AWS Load Balancer Controller installed above is responsible for provisioning these load balancers.
You can configure them using the annotations documented in the [AWS Load Balancer Controller guide](https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/guide/ingress/annotations/).

Each service has its own `externalLoadBalancer.enabled` (or, for HopsFS, `loadBalancer.enabled`) value, nested inside the relevant subchart.
When that value is left unset it inherits `global._hopsworks.externalLoadBalancers.enabled`, which defaults to `true`, so all of these load balancers are provisioned unless you disable them.
The exact value paths are:

- `arrowflight.externalLoadBalancer.enabled`
- `kafka.cluster.kafka.externalLoadBalancer.enabled`
- `rondb.rondb.meta.rdrs.externalLoadBalancer.enabled` (rdrs)
- `rondb.rondb.meta.mysqld.externalLoadBalancer.enabled` (mysql)
- `olk.opensearch.externalLoadBalancer.enabled` (opensearch)
- `hopsfs.namenode.loadBalancer.enabled` (namenode)
- `hopsfs.datanode.loadBalancer.enabled` (datanode)
- `trino.externalLoadBalancer.enabled` (only when Trino is enabled)

Other load balancer providers are also supported by providing the appropriate controller, class, and annotations.

### Ingress

```yaml
  ingress:
    enabled: true
    ingressClassName: alb
    annotations:
      alb.ingress.kubernetes.io/scheme: internet-facing
```

The Hopsworks UI and REST interface are available outside the Kubernetes cluster through an Ingress.
On AWS this is implemented by provisioning an application load balancer using the AWS Load Balancer Controller, which reads the [Ingress annotations](https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/guide/ingress/annotations/).

HTTPS is required to access the Hopsworks UI, so the Ingress must reference an ACM certificate (Step 1.7) through this annotation:

```bash
alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:REGION:ACCOUNT_ID:certificate/CERTIFICATE_ID
```

This configures the TLS certificate that the application load balancer uses to terminate the connection.
The certificate must be available in the [AWS Certificate Manager](https://aws.amazon.com/certificate-manager/) and cover your `HOST_DOMAIN`.

The chart does not create a DNS record for you.
After the Ingress is provisioned, find the load balancer hostname with `kubectl get ingress -n hopsworks` and point your `HOST_DOMAIN` at it, as described in Step 3.1.

### Cluster roles and cluster role bindings

By default a set of cluster roles is provisioned.
If you don't have permissions to provision cluster roles or cluster role bindings, reach out to your Kubernetes administrator and provide the appropriate resource names as values in the values file.

## Next steps

Check out our other guides for how to get started with Hopsworks and the Feature Store:

- Get started with the [Hopsworks Feature Store](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/quickstart.ipynb){:target="_blank"}
- Follow one of our [tutorials](../../tutorials/index.md)
- Follow one of our [guides](../../user_guides/index.md)
