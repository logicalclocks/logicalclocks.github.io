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

<figure class="hops-diagram">
<svg viewBox="0 0 1000 630" role="img" aria-label="A KServe deployment where a device prediction request passes through Istio to a transformer that builds a feature vector from client input and feature store lookups, then a predictor returns predictions, while inference is logged through Kafka to the feature store and metrics go to Prometheus." xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="kserve-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/></marker></defs>

  <!-- deployment panel -->
  <rect class="d-panel-fs" x="280" y="60" width="680" height="350" rx="14"/>
  <text class="d-cap d-cap-fs" x="296" y="52">KServe deployment</text>

  <!-- client -->
  <text class="d-sub" x="105" y="200" text-anchor="middle">1. Predict: {'id': 1234,</text>
  <text class="d-sub" x="105" y="214" text-anchor="middle">'device': 'iphone'}</text>
  <rect class="d-box-ext" x="40" y="228" width="130" height="60" rx="8"/>
  <text class="d-t" x="105" y="263" text-anchor="middle">devices</text>

  <!-- istio gateway -->
  <rect class="d-box" x="200" y="234" width="64" height="48" rx="8"/>
  <text class="d-sub" x="232" y="255" text-anchor="middle">Istio</text>
  <text class="d-sub" x="232" y="270" text-anchor="middle">https</text>
  <path class="d-flow" d="M170 258 H200" marker-end="url(#kserve-arrow)"/>
  <path class="d-flow" d="M264 258 H300" marker-end="url(#kserve-arrow)"/>

  <!-- transformer -->
  <rect class="d-box" x="300" y="100" width="290" height="290" rx="10"/>
  <text class="d-t" x="445" y="128" text-anchor="middle">Transformer</text>
  <text class="d-sub" x="445" y="146" text-anchor="middle">build-feature-vector.py</text>
  <text class="d-sub" x="320" y="176">feature_view</text>
  <rect class="d-box-own" x="318" y="184" width="254" height="196" rx="8"/>
  <text class="d-sub" x="330" y="208">Feature</text>
  <text class="d-sub" x="462" y="208">Feature Origin</text>
  <path class="d-flow" d="M452 190 V374"/>
  <path class="d-flow" d="M324 220 H566"/>
  <text class="d-sub" x="330" y="246">device: iphone</text>
  <text class="d-sub" x="462" y="246">client</text>
  <path class="d-flow" d="M324 264 H566"/>
  <text class="d-sub" x="330" y="292">age: ?</text>
  <text class="d-sub" x="462" y="292">feature-store</text>
  <path class="d-flow" d="M324 314 H566"/>
  <text class="d-sub" x="330" y="348">spend-7-days: ?</text>
  <text class="d-sub" x="462" y="348">feature-store</text>

  <!-- predictor -->
  <rect class="d-box" x="690" y="100" width="250" height="290" rx="10"/>
  <text class="d-t" x="815" y="128" text-anchor="middle">Predictor</text>
  <text class="d-sub" x="815" y="146" text-anchor="middle">predictor.py</text>
  <text class="d-sub" x="815" y="212" text-anchor="middle">PyTorch</text>
  <text class="d-sub" x="815" y="242" text-anchor="middle">TensorFlow</text>
  <text class="d-sub" x="815" y="272" text-anchor="middle">scikit-learn</text>
  <text class="d-sub" x="815" y="302" text-anchor="middle">XGBoost</text>

  <path class="d-flow" d="M590 252 H690" marker-end="url(#kserve-arrow)"/>
  <text class="d-sub" x="640" y="242" text-anchor="middle">3. model.predict()</text>

  <!-- inference logging: transformer -> logs -> kafka -> feature store -->
  <path class="d-flow" d="M445 390 V440 H405 V470" marker-end="url(#kserve-arrow)"/>
  <rect class="d-box" x="300" y="470" width="210" height="58" rx="8" stroke-dasharray="4 4"/>
  <text class="d-sub" x="405" y="494" text-anchor="middle">Logs: Inputs, Transformed Inputs,</text>
  <text class="d-sub" x="405" y="512" text-anchor="middle">Predictions</text>
  <path class="d-flow" d="M405 528 V544 H385 V560" marker-end="url(#kserve-arrow)"/>
  <rect class="d-box-ext" x="310" y="560" width="150" height="44" rx="8"/>
  <text class="d-t" x="385" y="587" text-anchor="middle">Kafka</text>
  <path class="d-flow" d="M460 582 H520 V536 H560" marker-end="url(#kserve-arrow)"/>

  <!-- feature store -->
  <rect class="d-box-own" x="560" y="500" width="210" height="72" rx="10"/>
  <text class="d-t" x="665" y="542" text-anchor="middle">Feature Store</text>

  <!-- feature retrieval -->
  <path class="d-flow" d="M560 390 V470 H640 V500" stroke-dasharray="4 4" marker-end="url(#kserve-arrow)"/>
  <text class="d-sub" x="690" y="460" text-anchor="middle">2. get_feature_vector({'id': 1234}, passed={'device': 'iphone'})</text>

  <!-- metrics -->
  <path class="d-flow" d="M815 390 V440 H875 V470" stroke-dasharray="4 4" marker-end="url(#kserve-arrow)"/>
  <rect class="d-box" x="810" y="470" width="130" height="44" rx="8" stroke-dasharray="4 4"/>
  <text class="d-t" x="875" y="497" text-anchor="middle">Metrics</text>
  <path class="d-flow" d="M875 514 V555" stroke-dasharray="4 4" marker-end="url(#kserve-arrow)"/>
  <rect class="d-box-ext" x="810" y="555" width="130" height="48" rx="8"/>
  <text class="d-t" x="875" y="584" text-anchor="middle">Prometheus</text>
</svg>
</figure>

## Deployment API

The deployment API is the interface to the online inference pipeline that clients send prediction requests to.
It is the deployment API, not the model signature, that clients should version against.
The model signature (the input and output schema of the model) changes whenever you retrain with a different set of features, so coupling clients to it turns every model update into a breaking change.
The deployment API is a stable contract that can stay the same across model versions.

A client request to the deployment API carries two kinds of parameter:

- **serving keys**: the entity IDs used to retrieve pre-computed features from the feature store.
- **request parameters**: values known only at request time, sent in the request and used to build the feature vector or to compute on-demand features.

Because clients depend on it, a deployment API should carry an SLO, typically a p99 latency target for online predictions.

## Testing model deployments

Two release-safety mechanisms are often confused, because they test different things.
A blue/green test tests the correctness and performance of the model deployment directly, running the new deployment alongside the old one so clients can be switched over with no risk.
An A/B test does not test the deployment; it tests the model's effect on the application, measured against an application KPI, to decide whether the new model actually makes the product better.

!!! info "Model Serving Guide"
    More information can be found in the [Model Serving guide](../../user_guides/mlops/serving/index.md).

!!! tip "Python deployments"
    For deploying Python scripts without a model artifact, see the [Python Deployments](../../user_guides/projects/python-deployment/python-deployment.md) page.
