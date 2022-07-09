# Feature Vectors
Once you have trained a model, it is time to deploy it. You can get back all the features required to feed into an ML model with a single method call. A feature view provides great flexibility for you to retrieve a vector (or row) of features from any environment, whether you are either inside the Hopsworks platform, a model serving platform, or in an external environment, such as your application server. Harnessing the powerful [RonDB](https://www.rondb.com/), feature vectors are served at in-memory latency.

If you want to understand more about the concept of feature vectors, you can refer to [here](../../../concepts/fs/feature_view/online_api.md).

## Retrieval
You can get back feature vectors from either python or java client by providing the primary key value(s) for the feature view.

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

## Preview
In order to enable ML engineers to test feature serving easily, a feature view can return a sample of feature vectors without specifying any primary keys.
=== "Python"
    ```python
    # get a single vector
    feature_view.preview_feature_vector()

    # get multiple vectors
    feature_view.preview_feature_vectors(n=3) # n = size of feature vectors
    ```
=== "Java"
    ```java
    // get a single vector
    featureView.previewFeatureVector();

    // get multiple vectors
    featureView.previewFeatureVectors(3);
    ```

## Passed features
fabio's part
