# Distribution Comparison

Distribution comparison lets you detect drift in the **shape of a feature's distribution** between a detection window and a reference window, rather than comparing a single scalar metric such as the mean.
It is configured with the `compare_on_distribution` method, as an alternative to [`compare_on`](statistics_comparison.md#comparison-criteria).

A single scalar metric can miss meaningful changes.
For example, the mean of a feature can stay constant while its variance grows or while a unimodal distribution becomes bimodal.
Distribution comparison captures these changes by computing a distance between the detection and reference distributions and comparing it against a threshold.

!!! info "Reference window required"
    Distribution comparison always compares two windows, so a reference window is mandatory.
    Define it with `with_reference_window` or `with_reference_training_dataset` before calling `compare_on_distribution`.

!!! tip "Reference training dataset"
    On a Feature View, you can use a training dataset as the reference distribution with `with_reference_training_dataset(training_dataset_version=...)`.
    This is the basis for [Model Monitoring](../../mlops/model_monitoring/index.md), where a model's production inference data is compared against the distribution of its training dataset.

## Use cases

Distribution comparison is most valuable when changes in your data are not captured by a single scalar metric, but by a change in the overall shape of the feature distribution.
It can be enabled on both Feature Groups and Feature Views, but for different purposes.

For **Feature Groups**, distribution comparison helps you detect when newly ingested feature data drifts in shape from a baseline window of historical data, surfacing issues such as a new category becoming dominant or a numeric feature shifting from unimodal to multimodal, even when its mean stays stable.
See the [Feature Monitoring for Feature Groups](../feature_group/feature_monitoring.md) guide to configure it.

For **Feature Views**, distribution comparison helps you quantify how much the distribution of newly inserted Feature Group data has drifted from your training dataset, and decide whether to retrain your ML models on a new training dataset version before the drift degrades model performance.
See the [Feature Monitoring for Feature Views](../feature_view/feature_monitoring.md) guide to configure it.

## Distance metrics

You select the distance metric with the `metric` parameter.
The following metrics are available:

- **PSI** (Population Stability Index) — the default metric, widely used to monitor drift in production.
  It is the only metric with a built-in default threshold of `0.2`.
- **KL_DIVERGENCE** — Kullback–Leibler divergence; asymmetric, sensitive to regions where the reference has low probability.
- **JS_DIVERGENCE** — Jensen–Shannon divergence; a symmetric, bounded smoothing of KL divergence.
- **HELLINGER** — Hellinger distance; symmetric and bounded in `[0, 1]`.
- **WASSERSTEIN** — Wasserstein (earth mover's) distance; numeric features only.
- **KOLMOGOROV_SMIRNOV** — Kolmogorov–Smirnov statistic; numeric features only.

For every metric other than PSI, you must provide a `threshold` explicitly.

!!! warning "Numeric-only metrics"
    `WASSERSTEIN` and `KOLMOGOROV_SMIRNOV` require a numeric feature.
    Applying them to a categorical feature raises an error.

## Binning

To compute a distance, Hopsworks first discretizes the feature values into a probability distribution over bins.
You control the binning with the following parameters:

- `binning_strategy` — how to build the bins.
  One of `EQUI_WIDTH` (equal-width bins), `EQUI_FREQUENCY` (equal-frequency / quantile bins), `CUSTOM_EDGES` (user-provided bin edges) or `CATEGORICAL` (one bin per category).
  Defaults to `EQUI_FREQUENCY` for numeric features and `CATEGORICAL` otherwise.
- `bin_count` — the number of bins for numeric strategies.
  Defaults to `10`.
- `custom_bin_edges` — the list of bin edges, required when `binning_strategy` is `CUSTOM_EDGES`.
- `smoothing_epsilon` — a small additive constant applied to bins to avoid `log(0)` in log-based metrics such as PSI and KL divergence.
  Defaults to `1e-6`.

!!! info "Next steps"
    Distribution comparison results integrate with the same [alerting](index.md#alerting) and [interactive graph](interactive_graph.md) tooling as scalar statistics comparison.
