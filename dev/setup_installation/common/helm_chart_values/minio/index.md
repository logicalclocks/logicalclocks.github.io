# MinIO values { #helm-values-minio }

Values under `minio` configure MinIO, an S3-compatible object store deployed inside the cluster.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.2.0-alpha-1791295130` (Hopsworks `5.2.0`)._

Deployed when [`global._hopsworks.minio.enabled`](global.md#helm.global._hopsworks.minio.enabled) is `true`.

## General { #helm-values-minio-general }

??? example "Defaults as YAML"

    ```yaml
    minio:
      add_node_port: false
      affinity: {}
      buckets:
      - name: hopsworks
      cleanupOnUninstall:
        enabled: true
        ttlSecondsAfterFinished: null
      deploymentName: minio
      enabled: true
      hopsworkslib: {}
      image:
        name: minio
        pullPolicy: IfNotPresent
        registry: docker.hops.works
        tag: RELEASE.2024-03-26T22-10-45Z-cpuv1
      nodeSelector: {}
      podDisruptionBudget:
        enabled: true
        minAvailable: 1
      protocol: http
      publicBuckets:
      - name: public
      - name: buildkit
      replicas: 2
      resources:
        limits:
          cpu: '4'
          memory: 8Gi
        requests:
          cpu: '1'
          memory: 4Gi
      storage: 100Gi
      storageClassName: null
      tests:
        minioBackup:
          bucket: ''
          enabled: false
          subfolder: ''
      tolerations: []
    ```

<div class="hops-values" markdown>

`minio` <a class="headerlink" href="#helm.minio" title="Permanent link">#</a> { #helm.minio }
:   Type `object`.
    override minio values      

    ??? note "Default"

        ```yaml
        replicas: 2
        resources:
          limits:
            cpu: '4'
            memory: 8Gi
        storage: 100Gi
        ```

`minio.add_node_port` <a class="headerlink" href="#helm.minio.add_node_port" title="Permanent link">#</a> { #helm.minio.add_node_port }
:   Type `bool`, default `false`.

`minio.affinity` <a class="headerlink" href="#helm.minio.affinity" title="Permanent link">#</a> { #helm.minio.affinity }
:   Type `object`, default `{}`.
    affinity configuration

`minio.buckets[0].name` <a class="headerlink" href="#helm.minio.buckets.0.name" title="Permanent link">#</a> { #helm.minio.buckets.0.name }
:   Type `string`, default `"hopsworks"`.

`minio.cleanupOnUninstall` <a class="headerlink" href="#helm.minio.cleanupOnUninstall" title="Permanent link">#</a> { #helm.minio.cleanupOnUninstall }
:   Type `object`, default `{"enabled":true,"ttlSecondsAfterFinished":null}`.
    post-delete cleanup of MinIO leftovers. The MinIO StatefulSet PVC survives uninstall; this deletes it by label (app=minio), but only when global._hopsworks.wipeDataOnUninstall is enabled and never for PVCs labelled hopsworks.ai/keep=true.

`minio.cleanupOnUninstall.enabled` <a class="headerlink" href="#helm.minio.cleanupOnUninstall.enabled" title="Permanent link">#</a> { #helm.minio.cleanupOnUninstall.enabled }
:   Type `bool`, default `true`.
    enable the post-delete MinIO data-PVC cleanup hook (also requires global._hopsworks.wipeDataOnUninstall)

`minio.cleanupOnUninstall.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.minio.cleanupOnUninstall.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.minio.cleanupOnUninstall.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    ttlSecondsAfterFinished for the cleanup Job; null falls through to the global default

`minio.deploymentName` <a class="headerlink" href="#helm.minio.deploymentName" title="Permanent link">#</a> { #helm.minio.deploymentName }
:   Type `string`, default `"minio"`.

`minio.enabled` <a class="headerlink" href="#helm.minio.enabled" title="Permanent link">#</a> { #helm.minio.enabled }
:   Type `bool`, default `true`.

`minio.hopsworkslib` <a class="headerlink" href="#helm.minio.hopsworkslib" title="Permanent link">#</a> { #helm.minio.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`minio.image.name` <a class="headerlink" href="#helm.minio.image.name" title="Permanent link">#</a> { #helm.minio.image.name }
:   Type `string`, default `"minio"`.

`minio.image.pullPolicy` <a class="headerlink" href="#helm.minio.image.pullPolicy" title="Permanent link">#</a> { #helm.minio.image.pullPolicy }
:   Type `string`, default `"IfNotPresent"`.

`minio.image.registry` <a class="headerlink" href="#helm.minio.image.registry" title="Permanent link">#</a> { #helm.minio.image.registry }
:   Type `string`, default `"docker.hops.works"`.

`minio.image.tag` <a class="headerlink" href="#helm.minio.image.tag" title="Permanent link">#</a> { #helm.minio.image.tag }
:   Type `string`, default `"RELEASE.2024-03-26T22-10-45Z-cpuv1"`.

`minio.nodeSelector` <a class="headerlink" href="#helm.minio.nodeSelector" title="Permanent link">#</a> { #helm.minio.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

`minio.podDisruptionBudget.enabled` <a class="headerlink" href="#helm.minio.podDisruptionBudget.enabled" title="Permanent link">#</a> { #helm.minio.podDisruptionBudget.enabled }
:   Type `bool`, default `true`.

`minio.podDisruptionBudget.minAvailable` <a class="headerlink" href="#helm.minio.podDisruptionBudget.minAvailable" title="Permanent link">#</a> { #helm.minio.podDisruptionBudget.minAvailable }
:   Type `int`, default `1`.

`minio.protocol` <a class="headerlink" href="#helm.minio.protocol" title="Permanent link">#</a> { #helm.minio.protocol }
:   Type `string`, default `"http"`.

`minio.publicBuckets[0].name` <a class="headerlink" href="#helm.minio.publicBuckets.0.name" title="Permanent link">#</a> { #helm.minio.publicBuckets.0.name }
:   Type `string`, default `"public"`.

`minio.publicBuckets[1].name` <a class="headerlink" href="#helm.minio.publicBuckets.1.name" title="Permanent link">#</a> { #helm.minio.publicBuckets.1.name }
:   Type `string`, default `"buildkit"`.

`minio.replicas` <a class="headerlink" href="#helm.minio.replicas" title="Permanent link">#</a> { #helm.minio.replicas }
:   Type `int`, default `2`.

`minio.resources.limits.cpu` <a class="headerlink" href="#helm.minio.resources.limits.cpu" title="Permanent link">#</a> { #helm.minio.resources.limits.cpu }
:   Type `string`, default `"4"`.

`minio.resources.limits.memory` <a class="headerlink" href="#helm.minio.resources.limits.memory" title="Permanent link">#</a> { #helm.minio.resources.limits.memory }
:   Type `string`, default `"8Gi"`.

`minio.resources.requests.cpu` <a class="headerlink" href="#helm.minio.resources.requests.cpu" title="Permanent link">#</a> { #helm.minio.resources.requests.cpu }
:   Type `string`, default `"1"`.

`minio.resources.requests.memory` <a class="headerlink" href="#helm.minio.resources.requests.memory" title="Permanent link">#</a> { #helm.minio.resources.requests.memory }
:   Type `string`, default `"4Gi"`.

`minio.storage` <a class="headerlink" href="#helm.minio.storage" title="Permanent link">#</a> { #helm.minio.storage }
:   Type `string`, default `"100Gi"`.

`minio.storageClassName` <a class="headerlink" href="#helm.minio.storageClassName" title="Permanent link">#</a> { #helm.minio.storageClassName }
:   Type `string`, default `nil`.
    storage class name

`minio.tests.minioBackup.bucket` <a class="headerlink" href="#helm.minio.tests.minioBackup.bucket" title="Permanent link">#</a> { #helm.minio.tests.minioBackup.bucket }
:   Type `string`, default `""`.

`minio.tests.minioBackup.enabled` <a class="headerlink" href="#helm.minio.tests.minioBackup.enabled" title="Permanent link">#</a> { #helm.minio.tests.minioBackup.enabled }
:   Type `bool`, default `false`.

`minio.tests.minioBackup.subfolder` <a class="headerlink" href="#helm.minio.tests.minioBackup.subfolder" title="Permanent link">#</a> { #helm.minio.tests.minioBackup.subfolder }
:   Type `string`, default `""`.

`minio.tolerations` <a class="headerlink" href="#helm.minio.tolerations" title="Permanent link">#</a> { #helm.minio.tolerations }
:   Type `list`, default `[]`.

</div>

## deployment { #helm-values-minio-deployment }

??? example "Defaults as YAML"

    ```yaml
    minio:
      deployment:
        env:
          MINIO_REGION: eu-west-1
          MINIO_ROOT_PASSWORD: minioadmin
          MINIO_ROOT_USER: minioadmin
        extra_envs:
          MINIO_PROMETHEUS_AUTH_TYPE: public
        ports:
          console: 9001
          http: 9000
    ```

<div class="hops-values" markdown>

`minio.deployment.env.MINIO_REGION` <a class="headerlink" href="#helm.minio.deployment.env.MINIO_REGION" title="Permanent link">#</a> { #helm.minio.deployment.env.MINIO_REGION }
:   Type `string`, default `"eu-west-1"`.

`minio.deployment.env.MINIO_ROOT_PASSWORD` <a class="headerlink" href="#helm.minio.deployment.env.MINIO_ROOT_PASSWORD" title="Permanent link">#</a> { #helm.minio.deployment.env.MINIO_ROOT_PASSWORD }
:   Type `string`, default `"minioadmin"`.

`minio.deployment.env.MINIO_ROOT_USER` <a class="headerlink" href="#helm.minio.deployment.env.MINIO_ROOT_USER" title="Permanent link">#</a> { #helm.minio.deployment.env.MINIO_ROOT_USER }
:   Type `string`, default `"minioadmin"`.

`minio.deployment.extra_envs` <a class="headerlink" href="#helm.minio.deployment.extra_envs" title="Permanent link">#</a> { #helm.minio.deployment.extra_envs }
:   Type `object`, default `{"MINIO_PROMETHEUS_AUTH_TYPE":"public"}`.
    extra envs

`minio.deployment.ports.console` <a class="headerlink" href="#helm.minio.deployment.ports.console" title="Permanent link">#</a> { #helm.minio.deployment.ports.console }
:   Type `int`, default `9001`.

`minio.deployment.ports.http` <a class="headerlink" href="#helm.minio.deployment.ports.http" title="Permanent link">#</a> { #helm.minio.deployment.ports.http }
:   Type `int`, default `9000`.

</div>

## service { #helm-values-minio-service }

??? example "Defaults as YAML"

    ```yaml
    minio:
      service:
        annotations:
          consul.hashicorp.com/service-name: minio
          consul.hashicorp.com/service-port: http
        name: minio
        ports:
          console: 9001
          http: 9000
    ```

<div class="hops-values" markdown>

`minio.service.annotations."consul.hashicorp.com/service-name"` <a class="headerlink" href="#helm.minio.service.annotations.consul.hashicorp.com-service-name" title="Permanent link">#</a> { #helm.minio.service.annotations.consul.hashicorp.com-service-name }
:   Type `string`, default `"minio"`.

`minio.service.annotations."consul.hashicorp.com/service-port"` <a class="headerlink" href="#helm.minio.service.annotations.consul.hashicorp.com-service-port" title="Permanent link">#</a> { #helm.minio.service.annotations.consul.hashicorp.com-service-port }
:   Type `string`, default `"http"`.

`minio.service.name` <a class="headerlink" href="#helm.minio.service.name" title="Permanent link">#</a> { #helm.minio.service.name }
:   Type `string`, default `"minio"`.

`minio.service.ports.console` <a class="headerlink" href="#helm.minio.service.ports.console" title="Permanent link">#</a> { #helm.minio.service.ports.console }
:   Type `int`, default `9001`.

`minio.service.ports.http` <a class="headerlink" href="#helm.minio.service.ports.http" title="Permanent link">#</a> { #helm.minio.service.ports.http }
:   Type `int`, default `9000`.

</div>

<!-- END GENERATED VALUES -->
