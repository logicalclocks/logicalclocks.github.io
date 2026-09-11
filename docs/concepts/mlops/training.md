# Model Training

A training pipeline is a program that orchestrates the training of a machine learning model, reading features and labels from the feature store as training data.
Hopsworks supports running model training pipelines on any Python environment, whether on an external Python client or on a Hopsworks cluster.
The outputs of a training pipeline are typically experiment results, including logs, and possibly a trained model.
You can plugin your own experimentation tracking platform or model registry, or you can use Hopsworks.

A training pipeline typically runs five steps: select a feature view and a training dataset version, train the model, evaluate it, validate it, and register it in the model registry if it passes.

## Evaluation and validation

Model evaluation and model validation are not the same thing.
Evaluation measures the model's performance on a held-out test set, using metrics such as accuracy or AUC.
Validation is a pass/fail gate: the model is run against evaluation data, including bias slices of the holdout built with feature-view filters and training helper columns (a column such as gender used to slice results but dropped before training), and only a model that passes is registered.
The output of validation is a model validation scorecard, and it is what decides whether the model reaches the registry.

## Training Pipelines on Hopsworks

If you train models with Hopsworks, you can setup CI/CD pipelines as shown below, where the experiments are tracked by Hopsworks, and any model created is published to a model registry.
Each project has its own private model registry, so when you are working in a development project, you typically publish models to your project's private development registry, and if all model validation tests pass, and the model performance is good enough, the same training pipeline can be submitted via a CI/CD pipeline (e.g., GitHub push request) to a staging project, and the same procedure can be repeated to push the training pipeline to a production project.

--8<-- "concepts/mlops/training/training-pipelines-on-hopsworks.html"

Hopsworks [Model Registry](registry.md) and [Model Serving](serving.md) capabilities can then be used to build a batch or online prediction service using the model.
