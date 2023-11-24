# Helper columns

HSFS provides functionality to define two types of helper columns `inference_helper_columns` and `training_helper_columns` to [feature views](./overview.md).

`inference_helper_columns` are a list of feature names that are not used in training the model itself but are used to compute features during batch or online inference. For example in credit card fraud detection system 
features like days until credit card expires `days_until_card_expires` and distance between previous and current place of transaction `loc_delta_t_minus_1` need to be computed when new transaction arrives. Feature `days_until_card_expires` will be computed
using credit card expiry date `expiry_date` that is stored in credit card profile feature group and needs to be fetched from the feature store, as well as date of transaction `date_of_transaction` that arrives at request time. To compute `loc_delta_t_minus_1`
previous transaction coordinates `longitude` and `latitude` needs to fetched from the feature store and compared to new transaction coordinates that arrives at inference application. In this use case `expiry_date`, `date_of_transaction`, `longitude` and `latitude`
are `inference_helper_columns`. They are not used for training but are necessary for computing on-demand/derived features.

`training_helper_columns` are a list of feature names that are not the part of the model schema itself but are used during training for the extra information. For example one might want to use feature like `category` of the purchased 
product to assign different weights during the training time.

## Definition
Both inference and training helper column name(s) must be part of the `Query` object. If helper column name(s) belong to feature group that is part of a `Join` with `prefix` defined, then this prefix needs to prepended
to the original column name when defining helper column list.

=== "Python"

    !!! example "Define inference and training helper columns with feature views."
        ```python
        # define query object 
        query = label_fg.select("fraud_label")\
                        .join(cc_profile.select("expiry_date"))\
                        .join(trans_fg.select(["category", "amount",  "days_until_card_expires", "date_of_transaction"
                                               "locaton_delta", "longitude", "latitude", "category"])) \
                        .join(window_aggs_fg.select_except(["trans_volume_mstd", "trans_volume_mavg", "trans_freq", 
                                                            "loc_delta_mavg"]))
        
        # define feature view with helper columns
        feature_view = fs.get_or_create_feature_view(
            name='fv_with_helper_col',
            version=1,
            query=query,
            labels=["fraud_label"],
            transformation_functions=transformation_functions,
            inference_helper_columns=["longitude", "latitude", "date_of_transaction", "expiry_date" ],
            training_helper_columns=["category"]
        )
        ```

## Retrieval
When replaying a `Query` during model inference, helper columns will be omitted. However, they can be optionally fetched with inference or training data.

### Batch inference

=== "Python"

    !!! example "Fetch inference helper column values and compute on-demand features for batch inference."
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

        # compute time delta
        df['days_until_card_expires'] = df.apply(lambda row: time_delta(row['date_of_transaction'],  
                                                                        row['expiry_date']), axis=1)

        # prepare datatame for prediction
        df = df[[f.name for f in feature_view.features if not (f.label or f.inference_helper_column or f.training_helper_column)]]
        ```

### Online inference

=== "Python"

    !!! example "Fetch inference helper column values and compute on-demand features for online inference."
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

        # here current longitute and lattitude are longitude and latitude are provided as parameters to the application
        cc_num = ...
        longitude = ...
        latitute = ...
        date_of_transaction = ...
        
        # get previous transaction location of this credit card
        inference_helper = feature_view.get_inference_helper({"cc_num": cc_num}, return_type="dict")

        # compute location delta 
        loc_delta_t_minus_1 = location_delta(longitude, 
                                             latitute, 
                                             inference_helper['longitude'], 
                                             inference_helper['latitute'])

        # compute time delta 
        days_until_card_expires = time_delta(date_of_transaction,
                                             inference_helper['expiry_date'])

        # Now get assembled feature vector for prediction
        feature_vector = feature_view.get_feature_vector({"cc_num": cc_num}, 
                                                          passed_features={"loc_delta_t_minus_1": loc_delta_t_minus_1, 
                                                                           "days_until_card_expires": days_until_card_expires}
                                                         )
        ```


