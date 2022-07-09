A prediction service is an end-to-end analytical or operational machine learning system that takes in data and outputs predictions that are consumed by users of the prediction service.

A prediction service consists of the following components:

* feature pipeline(s),
* training pipeline,
* inference pipeline (for either batch predictions or online predictions)
* a sink for predictions - either a store or a user-interface.

## Analytical ML

In the analytical ML figure below, we can see an analytical prediction service, where feature pipelines update the feature store with new feature data, running at some schedule (e.g., hourly, daily), and a batch program also runs on a schedule, reading batch scoring data from the feature store, computing predictions for that data with an embedded model, and writing those predictions to a database sink, from where the predictions are used for (predictive, prescriptive) analytical reports and/or to AI-enable operational services.

<img src="../../../assets/images/concepts/mlops/analytical-prediction-service.svg">

## Operational ML

In the operational ML figure below, we can see an operational prediction service, where feature pipelines update the feature store with new feature data, running at some schedule (e.g., streaming, hourly, daily), and the operational service sends prediction requests to a model deployed on KServe via its secured Istio endpoint. A deployed model on KServer handles the prediction request by first retrieving pre-computed features from the feature store for the given request, and then building a feature vector that is scored by the model. The prediction result is returned to the client (the operational service). KServe logs both the feature values and the prediction results back to Hopsworks for further analysis and to help create new training data.

<img src="../../../assets/images/concepts/mlops/operational-prediction-service.svg">


## MLOps Flywheel

Once you have built your analytical or operational ML system, the MLOps flywheel is the path to building a self-managing system that automatically collects and processes feature logs, prediction logs, and outcomes to help create new training data for models. This enables a ML flywheel where new training data and insights are generated from your operational or analytical ML service, by feeding logs back into the feature store. More training data enables the training of bettter models, and with better models, you should hopefully improve you operational/batch services, so that you attract more clients, who in turn produce more data for training models. And, thus, the ML flywheel is bootstrapped and leads to a virtuous cycle of more data leading to better models and more models leading to more users, who produce more data, and so on.

<img src="../../../assets/images/concepts/mlops/flywheel.svg">
