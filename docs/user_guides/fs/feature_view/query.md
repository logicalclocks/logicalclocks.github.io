# Query vs DataFrame

HSFS provides a DataFrame API to ingest data into the Hopsworks Feature Store.
You can also retrieve feature data in a DataFrame, that can either be used directly to train models or [materialized to file(s)](./training-data.md) for later use to train models.

The idea of the Feature Store is to have pre-computed features available for both training and serving models.
The key functionality required to generate training datasets from reusable features are: feature selection, joins, filters, and point in time queries.
The Query object enables you to select features from different feature groups to join together to be used in a feature view.

The joining functionality is heavily inspired by the APIs used by Pandas to merge DataFrames.
The APIs allow you to specify which features to select from which feature group, how to join them and which features to use in join conditions.

=== "Python"
    ```python
    fs = ...
    credit_card_transactions_fg = fs.get_feature_group(name="credit_card_transactions", version=1)
    account_details_fg = fs.get_feature_group(name="account_details", version=1)
    merchant_details_fg = fs.get_feature_group(name="merchant_details", version=1)

    # create a query
    selected_features = credit_card_transactions_fg.select_all() \
        .join(account_details_fg.select_all(), on=["cc_num"]) \
        .join(merchant_details_fg.select_all())

    # save the query to feature view
    feature_view = fs.create_feature_view(
        version=1,
        name='credit_card_fraud',
        labels=["is_fraud"],
        query=selected_features
    )

    # retrieve the query back from the feature view
    feature_view = fs.get_feature_view(“credit_card_fraud”, version=1)
    query = feature_view.query
    ```

=== "Scala"
    ```scala

    val fs = ...
    val creditCardTransactionsFg = fs.getFeatureGroup("credit_card_transactions", 1)
    val accountDetailsFg = fs.getFeatureGroup(name="account_details", version=1)
    val merchantDetailsFg = fs.getFeatureGroup("merchant_details", 1)

    // create a query
    val selectedFeatures = (creditCardTransactionsFg.selectAll()
        .join(accountDetailsFg.selectAll(), on=Seq("cc_num"))
        .join(merchantDetailsFg.selectAll()))

    val featureView = featureStore.createFeatureView()
        .name("credit_card_fraud")
        .query(selectedFeatures)
        .build();

    // retrieve the query back from the feature view
    val featureView = fs.getFeatureView(“credit_card_fraud”, 1)
    val query = featureView.getQuery()
    ```

If a data scientist wants to modify a new feature that is not available in the feature store, she can write code to compute the new feature (using existing features or external data) and ingest the new feature values into the feature store.
If the new feature is based solely on existing feature values in the Feature Store, we call it a derived feature.
The same HSFS APIs can be used to compute derived features as well as features using external data sources.

## The Query Abstraction

Most operations performed on `FeatureGroup` metadata objects will return a `Query` with the applied operation.

### Examples

Selecting features from a feature group is a lazy operation, returning a query with the selected features only:

=== "Python"
    ```python
    credit_card_transactions_fg = fs.get_feature_group("credit_card_transactions")

    # Returns Query
    selected_features = credit_card_transactions_fg.select(["amount", "latitude", "longitude"])
    ```

=== "Scala"
    ```Scala
    val creditCardTransactionsFg = fs.getFeatureGroup("credit_card_transactions")

    # Returns Query
    val selectedFeatures = creditCardTransactionsFg.select(Seq("amount", "latitude", "longitude"))
    ```

#### Join

Similarly, joins return query objects.
The simplest join in one where we join all of the features together from two different feature groups without specifying a join key - `HSFS` will infer the join key as a common primary key between the two feature groups.
By default, Hopsworks will use the maximal matching subset of the primary keys of the two feature groups as joining key(s), if not specified otherwise.

=== "Python"
    ```python
    # Returns Query
    selected_features = credit_card_transactions_fg.join(account_details_fg)
    ```

=== "Scala"
    ```Scala
    // Returns Query
    val selectedFeatures = creditCardTransactionsFg.join(accountDetailsFg)
    ```
More complex joins are possible by selecting subsets of features from the joined feature groups and by specifying a join key and type.
Possible join types are "inner", "left" or "right".
By default`join_type` is `"left".
Furthermore, it is possible to specify different
features for the join key of the left and right feature group.
The join key lists should contain the names of the features to join on.

=== "Python"
    ```python
    selected_features = credit_card_transactions_fg.select_all() \
        .join(account_details_fg.select_all(), on=["cc_num"]) \
        .join(merchant_details_fg.select_all(), left_on=["merchant_id"], right_on=["id"], join_type="inner")
    ```

=== "Scala"
    ```scala
    val selectedFeatures = (creditCardTransactionsFg.selectAll()
        .join(accountDetailsFg.selectAll(), Seq("cc_num"))
        .join(merchantDetailsFg.selectAll(), Seq("merchant_id"), Seq("id"), "inner"))
    ```

!!! warning
    If there is feature name clash in the query then prefixes will be automatically generated and applied.
    Generated prefix is feature group alias in the query (e.g., fg1, fg2).
    Prefix is applied to the right feature group of the query.

### Data modeling in Hopsworks

Since v4.0 Hopsworks Feature selection API supports both Star and Snowflake Schema data models.

#### Star schema data model

When choosing Star Schema data model all tables are children of the parent (the left most) feature group, which has all
foreign keys for its child feature groups.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/fs/feature_view/star.png" alt="Star schema data model">
    <figcaption>Star schema data model</figcaption>
  </figure>
</p>

=== "Python"
    ```python
       selected_features = credit_card_transactions.select_all()
        .join(aggregated_cc_transactions.select_all())
        .join(account_details.select_all())
        .join(merchant_details.select_all())
        .join(cc_issuer_details.select_all())
    ```

In online inference, when you want to retrieve features in your online model, you have to provide all foreign key values,
known as the serving_keys, from the parent feature group to retrieve your precomputed feature values using the feature view.

=== "Python"
    ```python
      feature vector = feature_view.get_feature_vector({
        ‘cc_num’: “1234 5555 3333 8888”,
        ‘issuer_id’: 20440455,
        ‘merchant_id’: 44208484,
        ‘account_id’: 84403331
        })
    ```

#### Snowflake schema

Hopsworks also provides the possibility to define a feature view that consists of a nested tree of children (to up to a depth of 20) from the root (left most) feature group.
This is called  Snowflake Schema data model where you need to build nested tables (subtrees) using joins, and then join the subtrees to their parents iteratively until you reach the root node (the leftmost feature group in the feature selection):

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/fs/feature_view/snowflake.png" alt="Snowflake schema data model">
    <figcaption>Snowflake schema data model</figcaption>
  </figure>
</p>

=== "Python"
    ```python
        nested_selection = aggregated_cc_transactions.select_all()
        .join(account_details.select_all())
        .join(cc_issuer_details.select_all())

        selected_features = credit_card_transactions.select_all()
                .join(nested_selection)
        .join(merchant_details.select_all())
    ```

Now, you have the benefit that in online inference you only need to pass two serving key values (the foreign keys of the leftmost feature group) to retrieve the precomputed features:

=== "Python"
    ```python
        feature vector = feature_view.get_feature_vector({
          ‘cc_num’: “1234 5555 3333 8888”,
          ‘merchant_id’: 44208484,
        })
    ```

#### Filter

In the same way as joins, applying filters to feature groups creates a query with the applied filter.

Filters are constructed with Python Operators `==`, `>=`, `<=`, `!=`, `>`, `<` and additionally with the methods `isin` and `like`.
Bitwise Operators `&` and `|` are used to construct conjunctions.
For the Scala part of the API, equivalent methods are available in the `Feature` and `Filter` classes.

=== "Python"
    ```python
    filtered_credit_card_transactions = credit_card_transactions_fg.filter(credit_card_transactions_fg.category == "Grocery")
    ```

=== "Scala"
    ```scala
    val filteredCreditCardTransactions = creditCardTransactionsFg.filter(creditCardTransactionsFg.getFeature("category").eq("Grocery"))
    ```

Filters are fully compatible with joins:

=== "Python"
    ```python
    selected_features = credit_card_transactions_fg.select_all() \
        .join(account_details_fg.select_all(), on=["cc_num"]) \
        .join(merchant_details_fg.select_all(), left_on=["merchant_id"], right_on=["id"]) \
        .filter((credit_card_transactions_fg.category == "Grocery") | (credit_card_transactions_fg.category == "Restaurant/Cafeteria"))
    ```

=== "Scala"
    ```scala
    val selectedFeatures = (creditCardTransactionsFg.selectAll()
        .join(accountDetailsFg.selectAll(), Seq("cc_num"))
        .join(merchantDetailsFg.selectAll(), Seq("merchant_id"), Seq("id"), "left")
        .filter(creditCardTransactionsFg.getFeature("category").eq("Grocery").or(creditCardTransactionsFg.getFeature("category").eq("Restaurant/Cafeteria"))))
    ```

The filters can be applied at any point of the query:

=== "Python"
    ```python
    selected_features = credit_card_transactions_fg.select_all() \
        .join(accountDetails_fg.select_all().filter(accountDetails_fg.avg_temp >= 22), on=["cc_num"]) \
        .join(merchant_details_fg.select_all(), left_on=["merchant_id"], right_on=["id"]) \
        .filter(credit_card_transactions_fg.category == "Grocery")
    ```

=== "Scala"
    ```scala
    val selectedFeatures = (creditCardTransactionsFg.selectAll()
        .join(accountDetailsFg.selectAll().filter(accountDetailsFg.getFeature("avg_temp").ge(22)), Seq("cc_num"))
        .join(merchantDetailsFg.selectAll(), Seq("merchant_id"), Seq("id"), "left")
        .filter(creditCardTransactionsFg.getFeature("category").eq("Grocery")))
    ```

#### Joins and/or Filters on feature view query

The query retrieved from a feature view can be extended with new joins and/or new filters.
However, this operation will not update the metadata and persist the updated query of the feature view itself.
This query can then be used to create a new feature view.

=== "Python"
    ```python
    fs = ...
    merchant_details_fg = fs.get_feature_group(name="merchant_details", version=1)
    credit_card_transactions_fg = fs.get_feature_group(name="credit_card_transactions", version=1)
    feature_view = fs.get_feature_view(“credit_card_fraud”, version=1)
    feature_view.query \
        .join(merchant_details_fg.select_all()) \
        .filter(credit_card_transactions_fg.category == "Cash Withdrawal")
    ```

=== "Scala"
    ```scala
    val fs = ...
    val merchantDetailsFg = fs.getFeatureGroup("merchant_details", 1)
    val creditCardTransactionsFg = fs.getFeatureGroup("credit_card_transactions", 1)
    val featureView = fs.getFeatureView(“credit_card_fraud”, 1)
    featureView.getQuery()
        .join(merchantDetailsFg.selectAll())
        .filter(creditCardTransactionsFg.getFeature("category").eq("Cash Withdrawal"))
    ```

!!! warning
    Every join/filter operation applied to an existing feature view query instance will update its state and accumulate.
    To successfully apply new join/filter logic it is recommended to refresh the query instance by re-fetching the feature view:

=== "Python"
    ```python
    fs = ...

    merchant_details_fg = fs.get_feature_group(name="merchant_details", version=1)
    account_details_fg = fs.get_feature_group(name="account_details", version=1)
    credit_card_transactions_fg = fs.get_feature_group(name="credit_card_transactions", version=1)

    # fetch new feature view and its query instance
    feature_view = fs.get_feature_view(“credit_card_fraud”, version=1)

    # apply join/filter logic based on purchase type
    feature_view.query.join(merchant_details_fg.select_all()) \
        .filter((credit_card_transactions_fg.category == "Cash Withdrawal"))

    # to apply new logic independent of purchase type from above
    # re-fetch new feature view and its query instance
    feature_view = fs.get_feature_view(“credit_card_fraud”, version=1)

    # apply new join/filter logic based on account details
    feature_view.query.join(merchant_details_fg.select_all()) \
        .filter(account_details_fg.gender == "F")
    ```

=== "Scala"
    ```scala
    fs = ...
    merchantDetailsFg = fs.getFeatureGroup("merchant_details", 1)
    accountDetailsFg = fs.getFeatureGroup("account_details", 1)
    creditCardTransactionsFg = fs.getFeatureGroup("credit_card_transactions", 1)

    // fetch new feature view and its query instance
    val featureView = fs.getFeatureView(“credit_card_fraud”, version=1)

    // apply join/filter logic based on purchase type
    featureView.getQuery.join(merchantDetailsFg.selectAll())
        .filter(creditCardTransactionsFg.getFeature("category").eq("Cash Withdrawal"))

    // to apply new logic independent of purchase type from above
    // re-fetch new feature view and its query instance
    val featureView = fs.getFeatureView(“credit_card_fraud”, 1)

    // apply new join/filter logic based on account details
    featureView.getQuery.join(merchantDetailsFg.selectAll())
        .filter(accountDetailsFg.getFeature("gender").eq("F"))
    ```
