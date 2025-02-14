---
description: Documentation on how to connect to Hopsworks from a Java client.
---

# Java client

Starting from version 3.9.0-RC13, HSFS provides a pure Java client. This guide explains how to use the client to connect to Hopsworks and read or write feature data.

## Generate an API key

For instructions on how to generate an API key follow this [user guide](../projects/api_key/create_api_key.md). For the Java client to work correctly make sure you add the following scopes to your API key:

  1. featurestore
  2. project
  3. job
  4. kafka

## Add the HSFS dependency to your project:

The HSFS library is available on the Hopsworks' Maven repository. If you are using Maven as build tool, you can add the following in your pom.xml file:

```xml
<repositories>
    <repository>
        <id>Hops</id>
        <name>Hops Repository</name>
        <url>https://archiva.hops.works/repository/Hops/</url>
        <releases>
            <enabled>true</enabled>
        </releases>
        <snapshots>
            <enabled>true</enabled>
        </snapshots>
    </repository>
</repositories>
```

The artifactId for the HSFS Java build is hsfs, if you are using Maven as build tool, you can add the following dependency:

```xml
<dependency>
    <groupId>com.logicalclocks</groupId>
    <artifactId>hsfs</artifactId>
    <version>${hsfs.version}</version>
</dependency>
```

!!!note "Java Version"

    Please note that the Java client has been tested with Java versions up to Java 17

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

### Update feature data

The Java client allows you to update data on existing feature groups using the streaming interface. You can provide a list of POJO objects to the [insertStream](https://docs.hopsworks.ai/feature-store-api/{{{ hopsworks_version }}}/javadoc/com/logicalclocks/hsfs/StreamFeatureGroup.html#insertStream-java.util.List-) method.

The feature group should exists already (can be created using the Python client) and the POJO objects should be serializable with the feature group's AVRO schema. 

Please see the [tutorial](https://github.com/logicalclocks/hopsworks-tutorials/tree/master/integrations/java/java) for a code example on how to write data.

### Limitations

Currently using the Java client to retrieve feature vectors have the following limitations:

* Only the SQL interface is supported. It is not possible to retrieve feature vectors using the REST API Interface
* Feature Views with model dependent transformations attached are not applied. If your feature view has model dependent transformations, please use the Python client.

## Next Steps

You can find more information on how to interact from Java client in the [JavaDoc](https://docs.hopsworks.ai/feature-store-api/{{{ hopsworks_version }}}/javadoc/) or this [tutorial](https://github.com/logicalclocks/hopsworks-tutorials/tree/master/integrations/java/java)