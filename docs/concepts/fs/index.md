# Feature Store Architecture


<a name="what"></a>

## What is Hopsworks Feature Store?

Hopsworks and its Feature Store are an open source data-intensive AI platform used for the development and operation of machine learning models at scale.
The Hopsworks Feature Store provides the Hopsworks API to enable clients to write features to feature groups in the feature store, and to read features from feature views - either through a low latency Online API to retrieve pre-computed features for operational models or through a high throughput, latency insensitive Offline API, used to create training data and to retrieve batch data for scoring.

<figure class="hops-diagram">
<svg viewBox="0 0 1080 210" role="img" aria-label="Feature store architecture. A feature pipeline writes to feature groups, held in an online store and an offline store. Feature views read from the feature groups and serve features through an online API for operational models and an offline API for training data and batch scoring." xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="fs-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/>
    </marker>
  </defs>

  <a class="d-link" href="../dev/outside/">
    <rect class="d-api" x="20" y="14" width="1040" height="28" rx="6"/>
    <text class="d-t" x="540" y="33" text-anchor="middle">Hopsworks API · Python · Java · REST</text>
  </a>

  <path class="d-flow" d="M200 100 H256" marker-end="url(#fs-arrow)"/>
  <path class="d-flow" d="M616 100 H656" marker-end="url(#fs-arrow)"/>
  <path class="d-flow" d="M347 120 V150" marker-end="url(#fs-arrow)"/>
  <path class="d-flow" d="M515 120 V150" marker-end="url(#fs-arrow)"/>
  <path class="d-flow" d="M760 120 V150" marker-end="url(#fs-arrow)"/>
  <path class="d-flow" d="M956 120 V150" marker-end="url(#fs-arrow)"/>
  <text class="d-t d-sub" x="212" y="94">write</text>
  <text class="d-t d-sub" x="622" y="94">read</text>

  <text class="d-t d-cap d-cap-ext" x="20" y="66">Write</text>
  <a class="d-link" href="feature_group/feature_pipelines/">
    <rect class="d-box" x="20" y="76" width="180" height="48" rx="8"/>
    <text class="d-t" x="110" y="97" text-anchor="middle">Feature pipeline</text>
    <text class="d-t d-sub" x="110" y="114" text-anchor="middle">Python · Spark · Flink · SQL</text>
  </a>

  <text class="d-t d-cap d-cap-fs" x="262" y="66">Feature Store</text>
  <rect class="d-panel-fs" x="256" y="72" width="360" height="126" rx="12"/>
  <a class="d-link" href="feature_group/fg_overview/">
    <rect class="d-box-own" x="272" y="80" width="328" height="40" rx="6"/>
    <text class="d-t" x="436" y="105" text-anchor="middle">Feature Groups</text>
  </a>
  <a class="d-link" href="feature_group/fg_overview/">
    <rect class="d-box" x="272" y="150" width="150" height="40" rx="6"/>
    <text class="d-t" x="347" y="175" text-anchor="middle">Online store</text>
  </a>
  <a class="d-link" href="feature_group/fg_overview/">
    <rect class="d-box" x="440" y="150" width="160" height="40" rx="6"/>
    <text class="d-t" x="520" y="175" text-anchor="middle">Offline store</text>
  </a>

  <text class="d-t d-cap d-cap-fs" x="662" y="66">Read</text>
  <rect class="d-panel-fs" x="656" y="72" width="404" height="126" rx="12"/>
  <a class="d-link" href="feature_view/fv_overview/">
    <rect class="d-box-own" x="672" y="80" width="372" height="40" rx="6"/>
    <text class="d-t" x="858" y="105" text-anchor="middle">Feature Views</text>
  </a>
  <a class="d-link" href="feature_view/online_api/">
    <rect class="d-box" x="672" y="150" width="176" height="40" rx="6"/>
    <text class="d-t" x="760" y="168" text-anchor="middle">Online API</text>
    <text class="d-t d-sub" x="760" y="183" text-anchor="middle">operational models</text>
  </a>
  <a class="d-link" href="feature_view/offline_api/">
    <rect class="d-box" x="868" y="150" width="176" height="40" rx="6"/>
    <text class="d-t" x="956" y="168" text-anchor="middle">Offline API</text>
    <text class="d-t d-sub" x="956" y="183" text-anchor="middle">training data · batch</text>
  </a>
</svg>
</figure>

## Hopsworks API

The Hopsworks API is how you, as a developer, will use the feature store.
The Hopsworks API helps simplify some of the problems that feature stores address including:

- consistent features for training and serving
- centralized, secure access to features
- point-in-time JOINs of features to create training data with no data leakage
- easier connection and backfilling of features from external data sources
- use of external tables as features
- transparent computation of statistics and usage data for features.

## Write to feature groups, read from feature views

You write to feature groups with a feature pipeline program.
The program can be written in Python, Spark, Flink, or SQL.

You read from views on top of the feature groups, called feature views.
That is, a feature view does not store feature data, but is a logical grouping of features.
Typically, you define a feature view because you want to train/deploy a model with exactly those features in the feature view.
Feature views enable the reuse of feature data from different feature groups across different models.
