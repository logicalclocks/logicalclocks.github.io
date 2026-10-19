---
releases:
  "5.2.1":
    released: "2026-10-16"
    application: "5.2.1"
    python_client: "5.2.1"
  "5.2.0":
    released: "2026-10-15"
    application: "5.2.0"
    python_client: "5.2.1"
---

# Release notes { #hopsworks-5-2 }

The releases of Hopsworks 5.2, newest first.
To upgrade from 5.1 or between 5.2 releases, follow [Upgrading to Hopsworks 5.2][upgrading-to-5-2].

## 5.2.1 { #hopsworks-5-2-1 }

### What's changed

- Changed the OpenSearch index pass of the 5.1 to 5.2 upgrade to copy one index at a time behind a write block on that index alone, instead of refusing every OpenSearch client, reads included, for the whole pass; upgrade 5.1 clusters to 5.2.1 rather than 5.2.0 ([what keeps working][docs-os-what-works]).
- Fixed restricted project members reading every field of their project's embedding indices; they now read only the features of a grant or a share, and get HTTP 403 without one ([security configuration][docs-os-security]).
- Fixed OpenSearch restarts and the 5.1 to 5.2 index pass deleting the OpenSearch roles behind restricted grants and feature group shares, which left a shared project with HTTP 403, and every `helm upgrade` restarting OpenSearch.
- Fixed the 5.1 to 5.2 index pass failing with `field _id not found` on an index with an empty mapping, such as a `projects` index that was never written, and losing documents that were not yet refreshed when it copied an index.
- Fixed the OpenSearch index pass not refusing a 5.0 cluster, still on OpenSearch 1.x, which can't be upgraded straight to 5.2.

### Configuration changes

- Changed `olk.opensearch.indexUpgrade.enabled` to `olk.opensearch.indexUpgrade.mode`: `copy`, the default, or `report`, which lists the indices the 5.1 to 5.2 upgrade would copy and how long each stays blocked, and fails before anything changes, the Kafka migration included ([set the timeout][docs-os-timeout]).
  From 5.1.2 the 5.1 chart reads the same key to copy the indices before the 5.2 upgrade; pass it with `--set`, not in your values file ([copying on 5.1][docs-os-copy-51]).

### Breaking changes

- Remove `olk.opensearch.indexUpgrade.enabled` from your values, using `olk.opensearch.indexUpgrade.mode: report` in place of `false`, or the values schema rejects the upgrade.
- `helm upgrade` now stops before changing anything, also on a cluster already on 5.2.0, if an OpenSearch vector field would still be served by nmslib, which crashes OpenSearch 3.8 nodes on CPUs without AVX-512; apply the remedy the hook's log gives for each index or template it names ([nmslib fields][docs-os-nmslib]).
- Feature groups shared with a subset of their features can no longer be queried in Trino, only read online and in similarity search, because a data owner could point them at another project's files; share the whole feature group to query it in Trino ([upgrade guide][helm-upgrade-subset-shares]).
  `hopsworks.variables.trino_feature_group_subset_shares_enabled: "true"` turns Trino access to them back on, and with it that exposure.

## 5.2.0 { #hopsworks-5-2-0 }

5.2.0 also includes the changes of [5.1.1][hopsworks-5-1-1], which are listed under that release.

Upgrade 5.1 clusters, and 5.1.2 clusters in particular, to [5.2.1][hopsworks-5-2-1] instead of 5.2.0, as its breaking changes explain.

### What's changed

- Added the HopsFS CSI driver, on by default (`global._hopsworks.csi.enabled`), which mounts HopsFS into Jupyter, web terminal, Python and Ray job, Python app, Python deployment, Airflow and Trino pods without a privileged container; Trino needs it ([values][values-hopsfs-csi]).
- Added the KServe Standard deployment mode, the default for new model deployments, which runs a deployment as a Kubernetes Deployment instead of a Knative service; existing deployments keep Knative mode.
- Added KEDA 2.21 and its HTTP add-on, installed by default (`hopsworks.variables.kube_keda_installed`), to autoscale Standard-mode deployments on CPU, memory, requests or vLLM engine metrics and scale them to zero ([scaling][docs-autoscaling], [values][values-hw-keda]).
- Added scale to zero for idle Python apps when KEDA is installed, after `hopsworks.variables.pythonapp_idle_cooldown_seconds` (6 hours); with ingress-nginx, raise `nginx.ingress.kubernetes.io/proxy-read-timeout` in `hopsworks.ingress.annotations`, or the request that wakes an app fails after 60 seconds ([apps][docs-apps-idle]).
- Added Flask, Gradio and Node.js apps, which start from their app file like Streamlit apps ([app types][docs-apps-types]).
- Added database access for apps, on by default, which creates the project's online feature store database and gives the app its `MYSQL_*` connection variables; apps also get `TRINO_*` variables where the project has Trino ([database access][docs-apps-db]).
- Added npm installs of many packages in one build, from a list, a `package.json` with its lockfile or a Git repository ([npm packages][docs-npm]).
- Added versions of model deployments, so an earlier configuration can be activated again ([versions][docs-deployment-versions]).
- Added deployment schemas, which validate inference requests, and deployments of a model or a feature view without a predictor script ([deployment schema][docs-deployment-schema]).
- Added separate Python environments for the predictor and the transformer of a model deployment.
- Added real-time feature logging to an online feature group, for feature views that start logging on 5.2 ([feature logging][docs-feature-logging]).
- Added event-time windows to feature monitoring, the default for new configurations on feature groups and feature views with an event time; existing configurations are unchanged ([time basis][docs-fm-time-basis]).
- Added sharing of Trino catalogs and feature groups with other projects, down to schemas, tables and columns, and private Trino catalogs of one user ([sharing][docs-trino-sharing], [private catalogs][docs-trino-private]).
- Added Trino connector table functions, such as `system.query`, for Data Owners on their project's Trino catalogs.
- Added per-member credentials for Oracle data sources, so that each member reads with their own username, password and wallet, also through Trino catalogs and in jobs, Jupyter, terminals and apps ([provided credentials][docs-ds-provided]).
- Added `spine_df` to `FeatureView.get_batch_data` and the training data methods, to read features for rows you supply, within `hopsworks.variables.featurestore_asof_spine_max_rows` and the related size limits.
- Added the Factory, where users build ML systems and analytics tables in the web terminal, with their code in Git or in Hopsworks only; it needs `hopsworks.terminal.enabled` (`hopsworks.factory_enabled`, `hopsworks.factory_chat_enabled`) ([Factory][docs-factory]).
- Added a `hopsworks_analytics` project, off by default (`hopsworks.variables.hopsworks_analytics`), for cluster-wide Superset dashboards on the Hopsworks metadata, which exposes user email addresses to every Hopsworks administrator and to the model provider of the dashboard setup ([values][values-hopsworks-analytics]).
- Added proxy tokens for apps and Superset, off by default (`hopsworks.variables.hopsable_proxy_enabled`), so that a gateway outside the cluster can relay requests to them for API-key clients.
- Added the `TERMINAL` API key scope, so that the `hops` CLI can start, extend and attach to web terminal sessions and teleport Claude Code sessions to them; staged teleport files are deleted after `hopsworks.terminal.teleportTtlDays` (7), and the unused `KUBE` and `SINK` scopes are removed ([teleport][docs-teleport], [scopes][docs-api-scopes]).
- Added a memory guard to web terminals, on by default (`hopsworks.terminal.oomGuard`), which ends the process using the most memory instead of losing the session, and an out-of-memory notice when a session is lost anyway.
- Added Elasticsearch, ClickHouse and Teradata as data sources.
- Added an execution graph of the dbt models and tests to the executions of jobs on `dbt-pipeline` environments whose run writes one.
- Added time-to-live settings to the feature group create and edit forms, which ask before a change deletes online rows ([TTL][docs-ttl]).
- Added backups and restores of the Superset database, on by default with the cluster backups ([disaster recovery][docs-superset-backup]).
- Added support for Kubernetes 1.37; upgrade Hopsworks to 5.2 before the cluster, because 5.1 doesn't install on 1.37.
- Changed job, Jupyter, app and deployment logs to be read live from Kubernetes instead of being shipped to OpenSearch; Jupyter and app logs, and those of Python deployments with disk logging on (the default), are archived to the project's `Logs` dataset ([deployment logs][docs-serving-logs]).
- Changed the built-in Python environments to Python 3.13; custom environments keep the Python version they were built with.
- Changed LLM deployments to vLLM and vLLM-Omni v0.28.0; deployments created or edited on 5.1 keep v0.20.0 until you change their vLLM version, so keep the v0.20.0 images in a mirrored registry.
- Changed Trino to read its users, groups, user catalogs and access rules from HopsFS instead of Secrets, which fixes `helm upgrade` failing on clusters with many Trino catalogs or project members.
- Changed the Trino administrator, which the admin SQL console uses, to read only the `system`, `tpch` and `tpcds` catalogs.
- Changed reads of a feature view whose feature groups all come from one Snowflake data source to run the point-in-time joins in Snowflake.
- Changed datasets to be searchable by name, description and tags; tags now attach to a whole dataset, and existing tags on files inside a dataset can be read and deleted but no longer added.
- Changed adding a member to a project to create the member's home directory in the background.
- Changed removing a member from a project to hand their home directory to a Data Owner, chosen in the remove dialog, instead of leaving it unreadable ([removed members][docs-member-files]).
- Changed project creation to give every project Trino and Superset where the cluster runs them, also through the REST API, where a request without a service list created a project with Kafka only.
- Changed project creation to refuse a pre-created namespace longer than 25 characters, like a project name.
- Changed the feature store sharing card in the project settings to manage shares with projects and grants to restricted users, of the whole feature store or of single feature groups ([sharing][docs-fs-sharing]).
- Changed the Set up data source dialog to list each SQL engine and CRM vendor as its own choice, with a filter box, and the Snowflake form to accept a programmatic access token in its password field.
- Changed the Jupyter overview to show the server's log archives and its configuration, which is saved when you start Jupyter.
- Changed Hugging Face model imports to download a single commit, which can be given as a revision and is recorded in the model's description.
- Changed the coding agent instruction files in members' home directories, such as `AGENTS.md`, to be updated on upgrade unless the member edited them.
- Fixed filtered similarity search failing on embedding indices created before 5.1, which the upgrade rebuilds on faiss ([upgrading OpenSearch][docs-os-faiss]).
- Fixed Helm 4 server-side apply conflicts on `helm upgrade` over the replicas of HPA-managed workloads other than the RonDB REST server, the rules of the Knative serving webhooks and the `rss-configuration` ConfigMap ([Helm 4 notes][helm4-migration]).
- Fixed model deployments answering 403 to users on a password an administrator set, and still admitting users deactivated or removed from the project; accounts and memberships from before the upgrade are corrected at their next change.
- Fixed, on clusters with more than one RonDB MySQL server, library installs building on an older image of the environment and losing earlier installs, `insert(wait_for_online_ingestion=True)` returning before the rows were online, and apps reporting the execution they replaced.
- Fixed tags and keywords added right after an artifact was created missing from search.
- Fixed deleted feature views, feature groups and projects coming back as empty entries, which blocked creating new ones with the same name.
- Fixed ingestion statistics runs piling up on frequently written feature groups and leaving other jobs pending; at most one runs per feature group.
- Fixed Python engine reads failing for queries with a filter on a joined feature group or a filter that compares features of two feature groups.
- Fixed writes to Iceberg feature groups from Python jobs and apps failing with `Unable to load libhdfs`.
- Fixed the table preview of a PostgreSQL data source failing for a role granted only some columns.
- Fixed a Jupyter server that had just started failing requests on clusters with more than one Hopsworks instance.
- Fixed project creation sometimes failing and rolling back on a group that "already exists".
- Fixed Spark Connect in web terminals never starting on clusters that enforce the Kyverno restricted policies.
- Fixed agent deployments that mount HopsFS never starting on OpenShift.
- Fixed the dialogs of Git repository actions in the project settings closing on their own, and transformation function previews showing the imports of the defining module.
- Fixed the Hopsworks admin pod starting before the database migrations had finished.
- Fixed the Hive Metastore `metastore-db-init` Job failing on a fresh install when it started before the HopsFS NameNode.
- Fixed security vulnerabilities in the HopsFS, Hive Metastore, Trino, Spark history server and Ray images, and in the Hopsworks server dependencies.
- Changed the SQL Runner of the Query Engine page to fill the page, show row numbers and column types, list a table's columns and draw `EXPLAIN (FORMAT GRAPHVIZ)` plans as a graph, and fixed it leaving queries running and completing no column names after `FROM` (also in [5.1.2][hopsworks-5-1-2]).
- Fixed queued service operations failing on every retry when they removed a user from Superset or set up Superset for a project Observer, and security vulnerabilities in the Payara, Hopsworks certificate authority, Grafana, Filebeat and Superset images and the MySQL and Redis of Superset (also in [5.1.2][hopsworks-5-1-2]).

### Configuration changes

- Added `kserve.kserve.storage.resources` for the storage initializer that downloads models into deployment pods.
- Added `kafka.cluster.kafka.config.replicationFactor` and `minInsyncReplicas` for multi-broker Kafka; `minInsyncReplicas` above a topic's replicas makes `acks=all` writes to it fail ([values][values-kafka]).
- Changed the default driver memory of new Ray jobs (`hopsworks.variables.ray_job_driver_memory`) from 2048 to 4096 MB.
- Changed `hopsworks.variables.trino_default_catalog` from `hive` to `delta`, the catalog new Superset connections to Trino open in.
- Changed `values.openshift.yaml` to turn on credential files for Trino catalogs (`global._hopsworks.trino.mountableSecrets.enabled`).
- Fixed Helm 4 rejecting an empty `kafka.cluster.kafka.authorizer.authorizerClass`.
- Fixed `global._hopsworks.jobs.ttlSecondsAfterFinished: 0` being replaced by `86400`.
- Changed `hopsworks.variables.trino_events_cleaner_batch_size` from 1000 to 100 (also in [5.1.2][hopsworks-5-1-2]).

### Breaking changes

- Upgrade to 5.2 only from 5.1, satellites before central, with central and its satellites all under Helm or all under ArgoCD ([upgrade guide][helm-upgrade-guide]).
- Upgrade 5.1 clusters to [5.2.1][hopsworks-5-2-1] instead of 5.2.0, whose OpenSearch index pass refuses every client and whose OpenSearch restarts delete the roles behind restricted-access grants and feature group shares; on [5.1.2][hopsworks-5-1-2], which fixed those restarts, 5.2.0 is a regression.
- The upgrade migrates Kafka from ZooKeeper to KRaft, which can't be undone: give `helm upgrade` a long enough `--timeout`, never pass `--atomic` (`--rollback-on-failure` in Helm 4) or run `helm rollback`, and under ArgoCD sync twice ([Kafka 4 and KRaft][docs-kafka4-expect]).
- Kafka 4.3 rejects clients older than Apache Kafka 2.1 or librdkafka 1.8.2; upgrade them first ([client compatibility][docs-kafka4-clients]).
- On a cluster installed before 5.1, OpenSearch refuses every client while the upgrade copies its oldest indices; plan the outage and the timeout ([upgrade guide][helm-upgrade-opensearch]).
- OpenSearch now reports its own version, `3.8.0`, instead of `7.10.2`; check clients that connect to it directly against the [OpenSearch 3.0 breaking changes](https://docs.opensearch.org/latest/breaking-changes/).
- OpenSearch snapshot repositories on MinIO before `RELEASE.2025-01-20T14-49-07Z` and on other S3-compatible stores that require `Content-MD5` need `legacy_md5_checksum_calculation: true`, or the upgrade fails ([upgrade guide][helm-upgrade-opensearch]).
- KEDA, installed by default, can't share a Kubernetes cluster with another KEDA or the OpenShift Custom Metrics Autoscaler, including the KEDA of another Hopsworks release such as a satellite; set `hopsworks.variables.kube_keda_installed: false` on all but one ([upgrade guide][helm-upgrade-keda]).
- The chart now creates a cluster-wide IngressClass named `istio`; if the cluster already has one, set `kserve.istio.ingressClass.enabled: false`, or the upgrade fails.
- Removed the KServe local model controller; if you set `kserve.kserve.localmodel.enabled: true`, remove it, or the chart fails to render.
- Project namespaces now get a NetworkPolicy that admits traffic only from the same namespace and the Hopsworks namespace; add any other namespace that reaches project pods, such as Istio or monitoring, to `hopsworks.variables.project_namespace_network_policy_allowed_namespaces` ([values][values-netpol]).
  Turning them off with `hopsworks.variables.project_namespace_network_policy_enabled: false` leaves the existing ones; delete them with `kubectl delete networkpolicy -A --field-selector metadata.name=hopsworks-project-isolation`.
- With `hopsworks.rbac.useExistingRole: true`, add the chart's new [ClusterRole grants][helm-role] on `scaledobjects`, `interceptorroutes`, `ingresses`, `networkpolicies` and `csidrivers`, or model deployments and project creation fail.
- On OpenShift, use the `values.openshift.yaml` of the 5.2 chart, which creates an SCC for the privileged HopsFS CSI node plugin; if a cluster administrator owns SCCs, see the [hopsfs-csi README][helm-csi-scc].
- Overrides of the Trino `initContainers`, `additionalVolumes` or `additionalVolumeMounts`, including those [5.1.0][hopsworks-5-1-0] asked for with `hopsworks.hopsfsMount.enabled: false`, fail the render; remove the overrides, or copy the new entries from the chart into them.
- If you override `trino.trino.image.tag`, use a Hopsworks Trino image of `483-v2` or later and set `global._hopsworks.trino.image.tag` to the same tag.
- If you set `trino.trino.serviceAccount.name`, set `trino.trinotest.serviceAccount.name` to the same name.
- With cluster backups on, Superset backups need an object store and, with `superset.auth.createSecrets: false`, the `backup.hops.works/include=true` label on its Secrets, or the chart fails to render; set `superset.backups.enabled: false` to skip them ([disaster recovery][docs-superset-backup]).
- If your release namespace is longer than 34 characters, set `global._hopsworks.csi.driverName`, because the default driver name would exceed 63 characters.
- With Helm 4, pass `--skip-crds` to a `helm install` on a cluster that already has the Strimzi CRDs, and after a reinstall run `helm upgrade` once to recreate the KEDA CRDs ([upgrade guide][helm-upgrade-strimzi]).
- MongoDB data sources need MongoDB 4.2 or later; upgrade older MongoDB servers, or browsing and testing their data sources fails.
- Web terminal sessions now last 8 hours, and every upgrade sets `terminal_session_hours` from `hopsworks.terminal.sessionHours`, replacing a value set in the admin UI ([upgrade guide][helm-upgrade-terminal]).
- Trino no longer records the admin query history, and its records lose their query text after `hopsworks.variables.trino_events_strip_details_after_days` (7); to keep either, or if your values restate `trino.trino.additionalConfigProperties`, see the [upgrade guide][helm-upgrade-trino] (also in [5.1.2][hopsworks-5-1-2]).

### Deprecations

- Deprecated `global._hopsworks.trino.mountableSecrets.mechanism`, `global._hopsworks.trino.userCatalogShards`, `trino.auth.adminUserPwdHash`, `trino.auth.monitoringUserPwdHash` and `hw-kyverno.policyExceptions.trino`, which nothing reads any more.
- Deprecated `hopsworks.variables.mount_hopsfs_in_python_job`, which only legacy Python jobs still read.
- Deprecated the name of `kafka.cluster.zookeeper`, which now sizes and places the KRaft controllers; its `services.client.annotations` is no longer read.
- Deprecated the `environmentDTO` field of model deployments in the REST API; use `predictorEnvironment` and `transformerEnvironment`.

### Upgraded components

| Component | 5.1.0 | 5.2.0 |
| --------- | ----- | ----- |
| Airflow image | 5.1.0 | 5.2.0 |
| ArrowFlight server | 5.1.0 | 5.2.0 |
| Base environment images | 5.1.0 | 5.2.1 |
| Filebeat | 8.19.21 | 8.19.23 (also in [5.1.2][hopsworks-5-1-2]) |
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
| Payara | 6.2025.11-jdk21.0 | 6.2025.11-jdk21.1 (also in [5.1.2][hopsworks-5-1-2]) |
| Python in the base environments | 3.12 | 3.13 |
| Ray | 2.55.1 | 2.58.0 |
| RonDB | 26.02.10 | 26.02.11 (also in [5.1.1][hopsworks-5-1-1]) |
| scikit-learn model server | 0.19.1 | 0.21.0 |
| Spark history server | 4.1.3.0 | 4.1.3.1 |
| Storage initializer | 5.1.0 | 5.2.0 |
| Strimzi | 0.45.2-h1 | 1.2.0 |
| Superset | 6.0.0p4.4 | 6.0.0p4.5 (also in [5.1.2][hopsworks-5-1-2]) |
| Superset MySQL | 8.4.11-ubuntu24.04-h4 | 8.4.11-ubuntu24.04-h5 (also in [5.1.2][hopsworks-5-1-2]) |
| Superset Redis | 7.4.11-alpine-h1 | 7.4.11-alpine-h2 (also in [5.1.2][hopsworks-5-1-2]) |
| Toolbox image (hwutils) | 1.9 | 1.10 |
| Trino | 480-v10 | 483-v2 |
| Trino mountable-secrets sidecar | 3.4.3.3-EE-RC0-1 | 3.4.3.3-EE-RC1-1 |
| vLLM | v0.20.0 | v0.28.0 |
| vLLM-Omni | v0.20.0 | v0.28.0 |

[docs-os-what-works]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade_opensearch/#opensearch-what-keeps-working
[docs-os-timeout]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade_opensearch/#opensearch-set-the-timeout
[docs-os-copy-51]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade_opensearch/#opensearch-copy-on-51
[docs-os-nmslib]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade_opensearch/#opensearch-nmslib-fields
[docs-os-security]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade_opensearch/#security-configuration
[helm-upgrade-subset-shares]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.1/UPGRADE.md#feature-groups-shared-with-a-subset-of-their-features
[docs-autoscaling]: https://docs.hopsworks.ai/5.2/user_guides/mlops/serving/autoscaling/
[docs-apps-idle]: https://docs.hopsworks.ai/5.2/user_guides/projects/apps/#scale-to-zero-when-idle
[docs-apps-types]: https://docs.hopsworks.ai/5.2/user_guides/projects/apps/#app-types
[docs-apps-db]: https://docs.hopsworks.ai/5.2/user_guides/projects/apps/#database-and-feature-store-access
[docs-npm]: https://docs.hopsworks.ai/5.2/user_guides/projects/python/python_install/#npm-packages
[docs-deployment-versions]: https://docs.hopsworks.ai/5.2/user_guides/mlops/serving/deployment-versions/
[docs-deployment-schema]: https://docs.hopsworks.ai/5.2/user_guides/mlops/serving/deployment-schema/
[docs-fm-time-basis]: https://docs.hopsworks.ai/5.2/user_guides/fs/feature_monitoring/scheduled_statistics/#time-basis
[docs-ds-provided]: https://docs.hopsworks.ai/5.2/user_guides/fs/data_source/creation/sql/#data-source-provided-credentials
[docs-factory]: https://docs.hopsworks.ai/5.2/user_guides/client_installation/#build-an-ml-system
[docs-api-scopes]: https://docs.hopsworks.ai/5.2/user_guides/projects/api_key/api_key_scopes/
[docs-ttl]: https://docs.hopsworks.ai/5.2/user_guides/fs/feature_group/ttl/
[docs-member-files]: https://docs.hopsworks.ai/5.2/user_guides/projects/project/manage_members/#what-happens-to-a-removed-members-files
[docs-fs-sharing]: https://docs.hopsworks.ai/5.2/user_guides/fs/sharing/sharing/
[docs-serving-logs]: https://docs.hopsworks.ai/5.2/user_guides/mlops/serving/troubleshooting/#configuring-disk-logging
[docs-feature-logging]: https://docs.hopsworks.ai/5.2/user_guides/fs/feature_view/deployment/#feature-logging
[docs-trino-sharing]: https://docs.hopsworks.ai/5.2/user_guides/projects/trino/sharing/
[docs-trino-private]: https://docs.hopsworks.ai/5.2/user_guides/projects/trino/catalogs/#private-catalogs
[docs-superset-backup]: https://docs.hopsworks.ai/5.2/setup_installation/admin/ha-dr/dr/#superset-backup
[docs-teleport]: https://docs.hopsworks.ai/5.2/user_guides/projects/terminal/teleport/
[docs-kafka4-expect]: https://docs.hopsworks.ai/5.2/setup_installation/admin/kafka4/#what-to-expect
[docs-kafka4-clients]: https://docs.hopsworks.ai/5.2/setup_installation/admin/kafka4/#kafka4-client-compatibility
[docs-os-faiss]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade_opensearch/#embedding-indices-move-to-faiss
[values-hopsfs-csi]: https://docs.hopsworks.ai/5.2/setup_installation/common/helm_chart_values/hopsfs-csi/
[values-hw-keda]: https://docs.hopsworks.ai/5.2/setup_installation/common/helm_chart_values/hw-keda/
[values-kafka]: https://docs.hopsworks.ai/5.2/setup_installation/common/helm_chart_values/kafka/#helm.kafka.cluster.kafka.config.minInsyncReplicas
[values-hopsworks-analytics]: https://docs.hopsworks.ai/5.2/setup_installation/common/helm_chart_values/hopsworks/#helm.hopsworks.variables.hopsworks_analytics
[values-netpol]: https://docs.hopsworks.ai/5.2/setup_installation/common/helm_chart_values/hopsworks/#helm.hopsworks.variables.project_namespace_network_policy_enabled
[helm-upgrade-guide]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/UPGRADE.md#51x-to-52x
[helm-upgrade-opensearch]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/UPGRADE.md#opensearch-380
[helm-upgrade-strimzi]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/UPGRADE.md#strimzi-crds
[helm-upgrade-keda]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/UPGRADE.md#keda-autoscaling-of-standard-mode-deployments
[helm-upgrade-trino]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/UPGRADE.md#trino-query-history
[helm-upgrade-terminal]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/UPGRADE.md#terminal-session-length
[helm4-migration]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/HELM4_MIGRATION.md
[helm-role]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/charts/hopsworks/templates/role.yaml
[helm-csi-scc]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/charts/hopsfs-csi/README.md#when-the-cluster-administrators-own-the-scc
