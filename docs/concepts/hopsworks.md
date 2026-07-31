Hopsworks is a **modular** MLOps platform with:

- a feature store (available as standalone)
- model registry and model serving based on KServe
- vector database based on OpenSearch
- a data science and data engineering platform

<figure class="hops-arch">
<svg viewBox="0 0 1000 470" role="img" aria-label="Hopsworks platform architecture: feature engineering feeds the feature store and MLOps layer, model training reads from it, all on a shared multi-tenant platform." xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;font-family:Roboto,system-ui,sans-serif">
  <style>
    .ha-panel-fs { fill:#21b182; fill-opacity:.07; stroke:#21b182; stroke-opacity:.55; }
    .ha-panel-ext { fill:#41b7dc; fill-opacity:.06; stroke:#41b7dc; stroke-opacity:.45; }
    .ha-band { fill:currentColor; fill-opacity:.03; stroke:currentColor; stroke-opacity:.18; }
    .ha-box { fill:currentColor; fill-opacity:.02; stroke:currentColor; stroke-opacity:.22; }
    .ha-box-own { fill:#21b182; fill-opacity:.10; stroke:#21b182; stroke-opacity:.55; }
    .ha-api { fill:#21b182; fill-opacity:.16; stroke:#21b182; stroke-opacity:.6; }
    .ha-t { fill:currentColor; }
    .ha-cap-fs { fill:#188a64; font-weight:600; letter-spacing:.04em; }
    .ha-cap-ext { fill:#186781; font-weight:600; letter-spacing:.04em; }
    .ha-flow { stroke:currentColor; stroke-opacity:.3; fill:none; }
    text { font-size:13px; }
    .ha-cap { font-size:11px; text-transform:uppercase; }
    .ha-sub { font-size:11px; fill:currentColor; fill-opacity:.6; }
    a.ha-link { cursor:pointer; }
    a.ha-link > rect { transition:fill-opacity .12s, stroke-opacity .12s; }
    a.ha-link:hover > rect { fill-opacity:.24; stroke-opacity:.9; }
    a.ha-link > text, a.ha-link:hover > text { text-decoration:none; }
  </style>

  <!-- flow connectors behind panels -->
  <path class="ha-flow" d="M236 210 H262" marker-end="url(#ha-arrow)"/>
  <path class="ha-flow" d="M736 210 H762" marker-end="url(#ha-arrow)"/>
  <defs>
    <marker id="ha-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/>
    </marker>
  </defs>

  <!-- Feature Engineering -->
  <text class="ha-t ha-cap ha-cap-ext" x="30" y="40">Feature Engineering</text>
  <rect class="ha-panel-ext" x="24" y="52" width="212" height="308" rx="12"/>
  <a class="ha-link" href="../fs/feature_group/feature_pipelines/">
    <rect class="ha-box" x="42" y="70" width="176" height="34" rx="6"/>
    <text class="ha-t" x="130" y="92" text-anchor="middle">Python, Pandas, Polars</text>
  </a>
  <a class="ha-link" href="../fs/feature_group/feature_pipelines/">
    <rect class="ha-box" x="42" y="112" width="176" height="34" rx="6"/>
    <text class="ha-t" x="130" y="134" text-anchor="middle">Spark, Spark Streaming</text>
  </a>
  <a class="ha-link" href="../fs/feature_group/feature_pipelines/">
    <rect class="ha-box" x="42" y="154" width="176" height="34" rx="6"/>
    <text class="ha-t" x="130" y="176" text-anchor="middle">Flink</text>
  </a>
  <a class="ha-link" href="../fs/feature_group/feature_pipelines/">
    <rect class="ha-box" x="42" y="196" width="176" height="34" rx="6"/>
    <text class="ha-t" x="130" y="218" text-anchor="middle">SQL</text>
  </a>
  <a class="ha-link" href="../fs/feature_group/external_fg/">
    <rect class="ha-box" x="42" y="250" width="176" height="90" rx="6"/>
    <text class="ha-t ha-sub" x="130" y="272" text-anchor="middle">DATA SOURCES</text>
    <text class="ha-t" x="130" y="296" text-anchor="middle">S3 · Kafka · JDBC</text>
    <text class="ha-t" x="130" y="318" text-anchor="middle">Snowflake · BigQuery</text>
  </a>

  <!-- Feature Store & MLOps -->
  <text class="ha-t ha-cap ha-cap-fs" x="268" y="40">Feature Store &amp; MLOps</text>
  <rect class="ha-panel-fs" x="262" y="52" width="476" height="308" rx="12"/>
  <a class="ha-link" href="../dev/outside/">
    <rect class="ha-api" x="280" y="68" width="440" height="30" rx="6"/>
    <text class="ha-t" x="500" y="88" text-anchor="middle">Hopsworks API · Python · Java · REST</text>
  </a>

  <text class="ha-t ha-sub" x="292" y="122">FEATURE STORE</text>
  <a class="ha-link" href="../fs/feature_group/fg_overview/">
    <rect class="ha-box-own" x="280" y="132" width="210" height="34" rx="6"/>
    <text class="ha-t" x="385" y="154" text-anchor="middle">Feature Groups</text>
  </a>
  <a class="ha-link" href="../fs/feature_group/external_fg/">
    <rect class="ha-box" x="280" y="174" width="210" height="34" rx="6"/>
    <text class="ha-t" x="385" y="196" text-anchor="middle">External Feature Groups</text>
  </a>
  <a class="ha-link" href="../fs/feature_view/fv_overview/">
    <rect class="ha-box" x="280" y="216" width="210" height="34" rx="6"/>
    <text class="ha-t" x="385" y="238" text-anchor="middle">Feature Views (online / offline)</text>
  </a>
  <a class="ha-link" href="../mlops/opensearch/">
    <rect class="ha-box" x="280" y="258" width="210" height="34" rx="6"/>
    <text class="ha-t" x="385" y="280" text-anchor="middle">Vector Index</text>
  </a>

  <text class="ha-t ha-sub" x="522" y="122">MLOPS</text>
  <a class="ha-link" href="../mlops/registry/">
    <rect class="ha-box-own" x="510" y="132" width="210" height="34" rx="6"/>
    <text class="ha-t" x="615" y="154" text-anchor="middle">Model Registry</text>
  </a>
  <a class="ha-link" href="../mlops/serving/">
    <rect class="ha-box" x="510" y="174" width="210" height="34" rx="6"/>
    <text class="ha-t" x="615" y="196" text-anchor="middle">Model Serving on KServe</text>
  </a>
  <a class="ha-link" href="../mlops/model_monitoring/">
    <rect class="ha-box" x="510" y="216" width="210" height="34" rx="6"/>
    <text class="ha-t" x="615" y="238" text-anchor="middle">Model Monitoring</text>
  </a>
  <a class="ha-link" href="../mlops/model_monitoring/">
    <rect class="ha-box" x="510" y="258" width="210" height="34" rx="6"/>
    <text class="ha-t" x="615" y="280" text-anchor="middle">Prediction / feature logging</text>
  </a>

  <!-- Model Training -->
  <text class="ha-t ha-cap ha-cap-ext" x="768" y="40">Model Training</text>
  <rect class="ha-panel-ext" x="762" y="52" width="214" height="308" rx="12"/>
  <a class="ha-link" href="../mlops/training/">
    <rect class="ha-box" x="780" y="70" width="178" height="34" rx="6"/>
    <text class="ha-t" x="869" y="92" text-anchor="middle">Experiment Tracking</text>
  </a>
  <a class="ha-link" href="../mlops/training/">
    <rect class="ha-box" x="780" y="112" width="178" height="50" rx="6"/>
    <text class="ha-t" x="869" y="134" text-anchor="middle">Distributed Training</text>
    <text class="ha-t" x="869" y="152" text-anchor="middle">&amp; HPO</text>
  </a>
  <a class="ha-link" href="../mlops/training/">
    <rect class="ha-box" x="780" y="196" width="178" height="90" rx="6"/>
    <text class="ha-t ha-sub" x="869" y="218" text-anchor="middle">FRAMEWORKS</text>
    <text class="ha-t" x="869" y="242" text-anchor="middle">PyTorch · TensorFlow</text>
    <text class="ha-t" x="869" y="264" text-anchor="middle">Scikit-Learn · XGBoost</text>
  </a>

  <!-- Platform band -->
  <a class="ha-link" href="../projects/governance/">
    <rect class="ha-band" x="24" y="386" width="952" height="60" rx="12"/>
    <text class="ha-t ha-sub" x="40" y="410">MULTI-TENANT PLATFORM</text>
    <text class="ha-t" x="40" y="432">Projects &amp; multi-tenancy · Jobs (Python, Spark, Flink) · Jupyter · Airflow · Governance (search, tags, lineage) · Auth (SSO, RBAC)</text>
  </a>
</svg>
</figure>

## Standalone Feature Store

Hopsworks was the first open-source and first enterprise feature store for ML.  You can use Hopsworks as a standalone feature store with the Hopsworks API.

## Model Management

Hopsworks includes support for model management, with model deployments using [the KServe framework](https://github.com/kserve/kserve) and a model registry designed for KServe.
Hopsworks logs all inference requests to Kafka to enable easy monitoring of deployed models, and provides model metrics with grafana/prometheus.

## Vector DB

Hopsworks provides a vector database (or embedding store) based on [OpenSearch kNN](https://opensearch.org/docs/latest/search-plugins/knn/index/) ([FAISS](https://ai.facebook.com/tools/faiss/) and [nmslib](https://github.com/nmslib/nmslib)).
Hopsworks Vector DB includes out-of-the-box support for authentication, access control, filtering, backup-and-restore, and horizontal scalability.
Hopsworks' Feature Store and vector DB are often used together to build scalable recommender systems, such as ranking-and-retrieval for real-time recommendations.

## Governance

Hopsworks provides a data-mesh architecture for managing ML assets and teams, with multi-tenant projects.
Not unlike a GitHub repository, a project is a sandbox containing team members, data, and ML assets.
In Hopsworks, all ML assets (features, models, training data) are versioned, taggable, lineage-tracked, and support free-text search.
Data can be also be securely shared between projects.

## Data Science Platform

You can develop feature engineering, model training and inference pipelines in Hopsworks.
There is support for version control (GitHub, GitLab, BitBucket), Jupyter notebooks, a shared distributed file system, many bundled modular project Python environments for managing Python dependencies without needing to write Dockerfiles, jobs (Python, Spark, Flink), and workflow orchestration with Airflow.
