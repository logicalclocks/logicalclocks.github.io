# How To Run A PySpark Notebook

### Introduction

Jupyter is provided as a service in Hopsworks, providing the same user experience and features as if run on your laptop.

* Supports JupyterLab and the classic Jupyter front-end
* Configured with Python3, PySpark and Ray kernels


## Step 1: Jupyter dashboard

The image below shows the Jupyter service page in Hopsworks and is accessed by clicking `Jupyter` in the sidebar.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jupyter/jupyter_overview_spark.png" alt="Jupyter dashboard in Hopsworks">
    <figcaption>Jupyter dashboard in Hopsworks</figcaption>
  </figure>
</p>

From this page, you can configure various options and settings to start Jupyter with as described in the sections below.

## Step 2: A Spark environment must be configured

The PySpark kernel will only be available if Jupyter is configured to use the `spark-feature-pipeline` or an environment cloned from it.
You can easily refer to the green ticks as to what kernels are available in which environment.
<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jupyter/select_spark_environment.png" alt="Select an environment with PySpark kernel enabled">
    <figcaption>Select an environment with PySpark kernel enabled</figcaption>
  </figure>
</p>

## Step 3 (Optional): Configure spark properties

Next step is to configure the Ray properties to be used in Jupyter, Click `edit configuration` to get to the 
configuration page and select `Ray`.

### Resource and compute

Resource allocation for the Spark driver and executors can be configured, also the number of executors and whether dynamic execution should be enabled.

* `Driver memory`: Number of cores to allocate for the Spark driver

* `Driver virtual cores`: Number of MBs to allocate for the Spark driver

* `Executor memory`: Number of cores to allocate for each Spark executor

* `Executor virtual cores`: Number of MBs to allocate for each Spark executor

* `Dynamic/Static`: Run the Spark application in static or dynamic allocation mode (see [spark docs](https://spark.apache.org/docs/latest/configuration.html#dynamic-allocation) for details).


<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jupyter/spark_resource_and_compute.png" alt="Resource configuration for the Spark kernels">
    <figcaption>Resource configuration for the Spark kernels</figcaption>
  </figure>
</p>

### Attach files or dependencies

Additional files or dependencies required for the Spark job can be configured.

* `Additional archives`: List of zip or .tgz files that will be locally accessible by the application

* `Additional jars`: List of .jar files to add to the CLASSPATH of the application

* `Additional python dependencies`: List of .py, .zip or .egg files that will be locally accessible by the application

* `Additional files`: List of files that will be locally accessible by the application

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jupyter/spark_additional_files.png" alt="File configuration for the Spark kernels">
    <figcaption>File configuration for the Spark kernels</figcaption>
  </figure>
</p>

Line-separates [properties](https://spark.apache.org/docs/3.1.1/configuration.html) to be set for the Spark application. For example, changing the configuration variables for the Kryo Serializer or setting environment variables for the driver, you can set the properties as shown below.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jupyter/spark_properties.png" alt="File configuration for the Spark kernels">
    <figcaption>Additional Spark configuration</figcaption>
  </figure>
</p>


Click `Save` to save the new configuration.

## Step 4 (Optional): Configure root folder and automatic shutdown

Before starting the server there are two additional configurations that can be set next to the `Run Jupyter` button.

The runtime of the Jupyter instance can be configured, this is useful to ensure that idle instances will not be hanging around and keep allocating resources. If a limited runtime is not desirable, this can be disabled by setting `no limit`.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jupyter/configure_shutdown.png" alt="Configure maximum runtime">
    <figcaption>Configure maximum runtime</figcaption>
  </figure>
</p>

The root path from which to start the Jupyter instance can be configured. By default it starts by setting the `/Jupyter` folder as the root.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jupyter/start_from_folder.png" alt="Configure root folder">
    <figcaption>Configure root folder</figcaption>
  </figure>
</p>


## Step 5: (Kueue enabled) Select a Queue

Currently we do not have Kueue support for Spark. You do not need to select a queue to run the notebook in.

## Step 5: Start Jupyter

Start the Jupyter instance by clicking the `Run Jupyter` button.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jupyter/spark_jupyter_starting.gif" alt="Starting Jupyter and running a Spark notebook">
    <figcaption>Starting Jupyter and running a Spark notebook</figcaption>
  </figure>
</p>

## Step 6: Access Spark UI

Navigate back to Hopsworks and a Spark session will have appeared, click on the `Spark UI` button to go to the Spark UI.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/jupyter/spark_ui.gif" alt="Access Spark UI and see application logs">
    <figcaption>Access Spark UI and see application logs</figcaption>
  </figure>
</p>

## Accessing project data

### Read directly from the filesystem (recommended)

To read a dataset in your project using Spark, use the full filesystem path where the data is stored. For example, to read a CSV file named `data.csv` located in the `Resources` dataset of a project called `my_project`:

```python
df = spark.read.csv("/Projects/my_project/Resources/data.csv", header=True, inferSchema=True)
df.show()
```

### Additional files

Different files can be attached to the jupyter session and made available in the `/srv/hops/artifacts` folder when the PySpark kernel is started. This configuration is mainly useful when you need to add additional configuration such as jars that needs to be added to the CLASSPATH.

When reading data in your Spark application, it is recommended to use the Spark read API as previously demonstrated, since this reads from the filesystem directly, whereas `Additional files` configuration options will download the files in its entirety and is not a scalable option.

## Going Further

You can learn how to [install a library](../python/python_install.md) so that it can be used in a notebook.
