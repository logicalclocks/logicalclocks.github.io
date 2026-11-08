---
description: Copy the files under a prefix of an S3, GCS, ADLS, SFTP or Google Drive data source into a project dataset with a files ingestion job, optionally mirroring deletions and keeping a file index feature group.
---

# Copy files from S3, GCS, ADLS, SFTP or Google Drive into a dataset { #files-ingestion }

## Introduction

An [S3][data-source-s3], [GCS][data-source-gcs] or [ADLS](creation/adls.md) data source can do more than back external feature groups over tabular files.
It can also copy the files under a prefix of its bucket or container, whatever their format, into a dataset of the project, either once or on a schedule.
An [SFTP][data-source-sftp] or [Google Drive][data-source-google-drive] data source exists only for this, and copies the files under a path of the server or a folder of the Drive the same way.
This is the **files mode** of the dltHub ingestion job that also [ingests tables into feature groups][ingest-data-with-dlthub].

Each run lists the prefix, copies the files that are new or changed, skips the ones it already has, and writes a small CSV audit file of what it changed, so downstream jobs can process only what changed.
Optionally, a run also deletes from the dataset the files that disappeared from the source, and keeps a feature group with one row per file.

Data only flows from the source into Hopsworks.
Changes made in the dataset are never written back to the bucket.

Typical uses are document corpora for retrieval, agents and unstructured data pipelines, where the files are read from the dataset through the HopsFS mount of a job, a terminal or an app.
Tabular files that should become feature groups are better served by an external feature group over the path, or by the table ingestion flow; see [Limitations](#limitations).

## Prerequisites

### Data source

A data source of type S3, GCS, ADLS, SFTP or Google Drive in the project's feature store, with credentials that can list and read the prefix.
Create it as described in the [S3][data-source-s3], [GCS][data-source-gcs], [ADLS](creation/adls.md), [SFTP][data-source-sftp] or [Google Drive][data-source-google-drive] guide.
Other data source types are not supported; see [Limitations](#limitations).

An S3 data source that authenticates with an IAM role must have a role mapping an administrator created with [AWS Role chaining](../../../setup_installation/admin/roleChaining.md); a data source without one is refused when the job is created.
Hopsworks assumes the role when it starts the job and hands the job temporary credentials that live for `dlt_files_credentials_duration_seconds`, an hour by default.
A run longer than that fails at the first request made with the expired credentials, so for a long first copy an administrator raises the setting, and before that the [maximum session duration of the role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html#id_roles_use_view-role-max-session), which must allow it.
Access key and secret, service account key file, service principal, SFTP password and SFTP private key credentials have no such limit.

### Role

Only data owners of the project can create, change or run a files ingestion job, because the copy widens access: every member who can read the dataset can read every copied file, whatever permissions the objects carry in the bucket.
A scheduled run executes as the user who created the job, so when that user leaves the project, another data owner takes the job over by editing it.

### Cluster version and environment

Files ingestion is available from Hopsworks 5.3.0.
The job runs in the `dlthub-ingestion-pipeline` environment, whose image ships with the cluster; the files mode needs the image of the same release as the backend, so a cluster that pins an older image cannot run it.
The Python client and the `hops` CLI need the same version or later.

### Cluster settings

| Variable | Default | Meaning |
| --- | --- | --- |
| `data_source_audit_retention_days` | `7` | Days of audit files kept per dataset. `0` keeps them forever. |
| `dlt_files_credentials_duration_seconds` | `3600` | Lifetime in seconds of the temporary credentials a run gets from an IAM-role S3 data source; the role's maximum session duration must allow it, and a longer run fails at the first expired request. |
| `dlt_files_listing_timeout_seconds` | `3600` | Seconds a run waits for the listing of the prefix; see [How a run works](#how-a-run-works). |

## Creation in the UI

### Step 1: Open the data source

Head to the `Data Sources` view in Hopsworks and open the data source, or create it and continue from its last step.
Click `Next` to open the second step of the wizard.

### Step 2: Choose `Copy files into a dataset`

The second step offers two ways to use the data source: `External feature group over a path`, which keeps the files where they are, and `Copy files into a dataset`, which this guide covers.
For an ADLS, SFTP or Google Drive data source only the second is offered, since those types back no feature groups.

<!-- TODO screenshot files_ingestion_wizard.png to capture; uncomment once the file exists:
<figure markdown>
  ![Copy files into a dataset](../../../assets/images/guides/fs/data_source/files_ingestion_wizard.png)
  <figcaption>The second step of the wizard, with Copy files into a dataset selected</figcaption>
</figure>
-->

1. **Prefix**: the path inside the bucket or container whose files are copied, for example `handbook/2026/`.
   It is relative to the root of the bucket or container; the path set on an S3 data source is not applied, so repeat it in the prefix when the files live under it.
   For SFTP it is relative to the root path of the data source, and for Google Drive it is a path of folder names below the shared folder, so a run lists `sftp://<host>:<port><root path>/<prefix>` or `gdrive://<folder ID>/<prefix>`.
   A prefix is a folder, not the start of a key: the job lists under `<prefix>/`, so `handbook` selects `handbook/a.pdf` but not `handbook-old/a.pdf`.
   Click `Browse` to pick it from a listing of the bucket; each level lists its folders and files, with their size and modification time.
   Browsing is not available for ADLS, SFTP and Google Drive, so type the prefix there.
   An empty prefix copies the whole bucket, root path or folder; see [How a run works](#how-a-run-works) before doing that on a large one.
2. **Include** and **Exclude**: glob patterns, one per line, matched against the path of each file relative to the prefix, not to the bucket.
   With prefix `handbook/`, write `**/*.pdf`, not `handbook/**/*.pdf`.
   `**` matches across folders, so `**/*.pdf` selects every PDF under the prefix and `**/~$*` excludes Office lock files.
   A file is copied when it matches at least one include pattern, or all of them when there is none, and no exclude pattern.
3. **Dataset**: a new dataset in the project root, or an existing one.
   A new dataset is created editable by data owners only, and an existing one is accepted only with that permission, since every run writes into it as a data owner.
   The platform datasets `Logs`, `Resources`, `Jupyter`, `Models`, and the training-datasets and feature-store datasets cannot be targets.
   A dataset can be the target of at most one files ingestion job across all data sources of the project; choosing one that another job already copies into is refused.
4. **Mirror deletions**: also delete from the dataset the files that are no longer under the prefix; see [Mirroring deletions](#mirroring-deletions).
   Off by default, so a plain run only adds and updates.
5. **Index the files in a feature group**: keep a feature group with one row per file; see [The file index](#the-file-index).
   **Feature group** names it; empty means `files_<dataset>`.
6. **Maximum file size** in MB; larger files are skipped and reported. Empty or `0` copies every file.
7. **Schedule**: an optional schedule for recurring runs, as for any [scheduled job](../../projects/jobs/schedule_job.md): a [Quartz cron expression](https://www.quartz-scheduler.org/documentation/quartz-2.3.0/tutorials/crontrigger.html) in UTC, seconds first, so `0 0 2 ? * *` runs daily at 02:00.
8. **Memory** and **CPU cores** of the job, `2048` MB and `1` core by default; the job copies one file at a time, so memory matters more than cores.
9. Under `Advanced`:
    - **Files per page**: how many objects a listing request returns, `100` by default.
    - **Fail on first error**: stop the run at the first file that fails instead of continuing with the others.
    - **Job name**: `<data source>_<dataset>_files` by default, with every character outside letters, digits and underscore replaced by `_`.
    - **Alerts**: an alert receiver notified when a run fails.

<!-- TODO screenshot files_ingestion_prefix_browser.png to capture; uncomment once the file exists:
<figure markdown>
  ![Prefix browser](../../../assets/images/guides/fs/data_source/files_ingestion_prefix_browser.png)
  <figcaption>Browsing the bucket for the prefix</figcaption>
</figure>
-->

Click `Create` to create the job, the dataset if it is new, and the index feature group if indexing is on.
The job is also started unless you turn `Start the job after creation` off.

### The job page

The job appears in the `Jobs` view like any other ingestion job, and its page shows the data source, prefix, patterns and dataset it copies into.
`Edit` changes the prefix, patterns, mirroring, indexing, size cap, schedule and resources; the data source and the dataset of a job cannot change, so create another job to copy into a different dataset.

<!-- TODO screenshot files_ingestion_job.png to capture; uncomment once the file exists:
<figure markdown>
  ![Files ingestion job page](../../../assets/images/guides/fs/data_source/files_ingestion_job.png)
  <figcaption>The page of a files ingestion job</figcaption>
</figure>
-->

Each execution row shows the counters of the run: files listed (after the include and exclude patterns), copied, updated, skipped as unchanged, deleted, failed and oversized, and the bytes copied.
The `Audit` link of a run that changed something opens its audit CSV in the file browser; see [State and audit files](#state-and-audit-files).
The execution logs show every file the run touched and the error of each file that failed.

<!-- TODO screenshot files_ingestion_executions.png to capture; uncomment once the file exists:
<figure markdown>
  ![Executions of a files ingestion job](../../../assets/images/guides/fs/data_source/files_ingestion_executions.png)
  <figcaption>The executions of a files ingestion job with their counters and audit link</figcaption>
</figure>
-->

### Deleting the job

Deleting the job removes its schedule, its credentials in the cluster and its state directory, and keeps the dataset and the index feature group by default.
The delete dialog offers `Also delete the dataset` and `Also delete the index feature group`.
The index is only deleted when it is the feature group the job created, so a feature group that existed before the job is never removed.
A data source that still has files ingestion jobs cannot be deleted; delete the jobs first.

<!-- TODO screenshot files_ingestion_delete.png to capture; uncomment once the file exists:
<figure markdown>
  ![Deleting a files ingestion job](../../../assets/images/guides/fs/data_source/files_ingestion_delete.png)
  <figcaption>The delete dialog of a files ingestion job</figcaption>
</figure>
-->

## Using the Python client

`ingest_files` on an S3, GCS, ADLS, SFTP or Google Drive data source creates the job and returns it; other data source types raise.

```python
import hopsworks


project = hopsworks.login()
fs = project.get_feature_store()

s3 = fs.get_data_source("acme_docs").storage_connector

job = s3.ingest_files(
    dataset="acme_docs_handbook",  # existing (owned) or new
    prefix="handbook/2026/",  # a folder, from the bucket root; relative to it:
    include=["**/*.pdf", "**/*.docx"],
    exclude=["**/~$*"],
    mirror_deletions=False,
    index=False,  # True -> files_<dataset>; or a feature group name
    max_file_size_mb=None,  # None or 0 -> no cap
    schedule=None,  # Quartz cron in UTC, e.g. "0 0 2 ? * *" for daily at 02:00
    resources=None,  # {"cores": 1, "memory": 2048, "gpus": 0}
    name=None,  # job name, default "<data source>_<dataset>_files"
    fail_on_first_error=False,
    files_per_page=100,
)

execution = job.run(await_termination=True)
execution.files_progress  # counters of the run, None until the run wrote them
job.last_stats  # the same for the latest execution

job.job  # the hopsworks Job
job.name, job.dataset_name, job.prefix, job.index_feature_group

job = job.update(
    prefix="handbook/",
    include=["**/*.pdf"],
    mirror_deletions=True,
    index=True,
    max_file_size_mb=500,
)

s3.get_files_ingestion_jobs()  # the files ingestion jobs of this data source

job.delete(delete_files=False, delete_index=False)
```

`files_progress` and `last_stats` return the stats of the run as a dictionary with the keys of the stats file described in [State and audit files](#state-and-audit-files), plus `datasetName`, `connectorName`, `prefix` and `auditPath`, the absolute HopsFS path of the audit file.
`prefix` is a folder relative to the root of the bucket or container, to the SFTP root path or to the Drive folder, as in the UI, and the patterns are relative to the prefix.
`update` re-saves the job; a job's data source and dataset cannot change.
`index` accepts a feature group name only while the job had no index; afterwards turning it on uses the name chosen then.

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-method"></code> [`FeatureStore.get_data_source`][hsfs.feature_store.FeatureStore.get_data_source]
    - <code class="doc-symbol doc-symbol-class"></code> [`StorageConnector`][hsfs.storage_connector.StorageConnector]
        - <code class="doc-symbol doc-symbol-method"></code> `ingest_files`
        - <code class="doc-symbol doc-symbol-method"></code> `get_files_ingestion_jobs`
    - <code class="doc-symbol doc-symbol-class"></code> `FilesIngestionJob`
        - <code class="doc-symbol doc-symbol-method"></code> `run`
        - <code class="doc-symbol doc-symbol-method"></code> `update`
        - <code class="doc-symbol doc-symbol-method"></code> `delete`
        - <code class="doc-symbol doc-symbol-attribute"></code> `last_stats`
    - <code class="doc-symbol doc-symbol-class"></code> `Execution`
        - <code class="doc-symbol doc-symbol-attribute"></code> `files_progress`

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>

## Using the CLI

```bash
hops datasource ingest-files acme_docs --dataset acme_docs_handbook \
  --prefix handbook/2026/ --include "**/*.pdf" --include "**/*.docx" \
  --exclude "**/~$*" --cron "0 0 2 ? * *"
hops datasource ingest-files acme_docs --dataset acme_docs_handbook \
  --prefix handbook/ --mirror-deletions --index --max-file-size-mb 500 --no-run
```

The command creates the job, prints its name and, unless `--no-run`, starts a run and prints its execution id.
`--include` and `--exclude` repeat; `--index` names the feature group `files_<dataset>` and `--index-name` chooses another name; `--name` sets the job name.
`hops datasource files-jobs acme_docs` lists the files ingestion jobs of the data source.
Runs, schedules, logs and deletion of the job are managed with the `hops job` commands, as for any job.

## How a run works

The job runs as a Kubernetes pod of the `dlthub-ingestion-pipeline` environment, with the data source's credentials in a Secret and the job's configuration in a ConfigMap that are rewritten at every start, so a credential changed on the data source is used by the next run.
The dataset and the state directory are reached through the pod's HopsFS mount.
A run goes through these steps.

1. **Lease**.
   The run takes a lease on the dataset, `lease.json` in the state directory, and refreshes it every minute.
   A run that finds a lease refreshed within the last five minutes by another execution exits without copying anything, as a success, with `another run is active` in its log; this is what happens when a schedule fires while the previous run is still copying.
   A lease older than five minutes is taken over, so a killed run does not block the next one.
2. **Listing**.
   The run lists every object under the prefix, in pages of `Files per page`, and applies the include and exclude patterns.
   The listing is full every run, with no incremental listing, so a run over a prefix with millions of objects spends most of its time listing; narrow the prefix, or split it across jobs, for very large buckets.
   The run waits `dlt_files_listing_timeout_seconds`, an hour by default, for the listing; the timeout bounds the listing only, not the copies.
   A listing that exceeds it fails the run with an incomplete listing, `listingComplete` false in the stats, and deletions are never mirrored from one.
3. **Skip or copy**.
   Each listed file is compared with its row in the manifest of the previous runs.
   A file whose copy is in the dataset and whose size and modification date are unchanged is skipped, and counted as `skipped`; there is no checksum comparison, so a file changed without a change of either is only copied again after it is deleted from the dataset.
   A file over the size cap is counted as `oversized`, listed in the audit file, and not copied until it shrinks or the cap is raised.
   Any other file is downloaded one at a time, written next to its destination as a temporary file and renamed into place once complete, so readers of the dataset never see a partial file; it is counted as `copied` when new and `updated` when it replaced an earlier copy.
   The copy keeps the path relative to the prefix, so `handbook/2026/a/b.pdf` under prefix `handbook/2026/` lands at `<dataset>/a/b.pdf`.
4. **Failures**.
   A file that cannot be downloaded or written is counted as `failed`, logged with its error, and the run continues with the next file unless `Fail on first error` is on.
   The previous copy of a failed file, if any, stays in place and in the manifest, and the file is retried on the next run.
   A run that cannot list the prefix, reach the dataset or write its state fails outright.
5. **Mirroring and indexing**, when turned on; see the next sections.
6. **Stats and audit**.
   The run writes its stats file and, when it changed something, its audit file, then releases the lease.

The outcome of a run is its `status` in the stats file and the state of its execution:

| Status | Exit code | Execution | Meaning |
| --- | --- | --- | --- |
| `ok` | `0` | `FINISHED` | Every listed file is in the dataset, copied or unchanged; oversized files are reported but do not fail the run. |
| `partial` | `2` | `FAILED` | Some files failed, or the prefix listed nothing while the dataset holds copies; the successful copies are kept and the failed ones are retried on the next run. |
| `failed` | `1` | `FAILED` | The run stopped on an error, named in `error` and in the logs; with `Fail on first error`, that of the first file. |

A partial run fails its execution so that the alert receiver is notified and the execution row shows it; the dataset still holds every file that was copied.

A run that is killed, or that loses its credentials when an IAM role session expires, leaves no partial file in the dataset, since copies are renamed into place only when complete, and leaves its lease to expire.
The manifest is written whole at the end of a run, so the files such a run copied are compared by size and modification date again on the next run and found unchanged.

## Mirroring deletions

With `Mirror deletions` on, a run that completed its listing without any failed file deletes from the dataset every file whose source object is gone from the prefix or no longer matches the patterns, and counts them as `deleted`.
Empty folders left behind are removed too.

Deletions are skipped, and `deletionsSkipped` is set in the stats, whenever the run cannot be sure the file is really gone:

- the listing was incomplete, because it timed out or failed part way;
- any file failed to copy in this run, since a listing problem and a copy problem can have the same cause;
- the listing was complete but empty while the previous run had copied files.
  The run then ends as `partial` with the error that the prefix listed nothing, so a prefix typo or a moved folder cannot empty the dataset.
  Fix the prefix, or empty the dataset by hand when the source is really empty.

The next run that lists and copies cleanly performs the deletions.
A run with mirroring off never deletes, so a file removed from the prefix stays in the dataset until mirroring is turned on or a data owner deletes it.

Mirroring only touches files the job copied, that is, files with a row in the manifest.
Files that a data owner placed in the dataset by other means are left alone, but a file with the same relative path as a source object is overwritten by it.

## State and audit files

The job keeps its state in the project at:

```text
DataSources/<data source>/files/<dataset>/
```

| File | Written by | Content |
| --- | --- | --- |
| `owner.json` | Hopsworks, when the job is created | The job that copies into this dataset: `jobId`, `jobName`, `connectorId`, `connectorName`, `datasetName`, `createdAt`. A second files job on the same dataset is refused while it exists. |
| `lease.json` | the run | `executionId`, `pod`, `startedAt` and `heartbeat` of the run that holds the dataset; see [How a run works](#how-a-run-works). |
| `manifest.jsonl` | the run | One JSON object per file in the dataset: `file_id` (SHA-1 of the source URL), `source_url`, `relative_path`, `hopsfs_path`, `file_name`, `file_type`, `mime_type`, `size_bytes`, `modified_at`, `etag` (reserved, always empty), `content_hash` (SHA-256 of the copy), `execution_id` and `copied_at` of the run that copied it. Replaced atomically at the end of each run. |
| `<execution id>_files_stats.json` | the run, also when it fails | The outcome of the run, described below. |
| `audit/date=<YYYY-MM-DD>/<HHMMSS>Z_<execution id>.csv` | the run, when it changed something | One row per changed file, described below. |

The stats file holds the counters shown in the UI and returned by `files_progress`:

```json
{
  "executionId": 4711,
  "startedAt": "2026-11-07T10:15:00Z",
  "finishedAt": "2026-11-07T10:21:30Z",
  "status": "partial",
  "listed": 120,
  "copied": 10,
  "updated": 2,
  "skipped": 100,
  "deleted": 3,
  "failed": 1,
  "oversized": 4,
  "bytesCopied": 123456,
  "listingComplete": true,
  "deletionsSkipped": true,
  "indexed": 12,
  "error": null,
  "auditFile": "audit/date=2026-11-07/101500Z_4711.csv",
  "failedFiles": [{"relativePath": "a/b.pdf", "error": "..."}]
}
```

`failedFiles` lists at most 100 files; the logs list them all.
`auditFile` is relative to the state directory and null when the run changed nothing.

The audit file has the same columns as the [SharePoint](creation/sharepoint.md#the-audit-log) audit log:

```csv
execution_id,op,kind,path,src_path
4711,copied,file,a/b.pdf,s3://acme-docs/handbook/2026/a/b.pdf
4711,updated,file,a/c.pdf,s3://acme-docs/handbook/2026/a/c.pdf
4711,deleted,file,old/d.pdf,s3://acme-docs/handbook/2026/old/d.pdf
4711,failed,file,a/e.pdf,s3://acme-docs/handbook/2026/a/e.pdf
4711,oversized,file,video/f.mp4,s3://acme-docs/handbook/2026/video/f.mp4
```

`op` is `copied`, `updated`, `deleted`, `failed` or `oversized`, `kind` is always `file`, `path` is the path relative to the dataset root and `src_path` the source URL.

The `date=` directories are Hive-style partitions, so a filter on `date` reads only the matching days.
From a Python job, with DuckDB from the `python-feature-pipeline` environment:

```python
import duckdb


changes = duckdb.sql(
    """
    SELECT date, execution_id, op, path, src_path
    FROM read_csv('/hopsfs/DataSources/acme_docs/files/acme_docs_handbook/audit/*/*.csv',
                  hive_partitioning = true,
                  columns = {'execution_id': 'BIGINT', 'op': 'VARCHAR',
                             'kind': 'VARCHAR', 'path': 'VARCHAR',
                             'src_path': 'VARCHAR'})
    WHERE date >= DATE '2026-11-01' AND op IN ('copied', 'updated')
    """
).df()
```

Each run deletes the audit days older than `data_source_audit_retention_days`.

## The file index

A job with indexing on keeps version 1 of a Delta feature group, `files_<dataset>` by default, with one row per file in the dataset.
Hopsworks creates it with the job, offline only and without statistics, with `file_id` as primary key and `ingestion_date` as partition key, and the job page links it.

| Column | Content |
| --- | --- |
| `file_id` | SHA-1 of the source URL, the primary key; it stays the same as long as the object keeps its key |
| `connector`, `source_type` | the data source and its type, `s3`, `gcs`, `adls`, `sftp` or `gdrive` |
| `file_name`, `file_type` | the name, and its extension in lowercase |
| `relative_path` | the path relative to the prefix and to the dataset root |
| `hopsfs_path` | the copy in the dataset, `/Projects/<project>/<dataset>/...` |
| `source_url` | the object, as `s3://`, `gs://`, `az://`, `sftp://` or `gdrive://` URL |
| `mime_type`, `size_bytes` | content type, from the extension, and size in bytes |
| `modified_at` | the object's last modification time, UTC |
| `content_hash`, `etag` | SHA-256 of the copy, and a reserved column that is always empty |
| `execution_id`, `indexed_at` | the run that last wrote the row, and when |
| `ingestion_date` | the partition: the UTC day the file was first indexed, which is the day it was copied in, or for a file already in the dataset, the day indexing was turned on |

The table holds no file content; the file is in the dataset at `hopsfs_path`.

After mirroring, each run compares the manifest with the table:

- A file that has no row, or whose `relative_path`, `size_bytes`, `modified_at` or `content_hash` changed, is written.
  A new file goes into today's partition; a changed file keeps the partition of the day it was first indexed.
- The row of a file that mirroring deleted is removed.
- A file whose copy failed keeps its current row, or gets none, until a run copies it.

The rows are written and deleted with delta-rs through the feature group's `insert` and `remove_rows`, so each run adds commits to the feature group's activity, and a run compacts and vacuums the table afterwards; see [Delta maintenance][delta-maintenance-feature-group].
Indexing can be turned on for an existing job: its next run indexes every file in the manifest.
Turning it off keeps the feature group.
The name of an index must not be that of an existing feature group, and a job deletes only the feature group it created.

In a terminal, the feature store is mounted at `/hopsfs/featurestore/<project>_featurestore.db/`, and the DuckDB CLI reads the index with its `delta` extension:

```bash
duckdb -c "SELECT file_name, size_bytes, modified_at, hopsfs_path
FROM delta_scan('/hopsfs/featurestore/acme_featurestore.db/files_acme_docs_handbook_1')
WHERE file_type = 'pdf' ORDER BY modified_at DESC LIMIT 20;"
```

Use `delta_scan`, not `read_parquet` over the partition directories: until a vacuum, those directories also hold the files of deleted and rewritten rows.

Claude and the other coding agents in a terminal load the `hops-files-search` skill for questions about the copied files; it finds the index of a dataset and shapes the queries this way.

## Limitations

- Only S3, GCS, ADLS, SFTP and Google Drive data sources are supported.
  [SharePoint](creation/sharepoint.md), Gmail and Outlook have their own sync jobs.
- The listing is full on every run, and files are copied one at a time, so a prefix with millions of objects or a very large total size is better split into several jobs with narrower prefixes.
- A run on an IAM-role S3 data source cannot outlast `dlt_files_credentials_duration_seconds`.
- Files are copied as they are.
  Turning tabular files into feature groups is not part of this job; use an [external feature group](../feature_group/create_external.md) over the path or the [table ingestion flow][ingest-data-with-dlthub] instead.
- Browsing the source for a prefix is not available for ADLS, SFTP and Google Drive; type the prefix.
- One job per dataset: a dataset that one job copies into cannot be the target of another, whatever its data source.
- The backend and the `dlthub-ingestion-pipeline` image must be of the same release; an older image does not know the files mode.

## Next steps

- Read the copied files from a job or an app through the HopsFS mount, at `/hopsfs/<dataset>/...`, and the index with the [feature group API][create-feature-group].
- [Share the dataset](../../projects/datasets/sharing.md) read-only with another project.
- Ingest tables of an S3, GCS or ADLS data source into feature groups with the [dltHub ingestion job][ingest-data-with-dlthub].
