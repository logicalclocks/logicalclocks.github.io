# Model Monitoring Creation

This guide shows how to configure monitoring for a model in production using the ==Hopsworks Python library==.
Make sure you have read the [Model Monitoring overview](index.md) first.

!!! info "Prerequisites"
    Make sure you meet the [prerequisites](index.md#prerequisites): a feature view with feature logging enabled, a registered model with a recorded training dataset version, and a model deployment with a predictor script that logs its inference data.

!!! warning "Limited UI support"
    Like feature monitoring, model monitoring can currently only be configured using the [Hopsworks Python library](https://pypi.org/project/hopsworks).

## Code

In this section, we show you how to set up model monitoring from a model or a model deployment using the ==Hopsworks Python library==.

### Step 1: Connect to Hopsworks

Connect the client running your notebook to Hopsworks and get the Model Registry and Model Serving handles.

=== "Python"

    ```python
    import hopsworks


    project = hopsworks.login()

    mr = project.get_model_registry()
    ms = project.get_model_serving()
    ```

See the API reference for [`hopsworks.login`][hopsworks.login], [`Project.get_model_registry`][hopsworks_common.project.Project.get_model_registry] and [`Project.get_model_serving`][hopsworks_common.project.Project.get_model_serving].

### Step 2: Get a model or deployment

Retrieve the model or the deployment whose inference data you want to monitor.

=== "From a deployment"

    ```python
    my_deployment = ms.get_deployment("my_deployment")
    ```

=== "From a model"

    ```python
    my_model = mr.get_model("my_model", version=1)
    ```

See the API reference for [`ModelServing.get_deployment`][hsml.model_serving.ModelServing.get_deployment] and [`ModelRegistry.get_model`][hsml.model_registry.ModelRegistry.get_model].

### Step 3: Create a model monitoring configuration

Start a new configuration from the deployment or the model.
Hopsworks resolves the model's parent feature view from its provenance and fills in the model name and version for you.

=== "From a deployment"

    ```python
    fm_monitoring_config = my_deployment.create_model_monitoring(
        name="model_psi_monitoring",
    )
    ```

=== "From a model"

    ```python
    fm_monitoring_config = my_model.create_model_monitoring(
        name="model_psi_monitoring",
    )
    ```

See the API reference for [`Deployment.create_model_monitoring`][hsml.deployment.Deployment.create_model_monitoring] and [`Model.create_model_monitoring`][hsml.model.Model.create_model_monitoring].

!!! tip "Configuring from a feature view"
    You can also configure model monitoring directly from the feature view backing the model, using `feature_view.create_model_monitoring`.
    See the [Feature Monitoring guide for Feature Views](../../fs/feature_view/feature_monitoring.md#monitor-a-model-in-production).

!!! info "Custom schedule"
    By default, monitoring runs every day at 12PM.
    You can modify the schedule by adjusting the `cron_expression`, `start_date_time` and `end_date_time` parameters of `create_model_monitoring` (UTC, Quartz specification).

!!! warning "Sub-hourly schedules"
    The inference-log feature group materializes its offline data at most once per hour.
    A cron expression that fires more than once per hour produces redundant or incomplete detection windows and triggers a warning, so use a schedule that fires at most once per hour.

### Step 4: Define a detection window

The detection window covers the inference data recently served by the model.
Define it using the `window_length` and `time_offset` parameters of the `with_detection_window` method.

=== "Python"

    ```python
    fm_monitoring_config.with_detection_window(
        time_offset="1d",  # data served by this model in the last day
        window_length="1d",
    )
    ```

See the API reference for [`FeatureMonitoringConfig.with_detection_window`][hsfs.core.feature_monitoring_config.FeatureMonitoringConfig.with_detection_window].

### Step 5: Define the reference training dataset

By default, the reference is the training dataset version used to train the model, recorded at model registration time.
You can call `with_reference_training_dataset()` without arguments to make this explicit.

=== "Python"

    ```python
    fm_monitoring_config.with_reference_training_dataset(
        # omitted -> defaults to the model's training dataset version
    )
    ```

See the API reference for [`FeatureMonitoringConfig.with_reference_training_dataset`][hsfs.core.feature_monitoring_config.FeatureMonitoringConfig.with_reference_training_dataset].

!!! info "Training dataset version validation"
    If you pass a specific version, it must match the model's recorded training dataset version, otherwise the call raises an exception.
    This guards against accidentally comparing production data against a training dataset the model was never trained on.

### Step 6.A: Compare on a scalar metric

Select the feature and the metric to compare, and define a relative or absolute threshold.

=== "Python"

    ```python
    fm_monitoring_config.compare_on(
        feature_name="amount",  # the feature to compare
        metric="mean",
        threshold=0.2,  # a relative change over 20% is considered anomalous
        relative=True,  # relative or absolute change
        strict=False,  # strict or relaxed comparison
    )
    ```

See the API reference for [`FeatureMonitoringConfig.compare_on`][hsfs.core.feature_monitoring_config.FeatureMonitoringConfig.compare_on].

### Step 6.B: Compare on the whole distribution

Alternatively, instead of a single scalar metric, you can detect drift in the shape of the feature's distribution using `compare_on_distribution`.
Select a distribution distance metric (e.g., `PSI`) and a threshold.

=== "Python"

    ```python
    fm_monitoring_config.compare_on_distribution(
        feature_name="amount",  # the feature to compare
        metric="PSI",
        threshold=0.2,  # a distance above 0.2 is considered a significant shift
    )
    ```

See the API reference for [`FeatureMonitoringConfig.compare_on_distribution`][hsfs.core.feature_monitoring_config.FeatureMonitoringConfig.compare_on_distribution].

!!! tip "More distribution options"
    See the [Distribution comparison guide](../../fs/feature_monitoring/distribution_comparison.md) for the full list of metrics and binning strategies.

### Step 7: Save the configuration

Finally, save the configuration by calling the `save` method.
Once saved, the schedule for the statistics computation and comparison is activated automatically.

=== "Python"

    ```python
    fm_monitoring_config.save()
    ```

See the API reference for [`FeatureMonitoringConfig.save`][hsfs.core.feature_monitoring_config.FeatureMonitoringConfig.save].

### Step 8: Retrieve configurations

You can list the monitoring configurations attached to a model or deployment.

=== "From a deployment"

    ```python
    fm_configs = my_deployment.get_monitoring_configs()
    ```

=== "From a model"

    ```python
    fm_configs = my_model.get_monitoring_configs()
    ```

See the API reference for [`Deployment.get_monitoring_configs`][hsml.deployment.Deployment.get_monitoring_configs] and [`Model.get_monitoring_configs`][hsml.model.Model.get_monitoring_configs].

!!! info "Next steps"
    Model monitoring results integrate with the same [alerting](../../fs/feature_monitoring/index.md#alerting) and [interactive graph](../../fs/feature_monitoring/interactive_graph.md) tooling as feature monitoring.
    See the [`FeatureMonitoringConfig`][hsfs.core.feature_monitoring_config.FeatureMonitoringConfig] reference to learn how to disable, manually trigger, or delete a configuration.
