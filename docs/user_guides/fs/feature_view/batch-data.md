# Batch data (analytical ML systems)

## Creation
It is very common that ML models are deployed in a "batch" setting where ML pipelines score incoming new data at a regular interval, for example, daily or weekly. Feature views support batch prediction by returning batch data as a DataFrame over a time range, by `start_time` and `end_time`. The resultant DataFrame (or batch-scoring DataFrame) can then be fed to models to make predictions.

=== "Python"
    ```python
    import datetime
    start_date = (datetime.datetime.now() - datetime.timedelta(hours=24))
    end_date = (datetime.datetime.now())

    feature_view = fs.get_feature_view("transactions_fv", 1)
    transactions_df = feature_view.get_batch_data(start_time=start_date, end_time=end_date)
    ```


## Creation with transformation
If you have specified transformation functions when creating a feature view, you will get back transformed batch data as well. If your transformation functions require statistics of training dataset, you must also provide the training data version. `init_batch_scoring` will then fetch the statistics and initialize the functions with required statistics. Then you can follow the above examples and create the batch data. Please note that transformed batch data can only be returned in the python client but not in the java client.

```python
feature_view.init_batch_scoring(training_dataset_version=1)
```

It is important to note that in addition to the filters defined in feature view, [extra filters](./training-data.md#Extra-filters) will be applied if they are defined in the given training dataset version.
