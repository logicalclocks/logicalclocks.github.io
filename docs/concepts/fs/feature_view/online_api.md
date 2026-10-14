# Online API

The Feature View provides an Online API to return an individual feature vector, or a batch of feature vectors, containing the latest feature values.
To retrieve a feature vector, a client provides the feature view's serving keys.
The serving keys are the foreign keys of the feature view's label feature group; a feature view does not have a primary key of its own.
For example, if a feature view is built from the `customer_profile` and `customer_purchases` feature groups joined on `customer_id`, then `customer_id` is the serving key you provide to retrieve a feature vector.

A feature-view query can also produce historical or aggregate online features.
The `collect` operation returns the most recent N matching rows for an entity as one ordered array of row structs.
The `aggregate` operation returns scalar count, sum, minimum, maximum, or average features over an entity's matching rows and optional event-time window, as well as the greatest or least value across several columns.
Hopsworks applies the same operations when creating offline training data to prevent training-serving skew.

The online API serves regular features with primary-key reads, collected history with ordered index scans, and aggregate or supported nested-join features with pushdown queries in RonDB.
The entity key identifies the feature vector, while a collected feature's event-time ordering column remains inside the collected rows and is not required from the caller.

## Feature Vectors

A feature vector is a row of features (without the primary key(s) and event timestamp):

--8<-- "concepts/fs/feature_view/online_api/feature-vectors.html"

It may be the case that for any given feature vector, not all features will come pre-engineered from the feature store.
Some features will be provided by the client (or at least the raw data to compute the feature will come from the client).
We call these 'passed' features and, similar to precomputed features from the feature store, they can also be transformed by the Hopsworks client in the method:

```python
feature_view.get_feature_vector(entry, passed_features={"pressure": 1013})
```

When you call `get_feature_vector`, Hopsworks builds the vector in a fixed order:

1. retrieve the precomputed features from the online store using the serving keys,
2. merge in any passed features,
3. compute on-demand transformations (ODTs),
4. compute model-dependent transformations (MDTs),
5. drop the index and helper columns,
6. return the feature vector.

This ordering is the composition constraint: on-demand transformations run before model-dependent ones, which are always last, just before the model is called.
