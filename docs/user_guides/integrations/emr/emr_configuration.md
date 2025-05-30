---
description: Documentation on how to configure an EMR cluster to read and write features from the Hopsworks Feature Store
---
# Configure EMR for the Hopsworks Feature Store
To enable EMR to access the Hopsworks Feature Store, you need to set up a Hopsworks API key, add a bootstrap action and configurations to your EMR cluster.

!!! info
    Ensure [Networking](networking.md) is set up correctly before proceeding with this guide.

## Step 1: Set up a Hopsworks API key

For instructions on how to generate an API key follow this [user guide](../../projects/api_key/create_api_key.md). For the EMR integration to work correctly make sure you add the following scopes to your API key:

  1. featurestore
  2. project
  3. job
  4. kafka

### Store the API key in the AWS Secrets Manager

In the AWS management console ensure that your active region is the region you use for EMR.
Go to the *AWS Secrets Manager* and select *Store new secret*. Select *Other type of secrets* and add *api-key*
as the key and paste the API key created in the previous step as the value. Click next.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/integrations/databricks/aws/databricks_secrets_manager_step_1.png" alt="Store a Hopsworks API key in the Secrets Manager">
    <figcaption>Store a Hopsworks API key in the Secrets Manager</figcaption>
  </figure>
</p>

As a secret name, enter *hopsworks/featurestore*. Select next twice and finally store the secret.
Then click on the secret in the secrets list and take note of the *Secret ARN*.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/integrations/emr/secrets_manager.png" alt="Name the secret">
    <figcaption>Name the secret</figcaption>
  </figure>
</p>

### Grant access to the secret to the EMR EC2 instance profile

Identify your EMR EC2 instance profile in the EMR cluster summary:
<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/integrations/emr/emr_instance_profile.png" alt="Identify your EMR EC2 instance profile">
    <figcaption>Identify your EMR EC2 instance profile</figcaption>
  </figure>
</p>


In the AWS Management Console, go to *IAM*, select *Roles* and then the EC2 instance profile used by your EMR cluster.
Select *Add inline policy*. Choose *Secrets Manager* as a service, expand the *Read* access level and check *GetSecretValue*.
Expand Resources and select *Add ARN*. Paste the ARN of the secret created in the previous step.
Click on *Review*, give the policy a name and click on *Create policy*.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/integrations/emr/emr_policy.png" alt="Configure the access policy for the Secrets Manager">
    <figcaption>Configure the access policy for the Secrets Manager</figcaption>
  </figure>
</p>

## Step 2: Configure your EMR cluster

### Add the Hopsworks Feature Store configuration to your EMR cluster
In order for EMR to be able to talk to the Feature Store, you need to update the Hadoop and Spark configurations.
Copy the configuration below and replace ip-XXX-XX-XX-XXX.XX-XXXX-X.compute.internal with the private DNS name of your Hopsworks master node.

```json
[
  {
    "Classification": "hadoop-env",
    "Properties": {

    },
    "Configurations": [
      {
        "Classification": "export",
        "Properties": {
          "HADOOP_CLASSPATH": "$HADOOP_CLASSPATH:/usr/lib/hopsworks/client/*"
        },
        "Configurations": [

        ]
      }
    ]
  },
  {
    "Classification": "spark-defaults",
    "Properties": {
      "spark.hadoop.hops.ipc.server.ssl.enabled": true,
      "spark.hadoop.fs.hopsfs.impl": "io.hops.hopsfs.client.HopsFileSystem",
      "spark.hadoop.client.rpc.ssl.enabled.protocol": "TLSv1.2",
      "spark.hadoop.hops.ssl.hostname.verifier": "ALLOW_ALL",
      "spark.hadoop.hops.rpc.socket.factory.class.default": "io.hops.hadoop.shaded.org.apache.hadoop.net.HopsSSLSocketFactory",
      "spark.hadoop.hops.ssl.keystores.passwd.name": "/usr/lib/hopsworks/material_passwd",
      "spark.hadoop.hops.ssl.keystore.name": "/usr/lib/hopsworks/keyStore.jks",
      "spark.hadoop.hops.ssl.trustore.name": "/usr/lib/hopsworks/trustStore.jks",
      "spark.serializer": "org.apache.spark.serializer.KryoSerializer",
      "spark.executor.extraClassPath": "/usr/lib/hopsworks/client/*",
      "spark.driver.extraClassPath": "/usr/lib/hopsworks/client/*",
      "spark.sql.hive.metastore.jars": "path",
      "spark.sql.hive.metastore.jars.path": "/usr/lib/hopsworks/apache-hive-bin/lib/*",
      "spark.hadoop.hive.metastore.uris": "thrift://ip-XXX-XX-XX-XXX.XX-XXXX-X.compute.internal:9083"
    }
  },
]
```

When you create your EMR cluster, add the configuration:

!!! note
    Don't forget to replace ip-XXX-XX-XX-XXX.XX-XXXX-X.compute.internal with the private DNS name of your Hopsworks master node.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/integrations//emr/emr_config.png" alt="Configure EMR to access the Feature Store">
    <figcaption>Configure EMR to access the Feature Store</figcaption>
  </figure>
</p>

### Add the Bootstrap Action to your EMR cluster

EMR requires Hopsworks connectors to be able to communicate with the Hopsworks Feature Store. These connectors can be installed with the
bootstrap action shown below. Copy the content into a file and name the file `hopsworks.sh`. Copy that file into any S3 bucket that
is readable by your EMR clusters and take note of the S3 URI of that file e.g., `s3://my-emr-init/hopsworks.sh`.

```bash
#!/bin/bash
set -e

if [ "$#" -ne 3 ]; then
    echo "Usage hopsworks.sh HOPSWORKS_API_KEY_SECRET, HOPSWORKS_HOST, PROJECT_NAME"
    exit 1
fi

SECRET_NAME=$1
HOST=$2
PROJECT=$3

API_KEY=$(aws secretsmanager get-secret-value --secret-id $SECRET_NAME | jq -r .SecretString | jq -r '.["api-key"]')

PROJECT_ID=$(curl -H "Authorization: ApiKey ${API_KEY}" https://$HOST/hopsworks-api/api/project/getProjectInfo/$PROJECT | jq -r .projectId)

sudo yum -y install python3-devel.x86_64 || true

sudo mkdir /usr/lib/hopsworks
sudo chown hadoop:hadoop /usr/lib/hopsworks
cd /usr/lib/hopsworks

curl -o client.tar.gz -H "Authorization: ApiKey ${API_KEY}" https://$HOST/hopsworks-api/api/project/$PROJECT_ID/client

tar -xvf client.tar.gz
tar -xzf client/apache-hive-*-bin.tar.gz || true
mv apache-hive-*-bin apache-hive-bin
rm client.tar.gz
rm client/apache-hive-*-bin.tar.gz

curl -H "Authorization: ApiKey ${API_KEY}" https://$HOST/hopsworks-api/api/project/$PROJECT_ID/credentials | jq -r .kStore | base64 -d > keyStore.jks

curl -H "Authorization: ApiKey ${API_KEY}" https://$HOST/hopsworks-api/api/project/$PROJECT_ID/credentials | jq -r .tStore | base64 -d > trustStore.jks

echo -n $(curl -H "Authorization: ApiKey ${API_KEY}" https://$HOST/hopsworks-api/api/project/$PROJECT_ID/credentials | jq -r .password) > material_passwd

chmod -R o-rwx /usr/lib/hopsworks

sudo pip3 install --upgrade hopsworks~=X.X.0

```
!!! attention "Matching Hopsworks version"

    We recommend that the major and minor version of the Python library match the major and minor version of the Hopsworks deployment.

    <p align="center">
        <figure>
            <img src="../../../../assets/images/hopsworks-version.png" alt="The library version needs to match the major version of Hopsworks">
            <figcaption>You find the Hopsworks version inside any of your Project's settings tab on Hopsworks</figcaption>
        </figure>
    </p>

Add the bootstrap actions when configuring your EMR cluster. Provide 3 arguments to the bootstrap action: The name of the API key secret e.g., `hopsworks/featurestore`,
the public DNS name of your Hopsworks cluster, such as `ad005770-33b5-11eb-b5a7-bfabd757769f.cloud.hopsworks.ai`, and the name of your Hopsworks project, e.g. `demo_fs_meb10179`.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/integrations/emr/emr_bootstrap_action.png" alt="Set the bootstrap action for EMR">
    <figcaption>Set the bootstrap action for EMR</figcaption>
  </figure>
</p>

Your EMR cluster will now be able to access your Hopsworks Feature Store.

## Next Steps

Use the [Login API](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/api/login/) to connect to the Hopsworks Feature Store. For more information about how to use the Feature Store, see the [Quickstart Guide](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/quickstart.ipynb){:target="_blank"}.
