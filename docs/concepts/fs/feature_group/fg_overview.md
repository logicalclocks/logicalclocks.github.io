# Features and Feature Groups

As a programmer, you can consider a feature, in machine learning, to be a variable associated with some entity that contains a value that is useful for helping train a model to solve a prediction problem.
That is, the feature is just a variable with predictive power for a machine learning problem, or task.

A feature group is a table of features.
Each feature group has a primary key, and optionally an event_time column (indicating when the features in that row were observed), a partition key, and foreign keys that point to the primary keys of other feature groups.
These are index columns, not features: they identify and join rows, and they are excluded when you select the features for a model.
A feature group stores untransformed feature data, so the same feature can be reused across models that each transform it differently.

??? note "Partitioning"
    The partition key determines how the feature group rows are laid out on disk, so that queries using the partition key read only the data they need.
    For example, if the partition key is the day and you have hundreds of days of data, a query for a given day or a range of days reads only those days from disk.

<img src="../../../../assets/images/concepts/fs/feature-group-table.png">

## Online and offline Storage

Feature groups can be stored in a low-latency "online" database and/or in low cost, high throughput "offline" storage, typically a data lake or data warehouse.
A feature group with an embedding column can also have a vector index, for similarity search from inference pipelines and agents.

<img src="../../../../assets/images/concepts/fs/feature-storage.svg">

### Online Storage

By default, the online store keeps only the latest values of features for a feature group.
It serves those precomputed features to models at runtime, and is backed by [RonDB](https://www.rondb.com), a low latency, high throughput, high availability data store.

### Offline Storage

The offline store stores the historical values of features for a feature group so that it may store much more data than the online store.
Offline feature groups are used, typically, to create training data for models, but also to retrieve data for batch scoring of models.

In most cases, offline data is stored in Hopsworks, but through the implementation of data sources, it can reside in an external file system.
The externally stored data can be managed by Hopsworks by defining ordinary feature groups or it can be used for reading only by defining [External Feature Group](external_fg.md).
