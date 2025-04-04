---
description: Documentation on how to export a Scikit-learn model to the model registry
---

# How To Export a Scikit-learn Model

## Introduction

In this guide you will learn how to export a Scikit-learn model and register it in the Model Registry.

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

Define your Scikit-learn model and run the training loop.

=== "Python"
    ```python
    # Define a model
    iris_knn = KNeighborsClassifier(..)

    iris_knn.fit(..)
    ```

### Step 3: Export to local path

Export the Scikit-learn model to a directory on the local filesystem.

=== "Python"
    ```python
    model_file = "skl_knn.pkl"

    joblib.dump(iris_knn, model_file)
    ```

### Step 4: Register model in registry

Use the `ModelRegistry.sklearn.create_model(..)` function to register a model as a Scikit-learn model. Define a name, and attach optional metrics for your model, then invoke the `save()` function with the parameter being the path to the local directory where the model was exported to.

=== "Python"
    ```python
    # Model evaluation metrics
    metrics = {'accuracy': 0.92}

    skl_model = mr.sklearn.create_model("skl_model", metrics=metrics)

    skl_model.save(model_file)
    ```

## Going Further

You can attach an [Input Example](../input_example.md) and a [Model Schema](../model_schema.md) to your model to document the shape and type of the data the model was trained on.
