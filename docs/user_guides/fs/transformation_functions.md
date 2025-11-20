
# Transformation Functions

In AI systems, [transformation functions](https://www.hopsworks.ai/dictionary/transformation) transform data to create features, the inputs to machine learning models (in both training and inference). The [taxonomy of data transformations](../../concepts/mlops/data_transformations.md) introduces three types of data transformation prevalent in all AI systems. Hopsworks offers simple Python APIs to define custom transformation functions. These can be used along with [feature groups](./feature_group/index.md) and [feature views](./feature_view/overview.md) to create [on-demand transformations](./feature_group/on_demand_transformations.md) and [model-dependent transformations](./feature_view/model-dependent-transformations.md), producing modular AI pipelines that are skew-free.

## Custom Transformation Function Creation

User-defined transformation functions can be created in Hopsworks using the [`@udf`](http://docs.hopsworks.ai/hopsworks-api/{{{hopsworks_version}}}/generated/api/udf/) decorator. These functions can be either implemented as pure Python UDFs or Pandas UDFs (User-Defined Functions).

Hopsworks offers three execution modes to control the execution of transformation functions during training dataset creation, batch inference, and online inference. By default, Hopsworks executes transformation functions as Python UDFs for [feature vector retrieval](feature_view/feature-vectors.md) in online inference pipelines and as Pandas UDFs for both [batch data retrieval](feature_view/batch-data.md) in batch inference pipelines and [training dataset creation](feature_view/training-data.md) in training pipelines. Python UDFs are optimized for smaller data volumes, while Pandas UDFs provide better performance on larger datasets. This execution mode provides the optimal balance based on the data size across training dataset generations, batch inference, and online inference. Additionally, Hopsworks allows you to explicitly set the execution mode for a transformation function to `python` or `pandas`, forcing the transformation function to always run as either a Python or Pandas UDF as specified.

A Pandas UDF in Hopsworks accepts one or more Pandas Series as input and can return either one or more Series or a Pandas DataFrame. When integrated with PySpark applications, Hopsworks automatically executes Pandas UDFs using PySpark’s [`pandas_udf`](https://spark.apache.org/docs/3.4.1/api/python/reference/pyspark.sql/api/pyspark.sql.functions.pandas_udf.html), enabling the transformation functions to efficiently scale for large datasets.

!!! warning "Java/Scala support"

    Hopsworks supports transformations functions in Python (Pandas UDFs, Python UDFs). Transformations functions can also be executed in Python-based DataFrame frameworks (PySpark, Pandas). There is currently no support for transformation functions in SQL or Java-based feature pipelines.

Transformation functions created in Hopsworks can be directly attached to feature views or feature groups or stored in the feature store for later retrieval. These functions can be part of a library [installed](../../user_guides/projects/python/python_install.md) in Hopsworks or be defined in a [Jupyter notebook](../../user_guides/projects/jupyter/python_notebook.md) running a Python kernel or added when starting a Jupyter notebook or [Hopsworks job](../../user_guides/projects/jobs/spark_job.md).

!!! warning "PySpark Kernels"

    Definition transformation function within a Jupyter notebook is only supported in Python Kernel. In a PySpark Kernel transformation function have to defined as modules or added when starting a Jupyter notebook.

The `@udf` decorator in Hopsworks creates a metadata class called [`HopsworksUdf`](http://docs.hopsworks.ai/hopsworks-api/{{{hopsworks_version}}}/generated/api/hopsworks_udf/). This class manages the necessary operations to execute the transformation function.

The decorator accepts three parameters:

- **`return_type`** (required): Specifies the data type(s) of the features returned by the transformation function. It can be a single Python type if the function returns one transformed feature, or a list of Python types if it returns multiple transformed features. The supported Python types that be used with the `return_type` argument are provided in the table below:

    |       Supported Python Types       |
    |:----------------------------------:|
    |               str                  |
    |               int                  |
    |              float                 |
    |               bool                 |
    |         datetime.datetime          |
    |           datetime.date            |
    |           datetime.time            |

- **`drop`** (optional): Identifies input arguments to exclude from the output after transformations are applied. By default, all inputs are retained in the output. Further details on this argument can be found [below](#dropping-input-features).

- **`mode`** (optional): Determines the execution mode of the transformation function. The argument accepts three values: `default`, `python`, or `pandas`. By default, the `mode` is set to `default`.  Further details on this argument can be found [below](#specifying-execution-modes).

Hopsworks supports four types of transformation functions across all execution modes:

1. One-to-one: Transforms one feature into one transformed feature.
2. One-to-many: Transforms one feature into multiple transformed features.
3. Many-to-one: Transforms multiple features into one transformed feature.
4. Many-to-many: Transforms multiple features into multiple transformed features.

### One-to-one transformations

To create a one-to-one transformation function, the Hopsworks `@udf` decorator must be provided with the `return_type` as a single Python type. The transformation function should take one argument as input and return a Pandas Series.

=== "Python"

    !!! example "Creation of a one-to-one transformation function in Hopsworks."
        ```python
        from hopsworks import udf

        @udf(return_type=int)
        def add_one(feature):
            return feature + 1
        ```

### Many-to-one transformations

The creation of many-to-one transformation functions is similar to that of a one-to-one transformation function, the only difference being that the transformation function accepts multiple features as input.

=== "Python"
    !!! example "Creation of a many-to-one transformation function in Hopsworks."
        ```python
        from hopsworks import udf

        @udf(return_type=int)
        def add_features(feature1, feature2, feature3):
            return feature + feature2 + feature3
        ```

### One-to-many transformations

To create a one-to-many transformation function, the Hopsworks `@udf` decorator must be provided with the `return_type` as a list of Python types, and the transformation function should take one argument as input and return multiple features as a Pandas DataFrame. The return types provided to the decorator must match the types of each column in the returned Pandas DataFrame.

=== "Python"
    !!! example "Creation of a one-to-many transformation function in Hopsworks."
        ```python
        from hopsworks import udf
        import pandas as pd

        @udf(return_type=[int, int])
        def add_one_and_two(feature1):
            return feature1 + 1, feature1 + 2
        ```

### Many-to-many transformations

The creation of a many-to-many transformation function is similar to that of a one-to-many transformation function, the only difference being that the transformation function accepts multiple features as input.

=== "Python"
    !!! example "Creation of a many-to-many transformation function in Hopsworks."
        ```python
        from hopsworks import udf
        import pandas as pd

        @udf(return_type=[int, int, int])
        def add_one_multiple(feature1, feature2, feature3):
            return feature1 + 1, feature2 + 1, feature3 + 1
        ```

### Specifying execution modes

The `mode` parameter of the `@udf` decorator can be used to specify the execution mode of the transformation function. It accepts three possible values `default`, `python` and `pandas`.  Each mode is explained in more detail below:

#### Default

This execution mode assumes that the transformation function can be executed as either a Pandas UDF or a Python UDF. It serves as the default mode used when the `mode` parameter is not specified. In this mode, the transformation function is executed as a Pandas UDF during training and in the batch inference pipeline, while it operates as a Python UDF during online inference.

=== "Python"
    !!! example "Creating a many to many transformations function using the default execution mode"
        ```python
        from hopsworks import udf
        import pandas as pd

        # "default" mode is used if the parameter `mode` is not explicitly set.
        @udf(return_type=[int, int, int])
        def add_one_multiple(feature1, feature2, feature3):
            return feature1 + 1, feature2 + 1, feature3 + 1

        @udf(return_type=[int, int, int], mode="default")
        def add_two_multiple(feature1, feature2, feature3):
            return feature1 + 2, feature2 + 2, feature3 + 2
        ```

#### Python

The transformation function can be configured to always execute as a Python UDF by setting the `mode` parameter of the `@udf` decorator to `python`.

=== "Python"
    !!! example "Creating a many to many transformation function as a Python UDF"
        ```python
        from hopsworks import udf
        import pandas as pd

        @udf(return_type=[int, int, int], mode = "python")
        def add_one_multiple(feature1, feature2, feature3):
            return feature1 + 1, feature2 + 1, feature3 + 1
        ```

#### Pandas

The transformation function can be configured to always execute as a Pandas UDF by setting the `mode` parameter of the `@udf` decorator to `pandas`.

=== "Python"
    !!! example "Creating a many to many transformations function as a Pandas UDF"
        ```python
        from hopsworks import udf
        import pandas as pd

        # A Pandas UDF returning a Pandas DataFrame
        @udf(return_type=[int, int, int], mode = "pandas")
        def add_one_multiple(feature1, feature2, feature3):
            return pd.DataFrame({"add_one_feature1":feature1 + 1, "add_one_feature2":feature2 + 1, "add_one_feature3":feature3 + 1})

        # A Pandas UDF returning multiple Pandas Series
        @udf(return_type=[int, int, int], mode="pandas")
        def add_two_multiple(feature1, feature2, feature3):
            return feature1 + 2, feature2 + 2, feature3 + 2
        ```

### Dropping input features

The `drop` parameter of the `@udf` decorator is used to drop specific columns in the input DataFrame after transformation.  If any argument of the transformation function is passed to the `drop` parameter, then the column mapped to the argument is dropped after the transformation functions are applied. In the example below, the columns mapped to the arguments `feature1` and `feature3` are dropped after the application of all transformation functions.

=== "Python"
    !!! example "Specify arguments to drop after transformation"
        ```python
        from hopsworks import udf
        import pandas as pd

        @udf(return_type=[int, int, int], drop=["feature1", "feature3"])
        def add_one_multiple(feature1, feature2, feature3):
            return feature1 + 1, feature2 + 1, feature3 + 1
        ```

### Specifying output features names for transformation functions

The [`alias`](http://docs.hopsworks.ai/hopsworks-api/{{{hopsworks_version}}}/generated/api/transformation_functions_api/#alias) function of a transformation function allows the specification of names of transformed features generated by the transformation function. Each name must be uniques and should be at-most 63 characters long. If no name is provided via the `alias` function, Hopsworks generates default output feature names when [on-demand](./feature_group/on_demand_transformations.md) or [model-dependent](./feature_view/model-dependent-transformations.md) transformation functions are created.

=== "Python"
    !!! example "Specifying output column names for transformation functions."
        ```python
        from hopsworks import udf
        import pandas as pd

        @udf(return_type=[int, int, int], drop=["feature1", "feature3"])
        def add_one_multiple(feature1, feature2, feature3):
            return feature1 + 1, feature2 + 1, feature3 + 1

        # Specifying output feature names of the transformation function.
        add_one_multiple.alias("transformed_feature1", "transformed_feature2", "transformed_feature3")
        ```

### Training dataset statistics

A keyword argument `statistics` can be defined in the transformation function if it requires training dataset statistics for any of its arguments. The `statistics` argument must be assigned an instance of the class [`TransformationStatistics`](http://docs.hopsworks.ai/hopsworks-api/{{{hopsworks_version}}}/generated/api/transformation_statistics/) as the default value. The `TransformationStatistics` instance must be initialized using the names of the arguments requiring statistics.

!!! warning "Transformation Statistics"

    The statistics provided to the transformation function is the statistics computed using [the train set](https://www.hopsworks.ai/dictionary/train-training-set). Training dataset statistics are not available for on-demand transformations.

The `TransformationStatistics` instance contains separate objects with the same name as the arguments used to initialize it. These objects encapsulate statistics related to the argument as instances of the class [`FeatureTransformationStatistics`](http://docs.hopsworks.ai/hopsworks-api/{{{hopsworks_version}}}/generated/api/feature_transformation_statistics/). Upon instantiation, instances of `FeatureTransformationStatistics` contain `None` values and are updated with the required statistics after the creation of a training dataset.

=== "Python"
    !!! example "Creation of a transformation function in Hopsworks that uses training dataset statistics"
        ```python
        from hopsworks import udf
        from hopsworks.transformation_statistics import TransformationStatistics

        stats = TransformationStatistics("argument1", "argument2", "argument3") 

        @udf(int)
        def add_features(argument1, argument2, argument3, statistics=stats):
            return argument + argument2 + argument3 + statistics.argument1.mean + statistics.argument2.mean + statistics.argument3.mean
        ```

### Passing context variables to transformation function

The `context` keyword argument can be defined in a transformation function to access shared context variables. These variables contain common data used across transformation functions. By including the context argument, you can pass the necessary data as a dictionary into the into the `context` argument of the transformation function during [training dataset creation](feature_view/training-data.md#passing-context-variables-to-transformation-functions) or [feature vector retrieval](feature_view/feature-vectors.md#passing-context-variables-to-transformation-functions) or [batch data retrieval](feature_view/batch-data.md#passing-context-variables-to-transformation-functions).

=== "Python"
    !!! example "Creation of a transformation function in Hopsworks that accepts context variables"
        ```python
        from hopsworks import udf

        @udf(int)
        def add_features(argument1, context):
            return argument + context["value_to_add"]
        ```

## Saving to the Feature Store

To save a transformation function to the feature store, use the function `create_transformation_function`. It creates a [`TransformationFunction`](http://docs.hopsworks.ai/hopsworks-api/{{{hopsworks_version}}}/generated/api/transformation_functions_api/) object which can then be saved by calling the save function. The save function will throw an error if another transformation function with the same name and version is already saved in the feature store.

=== "Python"

    !!! example "Register transformation function `add_one` in the Hopsworks feature store"
        ```python
        plus_one_meta = fs.create_transformation_function(
                    transformation_function=add_one,
                    version=1)
        plus_one_meta.save()
        ```

## Retrieval from the Feature Store

To retrieve all transformation functions from the feature store, use the function `get_transformation_functions`, which returns the list of `TransformationFunction` objects.

A specific transformation function can be retrieved using its `name` and `version` with the function `get_transformation_function`. If only the `name` is provided, then the version will default to 1.

=== "Python"

    !!! example "Retrieving transformation functions from the feature store"
        ```python
        # get all transformation functions
        fs.get_transformation_functions()

        # get transformation function by name. This will default to version 1
        plus_one_fn = fs.get_transformation_function(name="plus_one")

        # get transformation function by name and version.
        plus_one_fn = fs.get_transformation_function(name="plus_one", version=2)
        ```

## Using transformation functions

Transformation functions can be used by attaching it to a feature view to [create model-dependent transformations](./feature_view/model-dependent-transformations.md) or attached to feature groups to  [create on-demand transformations](./feature_group/on_demand_transformations.md)
