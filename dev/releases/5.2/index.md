# Release notes { #hopsworks-5-2 }

The releases of Hopsworks 5.2, newest first.

## 5.2.3 { #hopsworks-5-2-3 }

Helm chart 5.2.3 · Released on 2026-10-29 · Changes since [5.2.2][hopsworks-5-2-2] · Python client [5.2.2](https://github.com/logicalclocks/hopsworks-api/releases/tag/5.2.2), unchanged

### Breaking changes

- [HELM] Mirror `envoyproxy/envoy:v1.38.0` to the path `envoyproxy/envoy` of your registry before the upgrade when `global._hopsworks.imageRegistry` points at your own: Python apps now pull their Envoy sidecar from that registry instead of Docker Hub, so air-gapped installs can start them ([Envoy image of Python apps][docs-upgrade-python-app-envoy]).

### Upgrade steps

Follow [Changes from 5.2.3][docs-upgrade-changes-from-523] in the upgrade guide.

### Configuration changes

- [HELM] Added `hopsworks.variables.python_app_envoy_image_version` (default `v1.38.0`), the tag of the Envoy sidecar of Python apps ([values][values-python-app-envoy]).

## 5.2.2 { #hopsworks-5-2-2 }

Helm chart 5.2.2 · Released on 2026-10-28 · Changes since [5.2.1][hopsworks-5-2-1] · Python client [5.2.2](https://github.com/logicalclocks/hopsworks-api/releases/tag/5.2.2)

### What's changed

- [API] Addressed vulnerabilities in the ArrowFlight server.
- [API] [FRONTEND] Addressed vulnerabilities in the Trino and Superset services of projects.
- [API] Fixed the OTLP sidecar of agent deployments with tracing running out of memory under ordinary traffic, which took the deployment out of service while the sidecar restarted; the sidecar now drops telemetry it can't keep up with instead of buffering it ([OTLP sidecar][docs-upgrade-otlp]).
- [API] [FRONTEND] [HELM] Fixed Python app pods staying in `ContainerCreating` after their execution ended; an app that was ready now ends only after `hopsworks.variables.pythonapp_unready_timeout_seconds` (600) without a ready container.
- [API] [FRONTEND] [HELM] Added GPU scheduling through NVIDIA Run:ai (`hopsworks.variables.run_ai_enable`, off by default), which binds every project to a Run:ai project so that Run:ai quotas, fair share and preemption apply to its pods, shows the project's GPU quota in the UI and adds `Project.get_gpu_availability()` to the Python client, which reports the cluster's GPUs when Run:ai is off; it can't be combined with Kueue ([Run:ai][docs-run-ai]).
- [API] [FRONTEND] [HELM] Added SharePoint data sources, which copy a folder of a SharePoint Online document library into a project dataset once or on a schedule, also with `SharePointConnector.create_sync` and `copy_folder` in the Python client and `hops datasource sharepoint`; `hopsworks.variables.enable_sharepoint_storage_connectors` turns them off ([SharePoint][docs-sharepoint]).
- [API] [FRONTEND] [HELM] Added Hopsworks data sources, which read the feature groups of a project on another Hopsworks cluster through ArrowFlight, as external feature groups or with dltHub ingestion, also with `hops datasource create hopsworks`; `hopsworks.variables.enable_hopsworks_storage_connectors` turns them off ([Hopsworks data source][docs-ds-hopsworks]).
- [API] [FRONTEND] Added Microsoft SQL Server and Azure SQL Database as SQL data sources, read through Spark, ArrowFlight, Trino catalogs and dltHub ingestion ([SQL Server][docs-ds-sqlserver]).
- [API] [FRONTEND] Added departments, which group projects: administrators create them and move projects between them in the cluster settings, and `hopsworks.create_project` in the Python client takes a `department`.
- [API] [FRONTEND] [HELM] Changed public (no-login) access to apps to cover every kind of app instead of only Streamlit apps, turned on by `hopsworks.variables.enable_public_apps` ([public access][docs-apps-public]).
- [API] [FRONTEND] Added a table viewer to the Apps page, and the dropping of an app's tables when the app is deleted, for apps created from 5.2.2 on, which create their tables with `App.create_table` and change them with `App.alter_table` in the Python client ([database access][docs-apps-db]).
- [API] Added `limit` to `FeatureGroup.read` and `ExternalFeatureGroup.read` in the Python client, and changed limited reads through ArrowFlight, such as `show(n)` and `hops fg preview`, to stop after that many rows instead of reading the whole feature group.
- [API] [FRONTEND] Fixed starting a terminal, notebook, Python job, Python app or deployment without enough project quota being accepted and then failing without a reason; the start is now refused with `Project quota exceeded`, and the Jupyter, Jobs and Deployments pages show the project's quota.
- [API] [FRONTEND] Fixed saving a Python app on a cluster with Kueue failing with `Queues in Kueue are not supported for:PythonApp`.
- [API] [FRONTEND] Fixed the Spark properties of a job or a Jupyter server written with spaces around `=`, such as `spark.executor.cores = 2`, being ignored.
- [API] Fixed `get_feature_groups` without a name in the Python client returning external feature groups and spine groups as managed ones, so `get_external_feature_groups` without a name returned none.
- [API] Fixed `hops fg create-external` saving the feature group without its `--query` or `--path`, added `--features` and `--online` to it and `--type` to `hops fg list`, and changed the type label of managed feature groups in `hops fg list` and `hops fg info` from `cached` to `managed`.
- [API] Fixed `hopsworks.login()` and Kafka inserts failing with `FileNotFoundError` on Windows, where the Python client used `/tmp`.
- [API] Fixed waiting for an online ingestion of no rows in the Python client lasting until its timeout, or forever with `timeout` 0.
- [API] [FRONTEND] Fixed apps whose name makes their Deployment name longer than 54 characters never scaling to zero when idle.
- [FRONTEND] Addressed vulnerabilities in Jupyter, Python apps, the Spark UI and the Ray dashboard.
- [FRONTEND] [HELM] Added **Compute Allocation** to the cluster settings of a cluster with Kueue, where administrators set the compute each department and project is guaranteed and can borrow, which Hopsworks applies as Kueue Cohorts and ClusterQueues, and follow its use.
  It needs `global._hopsworks.kueue.queueModel: per_project`, set at install; moving a running cluster from `shared`, the default, is not supported.
- [FRONTEND] [HELM] Added editing of node labels and priority classes to the **Kubernetes Scheduler** cluster settings, once `hopsworks.rbac.nodeLabels.edit` and `hopsworks.rbac.priorityClasses.edit` grant Hopsworks the permissions, both off by default.
  `hopsworks.rbac.nodeLabels.edit` grants patch on every node, which Kubernetes RBAC can't limit to labels, so it also allows changing taints.
- [FRONTEND] Changed **Extract** in the file browser to unzip or untar an archive in a background Terminal tab, instead of in a Spark job that copied it to a node's local disk and could fill it; without the Terminal it still runs the job.
- [FRONTEND] Added the selection of several files in the file browser, by dragging, Ctrl or Cmd-click and Shift-click, and their deletion with **Delete** or the Delete key.
- [FRONTEND] Added cancelling uploads in the file browser, per file or with **Cancel all**.
- [FRONTEND] Added sorting a dataset in the file browser by **Last update** and **Author**, and fixed going up to the dataset root after sorting a folder failing with HTTP 404.
- [FRONTEND] Added a **show shared** switch to the feature group list, which hides the feature groups shared with the project.
- [FRONTEND] Added a **Project limit reached** notice to the create project page, which turns off **Create New Project** once the user has reached their project limit, instead of showing only the error of a failed create.
- [FRONTEND] Fixed the **Add members** dialog saying every user is already a member on clusters with user search disabled.
- [FRONTEND] Fixed **Test connection** of Oracle data sources showing `Connection Failure` for a connection that works.
- [FRONTEND] Fixed the admin **Users** page not scrolling, which left most users out of reach, and added a sortable **Last login** column.
- [FRONTEND] Fixed error messages that were empty or generic for many failed actions, and 502 and 503 errors showing the raw HTML page of the ingress.
- [FRONTEND] Fixed a feature store shared with a project, or unshared from it, showing the change only after logging out and in again.
- [FRONTEND] Fixed a failed Jupyter start showing an exception class name, such as `KubeException`, instead of the reason.
- [HELM] Fixed Airflow on 5.2.0 and 5.2.1 having no `task_reschedule` table, and the upgrade from 5.1 emptying the Airflow tables after it, such as variables and XComs; the upgrade to 5.2.2 creates the missing table, and a failed conversion now fails the Airflow migrate Job.
  Rows that an earlier upgrade to 5.2.0 or 5.2.1 lost are not restored: re-create them or restore them from a backup.
- [HELM] Fixed an OpenSearch snapshot restore leaving the `.opendistro_security` index closed, after which OpenSearch crash-loops ([recover a cluster restored on 5.2.0 or 5.2.1][docs-os-restore-crash-loop]).
- [HELM] Fixed a fresh `helm install --wait` hanging when it ran more than an hour after the Trino auth seed Job finished, because the Job's TTL deleted it.
- [HELM] Added support for Kubernetes 1.33, which the chart refused below 1.34.
- [HELM] Changed the KEDA CRD upgrade hook to read the CRDs from the `hopsworks/keda-crds` image (`hw-keda.crdUpgradeJob.image`) instead of a hook ConfigMap, which took 13% of the 1 MiB Helm release Secret; mirror that image on an airgapped cluster ([KEDA CRDs][docs-keda-crds]).
- [HELM] Moved the upgrade guide and the Helm 4 migration notes from the chart's `UPGRADE.md` and `HELM4_MIGRATION.md` to the docs ([upgrading Hopsworks][docs-upgrade], [upgrading with Helm 4][docs-helm4]).
- [HELM] Fixed the Jobs of the VPA install and uninstall, the Kueue objects, the Trino auth seed, the Airflow key bootstrap, Velero backups and the OpenSearch reindex ignoring `global._hopsworks.nodeSelector` and `global._hopsworks.tolerations`, and the wipe Job ignoring `global._hopsworks.nodeSelector` ([dedicated node pools][docs-node-pools]).
- [HELM] Fixed the `TooManyShards` alert never firing; a cluster above 90% of its shard limit starts alerting after the upgrade.
- Addressed vulnerabilities in the Hopsworks server image and its dependencies, the UI dependencies and the database migration image.
- Addressed vulnerabilities in the Superset, Prometheus, Grafana, OpenSearch Dashboards, OpenSearch metrics exporter, Logstash and Trino images.
- Addressed vulnerabilities in the Python environment base images and in the Airflow, terminal, Kafka, Vertical Pod Autoscaler, Spark operator CRD, KServe, KEDA HTTP add-on, remote shuffle service init and BuildKit images.
- Fixed the statistics cleaner's query taking an hour or more per run on clusters with many feature statistics, during which it blocked the schema migrations of the statistics tables.
- Fixed the Superset Redis being OOM-killed every few hours by zombie processes its health probes left behind.
- Changed the RonDB REST server to size its buffer pool from its memory limit, return idle buffers after 15 minutes and opt out of transparent huge pages, so that its memory stays bounded.

### Breaking changes

- [API] [FRONTEND] [HELM] Changed how OnlineFS checks the topic of the records it writes, to address a vulnerability ([what this affects][docs-upgrade-onlinefs]).
  Restart the producers that hold on to a topic after it changes; on a Kafka where records reach OnlineFS on a renamed topic, such as a mirrored secondary, set `onlinefs.configmapOverrides.onlinefssite.service.verifyFeatureGroupTopic: false`.
- [API] [FRONTEND] On a cluster with Kueue, Spark jobs are now queued by Kueue and run with static executors instead of dynamic allocation: a job saved with dynamic allocation runs its dynamic-allocation minimum, at least one executor, and `spark.dynamicAllocation.enabled=true` is refused; set `spark.executor.instances` for more executors ([what changes][docs-kueue-what-changes]).
- [API] [FRONTEND] The upgrade deletes the Deployment of every Python app whose executions have all ended, also one that still answers requests; start such an app again to keep it running.
- [API] [FRONTEND] Apps created from 5.2.2 on can only read the online feature store database, apart from the tables they create with `App.create_table` and change with `App.alter_table` in the Python client, or with `createTable` and `alterTable` of `@hopsworks/app` in Node.js; before, the apps of Data Owners could create, alter and write to any of its tables with their own SQL ([database access][docs-apps-db]).
- [API] Python clients older than 5.2.2 fail to list the data sources of a feature store that has a Hopsworks or SharePoint data source; use the 5.2.2 client in the jobs and environments that list them ([client version][docs-sharepoint-client]).
- [API] [FRONTEND] Ingestion from a MongoDB data source, and fetching its schema, now needs MongoDB 4.4 or later instead of 4.2.
- [FRONTEND] Because of a security fix, open Jupyter servers from the Hopsworks UI.
- [FRONTEND] Because of a security fix, give a Python app that calls Hopsworks credentials of its own, such as an API key.
- [HELM] Hopsworks now uses Kueue 0.20.3 installed as its own release, `kueue` in `kueue-system`, instead of the Kueue 0.12.2 bundled in its namespace, and the chart refuses to render while the bundled Kueue still runs ([Kueue outside the Hopsworks namespace][docs-upgrade-kueue-external]).
  With `global._hopsworks.kueue.enabled: true`, move Kueue with the 5.1 chart's `migrate-to-external.sh` before the upgrade, run the chart's `upgrade-kueue.sh` after it, and remove `hw-kueue.managerConfig`, `hw-kueue.nameOverride` and every `hw-kueue.kueue` value but `enabled` from your values, or the values schema rejects the upgrade.
- [HELM] Remove `rondb.rondb.rdrs.internal.bufferSize`, `gomaxprocs` and `maxAllocatedBuffers` from your values, which the chart ignored, or `helm upgrade` fails before changing anything.
- [HELM] The hopsworks, HopsFS and Hive schema migrations now run on the DDL SQL node instead of the application SQL nodes, so they no longer wait for application queries; a cluster that disables it (`rondb.rondb.meta.ddlMySQLd.enabled: false`) sets `hopsworks.dependencies.mysql.ddlConsulServiceName`, `hopsfs.dependencies.mysql.ddlConsulServiceName` and `hive.metastore.dependencies.mysql.ddlConsulServiceName` to `mysql`, or the migrations wait for a SQL node that doesn't exist ([DDL SQL node][docs-upgrade-ddl]).
- [HELM] The chart package no longer ships `values.aws.yaml`, `values.azure.yml`, `values.gcp.yaml`, `values.rhel8.yaml` and `values.nodeselector-tolerations.yaml`; keep a copy of the one you pass, or start from the values file of the [AWS][docs-setup-aws], [Azure][docs-setup-azure] or [GCP][docs-setup-gcp] setup guide and take the RHEL 8 and node pool values from [Python build performance][docs-buildkitd-rhel8] and [dedicated node pools][docs-node-pools].

### Deprecations

- [HELM] Deprecated `hopsworks.variables.streamlit_sharing`; use `hopsworks.variables.enable_public_apps`, which covers every kind of app, and `true` in either one turns public access on.

### Upgrade steps

Follow [Changes from 5.2.2][docs-upgrade-changes-from-522] in the upgrade guide.

### Upgraded components

| Component | 5.2.1 | 5.2.2 |
| --------- | ----- | ----- |
| Airflow image | 5.2.0 | 5.2.1 |
| Alertmanager | 0.34.0-alpine-h1.1 | 0.34.0-alpine-h2.1 |
| ArrowFlight server | 5.2.0 | 5.2.1 |
| Base environment images | 5.2.1 | 5.2.3 |
| BuildKit | v0.32.2 | v0.34.1 |
| Grafana | 12.4.9-h12 | 12.4.13-h0 |
| Kafka | 1.2.0-kafka-4.3.1-h1 | 1.2.0-kafka-4.3.1-h2 |
| KEDA HTTP add-on | 0.16.0 | 0.16.0-h2 |
| KServe | v0.21.0 | 0.21.0-h1 |
| KServe RBAC proxy | v0.18.0 | v0.23.0 |
| KServe utilities | 0.1.11 | 0.1.12 |
| kube-state-metrics | v2.12.0 | 2.20.0-alpine-h2.0 |
| Logstash | 7.17.29.6 | 7.17.29.7 |
| MySQL Connector/J | 8.0.21.1 | 8.0.21.2 |
| OnlineFS | 2.5 | 2.5.2 |
| OpenSearch Dashboards | 3.8.0.0 | 3.8.0.1 |
| OpenSearch metrics exporter | 1.11.0-alpine-h1.1 | 1.11.0-alpine-h2.1 |
| Payara | 6.2025.11-jdk21.1 | 6.2025.11-jdk21.2 |
| Prometheus | 3.14.0-alpine-h1.1 | 3.15.1-alpine-h2.0 |
| Prometheus adapter | 0.12.0-alpine-h1.1 | 0.12.0-alpine-h2.1 |
| Prometheus config reloader | 0.93.1-alpine-h1.1 | 0.93.1-alpine-h2.1 |
| Prometheus node exporter | 1.12.1-alpine-h1.1 | 1.12.1-alpine-h2.1 |
| Pushgateway | 1.11.3-alpine-h1.1 | 1.11.3-alpine-h2.1 |
| Remote shuffle service init image | 0.9.2 | 0.9.3 |
| RonDB | 26.02.11 | 26.02.12 |
| Spark operator | 2.5.1-h1-1.9 | 2.5.1-h1-1.10 |
| Superset | 6.0.0p4.5 | 6.0.0p4.6 |
| Superset init image | 0.14.0-alpine-h1.1 | 0.14.0-alpine-h2.1 |
| Superset MySQL | 8.4.11-ubuntu24.04-h5 | 8.4.13-ubuntu24.04-h0 |
| Superset MySQL metrics exporter | 0.20.0-alpine-h1.1 | 0.20.0-alpine-h2.1 |
| Superset MySQL volume permissions image | 12-alpine-h1.1 | 12-alpine-h2.1 |
| Superset Redis | 7.4.11-alpine-h2 | 7.4.11-alpine-h4 |
| Superset Redis metrics exporter | 1.90.0-alpine-h1.1 | 1.90.0-alpine-h2.1 |
| Trino | 483-v2 | 483-v3 |
| Vertical Pod Autoscaler installer | 1.7.1-2 | 1.7.1-3 |

### Configuration changes

- [HELM] Changed the memory request and limit of the RonDB REST server pods (`rondb.rondb.resources.requests.memory.rdrsMiB`, `rondb.rondb.resources.limits.memory.rdrsMiB`) from 100 MiB and 500 MiB to 2 GiB; check node capacity before the upgrade.
- [HELM] Changed the default of `hopsworks.variables.agent_deployment_otel_memory_mb`, the memory request and limit of the OTLP sidecar of traced agent deployments, from 1024 to 2048.
  Each traced agent deployment reserves it on its node once it is recreated, so check node memory before you redeploy them ([OTLP sidecar][docs-upgrade-otlp]).
- [HELM] Changed the default of `trino.authSeeder.ttlSecondsAfterFinished` from 3600 to `null`, which keeps the finished Trino auth seed Job for `global._hopsworks.jobs.ttlSecondsAfterFinished` (1 day).
- [HELM] Removed `hw-kueue.managerConfig`, `hw-kueue.nameOverride` and the `hw-kueue.kueue` values but `enabled`, which configured the Kueue the chart bundled until 5.2.1.
- [HELM] Removed the Kueue image from `values.airgap.yaml`, because the chart no longer installs Kueue; pass the mirrored image and chart to `upgrade-kueue.sh` with `--kueue-image` and `--kueue-repo` instead.
- [HELM] Added `global._hopsworks.kueue.namespace` (default `kueue-system`), the namespace of the Kueue release Hopsworks uses.
- [HELM] Added `hw-kueue.enforcePrerequisiteCheck` (default `true`); `false` skips the check that refuses to render while the bundled Kueue 0.12 or its `v1alpha1` storage is still on the cluster, or while no Kueue serving `v1beta2` is installed.
- [HELM] Added `onlinefs.configmapOverrides.onlinefssite.service.verifyFeatureGroupTopic` (default `true`), which turns off the OnlineFS check that a record arrived on the online topic of its feature group.
- [HELM] Added `hopsworks.dependencies.mysql.ddlConsulServiceName`, `hopsfs.dependencies.mysql.ddlConsulServiceName` and `hive.metastore.dependencies.mysql.ddlConsulServiceName` (default `mysqlddl`), the SQL node the schema migrations connect to.
- [HELM] Added the RonDB REST server settings the chart didn't expose, under `rondb.rondb.rdrs`, such as its buffer pool, its request, BLOB and batch size limits, its rate limit and its use of transparent huge pages.

## 5.2.1 { #hopsworks-5-2-1 }

Helm chart 5.2.1 · Released on 2026-10-16 · Changes since [5.2.0][hopsworks-5-2-0] · Python client [5.2.1](https://github.com/logicalclocks/hopsworks-api/releases/tag/5.2.1), unchanged

### What's changed

- [API] [FRONTEND] [HELM] Fixed OpenSearch restarts and the 5.1 to 5.2 index pass deleting the OpenSearch roles behind restricted grants and feature group shares, which left a shared project with HTTP 403.
  Grants and shares made before the last OpenSearch restart before this upgrade lost their roles, and granting or sharing again is refused: revoke and grant again, or unshare and share again.
- [HELM] Fixed the 5.1 to 5.2 index pass losing documents that were not yet refreshed when it copied an index.
- [HELM] Fixed the 5.1 to 5.2 index pass failing with `field _id not found` on an index with an empty mapping, such as a `projects` index that was never written.
- [HELM] Addressed vulnerabilities in OpenSearch.
  It applies once an OpenSearch pod logs `Security configuration applied` after the upgrade; if none does, run `run_security_admin.sh` as [Security configuration][docs-os-security] shows.
- [HELM] Changed the OpenSearch index pass of the 5.1 to 5.2 upgrade to copy one index at a time behind a write block on that index alone, instead of refusing every OpenSearch client, reads included, for the whole pass; upgrade 5.1 clusters to 5.2.1 rather than 5.2.0 ([what keeps working][docs-os-what-works]).
- [HELM] Changed the OpenSearch index pass to run before the Kafka migration, so its report (`olk.opensearch.indexUpgrade.mode: report`) and its refusals stop an upgrade from 5.1 before anything changes ([set the timeout][docs-os-timeout]).
- [HELM] Fixed the OpenSearch index pass not refusing a 5.0 cluster, still on OpenSearch 1.x, which can't be upgraded straight to 5.2.
- [HELM] Fixed every `helm upgrade` restarting OpenSearch.

### Breaking changes

- [API] [FRONTEND] [HELM] Because of a security fix, share the whole feature group with a project that queries it in Trino and may read all its features.
  `hopsworks.variables.trino_feature_group_subset_shares_enabled: "true"` keeps the behaviour of 5.2.0, without the fix.
- [HELM] Remove `olk.opensearch.indexUpgrade.enabled` from your values, using `olk.opensearch.indexUpgrade.mode: report` in place of `false`, or the values schema rejects the upgrade.
- [HELM] `helm upgrade` now stops before changing anything, also on a cluster already on 5.2.0, if an OpenSearch vector field would still be served by nmslib, which crashes OpenSearch 3.8 nodes on CPUs without AVX-512, where 5.2.0 upgraded without checking; apply the remedy the hook's log gives for each index or template it names ([nmslib fields][docs-os-nmslib]).

### Configuration changes

- [HELM] Changed `olk.opensearch.indexUpgrade.enabled` to `olk.opensearch.indexUpgrade.mode`: `copy`, the default, or `report`, which lists the indices the 5.1 to 5.2 upgrade would copy and how long each stays blocked, and fails before anything changes, the Kafka migration included ([set the timeout][docs-os-timeout]).
  From 5.1.2 the 5.1 chart reads the same key to copy the indices before the 5.2 upgrade; pass it with `--set`, not in your values file ([copying on 5.1][docs-os-copy-51]).
- [HELM] Added `hopsworks.variables.trino_feature_group_subset_shares_enabled` (default `"false"`), which turns off the fix of a vulnerability in Trino queries of shared feature groups.

## 5.2.0 { #hopsworks-5-2-0 }

Helm chart 5.2.0 · Released on 2026-10-15 · Changes since [5.1.0][hopsworks-5-1-0] · Python client 5.2.1 ([5.2.0](https://github.com/logicalclocks/hopsworks-api/releases/tag/5.2.0), [5.2.1](https://github.com/logicalclocks/hopsworks-api/releases/tag/5.2.1))

### What's changed

- [API] Addressed vulnerabilities in the Java client dependencies.
- [API] [FRONTEND] Addressed vulnerabilities in model deployments.
- [API] [FRONTEND] Fixed, on clusters with more than one RonDB MySQL server, library installs building on an older image of the environment and losing earlier installs, `insert(wait_for_online_ingestion=True)` returning before the rows were online, and apps reporting the execution they replaced.
- [API] Fixed OnlineFS leaving out of the online store a row with a null in a nullable `TEXT` column of an online feature group.
- [API] Fixed `FeatureView.init_serving` in the Python client never releasing its online store connections, so a process serving many feature views could exhaust the connections of the RonDB MySQL servers.
- [API] [FRONTEND] [HELM] Added the KServe Standard deployment mode, the default for new model deployments, which runs a deployment as a Kubernetes Deployment instead of a Knative service; existing deployments keep Knative mode, and `knative_mode` of a predictor in the Python client chooses the mode.
- [API] [FRONTEND] [HELM] Added KEDA 2.21 and its HTTP add-on, installed by default (`hopsworks.variables.kube_keda_installed`), to autoscale Standard-mode deployments on CPU, memory, requests or vLLM engine metrics and scale them to zero, set with `autoscaler` of a predictor's scaling configuration in the Python client ([scaling][docs-autoscaling], [values][values-hw-keda]).
- [API] [FRONTEND] [HELM] Changed LLM deployments to vLLM and vLLM-Omni v0.28.0 (`hopsworks.variables.kube_serving_vllm_versions`, `hopsworks.variables.kube_serving_vllm_omni_versions`); deployments created or edited on 5.1 keep v0.20.0 until you change their vLLM version, so keep the v0.20.0 images in a mirrored registry.
- [API] [FRONTEND] [HELM] Added the Factory, where users build ML systems and analytics tables in the web terminal, with their code in Git or in Hopsworks only; it needs `hopsworks.terminal.enabled` (`hopsworks.factory_enabled`, `hopsworks.factory_chat_enabled`) ([Factory][docs-factory]).
- [API] [FRONTEND] [HELM] Changed job, Jupyter, app and deployment logs to be read live from Kubernetes instead of being shipped to OpenSearch; Jupyter and app logs, and those of Python deployments with disk logging on (the default), are archived to the project's `Logs` dataset, which `Deployment.download_logs` in the Python client downloads for a deployment ([deployment logs][docs-serving-logs]).
- [API] [FRONTEND] Changed the built-in Python environments to Python 3.13 on Ubuntu 26.04, with PyTorch 2.13, transformers 5.17, accelerate 1.15, DeepSpeed 0.19 and LangChain 1.4 in the environments that ship them; custom environments keep the Python version they were built with.
- [API] Added support for Python 3.14 to the Python client.
- [API] [FRONTEND] [HELM] Added real-time feature logging to an online feature group, the default transport (`hopsworks.variables.serving_feature_logging_transport`) for feature views that start logging on 5.2 ([feature logging][docs-feature-logging]).
- [API] [FRONTEND] [HELM] Added scale to zero for idle Python apps when KEDA is installed, after `hopsworks.variables.pythonapp_idle_cooldown_seconds`, which `create_app` in the Python client sets per app with `idle_scale_to_zero` and `idle_cooldown_seconds` ([apps][docs-apps-idle]).
  With ingress-nginx, raise `nginx.ingress.kubernetes.io/proxy-read-timeout` in `hopsworks.ingress.annotations`, or the request that wakes an app fails after 60 seconds.
- [API] [FRONTEND] Added database access for apps, on by default (`db_access` of `create_app` in the Python client), which creates the project's online feature store database and gives the app its `MYSQL_*` connection variables; apps also get `TRINO_*` variables where the project has Trino ([database access][docs-apps-db]).
- [API] [FRONTEND] Added Flask, Gradio and Node.js apps (`app_kind` of `create_app` in the Python client), which start from their app file like Streamlit apps ([app types][docs-apps-types]).
- [API] [FRONTEND] Added versions of model deployments, so an earlier configuration can be activated again, in the Python client with `Deployment.rollback` ([versions][docs-deployment-versions]).
- [API] [FRONTEND] Added deployment schemas, which validate inference requests, and deployments of a model or a feature view without a predictor script ([deployment schema][docs-deployment-schema]).
- [API] [FRONTEND] Added separate Python environments for the predictor and the transformer of a model deployment (`environment` of `Transformer` in the Python client).
- [API] [FRONTEND] Added per-member credentials for Oracle data sources, so that each member reads with their own username, password and wallet, also through Trino catalogs and in jobs, Jupyter, terminals and apps ([provided credentials][docs-ds-provided]).
- [API] [FRONTEND] Added event-time windows to feature monitoring, the default for new configurations on feature groups and feature views with an event time; existing configurations are unchanged ([time basis][docs-fm-time-basis]).
- [API] [FRONTEND] [HELM] Added `spine_df` to `FeatureView.get_batch_data` and the training data methods, to read features for rows you supply, within `hopsworks.variables.featurestore_asof_spine_max_rows` and the related size limits.
- [API] [FRONTEND] Changed removing a member from a project to hand their home directory to a Data Owner, chosen in the remove dialog or with `new_file_owner` of `Project.remove_member` in the Python client, instead of leaving it unreadable ([removed members][docs-member-files]).
- [API] [FRONTEND] Changed project creation to give every project Trino and Superset where the cluster runs them, also through the REST API, where a request without a service list created a project with Kafka only.
- [API] [FRONTEND] Changed datasets to be searchable by name, description and tags; tags now attach to a whole dataset, and existing tags on files inside a dataset can be read and deleted but no longer added.
- [API] [FRONTEND] [HELM] Added the `TERMINAL` API key scope, so that the `hops` CLI can start, extend and attach to web terminal sessions and teleport Claude Code sessions to them, which the UI opens from a `?terminal=open` link; staged teleport files are deleted after `hopsworks.terminal.teleportTtlDays` (7), and the unused `KUBE` and `SINK` scopes are removed ([teleport][docs-teleport], [scopes][docs-api-scopes]).
- [API] Added the Hopsworks skills for coding agents to the Python client package, so that `hops skills install` adds them to a repository on your own machine, and changed `hops setup` to write `AGENTS.md` and `.claude/` files for coding agents into the current directory unless given `--no-scaffold` ([coding agents][docs-agent-skills]).
- [API] Added `hops logout`, and changed `hops setup` to ask for the host again, so that it can move to another cluster.
- [API] Changed `hops datasource create` to create every data source type.
- [API] Changed the `hops` CLI to explain a failed request, such as one with an API key that lacks a scope, instead of printing a traceback, and `hops project list` to list every project you are a member of instead of only the active one.
- [API] Changed reads of a feature view whose feature groups all come from one Snowflake data source to run the point-in-time joins in Snowflake.
- [API] Changed online feature vector reads and model deployment predictions in the Python client to make fewer round trips, and concurrent reads through one feature view to run in parallel instead of one at a time; `Deployment.init_predict` prepares a deployment's first prediction ahead of it.
- [API] Changed `import hopsworks` and `hopsworks.login()` in the Python client to take a fraction of the time, which also speeds up every `hops` command.
- [API] Added `timeout` to `FeatureView.get_feature_vector` and `get_feature_vectors` in the Python client, a deadline for the whole online read.
- [API] Added `Query.read_batches` to the Python client, which reads a query as Arrow record batches instead of loading the whole result.
- [API] Added `ModelServing.get_vllm_image_tags` to the Python client, which lists the vLLM image tags an LLM deployment can use.
- [API] Changed `FeatureGroup.remove_rows` in the Python client to also delete the online rows of a feature group with an embedding index from the vector database, where it deleted only the offline rows.
- [API] Changed the first offline materialization of a feature group written from Spark to start at the feature group's creation instead of the oldest record of the project's online topic; the `initial_offset_margin_hours` write option (1 by default) moves the start earlier to allow for clock skew.
- [API] [FRONTEND] Added npm installs of many packages in one build, from a list, a `package.json`, with or without its lockfile, or a Git repository, in the Python client with `Environment.install_npm`, `install_npm_from_package_json` and `install_npm_from_git` ([npm packages][docs-npm]).
- [API] [FRONTEND] [HELM] Added Elasticsearch, ClickHouse and Teradata as data sources; `hopsworks.variables.enable_elasticsearch_storage_connectors` turns Elasticsearch data sources off.
- [API] [FRONTEND] Added a suggested feature group description to the metadata a data source infers for a table, which the feature group form fills in and `DataSource.infer_metadata` in the Python client returns as `suggested_description`.
- [API] [HELM] Added proxy tokens for apps and Superset, off by default (`hopsworks.variables.hopsable_proxy_enabled`), so that a gateway outside the cluster can relay requests to them for API-key clients.
- [API] [FRONTEND] Changed Hugging Face model imports to download a single commit, which can be given with `revision` of `ModelRegistry.hf_download` in the Python client, and to record it in the model's description.
- [API] [HELM] Added Trino connector table functions, such as `system.query`, for Data Owners on their project's Trino catalogs.
- [API] [FRONTEND] Changed adding a member to a project to create the member's home directory in the background.
- [API] [FRONTEND] Changed project creation to refuse a pre-created namespace longer than 25 characters, like a project name.
- [API] Changed the Python client to accept opensearch-py 3.
- [API] [HELM] Fixed filtered similarity search failing on embedding indices created before 5.1, which the upgrade rebuilds on faiss ([upgrading OpenSearch][docs-os-faiss]).
- [API] Fixed `find_neighbors` in the Python client failing with `Engine [NMSLIB] does not support filters` on embedding feature groups created before 5.1, and failing on a project's default embedding index when fewer rows than `k` match (also in [5.1.1][hopsworks-5-1-1]).
- [API] Fixed writes to Iceberg feature groups failing with `Unable to load libhdfs` from Python jobs, apps and DLT jobs, and with `Unable to load libjvm` from web terminals.
- [API] Fixed model deployments answering 403 to users whose password an administrator set.
  Such users already on a temporary password regain access at their next password change or account update.
- [API] [FRONTEND] Fixed ingestion statistics runs piling up on frequently written feature groups and leaving other jobs pending; at most one runs per feature group.
- [API] [FRONTEND] Fixed deleted feature views, feature groups and projects coming back as empty entries, which blocked creating new ones with the same name.
- [API] Fixed external Spark clients failing to read, write or delete DELTA feature groups when the HopsFS NameNode and DataNode load balancers are turned off (also in [5.1.2][hopsworks-5-1-2]).
- [API] Fixed `Deployment.start()` and `save()` in the Python client returning before the deployment could be reached, so that the first `predict()` failed with "Deployment not created or running".
- [API] [FRONTEND] Fixed a change of an LLM deployment's vLLM version being dropped, so that the deployment restarted on its old image, and LLM deployments failing to restart or update once an administrator removed their version from `hopsworks.variables.kube_serving_vllm_versions` or `hopsworks.variables.kube_serving_vllm_omni_versions`.
- [API] Fixed `get_feature_vectors` in the Python client failing a whole batch with HTTP 400 through the REST client on an entry with a null primary key, which the SQL client served.
- [API] Fixed the first insert from the Python engine into a feature group whose Kafka topic had just been created failing with `NOT_LEADER_FOR_PARTITION`.
- [API] Fixed inserts from the Python engine failing on a timestamp column holding a null (`NaT`).
- [API] Fixed Kafka clients started at the same time in one Python client process, such as two streaming pipelines on two threads, failing with `ssl.ca.location failed` while another rewrote the certificate files they share.
- [API] Fixed `DataSource.infer_metadata` in the Python client failing with `AttributeError: 'dict' object has no attribute 'name'`.
- [API] Fixed the Python client installing pyarrow 26 next to NumPy 1, with which importing `hsfs.feature_group` fails with `pyarrow requires NumPy 2.0 or newer`; it now requires pyarrow below 26 (also in [5.1.2][hopsworks-5-1-2]).
- [API] Fixed `hops sql` failing with `Schema '<project>' does not exist` unless given a schema; it now reads the project's feature store in the `delta` catalog by default, so pass `--catalog iceberg` for Iceberg feature groups.
- [API] Fixed `hops` commands, such as `hops setup`, failing on a machine with PySpark installed.
- [API] Fixed `create_feature_view` not warning, and `get_feature_vector` giving a misleading error, when a feature view selects the time partition columns of a Hudi feature group, which are offline only.
- [API] Fixed Python engine reads failing for queries with a filter on a joined feature group or a filter that compares features of two feature groups.
- [API] [FRONTEND] Fixed a killed Spark job with pending executors staying in the aggregating logs state for up to 20 minutes (also in [5.1.1][hopsworks-5-1-1]).
- [API] [FRONTEND] Fixed the logs of Ray jobs missing the output of their workers when copying the head's log files took longer than five minutes.
- [API] [FRONTEND] Fixed project creation sometimes failing and rolling back on a group that "already exists".
- [API] [FRONTEND] Fixed tags and keywords added right after an artifact was created missing from search.
- [API] [FRONTEND] Fixed Trino giving a project access to only one of several feature stores shared with it (also in [5.1.1][hopsworks-5-1-1]).
- [API] [FRONTEND] Fixed Git operations failing with an I/O error when a Git provider proxy is set and HopsFS encryption at rest is on.
- [API] [FRONTEND] Fixed agent and Python deployments that mount HopsFS never starting on OpenShift.
- [API] [FRONTEND] Fixed the table metadata of a PostgreSQL data source without a schema coming back empty, and the table lists and metadata of Redshift, Snowflake and BigQuery data sources failing on names with backslashes or on a Snowflake database name that isn't a plain identifier.
- [API] Fixed ArrowFlight reads of PostgreSQL `uuid` columns.
- [API] Fixed ArrowFlight queries of PostgreSQL data sources run by a read-only role.
- [API] Fixed ArrowFlight reads of MySQL data sources without a password.
- [API] Fixed ArrowFlight reads from S3 and AWS Glue data sources on OpenShift.
- [FRONTEND] [HELM] Fixed the post-upgrade search index rebuild failing without the admin password, for example when password login is disabled, and running on every upgrade; it now runs in the background once per index format, and shows its progress and a **Reindex now** button under **Cluster settings > Service Operations > OpenSearch Index Commands** (also in [5.1.1][hopsworks-5-1-1]).
  An upgrade from 5.1.0 rebuilds the index, and search is incomplete until it finishes.
- [FRONTEND] [HELM] Added sharing of Trino catalogs and feature groups with other projects, down to schemas, tables and columns, and private Trino catalogs of one user ([sharing][docs-trino-sharing], [private catalogs][docs-trino-private]).
- [FRONTEND] Changed the feature store sharing card in the project settings to manage shares with projects and grants to restricted users, of the whole feature store or of single feature groups ([sharing][docs-fs-sharing]).
- [FRONTEND] [HELM] Added a memory guard to web terminals, on by default (`hopsworks.terminal.oomGuard`), which ends the process using the most memory instead of losing the session, and an out-of-memory notice when a session is lost anyway.
- [FRONTEND] [HELM] Added a `hopsworks_analytics` project, off by default (`hopsworks.variables.hopsworks_analytics`), for cluster-wide Superset dashboards on the Hopsworks metadata, which exposes user email addresses to every Hopsworks administrator and to the model provider of the dashboard setup ([values][values-hopsworks-analytics]).
- [FRONTEND] Changed the Jupyter overview to show the server's log archives and its configuration, which is saved when you start Jupyter.
- [FRONTEND] Added tabs for the windows of a web terminal session, which open, close and rename them.
- [FRONTEND] Added time-to-live settings to the feature group create and edit forms, which ask before a change deletes online rows ([TTL][docs-ttl]).
- [FRONTEND] Added an execution graph of the dbt models and tests to the executions of jobs on `dbt-pipeline` environments whose run writes one.
- [FRONTEND] Changed the SQL Runner of the Query Engine page to fill the page, show row numbers and column types in the results, list a table's columns in the Explorer and draw `EXPLAIN (FORMAT GRAPHVIZ)` plans as a graph ([SQL Runner][docs-sql-runner]) (also in [5.1.2][hopsworks-5-1-2]).
- [FRONTEND] Changed the Set up data source dialog to list each SQL engine and CRM vendor as its own choice, with a filter box.
- [FRONTEND] Changed the Snowflake data source form to label its password option and field for a programmatic access token (PAT).
- [FRONTEND] Added suggestions of each connector's properties to the properties editor of the Trino catalog form.
- [FRONTEND] Changed the coding agent instruction files in members' home directories, such as `AGENTS.md`, to be updated on upgrade unless the member edited them.
- [FRONTEND] Fixed queued service operations failing on every retry when they removed a user from Superset or set up a project Observer's online feature store connection in Superset, and stopping for good after 68 failed attempts; a failing operation now retries once a day (also in [5.1.2][hopsworks-5-1-2]).
- [FRONTEND] Fixed a Jupyter server that had just started failing requests on clusters with more than one Hopsworks instance.
- [FRONTEND] Fixed Spark Connect in web terminals never starting on clusters that enforce the Kyverno restricted policies.
- [FRONTEND] Fixed the SQL Runner leaving a query running when you leave it right after starting the query, and its autocompletion offering no column names in `WHERE`, `GROUP BY` or join conditions (also in [5.1.2][hopsworks-5-1-2]).
- [FRONTEND] Fixed the **Why?** button of an online ingestion in a feature group's activity opening every OnlineFS log of the project instead of that ingestion's; it is now named **Logs** (also in [5.1.1][hopsworks-5-1-1]).
- [FRONTEND] Fixed the table preview of a PostgreSQL data source failing for a role granted only some columns.
- [FRONTEND] Fixed the dialogs and drawers of Git repository actions in the project settings closing on their own, and the Git Status drawer never opening.
- [FRONTEND] Fixed transformation function previews showing the imports of the defining module instead of only the function.
- [FRONTEND] Fixed Codex agent jobs failing before they reached the model.
- [FRONTEND] Fixed the dialog that `hops setup` opens in the browser leaving a user without projects stuck; it can now create a project.
- [HELM] Changed Trino to read its users, groups, user catalogs and access rules from HopsFS instead of Secrets, which fixes `helm upgrade` failing on clusters with many Trino catalogs or project members.
- [HELM] Fixed OpenSearch losing unflushed vectors and rejecting vector writes for about two minutes on its first start on 5.1 (also in [5.1.1][hopsworks-5-1-1]).
  A values file that sets `olk.opensearch.knn.circuit_breaker.triggered: true`, or an upgrade with `--reuse-values`, keeps the problem.
- [HELM] Fixed RonDB daemons ignoring SIGTERM, so every pod stop ended in a kill and a stopped data node could stall the cluster (also in [5.1.1][hopsworks-5-1-1]).
- [HELM] Added the HopsFS CSI driver, on by default (`global._hopsworks.csi.enabled`), which mounts HopsFS without a privileged container into the pods of Jupyter, web terminals, Git commands, Python, Ray, agent and DLT jobs, Python apps, Python deployments, Airflow and Trino; Trino needs it ([values][values-hopsfs-csi]).
- [HELM] Added support for Kubernetes 1.37; upgrade Hopsworks to 5.2 before the cluster, because 5.1 doesn't install on 1.37.
  Under ArgoCD 3.4 or older with server-side apply, upgrade ArgoCD to 3.5 or ignore `spec.preventPodSchedulingIfMissing` on CSIDrivers before moving to 1.37, or ArgoCD stops syncing ([Kubernetes 1.37][docs-upgrade-k8s-137]).
- [HELM] Added backups and restores of the Superset database, on by default with the cluster backups ([disaster recovery][docs-superset-backup]).
- [HELM] Changed the RonDB REST server probes to outlast a data node failure and to use their own port (also in [5.1.1][hopsworks-5-1-1]).
- [HELM] Fixed the Hopsworks admin pod starting before the database migrations had finished.
- [HELM] Fixed the RonDB REST server reading request bodies over 64 KiB as empty; it now buffers them in `rondb.rondb.rdrs.uploadPath` (also in [5.1.1][hopsworks-5-1-1]).
- [HELM] Fixed Helm 4 server-side apply conflicts on `helm upgrade` over the replicas of HPA-managed workloads other than the RonDB REST server, the rules of the Knative serving webhooks and the `rss-configuration` ConfigMap ([Upgrading with Helm 4][docs-helm4]).
- [HELM] Fixed environment builds never starting when `rondb.rondb.priorityClass` is renamed (also in [5.1.1][hopsworks-5-1-1]).
- [HELM] Fixed the Hive Metastore `metastore-db-init` Job failing on a fresh install when it started before the HopsFS NameNode.
- Addressed vulnerabilities in the Airflow, HopsFS, Hive Metastore, Trino, Spark history server and Ray images, and in the Hopsworks server dependencies.
- Addressed vulnerabilities in the Payara, Hopsworks certificate authority, Grafana, Filebeat and Superset images, and in the MySQL and Redis of Superset (also in [5.1.2][hopsworks-5-1-2]).

### Breaking changes

- [API] [FRONTEND] Because of a security fix, Data Scientists ask the creator of a job or a Data Owner of the project to change it, other than its schedule (also in [5.1.1][hopsworks-5-1-1]).
- [API] `get_batch_data` and the training data methods of `FeatureView` in the Python client now raise `TypeError` on a keyword argument they don't take, which they used to ignore; remove such arguments.
- [API] With `allow_missing=True`, `get_feature_vector` and `get_feature_vectors` in the Python client now return a serving key you pass in its slot of the vector when no row matches it, instead of `None`; code that detects a missing row by a `None` key must check the other features instead.
- [API] `Deployment.read_logs` and `tail_logs` in the Python client, `hops deployment logs` and `hops agent logs` now read only the live pods of a deployment and ignore `until`, where 5.1 read the logs of stopped deployments from OpenSearch by default; get those with `Deployment.download_logs` or `--download`.
- [API] Setting `Deployment.environment` in the Python client on a deployment you read back now moves only the predictor, where it used to move the transformer too; set `transformer.environment` as well.
- [API] `hops search ls` is now `hops search`, which also finds jobs, apps, models, deployments and agents; update scripts that call `hops search ls`.
- [API] [FRONTEND] MongoDB data sources need MongoDB 4.2 or later instead of 3.6; upgrade older MongoDB servers, or browsing and testing their data sources fails.
- [API] [FRONTEND] Adding more than 20 members to a project in one request is now refused, which 5.1 accepted; add them in batches of at most 20.
- [API] [HELM] Statements that administrators run through the admin Trino REST API (`admin/trino/v1/statement`) can no longer read the tables of projects, because the Trino administrator reads only the `system`, `tpch` and `tpcds` catalogs; query a project's tables from the SQL Runner of its Query Engine page as a member of the project.
- [FRONTEND] [HELM] Recorded Trino queries now lose their query text, plan and JSON details after `hopsworks.variables.trino_events_strip_details_after_days` (`7`), instead of keeping them until the query is deleted after 61 days, and the first nightly cleanup after the upgrade strips every older one; set it to `61` or more to keep them (also in [5.1.2][hopsworks-5-1-2]).
- [FRONTEND] [HELM] The chart no longer enables Trino's MySQL event listener, which crash-looped the Trino coordinator after a RonDB MySQL server restart, so the admin [Trino query history][docs-trino-history] records no new queries; to keep it, add the listener as [Trino query history][docs-upgrade-trino-history] shows (also in [5.1.2][hopsworks-5-1-2]).
- [FRONTEND] [HELM] Web terminal sessions now last 8 hours instead of 4, and every upgrade sets `terminal_session_hours` from `hopsworks.terminal.sessionHours`, replacing a value set in the admin UI, which upgrades used to keep; to keep another length, set it in `hopsworks.terminal.sessionHours`.
- [HELM] Upgrade 5.1 clusters to [5.2.2][hopsworks-5-2-2] instead of 5.2.0, whose OpenSearch index pass refuses every client, fails on an index with an empty mapping and doesn't check for nmslib vector fields, and whose index pass and OpenSearch restarts delete the roles behind restricted-access grants and feature group shares; 5.2.0 also lacks the OpenSearch vulnerability fix and the opt-in index copy Job of [5.1.2][hopsworks-5-1-2] ([upgrading OpenSearch][docs-os]).
  5.2.1 fixes these, but like 5.2.0 it loses Airflow tables, such as variables and XComs, in the upgrade from 5.1.
- [HELM] The upgrade migrates Kafka from ZooKeeper to KRaft, which can't be undone: give `helm upgrade` a long enough `--timeout`, never pass `--atomic` (`--rollback-on-failure` in Helm 4) or run `helm rollback`, and under ArgoCD invalidate its cluster cache, hard-refresh and sync again by hand ([Kafka 4 and KRaft][docs-kafka4-expect], [under ArgoCD][docs-kafka4-argocd]).
- [HELM] Upgrade to 5.2 only from 5.1, satellites before central, with central and its satellites all under Helm or all under ArgoCD ([satellite clusters][docs-os-satellites], [Strimzi CRDs][docs-kafka4-strimzi-crds]).
- [HELM] On a cluster installed before 5.1, OpenSearch refuses every client while the upgrade copies its oldest indices; plan the outage and the timeout ([upgrading OpenSearch][docs-os]).
- [HELM] On a 5.1 cluster with many feature statistics, each statement of schema migration V109 of 5.2.0 and 5.2.1 waits up to an hour for a statistics cleaner query of the running 5.1 pods, which 5.2.2 avoids; if it waits, scale `hopsworks-instance` to 0 and kill that query as [Migration V109][docs-upgrade-v109] shows.
- [HELM] OpenSearch snapshot repositories you configure yourself under `olk.opensearch.backup.repositories` or `olk.opensearch.restore.repositories`, on MinIO before `RELEASE.2025-01-20T14-49-07Z` or other S3-compatible stores that require `Content-MD5`, which OpenSearch 2.19 sent and 3.8 doesn't, need `legacy_md5_checksum_calculation: true` in their `s3` block, or the upgrade fails; the chart already sets it on the repositories it generates for the bundled MinIO ([snapshot repositories][docs-os-s3-md5]).
- [HELM] The chart now creates a cluster-wide IngressClass named `istio`, which 5.1 didn't; if the cluster already has one, set `kserve.istio.ingressClass.enabled: false`, or the upgrade fails.
- [HELM] KEDA, installed by default where 5.1 didn't install it, can't share a Kubernetes cluster with another KEDA or the OpenShift Custom Metrics Autoscaler, including the KEDA of another Hopsworks release such as a satellite; set `hopsworks.variables.kube_keda_installed: false` on all but one ([KEDA][docs-upgrade-keda]).
- [HELM] The post-upgrade search index rebuild signs in as the agent user, instead of with `hopsworks.variables.admin_email` and `admin_password`, and fails the `helm upgrade` if `hopsworks.agent_email` and `hopsworks.agent_password` (default `agent@hops.io`, `admin`) don't match that account (also in [5.1.1][hopsworks-5-1-1]).
  Set them, or turn the rebuild off with `hopsworks.opensearchReindex.enabled: false`.
- [HELM] With Helm 4, pass `--skip-crds` to a `helm install` on a cluster that already has the Strimzi CRDs, and after a reinstall run `helm upgrade` once to recreate the KEDA CRDs ([Strimzi CRDs][docs-kafka4-strimzi-crds], [KEDA CRDs][docs-keda-crds]).
- [HELM] If your values restate `trino.trino.additionalConfigProperties` with its `event-listener.config-files` entry, which the 5.1.1 chart set by default, remove that entry or add the listener files as [Trino query history][docs-upgrade-trino-history] shows, or Trino doesn't start (also in [5.1.2][hopsworks-5-1-2]).
- [HELM] Overrides of the Trino `initContainers`, `additionalVolumes` or `additionalVolumeMounts`, including those [5.1.0][hopsworks-5-1-0] asked for with `hopsworks.hopsfsMount.enabled: false`, fail the render; remove the overrides, or copy the new entries from the chart into them.
- [HELM] Under ArgoCD with `trino.auth.createSecrets` on (the default), set `trino.auth.adminUserPwd` and `trino.auth.monitoringUserPwd` to the passwords of your 5.1 release, which now default to empty instead of fixed passwords, or the chart fails to render; a `helm upgrade` outside ArgoCD reuses the existing Secrets whatever `global._hopsworks.mode` is.
- [HELM] If you set `trino.trino.serviceAccount.name`, set `trino.trinotest.serviceAccount.name` to the same name, because the test coordinator now shares the Trino account instead of creating its own `hopsworks-trino-test`, or the chart fails to render.
- [HELM] If your values override `trino.trino.accessControl.rules`, merge the rules of the 5.2 chart into your copy, because the backend now builds the Trino access rules from that value and the 5.1 rules leave out the private (`_<user>__*`) catalogs and give the `admin` group every catalog.
- [HELM] If you override `trino.trino.image.tag`, use a Hopsworks Trino image of `483-v2` or later instead of the `480` images of 5.1, and set `global._hopsworks.trino.image.tag` to the same tag.
- [HELM] With cluster backups on, Superset backups, new in 5.2, need an object store and, with `superset.auth.createSecrets: false`, the `backup.hops.works/include=true` label on its Secrets, or the chart fails to render; set `superset.backups.enabled: false` to skip them ([disaster recovery][docs-superset-backup]).
- [HELM] Removed the KServe local model controller; if you set `kserve.kserve.localmodel.enabled: true`, remove it, or the chart fails to render.
- [HELM] If your release namespace is longer than 34 characters, set `global._hopsworks.csi.driverName`, because the default name of the HopsFS CSI driver, new in 5.2, would exceed 63 characters ([driver name][docs-csi-driver-name]).
- [HELM] On OpenShift, use the `values.openshift.yaml` of the 5.2 chart, which creates an SCC for the privileged HopsFS CSI node plugin, new in 5.2; if a cluster administrator owns SCCs, see [when the cluster administrators own the SCC][docs-csi-admin-scc].
- [HELM] Project namespaces now get a NetworkPolicy that admits traffic only from the same namespace and the Hopsworks namespace, where 5.1 restricted only web terminal pods; add any other namespace that reaches project pods, such as Istio or monitoring, to `hopsworks.variables.project_namespace_network_policy_allowed_namespaces` ([values][values-netpol]).
  Turning them off with `hopsworks.variables.project_namespace_network_policy_enabled: false` leaves the existing ones; delete them with `kubectl delete networkpolicy -A --field-selector metadata.name=hopsworks-project-isolation`.
- [HELM] With `hopsworks.rbac.useExistingRole: true`, add the chart's new ClusterRole grants (`charts/hopsworks/templates/role.yaml`) on `scaledobjects`, `interceptorroutes`, `ingresses`, `networkpolicies` and `csidrivers`, or model deployments, project creation and every pod that mounts HopsFS fail.
- [HELM] The RonDB REST server now uses a probe port and an upload path that need RonDB 26.02.11, where 5.1.0 probed its REST port and set no upload path (also in [5.1.1][hopsworks-5-1-1]).
  If you pin `rondb.rondb.images.rondb.tag` to an older version, set `rondb.rondb.rdrs.probePort.enabled: false` and `rondb.rondb.rdrs.uploadPath: ""`, or the REST server doesn't start.
- [HELM] Kafka 4.3 rejects clients older than Apache Kafka 2.1 or librdkafka 1.8.2, which the Kafka 3.9 of 5.1 accepted; upgrade them first; with your own Kafka cluster, its brokers must run Kafka 2.1 or later ([client compatibility][docs-kafka4-clients]).
- [HELM] OpenSearch now reports its own version, `3.8.0`, instead of `7.10.2`; check clients that connect to it directly against the [OpenSearch 3.0 breaking changes](https://docs.opensearch.org/latest/breaking-changes/).

### Deprecations

- [API] Deprecated `entry` of `get_feature_vector`, `get_feature_vectors`, `get_inference_helper` and `get_inference_helpers` in the Python client; use `serving_keys`.
- [API] Deprecated `Deployment.environment` in the Python client; use `predictor.environment` and `transformer.environment`.
- [API] Deprecated `source="opensearch"` of `Deployment.read_logs` and `tail_logs` in the Python client and `--source opensearch` of `hops deployment logs` and `hops agent logs`, whose default is now `kubernetes` instead of `opensearch`.
- [API] Deprecated spine groups (`get_or_create_spine_group`) and the `spine` argument of `FeatureView` reads in the Python client; use `spine_df`.
- [API] Deprecated `ModelSchema` in the Python client; a model created with `create_model(feature_view=...)` takes its schema from the feature view, and a deployment describes its requests with the [deployment schema][docs-deployment-schema].
- [API] Deprecated `hops init`; use `hops skills install`.
- [API] Deprecated the `environmentDTO` field of model deployments in the REST API; use `predictorEnvironment` and `transformerEnvironment`.
- [HELM] Deprecated the name of `kafka.cluster.zookeeper`, which now sizes and places the KRaft controllers; its `services.client.annotations` is no longer read.
- [HELM] Deprecated `hopsworks.variables.mount_hopsfs_in_python_job`, which only legacy Python jobs still read.
- [HELM] Deprecated `global._hopsworks.trino.mountableSecrets.mechanism`, `global._hopsworks.trino.userCatalogShards`, `trino.auth.adminUserPwdHash`, `trino.auth.monitoringUserPwdHash` and `hw-kyverno.policyExceptions.trino`, which nothing reads any more.

### Upgrade steps

Follow [Before every upgrade][docs-upgrade-before] and [5.1.x to 5.2.x][docs-upgrade-51-to-52] in the upgrade guide.

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

- [HELM] Changed the default of `olk.opensearch.knn.circuit_breaker.triggered` from `true` to `false` and of `olk.opensearch.knn.circuit_breaker.percent` from `0.75` to `75` (also in [5.1.1][hopsworks-5-1-1]).
- [HELM] Changed the default of `hopsworks.variables.docker_operations_buildkit_priority_class` from `rondb-high-priority` to empty, so environment builds run at the default priority (also in [5.1.1][hopsworks-5-1-1]).
- [HELM] Changed `rondb.rondb.terminationGracePeriodSeconds` to one value per component, and the data nodes' default from 60 to 300 seconds; an integer still sets only the data nodes (also in [5.1.1][hopsworks-5-1-1]).
- [HELM] Removed the MySQL event listener from the default `trino.trino.additionalConfigProperties` and from `trino.trino.coordinator.additionalConfigFiles` and `trino.trino.worker.additionalConfigFiles` (also in [5.1.2][hopsworks-5-1-2]).
- [HELM] Changed the default of `hopsworks.variables.trino_events_cleaner_batch_size` from 1000 to 100 (also in [5.1.2][hopsworks-5-1-2]).
- [HELM] Changed `hopsworks.variables.trino_default_catalog` from `hive` to `delta`, the catalog new Superset connections to Trino open in.
- [HELM] Changed the default driver memory of new Ray jobs (`hopsworks.variables.ray_job_driver_memory`) from 2048 to 4096 MB.
- [HELM] Added `kserve.servingTerminationGracePeriodSeconds` (default `120`), the termination grace period the model serving webhook sets on model deployment pods, which 5.1 set to 3 seconds.
- [HELM] Changed `trino.trinotest.serviceAccount.create` to `false` and `name` to `hopsworks-trino`, so the test coordinator shares the Trino account.
- [HELM] Changed the defaults of `trino.auth.adminUserPwd` and `trino.auth.monitoringUserPwd` to empty, so the chart generates the passwords.
- [HELM] Changed `values.openshift.yaml` to turn on credential files for Trino catalogs (`global._hopsworks.trino.mountableSecrets.enabled`).
- [HELM] Changed `values.airgap.yaml` to pull the HopsFS CSI driver and KEDA images from the mirror registry.
- [HELM] Fixed `values.openshift.yaml` for the OpenShift `restricted-v2` SCC, covering Strimzi, the Kafka brokers and KRaft controllers, the Spark operator and the MySQL and Redis of Superset, and turned off the Prometheus node exporter, which OpenShift ships itself (also in [5.1.1][hopsworks-5-1-1]).
  Use it with Helm 4 or Helm 3.17.1 or later, because older Helm 3 releases ignore its `null` overrides of subchart values.
- [HELM] Fixed `global._hopsworks.jobs.ttlSecondsAfterFinished: 0` being replaced by `86400`.
- [HELM] Fixed Helm 4 rejecting an empty `kafka.cluster.kafka.authorizer.authorizerClass`.
- [HELM] Fixed the values schema rejecting `hopsworks.variables.loadbalancer_external_domain_namenode` and `hopsworks.variables.loadbalancer_external_domain_datanode` (also in [5.1.1][hopsworks-5-1-1]).
- [HELM] Added `hopsworks.opensearchReindex.enabled` to turn off the post-upgrade search index rebuild, and `hopsworks.variables.command_search_fs_reindex_queue_wait_as_ms` to bound its wait for the search command queue (also in [5.1.1][hopsworks-5-1-1]).
- [HELM] Added `hopsworks.variables.trino_events_strip_details_after_days` (default `7`), the days after which a recorded Trino query loses its text, plan and JSON details (also in [5.1.2][hopsworks-5-1-2]).
- [HELM] Added `olk.opensearch.indexUpgrade.enabled` and `activeDeadlineSeconds` (3600) for the pre-upgrade OpenSearch index pass ([set the timeout][docs-os-timeout]).
- [HELM] Added `kafka.migrationJob` and `kafka.crdUpgradeJob` for the hooks that migrate Kafka to KRaft and convert the Strimzi CRDs; `kafka.migrationJob.timeoutSeconds` (1800) bounds each of the migration's three waits ([Kafka 4 and KRaft][docs-kafka4-expect]).
- [HELM] Added `kafka.cluster.kafka.config.replicationFactor` and `minInsyncReplicas` for multi-broker Kafka; `minInsyncReplicas` above a topic's replicas makes `acks=all` writes to it fail ([values][values-kafka]).
- [HELM] Added `nodePort` values to pin the node ports of unmanaged external load balancers: ArrowFlight, OpenSearch, the HopsFS NameNode and DataNodes, Trino, the Hive Metastore, Kafka (`bootstrapNodePort`, `startingNodePort`) and the RonDB MySQL and REST servers (also in [5.1.1][hopsworks-5-1-1]).
  The RonDB ones ignore `global._hopsworks.externalLoadBalancers.managed` and apply only when `rondb.rondb.meta.mysqld.externalLoadBalancer.managed` or `rondb.rondb.meta.rdrs.externalLoadBalancer.managed` is `false`.
- [HELM] Added `rondb.rondb.rdrs.probes` and `rondb.rondb.rdrs.probePort`, the settings and the port of the RonDB REST server probes, and `rondb.rondb.rdrs.maxKeepaliveRequests` to close a keep-alive connection after that many requests, so clients rebalance after a rolling restart (also in [5.1.1][hopsworks-5-1-1]).
- [HELM] Added `rondb.rondb.rdrs.ttlPurge.enable` and `activeWindow` to turn off the TTL purge of the RonDB REST server or limit it to a daily window (also in [5.1.1][hopsworks-5-1-1]).
- [HELM] Added `kserve.kserve.storage.resources` for the storage initializer that downloads models into deployment pods.
- [HELM] Added `kserve.istio.ingressClass.enabled` and `kserve.istio.ingressClass.name` for the cluster-wide IngressClass the chart creates.
- [HELM] Added `hopsworks.variables.kube_keda_installed` (default `true`), which installs KEDA and lets model deployments autoscale through it.
- [HELM] Added `hopsworks.variables.project_namespace_network_policy_enabled` (default `true`) and `project_namespace_network_policy_allowed_namespaces` for the NetworkPolicy of project namespaces.
- [HELM] Added `superset.backups.enabled` (default `true`) for the Superset backups.
- [HELM] Added `global._hopsworks.csi.driverName` to name the HopsFS CSI driver of a release.
- [HELM] Added `global._hopsworks.trino.image.tag` (default `483-v2`), which has to match `trino.trino.image.tag`.
- [HELM] Added `hopsworks.terminal.sessionHours` (default `8`), which every upgrade writes to the web terminal session length.

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
[docs-agent-skills]: https://docs.hopsworks.ai/5.2/user_guides/client_installation/#skills-and-instructions-for-coding-agents
[docs-api-scopes]: https://docs.hopsworks.ai/5.2/user_guides/projects/api_key/api_key_scopes/
[docs-ttl]: https://docs.hopsworks.ai/5.2/user_guides/fs/feature_group/ttl/
[docs-member-files]: https://docs.hopsworks.ai/5.2/user_guides/projects/project/manage_members/#what-happens-to-a-removed-members-files
[docs-fs-sharing]: https://docs.hopsworks.ai/5.2/user_guides/fs/sharing/sharing/
[docs-serving-logs]: https://docs.hopsworks.ai/5.2/user_guides/mlops/serving/troubleshooting/#configuring-disk-logging
[docs-feature-logging]: https://docs.hopsworks.ai/5.2/user_guides/fs/feature_view/feature_logging/#choosing-the-transport
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
[values-python-app-envoy]: https://docs.hopsworks.ai/5.2/setup_installation/common/helm_chart_values/hopsworks/#helm.hopsworks.variables.python_app_envoy_image_version
[values-netpol]: https://docs.hopsworks.ai/5.2/setup_installation/common/helm_chart_values/hopsworks/#helm.hopsworks.variables.project_namespace_network_policy_enabled
[docs-os]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade_opensearch/
[docs-upgrade-before]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade/#upgrade-before-every-upgrade
[docs-upgrade-51-to-52]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade/#upgrade-51-to-52
[docs-upgrade-changes-from-522]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade/#upgrade-changes-from-522
[docs-upgrade-changes-from-523]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade/#upgrade-changes-from-523
[docs-upgrade-python-app-envoy]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade/#upgrade-python-app-envoy
[docs-upgrade-v109]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade/#upgrade-v109-statistics-cleaner
[docs-upgrade-onlinefs]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade/#upgrade-onlinefs-topics
[docs-upgrade-ddl]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade/#upgrade-ddl-sql-node
[docs-upgrade-otlp]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade/#upgrade-agent-otlp-sidecar
[docs-upgrade-kueue-external]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade/#upgrade-kueue-external
[docs-upgrade]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade/
[docs-helm4]: https://docs.hopsworks.ai/5.2/setup_installation/admin/helm4/
[docs-kueue-what-changes]: https://docs.hopsworks.ai/5.2/setup_installation/admin/kueue_external/#what-changes
[docs-run-ai]: https://docs.hopsworks.ai/5.2/setup_installation/admin/run_ai/
[docs-keda-crds]: https://docs.hopsworks.ai/5.2/setup_installation/admin/keda/#keda-crds
[docs-os-restore-crash-loop]: https://docs.hopsworks.ai/5.2/setup_installation/admin/ha-dr/dr/#opensearch-restore-crash-loop
[docs-os-security]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade_opensearch/#opensearch-security-configuration
[docs-node-pools]: https://docs.hopsworks.ai/5.2/setup_installation/admin/node_pools/
[docs-buildkitd-rhel8]: https://docs.hopsworks.ai/5.2/setup_installation/admin/build_performance/#buildkitd-rhel8
[docs-sharepoint]: https://docs.hopsworks.ai/5.2/user_guides/fs/data_source/creation/sharepoint/
[docs-sharepoint-client]: https://docs.hopsworks.ai/5.2/user_guides/fs/data_source/creation/sharepoint/#client-version
[docs-ds-hopsworks]: https://docs.hopsworks.ai/5.2/user_guides/fs/data_source/creation/hopsworks/
[docs-ds-sqlserver]: https://docs.hopsworks.ai/5.2/user_guides/fs/data_source/creation/sql/#sql-server-specific-notes
[docs-apps-public]: https://docs.hopsworks.ai/5.2/user_guides/projects/apps/#public-access-for-streamlit-apps
[docs-setup-aws]: https://docs.hopsworks.ai/5.2/setup_installation/aws/getting_started/
[docs-setup-azure]: https://docs.hopsworks.ai/5.2/setup_installation/azure/getting_started/
[docs-setup-gcp]: https://docs.hopsworks.ai/5.2/setup_installation/gcp/getting_started/
[docs-sql-runner]: https://docs.hopsworks.ai/5.2/user_guides/projects/trino/query_engine/#sql-runner
[docs-upgrade-k8s-137]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade/#upgrade-kubernetes-137
[docs-trino-history]: https://docs.hopsworks.ai/5.2/setup_installation/admin/trino/#query-history
[docs-upgrade-trino-history]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade/#upgrade-trino-query-history
[docs-upgrade-keda]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade/#upgrade-keda
[docs-os-satellites]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade_opensearch/#opensearch-satellite-clusters
[docs-os-s3-md5]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade_opensearch/#snapshot-repositories-on-s3-compatible-stores
[docs-kafka4-strimzi-crds]: https://docs.hopsworks.ai/5.2/setup_installation/admin/kafka4/#kafka4-strimzi-crds
[docs-kafka4-argocd]: https://docs.hopsworks.ai/5.2/setup_installation/admin/kafka4/#kafka4-argocd
[docs-csi-driver-name]: https://docs.hopsworks.ai/5.2/setup_installation/admin/hopsfs_csi/#hopsfs-csi-driver-name
[docs-csi-admin-scc]: https://docs.hopsworks.ai/5.2/setup_installation/admin/hopsfs_csi/#hopsfs-csi-admin-scc
