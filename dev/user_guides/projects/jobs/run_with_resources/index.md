# How To Run a Job with Different Resources

## Introduction

A job has one compute configuration: the cores, memory and GPUs every execution gets.
Some runs need more than the others, such as a backfill over a year of data or a retry after an out-of-memory kill.
For those you can give a single execution resources of its own when you start it.

The job itself is not changed.
You give only the fields you want to change, every other field keeps the job's value, and the next plain run uses the job's configuration again.
Each execution records what it was given, so you can see later which runs had different resources.

!!! note "Not available for Python Apps"
    A Python App is a long-running deployment, not a run of a job.
    Change its resources in the app's own configuration.

## UI

On the job, open the menu next to the `Run` button and choose `Run with different arguments or resources`.
In the `Run job` dialog, tick `Run with different resources`.

The dialog then shows the resource fields of the job, filled in with the job's current values.
Change the ones this run needs and click `Run`.
Only the fields you changed are sent; a field you leave as it is follows the job, also if the job is edited before the execution starts.

The details of an execution show what it was given under `Resources of this run`.
The field is absent for an execution that ran with the job's resources.

## Python API

Pass `resources` to `job.run()` with the fields to change, under the names they have in the job configuration (see `job.config`):

```python
import hopsworks


project = hopsworks.login()
job = project.get_job_api().get_job("my_job")

# This run gets 16 GB and a GPU; the cores, and everything else, stay the job's
execution = job.run(resources={"resourceConfig": {"memory": 16384, "gpus": 1}})

# What the run was given; None for a run with the job's resources
print(execution.resources)
```

A Spark job uses the names of its own configuration:

```python
spark_job = project.get_job_api().get_job("my_spark_job")
execution = spark_job.run(
    resources={
        "spark.executor.memory": 16384,
        "spark.dynamicAllocation.maxExecutors": 8,
    }
)
```

A Spark job uses dynamic allocation unless you turned it off, and the number of executors then follows `spark.dynamicAllocation.minExecutors` and `spark.dynamicAllocation.maxExecutors`.
`spark.executor.instances` sets the number of executors of a job with static executors, and has no effect while dynamic allocation is on.

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-class"></code> [`Job`][hopsworks_common.job.Job]
        - <code class="doc-symbol doc-symbol-method"></code> [`run`][hopsworks_common.job.Job.run]
    - <code class="doc-symbol doc-symbol-class"></code> [`Execution`][hopsworks_common.execution.Execution]
        - <code class="doc-symbol doc-symbol-attribute"></code> [`resources`][hopsworks_common.execution.Execution.resources]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>

## CLI

`hops job run` takes the same fields as JSON:

```bash
hops job run my_job --resources '{"resourceConfig": {"memory": 16384}}'
```

## Airflow

In a DAG you [write yourself][write-your-own-dag], `HopsworksLaunchOperator` takes the fields in `job_resources`:

```python
from hopsworks.airflow.operators import HopsworksLaunchOperator


HopsworksLaunchOperator(
    task_id="backfill_profiles_fg",
    project_id=42,
    job_name="profiles_fg",
    job_resources={"resourceConfig": {"memory": 16384}},
)
```

The operator starts the execution and returns; to wait for it, add a `HopsworksJobSuccessSensor` after it, as in [Write your own DAG][write-your-own-dag].

!!! warning "`job_resources`, not `resources`"
    Airflow keeps the operator argument `resources` for the resources of the Airflow task itself.
    A value passed there does not reach the Hopsworks job.

`job_resources` is a templated field, so its values can come from the DAG run, for example from `params`.

## Fields

Memory is in MB, as in the job configuration.

| Job type | Fields |
| --- | --- |
| Python, Jupyter Notebook, ingestion and agent jobs | `resourceConfig`: `cores`, `memory`, `gpus`, `shmSize`, `diskGb` |
| | `hopsfsMountConfig`: `memory`, `cores`, `namenodeConnections` |
| Docker | `resourceConfig`: `cores`, `memory`, `gpus`, `shmSize`, `diskGb` |
| Spark and PySpark | `spark.driver.cores`, `spark.driver.memory`, `spark.driver.memoryOverheadFactor`, `driverDiskGb` |
| | `spark.executor.cores`, `spark.executor.memory`, `spark.executor.memoryOverheadFactor`, `executorDiskGb`, `spark.executor.instances` |
| | `spark.dynamicAllocation.enabled`, `spark.dynamicAllocation.minExecutors`, `spark.dynamicAllocation.maxExecutors`, `spark.dynamicAllocation.initialExecutors` |
| Ray | `driverCores`, `driverMemory`, `driverGpus`, `driverDiskGb` |
| | `workerCores`, `workerMemory`, `workerGpus`, `workerDiskGb`, `workerMinInstances`, `workerMaxInstances` |
| | `hopsfsMountConfig`: `memory`, `cores`, `namenodeConnections` |

A field that is not in the list for the job's type, or a value that is not valid for the field, is refused when the execution is started, and nothing runs.

A Docker job does not mount HopsFS, so it takes no `hopsfsMountConfig`.

!!! note "Ingestion jobs with several tables"
    A table that has resources of its own keeps them.
    The resources given for the execution replace only those of the job.

!!! note "Ingestion jobs on a cluster without the HopsFS CSI driver"
    On such a cluster the HopsFS mount runs inside the ingestion container and has no memory or cores of its own.
    Of `hopsfsMountConfig` only `namenodeConnections` is accepted; give the mount more memory or cores through `resourceConfig`.

!!! note "Spark jobs on a cluster with Kueue"
    Dynamic allocation is off for Spark jobs that run under Kueue.
    Resources given for an execution cannot turn it back on.
