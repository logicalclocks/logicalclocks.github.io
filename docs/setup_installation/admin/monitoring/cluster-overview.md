---
description: Inspect Hopsworks services, Kubernetes workloads, RonDB memory, alerts, and resource recommendations from Cluster Settings.
---

# Cluster overview { #hopsworks-cluster-overview }

Sign in as a Hopsworks administrator, open your user menu, and select **Cluster Settings** > **Overview**.
The overview shows platform service health and items that need attention.
Use the overview tiles or its sidebar pages to investigate the affected service or resource.

Snapshot times show when Hopsworks obtained the data.
If a refresh fails and an older snapshot is available, the page identifies it as stale.
Check the snapshot time and any unavailable-data notices before acting on a reading.

## Inspect Kubernetes resources { #cluster-overview-kubernetes }

- Open **Workloads** to check replica readiness, failed runs, events, and the pods controlled by a workload.
- Open **Pods** and select a pod to inspect its container states, restart counts, resource requests and limits, and recent events.
  On a platform pod, open **Logs** and choose a container to read or download its logs if the Hopsworks service account has access.
- Open **Events** to inspect Kubernetes events, including warnings about scheduling, pulls, and mounts.
- Open **Nodes** to check node conditions and capacity when Hopsworks has permission to list nodes.
  Resource usage also depends on metrics availability.
  If the node reports allocatable ephemeral storage, check how much of it pods request.
- Open **Storage** to see persistent volume claims and their measured usage where available.
- Open **Registry** to see tags, sizes, referenced images, and possible cleanup candidates for the built-in registry.
  Identifying a candidate leaves the image in the registry.

The namespace selector lists the platform namespace and other namespaces available to the installation.
Select a project namespace in **Workloads**, **Pods**, **Events**, or **Storage** to inspect that project's Kubernetes objects.
Pod logs and resource recommendations are available for platform namespaces.

For a custom Kubernetes role, check the [cluster overview upgrade permissions][upgrade-cluster-overview-access].
For indexed logs across services and time ranges, see [Services Logs][services-logs].

## Review alerts and changes { #cluster-overview-alerts }

Open **Alerts** for currently firing alerts and automated checks for known operational issues.
Check the time and coverage of the data behind each result.

Open **Changes** to correlate Kubernetes changes and Helm releases with the time an issue began.
Open **Certificates** to inspect expiry for certificates issued by the Hopsworks certificate operator.

## Interpret RonDB memory { #cluster-overview-rondb }

Open **RonDB** to compare data-node status and DataMemory usage and to search table allocations by database and table name.
The overview tile reports the highest DataMemory utilization among data nodes with readings.
The RonDB page reports node status, DataMemory, and table allocation independently, so available readings remain visible if one source is unavailable.

- **DataMemory used** and **DataMemory total** describe the shared DataMemory pool on each node.
  Check individual nodes and whether all data nodes have a reading when assessing how much the cluster can grow.
- **Allocated memory** and **Allocated disk** describe the space allocated to a table.
  The **Free within** columns describe unused space within those allocations.
  Use per-node DataMemory for cluster capacity planning, since tables share that pool and can request further allocations.
  Table allocation alone cannot establish a row growth limit.

The table listing is capped at the 10,000 tables with the largest memory allocations.
When the page reports an incomplete listing, search and counts cover only the retained tables.

## Review resource recommendations { #cluster-overview-recommendations }

Open **Recommendations** and select a workload to review CPU, memory, and replica advice.
Check the observation window, its sample coverage, and whether the pod template changed during that window.
Use a window that covers your busiest periods and the current workload configuration.

1. After changing the namespace or a filter, wait for the table to finish refreshing.
   Select the workloads you intend to change and choose **Values file**.
2. Review the proposed values, the included workloads, and any fields that were skipped or require a manual change.
3. Check the namespace and chart version in the suggested Helm command and review the file against your release values.
4. Check requests, namespace quotas, and capacity during the rollout.
   Stage changes that compete for headroom, especially workloads with local volumes that need to stay on a specific node.
5. Apply the reviewed values through your normal [Hopsworks upgrade procedure][upgrade-before-every-upgrade], and check workload readiness before applying the next group.

The recommendations and capacity checks use observed metrics and the available cluster data.
The placement check estimates whether the requested resources fit and cannot predict the order in which Kubernetes schedules replacement pods.
Downloading the file leaves the cluster unchanged.

For a support archive or an interactive shell, see [Cluster diagnostics][hopsworks-cluster-diagnostics].
