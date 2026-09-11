The Feature View provides an Online API to return an individual feature vector, or a batch of feature vectors, containing the latest feature values.
To retrieve a feature vector, a client needs to provide the primary key(s) for the feature groups backing the feature view.
For example, if you have `customer_profile` and `customer_purchases` Feature Groups both with `customer_id` as a primary key, and a Feature View made up from features from both Feature Groups, then, you would use `customer_id` to retrieve a feature vector using the Feature View object.

A feature-view query can also produce historical or aggregate online features.
The `collect` operation returns the most recent N matching rows for an entity as one ordered array of row structs.
The `aggregate` operation returns scalar count, sum, minimum, maximum, or average features over an entity's matching rows and optional event-time window, as well as the greatest or least value across several columns.
Hopsworks applies the same operations when creating offline training data to prevent training-serving skew.

The online API serves regular features with primary-key reads, collected history with ordered index scans, and aggregate or supported nested-join features with pushdown queries in RonDB.
The entity key identifies the feature vector, while a collected feature's event-time ordering column remains inside the collected rows and is not required from the caller.

## Feature Vectors

A feature vector is a row of features (without the primary key(s) and event timestamp):

<img src="../../../../assets/images/concepts/fs/feature-vector.svg">

It may be the case that for any given feature vector, not all features will come pre-engineered from the feature store.
Some features will be provided by the client (or at least the raw data to compute the feature will come from the client).
We call these 'passed' features and, similar to precomputed features from the feature store, they can also be transformed by the Hopsworks client in the method:

- feature_view.get_feature_vector(entry, passed_features={...})
