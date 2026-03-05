In Hopsworks, you can easily deploy models from the model registry using [KServe](https://kserve.github.io/website/latest/), the standard open-source framework for model serving on Kubernetes.
You can deploy models programmatically using the HSML library or via the UI.
A KServe model deployment can include the following components:

**`Predictor (KServe component)`**

:   A predictor runs a model server (Python, TensorFlow Serving, or vLLM) that loads a trained model, handles inference requests and returns predictions.

**`Transformer (KServe component)`**

:   A ^^pre-processing^^ and ^^post-processing^^ component that can transform model inputs before predictions are made, and predictions before these are delivered back to the client. Not available for vLLM deployments.

**`Inference Logger`**

:   Hopsworks logs inputs and outputs of transformers and predictors to a ^^Kafka topic^^ that is part of the same project as the model. Not available for vLLM deployments.

**`Inference Batcher`**

:   Inference requests can be batched to improve throughput (at the cost of slightly higher latency).

**`Istio Model Endpoint`**

:   You can publish a model over ^^REST(HTTP)^^ or ^^gRPC^^ using a Hopsworks API key, accessible via path-based routing through Istio.
    API keys have scopes to ensure the principle of least privilege access control to resources managed by Hopsworks.

    !!! warning "Host-based routing"
        The Istio Model Endpoint supports host-based routing for inference requests; however, this approach is considered legacy. Path-based routing is recommended for new deployments.

Models deployed on KServe in Hopsworks can be easily integrated with the Hopsworks Feature Store using either a Transformer or Predictor Python script, that builds the predictor's input feature vector using the application input and pre-computed features from the Feature Store.

<img src="../../../assets/images/concepts/mlops/kserve.svg">

!!! info "Model Serving Guide"
    More information can be found in the [Model Serving guide](../../user_guides/mlops/serving/index.md).

!!! tip "Python deployments"
    For deploying Python scripts without a model artifact, see the [Python Deployments](../../user_guides/projects/python-deployment/python-deployment.md) page.
