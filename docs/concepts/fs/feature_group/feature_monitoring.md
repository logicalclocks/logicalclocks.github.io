# Feature Monitoring

Feature monitoring complements data validation by letting you monitor feature data after it has been ingested into the feature store.
It computes statistics over a detection window of data, compares them against a reference window, and raises alerts when the comparison crosses a threshold.
The comparison can be a single scalar metric (e.g., the mean) or the whole feature distribution using a distance metric such as PSI or KL divergence.

You can monitor at two levels, and each level detects a different kind of change.

## Monitoring a feature group

Monitoring a feature group watches the raw data as it is ingested, independently of any model.
The reference window is usually an earlier window of the same feature group, so what you detect is data ingestion drift: a new batch that no longer looks like the data already in the feature group.

After creating a feature group, you can schedule statistics over one or more features, computed on the whole feature data or on a subset defined by a detection window.
You then enable a comparison against a reference window and define the criteria: which statistic to compare and the threshold that flags an anomaly.

## Monitoring a feature view

Monitoring a feature view watches what a specific model actually sees, because a feature view backs the features served to a model.
Here the reference window is typically the model's training dataset, so what you detect is feature drift: the served features drifting away from the distribution the model was trained on.

The mechanism is the same scheduled statistics and distribution comparison as for a feature group, computed using the feature view query; only the reference changes.
Comparing a model's logged inference data against its training dataset, and deciding when to retrain, is model monitoring; see [Model Monitoring](../../mlops/model_monitoring.md).

## Statistics on training data

A feature view holds no statistics of its own, since it is only an interface over features and their transformations.
Statistics are computed over a training dataset instead.
Those training-dataset statistics are the reference that feature-view monitoring compares against, and some online transformations need them too (normalizing a numerical feature requires the training-set mean).

!!! info "Feature Monitoring Guide"
    More information can be found in the [Feature monitoring guide](../../../user_guides/fs/feature_monitoring/index.md).
