# How To Run A Python Job

## Introduction

All members of a project in Hopsworks can launch the following types of applications through a project's Jobs service:

- Python (*Hopsworks Enterprise only*)
- Apache Spark

Launching a job of any type is very similar process, what mostly differs between job types is
the various configuration parameters each job type comes with. After following this guide you will be able to create a Python job.

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

By default, the dialog will create a Spark job. To instead configure a Python job, click `Advanced options`, which will open up the advanced configuration page for the job.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/create_new_job.png" alt="Create new job dialog">
    <figcaption>Create new job dialog</figcaption>
  </figure>
</p>

### Step 3: Set the script

Next step is to select the python script to run. You can either select `From project`, if the file was previously uploaded to Hopsworks, or `Upload new file` which lets you select a file from your local filesystem as demonstrated below.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/upload_job_py_file.gif" alt="Configure program">
    <figcaption>Configure program</figcaption>
  </figure>
</p>

### Step 4: Set the job type

Next step is to set the job type to `PYTHON` to indicate it should be executed as a simple python script. Then click `Create New Job` to create the job. 

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/advanced_configuration_py.gif" alt="Set the job type">
    <figcaption>Set the job type</figcaption>
  </figure>
</p>

### Step 5 (optional): Additional configuration

It is possible to also set following configuration settings for a `PYTHON` job.

* `Container memory`: The amount of memory in MB to be allocated to the Python script
* `Container cores`: The number of cores to be allocated for the Python script
* `Additional files`: List of files that will be locally accessible by the application

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/configure_py.png" alt="Set the job type">
    <figcaption>Set the job type</figcaption>
  </figure>
</p>

### Step 6: Execute the job

Now click the `Run` button to start the execution of the job, and then click on `Executions` to see the list of all executions.

Once the execution is finished, click on `Logs` to see the logs for the execution.


<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/start_job_py.gif" alt="Start job execution">
    <figcaption>Start job execution</figcaption>
  </figure>
</p>

## Code

### Step 1: Upload the python script

This snippet assumes the python script is in the current working directory and named `script.py`. It will upload the python script to run to the `Resources` dataset.

```python

import hopsworks

connection = hopsworks.connection()

project = connection.get_project()

dataset_api = project.get_dataset_api()

uploaded_file_path = dataset_api.upload("script.py", "Resources")

```


### Step 2: Create PYTHON job

In this snippet we get the `JobsApi` object to get the default job configuration for a `PYTHON` job, set the python script to run and create the `Job` object.

```python

jobs_api = project.get_jobs_api()

py_job_config = jobs_api.get_configuration("PYTHON")

py_job_config['appPath'] = uploaded_file_path

job = jobs_api.create_job("py_job", py_job_config)

```

### Step 3: Execute the job

In this snippet we execute the job synchronously, that is wait until it reaches a terminal state, and then download and print the logs.

```python

# Run the job
execution = job.run(await_termination=True)

# Download logs
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

In this guide you learned how to create and run a job.