# Python Environments

### Introduction

Hopsworks postulates that building ML systems following the FTI pipeline architecture is best practice. This architecture consists of three independently developed and operated ML pipelines:

- Feature Pipeline: takes as input raw data that it transforms into features (and labels)
- Training Pipeline: takes as input features (and labels) and outputs a trained model
- Inference Pipeline: takes new feature data and a trained model and makes predictions.

In order to facilitate the development of these pipelines Hopsworks bundles several python environments containing necessary dependencies. 
Each environment can also be customized further by installing additional dependencies from PyPi, Conda, Wheel files, GitHub repos or applying custom Dockerfiles on top.

### Step 1: Go to environments page

Under the `Project settings` section you can find the `Python environment` setting.

### Step 2: List available environments

Environments listed under `FEATURE ENGINEERING` corresponds to environments you would use in a feature pipeline, `MODEL TRAINING` maps to environments used in a training pipeline and `MODEL INFERENCE` are what you would use in inference pipelines. 

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/python/environment_overview.png" alt="Bundled python environments">
    <figcaption>Bundled python environments</figcaption>
  </figure>
</p>

!!! note "Python version"
    The python version used in all the environments is 3.10.

### Feature engineering

The `FEATURE ENGINEERING` environments can be used in [Jupyter notebooks](../jupyter/python_notebook.md), a [Python job](../jobs/python_job.md) or a [PySpark job](../jobs/pyspark_job.md).

* `python-feature-pipeline` for writing feature pipelines using Python
* `spark-feature-pipeline` for writing feature pipelines using PySpark

### Model training

The `MODEL TRAINING` environments can be used in [Jupyter notebooks](../jupyter/python_notebook.md) or a [Python job](../jobs/python_job.md) or in a [Ray job](../jobs/ray_job.md). 

* `tensorflow-training-pipeline` to train TensorFlow models
* `torch-training-pipeline` to train PyTorch models
* `pandas-training-pipeline` to train XGBoost, Catboost and Sklearn models
* `ray_training_pipeline` a general purpose environment for distributed training using Ray framework to train 
  XGBoost and Sklearn models. Should be used in [Ray job](../jobs/ray_job.md). It can be customized to install 
  additional dependencies of your choice.
* `ray_torch_training_pipeline` for distributed training of PyTorch models using Ray framework in a [Ray job](../jobs/ray_job.md)
* `ray_tensorflow_training_pipeline` for distributed training of TensorFlow models using Ray framework in a [Ray job](../jobs/ray_job.md)

### Model inference

The `MODEL INFERENCE` environments can be used in a deployment using a custom predictor script.

* `tensorflow-inference-pipeline` to load and serve TensorFlow models
* `torch-inference-pipeline` to load and serve PyTorch models
* `pandas-inference-pipeline` to load and serve XGBoost, Catboost and Sklearn models
* `vllm-inference-pipeline` to load and serve LLMs with vLLM inference engine
* `minimal-inference-pipeline` to install your own custom framework, contains a minimal set of dependencies

## Next steps

In this guide you learned how to find the bundled python environments and where they can be used. Now you can test out the environment in a [Jupyter notebook](../jupyter/python_notebook.md).
