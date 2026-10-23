# How To Trace Feature View Transformations in a Deployment

## Introduction

A model deployment whose model was trained from a feature view runs that feature view's on-demand and model-dependent transformations on every request, as a DAG of transformation functions.
Transformation tracing measures how long each of them takes.

With tracing on, the deployment:

- counts every request's transformations on its Prometheus endpoint, per feature view and per transformation function, with the fastest and slowest feature vector of the last minute;
- records a sample of the requests as traces: the request, its feature lookup, each transformation phase with one span per function in DAG order, the prediction and the feature log write;
- shows those traces in the `Transformations` section of the deployment page.

It applies to deployments created with `model.deploy(...)` from a model with a feature view, to feature view deployments, and to predictor scripts that call `get_feature_vector` or `get_feature_vectors`.

!!! info "Create the deployment with tracing"
    Tracing exports its spans through a collector sidecar, which is added to the deployment's pods when the deployment is created or updated with tracing enabled.
    A running pod cannot gain a container, so a deployment created without tracing has to be updated with it, which restarts it.
    Once it has tracing, it can be switched off and on, and its sampling changed, while it runs.

## Code

### Step 1: Connect to Hopsworks

```python
import hopsworks


project = hopsworks.login()
mr = project.get_model_registry()
ms = project.get_model_serving()
```

### Step 2: Deploy with tracing

```python
import hopsworks


project = hopsworks.login()
model = project.get_model_registry().get_model("fraud_model", version=1)

deployment = model.deploy(
    name="fraud",
    tracing={"enabled": True, "sampling_percentage": 10},
)
deployment.start()
```

`sampling_percentage` is the share of requests recorded as traces, from 0 to 100, and defaults to 10.
Every request is counted in the metrics, whatever the sampling.

To add tracing to an existing deployment, update it; this restarts its pods:

```python
import hopsworks


project = hopsworks.login()
deployment = project.get_model_serving().get_deployment("fraud")

deployment.tracing = {"enabled": True}
deployment.save()
```

### Step 3: Switch tracing off and on while the deployment runs

```python
import hopsworks


project = hopsworks.login()
deployment = project.get_model_serving().get_deployment("fraud")

deployment.set_tracing(active=False)
deployment.set_tracing(active=True, sampling_percentage=50)
```

The deployment is not restarted.
Its pods apply the change within about a minute, and pods started later begin with it.
Switched off, the deployment records no metrics and no traces and runs no timing code.

The same change over the REST API, where a field left out keeps its value:

```bash
curl -X PUT \
  -H "Authorization: ApiKey $HOPSWORKS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"active": true, "samplingPercentage": 50}' \
  "https://$HOPSWORKS_HOST/hopsworks-api/api/project/$PROJECT_ID/serving/$DEPLOYMENT_ID/tracing"
```

A deployment created without tracing answers `400` with error code `240058`, as does a `samplingPercentage` outside 0 to 100.

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-method"></code> [`Model.deploy`][hsml.model.Model.deploy]
    - <code class="doc-symbol doc-symbol-class"></code> [`Deployment`][hsml.deployment.Deployment]
        - <code class="doc-symbol doc-symbol-method"></code> [`set_tracing`][hsml.deployment.Deployment.set_tracing]
        - <code class="doc-symbol doc-symbol-attribute"></code> [`tracing`][hsml.deployment.Deployment.tracing]
    - <code class="doc-symbol doc-symbol-class"></code> [`DeploymentTracingConfig`][hsml.deployment_tracing_config.DeploymentTracingConfig]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>

## Web UI

The deployment page of a deployment that serves a feature view has a `Transformations` section.
While tracing is on, the section lists the traced requests; expanding one shows its spans with their durations.
While it is off, the section is titled `Feature View Transformations: Metrics` and says how to turn tracing on.
On a deployment created with tracing, the switch in the section header turns it off and on, like `set_tracing`, and shows the sampling.

The deployment's Grafana dashboard, opened with `View in Grafana` in the `Metrics` section, charts the metrics under `Feature view transformations`.

## Metrics

| Metric | Labels | Meaning |
| --- | --- | --- |
| `hopsworks_transformations_calls_total`, `hopsworks_transformations_seconds_total` | `feature_view`, `feature_view_version`, `kind` | Count and total time of all on-demand (`kind="on_demand"`) or all model-dependent (`kind="model_dependent"`) transformations of one feature vector |
| `hopsworks_transformations_window_min_seconds`, `hopsworks_transformations_window_max_seconds` | the above | Fastest and slowest feature vector in the last complete 60 second window |
| `hopsworks_transformation_function_calls_total`, `hopsworks_transformation_function_seconds_total`, `hopsworks_transformation_function_errors_total` | the above, `transformation`, `outputs` | The same per transformation function, and the calls that raised |
| `hopsworks_transformation_function_window_min_seconds`, `hopsworks_transformation_function_window_max_seconds` | the above | Fastest and slowest call of the function in the last complete 60 second window |
| `hopsworks_transformation_dag_edge` | the above, `depends_on` | 1 for each edge of the transformation DAG |

The average time is `rate(..._seconds_total[5m]) / rate(..._calls_total[5m])`.
`outputs` identifies a function, since one function can be attached to several features.

## Traces

A traced request records:

```text
predict
├── feature_lookup
│   └── transformations
│       ├── on_demand_transformations
│       │   └── one span per on-demand function, in DAG order
│       └── model_dependent_transformations
│           └── one span per model-dependent function, in DAG order
├── model_predict
└── feature_log
    └── feature_log_write
        └── feature_view.log
```

Only the first row of a request is traced, so a batch request records one `transformations` span; all of its rows are counted in the metrics.
Traces are stored in the project's online feature store, so keep the sampling low on a deployment that serves many requests.

## Overhead

Measured on a feature view with five transformation functions:

| State | Added time per feature vector |
| --- | --- |
| Tracing switched off, or deployment created without tracing | none |
| Tracing on, request not sampled | about 17 µs |
| Tracing on, request sampled | about 0.4 ms |

The collector sidecar requests 0.5 CPU and 1 GiB of memory per replica by default, set by the cluster administrator.
