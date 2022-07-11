# Query vs DataFrame

HSFS provides a DataFrame API to ingest data into the Hopsworks Feature Store. You can also retrieve feature data in a DataFrame, that can either be used directly to train models or [materialized to file(s)](./training-data.md) for later use to train models.

The idea of the Feature Store is to have pre-computed features available for both training and serving models. The key functionality required to generate training datasets from reusable features are: feature selection, joins, filters, and point in time queries. The Query object enables you to select features from different feature groups to join together to be used in a feature view.

The joining functionality is heavily inspired by the APIs used by Pandas to merge DataFrames. The APIs allow you to specify which features to select from which feature group, how to join them and which features to use in join conditions.

=== "Python"
    ```python
    # create a query
    feature_join = rain_fg.select_all() \
        .join(temperature_fg.select_all(), on=["date", "location_id"]) \
        .join(location_fg.select_all())

    # save the query to feature view
    feature_view = fs.create_feature_view(
        name='rain_dataset',
        query=feature_join
    )

    # retrieve the query back from the feature view
    feature_view = fs.get_feature_view(“rain_dataset”, version=1)
    query = feature_view.query
    ```

=== "Scala"
    ```scala
    // create a query
    val featureJoin = (rainFg.selectAll()
        .join(temperatureFg.selectAll(), on=Seq("date", "location_id"))
        .join(locationFg.selectAll()))

    val featureView = featureStore.createFeatureView()
        .name("rain_dataset")
        .query(featureJoin)
        .build();

    // retrieve the query back from the feature view
    val featureView = fs.getFeatureView(“rain_dataset”, 1)
    val query = featureView.getQuery()
    ```

If a data scientist wants to modify a new feature that is not available in the feature store, she can write code to compute the new feature (using existing features or external data) and ingest the new feature values into the feature store. If the new feature is based solely on existing feature values in the Feature Store, we call it a derived feature. The same HSFS APIs can be used to compute derived features as well as features using external data sources.

## The Query Abstraction

Most operations performed on `FeatureGroup` metadata objects will return a `Query` with the applied operation.

### Examples

Selecting features from a feature group is a lazy operation, returning a query with the selected features only:

=== "Python"
    ```python
    rain_fg = fs.get_feature_group("rain_fg")

    # Returns Query
    feature_join = rain_fg.select(["location_id", "weekly_rainfall"])
    ```

=== "Scala"
    ```Scala
    val rainFg = fs.getFeatureGroup("rain_fg")
    
    # Returns Query
    val featureJoin = rainFg.select(Seq("location_id", "weekly_rainfall"))
    ```

#### Join

Similarly, joins return query objects. The simplest join in one where we join all of the features together from two different feature groups without specifying a join key - `HSFS` will infer the join key as a common primary key between the two feature groups.
By default, Hopsworks will use the maximal matching subset of the primary keys of the two feature groups as joining key(s), if not specified otherwise.

=== "Python"
    ```python
    # Returns Query
    feature_join = rain_fg.join(temperature_fg)
    ```

=== "Scala"
    ```Scala
    // Returns Query
    val featureJoin = rainFg.join(temperatureFg)
    ```
More complex joins are possible by selecting subsets of features from the joined feature groups and by specifying a join key and type.
Possible join types are "inner", "left" or "right". Furthermore, it is possible to specify different features for the join key of the left and right feature group.
The join key lists should contain the names of the features to join on.

=== "Python"
    ```python
    feature_join = rain_fg.select_all() \
        .join(temperature_fg.select_all(), on=["date", "location_id"]) \
        .join(location_fg.select_all(), left_on=["location_id"], right_on=["id"], how="left")
    ```

=== "Scala"
    ```scala
    val featureJoin = (rainFg.selectAll()
        .join(temperatureFg.selectAll(), Seq("date", "location_id"))
        .join(locationFg.selectAll(), Seq("location_id"), Seq("id"), "left"))
    ```

!!! error "Nested Joins"
The API currently does not support nested joins. That is joins of joins.
You can fall back to Spark DataFrames to cover these cases. However, if you have to use joins of joins, most likely there is potential to optimise your feature group structure.

#### Filter

In the same way as joins, applying filters to feature groups creates a query with the applied filter.

Filters are constructed with Python Operators `==`, `>=`, `<=`, `!=`, `>`, `<` and using the Bitwise Operators `&` and `|` to construct conjunctions.
For the Scala part of the API, equivalent methods are available in the `Feature` and `Filter` classes.

=== "Python"
    ```python
    filtered_rain = rain_fg.filter(rain_fg.location_id == 10)
    ```

=== "Scala"
    ```scala
    val filteredRain = rainFg.filter(rainFg.getFeature("location_id").eq(10))
    ```

Filters are fully compatible with joins:

=== "Python"
    ```python
    feature_join = rain_fg.select_all() \
        .join(temperature_fg.select_all(), on=["date", "location_id"]) \
        .join(location_fg.select_all(), left_on=["location_id"], right_on=["id"], how="left") \
        .filter((rain_fg.location_id == 10) | (rain_fg.location_id == 20))
    ```

=== "Scala"
    ```scala
    val featureJoin = (rainFg.selectAll()
        .join(temperatureFg.selectAll(), Seq("date", "location_id"))
        .join(locationFg.selectAll(), Seq("location_id"), Seq("id"), "left")
        .filter(rainFg.getFeature("location_id").eq(10).or(rainFg.getFeature("location_id").eq(20))))
    ```

The filters can be applied at any point of the query:

=== "Python"
    ```python
    feature_join = rain_fg.select_all() \
        .join(temperature_fg.select_all().filter(temperature_fg.avg_temp >= 22), on=["date", "location_id"]) \
        .join(location_fg.select_all(), left_on=["location_id"], right_on=["id"], how="left") \
        .filter(rain_fg.location_id == 10)
    ```

=== "Scala"
    ```scala
    val featureJoin = (rainFg.selectAll()
        .join(temperatureFg.selectAll().filter(temperatureFg.getFeature("avg_temp").ge(22)), Seq("date", "location_id"))
        .join(locationFg.selectAll(), Seq("location_id"), Seq("id"), "left")
        .filter(rainFg.getFeature("location_id").eq(10)))
    ```