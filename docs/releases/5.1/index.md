---
releases:
  "5.1.2":
    released: "2026-10-16"
    python_client: "5.1.2"
  "5.1.1":
    released: "2026-10-09"
    python_client: "5.1.1"
  "5.1.0":
    released: "2026-09-24"
    python_client: "5.1.0"
---

# Release notes { #hopsworks-5-1 }

The releases of Hopsworks 5.1, newest first.

## 5.1.2 { #hopsworks-5-1-2 }

### What's changed

- Addressed vulnerabilities in OpenSearch.
  It applies once an OpenSearch pod logs `Security configuration applied` after the upgrade; if none does, run `run_security_admin.sh` as the chart's `README.md` shows.
- Fixed every OpenSearch restart deleting the OpenSearch roles of restricted-access grants and feature group shares, and every `helm upgrade` restarting OpenSearch.
  Grants and shares made before the last OpenSearch restart on 5.1.0 or 5.1.1 lost their roles, and granting or sharing again is refused: revoke and grant again, or unshare and share again.
- Fixed security vulnerabilities in the Hopsworks certificate authority, Grafana, Filebeat and Superset images, and in the MySQL and Redis of Superset.
- Added an opt-in Job that copies the OpenSearch indices created before OpenSearch 2.0 during a 5.1 upgrade, in a window you pick, so the upgrade to 5.2.1 or later has nothing left to copy; set `olk.opensearch.indexUpgrade.mode` to `report` to list them, or to `copy` ([values][values-olk-index-upgrade]).
  Turn vector ingestion off in an upgrade of its own first (`onlinefs.deployment.vectordb.enabled: false`), and pass the mode with `--set`, not in your values file, because 5.2.1 and later read the same key.
- Changed the SQL Runner of the Query Engine page to fill the page, show row numbers and column types in the results, list a table's columns in the Explorer and draw `EXPLAIN (FORMAT GRAPHVIZ)` plans as a graph ([SQL Runner][docs-sql-runner]).
- Fixed queued service operations failing on every retry when they removed a user from Superset or set up a project Observer's online feature store connection in Superset, and stopping for good after 68 failed attempts; a failing operation now retries once a day.
- Fixed the SQL Runner leaving a query running when you leave it right after starting the query, and its autocompletion offering no column names in `WHERE`, `GROUP BY` or join conditions.

### Breaking changes

- If your values restate `trino.trino.additionalConfigProperties` with its `event-listener.config-files` entry, which the 5.1.1 chart set by default, remove that entry or add the listener files as the chart's `README.md` shows, or Trino doesn't start.
- Recorded Trino queries now lose their query text, plan and JSON details after `hopsworks.variables.trino_events_strip_details_after_days` (`7`), instead of keeping them until the query is deleted after 61 days, and the first nightly cleanup after the upgrade strips every older one; set it to `61` or more to keep them.
- The chart no longer enables Trino's MySQL event listener, which crash-looped the Trino coordinator after a RonDB MySQL server restart, so the admin [Trino query history][docs-trino-history] records no new queries; to keep it, add the listener as the chart's `README.md` shows.

### Upgraded components

| Component | 5.1.1 | 5.1.2 |
| --------- | ----- | ----- |
| Base environment images | 5.1.1 | 5.1.2 |
| Filebeat | 8.19.21 | 8.19.23 |
| Grafana | 12.4.9-h9 | 12.4.9-h10 |
| Payara | 6.2025.11-jdk21.0 | 6.2025.11-jdk21.1 |
| Superset | 6.0.0p4.4 | 6.0.0p4.5 |
| Superset MySQL | 8.4.11-ubuntu24.04-h4 | 8.4.11-ubuntu24.04-h5 |
| Superset Redis | 7.4.11-alpine-h1 | 7.4.11-alpine-h2 |

### Configuration changes

- Removed the MySQL event listener from the default `trino.trino.additionalConfigProperties` and from `trino.trino.coordinator.additionalConfigFiles` and `trino.trino.worker.additionalConfigFiles`.
- Changed the default of `hopsworks.variables.trino_events_cleaner_batch_size` from 1000 to 100.
- Added `hopsworks.variables.trino_events_strip_details_after_days` (default `7`), the days after which a recorded Trino query loses its text, plan and JSON details.

## 5.1.1 { #hopsworks-5-1-1 }

### What's changed

- Addressed vulnerabilities in jobs.
- Fixed OpenSearch losing unflushed vectors and rejecting vector writes for about two minutes on its first start on 5.1.
  A values file that sets `triggered: true` or `percent: 0.75`, or an upgrade with `--reuse-values`, keeps the problem.
- Fixed the database migration of the upgrade from 5.0 failing when the feature groups have more than about 32,000 features in total.
- Fixed the post-upgrade search index rebuild failing without the admin password, for example when password login is disabled, and running on every upgrade; it now runs in the background once per index format, and shows its progress and a **Reindex now** button under **Cluster settings > Service Operations > OpenSearch Index Commands**.
  The first upgrade to 5.1.1 rebuilds the index, and search is incomplete until it finishes.
- Fixed RonDB daemons ignoring SIGTERM, so every pod stop ended in a kill and a stopped data node could stall the cluster.
- Changed the RonDB REST server probes to outlast a data node failure and to use their own port.
- Fixed the RonDB REST server reading request bodies over 64 KiB as empty; it now buffers them in `rondb.rondb.rdrs.uploadPath`.
- Fixed environment builds never starting when `rondb.rondb.priorityClass` is renamed.
- Fixed Trino giving a project access to only one of several feature stores shared with it.
- Fixed a killed Spark job with pending executors staying in the aggregating logs state for up to 20 minutes.
- Fixed the **Why?** button of an online ingestion in a feature group's activity opening every OnlineFS log of the project instead of that ingestion's; it is now named **Logs**.

### Breaking changes

- The post-upgrade search index rebuild signs in as the agent user, instead of with `hopsworks.variables.admin_email` and `admin_password`, and fails the `helm upgrade` if `hopsworks.agent_email` and `hopsworks.agent_password` (default `agent@hops.io`, `admin`) don't match that account.
  Set them, or turn the rebuild off with `hopsworks.opensearchReindex.enabled: false`.
- The RonDB REST server now uses a probe port and an upload path that need RonDB 26.02.11, where 5.1.0 probed its REST port and set no upload path.
  If you pin `rondb.rondb.images.rondb.tag` to an older version, set `rondb.rondb.rdrs.probePort.enabled: false` and `rondb.rondb.rdrs.uploadPath: ""`, or the REST server doesn't start.

### Upgraded components

| Component | 5.1.0 | 5.1.1 |
| --------- | ----- | ----- |
| Base environment images | 5.1.0 | 5.1.1 |
| RonDB | 26.02.10 | 26.02.11 |
| Trino | 480-v10 | 480-v11 |

### Configuration changes

- Changed the defaults of `olk.opensearch.knn.circuit_breaker.triggered` to `false` and `olk.opensearch.knn.circuit_breaker.percent` to `75`.
- Changed the default of `hopsworks.variables.docker_operations_buildkit_priority_class` from `rondb-high-priority` to empty, so environment builds run at the default priority.
- Changed `rondb.rondb.terminationGracePeriodSeconds` to one value per component, and the data nodes' default from 60 to 300 seconds; an integer still sets only the data nodes.
- Fixed `values.openshift.yaml` for the OpenShift `restricted-v2` SCC, covering Strimzi, Kafka, ZooKeeper, the Spark operator and the MySQL and Redis of Superset, and turned off the Prometheus node exporter, which OpenShift ships itself.
  Use it with Helm 4 or Helm 3.17.1 or later, because older Helm 3 releases ignore its `null` overrides of subchart values.
- Fixed the values schema rejecting `hopsworks.variables.loadbalancer_external_domain_namenode` and `hopsworks.variables.loadbalancer_external_domain_datanode`.
- Added `hopsworks.opensearchReindex.enabled` to turn off the post-upgrade search index rebuild, and `hopsworks.variables.command_search_fs_reindex_queue_wait_as_ms` to bound its wait for the search command queue.
- Added `rondb.rondb.rdrs.probes` and `rondb.rondb.rdrs.probePort`, the settings and the port of the RonDB REST server probes, and `rondb.rondb.rdrs.maxKeepaliveRequests` to close a keep-alive connection after that many requests, so clients rebalance after a rolling restart.
- Added `nodePort` values to pin the node ports of unmanaged external load balancers: ArrowFlight, OpenSearch, the HopsFS NameNode and DataNodes, Trino, the Hive Metastore, Kafka (`bootstrapNodePort`, `startingNodePort`) and the RonDB MySQL and REST servers.
  The RonDB ones ignore `global._hopsworks.externalLoadBalancers.managed` and apply only when `rondb.rondb.meta.mysqld.externalLoadBalancer.managed` or `rondb.rondb.meta.rdrs.externalLoadBalancer.managed` is `false`.
- Added `rondb.rondb.rdrs.ttlPurge.enable` and `activeWindow` to turn off the TTL purge of the RonDB REST server or limit it to a daily window.

## 5.1.0 { #hopsworks-5-1-0 }

### What's changed

- Addressed vulnerabilities in model serving.
- Addressed vulnerabilities in environment images.
- Addressed vulnerabilities in feature views (also in [5.0.8][hopsworks-5-0-8]).
- Addressed vulnerabilities in project datasets (also in [5.0.10][hopsworks-5-0-10]).
- Changed model deployments, jobs, Jupyter servers and terminals to each get their own serving API key.
- Fixed security vulnerabilities in the Hopsworks server dependencies and in the Superset, Grafana, Prometheus, Consul, certificates operator, Docker registry, BuildKit, Istio, Knative Serving, KServe utilities, scikit-learn model server, Strimzi, OpenSearch, Logstash and Filebeat images.
- Fixed security vulnerabilities in the Hopsworks server dependencies, in the Payara, HopsFS, Hive Metastore, ArrowFlight, OnlineFS, Airflow, Git, toolbox, base environment, Filebeat, Grafana, OpenSearch, OpenSearch Dashboards, Logstash, remote shuffle service and Superset images, and in the MySQL database of Superset (also in [5.0.8][hopsworks-5-0-8]).
- Fixed security vulnerabilities in the Hopsworks and Hopsworks CA images (also in [5.0.6][hopsworks-5-0-6] and [5.0.9][hopsworks-5-0-9]).
- Fixed security vulnerabilities in the MySQL database of Superset (also in [5.0.1][hopsworks-5-0-1]).
- Fixed security vulnerabilities in the Strimzi operator and Kafka images (also in [5.0.3][hopsworks-5-0-3]).
- Fixed security vulnerabilities in the ArrowFlight and remote shuffle service images (also in [5.0.10][hopsworks-5-0-10]).
- Fixed RonDB data nodes reporting ready while the management server is unreachable, which let a rollout stop the healthy data node of the same node group and shut the cluster down; their liveness probe also no longer kills them then (also in [5.0.11][hopsworks-5-0-11]).
- Fixed RonDB rolling restarts making healthy data nodes shut down; data nodes now wait for the rollout to settle (`rondb.rondb.ndbmtdSettleWait`) (also in [5.0.11][hopsworks-5-0-11]).
- Fixed the Airflow migration Job losing tables on clusters with more than one RonDB MySQL server, so the upgrade never completed; it now uses only the DDL MySQL server (also in [5.0.13][hopsworks-5-0-13]).
  A cluster whose earlier upgrade already failed this way needs the Airflow schema dropped on every MySQL server before it upgrades again.
- Fixed a failed HopsFS schema migration being reported as successful, which let the NameNode start on a partly migrated schema (also in [5.0.2][hopsworks-5-0-2]).
- Fixed online feature store ingestion skipping rows that failed with transient RonDB errors, such as `Rowid already allocated`, during a RonDB upgrade; it now pauses and retries until they are written (also in [5.0.4][hopsworks-5-0-4]).
  Set the pause between retries with `onlinefs.configmapOverrides.onlinefssite.service.pauseRetrySleepMs` (default `5000`).
- Fixed uploading files in the file browser deleting the files of the previous upload unless the page was reloaded (also in [5.0.10][hopsworks-5-0-10]).
- Fixed Velero backups leaving out the Trino authentication Secrets, and the Velero storage location rejecting AWS S3 without a custom endpoint.
- Fixed database migrations crash-looping on a lock left by a transient Kubernetes API error.
- Fixed database initialization and migrations starting while RonDB was still restarting; they now wait for each RonDB StatefulSet to roll out (also in [5.0.1][hopsworks-5-0-1]).
- Fixed init containers that wait for a RonDB rollout giving up after 30 minutes, which failed the Hive Metastore, HopsFS, Airflow migration and CA pods when a RonDB restart took longer (also in [5.0.10][hopsworks-5-0-10]).
- Fixed the RonDB MySQL setup and in-place restore Jobs failing for good when data nodes took more than about two hours to start, and the MySQL servers crash-looping while they wait for a backup restore (also in [5.0.11][hopsworks-5-0-11]).
- Fixed every model deployment failing when the Knative controller started with an empty registry certificate.
- Fixed model deployments with images from the managed Docker registry failing to start (also in [5.0.1][hopsworks-5-0-1]).
- Fixed image pulls from the in-cluster Docker registry failing with `x509: certificate signed by unknown authority`, for example on RHEL-family nodes.
- Fixed online feature store ingestion stalling for every project when a write exceeded the project's RonDB transaction size quota; OnlineFS now commits such a batch in smaller transactions.
- Fixed online feature store ingestion stalling after a feature group with pending records was deleted (also in [5.0.2][hopsworks-5-0-2]).
- Fixed OpenSearch snapshot restores never finishing on single-node clusters, and indices staying closed after a failed restore.
- Fixed the Hopsworks admin pod getting stuck in CrashLoopBackOff when workers were slow to register; the admin sidecar now keeps retrying, restarts unregistered workers and redeploys Hopsworks after the admin container restarts (also in [5.0.3][hopsworks-5-0-3]).
- Fixed service logs being dropped from the `.services` OpenSearch index when Kubernetes labels pushed it past 1000 fields (also in [5.0.12][hopsworks-5-0-12]).
- Fixed Kafka failing to start on clusters with many API groups, such as OpenShift, when the Vertical Pod Autoscaler (`global._hopsworks.vpaEnabled`) is on, because pod creation stalled for about 20 seconds (also in [5.0.8][hopsworks-5-0-8]).
- Fixed OnlineFS upgrades stalling on a full node pool: with two or more `onlinefs.deployment.replicas`, a rollout now replaces one pod at a time (also in [5.0.13][hopsworks-5-0-13]).
- Changed the memory split of the remote shuffle servers to stop heap out-of-memory crashes: 20% of `spark.rss.shuffleServer.resources.limits.memory` is reserved for native memory and the rest is split 25% heap, 75% off-heap (also in [5.0.12][hopsworks-5-0-12]).
- Fixed the remote shuffle servers never receiving their off-heap memory setting, which left their buffers about nine times too small (also in [5.0.12][hopsworks-5-0-12]).
- Added Apache Iceberg as a feature group table format (`time_travel_format="ICEBERG"`), also for feature groups created from Iceberg tables in a data source ([table format](https://docs.hopsworks.ai/5.1/user_guides/fs/feature_group/create/#table-format)).
- Added partition transforms (`partitioned_by`) for Iceberg and Hudi feature groups, Delta liquid clustering (`clustered_by`), Hudi bucket indexes (`bucket_index`), z-ordering (`zorder_by`) and Iceberg sort orders (`sort_order`) ([partitioning](https://docs.hopsworks.ai/5.1/user_guides/fs/feature_group/partitioning/)).
- Added [model monitoring](https://docs.hopsworks.ai/5.1/user_guides/mlops/model_monitoring/), which compares the inference data a deployment logs with the model's training dataset and shows the drift on the deployment page, and [distribution comparison](https://docs.hopsworks.ai/5.1/user_guides/fs/feature_monitoring/distribution_comparison/) to feature monitoring; `hopsworks.variables.feature_monitoring_max_num_features` (default `15`) caps the features of a configuration (also in [5.0.1][hopsworks-5-0-1]).
- Added Trino catalogs that project Data Owners create by hand or from a data source; Trino loads them at its daily scheduled restart (02:00 by default, only when a change is pending) or when an administrator restarts it, and tests them on a single-node coordinator (`global._hopsworks.trino.testCoordinator.enabled`) ([Trino catalogs](https://docs.hopsworks.ai/5.1/user_guides/projects/trino/catalogs/)).
- Added file-based credentials, such as Oracle wallets, for user-created Trino catalogs: a project uploads them as mountable secrets, and a privileged sidecar on every Trino pod mounts `/apps/mountable-secrets` from HopsFS read-only ([credential files](https://docs.hopsworks.ai/5.1/setup_installation/admin/trino/#credential-files-a-project-supplies)).
- Added dltHub ingestion jobs that copy several tables of a data source, each into its own feature group with its own settings and resources ([dltHub ingestion](https://docs.hopsworks.ai/5.1/user_guides/fs/feature_group/ingest_with_dlthub/)).
- Added the AWS Glue data source, and the Google Sheets data source, which ingests spreadsheet tabs into feature groups with dltHub ([AWS Glue](https://docs.hopsworks.ai/5.1/user_guides/fs/data_source/creation/glue/)).
- Added [chaining of on-demand transformation functions](https://docs.hopsworks.ai/5.1/user_guides/fs/feature_group/on_demand_transformations/#chaining-on-demand-transformations), where the output of one function feeds another, with a view of the chain on the feature group and feature view pages (also in [5.0.1][hopsworks-5-0-1]).
- Added secondary indexes for online feature groups, declared in `OnlineConfig` when the feature group is created (also in [5.0.1][hopsworks-5-0-1]).
- Added tags to jobs and apps, and jobs, models, deployments, apps and agents to search; administrators can inspect and cancel stuck search index commands under **Cluster settings > Service Operations** ([tags](https://docs.hopsworks.ai/5.1/user_guides/fs/tags/tags/), [search index](https://docs.hopsworks.ai/5.1/setup_installation/admin/search_index/)).
- Changed feature group schemas to be read from the Hopsworks database instead of the Hive Metastore; existing feature groups move over in the background after the upgrade.
- Added Git repositories as a source for agent deployments, token prices per deployment to estimate the LLM cost, and dashboards of traces, LLM calls, tokens, cost and tool calls (also in [5.0.1][hopsworks-5-0-1]).
  Agent deployments now mount HopsFS, which on clusters with Kyverno needs `hw-kyverno.policyExceptions.pythonDeployment.enabled` (default `true`).
- Added **Auto-redeploy on new commits** to Python apps and agent deployments from a Git repository, which rolls them to each new commit of the tracked branch.
- Added an optional persistent BuildKit daemon (`global._hopsworks.buildkitd.enabled`) that keeps caches between environment builds; each replica requests 8 CPUs, 16Gi of memory and a 100Gi volume ([build performance](https://docs.hopsworks.ai/5.1/setup_installation/admin/build_performance/)).
- Changed environment builds to install libraries with uv when the image has it, to read the library list from the built image instead of starting three more Jobs, and to show the stage of a running build.
- Added npm packages to Python environments, installed globally and on `PATH` for jobs, Jupyter and the terminal; set `hopsworks.variables.npm_registry_url` to install from a registry other than registry.npmjs.org ([installing libraries](https://docs.hopsworks.ai/5.1/user_guides/projects/python/python_install/)).
- Added toolchain caches (`HOPSWORKS_BUILD_CACHE`), layer reuse for scripts that fetch nothing that changes (`HOPSWORKS_BUILD_HERMETIC`) and secret references (`NAME=secret:<secret>`) to custom commands ([custom commands](https://docs.hopsworks.ai/5.1/user_guides/projects/python/custom_commands/#making-custom-command-builds-faster)).
- Added the `dbt-pipeline` environment, with dbt and its Trino and DuckDB adapters, and fixed Jupyter servers on the `agent-job` environment losing their priority class, node affinity and Kueue queue.
- Added an app base path, a proxy routing mode and a readiness probe path to [apps](https://docs.hopsworks.ai/5.1/user_guides/projects/apps/), so an app can be served from its root without `APP_BASE_URL_PATH`; existing apps keep the prefix routing, and the App Metrics Grafana dashboard shows zero instead of "No data" for apps without traffic (also in [5.0.1][hopsworks-5-0-1]).
- Added the online feature store (RonDB) quotas and memory usage to the project settings, a banner on project pages near or over quota, and a Quotas and Rate Limits page in the cluster settings for the defaults of new projects; HopsFS quotas are now labelled GB instead of TB, the unit they always had (also in [5.0.1][hopsworks-5-0-1]).
  Default RonDB quotas in `hopsworks.variables.rondb_quotas` now apply to new projects; usage refreshes every `hopsworks.variables.rondb_usage_cache_ttl_seconds`, and on a large cluster raise `rondb_usage_query_timeout_seconds` if usage stops showing.
- Added deleting rows from the online store of a feature group with `remove_rows`; online ingestion results and the ingestion activity in the UI show them as deleted rows (also in [5.0.8][hopsworks-5-0-8]).
- Added a lifecycle webhook that posts user, project and membership events to `hopsworks.variables.lifecycle_webhook_url`, tagged with `lifecycle_webhook_cluster_id` and signed with HMAC-SHA256 when `lifecycle_webhook_secret` is set (also in [5.0.1][hopsworks-5-0-1]).
- Added [mandatory tags](https://docs.hopsworks.ai/5.1/user_guides/fs/tags/mandatory_tags/) for models and deployments, and tags on deployments (also in [5.0.2][hopsworks-5-0-2]).
  Model tags move from HopsFS to the database the first time a model is read or tagged after the upgrade, and a tag that no longer matches its schema is dropped.
- Added an upload policy, `hopsworks.variables.upload_policy`, that allows file uploads to everyone (`enabled`), to administrators only (`admins_only`) or to nobody (`disabled`), from the web UI and from clients such as the Python SDK; the web UI disables its upload controls for blocked users (also in [5.0.8][hopsworks-5-0-8]).
  The upgrade writes the value to the cluster, so a change made in the admin UI lasts until the next upgrade.
- Added support for Kubernetes 1.35 and 1.36 (also in [5.0.1][hopsworks-5-0-1]).
- Added the GitHub Copilot and OpenCode CLIs to the web terminal, next to Claude Code and Codex; the coding agents share the skills in your home directory and keep their logins and sessions across terminal sessions (also in [5.0.10][hopsworks-5-0-10]).
- Added GitHub Copilot as a provider of agent tasks, signed in with the token of a GitHub AI provider or of your github.com Git provider, which can't be a classic personal access token (also in [5.0.10][hopsworks-5-0-10]).
- Added a Copilot tab and a Business Glossary for each coding agent to the Agents page of the cluster settings, now called Coding Agents (also in [5.0.10][hopsworks-5-0-10]).
- Added support for Git repositories behind a private CA or an HTTP proxy: set `hopsworks.variables.git_custom_ca_configmap` to a ConfigMap that exists in every project namespace, `git_<provider>_http_proxy` and `git_<provider>_https_proxy` for GitHub, GitLab and BitBucket, or `git_disable_tls_verification` (also in [5.0.10][hopsworks-5-0-10]).
- Changed upgrades to update the KServe, Knative Serving and cert-manager CRDs in a pre-upgrade Job, which removes the unused `predictors.serving.kserve.io` CRD.
- Changed environment image builds to the `rondb-high-priority` priority class (`hopsworks.variables.docker_operations_buildkit_priority_class`), so they can preempt Jupyter and job pods.
- Changed Grafana to load the Hopsworks dashboards from its image instead of ConfigMaps; add your own with `global._hopsworks.grafana.extraDashboardProviders`.
  A custom Grafana image must contain the Hopsworks dashboards, and a custom `grafana.grafana.dashboardProviders` must point to `/usr/share/grafana/dashboards/<folder>`.
- Changed Spark metrics to be scraped by Prometheus instead of pushed to the Pushgateway.
- Changed the Trino connections that Hopsworks creates in Superset to allow changing catalogs, so SQL Lab can query any Trino catalog; existing connections are unchanged ([Superset](https://docs.hopsworks.ai/5.1/user_guides/projects/superset/superset/)).
- Changed the Claude Code settings that Hopsworks creates for new project members to auto mode, so agent sessions in the terminal run without a prompt per tool call; existing settings are unchanged.
- Added a load status to alert receivers and to the AlertManager configuration, which shows a change AlertManager has not loaded yet or rejected, and linked the alert title in AlertManager emails to the job, feature group or feature view that raised it ([receiver load status](https://docs.hopsworks.ai/5.1/user_guides/projects/alerts/#receiver-load-status)).
- Added a **Why?** action to online ingestions with failed or ignored rows in the feature group activity, which opens their records in OpenSearch Dashboards.
- Changed OpenSearch snapshots and restores to skip the `.opendistro_security` index and hidden plugin indices.
- Removed the per-project Hive database (`<project>.db`) and its quota from new projects; existing projects keep theirs.
- Added key pair authentication to DLT ingestion from Snowflake (also in [5.0.14][hopsworks-5-0-14]).
- Added a **Stop** button to the SQL Runner (also in [5.0.14][hopsworks-5-0-14]).
- Added post-delete Jobs that remove the Secrets, ConfigMaps and certificates `helm uninstall` used to leave behind (also in [5.0.2][hopsworks-5-0-2]).
- Changed projects created without the `Users` dataset to get it, with a home folder for each member, automatically after the upgrade, instead of asking the data owner to enable private user directories (also in [5.0.2][hopsworks-5-0-2]).
- Changed the Hopsworks admin container to restart after about 10 minutes without a response (`hopsworks.probs.admin.livenessProbe`), with up to 30 minutes to start (`hopsworks.probs.admin.startupProbe`) (also in [5.0.3][hopsworks-5-0-3]).
- Added the full color palette, interface styles such as border radius, border width and shadows, a live preview, and a branding export, import and reset to the Branding page of the cluster settings, shown when the cluster variable `enable_custom_branding` is `true` (also in [5.0.6][hopsworks-5-0-6]).
- Added the status of the TTL purge of online feature groups: a TTL purge card on the feature group overview and a TTL Purge page in the cluster settings (also in [5.0.10][hopsworks-5-0-10]).
- Added a read-only `featurestore` directory to the web terminal with the files of the project's offline feature store (also in [5.0.10][hopsworks-5-0-10]).
- Added the `KafkaAuthenticationFailures` Prometheus alert for clients that keep failing to authenticate, for example with an expired certificate (also in [5.0.10][hopsworks-5-0-10]).
- Changed the Kafka Entity Operator, when `kafka.cluster.entityOperator` is set, to follow the tolerations, topology spread and node affinity of the Kafka brokers, unless set under `kafka.cluster.entityOperator.template.pod` (also in [5.0.11][hopsworks-5-0-11]).
- Added **Driver overhead factor** and **Executor overhead factor** to the Spark configuration of jobs, Jupyter and project defaults, which set `spark.driver.memoryOverheadFactor` and `spark.executor.memoryOverheadFactor` ([PySpark jobs](https://docs.hopsworks.ai/5.1/user_guides/projects/jobs/pyspark_job/)) (also in [5.0.12][hopsworks-5-0-12]).
  Jupyter Spark sessions now default both to `0.4`, as PySpark jobs do, so notebooks and their executors request more memory than before.
- Added a **Monitor** button to each running Spark application on the Jupyter page, showing its driver and executor pods, and fixed the Jupyter server monitor showing a Spark executor as the notebook pod; the Grafana link there is now called **Metrics** (also in [5.0.12][hopsworks-5-0-12]).
- Changed `GET /project/{id}/jupyter/running` to return `204 No Content` instead of `404` when no Jupyter server is running (also in [5.0.10][hopsworks-5-0-10]).
- Removed the Plans dialog from the web terminal (also in [5.0.10][hopsworks-5-0-10]).
- Fixed the Jupyter server of Spark environments running out of memory: it now adds the driver memory overhead of the session's Spark configuration and a floor (`hopsworks.variables.jupyter_spark_notebook_server_memory_floor_mb`) to the driver memory (also in [5.0.10][hopsworks-5-0-10]).
- Fixed Spark executors started from Jupyter having no CPU limit and rounding fractional executor cores up to a whole core; they now get the executor cores of the session as request and limit, as job executors do (also in [5.0.10][hopsworks-5-0-10]).
- Fixed Spark jobs failing to reach the remote shuffle service when an evicted coordinator pod was left behind.
- Fixed API keys created by `hops setup` lacking the `KAFKA`, `PYTHON_LIBRARIES`, `GIT`, `TRINO` and `SUPERSET` scopes, so they could not insert into online feature groups.
- Fixed Ray jobs and the Ray clusters of Jupyter failing to start on OpenShift, because their pods couldn't read the project certificates (also in [5.0.9][hopsworks-5-0-9]).
- Fixed web terminals failing to start on OpenShift (also in [5.0.9][hopsworks-5-0-9]).
- Fixed Airflow failing to start on OpenShift with `airflow: command not found` (also in [5.0.6][hopsworks-5-0-6]).
- Fixed adding a member to a project failing when feature groups are shared with that project (also in [5.0.1][hopsworks-5-0-1]).
- Fixed environment variables set in an app's configuration not reaching the app, and not showing when you edit the app (also in [5.0.1][hopsworks-5-0-1]).
- Fixed web terminals shutting down after about 30 minutes in a background browser tab or on a sleeping laptop; a terminal now stops only when its session expires (also in [5.0.1][hopsworks-5-0-1]).
- Fixed environment builds against the managed Docker registry ignoring `hopsworks.variables.docker_operations_push_insecure` and failing on a self-signed certificate; set the new `hopsworks.variables.docker_operations_registry_http` to `"true"` for a registry served over plain HTTP (also in [5.0.1][hopsworks-5-0-1]).
- Fixed project membership changes being slow, and Airflow requests timing out or failing with server errors, when Airflow is turned off (`global._hopsworks.airflow.enabled: false`) (also in [5.0.1][hopsworks-5-0-1]).
- Fixed `pip install` and `uv pip install` in the web terminal, and `uv pip install` in Jupyter and Ray, ignoring the index, mirror and proxy settings in `hopsworks.dockerImage.pypi.global_parameters` (also in [5.0.2][hopsworks-5-0-2]).
- Fixed deleting a feature group failing after many online ingestions; Hopsworks now keeps the latest 1000 online ingestions of each feature group (cluster variable `online_ingestion_max_per_featuregroup`) (also in [5.0.2][hopsworks-5-0-2]).
- Fixed Arrow Flight queries of partitioned DELTA feature groups failing once the feature group is older than `delta.logRetentionDuration` (also in [5.0.8][hopsworks-5-0-8]).
- Fixed offline reads of a feature view or query that includes a spine group failing with an HTTP 500 error (also in [5.0.13][hopsworks-5-0-13]).
- Fixed reads of external feature groups failing after features were appended (also in [5.0.14][hopsworks-5-0-14]).
- Fixed Snowflake reads through the Hopsworks Query Service ignoring the role of the data source (also in [5.0.14][hopsworks-5-0-14]).
- Fixed DLT ingestion rejecting a load whose decimal values are narrower than the precision of the source column (also in [5.0.14][hopsworks-5-0-14]).
- Fixed writes to an online feature group failing after its table was truncated (also in [5.0.10][hopsworks-5-0-10]).
- Fixed the project home page crashing with "Something went wrong while loading this page" because of the Feature usage card (also in [5.0.10][hopsworks-5-0-10]).
- Fixed the deployment test, the endpoint addresses and code snippets of deployments, and their metrics dashboard using the project name instead of its Kubernetes namespace, which broke them on clusters with pre-created namespaces.
- Fixed the Kyverno restricted policies blocking schema fetches of REST and CRM data sources.
- Fixed enabling feature logging failing with a duplicate column on feature views with two serving keys from one feature group, or with an event time as a serving key.
- Fixed a read from an unreachable data source blocking with nothing logged; it now fails after 180 seconds (cluster variable `arrow_flight_read_timeout_as_ms`) with an error that names the data source.
- Fixed `kubectl` failing in every web terminal, because terminals never got a kubeconfig (also in [5.0.10][hopsworks-5-0-10]).
- Changed LLM deployments to no longer get the inference logger sidecar, which they never used (also in [5.0.2][hopsworks-5-0-2]).
- Fixed updating a deployment's transformer script to a full HopsFS path failing with script not found.
- Fixed deleting a user right after deleting their projects failing with a generic error; it now returns a conflict that says to retry.
- Fixed the web terminal retrying a session that had shut down on its timeout instead of offering to restart it, and a generic `Error occurred.` message after the computer woke from sleep.
- Fixed the BigQuery data source form accepting a missing BigQuery project, which then failed when creating a feature group.
- Fixed the "HDFS Bytes Written" panel of the Spark Grafana dashboard showing bytes read, and the REST API latency panel of the project metrics page showing no data.
- Fixed giving project members access to Superset failing with HTTP 429 (Too Many Requests) errors (also in [5.0.1][hopsworks-5-0-1]).
- Fixed Superset redirecting to its internal host behind a reverse proxy that rewrites the Host header; set `hopsworks.variables.hopsworks_public_proxy_url` to the public `host[:port]` (also in [5.0.1][hopsworks-5-0-1]).
- Fixed failed or partly deleted projects counting against the owner's maximum number of projects (also in [5.0.1][hopsworks-5-0-1]).
- Fixed ingestion with dltHub and schema fetching from NoSQL data sources failing when the project, data source or table names are long (also in [5.0.1][hopsworks-5-0-1]).
- Fixed project pages showing a "Feature not enabled: DATA_SCIENCE_PROFILE" error when the data science profile is off; the model registry, deployments and apps are now hidden from the menu (also in [5.0.1][hopsworks-5-0-1]).
- Fixed saving the Alertmanager configuration in the admin UI silently failing when it sets a boolean or numeric option, such as `smtp_require_tls` or `max_alerts` (also in [5.0.2][hopsworks-5-0-2]).
- Fixed the data preview of a feature view's logging feature group failing (also in [5.0.2][hopsworks-5-0-2]).
- Fixed the create and edit forms of model and LLM deployments: a hidden tracing field could block saving, the vLLM image tag could stay blank, and editing a deployment reset its resources (also in [5.0.6][hopsworks-5-0-6]).
- Fixed feature monitoring charts not showing the standard deviation (also in [5.0.6][hopsworks-5-0-6]).
- Fixed the **SQL Runner** returning a different number of rows on each run, ignoring the row limit for some queries and discarding the typed query when the limit changed; it now shows the row count of a result (also in [5.0.8][hopsworks-5-0-8]).
- Fixed Superset queries through Trino logging `Access Denied: Cannot access catalog system`, and project creation and new project members logging Trino `Access Denied: Invalid credentials` errors before their Superset connection is ready (also in [5.0.8][hopsworks-5-0-8]).
- Fixed project members with the Observer role being offered Superset actions that fail; the UI now disables them (also in [5.0.8][hopsworks-5-0-8]).
- Fixed init containers without requests and limits being charged a namespace `LimitRange` default for the whole life of the pod; the RonDB and Consul charts are not covered yet (also in [5.0.9][hopsworks-5-0-9]).
- Fixed feature statistics failing to save when a column has a NaN or infinite statistic, such as the standard deviation of an all-null column (also in [5.0.9][hopsworks-5-0-9]).
- Fixed the state of a Spark or Ray job execution switching between queued and running while one of its pods couldn't be scheduled (also in [5.0.9][hopsworks-5-0-9]).
- Fixed the KServe local model controller image (`kserve.kserve.localmodel.enabled`) failing to pull (also in [5.0.9][hopsworks-5-0-9]).
- Fixed Git operations failing to authenticate when a provider token or password contains special characters (also in [5.0.10][hopsworks-5-0-10]).
  The upgrade converts the saved credentials; if a provider still fails, save it again in your account settings.
- Fixed creating or editing a BigQuery data source failing with a gRPC error when the form lists the GCP projects (also in [5.0.10][hopsworks-5-0-10]).
- Fixed the OpenSearch metrics exporter reporting the parent cluster on a satellite deployment, and missing OpenSearch with a custom `global._hopsworks.consulDomainName` (also in [5.0.13][hopsworks-5-0-13]).

### Breaking changes

- `helm uninstall` now deletes the data volumes of the HopsFS DataNodes, MinIO, OpenSearch, Kafka, Consul and the remote shuffle service, for good, instead of keeping them (also in [5.0.2][hopsworks-5-0-2]).
  To keep them, set `global._hopsworks.wipeDataOnUninstall: false` or label the PVCs `hopsworks.ai/keep=true` before you uninstall; the Superset MySQL volume is deleted regardless.
- OpenSearch drops vectors not yet flushed and rejects vector writes for about two minutes on its first start on 5.1, because of the default `olk.opensearch.knn.circuit_breaker` settings; set `triggered: false` and `percent: 75` under it, or upgrade to [5.1.1][hopsworks-5-1-1] instead.
- Rebuild the environment images built from custom commands or with libraries from a private Git repository, and rotate the credentials in `hopsworks.dockerImage.packageAuth.secretName` and the Git tokens they use, to address a vulnerability.
- Raised the minimum Kubernetes version from 1.27 to 1.34; upgrade Kubernetes first, because Helm refuses to install or upgrade on an older cluster.
- Every `helm upgrade`, including values-only ones, now rebuilds the feature store search index afterwards, which the 5.0 chart never did, signing in with `hopsworks.variables.admin_email` and `hopsworks.variables.admin_password`, and fails the upgrade if they don't sign in to the Hopsworks admin account.
  Set them to the admin account's credentials before you upgrade; if password login is disabled, upgrade to [5.1.1][hopsworks-5-1-1] instead.
- The Airflow migration Job now waits for the DDL MySQL server, instead of any MySQL server, so the upgrade hangs with `rondb.rondb.meta.ddlMySQLd.enabled: false` (also in [5.0.13][hopsworks-5-0-13]).
  Keep it enabled if you use Airflow.
- Init containers now set CPU and memory requests and limits, which most of them used to leave unset (also in [5.0.9][hopsworks-5-0-9]).
  If a namespace `LimitRange` has a `min` or `max` they don't fit, set `global._hopsworks.initContainerResources` before you upgrade, or Kubernetes rejects the pods.
- The admin liveness and startup probes now have a default `exec` handler, instead of no probe, so a probe you set with `httpGet` or `tcpSocket` also needs `exec: null`, or Kubernetes rejects the pod (also in [5.0.3][hopsworks-5-0-3]).
  This needs Helm 4 or Helm 3.17.1 or later, because older Helm 3 releases ignore a `null` for a subchart value.
- Removed Brewer; remove `global._hopsworks.brewer`, `brewer`, `hopsworks.ingress.brewer`, `hopsworks.variables.brewer_*` and `hw-kyverno.policyExceptions.brewer` from your values, because the values schema rejects them.
  With `--reuse-values`, which keeps the 5.0 defaults such as `brewer`, use `--reset-then-reuse-values`.
- Removed `hopsworks.variables.hive_default_quota` and `hopsworks.variables.enable_conda_install`; remove them from your values, because the values schema rejects them.
- The consul-k8s chart fails to render with `disable_hostname` in `consul.consul.server.extraConfig`, where the 5.0 chart set it; remove it, because `consul.consul.global.metrics.disableAgentHostName` (default `true`) replaces it.
  With `--reuse-values`, which keeps the 5.0 default `extraConfig`, use `--reset-then-reuse-values`.
- The chart fails to render with `hopsworks.hopsfsMount.enabled: false`, because the new Trino mountable-secrets sidecar needs the HopsFS mount.
  Set `global._hopsworks.trino.mountableSecrets.enabled: false`, and override `trino.trino.initContainers` and `trino.trinotest.initContainers.coordinator` without the `mountable-secrets` container, as `values.openshift.yaml` does.
- Removed the Kafka quota defaults Job, which applied `kafka.cluster.kafka.quotas.defaults` to each client, so it is ignored with `type: strimzi`, and fails the render with `type: kafka` when `enabled` is `true` (also in [5.0.13][hopsworks-5-0-13]).
  If you set it, move your limits to `kafka.cluster.kafka.quotas.strimzi` or `kafka.cluster.kafka.quotas.kafka`, with new numbers: the `strimzi` rates are a total per broker, shared by all clients.
- `quotas` on a user in `kafka.users` now fail the render under the default `strimzi` plugin, which never enforced them (also in [5.0.13][hopsworks-5-0-13]).
  Remove them, or set `kafka.cluster.kafka.quotas.type: kafka`, `kafka.cluster.kafka.quotas.minAvailableRatioPerVolume: 0` and `kafka.cluster.kafka.authorizer.principalBuilderClass: ""` to enforce them.
- Removed `hopsworks.variables.jupyter_spark_driver_memory_overhead_factor`, added in 5.0.10; the driver memory overhead of a notebook now comes from its Spark configuration (also in [5.0.12][hopsworks-5-0-12]).
  Remove it from your values before you upgrade, because the values schema rejects it; with `--reuse-values`, which keeps the old default, use `--reset-then-reuse-values`.
- 5.1.0 came out before [5.0.14][hopsworks-5-0-14] and lacks most of its changes, such as the addressed vulnerabilities in jobs; if you run 5.0.14, upgrade to [5.1.2][hopsworks-5-1-2] or later instead.
- 5.1.0 ships an older RonDB chart than [5.0.13][hopsworks-5-0-13], without `rondb.rondb.rdrs.probes`, so the RonDB REST server restarts again during a data node failure; if you run 5.0.13, upgrade to [5.1.1][hopsworks-5-1-1] or later instead.
- `catalog-volume` moved from `trino.trino.configMounts` to the `additionalVolumes` and `additionalVolumeMounts` of `trino.trino.coordinator` and `trino.trino.worker`.
  If you override these lists, copy both entries from the chart's values and remove `catalog-volume` from an overridden `trino.trino.configMounts`, or the Trino pods don't start.
- Trino pods now run as the `hopsworks-trino` and `hopsworks-trino-test` ServiceAccounts instead of `default`; move anything you attached to `default` for Trino, such as a cloud identity annotation or an OpenShift SCC.
- Spark is upgraded from 3.5 to 4.1, which is built for Scala 2.13; rebuild job JARs built for Scala 2.12, and check your jobs against the [Spark migration guide](https://spark.apache.org/docs/latest/migration-guide.html).
- Removed library installs from a conda channel, an `.egg` file or an `environment.yml` file, because the base environments are now uv virtualenvs without conda; use pip, a wheel, a Git repository, a `requirements.txt` file or custom commands instead ([installing libraries](https://docs.hopsworks.ai/5.1/user_guides/projects/python/python_install/)).
- Hopsworks now rejects a KServe deployment that sets the `PYTHONPATH` environment variable, which 5.0 accepted and KServe 0.19 blocks; remove it from your deployments.
- Prometheus is upgraded from 2.51 to 3.14; check custom alert rules and scrape configs against the [Prometheus 3 migration guide](https://prometheus.io/docs/prometheus/latest/migration/).
- Knative request metrics are now `http_server_request_duration_seconds` instead of `revision_request_count` and `revision_request_latencies`, with new label names, and Spark metrics have new names; update custom Grafana dashboards and alert rules.
- `vpa.image.tag` is now the version of the VPA installer image (default `"1.7.1-2"`), separate from `vpa.imagesTag`; remove any override of it, including the `"1.7.1"` that [5.0.8][hopsworks-5-0-8] asked for, and upgrade with `--reset-then-reuse-values` instead of `--reuse-values`, which keeps the old value.
- Filebeat now keeps only the Kubernetes labels listed under `olk.filebeat.kubernetesMetadata`, and the `serviceLabelKey` of each `olk.logstash.extendServicesPipeline` entry, on service logs, instead of every pod label (also in [5.0.12][hopsworks-5-0-12]).
  Add any other label you filter on to `olk.filebeat.kubernetesMetadata.extraPodLabels`, `extraNamespaceLabels` or `extraNodeLabels`; an overridden `olk.filebeat.logs_locations` keeps its own `add_kubernetes_metadata` processor and every label, so to get the fix set `addKubernetesMetadata: true` on each entry and drop that processor.
- Removed the Code Style, Testing and Security rules from the Coding Agents page of the cluster settings, and web terminals no longer give them to the coding agents (also in [5.0.10][hopsworks-5-0-10]).
  If you set them, move what you need to the new Business Glossary or the system-wide instructions of each agent.
- `hopsworks.variables.enable_read_only_git_repositories` now defaults to `false` instead of `'true'`, so users can commit and push from Git repositories in Hopsworks; to keep them read-only, set it to `'true'` before you upgrade.
- Feature monitoring is now on by default, instead of off, and the upgrade writes `hopsworks.variables.enable_feature_monitoring` to the cluster, replacing a value set in the admin UI (also in [5.0.1][hopsworks-5-0-1]).
  To keep it off, set it to `'false'` before you upgrade.

### Deprecations

- Deprecated `kserve.istio.gateways.http10` for `kserve.istio.gateways.ingress.http10`; the old key, ignored in 5.0, works again.
- Deprecated `kafka.cluster.kafka.quotas.defaults`, which is no longer honoured; see the breaking changes above (also in [5.0.13][hopsworks-5-0-13]).
- Deprecated `hopsworks.envs.postInstall.DEPLOY_RETRIES`, which has no effect now that the admin sidecar retries until the deployment succeeds (also in [5.0.3][hopsworks-5-0-3]).
- Deprecated `grafana.grafana.dashboardsConfigMaps`, which the chart leaves empty now that its dashboards ship in the Grafana image.

### Upgrade steps

No upgrade steps are listed for this release.

### Upgraded components

| Component | 5.0.0 | 5.1.0 |
| --------- | ----- | ----- |
| Airflow image | 5.0.0 | 5.1.0 |
| Alertmanager | v0.27.0 | 0.34.0-alpine-h1.1 |
| ArrowFlight server | 5.0.0 | 5.1.0 |
| Base environment images | 5.0.0 | 5.1.0 |
| BuildKit | v0.14.1 | v0.32.2 |
| cert-manager | v1.11.1 | v1.21.1 |
| Certificates operator | 0.3.2 | 0.4.0 |
| Consul | 1.16.3 | 1.16.4-alpine-h1 |
| consul-k8s | 1.3.1 | 1.8.16 |
| Docker registry | 2.8.3 | 3.1.1 |
| Filebeat | 8.15.0 | 8.19.21 |
| Git image | 1.4 | 1.5 |
| Grafana | 10.2.2-h6 | 12.4.9-h9 |
| Hive Metastore | 3.0.0.14.5-v1 | 4.1.0.0-v1 |
| HopsFS | 3.4.3.1-EE-RC0 | 3.4.3.3-EE-RC0 |
| Hudi bundle of the Hive Metastore | 0.12.3.0 | 1.2.0 |
| Image builder | 0.1 | 0.2 |
| Inference logger | 5.0.0 | 5.1.0 |
| Istio | 1.20.3 | 1.29.7 |
| Kafka | 3.9.1 | 3.9.2 |
| Knative Serving | v1.13.1 | v1.23.0 |
| KServe | v0.14.0-rc1 | v0.19.0 |
| KServe utilities | 0.1.4 | 0.1.10 |
| KubeRay operator | v1.4.0 | 1.4.0-h1 |
| Logstash | 7.17.9.4 | 7.17.29.6 |
| Model serving authenticator | 5.0.0 | 5.1.0 |
| Model serving webhook | 5.0.0 | 5.1.0 |
| MySQL Connector/J | 8.0.21.0 | 8.0.21.1 |
| OnlineFS | 2.3 | 2.4 |
| OpenSearch | 1.3.6.2 | 2.19.6.3 |
| OpenSearch Dashboards | 1.3.6.6 | 2.19.6.7 |
| OpenSearch metrics exporter | v1.7.0 | 1.11.0-alpine-h1.1 |
| Payara | 6.2024.12-jdk17.6 | 6.2025.11-jdk21.0 |
| Prometheus | v2.51.2 | 3.14.0-alpine-h1.1 |
| Prometheus adapter | v0.12.0 | 0.12.0-alpine-h1.1 |
| Prometheus config reloader | v0.70.0 | 0.93.1-alpine-h1.1 |
| Pushgateway | v1.8.0 | 1.11.3-alpine-h1.1 |
| Remote shuffle service (Apache Uniffle) | 0.10.7 | 0.11.1 |
| Remote shuffle service init image | 0.9.1 | 0.9.2 |
| RonDB | 26.02.4 | 26.02.10 (also in [5.0.11][hopsworks-5-0-11]) |
| RonDB MySQL metrics exporter | 0.11.4 | 0.11.5 (also in [5.0.1][hopsworks-5-0-1]) |
| scikit-learn model server | 0.14.1 | 0.19.1 |
| Spark | 3.5.5.1 | 4.1.3.0 |
| Spark history server | 3.5.5.1 | 4.1.3.0 |
| Spark operator | 2.2.1-h4 | 2.5.1-h1 |
| Storage initializer | 5.0.0 | 5.1.0 |
| Strimzi | 0.45.1-h4 | 0.45.2-h1 |
| Superset | 6.0.0p2.4 | 6.0.0p4.4 |
| Superset init image | dockerize | 0.14.0-alpine-h1.1 (also in [5.0.14][hopsworks-5-0-14]) |
| Superset MySQL | 8.4.5-debian-12-r0-h1 | 8.4.11-ubuntu24.04-h4 |
| Superset MySQL metrics exporter | 0.17.2-debian-12-r7 | 0.20.0-alpine-h1.1 (also in [5.0.14][hopsworks-5-0-14]) |
| Superset MySQL volume permissions image | 12-debian-12-r43 | 12-alpine-h1.1 (also in [5.0.14][hopsworks-5-0-14]) |
| Superset Redis | 7.4.9-bookworm | 7.4.11-alpine-h1 |
| Superset Redis metrics exporter | 1.50.0-debian-11-r1 | 1.90.0-alpine-h1.1 (also in [5.0.14][hopsworks-5-0-14]) |
| TensorFlow | 2.19.0 | 2.20.0 |
| TensorFlow Serving | 2.19.0 | 2.20.0 |
| Toolbox image (hwutils) | 1.7 | 1.9 |
| Trino | 480-v6 | 480-v10 |
| Vertical Pod Autoscaler | 1.2.1 | 1.7.1 (also in [5.0.8][hopsworks-5-0-8]) |
| Vertical Pod Autoscaler installer | 1.2 | 1.7.1-2 |

### Configuration changes

- Changed `hopsworks.variables.docker_operations_buildkit_extra_args` to empty by default, dropping the S3 build cache arguments that failed without S3 credentials; set them again to keep an S3 build cache.
- Changed the default `kserve.kserve.controller.deploymentMode` from `Serverless` to `Knative`, its KServe 0.19 name.
- Added `rondb.rondb.timeoutsMinutes.ndbmtdStartupProbe` and `rondb.rondb.timeoutsMinutes.mysqldStartupProbe`, the startup probe timeouts of the RonDB data nodes and MySQL servers, and raised them from 25 to 120 minutes and from about 17 to 20 minutes (also in [5.0.5][hopsworks-5-0-5]).
- Changed `rondb.rondb.timeoutsMinutes.ndbmtdStartupProbe` to 240 minutes, from 120, so data nodes that take over two hours to reload aren't restarted in a loop (also in [5.0.11][hopsworks-5-0-11]).
- Changed the default `spark.rss.shuffleServer.bufferCapacityRatio` to `0.6` and `spark.rss.shuffleServer.resources.limits.cpu` to `2000m` (also in [5.0.12][hopsworks-5-0-12]).
- Changed `hopsworks.variables.docker_operations_timeout_listing_minutes`, `docker_operations_timeout_check_minutes` and `docker_operations_timeout_export_minutes` from 5 to 15 minutes, and `max_concurrent_base_sync_ops` from 6 to 5, so large base images finish syncing (also in [5.0.9][hopsworks-5-0-9]).
- Changed the Superset init image to its own `superset/dockerize` repository, also in `values.airgap.yaml` (also in [5.0.14][hopsworks-5-0-14]).
- Fixed users added to `rondb.rondb.mysql.users` after the install never being created, and users with privileges on a single database or table failing; every upgrade now creates the listed users (also in [5.0.11][hopsworks-5-0-11]).
- Fixed the values schema rejecting a cron string in `hopsworks.velero.backup.schedule`.
- Fixed the chart failing to render with `hopsworks.dropDatabase: true` (also in [5.0.9][hopsworks-5-0-9]).
- Added `spark.sql.ansiEnabled` (default `false`), so SQL keeps returning null on overflow and invalid casts on Spark 4.1, as on Spark 3.5.
- Added `hopsworks.dockerImage.pypi.pythonDownloads` (default `never`), so uv never downloads a Python interpreter during environment builds.
- Added `rondb.rondb.mysql.exporter.maxOpenConnections` (default `1`), the connections of the RonDB MySQL metrics exporter; the render fails if it exceeds `rondb.rondb.mysql.exporter.maxUserConnections` (also in [5.0.1][hopsworks-5-0-1]).
- Added `kafka.cluster.clusterCa.validityDays` and `kafka.cluster.clientsCa.validityDays` (default `365`) for the certificates Strimzi issues, applied at the next issuance (also in [5.0.10][hopsworks-5-0-10]).
- Added `kafka.cluster.kafka.quotas.type` to choose the Kafka quota plugin: `strimzi` (the default), set under `kafka.cluster.kafka.quotas.strimzi`, or `kafka`, which enforces per-user quotas from `kafka.users[].quotas` and defaults from `kafka.cluster.kafka.quotas.kafka` (also in [5.0.13][hopsworks-5-0-13]).
  `kafka` also needs `kafka.cluster.kafka.quotas.minAvailableRatioPerVolume: 0`, per-user quotas need `kafka.cluster.kafka.authorizer.principalBuilderClass: ""`, which changes how ACLs and `superUsers` match principals, and none of these settings take effect on clusters first installed on Hopsworks 4.3 or 4.5.
- Added `cleanupOnUninstall.enabled` to each component chart, such as `hopsworks.cleanupOnUninstall.enabled`, and `certs-operator.gracefulCertTeardown.enabled`, to turn off the uninstall cleanup of that component (also in [5.0.2][hopsworks-5-0-2]).
- Added `hopsworks.jupyter.notebookConfig.enableUploads`; set it to `false` to block file uploads from the Jupyter UI and base64 uploads through the Jupyter Contents API (also in [5.0.8][hopsworks-5-0-8]).
- Added `global._hopsworks.initContainerResources` (`waiter`, `tool`, `runtime`) to size the requests and limits that init containers now set (also in [5.0.9][hopsworks-5-0-9]).
- Added `rondb.rondb.ndbmtdSequencedRollout.enabled` (default `false`) to roll the RonDB data nodes one node group at a time, on clusters with more than one node group (also in [5.0.5][hopsworks-5-0-5]).
- Added `hive.externalLoadBalancer.enabled` (default `false`) to expose the Hive Metastore outside Kubernetes, for example to external Spark applications (also in [5.0.1][hopsworks-5-0-1]).
- Added `hopsworks.velero.backup.storageLocation.s3ForcePathStyle` for S3-compatible backup stores that need path-style addressing (also in [5.0.1][hopsworks-5-0-1]).
- Added `hopsfs.objectStorage.s3.disableCertChecking` and `hopsfs.objectStorage.s3.disableChecksumValidation` to turn off TLS certificate checks and client-side checksum validation for the HopsFS S3 endpoint (also in [5.0.3][hopsworks-5-0-3]).
- Added `hopsworks.variables.docker_operations_lock_dependencies`, `docker_operations_allow_hermetic_custom_commands` and `docker_operations_multi_region_copy`, off by default, for hash-locked build dependencies, cached hermetic custom commands and image copies to the second region.
- Added cluster variables for the default CPU, memory and GPU of new jobs and Python apps, such as `hopsworks.variables.spark_job_executor_memory`.
- Added `hopsworks.variables.pushgateway_group_ttl_minutes`, `pushgateway_monitor_interval_ms` and `pushgateway_cleaner_batch_size` to clean stale Pushgateway metric groups.
- Added `kserve.knative.imageRegistry` for the Knative images.
- Added `olk.opensearch.audit.enabled` (default `false`) and `olk.opensearch.audit.retentionDays` for OpenSearch security audit logs.
- Added `global._hopsworks.trino.egressProbe.echoUrl` to show which IP addresses an external database must allow.
- Added `olk.opensearch.security.default_tenant` (default `Private`), the tenant OpenSearch Dashboards opens in.
- Added `kserve.kserve.servingruntime.vllmopenai.imageRegistry` and `kserve.kserve.servingruntime.vllmomni.imageRegistry` to pull the vLLM images from a mirror (also in [5.0.1][hopsworks-5-0-1]).
- Added `rondb.rondb.rondbConfig.UseTcInRRGroup` and `rondb.rondb.rondbConfig.MaxRRGroupSize` to tune the RonDB round-robin groups (also in [5.0.1][hopsworks-5-0-1]).
- Added `hopsworks.envs.postInstall.DEPLOY_RETRY_INTERVAL_SEC`, `ASADMIN_TIMEOUT_SEC` and `ASADMIN_DEPLOY_TIMEOUT_SEC` to tune how the admin sidecar retries the Hopsworks deployment (also in [5.0.3][hopsworks-5-0-3]).
- Added `hopsworks.service.worker.external.https.nodePort` to pin the node port of the Hopsworks HTTPS service when its `type` is `NodePort` (also in [5.0.4][hopsworks-5-0-4]).
- Added `docker-registry.affinity`, `minio.affinity` and `hopsworks.dockerRegistry.preset.affinity` for the Docker registry, MinIO and the preset image push Job (also in [5.0.6][hopsworks-5-0-6]).
- Added `rondb.rondb.mysql.users[].existingSecret` to read the password of a MySQL user from your own Secret (also in [5.0.11][hopsworks-5-0-11]).
- Added `onlinefs.deployment.strategy` to set the rollout strategy of OnlineFS (also in [5.0.13][hopsworks-5-0-13]).

[docs-sql-runner]: https://docs.hopsworks.ai/5.1/user_guides/projects/trino/query_engine/#sql-runner
[docs-trino-history]: https://docs.hopsworks.ai/5.1/setup_installation/admin/trino/#query-history
[values-olk-index-upgrade]: https://docs.hopsworks.ai/5.1/setup_installation/common/helm_chart_values/olk/#helm.olk.opensearch.indexUpgrade.mode
