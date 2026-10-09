# Spark values { #helm-values-spark }

Values under `spark` configure the Spark operator, the Spark history server and the remote shuffle service.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.2.0-alpha-1791567888` (Hopsworks `5.2.0`)._

Deployed when [`global._hopsworks.full_platform`](global.md#helm.global._hopsworks.full_platform) is `true`.

!!! info "Upstream charts"

    - Values under `spark.spark-operator` go to [`spark-operator` 2.5.1](https://github.com/kubeflow/spark-operator/blob/v2.5.1/charts/spark-operator-chart/README.md) from `https://kubeflow.github.io/spark-operator/`.

    Only the values Hopsworks sets under `spark.spark-operator` are listed on this page.
    Any other value of the chart can be set there too; the link opens its documentation for the version Hopsworks pins.

## General { #helm-values-spark-general }

??? example "Defaults as YAML"

    ```yaml
    spark:
      cleanupOnUninstall:
        enabled: true
        ttlSecondsAfterFinished: null
      historyServer:
        certsDir: /srv/hops/super_crypto/spark
        cleaner:
          enabled: true
          interval: 1d
          maxAge: 7d
        deploymentName: spark-history-server-deployment
        hadoopHome: /srv/hops/hadoop
        image:
          pullPolicy: Always
          repository: sparkhistoryserver
          tag: 4.1.3.0
        name: spark-history-server
        nodeSelector: {}
        probes:
          liveness:
            failureThreshold: 10
            httpGet:
              path: /
              port: http
              scheme: HTTPS
            initialDelaySeconds: 8
            periodSeconds: 5
            timeoutSeconds: 10
          readiness:
            failureThreshold: 10
            httpGet:
              path: /
              port: http
              scheme: HTTPS
            initialDelaySeconds: 8
            periodSeconds: 5
            timeoutSeconds: 10
        replicaCount: 1
        resources:
          limits:
            cpu: 2000m
            memory: 3Gi
          requests:
            cpu: 500m
            memory: 1Gi
        service:
          annotations:
            consul.hashicorp.com/service-name: sparkhistoryserver
          externalPort: 80
          internalPort: 18080
          name: sparkhistoryserver
          type: ClusterIP
        sparkHome: /srv/hops/spark
        tolerations: []
        topologySpreadConstraint: {}
      hopsworkslib: {}
      sparkJobDebugLevel: INFO
      sql:
        ansiEnabled: false
    ```

<div class="hops-values" markdown>

`spark` <a class="headerlink" href="#helm.spark" title="Permanent link">#</a> { #helm.spark }
:   Type `object`, default `{}`.
    override spark values

`spark.cleanupOnUninstall` <a class="headerlink" href="#helm.spark.cleanupOnUninstall" title="Permanent link">#</a> { #helm.spark.cleanupOnUninstall }
:   Type `object`, default `{"enabled":true,"ttlSecondsAfterFinished":null}`.
    post-delete cleanup of Spark/RSS leftovers: the spark-operator and rss-webhook TLS Secrets (generated at runtime by the operators, not Helm-tracked), and the rss shuffle-server data PVCs. PVCs are only deleted when global._hopsworks.wipeDataOnUninstall is enabled and never for PVCs labelled hopsworks.ai/keep=true.

`spark.cleanupOnUninstall.enabled` <a class="headerlink" href="#helm.spark.cleanupOnUninstall.enabled" title="Permanent link">#</a> { #helm.spark.cleanupOnUninstall.enabled }
:   Type `bool`, default `true`.
    enable the post-delete Spark/RSS cleanup hook

`spark.cleanupOnUninstall.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.spark.cleanupOnUninstall.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.spark.cleanupOnUninstall.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    ttlSecondsAfterFinished for the cleanup Job; null falls through to the global default

`spark.historyServer` <a class="headerlink" href="#helm.spark.historyServer" title="Permanent link">#</a> { #helm.spark.historyServer }
:   Type `object`.
    The configuration for the Spark history server

    ??? note "Default"

        ```yaml
        certsDir: /srv/hops/super_crypto/spark
        cleaner:
          enabled: true
          interval: 1d
          maxAge: 7d
        deploymentName: spark-history-server-deployment
        hadoopHome: /srv/hops/hadoop
        image:
          pullPolicy: Always
          repository: sparkhistoryserver
          tag: 4.1.3.0
        name: spark-history-server
        nodeSelector: {}
        probes:
          liveness:
            failureThreshold: 10
            httpGet:
              path: /
              port: http
              scheme: HTTPS
            initialDelaySeconds: 8
            periodSeconds: 5
            timeoutSeconds: 10
          readiness:
            failureThreshold: 10
            httpGet:
              path: /
              port: http
              scheme: HTTPS
            initialDelaySeconds: 8
            periodSeconds: 5
            timeoutSeconds: 10
        replicaCount: 1
        resources:
          limits:
            cpu: 2000m
            memory: 3Gi
          requests:
            cpu: 500m
            memory: 1Gi
        service:
          annotations:
            consul.hashicorp.com/service-name: sparkhistoryserver
          externalPort: 80
          internalPort: 18080
          name: sparkhistoryserver
          type: ClusterIP
        sparkHome: /srv/hops/spark
        tolerations: []
        topologySpreadConstraint: {}
        ```

`spark.historyServer.nodeSelector` <a class="headerlink" href="#helm.spark.historyServer.nodeSelector" title="Permanent link">#</a> { #helm.spark.historyServer.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

`spark.historyServer.topologySpreadConstraint` <a class="headerlink" href="#helm.spark.historyServer.topologySpreadConstraint" title="Permanent link">#</a> { #helm.spark.historyServer.topologySpreadConstraint }
:   Type `object`, default `{}`.
    The default topology spread constraint. If not defined the global topology spread constraint would be used instead.

`spark.hopsworkslib` <a class="headerlink" href="#helm.spark.hopsworkslib" title="Permanent link">#</a> { #helm.spark.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`spark.sparkJobDebugLevel` <a class="headerlink" href="#helm.spark.sparkJobDebugLevel" title="Permanent link">#</a> { #helm.spark.sparkJobDebugLevel }
:   Type `string`, default `"INFO"`.

`spark.sql` <a class="headerlink" href="#helm.spark.sql" title="Permanent link">#</a> { #helm.spark.sql }
:   Type `object`, default `{"ansiEnabled":false}`.
    Spark SQL defaults applied cluster-wide through `spark-defaults.conf`.

`spark.sql.ansiEnabled` <a class="headerlink" href="#helm.spark.sql.ansiEnabled" title="Permanent link">#</a> { #helm.spark.sql.ansiEnabled }
:   Type `bool`, default `false`.
    Whether to enable ANSI SQL mode (`spark.sql.ansi.enabled`). Spark 4 changed the upstream default to `true`, which turns arithmetic overflow and invalid casts into runtime errors instead of returning `null`. Hopsworks pins it to `false` so SQL that ran on Spark 3.x keeps the same semantics after the upgrade. Set to `true` to opt in to standards-compliant behavior cluster-wide; individual jobs can still override `spark.sql.ansi.enabled` themselves.

</div>

## dependencies { #helm-values-spark-dependencies }

??? example "Defaults as YAML"

    ```yaml
    spark:
      dependencies:
        hive:
          consulServiceName: hive
          consulServiceTag: metastore
          port: 9083
        namenode:
          consulServiceName: namenode
          consulServiceTag: rpc
          port: 8020
        prometheusPushgateway:
          consulServiceName: prometheus
          consulServiceTag: pushgateway
          port: 9091
          protocol: http
    ```

<div class="hops-values" markdown>

`spark.dependencies.hive.consulServiceName` <a class="headerlink" href="#helm.spark.dependencies.hive.consulServiceName" title="Permanent link">#</a> { #helm.spark.dependencies.hive.consulServiceName }
:   Type `string`, default `"hive"`.

`spark.dependencies.hive.consulServiceTag` <a class="headerlink" href="#helm.spark.dependencies.hive.consulServiceTag" title="Permanent link">#</a> { #helm.spark.dependencies.hive.consulServiceTag }
:   Type `string`, default `"metastore"`.

`spark.dependencies.hive.port` <a class="headerlink" href="#helm.spark.dependencies.hive.port" title="Permanent link">#</a> { #helm.spark.dependencies.hive.port }
:   Type `int`, default `9083`.

`spark.dependencies.namenode.consulServiceName` <a class="headerlink" href="#helm.spark.dependencies.namenode.consulServiceName" title="Permanent link">#</a> { #helm.spark.dependencies.namenode.consulServiceName }
:   Type `string`, default `"namenode"`.

`spark.dependencies.namenode.consulServiceTag` <a class="headerlink" href="#helm.spark.dependencies.namenode.consulServiceTag" title="Permanent link">#</a> { #helm.spark.dependencies.namenode.consulServiceTag }
:   Type `string`, default `"rpc"`.

`spark.dependencies.namenode.port` <a class="headerlink" href="#helm.spark.dependencies.namenode.port" title="Permanent link">#</a> { #helm.spark.dependencies.namenode.port }
:   Type `int`, default `8020`.

`spark.dependencies.prometheusPushgateway.consulServiceName` <a class="headerlink" href="#helm.spark.dependencies.prometheusPushgateway.consulServiceName" title="Permanent link">#</a> { #helm.spark.dependencies.prometheusPushgateway.consulServiceName }
:   Type `string`, default `"prometheus"`.

`spark.dependencies.prometheusPushgateway.consulServiceTag` <a class="headerlink" href="#helm.spark.dependencies.prometheusPushgateway.consulServiceTag" title="Permanent link">#</a> { #helm.spark.dependencies.prometheusPushgateway.consulServiceTag }
:   Type `string`, default `"pushgateway"`.

`spark.dependencies.prometheusPushgateway.port` <a class="headerlink" href="#helm.spark.dependencies.prometheusPushgateway.port" title="Permanent link">#</a> { #helm.spark.dependencies.prometheusPushgateway.port }
:   Type `int`, default `9091`.

`spark.dependencies.prometheusPushgateway.protocol` <a class="headerlink" href="#helm.spark.dependencies.prometheusPushgateway.protocol" title="Permanent link">#</a> { #helm.spark.dependencies.prometheusPushgateway.protocol }
:   Type `string`, default `"http"`.

</div>

## rss { #helm-values-spark-rss }

??? example "Defaults as YAML"

    ```yaml
    spark:
      rss:
        appName: rss-hops
        configDir: /data/rssadmin/rss/conf
        configmap:
          name: rss-configuration
        controller:
          containerPort: 9876
          image: rss-controller
          replicas: 1
          resources:
            limits:
              cpu: '1'
              memory: 512Mi
            requests:
              cpu: 100m
              memory: 150Mi
          serviceAccount:
            annotations: {}
        coordinator:
          count: 2
          dynamicClientConfigMapName: rss-dynamic-client-configuration
          dynamicClientConfigMountPath: /tmp
          httpPort: 19996
          labels:
            role: rss-hops-coordinator
          replicas: 1
          resources:
            limits:
              cpu: 500m
              memory: 2Gi
            requests:
              cpu: 500m
          rpcPort: 19997
          xmxSizeMemoryExtraPercentage: 30
        dashboard:
          enabled: false
          httpPort: 19997
          name: uniffle-dashboard
          resources:
            limits:
              cpu: 500m
              memory: 2Gi
            requests:
              cpu: 250m
          xmxSizeMemoryExtraPercentage: 30
        dynamicClient:
          readBufferSize: 14m
          storageType: MEMORY_LOCALFILE
        fullnameOverride: null
        image:
          image: rss
          initImage: hops-rss-init
          initImageVersion: 0.9.2
          pullPolicy: Always
        namespaceSelector: ''
        nodeSelector: {}
        resources:
          jobs:
            limits:
              cpu: 200m
          rss:
            limits:
              cpu: 500m
              memory: 1Gi
        serviceAccount:
          annotations: {}
        shuffleServer:
          bufferCapacity: -1
          bufferCapacityRatio: 0.6
          diskCapacity: -1
          diskCapacityRatio: 0.8
          httpPort: 19998
          nettyPort: 20000
          readBufferCapacity: -1
          readBufferCapacityRatio: 0.1
          replicas: 3
          resources:
            limits:
              cpu: 2000m
              memory: 3Gi
            requests:
              cpu: 200m
          rpcPort: 19999
          upgradeStrategy: FullUpgrade
        storage:
          size: 10Gi
          storageClassName: null
          volumeNameTemplate: rss-storage
        tolerations: []
        topologySpreadConstraint: {}
        ttlSecondsAfterFinished: null
        version: 0.11.1
        webhook:
          app: rss-webhook
          resources:
            limits:
              cpu: '1'
              memory: 512Mi
            requests:
              cpu: 100m
              memory: 150Mi
          service:
            name: rss-webhook
            port: 443
            targetPort: 9876
        webhookName: rss-webhook
    ```

<div class="hops-values" markdown>

`spark.rss` <a class="headerlink" href="#helm.spark.rss" title="Permanent link">#</a> { #helm.spark.rss }
:   Type `object`.
    The configuration for the uniffle remote shuffle service

    ??? note "Default"

        ```yaml
        appName: rss-hops
        configDir: /data/rssadmin/rss/conf
        configmap:
          name: rss-configuration
        controller:
          containerPort: 9876
          image: rss-controller
          replicas: 1
          resources:
            limits:
              cpu: '1'
              memory: 512Mi
            requests:
              cpu: 100m
              memory: 150Mi
          serviceAccount:
            annotations: {}
        coordinator:
          count: 2
          dynamicClientConfigMapName: rss-dynamic-client-configuration
          dynamicClientConfigMountPath: /tmp
          httpPort: 19996
          labels:
            role: rss-hops-coordinator
          replicas: 1
          resources:
            limits:
              cpu: 500m
              memory: 2Gi
            requests:
              cpu: 500m
          rpcPort: 19997
          xmxSizeMemoryExtraPercentage: 30
        dashboard:
          enabled: false
          httpPort: 19997
          name: uniffle-dashboard
          resources:
            limits:
              cpu: 500m
              memory: 2Gi
            requests:
              cpu: 250m
          xmxSizeMemoryExtraPercentage: 30
        dynamicClient:
          readBufferSize: 14m
          storageType: MEMORY_LOCALFILE
        fullnameOverride: null
        image:
          image: rss
          initImage: hops-rss-init
          initImageVersion: 0.9.2
          pullPolicy: Always
        namespaceSelector: ''
        nodeSelector: {}
        resources:
          jobs:
            limits:
              cpu: 200m
          rss:
            limits:
              cpu: 500m
              memory: 1Gi
        serviceAccount:
          annotations: {}
        shuffleServer:
          bufferCapacity: -1
          bufferCapacityRatio: 0.6
          diskCapacity: -1
          diskCapacityRatio: 0.8
          httpPort: 19998
          nettyPort: 20000
          readBufferCapacity: -1
          readBufferCapacityRatio: 0.1
          replicas: 3
          resources:
            limits:
              cpu: 2000m
              memory: 3Gi
            requests:
              cpu: 200m
          rpcPort: 19999
          upgradeStrategy: FullUpgrade
        storage:
          size: 10Gi
          storageClassName: null
          volumeNameTemplate: rss-storage
        tolerations: []
        topologySpreadConstraint: {}
        ttlSecondsAfterFinished: null
        version: 0.11.1
        webhook:
          app: rss-webhook
          resources:
            limits:
              cpu: '1'
              memory: 512Mi
            requests:
              cpu: 100m
              memory: 150Mi
          service:
            name: rss-webhook
            port: 443
            targetPort: 9876
        webhookName: rss-webhook
        ```

`spark.rss.controller.serviceAccount.annotations` <a class="headerlink" href="#helm.spark.rss.controller.serviceAccount.annotations" title="Permanent link">#</a> { #helm.spark.rss.controller.serviceAccount.annotations }
:   Type `object`, default `{}`.
    service account annotations

`spark.rss.coordinator.resources.requests` <a class="headerlink" href="#helm.spark.rss.coordinator.resources.requests" title="Permanent link">#</a> { #helm.spark.rss.coordinator.resources.requests }
:   Type `object`, default `{"cpu":"500m"}`.
    memory is set to be equal to the limit 

`spark.rss.dashboard.resources.requests` <a class="headerlink" href="#helm.spark.rss.dashboard.resources.requests" title="Permanent link">#</a> { #helm.spark.rss.dashboard.resources.requests }
:   Type `object`, default `{"cpu":"250m"}`.
    memory is set to be equal to the limit 

`spark.rss.fullnameOverride` <a class="headerlink" href="#helm.spark.rss.fullnameOverride" title="Permanent link">#</a> { #helm.spark.rss.fullnameOverride }
:   Type `string`, default `nil`.
    fullnameOverride

`spark.rss.namespaceSelector` <a class="headerlink" href="#helm.spark.rss.namespaceSelector" title="Permanent link">#</a> { #helm.spark.rss.namespaceSelector }
:   Type `string`, default `""`.
    Label selector (key=value or key1=value1,key2=value2) for namespaces this instance should manage. Only events from matching namespaces will be processed by the controller and webhook. If empty, all namespaces are managed.

`spark.rss.nodeSelector` <a class="headerlink" href="#helm.spark.rss.nodeSelector" title="Permanent link">#</a> { #helm.spark.rss.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

`spark.rss.resources.jobs` <a class="headerlink" href="#helm.spark.rss.resources.jobs" title="Permanent link">#</a> { #helm.spark.rss.resources.jobs }
:   Type `object`, default `{"limits":{"cpu":"200m"}}`.
    jobs resources

`spark.rss.resources.rss` <a class="headerlink" href="#helm.spark.rss.resources.rss" title="Permanent link">#</a> { #helm.spark.rss.resources.rss }
:   Type `object`, default `{"limits":{"cpu":"500m","memory":"1Gi"}}`.
    rss resources

`spark.rss.serviceAccount.annotations` <a class="headerlink" href="#helm.spark.rss.serviceAccount.annotations" title="Permanent link">#</a> { #helm.spark.rss.serviceAccount.annotations }
:   Type `object`, default `{}`.
    service account annotations

`spark.rss.shuffleServer.resources.requests` <a class="headerlink" href="#helm.spark.rss.shuffleServer.resources.requests" title="Permanent link">#</a> { #helm.spark.rss.shuffleServer.resources.requests }
:   Type `object`, default `{"cpu":"200m"}`.
    memory is set to be equal to the limit 

`spark.rss.storage.storageClassName` <a class="headerlink" href="#helm.spark.rss.storage.storageClassName" title="Permanent link">#</a> { #helm.spark.rss.storage.storageClassName }
:   Type `string`, default `nil`.
    storage class name to request for volumes attached to rss

`spark.rss.topologySpreadConstraint` <a class="headerlink" href="#helm.spark.rss.topologySpreadConstraint" title="Permanent link">#</a> { #helm.spark.rss.topologySpreadConstraint }
:   Type `object`, default `{}`.
    The default topology spread constraint. If not defined the global topology spread constraint would be used instead.

`spark.rss.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.spark.rss.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.spark.rss.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    TTL in seconds for the rss-config Job. Overrides global default.

`spark.rss.webhookName` <a class="headerlink" href="#helm.spark.rss.webhookName" title="Permanent link">#</a> { #helm.spark.rss.webhookName }
:   Type `string`, default `"rss-webhook"`.
    Name of the MutatingWebhookConfiguration and ValidatingWebhookConfiguration. Override when running multiple instances on the same cluster to avoid name collisions.

</div>

## spark-operator { #helm-values-spark-spark-operator }

??? example "Defaults as YAML"

    ```yaml
    spark:
      spark-operator:
        certManager:
          duration: ''
          enable: false
          issuerRef: {}
          renewBefore: ''
        commonLabels: {}
        controller:
          affinity: {}
          annotations: {}
          batchScheduler:
            default: ''
            enable: false
            kubeSchedulerNames: []
          driverPodCreationGracePeriod: 10s
          env: []
          envFrom: []
          labels: {}
          leaderElection:
            enable: true
          logLevel: info
          maxTrackedExecutorPerApp: 1000
          nodeSelector: {}
          podDisruptionBudget:
            enable: false
            minAvailable: 1
          podSecurityContext:
            fsGroup: 185
          pprof:
            enable: false
            port: 6060
            portName: pprof
          priorityClassName: ''
          rbac:
            annotations: {}
            create: true
          replicas: 1
          resources:
            requests:
              cpu: 300m
              memory: 512Mi
          securityContext:
            allowPrivilegeEscalation: false
            capabilities:
              drop:
              - ALL
            privileged: false
            readOnlyRootFilesystem: true
            runAsNonRoot: true
            seccompProfile:
              type: RuntimeDefault
          serviceAccount:
            annotations: {}
            automountServiceAccountToken: true
            create: true
            name: ''
          sidecars: []
          tolerations: []
          topologySpreadConstraints: []
          uiIngress:
            annotations: {}
            enable: false
            ingressClassName: ''
            tls: []
            urlFormat: ''
          uiService:
            enable: true
          volumeMounts:
          - mountPath: /tmp
            name: tmp
            readOnly: false
          volumes:
          - emptyDir:
              sizeLimit: 1Gi
            name: tmp
          workers: 10
          workqueueRateLimiter:
            bucketQPS: 50
            bucketSize: 500
            maxDelay:
              duration: 6h
              enable: true
        fullnameOverride: ''
        hook:
          affinity: {}
          image:
            registry: docker.hops.works
            repository: hopsworks/spark-operator-crds
            tag: 2.5.1-h1-1.9
          nodeSelector: {}
          tolerations: []
          upgradeCrd: true
        image:
          pullPolicy: IfNotPresent
          pullSecrets: []
          registry: docker.hops.works
          repository: hopsworks/spark-operator
          tag: 2.5.1-h1
        nameOverride: ''
        podSecurityContext:
          fsGroup: 185
          runAsGroup: 185
          runAsNonRoot: true
          runAsUser: 185
          seccompProfile:
            type: RuntimeDefault
        prometheus:
          metrics:
            enable: true
            endpoint: /metrics
            jobStartLatencyBuckets: 30,60,90,120,150,180,210,240,270,300
            port: 8080
            portName: metrics
            prefix: ''
          podMonitor:
            create: false
            jobLabel: spark-operator-podmonitor
            labels: {}
            podMetricsEndpoint:
              interval: 5s
              scheme: http
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL
          runAsGroup: 185
          runAsNonRoot: true
          runAsUser: 185
          seccompProfile:
            type: RuntimeDefault
        spark:
          jobNamespaces: []
          rbac:
            annotations: {}
            create: true
          serviceAccount:
            annotations: {}
            automountServiceAccountToken: true
            create: true
            name: ''
        webhook:
          affinity: {}
          annotations: {}
          enable: true
          env: []
          envFrom: []
          failurePolicy: Fail
          labels: {}
          leaderElection:
            enable: true
          logLevel: info
          nodeSelector: {}
          podDisruptionBudget:
            enable: false
            minAvailable: 1
          podSecurityContext:
            fsGroup: 185
          port: 9443
          portName: webhook
          priorityClassName: ''
          rbac:
            annotations: {}
            create: true
          replicas: 1
          resourceQuotaEnforcement:
            enable: false
          resources:
            requests:
              cpu: 300m
              memory: 512Mi
          securityContext:
            allowPrivilegeEscalation: false
            capabilities:
              drop:
              - ALL
            privileged: false
            readOnlyRootFilesystem: true
            runAsNonRoot: true
            seccompProfile:
              type: RuntimeDefault
          serviceAccount:
            annotations: {}
            automountServiceAccountToken: true
            create: true
            name: ''
          sidecars: []
          timeoutSeconds: 10
          tolerations: []
          topologySpreadConstraints: []
          volumeMounts:
          - mountPath: /etc/k8s-webhook-server/serving-certs
            name: serving-certs
            readOnly: false
            subPath: serving-certs
          - mountPath: /tmp
            name: tmp
          volumes:
          - emptyDir:
              sizeLimit: 500Mi
            name: serving-certs
          - emptyDir: {}
            name: tmp
    ```

<div class="hops-values" markdown>

`spark.spark-operator` <a class="headerlink" href="#helm.spark.spark-operator" title="Permanent link">#</a> { #helm.spark.spark-operator }
:   Type `object`, passed to the [`spark-operator` 2.5.1](https://github.com/kubeflow/spark-operator/blob/v2.5.1/charts/spark-operator-chart/README.md) chart, whose other values are documented there.
    override spark operator values

    ??? note "Default"

        ```yaml
        certManager:
          duration: ''
          enable: false
          issuerRef: {}
          renewBefore: ''
        commonLabels: {}
        controller:
          affinity: {}
          annotations: {}
          batchScheduler:
            default: ''
            enable: false
            kubeSchedulerNames: []
          driverPodCreationGracePeriod: 10s
          env: []
          envFrom: []
          labels: {}
          leaderElection:
            enable: true
          logLevel: info
          maxTrackedExecutorPerApp: 1000
          nodeSelector: {}
          podDisruptionBudget:
            enable: false
            minAvailable: 1
          podSecurityContext:
            fsGroup: 185
          pprof:
            enable: false
            port: 6060
            portName: pprof
          priorityClassName: ''
          rbac:
            annotations: {}
            create: true
          replicas: 1
          resources:
            requests:
              cpu: 300m
              memory: 512Mi
          securityContext:
            allowPrivilegeEscalation: false
            capabilities:
              drop:
              - ALL
            privileged: false
            readOnlyRootFilesystem: true
            runAsNonRoot: true
            seccompProfile:
              type: RuntimeDefault
          serviceAccount:
            annotations: {}
            automountServiceAccountToken: true
            create: true
            name: ''
          sidecars: []
          tolerations: []
          topologySpreadConstraints: []
          uiIngress:
            annotations: {}
            enable: false
            ingressClassName: ''
            tls: []
            urlFormat: ''
          uiService:
            enable: true
          volumeMounts:
          - mountPath: /tmp
            name: tmp
            readOnly: false
          volumes:
          - emptyDir:
              sizeLimit: 1Gi
            name: tmp
          workers: 10
          workqueueRateLimiter:
            bucketQPS: 50
            bucketSize: 500
            maxDelay:
              duration: 6h
              enable: true
        fullnameOverride: ''
        hook:
          affinity: {}
          image:
            registry: docker.hops.works
            repository: hopsworks/spark-operator-crds
            tag: 2.5.1-h1-1.9
          nodeSelector: {}
          tolerations: []
          upgradeCrd: true
        image:
          pullPolicy: IfNotPresent
          pullSecrets: []
          registry: docker.hops.works
          repository: hopsworks/spark-operator
          tag: 2.5.1-h1
        nameOverride: ''
        podSecurityContext:
          fsGroup: 185
          runAsGroup: 185
          runAsNonRoot: true
          runAsUser: 185
          seccompProfile:
            type: RuntimeDefault
        prometheus:
          metrics:
            enable: true
            endpoint: /metrics
            jobStartLatencyBuckets: 30,60,90,120,150,180,210,240,270,300
            port: 8080
            portName: metrics
            prefix: ''
          podMonitor:
            create: false
            jobLabel: spark-operator-podmonitor
            labels: {}
            podMetricsEndpoint:
              interval: 5s
              scheme: http
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL
          runAsGroup: 185
          runAsNonRoot: true
          runAsUser: 185
          seccompProfile:
            type: RuntimeDefault
        spark:
          jobNamespaces: []
          rbac:
            annotations: {}
            create: true
          serviceAccount:
            annotations: {}
            automountServiceAccountToken: true
            create: true
            name: ''
        webhook:
          affinity: {}
          annotations: {}
          enable: true
          env: []
          envFrom: []
          failurePolicy: Fail
          labels: {}
          leaderElection:
            enable: true
          logLevel: info
          nodeSelector: {}
          podDisruptionBudget:
            enable: false
            minAvailable: 1
          podSecurityContext:
            fsGroup: 185
          port: 9443
          portName: webhook
          priorityClassName: ''
          rbac:
            annotations: {}
            create: true
          replicas: 1
          resourceQuotaEnforcement:
            enable: false
          resources:
            requests:
              cpu: 300m
              memory: 512Mi
          securityContext:
            allowPrivilegeEscalation: false
            capabilities:
              drop:
              - ALL
            privileged: false
            readOnlyRootFilesystem: true
            runAsNonRoot: true
            seccompProfile:
              type: RuntimeDefault
          serviceAccount:
            annotations: {}
            automountServiceAccountToken: true
            create: true
            name: ''
          sidecars: []
          timeoutSeconds: 10
          tolerations: []
          topologySpreadConstraints: []
          volumeMounts:
          - mountPath: /etc/k8s-webhook-server/serving-certs
            name: serving-certs
            readOnly: false
            subPath: serving-certs
          - mountPath: /tmp
            name: tmp
          volumes:
          - emptyDir:
              sizeLimit: 500Mi
            name: serving-certs
          - emptyDir: {}
            name: tmp
        ```

`spark.spark-operator.certManager.duration` <a class="headerlink" href="#helm.spark.spark-operator.certManager.duration" title="Permanent link">#</a> { #helm.spark.spark-operator.certManager.duration }
:   Type `string`, default `2160h` (90 days) will be used if not specified..
    The duration of the certificate validity (e.g. `2160h`). See [cert-manager.io/v1.Certificate](https://cert-manager.io/docs/reference/api-docs/#cert-manager.io/v1.Certificate).

`spark.spark-operator.certManager.enable` <a class="headerlink" href="#helm.spark.spark-operator.certManager.enable" title="Permanent link">#</a> { #helm.spark.spark-operator.certManager.enable }
:   Type `bool`, default `false`.
    Specifies whether to use [cert-manager](https://cert-manager.io) to generate certificate for webhook. `webhook.enable` must be set to `true` to enable cert-manager.

`spark.spark-operator.certManager.issuerRef` <a class="headerlink" href="#helm.spark.spark-operator.certManager.issuerRef" title="Permanent link">#</a> { #helm.spark.spark-operator.certManager.issuerRef }
:   Type `object`, default A self-signed issuer will be created and used if not specified..
    The reference to the issuer.

`spark.spark-operator.certManager.renewBefore` <a class="headerlink" href="#helm.spark.spark-operator.certManager.renewBefore" title="Permanent link">#</a> { #helm.spark.spark-operator.certManager.renewBefore }
:   Type `string`, default 1/3 of issued certificate’s lifetime..
    The duration before the certificate expiration to renew the certificate (e.g. `720h`). See [cert-manager.io/v1.Certificate](https://cert-manager.io/docs/reference/api-docs/#cert-manager.io/v1.Certificate).

`spark.spark-operator.commonLabels` <a class="headerlink" href="#helm.spark.spark-operator.commonLabels" title="Permanent link">#</a> { #helm.spark.spark-operator.commonLabels }
:   Type `object`, default `{}`.
    Common labels to add to the resources.

`spark.spark-operator.controller.affinity` <a class="headerlink" href="#helm.spark.spark-operator.controller.affinity" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.affinity }
:   Type `object`, default `{}`.
    Affinity for controller pods.

`spark.spark-operator.controller.annotations` <a class="headerlink" href="#helm.spark.spark-operator.controller.annotations" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.annotations }
:   Type `object`, default `{}`.
    Extra annotations for controller pods.

`spark.spark-operator.controller.batchScheduler.default` <a class="headerlink" href="#helm.spark.spark-operator.controller.batchScheduler.default" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.batchScheduler.default }
:   Type `string`, default `""`.
    Default batch scheduler to be used if not specified by the user. If specified, this value must be either "volcano" or "yunikorn". Specifying any other value will cause the controller to error on startup.

`spark.spark-operator.controller.batchScheduler.enable` <a class="headerlink" href="#helm.spark.spark-operator.controller.batchScheduler.enable" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.batchScheduler.enable }
:   Type `bool`, default `false`.
    Specifies whether to enable batch scheduler for spark jobs scheduling. If enabled, users can specify batch scheduler name in spark application.

`spark.spark-operator.controller.batchScheduler.kubeSchedulerNames` <a class="headerlink" href="#helm.spark.spark-operator.controller.batchScheduler.kubeSchedulerNames" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.batchScheduler.kubeSchedulerNames }
:   Type `list`, default `[]`.
    Specifies a list of kube-scheduler names for scheduling Spark pods.

`spark.spark-operator.controller.driverPodCreationGracePeriod` <a class="headerlink" href="#helm.spark.spark-operator.controller.driverPodCreationGracePeriod" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.driverPodCreationGracePeriod }
:   Type `string`, default `"10s"`.
    Grace period after a successful spark-submit when driver pod not found errors will be retried. Useful if the driver pod can take some time to be created.

`spark.spark-operator.controller.env` <a class="headerlink" href="#helm.spark.spark-operator.controller.env" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.env }
:   Type `list`, default `[]`.
    Environment variables for controller containers.

`spark.spark-operator.controller.envFrom` <a class="headerlink" href="#helm.spark.spark-operator.controller.envFrom" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.envFrom }
:   Type `list`, default `[]`.
    Environment variable sources for controller containers.

`spark.spark-operator.controller.labels` <a class="headerlink" href="#helm.spark.spark-operator.controller.labels" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.labels }
:   Type `object`, default `{}`.
    Extra labels for controller pods.

`spark.spark-operator.controller.leaderElection.enable` <a class="headerlink" href="#helm.spark.spark-operator.controller.leaderElection.enable" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.leaderElection.enable }
:   Type `bool`, default `true`.
    Specifies whether to enable leader election for controller.

`spark.spark-operator.controller.logLevel` <a class="headerlink" href="#helm.spark.spark-operator.controller.logLevel" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.logLevel }
:   Type `string`, default `"info"`.
    Configure the verbosity of logging, can be one of `debug`, `info`, `error`.

`spark.spark-operator.controller.maxTrackedExecutorPerApp` <a class="headerlink" href="#helm.spark.spark-operator.controller.maxTrackedExecutorPerApp" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.maxTrackedExecutorPerApp }
:   Type `int`, default `1000`.
    Specifies the maximum number of Executor pods that can be tracked by the controller per SparkApplication.

`spark.spark-operator.controller.nodeSelector` <a class="headerlink" href="#helm.spark.spark-operator.controller.nodeSelector" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.nodeSelector }
:   Type `object`, default `{}`.
    Node selector for controller pods.

`spark.spark-operator.controller.podDisruptionBudget.enable` <a class="headerlink" href="#helm.spark.spark-operator.controller.podDisruptionBudget.enable" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.podDisruptionBudget.enable }
:   Type `bool`, default `false`.
    Specifies whether to create pod disruption budget for controller. Ref: [Specifying a Disruption Budget for your Application](https://kubernetes.io/docs/tasks/run-application/configure-pdb/)

`spark.spark-operator.controller.podDisruptionBudget.minAvailable` <a class="headerlink" href="#helm.spark.spark-operator.controller.podDisruptionBudget.minAvailable" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.podDisruptionBudget.minAvailable }
:   Type `int`, default `1`.
    The number of pods that must be available. Require `controller.replicas` to be greater than 1

`spark.spark-operator.controller.podSecurityContext` <a class="headerlink" href="#helm.spark.spark-operator.controller.podSecurityContext" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.podSecurityContext }
:   Type `object`, default `{"fsGroup":185}`.
    Security context for controller pods.

`spark.spark-operator.controller.pprof.enable` <a class="headerlink" href="#helm.spark.spark-operator.controller.pprof.enable" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.pprof.enable }
:   Type `bool`, default `false`.
    Specifies whether to enable pprof.

`spark.spark-operator.controller.pprof.port` <a class="headerlink" href="#helm.spark.spark-operator.controller.pprof.port" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.pprof.port }
:   Type `int`, default `6060`.
    Specifies pprof port.

`spark.spark-operator.controller.pprof.portName` <a class="headerlink" href="#helm.spark.spark-operator.controller.pprof.portName" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.pprof.portName }
:   Type `string`, default `"pprof"`.
    Specifies pprof service port name.

`spark.spark-operator.controller.priorityClassName` <a class="headerlink" href="#helm.spark.spark-operator.controller.priorityClassName" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.priorityClassName }
:   Type `string`, default `""`.
    Priority class for controller pods.

`spark.spark-operator.controller.rbac.annotations` <a class="headerlink" href="#helm.spark.spark-operator.controller.rbac.annotations" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.rbac.annotations }
:   Type `object`, default `{}`.
    Extra annotations for the controller RBAC resources.

`spark.spark-operator.controller.rbac.create` <a class="headerlink" href="#helm.spark.spark-operator.controller.rbac.create" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.rbac.create }
:   Type `bool`, default `true`.
    Specifies whether to create RBAC resources for the controller.

`spark.spark-operator.controller.replicas` <a class="headerlink" href="#helm.spark.spark-operator.controller.replicas" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.replicas }
:   Type `int`, default `1`.
    Number of replicas of controller.

`spark.spark-operator.controller.resources` <a class="headerlink" href="#helm.spark.spark-operator.controller.resources" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.resources }
:   Type `object`, default `{"requests":{"cpu":"300m","memory":"512Mi"}}`.
    Pod resource requests and limits for controller containers. Note, that each job submission will spawn a JVM within the controller pods using "/usr/local/openjdk-11/bin/java -Xmx128m". Kubernetes may kill these Java processes at will to enforce resource limits. When that happens, you will see the following error: 'failed to run spark-submit for SparkApplication \[...\]: signal: killed' - when this happens, you may want to increase memory limits.

`spark.spark-operator.controller.securityContext` <a class="headerlink" href="#helm.spark.spark-operator.controller.securityContext" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.securityContext }
:   Type `object`.
    Security context for controller containers.

    ??? note "Default"

        ```yaml
        allowPrivilegeEscalation: false
        capabilities:
          drop:
          - ALL
        privileged: false
        readOnlyRootFilesystem: true
        runAsNonRoot: true
        seccompProfile:
          type: RuntimeDefault
        ```

`spark.spark-operator.controller.serviceAccount.annotations` <a class="headerlink" href="#helm.spark.spark-operator.controller.serviceAccount.annotations" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.serviceAccount.annotations }
:   Type `object`, default `{}`.
    Extra annotations for the controller service account.

`spark.spark-operator.controller.serviceAccount.automountServiceAccountToken` <a class="headerlink" href="#helm.spark.spark-operator.controller.serviceAccount.automountServiceAccountToken" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.serviceAccount.automountServiceAccountToken }
:   Type `bool`, default `true`.
    Auto-mount service account token to the controller pods.

`spark.spark-operator.controller.serviceAccount.create` <a class="headerlink" href="#helm.spark.spark-operator.controller.serviceAccount.create" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.serviceAccount.create }
:   Type `bool`, default `true`.
    Specifies whether to create a service account for the controller.

`spark.spark-operator.controller.serviceAccount.name` <a class="headerlink" href="#helm.spark.spark-operator.controller.serviceAccount.name" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.serviceAccount.name }
:   Type `string`, default `""`.
    Optional name for the controller service account.

`spark.spark-operator.controller.sidecars` <a class="headerlink" href="#helm.spark.spark-operator.controller.sidecars" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.sidecars }
:   Type `list`, default `[]`.
    Sidecar containers for controller pods.

`spark.spark-operator.controller.tolerations` <a class="headerlink" href="#helm.spark.spark-operator.controller.tolerations" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.tolerations }
:   Type `list`, default `[]`.
    List of node taints to tolerate for controller pods.

`spark.spark-operator.controller.topologySpreadConstraints` <a class="headerlink" href="#helm.spark.spark-operator.controller.topologySpreadConstraints" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.topologySpreadConstraints }
:   Type `list`, default `[]`.
    Topology spread constraints rely on node labels to identify the topology domain(s) that each Node is in. Ref: [Pod Topology Spread Constraints](https://kubernetes.io/docs/concepts/workloads/pods/pod-topology-spread-constraints/). The labelSelector field in topology spread constraint will be set to the selector labels for controller pods if not specified.

`spark.spark-operator.controller.uiIngress.annotations` <a class="headerlink" href="#helm.spark.spark-operator.controller.uiIngress.annotations" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.uiIngress.annotations }
:   Type `object`, default `{}`.
    Optionally set default ingress annotations for the Spark UI's ingress. `ingressAnnotations` in the SparkApplication spec overrides this.

`spark.spark-operator.controller.uiIngress.enable` <a class="headerlink" href="#helm.spark.spark-operator.controller.uiIngress.enable" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.uiIngress.enable }
:   Type `bool`, default `false`.
    Specifies whether to create ingress for Spark web UI. `controller.uiService.enable` must be `true` to enable ingress.

`spark.spark-operator.controller.uiIngress.ingressClassName` <a class="headerlink" href="#helm.spark.spark-operator.controller.uiIngress.ingressClassName" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.uiIngress.ingressClassName }
:   Type `string`, default `""`.
    Optionally set the ingressClassName.

`spark.spark-operator.controller.uiIngress.tls` <a class="headerlink" href="#helm.spark.spark-operator.controller.uiIngress.tls" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.uiIngress.tls }
:   Type `list`, default `[]`.
    Optionally set default TLS configuration for the Spark UI's ingress. `ingressTLS` in the SparkApplication spec overrides this.

`spark.spark-operator.controller.uiIngress.urlFormat` <a class="headerlink" href="#helm.spark.spark-operator.controller.uiIngress.urlFormat" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.uiIngress.urlFormat }
:   Type `string`, default `""`.
    Ingress URL format. Required if `controller.uiIngress.enable` is true.

`spark.spark-operator.controller.uiService.enable` <a class="headerlink" href="#helm.spark.spark-operator.controller.uiService.enable" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.uiService.enable }
:   Type `bool`, default `true`.
    Specifies whether to create service for Spark web UI.

`spark.spark-operator.controller.volumeMounts` <a class="headerlink" href="#helm.spark.spark-operator.controller.volumeMounts" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.volumeMounts }
:   Type `list`, default `[{"mountPath":"/tmp","name":"tmp","readOnly":false}]`.
    Volume mounts for controller containers.

`spark.spark-operator.controller.volumes` <a class="headerlink" href="#helm.spark.spark-operator.controller.volumes" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.volumes }
:   Type `list`, default `[{"emptyDir":{"sizeLimit":"1Gi"},"name":"tmp"}]`.
    Volumes for controller pods.

`spark.spark-operator.controller.workers` <a class="headerlink" href="#helm.spark.spark-operator.controller.workers" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.workers }
:   Type `int`, default `10`.
    Reconcile concurrency, higher values might increase memory usage.

`spark.spark-operator.controller.workqueueRateLimiter.bucketQPS` <a class="headerlink" href="#helm.spark.spark-operator.controller.workqueueRateLimiter.bucketQPS" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.workqueueRateLimiter.bucketQPS }
:   Type `int`, default `50`.
    Specifies the average rate of items process by the workqueue rate limiter.

`spark.spark-operator.controller.workqueueRateLimiter.bucketSize` <a class="headerlink" href="#helm.spark.spark-operator.controller.workqueueRateLimiter.bucketSize" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.workqueueRateLimiter.bucketSize }
:   Type `int`, default `500`.
    Specifies the maximum number of items that can be in the workqueue at any given time.

`spark.spark-operator.controller.workqueueRateLimiter.maxDelay.duration` <a class="headerlink" href="#helm.spark.spark-operator.controller.workqueueRateLimiter.maxDelay.duration" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.workqueueRateLimiter.maxDelay.duration }
:   Type `string`, default `"6h"`.
    Specifies the maximum delay duration for the workqueue rate limiter.

`spark.spark-operator.controller.workqueueRateLimiter.maxDelay.enable` <a class="headerlink" href="#helm.spark.spark-operator.controller.workqueueRateLimiter.maxDelay.enable" title="Permanent link">#</a> { #helm.spark.spark-operator.controller.workqueueRateLimiter.maxDelay.enable }
:   Type `bool`, default `true`.
    Specifies whether to enable max delay for the workqueue rate limiter. This is useful to avoid losing events when the workqueue is full.

`spark.spark-operator.fullnameOverride` <a class="headerlink" href="#helm.spark.spark-operator.fullnameOverride" title="Permanent link">#</a> { #helm.spark.spark-operator.fullnameOverride }
:   Type `string`, default `""`.
    String to fully override release name.

`spark.spark-operator.hook.affinity` <a class="headerlink" href="#helm.spark.spark-operator.hook.affinity" title="Permanent link">#</a> { #helm.spark.spark-operator.hook.affinity }
:   Type `object`, default `{}`.
    Affinity for the Helm hook Job.

`spark.spark-operator.hook.image.registry` <a class="headerlink" href="#helm.spark.spark-operator.hook.image.registry" title="Permanent link">#</a> { #helm.spark.spark-operator.hook.image.registry }
:   Type `string`, default `"docker.hops.works"`.
    Image registry.

`spark.spark-operator.hook.image.repository` <a class="headerlink" href="#helm.spark.spark-operator.hook.image.repository" title="Permanent link">#</a> { #helm.spark.spark-operator.hook.image.repository }
:   Type `string`, default `"hopsworks/spark-operator-crds"`.
    Image repository.

`spark.spark-operator.hook.image.tag` <a class="headerlink" href="#helm.spark.spark-operator.hook.image.tag" title="Permanent link">#</a> { #helm.spark.spark-operator.hook.image.tag }
:   Type `string`, default If not set, the chart appVersion will be used..
    Image tag.

`spark.spark-operator.hook.nodeSelector` <a class="headerlink" href="#helm.spark.spark-operator.hook.nodeSelector" title="Permanent link">#</a> { #helm.spark.spark-operator.hook.nodeSelector }
:   Type `object`, default `{}`.
    Node selector for the Helm hook Job.

`spark.spark-operator.hook.tolerations` <a class="headerlink" href="#helm.spark.spark-operator.hook.tolerations" title="Permanent link">#</a> { #helm.spark.spark-operator.hook.tolerations }
:   Type `list`, default `[]`.
    List of node taints to tolerate for the Helm hook Job.

`spark.spark-operator.hook.upgradeCrd` <a class="headerlink" href="#helm.spark.spark-operator.hook.upgradeCrd" title="Permanent link">#</a> { #helm.spark.spark-operator.hook.upgradeCrd }
:   Type `bool`, default `true`.
    Whether to create a Helm pre-install/pre-upgrade hook Job to update CRDs.

`spark.spark-operator.image.pullPolicy` <a class="headerlink" href="#helm.spark.spark-operator.image.pullPolicy" title="Permanent link">#</a> { #helm.spark.spark-operator.image.pullPolicy }
:   Type `string`, default `"IfNotPresent"`.
    Image pull policy.

`spark.spark-operator.image.pullSecrets` <a class="headerlink" href="#helm.spark.spark-operator.image.pullSecrets" title="Permanent link">#</a> { #helm.spark.spark-operator.image.pullSecrets }
:   Type `list`, default `[]`.
    Image pull secrets for private image registry.

`spark.spark-operator.image.registry` <a class="headerlink" href="#helm.spark.spark-operator.image.registry" title="Permanent link">#</a> { #helm.spark.spark-operator.image.registry }
:   Type `string`, default `"docker.hops.works"`.
    Image registry.

`spark.spark-operator.image.repository` <a class="headerlink" href="#helm.spark.spark-operator.image.repository" title="Permanent link">#</a> { #helm.spark.spark-operator.image.repository }
:   Type `string`, default `"hopsworks/spark-operator"`.
    Image repository.

`spark.spark-operator.image.tag` <a class="headerlink" href="#helm.spark.spark-operator.image.tag" title="Permanent link">#</a> { #helm.spark.spark-operator.image.tag }
:   Type `string`, default If not set, the chart appVersion will be used..
    Image tag.

`spark.spark-operator.nameOverride` <a class="headerlink" href="#helm.spark.spark-operator.nameOverride" title="Permanent link">#</a> { #helm.spark.spark-operator.nameOverride }
:   Type `string`, default `""`.
    String to partially override release name.

`spark.spark-operator.podSecurityContext` <a class="headerlink" href="#helm.spark.spark-operator.podSecurityContext" title="Permanent link">#</a> { #helm.spark.spark-operator.podSecurityContext }
:   Type `object`.
    Pod-level security context for spark-operator

    ??? note "Default"

        ```yaml
        fsGroup: 185
        runAsGroup: 185
        runAsNonRoot: true
        runAsUser: 185
        seccompProfile:
          type: RuntimeDefault
        ```

`spark.spark-operator.prometheus.metrics.enable` <a class="headerlink" href="#helm.spark.spark-operator.prometheus.metrics.enable" title="Permanent link">#</a> { #helm.spark.spark-operator.prometheus.metrics.enable }
:   Type `bool`, default `true`.
    Specifies whether to enable prometheus metrics scraping.

`spark.spark-operator.prometheus.metrics.endpoint` <a class="headerlink" href="#helm.spark.spark-operator.prometheus.metrics.endpoint" title="Permanent link">#</a> { #helm.spark.spark-operator.prometheus.metrics.endpoint }
:   Type `string`, default `"/metrics"`.
    Metrics serving endpoint.

`spark.spark-operator.prometheus.metrics.jobStartLatencyBuckets` <a class="headerlink" href="#helm.spark.spark-operator.prometheus.metrics.jobStartLatencyBuckets" title="Permanent link">#</a> { #helm.spark.spark-operator.prometheus.metrics.jobStartLatencyBuckets }
:   Type `string`, default `"30,60,90,120,150,180,210,240,270,300"`.
    Job Start Latency histogram buckets. Specified in seconds.

`spark.spark-operator.prometheus.metrics.port` <a class="headerlink" href="#helm.spark.spark-operator.prometheus.metrics.port" title="Permanent link">#</a> { #helm.spark.spark-operator.prometheus.metrics.port }
:   Type `int`, default `8080`.
    Metrics port.

`spark.spark-operator.prometheus.metrics.portName` <a class="headerlink" href="#helm.spark.spark-operator.prometheus.metrics.portName" title="Permanent link">#</a> { #helm.spark.spark-operator.prometheus.metrics.portName }
:   Type `string`, default `"metrics"`.
    Metrics port name.

`spark.spark-operator.prometheus.metrics.prefix` <a class="headerlink" href="#helm.spark.spark-operator.prometheus.metrics.prefix" title="Permanent link">#</a> { #helm.spark.spark-operator.prometheus.metrics.prefix }
:   Type `string`, default `""`.
    Metrics prefix, will be added to all exported metrics.

`spark.spark-operator.prometheus.podMonitor.create` <a class="headerlink" href="#helm.spark.spark-operator.prometheus.podMonitor.create" title="Permanent link">#</a> { #helm.spark.spark-operator.prometheus.podMonitor.create }
:   Type `bool`, default `false`.
    Specifies whether to create pod monitor. Note that prometheus metrics should be enabled as well.

`spark.spark-operator.prometheus.podMonitor.jobLabel` <a class="headerlink" href="#helm.spark.spark-operator.prometheus.podMonitor.jobLabel" title="Permanent link">#</a> { #helm.spark.spark-operator.prometheus.podMonitor.jobLabel }
:   Type `string`, default `"spark-operator-podmonitor"`.
    The label to use to retrieve the job name from

`spark.spark-operator.prometheus.podMonitor.labels` <a class="headerlink" href="#helm.spark.spark-operator.prometheus.podMonitor.labels" title="Permanent link">#</a> { #helm.spark.spark-operator.prometheus.podMonitor.labels }
:   Type `object`, default `{}`.
    Pod monitor labels

`spark.spark-operator.prometheus.podMonitor.podMetricsEndpoint` <a class="headerlink" href="#helm.spark.spark-operator.prometheus.podMonitor.podMetricsEndpoint" title="Permanent link">#</a> { #helm.spark.spark-operator.prometheus.podMonitor.podMetricsEndpoint }
:   Type `object`, default `{"interval":"5s","scheme":"http"}`.
    Prometheus metrics endpoint properties. `metrics.portName` will be used as a port

`spark.spark-operator.securityContext` <a class="headerlink" href="#helm.spark.spark-operator.securityContext" title="Permanent link">#</a> { #helm.spark.spark-operator.securityContext }
:   Type `object`.
    Container-level security context for spark-operator

    ??? note "Default"

        ```yaml
        allowPrivilegeEscalation: false
        capabilities:
          drop:
          - ALL
        runAsGroup: 185
        runAsNonRoot: true
        runAsUser: 185
        seccompProfile:
          type: RuntimeDefault
        ```

`spark.spark-operator.spark.jobNamespaces` <a class="headerlink" href="#helm.spark.spark-operator.spark.jobNamespaces" title="Permanent link">#</a> { #helm.spark.spark-operator.spark.jobNamespaces }
:   Type `list`, default `[]`.
    List of namespaces where to run spark jobs. If empty string is included, all namespaces will be allowed. Make sure the namespaces have already existed.

`spark.spark-operator.spark.rbac.annotations` <a class="headerlink" href="#helm.spark.spark-operator.spark.rbac.annotations" title="Permanent link">#</a> { #helm.spark.spark-operator.spark.rbac.annotations }
:   Type `object`, default `{}`.
    Optional annotations for the spark application RBAC resources.

`spark.spark-operator.spark.rbac.create` <a class="headerlink" href="#helm.spark.spark-operator.spark.rbac.create" title="Permanent link">#</a> { #helm.spark.spark-operator.spark.rbac.create }
:   Type `bool`, default `true`.
    Specifies whether to create RBAC resources for spark applications.

`spark.spark-operator.spark.serviceAccount.annotations` <a class="headerlink" href="#helm.spark.spark-operator.spark.serviceAccount.annotations" title="Permanent link">#</a> { #helm.spark.spark-operator.spark.serviceAccount.annotations }
:   Type `object`, default `{}`.
    Optional annotations for the spark service account.

`spark.spark-operator.spark.serviceAccount.automountServiceAccountToken` <a class="headerlink" href="#helm.spark.spark-operator.spark.serviceAccount.automountServiceAccountToken" title="Permanent link">#</a> { #helm.spark.spark-operator.spark.serviceAccount.automountServiceAccountToken }
:   Type `bool`, default `true`.
    Auto-mount service account token to the spark applications pods.

`spark.spark-operator.spark.serviceAccount.create` <a class="headerlink" href="#helm.spark.spark-operator.spark.serviceAccount.create" title="Permanent link">#</a> { #helm.spark.spark-operator.spark.serviceAccount.create }
:   Type `bool`, default `true`.
    Specifies whether to create a service account for spark applications.

`spark.spark-operator.spark.serviceAccount.name` <a class="headerlink" href="#helm.spark.spark-operator.spark.serviceAccount.name" title="Permanent link">#</a> { #helm.spark.spark-operator.spark.serviceAccount.name }
:   Type `string`, default `""`.
    Optional name for the spark service account.

`spark.spark-operator.webhook.affinity` <a class="headerlink" href="#helm.spark.spark-operator.webhook.affinity" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.affinity }
:   Type `object`, default `{}`.
    Affinity for webhook pods.

`spark.spark-operator.webhook.annotations` <a class="headerlink" href="#helm.spark.spark-operator.webhook.annotations" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.annotations }
:   Type `object`, default `{}`.
    Extra annotations for webhook pods.

`spark.spark-operator.webhook.enable` <a class="headerlink" href="#helm.spark.spark-operator.webhook.enable" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.enable }
:   Type `bool`, default `true`.
    Specifies whether to enable webhook.

`spark.spark-operator.webhook.env` <a class="headerlink" href="#helm.spark.spark-operator.webhook.env" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.env }
:   Type `list`, default `[]`.
    Environment variables for webhook containers.

`spark.spark-operator.webhook.envFrom` <a class="headerlink" href="#helm.spark.spark-operator.webhook.envFrom" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.envFrom }
:   Type `list`, default `[]`.
    Environment variable sources for webhook containers.

`spark.spark-operator.webhook.failurePolicy` <a class="headerlink" href="#helm.spark.spark-operator.webhook.failurePolicy" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.failurePolicy }
:   Type `string`, default `"Fail"`.
    Specifies how unrecognized errors are handled. Available options are `Ignore` or `Fail`.

`spark.spark-operator.webhook.labels` <a class="headerlink" href="#helm.spark.spark-operator.webhook.labels" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.labels }
:   Type `object`, default `{}`.
    Extra labels for webhook pods.

`spark.spark-operator.webhook.leaderElection.enable` <a class="headerlink" href="#helm.spark.spark-operator.webhook.leaderElection.enable" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.leaderElection.enable }
:   Type `bool`, default `true`.
    Specifies whether to enable leader election for webhook.

`spark.spark-operator.webhook.logLevel` <a class="headerlink" href="#helm.spark.spark-operator.webhook.logLevel" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.logLevel }
:   Type `string`, default `"info"`.
    Configure the verbosity of logging, can be one of `debug`, `info`, `error`.

`spark.spark-operator.webhook.nodeSelector` <a class="headerlink" href="#helm.spark.spark-operator.webhook.nodeSelector" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.nodeSelector }
:   Type `object`, default `{}`.
    Node selector for webhook pods.

`spark.spark-operator.webhook.podDisruptionBudget.enable` <a class="headerlink" href="#helm.spark.spark-operator.webhook.podDisruptionBudget.enable" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.podDisruptionBudget.enable }
:   Type `bool`, default `false`.
    Specifies whether to create pod disruption budget for webhook. Ref: [Specifying a Disruption Budget for your Application](https://kubernetes.io/docs/tasks/run-application/configure-pdb/)

`spark.spark-operator.webhook.podDisruptionBudget.minAvailable` <a class="headerlink" href="#helm.spark.spark-operator.webhook.podDisruptionBudget.minAvailable" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.podDisruptionBudget.minAvailable }
:   Type `int`, default `1`.
    The number of pods that must be available. Require `webhook.replicas` to be greater than 1

`spark.spark-operator.webhook.podSecurityContext` <a class="headerlink" href="#helm.spark.spark-operator.webhook.podSecurityContext" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.podSecurityContext }
:   Type `object`, default `{"fsGroup":185}`.
    Security context for webhook pods.

`spark.spark-operator.webhook.port` <a class="headerlink" href="#helm.spark.spark-operator.webhook.port" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.port }
:   Type `int`, default `9443`.
    Specifies webhook port.

`spark.spark-operator.webhook.portName` <a class="headerlink" href="#helm.spark.spark-operator.webhook.portName" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.portName }
:   Type `string`, default `"webhook"`.
    Specifies webhook service port name.

`spark.spark-operator.webhook.priorityClassName` <a class="headerlink" href="#helm.spark.spark-operator.webhook.priorityClassName" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.priorityClassName }
:   Type `string`, default `""`.
    Priority class for webhook pods.

`spark.spark-operator.webhook.rbac.annotations` <a class="headerlink" href="#helm.spark.spark-operator.webhook.rbac.annotations" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.rbac.annotations }
:   Type `object`, default `{}`.
    Extra annotations for the webhook RBAC resources.

`spark.spark-operator.webhook.rbac.create` <a class="headerlink" href="#helm.spark.spark-operator.webhook.rbac.create" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.rbac.create }
:   Type `bool`, default `true`.
    Specifies whether to create RBAC resources for the webhook.

`spark.spark-operator.webhook.replicas` <a class="headerlink" href="#helm.spark.spark-operator.webhook.replicas" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.replicas }
:   Type `int`, default `1`.
    Number of replicas of webhook server.

`spark.spark-operator.webhook.resourceQuotaEnforcement.enable` <a class="headerlink" href="#helm.spark.spark-operator.webhook.resourceQuotaEnforcement.enable" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.resourceQuotaEnforcement.enable }
:   Type `bool`, default `false`.
    Specifies whether to enable the ResourceQuota enforcement for SparkApplication resources.

`spark.spark-operator.webhook.resources` <a class="headerlink" href="#helm.spark.spark-operator.webhook.resources" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.resources }
:   Type `object`, default `{"requests":{"cpu":"300m","memory":"512Mi"}}`.
    Pod resource requests and limits for webhook pods.

`spark.spark-operator.webhook.securityContext` <a class="headerlink" href="#helm.spark.spark-operator.webhook.securityContext" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.securityContext }
:   Type `object`.
    Security context for webhook containers.

    ??? note "Default"

        ```yaml
        allowPrivilegeEscalation: false
        capabilities:
          drop:
          - ALL
        privileged: false
        readOnlyRootFilesystem: true
        runAsNonRoot: true
        seccompProfile:
          type: RuntimeDefault
        ```

`spark.spark-operator.webhook.serviceAccount.annotations` <a class="headerlink" href="#helm.spark.spark-operator.webhook.serviceAccount.annotations" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.serviceAccount.annotations }
:   Type `object`, default `{}`.
    Extra annotations for the webhook service account.

`spark.spark-operator.webhook.serviceAccount.automountServiceAccountToken` <a class="headerlink" href="#helm.spark.spark-operator.webhook.serviceAccount.automountServiceAccountToken" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.serviceAccount.automountServiceAccountToken }
:   Type `bool`, default `true`.
    Auto-mount service account token to the webhook pods.

`spark.spark-operator.webhook.serviceAccount.create` <a class="headerlink" href="#helm.spark.spark-operator.webhook.serviceAccount.create" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.serviceAccount.create }
:   Type `bool`, default `true`.
    Specifies whether to create a service account for the webhook.

`spark.spark-operator.webhook.serviceAccount.name` <a class="headerlink" href="#helm.spark.spark-operator.webhook.serviceAccount.name" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.serviceAccount.name }
:   Type `string`, default `""`.
    Optional name for the webhook service account.

`spark.spark-operator.webhook.sidecars` <a class="headerlink" href="#helm.spark.spark-operator.webhook.sidecars" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.sidecars }
:   Type `list`, default `[]`.
    Sidecar containers for webhook pods.

`spark.spark-operator.webhook.timeoutSeconds` <a class="headerlink" href="#helm.spark.spark-operator.webhook.timeoutSeconds" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.timeoutSeconds }
:   Type `int`, default `10`.
    Specifies the timeout seconds of the webhook, the value must be between 1 and 30.

`spark.spark-operator.webhook.tolerations` <a class="headerlink" href="#helm.spark.spark-operator.webhook.tolerations" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.tolerations }
:   Type `list`, default `[]`.
    List of node taints to tolerate for webhook pods.

`spark.spark-operator.webhook.topologySpreadConstraints` <a class="headerlink" href="#helm.spark.spark-operator.webhook.topologySpreadConstraints" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.topologySpreadConstraints }
:   Type `list`, default `[]`.
    Topology spread constraints rely on node labels to identify the topology domain(s) that each Node is in. Ref: [Pod Topology Spread Constraints](https://kubernetes.io/docs/concepts/workloads/pods/pod-topology-spread-constraints/). The labelSelector field in topology spread constraint will be set to the selector labels for webhook pods if not specified.

`spark.spark-operator.webhook.volumeMounts` <a class="headerlink" href="#helm.spark.spark-operator.webhook.volumeMounts" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.volumeMounts }
:   Type `list`.
    Volume mounts for webhook containers.

    ??? note "Default"

        ```yaml
        - mountPath: /etc/k8s-webhook-server/serving-certs
          name: serving-certs
          readOnly: false
          subPath: serving-certs
        - mountPath: /tmp
          name: tmp
        ```

`spark.spark-operator.webhook.volumes` <a class="headerlink" href="#helm.spark.spark-operator.webhook.volumes" title="Permanent link">#</a> { #helm.spark.spark-operator.webhook.volumes }
:   Type `list`.
    Volumes for webhook pods.

    ??? note "Default"

        ```yaml
        - emptyDir:
            sizeLimit: 500Mi
          name: serving-certs
        - emptyDir: {}
          name: tmp
        ```

</div>

## sparkOperatorUpgradeJob { #helm-values-spark-sparkoperatorupgradejob }

??? example "Defaults as YAML"

    ```yaml
    spark:
      sparkOperatorUpgradeJob:
        crdImage:
          repository: spark-operator-crds
          tag: 2.2.1-1.4
        imagePullPolicy: Always
        leaderElectionLockName: spark-operator-lock
        leaderElectionLockNamespace: ''
        name: spark-operator-upgrade-job
        nodeSelector: {}
        podMonitorName: spark-operator-podmonitor
        resources:
          limits:
            cpu: 200m
            memory: 200M
          requests:
            cpu: 100m
            memory: 100M
        serviceAccount:
          annotations: {}
        sparkJobNamespace: ''
        tolerations: []
    ```

<div class="hops-values" markdown>

`spark.sparkOperatorUpgradeJob` <a class="headerlink" href="#helm.spark.sparkOperatorUpgradeJob" title="Permanent link">#</a> { #helm.spark.sparkOperatorUpgradeJob }
:   Type `object`.
    Job configuration to clean up old spark-operator resources before upgrading.

    ??? note "Default"

        ```yaml
        crdImage:
          repository: spark-operator-crds
          tag: 2.2.1-1.4
        imagePullPolicy: Always
        leaderElectionLockName: spark-operator-lock
        leaderElectionLockNamespace: ''
        name: spark-operator-upgrade-job
        nodeSelector: {}
        podMonitorName: spark-operator-podmonitor
        resources:
          limits:
            cpu: 200m
            memory: 200M
          requests:
            cpu: 100m
            memory: 100M
        serviceAccount:
          annotations: {}
        sparkJobNamespace: ''
        tolerations: []
        ```

`spark.sparkOperatorUpgradeJob.crdImage` <a class="headerlink" href="#helm.spark.sparkOperatorUpgradeJob.crdImage" title="Permanent link">#</a> { #helm.spark.sparkOperatorUpgradeJob.crdImage }
:   Type `object`, default `{"repository":"spark-operator-crds","tag":"2.2.1-1.4"}`.
    Image for the pre-upgrade Job. Must ship the spark-operator CRDs at `/opt/spark-operator-crds/` and provide `bash` and `kubectl`.

`spark.sparkOperatorUpgradeJob.leaderElectionLockName` <a class="headerlink" href="#helm.spark.sparkOperatorUpgradeJob.leaderElectionLockName" title="Permanent link">#</a> { #helm.spark.sparkOperatorUpgradeJob.leaderElectionLockName }
:   Type `string`, default `"spark-operator-lock"`.
    Leader election lease name used by the old chart (only if replicaCount > 1).

`spark.sparkOperatorUpgradeJob.leaderElectionLockNamespace` <a class="headerlink" href="#helm.spark.sparkOperatorUpgradeJob.leaderElectionLockNamespace" title="Permanent link">#</a> { #helm.spark.sparkOperatorUpgradeJob.leaderElectionLockNamespace }
:   Type `string`, default `""`.
    Optional leader election lease namespace (defaults to release namespace).

`spark.sparkOperatorUpgradeJob.nodeSelector` <a class="headerlink" href="#helm.spark.sparkOperatorUpgradeJob.nodeSelector" title="Permanent link">#</a> { #helm.spark.sparkOperatorUpgradeJob.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

`spark.sparkOperatorUpgradeJob.podMonitorName` <a class="headerlink" href="#helm.spark.sparkOperatorUpgradeJob.podMonitorName" title="Permanent link">#</a> { #helm.spark.sparkOperatorUpgradeJob.podMonitorName }
:   Type `string`, default `"spark-operator-podmonitor"`.
    PodMonitor name used by the old chart (only if enabled).

`spark.sparkOperatorUpgradeJob.serviceAccount.annotations` <a class="headerlink" href="#helm.spark.sparkOperatorUpgradeJob.serviceAccount.annotations" title="Permanent link">#</a> { #helm.spark.sparkOperatorUpgradeJob.serviceAccount.annotations }
:   Type `object`, default `{}`.
    service account annotations

`spark.sparkOperatorUpgradeJob.sparkJobNamespace` <a class="headerlink" href="#helm.spark.sparkOperatorUpgradeJob.sparkJobNamespace" title="Permanent link">#</a> { #helm.spark.sparkOperatorUpgradeJob.sparkJobNamespace }
:   Type `string`, default `""`.
    Namespace where spark app RBAC/SA were created by the old chart.

</div>

<!-- END GENERATED VALUES -->
