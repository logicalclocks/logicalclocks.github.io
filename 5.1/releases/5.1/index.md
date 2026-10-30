# Release notes { #hopsworks-5-1 }

The releases of Hopsworks 5.1, newest first.

## 5.1.2 { #hopsworks-5-1-2 }

Helm chart 5.1.2 · Released on 2026-10-16 · Changes since [5.1.1][hopsworks-5-1-1] · Python client [5.1.2](https://github.com/logicalclocks/hopsworks-api/releases/tag/5.1.2)

### What's changed

- [API] [FRONTEND] [HELM] Fixed every OpenSearch restart deleting the OpenSearch roles of restricted-access grants and feature group shares.
  Grants and shares made before the last OpenSearch restart on 5.1.0 or 5.1.1 lost their roles, and granting or sharing again is refused: revoke and grant again, or unshare and share again.
- [API] Fixed external Spark clients failing to read, write or delete DELTA feature groups when the HopsFS NameNode and DataNode load balancers are turned off.
- [API] Fixed the Python client installing pyarrow 26 next to NumPy 1, with which importing `hsfs.feature_group` fails with `pyarrow requires NumPy 2.0 or newer`; it now requires pyarrow below 26.
- [FRONTEND] Fixed queued service operations failing on every retry when they removed a user from Superset or set up a project Observer's online feature store connection in Superset, and stopping for good after 68 failed attempts; a failing operation now retries once a day.
- [FRONTEND] Changed the SQL Runner of the Query Engine page to fill the page, show row numbers and column types in the results, list a table's columns in the Explorer and draw `EXPLAIN (FORMAT GRAPHVIZ)` plans as a graph ([SQL Runner][docs-sql-runner]).
- [FRONTEND] Fixed the SQL Runner leaving a query running when you leave it right after starting the query, and its autocompletion offering no column names in `WHERE`, `GROUP BY` or join conditions.
- [HELM] Addressed vulnerabilities in OpenSearch.
  It applies once an OpenSearch pod logs `Security configuration applied` after the upgrade; if none does, run `run_security_admin.sh` as [Security configuration][docs-os-security] shows.
- [HELM] Added an opt-in Job that copies the OpenSearch indices created before OpenSearch 2.0 during a 5.1 upgrade, in a window you pick, so the upgrade to 5.2.1 or later has nothing left to copy; set `olk.opensearch.indexUpgrade.mode` to `report` to list them, or to `copy` ([copying on 5.1.x][docs-os-copy-51]).
  Turn vector ingestion off in an upgrade of its own first (`onlinefs.deployment.vectordb.enabled: false`), and pass the mode with `--set`, not in your values file, because 5.2.1 and later read the same key.
- [HELM] Fixed every `helm upgrade` restarting OpenSearch.
- Addressed vulnerabilities in the Payara, Hopsworks certificate authority, Grafana, Filebeat and Superset images, and in the MySQL and Redis of Superset.

### Breaking changes

- [FRONTEND] [HELM] Recorded Trino queries now lose their query text, plan and JSON details after `hopsworks.variables.trino_events_strip_details_after_days` (`7`), instead of keeping them until the query is deleted after 61 days, and the first nightly cleanup after the upgrade strips every older one; set it to `61` or more to keep them.
- [FRONTEND] [HELM] The chart no longer enables Trino's MySQL event listener, which crash-looped the Trino coordinator after a RonDB MySQL server restart, so the admin [Trino query history][docs-trino-history] records no new queries; to keep it, add the listener as [Trino query history][docs-upgrade-trino-history] shows.
- [HELM] If your values restate `trino.trino.additionalConfigProperties` with its `event-listener.config-files` entry, which the 5.1.1 chart set by default, remove that entry or add the listener files as [Trino query history][docs-upgrade-trino-history] shows, or Trino doesn't start.

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

- [HELM] Removed the MySQL event listener from the default `trino.trino.additionalConfigProperties` and from `trino.trino.coordinator.additionalConfigFiles` and `trino.trino.worker.additionalConfigFiles`.
- [HELM] Changed the default of `hopsworks.variables.trino_events_cleaner_batch_size` from 1000 to 100.
- [HELM] Added `hopsworks.variables.trino_events_strip_details_after_days` (default `7`), the days after which a recorded Trino query loses its text, plan and JSON details.
- [HELM] Added `olk.opensearch.indexUpgrade.mode` (default `none`), which runs the 5.2 upgrade's OpenSearch index pass in a post-upgrade Job of a 5.1 upgrade, and `olk.opensearch.indexUpgrade.activeDeadlineSeconds` (default `3600`), the deadline of that Job ([values][values-olk-index-upgrade]).

## 5.1.1 { #hopsworks-5-1-1 }

Helm chart 5.1.1 · Released on 2026-10-09 · Changes since [5.1.0][hopsworks-5-1-0] · Python client [5.1.1](https://github.com/logicalclocks/hopsworks-api/releases/tag/5.1.1)

### What's changed

- [API] Fixed `find_neighbors` in the Python client failing with `Engine [NMSLIB] does not support filters` on embedding feature groups created before 5.1, and failing on a project's default embedding index when fewer rows than `k` match.
- [API] [FRONTEND] Fixed Trino giving a project access to only one of several feature stores shared with it.
- [API] [FRONTEND] Fixed a killed Spark job with pending executors staying in the aggregating logs state for up to 20 minutes.
- [FRONTEND] [HELM] Fixed the post-upgrade search index rebuild failing without the admin password, for example when password login is disabled, and running on every upgrade; it now runs in the background once per index format, and shows its progress and a **Reindex now** button under **Cluster settings > Service Operations > OpenSearch Index Commands**.
  The first upgrade to 5.1.1 rebuilds the index, and search is incomplete until it finishes.
- [FRONTEND] Fixed the **Why?** button of an online ingestion in a feature group's activity opening every OnlineFS log of the project instead of that ingestion's; it is now named **Logs**.
- [HELM] Fixed the database migration of the upgrade from 5.0 failing when the feature groups have more than about 32,000 features in total.
- [HELM] Fixed OpenSearch losing unflushed vectors and rejecting vector writes for about two minutes on its first start on 5.1.
  A values file that sets `olk.opensearch.knn.circuit_breaker.triggered: true`, or an upgrade with `--reuse-values`, keeps the problem.
- [HELM] Fixed RonDB daemons ignoring SIGTERM, so every pod stop ended in a kill and a stopped data node could stall the cluster.
- [HELM] Changed the RonDB REST server probes to outlast a data node failure and to use their own port.
- [HELM] Fixed the RonDB REST server reading request bodies over 64 KiB as empty; it now buffers them in `rondb.rondb.rdrs.uploadPath`.
- [HELM] Fixed environment builds never starting when `rondb.rondb.priorityClass` is renamed.

### Breaking changes

- [API] [FRONTEND] Because of a security fix, Data Scientists ask the creator of a job or a Data Owner of the project to change it, other than its schedule.
- [HELM] The post-upgrade search index rebuild signs in as the agent user, instead of with `hopsworks.variables.admin_email` and `admin_password`, and fails the `helm upgrade` if `hopsworks.agent_email` and `hopsworks.agent_password` (default `agent@hops.io`, `admin`) don't match that account.
  Set them, or turn the rebuild off with `hopsworks.opensearchReindex.enabled: false`.
- [HELM] The RonDB REST server now uses a probe port and an upload path that need RonDB 26.02.11, where 5.1.0 probed its REST port and set no upload path.
  If you pin `rondb.rondb.images.rondb.tag` to an older version, set `rondb.rondb.rdrs.probePort.enabled: false` and `rondb.rondb.rdrs.uploadPath: ""`, or the REST server doesn't start.

### Upgraded components

| Component | 5.1.0 | 5.1.1 |
| --------- | ----- | ----- |
| Base environment images | 5.1.0 | 5.1.1 |
| RonDB | 26.02.10 | 26.02.11 |
| Trino | 480-v10 | 480-v11 |

### Configuration changes

- [HELM] Changed the default of `olk.opensearch.knn.circuit_breaker.triggered` from `true` to `false` and of `olk.opensearch.knn.circuit_breaker.percent` from `0.75` to `75`.
- [HELM] Changed the default of `hopsworks.variables.docker_operations_buildkit_priority_class` from `rondb-high-priority` to empty, so environment builds run at the default priority.
- [HELM] Changed `rondb.rondb.terminationGracePeriodSeconds` to one value per component, and the data nodes' default from 60 to 300 seconds; an integer still sets only the data nodes.
- [HELM] Fixed `values.openshift.yaml` for the OpenShift `restricted-v2` SCC, covering Strimzi, Kafka, ZooKeeper, the Spark operator and the MySQL and Redis of Superset, and turned off the Prometheus node exporter, which OpenShift ships itself.
  Use it with Helm 4 or Helm 3.17.1 or later, because older Helm 3 releases ignore its `null` overrides of subchart values.
- [HELM] Fixed the values schema rejecting `hopsworks.variables.loadbalancer_external_domain_namenode` and `hopsworks.variables.loadbalancer_external_domain_datanode`.
- [HELM] Added `hopsworks.opensearchReindex.enabled` to turn off the post-upgrade search index rebuild, and `hopsworks.variables.command_search_fs_reindex_queue_wait_as_ms` to bound its wait for the search command queue.
- [HELM] Added `rondb.rondb.rdrs.probes` and `rondb.rondb.rdrs.probePort`, the settings and the port of the RonDB REST server probes, and `rondb.rondb.rdrs.maxKeepaliveRequests` to close a keep-alive connection after that many requests, so clients rebalance after a rolling restart.
- [HELM] Added `nodePort` values to pin the node ports of unmanaged external load balancers: ArrowFlight, OpenSearch, the HopsFS NameNode and DataNodes, Trino, the Hive Metastore, Kafka (`bootstrapNodePort`, `startingNodePort`) and the RonDB MySQL and REST servers.
  The RonDB ones ignore `global._hopsworks.externalLoadBalancers.managed` and apply only when `rondb.rondb.meta.mysqld.externalLoadBalancer.managed` or `rondb.rondb.meta.rdrs.externalLoadBalancer.managed` is `false`.
- [HELM] Added `rondb.rondb.rdrs.ttlPurge.enable` and `activeWindow` to turn off the TTL purge of the RonDB REST server or limit it to a daily window.

## 5.1.0 { #hopsworks-5-1-0 }

Helm chart 5.1.0 · Released on 2026-09-24 · Changes since [5.0.0][hopsworks-5-0-0] · Python client [5.1.0](https://github.com/logicalclocks/hopsworks-api/releases/tag/5.1.0)

### What's changed

- [API] [FRONTEND] Addressed vulnerabilities in feature views (also in [5.0.8][hopsworks-5-0-8]).
- [API] [FRONTEND] Addressed vulnerabilities in project datasets (also in [5.0.10][hopsworks-5-0-10]).
- [API] Addressed vulnerabilities in model serving.
- [API] [HELM] Fixed online feature store ingestion skipping rows that failed with transient RonDB errors, such as `Rowid already allocated`, during a RonDB upgrade; it now pauses and retries every `onlinefs.configmapOverrides.onlinefssite.service.pauseRetrySleepMs` until they are written (also in [5.0.4][hopsworks-5-0-4]).
- [API] Fixed online feature store ingestion stalling for every project when a write exceeded the project's RonDB transaction size quota; OnlineFS now commits such a batch in smaller transactions.
- [API] Fixed online feature store ingestion stalling after a feature group with pending records was deleted (also in [5.0.2][hopsworks-5-0-2]).
- [API] [FRONTEND] Fixed Spark jobs failing to reach the remote shuffle service when an evicted coordinator pod was left behind.
- [API] Fixed the Python client installing PyMySQL 1.2.1 or later, with which `import hsfs` fails with an `ImportError`; it now requires PyMySQL below 1.2.1 (also in [5.0.12][hopsworks-5-0-12]).
- [API] Fixed writes to an online feature group failing after its table was truncated (also in [5.0.10][hopsworks-5-0-10]).
- [API] [FRONTEND] Added Apache Iceberg as a feature group table format (`time_travel_format="ICEBERG"`), also for feature groups created from Iceberg tables in a data source ([table format](https://docs.hopsworks.ai/5.1/user_guides/fs/feature_group/create/#table-format)).
- [API] [FRONTEND] Added partition transforms (`partitioned_by`) for Iceberg and Hudi feature groups, Delta liquid clustering (`clustered_by`), Hudi bucket indexes (`bucket_index`), z-ordering (`zorder_by`) and Iceberg sort orders (`sort_order`) ([partitioning](https://docs.hopsworks.ai/5.1/user_guides/fs/feature_group/partitioning/)).
- [API] [FRONTEND] [HELM] Added [model monitoring](https://docs.hopsworks.ai/5.1/user_guides/mlops/model_monitoring/), which compares the inference data a deployment logs with the model's training dataset and shows the drift on the deployment page, and [distribution comparison](https://docs.hopsworks.ai/5.1/user_guides/fs/feature_monitoring/distribution_comparison/) to feature monitoring, set up in the Python client with `create_model_monitoring` of a feature view, model or deployment and `compare_on_distribution`; `hopsworks.variables.feature_monitoring_max_num_features` (default `15`) caps the features of a configuration (also in [5.0.1][hopsworks-5-0-1]).
- [API] [FRONTEND] [HELM] Added Trino catalogs that project Data Owners create by hand or from a data source; Trino loads them at its daily scheduled restart (02:00 by default, only when a change is pending) or when an administrator restarts it, and tests them on a single-node coordinator (`global._hopsworks.trino.testCoordinator.enabled`); the Python client manages them with `project.get_trino_catalog_api()` and creates one from a data source with `create_trino_catalog()` of its `storage_connector` ([Trino catalogs](https://docs.hopsworks.ai/5.1/user_guides/projects/trino/catalogs/)).
- [API] [FRONTEND] Added dltHub ingestion jobs that copy several tables of a data source, each into its own feature group with its own settings and resources ([dltHub ingestion](https://docs.hopsworks.ai/5.1/user_guides/fs/feature_group/ingest_with_dlthub/)).
- [API] [FRONTEND] Added the AWS Glue data source ([AWS Glue](https://docs.hopsworks.ai/5.1/user_guides/fs/data_source/creation/glue/)).
- [API] [FRONTEND] Added the Google Sheets data source, which ingests spreadsheet tabs into feature groups with dltHub.
- [API] [FRONTEND] Added [chaining of on-demand transformation functions](https://docs.hopsworks.ai/5.1/user_guides/fs/feature_group/on_demand_transformations/#chaining-on-demand-transformations), where the output of one function feeds another, with a view of the chain on the feature group and feature view pages and from `visualize_transformations()` in the Python client, and `n_processes` of a feature group's `insert` and `save` to run independent transformations in parallel (also in [5.0.1][hopsworks-5-0-1]).
- [API] Added secondary indexes for online feature groups, declared with `secondary_indexes` in `OnlineConfig` of the Python client, or `secondaryIndexes` in the Java client, when the feature group is created (also in [5.0.1][hopsworks-5-0-1]).
- [API] [FRONTEND] [HELM] Added tags to jobs and apps (`Job.add_tag` and the other tag methods of `Job` in the Python client, and `hops fv` and `hops job` `tags`, `add-tag` and `remove-tag`), the time each tag and keyword was attached (`get_tag_metadata` and `get_keywords_metadata` of feature groups and feature views), and jobs, models, deployments, apps and agents to search; administrators can inspect and cancel stuck search index commands under **Cluster settings > Service Operations** ([tags](https://docs.hopsworks.ai/5.1/user_guides/fs/tags/tags/), [search index](https://docs.hopsworks.ai/5.1/setup_installation/admin/search_index/)).
- [API] [FRONTEND] [HELM] Added Git repositories as a source for agent deployments (`git_url`, `git_provider` and `git_branch` of `deploy_agent` in the Python client), token prices per deployment to estimate the LLM cost (`input_token_price_per_million_tokens` and `output_token_price_per_million_tokens` of `DeploymentTracingConfig`), and dashboards of traces, LLM calls, tokens, cost and tool calls ([agent deployments][docs-agent-deployments-git]) (also in [5.0.1][hopsworks-5-0-1]).
  Agent deployments now mount HopsFS, which on clusters with Kyverno needs `hw-kyverno.policyExceptions.pythonDeployment.enabled` (default `true`).
- [API] [FRONTEND] Added **Auto-redeploy on new commits** to Python apps and agent deployments from a Git repository, which rolls them to each new commit of the tracked branch; set it with `git_auto_redeploy` in the Python client or `--git-auto-redeploy` of `hops app create` ([apps][docs-apps-auto-redeploy]).
- [API] [FRONTEND] [HELM] Added an app base path, a proxy routing mode and a readiness probe path to [apps](https://docs.hopsworks.ai/5.1/user_guides/projects/apps/), set in the Python client with `app_base_path` and `readiness_probe_path` of `create_app`, so an app can be served from its root without `APP_BASE_URL_PATH`; existing apps keep the prefix routing, and the App Metrics Grafana dashboard shows zero instead of "No data" for apps without traffic (also in [5.0.1][hopsworks-5-0-1]).
- [API] Added uploading a local `script_file` or `config_file` of a predictor or transformer to the project when the deployment is saved, such as by `model.deploy()`, in the Python client, and fixed updating a deployment's transformer script to a full HopsFS path failing with script not found.
- [API] [FRONTEND] Added deleting rows from a feature group with `remove_rows` in the Python client and `removeRows` in the Java client, which delete from both stores of an online feature group unless `storage` is `"offline"` or `"online"`; online ingestion results and the ingestion activity in the UI show them as deleted rows (also in [5.0.8][hopsworks-5-0-8]).
- [API] Added project member management (`Project.get_members`, `add_member`, `remove_member`), feature group access for members with the Feature store restricted role (`FeatureGroup.grant_restricted_access`, `revoke_restricted_access`, `get_restricted_access`) and user administration (`hopsworks.get_users_api()`) to the Python client ([users](https://docs.hopsworks.ai/5.1/setup_installation/admin/user/#python-sdk), [members](https://docs.hopsworks.ai/5.1/user_guides/projects/project/manage_members/#python-sdk), [sharing](https://docs.hopsworks.ai/5.1/user_guides/fs/sharing/sharing/#using-the-api-to-share-a-feature-group)) (also in [5.0.8][hopsworks-5-0-8]).
- [API] Added `OnlineIngestion.get_failures()` to the Python client, which lists the rows an online ingestion failed to write and why, and changed inserts into online feature groups to fail when Kafka doesn't deliver a row, such as one over the broker's maximum message size, instead of only on authorization errors and timeouts.
- [API] Added support for the `storage` argument of `FeatureGroup.insert` on stream feature groups, which ignored it with a warning: `"online"` now writes the rows only to the online store and `"offline"` only to the offline store.
- [API] [FRONTEND] Added [mandatory tags](https://docs.hopsworks.ai/5.1/user_guides/fs/tags/mandatory_tags/) for models and deployments, and tags on deployments, which the Python client sets with `Deployment.add_tag` and reports in `missing_mandatory_tags` of a model or deployment (also in [5.0.2][hopsworks-5-0-2]).
  Model tags move from HopsFS to the database the first time a model is read or tagged after the upgrade, and a tag that no longer matches its schema is dropped.
- [API] [FRONTEND] Added key pair authentication to DLT ingestion from Snowflake, which accounts that enforce MFA need ([Snowflake data source][docs-snowflake]) (also in [5.0.14][hopsworks-5-0-14]).
- [API] [FRONTEND] [HELM] Added an upload policy, `hopsworks.variables.upload_policy`, that allows file uploads to everyone (`enabled`), to administrators only (`admins_only`) or to nobody (`disabled`), from the web UI and from clients such as the Python SDK; the web UI disables its upload controls for blocked users, and `upload(overwrite=True)` in the Python client no longer deletes the existing file when the policy blocks the upload (also in [5.0.8][hopsworks-5-0-8]).
  The upgrade writes the value to the cluster, so a change made in the admin UI lasts until the next upgrade.
- [API] [FRONTEND] Added the GitHub Copilot and OpenCode CLIs to the web terminal, next to Claude Code and Codex; the coding agents share the skills in your home directory, which `hops skills list` now lists, and keep their logins and sessions across terminal sessions (also in [5.0.10][hopsworks-5-0-10]).
- [API] [FRONTEND] Added GitHub Copilot as a provider of agent tasks, signed in with the token of a GitHub AI provider or of your github.com Git provider, which can't be a classic personal access token (also in [5.0.10][hopsworks-5-0-10]).
- [API] [FRONTEND] [HELM] Removed the per-project Hive database (`<project>.db`) and its quota from new projects; existing projects keep theirs.
- [API] Changed model deployments, jobs, Jupyter servers and terminals to each get their own serving API key.
- [API] Changed feature group schemas to be read from the Hopsworks database instead of the Hive Metastore; existing feature groups move over in the background after the upgrade.
- [API] Changed `GET /project/{id}/jupyter/running` to return `204 No Content` instead of `404` when no Jupyter server is running (also in [5.0.10][hopsworks-5-0-10]).
- [API] Changed `import hopsworks` to no longer import great_expectations when it is installed, which made the import take about 9 seconds instead of under 1.
- [API] Removed the Python client's dependency on pyjks, which can't read JDK 21 keystores; the client now reads Java keystores itself.
- [API] Changed training dataset creation on Spark to skip reading the written splits back when statistics are off (`statistics_config=False`), the slowest step for a large training dataset.
- [API] Added the `hops alert` commands to the `hops` CLI, for the alerts and receivers of a project, job, feature group or feature view.
- [API] Added `--verify` and `--no-verify` to the `hops` CLI, which turn hostname verification on or off as `hopsworks.login(hostname_verification=...)` does, also for the Trino connection of `hops sql`.
- [API] [FRONTEND] Added **Driver overhead factor** and **Executor overhead factor** to the Spark configuration of jobs, Jupyter and project defaults, which set `spark.driver.memoryOverheadFactor` and `spark.executor.memoryOverheadFactor`, also as `driver_memory_overhead_factor` and `executor_memory_overhead_factor` of `JobConfiguration` in the Python client ([PySpark jobs](https://docs.hopsworks.ai/5.1/user_guides/projects/jobs/pyspark_job/)) (also in [5.0.12][hopsworks-5-0-12]).
  Jupyter Spark sessions now default both to `0.4`, as PySpark jobs do, so notebooks and their executors request more memory than before.
- [API] [FRONTEND] [HELM] Added toolchain caches (`HOPSWORKS_BUILD_CACHE`), layer reuse for scripts that fetch nothing that changes (`HOPSWORKS_BUILD_HERMETIC`), when `hopsworks.variables.docker_operations_allow_hermetic_custom_commands` is `"true"`, and secret references (`NAME=secret:<secret>`) to custom commands ([custom commands](https://docs.hopsworks.ai/5.1/user_guides/projects/python/custom_commands/#making-custom-command-builds-faster)).
- [API] Fixed inserts into online feature groups waiting until the online ingestion timeout when the Python client writes some rows only to the offline store, such as earlier duplicates of a primary key or rows past the feature group's TTL; these rows now show as ignored.
- [API] Fixed inserts with the `upsert_if_newer` online ingestion option failing for online feature groups with a composite primary key (also in [5.0.8][hopsworks-5-0-8]).
- [API] Fixed reads through the Hopsworks Query Service failing with "Could not read data using Hopsworks Query Service" when a filter on a numeric partition column meets a partition whose value is null, such as `read_log` of a feature view filtered by model.
- [API] Fixed `hops env install -f` failing unless run from the project's mount; `-f` now takes a local requirements file, which it uploads to the project, or a path in the project.
- [API] Fixed the Python client waiting forever on a library install or environment creation that never finishes; it now raises after waiting 30 minutes, also while the command is still running, so pass a larger `timeout` to `create_environment`, `install_wheel`, `install_requirements` or `uninstall` for longer installs.
- [API] Fixed Trino connections of external Python clients with `verify=True` failing with `unable to get local issuer certificate`; they now verify against the cluster's CA.
- [API] Fixed online feature vectors failing with a `ValueError` on `TIMESTAMP(n)` and `DATETIME(n)` features with fractional seconds, and similarity search results losing the milliseconds of timestamps (also in [5.0.8][hopsworks-5-0-8]).
- [API] Fixed `SnowflakeConnector.connector_options()` in the Python client failing for a data source with key pair authentication, and leaving out the role set on the data source (also in [5.0.14][hopsworks-5-0-14]).
- [API] [FRONTEND] Fixed the deployment test, the endpoint addresses and code snippets of deployments, their metrics dashboard, and predictions and endpoint URLs in the Python client using the project name instead of its Kubernetes namespace, which broke them on clusters with pre-created namespaces.
- [API] [FRONTEND] Fixed model deployments with images from the managed Docker registry failing to start (also in [5.0.1][hopsworks-5-0-1]).
- [API] Fixed `Project.project_namespace` in the Python client always returning `None`.
- [API] Fixed feature logging and feature monitoring on feature views with model-dependent transformations, such as one-hot encoding.
- [API] Fixed model monitoring without a `feature_name` failing against a training dataset reference, because it also monitored the serving keys, predictions and logging metadata columns; it now monitors the model's training features.
- [API] Fixed creating a training dataset with `coalesce=True` on Spark failing with `SparkOutOfMemoryError`, even on small datasets, when it has transformation functions or a time series split.
- [API] Fixed training datasets created with the Python engine ignoring an external data source or path and being written to the default location.
- [API] Fixed statistics computation on Spark failing on a numeric column whose values are all NaN, and computing a wrong histogram for a numeric column with any NaN.
- [API] Fixed transformation functions defined inside another function failing with an `IndentationError` when applied.
- [API] Fixed `get_tag` and `get_tags` of feature groups, feature views, training datasets, models and datasets in the Python client failing with a `TypeError` when a tag value is not a plain string, and `get_tag` of models always failing (also in [5.0.2][hopsworks-5-0-2]).
- [API] Fixed `share`, `shared_with` and `unshare` of feature groups and feature stores, and `DatasetApi.unshare`, failing in the Python client (also in [5.0.8][hopsworks-5-0-8]).
- [API] Fixed assigning `Job.config` in the Python client failing.
- [API] Fixed creating an agent task with `JobApi.create_job` in the Python client failing with `'appPath' not set in job configuration` (also in [5.0.10][hopsworks-5-0-10]).
- [API] Fixed `find_neighbors` in the Python client returning fewer than `k` neighbors when at least `k` rows match a `filter` or share the project's embedding index with other feature groups, for embedding feature groups created on 5.1.
- [API] Fixed random splits of training datasets with the Python engine ignoring `seed`, so they were not reproducible (also in [5.0.2][hopsworks-5-0-2]).
- [API] Fixed importing the Python client reseeding Python's global `random` module (also in [5.0.2][hopsworks-5-0-2]).
- [API] [FRONTEND] Fixed feature statistics failing to save when a column has a NaN or infinite statistic, such as the standard deviation of an all-null column, statistics of DELTA feature groups being computed on the previous commit, and wrong uniqueness statistics, which are now left empty when `exact_uniqueness` is off (also in [5.0.9][hopsworks-5-0-9]).
- [API] Fixed API keys created by `hops setup` lacking the `KAFKA`, `PYTHON_LIBRARIES`, `GIT`, `TRINO` and `SUPERSET` scopes, so they could not insert into online feature groups.
- [API] [FRONTEND] Fixed Ray jobs and the Ray clusters of Jupyter failing to start on OpenShift, because their pods couldn't read the project certificates (also in [5.0.9][hopsworks-5-0-9]).
- [API] [FRONTEND] Fixed adding a member to a project failing when feature groups are shared with that project (also in [5.0.1][hopsworks-5-0-1]).
- [API] [FRONTEND] [HELM] Fixed deleting a feature group failing after many online ingestions; Hopsworks now keeps the latest 1000 online ingestions of each feature group (cluster variable `online_ingestion_max_per_featuregroup`) (also in [5.0.2][hopsworks-5-0-2]).
- [API] Fixed offline reads of a feature view or query that includes a spine group failing with an HTTP 500 error (also in [5.0.13][hopsworks-5-0-13]).
- [API] Fixed reads of external feature groups in the Python engine failing when they leave out a feature appended to the feature group (also in [5.0.14][hopsworks-5-0-14]).
- [API] Fixed Snowflake reads through the Hopsworks Query Service, such as Python engine reads, using the Snowflake user's default role instead of the role set on the data source (also in [5.0.14][hopsworks-5-0-14]).
- [API] Fixed enabling feature logging failing with a duplicate column on feature views with two serving keys from one feature group, or with an event time as a serving key.
- [API] [FRONTEND] [HELM] Fixed a read from an unreachable data source blocking with nothing logged; it now fails after 180 seconds (cluster variable `arrow_flight_read_timeout_as_ms`) with an error that names the data source.
- [API] [FRONTEND] Fixed deleting a user right after deleting their projects failing with a generic error; it now returns a conflict that says to retry.
- [API] [FRONTEND] Fixed failed or partly deleted projects counting against the owner's maximum number of projects (also in [5.0.1][hopsworks-5-0-1]).
- [API] [FRONTEND] Fixed ingestion with dltHub and schema fetching from NoSQL data sources failing when the project, data source or table names are long (also in [5.0.1][hopsworks-5-0-1]).
- [API] [FRONTEND] Fixed the state of a Spark or Ray job execution switching between queued and running while one of its pods couldn't be scheduled (also in [5.0.9][hopsworks-5-0-9]).
- [API] [FRONTEND] Fixed Git operations failing to authenticate when a provider token or password contains special characters (also in [5.0.10][hopsworks-5-0-10]).
  The upgrade converts the saved credentials; if a provider still fails, save it again in your account settings.
- [API] [FRONTEND] Fixed agent tasks that run at the same time failing to sign in to Claude Code, because they shared one credentials file (also in [5.0.10][hopsworks-5-0-10]).
- [API] Fixed Arrow Flight queries of partitioned DELTA feature groups failing once the feature group is older than `delta.logRetentionDuration` (also in [5.0.8][hopsworks-5-0-8]).
- [API] [FRONTEND] Fixed DLT ingestion rejecting a load whose decimal values are narrower than the precision of the source column (also in [5.0.14][hopsworks-5-0-14]).
- [FRONTEND] Fixed uploading files in the file browser deleting the files of the previous upload unless the page was reloaded (also in [5.0.10][hopsworks-5-0-10]).
- [FRONTEND] [HELM] Added file-based credentials, such as Oracle wallets, for user-created Trino catalogs: a project uploads them as mountable secrets, and a privileged sidecar on every Trino pod mounts `/apps/mountable-secrets` from HopsFS read-only ([credential files](https://docs.hopsworks.ai/5.1/setup_installation/admin/trino/#credential-files-a-project-supplies)).
- [FRONTEND] [HELM] Changed environment builds to install libraries with uv when the image has it, to read the library list from the built image instead of starting three more Jobs, and to show the stage of a running build.
- [FRONTEND] [HELM] Added npm packages to Python environments, installed globally and on `PATH` for jobs, Jupyter and the terminal; set `hopsworks.variables.npm_registry_url` to install from a registry other than registry.npmjs.org ([installing libraries](https://docs.hopsworks.ai/5.1/user_guides/projects/python/python_install/)).
- [FRONTEND] [HELM] Added the `dbt-pipeline` environment, with dbt and its Trino and DuckDB adapters.
- [FRONTEND] [HELM] Added the online feature store (RonDB) quotas and memory usage to the project settings, a banner on project pages near or over quota, and a Quotas and Rate Limits page in the cluster settings for the defaults of new projects; HopsFS quotas are now labelled GB instead of TB, the unit they always had (also in [5.0.1][hopsworks-5-0-1]).
  Default RonDB quotas in `hopsworks.variables.rondb_quotas` now apply to new projects; usage refreshes every `hopsworks.variables.rondb_usage_cache_ttl_seconds`, and on a large cluster raise `rondb_usage_query_timeout_seconds` if usage stops showing.
- [FRONTEND] Added a Copilot tab and a Business Glossary for each coding agent to the Agents page of the cluster settings, now called Coding Agents (also in [5.0.10][hopsworks-5-0-10]).
- [FRONTEND] [HELM] Added a load status to alert receivers and to the AlertManager configuration, which shows a change AlertManager has not loaded yet or rejected, and linked the alert title in AlertManager emails to the job, feature group or feature view that raised it ([receiver load status](https://docs.hopsworks.ai/5.1/user_guides/projects/alerts/#receiver-load-status)).
- [FRONTEND] Changed projects created without the `Users` dataset to get it, with a home folder for each member, automatically after the upgrade, instead of asking the data owner to enable private user directories (also in [5.0.2][hopsworks-5-0-2]).
- [FRONTEND] Added the status of the TTL purge of online feature groups: a TTL purge card on the feature group overview and a TTL Purge page in the cluster settings (also in [5.0.10][hopsworks-5-0-10]).
- [FRONTEND] Added a read-only `featurestore` directory to the web terminal with the files of the project's offline feature store (also in [5.0.10][hopsworks-5-0-10]).
- [FRONTEND] Added a **Monitor** button to each running Spark application on the Jupyter page, showing its driver and executor pods, and fixed the Jupyter server monitor showing a Spark executor as the notebook pod; the Grafana link there and in the job drawer menu is now called **Metrics** (also in [5.0.12][hopsworks-5-0-12]).
- [FRONTEND] Added a **Why?** action to online ingestions with failed or ignored rows in the feature group activity, which explains the two counts and links the OnlineFS log entries in OpenSearch Dashboards.
- [FRONTEND] Added a **Stop** button to the SQL Runner, and leaving the SQL Runner now stops the running query; the run status shows the elapsed time and the rows the query engine processed (also in [5.0.14][hopsworks-5-0-14]).
- [FRONTEND] Added the full color palette, interface styles such as border radius, border width and shadows, a live preview, and a branding export, import and reset to the Branding page of the cluster settings, shown when the cluster variable `enable_custom_branding` is `true` (also in [5.0.6][hopsworks-5-0-6]).
- [FRONTEND] Changed the Trino connections that Hopsworks creates in Superset to allow changing catalogs, so SQL Lab can query any Trino catalog; existing connections are unchanged ([Superset](https://docs.hopsworks.ai/5.1/user_guides/projects/superset/superset/)).
- [FRONTEND] Changed the Claude Code settings that Hopsworks creates for new project members to auto mode, so agent sessions in the terminal run without a prompt per tool call; existing settings are unchanged.
- [FRONTEND] Changed the options of the feature group delete dialog to the short labels **Force delete** and **Cascade delete**, with their descriptions in tooltips.
- [FRONTEND] Removed the Plans dialog from the web terminal (also in [5.0.10][hopsworks-5-0-10]).
- [FRONTEND] [HELM] Fixed the Jupyter server of Spark environments running out of memory: it now adds the driver memory overhead of the session's Spark configuration and a floor (`hopsworks.variables.jupyter_spark_notebook_server_memory_floor_mb`) to the driver memory (also in [5.0.10][hopsworks-5-0-10]).
- [FRONTEND] Fixed the project home page crashing with "Something went wrong while loading this page" because of the Feature usage card (also in [5.0.10][hopsworks-5-0-10]).
- [FRONTEND] Fixed project pages showing a "Feature not enabled: DATA_SCIENCE_PROFILE" error when the data science profile is off; the model registry, deployments and apps are now hidden from the menu (also in [5.0.1][hopsworks-5-0-1]).
- [FRONTEND] Fixed `kubectl` failing in every web terminal, because terminals never got a kubeconfig (also in [5.0.10][hopsworks-5-0-10]).
- [FRONTEND] Fixed web terminals failing to start on OpenShift (also in [5.0.9][hopsworks-5-0-9]).
- [FRONTEND] Fixed web terminals shutting down after about 30 minutes in a background browser tab or on a sleeping laptop; a terminal now stops only when its session expires (also in [5.0.1][hopsworks-5-0-1]).
- [FRONTEND] Fixed project membership changes being slow, and Airflow requests timing out or failing with server errors, when Airflow is turned off (`global._hopsworks.airflow.enabled: false`) (also in [5.0.1][hopsworks-5-0-1]).
- [FRONTEND] Fixed giving project members access to Superset failing with HTTP 429 (Too Many Requests) errors (also in [5.0.1][hopsworks-5-0-1]).
- [FRONTEND] [HELM] Fixed Superset redirecting to its internal host behind a reverse proxy that rewrites the Host header; set `hopsworks.variables.hopsworks_public_proxy_url` to the public `host[:port]` (also in [5.0.1][hopsworks-5-0-1]).
- [FRONTEND] Fixed Spark executors started from Jupyter having no CPU limit and rounding fractional executor cores up to a whole core; they now get the executor cores of the session as request and limit, as job executors do (also in [5.0.10][hopsworks-5-0-10]).
- [FRONTEND] Fixed Jupyter servers on the `agent-job` environment losing their priority class, node affinity and Kueue queue.
- [FRONTEND] Fixed environment variables set in an app's configuration not reaching the app, and not showing when you edit the app (also in [5.0.1][hopsworks-5-0-1]).
- [FRONTEND] [HELM] Fixed `pip install` and `uv pip install` in the web terminal, and `uv pip install` in Jupyter and Ray, ignoring the index, mirror and proxy settings in `hopsworks.dockerImage.pypi.global_parameters` (also in [5.0.2][hopsworks-5-0-2]).
- [FRONTEND] Fixed saving the Alertmanager configuration in the admin UI silently failing when it sets a boolean or numeric option, such as `smtp_require_tls` or `max_alerts` (also in [5.0.2][hopsworks-5-0-2]).
- [FRONTEND] Fixed the data preview of a feature view's logging feature group failing (also in [5.0.2][hopsworks-5-0-2]).
- [FRONTEND] Fixed creating or editing a BigQuery data source failing with a gRPC error when the form lists the GCP projects (also in [5.0.10][hopsworks-5-0-10]).
- [FRONTEND] Fixed the create and edit forms of model and LLM deployments: a hidden tracing field could block saving, the vLLM image tag could stay blank, and editing a deployment reset its resources (also in [5.0.6][hopsworks-5-0-6]).
- [FRONTEND] Fixed the **SQL Runner** returning a different number of rows on each run, ignoring the row limit for some queries and discarding the typed query when the limit changed; it now shows the row count of a result (also in [5.0.8][hopsworks-5-0-8]).
- [FRONTEND] Fixed long query plans and table definitions overflowing the SQL Runner results panel instead of scrolling (also in [5.0.14][hopsworks-5-0-14]).
- [FRONTEND] Fixed feature monitoring charts not showing the standard deviation (also in [5.0.6][hopsworks-5-0-6]).
- [FRONTEND] Fixed project members with the Observer role being offered Superset actions that fail; the UI now disables them (also in [5.0.8][hopsworks-5-0-8]).
- [FRONTEND] Fixed the web terminal retrying a session that had shut down on its timeout instead of offering to restart it.
- [FRONTEND] Fixed pages showing a generic `Error occurred.` message after the computer woke from sleep.
- [FRONTEND] Fixed the BigQuery data source form accepting a missing BigQuery project, which then failed when creating a feature group.
- [FRONTEND] Fixed the Avg REST API Latency panel of the project metrics page showing no data.
- [HELM] Fixed RonDB data nodes reporting ready while the management server is unreachable, which let a rollout stop the healthy data node of the same node group and shut the cluster down; their liveness probe also no longer kills them then (also in [5.0.11][hopsworks-5-0-11]).
- [HELM] Fixed RonDB rolling restarts making healthy data nodes shut down; data nodes now wait for the rollout to settle (`rondb.rondb.ndbmtdSettleWait`) (also in [5.0.11][hopsworks-5-0-11]).
- [HELM] Fixed the Airflow migration Job losing tables on clusters with more than one RonDB MySQL server, so the upgrade never completed; it now uses only the DDL MySQL server (also in [5.0.13][hopsworks-5-0-13]).
  A cluster whose earlier upgrade already failed this way needs the Airflow schema dropped on every MySQL server before it upgrades again.
- [HELM] Fixed a failed HopsFS schema migration being reported as successful, which let the NameNode start on a partly migrated schema (also in [5.0.2][hopsworks-5-0-2]).
- [HELM] Fixed the RonDB MySQL setup and in-place restore Jobs failing for good when data nodes took more than about two hours to start, and the MySQL servers crash-looping while they wait for a backup restore (also in [5.0.11][hopsworks-5-0-11]).
- [HELM] Fixed database initialization and migrations starting while RonDB was still restarting; they now wait for each RonDB StatefulSet to roll out (also in [5.0.1][hopsworks-5-0-1]).
- [HELM] Fixed init containers that wait for a RonDB rollout giving up after 30 minutes, which failed the Hive Metastore, HopsFS, Airflow migration and CA pods when a RonDB restart took longer (also in [5.0.10][hopsworks-5-0-10]).
- [HELM] Fixed database migrations crash-looping on a lock left by a transient Kubernetes API error.
- [HELM] Fixed Velero backups leaving out the Trino authentication Secrets.
- [HELM] Fixed `helm install` failing with Velero backups to AWS S3 that set no custom S3 endpoint.
- [HELM] Fixed every model deployment failing when the Knative controller started with an empty registry certificate.
- [HELM] Fixed image pulls from the in-cluster Docker registry failing with `x509: certificate signed by unknown authority`, for example on RHEL-family nodes.
- [HELM] Fixed OpenSearch snapshot restores never finishing on single-node clusters, and indices staying closed after a failed restore.
- [HELM] Fixed the Hopsworks admin pod getting stuck in CrashLoopBackOff when workers were slow to register; the admin sidecar now keeps retrying, restarts unregistered workers and redeploys Hopsworks after the admin container restarts (also in [5.0.3][hopsworks-5-0-3]).
- [HELM] Fixed Airflow failing to start on OpenShift with `airflow: command not found` (also in [5.0.6][hopsworks-5-0-6]).
- [HELM] Fixed service logs being dropped from the `.services` OpenSearch index when Kubernetes labels pushed it past 1000 fields (also in [5.0.12][hopsworks-5-0-12]).
- [HELM] Fixed Kafka failing to start on clusters with many API groups, such as OpenShift, when the Vertical Pod Autoscaler (`global._hopsworks.vpaEnabled`) is on, because pod creation stalled for about 20 seconds (also in [5.0.8][hopsworks-5-0-8]).
- [HELM] Fixed OnlineFS upgrades stalling on a full node pool: with two or more `onlinefs.deployment.replicas`, a rollout now replaces one pod at a time (also in [5.0.13][hopsworks-5-0-13]).
- [HELM] Changed the memory split of the remote shuffle servers to stop heap out-of-memory crashes: 20% of `spark.rss.shuffleServer.resources.limits.memory` is reserved for native memory and the rest is split 25% heap, 75% off-heap (also in [5.0.12][hopsworks-5-0-12]).
- [HELM] Fixed the remote shuffle servers never receiving their off-heap memory setting, which left their buffers about nine times too small (also in [5.0.12][hopsworks-5-0-12]).
- [HELM] Added an optional persistent BuildKit daemon (`global._hopsworks.buildkitd.enabled`) that keeps caches between environment builds; each replica requests 8 CPUs, 16Gi of memory and a 100Gi volume ([build performance](https://docs.hopsworks.ai/5.1/setup_installation/admin/build_performance/)).
- [HELM] Added support for Kubernetes 1.35 and 1.36 (also in [5.0.1][hopsworks-5-0-1]).
- [HELM] Added sequenced rollouts that restart the RonDB data nodes one node group at a time on clusters with more than one node group, turned on with `rondb.rondb.ndbmtdSequencedRollout.enabled` (default `false`) (also in [5.0.5][hopsworks-5-0-5]).
- [HELM] Added a lifecycle webhook that posts user, project and membership events to `hopsworks.variables.lifecycle_webhook_url`, tagged with `lifecycle_webhook_cluster_id` and signed with HMAC-SHA256 when `lifecycle_webhook_secret` is set (also in [5.0.1][hopsworks-5-0-1]).
- [HELM] Added support for Git repositories behind a private CA or an HTTP proxy: set `hopsworks.variables.git_custom_ca_configmap` to a ConfigMap that exists in every project namespace, `git_<provider>_http_proxy` and `git_<provider>_https_proxy` for GitHub, GitLab and BitBucket, or `git_disable_tls_verification` (also in [5.0.10][hopsworks-5-0-10]).
- [HELM] Added an external LoadBalancer for the Hive Metastore, turned on with `hive.externalLoadBalancer.enabled` (default `false`), so that clients outside Kubernetes, such as external Spark applications, can reach it (also in [5.0.1][hopsworks-5-0-1]).
- [HELM] Added the `KafkaAuthenticationFailures` Prometheus alert for clients that keep failing to authenticate, for example with an expired certificate (also in [5.0.10][hopsworks-5-0-10]).
- [HELM] Added post-delete Jobs that remove the Secrets, ConfigMaps and certificates `helm uninstall` used to leave behind (also in [5.0.2][hopsworks-5-0-2]).
- [HELM] Changed Grafana to load the Hopsworks dashboards from its image instead of ConfigMaps; add your own with `global._hopsworks.grafana.extraDashboardProviders`.
  A custom `grafana.grafana.dashboardProviders` must point to `/usr/share/grafana/dashboards/<folder>`.
- [HELM] Changed upgrades to update the KServe, Knative Serving and cert-manager CRDs in a pre-upgrade Job, which removes the unused `predictors.serving.kserve.io` CRD.
- [HELM] Changed environment image builds to the `rondb-high-priority` priority class (`hopsworks.variables.docker_operations_buildkit_priority_class`), so they can preempt Jupyter and job pods.
- [HELM] Changed Spark metrics to be scraped by Prometheus instead of pushed to the Pushgateway.
- [HELM] Changed the Kafka Entity Operator, when `kafka.cluster.entityOperator` is set, to follow the tolerations, topology spread and node affinity of the Kafka brokers, unless set under `kafka.cluster.entityOperator.template.pod` (also in [5.0.11][hopsworks-5-0-11]).
- [HELM] Changed OpenSearch snapshots and restores to skip the `.opendistro_security` index and hidden plugin indices.
- [HELM] Fixed environment builds against the managed Docker registry ignoring `hopsworks.variables.docker_operations_push_insecure` and failing on a self-signed certificate; set the new `hopsworks.variables.docker_operations_registry_http` to `"true"` for a registry served over plain HTTP (also in [5.0.1][hopsworks-5-0-1]).
- [HELM] Fixed Superset queries through Trino logging `Access Denied: Cannot access catalog system`, and project creation and new project members logging Trino `Access Denied: Invalid credentials` errors before their Superset connection is ready (also in [5.0.8][hopsworks-5-0-8]).
- [HELM] Fixed the Kyverno restricted policies blocking schema fetches of REST and CRM data sources.
- [HELM] Fixed the KServe local model controller image (`kserve.kserve.localmodel.enabled`) failing to pull (also in [5.0.9][hopsworks-5-0-9]).
- [HELM] Fixed the OpenSearch metrics exporter reporting the parent cluster on a satellite deployment, and missing OpenSearch with a custom `global._hopsworks.consulDomainName` (also in [5.0.13][hopsworks-5-0-13]).
- Addressed vulnerabilities in the Hopsworks server dependencies and in the Superset, Grafana, Prometheus, Consul, certificates operator, Docker registry, BuildKit, Istio, Knative Serving, KServe utilities, scikit-learn model server, Strimzi, OpenSearch, OpenSearch Dashboards, Logstash, Filebeat, Spark operator, KubeRay operator, Vertical Pod Autoscaler installer, Spark history server, Hive Metastore, model serving webhook, model serving authenticator, inference logger, storage initializer, remote shuffle service, Git and base environment images.
- Addressed vulnerabilities in the Hopsworks server dependencies, in the Payara, HopsFS, Hive Metastore, ArrowFlight, OnlineFS, Airflow, Git, toolbox, base environment, Filebeat, Grafana, OpenSearch, OpenSearch Dashboards, Logstash, remote shuffle service, Spark history server and Superset images, and in the MySQL database of Superset (also in [5.0.8][hopsworks-5-0-8]).
- Addressed vulnerabilities in the Hopsworks and Hopsworks CA images (also in [5.0.6][hopsworks-5-0-6] and [5.0.9][hopsworks-5-0-9]).
- Addressed vulnerabilities in the MySQL database of Superset (also in [5.0.1][hopsworks-5-0-1]).
- Addressed vulnerabilities in the Strimzi operator and Kafka images (also in [5.0.3][hopsworks-5-0-3]).
- Addressed vulnerabilities in the ArrowFlight and remote shuffle service images (also in [5.0.10][hopsworks-5-0-10]).
- Fixed Python jobs, notebooks, apps and agent tasks crashing with a segmentation fault when they list or change the owner of a HopsFS directory through pydoop (also in [5.0.9][hopsworks-5-0-9]).
- Fixed `npm install -g` and `corepack enable` failing for the non-root user in jobs, notebooks, apps and deployments that run on the base environment images (also in [5.0.1][hopsworks-5-0-1]).
- Changed the base environment images to Node.js 26.7.0, instead of 20 (also in [5.0.1][hopsworks-5-0-1]).
- Changed LLM deployments to no longer get the inference logger sidecar, which they never used (also in [5.0.2][hopsworks-5-0-2]).

### Breaking changes

- [API] [FRONTEND] [HELM] Removed Brewer; remove `global._hopsworks.brewer`, `brewer`, `hopsworks.ingress.brewer`, `hopsworks.variables.brewer_*` and `hw-kyverno.policyExceptions.brewer` from your values, because the values schema rejects them.
  With `--reuse-values`, which keeps the 5.0 defaults such as `brewer`, use `--reset-then-reuse-values`.
- [API] [HELM] Spark is upgraded from 3.5 to 4.1, which is built for Scala 2.13; rebuild job JARs built for Scala 2.12, and check your jobs against the [Spark migration guide](https://spark.apache.org/docs/latest/migration-guide.html).
  The Java client now needs Java 17 instead of Java 8, and its Spark artifact is `hsfs-spark-spark4.1` instead of `hsfs-spark-spark3.5`; update your build.
- [API] Hudi feature groups move to Hudi table version 9 on their first write from 5.1, instead of version 8, so Spark outside Hopsworks that reads them with Hudi 1.0, such as with the 5.0 hsfs-spark artifact, can no longer read them; upgrade those readers to the 5.1 Java client or Hudi 1.2.
- [API] `find_neighbors` in the Python client fails with `Engine [NMSLIB] does not support filters` on embedding feature groups created before 5.1, which it searched on 5.0; upgrade to [5.1.1][hopsworks-5-1-1] instead.
- [API] In the Python client, `create_feature_monitoring` no longer takes `feature_name` and `create_statistics_monitoring` is now `create_scheduled_statistics`, which takes `feature_names`, on feature groups and feature views, because one configuration now monitors several features, each named with `compare_on(feature_name=...)` (also in [5.0.1][hopsworks-5-0-1]).
  Also replace `with_reference_value(value)` with `compare_on(..., specific_value=value)` and `run_job()` with `run_once()`, pass `strict` and `relative` to `compare_on` by name, and read the results of each feature from `feature_statistics_results`; see [Feature monitoring][docs-feature-monitoring].
- [API] `hops fg keywords`, `add-keyword` and `remove-keyword` now work on keywords instead of tags, and `add-keyword --value` fails; use `hops fg tags`, `add-tag` and `remove-tag` for name/value tags.
- [API] [FRONTEND] Hopsworks now rejects a KServe deployment that sets the `PYTHONPATH` environment variable, which 5.0 accepted and KServe 0.19 blocks, and a job, deployment or user environment variable named `PYTHON_BIN`, which Hopsworks now sets on deployments itself; remove them.
- [API] [FRONTEND] Removed library installs from a conda channel, an `.egg` file or an `environment.yml` file, because the base environments are now uv virtualenvs without conda; use pip, a wheel, a Git repository, a `requirements.txt` file or custom commands instead ([installing libraries](https://docs.hopsworks.ai/5.1/user_guides/projects/python/python_install/)).
- [FRONTEND] [HELM] Rotate the credentials in `hopsworks.dockerImage.packageAuth.secretName` and the Git tokens of the private Git repositories that environments install libraries from, then rebuild the environments built from custom commands or from such a repository, to address a vulnerability.
- [FRONTEND] Removed the Code Style, Testing and Security rules from the Coding Agents page of the cluster settings, and web terminals no longer give them to the coding agents (also in [5.0.10][hopsworks-5-0-10]).
  If you set them, move what you need to the new Business Glossary or the system-wide instructions of each agent.
- [HELM] Raised the minimum Kubernetes version from 1.27 to 1.34; upgrade Kubernetes first, because Helm refuses to install or upgrade on an older cluster.
- [HELM] OpenSearch drops vectors not yet flushed and rejects vector writes for about two minutes on its first start on 5.1, because of the default `olk.opensearch.knn.circuit_breaker` settings; set `triggered: false` and `percent: 75` under it, or upgrade to [5.1.1][hopsworks-5-1-1] instead.
- [HELM] `helm uninstall` now deletes the data volumes of the HopsFS DataNodes, MinIO, OpenSearch, Kafka, Consul and the remote shuffle service, for good, instead of keeping them (also in [5.0.2][hopsworks-5-0-2]).
  To keep them, set `global._hopsworks.wipeDataOnUninstall: false` or label the PVCs `hopsworks.ai/keep=true` before you uninstall; the Superset MySQL volume is deleted regardless.
- [HELM] Every `helm upgrade`, including values-only ones, now rebuilds the feature store search index afterwards, which the 5.0 chart never did, signing in with `hopsworks.variables.admin_email` and `hopsworks.variables.admin_password`, and fails the upgrade if they don't sign in to the Hopsworks admin account.
  Set them to the admin account's credentials before you upgrade; if password login is disabled, upgrade to [5.1.1][hopsworks-5-1-1] instead.
- [HELM] The consul-k8s chart fails to render with `disable_hostname` in `consul.consul.server.extraConfig`, where the 5.0 chart set it; remove it, because `consul.consul.global.metrics.disableAgentHostName` (default `true`) replaces it.
  With `--reuse-values`, which keeps the 5.0 default `extraConfig`, use `--reset-then-reuse-values`.
- [HELM] Removed `hopsworks.variables.jupyter_spark_driver_memory_overhead_factor`, added in 5.0.10; the driver memory overhead of a notebook now comes from its Spark configuration (also in [5.0.12][hopsworks-5-0-12]).
  Remove it from your values before you upgrade, because the values schema rejects it; with `--reuse-values`, which keeps the old default, use `--reset-then-reuse-values`.
- [HELM] Removed `hopsworks.variables.hive_default_quota` and `hopsworks.variables.enable_conda_install`; remove them from your values, because the values schema rejects them.
  With `--reuse-values`, which keeps the 5.0 defaults of both, use `--reset-then-reuse-values`.
- [HELM] `vpa.image.tag` is now the version of the VPA installer image (default `"1.7.1-2"`), separate from `vpa.imagesTag`; remove any override of it, including the `"1.7.1"` that [5.0.8][hopsworks-5-0-8] asked for, and upgrade with `--reset-then-reuse-values` instead of `--reuse-values`, which keeps the old value.
- [HELM] The Airflow migration Job now waits for the DDL MySQL server, instead of any MySQL server, so the upgrade hangs with `rondb.rondb.meta.ddlMySQLd.enabled: false` (also in [5.0.13][hopsworks-5-0-13]).
  Keep it enabled if you use Airflow.
- [HELM] Init containers now set CPU and memory requests and limits, which most of them used to leave unset, so a namespace `LimitRange` default is no longer charged to the pod for its whole life; the RonDB and Consul charts are not covered yet (also in [5.0.9][hopsworks-5-0-9]).
  If a namespace `LimitRange` has a `min` or `max` they don't fit, set `global._hopsworks.initContainerResources` before you upgrade, or Kubernetes rejects the pods.
- [HELM] The chart fails to render with `hopsworks.hopsfsMount.enabled: false`, because the new Trino mountable-secrets sidecar needs the HopsFS mount.
  Set `global._hopsworks.trino.mountableSecrets.enabled: false`, and override `trino.trino.initContainers` and `trino.trinotest.initContainers.coordinator` without the `mountable-secrets` container, as `values.openshift.yaml` does.
- [HELM] Removed the Kafka quota defaults Job, which applied `kafka.cluster.kafka.quotas.defaults` to each client, so it is ignored with `type: strimzi`, and fails the render with `type: kafka` when `enabled` is `true` (also in [5.0.13][hopsworks-5-0-13]).
  If you set it, move your limits to `kafka.cluster.kafka.quotas.strimzi` or `kafka.cluster.kafka.quotas.kafka`, with new numbers: the `strimzi` rates are a total per broker, shared by all clients.
- [HELM] `quotas` on a user in `kafka.users` now fail the render under the default `strimzi` plugin, which never enforced them (also in [5.0.13][hopsworks-5-0-13]).
  Remove them, or set `kafka.cluster.kafka.quotas.type: kafka`, `kafka.cluster.kafka.quotas.minAvailableRatioPerVolume: 0` and `kafka.cluster.kafka.authorizer.principalBuilderClass: ""` to enforce them.
- [HELM] The Hopsworks admin container now has a liveness probe (`hopsworks.probs.admin.livenessProbe`) that restarts it after about 10 minutes without a response and a startup probe (`hopsworks.probs.admin.startupProbe`) that gives it up to 30 minutes to start, instead of no probes, so a probe you set with `httpGet` or `tcpSocket` also needs `exec: null`, or Kubernetes rejects the pod (also in [5.0.3][hopsworks-5-0-3]).
  This needs Helm 4 or Helm 3.17.1 or later, because older Helm 3 releases ignore a `null` for a subchart value.
- [HELM] `catalog-volume` moved from `trino.trino.configMounts` to the `additionalVolumes` and `additionalVolumeMounts` of `trino.trino.coordinator` and `trino.trino.worker`.
  If you override these lists, copy both entries from the chart's values and remove `catalog-volume` from an overridden `trino.trino.configMounts`, or the Trino pods don't start.
- [HELM] Grafana now refuses to start on an image that doesn't carry the Hopsworks dashboards, because they ship in its image instead of ConfigMaps; if you override `grafana.grafana.image`, use the image the chart ships or one built from it.
- [HELM] 5.1.0 came out before [5.0.14][hopsworks-5-0-14] and lacks most of its changes, such as the addressed vulnerabilities in jobs; if you run 5.0.14, upgrade to [5.1.2][hopsworks-5-1-2] or later instead.
- [HELM] 5.1.0 ships an older RonDB chart than [5.0.13][hopsworks-5-0-13], without `rondb.rondb.rdrs.probes`, so the RonDB REST server restarts again during a data node failure; if you run 5.0.13, upgrade to [5.1.1][hopsworks-5-1-1] or later instead.
- [HELM] Trino pods now run as the `hopsworks-trino` and `hopsworks-trino-test` ServiceAccounts instead of `default`; move anything you attached to `default` for Trino, such as a cloud identity annotation or an OpenShift SCC.
- [HELM] Prometheus is upgraded from 2.51 to 3.14; check custom alert rules and scrape configs against the [Prometheus 3 migration guide](https://prometheus.io/docs/prometheus/latest/migration/).
- [HELM] Grafana is upgraded from 10.2 to 12.4, which no longer loads AngularJS panel plugins, though it converts the old core graph, table and singlestat panels; check dashboards you mount through `grafana.grafana.dashboardsConfigMaps` against the [Grafana 12 breaking changes](https://grafana.com/docs/grafana/latest/whatsnew/whats-new-in-v12/whats-new-in-v12-0/#breaking-changes).
- [HELM] Knative request metrics are now `http_server_request_duration_seconds` instead of `revision_request_count` and `revision_request_latencies`, with new label names, and Spark metrics have new names; update custom Grafana dashboards and alert rules.
- [HELM] Filebeat now keeps only the Kubernetes labels listed under `olk.filebeat.kubernetesMetadata`, and the `serviceLabelKey` of each `olk.logstash.extendServicesPipeline` entry, on service logs, instead of every pod label (also in [5.0.12][hopsworks-5-0-12]).
  Add any other label you filter on to `olk.filebeat.kubernetesMetadata.extraPodLabels`, `extraNamespaceLabels` or `extraNodeLabels`; an overridden `olk.filebeat.logs_locations` keeps its own `add_kubernetes_metadata` processor and every label, so to get the fix set `addKubernetesMetadata: true` on each entry and drop that processor.
- [HELM] `hopsworks.variables.enable_read_only_git_repositories` now defaults to `'false'` instead of `'true'`, so users can commit and push from Git repositories in Hopsworks; to keep them read-only, set it to `'true'` before you upgrade.
- [HELM] Feature monitoring is now on by default, instead of off, and the upgrade writes `hopsworks.variables.enable_feature_monitoring` to the cluster, replacing a value set in the admin UI (also in [5.0.1][hopsworks-5-0-1]).
  To keep it off, set it to `'false'` before you upgrade.

### Deprecations

- [API] Deprecated `FeatureGroup.commit_delete_record` in the Python client for `remove_rows`, which also deletes the rows from the online store (also in [5.0.8][hopsworks-5-0-8]).
- [API] Deprecated `stddev` of `FeatureDescriptiveStatistics` and `FeatureTransformationStatistics` in the Python client, replaced by `std_dev` (also in [5.0.1][hopsworks-5-0-1]).
- [API] Deprecated the alert statuses `feature_monitor_shift_undetected` and `feature_monitor_shift_detected` in the Python client for `monitoring_shift_undetected` and `monitoring_shift_detected` (also in [5.0.1][hopsworks-5-0-1]).
- [HELM] Deprecated `kserve.istio.gateways.http10` for `kserve.istio.gateways.ingress.http10`; the old key, ignored in 5.0, works again.
- [HELM] Deprecated `kafka.cluster.kafka.quotas.defaults`, which is no longer honoured; see the breaking changes above (also in [5.0.13][hopsworks-5-0-13]).
- [HELM] Deprecated `hopsworks.envs.postInstall.DEPLOY_RETRIES`, which has no effect now that the admin sidecar retries until the deployment succeeds (also in [5.0.3][hopsworks-5-0-3]).
- [HELM] Deprecated `grafana.grafana.dashboardsConfigMaps`, which the chart leaves empty now that its dashboards ship in the Grafana image; a dashboard you mount through it also needs a provider in `global._hopsworks.grafana.extraDashboardProviders`.

### Upgrade steps

Follow [Before every upgrade][docs-upgrade-before] and [5.0.x to 5.1.x][docs-upgrade-50-to-51] in the upgrade guide, which the docs have from 5.2 on.

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

- [HELM] Changed `hopsworks.variables.docker_operations_buildkit_extra_args` to empty by default, dropping the S3 build cache arguments that failed without S3 credentials; set them again to keep an S3 build cache.
- [HELM] Changed the default `kserve.kserve.controller.deploymentMode` from `Serverless` to `Knative`, its KServe 0.19 name.
- [HELM] Added `rondb.rondb.timeoutsMinutes.ndbmtdStartupProbe` and `rondb.rondb.timeoutsMinutes.mysqldStartupProbe`, the startup probe timeouts of the RonDB data nodes and MySQL servers, and raised the MySQL server one from about 17 to 20 minutes (also in [5.0.5][hopsworks-5-0-5]).
- [HELM] Changed `rondb.rondb.timeoutsMinutes.ndbmtdStartupProbe` to 240 minutes, from 25 in 5.0.0 and 120 in 5.0.5, so data nodes that take over two hours to reload aren't restarted in a loop (also in [5.0.11][hopsworks-5-0-11]).
- [HELM] Changed the default `spark.rss.shuffleServer.bufferCapacityRatio` to `0.6` and `spark.rss.shuffleServer.resources.limits.cpu` to `2000m` (also in [5.0.12][hopsworks-5-0-12]).
- [HELM] Changed `hopsworks.variables.docker_operations_timeout_listing_minutes`, `docker_operations_timeout_check_minutes` and `docker_operations_timeout_export_minutes` from 5 to 15 minutes, and `max_concurrent_base_sync_ops` from 6 to 5, so large base images finish syncing (also in [5.0.9][hopsworks-5-0-9]).
- [HELM] Changed the default Trino access rules, `trino.trino.accessControl.rules`, to let every user read the `system.metadata` tables; if you override the rules, add the same grant (also in [5.0.8][hopsworks-5-0-8]).
- [HELM] Changed the Superset init image to its own `superset/dockerize` repository, also in `values.airgap.yaml`; if you override `superset.superset.initImage.repository`, point it at a mirror of that image (also in [5.0.14][hopsworks-5-0-14]).
- [HELM] Changed the Prometheus adapter image repository to `prometheus/prometheus-adapter`, also in `values.airgap.yaml`; if you mirror images or override `prometheus.prometheus-adapter.image.repository`, mirror the new image.
- [HELM] Changed the KubeRay operator image repository to `hopsworks/kuberay-operator`, also in `values.airgap.yaml`; if you mirror images or override `ray.kuberay-operator.image.repository`, mirror the new image.
- [HELM] Changed the KServe controller image repository, `kserve.kserve.controller.image`, to `kserve/kserve-controller` instead of `hopsworks/kserve-controller`; if you mirror images or override it, mirror the new image.
- [HELM] Changed `values.openshift.yaml` to turn off the Trino mountable-secrets sidecar (`global._hopsworks.trino.mountableSecrets.enabled: false`), which needs the privileged SCC, and to run Trino and its test coordinator under the UID the SCC assigns.
- [HELM] Fixed users added to `rondb.rondb.mysql.users` after the install never being created, and users with privileges on a single database or table failing; every upgrade now creates the listed users (also in [5.0.11][hopsworks-5-0-11]).
- [HELM] Fixed the values schema rejecting a cron string in `hopsworks.velero.backup.schedule`.
- [HELM] Fixed the chart failing to render with `hopsworks.dropDatabase: true` (also in [5.0.9][hopsworks-5-0-9]).
- [HELM] Added `spark.spark-operator.hook.upgradeCrd` (default `true`), a pre-install and pre-upgrade Job that updates the Spark operator CRDs from the `hopsworks/spark-operator-crds:2.5.1-h1-1.9` image, also in `values.airgap.yaml`; if you mirror images, mirror that tag.
- [HELM] Added `spark.sql.ansiEnabled` (default `false`), so SQL keeps returning null on overflow and invalid casts on Spark 4.1, as on Spark 3.5.
- [HELM] Added `hopsworks.dockerImage.pypi.pythonDownloads` (default `never`), so uv never downloads a Python interpreter during environment builds.
- [HELM] Added `rondb.rondb.mysql.exporter.maxOpenConnections` (default `1`), the connections of the RonDB MySQL metrics exporter; the render fails if it exceeds `rondb.rondb.mysql.exporter.maxUserConnections` (also in [5.0.1][hopsworks-5-0-1]).
- [HELM] Added `kafka.cluster.clusterCa.validityDays` and `kafka.cluster.clientsCa.validityDays` (default `365`) for the certificates Strimzi issues, applied at the next issuance (also in [5.0.10][hopsworks-5-0-10]).
- [HELM] Added `kafka.cluster.kafka.quotas.type` to choose the Kafka quota plugin: `strimzi` (the default), set under `kafka.cluster.kafka.quotas.strimzi`, or `kafka`, which enforces per-user quotas from `kafka.users[].quotas` and defaults from `kafka.cluster.kafka.quotas.kafka` (also in [5.0.13][hopsworks-5-0-13]).
  `kafka` also needs `kafka.cluster.kafka.quotas.minAvailableRatioPerVolume: 0`, per-user quotas need `kafka.cluster.kafka.authorizer.principalBuilderClass: ""`, which changes how ACLs and `superUsers` match principals, and none of these settings take effect on clusters first installed on Hopsworks 4.3 or 4.5.
- [HELM] Added `airflow.dependencies.mysql.ddlConsulServiceName` (default `mysqlddl`), the DDL MySQL server the Airflow migration Job connects to (also in [5.0.13][hopsworks-5-0-13]).
- [HELM] Added `global._hopsworks.wipeDataOnUninstall` (default `true`) to delete the data volumes on `helm uninstall` (also in [5.0.2][hopsworks-5-0-2]).
- [HELM] Added `cleanupOnUninstall.enabled` to each component chart, such as `hopsworks.cleanupOnUninstall.enabled`, and `certs-operator.gracefulCertTeardown.enabled`, to turn off the uninstall cleanup of that component (also in [5.0.2][hopsworks-5-0-2]).
- [HELM] Added `hopsworks.jupyter.notebookConfig.enableUploads`; set it to `false` to block file uploads from the Jupyter UI and base64 uploads through the Jupyter Contents API (also in [5.0.8][hopsworks-5-0-8]).
- [HELM] Added `global._hopsworks.initContainerResources` (`waiter`, `tool`, `runtime`) to size the requests and limits that init containers now set (also in [5.0.9][hopsworks-5-0-9]).
- [HELM] Added `olk.filebeat.kubernetesMetadata`, the pod, namespace and node labels Filebeat keeps on service logs (`extraPodLabels`, `extraNamespaceLabels`, `extraNodeLabels` for your own), and `addKubernetesMetadata` on each `olk.filebeat.logs_locations` entry (also in [5.0.12][hopsworks-5-0-12]).
- [HELM] Added `hopsworks.velero.backup.storageLocation.s3ForcePathStyle` for S3-compatible backup stores that need path-style addressing (also in [5.0.1][hopsworks-5-0-1]).
- [HELM] Added `hopsfs.objectStorage.s3.disableCertChecking` and `hopsfs.objectStorage.s3.disableChecksumValidation` to turn off TLS certificate checks and client-side checksum validation for the HopsFS S3 endpoint (also in [5.0.3][hopsworks-5-0-3]).
- [HELM] Added `hopsworks.variables.docker_operations_lock_dependencies`, `docker_operations_allow_hermetic_custom_commands` and `docker_operations_multi_region_copy`, off by default, for hash-locked build dependencies, cached hermetic custom commands and image copies to the second region.
- [HELM] Added cluster variables for the default CPU, memory and GPU of new jobs and Python apps, such as `hopsworks.variables.spark_job_executor_memory`.
- [HELM] Added `hopsworks.variables.pushgateway_group_ttl_minutes`, `pushgateway_monitor_interval_ms` and `pushgateway_cleaner_batch_size` to clean stale Pushgateway metric groups.
- [HELM] Added `kserve.knative.imageRegistry` for the Knative images.
- [HELM] Added `olk.opensearch.audit.enabled` (default `false`) and `olk.opensearch.audit.retentionDays` for OpenSearch security audit logs.
- [HELM] Added `global._hopsworks.trino.egressProbe.echoUrl` to show which IP addresses an external database must allow.
- [HELM] Added `global._hopsworks.trino.userCatalogShards` (default `2`), the number of Secrets that hold user-created Trino catalogs, each capped near 1 MiB; to raise it, also add a `hopsworks-trino-catalogs-user-<N>` source for each new shard to the `catalog-volume` of `trino.trino.coordinator` and `trino.trino.worker`, or the render fails.
- [HELM] Added `olk.opensearch.security.default_tenant` (default `Private`), the tenant OpenSearch Dashboards opens in.
- [HELM] Added `kserve.kserve.servingruntime.vllmopenai.imageRegistry` and `kserve.kserve.servingruntime.vllmomni.imageRegistry` to pull the vLLM images from a mirror (also in [5.0.1][hopsworks-5-0-1]).
- [HELM] Added `rondb.rondb.rondbConfig.UseTcInRRGroup` and `rondb.rondb.rondbConfig.MaxRRGroupSize` to tune the RonDB round-robin groups (also in [5.0.1][hopsworks-5-0-1]).
- [HELM] Added `hopsworks.envs.postInstall.DEPLOY_RETRY_INTERVAL_SEC`, `ASADMIN_TIMEOUT_SEC` and `ASADMIN_DEPLOY_TIMEOUT_SEC` to tune how the admin sidecar retries the Hopsworks deployment (also in [5.0.3][hopsworks-5-0-3]).
- [HELM] Added `hopsworks.service.worker.external.https.nodePort` to pin the node port of the Hopsworks HTTPS service when its `type` is `NodePort` (also in [5.0.4][hopsworks-5-0-4]).
- [HELM] Added `docker-registry.affinity`, `minio.affinity` and `hopsworks.dockerRegistry.preset.affinity` for the Docker registry, MinIO and the preset image push Job (also in [5.0.6][hopsworks-5-0-6]).
- [HELM] Added `rondb.rondb.mysql.users[].existingSecret` to read the password of a MySQL user from your own Secret (also in [5.0.11][hopsworks-5-0-11]).
- [HELM] Added `onlinefs.deployment.strategy` to set the rollout strategy of OnlineFS (also in [5.0.13][hopsworks-5-0-13]).

[docs-sql-runner]: https://docs.hopsworks.ai/5.1/user_guides/projects/trino/query_engine/#sql-runner
[docs-trino-history]: https://docs.hopsworks.ai/5.1/setup_installation/admin/trino/#query-history
[docs-os-security]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade_opensearch/#opensearch-security-configuration
[docs-os-copy-51]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade_opensearch/#opensearch-copy-on-51
[docs-upgrade-trino-history]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade/#upgrade-trino-query-history
[values-olk-index-upgrade]: https://docs.hopsworks.ai/5.1/setup_installation/common/helm_chart_values/olk/#helm.olk.opensearch.indexUpgrade.mode
[docs-upgrade-before]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade/#upgrade-before-every-upgrade
[docs-upgrade-50-to-51]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade/#upgrade-50-to-51
[docs-agent-deployments-git]: https://docs.hopsworks.ai/5.1/user_guides/agents/deployments/#deploy-from-a-git-repository
[docs-apps-auto-redeploy]: https://docs.hopsworks.ai/5.1/user_guides/projects/apps/#auto-redeploy-on-new-commits
[docs-snowflake]: https://docs.hopsworks.ai/5.1/user_guides/fs/data_source/creation/snowflake/
[docs-feature-monitoring]: https://docs.hopsworks.ai/5.1/user_guides/fs/feature_group/feature_monitoring/
