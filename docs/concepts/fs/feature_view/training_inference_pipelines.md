# Consistent Transformations

A *training pipeline* is a program that orchestrates the training of a machine learning model.
For supervised machine learning, a training pipeline requires both features and labels, and these can typically be retrieved from the feature store as either in-memory Pandas/Polars DataFrames or read as training data files, created from the feature store.
An *inference pipeline* is a program that takes user input, optionally enriches it with features from the feature store, and builds a feature vector (or batch of feature vectors) with with it uses a model to make a prediction.

## Transformations

Feature transformations are mathematical operations that change feature values with the goal of improving model convergence or performance properties.
Transformation functions take as input a single value (or small number of values), they often require state (such as the mean value of a feature to normalize the input), and they output a single value or a list of values.

## Offline-Online Feature Skew

Offline-online feature skew is a difference between the transformation code that runs in an offline (training) pipeline and the transformation code that runs in the corresponding inference pipeline.
It is a code difference, not a data difference, so it cannot be detected by comparing distributions; the only way to avoid it is to run the same code in both pipelines.
In the image below, you can see that transformations happen after the Feature Store, but that the implementation of the transformation functions need to be consistent between the training and inference pipelines.

<figure class="hops-diagram">
<svg viewBox="0 0 1000 525" role="img" aria-label="Feature transformations run after the feature store, and the same transformation code and state must be applied in both the online serving pipeline and the offline training pipeline to avoid offline-online skew." xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="skew-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/></marker></defs>

  <path class="d-flow" d="M70 135 H980" stroke-dasharray="2 7"/>
  <text class="d-sub" x="25" y="118">Online</text>
  <text class="d-sub" x="25" y="153">Offline</text>

  <rect class="d-box-own" x="95" y="55" width="160" height="210" rx="8"/>
  <text class="d-t" x="175" y="82" text-anchor="middle">Feature Groups</text>
  <circle class="d-box-own" cx="215" cy="105" r="8"/>
  <circle class="d-box-own" cx="215" cy="200" r="8"/>

  <rect class="d-box" x="35" y="345" width="180" height="105" rx="8" stroke-dasharray="4 4"/>
  <text class="d-t" x="125" y="376" text-anchor="middle">&lt;pre&gt;</text>
  <text class="d-sub" x="125" y="398" text-anchor="middle">Aggregations,</text>
  <text class="d-sub" x="125" y="416" text-anchor="middle">dim-reduction,</text>
  <text class="d-sub" x="125" y="434" text-anchor="middle">validation</text>
  <text class="d-t" x="125" y="476" text-anchor="middle">Feature Pipelines</text>

  <rect class="d-alert-line" x="380" y="55" width="230" height="64" rx="8" fill="none"/>
  <text class="d-t" x="495" y="82" text-anchor="middle">&lt;post&gt;</text>
  <text class="d-t" x="495" y="103" text-anchor="middle">Feature Transformations</text>

  <rect class="d-alert-line" x="380" y="330" width="230" height="64" rx="8" fill="none"/>
  <text class="d-t" x="495" y="357" text-anchor="middle">&lt;post&gt;</text>
  <text class="d-t" x="495" y="378" text-anchor="middle">Feature Transformations</text>

  <text class="d-alert" x="495" y="188" text-anchor="middle">Same transformation code</text>
  <text class="d-alert" x="495" y="208" text-anchor="middle">Same transformation state</text>
  <path class="d-alert-line" d="M495 172 V121" marker-end="url(#skew-arrow)"/>
  <path class="d-alert-line" d="M495 222 V328" marker-end="url(#skew-arrow)"/>

  <rect class="d-box" x="790" y="55" width="170" height="60" rx="8"/>
  <text class="d-t" x="875" y="90" text-anchor="middle">Model Serving</text>

  <rect class="d-box-own" x="660" y="330" width="150" height="64" rx="8"/>
  <text class="d-t" x="735" y="367" text-anchor="middle">Training Data</text>

  <rect class="d-box" x="660" y="450" width="150" height="48" rx="8"/>
  <text class="d-t" x="735" y="479" text-anchor="middle">Model Training</text>

  <rect class="d-box-own" x="830" y="330" width="150" height="64" rx="8"/>
  <text class="d-t" x="905" y="357" text-anchor="middle">Model</text>
  <text class="d-t" x="905" y="378" text-anchor="middle">Registry</text>

  <rect class="d-box" x="830" y="450" width="150" height="48" rx="8"/>
  <text class="d-t" x="905" y="479" text-anchor="middle">Batch Predictions</text>

  <path class="d-flow" d="M125 345 V265" marker-end="url(#skew-arrow)"/>
  <path class="d-flow" d="M255 105 H340 V87 H380" marker-end="url(#skew-arrow)"/>
  <path class="d-flow" d="M610 87 H790" marker-end="url(#skew-arrow)"/>
  <path class="d-flow" d="M255 200 H320 V362 H380" marker-end="url(#skew-arrow)"/>
  <path class="d-flow" d="M610 362 H660" marker-end="url(#skew-arrow)"/>
  <path class="d-flow" d="M735 394 V450" marker-end="url(#skew-arrow)"/>
  <path class="d-flow" d="M810 474 V362 H830" marker-end="url(#skew-arrow)"/>
  <path class="d-flow" d="M905 330 V115" marker-end="url(#skew-arrow)"/>
  <path class="d-flow" d="M905 394 V450" marker-end="url(#skew-arrow)"/>
</svg>
</figure>

There are 3 main approaches to prevent offline-online feature skew that we support in Hopsworks.
These are (1) perform transformations in models, (2) perform transformations in pipelines (sklearn, TF, PyTorch) and use the model registry to save the transformation pipeline so that the same transformation is used in your inference pipeline, and (3) use Hopsworks transformations, defined as UDFs in Python.

### Transformations as Pre-Processing Layers in Models

Transformation functions can be implemented as preprocessing steps within a model.
For example, you can write a transformation function as a pre-processing layer in Keras/TensorFlow.
When you save the model, the preprocessing steps will also be saved as part of the model.
Any state required to compute the transformation, such as the arithmetic mean of a numerical feature in the train set, is also stored with the function, enabling consistent transformations during inference.  When data preprocessing is part of the model, users can just send the untransformed feature values to the model and the model itself will apply any transformation functions as preprocessing layers (such as encoding categorical variables or normalizing numerical variables).

### Transformation Pipelines in Scikit-Learn/TensorFlow/PyTorch

You have to save your transformation pipeline (serialize the object or the parameters) and make sure you apply exactly the same transformations in your inference pipeline.
This means you should version the transformations.
In Hopsworks, you can store the transformations with your versioned models in the Model Registry, helping you to ensure the same transformation pipeline is applied to both training/serving for the same model version.

### Transformations as Python UDFs in Hopsworks

Hopsworks feature store also supports consistent transformation functions by enabling a Python UDF, that implements a transformation, to be attached a to feature in a feature view.
When training data is created with a feature view or when a feature vector is retrieved from a feature view, Hopsworks ensures that any transformation functions defined over any features will be applied before returning feature values.
You can use built-in transformation objects in Hopsworks or write your own custom transformation functions as Python UDFs.
The benefit of this approach is that transformations are applied consistently when creating training data and when retrieving feature data from the online feature store.
Transformations no longer need to be included in either your training pipeline or inference pipeline, as they are applied transparently when creating training data and retrieving feature vectors.
Hopsworks uses Spark to create training data as files, and any transformation functions for features are executed as Python UDFs in Spark - enabling transformation functions to be applied on large volumes of data and removing potentially CPU-intensive transformations from training pipelines.
