---
description: Documentation on how to configure and execute a Jupyter Notebook job on Hopsworks.
---

# How To Run A Jupyter Notebook Job

## Introduction

All members of a project in Hopsworks can launch the following types of applications through a project's Jobs service:

- Python
- Apache Spark

Launching a job of any type is very similar process, what mostly differs between job types is
the various configuration parameters each job type comes with. After following this guide you will be able to create a Jupyter Notebook job.

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

By default, the dialog will create a Spark job. To instead configure a Jupyter Notebook job, select `PYTHON`.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/jobs_select_python.gif" alt="Select Python job type">
    <figcaption>Select Python job type</figcaption>
  </figure>
</p>

### Step 4: Set the notebook

Next step is to select the Jupyter Notebook to run. You can either select `From project`, if the file was previously uploaded to Hopsworks, or `Upload new file` which lets you select a file from your local filesystem as demonstrated below. By default, the job name is the same as the file name, but you can customize it as shown. 

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/upload_job_notebook_file.gif" alt="Configure program">
    <figcaption>Configure program</figcaption>
  </figure>
</p>

Then click `Create job` to create the job.

### Step 5 (optional): Set the Jupyter Notebook arguments

In the job settings, you can specify arguments for your notebook script.
Arguments must be in the format of `-p arg1 value1 -p arg2 value2`. For each argument, you must first provide `-p`, followed by the parameter name (e.g. `arg1`), followed by its value (e.g. `value1`).
The next step is to read the arguments in the notebook which is explained in this [guide](https://papermill.readthedocs.io/en/latest/usage-parameterize.html).

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/job_notebook_args.png" alt="Configure notebook arguments">
    <figcaption>Configure notebook arguments</figcaption>
  </figure>
</p>

### Step 6 (optional): Additional configuration

It is possible to also set following configuration settings for a `PYTHON` job.

* `Environment`: The python environment to use
* `Container memory`: The amount of memory in MB to be allocated to the Jupyter Notebook script
* `Container cores`: The number of cores to be allocated for the Jupyter Notebook script
* `Additional files`: List of files that will be locally accessible by the application
You can always modify the arguments in the job settings.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/configure_py.png" alt="Set the job type">
    <figcaption>Set the job type</figcaption>
  </figure>
</p>

### Step 7: Execute the job

Now click the `Run` button to start the execution of the job. You will be redirected to the `Executions` page where you can see the list of all executions.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/start_job_notebook.gif" alt="Start job execution">
    <figcaption>Start job execution</figcaption>
  </figure>
</p>

### Step 8: Visualize output notebook
Once the execution is finished, click `Logs` and then `notebook out` to see the logs for the execution.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jobs/job_view_out_notebook.gif" alt="Visualize output notebook">
    <figcaption>Visualize output notebook</figcaption>
  </figure>
</p>

You can directly edit and save the output notebook by clicking `Open Notebook`.

## Code

### Step 1: Upload the Jupyter Notebook script

This snippet assumes the Jupyter Notebook script is in the current working directory and named `notebook.ipynb`. 

It will upload the Jupyter Notebook script to the `Resources` dataset in your project.

```python

import hopsworks

project = hopsworks.login()

dataset_api = project.get_dataset_api()

uploaded_file_path = dataset_api.upload("notebook.ipynb", "Resources")

```


### Step 2: Create Jupyter Notebook job

In this snippet we get the `JobsApi` object to get the default job configuration for a `PYTHON` job, set the Jupyter Notebook script to run and create the `Job` object.

```python

jobs_api = project.get_jobs_api()

notebook_job_config = jobs_api.get_configuration("PYTHON")

notebook_job_config['appPath'] = uploaded_file_path

job = jobs_api.create_job("notebook_job", notebook_job_config)

```

### Step 3: Execute the job

In this code snippet, we execute the job with arguments and wait until it reaches a terminal state.

```python

# Run the job
execution = job.run(args='-p a 2 -p b 5', await_termination=True)
```

### API Reference

[Jobs](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/api/jobs/)

[Executions](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/api/executions/)

## Conclusion

In this guide you learned how to create and run a Jupyter Notebook job.