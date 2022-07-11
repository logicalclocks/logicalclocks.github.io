External feature groups are offline feature groups where their data is stored in an external table. An external table requires a storage connector, defined with the Connector API (or more typically in the user interface), to enable HSFS to retrieve data from the external table. An external table includes a user-defined SQL string for retrieving data, but you also perform SQL operations, including projections, aggregations, and so on. The SQL query is executed on-demand when HSFS retrieves data from the external Feature Group, for example, when creating training data using features in the external table.

In the image below, we can see that HSFS currently supports a large number of data sources, including any JDBC-enabled source, Snowflake, Data Lake, Redshift, BigQuery, S3, ADLS, GCS, and Kafka

<img src="../../../../assets/images/concepts/fs/fg-connector-api.svg">

