# Azure Machine Learning Notebooks Integration

Connecting to the Feature Store from Azure Machine Learning Notebooks requires setting up a Feature Store API key for Azure Machine Learning Notebooks and installing the **HSFS** on the notebook. This guide explains step by step how to connect to the Feature Store from Azure Machine Learning Notebooks.

!!! info "Network Connectivity"

    To be able to connect to the Feature Store, please ensure that the Network Security Group of your Hopsworks instance on Azure is configured to allow incoming traffic from your compute target on ports 443, 9083 and 9085 (443,9083,9085). See [Network security groups](https://docs.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview) for more information. If your compute target is not in the same VNet as your Hopsworks instance and the Hopsworks instance is not accessible from the internet then you will need to configure [Virtual Network Peering](https://docs.microsoft.com/en-us/azure/virtual-network/virtual-network-manage-peering).

## Generate an API key

For instructions on how to generate an API key follow this [user guide](../projects/api_key/create_api_key.md). For the Azure ML Notebooks integration to work correctly make sure you add the following scopes to your API key:

  1. featurestore
  2. project
  3. job
  4. kafka

## Connect from an Azure Machine Learning Notebook

To access the Feature Store from Azure Machine Learning, open a Python notebook and proceed with the following steps to install HSFS and connect to the Feature Store:

<p align="center">
  <figure>
    <img src="../../../assets/images/guides/integrations/azure/notebooks/step-1.png" alt="Connecting from an Azure Machine Learning Notebook">
    <figcaption>Connecting from an Azure Machine Learning Notebook</figcaption>
  </figure>
</p>

### Install **HSFS**

To be able to access the Hopsworks Feature Store, the `HSFS` Python library needs to be installed. One way of achieving this is by opening a Python notebook in Azure Machine Learning and installing the `HSFS` with a magic command and pip:

```
!pip install hsfs[python]~=[HOPSWORKS_VERSION]
```

!!! attention "Hive Dependencies"

    By default, `HSFS` assumes Spark is used as execution engine and therefore Hive dependencies are not installed. Hence, if you are using a regular Python Kernel **without Spark**, make sure to install the **"python"** extra dependencies (`hsfs[python]`).

!!! attention "Matching Hopsworks version"
    The **major version of `HSFS`** needs to match the **major version of Hopsworks**. Check [PyPI](https://pypi.org/project/hsfs/#history) for available releases.

    <p align="center">
        <figure>
            <img src="../../../assets/images/hopsworks-version.png" alt="HSFS version needs to match the major version of Hopsworks">
            <figcaption>You find the Hopsworks version inside any of your Project's settings tab on Hopsworks</figcaption>
        </figure>
    </p>

### Connect to the Feature Store

You are now ready to connect to the Hopsworks Feature Store from the notebook:

```python
import hsfs

# Put the API key into Key Vault for any production setup:
# See, https://docs.microsoft.com/en-us/azure/machine-learning/how-to-use-secrets-in-runs
#from azureml.core import Experiment, Run
#run = Run.get_context()
#secret_value = run.get_secret(name="fs-api-key")
secret_value = 'MY_API_KEY'

# Create a connection
conn = hsfs.connection(
    host='MY_INSTANCE.cloud.hopsworks.ai', # DNS of your Feature Store instance
    port=443,                              # Port to reach your Hopsworks instance, defaults to 443
    project='MY_PROJECT',                  # Name of your Hopsworks Feature Store project
    api_key_value=secret_value,            # The API key to authenticate with Hopsworks
    hostname_verification=True,            # Disable for self-signed certificates
    engine='python'                        # Choose Python as engine
)

# Get the feature store handle for the project's feature store
fs = conn.get_feature_store()
```

## Next Steps

For more information about how to use the Feature Store, see the [Quickstart Guide](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/quickstart.ipynb){:target="_blank"}.
