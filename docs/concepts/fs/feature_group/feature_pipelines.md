A feature pipeline is a program that orchestrates the execution of a dataflow graph of data validation, aggregation, dimensionality reduction, transformation, and other feature engineering steps on input data to create and/or update feature data. With HSFS, you can write feature pipelines in different languages as shown in the figure below. 

<img src="../../../../assets/images/concepts/fs/feature-pipelines.svg">

### Data Sources
Your feature pipeline needs to connect to some (external) data source to read the data to be processed. Python, Spark, and Flink have connectors to a huge number of different data sources, while SQL feature pipelines are often restricted to a single data source (for example, your connector to SnowFlake only runs SQL on SnowFlake). SparkSQL, in contrast, can be used over tables that originate in different  data sources.

### Data Validation
In order to be able to train and serve models that you can rely on, you need clean, high quality features. Data validation operations include removing bad data, removing or imputing missing values, and identifying problems such as feature shift. HSFS supports Great Expectations to specify data validation rules that are executed in the client before features are written to the Feature Store. The validation results are collected and shown in Hopsworks.

### Aggregations

Aggregations are used to summarize large datasets into more concise, signal-rich features. Popular aggregations include count(), sum(), mean(), median(), stddev(), min(), and max(). These aggregations produce a single number (a numerical feature) that captures information about a potentially large dataset. Both numerical and categorical features are often transformed before being used to train or serve models.

### Dimensionality Reduction
If input data is impractically large or if it has a signnificant amount of redundancy, it can often be transformed into a reduced set of features with dimensionality reduction (often called feature extraction). Popular dimensionality algorithms include embedding algorithms, PCA, and TSNE.

### Transformations
Transformations are covered in more detail in [training/inference pipelines](../feature_view/training_inference_pipelines.md), as transformations typically happen after the feature store. If you store transformed features in feature groups, the feature data is no longer useful for EDA (as it near to impossible for Data Scientists to understand the transformed values). It also makes it impossible for inference pipelines to log untransformed feature values and predictions for an operational model. There is one use case for storing transformed features in feature groups - when you need to have ultra low latency when reading precomputed features (and online transformations when reading features add too much latency for your use case). The figure below shows to include transformations in your feature pipelines. 

<img src="../../../../assets/images/concepts/fs/feature-pipelines-with-transformations.svg">

### Feature Engineering in Python
Python is the most widely used framework for feature engineering due to its extensive library support for aggregations (Pandas), data validation (Great Expectations), and dimensionality reduction (embeddings, PCA), and transformations (in Scikit-Learn, TensorFlow, PyTorch). Python also supports open-source feature engineering frameworks used for automated feature engineering, such as [featuretools](https://www.featuretools.com/) that supports relational and temporal sources.


### Feature Engineering in Spark/PySpark

Spark is popular as a feature engineering framework as it can scale to process larger volumes of data than Python, and provides native support for aggregations, and it supports many of the same data validation (Great Expectations), and dimensionality reduction algorithms (embeddings, PCA) as Python. Spark also has native support for transformations, which are useful for analytical models (batch scoring), but less useful for operational models, where online transformations are required, and Spark environments are less common. Online model serving environments typically only support online transformations in Python.

### Feature Engineering in SQL

SQL has grown in popularity for performing heavy lifting in feature pipelines - computing aggregates on data - when the input data already resides in a data warehouse. Data warehouses also support data validation, for example, through Great Expectations in DBT. However, SQL is not mature as a platform for transformations and dimensionality reductions, where UDFs are applied row-wise.


You can do aggregation in SQL for data in your data warehouse or database.

### Feature Engineering in Flink

Flink is used for feature engineering when you need very fresh features computed in real-time. Flink pipelines are often written in Java, and provide native support for aggregations, with dimensionality reduction algorithms and transformations also possible in Java.

