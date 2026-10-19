---
releases:
  "5.1.2":
    released: "2026-10-16"
    application: "5.1.2"
    python_client: "5.1.2"
  "5.1.1":
    released: "2026-10-09"
    application: "5.1.1"
    python_client: "5.1.1"
  "5.1.0":
    released: "2026-09-24"
    application: "5.1.0"
    python_client: "5.1.0"
---

# Release notes { #hopsworks-5-1 }

The releases of Hopsworks 5.1, newest first.

## 5.1.2 { #hopsworks-5-1-2 }

### What's changed

- Fixed a security issue in OpenSearch.
  The fix applies once an OpenSearch pod logs `Security configuration applied` after the upgrade; if none does, run `run_security_admin.sh` as the chart's `README.md` shows.
- Fixed every OpenSearch restart deleting the OpenSearch roles of restricted-access grants and feature group shares, and every `helm upgrade` restarting OpenSearch.
  Grants and shares made before the last OpenSearch restart on 5.1.0 or 5.1.1 lost their roles, and granting or sharing again is refused: revoke and grant again, or unshare and share again.
- Fixed security vulnerabilities in the Hopsworks certificate authority, Grafana, Filebeat and Superset images, and in the MySQL and Redis of Superset.
- Added an opt-in Job that copies the OpenSearch indices created before OpenSearch 2.0 during a 5.1 upgrade, in a window you pick, so the upgrade to 5.2.1 or later has nothing left to copy; set `olk.opensearch.indexUpgrade.mode` to `report` to list them, or to `copy` ([values][values-olk-index-upgrade]).
  Turn vector ingestion off in an upgrade of its own first (`onlinefs.deployment.vectordb.enabled: false`), and pass the mode with `--set`, not in your values file, because 5.2.1 and later read the same key.
- Changed the SQL Runner of the Query Engine page to fill the page, show row numbers and column types in the results, list a table's columns in the Explorer and draw `EXPLAIN (FORMAT GRAPHVIZ)` plans as a graph ([SQL Runner][docs-sql-runner]).
- Fixed queued service operations failing on every retry when they removed a user from Superset or set up a project Observer's online feature store connection in Superset, and stopping for good after 68 failed attempts; a failing operation now retries once a day.
- Fixed the SQL Runner leaving a query running when you leave it right after starting the query, and its autocompletion offering no column names in `WHERE`, `GROUP BY` or join conditions.

### Configuration changes

- Changed the default of `hopsworks.variables.trino_events_cleaner_batch_size` from 1000 to 100.

### Breaking changes

- If your values restate `trino.trino.additionalConfigProperties` with its `event-listener.config-files` entry, remove that entry or add the listener files as the chart's `README.md` shows, or Trino doesn't start.
- Recorded Trino queries now lose their query text, plan and JSON details after `hopsworks.variables.trino_events_strip_details_after_days` (`7`), and the first nightly cleanup after the upgrade strips every older one; set it to `61` or more to keep them.
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

## 5.1.1 { #hopsworks-5-1-1 }

### What's changed

- Fixed a security issue in jobs.
- Fixed OpenSearch losing unflushed vectors and rejecting vector writes for about two minutes on its first start on 5.1; `olk.opensearch.knn.circuit_breaker.triggered` now defaults to `false` and `percent` to `75`.
  A values file that sets `triggered: true` or `percent: 0.75`, or an upgrade with `--reuse-values`, keeps the problem.
- Fixed the database migration of the upgrade from 5.0 failing when the feature groups have more than about 32,000 features in total.
- Fixed the post-upgrade search index rebuild failing without the admin password, for example when password login is disabled, and running on every upgrade; it now runs in the background once per index format, and shows its progress and a **Reindex now** button under **Cluster settings > Service Operations > OpenSearch Index Commands**.
  The first upgrade to 5.1.1 rebuilds the index, and search is incomplete until it finishes.
- Fixed RonDB daemons ignoring SIGTERM, so every pod stop ended in a kill and a stopped data node could stall the cluster.
- Changed the RonDB REST server probes to outlast a data node failure and to use their own port.
- Fixed the RonDB REST server reading request bodies over 64 KiB as empty; it now buffers them in `rondb.rondb.rdrs.uploadPath`.
- Fixed environment builds never starting when `rondb.rondb.priorityClass` is renamed; `hopsworks.variables.docker_operations_buildkit_priority_class` now defaults to empty, so builds run at the default priority and no longer preempt other pods.
- Fixed Trino giving a project access to only one of several feature stores shared with it.
- Fixed a killed Spark job with pending executors staying in the aggregating logs state for up to 20 minutes.
- Fixed the **Why?** button of an online ingestion in a feature group's activity opening every OnlineFS log of the project instead of that ingestion's; it is now named **Logs**.

### Configuration changes

- Changed `rondb.rondb.terminationGracePeriodSeconds` to one value per component, and the data nodes' default from 60 to 300 seconds; an integer still sets only the data nodes.
- Fixed `values.openshift.yaml` for the OpenShift `restricted-v2` SCC, covering Strimzi, Kafka, ZooKeeper, the Spark operator and the MySQL and Redis of Superset, and turned off the Prometheus node exporter, which OpenShift ships itself.
  Use it with Helm 4 or Helm 3.17.1 or later, because older Helm 3 releases ignore its `null` overrides of subchart values.
- Fixed the values schema rejecting `hopsworks.variables.loadbalancer_external_domain_namenode` and `hopsworks.variables.loadbalancer_external_domain_datanode`.
- Added `hopsworks.opensearchReindex.enabled` to turn off the post-upgrade search index rebuild, and `hopsworks.variables.command_search_fs_reindex_queue_wait_as_ms` to bound its wait for the search command queue.
- Added `rondb.rondb.rdrs.probes` and `rondb.rondb.rdrs.probePort`, the settings and the port of the RonDB REST server probes, and `rondb.rondb.rdrs.maxKeepaliveRequests` to close a keep-alive connection after that many requests, so clients rebalance after a rolling restart.
- Added `nodePort` values to pin the node ports of unmanaged external load balancers: ArrowFlight, OpenSearch, the HopsFS NameNode and DataNodes, Trino, the Hive Metastore, Kafka (`bootstrapNodePort`, `startingNodePort`) and the RonDB MySQL and REST servers.
  The RonDB ones ignore `global._hopsworks.externalLoadBalancers.managed` and apply only when `rondb.rondb.meta.mysqld.externalLoadBalancer.managed` or `rondb.rondb.meta.rdrs.externalLoadBalancer.managed` is `false`.
- Added `rondb.rondb.rdrs.ttlPurge.enable` and `activeWindow` to turn off the TTL purge of the RonDB REST server or limit it to a daily window.

### Breaking changes

- The post-upgrade search index rebuild signs in as the agent user, and fails the `helm upgrade` if `hopsworks.agent_email` and `hopsworks.agent_password` (default `agent@hops.io`, `admin`) don't match that account.
  Set them, or turn the rebuild off with `hopsworks.opensearchReindex.enabled: false`.
- The RonDB REST server now uses a probe port and an upload path that need RonDB 26.02.11.
  If you pin `rondb.rondb.images.rondb.tag` to an older version, set `rondb.rondb.rdrs.probePort.enabled: false` and `rondb.rondb.rdrs.uploadPath: ""`, or the REST server doesn't start.

### Upgraded components

| Component | 5.1.0 | 5.1.1 |
| --------- | ----- | ----- |
| Base environment images | 5.1.0 | 5.1.1 |
| RonDB | 26.02.10 | 26.02.11 |
| Trino | 480-v10 | 480-v11 |

## 5.1.0 { #hopsworks-5-1-0 }

5.1.0 also includes the changes of [5.0.1][hopsworks-5-0-1] to [5.0.13][hopsworks-5-0-13], which are listed under those releases, except the configurable RonDB REST server probes of 5.0.13 (`rondb.rondb.rdrs.probes`), which return in [5.1.1][hopsworks-5-1-1].

### What's changed

- Fixed a security issue in model serving.
- Fixed a security issue in environment images.
- Fixed security vulnerabilities in the Hopsworks server dependencies and in the Superset, Grafana, Prometheus, Consul, certificates operator, Docker registry, BuildKit, Istio, Knative Serving, KServe utilities, scikit-learn model server, Strimzi, OpenSearch, Logstash and Filebeat images.
- Changed model deployments, jobs, Jupyter servers and terminals to each get their own serving API key.
- Fixed database migrations crash-looping on a lock left by a transient Kubernetes API error, and restarting once on every fresh install.
- Fixed Velero backups leaving out the Trino authentication Secrets, and the Velero storage location rejecting AWS S3 without a custom endpoint.
- Fixed OpenSearch snapshot restores never finishing on single-node clusters, and indices staying closed after a failed restore.
- Fixed every model deployment failing when the Knative controller started with an empty registry certificate.
- Fixed image pulls from the in-cluster Docker registry failing with `x509: certificate signed by unknown authority`, for example on RHEL-family nodes.
- Added Apache Iceberg as a feature group table format (`time_travel_format="ICEBERG"`), also for feature groups created from Iceberg tables in a data source ([table format](https://docs.hopsworks.ai/5.1/user_guides/fs/feature_group/create/#table-format)).
- Added partition transforms (`partitioned_by`) for Iceberg and Hudi feature groups, Delta liquid clustering (`clustered_by`), Hudi bucket indexes (`bucket_index`), z-ordering (`zorder_by`) and Iceberg sort orders (`sort_order`) ([partitioning](https://docs.hopsworks.ai/5.1/user_guides/fs/feature_group/partitioning/)).
- Added Trino catalogs that project Data Owners create by hand or from a data source; Trino loads them at its daily scheduled restart (02:00 by default, only when a change is pending) or when an administrator restarts it, and tests them on a single-node coordinator (`global._hopsworks.trino.testCoordinator.enabled`) ([Trino catalogs](https://docs.hopsworks.ai/5.1/user_guides/projects/trino/catalogs/)).
- Added file-based credentials, such as Oracle wallets, for user-created Trino catalogs: a project uploads them as mountable secrets, and a privileged sidecar on every Trino pod mounts `/apps/mountable-secrets` from HopsFS read-only ([credential files](https://docs.hopsworks.ai/5.1/setup_installation/admin/trino/#credential-files-a-project-supplies)).
- Added dltHub ingestion jobs that copy several tables of a data source, each into its own feature group with its own settings and resources ([dltHub ingestion](https://docs.hopsworks.ai/5.1/user_guides/fs/feature_group/ingest_with_dlthub/)).
- Added the AWS Glue data source, and the Google Sheets data source, which ingests spreadsheet tabs into feature groups with dltHub ([AWS Glue](https://docs.hopsworks.ai/5.1/user_guides/fs/data_source/creation/glue/)).
- Added tags to jobs and apps, and jobs, models, deployments, apps and agents to search; administrators can inspect and cancel stuck search index commands under **Cluster Settings > Service Operations** ([tags](https://docs.hopsworks.ai/5.1/user_guides/fs/tags/tags/), [search index](https://docs.hopsworks.ai/5.1/setup_installation/admin/search_index/)).
- Added an optional persistent BuildKit daemon (`global._hopsworks.buildkitd.enabled`) that keeps caches between environment builds; each replica requests 8 CPUs, 16Gi of memory and a 100Gi volume ([build performance](https://docs.hopsworks.ai/5.1/setup_installation/admin/build_performance/)).
- Changed environment builds to install libraries with uv when the image has it, to read the library list from the built image instead of starting three more Jobs, and to show the stage of a running build.
- Added npm packages to Python environments, installed globally and on `PATH` for jobs, Jupyter and the terminal; set `hopsworks.variables.npm_registry_url` to install from a registry other than registry.npmjs.org ([installing libraries](https://docs.hopsworks.ai/5.1/user_guides/projects/python/python_install/)).
- Added toolchain caches (`HOPSWORKS_BUILD_CACHE`), layer reuse for scripts that fetch nothing that changes (`HOPSWORKS_BUILD_HERMETIC`) and secret references (`NAME=secret:<secret>`) to custom commands ([custom commands](https://docs.hopsworks.ai/5.1/user_guides/projects/python/custom_commands/#making-custom-command-builds-faster)).
- Added **Auto-redeploy on new commits** to Python apps and agent deployments from a Git repository, which rolls them to each new commit of the tracked branch.
- Added the `dbt-pipeline` environment, with dbt and its Trino and DuckDB adapters, and fixed Jupyter servers on the `agent-job` environment losing their priority class, node affinity and Kueue queue.
- Changed feature group schemas to be read from the Hopsworks database instead of the Hive Metastore; existing feature groups move over in the background after the upgrade.
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
- Added key pair authentication to DLT ingestion from Snowflake and a **Stop** button to the SQL Runner, and fixed Snowflake reads through the Hopsworks Query Service ignoring the role of the data source and reads of external feature groups after features were appended (also in [5.0.14][hopsworks-5-0-14]).
- Fixed the deployment test, the endpoint addresses and code snippets of deployments, and their metrics dashboard using the project name instead of its Kubernetes namespace, which broke them on clusters with pre-created namespaces.
- Fixed Spark jobs failing to reach the remote shuffle service when an evicted coordinator pod was left behind.
- Fixed API keys created by `hops setup` lacking the `KAFKA`, `PYTHON_LIBRARIES`, `GIT`, `TRINO` and `SUPERSET` scopes, so they could not insert into online feature groups.
- Fixed the Kyverno restricted policies blocking schema fetches of REST and CRM data sources.
- Fixed enabling feature logging failing with a duplicate column on feature views with two serving keys from one feature group, or with an event time as a serving key.
- Fixed a read from an unreachable data source blocking with nothing logged; it now fails after 180 seconds (`arrow_flight_read_timeout_as_ms`) with an error that names the data source.
- Fixed updating a deployment's transformer script to a full HopsFS path failing with script not found.
- Fixed deleting a user right after deleting their projects failing with a generic error; it now returns a conflict that says to retry.
- Fixed the web terminal retrying a session that had shut down on its timeout instead of offering to restart it, and a generic `Error occurred.` message after the computer woke from sleep.
- Fixed the BigQuery data source form accepting a missing BigQuery project, which then failed when creating a feature group.
- Fixed the "HDFS Bytes Written" panel of the Spark Grafana dashboard showing bytes read, and the REST API latency panel of the project metrics page showing no data.

### Configuration changes

- Changed `hopsworks.variables.docker_operations_buildkit_extra_args` to empty by default, dropping the S3 build cache arguments that failed without S3 credentials; set them again to keep an S3 build cache.
- Changed the default `kserve.kserve.controller.deploymentMode` from `Serverless` to `Knative`, its KServe 0.19 name.
- Changed the Superset init image to its own `superset/dockerize` repository, also in `values.airgap.yaml` (also in [5.0.14][hopsworks-5-0-14]).
- Fixed the values schema rejecting a cron string in `hopsworks.velero.backup.schedule`.
- Added `spark.sql.ansiEnabled` (default `false`), so SQL keeps returning null on overflow and invalid casts on Spark 4.1, as on Spark 3.5.
- Added `hopsworks.dockerImage.pypi.pythonDownloads` (default `never`), so uv never downloads a Python interpreter during environment builds.
- Added `hopsworks.variables.docker_operations_lock_dependencies`, `docker_operations_allow_hermetic_custom_commands` and `docker_operations_multi_region_copy`, off by default, for hash-locked build dependencies, cached hermetic custom commands and image copies to the second region.
- Added cluster variables for the default CPU, memory and GPU of new jobs and Python apps, such as `hopsworks.variables.spark_job_executor_memory`.
- Added `hopsworks.variables.pushgateway_group_ttl_minutes`, `pushgateway_monitor_interval_ms` and `pushgateway_cleaner_batch_size` to clean stale Pushgateway metric groups.
- Added `kserve.knative.imageRegistry` for the Knative images.
- Added `olk.opensearch.audit.enabled` (default `false`) and `olk.opensearch.audit.retentionDays` for OpenSearch security audit logs.
- Added `global._hopsworks.trino.egressProbe.echoUrl` to show which IP addresses an external database must allow.
- Added `olk.opensearch.security.default_tenant` (default `Private`), the tenant OpenSearch Dashboards opens in.

### Breaking changes

- Rebuild the environment images built from custom commands or with libraries from a private Git repository, and rotate the credentials in `hopsworks.dockerImage.packageAuth.secretName` and the Git tokens they use, for a security fix.
- Raised the minimum Kubernetes version from 1.27 to 1.34; upgrade Kubernetes first, because Helm refuses to install or upgrade on an older cluster.
- Every `helm upgrade`, including values-only ones, now rebuilds the feature store search index afterwards, signing in with `hopsworks.variables.admin_email` and `hopsworks.variables.admin_password`, and fails the upgrade if they don't sign in to the Hopsworks admin account.
  Set them to the admin account's credentials before you upgrade; if password login is disabled, upgrade to [5.1.1][hopsworks-5-1-1] instead.
- OpenSearch drops vectors not yet flushed and rejects vector writes for about two minutes on its first start on 5.1, because of the default `olk.opensearch.knn.circuit_breaker` settings; set `triggered: false` and `percent: 75` under it, or upgrade to [5.1.1][hopsworks-5-1-1] instead.
- Removed Brewer; remove `global._hopsworks.brewer`, `brewer`, `hopsworks.ingress.brewer`, `hopsworks.variables.brewer_*` and `hw-kyverno.policyExceptions.brewer` from your values, because the values schema rejects them.
  With `--reuse-values`, which keeps the 5.0 defaults such as `brewer`, use `--reset-then-reuse-values`.
- Removed `hopsworks.variables.hive_default_quota` and `hopsworks.variables.enable_conda_install`; remove them from your values, because the values schema rejects them.
- The consul-k8s chart fails to render with `disable_hostname` in `consul.consul.server.extraConfig`; remove it, because `consul.consul.global.metrics.disableAgentHostName` (default `true`) replaces it.
- The chart fails to render with `hopsworks.hopsfsMount.enabled: false`, because the new Trino mountable-secrets sidecar needs the HopsFS mount.
  Set `global._hopsworks.trino.mountableSecrets.enabled: false`, and override `trino.trino.initContainers` and `trino.trinotest.initContainers.coordinator` without the `mountable-secrets` container, as `values.openshift.yaml` does.
- 5.1.0 came out before [5.0.14][hopsworks-5-0-14] and lacks most of its changes, such as a security fix in jobs; if you run 5.0.14, upgrade to [5.1.2][hopsworks-5-1-2] or later instead.
- 5.1.0 ships an older RonDB chart than [5.0.13][hopsworks-5-0-13], without `rondb.rondb.rdrs.probes`, so the RonDB REST server restarts again during a data node failure; if you run 5.0.13, upgrade to [5.1.1][hopsworks-5-1-1] or later instead.
- Spark is upgraded from 3.5 to 4.1, which is built for Scala 2.13; rebuild job JARs built for Scala 2.12, and check your jobs against the [Spark migration guide](https://spark.apache.org/docs/latest/migration-guide.html).
- Removed library installs from a conda channel, an `.egg` file or an `environment.yml` file, because the base environments are now uv virtualenvs without conda; use pip, a wheel, a Git repository, a `requirements.txt` file or custom commands instead ([installing libraries](https://docs.hopsworks.ai/5.1/user_guides/projects/python/python_install/)).
- `catalog-volume` moved from `trino.trino.configMounts` to the `additionalVolumes` and `additionalVolumeMounts` of `trino.trino.coordinator` and `trino.trino.worker`.
  If you override these lists, copy both entries from the chart's values and remove `catalog-volume` from an overridden `trino.trino.configMounts`, or the Trino pods don't start.
- Trino pods now run as the `hopsworks-trino` and `hopsworks-trino-test` ServiceAccounts instead of `default`; move anything you attached to `default` for Trino, such as a cloud identity annotation or an OpenShift SCC.
- Prometheus is upgraded from 2.51 to 3.14; check custom alert rules and scrape configs against the [Prometheus 3 migration guide](https://prometheus.io/docs/prometheus/latest/migration/).
- Hopsworks now rejects a KServe deployment that sets the `PYTHONPATH` environment variable, which KServe 0.19 blocks; remove it from your deployments.
- Knative request metrics are now `http_server_request_duration_seconds` instead of `revision_request_count` and `revision_request_latencies`, with new label names, and Spark metrics have new names; update custom Grafana dashboards and alert rules.
- `hopsworks.variables.enable_read_only_git_repositories` now defaults to `false`, so users can commit and push from Git repositories in Hopsworks; to keep them read-only, set it to `'true'` before you upgrade.
- `vpa.image.tag` is now the version of the VPA installer image (default `"1.7.1-2"`), separate from `vpa.imagesTag`; remove any override of it, including the `"1.7.1"` that [5.0.8][hopsworks-5-0-8] asked for.

### Deprecations

- Deprecated `kserve.istio.gateways.http10` for `kserve.istio.gateways.ingress.http10`; the old key, ignored in 5.0, works again.
- Deprecated `grafana.grafana.dashboardsConfigMaps`, which stays empty now that the dashboards ship in the Grafana image.

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

[docs-sql-runner]: https://docs.hopsworks.ai/5.1/user_guides/projects/trino/query_engine/#sql-runner
[docs-trino-history]: https://docs.hopsworks.ai/5.1/setup_installation/admin/trino/#query-history
[values-olk-index-upgrade]: https://docs.hopsworks.ai/5.1/setup_installation/common/helm_chart_values/olk/#helm.olk.opensearch.indexUpgrade.mode
