---
description: Documentation on how to deploy a feature view as an online endpoint that returns transformed feature vectors.
---

# How To Deploy A Feature View { #feature-view-deployment }

## Introduction

In this guide, you will learn how to serve a feature view without a model.
A feature view deployment answers a prediction-style request with the transformed feature vector a model would receive.
It uses the same request contract, feature lookup, transformations, logging, and monitoring as a model deployment served by the default predictor.
See the [Deployment Schema Guide][deployment-schema] for the request contract and the error codes, which are shared with model deployments.

Use it to serve features to a model that runs outside Hopsworks, to test transformations online before a model exists, or to give a feature vector API to another team.

!!! warning "Serving identity"
    The deployment looks up features as the project's serving identity, not as the caller.
    Anyone allowed to call the deployment can obtain the transformed features of any entity the feature view can serve.

## Code

### Step 1: Connect to Hopsworks

=== "Python"

    ```python
    import hopsworks


    project = hopsworks.login()

    fs = project.get_feature_store()
    ```

### Step 2: Pin a training dataset

Model-dependent transformations that need statistics, such as `min_max_scaler`, take them from a training dataset.
The deployment uses the training dataset you last read or created in this session, or the one you pass to `deploy()`.

=== "Python"

    ```python
    feature_view = fs.get_feature_view("transactions", version=1)

    # reading or creating a training dataset records it as the one to serve with
    X_train, X_test, y_train, y_test = feature_view.train_test_split(test_size=0.2)
    ```

If the feature view has such a transformation and no training dataset was read or created, `deploy()` refuses and names the transformation, because its statistics cannot be computed.

### Step 3: Deploy the feature view

=== "Python"

    ```python
    deployment = feature_view.deploy(
        name="transactionsfv",
        passed_features=["amount"],  # features the client sends with each request
    )
    deployment.start(await_running=600)
    ```

The deployment name defaults to the feature view name and version without special characters.
The client publishes the deployment schema before the deployment is created, so `deployment.schema` describes the request immediately:

=== "Python"

    ```python
    deployment.schema.describe()
    print(deployment.schema.names)  # the order of positional rows
    ```

### Step 4: Request feature vectors

Each row carries the serving keys, the passed features, the request parameters of on-demand transformations, and any extra logging columns.
The response carries one transformed vector per row and the column names.

=== "Python"

    ```python
    response = deployment.predict(
        inputs=[{"cc_num": 4473593503484549, "amount": 12.5}]
    )
    print(response["columns"])  # ["amount_scaled", "age_days", ...]
    print(response["predictions"])  # [[0.31, -1.2, ...]]
    ```

Rows can also be arrays in `deployment.schema.names` order.
When every stored feature of the view is passed, the schema has no serving keys and the deployment only computes the on-demand features and applies the model-dependent transformations; see [Deployments without lookups][deployment-schema-no-lookup].
Invalid rows are refused before any feature is read; see [Errors][deployment-schema-errors].

### Step 5: Inspect the deployment

=== "Python"

    ```python
    print(deployment.has_feature_view)  # True
    print(deployment.feature_view_name, deployment.feature_view_version)
    print(deployment.training_dataset_version)  # the pinned version
    feature_view = deployment.get_feature_view()  # the FeatureView object
    print(deployment.get_model())  # None
    ```

## Feature logging

When logging is enabled on the feature view, every request is logged with the untransformed and transformed features, the request id, the training dataset version, and the reserved deployment columns `deployment_name`, `deployment_version`, `deployment_schema_id`, and `request_row`, when the logging feature group declares them.
The model columns of the log are null, because there is no model.
See [Feature logging in the Deployment Schema Guide][deployment-schema-feature-logging] for how requests are logged and for the reserved columns.

=== "Python"

    ```python
    feature_view.enable_logging(
        extra_log_columns=[
            {"name": "deployment_name", "type": "string"},
            {"name": "deployment_version", "type": "int"},
            {"name": "deployment_schema_id", "type": "string"},
            {"name": "request_row", "type": "int"},
        ]
    )
    deployment = feature_view.deploy(name="transactionsfv", passed_features=["amount"])
    ```

## Feature monitoring

A feature view deployment has no model, so `deployment.create_model_monitoring()` raises.
Use `deployment.create_feature_monitoring()`, which attaches a feature monitoring configuration to the logging feature group of the view:

=== "Python"

    ```python
    config = (
        deployment.create_feature_monitoring(name="amount_drift")
        .with_detection_window(time_offset="1d", window_length="1d")
        .with_reference_window(time_offset="8d", window_length="7d")
        .compare_on(metric="MEAN", threshold=10.0, feature_name="amount")
        .save()
    )
    deployment.get_monitoring_configs()
    ```

A distribution comparison (`compare_on_distribution`) over rolling windows needs KLL statistics on the logging feature group, which it does not keep by default; enable them in the logging feature group's statistics configuration first.

Two deployments of the same feature view version log to the same feature group; their rows are told apart by the reserved deployment columns, but a monitoring configuration sees both.
Deploy a separate version of the feature view when the statistics of one deployment must not include another's traffic.

## Custom predictor script

To post-process the vectors or to change how they are looked up, subclass the default predictor and pass the script to `deploy()`.
The script must end with the hand-over to the serving wrapper:

=== "Python"

    ```python
    from hsml.deployment.default_predictor import DefaultPredict, run_kserve_wrapper


    class Predict(DefaultPredict):
        def model_predict(self, feature_vectors):
            # a feature view deployment has no model: return the vectors
            return feature_vectors.round(3)


    if __name__ == "__main__":
        run_kserve_wrapper()
    ```

Backends that support the `SERVING_SCRIPT_KIND=predictor` marker set by `deploy()` start the serving wrapper directly and never run the `__main__` block.
Older backends start the script with `python`, and the block hands over to the wrapper.
`deploy(script_file=...)` refuses a local script without it; a script already in HopsFS is not checked client-side.

## REST access

The deployment answers on the KServe V1 route of the Istio ingress, `<base_url>/v1/models/<deployment_name>:predict`, and through the Hopsworks REST API at `/project/<project_id>/inference/serving/<deployment_name>:predict`.
See the [REST API Guide][hopsworks-model-serving-rest-api] for authentication and the base URL.
`deployment.get_inference_url()` returns the Istio URL, or `None` when the Istio ingress is not configured for external access.
Use the Hopsworks REST API path above when it does.

## CLI

```bash
hops fv deploy transactions --passed-feature amount
hops deployment schema transactionsfv --openapi
```

## API Reference

`hsfs.feature_view.FeatureView.deploy`

[`Deployment`][hsml.deployment.deployment.Deployment]
