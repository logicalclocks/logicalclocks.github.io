# Tags { #tags-guide }

## Introduction

Hopsworks feature store enables users to attach tags to artifacts, such as feature groups, feature views, training datasets, jobs, apps, models or deployments.

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

!!! warning "Immutable"
    Tag schemas are immutable.
    Once defined, a tag schema cannot be edited nor deleted.

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

### Archiving deleted attachments

When you define a schema you can also tick `Archive deleted tags`, or pass `archive=True` through the API.
The flag is a property of the schema rather than of any one attachment, which is why it is set where the schema is defined and applies to every tag attached with it afterwards.

=== "Python"

    ```python
    from hopsworks.core.tag_schemas_api import TagSchemasApi


    schema = {
        "type": "object",
        "properties": {"owner": {"type": "string"}},
        "required": ["owner"],
        "additionalProperties": False,
    }

    # keep attachments of this tag once they are deleted
    TagSchemasApi().create("ownership", schema, archive=True)
    ```

The flag defaults to `False`, which discards an attachment when it is deleted.
Registering a schema requires administrator privileges, as it does without the flag.

!!! note "Records intent, no behaviour yet"
    Setting `archive` today only records the decision on the schema.
    Nothing reads it: copying deleted attachments into an offline feature group for analysis is a later change.
    Set it now on schemas whose history you expect to want, because the flag cannot recover attachments that were already deleted while it was off.

## Step 2: Attach a tag to an artifact

Once the tag schema has been created, you can attach a tag with that schema to a feature group, feature view, training dataset, job, app, model or deployment either using the APIs, or by using the UI.

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

#### Jobs and apps

Jobs and apps carry tags through the same three methods, reached from the job handle rather than the feature store:

=== "Python"

    ```python
    jobs_api = project.get_jobs_api()
    job = jobs_api.get_job("transactions_ingest")

    job.add_tag("data_privacy", {"business_unit": "Fraud", "pii": True})
    job.get_tags()
    job.delete_tag("data_privacy")
    ```

An app is a job whose type is `PYTHON_APP`, so an app is tagged exactly the same way, through the handle its name resolves to.

The CLI covers the same three operations:

```bash
hops job tags transactions_ingest
hops job add-tag transactions_ingest data_privacy --value '{"business_unit": "Fraud", "pii": true}'
hops job remove-tag transactions_ingest data_privacy
```

`--value` takes JSON for a schema with properties, or a plain string for a single-property schema.

Tags on a job are also editable in the UI, on the job's `Tags` section, and when creating or editing the job.
For an app, the equivalent section is on the app overview page.

Deleting a job deletes its tags with it.
They are not restored by creating a new job under the same name, because the tags belong to the job that was deleted and not to its name.

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

Hopsworks records the time each tag was attached and reports it alongside the value.
`get_tags()` returns values only, so read the attachment time through the `_metadata` variants, which return `Tag` objects instead of bare values:

=== "Python"

    ```python
    fg = fs.get_feature_group("transactions_4h_aggs_fraud_batch_fg", version=1)

    tag = fg.get_tag_metadata("data_privacy")
    print(tag.value, tag.created_on)

    # every tag on the artifact, keyed by name
    for name, attached in fg.get_tags_metadata().items():
        print(name, attached.created_on)
    ```

`created_on` is an aware UTC `datetime`, and the same methods exist on feature views, training datasets and jobs.

The timestamp records when the tag was **attached**, not when its value last changed.
Re-attaching a tag to change its value keeps the original attachment time, so the value can be corrected without losing the record of when the artifact was first classified.

`created_on` is `None` when the attachment time is unknown rather than recent.
That happens for tags attached before the cluster recorded attachment times, and for legacy per-file dataset tags, which are stored as HopsFS extended attributes and carry no timestamp.

## Step 3: Search

Hopsworks indexes the tags attached to feature groups, feature views, training datasets, jobs, models and deployments.
The tags are then searchable using the free text search box located at the top of the UI, and can be filtered on directly.
See the [tag and keyword search guide][search-with-tags-and-keywords] for filtering by a specific tag key and value rather than by free text.

Tags on artifacts of every indexed class are searchable, so a governance question such as "which artifacts are missing a data owner" can be answered across feature groups, jobs and deployments in one query.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/tags/search_ui.gif" alt="Search for tags in the feature store">
    <figcaption>Search for tags in the feature store</figcaption>
  </figure>
</p>
