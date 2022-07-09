See here for <a href="../../../../concepts/fs/feature_view/versioning/">information about version of feature views</a>.

### Schema Versioning

The schema of feature groups is versioned. If you make a breaking change to the schema of a feature group, you need to increment the version of the feature group, and then backfill the new feature group. A breaking schema change is when you:

 - drop a column from the schema
 - add a new fature without any default value for the new feature
 - change how a feature is computed, such that, for training models, the data for the old feature is not compatible with the data for the new feature. For example, if you have an embedding as a feature and change the algorithm to compute that embedding, you probably should not mix feature values computed with the old embedding model with feature values computed with the new embedding model.

<img src="../../../../assets/images/concepts/fs/schema-versioning.svg">

### Data Versioning for Feature Groups

Data Versioning of a feature group involves tracking updates to the feature group, so that you can recover the state of the feature group at a given point-in-time in the past.

<img src="../../../../assets/images/concepts/fs/data-versioning.svg">

