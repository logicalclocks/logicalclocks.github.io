# Feature Vectors
Once you have trained a model, it is time to deploy it. You can get back all the features required to feed into an ML model with a single method call. A feature view provides great flexibility for you to retrieve a vector (or row) of features from any environment, whether you are either inside the Hopsworks platform, a model serving platform, or in an external environment, such as your application server. Harnessing the powerful [RonDB](https://www.rondb.com/), feature vectors are served at in-memory latency.

If you want to understand more about the concept of feature vectors, you can refer to [here](../../../concepts/fs/feature_view/online_api.md).

## Retrieval
You can get back feature vectors from either python or java client by providing the primary key value(s) for the feature view. Note that filters defined in feature view and training data will not be applied when feature vectors are returned. If you need to retrieve a complete value of feature vectors without missing values, the required `entry` are [feature_view.primary_keys](https://docs.hopsworks.ai/feature-store-api/3.7/generated/api/feature_view_api/#primary_keys). Alternative, you can provide the primary key of the feature groups as the key of the entry. It is also possible to provide a subset of the entry, which will be discussed [below](#partial-feature-retrieval).

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

### Required entry
Starting from python client v3.4, you can specify different values for the primary key of the same name which exists in multiple feature groups but are not joint by the same name. The table below summarises the value of `primary_keys` in different settings. Considering that you are joining 2 feature groups, namely, `left_fg` and `right_fg`, the feature groups have different primary keys, and features (`feature_*`) in each setting. Also, the 2 feature groups are [joint](https://docs.hopsworks.ai/feature-store-api/3.7/generated/api/query_api/#join) on different *join conditions* and *prefix* as `left_fg.join(right_fg, <join conditions>, prefix=<prefix>)`.

For java client, and python client before v3.4, the `primary_keys` are the set of primary key of all the feature groups in the query. Python client is backward compatible. It means that the `primary_keys` used before v3.4 can be applied to python client of later versions as well.

| Setting | primary key of `left_fg` | primary key of `right_fg` | join conditions                            | prefix | primary_keys                                   | note                                                     |
|------|----------------------------|-----------------------------|-------------------------------------------|--------|-----------------------------------------------|----------------------------------------------------------|
|   1  | id                        | id                         | ```on=["id"]```                               |        | id                                           | Same feature name is used in the join.                        |
|   2  | id1                        | id2                         | `left_on=["id1"], right_on=["id2"]`        |        | id1                                           |  Different feature names are used in the join.               |
|   3  | id1, id2                   | id1                         | `on=["id1"]`                               |        | id1, id2                                      | `id2` is not part of the join conditions                  |
|   4  | id, user_id                | id                          | `left_on=["user_id"], right_on=["id"]`     |        | id, user_id                                   | Value of `user_id` is used for retrieving features from `right_fg` |
|   5  | id1                        | id1, id2                    | `on=["id1"]`                               |        | id1, id2                                      | `id2` is not part of the join conditions                  |
|   6  | id                         | id, user_id                 | `left_on=["id"], right_on=["user_id"]`     | “right_“| id, “right_id“ | Value of “right_id“ and "id" are used for retrieving features from `right_fg` |
|   7  | id                         | id, user_id                 | `left_on=["id"], right_on=["user_id"]`     |         | id, “fgId_&lt;rightFgId&gt;_&lt;joinIndex&gt;_id” | Value of “fgId_&lt;rightFgId&gt;_&lt;joinIndex&gt;_id“ and "id" are used for retrieving features from `right_fg`. See note below. |
|   8  | id                        | id                         | `left_on=["id"], right_on=["feature_1"]`  | “right_“ | id, “right_id“                              | No primary key from `right_fg` is used in the join. Value of `right_id` is used for retrieving features from `right_fg` |
|   9  | id                        | id                         | `left_on=["id"], right_on=["feature_1"]`  |          | id1, “fgId_&lt;rightFgId&gt;_&lt;joinIndex&gt;_id” | No primary key from `right_fg` is used in the join. Value of "fgId_&lt;rightFgId&gt;_&lt;joinIndex&gt;_id" is used for retrieving features from "right_fg`. See note below. |
|   10  | id                        | id                         | `left_on=["feature_1"], right_on=["id"]` | “right_“ | id, “right_id“                              | No primary key from `left_fg` is used in the join. Value of `right_id` is used for retrieving features from `right_fg` |
|   11  | id                        | id                         | `left_on=["feature_1"], right_on=["id"]` |          | id1, “fgId_&lt;rightFgId&gt;_&lt;joinIndex&gt;_id” | No primary key from `left_fg` is used in the join. Value of “fgId_&lt;rightFgId&gt;_&lt;joinIndex&gt;_id” is used for retrieving features from `right_fg`. See note below. |
|   12  | user, year                 | user, year                  | `left_on=["user"], right_on=["user"]`     | “right_“ | user, year, “right_year“                   | Value of "user" and "right_year" are used for retrieving features from `right_fg`. `right_fg` can be the same as feature group as `left_fg`. |
|   13  | user, year                 | user, year                  | `left_on=["user"], right_on=["user"]`     |        | user, year, “fgId_&lt;rightFgId&gt;_&lt;joinIndex&gt;_year” | Value of "user" and "fgId_&lt;rightFgId&gt;_&lt;joinIndex&gt;_year" are used for retrieving features from `right_fg`. `right_fg` can be the same as feature group as `left_fg`. See note below. |

Note:

"&lt;rightFgId&gt;" can be found by `right_fg.id`. "&lt;joinIndex&gt;" is the order or the feature group in the join. In the example, it is 1 because `right_fg` is in the first join in the query `left_fg.join(right_fg, <join conditions>)`.

### Missing Primary Key Entries

It can happen that some of the primary key entries are not available in some or all of the feature groups used by a feature view.

Take the above example assuming the feature view consists of two joined feature groups, first one with primary key column `pk1`, the second feature group with primary key column `pk2`.
```python
# get a single vector
feature_view.get_feature_vector(
    entry = {"pk1": 1, "pk2": 2}
)
```
This call will raise an exception if `pk1 = 1` OR `pk2 = 2` can't be found but also if `pk1 = 1` AND `pk2 = 2` can't be found, meaning, it will not return a partial or empty feature vector.

When retrieving a batch of vectors, the behaviour is slightly different.
```python
# get multiple vectors
feature_view.get_feature_vectors(
    entry = [
        {"pk1": 1, "pk2": 2},
        {"pk1": 3, "pk2": 4},
        {"pk1": 5, "pk2": 6}
    ]
)
```
This call will raise an exception if for example for the third entry `pk1 = 5` OR `pk2 = 6` can't be found, however, it will simply not return a vector for this entry if `pk1 = 5` AND `pk2 = 6`
can't be found.
That means, `get_feature_vectors` will never return partial feature vector, but will omit empty feature vectors.

If you are aware of missing features, you can use the [*passed features*](#passed-features) or [Partial feature retrieval](#partial-feature-retrieval) functionality, described down below.

### Partial feature retrieval
If your model can handle missing value or if you want to impute the missing value, you can get back feature vectors with partial values using python client starting from version 3.4. In the example below, let's say you join 2 feature groups by `fg1.join(fg2, left_on=["pk1"], right_on=["pk2"])`, required keys of the `entry` are `pk1` and `pk2`. If `pk2` is not provided, this returns feature values from the first feature group and null values from the second feature group when using the option `allow_missing=True`, otherwise it raises exception.

```python
# get a single vector with 
feature_view.get_feature_vector(
    entry = {"pk1": 1},
    allow_missing=True
)

# get multiple vectors
feature_view.get_feature_vectors(
    entry = [
        {"pk1": 1},
        {"pk1": 3},
    ],
    allow_missing=True
)
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

## Feature Server
In addition to Python/Java clients, from Hopsworks 3.3, a new [feature server](./feature-server.md) implemented in Go is introduced. With this new API, single or batch feature vectors can be retrieved in any programming language.
