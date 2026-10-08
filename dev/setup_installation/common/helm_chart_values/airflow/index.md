# Airflow values { #helm-values-airflow }

Values under `airflow` configure Apache Airflow, which schedules and orchestrates Hopsworks jobs.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.2.0-alpha-1791461629` (Hopsworks `5.2.0`)._

Deployed according to the first of these values that is set: [`global._hopsworks.airflow.enabled`](global.md#helm.global._hopsworks.airflow.enabled), [`global._hopsworks.full_platform`](global.md#helm.global._hopsworks.full_platform).

## General { #helm-values-airflow-general }

??? example "Defaults as YAML"

    ```yaml
    airflow:
      appName: airflow
      bidirectional_mount: mounted
      cleanupOnUninstall:
        enabled: true
        ttlSecondsAfterFinished: null
      csi: {}
      debug: false
      dependencies:
        hopsworks:
          consulServiceName: glassfish
          consulServiceTag: hopsworks
          port: 8182
        mysql:
          consulServiceName: mysql
          ddlConsulServiceName: mysqlddl
          port: 3306
        namenode:
          consulServiceName: namenode
          port: 8020
      hopsfs_bin_url: null
      hopsworks:
        caBundlePath: /etc/airflow/ca/hopsworks-ca.crt
        enableApiKeyFallback: true
        hwJwtCacheTtlSeconds: 60
        internalClientCn: hopsworks-ee.hopsworks.svc
        manifestPath: /shared-volume/hopsfs/.airflow/manifest.json
        membershipCacheTtlSeconds: 60
        url: ''
      hopsworkslib: {}
      image:
        pullPolicy: IfNotPresent
        registry: docker.hops.works
      migrationBackOffLimit: 10
      migrationJobTtlSecondsAfterFinished: null
      orphanCleanup:
        schedule: 42 2 * * *
      reset_db_if_error: false
      serviceAccount:
        annotations: {}
      serviceAccountName: airflow
      tls: true
    ```

<div class="hops-values" markdown>

`airflow` <a class="headerlink" href="#helm.airflow" title="Permanent link">#</a> { #helm.airflow }
:   Type `object`, default `{"csi":{}}`.
    override airflow values

`airflow.appName` <a class="headerlink" href="#helm.airflow.appName" title="Permanent link">#</a> { #helm.airflow.appName }
:   Type `string`, default `"airflow"`.
    app name label

`airflow.bidirectional_mount` <a class="headerlink" href="#helm.airflow.bidirectional_mount" title="Permanent link">#</a> { #helm.airflow.bidirectional_mount }
:   Type `string`, default `"mounted"`.
    the name of bidirectional mount

`airflow.cleanupOnUninstall` <a class="headerlink" href="#helm.airflow.cleanupOnUninstall" title="Permanent link">#</a> { #helm.airflow.cleanupOnUninstall }
:   Type `object`, default `{"enabled":true,"ttlSecondsAfterFinished":null}`.
    post-delete cleanup of Airflow leftovers. The keys Secret (airflowApi.keysSecretName) is created by the keys-bootstrap pre-install hook via kubectl, so Helm/ArgoCD never track it; this deletes it by name on uninstall.

`airflow.cleanupOnUninstall.enabled` <a class="headerlink" href="#helm.airflow.cleanupOnUninstall.enabled" title="Permanent link">#</a> { #helm.airflow.cleanupOnUninstall.enabled }
:   Type `bool`, default `true`.
    enable the post-delete Airflow keys-Secret cleanup hook

`airflow.cleanupOnUninstall.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.airflow.cleanupOnUninstall.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.airflow.cleanupOnUninstall.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    ttlSecondsAfterFinished for the cleanup Job; null falls through to the global default

`airflow.debug` <a class="headerlink" href="#helm.airflow.debug" title="Permanent link">#</a> { #helm.airflow.debug }
:   Type `bool`, default `false`.
    enable or disable debug logging for hopsfs

`airflow.dependencies.hopsworks` <a class="headerlink" href="#helm.airflow.dependencies.hopsworks" title="Permanent link">#</a> { #helm.airflow.dependencies.hopsworks }
:   Type `object`, default `{"consulServiceName":"glassfish","consulServiceTag":"hopsworks","port":8182}`.
    hopsworks consul service

`airflow.dependencies.mysql` <a class="headerlink" href="#helm.airflow.dependencies.mysql" title="Permanent link">#</a> { #helm.airflow.dependencies.mysql }
:   Type `object`, default `{"consulServiceName":"mysql","ddlConsulServiceName":"mysqlddl","port":3306}`.
    mysql consul service

`airflow.dependencies.namenode` <a class="headerlink" href="#helm.airflow.dependencies.namenode" title="Permanent link">#</a> { #helm.airflow.dependencies.namenode }
:   Type `object`, default `{"consulServiceName":"namenode","port":8020}`.
    namenode consul service. This uses a headless ClusterIP underneath with `publishNotReadyAddresses: true`

`airflow.hopsfs_bin_url` <a class="headerlink" href="#helm.airflow.hopsfs_bin_url" title="Permanent link">#</a> { #helm.airflow.hopsfs_bin_url }
:   Type `string`, default `nil`.
    url to download a patched hopsfs mount for testing and development

`airflow.hopsworks` <a class="headerlink" href="#helm.airflow.hopsworks" title="Permanent link">#</a> { #helm.airflow.hopsworks }
:   Type `object`.
    Hopsworks-specific Airflow 3 configuration.

    ??? note "Default"

        ```yaml
        caBundlePath: /etc/airflow/ca/hopsworks-ca.crt
        enableApiKeyFallback: true
        hwJwtCacheTtlSeconds: 60
        internalClientCn: hopsworks-ee.hopsworks.svc
        manifestPath: /shared-volume/hopsfs/.airflow/manifest.json
        membershipCacheTtlSeconds: 60
        url: ''
        ```

`airflow.hopsworkslib` <a class="headerlink" href="#helm.airflow.hopsworkslib" title="Permanent link">#</a> { #helm.airflow.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`airflow.image` <a class="headerlink" href="#helm.airflow.image" title="Permanent link">#</a> { #helm.airflow.image }
:   Type `object`, default `{"pullPolicy":"IfNotPresent","registry":"docker.hops.works"}`.
    image configuration. The image tag is the .Chart.AppVersion 

`airflow.migrationBackOffLimit` <a class="headerlink" href="#helm.airflow.migrationBackOffLimit" title="Permanent link">#</a> { #helm.airflow.migrationBackOffLimit }
:   Type `int`, default `10`.
    backoffLimit for airflow migration job

`airflow.migrationJobTtlSecondsAfterFinished` <a class="headerlink" href="#helm.airflow.migrationJobTtlSecondsAfterFinished" title="Permanent link">#</a> { #helm.airflow.migrationJobTtlSecondsAfterFinished }
:   Type `string`, default `nil`.
    TTL in seconds for the migrate-airflow Job. Overrides global default.

`airflow.orphanCleanup` <a class="headerlink" href="#helm.airflow.orphanCleanup" title="Permanent link">#</a> { #helm.airflow.orphanCleanup }
:   Type `object`, default `{"schedule":"42 2 * * *"}`.
    periodic cleanup of orphaned Airflow rows. The metadata tables live in RonDB without enforced foreign keys (NDB cannot carry FKs on the blob/text tables), so a CronJob restores the dropped ON DELETE CASCADE semantics by deleting children whose parent `airflow db clean` removed. Gated by the airflow subchart's own enable condition in the umbrella `Chart.yaml` (`global._hopsworks.airflow.enabled,global._hopsworks.full_platform`): if airflow is disabled, this CronJob is not rendered.

`airflow.reset_db_if_error` <a class="headerlink" href="#helm.airflow.reset_db_if_error" title="Permanent link">#</a> { #helm.airflow.reset_db_if_error }
:   Type `bool`, default `false`.
    if true, will reset the database and create a new one in case of error. In Airflow 3 the db-reset job runs unconditionally before migrate; this key is retained for backwards compatibility but the v3 chart ignores it.

`airflow.serviceAccount.annotations` <a class="headerlink" href="#helm.airflow.serviceAccount.annotations" title="Permanent link">#</a> { #helm.airflow.serviceAccount.annotations }
:   Type `object`, default `{}`.
    service account annotations

`airflow.serviceAccountName` <a class="headerlink" href="#helm.airflow.serviceAccountName" title="Permanent link">#</a> { #helm.airflow.serviceAccountName }
:   Type `string`, default `"airflow"`.
    service account name

`airflow.tls` <a class="headerlink" href="#helm.airflow.tls" title="Permanent link">#</a> { #helm.airflow.tls }
:   Type `bool`, default `true`.
    enable or disable TLS

</div>

## airflowApi { #helm-values-airflow-airflowapi }

??? example "Defaults as YAML"

    ```yaml
    airflow:
      airflowApi:
        basePath: /hopsworks-api/airflow
        bundleRoot: /opt/airflow/hopsworks-bundle/dags
        corsAllowedOrigins: ''
        jwtAlgorithm: RS256
        jwtAudience: hopsworks-airflow
        jwtExpirationSeconds: 3600
        jwtPrivateKeyPath: /etc/airflow/keys/api-server-private.pem
        jwtPublicKeyPath: /etc/airflow/keys/api-server-public.pem
        keysSecretName: hopsworks-airflow-keys
        schedulerPrivateKeyPath: /etc/airflow/keys/scheduler-private.pem
        schedulerPublicKeyPath: /etc/airflow/keys/scheduler-public.pem
    ```

<div class="hops-values" markdown>

`airflow.airflowApi.basePath` <a class="headerlink" href="#helm.airflow.airflowApi.basePath" title="Permanent link">#</a> { #helm.airflow.airflowApi.basePath }
:   Type `string`, default `"/hopsworks-api/airflow"`.

`airflow.airflowApi.bundleRoot` <a class="headerlink" href="#helm.airflow.airflowApi.bundleRoot" title="Permanent link">#</a> { #helm.airflow.airflowApi.bundleRoot }
:   Type `string`, default `"/opt/airflow/hopsworks-bundle/dags"`.

`airflow.airflowApi.corsAllowedOrigins` <a class="headerlink" href="#helm.airflow.airflowApi.corsAllowedOrigins" title="Permanent link">#</a> { #helm.airflow.airflowApi.corsAllowedOrigins }
:   Type `string`, default `""`.

`airflow.airflowApi.jwtAlgorithm` <a class="headerlink" href="#helm.airflow.airflowApi.jwtAlgorithm" title="Permanent link">#</a> { #helm.airflow.airflowApi.jwtAlgorithm }
:   Type `string`, default `"RS256"`.

`airflow.airflowApi.jwtAudience` <a class="headerlink" href="#helm.airflow.airflowApi.jwtAudience" title="Permanent link">#</a> { #helm.airflow.airflowApi.jwtAudience }
:   Type `string`, default `"hopsworks-airflow"`.

`airflow.airflowApi.jwtExpirationSeconds` <a class="headerlink" href="#helm.airflow.airflowApi.jwtExpirationSeconds" title="Permanent link">#</a> { #helm.airflow.airflowApi.jwtExpirationSeconds }
:   Type `int`, default `3600`.

`airflow.airflowApi.jwtPrivateKeyPath` <a class="headerlink" href="#helm.airflow.airflowApi.jwtPrivateKeyPath" title="Permanent link">#</a> { #helm.airflow.airflowApi.jwtPrivateKeyPath }
:   Type `string`, default `"/etc/airflow/keys/api-server-private.pem"`.

`airflow.airflowApi.jwtPublicKeyPath` <a class="headerlink" href="#helm.airflow.airflowApi.jwtPublicKeyPath" title="Permanent link">#</a> { #helm.airflow.airflowApi.jwtPublicKeyPath }
:   Type `string`, default `"/etc/airflow/keys/api-server-public.pem"`.

`airflow.airflowApi.keysSecretName` <a class="headerlink" href="#helm.airflow.airflowApi.keysSecretName" title="Permanent link">#</a> { #helm.airflow.airflowApi.keysSecretName }
:   Type `string`, default `"hopsworks-airflow-keys"`.

`airflow.airflowApi.schedulerPrivateKeyPath` <a class="headerlink" href="#helm.airflow.airflowApi.schedulerPrivateKeyPath" title="Permanent link">#</a> { #helm.airflow.airflowApi.schedulerPrivateKeyPath }
:   Type `string`, default `"/etc/airflow/keys/scheduler-private.pem"`.

`airflow.airflowApi.schedulerPublicKeyPath` <a class="headerlink" href="#helm.airflow.airflowApi.schedulerPublicKeyPath" title="Permanent link">#</a> { #helm.airflow.airflowApi.schedulerPublicKeyPath }
:   Type `string`, default `"/etc/airflow/keys/scheduler-public.pem"`.

</div>

## common { #helm-values-airflow-common }

??? example "Defaults as YAML"

    ```yaml
    airflow:
      common:
        celery:
          broker_url: rdis://:6379/0
          celery_app_name: airflow.executors.celery_executor
          default_queue: default
          flower_port: 5555
          flower_url_prefix: http://localhost/hopsworks-api/flower
          worker_concurrency: 8
          worker_log_server_port: 8793
        core_config:
          airflow_home: /airflow
          base_log_folder: /airflow/logs
          dag_concurrency: 16
          dagbag_import_timeout: 60
          dags_are_paused_at_creation: true
          dags_folder: /airflow/dags
          default_timezone: utc
          donot_pickle: false
          executor: LocalExecutor
          fernet_key: G3jB5--jCQpRYp7hwUtpfQ_S8zLRbRMwX8tr3dehnNU=
          hostname_callable: airflow.utils.net.get_host_ip_address
          load_examples: false
          logging_config_class: log_config.LOGGING_CONFIG
          max_active_runs_per_dag: 16
          non_pooled_task_slot_count: 128
          parallelism: 32
          plugins_folder: /airflow/plugins
          sql_alchemy_max_overflow: 30
          sql_alchemy_pool_pre_ping: true
          sql_alchemy_pool_recycle: 3600
          sql_alchemy_pool_size: 10
        group: airflow
        namenode_cluster_ip_name: namenode-cluster-ip
        smtp:
          smtp_host: localhost
          smtp_mail_from: admin@kth.se
          smtp_password: admin
          smtp_port: 25
          smtp_ssl: false
          smtp_starttls: true
          smtp_user: admin@kth.se
        user: airflow
    ```

<div class="hops-values" markdown>

`airflow.common.celery.broker_url` <a class="headerlink" href="#helm.airflow.common.celery.broker_url" title="Permanent link">#</a> { #helm.airflow.common.celery.broker_url }
:   Type `string`, default `"rdis://:6379/0"`.

`airflow.common.celery.celery_app_name` <a class="headerlink" href="#helm.airflow.common.celery.celery_app_name" title="Permanent link">#</a> { #helm.airflow.common.celery.celery_app_name }
:   Type `string`, default `"airflow.executors.celery_executor"`.

`airflow.common.celery.default_queue` <a class="headerlink" href="#helm.airflow.common.celery.default_queue" title="Permanent link">#</a> { #helm.airflow.common.celery.default_queue }
:   Type `string`, default `"default"`.

`airflow.common.celery.flower_port` <a class="headerlink" href="#helm.airflow.common.celery.flower_port" title="Permanent link">#</a> { #helm.airflow.common.celery.flower_port }
:   Type `int`, default `5555`.

`airflow.common.celery.flower_url_prefix` <a class="headerlink" href="#helm.airflow.common.celery.flower_url_prefix" title="Permanent link">#</a> { #helm.airflow.common.celery.flower_url_prefix }
:   Type `string`, default `"http://localhost/hopsworks-api/flower"`.

`airflow.common.celery.worker_concurrency` <a class="headerlink" href="#helm.airflow.common.celery.worker_concurrency" title="Permanent link">#</a> { #helm.airflow.common.celery.worker_concurrency }
:   Type `int`, default `8`.

`airflow.common.celery.worker_log_server_port` <a class="headerlink" href="#helm.airflow.common.celery.worker_log_server_port" title="Permanent link">#</a> { #helm.airflow.common.celery.worker_log_server_port }
:   Type `int`, default `8793`.

`airflow.common.core_config.airflow_home` <a class="headerlink" href="#helm.airflow.common.core_config.airflow_home" title="Permanent link">#</a> { #helm.airflow.common.core_config.airflow_home }
:   Type `string`, default `"/airflow"`.

`airflow.common.core_config.base_log_folder` <a class="headerlink" href="#helm.airflow.common.core_config.base_log_folder" title="Permanent link">#</a> { #helm.airflow.common.core_config.base_log_folder }
:   Type `string`, default `"/airflow/logs"`.

`airflow.common.core_config.dag_concurrency` <a class="headerlink" href="#helm.airflow.common.core_config.dag_concurrency" title="Permanent link">#</a> { #helm.airflow.common.core_config.dag_concurrency }
:   Type `int`, default `16`.

`airflow.common.core_config.dagbag_import_timeout` <a class="headerlink" href="#helm.airflow.common.core_config.dagbag_import_timeout" title="Permanent link">#</a> { #helm.airflow.common.core_config.dagbag_import_timeout }
:   Type `int`, default `60`.

`airflow.common.core_config.dags_are_paused_at_creation` <a class="headerlink" href="#helm.airflow.common.core_config.dags_are_paused_at_creation" title="Permanent link">#</a> { #helm.airflow.common.core_config.dags_are_paused_at_creation }
:   Type `bool`, default `true`.

`airflow.common.core_config.dags_folder` <a class="headerlink" href="#helm.airflow.common.core_config.dags_folder" title="Permanent link">#</a> { #helm.airflow.common.core_config.dags_folder }
:   Type `string`, default `"/airflow/dags"`.

`airflow.common.core_config.default_timezone` <a class="headerlink" href="#helm.airflow.common.core_config.default_timezone" title="Permanent link">#</a> { #helm.airflow.common.core_config.default_timezone }
:   Type `string`, default `"utc"`.

`airflow.common.core_config.donot_pickle` <a class="headerlink" href="#helm.airflow.common.core_config.donot_pickle" title="Permanent link">#</a> { #helm.airflow.common.core_config.donot_pickle }
:   Type `bool`, default `false`.

`airflow.common.core_config.executor` <a class="headerlink" href="#helm.airflow.common.core_config.executor" title="Permanent link">#</a> { #helm.airflow.common.core_config.executor }
:   Type `string`, default `"LocalExecutor"`.

`airflow.common.core_config.fernet_key` <a class="headerlink" href="#helm.airflow.common.core_config.fernet_key" title="Permanent link">#</a> { #helm.airflow.common.core_config.fernet_key }
:   Type `string`, default `"G3jB5--jCQpRYp7hwUtpfQ_S8zLRbRMwX8tr3dehnNU="`.

`airflow.common.core_config.hostname_callable` <a class="headerlink" href="#helm.airflow.common.core_config.hostname_callable" title="Permanent link">#</a> { #helm.airflow.common.core_config.hostname_callable }
:   Type `string`, default `"airflow.utils.net.get_host_ip_address"`.

`airflow.common.core_config.load_examples` <a class="headerlink" href="#helm.airflow.common.core_config.load_examples" title="Permanent link">#</a> { #helm.airflow.common.core_config.load_examples }
:   Type `bool`, default `false`.

`airflow.common.core_config.logging_config_class` <a class="headerlink" href="#helm.airflow.common.core_config.logging_config_class" title="Permanent link">#</a> { #helm.airflow.common.core_config.logging_config_class }
:   Type `string`, default `"log_config.LOGGING_CONFIG"`.

`airflow.common.core_config.max_active_runs_per_dag` <a class="headerlink" href="#helm.airflow.common.core_config.max_active_runs_per_dag" title="Permanent link">#</a> { #helm.airflow.common.core_config.max_active_runs_per_dag }
:   Type `int`, default `16`.

`airflow.common.core_config.non_pooled_task_slot_count` <a class="headerlink" href="#helm.airflow.common.core_config.non_pooled_task_slot_count" title="Permanent link">#</a> { #helm.airflow.common.core_config.non_pooled_task_slot_count }
:   Type `int`, default `128`.

`airflow.common.core_config.parallelism` <a class="headerlink" href="#helm.airflow.common.core_config.parallelism" title="Permanent link">#</a> { #helm.airflow.common.core_config.parallelism }
:   Type `int`, default `32`.

`airflow.common.core_config.plugins_folder` <a class="headerlink" href="#helm.airflow.common.core_config.plugins_folder" title="Permanent link">#</a> { #helm.airflow.common.core_config.plugins_folder }
:   Type `string`, default `"/airflow/plugins"`.

`airflow.common.core_config.sql_alchemy_max_overflow` <a class="headerlink" href="#helm.airflow.common.core_config.sql_alchemy_max_overflow" title="Permanent link">#</a> { #helm.airflow.common.core_config.sql_alchemy_max_overflow }
:   Type `int`, default `30`.
    We set it high, not unlimited to account for memory leaks

`airflow.common.core_config.sql_alchemy_pool_pre_ping` <a class="headerlink" href="#helm.airflow.common.core_config.sql_alchemy_pool_pre_ping" title="Permanent link">#</a> { #helm.airflow.common.core_config.sql_alchemy_pool_pre_ping }
:   Type `bool`, default `true`.

`airflow.common.core_config.sql_alchemy_pool_recycle` <a class="headerlink" href="#helm.airflow.common.core_config.sql_alchemy_pool_recycle" title="Permanent link">#</a> { #helm.airflow.common.core_config.sql_alchemy_pool_recycle }
:   Type `int`, default `3600`.

`airflow.common.core_config.sql_alchemy_pool_size` <a class="headerlink" href="#helm.airflow.common.core_config.sql_alchemy_pool_size" title="Permanent link">#</a> { #helm.airflow.common.core_config.sql_alchemy_pool_size }
:   Type `int`, default `10`.

`airflow.common.group` <a class="headerlink" href="#helm.airflow.common.group" title="Permanent link">#</a> { #helm.airflow.common.group }
:   Type `string`, default `"airflow"`.

`airflow.common.namenode_cluster_ip_name` <a class="headerlink" href="#helm.airflow.common.namenode_cluster_ip_name" title="Permanent link">#</a> { #helm.airflow.common.namenode_cluster_ip_name }
:   Type `string`, default `"namenode-cluster-ip"`.

`airflow.common.smtp.smtp_host` <a class="headerlink" href="#helm.airflow.common.smtp.smtp_host" title="Permanent link">#</a> { #helm.airflow.common.smtp.smtp_host }
:   Type `string`, default `"localhost"`.

`airflow.common.smtp.smtp_mail_from` <a class="headerlink" href="#helm.airflow.common.smtp.smtp_mail_from" title="Permanent link">#</a> { #helm.airflow.common.smtp.smtp_mail_from }
:   Type `string`, default `"admin@kth.se"`.

`airflow.common.smtp.smtp_password` <a class="headerlink" href="#helm.airflow.common.smtp.smtp_password" title="Permanent link">#</a> { #helm.airflow.common.smtp.smtp_password }
:   Type `string`, default `"admin"`.

`airflow.common.smtp.smtp_port` <a class="headerlink" href="#helm.airflow.common.smtp.smtp_port" title="Permanent link">#</a> { #helm.airflow.common.smtp.smtp_port }
:   Type `int`, default `25`.

`airflow.common.smtp.smtp_ssl` <a class="headerlink" href="#helm.airflow.common.smtp.smtp_ssl" title="Permanent link">#</a> { #helm.airflow.common.smtp.smtp_ssl }
:   Type `bool`, default `false`.

`airflow.common.smtp.smtp_starttls` <a class="headerlink" href="#helm.airflow.common.smtp.smtp_starttls" title="Permanent link">#</a> { #helm.airflow.common.smtp.smtp_starttls }
:   Type `bool`, default `true`.

`airflow.common.smtp.smtp_user` <a class="headerlink" href="#helm.airflow.common.smtp.smtp_user" title="Permanent link">#</a> { #helm.airflow.common.smtp.smtp_user }
:   Type `string`, default `"admin@kth.se"`.

`airflow.common.user` <a class="headerlink" href="#helm.airflow.common.user" title="Permanent link">#</a> { #helm.airflow.common.user }
:   Type `string`, default `"airflow"`.

</div>

## csi { #helm-values-airflow-csi }

??? example "Defaults as YAML"

    ```yaml
    airflow:
      csi:
        clientCertificateSecretKey: ''
        clientKeySecretKey: ''
        defaultPermissions: true
        fallbackGroup: airflow
        fallbackUser: airflow
        imageTag: ''
        rootCABundleSecretKey: ''
        secretName: ''
        sidecarGid: 1508
        sidecarResources:
          limits:
            cpu: '1'
            memory: 1024Mi
          requests:
            cpu: 200m
            memory: 256Mi
        sidecarUid: 1512
    ```

<div class="hops-values" markdown>

`airflow.csi` <a class="headerlink" href="#helm.airflow.csi" title="Permanent link">#</a> { #helm.airflow.csi }
:   Type `object`.
    CSI settings for the unprivileged HopsFS FUSE sidecar. When `tls=true`, the default secret selectors target the Airflow CSI-specific HopsworksCert secret.

    ??? note "Default"

        ```yaml
        clientCertificateSecretKey: ''
        clientKeySecretKey: ''
        defaultPermissions: true
        fallbackGroup: airflow
        fallbackUser: airflow
        imageTag: ''
        rootCABundleSecretKey: ''
        secretName: ''
        sidecarGid: 1508
        sidecarResources:
          limits:
            cpu: '1'
            memory: 1024Mi
          requests:
            cpu: 200m
            memory: 256Mi
        sidecarUid: 1512
        ```

`airflow.csi.clientCertificateSecretKey` <a class="headerlink" href="#helm.airflow.csi.clientCertificateSecretKey" title="Permanent link">#</a> { #helm.airflow.csi.clientCertificateSecretKey }
:   Type `string`, default `""`.
    override the client certificate bundle file name inside the mounted TLS secret

`airflow.csi.clientKeySecretKey` <a class="headerlink" href="#helm.airflow.csi.clientKeySecretKey" title="Permanent link">#</a> { #helm.airflow.csi.clientKeySecretKey }
:   Type `string`, default `""`.
    override the client key file name inside the mounted TLS secret

`airflow.csi.defaultPermissions` <a class="headerlink" href="#helm.airflow.csi.defaultPermissions" title="Permanent link">#</a> { #helm.airflow.csi.defaultPermissions }
:   Type `bool`, default `true`.
    enable the kernel-side default_permissions check on the fuse mount; set false on OpenShift, where workload uids are arbitrary and can never match the owners hopsfs-mount reports (HDFS permissions are still enforced server-side)

`airflow.csi.imageTag` <a class="headerlink" href="#helm.airflow.csi.imageTag" title="Permanent link">#</a> { #helm.airflow.csi.imageTag }
:   Type `string`, default `""`.
    override the tag of the hopsfs-csi image run as the unprivileged FUSE sidecar. Empty (the default) takes global._hopsworks.csi.image.tag, the one place the hopsfs-csi image is named, so the sidecar and the node plugin it fetches the mount from cannot drift; set only to test a sidecar build against a deployed plugin

`airflow.csi.rootCABundleSecretKey` <a class="headerlink" href="#helm.airflow.csi.rootCABundleSecretKey" title="Permanent link">#</a> { #helm.airflow.csi.rootCABundleSecretKey }
:   Type `string`, default `""`.
    override the root CA bundle file name inside the mounted TLS secret

`airflow.csi.secretName` <a class="headerlink" href="#helm.airflow.csi.secretName" title="Permanent link">#</a> { #helm.airflow.csi.secretName }
:   Type `string`, default `""`.
    override the Secret holding the PEM TLS material mounted into the FUSE sidecar (defaults to the csi HopsworksCert secret)

`airflow.csi.sidecarGid` <a class="headerlink" href="#helm.airflow.csi.sidecarGid" title="Permanent link">#</a> { #helm.airflow.csi.sidecarGid }
:   Type `int`, default `1508`.
    gid recorded on the fuse mount; matches the airflow group precreated in the hopsfs-csi image

`airflow.csi.sidecarResources` <a class="headerlink" href="#helm.airflow.csi.sidecarResources" title="Permanent link">#</a> { #helm.airflow.csi.sidecarResources }
:   Type `object`.
    resources for the unprivileged FUSE sidecar. All four slots are set on purpose: a namespace LimitRange fills any missing one with its own default, which for a limit-less request is rejected at admission when the default falls below the request (see HWORKS-3086).

    ??? note "Default"

        ```yaml
        limits:
          cpu: '1'
          memory: 1024Mi
        requests:
          cpu: 200m
          memory: 256Mi
        ```

`airflow.csi.sidecarUid` <a class="headerlink" href="#helm.airflow.csi.sidecarUid" title="Permanent link">#</a> { #helm.airflow.csi.sidecarUid }
:   Type `int`, default `1512`.
    uid recorded on the fuse mount and used to run the sidecar; matches the airflow user precreated in the hopsfs-csi image

</div>

## dagProcessor { #helm-values-airflow-dagprocessor }

??? example "Defaults as YAML"

    ```yaml
    airflow:
      dagProcessor:
        deployment:
          replicas: 1
        name: airflow-dag-processor
        nodeSelector: {}
        probe:
          failureThreshold: 20
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 10
        refreshIntervalSeconds: 5
        resources:
          limits:
            memory: 2000Mi
          requests:
            cpu: 200m
            memory: 500Mi
        securityContext:
          runAsGroup: 1508
          runAsNonRoot: true
          runAsUser: 1512
        tolerations: []
    ```

<div class="hops-values" markdown>

`airflow.dagProcessor.deployment.replicas` <a class="headerlink" href="#helm.airflow.dagProcessor.deployment.replicas" title="Permanent link">#</a> { #helm.airflow.dagProcessor.deployment.replicas }
:   Type `int`, default `1`.

`airflow.dagProcessor.name` <a class="headerlink" href="#helm.airflow.dagProcessor.name" title="Permanent link">#</a> { #helm.airflow.dagProcessor.name }
:   Type `string`, default `"airflow-dag-processor"`.

`airflow.dagProcessor.nodeSelector` <a class="headerlink" href="#helm.airflow.dagProcessor.nodeSelector" title="Permanent link">#</a> { #helm.airflow.dagProcessor.nodeSelector }
:   Type `object`, default `{}`.

`airflow.dagProcessor.probe.failureThreshold` <a class="headerlink" href="#helm.airflow.dagProcessor.probe.failureThreshold" title="Permanent link">#</a> { #helm.airflow.dagProcessor.probe.failureThreshold }
:   Type `int`, default `20`.

`airflow.dagProcessor.probe.initialDelaySeconds` <a class="headerlink" href="#helm.airflow.dagProcessor.probe.initialDelaySeconds" title="Permanent link">#</a> { #helm.airflow.dagProcessor.probe.initialDelaySeconds }
:   Type `int`, default `30`.

`airflow.dagProcessor.probe.periodSeconds` <a class="headerlink" href="#helm.airflow.dagProcessor.probe.periodSeconds" title="Permanent link">#</a> { #helm.airflow.dagProcessor.probe.periodSeconds }
:   Type `int`, default `10`.

`airflow.dagProcessor.probe.timeoutSeconds` <a class="headerlink" href="#helm.airflow.dagProcessor.probe.timeoutSeconds" title="Permanent link">#</a> { #helm.airflow.dagProcessor.probe.timeoutSeconds }
:   Type `int`, default `10`.

`airflow.dagProcessor.refreshIntervalSeconds` <a class="headerlink" href="#helm.airflow.dagProcessor.refreshIntervalSeconds" title="Permanent link">#</a> { #helm.airflow.dagProcessor.refreshIntervalSeconds }
:   Type `int`, default `5`.

`airflow.dagProcessor.resources.limits.memory` <a class="headerlink" href="#helm.airflow.dagProcessor.resources.limits.memory" title="Permanent link">#</a> { #helm.airflow.dagProcessor.resources.limits.memory }
:   Type `string`, default `"2000Mi"`.

`airflow.dagProcessor.resources.requests.cpu` <a class="headerlink" href="#helm.airflow.dagProcessor.resources.requests.cpu" title="Permanent link">#</a> { #helm.airflow.dagProcessor.resources.requests.cpu }
:   Type `string`, default `"200m"`.

`airflow.dagProcessor.resources.requests.memory` <a class="headerlink" href="#helm.airflow.dagProcessor.resources.requests.memory" title="Permanent link">#</a> { #helm.airflow.dagProcessor.resources.requests.memory }
:   Type `string`, default `"500Mi"`.

`airflow.dagProcessor.securityContext.runAsGroup` <a class="headerlink" href="#helm.airflow.dagProcessor.securityContext.runAsGroup" title="Permanent link">#</a> { #helm.airflow.dagProcessor.securityContext.runAsGroup }
:   Type `int`, default `1508`.

`airflow.dagProcessor.securityContext.runAsNonRoot` <a class="headerlink" href="#helm.airflow.dagProcessor.securityContext.runAsNonRoot" title="Permanent link">#</a> { #helm.airflow.dagProcessor.securityContext.runAsNonRoot }
:   Type `bool`, default `true`.

`airflow.dagProcessor.securityContext.runAsUser` <a class="headerlink" href="#helm.airflow.dagProcessor.securityContext.runAsUser" title="Permanent link">#</a> { #helm.airflow.dagProcessor.securityContext.runAsUser }
:   Type `int`, default `1512`.

`airflow.dagProcessor.tolerations` <a class="headerlink" href="#helm.airflow.dagProcessor.tolerations" title="Permanent link">#</a> { #helm.airflow.dagProcessor.tolerations }
:   Type `list`, default `[]`.

</div>

## scheduler { #helm-values-airflow-scheduler }

??? example "Defaults as YAML"

    ```yaml
    airflow:
      scheduler:
        config:
          dag_dir_list_interval: 40
          job_heartbeat_sec: 5
          max_threads: 2
          min_file_process_interval: 10
          print_stats_interval: 600
          scheduler_zombie_task_threshold: 300
        deployment:
          replicas: 1
        is_tls: false
        name: airflow-scheduler
        nodeSelector: {}
        podDisruptionBudget:
          enabled: true
          minAvailable: 1
        probe:
          failureThreshold: 20
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 10
        probeCheckWebserver: true
        probeCommand: set -e && pgrep -f "airflow scheduler"
        resources:
          limits:
            memory: 2000Mi
          requests:
            cpu: '1'
            memory: 1000Mi
        securityContext:
          runAsGroup: 1508
          runAsNonRoot: true
          runAsUser: 1512
        service:
          annotations:
            consul.hashicorp.com/service-name: airflow
            consul.hashicorp.com/service-tags: scheduler
        tolerations: []
        topologySpreadConstraint: {}
    ```

<div class="hops-values" markdown>

`airflow.scheduler.config.dag_dir_list_interval` <a class="headerlink" href="#helm.airflow.scheduler.config.dag_dir_list_interval" title="Permanent link">#</a> { #helm.airflow.scheduler.config.dag_dir_list_interval }
:   Type `int`, default `40`.

`airflow.scheduler.config.job_heartbeat_sec` <a class="headerlink" href="#helm.airflow.scheduler.config.job_heartbeat_sec" title="Permanent link">#</a> { #helm.airflow.scheduler.config.job_heartbeat_sec }
:   Type `int`, default `5`.

`airflow.scheduler.config.max_threads` <a class="headerlink" href="#helm.airflow.scheduler.config.max_threads" title="Permanent link">#</a> { #helm.airflow.scheduler.config.max_threads }
:   Type `int`, default `2`.

`airflow.scheduler.config.min_file_process_interval` <a class="headerlink" href="#helm.airflow.scheduler.config.min_file_process_interval" title="Permanent link">#</a> { #helm.airflow.scheduler.config.min_file_process_interval }
:   Type `int`, default `10`.

`airflow.scheduler.config.print_stats_interval` <a class="headerlink" href="#helm.airflow.scheduler.config.print_stats_interval" title="Permanent link">#</a> { #helm.airflow.scheduler.config.print_stats_interval }
:   Type `int`, default `600`.

`airflow.scheduler.config.scheduler_zombie_task_threshold` <a class="headerlink" href="#helm.airflow.scheduler.config.scheduler_zombie_task_threshold" title="Permanent link">#</a> { #helm.airflow.scheduler.config.scheduler_zombie_task_threshold }
:   Type `int`, default `300`.

`airflow.scheduler.deployment.replicas` <a class="headerlink" href="#helm.airflow.scheduler.deployment.replicas" title="Permanent link">#</a> { #helm.airflow.scheduler.deployment.replicas }
:   Type `int`, default `1`.

`airflow.scheduler.is_tls` <a class="headerlink" href="#helm.airflow.scheduler.is_tls" title="Permanent link">#</a> { #helm.airflow.scheduler.is_tls }
:   Type `bool`, default `false`.

`airflow.scheduler.name` <a class="headerlink" href="#helm.airflow.scheduler.name" title="Permanent link">#</a> { #helm.airflow.scheduler.name }
:   Type `string`, default `"airflow-scheduler"`.

`airflow.scheduler.nodeSelector` <a class="headerlink" href="#helm.airflow.scheduler.nodeSelector" title="Permanent link">#</a> { #helm.airflow.scheduler.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

`airflow.scheduler.podDisruptionBudget.enabled` <a class="headerlink" href="#helm.airflow.scheduler.podDisruptionBudget.enabled" title="Permanent link">#</a> { #helm.airflow.scheduler.podDisruptionBudget.enabled }
:   Type `bool`, default `true`.

`airflow.scheduler.podDisruptionBudget.minAvailable` <a class="headerlink" href="#helm.airflow.scheduler.podDisruptionBudget.minAvailable" title="Permanent link">#</a> { #helm.airflow.scheduler.podDisruptionBudget.minAvailable }
:   Type `int`, default `1`.

`airflow.scheduler.probe.failureThreshold` <a class="headerlink" href="#helm.airflow.scheduler.probe.failureThreshold" title="Permanent link">#</a> { #helm.airflow.scheduler.probe.failureThreshold }
:   Type `int`, default `20`.

`airflow.scheduler.probe.initialDelaySeconds` <a class="headerlink" href="#helm.airflow.scheduler.probe.initialDelaySeconds" title="Permanent link">#</a> { #helm.airflow.scheduler.probe.initialDelaySeconds }
:   Type `int`, default `30`.

`airflow.scheduler.probe.periodSeconds` <a class="headerlink" href="#helm.airflow.scheduler.probe.periodSeconds" title="Permanent link">#</a> { #helm.airflow.scheduler.probe.periodSeconds }
:   Type `int`, default `10`.

`airflow.scheduler.probe.timeoutSeconds` <a class="headerlink" href="#helm.airflow.scheduler.probe.timeoutSeconds" title="Permanent link">#</a> { #helm.airflow.scheduler.probe.timeoutSeconds }
:   Type `int`, default `10`.

`airflow.scheduler.probeCheckWebserver` <a class="headerlink" href="#helm.airflow.scheduler.probeCheckWebserver" title="Permanent link">#</a> { #helm.airflow.scheduler.probeCheckWebserver }
:   Type `bool`, default `true`.

`airflow.scheduler.probeCommand` <a class="headerlink" href="#helm.airflow.scheduler.probeCommand" title="Permanent link">#</a> { #helm.airflow.scheduler.probeCommand }
:   Type `string`, default `"set -e && pgrep -f \"airflow scheduler\""`.
    The probe here will be concatenated with sleeping for the heartbeat time and then trying to reach the webserver. If the webserver is not reachable the scheduler should be restarted  <https://hopsworks.atlassian.net/browse/HWORKS-1915> The scheduler goes to a non consistent state, then the health check of the webserver returns scheduler non-healthy and it fails

`airflow.scheduler.resources.limits` <a class="headerlink" href="#helm.airflow.scheduler.resources.limits" title="Permanent link">#</a> { #helm.airflow.scheduler.resources.limits }
:   Type `object`, default `{"memory":"2000Mi"}`.
    resources limits configuration

`airflow.scheduler.resources.requests` <a class="headerlink" href="#helm.airflow.scheduler.resources.requests" title="Permanent link">#</a> { #helm.airflow.scheduler.resources.requests }
:   Type `object`, default `{"cpu":"1","memory":"1000Mi"}`.
    resources requests configuration

`airflow.scheduler.securityContext.runAsGroup` <a class="headerlink" href="#helm.airflow.scheduler.securityContext.runAsGroup" title="Permanent link">#</a> { #helm.airflow.scheduler.securityContext.runAsGroup }
:   Type `int`, default `1508`.

`airflow.scheduler.securityContext.runAsNonRoot` <a class="headerlink" href="#helm.airflow.scheduler.securityContext.runAsNonRoot" title="Permanent link">#</a> { #helm.airflow.scheduler.securityContext.runAsNonRoot }
:   Type `bool`, default `true`.

`airflow.scheduler.securityContext.runAsUser` <a class="headerlink" href="#helm.airflow.scheduler.securityContext.runAsUser" title="Permanent link">#</a> { #helm.airflow.scheduler.securityContext.runAsUser }
:   Type `int`, default `1512`.

`airflow.scheduler.service.annotations."consul.hashicorp.com/service-name"` <a class="headerlink" href="#helm.airflow.scheduler.service.annotations.consul.hashicorp.com-service-name" title="Permanent link">#</a> { #helm.airflow.scheduler.service.annotations.consul.hashicorp.com-service-name }
:   Type `string`, default `"airflow"`.

`airflow.scheduler.service.annotations."consul.hashicorp.com/service-tags"` <a class="headerlink" href="#helm.airflow.scheduler.service.annotations.consul.hashicorp.com-service-tags" title="Permanent link">#</a> { #helm.airflow.scheduler.service.annotations.consul.hashicorp.com-service-tags }
:   Type `string`, default `"scheduler"`.

`airflow.scheduler.tolerations` <a class="headerlink" href="#helm.airflow.scheduler.tolerations" title="Permanent link">#</a> { #helm.airflow.scheduler.tolerations }
:   Type `list`, default `[]`.

`airflow.scheduler.topologySpreadConstraint` <a class="headerlink" href="#helm.airflow.scheduler.topologySpreadConstraint" title="Permanent link">#</a> { #helm.airflow.scheduler.topologySpreadConstraint }
:   Type `object`, default `{}`.
    The default topology spread constraint. If not defined the global topology spread constraint would be used instead.

</div>

## webserver { #helm-values-airflow-webserver }

??? example "Defaults as YAML"

    ```yaml
    airflow:
      webserver:
        config:
          authenticate: true
          expose_config: true
          rbac: true
          secret_key: temporary_key
          web_server_host: 0.0.0.0
          web_server_port: 12358
          web_server_worker_timeout: 120
          worker_class: sync
          workers: 2
        configHelm:
          base_path: /hopsworks-api/airflow
        deployment:
          replicas: 1
        forwardedAllowIps: 10.0.0.0/8,172.16.0.0/12,192.168.0.0/16
        heartbeat: 30
        is_tls: false
        name: airflow-webserver
        nodeSelector: {}
        podDisruptionBudget:
          enabled: true
          minAvailable: 1
        probe:
          failureThreshold: 10
          initialDelaySeconds: 60
          periodSeconds: 5
          timeoutSeconds: 10
        resources:
          limits:
            memory: 2000Mi
          requests:
            cpu: 100m
            memory: 1000Mi
        securityContext:
          runAsGroup: 1508
          runAsUser: 1512
        service:
          annotations:
            consul.hashicorp.com/service-name: airflow
            consul.hashicorp.com/service-port: server
            consul.hashicorp.com/service-tags: ui
        tolerations: []
        topologySpreadConstraint: {}
    ```

<div class="hops-values" markdown>

`airflow.webserver.config.authenticate` <a class="headerlink" href="#helm.airflow.webserver.config.authenticate" title="Permanent link">#</a> { #helm.airflow.webserver.config.authenticate }
:   Type `bool`, default `true`.

`airflow.webserver.config.expose_config` <a class="headerlink" href="#helm.airflow.webserver.config.expose_config" title="Permanent link">#</a> { #helm.airflow.webserver.config.expose_config }
:   Type `bool`, default `true`.

`airflow.webserver.config.rbac` <a class="headerlink" href="#helm.airflow.webserver.config.rbac" title="Permanent link">#</a> { #helm.airflow.webserver.config.rbac }
:   Type `bool`, default `true`.

`airflow.webserver.config.secret_key` <a class="headerlink" href="#helm.airflow.webserver.config.secret_key" title="Permanent link">#</a> { #helm.airflow.webserver.config.secret_key }
:   Type `string`, default `"temporary_key"`.

`airflow.webserver.config.web_server_host` <a class="headerlink" href="#helm.airflow.webserver.config.web_server_host" title="Permanent link">#</a> { #helm.airflow.webserver.config.web_server_host }
:   Type `string`, default `"0.0.0.0"`.

`airflow.webserver.config.web_server_port` <a class="headerlink" href="#helm.airflow.webserver.config.web_server_port" title="Permanent link">#</a> { #helm.airflow.webserver.config.web_server_port }
:   Type `int`, default `12358`.

`airflow.webserver.config.web_server_worker_timeout` <a class="headerlink" href="#helm.airflow.webserver.config.web_server_worker_timeout" title="Permanent link">#</a> { #helm.airflow.webserver.config.web_server_worker_timeout }
:   Type `int`, default `120`.

`airflow.webserver.config.worker_class` <a class="headerlink" href="#helm.airflow.webserver.config.worker_class" title="Permanent link">#</a> { #helm.airflow.webserver.config.worker_class }
:   Type `string`, default `"sync"`.

`airflow.webserver.config.workers` <a class="headerlink" href="#helm.airflow.webserver.config.workers" title="Permanent link">#</a> { #helm.airflow.webserver.config.workers }
:   Type `int`, default `2`.

`airflow.webserver.configHelm.base_path` <a class="headerlink" href="#helm.airflow.webserver.configHelm.base_path" title="Permanent link">#</a> { #helm.airflow.webserver.configHelm.base_path }
:   Type `string`, default `"/hopsworks-api/airflow"`.

`airflow.webserver.deployment.replicas` <a class="headerlink" href="#helm.airflow.webserver.deployment.replicas" title="Permanent link">#</a> { #helm.airflow.webserver.deployment.replicas }
:   Type `int`, default `1`.

`airflow.webserver.forwardedAllowIps` <a class="headerlink" href="#helm.airflow.webserver.forwardedAllowIps" title="Permanent link">#</a> { #helm.airflow.webserver.forwardedAllowIps }
:   Type `string`, default `"10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"`.

`airflow.webserver.heartbeat` <a class="headerlink" href="#helm.airflow.webserver.heartbeat" title="Permanent link">#</a> { #helm.airflow.webserver.heartbeat }
:   Type `int`, default `30`.

`airflow.webserver.is_tls` <a class="headerlink" href="#helm.airflow.webserver.is_tls" title="Permanent link">#</a> { #helm.airflow.webserver.is_tls }
:   Type `bool`, default `false`.

`airflow.webserver.name` <a class="headerlink" href="#helm.airflow.webserver.name" title="Permanent link">#</a> { #helm.airflow.webserver.name }
:   Type `string`, default `"airflow-webserver"`.

`airflow.webserver.nodeSelector` <a class="headerlink" href="#helm.airflow.webserver.nodeSelector" title="Permanent link">#</a> { #helm.airflow.webserver.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

`airflow.webserver.podDisruptionBudget.enabled` <a class="headerlink" href="#helm.airflow.webserver.podDisruptionBudget.enabled" title="Permanent link">#</a> { #helm.airflow.webserver.podDisruptionBudget.enabled }
:   Type `bool`, default `true`.

`airflow.webserver.podDisruptionBudget.minAvailable` <a class="headerlink" href="#helm.airflow.webserver.podDisruptionBudget.minAvailable" title="Permanent link">#</a> { #helm.airflow.webserver.podDisruptionBudget.minAvailable }
:   Type `int`, default `1`.

`airflow.webserver.probe.failureThreshold` <a class="headerlink" href="#helm.airflow.webserver.probe.failureThreshold" title="Permanent link">#</a> { #helm.airflow.webserver.probe.failureThreshold }
:   Type `int`, default `10`.

`airflow.webserver.probe.initialDelaySeconds` <a class="headerlink" href="#helm.airflow.webserver.probe.initialDelaySeconds" title="Permanent link">#</a> { #helm.airflow.webserver.probe.initialDelaySeconds }
:   Type `int`, default `60`.

`airflow.webserver.probe.periodSeconds` <a class="headerlink" href="#helm.airflow.webserver.probe.periodSeconds" title="Permanent link">#</a> { #helm.airflow.webserver.probe.periodSeconds }
:   Type `int`, default `5`.

`airflow.webserver.probe.timeoutSeconds` <a class="headerlink" href="#helm.airflow.webserver.probe.timeoutSeconds" title="Permanent link">#</a> { #helm.airflow.webserver.probe.timeoutSeconds }
:   Type `int`, default `10`.

`airflow.webserver.resources.limits` <a class="headerlink" href="#helm.airflow.webserver.resources.limits" title="Permanent link">#</a> { #helm.airflow.webserver.resources.limits }
:   Type `object`, default `{"memory":"2000Mi"}`.
    resources limits configuration

`airflow.webserver.resources.requests` <a class="headerlink" href="#helm.airflow.webserver.resources.requests" title="Permanent link">#</a> { #helm.airflow.webserver.resources.requests }
:   Type `object`, default `{"cpu":"100m","memory":"1000Mi"}`.
    resources requests configuration

`airflow.webserver.securityContext.runAsGroup` <a class="headerlink" href="#helm.airflow.webserver.securityContext.runAsGroup" title="Permanent link">#</a> { #helm.airflow.webserver.securityContext.runAsGroup }
:   Type `int`, default `1508`.

`airflow.webserver.securityContext.runAsUser` <a class="headerlink" href="#helm.airflow.webserver.securityContext.runAsUser" title="Permanent link">#</a> { #helm.airflow.webserver.securityContext.runAsUser }
:   Type `int`, default `1512`.

`airflow.webserver.service.annotations` <a class="headerlink" href="#helm.airflow.webserver.service.annotations" title="Permanent link">#</a> { #helm.airflow.webserver.service.annotations }
:   Type `object`.
    annotations on the airflow-webserver Service; the map is open, so an operator can add their own

    ??? note "Default"

        ```yaml
        consul.hashicorp.com/service-name: airflow
        consul.hashicorp.com/service-port: server
        consul.hashicorp.com/service-tags: ui
        ```

`airflow.webserver.tolerations` <a class="headerlink" href="#helm.airflow.webserver.tolerations" title="Permanent link">#</a> { #helm.airflow.webserver.tolerations }
:   Type `list`, default `[]`.

`airflow.webserver.topologySpreadConstraint` <a class="headerlink" href="#helm.airflow.webserver.topologySpreadConstraint" title="Permanent link">#</a> { #helm.airflow.webserver.topologySpreadConstraint }
:   Type `object`, default `{}`.
    The default topology spread constraint. If not defined the global topology spread constraint would be used instead.

</div>

<!-- END GENERATED VALUES -->
