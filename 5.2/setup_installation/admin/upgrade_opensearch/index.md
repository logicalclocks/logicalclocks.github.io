# Upgrading OpenSearch { #upgrading-opensearch }

## Introduction

Each Hopsworks release ships a fixed OpenSearch version, and upgrading Hopsworks upgrades it.

| Hopsworks | OpenSearch |
| --------- | ---------- |
| 4.8.x, 5.0.x | 1.3.x |
| 5.1.x | 2.19.x |
| 5.2.x | 3.8.0 |

This page covers what changes for you on the 5.1 to 5.2 upgrade, because that is the one that can interrupt service, and the steps to run it.
The commands assume Hopsworks is installed in the `hopsworks` namespace.

## Upgrade one minor release at a time

Upgrade 5.0.x to 5.1.x, let it come up, then upgrade to 5.2.x.
Going from 5.0.x straight to 5.2.x is not supported.

OpenSearch 3.x refuses to start if the cluster still holds an index that was created before OpenSearch 2.0.
OpenSearch 2.19 keeps serving indices created by 1.x without rewriting them, so a cluster that has passed through 5.1.x can still hold such indices.
When a 3.x node meets one it stops during startup, while its container keeps reporting `Running`, so the first pod of the rolling upgrade never becomes ready and nothing in `kubectl get pods` says why.

## The index pass on 5.1.x to 5.2.x

A `pre-upgrade` hook runs before the OpenSearch StatefulSet is touched, so the old cluster is still intact if it fails.
It checks every index against the OpenSearch 2.0 floor.
A cluster that has only ever held indices created by 2.x has nothing to fix, and the hook exits immediately.

On a cluster installed before 5.1 the hook repairs what it finds:

- It deletes only the indices the platform recreates or expires by itself: logs, audit logs, `pypi_libraries_*`, and plugin indices that the plugin repopulates.
- It reindexes everything else with the name preserved, including `featurestore`, `projects`, the OpenSearch Dashboards saved objects, the index state management policies and the embedding indices behind similarity search.
  Nothing else is deleted, because anything the hook does not recognise might hold data nothing can rebuild.

### Plan for an outage

While the hook copies indices, every client except the hook is refused, reads included.
Hopsworks search, OpenSearch Dashboards, logstash and OnlineFS all receive HTTP 403 until the hook exits.
The hook does this so that no write can land in an index while it is being copied and then be overwritten by the copy coming back.

Rows written to feature groups with embeddings during the window are marked failed by OnlineFS rather than retried, because OnlineFS treats a rejected write as a permanent failure.
Re-ingest those feature groups after the upgrade.
Log lines shipped by logstash during the window may also be missing.

The hook restores access when it exits, whether it succeeds or fails.
If it is killed outright, for example by a node loss, clients stay refused until you run the upgrade again, because the next run picks up where it stopped and then lets clients back in.

### Set the timeout

The hook is bounded by `olk.opensearch.indexUpgrade.activeDeadlineSeconds`, which defaults to 3600 seconds.
Pass `helm upgrade --timeout` at least that long, or Helm gives up on the hook before the hook finishes.

A reindex copies each index twice to keep its name, so the time grows with the size of your old indices, `featurestore` and the embedding indices in particular.
As a guide, a copy ran at roughly 15 MB per second on a 16-CPU node, and slower disks or fewer CPUs take longer.
Before it starts, the hook prints the size of every index it will copy, an estimate, and the configured deadline, and warns when the estimate exceeds the deadline.
To read that report without changing anything, set `olk.opensearch.indexUpgrade.enabled` to `false`.
The hook then lists the indices and fails, and you can raise the deadline and the timeout before running the real upgrade.

Free disk space matters as well, because a copy needs room for a second complete copy of the largest index.
The hook checks this on the smallest data node and stops if there is not enough.

## Embedding indices move to faiss

OpenSearch indexes embeddings with an engine, and Hopsworks 5.1 and later create embedding indices on faiss.
Indices created by Hopsworks 5.0 and earlier use nmslib, which OpenSearch has deprecated and which does not accept the filter that the Hopsworks 5.1 and later clients send with every similarity search.

The index pass therefore recreates each embedding index on faiss while it copies it, so similarity search with filters works once the upgrade to 5.2 is done.
Until then, on 5.1, filtered search fails on feature groups whose embedding index was created on 5.0, as described in the upgrade steps below.
Approximate nearest neighbor results can shift slightly, because the graph is rebuilt on a different engine.
Indices that you created yourself, outside the Hopsworks embedding naming, keep their engine.

## Satellite clusters

A satellite cluster runs its own OpenSearch and gets its own index pass when it upgrades to 5.2.
The outage is confined to that satellite's OpenSearch, and `activeDeadlineSeconds` is set per release, so a satellite holding large embedding indices sets its own value and its own `--timeout`.

Upgrade every satellite to 5.1.x before the central cluster moves to 5.2.x.
A satellite still on OpenSearch 1.3 would be two major versions behind a 5.2.x central cluster.
A satellite on 5.2.x while the central cluster is still on 5.1.x should work, but it is untested and not the recommended order.

## Upgrade steps

1. Take a snapshot and check that it completed, because the index pass rewrites indices in place.
2. Upgrade to 5.1.x if you are not already on it, and confirm that OpenSearch 2.19 is live and green:

    ```bash
    kubectl exec -n hopsworks opensearch-0 -c opensearch -- bash -c \
      'curl -sk -u "admin:$ADMIN_PASSWORD" https://localhost:9200 | grep number'
    kubectl exec -n hopsworks opensearch-0 -c opensearch -- bash -c \
      'curl -sk -u "admin:$ADMIN_PASSWORD" https://localhost:9200/_cluster/health?pretty | grep status'
    ```

    The indices are still the ones 1.x created at this point.
    That is expected, since 2.19 does not rewrite them.

    Two known issues apply to this upgrade:

    - On the first OpenSearch 2.19 start of each cluster, central or satellite, vector writes are rejected for about two minutes and the vectors that had not been flushed are lost.
      The chart fixes this on the 5.1 line, and a values file that copied the old `knn.circuit_breaker` settings (`triggered: true` or `percent: 0.75`) keeps the problem.
    - On 5.1, similarity search with a filter fails on feature groups whose embedding index was created on 5.0, because the 5.1 client sends the filter inside the nearest-neighbor query and the nmslib engine rejects it.
      A client fix and the pass in step 3 both resolve it.
3. Upgrade to 5.2.x with a `--timeout` at least as long as `olk.opensearch.indexUpgrade.activeDeadlineSeconds`, and watch the hook:

    ```bash
    kubectl logs -n hopsworks -l component=opensearch-index-upgrade -f
    ```

    It ends with `Every index is now on OpenSearch 2.0 or later. Safe to upgrade.`
4. Verify the upgrade:

    ```bash
    kubectl get pods -n hopsworks -l app=opensearch
    kubectl logs -n hopsworks opensearch-0 -c opensearch | grep -c StartupException
    kubectl exec -n hopsworks opensearch-0 -c opensearch -- bash -c \
      'curl -sk -u "admin:$ADMIN_PASSWORD" https://localhost:9200 | grep -E "number|minimum_index"'
    ```

    The `StartupException` count must be 0.
    Expect version `3.8.0`, `minimum_index_compatibility_version` `2.0.0` and green cluster health.
    Then run a search in the Hopsworks UI and a similarity search on a feature group with an embedding.
5. Re-ingest the feature groups that OnlineFS marked failed during the outage.

## If the hook fails

The upgrade stops before the OpenSearch StatefulSet is touched, so the cluster is still on 5.1.x, and the hook lets clients back in on its way out.
The hook log names the index and the reason.

- **Not enough disk:** free space on the smallest data node and retry.
  The hook also stops when it cannot measure free disk or an index size, rather than skipping the check.
- **A closed index:** open it, or reindex it by hand, and retry.
  The hook refuses to copy a closed index because it can neither size nor read it, and nothing in Hopsworks leaves an index closed, so this usually means a snapshot restore that died.
  Leaving it closed does not help, since a 3.x node still refuses to start.
- **Timed out:** raise `activeDeadlineSeconds` and `--timeout` together and retry.
  The retry resumes any index that was in the middle of a copy.
- **No answer from the cluster:** the hook prints the address and the last HTTP code.
  `000` is a DNS or connection failure, or a rejected admin certificate.
  `401` or `403` means the certificate's distinguished name is not in `plugins.security.authcz.admin_dn`.

To reindex by hand instead, set `olk.opensearch.indexUpgrade.enabled` to `false`.
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
- Set `index.blocks.write` to `true` on the source before you copy it, so writes during the copy are refused instead of missed by it.
  `_reindex` reads its source through a scroll, which the block does not cover, so the copy still runs, whereas a block on the destination refuses it.
  Keep writers stopped from the `DELETE` until the recreated index is filled, because a write to the missing name creates it from the index templates.
- Use the admin certificate for `.opendistro_security`, `.opendistro-ism-config` and `.plugins-ml-config`, because these protected system indices answer 403 to the `admin` user's password.
