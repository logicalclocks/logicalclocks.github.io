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

## Creation with transformation
If you have specified transformation functions when creating a feature view, you will get back transformed batch data as well. If your transformation functions require statistics of training dataset, you must also provide the training data version. `init_batch_scoring` will then fetch the statistics and initialize the functions with required statistics. Then you can follow the above examples and create the batch data. Please note that transformed batch data can only be returned in the python client but not in the java client.

```python
feature_view.init_batch_scoring(training_dataset_version=1)
```

