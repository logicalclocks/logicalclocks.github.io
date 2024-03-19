In Hopsworks, you can easily deploy models from the model registry in KServe or in Docker containers (for Hopsworks Community). KServe is the defacto open-source framework for model serving on Kubernetes. You can deploy models in either programs, using the HSML library, or in the UI. A KServe model deployment can include the following components:

**`Transformer`**

:   A ^^pre-processing^^ and ^^post-processing^^ component that can transform model inputs before predictions are made, and predictions before these are delivered back to the client.
    

**`Predictor`**

:   A predictor is a ML model in a Python object that takes a feature vector as input and returns a prediction as output.

**`Inference Logger`**

:   Hopsworks logs inputs and outputs of transformers and predictors to a ^^Kafka topic^^ that is part of the same project as the model.

**`Inference Batcher`**

:   Inference requests can be batched to improve throughput (at the cost of slightly higher latency).

**`Istio Model Endpoint`**

:   You can publish a model over ^^REST(HTTP)^^ or ^^gRPC^^ using a Hopsworks API key. API keys have scopes to ensure the principle of least privilege access control to resources managed by Hopsworks.

Models deployed on KServe in Hopsworks can be easily integrated with the Hopsworks Feature Store using either a Transformer or Predictor Python script, that builds the predictor's input feature vector using the application input and pre-computed features from the Feature Store.

<img src="../../../assets/images/concepts/mlops/kserve.svg">

!!! info "Model Serving Guide"
    More information can be found in the [Model Serving guide](../../user_guides/mlops/serving/index.md).