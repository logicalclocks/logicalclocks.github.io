# HopsFS values { #helm-values-hopsfs }

Values under `hopsfs` configure HopsFS, the distributed file system behind datasets and the offline feature store.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.2.0-alpha-1791640691` (Hopsworks `5.2.0`)._

Deployed when [`global._hopsworks.full_platform`](global.md#helm.global._hopsworks.full_platform) is `true`.

## General { #helm-values-hopsfs-general }

??? example "Defaults as YAML"

    ```yaml
    hopsfs:
      bypassBucketValidation: false
      cleanupOnUninstall:
        enabled: true
        ttlSecondsAfterFinished: null
      client:
        failureReplacementPolicy: NEVER
        locateFollowingBlockRetries: 10
      dataDir: /srv/hops/hopsdata/hdfs
      datanode:
        count: 5
        storage:
          size: 100Gi
          storageClassName: null
      hopsworkslib: {}
      image:
        name: hopsfs
        pullPolicy: IfNotPresent
        registry: ''
        tag: 3.4.3.3-EE-RC1
      namenode:
        resources:
          limits:
            memory: 2048Mi
          requests:
            memory: 1024Mi
      nuke_db_in_retry: false
      objectStorage:
        enabled: true
      parallel_preset: 3
      presetJob:
        clientRetryCount: 10
        clientRetryIntervalSeconds: 10
        runIndex: 0
        ttlSecondsAfterFinished: null
      serviceAccount:
        annotations: {}
      setupJob:
        timeoutMinutes: 25
    ```

<div class="hops-values" markdown>

`hopsfs` <a class="headerlink" href="#helm.hopsfs" title="Permanent link">#</a> { #helm.hopsfs }
:   Type `object`.
    override hopsfs values

    ??? note "Default"

        ```yaml
        datanode:
          count: 5
          storage:
            size: 100Gi
            storageClassName: null
        namenode:
          resources:
            limits:
              memory: 2048Mi
            requests:
              memory: 1024Mi
        objectStorage:
          enabled: true
        ```

`hopsfs.bypassBucketValidation` <a class="headerlink" href="#helm.hopsfs.bypassBucketValidation" title="Permanent link">#</a> { #helm.hopsfs.bypassBucketValidation }
:   Type `bool`, default `false`.
    Do not run HopsFS bucket validation pre-install, pre-upgrade Job

`hopsfs.cleanupOnUninstall` <a class="headerlink" href="#helm.hopsfs.cleanupOnUninstall" title="Permanent link">#</a> { #helm.hopsfs.cleanupOnUninstall }
:   Type `object`, default `{"enabled":true,"ttlSecondsAfterFinished":null}`.
    post-delete cleanup of HopsFS leftovers. The datanode StatefulSet PVC survives uninstall; this deletes it by its labels (app=hopsfs, service=datanode), but only when global._hopsworks.wipeDataOnUninstall is enabled and never for PVCs labelled hopsworks.ai/keep=true.

`hopsfs.cleanupOnUninstall.enabled` <a class="headerlink" href="#helm.hopsfs.cleanupOnUninstall.enabled" title="Permanent link">#</a> { #helm.hopsfs.cleanupOnUninstall.enabled }
:   Type `bool`, default `true`.
    enable the post-delete HopsFS data-PVC cleanup hook (also requires global._hopsworks.wipeDataOnUninstall)

`hopsfs.cleanupOnUninstall.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.hopsfs.cleanupOnUninstall.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.hopsfs.cleanupOnUninstall.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    ttlSecondsAfterFinished for the cleanup Job; null falls through to the global default

`hopsfs.client.failureReplacementPolicy` <a class="headerlink" href="#helm.hopsfs.client.failureReplacementPolicy" title="Permanent link">#</a> { #helm.hopsfs.client.failureReplacementPolicy }
:   Type `string`, default `"NEVER"`.

`hopsfs.client.locateFollowingBlockRetries` <a class="headerlink" href="#helm.hopsfs.client.locateFollowingBlockRetries" title="Permanent link">#</a> { #helm.hopsfs.client.locateFollowingBlockRetries }
:   Type `int`, default `10`.

`hopsfs.dataDir` <a class="headerlink" href="#helm.hopsfs.dataDir" title="Permanent link">#</a> { #helm.hopsfs.dataDir }
:   Type `string`, default `"/srv/hops/hopsdata/hdfs"`.

`hopsfs.hopsworkslib` <a class="headerlink" href="#helm.hopsfs.hopsworkslib" title="Permanent link">#</a> { #helm.hopsfs.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`hopsfs.image.name` <a class="headerlink" href="#helm.hopsfs.image.name" title="Permanent link">#</a> { #helm.hopsfs.image.name }
:   Type `string`, default `"hopsfs"`.

`hopsfs.image.pullPolicy` <a class="headerlink" href="#helm.hopsfs.image.pullPolicy" title="Permanent link">#</a> { #helm.hopsfs.image.pullPolicy }
:   Type `string`, default `"IfNotPresent"`.

`hopsfs.image.registry` <a class="headerlink" href="#helm.hopsfs.image.registry" title="Permanent link">#</a> { #helm.hopsfs.image.registry }
:   Type `string`, default `""`.
    Override the full registry+path prefix (must end with /). When set (non-empty), takes precedence over global._hopsworks.imageRegistry, bypassing the hardcoded /hopsworks/ segment. Use for custom HopsFS images at non-standard paths, e.g. "docker.hops.works/dev/salman/". Leave empty to use global._hopsworks.imageRegistry + "/hopsworks/".

`hopsfs.image.tag` <a class="headerlink" href="#helm.hopsfs.image.tag" title="Permanent link">#</a> { #helm.hopsfs.image.tag }
:   Type `string`, default `"3.4.3.3-EE-RC1"`.

`hopsfs.nuke_db_in_retry` <a class="headerlink" href="#helm.hopsfs.nuke_db_in_retry" title="Permanent link">#</a> { #helm.hopsfs.nuke_db_in_retry }
:   Type `bool`, default `false`.

`hopsfs.parallel_preset` <a class="headerlink" href="#helm.hopsfs.parallel_preset" title="Permanent link">#</a> { #helm.hopsfs.parallel_preset }
:   Type `int`, default `3`.

`hopsfs.presetJob.clientRetryCount` <a class="headerlink" href="#helm.hopsfs.presetJob.clientRetryCount" title="Permanent link">#</a> { #helm.hopsfs.presetJob.clientRetryCount }
:   Type `int`, default `10`.

`hopsfs.presetJob.clientRetryIntervalSeconds` <a class="headerlink" href="#helm.hopsfs.presetJob.clientRetryIntervalSeconds" title="Permanent link">#</a> { #helm.hopsfs.presetJob.clientRetryIntervalSeconds }
:   Type `int`, default `10`.

`hopsfs.presetJob.runIndex` <a class="headerlink" href="#helm.hopsfs.presetJob.runIndex" title="Permanent link">#</a> { #helm.hopsfs.presetJob.runIndex }
:   Type `int`, default `0`.
    Index to make job names unique if necessary

`hopsfs.presetJob.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.hopsfs.presetJob.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.hopsfs.presetJob.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    TTL in seconds for the namenode-preset-folders Job. Overrides global default.

`hopsfs.serviceAccount.annotations` <a class="headerlink" href="#helm.hopsfs.serviceAccount.annotations" title="Permanent link">#</a> { #helm.hopsfs.serviceAccount.annotations }
:   Type `object`, default `{}`.
    service account annotations

`hopsfs.setupJob.timeoutMinutes` <a class="headerlink" href="#helm.hopsfs.setupJob.timeoutMinutes" title="Permanent link">#</a> { #helm.hopsfs.setupJob.timeoutMinutes }
:   Type `int`, default `25`.

</div>

## datanode { #helm-values-hopsfs-datanode }

??? example "Defaults as YAML"

    ```yaml
    hopsfs:
      datanode:
        count: 5
        dataPort: 50010
        gracefulDrain:
          enabled: true
          terminationGracePeriodSecs: null
          timeoutSecs: null
          uploadThroughputMiBps: 35
        httpPort: 50075
        httpsPort: 50475
        ipcPort: 50020
        jvmOpts: ''
        loadBalancer:
          annotations: {}
          enabled: null
          loadBalancerClass: null
          managed: null
          nodePort: null
        monitoringPort: 50076
        nodeSelector: {}
        podDisruptionBudget:
          enabled: true
          minAvailable: 1
        resources:
          limits:
            cpu: '4'
            memory: 2048Mi
          requests:
            cpu: '1'
            memory: 500Mi
        rpcHandlerCount: 20
        storage:
          size: 100Gi
          storageClassName: null
        tls:
          extraDnsNames: []
          extraIpAddresses: []
        tolerations: []
        topologySpreadConstraint: {}
        xmx: 1024
    ```

<div class="hops-values" markdown>

`hopsfs.datanode.count` <a class="headerlink" href="#helm.hopsfs.datanode.count" title="Permanent link">#</a> { #helm.hopsfs.datanode.count }
:   Type `int`, default `5`.

`hopsfs.datanode.dataPort` <a class="headerlink" href="#helm.hopsfs.datanode.dataPort" title="Permanent link">#</a> { #helm.hopsfs.datanode.dataPort }
:   Type `int`, default `50010`.

`hopsfs.datanode.gracefulDrain.enabled` <a class="headerlink" href="#helm.hopsfs.datanode.gracefulDrain.enabled" title="Permanent link">#</a> { #helm.hopsfs.datanode.gracefulDrain.enabled }
:   Type `bool`, default `true`.
    Enable the preStop drain hook when async cloud upload is on. Set false to opt out even when async is enabled; risks data loss under non-empty upload backlog.

`hopsfs.datanode.gracefulDrain.terminationGracePeriodSecs` <a class="headerlink" href="#helm.hopsfs.datanode.gracefulDrain.terminationGracePeriodSecs" title="Permanent link">#</a> { #helm.hopsfs.datanode.gracefulDrain.terminationGracePeriodSecs }
:   Type `string`, default `nil`.
    Explicit override for the pod terminationGracePeriodSeconds. When null, defaults to the calculated drain timeout.

`hopsfs.datanode.gracefulDrain.timeoutSecs` <a class="headerlink" href="#helm.hopsfs.datanode.gracefulDrain.timeoutSecs" title="Permanent link">#</a> { #helm.hopsfs.datanode.gracefulDrain.timeoutSecs }
:   Type `string`, default `nil`.
    Explicit override for the dfsadmin -timeout passed to the preStop drain RPC. When null, calculated from queueCapacity, blockSizeMiB, and uploadThroughputMiBps.

`hopsfs.datanode.gracefulDrain.uploadThroughputMiBps` <a class="headerlink" href="#helm.hopsfs.datanode.gracefulDrain.uploadThroughputMiBps" title="Permanent link">#</a> { #helm.hopsfs.datanode.gracefulDrain.uploadThroughputMiBps }
:   Type `int`, default `35`.
    Operator estimate of per-DN S3 upload throughput in MiB/s. Drives the calculated drain timeout when timeoutSecs is null.

`hopsfs.datanode.httpPort` <a class="headerlink" href="#helm.hopsfs.datanode.httpPort" title="Permanent link">#</a> { #helm.hopsfs.datanode.httpPort }
:   Type `int`, default `50075`.

`hopsfs.datanode.httpsPort` <a class="headerlink" href="#helm.hopsfs.datanode.httpsPort" title="Permanent link">#</a> { #helm.hopsfs.datanode.httpsPort }
:   Type `int`, default `50475`.

`hopsfs.datanode.ipcPort` <a class="headerlink" href="#helm.hopsfs.datanode.ipcPort" title="Permanent link">#</a> { #helm.hopsfs.datanode.ipcPort }
:   Type `int`, default `50020`.

`hopsfs.datanode.jvmOpts` <a class="headerlink" href="#helm.hopsfs.datanode.jvmOpts" title="Permanent link">#</a> { #helm.hopsfs.datanode.jvmOpts }
:   Type `string`, default `""`.

`hopsfs.datanode.loadBalancer.annotations` <a class="headerlink" href="#helm.hopsfs.datanode.loadBalancer.annotations" title="Permanent link">#</a> { #helm.hopsfs.datanode.loadBalancer.annotations }
:   Type `object`, default `{}`.
    annotations for load balancer

`hopsfs.datanode.loadBalancer.enabled` <a class="headerlink" href="#helm.hopsfs.datanode.loadBalancer.enabled" title="Permanent link">#</a> { #helm.hopsfs.datanode.loadBalancer.enabled }
:   Type `string`, default `nil`.
    Enable External Load Balancers for datanode. If not set the .global._hopsworks.externalLoadBalancers.enabled will be used instead

`hopsfs.datanode.loadBalancer.loadBalancerClass` <a class="headerlink" href="#helm.hopsfs.datanode.loadBalancer.loadBalancerClass" title="Permanent link">#</a> { #helm.hopsfs.datanode.loadBalancer.loadBalancerClass }
:   Type `string`, default `nil`.
    load balancer class name

`hopsfs.datanode.loadBalancer.managed` <a class="headerlink" href="#helm.hopsfs.datanode.loadBalancer.managed" title="Permanent link">#</a> { #helm.hopsfs.datanode.loadBalancer.managed }
:   Type `string`, default `nil`.
    Cloud provider provisions Load Balancers. If not set the .global._hopsworks.externalLoadBalancers.managed will be used instead

`hopsfs.datanode.loadBalancer.nodePort` <a class="headerlink" href="#helm.hopsfs.datanode.loadBalancer.nodePort" title="Permanent link">#</a> { #helm.hopsfs.datanode.loadBalancer.nodePort }
:   Type `string`, default `nil`.
    Explicit nodePort for the external service when the load balancer is unmanaged (managed: false), so a load balancer outside Kubernetes can target a fixed port. Null lets Kubernetes allocate one from the cluster's node-port range; a set value must lie in that range (30000-32767 by default), which the API server enforces at install.

`hopsfs.datanode.monitoringPort` <a class="headerlink" href="#helm.hopsfs.datanode.monitoringPort" title="Permanent link">#</a> { #helm.hopsfs.datanode.monitoringPort }
:   Type `int`, default `50076`.

`hopsfs.datanode.nodeSelector` <a class="headerlink" href="#helm.hopsfs.datanode.nodeSelector" title="Permanent link">#</a> { #helm.hopsfs.datanode.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

`hopsfs.datanode.podDisruptionBudget.enabled` <a class="headerlink" href="#helm.hopsfs.datanode.podDisruptionBudget.enabled" title="Permanent link">#</a> { #helm.hopsfs.datanode.podDisruptionBudget.enabled }
:   Type `bool`, default `true`.
    Enable the DataNode PodDisruptionBudget. When enabled, the PDB hardcodes maxUnavailable=1 to prevent concurrent DN unavailability from exhausting HDFS client pipeline-recovery retries and failing in-flight writes. Not operator-tunable; this applies independently of async cloud upload.

`hopsfs.datanode.resources.limits.cpu` <a class="headerlink" href="#helm.hopsfs.datanode.resources.limits.cpu" title="Permanent link">#</a> { #helm.hopsfs.datanode.resources.limits.cpu }
:   Type `string`, default `"4"`.

`hopsfs.datanode.resources.limits.memory` <a class="headerlink" href="#helm.hopsfs.datanode.resources.limits.memory" title="Permanent link">#</a> { #helm.hopsfs.datanode.resources.limits.memory }
:   Type `string`, default `"2048Mi"`.

`hopsfs.datanode.resources.requests.cpu` <a class="headerlink" href="#helm.hopsfs.datanode.resources.requests.cpu" title="Permanent link">#</a> { #helm.hopsfs.datanode.resources.requests.cpu }
:   Type `string`, default `"1"`.

`hopsfs.datanode.resources.requests.memory` <a class="headerlink" href="#helm.hopsfs.datanode.resources.requests.memory" title="Permanent link">#</a> { #helm.hopsfs.datanode.resources.requests.memory }
:   Type `string`, default `"500Mi"`.

`hopsfs.datanode.rpcHandlerCount` <a class="headerlink" href="#helm.hopsfs.datanode.rpcHandlerCount" title="Permanent link">#</a> { #helm.hopsfs.datanode.rpcHandlerCount }
:   Type `int`, default `20`.

`hopsfs.datanode.storage.size` <a class="headerlink" href="#helm.hopsfs.datanode.storage.size" title="Permanent link">#</a> { #helm.hopsfs.datanode.storage.size }
:   Type `string`, default `"100Gi"`.

`hopsfs.datanode.storage.storageClassName` <a class="headerlink" href="#helm.hopsfs.datanode.storage.storageClassName" title="Permanent link">#</a> { #helm.hopsfs.datanode.storage.storageClassName }
:   Type `string`, default `nil`.
    storage class name to request for volumes attached to the data nodes

`hopsfs.datanode.tls.extraDnsNames` <a class="headerlink" href="#helm.hopsfs.datanode.tls.extraDnsNames" title="Permanent link">#</a> { #helm.hopsfs.datanode.tls.extraDnsNames }
:   Type `list`, default `[]`.
    Additional DNS names to add as SAN to Datanode x.509 certificate

`hopsfs.datanode.tls.extraIpAddresses` <a class="headerlink" href="#helm.hopsfs.datanode.tls.extraIpAddresses" title="Permanent link">#</a> { #helm.hopsfs.datanode.tls.extraIpAddresses }
:   Type `list`, default `[]`.
    Additional IP addresses to add as SAN to Datanode x.509 certificate

`hopsfs.datanode.tolerations` <a class="headerlink" href="#helm.hopsfs.datanode.tolerations" title="Permanent link">#</a> { #helm.hopsfs.datanode.tolerations }
:   Type `list`, default `[]`.

`hopsfs.datanode.topologySpreadConstraint` <a class="headerlink" href="#helm.hopsfs.datanode.topologySpreadConstraint" title="Permanent link">#</a> { #helm.hopsfs.datanode.topologySpreadConstraint }
:   Type `object`, default `{}`.
    The default topology spread constraint. If not defined the global topology spread constraint would be used instead.

`hopsfs.datanode.xmx` <a class="headerlink" href="#helm.hopsfs.datanode.xmx" title="Permanent link">#</a> { #helm.hopsfs.datanode.xmx }
:   Type `int`, default `1024`.

`hopsfs.datanode.podDisruptionBudget.minAvailable` <span class="hops-values-deprecated">Deprecated</span> <a class="headerlink" href="#helm.hopsfs.datanode.podDisruptionBudget.minAvailable" title="Permanent link">#</a> { #helm.hopsfs.datanode.podDisruptionBudget.minAvailable }
:   Type `int`, default `1`.
    DEPRECATED. The DN PDB no longer uses minAvailable; the template hardcodes maxUnavailable=1. Retained only so existing values overrides do not fail schema validation on upgrade.

</div>

## dependencies { #helm-values-hopsfs-dependencies }

??? example "Defaults as YAML"

    ```yaml
    hopsfs:
      dependencies:
        glassfish:
          consulServiceName: glassfish
          consulServiceTag: ca
          port: 8182
        mgmd:
          consulServiceName: mgmd
          port: 1186
        mysql:
          consulServiceName: mysql
          port: 3306
        objectStorage:
          consulServiceName: minio
          port: 9000
    ```

<div class="hops-values" markdown>

`hopsfs.dependencies.glassfish.consulServiceName` <a class="headerlink" href="#helm.hopsfs.dependencies.glassfish.consulServiceName" title="Permanent link">#</a> { #helm.hopsfs.dependencies.glassfish.consulServiceName }
:   Type `string`, default `"glassfish"`.

`hopsfs.dependencies.glassfish.consulServiceTag` <a class="headerlink" href="#helm.hopsfs.dependencies.glassfish.consulServiceTag" title="Permanent link">#</a> { #helm.hopsfs.dependencies.glassfish.consulServiceTag }
:   Type `string`, default `"ca"`.

`hopsfs.dependencies.glassfish.port` <a class="headerlink" href="#helm.hopsfs.dependencies.glassfish.port" title="Permanent link">#</a> { #helm.hopsfs.dependencies.glassfish.port }
:   Type `int`, default `8182`.

`hopsfs.dependencies.mgmd.consulServiceName` <a class="headerlink" href="#helm.hopsfs.dependencies.mgmd.consulServiceName" title="Permanent link">#</a> { #helm.hopsfs.dependencies.mgmd.consulServiceName }
:   Type `string`, default `"mgmd"`.

`hopsfs.dependencies.mgmd.port` <a class="headerlink" href="#helm.hopsfs.dependencies.mgmd.port" title="Permanent link">#</a> { #helm.hopsfs.dependencies.mgmd.port }
:   Type `int`, default `1186`.

`hopsfs.dependencies.mysql.consulServiceName` <a class="headerlink" href="#helm.hopsfs.dependencies.mysql.consulServiceName" title="Permanent link">#</a> { #helm.hopsfs.dependencies.mysql.consulServiceName }
:   Type `string`, default `"mysql"`.

`hopsfs.dependencies.mysql.port` <a class="headerlink" href="#helm.hopsfs.dependencies.mysql.port" title="Permanent link">#</a> { #helm.hopsfs.dependencies.mysql.port }
:   Type `int`, default `3306`.

`hopsfs.dependencies.objectStorage.consulServiceName` <a class="headerlink" href="#helm.hopsfs.dependencies.objectStorage.consulServiceName" title="Permanent link">#</a> { #helm.hopsfs.dependencies.objectStorage.consulServiceName }
:   Type `string`, default `"minio"`.

`hopsfs.dependencies.objectStorage.port` <a class="headerlink" href="#helm.hopsfs.dependencies.objectStorage.port" title="Permanent link">#</a> { #helm.hopsfs.dependencies.objectStorage.port }
:   Type `int`, default `9000`.

</div>

## log4j { #helm-values-hopsfs-log4j }

??? example "Defaults as YAML"

    ```yaml
    hopsfs:
      log4j:
        console_logger_level: INFO
        enable_audit_log: true
        level: INFO
        rfa_logger_level: INFO
        rfa_max_backup_index: 10
        rfa_max_file_size: 256MB
        root_level_logger: INFO
    ```

<div class="hops-values" markdown>

`hopsfs.log4j.console_logger_level` <a class="headerlink" href="#helm.hopsfs.log4j.console_logger_level" title="Permanent link">#</a> { #helm.hopsfs.log4j.console_logger_level }
:   Type `string`, default `"INFO"`.
    Log level threshold for Console appender. Defaults to root_level_logger if not specified.

`hopsfs.log4j.enable_audit_log` <a class="headerlink" href="#helm.hopsfs.log4j.enable_audit_log" title="Permanent link">#</a> { #helm.hopsfs.log4j.enable_audit_log }
:   Type `bool`, default `true`.

`hopsfs.log4j.level` <a class="headerlink" href="#helm.hopsfs.log4j.level" title="Permanent link">#</a> { #helm.hopsfs.log4j.level }
:   Type `string`, default `"INFO"`.
    Backward compatibility field. Not used by log4j configuration.

`hopsfs.log4j.rfa_logger_level` <a class="headerlink" href="#helm.hopsfs.log4j.rfa_logger_level" title="Permanent link">#</a> { #helm.hopsfs.log4j.rfa_logger_level }
:   Type `string`, default `"INFO"`.
    Log level threshold for Rolling File Appender. Defaults to root_level_logger if not specified.

`hopsfs.log4j.rfa_max_backup_index` <a class="headerlink" href="#helm.hopsfs.log4j.rfa_max_backup_index" title="Permanent link">#</a> { #helm.hopsfs.log4j.rfa_max_backup_index }
:   Type `int`, default `10`.
    Maximum number of backup log files to keep

`hopsfs.log4j.rfa_max_file_size` <a class="headerlink" href="#helm.hopsfs.log4j.rfa_max_file_size" title="Permanent link">#</a> { #helm.hopsfs.log4j.rfa_max_file_size }
:   Type `string`, default `"256MB"`.
    Maximum size of each log file before rotation (e.g., 256MB, 1GB)

`hopsfs.log4j.root_level_logger` <a class="headerlink" href="#helm.hopsfs.log4j.root_level_logger" title="Permanent link">#</a> { #helm.hopsfs.log4j.root_level_logger }
:   Type `string`, default `"INFO"`.
    Root logger level - acts as a global minimum level for all appenders

</div>

## namenode { #helm-values-hopsfs-namenode }

??? example "Defaults as YAML"

    ```yaml
    hopsfs:
      namenode:
        acls:
          enabled: true
        auditLog:
          enableListOperation: false
          enableStatOperation: false
        blockSizeMiB: 128
        blockreportExecutorCount: 40
        clusterIp:
          name: namenode-cluster-ip
        count: 1
        customConfig: {}
        dirs:
        - group: hdfs
          mode: 1775
          owner: payara
          path: /Projects
        - group: hadoop
          mode: 1775
          owner: hdfs
          path: /user
        - group: hadoop
          mode: 1775
          owner: hdfs
          path: /apps
        - group: hadoop
          mode: 1775
          owner: hdfs
          path: /tmp
        - group: hadoop
          mode: 1777
          owner: hive
          path: /tmp/hive
        httpPort: 50070
        httpsPort: 50470
        jvmOpts: ''
        loadBalancer:
          annotations: {}
          enabled: null
          loadBalancerClass: null
          managed: null
          nodePort: null
        maxBlocksPerFile: 10240
        maxDirectMemorySize: 1024
        maxDirectoryItems: 131072
        monitoringPort: 50071
        nodeSelector: {}
        numBlockReplicas: 1
        podDisruptionBudget:
          enabled: true
          minAvailable: 1
        quotaEnabled: true
        resources:
          limits:
            cpu: '4'
            memory: 2048Mi
          requests:
            cpu: '1'
            memory: 1024Mi
        rpcHandlerCount: 120
        rpcPort: 8020
        service:
          annotations:
            consul.hashicorp.com/service-name: namenode
            consul.hashicorp.com/service-port: rpc
            consul.hashicorp.com/service-tags: rpc,http
            prometheus.io/path: /metrics
            prometheus.io/port: 50071
            prometheus.io/scheme: http
            prometheus.io/scrape: 'true'
          name: namenode
        setupBackOffLimit: 10
        startupProbe:
          failureThreshold: 50
          initialDelaySeconds: 10
          periodSeconds: 15
          timeoutSeconds: 10
        stoCleanFaildOpsDelay: 600000
        stoCleanSlowOpsDelay: 900000
        subtreeExecutorCount: 40
        tls:
          extraDnsNames: []
          extraIpAddresses: []
        tolerations: []
        topologySpreadConstraint: {}
        txRetryCount: 10
        users:
        - gid: 1508
          group: airflow
          mode: 1750
          name: airflow
          uid: 1512
        - extra_folders:
          - /user/spark/applicationHistory
          - /user/spark/eventlog
          - /user/spark/share
          - /user/spark/spark-warehouse
          group: hadoop
          mode: 1777
          name: spark
          uid: 1505
        - extra_folders:
          - /apps/hive
          - /apps/hive/warehouse
          group: hadoop
          mode: 1755
          name: hive
        - group: hdfs
          mode: 1750
          name: payara
        - extra_folders:
          - /user/ray/applications
          group: hadoop
          mode: 1750
          name: ray
        - group: hdfs
          mode: 1750
          name: trino
        xattrs:
          enabled: true
          maxXAttrSize: 1039755
          maxXAttrsPerInode: 32
        xmx: 1024
    ```

<div class="hops-values" markdown>

`hopsfs.namenode.acls.enabled` <a class="headerlink" href="#helm.hopsfs.namenode.acls.enabled" title="Permanent link">#</a> { #helm.hopsfs.namenode.acls.enabled }
:   Type `bool`, default `true`.

`hopsfs.namenode.auditLog.enableListOperation` <a class="headerlink" href="#helm.hopsfs.namenode.auditLog.enableListOperation" title="Permanent link">#</a> { #helm.hopsfs.namenode.auditLog.enableListOperation }
:   Type `bool`, default `false`.

`hopsfs.namenode.auditLog.enableStatOperation` <a class="headerlink" href="#helm.hopsfs.namenode.auditLog.enableStatOperation" title="Permanent link">#</a> { #helm.hopsfs.namenode.auditLog.enableStatOperation }
:   Type `bool`, default `false`.

`hopsfs.namenode.blockSizeMiB` <a class="headerlink" href="#helm.hopsfs.namenode.blockSizeMiB" title="Permanent link">#</a> { #helm.hopsfs.namenode.blockSizeMiB }
:   Type `int`, default `128`.
    HDFS block size in MiB. Templated into dfs.blocksize. Also drives the calculated DN graceful-drain timeout.

`hopsfs.namenode.blockreportExecutorCount` <a class="headerlink" href="#helm.hopsfs.namenode.blockreportExecutorCount" title="Permanent link">#</a> { #helm.hopsfs.namenode.blockreportExecutorCount }
:   Type `int`, default `40`.

`hopsfs.namenode.clusterIp.name` <a class="headerlink" href="#helm.hopsfs.namenode.clusterIp.name" title="Permanent link">#</a> { #helm.hopsfs.namenode.clusterIp.name }
:   Type `string`, default `"namenode-cluster-ip"`.

`hopsfs.namenode.count` <a class="headerlink" href="#helm.hopsfs.namenode.count" title="Permanent link">#</a> { #helm.hopsfs.namenode.count }
:   Type `int`, default `1`.

`hopsfs.namenode.customConfig` <a class="headerlink" href="#helm.hopsfs.namenode.customConfig" title="Permanent link">#</a> { #helm.hopsfs.namenode.customConfig }
:   Type `object`, default `{}`.
    Set/Override hdfs-site.xml properties. Each entry in this map will template a <property></property> entry at the bottom of the hdfs-site.xml. The name of the property is the map entry key and the value of the property is the value of the map entry key.

`hopsfs.namenode.dirs[0].group` <a class="headerlink" href="#helm.hopsfs.namenode.dirs.0.group" title="Permanent link">#</a> { #helm.hopsfs.namenode.dirs.0.group }
:   Type `string`, default `"hdfs"`.

`hopsfs.namenode.dirs[0].mode` <a class="headerlink" href="#helm.hopsfs.namenode.dirs.0.mode" title="Permanent link">#</a> { #helm.hopsfs.namenode.dirs.0.mode }
:   Type `int`, default `1775`.

`hopsfs.namenode.dirs[0].owner` <a class="headerlink" href="#helm.hopsfs.namenode.dirs.0.owner" title="Permanent link">#</a> { #helm.hopsfs.namenode.dirs.0.owner }
:   Type `string`, default `"payara"`.

`hopsfs.namenode.dirs[0].path` <a class="headerlink" href="#helm.hopsfs.namenode.dirs.0.path" title="Permanent link">#</a> { #helm.hopsfs.namenode.dirs.0.path }
:   Type `string`, default `"/Projects"`.

`hopsfs.namenode.dirs[1].group` <a class="headerlink" href="#helm.hopsfs.namenode.dirs.1.group" title="Permanent link">#</a> { #helm.hopsfs.namenode.dirs.1.group }
:   Type `string`, default `"hadoop"`.

`hopsfs.namenode.dirs[1].mode` <a class="headerlink" href="#helm.hopsfs.namenode.dirs.1.mode" title="Permanent link">#</a> { #helm.hopsfs.namenode.dirs.1.mode }
:   Type `int`, default `1775`.

`hopsfs.namenode.dirs[1].owner` <a class="headerlink" href="#helm.hopsfs.namenode.dirs.1.owner" title="Permanent link">#</a> { #helm.hopsfs.namenode.dirs.1.owner }
:   Type `string`, default `"hdfs"`.

`hopsfs.namenode.dirs[1].path` <a class="headerlink" href="#helm.hopsfs.namenode.dirs.1.path" title="Permanent link">#</a> { #helm.hopsfs.namenode.dirs.1.path }
:   Type `string`, default `"/user"`.

`hopsfs.namenode.dirs[2].group` <a class="headerlink" href="#helm.hopsfs.namenode.dirs.2.group" title="Permanent link">#</a> { #helm.hopsfs.namenode.dirs.2.group }
:   Type `string`, default `"hadoop"`.

`hopsfs.namenode.dirs[2].mode` <a class="headerlink" href="#helm.hopsfs.namenode.dirs.2.mode" title="Permanent link">#</a> { #helm.hopsfs.namenode.dirs.2.mode }
:   Type `int`, default `1775`.

`hopsfs.namenode.dirs[2].owner` <a class="headerlink" href="#helm.hopsfs.namenode.dirs.2.owner" title="Permanent link">#</a> { #helm.hopsfs.namenode.dirs.2.owner }
:   Type `string`, default `"hdfs"`.

`hopsfs.namenode.dirs[2].path` <a class="headerlink" href="#helm.hopsfs.namenode.dirs.2.path" title="Permanent link">#</a> { #helm.hopsfs.namenode.dirs.2.path }
:   Type `string`, default `"/apps"`.

`hopsfs.namenode.dirs[3].group` <a class="headerlink" href="#helm.hopsfs.namenode.dirs.3.group" title="Permanent link">#</a> { #helm.hopsfs.namenode.dirs.3.group }
:   Type `string`, default `"hadoop"`.

`hopsfs.namenode.dirs[3].mode` <a class="headerlink" href="#helm.hopsfs.namenode.dirs.3.mode" title="Permanent link">#</a> { #helm.hopsfs.namenode.dirs.3.mode }
:   Type `int`, default `1775`.

`hopsfs.namenode.dirs[3].owner` <a class="headerlink" href="#helm.hopsfs.namenode.dirs.3.owner" title="Permanent link">#</a> { #helm.hopsfs.namenode.dirs.3.owner }
:   Type `string`, default `"hdfs"`.

`hopsfs.namenode.dirs[3].path` <a class="headerlink" href="#helm.hopsfs.namenode.dirs.3.path" title="Permanent link">#</a> { #helm.hopsfs.namenode.dirs.3.path }
:   Type `string`, default `"/tmp"`.

`hopsfs.namenode.dirs[4].group` <a class="headerlink" href="#helm.hopsfs.namenode.dirs.4.group" title="Permanent link">#</a> { #helm.hopsfs.namenode.dirs.4.group }
:   Type `string`, default `"hadoop"`.

`hopsfs.namenode.dirs[4].mode` <a class="headerlink" href="#helm.hopsfs.namenode.dirs.4.mode" title="Permanent link">#</a> { #helm.hopsfs.namenode.dirs.4.mode }
:   Type `int`, default `1777`.

`hopsfs.namenode.dirs[4].owner` <a class="headerlink" href="#helm.hopsfs.namenode.dirs.4.owner" title="Permanent link">#</a> { #helm.hopsfs.namenode.dirs.4.owner }
:   Type `string`, default `"hive"`.

`hopsfs.namenode.dirs[4].path` <a class="headerlink" href="#helm.hopsfs.namenode.dirs.4.path" title="Permanent link">#</a> { #helm.hopsfs.namenode.dirs.4.path }
:   Type `string`, default `"/tmp/hive"`.

`hopsfs.namenode.httpPort` <a class="headerlink" href="#helm.hopsfs.namenode.httpPort" title="Permanent link">#</a> { #helm.hopsfs.namenode.httpPort }
:   Type `int`, default `50070`.

`hopsfs.namenode.httpsPort` <a class="headerlink" href="#helm.hopsfs.namenode.httpsPort" title="Permanent link">#</a> { #helm.hopsfs.namenode.httpsPort }
:   Type `int`, default `50470`.

`hopsfs.namenode.jvmOpts` <a class="headerlink" href="#helm.hopsfs.namenode.jvmOpts" title="Permanent link">#</a> { #helm.hopsfs.namenode.jvmOpts }
:   Type `string`, default `""`.

`hopsfs.namenode.loadBalancer.annotations` <a class="headerlink" href="#helm.hopsfs.namenode.loadBalancer.annotations" title="Permanent link">#</a> { #helm.hopsfs.namenode.loadBalancer.annotations }
:   Type `object`, default `{}`.
    annotations for load balancer

`hopsfs.namenode.loadBalancer.enabled` <a class="headerlink" href="#helm.hopsfs.namenode.loadBalancer.enabled" title="Permanent link">#</a> { #helm.hopsfs.namenode.loadBalancer.enabled }
:   Type `string`, default `nil`.
    Enable External Load Balancers for namenode. If not set the .global._hopsworks.externalLoadBalancers.enabled will be used instead

`hopsfs.namenode.loadBalancer.loadBalancerClass` <a class="headerlink" href="#helm.hopsfs.namenode.loadBalancer.loadBalancerClass" title="Permanent link">#</a> { #helm.hopsfs.namenode.loadBalancer.loadBalancerClass }
:   Type `string`, default `nil`.
    load balancer class name

`hopsfs.namenode.loadBalancer.managed` <a class="headerlink" href="#helm.hopsfs.namenode.loadBalancer.managed" title="Permanent link">#</a> { #helm.hopsfs.namenode.loadBalancer.managed }
:   Type `string`, default `nil`.
    Cloud provider provisions Load Balancers. If not set the .global._hopsworks.externalLoadBalancers.managed will be used instead

`hopsfs.namenode.loadBalancer.nodePort` <a class="headerlink" href="#helm.hopsfs.namenode.loadBalancer.nodePort" title="Permanent link">#</a> { #helm.hopsfs.namenode.loadBalancer.nodePort }
:   Type `string`, default `nil`.
    Explicit nodePort for the external service when the load balancer is unmanaged (managed: false), so a load balancer outside Kubernetes can target a fixed port. Null lets Kubernetes allocate one from the cluster's node-port range; a set value must lie in that range (30000-32767 by default), which the API server enforces at install.

`hopsfs.namenode.maxBlocksPerFile` <a class="headerlink" href="#helm.hopsfs.namenode.maxBlocksPerFile" title="Permanent link">#</a> { #helm.hopsfs.namenode.maxBlocksPerFile }
:   Type `int`, default `10240`.
    Maximum number of blocks per file

`hopsfs.namenode.maxDirectMemorySize` <a class="headerlink" href="#helm.hopsfs.namenode.maxDirectMemorySize" title="Permanent link">#</a> { #helm.hopsfs.namenode.maxDirectMemorySize }
:   Type `int`, default `1024`.

`hopsfs.namenode.maxDirectoryItems` <a class="headerlink" href="#helm.hopsfs.namenode.maxDirectoryItems" title="Permanent link">#</a> { #helm.hopsfs.namenode.maxDirectoryItems }
:   Type `int`, default `131072`.
    Maximum number of items (files and directories) allowed in a directory

`hopsfs.namenode.monitoringPort` <a class="headerlink" href="#helm.hopsfs.namenode.monitoringPort" title="Permanent link">#</a> { #helm.hopsfs.namenode.monitoringPort }
:   Type `int`, default `50071`.

`hopsfs.namenode.nodeSelector` <a class="headerlink" href="#helm.hopsfs.namenode.nodeSelector" title="Permanent link">#</a> { #helm.hopsfs.namenode.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

`hopsfs.namenode.numBlockReplicas` <a class="headerlink" href="#helm.hopsfs.namenode.numBlockReplicas" title="Permanent link">#</a> { #helm.hopsfs.namenode.numBlockReplicas }
:   Type `int`, default `1`.

`hopsfs.namenode.podDisruptionBudget.enabled` <a class="headerlink" href="#helm.hopsfs.namenode.podDisruptionBudget.enabled" title="Permanent link">#</a> { #helm.hopsfs.namenode.podDisruptionBudget.enabled }
:   Type `bool`, default `true`.

`hopsfs.namenode.podDisruptionBudget.minAvailable` <a class="headerlink" href="#helm.hopsfs.namenode.podDisruptionBudget.minAvailable" title="Permanent link">#</a> { #helm.hopsfs.namenode.podDisruptionBudget.minAvailable }
:   Type `int`, default `1`.

`hopsfs.namenode.quotaEnabled` <a class="headerlink" href="#helm.hopsfs.namenode.quotaEnabled" title="Permanent link">#</a> { #helm.hopsfs.namenode.quotaEnabled }
:   Type `bool`, default `true`.

`hopsfs.namenode.resources.limits.cpu` <a class="headerlink" href="#helm.hopsfs.namenode.resources.limits.cpu" title="Permanent link">#</a> { #helm.hopsfs.namenode.resources.limits.cpu }
:   Type `string`, default `"4"`.

`hopsfs.namenode.resources.limits.memory` <a class="headerlink" href="#helm.hopsfs.namenode.resources.limits.memory" title="Permanent link">#</a> { #helm.hopsfs.namenode.resources.limits.memory }
:   Type `string`, default `"2048Mi"`.

`hopsfs.namenode.resources.requests.cpu` <a class="headerlink" href="#helm.hopsfs.namenode.resources.requests.cpu" title="Permanent link">#</a> { #helm.hopsfs.namenode.resources.requests.cpu }
:   Type `string`, default `"1"`.

`hopsfs.namenode.resources.requests.memory` <a class="headerlink" href="#helm.hopsfs.namenode.resources.requests.memory" title="Permanent link">#</a> { #helm.hopsfs.namenode.resources.requests.memory }
:   Type `string`, default `"1024Mi"`.

`hopsfs.namenode.rpcHandlerCount` <a class="headerlink" href="#helm.hopsfs.namenode.rpcHandlerCount" title="Permanent link">#</a> { #helm.hopsfs.namenode.rpcHandlerCount }
:   Type `int`, default `120`.

`hopsfs.namenode.rpcPort` <a class="headerlink" href="#helm.hopsfs.namenode.rpcPort" title="Permanent link">#</a> { #helm.hopsfs.namenode.rpcPort }
:   Type `int`, default `8020`.

`hopsfs.namenode.service.annotations."consul.hashicorp.com/service-name"` <a class="headerlink" href="#helm.hopsfs.namenode.service.annotations.consul.hashicorp.com-service-name" title="Permanent link">#</a> { #helm.hopsfs.namenode.service.annotations.consul.hashicorp.com-service-name }
:   Type `string`, default `"namenode"`.

`hopsfs.namenode.service.annotations."consul.hashicorp.com/service-port"` <a class="headerlink" href="#helm.hopsfs.namenode.service.annotations.consul.hashicorp.com-service-port" title="Permanent link">#</a> { #helm.hopsfs.namenode.service.annotations.consul.hashicorp.com-service-port }
:   Type `string`, default `"rpc"`.

`hopsfs.namenode.service.annotations."consul.hashicorp.com/service-tags"` <a class="headerlink" href="#helm.hopsfs.namenode.service.annotations.consul.hashicorp.com-service-tags" title="Permanent link">#</a> { #helm.hopsfs.namenode.service.annotations.consul.hashicorp.com-service-tags }
:   Type `string`, default `"rpc,http"`.

`hopsfs.namenode.service.annotations."prometheus.io/path"` <a class="headerlink" href="#helm.hopsfs.namenode.service.annotations.prometheus.io-path" title="Permanent link">#</a> { #helm.hopsfs.namenode.service.annotations.prometheus.io-path }
:   Type `string`, default `"/metrics"`.

`hopsfs.namenode.service.annotations."prometheus.io/port"` <a class="headerlink" href="#helm.hopsfs.namenode.service.annotations.prometheus.io-port" title="Permanent link">#</a> { #helm.hopsfs.namenode.service.annotations.prometheus.io-port }
:   Type `int`, default `50071`.

`hopsfs.namenode.service.annotations."prometheus.io/scheme"` <a class="headerlink" href="#helm.hopsfs.namenode.service.annotations.prometheus.io-scheme" title="Permanent link">#</a> { #helm.hopsfs.namenode.service.annotations.prometheus.io-scheme }
:   Type `string`, default `"http"`.

`hopsfs.namenode.service.annotations."prometheus.io/scrape"` <a class="headerlink" href="#helm.hopsfs.namenode.service.annotations.prometheus.io-scrape" title="Permanent link">#</a> { #helm.hopsfs.namenode.service.annotations.prometheus.io-scrape }
:   Type `string`, default `"true"`.

`hopsfs.namenode.service.name` <a class="headerlink" href="#helm.hopsfs.namenode.service.name" title="Permanent link">#</a> { #helm.hopsfs.namenode.service.name }
:   Type `string`, default `"namenode"`.

`hopsfs.namenode.setupBackOffLimit` <a class="headerlink" href="#helm.hopsfs.namenode.setupBackOffLimit" title="Permanent link">#</a> { #helm.hopsfs.namenode.setupBackOffLimit }
:   Type `int`, default `10`.
    Back off limit for database migration job. Default to be 10, i.e. 34 minutes, 30 seconds

`hopsfs.namenode.startupProbe.failureThreshold` <a class="headerlink" href="#helm.hopsfs.namenode.startupProbe.failureThreshold" title="Permanent link">#</a> { #helm.hopsfs.namenode.startupProbe.failureThreshold }
:   Type `int`, default `50`.

`hopsfs.namenode.startupProbe.initialDelaySeconds` <a class="headerlink" href="#helm.hopsfs.namenode.startupProbe.initialDelaySeconds" title="Permanent link">#</a> { #helm.hopsfs.namenode.startupProbe.initialDelaySeconds }
:   Type `int`, default `10`.

`hopsfs.namenode.startupProbe.periodSeconds` <a class="headerlink" href="#helm.hopsfs.namenode.startupProbe.periodSeconds" title="Permanent link">#</a> { #helm.hopsfs.namenode.startupProbe.periodSeconds }
:   Type `int`, default `15`.

`hopsfs.namenode.startupProbe.timeoutSeconds` <a class="headerlink" href="#helm.hopsfs.namenode.startupProbe.timeoutSeconds" title="Permanent link">#</a> { #helm.hopsfs.namenode.startupProbe.timeoutSeconds }
:   Type `int`, default `10`.

`hopsfs.namenode.stoCleanFaildOpsDelay` <a class="headerlink" href="#helm.hopsfs.namenode.stoCleanFaildOpsDelay" title="Permanent link">#</a> { #helm.hopsfs.namenode.stoCleanFaildOpsDelay }
:   Type `int`, default `600000`.

`hopsfs.namenode.stoCleanSlowOpsDelay` <a class="headerlink" href="#helm.hopsfs.namenode.stoCleanSlowOpsDelay" title="Permanent link">#</a> { #helm.hopsfs.namenode.stoCleanSlowOpsDelay }
:   Type `int`, default `900000`.

`hopsfs.namenode.subtreeExecutorCount` <a class="headerlink" href="#helm.hopsfs.namenode.subtreeExecutorCount" title="Permanent link">#</a> { #helm.hopsfs.namenode.subtreeExecutorCount }
:   Type `int`, default `40`.

`hopsfs.namenode.tls.extraDnsNames` <a class="headerlink" href="#helm.hopsfs.namenode.tls.extraDnsNames" title="Permanent link">#</a> { #helm.hopsfs.namenode.tls.extraDnsNames }
:   Type `list`, default `[]`.
    Additional DNS names to add as SAN to Datanode x.509 certificate

`hopsfs.namenode.tls.extraIpAddresses` <a class="headerlink" href="#helm.hopsfs.namenode.tls.extraIpAddresses" title="Permanent link">#</a> { #helm.hopsfs.namenode.tls.extraIpAddresses }
:   Type `list`, default `[]`.
    Additional IP addresses to add as SAN to Datanode x.509 certificate

`hopsfs.namenode.tolerations` <a class="headerlink" href="#helm.hopsfs.namenode.tolerations" title="Permanent link">#</a> { #helm.hopsfs.namenode.tolerations }
:   Type `list`, default `[]`.

`hopsfs.namenode.topologySpreadConstraint` <a class="headerlink" href="#helm.hopsfs.namenode.topologySpreadConstraint" title="Permanent link">#</a> { #helm.hopsfs.namenode.topologySpreadConstraint }
:   Type `object`, default `{}`.
    The default topology spread constraint. If not defined the global topology spread constraint would be used instead.

`hopsfs.namenode.txRetryCount` <a class="headerlink" href="#helm.hopsfs.namenode.txRetryCount" title="Permanent link">#</a> { #helm.hopsfs.namenode.txRetryCount }
:   Type `int`, default `10`.

`hopsfs.namenode.users[0].gid` <a class="headerlink" href="#helm.hopsfs.namenode.users.0.gid" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.0.gid }
:   Type `int`, default `1508`.

`hopsfs.namenode.users[0].group` <a class="headerlink" href="#helm.hopsfs.namenode.users.0.group" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.0.group }
:   Type `string`, default `"airflow"`.

`hopsfs.namenode.users[0].mode` <a class="headerlink" href="#helm.hopsfs.namenode.users.0.mode" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.0.mode }
:   Type `int`, default `1750`.

`hopsfs.namenode.users[0].name` <a class="headerlink" href="#helm.hopsfs.namenode.users.0.name" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.0.name }
:   Type `string`, default `"airflow"`.

`hopsfs.namenode.users[0].uid` <a class="headerlink" href="#helm.hopsfs.namenode.users.0.uid" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.0.uid }
:   Type `int`, default `1512`.

`hopsfs.namenode.users[1].extra_folders[0]` <a class="headerlink" href="#helm.hopsfs.namenode.users.1.extra_folders.0" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.1.extra_folders.0 }
:   Type `string`, default `"/user/spark/applicationHistory"`.

`hopsfs.namenode.users[1].extra_folders[1]` <a class="headerlink" href="#helm.hopsfs.namenode.users.1.extra_folders.1" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.1.extra_folders.1 }
:   Type `string`, default `"/user/spark/eventlog"`.

`hopsfs.namenode.users[1].extra_folders[2]` <a class="headerlink" href="#helm.hopsfs.namenode.users.1.extra_folders.2" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.1.extra_folders.2 }
:   Type `string`, default `"/user/spark/share"`.

`hopsfs.namenode.users[1].extra_folders[3]` <a class="headerlink" href="#helm.hopsfs.namenode.users.1.extra_folders.3" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.1.extra_folders.3 }
:   Type `string`, default `"/user/spark/spark-warehouse"`.

`hopsfs.namenode.users[1].group` <a class="headerlink" href="#helm.hopsfs.namenode.users.1.group" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.1.group }
:   Type `string`, default `"hadoop"`.

`hopsfs.namenode.users[1].mode` <a class="headerlink" href="#helm.hopsfs.namenode.users.1.mode" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.1.mode }
:   Type `int`, default `1777`.

`hopsfs.namenode.users[1].name` <a class="headerlink" href="#helm.hopsfs.namenode.users.1.name" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.1.name }
:   Type `string`, default `"spark"`.

`hopsfs.namenode.users[1].uid` <a class="headerlink" href="#helm.hopsfs.namenode.users.1.uid" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.1.uid }
:   Type `int`, default `1505`.

`hopsfs.namenode.users[2].extra_folders[0]` <a class="headerlink" href="#helm.hopsfs.namenode.users.2.extra_folders.0" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.2.extra_folders.0 }
:   Type `string`, default `"/apps/hive"`.

`hopsfs.namenode.users[2].extra_folders[1]` <a class="headerlink" href="#helm.hopsfs.namenode.users.2.extra_folders.1" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.2.extra_folders.1 }
:   Type `string`, default `"/apps/hive/warehouse"`.

`hopsfs.namenode.users[2].group` <a class="headerlink" href="#helm.hopsfs.namenode.users.2.group" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.2.group }
:   Type `string`, default `"hadoop"`.

`hopsfs.namenode.users[2].mode` <a class="headerlink" href="#helm.hopsfs.namenode.users.2.mode" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.2.mode }
:   Type `int`, default `1755`.

`hopsfs.namenode.users[2].name` <a class="headerlink" href="#helm.hopsfs.namenode.users.2.name" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.2.name }
:   Type `string`, default `"hive"`.

`hopsfs.namenode.users[3].group` <a class="headerlink" href="#helm.hopsfs.namenode.users.3.group" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.3.group }
:   Type `string`, default `"hdfs"`.

`hopsfs.namenode.users[3].mode` <a class="headerlink" href="#helm.hopsfs.namenode.users.3.mode" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.3.mode }
:   Type `int`, default `1750`.

`hopsfs.namenode.users[3].name` <a class="headerlink" href="#helm.hopsfs.namenode.users.3.name" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.3.name }
:   Type `string`, default `"payara"`.

`hopsfs.namenode.users[4].extra_folders[0]` <a class="headerlink" href="#helm.hopsfs.namenode.users.4.extra_folders.0" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.4.extra_folders.0 }
:   Type `string`, default `"/user/ray/applications"`.

`hopsfs.namenode.users[4].group` <a class="headerlink" href="#helm.hopsfs.namenode.users.4.group" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.4.group }
:   Type `string`, default `"hadoop"`.

`hopsfs.namenode.users[4].mode` <a class="headerlink" href="#helm.hopsfs.namenode.users.4.mode" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.4.mode }
:   Type `int`, default `1750`.

`hopsfs.namenode.users[4].name` <a class="headerlink" href="#helm.hopsfs.namenode.users.4.name" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.4.name }
:   Type `string`, default `"ray"`.

`hopsfs.namenode.users[5].group` <a class="headerlink" href="#helm.hopsfs.namenode.users.5.group" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.5.group }
:   Type `string`, default `"hdfs"`.

`hopsfs.namenode.users[5].mode` <a class="headerlink" href="#helm.hopsfs.namenode.users.5.mode" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.5.mode }
:   Type `int`, default `1750`.

`hopsfs.namenode.users[5].name` <a class="headerlink" href="#helm.hopsfs.namenode.users.5.name" title="Permanent link">#</a> { #helm.hopsfs.namenode.users.5.name }
:   Type `string`, default `"trino"`.

`hopsfs.namenode.xattrs.enabled` <a class="headerlink" href="#helm.hopsfs.namenode.xattrs.enabled" title="Permanent link">#</a> { #helm.hopsfs.namenode.xattrs.enabled }
:   Type `bool`, default `true`.

`hopsfs.namenode.xattrs.maxXAttrSize` <a class="headerlink" href="#helm.hopsfs.namenode.xattrs.maxXAttrSize" title="Permanent link">#</a> { #helm.hopsfs.namenode.xattrs.maxXAttrSize }
:   Type `int`, default `1039755`.

`hopsfs.namenode.xattrs.maxXAttrsPerInode` <a class="headerlink" href="#helm.hopsfs.namenode.xattrs.maxXAttrsPerInode" title="Permanent link">#</a> { #helm.hopsfs.namenode.xattrs.maxXAttrsPerInode }
:   Type `int`, default `32`.

`hopsfs.namenode.xmx` <a class="headerlink" href="#helm.hopsfs.namenode.xmx" title="Permanent link">#</a> { #helm.hopsfs.namenode.xmx }
:   Type `int`, default `1024`.

</div>

## objectStorage { #helm-values-hopsfs-objectstorage }

??? example "Defaults as YAML"

    ```yaml
    hopsfs:
      objectStorage:
        asyncUpload:
          enabled: false
        azure:
          storage:
            account: hopsfsdatastore
            container: hopsfs
            enableSoftDeletes: false
            identityClientId: 9cf39842-07c7-444a-8a44-63ee91411b70
            softDeletesRetentionDays: 90
        blockReportDelay: 21600000
        datanode:
          asyncUpload:
            queueCapacity: 1000
            retryCount: 3
            retryIntervalMs: 30000
            threads: 8
          cache:
            bypass: false
            deleteActivationPercentage: 70
            deleteWait: 1200000
          maxUploadThreads: 20
        enabled: true
        gcs:
          bucket:
            enableVersioning: true
            location: europe-north1
            name: hopsfs
        markBlocksCorruptOrMissingAfter: 3600000
        numCommittedAllowed: 1
        provider: ''
        restoreFromBackup: null
        s3:
          bucket:
            aclBucketOwnerFullControl: false
            encryption:
              bucketKeyEnabled: true
              enabled: false
              mode: SSE-KMS
              userKeyARN: ''
            name: ''
            versioning: null
          bypassGovernanceRetention: false
          credentialsSecret:
            access_key_id: ''
            name: ''
            secret_key_id: ''
          disableCertChecking: false
          disableChecksumValidation: false
          endpoint: null
          region: ''
          signingRegion: null
        storeSmallFilesInDB: false
    ```

<div class="hops-values" markdown>

`hopsfs.objectStorage.asyncUpload.enabled` <a class="headerlink" href="#helm.hopsfs.objectStorage.asyncUpload.enabled" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.asyncUpload.enabled }
:   Type `bool`, default `false`.
    Enable async cloud upload. dfs.cloud.async.upload.enabled (shared NN + DN scope)

`hopsfs.objectStorage.azure.storage.account` <a class="headerlink" href="#helm.hopsfs.objectStorage.azure.storage.account" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.azure.storage.account }
:   Type `string`, default `"hopsfsdatastore"`.

`hopsfs.objectStorage.azure.storage.container` <a class="headerlink" href="#helm.hopsfs.objectStorage.azure.storage.container" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.azure.storage.container }
:   Type `string`, default `"hopsfs"`.

`hopsfs.objectStorage.azure.storage.enableSoftDeletes` <a class="headerlink" href="#helm.hopsfs.objectStorage.azure.storage.enableSoftDeletes" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.azure.storage.enableSoftDeletes }
:   Type `bool`, default `false`.

`hopsfs.objectStorage.azure.storage.identityClientId` <a class="headerlink" href="#helm.hopsfs.objectStorage.azure.storage.identityClientId" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.azure.storage.identityClientId }
:   Type `string`, default `"9cf39842-07c7-444a-8a44-63ee91411b70"`.

`hopsfs.objectStorage.azure.storage.softDeletesRetentionDays` <a class="headerlink" href="#helm.hopsfs.objectStorage.azure.storage.softDeletesRetentionDays" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.azure.storage.softDeletesRetentionDays }
:   Type `int`, default `90`.

`hopsfs.objectStorage.blockReportDelay` <a class="headerlink" href="#helm.hopsfs.objectStorage.blockReportDelay" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.blockReportDelay }
:   Type `int`, default `21600000`.
    dfs.cloud.block.report.delay

`hopsfs.objectStorage.datanode.asyncUpload.queueCapacity` <a class="headerlink" href="#helm.hopsfs.objectStorage.datanode.asyncUpload.queueCapacity" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.datanode.asyncUpload.queueCapacity }
:   Type `int`, default `1000`.
    Bounded async-upload queue size; overflow triggers sync fallback. dfs.cloud.dn.async.upload.queue.capacity

`hopsfs.objectStorage.datanode.asyncUpload.retryCount` <a class="headerlink" href="#helm.hopsfs.objectStorage.datanode.asyncUpload.retryCount" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.datanode.asyncUpload.retryCount }
:   Type `int`, default `3`.
    Retry attempts before re-enqueueing a failed upload at queue tail. dfs.cloud.dn.async.upload.retry.count

`hopsfs.objectStorage.datanode.asyncUpload.retryIntervalMs` <a class="headerlink" href="#helm.hopsfs.objectStorage.datanode.asyncUpload.retryIntervalMs" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.datanode.asyncUpload.retryIntervalMs }
:   Type `int`, default `30000`.
    Base backoff in ms between retries (exponential, capped at 5 min). dfs.cloud.dn.async.upload.retry.interval.ms

`hopsfs.objectStorage.datanode.asyncUpload.threads` <a class="headerlink" href="#helm.hopsfs.objectStorage.datanode.asyncUpload.threads" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.datanode.asyncUpload.threads }
:   Type `int`, default `8`.
    Async-upload worker pool size. dfs.cloud.dn.async.upload.threads

`hopsfs.objectStorage.datanode.cache.bypass` <a class="headerlink" href="#helm.hopsfs.objectStorage.datanode.cache.bypass" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.datanode.cache.bypass }
:   Type `bool`, default `false`.

`hopsfs.objectStorage.datanode.cache.deleteActivationPercentage` <a class="headerlink" href="#helm.hopsfs.objectStorage.datanode.cache.deleteActivationPercentage" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.datanode.cache.deleteActivationPercentage }
:   Type `int`, default `70`.

`hopsfs.objectStorage.datanode.cache.deleteWait` <a class="headerlink" href="#helm.hopsfs.objectStorage.datanode.cache.deleteWait" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.datanode.cache.deleteWait }
:   Type `int`, default `1200000`.
    Minimum block file age in milliseconds before a cached block is eligible for deletion. Prevents removing newly downloaded blocks that may still be served to remote clients. dfs.dn.cloud.cache.delete.wait

`hopsfs.objectStorage.datanode.maxUploadThreads` <a class="headerlink" href="#helm.hopsfs.objectStorage.datanode.maxUploadThreads" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.datanode.maxUploadThreads }
:   Type `int`, default `20`.

`hopsfs.objectStorage.enabled` <a class="headerlink" href="#helm.hopsfs.objectStorage.enabled" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.enabled }
:   Type `bool`, default `true`.

`hopsfs.objectStorage.gcs.bucket.enableVersioning` <a class="headerlink" href="#helm.hopsfs.objectStorage.gcs.bucket.enableVersioning" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.gcs.bucket.enableVersioning }
:   Type `bool`, default `true`.

`hopsfs.objectStorage.gcs.bucket.location` <a class="headerlink" href="#helm.hopsfs.objectStorage.gcs.bucket.location" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.gcs.bucket.location }
:   Type `string`, default `"europe-north1"`.

`hopsfs.objectStorage.gcs.bucket.name` <a class="headerlink" href="#helm.hopsfs.objectStorage.gcs.bucket.name" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.gcs.bucket.name }
:   Type `string`, default `"hopsfs"`.

`hopsfs.objectStorage.markBlocksCorruptOrMissingAfter` <a class="headerlink" href="#helm.hopsfs.objectStorage.markBlocksCorruptOrMissingAfter" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.markBlocksCorruptOrMissingAfter }
:   Type `int`, default `3600000`.
    dfs.cloud.mark.blocks.corrupt.or.missing.after

`hopsfs.objectStorage.numCommittedAllowed` <a class="headerlink" href="#helm.hopsfs.objectStorage.numCommittedAllowed" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.numCommittedAllowed }
:   Type `int`, default `1`.
    When using cloud storage, setting this to 1 allows NN to verify a block on cloud instead of waiting for DN signal.

`hopsfs.objectStorage.provider` <a class="headerlink" href="#helm.hopsfs.objectStorage.provider" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.provider }
:   Type `string`, default `""`.
    object storage provicer, possible values are \["S3", "AZURE", "GCS"\]

`hopsfs.objectStorage.restoreFromBackup` <a class="headerlink" href="#helm.hopsfs.objectStorage.restoreFromBackup" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.restoreFromBackup }
:   Type `string`, default `nil`.
    restore from backup flag which instructs HopsFS to roll backed deleted blocks

`hopsfs.objectStorage.s3.bucket.aclBucketOwnerFullControl` <a class="headerlink" href="#helm.hopsfs.objectStorage.s3.bucket.aclBucketOwnerFullControl" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.s3.bucket.aclBucketOwnerFullControl }
:   Type `bool`, default `false`.

`hopsfs.objectStorage.s3.bucket.encryption.bucketKeyEnabled` <a class="headerlink" href="#helm.hopsfs.objectStorage.s3.bucket.encryption.bucketKeyEnabled" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.s3.bucket.encryption.bucketKeyEnabled }
:   Type `bool`, default `true`.

`hopsfs.objectStorage.s3.bucket.encryption.enabled` <a class="headerlink" href="#helm.hopsfs.objectStorage.s3.bucket.encryption.enabled" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.s3.bucket.encryption.enabled }
:   Type `bool`, default `false`.

`hopsfs.objectStorage.s3.bucket.encryption.mode` <a class="headerlink" href="#helm.hopsfs.objectStorage.s3.bucket.encryption.mode" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.s3.bucket.encryption.mode }
:   Type `string`, default `"SSE-KMS"`.
    s3 encryption mode, possible values are \[SSE-S3, SSE-KMS\]

`hopsfs.objectStorage.s3.bucket.encryption.userKeyARN` <a class="headerlink" href="#helm.hopsfs.objectStorage.s3.bucket.encryption.userKeyARN" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.s3.bucket.encryption.userKeyARN }
:   Type `string`, default `""`.

`hopsfs.objectStorage.s3.bucket.name` <a class="headerlink" href="#helm.hopsfs.objectStorage.s3.bucket.name" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.s3.bucket.name }
:   Type `string`, default `""`.

`hopsfs.objectStorage.s3.bucket.versioning` <a class="headerlink" href="#helm.hopsfs.objectStorage.s3.bucket.versioning" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.s3.bucket.versioning }
:   Type `string`, default `nil`.
    versioning is enabled or disabled. If global backup is enabled then versioning will be set to be enabled by default unless overriden on the HopsFS subchart. 

`hopsfs.objectStorage.s3.bypassGovernanceRetention` <a class="headerlink" href="#helm.hopsfs.objectStorage.s3.bypassGovernanceRetention" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.s3.bypassGovernanceRetention }
:   Type `bool`, default `false`.

`hopsfs.objectStorage.s3.credentialsSecret` <a class="headerlink" href="#helm.hopsfs.objectStorage.s3.credentialsSecret" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.s3.credentialsSecret }
:   Type `object`, default `{"access_key_id":"","name":"","secret_key_id":""}`.
    credentials secret configuration. If not defined the global._hopsworks.managedObjectStorage.s3.secret configuration will be used instead

`hopsfs.objectStorage.s3.credentialsSecret.access_key_id` <a class="headerlink" href="#helm.hopsfs.objectStorage.s3.credentialsSecret.access_key_id" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.s3.credentialsSecret.access_key_id }
:   Type `string`, default `""`.
    Defaults to access-key-id

`hopsfs.objectStorage.s3.credentialsSecret.name` <a class="headerlink" href="#helm.hopsfs.objectStorage.s3.credentialsSecret.name" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.s3.credentialsSecret.name }
:   Type `string`, default `""`.
    Default to aws-credentials

`hopsfs.objectStorage.s3.credentialsSecret.secret_key_id` <a class="headerlink" href="#helm.hopsfs.objectStorage.s3.credentialsSecret.secret_key_id" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.s3.credentialsSecret.secret_key_id }
:   Type `string`, default `""`.
    Defaults to secret-access-key

`hopsfs.objectStorage.s3.disableCertChecking` <a class="headerlink" href="#helm.hopsfs.objectStorage.s3.disableCertChecking" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.s3.disableCertChecking }
:   Type `bool`, default `false`.
    disable TLS certificate checking for the S3 endpoint (useful with self-signed certs / MinIO)

`hopsfs.objectStorage.s3.disableChecksumValidation` <a class="headerlink" href="#helm.hopsfs.objectStorage.s3.disableChecksumValidation" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.s3.disableChecksumValidation }
:   Type `bool`, default `false`.
    disable client-side checksum validation for S3 objects

`hopsfs.objectStorage.s3.endpoint` <a class="headerlink" href="#helm.hopsfs.objectStorage.s3.endpoint" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.s3.endpoint }
:   Type `string`, default `nil`.
    s3 provider endpoint

`hopsfs.objectStorage.s3.region` <a class="headerlink" href="#helm.hopsfs.objectStorage.s3.region" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.s3.region }
:   Type `string`, default `""`.

`hopsfs.objectStorage.s3.signingRegion` <a class="headerlink" href="#helm.hopsfs.objectStorage.s3.signingRegion" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.s3.signingRegion }
:   Type `string`, default `nil`.
    s3 provider signing region

`hopsfs.objectStorage.storeSmallFilesInDB` <a class="headerlink" href="#helm.hopsfs.objectStorage.storeSmallFilesInDB" title="Permanent link">#</a> { #helm.hopsfs.objectStorage.storeSmallFilesInDB }
:   Type `bool`, default `false`.

</div>

## security { #helm-values-hopsfs-security }

??? example "Defaults as YAML"

    ```yaml
    hopsfs:
      security:
        fsGroup: 1234
        runAsGroup: 1234
        runAsUser: 1506
        securityActions:
          maxConnectionsPerRoute: 30
        tde:
          enabled: false
          kmsUri: ''
        tls:
          enabled: true
    ```

<div class="hops-values" markdown>

`hopsfs.security.fsGroup` <a class="headerlink" href="#helm.hopsfs.security.fsGroup" title="Permanent link">#</a> { #helm.hopsfs.security.fsGroup }
:   Type `int`, default `1234`.

`hopsfs.security.runAsGroup` <a class="headerlink" href="#helm.hopsfs.security.runAsGroup" title="Permanent link">#</a> { #helm.hopsfs.security.runAsGroup }
:   Type `int`, default `1234`.

`hopsfs.security.runAsUser` <a class="headerlink" href="#helm.hopsfs.security.runAsUser" title="Permanent link">#</a> { #helm.hopsfs.security.runAsUser }
:   Type `int`, default `1506`.

`hopsfs.security.securityActions.maxConnectionsPerRoute` <a class="headerlink" href="#helm.hopsfs.security.securityActions.maxConnectionsPerRoute" title="Permanent link">#</a> { #helm.hopsfs.security.securityActions.maxConnectionsPerRoute }
:   Type `int`, default `30`.
    Maximum number of concurrent HTTP connections to Hopsworks CA. Currently used only by WebHDFS

`hopsfs.security.tde` <a class="headerlink" href="#helm.hopsfs.security.tde" title="Permanent link">#</a> { #helm.hopsfs.security.tde }
:   Type `object`, default `{"enabled":false,"kmsUri":""}`.
    Configuration for Transparent Data Encryption

`hopsfs.security.tde.enabled` <a class="headerlink" href="#helm.hopsfs.security.tde.enabled" title="Permanent link">#</a> { #helm.hopsfs.security.tde.enabled }
:   Type `bool`, default `false`.
    Flag to enable encryption-at-rest

`hopsfs.security.tde.kmsUri` <a class="headerlink" href="#helm.hopsfs.security.tde.kmsUri" title="Permanent link">#</a> { #helm.hopsfs.security.tde.kmsUri }
:   Type `string`, default `""`.
    KMS URI when encryption-at-rest is enabled ie <http://10.1.1.2:9600>

`hopsfs.security.tls.enabled` <a class="headerlink" href="#helm.hopsfs.security.tls.enabled" title="Permanent link">#</a> { #helm.hopsfs.security.tls.enabled }
:   Type `bool`, default `true`.

</div>

<!-- END GENERATED VALUES -->
