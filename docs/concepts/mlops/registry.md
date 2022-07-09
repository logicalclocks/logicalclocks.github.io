Hopsworks Model Registry is designed with specific support for KServe and MLOps, through versioning. It enables developers to publish, test, monitor, govern and share models for collaboration with other teams. The model registry is where developers publish their models during the experimentation phase. The model registry can also be used to share models with the team and stakeholders.

Like other project-based multi-tenant services in Hopsworks, a model registry is private to a project. That means you can easily add a development, staging, and production model registry to a cluster, and implement CI/CD processes for transitioning a model from development to staging to production.

The model registry for KServe's capability are shown in the diagram below:

<img src="../../../assets/images/concepts/mlops/model-registry.svg">

The model registry centralizes model management, enabling models to be securely accessed and governed. Models are more than just the model itself - the registry also stores sample data for testsing, configuration information, provenance information, environment variables, links to the code used to generate the model, the model version, and tags/descriptions). When you save a model, you can also save model metrics with the model, enabling users to understand, for example, performance of the model on test (or unseen) data.

## Model Package
A ML model consists of a number of different components in a model package:
 - Model Input/Output Schema
 - Model artifacts
 - Model version information
 - Model format (based on the ML framework used to train the model - e.g., .pkl or .tb files)

You can also optionally include in your packaged model:
 - Sample data (used to test the model  in KServe)
 - The source notebook/program/experiment used to create the model


