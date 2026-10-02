---
description: What to know before upgrading the OpenSearch that ships with Hopsworks, from 5.0 and 5.1 to 5.2
---

# Upgrading OpenSearch { #upgrading-opensearch }

## Introduction

Each Hopsworks release ships a fixed OpenSearch version, and upgrading Hopsworks upgrades it.

| Hopsworks | OpenSearch |
| --------- | ---------- |
| 4.8.x, 5.0.x | 1.3.x |
| 5.1.x | 2.19.x |
| 5.2.x | 3.8.0 |

This page covers what changes for you on the 5.1 to 5.2 upgrade, because that is the one that can interrupt service.
The step-by-step commands are in `UPGRADE.md` in the [hopsworks-helm repository](https://github.com/logicalclocks/hopsworks-helm/blob/main/UPGRADE.md).

## Upgrade one major at a time

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

The index pass therefore recreates each embedding index on faiss while it copies it, so similarity search with filters keeps working after the upgrade.
Approximate nearest neighbor results can shift slightly, because the graph is rebuilt on a different engine.
Indices that you created yourself, outside the Hopsworks embedding naming, keep their engine.

## Satellite clusters

A satellite cluster runs its own OpenSearch and gets its own index pass when it upgrades to 5.2.
The outage is confined to that satellite's OpenSearch, and `activeDeadlineSeconds` is set per release, so a satellite holding large embedding indices sets its own value and its own `--timeout`.

Upgrade every satellite to 5.1.x before the central cluster moves to 5.2.x.
A central cluster on 5.0.x creates nmslib indices, which 3.x refuses, and a satellite still on OpenSearch 1.3 would be two major versions behind a 5.2.x central cluster.
A satellite on 5.2.x while the central cluster is still on 5.1.x should work, but it is untested and not the recommended order.

## After the upgrade

Check that OpenSearch reports version 3.8.0, that the cluster health is green, and that there is no `StartupException` in the OpenSearch log.
Then run a search in the Hopsworks UI and a similarity search on a feature group with an embedding.
Re-ingest the feature groups that OnlineFS marked failed during the outage.
