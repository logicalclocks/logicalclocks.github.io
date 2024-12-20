# Model Dependent Transformation Functions


[Model-dependent transformations](https://www.hopsworks.ai/dictionary/model-dependent-transformations) transform feature data for a specific model. Feature encoding is one example of such a transformations. Feature encoding is parameterized by statistics from the training dataset, and, as such, many model-dependent transformations require the training dataset statistics as a parameter. Hopsworks enhances the robustness of AI pipelines by preventing [training-inference skew](https://www.hopsworks.ai/dictionary/training-inference-skew) by ensuring that the same model-dependent transformations and statistical parameters are used during both training dataset generation and online inference.

Additionally, Hopsworks offers built-in model-dependent transformation functions, such as `min_max_scaler`, `standard_scaler`, `robust_scaler`, `label_encoder`, and `one_hot_encoder`, which can be easily imported and declaratively applied to features in a feature view.

## Model Dependent Transformation Function Creation

Hopsworks allows you to create a model-dependent transformation function by attaching a [transformation function](../transformation_functions.md) to a feature view. The attached transformation function can be a simple function that takes one feature as input and outputs the transformed feature data. For example, in the case of min-max scaling a numerical feature, you will have a number as input parameter to the transformation function and a number as output. However, in the case of one-hot encoding a categorical variable, you will have a string as input and an array of 1s and 0s and output. You can also have transformation functions that take multiple features as input and produce one or more values as output. That is, transformation functions can be one-to-one, one-to-many, many-to-one, or many-to-many.

Each model-dependent transformation function can map specific features to its arguments by explicitly providing their names as arguments to the transformation function. If no feature names are provided, the transformation function will default to using features from the feature view that match the name of the transformation function's argument.

Hopsworks by default generates default names of transformed features output by a model-dependent transformation function. The generated names follows a naming convention structured as `functionName_features_outputColumnNumber` if the transformation function outputs multiple columns and `functionName_features` if the transformation function outputs one column. For instance, for the function named `add_one_multiple` that outputs multiple columns in the example given below, produces output columns that would be labeled as  `add_one_multiple_feature1_feature2_feature3_0`,  `add_one_multiple_feature1_feature2_feature3_1`  and   `add_one_multiple_feature1_feature2_feature3_2`. The function named `add_two` that outputs a single column in the example given below, produces a single output column names as `add_two_feature`. Additionally, Hopsworks also allows users to specify custom names for transformed feature using the [`alias`](../transformation_functions.md#specifying-output-features–names-for-transformation-functions) function.


=== "Python"

    !!! example "Creating model-dependent transformation functions"
        ```python
        # Defining a many to many transformation function.
        @udf(return_type=[int, int, int], drop=["feature1", "feature3"])
        def add_one_multiple(feature1, feature2, feature3):
            return pd.DataFrame({"add_one_feature1":feature1 + 1, "add_one_feature2":feature2 + 1, "add_one_feature3":feature3 + 1})
        
        # Defining a one to one transformation function.
        @udf(return_type=int)
        def add_two(feature):
            return feature + 2

        # Creating model-dependent transformations by attaching transformation functions to feature views.
        feature_view = fs.create_feature_view(
            name='transactions_view',
            query=query,
            labels=["fraud_label"],
            transformation_functions=[
                add_two,
                add_one_multiple
            ]
        )
        ```

### Specifying input features

The features to be used by a model-dependent transformation function can be specified by providing the feature names (from the feature view / feature group) as input to the transformation functions. 


=== "Python"

    !!! example "Specifying input features to be passed to a model-dependent transformation function"
        ```python
        feature_view = fs.create_feature_view(
            name='transactions_view',
            query=query,
            labels=["fraud_label"],
            transformation_functions=[
                add_two("feature_1"),
                add_two("feature_2"),
                add_one_multiple("feature_5", "feature_6", "feature_7")
            ]
        )
        ```

### Using built-in transformations

Built-in transformation functions are attached in the same way. The only difference is that they can either be retrieved from the Hopsworks or imported from the `hopsworks` module.

=== "Python"

    !!! example "Creating model-dependent transformation using built-in transformation functions retrieved from Hopsworks"
        ```python
        min_max_scaler = fs.get_transformation_function(name="min_max_scaler")
        standard_scaler = fs.get_transformation_function(name="standard_scaler")
        robust_scaler = fs.get_transformation_function(name="robust_scaler")
        label_encoder = fs.get_transformation_function(name="label_encoder")
        
        feature_view = fs.create_feature_view(
            name='transactions_view',
            query=query,
            labels=["fraud_label"],
            transformation_functions = [
                label_encoder("category"),
                robust_scaler("amount"),
                min_max_scaler("loc_delta"),
                standard_scaler("age_at_transaction")
            ]
        )
        ```

To attach built-in transformation functions from the `hopsworks` module they can be directly imported into the code from `hopsworks.builtin_transformations`.

=== "Python"

    !!! example "Creating model-dependent transformation using built-in transformation functions imported from hopsworks"
        ```python
        from hopsworks.builtin_transformations import min_max_scaler, label_encoder, robust_scaler, standard_scaler
        
        feature_view = fs.create_feature_view(
            name='transactions_view',
            query=query,
            labels=["fraud_label"],
            transformation_functions = [
                label_encoder("category": ),
                robust_scaler("amount"),
                min_max_scaler("loc_delta"),
                standard_scaler("age_at_transaction")
            ]
        )
        ```


## Using Model Dependent Transformations

Model-dependent transformations attached to a feature view are automatically applied when you [create training data](./training-data.md#creation), [read training data](./training-data.md#read-training-data), [read batch inference data](./batch-data.md#creation-with-transformation), or [get feature vectors](./feature-vectors.md#retrieval-with-transformation). The generated data includes untransformed features, on-demand features, if any, and the transformed features. The transformed features are organized by their output column names in alphabetical order and are positioned after the untransformed and on-demand features. 

Model-dependent transformation functions can also be manually applied to a feature vector using the `transform` function. 

=== "Python"

    !!! example "Manually applying model-dependent transformations during online inference"
        ```python
        # Initialize the feature view with the correct training dataset version used for model-dependent transformations
        fv.init_serving(training_dataset_version)

        # Get untransformed feature Vector
        feature_vector = fv.get_feature_vector(entry={"index":10}, transformed=False, return_type="pandas")

        # Apply Model Dependent transformations
        encode_feature_vector = fv.transform(feature_vector)
        ```

