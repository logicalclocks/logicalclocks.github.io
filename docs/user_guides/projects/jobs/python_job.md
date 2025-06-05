---
description: Documentation on how to configure and execute a Python job on Hopsworks.
---

# How To Run A Python Job

## Introduction

All members of a project in Hopsworks can launch the following types of applications through a project's Jobs service:

- Python
- Apache Spark

Launching a job of any type is very similar process, what mostly differs between job types is
the various configuration parameters each job type comes with. Hopsworks support scheduling jobs to run on a regular basis,
e.g backfilling a Feature Group by running your feature engineering pipeline nightly. Scheduling can be done both through the UI and the python API,
checkout [our Scheduling guide](schedule_job.md).

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

By default, the dialog will create a Spark job. To instead configure a Python job, select `PYTHON`.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/jobs_select_python.gif" alt="Select Python job type">
    <figcaption>Select Python job type</figcaption>
  </figure>
</p>

### Step 4: Set the script

Next step is to select the python script to run. You can either select `From project`, if the file was previously uploaded to Hopsworks, or `Upload new file` which lets you select a file from your local filesystem as demonstrated below. By default, the job name is the same as the file name, but you can customize it as shown. 

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/upload_job_py_file.gif" alt="Configure program">
    <figcaption>Configure program</figcaption>
  </figure>
</p>

### Step 5 (optional): Set the Python script arguments

In the job settings, you can specify arguments for your Python script.
Remember to handle the arguments inside your Python script.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/job_notebook_args.png" alt="Configure Python script arguments">
    <figcaption>Configure Python script arguments</figcaption>
  </figure>
</p>

### Step 6 (optional): Additional configuration

It is possible to also set following configuration settings for a `PYTHON` job.

* `Environment`: The python environment to use
* `Container memory`: The amount of memory in MB to be allocated to the Python script
* `Container cores`: The number of cores to be allocated for the Python script
* `Additional files`: List of files that will be locally accessible in the working directory of the application. Only recommended to use if project datasets are not mounted under `/hopsfs`.
  You can always modify the arguments in the job settings.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/configure_py.png" alt="Additional configuration">
    <figcaption>Additional configuration</figcaption>
  </figure>
</p>

### Step 7: Execute the job

Now click the `Run` button to start the execution of the job. You will be redirected to the `Executions` page where you can see the list of all executions.

Once the execution is finished, click on `Logs` to see the logs for the execution.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/start_job_py.gif" alt="Start job execution">
    <figcaption>Start job execution</figcaption>
  </figure>
</p>

## Code

### Step 1: Upload the Python script

This snippet assumes the python script is in the current working directory and named `script.py`. 

It will upload the python script to the `Resources` dataset in your project.

```python

import hopsworks

project = hopsworks.login()

dataset_api = project.get_dataset_api()

uploaded_file_path = dataset_api.upload("script.py", "Resources")

```

### Step 2: Create Python job

In this snippet we get the `JobsApi` object to get the default job configuration for a `PYTHON` job, set the python script and override the environment to run in, and finally create the `Job` object.

```python

jobs_api = project.get_job_api()

py_job_config = jobs_api.get_configuration("PYTHON")

# Set the application file
py_job_config['appPath'] = uploaded_file_path

# Override the python job environment
py_job_config['environmentName'] = "python-feature-pipeline"

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

## Configuration
The following table describes the JSON payload returned by `jobs_api.get_configuration("PYTHON")`

| Field                   | Type           | Description                                     | Default                 |
|-------------------------|----------------|-------------------------------------------------|--------------------------|
| `type`                  | string         | Type of the job configuration                   | `"pythonJobConfiguration"` |
| `appPath`               | string         | Project path to script (e.g `Resources/foo.py`) | `null`            |
| `environmentName`       | string         | Name of the project python environment          | `"pandas-training-pipeline"` |
| `resourceConfig.cores`  | number (float) | Number of CPU cores to be allocated             | `1.0`                    |
| `resourceConfig.memory` | number (int)   | Number of MBs to be allocated                   | `2048`                   |
| `resourceConfig.gpus`   | number (int)   | Number of GPUs to be allocated                  | `0`                      |
| `logRedirection`        | boolean        | Whether logs are redirected                     | `true`                   |
| `jobType`               | string         | Type of job                                     | `"PYTHON"`               |


## Accessing project data
!!! notice "Recommended approach if `/hopsfs` is mounted"
    If your Hopsworks installation is configured to mount the project datasets under `/hopsfs`, which it is in most cases, then please refer to this section instead of the `Additional files` property to reference file resources.

### Absolute paths
The project datasets are mounted under `/hopsfs`, so you can access `data.csv` from the `Resources` dataset using `/hopsfs/Resources/data.csv` in your script.

### Relative paths
The script's working directory is the folder it is located in. For example, if it is located in the `Resources` dataset, and you have a file named `data.csv` in that dataset, you simply access it using `data.csv`. Also, if you write a local file, for example `output.txt`, it will be saved in the `Resources` dataset.


## API Reference

[Jobs](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/api/jobs/)

[Executions](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/api/executions/)
