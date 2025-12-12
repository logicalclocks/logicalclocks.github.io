
Hopsworks provides a complete self-service development environment for feature engineering and model training.
You can develop programs as Jupyter notebooks or jobs, customize the bundled FTI (feature, training and inference pipeline) python environments, you can manage your source code with Git, and you can orchestrate jobs with Airflow.

<img src="../../../assets/images/concepts/dev/dev-inside.svg" alt="Hopsworks Development Environment" />

### Jupyter Notebooks

Hopsworks provides a Jupyter notebook development environment for programs written in Python, Spark, Flink, and SparkSQL.
You can also develop in your IDE (PyCharm, IntelliJ, etc), test locally, and then run your programs as Jobs in Hopsworks.
Jupyter notebooks can also be run as Jobs.

### Source Code Control

Hopsworks provides source code control support using Git (GitHub, GitLab or BitBucket).
You can securely check out code into your project and commit and push updates to your code to your source code repository.

### FTI Pipeline Environments

Hopsworks postulates that building ML systems following the FTI pipeline architecture is best practice.
This architecture consists of three independently developed and operated ML pipelines:

- Feature pipeline: takes as input raw data that it transforms into features (and labels)
- Training pipeline: takes as input features (and labels) and outputs a trained model
- Inference pipeline: takes new feature data and a trained model and makes predictions

In order to facilitate the development of these pipelines Hopsworks bundles several python environments containing necessary dependencies.
Each of these environments may then also be customized further by cloning it and installing additional dependencies from PyPi, Conda channels, Wheel files, GitHub repos or a custom Dockerfile.
Internal compute such as Jobs and Jupyter is run in one of these environments and changes are applied transparently when you install new libraries using our APIs.
That is, there is no need to write a Dockerfile, users install libraries directly in one or more of the environments.
You can setup custom development and production environments by creating separate projects or creating multiple clones of an environment within the same project.

### Jobs

In Hopsworks, a Job is a schedulable program that is allocated compute and memory resources.
You can run a Job in Hopsworks:

- From the UI
- Programmatically with the Hopsworks SDK (Python, Java) or REST API
- From Airflow programs (either inside our outside Hopsworks)
- From your IDE using a plugin ([PyCharm/IntelliJ plugin](https://plugins.jetbrains.com/plugin/15537-hopsworks))

### Orchestration

Airflow comes out-of-the box with Hopsworks, but you can also use an external Airflow cluster (with the Hopsworks Job operator) if you have one.
Airflow can be used to schedule the execution of Jobs, individually or as part of Airflow DAGs.
