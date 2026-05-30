---
description: Documentation on how to orchestrate Hopsworks jobs using Apache Airflow
---

# Orchestrate Jobs using Apache Airflow

## Introduction

Hopsworks jobs can be orchestrated using [Apache Airflow](https://airflow.apache.org/).
You can define an Airflow DAG (Directed Acyclic Graph) containing the dependencies between Hopsworks jobs.
You can then schedule the DAG to be executed at a specific schedule using a [cron](https://en.wikipedia.org/wiki/Cron) expression.

Airflow DAGs are defined as Python files.
Within the Python file, different operators can be used to trigger different actions.
Hopsworks provides operators to execute jobs on Hopsworks and sensors to wait for a specific job to finish or for a HopsFS path to appear.

Hopsworks ships **Airflow 3.0.6**.
The DAG-authoring API differs significantly from Airflow 1.x; see [the Airflow 3 upgrade page](airflow3_upgrade.md) for a porting checklist.

### Use Apache Airflow in Hopsworks

Hopsworks deployments include a deployment of Apache Airflow.
You can access it from the Hopsworks UI by clicking on the _Airflow_ button on the left menu.

Authorization is per Hopsworks project:
admins on Hopsworks (`HOPS_ADMIN`) have access to all DAGs;
regular users see only DAGs of the projects they are a member of (DAGs, runs, logs, triggers, edits — all surfaces).
The Audit Log is row-filtered for non-admins to events for DAGs in their projects.
See the [security model](security_model.md) for the full surface-by-surface contract.

The Hopsworks UI's Airflow page shows each DAG's most recent runs as colored squares in a **Last runs** column (green = success, red = failed, blue = running, yellow = queued / scheduled, gray = other).
Clicking anywhere on a DAG row opens the DAG in the Airflow UI.
The pencil at the row's end opens the generated Python file in an in-app editor.
The trash icon deletes the DAG: a click-confirm dialog appears, and on confirm the Python file is removed from the project's `Airflow/` HopsFS dataset, the per-DAG `hopsworks_api_key_<sha256(dag_id)[:16]>` Variable is deleted from Airflow, the row in `dag_project_index` is dropped, and `airflow.api.common.delete_dag.delete_dag` is called so the `dag`, `dag_run`, `task_instance`, `xcom`, `log`, and related rows go with it.
After delete the page reloads to reflect the new state.

#### Hopsworks DAG Builder

<figure>
  <img src="../../../../assets/images/guides/airflow/airflow_dag_builder.png" alt="Airflow DAG Builder"/>
  <figcaption>Airflow DAG Builder</figcaption>
</figure>

You can create a new Airflow DAG to orchestrate jobs using the Hopsworks DAG builder tool.
Click on _New Workflow_ to create a new Airflow DAG.
You should provide a name for the DAG as well as a schedule interval.
You can define the schedule using the dropdown menus or by providing a cron expression.

The schedule `@continuous` is rejected by both the UI form and the backend.
A continuous DAG re-runs as soon as the previous run finishes, so a DAG that errors at parse time (for example, missing the per-DAG API key Variable) loops at wall-clock speed and OOM-kills the shared scheduler pod, taking every other project's DAGs down with it.
Use a cron expression for periodic runs, or `@once` for one-shot DAGs.

You can add to the DAG Hopsworks operators and sensors:

- **Operator**: The operator is used to trigger a job execution.
When configuring the operator you select the job you want to execute and you can optionally provide execution arguments.
You can decide whether or not the operator should wait for the execution to be completed.
If you select the _wait_ option, the operator will block and Airflow will not execute any parallel task.
If you select the _wait_ option the Airflow task fails if the job fails.
If you want to execute tasks in parallel, you should not select the _wait_ option but instead use the sensor.
When configuring the operator, you can can also provide which other Airflow tasks it depends on.
If you add a dependency, the task will be executed only after the upstream tasks have been executed successfully.

- **Sensor**: The sensor can be used to wait for executions to be completed.
Similarly to the _wait_ option of the operator, the sensor blocks until the job execution is completed.
The sensor can be used to launch several jobs in parallel and wait for their execution to be completed.
Please note that the sensor is defined at the job level rather than the execution level.
The sensor will wait for the most recent execution to be completed and it will fail the Airflow task if the execution was not successful.

You can then create the DAG and Hopsworks will generate the Python file.

#### Write your own DAG

If you prefer to code the DAGs or you want to edit a DAG built with the builder tool, you can do so.
The Airflow DAGs are stored in the _Airflow_ dataset which you can access using the file browser in the project settings.

The Hopsworks operators and sensors are shipped in the `apache-airflow-providers-hopsworks` provider package that is preinstalled on Hopsworks-managed Airflow.
Import them from the standard provider namespace:

```python
from hopsworks.airflow.operators import HopsworksLaunchOperator  # noqa: F401
from hopsworks.airflow.sensors import (  # noqa: F401
    HopsworksHdfsSensor,
    HopsworksJobSuccessSensor,
)
```

Launch a Hopsworks job:

```python
from hopsworks.airflow.operators import HopsworksLaunchOperator


HopsworksLaunchOperator(
    task_id="profiles_fg_0",
    project_id=42,
    job_name="profiles_fg",
    args="",
    wait_for_completion=True,
)
```

Provide the Airflow task name (`task_id`) and the Hopsworks job information (`project_id`, `job_name`, `args`).
Set `wait_for_completion=True` to block until the job execution finishes.

Wait for a job's most recent execution to be successful:

```python
from hopsworks.airflow.sensors import HopsworksJobSuccessSensor


HopsworksJobSuccessSensor(
    task_id="wait_for_profiles_fg",
    project_id=42,
    job_name="profiles_fg",
)
```

Wait for a HopsFS path to exist (replaces the Airflow 1.x `HopsworksHdfsSensor` plugin):

```python
from hopsworks.airflow.sensors import HopsworksHdfsSensor


HopsworksHdfsSensor(
    task_id="wait_for_arrival",
    project_id=42,
    path="Resources/landing/2026-05-22/_SUCCESS",
)
```

`project_id` can be replaced with `project_name=` if you prefer name-based lookup.

!!! note "Authorization is automatic"
    Airflow 3 on Hopsworks does not use Airflow's `access_control` parameter.
    DAG visibility is enforced from the dag_id-to-project mapping that Hopsworks writes when the DAG is composed (see the [security model](security_model.md)); editing the DAG file cannot change ownership.
    Hopsworks admins (`HOPS_ADMIN`) have full access to every DAG; project members access DAGs of their own projects.

#### Manage Airflow DAGs using Git

You can leverage the [Git integration](../git/clone_repo.md) to track your Airflow DAGs in a git repository.
Airflow will only consider the DAG files which are stored in the _Airflow_ Dataset in Hopsworks.
After cloning the git repository in Hopsworks, you can automate the process of copying the DAG file in the _Airflow_ Dataset using [`DatasetApi.copy`][hopsworks_common.core.dataset_api.DatasetApi.copy] of the Hopsworks API.
