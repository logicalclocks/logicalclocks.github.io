# Search Index Administration { #search-index-administration }

## Introduction

Hopsworks keeps a search index of the artifacts in a deployment: feature groups, feature views, training datasets, jobs, models and deployments.
The index is updated from the database, not written to directly.
Every change to a searchable property queues a command in the same transaction that made the change, and a background executor applies the queued commands to OpenSearch.

That design is what makes the index eventually consistent rather than immediately correct, and it is the thing to understand before diagnosing a stale search result.
A tag that was attached seconds ago and does not appear in search yet is normal.
A tag that has not appeared after minutes means a command is stuck, which this page covers.

Only administrators can reach any of this.

## Commands needing attention

Go to `Cluster Settings` > `Search Index`.
The page lists every command that has failed at least once, oldest first.

For each it shows the document, the artifact type, the operation, the number of attempts made, when the next attempt is due, the project, and the last error.
When the list is empty, every queued update has been applied.

The reason a stuck command matters more than one failure suggests is ordering.
Commands for a single document are applied in order, so while one keeps failing, every later update to that same document waits behind it, and that artifact's search result stays as it was.
Other documents are unaffected.

Retries are automatic and unbounded, with the delay growing between attempts.
Unbounded is deliberate: abandoning a command would not lose only its own update, it would strand every later update to that document.
So a command in this list is usually a transient failure that will clear itself, and the list is worth acting on when an entry stops making progress.

The page makes that call for you at 20 attempts.
A command that has failed 20 times or more is marked `stuck`, with a red border and a callout explaining what to do.
The threshold is where the retry delay has been at its cap for a while, so crossing it means roughly an hour of the same failure: whatever a retry could outwait has had its chance.
Read the stuck command's error first, because a failure whose cause has since been fixed clears itself on the next retry and needs nothing from you.
Otherwise cancel it, as described below.

### Cancelling a command

Cancel a command only to let the ones behind it through.

The update the cancelled command carried is lost.
The document keeps whatever the index already held, so cancelling an `UPDATE_TAGS` leaves the old tags visible in search until something changes that artifact again and queues a fresh command.
That is why cancelling is an explicit operator action and never something the executor does on its own.

A command can only be cancelled while it is `FAILED`, which is the state between attempts where nothing owns the row.
A command that has just been picked up for another attempt cannot be cancelled, and the request is refused with that reason rather than interrupting the attempt.
Wait for the attempt to finish and retry.

Each cancellation is logged with the command id, the document, the attempt count, the requesting administrator and the last error, because once the row is gone the log is the only record it existed.

## Rebuilding the index

A reindex rebuilds the search index from the database.
It is the recovery path after the index has been lost or has diverged, not routine maintenance.

```bash
# queue a reindex, returns the run id
curl -X POST -H "Authorization: Bearer $JWT" \
  "https://$HOPSWORKS_HOST/hopsworks-api/api/admin/search/featurestore/reindex"

# follow that run
curl -H "Authorization: Bearer $JWT" \
  "https://$HOPSWORKS_HOST/hopsworks-api/api/admin/search/featurestore/reindex/$RUN_ID"
```

The `POST` returns `200` with the run id rather than an empty `204`.
The run id is what makes progress observable: without it a caller can only watch the global command queue, which mixes the reindex with whatever ordinary use is queueing alongside it.

Reindexing queues a command per document, so on a large deployment it takes a while and shows up as a long queue.
That is expected, and ordinary updates continue to be applied while it drains.

## Configuration

Set these in `Cluster Settings` > `Configuration`.

| Variable | Default | Effect |
| --- | --- | --- |
| `cross_project_global_search_enabled` | `true` | Whether a search may return artifacts from projects the caller is not a member of. Set `false` on a multi-tenant deployment to restrict every search to the projects the caller can already access. |
| `command_search_fs_retry_backoff_base_as_ms` | `5000` | The delay before the first retry of a failed command. The delay doubles per attempt from here. |
| `command_search_fs_retry_backoff_max_as_ms` | `300000` | The ceiling on that growing delay, so a long-failing command keeps retrying at a fixed interval rather than drifting to never. |

Lowering the backoff makes a transient failure clear sooner at the cost of more load against OpenSearch while it is failing.
Raising it does the opposite.

!!! warning "Turning off cross-project search does not rewrite history"
    `cross_project_global_search_enabled` filters searches as they are made.
    It does not remove anything from the index, so switching it off restricts what users can find from that point on and is not a way to redact something already indexed.
