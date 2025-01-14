# Batch data (analytical ML systems)

## Creation
It is very common that ML models are deployed in a "batch" setting where ML pipelines score incoming new data at a regular interval, for example, daily or weekly. Feature views support batch prediction by returning batch data as a DataFrame over a time range, by `start_time` and `end_time`. The resultant DataFrame (or batch-scoring DataFrame) can then be fed to models to make predictions.

=== "Python"
    ```python
    # get batch data
    df = feature_view.get_batch_data(
        start_time = "20220620",
        end_time = "20220627"
    ) # return a dataframe
    ```
=== "Java"
    ```java
    Dataset<Row> ds = featureView.getBatchData("20220620", "20220627")
    ```

## Retrieve batch data with primary keys and event time
For certain use cases, e.g. time series models, the input data needs to be sorted according to the primary key(s) and event time combination. Or one might want to merge predictions back with the original input data for postmortem analysis.
Primary key(s) and event time are not usually included in the feature view query as they are not features used for training.
To retrieve the primary key(s) and/or event time when retrieving batch data for inference, you need to set the parameters `primary_key=True` and/or `event_time=True`.

=== "Python"
    ```python
    # get batch data
    df = feature_view.get_batch_data(
    start_time = "20220620",
    end_time = "20220627",
    primary_key=True,
    event_time=True
    ) # return a dataframe with primary keys and event time
    ```
!!! note
    All primary and event time columns of all the feature groups included in the feature view will be returned. If they have the same names across feature groups and the join prefix was not provided then reading operation will fail with ambiguous column exception.
    Make sure to define the join prefix if primary key and event time columns have the same names across feature groups.

For Python-clients, handling small or moderately-sized data, we recommend enabling the [ArrowFlight Server with DuckDB](../../../setup_installation/common/arrow_flight_duckdb.md), which will provide significant speedups over Spark/Hive for reading batch data.
If the service is enabled, and you want to read this particular batch data with Hive instead, you can set the read_options to `{"use_hive": True}`.
```python
# get batch data with Hive
df = feature_view.get_batch_data(
    start_time = "20220620",
    end_time = "20220627",
    read_options={"use_hive: True})
)
```

## Creation with transformation
If you have specified transformation functions when creating a feature view, you will get back transformed batch data as well. If your transformation functions require statistics of training dataset, you must also provide the training data version. `init_batch_scoring` will then fetch the statistics and initialize the functions with required statistics. Then you can follow the above examples and create the batch data. Please note that transformed batch data can only be returned in the python client but not in the java client.

```python
feature_view.init_batch_scoring(training_dataset_version=1)
```

It is important to note that in addition to the filters defined in feature view, [extra filters](./training-data.md#Extra-filters) will be applied if they are defined in the given training dataset version.