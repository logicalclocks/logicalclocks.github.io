# How To Run A PySpark Job

## Introduction

All members of a project in Hopsworks can launch the following types of applications through a project's Jobs service:

- Python (*Hopsworks Enterprise only*)
- Apache Spark

Launching a job of any type is very similar process, what mostly differs between job types is
the various configuration parameters each job type comes with. After following this guide you will be able to create a PySpark job.

The PySpark program can either be a `.py` script or a `.ipynb` file.

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

To configure a  job, click `Advanced options`, which will open up the advanced configuration page for the job.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/create_new_job.png" alt="Create new job dialog">
    <figcaption>Create new job dialog</figcaption>
  </figure>
</p>

### Step 3: Set the script

Next step is to select the program to run. You can either select `From project`, if the file was previously uploaded to Hopsworks, or `Upload new file` which lets you select a file from your local filesystem as demonstrated below.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/upload_job_py_file.gif" alt="Configure program">
    <figcaption>Configure program</figcaption>
  </figure>
</p>

### Step 4: Set the job type

Next step is to set the job type to `SPARK` to indicate it should be executed as a spark job. Then specify [advanced configuration](#step-5-optional-advanced-configuration) or click `Create New Job` to create the job.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/advanced_configuration_pyspark.png" alt="Set the job type">
    <figcaption>Set the job type</figcaption>
  </figure>
</p>

### Step 5 (optional): Advanced configuration

Resource allocation for the Spark driver and executors can be configured, also the number of executors and whether dynamic execution should be enabled.

* `Driver memory`: Number of cores to allocate for the Spark driver

* `Driver virtual cores`: Number of MBs to allocate for the Spark driver

* `Executor memory`: Number of cores to allocate for each Spark executor

* `Executor virtual cores`: Number of MBs to allocate for each Spark executor

* `Dynamic/Static`: Run the Spark application in static or dynamic allocation mode (see [spark docs](https://spark.apache.org/docs/latest/configuration.html#dynamic-allocation) for details).


<p align="center">
  <figure>
    <a  href="../../../../assets/images/guides/jupyter/spark_resource_and_compute.png">
      <img src="../../../../assets/images/guides/jupyter/spark_resource_and_compute.png" alt="Resource configuration for the Spark kernels">
    </a>
    <figcaption>Resource configuration for the Spark kernels</figcaption>
  </figure>
</p>

Additional files or dependencies required for the Spark job can be configured.

* `Additional archives`: Number of cores to allocate for the Spark driver

* `Additional jars`: Number of MBs to allocate for the Spark driver

* `Additional python dependencies`: Number of cores to allocate for each Spark executor

* `Additional files`: Number of MBs to allocate for each Spark executor

<p align="center">
  <figure>
    <a  href="../../../../assets/images/guides/jupyter/spark_additional_files.png">
      <img src="../../../../assets/images/guides/jupyter/spark_additional_files.png" alt="File configuration for the Spark kernels">
    </a>
    <figcaption>File configuration for the Spark kernels</figcaption>
  </figure>
</p>

Line-separates [properties](https://spark.apache.org/docs/3.1.1/configuration.html) to be set for the Spark application. For example, changing the configuration variables for the Kryo Serializer or setting environment variables for the driver, you can set the properties as shown below.

<p align="center">
  <figure>
    <a  href="../../../../assets/images/guides/jupyter/spark_properties.png">
      <img src="../../../../assets/images/guides/jupyter/spark_properties.png" alt="File configuration for the Spark kernels">
    </a>
    <figcaption>Additional Spark configuration</figcaption>
  </figure>
</p>

### Step 6: Execute the job

Now click the `Run` button to start the execution of the job, and then click on `Executions` to see the list of all executions.


<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/start_job_pyspark.gif" alt="Start job execution">
    <figcaption>Start job execution</figcaption>
  </figure>
</p>

### Step 7: Application logs

To monitor logs while the execution is running, click `Spark UI` to open the Spark UI in a separate tab. 

Once the execution is finished, you can click on `Logs` to see the full logs for execution.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/spark_logs.png" alt="Access Spark logs">
    <figcaption>Access Spark logs</figcaption>
  </figure>
</p>

## Code

### Step 1: Upload the python program

This snippet assumes the python script is in the current working directory and named `script.py`. It will upload the python script to run to the `Resources` dataset.

```python

import hopsworks

connection = hopsworks.connection()

project = connection.get_project()

dataset_api = project.get_dataset_api()

uploaded_file_path = dataset_api.upload("script.ipynb", "Resources")

```


### Step 2: Create SPARK job

In this snippet we get the `JobsApi` object to get the default job configuration for a `SPARK` job, set the python script to run and create the `Job` object.

```python

jobs_api = project.get_jobs_api()

spark_config = jobs_api.get_configuration("SPARK")

spark_config['appPath'] = uploaded_file_path

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

### API Reference

[Jobs](https://docs.hopsworks.ai/hopsworks-api/dev/generated/api/jobs/)

[Executions](https://docs.hopsworks.ai/hopsworks-api/dev/generated/api/executions/)

## Conclusion

In this guide you learned how to create and run a PySpark job.