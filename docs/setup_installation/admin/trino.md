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

<figure>
  <img src="../../../assets/images/admin/trino/catalogs-pending.png" alt="Pending catalogs" />
  <figcaption>Catalogs awaiting sync and restart</figcaption>
</figure>

### Syncing

Select the catalogs to apply and click "Sync selected".
This writes the catalog definitions into the backend-owned ConfigMap that the cluster mounts.
Any `${HOPSWORKS_SECRET:...}` reference is resolved to its value only at this step, so secrets are never stored in the catalog database rows.
After syncing, a catalog moves to Pending restart, meaning it is present in the ConfigMap but not yet loaded by the running cluster.

<figure>
  <img src="../../../assets/images/admin/trino/catalogs-pending-restart.png" alt="Catalogs pending restart" />
  <figcaption>Synced catalogs wait in Pending restart until the next restart</figcaption>
</figure>

### Restarting

Trino reads catalogs only at startup, so synced changes take effect on the next restart.
Click "Restart Trino" to roll out the coordinator and workers.
The confirmation dialog reports how many queries are currently running or queued, because the restart interrupts them, so you can choose a low-traffic window before confirming.

<figure>
  <img src="../../../assets/images/admin/trino/restart-confirm.png" alt="Restart confirmation" />
  <figcaption>The restart confirmation reports the running queries the restart will interrupt</figcaption>
</figure>

A restart is refused while another sync or restart is already running, and while a rollout is still in progress, so concurrent actions by different administrators cannot collide or trigger redundant restarts.

## Configuration

Trino behavior can be customized through cluster configuration variables. To modify these settings, navigate to **Cluster Settings** → **Configuration** and search for the variable name.

**Available Variables:**

- **trino_enabled**: Enable or disable Trino cluster-wide (default: `true`)
- **trino_default_catalog**: Default catalog used for Superset queries (default: `hive`)
- **trino_test_coordinator_enabled**: Enable the optional test coordinator that backs the "Test connection" action for user-created catalogs (default: `true`)

These settings control the availability and default behavior of the Trino query engine across your Hopsworks cluster.

## Best Practices for Trino Management

- **Monitor regularly**: Check cluster overview daily to spot trends and issues early
- **Review slow queries**: Investigate queries with long execution times in the query history
- **Balance workload**: Ensure workers are evenly distributed and not overloaded
- **Scale appropriately**: Add workers during peak usage periods if resources are constrained
- **Track growth**: Monitor query volume trends to plan for future capacity needs
