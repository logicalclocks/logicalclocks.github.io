# Getting started with managed.hopsworks.ai (AWS)

[Managed.hopsworks.ai](https://managed.hopsworks.ai) is our managed platform for running Hopsworks and the Feature Store
in the cloud. It integrates seamlessly with third-party platforms such as Databricks,
SageMaker and KubeFlow. This guide shows how to set up [managed.hopsworks.ai](https://managed.hopsworks.ai) with your organization's AWS account.

## Prerequisit
To run the commands in this guide, you must have the AWS CLI installed and configured and your user must have at least the set of permission listed below. See the [Getting started guide](https://docs.aws.amazon.com/cli/v1/userguide/cli-chap-install.html) in the AWS CLI User Guide for more information about installing and configuring the AWS CLI.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "iam:CreateInstanceProfile",
                "iam:PassRole",
                "iam:CreateRole",
                "iam:PutRolePolicy",
                "iam:AddRoleToInstanceProfile",
                "ec2:ImportKeyPair",
                "ec2:CreateKeyPair",
                "s3:CreateBucket"
            ],
            "Resource": "*"
        }
    ]
}
```

All the commands have unix-like quotation rules. These commands will need to be adapted to your terminal's quoting rules. See [Using quotation marks with strings](https://docs.aws.amazon.com/cli/v1/userguide/cli-usage-parameters-quoting-strings.html) in the AWS CLI User Guide.

All the commands use the default AWS profile. Add the *--profile* parameter to use another profile. 

## Step 1: Connecting your AWS account

[Managed.hopsworks.ai](https://managed.hopsworks.ai) deploys Hopsworks clusters to your AWS account. To enable this you have to permit us to do so. This is done using an AWS cross-account role.

<p align="center">
  <iframe
    title="Azure information video"
    style="width:700px; height: 370px;"
    src="https://www.youtube.com/embed/DLMBdA8d9nU"
    frameBorder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowFullScreen
  >
  </iframe>
</p>

In [managed.hopsworks.ai](https://managed.hopsworks.ai/) click on *Connect to AWS* or go to *Settings* and click on *Configure* next to *AWS*. Then click on *Cross-accont role*. This will direct you to a page with the instructions needed to create the Cross account role and set up the connection. Follow the instructions.

!!! note 
    it is possible to limit the permissions that are set up during this phase. For more details see [restrictive-permissions](restrictive_permissions.md).


<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/aws/create-role-instructions.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/aws/create-role-instructions.png" alt="Screenshot of the instruction to create the cross account role">
    </a>
    <figcaption>Instructions to create the cross account role</figcaption>
  </figure>
</p>

## Step 2: Creating storage

!!! note 
    If you prefer using terraform, you can skip this step and the remaining steps, and instead, follow [this guide](../common/terraform.md#getting-started-with-aws).

The Hopsworks clusters deployed by [managed.hopsworks.ai](https://managed.hopsworks.ai) store their data in an S3 bucket in your AWS account.


To create the bucket run the following command, replacing *BUCKET_NAME* with the name you want for your bucket and setting the region to the aws region in which you want to run your cluster.

!!! warning
    The bucket must be in the same region as the hopsworks cluster you are going to run

```bash
aws s3 mb s3://BUCKET_NAME --region us-east-2
```


## Step 3: Creating Instance profile

Hopsworks cluster nodes need access to certain resources such as the S3 bucket you created above, an ecr repository, and CloudWatch.


First, create an instance profile by running:
```bash
aws iam create-instance-profile --instance-profile-name hopsworksai-instances
```

We will now create a role with the needed permissions for this instance profile. 
Start by creating a file named *assume-role-policy.json* containing the following:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

Run the following to create the role:

```bash
aws iam create-role --role-name hopsworksai-instances \
   --description "Role for the hopsworks cluster instances" \
   --assume-role-policy-document file://assume-role-policy.json
```

Create a file called *instances-policy.json* containing the following permissions.
{!setup_installation/aws/instance_profile_permissions.md!}

Attach the permission to the role by running:
```bash
aws iam put-role-policy --role-name hopsworksai-instances \
   --policy-name hopsworksai-instances \
   --policy-document file://instances-policy.json
```

Finally, attach the role to the instance profile by running:
```bash
aws iam add-role-to-instance-profile \
   --role-name hopsworks-instances \
   --instance-profile-name hopsworksai-instances
```

## Step 4: Create an SSH key
When deploying clusters, [managed.hopsworks.ai](https://managed.hopsworks.ai) installs an ssh key on the cluster's instances so that you can access them if necessary. For this purpose, you need to add an ssh key to your AWS EC2 environment. This can be done in two ways: [creating a new key pair](#step-31-create-a-new-key-pair) or [importing an existing key pair](#step-32-import-a-key-pair).

### Step 4.1: Create a new key pair
To create a new key pair run the following command replacing REGION by the region in which you want to run the hopsworks cluster.
```bash
aws ec2 create-key-pair --key-name hopsworksai \
    --region REGION
```
The output is an ASCII version of the private key and key fingerprint. You need to save the key to a file.

### Step 4.2: Import a key pair
To import an existing key pair run the following command replacing *PATH_TO_PUBLIC_KEY* by the path to the public key on your machine and REGION by the region in which you want to run the hopsworks cluster.
```bash
aws ec2 import-key-pair --key-name hopsworskai \
   --public-key-material fileb://PATH_TO_PUBLIC_KEY \
   --region REGION
```

## Step 5: Deploying a Hopsworks cluster

In [managed.hopsworks.ai](https://managed.hopsworks.ai), select *Create cluster*:

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/create-instance.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/common/create-instance.png" alt="Create a Hopsworks cluster">
    </a>
    <figcaption>Create a Hopsworks cluster</figcaption>
  </figure>
</p>

Select the *Region* in which you want your cluster to run (1), name your cluster (2).

Select the *Instance type* (3) and *Local storage* (4) size for the cluster *Head node*.

Check if you want to *Enable EBS encryption* (5)

Enter the name of the *S3 bucket* (6) you created in [step 2](#step-2-creating-storage).

!!! note
    The S3 bucket you are using must be empty.

Make sure that the *ECR AWS Account Id* (7) is correct. It is set by default to the AWS account id where you set the cross-account role and need to match the permissions you set in [step 3](#step-3-creating-instance-profile). 
Press *Next*:

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/aws/create-instance-general.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/aws/create-instance-general.png" alt="Create a Hopsworks cluster, general Information">
    </a>
    <figcaption>Create a Hopsworks cluster, general information</figcaption>
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

Select the *SSH key* you created in [step 4](#step-4-create-an-ssh-key):

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/aws/connect-aws-ssh.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/aws/connect-aws-ssh.png" alt="Choose SSH key">
    </a>
    <figcaption>Choose SSH key</figcaption>
  </figure>
</p>

Select the *Instance Profile* that you created in [step 3](#step-3-creating-instance-profile):

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/aws/connect-aws-profile.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/aws/connect-aws-profile.png" alt="Choose the instance profile">
    </a>
    <figcaption>Choose the instance profile</figcaption>
  </figure>
</p>

To backup the S3 bucket data when taking a cluster backup we need to set a retention policy for S3. You can deactivate the retention policy by setting this value to 0 but this will block you from taking any backup of your cluster. Choose the retention period in days and click on *Review and submit*:

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/azure/connect-azure-backup.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/azure/connect-azure-backup.png" alt="Choose the backup retention policy">
    </a>
    <figcaption>Choose the backup retention policy</figcaption>
  </figure>
</p>

Review all information and select *Create*:

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/aws/connect-aws-review.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/aws/connect-aws-review.png" alt="Review cluster information">
    </a>
    <figcaption>Review cluster information</figcaption>
  </figure>
</p>

The cluster will start. This will take a few minutes:

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/booting.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/common/booting.png" alt="Booting Hopsworks cluster">
    </a>
    <figcaption>Booting Hopsworks cluster</figcaption>
  </figure>
</p>

As soon as the cluster has started, you will be able to log in to your new Hopsworks cluster. You will also be able to stop, restart, or terminate the cluster.


<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/running.png">
      <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/common/running.png" alt="Running Hopsworks cluster">
    </a>
    <figcaption>Running Hopsworks cluster</figcaption>
  </figure>
</p>

## Step 6: Next steps

Check out our other guides for how to get started with Hopsworks and the Feature Store:

* Make Hopsworks services [accessible from outside services](../common/services.md)
* Get started with the [Hopsworks Feature Store](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/quickstart.ipynb){:target="_blank"}
* Follow one of our [tutorials](../../tutorials/index.md)
* Follow one of our [Guide](../../user_guides/index.md)
* Code examples and notebooks: [hops-examples](https://github.com/logicalclocks/hops-examples)
