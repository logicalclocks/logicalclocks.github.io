# Query vs DataFrame

Hopsworks provides a DataFrame API to ingest data into the Hopsworks Feature Store.
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
The same Hopsworks APIs can be used to compute derived features as well as features using external data sources.

## The Query Abstraction

Most operations performed on `FeatureGroup` metadata objects will return a `Query` with the applied operation.

### Examples

Selecting features from a feature group is a lazy operation, returning a query with the selected features only:

=== "Python"

    ```python
    credit_card_transactions_fg = fs.get_feature_group("credit_card_transactions")

    # Returns Query
    selected_features = credit_card_transactions_fg.select(
        ["amount", "latitude", "longitude"]
    )
    ```

=== "Scala"

    ```scala
    val creditCardTransactionsFg = fs.getFeatureGroup("credit_card_transactions")

    # Returns Query
    val selectedFeatures = creditCardTransactionsFg.select(Seq("amount", "latitude", "longitude"))
    ```

#### Join

Similarly, joins return query objects.
The simplest join in one where we join all of the features together from two different feature groups without specifying a join key - `Hopsworks` will infer the join key as a common primary key between the two feature groups.
By default, Hopsworks will use the maximal matching subset of the primary keys of the two feature groups as joining key(s), if not specified otherwise.

=== "Python"

    ```python
    # Returns Query
    selected_features = credit_card_transactions_fg.join(account_details_fg)
    ```

=== "Scala"

    ```scala
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
    selected_features = (
        credit_card_transactions_fg.select_all()
        .join(account_details_fg.select_all(), on=["cc_num"])
        .join(
            merchant_details_fg.select_all(),
            left_on=["merchant_id"],
            right_on=["id"],
            join_type="inner",
        )
    )
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

The Python SQL client executes each nested subtree as one SQL statement.
The Python REST client pushes supported nested subtrees to RonDB through RonSQL, so callers provide the same root serving keys for either client.
REST serving requires every nested join to cover the child feature group's complete primary key and all feature groups in the subtree to belong to the same feature store.
Inner and left joins are supported, and all nested joins in a subtree must use the same join type, because a subtree mixing them cannot be split into independent REST queries without changing which rows an inner-join miss removes.
Right joins, full joins, subtrees mixing inner and left joins, partial-primary-key hops, and cross-feature-store nested joins require the SQL client.

#### Filter

In the same way as joins, applying filters to feature groups creates a query with the applied filter.

Filters are constructed with Python Operators `==`, `>=`, `<=`, `!=`, `>`, `<` and additionally with the methods `isin` and `like`.
Bitwise Operators `&` and `|` are used to construct conjunctions.
For the Scala part of the API, equivalent methods are available in the `Feature` and `Filter` classes.

=== "Python"

    ```python
    filtered_credit_card_transactions = credit_card_transactions_fg.filter(
        credit_card_transactions_fg.category == "Grocery"
    )
    ```

=== "Scala"

    ```scala
    val filteredCreditCardTransactions = creditCardTransactionsFg.filter(creditCardTransactionsFg.getFeature("category").eq("Grocery"))
    ```

Filters are fully compatible with joins:

=== "Python"

    ```python
    selected_features = (
        credit_card_transactions_fg.select_all()
        .join(account_details_fg.select_all(), on=["cc_num"])
        .join(
            merchant_details_fg.select_all(),
            left_on=["merchant_id"],
            right_on=["id"],
        )
        .filter(
            (credit_card_transactions_fg.category == "Grocery")
            | (credit_card_transactions_fg.category == "Restaurant/Cafeteria")
        )
    )
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
    selected_features = (
        credit_card_transactions_fg.select_all()
        .join(
            accountDetails_fg.select_all().filter(
                accountDetails_fg.avg_temp >= 22
            ),
            on=["cc_num"],
        )
        .join(
            merchant_details_fg.select_all(),
            left_on=["merchant_id"],
            right_on=["id"],
        )
        .filter(credit_card_transactions_fg.category == "Grocery")
    )
    ```

=== "Scala"

    ```scala
    val selectedFeatures = (creditCardTransactionsFg.selectAll()
        .join(accountDetailsFg.selectAll().filter(accountDetailsFg.getFeature("avg_temp").ge(22)), Seq("cc_num"))
        .join(merchantDetailsFg.selectAll(), Seq("merchant_id"), Seq("id"), "left")
        .filter(creditCardTransactionsFg.getFeature("category").eq("Grocery")))
    ```

#### Collect recent rows

Use `collect` to include the most recent matching rows for each entity in a feature view.
The operation produces one array-of-struct feature whose elements contain the selected value features and the ordering feature.
This preserves the relationship between values in the same source row, including null values.

`collect` is a non-terminal query operation, so you can filter the source rows before collecting them and join other feature groups afterward.
Filters are applied before the row limit, which means the result contains the most recent N rows that match the filter.
For online serving, filters on a collected or aggregated feature group must be AND-combined comparisons of a feature against a value, because OR conditions and feature-to-feature comparisons cannot be applied to the online statement without breaking the match with offline training data.

```python
transactions_fg = fs.get_feature_group(name="transactions", version=1)
customers_fg = fs.get_feature_group(name="customers", version=1)

query = (
    transactions_fg.select(["user_id", "event_time", "amount", "category"])
    .filter(transactions_fg.amount > 0)
    .collect(100, order_by="event_time")
    .join(customers_fg.select(["country", "tier"]), on=["user_id"])
)
```

The `order_by` argument defaults to the feature group's event-time feature.
The default output order is newest first.
Set `ascending=True` to return the same most recent N rows from oldest to newest.

For online feature groups, the primary key must contain the entity key followed by the ordering feature.
For example, a per-user transaction history ordered by event time uses the primary key `(user_id, event_time)`.
The ordering feature is not supplied as a serving key because the lookup identifies an entity rather than one event.

Labels cannot be collected because a collected output is an input feature containing several historical rows.
Complex-typed value features (arrays, maps, structs, and binary) cannot be collected on an online-enabled feature group, because the online clients cannot yet decode them inside the collected rows.
The value of `n` must be a positive integer and cannot exceed the maximum configured by the Hopsworks administrator.
The product of `n` and the number of selected features is also capped, because point-in-time training data materializes that many values for every source event.

When time-to-live is enabled on the source feature group, offline training data uses the same lookback horizon as online serving.
An explicit lookback can narrow that horizon but cannot make it wider than the feature group's time-to-live.

#### Aggregate rows by entity

Use `aggregate` to define scalar features computed from all matching rows for each entity.
The operation supports `count`, `sum`, `min`, `max`, and `avg`.
Use the special `"*"` key with `count` to count rows.
Use a comma-separated feature key with `greatest` or `least` to aggregate the row-wise greatest or least value.

```python
from datetime import timedelta

transactions_fg = fs.get_feature_group(name="transactions", version=1)

query = (
    transactions_fg.select(["user_id", "event_time", "amount", "fee"])
    .filter(transactions_fg.category == "grocery")
    .aggregate(
        {
            "amount": ["count", "sum", "avg"],
            "*": ["count"],
            "amount,fee": ["greatest"],
        },
        window=timedelta(days=30),
    )
)
```

Each feature and function pair creates one scalar output feature.
For example, the query above creates `amount_count`, `amount_sum`, `amount_avg`, `count`, and `amount_fee_greatest`.
The functions are type-checked when the feature view is created: `sum` and `avg` require numeric features, `min` and `max` accept any non-complex feature, and `greatest` and `least` require integer features.

The optional `window` is a trailing event-time interval, given as a whole number of seconds or a timedelta.
A windowed aggregation requires the feature group to declare a TIMESTAMP event-time feature.
Online serving anchors the window at the read time, while point-in-time training data anchors it at each training row's own event time, so a training row never includes source events that had already expired at that row's time.
If the source feature group has time-to-live enabled, the aggregation window cannot exceed the time-to-live period because older rows are unavailable during online serving.

For online feature groups, the primary key must contain the entity key followed by the event-time feature, exactly like `collect`, so the online store keeps per-entity history.
In a feature view with point-in-time joins, a windowed aggregation must be joined directly to the root feature group with an inner or left join.
Query shapes that cannot be computed point-in-time correct are rejected with an error when the feature view is created, instead of silently producing training data with future leakage.

`aggregate` and `collect` are mutually exclusive on the same query node.
Sub-entity grouping through `group_by` is not supported.
You can apply either operation independently to different feature groups in the same feature-view query.

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
        .filter(credit_card_transactions_fg.category == "Cash Withdrawal")

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
