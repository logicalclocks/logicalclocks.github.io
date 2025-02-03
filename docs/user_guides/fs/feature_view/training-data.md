# Training data

Training data can be created from the feature view and used by different ML libraries for training different models.

You can read [training data concepts](../../../concepts/fs/feature_view/offline_api.md) for more details. To see a full example of how to create training data, you can read [this notebook](https://github.com/logicalclocks/hopsworks-tutorials/blob/master/batch-ai-systems/fraud_batch/2_fraud_batch_training_pipeline.ipynb).

For Python-clients, handling small or moderately-sized data, we recommend enabling the [ArrowFlight Server with DuckDB](../../../setup_installation/common/arrow_flight_duckdb.md) service,
which will provide significant speedups over Spark/Hive for reading and creating in-memory training datasets.

## Creation
It can be created as in-memory DataFrames or materialised as `tfrecords`, `parquet`, `csv`, or `tsv` files to HopsFS or in all other locations, for example, S3, GCS. If you materialise a training dataset, a `PySparkJob` will be launched. By default, `create_training_data` waits for the job to finish. However, you can run the job asynchronously by passing `write_options={"wait_for_job": False}`. You can monitor the job status in the [jobs overview UI](../../projects/jobs/pyspark_job.md#step-1-jobs-overview). 

```python
# create a training dataset as dataframe
feature_df, label_df = feature_view.training_data(
    description = 'transactions fraud batch training dataset',
)

# materialise a training dataset
version, job = feature_view.create_training_data(
    description = 'transactions fraud batch training dataset',
    data_format = 'csv',
    write_options = {"wait_for_job": False}
) # By default, it is materialised to HopsFS
print(job.id) # get the job's id and view the job status in the UI
```


### Extra filters
Sometimes data scientists need to train different models using subsets of a dataset. For example, there can be different models for different countries, seasons, and different groups. One way is to create different feature views for training different models. Another way is to add extra filters on top of the feature view when creating training data.

In the [transaction fraud example](https://github.com/logicalclocks/hopsworks-tutorials/blob/master/batch-ai-systems/fraud_batch/1_fraud_batch_feature_pipeline.ipynb), there are different transaction categories, for example: "Health/Beauty", "Restaurant/Cafeteria", "Holliday/Travel" etc. Examples below show how to create training data for different transaction categories.
```python
# Create a training dataset for Health/Beauty
df_health = feature_view.training_data(
    description = 'transactions fraud batch training dataset for Health/Beauty',
    extra_filter = trans_fg.category == "Health/Beauty"
)
# Create a training dataset for Restaurant/Cafeteria and Holliday/Travel
df_restaurant_travel = feature_view.training_data(
    description = 'transactions fraud batch training dataset for Restaurant/Cafeteria and Holliday/Travel',
    extra_filter = trans_fg.category == "Restaurant/Cafeteria" and trans_fg.category == "Holliday/Travel"
)
```


### Train/Validation/Test Splits
In most cases, ML practitioners want to slice a dataset into multiple splits, most commonly train-test splits or train-validation-test splits, so that they can train and test their models. Feature view provides a sklearn-like API for this purpose, so it is very easy to create a training dataset with different splits.

Create a training dataset (as in-memory DataFrames) or materialise a training dataset with train and test splits.
```python
# create a training dataset 
X_train, X_test, y_train, y_test = feature_view.train_test_split(test_size=0.2)

# materialise a training dataset
version, job = feature_view.create_train_test_split(
    test_size = 0.2,
    description = 'transactions fraud batch training dataset',
    data_format = 'csv'
)
```

Create a training dataset (as in-memory DataFrames) or materialise a training dataset with train, validation, and test splits.
```python
# create a training dataset as DataFrame
X_train, X_val, X_test, y_train, y_val, y_test = feature_view.train_validation_test_split(validation_size=0.3, test_size=0.2)

# materialise a training dataset
version, job = feature_view.create_train_validation_test_split(
    validation_size = 0.3, 
    test_size = 0.2
    description = 'transactions fraud batch training dataset',
    data_format = 'csv'
)
```

If the [ArrowFlight Server with DuckDB](../../../setup_installation/common/arrow_flight_duckdb.md) service is enabled,
and you want to create a particular in-memory training dataset with Hive instead, you can set `read_options={"use_hive": True}`.
```python
# create a training dataset as DataFrame with Hive
X_train, X_test, y_train, y_test = feature_view.train_test_split(test_size=0.2, read_options={"use_hive: True})
```

## Read Training Data
Once you have created a training dataset, all its metadata are saved in Hopsworks. This enables you to reproduce exactly the same dataset at a later point in time. This holds for training data as both DataFrames or files. That is, you can delete the training data files (for example, to reduce storage costs), but still reproduce the training data files later on if you need to.
```python
# get a training dataset
feature_df, label_df = feature_view.get_training_data(training_dataset_version=1)

# get a training dataset with train and test splits
X_train, X_test, y_train, y_test = feature_view.get_train_test_split(training_dataset_version=1)

# get a training dataset with train, validation and test splits
X_train, X_val, X_test, y_train, y_val, y_test = feature_view.get_train_validation_test_split(training_dataset_version=1)
```

## Passing Context Variables to Transformation Functions
Once you have [defined a transformation function using a context variable](../transformation_functions.md#passing-context-variables-to-transformation-function), you can pass the required context variables using the `transformation_context` parameter when generating IN-MEMORY training data or materializing a training dataset.

!!! note
    Passing context variables for materializing a training dataset is only supported in the PySpark Kernel.


=== "Python"   
    !!! example "Passing context variables while creating training data."
        ```python
        # Passing context variable to IN-MEMORY Training Dataset.
        X_train, X_test, y_train, y_test = feature_view.get_train_test_split(training_dataset_version=1, 
                                                                         primary_key=True,
                                                                         event_time=True,
                                                                         transformation_context={"context_parameter":10})

        # Passing context variable to Materialized Training Dataset.
        version, job = feature_view.get_train_test_split(training_dataset_version=1, 
                                                                         primary_key=True,
                                                                         event_time=True,
                                                                         transformation_context={"context_parameter":10})

        ```

## Read training data with primary key(s) and event time
For certain use cases, e.g. time series models, the input data needs to be sorted according to the primary key(s) and event time combination. 
Primary key(s) and event time are not usually included in the feature view query as they are not features used for training.
To retrieve the primary key(s) and/or event time when retrieving training data, you need to set the parameters `primary_key=True` and/or `event_time=True`.


```python
# get a training dataset
X_train, X_test, y_train, y_test = feature_view.get_train_test_split(training_dataset_version=1, 
                                                                     primary_key=True,
                                                                     event_time=True)
```

!!! note
    All primary and event time columns of all the feature groups included in the feature view will be returned. If they have the same names across feature groups and the join prefix was not provided then reading operation will fail with ambiguous column exception.
    Make sure to define the join prefix if primary key and event time columns have the same names across feature groups. 

    To use primary key(s) and event time column with materialized training datasets it needs to be created with `primary_key=True` and/or `with_event_time=True`.  

## Deletion
To clean up unused training data, you can delete all training data or for a particular version. Note that all metadata of training data and materialised files stored in HopsFS will be deleted and cannot be recreated anymore.
```python
# delete a training data version
feature_view.delete_training_dataset(training_dataset_version=1)

# delete all training datasets
feature_view.delete_all_training_datasets()
```
It is also possible to keep the metadata and delete only the materialised files. Then you can recreate the deleted files by just specifying a version, and you get back the exact same dataset again. This is useful when you are running out of storage.
```python
# delete files of a training data version
feature_view.purge_training_data(training_dataset_version=1)

# delete files of all training datasets
feature_view.purge_all_training_data()
```
To recreate a training dataset:
```python
feature_view.recreate_training_dataset(training_dataset_version =1)
```

## Tags
Similar to feature view, You can attach, get, and remove tags. You can refer to [here](../tags/tags.md) if you want to learn more about how tags work.
```python
# attach
feature_view.add_training_dataset_tag(
    training_dataset_version=1, 
    name="tag_schema", 
    value={"key", "value"}
)

# get
feature_view.get_training_dataset_tag(training_dataset_version=1, name="tag_schema")

#remove
feature_view.delete_training_dataset_tag(training_dataset_version=1, name="tag_schema")
```

## Next
Once you have created a training dataset and trained your model, you can deploy your model in a "batch"  or "online" setting. Next, you can learn how to create [batch data](./batch-data.md) and get [feature vectors](./feature-vectors.md).