Hopsworks is a **modular** MLOps platform with:

 - a feature store (available as standalone)
 - model registry and model serving based on KServe
 - vector database based on OpenSearch
 - a data science and data engineering platform

<img src="../../assets/images/concepts/mlops/architecture.svg">

## Standalone Feature Store
Hopsworks was the first open-source and first enterprise feature store for ML.  You can use Hopsworks as a standalone feature store with the HSFS API.

## Model Management
Hopsworks includes support for model management, with model deployments using [the KServe framework](https://github.com/kserve/kserve) and a model registry designed for KServe. Hopsworks logs all inference requests to Kafka to enable easy monitoring of deployed models, and provides model metrics with grafana/prometheus.

## Vector DB
Hopsworks provides a vector database (or embedding store) based on [OpenSearch kNN](https://opensearch.org/docs/latest/search-plugins/knn/index/) ([FAISS](https://ai.facebook.com/tools/faiss/) and [nmslib](https://github.com/nmslib/nmslib)). Hopsworks Vector DB includes out-of-the-box support for authentication, access control, filtering, backup-and-restore, and horizontal scalability. Hopsworks' Feature Store and vector DB are often used together to build scalable recommender systems, such as ranking-and-retrieval for real-time recommendations. 

## Governance
Hopsworks provides a data-mesh architecture for managing ML assets and teams, with multi-tenant projects. Not unlike a github repository, a project is a sandbox containing team members, data, and ML assets. In Hopsworks, all ML assets (features, models, training data) are versioned, taggable, lineage-tracked, and support free-text search. Data can be also be securely shared between projects.

## Data Science Platform
You can develop feature engineering pipelines and training pipelines in Hopsworks. There is support for version control (github, gitlab, bitbucket), Jupyter notebooks, a shared distriubted file system, per project conda environments for managing python dependencies without needing to write Dockerfiles, jobs (Python, Spark, Flink), and workflow orchestration with Airflow.

