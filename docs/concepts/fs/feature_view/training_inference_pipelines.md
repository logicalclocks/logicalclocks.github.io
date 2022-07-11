A *training pipeline* is a program that orchestrates the training of a machine learning model. For supervised machine learning, a training pipeline requires both features and labels, and these can typically be retrieved from the feature store as either in-memory Pandas DataFrames or read as training data files, created from the feature store. An *inference pipeline* is a program that takes user input, optionally enriches it with features from the feature store, and builds a feature vector (or batch of feature vectors) with with it uses a model to make a prediction.


## Transformations
Feature transformations are mathematical operations that change feature values with the goal of improving model convergence or performance properties. Transformation functions take as input a single value (or small number of values), they often require state (such as the mean value of a feature to normalize the input), and they output a single value or a list of values.

## Training Serving Skew

It is crucial that the transformations performed when creating features (for training or serving) are consistent - use the same code - to avoid training/serving skew. In the image below, you can see that transformations happen after the Feature Store, but that the implementation of the transformation functions need to be consistent between the training and inference pipelines. 

<img src="../../../../assets/images/concepts/fs/no-training-serving-skew.svg">

There are 3 main approaches to prevent training/serving skew that we support in Hopsworks. These are (1) perform transformations in models, (2) perform transformations in pipelines (sklearn, TF, PyTorch) and use the model registry to save the transformation pipeline so that the same transformation is used in your inference pipeline, and (3) use HSFS transformations, defined as UDFs in Python.


### Transformations as Pre-Processing Layers in Models

Transformation functions can be implemented as preprocessing steps within a model. For example, you can write a transformation function as a pre-processing layer in Keras/TensorFlow. When you save the model, the preprocessing steps will also be saved as part of the model. Any state required to compute the transformation, such as the arithmetic mean of a numerical feature in the train set, is also stored with the function, enabling consistent transformations during inference.  When data preprocessing is part of the model, users can just send the untransformed feature values to the model and the model itself will apply any transformation functions as preprocessing layers (such as encoding categorical variables or normalizing numerical variables).


### Transformation Pipelines in Scikit-Learn/TensorFlow/PyTorch

You have to save your transformation pipeline (serialize the object or the parameters) and make sure you apply exactly the same transformations in your inference pipeline. This means you should version the transformations. In Hopsworks, you can store the transformations with your versioned models in the Model Registry, helping you to ensure the same transformation pipeline is applied to both training/serving for the same model version.

### Transformations as Python UDFs in HSFS

Hopsworks feature store also supports consistent transformation functions by enabling a Python UDF, that implements a transformation, to be attached a to feature in a feature view. When training data is created with a feature view or when a feature vector is retrieved from a feature view, HSFS ensures that any transformation functions defined over any features will be applied before returning feature values. You can use built-in transformation objects in HSFS or write your own custom transformation functions as Python UDFs. The benefit of this approach is that transformations are applied consistently when creating training data and when retrieving feature data from the online feature store. Transformations no longer need to be included in either your training pipeline or inference pipeline, as they are applied transparently when creating training data and retrieving feature vectors. Hopsworks uses Spark to create training data as files, and any transformation functions for features are executed as Python UDFs in Spark - enabling transformation functions to be applied on large volumes of data and removing potentially CPU-intensive transformations from training pipelines.
