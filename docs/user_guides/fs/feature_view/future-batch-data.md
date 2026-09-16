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
`spine_df` is the set of rows to predict for: one row per entity and moment, carrying the serving keys and the prediction time.
It replaces the root feature group as the anchor of the query, and every feature group is looked up as of each row's own time.

## Retrieving batch data for future timestamps

```python
import datetime

import pandas as pd
from hsfs.constructor.prediction_times import PredictionTimes

tomorrow = datetime.date.today() + datetime.timedelta(days=1)

entities = pd.DataFrame(
    [{"country": "sweden", "city": "stockholm", "street": "sveavagen"}]
)
schedule = PredictionTimes.every("daily", offset="00:00", start=tomorrow, count=7)

batch_data = feature_view.get_batch_data(
    spine_df=schedule.cross(entities, event_time="date"),
)
```

The result has one row per entity per prediction time, so the example returns seven rows.
Rows come back in the order of `spine_df`, and within an entity in prediction-time order, so the frame can be handed to a model and its predictions joined back positionally.

Every feature is taken from the most recent row at or before its prediction time.
For a forecast row dated in the future, that is the forecast for that day.
A feature group with no matching row contributes `NULL` rather than removing the row, the same as any left join, so an entity the feature store has never seen still comes back with the features that do resolve.

## Choosing the entities

`spine_df` accepts a pandas or polars DataFrame, or a list of dictionaries.
Its columns may be:

- the feature view's required serving keys, which identify the entity;
- any column of the root feature group, which is then used as supplied instead of being looked up.

The second kind is the same idea as a passed feature in an online deployment.
If the root feature group holds a `pm25` column and `spine_df` carries one, the value you passed is returned and no lookup is made for it.

Omitting some serving keys is allowed and warns, because a model may be able to infer what is missing.
Omitting all of them is an error: nothing in the feature view can then be looked up, which is a mistake rather than an empty result.
A column that matches neither a serving key nor a root feature is an error naming the columns that are accepted.

## Choosing the timestamps

The frame carries one timestamp per row, under the root feature group's event time column.
Build it yourself if you already have the rows, or let `PredictionTimes` build a schedule and cross it with your entities.
`cross` is worth preferring over rolling your own: it fixes the row order, entities as given and ascending in time within each, which is the order the result comes back in.

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


Times are local, and daylight saving is resolved the way a scheduler resolves it.
A local time that does not exist on the day the clocks go forward is skipped.
A local time that occurs twice on the day they go back is taken at its first occurrence.

!!! note
    The prediction time in the returned frame is the time you asked for, not the event time of the row that matched it.
    A prediction time of 08:00 matching a forecast row written at 00:00 comes back as 08:00.

## Latest feature values for every entity

One row per entity, all at the same instant, is the offline equivalent of `get_feature_vectors`.
Capture the timestamp once so every entity is read at the same moment rather than each drifting.

```python
import datetime

now = datetime.datetime.now(datetime.timezone.utc)

spine = pd.DataFrame({"entity_id": [1, 2, 3]})
spine["event_time"] = now   # named after the root feature group's event time column

latest = feature_view.get_batch_data(spine_df=spine)
```

To cover every entity the feature store knows about rather than a list you maintain, read them
off the feature view's root feature group.
`get_root_fg()` returns the feature group the view is anchored on, and `read_primary_keys()` returns its distinct primary key values, one row per entity.

```python
import datetime
from hsfs.constructor.prediction_times import PredictionTimes

fg = feature_view.get_root_fg()
now = datetime.datetime.now(datetime.timezone.utc)

spine = PredictionTimes.of([now]).cross(fg.read_primary_keys(), event_time=fg.event_time)
latest = feature_view.get_batch_data(spine_df=spine)
```

`read_primary_keys()` returns entities and no time, so it is not a `spine_df` on its own and passing it directly is refused.
Crossing it with one instant is what makes it one.
It reads the key columns of the whole feature group to take the distinct rows, so the cost scales with the feature group rather than with the number of entities, and it returns the root's keys only: a joined feature group keyed on something the root does not carry is not covered by it and comes back `NULL`.

There is no implicit "as of now": the time is always in the frame.
A wall-clock default would make the same call return different rows on a re-run, and a training dataset materialized that way could never be reproduced.
Event times are kept to the millisecond, so sub-millisecond precision in the timestamp you pass is dropped rather than rejected.

## Bounding how stale a feature may be

An as-of lookup carries the last value forward for ever.
If a forecast is missing for one day, that day silently inherits the previous day's weather, and the frame gives no sign of it.

`max_feature_age` bounds how old a matched row may be, relative to the prediction time.
A row older than the bound is returned as `NULL`, so the gap is visible to you and to the model.

```python
# Set when the view is created, so it applies to every read anchored on a spine_df,
# batch inference and training data alike.
feature_view = fs.create_feature_view(
    name="air_quality_fv",
    query=query,
    max_feature_age=datetime.timedelta(days=1),
)

batch_data = feature_view.get_batch_data(spine_df=spine)
```

One bound covers the whole view: every feature group it reads is held to the same limit.
It is read-only after creation and stored with the view.
That is deliberate: if it could be changed per call, a training set and an inference read could be built with different bounds, which is the training/serving skew a feature view exists to prevent.
Read it back with `feature_view.max_feature_age`, which returns a `timedelta` or `None` when the view is unbounded.

## Keys and event time in the result

For a normal `get_batch_data` call, `primary_key` and `event_time` default to `False`.
For a call with `spine_df` they default to `True`, because without the keys and the prediction time the frame does not say which row belongs to which entity or day.
Pass `False` explicitly to leave them out, which is what you want when the model consumes the frame directly.

```python
batch_data = feature_view.get_batch_data(
    spine_df=spine,
    primary_key=False,
    event_time=False,
)
```

!!! note
    When feature groups in the view share a column name, key columns come back fully qualified as `<project>_<feature_group>_<version>_<column>`.
    This is how `get_batch_data` has always named ambiguous key columns; it is not specific to this call.

## Training data from the same rows

The same mechanism builds training data. Pass `spine_df` to `training_data`,
`train_test_split`, `train_validation_test_split` or any of the `create_*` methods, and the
query is anchored on your rows instead of on the root feature group.

```python
train_x, test_x, train_y, test_y = feature_view.train_test_split(
    test_size=0.2,
    spine_df=labels,   # keys, an event time per row, and the label
)
```

One difference from a batch read: columns the feature view does not define are
carried through to the output untouched, which is how the label rides along. A batch read stays
strict about unknown columns, because inference has no labels and a mistyped column there is
worth catching.

`max_feature_age` applies here too, because it belongs to the view rather than to the call.
A training example built from a feature that stopped being produced is the same silent
staleness as an inference row built from one, and it is worse: the model learns from it.

```python
# the view was created with max_feature_age=timedelta(days=1), so any feature whose newest
# row is older than a day carries NULL rather than a stale value
train_x, test_x, train_y, test_y = feature_view.train_test_split(
    test_size=0.2, spine_df=labels
)
```

The label is the caller's own column and is never nulled by the bound.

This is what a spine group does, without having had to create the feature view with one.
`spine_df` and `spine` both replace the left side of the query, so passing both is an error.

!!! note "Materialized training datasets built this way are not reproducible"
    A `create_*` call records the query, not your dataframe, so the dataset cannot be rebuilt
    from its metadata alone. Keep the frame if you need to regenerate it.

## Limits and performance

Offline feature groups only.
Online serving through `get_feature_vector` is unchanged and does not take prediction times.

Both engines are supported.
The Hopsworks Query Service renders each lookup as a DuckDB `ASOF LEFT JOIN`, and Spark renders it as a ranked window over the same rows.
Both return the same frame.

The size of `spine_df` is bounded by cluster limits, which an administrator sets:

| Variable | Bounds |
| --- | --- |
| `featurestore_asof_spine_max_rows` | Rows, meaning entities multiplied by prediction times |
| `featurestore_asof_spine_max_bytes` | The serialized size of those rows |
| `featurestore_asof_spine_max_columns` | Columns in `spine_df` |
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
- `spine_df` cannot be combined with `start_time` and `end_time`.
  The frame's own timestamps define the time axis.
- A feature view created with a spine group uses `spine=` instead; the two cannot be combined.
- A filter on a column the entities supply is refused, because it would drop rows you asked to predict for.
