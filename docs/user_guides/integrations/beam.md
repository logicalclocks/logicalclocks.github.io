---
description: Documentation on how to configure an Apache Beam Dataflow Runner job to write features in to the Hopsworks Feature Store
---
# Apache Beam DataflowRunner

Connecting to the Feature Store from an Apache Beam Dataflow Runner, requires Hopsworks certificates. For this in your Beam Java application `pom.xml` file include following snippet:
```
    <resources>
      <resource>
        <directory>java.io.tmpdir</directory>
        <includes>
          <include>**/*.jks</include>
        </includes>
      </resource>
    </resources>
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

For more information about how to connect, see the [Connection](https://docs.hopsworks.ai/feature-store-api/{{{ hopsworks_version }}}/generated/api/connection_api/) API reference.