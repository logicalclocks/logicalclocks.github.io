---
releases:
  "5.0.13":
    released: "2026-09-28"
    application: "5.0.12"
    python_client: "5.0.9"
  "5.0.12":
    released: "2026-09-21"
    application: "5.0.11"
    python_client: "5.0.9"
  "5.0.11":
    released: "2026-09-16"
    application: "5.0.10"
    python_client: "5.0.7"
  "5.0.10":
    released: "2026-09-11"
    application: "5.0.10"
    python_client: "5.0.7"
  "5.0.9":
    released: "2026-08-28"
    application: "5.0.9"
    python_client: "5.0.6"
  "5.0.8":
    released: "2026-08-21"
    application: "5.0.7"
    python_client: "5.0.5"
  "5.0.6":
    released: "2026-07-29"
    application: "5.0.4"
    python_client: "5.0.3"
  "5.0.5":
    released: "2026-07-22"
    application: "5.0.3"
    python_client: "5.0.3"
  "5.0.4":
    released: "2026-07-17"
    application: "5.0.3"
    python_client: "5.0.3"
  "5.0.3":
    released: "2026-07-14"
    application: "5.0.3"
    python_client: "5.0.3"
  "5.0.2":
    released: "2026-07-10"
    application: "5.0.3"
    python_client: "5.0.3"
  "5.0.1":
    released: "2026-07-03"
    application: "5.0.1"
    python_client: "5.0.1"
  "5.0.0":
    released: "2026-06-11"
    since: "4.8.2"
    application: "5.0.0"
    python_client: "5.0.0"
---

# Hopsworks 5.0 { #hopsworks-5-0 }

The releases of Hopsworks 5.0, newest first.
To upgrade from 4.8 or between 5.0 releases, follow [Upgrading to Hopsworks 5.0][upgrading-to-5-0].

## 5.0.13 { #hopsworks-5-0-13 }

### Breaking changes

- Removed the Kafka quota defaults Job, so `kafka.cluster.kafka.quotas.defaults` is ignored with `type: strimzi`, and fails the render with `type: kafka` when `enabled` is `true`.
  If you set it, move your limits to `kafka.cluster.kafka.quotas.strimzi` or `kafka.cluster.kafka.quotas.kafka`, with new numbers: the `strimzi` rates are a total per broker, shared by all clients.
- `quotas` on a user in `kafka.users` now fail the render under the default `strimzi` plugin, which never enforced them.
  Remove them, or set `kafka.cluster.kafka.quotas.type: kafka`, `kafka.cluster.kafka.quotas.minAvailableRatioPerVolume: 0` and `kafka.cluster.kafka.authorizer.principalBuilderClass: ""` to enforce them.
- The Airflow migration Job now waits for the DDL MySQL server, so the upgrade hangs with `rondb.rondb.meta.ddlMySQLd.enabled: false`.
  Keep it enabled if you use Airflow.

### Release notes

- Added `kafka.cluster.kafka.quotas.type` to choose the Kafka quota plugin: `strimzi` (the default), set under `kafka.cluster.kafka.quotas.strimzi`, or `kafka`, which enforces per-user quotas from `kafka.users[].quotas` and defaults from `kafka.cluster.kafka.quotas.kafka`.
  On clusters first installed on Hopsworks 4.3 or 4.5, whose Strimzi CRDs drop `spec.kafka.quotas`, none of these settings take effect.
  `kafka` also needs `kafka.cluster.kafka.quotas.minAvailableRatioPerVolume: 0`, and per-user quotas need `kafka.cluster.kafka.authorizer.principalBuilderClass: ""`, which changes how ACLs and `superUsers` match principals.
- Added `onlinefs.deployment.strategy` to set the rollout strategy of OnlineFS.
- Changed the RonDB REST server probes to outlast a data node failure, and made them configurable under `rondb.rondb.rdrs.probes`.
- Fixed OnlineFS upgrades stalling on a full node pool: with two or more `onlinefs.deployment.replicas`, a rollout now replaces one pod at a time.
- Fixed the Airflow migration Job losing tables on clusters with more than one RonDB MySQL server; it now uses only the DDL MySQL server.
- Fixed the OpenSearch metrics exporter reporting the parent cluster on a satellite deployment, and missing OpenSearch with a custom `global._hopsworks.consulDomainName`.

## 5.0.12 { #hopsworks-5-0-12 }

### Breaking changes

- Filebeat now keeps only the Kubernetes labels listed under `olk.filebeat.kubernetesMetadata`, and the `serviceLabelKey` of each `olk.logstash.extendServicesPipeline` entry, on service logs.
  Add any other label you filter on to `olk.filebeat.kubernetesMetadata.extraPodLabels`, `extraNamespaceLabels` or `extraNodeLabels`; if you override `olk.filebeat.logs_locations`, set `addKubernetesMetadata: true` on each entry and drop its `add_kubernetes_metadata` processor.
- Removed `hopsworks.variables.jupyter_spark_driver_memory_overhead_factor`, added in 5.0.10; the driver memory overhead of a notebook now comes from its Spark configuration.
  Remove it from your values before you upgrade, because the values schema rejects it; with `--reuse-values`, which keeps the old default, use `--reset-then-reuse-values`.

### Release notes

- Added the Spark properties `spark.driver.memoryOverheadFactor` and `spark.executor.memoryOverheadFactor` to the Spark configuration of jobs, Jupyter and project defaults.
- Changed the memory split of the remote shuffle servers to stop heap out-of-memory crashes: 20% of `spark.rss.shuffleServer.resources.limits.memory` is reserved for native memory and the rest is split 25% heap, 75% off-heap.
  `spark.rss.shuffleServer.bufferCapacityRatio` now defaults to `0.6` and `spark.rss.shuffleServer.resources.limits.cpu` to `2000m`.
- Fixed the remote shuffle servers never receiving their off-heap memory setting, which left their buffers about nine times too small.
- Fixed service logs being dropped from the `.services` OpenSearch index when Kubernetes labels pushed it past 1000 fields.

### Upgraded components

| Component | 5.0.11 | 5.0.12 |
| --------- | ------ | ------ |
| Base environment images | 5.0.9 | 5.0.10 |

## 5.0.11 { #hopsworks-5-0-11 }

### Release notes

- Changed the Kafka Entity Operator to follow the tolerations, topology spread and node affinity of the Kafka brokers, unless set under `kafka.cluster.entityOperator.template.pod`.
- Added `rondb.rondb.mysql.users[].existingSecret` to read the password of a MySQL user from your own Secret.
- Changed `rondb.rondb.timeoutsMinutes.ndbmtdStartupProbe` to 240 minutes, from 120, so data nodes that take over two hours to reload aren't restarted in a loop.
- Fixed RonDB rolling restarts making healthy data nodes shut down; data nodes now wait for the rollout to settle (`rondb.rondb.ndbmtdSettleWait`).

### Upgraded components

| Component | 5.0.10 | 5.0.11 |
| --------- | ------ | ------ |
| RonDB | 26.02.9 | 26.02.10 |

## 5.0.10 { #hopsworks-5-0-10 }

### Release notes

- Added the `hopsworks.variables.git_*` variables for private CA certificates (`git_custom_ca_configmap`, which must exist in every project namespace), per-provider HTTP and HTTPS proxies, and disabled TLS verification in Git operations.
- Added `hopsworks.variables.jupyter_spark_notebook_server_memory_floor_mb` (default `512`) and `jupyter_spark_driver_memory_overhead_factor` (default `0.25`) to size the Jupyter server of Spark environments.
- Added the `KafkaAuthenticationFailures` Prometheus alert for clients that keep failing to authenticate, for example with an expired certificate.
- Added `kafka.cluster.clusterCa.validityDays` and `kafka.cluster.clientsCa.validityDays` (default `365`) for the certificates Strimzi issues, applied at the next issuance.
- Fixed Git operations failing to authenticate when a provider token or password contains special characters.
- Fixed writes to an online feature group failing after its table was truncated.
- Fixed init containers that wait for a RonDB rollout giving up after 30 minutes, which failed the Hive Metastore, HopsFS, Airflow migration and CA pods when a RonDB restart took longer.
- Fixed security vulnerabilities in the remote shuffle service.

### Upgraded components

| Component | 5.0.9 | 5.0.10 |
| --------- | ----- | ------ |
| ArrowFlight server | 5.0.3 | 5.0.4 |
| Base environment images | 5.0.8 | 5.0.9 |
| Git image | 1.4.2 | 1.4.4 |
| OnlineFS | 2.3.4 | 2.3.5 |
| Remote shuffle service (Apache Uniffle) | 0.10.8 | 0.10.8.1 |

## 5.0.9 { #hopsworks-5-0-9 }

### Breaking changes

- Init containers now set CPU and memory requests and limits.
  If a namespace `LimitRange` has a `min` or `max` they don't fit, set `global._hopsworks.initContainerResources` before you upgrade, or Kubernetes rejects the pods.

### Release notes

- Added `global._hopsworks.initContainerResources` (`waiter`, `tool`, `runtime`) to size the requests and limits that init containers now set.
- Changed `hopsworks.variables.docker_operations_timeout_listing_minutes`, `docker_operations_timeout_check_minutes` and `docker_operations_timeout_export_minutes` from 5 to 15 minutes, and `max_concurrent_base_sync_ops` from 6 to 5, so large base images finish syncing.
- Fixed init containers without requests and limits being charged a namespace `LimitRange` default for the whole life of the pod; the RonDB and Consul charts are not covered yet.
- Fixed the chart failing to render with `hopsworks.dropDatabase: true`.
- Fixed the KServe local model controller image (`kserve.kserve.localmodel.enabled`) failing to pull.

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

## 5.0.8 { #hopsworks-5-0-8 }

There is no 5.0.7 release.

### Breaking changes

- `vpa.image.tag` is now a string, so an override such as `1.2` fails the values schema.
  If you override it, quote it and set it equal to `vpa.imagesTag` before you upgrade; with `--reuse-values` and `global._hopsworks.vpaEnabled: true`, use `--reset-then-reuse-values`.

### Release notes

- Added `hopsworks.variables.upload_policy` (`enabled`, `admins_only` or `disabled`) to control who can upload files, from the web UI and from clients such as the Python SDK.
  The upgrade writes the value to the cluster, so a change made in the admin UI lasts until the next upgrade.
- Added `hopsworks.jupyter.notebookConfig.enableUploads`; set it to `false` to block file uploads from the Jupyter UI and base64 uploads through the Jupyter Contents API.
- Fixed pod creation stalling for about 20 seconds on clusters with many API groups when the Vertical Pod Autoscaler (`global._hopsworks.vpaEnabled`) is on.
- Fixed Superset queries through Trino logging `Access Denied: Cannot access catalog system`.
- Fixed security vulnerabilities in the Payara, Filebeat, Grafana, OpenSearch, OpenSearch Dashboards, Logstash, remote shuffle service and Superset images, and in the MySQL database of Superset.

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

## 5.0.6 { #hopsworks-5-0-6 }

### Release notes

- Added `docker-registry.affinity`, `minio.affinity` and `hopsworks.dockerRegistry.preset.affinity` for the Docker registry, MinIO and the preset image push Job.
- Fixed Airflow failing to start on OpenShift with `airflow: command not found`.

### Upgraded components

| Component | 5.0.5 | 5.0.6 |
| --------- | ----- | ----- |
| Airflow image | 5.0.0 | 5.0.1 |

## 5.0.5 { #hopsworks-5-0-5 }

### Release notes

- Added `rondb.rondb.ndbmtdSequencedRollout.enabled` (default `false`) to roll the RonDB data nodes one node group at a time, on clusters with more than one node group.
- Changed the RonDB startup probe timeouts (`rondb.rondb.timeoutsMinutes`) from 25 to 120 minutes for data nodes and from about 17 to 20 minutes for MySQL servers.

### Upgraded components

| Component | 5.0.4 | 5.0.5 |
| --------- | ----- | ----- |
| RonDB | 26.02.6 | 26.02.8 |

## 5.0.4 { #hopsworks-5-0-4 }

### Release notes

- Added `hopsworks.service.worker.external.https.nodePort` to pin the node port of the Hopsworks HTTPS service when its `type` is `NodePort`.
- Fixed online feature store ingestion dropping rows on temporary RonDB errors, such as during a RonDB upgrade; it now pauses and retries.
  Set the pause between retries with `onlinefs.configmapOverrides.onlinefssite.service.pauseRetrySleepMs` (default `5000`).

### Upgraded components

| Component | 5.0.3 | 5.0.4 |
| --------- | ----- | ----- |
| OnlineFS | 2.3.1 | 2.3.2 |

## 5.0.3 { #hopsworks-5-0-3 }

### Breaking changes

- The admin liveness and startup probes now have a default `exec` handler, so a probe you set with `httpGet` or `tcpSocket` also needs `exec: null`, or Kubernetes rejects the pod.
  This needs Helm 4 or Helm 3.17.1 or later, because older Helm 3 releases ignore a `null` for a subchart value.

### Release notes

- Added `hopsfs.objectStorage.s3.disableCertChecking` and `hopsfs.objectStorage.s3.disableChecksumValidation` to turn off TLS certificate checks and client-side checksum validation for the HopsFS S3 endpoint.
- Added `hopsworks.envs.postInstall.DEPLOY_RETRY_INTERVAL_SEC`, `ASADMIN_TIMEOUT_SEC` and `ASADMIN_DEPLOY_TIMEOUT_SEC` to tune how the admin sidecar retries the Hopsworks deployment.
- Changed the Hopsworks admin container to restart after about 10 minutes without a response (`hopsworks.probs.admin.livenessProbe`), with up to 30 minutes to start (`hopsworks.probs.admin.startupProbe`).
- Deprecated `hopsworks.envs.postInstall.DEPLOY_RETRIES`, which has no effect now that the admin sidecar retries until the deployment succeeds.
- Fixed security vulnerabilities in the Strimzi operator and Kafka images.
- Fixed the Hopsworks admin pod getting stuck in CrashLoopBackOff when workers were slow to register; the admin sidecar now keeps retrying and restarts unregistered workers.

### Upgraded components

| Component | 5.0.2 | 5.0.3 |
| --------- | ----- | ----- |
| HopsFS | 3.4.3.1-EE-RC1 | 3.4.3.1-EE-RC3 |
| RonDB | 26.02.5 | 26.02.6 |
| Strimzi | 0.45.1-h4 | 0.45.1-h5 |

## 5.0.2 { #hopsworks-5-0-2 }

### Breaking changes

- `helm uninstall` now deletes the data volumes of the HopsFS DataNodes, MinIO, OpenSearch, Kafka, Consul and the remote shuffle service, for good.
  To keep them, set `global._hopsworks.wipeDataOnUninstall: false` or label the PVCs `hopsworks.ai/keep=true` before you uninstall; the Superset MySQL volume is deleted regardless.

### Release notes

- Added post-delete Jobs that remove the Secrets, ConfigMaps and certificates `helm uninstall` used to leave behind.
- Fixed `uv pip install` in the web terminal ignoring the index, mirror and proxy settings in `hopsworks.dockerImage.pypi.global_parameters`.
- Fixed a failed HopsFS schema migration being reported as successful, which let the NameNode start on a partly migrated schema.

### Upgraded components

| Component | 5.0.1 | 5.0.2 |
| --------- | ----- | ----- |
| Base environment images | 5.0.1 | 5.0.2 |
| Model serving webhook | 5.0.1 | 5.0.2 |
| OnlineFS | 2.3 | 2.3.1 |
| RonDB | 26.02.4 | 26.02.5 |

## 5.0.1 { #hopsworks-5-0-1 }

### Breaking changes

- Feature monitoring is now on by default, and the upgrade writes `hopsworks.variables.enable_feature_monitoring` to the cluster, replacing a value set in the admin UI.
  To keep it off, set it to `'false'` before you upgrade.

### Release notes

- Added support for Kubernetes 1.35 and 1.36.
- Added `hive.externalLoadBalancer.enabled` (default `false`) to expose the Hive Metastore outside Kubernetes, for example to external Spark applications.
- Added `hopsworks.velero.backup.storageLocation.s3ForcePathStyle` for S3-compatible backup stores that need path-style addressing.
- Added `kserve.kserve.servingruntime.vllmopenai.imageRegistry` and `kserve.kserve.servingruntime.vllmomni.imageRegistry` to pull the vLLM images from a mirror.
- Added `hopsworks.variables.rondb_usage_cache_ttl_seconds` and `rondb_usage_query_timeout_seconds` for the RonDB usage on the project quotas page; raise the timeout if usage stops showing on a large cluster.
- Added `hopsworks.variables.feature_monitoring_max_num_features` (default `15`) to cap the features of a feature monitoring configuration.
- Added `hopsworks.variables.lifecycle_webhook_url`, `lifecycle_webhook_cluster_id` and `lifecycle_webhook_secret` to post user, project and membership events to a webhook, signed with HMAC-SHA256 when a secret is set.
- Added `hw-kyverno.policyExceptions.pythonDeployment.enabled` (default `true`) so Python and agent deployments that mount HopsFS start under the Kyverno restricted policies.
- Added `hopsworks.variables.docker_operations_registry_http`; set it to `"true"` when environment builds pull from a self-managed registry over plain HTTP.
- Fixed security vulnerabilities in the MySQL database of Superset.
- Fixed Superset redirecting to its internal host behind a reverse proxy that rewrites the Host header; set `hopsworks.variables.hopsworks_public_proxy_url` to the public `host[:port]`.
- Fixed model deployments with images from the managed Docker registry failing to start.
- Fixed database initialization and migrations starting while RonDB was still restarting; they now wait up to 30 minutes for each RonDB StatefulSet to roll out.
- Fixed the App Metrics Grafana dashboard showing "No data" for apps without traffic.

### Upgraded components

| Component | 5.0.0 | 5.0.1 |
| --------- | ----- | ----- |
| Base environment images | 5.0.0 | 5.0.1 |
| HopsFS | 3.4.3.1-EE-RC0 | 3.4.3.1-EE-RC1 |
| Model serving webhook | 5.0.0 | 5.0.1 |
| RonDB MySQL metrics exporter | 0.11.4 | 0.11.5 |
| Superset MySQL | 8.4.5-debian-12-r0-h1 | 8.4.5-debian-12-r0-h2 (MySQL 8.4.10) |

## 5.0.0 { #hopsworks-5-0-0 }

Entries marked with a 4.8 release also shipped in that 4.8 patch release, so you can skip them if you upgrade from it or a later one.
If you run 4.8.13 or later, upgrade to the latest 5.0 release instead of 5.0.0, as [Upgrading to Hopsworks 5.0][upgrading-to-5-0] explains.

### Breaking changes

- Upgraded Airflow from 1.10 to Airflow 3, and DAGs written for Airflow 1.10 don't run on it.
  The upgrade drops and recreates the Airflow metadata database, so DAG run history and the Variables and Connections created in Airflow are lost for good; see [Upgrading to Hopsworks 5.0][upgrading-to-5-0].
- `hopsworks.variables.jupyter_shell_command` is now a JSON list of the command and its arguments.
  If you set it, rewrite it as a list, for example `'["/bin/bash"]'`, because a plain path produces an invalid Jupyter configuration.
- Removed `hopsworks.variables.dlthub_image_name`, replaced by the `dlthub-ingestion-pipeline` environment; remove it from your values before you upgrade, because the values schema rejects it.
- Removed `hopsworks.payara.executorService`, replaced by `hopsworks.payara.websocketProxy`; remove it from your values before you upgrade, because the values schema rejects it.
- `global._hopsworks.superset.mysql.enabled` and `global._hopsworks.superset.redis.enabled` must match `superset.mysql.enabled` and `superset.superset.redis.enabled`.
  If you disabled the MySQL or Redis of Superset, also set the matching global value to `false`, or the chart fails to render.
- The Spark operator pre-upgrade Job now pulls the `spark-operator-crds` image (`spark.sparkOperatorUpgradeJob.crdImage`) on every upgrade (also in 4.8.17).
  Air-gapped installations must mirror it first, or `helm upgrade` fails.
- Removed `VLLM_USE_FLASHINFER_SAMPLER=0` from the vLLM serving runtimes (also in 4.8.7).
  If you serve vLLM models on GPUs older than compute capability 7.5, set it in `kserve.kserve.servingruntime.vllmopenai.env` or `kserve.kserve.servingruntime.vllmomni.env`.

### Release notes

- Added `ddl-mysqld`, a separate MySQL server for online feature store schema changes, enabled by default with `rondb.rondb.meta.ddlMySQLd.enabled` (also in 4.8.4).
- Added asynchronous upload of HopsFS blocks to object storage (`hopsfs.objectStorage.asyncUpload.enabled`, off by default).
  With it on, a stopping DataNode first uploads its pending blocks, which can take about an hour (`hopsfs.datanode.gracefulDrain`); turning that drain off can lose them.
- Added `hopsfs.namenode.blockSizeMiB` (default `128`) to set the HopsFS block size.
- Added `DataMemory`, `TimeBetweenGlobalCheckpoints` and other RonDB settings to `rondb.rondb.rondbConfig` (also in 4.8.5).
- Added `hopsworks.variables.kube_user_workload_tolerations` to add tolerations to user workloads such as Jupyter, jobs and deployments (also in 4.8.8).
- Added `hopsworks.dockerImage.packageAuth.secretName` and `hopsworks.dockerImage.packageAuth.caCertsConfigMap` for pip, conda and apt mirrors that need credentials or a private CA (also in 4.8.8).
- Added `onlinefs.configmapOverrides` to tune the threads, caches, and RonDB, Kafka and logging settings of the online feature store service.
- Added `arrowflight.deployment.server.hopsfs_query_mode` to make the ArrowFlight server load feature group data into DuckDB tables (`table`) instead of views (`view`) (also in 4.8.3).
- Added `hopsworks.payara.websocketProxy` to tune the WebSocket proxy of Jupyter, terminals and Python apps, such as `maxSessionsPerApp` (default `500` per pod).
- Added WebSocket proxy panels to the Hopsworks Grafana dashboard, replacing the Jupyter executor pool panel.
- Added an App Metrics Grafana dashboard with the request rate, latency, CPU and memory of Python apps.
- Added Grafana dashboards and Prometheus alerts for the MySQL and Redis of Superset.
- Added a Superset Public role to share dashboards and chart permalinks without a login; only dashboards granted to it are public, and `superset.superset.allowAnonymousAccess: false` requires a login for all.
- Changed Superset to enable dashboard role-based access control.
- Added `hopsworks.variables.superset_proxy_*` for the connection pool and timeouts of the Hopsworks proxy in front of Superset.
- Added `hopsworks.variables.streamlit_sharing` (default `false`) to allow Streamlit apps that are reachable without a Hopsworks login.
- Added the `python-app-pipeline` environment, with Streamlit, for interactive apps.
- Added the `python-agent-pipeline` environment, with FastAPI, LlamaIndex and OpenTelemetry, for Python agents.
- Added the `agent-job` environment, with Claude Code and OpenAI Codex, for agent jobs.
- Added the `dlthub-ingestion-pipeline` environment for ingesting data into feature groups with dltHub.
- Added `hopsworks.variables.agent_jobs_enabled` (default `"true"`) to turn agent jobs on or off.
- Added an OpenTelemetry tracing sidecar to agent deployments, sized with `hopsworks.variables.agent_deployment_otel_cpu` and `agent_deployment_otel_memory_mb` and turned off with `agent_deployment_otel_enabled: "false"`.
- Added the `vllm-omni` serving runtime for vLLM-Omni models (also in 4.8.7).
- Changed the `vllm-openai` serving runtime to the `vllm/vllm-openai` image (also in 4.8.7).
- Added `hopsworks.variables.kube_serving_vllm_versions` and `kube_serving_vllm_omni_versions`, the vLLM image tags a deployment can choose; update them when you change the vLLM runtime images (also in 4.8.7).
- Added `hopsworks.variables.platform_intelligence_llm_*` for the LLM of Platform Intelligence, which stays off without an API key.
- Added `hopsworks.variables.kube_scheduling_jobinit_*` to size the CPU and memory of the initialization step of Spark and Ray jobs.
- Added Kyverno policy exceptions so Python apps and web terminals start under Kyverno policies (`hw-kyverno.policyExceptions.pythonapp.enabled`, `hw-kyverno.policyExceptions.terminal.enabled`).
- Added `global._hopsworks.kyverno.policies.addCertificatesVolume.initContainers.enabled` to inject the custom CA certificates into the init containers of pods annotated `kyverno-inject-certs-init: enabled` (also in 4.8.8).
- Changed the default HopsFS resources: NameNode and DataNodes get 1024 MiB of heap, a CPU request of 1 and a CPU limit of 4, the NameNode 1024 MiB of direct memory, and DataNodes a memory limit of 2048Mi instead of 750Mi.
  Plan for the extra CPU requests of the 5 default DataNodes.
- Changed the HopsFS DataNode PodDisruptionBudget to evict one DataNode at a time; `hopsfs.datanode.podDisruptionBudget.minAvailable` is ignored.
- Changed HopsFS pods to restart when a `helm upgrade` changes the HopsFS configuration.
- Changed the console logs of the HopsFS NameNode and DataNodes from JSON to plain text.
- Changed RonDB upgrades to roll the management server before the data nodes, so data nodes no longer shut down with error 2305 (also in 4.8.6).
- Changed `helm upgrade` to fail when `rondb.rondb.clusterSize.numNodeGroups` differs from the running cluster, because RonDB can't change node groups online (also in 4.8.6).
- Changed `hopsfs.image.registry`, when set, to override `global._hopsworks.imageRegistry` as the full registry and path prefix of the HopsFS image, ending in `/`.
- Changed the Redis of Superset to cap its memory at 256 MB with `allkeys-lru` eviction.
- Deprecated `airflow.reset_db_if_error`, which Airflow 3 ignores.
- Fixed security vulnerabilities in the Payara and OpenSearch images.
- Fixed security vulnerabilities in the Grafana, OpenSearch Dashboards, Strimzi and remote shuffle service images, and in the Redis and MySQL images of Superset (also in 4.8.11).
- Fixed external LoadBalancer Services, such as those of ArrowFlight, HopsFS, OpenSearch and Trino, not being created with Helm 3.20.1 and later; a component without its own setting again follows `global._hopsworks.externalLoadBalancers`.
- Fixed members with the Feature store restricted project role getting more access to OpenSearch than intended.
- Fixed `hopsfs.namenode.auditLog.enableStatOperation` and `enableListOperation` being ignored; the NameNode audit-logs stat and list operations only when they are `true` (also in 4.8.8).
- Fixed `helm upgrade --force` failing with a conflict on unchanged chart Jobs; their names now include the release revision, so every `helm upgrade` runs them again (also in 4.8.3).
- Fixed the preset base image push Job not running again when only image versions or digests changed, for example with Argo CD (also in 4.8.6).
- Fixed fresh installs failing and rolling back when the Knative Serving webhook was not ready yet.
- Fixed Airflow pods failing to start when the HopsFS mount took longer than 30 seconds.

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
