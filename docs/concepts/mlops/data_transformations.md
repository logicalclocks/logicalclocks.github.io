# Data Transformations

[Data transformations](https://www.hopsworks.ai/dictionary/data-transformation) are integral to all AI applications.
Data transformations produce new features that can enhance the performance of an AI application.
However, [not all transformations in an AI application are equivalent](https://www.hopsworks.ai/post/a-taxonomy-for-data-transformations-in-ai-systems).

Transformations like binning and aggregations typically create reusable features, while transformations like one-hot encoding, scaling and normalization often produce model-specific features.
Additionally, in real-time AI systems, some features can only be computed during inference when the request is received, as they need request-time parameters to be computed.

![Types of features](../../assets/images/concepts/mlops/transformation-features.jpg)

This classification of features can be used to create a taxonomy for data transformation that would apply to any scalable and modular AI system that aims to reuse features.
The taxonomy helps identify which classes of data transformation can cause [online-offline](https://www.hopsworks.ai/dictionary/online-offline-feature-skew) skews in AI systems, allowing for their prevention.
Hopsworks provides support for a feature view abstraction as well as model-dependent transformations and on-demand transformations to prevent online-offline skew.

## Data Transformation Taxonomy for AI Systems

Transformation functions in an AI system can be classified into three types based on the nature of the input features they generate: [model-independent](https://www.hopsworks.ai/dictionary/model-independent-transformations), [model-dependent](https://www.hopsworks.ai/dictionary/model-dependent-transformations), and [on-demand](https://www.hopsworks.ai/dictionary/on-demand-transformation) transformations.

![Types of transformations](../../assets/images/concepts/mlops/taxonomy-transformations.jpg)

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
![Types of transformations in modular AI Pipeline](../../assets/images/concepts/mlops/transformation-in-modular-AI-pipeline.jpg)

Model-independent transformations are utilized exclusively in areas where new and historical data arrives, typically within feature pipelines.
Model-dependent transformations are necessary during the creation of training data, in training programs and must also be consistently applied in inference programs prior to making predictions.
On-demand transformations are primarily employed in online inference programs, though they can also be integrated into feature engineering programs to backfill data into the feature store.

The presence of model-dependent and on-demand transformations across different modules in a modular AI system introduces the potential for online-offline skew.
Hopsworks provides support for  model-dependent transformations and on-demand transformations to easily create modular skew-free AI pipelines.

## Hopsworks and the Data Transformation Taxonomy

![Data transformations Hopsworks](../../assets/images/concepts/mlops/data-transformations-hopsworks.jpg)

In Hopsworks, an AI system is typically decomposed into different [AI pipelines](https://www.hopsworks.ai/dictionary/ai-pipelines) and usually falls into either a [feature pipeline](https://www.hopsworks.ai/dictionary/feature-pipeline), a [training pipeline](https://www.hopsworks.ai/dictionary/training-pipeline), or an [inference pipeline](https://www.hopsworks.ai/dictionary/inference-pipeline).

Hopsworks stores reusable feature data, created by model-independent transformations within the feature pipeline, into [feature groups](../fs/feature_group/fg_overview.md) (tables containing feature data in both offline and online stores).
Model-independent transformations in Hopsworks can be performed using a wide range of commonly used data engineering tools and the generated features can be seamlessly inserted into feature groups.
The figure below illustrates the different software tools supported by Hopsworks for creating reusable features through model-independent transformations.

![Supported feature engineering tools](../../assets/images/concepts/mlops/supported-feature-engineering-tools.jpg)

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
This allows for the computation of on-demand features in real-time during online-inference.
