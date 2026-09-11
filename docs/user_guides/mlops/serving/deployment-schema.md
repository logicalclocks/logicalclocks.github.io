---
description: Documentation on the deployment schema, the request contract of a model deployment, and the default predictor that serves a model without a predictor script.
---

# How To Use A Deployment Schema { #deployment-schema }

## Introduction

In this guide, you will learn how a deployment describes the prediction requests it accepts, how clients read that contract, and how to serve a model without writing a predictor script.

A deployment schema lists the fields a client sends with each request, with their types, nullability, and order, plus the shape of the response.
It is inferred from the feature view the model was registered with: the serving keys, the features you pass with the request, the request parameters of on-demand transformations, and the extra columns of feature logging.
It is published as a JSON Schema and an OpenAPI document, so clients in any language can validate requests before sending them.
Every REST V1 request is validated in the pod before any predictor code runs, and rejected with a structured error when it does not match.
Enforcement covers the KServe REST V1 protocol only: a gRPC deployment is served without it, and the pod logs a warning at startup.

The **default predictor** is the library class that serves such a deployment: it looks up and transforms the features by serving key, runs the model, and logs the request when the feature view has logging enabled.
A [feature view can be deployed on its own][feature-view-deployment] with the same class and the same contract, returning the transformed feature vector instead of a prediction.

## Code

### Step 1: Connect to Hopsworks

=== "Python"

    ```python
    import hopsworks


    project = hopsworks.login()

    fs = project.get_feature_store()
    mr = project.get_model_registry()
    ```

### Step 2: Register the model with its feature view

Register the model with `feature_view=` so the deployment knows where its features come from.
The training dataset version is taken from the training dataset you last read or created with that feature view in this session, and the model schema is inferred from the feature view's training dataset schema.

=== "Python"

    ```python
    feature_view = fs.get_feature_view("transactions", version=1)
    X_train, X_test, y_train, y_test = feature_view.train_test_split(test_size=0.2)

    # ... train and pickle the model into model_dir ...

    model = mr.python.create_model(
        name="fraud",
        feature_view=feature_view,
    )
    model.save("model_dir")
    ```

The default predictor loads a single `.pkl`, `.pickle`, or `.joblib` file from the model directory.

### Step 3: Deploy without a predictor script

=== "Python"

    ```python
    deployment = model.deploy(
        name="fraud",
        passed_features=["amount"],  # features the client sends with each request
    )
    deployment.start(await_running=600)
    ```

The default predictor is used when the model is a Python model registered with a feature view, no `script_file` or transformer is given, and the deployment uses KServe over REST.
Pass `default_predictor=True` to force it, for instance for a scikit-learn model, or `default_predictor=False` to keep the plain model server.

At pod start the predictor checks that every input column of the model schema is served by the feature view, with a compatible type.
A mismatch fails the deployment with the offending columns in `deployment.get_logs()`, instead of serving wrong predictions.

If the feature view has a transformation that needs training dataset statistics, such as `min_max_scaler`, and the model has no training dataset version, `deploy()` refuses and names the transformation.

### Step 4: Read the contract

=== "Python"

    ```python
    schema = deployment.schema
    schema.describe()  # one row per field: group, name, type, nullable

    print(schema.names)  # the order of positional rows
    print(schema.unresolved)  # fields whose type is not known, such as request parameters

    json_schema = schema.to_json_schema()  # {"request": ..., "response": ...}
    openapi = schema.to_openapi("fraud", url=deployment.get_inference_url())
    ```

Fields belong to one of four groups:

| group | source | required |
| --- | --- | --- |
| serving keys | the feature view's serving keys, present only when a feature is looked up | yes, non-null |
| passed features | `passed_features=` | yes, nullable when the feature is |
| request parameters | arguments of on-demand transformations that are not features | yes |
| extra logging features | extra columns of the feature view's logging, minus the reserved ones | no |

Request parameter types come from the annotations of the transformation function's arguments: `def amount_ratio(amount: float, budget: float)` records `budget` as `double`.
An unannotated argument is reported as unresolved, and any value is accepted for it unless you refine the schema (Step 6).

### Step 5: Send requests

Rows are objects keyed by field name, or arrays in `schema.names` order.
A request holds one to `schema.max_batch_rows` rows (default 512).
The limit is part of the schema, so the published JSON Schema, the client, the transformer, and the predictor all apply the same one.
Set `SERVING_MAX_BATCH_ROWS` in `env_vars=` to change it; the change publishes a new schema id.
A request carries either `instances` or `inputs`, never both.

=== "Python"

    ```python
    deployment.predict(inputs=[{"cc_num": 4473593503484549, "amount": 12.5}])
    deployment.predict(inputs=[[4473593503484549, 12.5]])
    ```

The client validates the rows against the schema before sending and raises `ModelServingException` with every problem found; pass `validate=False` to skip that and let the pod answer.
A batch is all objects or all arrays, in the published JSON Schema as in the pod.

=== "curl"

    ```bash
    # INFERENCE_URL is deployment.get_inference_url(), also shown on the deployment page
    curl -X POST "$INFERENCE_URL" \
      -H "Authorization: ApiKey $API_KEY" -H "Content-Type: application/json" \
      -d '{"instances": [{"cc_num": 4473593503484549, "amount": 12.5}]}'
    ```

### Step 6: Refine or replace the schema

Pass `schema=` to `deploy()` to refine the inferred schema, for instance to give a request parameter a type.
A refinement keeps the inferred fields; adding or removing one is refused.

=== "Python"

    ```python
    from hsml.deployment_schema import DeploymentSchema

    deployment = model.deploy(name="fraud", passed_features=["amount"])
    inferred = deployment.schema
    refined = DeploymentSchema(
        serving_keys=inferred.serving_keys,
        passed_features=inferred.passed_features,
        request_parameters=[{"name": "rate", "type": "double", "nullable": False}],
        extra_logging_features=inferred.extra_logging_features,
        feature_view=inferred.feature_view,
        training_dataset_version=inferred.training_dataset_version,
        output=inferred.output,
    )
    deployment.schema = refined
    deployment.save()
    ```

A custom predictor script deployed with `schema=` (or `passed_features=`) gets the same validation in the pod, before its `predict()` is called, for REST V1 requests.
The client validates REST requests only, so a gRPC client is not checked on either side.

### Step 7: Republish after changing the feature view

The served contract does not change when you enable logging, add logging columns, or change the feature view.
Re-infer and save to publish the new contract as a new revision:

=== "Python"

    ```python
    deployment.reinfer_schema()
    deployment.save()
    ```

## Revisions { #deployment-schema-revisions }

Every schema is content-addressed: `deployment.schema_id` is a hash of its content, and equal schemas have equal ids.
The client writes the schema and its JSON Schema and OpenAPI renderings to `/Deployments/<deployment-name>/resources/schema/<schema_id>.*` before the deployment is created or updated, and records the id in the environment variable `SERVING_SCHEMA_ID` of the predictor and of the transformer, when there is one.
`SERVING_SCHEMA_ENFORCER` on the same components records which of the two validates requests for that revision.
The files are never modified or removed while the deployment exists.

A deployment revision therefore always enforces the exact schema it was created with, and answers discovery consistently with what it enforces.
The pod also takes its model, feature view, and training dataset version from its own revision, and refuses to start when the schema was published for another training dataset version than the one it would serve.
Updating the schema rolls the instances: old pods keep the old contract until they are replaced.
Rolling back is `deployment.schema = previous_schema; deployment.save()`, which points the revision at a file that is still there.

## Discovery for non-Python clients

The Hopsworks REST API serves the three documents to any client with an API key that has the `SERVING` scope, so prediction access implies discovery access:

```bash
SERVING_ID=$(curl -s -H "Authorization: ApiKey $API_KEY" \
  "https://$HOST/hopsworks-api/api/project/$PROJECT_ID/serving?name=fraud" | jq .id)

curl -s -H "Authorization: ApiKey $API_KEY" \
  "https://$HOST/hopsworks-api/api/project/$PROJECT_ID/serving/$SERVING_ID/schema?format=openapi"
```

`format` is `schema` (default), `jsonschema`, or `openapi`.
`schemaId=<id>` returns the documents of an earlier revision.
A deployment without a schema, or an unknown id, answers `404` with error code `240037`.

## Type encoding

The JSON Schema fragment, the accepted JSON values, and the encoding the Python client applies follow one table.

| feature type | JSON Schema | accepted JSON | Python client sends |
| --- | --- | --- | --- |
| `tinyint`, `smallint`, `int` | `{"type": "integer"}` | integer | `int` |
| `bigint` | integer or decimal string | integer, or a decimal string for values beyond 2^53 | `int` |
| `float`, `double` | `{"type": "number"}` | finite number | `int`, `float` |
| `decimal(p,s)` | number or string | number, or decimal string | `Decimal` as string |
| `string`, `varchar(n)`, `char(n)` | `{"type": "string"}` | string | `str` |
| `boolean` | `{"type": "boolean"}` | boolean | `bool` |
| `timestamp` | RFC 3339 string or integer | RFC 3339 string, or epoch milliseconds | `datetime` as RFC 3339 UTC |
| `date` | date string or integer | `YYYY-MM-DD`, or days since epoch | `date` as `YYYY-MM-DD` |
| `binary` | base64 string | base64 string | `bytes` as base64 |
| `array<T>` | array of `T` | array | list |
| `struct<...>` | object with exactly those fields | object | dict |
| `map<K,V>` | object with values of `V` | object | dict |
| unresolved | `{}` | anything | unchanged |

## Errors { #deployment-schema-errors }

Errors raised by the default predictor and by the schema enforcement carry a structured `detail`:

```json
{"detail": {
  "code": "SCHEMA_VALIDATION",
  "message": "Prediction request does not match the deployment schema of 'fraud'.",
  "schema_id": "3f9a1c2b7d4e6f80",
  "errors": [
    {"row": 0, "field": "amount", "reason": "missing"},
    {"row": 2, "field": "cc_num", "reason": "must not be null"}
  ]}}
```

| status | code | when |
| --- | --- | --- |
| 400 | `SCHEMA_VALIDATION` | the request does not match the schema; `errors` names every row and field |
| 400 | `FEATURE_LOOKUP_FAILED` | the feature store rejected the lookup for a reason other than a missing entity |
| 404 | `ENTITY_NOT_FOUND` | at least one row's serving keys match no entity; the batch is rejected and `errors` names the rows |
| 413 | `BATCH_TOO_LARGE` | more than `SERVING_MAX_BATCH_ROWS` rows |
| 422 | `TRANSFORMATION_FAILED` | a transformation raised; `field` is the transformation name |
| 500 | `MODEL_FAILED` | the model raised |
| 500 | `CONTRACT_VIOLATION` | the pod produced a result that does not match the contract: a different number of vectors or predictions than rows, or other feature vector columns than published |
| 503 | `FEATURE_STORE_UNAVAILABLE` | the online store or the feature store API could not be reached |

A request is all or nothing: either every row gets a prediction, in request order, or the whole request fails and no row is logged.
Error responses never include feature values or exception text: a failure names the exception type only, and `detail.request_id` carries the correlation id (the `x-request-id` header, or one generated for the request) under which the pod log holds the full error.
The Hopsworks REST inference proxy does not forward `x-request-id`; send it through the Istio URL when the id must be yours.
Responses with a 5xx status may be retried; a retry may read newer features and always produces another log row, so reuse the `x-request-id` header to tie the rows together.

## Feature logging and monitoring { #deployment-schema-feature-logging }

When the feature view has logging enabled, the default predictor logs every request with the untransformed and transformed features, the predictions, the request id, the training dataset version, and the model name and version, so `deployment.create_model_monitoring()` works with no extra code.

Declare the reserved extra logging columns on the feature view and the predictor fills them, which tells deployments and revisions apart in the log:

| column | type | value |
| --- | --- | --- |
| `deployment_name` | `string` | the deployment name |
| `deployment_version` | `int` | the deployment version |
| `deployment_schema_id` | `string` | the schema id of the revision that served the request |
| `request_row` | `int` | the row's index in its request |

Any other extra logging column becomes a request field that clients may send.

Logging is asynchronous: the request is answered immediately, the logging frame is built on a background thread of the predictor, and the rows are handed to the pod's inference-logger sidecar from there.
A logging failure never fails a request, and both buffers are bounded by `FEATURE_LOGGER_QUEUE_SIZE` rows (default 1000: rows waiting for the predictor's logging thread, and rows waiting in the sidecar logger); beyond it a request's rows are dropped and counted, so a slow logger cannot exhaust the pod's memory.
Both buffers count rows rather than requests, because one request carries a whole batch.
The predictor's own backlog admits one request whatever its size when it is empty, so a deployment whose batches are larger than the buffer logs instead of dropping every request; its peak is then that single batch, itself capped by the schema's batch limit.
There is no synchronous mode: a prediction is never delayed by its log write.

## Custom predictor scripts

Subclass the default predictor when the model needs another loader or the predictions need post-processing, and deploy with `default_predictor=True` so the schema is still inferred:

=== "Python"

    ```python
    from hsml.default_predictor import DefaultPredict


    class Predict(DefaultPredict):
        def load_model(self, model_files_path): ...

        def model_predict(self, feature_vectors):
            return self.model.predict_proba(feature_vectors[self.model_input_columns])
    ```

The serving wrapper imports a model deployment's script itself, so the script needs no `__main__` block.
Only a [feature view deployment][feature-view-deployment] script, which may be started as a plain script, hands over to the wrapper.
Any predictor script, subclass or not, is protected by the serving wrapper when the deployment carries a schema: invalid rows and oversize batches are refused before `predict()` runs.
With a transformer, the transformer validates the request, whether or not it implements `preprocess()`, and the predictor trusts the transformer's output.
Each pod reads that role from its own revision, so a predictor created before a transformer was added keeps validating until it is replaced.
This needs an inference environment built from a Hopsworks 5.1 or later base image; an older image serves the deployment without checking.

## Deployments without lookups { #deployment-schema-no-lookup }

Nothing is looked up in the online store when every stored feature of the view arrives with the request, or when the model has no feature view.
In both cases the schema has no serving keys.

### Every feature passed

Pass every non-label stored feature of the view in `passed_features=`; on-demand features are computed from the request parameters, so they are never looked up.
The view still computes the on-demand features and applies the model-dependent transformations with the pinned training dataset's statistics, and feature logging and monitoring work as for any other deployment.

=== "Python"

    ```python
    stored = [
        f.name
        for f in feature_view.features
        if not f.label and f.on_demand_transformation_function is None
    ]
    deployment = model.deploy(name="fraud_passed", passed_features=stored)
    print(deployment.schema.serving_keys)  # []
    ```

The same applies to `feature_view.deploy(passed_features=stored)`, which then returns the transformed vectors of the passed features.

### A model without a feature view

A Python model registered without a feature view deploys with the default predictor when you pass `default_predictor=True` and name its input columns with `passed_features=`, in the order the model expects.
Those columns are the whole request: the schema has no serving keys and no request parameters, nothing is looked up or transformed, and there is no feature logging or monitoring because there is no feature view.
The types are unresolved, so any JSON value is accepted for them; refine the schema with `schema=` to pin them down.

=== "Python"

    ```python
    model = mr.python.create_model(name="fraud_plain")
    model.save("model_dir")

    deployment = model.deploy(
        default_predictor=True,
        passed_features=["amount", "age_days"],  # the model's input columns, in its order
    )
    deployment.schema.describe()  # passed features only, types unresolved
    deployment.predict(inputs=[{"amount": 12.5, "age_days": 41}])
    ```

## Access control

Prediction through the Hopsworks REST API and through the Istio ingress requires an API key with the `SERVING` scope and the Data Owner or Data Scientist role in the project.
The pod looks up features as the project's serving identity, not as the caller.
Anyone allowed to call `:predict` can therefore obtain the transformed features of any entity the feature view can serve, and a feature view deployment returns those features directly.
Log rows contain feature values and are governed by the logging feature group's permissions.

## Environment variables

| variable | set by | meaning |
| --- | --- | --- |
| `SERVING_SCHEMA_ID` | the client | the schema the revision serves |
| `SERVING_FEATURE_VIEW_NAME`, `SERVING_FEATURE_VIEW_VERSION` | the client, feature view deployments | the feature view served |
| `SERVING_TRAINING_DATASET_VERSION` | the client, feature view deployments | the pinned training dataset |
| `SERVING_SCHEMA_ENFORCER` | the client | `predictor` or `transformer`: the component of the revision that validates requests |
| `SERVING_MAX_BATCH_ROWS` | you, through `env_vars=` | rows accepted per request, default 512; recorded in the schema at publication |
| `FEATURE_LOGGER_QUEUE_SIZE` | you, through `env_vars=` | rows the predictor's logging thread and the async logger each buffer before dropping, default 1000; a value that is not a positive integer is ignored |

The `SERVING_*` names are reserved and refused in `env_vars=`, except `SERVING_MAX_BATCH_ROWS`.

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-method"></code> [`Model.deploy`][hsml.model.Model.deploy]
    - <code class="doc-symbol doc-symbol-method"></code> [`FeatureView.deploy`][hsfs.feature_view.FeatureView.deploy]
    - <code class="doc-symbol doc-symbol-class"></code> [`Deployment`][hsml.deployment.Deployment]
        - <code class="doc-symbol doc-symbol-method"></code> [`predict`][hsml.deployment.Deployment.predict]
        - <code class="doc-symbol doc-symbol-method"></code> [`reinfer_schema`][hsml.deployment.Deployment.reinfer_schema]
        - <code class="doc-symbol doc-symbol-method"></code> [`get_logs`][hsml.deployment.Deployment.get_logs]
        - <code class="doc-symbol doc-symbol-attribute"></code> [`schema`][hsml.deployment.Deployment.schema]
    - <code class="doc-symbol doc-symbol-class"></code> [`DeploymentSchema`][hsml.deployment_schema.DeploymentSchema]
        - <code class="doc-symbol doc-symbol-method"></code> [`describe`][hsml.deployment_schema.DeploymentSchema.describe]
        - <code class="doc-symbol doc-symbol-method"></code> [`to_openapi`][hsml.deployment_schema.DeploymentSchema.to_openapi]
        - <code class="doc-symbol doc-symbol-method"></code> [`to_json_schema`][hsml.deployment_schema.DeploymentSchema.to_json_schema]
    - <code class="doc-symbol doc-symbol-class"></code> [`DefaultPredict`][hsml.default_predictor.DefaultPredict]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>
