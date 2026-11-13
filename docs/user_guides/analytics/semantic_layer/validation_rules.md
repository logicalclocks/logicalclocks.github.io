---
description: Reference of the checks a semantic project's compile runs, MetricFlow's validation rules and the Hopsworks rules, with the rule name each issue carries and what it reports.
---

# Validation Rules { #semantic-validation-rules }

A compile checks the definitions with MetricFlow's 28 validation rules, then with the Hopsworks rules, which bind them to feature groups and plan every metric.
Each problem is an issue with a level, a rule, the file, line and column, and the element, as [Compile and builds][semantic-builds-compile] shows.
An `ERROR` makes the build `INVALID`, so the last valid build keeps answering queries; a `WARNING` does not.

## MetricFlow rules { #semantic-validation-metricflow }

The rules of MetricFlow's default validator, in its order, with the `RULE` their issues carry.
Every issue is an `ERROR` unless the table says `WARNING`.

| MetricFlow rule | `RULE` | Reports |
| --- | --- | --- |
| PercentileAggregationRule | `PERCENTILE` | A `percentile` measure without `agg_params.percentile`, or with one that is not strictly between 0 and 1; a `median` measure with another percentile or `use_discrete_percentile`; percentile parameters on another aggregation. |
| DerivedMetricRule | `DERIVED_METRIC` | An alias used by two inputs, an input with both `offset_window` and `offset_to_grain`, a custom granularity in `offset_to_grain`; a `WARNING` for an input that `expr` does not use. |
| CountAggregationExprRule | `COUNT_EXPR` | A `count` measure without `expr`, or whose `expr` starts with `distinct`; use `count_distinct` for that. |
| SemanticModelMeasuresUniqueRule | `UNIQUE_NAMES` | A measure name defined in two semantic models. |
| SemanticModelValidityWindowRule | `VALIDITY_WINDOW` | Validity parameters other than one `is_start` and one `is_end` time dimension; a validity window without a natural entity, with a primary or unique entity, or with measures. |
| DimensionConsistencyRule | `DIMENSION_CONSISTENCY` | A dimension name with another type, or another `is_partition`, in another semantic model. |
| ElementConsistencyRule | `ELEMENT_CONSISTENCY` | A name that is a measure, a dimension or an entity in one semantic model and another kind of element in another. |
| NaturalEntityConfigurationRule | `NATURAL_ENTITY` | More than one natural entity in a semantic model, or one without a validity window. |
| MeasureConstraintAliasesRule | `MEASURE_ALIAS` | A metric that reads differently filtered versions of a measure without aliasing them; an alias that names a measure, or that another metric uses. |
| MetricMeasuresRule | `REFERENCE` | A metric that reads a measure no semantic model defines. |
| CumulativeMetricRule | `CUMULATIVE_METRIC` | Both `window` and `grain_to_date`; a `window` given twice with different values; a custom granularity in `window` or `grain_to_date`; an input metric that is not simple. A `WARNING` for both a measure and a metric as input. |
| NonEmptyRule | `EMPTY` | No semantic models; a `WARNING` for no metrics. |
| UniqueAndValidNameRule | `NAMING`, `UNIQUE_NAMES` | A name that is not lower case letters, digits and underscores starting with a letter, is shorter than two characters, ends with `_`, contains `__`, is a granularity or is `metric_time`; a name defined twice; two elements of a semantic model with one name; a custom granularity with the name of another element. |
| AggregationTimeDimensionRule | `AGG_TIME_DIMENSION` | A measure without an agg time dimension, declared or from the [event time][semantic-define-event-time] of its feature group, or with one that is not a time dimension of its semantic model. |
| ReservedKeywordsRule | `RESERVED_KEYWORD` | An entity, dimension or measure, or a part of a `node_relation`, named with an SQL reserved keyword, such as `select` or `from`. |
| MeasuresNonAdditiveDimensionRule | `NON_ADDITIVE_DIMENSION` | A `non_additive_dimension` that is not a time dimension of the semantic model, or not at the granularity of the measure's agg time dimension; `window_groupings` that are not entities of the semantic model. |
| SemanticModelDefaultsRule | `AGG_TIME_DIMENSION` | A `defaults.agg_time_dimension` that is not a time dimension of the semantic model. |
| PrimaryEntityRule | `PRIMARY_ENTITY` | Two primary entities; an entity of type `primary` and `primary_entity` both; dimensions without a primary entity. |
| PrimaryEntityDimensionPairs | `PRIMARY_ENTITY_DIMENSION` | Two semantic models with the same primary entity and a dimension of the same name, which one group-by name would reach in both. |
| WhereFiltersAreParseable | `WHERE_FILTER` | A filter of a metric, an input or a saved query that does not parse. A `WARNING` for a filter that names an unknown granularity, or one that cannot be applied. |
| SavedQueryRule | `SAVED_QUERY` | A saved query metric that does not exist; a group-by that does not parse or is not a metric, `metric_time`, a dimension or an entity; an order-by that is none of its metrics and group-bys; a negative limit. |
| MetricLabelsRule | `LABELS` | Two metrics with the same label. |
| SemanticModelLabelsRule | `LABELS` | Two semantic models with the same label; two dimensions, entities or measures of a semantic model with the same label. |
| EntityLabelsRule | `LABELS` | An entity with different labels in different semantic models. |
| ConversionMetricRule | `CONVERSION_METRIC` | An entity that is not an entity of both semantic models; an input that does not aggregate with `count`, `count_distinct` or `sum` of `1`; a constant property that is not a dimension or entity of its semantic model; a custom granularity in `window`; an input metric that is not simple. A `WARNING` for a filter on the conversion input, and for both a measure and a metric as input. |
| TimeSpineRule | `TIME_SPINE` | Only `WARNING`s, with a time spine declared: two time spines of one granularity, no time dimensions, or a finest time spine coarser than the finest agg time dimension of the measures. |
| TimeDimensionHasGranularityRule | `TIME_DIMENSION` | A time dimension without `type_params.time_granularity`. |
| SimpleMetricExprRule | `SIMPLE_METRIC_EXPR` | A `WARNING` for a simple metric that reads a measure and sets an `expr` of its own, which is ignored. |

## Hopsworks rules { #semantic-validation-hopsworks }

| `RULE` | Level | Reports |
| --- | --- | --- |
| `TOO_MANY_FILES`, `FILE_TOO_LARGE`, `FILES_TOO_LARGE` | `ERROR` | More than 1000 files under the root path, a file over 1 MiB, or files over 32 MiB in all, see [Project layout][semantic-define-layout]. |
| `TOO_MANY` | `ERROR` | More elements of one kind than a semantic project may define, see [Limits][semantic-validation-limits], at the first element over the limit; nothing after it is read. |
| `TOO_MANY_ISSUES` | `ERROR`, `WARNING` | More than 1,000 errors or 1,000 warnings: the first 1,000 of each are listed, then one issue says how many more were found. An `ERROR` also when the issues take more room than a build stores, 4 MiB; the leading issues are kept and the build is `INVALID`. |
| `ANSWER_TOO_LARGE` | `ERROR` | The compile's answer, which holds the definition files and every issue found in them, is larger than 64 MiB, or 8 MiB for the editor's validation. Fix the definitions that repeat an error, or split them over more than one semantic project. |
| `YAML_SYNTAX` | `ERROR` | A file that does not parse as YAML or JSON. |
| `YAML_DUPLICATE_KEY` | `WARNING` | A key twice in one mapping; the last value is used. |
| `UNKNOWN_KEY` | `WARNING` | A top-level key the format does not define. |
| `REQUIRED` | `ERROR` | A required key left out, such as a metric's `type` or a simple metric's `measure`. |
| `TYPE` | `ERROR` | A value of the wrong type, or an unknown aggregation, granularity, entity type, metric type or window. |
| `MODEL_REF` | `ERROR` | A `model` that is not `ref('<name>')`, or a semantic model with none of `model`, `node_relation` and `config.meta.hopsworks.feature_group`. |
| `FILTER` | `ERROR` | A `filter` that is neither a string nor a list of strings. |
| `REFERENCE` | `ERROR` | A metric, measure or semantic model a definition names and none defines. |
| `PHASE` | `ERROR` | `agg` on the metric itself, dbt's newer YAML spec; a metric without a measure takes `type_params.metric_aggregation_params`. |
| `METRIC_AGGREGATION_PARAMS` | `WARNING` | A simple metric with both `metric_aggregation_params` and a measure; the measure is ignored. |
| `CYCLE` | `ERROR` | Metrics that read each other in a cycle. |
| `RELATION` | `ERROR` | A semantic model whose feature group does not exist, or is in a feature store neither the project's nor shared with it. |
| `EXPR` | `ERROR` | An `expr` that does not compile against the feature group's features, such as a feature name with a typo. |
| `TIME_DIMENSION` | `ERROR` | A time dimension whose feature is not a date or a timestamp. |
| `EVENT_TIME` | `WARNING` | A feature group event time that cannot be linked to a time dimension of a semantic model, see [Event time][semantic-define-event-time]. |
| `TIME_SPINE` | `ERROR` | A metric that needs a time spine none is bound for, see [Without a time spine][semantic-time-spine-missing]. A `WARNING` for a declared time spine that does not bind. |
| `METRIC` | `ERROR` | A metric that the planner cannot plan, with the planner's reason, such as an exact percentile on Trino. |
| `SAVED_QUERY` | `ERROR` | A saved query that the planner cannot plan, with the planner's reason. |
| `NAME_TOO_LONG` | `ERROR` | A metric or saved query name longer than 255 characters. |
| `UNSUPPORTED` | `WARNING` | A metric or saved query of a shape the planner refuses, see [Limits][semantic-metric-types-limits]; its queries are refused, and the build serves the others. |
| `METRIC_TAGS_NOT_A_MAP`, `METRIC_TAG_UNKNOWN_SCHEMA`, `METRIC_TAG_INVALID_VALUE`, `METRIC_TAG_MANDATORY_MISSING` | `ERROR` | A metric's tags, see [Tag a metric][semantic-tags-metrics]. |
| `SAVED_QUERY_TAGS_NOT_A_MAP`, `SAVED_QUERY_TAG_UNKNOWN_SCHEMA`, `SAVED_QUERY_TAG_INVALID_VALUE` | `ERROR` | A saved query's tags, checked as a metric's are. |
| `EXPORT_NAME` | `ERROR` | An export name that is not a feature group name, lower case letters, digits and underscores starting with a letter and at most 63 characters, or that two saved queries define. |
| `EXPORT_AS` | `ERROR` | An export without `export_as`, or with `export_as: view` or anything but `table`. |
| `EXPORT_TARGET` | `ERROR` | An export's feature group name, its `alias` or else its name, that is not a valid feature group name or that two exports write; a `version` below 1. A `WARNING` for a `schema`, which is not used. |
| `EXPORT_SCHEDULE` | `ERROR` | A `schedule` that is not a Quartz cron expression, is longer than 255 characters, or does not have `0` as its seconds field. |
| `EXPORT_LOOKBACK` | `ERROR` | A `lookback` that is not `<count> <granularity>` with a count of at least 1, such as `7 days`, or an export with a lookback whose saved query does not group by `metric_time` at a grain. |
| `EXPORT_KEYS` | `ERROR` | An export of a saved query without group-bys. |
| `EXPORT_SETTINGS` | `ERROR` | A `config.meta.hopsworks.exports` that does not map export names to settings, or that names an export the saved query does not have. |
| `EXPORT_SERVING` | `WARNING` | A saved query with exports whose rows can depend on when it runs, through `CURRENT_DATE`, `now()` or a function the compiler does not know, such as a UDF, in a filter or expression: its exports are refreshed, and never [answer queries][semantic-exports-serving-rules]. |

The `EXPORT_*` rules check the [metric exports][semantic-exports-validation] of saved queries.

## Limits { #semantic-validation-limits }

A semantic project defines at most, over all its files:

| Element | Most |
| --- | --- |
| Semantic models | 1,000 |
| Entities | 10,000 |
| Dimensions | 20,000 |
| Measures | 10,000 |
| Metrics | 10,000 |
| Saved queries | 1,000 |
| Exports | 1,000 |
| Time spines | 100 |

The first element over a limit is a `TOO_MANY` error at its file and line, and the compile reads nothing after it.
A compile lists at most 1,000 errors and 1,000 warnings, and stops once it has found more than 1,000 errors; a build's error and warning counts count every issue found, and can be larger than the list.
The files under the root path are limited too, see [Project layout][semantic-define-layout].

`hops semantic build <name> <id>`, `SemanticProject.get_build(id).issues` and **View issues** on the **Builds** card list a build's issues.
