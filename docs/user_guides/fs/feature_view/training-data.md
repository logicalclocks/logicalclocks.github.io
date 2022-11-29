# Training data

Training data can be created from the feature view and used by different ML libraries for training different models.

You can read [training data concepts](../../../concepts/fs/feature_view/offline_api.md) for more details. To see a full example of how to create training data, you can read [this notebook](https://github.com/logicalclocks/hopsworks-tutorials/blob/master/fraud_batch/2_feature_view_creation.ipynb).

## Creation
It can be created as in-memory DataFrames or materialised as `tfrecords`, `parquet`, `csv`, or `tsv` files to HopsFS or in all other locations, for example, S3, GCS. If you materialise a training dataset, a `PySparkJob` will be launched. By default, `create_training_data` waits for the job to finish. However, you can run the job asynchronously by passing `write_options={"wait_for_job": False}`. You can monitor the job status in the [jobs overview UI](../../projects/jobs/pyspark_job.md#step-1-jobs-overview).

=== "Python"
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

In the [transaction fraud example](https://github.com/logicalclocks/hopsworks-tutorials/blob/master/fraud_batch/1_feature_groups.ipynb), there are different transaction categories, for example: "Health/Beauty", "Restaurant/Cafeteria", "Holliday/Travel" etc. Examples below show how to create training data for different transaction categories.
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

### Event-time based dataset split
Also you can create dataset splits based on event-time filter. There can be several such splits.
```python
start_time = 1640991600000
end_time = 1642633200000

td_train_version, td_job = feature_view.create_training_data(
        start_time=start_time,
        end_time=end_time,    
        description='training dataset, 2022-01-01 -> 2022-01-20',
        data_format="csv",
        coalesce = True,
        write_options = {'wait_for_job': True},
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
    data_format = 'csv' # or 'tfrecords', 'parquet', 'tsv'
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

## Deletion
To clean up unused training data, you can delete all training data or for a particular version. Note that all metadata of training data and materialised files stored in HopsFS will be deleted and cannot be recreated anymore.
```python
# delete a training data version
feature_view.delete_training_dataset(version=1)

# delete all training datasets
feature_view.delete_training_dataset()
```
It is also possible to keep the metadata and delete only the materialised files. Then you can recreate the deleted files by just specifying a version, and you get back the exact same dataset again. This is useful when you are running out of storage.
```python
# delete files of a training data version
feature_view.purge_training_data(version=1)

# delete files of all training datasets
feature_view.purge_all_training_data()
```
To recreate a training dataset:
```python
feature_view.recreate_training_dataset(version=1)
```

## Tags
Similar to feature view, You can attach, get, and remove tags. You can refer to [here]() if you want to learn more about how tags work.
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
