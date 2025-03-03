# Feature Vectors
The Hopsworks Platform integrates real-time capabilities with its Online Store. Based on [RonDB](https://www.rondb.com/), your feature vectors are served at scale at in-memory latency (~1-10ms). Checkout the benchmarks results [here](https://www.hopsworks.ai/post/feature-store-benchmark-comparison-hopsworks-and-feast#images-2) and the code [here](https://github.com/featurestoreorg/featurestore-benchmarks). The same Feature View which was used to create training datasets can be used to retrieve feature vectors for real-time predictions. This allows you to serve the same features to your model in training and serving, ensuring consistency and reducing boilerplate. Whether you are either inside the Hopsworks platform, a model serving platform, or in an external environment, such as your application server.

Below is a practical guide on how to use the Online Store Python and Java Client. The aim is to get you started quickly by providing code snippets which illustrate various use cases and functionalities of the clients. If you need to get more familiar with the concept of feature vectors, you can read this [short introduction](../../../concepts/fs/feature_view/online_api.md) first.

## Retrieval
You can get back feature vectors from either python or java client by providing the primary key value(s) for the feature view. Note that filters defined in feature view and training data will not be applied when feature vectors are returned. If you need to retrieve a complete value of feature vectors without missing values, the required `entry` are [feature_view.primary_keys](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/api/feature_view_api/#primary_keys). Alternative, you can provide the primary key of the feature groups as the key of the entry. It is also possible to provide a subset of the entry, which will be discussed [below](#partial-feature-retrieval).

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
Starting from python client v3.4, you can specify different values for the primary key of the same name which exists in multiple feature groups but are not joint by the same name. The table below summarises the value of `primary_keys` in different settings. Considering that you are joining 2 feature groups, namely, `left_fg` and `right_fg`, the feature groups have different primary keys, and features (`feature_*`) in each setting. Also, the 2 feature groups are [joint](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/api/query_api/#join) on different *join conditions* and *prefix* as `left_fg.join(right_fg, <join conditions>, prefix=<prefix>)`.

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
=== "Python"
    ```python
    # get a single vector
    feature_view.get_feature_vector(
        entry = {"pk1": 1, "pk2": 2}
    )
    ```
=== "Java"
    ```java
    // get a single vector
    Map<String, Object> entry1 = Maps.newHashMap();
    entry1.put("pk1", 1);
    entry1.put("pk2", 2);
    featureView.getFeatureVector(entry1);
    ```
This call will raise an exception if `pk1 = 1` OR `pk2 = 2` can't be found but also if `pk1 = 1` AND `pk2 = 2` can't be found, meaning, it will not return a partial or empty feature vector.

When retrieving a batch of vectors, the behaviour is slightly different.
=== "Python"
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
=== "Java"
    ```java
    // get multiple vectors
    Map<String, Object> entry2 = Maps.newHashMap();
    entry2.put("pk1", 3);
    entry2.put("pk2", 4);
    Map<String, Object> entry3 = Maps.newHashMap();
    entry3.put("pk1", 5);
    entry3.put("pk2", 6);
    featureView.getFeatureVectors(Lists.newArrayList(entry1, entry2, entry3);
    ```
This call will raise an exception if for example for the third entry `pk1 = 5` OR `pk2 = 6` can't be found, however, it will simply not return a vector for this entry if `pk1 = 5` AND `pk2 = 6`
can't be found.
That means, `get_feature_vectors` will never return partial feature vector, but will omit empty feature vectors.

If you are aware of missing features, you can use the [*passed features*](#passed-features) or [Partial feature retrieval](#partial-feature-retrieval) functionality, described down below.

### Partial feature retrieval
If your model can handle missing value or if you want to impute the missing value, you can get back feature vectors with partial values using python client starting from version 3.4 (Note that this does not apply to java client.). In the example below, let's say you join 2 feature groups by `fg1.join(fg2, left_on=["pk1"], right_on=["pk2"])`, required keys of the `entry` are `pk1` and `pk2`. If `pk2` is not provided, this returns feature values from the first feature group and null values from the second feature group when using the option `allow_missing=True`, otherwise it raises exception.

=== "Python"
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

=== "Python"
    ```python
    feature_view.init_serving(training_dataset_version=1)
    ```

## Passed features
If some of the features values are only known at prediction time and cannot be computed and cached in the online feature store, you can provide those values as `passed_features` option. The `get_feature_vector` method is going to use the passed values to construct the final feature vector to submit to the model.

You can use the `passed_features` parameter to overwrite individual features being retrieved from the online feature store. The feature view will apply the necessary transformations to the passed features as it does for the feature data retrieved from the online feature store.

Please note that passed features is only available in the python client but not in the java client.

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

## Retrieving untransformed feature vectors

By default, the `get_feature_vector` and `get_feature_vectors` functions return transformed feature vectors, which has model-dependent transformations applied and includes on-demand features.

However, you can retrieve the untransformed feature vectors without applying model-dependent transformations while still including on-demand features by setting the `transform` parameter to False.

=== "Python"    
!!! example "Returning untransformed feature vectors"
    ```python
    # Fetching untransformed feature vector.
    untransformed_feature_vector = feature_view.get_feature_vector(
        entry={"id": 1}, transform=False
    )

    # Fetching untransformed feature vectors.
    untransformed_feature_vectors = feature_view.get_feature_vectors(
        entry=[{"id": 1}, {"id": 2}], transform=False
    )
    ```

## Retrieving feature vector without on-demand features

The `get_feature_vector` and `get_feature_vectors` methods can also return untransformed feature vectors without on-demand features by disabling model-dependent transformations and excluding on-demand features. To achieve this, set the  parameters `transform` and `on_demand_features` to `False`.

=== "Python"    
!!! example "Returning untransformed feature vectors"
    ```python
    untransformed_feature_vector = feature_view.get_feature_vector(
        entry={"id": 1}, transform=False, on_demand_features=False
    )
    untransformed_feature_vectors = feature_view.get_feature_vectors(
        entry=[{"id": 1}, {"id": 2}], transform=False, on_demand_features=False
    )
    ```

## Passing Context Variables to Transformation Functions
After [defining a transformation function using a context variable](../transformation_functions.md#passing-context-variables-to-transformation-function), you can pass the required context variables using the `transformation_context` parameter when fetching the feature vectors.

=== "Python"   
    !!! example "Passing context variables while fetching batch data."
        ```python
        # Passing context variable to IN-MEMORY Training Dataset.
        batch_data = feature_view.get_feature_vectors(
            entry = [{ "pk1": 1 }],
            transformation_context={"context_parameter":10}
        )
        ```

## Choose the right Client

The Online Store can be accessed via the **Python** or **Java** client allowing you to use your language of choice to connect to the Online Store. Additionally, the Python client provides two different implementations to fetch data: **SQL** or **REST**. The SQL client is the default implementation. It requires a direct SQL connection to your RonDB cluster and uses python asyncio to offer high performance even when your Feature View rows involve querying multiple different tables. The REST client is an alternative implementation connecting to [RonDB Feature Vector Server](./feature-server.md). Perfect if you want to avoid exposing ports of your database cluster directly to clients. This implementation is available as of Hopsworks 3.7.

Initialise the client by calling the `init_serving` method on the Feature View object before starting to fetch feature vectors. This will initialise the chosen client, test the connection, and initialise the transformation functions registered with the Feature View. Note to use the REST client in the Hopsworks Cluster python environment you will need to provide an API key explicitly as JWT authentication is not yet supported. More configuration options can be found in the [API documentation](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/api/feature_view_api/#init_serving).

=== "Python"
```python
# initialize the SQL client to fetch feature vectors from the Online Store
my_feature_view.init_serving()

# or use the REST client
my_feature_view.init_serving(
    init_rest_client=True,
    config_rest_client={
        "api_key": "your_api_key",
    }
)
```
Once the client is initialised, you can start fetching feature vector(s) via the Feature View methods: `get_feature_vector(s)`. You can initialise both clients for a given Feature View and switch between them by using the force flags in the get_feature_vector(s) methods.

=== "Python"
```python
# initialize both clients and set the default to REST
my_feature_view.init_serving(
    init_rest_client=True,
    init_sql_client=True,
    config_rest_client={
        "api_key": "your_api_key",
    },
    default_client="rest"
)

# this will fetch a feature vector via REST
try:
    my_feature_view.get_feature_vector(
        entry = {"pk1": 1, "pk2": 2},
    )
except TimeoutException:
    # if the REST client times out, the SQL client will be used
    my_feature_view.get_feature_vector(
        entry = {"pk1": 1, "pk2": 2},
        force_sql=True
    )
```

## Feature Server
In addition to Python/Java clients, from Hopsworks 3.3, a new [feature server](./feature-server.md) implemented in Go is introduced. With this new API, single or batch feature vectors can be retrieved in any programming language. Note that you can connect to the Feature Vector Server via any REST client. However registered transformation function will not be applied to values in the JSON response and values stored in Feature Groups which contain embeddings will be missing.

