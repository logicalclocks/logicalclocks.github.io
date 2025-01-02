---
description: Documentation on how to connect to Hopsworks from a Python environment (e.g. from Sagemaker, Google Colab, Kubeflow or local environment)
---

# Python Environments (Local, AWS SageMaker, Google Colab or Kubeflow)

This guide explains step by step how to connect to Hopsworks from any Python environment such as your local environment, AWS SageMaker, Google Colab or Kubeflow.

## Install Python Library

To be able to interact with Hopsworks from a Python environment you need to install the `Hopsworks` Python library. The library is available on [PyPi](https://pypi.org/project/hopsworks/) and can be installed using `pip`: 

```
pip install hopsworks[python]~=[HOPSWORKS_VERSION]
```

!!! attention "Python Profile"

    By default, `pip install hopsworks`, does not install all the necessary dependencies required to use the Hopsworks library from a pure Python environment. To ensure that all the dependencies are installed, you should install the library using with the Python profile `pip install hopsworks[python]`.

!!! attention "Matching Hopsworks version"

    We recommend that the major and minor version of the Python library match the major and minor version of the Hopsworks deployment.

    <p align="center">
        <figure>
            <img src="../../../../assets/images/hopsworks-version.png" alt="The library version needs to match the major version of Hopsworks">
            <figcaption>You find the Hopsworks version inside any of your Project's settings tab on Hopsworks</figcaption>
        </figure>
    </p>

## Generate an API key

For instructions on how to generate an API key follow this [user guide](../projects/api_key/create_api_key.md). For the Python client to work correctly make sure you add the following scopes to your API key:

  1. featurestore
  2. project
  3. job
  4. kafka

## Connect to the Feature Store

You are now ready to connect to Hopsworks from your Python environment:

```python
import hopsworks 
project = hopsworks.login(
    host='my_instance',                 # DNS of your Hopsworks instance
    port=443,                           # Port to reach your Hopsworks instance, defaults to 443
    project='my_project',               # Name of your Hopsworks project
    api_key_value='apikey',             # The API key to authenticate with Hopsworks
    engine='python',                    # Use the Python engine
)
fs = project.get_feature_store()        # Get the project's default feature store
```

!!! note "Engine"

    `Hopsworks` leverage several engines depending on whether you are running using Apache Spark or Pandas/Polars. The default behaviour of the library is to use the `spark` engine if you do not specify any `engine` option in the `login` method and if the `PySpark` library is available in the environment.

    Please refer to the [Spark integration guide](spark.md) to configure your PySpark cluster to interact with Hopsworks.

## Next Steps

For more information on how to use the Hopsworks API check out the other guides or the [API Reference](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/api/connection_api/). 
