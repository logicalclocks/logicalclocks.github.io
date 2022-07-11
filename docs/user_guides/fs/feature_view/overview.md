# Feature View

A feature view is a set of features that come from one or more feature groups. It is a logical view over the feature groups, as the feature data is only stored in feature groups. Feature views are used to read feature data for both training and serving (online and batch). You can create [training datasets](training-data.md), create [batch data](batch-data.md) and get [feature vectors](feature-vectors.md).

If you want to understand more about the concept of feature view, you can refer to [here](../../../concepts/fs/feature_view/fv_overview.md).

## Creation
[Query](./query.md) and [transformation function](./transformation-function.md) are the building blocks of a feature view. You can define your set of features by building a `query`. You can also define which columns in your feature view are the `labels`, which is useful for supervised machine learning tasks. Furthermore, in python client, each feature can be attached to its own transformation function. This way, when a feature is read (for training or scoring), the transformation is executed on-demand - just before the feature data is returned. For example, when a client reads a numerical feature, the feature value could be normalized by a StandardScalar transformation function before it is returned to the client.

=== "Python"

    ```python
    # create a simple feature view
    feature_view = fs.create_feature_view(
        name='transactions_view',
        query=query
    )
    
    # create a feature view with transformation and label
    feature_view = fs.create_feature_view(
        name='transactions_view',
        query=query,
        labels=["fraud_label"],
        transformation_functions={
            "amount": fs.get_transformation_function(name="standard_scaler", version=1)
        }
    )
    ```

=== "Java"

    ```java
    // create a simple feature view
    FeatureView featureView = featureStore.createFeatureView()
                                            .name("transactions_view)
                                            .query(query)
                                            .build();

    // create a feature view with label
    FeatureView featureView = featureStore.createFeatureView()
                                            .name("transactions_view)
                                            .query(query)
                                            .labels(Lists.newArrayList("fraud_label")
                                            .build();
    ```

You can refer to [query](./query.md) and [transformation function](./transformation-function.md) for creating `query` and `transformation_function`.

## Retrieval
Once you have created a feature view, you can retrieve it by its name and version.

=== "Python"
    ```python
    feature_view = fs.get_feature_view(name="transactions_view", version=1)
    ```
=== "Java"
    ```java
    FeatureView featureView = featureStore.getFeatureView("transactions_view", 1)
    ```

## Deletion
If there are some feature view instances which you do not use anymore, you can delete a feature view. It is important to mention that all training datasets (include all materialised hopsfs training data) will be deleted along with the feature view.

=== "Python"
    ```python
    feature_view.delete()
    ```
=== "Java"
    ```java
    featureView.delete()
    ```

## Tags

Feature views also support tags. You can attach, get, and remove tags. You can refer to [here]() if you want to learn more about how tags work.

=== "Python"
    ```python
    # attach
    feature_view.add_tag(name="tag_schema", value={"key", "value"}
    
    # get
    feature_view.get_tag(name="tag_schema")
    
    #remove
    feature_view.delete_tag(name="tag_schema")
    ```
=== "Java"
    ```java
    // attach
    Map<String, String> tag = Maps.newHashMap();
    tag.put("key", "value");
    featureView.addTag("tag_schema", tag)

    // get
    featureView.getTag("tag_schema")

    // remove
    featureView.deleteTag("tag_schema")
    ```

## Next
Once you have created a feature view, you can now [create training data](./training-data.md)