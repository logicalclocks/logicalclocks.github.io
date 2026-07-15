# Airflow 3 in Hopsworks

Hopsworks now ships Apache Airflow 3.0.6 as its workflow engine.
Airflow 3 is a major release with breaking changes to the DAG authoring API; the old 1.10-era DAGs do not run on it.
This page covers what changed, what you need to do to your DAGs, and what the new per-project security model guarantees.

## Per-project DAG isolation

A non-admin Hopsworks user can only see, trigger, edit, pause, clear, or read logs of DAGs that belong to a Hopsworks project they are a member of.
The boundary is enforced on every authenticated request to the Airflow API server, every navigation in the Airflow UI, and every CLI call.

The **Audit Log** is visible to every authenticated user but its rows are filtered server-side: non-admin users see only events whose `dag_id` belongs to one of their projects.
The Hopsworks platform admin (`HOPS_ADMIN`) sees the unfiltered log.

What this **does not** isolate in this release:

- **Execution-time data access.** DAG tasks run in one shared scheduler process (LocalExecutor).
  A task can in principle read any Airflow Variable, Connection, or XCom row, regardless of project.
  Treat Airflow Variables, Connections, and Pools as cluster-wide.
- **DAG parsing.** DAGs from all projects are parsed in one shared process.
  Module-top-level code in a DAG file runs with the dag-processor's privileges; treat it as cluster-wide too.

These are tracked for a future release that switches to KubernetesExecutor plus per-team dag-processors.
Until then, do not put project-private secrets in Airflow Variables or Connections — the per-DAG Hopsworks API key written by Hopsworks (see [API key for operators](#api-key-for-operators-no-embed)) is the exception, written by the platform itself rather than by users.

## What changed in the DAG API

You **must rewrite** your existing 1.10 DAGs for Airflow 3.
No automated rewrite tool ships with this release.
Concrete things to change:

| Old (Airflow 1.10) | New (Airflow 3.0.6) |
| --- | --- |
| `schedule_interval='@daily'` | `schedule='@daily'` |
| `provide_context=True` | implicit, remove the argument |
| `execution_date` in a template | `logical_date` |
| `from airflow.operators.python_operator import ...` | `from airflow.operators.python import ...` |
| `@apply_defaults` on custom operators | removed; declare `__init__` params normally |
| `SubDagOperator` | TaskGroups + Assets |
| `from airflow.models import BaseOperator` | `from airflow.sdk.bases.operator import BaseOperator` |
| Custom Hopsworks operators imported via plugins | Provider package `apache-airflow-providers-hopsworks` |
| Default `catchup_by_default = True` | Default `catchup=False`; set explicitly |
| `schedule_interval='@continuous'` | Rejected by Hopsworks; use cron or `@once` |

The Hopsworks-provided operators are now exposed via a standard provider:

```python
from hopsworks.airflow.operators import HopsworksLaunchOperator  # noqa: F401
from hopsworks.airflow.sensors import (  # noqa: F401
    HopsworksHdfsSensor,
    HopsworksJobSuccessSensor,
)
```

`HopsworksHdfsSensor` replaces the legacy `HopsworksHdfsSensor` plugin from the 1.x shim.
It polls `/hopsworks-api/api/project/<id>/dataset/<path>?action=stat` and accepts either `project_id` or `project_name`.

## API key for operators (no embed)

Hopsworks operators and sensors authenticate via the `HopsworksHook`, which resolves a credential in this order:

1. **Task token exchange** — the scheduler signs a per-task RS256 token; the hook POSTs it to `/api/auth/airflow-task-exchange/exchange` on Hopsworks and gets a project-scoped JWT back.
2. **Per-DAG Airflow Variable** — Hopsworks writes a per-DAG API key into an Airflow Variable named `hopsworks_api_key_<sha256(dag_id)[:16]>` (Fernet-encrypted at rest) on every DAG compose.
   The hook reads it at task runtime via `Variable.get(...)` and uses it as `Authorization: ApiKey <key>`.
3. **Airflow Connection** `hopsworks_default` — `conn.password` is read as a literal API key.
   Useful for out-of-cluster operators.
4. **`HOPSWORKS_API_KEY` env var** — manual override for power users.

The generated DAG file **never carries the API key** — the secret lives only in the Airflow Variables table (admin-only via `HopsworksAuthManager`), so the DAG `.py` is safe to inspect, version-control, or share.
Re-generate the DAG from the Hopsworks UI to rotate the key.

DAG files composed before this change still embed `os.environ.setdefault("HOPSWORKS_API_KEY", "<key>")` near the top of the file.
They continue to work because the env-var path is the fourth tier in the hook's fallback, but the secret is in the file.
Regenerate the DAG from the Hopsworks UI to drop the embed and switch to the Variable-fetch path.

## DAG identity

The Airflow `dag_id` for a Hopsworks-composed DAG is now:

```text
p_<project_slug>_<project_id>__<dag_user_name>
```

For example, project `acme` (id `42`) with a DAG named `daily_ingest`
becomes `p_acme_42__daily_ingest` in the Airflow UI. The Hopsworks UI
hides the prefix when displaying DAG names.

If you reference your DAGs by `dag_id` from external code (XCom pulls
across DAGs, `TriggerDagRunOperator`, REST API integrations), update
those references to the new format.

## REST authentication

The Airflow API server is reached through the standard Hopsworks reverse
proxy at `https://<hopsworks>/hopsworks-api/airflow/`. Browsers carry an
HttpOnly `_token` cookie set by the auth manager; external clients use
bearer tokens.

To obtain a bearer token from a Hopsworks JWT:

```bash
curl -X POST "https://<hopsworks>/hopsworks-api/airflow/auth/token" \
     -H "Content-Type: application/json" \
     -d '{"hopsworks_jwt": "<your-hopsworks-jwt>"}'
```

Response:

```json
{"access_token": "<airflow-jwt>", "token_type": "Bearer", "expires_in": 3600}
```

Use the returned `access_token` in `Authorization: Bearer` on all
`/api/v2/*` calls.

## Recent runs in the Hopsworks UI

The Hopsworks Airflow page lists each DAG with a **Last runs** column that renders the most recent runs as colored squares (green = success, red = failed, blue = running, yellow = queued / scheduled, gray = other).
Hover any square for the run id, state, and start time.
The data is read from a project-scoped Hopsworks endpoint that proxies to the auth manager and walks the same `dag_run` table the Airflow UI does, so the two views stay consistent.

Clicking anywhere on a DAG row opens the DAG in the Airflow UI (in a new tab).
The pencil column at the row's end opens the generated Python file in a Hopsworks editor without leaving Hopsworks.

## Metadata DB on upgrade

Upgrading from Airflow 1.10 to Airflow 3 drops and recreates the Airflow metadata DB.
Historical DAG-run records, task logs in the DB, and any ad-hoc Variables / Connections you had configured are not preserved.
Snapshot HopsFS `Projects/<P>/Airflow/` before upgrade so you can roll back DAG files; the DB itself is not recoverable through the chart.

## Task logs across pod restarts

Airflow 3 with the LocalExecutor writes task logs to the scheduler pod's local filesystem and serves them on port 8793 to the api-server pod.
The scheduler records the source endpoint (host + port) on the task instance row.
Hopsworks configures the scheduler with `[core] hostname_callable = airflow.utils.net.get_host_ip_address` so that endpoint is the pod IP (routable across pods), not the pod's DNS hostname (not resolvable from sibling pods).

Logs from runs that started before the scheduler pod was last restarted are unrecoverable — the pod's filesystem is ephemeral.
Re-trigger the DAG to regenerate task logs if you need them.
