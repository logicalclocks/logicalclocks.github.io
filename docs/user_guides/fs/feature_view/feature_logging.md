# User Guide: Feature and Prediction Logging with a Feature View

Feature logging is essential for debugging, monitoring, and auditing the data your models use. This guide explains how to log features and predictions, and retrieve and manage these logs with feature view in Hopsworks.

## Logging Features and Predictions

After you have trained a model, you can log the features it uses and the predictions with the feature view used to create the training data for the model. You can log either transformed or/and untransformed features values.

### Enabling Feature Logging

To enable logging, set `logging_enabled=True` when creating the feature view. Two feature groups will be created for storing transformed and untransformed features, but they are not visible in the UI. The logged features will be written to the offline feature store every hour by scheduled materialization jobs which are created automatically.

```python
feature_view = fs.create_feature_view("name", query, logging_enabled=True)
```

Alternatively, you can enable logging on an existing feature view by calling `feature_view.enable_logging()`. Also, calling `feature_view.log()` will implicitly enable logging if it has not already been enabled.

### Logging Features and Predictions

You can log features and predictions by calling `feature_view.log`. The logged features are written periodically to the offline store. If you need it to be available immediately, call `feature_view.materialize_log`.

You can log either transformed or/and untransformed features. To get untransformed features, you can specify `transform=False` in `feature_view.get_batch_data` or `feature_view.get_feature_vector(s)`. Inference helper columns are returned along with the untransformed features. If you have On-Demand features as well, call `feature_view.compute_on_demand_features` to get the on demand features before calling `feature_view.log`.To get the transformed features, you can call `feature_view.transform` and pass the untransformed feature with the on-demand feature.

Predictions can be optionally provided as one or more columns in the DataFrame containing the features or separately in the `predictions` argument. There must be the same number of prediction columns as there are labels in the feature view. It is required to provide predictions in the `predictions` argument if you provide the features as `list` instead of pandas `dataframe`. The training dataset version will also be logged if you have called either `feature_view.init_serving(...)` or `feature_view.init_batch_scoring(...)` or if the provided model has a training dataset version.

The wallclock time of calling `feature_view.log` is automatically logged, enabling filtering by logging time when retrieving logs.

#### Example 1: Log Features Only

You have a DataFrame of features you want to log.

```python
import pandas as pd

features = pd.DataFrame({
    "feature1": [1.1, 2.2, 3.3],
    "feature2": [4.4, 5.5, 6.6]
})

# Log features
feature_view.log(features)
```

#### Example 2: Log Features, Predictions, and Model

You can also log predictions, and optionally the training dataset and the model used for prediction.

```python
predictions = pd.DataFrame({
    "prediction": [0, 1, 0]
})

# Log features and predictions
feature_view.log(features, 
                 predictions=predictions, 
                 training_dataset_version=1, 
                 model=Model(1, "model", version=1)
)
```

#### Example 3: Log Both Transformed and Untransformed Features

**Batch Features**
```python
untransformed_df = fv.get_batch_data(transformed=False)
# then apply the transformations after:
transformed_df = fv.transform(untransformed_df)
# Log untransformed features
feature_view.log(untransformed_df)
# Log transformed features
feature_view.log(transformed_df, transformed=True)
```

**Real-time Features**
```python
untransformed_vector = fv.get_feature_vector({"id": 1}, transform=False)
# then apply the transformations after:
transformed_vector = fv.transform(untransformed_vector)
# Log untransformed features
feature_view.log(untransformed_vector)
# Log transformed features
feature_view.log(transformed_vector, transformed=True)
```

## Retrieving the Log Timeline

To audit and review the feature/prediction logs, you might want to retrieve the timeline of log entries. This helps understand when data was logged and monitor the logs.

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

Read all log entries for comprehensive analysis. The output will return all values of the same primary keys instead of just the latest value.

```python
# Read all log entries
log_entries = feature_view.read_log()
print(log_entries)
```

### Read Log Entries within a Time Range

Focus on logs within a specific time range. You can specify `start_time` and `end_time` for filtering, but the time columns will not be returned in the DataFrame. You can provide the `start/end_time` as `datetime`, `date`, `int`, or `str` type. Accepted date format are: `%Y-%m-%d`, `%Y-%m-%d %H`, `%Y-%m-%d %H:%M`, `%Y-%m-%d %H:%M:%S`, or `%Y-%m-%d %H:%M:%S.%f`

```python
# Read log entries from January 2022
log_entries = feature_view.read_log(start_time="2022-01-01", end_time="2022-01-31")
print(log_entries)
```

### Read Log Entries by Training Dataset Version

Analyze logs from a particular version of the training dataset. The training dataset version column will be returned in the DataFrame.

```python
# Read log entries of training dataset version 1
log_entries = feature_view.read_log(training_dataset_version=1)
print(log_entries)
```

### Read Log Entries by Model in Hopsworks

Analyze logs from a particular name and version of the HSML model. The HSML model column will be returned in the DataFrame.

```python
# Read log entries of a specific HSML model
log_entries = feature_view.read_log(model=Model(1, "model", version=1))
print(log_entries)
```

### Read Log Entries using a Custom Filter

Provide filters which work similarly to the filter method in the `Query` class. The filter should be part of the query in the feature view.

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

Besides the scheduled materialization job, you can materialize logs from Kafka to the offline store on demand. This does not pause the scheduled job. By default, it materializes both transformed and untransformed logs, optionally specifying whether to materialize transformed (transformed=True) or untransformed (transformed=False) logs.

### Materialize Logs

Materialize logs and optionally wait for the process to complete.

```python
# Materialize logs and wait for completion
materialization_result = feature_view.materialize_log(wait=True)
# Materialize only transformed log entries
feature_view.materialize_log(wait=True, transformed=True)
```

## Deleting Logs

When log data is no longer needed, you might want to delete it to free up space and maintain data hygiene. This operation deletes the feature groups and recreates new ones. Scheduled materialization job and log timeline are reset as well.

### Delete Logs

Remove all log entries (both transformed and untransformed logs), optionally specifying whether to delete transformed (transformed=True) or untransformed (transformed=False) logs. 

```python
# Delete all log entries
feature_view.delete_log()

# Delete only transformed log entries
feature_view.delete_log(transformed=True)
```

## Summary

Feature logging is a crucial part of maintaining and monitoring your machine learning workflows. By following these examples, you can effectively log, retrieve, and delete logs, as well as manage the lifecycle of log materialization jobs, adding observability for your AI system and making it auditable.