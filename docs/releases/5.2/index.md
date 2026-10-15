---
releases:
  "5.2.0":
    released: "2026-10-15"
    application: "5.2.0"
    python_client: "5.2.1"
---

# Hopsworks 5.2 { #hopsworks-5-2 }

The releases of Hopsworks 5.2, newest first.
To upgrade from 5.1 or between 5.2 releases, follow [Upgrading to Hopsworks 5.2][upgrading-to-5-2].

## 5.2.0 { #hopsworks-5-2-0 }

5.2.0 also includes the changes of [5.1.1][hopsworks-5-1-1], which are listed under that release.

### Breaking changes

- Upgrade to 5.2 only from 5.1, satellites before central, with central and its satellites all under Helm or all under ArgoCD ([upgrading to 5.2][upgrading-to-5-2-0]).
- The upgrade migrates Kafka from ZooKeeper to KRaft, which can't be undone: give `helm upgrade` a long enough `--timeout`, never pass `--atomic` (`--rollback-on-failure` in Helm 4) or run `helm rollback`, and under ArgoCD sync twice ([Kafka 4 and KRaft][docs-kafka4-expect]).
- Kafka 4.3 rejects clients older than Apache Kafka 2.1 or librdkafka 1.8.2; upgrade them first ([client compatibility][docs-kafka4-clients]).
- On a cluster installed before 5.1, OpenSearch refuses every client while the upgrade copies its oldest indices; plan the outage and the timeout ([upgrading OpenSearch][docs-os-index-pass]).
- OpenSearch now reports its own version, `3.8.0`, instead of `7.10.2`; check clients that connect to it directly against the [OpenSearch 3.0 breaking changes](https://docs.opensearch.org/latest/breaking-changes/).
- OpenSearch snapshot repositories on MinIO before `RELEASE.2025-01-20T14-49-07Z` and on other S3-compatible stores that require `Content-MD5` need `legacy_md5_checksum_calculation: true`, or the upgrade fails ([chart upgrade guide][helm-upgrade-opensearch]).
- KEDA, installed by default, can't share a Kubernetes cluster with another KEDA or the OpenShift Custom Metrics Autoscaler, including the KEDA of another Hopsworks release such as a satellite; set `hopsworks.variables.kube_keda_installed: false` on all but one ([chart upgrade guide][helm-upgrade-keda]).
- The chart now creates a cluster-wide IngressClass named `istio`; if the cluster already has one, set `kserve.istio.ingressClass.enabled: false`, or the upgrade fails.
- Removed the KServe local model controller; set `kserve.kserve.localmodel.enabled: false`, or the chart fails to render.
- Project namespaces now get a NetworkPolicy that admits traffic only from the same namespace and the Hopsworks namespace; add any other namespace that reaches project pods, such as Istio or monitoring, to `hopsworks.variables.project_namespace_network_policy_allowed_namespaces` ([values][values-netpol]).
- With `hopsworks.rbac.useExistingRole: true`, add the chart's new [ClusterRole grants][helm-role] on `scaledobjects`, `interceptorroutes`, `ingresses`, `networkpolicies` and `csidrivers`, or model deployments and project creation fail.
- On OpenShift, use the `values.openshift.yaml` of the 5.2 chart, which creates an SCC for the privileged HopsFS CSI node plugin; if a cluster administrator owns SCCs, see the [hopsfs-csi README][helm-csi-scc].
- Overrides of the Trino `initContainers`, `additionalVolumes` or `additionalVolumeMounts`, including those [5.1.0][hopsworks-5-1-0] asked for with `hopsworks.hopsfsMount.enabled: false`, fail the render; copy the new entries from the chart, or remove the overrides with `global._hopsworks.trino.mountableSecrets.enabled: false`.
- If you override `trino.trino.image.tag`, use a Hopsworks Trino image of `483-v2` or later and set `global._hopsworks.trino.image.tag` to the same tag.
- If you set `trino.trino.serviceAccount.name`, set `trino.trinotest.serviceAccount.name` to the same name.
- Trino no longer records the admin query history; to keep it, or if your values restate `trino.trino.additionalConfigProperties`, see the [chart upgrade guide][helm-upgrade-trino].
- Recorded Trino queries lose their query text after `hopsworks.variables.trino_events_strip_details_after_days` (7), and the first nightly cleanup after the upgrade strips the older ones; set it to `61` to keep them.
- With cluster backups on, Superset backups need an object store and, with `superset.auth.createSecrets: false`, the `backup.hops.works/include=true` label on its Secrets, or the chart fails to render; set `superset.backups.enabled: false` to skip them ([disaster recovery][docs-superset-backup]).
- If your release namespace is longer than 34 characters, set `global._hopsworks.csi.driverName`, because the default driver name would exceed 63 characters.
- With Helm 4, pass `--skip-crds` to a `helm install` on a cluster that already has the Strimzi CRDs, and after a reinstall run `helm upgrade` once to recreate the KEDA CRDs ([chart upgrade guide][helm-upgrade-strimzi]).
- Web terminal sessions now last 8 hours, and every upgrade sets `terminal_session_hours` from `hopsworks.terminal.sessionHours`, replacing a value set in the admin UI ([chart upgrade guide][helm-upgrade-terminal]).

### Release notes

- Added the HopsFS CSI driver, on by default (`global._hopsworks.csi.enabled`), which mounts HopsFS into Jupyter, web terminal, Python and Ray job, Python app, Python deployment, Airflow and Trino pods without a privileged container; Trino needs it ([values][values-hopsfs-csi]).
- Added the KServe Standard deployment mode, the default for new model deployments, which runs a deployment as a Kubernetes Deployment instead of a Knative service; existing deployments keep Knative mode.
- Added KEDA 2.21 and its HTTP add-on, installed by default (`hopsworks.variables.kube_keda_installed`), to autoscale Standard-mode deployments on CPU, memory, requests or vLLM engine metrics and scale them to zero ([scaling][docs-autoscaling], [values][values-hw-keda]).
- Added scale to zero for idle Python apps when KEDA is installed, after `hopsworks.variables.pythonapp_idle_cooldown_seconds` (6 hours); with ingress-nginx, raise `nginx.ingress.kubernetes.io/proxy-read-timeout` in `hopsworks.ingress.annotations`, or the request that wakes an app fails after 60 seconds.
- Added versions of model deployments, so an earlier configuration can be activated again.
- Added real-time feature logging to an online feature group, for feature views that start logging on 5.2 ([feature logging][docs-feature-logging]).
- Added `kserve.kserve.storage.resources` for the storage initializer that downloads models into deployment pods.
- Added sharing of Trino catalogs and feature groups with other projects, down to schemas, tables and columns ([sharing][docs-trino-sharing]).
- Added private Trino catalogs, which belong to one user in every project they are a member of ([private catalogs][docs-trino-private]).
- Added Trino connector table functions, such as `system.query`, for Data Owners on their project's Trino catalogs.
- Added `spine_df` to `FeatureView.get_batch_data` and the training data methods, to read features for rows you supply.
- Added the Factory, where users build ML systems and analytics tables in the web terminal (`hopsworks.factory_enabled`, `hopsworks.factory_chat_enabled`).
- Added `hopsworks.variables.hopsworks_analytics` (default `false`) for cluster-wide Superset dashboards on the Hopsworks metadata, which holds user email addresses that the setup wizard's coding agent can send to its model provider ([values][values-hopsworks-analytics]).
- Added `hopsworks.variables.hopsable_proxy_enabled` (default `false`), so that a gateway outside the cluster can relay requests to apps and Superset.
- Added Elasticsearch, ClickHouse and Teradata as data sources.
- Added backups and restores of the Superset database, on by default with the cluster backups ([disaster recovery][docs-superset-backup]).
- Added `kafka.cluster.kafka.config.replicationFactor` and `minInsyncReplicas` for multi-broker Kafka; `minInsyncReplicas` above a topic's replicas makes `acks=all` writes to it fail ([values][values-kafka]).
- Added `hopsworks.terminal.oomGuard`, which keeps a web terminal session alive when a process runs out of memory.
- Added `hopsworks.terminal.teleportTtlDays`, which deletes old teleported coding-agent sessions ([teleport][docs-teleport]).
- Added support for Kubernetes 1.37; upgrade Hopsworks to 5.2 before the cluster, because 5.1 doesn't install on 1.37.
- Changed job, Jupyter, app and deployment logs to be read live from Kubernetes instead of being shipped to OpenSearch; Jupyter, app and deployment logs are archived to the project's `Logs` dataset when they stop.
- Changed the built-in Python environments to Python 3.13; custom environments keep the Python version they were built with.
- Changed LLM deployments to vLLM and vLLM-Omni v0.28.0; deployments created or edited on 5.1 keep v0.20.0 until you change their vLLM version, so keep the v0.20.0 images in a mirrored registry.
- Changed the default driver memory of new Ray jobs (`hopsworks.variables.ray_job_driver_memory`) from 2048 to 4096 MB.
- Changed Trino to read its users, groups, user catalogs and access rules from HopsFS instead of Secrets, which fixes `helm upgrade` failing on clusters with many Trino catalogs or project members.
- Changed `hopsworks.variables.trino_default_catalog` from `hive` to `delta`, the catalog new Superset connections to Trino open in.
- Changed the Trino administrator, which the admin SQL console uses, to read only the `system`, `tpch` and `tpcds` catalogs.
- Changed `values.openshift.yaml` to turn on credential files for Trino catalogs (`global._hopsworks.trino.mountableSecrets.enabled`).
- Changed adding a member to a project to create the member's home directory in the background.
- Deprecated `global._hopsworks.trino.mountableSecrets.mechanism`, `global._hopsworks.trino.userCatalogShards`, `trino.auth.adminUserPwdHash`, `trino.auth.monitoringUserPwdHash` and `hw-kyverno.policyExceptions.trino`, which no longer do anything.
- Deprecated `hopsworks.variables.mount_hopsfs_in_python_job`, which now applies only to Python jobs, because Python apps always mount HopsFS.
- Fixed filtered similarity search failing on embedding indices created before 5.1, which the upgrade rebuilds on faiss ([upgrading OpenSearch][docs-os-faiss]).
- Fixed Helm 4 server-side apply conflicts on `helm upgrade` over HPA-managed replicas, except the RonDB REST server's, the Knative serving webhooks and the `rss-configuration` ConfigMap ([Helm 4 notes][helm4-migration]).
- Fixed Helm 4 rejecting an empty `kafka.cluster.kafka.authorizer.authorizerClass`.
- Fixed model deployment pods being rejected during a rollout of the model serving webhook.
- Fixed the Hopsworks admin pod starting before the database migrations had finished.
- Fixed the Hive Metastore `metastore-db-init` Job failing on a fresh install when it started before the HopsFS NameNode.
- Fixed `global._hopsworks.jobs.ttlSecondsAfterFinished: 0` being replaced by `86400`.
- Fixed security vulnerabilities in the HopsFS, Hive Metastore, Trino, Spark history server, Ray, Payara, Filebeat and Superset images.

[docs-autoscaling]: https://docs.hopsworks.ai/5.2/user_guides/mlops/serving/autoscaling/
[docs-feature-logging]: https://docs.hopsworks.ai/5.2/user_guides/fs/feature_view/deployment/#feature-logging
[docs-kafka4-clients]: https://docs.hopsworks.ai/5.2/setup_installation/admin/kafka4/#kafka4-client-compatibility
[docs-kafka4-expect]: https://docs.hopsworks.ai/5.2/setup_installation/admin/kafka4/#what-to-expect
[docs-os-faiss]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade_opensearch/#embedding-indices-move-to-faiss
[docs-os-index-pass]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade_opensearch/#the-index-pass-on-51x-to-52x
[docs-superset-backup]: https://docs.hopsworks.ai/5.2/setup_installation/admin/ha-dr/dr/#superset-backup
[docs-teleport]: https://docs.hopsworks.ai/5.2/user_guides/projects/terminal/teleport/
[docs-trino-private]: https://docs.hopsworks.ai/5.2/user_guides/projects/trino/catalogs/#private-catalogs
[docs-trino-sharing]: https://docs.hopsworks.ai/5.2/user_guides/projects/trino/sharing/
[helm-csi-scc]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/charts/hopsfs-csi/README.md#when-the-cluster-administrators-own-the-scc
[helm-role]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/charts/hopsworks/templates/role.yaml
[helm-upgrade-keda]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/UPGRADE.md#keda-autoscaling-of-standard-mode-deployments
[helm-upgrade-opensearch]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/UPGRADE.md#opensearch-380
[helm-upgrade-strimzi]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/UPGRADE.md#strimzi-crds
[helm-upgrade-terminal]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/UPGRADE.md#terminal-session-length
[helm-upgrade-trino]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/UPGRADE.md#trino-query-history
[helm4-migration]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/HELM4_MIGRATION.md
[values-hopsfs-csi]: https://docs.hopsworks.ai/5.2/setup_installation/common/helm_chart_values/hopsfs-csi/
[values-hopsworks-analytics]: https://docs.hopsworks.ai/5.2/setup_installation/common/helm_chart_values/hopsworks/#helm.hopsworks.variables.hopsworks_analytics
[values-hw-keda]: https://docs.hopsworks.ai/5.2/setup_installation/common/helm_chart_values/hw-keda/
[values-kafka]: https://docs.hopsworks.ai/5.2/setup_installation/common/helm_chart_values/kafka/#helm.kafka.cluster.kafka.config.minInsyncReplicas
[values-netpol]: https://docs.hopsworks.ai/5.2/setup_installation/common/helm_chart_values/hopsworks/#helm.hopsworks.variables.project_namespace_network_policy_enabled

### Upgraded components

| Component | 5.1.0 | 5.2.0 |
| --------- | ----- | ----- |
| Airflow image | 5.1.0 | 5.2.0 |
| ArrowFlight server | 5.1.0 | 5.2.0 |
| Base environment images | 5.1.0 | 5.2.1 |
| Filebeat | 8.19.21 | 8.19.23 |
| Git image | 1.5 | 1.6 |
| Grafana | 12.4.9-h9 | 12.4.9-h12 |
| Hive Metastore | 4.1.0.0-v1 | 4.1.0.1-v1 |
| HopsFS | 3.4.3.3-EE-RC0 | 3.4.3.3-EE-RC1 |
| Inference logger | 5.1.0 | 5.2.0 |
| Kafka | 3.9.2 | 4.3.1 |
| KServe | v0.19.0 | v0.21.0 |
| KServe utilities | 0.1.10 | 0.1.11 |
| Model serving authenticator | 5.1.0 | 5.2.0 |
| Model serving webhook | 5.1.0 | 5.2.0 |
| OnlineFS | 2.4 | 2.5 |
| OpenSearch | 2.19.6.3 | 3.8.0.0 |
| OpenSearch Dashboards | 2.19.6.7 | 3.8.0.0 |
| Payara | 6.2025.11-jdk21.0 | 6.2025.11-jdk21.1 |
| Python in the base environments | 3.12 | 3.13 |
| Ray | 2.55.1 | 2.58.0 |
| RonDB | 26.02.10 | 26.02.11 (also in [5.1.1][hopsworks-5-1-1]) |
| scikit-learn model server | 0.19.1 | 0.21.0 |
| Spark history server | 4.1.3.0 | 4.1.3.1 |
| Storage initializer | 5.1.0 | 5.2.0 |
| Strimzi | 0.45.2-h1 | 1.2.0 |
| Superset | 6.0.0p4.4 | 6.0.0p4.5 |
| Superset MySQL | 8.4.11-ubuntu24.04-h4 | 8.4.11-ubuntu24.04-h5 |
| Superset Redis | 7.4.11-alpine-h1 | 7.4.11-alpine-h2 |
| Toolbox image (hwutils) | 1.9 | 1.10 |
| Trino | 480-v10 | 483-v2 |
| Trino mountable-secrets sidecar | 3.4.3.3-EE-RC0-1 | 3.4.3.3-EE-RC1-1 |
| vLLM | v0.20.0 | v0.28.0 |
| vLLM-Omni | v0.20.0 | v0.28.0 |
