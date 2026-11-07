---
description: How to export a saved query into a feature group that a scheduled job keeps fresh, with full or lookback refreshes, who the job runs as, and what each export status means.
---

# Metric Exports { #semantic-exports }

An export writes the rows of a [saved query][semantic-saved-queries] into a feature group, and a job refreshes them on a schedule or on demand.
Feature views, training data, models and pipelines then read the metrics as any other feature group.
The examples use the `sales` semantic project of [Define metrics][semantic-define-metrics].

## Define an export { #semantic-exports-define }

An export is dbt's `exports:` on a saved query, and its Hopsworks settings go under the saved query's `config.meta.hopsworks.exports`, keyed by the export's name:

```yaml
saved_queries:
  - name: daily_revenue_by_country
    label: Daily revenue by country
    query_params:
      metrics:
        - revenue
        - orders
      group_by:
        - TimeDimension('metric_time', 'day')
        - Dimension('customer__country')
    exports:
      - name: revenue_by_country_daily
        config:
          export_as: table
          alias: revenue_by_country_daily
    config:
      meta:
        hopsworks:
          exports:
            revenue_by_country_daily:
              schedule: "0 0 2 * * ?"
              version: 1
              lookback: 7 days
              enabled: true
```

| Key | Value |
| --- | --- |
| `exports[].name` | The export's name: lower case letters, digits and underscores, starting with a letter, at most 63 characters, unique in the semantic project. |
| `exports[].config.export_as` | `table`. The saved query's own `config.export_as` sets it for all its exports. |
| `exports[].config.alias` | The feature group's name; the export's name when not set. |
| `exports[].config.schema` | Not used: the feature group is created in the project's feature store. |
| `schedule` | A Quartz cron expression with `0` seconds, such as `0 0 2 * * ?` for 02:00 every day. Without it, the export runs only when a Data Owner runs it. |
| `version` | The feature group's version, 1 by default. |
| `lookback` | `<count> <granularity>` with a granularity from `second` to `year`, such as `7 days`, `3 months` or `1 year`: each run replaces only the rows of that window, see [Refreshes][semantic-exports-refresh]. Without it, each run replaces every row. |
| `enabled` | `false` takes the schedule off the export's job and refuses runs; `true` by default. |

Exports compile with the build, and take effect when that build answers queries: at once in `FOLLOW` mode, on a promote in `PINNED` mode, see [Serving modes][semantic-overview-serving-modes].

## Validation { #semantic-exports-validation }

A compile checks every export, and each problem is an issue at the export's file and line, as for any [validation rule][semantic-validation-hopsworks]:

| `RULE` | Level | Reports |
| --- | --- | --- |
| `EXPORT_NAME` | `ERROR` | An export name that is not a feature group name, or that two saved queries define. |
| `EXPORT_AS` | `ERROR` | An export without `export_as`, or with `export_as: view` or anything but `table`. |
| `EXPORT_TARGET` | `ERROR` | A feature group name, the alias or the export's name, that is not valid, or that two exports write; a version below 1. A `WARNING` for a `schema`, which is not used. |
| `EXPORT_SCHEDULE` | `ERROR` | A schedule that is not a Quartz cron expression, is longer than 255 characters, or does not have `0` as its seconds field. |
| `EXPORT_LOOKBACK` | `ERROR` | A lookback that is not `<count> <granularity>` with a count of at least 1, or a saved query that does not group by `metric_time` at a grain, the column the window is cut on. |
| `EXPORT_KEYS` | `ERROR` | A saved query without group-bys: they are the feature group's primary key and event time. |
| `EXPORT_SETTINGS` | `ERROR` | A `config.meta.hopsworks.exports` that does not map export names to settings, or that has settings for a name that is not an export of the saved query. |

## The feature group { #semantic-exports-feature-group }

The export's first run creates the feature group, as the semantic project's creator, and records its id.
For `revenue_by_country_daily`:

| Feature | Type | Role |
| --- | --- | --- |
| `metric_time__day` | timestamp | Event time |
| `customer__country` | string | Primary key |
| `revenue` | double | |
| `orders` | bigint | |

- The features are the saved query's group-bys and metrics, named as the columns of a query.
- The primary key is every group-by except the `metric_time` one, whose column is the event time; when `metric_time` is the only group-by, it is the primary key too.
  A date part, such as `metric_time__extract_dow`, is a key column, not the event time.
- Without a `metric_time` group-by, the feature group has no event time.
- It is a Delta feature group in the offline feature store only, without statistics.
- Its description is the saved query's description, or `Export <export> of saved query <saved query> of semantic project <semantic project>.`
- Each successful run links it to the feature groups the saved query reads as its provenance parents.

Later runs write the feature group the first run created, and no other.
A change of `alias` or `version` points the export at a new feature group, which its next run creates; the old one stays.
A change of the saved query's metrics or group-bys changes the columns, which the existing feature group refuses: raise `version` with it.
A deleted export feature group is created again by the next run.

```python
import hopsworks


project = hopsworks.login()
fs = project.get_feature_store()
fg = fs.get_feature_group("revenue_by_country_daily", version=1)
print(fg.read().head())
```

## Refreshes { #semantic-exports-refresh }

Every run runs the whole saved query, past the [result cache][semantic-result-cache], and replaces rows of the feature group in one commit that keeps the feature group and its id.

| Export | A run replaces |
| --- | --- |
| Without `lookback` | Every row. |
| With `lookback` | The rows whose `metric_time` is at or after the window start; the rows before it stay. |

- The window starts at the run's logical time minus the lookback, truncated to the grain of `metric_time`; weeks start on Monday.
- A scheduled run's logical time is the start of its schedule interval, the schedule's previous fire time.
  The run of `0 0 2 * * ?` at 02:00 on 2026-11-07 has the logical time 2026-11-06 02:00, so with `lookback: 7 days` and a daily `metric_time` it replaces the rows from 2026-10-30 00:00 on.
- A run started by hand takes the start of the schedule's latest complete interval, the logical time of the last scheduled run, or the time it starts when the export has no schedule.
- Groups that vanished from the window are removed, and an empty result empties the window.
- Cumulative and offset metrics in the window see their full history, since the whole saved query runs.
- The first run writes every row.
- A `metric_time` at a custom granularity of the time spine cannot be truncated, so such a run replaces every row and says so in its message.

A run writes nothing when the result reaches the gateway's row cap, `TRUNCATED`, since the rows may be incomplete, or when the target feature group exists and the export did not create it, `TARGET_EXISTS`.

## Who runs an export { #semantic-exports-owner }

Each export has a Python job, `semantic-export-<semantic project id>-<export>`, that Hopsworks creates in the `python-feature-pipeline` environment and keeps in step with the export:

- The job runs as the semantic project's creator, who must be a Data Owner of the project, as creating feature groups needs.
  While the creator is not, the export has no job and its status is `OWNER_NOT_DATA_OWNER`.
- Its script is `SemanticExports/semantic_export.py`, in a dataset that only Data Owners can edit.
- Its schedule is the export's: runs that the schedule missed are not made up, and runs of one export never overlap.
- Hopsworks updates the job right after a build with changed exports starts answering queries, and checks every job every two minutes.
- An export the served build no longer defines loses its job, and its feature group stays; so does a deleted semantic project.

Data Owners and Data Scientists who can edit the YAML can change what an export reads, and the job writes only the export's own feature group.

The job needs the Hopsworks 5.3 library in the `python-feature-pipeline` environment; with an older one, the run fails before writing and the job's log says `update the python-feature-pipeline environment to 5.3`.

## List exports and their status { #semantic-exports-list }

=== "CLI"

    ```bash
    hops semantic export list sales
    ```

    ```text
    NAME                      SAVED QUERY               FEATURE GROUP                SCHEDULE     LOOKBACK  STATUS     LAST RUN              ROWS  MESSAGE
    ------------------------  ------------------------  ---------------------------  -----------  --------  ---------  --------------------  ----  -----------------------------------------------
    revenue_by_country_daily  daily_revenue_by_country  revenue_by_country_daily v1  0 0 2 * * ?  7 days    SUCCEEDED  2026-11-06T02:00:00Z  22    Replaced the rows from 2026-10-30T00:00:00Z on.
    ```

=== "Python"

    ```python
    import hopsworks


    project = hopsworks.login()
    sales = project.get_semantic_layer_api().get_project("sales")
    for export in sales.exports():
        print(export.name, export.feature_group_id, export.last_status, export.last_rows)
    ```

    ```text
    revenue_by_country_daily 501 SUCCEEDED 22
    ```

`LAST RUN` is the last run's logical time, and `ROWS` the rows it wrote: with a lookback, those of the window.
In the UI, the **Exports** card of the semantic project's overview lists each export with its saved query, its feature group, which links to the feature group once a run has created it, its schedule and lookback, or **On demand** and **Full refresh**, its status, its last run and rows, its message, and a link to its job.
The status badge explains the status on hover.
A saved query's sheet lists its exports with their feature groups and statuses under **Exports**.

`hops semantic export list sales --json` prints every field of `SemanticExport`, and the [`list_exports`][semantic-agent-tools-list] tool of the MCP server lists them for an agent.

| Status | Meaning | Fix |
| --- | --- | --- |
| `NEVER_RUN` | No run has reported since the export was defined. | |
| `RUNNING` | A run is going on. A run whose job ended without reporting reads `FAILED`, with `The run ended without reporting a result; see the job's logs`. | |
| `SUCCEEDED` | The last run wrote the rows; the message says which. | |
| `FAILED` | The saved query or the write failed; the message holds the error. | Fix the cause and run again. |
| `TRUNCATED` | The saved query returned as many rows as the gateway's row cap, so the run wrote nothing. | Narrow the saved query with a filter, fewer group-bys or a coarser grain, or raise the `semantic-gateway` value `maxRows`. |
| `TARGET_EXISTS` | A feature group of the target's name and version exists that the export did not create, so the run wrote nothing. | See [Target exists][semantic-exports-target-exists]. |
| `OWNER_NOT_DATA_OWNER` | The semantic project's creator is not a Data Owner, so the export has no job. | Make the creator a Data Owner, or have a Data Owner create the semantic project. |
| `JOB_ERROR` | Hopsworks could not create or update the job; the message says why, and it tries again every two minutes. | Fix the cause, such as a job of the export's name that the export did not create. |
| `DISABLED` | The definition sets `enabled: false`: the job has no schedule and runs are refused. | |

A run that started under an earlier definition of the export reports into the message only, as `A run of an earlier definition of this export (generation <n>) reported <status>`, and leaves the status as it is.

## Run an export now { #semantic-exports-run }

=== "CLI"

    ```bash
    hops semantic export run sales revenue_by_country_daily --wait
    ```

    ```text
    Export revenue_by_country_daily SUCCEEDED: 22 rows. Replaced the rows from 2026-10-30T00:00:00Z on.
    ```

=== "Python"

    ```python
    import hopsworks


    project = hopsworks.login()
    sales = project.get_semantic_layer_api().get_project("sales")
    execution = sales.run_export("revenue_by_country_daily", wait=True)
    print(execution.state)
    ```

This run started at 10:15 on 2026-11-07, and replaced the window of the 02:00 run that day, see [Refreshes][semantic-exports-refresh].
Without `--wait`, the CLI prints `Started export revenue_by_country_daily (execution #42).` and returns.
In the UI, **Run now** on the **Exports** card starts the run; it shows to Data Owners, and is disabled with the reason for an export that cannot run.
Starting a run while another run of the export goes on is refused with `SEMANTIC_LAYER_EXPORT_NOT_RUNNABLE`, naming the execution in progress.

| Error | Code | Status | Meaning |
| --- | --- | --- | --- |
| `SEMANTIC_LAYER_FORBIDDEN` | 590003 | 403 | The caller is not a Data Owner of the project. |
| `SEMANTIC_LAYER_EXPORT_NOT_FOUND` | 590020 | 404 | The build that answers queries defines no export of that name. |
| `SEMANTIC_LAYER_EXPORT_NOT_RUNNABLE` | 590021 | 409 | The export is disabled, its owner is not a Data Owner, Hopsworks has not created its job yet, or a run is in progress; the message says which. |

A run that wrote nothing fails its job execution: with `--wait`, the CLI exits with `The run of export <export> failed: ...` and points to `hops semantic export list`, and `run_export(..., wait=True)` raises `JobExecutionException`.

## Target exists { #semantic-exports-target-exists }

An export writes only a feature group it created, so a feature group of the same name and version that it did not create stops it:

```text
Feature group revenue_by_country_daily version 1 exists and export 'revenue_by_country_daily' did not create it, so nothing was written. Delete it, or give the export another alias or version.
```

The feature group an export creates has `[semantic export <semantic project id>/<export>]` at the end of its description. A run takes over a feature group with its export's mark when the export has none recorded, as after a first run that wrote it but could not report.

- Delete that feature group when nothing needs it, then run the export again.
- Or change the export's `alias` or `version` in the YAML and compile; the next run creates the new feature group.

## Over REST { #semantic-exports-rest }

The exports are under `/hopsworks-api/api/project/<project id>/semantic/projects/<semantic project id>/`:

| Method | Path | Does |
| --- | --- | --- |
| GET | `exports` | Lists the exports of the build that answers queries, with their state. Data Owners and Data Scientists; an API key needs the `FEATURESTORE` scope. |
| POST | `exports/<export>/run` | Starts the export's job and answers `{"jobName", "executionId"}`. Data Owners. |
| PUT | `exports/<export>/status` | The job's report of a run. Accepted only from a running execution of the export's job. |

```json
{
  "items": [
    {
      "name": "revenue_by_country_daily",
      "savedQuery": "daily_revenue_by_country",
      "exportAs": "TABLE",
      "featureGroup": "revenue_by_country_daily",
      "featureGroupId": 501,
      "version": 1,
      "schedule": "0 0 2 * * ?",
      "lookback": "7 days",
      "enabled": true,
      "jobName": "semantic-export-7-revenue_by_country_daily",
      "lastStatus": "SUCCEEDED",
      "lastRun": "2026-11-06T02:00:00Z",
      "lastRows": 22,
      "lastMessage": "Replaced the rows from 2026-10-30T00:00:00Z on."
    }
  ],
  "count": 1
}
```

The gateway's `saved-queries` listing, the `EXPORTS` column of dbt's `semantic_layer.saved_queries()`, and the `exports` field of GraphQL's `savedQueries` carry each saved query's exports too, see [Connect dbt clients][semantic-connect-clients].

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-class"></code> [`SemanticProject`][hopsworks_common.semantic_layer.SemanticProject]
        - <code class="doc-symbol doc-symbol-method"></code> [`exports`][hopsworks_common.semantic_layer.SemanticProject.exports]
        - <code class="doc-symbol doc-symbol-method"></code> [`run_export`][hopsworks_common.semantic_layer.SemanticProject.run_export]
    - <code class="doc-symbol doc-symbol-class"></code> [`SemanticExport`][hopsworks_common.semantic_layer.SemanticExport]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>
