---
description: Documentation on how to export a Tensorflow model to the model registry
---

# How To Export a TensorFlow Model

## Introduction

In this guide you will learn how to export a TensorFlow model and register it in the Model Registry.

!!! notice "Save in SavedModel format"
    Make sure the model is saved in the [SavedModel](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/saved_model/README.md) format to be able to deploy it on TensorFlow Serving.


## Code

### Step 1: Connect to Hopsworks

=== "Python"
    ```python
    import hopsworks

    project = hopsworks.login()

    # get Hopsworks Model Registry handle
    mr = project.get_model_registry()
    ```

### Step 2: Train

Define your TensorFlow model and run the training loop.

=== "Python"
    ```python
    # Define a model
    model = tf.keras.Sequential()

    # Add layers
    model.add(..)

    # Compile the model.
    model.compile(..)
        
    # Train the model
    model.fit(..)
    ```

### Step 3: Export to local path

Export the TensorFlow model to a directory on the local filesystem.

=== "Python"
    ```python
    model_dir = "./model"

    tf.saved_model.save(model, model_dir)
    ```

### Step 4: Register model in registry

Use the `ModelRegistry.tensorflow.create_model(..)` function to register a model as a TensorFlow model. Define a name, and attach optional metrics for your model, then invoke the `save()` function with the parameter being the path to the local directory where the model was exported to.  

=== "Python"
    ```python
    # Model evaluation metrics
    metrics = {'accuracy': 0.92}

    tf_model = mr.tensorflow.create_model("tf_model", metrics=metrics)

    tf_model.save(model_dir)
    ```

## Going Further

You can attach an [Input Example](../input_example.md) and a [Model Schema](../model_schema.md) to your model to document the shape and type of the data the model was trained on.
