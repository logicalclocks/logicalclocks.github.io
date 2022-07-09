# Upgrade existing clusters on Hopsworks.ai from version 2.4 or newer (AWS) 

This guide shows you how to upgrade your existing Hopsworks cluster to a newer version of Hopsworks.

## Step 1: Make sure your cluster is running

It is important that your cluster is **Running**. Otherwise you will not be able to upgrade. As soon as a new version is available an upgrade notification will appear.

You can proceed by clicking the *Upgrade* button.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/aws/aws-notification-running-2.4.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/aws/aws-notification-running-2.4.png" alt="New version notification">
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


First, check which role or access key you have added to Hopsworks.ai, you can go to the *Settings* tab, and then click *Edit* next to the AWS cloud account

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

## Step 3: Run the upgrade process

You need to click on *Upgrade* to start the upgrade process. You will be prompted with the screen shown below to confirm your intention to upgrade: 

!!! note
    No need to worry about the following message since this is done already in [Step 2](#step-2-add-backup-permissions-to-your-cross-account-role)

    **Make sure that your cross-account role which you have connected to Hopsworks.ai has the following permissions:
    [ "ec2:RegisterImage", "ec2:DeregisterImage", "ec2:DescribeImages", "ec2:CreateSnapshot", "ec2:DeleteSnapshot", "ec2:DescribeSnapshots"]**

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/aws/aws-upgrade-prompt-1_2.4.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/aws/aws-upgrade-prompt-1_2.4.png" alt="AWS Upgrade Prompt">
    </a>
    <figcaption>Upgrade confirmation</figcaption>
  </figure>
</p>

Check the *Yes, upgrade cluster* checkbox to proceed, then the *Upgrade* button will be activated as shown below:

!!! warning
    Currently, we only support upgrade for the head node and you will need to recreate your workers once the upgrade is successfully completed. 

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/aws/aws-upgrade-prompt-2_2.4.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/aws/aws-upgrade-prompt-2_2.4.png" alt="AWS Upgrade Prompt">
    </a>
    <figcaption>Upgrade confirmation</figcaption>
  </figure>
</p>

Depending on how big your current cluster is, the upgrade process may take from 1 hour to a few hours until completion.

!!! note
    We don't delete your old cluster until the upgrade process is successfully completed. 


<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/aws/aws-upgrade-start_2.4.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/aws/aws-upgrade-start_2.4.png" alt="AWS Upgrade starting">
    </a>
    <figcaption>Upgrade is running</figcaption>
  </figure>
</p>

Once the upgrade is completed, you can confirm that you have the new Hopsworks version by checking the version on the *Details* tab of your cluster.

## Error handling 
There are two categories of errors that you may encounter during an upgrade. First, a permission error due to missing permission or a misconfigured policy in your cross-account role, see [Error 1](#error-1-missing-backup-permissions). Second, an error during the upgrade process running on your cluster, see [Error 2](#error-2-upgrade-process-error).

### Error 1: Missing backup permissions

If one or more backup permissions are missing, or if the resource is not set correctly, you will be notified with an error message as shown below:

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/aws/aws-upgrade-backup-permission-error.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/aws/aws-upgrade-backup-permission-error.png" alt="AWS Upgrade Retry">
    </a>
    <figcaption>Upgrade permissions are missing</figcaption>
  </figure>
</p>

Update you cross account role as described in [Step 2](#step-2-add-backup-permissions-to-your-cross-account-role), then click *Start*. Once the cluster is up and running, you can try running the upgrade again.


### Error 2: Upgrade process error

If an error occurs during the upgrade process, you will have the option to rollback to your old cluster as shown below: 

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/aws/aws-upgrade-error_2.4.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/aws/aws-upgrade-error_2.4.png" alt="Error during upgrade">
    </a>
    <figcaption>Error occurred during upgrade</figcaption>
  </figure>
</p>

Click on *Rollback* to recover your old cluster before upgrade.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/aws/aws-rollback-prompt-1_2.4.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/aws/aws-rollback-prompt-1_2.4.png" alt="Rollback prompt">
    </a>
    <figcaption>Upgrade rollback confirmation</figcaption>
  </figure>
</p>

Check the *Yes, rollback cluster* checkbox to proceed, then the *Rollback* button will be activated as shown below:

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/aws/aws-rollback-prompt-2_2.4.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/aws/aws-rollback-prompt-2_2.4.png" alt="Rollback prompt">
    </a>
    <figcaption>Upgrade rollback confirmation</figcaption>
  </figure>
</p>

Once the rollback is completed, you will be able to continue working as normal with your old cluster.

!!! note
    The old cluster will be **stopped** after the rollback. You have to click on the *Start* button.

