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

### Archiving a tag for analytics

Most tags are only ever read as they are now: who owns this feature group, whether it holds PII.
Some are interesting over time, and for those the current value is the least useful part.
Marking a schema as archived says that attachments of this tag are worth keeping once they stop being current, so the tag's history can be analysed and not just its present state.

Tick `Archive deleted tags` when defining the schema, or pass `archive=True` through the API:

=== "Python"

    ```python
    from hopsworks.core.tag_schemas_api import TagSchemasApi


    schema = {
        "type": "object",
        "properties": {"state": {"type": "string"}},
        "required": ["state"],
        "additionalProperties": False,
    }

    TagSchemasApi().create("asset_lifecycle", schema, archive=True)
    ```

The flag is a property of the schema rather than of any one attachment, which is why it is set where the schema is defined and applies to every tag attached with it afterwards.
It defaults to `False`, which discards an attachment once it stops being current.
Registering a schema requires administrator privileges, as it does without the flag.

#### What it is for

Take an `asset_lifecycle` tag whose `state` is `dev`, `qa` or `prod`.
Every artifact carries it, and the value moves forward as the artifact is promoted.

Read as an ordinary tag it answers one question, which is where an artifact is now.
The questions worth asking are about the pipeline rather than the artifact: how long does something sit in `qa` before it reaches `prod`, is that getting slower, whose artifacts stall.

Those become answerable once the tag's history is kept as one record per value, each with the time that value became current.
The analysis is then a group-by over the artifact: order its `dev`, `qa` and `prod` records by time, and the gaps between them are how long it spent in each stage.
Aggregated across every artifact, that gives the promotion times for the deployment as a whole and how they are moving.

Without archiving, promoting an artifact to `prod` discards the record that it was ever in `qa`, and the question stops being answerable at all.
So the flag is worth setting on a tag whose values are states an artifact passes through, rather than facts about it.

This history is not the same thing as the [attachment time][when-a-tag-was-attached] on the live tag.
That timestamp deliberately stays at the first attachment when a value is corrected, so it records when an artifact was first classified and not when it entered its current state.
The per-value history is what the archive is for.

!!! note "Records intent, no behaviour yet"
    Setting `archive` today only records the decision on the schema.
    Nothing reads it: copying the retained attachments into an offline feature group, where they can be queried as above, is a later change.
    Set it now on the schemas whose history you expect to want, because the flag cannot recover attachments that were already discarded while it was off.

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

## Archive tag history

By default a tag records only its current value: reading it tells you where an artifact is now, not
where it has been. Turning on **Archive tag history** for a schema makes Hopsworks additionally
record every change to that tag's values, so you can ask how long an artifact spent in each state.

The flag is set per schema, in `Cluster settings` > `Tag schemas`, when the schema is created. To
turn it on or off for a schema that already exists, a cluster administrator calls
`PUT /hopsworks-api/api/tags/{name}/archive?value=true`. It applies to every artifact the tag is
attached to: feature groups, feature views, training datasets, jobs, models and deployments.

Turning it off ends every interval the tag still has open, at the moment you turn it off, and keeps
everything already recorded. The recorded rows stay because they are still true; the open intervals
have to be ended because nothing would ever end them once recording stops, and the last value of
every artifact would otherwise read as current forever. Turning it back on starts a fresh interval
at that moment rather than pretending the gap was observed.

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
SELECT e.artifact_type, e.artifact_id, e.tag_name, e.tag_key, e.tag_value,
       e.added_on, e.removed_at
FROM (
  SELECT artifact_type, artifact_id, tag_name, tag_key, tag_value, event_type,
         event_time AS added_on,
         LEAD(event_time) OVER (
           PARTITION BY artifact_type, artifact_id, tag_name, tag_key
           ORDER BY event_time,
                    CASE WHEN event_type = 'CLOSED' THEN 0 ELSE 1 END,
                    id
         ) AS removed_at
  FROM   hopsworks.tag_history
) e
WHERE e.event_type = 'OPENED'
```

Two details in that query are easy to get wrong and produce numbers that look reasonable:

- The `OPENED` filter has to be in the outer query. SQL applies `WHERE` before window functions, so
  filtering inside would hide every `CLOSED` row from `LEAD`, and anything that ended without a
  successor, a detached tag or a deleted artifact, would report as still current with its duration
  growing forever.
- The ordering has to put `CLOSED` before `OPENED` at the same timestamp. Both halves of a value
  change share one `event_time` by design, so the ordering needs a tie-break, and `id` is not one:
  rows are not written in the order the two halves were built.

A `removed_at` of `NULL` means the artifact is still in that state. An `added_on` of `NULL` means the
tag was attached before Hopsworks began recording attachment times, so the start is unknown; it is
left empty rather than filled with a guess.

The history outlives what it describes. Deleting the artifact, the tag schema or the project closes
the open intervals and keeps the rows, so a report over a past quarter still returns what was true
then.

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
