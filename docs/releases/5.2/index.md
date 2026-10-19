---
releases:
  "5.2.1":
    released: "2026-10-16"
    python_client: "5.2.1"
  "5.2.0":
    released: "2026-10-15"
    python_client: "5.2.1"
---

# Release notes { #hopsworks-5-2 }

The releases of Hopsworks 5.2, newest first.

## 5.2.1 { #hopsworks-5-2-1 }

### What's changed

- Fixed the 5.1 to 5.2 index pass failing with `field _id not found` on an index with an empty mapping, such as a `projects` index that was never written, and losing documents that were not yet refreshed when it copied an index.
- Addressed vulnerabilities in OpenSearch.
  It applies once an OpenSearch pod logs `Security configuration applied` after the upgrade; if none does, run `run_security_admin.sh` as the chart's `UPGRADE.md` shows.
- Changed the OpenSearch index pass of the 5.1 to 5.2 upgrade to copy one index at a time behind a write block on that index alone, instead of refusing every OpenSearch client, reads included, for the whole pass; upgrade 5.1 clusters to 5.2.1 rather than 5.2.0 ([what keeps working][docs-os-what-works]).
- Fixed OpenSearch restarts and the 5.1 to 5.2 index pass deleting the OpenSearch roles behind restricted grants and feature group shares, which left a shared project with HTTP 403.
  Grants and shares made before the last OpenSearch restart on 5.2.0 lost their roles, and granting or sharing again is refused: revoke and grant again, or unshare and share again.
- Changed the OpenSearch index pass to run before the Kafka migration, so its report (`olk.opensearch.indexUpgrade.mode: report`) and its refusals stop an upgrade from 5.1 before anything changes ([set the timeout][docs-os-timeout]).
- Fixed the OpenSearch index pass not refusing a 5.0 cluster, still on OpenSearch 1.x, which can't be upgraded straight to 5.2.
- Fixed every `helm upgrade` restarting OpenSearch.

### Breaking changes

- Remove `olk.opensearch.indexUpgrade.enabled` from your values, using `olk.opensearch.indexUpgrade.mode: report` in place of `false`, or the values schema rejects the upgrade.
- `helm upgrade` now stops before changing anything, also on a cluster already on 5.2.0, if an OpenSearch vector field would still be served by nmslib, which crashes OpenSearch 3.8 nodes on CPUs without AVX-512, where 5.2.0 upgraded without checking; apply the remedy the hook's log gives for each index or template it names ([nmslib fields][docs-os-nmslib]).
- Feature groups shared with a subset of their features can no longer be queried in Trino, only read online and in similarity search, to address a vulnerability; share the whole feature group to query it in Trino.
  `hopsworks.variables.trino_feature_group_subset_shares_enabled: "true"` turns Trino access to them back on, which undoes that.

### Configuration changes

- Changed `olk.opensearch.indexUpgrade.enabled` to `olk.opensearch.indexUpgrade.mode`: `copy`, the default, or `report`, which lists the indices the 5.1 to 5.2 upgrade would copy and how long each stays blocked, and fails before anything changes, the Kafka migration included ([set the timeout][docs-os-timeout]).
  From 5.1.2 the 5.1 chart reads the same key to copy the indices before the 5.2 upgrade; pass it with `--set`, not in your values file ([copying on 5.1][docs-os-copy-51]).
- Added `hopsworks.variables.trino_feature_group_subset_shares_enabled` (default `"false"`), which lets Trino serve feature groups shared with a subset of their features.

## 5.2.0 { #hopsworks-5-2-0 }

Upgrade 5.1 clusters, and 5.1.2 clusters in particular, to [5.2.1][hopsworks-5-2-1] instead of 5.2.0, as its breaking changes explain.

### What's changed

- Addressed vulnerabilities in model deployments.
- Addressed vulnerabilities in jobs (also in [5.1.1][hopsworks-5-1-1]).
- Fixed model deployments answering 403 to users whose password an administrator set.
  Such users already on a temporary password regain access at their next password change or account update.
- Fixed, on clusters with more than one RonDB MySQL server, library installs building on an older image of the environment and losing earlier installs, `insert(wait_for_online_ingestion=True)` returning before the rows were online, and apps reporting the execution they replaced.
- Fixed OpenSearch losing unflushed vectors and rejecting vector writes for about two minutes on its first start on 5.1 (also in [5.1.1][hopsworks-5-1-1]).
  A values file that sets `triggered: true` or `percent: 0.75`, or an upgrade with `--reuse-values`, keeps the problem.
- Fixed RonDB daemons ignoring SIGTERM, so every pod stop ended in a kill and a stopped data node could stall the cluster (also in [5.1.1][hopsworks-5-1-1]).
- Changed the RonDB REST server probes to outlast a data node failure and to use their own port (also in [5.1.1][hopsworks-5-1-1]).
- Fixed the RonDB REST server reading request bodies over 64 KiB as empty; it now buffers them in `rondb.rondb.rdrs.uploadPath` (also in [5.1.1][hopsworks-5-1-1]).
- Addressed vulnerabilities in the Airflow, HopsFS, Hive Metastore, Trino, Spark history server and Ray images, and in the Hopsworks server dependencies.
- Addressed vulnerabilities in the Payara, Hopsworks certificate authority, Grafana, Filebeat and Superset images and the MySQL and Redis of Superset (also in [5.1.2][hopsworks-5-1-2]).
- Fixed queued service operations failing on every retry when they removed a user from Superset or set up Superset for a project Observer (also in [5.1.2][hopsworks-5-1-2]).
- Changed Trino to read its users, groups, user catalogs and access rules from HopsFS instead of Secrets, which fixes `helm upgrade` failing on clusters with many Trino catalogs or project members.
- Fixed Helm 4 server-side apply conflicts on `helm upgrade` over the replicas of HPA-managed workloads other than the RonDB REST server, the rules of the Knative serving webhooks and the `rss-configuration` ConfigMap (see `HELM4_MIGRATION.md` in the 5.2 chart).
- Fixed the post-upgrade search index rebuild failing without the admin password, for example when password login is disabled, and running on every upgrade; it now runs in the background once per index format, and shows its progress and a **Reindex now** button under **Cluster settings > Service Operations > OpenSearch Index Commands** (also in [5.1.1][hopsworks-5-1-1]).
  An upgrade from 5.1.0 rebuilds the index, and search is incomplete until it finishes.
- Added the HopsFS CSI driver, on by default (`global._hopsworks.csi.enabled`), which mounts HopsFS into Jupyter, web terminal, Python and Ray job, Python app, Python deployment, Airflow and Trino pods without a privileged container; Trino needs it ([values][values-hopsfs-csi]).
- Added the KServe Standard deployment mode, the default for new model deployments, which runs a deployment as a Kubernetes Deployment instead of a Knative service; existing deployments keep Knative mode.
- Added KEDA 2.21 and its HTTP add-on, installed by default (`hopsworks.variables.kube_keda_installed`), to autoscale Standard-mode deployments on CPU, memory, requests or vLLM engine metrics and scale them to zero ([scaling][docs-autoscaling], [values][values-hw-keda]).
- Added the Factory, where users build ML systems and analytics tables in the web terminal, with their code in Git or in Hopsworks only; it needs `hopsworks.terminal.enabled` (`hopsworks.factory_enabled`, `hopsworks.factory_chat_enabled`) ([Factory][docs-factory]).
- Changed job, Jupyter, app and deployment logs to be read live from Kubernetes instead of being shipped to OpenSearch; Jupyter and app logs, and those of Python deployments with disk logging on (the default), are archived to the project's `Logs` dataset ([deployment logs][docs-serving-logs]).
- Changed LLM deployments to vLLM and vLLM-Omni v0.28.0; deployments created or edited on 5.1 keep v0.20.0 until you change their vLLM version, so keep the v0.20.0 images in a mirrored registry.
- Changed the built-in Python environments to Python 3.13; custom environments keep the Python version they were built with.
- Added support for Kubernetes 1.37; upgrade Hopsworks to 5.2 before the cluster, because 5.1 doesn't install on 1.37.
  Under ArgoCD 3.4 or older with server-side apply, upgrade ArgoCD to 3.5 or ignore `spec.preventPodSchedulingIfMissing` on CSIDrivers before moving to 1.37, or ArgoCD stops syncing (see `UPGRADE.md` in the 5.2 chart).
- Added sharing of Trino catalogs and feature groups with other projects, down to schemas, tables and columns, and private Trino catalogs of one user ([sharing][docs-trino-sharing], [private catalogs][docs-trino-private]).
- Added real-time feature logging to an online feature group, for feature views that start logging on 5.2 ([feature logging][docs-feature-logging]).
- Added scale to zero for idle Python apps when KEDA is installed, after `hopsworks.variables.pythonapp_idle_cooldown_seconds` (6 hours); with ingress-nginx, raise `nginx.ingress.kubernetes.io/proxy-read-timeout` in `hopsworks.ingress.annotations`, or the request that wakes an app fails after 60 seconds ([apps][docs-apps-idle]).
- Added database access for apps, on by default, which creates the project's online feature store database and gives the app its `MYSQL_*` connection variables; apps also get `TRINO_*` variables where the project has Trino ([database access][docs-apps-db]).
- Added Flask, Gradio and Node.js apps, which start from their app file like Streamlit apps ([app types][docs-apps-types]).
- Added versions of model deployments, so an earlier configuration can be activated again ([versions][docs-deployment-versions]).
- Added deployment schemas, which validate inference requests, and deployments of a model or a feature view without a predictor script ([deployment schema][docs-deployment-schema]).
- Added separate Python environments for the predictor and the transformer of a model deployment.
- Added per-member credentials for Oracle data sources, so that each member reads with their own username, password and wallet, also through Trino catalogs and in jobs, Jupyter, terminals and apps ([provided credentials][docs-ds-provided]).
- Added event-time windows to feature monitoring, the default for new configurations on feature groups and feature views with an event time; existing configurations are unchanged ([time basis][docs-fm-time-basis]).
- Added `spine_df` to `FeatureView.get_batch_data` and the training data methods, to read features for rows you supply, within `hopsworks.variables.featurestore_asof_spine_max_rows` and the related size limits.
- Changed removing a member from a project to hand their home directory to a Data Owner, chosen in the remove dialog, instead of leaving it unreadable ([removed members][docs-member-files]).
- Changed the feature store sharing card in the project settings to manage shares with projects and grants to restricted users, of the whole feature store or of single feature groups ([sharing][docs-fs-sharing]).
- Changed project creation to give every project Trino and Superset where the cluster runs them, also through the REST API, where a request without a service list created a project with Kafka only.
- Changed datasets to be searchable by name, description and tags; tags now attach to a whole dataset, and existing tags on files inside a dataset can be read and deleted but no longer added.
- Added the `TERMINAL` API key scope, so that the `hops` CLI can start, extend and attach to web terminal sessions and teleport Claude Code sessions to them; staged teleport files are deleted after `hopsworks.terminal.teleportTtlDays` (7), and the unused `KUBE` and `SINK` scopes are removed ([teleport][docs-teleport], [scopes][docs-api-scopes]).
- Added a memory guard to web terminals, on by default (`hopsworks.terminal.oomGuard`), which ends the process using the most memory instead of losing the session, and an out-of-memory notice when a session is lost anyway.
- Changed the Trino administrator, which the admin SQL console uses, to read only the `system`, `tpch` and `tpcds` catalogs.
- Changed reads of a feature view whose feature groups all come from one Snowflake data source to run the point-in-time joins in Snowflake.
- Added npm installs of many packages in one build, from a list, a `package.json` with its lockfile or a Git repository ([npm packages][docs-npm]).
- Added Trino connector table functions, such as `system.query`, for Data Owners on their project's Trino catalogs.
- Added Elasticsearch, ClickHouse and Teradata as data sources.
- Added backups and restores of the Superset database, on by default with the cluster backups ([disaster recovery][docs-superset-backup]).
- Added a `hopsworks_analytics` project, off by default (`hopsworks.variables.hopsworks_analytics`), for cluster-wide Superset dashboards on the Hopsworks metadata, which exposes user email addresses to every Hopsworks administrator and to the model provider of the dashboard setup ([values][values-hopsworks-analytics]).
- Added proxy tokens for apps and Superset, off by default (`hopsworks.variables.hopsable_proxy_enabled`), so that a gateway outside the cluster can relay requests to them for API-key clients.
- Added time-to-live settings to the feature group create and edit forms, which ask before a change deletes online rows ([TTL][docs-ttl]).
- Added an execution graph of the dbt models and tests to the executions of jobs on `dbt-pipeline` environments whose run writes one.
- Changed the SQL Runner of the Query Engine page to fill the page, show row numbers and column types, list a table's columns and draw `EXPLAIN (FORMAT GRAPHVIZ)` plans as a graph, and fixed it leaving queries running and completing no column names after `FROM` (also in [5.1.2][hopsworks-5-1-2]).
- Changed adding a member to a project to create the member's home directory in the background.
- Changed project creation to refuse a pre-created namespace longer than 25 characters, like a project name.
- Changed the Set up data source dialog to list each SQL engine and CRM vendor as its own choice, with a filter box, and the Snowflake form to accept a programmatic access token in its password field.
- Changed the Jupyter overview to show the server's log archives and its configuration, which is saved when you start Jupyter.
- Changed Hugging Face model imports to download a single commit, which can be given as a revision and is recorded in the model's description.
- Changed the coding agent instruction files in members' home directories, such as `AGENTS.md`, to be updated on upgrade unless the member edited them.
- Fixed filtered similarity search failing on embedding indices created before 5.1, which the upgrade rebuilds on faiss ([upgrading OpenSearch][docs-os-faiss]).
- Fixed ingestion statistics runs piling up on frequently written feature groups and leaving other jobs pending; at most one runs per feature group.
- Fixed deleted feature views, feature groups and projects coming back as empty entries, which blocked creating new ones with the same name.
- Fixed Trino giving a project access to only one of several feature stores shared with it (also in [5.1.1][hopsworks-5-1-1]).
- Fixed environment builds never starting when `rondb.rondb.priorityClass` is renamed (also in [5.1.1][hopsworks-5-1-1]).
- Fixed Python engine reads failing for queries with a filter on a joined feature group or a filter that compares features of two feature groups.
- Fixed writes to Iceberg feature groups from Python jobs and apps failing with `Unable to load libhdfs`.
- Fixed a Jupyter server that had just started failing requests on clusters with more than one Hopsworks instance.
- Fixed a killed Spark job with pending executors staying in the aggregating logs state for up to 20 minutes (also in [5.1.1][hopsworks-5-1-1]).
- Fixed project creation sometimes failing and rolling back on a group that "already exists".
- Fixed the Hopsworks admin pod starting before the database migrations had finished.
- Fixed the Hive Metastore `metastore-db-init` Job failing on a fresh install when it started before the HopsFS NameNode.
- Fixed Spark Connect in web terminals never starting on clusters that enforce the Kyverno restricted policies.
- Fixed agent deployments that mount HopsFS never starting on OpenShift.
- Fixed tags and keywords added right after an artifact was created missing from search.
- Fixed Git operations failing with an I/O error when a Git provider proxy is set and HopsFS encryption at rest is on.
- Fixed the table preview of a PostgreSQL data source failing for a role granted only some columns.
- Fixed ArrowFlight reads of PostgreSQL `uuid` columns.
- Fixed ArrowFlight queries of PostgreSQL data sources run by a read-only role.
- Fixed ArrowFlight reads of MySQL data sources without a password.
- Fixed ArrowFlight reads from S3 and AWS Glue data sources on OpenShift.
- Fixed the **Why?** button of an online ingestion in a feature group's activity opening every OnlineFS log of the project instead of that ingestion's; it is now named **Logs** (also in [5.1.1][hopsworks-5-1-1]).
- Fixed the dialogs of Git repository actions in the project settings closing on their own, and transformation function previews showing the imports of the defining module.

### Breaking changes

- Upgrade to 5.2 only from 5.1, satellites before central, with central and its satellites all under Helm or all under ArgoCD (see `UPGRADE.md` in the 5.2 chart).
- Upgrade 5.1 clusters to [5.2.1][hopsworks-5-2-1] instead of 5.2.0, whose OpenSearch index pass refuses every client and whose OpenSearch restarts delete the roles behind restricted-access grants and feature group shares; on [5.1.2][hopsworks-5-1-2], which fixed those restarts, 5.2.0 is a regression.
- The upgrade migrates Kafka from ZooKeeper to KRaft, which can't be undone: give `helm upgrade` a long enough `--timeout`, never pass `--atomic` (`--rollback-on-failure` in Helm 4) or run `helm rollback`, and under ArgoCD sync twice ([Kafka 4 and KRaft][docs-kafka4-expect]).
- On a cluster installed before 5.1, OpenSearch refuses every client while the upgrade copies its oldest indices; plan the outage and the timeout ([upgrading OpenSearch][docs-os]).
- OpenSearch snapshot repositories you configure yourself under `olk.opensearch.backup.repositories` or `olk.opensearch.restore.repositories`, on MinIO before `RELEASE.2025-01-20T14-49-07Z` or other S3-compatible stores that require `Content-MD5`, which OpenSearch 2.19 sent and 3.8 doesn't, need `legacy_md5_checksum_calculation: true` in their `s3` block, or the upgrade fails; the chart already sets it on the repositories it generates for the bundled MinIO ([upgrading OpenSearch][docs-os]).
- The chart now creates a cluster-wide IngressClass named `istio`, which 5.1 didn't; if the cluster already has one, set `kserve.istio.ingressClass.enabled: false`, or the upgrade fails.
- KEDA, installed by default where 5.1 didn't install it, can't share a Kubernetes cluster with another KEDA or the OpenShift Custom Metrics Autoscaler, including the KEDA of another Hopsworks release such as a satellite; set `hopsworks.variables.kube_keda_installed: false` on all but one (see `UPGRADE.md` in the 5.2 chart).
- With `hopsworks.rbac.useExistingRole: true`, add the chart's new ClusterRole grants (`charts/hopsworks/templates/role.yaml`) on `scaledobjects`, `interceptorroutes`, `ingresses`, `networkpolicies` and `csidrivers`, or model deployments, project creation and every pod that mounts HopsFS fail.
- On OpenShift, use the `values.openshift.yaml` of the 5.2 chart, which creates an SCC for the privileged HopsFS CSI node plugin, new in 5.2; if a cluster administrator owns SCCs, see `charts/hopsfs-csi/README.md` in the chart.
- The post-upgrade search index rebuild signs in as the agent user, instead of with `hopsworks.variables.admin_email` and `admin_password`, and fails the `helm upgrade` if `hopsworks.agent_email` and `hopsworks.agent_password` (default `agent@hops.io`, `admin`) don't match that account (also in [5.1.1][hopsworks-5-1-1]).
  Set them, or turn the rebuild off with `hopsworks.opensearchReindex.enabled: false`.
- The RonDB REST server now uses a probe port and an upload path that need RonDB 26.02.11, where 5.1.0 probed its REST port and set no upload path (also in [5.1.1][hopsworks-5-1-1]).
  If you pin `rondb.rondb.images.rondb.tag` to an older version, set `rondb.rondb.rdrs.probePort.enabled: false` and `rondb.rondb.rdrs.uploadPath: ""`, or the REST server doesn't start.
- Overrides of the Trino `initContainers`, `additionalVolumes` or `additionalVolumeMounts`, including those [5.1.0][hopsworks-5-1-0] asked for with `hopsworks.hopsfsMount.enabled: false`, fail the render; remove the overrides, or copy the new entries from the chart into them.
- If you override `trino.trino.image.tag`, use a Hopsworks Trino image of `483-v2` or later instead of the `480` images of 5.1, and set `global._hopsworks.trino.image.tag` to the same tag.
- If you set `trino.trino.serviceAccount.name`, set `trino.trinotest.serviceAccount.name` to the same name, because the test coordinator now shares the Trino account instead of creating its own `hopsworks-trino-test`, or the chart fails to render.
- Under ArgoCD, or with any `global._hopsworks.mode` other than `auto`, set `trino.auth.adminUserPwd` and `trino.auth.monitoringUserPwd`, which now default to empty instead of fixed passwords, or the chart fails to render.
- Removed the KServe local model controller; if you set `kserve.kserve.localmodel.enabled: true`, remove it, or the chart fails to render.
- With cluster backups on, Superset backups, new in 5.2, need an object store and, with `superset.auth.createSecrets: false`, the `backup.hops.works/include=true` label on its Secrets, or the chart fails to render; set `superset.backups.enabled: false` to skip them ([disaster recovery][docs-superset-backup]).
- If your release namespace is longer than 34 characters, set `global._hopsworks.csi.driverName`, because the default name of the HopsFS CSI driver, new in 5.2, would exceed 63 characters.
- With Helm 4, pass `--skip-crds` to a `helm install` on a cluster that already has the Strimzi CRDs, and after a reinstall run `helm upgrade` once to recreate the KEDA CRDs (see `UPGRADE.md` in the 5.2 chart).
- Kafka 4.3 rejects clients older than Apache Kafka 2.1 or librdkafka 1.8.2, which the Kafka 3.9 of 5.1 accepted; upgrade them first; with your own Kafka cluster, its brokers must run Kafka 2.1 or later ([client compatibility][docs-kafka4-clients]).
- Project namespaces now get a NetworkPolicy that admits traffic only from the same namespace and the Hopsworks namespace, where 5.1 restricted only web terminal pods; add any other namespace that reaches project pods, such as Istio or monitoring, to `hopsworks.variables.project_namespace_network_policy_allowed_namespaces` ([values][values-netpol]).
  Turning them off with `hopsworks.variables.project_namespace_network_policy_enabled: false` leaves the existing ones; delete them with `kubectl delete networkpolicy -A --field-selector metadata.name=hopsworks-project-isolation`.
- Trino no longer records the admin query history, and its records lose their query text after `hopsworks.variables.trino_events_strip_details_after_days` (7) instead of keeping it for 61 days; to keep either, or if your values restate `trino.trino.additionalConfigProperties`, see `UPGRADE.md` in the 5.2 chart (also in [5.1.2][hopsworks-5-1-2]).
- OpenSearch now reports its own version, `3.8.0`, instead of `7.10.2`; check clients that connect to it directly against the [OpenSearch 3.0 breaking changes](https://docs.opensearch.org/latest/breaking-changes/).
- MongoDB data sources need MongoDB 4.2 or later; upgrade older MongoDB servers, or browsing and testing their data sources fails.
- Web terminal sessions now last 8 hours instead of 4, and every upgrade sets `terminal_session_hours` from `hopsworks.terminal.sessionHours`, replacing a value set in the admin UI, which upgrades used to keep (see `UPGRADE.md` in the 5.2 chart).

### Deprecations

- Deprecated the name of `kafka.cluster.zookeeper`, which now sizes and places the KRaft controllers; its `services.client.annotations` is no longer read.
- Deprecated `hopsworks.variables.mount_hopsfs_in_python_job`, which only legacy Python jobs still read.
- Deprecated `global._hopsworks.trino.mountableSecrets.mechanism`, `global._hopsworks.trino.userCatalogShards`, `trino.auth.adminUserPwdHash`, `trino.auth.monitoringUserPwdHash` and `hw-kyverno.policyExceptions.trino`, which nothing reads any more.
- Deprecated the `environmentDTO` field of model deployments in the REST API; use `predictorEnvironment` and `transformerEnvironment`.

### Upgrade steps

No upgrade steps are listed for this release.

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

### Configuration changes

- Changed the defaults of `olk.opensearch.knn.circuit_breaker.triggered` to `false` and `olk.opensearch.knn.circuit_breaker.percent` to `75` (also in [5.1.1][hopsworks-5-1-1]).
- Changed the default of `hopsworks.variables.docker_operations_buildkit_priority_class` from `rondb-high-priority` to empty, so environment builds run at the default priority (also in [5.1.1][hopsworks-5-1-1]).
- Changed `rondb.rondb.terminationGracePeriodSeconds` to one value per component, and the data nodes' default from 60 to 300 seconds; an integer still sets only the data nodes (also in [5.1.1][hopsworks-5-1-1]).
- Changed `hopsworks.variables.trino_default_catalog` from `hive` to `delta`, the catalog new Superset connections to Trino open in.
- Changed the default driver memory of new Ray jobs (`hopsworks.variables.ray_job_driver_memory`) from 2048 to 4096 MB.
- Changed `values.openshift.yaml` to turn on credential files for Trino catalogs (`global._hopsworks.trino.mountableSecrets.enabled`).
- Changed `hopsworks.variables.trino_events_cleaner_batch_size` from 1000 to 100 (also in [5.1.2][hopsworks-5-1-2]).
- Changed `trino.trinotest.serviceAccount.create` to `false` and `name` to `hopsworks-trino`, so the test coordinator shares the Trino account.
- Changed the defaults of `trino.auth.adminUserPwd` and `trino.auth.monitoringUserPwd` to empty, so the chart generates the passwords.
- Fixed `values.openshift.yaml` for the OpenShift `restricted-v2` SCC, covering Strimzi, the Kafka brokers and KRaft controllers, the Spark operator and the MySQL and Redis of Superset, and turned off the Prometheus node exporter, which OpenShift ships itself (also in [5.1.1][hopsworks-5-1-1]).
  Use it with Helm 4 or Helm 3.17.1 or later, because older Helm 3 releases ignore its `null` overrides of subchart values.
- Fixed `global._hopsworks.jobs.ttlSecondsAfterFinished: 0` being replaced by `86400`.
- Fixed Helm 4 rejecting an empty `kafka.cluster.kafka.authorizer.authorizerClass`.
- Fixed the values schema rejecting `hopsworks.variables.loadbalancer_external_domain_namenode` and `hopsworks.variables.loadbalancer_external_domain_datanode` (also in [5.1.1][hopsworks-5-1-1]).
- Added `hopsworks.opensearchReindex.enabled` to turn off the post-upgrade search index rebuild, and `hopsworks.variables.command_search_fs_reindex_queue_wait_as_ms` to bound its wait for the search command queue (also in [5.1.1][hopsworks-5-1-1]).
- Added `kafka.cluster.kafka.config.replicationFactor` and `minInsyncReplicas` for multi-broker Kafka; `minInsyncReplicas` above a topic's replicas makes `acks=all` writes to it fail ([values][values-kafka]).
- Added `nodePort` values to pin the node ports of unmanaged external load balancers: ArrowFlight, OpenSearch, the HopsFS NameNode and DataNodes, Trino, the Hive Metastore, Kafka (`bootstrapNodePort`, `startingNodePort`) and the RonDB MySQL and REST servers (also in [5.1.1][hopsworks-5-1-1]).
  The RonDB ones ignore `global._hopsworks.externalLoadBalancers.managed` and apply only when `rondb.rondb.meta.mysqld.externalLoadBalancer.managed` or `rondb.rondb.meta.rdrs.externalLoadBalancer.managed` is `false`.
- Added `rondb.rondb.rdrs.probes` and `rondb.rondb.rdrs.probePort`, the settings and the port of the RonDB REST server probes, and `rondb.rondb.rdrs.maxKeepaliveRequests` to close a keep-alive connection after that many requests, so clients rebalance after a rolling restart (also in [5.1.1][hopsworks-5-1-1]).
- Added `rondb.rondb.rdrs.ttlPurge.enable` and `activeWindow` to turn off the TTL purge of the RonDB REST server or limit it to a daily window (also in [5.1.1][hopsworks-5-1-1]).
- Added `kserve.kserve.storage.resources` for the storage initializer that downloads models into deployment pods.
- Added `kserve.istio.ingressClass.enabled` and `kserve.istio.ingressClass.name` for the cluster-wide IngressClass the chart creates.
- Added `hopsworks.variables.kube_keda_installed` (default `true`), which installs KEDA and lets model deployments autoscale through it.
- Added `hopsworks.variables.project_namespace_network_policy_enabled` (default `true`) and `project_namespace_network_policy_allowed_namespaces` for the NetworkPolicy of project namespaces.
- Added `superset.backups.enabled` (default `true`) for the Superset backups.
- Added `global._hopsworks.csi.driverName` to name the HopsFS CSI driver of a release.
- Added `hopsworks.terminal.sessionHours` (default `8`), which every upgrade writes to the web terminal session length.

[docs-os-what-works]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade_opensearch/#opensearch-what-keeps-working
[docs-os-timeout]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade_opensearch/#opensearch-set-the-timeout
[docs-os-copy-51]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade_opensearch/#opensearch-copy-on-51
[docs-os-nmslib]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade_opensearch/#opensearch-nmslib-fields
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
[docs-os]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade_opensearch/
