# Search Index Administration { #search-index-administration }

## Introduction

Hopsworks keeps a search index of the artifacts in a deployment: feature groups, feature views, training datasets, data sources, datasets, jobs, models and deployments.
The index is updated from the database, not written to directly.
Every change to a searchable property queues a command in the same transaction that made the change, and a background executor applies the queued commands to OpenSearch.

That design is what makes the index eventually consistent rather than immediately correct, and it is the thing to understand before diagnosing a stale search result.
A tag that was attached seconds ago and does not appear in search yet is normal.
A tag that has not appeared after minutes means a command is stuck, which this page covers.

Only administrators can reach any of this.

## Commands needing attention

Go to `Cluster Settings` > `Service Operations` and open the `OpenSearch Index Commands` tab.
The page opens on the `Service Operations` tab, which carries the platform's operation logs; the index commands share the page because both answer whether the platform is digesting what it was asked to do.

You do not need to check the tab on the off-chance.
While any command needs attention, the `Service Operations` entry in the settings menu shows a pulsing orange dot and the `OpenSearch Index Commands` tab is outlined in orange.
Both appear and clear on their own as the queue fails and drains, so no dot means there is nothing to look at.

Below the `Featurestore search index` card, which reports on the [index rebuild][search-index-rebuild], the tab lists every command that has failed at least once, oldest first.

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

### Cancelling a command { #cancelling-a-command }

Cancel a command only to let the ones behind it through.

The update the cancelled command carried is lost.
The document keeps whatever the index already held, so cancelling an `UPDATE_TAGS` leaves the old tags visible in search until something changes that artifact again and queues a fresh command.
That is why cancelling is an explicit operator action and never something the executor does on its own.

A command can only be cancelled while it is `FAILED`, which is the state between attempts where nothing owns the row.
A command that has just been picked up for another attempt cannot be cancelled, and the request is refused with that reason rather than interrupting the attempt.
Wait for the attempt to finish and retry.

Each cancellation is logged with the command id, the document, the attempt count, the requesting administrator and the last error, because once the row is gone the log is the only record it existed.

## Rebuilding the index { #search-index-rebuild }

A reindex rebuilds the search index from the database.
It is the recovery path after the index has been lost or has diverged, not routine maintenance.

The `Featurestore search index` card at the top of the `OpenSearch Index Commands` tab shows the latest run: its state, how many of its commands are pending, failed and cancelled, and `rebuilt` once every command has been applied.
Its `Reindex now` button requests a run.
The same is available through the REST API:

```bash
# queue a reindex, returns the run id
curl -X POST -H "Authorization: Bearer $JWT" \
  "https://$HOPSWORKS_HOST/hopsworks-api/api/admin/search/featurestore/reindex"

# queue the data sources and datasets only, into the index as it is
curl -X POST -H "Authorization: Bearer $JWT" \
  "https://$HOPSWORKS_HOST/hopsworks-api/api/admin/search/featurestore/reindex?scope=ADDITIVE"

# follow that run
curl -H "Authorization: Bearer $JWT" \
  "https://$HOPSWORKS_HOST/hopsworks-api/api/admin/search/featurestore/reindex/$RUN_ID"
```

A run without `scope`, or with `scope=ALL`, empties the index and queues commands for every artifact; `Reindex now` requests this one.
A run with `scope=ADDITIVE` leaves the index as it is and queues commands for the data sources and datasets only, so the rest of search keeps answering while it runs.
The 5.3 post-upgrade hook requests that one: data sources are the only class 5.3 adds, and datasets, added in 5.2, may be missing from the index of a cluster upgraded from 5.1.
If an `ADDITIVE` run ends early, request another `ADDITIVE` run rather than pressing `Reindex now`, which would empty the index.
The run's description, in the answer to the `POST` and to both `GET`s, carries its `scope`.

The `POST` returns `202` with the run id, and `409` while another run is in progress or still applying its commands.
A `POST` with a `key` returns `200` with the run already queued under that key, and `400` when that run has another scope.
The run id is what makes progress observable: without it a caller can only watch the global command queue, which mixes the reindex with whatever ordinary use is queueing alongside it.
The run has finished when its `state` is `QUEUED`, meaning every command is in the queue, and its `pending` count is `0`.
It rebuilt the index only if its `cancelled` count is also `0`.
Otherwise the card shows `applied, with cancelled commands`: the documents those commands carried kept what the index already held, as with any [cancelled command][cancelling-a-command].
Once the cause of their failures is fixed, request another run to rebuild them.

Reindexing queues commands for every document, so on a large deployment it takes a while and shows up as a long queue.
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
