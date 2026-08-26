---
title: Hopsworks Documentation
description: "Hopsworks documentation: quickstart, architecture, guides by role and by task, deployment models, and API reference."
hide:
  - toc
---

<p class="hops-eyebrow">Hopsworks Documentation</p>

# Build, deploy & maintain AI systems

<p class="hops-lede">Features, training data, models and inference on one governed platform.</p>

<!-- markdownlint-disable MD007 MD030 -->
<div class="grid cards hops-quickcards" markdown>

-   :material-console: **Start from your terminal**

    ---

    Install the client and authenticate.
    `hops setup` opens a browser, caches an API key and connects you to a feature store.

    ```bash
    pip install "hopsworks[python]"
    hops setup
    ```

    [Client installation](user_guides/client_installation/index.md) ·
    <a href="python-api/">Python API</a>

-   :material-cloud-outline: **Use the managed SaaS**

    ---

    Sign in to the Hopsworks serverless app and create a project.
    Nothing to install, free tier available.

    [Open run.hopsworks.ai ↗](https://run.hopsworks.ai) ·
    [Tutorials](tutorials/index.md)

-   :material-server: **Deploy on your cloud or on-prem**

    ---

    Managed Kubernetes on AWS, Azure or GCP, or an air-gapped data centre.
    Talk to us to size and install it.

    [Contact Hopsworks ↗](https://www.hopsworks.ai/contact) ·
    [Deployment options](setup_installation/index.md)

</div>
<!-- markdownlint-enable MD007 MD030 -->

## Your first feature vector, in three steps

Create an [API key](user_guides/projects/api_key/create_api_key.md) in your project, then connect, write a feature group and read a feature vector back.

<div class="hops-steps">
<div class="hops-steps-rail" role="tablist" aria-label="Write features and read them in real time, step by step">
<button class="hops-step is-active" type="button" role="tab" aria-selected="true" data-step="connect">
<span class="hops-step-num">1</span>
<span class="hops-step-body"><strong>Connect</strong>
<small>Sign in and get a feature store.</small></span>
</button>
<button class="hops-step" type="button" role="tab" aria-selected="false" data-step="write">
<span class="hops-step-num">2</span>
<span class="hops-step-body"><strong>Write features</strong>
<small>Create a feature group and write data to the feature store.</small></span>
</button>
<button class="hops-step" type="button" role="tab" aria-selected="false" data-step="read">
<span class="hops-step-num">3</span>
<span class="hops-step-body"><strong>Read online</strong>
<small>Read a feature vector back from the online store.</small></span>
</button>
</div>
<div class="hops-steps-panels" markdown>
<div class="hops-step-panel is-active" data-step="connect" markdown>

```python
# pip install "hopsworks[python]"
import hopsworks


project = hopsworks.login()  # prompts for host and API key
fs = project.get_feature_store()
```

<p class="hops-step-status">Connected, feature store ready.</p>
</div>
<div class="hops-step-panel" data-step="write" markdown>

```python
import pandas as pd

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
```

<p class="hops-step-status">Feature group `transactions` v1 written, offline and online.</p>
</div>
<div class="hops-step-panel" data-step="read" markdown>

```python
fv = fs.get_or_create_feature_view(
    name="transactions_view",
    version=1,
    query=fg.select_all(),
)
fv.get_feature_vector(entry={"cc_num": 4467360740682089})
```

<p class="hops-step-status">Feature vector served from the online store.</p>
</div>
</div>
</div>

Next: [create a feature group](user_guides/fs/feature_group/create.md),
[create a feature view](user_guides/fs/feature_view/overview.md),
[retrieve feature vectors](user_guides/fs/feature_view/feature-vectors.md).

## One architecture, three pipelines

Independent [feature, training and inference pipelines](concepts/fti.md), connected by a shared feature store and model registry.

--8<-- "index/one-architecture-three-pipelines.html"

## Find your path

<div class="hops-role-index" markdown>

<div class="hops-role" markdown>
:material-code-tags:{ .hops-role-ico } Developer
{ .hops-role-cap }

- [Client installation](user_guides/client_installation/index.md)
- [Python, SageMaker, Kubeflow](user_guides/integrations/python.md)
- [Create a feature group](user_guides/fs/feature_group/create.md)
- <a href="python-api/">Python API reference</a>
</div>

<div class="hops-role" markdown>
:material-chart-scatter-plot:{ .hops-role-ico } Data scientist
{ .hops-role-cap }

- [Tutorials](tutorials/index.md)
- [Feature views](concepts/fs/feature_view/fv_overview.md)
- [Training data](user_guides/fs/feature_view/training-data.md)
- [Model serving](user_guides/mlops/serving/index.md)
</div>

<div class="hops-role" markdown>
:material-server:{ .hops-role-ico } Platform engineer
{ .hops-role-cap }

- [Jobs](user_guides/projects/jobs/python_job.md)
- [Airflow](user_guides/projects/airflow/airflow.md)
- [Python environments](user_guides/projects/python/python_env_overview.md)
- [Kubernetes scheduling](user_guides/projects/scheduling/kube_scheduler.md)
</div>

<div class="hops-role" markdown>
:material-shield-lock-outline:{ .hops-role-ico } Security engineer
{ .hops-role-cap }

- [Configure authentication](setup_installation/admin/auth.md)
- [API keys](user_guides/projects/api_key/create_api_key.md)
- [IAM role chaining](setup_installation/admin/roleChaining.md)
- [Audit logs](setup_installation/admin/audit/audit-logs.md)
</div>

<div class="hops-role" markdown>
:material-cog-outline:{ .hops-role-ico } Administrator
{ .hops-role-cap }

- [Administration overview](setup_installation/admin/index.md)
- [User management](setup_installation/admin/user.md)
- [Alerts](setup_installation/admin/alert.md)
- [HA and DR](setup_installation/admin/ha-dr/intro.md)
</div>

<div class="hops-role" markdown>
:material-compass-outline:{ .hops-role-ico } Evaluator
{ .hops-role-cap }

- [What Hopsworks is](concepts/hopsworks.md)
- [Feature store architecture](concepts/fs/index.md)
- [Analytical and operational ML](concepts/mlops/prediction_services.md)
- [Deployment options](setup_installation/index.md)
</div>

</div>

## By task

| Task | Start here |
| --- | --- |
| :material-rocket-launch-outline: Deploy | [AWS](setup_installation/aws/getting_started.md), [Azure](setup_installation/azure/getting_started.md), [GCP](setup_installation/gcp/getting_started.md), [on-prem](setup_installation/on_prem/contact_hopsworks.md), [Helm values](setup_installation/common/helm_chart_values.md) |
| :material-monitor-dashboard: Operate | [Administration](setup_installation/admin/index.md), [monitoring](setup_installation/admin/monitoring/grafana.md), [alerts](setup_installation/admin/alert.md), [HA and DR](setup_installation/admin/ha-dr/intro.md), [service operations](setup_installation/admin/operationLogs.md) |
| :material-wrench-outline: Troubleshoot | [Model serving](user_guides/mlops/serving/troubleshooting.md), [Python deployments](user_guides/projects/python-deployment/troubleshooting.md), [online ingestion](user_guides/fs/feature_group/online_ingestion_observability.md), [Jupyter session capacity](user_guides/projects/jupyter/session_capacity_warnings.md) |
| :material-arrow-up-circle-outline: Upgrade | [3.x to 4.0 migration](user_guides/migration/40_migration.md), [Airflow 3 upgrade](user_guides/projects/airflow/airflow3_upgrade.md), [Airflow 3 operator notes](setup_installation/admin/airflow3.md) |

<div class="hops-colophon" markdown>

<div markdown>
:material-api:{ .hops-colophon-ico } APIs
{ .hops-colophon-cap }

- <a href="python-api/">Python API</a>
- <a href="javadoc/">Java API</a>
- Machine-readable: <a href="llms.txt">llms.txt</a>, <a href="llms-full.txt">llms-full.txt</a>, or `<page>.md`
</div>

<div markdown>
:material-tune:{ .hops-colophon-ico } Configure and query
{ .hops-colophon-cap }

- [Helm chart values](setup_installation/common/helm_chart_values.md)
- [Cluster configuration](setup_installation/admin/variables.md)
- [Query engine (Trino)](user_guides/projects/trino/query_engine.md)
- [Vector similarity search](user_guides/fs/vector_similarity_search.md)
</div>

<div markdown>
:material-forum-outline:{ .hops-colophon-ico } Community and source
{ .hops-colophon-cap }

- [Public Slack ↗](https://join.slack.com/t/public-hopsworks/shared_invite/zt-24fc3hhyq-VBEiN8UZlKsDrrLvtU4NaA)
- [hopsworks-api on GitHub ↗](https://github.com/logicalclocks/hopsworks-api)
- [Apache License 2.0 ↗](https://www.apache.org/licenses/LICENSE-2.0.html)
</div>

</div>
