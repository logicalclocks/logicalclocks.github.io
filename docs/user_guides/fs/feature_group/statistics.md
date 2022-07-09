# How to compute statistics on feature data

### Introduction

In this guide you will learn how to configure, compute and visualize statistics for the features registered with Hopsworks. 

Hopsworks groups features in four categories:

* **Descriptive**: These are the basic statistics Hopsworks computes. They include an _approximate_ count of the distinctive values and the completeness (i.e. the percentage of non null values). For numerical features Hopsworks also computes the minimum, maximum, mean, standard deviation and the sum of each feature. Enabled by default.

* **Histograms**: Hopsworks computes the distribution of the values of a feature. Exact histograms are computed as long as the number of distinct values is less than 20. If a feature has a numerical data type (e.g. integer, float, double, ...) and has more than 20 unique values, then the values are bucketed in 20 buckets and the histogram represents the distribution of values in those buckets. By default histograms are disabled.

* **Correlation**: If enabled, Hopsworks computes the Pearson correlation between features of numerical data type within a feature group. By default correlation is disabled.

* **Exact Statistics**: Exact statistics are an enhancement of the descriptive statistics that provide an exact count of distinctive values, entropy, uniqueness and distinctivness of the value of a feature. These statistics are more expensive to compute as they take into consideration all the values and they don't use approximations. By default they are disabled. 

When statistics are enabled, they are computed every time new data is written into the *offline* storage of a feature group. Statistics are then displayed on the Hopsworks UI and users can track how data has changed over time. 

## Prerequisites

Before you begin this guide we suggest you read the [Feature Group](../../../concepts/fs/feature_group/fg_overview.md) concept page to understand what a feature group is and how it fits in the ML pipeline. 
We also suggest you familiarize with the APIs to [create a feature group](./create.md).

## Enable statistics when creating a feature group 

As mentioned above, by default only descriptive statistics are enabled when creating a feature group. To enable histograms, correlations or exact statistics the `statistics_config` configuration parameter can be provided in the create statement.

The `statistics_config` parameter takes a dictionary with the keys: `enabled`, `correlations`, `histograms` and `exact_uniqueness` and, as values, a boolean to describe whether or not to compute the specific class of statistics.

Additionally it is possible to restrict the statistics computation to only a subset of columns. This is configurable by adding a `columns` key to the `statistics_config` parameter. The key should contain the list of columns for which to compute statistics. 
By default the value is empty list `[]` and the statistics are computed for all columns in the feature group.

=== "Python"

    ```python
    fg = feature_store.create_feature_group(name="weather",
        version=1,
        description="Weather Features",
        online_enabled=True,
        primary_key=['location_id'],
        partition_key=['day'],
        event_time='event_time',
        statistics_config={
            "enabled": True,
            "histograms": True,
            "correlations": True,
            "exact_uniqueness": False,
            "columns": []
        }
    )
    ```

## Enable statistics after creating a feature group

It is possible users to change the statistics configuration after a feature group was created. Either to add or remove a class of statistics, or to change the set of features for which to compute statistics.

=== "Python"

    ```python
    fg.statistics_config = {
            "enabled": True,
            "histograms": False,
            "correlations": False,
            "exact_uniqueness": False 
            "columns": ['location_id', 'min_temp', 'max_temp']
        }

    fg.update_statistics_config()
    ```

## Explicitly compute statistics

As mentioned above, the statistics are computed every time new data is written into the *offline* storage of a feature group. By invoking the `compute_statistics` method, users can trigger explicitly the statistics computation for the data available in a feature group.

This is useful when a feature group is receiving frequent updates. Users can schedule periodic statistics computation that take into consideration several data commits.

By default, the `compute_statistics` method computes statistics on the most recent version of the data available in a feature group. Users can provide a specific time using the `wallclock_time` parameter, to compute the statistics for a previous version of the data.

Hopsworks can compute statistics of external feature groups. As external feature groups are read only from an Hopsworks prospective, statistics computation can be triggered using the `compute_statistics` method.

=== "Python"

    ```python
    fg.compute_statistics(wallclock_time='20220611 20:00')
    ```

## Inspect statisitcs  

You can also create a new feature group through the UI.
