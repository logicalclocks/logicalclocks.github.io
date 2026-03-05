# Model Serving Guide

## Deployment

Assuming you have already created a model in the [Model Registry](../registry/index.md), a deployment can now be created to prepare a model artifact for this model and make it accessible for running predictions behind a REST or gRPC endpoint.

Refer to the [Deployment Creation Guide](deployment.md) for step-by-step instructions on creating a deployment for your model. For details on monitoring the status and lifecycle of an existing deployment, see the [Deployment State Guide](deployment-state.md).

!!! tip "Python deployments"
    If you want to deploy a Python script without a model artifact, see the [Python Deployments](../../projects/python-deployment/python-deployment.md) page.

### Predictor (KServe component)

Predictors are responsible for running a model server that loads a trained model, handles inference requests and returns predictions, see the [Predictor Guide](predictor.md).

### Transformer (KServe component)

Transformers are used to apply transformations on the model inputs before sending them to the predictor for making predictions using the model, see the [Transformer Guide](transformer.md).

### Inference Batcher

Configure the predictor to batch inference requests, see the [Inference Batcher Guide](inference-batcher.md).

### Inference Logger

Configure the predictor to log inference requests and predictions, see the [Inference Logger Guide](inference-logger.md).

### Resources

Configure the resources to be allocated for predictor and transformer in a model deployment, see the [Resources Guide](resources.md).

### Autoscaling

Configure autoscaling for your model deployment, including scale-to-zero, scale metrics and scaling parameters, see the [Autoscaling Guide](autoscaling.md).

### Scheduling

!!! info "Kueue is required"
    This feature requires Kueue to be enabled in your cluster. If Kueue is not available, queue and topology options will not be accessible.

Configure scheduling for your model deployment using Kueue queues, see the [Scheduling Guide](scheduling.md).

### API Protocol

Choose between REST and gRPC API protocols for your model deployment, see the [API Protocol Guide](api-protocol.md).

### REST API

Send inference requests to deployed models using REST API, see the [REST API Guide](rest-api.md).

### Troubleshooting

Inspect the model server logs to troubleshoot your model deployments, see the [Troubleshooting Guide](troubleshooting.md).

### External access

Grant users authenticated by an external Identity Provider access to model deployments, see the [External Access Guide](external-access.md).
