# Kafka values { #helm-values-kafka }

Values under `kafka` configure Kafka, run by the Strimzi operator, which carries feature data on its way to the online feature store.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.1.0` (Hopsworks `5.1.0`)._

Deployed when [`global._hopsworks.kafka.enabled`](global.md#helm.global._hopsworks.kafka.enabled) is `true`.

!!! info "Upstream charts"

    - Values under `kafka.strimzi-kafka-operator` go to [`strimzi-kafka-operator` 0.45.2](https://artifacthub.io/packages/helm/strimzi/strimzi-kafka-operator/0.45.2) from `https://strimzi.io/charts/`.

    Only the values Hopsworks sets under `kafka.strimzi-kafka-operator` are listed on this page.
    Any other value of the chart can be set there too; the link opens its documentation for the version Hopsworks pins.

## General { #helm-values-kafka-general }

??? example "Defaults as YAML"

    ```yaml
    kafka:
      appName: kafka
      cleanupOnUninstall:
        enabled: true
        ttlSecondsAfterFinished: null
      cluster:
        kafka:
          storageClassName: null
        zookeeper:
          storageClassName: null
      configmap:
        name: kafka-configmap
      hopsworkslib: {}
      metrics:
        configMapKey: kafka-metrics-config
        enabled: true
        type: jmxPrometheusExporter
      strimzi-kafka-operator:
        createGlobalResources: true
        defaultImageRegistry: docker.hops.works
        defaultImageRepository: strimzi
        defaultImageTag: 0.45.2-h1
        enabled: true
        extraEnvs:
        - name: HOPSWORKS_FIRST_STRIMZICA_CA_CERT
          valueFrom:
            secretKeyRef:
              key: ca.crt
              name: kafka-cluster-cluster-ca-cert
        - name: HOPSWORKS_FIRST_STRIMZICA_CLIENT_CERT
          valueFrom:
            secretKeyRef:
              key: ca.crt
              name: kafka-cluster-clients-ca-cert
        - name: HOPSWORKS_FIRST_STRIMZICA_CLIENT_CA
          valueFrom:
            secretKeyRef:
              key: ca.key
              name: kafka-cluster-clients-ca
        - name: HOPSWORKS_FIRST_STRIMZICA_CA
          valueFrom:
            secretKeyRef:
              key: ca.key
              name: kafka-cluster-cluster-ca
        nodeSelector: {}
        podSecurityContext:
          fsGroup: 1000
          runAsGroup: 1000
          runAsNonRoot: true
          runAsUser: 1000
          seccompProfile:
            type: RuntimeDefault
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL
          runAsGroup: 1000
          runAsNonRoot: true
          runAsUser: 1000
          seccompProfile:
            type: RuntimeDefault
        tolerations: []
        watchAnyNamespace: false
      topics: []
      users: []
    ```

<div class="hops-values" markdown>

`kafka` <a class="headerlink" href="#helm.kafka" title="Permanent link">#</a> { #helm.kafka }
:   Type `object`.
    override kafka values

    ??? note "Default"

        ```yaml
        cluster:
          kafka:
            storageClassName: null
          zookeeper:
            storageClassName: null
        strimzi-kafka-operator:
          defaultImageRegistry: docker.hops.works
        ```

`kafka.appName` <a class="headerlink" href="#helm.kafka.appName" title="Permanent link">#</a> { #helm.kafka.appName }
:   Type `string`, default `"kafka"`.

`kafka.cleanupOnUninstall` <a class="headerlink" href="#helm.kafka.cleanupOnUninstall" title="Permanent link">#</a> { #helm.kafka.cleanupOnUninstall }
:   Type `object`, default `{"enabled":true,"ttlSecondsAfterFinished":null}`.
    post-delete cleanup of Kafka leftovers. Strimzi's Kafka/Zookeeper StatefulSet PVCs survive uninstall; this deletes them by the strimzi.io/cluster label, but only when global._hopsworks.wipeDataOnUninstall is enabled and never for PVCs labelled hopsworks.ai/keep=true.

`kafka.cleanupOnUninstall.enabled` <a class="headerlink" href="#helm.kafka.cleanupOnUninstall.enabled" title="Permanent link">#</a> { #helm.kafka.cleanupOnUninstall.enabled }
:   Type `bool`, default `true`.
    enable the post-delete Kafka data-PVC cleanup hook (also requires global._hopsworks.wipeDataOnUninstall)

`kafka.cleanupOnUninstall.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.kafka.cleanupOnUninstall.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.kafka.cleanupOnUninstall.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    ttlSecondsAfterFinished for the cleanup Job; null falls through to the global default

`kafka.configmap.name` <a class="headerlink" href="#helm.kafka.configmap.name" title="Permanent link">#</a> { #helm.kafka.configmap.name }
:   Type `string`, default `"kafka-configmap"`.

`kafka.hopsworkslib` <a class="headerlink" href="#helm.kafka.hopsworkslib" title="Permanent link">#</a> { #helm.kafka.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`kafka.metrics.configMapKey` <a class="headerlink" href="#helm.kafka.metrics.configMapKey" title="Permanent link">#</a> { #helm.kafka.metrics.configMapKey }
:   Type `string`, default `"kafka-metrics-config"`.

`kafka.metrics.enabled` <a class="headerlink" href="#helm.kafka.metrics.enabled" title="Permanent link">#</a> { #helm.kafka.metrics.enabled }
:   Type `bool`, default `true`.

`kafka.metrics.type` <a class="headerlink" href="#helm.kafka.metrics.type" title="Permanent link">#</a> { #helm.kafka.metrics.type }
:   Type `string`, default `"jmxPrometheusExporter"`.

`kafka.strimzi-kafka-operator` <a class="headerlink" href="#helm.kafka.strimzi-kafka-operator" title="Permanent link">#</a> { #helm.kafka.strimzi-kafka-operator }
:   Type `object`, passed to the [`strimzi-kafka-operator` 0.45.2](https://artifacthub.io/packages/helm/strimzi/strimzi-kafka-operator/0.45.2) chart, whose other values are documented there.
    override values for strimzi operator

    ??? note "Default"

        ```yaml
        createGlobalResources: true
        defaultImageRegistry: docker.hops.works
        defaultImageRepository: strimzi
        defaultImageTag: 0.45.2-h1
        enabled: true
        extraEnvs:
        - name: HOPSWORKS_FIRST_STRIMZICA_CA_CERT
          valueFrom:
            secretKeyRef:
              key: ca.crt
              name: kafka-cluster-cluster-ca-cert
        - name: HOPSWORKS_FIRST_STRIMZICA_CLIENT_CERT
          valueFrom:
            secretKeyRef:
              key: ca.crt
              name: kafka-cluster-clients-ca-cert
        - name: HOPSWORKS_FIRST_STRIMZICA_CLIENT_CA
          valueFrom:
            secretKeyRef:
              key: ca.key
              name: kafka-cluster-clients-ca
        - name: HOPSWORKS_FIRST_STRIMZICA_CA
          valueFrom:
            secretKeyRef:
              key: ca.key
              name: kafka-cluster-cluster-ca
        nodeSelector: {}
        podSecurityContext:
          fsGroup: 1000
          runAsGroup: 1000
          runAsNonRoot: true
          runAsUser: 1000
          seccompProfile:
            type: RuntimeDefault
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL
          runAsGroup: 1000
          runAsNonRoot: true
          runAsUser: 1000
          seccompProfile:
            type: RuntimeDefault
        tolerations: []
        watchAnyNamespace: false
        ```

`kafka.topics` <a class="headerlink" href="#helm.kafka.topics" title="Permanent link">#</a> { #helm.kafka.topics }
:   Type `list`, default `[]`.
    A list of topics to provision in the Kafka cluster.

`kafka.users` <a class="headerlink" href="#helm.kafka.users" title="Permanent link">#</a> { #helm.kafka.users }
:   Type `list`, default `[]`.
    A list of user to provision in the Kafka cluster.

</div>

## cluster { #helm-values-kafka-cluster }

??? example "Defaults as YAML"

    ```yaml
    kafka:
      cluster:
        clientsCa:
          validityDays: 365
        clusterCa:
          validityDays: 365
        entityOperator: {}
        kafka:
          authorizer:
            authorizerClass: io.hops.kafka.HopsAclAuthorizer
            principalBuilderClass: io.hops.kafka.HopsPrincipalBuilder
            superUsers: []
            type: custom
          config:
            database:
              name: hopsworks
            log:
              retention:
                bytes: -1
                checkIntervalMs: 300000
                hours: 168
          dependencies:
            glassfish:
              consulServiceName: glassfish
              consulServiceTag: hopsworks
            mysql:
              consulServiceName: mysql
              port: 3306
            onlinefs:
              consulServiceName: onlinefs
          externalLoadBalancer:
            annotations: {}
            class: null
            dns: ''
            enabled: null
            finalizers: []
            managed: null
            nodeSelector: {}
            startingAdvertisedPort: 9093
          jvmOptions: {}
          nodeSelector: {}
          podAntiAffinity:
            required: false
          podSecurityContext:
            fsGroup: 1001
            runAsGroup: 1001
            runAsNonRoot: true
            runAsUser: 1001
            seccompProfile:
              type: RuntimeDefault
          quotas:
            defaults:
              consumerByteRate: 9223372036854775807
              enabled: false
              producerByteRate: 1048576
              requestPercentage: 100
            kafka:
              consumerByteRate: null
              controllerMutationRate: null
              producerByteRate: null
              requestPercentage: null
            minAvailableBytesPerVolume: 0
            minAvailableRatioPerVolume: 0.01
            strimzi:
              consumerByteRate: null
              excludedPrincipals: []
              producerByteRate: null
            type: strimzi
            window:
              num: 11
              sizeSeconds: 1
          replicas: 1
          resources: {}
          securityContext:
            allowPrivilegeEscalation: false
            capabilities:
              drop:
              - ALL
            runAsGroup: 1001
            runAsNonRoot: true
            runAsUser: 1001
            seccompProfile:
              type: RuntimeDefault
          services:
            brokers:
              annotations:
                consul.hashicorp.com/service-name: kafka
                consul.hashicorp.com/service-port: 9092
                consul.hashicorp.com/service-tags: broker
            pods:
              annotations:
                prometheus.io/path: /metrics
                prometheus.io/port: 9404
                prometheus.io/scheme: http
                prometheus.io/scrape: 'true'
          storageClassName: null
          storageSize: 30Gi
          tolerations: []
          topologySpreadConstraint: {}
          version: 3.9.2
        name: kafka-cluster
        tlscerts:
          annotations:
            certs.hopsworks.ai/owned-by: deployment-strimzi-cluster-operator
        zookeeper:
          nodeSelector: {}
          podAntiAffinity:
            required: false
          podSecurityContext:
            fsGroup: 1001
            runAsGroup: 1001
            runAsNonRoot: true
            runAsUser: 1001
            seccompProfile:
              type: RuntimeDefault
          replicas: 1
          resources:
            limits:
              cpu: '2'
              memory: 3Gi
            requests:
              cpu: 200m
              memory: 1Gi
          securityContext:
            allowPrivilegeEscalation: false
            capabilities:
              drop:
              - ALL
            runAsGroup: 1001
            runAsNonRoot: true
            runAsUser: 1001
            seccompProfile:
              type: RuntimeDefault
          services:
            client:
              annotations:
                consul.hashicorp.com/service-name: zookeeper
                consul.hashicorp.com/service-tags: client
          storageClassName: null
          storageSize: 5Gi
          tolerations: []
          topologySpreadConstraint: {}
    ```

<div class="hops-values" markdown>

`kafka.cluster.clientsCa.validityDays` <a class="headerlink" href="#helm.kafka.cluster.clientsCa.validityDays" title="Permanent link">#</a> { #helm.kafka.cluster.clientsCa.validityDays }
:   Type `int`, default `365`.
    Validity in days of the KafkaUser certificates Strimzi issues under the clients CA. Applies at the next issuance; already-issued certificates keep their dates.

`kafka.cluster.clusterCa.validityDays` <a class="headerlink" href="#helm.kafka.cluster.clusterCa.validityDays" title="Permanent link">#</a> { #helm.kafka.cluster.clusterCa.validityDays }
:   Type `int`, default `365`.
    Validity in days of the certificates Strimzi issues under the cluster CA (brokers, ZooKeeper, entity operator). Applies at the next issuance; already-issued certificates keep their dates.

`kafka.cluster.entityOperator` <a class="headerlink" href="#helm.kafka.cluster.entityOperator" title="Permanent link">#</a> { #helm.kafka.cluster.entityOperator }
:   Type `object`, default `{}`.
    entity operator configuration for the cluster 

`kafka.cluster.kafka.authorizer.authorizerClass` <a class="headerlink" href="#helm.kafka.cluster.kafka.authorizer.authorizerClass" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.authorizer.authorizerClass }
:   Type `string`, default `"io.hops.kafka.HopsAclAuthorizer"`.

`kafka.cluster.kafka.authorizer.principalBuilderClass` <a class="headerlink" href="#helm.kafka.cluster.kafka.authorizer.principalBuilderClass" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.authorizer.principalBuilderClass }
:   Type `string`, default `"io.hops.kafka.HopsPrincipalBuilder"`.

`kafka.cluster.kafka.authorizer.superUsers` <a class="headerlink" href="#helm.kafka.cluster.kafka.authorizer.superUsers" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.authorizer.superUsers }
:   Type `list`, default `[]`.

`kafka.cluster.kafka.authorizer.type` <a class="headerlink" href="#helm.kafka.cluster.kafka.authorizer.type" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.authorizer.type }
:   Type `string`, default `"custom"`.

`kafka.cluster.kafka.config.database.name` <a class="headerlink" href="#helm.kafka.cluster.kafka.config.database.name" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.config.database.name }
:   Type `string`, default `"hopsworks"`.

`kafka.cluster.kafka.config.log.retention.bytes` <a class="headerlink" href="#helm.kafka.cluster.kafka.config.log.retention.bytes" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.config.log.retention.bytes }
:   Type `int`, default `-1`.
    The maximum size of the log before deleting it.

`kafka.cluster.kafka.config.log.retention.checkIntervalMs` <a class="headerlink" href="#helm.kafka.cluster.kafka.config.log.retention.checkIntervalMs" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.config.log.retention.checkIntervalMs }
:   Type `int`, default `300000`.
    The interval at which log segments are checked for deletion.

`kafka.cluster.kafka.config.log.retention.hours` <a class="headerlink" href="#helm.kafka.cluster.kafka.config.log.retention.hours" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.config.log.retention.hours }
:   Type `int`, default `168`.
    The number of hours to keep a log segment before deleting it.

`kafka.cluster.kafka.dependencies.glassfish.consulServiceName` <a class="headerlink" href="#helm.kafka.cluster.kafka.dependencies.glassfish.consulServiceName" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.dependencies.glassfish.consulServiceName }
:   Type `string`, default `"glassfish"`.

`kafka.cluster.kafka.dependencies.glassfish.consulServiceTag` <a class="headerlink" href="#helm.kafka.cluster.kafka.dependencies.glassfish.consulServiceTag" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.dependencies.glassfish.consulServiceTag }
:   Type `string`, default `"hopsworks"`.

`kafka.cluster.kafka.dependencies.mysql.consulServiceName` <a class="headerlink" href="#helm.kafka.cluster.kafka.dependencies.mysql.consulServiceName" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.dependencies.mysql.consulServiceName }
:   Type `string`, default `"mysql"`.

`kafka.cluster.kafka.dependencies.mysql.port` <a class="headerlink" href="#helm.kafka.cluster.kafka.dependencies.mysql.port" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.dependencies.mysql.port }
:   Type `int`, default `3306`.

`kafka.cluster.kafka.dependencies.onlinefs.consulServiceName` <a class="headerlink" href="#helm.kafka.cluster.kafka.dependencies.onlinefs.consulServiceName" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.dependencies.onlinefs.consulServiceName }
:   Type `string`, default `"onlinefs"`.

`kafka.cluster.kafka.externalLoadBalancer.annotations` <a class="headerlink" href="#helm.kafka.cluster.kafka.externalLoadBalancer.annotations" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.externalLoadBalancer.annotations }
:   Type `object`, default `{}`.
    load balancer annotations

`kafka.cluster.kafka.externalLoadBalancer.class` <a class="headerlink" href="#helm.kafka.cluster.kafka.externalLoadBalancer.class" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.externalLoadBalancer.class }
:   Type `string`, default `nil`.
    load balancer class name

`kafka.cluster.kafka.externalLoadBalancer.dns` <a class="headerlink" href="#helm.kafka.cluster.kafka.externalLoadBalancer.dns" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.externalLoadBalancer.dns }
:   Type `string`, default `""`.
    In case of unmanaged Load Balancers this is the advertised host for the brokers

`kafka.cluster.kafka.externalLoadBalancer.enabled` <a class="headerlink" href="#helm.kafka.cluster.kafka.externalLoadBalancer.enabled" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.externalLoadBalancer.enabled }
:   Type `string`, default `nil`.
    Enable External Load Balancers for Kafka cluster. If not set the .global._hopsworks.externalLoadBalancers.enabled will be used instead

`kafka.cluster.kafka.externalLoadBalancer.finalizers` <a class="headerlink" href="#helm.kafka.cluster.kafka.externalLoadBalancer.finalizers" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.externalLoadBalancer.finalizers }
:   Type `list`, default `[]`.
    A list of finalizers which will be configured for the services created for the external listener.

`kafka.cluster.kafka.externalLoadBalancer.managed` <a class="headerlink" href="#helm.kafka.cluster.kafka.externalLoadBalancer.managed" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.externalLoadBalancer.managed }
:   Type `string`, default `nil`.
    Cloud provider provisions Load Balancers. If not set the .global._hopsworks.externalLoadBalancers.managed will be used instead

`kafka.cluster.kafka.externalLoadBalancer.nodeSelector` <a class="headerlink" href="#helm.kafka.cluster.kafka.externalLoadBalancer.nodeSelector" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.externalLoadBalancer.nodeSelector }
:   Type `object`, default `{}`.
    selector for nodes the load balancer can use to route traffic

`kafka.cluster.kafka.externalLoadBalancer.startingAdvertisedPort` <a class="headerlink" href="#helm.kafka.cluster.kafka.externalLoadBalancer.startingAdvertisedPort" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.externalLoadBalancer.startingAdvertisedPort }
:   Type `int`, default `9093`.
    In case of unmanaged Load Balancers this is the starting advertised port for the brokers  

`kafka.cluster.kafka.jvmOptions` <a class="headerlink" href="#helm.kafka.cluster.kafka.jvmOptions" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.jvmOptions }
:   Type `object`, default `{}`.
    jvm options

`kafka.cluster.kafka.nodeSelector` <a class="headerlink" href="#helm.kafka.cluster.kafka.nodeSelector" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

`kafka.cluster.kafka.podAntiAffinity.required` <a class="headerlink" href="#helm.kafka.cluster.kafka.podAntiAffinity.required" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.podAntiAffinity.required }
:   Type `bool`, default `false`.

`kafka.cluster.kafka.podSecurityContext` <a class="headerlink" href="#helm.kafka.cluster.kafka.podSecurityContext" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.podSecurityContext }
:   Type `object`.
    Pod-level security context for Kafka pods

    ??? note "Default"

        ```yaml
        fsGroup: 1001
        runAsGroup: 1001
        runAsNonRoot: true
        runAsUser: 1001
        seccompProfile:
          type: RuntimeDefault
        ```

`kafka.cluster.kafka.quotas.kafka.consumerByteRate` <a class="headerlink" href="#helm.kafka.cluster.kafka.quotas.kafka.consumerByteRate" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.quotas.kafka.consumerByteRate }
:   Type `string`, default `nil`.
    Built-in plugin only. Default bytes/sec each client may fetch from each broker. Per broker. Unset = none.

`kafka.cluster.kafka.quotas.kafka.controllerMutationRate` <a class="headerlink" href="#helm.kafka.cluster.kafka.quotas.kafka.controllerMutationRate" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.quotas.kafka.controllerMutationRate }
:   Type `string`, default `nil`.
    Built-in plugin only. Default ceiling on partition create/delete mutations per second, per broker. Unset = none.

`kafka.cluster.kafka.quotas.kafka.producerByteRate` <a class="headerlink" href="#helm.kafka.cluster.kafka.quotas.kafka.producerByteRate" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.quotas.kafka.producerByteRate }
:   Type `string`, default `nil`.
    Built-in plugin only. Default bytes/sec each client may publish to each broker. Per broker. Unset = none.

`kafka.cluster.kafka.quotas.kafka.requestPercentage` <a class="headerlink" href="#helm.kafka.cluster.kafka.quotas.kafka.requestPercentage" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.quotas.kafka.requestPercentage }
:   Type `string`, default `nil`.
    Built-in plugin only. Default ceiling on each client's CPU use, as a percentage of a broker's network and I/O threads. Unset = none.

`kafka.cluster.kafka.quotas.minAvailableBytesPerVolume` <a class="headerlink" href="#helm.kafka.cluster.kafka.quotas.minAvailableBytesPerVolume" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.quotas.minAvailableBytesPerVolume }
:   Type `int`, default 0.
    Strimzi plugin only. Halt producers when available bytes per broker volume falls below this value; 0 = disabled

`kafka.cluster.kafka.quotas.minAvailableRatioPerVolume` <a class="headerlink" href="#helm.kafka.cluster.kafka.quotas.minAvailableRatioPerVolume" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.quotas.minAvailableRatioPerVolume }
:   Type `float`, default `0.01`.
    Strimzi plugin only. Halt producers when available ratio per broker volume falls below this value (0.0-1.0)

`kafka.cluster.kafka.quotas.strimzi.consumerByteRate` <a class="headerlink" href="#helm.kafka.cluster.kafka.quotas.strimzi.consumerByteRate" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.quotas.strimzi.consumerByteRate }
:   Type `string`, default `nil`.
    Strimzi plugin only. Per-broker consumer byte-rate shared between all non-excluded clients on that broker. Unset = unlimited.

`kafka.cluster.kafka.quotas.strimzi.excludedPrincipals` <a class="headerlink" href="#helm.kafka.cluster.kafka.quotas.strimzi.excludedPrincipals" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.quotas.strimzi.excludedPrincipals }
:   Type `list`, default `[]`.
    Strimzi plugin only. Principals exempt from the rates above, each prefixed `User:`. Strimzi prepends its own broker and cruise-control principals. A superUser is exempt from ACLs but NOT from quotas, so without an entry here the platform's own clients are throttled by a rate meant for tenants. VERIFY ON THE CLUSTER; do not assume an entry took effect. Strimzi joins this list with ';' and the plugin splits on ';' with no escaping, so a principal whose own name contains ';' cannot be expressed. `authorizer.principalBuilderClass` decides the form: the default Kafka builder yields the certificate DN, which is expressible; this chart's default io.hops.kafka.HopsPrincipalBuilder yields the CN with every differing subject-alternative -name appended and ';'-joined, which is not. The chart fails the render on an entry that lacks the `User:` prefix or contains ';' rather than rendering an exemption that cannot match. Measured on 5.0: onlinefs stayed capped at the configured rate with its entry present. Confirm with kafka-consumer-perf-test.sh.

`kafka.cluster.kafka.quotas.strimzi.producerByteRate` <a class="headerlink" href="#helm.kafka.cluster.kafka.quotas.strimzi.producerByteRate" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.quotas.strimzi.producerByteRate }
:   Type `string`, default `nil`.
    Strimzi plugin only. Per-broker producer byte-rate shared between all non-excluded clients on that broker. Unset = unlimited.

`kafka.cluster.kafka.quotas.type` <a class="headerlink" href="#helm.kafka.cluster.kafka.quotas.type" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.quotas.type }
:   Type `string`, default `"strimzi"`.
    Quota plugin: "strimzi" or "kafka". "strimzi" installs Strimzi's StaticQuotaCallback - a storage guard plus per-broker rates shared between clients, with an exclusion list. "kafka" leaves Kafka's built-in plugin in place - per-user, per-broker limits resolved from config entities, and the only mode in which a KafkaUser's spec.quotas is enforced. Enabling one disables the other.

`kafka.cluster.kafka.quotas.window.num` <a class="headerlink" href="#helm.kafka.cluster.kafka.quotas.window.num" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.quotas.window.num }
:   Type `int`, default `11`.
    Applies under both plugins. Number of samples retained for the quota rate calculation.

`kafka.cluster.kafka.quotas.window.sizeSeconds` <a class="headerlink" href="#helm.kafka.cluster.kafka.quotas.window.sizeSeconds" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.quotas.window.sizeSeconds }
:   Type `int`, default `1`.
    Applies under both plugins. Duration of each quota sample window in seconds.

`kafka.cluster.kafka.replicas` <a class="headerlink" href="#helm.kafka.cluster.kafka.replicas" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.replicas }
:   Type `int`, default `1`.

`kafka.cluster.kafka.resources` <a class="headerlink" href="#helm.kafka.cluster.kafka.resources" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.resources }
:   Type `object`, default `{}`.
    resources configuration

`kafka.cluster.kafka.securityContext` <a class="headerlink" href="#helm.kafka.cluster.kafka.securityContext" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.securityContext }
:   Type `object`.
    Container-level security context for Kafka containers

    ??? note "Default"

        ```yaml
        allowPrivilegeEscalation: false
        capabilities:
          drop:
          - ALL
        runAsGroup: 1001
        runAsNonRoot: true
        runAsUser: 1001
        seccompProfile:
          type: RuntimeDefault
        ```

`kafka.cluster.kafka.services.brokers.annotations."consul.hashicorp.com/service-name"` <a class="headerlink" href="#helm.kafka.cluster.kafka.services.brokers.annotations.consul.hashicorp.com-service-name" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.services.brokers.annotations.consul.hashicorp.com-service-name }
:   Type `string`, default `"kafka"`.

`kafka.cluster.kafka.services.brokers.annotations."consul.hashicorp.com/service-port"` <a class="headerlink" href="#helm.kafka.cluster.kafka.services.brokers.annotations.consul.hashicorp.com-service-port" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.services.brokers.annotations.consul.hashicorp.com-service-port }
:   Type `int`, default `9092`.

`kafka.cluster.kafka.services.brokers.annotations."consul.hashicorp.com/service-tags"` <a class="headerlink" href="#helm.kafka.cluster.kafka.services.brokers.annotations.consul.hashicorp.com-service-tags" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.services.brokers.annotations.consul.hashicorp.com-service-tags }
:   Type `string`, default `"broker"`.

`kafka.cluster.kafka.services.pods.annotations."prometheus.io/path"` <a class="headerlink" href="#helm.kafka.cluster.kafka.services.pods.annotations.prometheus.io-path" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.services.pods.annotations.prometheus.io-path }
:   Type `string`, default `"/metrics"`.

`kafka.cluster.kafka.services.pods.annotations."prometheus.io/port"` <a class="headerlink" href="#helm.kafka.cluster.kafka.services.pods.annotations.prometheus.io-port" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.services.pods.annotations.prometheus.io-port }
:   Type `int`, default `9404`.

`kafka.cluster.kafka.services.pods.annotations."prometheus.io/scheme"` <a class="headerlink" href="#helm.kafka.cluster.kafka.services.pods.annotations.prometheus.io-scheme" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.services.pods.annotations.prometheus.io-scheme }
:   Type `string`, default `"http"`.

`kafka.cluster.kafka.services.pods.annotations."prometheus.io/scrape"` <a class="headerlink" href="#helm.kafka.cluster.kafka.services.pods.annotations.prometheus.io-scrape" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.services.pods.annotations.prometheus.io-scrape }
:   Type `string`, default `"true"`.

`kafka.cluster.kafka.storageClassName` <a class="headerlink" href="#helm.kafka.cluster.kafka.storageClassName" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.storageClassName }
:   Type `string`, default `nil`.
    storage class name

`kafka.cluster.kafka.storageSize` <a class="headerlink" href="#helm.kafka.cluster.kafka.storageSize" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.storageSize }
:   Type `string`, default `"30Gi"`.

`kafka.cluster.kafka.tolerations` <a class="headerlink" href="#helm.kafka.cluster.kafka.tolerations" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.tolerations }
:   Type `list`, default `[]`.

`kafka.cluster.kafka.topologySpreadConstraint` <a class="headerlink" href="#helm.kafka.cluster.kafka.topologySpreadConstraint" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.topologySpreadConstraint }
:   Type `object`, default `{}`.
    The default topology spread constraint. If not defined the global topology spread constraint would be used instead.

`kafka.cluster.kafka.version` <a class="headerlink" href="#helm.kafka.cluster.kafka.version" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.version }
:   Type `string`, default `"3.9.2"`.

`kafka.cluster.name` <a class="headerlink" href="#helm.kafka.cluster.name" title="Permanent link">#</a> { #helm.kafka.cluster.name }
:   Type `string`, default `"kafka-cluster"`.

`kafka.cluster.tlscerts.annotations."certs.hopsworks.ai/owned-by"` <a class="headerlink" href="#helm.kafka.cluster.tlscerts.annotations.certs.hopsworks.ai-owned-by" title="Permanent link">#</a> { #helm.kafka.cluster.tlscerts.annotations.certs.hopsworks.ai-owned-by }
:   Type `string`, default `"deployment-strimzi-cluster-operator"`.

`kafka.cluster.zookeeper.nodeSelector` <a class="headerlink" href="#helm.kafka.cluster.zookeeper.nodeSelector" title="Permanent link">#</a> { #helm.kafka.cluster.zookeeper.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

`kafka.cluster.zookeeper.podAntiAffinity.required` <a class="headerlink" href="#helm.kafka.cluster.zookeeper.podAntiAffinity.required" title="Permanent link">#</a> { #helm.kafka.cluster.zookeeper.podAntiAffinity.required }
:   Type `bool`, default `false`.

`kafka.cluster.zookeeper.podSecurityContext` <a class="headerlink" href="#helm.kafka.cluster.zookeeper.podSecurityContext" title="Permanent link">#</a> { #helm.kafka.cluster.zookeeper.podSecurityContext }
:   Type `object`.
    Pod-level security context for Zookeeper pods

    ??? note "Default"

        ```yaml
        fsGroup: 1001
        runAsGroup: 1001
        runAsNonRoot: true
        runAsUser: 1001
        seccompProfile:
          type: RuntimeDefault
        ```

`kafka.cluster.zookeeper.replicas` <a class="headerlink" href="#helm.kafka.cluster.zookeeper.replicas" title="Permanent link">#</a> { #helm.kafka.cluster.zookeeper.replicas }
:   Type `int`, default `1`.

`kafka.cluster.zookeeper.resources` <a class="headerlink" href="#helm.kafka.cluster.zookeeper.resources" title="Permanent link">#</a> { #helm.kafka.cluster.zookeeper.resources }
:   Type `object`, default `{"limits":{"cpu":"2","memory":"3Gi"},"requests":{"cpu":"200m","memory":"1Gi"}}`.
    resources configuration

`kafka.cluster.zookeeper.securityContext` <a class="headerlink" href="#helm.kafka.cluster.zookeeper.securityContext" title="Permanent link">#</a> { #helm.kafka.cluster.zookeeper.securityContext }
:   Type `object`.
    Container-level security context for Zookeeper containers

    ??? note "Default"

        ```yaml
        allowPrivilegeEscalation: false
        capabilities:
          drop:
          - ALL
        runAsGroup: 1001
        runAsNonRoot: true
        runAsUser: 1001
        seccompProfile:
          type: RuntimeDefault
        ```

`kafka.cluster.zookeeper.services.client.annotations."consul.hashicorp.com/service-name"` <a class="headerlink" href="#helm.kafka.cluster.zookeeper.services.client.annotations.consul.hashicorp.com-service-name" title="Permanent link">#</a> { #helm.kafka.cluster.zookeeper.services.client.annotations.consul.hashicorp.com-service-name }
:   Type `string`, default `"zookeeper"`.

`kafka.cluster.zookeeper.services.client.annotations."consul.hashicorp.com/service-tags"` <a class="headerlink" href="#helm.kafka.cluster.zookeeper.services.client.annotations.consul.hashicorp.com-service-tags" title="Permanent link">#</a> { #helm.kafka.cluster.zookeeper.services.client.annotations.consul.hashicorp.com-service-tags }
:   Type `string`, default `"client"`.

`kafka.cluster.zookeeper.storageClassName` <a class="headerlink" href="#helm.kafka.cluster.zookeeper.storageClassName" title="Permanent link">#</a> { #helm.kafka.cluster.zookeeper.storageClassName }
:   Type `string`, default `nil`.
    storage class name

`kafka.cluster.zookeeper.storageSize` <a class="headerlink" href="#helm.kafka.cluster.zookeeper.storageSize" title="Permanent link">#</a> { #helm.kafka.cluster.zookeeper.storageSize }
:   Type `string`, default `"5Gi"`.

`kafka.cluster.zookeeper.tolerations` <a class="headerlink" href="#helm.kafka.cluster.zookeeper.tolerations" title="Permanent link">#</a> { #helm.kafka.cluster.zookeeper.tolerations }
:   Type `list`, default `[]`.

`kafka.cluster.zookeeper.topologySpreadConstraint` <a class="headerlink" href="#helm.kafka.cluster.zookeeper.topologySpreadConstraint" title="Permanent link">#</a> { #helm.kafka.cluster.zookeeper.topologySpreadConstraint }
:   Type `object`, default `{}`.
    The default topology spread constraint. If not defined the global topology spread constraint would be used instead.

`kafka.cluster.kafka.quotas.defaults.consumerByteRate` <span class="hops-values-deprecated">Deprecated</span> <a class="headerlink" href="#helm.kafka.cluster.kafka.quotas.defaults.consumerByteRate" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.quotas.defaults.consumerByteRate }
:   Type `int`, default `9223372036854775807`.
    Deprecated and no longer honoured.

`kafka.cluster.kafka.quotas.defaults.enabled` <span class="hops-values-deprecated">Deprecated</span> <a class="headerlink" href="#helm.kafka.cluster.kafka.quotas.defaults.enabled" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.quotas.defaults.enabled }
:   Type `bool`, default `false`.
    Deprecated and no longer honoured. Use `quotas.kafka.*` with `type: kafka`, or `quotas.strimzi.*` with `type: strimzi`. Fails the render when combined with `type: kafka`; ignored under `type: strimzi`.

`kafka.cluster.kafka.quotas.defaults.producerByteRate` <span class="hops-values-deprecated">Deprecated</span> <a class="headerlink" href="#helm.kafka.cluster.kafka.quotas.defaults.producerByteRate" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.quotas.defaults.producerByteRate }
:   Type `int`, default `1048576`.
    Deprecated and no longer honoured.

`kafka.cluster.kafka.quotas.defaults.requestPercentage` <span class="hops-values-deprecated">Deprecated</span> <a class="headerlink" href="#helm.kafka.cluster.kafka.quotas.defaults.requestPercentage" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.quotas.defaults.requestPercentage }
:   Type `int`, default `100`.
    Deprecated and no longer honoured.

</div>

<!-- END GENERATED VALUES -->
