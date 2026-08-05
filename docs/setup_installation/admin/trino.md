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

Catalogs created by project Data Owners are saved to the database but are not loaded by the running cluster until an administrator applies them.
Applying a catalog is a two-step, admin-gated workflow on the Catalogs tab under Cluster Settings, Query Engine: sync the pending changes, then restart Trino.

The tab lists every catalog waiting to be applied, along with its status and the operation to apply (create, update, or remove).

Nothing notifies you when a Data Owner creates a catalog, and nothing notifies them when you apply it.
A catalog waits in Pending sync until an administrator acts, with no service level attached, so check this tab periodically or agree a cadence with your projects.

<figure>
  <img src="../../../assets/images/admin/trino/catalogs-pending.png" alt="Pending catalogs" />
  <figcaption>Catalogs awaiting sync and restart</figcaption>
</figure>

### Syncing

Select the catalogs to apply and click "Sync selected".
This writes the catalog definitions into the backend-owned Kubernetes Secrets that the cluster mounts at `/etc/trino/catalog`.
After syncing, a catalog moves to Pending restart, meaning it is present in the mount but not yet loaded by the running cluster.

#### Where catalog credentials are stored

A connector's credentials end up in the places below. Anyone who can read those places can read the credentials, so plan access to them accordingly.

- A `${HOPSWORKS_SECRET:<name>}` reference is stored verbatim in the `trino_catalog` database row and is resolved to its value only at sync time. The database row never holds the value.
- A literal value typed straight into the properties editor is stored as-is in the `trino_catalog` database row, in cleartext, and is captured by database backups. Use a secret reference for any credential you do not want in the database.
- Either way, the synced file holds the resolved plaintext, because Trino reads the credential from the catalog file itself. That file lives in a Kubernetes Secret rather than a ConfigMap, so it is covered by the RBAC that applies to Secrets in the Hopsworks namespace and by etcd encryption-at-rest on clusters that enable it.

<figure>
  <img src="../../../assets/images/admin/trino/catalogs-pending-restart.png" alt="Catalogs pending restart" />
  <figcaption>Synced catalogs wait in Pending restart until the next restart</figcaption>
</figure>

### Restarting

Trino reads catalogs only at startup, so synced changes take effect on the next restart.
Click "Restart Trino" to roll out the coordinator and workers.
The confirmation dialog reports how many queries are currently running or queued, so you can choose a low-traffic window before confirming.
The restart cancels those queries for **every project on the cluster**, not only the project whose catalog is being applied, and in-flight results are lost.
Trino keeps recent query detail in the coordinator's memory, so after a restart the live query views show only what the new coordinator has seen; older queries remain in the query history, which is stored separately.

<figure>
  <img src="../../../assets/images/admin/trino/restart-confirm.png" alt="Restart confirmation" />
  <figcaption>The restart confirmation reports the running queries the restart will interrupt</figcaption>
</figure>

A restart is refused while another sync or restart is already running, so concurrent actions by different administrators cannot collide or trigger redundant restarts.
If nothing is waiting to load or unload, the restart is skipped and reported as such rather than interrupting queries for no reason.

### Recovering a catalog Trino cannot load

Trino reads its catalogs at startup and refuses to start if it cannot load one of them.
A user catalog with an invalid definition therefore stops the whole query engine, coordinator and workers alike, and the pods stay in `CrashLoopBackOff`.
Kubernetes keeps the previous pods serving while the new ones fail, so queries may keep working for a while and the rollout never completes.

Click "Restart Trino" to recover.
The button stays available when nothing is pending, labelled "Restart Trino (recover)", because this situation leaves no pending catalog to act on.

<figure>
  <img src="../../../assets/images/admin/trino/catalogs-recover.png" alt="Recover restart" />
  <figcaption>With no pending catalogs, the restart action is still available to recover a failed rollout</figcaption>
</figure>

Hopsworks reads the coordinator log, identifies the catalog Trino rejected, removes it from the mount, marks it **Failed**, and restarts so the cluster comes back without it.
The result names the catalogs that were removed:

> Removed 1 catalog Trino could not load. `project1__orders_pg`. Trino is restarting without them; the owners must fix the definitions.

Only user-created catalogs are removed this way.
A default catalog that fails to load is left in place, because that is a cluster configuration problem rather than something an administrator should resolve by deleting data.

A removed catalog keeps its row, so its owner can see what happened on the project's Catalogs page along with the error Trino reported.
Editing the definition returns it to Pending sync and it re-enters the normal flow.

<figure>
  <img src="../../../assets/images/guides/trino/catalog-failed.png" alt="Failed catalog" />
  <figcaption>The owner sees the failure and the reason Trino gave</figcaption>
</figure>

Failed catalogs are not listed under pending, because they no longer block anything and no administrator action can fix them.
If Hopsworks cannot attribute the failure to a user catalog, it reports the connection error instead of removing anything, and the coordinator log is the place to look.

## Configuration

Trino behavior can be customized through cluster configuration variables. To modify these settings, navigate to **Cluster Settings** → **Configuration** and search for the variable name.

**Available Variables:**

- **trino_enabled**: Enable or disable Trino cluster-wide (default: `true`)
- **trino_default_catalog**: Default catalog used for Superset queries (default: `hive`)
- **trino_test_coordinator_enabled**: Enable the optional test coordinator that backs the "Test connection" action for user-created catalogs (default: `true`)

These settings control the availability and default behavior of the Trino query engine across your Hopsworks cluster.

### Test coordinator resource cost

`trino_test_coordinator_enabled` is on by default, and enabling it runs **an additional single-node Trino coordinator pod** for the lifetime of the cluster.
It exists only to connection-test user catalogs before they are synced, so on a small or cost-sensitive cluster it is reasonable to turn it off.
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
When they are full, a sync fails with an error naming the limit.

Raise the value in your Helm values to add capacity.
The chart mounts one source per shard and refuses to render if the two disagree, so a mismatch fails the upgrade rather than silently dropping catalogs.

## Best Practices for Trino Management

- **Monitor regularly**: Check cluster overview daily to spot trends and issues early
- **Review slow queries**: Investigate queries with long execution times in the query history
- **Balance workload**: Ensure workers are evenly distributed and not overloaded
- **Scale appropriately**: Add workers during peak usage periods if resources are constrained
- **Track growth**: Monitor query volume trends to plan for future capacity needs
