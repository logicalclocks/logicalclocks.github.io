# Content Parity Review

Page-by-page review of the refactor branch against `main`: content parity (nothing lost, nothing invented) and readability.
Order follows the `mkdocs.yml` nav; pages not in the nav (deleted, or orphaned) come last.

Status: `[ ]` pending, `[x]` reviewed OK, `[!]` reviewed with a follow-up noted at the bottom.

| Status | Page | Change | +/- |
| ------ | ---- | ------ | --- |
| [ ] | `concepts/index.md` | added | +26/-0 |
| [ ] | `concepts/hopsworks.md` | modified | +12/-7 |
| [ ] | `concepts/projects/governance.md` | modified | +4/-2 |
| [ ] | `concepts/projects/storage.md` | modified | +5/-2 |
| [ ] | `concepts/fti.md` | added | +66/-0 |
| [ ] | `concepts/fs/index.md` | modified | +4/-2 |
| [x] | `concepts/fs/feature_group/fg_overview.md` | modified | +19/-11 |
| [!] | `concepts/fs/feature_group/write_apis.md` | modified | +8/-7 |
| [ ] | `concepts/fs/feature_group/external_fg.md` | modified | +5/-3 |
| [x] | `concepts/fs/feature_group/feature_pipelines.md` | modified | +18/-22 |
| [ ] | `concepts/fs/feature_group/streaming_feature_pipelines.md` | added | +30/-0 |
| [ ] | `concepts/mlops/data_transformations.md` | modified | +11/-5 |
| [ ] | `concepts/fs/feature_view/fv_overview.md` | modified | +8/-3 |
| [ ] | `concepts/fs/feature_view/offline_api.md` | modified | +9/-5 |
| [ ] | `concepts/fs/feature_group/spine_group.md` | modified | +6/-3 |
| [ ] | `concepts/fs/feature_view/online_api.md` | modified | +17/-3 |
| [ ] | `concepts/fs/feature_view/training_inference_pipelines.md` | modified | +7/-4 |
| [ ] | `concepts/fs/feature_group/on_demand_feature.md` | modified | +11/-1 |
| [ ] | `concepts/fs/feature_group/fg_statistics.md` | modified | +6/-4 |
| [ ] | `concepts/fs/feature_group/feature_monitoring.md` | modified | +23/-11 |
| [x] | `concepts/fs/feature_group/versioning.md` | modified | +30/-6 |
| [ ] | `concepts/projects/search.md` | modified | +28/-5 |
| [ ] | `concepts/projects/cicd.md` | modified | +7/-8 |
| [ ] | `concepts/mlops/training.md` | modified | +14/-2 |
| [ ] | `concepts/mlops/registry.md` | modified | +3/-1 |
| [ ] | `concepts/mlops/serving.md` | modified | +25/-1 |
| [ ] | `concepts/mlops/model_monitoring.md` | modified | +16/-3 |
| [ ] | `concepts/mlops/prediction_services.md` | modified | +34/-17 |
| [ ] | `concepts/mlops/agents.md` | added | +27/-0 |
| [ ] | `concepts/mlops/opensearch.md` | modified | +9/-4 |
| [ ] | `concepts/dev/inside.md` | modified | +9/-7 |
| [ ] | `concepts/dev/outside.md` | modified | +4/-2 |
| [ ] | `concepts/mlops/bi_tools.md` | modified | +2/-0 |
| [ ] | `user_guides/fs/data_source/index.md` | modified | +137/-17 |
| [ ] | `user_guides/fs/data_source/creation/jdbc.md` | modified | +5/-2 |
| [ ] | `user_guides/fs/data_source/creation/snowflake.md` | modified | +5/-2 |
| [ ] | `user_guides/fs/data_source/creation/kafka.md` | modified | +7/-3 |
| [ ] | `user_guides/fs/data_source/creation/hopsfs.md` | modified | +5/-2 |
| [ ] | `user_guides/fs/data_source/creation/s3.md` | modified | +4/-1 |
| [ ] | `user_guides/fs/data_source/creation/glue.md` | modified | +7/-3 |
| [ ] | `user_guides/fs/data_source/creation/redshift.md` | modified | +5/-2 |
| [ ] | `user_guides/fs/data_source/creation/adls.md` | modified | +6/-2 |
| [ ] | `user_guides/fs/data_source/creation/bigquery.md` | modified | +5/-2 |
| [ ] | `user_guides/fs/data_source/creation/gcs.md` | modified | +5/-2 |
| [ ] | `user_guides/fs/data_source/creation/sql.md` | modified | +14/-3 |
| [ ] | `user_guides/fs/data_source/creation/crm_sales_analytics.md` | modified | +6/-4 |
| [ ] | `user_guides/fs/data_source/creation/rest_api.md` | modified | +5/-3 |
| [ ] | `user_guides/fs/data_source/creation/unity_catalog.md` | modified | +19/-12 |
| [ ] | `user_guides/fs/data_source/creation/sap_hana.md` | modified | +3/-1 |
| [ ] | `user_guides/fs/data_source/usage.md` | modified | +2/-0 |
| [ ] | `user_guides/fs/feature_group/create.md` | modified | +12/-33 |
| [ ] | `user_guides/fs/feature_group/create_external.md` | modified | +1/-1 |
| [ ] | `user_guides/fs/feature_group/data_types.md` | modified | +47/-38 |
| [ ] | `user_guides/fs/feature_group/data_validation.md` | modified | +2/-2 |
| [ ] | `user_guides/fs/feature_group/data_validation_advanced.md` | modified | +1/-1 |
| [ ] | `user_guides/fs/feature_group/feature_monitoring.md` | modified | +2/-2 |
| [ ] | `user_guides/fs/feature_group/notification.md` | modified | +0/-11 |
| [ ] | `user_guides/fs/feature_group/online_ingestion_observability.md` | modified | +1/-1 |
| [ ] | `user_guides/fs/feature_group/ttl.md` | modified | +120/-0 |
| [ ] | `user_guides/fs/feature_view/training-data.md` | modified | +1/-1 |
| [ ] | `user_guides/fs/feature_view/batch-data.md` | modified | +6/-6 |
| [ ] | `user_guides/fs/feature_view/feature_monitoring.md` | modified | +2/-2 |
| [ ] | `user_guides/fs/compute_engines.md` | modified | +14/-27 |
| [ ] | `user_guides/integrations/index.md` | modified | +0/-1 |
| [ ] | `user_guides/integrations/python.md` | modified | +1/-1 |
| [ ] | `user_guides/integrations/emr/emr_configuration.md` | modified | +1/-1 |
| [ ] | `user_guides/integrations/hdinsight.md` | modified | +1/-1 |
| [ ] | `user_guides/integrations/mlstudio_designer.md` | modified | +1/-1 |
| [ ] | `user_guides/integrations/mlstudio_notebooks.md` | modified | +1/-1 |
| [ ] | `user_guides/fs/sharing/sharing.md` | modified | +65/-3 |
| [ ] | `user_guides/fs/tags/tags.md` | modified | +119/-6 |
| [ ] | `user_guides/fs/tags/keywords.md` | added | +130/-0 |
| [ ] | `user_guides/fs/feature_monitoring/index.md` | modified | +1/-1 |
| [ ] | `user_guides/fs/feature_monitoring/distribution_comparison.md` | modified | +10/-10 |
| [ ] | `user_guides/projects/auth/registration.md` | modified | +6/-13 |
| [ ] | `user_guides/projects/project/create_project.md` | modified | +1/-2 |
| [ ] | `user_guides/projects/project/manage_members.md` | modified | +25/-0 |
| [ ] | `user_guides/projects/search.md` | added | +112/-0 |
| [ ] | `user_guides/projects/python/python_env_overview.md` | modified | +14/-12 |
| [ ] | `user_guides/projects/python/python_install.md` | modified | +43/-3 |
| [ ] | `user_guides/projects/python/python_env_export.md` | modified | +6/-1 |
| [ ] | `user_guides/projects/python/custom_commands.md` | modified | +67/-3 |
| [ ] | `user_guides/projects/python/environment_history.md` | modified | +1/-1 |
| [ ] | `user_guides/projects/jupyter/python_notebook.md` | modified | +3/-3 |
| [ ] | `user_guides/projects/jupyter/spark_notebook.md` | modified | +2/-2 |
| [ ] | `user_guides/projects/jupyter/ray_notebook.md` | modified | +4/-2 |
| [ ] | `user_guides/projects/terminal.md` | added | +52/-0 |
| [ ] | `user_guides/projects/jobs/python_job.md` | modified | +13/-15 |
| [ ] | `user_guides/projects/jobs/notebook_job.md` | modified | +6/-5 |
| [ ] | `user_guides/projects/jobs/pyspark_job.md` | modified | +5/-4 |
| [ ] | `user_guides/projects/jobs/spark_job.md` | modified | +9/-10 |
| [ ] | `user_guides/projects/jobs/ray_job.md` | modified | +7/-4 |
| [ ] | `user_guides/projects/jobs/schedule_job.md` | modified | +25/-25 |
| [ ] | `user_guides/projects/jobs/batch_feature_pipeline.md` | modified | +12/-12 |
| [ ] | `user_guides/projects/scheduling/kube_scheduler.md` | modified | +2/-2 |
| [ ] | `user_guides/projects/scheduling/kueue_details.md` | modified | +1/-1 |
| [ ] | `user_guides/projects/airflow/airflow.md` | modified | +1/-1 |
| [ ] | `user_guides/projects/airflow/airflow3_upgrade.md` | modified | +7/-7 |
| [ ] | `user_guides/projects/airflow/security_model.md` | modified | +2/-2 |
| [ ] | `user_guides/projects/alerts/index.md` | added | +80/-0 |
| [ ] | `user_guides/projects/git/configure_git_provider.md` | modified | +4/-2 |
| [ ] | `user_guides/projects/git/clone_repo.md` | modified | +2/-2 |
| [ ] | `user_guides/projects/git/repository_actions.md` | modified | +3/-8 |
| [ ] | `user_guides/projects/datasets/sharing.md` | added | +41/-0 |
| [ ] | `user_guides/projects/secrets/create_secret.md` | modified | +2/-2 |
| [ ] | `user_guides/projects/env_vars/create.md` | modified | +2/-2 |
| [ ] | `user_guides/projects/trino/query_engine.md` | modified | +114/-0 |
| [ ] | `user_guides/projects/trino/catalogs.md` | added | +141/-0 |
| [ ] | `user_guides/projects/superset/superset.md` | modified | +27/-13 |
| [ ] | `user_guides/projects/python-deployment/python-deployment.md` | modified | +1/-1 |
| [ ] | `user_guides/projects/python-deployment/rest-api.md` | modified | +1/-1 |
| [ ] | `user_guides/mlops/registry/index.md` | modified | +39/-5 |
| [ ] | `user_guides/mlops/registry/import_huggingface.md` | modified | +11/-11 |
| [ ] | `user_guides/mlops/serving/deployment.md` | modified | +9/-10 |
| [ ] | `user_guides/mlops/serving/predictor.md` | modified | +19/-19 |
| [ ] | `user_guides/mlops/serving/resources.md` | modified | +1/-1 |
| [ ] | `user_guides/mlops/serving/autoscaling.md` | modified | +2/-2 |
| [ ] | `user_guides/mlops/serving/scheduling.md` | modified | +2/-2 |
| [ ] | `user_guides/mlops/model_monitoring/index.md` | modified | +1/-1 |
| [ ] | `user_guides/client_installation/index.md` | modified | +1/-13 |
| [ ] | `setup_installation/aws/getting_started.md` | modified | +2/-2 |
| [ ] | `setup_installation/admin/variables.md` | modified | +1/-1 |
| [ ] | `setup_installation/admin/configuration_reference.md` | added | +517/-0 |
| [ ] | `setup_installation/admin/build_performance.md` | added | +261/-0 |
| [ ] | `setup_installation/admin/user.md` | modified | +52/-10 |
| [ ] | `setup_installation/admin/project.md` | modified | +2/-2 |
| [ ] | `setup_installation/admin/alert.md` | modified | +25/-11 |
| [ ] | `setup_installation/admin/configure-project-mapping.md` | modified | +2/-2 |
| [ ] | `setup_installation/admin/airflow3.md` | modified | +4/-4 |
| [ ] | `setup_installation/admin/search_index.md` | added | +93/-0 |
| [ ] | `setup_installation/admin/monitoring/grafana.md` | modified | +4/-4 |
| [ ] | `setup_installation/admin/monitoring/services-logs.md` | modified | +4/-4 |
| [ ] | `setup_installation/admin/monitoring/websocket-pool.md` | modified | +3/-2 |
| [ ] | `setup_installation/admin/auth.md` | modified | +10/-8 |
| [ ] | `setup_installation/admin/oauth2/create-client.md` | modified | +1/-1 |
| [ ] | `setup_installation/admin/oauth2/configure-project-mapping.md` | modified | +2/-2 |
| [ ] | `setup_installation/admin/ldap/configure-ldap.md` | modified | +1/-1 |
| [ ] | `setup_installation/admin/ldap/configure-krb.md` | modified | +1/-1 |
| [ ] | `setup_installation/admin/ldap/configure-project-mapping.md` | modified | +2/-2 |
| [ ] | `setup_installation/admin/ha-dr/dr.md` | modified | +3/-3 |
| [ ] | `setup_installation/admin/audit/audit-logs.md` | modified | +9/-9 |
| [ ] | `setup_installation/admin/trino.md` | modified | +198/-1 |
| [ ] | `setup_installation/admin/superset.md` | modified | +37/-6 |
| [ ] | `reference/rest_error_codes.md` | added | +1225/-0 |
| [x] | `concepts/fs/feature_view/feature_monitoring.md` | deleted, merged into `concepts/fs/feature_group/feature_monitoring.md` (Monitoring a feature view) | +0/-26 |
| [x] | `concepts/fs/feature_view/statistics.md` | deleted, merged into `concepts/fs/feature_group/feature_monitoring.md` (Statistics on training data) | +0/-5 |
| [x] | `concepts/fs/feature_view/versioning.md` | deleted, merged into `concepts/fs/feature_group/versioning.md` | +0/-6 |
| [ ] | `tutorials/index.md` | modified | +1/-1 |
| [ ] | `user_guides/integrations/flink.md` | deleted | +0/-39 |

## Follow-ups

- `concepts/fs/feature_group/write_apis.md`: prose still says Hudi DeltaStreamer and Apache Hudi dedup for the offline path, while every diagram on the branch labels the offline store Delta. Decide the 5.x wording and align prose or figures.
