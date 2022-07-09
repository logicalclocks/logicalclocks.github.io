# Deploy in a VPC with a custom domain name

Some organizations follow network patterns which impose a specific domain
name for Instances. In that case, the instance's hostname instead of `ip-10-0-0-175.us-east-2.compute.internal` would be `ip-10-0-0-175.bar.foo`

The control plane at [hopsworks.ai](https://www.hopsworks.ai/) needs to be
aware of such case in order to properly initialize the Cluster.

!!! note
    This feature is enabled **only** upon request. If you want this feature to be enable for your account please contact [sales](mailto:sales@logicalclocks.com)

There are multiple ways to use custom domain names in your organization
which are beyond the scope of this guide. We assume your cloud/network
team has already setup the infrastructure.

If you are using a resolver such as [Amazon Route 53](https://aws.amazon.com/route53/), it is advised to update the record sets automatically. See our
guide below for more information.

## Set cluster domain name

If this feature is enabled for your account, then in the [VPC selection](../cluster_creation/#step-8-vpc-selection)
step you will have the option to specify the custom domain name as
shown in the figure below.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/aws/vpc-custom-domain-name.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/aws/vpc-custom-domain-name.png" alt="Custom domain name">
    </a>
    <figcaption>VPC with custom domain name</figcaption>
  </figure>
</p>

In this case, the hostname of the Instance would be `INSTANCE_ID.dev.hopsworks.domain`

Hostnames **must** be resolvable by all Virtual Machines in the cluster. For
that reason we suggest, if possible, to automatically register the hostnames
with your DNS.

In the following section we present an example of automatic
name registration in Amazon Route 53

## Auto registration with Amazon Route 53

It is quite common for organizations in AWS to use Route 53 for DNS or for hosted zones.
You can configure a cluster in _hopsworks.ai_ to execute some custom
initialization script **before** any other action. This script will
be executed on all nodes of the cluster.

Since the hostname of the VM is in the form of `INSTANCE_ID.DOMAIN_NAME`
it is easy to automate the zone update. The script below creates an A record
in a configured Route 53 hosted zone.

!!! warning
    If you want the VM to register itself with Route 53 you **must** amend the
    [Instance Profile](cluster_creation/#step-5-select-the-instance-profile) with the following permissions

```json
{
    "Sid": "Route53RecordSet",
    "Effect": "Allow",
    "Action": [
        "route53:ChangeResourceRecordSets"
    ],
    "Resource": "arn:aws:route53:::hostedzone/YOUR_HOSTED_ZONE_ID"
},
{
    "Sid": "Route53GetChange",
    "Effect": "Allow",
    "Action": [
        "route53:GetChange"
    ],
    "Resource": "arn:aws:route53:::change/*"
}
```

The following script will get the instance ID from the EC2 metadata server
and add an A record to the hosted zone in Route53. **Update** the 
`YOUR_HOSTED_ZONE_ID` and `YOUR_CUSTOM_DOMAIN_NAME` to match yours.

```bash
#!/usr/bin/env bash
set -e

HOSTED_ZONE_ID=YOUR_HOSTED_ZONE_ID
ZONE=YOUR_CUSTOM_DOMAIN_NAME

record_set_file=/tmp/record_set.json

instance_id=$(curl --silent http://169.254.169.254/2016-09-02/meta-data/instance-id)

domain_name="${instance_id}.${ZONE}"

local_ip=$(curl --silent http://169.254.169.254/2016-09-02/meta-data/local-ipv4)

cat << EOC | tee $record_set_file
{
    "Changes": [
        {
            "Action": "UPSERT",
            "ResourceRecordSet": {
                "Name": "${domain_name}",
                "Type": "A",
                "TTL": 60,
                "ResourceRecords": [
                    {
                        "Value": "${local_ip}"
                    }
                ]
            }
        }
    ]
}
EOC

echo "Adding A record ${domain_name} -> ${local_ip} to Hosted Zone ${HOSTED_ZONE_ID}"
change_resource_id=$(aws route53 change-resource-record-sets --hosted-zone-id ${HOSTED_ZONE_ID} --change-batch file://${record_set_file} | jq -r '.ChangeInfo.Id')

echo "Change resource ID: ${change_resource_id}"
aws route53 wait resource-record-sets-changed --id ${change_resource_id}
echo "Added resource record set"

rm -f ${record_set_file}
```

## Set VM initialization script
As a final step you need to configure the Cluster to use the script above
during VM creation with the [user init script](../cluster_creation/#step-14-add-an-init-script-to-your-instances) option.

Paste the script to the text box and **make sure** you select this script
to be executed before anything else on the VM.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/aws/custom-domain-name-route53-script.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/aws/custom-domain-name-route53-script.png" alt="Automatic domain name registration">
    </a>
    <figcaption>Automatic domain name registration with Route53</figcaption>
  </figure>
</p>
