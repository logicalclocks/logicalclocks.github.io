# Feature Monitoring for Feature Views

Feature Monitoring complements the Hopsworks data validation capabilities for Feature Group data by allowing you to monitor your data once they have been ingested into the Feature Store.
Hopsworks feature monitoring is centered around two functionalities: **scheduled statistics** and **statistics comparison**.

Before continuing with this guide, see the [Feature monitoring guide](../feature_monitoring/index.md) to learn more about how feature monitoring works, and get familiar with the different use cases of feature monitoring for Feature Views described in the **Use cases** sections of the [Scheduled statistics guide](../feature_monitoring/scheduled_statistics.md#use-cases) and [Statistics comparison guide](../feature_monitoring/statistics_comparison.md#use-cases).

!!! warning "Limited UI support"
    Currently, feature monitoring can only be configured using the [Hopsworks Python library](https://pypi.org/project/hopsworks).
    However, you can enable/disable a feature monitoring configuration or trigger the statistics comparison manually from the UI.

## Code

In this section, we show you how to set up feature monitoring on a Feature View using the ==Hopsworks Python library==.
Alternatively, you can get started quickly by running our [tutorial for feature monitoring](https://github.com/logicalclocks/hopsworks-tutorials/blob/master/api_examples/feature_monitoring.ipynb).

!!! info "Prerequisites"
    - A Hopsworks project.
      If you don't have one yet, go to [app.hopsworks.ai](https://app.hopsworks.ai), sign up with your email and create your first project.
    - An API key, which you can get from "Account Settings" on [app.hopsworks.ai](https://app.hopsworks.ai).
    - The [Hopsworks Python library](https://pypi.org/project/hopsworks) installed in your client.
      See the [installation guide](../../client_installation/index.md).
    - A Feature View and a Training Dataset.

### Step 1: Connect to Hopsworks

Connect the client running your notebook to Hopsworks.
You will be prompted to paste your API key to connect the notebook to your project.

=== "Python"

    ```python
    import hopsworks


    project = hopsworks.login()

    fs = project.get_feature_store()
    ```

See the API reference for [`hopsworks.login`][hopsworks.login] and [`Project.get_feature_store`][hopsworks_common.project.Project.get_feature_store].

### Step 2: Get or create a Feature View

Feature monitoring can be enabled on already created Feature Views.
We suggest you read the [Feature View](../../../concepts/fs/feature_view/fv_overview.md) concept page and familiarize yourself with the APIs to [create a feature view](overview.md) using the [query abstraction](query.md).

=== "Python"

    ```python
    # Retrieve an existing feature view
    trans_fv = fs.get_feature_view("trans_fv", version=1)

    # Or, create a new feature view
    query = trans_fg.select(["fraud_label", "amount", "cc_num"])
    trans_fv = fs.create_feature_view(
        name="trans_fv",
        version=1,
        query=query,
        labels=["fraud_label"],
    )
    ```

See the API reference for [`FeatureStore.get_feature_view`][hsfs.feature_store.FeatureStore.get_feature_view] and [`FeatureStore.create_feature_view`][hsfs.feature_store.FeatureStore.create_feature_view].

### Step 3: Get or create a Training Dataset

A Training Dataset can be used later as a reference window to compare against (see Step 6).

=== "Python"

    ```python
    # Create a training dataset with train and test splits
    _, _ = trans_fv.create_train_validation_test_split(
        description="transactions fraud batch training dataset",
        data_format="csv",
        validation_size=0.2,
        test_size=0.1,
    )
    ```

See the API reference for [`FeatureView.create_train_validation_test_split`][hsfs.feature_view.FeatureView.create_train_validation_test_split].

### Step 4: Create a monitoring configuration

Start a new configuration on the Feature View.
Use `create_scheduled_statistics` to only compute statistics on a schedule, or `create_feature_monitoring` to also compare them against a reference.

=== "Scheduled statistics"

    ```python
    # compute statistics on one or more features on a schedule
    fm_monitoring_config = trans_fv.create_scheduled_statistics(
        name="trans_fv_all_features_monitoring",
        description="Compute statistics on the Feature View data on a daily basis",
        feature_names=["amount"],  # omit to monitor all features
    )
    ```

=== "Statistics comparison"

    ```python
    # the feature to compare is selected later in
    # compare_on / compare_on_distribution (Step 7.A / 7.B), not here
    fm_monitoring_config = trans_fv.create_feature_monitoring(
        name="trans_fv_amount_monitoring",
        description="Compute and compare descriptive statistics on the Feature View data on a daily basis",
    )
    ```

See the API reference for [`FeatureView.create_scheduled_statistics`][hsfs.feature_view.FeatureView.create_scheduled_statistics] and [`FeatureView.create_feature_monitoring`][hsfs.feature_view.FeatureView.create_feature_monitoring].

!!! info "Custom schedule"
    By default, the computation of statistics is scheduled to run endlessly, every day at 12PM.
    You can modify the default schedule by adjusting the `cron_expression`, `start_date_time` and `end_date_time` parameters (e.g., `cron_expression="0 0 12 ? * MON *"` for a weekly run).
    To compute statistics on only a subset of the feature data, use the `row_percentage` parameter of `with_detection_window` (see Step 5).

### Step 5: (Optional) Define a detection window

By default, the detection window is an _expanding window_ covering the whole Feature Group data.
You can define a different detection window using the `window_length` and `time_offset` parameters of the `with_detection_window` method.
Additionally, you can specify the percentage of feature data on which statistics will be computed using the `row_percentage` parameter.

=== "Python"

    ```python
    fm_monitoring_config.with_detection_window(
        window_length="1w",  # data ingested during one week
        time_offset="1w",  # starting from last week
        row_percentage=0.8,  # use 80% of the data
    )
    ```

See the API reference for [`FeatureMonitoringConfig.with_detection_window`][hsfs.core.feature_monitoring_config.FeatureMonitoringConfig.with_detection_window].

### Step 6: (Optional) Define a reference window

When setting up feature monitoring for a Feature View, the reference can be either a reference window of feature data or a training dataset.

!!! tip "Basis for Model Monitoring"
    Using a training dataset as the reference is the basis for [Model Monitoring](../../mlops/model_monitoring/index.md), where a model's production inference data is compared against the distribution of its training dataset.

=== "Python"

    ```python
    # compare statistics against a reference window
    fm_monitoring_config.with_reference_window(
        window_length="1w",  # data ingested during one week
        time_offset="2w",  # starting from two weeks ago
        row_percentage=0.8,  # use 80% of the data
    )

    # or a training dataset
    fm_monitoring_config.with_reference_training_dataset(
        training_dataset_version=1,  # use the training dataset used to train your production model
    )
    ```

See the API reference for [`FeatureMonitoringConfig.with_reference_window`][hsfs.core.feature_monitoring_config.FeatureMonitoringConfig.with_reference_window] and [`FeatureMonitoringConfig.with_reference_training_dataset`][hsfs.core.feature_monitoring_config.FeatureMonitoringConfig.with_reference_training_dataset].

!!! info "Comparing against a specific value"
    Instead of a reference window or training dataset, you can compare the detection statistics against a fixed reference value (i.e., a window of size 1).
    In that case, skip this step and pass the `specific_value` parameter to `compare_on` in Step 7.

### Step 7.A: (Optional) Compare on a scalar metric

In order to compare detection and reference statistics, you need to provide the criteria for such comparison.
First, you select the feature and the metric to consider in the comparison using the `feature_name` and `metric` parameters.
Then, you can define a relative or absolute threshold using the `threshold` and `relative` parameters.

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

!!! info "Difference values and thresholds"
    For more information about the computation of difference values and the comparison against threshold bounds see the [Comparison criteria section](../feature_monitoring/statistics_comparison.md#comparison-criteria) in the Statistics comparison guide.

### Step 7.B: (Optional) Compare on the whole distribution

Alternatively, instead of a single scalar metric, you can detect drift in the shape of a feature's distribution using `compare_on_distribution`.
Select a distribution distance metric (e.g., `PSI`) and a threshold.
A reference window or training dataset (Step 6) is required for distribution comparison.

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
    See the [Distribution comparison guide](../feature_monitoring/distribution_comparison.md) for the full list of metrics and binning strategies.

### Step 8: Save the configuration

Finally, you can save your feature monitoring configuration by calling the `save` method.
Once the configuration is saved, the schedule for the statistics computation and comparison will be activated automatically.

=== "Python"

    ```python
    fm_monitoring_config.save()
    ```

See the API reference for [`FeatureMonitoringConfig.save`][hsfs.core.feature_monitoring_config.FeatureMonitoringConfig.save].

### Step 9: Retrieve configurations and history

Once saved, you can retrieve your feature monitoring configurations and the results of past executions directly from the Feature View.

=== "Python"

    ```python
    # fetch all configurations attached to the feature view
    configs = trans_fv.get_feature_monitoring_configs()

    # or a single configuration by name
    config = trans_fv.get_feature_monitoring_configs(name="trans_fv_amount_monitoring")

    # fetch the history of monitoring results (with computed statistics)
    history = trans_fv.get_feature_monitoring_history(
        config_name="trans_fv_amount_monitoring",
        with_statistics=True,
    )
    ```

See the API reference for [`FeatureView.get_feature_monitoring_configs`][hsfs.feature_view.FeatureView.get_feature_monitoring_configs] and [`FeatureView.get_feature_monitoring_history`][hsfs.feature_view.FeatureView.get_feature_monitoring_history].

### API Reference

[`FeatureView`][hsfs.feature_view.FeatureView]

## Monitor a model in production

A Feature View can also monitor the inference data of a model served in production, comparing it against the training dataset the model was trained on.
This is the feature-view entry point to [Model Monitoring](../../mlops/model_monitoring/index.md).

It targets the feature view's logging feature group, so feature logging must be enabled with `feature_view.enable_logging()`, and filters the detection window by the given model name and version.
The reference defaults to the training dataset version used to train the model.

=== "Python"

    ```python
    fm_monitoring_config = trans_fv.create_model_monitoring(
        name="trans_fv_model_monitoring",
        model_name="my_model",
        model_version=1,
    ).with_detection_window(
        time_offset="1d",
        window_length="1d",
    ).with_reference_training_dataset(
        # omitted -> defaults to the model's training dataset version
    ).compare_on_distribution(
        feature_name="amount",
        metric="PSI",
        threshold=0.2,
    ).save()
    ```

See the API reference for [`FeatureView.create_model_monitoring`][hsfs.feature_view.FeatureView.create_model_monitoring].

!!! info "Explore the API"
    The [`FeatureMonitoringConfig`][hsfs.core.feature_monitoring_config.FeatureMonitoringConfig] reference documents the full set of available methods, such as enabling or disabling a configuration, triggering it manually, or deleting it.
