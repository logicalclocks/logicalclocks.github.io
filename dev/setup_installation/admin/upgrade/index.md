# Upgrading Hopsworks { #upgrading-hopsworks }

## Introduction

Upgrade a self-managed Hopsworks cluster one minor release at a time, in order.
Skipping a minor release is not supported, and for OpenSearch it fails at startup.
This page covers upgrades from 5.0.x and later.
The commands assume Hopsworks is installed in the `hopsworks` namespace.

| Upgrade | OpenSearch | What needs action |
| ------- | ---------- | ----------------- |
| [5.0.x to 5.1.x][upgrade-50-to-51] | 1.3.x to 2.19.x | Kubernetes 1.34 or later before the upgrade, a first Helm 4 upgrade, and from 5.0.13 or earlier to 5.1.2 or later [the Trino query history][upgrade-trino-query-history]. |
| [5.1.x to 5.2.x][upgrade-51-to-52] | 2.19.x to 3.8.0: upgrade to 5.2.1 or later | The index pass, Kafka moves to KRaft, KEDA, Kubernetes 1.37 only afterwards, Trino, and from 5.2.2 [OnlineFS and the schema migrations][upgrade-changes-from-522]. |
| [5.2.x to 5.3.x][upgrade-52-to-53] | stays on 3.8.0 | ICEBERG feature groups in Trino, the Filebeat registry, the memory of the OTLP sidecar of agent deployments, from 5.2.0 [the subset shares in Trino][upgrade-trino-subset-shares] and the OpenSearch security configuration, and from 5.2.0 or 5.2.1 [OnlineFS and the schema migrations][upgrade-changes-from-522]. |

## Before every upgrade { #upgrade-before-every-upgrade }

1. Take a backup and check that it completed, as described in [Disaster Recovery][disaster-recovery].
2. Pass `helm upgrade --timeout` long enough for the hooks of that upgrade.
   The upgrade from 5.1.x to 5.2.x has two that can run for hours: the [OpenSearch index pass][opensearch-set-the-timeout] and the [Kafka migration][kafka4-kraft-upgrade].
3. If you run satellite clusters, read the order in which they upgrade relative to the central cluster, for [OpenSearch][opensearch-satellite-clusters] and for [Kafka][kafka4-before-you-start].
4. If this is the first upgrade of the release with Helm 4, read [Upgrading with Helm 4][upgrading-with-helm-4] first.

## 5.0.x to 5.1.x { #upgrade-50-to-51 }

An upgrade from 5.0.13 or earlier to 5.1.2 or later also stops the Trino query history and strips the details of recorded queries after 7 days, which cannot be undone, as described in [Trino query history][upgrade-trino-query-history].

### Kubernetes 1.34 { #upgrade-kubernetes-134 }

5.1 requires Kubernetes 1.34 or later, up from 1.27 in 5.0, and `helm upgrade` refuses an older Kubernetes cluster.
Upgrade Kubernetes first: 5.0.1 and later support up to 1.36, and 5.0.0 up to 1.34.

### OpenSearch 2.19 { #upgrade-opensearch-219 }

OpenSearch goes from 1.3.x to 2.19.x.
The indices stay as they are, and the upgrade to 5.2 deals with those created by 1.x.
Upgrade from 5.0 to 5.1.2 or later, which avoids the known issues of 5.1.0 and 5.1.1, as described in [Upgrading OpenSearch][opensearch-upgrade-steps] (step 2) and [Security configuration][opensearch-security-configuration].
Then confirm that OpenSearch 2.19 is live and green before the next upgrade, as step 2 there shows.

### First upgrade with Helm 4 { #upgrade-51-helm4 }

The chart changes described in [Upgrading with Helm 4][upgrading-with-helm-4] ship from 5.2.0, so a 5.1.x chart still declares `.spec.replicas` next to the HPA of an autoscaled workload.
A server-side Helm 4 upgrade to 5.1.x therefore fails with `conflict with "kube-controller-manager" with subresource "scale"` on a workload its HPA has rescaled.
A release installed by Helm 3 stays client-side under Helm 4 unless you pass `--server-side=true`, and does not meet that conflict.
An upgrade from 5.0 to 5.1 also conflicted on the `trino-password-file` and `trino-groups-file` Secrets, whose fields the backend owns.
Running it again with `--force-conflicts` overwrites the Trino user database that the backend wrote (`password.db` and `group.db`), so check the Trino users afterwards.
`--force-conflicts` applies to the whole release, as [The RSS ConfigMap][helm4-rss-configmap] explains.

## 5.1.x to 5.2.x { #upgrade-51-to-52 }

### OpenSearch 3.8.0 { #upgrade-opensearch-38 }

Upgrade a 5.1.x cluster to 5.2.1 or later.
OpenSearch 3.8.0 refuses to start on an index created before OpenSearch 2.0, so a `pre-upgrade` hook copies those indices on the running 2.19 cluster first.
Follow [Upgrading OpenSearch][upgrading-opensearch]: it covers what keeps working during the pass, the timeout, the report, vector ingestion and the steps.

### Kafka 4 and KRaft { #upgrade-kafka-kraft }

The upgrade migrates every Kafka from ZooKeeper to KRaft and moves Strimzi from 0.45 to 1.2.
Run the read-only checks in [Before you start][kafka4-before-you-start] first, and read [Kafka 4 and KRaft upgrade notes][kafka4-kraft-upgrade], including the step and the `ignoreDifferences` entry that ArgoCD needs.

### Migration V109 waits for the statistics cleaner { #upgrade-v109-statistics-cleaner }

Up to 5.1.2, a query of the statistics cleaner can take up to an hour on a cluster with many feature statistics; 5.1.3 fixes it.
The 5.1.x pods keep running while the 5.2 schema migrations run, so each statement of migration V109 waits for that query on an upgrade from 5.1.2 or earlier to 5.2.0 or 5.2.1, or to any 5.2 release on a cluster that disables the DDL SQL node.
From 5.2.2 the migrations run on the DDL SQL node and do not wait for it, as described in [Schema migrations run on the DDL SQL node][upgrade-ddl-sql-node].
When you upgrade to 5.2.0 or 5.2.1, or with the DDL SQL node disabled, upgrade to the latest 5.1.x patch first.

If V109 is already waiting, `Waiting for table metadata lock` shows in the processlist next to a `SELECT fds.* FROM hopsworks.feature_descriptive_statistics`.
Scale `hopsworks-instance` to 0, `KILL` that query on its SQL node, and scale `hopsworks-instance` back up once Flyway has finished.

### KEDA { #upgrade-keda }

From 5.2 the chart installs KEDA 2.21 and its HTTP add-on by default (`hopsworks.variables.kube_keda_installed: true`), so this upgrade adds them to every existing release.
[KEDA Autoscaling][keda-autoscaling] describes what the chart installs and what KEDA needs from the cluster.

- **One external metrics provider per Kubernetes cluster.**
  A Kubernetes cluster that already runs KEDA, or the OpenShift Custom Metrics Autoscaler, must have it removed first, or leave the subchart off with `hopsworks.variables.kube_keda_installed: false`, as described in [Cluster requirements][keda-requirements].
- **The CRDs arrive through a pre-upgrade hook.**
  The `keda-crd-upgrade` hook creates the KEDA CRDs before the operators start, as described in [CustomResourceDefinitions][keda-crds].
  It needs the toolbox image, from 5.2.2 also the `hopsworks/keda-crds` image it reads the CRDs from, and a few seconds of the `--timeout`, and no step before `helm upgrade`.
  A failed upgrade to 5.2.0 or 5.2.1 can leave a ConfigMap behind, which [CustomResourceDefinitions][keda-crds] says how to delete.
- **Six more images to mirror on an airgapped cluster**, seven from 5.2.2: `ghcr.io/kedacore/keda`, `keda-metrics-apiserver` and `keda-admission-webhooks`, `ghcr.io/kedacore/http-add-on-operator`, `http-add-on-interceptor` and `http-add-on-scaler`, and from 5.2.2 `hopsworks/keda-crds`.
  [What the chart installs][keda-components] names the values that override them.
- **The upgrade does not change deployments.**
  A Standard-mode deployment keeps its stored scaling configuration.
  Where it named no autoscaler, KEDA runs it from its next start, with the same CPU or memory threshold as before.
  Nothing scales to zero until a minimum of 0 is set.
- **Uninstall takes longer**, because a cleanup hook waits for the KEDA operators before the release is deleted, as described in [Uninstalling][keda-uninstall].

### Kubernetes 1.37 { #upgrade-kubernetes-137 }

5.2 supports Kubernetes up to 1.37, but 5.1.x stops at 1.36.
Upgrade Hopsworks to 5.2.x before you move the Kubernetes cluster to 1.37.

Under ArgoCD before 3.5.0, an Application with the `ServerSideApply=true` sync option stops syncing on Kubernetes 1.37.
Kubernetes 1.37 adds `spec.preventPodSchedulingIfMissing` to every CSIDriver, and the schema built into those ArgoCD versions lacks it, so the Application shows every resource as Unknown and syncs no new revision:

```text
ComparisonError: ... .spec.preventPodSchedulingIfMissing: field not declared in schema
```

Before you move the Kubernetes cluster to 1.37, do one of the following:

- Upgrade ArgoCD to 3.5.0 or later (argo-cd Helm chart 10.2.3 or later), after reading its [3.4 to 3.5 upgrade notes](https://argo-cd.readthedocs.io/en/stable/operator-manual/upgrading/3.4-3.5/).
  For Hopsworks three of them matter.
  Charts render with Helm 4.2, and `helm.version: v3` is ignored.
  An OCI chart registry over plain HTTP needs `insecureOCIForceHttp: "true"` in its repository Secret, which has no effect if `insecure: "true"` is also set.
  An HPA without metrics is now Degraded, so a sync right after a deploy can fail on the Knative `activator` HPA until `syncPolicy.retry` runs it again; to accept such HPAs, [override](https://argo-cd.readthedocs.io/en/stable/operator-manual/health/) the `autoscaling_HorizontalPodAutoscaler` health check in `argocd-cm`.
- Stay on your ArgoCD version and add this to the Application:

    ```yaml
    spec:
      ignoreDifferences:
        - group: storage.k8s.io
          kind: CSIDriver
          jsonPointers:
            - /spec/preventPodSchedulingIfMissing
    ```

### Trino query history { #upgrade-trino-query-history }

From 5.0.14, 5.1.2 and 5.2.0 the chart no longer enables the Trino MySQL event listener, so `hopsworks.trino_queries` stops receiving rows, and the administrators' Trino query history shows only what was recorded before the upgrade.
To keep it, add the listener in your values:

```yaml
trino:
  trino:
    additionalConfigProperties:
      - internal-communication.shared-secret=${ENV:TRINO_SHARED_SECRET}
      - http-server.process-forwarded=true
      - event-listener.config-files=etc/mysql-event-listener.properties
    coordinator:
      additionalConfigFiles:
        mysql-event-listener.properties: &mysqlEventListenerProperties |
          event-listener.name=mysql
          mysql-event-listener.db.url=jdbc:mysql://${ENV:MYSQL_ADDRESS}/${ENV:MYSQL_DB}?user=${ENV:MYSQL_USER}&password=${ENV:MYSQL_PASSWORD}&useSSL=false&allowPublicKeyRetrieval=true
    worker:
      additionalConfigFiles:
        mysql-event-listener.properties: *mysqlEventListenerProperties
```

`additionalConfigProperties` replaces the chart's list, so it must repeat the chart's other entries.
Both roles need the file, because the property reaches the workers too.

From the same releases, recorded rows also lose their query text, plan and JSON columns after `hopsworks.variables.trino_events_strip_details_after_days` (7) days.
User, state, timing and resource columns stay until `trino_events_delete_after_days` (61).
The first nightly cleanup after the upgrade strips every existing row older than 7 days.
Set the value to 61 or more to keep the details.

### Feature groups shared with a subset of their features { #upgrade-trino-subset-shares }

From 5.2.1, Trino serves feature groups shared with a subset of their features through `delta_shared`, `hudi_shared` and `iceberg_shared` only while `hopsworks.variables.trino_feature_group_subset_shares_enabled` is `"true"`.
It defaults to `"false"`.
Shares of a whole feature group, and the online and embedding access of a subset share, do not depend on it.

Those catalogs read HopsFS as a superuser, and a data owner writes the table metadata that names a shared table's data files, so through the metastore they can point that table at another project's files.
Keep the value at `"false"`.

### `consul-server-acl-init` fails with `field is immutable` { #upgrade-consul-acl-init }

The upgrade can fail on the `consul-server-acl-init` Job with `spec.template: field is immutable`.
Delete that Job and run the upgrade again.

## 5.2.x to 5.3.x { #upgrade-52-to-53 }

OpenSearch stays on 3.8.0.
An upgrade from 5.2.0 or 5.2.1 also gets the [changes from 5.2.2][upgrade-changes-from-522].
An upgrade from 5.2.0 also crosses two changes of 5.2.1, described under 5.1.x to 5.2.x: [Feature groups shared with a subset of their features][upgrade-trino-subset-shares], and the OpenSearch [Security configuration][opensearch-security-configuration], which takes away the read access of restricted project members.

### ICEBERG feature groups in Trino { #upgrade-iceberg-trino }

From 5.3, the Trino `iceberg` catalog reads an ICEBERG feature group on HopsFS once Hopsworks has registered its current Iceberg metadata in the Hive metastore.
Hopsworks does that on every commit, and when the client syncs after an empty save or a schema change, so a feature group created before the upgrade is readable from Trino after its next write.

To register every existing ICEBERG feature group at once, call the backfill endpoint as an administrator, passing the returned `nextAfterId` as `afterId`, until it is null:

```text
POST /hopsworks-api/api/admin/featurestore/iceberg/metastore/backfill?afterId=0&limit=100
```

Each item of the response reports one feature group:

- `PUBLISHED`: registered now.
- `UP_TO_DATE`: already registered.
- `NO_METADATA`: nothing committed yet.
- `SKIPPED`: not mirrored, or deleted.
- `FOREIGN_LOCATION`: its metastore table is not at the feature group's location, so it is not registered.
- `FAILED`: with the error.

The call is safe to repeat.
Each feature group costs a few HopsFS reads and one metastore update, and there is no outage.

Two Trino changes come with it:

- The `hive` catalog no longer reads ICEBERG feature groups, because the Trino Hive connector refuses tables registered as Iceberg.
  Queries and Superset datasets that read them through `hive` must move to `iceberg`.
- In the `iceberg` catalog the feature store schema is read-only, for data owners too.

Spark access by name (`spark.table`, `spark.sql`, `DESCRIBE`) to an ICEBERG feature group needs the Iceberg storage handler on the Spark classpath, which the base images carry from 5.2.
Custom Python environments are not rebuilt on upgrade: a project environment cloned from a release before 5.2 keeps its own image, built from that release's base.
Once a feature group is registered as `table_type=ICEBERG`, at its next commit or by the backfill, access by name from such an environment fails with `Failed to load storage handler` until the environment is rebuilt.
Installing or uninstalling a library rebuilds the environment from the current base image.
Reads and writes by path through the feature store client are not affected.

### Filebeat registry { #upgrade-filebeat-registry }

Releases before 5.3 mounted the Filebeat registry at a path Filebeat never wrote to, so every Filebeat restart, pod re-creation and `helm upgrade` shipped all of a node's current container logs again into `.services-*` and the project log indices.
On the upgrade to 5.3:

- The registry moves to `/var/lib/filebeat-data/<namespace>` on each node.
  That directory starts empty, so each node ships its current container logs once more, as every restart did before.
  Later restarts and upgrades resume from the registry.
- Leave the existing contents of `/var/lib/filebeat-data` in place.
  Nothing in the chart reads them, and they may belong to another Filebeat on the node.

### Agent deployments reserve 2 GiB for their OTLP sidecar { #upgrade-agent-otlp-sidecar }

An agent deployment with tracing enabled runs a `hops-otlp` sidecar next to the agent.
`hopsworks.variables.agent_deployment_otel_memory_mb` is both the memory request and the memory limit of that container, so the value is reserved on the node, not only allowed.
From 5.3 the default is 2048, up from 1024, because at 1 GiB the sidecar was OOM-killed under ordinary traffic.

- **Check capacity before you redeploy.**
  A cluster that runs N traced agent deployments reserves 2 GiB x N for their sidecars, where it reserved 1 GiB x N.
  On nodes sized for the old default, an agent pod recreated after the upgrade can stay `Pending` for lack of memory.
  Count the traced agent deployments against the free memory of the nodes that schedule them before you redeploy them.
- **Running pods keep the old reservation until they are recreated.**
  The upgrade does not restart agent deployments, so nothing changes for a running one until it is stopped and started, saved, or rescheduled.
  The increase arrives one deployment at a time, which is also why a shortage shows up later than the upgrade.
- **Keeping 1024 keeps the OOM.**
  `hopsworks.variables.agent_deployment_otel_memory_mb: "1024"` pins the old value on a cluster that cannot spare the memory, at the cost the increase removes.
  The buffering fixes in the 5.3 sidecar image make an OOM much less likely than before, because what the sidecar holds no longer grows with how far the feature store write falls behind, but it remains the trade.
- **What an OOM looks like.**
  `hops-otlp` is an ordinary second container without probes, so the OOM kill restarts that container alone: the agent container's `restartCount` stays 0, and only the sidecar's `lastState` shows `OOMKilled`.
  While the sidecar restarts, the pod reports `Ready=False` and leaves the endpoints of its service, so the agent, healthy and still running, receives no requests.
  Looking for agent restarts finds none.

## Changes from 5.2.2 { #upgrade-changes-from-522 }

These changes ship in 5.2.2 and 5.3.0.
They apply to an upgrade from 5.1.x to 5.2.2 or later, from 5.2.0 or 5.2.1 to a later 5.2 release, and from 5.2.0 or 5.2.1 to 5.3.

### OnlineFS drops records that arrive on another topic { #upgrade-onlinefs-topics }

OnlineFS writes a record only if it arrived on the online topic of the feature group that its headers name.
Before, the headers alone decided, so a producer could write into another project's online feature groups.
A record that fails the check is dropped, logged by OnlineFS (`Record dropped, it did not arrive on the online topic of the feature group in its headers`) and counted in `onlinefs_topic_mismatch_total`, on the Topics row of the OnlineFS dashboard.

- **Producers that hold on to an old topic.**
  After a project's topic changes, or a feature group moves from the project topic to a topic of its own, the records that producers keep writing to the old topic are dropped until those producers restart.
  Producers that hold on to their topic include the inference logger of model deployments, streaming jobs and long-lived sessions.
- **Records that reach OnlineFS on another topic name.**
  A Kafka where records reach OnlineFS on a topic other than the one Hopsworks resolves for their feature group, such as a multi-region secondary that reads topics renamed or prefixed by mirroring, needs `onlinefs.configmapOverrides.onlinefssite.service.verifyFeatureGroupTopic: false`.
  With the check off, OnlineFS logs a warning at startup and attributes records by their headers, as before.
  Projects that share a topic need no change: their records arrive on the topic resolved for them.
- **A project can no longer use another project's online topic.**
  Creating a project, changing its topic, creating an online feature group or changing its topic, or creating a Kafka topic fails with `TOPIC_IN_USE_BY_ANOTHER_PROJECT` (190026) when the topic is the online topic of another project, the topic of another project's feature group, or a topic another project owns.
  The upgrade leaves a project or feature group already configured that way as it is, and updates that keep its topic still succeed.
  A project whose own topic is taken that way cannot create online feature groups until it gets a topic of its own, while the project that created the topic, or whose default `<project>_onlinefs` topic it is, keeps using it.
  With an external Kafka (`enable_bring_your_own_kafka`), where Hopsworks owns no topics and projects may share one, this is not enforced.
- **After the upgrade**, check that the topic mismatch panels stay at zero.
  A drop from a legitimate producer means one of the cases above: its insert never completes its online ingestion, and the project's `get_failures` does not list the dropped records.

### Schema migrations run on the DDL SQL node { #upgrade-ddl-sql-node }

The hopsworks and HopsFS Flyway migrations and the Hive `schematool` connect to the DDL SQL node (`mysqlddl`, `rondb.rondb.meta.ddlMySQLd`), as the Airflow migrations already do.
A migration no longer waits for application queries on the other SQL nodes that hold a related table, such as the statistics cleaner's query during migration V109.
On a table that an application query holds itself, each statement waits up to `ndb_schema_dist_lock_wait_timeout` (30 seconds) and then completes with warning 1296 (`Distribution of ALTER TABLE ... failed`).
The SQL node running that query keeps the old table definition: the query's transaction gets error 1412 (`Table definition has changed`) on its next statement on the table, and the first statement on the table after the transaction ends loads the new definition.
The migration pods wait for the rollout of the DDL SQL node before they start.
5.1.3 carries the same change, so it also applies to an upgrade to 5.1.3.

The DDL SQL node is on by default.
A cluster that disables it (`rondb.rondb.meta.ddlMySQLd.enabled: false`) points the migrations back at the application SQL nodes:

```yaml
hopsworks:
  dependencies:
    mysql:
      ddlConsulServiceName: mysql
hopsfs:
  dependencies:
    mysql:
      ddlConsulServiceName: mysql
hive:
  metastore:
    dependencies:
      mysql:
        ddlConsulServiceName: mysql
```

The Airflow `ddlConsulServiceName` cannot point at `mysql`, because its migrations need a single SQL node, so a cluster without the DDL SQL node runs with `global._hopsworks.airflow.enabled: false`.
