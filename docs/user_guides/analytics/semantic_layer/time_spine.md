---
description: How to create the time spine feature group of the Hopsworks Semantic Layer, declare it as a dbt time spine model, add custom granularities, and what a compile reports without one.
---

# Time Spine { #semantic-time-spine }

A time spine is a feature group with one row per period, one per day by default.
Cumulative metrics, offsets, `join_to_timespine` and custom granularities join to it, so a period without rows still has a place in the result, and a window or an offset counts periods rather than rows.
Create the feature group once per Hopsworks project, then declare it in each semantic project that needs it.
[Metric types][semantic-metric-types-requirements] lists the metrics that need one.

## Create the time spine { #semantic-time-spine-create }

=== "CLI"

    ```bash
    hops semantic time-spine create --start 2020-01-01 --end 2030-12-31
    ```

    It writes the rows, waits until they are in the offline store, and ends with:

    ```text
    Wrote the day time spine from 2020-01-01 to 2030-12-31 to feature group time_spine_day version 1 (date_day).
    ```

=== "Python"

    ```python
    import hopsworks


    project = hopsworks.login()
    sl = project.get_semantic_layer_api()
    spine = sl.create_time_spine("2020-01-01", "2030-12-31")
    print(spine.name, spine.version)
    ```

    ```text
    time_spine_day 1
    ```

The spine is the offline feature group `time_spine_<grain>`, version 1, with one row per period from the start through the end.
Its primary key `date_<grain>` holds the start of each period: a date for a day or a coarser grain, a timestamp for an hour, a minute or a second.

| Option | Meaning |
| --- | --- |
| `--start` | The first day of the spine, ISO-8601; it moves back to the start of its period. |
| `--end` | The last day of the spine, included. |
| `--grain` | `day` (default), `second`, `minute`, `hour`, `week`, `month`, `quarter` or `year`; weeks start on Monday. |
| `--custom NAME=FREQ` | A custom granularity column, repeatable, see [Custom granularities][semantic-time-spine-custom]. |

Running it again inserts the rows into the existing feature group, so a wider range extends the spine; the custom granularities must be the ones the spine already has.
The spine holds one row per period: ten years are 3,653 days, or 315 million seconds.
Cover the time of every row the metrics read, since a cumulative or offset metric has rows only for the periods the spine has.

## Declare the time spine { #semantic-time-spine-model }

A semantic project declares its time spine as a dbt time spine model, in any YAML file under `model-paths`, such as `models/time_spine.yml`:

```yaml
models:
  - name: time_spine_day
    description: One row per day, written by hops semantic time-spine create.
    time_spine:
      standard_granularity_column: date_day
    columns:
      - name: date_day
        granularity: day
```

`time_spine.standard_granularity_column` names the column with one row per period, and its `granularity` in `columns` is the grain of the spine.
The compile reads YAML only, so the model needs no SQL file.

The model binds the feature group `time_spine_<grain>` of the project's feature store, at its latest version, whatever the model's name.
`config.meta.hopsworks` binds another, with the keys of a [semantic model][semantic-define-binding]:

```yaml
models:
  - name: time_spine_day
    time_spine:
      standard_granularity_column: date_day
    columns:
      - name: date_day
        granularity: day
    config:
      meta:
        hopsworks:
          feature_group: calendar_days
          version: 2
```

In the `NATIVE` format, `project_configuration.time_spines` declares the spine, each with a `primary_column` of a `name` and a `time_granularity`, and its `node_relation` names the feature store of the feature group `time_spine_<grain>`.
Without a `name`, the spine reads the event time of its feature group.

A semantic project can declare one spine per grain.
A metric reads the spine at the grain of its measures' agg time dimension, or a finer one, so measures aggregated by hour need an hourly spine.
A spine binds when its feature group exists, its standard granularity column, or else the feature group's event time, is a date or a timestamp, and it has a column for each custom granularity; otherwise the build has a `TIME_SPINE` warning that says why, at the time spine model.

## Custom granularities { #semantic-time-spine-custom }

A custom granularity is a column of the spine that maps each period to a period of its own, such as a fiscal quarter:

=== "CLI"

    ```bash
    hops semantic time-spine create --start 2020-01-01 --end 2030-12-31 --custom fiscal_quarter=Q-JAN
    ```

    ```text
    Wrote the day time spine from 2020-01-01 to 2030-12-31 to feature group time_spine_day version 1 (date_day, fiscal_quarter).
    ```

=== "Python"

    ```python
    import hopsworks


    project = hopsworks.login()
    sl = project.get_semantic_layer_api()
    sl.create_time_spine(
        "2020-01-01",
        "2030-12-31",
        custom_granularities={
            "fiscal_quarter": "Q-JAN",
            "fiscal_year": lambda day: f"FY{day.year + (day.month > 1)}",
        },
    )
    ```

`FREQ` is a pandas period frequency, and each row holds the start of its period at that frequency, typed like `date_<grain>`.
`Q-JAN` is the quarters of a fiscal year that ends in January, which start on the first of February, May, August and November.
In Python, a callable takes each row's `date_<grain>` and returns the row's value of the column, such as `FY2027`.

The time spine model lists the custom granularities:

```yaml
models:
  - name: time_spine_day
    time_spine:
      standard_granularity_column: date_day
      custom_granularities:
        - name: fiscal_quarter
    columns:
      - name: date_day
        granularity: day
```

Each entry takes a `name`, and a `column_name` when the spine's column has another name.
A query groups by a custom granularity as by a grain:

```bash
hops semantic query sales --metrics revenue --group-by metric_time__fiscal_quarter \
  --order-by metric_time__fiscal_quarter -o csv
```

```text
metric_time__fiscal_quarter,revenue
2025-11-01,220.75
2026-02-01,171.25
```

The orders of January fall in the fiscal quarter that starts on November 1, 2025, and those of February and March in the one that starts on February 1, 2026.
An offset window can count custom granularity periods, such as `offset_window: 1 fiscal_quarter`.
A query that names a granularity no time spine of the semantic project defines is refused with 400 `SEMANTIC_LAYER_INVALID_QUERY`.
[Metric types][semantic-metric-types-limits] lists the queries with custom granularities that are refused.

## Without a time spine { #semantic-time-spine-missing }

A metric that needs a spine at its grain when none is bound is a `TIME_SPINE` error at the metric, so the build is `INVALID`, and the last valid build keeps answering queries.
With `models/cumulative.yml`:

```yaml
metrics:
  - name: revenue_7d
    type: cumulative
    type_params:
      measure: revenue
      cumulative_type_params:
        window: 7 days
```

and no time spine model, the compile reports:

```bash
hops semantic compile sales --wait
```

```text
Build 4: INVALID (1 errors, 0 warnings)
LEVEL  RULE        LOCATION                   ELEMENT            MESSAGE
-----  ----------  -------------------------  -----------------  -----------------------------------------------------------------------------------------------------
ERROR  TIME_SPINE  models/cumulative.yml:2:5  metric:revenue_7d  metric revenue_7d needs a time spine at day grain or finer for a cumulative window, and none is bound
```

The message names what reads the spine: `a cumulative window`, `the offset of input <metric>`, `join_to_timespine`, or a custom granularity.
A spine declared with no feature group to bind adds a `TIME_SPINE` warning at the time spine model, such as `the day time spine is not bound: no feature group time_spine_day in sales_featurestore; metrics that need it cannot be queried`.
Create the spine and compile again.

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-method"></code> [`Project.get_semantic_layer_api`][hopsworks_common.project.Project.get_semantic_layer_api]
    - <code class="doc-symbol doc-symbol-class"></code> [`SemanticLayerApi`][hopsworks_common.core.semantic_layer_api.SemanticLayerApi]
        - <code class="doc-symbol doc-symbol-method"></code> [`create_time_spine`][hopsworks_common.core.semantic_layer_api.SemanticLayerApi.create_time_spine]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>
