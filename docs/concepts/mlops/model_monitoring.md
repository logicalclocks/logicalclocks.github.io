Model monitoring lets you track how a deployed model behaves in production by comparing the data it serves against the data it was trained on.

When a model runs in production, the statistical properties of its inputs and predictions can drift away from those of the training data.
This degrades model quality silently, without any error being raised.
Model monitoring detects this drift early so you can decide whether to retrain the model.

## How it works

Model monitoring builds on two existing Hopsworks capabilities:

- **Feature logging**: a model deployment logs the features it serves and its predictions to the feature view's logging feature group through the Feature View logging APIs.
  See the [Feature Logging guide](../../user_guides/fs/feature_view/feature_logging.md).
- **Feature monitoring**: Hopsworks computes statistics over windows of feature data and compares them against a reference, optionally raising alerts on significant shifts.
  See the [Feature Monitoring concept](../fs/feature_view/feature_monitoring.md).

!!! info "Feature logging vs. the inference logger"
    Hopsworks provides two separate inference logging mechanisms.
    The [inference logger](../../user_guides/mlops/serving/inference-logger.md) stores the model inputs and predictions from inference requests and responses into Kafka, for later consumption and analysis.
    [Feature logging](../../user_guides/fs/feature_view/feature_logging.md) supports more fine-grained logging of inference logs and features, enabling feature monitoring and model monitoring.
    Model monitoring relies on feature logging, not on the inference logger.

A model monitoring configuration is a feature monitoring configuration over the logging feature group, filtered to a single model and version.
The detection window covers the recently served inference data, and the reference defaults to the training dataset version that was used to train that model.
By comparing the two — on a scalar metric or on the whole feature distribution — Hopsworks detects training/serving skew and drift over time.

## Where to configure it

Because monitoring is anchored on the feature view that backs the model, you can configure model monitoring from whichever entity is most convenient:

- a **model deployment**, when operating a model in production.
- a **model** in the model registry.
- a **feature view**, when working directly with the feature data.

All three resolve to the same underlying configuration.

!!! info "Model Monitoring Guide"
    More information can be found in the [Model Monitoring guide](../../user_guides/mlops/model_monitoring/index.md).
