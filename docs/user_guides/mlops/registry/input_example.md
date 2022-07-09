# How To Attach An Input Example

## Introduction

In this guide you will learn how to attach an input example to a model. An input example is simply an instance of a valid model input. Attaching an input example to your model will give other users a better understanding of what data it expects.

## Code

### Step 1: Connect to Hopsworks

```python
import hopsworks

connection = hopsworks.connection()

project = connection.get_project("my_project")

# get Hopsworks Model Registry handle
mr = project.get_model_registry()
```

### Step 2: Generate an input example

Generate an input example which corresponds to a valid input to your model. Currently we support `pandas.DataFrame, pandas.Series, numpy.ndarray, list` to be passed as input example.

```python
import numpy as np

input_example = np.random.randint(0, high=256, size=784, dtype=np.uint8)

```

### Step 3: Set input_example parameter

Set the `input_example` parameter in the `create_model` function and call `save()` to attaching it to the model and register it in the registry.
```python

model = mr.tensorflow.create_model(name="mnist",
                                   input_example=input_example)
model.save("./model")

```

## Conclusion

In this guide you learned how to attach an input example to your model.