# How To Run A Python Notebook

## Introduction

Jupyter is provided as a service in Hopsworks, providing the same user experience and features as if run on your laptop.

- Supports JupyterLab and the classic Jupyter front-end
- Configured with Python3, PySpark and Ray kernels

## Step 1: Jupyter dashboard

The image below shows the Jupyter service page in Hopsworks and is accessed by clicking `Jupyter` in the sidebar.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jupyter/jupyter_overview_py.png" alt="Jupyter dashboard in Hopsworks">
    <figcaption>Jupyter dashboard in Hopsworks</figcaption>
  </figure>
</p>

From this page, you can configure various options and settings to start Jupyter with as described in the sections below.

## Step 2 (Optional): Configure resources

Next step is to configure Jupyter, Click `edit configuration` to get to the configuration page and select `Python`.

- `Container cores`: Number of cores to allocate for the Jupyter instance

- `Container memory`: Number of MBs to allocate for the Jupyter instance

!!! notice "Configured resource pool is shared by all running kernels. If a kernel crashes while executing a cell, try increasing the Container memory."

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jupyter/python_configuration.png" alt="Resource configuration for the Python kernel">
    <figcaption>Resource configuration for the Python kernel</figcaption>
  </figure>
</p>

Click `Save` to save the new configuration.

## Step 3 (Optional): Configure environment, root folder and automatic shutdown

Before starting the server there are three additional configurations that can be set next to the `Run Jupyter` button.

The environment that Jupyter should run in needs to be configured.
Select the environment that contains the necessary dependencies for your code.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jupyter/configure_environment.png" alt="Configure environment">
    <figcaption>Configure environment</figcaption>
  </figure>
</p>

The runtime of the Jupyter instance can be configured, this is useful to ensure that idle instances will not be hanging around and keep allocating resources.
If a limited runtime is not desirable, this can be disabled by setting `no limit`.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jupyter/configure_shutdown.png" alt="Configure maximum runtime">
    <figcaption>Configure maximum runtime</figcaption>
  </figure>
</p>

The root path from which to start the Jupyter instance can be configured.
By default it starts by setting the `/Jupyter` folder as the root.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jupyter/start_from_folder.png" alt="Configure root folder">
    <figcaption>Configure root folder</figcaption>
  </figure>
</p>

## Step 4: (Kueue enabled) Select a Queue

If the cluster is installed with Kueue enabled, you will need to select a queue in which the notebook should run.
This can be done from `Advance configuration -> Scheduler section`.

![Default queue for job](../../../assets/images/guides/project/scheduler/job_queue.png)

## Step 5: Start Jupyter

Start the Jupyter instance by clicking the `Run Jupyter` button.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jupyter/python_jupyter_starting.gif" alt="Starting Jupyter and running a Python notebook">
    <figcaption>Starting Jupyter and running a Python notebook</figcaption>
  </figure>
</p>

## Accessing project data

!!! notice "Recommended approach if `/hopsfs` is mounted"
    If your Hopsworks installation is configured to mount the project datasets under `/hopsfs`, which it is in most cases, then please refer to this section.
    If the file system is not mounted, then project files can be localized using the [download api](https://docs.hopsworks.ai/hopsworks-api/{{{hopsworks_version}}}/generated/api/datasets/#download) to localize files in the current working directory.

### Absolute paths

The project datasets are mounted under `/hopsfs`, so you can access `data.csv` from the `Resources` dataset using `/hopsfs/Resources/data.csv` in your notebook.

### Relative paths

The notebook's working directory is the folder it is located in.
For example, if it is located in the `Resources` dataset, and you have a file named `data.csv` in that dataset, you simply access it using `data.csv`.
Also, if you write a local file, for example `output.txt`, it will be saved in the `Resources` dataset.

## Going Further

You can learn how to [install a library](../python/python_install.md) so that it can be used in a notebook.
