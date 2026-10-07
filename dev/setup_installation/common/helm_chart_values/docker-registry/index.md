# Docker registry values { #helm-values-docker-registry }

Values under `docker-registry` configure the in-cluster Docker registry that stores the images Hopsworks builds, such as project Python environments.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.2.0-alpha-1791369399` (Hopsworks `5.2.0`)._

Deployed when [`global._hopsworks.full_platform`](global.md#helm.global._hopsworks.full_platform) is `true`.

## General { #helm-values-docker-registry-general }

??? example "Defaults as YAML"

    ```yaml
    docker-registry:
      affinity: {}
      appName: docker-registry
      debug: false
      dependencies:
        objectStorage:
          consulServiceName: minio
          port: 9000
      enabled: true
      hopsworkslib: {}
      image:
        name: registry
        pullPolicy: IfNotPresent
        registry: docker.hops.works
        tag: 3.1.1
      nodeSelector: {}
      podDisruptionBudget:
        enabled: true
        minAvailable: 1
      replicas: 1
      resources:
        limits:
          cpu: '2'
          memory: 10G
        requests:
          cpu: '2'
          memory: 4G
      security:
        secret: docker
        tls:
          enabled: true
      service:
        headless:
          name: registry-headless
        monitoringPort: 5001
        nodePort:
          annotations:
            consul.hashicorp.com/service-name: registry
        port: 30443
      storage: null
      storageClassName: null
      tolerations: []
    ```

<div class="hops-values" markdown>

`docker-registry` <a class="headerlink" href="#helm.docker-registry" title="Permanent link">#</a> { #helm.docker-registry }
:   Type `object`, default `{"storageClassName":null}`.
    override docker-registry values

`docker-registry.affinity` <a class="headerlink" href="#helm.docker-registry.affinity" title="Permanent link">#</a> { #helm.docker-registry.affinity }
:   Type `object`, default `{}`.
    affinity configuration

`docker-registry.appName` <a class="headerlink" href="#helm.docker-registry.appName" title="Permanent link">#</a> { #helm.docker-registry.appName }
:   Type `string`, default `"docker-registry"`.

`docker-registry.debug` <a class="headerlink" href="#helm.docker-registry.debug" title="Permanent link">#</a> { #helm.docker-registry.debug }
:   Type `bool`, default `false`.

`docker-registry.dependencies.objectStorage.consulServiceName` <a class="headerlink" href="#helm.docker-registry.dependencies.objectStorage.consulServiceName" title="Permanent link">#</a> { #helm.docker-registry.dependencies.objectStorage.consulServiceName }
:   Type `string`, default `"minio"`.

`docker-registry.dependencies.objectStorage.port` <a class="headerlink" href="#helm.docker-registry.dependencies.objectStorage.port" title="Permanent link">#</a> { #helm.docker-registry.dependencies.objectStorage.port }
:   Type `int`, default `9000`.

`docker-registry.enabled` <a class="headerlink" href="#helm.docker-registry.enabled" title="Permanent link">#</a> { #helm.docker-registry.enabled }
:   Type `bool`, default `true`.

`docker-registry.hopsworkslib` <a class="headerlink" href="#helm.docker-registry.hopsworkslib" title="Permanent link">#</a> { #helm.docker-registry.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`docker-registry.image.name` <a class="headerlink" href="#helm.docker-registry.image.name" title="Permanent link">#</a> { #helm.docker-registry.image.name }
:   Type `string`, default `"registry"`.

`docker-registry.image.pullPolicy` <a class="headerlink" href="#helm.docker-registry.image.pullPolicy" title="Permanent link">#</a> { #helm.docker-registry.image.pullPolicy }
:   Type `string`, default `"IfNotPresent"`.

`docker-registry.image.registry` <a class="headerlink" href="#helm.docker-registry.image.registry" title="Permanent link">#</a> { #helm.docker-registry.image.registry }
:   Type `string`, default `"docker.hops.works"`.

`docker-registry.image.tag` <a class="headerlink" href="#helm.docker-registry.image.tag" title="Permanent link">#</a> { #helm.docker-registry.image.tag }
:   Type `string`, default `"3.1.1"`.
    Distribution v3. The chart configures the registry only through `REGISTRY_*` environment variables and mounts no config file, so v3's new default config path does not affect it.

`docker-registry.nodeSelector` <a class="headerlink" href="#helm.docker-registry.nodeSelector" title="Permanent link">#</a> { #helm.docker-registry.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

`docker-registry.podDisruptionBudget.enabled` <a class="headerlink" href="#helm.docker-registry.podDisruptionBudget.enabled" title="Permanent link">#</a> { #helm.docker-registry.podDisruptionBudget.enabled }
:   Type `bool`, default `true`.

`docker-registry.podDisruptionBudget.minAvailable` <a class="headerlink" href="#helm.docker-registry.podDisruptionBudget.minAvailable" title="Permanent link">#</a> { #helm.docker-registry.podDisruptionBudget.minAvailable }
:   Type `int`, default `1`.

`docker-registry.replicas` <a class="headerlink" href="#helm.docker-registry.replicas" title="Permanent link">#</a> { #helm.docker-registry.replicas }
:   Type `int`, default `1`.
    Number of replicas. Not rendered while the HPA is active (hpa.enabled and no VPA on the registry): the HPA then owns spec.replicas, starting from hpa.minReplicas. Turning the HPA on for a running release drops the StatefulSet to 1 once, until the HPA scales it back up.

`docker-registry.resources.limits.cpu` <a class="headerlink" href="#helm.docker-registry.resources.limits.cpu" title="Permanent link">#</a> { #helm.docker-registry.resources.limits.cpu }
:   Type `string`, default `"2"`.

`docker-registry.resources.limits.memory` <a class="headerlink" href="#helm.docker-registry.resources.limits.memory" title="Permanent link">#</a> { #helm.docker-registry.resources.limits.memory }
:   Type `string`, default `"10G"`.

`docker-registry.resources.requests.cpu` <a class="headerlink" href="#helm.docker-registry.resources.requests.cpu" title="Permanent link">#</a> { #helm.docker-registry.resources.requests.cpu }
:   Type `string`, default `"2"`.

`docker-registry.resources.requests.memory` <a class="headerlink" href="#helm.docker-registry.resources.requests.memory" title="Permanent link">#</a> { #helm.docker-registry.resources.requests.memory }
:   Type `string`, default `"4G"`.

`docker-registry.security.secret` <a class="headerlink" href="#helm.docker-registry.security.secret" title="Permanent link">#</a> { #helm.docker-registry.security.secret }
:   Type `string`, default `"docker"`.

`docker-registry.security.tls.enabled` <a class="headerlink" href="#helm.docker-registry.security.tls.enabled" title="Permanent link">#</a> { #helm.docker-registry.security.tls.enabled }
:   Type `bool`, default `true`.

`docker-registry.service.headless.name` <a class="headerlink" href="#helm.docker-registry.service.headless.name" title="Permanent link">#</a> { #helm.docker-registry.service.headless.name }
:   Type `string`, default `"registry-headless"`.

`docker-registry.service.monitoringPort` <a class="headerlink" href="#helm.docker-registry.service.monitoringPort" title="Permanent link">#</a> { #helm.docker-registry.service.monitoringPort }
:   Type `int`, default `5001`.
    Port of the registry's debug server. Serves `/metrics`, and also `/debug/pprof`, which is why its Service is ClusterIP.

`docker-registry.service.nodePort.annotations."consul.hashicorp.com/service-name"` <a class="headerlink" href="#helm.docker-registry.service.nodePort.annotations.consul.hashicorp.com-service-name" title="Permanent link">#</a> { #helm.docker-registry.service.nodePort.annotations.consul.hashicorp.com-service-name }
:   Type `string`, default `"registry"`.

`docker-registry.service.port` <a class="headerlink" href="#helm.docker-registry.service.port" title="Permanent link">#</a> { #helm.docker-registry.service.port }
:   Type `int`, default `30443`.

`docker-registry.storage` <a class="headerlink" href="#helm.docker-registry.storage" title="Permanent link">#</a> { #helm.docker-registry.storage }
:   Type `string`, default `nil`.
    storage class name. Set if the REGISTRY_STORAGE is not S3

`docker-registry.storageClassName` <a class="headerlink" href="#helm.docker-registry.storageClassName" title="Permanent link">#</a> { #helm.docker-registry.storageClassName }
:   Type `string`, default `nil`.
    storage class name

`docker-registry.tolerations` <a class="headerlink" href="#helm.docker-registry.tolerations" title="Permanent link">#</a> { #helm.docker-registry.tolerations }
:   Type `list`, default `[]`.

</div>

## config { #helm-values-docker-registry-config }

??? example "Defaults as YAML"

    ```yaml
    docker-registry:
      config:
      - name: REGISTRY_STORAGE_DELETE_ENABLED
        value: 'true'
      - name: REGISTRY_STORAGE_CACHE_BLOBDESCRIPTOR
        value: inmemory
      - name: REGISTRY_STORAGE_CACHE_BLOBDESCRIPTORSIZE
        value: '10'
      - name: REGISTRY_STORAGE
        value: s3
      - name: REGISTRY_STORAGE_S3_ACCESSKEY
        value: minioadmin
      - name: REGISTRY_STORAGE_S3_SECRETKEY
        value: minioadmin
      - name: REGISTRY_STORAGE_S3_REGION
        value: eu-west-1
      - name: REGISTRY_STORAGE_S3_BUCKET
        value: public
      - name: REGISTRY_STORAGE_S3_ROOTDIRECTORY
        value: /
      - name: REGISTRY_STORAGE_S3_SECURE
        value: 'false'
      - name: REGISTRY_STORAGE_S3_V4AUTH
        value: 'true'
      - name: REGISTRY_STORAGE_S3_FORCEPATHSTYLE
        value: 'true'
      - name: REGISTRY_STORAGE_S3_LOGLEVEL
        value: debug
      - name: REGISTRY_STORAGE_S3_CHUNKSIZE
        value: '209715200'
      - name: REGISTRY_HTTP_DRAINTIMEOUT
        value: 10m
      - name: REGISTRY_VALIDATION_DISABLED
        value: 'true'
      - name: REGISTRY_STORAGE_REDIRECT_DISABLE
        value: 'true'
      - name: REGISTRY_LOG_LEVEL
        value: info
      - name: REGISTRY_HTTP_HEADERS
        value: '{X-Content-Type-Options: [nosniff]}'
    ```

<div class="hops-values" markdown>

`docker-registry.config[0].name` <a class="headerlink" href="#helm.docker-registry.config.0.name" title="Permanent link">#</a> { #helm.docker-registry.config.0.name }
:   Type `string`, default `"REGISTRY_STORAGE_DELETE_ENABLED"`.

`docker-registry.config[0].value` <a class="headerlink" href="#helm.docker-registry.config.0.value" title="Permanent link">#</a> { #helm.docker-registry.config.0.value }
:   Type `string`, default `"true"`.

`docker-registry.config[10].name` <a class="headerlink" href="#helm.docker-registry.config.10.name" title="Permanent link">#</a> { #helm.docker-registry.config.10.name }
:   Type `string`, default `"REGISTRY_STORAGE_S3_V4AUTH"`.

`docker-registry.config[10].value` <a class="headerlink" href="#helm.docker-registry.config.10.value" title="Permanent link">#</a> { #helm.docker-registry.config.10.value }
:   Type `string`, default `"true"`.

`docker-registry.config[11].name` <a class="headerlink" href="#helm.docker-registry.config.11.name" title="Permanent link">#</a> { #helm.docker-registry.config.11.name }
:   Type `string`, default `"REGISTRY_STORAGE_S3_FORCEPATHSTYLE"`.

`docker-registry.config[11].value` <a class="headerlink" href="#helm.docker-registry.config.11.value" title="Permanent link">#</a> { #helm.docker-registry.config.11.value }
:   Type `string`, default `"true"`.

`docker-registry.config[12].name` <a class="headerlink" href="#helm.docker-registry.config.12.name" title="Permanent link">#</a> { #helm.docker-registry.config.12.name }
:   Type `string`, default `"REGISTRY_STORAGE_S3_LOGLEVEL"`.

`docker-registry.config[12].value` <a class="headerlink" href="#helm.docker-registry.config.12.value" title="Permanent link">#</a> { #helm.docker-registry.config.12.value }
:   Type `string`, default `"debug"`.

`docker-registry.config[13].name` <a class="headerlink" href="#helm.docker-registry.config.13.name" title="Permanent link">#</a> { #helm.docker-registry.config.13.name }
:   Type `string`, default `"REGISTRY_STORAGE_S3_CHUNKSIZE"`.

`docker-registry.config[13].value` <a class="headerlink" href="#helm.docker-registry.config.13.value" title="Permanent link">#</a> { #helm.docker-registry.config.13.value }
:   Type `string`, default `"209715200"`.

`docker-registry.config[14].name` <a class="headerlink" href="#helm.docker-registry.config.14.name" title="Permanent link">#</a> { #helm.docker-registry.config.14.name }
:   Type `string`, default `"REGISTRY_HTTP_DRAINTIMEOUT"`.

`docker-registry.config[14].value` <a class="headerlink" href="#helm.docker-registry.config.14.value" title="Permanent link">#</a> { #helm.docker-registry.config.14.value }
:   Type `string`, default `"10m"`.

`docker-registry.config[15].name` <a class="headerlink" href="#helm.docker-registry.config.15.name" title="Permanent link">#</a> { #helm.docker-registry.config.15.name }
:   Type `string`, default `"REGISTRY_VALIDATION_DISABLED"`.

`docker-registry.config[15].value` <a class="headerlink" href="#helm.docker-registry.config.15.value" title="Permanent link">#</a> { #helm.docker-registry.config.15.value }
:   Type `string`, default `"true"`.

`docker-registry.config[16].name` <a class="headerlink" href="#helm.docker-registry.config.16.name" title="Permanent link">#</a> { #helm.docker-registry.config.16.name }
:   Type `string`, default `"REGISTRY_STORAGE_REDIRECT_DISABLE"`.

`docker-registry.config[16].value` <a class="headerlink" href="#helm.docker-registry.config.16.value" title="Permanent link">#</a> { #helm.docker-registry.config.16.value }
:   Type `string`, default `"true"`.

`docker-registry.config[17].name` <a class="headerlink" href="#helm.docker-registry.config.17.name" title="Permanent link">#</a> { #helm.docker-registry.config.17.name }
:   Type `string`, default `"REGISTRY_LOG_LEVEL"`.

`docker-registry.config[17].value` <a class="headerlink" href="#helm.docker-registry.config.17.value" title="Permanent link">#</a> { #helm.docker-registry.config.17.value }
:   Type `string`, default `"info"`.

`docker-registry.config[18].name` <a class="headerlink" href="#helm.docker-registry.config.18.name" title="Permanent link">#</a> { #helm.docker-registry.config.18.name }
:   Type `string`, default `"REGISTRY_HTTP_HEADERS"`.

`docker-registry.config[18].value` <a class="headerlink" href="#helm.docker-registry.config.18.value" title="Permanent link">#</a> { #helm.docker-registry.config.18.value }
:   Type `string`, default `"{X-Content-Type-Options: [nosniff]}"`.

`docker-registry.config[1].name` <a class="headerlink" href="#helm.docker-registry.config.1.name" title="Permanent link">#</a> { #helm.docker-registry.config.1.name }
:   Type `string`, default `"REGISTRY_STORAGE_CACHE_BLOBDESCRIPTOR"`.

`docker-registry.config[1].value` <a class="headerlink" href="#helm.docker-registry.config.1.value" title="Permanent link">#</a> { #helm.docker-registry.config.1.value }
:   Type `string`, default `"inmemory"`.

`docker-registry.config[2].name` <a class="headerlink" href="#helm.docker-registry.config.2.name" title="Permanent link">#</a> { #helm.docker-registry.config.2.name }
:   Type `string`, default `"REGISTRY_STORAGE_CACHE_BLOBDESCRIPTORSIZE"`.

`docker-registry.config[2].value` <a class="headerlink" href="#helm.docker-registry.config.2.value" title="Permanent link">#</a> { #helm.docker-registry.config.2.value }
:   Type `string`, default `"10"`.

`docker-registry.config[3].name` <a class="headerlink" href="#helm.docker-registry.config.3.name" title="Permanent link">#</a> { #helm.docker-registry.config.3.name }
:   Type `string`, default `"REGISTRY_STORAGE"`.

`docker-registry.config[3].value` <a class="headerlink" href="#helm.docker-registry.config.3.value" title="Permanent link">#</a> { #helm.docker-registry.config.3.value }
:   Type `string`, default `"s3"`.

`docker-registry.config[4].name` <a class="headerlink" href="#helm.docker-registry.config.4.name" title="Permanent link">#</a> { #helm.docker-registry.config.4.name }
:   Type `string`, default `"REGISTRY_STORAGE_S3_ACCESSKEY"`.

`docker-registry.config[4].value` <a class="headerlink" href="#helm.docker-registry.config.4.value" title="Permanent link">#</a> { #helm.docker-registry.config.4.value }
:   Type `string`, default `"minioadmin"`.

`docker-registry.config[5].name` <a class="headerlink" href="#helm.docker-registry.config.5.name" title="Permanent link">#</a> { #helm.docker-registry.config.5.name }
:   Type `string`, default `"REGISTRY_STORAGE_S3_SECRETKEY"`.

`docker-registry.config[5].value` <a class="headerlink" href="#helm.docker-registry.config.5.value" title="Permanent link">#</a> { #helm.docker-registry.config.5.value }
:   Type `string`, default `"minioadmin"`.

`docker-registry.config[6].name` <a class="headerlink" href="#helm.docker-registry.config.6.name" title="Permanent link">#</a> { #helm.docker-registry.config.6.name }
:   Type `string`, default `"REGISTRY_STORAGE_S3_REGION"`.

`docker-registry.config[6].value` <a class="headerlink" href="#helm.docker-registry.config.6.value" title="Permanent link">#</a> { #helm.docker-registry.config.6.value }
:   Type `string`, default `"eu-west-1"`.

`docker-registry.config[7].name` <a class="headerlink" href="#helm.docker-registry.config.7.name" title="Permanent link">#</a> { #helm.docker-registry.config.7.name }
:   Type `string`, default `"REGISTRY_STORAGE_S3_BUCKET"`.

`docker-registry.config[7].value` <a class="headerlink" href="#helm.docker-registry.config.7.value" title="Permanent link">#</a> { #helm.docker-registry.config.7.value }
:   Type `string`, default `"public"`.

`docker-registry.config[8].name` <a class="headerlink" href="#helm.docker-registry.config.8.name" title="Permanent link">#</a> { #helm.docker-registry.config.8.name }
:   Type `string`, default `"REGISTRY_STORAGE_S3_ROOTDIRECTORY"`.

`docker-registry.config[8].value` <a class="headerlink" href="#helm.docker-registry.config.8.value" title="Permanent link">#</a> { #helm.docker-registry.config.8.value }
:   Type `string`, default `"/"`.

`docker-registry.config[9].name` <a class="headerlink" href="#helm.docker-registry.config.9.name" title="Permanent link">#</a> { #helm.docker-registry.config.9.name }
:   Type `string`, default `"REGISTRY_STORAGE_S3_SECURE"`.

`docker-registry.config[9].value` <a class="headerlink" href="#helm.docker-registry.config.9.value" title="Permanent link">#</a> { #helm.docker-registry.config.9.value }
:   Type `string`, default `"false"`.

</div>

## hpa { #helm-values-docker-registry-hpa }

??? example "Defaults as YAML"

    ```yaml
    docker-registry:
      hpa:
        enabled: true
        maxReplicas: 4
        minReplicas: 1
        targetCPUUtilizationPercentage: 60
        targetMemoryUtilizationPercentage: 60
    ```

<div class="hops-values" markdown>

`docker-registry.hpa.enabled` <a class="headerlink" href="#helm.docker-registry.hpa.enabled" title="Permanent link">#</a> { #helm.docker-registry.hpa.enabled }
:   Type `bool`, default `true`.
    Autoscale the registry with an HPA (suppressed when a VPA targets it). While active, replicas is not rendered and the HPA owns spec.replicas.

`docker-registry.hpa.maxReplicas` <a class="headerlink" href="#helm.docker-registry.hpa.maxReplicas" title="Permanent link">#</a> { #helm.docker-registry.hpa.maxReplicas }
:   Type `int`, default `4`.

`docker-registry.hpa.minReplicas` <a class="headerlink" href="#helm.docker-registry.hpa.minReplicas" title="Permanent link">#</a> { #helm.docker-registry.hpa.minReplicas }
:   Type `int`, default `1`.

`docker-registry.hpa.targetCPUUtilizationPercentage` <a class="headerlink" href="#helm.docker-registry.hpa.targetCPUUtilizationPercentage" title="Permanent link">#</a> { #helm.docker-registry.hpa.targetCPUUtilizationPercentage }
:   Type `int`, default `60`.

`docker-registry.hpa.targetMemoryUtilizationPercentage` <a class="headerlink" href="#helm.docker-registry.hpa.targetMemoryUtilizationPercentage" title="Permanent link">#</a> { #helm.docker-registry.hpa.targetMemoryUtilizationPercentage }
:   Type `int`, default `60`.

</div>

## tamperContainerEngine { #helm-values-docker-registry-tampercontainerengine }

??? example "Defaults as YAML"

    ```yaml
    docker-registry:
      tamperContainerEngine:
        containerdConfigFile: config.toml
        defaultServer: null
        enabled: true
        fallbackTo: https://docker.hops.works
        patchEngine: true
        patchEtcHosts: true
        patchOS: true
        registryProtocol: https
        rollbackChangesIfDeleted: true
        tolerations:
        - effect: NoSchedule
          operator: Exists
        - key: CriticalAddonsOnly
          operator: Exists
        - effect: NoExecute
          operator: Exists
        trustCA: USE_ROOT_HOPSWORKS_CA
        verifyTLS: true
        waitBeforeReset: 0
    ```

<div class="hops-values" markdown>

`docker-registry.tamperContainerEngine.containerdConfigFile` <a class="headerlink" href="#helm.docker-registry.tamperContainerEngine.containerdConfigFile" title="Permanent link">#</a> { #helm.docker-registry.tamperContainerEngine.containerdConfigFile }
:   Type `string`, default `"config.toml"`.

`docker-registry.tamperContainerEngine.defaultServer` <a class="headerlink" href="#helm.docker-registry.tamperContainerEngine.defaultServer" title="Permanent link">#</a> { #helm.docker-registry.tamperContainerEngine.defaultServer }
:   Type `string`, default `nil`.
    default server to use in container engine. Change it to docker.hops.works if needed

`docker-registry.tamperContainerEngine.enabled` <a class="headerlink" href="#helm.docker-registry.tamperContainerEngine.enabled" title="Permanent link">#</a> { #helm.docker-registry.tamperContainerEngine.enabled }
:   Type `bool`, default `true`.

`docker-registry.tamperContainerEngine.fallbackTo` <a class="headerlink" href="#helm.docker-registry.tamperContainerEngine.fallbackTo" title="Permanent link">#</a> { #helm.docker-registry.tamperContainerEngine.fallbackTo }
:   Type `string`, default `"https://docker.hops.works"`.

`docker-registry.tamperContainerEngine.patchEngine` <a class="headerlink" href="#helm.docker-registry.tamperContainerEngine.patchEngine" title="Permanent link">#</a> { #helm.docker-registry.tamperContainerEngine.patchEngine }
:   Type `bool`, default `true`.

`docker-registry.tamperContainerEngine.patchEtcHosts` <a class="headerlink" href="#helm.docker-registry.tamperContainerEngine.patchEtcHosts" title="Permanent link">#</a> { #helm.docker-registry.tamperContainerEngine.patchEtcHosts }
:   Type `bool`, default `true`.

`docker-registry.tamperContainerEngine.patchOS` <a class="headerlink" href="#helm.docker-registry.tamperContainerEngine.patchOS" title="Permanent link">#</a> { #helm.docker-registry.tamperContainerEngine.patchOS }
:   Type `bool`, default `true`.

`docker-registry.tamperContainerEngine.registryProtocol` <a class="headerlink" href="#helm.docker-registry.tamperContainerEngine.registryProtocol" title="Permanent link">#</a> { #helm.docker-registry.tamperContainerEngine.registryProtocol }
:   Type `string`, default `"https"`.

`docker-registry.tamperContainerEngine.rollbackChangesIfDeleted` <a class="headerlink" href="#helm.docker-registry.tamperContainerEngine.rollbackChangesIfDeleted" title="Permanent link">#</a> { #helm.docker-registry.tamperContainerEngine.rollbackChangesIfDeleted }
:   Type `bool`, default `true`.

`docker-registry.tamperContainerEngine.tolerations[0].effect` <a class="headerlink" href="#helm.docker-registry.tamperContainerEngine.tolerations.0.effect" title="Permanent link">#</a> { #helm.docker-registry.tamperContainerEngine.tolerations.0.effect }
:   Type `string`, default `"NoSchedule"`.

`docker-registry.tamperContainerEngine.tolerations[0].operator` <a class="headerlink" href="#helm.docker-registry.tamperContainerEngine.tolerations.0.operator" title="Permanent link">#</a> { #helm.docker-registry.tamperContainerEngine.tolerations.0.operator }
:   Type `string`, default `"Exists"`.

`docker-registry.tamperContainerEngine.tolerations[1].key` <a class="headerlink" href="#helm.docker-registry.tamperContainerEngine.tolerations.1.key" title="Permanent link">#</a> { #helm.docker-registry.tamperContainerEngine.tolerations.1.key }
:   Type `string`, default `"CriticalAddonsOnly"`.

`docker-registry.tamperContainerEngine.tolerations[1].operator` <a class="headerlink" href="#helm.docker-registry.tamperContainerEngine.tolerations.1.operator" title="Permanent link">#</a> { #helm.docker-registry.tamperContainerEngine.tolerations.1.operator }
:   Type `string`, default `"Exists"`.

`docker-registry.tamperContainerEngine.tolerations[2].effect` <a class="headerlink" href="#helm.docker-registry.tamperContainerEngine.tolerations.2.effect" title="Permanent link">#</a> { #helm.docker-registry.tamperContainerEngine.tolerations.2.effect }
:   Type `string`, default `"NoExecute"`.

`docker-registry.tamperContainerEngine.tolerations[2].operator` <a class="headerlink" href="#helm.docker-registry.tamperContainerEngine.tolerations.2.operator" title="Permanent link">#</a> { #helm.docker-registry.tamperContainerEngine.tolerations.2.operator }
:   Type `string`, default `"Exists"`.

`docker-registry.tamperContainerEngine.trustCA` <a class="headerlink" href="#helm.docker-registry.tamperContainerEngine.trustCA" title="Permanent link">#</a> { #helm.docker-registry.tamperContainerEngine.trustCA }
:   Type `string`, default `"USE_ROOT_HOPSWORKS_CA"`.

`docker-registry.tamperContainerEngine.verifyTLS` <a class="headerlink" href="#helm.docker-registry.tamperContainerEngine.verifyTLS" title="Permanent link">#</a> { #helm.docker-registry.tamperContainerEngine.verifyTLS }
:   Type `bool`, default `true`.

`docker-registry.tamperContainerEngine.waitBeforeReset` <a class="headerlink" href="#helm.docker-registry.tamperContainerEngine.waitBeforeReset" title="Permanent link">#</a> { #helm.docker-registry.tamperContainerEngine.waitBeforeReset }
:   Type `int`, default `0`.

</div>

<!-- END GENERATED VALUES -->
