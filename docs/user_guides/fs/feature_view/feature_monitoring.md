# Feature Monitoring for Feature Views

Feature Monitoring complements the Hopsworks data validation capabilities for Feature Group data by allowing you to monitor your data once they have been ingested into the Feature Store. Hopsworks feature monitoring is centered around two functionalities: **scheduled statistics** and **statistics comparison**.

Before continuing with this guide, see the [Feature monitoring guide](../feature_monitoring/index.md) to learn more about how feature monitoring works, and get familiar with the different use cases of feature monitoring for Feature Views described in the **Use cases** sections of the [Scheduled statistics guide](../feature_monitoring/scheduled_statistics.md#use-cases) and [Statistics comparison guide](../feature_monitoring/statistics_comparison.md#use-cases).

!!! warning "Limited UI support"
    Currently, feature monitoring can only be configured using the [Hopsworks Python library](https://pypi.org/project/hopsworks). However, you can enable/disable a feature monitoring configuration or trigger the statistics comparison manually from the UI, as shown in the [Advanced guide](../feature_monitoring/feature_monitoring_advanced.md).

## Code

In this section, we show you how to setup feature monitoring in a Feature View using the ==Hopsworks Python library==. Alternatively, you can get started quickly by running our [tutorial for feature monitoring](https://github.com/logicalclocks/hopsworks-tutorials/blob/master/integrations/feature-monitoring/feature-monitoring.ipynb).

First, checkout the pre-requisite and Hopsworks setup to follow the guide below. Create a project, install the [Hopsworks Python library](https://pypi.org/project/hopsworks) in your environment and connect via the generated API key. The second step is to start a new configuration for feature monitoring. 

After that, you can optionally define a detection window of data to compute statistics on, or use the default detection window (i.e., whole feature data). If you want to setup scheduled statistics alone, you can jump to the last step to save your configuration. Otherwise, the third and fourth steps are also optional and show you how to setup the comparison of statistics on a schedule by defining a reference window and specifying the statistics metric to be compared.

### Step 1: Pre-requisite

In order to setup feature monitoring for a Feature View, you will need:

- A Hopsworks project. If you don't have a project yet you can go to [managed.hopsworks.ai](https://managed.hopsworks.ai), signup with your email and create your first project.
- An API key, you can get one by following the instructions [here](../../../setup_installation/common/api_key.md)
- The [Hopsworks Python library](https://pypi.org/project/hopsworks) installed in your client. See the [installation guide](../../client_installation/index.md).
- A Feature View
- A Training Dataset

#### Connect your notebook to Hopsworks

Connect the client running your notebooks to Hopsworks.

=== "Python"
    ```python3
    import hopsworks

    project = hopsworks.login()

    fs = project.get_feature_store()
    ```

You will be prompted to paste your API key to connect the notebook to your project. The `fs` Feature Store entity is now ready to be used to insert or read data from Hopsworks.

#### Get or create a Feature View

Feature monitoring can be enabled on already created Feature Views. We suggest you read the [Feature View](../../../concepts/fs/feature_view/fv_overview.md) concept page to understand what a feature view is. We also suggest you familiarize with the APIs to [create a feature view](overview.md) and how to create them using the [query abstraction](query.md).

The following is a code example for getting or creating a Feature View with name `trans_fv` for transaction data.

=== "Python"

    ```python3
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

#### Get or create a Training Dataset

The following is a code example for creating a training dataset with two splits using a previously created feature view.

=== "Python"

    ```python3
    # Create a training dataset with train and test splits
    _, _ = trans_fv.create_train_validation_test_split(
        description = 'transactions fraud batch training dataset',
        data_format = 'csv',
        validation_size = 0.2,
        test_size = 0.1,
    )
    ```

### Step 2: Initialize configuration

#### Scheduled statistics

You can setup statistics monitoring on a ==single feature or multiple features== of your Feature Group data, included in your Feature View query.

=== "Python"
    ```python3
    # compute statistics for all the features
    fg_monitoring_config = trans_fv.create_statistics_monitoring(
        name="trans_fv_all_features_monitoring",
        description="Compute statistics on all data of all features of the Feature Group data on a daily basis",
    )

    # or for a single feature
    fg_monitoring_config = trans_fv.create_statistics_monitoring(
        name="trans_fv_amount_monitoring",
        description="Compute statistics on all data of a single feature of the Feature Group data on a daily basis",
        feature_name="amount",
    )
    ```

#### Statistics comparison

When enabling the comparison of statistics in a feature monitoring configuration, you need to specify a ==single feature== of your Feature Group data, included in your Feature View query. You can create multiple feature monitoring configurations on the same Feature View, but each of them should point to a single feature in the Feature View query.

=== "Python"
    ```python3
    fg_monitoring_config = trans_fv.create_feature_monitoring(
        name="trans_fv_amount_monitoring",
        feature_name="amount",
        description="Compute descriptive statistics on the amount Feature of the Feature Group data on a daily basis",
    )
    ```

#### Custom schedule or percentage of window data

By default, the computation of statistics is scheduled to run endlessly, every day at 12PM. You can modify the default schedule by adjusting the `cron_expression`, `start_date_time` and `end_date_time` parameters.

=== "Python"
    ```python3
    fg_monitoring_config = trans_fv.create_statistics_monitoring(
        name="trans_fv_all_features_monitoring",
        description="Compute statistics on all data of all features of the Feature Group data on a weekly basis",
        cron_expression="0 0 12 ? * MON *",  # weekly 
        row_percentage=0.8,                  # use 80% of the data
    )

    # or
    fg_monitoring_config = trans_fv.create_feature_monitoring(
        name="trans_fv_amount_monitoring",
        feature_name="amount",
        description="Compute descriptive statistics on the amount Feature of the Feature Group data on a weekly basis",
        cron_expression="0 0 12 ? * MON *",  # weekly 
        row_percentage=0.8,                  # use 80% of the data
    )
    ```

### Step 3: (Optional) Define a detection window

By default, the detection window is an _expanding window_ covering the whole Feature Group data. You can define a different detection window using the `window_length` and `time_offset` parameters provided in the `with_detection_window` method. Additionally, you can specify the percentage of feature data on which statistics will be computed using the `row_percentage` parameter.

=== "Python"
    ```python3
    fm_monitoring_config.with_detection_window(
        window_length="1w",  # data ingested during one week
        time_offset="1w",    # starting from last week
        row_percentage=0.8,  # use 80% of the data
    )
    ```

### Step 4: (Optional) Define a reference window

When setting up feature monitoring for a Feature View, reference windows can be either a regular window, a specific value (i.e., window of size 1) or a training dataset.

=== "Python"
    ```python3
    # compare statistics against a reference window
    fm_monitoring_config.with_reference_window(
        window_length="1w",  # data ingested during one week
        time_offset="2w",    # starting from two weeks ago
        row_percentage=0.8,  # use 80% of the data
    )

    # or a specific value
    fm_monitoring_config.with_reference_value(
        value=100,
    )

    # or a training dataset
    fm_monitoring_config.with_reference_training_dataset(
        training_dataset_version=1, # use the training dataset used to train your production model
    )
    ```

### Step 5: (Optional) Define the statistics comparison criteria

In order to compare detection and reference statistics, you need to provide the criteria for such comparison. First, you select the metric to consider in the comparison using the `metric` parameter. Then, you can define a relative or absolute threshold using the `threshold` and `relative` parameters.

=== "Python"
    ```python3
    fm_monitoring_config.compare_on(
        metric="mean", 
        threshold=0.2,  # a relative change over 20% is considered anomalous
        relative=True,  # relative or absolute change
        strict=False,   # strict or relaxed comparison
    )
    ```

!!! info "Difference values and thresholds"
    For more information about the computation of difference values and the comparison against threshold bounds see the [Comparison criteria section](../feature_monitoring/statistics_comparison.md#comparison-criteria) in the Statistics comparison guide.


### Step 6: Save configuration

Finally, you can save your feature monitoring configuration by calling the `save` method. Once the configuration is saved, the schedule for the statistics computation and comparison will be activated automatically.

=== "Python"
    ```python3
    fm_monitoring_config.save()
    ```

!!! info "Next steps"
    See the [Advanced guide](../feature_monitoring/feature_monitoring_advanced.md) to learn how to delete, disable or trigger feature monitoring manually.