# Development Outside Hopsworks

You can write programs that use Hopsworks in any [Python, Spark, or PySpark environment](../../user_guides/integrations/index.md).
Hopsworks also supports running SQL queries to compute features in external data warehouses.
The Feature Store can also be queried with SQL.

There is REST API for Hopsworks that can be used with a valid API key, generated in Hopsworks.
However, it is often easier to develop your programs against the Hopsworks SDK, available in Python and Java/Scala, which covers the feature store, the model registry and model serving.
The same library ships the `hops` command line, so a shell, a CI pipeline or a coding agent on your machine can read and write the project with the same API key; see the [Hopsworks CLI guide][hopsworks-cli].

--8<-- "concepts/dev/outside/development-outside-hopsworks.html"
