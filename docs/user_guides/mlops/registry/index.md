# Model Registry Guides

**Hopsworks Model Registry** is a centralized repository, within an organization, to manage machine learning models.
A model is the product of training a machine learning algorithm with training data.

This section provides guides for creating models and publish them to the Model Registry to make them available for download for batch predictions, or deployed to serve realtime applications.

## Exporting a model

Follow these framework-specific guides to export a Model to the Model Registry.

<div class="grid cards" markdown>

-   :simple-tensorflow:{ .lg .middle style="color:#FF6F00" } **TensorFlow**

    ---

    Export a TensorFlow or Keras model.

    [:octicons-arrow-right-24: Export guide](frameworks/tf.md)

-   :simple-pytorch:{ .lg .middle style="color:#EE4C2C" } **Torch**

    ---

    Export a PyTorch model.

    [:octicons-arrow-right-24: Export guide](frameworks/tch.md)

-   :simple-scikitlearn:{ .lg .middle style="color:#F7931E" } **Scikit-learn**

    ---

    Export a scikit-learn model.

    [:octicons-arrow-right-24: Export guide](frameworks/skl.md)

-   :material-robot-outline:{ .lg .middle style="color:var(--hops-accent-text)" } **LLM**

    ---

    Export a large language model.

    [:octicons-arrow-right-24: Export guide](frameworks/llm.md)

-   :simple-python:{ .lg .middle style="color:#3776AB" } **Other Python frameworks**

    ---

    Export any other Python model, such as XGBoost or LightGBM.

    [:octicons-arrow-right-24: Export guide](frameworks/python.md)

</div>

## Importing a model from HuggingFace

You can also import a model directly from the [HuggingFace Hub](https://huggingface.co) through the Hopsworks UI.
The download runs server-side and the model is registered automatically.
See [Import from HuggingFace][how-to-import-a-model-from-huggingface].

## Model Schema

A [Model schema](model_schema.md) describes the input and outputs for a model.
It provides a functional description of the model which makes it simpler to get started working with it.
For example if the model inputs a tensor, the model schema can define the shape and data type of the tensor.

## Input Example

An [Input example](input_example.md) provides an instance of a valid model input.
Input examples are stored with the model as separate artifacts.
