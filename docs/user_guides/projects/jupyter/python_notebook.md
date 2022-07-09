# How To Run A Python Notebook

### Introduction

Jupyter is provided as a service in Hopsworks, providing the same user experience and features as if run on your laptop.

* Supports JupyterLab and the classic Jupyter front-end
* Configured with Python3, Spark, PySpark and SparkR kernels


## Step 1: Jupyter dashboard

The image below shows the Jupyter service page in Hopsworks and is accessed by clicking `Jupyter` in the sidebar.

<p align="center">
  <figure>
    <a  href="../../../../assets/images/guides/jupyter/jupyter_overview.png">
      <img src="../../../../assets/images/guides/jupyter/jupyter_overview.png" alt="Jupyter dashboard in Hopsworks">
    </a>
    <figcaption>Jupyter dashboard in Hopsworks</figcaption>
  </figure>
</p>

From this page, you can configure various options and settings to start Jupyter with as described in the sections below.

## Step 2 (Optional): Configure resources

Next step is to configure Jupyter, Click `edit configuration` to get to the configuration page and select `Python`.

* `Container cores`: Number of cores to allocate for the Jupyter instance

* `Container memory`: Number of MBs to allocate for the Jupyter instance

!!! notice "Configured resource pool is shared by all running kernels. If a kernel crashes while executing a cell, try increasing the Container memory."

<p align="center">
  <figure>
    <a  href="../../../../assets/images/guides/jupyter/python_configuration.png">
      <img src="../../../../assets/images/guides/jupyter/python_configuration.png" alt="Resource configuration for the Python kernel">
    </a>
    <figcaption>Resource configuration for the Python kernel</figcaption>
  </figure>
</p>

Click `Save` to save the new configuration.

## Step 3 (Optional): Configure max runtime and root path

Before starting the server there are two additional configurations that can be set next to the `Run Jupyter` button.

The runtime of the Jupyter instance can be configured, this is useful to ensure that idle instances will not be hanging around and keep allocating resources. If a limited runtime is not desirable, this can be disabled by setting `no limit`. 

<p align="center">
  <figure>
    <a  href="../../../../assets/images/guides/jupyter/configure_shutdown.png">
      <img src="../../../../assets/images/guides/jupyter/configure_shutdown.png" alt="Configure maximum runtime">
    </a>
    <figcaption>Configure maximum runtime</figcaption>
  </figure>
</p>

The root path from which to start the Jupyter instance can be configured. By default it starts by setting the `/Jupyter` folder as the root.

<p align="center">
  <figure>
    <a  href="../../../../assets/images/guides/jupyter/start_from_folder.png">
      <img src="../../../../assets/images/guides/jupyter/start_from_folder.png" alt="Configure root folder">
    </a>
    <figcaption>Configure root folder</figcaption>
  </figure>
</p>


## Step 4: Start Jupyter

Start the Jupyter instance by clicking the `Run Jupyter` button.

<p align="center">
  <figure>
    <a  href="../../../../assets/images/guides/jupyter/python_jupyter_starting.gif">
      <img src="../../../../assets/images/guides/jupyter/python_jupyter_starting.gif" alt="Starting Jupyter and running a Python notebook">
    </a>
    <figcaption>Starting Jupyter and running a Python notebook</figcaption>
  </figure>
</p>


## Conclusion

In this guide you learned how to configure and run a Python application in Jupyter. You can now follow this [guide](../python/python_install.md) to install a library that can be used in a notebook.
