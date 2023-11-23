---
description: Documentation on how to install the Hopsworks and HSFS Python libraries, including the specific requirements for Mac OSX and Windows.
---
# Client Installation Guide

## Hopsworks (including Feature Store and MLOps)
The Hopsworks client library is required to connect to the Hopsworks Feature Store and MLOps services from your local machine or any other Python environment such as Google Colab or AWS Sagemaker. Execute the following command to install the full Hopsworks client library in your Python environment:

!!! note "Virtual environment"
    It is recommended to use a virtual python environment instead of the system environment used by your operating system, in order to avoid any side effects regarding interfering dependencies.

```
pip install hopsworks
```
Supported versions of Python: 3.8, 3.9, 3.10, 3.11, 3.12 ([PyPI ↗](https://pypi.org/project/hopsworks/))

!!! attention "OSX Installation"

    On OSX systems you might need to install librdkafka manually before installing hopsworks. You can verify if you have installed it previously using `brew info librdkafka`. Hopsworks requires `librdkafka` version to be lower than 2.0.0. If it is not installed yet, you can do so using `brew install`, however, you always need to set the `C_INCLUDE_PATH` and `LIBRARY_PATH`.

    If not installed yet, install librdkafka:
    ```
    curl -O https://raw.githubusercontent.com/Homebrew/homebrew-core/f7d0f40bbc4075177ecf16812fd95951a723a996/Formula/librdkafka.rb
    brew install --build-from-source librdkafka.rb
    ```
    If it is already installed, set the environment variables and proceed with installing the hopsworks client library:
    ```
    export C_INCLUDE_PATH=$(brew --prefix)/include
    export LIBRARY_PATH=$(brew --prefix)/lib
    pip install hopsworks
    ```

!!! attention "Windows/Conda Installation"

    On Windows systems you might need to install twofish manually before installing hopsworks, if you don't have the Microsoft Visual C++ Build Tools installed. In that case, it is recommended to use a conda environment and run the following commands:
    
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
Supported versions of Python: 3.8, 3.9, 3.10, 3.11, 3.12 ([PyPI ↗](https://pypi.org/project/hsfs/))

!!! attention "OSX Installation"

    On OSX systems you might need to install librdkafka manually before installing hopsworks. You can verify if you have installed it previously using `brew info librdkafka`. Hopsworks requires `librdkafka` version to be lower than 2.0.0. If it is not installed yet, you can do so using `brew install`, however, you always need to set the `C_INCLUDE_PATH` and `LIBRARY_PATH`.

    If not installed yet, install librdkafka:
    ```
    curl -O https://raw.githubusercontent.com/Homebrew/homebrew-core/f7d0f40bbc4075177ecf16812fd95951a723a996/Formula/librdkafka.rb
    brew install --build-from-source librdkafka.rb
    ```
    If it is already installed, set the environment variables and proceed with installing the hopsworks client library:
    ```
    export C_INCLUDE_PATH=$(brew --prefix)/include
    export LIBRARY_PATH=$(brew --prefix)/lib
    pip install hsfs[python]
    ```

!!! attention "Windows/Conda Installation"

    On Windows systems you might need to install twofish manually before installing hsfs, if you don't have the Microsoft Visual C++ Build Tools installed. In that case, it is recommended to use a conda environment and run the following commands:
    
    ```
    conda install twofish
    setx CONDA_DLL_SEARCH_MODIFICATION_ENABLE 1
    pip install hsfs[python]
    ```

## Next Steps

If you are using a local python environment and want to connect to the Hopsworks Feature Store, you can follow the [Python Guide](../integrations/python.md#generate-an-api-key) section to create an API Key and to get started.

## Other environments

The Hopsworks Feature Store client libraries can also be installed in external environments, such as Databricks, AWS Sagemaker, or Azure Machine Learning. For more information, see [Client Integrations](../integrations/index.md).

