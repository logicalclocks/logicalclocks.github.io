# Operator Notes: Airflow 3 on Hopsworks

Administrative reference for cluster operators upgrading or installing Hopsworks with Airflow 3.

## What the chart deploys

The Airflow subchart now creates four Kubernetes objects in addition to
what the v1 chart deployed:

1. `dag-processor` Deployment — runs `airflow dag-processor`, parses
   DAGs listed in the manifest. Carries only validator keys (no private
   keys).
2. `keys-bootstrap` pre-install Job — generates two RSA 4096 keypairs
   (api-server + scheduler) and writes them to the
   `hopsworks-airflow-keys` Secret. Idempotent; re-runs are no-ops.
3. `db-reset` pre-install Job — drops and recreates the Airflow metadata database before migration.
   Install-only: gated by `hopsworkslib.isInstall`, so it never re-fires on `helm upgrade` or ArgoCD resync.
   Set `global._hopsworks.mode=install` on the first install only.
4. `hopsworks-airflow-keys` Secret — four PEM files (two private, two
   public). Pods project only the keys they need.

The existing `webserver` (now Airflow `api-server`) and `scheduler`
Deployments keep their resource names; only the container command and
environment changed.

## Resource matrix

| Component | Image | Command | Private keys mounted |
| --- | --- | --- | --- |
| `airflow-webserver` | `apache/airflow:3.0.6-python3.12` + Hopsworks layers | `airflow api-server --proxy-headers` | api-server-private |
| `airflow-scheduler` | same | `airflow scheduler` | scheduler-private |
| `airflow-dag-processor` | same | `airflow dag-processor` | none (validator-only) |

All three pods render `/opt/airflow/airflow.cfg` from `airflow.cfg.template` at container start (the runtime MySQL password is substituted into the template before the main process execs).
Liveness probes use a TCP check on the scheduler's serve_logs port (8793) and a `/proc/1/comm` read for the dag-processor; `pgrep` is unreliable under kernel hardening such as `kernel.yama.ptrace_scope >= 1` or `hidepid`.

## Key rotation

Re-run the `keys-bootstrap` Job with the `--rotate` flag (or delete the
`hopsworks-airflow-keys` Secret and run a `helm upgrade`), then
rolling-restart in this order:

```text
api-server → scheduler → dag-processor
```

Outstanding user cookies and outstanding Execution-API task tokens are
invalidated; the proxy re-mints on 401. Plan for ~30s of UI
unavailability during the api-server restart.

## Metadata DB on upgrade

The v3 chart drops and recreates the Airflow metadata database **on install only**, gated by `hopsworkslib.isInstall` (set `global._hopsworks.mode=install` on the first install).
There is no in-place 1.x → 3.x schema migration path; DAG-run history, ad-hoc Variables, ad-hoc Connections, and audit records from a 1.x deployment are not preserved by the cutover.
Schema changes after install go through the existing `migrate` job's Alembic migrations.

Customer DAG files in HopsFS at `Projects/<P>/Airflow/` are untouched.
Snapshot HopsFS before the upgrade if you need a rollback path that preserves DAG sources.

## Reverse proxy contract

`AirflowProxyServlet` in hopsworks-ee validates the Hopsworks JWT and forwards `Set-Cookie` from Airflow unchanged.
The proxy does not rewrite cookie `Path=`; Airflow sets the cookie path from `[api] base_url` automatically.

Membership is **not** refreshed on every forwarded request.
The Airflow JWT carries `project_ids` / `project_roles` / `is_admin` at mint time and is stable for the cookie's TTL (1 hour by default).
Real-time membership changes are propagated by the Hopsworks backend pushing to `POST /auth/internal/invalidate`, which evicts the affected user's cached entry so the next login re-fetches the membership.
A 60-second safety-net TTL on the cache catches drift even without an explicit invalidation.
See [Airflow Security Model](../../user_guides/projects/airflow/security_model.md#token--cookie-behavior) for the full description.

## DAG reconciler

`AirflowDagReconciler` is a Hopsworks-side singleton EJB that runs every 60 s (with a 30 s initial delay) on the Hopsworks admin pod.
It walks `Projects/<P>/Airflow/*.py` for every project, derives the canonical `dag_id` (`p_<project_slug>_<project_id>__<dag_user_name>`), and reconciles `dag_project_index` against the on-disk truth:

- A `.py` present on HopsFS without a matching index row triggers a row insert.
  This is the path that picks up files uploaded via the Hopsworks File Browser or copied via `DatasetApi.copy`, without needing a backend restart.
- An index row whose `.py` is gone triggers a row delete plus the same `airflow.api.common.delete_dag.delete_dag` cleanup the explicit delete button uses.

The reconciler runs under `@TransactionAttribute(NOT_SUPPORTED)` because the Airflow auth-manager HTTP calls it makes do not participate in the EJB global transaction.
Its logs appear in the admin pod under the logger `io.hops.hopsworks.common.airflow.AirflowDagReconciler`.

## Orphan cleanup CronJob

The chart deploys an `airflow-orphan-cleanup` CronJob (gated by `airflow.enabled`, no separate enable flag) that runs the SQL in `cleanup_orphans.sql` against the Airflow metadata DB.
It deletes orphan rows in `dag_run`, `task_instance`, `task_instance_history`, `xcom`, `log`, `dag_warning`, `asset_dag_run_queue` (`target_dag_id`), `task_outlet_asset_reference` (`dag_id`), and `deadline` (both `dag_id` and `dagrun_id`) that point at a `dag_id` no longer in the `dag` table.
This is the cleanup path Airflow itself does not run automatically when a DAG is hard-deleted out of band.
Only the most recent successful run of the CronJob is retained in-namespace; older Pods are reaped by the CronJob's history limit.

## OpenShift compatibility

The airflow image is built to OpenShift's arbitrary-UID + GID-0 contract.
`/etc/airflow` and `launcher.sh` are group-owned by root (`chown :0`) with the user permission bits mirrored onto the group (`chmod g=u`), so OpenShift's per-namespace UID (which always has GID 0) can read, write, and execute everything the `airflow` UID can on vanilla Kubernetes.
No `runAsUser` override is needed when deploying on OpenShift; the chart's pod-spec works unchanged.

## Metrics

The legacy `airflow-exporter` 1.3.0 does not support Airflow 3. Metrics
are now emitted via Airflow-native StatsD into a sidecar
`statsd_exporter` Pod, scraped by Prometheus on its `/metrics`
endpoint. The legacy `AllowMetricsSecurityManager` is gone.

## See also

- User-facing release notes: `user_guides/projects/airflow/airflow3_upgrade.md`
- Security model: `user_guides/projects/airflow/security_model.md`
