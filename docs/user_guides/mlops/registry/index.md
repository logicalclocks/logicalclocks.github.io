# Model Registry Guides

Hopsworks Model Registry is a centralized repository, within an organization, to manage machine learning models. A model is the product of training a machine learning algorithm with training data.

This section provides guides for creating models and publish them to the Model Registry to make them available to make them available for download for batch predictions, or deployed to serve realtime applications.


## Exporting a model

Follow these framework-specific guides to export a Model to the Model Registry.

* [TensorFlow](frameworks/tf.md)

* [Scikit-learn](frameworks/skl.md)

* [Other frameworks](frameworks/python.md)


## Model Schema

A [Model schema](model_schema.md) describes the input and outputs for a model. It provides a functional description of the model which makes it simpler to get started working with it. For example if the model inputs a tensor, the model schema can define the shape and data type of the tensor.


## Input Example

An [Input example](input_example.md) provides an instance of a valid model input. Input examples are stored with the model as separate artifacts.
