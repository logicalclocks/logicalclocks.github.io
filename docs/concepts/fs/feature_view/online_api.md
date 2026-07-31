# Online API

The Feature View provides an Online API to return an individual feature vector, or a batch of feature vectors, containing the latest feature values.
To retrieve a feature vector, a client provides the feature view's serving keys.
The serving keys are the foreign keys of the feature view's label feature group; a feature view does not have a primary key of its own.
For example, if a feature view is built from the `customer_profile` and `customer_purchases` feature groups joined on `customer_id`, then `customer_id` is the serving key you provide to retrieve a feature vector.

## Feature Vectors

A feature vector is a row of features (without the primary key(s) and event timestamp):

<img src="../../../../assets/images/concepts/fs/feature-vector.svg">

It may be the case that for any given feature vector, not all features will come pre-engineered from the feature store.
Some features will be provided by the client (or at least the raw data to compute the feature will come from the client).
We call these 'passed' features and, similar to precomputed features from the feature store, they can also be transformed by the Hopsworks client in the method:

- feature_view.get_feature_vector(entry, passed_features={...})

When you call `get_feature_vector`, Hopsworks builds the vector in a fixed order:

1. retrieve the precomputed features from the online store using the serving keys,
2. merge in any passed features,
3. compute on-demand transformations (ODTs),
4. compute model-dependent transformations (MDTs),
5. drop the index and helper columns,
6. return the feature vector.

This ordering is the composition constraint: on-demand transformations run before model-dependent ones, which are always last, just before the model is called.
