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

### Step 1: Deploy with tracing

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

A feature view deployment takes the same argument:

```python
import hopsworks


project = hopsworks.login()
fv = project.get_feature_store().get_feature_view("transactions", version=1)

deployment = fv.deploy(
    training_dataset_version=1,
    tracing={"enabled": True, "sampling_percentage": 10},
)
deployment.start()
```

`sampling_percentage` is the share of requests recorded as traces, from 0 to 100, and defaults to 10.
Every request is counted in the metrics, whatever the sampling.

Tracing stays on for `duration_days`, 7 by default, and then Hopsworks switches it off:

```python
deployment = model.deploy(
    name="fraud",
    tracing={"enabled": True, "duration_days": 30},
)
```

A longer period stores more traces in the online feature store; making sure it has room for them is up to you.

To add tracing to an existing deployment, update it; this restarts its pods:

```python
import hopsworks


project = hopsworks.login()
deployment = project.get_model_serving().get_deployment("fraud")

deployment.tracing = {"enabled": True}
deployment.save()
```

### Step 2: Switch tracing off and on while the deployment runs

```python
import hopsworks


project = hopsworks.login()
deployment = project.get_model_serving().get_deployment("fraud")

deployment.set_tracing(active=False)
deployment.set_tracing(active=True, sampling_percentage=50)
deployment.set_tracing(active=True, duration_days=30)
```

Switching tracing on, or changing `duration_days` while it is on, keeps it on for `duration_days` from now.
`deployment.tracing.active_until` is when it will be switched off.
Hopsworks checks every 5 minutes: once the period has ended it switches tracing off, sets `active` to `False` and records the end in `deployment.tracing.expired_at`.

The deployment is not restarted.
Its pods apply the change within about a minute, and pods started later begin with it.
Switched off, the deployment records no metrics and no traces and runs no timing code.
Only requests are ever traced: Prometheus scrapes of the deployment and its other endpoints are not.

The same change over the REST API, where a field left out keeps its value:

```bash
curl -X PUT \
  -H "Authorization: ApiKey $HOPSWORKS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"active": true, "samplingPercentage": 50, "durationDays": 30}' \
  "https://$HOPSWORKS_HOST/hopsworks-api/api/project/$PROJECT_ID/serving/$DEPLOYMENT_ID/tracing"
```

A deployment created without tracing answers `400` with error code `240062`, as does a `samplingPercentage` outside 0 to 100 or a `durationDays` below 1.
The response carries `activeUntil` and `expiredAt` in epoch milliseconds.

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-method"></code> [`Model.deploy`][hsml.model.Model.deploy]
    - <code class="doc-symbol doc-symbol-class"></code> [`Deployment`][hsml.deployment.Deployment]
        - <code class="doc-symbol doc-symbol-method"></code> <autoref identifier="hsml.deployment.Deployment.set_tracing" optional><code>set_tracing</code></autoref>
        - <code class="doc-symbol doc-symbol-method"></code> <autoref identifier="hsml.deployment.Deployment.delete_traces" optional><code>delete_traces</code></autoref>
        - <code class="doc-symbol doc-symbol-attribute"></code> [`tracing`][hsml.deployment.Deployment.tracing]
    - <code class="doc-symbol doc-symbol-class"></code> [`DeploymentTracingConfig`][hsml.deployment_tracing_config.DeploymentTracingConfig]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>

## Web UI

The deployment page of a deployment that serves a feature view has a `Transformations` section.
While tracing is on, the section lists the traced requests; expanding one shows its spans with their durations.
While it is off, the section is titled `Feature View Transformations: Metrics` and shows `Tracing is disabled`; clicking it shows how to turn tracing on.
On a deployment created with tracing, the switch in the section header turns it off and on, like `set_tracing`, and shows the sampling and the time tracing will be switched off.
Once the period has ended, the section says when tracing was switched off.

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

`feature_log` only queues the log write and returns, and `feature_log_write` runs on a background thread after the response is sent.
The deployment page draws the write and `feature_view.log` as a separate background log process on its own time axis, so they are not counted in the request time.

Only the first row of a request is traced, so a batch request records one `transformations` span; all of its rows are counted in the metrics.

## Trace storage limits

Traces are stored in the online feature store's disk tablespace, which feature groups with disk columns share.
Each deployment's `duration_days` bounds how long it records traces; three cluster settings bound what model and feature view deployments store there:

| Variable | Default | Effect |
| --- | --- | --- |
| `serving_tracing_max_traces_per_minute` | `60` | Most traces one predictor pod records per minute, whatever the sampling percentage. Below 1, no cap. |
| `serving_tracing_retention_days` | `7` | Traces older than this are deleted. `0` keeps them. |
| `serving_tracing_pause_free_percent` | `20` | Tracing is paused on every model and feature view deployment while less than this percentage of the tablespace is free. |

Hopsworks checks the tablespace every 5 minutes.
A paused deployment reads `paused_reason == "DISK_NEARLY_FULL"` on `deployment.tracing`, and its page says tracing is paused.
Deleted traces free space for later traces in the same tables, not in the tablespace, so a pause lifts once an administrator adds a data file to the tablespace and at least 10 points more than the threshold are free.
The settings are Helm values under `hopsworks.variables`; a changed cap reaches running pods the next time their tracing is switched or they restart.
Deleting a deployment deletes its traces.

The `LowDiskDataFileExtents` alert fires when less than 20% of the tablespace is free.

To delete a deployment's traces yourself, all of them or those created before a time:

```python
from datetime import datetime, timedelta

deployment.delete_traces()
deployment.delete_traces(
    until_datetime=datetime.now() - timedelta(days=1), batch_size=1000
)
```

Each request deletes at most `batch_size` rows (default 1000, at most 10000) from each trace table in one transaction, since RonDB caps the operations one transaction holds; `delete_traces` repeats it until none are left and returns the number of rows deleted.
Over the REST API, one request deletes one batch and returns `{"deleted": <rows>}`; repeat it until `deleted` is 0.
`until` is in epoch milliseconds and is optional:

```bash
curl -X DELETE \
  -H "Authorization: ApiKey $HOPSWORKS_API_KEY" \
  "https://$HOPSWORKS_HOST/hopsworks-api/api/project/$PROJECT_ID/otel/servings/$DEPLOYMENT_ID/traces?until=1793145600000&batchSize=1000"
```

A `batchSize` outside 1 to 10000 answers `400` with error code `240064`.

## Overhead

The figures below are a guideline to the overhead to expect, not a guarantee: they depend on the transformation functions, the hardware and the load.
They were measured on a feature view with five transformation functions.

| State | Added time per feature vector |
| --- | --- |
| Tracing switched off, or deployment created without tracing | none |
| Tracing on, request not sampled | 17 to 34 µs, about 45% of the transformations' own time |
| Tracing on, request sampled | 0.4 to 0.65 ms |

Request latency inside the predictor pod, for 300 sequential requests of one row each:

| Deployment | p50 | p95 | p99 |
| --- | --- | --- | --- |
| Created without tracing | 3.1 ms | 4.3 ms | 4.9 to 5.1 ms |
| Tracing on, 10% sampled | 3.6 to 4.1 ms | 6.6 to 7.1 ms | 8.4 ms |

The p95 and p99 of the traced deployment fall on its sampled requests.
Tracing does not change the predictor's memory: both deployments peaked at about 420 MB resident.

The collector sidecar requests 0.5 CPU and 1 GiB of memory per replica by default, set by the cluster administrator.
A deployment created with tracing serves its requests with one worker process per replica, so that its metrics count every request; scale it with replicas.
Setting the `KSERVE_WORKERS` environment variable raises the worker count, and the metrics then count only the requests of the worker each scrape reaches.
