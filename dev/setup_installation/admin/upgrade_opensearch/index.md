# Upgrading OpenSearch { #upgrading-opensearch }

## Introduction

Each Hopsworks release ships a fixed OpenSearch version, and upgrading Hopsworks upgrades it.

| Hopsworks | OpenSearch |
| --------- | ---------- |
| 4.8.x, 5.0.x | 1.3.x |
| 5.1.x | 2.19.x |
| 5.2.x | 3.8.0 |

This page covers what changes for you on the 5.1 to 5.2 upgrade, because that is the one that can interrupt service, and the steps to run it.
Upgrade a 5.1.x cluster to 5.2.1 or later, which this page describes.
5.2.0 still ships the earlier index pass, which refuses every client for the whole pass, fails on an index whose mapping is empty, deletes `.opendistro_security` and with it the roles of restricted grants and shares, and does not check for nmslib fields.
The commands assume Hopsworks is installed in the `hopsworks` namespace.

## Upgrade one minor release at a time

Upgrade 5.0.x to 5.1.x, let it come up, then upgrade to 5.2.x.
Going from 5.0.x straight to 5.2.x is not supported.

OpenSearch 3.x refuses to start if the cluster still holds an index that was created before OpenSearch 2.0.
OpenSearch 2.19 keeps serving indices created by 1.x without rewriting them, so a cluster that has passed through 5.1.x can still hold such indices.
When a 3.x node meets one it stops during startup, so the first pod of the rolling upgrade never becomes ready, and only the OpenSearch log says why.

## The index pass on 5.1.x to 5.2.x

A `pre-upgrade` hook runs before the OpenSearch StatefulSet is touched, so OpenSearch is still on 2.19 if it fails.
It checks every index against the OpenSearch 2.0 floor.
A cluster that has only ever held indices created by 2.x has no pre-2.0 index to fix, but the hook still runs the check in [Vector fields that would stay on nmslib][opensearch-nmslib-fields], and moves embedding indices that still use nmslib to faiss.

On a cluster installed before 5.1 the hook repairs what it finds:

- It deletes only the indices the platform recreates or expires by itself: logs, audit logs, `pypi_libraries_*`, `.tasks`, and plugin indices that the plugin repopulates.
- It copies everything else and keeps its name, including `featurestore`, `projects`, the OpenSearch Dashboards saved objects, the index state management policies, the embedding indices behind similarity search, and `.opendistro_security`, which holds the roles and mappings that Hopsworks creates for restricted grants and feature group shares.
  Nothing else is deleted, because anything the hook does not recognise might hold data nothing can rebuild.

From 5.1.2 you can run the same pass on 5.1.x first, in a window you choose and with vector ingestion off, as described in [Copying the indices on 5.1.x first][opensearch-copy-on-51].
The hook then finds nothing left to copy.

### What keeps working { #opensearch-what-keeps-working }

The hook copies one index at a time and blocks writes only on the index it is copying.
Reads keep working on every index, apart from the moment each index is swapped for its copy: a read then gets HTTP 404 while the name is missing, or 503 while the new index's shards start.
Writes to every other index keep working.
A write to the index being copied is refused with HTTP 403 until its copy is done, which takes about a second for a small index and minutes for a large one.

- OnlineFS retries a vector write that the block refuses for about a minute, then marks the row failed.
  The hook warns for each embedding index that it expects to stay blocked for more than about 45 seconds.
  To keep those rows, [copy the indices on 5.1.x first][opensearch-copy-on-51] with vector ingestion off, or turn it off around the upgrade, as in the [upgrade steps][opensearch-upgrade-steps].
- Log lines that logstash ships to a log index while it is blocked may be missing.
- A grant, a revoke or a feature group share fails while the hook copies `.opendistro_security`, which it copies last, and changes nothing.
  Repeat it after the upgrade.
  Users already logged in keep working meanwhile.
- A write that reaches an index's name in the moment between its delete and its clone creates a new index under that name, and the hook stops, as described in [If the hook fails][opensearch-hook-fails].

### How an index is copied

For each index, the hook:

1. Creates a copy named `osupg-<8 hex digits>` from the index's settings and mappings, and records in the copy's mapping `_meta` which index it copies and how far it got.
2. Blocks writes and mapping updates on the index.
   Reads keep working.
3. Reindexes the index into the copy and compares the document counts.
4. Gives the copy the index's replicas and blocks writes on it.
5. Deletes the index and clones the copy back under its name, with its aliases, replicas and ingest pipelines.
6. Checks the clone, lifts its block, and deletes the copy.

The hook pauses Index State Management while it runs.
A cloned index has a new UUID, so an ISM policy attached to the index has to be attached again.

If the hook is stopped, for example by a node loss, the next run picks up from what the copies record.
A copy that was not complete is dropped, and its index is unblocked and copied again.
A complete copy is cloned back.
A hook stopped by its deadline also tries to drop an incomplete copy and unblock its index before it exits, and leaves both to the next run if it cannot.

### Set the timeout { #opensearch-set-the-timeout }

The hook is bounded by `olk.opensearch.indexUpgrade.activeDeadlineSeconds`, which defaults to 3600 seconds.
Pass `helm upgrade --timeout` at least that long, or Helm gives up on the hook before the hook finishes.

The time grows with the size of your old indices, `featurestore` and the embedding indices in particular.
As a guide, a copy ran at roughly 15 MB per second on a 16-CPU node, and slower disks or fewer CPUs take longer.
Before it starts, the hook prints the size of every index it will copy, how long each one is expected to stay blocked, the total, and the configured deadline, and warns when the total exceeds the deadline.
To read that report without changing anything, set `olk.opensearch.indexUpgrade.mode` to `report`.
The hook then lists the indices and fails, apart from finishing an index that an interrupted earlier run left half done, and you can raise the deadline and the timeout before running the real upgrade.
A cluster with nothing to copy or delete gets no report: the hook prints `Nothing to do` and the upgrade goes ahead.
Once it copies, the hook logs how long writes to each index were actually refused.

Free disk space matters as well, because a copy needs room for a second complete copy of the largest index.
The hook checks this on the smallest data node and stops if there is not enough.

## Embedding indices move to faiss

OpenSearch indexes embeddings with an engine, and Hopsworks 5.1 and later create embedding indices on faiss.
Indices created by Hopsworks 5.0 and earlier use nmslib, which OpenSearch has deprecated and which does not accept the filter that the Hopsworks 5.1 and later clients send with every similarity search.

The index pass therefore recreates each embedding index on faiss while it copies it, so similarity search with filters works once the upgrade to 5.2 is done.
Until then, on 5.1, filtered search fails on feature groups whose embedding index was created on 5.0, as described in the upgrade steps below.
Approximate nearest neighbor results can shift slightly, because the graph is rebuilt on a different engine.
On every other copied index, a vector field without an explicit engine comes back on faiss too, because 1.x defaulted it to nmslib and the copy is created on 2.19, which gives it faiss.
Every other vector field keeps its engine, and one that would stay on nmslib stops the hook before it changes anything, as the next section describes.

## Vector fields that would stay on nmslib { #opensearch-nmslib-fields }

The nmslib library in OpenSearch 3.8 is built for CPUs with AVX-512, and a node whose CPU lacks it crashes when it loads the library: at startup, or at the first similarity search that reaches it.
Intel Core processors from the 12th generation on, and AMD Zen 3 and older, such as EPYC Milan, lack AVX-512.

So before it changes anything, the hook reads every index mapping and index template, and stops if a vector field would still be served by nmslib once it is done:

- A field with `method.engine: nmslib`, except on the embedding indices that the hook moves to faiss (spaces `l2`, `cosinesimil` and `innerproduct`).
- Any `l1` or `linf` field, because only nmslib supports these spaces in 3.x.
- A field without an engine on an index that the hook does not copy and that was created before OpenSearch 2.19, because OpenSearch gave such a field nmslib before 2.18, and in some modes on 2.18, and segments keep the engine they were written with.
- An index template, legacy, composable or component, that would create such a field, whether an index uses it or not.

A model-based field passes, because k-NN trains only methods that need training, and nmslib has none.
A field whose engine the hook cannot establish, for example because its index's creation version cannot be read, stops it too.
The check has no override and does not look at the CPU, because a pod can be rescheduled onto another node.
The hook runs the same check again after the copies, so a mapping or template change made meanwhile that puts a field on nmslib stops it.
A satellite runs its own hook and checks its own fields.

The hook log lists each index or template, field, space type and remedy:

- `l2`, `cosinesimil` or `innerproduct`: rebuild the index with `method.engine: faiss`, as in [To reindex by hand][opensearch-reindex-by-hand].
- `l1` or `linf`: no engine other than nmslib supports them in 3.x, so the application has to use another space type, or the index or template has to be deleted.
- A template with another space type: set `method.engine: faiss` on the field, or delete the template.

## Security configuration

At every pod start OpenSearch applies the security configuration that ships with the chart, once every node runs the same version (see below), and so does `run_security_admin.sh` when an operator runs it.
From 5.1.2 on the 5.1 line, and from 5.2.1, this no longer replaces the roles and role mappings.
The chart's own entries are created or updated one by one, and the `fls_` roles and mappings that Hopsworks creates for restricted grants and feature group shares stay.
Up to 5.1.1, every restricted project member could read every field of the project's embedding indices, and every OpenSearch pod start removed the `fls_` roles, so a shared project got HTTP 403.
On 5.1.0 and 5.1.1, the OpenSearch roles and mappings behind grants and shares made before the last OpenSearch restart are gone, while Hopsworks still records the grant or share.
Granting or sharing again is therefore refused: revoke and grant again, or unshare and share again.
The other configuration types are still applied from the chart's files.

- A restricted project member without a grant gets HTTP 403 on the project's embedding indices.
  Read access comes only from a grant or a share, limited to the granted features.
- At pod start nothing is applied until every OpenSearch node has joined and runs the same version, so the last pod of a rolling upgrade, or the last to start, applies it.
  A pod started while another is down logs a warning and skips it, and a skip is not retried before the next pod start.
  On the upgrade to 5.1.2 or 5.2.1 this step is what takes away the restricted members' read access, so check after the roll that one pod applied it:

    ```bash
    for p in $(kubectl get pods -n hopsworks -l app=opensearch -o name); do
      kubectl logs -n hopsworks "$p" -c opensearch \
        | grep -E 'Security configuration applied|Not applying the security configuration'
    done
    ```

    If no pod logged `Security configuration applied`, apply it by hand once every OpenSearch pod is Ready on the same version:

    ```bash
    kubectl exec -n hopsworks opensearch-0 -c opensearch -- \
      bash /usr/share/opensearch/plugins/opensearch-security/tools/run_security_admin.sh
    ```

    `run_security_admin.sh` does not check the versions itself, so run it only when every OpenSearch pod is up on the same version.
    Pushed one type at a time, the configuration is no longer refused by nodes on another version, so a run on a mixed cluster rewrites it under the nodes still on the old version.

- A role or mapping that a later chart removes stays on a running cluster until you delete it by name, because entries are no longer replaced as a whole.

## Snapshot repositories on S3-compatible stores

When OpenSearch 3.x deletes objects from a snapshot repository, it sends a CRC32 checksum where 2.x sent `Content-MD5`.
MinIO before `RELEASE.2025-01-20T14-49-07Z`, and other S3-compatible stores that require `Content-MD5`, reject that, so repository verification fails with `Missing required header for this request: Content-Md5` and the `create-repos` Job fails the upgrade.
The chart already sets `legacy_md5_checksum_calculation: true` on the repositories it generates for the bundled MinIO.
For a repository you configure yourself on such a store, set it in the repository's `s3` block, under `olk.opensearch.backup.repositories` and under `olk.opensearch.restore.repositories`:

```yaml
olk:
  opensearch:
    backup:
      repositories:
        default:
          s3:
            legacy_md5_checksum_calculation: true
```

AWS S3 does not need it.

## Satellite clusters

A satellite cluster runs its own OpenSearch and gets its own index pass when it upgrades to 5.2.
Its write blocks are confined to that satellite's OpenSearch, and `activeDeadlineSeconds` is set per release, so a satellite holding large embedding indices sets its own value and its own `--timeout`.

Upgrade every satellite to 5.1.x before the central cluster moves to 5.2.x, because a satellite still on OpenSearch 1.3 would be two major versions behind a 5.2.x central cluster.
Then upgrade every satellite to 5.2.x before the central cluster, because a satellite's Kafka has to move to KRaft before the central upgrade converts the Strimzi resources.
Hopsworks clients on OpenSearch 2.19 against a satellite's OpenSearch 3.8 were verified.

To copy a satellite's indices on 5.1.x first, upgrade the satellite's release as described in the next section, since each release runs its own Job.

## Copying the indices on 5.1.x first { #opensearch-copy-on-51 }

From 5.1.2, the index pass can also run as a Job of a 5.1.x upgrade, in a window you choose and with vector ingestion off, so no row written to a feature group with embeddings is marked failed.
The Job copies like the hook, one index at a time, and deletes nothing: the logs and the other indices that the platform recreates are left to the 5.2 hook, which then has nothing left to copy.

The Job is a Helm `post-upgrade` hook, so it runs once the rest of the upgrade is in place.
Vector ingestion is turned off in an upgrade of its own before the Job runs, so that no OnlineFS pod still writes vectors to an embedding index while that index is blocked.

1. Check Kafka retention.
    Rows written to feature groups with embeddings wait in Kafka while vector ingestion is off.
    The effective retention of the OnlineFS topics, in time and in bytes, has to cover the run plus the catch-up afterwards, and the default is 168 hours.
2. Get the report: upgrade to 5.1.2 or later with `olk.opensearch.indexUpgrade.mode` set to `report`.
    The Job lists the indices, their sizes and how long each one stays blocked, and fails without changing anything, apart from finishing an index that an interrupted earlier run left half done.
    A cluster with nothing to copy gets no report: the Job prints `Nothing to copy` and succeeds.
    Raise `olk.opensearch.indexUpgrade.activeDeadlineSeconds` above the estimate if needed.
    Pass `mode` with `--set`, not in your values file: 5.2.1 and later read the same key, and a stored `report` makes their hook report and fail.
3. Turn vector ingestion off, and wait for OnlineFS to roll:

    ```bash
    helm upgrade hopsworks hopsworks/hopsworks -n hopsworks --version <5.1.2 or later> -f <your values> \
      --set onlinefs.deployment.vectordb.enabled=false
    kubectl rollout status deployment/onlinefs-deployment -n hopsworks
    kubectl get pods -n hopsworks -l app=onlinefs
    ```

    Go on once the rollout is complete and no older or terminating OnlineFS pod is listed, because an old pod keeps writing vectors until it is gone.
4. Run it with vector ingestion still off:

    ```bash
    helm upgrade hopsworks hopsworks/hopsworks -n hopsworks --version <the same 5.1.x> -f <your values> \
      --set olk.opensearch.indexUpgrade.mode=copy \
      --set onlinefs.deployment.vectordb.enabled=false \
      --timeout <longer than activeDeadlineSeconds>
    ```

    Helm waits for the Job, so the upgrade succeeds or fails with it.
    With ArgoCD, set `global._hopsworks.mode` to `upgrade`, because the Job renders only on an upgrade.
5. Turn vector ingestion back on in the next upgrade, with the same chart version:

    ```bash
    helm upgrade hopsworks hopsworks/hopsworks -n hopsworks --version <the same 5.1.x> -f <your values> \
      --set onlinefs.deployment.vectordb.enabled=true
    ```

    OnlineFS then writes the rows that waited in Kafka.
6. Take a new snapshot after the 5.2 upgrade, not now: a snapshot taken on 5.1.x still holds the logs and other pre-2.0 indices that the Job leaves to the 5.2 hook, and a 3.x cluster cannot restore them.

While the Job runs, reads and writes behave as described in [What keeps working][opensearch-what-keeps-working], with vector ingestion off.

- Do not restart OpenSearch, because a node that starts while `.opendistro_security` is swapped for its copy creates that index again from the chart's files.
- Do not run `run_security_admin.sh`, because it writes the security configuration that the Job may be copying.
- Do not change mappings or index templates, because a mapping update on the index being copied is refused, and the Job stops if a change puts a field on nmslib.
- The Job refuses nmslib fields that it would not convert, as the hook does, including those on log indices that the 5.2 hook would delete, because it deletes nothing itself.

If Helm times out, the Job can still be running.
Check `kubectl get jobs -n hopsworks -l component=opensearch-index-upgrade` before you retry or turn vector ingestion back on.
Do not roll back, because a rollback turns vector ingestion back on while the Job may still be copying an embedding index.
A rerun finishes what a stopped run left.

## Upgrade steps { #opensearch-upgrade-steps }

1. Take a snapshot and check that it completed, because the index pass rewrites indices in place.
2. Upgrade to 5.1.x if you are not already on it, and confirm that OpenSearch 2.19 is live and green:

    ```bash
    kubectl exec -n hopsworks opensearch-0 -c opensearch -- bash -c \
      'curl -sk -u "admin:$ADMIN_PASSWORD" https://localhost:9200/_cat/nodes?h=name,version'
    kubectl exec -n hopsworks opensearch-0 -c opensearch -- bash -c \
      'curl -sk -u "admin:$ADMIN_PASSWORD" https://localhost:9200/_cluster/health?pretty | grep status'
    ```

    Read the node versions, because on 5.1.x the root endpoint reports version `7.10.2` for client compatibility.
    The indices are still the ones 1.x created at this point.
    That is expected, since 2.19 does not rewrite them.

    Two known issues apply to this upgrade:

    - On the first OpenSearch 2.19 start of each cluster, central or satellite, vector writes are rejected for about two minutes and the vectors that had not been flushed are lost.
      The chart fixes this on the 5.1 line, and a values file that copied the old `knn.circuit_breaker` settings (`triggered: true` or `percent: 0.75`) keeps the problem.
      So does `helm upgrade --reuse-values` from a chart that rendered them: set the two values explicitly, or upgrade with `--reset-then-reuse-values`.
    - On 5.1, similarity search with a filter fails on feature groups whose embedding index was created on 5.0, because the 5.1 client sends the filter inside the nearest-neighbor query and the nmslib engine rejects it.
      A client fix and the index pass both resolve it.
3. Optionally, copy the indices on 5.1.x now, as described in [Copying the indices on 5.1.x first][opensearch-copy-on-51].
    The hook in step 6 then finds nothing left to copy, and you can skip steps 4 and 5.
4. Get the report: run the upgrade to 5.2.x with `--set olk.opensearch.indexUpgrade.mode=report`, as described in [Set the timeout][opensearch-set-the-timeout], and raise `olk.opensearch.indexUpgrade.activeDeadlineSeconds` above the estimate if needed.
    Leave it out of the real upgrade, because with `report` the hook fails after the report.
    With nothing to copy or delete the hook prints `Nothing to do` instead and succeeds, so that upgrade goes ahead: continue at step 7.
5. If the report warns that an embedding index stays blocked for long, turn vector ingestion off first, on your current 5.1.x:

    ```bash
    helm upgrade hopsworks hopsworks/hopsworks -n hopsworks --version <current 5.1.x> -f <your values> \
      --set onlinefs.deployment.vectordb.enabled=false
    kubectl rollout status deployment/onlinefs-deployment -n hopsworks
    kubectl get pods -n hopsworks -l app=onlinefs
    ```

    Wait until the rollout is complete and no older or terminating OnlineFS pod is listed, because an old pod keeps writing vectors until it is gone.
    Keep `--set onlinefs.deployment.vectordb.enabled=false` on the upgrade to 5.2.x in the next step.
    The rows written meanwhile stay in Kafka, as long as the topic still holds them, and are written to OpenSearch once ingestion is back on.
6. Upgrade to 5.2.x with a `--timeout` at least as long as `olk.opensearch.indexUpgrade.activeDeadlineSeconds`, and watch the hook:

    ```bash
    kubectl logs -n hopsworks -l component=opensearch-index-upgrade -f
    ```

    It ends with `Every index is now on OpenSearch 2.0 or later. Safe to upgrade.`, or with `Nothing to do` when no index needed it.
7. Verify the upgrade:

    ```bash
    kubectl get pods -n hopsworks -l app=opensearch
    kubectl logs -n hopsworks opensearch-0 -c opensearch | grep -c StartupException
    kubectl exec -n hopsworks opensearch-0 -c opensearch -- bash -c \
      'curl -sk -u "admin:$ADMIN_PASSWORD" https://localhost:9200 | grep -E "number|minimum_index"'
    ```

    The `StartupException` count must be 0.
    Expect version `3.8.0`, `minimum_index_compatibility_version` `2.0.0` and green cluster health.
    Then run a search in the Hopsworks UI and a similarity search on a feature group with an embedding.
8. If you turned vector ingestion off, turn it back on with a `helm upgrade` on 5.2.x and `--set onlinefs.deployment.vectordb.enabled=true`, and OnlineFS writes the rows that waited in Kafka.
    Otherwise, insert again the rows that OnlineFS marked failed while an embedding index was blocked.
9. Take a new snapshot once those rows are written, because a snapshot taken before the upgrade holds the pre-2.0 indices, which a 3.x cluster cannot restore.

## If the hook fails { #opensearch-hook-fails }

The upgrade stops before the OpenSearch StatefulSet is touched, so the cluster is still on 5.1.x.
The hook log names the index and the reason.
An index whose copy was complete stays blocked, or under its copy's name, until you run the upgrade again, so retry once the cause is fixed.
If Helm timed out, the hook can still be running, so check `kubectl get jobs -n hopsworks -l component=opensearch-index-upgrade` before you retry, because a retry starts a second run beside it.

- **Not enough disk:** free space on the smallest data node and retry.
  The hook also stops when it cannot measure free disk or an index size, rather than skipping the check.
- **A closed index:** open it, or reindex it by hand, and retry.
  The hook refuses to copy a closed index because it can neither size nor read it, and nothing in Hopsworks leaves an index closed, so this usually means a snapshot restore that died.
  Leaving it closed does not help, since a 3.x node still refuses to start.
- **Timed out:** raise `activeDeadlineSeconds` and `--timeout` together and retry.
  The retry finishes the index that was in the middle of a copy.
- **Killed while `.opendistro_security` was missing:** the security REST API answers HTTP 500 until the retry, which restores that index first.
- **A block the hook did not set:** an index to copy that already carries a `write`, `read_only` or `read_only_allow_delete` block stops the hook before it changes anything.
  Release it with `PUT <index>/_settings {"index.blocks.<block>": null}` and retry.
  A flood-stage disk watermark sets `read_only_allow_delete`, so free disk first in that case.
- **Stored source that is off or pruned:** `_reindex` copies the stored source, so an index with `_source` disabled, or with `includes` or `excludes`, would lose fields.
  The hook refuses it, also when it looks empty, and you reindex it by hand from where its data came from, or delete it if it holds nothing.
- **`<index> was created by something else while it was absent`:** a write reached the name in the moment between the delete and the clone, or an OpenSearch node started while `.opendistro_security` was missing and created it from the chart's files.
  The copy holds every document the original held and is kept.
  Save what the new index holds if you need it, delete the new index, and retry.
- **Document counts differ after a copy:** something wrote to the index past its block.
  Stop that writer and retry.
- **A refresh or a count fails:** the log has the response.
  The hook never treats an index it could not count as empty.
- **nmslib vector fields:** see [Vector fields that would stay on nmslib][opensearch-nmslib-fields].
- **No answer from the cluster:** the hook prints the address and the last HTTP code.
  `000` is a DNS or connection failure, or a rejected admin certificate.
  `401` or `403` means the certificate's distinguished name is not in `plugins.security.authcz.admin_dn`.

## If an OpenSearch pod stays Pending during the roll

With node-local storage, an OpenSearch pod can only start on the node that holds its data volume.
If that node is short of memory while old and new pods run side by side, the pod stays `Pending` with `Insufficient memory` and `didn't match PersistentVolume's node affinity`.
Free memory on that node first, for example with `kubectl scale -n hopsworks deploy hopsworks-instance --replicas=0`, and pass `--set hopsworks.replicaCount.worker=0` to the upgrade so that Helm does not scale the backend back up during the roll.
Scale it back afterwards.
OnlineFS restarting with `Failed to get all projects` meanwhile is expected, because the backend is down.

### To reindex by hand { #opensearch-reindex-by-hand }

To reindex by hand instead, set `olk.opensearch.indexUpgrade.mode` to `report`.
The hook then reports the offending indices and fails, and for each one you run:

```text
POST /_reindex {"source":{"index":"<name>"},"dest":{"index":"<name>-tmp"}}
DELETE /<name>
POST /_reindex {"source":{"index":"<name>-tmp"},"dest":{"index":"<name>"}}
DELETE /<name>-tmp
```

Three things have to be right when you do it by hand:

- Create the destination index first from the source's settings and mappings, because `_reindex` builds its destination from index templates and silently drops `index.knn` and `knn_vector` mappings.
- For an embedding index, set `method.engine` to `faiss` in the destination mapping, as the hook does, for `l2`, `cosinesimil` and `innerproduct` fields.
  A destination that keeps nmslib is created on 2.x, so 3.8 opens it, but filtered similarity search on it still fails, and a 3.8 node on a CPU without AVX-512 crashes when it loads it.
- Block writes on the source with `PUT /<name>/_block/write` before you copy it, so writes during the copy are refused instead of missed by it.
  The call returns once the writes already admitted have finished.
  `_reindex` reads its source through a scroll, which the block does not cover, so the copy still runs, whereas a block on the destination refuses it.
  Keep writers stopped from the `DELETE` until the recreated index is filled, because a write to the missing name creates it from the index templates.
- Use the admin certificate for `.opendistro_security`, `.opendistro-ism-config` and `.plugins-ml-config`, because these protected system indices answer 403 to the `admin` user's password.
