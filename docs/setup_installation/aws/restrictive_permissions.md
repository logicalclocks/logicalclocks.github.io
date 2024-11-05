# Limiting AWS permissions

[Managed.hopsworks.ai](https://managed.hopsworks.ai) requires a set of permissions to be able to manage resources in the user’s AWS account.
By default, [these permissions](#default-permissions) are set to easily allow a wide range of different configurations and allow
us to automate as many steps as possible. While we ensure to never access resources we shouldn’t,
we do understand that this might not be enough for your organization or security policy.
This guide explains how to lock down AWS permissions following the IT security policy principle of least privilege allowing
[managed.hopsworks.ai](https://managed.hopsworks.ai) to only access resources in a specific VPC.

## Default permissions 
This is the list of default permissions that are required by [managed.hopsworks.ai](https://managed.hopsworks.ai). If you prefer to limit these permissions, then proceed to the [next section](#limiting-the-cross-account-role-permissions).

```json
{!setup_installation/aws/aws_permissions.json!}
```

## Limiting the cross-account role permissions

### Step 1: Create a VPC

To restrict [managed.hopsworks.ai](https://managed.hopsworks.ai) from accessing resources outside of a specific VPC, you need to create a new VPC
connected to an Internet Gateway. This can be achieved in the AWS Management Console following this guide:
[Create the VPC](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-vpcs.html#Create-VPC).
Follow the steps of `Create a VPC, subnets, and other VPC resources`, naming your vpc and changing the `Number of Availability Zones` to 1 are the only changes you need to make to the default configuration.
Alternatively, an existing VPC such as the default VPC can be used and [managed.hopsworks.ai](https://managed.hopsworks.ai) will be restricted to this VPC.
Note the VPC ID of the VPC you want to use for the following steps.

!!! note
    Make sure you enable `DNS hostnames` for your VPC

!!! note
    If you use VPC endpoints to managed access to services such as S3 and ECR you need to ensure that the endpoints provide the same permissions as set in the [instance profile](../getting_started/#step-3-creating-instance-profile)

After you have created the VPC either [Create a Security Group](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html#CreatingSecurityGroups) or use VPC's default. Make sure that the VPC allow the following traffic.

#### Inbound traffic 

It is _**imperative**_ that the [Security Group](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html#AddRemoveRules) allows Inbound traffic from any Instance within the same Security Group in any (TCP) port. All VMs of the Cluster should be able to communicate with each other. It is also recommended to open TCP port `80` to sign the certificates. If you do not open port `80` you will have to use a self-signed certificate in your Hopsworks cluster. This can be done by checking the `Continue with self-signed certificate` check box in the `Security Group` step of the cluster creation.


We recommend configuring the [Network ACLs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html#Rules) to be open to all inbound traffic and let the security group handle the access restriction. But if you want to set limitations at the Network ACLs level, they must be configured so that at least the TCP ephemeral port `32768 - 65535` are open to the internet (this is so that outbound trafic can receive answers). It is also recommended to open TCP port `80` to sign the certificates. If you do not open port `80` you will have to use a self-signed certificate in your Hopsworks cluster. This can be done by checking the `Continue with self-signed certificate` check box in the `Security Group` step of the cluster creation.

#### Outbound traffic 

Clusters created on [managed.hopsworks.ai](https://managed.hopsworks.ai) need to be able to send http requests to *api.hopsworks.ai*. The *api.hopsworks.ai* domain use a content delivery network for better performance. This result in the impossibility to predict which IP the request will be sent to. If you require a list of static IPs to allow outbound traffic from your security group, use the *static IPs* option during [cluster creation](../cluster_creation/#limiting-outbound-traffic-to-hopsworksai).

Similar to Inbound traffic, the Security Group in place _**must**_ allow Outbound traffic in any (TCP) port towards any VM withing the same Security Group.

!!! note
    If you intend to use the managed users option on your Hopsworks cluster you should also allow outbound traffic to [cognito-idp.us-east-2.amazonaws.com](https://cognito-idp.us-east-2.amazonaws.com) and [managedhopsworks-prod.auth.us-east-2.amazoncognito.com](https://managedhopsworks-prod.auth.us-east-2.amazoncognito.com).

### Step 2: Create an instance profile

You need to create an instance profile that will identify all instances started by [managed.hopsworks.ai](https://managed.hopsworks.ai).
Follow this guide to create a role to be used by EC2 with no permissions attached:
[Creating a Role for an AWS Service (Console)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html).
Take note of the ARN of the role you just created.

You will need to add permissions to the instance profile to give access to the S3 bucket where Hopsworks will store its data. For more details about these permissions check [our guide here](../getting_started/#step-3-creating-instance-profile).
Check [bellow](#limiting-the-instance-profile-permissions) for more information on restricting the permissions given the instance profile.

### Step 3: Set permissions of the cross-account role

During the account setup for [managed.hopsworks.ai](https://managed.hopsworks.ai), you were asked to create and provide a cross-account role.
If you don’t remember which role you used then you can find it in Settings/Account Settings in [managed.hopsworks.ai](https://managed.hopsworks.ai).
Edit this role in the AWS Management Console and overwrite the existing inline policy with the following policy.

Note that you have to replace `[INSTANCE_PROFILE_NAME]` and `[VPC_ID]` for multiple occurrences in the given policy.

If you want to learn more about how this policy works check out:
[How to Help Lock Down a User’s Amazon EC2 Capabilities to a Single VPC](https://aws.amazon.com/blogs/security/how-to-help-lock-down-a-users-amazon-ec2-capabilities-to-a-single-vpc/).

```json
{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "NonResourceBasedPermissions",
        "Effect": "Allow",
        "Action": [
          "ec2:DescribeInstances",
          "ec2:DescribeVpcs",
          "ec2:DescribeVolumes",
          "ec2:DescribeSubnets",
          "ec2:DescribeKeyPairs",
          "ec2:DescribeInstanceStatus",
          "iam:ListInstanceProfiles",
          "ec2:DescribeSecurityGroups",
          "ec2:DescribeVpcAttribute",
          "ec2:DescribeRouteTables"
        ],
        "Resource": "*"
      },
      {
        "Sid": "IAMPassRoleToInstance",
        "Effect": "Allow",
        "Action": "iam:PassRole",
        "Resource": "arn:aws:iam::*:role/[INSTANCE_PROFILE_NAME]"
      },
      {
        "Sid": "EC2RunInstancesOnlyWithGivenRole",
        "Effect": "Allow",
        "Action": "ec2:RunInstances",
        "Resource": "arn:aws:ec2:*:*:instance/*",
        "Condition": {
          "ArnLike": {
            "ec2:InstanceProfile": "arn:aws:iam::*:instance-profile/[INSTANCE_PROFILE_NAME]"
          }
        }
      },
      {
        "Sid": "EC2RunInstancesOnlyInGivenVpc",
        "Effect": "Allow",
        "Action": "ec2:RunInstances",
        "Resource": "arn:aws:ec2:*:*:subnet/*",
        "Condition": {
          "ArnLike": {
            "ec2:vpc": "arn:aws:ec2:*:*:vpc/[VPC_ID]"
          }
        }
      },
      {
        "Sid": "AllowInstanceActions",
        "Effect": "Allow",
        "Action": [
          "ec2:StopInstances",
          "ec2:TerminateInstances",
          "ec2:StartInstances",
          "ec2:CreateTags",
          "ec2:AssociateIamInstanceProfile"
        ],
        "Resource": "arn:aws:ec2:*:*:instance/*",
        "Condition": {
          "ArnLike": {
            "ec2:InstanceProfile": "arn:aws:iam::*:instance-profile/[INSTANCE_PROFILE_NAME]"
          }
        }
      },
      {
        "Sid": "RemainingRunInstancePermissions",
        "Effect": "Allow",
        "Action": [
          "ec2:RunInstances",
          "ec2:CreateTags"
        ],
        "Resource": [
          "arn:aws:ec2:*:*:volume/*",
          "arn:aws:ec2:*::image/*",
          "arn:aws:ec2:*::snapshot/*",
          "arn:aws:ec2:*:*:network-interface/*",
          "arn:aws:ec2:*:*:key-pair/*",
          "arn:aws:ec2:*:*:security-group/*"
        ]
      },
      {
        "Sid": "EC2VpcNonResourceSpecificActions",
        "Effect": "Allow",
        "Action": [
          "ec2:AuthorizeSecurityGroupIngress",
          "ec2:RevokeSecurityGroupIngress"
        ],
        "Resource": "*",
        "Condition": {
          "ArnLike": {
            "ec2:vpc": "arn:aws:ec2:*:*:vpc/[VPC_ID]"
          }
        }
      },
      {
        "Sid": "EC2BackupCreation",
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

### Step 4: Create your Hopsworks instance

You can now create a new Hopsworks instance in [managed.hopsworks.ai](https://managed.hopsworks.ai) by selecting the configured instance profile,
VPC and security group during instance configuration. Selecting any other VPCs or instance profiles will result in permissions errors.

### Step 5: Supporting multiple VPCs

The policy can be extended to give [managed.hopsworks.ai](https://managed.hopsworks.ai) access to multiple VPCs.
See: [Creating a Condition with Multiple Keys or Values](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_multi-value-conditions.html).

### Other removable permissions

There are other permissions that are required by Hopsworks to provide certain product capabilities to the users. In this section, we go through these permissions and what are the implication or removing them. 

#### Backup permissions

The following permissions are only needed for the backup feature. You can remove them if you are not going to create backups or if you do not have access to this Enterprise feature.

```json
      {
        "Sid": "EC2BackupCreation",
        "Effect": "Allow",
        "Action": [
          "ec2:RegisterImage",
          "ec2:DeregisterImage",
          "ec2:DescribeImages",
          "ec2:CreateSnapshot",
          "ec2:DeleteSnapshot",
          "ec2:DescribeSnapshots"
        ],
        "Resource": "*",
      }
```

#### Early warnings if VPC is not configured correctly

The following permissions are needed to give an early warning if your VPC and security groups are badly configured. You can remove them if you don't need it.
```json
          "ec2:DescribeVpcAttribute",
          "ec2:DescribeRouteTables"
```

#### Open and close ports from within Hopsworks.ai 

The following permissions are used to let you close and open ports on your cluster from hopswork.ai, you can remove them if you do not want to open ports on your cluster or if you want to manually open ports in EC2.

```json
      {
        "Sid": "EC2VpcNonResourceSpecificActions",
        "Effect": "Allow",
        "Action": [
          "ec2:AuthorizeSecurityGroupIngress",
          "ec2:RevokeSecurityGroupIngress",
        ],
        "Resource": "*",
        "Condition": {
          "ArnLike": {
            "ec2:vpc": "arn:aws:ec2:*:*:vpc/[VPC_ID]"
          }
        }
      }
```

#### Non resource based permissions used for listing 

If you are using terraform, then you can also remove most of the *Describe* permissions in `NonResourceBasedPermissions` and use the following permissions instead

```json
        {
            "Sid": "NonResourceBasedPermissions",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "ec2:DescribeVolumes",
                "ec2:DescribeSecurityGroups"
            ],
            "Resource": "*"
        },
```

#### Load balancers permissions for external access 
If you plan to access your Hopsworks cluster from an external python environment, especially if you plan to use the [ArrowFlight with DuckDB](../../common/arrow_flight_duckdb) and the [Feature Store REST API server](../../../user_guides/fs/feature_view/feature-server), then it is required to create a network load balancer that forward requests to the ArrowFlight server(s) co-located with the RonDB MySQL Server(s). If you are not planning to use ArrowFlight server(s) or multiple mysql server(s), you can skip adding the following permissions. If you still wish to use the ArrowFlight server(s) but without adding the following permissions to your cross account role, check [this advanced terraform example for more details](https://github.com/logicalclocks/terraform-provider-hopsworksai/tree/main/examples/complete/aws/advanced/arrowflight-no-loadbalancer-permissions).


```json 
      {
        "Sid": "ManageLoadBalancersForExternalAccess",
        "Effect": "Allow",
        "Action": [
            "elasticloadbalancing:CreateLoadBalancer",
            "elasticloadbalancing:CreateListener",
            "elasticloadbalancing:CreateTargetGroup",
            "elasticloadbalancing:RegisterTargets",
            "elasticloadbalancing:AddTags",
            "elasticloadbalancing:DescribeTargetGroups",
            "elasticloadbalancing:DeleteLoadBalancer",
            "elasticloadbalancing:DeleteTargetGroup"
        ],
        "Resource": "*"
    }
```


## Limiting the instance profile permissions

### Backups
If you do not intend to take backups or if you do not have access to this Enterprise feature you can remove the permissions that are only used by the backup feature when [configuring instance profile permissions](../getting_started/#step-3-creating-instance-profile) .
For this remove the following permissions from the instance profile:

```json
      "S3:PutLifecycleConfiguration", 
      "S3:GetLifecycleConfiguration", 
      "S3:PutBucketVersioning", 
      "S3:ListBucketVersions",
      "S3:DeleteObjectVersion",
```

### CloudWatch Logs
Hopsworks put its logs in Amazon CloudWatch so that you can access them without having to ssh into the machine. If you are not interested in this feature you can remove the following from your instance profile policy:

```json
    {
      "Effect": "Allow",
      "Action": [
        "cloudwatch:PutMetricData",
        "ec2:DescribeVolumes",
        "ec2:DescribeTags",
        "logs:PutLogEvents",
        "logs:DescribeLogStreams",
        "logs:DescribeLogGroups",
        "logs:CreateLogStream",
        "logs:CreateLogGroup"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ssm:GetParameter"
      ],
      "Resource": "arn:aws:ssm:*:*:parameter/AmazonCloudWatch-*"
    }
```
