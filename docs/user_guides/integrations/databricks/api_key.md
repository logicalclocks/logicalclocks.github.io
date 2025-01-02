# Hopsworks API key

In order for the Databricks cluster to be able to communicate with Hopsworks, clients running on Databricks need to be able to access a Hopsworks API key.

## Generate an API key

For instructions on how to generate an API key follow this [user guide](../../projects/api_key/create_api_key.md). For the Databricks integration to work make sure you add the following scopes to your API key:

  1. featurestore
  2. project
  3. job
  4. kafka

## Quickstart API key Argument

!!! hint "API key as Argument"
    To get started quickly, without saving the Hopsworks API in a secret storage, you can simply supply it as an argument when instantiating a connection:


```python hl_lines="6"
    import hopsworks 
    project = hopsworks.login(
        host='my_instance',                 # DNS of your Feature Store instance
        port=443,                           # Port to reach your Hopsworks instance, defaults to 443
        project='my_project',               # Name of your Hopsworks Feature Store project
        api_key_value='apikey',             # The API key to authenticate with Hopsworks
        hostname_verification=True          # Disable for self-signed certificates
    )
    fs = project.get_feature_store()           # Get the project's default feature store
```

## Next Steps

Continue with the [configuration guide](configuration.md) to finalize the configuration of the Databricks Cluster to communicate with the Hopsworks Feature Store.
