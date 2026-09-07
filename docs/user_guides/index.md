# How-To Guides

Task-focused guides for the Hopsworks UI and APIs, organised by the part of the platform you are working with.
For what things are and why, see the [Concepts](../concepts/index.md).

<!-- markdownlint-disable MD030 -->
<div class="grid cards hops-start" markdown>

-   :material-console:{ .lg .middle } **Start here**

    ---

    Install the client and authenticate once.
    Every guide in this section runs from the same session.

    ```bash
    uv pip install "hopsworks[python]"
    hops setup
    ```

    [Client installation](client_installation/index.md) · [Create a project](projects/project/create_project.md) · [Create a feature group](fs/feature_group/create.md)

</div>
<!-- markdownlint-enable MD030 -->

<div class="hops-task-index" markdown>

<div class="hops-task-group" markdown>
:material-database:{ .hops-role-ico } Feature Store
{ .hops-role-cap }

- [Feature groups](fs/feature_group/index.md)
  Write features from a DataFrame, validate them, keep statistics.
- [Feature views](fs/feature_view/index.md)
  Read training data, batch data and online feature vectors.
- [Data sources](fs/data_source/index.md)
  Connect warehouses, object stores and databases as inputs.
- [Feature monitoring](fs/feature_monitoring/index.md)
  Watch statistics over time and compare them to a reference.
- [Transformations and integrations](fs/transformation_functions.md)
  Model-independent transformations, compute engines, external clients.

</div>

<div class="hops-task-group" markdown>
:material-rocket-launch-outline:{ .hops-role-ico } MLOps
{ .hops-role-cap }

- [Model registry](mlops/registry/index.md)
  Register models with metrics, schema and evaluation artifacts.
- [Model serving](mlops/serving/index.md)
  Deploy a model with a predictor, transformer, logging and autoscaling.
- [Model monitoring](mlops/model_monitoring/index.md)
  Compare inference data against training data on a schedule.
- [Agents](agents/index.md)
  Run agent tasks as jobs or serve interactive agents.

</div>

<div class="hops-task-group" markdown>
:material-folder-outline:{ .hops-role-ico } Projects and compute
{ .hops-role-cap }

- [Projects](projects/index.md)
  Sign in, create a project, manage members, secrets, keys and alerts.
- [Compute](compute/index.md)
  Jupyter, the terminal, jobs, Airflow and Python environments.
- [Analytics](analytics/index.md)
  SQL over the offline store with Trino, dashboards in Superset.

</div>

<div class="hops-task-group" markdown>
:material-wrench-outline:{ .hops-role-ico } Platform
{ .hops-role-cap }

- [Clients](client_installation/index.md)
  Python and Java libraries for your own environment, and the `hops` CLI.
- [Setup and administration](../setup_installation/index.md)
  Install on a cloud or on-prem, manage users and operations.
- [Migration 3.x to 4.0](migration/40_migration.md)
  What changed and how to move.

</div>

</div>
