# Feature Monitoring for Feature Groups

Feature Monitoring complements the Hopsworks data validation capabilities for Feature Groups by allowing you to monitor your data once they have been ingested into the Feature Store.
Hopsworks feature monitoring is centered around two functionalities: **scheduled statistics** and **statistics comparison**.

Before continuing with this guide, see the [Feature monitoring guide](../feature_monitoring/index.md) to learn more about how feature monitoring works, and get familiar with the different use cases of feature monitoring for Feature Groups described in the **Use cases** sections of the [Scheduled statistics guide](../feature_monitoring/scheduled_statistics.md#use-cases) and [Statistics comparison guide](../feature_monitoring/statistics_comparison.md#use-cases).

!!! warning "Limited UI support"
    Currently, feature monitoring can only be configured using the [Hopsworks Python library](https://pypi.org/project/hopsworks).
    However, you can enable/disable a feature monitoring configuration or trigger the statistics comparison manually from the UI.

## Code

In this section, we show you how to setup feature monitoring in a Feature Group using the ==Hopsworks Python library==.
Alternatively, you can get started quickly by running our [tutorial for feature monitoring](https://github.com/logicalclocks/hopsworks-tutorials/blob/master/api_examples/feature_monitoring.ipynb).

First, checkout the pre-requisite and Hopsworks setup to follow the guide below.
Create a project, install the [Hopsworks Python library](https://pypi.org/project/hopsworks) in your environment, connect via the generated API key.
The second step is to start a new configuration for feature monitoring.

After that, you can optionally define a detection window of data to compute statistics on, or use the default detection window (i.e., whole feature data).
If you want to setup scheduled statistics alone, you can jump to the last step to save your configuration.
Otherwise, the third and fourth steps are also optional and show you how to setup the comparison of statistics on a schedule by defining a reference window and specifying the statistics metric to monitor.

### Step 1: Pre-requisite

In order to setup feature monitoring for a Feature Group, you will need:

- A Hopsworks project.
  If you don't have a project yet you can go to [app.hopsworks.ai](https://app.hopsworks.ai), signup with your email and create your first project.
- An API key, you can get one by going to "Account Settings" on [app.hopsworks.ai](https://app.hopsworks.ai).
- The Hopsworks Python library installed in your client.
  See the [installation guide](../../client_installation/index.md).
- A Feature Group

#### Connect your notebook to Hopsworks

Connect the client running your notebooks to Hopsworks.

=== "Python"

    ```python
    import hopsworks


    project = hopsworks.login()

    fs = project.get_feature_store()
    ```

See the API reference for [`hopsworks.login`][hopsworks.login] and [`Project.get_feature_store`][hopsworks_common.project.Project.get_feature_store].

You will be prompted to paste your API key to connect the notebook to your project.
The `fs` Feature Store entity is now ready to be used to insert or read data from Hopsworks.

#### Get or create a Feature Group

Feature monitoring can be enabled on already created Feature Groups.
We suggest you read the [Feature Group](../../../concepts/fs/feature_group/fg_overview.md) concept page to understand what a feature group is and how it fits in the ML pipeline.
We also suggest you familiarize with the APIs to [create a feature group](./create.md).

The following is a code example for getting or creating a Feature Group with name `trans_fg` for transaction data.

=== "Python"

    ```python
    # Retrieve an existing feature group
    trans_fg = fs.get_feature_group("trans_fg", version=1)

    # Or, create a new feature group with transactions
    trans_fg = fs.get_or_create_feature_group(
        name="trans_fg",
        version=1,
        description="Transaction data",
        primary_key=["cc_num"],
        event_time="datetime",
    )
    trans_fg.insert(transactions_df)
    ```

See the API reference for [`FeatureStore.get_feature_group`][hsfs.feature_store.FeatureStore.get_feature_group] and [`FeatureStore.get_or_create_feature_group`][hsfs.feature_store.FeatureStore.get_or_create_feature_group].

### Step 2: Initialize configuration

#### Scheduled statistics

You can setup statistics monitoring on a ==single feature or multiple features== of your Feature Group.

=== "Python"

    ```python
    # compute statistics for all the features
    fg_monitoring_config = trans_fg.create_scheduled_statistics(
        name="trans_fg_all_features_monitoring",
        description="Compute statistics on all data of all features of the Feature Group on a daily basis",
    )

    # or for one or more specific features
    fg_monitoring_config = trans_fg.create_scheduled_statistics(
        name="trans_fg_amount_monitoring",
        description="Compute statistics on all data of selected features of the Feature Group on a daily basis",
        feature_names=["amount"],
    )
    ```

See the API reference for [`FeatureGroup.create_scheduled_statistics`][hsfs.feature_group.FeatureGroup.create_scheduled_statistics].

#### Statistics comparison

When enabling the comparison of statistics in a feature monitoring configuration, the feature to compare is selected later in the `compare_on` (or `compare_on_distribution`) method, not in `create_feature_monitoring`.
You can create multiple feature monitoring configurations for the same Feature Group.

=== "Python"

    ```python
    fg_monitoring_config = trans_fg.create_feature_monitoring(
        name="trans_fg_amount_monitoring",
        description="Compute and compare descriptive statistics on the Feature Group on a daily basis",
    )
    ```

See the API reference for [`FeatureGroup.create_feature_monitoring`][hsfs.feature_group.FeatureGroup.create_feature_monitoring].

#### Custom schedule

By default, the computation of statistics is scheduled to run endlessly, every day at 12PM.
You can modify the default schedule by adjusting the `cron_expression`, `start_date_time` and `end_date_time` parameters.
To compute statistics on only a subset of the feature data, use the `row_percentage` parameter of `with_detection_window` (see Step 3).

=== "Python"

    ```python
    fg_monitoring_config = trans_fg.create_scheduled_statistics(
        name="trans_fg_all_features_monitoring",
        description="Compute statistics on all data of all features of the Feature Group on a weekly basis",
        cron_expression="0 0 12 ? * MON *",  # weekly
    )

    # or
    fg_monitoring_config = trans_fg.create_feature_monitoring(
        name="trans_fg_amount_monitoring",
        description="Compute and compare descriptive statistics on the Feature Group on a weekly basis",
        cron_expression="0 0 12 ? * MON *",  # weekly
    )
    ```

### Step 3: (Optional) Define a detection window

By default, the detection window is an _expanding window_ covering the whole Feature Group data.
You can define a different detection window using the `window_length` and `time_offset` parameters provided in the `with_detection_window` method.
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

### Step 4: (Optional) Define a reference window

When setting up feature monitoring for a Feature Group, you can compare the detection statistics against a reference window of feature data.
A reference window is defined with the `with_reference_window` method.

=== "Python"

    ```python
    # compare statistics against a reference window
    fm_monitoring_config.with_reference_window(
        window_length="1w",  # data ingested during one week
        time_offset="2w",  # starting from two weeks ago
        row_percentage=0.8,  # use 80% of the data
    )
    ```

See the API reference for [`FeatureMonitoringConfig.with_reference_window`][hsfs.core.feature_monitoring_config.FeatureMonitoringConfig.with_reference_window].

!!! info "Comparing against a specific value"
    Instead of a reference window, you can compare the detection statistics against a fixed reference value (i.e., a window of size 1).
    In that case, skip this step and pass the `specific_value` parameter to `compare_on` in Step 5.

### Step 5.A: (Optional) Compare on a scalar metric

In order to compare detection and reference statistics, you need to provide the criteria for such comparison.
First, you select the feature and the metric to consider in the comparison using the `feature_name` and `metric` parameters.
Then, you can define a relative or absolute threshold using the `threshold` and `relative` parameters.

=== "Python"

    ```python
    # compare against a reference window
    fm_monitoring_config.compare_on(
        feature_name="amount",  # the feature to compare
        metric="mean",
        threshold=0.2,  # a relative change over 20% is considered anomalous
        relative=True,  # relative or absolute change
        strict=False,  # strict or relaxed comparison
    )

    # or compare against a specific value instead of a reference window
    fm_monitoring_config.compare_on(
        feature_name="amount",
        metric="mean",
        specific_value=100,
        threshold=0.2,
        relative=True,
    )
    ```

See the API reference for [`FeatureMonitoringConfig.compare_on`][hsfs.core.feature_monitoring_config.FeatureMonitoringConfig.compare_on].

!!! info "Difference values and thresholds"
    For more information about the computation of difference values and the comparison against threshold bounds see the [Comparison criteria section](../feature_monitoring/statistics_comparison.md#comparison-criteria) in the Statistics comparison guide.

### Step 5.B: (Optional) Compare on the whole distribution

Alternatively, instead of a single scalar metric, you can detect drift in the shape of a feature's distribution using `compare_on_distribution`.
Select a distribution distance metric (e.g., `PSI`) and a threshold.
A reference window (Step 4) is required for distribution comparison.

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

### Step 6: Save configuration

Finally, you can save your feature monitoring configuration by calling the `save` method.
Once the configuration is saved, the schedule for the statistics computation and comparison will be activated automatically.

=== "Python"

    ```python
    fm_monitoring_config.save()
    ```

See the API reference for [`FeatureMonitoringConfig.save`][hsfs.core.feature_monitoring_config.FeatureMonitoringConfig.save].

### Retrieve configurations and history

Once saved, you can retrieve your feature monitoring configurations and the results of past executions directly from the Feature Group.

=== "Python"

    ```python
    # fetch all configurations attached to the feature group
    configs = trans_fg.get_feature_monitoring_configs()

    # or a single configuration by name
    config = trans_fg.get_feature_monitoring_configs(name="trans_fg_amount_monitoring")

    # fetch the history of monitoring results (with computed statistics)
    history = trans_fg.get_feature_monitoring_history(
        config_name="trans_fg_amount_monitoring",
        with_statistics=True,
    )
    ```

See the API reference for [`FeatureGroup.get_feature_monitoring_configs`][hsfs.feature_group.FeatureGroup.get_feature_monitoring_configs] and [`FeatureGroup.get_feature_monitoring_history`][hsfs.feature_group.FeatureGroup.get_feature_monitoring_history].

!!! info "Explore the API"
    The [`FeatureMonitoringConfig`][hsfs.core.feature_monitoring_config.FeatureMonitoringConfig] reference documents the full set of available methods, such as enabling or disabling a configuration, triggering it manually, or deleting it.
