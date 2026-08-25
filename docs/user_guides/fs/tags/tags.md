# Tags

## Introduction

Hopsworks feature store enables users to attach tags to artifacts, such as feature groups, feature views, training datasets, models or deployments.

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

## Step 2: Attach a tag to an artifact

Once the tag schema has been created, you can attach a tag with that schema to a feature group, feature view, training dataset, model or deployment either using the APIs, or by using the UI.

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

## Step 3: Archive tag history

By default a tag records only its current value: reading it tells you where an artifact is now, not
where it has been. Turning on **Archive tag history** for a schema makes Hopsworks additionally
record every change to that tag's values, so you can ask how long an artifact spent in each state.

The flag is set per schema, in `Cluster settings` > `Tag schemas`, either when the schema is created
or afterwards. It applies to every artifact the tag is attached to: feature groups, feature views,
training datasets, jobs, models and deployments.

Two things are worth knowing before you turn it on:

- **History starts when you turn it on.** Changes made before that are not recoverable, because the
  live tag keeps only its current value. Attachments that already exist are backfilled with the
  state they are in, timed from when they were attached.
- **Turning it off stops recording but keeps what was recorded.** The rows already written are still
  true, and the tag is still attached, so nothing is deleted.

History is recorded per key of the schema, not per tag. Changing one key of a multi-key tag records
a change to that key alone and leaves the others untouched, so a correction to one field does not
make every other field look like it changed at the same moment.

### Reading the history

The history is stored in the `tag_history` table of the Hopsworks metadata database, one row per
transition: the value became current, or it stopped being current. A value change writes both at the
same instant, so one interval's end is the next one's start.

It is read with SQL rather than through the tag APIs, which continue to return the current value.
On a cluster with the `hopsworks_analytics` project enabled, its Superset connection can query the
table directly, and
`create_tag_history_dashboard.py` in the `okr-dashboards` repository builds a "Tag Lifecycle"
dashboard over it: time spent in each state, whether that is increasing, what is in each state now,
and what has been in one state longest.

The table stores events rather than intervals. To get `added_on` and `removed_at`, take the next
event's time for the same artifact, tag and key:

```sql
SELECT artifact_type, artifact_id, tag_name, tag_key, tag_value,
       event_time AS added_on,
       LEAD(event_time) OVER (
         PARTITION BY artifact_type, artifact_id, tag_name, tag_key
         ORDER BY event_time, id
       ) AS removed_at
FROM   hopsworks.tag_history
WHERE  event_type = 'OPENED'
```

A `removed_at` of `NULL` means the artifact is still in that state. An `added_on` of `NULL` means the
tag was attached before Hopsworks began recording attachment times, so the start is unknown; it is
left empty rather than filled with a guess.

The history outlives what it describes. Deleting the artifact, the tag schema or the project closes
the open intervals and keeps the rows, so a report over a past quarter still returns what was true
then.

## Step 4: Search

Hopsworks indexes the tags attached to feature groups, feature views and training datasets.
The tags will then be searchable using the free text search box located at the top of the UI.
Tags attached to models and deployments are stored and retrievable through the APIs and the UI, but they are not indexed for free text search.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/tags/search_ui.gif" alt="Search for tags in the feature store">
    <figcaption>Search for tags in the feature store</figcaption>
  </figure>
</p>
