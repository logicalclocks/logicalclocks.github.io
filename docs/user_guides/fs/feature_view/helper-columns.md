---
description: Using Helper columns in Feature View queries for online/batch inference and training dataset.
---

# Helper columns

Hopsworks Feature Store provides a functionality to define two types of helper columns `inference_helper_columns` and `training_helper_columns` for [feature views](./overview.md).

!!! note
    Both inference and training helper column name(s) must be part of the `Query` object.
    If helper column name(s) belong to feature group that is part of a `Join` with `prefix` defined, then this prefix needs to prepended
    to the original column name when defining helper column list.

## Inference Helper columns

`inference_helper_columns` are a list of feature names that are not used for training the model itself but are used for extra information during online or batch inference.
For example, computing an [on-demand feature](../../../concepts/fs/feature_group/on_demand_feature.md) such as `days_valid` (days left that a credit card is valid at the time of the transaction)
in a credit card fraud detection system.
The feature `days_valid` will be computed using the credit card expiry date that needs to be fetched from the feature store and compared to the transaction
date that the transaction is performed on (`days_valid` = `expiry_date` - `current_date`).
In this use case `expiry_date` is an inference helper column.
It is not used for training but is necessary
for computing the [on-demand feature](../../../concepts/fs/feature_group/on_demand_feature.md)`days_valid` feature.

=== "Python"

    !!! example "Define inference columns for feature views."
        ```python
        # define query object
        query = label_fg.select("fraud_label")\
                        .join(trans_fg.select(["amount", "days_valid", "expiry_date", "category"]))

        # define feature view with helper columns
        feature_view = fs.get_or_create_feature_view(
            name='fv_with_helper_col',
            version=1,
            query=query,
            labels=["fraud_label"],
            transformation_functions=transformation_functions,
            inference_helper_columns=["expiry_date"],
        )
        ```

### Retrieval

When retrieving data for model inference, helper columns will be omitted.
However, they can be optionally fetched with inference or training data.

#### Batch inference

=== "Python"

    !!! example "Fetch inference helper column values and compute on-demand features during batch inference."
        ```python

        # import feature functions
        from feature_functions import time_delta

        # Fetch feature view object
        feature_view = fs.get_feature_view(
            name='fv_with_helper_col',
            version=1,
        )

        # Fetch feature data for batch inference with helper columns
        df = feature_view.get_batch_data(start_time=start_time, end_time=end_time, inference_helpers=True, event_time=True)

        # compute location delta
        df['days_valid'] = df.apply(lambda row: time_delta(row['expiry_date'], row['transaction_date']), axis=1)

        # prepare datatame for prediction
        df = df[[f.name for f in feature_view.features if not (f.label or f.inference_helper_column or f.training_helper_column)]]
        ```

#### Online inference

=== "Python"

    !!! example "Fetch inference helper column values and compute on-demand features during online inference."
        ```python

        from feature_functions import time_delta

        # Fetch feature view object
        feature_view = fs.get_feature_view(
            name='fv_with_helper_col',
            version=1,
        )

        # Fetch feature data for batch inference without helper columns
        df_without_inference_helpers = feature_view.get_batch_data()

        # Fetch feature data for batch inference with helper columns
        df_with_inference_helpers = feature_view.get_batch_data(inference_helpers=True)

        # here cc_num, longitute and lattitude are provided as parameters to the application
        cc_num = ...
        transaction_date = ...

        # get previous transaction location of this credit card
        inference_helper = feature_view.get_inference_helper({"cc_num": cc_num}, return_type="dict")

        # compute location delta
        days_valid = time_delta(transaction_date, inference_helper['expiry_date'])

        # Now get assembled feature vector for prediction
        feature_vector = feature_view.get_feature_vector({"cc_num": cc_num},
                                                          passed_features={"days_valid": days_valid}
                                                         )
        ```

## Training Helper columns

`training_helper_columns` are a list of feature names that are not the part of the model schema itself but are used during training for the extra information.
For example one might want to use feature like `category` of the purchased product to assign different weights.

=== "Python"

    !!! example "Define training helper columns for feature views."
        ```python
        # define query object
        query = label_fg.select("fraud_label")\
                        .join(trans_fg.select(["amount", "days_valid", "expiry_date", "category"]))

        # define feature view with helper columns
        feature_view = fs.get_or_create_feature_view(
            name='fv_with_helper_col',
            version=1,
            query=query,
            labels=["fraud_label"],
            transformation_functions=transformation_functions,
            training_helper_columns=["category"]
        )
        ```

### Retrieval

When retrieving training data helper columns will be omitted.
However, they can be optionally fetched.

=== "Python"

    !!! example "Fetch training data with or without inference helper column values."
        ```python

        # import feature functions
        from feature_functions import location_delta, time_delta

        # Fetch feature view object
        feature_view = fs.get_feature_view(
            name='fv_with_helper_col',
            version=1,
        )

        # Create and training data with training helper columns
        TEST_SIZE = 0.2
        X_train, X_test, y_train, y_test = feature_view.train_test_split(
            description='transactions fraud training dataset',
            test_size=TEST_SIZE,
             training_helper_columns=True
        )

        # Get existing training data with training helper columns
        X_train, X_test, y_train, y_test = feature_view.get_train_test_split(
             training_dataset_version=1,
             training_helper_columns=True
        )
        ```

!!! note
    To use helper columns with materialized training dataset it needs to be created with `training_helper_columns=True`.
