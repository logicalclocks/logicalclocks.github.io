
Replace the following placeholders with their appropriate values

* *BUCKET_NAME* - S3 bucket name 
* *REGION* - region where the cluster is deployed
* *ECR_AWS_ACCOUNT_ID* - AWS account id for ECR repositories

!!! note
    Some of these permissions can be removed. Refer to [this guide](restrictive_permissions.md#limiting-the-instance-profile-permissions) for more information.

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
      "Sid": "AllowPullImagesFromHopsworkAi",
      "Effect": "Allow",
      "Action": [
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage"
      ],
      "Resource": [
        "arn:aws:ecr:REGION:822623301872:repository/filebeat",
        "arn:aws:ecr:REGION:822623301872:repository/base",
        "arn:aws:ecr:REGION:822623301872:repository/onlinefs",
        "arn:aws:ecr:REGION:822623301872:repository/airflow",
        "arn:aws:ecr:REGION:822623301872:repository/git",
        "arn:aws:ecr:REGION:822623301872:repository/testconnector",
        "arn:aws:ecr:REGION:822623301872:repository/flyingduck"
      ]
    },
    {
      "Sid": "AllowCreateRespositry",
      "Effect": "Allow",
      "Action": "ecr:CreateRepository",
      "Resource": "*"
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
        "arn:aws:ecr:REGION:ECR_AWS_ACCOUNT_ID:repository/*/filebeat",
        "arn:aws:ecr:REGION:ECR_AWS_ACCOUNT_ID:repository/*/base",
        "arn:aws:ecr:REGION:ECR_AWS_ACCOUNT_ID:repository/*/onlinefs",
        "arn:aws:ecr:REGION:ECR_AWS_ACCOUNT_ID:repository/*/airflow",
        "arn:aws:ecr:REGION:ECR_AWS_ACCOUNT_ID:repository/*/git",
        "arn:aws:ecr:REGION:ECR_AWS_ACCOUNT_ID:repository/*/testconnector",
        "arn:aws:ecr:REGION:ECR_AWS_ACCOUNT_ID:repository/*/flyingduck"
      ]
    },
    {
      "Sid": "AllowGetAuthToken",
      "Effect": "Allow",
      "Action": "ecr:GetAuthorizationToken",
      "Resource": "*"
    },
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
  ]
}
```
