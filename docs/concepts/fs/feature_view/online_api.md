The Feature View provides an Online API to return an individual feature vector, or a batch of feature vectors, containing the latest feature values. To retrieve a feature vector, a client needs to provide the primary key(s) for the feature groups backing the feature view. For example, if you have `customer_profile` and `customer_purchases` Feature Groups both with `customer_id` as a primary key, and a Feature View made up from features from both Feature Groups, then, you would use `customer_id` to retrieve a feature vector using the Feature View object.

## Feature Vectors

A feature vector is a row of features (without the primary key(s) and event timestamp):

<img src="../../../../assets/images/concepts/fs/feature-vector.svg">

It may be the case that for any given feature vector, not all features will come pre-engineered from the feature store. Some features will be provided by the client (or at least the raw data to compute the feature will come from the client). We call these 'passed' features and, similar to precomputed features from the feature store, they can also be transformed by the HSFS client in the method:

* feature_view.get_feature_vector(<primary-keys>, passed={ .... })

