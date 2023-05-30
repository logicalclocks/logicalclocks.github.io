---
description:Using Spine Groups in Feature View queries for training dataset and batch retrieval.
---

# Using Spines

In this section we will illustrate how to use a [Spine Group](../../../concepts/fs/feature_group/spine_group.md) instead of a regular Feature Group for performing
point-in-time joins when reading batch data for inference or when creating training datasets.

## Prerequisites

1. Make sure you have read the [concept section about spines](../../../concepts/fs/feature_group/spine_group.md) in feature and inference pipelines.
2. Make sure you have gone through the [Spine Group creation guide](../feature_group/create_spine.md).
3. Make sure you understand the [concept of feature views](../../../concepts/fs/feature_view/fv_overview.md) and how to create them using the [query abstraction](../feature_view/query.md)

## Feature View with a Spine Group

### Step 1: Query Definition

The first step before creating a Feature View, is to construct the query by selecting the label and features which are needed:

```python
# Select features for training data.
ds_query = trans_fg.select(["fraud_label"])\
    .join(window_aggs_fg.select_except(["cc_num"]), on="cc_num")

ds_query.show(5)
```

Similarly you can construct the query using a previously created spine equivalent.

However, there are two thing to note:

1. **If you want to use the query for a feature view to be used for online serving, you can only select the "label" or target feature from the spine.**
2. **Spine groups can only be used on the left side of the join.** Think of the left side of the join as the base set of entities that should be included in you batch of data or training dataset, which we enrich with the relevant and point-in-time correct feature values.

```python
trans_spine = fs.get_or_create_spine_group(
    name="spine_transactions",
    version=1,
    description="Transaction data",
    primary_key=['cc_num'],
    event_time='datetime',
    dataframe=trans_df
)

# Select features for training data.
ds_query_spine = trans_spine.select(["fraud_label"])\
    .join(window_aggs_fg.select_except(["cc_num"]), on="cc_num")
```

Calling the `show()` or `read()` method of this query object will use the spine dataframe included in the Spine Group object to perform the join.

```python
ds_query_spine.show(10)
```

### Step 2: Feature View Creation

With the above defined query, we can continue to create the Feature View in the same way we would do it also without a spine:

```python
feature_view_spine = fs.get_or_create_feature_view(
    name='transactions_view_spine',
    query=ds_query_spine,
    version=1,
    labels=["fraud_label"],
)
```

### Step 3: Training Dataset Creation

With the regular feature view, the labels are fetched from the feature store, but with the feature view created with a spine, you need to provide the dataframe.
Here you have the chance to pass a different set of entities to generate the training dataset.

```python
X_train, X_test, y_train, y_test = feature_view_spine.train_test_split(0.2, spine=new_entities_df)

X_train.show()
```

### Step 4: Retrieving New Batches Inference Data

You can now use the offline and online API of the feature stores to read features for inference.
Similarly to training dataset creation, every time you read up a new batch of data, you can pass a different spine dataframe.

```python
feature_view_spine.get_batch_data(spine=scroing_spine_df).show()
```

### Step 5: Online Feature Lookup

For the online lookup, the label is not required, therefore it was important to only select label from the left spine group, so that we don't need to provide a spine for online serving:

```python
# Note: no spine needs to be passed
feature_view.get_feature_vector({"cc_num": 4473593503484549})
```

## Replacing a Regular Feature Group with a Spine at Serving Time

In the case where you create a feature view with a regular feature group, but you would like to retrieve batch inference data using IDs (primary key values), you can use a spine to replace the left feature group.
To do this, you can pass the Spine Group instead of a dataframe.

```python
# Note: here feature_view was created with regular feature groups only
# and trans_spine is of type SpineGroup instead of a dataframe
feature_view.get_batch_data(spine=trans_spine).show()
```
