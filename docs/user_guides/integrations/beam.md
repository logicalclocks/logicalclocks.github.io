---
description: Documentation on how to configure an Apache Beam Dataflow Runner job to write features to the Hopsworks Feature Store
---
# Apache Beam Dataflow Runner

Connecting to the Feature Store from an Apache Beam Dataflow Runner, requires configuring the Hopsworks certificates. For this in your Beam Java application `pom.xml` file include following snippet:

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

For instructions on how to generate an API key follow this [user guide](../projects/api_key/create_api_key.md). For the Beam integration to work correctly make sure you add the following scopes to your API key:

  1. featurestore
  2. project
  3. job
  4. kafka

## Connecting to the Feature Store

You are now ready to connect to the Hopsworks Feature Store from Beam:

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

For more information and how to integrate Beam feature pipeline  to the Hopsworks Feature store follow the [tutorial](https://github.com/logicalclocks/hopsworks-tutorials/tree/master/integrations/java/beam).
