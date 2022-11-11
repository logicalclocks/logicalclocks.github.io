# Hopsworks Client Installation Guide

## Hopsworks (including Feature Store and MLOps)
The Hopsworks client library is required to connect to the Hopsworks Feature Store and MLOps services from your local machine. Execute the following command to install the full Hopsworks client library on your local machine:

```
pip install hopsworks
```
Supported versions of Python: 3.7, 3.8, 3.9

!!! attention "OSX Installation"

    On OSX system you might need to install librdkafka manually before installing hsfs. You can do so by running the following command:

    ```
    brew install librdkafka
    C_INCLUDE_PATH=$(readlink -f $(brew --prefix librdkafka))/include
    LIBRARY_PATH=$(readlink -f $(brew --prefix librdkafka))/lib
    pip install hopsworks
    ```

!!! attention "Windows/Conda Installation"

    It is recommended to use a conda environment to install the Hopsworks Feature Store client library on Windows. To install the Hopsworks Feature Store client library in a conda environment, execute the following commands:
    
    ```
    conda install twofish
    setx CONDA_DLL_SEARCH_MODIFICATION_ENABLE 1
    pip install hopsworks
    ```

## Feature Store only
To only install the Hopsworks Feature Store client library, execute the following command:

```
pip install hsfs[python]
```
Supported versions of Python: 3.7, 3.8, 3.9

!!! attention "OSX Installation"

    On OSX system you might need to install librdkafka manually before installing hsfs. You can do so by running the following command:

    ```
    brew install librdkafka
    C_INCLUDE_PATH=$(readlink -f $(brew --prefix librdkafka))/include
    LIBRARY_PATH=$(readlink -f $(brew --prefix librdkafka))/lib
    pip install hsfs[python]
    ```

!!! attention "Windows/Conda Installation"

    It is recommended to use a conda environment to install the Hopsworks Feature Store client library on Windows. To install the Hopsworks Feature Store client library in a conda environment, execute the following commands:
    
    ```
    conda install twofish
    setx CONDA_DLL_SEARCH_MODIFICATION_ENABLE 1
    pip install hsfs[python]
    ```

## Other environments

The Hopsworks client libraries can also be installed in other environments, such as Databricks, AWS Sagemaker, or Google Cloud Dataproc. For more information, see [Feature Store Client Integrations](../integrations/index.md).

