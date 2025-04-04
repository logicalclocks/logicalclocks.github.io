# Azure Machine Learning Designer Integration

Connecting to Hopsworks from the Azure Machine Learning Designer requires setting up a Hopsworks API key for the Designer and installing the **Hopsworks** Python library on the Designer. This guide explains step by step how to connect to the Feature Store from Azure Machine Learning Designer.

!!! info "Network Connectivity"

    To be able to connect to the Feature Store, please ensure that the Network Security Group of your Hopsworks instance on Azure is configured to allow incoming traffic from your compute target on ports 443, 9083 and 9085 (443,9083,9085). See [Network security groups](https://docs.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview) for more information. If your compute target is not in the same VNet as your Hopsworks instance and the Hopsworks instance is not accessible from the internet then you will need to configure [Virtual Network Peering](https://docs.microsoft.com/en-us/azure/virtual-network/virtual-network-manage-peering).

## Generate an API key

For instructions on how to generate an API key follow this [user guide](../projects/api_key/create_api_key.md). For the Azure ML Designer integration to work correctly make sure you add the following scopes to your API key:

  1. featurestore
  2. project
  3. job
  4. kafka

## Connect to Hopsworks 

To connect to Hopsworks from the Azure Machine Learning Designer, create a new pipeline or open an existing one:

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/integrations/azure/designer/step-1.png" alt="Add an Execute Python Script step">
    <figcaption>Add an Execute Python Script step</figcaption>
  </figure>
</p>

In the pipeline, add a new `Execute Python Script` step and replace the Python script from the next step:

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/integrations/azure/designer/step-2.png" alt="Add the code to access the Hopsworks">
    <figcaption>Add the code to access the Hopsworks</figcaption>
  </figure>
</p>

!!! info "Updating the script"

    Replace MY_VERSION, MY_API_KEY, MY_INSTANCE, MY_PROJECT and MY_FEATURE_GROUP with the respective values. The major version set for MY_VERSION needs to match the major version of Hopsworks. Check [PyPI](https://pypi.org/project/hopsworks/#history) for available releases.

    <p align="center">
    <figure>
        <img src="../../../assets/images/hopsworks-version.png" alt="Hopsworks version needs to match the major version of Hopsworks">
        <figcaption>You find the Hopsworks version inside any of your Project's settings tab on Hopsworks</figcaption>
    </figure>
    </p>

```python
import os
import importlib.util


package_name = 'hopsworks'
version = 'MY_VERSION'
spec = importlib.util.find_spec(package_name)
if spec is None:
    import os
    os.system(f"pip install %s[python]==%s" % (package_name, version))

# Put the API key into Key Vault for any production setup:
# See, https://docs.microsoft.com/en-us/azure/machine-learning/how-to-use-secrets-in-runs
#from azureml.core import Experiment, Run
#run = Run.get_context()
#secret_value = run.get_secret(name="fs-api-key")
secret_value = 'MY_API_KEY'

def azureml_main(dataframe1 = None, dataframe2 = None):

    import hopsworks
    project = hopsworks.login(
        host='MY_INSTANCE.cloud.hopsworks.ai', # DNS of your Hopsworks instance
        port=443,                              # Port to reach your Hopsworks instance, defaults to 443
        project='MY_PROJECT',                  # Name of your Hopsworks project
        api_key_value=secret_value,            # The API key to authenticate with Hopsworks
        hostname_verification=True,            # Disable for self-signed certificates
        engine='python'                        # Choose python as engine
    )
    fs = project.get_feature_store()              # Get the project's default feature store

    return fs.get_feature_group('MY_FEATURE_GROUP', version=1).read(),
```

Select a compute target and save the step. The step is now ready to use:

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/integrations/azure/designer/step-3.png" alt="Select a compute target">
    <figcaption>Select a compute target</figcaption>
  </figure>
</p>

As a next step, you have to connect the previously created `Execute Python Script` step with the next step in the pipeline. For instance, to export the features to a CSV file, create a `Export Data` step:

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/integrations/azure/designer/step-4.png" alt="Add an Export Data step">
    <figcaption>Add an Export Data step</figcaption>
  </figure>
</p>

Configure the `Export Data` step to write to you data store of choice:

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/integrations/azure/designer/step-5.png" alt="Configure the Export Data step">
    <figcaption>Configure the Export Data step</figcaption>
  </figure>
</p>

Connect the to steps by drawing a line between them:

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/integrations/azure/designer/step-6.png" alt="Connect the steps">
    <figcaption>Connect the steps</figcaption>
  </figure>
</p>

Finally, submit the pipeline and wait for it to finish:

!!! info "Performance on the first execution"

    The `Execute Python Script` step can be slow when being executed for the first time as the Hopsworks library needs to be installed on the compute target. Subsequent executions on the same compute target should use the already installed library.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/integrations/azure/designer/step-7.png" alt="Execute the pipeline">
    <figcaption>Execute the pipeline</figcaption>
  </figure>
</p>

## Next Steps

For more information on how to use the Hopsworks API check out the other guides or the [Login API](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/api/login/). 