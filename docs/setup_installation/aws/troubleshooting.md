# Troubleshooting

A list of common problems that you might encounter during cluster creation and how to solve them. 

## Unauthorized error during cluster creation

If you encounter the following error right after creating your cluster, then it is likely that you have either missed or misconfigured one of the permissions in the [cross account role setup](getting_started/#step-1-connecting-your-aws-account). 

<p align="center">
  <figure>
    <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/aws/troubleshooting-unauthorized-error.png" alt="Unauthorized error during cluster creation">
    <figcaption>Unauthorized error during cluster creation</figcaption>
  </figure>
</p>

In order to get more details regarding the authorization error above, you need to use the AWS Command Line Interface (AWS CLI) to decode the message using the `aws sts decode-authorization-message --encoded-message` command.

```
$ aws sts decode-authorization-message --encoded-message hg-Sh5-CUNT5jgB305YbOp_FDp2P70ZPw5iwoextxcdWmoc4wgm_K0pAUZEvTtCpvCk_-EwtaqaRS0act1BM-Bz-id4NOwo-OVZES5q9fLQIqk5_typL767idkb4jdzrrwNLD3h7iaaoleKGQpaW5kzI_oHEtibBRY2uWhU07oiwDHOAwb-cQ-kIA4nJIay7wVoL7QRx8nECpb56s68lMWhrdbqKj6uRQwsAILY7eoV-sDCbWWjnr98ja_olixhlV95txiV-oCR2qW6GKn4TVKl2raGbwjWRdS2GACP0fm7RUI_glPl7q65Erhrcr7Z2uF2SRF46VI5vfXkjXxv58e0x6SSRmKXF397e4QpPM6RyopmgDa9sSWAbkBxC86O9b30l47GX9w98trc76jsfU-UcdqK-Vu7Qy3-j8ehYMDpNvZRFNX64fUrsfusLJcHnhAPqUgCbvjfmEa605GkH7amlP2j23vprb94auzCVk8rgVkrSrBMek6YlWA0nzXtSjq8mVAvFE-n6x3ByLdt68Ldgc602FsFqifuzUm7CnjapIIwSAat_TXQCs-mjXyB983AEw__RwiXN
```

Then you will get the following message as response 
```json
{
    "DecodedMessage": "{\"allowed\":false,\"explicitDeny\":false,\"matchedStatements\":{\"items\":[]},\"failures\":{\"items\":[]},\"context\":{\"principal\":{\"id\":\"AROA27VDEGQLGDB4JOSOI:1f708920-18a6-11ed-8dd4-f162dca8fc19\",\"arn\":\"arn:aws:sts::xxxxx:assumed-role/cross-acount-role/1f708920-18a6-11ed-8dd4-f162dca8fc19\"},\"action\":\"ec2:CreateVpc\",\"resource\":\"arn:aws:ec2:us-east-2:xxxxx:vpc/*\",\"conditions\":{\"items\":[{\"key\":\"aws:Region\",\"values\":{\"items\":[{\"value\":\"us-east-2\"}]}},{\"key\":\"aws:Service\",\"values\":{\"items\":[{\"value\":\"ec2\"}]}},{\"key\":\"aws:Resource\",\"values\":{\"items\":[{\"value\":\"vpc/*\"}]}},{\"key\":\"aws:Type\",\"values\":{\"items\":[{\"value\":\"vpc\"}]}},{\"key\":\"aws:Account\",\"values\":{\"items\":[{\"value\":\"xxxxxx\"}]}},{\"key\":\"ec2:VpcID\",\"values\":{\"items\":[{\"value\":\"*\"}]}},{\"key\":\"aws:ARN\",\"values\":{\"items\":[{\"value\":\"arn:aws:ec2:us-east-2:xxxx:vpc/*\"}]}}]}}}"
}
```

From the above response we can see that the cross-account role is missing the `ec2:CreateVpc` permission. The solution is to terminate the cluster in error and update [cross account role setup](getting_started/#step-1-connecting-your-aws-account) with the missing permission(s) and then try to create a new cluster.

## Missing permissions error during cluster creation

If you encounter the following error right after creating your cluster, then the issue is with the instance profile permissions.  

<p align="center">
  <figure>
    <img style="border: 1px solid #000;width:700px" src="../../../assets/images/setup_installation/managed/aws/troubleshooting-missing-permissions-error.png" alt="Missing permissions error during cluster creation">
    <figcaption>Missing permissions error during cluster creation</figcaption>
  </figure>
</p>

This issue could be caused by one of the following:

* The [instance profile that you have chosen during cluster creation](cluster_creation/#step-5-select-the-instance-profile) is actually missing the permissions stated in the error  on your [chosen S3 bucket](cluster_creation/#step-2-setting-the-general-information). Then in that case, update your instance profile accordingly and then click *Retry* to retry cluster creation operation. 

* Your AWS organization is using [SCPs policy](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html) that disallow policy simulation. In that case, you could do a simple test to confirm the issue by using [the AWS PolicySim on AWS console](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html). If policy simulation is disallowed, you can configure managed.hopsworks.ai to skip the policy simulation step by removing the `iam:SimulatePrincipalPolicy` permission from [your cross account role](getting_started/#step-1-connecting-your-aws-account), by navitgating to the [AWS Roles console](https://us-east-1.console.aws.amazon.com/iamv2/home#/roles), search for your cross account role name and click on it, on the permissions tab click edit on hopsworks inline policy, choose JSON tab, remove `iam:SimulatePrincipalPolicy`, click *Review Policy*, and then click *Save Changes*, and finally navigate back to manged.hopsworks.ai and click *Retry* to retry the cluster creation.
