---
description: Let NVIDIA Run:ai schedule the GPUs of Hopsworks projects
---

# GPU Scheduling with NVIDIA Run:ai

On a Kubernetes cluster where NVIDIA Run:ai manages the GPUs, Hopsworks can hand GPU scheduling and GPU accounting to Run:ai.
Each Hopsworks project then becomes a Run:ai project, and Run:ai's quotas, fair share and preemption apply to every pod the project runs.

The integration is off by default.
With it off, Hopsworks schedules and reports GPUs from the Kubernetes API as before.

## What Hopsworks does

With `run_ai_enable` set, Hopsworks does the following:

- On project creation, Hopsworks creates a Run:ai project with the name of the project's Kubernetes namespace, bound to that namespace (`requestedNamespace`), in the Run:ai department named by `run_ai_default_department`.
  It labels the namespace `runai/queue=<run:ai project>`.
  A Run:ai project that is already bound to the namespace is adopted instead.
- Run:ai's admission webhooks then schedule every pod in the namespace with `runai-scheduler` in the project's queue: jobs, notebooks, terminals, Ray clusters and model deployments.
  Hopsworks also puts the `runai/queue` label on the workloads it creates.
- Projects that existed before the integration was enabled are bound on their first workload start, or by a background pass every `run_ai_reconcile_interval_s` seconds.
- Deleting a Hopsworks project deletes its Run:ai project.
- Kueue integration is off while Run:ai is enabled, even when `kueue_installed` is set.

Hopsworks never creates Run:ai departments and never moves a Run:ai project to another department.
Moving a project in Run:ai deletes and recreates it, which deletes its workloads and assets.
When a project is in another department than expected, the GPU view shows a warning and a Run:ai administrator moves it.

New Run:ai projects get `run_ai_project_gpu_quota` deserved GPUs, `0` by default.
Run:ai admits notebooks, terminals, Python apps and model deployments only within a project's quota, because it does not preempt them.
Hopsworks checks the quota before it starts one of those with GPUs and refuses the start, with the number of GPUs the project has left, instead of leaving a pod waiting.
Jobs are not checked: they are preemptible and run on idle GPUs over quota.
Assign quota to the projects that need GPU notebooks or deployments in the Run:ai UI.

## Prerequisites

1. Run:ai is installed on the same Kubernetes cluster as Hopsworks, and its control plane is reachable from the Hopsworks pods.
   The default `run_ai_url` is the in-cluster address of a self-hosted control plane, `http://runai-backend-traefik.runai-backend.svc.cluster.local:8080`.
2. The department named by `run_ai_default_department` exists in Run:ai.
   Every Run:ai installation has a department called `default`.
3. A Run:ai service account for Hopsworks, created under Access, Service accounts in the Run:ai UI.
   Give it an access rule with the **System administrator** role at cluster scope.
   Hopsworks creates and deletes projects, reads departments, and reads node pool metrics, which needs cluster read permission.
   When you create the access rule through the API instead of the UI, its `subjectId` is the service account's name, not its id.
4. A Kubernetes Secret in the Hopsworks namespace that holds the service account's client secret:

    ```bash
    kubectl -n hopsworks create secret generic runai-hopsworks \
      --from-literal=clientSecret=<client secret>
    ```

## Helm values

Set these values on the Hopsworks chart and run `helm upgrade`:

```yaml
hopsworks:
  variables:
    run_ai_enable: true
    run_ai_client_id: "<client id>"
    run_ai_client_secret_name: runai-hopsworks
    run_ai_client_secret_key: clientSecret
```

| Value | Default | Meaning |
| --- | --- | --- |
| `run_ai_enable` | `false` | Turns the integration on |
| `run_ai_url` | in-cluster control plane | Run:ai control-plane URL |
| `run_ai_client_id` | empty | Client id of the service account |
| `run_ai_client_secret_name` | empty | Secret holding the client secret |
| `run_ai_client_secret_key` | `clientSecret` | Key of the client secret in that Secret |
| `run_ai_cluster_name` | empty | Run:ai cluster to use; empty selects the only one |
| `run_ai_default_department` | `default` | Department new Run:ai projects are created in |
| `run_ai_project_gpu_quota` | `0` | Deserved GPUs of each new Run:ai project |
| `run_ai_ready_timeout_s` | `30` | Seconds project creation waits for the Run:ai project to become Ready |
| `run_ai_reconcile_interval_s` | `600` | Seconds between passes that bind existing projects |

These values are written to the Hopsworks configuration on every `helm upgrade`.
See [Cluster Configuration Variables Reference][cluster-configuration-variables-reference] for all variables.

## GPU availability

With the integration enabled, a project's Kubernetes page in the Hopsworks UI shows a Run:ai GPU section, and the terminal offers GPUs only to projects with deserved Run:ai GPUs.
The same numbers come from `GET /hopsworks-api/api/project/{id}/kube/gpu` and from the Python client:

```python
import hopsworks


project = hopsworks.login()

gpus = project.get_gpu_availability()
print(gpus.project, gpus.department)
print(gpus.available_non_preemptible, gpus.available_preemptible)
```

All numbers are for the project's default Run:ai node pool.

| Field | Meaning |
| --- | --- |
| `project`, `department` | Quota (deserved GPUs), limit, allocated and non-preemptible allocated GPUs |
| `node_pool_gpus` | Total, allocated and idle GPUs in the node pool |
| `available_non_preemptible` | GPUs notebooks, terminals and deployments can still get within quota |
| `available_preemptible` | Idle GPUs a batch job could borrow over quota now; an estimate, a larger job still queues |
| `warnings` | `RUN_AI_UNREACHABLE`, `RUN_AI_METRICS_MISSING`, `RUN_AI_PROJECT_NOT_READY`, `RUN_AI_DEPARTMENT_DRIFT`, `RUN_AI_BINDING_LEFT` |

## Operational dependency

Hopsworks keeps working when the Run:ai control plane is unreachable:

- Project creation still succeeds; the project is bound to Run:ai later by the background pass or its first workload start.
- Workloads in projects that are already bound start without calling the control plane, because the queue comes from the namespace label.
- A workload in a project that is not bound yet starts without a Run:ai queue, and a warning is logged.
- The quota check is skipped; Run:ai enforces the quota when it schedules the pod.

Run:ai's own admission webhooks are a hard dependency: they are configured with `failurePolicy: Fail` for every namespace labelled `runai/queue`.
When the `runai-admission-controller` or `admission` Deployment in the `runai` namespace is down, no pod can be created in a bound project namespace, Hopsworks system jobs in those namespaces included.
Pods in the Hopsworks namespace are not affected.
Monitor both Deployments like any other cluster-critical service.

## Turning the integration off

Setting `run_ai_enable` back to `false` stops Hopsworks from calling Run:ai, but the namespaces stay bound and Run:ai keeps scheduling their pods.
The GPU view reports `RUN_AI_BINDING_LEFT` for such projects.
To leave Run:ai, delete the Run:ai projects of the Hopsworks namespaces in Run:ai, which stops their workloads, and remove the `runai/queue` namespace label.
