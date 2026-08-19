# AI Systems

An AI system is a set of independent feature pipelines, training pipelines, and inference pipelines that are connected via a feature store and model registry.
Each pipeline is a separate program with its own inputs and outputs, and the shared data layer is what lets them be developed, run, and scaled independently.

An AI system is defined by how it computes its predictions, not by the type of application that consumes them.
The inference pipeline determines the class of AI system you are building.
There are four classes:

- **Real-time (interactive)**: a client sends a prediction request and an online inference pipeline computes and returns a prediction with low latency.
- **Batch**: an inference pipeline runs on a schedule, scores a set of entities, and writes the predictions to an inference store.
- **Stream processing**: an inference pipeline computes predictions continuously over an event stream.
- **Agentic workflows**: an LLM-driven control flow decides which steps to run, retrieving the context and features it needs from the feature store. See [Agents and LLM Systems](agents.md).

Whatever the class, an AI system is composed of the same parts:

- one or more feature pipeline(s) that keep the feature store up to date,
- a training pipeline that produces a model in the model registry,
- an inference pipeline that reads features and computes predictions,
- a sink for the predictions, either an inference store or a user interface.

The two figures below illustrate the two most common classes, batch and real-time.

## Batch AI systems

In the figure below, feature pipelines update the feature store with new feature data on a schedule (e.g., hourly, daily).
A batch inference pipeline also runs on a schedule, reads batch scoring data from the feature store, computes predictions with an embedded model, and writes those predictions to an inference store.
The inference store is any data store that holds the predictions from batch inference pipelines.
From there, the predictions are consumed by (predictive, prescriptive) analytical reports and/or to AI-enable operational services.

--8<-- "concepts/mlops/prediction_services/batch-ai-systems.html"

## Real-time AI systems

In the figure below, feature pipelines update the feature store with new feature data on a schedule (e.g., streaming, hourly, daily), and the operational service sends prediction requests to a model deployed on KServe via its secured Istio endpoint.
A deployed model on KServe handles the prediction request by first retrieving pre-computed features from the feature store for the given request, and then building a feature vector that is scored by the model.
The prediction result is returned to the client (the operational service).
KServe logs both the feature values and the prediction results back to Hopsworks for further analysis and to help create new training data.

--8<-- "concepts/mlops/prediction_services/real-time-ai-systems.html"

## MLOps Flywheel

Once you have built your batch or real-time AI system, the MLOps flywheel is the path to building a self-managing system that automatically collects and processes feature logs, prediction logs, and outcomes to help create new training data for models.
This enables a ML flywheel where new training data and insights are generated from your AI system, by feeding logs back into the feature store.
More training data enables the training of better models, and with better models, you should hopefully improve your operational/batch services, so that you attract more clients, who in turn produce more data for training models.
And, thus, the ML flywheel is bootstrapped and leads to a virtuous cycle of more data leading to better models and more models leading to more users, who produce more data, and so on.

--8<-- "concepts/mlops/prediction_services/mlops-flywheel.html"
