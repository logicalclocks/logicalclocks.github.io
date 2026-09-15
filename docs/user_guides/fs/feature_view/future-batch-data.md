# Batch data for future timestamps

## Why a time range is not enough

`get_batch_data(start_time, end_time)` filters the feature view's root feature group, the left-most feature group of its query, and joins the rest onto the rows it finds.
That works whenever the root feature group has an observation for every entity and time you want to score.
It returns nothing for the future, because the future has no observations yet.

An air quality feature view is the common shape.
It joins `air_quality` observations to a `weather` feature group that holds both observations and a forecast.
`get_batch_data(start_time=tomorrow, end_time=tomorrow + 7 days)` returns zero rows, even though `weather` holds all seven forecast days, because `air_quality` holds none of them.
The usual workaround is to read the forecast feature group directly, which loses the feature view's joins, its feature selection and its transformations.

Instead, tell the feature view which rows you want to predict for.
`serving_keys` is the set of entities and `prediction_times` is the set of timestamps.
Their cross product replaces the root feature group as the anchor of the query, and every feature group is looked up as of each prediction time.

## Retrieving batch data for future timestamps

```python
import datetime

import pandas as pd
from hsfs.constructor.prediction_times import PredictionTimes

tomorrow = datetime.date.today() + datetime.timedelta(days=1)

batch_data = feature_view.get_batch_data(
    serving_keys=pd.DataFrame(
        [{"country": "sweden", "city": "stockholm", "street": "sveavagen"}]
    ),
    prediction_times=PredictionTimes.every(
        "daily", offset="00:00", start=tomorrow, count=7
    ),
)
```

The result has one row per entity per prediction time, so the example returns seven rows.
Rows come back in the order of `serving_keys`, and within an entity in prediction-time order, so the frame can be handed to a model and its predictions joined back positionally.

Every feature is taken from the most recent row at or before its prediction time.
For a forecast row dated in the future, that is the forecast for that day.
A feature group with no matching row contributes `NULL` rather than removing the row, the same as any left join, so an entity the feature store has never seen still comes back with the features that do resolve.

## Choosing the entities

`serving_keys` accepts a pandas or polars DataFrame, or a list of dictionaries.
Its columns may be:

- the feature view's required serving keys, which identify the entity;
- any column of the root feature group, which is then used as supplied instead of being looked up.

The second kind is the same idea as a passed feature in an online deployment.
If the root feature group holds a `pm25` column and `serving_keys` carries one, the value you passed is returned and no lookup is made for it.

Omitting some serving keys is allowed and warns, because a model may be able to infer what is missing.
Omitting all of them is an error: nothing in the feature view can then be looked up, which is a mistake rather than an empty result.
A column that matches neither a serving key nor a root feature is an error naming the columns that are accepted.

## Choosing the timestamps

`PredictionTimes` builds the set of timestamps three ways.

```python
from hsfs.constructor.prediction_times import PredictionTimes

# A named interval with an offset. Intervals: hourly, daily, weekly, monthly.
PredictionTimes.every("daily", offset="08:00", start=tomorrow, count=7)
PredictionTimes.every("weekly", offset="mon:09:30", start=tomorrow, count=4)

# A cron expression, in the five-field Vixie dialect, where 0 and 7 are both Sunday.
PredictionTimes.cron("0 8 * * 1-5", start=tomorrow, count=10)

# An explicit list, for a schedule no rule describes.
PredictionTimes.of([datetime.datetime(2026, 3, 1, 8, 0)])
```

A plain list of timestamps is accepted wherever `PredictionTimes` is, so `prediction_times=[t1, t2]` is shorthand for `PredictionTimes.of([t1, t2])`.

Times are local, and daylight saving is resolved the way a scheduler resolves it.
A local time that does not exist on the day the clocks go forward is skipped.
A local time that occurs twice on the day they go back is taken at its first occurrence.

!!! note
    The prediction time in the returned frame is the time you asked for, not the event time of the row that matched it.
    A prediction time of 08:00 matching a forecast row written at 00:00 comes back as 08:00.

## Bounding how stale a feature may be

An as-of lookup carries the last value forward for ever.
If a forecast is missing for one day, that day silently inherits the previous day's weather, and the frame gives no sign of it.

`max_feature_age` bounds how old a matched row may be, relative to the prediction time.
A row older than the bound is returned as `NULL`, so the gap is visible to you and to the model.

```python
batch_data = feature_view.get_batch_data(
    serving_keys=serving_keys,
    prediction_times=PredictionTimes.every(
        "daily", offset="00:00", start=tomorrow, count=7
    ),
    # Per feature group, by name.
    max_feature_age={"weather": datetime.timedelta(days=1)},
)
```

A single `timedelta` bounds every feature group instead of one.
A name that is not a feature group of the feature view is an error rather than a bound that applies to nothing.

## Keys and event time in the result

For a normal `get_batch_data` call, `primary_key` and `event_time` default to `False`.
For a call with `serving_keys` and `prediction_times` they default to `True`, because without the keys and the prediction time the frame does not say which row belongs to which entity or day.
Pass `False` explicitly to leave them out, which is what you want when the model consumes the frame directly.

```python
batch_data = feature_view.get_batch_data(
    serving_keys=serving_keys,
    prediction_times=prediction_times,
    primary_key=False,
    event_time=False,
)
```

!!! note
    When feature groups in the view share a column name, key columns come back fully qualified as `<project>_<feature_group>_<version>_<column>`.
    This is how `get_batch_data` has always named ambiguous key columns; it is not specific to this call.

## Limits and performance

Offline feature groups only.
Online serving through `get_feature_vector` is unchanged and does not take prediction times.

Both engines are supported.
The Hopsworks Query Service renders each lookup as a DuckDB `ASOF LEFT JOIN`, and Spark renders it as a ranked window over the same rows.
Both return the same frame.

The size of the cross product of `serving_keys` and `prediction_times` is bounded by cluster limits, which an administrator sets:

| Variable | Bounds |
| --- | --- |
| `featurestore_asof_spine_max_rows` | Rows, meaning entities multiplied by prediction times |
| `featurestore_asof_spine_max_bytes` | The serialized size of those rows |
| `featurestore_asof_spine_max_columns` | Columns in `serving_keys` |
| `featurestore_asof_spine_max_horizon_days` | How far ahead a schedule may expand |

A request over any of them is refused before it runs, with the limit named.

Without a `lookback`, each feature group is scanned from its first row up to the last prediction time.
The upper bound excludes forecast rows beyond your horizon, but it does not bound history.
On a large feature group, `lookback` is what bounds the work, and `max_feature_age` bounds how many candidate rows each lookup considers.

## Restrictions

- The feature view's joins must be `LEFT` or `INNER`.
  A `RIGHT` or `FULL` join keeps source rows that have no prediction time to align to.
- Feature groups joined through another feature group are not supported.
- Every feature group in the view needs an event time, because an as-of lookup has nothing to order on without one.
- `serving_keys` and `prediction_times` cannot be combined with `start_time` and `end_time`.
  The prediction times define the time axis.
- A feature view created with a spine group uses `spine=` instead; the two cannot be combined.
- A filter on a column the entities supply is refused, because it would drop rows you asked to predict for.
