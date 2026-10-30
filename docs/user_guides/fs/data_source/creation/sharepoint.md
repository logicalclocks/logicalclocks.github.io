# How-To set up a SharePoint Data Source

## Introduction

A SharePoint data source connects a Hopsworks project to a [SharePoint Online](https://learn.microsoft.com/en-us/sharepoint/introduction) site.
It does not back feature groups.
Instead, it copies a folder of one of the site's document libraries into a dataset of the project, either once or on a schedule.

Each copy is a **sync**.
A sync runs as an ordinary Python job in the project, which uses [rclone](https://rclone.org/) to copy the files.
Every run that changes something writes a small CSV audit file that lists the changed paths, so downstream jobs can process only what changed.

Data only flows from SharePoint into Hopsworks.
Changes made in Hopsworks are never written back to SharePoint.

## Prerequisites

### Microsoft Entra ID application

Hopsworks signs in to Microsoft Graph as an application, with the client credentials flow.
A tenant administrator registers the application and grants it access to the site:

1. In the [Microsoft Entra admin center](https://entra.microsoft.com), open `Applications`, then `App registrations`, and click `New registration`.
   Choose `Accounts in this organizational directory only`.
   No redirect URI is needed.
2. Note the `Application (client) ID` and the `Directory (tenant) ID` on the overview page.
3. Under `API permissions`, add a Microsoft Graph **application** permission, then click `Grant admin consent`.
   Use one of:
    - `Sites.Selected`, then grant the application `read` on the site with `POST /sites/{site-id}/permissions`.
      This limits the application to the sites you grant.
    - `Sites.Read.All`, which lets the application read every site in the tenant.
4. Under `Certificates & secrets`, create a client secret and copy its **Value**.
   The value is shown only once; the `Secret ID` next to it is not the secret.

The client secret is stored in the Hopsworks secret store.
The data source API never returns it, and the data source form leaves it blank when you edit the data source.
The sync job receives it at the start of each run, through a call that only a run of that sync, started by a data owner, can make.
A client secret has an expiry date, so set a new one on the data source before the old one expires.

### Site

You need the URL of the SharePoint site, for example `https://contoso.sharepoint.com/sites/Finance`.
The tenant must have a SharePoint Online license; without one, Microsoft Graph returns `Tenant does not have a SPO license` for every site.

### Network access

The sync job and the Hopsworks backend connect to Microsoft Entra ID, Microsoft Graph and the tenant's SharePoint hosts over HTTPS.
For the global cloud these are `login.microsoftonline.com`, `graph.microsoft.com` and `<tenant>.sharepoint.com`; the US Government and China clouds use their own hosts.
Clusters that restrict outbound traffic must allow them.

### Client version

The Python client and the `hops` CLI support SharePoint data sources from Hopsworks 5.3.0.
Clients older than 5.3.0 do not know the SharePoint type and fail to list a feature store's data sources once it has one, so upgrade the client in environments that list data sources.

### Cluster settings

SharePoint data sources are enabled by the cluster variable `enable_sharepoint_storage_connectors` (default `true`).
The following cluster variables, set by an administrator, apply to every sync:

| Variable | Default | Meaning |
| --- | --- | --- |
| `data_source_audit_retention_days` | `7` | Days of audit files kept per sync. `0` keeps them forever. |
| `data_source_sync_min_interval_minutes` | `5` | Shortest interval a sync schedule may fire at. |
| `data_source_sync_job_memory` | `1024` | Memory in MB of a new sync job. |
| `data_source_sync_job_cores` | `0.5` | Cores of a new sync job. |
| `data_source_sync_transfers` | `4` | Files a sync copies in parallel, unless the sync sets its own value. |
| `data_source_sync_max_run_minutes` | `0` | Longest a run may take before it stops; `0` is unlimited. |

## Creation in the UI

### Step 1: Set up a new data source

Head to the `Data Sources` view in Hopsworks and click `New data source`.
Pick the `SharePoint` card, in the `Files & documents` category.

<figure markdown>
  ![Data Source Creation](../../../../assets/images/guides/fs/data_source/data_source_overview.png)
  <figcaption>The Data Source view in the user interface</figcaption>
</figure>

### Step 2: Enter the connection details

1. **Name** and an optional **Description**.
2. **Cloud**: `Global`, `US Government` or `China`, the Microsoft cloud of the tenant.
3. **Tenant ID** and **Client ID** of the application.
4. **Client secret**: the secret value.
5. **Site URL**.
6. Under `Advanced`, **Site ID**: only needed for an application granted `Sites.Selected` that is not allowed to look the site up by its URL.

Click `Test connection` to check the credentials.
On success, Hopsworks lists the site's document libraries.
Click `Next: Create sync` to save the data source and set up the first sync.

### Step 3: Create a sync

1. **Document library**: a library of the site.
2. **Folder**: the folder to copy; the library root copies the whole library.
3. **Dataset name**: a new dataset in the project root that receives the files.
4. **When**:
    - `Copy once now` copies the folder once.
      A later run, started by hand, adds new and changed files but never deletes.
    - `Keep in sync on a schedule` mirrors the folder on a schedule: every 15 minutes, hourly, daily, weekly, or a custom [Quartz cron expression](https://www.quartz-scheduler.org/documentation/quartz-2.3.0/tutorials/crontrigger.html) in UTC.
      A mirror also deletes files that were deleted in SharePoint.
5. **Alert on failure**: an alert receiver notified when a run fails or is killed.
6. **Index the files in a feature group**: keep a feature group with one row per file; see [The file index](#the-file-index).
   **Feature group** names it; empty means `sharepoint_<dataset>`.
7. Under `Advanced`:
    - **Include** and **Exclude** patterns, in [rclone filter syntax](https://rclone.org/filtering/), one per line.
    - **Maximum file size** in MB; larger files are skipped. `0` copies every file.
    - **Mirror deletions**, to change the default of the option chosen under `When`.
    - **Verify file contents**: compare checksums on every run, or every N runs.
      Other runs compare size and modification time only, so a file changed without a change of either is only picked up by a checksum run.
    - **Parallel transfers**.

The page then opens the data source's `Syncs` tab.

## The data source page

The data source page has three tabs.

- **Connection**: the connection details.
  The cloud, tenant and site cannot change while the data source has syncs.
- **Syncs**: one row per sync, with its library and folder, schedule, state, last run, and number and size of files.
  The row menu offers `Sync now`, `Pause` or `Resume`, `Remove schedule` or `Add schedule`, `Full resync`, `Edit` and `Delete`.
  `Full resync` runs the sync with checksum comparison.
  Below the table, the audit card of the selected sync shows its audit directory, retention, the rows of a day's audit files, and a DuckDB query over them.
- **Code**: the sync script of the data source, described below.

## How a sync runs

### The sync job

Each sync is a Python job named `sharepoint_<data source>_<dataset>`, marked with a `SharePoint sync` badge in the `Jobs` view.
It runs in the `python-feature-pipeline` environment, as the user who started it or, for a scheduled run, the user who created the job.
A run by a user who is not a data owner of the project fails, so when the sync's creator leaves the project, another data owner takes the sync over by editing it.
Its executions, logs, resources and alerts are managed like those of any job.
A run of a sync that is already running exits without copying anything.

### The sync script

All syncs of a data source run the script `DataSources/<data source>/sharepoint_sync.py` in the project.
Hopsworks writes the script when the data source is created and never overwrites it, so data owners can change it, for example to post-process the copied files.
The `Code` tab shows whether the script still matches the platform template, and `Reset to default` restores the template.

### The synced dataset

The synced dataset is a mirror of the SharePoint folder.
The file browser hides the upload, new folder, move, rename and delete actions inside it.
Data owners can still change files in it through the API, but a mirror run puts back what SharePoint has and removes what it does not, so change the files in SharePoint instead.
Deleting, moving or changing the permissions of the dataset itself is refused with error `110057`; change or delete the sync instead.
The dataset can be shared with other projects read-only.
Members of the project can read the dataset like any other.

While a file downloads, rclone writes it as `<name>.<fingerprint>.partial` and renames it when it is complete, so readers may see `.partial` files during a run.
A run that is killed can leave one behind; the next mirror run removes it.

The synced files count against the project's storage quota, which an administrator sets per project; the maximum file size limits each file, not the total.
When the quota is full, the files that do not fit fail, the run is reported as partial with the error `the project's storage quota is full`, and the next run copies them once there is room.

### The audit log

Every run that changes the dataset writes one CSV file:

```text
DataSources/<data source>/audit/<dataset>/date=<YYYY-MM-DD>/<HHMMSS>Z_<execution id>.csv
```

A run that changes nothing writes no file.
Each row is one changed path, relative to the dataset root:

```csv
execution_id,op,kind,path,src_path
812,added,file,Sales/2026/q3.csv,
812,updated,file,Sales/2026/q2.csv,
812,deleted,file,Sales/2025/q4.csv,
812,renamed,file,Sales/2026/q1-final.csv,Sales/2026/q1.csv
812,added,dir,Sales/2027,
```

`op` is `added`, `updated`, `deleted` or `renamed`, `kind` is `file` or `dir`, and `src_path` is the old path of a renamed file.
Files that failed to copy are not listed, since they did not change.

rclone skips OneNote notebooks and shortcuts to other libraries; they are counted as skipped and are not copied.

File and folder names are stored in Unicode NFC form, so a name SharePoint keeps decomposed, as files uploaded from macOS often are, is stored with precomposed letters such as `Å`.
HopsFS stores names in Latin-1, so a name with a character outside it, such as `ł`, `€` or Chinese characters, cannot be copied; the run fails for that file and its error names the file, and renaming it in SharePoint lets the next run copy it.

The `date=` directories are Hive-style partitions, so a filter on `date` reads only the matching days.
From a Python job, with DuckDB from the `python-feature-pipeline` environment:

```python
import duckdb


changes = duckdb.sql(
    """
    SELECT date, execution_id, op, kind, path, src_path
    FROM read_csv('/hopsfs/DataSources/finance_sharepoint/audit/reports/*/*.csv',
                  hive_partitioning = true,
                  columns = {'execution_id': 'BIGINT', 'op': 'VARCHAR',
                             'kind': 'VARCHAR', 'path': 'VARCHAR',
                             'src_path': 'VARCHAR'})
    WHERE date >= DATE '2026-10-19' AND op IN ('added', 'updated')
    """
).df()
```

Each run of a sync deletes the sync's audit days older than `data_source_audit_retention_days`.

### The file index

A sync with indexing on keeps version 1 of a Delta feature group, `sharepoint_<dataset>` by default, with one row per file in the dataset.
The `Syncs` tab links it in the `Index` column once the first run has created it.

| Column | Content |
| --- | --- |
| `file_id` | SharePoint item id, the primary key; it stays the same when the file is renamed or moved |
| `site_id`, `drive_id` | the site and the document library |
| `file_name`, `file_type` | the name, and its extension in lowercase |
| `sharepoint_path`, `web_url` | the path in the library, and a link to the file in SharePoint |
| `hopsfs_path` | the copy in the dataset, `/Projects/<project>/<dataset>/...` |
| `mime_type`, `size_bytes` | content type and size in bytes |
| `created_at`, `modified_at` | SharePoint creation and last modification times, UTC |
| `created_by`, `modified_by` | display names of the author and the last editor |
| `content_hash` | SharePoint's quickXorHash of the content |
| `sync_id`, `execution_id`, `indexed_at` | the sync and the run that last wrote the row, and when |
| `ingestion_date` | the partition: the UTC day the file was first indexed, which is the day it was copied in, or for a file already in the dataset, the day indexing was turned on |

The table holds no file content; the file is in the dataset at `hopsfs_path`.

Each run that does not fail lists the folder with its SharePoint metadata and compares it with the table:

- A file whose copy is in the dataset and that has no row, or whose path, size, modification time, editor or hash changed, is written.
  A new file goes into today's partition; a changed or renamed file keeps the partition of the day it was first indexed.
- A row whose file is gone from both SharePoint and the dataset is deleted, and so is a row whose path now holds another SharePoint file.
  A copy-only sync keeps its files, so it keeps their rows too.
- A file whose copy failed keeps its current row, or gets none, until a run copies it.

A run that stopped at its time budget leaves the index to the next run.
A run that copied its files but could not write the index is reported as partial with the error, and the next run brings the index up to date.

The rows are written and deleted with delta-rs through the feature group's `insert` and `remove_rows`, so each run adds commits to the feature group's activity.
A run that finds a day before today with more than one data file compacts the days from there on into files of about 200 MB, then vacuums files unused for 7 days.
delta-rs 1.4 rewrites a file to delete rows from it and does not write deletion vectors, so the table does not enable them.

Indexing can be turned on for an existing sync: its next run indexes every copied file that is still in the SharePoint folder.
A file a copy-only sync kept after it was deleted in SharePoint has no metadata to index, so it gets no row.
Turning it off keeps the feature group, and a new name starts a new one.
The sync script must be template version 2 or later; reset it to default if the data source page shows an older version.
Deleting the sync deletes the feature group, unless the files are kept.
The name of an index must not be that of an existing feature group, and a sync deletes only the feature group its runs created.

In a terminal, the feature store is mounted at `/hopsfs/featurestore/<project>_featurestore.db/`, and the DuckDB CLI reads the index with its `delta` extension:

```bash
duckdb -c "SELECT file_name, modified_by, modified_at, web_url
FROM delta_scan('/hopsfs/featurestore/acme_featurestore.db/sharepoint_reports_1')
WHERE file_type = 'pdf' ORDER BY modified_at DESC LIMIT 20;"
```

Use `delta_scan`, not `read_parquet` over the partition directories: until a vacuum, those directories also hold the files of deleted and rewritten rows.

### Failures

A run that cannot reach SharePoint, cannot find its folder, or fails in rclone fails its job execution.
A run in which some files fail to copy completes the others, skips deletions, fails its execution, and retries the failed files on the next run.
The sync's `last error` and the execution's logs show the cause, and the alert receiver chosen for the sync is notified.

### Deleting a sync

Deleting a sync deletes its job, schedule and alerts.
By default it also deletes the dataset, the audit log and the index feature group.
With `Keep the files`, the dataset stays as an ordinary dataset, still writable by data owners only, and its audit log is kept and no longer rotated.
A data source with syncs cannot be deleted; delete its syncs first.

## Using the Python client

```python
import hopsworks
from hsfs.storage_connector import SharePointConnector


project = hopsworks.login()
fs = project.get_feature_store()

sharepoint = fs.create_data_source(
    SharePointConnector(
        id=None,
        name="finance_sharepoint",
        featurestore_id=fs.id,
        tenant_id="00000000-0000-0000-0000-000000000000",
        client_id="00000000-0000-0000-0000-000000000000",
        client_secret=hopsworks.get_secrets_api().get_secret("sharepoint").value,
        site_url="https://contoso.sharepoint.com/sites/Finance",
    )
).storage_connector

drive = sharepoint.list_drives()[0]
sharepoint.list_folders(drive_id=drive["id"], path="Reports")

copy = sharepoint.copy_folder(
    drive_id=drive["id"], folder_path="Reports/2025", dataset_name="reports_2025"
)

sync = sharepoint.create_sync(
    drive_id=drive["id"],
    folder_path="Reports/2026",
    dataset_name="reports",
    schedule="0 0 * ? * *",
    include=["*.pdf", "*.xlsx"],
    index_files=True,
)
sync.status()
sync.run()
sync.get_audit()
sync.set_schedule("0 0 2 ? * *")
index = sync.get_index_feature_group()
sync.update(index_files=False)
sync.delete(keep_files=True)
```

`create_sync` creates an hourly schedule unless you pass another `schedule`; `schedule=None` creates a sync that runs only when started.

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-method"></code> [`FeatureStore.create_data_source`][hsfs.feature_store.FeatureStore.create_data_source]
    - <code class="doc-symbol doc-symbol-class"></code> `SharePointConnector`
        - <code class="doc-symbol doc-symbol-method"></code> `list_drives`
        - <code class="doc-symbol doc-symbol-method"></code> `list_folders`
        - <code class="doc-symbol doc-symbol-method"></code> `copy_folder`
        - <code class="doc-symbol doc-symbol-method"></code> `create_sync`
    - <code class="doc-symbol doc-symbol-class"></code> `SharePointSync`
        - <code class="doc-symbol doc-symbol-method"></code> `status`
        - <code class="doc-symbol doc-symbol-method"></code> `run`
        - <code class="doc-symbol doc-symbol-method"></code> `get_audit`
        - <code class="doc-symbol doc-symbol-method"></code> `set_schedule`
        - <code class="doc-symbol doc-symbol-method"></code> `update`
        - <code class="doc-symbol doc-symbol-method"></code> `get_index_feature_group`
        - <code class="doc-symbol doc-symbol-method"></code> `delete`
    - <code class="doc-symbol doc-symbol-docs"></code> [rclone filtering](https://rclone.org/filtering/)

    <a class="hops-api-cta" href="../../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>

## Using the CLI

```bash
export HOPSWORKS_DS_SHAREPOINT_CLIENT_SECRET=<secret value>
hops datasource create sharepoint finance_sharepoint \
  --tenant-id <tenant id> --client-id <client id> \
  --site-url https://contoso.sharepoint.com/sites/Finance
hops datasource sharepoint drives finance_sharepoint
hops datasource sharepoint folders finance_sharepoint --drive <drive id> --path Reports
hops datasource sharepoint copy finance_sharepoint --drive <drive id> --folder Reports/2025 --dataset reports_2025
hops datasource sharepoint sync create finance_sharepoint --drive <drive id> --folder Reports/2026 --dataset reports --cron "0 0 * ? * *" --index-files
hops datasource sharepoint sync index finance_sharepoint <sync id> --off
hops datasource sharepoint sync list finance_sharepoint
hops datasource sharepoint sync audit finance_sharepoint <sync id> --day 2026-10-22
hops datasource sharepoint sync delete finance_sharepoint <sync id> --keep-files
```

`hops datasource sharepoint sync` also has `status`, `run`, `pause`, `resume`, `resync`, `schedule`, `set-folder` and `index`, and `hops datasource sharepoint reset-script` restores the sync script.
