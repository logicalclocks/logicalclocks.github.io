Feature Monitoring complements data validation capabilities by allowing you to monitor your feature data after it has been ingested into the Feature Store.

HSFS supports monitoring features on your Feature Group by:

- transparently **computing statistics** on the whole or a subset of feature data defined by a detection window.
- **comparing statistics** against a reference window of feature data, and **configuring thresholds** to identify anomalous data.
- **configuring alerts** based on the statistics comparison results.

## Scheduled Statistics

After creating a Feature Group in HSFS, you can setup statistics monitoring to compute statistics over one or more features on a scheduled basis. Statistics are computed on the whole or a subset of feature data (i.e., detection window) already inserted into the Feature Group.

## Statistics Comparison

In addition to scheduled statistics, you can enable the comparison of statistics against a reference subset of feature data (i.e., reference window) and define the criteria for this comparison including the statistics metric to compare and a threshold to identify anomalous values.

!!! info "Feature Monitoring Guide"
    More information can be found in the [Feature monitoring guide](../../../user_guides/fs/feature_monitoring/index.md).


