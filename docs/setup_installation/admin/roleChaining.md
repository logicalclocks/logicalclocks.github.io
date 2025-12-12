# AWS IAM Role Chaining

## Introduction

When running Hopsworks in Amazon EKS you have several options to give the Hopsworks user access to AWS resources.
The simplest is to assign [Amazon EKS node IAM role](https://docs.aws.amazon.com/eks/latest/userguide/create-node-role.html) access to the resources.
But, this will make these resources accessible by all users.
To manage access to resources on a project base you need to use [Role chaining](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html#iam-term-role-chaining).

In this document we will see how to configure AWS and Hopsworks to use Role chaining in your Hopsworks projects.

## Prerequisites

Before you begin this guide you'll need the following:

- A Hopsworks cluster running on EKS.
- Enabled IAM [OpenID Connect (OIDC) provider](https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html) for your cluster.
- Administrator account on the Hopsworks cluster.

### Step 1: Create an IAM role and associate it with a Kubernetes service account

To use role chaining the hopsworks instance pods need to be able to impersonate the roles you want to be linked to your project.
For this you need to create an IAM role and associate it with your Kubernetes service accounts with assume role permissions and attach it to your hopsworks instance pods.
For more details on how to create an IAM roles for Kubernetes service accounts see the [aws documentation](https://docs.aws.amazon.com/eks/latest/userguide/associate-service-account-role.html).

!!!note
    To ensure that users can't use the service account role and impersonate the roles by their own means, you need to ensure that the service account is only attached to the hopsworks instance pods.

```sh
account_id=$(aws sts get-caller-identity --query "Account" --output text)
oidc_provider=$(aws eks describe-cluster --name my-cluster --region $AWS_REGION --query "cluster.identity.oidc.issuer" --output text | sed -e "s/^https:\/\///")

```

```sh
export namespace=hopsworks
export service_account=my-service-account

```

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::$account_id:oidc-provider/$oidc_provider"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "$oidc_provider:aud": "sts.amazonaws.com",
          "$oidc_provider:sub": "system:serviceaccount:$namespace:$service_account"
        }
      }
    }
  ]
}
```

<figcaption>Example trust policy for a service account.</figcaption>

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AssumeDataRoles",
            "Effect": "Allow",
            "Action": "sts:AssumeRole",
            "Resource": [
                "arn:aws:iam::123456789011:role/my-role",
                "arn:aws:iam::xxxxxxxxxxxx:role/s3-role",
                "arn:aws:iam::xxxxxxxxxxxx:role/dev-s3-role",
                "arn:aws:iam::xxxxxxxxxxxx:role/redshift"
            ]
        }
    ]
}
```

<figcaption>Example policy for assuming four roles.</figcaption>

The IAM role will need to add a trust policy to allow the service account to assume the role, and permissions to assume the different roles that will be used to access resources.

To associate the IAM role with your Kubernetes service account you will need to annotate your service account with the Amazon Resource Name (ARN) of the IAM role that you want the service account to assume.

```sh
kubectl annotate serviceaccount -n $namespace $service_account eks.amazonaws.com/role-arn=arn:aws:iam::$account_id:role/my-role
```

### Step 2: Create the resource roles

For the service account role to be able to impersonate the roles you also need to configure the roles themselves to allow it.
This is done by adding the service account role to the role's [Trust relationships](https://docs.aws.amazon.com/directoryservice/latest/admin-guide/edit_trust.html).

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
        "Effect": "Allow",
        "Principal": {
            "AWS": "arn:aws:iam::xxxxxxxxxxxx:role/service-account-role"
        },
        "Action": "sts:AssumeRole"
        }
    ]
}
```

<figcaption>Example resource roles.</figcaption>

### Step 3: Create mappings

Now that the service account IAM role can assume the roles we need to configure Hopsworks to delegate access to the roles on a project base.

In Hopsworks, click on your name in the top right corner of the navigation bar and choose _Cluster Settings_ from the dropdown menu.
In the Cluster Settings' _IAM Role Chaining_ tab you can configure the mappings between projects and IAM roles.

<figure>
  <img src="../../../assets/images/admin/iam-role/cluster-settings.png" alt="Role Chaining"/>
  <figcaption>Role Chaining</figcaption>
</figure>

Add mappings by clicking on _New role chaining_.
Enter the project name.
Select the type of user that can assume the role.
Enter the role ARN.
And click on _Create new role chaining_

<figure>
  <img src="../../../assets/images/admin/iam-role/new-role-chaining.png" alt="Create Role Chaining"/>
  <figcaption>Create Role Chaining</figcaption>
</figure>

Project member can now create connectors using _temporary credentials_ to assume the role you configured.
More details about using temporary credentials can be found in the [Temporary Credentials section](../../user_guides/fs/data_source/creation/s3.md#temporary-credentials) of the S3 datasource creation guide.

Project member can see the list of role they can assume by going the _Project Settings_ -> [Assuming IAM Roles](../../user_guides/projects/iam_role/iam_role_chaining.md) page.
