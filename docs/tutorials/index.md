---
hide:
  - navigation
---

# Tutorials

We are happy to welcome you to our collection of tutorials dedicated to exploring the fundamentals of Hopsworks and Machine Learning development. In addition to offering different types of use cases and common subjects in the field, it facilitates navigation and use of models in a production environment using Hopsworks Feature Store.

## How to run the tutorials

In order to run the tutorials, you will need a Hopsworks account. To do so, go to [app.hopsworks.ai](https://app.hopsworks.ai) and create one. With a managed account, just run the Jupyter notebook from within Hopsworks.
Generally the notebooks contain the information you will need on how to interact with the Hopsworks Platform.

The easiest way to get started is by using [Google Colab](https://colab.research.google.com/) to run the notebooks. However, you can also run them in your local Python environment with Jupyter.
You can find the raw notebook files in our [tutorials repository](https://github.com/logicalclocks/hopsworks-tutorials).

## Fraud Tutorial

This is a quick-start of the Hopsworks Feature Store; using a fraud use case we will load data into the feature store, create two feature groups from which we will make a training dataset and train a model.

### Batch
This is a batch use case variant of the fraud tutorial, it will give you a high level view on how to use our python APIs and the UI to navigate the feature groups.

| Notebooks   |                                      |
| ----------- | ------------------------------------ |
| 1. How to load, engineer and create feature groups | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/fraud_batch/1_feature_groups.ipynb){:target="_blank"}        |
| 2. How to create training datasets                 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/fraud_batch/2_feature_view_creation.ipynb){:target="_blank"} |
| 3. How to train a model from the feature store     | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/fraud_batch/3_model_training.ipynb){:target="_blank"}        |

### Online
This is a online use case variant of the fraud tutorial, it is similar to the batch use case, however, in this tutorial you will get introduced to the usage of Feature Groups which are kept in online storage, and how to access single feature vectors from the online storage
at low latency. Additionally, the model will be deployed as a model serving instance, to provide a REST endpoint for real time serving.

| Notebooks   |                                      |
| ----------- | ------------------------------------ |
| 1. How to load, engineer and create feature groups | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/fraud_online/1_feature_groups.ipynb){:target="_blank"}        |
| 2. How to create training datasets                 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/fraud_online/2_feature_view_creation.ipynb){:target="_blank"} |
| 3. How to train a model from the feature store and deploying it as a serving instance together with the online feature store | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/fraud_online/3_model_training.ipynb){:target="_blank"}        |

## Churn Tutorial

This is a churn tutorial with the Hopsworks feature store and model serving to build a prediction service. In this tutorial you will get introduced to the usage of Feature Groups which are kept in online storage, and how to access single feature vectors from the online storage
at low latency. Additionally, the model will be deployed as a model serving instance, to provide a REST endpoint for real time serving.

| Notebooks   |                                      |
| ----------- | ------------------------------------ |
| 1. How to load, engineer and create feature groups | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/churn/1_feature_groups.ipynb){:target="_blank"}        |
| 2. How to create training datasets                 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/churn/2_feature_view_creation.ipynb){:target="_blank"} |
| 3. How to train a model from the feature store and deploying it as a serving instance together with the online feature store | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/churn/3_model_training.ipynb){:target="_blank"}        |

## Iris Tutorial

In this tutorial you will learn how to create an online prediction service for the Iris flower prediction problem.

| Notebooks   |                                      |
| ----------- | ------------------------------------ |
| 1. All-in-one notebook, showing how to create the needed feature groups, train the model and deploy it as a serving instance | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/iris/iris_sklearn.ipynb){:target="_blank"}        |

## Integration Tutorials

Hopsworks is easily integrated with many tools, especially from the Python world. In this section you will find examples for some popular libraries and services.

### Great Expectations

Great Expectations is a library for data validation. You can use Great Expectations within Hopsworks to validate data which is to be inserted into the feature store, in order to ensure that only high-quality features end up in the feature store.

| Notebooks   |                                      |
| ----------- | ------------------------------------ |
| 1. A brief introduction to Great Expectations concepts which are relevant for integration with the Hopsworks MLOps platform | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/integrations/great_expectations/Great_Expectations_Hopsworks_Concepts.ipynb){:target="_blank"} |
| 2. How to integrate Great Expectations seamlessly with your Hopsworks feature pipelines | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/integrations/great_expectations/fraud_batch_data_validation.ipynb){:target="_blank"} |

### Weights and Biases

Weights and Biases is a developer tool for machine learning model training that with a couple of lines of code let you keep track of hyperparameters, system metrics, and outputs so you can compare experiments, and easily share your findings with colleagues.

This tutorial is a variant of the batch fraud tutorial using Weights and Biases for model training, tracking and as model registry.

| Notebooks   |                                      |
| ----------- | ------------------------------------ |
| 1. How to load, engineer and create feature groups | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/integrations/wandb/1_feature_groups.ipynb){:target="_blank"}        |
| 2. How to create training datasets                 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/integrations/wandb/2_feature_view_creation.ipynb){:target="_blank"} |
| 3. How to train a model from the feature store and use Weights and Biases to track the process | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/integrations/wandb/3_model_training.ipynb){:target="_blank"}        |
