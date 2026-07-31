---
description: "Hopsworks documentation: quickstart, architecture, guides by role and by task, deployment models, and API reference."
hide:
  - navigation
---

# Hopsworks Documentation

Hopsworks is a modular data platform for machine learning.
It provides a Python-centric feature store, a model registry and model serving on KServe, a vector database, and project-based multi-tenancy for teams.
You can run it as a standalone feature store, as an MLOps platform, or as both.

<!-- markdownlint-disable MD007 MD030 -->
<div class="grid cards" markdown>

-   :material-rocket-launch-outline: **Start in five minutes**

    ---

    Run the quickstart notebook in Colab against a free serverless project.
    Nothing to install.

    [Open the quickstart notebook ↗](https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/quickstart.ipynb)

-   :material-package-variant: **Install the client**

    ---

    `pip install hopsworks[python]`, then connect from any Python, Spark, Flink or Java environment.

    [Client installation](user_guides/client_installation/index.md)

-   :material-sitemap-outline: **See the architecture**

    ---

    How the feature store, MLOps and governance layers fit together.

    [Platform architecture](concepts/hopsworks.md) ·
    [Feature store architecture](concepts/fs/index.md)

</div>
<!-- markdownlint-enable MD007 MD030 -->

## Hello world

Create an [API key](user_guides/projects/api_key/create_api_key.md) in your project, then write a feature group and read a feature vector back.

```python
import hopsworks
import pandas as pd


project = hopsworks.login()  # prompts for host, project and API key
fs = project.get_feature_store()

df = pd.DataFrame(
    {
        "cc_num": [4467360740682089],
        "amount": [12.5],
        "event_time": pd.to_datetime(["2026-01-01T00:00:00Z"]),
    }
)

fg = fs.get_or_create_feature_group(
    name="transactions",
    version=1,
    primary_key=["cc_num"],
    event_time="event_time",
    online_enabled=True,
)
fg.insert(df)

fv = fs.get_or_create_feature_view(
    name="transactions_view",
    version=1,
    query=fg.select_all(),
)
fv.get_feature_vector(entry={"cc_num": 4467360740682089})
```

Next: [create a feature group](user_guides/fs/feature_group/create.md),
[create a feature view](user_guides/fs/feature_view/overview.md),
[retrieve feature vectors](user_guides/fs/feature_view/feature-vectors.md).

## Choose a deployment model

<!-- markdownlint-disable MD007 MD030 -->
<div class="grid cards" markdown>

-   :material-cloud-outline: **Serverless**

    ---

    Managed by Hopsworks, free tier available.
    Nothing to install or operate.

    [app.hopsworks.ai ↗](https://app.hopsworks.ai) ·
    [Tutorials](tutorials/index.md)

-   :material-kubernetes: **Managed Kubernetes**

    ---

    Install on your own EKS, AKS or GKE cluster.

    [AWS](setup_installation/aws/getting_started.md) ·
    [Azure](setup_installation/azure/getting_started.md) ·
    [GCP](setup_installation/gcp/getting_started.md)

-   :material-server: **On-premises**

    ---

    Any Kubernetes cluster, including air-gapped data centres.

    [On-prem background](setup_installation/on_prem/contact_hopsworks.md) ·
    [External Kafka cluster](setup_installation/on_prem/external_kafka_cluster.md)

-   :material-tune: **Configure the install**

    ---

    Every Helm value, and the cluster variables you set after install.

    [Helm chart values](setup_installation/common/helm_chart_values.md) ·
    [Cluster configuration](setup_installation/admin/variables.md)

</div>
<!-- markdownlint-enable MD007 MD030 -->

## By role

<!-- markdownlint-disable MD007 MD030 -->
<div class="grid cards" markdown>

-   **Developer**

    ---

    Connect from your own environment and build feature pipelines.

    - [Client installation](user_guides/client_installation/index.md)
    - [Python, SageMaker, Kubeflow](user_guides/integrations/python.md)
    - [Create a feature group](user_guides/fs/feature_group/create.md)
    - [Compute engines](user_guides/fs/compute_engines.md)
    - <a href="python-api/">Python API reference</a>

-   **Data scientist**

    ---

    Turn features into training data, models and deployments.

    - [Tutorials](tutorials/index.md)
    - [Feature views](concepts/fs/feature_view/fv_overview.md)
    - [Training data](user_guides/fs/feature_view/training-data.md)
    - [Model registry](user_guides/mlops/registry/index.md)
    - [Model serving](user_guides/mlops/serving/index.md)

-   **Platform engineer**

    ---

    Run pipelines, environments and orchestration in production.

    - [Jobs](user_guides/projects/jobs/python_job.md)
    - [Airflow](user_guides/projects/airflow/airflow.md)
    - [Python environments](user_guides/projects/python/python_env_overview.md)
    - [Kubernetes scheduling](user_guides/projects/scheduling/kube_scheduler.md)
    - [ArrowFlight with DuckDB](setup_installation/common/arrow_flight_duckdb.md)

-   **Security engineer**

    ---

    Authentication, secrets, isolation and audit.

    - [Configure authentication](setup_installation/admin/auth.md)
    - [OAuth2](setup_installation/admin/oauth2/create-client.md) ·
      [LDAP](setup_installation/admin/ldap/configure-ldap.md) ·
      [Kerberos](setup_installation/admin/ldap/configure-krb.md)
    - [API keys](user_guides/projects/api_key/create_api_key.md) ·
      [Secrets](user_guides/projects/secrets/create_secret.md)
    - [IAM role chaining](setup_installation/admin/roleChaining.md)
    - [Audit logs](setup_installation/admin/audit/audit-logs.md)
    - [Project-based multi-tenancy](concepts/projects/governance.md)

-   **Administrator**

    ---

    Operate the cluster, its users and its data.

    - [Administration overview](setup_installation/admin/index.md)
    - [User management](setup_installation/admin/user.md) ·
      [Project management](setup_installation/admin/project.md)
    - [Alerts](setup_installation/admin/alert.md)
    - [Grafana dashboards](setup_installation/admin/monitoring/grafana.md) ·
      [Service logs](setup_installation/admin/monitoring/services-logs.md)
    - [High availability and disaster recovery](setup_installation/admin/ha-dr/intro.md)

-   **Evaluator**

    ---

    Understand what Hopsworks is before installing anything.

    - [What Hopsworks is](concepts/hopsworks.md)
    - [Feature store architecture](concepts/fs/index.md)
    - [Analytical and operational ML](concepts/mlops/prediction_services.md)
    - [Tags, search and lineage](concepts/projects/search.md)
    - [Deployment options](setup_installation/index.md)

</div>
<!-- markdownlint-enable MD007 MD030 -->

## By task

| Task | Start here |
| --- | --- |
| Evaluate | [Platform overview](concepts/hopsworks.md), [feature store architecture](concepts/fs/index.md), [deployment options](setup_installation/index.md) |
| Learn | [Concepts](concepts/hopsworks.md), [tutorials](tutorials/index.md), [MLOps dictionary ↗](https://www.hopsworks.ai/mlops-dictionary) |
| Build | [How-to guides](user_guides/index.md), [feature store guides](user_guides/fs/index.md), [MLOps guides](user_guides/mlops/index.md), [agents](user_guides/agents/index.md) |
| Deploy | [AWS](setup_installation/aws/getting_started.md), [Azure](setup_installation/azure/getting_started.md), [GCP](setup_installation/gcp/getting_started.md), [on-prem](setup_installation/on_prem/contact_hopsworks.md), [Helm values](setup_installation/common/helm_chart_values.md) |
| Operate | [Administration](setup_installation/admin/index.md), [monitoring](setup_installation/admin/monitoring/grafana.md), [alerts](setup_installation/admin/alert.md), [HA and DR](setup_installation/admin/ha-dr/intro.md), [service operations](setup_installation/admin/operationLogs.md) |
| Troubleshoot | [Model serving](user_guides/mlops/serving/troubleshooting.md), [Python deployments](user_guides/projects/python-deployment/troubleshooting.md), [online ingestion](user_guides/fs/feature_group/online_ingestion_observability.md), [Jupyter session capacity](user_guides/projects/jupyter/session_capacity_warnings.md) |
| Upgrade | [3.x to 4.0 migration](user_guides/migration/40_migration.md), [Airflow 3 upgrade](user_guides/projects/airflow/airflow3_upgrade.md), [Airflow 3 operator notes](setup_installation/admin/airflow3.md) |

## Reference

- <a href="python-api/">Python API</a> and <a href="javadoc/">Java API</a>
- [Helm chart values](setup_installation/common/helm_chart_values.md) and [cluster configuration](setup_installation/admin/variables.md)
- [Query engine (Trino)](user_guides/projects/trino/query_engine.md) and [vector similarity search](user_guides/fs/vector_similarity_search.md)
- Machine-readable index for agents and LLMs: <a href="llms.txt">llms.txt</a>, <a href="llms-full.txt">llms-full.txt</a>.
  Every page also has a raw Markdown sibling at `<page>.md`.

## Community and source

- Questions and feedback: [Hopsworks Community ↗](https://community.hopsworks.ai/)
- Chat: [public Slack ↗](https://bit.ly/publichopsworks)
- Releases and issues: [hopsworks-api on GitHub ↗](https://github.com/logicalclocks/hopsworks-api)
- The Hopsworks Python API is licensed under the [Apache License 2.0 ↗](https://www.apache.org/licenses/LICENSE-2.0.html).
