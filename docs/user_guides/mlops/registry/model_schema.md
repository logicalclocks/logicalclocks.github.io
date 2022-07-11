# How To Attach A Model Schema

## Introduction

In this guide you will learn how to attach a model schema to your model. A model schema, describes the type and shape of inputs and outputs (predictions) for your model. Attaching a model schema to your model will give other users a better understanding of what data it expects.

## Code

### Step 1: Connect to Hopsworks

```python
import hopsworks

connection = hopsworks.connection()

project = connection.get_project("my_project")

# get Hopsworks Model Registry handle
mr = project.get_model_registry()
```

### Step 2: Create ModelSchema

Create a ModelSchema for your inputs and outputs by passing in an example that your model is trained on and a valid prediction. Currently, we support `pandas.DataFrame, pandas.Series, numpy.ndarray, list`.

```python

# Import a Schema and ModelSchema definition
from hsml.utils.model_schema import ModelSchema
from hsml.utils.schema import Schema

# Model inputs for MNIST dataset
inputs = [{'type': 'uint8', 'shape': [28, 28, 1], 'description': 'grayscale representation of 28x28 MNIST images'}]

# Build the input schema
input_schema = Schema(inputs)

# Model outputs
outputs = [{'type': 'float32', 'shape': [10]}]

# Build the output schema
output_schema = Schema(outputs)

# Create ModelSchema object
model_schema = ModelSchema(input_schema=input_schema, output_schema=output_schema)

```

### Step 3: Set model_schema parameter

Set the `model_schema` parameter in the `create_model` function and call `save()` to attaching it to the model and register it in the registry.
```python

model = mr.tensorflow.create_model(name="mnist",
                                   model_schema=model_schema)
model.save("./model")

```

## Conclusion

In this guide you learned how to attach an input example to your model.