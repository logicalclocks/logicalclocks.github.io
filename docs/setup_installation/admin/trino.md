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

## Catalogs and the Scheduled Restart

Projects create and change their own Trino catalogs, but a catalog change only takes effect once the query engine restarts and reloads its catalogs.
Two mechanisms apply pending changes: a daily scheduled restart, and the administrator's **Catalogs** view.

### Pending catalog requests

The **Catalogs** tab in the admin query engine view lists every pending catalog operation: creations, updates, and deletions waiting for a restart.
All pending requests are selected by default.
Clicking **Restart Trino** applies the selected operations in one action: they are synced to the query engine's configuration first, and the query engine is restarted after, behind a dialog that confirms what is about to be applied.
A restart without the sync would load nothing, because a newly created catalog is only a record until its definition is written out.

You can also **Delete** an individual pending request, which rejects that change without applying it.

The restart interrupts queries running anywhere on the cluster, so check the query history for activity first.

### Quarantine

The query engine exits when it cannot load a catalog, so one bad catalog definition would otherwise stop the whole cluster from starting.
A restart therefore quarantines any catalog the query engine cannot load and recovers without it.
The restart result names the quarantined catalogs, and each carries its load error on its page in the owning project.

### Scheduled restart

A scheduled restart applies pending catalog changes daily, so a project's catalog goes live without an administrator.
The tick does nothing at all unless a catalog change is actually pending, so a cluster whose catalogs are all loaded is never interrupted.

For clusters where cancelling a query is worse than a catalog going live late, the restart can be gated on the query engine being idle.
A busy cluster is then re-checked on an interval for a bounded time, and if it never goes idle the changes wait for the next day's tick rather than being applied over a running query.

## Configuration

Trino behavior can be customized through cluster configuration variables. To modify these settings, navigate to **Cluster Settings** → **Configuration** and search for the variable name.

**Available Variables:**

- **trino_enabled**: Enable or disable Trino cluster-wide (default: `true`)
- **trino_default_catalog**: Default catalog used for Superset queries (default: `hive`)
- **trino_scheduled_restart_enabled**: Apply pending catalog changes with a daily restart (default: `true`).
  Safe to leave on, because the restart is skipped entirely when no catalog change is pending.
- **trino_scheduled_restart_time**: Time of day for the scheduled restart, `HH:mm` in the server's timezone (default: `02:00`).
  Off-peak by default because the restart cancels every running query.
- **trino_scheduled_restart_only_when_idle**: Only restart when no query is running, queued, or blocked (default: `false`).
  Turn it on when cancelling a query is worse than a catalog going live late; the cost is that a catalog can miss its window on a busy cluster.
- **trino_scheduled_restart_idle_retry_minutes**: How long to wait between idle re-checks when the cluster is busy (default: `15`).
- **trino_scheduled_restart_idle_max_wait_minutes**: How long to keep re-checking before giving up until the next day (default: `240`).
  Expiry gives up rather than restarting anyway, because the idle gate was turned on to say exactly that.

These settings control the availability and default behavior of the Trino query engine across your Hopsworks cluster.

## Best Practices for Trino Management

- **Monitor regularly**: Check cluster overview daily to spot trends and issues early
- **Review slow queries**: Investigate queries with long execution times in the query history
- **Balance workload**: Ensure workers are evenly distributed and not overloaded
- **Scale appropriately**: Add workers during peak usage periods if resources are constrained
- **Track growth**: Monitor query volume trends to plan for future capacity needs
