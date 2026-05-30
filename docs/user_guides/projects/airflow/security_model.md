# Airflow Security Model

Hopsworks deploys Apache Airflow 3 with a custom auth manager that enforces per-Hopsworks-project DAG visibility.
This page is the authoritative reference for what the security boundary covers and what it does not.

## What is isolated

Every authenticated request to the Airflow API server, every page in the Airflow UI, every CLI call:

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

### Active-project scoping

Opening Airflow from a project's UI narrows visibility further to that project alone, even for users who are members of several.
The Hopsworks proxy forwards the project context via a `?hopsworks_project=<id>` query parameter that the auth manager turns into an `active_project_id` claim on the issued Airflow JWT.
The DAG list, the per-DAG endpoints, and the Audit Log are all filtered against the active project for the lifetime of the session.
Switching project in the Hopsworks UI re-mints the Airflow JWT with the new active project; the previous session's cookie remains valid for its TTL but is scoped to the previous project.
A Hopsworks admin opening Airflow without a project context sees every DAG; opening from a project still scopes to that project.

## What is **not** isolated

The shared `dag-processor` parses DAGs from all projects.
The shared LocalExecutor runs tasks from all projects in one process tree.
As a consequence:

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
  Hopsworks operators obtain a short-lived project-scoped token at task runtime via the Execution-API token exchange, so the primary auth path does not depend on Airflow Variables.

- **The per-DAG `hopsworks_api_key_<sha256(dag_id)[:16]>` Variable is a fallback only, and is not per-DAG isolated at runtime.**
  Hopsworks writes it during compose so the task-token-exchange path has a working credential to fall back to if the task-instance JWT is unreachable for any reason.
  The Variables UI is admin-only via `HopsworksAuthManager`, but inside a running task `Variable.get("hopsworks_api_key_<other-dag-sha>")` is not blocked — `dag_id` is non-secret and the hash is reproducible, so DAG code that calls `Variable.get` for another DAG's hashed name can read that key.
  Until per-task secret isolation lands with KubernetesExecutor, treat the fallback path as a shared credential surface within the cluster: don't run untrusted DAG code, and prefer the task-token-exchange path which is signed per-task and not stored in the metadata DB.
- **Do not assume DAG code is sandboxed at parse time.** Module-top-level
  code in a customer DAG can execute network calls and reach anything
  the dag-processor's ServiceAccount can reach.

## Token + cookie behavior

The auth manager sets a `_token` cookie on UI logins.
The cookie is `HttpOnly`, `Secure` (under TLS), `SameSite=Lax`, and scoped to `/hopsworks-api/airflow`.
The Hopsworks proxy passes it through unchanged; cookie path scoping is set by Airflow itself from the `[api] base_url` config.

The same auth manager mints bearer tokens for external clients via `POST /hopsworks-api/airflow/auth/token` (the auth manager's `/auth` router is mounted under the Airflow `[api] base_url`, which the Hopsworks chart pins to `/hopsworks-api/airflow/`).
The bearer token format and validation are identical to the cookie-borne token; only the carrier differs.

The Airflow JWT carries the user's `project_ids`, `project_roles`, and `is_admin` flag at mint time.
Membership is **not** refreshed per request — Airflow 3.0.x does not expose a synchronous refresh hook on `BaseAuthManager` — so a user's authorization is stable for the cookie's TTL (1 hour by default).

## Project membership changes

When a Hopsworks project's membership changes (add member, remove member, role change), the Hopsworks backend immediately invalidates the affected user's entry in the Airflow auth manager's cache via `/auth/internal/invalidate`.
The next login by that user re-fetches their project list and reflects the new membership.
The cache also has a 60-second safety-net TTL even without an explicit invalidation.
