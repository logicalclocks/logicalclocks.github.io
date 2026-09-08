---
description: Documentation on how to attach a model schema to a model.
---

# How To Attach A Model Schema

## Introduction

!!! warning "Deprecated"
    `ModelSchema` is deprecated and will be removed in a future release.
    A model registered with `create_model(feature_view=...)` gets its input and output schema from the feature view's training dataset, and a deployment describes its requests with the [deployment schema][deployment-schema].
    The default predictor still reads a legacy model schema to select the model's input columns; a `DefaultPredict` subclass that overrides `model_predict` replaces that.
    For a model without a feature view, name its input columns with `passed_features=` on `deploy()`.

In this guide you will learn how to attach a model schema to your model.
A model schema, describes the type and shape of inputs and outputs (predictions) for your model.
Attaching a model schema to your model will give other users a better understanding of what data it expects.

!!! info "Model schema and deployment schema"
    A model registered with `feature_view=` gets its model schema inferred from the feature view's training dataset schema when it is saved.
    The default predictor checks at pod start that every model input column is served by the feature view, and the deployment schema describes what clients send.
    See the [Deployment Schema Guide][deployment-schema].

## Code

### Step 1: Connect to Hopsworks

=== "Python"

    ```python
    import hopsworks


    project = hopsworks.login()

    # get Hopsworks Model Registry handle
    mr = project.get_model_registry()
    ```

### Step 2: Create ModelSchema

Create a ModelSchema for your inputs and outputs by passing in an example that your model is trained on and a valid prediction.
Currently, we support `pandas.DataFrame, pandas.Series, numpy.ndarray, list`.

=== "Python"

    ```python
    # Import a Schema and ModelSchema definition
    from hsml.model_schema import ModelSchema
    from hsml.schema import Schema


    # Model inputs for MNIST dataset
    inputs = [
        {
            "type": "uint8",
            "shape": [28, 28, 1],
            "description": "grayscale representation of 28x28 MNIST images",
        }
    ]

    # Build the input schema
    input_schema = Schema(inputs)

    # Model outputs
    outputs = [{"type": "float32", "shape": [10]}]

    # Build the output schema
    output_schema = Schema(outputs)

    # Create ModelSchema object
    model_schema = ModelSchema(input_schema=input_schema, output_schema=output_schema)
    ```

### Step 3: Set model_schema parameter

Set the `model_schema` parameter in the `create_model` function and call `save()` to attaching it to the model and register it in the registry.

=== "Python"

    ```python
    model = mr.tensorflow.create_model(name="mnist", model_schema=model_schema)
    model.save("./model")
    ```
