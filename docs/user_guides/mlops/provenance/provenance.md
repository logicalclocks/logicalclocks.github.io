# Provenance

## Introduction

Hopsworks allows users to track provenance (lineage) between:

- data sources
- feature groups
- feature views
- training datasets
- models

In the provenance pages we will call a provenance artifact or shortly artifact, any of the five entities above.

With the following provenance graph:

```plaintext
data source -> feature group -> feature group -> feature view -> training dataset -> model
```

we will call the parent, the artifact to the left, and the child, the artifact to the right.
So a feature view has a number of feature groups as parents and can have a number of training datasets as children.

Tracking provenance allows users to determine where and if an artifact is being used.
You can track, for example, if feature groups are being used to create additional (derived) feature groups or feature views, or if their data is eventually used to train models.

You can interact with the provenance graph using the UI or the APIs.

## Model provenance

The relationship between feature views and models is captured in the [model][hsml.model.Model] constructor.
If you do not provide at least the feature view object to the constructor, the provenance will not capture this relation and you will not be able to navigate from model to the feature view it used or from the feature view to this model.

You can provide the feature view object and have the training dataset version be inferred.

=== "Python"

    ```python
    # this fv object will be provided to the model constructor
    fv = hsfs.get_feature_view(...)

    # when calling trainig data related methods on the feature view, the training dataset version is cached in the feature view and is implicitly provided to the model constructor
    X_train, X_test, y_train, y_test = feature_view.train_test_split(...)

    # provide the feature_view object in the model constructor
    hsml.model_registry.ModelRegistry.python.create_model(
        ...
        feature_view = fv
        ...)
    ```

You can of course explicitly provide the training dataset version.
=== "Python"

    ```python
    # this object will be provided to the model constructor
    fv = hsfs.get_feature_view(...)

    # this training dataset version will be provided to the model constructor
    X_train, X_test, y_train, y_test = feature_view.get_train_test_split(training_dataset_version=1)

    # provide the feature_view object in the model constructor
    hsml.model_registry.ModelRegistry.python.create_model(
        ...
        feature_view = fv,
        training_dataset_version = 1,
        ...)
    ```

Once the relation is stored in the provenance graph, you can navigate the graph from model to feature view or training dataset and the other way around.

Users can call the [`Model.get_feature_view_provenance`][hsml.model.Model.get_feature_view_provenance] method or the [`Model.get_training_dataset_provenance`][hsml.model.Model.get_training_dataset_provenance] method which will each return a [provenance Link object](#provenance-links).

You can also retrieve directly the parent feature view object, without the need to extract them from the provenance links object, using the [`Model.get_feature_view`][hsml.model.Model.get_feature_view] method.

=== "Python"

    ```python
    feature_view = model.get_feature_view()
    ```

This utility method also has the options to initialize the required components for batch or online retrieval of feature vectors.

=== "Python"

    ```python
    model.get_feature_view(init: bool = True, online: Optional[bool]: None)
    ```

By default, the base init for feature vector retrieval is enabled.
In case you have a workflow that requires more particular options, you can disable this base init by setting the `init` to `false`.
The method detects if it is running within a deployment and will initialize the feature vector retrieval for the serving.
If the `online` argument is provided and `true` it will initialize for online feature vector retrieval.
If the `online` argument is provided and `false` it will initialize the feature vector retrieval for batch scoring.

### Using the UI

In the model overview UI you can explore the provenance graph of the model:

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/provenance/provenance_model.png" alt="Model provenance graph">
    <figcaption>Provenance graph of derived feature groups</figcaption>
  </figure>
</p>

## Provenance Links

All the `_provenance` methods return a `Link` dictionary object that contains `accessible`, `inaccesible`, `deleted` lists.

- `accessible` - contains any artifact from the result, that the user has access to.
- `inaccessible` - contains any artifacts that might have been shared at some point in the past, but where this sharing was retracted.
  Since the relation between artifacts is still maintained in the provenance, the user will only have access to limited metadata and the artifacts will be included in this `inaccessible` list.
- `deleted` - contains artifacts that are deleted with children stil present in the system.
  There is minimum amount of metadata for the deleted allowing for some limited human readable identification.
