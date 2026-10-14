# User Guide: Feature and Prediction Logging with a Feature View

Log features and predictions with a feature view, then retrieve them for debugging and monitoring.

## Feature and Prediction Logging

After you have trained a model, you can log the features it uses and the predictions with the feature view used to create the training data for the model.
You can log transformed features, untransformed features, or both.

### Enabling Feature Logging

To enable logging, set `logging_enabled=True` when creating the feature view.
One logging feature group stores transformed features, untransformed features, predictions, and logging metadata together.
Older feature views can retain separate transformed and untransformed logging groups.
The logged features are written to the offline feature store by a materialization job that is created automatically and runs on a schedule.

```python
feature_view = fs.create_feature_view("name", query, logging_enabled=True)
```

Alternatively, you can enable logging on an existing feature view by calling `feature_view.enable_logging()`.
Also, calling `feature_view.log()` will implicitly enable logging if it has not already been enabled.

### Choosing the Transport

A feature view logs through one of two transports, and the layout of its logging feature group follows from the choice.

| Transport | Path of a logged row | Readable |
| --- | --- | --- |
| `realtime` (default) | The deployment posts Arrow batches to its inference logger, which produces them to Kafka; the online store receives them within seconds and the materialization job appends them to the offline store on its schedule | Online at once with `read_log(online=True)` for the group's time to live, offline after materialization |
| `job` | The deployment appends Arrow batches to a file buffer on its pod, rotates the buffer on size or age and uploads it to HopsFS; a scheduled commit job appends the uploaded chunks to an offline-only logging group | Offline after the commit job has run |

A new feature view names its transport when logging is enabled:

```python
feature_view = fs.create_feature_view(
    "name", query, logging_enabled=True, logging_transport="job"
)
feature_view.feature_logging.transport  # "job"
```

A feature view that does not log yet names it when logging is enabled, and the transport is read back from the view:

```python
feature_view.enable_logging(transport="realtime")
feature_view.feature_logging.transport  # "realtime"
```

The two cannot be combined on one feature view: enabling the other transport while the view logs is refused.
To move a view from one transport to the other, drop its log and recreate the logging group for the new transport with `feature_view.delete_log(transport="job")`.
Deployments take the transport from the view; a `DeploymentLoggingConfig` that names a different one is rejected.

The `job` transport keeps no online copy, so `read_log(online=True)` is refused for such a view, and a deployment that stops uploads what its buffer holds and starts the commit job before the pod exits.
Run `deployment.commit_feature_logs()` or `feature_view.materialize_log()` to commit the uploaded chunks on demand, for example after a replica was killed.

### Choosing the Materialization Interval { #choosing-the-materialization-interval }

The materialization job runs every hour or once a day.
The platform default applies unless you choose one, at creation or later.

```python
feature_view = fs.create_feature_view(
    "name", query, logging_enabled=True, logging_materialization_interval="day"
)

feature_view.enable_logging(materialization_interval="hour")

feature_view.set_log_materialization_interval("day")
```

The interval only sets how often logs reach the offline store.
Run `feature_view.materialize_log()` to write them on demand between scheduled runs.
On the `job` transport the interval schedules the commit job instead.

### Logging Features and Predictions

You can log features and predictions by calling `feature_view.log`.
The logged features are written periodically to the offline store.
If you need it to be available immediately, call `feature_view.materialize_log`.

You can log either transformed or/and untransformed features.
To get untransformed features, you can specify `transform=False` in `feature_view.get_batch_data` or `feature_view.get_feature_vector(s)`.
Inference helper columns are returned along with the untransformed features.
If you have On-Demand features as well, call `feature_view.compute_on_demand_features` to get the on demand features before calling `feature_view.log`.To get the transformed features, you can call `feature_view.transform` and pass the untransformed feature with the on-demand feature.

Predictions can be optionally provided as one or more columns in the DataFrame containing the features or separately in the `predictions` argument.
There must be the same number of prediction columns as there are labels in the feature view.
It is required to provide predictions in the `predictions` argument if you provide the features as `list` instead of pandas `dataframe`.
The training dataset version will also be logged if you have called either `feature_view.init_serving(...)` or `feature_view.init_batch_scoring(...)` or if the provided model has a training dataset version.

The wallclock time of calling `feature_view.log` is automatically logged, enabling filtering by logging time when retrieving logs.

#### Example 1: Log Features Only

You have a DataFrame of features you want to log.

```python
import pandas as pd

features = pd.DataFrame(
    {"feature1": [1.1, 2.2, 3.3], "feature2": [4.4, 5.5, 6.6]}
)

# Log features
feature_view.log(features)
```

#### Example 2: Log Features, Predictions, and Model

You can also log predictions, and optionally the training dataset and the model used for prediction.

```python
predictions = pd.DataFrame({"prediction": [0, 1, 0]})

# Log features and predictions
feature_view.log(
    features,
    predictions=predictions,
    training_dataset_version=1,
    model=Model(1, "model", version=1),
)
```

#### Example 3: Log Both Transformed and Untransformed Features

##### Batch Features

```python
untransformed_df = fv.get_batch_data(transformed=False)
# then apply the transformations after:
transformed_df = fv.transform(untransformed_df)
# Log untransformed features
feature_view.log(untransformed_df)
# Log transformed features
feature_view.log(transformed_features=transformed_df)
```

##### Real-time Features

```python
untransformed_vector = fv.get_feature_vector({"id": 1}, transform=False)
# then apply the transformations after:
transformed_vector = fv.transform(untransformed_vector)
# Log untransformed features
feature_view.log(untransformed_vector)
# Log transformed features
feature_view.log(transformed_features=transformed_vector)
```

## Retrieving the Log Timeline

To audit and review the feature/prediction logs, you might want to retrieve the timeline of log entries.
This helps understand when data was logged and monitor the logs.

### Retrieve Log Timeline

A log timeline is the hudi commit timeline of the logging feature group.

```python
# Retrieve the latest 10 log entries
log_timeline = feature_view.get_log_timeline(limit=10)
print(log_timeline)
```

## Reading Log Entries

You may need to read specific log entries for analysis, such as entries within a particular time range or for a specific model version and training dataset version.

### Read all Log Entries

Read all log entries for comprehensive analysis.
The output will return all values of the same primary keys instead of just the latest value.

```python
# Read all log entries
log_entries = feature_view.read_log()
print(log_entries)
```

### Read Log Entries within a Time Range

Focus on logs within a specific time range.
You can specify `start_time` and `end_time` for filtering, but the time columns will not be returned in the DataFrame.
You can provide the `start/end_time` as `datetime`, `date`, `int`, or `str` type.
Accepted date format are: `%Y-%m-%d`, `%Y-%m-%d %H`, `%Y-%m-%d %H:%M`, `%Y-%m-%d %H:%M:%S`, or `%Y-%m-%d %H:%M:%S.%f`

```python
# Read log entries from January 2022
log_entries = feature_view.read_log(
    start_time="2022-01-01", end_time="2022-01-31"
)
print(log_entries)
```

### Read Log Entries by Training Dataset Version

Analyze logs from a particular version of the training dataset.
The training dataset version column will be returned in the DataFrame.

```python
# Read log entries of training dataset version 1
log_entries = feature_view.read_log(training_dataset_version=1)
print(log_entries)
```

### Read Log Entries by Model in Hopsworks

Analyze logs from a particular name and version of the HSML model.
The HSML model column will be returned in the DataFrame.

```python
# Read log entries of a specific HSML model
log_entries = feature_view.read_log(model=Model(1, "model", version=1))
print(log_entries)
```

### Read Log Entries using a Custom Filter

Provide filters which work similarly to the filter method in the `Query` class.
The filter should be part of the query in the feature view.

```python
# Read log entries where feature1 is greater than 0
log_entries = feature_view.read_log(filter=fg.feature1 > 0)
print(log_entries)
```

## Pausing and Resuming Logging

During maintenance or updates, you might need to pause logging to save computation resources.

### Pause Logging

Pause the schedule of the materialization job for writing logs to the offline store.

```python
# Pause logging
feature_view.pause_logging()
```

### Resume Logging

Resume the schedule of the materialization job for writing logs to the offline store.

```python
# Resume logging
feature_view.resume_logging()
```

## Materializing Logs

Besides the scheduled materialization job, you can materialize logs to the offline store on demand.
On the `realtime` transport this reads the rows from Kafka.
On the `job` transport this runs the commit job over the chunks that deployments uploaded to HopsFS.
This does not pause the scheduled job.
Materialization writes all columns of the logging group.
The `transformed` selector applies only to older feature views with separate logging groups.

### Materialize Logs

Materialize logs and optionally wait for the process to complete.

```python
# Materialize logs and wait for completion
materialization_result = feature_view.materialize_log(wait=True)
```

## Monitoring Feature Logging

A deployment that logs through the `realtime` transport reports what its inference logger is doing to Prometheus, and the deployment page shows it.
Open the deployment and look at the Feature logging card.
It shows four panels: rows logged per second by outcome, the time from a post to Kafka's acknowledgement, rows in flight, and posts per second by type and outcome.
The Full dashboard link opens the Feature Logging dashboard in Grafana, filtered to the same deployment, which adds in-flight bytes, rejected posts and totals over the selected range.

Two of these answer most questions.
A non-zero rate of dropped or failed rows means the deployment logs faster than the inference logger can produce, or Kafka is refusing writes; the deployment logs name the reason.
Rejected posts mean the batches the predictor builds do not match the logging group's schema, which happens after the feature view changed without a redeploy.

For a feature view on the `job` transport the card shows the same rows per second and buffered rows, the upload latency of a buffer segment to HopsFS, the bytes awaiting upload and the chunks uploaded per second; the predictor publishes these itself, and the Full dashboard adds commit job triggers and writer restarts.
The card is not shown for a view whose logging still runs through the row path of earlier releases.
Those logs are covered by the commit job's or the materialization job's own execution history instead.

## Deleting Logs

When log data is no longer needed, you might want to delete it to free up space and maintain data hygiene.
This operation deletes the feature groups and recreates new ones.
Scheduled materialization job and log timeline are reset as well.
Pass `transport="realtime"` or `transport="job"` to recreate the logging group for the other transport.

### Delete Logs

Remove all log entries.
The `transformed` selector applies only to older feature views with separate logging groups.

```python
# Delete all log entries
feature_view.delete_log()
```

Restart serving revisions after recreating a logging group so they load its new schema and destination.
