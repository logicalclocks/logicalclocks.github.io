# Tags { #tags-guide }

## Introduction

Hopsworks enables users to attach tags to artifacts, such as feature groups, feature views, training datasets, models, deployments, jobs or datasets.

A tag is a `{key: value}` pair which provides additional information about the data managed by Hopsworks.
Tags allow you to design custom metadata for your artifacts.
For example, you could design a tag schema that encodes governance rules for your feature store, such as classifying data as personally identifiable, defining a data retention period for the data, and defining who signed off on the creation of some feature.

## Prerequisites

Tags have a schema.
Before you can attach a tag to an artifact and fill in the tag values, you first need to select an existing tag schema or create a new tag schema.

Tag schemas can be defined by Hopsworks administrator in the `Cluster settings` section of the platform.
Schemas are defined globally across all projects.
When users attach tags to an artifact, the tag will be validated against a specific schema.
This allows tags to be consistent no matter the project or the team generating them.

!!! warning "Schema definitions cannot be edited"
    The JSON schema of a tag schema cannot be changed after it is created, because the values already attached were validated against the original definition.
    A schema can be deprecated so that it accepts no new attachments, and it can be deleted once nothing references it.
    Both are administrator actions and are described in the [Tag schema lifecycle][tag-schema-lifecycle] guide.

## Step 1: Define a tag schema

Tag schemas can be defined using the UI wizard in the `Cluster settings` > `Tag schemas` section.
Tag schemas have a name, the name is used to uniquely identify the schema.
You can also provide an optional description.

You can define a schema by using the UI tool or by providing the schema in JSON format.
If you use the UI tool, you should provide the name of the property in the schema, the type of the property, whether or not the property is required and an optional description.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/tags/tags_schema_simple.png" alt="UI tag schema definition">
    <figcaption>UI tag schema definition</figcaption>
  </figure>
</p>

The UI tool allows you to define simple not-nested schemas.
For more advanced use cases, more complex schemas (e.g., nested schemas) might be required to fully express the content of a given artifact.
In such cases it is possible to provide the schema directly as JSON string.
The JSON should follow the standard [https://json-schema.org](https://json-schema.org).
An example of complex schema is the following:

```json
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

Additionally it is also possible to define a single property as tag.
You can achieve this by defining a JSON schema like the following:

```json
{ "type" : "string" }
```

Where the type is a valid primitive type: `string`, `boolean`, `integer`, `number`.

## Step 2: Attach a tag to an artifact

Once the tag schema has been created, you can attach a tag with that schema to a feature group, feature view, training dataset, model, deployment, job or dataset, either using the APIs or the UI.

### Using the API

You can attach tags to feature groups and feature views by using the `add_tag()` method of the feature store APIs:

=== "Python"

    ```python
    # Retrieve the feature group
    fg = fs.get_feature_group("transactions_4h_aggs_fraud_batch_fg", version=1)

    # Define the tag
    tag = {
        "business_unit": "Fraud",
        "data_owner": "email@hopsworks.ai",
        "pii": True,
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

The same APIs work for feature views, training datasets, models and deployments alike.

#### Jobs

Jobs carry tags through the same three methods, on the `Job` object returned by the job API.

=== "Python"

    ```python
    job_api = project.get_job_api()
    job = job_api.get_job("transactions_ingestion")

    job.add_tag("data_privacy", {"business_unit": "Fraud", "pii": True})
    job.get_tags()
    job.delete_tag("data_privacy")
    ```

A job also has a free-text description, which is indexed for search alongside its tags.

=== "Python"

    ```python
    job.description = "Hourly ingestion of card transactions"
    job.save()
    ```

#### Datasets

Tags are attached to a dataset, which is a top-level directory in the project's file system.
They are reached through the dataset API by path.

=== "Python"

    ```python
    dataset_api = project.get_dataset_api()

    dataset_api.add("Resources", "data_privacy", {"business_unit": "Fraud", "pii": True})
    dataset_api.get_tags("Resources")
    dataset_api.delete("Resources", "data_privacy")
    ```

Tags can also be attached when the dataset is created.

=== "Python"

    ```python
    dataset_api.mkdir(
        "transactions_raw",
        tags=[{"name": "data_privacy", "value": {"business_unit": "Fraud", "pii": True}}],
    )
    ```

!!! warning "Tags on files inside a dataset are frozen"
    Tags could previously be attached to any file or directory inside a dataset.
    Attaching a new tag to a path inside a dataset is now rejected with HTTP 400 and error code 370013, because per-file tags were stored outside the database and could not be searched, counted, or governed.
    Tags that were already attached to such paths remain readable and deletable, and the file browser keeps showing them.
    Attach the tag to the dataset instead.

### Using the UI

You can attach tags to feature groups and feature views directly from the UI.
You can navigate on the artifact page and click on the `Add tags` button.
From there you can select the tag schema of the tag you want to attach and populate the values as shown in the gif below.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/tags/tags_ui.gif" alt="Attach tag to a feature group">
    <figcaption>Attach tag to a feature group</figcaption>
  </figure>
</p>

## When a tag was attached

Every tag attached after the upgrade that introduced this feature records the time it was attached.
`get_tags` returns values only, so the attachment time is exposed through a second pair of methods that keep the tag objects.

=== "Python"

    ```python
    fg = fs.get_feature_group("transactions_4h_aggs_fraud_batch_fg", version=1)

    tags = fg.get_tags_metadata()  # dict[str, Tag]
    for name, t in tags.items():
        print(name, t.value, t.created_on)

    one = fg.get_tag_metadata("data_privacy")
    ```

`get_tag_metadata` and `get_tags_metadata` are available on feature groups, feature views, training datasets, models, deployments and jobs, and on the dataset API as `get_tag_metadata(path, name)` and `get_tags_metadata(path)`.
`created_on` is `None` for tags that were attached before the upgrade, because the attachment time was not recorded then.
The UI shows the same value under the tag name on the artifact page.

## Step 3: Search

Hopsworks indexes the tags attached to feature groups, feature views, training datasets, models, deployments, jobs and datasets.
The tags will then be searchable using the free text search box located at the top of the UI.
For jobs the search also covers the job name and description, and for datasets the dataset name and description.
Model and deployment documents are written by Hopsworks itself, so a tag change on a model or a deployment is reflected in search rather than leaving a stale answer behind.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/tags/search_ui.gif" alt="Search for tags in the feature store">
    <figcaption>Search for tags in the feature store</figcaption>
  </figure>
</p>

Jobs and datasets can also be searched from the Python client.

=== "Python"

    ```python
    search_api = project.get_search_api()

    for job_meta in search_api.jobs("ingestion"):
        print(job_meta.name, job_meta.job_type)
        job = job_meta.get()  # the Job object, resolved in the hit's own project

    for ds_meta in search_api.datasets("transactions"):
        print(ds_meta.name, ds_meta.path)
    ```

Both accept a `tag_filter` and a `global_search` flag, like the feature group search.
Jobs and datasets carry no keywords, so a `keyword_filter` never matches them.
