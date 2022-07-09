The Hopsworks Feature Store is based on an offline data store, queryable via an Apache Hive API, and an online data store, queryable via a MySQL Server API.

Given that Feature Groups in Hopsworks have well-defined schemas, features in the Hopsworks Feature Store can be analyzed and reports can be generated from them using any BI Tools that include connectors for MySQL (JDBC) and Apache Hive (2-way TLS required). One platform we use with customers is [Apache Superset](https://superset.apache.org/), as it can be configured alongside Hopsworks to provide BI Tooling capabilities.
