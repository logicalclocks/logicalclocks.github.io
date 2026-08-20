---
description: Guide on how to manage Trino as a Hopsworks administrator
---

# Query Engine (Trino)

As a Hopsworks administrator, you can monitor and manage the Trino cluster used for query execution across all projects. The admin interface provides cluster-wide visibility into resources, performance, and worker health.

## Cluster Overview

The cluster overview provides a comprehensive view of your Trino deployment, including:

- **Cluster status**: Overall health and availability
- **Active queries**: Total number of running queries across all projects
- **Worker nodes**: Number of active and total workers
- **Resource utilization**: Cluster-wide CPU and memory usage
- **Query throughput**: Average query execution times and data processed

Use this dashboard to monitor overall cluster health and identify capacity issues.

<figure>
  <img src="../../../assets/images/admin/trino/trino-cluster.png" alt="cluster overview" />
  <figcaption>Trino cluster overview</figcaption>
</figure>

## Query History

The query history shows all queries executed across the Trino cluster, regardless of project. This centralized view helps administrators:

- **Monitor usage patterns**: Identify peak usage times and resource-intensive queries
- **Troubleshoot issues**: Investigate failed or slow queries
- **Audit activity**: Track query execution by project and user
- **Optimize performance**: Identify queries that may need optimization

Each query entry displays:

- Query ID and text
- Project and user who executed it
- Status (running, completed, failed)
- Execution time and resources consumed
- Timestamp

Click any query to view detailed execution information.

<figure>
  <img src="../../../assets/images/admin/trino/query-history.png" alt="query history" />
  <figcaption>Trino query history</figcaption>
</figure>

## Managing Workers

The workers view displays all Trino nodes in the cluster. For each node, you can see:

- **Node IP**: IP address of the worker node
- **Node version**: Trino version running on the node
- **Coordinator or worker**: Role of the node (coordinator or worker)
- **State**: Current state of the node (active, idle, or offline)

This view helps you monitor the cluster topology and identify any nodes that may be offline or experiencing issues.

<figure>
  <img src="../../../assets/images/admin/trino/workers.png" alt="workers" />
  <figcaption>Trino workers</figcaption>
</figure>

### Worker Status Details

Click on a worker to view detailed status information:

- **Resource metrics**: Detailed CPU, memory, and network usage over time
- **Task breakdown**: Types and number of tasks being executed
- **Error logs**: Any errors or warnings from the worker
- **Configuration**: Worker settings and assigned resources
- **Performance history**: Historical performance trends

Use this detailed view to diagnose worker-specific issues and optimize resource allocation.

<figure>
  <img src="../../../assets/images/admin/trino/worker-status.png" alt="worker status" />
  <figcaption>Trino worker status</figcaption>
</figure>

## Managing Catalogs

Catalogs created by project Data Owners are saved to the database but are not loaded by the running cluster until they are applied.
Two things apply them: the scheduled restart, which needs no administrator, and the Catalogs tab under Cluster Settings, Query Engine, where an administrator can apply them immediately or gate them behind approval.

The tab lists every catalog waiting to be applied, along with its status and the operation to apply (create, update, or remove).

Nothing notifies you when a Data Owner creates a catalog, and nothing notifies them when it is applied.
With the schedule on, a pending catalog goes live at the next restart that finds it, so the tab is where you go to apply one sooner or to reject it; with approval required, nothing goes live until you act, so check the tab periodically or agree a cadence with your projects.

<figure>
  <img src="../../../assets/images/admin/trino/catalogs-pending.png" alt="Pending catalogs" />
  <figcaption>Catalogs waiting to be applied</figcaption>
</figure>

### Applying pending requests

Every pending request is selected by default.
Clicking **Restart Trino** applies the selected ones in a single action: their definitions are written into the backend-owned Kubernetes Secrets that the cluster mounts at `/etc/trino/catalog`, and the query engine is restarted afterwards to load them, behind a dialog that confirms what is about to be applied.
Both halves are needed and in that order, which is why they are one button: a restart on its own would load nothing, because a catalog is only a database row until its definition is written out.

You can also **Delete** an individual pending request, which rejects that change without applying it.

The restart interrupts queries running anywhere on the cluster, so check the reported activity before confirming.

#### Where catalog credentials are stored

A connector's credentials end up in the places below. Anyone who can read those places can read the credentials, so plan access to them accordingly.

- A `${HOPSWORKS_SECRET:<name>}` reference is stored verbatim in the `trino_catalog` database row and is resolved to its value only at approval time. The database row never holds the value.
- A literal value typed straight into the properties editor is stored as-is in the `trino_catalog` database row, in cleartext, and is captured by database backups. Use a secret reference for any credential you do not want in the database.
- Either way, the written file holds the resolved plaintext, because Trino reads the credential from the catalog file itself.
  That file lives in a Kubernetes Secret rather than a ConfigMap, so it is covered by the RBAC that applies to Secrets in the Hopsworks namespace and by etcd encryption-at-rest on clusters that enable it.

<figure>
  <img src="../../../assets/images/admin/trino/catalogs-pending-restart.png" alt="Catalogs pending restart" />
  <figcaption>An applied catalog waits in Pending restart until the query engine reloads</figcaption>
</figure>

### Lifecycle settings

The same tab carries the **Catalog lifecycle** card, where the whole schedule is configured and saved as one group:

- **Scheduled restart every N hours or days.**
  The cadence is anchored at the configured time of day, so it keeps its phase across redeploys, and the next restart the schedule resolves to is shown next to the input.
- **Require approval for all catalog changes.**
  Turning this on cancels the scheduled restart entirely, because approval means nothing goes live unattended.
  Pending requests then wait in the table until an administrator applies them with Restart Trino, or rejects them with Delete.
- **Eager restart.**
  The query engine is checked every few minutes, and pending changes are applied ahead of the schedule the moment no query is running, queued, or blocked, so the restart lands in a moment with nothing to cancel.
  Users are told their catalog may go live earlier than the scheduled time.
- **Maximum catalogs**, across every project, at most 250.
  Each catalog is a file the query engine loads at startup, so the deployment is sized for a bounded number; the setting may lower the bound but never raise it past the ceiling.

Saving needs no redeploy: every Hopsworks instance derives its schedule from these settings and picks a change up within a minute, whichever instance served the save.

### A single project's allowance

The cluster-wide maximum is a ceiling on the deployment; how many catalogs any one project may create is set per project.
Open the project under Cluster Settings, Projects, and edit **Query Engine**, **Trino catalogs**, which shows the project's current count beside its limit.

A new project starts on the cluster default (`trino_catalog_max_per_project`, 10), so raising one project here raises that project only.
Checking **unlimited** removes the project's own bound, leaving only the cluster-wide ceiling; a limit of 0 blocks new catalogs in the project.
Both bounds apply to a create: the project must be under its own allowance, and the cluster must be under the ceiling.

### The wait for a quiet moment

A due scheduled restart does not fire into a busy cluster immediately.
It waits for the cluster to have no query running, queued, or blocked, re-checking every few minutes for up to an hour, and then restarts anyway: the wait buys a quiet moment when one exists, and the bounded give-up keeps a permanently busy cluster from deferring catalog changes forever.

An activity count the query engine cannot report counts as busy rather than idle, so a failed reading never costs someone their query.
The bounded wait is what makes that safe: a coordinator that is genuinely down never reports itself idle, and the restart that recovers it still happens when the window expires.

### Restarting

Trino reads catalogs only at startup, so a catalog change takes effect on the next restart, whether the schedule performs it or an administrator does.
Clicking "Restart Trino" applies the selected pending requests and rolls out the coordinator and workers.
The confirmation dialog reports how many queries are currently running or queued, so you can choose a low-traffic window before confirming.
The restart cancels those queries for **every project on the cluster**, not only the project whose catalog is being applied, and in-flight results are lost.
Trino keeps recent query detail in the coordinator's memory, so after a restart the live query views show only what the new coordinator has seen; older queries remain in the query history, which is stored separately.

<figure>
  <img src="../../../assets/images/admin/trino/restart-confirm.png" alt="Restart confirmation" />
  <figcaption>The restart confirmation reports the running queries the restart will interrupt</figcaption>
</figure>

A restart is refused while another approval or restart is already running, so concurrent actions by different administrators cannot collide or trigger redundant restarts.
If nothing is waiting to load or unload, the restart is skipped and reported as such rather than interrupting queries for no reason.

### Recovering a catalog Trino cannot load

Trino reads its catalogs at startup and refuses to start if it cannot load one of them.
A user catalog with an invalid definition therefore stops the whole query engine, coordinator and workers alike, and the pods stay in `CrashLoopBackOff`.
Kubernetes keeps the previous pods serving while the new ones fail, so queries may keep working for a while and the rollout never completes.

Click "Restart Trino" to recover.
The button stays available when nothing is waiting to be applied, because this situation leaves no pending catalog to load: the restart itself is the repair.

<figure>
  <img src="../../../assets/images/admin/trino/catalogs-recover.png" alt="Recover restart" />
  <figcaption>With nothing pending, the restart action is still available to recover a failed rollout</figcaption>
</figure>

Hopsworks reads the coordinator log, identifies the catalog Trino rejected, removes it from the mount, marks it **Failed**, and restarts so the cluster comes back without it.
The result names the catalogs that were removed:

> Removed 1 catalog Trino could not load. `project1__orders_pg`. Trino is restarting without them; the owners must fix the definitions.

Only user-created catalogs are removed this way.
A default catalog that fails to load is left in place, because that is a cluster configuration problem rather than something an administrator should resolve by deleting data.

A removed catalog keeps its row, so its owner can see what happened on the project's Catalogs page along with the error Trino reported.
Editing the definition returns it to Pending approval and it re-enters the normal flow.

Failed catalogs are not listed under pending, because they no longer block anything and no administrator action can fix them.
If Hopsworks cannot attribute the failure to a user catalog, it reports the connection error instead of removing anything, and the coordinator log is the place to look.

### Recovering catalog files lost from the mount

The catalog definitions are stored in the Hopsworks database, and the Kubernetes Secrets mounted at `/etc/trino/catalog` are derived from it.
A restore that brings back the database alone, a GitOps sync that prunes resources it does not manage, or a Secret deleted by hand therefore leaves catalogs that exist in Hopsworks with no file for Trino to read.

`POST /hopsworks-api/api/admin/trino/catalogs/reconcile` repairs it.
It writes the missing files back from the database, removes files that no catalog belongs to, which is also how a credential stops being mounted once its catalog is gone from the database, and reports what it changed.
It is always available, since an administrator calling it has already established that the repair is needed.
It also compares file contents, so it corrects a file whose name is right but whose content no longer matches the database.

Set **trino_catalog_reconcile_enabled** to `true` to have the same repair run on a schedule instead, shortly after startup and on the reconcile interval thereafter.
It is off by default because losing a shard Secret takes one of the events above rather than anything routine, so the repair belongs on a cluster that needs it rather than on every cluster.
Each scheduled pass compares which catalog files the Secrets hold against which ones the database expects, and repairs only when they disagree.
Comparing names rather than contents is what keeps a pass cheap enough for an interval, since rebuilding a file means decrypting every secret it references.
The consequence is that the scheduled pass does not notice a file whose name is right and content is wrong; use the endpoint for that.

Two things neither form does.
Neither restarts Trino, so a restored catalog is in the mount but not loaded until the next restart, like any other catalog change.
Neither touches a catalog that is pending approval, because that catalog's stored definition is the change an administrator has not approved yet, and applying it here would bypass that decision.
Those catalogs are reported as still needing approval.

A catalog whose `${HOPSWORKS_SECRET:<name>}` reference no longer resolves cannot be rebuilt, since the file Trino reads has to hold the resolved value.
The repair reports it, leaves any file it already has in place, because that copy resolved when it was approved and still works, and carries on with every other catalog.
Its owner has to repoint the reference at an existing secret.

## Credential files a project supplies

A connector that authenticates with a file, such as an Oracle wallet or a Java keystore, cannot be served by a catalog property alone.
Projects supply those files as [mountable secrets][mountable-secrets], and this section covers what that adds to a cluster.

A bundle is a directory of files in HopsFS under `mountable_secrets_path`, which defaults to `/apps/mountable-secrets`.
It is keyed by **project id** rather than by project name, so a deleted project and a later project of the same name can never share a directory.
The `charts/hopsfs` preset Job creates the root as `payara:hdfs` with mode `0750`.
The backend asks the filesystem for that owner and mode before it writes a bundle or deletes a project's tree, and refuses if either differs, so a root created by hand with the wrong mode fails every upload rather than quietly widening access.

Project members never reach those files directly.
The path is outside any project's dataset, and a catalog can only ever name a bundle in its own project.
A reference resolves to a path built from the project id, and a property that tries to extend a reference with a path, or to walk out of it with `..`, is refused when the catalog is created and again when it is resolved.

### How the files reach the query engine

Each Trino pod, the coordinator, every worker and the test coordinator, runs a sidecar container named `mountable-secrets` from the `hopsfs-mount` image.
It mounts the whole store read-only at `trino_mountable_secrets_root`, which defaults to `/opt/hopsworks/mounts`, with `ro`, `nosuid` and `nodev`.
Entries appear as uid 0 with modes that let any user read them, which is what lets the unprivileged Trino process open a wallet.

Two consequences of that sidecar are worth knowing before an upgrade.

It is **privileged**, because FUSE requires it.
On a cluster running the Kyverno restricted policies the chart ships a `PolicyException` for these pods, gated on Kyverno being enabled.
The same privileged FUSE sidecar already runs on the three Airflow deployments in the release namespace, so this is not a new class of workload for the cluster.

The Trino pods have their **own ServiceAccounts**, `hopsworks-trino` and `hopsworks-trino-test`, rather than the namespace default.
An SCC or a cloud identity can therefore be granted to Trino narrowly.
An upgrade from a release before this feature moves those pods off the `default` ServiceAccount, so any binding that named `default` to reach Trino has to be repointed.

!!! warning "OpenShift is not supported"
    The sidecar has to run privileged and as root, so the default restricted SCC rejects it.
    `values.openshift.yaml` therefore turns the store off, and a project on such a cluster cannot supply credential files.
    Note that Trino was already rejected by the restricted SCC before this feature, because the subchart pins `runAsUser: 1000` regardless of `securityContextEnabled`, so the sidecar adds a second reason rather than a new break.

### Turning the store off

Set `global._hopsworks.trino.mountableSecrets.enabled` to `false`, which seeds the `mountable_secrets_enabled` variable and stops the store being offered.
Turning it off is not a single value.
The sidecar entries live in untemplated subchart values, so the `initContainers` lists have to be restated without them, which is what `values.openshift.yaml` does and is the worked example to copy.
The chart fails the render when the flag and the mount disagree, so a half-done change stops the upgrade instead of producing pods that mount nothing.

An **already approved catalog keeps working only as far as its definition**.
Its reference still resolves to a path, but nothing populates that path any more.
For a connector that opens its files when a connection is made, such as Oracle, the coordinator starts cleanly and queries fail.
Sync does not consult the flag, by design, so switching the store off does not quarantine catalogs that already use it.

### Backup

Bundles are HopsFS files.
They are covered by the HopsFS backup, and **not** by the Kubernetes object backup that captures the catalog Secrets and the database.
A restore that brings back the database and the Secrets without the HopsFS path leaves catalogs that reference bundles which no longer exist, and those catalogs fail to authenticate at the next restart.
Recreating the bundle under the same name with the same filenames repairs it without editing any catalog.

### Diagnosing a bundle

There is no admin API for the store, so the checks are on the cluster.

```bash
# What the query engine can actually see for project <id>
kubectl exec -n hopsworks <trino-pod> -c <trino-container> -- ls -l /opt/hopsworks/mounts/<id>/<bundle>

# The mount itself, including its options
kubectl exec -n hopsworks <trino-pod> -c <trino-container> -- grep /opt/hopsworks/mounts /proc/mounts

# The source side
kubectl exec -n hopsworks <namenode-pod> -- /srv/hops/hadoop/bin/hdfs dfs -ls /apps/mountable-secrets/<id>
```

Check the mount on a **worker** and not only on the coordinator, since a query reads the source from the workers.
A missing mount is otherwise invisible: the sidecar mounts into its own filesystem, both containers report ready, and only a `${HOPSWORKS_MOUNT:...}` reference resolving to an empty directory gives it away.

The outbound addresses a data source must admit are reported in the project's Catalogs tab only when `global._hopsworks.trino.mountableSecrets.egressProbe.echoUrl` is set.
It is empty by default, because the probe otherwise calls a third-party service from every Trino pod on every start, and with it unset the UI reports that the addresses could not be determined.
Without it:

```bash
kubectl exec -n hopsworks <trino-pod> -c <trino-container> -- curl -s https://ifconfig.me
```

## Configuration

Trino behavior can be customized through cluster configuration variables. To modify these settings, navigate to **Cluster Settings** → **Configuration** and search for the variable name.

**Available Variables:**

- **trino_enabled**: Enable or disable Trino cluster-wide (default: `true`)
- **trino_default_catalog**: Default catalog used for Superset queries (default: `hive`)
- **trino_test_coordinator_enabled**: Enable the optional test coordinator that backs the "Test connection" action for user-created catalogs (default: `true`)
- **trino_catalog_reconcile_enabled**: Rebuild the user-catalog Secrets from the database on a schedule, for a cluster that has lost them (default: `false`, see [Recovering catalog files lost from the mount][recovering-catalog-files-lost-from-the-mount])
- **trino_catalog_max_per_project**: Catalogs a *newly created* project may create (default: `10`).
  It seeds each project's own allowance, which is then edited per project under Cluster Settings, Projects; changing it does not move the allowance of a project that already exists.
- **trino_catalog_max_bytes**: Largest a single catalog definition may be once its secret references are resolved, in bytes (default: `16384`)
- **trino_max_catalogs**: Catalogs the whole cluster may have, across every project (default: `250`, which is also the ceiling).
  Each catalog is a file the query engine loads at startup, so the setting may lower the bound but never raise it.
- **trino_scheduled_restart_enabled**: Apply pending catalog changes with a scheduled restart (default: `true`).
  Safe to leave on, because the restart is skipped entirely when no catalog change is pending.
- **trino_scheduled_restart_interval_hours**: How often the scheduled restart fires (default: `24`).
  Edited from the Catalog lifecycle card as "every N hours/days".
- **trino_scheduled_restart_time**: Anchor time of day for the cadence, `HH:mm` in the server's timezone (default: `02:00`).
  Off-peak by default because the restart cancels every running query.
- **trino_scheduled_restart_idle_wait_minutes**: How long a due scheduled restart waits for the cluster to go quiet before restarting anyway (default: `60`).
  Bounded, because a permanently busy cluster must not defer catalog changes forever.
- **trino_scheduled_restart_idle_retry_minutes**: How long to wait between those quiet-moment re-checks (default: `5`).
- **trino_eager_restart**: Restart ahead of the schedule the moment the query engine is idle while changes are pending (default: `false`).
- **trino_eager_restart_poll_minutes**: How often the eager restart looks for that idle moment (default: `10`).
- **trino_catalog_approval_required**: Require an administrator to apply every catalog change (default: `false`).
  Turning it on cancels the scheduled restart timers entirely, because approval means nothing goes live unattended.

These settings control the availability and default behavior of the Trino query engine across your Hopsworks cluster.

### Mountable secret settings

These are not all editable the same way, so they are listed apart from the variables above.

Three are seeded by the chart and belong to Helm, not to the variables table.

| Setting | Helm value | Seeded default |
| --- | --- | --- |
| `mountable_secrets_enabled` | `global._hopsworks.trino.mountableSecrets.enabled` | `true` |
| `mountable_secrets_path` | `global._hopsworks.trino.mountableSecrets.storeRoot` | `/apps/mountable-secrets` |
| `trino_mountable_secrets_root` | `global._hopsworks.trino.mountableSecrets.mountPath` | `/opt/hopsworks/mounts` |

Change these through your Helm values and an upgrade.
Editing the row instead moves only one end of the arrangement: the store root also presets the HopsFS directory and is passed to the mount sidecar as its source, and the mount root is what the Trino containers actually mount, so a row edited on its own points the backend at a path nothing is mounted from.
The chart keeps the two ends together, and refuses to render when the flag and the mount disagree.
Note also that the code's own fallback for the flag is `false`, which is what a cluster whose chart predates the row gets; the chart seeds `true`.

The five per-project limits have no seeded row at all.
The code's defaults apply until an administrator creates one, so searching for them in Cluster Settings finds nothing on a fresh cluster, which is expected rather than a fault.

| Setting | Default | What it caps |
| --- | --- | --- |
| `mountable_secret_max_per_project` | `10` | bundles one project may hold |
| `mountable_secret_max_files` | `32` | files in one bundle |
| `mountable_secret_max_file_bytes` | `1048576` | largest single file, in bytes |
| `mountable_secret_max_project_bytes` | `16777216` | a project's total across all its bundles, in bytes |
| `max_mountable_secret_upload_bytes` | `33554432` | largest upload request, refused before the body is read |

Turning the store off is described in [Turning the store off][turning-the-store-off].

### Test coordinator resource cost

`trino_test_coordinator_enabled` is on by default, and enabling it runs **an additional single-node Trino coordinator pod** for the lifetime of the cluster.
It exists only to connection-test user catalogs before they are approved, so on a small or cost-sensitive cluster it is reasonable to turn it off.
When it is off, "Test connection" reports that testing is unavailable and every other part of the catalog workflow is unaffected.

### Supported connectors

A project can create a catalog on any connector installed in the Trino image.
Connectors that expose no external data source are rejected: `system` and `jmx` (which would expose the query engine's own internals, including other projects' query text), `memory` and `blackhole` (which hold no data), `datasketches` and `ai` (function plugins), and `tpch` and `tpcds`, which already ship as shared read-only catalogs.

The installed set is the cluster variable `trino_connectors`, whose default matches the Trino image the chart pins.
The backend refuses a catalog on anything outside it, so a connector name that is not installed is rejected when the catalog is created rather than stopping the coordinator at the next restart.
The connector picker in the project UI is served from the same list, so it offers exactly what the backend accepts.

Change `trino_connectors` only when running an image with a different plugin set.
Removing a connector from the list does not affect catalogs already created on it.

### Catalog storage capacity

User-created catalogs are stored across a fixed number of Kubernetes Secrets, set by the Helm value `global._hopsworks.trino.userCatalogShards` (default: `2`).
Each Secret holds up to roughly 800 KiB of catalog definitions, so the default gives about 1.6 MiB in total, which is a large number of catalogs.
When they are full, an approval fails with an error naming the limit.

Raise the value in your Helm values to add capacity.
The chart mounts one source per shard and refuses to render if the two disagree, so a mismatch fails the upgrade rather than silently dropping catalogs.

Two per-catalog limits keep one project from consuming that shared budget.
`trino_catalog_max_per_project` caps how many catalogs a project may create, and `trino_catalog_max_bytes` caps how large a single definition may be.
The size is measured after `${HOPSWORKS_SECRET:}` references are resolved, because the resolved form is what occupies a Secret: a stored definition is bounded by its database column, but a reference costs a couple of dozen characters and expands to a secret of up to about 10 KiB, and the same secret may be referenced repeatedly, so a row that fits its column can resolve to megabytes.
The check therefore runs both when a catalog is created, so its owner hears about it, and again at approval, because a secret can be rotated to a larger value in between.

Both defaults are generous against real catalogs, which are a few hundred bytes; the largest legitimate ones inline a service account JSON or a certificate pair and stay a few KiB.
Raise them for a project with an unusual number of external sources, and remember that the product of the two bounds a single project's share of the shard budget.

## Best Practices for Trino Management

- **Monitor regularly**: Check cluster overview daily to spot trends and issues early
- **Review slow queries**: Investigate queries with long execution times in the query history
- **Balance workload**: Ensure workers are evenly distributed and not overloaded
- **Scale appropriately**: Add workers during peak usage periods if resources are constrained
- **Track growth**: Monitor query volume trends to plan for future capacity needs
