---
description: Documentation on how to configure and execute a PySpark job on Hopsworks.
---

# How To Run A PySpark Job

## Introduction

This guide will describe how to configure a job to execute a pyspark script inside the cluster.

All members of a project in Hopsworks can launch the following types of applications through a project's Jobs service:

- Python
- Apache Spark
- Ray

Launching a job of any type is very similar process, what mostly differs between job types is
the various configuration parameters each job type comes with.
Hopsworks clusters support scheduling to run jobs on a regular basis,
e.g backfilling a Feature Group by running your feature engineering pipeline nightly.
Scheduling can be done both through the UI and the python API,
checkout [our Scheduling guide](schedule_job.md).

PySpark program can either be a `.py` script or a `.ipynb` file, however be mindful of how to access/create
the spark session based on the extension you provide.

!!! notice "Instantiate the SparkSession"
    For a `.py` file, remember to instantiate the SparkSession i.e `spark=SparkSession.builder.getOrCreate()`

    For a `.ipynb` file, the `SparkSession` is already available as `spark` when the job is started.

## UI

### Step 1: Jobs overview

The image below shows the Jobs overview page in Hopsworks and is accessed by clicking `Jobs` in the sidebar.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/jobs_overview.png" alt="Jobs overview">
    <figcaption>Jobs overview</figcaption>
  </figure>
</p>

### Step 2: Create new job dialog

Click `New Job` and the following dialog will appear.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/create_new_job.png" alt="Create new job dialog">
    <figcaption>Create new job dialog</figcaption>
  </figure>
</p>

### Step 3: Set the job type

By default, the dialog will create a Spark job.
Make sure `SPARK` is chosen.

### Step 4: Set the script

Next step is to select the program to run.
You can either select `From project`, if the file was previously uploaded to Hopsworks, or `Upload new file` which lets you select a file from your local filesystem as demonstrated below.
By default, the job name is the same as the file name, but you can customize it as shown.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/upload_job_pyspark_file.gif" alt="Configure program">
    <figcaption>Configure program</figcaption>
  </figure>
</p>

Then click `Create job` to create the job.

### Step 5 (optional): Set the PySpark script arguments

In the job settings, you can specify arguments for your PySpark script.
Remember to handle the arguments inside your PySpark script.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/job_py_args.png" alt="Configure PySpark script arguments">
    <figcaption>Configure PySpark script arguments</figcaption>
  </figure>
</p>

### Step 6 (optional): Advanced configuration

Resource allocation for the Spark driver and executors can be configured, also the number of executors and whether dynamic execution should be enabled.

- `Environment`: The python environment to use, must be based on `spark-feature-pipeline`

- `Driver memory`: Number of cores to allocate for the Spark driver

- `Driver virtual cores`: Number of MBs to allocate for the Spark driver

- `Executor memory`: Number of cores to allocate for each Spark executor

- `Executor virtual cores`: Number of MBs to allocate for each Spark executor

- `Dynamic/Static`: Run the Spark application in static or dynamic allocation mode (see [spark docs](https://spark.apache.org/docs/latest/configuration.html#dynamic-allocation) for details).

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/spark_resource_and_compute.png" alt="Resource configuration for the PySpark job">
    <figcaption>Resource configuration for the PySpark job</figcaption>
  </figure>
</p>

Additional files or dependencies required for the Spark job can be configured.

- `Additional archives`: List of archives to be extracted into the working directory of each executor.

- `Additional jars`: List of jars to be placed in the working directory of each executor.

- `Additional python dependencies`: List of python files and archives to be placed on each executor and added to PATH.

- `Additional files`: List of files to be placed in the working directory of each executor.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jupyter/spark_additional_files.png" alt="File configuration for the PySpark job">
    <figcaption>File configuration for the PySpark job</figcaption>
  </figure>
</p>

Line-separates [properties](https://spark.apache.org/docs/3.1.1/configuration.html) to be set for the Spark application.
For example, changing the configuration variables for the Kryo Serializer or setting environment variables for the driver, you can set the properties as shown below.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jupyter/spark_properties.png" alt="Additional Spark configuration">
    <figcaption>Additional Spark configuration</figcaption>
  </figure>
</p>

### Step 7: (Kueue enabled) Select a Queue

Currently we do not have Kueue support for Spark.
You do not need to select a queue to run the job in.

### Step 8: Execute the job

Now click the `Run` button to start the execution of the job.
You will be redirected to the `Executions` page where you can see the list of all executions.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/start_job_pyspark.gif" alt="Start job execution">
    <figcaption>Start job execution</figcaption>
  </figure>
</p>

### Step 9: Application logs

To monitor logs while the execution is running, click `Spark UI` to open the Spark UI in a separate tab.

Once the execution is finished, you can click on `Logs` to see the full logs for execution.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/spark_logs.png" alt="Access Spark logs">
    <figcaption>Access Spark logs</figcaption>
  </figure>
</p>

## Code

### Step 1: Upload the PySpark program

This snippet assumes the program to run is in the current working directory and named `script.py`.

It will upload the python script to the `Resources` dataset in your project.

```python

import hopsworks

project = hopsworks.login()

dataset_api = project.get_dataset_api()

uploaded_file_path = dataset_api.upload("script.py", "Resources")

```

### Step 2: Create PySpark job

In this snippet we get the `JobsApi` object to get the default job configuration for a `PYSPARK` job, set the pyspark script and override the environment to run in, and finally create the `Job` object.

```python

jobs_api = project.get_job_api()

spark_config = jobs_api.get_configuration("PYSPARK")

# Set the application file
spark_config['appPath'] = uploaded_file_path

# Override the python job environment
spark_config['environmentName'] = "spark-feature-pipeline"

job = jobs_api.create_job("pyspark_job", spark_config)

```

### Step 3: Execute the job

In this snippet we execute the job synchronously, that is wait until it reaches a terminal state, and then download and print the logs.

```python

execution = job.run(await_termination=True)

out, err = execution.download_logs()

f_out = open(out, "r")
print(f_out.read())

f_err = open(err, "r")
print(f_err.read())

```

## Configuration

The following table describes the job configuration parameters for a PYSPARK job.

`conf = jobs_api.get_configuration("PYSPARK")`

| Field                                              | Type    | Description                                                                                                                                                        | Default                    |
|----------------------------------------------------|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------|
| <nobr>`conf['type']`</nobr>                        | string  | Type of the job configuration                                                                                                                                      | `"sparkJobConfiguration"`  |
| <nobr>`conf['appPath']`</nobr>                     | string  | Project path to spark program (e.g `Resources/foo.py`)                                                                                                             | `null`                     |
| <nobr>`conf['defaultArgs']`</nobr>                 | string  | Arguments to pass to the program. Will be overridden if arguments are passed explicitly via `Job.run(args="...")`                                                  | `null`                     |
| <nobr>`conf['environmentName']`</nobr>             | string  | Name of the project spark environment to use                                                                                                                       | `"spark-feature-pipeline"` |
| <nobr>`conf['spark.driver.cores']`</nobr>          | float   | Number of CPU cores allocated for the driver                                                                                                                       | `1.0`                      |
| <nobr>`conf['spark.driver.memory']`</nobr>         | int     | Memory allocated for the driver (in MB)                                                                                                                            | `2048`                     |
| <nobr>`conf['spark.executor.instances']`</nobr>    | int     | Number of executor instances                                                                                                                                       | `1`                        |
| <nobr>`conf['spark.executor.cores']`</nobr>        | float   | Number of CPU cores per executor                                                                                                                                   | `1.0`                      |
| <nobr>`conf['spark.executor.memory']`</nobr>       | int     | Memory allocated per executor (in MB)                                                                                                                              | `4096`                     |
| <nobr>`conf['spark.dynamicAllocation.enabled']`</nobr>          | boolean | Enable dynamic allocation of executors                                                                                                                             | `true`                     |
| <nobr>`conf['spark.dynamicAllocation.minExecutors']`</nobr>     | int     | Minimum number of executors with dynamic allocation                                                                                                                | `1`                        |
| <nobr>`conf['spark.dynamicAllocation.maxExecutors']`</nobr>     | int     | Maximum number of executors with dynamic allocation                                                                                                                | `2`                        |
| <nobr>`conf['spark.dynamicAllocation.initialExecutors']`</nobr> | int     | Initial number of executors with dynamic allocation                                                                                                                | `1`                        |
| <nobr>`conf['spark.blacklist.enabled']`</nobr>     | boolean | Whether executor/node blacklisting is enabled                                                                                                                      | `false`                    |
| <nobr>`conf['files']`</nobr>                       | string  | Comma-separated string of HDFS path(s) to files to be made available to the application. Example: `hdfs:///Project/<project_name>/Resources/file1.py,...`          | `null`                     |
| <nobr>`conf['pyFiles']`</nobr>                     | string  | Comma-separated string of HDFS path(s) to python modules to be made available to the application. Example: `hdfs:///Project/<project_name>/Resources/file1.py,...` | `null`                     |
| <nobr>`conf['jars']`</nobr>                        | string  | Comma-separated string of HDFS path(s) to jars to be included in CLASSPATH. Example: `hdfs:///Project/<project_name>/Resources/app.jar,...`                        | `null`                     |
| <nobr>`conf['archives']`</nobr>                   | string  | Comma-separated string of HDFS path(s) to archives to be made available to the application. Example: `hdfs:///Project/<project_name>/Resources/archive.zip,...`    | `null`                     |

## Accessing project data

### Read directly from the filesystem (recommended)

To read a dataset in your project using Spark, use the full filesystem path where the data is stored.
For example, to read a CSV file named `data.csv` located in the `Resources` dataset of a project called `my_project`:

```python
df = spark.read.csv("/Projects/my_project/Resources/data.csv", header=True, inferSchema=True)
df.show()
```

### Additional files

Different file types can be attached to the spark job and made available in the `/srv/hops/artifacts` folder when the PySpark job is started.
This configuration is mainly useful when you need to add additional setup, such as jars that needs to be added to the CLASSPATH.

When reading data in your Spark job it is recommended to use the Spark read API as previously demonstrated, since this reads from the filesystem directly, whereas `Additional files` configuration options will download the files in its entirety and is not a scalable option.

## API Reference

[Jobs](https://docs.hopsworks.ai/hopsworks-api/{{{hopsworks_version}}}/generated/api/jobs/)

[Executions](https://docs.hopsworks.ai/hopsworks-api/{{{hopsworks_version}}}/generated/api/executions/)
