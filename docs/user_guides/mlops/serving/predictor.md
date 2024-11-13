# How To Configure A Predictor

## Introduction

In this guide, you will learn how to configure a predictor for a trained model.

!!! warning
    This guide assumes that a model has already been trained and saved into the Model Registry. To learn how to create a model in the Model Registry, see [Model Registry Guide](../registry/frameworks/tf.md)

Predictors are the main component of deployments. They are responsible for running a model server that loads a trained model, handles inference requests and returns predictions. They can be configured to use different model servers, serving tools, log specific inference data or scale differently. In each predictor, you can configure the following components:

!!! info ""
    1. [Model server](#model-server)
    2. [Serving tool](#serving-tool)
    3. [User-provided script](#user-provided-script)
    4. [Python environments](#python-environments)
    5. [Transformer](#transformer)
    6. [Inference Logger](#inference-logger)
    7. [Inference Batcher](#inference-batcher)
    8. [Resources](#resources)
    9. [API protocol](#api-protocol)

## GUI

### Step 1: Create new deployment

If you have at least one model already trained and saved in the Model Registry, navigate to the deployments page by clicking on the `Deployments` tab on the navigation menu on the left.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployments_tab_sidebar.png" alt="Deployments navigation tab">
    <figcaption>Deployments navigation tab</figcaption>
  </figure>
</p>

Once in the deployments page, you can create a new deployment by either clicking on `New deployment` (if there are no existing deployments) or on `Create new deployment` it the top-right corner. Both options will open the deployment creation form.

### Step 2: Choose a backend

A simplified creation form will appear, including the most common deployment fields from all available configurations. The first step is to choose a ==backend== for your model deployment. The backend will filter the models shown below according to the framework that the model was registered with in the model registry.

For example if you registered the model as a TensorFlow model using `ModelRegistry.tensorflow.create_model(...)` you select `Tensorflow Serving` in the dropdown.

<p align="center">
  <figure>
    <img style="max-width: 55%; margin: 0 auto" src="../../../../assets/images/guides/mlops/serving/deployment_simple_form_1.png" alt="Select the model framework">
    <figcaption>Select the backend</figcaption>
  </figure>
</p>

All models compatible with the selected backend will be listed in the model dropdown.

<p align="center">
  <figure>
    <img style="max-width: 55%; margin: 0 auto" src="../../../../assets/images/guides/mlops/serving/deployment_simple_form_2.png" alt="Select the model">
    <figcaption>Select the model</figcaption>
  </figure>
</p>

Moreover, you can optionally select a predictor script (see [Step 3](#step-3-optional-select-a-predictor-script)), enable KServe (see [Step 4](#step-4-optional-enable-kserve)) or change other advanced configuration (see [Step 5](#step-5-optional-other-advanced-options)). Otherwise, click on `Create new deployment` to create the deployment for your model.

### Step 3 (Optional): Select a predictor script

For python models, if you want to use your own [predictor script](#step-2-optional-implement-predictor-script) click on `From project` and navigate through the file system to find it, or click on `Upload new file` to upload a predictor script now.

<p align="center">
  <figure>
    <img style="max-width: 55%; margin: 0 auto" src="../../../../assets/images/guides/mlops/serving/deployment_simple_form_py_pred.png" alt="Predictor script in the simplified deployment form">
    <figcaption>Select a predictor script in the simplified deployment form</figcaption>
  </figure>
</p>

### Step 4 (Optional): Change predictor environment

If you are using a predictor script it is also required to configure the inference environment for the predictor. This environment needs to have all the necessary dependencies installed to run your predictor script.

By default, we provide a set of environments like `tensorflow-inference-pipeline`, `torch-inference-pipeline` and `pandas-inference-pipeline` that serves this purpose for common machine learning frameworks.

To create your own it is recommended to [clone](../../projects/python/python_env_clone.md) the `minimal-inference-pipeline` and install additional dependencies for your use-case.

<p align="center">
  <figure>
    <img style="max-width: 55%; margin: 0 auto" src="../../../../assets/images/guides/mlops/serving/deployment_simple_form_py_pred_env.png" alt="Predictor script in the simplified deployment form">
    <figcaption>Select an environment for the predictor script</figcaption>
  </figure>
</p>

### Step 5 (Optional): Enable KServe

Other configuration such as the serving tool, is part of the advanced options of a deployment. To navigate to the advanced creation form, click on `Advanced options`.

<p align="center">
  <figure>
    <img style="max-width: 55%; margin: 0 auto" src="../../../../assets/images/guides/mlops/serving/deployment_simple_form_adv_options.png" alt="Advance options">
    <figcaption>Advanced options. Go to advanced deployment creation form</figcaption>
  </figure>
</p>

Here, you change the [serving tool](#serving-tool) for your deployment by enabling or disabling the KServe checkbox.

<p align="center">
  <figure>
    <img style="max-width: 85%; margin: 0 auto" src="../../../../assets/images/guides/mlops/serving/deployment_adv_form_kserve.png" alt="KServe in advanced deployment form">
    <figcaption>KServe checkbox in the advanced deployment form</figcaption>
  </figure>
</p>

### Step 6 (Optional): Other advanced options

Additionally, you can adjust the default values of the rest of components:

!!! info "Predictor components"
    1. [Transformer](#transformer)
    2. [Inference logger](#inference-logger)
    3. [Inference batcher](#inference-batcher)
    4. [Resources](#resources)
    5. [API protocol](#api-protocol)

Once you are done with the changes, click on `Create new deployment` at the bottom of the page to create the deployment for your model.

## Code

### Step 1: Connect to Hopsworks

=== "Python"
  ```python
  import hopsworks

  project = hopsworks.login()

  # get Hopsworks Model Registry handle
  mr = project.get_model_registry()

  # get Hopsworks Model Serving handle
  ms = project.get_model_serving()
  ```

### Step 2 (Optional): Implement a predictor script

=== "Predictor"
    ``` python
    class Predictor():

        def __init__(self):
            """ Initialization code goes here"""
            pass

        def predict(self, inputs):
            """ Serve predictions using the trained model"""
            pass
    ```
=== "Generate (vLLM deployments only)"
    ``` python
    from typing import Iterable, AsyncIterator, Union

    from vllm import LLM

    from kserve.protocol.rest.openai import (
        CompletionRequest,
        ChatPrompt,
        ChatCompletionRequestMessage,
    )
    from kserve.protocol.rest.openai.types import Completion

    class Predictor():

        def __init__(self):
            """ Initialization code goes here"""
        # initialize vLLM backend
        self.llm = LLM(os.environ["MODEL_FILES_PATH])

        # initialize tokenizer if needed
        # self.tokenizer = ...

        def apply_chat_template(
            self,
            messages: Iterable[ChatCompletionRequestMessage,],
        ) -> ChatPrompt:
          pass

        async def create_completion(
            self, request: CompletionRequest
        ) -> Union[Completion, AsyncIterator[Completion]]:
        """Generate responses using the LLM"""

        # Completion: used for returning a single answer (batch)
        # AsyncIterator[Completion]: used for returning a stream of answers

        pass
    ```

!!! info "Jupyter magic"
    In a jupyter notebook, you can add `%%writefile my_predictor.py` at the top of the cell to save it as a local file.

### Step 3 (Optional): Upload the script to your project

!!! info "You can also use the UI to upload your predictor script. See [above](#step-3-advanced-deployment-form)"

=== "Python"
  ```python
  uploaded_file_path = dataset_api.upload("my_predictor.py", "Resources", overwrite=True)
  predictor_script_path = os.path.join("/Projects", project.name, uploaded_file_path)
  ```

### Step 4: Define predictor

=== "Python"
  ```python
  my_model = mr.get_model("my_model", version=1)

  my_predictor = ms.create_predictor(my_model,
                                    # optional
                                    model_server="PYTHON",
                                    serving_tool="KSERVE",
                                    script_file=predictor_script_path
                                    )
  ```

### Step 5: Create a deployment with the predictor

=== "Python"
  ```python
  my_deployment = my_predictor.deploy()

  # or
  my_deployment = ms.create_deployment(my_predictor)
  my_deployment.save()
  ```

### API Reference

[Predictor](https://docs.hopsworks.ai/hopsworks-api/{{{ hopsworks_version }}}/generated/model-serving/predictor_api/)

## Model Server

Hopsworks Model Serving supports deploying models with a Flask server for python-based models, TensorFlow Serving for TensorFlow / Keras models and vLLM for Large Language Models (LLMs). Today, you can deploy PyTorch models as python-based models.

??? info "Show supported model servers"

    | Model Server       | Supported | ML Models and Frameworks                                                                        |
    | ------------------ | --------- | ----------------------------------------------------------------------------------------------- |
    | Flask              | ✅         | python-based (scikit-learn, xgboost, pytorch...)                                                |
    | TensorFlow Serving | ✅         | keras, tensorflow                                                                               |
    | TorchServe         | ❌         | pytorch                                                                                         |
    | vLLM               | ✅         | vLLM-supported models (see [list](https://docs.vllm.ai/en/latest/models/supported_models.html)) |

## Serving tool

In Hopsworks, model servers are deployed on Kubernetes. There are two options for deploying models on Kubernetes: using [KServe](https://kserve.github.io/website/latest/) inference services or Kubernetes built-in deployments. ==KServe is the recommended way to deploy models in Hopsworks==.

The following is a comparative table showing the features supported by each of them.

??? info "Show serving tools comparison"

    | Feature / requirement                                 | Kubernetes (enterprise) | KServe (enterprise)       |
    | ----------------------------------------------------- | ----------------------- | ------------------------- |
    | Autoscaling (scale-out)                               | ✅                       | ✅                         |
    | Resource allocation                                   | ➖ min. resources        | ✅ min / max. resources    |
    | Inference logging                                     | ➖ simple                | ✅ fine-grained            |
    | Inference batching                                    | ➖ partially             | ✅                         |
    | Scale-to-zero                                         | ❌                       | ✅ after 30s of inactivity |
    | Transformers                                          | ❌                       | ✅                         |
    | Low-latency predictions                               | ❌                       | ✅                         |
    | Multiple models                                       | ❌                       | ➖ (python-based)          |
    | User-provided predictor required <br /> (python-only) | ✅                       | ❌                         |

## User-provided script

Depending on the model server and serving platform used in the model deployment, you can (or need) to provide your own python script to load the model and make predictions.
This script is referred to as **predictor script**, and is included in the [artifact files](../serving/deployment.md#artifact-files) of the model deployment.

The predictor script needs to implement a given template depending on the model server of the model deployment. See the templates in [Step 2](#step-2-optional-implement-a-predictor-script).

??? info "Show supported user-provided predictors"

    | Serving tool | Model server       | User-provided predictor script                       |
    | ------------ | ------------------ | ---------------------------------------------------- |
    | Kubernetes   | Flask server       | ✅ (required)                                         |
    |              | TensorFlow Serving | ❌                                                    |
    | KServe       | Fast API           | ✅ (only required for artifacts with multiple models) |
    |              | TensorFlow Serving | ❌                                                    |
    |              | vLLM               | ✅ (required)                                         |

### Environment variables

A number of different environment variables is available in the predictor to ease its implementation.

??? info "Show environment variables"

    | Name                | Description                                                          |
    | ------------------- | -------------------------------------------------------------------- |
    | MODEL_FILES_PATH    | Local path to the model files                                        |
    | ARTIFACT_FILES_PATH | Local path to the artifact files                                     |
    | DEPLOYMENT_NAME     | Name of the current deployment                                       |
    | MODEL_NAME          | Name of the model being served by the current deployment             |
    | MODEL_VERSION       | Version of the model being served by the current deployment          |
    | ARTIFACT_VERSION    | Version of the model artifact being served by the current deployment |

## Python environments

Depending on the model server and serving tool used in the model deployment, you can select the Python environment where the predictor and transformer scripts will run. To create a new Python environment see [Python Environments](../../projects/python/python_env_overview.md).

??? info "Show supported Python environments"

    | Serving tool | Model server       | Editable | Predictor                           | Transformer                    |
    | ------------ | ------------------ | -------- | ----------------------------------- | ------------------------------ |
    | Kubernetes   | Flask server       | ❌        | `pandas-inference-pipeline` only    | ❌                              |
    |              | TensorFlow Serving | ❌        | (official) tensorflow serving image | ❌                              |
    | KServe       | Fast API           | ✅        | any `inference-pipeline` image      | any `inference-pipeline` image |
    |              | TensorFlow Serving | ✅        | (official) tensorflow serving image | any `inference-pipeline` image |
    |              | vLLM               | ✅        | `vllm-inference-pipeline` only      | any `inference-pipeline` image |

!!! note 
    The selected Python environment is used for both predictor and transformer. Support for selecting a different Python environment for the predictor and transformer is coming soon.

## Transformer

Transformers are used to apply transformations on the model inputs before sending them to the predictor for making predictions using the model. To learn more about transformers, see the [Transformer Guide](transformer.md).

!!! note
    Transformers are only supported in KServe deployments.

## Inference logger

Inference loggers are deployment components that log inference requests into a Kafka topic for later analysis. To learn about the different logging modes, see the [Inference Logger Guide](inference-logger.md)

## Inference batcher

Inference batcher are deployment component that apply batching to the incoming inference requests for a better throughput-latency trade-off. To learn about the different configuration available for the inference batcher, see the [Inference Batcher Guide](inference-batcher.md).

## Resources

Resources include the number of replicas for the deployment as well as the resources (i.e., memory, CPU, GPU) to be allocated per replica. To learn about the different combinations available, see the [Resources Guide](resources.md).

## API protocol

Hopsworks supports both REST and gRPC as the API protocols to send inference requests to model deployments. In general, you use gRPC when you need lower latency inference requests. To learn more about the REST and gRPC API protocols for model deployments, see the [API Protocol Guide](api-protocol.md).
