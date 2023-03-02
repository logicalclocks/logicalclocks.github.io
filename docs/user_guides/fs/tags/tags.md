# Tags 

## Introduction

Hopsworks feature store enables users to attach tags to artifacts, such as feature groups, feature views or training datasets.

A tag is a `{key: value}` pair which provides additional information about the data managed by Hopsworks. Tags allow you to design custom metadata for your artifacts. For example, you could design a tag schema that encodes governance rules for your feature store, such as classifying data as personally identifiable, defining a data retention period for the data, and defining who signed off on the creation of some feature.

## Prerequisites

Tags have a schema. Before you can attach a tag to an artifact and fill in the tag values, you first need to select an existing tag schema or create a new tag schema.

Tag schemas can be defined by Hopsworks administrator in the `Cluster settings` section of the platform. Schemas are defined globally across all projects. When users attach tags to an artifact, the tag will be validated against a specific schema. This allows tags to be consistent no matter the project or the team generating them. 

!!! warning "Immutable"
    Tag schemas are immutable. Once defined, a tag schema cannot be edited nor deleted. 

## Step 1: Define a tag schema

Tag schemas can be defined using the UI wizard in the `Cluster settings` > `Tag schemas` section. 
Tag schemas have a name, the name is used to uniquely identify the schema. You can also provide an optional description.

You can define a schema by using the UI tool or by providing the schema in JSON format.
If you use the UI tool, you should provide the name of the property in the schema, the type of the property, whether or not the property is required and an optional description. 

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/tags/tags_schema_simple.png" alt="UI tag schema definition">
    <figcaption>UI tag schema definition</figcaption>
  </figure>
</p>

The UI tool allows you to define simple not-nested schemas. For more advanced use cases, more complex schemas (e.g. nested schemas) might be required to fully express the content of a given artifact.
In such cases it is possible to provide the schema directly as JSON string. The JSON should follow the standard [https://json-schema.org](https://json-schema.org). An example of complex schema is the following:

```
{
  "type" : "object",
  "properties" :
  {
    "first_name" : { "type" : "string" },
    "last_name" : { "type" : "string" },
    "age" : { "type" : "integer" },
    "hobbies" : {
        "type" : "array",
        "items" : { "type" : "string" }
    }
  },
  "required" : ["first_name", "last_name", "age"],
  "additionalProperties": false
}
```

Additionally it is also possible to define a single property as tag. You can achieve this by defining a JSON schema like the following:

```
{ "type" : "string" }
```

Where the type is a valid primitive type: `string`, `boolean`, `integer`, `number`.

## Step 2: Attach a tag to an artifact

Once the tag schema has been created, you can attach a tag with that schema to a feature group, feature view or training datasets either using the feature store APIs, or by using the UI.

### Using the API

You can attach tags to feature groups and feature views by using the `add_tag()` method of the feature store APIs:

=== "Python"

    ```python
    # Retrieve the feature group
    fg = fs.get_feature_group("transactions_4h_aggs_fraud_batch_fg", version=1)

    # Define the tag
    tag = {
        'business_unit': 'Fraud',
        'data_owner': 'email@hopsworks.ai',
        'pii': True
    }

    # Attach the tag
    fg.add_tag("data_privacy", tag) 
    ```

You can see the list of tags attached to a given artifact by using the `get_tags()` method:

=== "Python"

    ```python
    # Retrieve the feature group
    fg = fs.get_feature_group("transactions_4h_aggs_fraud_batch_fg", version=1)

    # Retrieve the tags for this feature group 
    fg.get_tags()
    ```

Finally you can remove a tag from a given artifact by calling the `delete_tag()` method:

=== "Python"

    ```python
    # Retrieve the feature group
    fg = fs.get_feature_group("transactions_4h_aggs_fraud_batch_fg", version=1)

    # Retrieve the tags for this feature group 
    fg.delete_tag("data_privacy")
    ```

The same APIs work for feature views and training dataset alike.

### Using the UI

You can attach tags to feature groups and feature views directly from the UI. You can navigate on the artifact page and click on the `Add tags` button. From there you can select the tag schema of the tag you want to attach and populate the values as shown in the gif below.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/tags/tags_ui.gif" alt="Attach tag to a feature group">
    <figcaption>Attach tag to a feature group</figcaption>
  </figure>
</p>

## Step 3: Search

Hopsworks indexes the tags attached to feature groups, feature views and training datasets. The tags will then be searchable using the free text search box located at the top of the UI. 

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/tags/search_ui.gif" alt="Search for tags in the feature store">
    <figcaption>Search for tags in the feature store</figcaption>
  </figure>
</p>