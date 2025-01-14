# Model Serving Guide

## Deployment

Assuming you have already created a model in the [Model Registry](../registry/index.md), a deployment can now be created to prepare a model artifact for this model and make it accessible for running predictions behind a REST or gRPC endpoint. Follow the [Deployment Creation Guide](deployment.md) to create a Deployment for your model.

### Predictor

Predictors are responsible for running a model server that loads a trained model, handles inference requests and returns predictions, see the [Predictor Guide](predictor.md).

### Transformer

Transformers are used to apply transformations on the model inputs before sending them to the predictor for making predictions using the model, see the [Transformer Guide](transformer.md).

### Resource Allocation

Configure the resources to be allocated for predictor and transformer in a model deployment, see the [Resource Allocation Guide](resources.md).

### Inference Batcher

Configure the predictor to batch inference requests, see the [Inference Batcher Guide](inference-batcher.md).

### Inference Logger

Configure the predictor to log inference requests and predictions, see the [Inference Logger Guide](inference-logger.md).

### Troubleshooting

Inspect the model server logs to troubleshoot your model deployments, see the [Troubleshooting Guide](troubleshooting.md).