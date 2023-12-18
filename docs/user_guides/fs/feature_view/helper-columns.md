---
description: Using Helper columns in Feature View queries for online/batch inference and training dataset.
---

# Helper columns
Hopsworks Feature Store provides functionality to define two types of helper columns `inference_helper_columns` and `training_helper_columns` for [feature views](./overview.md).

!!! note
    Both inference and training helper column name(s) must be part of the `Query` object. If helper column name(s) belong to feature group that is part of a `Join` with `prefix` defined, then this prefix needs to prepended
    to the original column name when defining helper column list.

## Inference Helper columns
`inference_helper_columns` are a list of feature names that are not used for training the model itself but are used for extra information during online or batch inference. 
For example computing [on-demand feature](../../../concepts/fs/feature_group/on_demand_feature.md) like distance between previous and current place of transaction `loc_delta_t_minus_1` in credit card fraud detection system.
Feature `loc_delta_t_minus_1` will be computed using previous transaction coordinates `longitude` and `latitude` that needs to fetched from the feature store and compared to the new transaction coordinates that arrives at inference application. 
In this use case `longitude` and `latitude` are `inference_helper_columns`. They are not used for training but are necessary for computing [on-demand feature](../../../concepts/fs/feature_group/on_demand_feature.md) `loc_delta_t_minus_1`.

=== "Python"

    !!! example "Define inference columns for feature views."
        ```python
        # define query object 
        query = label_fg.select("fraud_label")\
                        .join(trans_fg.select(["amount", "loc_delta_t_minus_1", "longitude", "latitude", "category"])) 
        
        # define feature view with helper columns
        feature_view = fs.get_or_create_feature_view(
            name='fv_with_helper_col',
            version=1,
            query=query,
            labels=["fraud_label"],
            transformation_functions=transformation_functions,
            inference_helper_columns=["longitude", "latitude"],
        )
        ```

### Retrieval
When retrieving data for model inference, helper columns will be omitted. However, they can be optionally fetched with inference or training data.

#### Batch inference

=== "Python"

    !!! example "Fetch inference helper column values and compute on-demand features during batch inference."
        ```python

        # import feature functions
        from feature_functions import location_delta, time_delta
        
        # Fetch feature view object  
        feature_view = fs.get_feature_view(
            name='fv_with_helper_col',
            version=1,
        )

        # Fetch feature data for batch inference with helper columns
        df = feature_view.get_batch_data(start_time=start_time, end_time=end_time, inference_helpers=True)
        df['longitude_prev'] = df['longitude'].shift(-1)
        df['latitute_prev'] = df['latitute'].shift(-1)

        # compute location delta
        df['loc_delta_t_minus_1'] = df.apply(lambda row: location_delta(row['longitude'], 
                                                                        row['latitute'],
                                                                        row['longitude_prev'], 
                                                                        row['latitute_prev']), axis=1)

        # prepare datatame for prediction
        df = df[[f.name for f in feature_view.features if not (f.label or f.inference_helper_column or f.training_helper_column)]]
        ```

#### Online inference

=== "Python"

    !!! example "Fetch inference helper column values and compute on-demand features during online inference."
        ```python

        from feature_functions import location_delta, time_delta
        
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
        longitude = ...
        latitute = ...
        
        # get previous transaction location of this credit card
        inference_helper = feature_view.get_inference_helper({"cc_num": cc_num}, return_type="dict")

        # compute location delta 
        loc_delta_t_minus_1 = location_delta(longitude, 
                                             latitute, 
                                             inference_helper['longitude'], 
                                             inference_helper['latitute'])


        # Now get assembled feature vector for prediction
        feature_vector = feature_view.get_feature_vector({"cc_num": cc_num}, 
                                                          passed_features={"loc_delta_t_minus_1": loc_delta_t_minus_1}
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
                        .join(trans_fg.select(["amount", "loc_delta_t_minus_1", "longitude", "latitude", "category"])) 
        
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
When retrieving training data helper columns will be omitted. However, they can be optionally fetched.

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
