# Feature Vectors
Once you have trained a model, it is time to deploy it. You can get back all the features required to feed into an ML model with a single method call. A feature view provides great flexibility for you to retrieve a vector (or row) of features from any environment, whether you are either inside the Hopsworks platform, a model serving platform, or in an external environment, such as your application server. Harnessing the powerful [RonDB](https://www.rondb.com/), feature vectors are served at in-memory latency.

If you want to understand more about the concept of feature vectors, you can refer to [here](../../../concepts/fs/feature_view/online_api.md).

## Retrieval
You can get back feature vectors from either python or java client by providing the primary key value(s) for the feature view. Note that filters defined in feature view and training data will not be applied when feature vectors are returned.

=== "Python"
    ```python
    # get a single vector
    feature_view.get_feature_vector(
        entry = {"pk1": 1, "pk2": 2}
    )

    # get multiple vectors
    feature_view.get_feature_vectors(
        entry = [
            {"pk1": 1, "pk2": 2},
            {"pk1": 3, "pk2": 4},
            {"pk1": 5, "pk2": 6}
        ]
    )
    ```
=== "Java"
    ```java
    // get a single vector
    Map<String, Object> entry1 = Maps.newHashMap();
    entry1.put("pk1", 1);
    entry1.put("pk2", 2);
    featureView.getFeatureVector(entry1);

    // get multiple vectors
    Map<String, Object> entry2 = Maps.newHashMap();
    entry2.put("pk1", 3);
    entry2.put("pk2", 4);
    featureView.getFeatureVectors(Lists.newArrayList(entry1, entry2);
    ```

### Retrieval with transformation
If you have specified transformation functions when creating a feature view, you receive transformed feature vectors. If your transformation functions require statistics of training dataset, you must also provide the training data version. `init_serving` will then fetch the statistics and initialize the functions with the required statistics. Then you can follow the above examples and retrieve the feature vectors. Please note that transformed feature vectors can only be returned in the python client but not in the java client.

```python
feature_view.init_serving(training_dataset_version=1)
```

## Passed features
If some of the features values are only known at prediction time and cannot be computed and cached in the online feature store, you can provide those values as `passed_features` option. The `get_feature_vector` method is going to use the passed values to construct the final feature vector to submit to the model.

You can use the `passed_features` parameter to overwrite individual features being retrieved from the online feature store. The feature view will apply the necessary transformations to the passed features as it does for the feature data retrieved from the online feature store.

=== "Python"
    ```python
    # get a single vector
    feature_view.get_feature_vector(
        entry = {"pk1": 1, "pk2": 2},
        passed_features = {"feature_a": "value_a"}
    )

    # get multiple vectors
    feature_view.get_feature_vectors(
        entry = [
            {"pk1": 1, "pk2": 2},
            {"pk1": 3, "pk2": 4},
            {"pk1": 5, "pk2": 6}
        ],
        passed_features = [
            {"feature_a": "value_a1"},
            {"feature_a": "value_a2"},
            {"feature_a": "value_a3"},
        ]
    )
    ```

You can also use the parameter to provide values for all the features which are part of a specific feature group and used in the feature view. In this second case, you do not have to provide the primary key value for that feature group as no data needs to be retrieved from the online feature store.

=== "Python"
    ```python
    # get a single vector, replace values from an entire feature group
    # note how in this example you don't have to provide the value of 
    # pk2, but you need to provide the features coming from that feature group
    # in this case feature_b and feature_c 

    feature_view.get_feature_vector(
        entry = { "pk1": 1 },
        passed_features = {
            "feature_a": "value_a", 
            "feature_b": "value_b", 
            "feature_c": "value_c"
        }
    )
    ```