# Model Serving

In Hopsworks, you can easily deploy models from the model registry using [KServe](https://kserve.github.io/website/latest/), the standard open-source framework for model serving on Kubernetes.
You rarely deploy just a model.
What you deploy is an online inference pipeline, of which the model is one part, alongside feature retrieval, transformations, and logging.
You can deploy models programmatically using [`Model.deploy`][hsml.model.Model.deploy] or via the UI.
A KServe model deployment can include the following components:

**`Predictor (KServe component)`**

:   A predictor runs a model server (Python, TensorFlow Serving, or vLLM) that loads a trained model, handles inference requests and returns predictions.

**`Transformer (KServe component)`**

:   A ^^pre-processing^^ and ^^post-processing^^ component that can transform model inputs before predictions are made, and predictions before these are delivered back to the client.
    Not available for vLLM deployments.

**`Inference Logger`**

:   Hopsworks logs inputs and outputs of transformers and predictors to a ^^Kafka topic^^ that is part of the same project as the model.
    This is for storing inference requests and responses for later consumption and analysis, and is separate from the feature logging that powers [Model Monitoring](model_monitoring.md).
    Not available for vLLM deployments.

**`Inference Batcher`**

:   Inference requests can be batched to improve throughput (at the cost of slightly higher latency).

**`Istio Model Endpoint`**

:   You can publish a model over REST(HTTP) or gRPC using a Hopsworks API key, accessible via **path-based routing** through Istio.
    API keys have scopes to ensure the principle of least privilege access control to resources managed by Hopsworks.
    For more details on path-based routing of requests through Istio, see [REST API Guide](../../user_guides/mlops/serving/rest-api.md).

    !!! warning "Host-based routing"
        The Istio Model Endpoint supports host-based routing for inference requests; however, this approach is considered legacy.
        Path-based routing is recommended for new deployments.

Models deployed on KServe in Hopsworks can be easily integrated with the Hopsworks Feature Store using either a Transformer or Predictor Python script, that builds the predictor's input feature vector using the application input and pre-computed features from the Feature Store.

<img src="../../../assets/images/concepts/mlops/kserve.svg">

## Deployment API

The deployment API is the interface to the online inference pipeline that clients send prediction requests to.
It is the deployment API, not the model signature, that clients should version against.
The model signature (the input and output schema of the model) changes whenever you retrain with a different set of features, so coupling clients to it turns every model update into a breaking change.
The deployment API is a stable contract that can stay the same across model versions.

A client request to the deployment API carries two kinds of parameter:

- **serving keys**: the entity IDs used to retrieve pre-computed features from the feature store.
- **request parameters**: values known only at request time, sent in the request and used to build the feature vector or to compute on-demand features.

Because clients depend on it, a deployment API should carry an SLO, typically a p99 latency target for online predictions.

!!! info "Model Serving Guide"
    More information can be found in the [Model Serving guide](../../user_guides/mlops/serving/index.md).

!!! tip "Python deployments"
    For deploying Python scripts without a model artifact, see the [Python Deployments](../../user_guides/projects/python-deployment/python-deployment.md) page.
