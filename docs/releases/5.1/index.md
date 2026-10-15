---
releases:
  "5.1.1":
    released: "2026-10-09"
    application: "5.1.1"
    python_client: "5.1.1"
  "5.1.0":
    released: "2026-09-24"
    application: "5.1.0"
    python_client: "5.1.0"
---

# Hopsworks 5.1 { #hopsworks-5-1 }

The releases of Hopsworks 5.1, newest first.
To upgrade from 5.0 or between 5.1 releases, follow [Upgrading to Hopsworks 5.1][upgrading-to-5-1].

## 5.1.1 { #hopsworks-5-1-1 }

### Breaking changes

- The RonDB REST server now uses a probe port and an upload path that need RonDB 26.02.11.
  If you pin `rondb.rondb.images.rondb.tag` to an older version, set `rondb.rondb.rdrs.probePort.enabled: false` and `rondb.rondb.rdrs.uploadPath: ""`, or the REST server doesn't start.
- The post-upgrade search index rebuild signs in as the agent user, and fails the `helm upgrade` if `hopsworks.agent_email` and `hopsworks.agent_password` (default `agent@hops.io`, `admin`) don't match that account.
  Set them, or turn the rebuild off with `hopsworks.opensearchReindex.enabled: false`.

### Release notes

- Added `hopsworks.opensearchReindex.enabled` to turn off the post-upgrade search index rebuild, and `hopsworks.variables.command_search_fs_reindex_queue_wait_as_ms` to bound its wait for the search command queue.
- Added `nodePort` values to pin the node ports of unmanaged external load balancers: ArrowFlight, OpenSearch, the HopsFS NameNode and DataNodes, Trino, the Hive Metastore, Kafka (`bootstrapNodePort`, `startingNodePort`) and the RonDB MySQL and REST servers.
  The RonDB ones ignore `global._hopsworks.externalLoadBalancers.managed` and apply only when `rondb.rondb.meta.mysqld.externalLoadBalancer.managed` or `rondb.rondb.meta.rdrs.externalLoadBalancer.managed` is `false`.
- Added `rondb.rondb.rdrs.ttlPurge.enable` and `activeWindow` to turn off the TTL purge of the RonDB REST server or limit it to a daily window.
- Changed the RonDB REST server probes to outlast a data node failure and to use their own port, `rondb.rondb.rdrs.probePort`; set them under `rondb.rondb.rdrs.probes`.
- Fixed RonDB daemons ignoring SIGTERM, so every pod stop ended in a kill and a stopped data node could stall the cluster; `rondb.rondb.terminationGracePeriodSeconds` is now set per component.
- Fixed the RonDB REST server reading request bodies over 64 KiB as empty.
- Fixed Trino giving a project access to only one of several feature stores shared with it.
- Fixed environment builds never starting when `rondb.rondb.priorityClass` is renamed; `hopsworks.variables.docker_operations_buildkit_priority_class` now defaults to empty, so builds run at the default priority and no longer preempt other pods.
- Fixed the post-upgrade search index rebuild failing without the admin password, for example when password login is disabled.
  It now signs in as the agent user and runs once per index format; the first upgrade to 5.1.1 rebuilds the index, and search is incomplete until it finishes.
- Fixed OpenSearch losing unflushed vectors and rejecting vector writes for about two minutes on its first start on 5.1; `olk.opensearch.knn.circuit_breaker.triggered` now defaults to `false` and `percent` to `75`.
- Fixed `values.openshift.yaml` for the OpenShift `restricted-v2` SCC, covering Strimzi, Kafka, ZooKeeper, the Spark operator and the MySQL and Redis of Superset.
  Use it with Helm 4 or Helm 3.17.1 or later, because older Helm 3 releases ignore its `null` overrides of subchart values.
- Fixed the values schema rejecting `hopsworks.variables.loadbalancer_external_domain_namenode` and `hopsworks.variables.loadbalancer_external_domain_datanode`.

### Upgraded components

| Component | 5.1.0 | 5.1.1 |
| --------- | ----- | ----- |
| Base environment images | 5.1.0 | 5.1.1 |
| RonDB | 26.02.10 | 26.02.11 |
| Trino | 480-v10 | 480-v11 |

## 5.1.0 { #hopsworks-5-1-0 }

5.1.0 also includes the changes of [5.0.1][hopsworks-5-0-1] to [5.0.13][hopsworks-5-0-13], which are listed under those releases, except the configurable RonDB REST server probes of 5.0.13 (`rondb.rondb.rdrs.probes`), which return in [5.1.1][hopsworks-5-1-1].

### Breaking changes

- Raised the minimum Kubernetes version from 1.27 to 1.34; upgrade Kubernetes first, because Helm refuses to install or upgrade on an older cluster.
- Removed Brewer; remove `global._hopsworks.brewer`, `brewer`, `hopsworks.ingress.brewer`, `hopsworks.variables.brewer_*` and `hw-kyverno.policyExceptions.brewer` from your values, because the values schema rejects them.
- Removed `hopsworks.variables.hive_default_quota`; remove it from your values, because the values schema rejects it.
- Removed `hopsworks.variables.enable_conda_install`; remove it from your values, because the values schema rejects it.
- `hopsworks.variables.enable_read_only_git_repositories` now defaults to `false`, so users can commit and push from Git repositories in Hopsworks; to keep them read-only, set it to `'true'` before you upgrade.
- The consul-k8s chart fails to render with `disable_hostname` in `consul.consul.server.extraConfig`; remove it, because `consul.consul.global.metrics.disableAgentHostName` (default `true`) replaces it.
- The chart fails to render with `hopsworks.hopsfsMount.enabled: false`, because the new Trino mountable-secrets sidecar needs the HopsFS mount.
  Set `global._hopsworks.trino.mountableSecrets.enabled: false`, and override `trino.trino.initContainers` and `trino.trinotest.initContainers.coordinator` without the `mountable-secrets` container, as `values.openshift.yaml` does.
- `catalog-volume` moved from `trino.trino.configMounts` to the `additionalVolumes` and `additionalVolumeMounts` of `trino.trino.coordinator` and `trino.trino.worker`.
  If you override these lists, copy both entries from the chart's values and remove `catalog-volume` from an overridden `trino.trino.configMounts`, or the Trino pods don't start.
- Prometheus is upgraded from 2.51 to 3.14; check custom alert rules and scrape configs against the [Prometheus 3 migration guide](https://prometheus.io/docs/prometheus/latest/migration/).
- Knative request metrics are now `http_server_request_duration_seconds` instead of `revision_request_count` and `revision_request_latencies`, with new label names; update custom Grafana dashboards and alert rules.
- Spark metrics have new names; update custom Grafana dashboards and alert rules.
- `vpa.image.tag` is now the version of the VPA installer image (default `"1.7.1-2"`), separate from `vpa.imagesTag`; remove any override of it, including the `"1.7.1"` that [5.0.8][hopsworks-5-0-8] asked for.
- Trino pods now run as the `hopsworks-trino` and `hopsworks-trino-test` ServiceAccounts instead of `default`; move anything you attached to `default` for Trino, such as a cloud identity annotation or an OpenShift SCC.

### Release notes

- Added an optional persistent BuildKit daemon (`global._hopsworks.buildkitd.enabled`) that keeps caches between environment builds; each replica requests 8 CPUs, 16Gi of memory and a 100Gi volume.
- Added `hopsworks.variables.npm_registry_url` for the npm registry of Python environments.
- Added `hopsworks.variables.docker_operations_lock_dependencies` (default off) for hash-locked dependencies in environment builds.
- Added `hopsworks.variables.docker_operations_allow_hermetic_custom_commands` (default off) to cache hermetic custom commands in environment builds.
- Added `hopsworks.variables.docker_operations_multi_region_copy` (default off) to copy environment images to the second region.
- Added `hopsworks.dockerImage.pypi.pythonDownloads` (default `never`), so uv never downloads a Python interpreter during environment builds.
- Added the `dbt-pipeline` environment, with dbt and its Trino and DuckDB adapters.
- Added Trino catalogs created by project Data Owners, loaded when an administrator restarts Trino and tested on a single-node coordinator (`global._hopsworks.trino.testCoordinator.enabled`).
- Added file-based credentials, such as Oracle wallets, for user-created Trino catalogs, through a privileged sidecar on every Trino pod that mounts `/apps/mountable-secrets` from HopsFS read-only.
- Added `global._hopsworks.trino.egressProbe.echoUrl` to show which IP addresses an external database must allow.
- Added `spark.sql.ansiEnabled` (default `false`), so Spark 3.5 SQL keeps returning null on overflow and invalid casts.
- Added cluster variables for the default CPU, memory and GPU of new jobs and Python apps, such as `hopsworks.variables.spark_job_executor_memory`.
- Added `hopsworks.variables.pushgateway_group_ttl_minutes`, `pushgateway_monitor_interval_ms` and `pushgateway_cleaner_batch_size` to clean stale Pushgateway metric groups.
- Added `olk.opensearch.audit.enabled` (default `false`) and `olk.opensearch.audit.retentionDays` for OpenSearch security audit logs.
- Added `olk.opensearch.security.default_tenant` (default `Private`), the tenant OpenSearch Dashboards opens in.
- Added `kserve.knative.imageRegistry` for the Knative images.
- Changed every `helm upgrade`, including values-only ones, to rebuild the feature store search index afterwards.
- Changed upgrades to update the KServe, Knative Serving and cert-manager CRDs in a pre-upgrade Job, which removes the unused `predictors.serving.kserve.io` CRD.
- Changed the default `kserve.kserve.controller.deploymentMode` from `Serverless` to `Knative`, its KServe 0.19 name.
- Changed Spark metrics to be scraped by Prometheus instead of pushed to the Pushgateway.
- Changed environment image builds to the `rondb-high-priority` priority class (`hopsworks.variables.docker_operations_buildkit_priority_class`), so they can preempt Jupyter and job pods.
- Changed `hopsworks.variables.docker_operations_buildkit_extra_args` to empty by default, dropping the S3 build cache arguments that failed without S3 credentials; set them again to keep an S3 build cache.
- Changed Grafana to load the Hopsworks dashboards from its image instead of ConfigMaps; add your own with `global._hopsworks.grafana.extraDashboardProviders`.
  A custom Grafana image must contain the Hopsworks dashboards, and a custom `grafana.grafana.dashboardProviders` must point to `/usr/share/grafana/dashboards/<folder>`.
- Changed OpenSearch snapshots and restores to skip the `.opendistro_security` index and hidden plugin indices.
- Changed AlertManager emails to link the alert title to the job, feature group or feature view that raised it.
- Deprecated `kserve.istio.gateways.http10` for `kserve.istio.gateways.ingress.http10`; the old key, ignored in 5.0, works again.
- Fixed model serving requests over HTTPS skipping the model serving authenticator when `kserve.knative.https.enabled` is `true`.
- Fixed image pulls from the in-cluster Docker registry failing with `x509: certificate signed by unknown authority`, for example on RHEL-family nodes.
- Fixed every model deployment failing when the Knative controller started with an empty registry certificate.
- Fixed images built from custom commands keeping the package repository credentials staged for the build; rebuild those images, and rotate the credentials in `hopsworks.dockerImage.packageAuth.secretName`.
- Fixed OpenSearch snapshot restores never finishing on single-node clusters.
- Fixed OpenSearch indices staying closed after a failed snapshot restore.
- Fixed Velero backups leaving out the Trino authentication Secrets.
- Fixed the Velero storage location rejecting AWS S3 without a custom endpoint.
- Fixed the values schema rejecting a cron string in `hopsworks.velero.backup.schedule`.
- Fixed database migrations crash-looping on a lock left by a transient Kubernetes API error.
- Fixed database migrations restarting once on every fresh install.
- Fixed the Kyverno restricted policies blocking schema fetches of REST, CRM and Google Sheets data sources.
- Fixed the "HDFS Bytes Written" panel of the Spark Grafana dashboard showing bytes read.

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
| Superset init image | dockerize | 0.14.0-alpine-h1.1 |
| Superset MySQL | 8.4.5-debian-12-r0-h1 | 8.4.11-ubuntu24.04-h4 |
| Superset MySQL metrics exporter | 0.17.2-debian-12-r7 | 0.20.0-alpine-h1.1 |
| Superset MySQL volume permissions image | 12-debian-12-r43 | 12-alpine-h1.1 |
| Superset Redis | 7.4.9-bookworm | 7.4.11-alpine-h1 |
| Superset Redis metrics exporter | 1.50.0-debian-11-r1 | 1.90.0-alpine-h1.1 |
| TensorFlow | 2.19.0 | 2.20.0 |
| TensorFlow Serving | 2.19.0 | 2.20.0 |
| Toolbox image (hwutils) | 1.7 | 1.9 |
| Trino | 480-v6 | 480-v10 |
| Vertical Pod Autoscaler | 1.2.1 | 1.7.1 (also in [5.0.8][hopsworks-5-0-8]) |
| Vertical Pod Autoscaler installer | 1.2 | 1.7.1-2 |
