# Upgrade existing clusters on managed.hopsworks.ai from version 3.0 or newer (AWS) 

This guide shows you how to upgrade your existing Hopsworks cluster to a newer version of Hopsworks.

## Step 1: Make sure your cluster is running

It is important that your cluster is **Running**. Otherwise you will not be able to upgrade. As soon as a new version is available an upgrade notification will appear.

You can proceed by clicking the *Upgrade* button.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/aws/aws-notification-running-3.0.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/aws/aws-notification-running-3.0.png" alt="New version notification">
    </a>
    <figcaption>A new Hopsworks version is available</figcaption>
  </figure>
</p>

## Step 2: Add backup permissions to your cross account role

!!! note
    You can skip this step if you already have the following permissions in your cross account role:
    ```json 
    [ "ec2:RegisterImage", "ec2:DeregisterImage", "ec2:DescribeImages", "ec2:CreateSnapshot", "ec2:DeleteSnapshot", "ec2:DescribeSnapshots"]
    ```

We require some extra permissions to be added to the role you have created when connecting your AWS account as described in [getting started guide](../getting_started/#step-1-connecting-your-aws-account). These permissions are required to create a snapshot of your cluster before proceeding with the upgrade. 


First, check which role or access key you have added to managed.hopsworks.ai, you can go to the *Settings* tab, and then click *Edit* next to the AWS cloud account

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/aws/aws-account-settings.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/aws/aws-account-settings.png" alt="AWS account settings">
    </a>
    <figcaption>Cloud Accounts</figcaption>
  </figure>
</p>

Once you have clicked on *Edit*, you will be able to see the current assigned role

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/aws/aws-cross-account-role.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/aws/aws-cross-account-role.png" alt="AWS cross-account role">
    </a>
    <figcaption>AWS Cross-Account Role</figcaption>
  </figure>
</p>

Once you get your role name, navigate to [AWS management console](https://console.aws.amazon.com/iam/home#), then click on *Roles* and then search for your role name and click on it.  Go to the *Permissions* tab, click on *Add inline policy*, and then go to the *JSON* tab. Paste the following snippet, click on *Review policy*, name it, and click *Create policy*.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "HopsworksAIBackup",
            "Effect": "Allow",
            "Action": [
                "ec2:RegisterImage",
                "ec2:DeregisterImage",
                "ec2:DescribeImages",
                "ec2:CreateSnapshot",
                "ec2:DeleteSnapshot",
                "ec2:DescribeSnapshots"
            ],
            "Resource": "*"
        }
    ]
}
```

## Step 3: Update the instance profile permissions 

We have enforced using managed docker registry (ECR) starting from Hopsworks version 3.1.0, so you need to update your instance profile to include extra permissions to allow access to ECR. First, get the instance profile of your cluster by clicking on the *Details* tab and check the IAM role ARN shown in front of *IAM Instance Profile*. Once you get your role name, navigate to [AWS management console](https://console.aws.amazon.com/iam/home#), then click on *Roles* and then search for your role name and click on it.  Go to the *Permissions* tab, click on *Add inline policy*, and then go to the *JSON* tab. Paste the following snippet, click on *Review policy*, name it, and click *Create policy*.


```json
{
   "Version":"2012-10-17",
   "Statement":[
      {
         "Sid":"AllowPullImagesFromHopsworkAi",
         "Effect":"Allow",
         "Action":[
            "ecr:GetDownloadUrlForLayer",
            "ecr:BatchGetImage"
         ],
         "Resource":[
            "arn:aws:ecr:*:822623301872:repository/filebeat",
            "arn:aws:ecr:*:822623301872:repository/base",
            "arn:aws:ecr:*:822623301872:repository/onlinefs",
            "arn:aws:ecr:*:822623301872:repository/airflow",
            "arn:aws:ecr:*:822623301872:repository/git"
         ]
      },
      {
         "Sid":"AllowCreateRespositry",
         "Effect":"Allow",
         "Action":"ecr:CreateRepository",
         "Resource":"*"
      },
      {
         "Sid":"AllowPushandPullImagesToUserRepo",
         "Effect":"Allow",
         "Action":[
            "ecr:GetDownloadUrlForLayer",
            "ecr:BatchGetImage",
            "ecr:CompleteLayerUpload",
            "ecr:UploadLayerPart",
            "ecr:InitiateLayerUpload",
            "ecr:DeleteRepository",
            "ecr:BatchCheckLayerAvailability",
            "ecr:PutImage",
            "ecr:ListImages",
            "ecr:BatchDeleteImage",
            "ecr:GetLifecyclePolicy",
            "ecr:PutLifecyclePolicy",
            "ecr:TagResource"
         ],
         "Resource":[
            "arn:aws:ecr:*:*:repository/*/filebeat",
            "arn:aws:ecr:*:*:repository/*/base",
            "arn:aws:ecr:*:*:repository/*/onlinefs",
            "arn:aws:ecr:*:*:repository/*/airflow",
            "arn:aws:ecr:*:*:repository/*/git"
         ]
      },
      {
         "Sid":"AllowGetAuthToken",
         "Effect":"Allow",
         "Action":"ecr:GetAuthorizationToken",
         "Resource":"*"
      }
   ]
}
```

## Step 4: Run the upgrade process

You need to click on *Upgrade* to start the upgrade process. You will be prompted with the screen shown below to confirm your intention to upgrade: 

!!! note
    No need to worry about the steps shown below if you have already completed [Step 2](#step-2-add-backup-permissions-to-your-cross-account-role) and [Step 3](#step-3-update-the-instance-profile-permissions)

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/aws/aws-upgrade-prompt-1_3.0.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/aws/aws-upgrade-prompt-1_3.0.png" alt="AWS Upgrade Prompt">
    </a>
    <figcaption>Upgrade confirmation</figcaption>
  </figure>
</p>

Check the *Yes, upgrade cluster* checkbox to proceed, then the *Upgrade* button will be activated as shown below:

!!! warning
    Currently, we only support upgrade for the head node and you will need to recreate your workers once the upgrade is successfully completed. 

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/aws/aws-upgrade-prompt-2_3.0.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/aws/aws-upgrade-prompt-2_3.0.png" alt="AWS Upgrade Prompt">
    </a>
    <figcaption>Upgrade confirmation</figcaption>
  </figure>
</p>

Depending on how big your current cluster is, the upgrade process may take from 1 hour to a few hours until completion.

!!! note
    We don't delete your old cluster until the upgrade process is successfully completed. 


<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/aws/aws-upgrade-start_3.0.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/aws/aws-upgrade-start_3.0.png" alt="AWS Upgrade starting">
    </a>
    <figcaption>Upgrade is running</figcaption>
  </figure>
</p>

Once the upgrade is completed, you can confirm that you have the new Hopsworks version by checking the version on the *Details* tab of your cluster.

For more details about error handling check [this guide](../upgrade_2.4/#error-handling)