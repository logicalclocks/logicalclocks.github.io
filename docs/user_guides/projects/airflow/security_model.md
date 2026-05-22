# Airflow Security Model

Hopsworks deploys Apache Airflow 3 with a custom auth manager that
enforces per-Hopsworks-project DAG visibility. This page is the
authoritative reference for what the security boundary covers and what
it does not.

## What is isolated

Every authenticated request to the Airflow API server, every page in the
Airflow UI, every CLI call:

| Surface | Behavior for a non-admin user |
| --- | --- |
| `GET /api/v2/dags` | Returns only DAGs in the user's projects |
| `GET /api/v2/dags/{dag_id}` | 404 for cross-project DAGs |
| `POST /api/v2/dags/{dag_id}/dagRuns` (trigger) | 403 for cross-project DAGs |
| `POST /api/v2/dags/{dag_id}/pause` | 403 for cross-project |
| `GET /api/v2/dags/.../taskInstances/.../logs` | 403 for cross-project |
| Airflow UI menu | Connections / Variables / Pools / Config / Plugins / Providers / Cluster Activity stripped (admin-only). Audit Log is visible to all users but rows are filtered server-side to `dag_id IN (user's project dag_ids)`. |
| `GET /api/v2/dagSources/{dag_id}` | 403 for cross-project |
| Direct HopsFS access to `Projects/<P>/Airflow/` | POSIX ACLs deny cross-project read |

The dag-to-project map is written by the Hopsworks backend whenever a
DAG is composed or deleted, and stored in a table inside Airflow's own
metadata DB. Editing a DAG file directly (e.g. changing `tags=[...]`)
cannot move the DAG to a different project's namespace.

## What is **not** isolated

The shared `dag-processor` parses DAGs from all projects. The shared
LocalExecutor runs tasks from all projects in one process tree. As a
consequence:

- Tasks can read any Variable, Connection, or Pool present in the
  metadata DB.
- Tasks can read XCom rows belonging to other projects' tasks.
- DAG-author code at module top level runs in the shared parser with
  metadata DB credentials.
- A task can in principle read environment variables of co-running tasks
  on the same scheduler pod.

A future release switches to KubernetesExecutor with per-team
dag-processors to close these gaps. Until then:

- **Do not store project-private secrets in Airflow Variables or Connections.**
  Use the Hopsworks-side secrets API for per-project credentials.
  Hopsworks operators obtain a short-lived project-scoped token at task runtime via the Execution-API token exchange, so they do not depend on Airflow Variables.
  The one exception is the platform-managed per-DAG API key, which Hopsworks writes itself into an Airflow Variable named `hopsworks_api_key_<sha256(dag_id)[:16]>` on every compose; the variable value is Fernet-encrypted at rest and the variables list is admin-only, so project users cannot enumerate or read each other's keys.
- **Do not assume DAG code is sandboxed at parse time.** Module-top-level
  code in a customer DAG can execute network calls and reach anything
  the dag-processor's ServiceAccount can reach.

## Token + cookie behavior

The auth manager sets a `_token` cookie on UI logins.
The cookie is `HttpOnly`, `Secure` (under TLS), `SameSite=Lax`, and scoped to `/hopsworks-api/airflow`.
The Hopsworks proxy passes it through unchanged; cookie path scoping is set by Airflow itself from the `[api] base_url` config.

The same auth manager mints bearer tokens for external clients via `POST /auth/token`.
The bearer token format and validation are identical to the cookie-borne token; only the carrier differs.

The Airflow JWT carries the user's `project_ids`, `project_roles`, and `is_admin` flag at mint time.
Membership is **not** refreshed per request — Airflow 3.0.x does not expose a synchronous refresh hook on `BaseAuthManager` — so a user's authorization is stable for the cookie's TTL (1 hour by default).

## Project membership changes

When a Hopsworks project's membership changes (add member, remove member, role change), the Hopsworks backend immediately invalidates the affected user's entry in the Airflow auth manager's cache via `/auth/internal/invalidate`.
The next login by that user re-fetches their project list and reflects the new membership.
The cache also has a 60-second safety-net TTL even without an explicit invalidation.
