# Diagram Inventory

Worklist for the diagram refresh: every visual on every page moves to the hops-viz kit (animated scene where the mechanism is the message, static kit SVG otherwise).

Rules of engagement are in `design-system.md` (Diagrams section).

UI screenshots and product GIFs are NOT diagrams: mark them `screenshot, keep` and move on.

Status: `[ ]` todo, `[x]` done, `[-]` triaged out (screenshot or removed).

2026-08-19: all 43 inline kit figures were extracted to `diagrams/` in one mechanical sweep (main session).
The `[x]` tick still requires the per-page design pass (animate mechanisms, rebuild images/mermaid, triage screenshots).


## concepts

- [x] `docs/concepts/dev/inside.md` — capability map, static by design
- [x] `docs/concepts/dev/outside.md` — capability map, static by design
- [x] `docs/concepts/fs/feature_group/external_fg.md` — 1 animated (query pushdown at read time)
- [x] `docs/concepts/fs/feature_group/feature_pipelines.md` — 1 animated (stage walk + STRICT reject), 1 static kept (transform taxonomy flow)
- [x] `docs/concepts/fs/feature_group/fg_overview.md` — 1 animated (upsert vs append), 1 static kept (table anatomy)
- [x] `docs/concepts/fs/feature_group/fg_statistics.md` — 1 animated (write → validation report + statistics)
- [x] `docs/concepts/fs/feature_group/on_demand_feature.md` — 1 animated (one UDF, two pipelines, vector merge)
- [x] `docs/concepts/fs/feature_group/versioning.md` — 1 animated (inserts append commits, as_of cutoff), 2 static kept (schema v1→v2, fv/td grid)
- [x] `docs/concepts/fs/feature_group/write_apis.md` — 2 animated (stream: at-least-once→exactly-once dup story; batch: dual path, HDFS direct)
- [x] `docs/concepts/fs/feature_view/fv_overview.md` — 2 static kept (schema inheritance, fv dual outputs); mechanisms animated on online/offline api pages
- [x] `docs/concepts/fs/feature_view/offline_api.md` — 1 animated (PIT join sweep), 2 static kept (column lineage, batch ranges)
- [x] `docs/concepts/fs/feature_view/online_api.md` — 1 animated (get_feature_vector assembly, narrated steps)
- [x] `docs/concepts/fs/feature_view/training_inference_pipelines.md` — 1 animated (skew two-act: same udf then drift, 800 viewBox)
- [x] `docs/concepts/fs/index.md` — navigational chart, static by charter
- [x] `docs/concepts/fti.md` — navigational chart, static by charter
- [x] `docs/concepts/hopsworks.md` — navigational chart, static by charter
- [ ] `docs/concepts/mlops/agents.md` — 1 kit-static
- [ ] `docs/concepts/mlops/data_transformations.md` — 5 kit-static
- [ ] `docs/concepts/mlops/model_monitoring.md` — 1 kit-static
- [ ] `docs/concepts/mlops/opensearch.md` — 1 kit-static
- [ ] `docs/concepts/mlops/prediction_services.md` — 3 kit-static
- [ ] `docs/concepts/mlops/registry.md` — 1 kit-static
- [ ] `docs/concepts/mlops/serving.md` — 1 kit-static
- [ ] `docs/concepts/mlops/training.md` — 1 kit-static
- [ ] `docs/concepts/projects/cicd.md` — 2 kit-static
- [ ] `docs/concepts/projects/governance.md` — 1 kit-static
- [ ] `docs/concepts/projects/search.md` — 2 image(s)
- [ ] `docs/concepts/projects/storage.md` — 1 kit-static

## user_guides

- [ ] `docs/user_guides/fs/data_source/creation/adls.md` — 5 image(s)
- [ ] `docs/user_guides/fs/data_source/creation/bigquery.md` — 2 image(s)
- [ ] `docs/user_guides/fs/data_source/creation/crm_sales_analytics.md` — 10 image(s)
- [ ] `docs/user_guides/fs/data_source/creation/gcs.md` — 2 image(s)
- [ ] `docs/user_guides/fs/data_source/creation/glue.md` — 3 image(s)
- [ ] `docs/user_guides/fs/data_source/creation/hopsfs.md` — 2 image(s)
- [ ] `docs/user_guides/fs/data_source/creation/jdbc.md` — 2 image(s)
- [ ] `docs/user_guides/fs/data_source/creation/kafka.md` — 2 image(s)
- [ ] `docs/user_guides/fs/data_source/creation/redshift.md` — 4 image(s)
- [ ] `docs/user_guides/fs/data_source/creation/rest_api.md` — 2 image(s)
- [ ] `docs/user_guides/fs/data_source/creation/s3.md` — 2 image(s)
- [ ] `docs/user_guides/fs/data_source/creation/sap_hana.md` — 1 image(s)
- [ ] `docs/user_guides/fs/data_source/creation/snowflake.md` — 3 image(s)
- [ ] `docs/user_guides/fs/data_source/creation/sql.md` — 2 image(s)
- [ ] `docs/user_guides/fs/data_source/creation/unity_catalog.md` — 1 image(s)
- [ ] `docs/user_guides/fs/data_source/index.md` — 1 image(s)
- [ ] `docs/user_guides/fs/feature_group/create.md` — 1 image(s)
- [ ] `docs/user_guides/fs/feature_group/create_external.md` — 5 image(s)
- [ ] `docs/user_guides/fs/feature_group/data_validation.md` — 1 image(s)
- [ ] `docs/user_guides/fs/feature_group/deprecation.md` — 3 image(s)
- [ ] `docs/user_guides/fs/feature_group/ingest_with_dlthub.md` — 6 image(s)
- [ ] `docs/user_guides/fs/feature_group/notification.md` — 1 image(s)
- [ ] `docs/user_guides/fs/feature_group/online_ingestion_observability.md` — 1 image(s)
- [ ] `docs/user_guides/fs/feature_monitoring/index.md` — 3 image(s)
- [ ] `docs/user_guides/fs/feature_monitoring/interactive_graph.md` — 8 image(s)
- [ ] `docs/user_guides/fs/feature_monitoring/scheduled_statistics.md` — 2 image(s)
- [ ] `docs/user_guides/fs/feature_monitoring/statistics_comparison.md` — 3 image(s)
- [ ] `docs/user_guides/fs/feature_view/query.md` — 2 image(s)
- [ ] `docs/user_guides/fs/provenance/provenance.md` — 2 image(s)
- [ ] `docs/user_guides/fs/sharing/sharing.md` — 9 image(s)
- [ ] `docs/user_guides/fs/tags/mandatory_tags.md` — 2 image(s)
- [ ] `docs/user_guides/fs/tags/tags.md` — 3 image(s)
- [ ] `docs/user_guides/fs/vector_similarity_search.md` — 1 image(s)
- [ ] `docs/user_guides/integrations/databricks/configuration.md` — 3 image(s)
- [ ] `docs/user_guides/integrations/databricks/networking.md` — 15 image(s)
- [ ] `docs/user_guides/integrations/emr/emr_configuration.md` — 7 image(s)
- [ ] `docs/user_guides/integrations/emr/networking.md` — 6 image(s)
- [ ] `docs/user_guides/integrations/hdinsight.md` — 1 image(s)
- [ ] `docs/user_guides/integrations/mlstudio_designer.md` — 8 image(s)
- [ ] `docs/user_guides/integrations/mlstudio_notebooks.md` — 2 image(s)
- [ ] `docs/user_guides/integrations/python.md` — 1 image(s)
- [ ] `docs/user_guides/integrations/spark.md` — 1 image(s)
- [ ] `docs/user_guides/mlops/provenance/provenance.md` — 1 image(s)
- [ ] `docs/user_guides/mlops/serving/api-protocol.md` — 3 image(s)
- [ ] `docs/user_guides/mlops/serving/autoscaling.md` — 3 image(s)
- [ ] `docs/user_guides/mlops/serving/deployment-state.md` — 6 image(s)
- [ ] `docs/user_guides/mlops/serving/deployment.md` — 7 image(s)
- [ ] `docs/user_guides/mlops/serving/external-access.md` — 9 image(s)
- [ ] `docs/user_guides/mlops/serving/inference-batcher.md` — 3 image(s)
- [ ] `docs/user_guides/mlops/serving/inference-logger.md` — 3 image(s)
- [ ] `docs/user_guides/mlops/serving/predictor.md` — 7 image(s)
- [ ] `docs/user_guides/mlops/serving/resources.md` — 3 image(s)
- [ ] `docs/user_guides/mlops/serving/scheduling.md` — 5 image(s)
- [ ] `docs/user_guides/mlops/serving/transformer.md` — 4 image(s)
- [ ] `docs/user_guides/mlops/serving/troubleshooting.md` — 4 image(s)
- [ ] `docs/user_guides/projects/airflow/airflow.md` — 1 image(s)
- [ ] `docs/user_guides/projects/api_key/create_api_key.md` — 2 image(s)
- [ ] `docs/user_guides/projects/auth/krb.md` — 5 image(s)
- [ ] `docs/user_guides/projects/auth/ldap.md` — 3 image(s)
- [ ] `docs/user_guides/projects/auth/login.md` — 3 image(s)
- [ ] `docs/user_guides/projects/auth/oauth.md` — 3 image(s)
- [ ] `docs/user_guides/projects/auth/profile.md` — 4 image(s)
- [ ] `docs/user_guides/projects/auth/recovery.md` — 1 image(s)
- [ ] `docs/user_guides/projects/auth/registration.md` — 2 image(s)
- [ ] `docs/user_guides/projects/git/clone_repo.md` — 4 image(s)
- [ ] `docs/user_guides/projects/git/configure_git_provider.md` — 3 image(s)
- [ ] `docs/user_guides/projects/git/repository_actions.md` — 1 image(s)
- [ ] `docs/user_guides/projects/iam_role/iam_role_chaining.md` — 1 image(s)
- [ ] `docs/user_guides/projects/jobs/notebook_job.md` — 9 image(s)
- [ ] `docs/user_guides/projects/jobs/pyspark_job.md` — 9 image(s)
- [ ] `docs/user_guides/projects/jobs/python_job.md` — 8 image(s)
- [ ] `docs/user_guides/projects/jobs/ray_job.md` — 9 image(s)
- [ ] `docs/user_guides/projects/jobs/schedule_job.md` — 2 image(s)
- [ ] `docs/user_guides/projects/jobs/spark_job.md` — 10 image(s)
- [ ] `docs/user_guides/projects/jupyter/python_notebook.md` — 7 image(s)
- [ ] `docs/user_guides/projects/jupyter/ray_notebook.md` — 8 image(s)
- [ ] `docs/user_guides/projects/jupyter/session_capacity_warnings.md` — 3 image(s)
- [ ] `docs/user_guides/projects/jupyter/spark_notebook.md` — 9 image(s)
- [ ] `docs/user_guides/projects/project/create_project.md` — 4 image(s)
- [ ] `docs/user_guides/projects/project/manage_members.md` — 4 image(s)
- [ ] `docs/user_guides/projects/python-deployment/python-deployment.md` — 2 image(s)
- [ ] `docs/user_guides/projects/python-deployment/troubleshooting.md` — 4 image(s)
- [ ] `docs/user_guides/projects/python/custom_commands.md` — 1 image(s)
- [ ] `docs/user_guides/projects/python/environment_history.md` — 2 image(s)
- [ ] `docs/user_guides/projects/python/python_env_clone.md` — 3 image(s)
- [ ] `docs/user_guides/projects/python/python_env_export.md` — 1 image(s)
- [ ] `docs/user_guides/projects/python/python_env_overview.md` — 1 image(s)
- [ ] `docs/user_guides/projects/python/python_install.md` — 4 image(s)
- [ ] `docs/user_guides/projects/scheduling/kube_scheduler.md` — 7 image(s)
- [ ] `docs/user_guides/projects/scheduling/kueue_details.md` — 2 image(s)
- [ ] `docs/user_guides/projects/secrets/create_secret.md` — 3 image(s)
- [ ] `docs/user_guides/projects/superset/superset.md` — 5 image(s)
- [ ] `docs/user_guides/projects/terminal.md` — 2 image(s)
- [ ] `docs/user_guides/projects/trino/query_engine.md` — 11 image(s)

## setup_installation

- [ ] `docs/setup_installation/admin/alert.md` — 6 image(s)
- [ ] `docs/setup_installation/admin/audit/audit-logs.md` — 1 image(s)
- [ ] `docs/setup_installation/admin/auth.md` — 1 image(s)
- [ ] `docs/setup_installation/admin/configure-project-mapping.md` — 6 image(s)
- [ ] `docs/setup_installation/admin/ha-dr/dr.md` — 2 image(s)
- [ ] `docs/setup_installation/admin/ha-dr/ha.md` — 1 image(s)
- [ ] `docs/setup_installation/admin/ldap/configure-krb.md` — 3 image(s)
- [ ] `docs/setup_installation/admin/ldap/configure-ldap.md` — 3 image(s)
- [ ] `docs/setup_installation/admin/ldap/configure-project-mapping.md` — 6 image(s)
- [ ] `docs/setup_installation/admin/ldap/configure-server.md` — 1 image(s)
- [ ] `docs/setup_installation/admin/monitoring/grafana.md` — 2 image(s)
- [ ] `docs/setup_installation/admin/monitoring/services-logs.md` — 2 image(s)
- [ ] `docs/setup_installation/admin/oauth2/configure-project-mapping.md` — 6 image(s)
- [ ] `docs/setup_installation/admin/oauth2/create-azure-client.md` — 10 image(s)
- [ ] `docs/setup_installation/admin/oauth2/create-client.md` — 3 image(s)
- [ ] `docs/setup_installation/admin/oauth2/create-okta-client.md` — 6 image(s)
- [ ] `docs/setup_installation/admin/operationLogs.md` — 2 image(s)
- [ ] `docs/setup_installation/admin/project.md` — 2 image(s)
- [ ] `docs/setup_installation/admin/roleChaining.md` — 2 image(s)
- [ ] `docs/setup_installation/admin/superset.md` — 6 image(s)
- [ ] `docs/setup_installation/admin/trino.md` — 4 image(s)
- [ ] `docs/setup_installation/admin/user.md` — 8 image(s)
- [ ] `docs/setup_installation/admin/variables.md` — 2 image(s)
- [ ] `docs/setup_installation/common/arrow_flight_duckdb.md` — 1 image(s)
- [ ] `docs/setup_installation/on_prem/external_kafka_cluster.md` — 1 image(s)

## (root)

- [ ] `docs/index.md` — 1 kit-static
