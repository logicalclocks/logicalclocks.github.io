# On-Demand Transformation Functions

[On-demand transformations](https://www.hopsworks.ai/dictionary/on-demand-transformation) produce on-demand features, which usually require parameters accessible during inference for their calculation.
Hopsworks facilitates the creation of on-demand transformations without introducing [online-offline skew](https://www.hopsworks.ai/dictionary/online-offline-feature-skew), ensuring consistency while allowing their dynamic computation during online inference.

## On Demand Transformation Function Creation

An on-demand transformation function may be created by associating a [transformation function](../transformation_functions.md) with a feature group.
Each on-demand transformation function can generate one or multiple on-demand features.
If the on-demand transformation function returns a single feature, it is automatically assigned the same name as the transformation function.
However, if it returns multiple features, they are by default named using the format `functionName_outputColumnNumber`.
For instance, in the example below, the on-demand transformation function `transaction_age` produces an on-demand feature named `transaction_age` and the on-demand transformation function `stripped_strings` produces the on-demand features names `stripped_strings_0` and `stripped_strings_1`.
Alternatively, the name of the resulting on-demand feature can be explicitly defined using the [`alias`](../transformation_functions.md#specifying-output-features-names-for-transformation-functions) function.

!!! warning "On-demand transformation"
    All on-demand transformation functions attached to a feature group must have unique names and, in contrast to model-dependent transformations, they do not have access to training dataset statistics.

Each on-demand transformation function can map specific features to its arguments by explicitly providing their names as arguments to the transformation function.
If no feature names are provided, the transformation function will default to using features that match the name of the transformation function's argument.

=== "Python"
!!! example "Creating on-demand transformation functions."
    ```python
    # Define transformation function
    @hopsworks.udf(return_type=int, drop=["current_date"])
    def transaction_age(transaction_date, current_date):
        return (current_date - transaction_date).dt.days

    @hopsworks.udf(return_type=[str, str], drop=["current_date"])
    def stripped_strings(country, city):
        return country.strip(), city.strip()

    # Attach transformation function to feature group to create on-demand transformation function.
    fg = feature_store.create_feature_group(name="fg_transactions",
                version=1,
                description="Transaction Features",
                online_enabled=True,
                primary_key=['id'],
                event_time='event_time',
                transformation_functions=[transaction_age, stripped_strings]
                )
    ```

### Specifying input features

The features to be used by the on-demand transformation function can be specified by providing the feature names as input to the transformation functions.

=== "Python"
!!! example "Creating on-demand transformations by specifying features to be passed to transformation function."
    ```python
    fg = feature_store.create_feature_group(name="fg_transactions",
                version=1,
                description="Transaction Features",
                online_enabled=True,
                primary_key=['id'],
                event_time='event_time',
                transformation_functions=[age_transaction('transaction_time', 'current_time')]
                )
    ```

## Usage

On-demand transformation functions attached to a feature group are automatically executed in the feature pipeline when you [insert data](./create.md#batch-write-api) into a feature group and [by the Python client while retrieving feature vectors](../feature_view/feature-vectors.md#retrieval) for online inference using feature views that contain on-demand features.

The on-demand features computed by on-demand transformation functions are positioned after all other features in a feature group and are ordered alphabetically by their names.

### Inserting data

All on-demand transformation functions attached to a feature group are executed whenever new data is inserted.
This process computes on-demand features from historical data.
The DataFrame used for insertion must include all features required for executing all on-demand transformation functions in the feature group.

Inserting on-demand features as historical features saves time and computational resources by removing the need to compute all on-demand features while generating training or batch data.

### Accessing on-demand features in feature views

A feature view can include on-demand features from feature groups by selecting them in the [query](../feature_view/query.md) used to create the feature view.
These on-demand features are equivalent to regular features, and [model-dependent transformations](../feature_view/model-dependent-transformations.md) can be applied to them if required.

=== "Python"
!!! example "Creating feature view with on-demand features"
    ```python

    # Selecting on-demand features in query
    query = fg.select(["id", "feature1", "feature2", "on_demand_feature3", "on_demand_feature4"])

    # Creating a feature view using a query that contains on-demand transformations and model-dependent transformations
    feature_view = fs.create_feature_view(
            name='transactions_view',
            query=query,
            transformation_functions=[
                min_max_scaler("feature1"),
                min_max_scaler("on_demand_feature3"),
            ]
        )
    ```

### Computing on-demand features

On-demand features in the feature view are computed in real-time during online inference using the same on-demand transformation functions used to create them.
Hopsworks, by default, automatically computes all on-demand features when retrieving feature view input features (feature vectors) with the functions `get_feature_vector` and `get_feature_vectors`.
Additionally, on-demand features can be computed using the `compute_on_demand_features` function or by manually executing the same on-demand transformation function.

The values for the input parameters required to compute on-demand features can be provided using the `request_parameters` argument.
If values are not provided through the `request_parameters` argument, the transformation function will verify if the feature vector contains the necessary input parameters and will use those values instead.
However, if the required input parameters are also not present in the feature vector, an error will be thrown.

!!! note
    By default the functions `get_feature_vector` and `get_feature_vectors` will apply model-dependent transformation present in the feature view after computing on-demand features.

#### Retrieving a feature vector

The `get_feature_vector` function retrieves a single feature vector based on the feature view's serving key(s).
The on-demand features in the feature vector can be computed using real-time data by passing a dictionary that associates the name of each input parameter needed for the on-demand transformation function with its respective new value to the `request_parameter` argument.

=== "Python"
!!! example "Computing on-demand features while retrieving a feature vector"
    ```python
    feature_vector = feature_view.get_feature_vector(
        entry={"id": 1},
        request_parameter={
            "transaction_time": datetime(2022, 12, 28, 23, 55, 59),
            "current_time": datetime.now(),
        },
    )
    ```

#### Retrieving feature vectors

The `get_feature_vectors` function retrieves multiple feature vectors using a list of feature view serving keys.
The `request_parameter` in this case, can be a list of dictionaries that specifies the input parameters for the computation of on-demand features for each serving key or can be a dictionary if the on-demand transformations require the same parameters for all serving keys.

=== "Python"
!!! example "Computing on-demand features while retrieving a feature vectors"
    ```python
    # Specify unique request parameters for each serving key.
    feature_vector = feature_view.get_feature_vectors(
        entry=[{"id": 1}, {"id": 2}],
        request_parameter=[
            {
                "transaction_time": datetime(2022, 12, 28, 23, 55, 59),
                "current_time": datetime.now(),
            },
            {
                "transaction_time": datetime(2022, 11, 20, 12, 50, 00),
                "current_time": datetime.now(),
            },
        ],
    )

    # Specify common request parameters for all serving key.
    feature_vector = feature_view.get_feature_vectors(
        entry=[{"id": 1}, {"id": 2}],
        request_parameter={
            "transaction_time": datetime(2022, 12, 28, 23, 55, 59),
            "current_time": datetime.now(),
        },
    )
    ```

#### Retrieving feature vector without on-demand features

The `get_feature_vector` and `get_feature_vectors` methods can return untransformed feature vectors without on-demand features by disabling model-dependent transformations and excluding on-demand features.
To achieve this, set the  parameters `transform` and `on_demand_features` to `False`.

=== "Python"
!!! example "Returning untransformed feature vectors"
    ```python
    untransformed_feature_vector = feature_view.get_feature_vector(
        entry={"id": 1}, transform=False, on_demand_features=False
    )
    untransformed_feature_vectors = feature_view.get_feature_vectors(
        entry=[{"id": 1}, {"id": 2}], transform=False, on_demand_features=False
    )
    ```

#### Compute all on-demand features

The `compute_on_demand_features` function computes all on-demand features attached to a feature view and adds them to the feature vectors provided as input to the function.
This function does not apply model-dependent transformations to any of the features.
The `transform` function can be used to apply model-dependent transformations to the returned values if required.

The `request_parameter` in this case, can be a list of dictionaries that specifies the input parameters for the computation of on-demand features for each feature vector given as input to the function or can be a dictionary if the on-demand transformations require the same parameters for all input feature vectors.

=== "Python"
!!! example "Computing all on-demand features and manually applying model dependent transformations."
    ```python
    # Specify request parameters for each serving key.
    untransformed_feature_vector = feature_view.get_feature_vector(
        entry={"id": 1}, transform=False, on_demand_features=False
    )

    # re-compute and add on-demand features to the feature vector
    feature_vector_with_on_demand_features = fv.compute_on_demand_features(
        untransformed_feature_vector,
        request_parameter={
            "transaction_time": datetime(2022, 12, 28, 23, 55, 59),
            "current_time": datetime.now(),
        },
    )

    # Applying model dependent transformations
    encoded_feature_vector = fv.transform(feature_vector_with_on_demand_features)

    # Specify request parameters for each serving key.
    untransformed_feature_vectors = feature_view.get_feature_vectors(
        entry=[{"id": 1}, {"id": 2}], transform=False, on_demand_features=False
    )

    # re-compute and add on-demand features to the feature vectors - Specify unique request parameter for each feature vector
    feature_vectors_with_on_demand_features = fv.compute_on_demand_features(
        untransformed_feature_vectors,
        request_parameter=[
            {
                "transaction_time": datetime(2022, 12, 28, 23, 55, 59),
                "current_time": datetime.now(),
            },
            {
                "transaction_time": datetime(2022, 11, 20, 12, 50, 00),
                "current_time": datetime.now(),
            },
        ],
    )

    # re-compute and add on-demand feature to the feature vectors - Specify common request parameter for all feature vectors
    feature_vectors_with_on_demand_features = fv.compute_on_demand_features(
        untransformed_feature_vectors,
        request_parameter={
            "transaction_time": datetime(2022, 12, 28, 23, 55, 59),
            "current_time": datetime.now(),
        },
    )

    # Applying model dependent transformations
    encoded_feature_vector = fv.transform(feature_vectors_with_on_demand_features)

    ```

#### Compute one on-demand feature

On-demand transformation functions can also be accessed and executed as normal functions by using the dictionary `on_demand_transformations` that maps the on-demand features to their corresponding on-demand transformation function.

=== "Python"
!!! example "Executing each on-demand transformation function"
    ```python
    # Specify request parameters for each serving key.
    feature_vector = feature_view.get_feature_vector(
        entry={"id": 1}, transform=False, on_demand_features=False, return_type="pandas"
    )

    # Applying model dependent transformations
    feature_vector["on_demand_feature1"] = fv.on_demand_transformations[
        "on_demand_feature1"
    ](feature_vector["transaction_time"], datetime.now())

    ```
