Hopsworks supports running model training pipelines on any Python environment, whether on an external Python client or on a Hopsworks cluster. The outputs of a training pipeline are typically experiment results, including logs, and possibly a trained model. You can plugin your own experimentation tracking platform or model registry, or you can use Hopsworks.

### Training Pipelines on Hopsworks

If you train models with Hopsworks, you can setup CI/CD pipelines as shown below, where the experiments are tracked by Hopsworks, and any model created is published to a model registry. Each project has its own private model registry, so when you are working in a development project, you typically publish models to your project's private development registry, and if all model validation tests pass, and the model performance is good enough, the same training pipeline can be submitted via a CI/CD pipeline (e.g., Github push request) to a staging project, and the same procedure can be repeated to push the training pipeline to a production project.

<img src="../../../assets/images/concepts/mlops/training-pipeline.svg">

Hopsworks [Model Registry](registry.md) and [Model Serving](kserve.md) capabilities can then be used to build a batch or online prediction service using the model.
