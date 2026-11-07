---
description: How to write dbt semantic models and metrics over feature groups for the Hopsworks Semantic Layer.
---

# Define Metrics over Feature Groups { #semantic-define-metrics }

Metrics are defined in dbt semantic YAML: semantic models that read feature groups, and metrics over the measures of those models.
The examples on this page use two feature groups:

| Feature group | Primary key | Event time | Other features |
| --- | --- | --- | --- |
| `orders` | `order_id` | `order_ts` | `customer_id`, `status` (string), `amount` (double) |
| `customers` | `customer_id` | | `country` (string) |

## Project layout { #semantic-define-layout }

A dbt project has a `dbt_project.yml` at its root, and the semantic layer reads semantic models and metrics from the YAML files under its `model-paths`, `models` when none is given.
Register the folder that holds `dbt_project.yml` as the semantic project's root path.

```text
Resources/semantic/sales/
├── dbt_project.yml
└── models/
    └── semantic.yml
```

`dbt_project.yml`:

```yaml
name: sales
version: "1.0.0"
config-version: 2
profile: hopsworks
model-paths: ["models"]
```

A compile reads every `.yml`, `.yaml` and `.json` file under the root path, except in hidden folders and in the root's `target`, `dbt_packages` and `logs` folders, where dbt writes its output and packages.
It reads at most 1000 such files, each of at most 1 MiB and 32 MiB in all; past that, the build is `INVALID` with a `TOO_MANY_FILES`, `FILE_TOO_LARGE` or `FILES_TOO_LARGE` error.

## Semantic models { #semantic-define-models }

`models/semantic.yml` starts with one semantic model per feature group:

```yaml
version: 2

semantic_models:
  - name: orders
    description: One row per order.
    model: ref('orders')
    defaults:
      agg_time_dimension: order_ts
    entities:
      - name: order
        type: primary
        expr: order_id
      - name: customer
        type: foreign
        expr: customer_id
    dimensions:
      - name: order_ts
        type: time
        type_params:
          time_granularity: day
      - name: status
        type: categorical
    measures:
      - name: revenue
        agg: sum
        expr: amount
      - name: order_count
        agg: count
        expr: order_id

  - name: customers
    description: One row per customer.
    model: ref('customers')
    entities:
      - name: customer
        type: primary
        expr: customer_id
    dimensions:
      - name: country
        type: categorical
```

- **Entities** are the keys of a semantic model.
  Semantic models join on an entity they share: `orders` reaches `customers` through `customer`, the primary entity of `customers`.
  A query joins at most two hops away, and never along a join that would repeat the rows of a measure.
  An entity is `primary`, `unique`, `foreign`, or `natural`, the key of an [SCD Type II][semantic-metric-types-scd] semantic model.
- **Dimensions** are `categorical` or `time`.
  A time dimension needs `type_params.time_granularity`, and its column must be a date or a timestamp.
- **Measures** aggregate an `expr`, a feature or a SQL expression over the features of the feature group.
  Every measure needs a time dimension to aggregate over, from `defaults.agg_time_dimension` or its own `agg_time_dimension`; it becomes the measure's `metric_time`.
  `create_metric: true` on a measure also defines a simple metric with the measure's name, and `non_additive_dimension` makes it [semi-additive][semantic-metric-types-semi-additive].

Each `expr` is checked against the feature group's features at compile time, so a typo in a feature name is an error at its line instead of a failed query.
Names are lower-cased when compiled.

| `agg` | Notes |
| --- | --- |
| `sum`, `min`, `max`, `average` | |
| `count` | Counts the rows where `expr` is not null. |
| `count_distinct` | |
| `sum_boolean` | Counts the rows where `expr` is true. |
| `percentile` | Needs `agg_params.percentile`, strictly between 0 and 1, and `agg_params.use_approximate_percentile: true`. |

Trino computes only approximate continuous percentiles, so a metric over a `median` measure, or over an exact `percentile`, is a `METRIC` error at compile, and one over a percentile with both `use_approximate_percentile` and `use_discrete_percentile` compiles with an `UNSUPPORTED` warning and its queries are refused.
Write a median as a `percentile` measure with `percentile: 0.5` and `use_approximate_percentile: true`.

## Bind a semantic model to a feature group { #semantic-define-binding }

`model: ref('orders')` reads the feature group named `orders`, at its latest version.
A new version of the feature group then changes what the metrics read at the next compile.

`config.meta.hopsworks` names the feature group explicitly, and takes precedence over `ref`:

```yaml
semantic_models:
  - name: customers
    model: ref('customers')
    config:
      meta:
        hopsworks:
          feature_group: customer_profile
          version: 2
```

| Key | Value |
| --- | --- |
| `feature_group` | The feature group to read, when its name differs from the dbt model's. |
| `version` | The version of `feature_group` to read; without it, the latest version. |
| `feature_store` | The feature store that holds the feature group, such as `marketing_featurestore`, for a feature store or feature group shared with the project. Without it, the project's own feature store. |

In the `NATIVE` format, a semantic model names its feature group table with `node_relation`, as `schema_name` and `alias`, such as `sales_featurestore` and `orders_1`.

A semantic model reads a feature group that has an offline table: the project's own, or one shared with the project.
Any other relation is a `RELATION` error.

## Metrics { #semantic-define-metrics-types }

Metrics follow the semantic models in the same file, or in any other YAML file under `model-paths`:

```yaml
metrics:
  - name: revenue
    label: Revenue
    type: simple
    type_params:
      measure: revenue
  - name: orders
    label: Orders
    type: simple
    type_params:
      measure: order_count
  - name: revenue_per_order
    label: Average order value
    description: Revenue divided by orders, the basket size.
    type: ratio
    type_params:
      numerator: revenue
      denominator: orders
  - name: completed_revenue_per_order
    label: Completed revenue per order
    type: derived
    type_params:
      expr: completed_revenue / orders
      metrics:
        - name: revenue
          alias: completed_revenue
          filter: "{{ Dimension('order__status') }} = 'completed'"
        - name: orders
  - name: cancelled_orders
    label: Cancelled orders
    type: simple
    type_params:
      measure: order_count
    filter: "{{ Dimension('order__status') }} = 'cancelled'"
```

| Type | Definition |
| --- | --- |
| `simple` | One measure, `type_params.measure`, or an `expr` aggregated over a semantic model. |
| `ratio` | One metric divided by another, `type_params.numerator` and `type_params.denominator`. |
| `derived` | An `expr` over other metrics, listed in `type_params.metrics`, each with an optional `alias`, `filter` and offset. |
| `cumulative` | A measure aggregated over a window, or since the start of a period, that ends at each period of `metric_time`. |
| `conversion` | The rate or count of the events of one measure that follow an event of another, for the same entity. |

[Metric types][semantic-metric-types] has the YAML of each, and of offsets, `join_to_timespine`, semi-additive measures, SCD Type II dimensions and metric filters.

A `filter` applies to every query of a metric, or to one input of a derived metric.
Filters use the call syntax of queries: `{{ Dimension('order__status') }}`, `{{ TimeDimension('metric_time', 'month') }}`, `{{ Entity('customer') }}`, and `{{ Metric('revenue', group_by=['customer']) }}` for the value of a metric per entity.
The `label` and `description` show in the metric catalog of the UI and in search.

A semantic project also defines [saved queries][semantic-saved-queries], named metric queries, under `saved_queries:`.
The next steps are the [time spine][semantic-time-spine], which cumulative metrics and offsets need, and [compiling the definitions][semantic-compile-builds].
