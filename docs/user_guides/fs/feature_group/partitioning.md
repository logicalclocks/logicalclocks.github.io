---
description: Documentation on partition transforms, liquid clustering, and z-ordering for Feature Groups in Hopsworks.
---

# How to partition and cluster a Feature Group { #partitioning-feature-group }

## Introduction

In this guide you will learn how to lay out the offline data of a feature group.
Each layout mechanism is its own creation-time parameter, and each parameter maps to exactly one native mechanism of the table format:

| Parameter | What it configures | Formats |
| --- | --- | --- |
| `partitioned_by` | A native partition specification from transform expressions, such as `["day(ts)", "bucket(16, customer_id)"]`. | `ICEBERG` (full transform set), `HUDI` (identity and time grains). Rejected on `DELTA`, which has no partition transforms. |
| `clustered_by` | Delta liquid clustering columns, such as `["ts", "customer_id"]`. | `DELTA` only. |
| `bucket_index` | The Hudi bucket index, as `{"field": <primary key column>, "num_buckets": N}`. | `HUDI` only. |
| `zorder_by` | Columns to z-order the data files by. | `ICEBERG` (applied by [`FeatureGroup.optimize`][hsfs.feature_group.FeatureGroup.optimize]), `HUDI` (inline clustering). Rejected on `DELTA`, where `clustered_by` covers the use case. |
| `sort_order` | A persistent write sort order, such as `["merchant_id asc", "amount desc nulls last"]`. | `ICEBERG` only, and requires a Spark environment at creation. |
| `partition_key` | Plain identity partitioning on existing columns. | All formats; mutually exclusive with `partitioned_by` and with `clustered_by`. |

## Prerequisites

Before you begin this guide we suggest you read the [Feature Group](../../../concepts/fs/feature_group/fg_overview.md) concept page and the [create feature group][create-feature-group] guide, which covers `partition_key`, `event_time`, and `time_travel_format`.

## Partition transforms

Each element of `partitioned_by` is one transform expression:

| Expression | Behaviour | Typical use |
| --- | --- | --- |
| `col` or `identity(col)` | The original column value. | Low-cardinality columns. |
| `bucket(N, col)` | Murmur3 hash of the column modulo N. | High-cardinality ids. |
| `truncate(W, col)` | The value truncated to width W (numeric ranges, string prefixes). | Range-like grouping. |
| `year(col)` | Year of a timestamp or date column. | Very large historical tables. |
| `month(col)` | Month. | Monthly queries. |
| `day(col)` | Calendar day. | Event and transaction tables. |
| `hour(col)` | Hour of a timestamp column. | High-volume streams. |
| `week(col)` | ISO week. | HUDI only: Iceberg has no week transform. |
| `void(col)` | Always null. | ICEBERG only: partition spec evolution placeholder. |

Parsing is whitespace tolerant and the expressions are stored in a canonical lowercase form without spaces, so `bucket(16, customer_id)` reads back as `bucket(16,customer_id)`.
A column that happens to be named after a grain (`year`, `month`, `week`, `day`, `hour`) must use the explicit form `identity(year)`, because the bare name is reserved for the legacy grain migration error; the canonical form keeps the explicit `identity()` for these columns.
Transforms combine freely, for example one temporal transform plus one bucket, with the format-specific restrictions listed below.

On Iceberg an expression can name its partition field with an alias, for example `"bucket(16, customer_id) as shard"`; Iceberg metadata tables and partition spec evolution refer to fields by name.
Without an alias the field gets Iceberg's generated default name (`customer_id_bucket`, `ts_day`, and so on), and all field names in one spec must be unique, so two bucket transforms on the same column need an alias on one of them.
Aliases are rejected on `HUDI`, whose partition paths are always named after the source column or grain.

Not every transform is available on every format, and `DELTA` rejects `partitioned_by` entirely:

| Transform | ICEBERG | HUDI |
| --- | --- | --- |
| `identity` | yes | yes |
| `bucket` | yes | no, use `bucket_index` |
| `truncate` | yes | no |
| `year`/`month`/`day`/`hour` | yes | yes, and the column must be the event time |
| `week` | no | yes, and the column must be the event time |
| `void` | yes | no |

## Iceberg: hidden partitioning

On Iceberg the transform list compiles into the table's native partition spec.
No derived columns are added to the feature group schema, and your DataFrame carries only the real columns.
Because the partitioning is hidden, every engine reading the table prunes partitions from ordinary predicates on the source columns.

```python
fg = feature_store.create_feature_group(
    name="orders",
    version=1,
    description="Order events, day-partitioned and bucketed by customer",
    primary_key=["order_id"],
    event_time="order_ts",
    time_travel_format="ICEBERG",
    partitioned_by=["day(order_ts)", "bucket(16, customer_id)"],
)
fg.insert(orders_df)
```

A read that filters on the source columns plans only the matching day partition and, within it, one bucket of sixteen:

```python
df = (
    fg.select_all()
    .filter(fg.get_feature("order_ts") >= "2026-07-03")
    .filter(fg.get_feature("order_ts") < "2026-07-04")
    .filter(fg.get_feature("customer_id") == 1042)
    .read()
)
```

Iceberg allows at most one temporal transform per source column, because a finer grain already supports coarser pruning: use `day(ts)` alone rather than `year(ts)` plus `day(ts)`.

### Persistent sort order

`sort_order` sets the Iceberg table's persistent write sort order, so every write organizes rows before laying out files.
Each element is a column with an optional direction and null ordering: `"col"`, `"col desc"`, `"col asc nulls last"`.
Defaults follow Iceberg: ascending, nulls first when ascending and nulls last when descending.

```python
fg = feature_store.create_feature_group(
    name="payments",
    version=1,
    primary_key=["payment_id"],
    event_time="ts",
    time_travel_format="ICEBERG",
    partitioned_by=["day(ts)"],
    sort_order=["merchant_id asc", "amount desc nulls last"],
)
```

A sort order is applied through the Iceberg Java API, so creating a feature group with `sort_order` requires a Spark environment; the pure Python and catalog creation paths reject it rather than silently dropping it.
`sort_order` is the right choice when reads consistently filter or join on the same columns; `zorder_by` covers multi-dimensional point lookups instead.
The two are mutually exclusive as stored defaults, because they prescribe conflicting file layouts (writes sorted linearly while maintenance rewrites on the z-curve); a one-off z-order on a sorted table stays available through `optimize(strategy="zorder", columns=[...])`.

### Layout for point-in-time training data

Training data from a feature view runs a point-in-time join: each feature group is joined to the label side on the primary key with an event-time inequality, and a rank window keeps the latest row per label.
Inside that query shape, an event-time bound on the feature group is pushed into the Iceberg scan, so `day(event_ts)` partitioning prunes the history scan to the bounded window.
Set the bound with a `lookback` on the feature view read (or an explicit `event_ts >=` query filter); without one, point-in-time correctness requires scanning all history, and no partitioning can prune it.

The layout that serves this access pattern:

```python
fg = feature_store.create_feature_group(
    ...,
    time_travel_format="ICEBERG",
    partitioned_by=["day(event_ts)", "bucket(16, customer_id)"],
    sort_order=["customer_id asc", "event_ts desc"],
)
```

- `day(event_ts)` prunes the scan to the lookback window.
- `bucket(N, primary_key)` keeps each day's data grouped by key, bounding the rows any one join task reads.
- `sort_order` (or `zorder_by` plus a scheduled `optimize()`) clusters rows by key inside each file, so file-level min/max statistics skip files for keys not present in the label set.
- Prefer `insert` (append) over upserts for event history: the Iceberg upsert rewrites the table and discards the maintained clustering until the next `optimize()`.

Size the partitioning to the data volume: each `(day, bucket)` combination becomes at least one file, so a small feature group with fine-grained partitioning produces many tiny files and the task overhead outweighs the pruning.
As a rule of thumb, choose the day grain and bucket count so partitions land in the hundreds of megabytes; for small feature groups skip `bucket()` or use a coarser time grain.

## Delta: liquid clustering with clustered_by

Delta has no partition transforms, so `partitioned_by` is rejected there; the layout mechanism is liquid clustering, configured with `clustered_by` as a plain column list.
This matches Delta's own API, where `clusterBy(...)` and `partitionedBy(...)` are different layout mechanisms.
Liquid clustering supports at most 4 columns, and `clustered_by` cannot be combined with `partition_key`, because Delta does not support clustering a hive-partitioned table.

```python
fg = feature_store.create_feature_group(
    name="transactions",
    version=1,
    primary_key=["tx_id"],
    event_time="ts",
    time_travel_format="DELTA",
    clustered_by=["ts", "customer_id"],
)
```

Data skipping on the clustered columns replaces directory-style partitioning, so no derived columns are added and reads need no special predicates.
Delta only clusters on columns that have data-skipping statistics, which it collects for the first 32 columns by default; when a clustering column sits past that position Hopsworks widens `delta.dataSkippingNumIndexedCols` to cover it, so any schema column can be clustered.

!!!warning "Clustered Delta feature groups are writable by Spark only"
    Liquid clustering uses the Clustering and DomainMetadata Delta writer table features, which delta-rs (the pure Python write path) does not implement, so treating them as optional would corrupt the table contract.
    Creating a clustered feature group from a Python environment with `stream=False` fails, and delta-rs writes, deletes, and optimize raise on clustered feature groups.
    From Python, pass `stream=True` so writes go through the Spark materialization job, or write from a Spark job or notebook.

## Hudi: grain columns and the bucket index

Hudi has no hidden partitioning, so temporal transforms materialize as integer partition columns named after the grain (`year`, `month`, ...), derived from the event time on every write.
Your DataFrame must not contain these columns; the write path computes them.
The grain columns appear in the feature group schema flagged as partition columns, and by default they are stored offline only (set `online_partition_columns=True` to include them online).

Bucketing on Hudi is not a partition transform: it is the Hudi bucket index, which hashes a primary key field into a fixed number of buckets, configured with the `bucket_index` parameter:

```python
fg = feature_store.create_feature_group(
    name="transactions",
    version=1,
    primary_key=["tx_id"],
    event_time="ts",
    time_travel_format="HUDI",
    partitioned_by=["year(ts)", "month(ts)"],
    bucket_index={"field": "tx_id", "num_buckets": 16},
)
```

`bucket_index` injects the corresponding write options:

```text
hoodie.index.type=BUCKET
hoodie.bucket.index.num.buckets=N
hoodie.bucket.index.hash.field=col
```

The optional `"engine"` key accepts only `"simple"` (the default): Hudi's consistent-hashing bucket engine requires a merge-on-read table with a clustering lifecycle, and Hopsworks Hudi feature groups are copy-on-write.
You can equally set these options, including a partition-level bucket index with per-partition `hoodie.bucket.index.*` overrides, directly through `write_options` on insert.

On Hudi the platform rewrites `event_time` range filters into grain-column predicates at query time, so reads that filter on the event time prune partitions without referencing the grain columns.

## Z-ordering with zorder_by

`zorder_by` records up to 4 columns to z-order the data files by, so point lookups on those columns inside a partition skip most files.
It is supported for `ICEBERG` and `HUDI`; on `DELTA` it is rejected because `clustered_by` covers the same use case.

```python
fg = feature_store.create_feature_group(
    name="ad_clicks",
    version=1,
    description="Click stream, hour-partitioned, z-ordered by user and campaign",
    primary_key=["click_id"],
    event_time="click_ts",
    time_travel_format="ICEBERG",
    partitioned_by=["hour(click_ts)"],
    zorder_by=["user_id", "campaign_id"],
)
fg.insert(clicks_df)
fg.optimize()
```

On Iceberg, z-order is a rewrite strategy rather than a write-time property: writes stay cheap, and calling [`FeatureGroup.optimize`][hsfs.feature_group.FeatureGroup.optimize] rewrites the data files ordered on the z-curve of the `zorder_by` columns.
Run it from a scheduled job after heavy ingestion.
The initial z-order over a backfill needs `optimize(rewrite_all=True)` to rewrite every existing file; routine maintenance calls default to `rewrite_all=False` so they never rewrite the whole table by accident.
On Hudi, `zorder_by` configures inline clustering, which applies the z-order layout as part of the write pipeline, so no explicit call is needed.

## Optimizing the layout

[`FeatureGroup.optimize`][hsfs.feature_group.FeatureGroup.optimize] rewrites the offline data files to apply the feature group's layout and returns the format's rewrite metrics:

| `time_travel_format` | What `optimize()` does |
| --- | --- |
| `ICEBERG` | An Iceberg `rewriteDataFiles` action; requires a Spark environment. `strategy` picks `"zorder"` (over `columns`, defaulting to `zorder_by`), `"sort"` (the persistent `sort_order`), or `"binpack"`; unset, it follows the stored layout in that order. `rewrite_all=True` rewrites every file regardless of the planner thresholds (defaults to False for every strategy, so a routine call is incremental; pass it for the initial full z-order), `target_file_size_mb` overrides the target file size, and `where` restricts the rewrite to the matching files through an Iceberg filter expression over the feature group's columns. |
| `DELTA` | `OPTIMIZE`, which incrementally clusters a liquid-clustered table; `optimize(full=True)` runs `OPTIMIZE FULL` to recluster all existing data after the clustering columns changed (clustered tables only), and `where` restricts the rewrite with a predicate. `strategy="zorder"` with `columns` runs the legacy `OPTIMIZE ... ZORDER BY`, which Delta only supports on unclustered tables, because z-order and liquid clustering are incompatible. Clustered feature groups require Spark; from pure Python only unclustered compaction is available. |
| `HUDI` | Rejected: layout maintenance runs through inline clustering on writes. |

### Catalog-backed Iceberg tables

The Iceberg feature is fully supported on the default path-based (`HadoopTables`) layout. Some operations are not yet available when the table is backed by an external catalog:

| Operation | Path-based | Glue Data Catalog | User-provided catalog (`iceberg.catalog`) |
| --- | --- | --- | --- |
| Create with `partitioned_by` | yes | yes | yes |
| Create with `sort_order` | yes | no (rejected at creation) | no |
| `optimize()` | yes | no (run the catalog's `rewrite_data_files` procedure) | no |
| `update_partition_spec()` | yes | no (evolve through the catalog) | no |
| Introspection (`get_partition_spec`, `describe_layout`, ...) | yes | yes | no (inspect through the catalog) |

Where an operation is unavailable the call raises with a pointer to the catalog-side equivalent rather than silently doing nothing.

## Evolving the layout

Layout is not fixed at creation; each format's native evolution is exposed, and all three methods require a Spark environment (from pure Python they raise, run them from a Spark job or notebook):

- [`FeatureGroup.update_partition_spec`][hsfs.feature_group.FeatureGroup.update_partition_spec] evolves an Iceberg partition spec.
  Evolution is metadata-only: existing data keeps its old layout and new writes use the evolved spec, so no data is rewritten.

    ```python
    fg.update_partition_spec(add=["hour(ts)"], remove=["day(ts)"])
    ```

- [`FeatureGroup.update_clustering`][hsfs.feature_group.FeatureGroup.update_clustering] changes the Delta clustering columns.
  The change affects new writes; run `optimize(full=True)` to recluster existing data.

    ```python
    fg.update_clustering(["ts", "customer_id"])
    fg.optimize(full=True)
    ```

- [`FeatureGroup.disable_clustering`][hsfs.feature_group.FeatureGroup.disable_clustering] turns Delta clustering off (`CLUSTER BY NONE`); existing data keeps its layout.

Hudi partitions are physical directories and cannot evolve; `update_partition_spec` is rejected there.
Partition spec evolution requires a feature group created with `partitioned_by`; a feature group using `partition_key` is rejected, because its identity partitions are recorded on the features themselves and cannot be restated as an evolvable spec.
After each evolution the committed spec is read back from the table and persisted as the feature group's stored metadata (`partitioned_by`, `clustered_by`), so read-back always reflects the current layout, including changes made by external engines.
If the table change succeeds but the metadata update fails, the error says exactly that and names the applied layout; calling `update_partition_spec()` with no arguments re-syncs the stored metadata from the table without changing it.

## Inspecting the layout

The stored metadata describes what was requested; the table itself is the source of truth for what is physically there.
Five methods read the actual table state, so drift (for example, an external engine evolving the spec) is visible:

- [`FeatureGroup.get_partition_spec`][hsfs.feature_group.FeatureGroup.get_partition_spec] returns the current Iceberg partition spec fields (`ICEBERG` only).
- [`FeatureGroup.get_partition_specs`][hsfs.feature_group.FeatureGroup.get_partition_specs] returns the Iceberg spec history, oldest first (`ICEBERG` only).
- [`FeatureGroup.get_sort_order`][hsfs.feature_group.FeatureGroup.get_sort_order] returns the persistent sort order (`ICEBERG` only).
- [`FeatureGroup.get_clustering_columns`][hsfs.feature_group.FeatureGroup.get_clustering_columns] returns the actual Delta clustering columns (`DELTA` only, Spark required).
- [`FeatureGroup.describe_layout`][hsfs.feature_group.FeatureGroup.describe_layout] returns the stored metadata next to the actual table state for any format.

The format-specific getters raise on the wrong format rather than returning `None`, so an unconfigured layout is never confused with an unsupported operation.
For Iceberg feature groups written through a user-provided catalog (the `iceberg.catalog` write option), the current-metadata pointer lives in that catalog, so inspect the layout through the catalog instead; Glue-backed feature groups are inspected through the Glue Data Catalog automatically.

## Migrating from the grain list form

Earlier Hopsworks versions accepted `partitioned_by` as a list of bare grain names, for example `["year", "month"]`.
That form is no longer valid, because a bare element now means an identity transform on a column of that name.
Creation fails with an error pointing at the replacement: write the grain as a transform on your event time column, for example `["year(event_ts)", "month(event_ts)"]`.
Feature groups created with the old form keep working for reads; their stored layout is unchanged.
Writes and deletes to such feature groups fail with a migration-required error, because the new write path no longer derives the grain values and continuing would silently change the physical layout; recreate the feature group with the transform grammar to write again.

## Restrictions

- `partitioned_by` requires `time_travel_format` `ICEBERG` or `HUDI`; `clustered_by` requires `DELTA`; `bucket_index` requires `HUDI`; `zorder_by` requires `ICEBERG` or `HUDI`; `sort_order` requires `ICEBERG` and a Spark environment at creation.
- `partitioned_by` and `partition_key` cannot be combined, and neither can `clustered_by` and `partition_key`, nor `sort_order` and `zorder_by`.
- Temporal transforms require a `date` or `timestamp` source column, and `hour` requires a `timestamp`, because a date has no sub-day resolution.
- `bucket` and `truncate` follow the Iceberg source-type restrictions: `float`, `double`, and `boolean` sources are rejected, and `truncate` additionally rejects `date` and `timestamp`.
- Partition-field aliases are Iceberg-only, and all field names in one spec (explicit aliases and generated defaults) must be unique.
- The `bucket_index` field must be part of the primary key, because the Hudi bucket index hashes the record key; its `engine` accepts only `"simple"`.
- Clustered Delta feature groups are writable by Spark only; from Python use `stream=True`.
- Stream feature groups support `partitioned_by` and `clustered_by` on `ICEBERG` and `DELTA`, but `partitioned_by` is rejected on `HUDI`.
- Online-enabled feature groups support `partitioned_by` on `ICEBERG`, but not on `HUDI`, because the Hudi grain columns are not part of the online schema.
