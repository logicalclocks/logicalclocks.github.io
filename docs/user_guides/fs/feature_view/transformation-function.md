# Model Dependent Transformation Functions

Hopsworks provides functionality to attach transformation functions to [feature views](./overview.md).

These transformation functions are primarily [model-dependent transformations](https://www.hopsworks.ai/dictionary/model-dependent-transformations). Model-dependent transformations generate feature data tailored to a specific model, often requiring the computation of training dataset statistics. Hopsworks enables you to define custom model-dependent transformation functions that can take multiple features and their associated statistics as input and produce multiple transformed features as output. Hopsworks also automatically executes the defined transformation function as a [`@pandas_udf`]((https://spark.apache.org/docs/3.1.2/api/python/reference/api/pyspark.sql.functions.pandas_udf.html)) in a PySpark application and as Pandas functions in Python clients.

Custom transformation functions created in Hopsworks can be directly attached to feature views or stored in the feature store for later retrieval and attachment. These custom functions can be part of a library [installed](../../../user_guides/projects/python/python_install.md) in Hopsworks or added when starting a [Jupyter notebook](../../../user_guides/projects/jupyter/python_notebook.md) or [Hopsworks job](../../../user_guides/projects/jobs/spark_job.md).

Hopsworks also includes built-in transformation functions such as `min_max_scaler`, `standard_scaler`, `robust_scaler`, `label_encoder`, and `one_hot_encoder` that can be easily imported and used.

!!! warning "Pyspark decorators"

    Don't decorate transformation functions with Pyspark `@udf` or `@pandas_udf`, and also make sure not to use any Pyspark dependencies. That is because, the transformation functions may be executed by Python clients. Hopsworks will automatically run transformations as pandas udfs for you only if it is used inside Pyspark application.   

!!! warning "Java/Scala support"

    Creating and attaching Transformation functions to feature views are not supported for HSFS Java or Scala client. If feature view with transformation function was created using python client, you cannot get training data or get feature vectors from HSFS Java or Scala client.


## Creation of Custom Transformation Functions

User-defined, custom transformation functions can be created in Hopsworks using the `@udf` decorator. These functions should be designed as Pandas functions, meaning they must take input features as a [Pandas Series](https://pandas.pydata.org/docs/reference/api/pandas.Series.html) and return either a Pandas Series or a [Pandas DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html).

The `@udf` decorator in Hopsworks creates a metadata class called `HopsworksUdf`. This class manages the necessary operations to supply feature statistics to custom transformation functions and execute them as `@pandas_udf` in PySpark applications or as pure Pandas functions in Python clients. The decorator requires the `return_type` of the transformation function, which indicates the type of features returned. This can be a single Python type if the transformation function returns a single transformed feature as a Pandas Series, or a list of Python types if it returns multiple transformed features as a Pandas DataFrame. The supported types include `str`, `int`, `float`, `bool`, `datetime.datetime`, `datetime.date`, and `datetime.time`.

Hopsworks supports four types of transformation functions:

1. One to One: Transforms one feature into one transformed feature.
2. One to Many: Transforms one feature into multiple transformed features.
3. Many to One: Transforms multiple features into one transformed feature.
4. Many to Many: Transforms multiple features into multiple transformed features.

To create a One to One transformation function, the hopsworks `@udf` decorator must be provided with the return type as a Python type and the transformation function should take one argument as input and return a Pandas Series.

=== "Python"

    !!! example "Creation of a Custom One to One Transformation Function in Hopsworks."
        ```python
        from hopsworks import udf

        @udf(int)
        def add_one(feature):
            return feature + 1
        ```

Creation of a Many to One transformation function is similar to that of One to One transformation function, the only difference being that the transformation function accepts multiple features as input.

=== "Python"
    !!! example "Creation of a Many to One Custom Transformation Function in Hopsworks."
        ```python
        from hopsworks import udf

        @udf(int)
        def add_features(feature1, feature2, feature3):
            return feature + feature2 + feature3
        ```

To create a One to Many transformation function, the hopsworks `@udf` decorator must be provided with the return type as a list of Python types and the transformation function should take one argument as input and return multiple features as a Pandas DataFrame. The return types provided to the decorator must match the types of each column in the returned Pandas DataFrame.

=== "Python"
    !!! example "Creation of a One to Many Custom Transformation Function in Hopsworks."
        ```python
        from hopsworks import udf
        import pandas as pd

        @udf([int, int])
        def add_one_and_two(feature1):
            return pd.DataFrame({"add_one":feature1 + 1, "add_two":feature1 + 2})
        ```

Creation of a Many to Many transformation function is similar to that of One to May transformation function, the only difference being that the transformation function accepts multiple features as input.

=== "Python"    
    !!! example "Creation of a Many to Many Custom Transformation Function in Hopsworks."
        ```python
        from hopsworks import udf
        import pandas as pd

        @udf([int, int, int])
        def add_one_multiple(feature1, feature2, feature2):
            return pd.DataFrame({"add_one_feature1":feature1 + 1, "add_one_feature2":feature2 + 1, "add_one_feature3":feature3 + 1})
        ```
To access statistics pertaining to an argument provided as input to the transformation function, it is necessary to define a keyword argument named `statistics` in the transformation function. This statistics argument should be provided with an instance of class `TransformationStatistics` as default value. The `TransformationStatistics` instance must be initialized with the names of the arguments for which statistical information is required.

The `TransformationStatistics` instance contains separate objects with the same name as the arguments used to initialize it. These objects encapsulate statistics related to the feature as instances of the `FeatureTransformationStatistics` class. Upon instantiation, instances of `FeatureTransformationStatistics` are initialized with `None` values. These placeholders are subsequently populated with the required statistics when the training dataset is created.

=== "Python"   
    !!! example "Creation of a Custom Transformation Function in Hopsworks that accesses Feature Statistics"
        ```python
        from hopsworks import udf
        from hsfs.transformation_statistics import TransformationStatistics

        stats = TransformationStatistics("feature1", "feature2", "feature3") 

        @udf(int)
        def add_features(feature1, feature2, feature3, statistics=stats):
            return feature + feature2 + feature3 + statistics.feature1.mean + statistics.feature2.mean + statistics.feature3.mean
        ```

The output column generated by the transformation function follows a naming convention structured as `functionName_features_outputColumnNumber`. For instance, for the function named `add_one_multiple`, the output columns would be labeled as `add_one_multiple_feature1-feature2-feature3_0`, `add_one_multiple_feature1-feature2-feature3_1`, and `add_one_multiple_feature1-feature2-feature3_2`.

## Apply transformation functions to features

Transformation functions can be attached to a feature view as a list. Each transformation function can specify which features are to be use by explicitly providing their names as arguments. If no feature names are provided explicitly, the transformation function will default to using features from the feature view that matches the name of the transformation function's argument. Then the transformation functions are applied when you [read training data](./training-data.md#read-training-data), [read batch data](./batch-data.md#creation-with-transformation), or [get feature vectors](./feature-vectors.md#retrieval-with-transformation). By default all features provided as input to a transformation function are dropped when training data, batch data or feature vectors as created. 

=== "Python"

    !!! example "Attaching transformation functions to the feature view"
        ```python
        feature_view = fs.create_feature_view(
            name='transactions_view',
            query=query,
            labels=["fraud_label"],
            transformation_functions=[
                add_one,
                add_features,
                add_one_and_two,
                add_one_multiple
            ]
        )
        ```

To explicitly pass the features to a transformation function the feature name to be used can be passed as arguments to the transformation function.


=== "Python"

    !!! example "Attaching transformation functions to the feature view by explicitly specifying features to be passed to transformation function"
        ```python
        feature_view = fs.create_feature_view(
            name='transactions_view',
            query=query,
            labels=["fraud_label"],
            transformation_functions=[
                add_one("feature_1"),
                add_one("feature_2"),
                add_features("feature_1", "feature_2", "feature_3"),
                add_one_and_two("feature_4"),
                add_one_multiple("feature_5", "feature_6", "feature_7")
            ]
        )
        ```

Built-in transformation functions are attached in the same way. The only difference is that they can either be retrieved from the Hopsworks or imported from the hsfs module

=== "Python"

    !!! example "Attaching built-in transformation functions to the feature view by retrieving from Hopsworks"
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
                label_encoder("category": ),
                robust_scaler("amount"),
                min_max_scaler("loc_delta"),
                standard_scaler("age_at_transaction")
            ]
        )
        ```

To attach built in transformation functions from the hsfs module they can be directly imported into the code from `hsfs.builtin_transformations`.

=== "Python"

    !!! example "Attaching built-in transformation functions to the feature view by importing from hsfs"
        ```python
        from hsfs.builtin_transformations import min_max_scaler, label_encoder, robust_scaler, standard_scaler
        
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

## Saving Transformation Functions to Feature Store
To save a transformation function to the feature store, use the `create_transformation_function` which would create a `TransformationFunction` object. The `TransformationFunction` object can then be saved by calling the save function.

=== "Python"

    !!! example "Register transformation function  `add_one` in the Hopsworks feature store."
        ```python
        plus_one_meta = fs.create_transformation_function(
                    transformation_function=add_one,
                    version=1)
        plus_one_meta.save()
        ```

## Retrieval from Feature Store
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