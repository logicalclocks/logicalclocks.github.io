---
releases:
  "5.0.14":
    released: "2026-10-16"
    python_client: "5.0.10"
  "5.0.13":
    released: "2026-09-28"
    python_client: "5.0.9"
  "5.0.12":
    released: "2026-09-21"
    python_client: "5.0.9"
  "5.0.11":
    released: "2026-09-16"
    python_client: "5.0.7"
  "5.0.10":
    released: "2026-09-11"
    python_client: "5.0.7"
  "5.0.9":
    released: "2026-08-28"
    python_client: "5.0.6"
  "5.0.8":
    released: "2026-08-21"
    python_client: "5.0.5"
  "5.0.6":
    released: "2026-07-29"
    python_client: "5.0.3"
  "5.0.5":
    released: "2026-07-22"
    python_client: "5.0.3"
  "5.0.4":
    released: "2026-07-17"
    python_client: "5.0.3"
  "5.0.3":
    released: "2026-07-14"
    python_client: "5.0.3"
  "5.0.2":
    released: "2026-07-10"
    python_client: "5.0.3"
  "5.0.1":
    released: "2026-07-03"
    python_client: "5.0.1"
  "5.0.0":
    released: "2026-06-11"
    python_client: "5.0.0"
    since: "4.8.2"
---

# Release notes { #hopsworks-5-0 }

The releases of Hopsworks 5.0, newest first.

## 5.0.14 { #hopsworks-5-0-14 }

### What's changed

- Fixed a security issue in jobs.
- Fixed HopsFS staying in safe mode after all NameNodes restarted, a NameNode restart occasionally marking every block as corrupt, and NameNodes running out of file descriptors when many blocks are corrupt.
- Fixed RonDB daemons ignoring SIGTERM, so every pod stop ended in a kill and a stopped data node could stall the cluster.
- Fixed security vulnerabilities in the Payara, Hopsworks, Hopsworks CA, Hive Metastore, remote shuffle service, Spark operator, Filebeat, Logstash, Grafana, OpenSearch Dashboards and Superset images, in the MySQL and Redis of Superset, and in the Hopsworks server dependencies.
- Changed the RonDB REST server probes to use their own port, which keeps answering while a stalled data node blocks requests.
- Fixed the RonDB REST server reading request bodies over 64 KiB as empty.
- Added key pair authentication to DLT ingestion from Snowflake, which accounts that enforce MFA need ([Snowflake data source](https://docs.hopsworks.ai/5.0/user_guides/fs/data_source/creation/snowflake/)).
- Changed reads of a feature view whose feature groups all come from one Snowflake data source to run the whole query, point-in-time joins included, in Snowflake instead of reading each feature group in full.
- Added a **Stop** button to the SQL Runner, and leaving the SQL Runner now stops the running query; the run status shows the elapsed time and the rows the query engine processed.
- Changed the SQL Runner layout: the results fill the panel with row numbers and column types, the Explorer lists a table's columns, autocomplete completes the statement at the cursor, `EXPLAIN` plans render as JSON or a graph, and long plans and table definitions scroll instead of overflowing.
- Fixed Trino giving a project access to only one of several feature stores shared with it.
- Fixed reads of external feature groups failing on chained point-in-time joins, on joins with a prefix or extra primary keys, and after features were appended to the feature group.
- Fixed Snowflake reads through the Hopsworks Query Service, such as Python engine reads, using the Snowflake user's default role instead of the role set on the data source.
- Fixed queued project and member operations, such as Superset access changes, failing for good after 68 attempts, for project Observers, or when removing a member's Superset user; a failing operation now retries once a day.
- Fixed Git operations failing with an I/O error when a Git provider proxy is set on a cluster with HopsFS encryption at rest.
- Fixed a killed Spark job with pending executors staying in the aggregating logs state for up to 20 minutes.
- Fixed DLT ingestion rejecting a load whose decimal values are narrower than the precision of the source column.
- Fixed dialogs, drawers and menus opened from a table row closing by themselves on the Git, model deployment, alert receiver and feature monitoring pages, and the Git Status drawer never opening.

### Breaking changes

- The chart no longer turns on Trino's MySQL event listener, which crash-looped the Trino coordinator after a MySQL server restart, so the [Trino query history](https://docs.hopsworks.ai/5.0/setup_installation/admin/trino/#query-history) stops recording queries.
  To keep it, add the listener to your values as the chart's `README.md` shows; recorded queries now lose their text and plan after `hopsworks.variables.trino_events_strip_details_after_days`, from the first nightly cleanup, so set it to `61` or more to keep them.
- The RonDB REST server now uses a probe port and an upload path that need RonDB 26.02.11, instead of probing its REST port with no upload path.
  If you pin `rondb.rondb.images.rondb.tag` to an older version, set `rondb.rondb.rdrs.probePort.enabled: false` and `rondb.rondb.rdrs.uploadPath: ""`, or the REST server doesn't start.

### Upgraded components

| Component | 5.0.13 | 5.0.14 |
| --------- | ------ | ------ |
| Base environment images | 5.0.10 | 5.0.11 |
| Filebeat | 8.19.20 | 8.19.23 |
| Git image | 1.4.4 | 1.4.5 |
| Grafana | 10.2.2-h7 | 10.2.2-h7.1 |
| Hive Metastore | 3.0.0.14.7-v1 | 3.0.0.14.7-v2 |
| HopsFS | 3.4.3.1-EE-RC5 | 3.4.3.1-EE-RC6 |
| Logstash | 7.17.9.5 | 7.17.9.6 |
| OpenSearch Dashboards | 1.3.6.7 | 1.3.6.8 |
| Payara | 6.2024.12-jdk17.8 | 6.2024.12-jdk17.8.1 |
| Remote shuffle service (Apache Uniffle) | 0.10.8.1 | 0.10.8.2 |
| RonDB | 26.02.10 | 26.02.11 |
| Spark operator | 2.2.1-h4 | 2.2.1-h6 |
| Superset | 6.0.0p3.4 | 6.0.0p3.5 |
| Superset init image | dockerize | 0.14.0-alpine-h1.1 |
| Superset MySQL | 8.4.5-debian-12-r0-h3 (MySQL 8.4.11) | 8.4.11-ubuntu24.04-h5 |
| Superset MySQL metrics exporter | 0.17.2-debian-12-r7 | 0.20.0-alpine-h1.1 |
| Superset MySQL volume permissions image | 12-debian-12-r43 | 12-alpine-h1.1 |
| Superset Redis | 7.4.9-bookworm | 7.4.11-alpine-h2 |
| Superset Redis metrics exporter | 1.50.0-debian-11-r1 | 1.90.0-alpine-h1.1 |
| Trino | 480.1-v1 | 480.1-v2 |

### Configuration changes

- Changed `rondb.rondb.terminationGracePeriodSeconds` to one value per component, 300 seconds for `ndbmtds` instead of 60, and 30 for the others; a plain number still sets the data nodes only.
- Added `hopsworks.variables.trino_events_strip_details_after_days` (default `7`) and changed the default `hopsworks.variables.trino_events_cleaner_batch_size` to `100`.
- Changed the Superset init image to its own `superset/dockerize` repository, also in `values.airgap.yaml`; if you override `superset.superset.initImage.repository`, point it at a mirror of that image.
- Fixed `values.openshift.yaml` for the OpenShift `restricted-v2` SCC, covering Strimzi, Kafka, ZooKeeper, the Spark operator, Trino, Prometheus and the MySQL and Redis of Superset; it also turns off the Prometheus node exporter, which OpenShift ships itself.
  Use it with Helm 4 or Helm 3.17.1 or later, because older Helm 3 releases can ignore its `null` overrides of subchart values.
- Added `rondb.rondb.rdrs.probePort`, the port of the RonDB REST server probes, `rondb.rondb.rdrs.uploadPath`, where it buffers request bodies over 64 KiB, and `rondb.rondb.rdrs.maxKeepaliveRequests` to rebalance client connections after a rolling restart.
- Added `rondb.rondb.rdrs.ttlPurge.enable` and `activeWindow` to turn off the TTL purge of the RonDB REST server or limit it to a daily window.

## 5.0.13 { #hopsworks-5-0-13 }

### What's changed

- Fixed the Airflow migration Job losing tables on clusters with more than one RonDB MySQL server, so the upgrade never completed; it now uses only the DDL MySQL server.
  A cluster whose earlier upgrade already failed this way needs the Airflow schema dropped on every MySQL server before it upgrades again.
- Fixed OnlineFS upgrades stalling on a full node pool: with two or more `onlinefs.deployment.replicas`, a rollout now replaces one pod at a time.
- Changed the RonDB REST server probes to outlast a data node failure.
- Fixed offline reads of a feature view or query that includes a spine group failing with an HTTP 500 error.
- Fixed the OpenSearch metrics exporter reporting the parent cluster on a satellite deployment, and missing OpenSearch with a custom `global._hopsworks.consulDomainName`.

### Breaking changes

- The Airflow migration Job now waits for the DDL MySQL server, instead of any MySQL server, so the upgrade hangs with `rondb.rondb.meta.ddlMySQLd.enabled: false`.
  Keep it enabled if you use Airflow.
- Removed the Kafka quota defaults Job, which applied `kafka.cluster.kafka.quotas.defaults` to each client, so it is ignored with `type: strimzi`, and fails the render with `type: kafka` when `enabled` is `true`.
  If you set it, move your limits to `kafka.cluster.kafka.quotas.strimzi` or `kafka.cluster.kafka.quotas.kafka`, with new numbers: the `strimzi` rates are a total per broker, shared by all clients.
- `quotas` on a user in `kafka.users` now fail the render under the default `strimzi` plugin, which never enforced them.
  Remove them, or set `kafka.cluster.kafka.quotas.type: kafka`, `kafka.cluster.kafka.quotas.minAvailableRatioPerVolume: 0` and `kafka.cluster.kafka.authorizer.principalBuilderClass: ""` to enforce them.

### Deprecations

- Deprecated `kafka.cluster.kafka.quotas.defaults`, which is no longer honoured; see the breaking changes above.

### Configuration changes

- Added `kafka.cluster.kafka.quotas.type` to choose the Kafka quota plugin: `strimzi` (the default), set under `kafka.cluster.kafka.quotas.strimzi`, or `kafka`, which enforces per-user quotas from `kafka.users[].quotas` and defaults from `kafka.cluster.kafka.quotas.kafka`.
  `kafka` also needs `kafka.cluster.kafka.quotas.minAvailableRatioPerVolume: 0`, per-user quotas need `kafka.cluster.kafka.authorizer.principalBuilderClass: ""`, which changes how ACLs and `superUsers` match principals, and none of these settings take effect on clusters first installed on Hopsworks 4.3 or 4.5.
- Added `onlinefs.deployment.strategy` to set the rollout strategy of OnlineFS.
- Added `rondb.rondb.rdrs.probes` to configure the RonDB REST server probes.

## 5.0.12 { #hopsworks-5-0-12 }

### What's changed

- Changed the memory split of the remote shuffle servers to stop heap out-of-memory crashes: 20% of `spark.rss.shuffleServer.resources.limits.memory` is reserved for native memory and the rest is split 25% heap, 75% off-heap.
- Fixed the remote shuffle servers never receiving their off-heap memory setting, which left their buffers about nine times too small.
- Fixed service logs being dropped from the `.services` OpenSearch index when Kubernetes labels pushed it past 1000 fields.
- Added **Driver overhead factor** and **Executor overhead factor** to the Spark configuration of jobs, Jupyter and project defaults, which set `spark.driver.memoryOverheadFactor` and `spark.executor.memoryOverheadFactor` ([PySpark jobs](https://docs.hopsworks.ai/5.0/user_guides/projects/jobs/pyspark_job/)).
  Jupyter Spark sessions now default both to `0.4`, as PySpark jobs do, so notebooks and their executors request more memory than before.
- Added a **Monitor** button to each running Spark application on the Jupyter page, showing its driver and executor pods, and fixed the Jupyter server monitor showing a Spark executor as the notebook pod; the Grafana link there is now called **Metrics**.

### Breaking changes

- Removed `hopsworks.variables.jupyter_spark_driver_memory_overhead_factor`, added in 5.0.10; the driver memory overhead of a notebook now comes from its Spark configuration.
  Remove it from your values before you upgrade, because the values schema rejects it; with `--reuse-values`, which keeps the old default, use `--reset-then-reuse-values`.
- Filebeat now keeps only the Kubernetes labels listed under `olk.filebeat.kubernetesMetadata`, and the `serviceLabelKey` of each `olk.logstash.extendServicesPipeline` entry, on service logs, instead of every pod label.
  Add any other label you filter on to `olk.filebeat.kubernetesMetadata.extraPodLabels`, `extraNamespaceLabels` or `extraNodeLabels`; an overridden `olk.filebeat.logs_locations` keeps its own `add_kubernetes_metadata` processor and every label, so to get the fix set `addKubernetesMetadata: true` on each entry and drop that processor.

### Upgraded components

| Component | 5.0.11 | 5.0.12 |
| --------- | ------ | ------ |
| Base environment images | 5.0.9 | 5.0.10 |

### Configuration changes

- Changed the default `spark.rss.shuffleServer.bufferCapacityRatio` to `0.6` and `spark.rss.shuffleServer.resources.limits.cpu` to `2000m`.

## 5.0.11 { #hopsworks-5-0-11 }

### What's changed

- Fixed RonDB data nodes reporting ready while the management server is unreachable, which let a rollout stop the healthy data node of the same node group and shut the cluster down; their liveness probe also no longer kills them then.
- Fixed RonDB rolling restarts making healthy data nodes shut down; data nodes now wait for the rollout to settle (`rondb.rondb.ndbmtdSettleWait`).
- Fixed the RonDB MySQL setup and in-place restore Jobs failing for good when data nodes took more than about two hours to start, and the MySQL servers crash-looping while they wait for a backup restore.
- Changed the Kafka Entity Operator, when `kafka.cluster.entityOperator` is set, to follow the tolerations, topology spread and node affinity of the Kafka brokers, unless set under `kafka.cluster.entityOperator.template.pod`.

### Upgraded components

| Component | 5.0.10 | 5.0.11 |
| --------- | ------ | ------ |
| RonDB | 26.02.9 | 26.02.10 |

### Configuration changes

- Changed `rondb.rondb.timeoutsMinutes.ndbmtdStartupProbe` to 240 minutes, from 120, so data nodes that take over two hours to reload aren't restarted in a loop.
- Fixed users added to `rondb.rondb.mysql.users` after the install never being created, and users with privileges on a single database or table failing; every upgrade now creates the listed users.
- Added `rondb.rondb.mysql.users[].existingSecret` to read the password of a MySQL user from your own Secret.

## 5.0.10 { #hopsworks-5-0-10 }

### What's changed

- Fixed a security issue in project datasets.
- Fixed uploading files in the file browser deleting the files of the previous upload unless the page was reloaded.
- Fixed security vulnerabilities in the ArrowFlight and remote shuffle service images.
- Fixed init containers that wait for a RonDB rollout giving up after 30 minutes, which failed the Hive Metastore, HopsFS, Airflow migration and CA pods when a RonDB restart took longer.
- Added the GitHub Copilot and OpenCode CLIs to the web terminal, next to Claude Code and Codex; the coding agents share the skills in your home directory and keep their logins and sessions across terminal sessions.
- Added GitHub Copilot as a provider of agent tasks, signed in with the token of a GitHub AI provider or of your github.com Git provider, which can't be a classic personal access token.
- Added a Copilot tab and a Business Glossary for each coding agent to the Agents page of the cluster settings, now called Coding Agents.
- Added support for Git repositories behind a private CA or an HTTP proxy: set `hopsworks.variables.git_custom_ca_configmap` to a ConfigMap that exists in every project namespace, `git_<provider>_http_proxy` and `git_<provider>_https_proxy` for GitHub, GitLab and BitBucket, or `git_disable_tls_verification`.
- Fixed the Jupyter server of Spark environments running out of memory: it now adds an overhead (`hopsworks.variables.jupyter_spark_driver_memory_overhead_factor`) and a floor (`jupyter_spark_notebook_server_memory_floor_mb`) to the driver memory.
- Fixed Spark executors started from Jupyter having no CPU limit and rounding fractional executor cores up to a whole core; they now get the executor cores of the session as request and limit, as job executors do.
- Fixed Git operations failing to authenticate when a provider token or password contains special characters.
  The upgrade converts the saved credentials; if a provider still fails, save it again in your account settings.
- Fixed `kubectl` failing in every web terminal, because terminals never got a kubeconfig.
- Fixed writes to an online feature group failing after its table was truncated.
- Fixed the project home page crashing with "Something went wrong while loading this page" because of the Feature usage card.
- Added the status of the TTL purge of online feature groups: a TTL purge card on the feature group overview and a TTL Purge page in the cluster settings.
- Added a read-only `featurestore` directory to the web terminal with the files of the project's offline feature store.
- Added the `KafkaAuthenticationFailures` Prometheus alert for clients that keep failing to authenticate, for example with an expired certificate.
- Fixed creating or editing a BigQuery data source failing with a gRPC error when the form lists the GCP projects.
- Changed `GET /project/{id}/jupyter/running` to return `204 No Content` instead of `404` when no Jupyter server is running.
- Removed the Plans dialog from the web terminal.

### Breaking changes

- Removed the Code Style, Testing and Security rules from the Coding Agents page of the cluster settings, and web terminals no longer give them to the coding agents.
  If you set them, move what you need to the new Business Glossary or the system-wide instructions of each agent.

### Upgraded components

| Component | 5.0.9 | 5.0.10 |
| --------- | ----- | ------ |
| ArrowFlight server | 5.0.3 | 5.0.4 |
| Base environment images | 5.0.8 | 5.0.9 |
| Git image | 1.4.2 | 1.4.4 |
| OnlineFS | 2.3.4 | 2.3.5 |
| Remote shuffle service (Apache Uniffle) | 0.10.8 | 0.10.8.1 |

### Configuration changes

- Added `kafka.cluster.clusterCa.validityDays` and `kafka.cluster.clientsCa.validityDays` (default `365`) for the certificates Strimzi issues, applied at the next issuance.

## 5.0.9 { #hopsworks-5-0-9 }

### What's changed

- Fixed security vulnerabilities in the Hopsworks and Hopsworks CA images.
- Fixed init containers without requests and limits being charged a namespace `LimitRange` default for the whole life of the pod; the RonDB and Consul charts are not covered yet.
- Fixed Ray jobs and the Ray clusters of Jupyter failing to start on OpenShift, because their pods couldn't read the project certificates.
- Fixed web terminals failing to start on OpenShift.
- Fixed feature statistics failing to save when a column has a NaN or infinite statistic, such as the standard deviation of an all-null column.
- Fixed the state of a Spark or Ray job execution switching between queued and running while one of its pods couldn't be scheduled.
- Fixed the KServe local model controller image (`kserve.kserve.localmodel.enabled`) failing to pull.

### Breaking changes

- Init containers now set CPU and memory requests and limits, which most of them used to leave unset.
  If a namespace `LimitRange` has a `min` or `max` they don't fit, set `global._hopsworks.initContainerResources` before you upgrade, or Kubernetes rejects the pods.

### Upgraded components

| Component | 5.0.8 | 5.0.9 |
| --------- | ----- | ----- |
| ArrowFlight server | 5.0.2 | 5.0.3 |
| Base environment images | 5.0.5 | 5.0.8 |
| Git image | 1.4.1 | 1.4.2 |
| Hive Metastore | 3.0.0.14.6-v1 | 3.0.0.14.7-v1 |
| HopsFS | 3.4.3.1-EE-RC4 | 3.4.3.1-EE-RC5 |
| Model serving webhook | 5.0.2 | 5.0.3 |
| RonDB | 26.02.8 | 26.02.9 |
| Spark history server | 3.5.5.2 | 3.5.5.3 |
| Toolbox image (hwutils) | 1.7.1 | 1.7.2 |
| Trino | 480-v6 | 480.1-v1 |

### Configuration changes

- Changed `hopsworks.variables.docker_operations_timeout_listing_minutes`, `docker_operations_timeout_check_minutes` and `docker_operations_timeout_export_minutes` from 5 to 15 minutes, and `max_concurrent_base_sync_ops` from 6 to 5, so large base images finish syncing.
- Fixed the chart failing to render with `hopsworks.dropDatabase: true`.
- Added `global._hopsworks.initContainerResources` (`waiter`, `tool`, `runtime`) to size the requests and limits that init containers now set.

## 5.0.8 { #hopsworks-5-0-8 }

### What's changed

- Fixed a security issue in feature views.
- Fixed security vulnerabilities in the Hopsworks server dependencies, in the Payara, HopsFS, Hive Metastore, ArrowFlight, OnlineFS, Airflow, Git, toolbox, base environment, Filebeat, Grafana, OpenSearch, OpenSearch Dashboards, Logstash, remote shuffle service and Superset images, and in the MySQL database of Superset.
- Added an upload policy, `hopsworks.variables.upload_policy`, that allows file uploads to everyone (`enabled`), to administrators only (`admins_only`) or to nobody (`disabled`), from the web UI and from clients such as the Python SDK; the web UI disables its upload controls for blocked users.
  The upgrade writes the value to the cluster, so a change made in the admin UI lasts until the next upgrade.
- Fixed Kafka failing to start on clusters with many API groups, such as OpenShift, when the Vertical Pod Autoscaler (`global._hopsworks.vpaEnabled`) is on, because pod creation stalled for about 20 seconds.
- Fixed Arrow Flight queries of partitioned DELTA feature groups failing once the feature group is older than `delta.logRetentionDuration`.
- Added deleting rows from the online store of a feature group with `remove_rows`; online ingestion results and the ingestion activity in the UI show them as deleted rows.
- Fixed the **SQL Runner** returning a different number of rows on each run, ignoring the row limit for some queries and discarding the typed query when the limit changed; it now shows the row count of a result.
- Fixed Superset queries through Trino logging `Access Denied: Cannot access catalog system`, and project creation and new project members logging Trino `Access Denied: Invalid credentials` errors before their Superset connection is ready.
- Fixed project members with the Observer role being offered Superset actions that fail; the UI now disables them.

### Breaking changes

- `vpa.image.tag` is now a string, instead of a number, so an override such as `1.2` fails the values schema.
  If you override it, quote it and set it equal to `vpa.imagesTag` before you upgrade; with `--reuse-values` and `global._hopsworks.vpaEnabled: true`, use `--reset-then-reuse-values`.

### Upgraded components

| Component | 5.0.6 | 5.0.8 |
| --------- | ----- | ----- |
| Airflow image | 5.0.1 | 5.0.2 |
| ArrowFlight server | 5.0.0 | 5.0.2 |
| Base environment images | 5.0.2 | 5.0.5 |
| Filebeat | 8.15.0 | 8.19.20 |
| Git image | 1.4 | 1.4.1 |
| Grafana | 10.2.2-h6 | 10.2.2-h7 |
| Hive Metastore | 3.0.0.14.5-v1 | 3.0.0.14.6-v1 |
| HopsFS | 3.4.3.1-EE-RC3 | 3.4.3.1-EE-RC4 |
| Logstash | 7.17.9.4 | 7.17.9.5 |
| OnlineFS | 2.3.2 | 2.3.4 |
| OpenSearch | 1.3.6.2 | 1.3.6.3 |
| OpenSearch Dashboards | 1.3.6.6 | 1.3.6.7 |
| Payara | 6.2024.12-jdk17.6 | 6.2024.12-jdk17.8 |
| Remote shuffle service (Apache Uniffle) | 0.10.7 | 0.10.8 |
| Spark | 3.5.5.1 | 3.5.5.2 |
| Spark history server | 3.5.5.1 | 3.5.5.2 |
| Superset | 6.0.0p2.4 | 6.0.0p3.4 |
| Superset MySQL | 8.4.5-debian-12-r0-h2 (MySQL 8.4.10) | 8.4.5-debian-12-r0-h3 (MySQL 8.4.11) |
| Toolbox image (hwutils) | 1.7 | 1.7.1 |
| Vertical Pod Autoscaler | 1.2.1 | 1.7.1 |
| Vertical Pod Autoscaler installer | 1.2 | 1.7.1 |

### Configuration changes

- Added `hopsworks.jupyter.notebookConfig.enableUploads`; set it to `false` to block file uploads from the Jupyter UI and base64 uploads through the Jupyter Contents API.

## 5.0.6 { #hopsworks-5-0-6 }

### What's changed

- Fixed security vulnerabilities in the Hopsworks and Hopsworks CA images.
- Fixed Airflow failing to start on OpenShift with `airflow: command not found`.
- Added the full color palette, interface styles such as border radius, border width and shadows, a live preview, and a branding export, import and reset to the Branding page of the cluster settings, shown when the cluster variable `enable_custom_branding` is `true`.
- Fixed the create and edit forms of model and LLM deployments: a hidden tracing field could block saving, the vLLM image tag could stay blank, and editing a deployment reset its resources.
- Fixed feature monitoring charts not showing the standard deviation.

### Upgraded components

| Component | 5.0.5 | 5.0.6 |
| --------- | ----- | ----- |
| Airflow image | 5.0.0 | 5.0.1 |

### Configuration changes

- Added `docker-registry.affinity`, `minio.affinity` and `hopsworks.dockerRegistry.preset.affinity` for the Docker registry, MinIO and the preset image push Job.

## 5.0.5 { #hopsworks-5-0-5 }

### Upgraded components

| Component | 5.0.4 | 5.0.5 |
| --------- | ----- | ----- |
| RonDB | 26.02.6 | 26.02.8 |

### Configuration changes

- Added `rondb.rondb.timeoutsMinutes.ndbmtdStartupProbe` and `rondb.rondb.timeoutsMinutes.mysqldStartupProbe`, the startup probe timeouts of the RonDB data nodes and MySQL servers, and raised them from 25 to 120 minutes and from about 17 to 20 minutes.
- Added `rondb.rondb.ndbmtdSequencedRollout.enabled` (default `false`) to roll the RonDB data nodes one node group at a time, on clusters with more than one node group.

## 5.0.4 { #hopsworks-5-0-4 }

### What's changed

- Fixed online feature store ingestion skipping rows that failed with transient RonDB errors, such as `Rowid already allocated`, during a RonDB upgrade; it now pauses and retries until they are written.
  Set the pause between retries with `onlinefs.configmapOverrides.onlinefssite.service.pauseRetrySleepMs` (default `5000`).

### Upgraded components

| Component | 5.0.3 | 5.0.4 |
| --------- | ----- | ----- |
| OnlineFS | 2.3.1 | 2.3.2 |

### Configuration changes

- Added `hopsworks.service.worker.external.https.nodePort` to pin the node port of the Hopsworks HTTPS service when its `type` is `NodePort`.

## 5.0.3 { #hopsworks-5-0-3 }

### What's changed

- Fixed the Hopsworks admin pod getting stuck in CrashLoopBackOff when workers were slow to register; the admin sidecar now keeps retrying, restarts unregistered workers and redeploys Hopsworks after the admin container restarts.
- Fixed security vulnerabilities in the Strimzi operator and Kafka images.
- Changed the Hopsworks admin container to restart after about 10 minutes without a response (`hopsworks.probs.admin.livenessProbe`), with up to 30 minutes to start (`hopsworks.probs.admin.startupProbe`).

### Breaking changes

- The admin liveness and startup probes now have a default `exec` handler, instead of no probe, so a probe you set with `httpGet` or `tcpSocket` also needs `exec: null`, or Kubernetes rejects the pod.
  This needs Helm 4 or Helm 3.17.1 or later, because older Helm 3 releases ignore a `null` for a subchart value.

### Deprecations

- Deprecated `hopsworks.envs.postInstall.DEPLOY_RETRIES`, which has no effect now that the admin sidecar retries until the deployment succeeds.

### Upgraded components

| Component | 5.0.2 | 5.0.3 |
| --------- | ----- | ----- |
| HopsFS | 3.4.3.1-EE-RC1 | 3.4.3.1-EE-RC3 |
| RonDB | 26.02.5 | 26.02.6 |
| Strimzi | 0.45.1-h4 | 0.45.1-h5 |

### Configuration changes

- Added `hopsfs.objectStorage.s3.disableCertChecking` and `hopsfs.objectStorage.s3.disableChecksumValidation` to turn off TLS certificate checks and client-side checksum validation for the HopsFS S3 endpoint.
- Added `hopsworks.envs.postInstall.DEPLOY_RETRY_INTERVAL_SEC`, `ASADMIN_TIMEOUT_SEC` and `ASADMIN_DEPLOY_TIMEOUT_SEC` to tune how the admin sidecar retries the Hopsworks deployment.

## 5.0.2 { #hopsworks-5-0-2 }

### What's changed

- Fixed a failed HopsFS schema migration being reported as successful, which let the NameNode start on a partly migrated schema.
- Fixed online feature store ingestion stalling after a feature group with pending records was deleted.
- Added post-delete Jobs that remove the Secrets, ConfigMaps and certificates `helm uninstall` used to leave behind.
- Added [mandatory tags](https://docs.hopsworks.ai/5.0/user_guides/fs/tags/mandatory_tags/) for models and deployments, and tags on deployments.
  Model tags move from HopsFS to the database the first time a model is read or tagged after the upgrade, and a tag that no longer matches its schema is dropped.
- Changed projects created without the `Users` dataset to get it, with a home folder for each member, automatically after the upgrade, instead of asking the data owner to enable private user directories.
- Fixed `pip install` and `uv pip install` in the web terminal, and `uv pip install` in Jupyter and Ray, ignoring the index, mirror and proxy settings in `hopsworks.dockerImage.pypi.global_parameters`.
- Fixed deleting a feature group failing after many online ingestions; Hopsworks now keeps the latest 1000 online ingestions of each feature group (cluster variable `online_ingestion_max_per_featuregroup`).
- Changed LLM deployments to no longer get the inference logger sidecar, which they never used.
- Fixed saving the Alertmanager configuration in the admin UI silently failing when it sets a boolean or numeric option, such as `smtp_require_tls` or `max_alerts`.
- Fixed the data preview of a feature view's logging feature group failing.

### Breaking changes

- `helm uninstall` now deletes the data volumes of the HopsFS DataNodes, MinIO, OpenSearch, Kafka, Consul and the remote shuffle service, for good, instead of keeping them.
  To keep them, set `global._hopsworks.wipeDataOnUninstall: false` or label the PVCs `hopsworks.ai/keep=true` before you uninstall; the Superset MySQL volume is deleted regardless.

### Upgraded components

| Component | 5.0.1 | 5.0.2 |
| --------- | ----- | ----- |
| Base environment images | 5.0.1 | 5.0.2 |
| Model serving webhook | 5.0.1 | 5.0.2 |
| OnlineFS | 2.3 | 2.3.1 |
| RonDB | 26.02.4 | 26.02.5 |

### Configuration changes

- Added `cleanupOnUninstall.enabled` to each component chart, such as `hopsworks.cleanupOnUninstall.enabled`, and `certs-operator.gracefulCertTeardown.enabled`, to turn off the uninstall cleanup of that component.

## 5.0.1 { #hopsworks-5-0-1 }

### What's changed

- Fixed database initialization and migrations starting while RonDB was still restarting; they now wait up to 30 minutes for each RonDB StatefulSet to roll out.
- Fixed security vulnerabilities in the MySQL database of Superset.
- Added support for Kubernetes 1.35 and 1.36.
- Added [model monitoring](https://docs.hopsworks.ai/5.0/user_guides/mlops/model_monitoring/), which compares the inference data a deployment logs with the model's training dataset and shows the drift on the deployment page, and [distribution comparison](https://docs.hopsworks.ai/5.0/user_guides/fs/feature_monitoring/distribution_comparison/) to feature monitoring; `hopsworks.variables.feature_monitoring_max_num_features` (default `15`) caps the features of a configuration.
- Added [chaining of on-demand transformation functions](https://docs.hopsworks.ai/5.0/user_guides/fs/feature_group/on_demand_transformations/#chaining-on-demand-transformations), where the output of one function feeds another, with a view of the chain on the feature group and feature view pages.
- Added secondary indexes for online feature groups, declared in `OnlineConfig` when the feature group is created.
- Added the online feature store (RonDB) quotas and memory usage to the project settings, a banner on project pages near or over quota, and a Quotas and Rate Limits page in the cluster settings for the defaults of new projects; HopsFS quotas are now labelled GB instead of TB, the unit they always had.
  Default RonDB quotas in `hopsworks.variables.rondb_quotas` now apply to new projects; usage refreshes every `hopsworks.variables.rondb_usage_cache_ttl_seconds`, and on a large cluster raise `rondb_usage_query_timeout_seconds` if usage stops showing.
- Added Git repositories as a source for agent deployments, token prices per deployment to estimate the LLM cost, and dashboards of traces, LLM calls, tokens, cost and tool calls.
  Agent deployments now mount HopsFS, which on clusters with Kyverno needs `hw-kyverno.policyExceptions.pythonDeployment.enabled` (default `true`).
- Added an app base path, a proxy routing mode and a readiness probe path to [apps](https://docs.hopsworks.ai/5.0/user_guides/projects/apps/), so an app can be served from its root without `APP_BASE_URL_PATH`; existing apps keep the prefix routing, and the App Metrics Grafana dashboard shows zero instead of "No data" for apps without traffic.
- Added a lifecycle webhook that posts user, project and membership events to `hopsworks.variables.lifecycle_webhook_url`, tagged with `lifecycle_webhook_cluster_id` and signed with HMAC-SHA256 when `lifecycle_webhook_secret` is set.
- Fixed model deployments with images from the managed Docker registry failing to start.
- Fixed adding a member to a project failing when feature groups are shared with that project.
- Fixed environment builds against the managed Docker registry ignoring `hopsworks.variables.docker_operations_push_insecure` and failing on a self-signed certificate; set the new `hopsworks.variables.docker_operations_registry_http` to `"true"` for a registry served over plain HTTP.
- Fixed environment variables set in an app's configuration not reaching the app, and not showing when you edit the app.
- Fixed web terminals shutting down after about 30 minutes in a background browser tab or on a sleeping laptop; a terminal now stops only when its session expires.
- Fixed giving project members access to Superset failing with HTTP 429 (Too Many Requests) errors.
- Fixed Superset redirecting to its internal host behind a reverse proxy that rewrites the Host header; set `hopsworks.variables.hopsworks_public_proxy_url` to the public `host[:port]`.
- Fixed project membership changes being slow, and Airflow requests timing out or failing with server errors, when Airflow is turned off (`global._hopsworks.airflow.enabled: false`).
- Fixed failed or partly deleted projects counting against the owner's maximum number of projects.
- Fixed ingestion with dltHub and schema fetching from NoSQL data sources failing when the project, data source or table names are long.
- Fixed project pages showing a "Feature not enabled: DATA_SCIENCE_PROFILE" error when the data science profile is off; the model registry, deployments and apps are now hidden from the menu.

### Breaking changes

- Feature monitoring is now on by default, instead of off, and the upgrade writes `hopsworks.variables.enable_feature_monitoring` to the cluster, replacing a value set in the admin UI.
  To keep it off, set it to `'false'` before you upgrade.

### Upgraded components

| Component | 5.0.0 | 5.0.1 |
| --------- | ----- | ----- |
| Base environment images | 5.0.0 | 5.0.1 |
| HopsFS | 3.4.3.1-EE-RC0 | 3.4.3.1-EE-RC1 |
| Model serving webhook | 5.0.0 | 5.0.1 |
| RonDB MySQL metrics exporter | 0.11.4 | 0.11.5 |
| Superset MySQL | 8.4.5-debian-12-r0-h1 | 8.4.5-debian-12-r0-h2 (MySQL 8.4.10) |

### Configuration changes

- Added `rondb.rondb.mysql.exporter.maxOpenConnections` (default `1`), the connections of the RonDB MySQL metrics exporter; the render fails if it exceeds `rondb.rondb.mysql.exporter.maxUserConnections`.
- Added `hive.externalLoadBalancer.enabled` (default `false`) to expose the Hive Metastore outside Kubernetes, for example to external Spark applications.
- Added `kserve.kserve.servingruntime.vllmopenai.imageRegistry` and `kserve.kserve.servingruntime.vllmomni.imageRegistry` to pull the vLLM images from a mirror.
- Added `hopsworks.velero.backup.storageLocation.s3ForcePathStyle` for S3-compatible backup stores that need path-style addressing.
- Added `rondb.rondb.rondbConfig.UseTcInRRGroup` and `rondb.rondb.rondbConfig.MaxRRGroupSize` to tune the RonDB round-robin groups.

## 5.0.0 { #hopsworks-5-0-0 }

Entries marked with a 4.8 release also shipped in that 4.8 patch release, so you can skip them if you upgrade from it or a later one.
If you run 4.8.13 or later, or use Airflow with more than one MySQL server, upgrade to the latest 5.0 release instead of 5.0.0.

### What's changed

- Fixed a security issue in the feature store.
- Fixed external LoadBalancer Services, such as those of ArrowFlight, HopsFS, OpenSearch and Trino, not being created with Helm 3.20.1 and later; a component without its own setting again follows `global._hopsworks.externalLoadBalancers`.
- Changed RonDB upgrades to roll the management server first, so data nodes no longer shut down with error 2305, and to fail when `rondb.rondb.clusterSize.numNodeGroups` differs from the running cluster, which RonDB can't change online (also in 4.8.6).
- Fixed fresh installs failing and rolling back when the Knative Serving webhook was not ready yet.
- Fixed `helm upgrade --force` failing with a conflict on unchanged chart Jobs, which now run again on every `helm upgrade` (also in 4.8.3).
- Fixed security vulnerabilities in the OpenSearch image.
- Fixed security vulnerabilities in the Payara image (also in 4.8.10).
- Fixed security vulnerabilities in the Strimzi images and the Redis image of Superset (also in 4.8.6).
- Fixed security vulnerabilities in the Grafana, OpenSearch Dashboards and remote shuffle service images, and in the MySQL image of Superset (also in 4.8.11).
- Changed the Hopsworks UI to a new design, with a regrouped project sidebar.
- Added Agent Tasks, jobs that run Claude Code or OpenAI Codex headless on a prompt, in the new `agent-job` environment; turn them off with `hopsworks.variables.agent_jobs_enabled: "false"`, see [Agent Tasks](https://docs.hopsworks.ai/5.0/user_guides/agents/tasks/).
- Added Agent Deployments, the Python deployments without a model, listed under **Agents** and with optional OpenTelemetry tracing into project feature groups; see [Agent Deployments](https://docs.hopsworks.ai/5.0/user_guides/agents/deployments/).
  Size the tracing sidecar with `hopsworks.variables.agent_deployment_otel_cpu` and `agent_deployment_otel_memory_mb`, or turn tracing off for the cluster with `agent_deployment_otel_enabled: "false"`.
- Added Apps, Streamlit dashboards and custom web apps such as Flask, FastAPI or Gradio that run as long-lived services in a project, on the new `python-app-pipeline` environment; see [Apps](https://docs.hopsworks.ai/5.0/user_guides/projects/apps/).
- Added the Wizard, which opens on an empty project, asks what to build and from which data, and hands a kickoff prompt to Claude Code in the web terminal; it can import the feature groups of the `hopsworks_default` project (cluster variable `default_featurestore_project_name`).
- Added Spark and GPU web terminals, and Claude Code, OpenAI Codex, the `hops` CLI and a `kubectl` limited to the project in every terminal; with `hopsworks.terminal.enabled`, the chart also pushes the terminal images.
- Added Platform Intelligence, which uses an LLM to suggest feature group metadata and ingestion schedules from a data source preview, generate vLLM configurations and fill in model deployments; set `hopsworks.variables.platform_intelligence_llm_api_key`, and optionally `platform_intelligence_llm_model` and `platform_intelligence_llm_base_url`, to turn it on.
- Added SAP HANA, Databricks Unity Catalog (on AWS, with a personal access token or OAuth machine-to-machine credentials), MongoDB and Oracle data sources; see [Data sources](https://docs.hopsworks.ai/5.0/user_guides/fs/data_source/).
- Added a `Users` dataset with a private home directory per member, where Jupyter, Git and the web terminal start; a Data Owner can add it to an existing project, and it can't be shared.
- Added logical dates and data intervals to job schedules, which jobs read from `HOPS_LOGICAL_DATE`, `HOPS_START_TIME` and `HOPS_END_TIME`, with catch-up of missed intervals; see [Schedule a job](https://docs.hopsworks.ai/5.0/user_guides/projects/jobs/schedule_job/).
- Added per-project DAG isolation and the last runs of each DAG on the Airflow page; see [Airflow 3 in Hopsworks](https://docs.hopsworks.ai/5.0/user_guides/projects/airflow/airflow3_upgrade/).
- Added account-level environment variables, encrypted and injected into every job, deployment, app, Jupyter server and terminal you start, optionally from one of your secrets or shared with a project; see [Account-level environment variables](https://docs.hopsworks.ai/5.0/user_guides/projects/env_vars/create/).
- Added an optional expiration date to API keys; see [Create an API key](https://docs.hopsworks.ai/5.0/user_guides/projects/api_key/create_api_key/).
- Added `ddl-mysqld`, a separate MySQL server for online feature store schema changes, enabled by default with `rondb.rondb.meta.ddlMySQLd.enabled` (also in 4.8.4).
- Added asynchronous upload of HopsFS blocks to object storage (`hopsfs.objectStorage.asyncUpload.enabled`, off by default).
  With it on, a stopping DataNode first uploads its pending blocks, which can take about an hour (`hopsfs.datanode.gracefulDrain`); turning that drain off can lose them.
- Added the `python-agent-pipeline` environment, with FastAPI, LangChain, LlamaIndex and OpenTelemetry, for Python agents.
- Added public links to Streamlit apps, which open without a Hopsworks login, when `hopsworks.variables.streamlit_sharing` is `true`.
- Added request metrics to apps: an Envoy sidecar measures requests and latency, shown with CPU, memory and Kubernetes status on the app page and in the new App Metrics Grafana dashboard.
- Added Kyverno policy exceptions so apps and web terminals start under Kyverno policies (`hw-kyverno.policyExceptions.pythonapp.enabled`, `hw-kyverno.policyExceptions.terminal.enabled`).
- Added the datasets shared with a project to the HopsFS mount of Jupyter, jobs, apps and terminals, under `/hopsfs/shared-datasets/<project>/<dataset>`.
- Added browser sign-in for the `hops` CLI, which creates an API key for the project you pick.
- Added an optional transform script to dltHub ingestion jobs, which now run in the `dlthub-ingestion-pipeline` environment, and memory and CPU recommendations to the ingestion forms; see [Ingest data with dltHub](https://docs.hopsworks.ai/5.0/user_guides/fs/feature_group/ingest_with_dlthub/).
- Added downloading models from Hugging Face into the Model Registry from the UI; see [Import a model from Hugging Face](https://docs.hopsworks.ai/5.0/user_guides/mlops/registry/import_huggingface/).
- Added deleting a feature group together with the feature views that use it (`deleteFeatureViews`), or with `force` while keeping them, and removing a feature group or feature store shared with your project without deleting the original.
- Added a choice of a hash or an ordered index for the primary key of online feature groups.
- Added lookback windows to point-in-time joins and extra filters to batch data reads of feature views (also in 4.8.10).
- Added the `vllm-omni` serving runtime and a choice of vLLM version for each deployment, and moved the `vllm-openai` runtime to the `vllm/vllm-openai` image (also in 4.8.7).
- Added the `TIMESTAMP(n)` and `DATETIME(n)` online types with fractional seconds (also in 4.8.7).
- Added environment variables to deployments (also in 4.8.6).
- Added a Superset dashboards page to projects, to make dashboards public, share them with other projects, create permalinks and delete them; see [Superset](https://docs.hopsworks.ai/5.0/user_guides/projects/superset/superset/).
- Added a Superset Public role to share dashboards and chart permalinks without a login, and enabled dashboard role-based access control.
  Only dashboards granted to the Public role are public; set `superset.superset.allowAnonymousAccess: false` to require a login for all.
- Added Grafana dashboards and Prometheus alerts for the MySQL and Redis of Superset, and capped the Superset Redis memory at 256 MB with `allkeys-lru` eviction.
- Changed starting a Jupyter server, terminal or app to fail with HTTP 503 when the cluster is at its session limit, and added session capacity badges to those pages and WebSocket proxy panels to the Hopsworks Grafana dashboard; see [WebSocket proxy pool](https://docs.hopsworks.ai/5.0/setup_installation/admin/monitoring/websocket-pool/).
- Changed job runs to fail with HTTP 429 when the user already has 10 queued executions of the job (cluster variable `quotas_max_queued_executions_per_user_per_job`, `-1` turns the limit off).
- Changed web terminal sessions to end after 4 hours instead of 8 (cluster variable `terminal_session_hours`).
- Added CPU and memory requests and limits to the initialization step of Spark and Ray jobs, tuned with `hopsworks.variables.kube_scheduling_jobinit_*`, and to Git operation pods, so namespace quotas count them.
- Changed the HopsFS DataNode PodDisruptionBudget to evict one DataNode at a time, and HopsFS pods to restart when a `helm upgrade` changes the HopsFS configuration.
- Changed ArrowFlight queries to read only the partitions and files that match their filters (also in 4.8.3).
- Added uploading a file as a secret (also in 4.8.9).
- Added drag-and-drop upload of files and folders to the file browser.
- Added `source=opensearch` to the deployment logs API, to read the logs of stopped deployments.
- Changed Python deployments without a model to reject request batching and inference logging, which they don't support.
- Changed the console logs of the HopsFS NameNode and DataNodes from JSON to plain text.
- Changed the error pages of the Hopsworks server from the Payara defaults to Hopsworks pages.
- Fixed a failed or concurrent feature group creation leaving a Hive table behind that blocked creating the feature group again.
- Fixed model deployments being rejected on OpenShift by the `restricted-v2` security context constraint.
- Fixed the image push Job not running again under Argo CD when only image versions or digests changed (also in 4.8.6).
- Fixed new feature group and training dataset locations naming a NameNode pod IP (also in 4.8.7).
- Fixed libhdfs in Jupyter not finding HopsFS with a custom Consul domain (also in 4.8.7).
- Fixed Airflow pods failing to start when the HopsFS mount took longer than 30 seconds.
- Fixed downloading Superset charts through Hopsworks, and the Hopsworks proxy passing only 5 Superset requests at a time; tune its connection pool and timeouts with `hopsworks.variables.superset_proxy_*`.
- Fixed BigQuery previews failing for SQL queries and for BigQuery projects with a hyphen in their name, previews scanning the whole table, and the **Materialization Dataset** error staying after **BigQuery Project** was filled.
- Fixed web terminals failing to pull their image from a registry that needs credentials.
- Fixed the UI hanging when a web terminal failed to start.
- Fixed feature store metrics counting Hudi metadata columns as features (also in 4.8.9).
- Fixed adding an expectation to an expectation suite in the UI.
- Fixed the pagination of the feature usage table (also in 4.8.9).

### Breaking changes

- Upgraded Airflow from 1.10 to Airflow 3, and DAGs written for Airflow 1.10 don't run on it.
  The upgrade drops and recreates the Airflow metadata database, so DAG run history and the Variables and Connections created in Airflow are lost for good; see [Airflow 3 in Hopsworks](https://docs.hopsworks.ai/5.0/user_guides/projects/airflow/airflow3_upgrade/).
- Hopsworks now deletes finished job executions and their logs 90 days after they end, instead of keeping them, and deletes the older ones as soon as it starts after the upgrade.
  Copy the logs you want to keep before you upgrade; the cluster variable `executions_ttl_days` sets the retention (`0` turns it off) and takes effect when Hopsworks restarts.
- Removed `hopsworks.variables.dlthub_image_name`, replaced by the `dlthub-ingestion-pipeline` environment, and `hopsworks.payara.executorService`, replaced by `hopsworks.payara.websocketProxy`.
  Remove them from your values before you upgrade, because the values schema rejects them.
- `global._hopsworks.superset.mysql.enabled` and `global._hopsworks.superset.redis.enabled` must match `superset.mysql.enabled` and `superset.superset.redis.enabled`, which used to be enough on their own.
  If you disabled the MySQL or Redis of Superset, also set the matching global value to `false`, or the chart fails to render.
- The Spark operator pre-upgrade Job now pulls the `spark-operator-crds` image (`spark.sparkOperatorUpgradeJob.crdImage`) on every upgrade, instead of the toolbox image (also in 4.8.17).
  Air-gapped installations must mirror it first, or `helm upgrade` fails.
- `hopsworks.variables.jupyter_shell_command` is now a JSON list of the command and its arguments, instead of a path.
  If you set it, rewrite it as a list, for example `'["/bin/bash"]'`, because a plain path produces an invalid Jupyter configuration.
- Removed `VLLM_USE_FLASHINFER_SAMPLER=0` from the vLLM serving runtimes (also in 4.8.7).
  If you serve vLLM models on GPUs older than compute capability 7.5, set it in `kserve.kserve.servingruntime.vllmopenai.env` or `kserve.kserve.servingruntime.vllmomni.env`.

### Deprecations

- Deprecated `airflow.reset_db_if_error`, which Airflow 3 ignores.
- Deprecated `hopsfs.datanode.podDisruptionBudget.minAvailable`, which the DataNode PodDisruptionBudget no longer reads.

### Upgrade steps

No upgrade steps are listed for this release.

### Upgraded components

| Component | 4.8.2 | 5.0.0 |
| --------- | ----- | ----- |
| Airflow image | 4.8.0 | 5.0.0 |
| ArrowFlight server | 4.8.0 | 5.0.0 |
| Base environment images | 4.8.1 | 5.0.0 |
| Git image | 1.3 | 1.4 |
| Grafana | 10.2.2-h3 | 10.2.2-h6 (also in 4.8.11) |
| Hive Metastore | 3.0.0.13.15 | 3.0.0.14.5-v1 |
| HopsFS | 3.2.0.19-EE-RC0 | 3.4.3.1-EE-RC0 |
| Inference logger | 4.8.0 | 5.0.0 |
| Model serving authenticator | 4.8.0 | 5.0.0 |
| Model serving webhook | 4.8.0 | 5.0.0 |
| OnlineFS | 2.2 | 2.3 |
| OpenSearch | 1.3.6.1 | 1.3.6.2 |
| OpenSearch Dashboards | 1.3.6.3 | 1.3.6.6 (also in 4.8.11) |
| Payara | 6.2024.12-jdk17.2 | 6.2024.12-jdk17.6 |
| Python in the base environments | 3.11 | 3.12 |
| Ray | 2.9.0 | 2.55.1 |
| Remote shuffle service (Apache Uniffle) | 0.10.5 | 0.10.7 (also in 4.8.11) |
| RonDB | 26.02.2 | 26.02.4 (also in 4.8.11) |
| scikit-learn model server | 0.14.0 | 0.14.1 |
| Spark | 3.5.5 | 3.5.5.1 |
| Spark history server | 3.5.5 | 3.5.5.1 |
| Storage initializer | 4.8.0 | 5.0.0 |
| Strimzi | 0.45.1-h3 | 0.45.1-h4 (also in 4.8.6) |
| Superset | 6.0.0.0 | 6.0.0p2.4 |
| Superset MySQL | 8.4.5-debian-12-r0 | 8.4.5-debian-12-r0-h1 (also in 4.8.11) |
| Superset Redis | 7.0.10-debian-11-r4 | 7.4.9-bookworm (also in 4.8.6) |
| TensorFlow | 2.17.0 | 2.19.0 |
| TensorFlow Serving | 2.17.0 | 2.19.0 |
| Toolbox image (hwutils) | 1.4 | 1.7 |
| Trino | 477-v0 | 480-v6 |
| vLLM | v0.14.0 | v0.20.0 (also in 4.8.7) |

### Configuration changes

- Changed the default HopsFS resources: 1024 MiB of heap instead of 500, a CPU request of 1 and a CPU limit of 4 instead of 500m and 1000m for the NameNode and DataNodes, a NameNode memory request of 1024Mi and limit of 2560Mi instead of 500Mi and 750Mi, a DataNode memory limit of 2048Mi instead of 750Mi, and 1024 MiB of NameNode direct memory instead of 500.
  Plan for the extra CPU requests of the 5 default DataNodes.
- Fixed `hopsfs.namenode.auditLog.enableStatOperation` and `enableListOperation` being ignored; the NameNode no longer audit-logs stat and list operations unless you set them to `true` (also in 4.8.8).
- Changed `hopsfs.image.registry`, when set, to override `global._hopsworks.imageRegistry` as the full registry and path prefix of the HopsFS image, ending in `/`.
- Added the Superset, Trino and Kueue images to `values.airgap.yaml`.
- Added `hopsworks.payara.websocketProxy` to tune the WebSocket proxy of Jupyter, terminals and apps, such as `maxSessionsPerApp` (default `500` per pod).
- Added `hopsworks.variables.kube_user_workload_tolerations` for tolerations on user workloads such as Jupyter, jobs and deployments (also in 4.8.8).
- Added `hopsworks.dockerImage.packageAuth.secretName` and `caCertsConfigMap` for pip, conda and apt mirrors that need credentials or a private CA (also in 4.8.8).
- Added `global._hopsworks.kyverno.policies.addCertificatesVolume.initContainers.enabled` to inject the custom CA certificates into the init containers of pods annotated `kyverno-inject-certs-init: enabled` (also in 4.8.8).
- Added `onlinefs.configmapOverrides` to tune the threads, caches, and RonDB, Kafka and logging settings of the online feature store service.
- Added `hopsworks.variables.kube_serving_vllm_versions` and `kube_serving_vllm_omni_versions`, the vLLM image tags a deployment can choose; update them when you change the vLLM runtime images (also in 4.8.7).
- Added `rondb.rondb.createPriorityClass`, which you set to `false` when the RonDB PriorityClass already exists, for example on a satellite cluster (also in 4.8.5).
- Added RonDB settings such as `DataMemory` and `TimeBetweenGlobalCheckpoints` to `rondb.rondb.rondbConfig` (also in 4.8.5).
- Added `hopsfs.namenode.blockSizeMiB` (default `128`) to set the HopsFS block size.
- Added `arrowflight.deployment.server.hopsfs_query_mode` to make the ArrowFlight server load feature group data into DuckDB tables (`table`) instead of views (`view`) (also in 4.8.3).
- Added `BackupLogBufferSize` to `rondb.rondb.rondbConfig` (also in 4.8.6).
- Added `PartitionsPerNode` to `rondb.rondb.rondbConfig` (also in 4.8.11).
