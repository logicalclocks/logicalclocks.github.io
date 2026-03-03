# Azure Machine Learning Notebooks Integration

Connecting to the Hopsworks from Azure Machine Learning Notebooks requires setting up a Hopsworks API key for Azure Machine Learning Notebooks and installing the **Hopsworks** Python library on the notebook.
This guide explains step by step how to connect to the Hopsworks from Azure Machine Learning Notebooks.

!!! info "Network Connectivity"

    To be able to connect to the Feature Store, please ensure that the Network Security Group of your Hopsworks instance on Azure is configured to allow incoming traffic from your compute target on ports 443, 9083 and 9085 (443,9083,9085).
    See [Network security groups](https://docs.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview) for more information.
    If your compute target is not in the same VNet as your Hopsworks instance and the Hopsworks instance is not accessible from the internet then you will need to configure [Virtual Network Peering](https://docs.microsoft.com/en-us/azure/virtual-network/virtual-network-manage-peering).

## Install Hopsworks Python Library

To be able to interact with Hopsworks from a Python environment you need to install the `Hopsworks` Python library.
The library is available on [PyPi](https://pypi.org/project/hopsworks/) and can be installed using `pip`:

```sh
pip install hopsworks[python]~=[HOPSWORKS_VERSION]
```

!!! attention "Python Profile"

    By default, `pip install hopsworks` does not install all the necessary dependencies required to use the Hopsworks library from a local Python environment.
    To ensure that all the dependencies are installed, you should install the library using with the Python profile `pip install hopsworks[python]`.

!!! attention "Matching Hopsworks version"

    We recommend that the major and minor version of the Python library match the major and minor version of the Hopsworks deployment.

    <p align="center">
        <figure>
            <img src="../../../../assets/images/hopsworks-version.png" alt="The library version needs to match the major version of Hopsworks">
            <figcaption>You find the Hopsworks version inside any of your Project's settings tab on Hopsworks</figcaption>
        </figure>
    </p>

## Generate an API key

For instructions on how to generate an API key follow this [user guide](../projects/api_key/create_api_key.md).
For the Azure ML Notebooks integration to work correctly make sure you add the following scopes to your API key:

  1. featurestore
  2. project
  3. job
  4. kafka

## Connect from an Azure Machine Learning Notebook

To access Hopsworks from Azure Machine Learning, open a Python notebook and proceed with the following steps to install Hopsworks and connect to the Feature Store:

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/integrations/azure/notebooks/step-1.png" alt="Connecting from an Azure Machine Learning Notebook">
    <figcaption>Connecting from an Azure Machine Learning Notebook</figcaption>
  </figure>
</p>

### Connect to Hopsworks

You are now ready to connect to Hopsworks Feature Store from the notebook:

```python
import hopsworks

# Put the API key into Key Vault for any production setup:
# See, https://docs.microsoft.com/en-us/azure/machine-learning/how-to-use-secrets-in-runs
# from azureml.core import Experiment, Run
# run = Run.get_context()
# secret_value = run.get_secret(name="fs-api-key")
secret_value = "MY_API_KEY"

# Create a connection
project = hopsworks.login(
    host="MY_INSTANCE.cloud.hopsworks.ai",  # DNS of your Hopsworks instance
    port=443,  # Port to reach your Hopsworks instance, defaults to 443
    project="MY_PROJECT",  # Name of your Hopsworks project
    api_key_value=secret_value,  # The API key to authenticate with Hopsworks
    hostname_verification=True,  # Disable for self-signed certificates
    engine="python",  # Choose Python as engine
)

# Get the feature store handle for the project's feature store
fs = project.get_feature_store()
```

## Next Steps

For more information on how to use the Hopsworks API check out the other guides or the [Login API][hopsworks.login].
