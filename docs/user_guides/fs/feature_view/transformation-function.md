# Transformation Functions

HSFS provides functionality to attach transformation functions to [feature views](./overview.md).

User defined, custom transformation functions need to be registered in the feature store to make them accessible for feature view creation. To register them in the feature store, they either have to be part of the library [installed](https://hopsworks.readthedocs.io/en/stable/user_guide/hopsworks/python.html?highlight=install#installing-libraries) in Hopsworks or attached when starting a [Jupyter notebook](https://hopsworks.readthedocs.io/en/stable/user_guide/hopsworks/jupyter.html?highlight=jupyter) or [Hopsworks job](https://hopsworks.readthedocs.io/en/stable/user_guide/hopsworks/jobs.html).

!!! warning "Pyspark decorators"

    Don't decorate transformation functions with Pyspark `@udf` or `@pandas_udf`, and also make sure not to use any Pyspark dependencies. That is because, the transformation functions may be executed by Python clients. HSFS will decorate transformation function for you only if it is used inside Pyspark application.


## Creation
Hopsworks ships built-in transformation functions such as `min_max_scaler`, `standard_scaler`, `robust_scaler` and `label_encoder`. 

You can also create new functions. Let's assume that you have already installed Python library [transformation_fn_template](https://github.com/logicalclocks/transformation_fn_template) containing the transformation function `plus_one`.

=== "Python"

    !!! example "Register transformation function  `plus_one` in the Hopsworks feature store."
        ```python
        from custom_functions import transformations
        plus_one_meta = fs.create_transformation_function(
                    transformation_function=transformations.plus_one,
                    output_type=int,
                    version=1)
        plus_one_meta.save()
        ```

## Retrieval
To retrieve all transformation functions from the feature store, use `get_transformation_functions` which will return the list of available `TransformationFunction` objects. A specific transformation function can be retrieved with the `get_transformation_function` method where you can provide its name and version of the transformation function. If only the function name is provided then it will default to version 1.

=== "Python"

    !!! example "Retrieving transformation functions from the feature store"
        ```python
        # get all transformation functions
        fs.get_transformation_functions()

        # get transformation function by name. This will default to version 1
        plus_one_fn = fs.get_transformation_function(name="plus_one")

        # get built-in transformation function min max scaler
        min_max_scaler_fn = fs.get_transformation_function(name="min_max_scaler")

        # get transformation function by name and version.
        plus_one_fn = fs.get_transformation_function(name="plus_one", version=2)
        ```

## Apply transformation functions to features

You can define in the feature view transformation functions as dict, where key is feature name and value is online transformation function name. Then the transformation functions are applied when you [read training data](./training-data.md#read-training-data), [read batch data](./batch-data.md#creation-with-transformation), or [get feature vectors](./feature-vectors.md#retrieval-with-transformation).

=== "Python"

    !!! example "Attaching transformation functions to the feature view"
        ```python
        plus_one_fn = fs.get_transformation_function(name="plus_one", version=1)
        feature_view = fs.create_feature_view(
            name='transactions_view',
            query=query,
            labels=["fraud_label"],
            transformation_functions={
                "amount_spent": plus_one_fn
            }
        )
        ```

Built-in transformation functions are attached in the same way. The only difference is that it will compute the necessary statistics for the specific function in the background. For example min and max values for `min_max_scaler`; mean and standard deviation for `standard_scaler` etc.

=== "Python"

    !!! example "Attaching built-in transformation functions to the feature view"
        ```python
        min_max_scaler = fs.get_transformation_function(name="min_max_scaler")
        standard_scaler = fs.get_transformation_function(name="standard_scaler")
        robust_scaler = fs.get_transformation_function(name="robust_scaler")
        label_encoder = fs.get_transformation_function(name="label_encoder")
        
        feature_view = fs.create_feature_view(
            name='transactions_view',
            query=query,
            labels=["fraud_label"],
            transformation_functions = {
                "category": label_encoder,
                "amount": robust_scaler,
                "loc_delta": min_max_scaler,
                "age_at_transaction": standard_scaler
            }
        )
        ```

!!! warning "Java/Scala support"

    Creating and attaching Transformation functions to feature views are not supported for HSFS Java or Scala client. If feature view with transformation function was created using python client, you cannot get training data or get feature vectors from HSFS Java or Scala client.