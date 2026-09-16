---
description: Documentation on compacting, checkpointing and vacuuming Delta Feature Groups in Hopsworks.
---

# How to maintain a Delta Feature Group { #delta-maintenance-feature-group }

## Introduction

A Delta table that is written to repeatedly accumulates two things: data files and log entries.
Every commit writes at least one new data file, and every reader opens all of them.
Every commit also appends to the `_delta_log`, and a reader replays that log from the last checkpoint.
Neither is reclaimed on its own, and on a table written from Python neither is bounded on its own either: Spark writes a checkpoint every `delta.checkpointInterval` commits, delta-rs writes none.

Four methods on a feature group bound them.
They apply only to feature groups with `time_travel_format="DELTA"` and return `None` for any other format.

| Method | What it does |
| --- | --- |
| [`delta_optimize`][hsfs.feature_group.FeatureGroup.delta_optimize] | Rewrites many small files into fewer large ones. Also available as `delta_compact`. |
| [`delta_checkpoint`][hsfs.feature_group.FeatureGroup.delta_checkpoint] | Writes a checkpoint, so readers stop replaying the log from commit zero. |
| [`delta_cleanup_metadata`][hsfs.feature_group.FeatureGroup.delta_cleanup_metadata] | Expires the log entries a checkpoint already covers. |
| [`delta_vacuum`][hsfs.feature_group.FeatureGroup.delta_vacuum] | Deletes the data files no retained version references. |

Each dispatches on the engine, so the same call works from a Python client with delta-rs and from a PySpark job with Delta Spark.

## Prerequisites

Before you begin this guide we suggest you read the [Feature Group](../../../concepts/fs/feature_group/fg_overview.md) concept page and the [create feature group][create-feature-group] guide.

## The maintenance sequence

Run them in this order.

```python
fg = fs.get_feature_group("transactions", version=1)

fg.delta_optimize(max_concurrent_tasks=1)
fg.delta_checkpoint()
fg.delta_cleanup_metadata()
fg.delta_vacuum(retention_hours=168)
```

The order is what makes each step safe.
Compaction replaces many small files with few large ones and leaves the old ones on disk, still referenced by older versions.
The checkpoint goes next, so the smaller file list is recorded before anything is deleted.
Only then the two deletions: the log entries the checkpoint now covers, and the data files the compaction orphaned.

## Choosing a retention

`delta_vacuum` deletes files that versions inside the retention window no longer reference.
A query that is already running holds no lock on those files, so the retention has to stay comfortably longer than the longest query that runs against the group.
It is also the time travel window: a version whose files have been vacuumed cannot be read, which is why a compaction has to be followed by a checkpoint.

The effect of a short retention is not that a vacuum deletes more, but that it deletes sooner.
A run reclaims what earlier runs orphaned rather than its own rewrite, whose files are seconds old.

!!! warning "Delta's own floor"
    Delta refuses a retention under seven days unless its retention check is disabled.
    Hopsworks disables that check for you so a shorter retention takes effect, which means the value you pass is the value that applies.
    Pick it against your own readers rather than relying on the engine to refuse a bad one.

## Compacting only what changed

On a table partitioned by a date column, `after_ingest_date` bounds the rewrite to partitions at or after that date.

```python
fg.delta_optimize(after_ingest_date="2026-09-10")
```

Use it for anything that runs on a schedule.
Only files written since the last compaction need rewriting, and on a date-partitioned table they are all at or after that date, so bounding the rewrite this way keeps its cost flat.
Without it every run rewrites the whole table, including everything earlier runs already compacted, and the cost grows with the table forever.
Leave a day of slack for rows that arrived late.

Only a partition column can select files without reading them, so this is refused on a group that is not partitioned by a date.
Compact the whole table by leaving `after_ingest_date` unset.

## When to run them

For an append-heavy table, compact when the active file count crosses a threshold and otherwise once a day.
Around 100 files is the low hundreds of megabytes at typical commit sizes, near the engine's own target file size.

Read the last compaction time from the table's own history rather than keeping state, so the schedule survives restarts and multiple writers.

These can run from a [Hopsworks job](../../projects/jobs/pyspark_job.md) on a schedule.
Compaction is the only one of the four that a deployment reading the same table notices: measured beside live traffic it roughly doubled p99 for the few seconds it ran, while the median moved by a tenth of a millisecond.
The other three sat where the deployment sat with nothing running.
