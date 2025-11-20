---
description: Documentation on how to configure an external Spark cluster to read and write features from the Hopsworks Feature Store
---
# Spark Integration

Connecting to the Feature Store from an external Spark cluster, such as Cloudera, requires configuring it with the Hopsworks client jars and configuration.
This guide explains step by step how to connect to the Feature Store from an external Spark cluster.

## Download the Hopsworks Client Jars

In the *Project Settings*, select the *integration* tab and scroll to the *Configure Spark Integration* section.
Click on *Download client Jars*.
This will start the download of the *client.tar.gz* archive.
The archive contains two jar files for HopsFS, the Apache Hudi jar and the Java version of the HSFS library.
You should upload these libraries to your Spark cluster and attach them as local resources to your Job.
If you are using `spark-submit`, you should specify the `--jar` option.
For more details see: [Spark Dependency Management](https://spark.apache.org/docs/latest/submitting-applications.html#advanced-dependency-management).

<p align="center">
    <figure>
        <img src="../../../assets/images/guides/integrations/spark_integration.png" alt="Spark integration tab">
        <figcaption>The Spark Integration gives access to Jars and configuration for an external Spark cluster</figcaption>
    </figure>
</p>

## Download the certificates

Download the certificates from the same section as above.
Hopsworks uses X.509 certificates for authentication and authorization.
If you are interested in the Hopsworks security model, you can read more about it in this [blog post](https://www.logicalclocks.com/blog/how-we-secure-your-data-with-hopsworks).
The certificates are composed of three different components: the `keyStore.jks` containing the private key and the certificate for your project user, the `trustStore.jks` containing the certificates for the Hopsworks certificates authority, and a password to unlock the private key in the `keyStore.jks`.
The password is displayed in a pop-up when downloading the certificate and should be saved in a file named `material_passwd`.

!!! warning
    When you copy-paste the password to the `material_passwd` file, pay attention to not introduce additional empty spaces or new lines.

The three files (`keyStore.jks`, `trustStore.jks` and `material_passwd`) should be attached as resources to your Spark application as well.

## Configure your Spark cluster

!!! warning "Spark version limitation"

    Currently Spark version 3.3.x is suggested to be able to use the full suite of Hopsworks Feature Store capabilities.

Add the following configuration to the Spark application:

```
spark.hadoop.fs.hopsfs.impl                         io.hops.hopsfs.client.HopsFileSystem
spark.hadoop.hops.ipc.server.ssl.enabled            true
spark.hadoop.hops.ssl.hostname.verifier             ALLOW_ALL
spark.hadoop.hops.rpc.socket.factory.class.default  io.hops.hadoop.shaded.org.apache.hadoop.net.HopsSSLSocketFactory
spark.hadoop.client.rpc.ssl.enabled.protocol        TLSv1.2
spark.hadoop.hops.ssl.keystores.passwd.name         material_passwd
spark.hadoop.hops.ssl.keystore.name                 keyStore.jks
spark.hadoop.hops.ssl.trustore.name                 trustStore.jks
spark.sql.hive.metastore.jars                       path
spark.sql.hive.metastore.jars.path                  [Path to the Hopsworks Hive Jars]
spark.hadoop.hive.metastore.uris                    thrift://[metastore_ip]:[metastore_port]
```

`spark.sql.hive.metastore.jars.path` should point to the path with the jars from the uncompressed Hive archive you can find in *clients.tar.gz*.

## PySpark

To use PySpark, install the HSFS Python library which can be found on [PyPi](https://pypi.org/project/hsfs/).

!!! attention "Matching Hopsworks version"
    The **major version of `HSFS`** needs to match the **major version of Hopsworks**.

## Generating an API Key

For instructions on how to generate an API key follow this [user guide](../projects/api_key/create_api_key.md).
For the Spark integration to work correctly make sure you add the following scopes to your API key:

  1. featurestore
  2. project
  3. job
  4. kafka

## Connecting to the Feature Store

You are now ready to connect to the Hopsworks Feature Store from Spark:

```python
import hopsworks
project = hopsworks.login(
    host='my_instance',                 # DNS of your Feature Store instance
    port=443,                           # Port to reach your Hopsworks instance, defaults to 443
    project='my_project',               # Name of your Hopsworks Feature Store project
    api_key_value='api_key',            # The API key to authenticate with the feature store
    hostname_verification=True          # Disable for self-signed certificates
)
fs = project.get_feature_store()           # Get the project's default feature store
```

!!! note "Engine"

    `Hopsworks` leverages several engines depending on whether you are running using Apache Spark or Pandas/Polars.
    The default behaviour of the library is to use the `spark` engine if you do not specify any `engine` option in the `login` method and if the `PySpark` library is available in the environment.

## Next Steps

For more information about how to connect, see the [Login API](<https://docs.hopsworks.ai/hopsworks-api/{{{> hopsworks_version }}}/generated/api/login/) API reference.
Or continue with the Data Source guide to import your own data to the Feature Store.
