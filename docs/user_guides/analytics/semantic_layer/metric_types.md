---
description: The metric types of the Hopsworks Semantic Layer, simple, ratio, derived, cumulative and conversion, with offsets, filled gaps, semi-additive measures, SCD Type II dimensions, metric filters and metrics without a measure.
---

# Metric Types { #semantic-metric-types }

A metric is `simple`, `ratio`, `derived`, `cumulative` or `conversion`, and its inputs, measures and dimensions change how it aggregates: an offset, a join to the time spine, a semi-additive measure, a dimension with a validity window, a filter on another metric's value.
Each section on this page has the YAML, a query, and its rows.
The examples extend the `sales` semantic project of [Define metrics][semantic-define-metrics] with three more feature groups:

| Feature group | Primary key | Event time | Other features |
| --- | --- | --- | --- |
| `visits` | `visit_id` | `visit_ts` | `customer_id` |
| `balances` | `snapshot_id` | `snapshot_ts` | `customer_id`, `balance` (double) |
| `customer_tiers` | `customer_id`, `valid_from` | | `tier` (string), `valid_to` (date) |

The `orders` feature group has eight orders from January to March 2026, of four customers in `SE`, `DE` and `US`.
The definitions go in any YAML file under `model-paths`, such as `models/metric_types.yml`, next to `models/semantic.yml`.

## Which metrics need metric_time and a time spine { #semantic-metric-types-requirements }

| Metric | Every query groups by `metric_time` | Needs a [time spine][semantic-time-spine] |
| --- | --- | --- |
| `simple` | No | No |
| `ratio`, `derived` | With an input at an `offset_window` or `offset_to_grain` | With an offset |
| `cumulative` | With a `window` or a `grain_to_date` | Yes |
| `conversion` | No | No |
| A measure input with `join_to_timespine: true` | No | Yes |
| A semi-additive measure, an SCD dimension, a `Metric()` filter | No | No |

A metric that reads such a metric, a derived metric over a cumulative one for example, needs `metric_time` too.
`SemanticMetric.requires_metric_time` is set on these metrics, and the query workbench in the UI puts `metric_time` first in the group-bys when one is picked.
The agg time dimension of the metric's measures, such as `order__order_ts__day`, counts as `metric_time`.
A query without either is refused:

```bash
hops semantic query sales --metrics revenue_7d --group-by customer__country
```

```text
Error: Semantic layer request on 'sales' failed (HTTP 400, SEMANTIC_LAYER_INVALID_QUERY): metric revenue_7d accumulates over a window, so the query must group by metric_time or its agg time dimension
```

A metric that needs a time spine fails the compile with a `TIME_SPINE` error when none is bound, see [Without a time spine][semantic-time-spine-missing].

## Simple metrics { #semantic-metric-types-simple }

A simple metric aggregates one measure, `type_params.measure`:

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
```

```bash
hops semantic query sales --metrics revenue,orders --group-by metric_time__month \
  --order-by metric_time__month -o csv
```

```text
metric_time__month,revenue,orders
2026-01-01,220.75,4
2026-02-01,115.5,3
2026-03-01,55.75,1
```

`measure` is a measure's name, or a mapping with its `name` and any of `filter`, `alias`, [`join_to_timespine` and `fill_nulls_with`][semantic-metric-types-fill].

### Metrics without a measure { #semantic-metric-types-measureless }

A simple metric can aggregate its own `expr` over a semantic model, with `type_params.metric_aggregation_params` in place of a measure:

```yaml
metrics:
  - name: large_orders
    label: Orders of 50 or more
    type: simple
    type_params:
      expr: CASE WHEN amount >= 50 THEN 1 ELSE 0 END
      metric_aggregation_params:
        semantic_model: orders
        agg: sum
```

```bash
hops semantic query sales --metrics large_orders --group-by customer__country \
  --order-by customer__country -o csv
```

```text
customer__country,large_orders
DE,1
SE,1
US,2
```

| `metric_aggregation_params` key | Value |
| --- | --- |
| `semantic_model` | The semantic model to aggregate; required. |
| `agg` | An aggregation of [Define metrics][semantic-define-models], such as `sum` or `count_distinct`; required. |
| `agg_params` | `percentile`, `use_discrete_percentile` and `use_approximate_percentile`, as on a measure. |
| `agg_time_dimension` | The time dimension that is the metric's `metric_time`; the semantic model's `defaults.agg_time_dimension` without it. |
| `non_additive_dimension` | As on a [semi-additive measure][semantic-metric-types-semi-additive]. |

Without `expr`, the metric aggregates the feature of its own name.
Cumulative and conversion metrics read such a metric with `cumulative_type_params.metric`, `base_metric` and `conversion_metric` in place of a measure.

## Ratio metrics { #semantic-metric-types-ratio }

A ratio metric divides one metric by another:

```yaml
metrics:
  - name: revenue_per_order
    label: Average order value
    type: ratio
    type_params:
      numerator: revenue
      denominator: orders
```

```bash
hops semantic query sales --metrics revenue_per_order --group-by metric_time__month \
  --order-by metric_time__month -o csv
```

```text
metric_time__month,revenue_per_order
2026-01-01,55.1875
2026-02-01,38.5
2026-03-01,55.75
```

`numerator` and `denominator` are metric names, or mappings with a `name` and any of `filter`, `alias` and an [offset][semantic-metric-types-offsets].
The two metrics are aggregated at the query's group-bys before the division, so a ratio is never an average of ratios.
A ratio is a `DOUBLE`, whatever the types of the two metrics.

## Derived metrics { #semantic-metric-types-derived }

A derived metric is an `expr` over other metrics, listed in `type_params.metrics`, each with an optional `alias` and `filter`:

```yaml
metrics:
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
```

```bash
hops semantic query sales --metrics completed_revenue_per_order --group-by customer__country \
  --order-by customer__country -o csv
```

```text
customer__country,completed_revenue_per_order
DE,7.75
SE,35.0625
US,27.875
```

An `expr` that divides two integers, such as `orders / customers` over two counts, gives a fraction, a `DOUBLE`; a `CAST` the `expr` writes, such as `CAST(orders / customers AS BIGINT)`, sets the type instead.
A division of decimals follows Trino's rule for the type of a decimal quotient.

### Offsets { #semantic-metric-types-offsets }

An input with `offset_window` reads the metric a window earlier, and one with `offset_to_grain` reads it at the start of the period of a grain:

```yaml
metrics:
  - name: revenue_last_month
    label: Revenue a month earlier
    type: derived
    type_params:
      expr: revenue_1_month_ago
      metrics:
        - name: revenue
          alias: revenue_1_month_ago
          offset_window: 1 month
  - name: revenue_change_mom
    label: Revenue change on the month before
    type: derived
    type_params:
      expr: revenue - revenue_1_month_ago
      metrics:
        - name: revenue
        - name: revenue
          alias: revenue_1_month_ago
          offset_window: 1 month
  - name: revenue_first_month_of_quarter
    label: Revenue in the first month of the quarter
    type: derived
    type_params:
      expr: revenue_quarter_start
      metrics:
        - name: revenue
          alias: revenue_quarter_start
          offset_to_grain: quarter
```

```bash
hops semantic query sales --metrics revenue,revenue_last_month,revenue_change_mom \
  --group-by metric_time__month --order-by metric_time__month -o csv
```

```text
metric_time__month,revenue,revenue_last_month,revenue_change_mom
2026-01-01,220.75,,
2026-02-01,115.5,220.75,-105.25
2026-03-01,55.75,115.5,-59.75
2026-04-01,,55.75,
```

```bash
hops semantic query sales --metrics revenue,revenue_first_month_of_quarter \
  --group-by metric_time__month --order-by metric_time__month -o csv
```

```text
metric_time__month,revenue,revenue_first_month_of_quarter
2026-01-01,220.75,220.75
2026-02-01,115.5,220.75
2026-03-01,55.75,220.75
```

- `offset_window` is `<count> <granularity>`, such as `1 month` or `7 days`; `offset_to_grain` is a granularity.
  An input takes one of them, not both.
- The offset input reads the time spine: each period of the spine joins the value of the period the offset names, so April 2026 has the revenue of March and no revenue of its own.
- Metrics in one query are joined on their group-bys, and a metric without a value in a group is empty there: `revenue_change_mom` is empty in January and April, where one of its inputs is.
- A derived or ratio metric with an offset input needs `metric_time` in every query.
- A filter on `metric_time` alone, such as `{{ TimeDimension('metric_time', 'day') }} >= '2026-02-01'`, filters the periods of the time spine, not the rows the offset reads: each queried period that holds a period the filter keeps has one value, read at the offset.
  A filter at a finer grain than the query's, such as a day filter on a monthly query, keeps the months that hold a kept day.
- When the input at an offset is a cumulative metric, a query's time range also bounds the periods that metric is computed for, as in MetricFlow: the first offset's worth of the range has no rows, since the values it reads fall before the range. Start the range one offset earlier to get them.

## Cumulative metrics { #semantic-metric-types-cumulative }

A cumulative metric aggregates a measure over a window that ends at each period of `metric_time`:

```yaml
metrics:
  - name: revenue_7d
    label: Revenue over 7 days
    type: cumulative
    type_params:
      measure: revenue
      cumulative_type_params:
        window: 7 days
  - name: revenue_mtd
    label: Revenue month to date
    type: cumulative
    type_params:
      measure: revenue
      cumulative_type_params:
        grain_to_date: month
        period_agg: last
  - name: revenue_all_time
    label: Revenue to date
    type: cumulative
    type_params:
      measure: revenue
```

```bash
hops semantic query sales --metrics revenue_mtd,revenue_7d --group-by metric_time__day \
  --start-time 2026-02-10 --end-time 2026-02-18 --order-by metric_time__day -o csv
```

```text
metric_time__day,revenue_mtd,revenue_7d
2026-02-10,15.5,15.5
2026-02-11,115.5,115.5
2026-02-12,115.5,115.5
2026-02-13,115.5,115.5
2026-02-14,115.5,115.5
2026-02-15,115.5,115.5
2026-02-16,115.5,115.5
2026-02-17,115.5,100.0
2026-02-18,115.5,
```

The order of 15.50 on February 10 leaves the 7-day window on February 17, and the orders of February 11 leave it on February 18.
The month to date keeps them until the end of February.

| `cumulative_type_params` key | Value |
| --- | --- |
| `window` | `<count> <granularity>`, such as `7 days`: each period aggregates the rows of the window that ends with it. |
| `grain_to_date` | A granularity, such as `month`: each period aggregates the rows since the start of its period of that grain. |
| `period_agg` | `first` (default), `last` or `average`: the value a query coarser than the metric's grain keeps for each of its periods. |
| `metric` | A [simple metric without a measure][semantic-metric-types-measureless] to accumulate, in place of `type_params.measure`. |

Without `window` and `grain_to_date`, the metric accumulates over all time: each period has the total up to it, and a query without `metric_time` has the total of every row.
`window` and `grain_to_date` also read from `type_params`, where older YAML sets them.

A query at a coarser grain than the metric's keeps one value per period, the one `period_agg` picks:

```bash
hops semantic query sales --metrics revenue,revenue_mtd --group-by metric_time__month \
  --order-by metric_time__month -o csv
```

```text
metric_time__month,revenue,revenue_mtd
2026-01-01,220.75,220.75
2026-02-01,115.5,115.5
2026-03-01,55.75,55.75
```

With `period_agg: last`, the month to date of each month is its value on the month's last day.
A cumulative metric has a row for each period of the time spine whose window holds rows, so `period_agg: first` keeps the value of the first such day, January 5 in January.

## Filled gaps: join_to_timespine and fill_nulls_with { #semantic-metric-types-fill }

A measure input with `join_to_timespine: true` has a row for every period of the time spine, and `fill_nulls_with` puts a number in place of an empty value:

```yaml
metrics:
  - name: orders_filled
    label: Orders, zero without any
    type: simple
    type_params:
      measure:
        name: order_count
        join_to_timespine: true
        fill_nulls_with: 0
```

```bash
hops semantic query sales --metrics orders_filled --group-by metric_time__month \
  --start-time 2026-01-01 --end-time 2026-04-30 --order-by metric_time__month -o csv
```

```text
metric_time__month,orders_filled
2026-01-01,4
2026-02-01,3
2026-03-01,1
2026-04-01,0
```

- The join to the time spine applies when the query groups by `metric_time`; without a time range, the rows cover the whole spine, one per period.
- `fill_nulls_with` takes an integer, and applies with or without the join, for example where another metric of the query has a group this one has not.
- Both go on the measure input, or on `type_params` next to `measure` as dbt's newer YAML writes them, and on the inputs of a conversion metric.

## Conversion metrics { #semantic-metric-types-conversion }

A conversion metric counts the events of one measure that follow an event of another, for the same entity, such as the orders that follow a visit.
The examples add a semantic model over `visits`:

```yaml
semantic_models:
  - name: visits
    model: ref('visits')
    defaults:
      agg_time_dimension: visit_ts
    entities:
      - name: visit
        type: primary
        expr: visit_id
      - name: customer
        type: foreign
        expr: customer_id
    dimensions:
      - name: visit_ts
        type: time
        type_params:
          time_granularity: day
    measures:
      - name: visit_count
        agg: count
        expr: visit_id

metrics:
  - name: visit_to_order_rate
    label: Visit to order rate
    type: conversion
    type_params:
      conversion_type_params:
        entity: customer
        base_measure: visit_count
        conversion_measure: order_count
        calculation: conversion_rate
        window: 7 days
  - name: visit_to_order_conversions
    label: Orders within a week of a visit
    type: conversion
    type_params:
      conversion_type_params:
        entity: customer
        base_measure: visit_count
        conversion_measure: order_count
        calculation: conversions
        window: 7 days
```

```bash
hops semantic query sales --metrics visit_to_order_rate,visit_to_order_conversions \
  --group-by metric_time__month --order-by metric_time__month -o csv
```

```text
metric_time__month,visit_to_order_rate,visit_to_order_conversions
2026-01-01,1.0,3.0
2026-02-01,0.6666666666666666,2.0
2026-03-01,,
```

Each order counts once, under the latest visit of its customer at or before it and within the window, and is grouped by that visit's group-bys: its month here.
In January, the two orders of January 5 follow the visit of January 3, and the order of January 6 the visit that day, so 3 visits converted 3 orders.
The only visit in March has no order within a week, so March has no conversions.

| `conversion_type_params` key | Value |
| --- | --- |
| `entity` | The entity both events share, an entity of both semantic models; required. |
| `base_measure`, `conversion_measure` | The two events, each a measure that aggregates with `count`, `count_distinct`, or `sum` of `1`. |
| `base_metric`, `conversion_metric` | A [simple metric without a measure][semantic-metric-types-measureless], in place of each measure. |
| `calculation` | `conversion_rate` (default), conversions over base events, or `conversions`, their count. |
| `window` | `<count> <granularity>`: how long after the base event a conversion counts. Without it, any later conversion counts. |
| `constant_properties` | A list of `base_property` and `conversion_property`, a dimension or entity of each semantic model that both events must agree on, such as the product of the visit and the order. |

The base events read the query's filters, the metric's filter, the filter of the base measure input and the time range, and the conversion events only the filter of the conversion measure input.

## Semi-additive measures { #semantic-metric-types-semi-additive }

A semi-additive measure sums across entities but not across time, such as an account balance: a query keeps only the rows at the first, or last, value of its `non_additive_dimension` in each period.
The examples add a semantic model over `balances`, one row per customer and snapshot:

```yaml
semantic_models:
  - name: balances
    model: ref('balances')
    defaults:
      agg_time_dimension: snapshot_ts
    entities:
      - name: snapshot
        type: primary
        expr: snapshot_id
      - name: customer
        type: foreign
        expr: customer_id
    dimensions:
      - name: snapshot_ts
        type: time
        type_params:
          time_granularity: day
    measures:
      - name: customer_balance
        agg: sum
        expr: balance
        non_additive_dimension:
          name: snapshot_ts
          window_choice: max
          window_groupings:
            - customer
      - name: latest_balance
        agg: sum
        expr: balance
        non_additive_dimension:
          name: snapshot_ts
          window_choice: max

metrics:
  - name: customer_balance
    label: Customer balance
    type: simple
    type_params:
      measure: customer_balance
  - name: latest_balance
    label: Balance on the last snapshot day
    type: simple
    type_params:
      measure: latest_balance
```

```bash
hops semantic query sales --metrics customer_balance,latest_balance \
  --group-by metric_time__month --order-by metric_time__month -o csv
```

```text
metric_time__month,customer_balance,latest_balance
2026-01-01,170.0,170.0
2026-02-01,200.0,170.0
2026-03-01,85.0,85.0
```

In February, one customer's last snapshot is on February 15 and the other three are on February 28.
`customer_balance` takes each customer's last snapshot of the month, and `latest_balance` only the snapshots of the month's last snapshot day, February 28.

| `non_additive_dimension` key | Value |
| --- | --- |
| `name` | A time dimension of the semantic model, at the granularity of the measure's agg time dimension. |
| `window_choice` | `min` (default) keeps the rows at the earliest value in each period, `max` those at the latest. |
| `window_groupings` | Entities of the semantic model to pick the latest or earliest row of separately, such as each customer's. |

## SCD Type II dimensions { #semantic-metric-types-scd }

A semantic model over a slowly changing dimension table, one row per version of an entity with the time each version starts and ends, joins each measure row to the version valid at the row's time.
The examples add `customer_tiers`, the loyalty tier of each customer over time:

| `customer_id` | `tier` | `valid_from` | `valid_to` |
| --- | --- | --- | --- |
| 1 | silver | 2025-06-01 | 2026-01-01 |
| 1 | gold | 2026-01-01 | |
| 2 | silver | 2025-09-01 | |
| 3 | gold | 2025-01-01 | 2026-01-15 |
| 3 | silver | 2026-01-15 | |
| 4 | silver | 2026-02-01 | |

```yaml
semantic_models:
  - name: customer_tiers
    model: ref('customer_tiers')
    primary_entity: customer
    entities:
      - name: customer
        type: natural
        expr: customer_id
    dimensions:
      - name: valid_from
        type: time
        type_params:
          time_granularity: day
          validity_params:
            is_start: true
      - name: valid_to
        type: time
        type_params:
          time_granularity: day
          validity_params:
            is_end: true
      - name: tier
        type: categorical
```

```bash
hops semantic query sales --metrics revenue,orders --group-by customer__tier \
  --order-by customer__tier -o csv
```

```text
customer__tier,revenue,orders
gold,180.5,3
silver,211.5,5
```

Customer 3's order of January 6 counts as gold and its order of February 10 as silver, since the tier changed on January 15.

- The key is an entity of `type: natural`, and the model names it as its `primary_entity`.
- Two time dimensions carry `validity_params`: one `is_start: true`, one `is_end: true`.
  An empty end means the version is still valid.
- A measure row joins the version whose start is at or before the row's agg time, and whose end is after it.
- The model has no measures, no other entity of type `primary` or `unique`, and one natural entity.

## Metric filters { #semantic-metric-types-metric-filters }

`Metric('<metric>', group_by=['<entity>'])` in a filter is the value of a metric for each value of an entity, so a query can keep the rows of the customers whose revenue is over 100:

```bash
hops semantic query sales --metrics revenue,orders --group-by customer__country \
  --where "{{ Metric('revenue', group_by=['customer']) }} > 100" \
  --order-by customer__country -o csv
```

```text
customer__country,revenue,orders
SE,120.5,2
US,125.75,2
```

Of the two customers in `SE`, one has 120.50 of revenue and the other 70.25, so `SE` has the orders of the first only.

The same call goes in a metric's `filter`:

```yaml
metrics:
  - name: big_customer_revenue
    label: Revenue of customers above 100
    type: simple
    type_params:
      measure: revenue
    filter: "{{ Metric('revenue', group_by=['customer']) }} > 100"
```

- `group_by` names exactly one entity, or an entity path such as `order__customer`.
- The metric in the call is computed per entity with its own filters only, not the query's, and joined to the rows on that entity.

## Limits { #semantic-metric-types-limits }

A query of one of these shapes is refused with 400 `SEMANTIC_LAYER_INVALID_QUERY`, and a message that names the shape.
A metric or saved query whose definition has one compiles with an `UNSUPPORTED` warning, and the build serves its other metrics.

- A query without metrics of a dimension that an SCD model joins with its validity window.
- A cumulative metric read at an offset finer than the query's grain, such as an offset of 1 day in a monthly query.
- A semi-additive measure in a cumulative metric, or read at an offset finer than the query's grain.
- An input at an offset that is itself a ratio or derived metric, in a query grouped by a custom granularity, or by `metric_time` only at a date part.
- An input at an offset that is itself a ratio or derived metric, in a query whose grain cannot express the offset, such as an offset of 2 days in a monthly query.
- An input at an offset window in a custom granularity, such as `1 fiscal_quarter`, that is itself a ratio or derived metric.
- A `Metric()` filter that applies to an input at an offset that is itself a ratio or derived metric.
- A filter that combines `metric_time` with another group-by, one of them not a group-by of the query, on an input at an offset that is itself a ratio or derived metric.
- Two custom granularities of the time spine in one query.
- A custom granularity as a metric's `time_granularity`.
- A window in microseconds or nanoseconds.
- A saved query that groups by a metric.

These definitions are compile errors:

- A custom granularity in a cumulative `window` or `grain_to_date`, in a conversion `window`, or in `offset_to_grain`.
- `agg` on the metric itself, dbt's newer YAML spec: a metric without a measure takes `type_params.metric_aggregation_params`.

The [validation rules][semantic-validation-rules] list every check of a compile.
