# Feature Pipelines

A feature pipeline is a program that orchestrates the execution of a dataflow graph of data validation, aggregation, dimensionality reduction, transformation, and other feature engineering steps on input data to create and/or update feature data.
With Hopsworks, you can write feature pipelines in different languages as shown in the figure below.
A feature pipeline can run on a schedule over a batch of data, or continuously over an event stream; see [Streaming Feature Pipelines](streaming_feature_pipelines.md).

<figure class="hops-diagram">
<svg viewBox="0 0 1000 330" role="img" aria-label="Feature pipelines read from external data sources, run aggregation and validation steps in SQL, Python, or Spark and Flink, write to the feature store, and a later transform step produces features." xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="fp-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/></marker></defs>
  <rect class="d-box-ext" x="30" y="40" width="120" height="48" rx="8"/>
  <text class="d-t" x="90" y="69" text-anchor="middle">DB</text>
  <rect class="d-box-ext" x="30" y="108" width="120" height="48" rx="8"/>
  <text class="d-t" x="90" y="137" text-anchor="middle">Msg Bus</text>
  <rect class="d-box-ext" x="30" y="176" width="120" height="48" rx="8"/>
  <text class="d-t" x="90" y="205" text-anchor="middle">DB</text>
  <rect class="d-box-ext" x="30" y="244" width="120" height="48" rx="8"/>
  <text class="d-t" x="90" y="273" text-anchor="middle">Files</text>
  <path class="d-flow" d="M150 64 H320" marker-end="url(#fp-arrow)"/>
  <text class="d-t" x="235" y="54" text-anchor="middle">SQL</text>
  <path class="d-flow" d="M150 132 H200"/>
  <path class="d-flow" d="M150 268 H200"/>
  <path class="d-flow" d="M200 132 V268"/>
  <path class="d-flow" d="M150 200 H320" marker-end="url(#fp-arrow)"/>
  <text class="d-t" x="260" y="192" text-anchor="middle">Python</text>
  <text class="d-t" x="260" y="216" text-anchor="middle">Spark/Flink</text>
  <rect class="d-box" x="320" y="40" width="150" height="48" rx="8"/>
  <text class="d-t" x="395" y="69" text-anchor="middle">Aggregate, Validate</text>
  <rect class="d-box" x="320" y="168" width="150" height="64" rx="8"/>
  <text class="d-t" x="395" y="195" text-anchor="middle">Reduce, Aggregate,</text>
  <text class="d-t" x="395" y="215" text-anchor="middle">Validate</text>
  <path class="d-flow" d="M470 64 H540" marker-end="url(#fp-arrow)"/>
  <path class="d-flow" d="M470 200 H540" marker-end="url(#fp-arrow)"/>
  <rect class="d-box-own" x="540" y="40" width="120" height="252" rx="8"/>
  <text class="d-t" x="600" y="160" text-anchor="middle">Feature</text>
  <text class="d-t" x="600" y="180" text-anchor="middle">Store</text>
  <path class="d-flow" d="M660 166 H720" marker-end="url(#fp-arrow)"/>
  <rect class="d-box" x="720" y="142" width="110" height="48" rx="8"/>
  <text class="d-t" x="775" y="171" text-anchor="middle">Transform</text>
  <path class="d-flow" d="M830 166 H890" marker-end="url(#fp-arrow)"/>
  <rect class="d-box-own" x="890" y="142" width="100" height="48" rx="8"/>
  <text class="d-t" x="940" y="171" text-anchor="middle">Features</text>
</svg>
</figure>

## Data Sources

Your feature pipeline needs to connect to some (external) data source to read the data to be processed.
Python, Spark, and Flink have connectors to a huge number of different data sources, while SQL feature pipelines are often restricted to a single data source (for example, your connector to SnowFlake only runs SQL on SnowFlake).
SparkSQL, in contrast, can be used over tables that originate in different  data sources.

## Data Validation

In order to be able to train and serve models that you can rely on, you need clean, high quality features.
Data validation operations include removing bad data, removing or imputing missing values, and identifying problems such as feature drift.
Hopsworks supports Great Expectations to specify data validation rules that are executed in the client before features are written to the Feature Store.
The validation results are collected and shown in Hopsworks.
Data validation in ML is a shift-left property: data is validated before it is written to a feature group, since one bad data point could later fail a training or inference run.
The default ingestion policy is STRICT, so a feature pipeline fails on a validation error rather than writing bad data.

## Aggregations

Aggregations are used to summarize large datasets into more concise, signal-rich features.
Popular aggregations include count(), sum(), mean(), median(), stddev(), min(), and max().
These aggregations produce a single number (a numerical feature) that captures information about a potentially large dataset.
Both numerical and categorical features are often transformed before being used to train or serve models.

## Dimensionality Reduction

If input data is impractically large or if it has a significant amount of redundancy, it can often be transformed into a reduced set of features with dimensionality reduction (often called feature extraction).
Popular dimensionality algorithms include embedding algorithms, PCA, and TSNE.

## Transformations

Transformations are covered in more detail in [training/inference pipelines](../feature_view/training_inference_pipelines.md), as transformations typically happen after the feature store.
If you store transformed features in feature groups, the feature data is no longer useful for EDA (as it near to impossible for Data Scientists to understand the transformed values).
It also makes it impossible for inference pipelines to log untransformed feature values and predictions for an operational model.
There is one use case for storing transformed features in feature groups - when you need to have ultra low latency when reading precomputed features (and online transformations when reading features add too much latency for your use case).
The figure below shows to include transformations in your feature pipelines.

<figure class="hops-diagram">
<svg viewBox="0 0 1000 290" role="img" aria-label="A feature pipeline reads from external sources, then reduces, aggregates, validates, and transforms the data in Python or Spark and Flink before writing features to the feature store." xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="fpt-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/></marker></defs>
  <rect class="d-box-ext" x="40" y="40" width="140" height="48" rx="8"/>
  <text class="d-t" x="110" y="69" text-anchor="middle">Msg Bus</text>
  <rect class="d-box-ext" x="40" y="120" width="140" height="48" rx="8"/>
  <text class="d-t" x="110" y="149" text-anchor="middle">DB</text>
  <rect class="d-box-ext" x="40" y="200" width="140" height="48" rx="8"/>
  <text class="d-t" x="110" y="229" text-anchor="middle">Files</text>
  <path class="d-flow" d="M180 64 H210"/>
  <path class="d-flow" d="M180 224 H210"/>
  <path class="d-flow" d="M210 64 V224"/>
  <path class="d-flow" d="M180 144 H360" marker-end="url(#fpt-arrow)"/>
  <text class="d-t" x="285" y="136" text-anchor="middle">Python</text>
  <text class="d-t" x="285" y="160" text-anchor="middle">Spark/Flink</text>
  <rect class="d-box" x="360" y="104" width="180" height="80" rx="8"/>
  <text class="d-t" x="450" y="129" text-anchor="middle">Reduce, Aggregate,</text>
  <text class="d-t" x="450" y="149" text-anchor="middle">Validate,</text>
  <text class="d-t" x="450" y="169" text-anchor="middle">Transform</text>
  <path class="d-flow" d="M540 144 H620" marker-end="url(#fpt-arrow)"/>
  <rect class="d-box-own" x="620" y="40" width="140" height="208" rx="8"/>
  <text class="d-t" x="690" y="138" text-anchor="middle">Feature</text>
  <text class="d-t" x="690" y="158" text-anchor="middle">Store</text>
  <path class="d-flow" d="M760 144 H830" marker-end="url(#fpt-arrow)"/>
  <rect class="d-box-own" x="830" y="120" width="120" height="48" rx="8"/>
  <text class="d-t" x="890" y="149" text-anchor="middle">Features</text>
</svg>
</figure>

## Feature Engineering in Python

Python is the most widely used framework for feature engineering due to its extensive library support for aggregations (Pandas/Polars), data validation (Great Expectations), and dimensionality reduction (embeddings, PCA), and transformations (in Scikit-Learn, TensorFlow, PyTorch).
Python also supports open-source feature engineering frameworks used for automated feature engineering, such as [featuretools](https://www.featuretools.com/) that supports relational and temporal sources.

## Feature Engineering in Spark/PySpark

Spark is popular as a feature engineering framework as it can scale to process larger volumes of data than Python, and provides native support for aggregations, and it supports many of the same data validation (Great Expectations), and dimensionality reduction algorithms (embeddings, PCA) as Python.
Spark also has native support for transformations, which are useful for analytical models (batch scoring), but less useful for operational models, where online transformations are required, and Spark environments are less common.
Online model serving environments typically only support online transformations in Python.

## Feature Engineering in SQL

SQL has grown in popularity for performing heavy lifting in feature pipelines - computing aggregates on data - when the input data already resides in a data warehouse.
Data warehouses also support data validation, for example, through Great Expectations in DBT.
However, SQL is not mature as a platform for transformations and dimensionality reductions, where UDFs are applied row-wise.

You can do aggregation in SQL for data in your data warehouse or database.

## Feature Engineering in Flink

Apache Flink is a powerful and flexible framework for stateful feature computation operations over unbounded and bounded data streams.
It is used for feature engineering when you need very fresh features computed in real-time.
Flink provides a rich set of operators and functions such as time windows and aggregation operations that can be applied to keyed and/or global window streams.
Flink’s stateful operations allow users to maintain and update state across multiple data records or events, which is particularly useful for feature engineering tasks such as sessionization and/or maintaining rolling aggregates over a sliding window of data.

Flink feature engineering pipelines are supported in Java/Scala only.

## Feature Engineering in Beam

Beam feature engineering pipelines are supported in Java/Scala only.
