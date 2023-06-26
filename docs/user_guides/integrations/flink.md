---
description: Documentation on how to configure an external Flink cluster to write features to the Hopsworks Feature Store
---
# Flink Integration

Connecting to the Feature Store from an external Flink cluster, such as AWS EMR and GCP DataProc requires configuring it with the Hopsworks certificates. This guide explains step by step how to connect to the Feature Store from an external Flink cluster.

## Download the Hopsworks Certificates
In the *Project Settings*, select the *integration* tab and scroll to the *Configure Spark Integration* section. Click on *Download certificates*. 

<p align="center">
    <figure>
        <img src="../../../assets/images/guides/integrations/spark_integration.png" alt="Spark integration tab">
        <figcaption>The Spark Integration gives access to Jars and configuration for an external Spark cluster</figcaption>
    </figure>
</p>

Hopsworks uses X.509 certificates for authentication and authorization. If you are interested in the Hopsworks security model, you can read more about it in this [blog post](https://www.hopsworks.ai/post/how-we-secure-your-data-with-hopsworks).
The certificates are composed of three different components: the `keyStore.jks` containing the private key and the certificate for your project user, the `trustStore.jks` containing the certificates for the Hopsworks certificates authority, and a password to unlock the private key in the `keyStore.jks`. The password is displayed in a pop-up when downloading the certificate and should be saved in a file named `material_passwd`.

!!! warning
    When you copy-paste the password to the `material_passwd` file, pay attention to not introduce additional empty spaces or new lines.

The three files (`keyStore.jks`, `trustStore.jks` and `material_passwd`) should be accessible by your Flink application.

## Configure your Flink cluster

Add the following configuration to the `flink-conf.yaml`:

```
flink.hadoop.hops.ssl.keystore.name: replace_this_with_actual_path/keyStore.jks
flink.hadoop.hops.ssl.truststore.name: replace_this_with_actual_path/trustStore.jks
flink.hadoop.hops.ssl.keystores.passwd.name: replace_this_with_actual_path/material_passwd
```

## Generating an API Key

For instructions on how to generate an API key follow this [user guide](../projects/api_key/create_api_key.md). For the Flink integration to work correctly make sure you add the following scopes to your API key:

  1. featurestore
  2. project
  3. job
  4. kafka

## Connecting to the Feature Store

You are now ready to connect to the Hopsworks Feature Store from Flink:

```Java
//Establish connection with Hopsworks.
HopsworksConnection hopsworksConnection = HopsworksConnection.builder()
  .host("my_instance")                      // DNS of your Feature Store instance
  .port(443)                                // Port to reach your Hopsworks instance, defaults to 443
  .project("my_project")                    // Name of your Hopsworks Feature Store project 
  .apiKeyValue("api_key")                   // The API key to authenticate with the feature store
  .hostnameVerification(false)              // Disable for self-signed certificates
  .build();

//get feature store handle
FeatureStore fs = hopsworksConnection.getFeatureStore();
```

## Next Steps

For more information and how to integrate Flink streaming feature pipeline to the Hopsworks Feature store follow the [tutorial](https://github.com/logicalclocks/hopsworks-tutorials/tree/master/integrations/java/flink).