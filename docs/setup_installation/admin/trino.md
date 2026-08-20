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

Saving reprograms the schedule immediately, without a redeploy.

### The wait for a quiet moment

A due scheduled restart does not fire into a busy cluster immediately.
It waits for the cluster to have no query running, queued, or blocked, re-checking every few minutes for up to an hour, and then restarts anyway: the wait buys a quiet moment when one exists, and the bounded give-up keeps a permanently busy cluster from deferring catalog changes forever.

### Quarantine

The query engine exits when it cannot load a catalog, so one bad catalog definition would otherwise stop the whole cluster from starting.
A restart therefore quarantines any catalog the query engine cannot load and recovers without it.
The restart result names the quarantined catalogs, and each carries its load error on its page in the owning project.

## Configuration

Trino behavior can be customized through cluster configuration variables. To modify these settings, navigate to **Cluster Settings** → **Configuration** and search for the variable name.

**Available Variables:**

- **trino_enabled**: Enable or disable Trino cluster-wide (default: `true`)
- **trino_default_catalog**: Default catalog used for Superset queries (default: `hive`)
- **trino_scheduled_restart_enabled**: Apply pending catalog changes with a scheduled restart (default: `true`).
  Safe to leave on, because the restart is skipped entirely when no catalog change is pending.
- **trino_scheduled_restart_interval_hours**: How often the scheduled restart fires (default: `24`).
  Edited from the Catalog lifecycle card as "every N hours/days".
- **trino_scheduled_restart_time**: Anchor time of day for the cadence, `HH:mm` in the server's timezone (default: `02:00`).
  Off-peak by default because the restart cancels every running query.
- **trino_catalog_approval_required**: Require an administrator to apply every catalog change (default: `false`).
  Turning it on cancels the scheduled restart timers entirely, because approval means nothing goes live unattended.
- **trino_eager_restart**: Restart ahead of the schedule the moment the query engine is idle while changes are pending (default: `false`).
- **trino_eager_restart_poll_minutes**: How often the eager restart looks for that idle moment (default: `10`).
- **trino_scheduled_restart_idle_wait_minutes**: How long a due scheduled restart waits for the cluster to go quiet before restarting anyway (default: `60`).
  Bounded, because a permanently busy cluster must not defer catalog changes forever.
- **trino_scheduled_restart_idle_retry_minutes**: How long to wait between those quiet-moment re-checks (default: `5`).
- **trino_max_catalogs**: Catalogs the whole cluster may have, across every project (default: `250`, which is also the ceiling).
  Each catalog is a file the query engine loads at startup, so the setting may lower the bound but never raise it.

These settings control the availability and default behavior of the Trino query engine across your Hopsworks cluster.

## Best Practices for Trino Management

- **Monitor regularly**: Check cluster overview daily to spot trends and issues early
- **Review slow queries**: Investigate queries with long execution times in the query history
- **Balance workload**: Ensure workers are evenly distributed and not overloaded
- **Scale appropriately**: Add workers during peak usage periods if resources are constrained
- **Track growth**: Monitor query volume trends to plan for future capacity needs
