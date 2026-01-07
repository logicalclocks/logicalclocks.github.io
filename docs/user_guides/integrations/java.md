---
description: Documentation on how to connect to Hopsworks from a Java client.
---

# Java client

This guide explains step by step how to connect to Hopsworks from a Java client.

## Generate an API key

For instructions on how to generate an API key follow this [user guide](../projects/api_key/create_api_key.md).
For the Java client to work correctly make sure you add the following scopes to your API key:

  1. featurestore
  2. project
  3. job
  4. kafka

## Connecting to the Feature Store

You are now ready to connect to the Hopsworks Feature Store from a Java client:

```Java
//Import necessary classes
import com.logicalclocks.hsfs.FeatureStore;
import com.logicalclocks.hsfs.FeatureView;
import com.logicalclocks.hsfs.HopsworksConnection;

//Establish connection with Hopsworks.
HopsworksConnection hopsworksConnection = HopsworksConnection.builder()
  .host("my_instance")                      // DNS of your Feature Store instance
  .port(443)                                // Port to reach your Hopsworks instance, defaults to 443
  .project("my_project")                    // Name of your Hopsworks Feature Store project
  .apiKeyValue("api_key")                   // The API key to authenticate with the feature store
  .hostnameVerification(false)               // Disable for self-signed certificates
  .build();

//get feature store handle
FeatureStore fs = hopsworksConnection.getFeatureStore();

//get feature view handle
FeatureView fv = fs.getFeatureView(fvName, fvVersion);

// get feature vector
List<Object> singleVector = fv.getFeatureVector(new HashMap<String, Object>() {{
        put("id", 100);
        }});
```

## Next Steps

For more information how to interact from Java client with the Hopsworks Feature store follow this [tutorial](https://github.com/logicalclocks/hopsworks-tutorials/tree/java_engine/java).
