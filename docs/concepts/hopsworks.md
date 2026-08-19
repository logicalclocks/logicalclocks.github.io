# The Hopsworks Platform

Hopsworks is a **modular** MLOps platform with:

- a feature store (available as standalone)
- model registry and model serving based on KServe
- vector index based on OpenSearch
- a data science and data engineering platform

MLOps is a set of best practices for the automated testing, versioning, and monitoring of the ML pipelines and ML assets that power AI systems.
Hopsworks is modular, so you can adopt the feature store on its own or use the full platform across the MLOps lifecycle.

--8<-- "concepts/hopsworks/the-hopsworks-platform.html"

## Standalone Feature Store

Hopsworks was the first open-source and first enterprise feature store for ML.  You can use Hopsworks as a standalone feature store with the Hopsworks API.

## Model Management

Hopsworks includes support for model management, with model deployments using [the KServe framework](https://github.com/kserve/kserve) and a model registry designed for KServe.
Hopsworks logs all inference requests to Kafka to enable easy monitoring of deployed models, and provides model metrics with grafana/prometheus.

## Vector Index

A feature group with an embedding column can have a vector index, based on [OpenSearch kNN](https://opensearch.org/docs/latest/search-plugins/knn/index/) ([FAISS](https://ai.facebook.com/tools/faiss/) and [nmslib](https://github.com/nmslib/nmslib)).
The vector index includes out-of-the-box support for authentication, access control, filtering, backup-and-restore, and horizontal scalability.
The Feature Store and its vector index are often used together to build scalable recommender systems, such as ranking-and-retrieval for real-time recommendations.

## Governance

Hopsworks provides a data-mesh architecture for managing ML assets and teams, with multi-tenant projects.
Not unlike a GitHub repository, a project is a sandbox containing team members, data, and ML assets.
In Hopsworks, all ML assets (features, models, training data) are versioned, taggable, lineage-tracked, and support free-text search.
Data can be also be securely shared between projects.

## Data Science Platform

You can develop feature engineering, model training and inference pipelines in Hopsworks.
There is support for version control (GitHub, GitLab, BitBucket), Jupyter notebooks, a shared distributed file system, many bundled modular project Python environments for managing Python dependencies without needing to write Dockerfiles, jobs (Python, Spark, Flink), and workflow orchestration with Airflow.
