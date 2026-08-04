# Cluster Configuration Variables Reference

This page lists every cluster configuration key declared in the Hopsworks server source code, with its type and default value.
Descriptions are not included here.
The source declarations carry no description field, so adding one would mean inventing text that was never reviewed against the actual behaviour of the setting.
Adding descriptions is a planned enhancement, pending a source-side change that adds a description argument to the settings declarations.

Some defaults below are computed Java expressions rather than literal values, for example a reference to a constant defined in another class.
Those rows show the raw expression and are marked as computed rather than showing a guessed value.
A small number of keys are declared independently in more than one source file with their own default value.
Those are shown as separate rows and marked as duplicates rather than merged into one, since the two declarations can drift apart.

See [Cluster Configuration][cluster-configuration] for how to view and change these variables from the Hopsworks UI.

<!-- BEGIN GENERATED -->

| Key | Type | Default | Source module |
| --- | --- | --- | --- |
| `action_attempt_limit` | Integer | `3` | Settings.java |
| `admin_email` | String | `admin@hopsworks.ai` | Settings.java |
| `agent_base_image_name` | String | `agent-job` | Settings.java |
| `agent_default_max_turns` | Integer | `50` | Settings.java |
| `agent_default_model` | String | `claude-sonnet-4-5` | Settings.java |
| `agent_deployment_otel_cpu` | Double | `0.5` | Settings.java |
| `agent_deployment_otel_enabled` | Boolean | `true` | Settings.java |
| `agent_deployment_otel_image` | String | `docker.hops.works/hops-otel:5.0.0-SNAPSHOT` | Settings.java |
| `agent_deployment_otel_input_token_price_per_million` | Double | `0.0` | Settings.java |
| `agent_deployment_otel_memory_mb` | Integer | `1024` | Settings.java |
| `agent_deployment_otel_output_token_price_per_million` | Double | `0.0` | Settings.java |
| `agent_deployment_otel_ttl_seconds` | Integer | `86400` | Settings.java |
| `agent_image` | String | `agent-job` | Settings.java |
| `agent_jobs_enabled` | Boolean | `true` | Settings.java |
| `airflow_enabled` | Boolean | `true` | Settings.java |
| `airflow_user` | String | `airflow` | Settings.java |
| `alert_manager_config_map` | String | `hopsworks-release-alertmanager` | KubeSettings.java |
| `anaconda_enabled` | Boolean | `true` | Settings.java |
| `app_kill_grace_period_seconds` | Long | `2` | Settings.java |
| `application_certificate_validity_period` | String | `3d` | CAConf.java |
| `arrow_libhdfs_dir` | String | `/usr/local/bin/libhdfs-golang` | Settings.java |
| `async_services_timer_batch_size` | Integer | `1000` | Settings.java |
| `async_services_timer_delete_history_after_days` | Long | `7` | Settings.java |
| `async_services_timer_enabled` | Boolean | `true` | Settings.java |
| `async_services_timer_interval_ms` | Long | `15000` | Settings.java |
| `audit_log_count` | Integer | `10` | VariablesHelper.java |
| `audit_log_date_format` | String | `yyyy-MM-dd HH:mm:ss` | VariablesHelper.java |
| `audit_log_file_format` | String | `server_audit_log%g.log` | VariablesHelper.java |
| `audit_log_file_path` | String | `/audit-logs` | VariablesHelper.java |
| `audit_log_file_type` | String | `SimpleFormatter.class.getName()` *(computed expression, not a literal)* | VariablesHelper.java |
| `audit_log_size_limit` | Integer | `256000000` | VariablesHelper.java |
| `base_image_name` | String | `hopsworks-base` | Settings.java |
| `base_image_version` | String | `4.3.0` | Settings.java |
| `cert_mater_delay` | String | `1m` | Settings.java |
| `certs_dir` | String | `/srv/hops/certs-dir` *(duplicate key, also declared in Settings.java; values match)* | CAConf.java |
| `certs_dir` | String | `/srv/hops/certs-dir` *(duplicate key, also declared in CAConf.java; values match)* | Settings.java |
| `client_path` | String | `/srv/hops/client.tar.gz` | Settings.java |
| `cloud` | String | *(empty string)* | Settings.java |
| `cloud_events_endpoint` | String | *(empty string)* *(duplicate key, also declared in Settings.java; values match)* | CAConf.java |
| `cloud_events_endpoint` | String | *(empty string)* *(duplicate key, also declared in CAConf.java; values match)* | Settings.java |
| `cloud_events_endpoint_api_key` | String | *(empty string)* | Settings.java |
| `command_search_fs_history_clean_period_as_ms` | Long | `60000` | Settings.java |
| `command_search_fs_history_enable` | Boolean | `false` | Settings.java |
| `command_search_fs_history_window_as_s` | Long | `3600` | Settings.java |
| `command_search_fs_process_timer_period_as_ms` | Long | `1000` | Settings.java |
| `command_search_fs_retry_per_clean_interval` | Integer | `5` | Settings.java |
| `conda_default_repo` | String | `defaults` | Settings.java |
| `conda_env_name` | String | `hopsworks_environment` | Settings.java |
| `created_by_label_name` | String | `hw-created-by` | KubeSettings.java |
| `created_by_label_value` | String | `hopsworks` | KubeSettings.java |
| `databricks_account_host_allowlist` | String | `accounts.cloud.databricks.com,accounts.azuredatabricks.net,accounts.gcp.databricks.com` | Settings.java |
| `databricks_oauth_allow_private_ranges` | Boolean | `false` | Settings.java |
| `default_feature_store_project_id` | Integer | `-1` | Settings.java |
| `default_featurestore_project_name` | String | `hopsworks_default` | Settings.java |
| `default_jupyter_environment` | String | `pandas-training-pipeline` | Settings.java |
| `default_python_job_environment` | String | `pandas-training-pipeline` | Settings.java |
| `disable_password_login` | Boolean | `false` | Settings.java |
| `disable_registration` | Boolean | `false` | Settings.java |
| `disable_registration_ui` | Boolean | `false` | Settings.java |
| `dlthub-warehouse` | String | `dlthub-warehouse` | Settings.java |
| `dlthub_image_name` | String | `docker.hops.works/hopsworks/dlt` | Settings.java |
| `docker_base_image_dlthub` | String | `dlthub-ingestion-pipeline` | Settings.java |
| `docker_base_image_minimal_inference` | String | `minimal-inference-pipeline` | Settings.java |
| `docker_base_image_pandas_inference` | String | `pandas-inference-pipeline` | Settings.java |
| `docker_base_image_pandas_training` | String | `pandas-training-pipeline` | Settings.java |
| `docker_base_image_python` | String | `python-feature-pipeline` | Settings.java |
| `docker_base_image_python_app` | String | `python-app-pipeline` | Settings.java |
| `docker_base_image_python_version` | String | `3.12` | Settings.java |
| `docker_base_image_ray_tensorflow_training` | String | `ray-tensorflow-training-pipeline` | Settings.java |
| `docker_base_image_ray_torch_training` | String | `ray-torch-training-pipeline` | Settings.java |
| `docker_base_image_ray_training` | String | `ray-training-pipeline` | Settings.java |
| `docker_base_image_spark` | String | `spark-feature-pipeline` | Settings.java |
| `docker_base_image_tensorflow_inference` | String | `tensorflow-inference-pipeline` | Settings.java |
| `docker_base_image_tensorflow_training` | String | `tensorflow-training-pipeline` | Settings.java |
| `docker_base_image_torch_inference` | String | `torch-inference-pipeline` | Settings.java |
| `docker_base_image_torch_training` | String | `torch-training-pipeline` | Settings.java |
| `docker_base_image_vllm_inference` | String | `vllm-inference-pipeline` | Settings.java |
| `docker_cgroup_cpu_period` | String | `100000` | Settings.java |
| `docker_cgroup_enabled` | Boolean | `false` | Settings.java |
| `docker_cgroup_parent` | String | `docker.slice` | Settings.java |
| `docker_job_mount_allowed` | Boolean | `true` | Settings.java |
| `docker_job_mounts_list` | String | *(empty string)* | Settings.java |
| `docker_job_uid_strict` | Boolean | `true` | Settings.java |
| `docker_mounts` | String | `/srv/hops/hadoop/etc/hadoop,/srv/hops/spark,/srv/hops/flink` | Settings.java |
| `docker_namespace` | String | *(empty string)* | Settings.java |
| `docker_operations_backoff_limit` | Integer | `0` | Settings.java |
| `docker_operations_buildkit_backoff_limit` | Integer | `0` | Settings.java |
| `docker_operations_buildkit_extra_args` | String | *(empty string)* | Settings.java |
| `docker_operations_buildkit_image_root` | String | `docker.hops.works/hopsworks/moby/buildkit:v0.14.1` | Settings.java |
| `docker_operations_buildkit_limit_cpu` | Integer | `1` | Settings.java |
| `docker_operations_buildkit_limit_memory` | String | `2Gi` | Settings.java |
| `docker_operations_buildkit_priority_class` | String | `ndb-high-priority` | Settings.java |
| `docker_operations_buildkit_request_cpu` | Integer | `1` | Settings.java |
| `docker_operations_buildkit_request_memory` | String | `2Gi` | Settings.java |
| `docker_operations_buildkit_storage` | String | `2Gi` | Settings.java |
| `docker_operations_cert_name` | String | `kagent_certificate_bundle.pem` | Settings.java |
| `docker_operations_crane_extra_args` | String | *(empty string)* | Settings.java |
| `docker_operations_crane_image` | String | `docker.hops.works/hopsworks/hwutils:0.3` | Settings.java |
| `docker_operations_delete_jobs_add_description_if_fails` | Boolean | `false` | Settings.java |
| `docker_operations_delete_jobs_on_completion` | Boolean | `false` | Settings.java |
| `docker_operations_docker_context_builder` | String | `Auto` | Settings.java |
| `docker_operations_docker_context_builder_s3_bucket` | String | `hopsworks` | Settings.java |
| `docker_operations_docker_context_builder_s3_endpoint` | String | `http://minio.hopsworks.svc.cluster.local:9000` | Settings.java |
| `docker_operations_docker_context_builder_s3_region` | String | `eu-west-1` | Settings.java |
| `docker_operations_docker_context_builder_s3_retention_minutes` | Integer | `-1` | Settings.java |
| `docker_operations_hopsworks_ca_secret_name` | String | `docker-registry-crypto-material` | Settings.java |
| `docker_operations_image_builder_image` | String | `docker.hops.works/hopsworks/image-builder:0.1` | Settings.java |
| `docker_operations_image_pull_secrets` | String | *(empty string)* | Settings.java |
| `docker_operations_managed_docker_secrets` | String | *(empty string)* | Settings.java |
| `docker_operations_oci_worker_snapshotter` | String | `auto` | Settings.java |
| `docker_operations_push_insecure` | Boolean | `false` | Settings.java |
| `docker_operations_registry_container` | String | `docker` | Settings.java |
| `docker_operations_registry_http` | Boolean | `false` | Settings.java |
| `docker_operations_registry_pod` | String | `docker-registry-0` | Settings.java |
| `docker_operations_sidecar_image` | String | `docker.hops.works/hopsworks/hwutils:0.3` | Settings.java |
| `docker_operations_suspend_jobs` | Boolean | `false` | Settings.java |
| `docker_operations_timeout_check_minutes` | Integer | `5` | Settings.java |
| `docker_operations_timeout_delete_minutes` | Integer | `10` | Settings.java |
| `docker_operations_timeout_export_minutes` | Integer | `5` | Settings.java |
| `docker_operations_timeout_listing_minutes` | Integer | `10` | Settings.java |
| `docker_operations_timeout_minutes_buildkit` | Integer | `30` | Settings.java |
| `docker_operations_timeout_tag_minutes` | Integer | `5` | Settings.java |
| `download_allowed` | Boolean | `true` | Settings.java |
| `elastic_admin_password` | String | *(empty string)* | Settings.java |
| `elastic_admin_user` | String | *(empty string)* | Settings.java |
| `elastic_https_enabled` | Boolean | *(empty string)* | Settings.java |
| `elastic_jwt_enabled` | Boolean | *(empty string)* | Settings.java |
| `elastic_jwt_exp_ms` | Long | *(empty string)* | Settings.java |
| `elastic_jwt_url_parameter` | String | *(empty string)* | Settings.java |
| `elastic_logs_index_expiration` | Long | `604800000` | Settings.java |
| `elastic_max_page_size` | Integer | `10000` | Settings.java |
| `elastic_opendistro_security_enabled` | Boolean | *(empty string)* | Settings.java |
| `elastic_scroll_page_size` | Integer | `1000` | Settings.java |
| `elastic_version` | String | *(empty string)* | Settings.java |
| `enable_adls_storage_connectors` | Boolean | `false` | Settings.java |
| `enable_bigquery_storage_connectors` | Boolean | `false` | Settings.java |
| `enable_bring_your_own_kafka` | Boolean | `false` | Settings.java |
| `enable_conda_install` | Boolean | `true` | Settings.java |
| `enable_crm_storage_connectors` | Boolean | `true` | Settings.java |
| `enable_custom_branding` | Boolean | `false` | Settings.java |
| `enable_data_science_profile` | Boolean | `false` | Settings.java |
| `enable_feature_monitoring` | Boolean | `false` | Settings.java |
| `enable_gcs_storage_connectors` | Boolean | `false` | Settings.java |
| `enable_hopsfsmount_page_cache_in_jobs` | Boolean | `true` | Settings.java |
| `enable_hopsfsmount_page_cache_in_jupyter` | Boolean | `false` | Settings.java |
| `enable_kafka_storage_connectors` | Boolean | `true` | Settings.java |
| `enable_mongodb_storage_connectors` | Boolean | `true` | Settings.java |
| `enable_opensearch_storage_connectors` | Boolean | `false` | Settings.java |
| `enable_project_observer_role` | Boolean | `false` | Settings.java |
| `enable_read_only_git_repositories` | Boolean | `false` | Settings.java |
| `enable_redshift_storage_connectors` | Boolean | `true` | Settings.java |
| `enable_rest_storage_connectors` | Boolean | `true` | Settings.java |
| `enable_sap_hana_storage_connectors` | Boolean | `true` | Settings.java |
| `enable_snowflake_storage_connectors` | Boolean | `true` | Settings.java |
| `enable_sql_storage_connectors` | Boolean | `true` | Settings.java |
| `enable_terminal` | Boolean | `false` | Settings.java |
| `enable_unity_catalog_storage_connectors` | Boolean | `true` | Settings.java |
| `enable_user_search` | Boolean | `true` | Settings.java |
| `executions_cleaner_batch_size` | Integer | `1000` | Settings.java |
| `executions_cleaner_interval_ms` | Integer | `600000` | Settings.java |
| `executions_per_job_limit` | Integer | `10000` | Settings.java |
| `executions_ttl_days` | Integer | `90` | Settings.java |
| `feature_monitoring_max_num_features` | Integer | `15` | Settings.java |
| `featurestore_db_admin_pass` | String | *(empty string)* | Settings.java |
| `featurestore_db_admin_user` | String | *(empty string)* | Settings.java |
| `featurestore_default_quota` | Long | `String.valueOf(HdfsConstants.QUOTA_DONT_SET)` *(computed expression, not a literal)* | Settings.java |
| `featurestore_default_storage_format` | String | `ORC` | Settings.java |
| `featurestore_jdbc_url` | String | `jdbc:mysql://onlinefs.mysql.service.consul:3306/` | Settings.java |
| `featurestore_metrics_enabled` | Boolean | `true` | Settings.java |
| `featurestore_metrics_max_concurrent_event_processors` | Integer | `5` | Settings.java |
| `featurestore_metrics_online_ingestion_enabled` | Boolean | `false` | Settings.java |
| `featurestore_online_enabled` | Boolean | `false` | Settings.java |
| `featurestore_online_tablespace` | String | *(empty string)* | Settings.java |
| `fg_preview_limit` | Integer | `100` | Settings.java |
| `file_preview_image_size` | Integer | `10000000` | Settings.java |
| `file_preview_txt_size` | Integer | `100` | Settings.java |
| `first_time_login` | String | `0` | Settings.java |
| `flink_dir` | String | `/srv/hops/flink` | Settings.java |
| `flink_version` | String | *(empty string)* | Settings.java |
| `fs_java_job_util` | String | `hdfs:///user/spark/hsfs-utils-2.1.0-SNAPSHOT.jar` | Settings.java |
| `fs_py_job_util` | String | `hdfs:///user/spark/hsfs_util-2.1.0-SNAPSHOT.py` | Settings.java |
| `fs_storage_connector_session_duration` | Integer | `3600` | Settings.java |
| `git_command_timeout_minutes` | Integer | `60` | Settings.java |
| `git_image` | String | `docker.hops.works/hopsworks/git:0.7.0` | Settings.java |
| `grafana_version` | String | *(empty string)* | Settings.java |
| `hadoop_configmap_name` | String | `hopsfs-config` | Settings.java |
| `hadoop_dir` | String | `/srv/hops/hadoop` | Settings.java |
| `hadoop_version` | String | `2.8.2` | Settings.java |
| `hdfs_default_quota` | Long | `Long.toString(HdfsConstants.QUOTA_DONT_SET)` *(computed expression, not a literal)* | Settings.java |
| `hdfs_file_op_job_driver_mem` | Integer | `2048` | Settings.java |
| `hdfs_file_op_job_util` | String | `hdfs:///user/spark/hdfs_file_operations-0.2.0.py` | Settings.java |
| `hdfs_log_storage_policy` | String | `DistributedFileSystemOps.StoragePolicy.DEFAULT.toString()` *(computed expression, not a literal)* | Settings.java |
| `hdfs_user` | String | `hdfs` | Settings.java |
| `hdfscontentsmanager_base_hopsfs_client` | String | `libhdfs-go` | Settings.java |
| `hive2_version` | String | *(empty string)* | Settings.java |
| `hive_conf_path` | String | `/srv/hops/apache-hive/conf/hive-site.xml` | Settings.java |
| `hive_superuser` | String | `hive` | Settings.java |
| `hive_warehouse` | String | `/apps/hive/warehouse` | Settings.java |
| `hops_helm_install_namespace` | String | `hopsworks` *(duplicate key, also declared in Settings.java; values match)* | KubeSettings.java |
| `hops_helm_install_namespace` | String | `hopsworks` *(duplicate key, also declared in KubeSettings.java; values match)* | Settings.java |
| `hops_rpc_tls` | Boolean | `false` | Settings.java |
| `hopsfs_mount_mount_path` | String | `/hopsfs` | Settings.java |
| `hopsfsmount_log_level` | String | `warn` | Settings.java |
| `hopsfsmount_nn_connections` | Integer | `4` | Settings.java |
| `hopsfsmount_virtual_directories` | String | *(empty string)* | Settings.java |
| `hopsworks_dir` | String | `/srv/hops/domains` *(duplicate key, also declared in Settings.java; values diverge)* | CAConf.java |
| `hopsworks_dir` | String | `/srv/hops/domains/domain1` *(duplicate key, also declared in CAConf.java; values diverge)* | Settings.java |
| `hopsworks_engine` | String | `python` | Settings.java |
| `hopsworks_enterprise` | Boolean | `false` | Settings.java |
| `hopsworks_master_password` | String | `adminpw` *(duplicate key, also declared in Settings.java; values match)* | CAConf.java |
| `hopsworks_master_password` | String | `adminpw` *(duplicate key, also declared in CAConf.java; values match)* | Settings.java |
| `hopsworks_public_host` | String | *(empty string)* | Settings.java |
| `hopsworks_public_proxy_url` | String | *(empty string)* | Settings.java |
| `hopsworks_rest_log_level` | String | `PROD` *(duplicate key, also declared in Settings.java; values diverge)* | CAConf.java |
| `hopsworks_rest_log_level` | String | `String.valueOf(RESTLogLevel.PROD.name())` *(computed expression, not a literal)* *(duplicate key, also declared in CAConf.java; values diverge)* | Settings.java |
| `hopsworks_secret` | String | `hopsworks-secrets` | KubeSettings.java |
| `hopsworks_user` | String | `glassfish` | Settings.java |
| `hopsworks_version` | String | *(empty string)* | Settings.java |
| `hw_group_mapping_sync_enabled` | Boolean | `false` | Settings.java |
| `ingestion_job_cores` | Double | `1.0` | Settings.java |
| `ingestion_job_gpus` | Integer | `0` | Settings.java |
| `ingestion_job_memory` | Integer | `2048` | Settings.java |
| `int_service_api_key` | String | *(empty string)* | Settings.java |
| `job_name_validation_regex` | String | `^[a-zA-Z0-9_\\-]+$` | Settings.java |
| `jupyter_allow_no_limit_shutdown` | Boolean | `true` | Settings.java |
| `jupyter_dir` | String | `/srv/hops/jupyter` | Settings.java |
| `jupyter_group` | String | `jupyter` | Settings.java |
| `jupyter_host` | String | `localhost` | Settings.java |
| `jupyter_hour_shutdown_options` | String | `8,24,72` | Settings.java |
| `jupyter_origin_scheme` | String | `https` | Settings.java |
| `jupyter_remote_fs_driver` | String | `hdfscontentsmanager` | Settings.java |
| `jupyter_shell_command` | String | `/bin/bash` | Settings.java |
| `jupyter_shutdown_timer_interval` | String | `30m` | Settings.java |
| `jupyter_ws_ping_interval` | String | `10000` | Settings.java |
| `jwt_exp_leeway_sec` | Long | `900` | Settings.java |
| `jwt_issuer` | String | `hopsworks@logicalclocks.com` *(duplicate key, also declared in Settings.java; values match)* | CAConf.java |
| `jwt_issuer` | String | `hopsworks@logicalclocks.com` *(duplicate key, also declared in CAConf.java; values match)* | Settings.java |
| `jwt_lifetime_ms` | Long | `1800000` | Settings.java |
| `jwt_signature_algorithm` | String | `HS512` | Settings.java |
| `jwt_signing_key_name` | String | `apiKey` | Settings.java |
| `kafka_enabled` | Boolean | `true` | Settings.java |
| `kafka_max_num_topics` | Integer | `10` | Settings.java |
| `kafka_num_partitions` | Integer | `2` | Settings.java |
| `kafka_num_replicas` | Integer | `1` | Settings.java |
| `kafka_version` | String | *(empty string)* | Settings.java |
| `keepalive_timeout` | Integer | `30` | Settings.java |
| `kerberos_auth` | Boolean | `false` | Settings.java |
| `kibana_https_enabled` | Boolean | `false` | Settings.java |
| `kibana_multi_tenancy_enabled` | Boolean | `false` | Settings.java |
| `kibana_service_log_viewer` | String | *(empty string)* | Settings.java |
| `kibana_version` | String | *(empty string)* | Settings.java |
| `kube_api_max_attempts` | Integer | `12` | Settings.java |
| `kube_ca_certfile` | String | `/srv/hops/certs-dir/certs/ca.cert.pem` | Settings.java |
| `kube_ca_password` | String | `adminpw` | CAConf.java |
| `kube_client_certfile` | String | `/srv/hops/certs-dir/kube/hopsworks/hopsworks.cert.pem` | Settings.java |
| `kube_client_keyfile` | String | `/srv/hops/certs-dir/kube/hopsworks/hopsworks.key.pem` | Settings.java |
| `kube_client_keypass` | String | `adminpw` | Settings.java |
| `kube_cluster_domain` | String | `.svc.cluster.local` | KubeSettings.java |
| `kube_hopsworks_default_service_account` | String | `hopsworks-default` | Settings.java |
| `kube_hopsworks_user` | String | `hopsworks` | Settings.java |
| `kube_image_builder_service_account` | String | `image-builder` | Settings.java |
| `kube_img_pull_policy` | String | `Always` | Settings.java |
| `kube_keystore_key` | String | `adminpw` | Settings.java |
| `kube_keystore_path` | String | `/srv/hops/certs-dir/kube/hopsworks/hopsworks__kstore.jks` | Settings.java |
| `kube_knative_lb_domain` | String | *(empty string)* | Settings.java |
| `kube_kserve_installed` | Boolean | `false` | Settings.java |
| `kube_kserve_tensorflow_version` | String | *(empty string)* | Settings.java |
| `kube_master_url` | String | `https://192.168.68.102:6443` | Settings.java |
| `kube_remove_job_when_completed` | Boolean | `true` | Settings.java |
| `kube_scheduling_hopsfsmount_cpu_limits` | Double | `-1.0` | Settings.java |
| `kube_scheduling_hopsfsmount_cpu_requests` | Double | `1.0` | Settings.java |
| `kube_scheduling_hopsfsmount_memory_limits_mb` | Double | `2024.0` | Settings.java |
| `kube_scheduling_jobinit_cpu_limits` | Double | `-1.0` | Settings.java |
| `kube_scheduling_jobinit_cpu_requests` | Double | `0.5` | Settings.java |
| `kube_scheduling_jobinit_memory_limits_mb` | Double | `512.0` | Settings.java |
| `kube_scheduling_jobinit_memory_requests_mb` | Double | `256.0` | Settings.java |
| `kube_serving_max_num_instances` | Integer | `-1` | Settings.java |
| `kube_serving_min_num_instances` | Integer | `-1` | Settings.java |
| `kube_serving_vllm_omni_versions` | String | *(empty string)* | Settings.java |
| `kube_serving_vllm_versions` | String | *(empty string)* | Settings.java |
| `kube_skip_namespace_creation` | Boolean | `false` | Settings.java |
| `kube_truststore_key` | String | `adminpw` | Settings.java |
| `kube_truststore_path` | String | `/srv/hops/certs-dir/kube/hopsworks/hopsworks__tstore.jks` | Settings.java |
| `kube_type` | String | `local` *(duplicate key, also declared in Settings.java; values match)* | CAConf.java |
| `kube_type` | String | `local` *(duplicate key, also declared in CAConf.java; values match)* | Settings.java |
| `kube_user_workload_tolerations` | String | *(empty string)* | Settings.java |
| `kubernetes_installed` | String | `false` *(duplicate key, also declared in Settings.java; values match)* | CAConf.java |
| `kubernetes_installed` | Boolean | `false` *(duplicate key, also declared in CAConf.java; values match)* | Settings.java |
| `kueue_installed` | Boolean | `false` | Settings.java |
| `kueue_project_default_cluster_queue` | String | *(empty string)* | Settings.java |
| `kueue_project_default_local_queue` | String | *(empty string)* | Settings.java |
| `kueue_system_jobs_cluster_queue` | String | *(empty string)* | Settings.java |
| `kueue_system_jobs_local_queue` | String | *(empty string)* | Settings.java |
| `ldap_account_status` | Integer | `1` | Settings.java |
| `ldap_attr_binary` | String | `java.naming.ldap.attributes.binary` | Settings.java |
| `ldap_auth` | Boolean | `false` | Settings.java |
| `ldap_dyn_group_target` | String | `memberOf` | Settings.java |
| `ldap_group_dn` | String | *(empty string)* | Settings.java |
| `ldap_group_mapping` | String | *(empty string)* | Settings.java |
| `ldap_group_mapping_enabled` | Boolean | `true` | Settings.java |
| `ldap_group_mapping_sync_enabled` | Boolean | `false` | Settings.java |
| `ldap_group_mapping_sync_interval` | String | `0` | Settings.java |
| `ldap_group_mapping_sync_limit` | Integer | `0` | Settings.java |
| `ldap_group_members_filter` | String | `(&(objectCategory=user)(memberOf=%d))` | Settings.java |
| `ldap_group_search_filter` | String | `member=%d` | Settings.java |
| `ldap_group_target` | String | `cn` | Settings.java |
| `ldap_groups_search_filter` | String | `(&(objectCategory=group)(cn=%c))` | Settings.java |
| `ldap_groups_target` | String | `distinguishedName` | Settings.java |
| `ldap_krb_user_search_filter` | String | `krbPrincipalName=%s` | Settings.java |
| `ldap_user_dn` | String | *(empty string)* | Settings.java |
| `ldap_user_email` | String | `mail` | Settings.java |
| `ldap_user_givenName` | String | `givenName` | Settings.java |
| `ldap_user_id` | String | `uid` | Settings.java |
| `ldap_user_search_filter` | String | `uid=%s` | Settings.java |
| `ldap_user_surname` | String | `sn` | Settings.java |
| `library_install_timeout_minutes` | Integer | `60` | Settings.java |
| `lifecycle_webhook_cluster_id` | String | *(empty string)* | Settings.java |
| `lifecycle_webhook_secret` | String | *(empty string)* | Settings.java |
| `lifecycle_webhook_url` | String | *(empty string)* | Settings.java |
| `localhost` | Boolean | `false` | Settings.java |
| `login_page_overwrite` | String | *(empty string)* | Settings.java |
| `logstash_version` | String | *(empty string)* | Settings.java |
| `managed_cloud_provider_name` | String | `hopsworks.ai` | Settings.java |
| `managed_cloud_redirect_uri` | String | *(empty string)* | Settings.java |
| `managed_docker_registry` | Boolean | `false` | Settings.java |
| `management_mode` | String | `STANDALONE` | Settings.java |
| `master_encryption_password_value` | String | `encryption_master_password` | KubeSettings.java |
| `max_allowed_long_running_http_requests` | Integer | `50` | Settings.java |
| `max_concurrent_base_sync_ops` | Integer | `6` | Settings.java |
| `max_env_var_name_length` | Integer | `255` | Settings.java |
| `max_env_var_value_length` | Integer | `8192` | Settings.java |
| `max_env_vars_per_user` | Integer | `64` | Settings.java |
| `max_env_yml_byte_size` | Integer | `20000` | Settings.java |
| `max_num_proj_per_user` | Integer | `5` | Settings.java |
| `max_ongoing_opensearch_doc_write` | Integer | `100` | Settings.java |
| `max_project_cloned_environments` | Integer | `100` | Settings.java |
| `max_status_poll_retry` | Integer | `5` | Settings.java |
| `mount_hopsfs_in_python_deployments` | Boolean | `true` | Settings.java |
| `mount_hopsfs_in_python_job` | Boolean | `true` | Settings.java |
| `mount_hopsfs_in_ray_job_container` | Boolean | `true` | Settings.java |
| `ndb_version` | String | *(empty string)* | Settings.java |
| `news_webflow_api_key` | String | *(empty string)* | Settings.java |
| `news_webflow_api_url` | String | *(empty string)* | Settings.java |
| `notebook_converter_job_timeout_sec` | Long | `300` | Settings.java |
| `oauth_account_status` | Integer | `1` | Settings.java |
| `oauth_enabled` | Boolean | `false` | Settings.java |
| `oauth_group_mapping` | String | *(empty string)* | Settings.java |
| `oauth_group_mapping_enabled` | Boolean | `true` | Settings.java |
| `oauth_group_mapping_sync_enabled` | Boolean | `false` | Settings.java |
| `oauth_logout_redirect_uri` | String | `hopsworks/` | Settings.java |
| `oauth_redirect_uri` | String | `hopsworks/callback` | Settings.java |
| `ongoing_backup` | Boolean | `false` | Settings.java |
| `onlinefs_service_thread_number` | Integer | `10` | Settings.java |
| `opensearch_default_embedding_index` | String | *(empty string)* | Settings.java |
| `opensearch_index_mapping_limit` | Integer | `1000` | Settings.java |
| `opensearch_num_default_embedding_index` | Integer | `1` | Settings.java |
| `openshift` | Boolean | `false` | Settings.java |
| `payara_admin_password_value` | String | `admin_password` | KubeSettings.java |
| `payment_type` | String | `NOLIMIT` | Settings.java |
| `pki_ca_configuration` | String | *(empty string)* | CAConf.java |
| `platform_intelligence_llm_api_key` | String | *(empty string)* | Settings.java |
| `platform_intelligence_llm_base_url` | String | *(empty string)* | Settings.java |
| `platform_intelligence_llm_model` | String | `gpt-5.4-mini` | Settings.java |
| `preinstalled_python_lib_names` | String | `pydoop, pyspark, jupyterlab, hdfscontents, pyjks, hops-apache-beam, pyopenssl` | Settings.java |
| `project_namespace_labels` | String | *(empty string)* | Settings.java |
| `provenance_graph_max_size` | Integer | `50` | Settings.java |
| `public_projects` | String | *(empty string)* | Settings.java |
| `pypi_indexer_timer_enabled` | Boolean | `true` | Settings.java |
| `pypi_indexer_timer_interval` | String | `1d` | Settings.java |
| `pypi_rest_endpoint` | String | `https://pypi.org/pypi/{package}/json` | Settings.java |
| `pypi_simple_endpoint` | String | `https://pypi.org/simple/` | Settings.java |
| `python_app_envoy_cpu` | Double | `0.1` | Settings.java |
| `python_app_envoy_image` | String | `envoyproxy/envoy:v1.38.0` | Settings.java |
| `python_app_envoy_memory_mb` | Integer | `128` | Settings.java |
| `python_job_cores` | Double | `1.0` | Settings.java |
| `python_job_gpus` | Integer | `0` | Settings.java |
| `python_job_kube_waiting_timeout_ms` | Long | `300000` | Settings.java |
| `python_job_memory` | Integer | `2048` | Settings.java |
| `python_library_updates_monitor_interval` | String | `1d` | Settings.java |
| `python_pod_kill_grace_period_seconds` | Long | `600` | Settings.java |
| `pythonapp_cores` | Double | `1.0` | Settings.java |
| `pythonapp_gpus` | Integer | `0` | Settings.java |
| `pythonapp_memory` | Integer | `2048` | Settings.java |
| `quotas_featuregroups_online_disabled` | Long | `-1` | Settings.java |
| `quotas_featuregroups_online_enabled` | Long | `-1` | Settings.java |
| `quotas_max_parallel_executions` | Long | `-1` | Settings.java |
| `quotas_max_queued_executions_per_user_per_job` | Long | `10` | Settings.java |
| `quotas_model_deployments_running` | Long | `-1` | Settings.java |
| `quotas_model_deployments_total` | Long | `-1` | Settings.java |
| `quotas_training_datasets` | Long | `-1` | Settings.java |
| `ray_certs_dir` | String | `PlatformConstants.RAY_CERTS_DIR` *(computed expression, not a literal)* | Settings.java |
| `ray_cluster_max_worker_replicas` | Long | `20` | Settings.java |
| `ray_cluster_shutdown_after_completion` | Boolean | `true` | Settings.java |
| `ray_cluster_start_wait_time_seconds` | Integer | `120` | Settings.java |
| `ray_cluster_termination_grace_period_seconds` | Integer | `10` | Settings.java |
| `ray_enabled` | Boolean | `true` | Settings.java |
| `ray_job_active_deadline_seconds` | Integer | `120` | Settings.java |
| `ray_job_driver_cores` | Double | `1.0` | Settings.java |
| `ray_job_driver_gpus` | Integer | `0` | Settings.java |
| `ray_job_driver_memory` | Integer | `2048` | Settings.java |
| `ray_job_pod_kill_grace_period_seconds` | Integer | `300` | Settings.java |
| `ray_job_worker_cores` | Double | `1.0` | Settings.java |
| `ray_job_worker_gpus` | Integer | `0` | Settings.java |
| `ray_job_worker_memory` | Integer | `4096` | Settings.java |
| `ray_materialization_dir` | String | `/srv/hops/ray/job` | Settings.java |
| `ray_version` | String | `2.9.0` | Settings.java |
| `ray_warehouse_dir` | String | `ray-warehouse` | Settings.java |
| `reject_remote_user_no_group` | Boolean | `false` | Settings.java |
| `remote_auth_need_consent` | Boolean | `true` | Settings.java |
| `remote_shuffle_services_storage_type` | String | `MEMORY_LOCALFILE` | Settings.java |
| `replicated_kubernetes_ops_retention` | String | `P15D` | Settings.java |
| `requests_verify` | Boolean | `false` | Settings.java |
| `reserved_project_names` | String | `hopsworks,information_schema,airflow,glassfish_timers,grafana,hops,metastore,mysql,ndbinfo,performance_schema,sqoop,sys,base,python37,python38,python39,python310,filebeat,git,onlinefs,sklearnserver,rondb_replication,default,kube-system,kube-public,kube-node-lease,kube_system,kube_public,kube_node_lease,trino` | Settings.java |
| `resource_dirs` | String | `".sparkStaging;spark-warehouse;.flinkStaging;.flinkCheckpoints;apps;jobs;" + DLT_WAREHOUSE_DIR.getDefaultValue() + ";" + RAY_WAREHOUSE_DIR.getDefaultValue()` *(computed expression, not a literal)* | Settings.java |
| `rondb_mgmt_connection_timeout` | Integer | `5000` | Settings.java |
| `rondb_mgmt_max_response_lines` | Integer | `10000` | Settings.java |
| `rondb_mgmt_read_timeout` | Integer | `10000` | Settings.java |
| `rondb_quotas` | String | *(empty string)* | Settings.java |
| `rondb_usage_cache_ttl_seconds` | Integer | `60` | Settings.java |
| `rondb_usage_query_timeout_seconds` | Integer | `10` | Settings.java |
| `saas_entry_point_url` | String | *(empty string)* | Settings.java |
| `service_discovery_domain` | String | `consul` *(duplicate key, also declared in Settings.java; values match)* | CAConf.java |
| `service_discovery_domain` | String | `consul` *(duplicate key, also declared in CAConf.java; values match)* | Settings.java |
| `service_jwt_exp_leeway_sec` | Integer | `43200` | Settings.java |
| `service_jwt_lifetime_ms` | Long | `86400000` | Settings.java |
| `service_key_rotation_enabled` | String | `false` | CAConf.java |
| `service_key_rotation_interval` | String | `3d` | CAConf.java |
| `serving_allow_stop_after_seconds` | Integer | `0` | Settings.java |
| `serving_connection_pool_size` | Integer | `40` | Settings.java |
| `serving_feature_logger_client_pool_size` | String | `3` | Settings.java |
| `serving_feature_logger_client_req_timeout_seconds` | Integer | `3` | Settings.java |
| `serving_max_route_connections` | Integer | `10` | Settings.java |
| `serving_monitor_int` | String | `30s` | Settings.java |
| `serving_redeploy_not_found_after_seconds` | Integer | `120` | Settings.java |
| `serving_state_manager_batch_size` | Integer | `1000` | Settings.java |
| `serving_state_manager_enabled` | Boolean | `true` | Settings.java |
| `serving_state_manager_interval_ms` | Integer | `600000` | Settings.java |
| `spark_configmap_name` | String | `spark` | Settings.java |
| `spark_dir` | String | `/srv/hops/spark` | Settings.java |
| `spark_executor_min_memory` | Integer | `1024` | Settings.java |
| `spark_history_server_enabled` | Boolean | `true` | Settings.java |
| `spark_job_driver_cores` | Double | `1.0` | Settings.java |
| `spark_job_driver_memory` | Integer | `2048` | Settings.java |
| `spark_job_executor_cores` | Double | `1.0` | Settings.java |
| `spark_job_executor_memory` | Integer | `4096` | Settings.java |
| `spark_kubernetes_materialisation_dir` | String | `/srv/hops/artifacts` | Settings.java |
| `spark_launcher_sa_annotations` | String | *(empty string)* | Settings.java |
| `spark_pod_kill_grace_period_seconds` | Integer | `1200` | Settings.java |
| `spark_remove_job_when_completed` | Boolean | `true` | Settings.java |
| `spark_resource_manager` | String | `kubernetes` | Settings.java |
| `spark_ui_logs_offset` | Integer | `512000` | Settings.java |
| `spark_user` | String | `spark` | Settings.java |
| `spark_version` | String | *(empty string)* | Settings.java |
| `sql_max_select_in` | Integer | `100` | Settings.java |
| `staging_dir` | String | `/srv/hops/domains/domain1/staging` | Settings.java |
| `statistics_cleaner_batch_size` | Integer | `1000` | Settings.java |
| `statistics_cleaner_interval_ms` | Integer | `900000` | Settings.java |
| `streamlit_sharing` | Boolean | `false` | Settings.java |
| `sudoers_dir` | String | `/srv/hops/sbin` *(duplicate key, also declared in Settings.java; values match)* | CAConf.java |
| `sudoers_dir` | String | `/srv/hops/sbin` *(duplicate key, also declared in CAConf.java; values match)* | Settings.java |
| `superset_admin_roles` | String | `Admin` | Settings.java |
| `superset_ca_cert_path` | String | `/srv/hops/super_crypto/superset/hops_ca_bundle.pem` | Settings.java |
| `superset_enabled` | Boolean | `false` | Settings.java |
| `superset_proxy_connect_timeout_ms` | Integer | `10000` | Settings.java |
| `superset_proxy_connection_request_timeout_ms` | Integer | `10000` | Settings.java |
| `superset_proxy_max_connections` | Integer | `50` | Settings.java |
| `superset_proxy_read_timeout_ms` | Integer | `180000` | Settings.java |
| `superset_secret` | String | `superset-admin-credentials` | KubeSettings.java |
| `superset_user_roles` | String | `Gamma,sql_lab` | Settings.java |
| `tensorflow_version` | String | *(empty string)* | Settings.java |
| `terminal_gpu_image` | String | `terminal-gpu` | Settings.java |
| `terminal_image` | String | `terminal-server` | Settings.java |
| `terminal_session_hours` | Integer | `4` | Settings.java |
| `terminal_shm_size` | String | `1Gi` | Settings.java |
| `terminal_spark_image` | String | `terminal-spark` | Settings.java |
| `testconnector_image` | String | `docker.hops.works/hopsworks/testconnector:0.2` | Settings.java |
| `testconnector_launcher` | String | `testconnector-launch.sh` | Settings.java |
| `trino_credentials_secret` | String | `trino-admin-credentials` | KubeSettings.java |
| `trino_default_catalog` | String | `hive` | Settings.java |
| `trino_enabled` | Boolean | `false` | Settings.java |
| `trino_events_cleaner_batch_size` | Integer | `1000` | Settings.java |
| `trino_events_delete_after_days` | Integer | `61` | Settings.java |
| `trino_group_secret` | String | `trino-groups-file` | KubeSettings.java |
| `trino_password_secret` | String | `trino-password-file` | KubeSettings.java |
| `twofactor-excluded-groups` | String | `AGENT;CLUSTER_AGENT` | Settings.java |
| `twofactor_auth` | String | `false` | Settings.java |
| `unity_catalog_oauth_m2m_enabled` | Boolean | `true` | Settings.java |
| `upload_chunk_size` | Integer | `10485760` | Settings.java |
| `validate_remote_user_email_verified` | Boolean | `false` | Settings.java |
| `velero_backup_main_schedule_name` | String | *(empty string)* | Settings.java |
| `velero_backup_storage_location_name` | String | *(empty string)* | Settings.java |
| `velero_backup_users_schedule_name` | String | *(empty string)* | Settings.java |
| `velero_namespace` | String | *(empty string)* | Settings.java |
| `whitelist_users` | String | `agent@hops.io` | Settings.java |
| `yarn_app_uid` | Long | `1235` | Settings.java |
| `yarn_default_quota` | Integer | `60000` | Settings.java |
| `zookeeper_version` | String | *(empty string)* | Settings.java |

<!-- END GENERATED -->
