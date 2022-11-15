# Client Installation Guide

## Hopsworks (including Feature Store and MLOps)
The Hopsworks client library is required to connect to the Hopsworks Feature Store and MLOps services from your local machine or any other Python environment such as Google Colab or AWS Sagemaker. Execute the following command to install the full Hopsworks client library in your Python environment:

!!! note "Virtual environment"
    It is recommended to use a virtual python environment instead of the system environment used by your operating system, in order to avoid any side effects regarding interfering dependencies.

```
pip install hopsworks
```
Supported versions of Python: 3.7, 3.8, 3.9

!!! attention "OSX Installation"

    On OSX systems you might need to install librdkafka manually before installing hopsworks. You can do so by running the following commands:

    ```
    brew install librdkafka
    C_INCLUDE_PATH=$(readlink -f $(brew --prefix librdkafka))/include
    LIBRARY_PATH=$(readlink -f $(brew --prefix librdkafka))/lib
    pip install hopsworks
    ```

!!! attention "Windows/Conda Installation"

    On Windows systems you might need to install twofish manually before installing hopsworks. It is recommended to use a conda environment and run the following commands:
    
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

    On OSX systems you might need to install librdkafka manually before installing hsfs. You can do so by running the following commands:

    ```
    brew install librdkafka
    C_INCLUDE_PATH=$(readlink -f $(brew --prefix librdkafka))/include
    LIBRARY_PATH=$(readlink -f $(brew --prefix librdkafka))/lib
    pip install hsfs[python]
    ```

!!! attention "Windows/Conda Installation"

    On Windows systems you might need to install twofish manually before installing hsfs. It is recommended to use a conda environment and run the following commands:
    
    ```
    conda install twofish
    setx CONDA_DLL_SEARCH_MODIFICATION_ENABLE 1
    pip install hsfs[python]
    ```

## Next Steps

If you are using local python environment and want to connect to the Hopsworks Feature Store, you can follow the [Python Guide](../integrations/python.md#generate-an-api-key) section.

## Other environments

The Hopsworks Feature Store client libraries can also be installed in external environments, such as Databricks, AWS Sagemaker, or Azure Machine Learning. For more information, see [Client Integrations](../integrations/index.md).

