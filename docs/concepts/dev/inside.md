Hopsworks provides a complete self-service development environment for feature engineering and model training. You can develop programs as Jupyer noteooks or jobs, you can manage the Python libaries in a project using its conda environment, you can manage your source code in Git or BitBucket, and you can orchestrate jobs with Airflow.

<img src="../../../assets/images/concepts/dev/dev-inside.svg">

### Jupyter Notebooks

Hopsworks provides a Jupyter notebook development environment for programs written in Python, Spark, Flink, and SparkSQL. You can also develop in your IDE (PyCharm, IntelliJ, etc), test locally, and then run your programs as Jobs in Hopsworks. Jupyter notebooks can also be run as Jobs.

### Source Code Control

Hopsworks provides source code control support using Git (Github, Gitlab) or Bitbucket. You can securely checkout code into your project and commit and push updates to your code to your source code repository. 

### Conda Environment per Project

Hopsworks supports the self-service installation of Python libraries using PyPi, Conda, Wheel files, or Github URLs. The Python libraries are installed in a Conda environment linked with your project. Each project has a base Docker image and its custom conda environment. Jobs are run as Docker images, but they are compiled transparently for you when you update your Conda enviornment. That is, there is no need to write a Dockerfile, users install Python libraries in their project. You can setup custom development and production environments by creating new projects, each with their own conda environment.

### Jobs

In Hopsworks, a Job is a schedulable program that is allocated compute and memory resources. You can run a Job in Hopsworks:

* from the UI;
* programmatically with the Hopsworks SDK (Python, Java) or REST API;
* from Airflow programs (either inside our outside Hopsworks);
* from your IDE using a plugin ([PyCharm/IntelliJ plugin](https://plugins.jetbrains.com/plugin/15537-hopsworks));

### Orchestration

Airflow comes out-of-the box with Hopsworks, but you can also use an external Airflow cluster (with the Hopsworks Job operator) if you have one. Airflow can be used to schedule the execution of Jobs, individually or as part of Airflow DAGs.