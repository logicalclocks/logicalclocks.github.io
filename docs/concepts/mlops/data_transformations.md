# Data Transformations

[Data transformations](https://www.hopsworks.ai/dictionary/data-transformation) are integral to all AI applications.
Data transformations produce new features that can enhance the performance of an AI application.
However, [not all transformations in an AI application are equivalent](https://www.hopsworks.ai/post/a-taxonomy-for-data-transformations-in-ai-systems).

Transformations like binning and aggregations typically create reusable features, while transformations like one-hot encoding, scaling and normalization often produce model-specific features.
Additionally, in real-time AI systems, some features can only be computed during inference when the request is received, as they need request-time parameters to be computed.

<figure class="hops-diagram">
<svg viewBox="0 0 1000 250" role="img" aria-label="A feature falls into three categories: reusable features from model-independent transformations (aggregations, binning, chunking for RAG), model-specific features from model-dependent transformations (encoding, scaling, imputation, tokenization in LLMs), and on-demand features that need request-time parameters to compute." xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="tf-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/>
    </marker>
  </defs>
  <rect class="d-box" x="420" y="20" width="160" height="48" rx="8"/>
  <text class="d-t" x="500" y="49" text-anchor="middle">Feature</text>

  <path class="d-flow" d="M500 68 V100 H175 V140" marker-end="url(#tf-arrow)"/>
  <path class="d-flow" d="M500 68 V140" marker-end="url(#tf-arrow)"/>
  <path class="d-flow" d="M500 68 V100 H825 V140" marker-end="url(#tf-arrow)"/>

  <rect class="d-box-own" x="40" y="140" width="270" height="48" rx="8"/>
  <text class="d-t" x="175" y="169" text-anchor="middle">Reusable features</text>
  <text class="d-t d-sub" x="175" y="212" text-anchor="middle">aggregations, binning,</text>
  <text class="d-t d-sub" x="175" y="230" text-anchor="middle">chunking for RAG</text>

  <rect class="d-box" x="365" y="140" width="270" height="48" rx="8"/>
  <text class="d-t" x="500" y="169" text-anchor="middle">Model-specific features</text>
  <text class="d-t d-sub" x="500" y="212" text-anchor="middle">encoding, scaling, imputation,</text>
  <text class="d-t d-sub" x="500" y="230" text-anchor="middle">tokenization in LLMs</text>

  <rect class="d-box-ext" x="690" y="140" width="270" height="48" rx="8"/>
  <text class="d-t" x="825" y="169" text-anchor="middle">On-demand features</text>
  <text class="d-t d-sub" x="825" y="212" text-anchor="middle">need request-time</text>
  <text class="d-t d-sub" x="825" y="230" text-anchor="middle">parameters to compute</text>
</svg>
</figure>

This classification of features can be used to create a taxonomy for data transformation that would apply to any scalable and modular AI system that aims to reuse features.
The taxonomy helps identify which classes of data transformation can cause [online-offline](https://www.hopsworks.ai/dictionary/online-offline-feature-skew) skews in AI systems, allowing for their prevention.
Hopsworks provides support for a feature view abstraction as well as model-dependent transformations and on-demand transformations to prevent online-offline skew.

## Data Transformation Taxonomy for AI Systems

Transformation functions in an AI system can be classified into three types based on the nature of the input features they generate: [model-independent](https://www.hopsworks.ai/dictionary/model-independent-transformations), [model-dependent](https://www.hopsworks.ai/dictionary/model-dependent-transformations), and [on-demand](https://www.hopsworks.ai/dictionary/on-demand-transformation) transformations.

<figure class="hops-diagram">
<svg viewBox="0 0 1000 260" role="img" aria-label="A transformation is model-independent (data-engineering transforms like aggregations and windowed counts, producing reusable features), model-dependent (encoding, scaling and imputation parameterized by the training data, producing model-specific features), or on-demand (needing request-time data, producing on-demand features)." xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="tt-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/>
    </marker>
  </defs>
  <rect class="d-box" x="410" y="20" width="180" height="48" rx="8"/>
  <text class="d-t" x="500" y="49" text-anchor="middle">Transformation</text>

  <path class="d-flow" d="M500 68 V100 H175 V140" marker-end="url(#tt-arrow)"/>
  <path class="d-flow" d="M500 68 V140" marker-end="url(#tt-arrow)"/>
  <path class="d-flow" d="M500 68 V100 H825 V140" marker-end="url(#tt-arrow)"/>

  <rect class="d-box-own" x="40" y="140" width="270" height="48" rx="8"/>
  <text class="d-t" x="175" y="169" text-anchor="middle">Model-independent</text>
  <text class="d-t d-sub" x="175" y="212" text-anchor="middle">aggregations, windowed count, RFM</text>
  <text class="d-t d-sub" x="175" y="230" text-anchor="middle">produces reusable features</text>

  <rect class="d-box" x="365" y="140" width="270" height="48" rx="8"/>
  <text class="d-t" x="500" y="169" text-anchor="middle">Model-dependent</text>
  <text class="d-t d-sub" x="500" y="212" text-anchor="middle">encoding, scaling, imputation</text>
  <text class="d-t d-sub" x="500" y="230" text-anchor="middle">produces model-specific features</text>

  <rect class="d-box-ext" x="690" y="140" width="270" height="48" rx="8"/>
  <text class="d-t" x="825" y="169" text-anchor="middle">On-demand</text>
  <text class="d-t d-sub" x="825" y="212" text-anchor="middle">needs request-time data, computed online</text>
  <text class="d-t d-sub" x="825" y="230" text-anchor="middle">produces on-demand features</text>
</svg>
</figure>

**Model-independent transformations** create reusable features that can be utilized across one or more machine-learning models.
These transformations include techniques such as grouped aggregations (e.g., minimum, maximum, or average of a variable), windowed aggregations (e.g., the number of clicks per day), and binning to generate categorical variables.
Since the data produced by model-independent transformations are reusable, these features can be stored in a feature store.

**Model-dependent transformations** generate features specific to one model.
These include transformations that are unique to a particular model or are parameterized by the training dataset, making them model-specific.
For instance, text tokenization is a transformation required by all large language models (LLMs) but each LLM has their own (unique) tokenizer.
Other transformations, such as encoding categorical variables in a numerical representation or scaling/normalizing/standardizing numerical variables to enhance the performance of gradient-based models, are parameterized by the training dataset.
Consequently, the features produced are applicable only to the model trained using that specific training dataset.
Since these features are not reusable, there is no need to store them in a feature store.
Also, storing encoded features in a feature store leads to write amplification, as every time feature values are written to a feature group, all existing rows in the feature group have to be re-encoded (and creation of a training dataset using a subset or rows in the feature group becomes impossible as they cannot be re-encoded).

**On-demand transformations** are exclusive to [real-time AI systems](https://www.hopsworks.ai/dictionary/real-time-machine-learning), where predictions must be generated in real time based on incoming prediction requests.
On-demand transformations compute on-demand features, which usually require at least one input parameter that is only available in a prediction request for their computation.
These transformations can also combine request-time parameters with precomputed features from feature stores.
Some examples include generating *zip_codes* from latitude and longitude received in the prediction request or calculating the *time_since_last_transaction* from a transaction request.
The on-demand features produced can also be computed and [backfilled](https://www.hopsworks.ai/dictionary/backfill-features) into a feature store when the necessary historical data required for their computation becomes available.
Backfilling on-demand features into the feature store eliminates the need to recompute them when creating training data.
On-demand transformations are typically also model-independent transformations (model-dependent transformations can be applied after the on-demand transformation).

Each of these transformations is employed within specific areas in a modular AI system and can be illustrated using the figure below.

<figure class="hops-diagram">
<svg viewBox="0 0 1000 400" role="img" aria-label="The three transformation types placed across the FTI pipeline. Model-independent transformations run in the feature pipeline and produce reusable features stored in the feature store. Model-dependent transformations run in the training pipeline and, again, in the online inference pipeline. On-demand transformations run in the online inference pipeline on request-time input, and can also run in the feature pipeline to backfill. Model-dependent and on-demand transformations therefore run in more than one pipeline, which is where online-offline skew can appear." xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="tx-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/>
    </marker>
  </defs>

  <!-- legend -->
  <rect class="d-box-own" x="20" y="20" width="16" height="16" rx="3"/>
  <text class="d-t d-sub" x="44" y="33">MIT, model-independent, reusable</text>
  <rect class="d-box" x="360" y="20" width="16" height="16" rx="3"/>
  <text class="d-t d-sub" x="384" y="33">MDT, model-dependent, per model</text>
  <rect class="d-box-ext" x="700" y="20" width="16" height="16" rx="3"/>
  <text class="d-t d-sub" x="724" y="33">ODT, on-demand, request-time</text>

  <!-- feature pipeline -->
  <rect class="d-box" x="20" y="104" width="230" height="116" rx="10"/>
  <text class="d-t" x="135" y="128" text-anchor="middle">Feature pipeline</text>
  <rect class="d-box-own" x="44" y="146" width="60" height="24" rx="5"/>
  <text class="d-t d-sub" x="74" y="162" text-anchor="middle">MIT</text>
  <rect class="d-box-ext" x="120" y="146" width="106" height="24" rx="5" stroke-dasharray="4 3"/>
  <text class="d-t d-sub" x="173" y="162" text-anchor="middle">ODT (backfill)</text>
  <text class="d-t d-sub" x="135" y="200" text-anchor="middle">new and historical data</text>

  <!-- feature store -->
  <rect class="d-box-own" x="320" y="116" width="170" height="92" rx="10"/>
  <text class="d-t" x="405" y="156" text-anchor="middle">Feature store</text>
  <text class="d-t d-sub" x="405" y="176" text-anchor="middle">reusable features</text>

  <!-- training pipeline -->
  <rect class="d-box" x="570" y="80" width="230" height="90" rx="10"/>
  <text class="d-t" x="685" y="112" text-anchor="middle">Training pipeline</text>
  <rect class="d-box" x="655" y="126" width="60" height="24" rx="5"/>
  <text class="d-t d-sub" x="685" y="142" text-anchor="middle">MDT</text>

  <!-- inference pipeline -->
  <rect class="d-box" x="570" y="220" width="230" height="96" rx="10"/>
  <text class="d-t" x="685" y="250" text-anchor="middle">Online inference pipeline</text>
  <rect class="d-box-ext" x="600" y="266" width="60" height="24" rx="5"/>
  <text class="d-t d-sub" x="630" y="282" text-anchor="middle">ODT</text>
  <text class="d-t d-sub" x="676" y="282" text-anchor="middle">then</text>
  <rect class="d-box" x="710" y="266" width="60" height="24" rx="5"/>
  <text class="d-t d-sub" x="740" y="282" text-anchor="middle">MDT</text>

  <!-- prediction request -->
  <rect class="d-box-ext" x="320" y="238" width="170" height="60" rx="8"/>
  <text class="d-t" x="405" y="264" text-anchor="middle">Prediction request</text>
  <text class="d-t d-sub" x="405" y="282" text-anchor="middle">request-time input</text>

  <!-- arrows -->
  <path class="d-flow" d="M250 162 H320" marker-end="url(#tx-arrow)"/>
  <path class="d-flow" d="M490 150 H530 V125 H570" marker-end="url(#tx-arrow)"/>
  <path class="d-flow" d="M490 178 H530 V268 H570" marker-end="url(#tx-arrow)"/>
  <path class="d-flow" d="M490 268 H570" marker-end="url(#tx-arrow)"/>

  <!-- band -->
  <rect class="d-band" x="20" y="348" width="780" height="40" rx="10"/>
  <text class="d-t d-sub" x="40" y="373">MDTs and ODTs each run in more than one pipeline, which is where online-offline skew appears. Feature-view MDTs and feature-group ODTs remove it.</text>
</svg>
</figure>

Model-independent transformations are utilized exclusively in areas where new and historical data arrives, typically within feature pipelines.
Model-dependent transformations are necessary during the creation of training data, in training programs and must also be consistently applied in inference programs prior to making predictions.
On-demand transformations are primarily employed in online inference programs, though they can also be integrated into feature engineering programs to backfill data into the feature store.

The presence of model-dependent and on-demand transformations across different modules in a modular AI system introduces the potential for online-offline skew.
Hopsworks provides support for  model-dependent transformations and on-demand transformations to easily create modular skew-free AI pipelines.

## Hopsworks and the Data Transformation Taxonomy

<figure class="hops-diagram">
<svg viewBox="0 0 1000 500" role="img" aria-label="Hopsworks decomposes an AI system into three AI pipelines over a feature store and storage. The feature pipeline runs model-independent and on-demand transformations and writes to feature groups. The training and inference pipelines run model-dependent transformations. On-demand UDFs are registered on feature groups, model-dependent UDFs on feature views. The feature store is backed by external tables, HopsFS-S3, RonDB and OpenSearch." xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="dh-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/>
    </marker>
  </defs>

  <!-- band captions -->
  <text class="d-t d-cap" x="984" y="40" text-anchor="end">AI pipelines</text>
  <text class="d-t d-cap d-cap-fs" x="984" y="238" text-anchor="end">Feature store</text>
  <text class="d-t d-cap" x="984" y="404" text-anchor="end">Storage</text>

  <!-- AI pipelines -->
  <rect class="d-box" x="30" y="52" width="270" height="130" rx="10"/>
  <text class="d-t" x="165" y="76" text-anchor="middle">Feature pipeline</text>
  <rect class="d-box-own" x="54" y="90" width="222" height="28" rx="5"/>
  <text class="d-t d-sub" x="165" y="109" text-anchor="middle">Model-independent (MIT)</text>
  <rect class="d-box-ext" x="54" y="126" width="222" height="28" rx="5" stroke-dasharray="4 3"/>
  <text class="d-t d-sub" x="165" y="145" text-anchor="middle">On-demand (ODT), backfill</text>

  <rect class="d-box" x="365" y="52" width="250" height="130" rx="10"/>
  <text class="d-t" x="490" y="76" text-anchor="middle">Training pipeline</text>
  <text class="d-t d-sub" x="490" y="104" text-anchor="middle">model training</text>
  <rect class="d-box" x="400" y="120" width="180" height="28" rx="5"/>
  <text class="d-t d-sub" x="490" y="139" text-anchor="middle">Model-dependent (MDT)</text>

  <rect class="d-box" x="680" y="52" width="290" height="130" rx="10"/>
  <text class="d-t" x="825" y="76" text-anchor="middle">Online inference pipeline</text>
  <rect class="d-box-ext" x="700" y="90" width="250" height="26" rx="5"/>
  <text class="d-t d-sub" x="825" y="108" text-anchor="middle">On-demand (ODT)</text>
  <rect class="d-box" x="700" y="146" width="250" height="26" rx="5"/>
  <text class="d-t d-sub" x="825" y="164" text-anchor="middle">Model-dependent (MDT)</text>
  <text class="d-t d-sub" x="825" y="135" text-anchor="middle">model inference</text>

  <!-- feature store -->
  <rect class="d-panel-fs" x="20" y="222" width="950" height="150" rx="12"/>
  <rect class="d-box-own" x="50" y="248" width="270" height="98" rx="10"/>
  <text class="d-t" x="185" y="274" text-anchor="middle">Feature group</text>
  <rect class="d-box-ext" x="74" y="292" width="222" height="30" rx="5"/>
  <text class="d-t d-sub" x="185" y="312" text-anchor="middle">On-demand UDFs</text>

  <rect class="d-box-own" x="520" y="248" width="300" height="98" rx="10"/>
  <text class="d-t" x="670" y="274" text-anchor="middle">Feature view</text>
  <rect class="d-box" x="544" y="292" width="252" height="30" rx="5"/>
  <text class="d-t d-sub" x="670" y="312" text-anchor="middle">Model-dependent UDFs</text>

  <!-- storage -->
  <rect class="d-box-ext" x="30" y="410" width="220" height="66" rx="8"/>
  <text class="d-t" x="140" y="438" text-anchor="middle">External tables</text>
  <text class="d-t d-sub" x="140" y="457" text-anchor="middle">offline: BigQuery, Snowflake</text>
  <rect class="d-box" x="270" y="410" width="220" height="66" rx="8"/>
  <text class="d-t" x="380" y="438" text-anchor="middle">HopsFS-S3</text>
  <text class="d-t d-sub" x="380" y="457" text-anchor="middle">offline store</text>
  <rect class="d-box" x="510" y="410" width="220" height="66" rx="8"/>
  <text class="d-t" x="620" y="438" text-anchor="middle">RonDB</text>
  <text class="d-t d-sub" x="620" y="457" text-anchor="middle">online store, metastore</text>
  <rect class="d-box-ext" x="750" y="410" width="220" height="66" rx="8"/>
  <text class="d-t" x="860" y="438" text-anchor="middle">OpenSearch</text>
  <text class="d-t d-sub" x="860" y="457" text-anchor="middle">vector index, search</text>

  <!-- flows -->
  <path class="d-flow" d="M165 182 V248" marker-end="url(#dh-arrow)"/>
  <path class="d-flow" d="M320 297 H400 V182" marker-end="url(#dh-arrow)"/>
  <path class="d-flow" d="M820 297 H900 V182" marker-end="url(#dh-arrow)"/>
  <path class="d-flow" d="M320 320 H520" marker-end="url(#dh-arrow)"/>
  <text class="d-t d-sub" x="410" y="338" text-anchor="middle">reachable by graph traversal</text>
  <path class="d-flow" d="M185 372 V410"/>
  <path class="d-flow" d="M620 372 V410"/>
  <path class="d-flow" d="M860 372 V410"/>
</svg>
</figure>

In Hopsworks, an AI system is typically decomposed into different [AI pipelines](https://www.hopsworks.ai/dictionary/ai-pipelines) and usually falls into either a [feature pipeline](https://www.hopsworks.ai/dictionary/feature-pipeline), a [training pipeline](https://www.hopsworks.ai/dictionary/training-pipeline), or an [inference pipeline](https://www.hopsworks.ai/dictionary/inference-pipeline).

Hopsworks stores reusable feature data, created by model-independent transformations within the feature pipeline, into [feature groups](../fs/feature_group/fg_overview.md) (tables containing feature data in both offline and online stores).
Model-independent transformations in Hopsworks can be performed using a wide range of commonly used data engineering tools and the generated features can be seamlessly inserted into feature groups.
The figure below illustrates the different software tools supported by Hopsworks for creating reusable features through model-independent transformations.

<figure class="hops-diagram">
<svg viewBox="0 0 1000 460" role="img" aria-label="A quadrant of feature-engineering tools supported by Hopsworks, placed by streaming versus batch and by smaller versus bigger data. Streaming and smaller data: Feldera, Pathway, Bytewax, Quix streams. Streaming and bigger data: Apache Flink, Apache Beam, Apache Spark Streaming. Batch and smaller data: Pandas, Polars, DuckDB, Data Fusion. Batch and bigger data: dbt over Snowflake, BigQuery and Redshift, Apache Spark, Dask." xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="q-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/>
    </marker>
  </defs>

  <rect class="d-box" x="150" y="46" width="700" height="368" rx="12"/>
  <path class="d-flow" d="M500 46 V414"/>
  <path class="d-flow" d="M150 230 H850"/>

  <text class="d-t d-cap" x="500" y="30" text-anchor="middle">Streaming</text>
  <text class="d-t d-cap" x="500" y="446" text-anchor="middle">Batch</text>
  <text class="d-t d-cap" x="140" y="234" text-anchor="end">Smaller data</text>
  <text class="d-t d-cap" x="860" y="234" text-anchor="start">Bigger data</text>

  <text class="d-t" x="200" y="96">Feldera</text>
  <text class="d-t" x="200" y="126">Pathway</text>
  <text class="d-t" x="200" y="156">Bytewax</text>
  <text class="d-t" x="200" y="186">Quix streams</text>

  <text class="d-t" x="560" y="96">Apache Flink</text>
  <text class="d-t" x="560" y="126">Apache Beam</text>
  <text class="d-t" x="560" y="156">Apache Spark Streaming</text>

  <text class="d-t" x="200" y="290">Pandas</text>
  <text class="d-t" x="200" y="320">Polars</text>
  <text class="d-t" x="200" y="350">DuckDB</text>
  <text class="d-t" x="200" y="380">Data Fusion</text>

  <text class="d-t" x="560" y="290">dbt: Snowflake, BigQuery, Redshift</text>
  <text class="d-t" x="560" y="320">Apache Spark</text>
  <text class="d-t" x="560" y="350">Dask</text>
</svg>
</figure>

Additionally, Hopsworks provides a simple Python API to [create custom transformation functions](../../user_guides/fs/transformation_functions.md) as either Python or Pandas User-Defined Functions (UDFs).
Pandas UDFs enable the vectorized execution of transformation functions, offering significantly higher throughput compared to Python UDFs for large volumes of data.
They can also be scaled out across workers in a Spark program, allowing for scalability from gigabytes (GBs) to terabytes (TBs) or more.
However, Python UDFs can be much faster for small volumes of data, such as in the case of online inference.

Transformation functions defined in Hopsworks can then be attached to feature groups to [create on-demand transformation](../../user_guides/fs/feature_group/on_demand_transformations.md).
On-demand transformations in feature groups are executed automatically whenever data is inserted into them to compute and backfill the on-demand features into the feature group.
Backfilling on-demand features removes the need to recompute them while creating training and batch data.

Hopsworks also provides a powerful abstraction known as [feature views](../fs/feature_view/fv_overview.md), which enables feature reuse and prevents skew between training and inference pipelines.
A feature view is a meta-data-only selection of features, created from potentially different feature groups.
It includes the input and output schema required for a model.
This means that a feature view describes not only the input features but also the output targets, along with any helper columns necessary for training or inference of the model.
This allows feature views to create consistent snapshots of data for both training and inference of a model.
Additionally feature views, also compute and save statistics for the training datasets they create.

Hopsworks supports attaching transformations functions to feature views to [create model-dependent transformations](../../user_guides/fs/feature_view/model-dependent-transformations.md) that have no online-offline skew.
These transformations get access to the same training dataset statistics during both training and inference ensuring their consistency.
Additionally, feature views through lineage get access to the on-demand transformation used to create on-demand features if any are selected during the creation of the feature view.

The registration locus is the cleanest way to remember where each transformation lives: on-demand transformations are registered on feature groups, model-dependent transformations on feature views.
A Hopsworks transformation function is also mixed-mode: the same decorated Python function runs as a Pandas UDF offline, to create training data, and as a Python UDF online, to build a single feature vector, so one definition serves both pipelines with no skew.
This allows for the computation of on-demand features in real-time during online-inference.
