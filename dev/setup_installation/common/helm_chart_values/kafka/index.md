# Kafka values { #helm-values-kafka }

Values under `kafka` configure Kafka, run by the Strimzi operator, which carries feature data on its way to the online feature store.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.2.0-alpha-1791370120` (Hopsworks `5.2.0`)._

Deployed when [`global._hopsworks.kafka.enabled`](global.md#helm.global._hopsworks.kafka.enabled) is `true`.

!!! info "Upstream charts"

    - Values under `kafka.strimzi-kafka-operator` go to [`strimzi-kafka-operator` 1.2.0](https://artifacthub.io/packages/helm/strimzi/strimzi-kafka-operator/1.2.0) from `https://strimzi.io/charts/`.

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
        defaultImageTag: 1.2.0
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
:   Type `object`, passed to the [`strimzi-kafka-operator` 1.2.0](https://artifacthub.io/packages/helm/strimzi/strimzi-kafka-operator/1.2.0) chart, whose other values are documented there.
    override values for strimzi operator

    ??? note "Default"

        ```yaml
        createGlobalResources: true
        defaultImageRegistry: docker.hops.works
        defaultImageRepository: strimzi
        defaultImageTag: 1.2.0
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
          image:
            name: kafka
            tag: 1.2.0-kafka-4.3.1-h1
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
          version: 4.3.1
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

`kafka.cluster.kafka.image` <a class="headerlink" href="#helm.kafka.cluster.kafka.image" title="Permanent link">#</a> { #helm.kafka.cluster.kafka.image }
:   Type `object`, default `{"name":"kafka","tag":"1.2.0-kafka-4.3.1-h1"}`.
    a tag docker.hops.works does not carry, because only the `-h<N>` builds are published there. So clearing it also means pointing `strimzi-kafka-operator.defaultImageRegistry` at `quay.io` (or mirroring the plain upstream tags), and the same applies to the operator's Kafka Exporter and Cruise Control defaults if those are ever turned on.

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
    Resources of the broker pods. Applied through the broker KafkaNodePool; the v1 Kafka API has no spec.kafka.resources.

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
:   Type `string`, default `"4.3.1"`.

`kafka.cluster.name` <a class="headerlink" href="#helm.kafka.cluster.name" title="Permanent link">#</a> { #helm.kafka.cluster.name }
:   Type `string`, default `"kafka-cluster"`.

`kafka.cluster.tlscerts.annotations."certs.hopsworks.ai/owned-by"` <a class="headerlink" href="#helm.kafka.cluster.tlscerts.annotations.certs.hopsworks.ai-owned-by" title="Permanent link">#</a> { #helm.kafka.cluster.tlscerts.annotations.certs.hopsworks.ai-owned-by }
:   Type `string`, default `"deployment-strimzi-cluster-operator"`.

`kafka.cluster.zookeeper` <a class="headerlink" href="#helm.kafka.cluster.zookeeper" title="Permanent link">#</a> { #helm.kafka.cluster.zookeeper }
:   Type `object`.
    Sizing and scheduling for the KRaft **controller pool**, despite the name. No ZooKeeper ensemble is deployed any more - Strimzi 1.x has no `.spec.zookeeper` - but controllers replace that ensemble one-for-one, so `kafka.controllerConfig` keeps reading these values: a 3-node quorum stays a 3-node quorum with the same storage, resources, scheduling and security context, and no values change is needed. The key keeps its name because renaming it would break every existing values file.

    ??? note "Default"

        ```yaml
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

`kafka.cluster.zookeeper.nodeSelector` <a class="headerlink" href="#helm.kafka.cluster.zookeeper.nodeSelector" title="Permanent link">#</a> { #helm.kafka.cluster.zookeeper.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

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

`kafka.cluster.zookeeper.storageClassName` <a class="headerlink" href="#helm.kafka.cluster.zookeeper.storageClassName" title="Permanent link">#</a> { #helm.kafka.cluster.zookeeper.storageClassName }
:   Type `string`, default `nil`.
    storage class name

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

## crdUpgradeJob { #helm-values-kafka-crdupgradejob }

??? example "Defaults as YAML"

    ```yaml
    kafka:
      crdUpgradeJob:
        enabled: true
        image:
          name: crds
          tag: 1.2.0-h1
        name: strimzi-crd-upgrade
        nodeSelector: {}
        resources:
          limits:
            cpu: 500m
            memory: 512Mi
          requests:
            cpu: 100m
            memory: 128Mi
        serviceAccount:
          annotations: {}
        tolerations: []
        ttlSecondsAfterFinished: null
    ```

<div class="hops-values" markdown>

`kafka.crdUpgradeJob.enabled` <a class="headerlink" href="#helm.kafka.crdUpgradeJob.enabled" title="Permanent link">#</a> { #helm.kafka.crdUpgradeJob.enabled }
:   Type `bool`, default `true`.
    Run the Job that keeps the Strimzi CRDs in step with the operator this chart deploys, and preflights the KRaft migration. It runs pre-install and pre-upgrade: Helm applies the operator subchart's `crds/` on install only and skips any CRD that already exists, so every other path goes through here. A cluster whose objects are still stored as `v1beta2` is converted first (through the 0.51.0 bundle in `image`), which leaves both API versions served until the next upgrade renders `v1` and finishes the move to the 1.2.0 bundle. A failed *refresh* is not fatal by itself - it repairs rather than gates, so a failed apply warns and lets the upgrade continue - but the Job then refuses the upgrade when the live CRDs are too old for the Kafka resource this chart renders. The preflight checks are fatal: they only fire on states that would corrupt or roll back a cluster.

`kafka.crdUpgradeJob.image` <a class="headerlink" href="#helm.kafka.crdUpgradeJob.image" title="Permanent link">#</a> { #helm.kafka.crdUpgradeJob.image }
:   Type `object`, default `{"name":"crds","tag":"1.2.0-h1"}`.
    Image carrying the CRD bundles the Job applies: `strimzi-crds-<version>.yaml` for the Strimzi version this chart depends on, and the 0.51.0 bundle a cluster still storing `v1beta2` is converted through (Kubernetes refuses to drop a version still listed in a CRD's `status.storedVersions`, and 0.51.0 is the last Strimzi release to serve both). Built by `strimzi-crds` in the docker-images repo and pulled from the operator's `defaultImageRegistry`/`defaultImageRepository` like the broker image, so an airgapped install mirrors it with the rest (`vendor_images.sh` includes it). The tag's Strimzi part must match the dependency version: the Job refuses the upgrade when the bundle it needs is not in the image.

`kafka.crdUpgradeJob.name` <a class="headerlink" href="#helm.kafka.crdUpgradeJob.name" title="Permanent link">#</a> { #helm.kafka.crdUpgradeJob.name }
:   Type `string`, default `"strimzi-crd-upgrade"`.

`kafka.crdUpgradeJob.nodeSelector` <a class="headerlink" href="#helm.kafka.crdUpgradeJob.nodeSelector" title="Permanent link">#</a> { #helm.kafka.crdUpgradeJob.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

`kafka.crdUpgradeJob.resources` <a class="headerlink" href="#helm.kafka.crdUpgradeJob.resources" title="Permanent link">#</a> { #helm.kafka.crdUpgradeJob.resources }
:   Type `object`.
    resources configuration. Both halves are set deliberately: a namespace LimitRange defaults per resource, so a container that declares only requests still has limits injected - at whatever the operator's default is, which is high enough on some clusters to exhaust a ResourceQuota or stop the pod scheduling outright. The Job runs kubectl over about 1 MB of CRD YAML, so it is sized like the `tool` tier of hopsworkslib.initContainerResources.

    ??? note "Default"

        ```yaml
        limits:
          cpu: 500m
          memory: 512Mi
        requests:
          cpu: 100m
          memory: 128Mi
        ```

`kafka.crdUpgradeJob.serviceAccount.annotations` <a class="headerlink" href="#helm.kafka.crdUpgradeJob.serviceAccount.annotations" title="Permanent link">#</a> { #helm.kafka.crdUpgradeJob.serviceAccount.annotations }
:   Type `object`, default `{}`.
    service account annotations

`kafka.crdUpgradeJob.tolerations` <a class="headerlink" href="#helm.kafka.crdUpgradeJob.tolerations" title="Permanent link">#</a> { #helm.kafka.crdUpgradeJob.tolerations }
:   Type `list`, default `[]`.

`kafka.crdUpgradeJob.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.kafka.crdUpgradeJob.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.kafka.crdUpgradeJob.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    ttlSecondsAfterFinished for the Job; null falls through to the global default

</div>

## migrationJob { #helm-values-kafka-migrationjob }

??? example "Defaults as YAML"

    ```yaml
    kafka:
      migrationJob:
        enabled: true
        name: kafka-kraft-migration
        nodeSelector: {}
        resources:
          limits:
            cpu: 500m
            memory: 512Mi
          requests:
            cpu: 100m
            memory: 128Mi
        serviceAccount:
          annotations: {}
        timeoutSeconds: 1800
        tolerations: []
        ttlSecondsAfterFinished: null
    ```

<div class="hops-values" markdown>

`kafka.migrationJob.enabled` <a class="headerlink" href="#helm.kafka.migrationJob.enabled" title="Permanent link">#</a> { #helm.kafka.migrationJob.enabled }
:   Type `bool`, default `true`.
    Run the pre-upgrade Job that carries a ZooKeeper-based cluster to KRaft before the rest of the upgrade is applied. It exits immediately on a cluster that is already on KRaft, so leaving it on costs one short Job per upgrade. Turning it off on a cluster that still needs migrating does not make the upgrade work - it makes it fail later, in the preflight, because the Strimzi this chart ships cannot serve a ZooKeeper cluster at all.

`kafka.migrationJob.name` <a class="headerlink" href="#helm.kafka.migrationJob.name" title="Permanent link">#</a> { #helm.kafka.migrationJob.name }
:   Type `string`, default `"kafka-kraft-migration"`.

`kafka.migrationJob.nodeSelector` <a class="headerlink" href="#helm.kafka.migrationJob.nodeSelector" title="Permanent link">#</a> { #helm.kafka.migrationJob.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

`kafka.migrationJob.resources` <a class="headerlink" href="#helm.kafka.migrationJob.resources" title="Permanent link">#</a> { #helm.kafka.migrationJob.resources }
:   Type `object`.
    resources configuration. Requests and limits both set, for the reason given on `crdUpgradeJob.resources`. This one only polls kubectl in a sleep loop.

    ??? note "Default"

        ```yaml
        limits:
          cpu: 500m
          memory: 512Mi
        requests:
          cpu: 100m
          memory: 128Mi
        ```

`kafka.migrationJob.serviceAccount.annotations` <a class="headerlink" href="#helm.kafka.migrationJob.serviceAccount.annotations" title="Permanent link">#</a> { #helm.kafka.migrationJob.serviceAccount.annotations }
:   Type `object`, default `{}`.
    service account annotations

`kafka.migrationJob.timeoutSeconds` <a class="headerlink" href="#helm.kafka.migrationJob.timeoutSeconds" title="Permanent link">#</a> { #helm.kafka.migrationJob.timeoutSeconds }
:   Type `int`, default `1800`.
    How long to wait, in seconds, for Strimzi to reach KRaftPostMigration and then KRaft. Each wait gets this budget separately. On timeout the Job fails and so does the upgrade, but the cluster is not stranded: the operator keeps migrating regardless of this Job, so the next upgrade picks up wherever it got to.

`kafka.migrationJob.tolerations` <a class="headerlink" href="#helm.kafka.migrationJob.tolerations" title="Permanent link">#</a> { #helm.kafka.migrationJob.tolerations }
:   Type `list`, default `[]`.

`kafka.migrationJob.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.kafka.migrationJob.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.kafka.migrationJob.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    ttlSecondsAfterFinished for the Job; null falls through to the global default

</div>

<!-- END GENERATED VALUES -->
