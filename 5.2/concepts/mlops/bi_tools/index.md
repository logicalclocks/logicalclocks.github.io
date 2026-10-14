# BI Tools

Feature groups have well-defined schemas and live in two stores, so any BI tool that speaks SQL can analyze features and build reports on them.

- The offline store is queried through the [Query Engine](../../user_guides/projects/trino/query_engine.md), Trino, with one catalog per table format (`delta`, `iceberg`, `hudi`).
  Any tool with a Trino connector (JDBC or ODBC) can read it.
- The online store, RonDB, is queried over the MySQL protocol, so any tool with a MySQL connector can read the latest feature values.

Hopsworks bundles [Apache Superset](https://superset.apache.org/) as a project service, already connected to the project's Trino catalogs.
Dashboards live inside the project and follow its access control.

<figure>
  <img src="../../../assets/images/guides/superset/superset-dashboards.png" alt="Superset dashboards listed inside a Hopsworks project" />
  <figcaption>Superset dashboards inside a project, with their public and shared status.</figcaption>
</figure>

SQL Lab in Superset runs directly against the feature store: pick the project's Trino connection, then the catalog matching the feature group's table format.

<figure>
  <img src="../../../assets/images/guides/superset/sql-lab-catalog.png" alt="Superset SQL Lab with the project's Trino connection and the delta, hudi and iceberg catalogs" />
  <figcaption>SQL Lab on the project's Trino connection, one catalog per table format.</figcaption>
</figure>

See the [Superset guide](../../user_guides/projects/superset/superset.md) for building dashboards on feature data, and the [Superset setup](../../setup_installation/admin/superset.md) page for enabling it on a cluster.
