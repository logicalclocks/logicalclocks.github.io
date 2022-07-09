The feature view provides an *Offline API* for

 * creating training data
 * creating batch (scoring) data

## Training Data

Training data is created using a feature view. You can create training data as either:

 - in-memory Pandas DataFrames, useful when you have a small amount of training data;
 - materialized training data in files, in a file format of your choice (such as .tfrecord, .csv, or .parquet).

You can apply filters when creating training data from a feature view:

 - start-time and end-time, for example, to create the train-set from an earlier time range, and the test-set from a later (unseen) time range;
 - feature value features, for example, only train a model on customers from a particular country.

Note that filters are not applied when retrieving feature vectors using feature views, as we only look up features for a specific entity, like a customer. In this case, the application should know that predictions for this customer should be made on the model trained on customers in USA, for example.


### Point-in-time Correct Training Data

When you create training data from features in different feature groups, it is possible that the feature groups are updated at different cadences. For example, maybe one feature group is updated hourly, while another feature group is updated daily. It is very complex to write code that joins features together from such feature groups and ensures there is no data leakage in the resultant training data. HSFS hides this complexity by performing the point-in-time JOIN transparently, similar to the illustration below:


<img src="../../../../assets/images/concepts/fs/feature-view-training-data.svg">

HSFS uses the event_time columns on both feature groups to determine the most recent (but not newer) feature values that are joined together with the feature values from the feature group containing the label. That is, the features in the feature group containinig the label are the observation times for the features in the resulting training data, and we want feature values from the other feature groups that have the most recent timestamps, but not newer than the timestamp in the label-containing feature group.


### Splitting Training Data

You can create random train/validation/test splits of your training data using the HSFS API. You can also time-based splits with the HSFS API.

### Evaluation Sets
Test data can also be split into evaluation sets to help evaluate a model for potential bias. First, you have to identify the classes of samples that could be at risk of bias, and generate *evaluation sets* from your unseen test set - one evaluation set for each group of samples at risk of bias. For example, if you have a feature group of users, where one of the features is gender, and you want to evaluate the risk of bias due to gender, you can use filters to generate 3 evaluation sets from your test set - one for male, female, and non-binary. Then you score your model against all 3 evaluation sets to ensure that the predicition performance is comparable and non-biased across all 3 gender.


## Batch (Scoring) Data

Batch data for scoring models is created using a feature view. Similar to training data, you can create batch data as either:

 - in-memory Pandas DataFrames, useful when you have a small amount of data to score;
 - materialized data in files, in a file format of your choice (such as .tfrecord, .csv, or .parquet)

Batch data requires specification of a `start_time` for the start of the batch scoring data. You can also specify the `end_time` (default is the current date).

<img src="../../../../assets/images/concepts/fs/batch-scoring-data.svg">
