# Model Monitoring

Model monitoring lets you detect drift between the data a model was trained on and the data it serves in production.
It is built on top of [feature monitoring](../../fs/feature_monitoring/index.md): a model monitoring configuration computes statistics over the model's logged inference data (the _detection window_) and compares them against the training dataset the model was trained on (the _reference window_).

You can configure model monitoring from a [model deployment](model_monitoring.md), a [model](model_monitoring.md), or a [feature view](model_monitoring.md) — all three resolve to the same underlying configuration on the feature view's logging feature group, filtered by the model name and version.

## Prerequisites

To enable model monitoring, you need:

- A **feature view** with **feature logging enabled**.
  Logging is what captures the inference data that monitoring analyzes.
  If logging is not enabled, enable it with `feature_view.enable_logging()`.
- A **registered model** trained from that feature view, with a **recorded training dataset version**.
  The training dataset version is recorded automatically when the model is created from a feature view, and is used as the default reference distribution.
- A **model deployment** that logs its inference data to the feature view via the feature view `log` methods (typically from its predictor script).
  Feature logging is what produces the data that monitoring analyzes, so the deployment must write its inference data to the feature view's logging feature group.
  This is currently only supported for model deployments with a predictor script.
  See the [Feature Logging guide](../../fs/feature_view/feature_logging.md).

## How it relates to feature monitoring

Model monitoring is feature monitoring applied to a model's inference logs:

- The **detection window** covers the data recently served by the model, read from the logging feature group and filtered by model name and version.
- The **reference window** defaults to the training dataset version used to train the model, so you compare production data against training data out of the box.
- The **comparison criteria** uses the same [scalar metric](../../fs/feature_monitoring/statistics_comparison.md) and [data distribution](../../fs/feature_monitoring/distribution_comparison.md) criteria as feature monitoring.

!!! info "Next steps"
    See the [Model Monitoring Creation guide](model_monitoring.md) for code examples from a model deployment, a model, and a feature view.
