# Tag Schema Lifecycle

## Introduction

A tag schema is defined once and then attached to artifacts across every project on the cluster, as described in the [Tags](tags.md) guide.
This guide covers what an administrator can do with a schema afterwards: retire it so that nothing new uses it, and remove it once nothing does.

The JSON definition of a schema cannot be changed after it is created.
The values already attached were validated against the original definition, and editing it would leave those values unvalidated.
Create a new schema instead, deprecate the old one, and migrate at your own pace.

Deprecating, restoring and deleting a schema are administrator actions, performed in the `Cluster settings` > `Tag schemas` section or through the REST API.
Attaching and detaching tag values stays with the project members.

## Deprecate a schema

Deprecation stops a schema from being attached to anything new while leaving everything already attached untouched.
Use it when a schema is being replaced and you want existing owners to migrate off it without breaking their pipelines.

| Operation on a deprecated schema | Allowed |
| --- | --- |
| Read the schema, list schemas, read attached values | Yes |
| Attach it to an artifact that does not have it | No, rejected with HTTP 400 and error code 370011 |
| Update the value already attached to an artifact | Yes, so a team can correct data while migrating off |
| Detach it from an artifact | Yes |
| Register it as a mandatory tag | No, because a mandatory tag that nobody may attach cannot be satisfied |
| Delete the schema | Yes, under the rules below |
| Restore it | Yes |

A schema that is currently registered as a [mandatory tag](mandatory_tags.md) cannot be deprecated.
The request is rejected with HTTP 409 and error code 370012.
Remove the mandatory registrations first, then deprecate.

In the UI, deprecated schemas carry a muted `Deprecated` badge with the date, and the schema detail drawer shows which administrator deprecated it.
The tag picker on an artifact page no longer offers them, while a deprecated tag that is already attached still renders so it can be edited or removed.

=== "Python"

    ```python
    import hopsworks
    from hopsworks_common.core.tag_schemas_api import TagSchemasApi


    hopsworks.login()
    tag_schemas = TagSchemasApi()

    tag_schemas.deprecate("data_privacy_v1")

    # Existing attachments keep working; new ones are refused.
    schema = tag_schemas.get("data_privacy_v1")
    print(schema["deprecated"], schema["deprecatedOn"], schema["deprecatedBy"])
    ```

## Restore a schema

Restoring clears the deprecation and the record of who set it and when.
Those three fields describe the current state rather than a history, so a restored schema looks like one that was never deprecated.
The audit log remains the record of the full sequence of actions.

=== "Python"

    ```python
    tag_schemas.restore("data_privacy_v1")
    ```

## Check what uses a schema

Before deleting a schema, ask what still references it.

=== "Python"

    ```python
    usage = tag_schemas.usage("data_privacy_v1")

    print(usage["attachmentCount"])            # values attached across all projects
    print(usage["mandatoryRegistrationCount"])  # mandatory registrations
    print(usage["deletable"])                   # both counts are zero
    for ref in usage.get("references", []):
        print(ref["kind"], ref["projectName"], ref["artifactName"], ref["version"])
    ```

`references` lists the artifacts holding a value, up to a limit.
Above that limit the list is omitted and `truncated` is `true`, leaving `attachmentCount` as the answer.

`complete` is always `false`.
Tags attached to individual files inside a dataset before per-file tags were frozen live in the file system rather than the database, and no query can enumerate them without walking the file system.
The counts therefore cover database-backed references only.
This is why the UI wording is "No database-backed references found" rather than "not used".

## Delete a schema

A schema can be deleted once nothing references it.
The request is refused with HTTP 409 and error code 370010 while any value is attached or any mandatory registration exists, and the error names what to detach.

The check and the deletion run in one transaction against the database, and foreign keys refuse the deletion even if a value is attached between the check and the commit.
The dialog in the UI is advisory; the database is authoritative, so a delete that looked safe a moment earlier can still be refused.

=== "Python"

    ```python
    usage = tag_schemas.usage("data_privacy_v1")
    if usage["deletable"]:
        tag_schemas.delete("data_privacy_v1")
    ```

### Force delete

`force=True` deletes the schema together with every value attached to it, in a single transaction, and queues the affected artifacts for reindexing so that search stops returning the deleted tag.
It is exposed on the REST API and in the Python client, and deliberately not in the UI.

=== "Python"

    ```python
    tag_schemas.delete("data_privacy_v1", force=True)
    ```

Above a threshold of attached values, configured cluster-wide and defaulting to 5000, a force delete is refused with HTTP 409 rather than started.
The error states the count and names the reindex endpoint.
A partial delete that leaves stale values in the search index is worse than a refusal, and reindexing that many documents is an operation an administrator should schedule.

### Deleting against an older backend

A plain `delete` against a Hopsworks version older than the one described here is refused by the client rather than sent.
That backend ignores the unknown `force` parameter and deletes every attached value for any delete call, so the safest-looking call would get the most destructive behaviour the old server has.
The client detects it through the usage endpoint, which shipped in the same release as the refusal, and raises a `RuntimeError` naming `force=True` as the way to proceed deliberately.

## Command line

The same two lifecycle actions are available in the CLI.

```bash
hops tags deprecate data_privacy_v1
hops tags restore data_privacy_v1
```
