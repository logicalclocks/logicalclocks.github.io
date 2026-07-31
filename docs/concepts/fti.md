# FTI Pipeline Architecture

Hopsworks is built around a single architecture for AI systems: the decomposition of any AI system into **feature**, **training**, and **inference** (FTI) pipelines.
This page defines that architecture.
Every other concept in this section is a part of it, so read this first.

## The three pipelines

An AI system decomposes naturally into three machine learning pipelines, each with clear inputs and outputs, each developed, tested, and operated independently.

- A **feature pipeline** takes data as input and produces reusable feature data as output.
- A **training pipeline** takes feature data as input, trains a model, and outputs the trained model.
- An **inference pipeline** takes feature data and a model as input and outputs predictions and prediction logs.

The three pipelines are independent programs.
They are composed into a working system through a shared data layer: a [feature store](fs/index.md) and a [model registry](mlops/registry.md).

<figure class="hops-diagram">
<svg viewBox="0 0 1120 190" role="img" aria-label="FTI pipeline flow. Data sources feed a feature pipeline that writes to the feature store. A training pipeline reads the feature store and produces a model in the model registry. An inference pipeline reads the feature store and the model to produce predictions and prediction logs." xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="fti-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/>
    </marker>
  </defs>

  <path class="d-flow" d="M150 54 H170" marker-end="url(#fti-arrow)"/>
  <path class="d-flow" d="M310 54 H330" marker-end="url(#fti-arrow)"/>
  <path class="d-flow" d="M470 54 H490" marker-end="url(#fti-arrow)"/>
  <path class="d-flow" d="M630 54 H650" marker-end="url(#fti-arrow)"/>
  <path class="d-flow" d="M790 54 H810" marker-end="url(#fti-arrow)"/>
  <path class="d-flow" d="M950 54 H970" marker-end="url(#fti-arrow)"/>
  <path class="d-flow" d="M400 78 C400 112, 820 112, 848 78" marker-end="url(#fti-arrow)" stroke-dasharray="4 3"/>
  <path class="d-flow" d="M880 78 V120" marker-end="url(#fti-arrow)"/>

  <a class="d-link" href="../fs/feature_group/external_fg/">
    <rect class="d-box" x="10" y="30" width="140" height="48" rx="8"/>
    <text class="d-t" x="80" y="58" text-anchor="middle">Data sources</text>
  </a>
  <a class="d-link" href="../fs/feature_group/feature_pipelines/">
    <rect class="d-box" x="170" y="30" width="140" height="48" rx="8"/>
    <text class="d-t" x="240" y="58" text-anchor="middle">Feature pipeline</text>
  </a>
  <a class="d-link" href="../fs/feature_group/fg_overview/">
    <rect class="d-box-own" x="330" y="30" width="140" height="48" rx="8"/>
    <text class="d-t" x="400" y="58" text-anchor="middle">Feature store</text>
  </a>
  <a class="d-link" href="../mlops/training/">
    <rect class="d-box" x="490" y="30" width="140" height="48" rx="8"/>
    <text class="d-t" x="560" y="58" text-anchor="middle">Training pipeline</text>
  </a>
  <a class="d-link" href="../mlops/registry/">
    <rect class="d-box-own" x="650" y="30" width="140" height="48" rx="8"/>
    <text class="d-t" x="720" y="58" text-anchor="middle">Model registry</text>
  </a>
  <a class="d-link" href="../mlops/serving/">
    <rect class="d-box" x="810" y="30" width="140" height="48" rx="8"/>
    <text class="d-t" x="880" y="58" text-anchor="middle">Inference pipeline</text>
  </a>
  <a class="d-link" href="../mlops/prediction_services/">
    <rect class="d-box" x="970" y="30" width="140" height="48" rx="8"/>
    <text class="d-t" x="1040" y="58" text-anchor="middle">Predictions</text>
  </a>
  <a class="d-link" href="../mlops/model_monitoring/">
    <rect class="d-box" x="810" y="120" width="140" height="48" rx="8"/>
    <text class="d-t" x="880" y="148" text-anchor="middle">Prediction logs</text>
  </a>
</svg>
</figure>

Feature pipelines ingest both backfill and production data and compute feature data that is stored as tabular data in the feature store.
Feature pipelines can be batch programs or stream processing programs.
Training pipelines read training data from the feature store and store the models they produce in the model registry.
Inference pipelines output predictions using a model, either downloaded from the model registry or served behind an API, together with new feature data that is precomputed in the feature store or computed from data available at prediction request time.

## Why this architecture

The five common AI system architectures (batch, stateless real-time, stateful real-time, RAG, and agentic) are very different from one another.
Moving from one to another, or transferring what you learned building one, is hard.
The FTI decomposition gives you one architecture for all of them.

Modularity is the reason.
Splitting an AI system into independent, small, testable modules lets teams build higher-quality systems faster.
It also splits the work cleanly: feature engineering can involve data engineers, model training is the realm of data scientists, and inference can involve operations.

## The shared data layer

The feature store holds three stores of feature data, each serving a different pipeline.

- A row-oriented online store for low latency access from online inference pipelines and agents.
- A columnar offline store for training models and batch inference.
- A [vector index](mlops/opensearch.md) over embeddings for inference pipelines and agents.

The model registry holds the trained models and their assets, versioned, for inference pipelines to load.

## What an AI system is

An AI system is a set of independent feature pipelines, training pipelines, and inference pipelines connected through a feature store and a model registry.

An AI system is defined by how it computes its predictions, not by the type of application that consumes them.
On that basis, AI systems built with a feature store fall into four classes.

- **Real-time (interactive)** systems make predictions in response to user requests.
    They read precomputed features from the feature store and can also compute features on demand from the request parameters.
- **Agentic workflows** achieve goals with some autonomy using LLMs and tools, drawing context from a vector index, the online and offline stores, and external APIs.
- **Batch** systems run inference on a schedule and write predictions to a downstream store, called an inference store, for an application to consume later.
- **Stream processing** systems use an embedded model to make predictions on streaming data without user input, often machine to machine.

The inference pipeline is what determines the class.
When you know how a system computes its predictions, you know which of these you are building.

## Where to go next

- [Feature Store Architecture](fs/index.md) for the shared data layer in detail.
- [Feature Groups](fs/feature_group/fg_overview.md) for how feature pipelines write feature data.
- [Feature Views](fs/feature_view/fv_overview.md) for how training and inference pipelines read it.
- [AI Systems](mlops/prediction_services.md) for the inference side and how each class is served.
