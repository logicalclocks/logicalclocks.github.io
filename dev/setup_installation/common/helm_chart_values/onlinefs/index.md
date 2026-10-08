# OnlineFS values { #helm-values-onlinefs }

Values under `onlinefs` configure OnlineFS, which consumes feature rows from Kafka and writes them to RonDB.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.2.0-alpha-1791477965` (Hopsworks `5.2.0`)._

Always deployed.

## General { #helm-values-onlinefs-general }

??? example "Defaults as YAML"

    ```yaml
    onlinefs:
      apiKey:
        email: onlinefs@hopsworks.ai
        password: onlinefspw
        secret_name: onlinefs-api-key-auth
      appName: onlinefs
      configmap:
        name: onlinefs-configmap
      debug: false
      hopsworkslib: {}
      hpa:
        enabled: false
        maxReplicas: 5
        targetCPUUtilizationPercentage: 80
        targetMemoryUtilizationPercentage: 80
      nodeSelector: {}
      podDisruptionBudget:
        enabled: true
        minAvailable: 1
      serviceAccount:
        annotations: {}
        create: true
        name: onlinefs-default
      setupBackOffLimit: 10
      tlscerts:
        commonName: ''
        locality: onlinefs
      tolerations: []
      topologySpreadConstraint: {}
    ```

<div class="hops-values" markdown>

`onlinefs` <a class="headerlink" href="#helm.onlinefs" title="Permanent link">#</a> { #helm.onlinefs }
:   Type `object`, default `{"debug":false}`.
    override onlinefs values

`onlinefs.apiKey.email` <a class="headerlink" href="#helm.onlinefs.apiKey.email" title="Permanent link">#</a> { #helm.onlinefs.apiKey.email }
:   Type `string`, default `"onlinefs@hopsworks.ai"`.

`onlinefs.apiKey.password` <a class="headerlink" href="#helm.onlinefs.apiKey.password" title="Permanent link">#</a> { #helm.onlinefs.apiKey.password }
:   Type `string`, default `"onlinefspw"`.

`onlinefs.apiKey.secret_name` <a class="headerlink" href="#helm.onlinefs.apiKey.secret_name" title="Permanent link">#</a> { #helm.onlinefs.apiKey.secret_name }
:   Type `string`, default `"onlinefs-api-key-auth"`.

`onlinefs.appName` <a class="headerlink" href="#helm.onlinefs.appName" title="Permanent link">#</a> { #helm.onlinefs.appName }
:   Type `string`, default `"onlinefs"`.

`onlinefs.configmap.name` <a class="headerlink" href="#helm.onlinefs.configmap.name" title="Permanent link">#</a> { #helm.onlinefs.configmap.name }
:   Type `string`, default `"onlinefs-configmap"`.

`onlinefs.debug` <a class="headerlink" href="#helm.onlinefs.debug" title="Permanent link">#</a> { #helm.onlinefs.debug }
:   Type `bool`, default `false`.

`onlinefs.hopsworkslib` <a class="headerlink" href="#helm.onlinefs.hopsworkslib" title="Permanent link">#</a> { #helm.onlinefs.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`onlinefs.hpa.enabled` <a class="headerlink" href="#helm.onlinefs.hpa.enabled" title="Permanent link">#</a> { #helm.onlinefs.hpa.enabled }
:   Type `bool`, default `false`.
    Autoscale the Deployment with an HPA. While enabled, deployment.replicas is not rendered and the HPA owns spec.replicas.

`onlinefs.hpa.maxReplicas` <a class="headerlink" href="#helm.onlinefs.hpa.maxReplicas" title="Permanent link">#</a> { #helm.onlinefs.hpa.maxReplicas }
:   Type `int`, default `5`.

`onlinefs.hpa.targetCPUUtilizationPercentage` <a class="headerlink" href="#helm.onlinefs.hpa.targetCPUUtilizationPercentage" title="Permanent link">#</a> { #helm.onlinefs.hpa.targetCPUUtilizationPercentage }
:   Type `int`, default `80`.

`onlinefs.hpa.targetMemoryUtilizationPercentage` <a class="headerlink" href="#helm.onlinefs.hpa.targetMemoryUtilizationPercentage" title="Permanent link">#</a> { #helm.onlinefs.hpa.targetMemoryUtilizationPercentage }
:   Type `int`, default `80`.

`onlinefs.nodeSelector` <a class="headerlink" href="#helm.onlinefs.nodeSelector" title="Permanent link">#</a> { #helm.onlinefs.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

`onlinefs.podDisruptionBudget.enabled` <a class="headerlink" href="#helm.onlinefs.podDisruptionBudget.enabled" title="Permanent link">#</a> { #helm.onlinefs.podDisruptionBudget.enabled }
:   Type `bool`, default `true`.

`onlinefs.podDisruptionBudget.minAvailable` <a class="headerlink" href="#helm.onlinefs.podDisruptionBudget.minAvailable" title="Permanent link">#</a> { #helm.onlinefs.podDisruptionBudget.minAvailable }
:   Type `int`, default `1`.

`onlinefs.serviceAccount.annotations` <a class="headerlink" href="#helm.onlinefs.serviceAccount.annotations" title="Permanent link">#</a> { #helm.onlinefs.serviceAccount.annotations }
:   Type `object`, default `{}`.
    service account annotations

`onlinefs.serviceAccount.create` <a class="headerlink" href="#helm.onlinefs.serviceAccount.create" title="Permanent link">#</a> { #helm.onlinefs.serviceAccount.create }
:   Type `bool`, default `true`.

`onlinefs.serviceAccount.name` <a class="headerlink" href="#helm.onlinefs.serviceAccount.name" title="Permanent link">#</a> { #helm.onlinefs.serviceAccount.name }
:   Type `string`, default `"onlinefs-default"`.

`onlinefs.setupBackOffLimit` <a class="headerlink" href="#helm.onlinefs.setupBackOffLimit" title="Permanent link">#</a> { #helm.onlinefs.setupBackOffLimit }
:   Type `int`, default `10`.

`onlinefs.tlscerts.commonName` <a class="headerlink" href="#helm.onlinefs.tlscerts.commonName" title="Permanent link">#</a> { #helm.onlinefs.tlscerts.commonName }
:   Type `string`, default `""`.

`onlinefs.tlscerts.locality` <a class="headerlink" href="#helm.onlinefs.tlscerts.locality" title="Permanent link">#</a> { #helm.onlinefs.tlscerts.locality }
:   Type `string`, default `"onlinefs"`.

`onlinefs.tolerations` <a class="headerlink" href="#helm.onlinefs.tolerations" title="Permanent link">#</a> { #helm.onlinefs.tolerations }
:   Type `list`, default `[]`.

`onlinefs.topologySpreadConstraint` <a class="headerlink" href="#helm.onlinefs.topologySpreadConstraint" title="Permanent link">#</a> { #helm.onlinefs.topologySpreadConstraint }
:   Type `object`, default `{}`.
    The default topology spread constraint. If not defined the global topology spread constraint would be used instead.

</div>

## configmapOverrides { #helm-values-onlinefs-configmapoverrides }

??? example "Defaults as YAML"

    ```yaml
    onlinefs:
      configmapOverrides:
        kafka: {}
        kafkaVectorDb: {}
        log4j: {}
        onlinefssite:
          hopsworks:
            tokenLocation: /onlinefs/etc/token
          kafkaConsumer:
            pollTimeoutMs: 1000
            topicList: ''
            topicPattern: .*_onlinefs
          rondb:
            batchSize: 300
            maxCachedInstances: 1024
            maxCachedSessions: 20
            maxTransactions: 1024
            poolSize: 1
            reconnectTimeout: 5
            useDynamicObjectCache: false
            useSessionCache: false
          service:
            featureGroupCacheExpire: 30
            featureStoreCacheExpire: 30
            featureViewCacheExpire: 10
            getSessionRetrySleepMs: 100
            maxBlacklistSize: 100
            maxFeatureGroupCacheSize: 1000
            maxFeatureStoreCacheSize: 1000
            maxFeatureViewCacheSize: 1000
            pauseRetrySleepMs: 5000
            ronDbThreadNumber: 10
            threadNumber: 10
            vectorDbThreadNumber: 10
        producer: {}
    ```

<div class="hops-values" markdown>

`onlinefs.configmapOverrides.kafka` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.kafka" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.kafka }
:   Type `object`, default `{}`.
    Extra properties to add or overwrite in onlinefs-kafka.properties

`onlinefs.configmapOverrides.kafkaVectorDb` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.kafkaVectorDb" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.kafkaVectorDb }
:   Type `object`, default `{}`.
    Extra properties to add or overwrite in onlinefs-kafka-vector-db.properties

`onlinefs.configmapOverrides.log4j` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.log4j" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.log4j }
:   Type `object`, default `{}`.
    Extra properties to add or overwrite in log4j.properties

`onlinefs.configmapOverrides.onlinefssite.hopsworks.tokenLocation` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.onlinefssite.hopsworks.tokenLocation" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.onlinefssite.hopsworks.tokenLocation }
:   Type `string`, default `"/onlinefs/etc/token"`.

`onlinefs.configmapOverrides.onlinefssite.kafkaConsumer.pollTimeoutMs` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.onlinefssite.kafkaConsumer.pollTimeoutMs" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.onlinefssite.kafkaConsumer.pollTimeoutMs }
:   Type `int`, default `1000`.

`onlinefs.configmapOverrides.onlinefssite.kafkaConsumer.topicList` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.onlinefssite.kafkaConsumer.topicList" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.onlinefssite.kafkaConsumer.topicList }
:   Type `string`, default `""`.

`onlinefs.configmapOverrides.onlinefssite.kafkaConsumer.topicPattern` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.onlinefssite.kafkaConsumer.topicPattern" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.onlinefssite.kafkaConsumer.topicPattern }
:   Type `string`, default `".*_onlinefs"`.

`onlinefs.configmapOverrides.onlinefssite.rondb.batchSize` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.onlinefssite.rondb.batchSize" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.onlinefssite.rondb.batchSize }
:   Type `int`, default `300`.

`onlinefs.configmapOverrides.onlinefssite.rondb.maxCachedInstances` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.onlinefssite.rondb.maxCachedInstances" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.onlinefssite.rondb.maxCachedInstances }
:   Type `int`, default `1024`.

`onlinefs.configmapOverrides.onlinefssite.rondb.maxCachedSessions` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.onlinefssite.rondb.maxCachedSessions" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.onlinefssite.rondb.maxCachedSessions }
:   Type `int`, default `20`.

`onlinefs.configmapOverrides.onlinefssite.rondb.maxTransactions` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.onlinefssite.rondb.maxTransactions" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.onlinefssite.rondb.maxTransactions }
:   Type `int`, default `1024`.

`onlinefs.configmapOverrides.onlinefssite.rondb.poolSize` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.onlinefssite.rondb.poolSize" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.onlinefssite.rondb.poolSize }
:   Type `int`, default `1`.

`onlinefs.configmapOverrides.onlinefssite.rondb.reconnectTimeout` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.onlinefssite.rondb.reconnectTimeout" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.onlinefssite.rondb.reconnectTimeout }
:   Type `int`, default `5`.

`onlinefs.configmapOverrides.onlinefssite.rondb.useDynamicObjectCache` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.onlinefssite.rondb.useDynamicObjectCache" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.onlinefssite.rondb.useDynamicObjectCache }
:   Type `bool`, default `false`.

`onlinefs.configmapOverrides.onlinefssite.rondb.useSessionCache` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.onlinefssite.rondb.useSessionCache" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.onlinefssite.rondb.useSessionCache }
:   Type `bool`, default `false`.

`onlinefs.configmapOverrides.onlinefssite.service.featureGroupCacheExpire` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.onlinefssite.service.featureGroupCacheExpire" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.onlinefssite.service.featureGroupCacheExpire }
:   Type `int`, default `30`.

`onlinefs.configmapOverrides.onlinefssite.service.featureStoreCacheExpire` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.onlinefssite.service.featureStoreCacheExpire" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.onlinefssite.service.featureStoreCacheExpire }
:   Type `int`, default `30`.

`onlinefs.configmapOverrides.onlinefssite.service.featureViewCacheExpire` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.onlinefssite.service.featureViewCacheExpire" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.onlinefssite.service.featureViewCacheExpire }
:   Type `int`, default `10`.

`onlinefs.configmapOverrides.onlinefssite.service.getSessionRetrySleepMs` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.onlinefssite.service.getSessionRetrySleepMs" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.onlinefssite.service.getSessionRetrySleepMs }
:   Type `int`, default `100`.

`onlinefs.configmapOverrides.onlinefssite.service.maxBlacklistSize` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.onlinefssite.service.maxBlacklistSize" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.onlinefssite.service.maxBlacklistSize }
:   Type `int`, default `100`.

`onlinefs.configmapOverrides.onlinefssite.service.maxFeatureGroupCacheSize` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.onlinefssite.service.maxFeatureGroupCacheSize" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.onlinefssite.service.maxFeatureGroupCacheSize }
:   Type `int`, default `1000`.

`onlinefs.configmapOverrides.onlinefssite.service.maxFeatureStoreCacheSize` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.onlinefssite.service.maxFeatureStoreCacheSize" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.onlinefssite.service.maxFeatureStoreCacheSize }
:   Type `int`, default `1000`.

`onlinefs.configmapOverrides.onlinefssite.service.maxFeatureViewCacheSize` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.onlinefssite.service.maxFeatureViewCacheSize" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.onlinefssite.service.maxFeatureViewCacheSize }
:   Type `int`, default `1000`.

`onlinefs.configmapOverrides.onlinefssite.service.pauseRetrySleepMs` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.onlinefssite.service.pauseRetrySleepMs" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.onlinefssite.service.pauseRetrySleepMs }
:   Type `int`, default `5000`.

`onlinefs.configmapOverrides.onlinefssite.service.ronDbThreadNumber` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.onlinefssite.service.ronDbThreadNumber" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.onlinefssite.service.ronDbThreadNumber }
:   Type `int`, default `10`.

`onlinefs.configmapOverrides.onlinefssite.service.threadNumber` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.onlinefssite.service.threadNumber" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.onlinefssite.service.threadNumber }
:   Type `int`, default `10`.

`onlinefs.configmapOverrides.onlinefssite.service.vectorDbThreadNumber` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.onlinefssite.service.vectorDbThreadNumber" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.onlinefssite.service.vectorDbThreadNumber }
:   Type `int`, default `10`.

`onlinefs.configmapOverrides.producer` <a class="headerlink" href="#helm.onlinefs.configmapOverrides.producer" title="Permanent link">#</a> { #helm.onlinefs.configmapOverrides.producer }
:   Type `object`, default `{}`.
    Extra properties to add or overwrite in producer.properties

</div>

## dependencies { #helm-values-onlinefs-dependencies }

??? example "Defaults as YAML"

    ```yaml
    onlinefs:
      dependencies:
        glassfish:
          consulServiceName: glassfish
          consulServiceTag: hopsworks
          port: 8182
        kafka:
          consulServiceName: kafka
          consulServiceTag: broker
          port: 9092
          securityProtocol: SSL
          url: ''
        mgmd:
          consulServiceName: mgmd
          port: 1186
          url: ''
        opensearch:
          consulServiceName: elastic
          consulServiceTag: rest
          port: 9200
    ```

<div class="hops-values" markdown>

`onlinefs.dependencies.glassfish.consulServiceName` <a class="headerlink" href="#helm.onlinefs.dependencies.glassfish.consulServiceName" title="Permanent link">#</a> { #helm.onlinefs.dependencies.glassfish.consulServiceName }
:   Type `string`, default `"glassfish"`.

`onlinefs.dependencies.glassfish.consulServiceTag` <a class="headerlink" href="#helm.onlinefs.dependencies.glassfish.consulServiceTag" title="Permanent link">#</a> { #helm.onlinefs.dependencies.glassfish.consulServiceTag }
:   Type `string`, default `"hopsworks"`.

`onlinefs.dependencies.glassfish.port` <a class="headerlink" href="#helm.onlinefs.dependencies.glassfish.port" title="Permanent link">#</a> { #helm.onlinefs.dependencies.glassfish.port }
:   Type `int`, default `8182`.

`onlinefs.dependencies.kafka.consulServiceName` <a class="headerlink" href="#helm.onlinefs.dependencies.kafka.consulServiceName" title="Permanent link">#</a> { #helm.onlinefs.dependencies.kafka.consulServiceName }
:   Type `string`, default `"kafka"`.

`onlinefs.dependencies.kafka.consulServiceTag` <a class="headerlink" href="#helm.onlinefs.dependencies.kafka.consulServiceTag" title="Permanent link">#</a> { #helm.onlinefs.dependencies.kafka.consulServiceTag }
:   Type `string`, default `"broker"`.

`onlinefs.dependencies.kafka.port` <a class="headerlink" href="#helm.onlinefs.dependencies.kafka.port" title="Permanent link">#</a> { #helm.onlinefs.dependencies.kafka.port }
:   Type `int`, default `9092`.

`onlinefs.dependencies.kafka.securityProtocol` <a class="headerlink" href="#helm.onlinefs.dependencies.kafka.securityProtocol" title="Permanent link">#</a> { #helm.onlinefs.dependencies.kafka.securityProtocol }
:   Type `string`, default `"SSL"`.
    Kafka security.protocol. PLAINTEXT or SSL

`onlinefs.dependencies.kafka.url` <a class="headerlink" href="#helm.onlinefs.dependencies.kafka.url" title="Permanent link">#</a> { #helm.onlinefs.dependencies.kafka.url }
:   Type `string`, default `""`.
    The Kafka Brokers URL (can be comma-separated urls with port or a single url), if not set the consul DNS name will be used

`onlinefs.dependencies.mgmd.consulServiceName` <a class="headerlink" href="#helm.onlinefs.dependencies.mgmd.consulServiceName" title="Permanent link">#</a> { #helm.onlinefs.dependencies.mgmd.consulServiceName }
:   Type `string`, default `"mgmd"`.

`onlinefs.dependencies.mgmd.port` <a class="headerlink" href="#helm.onlinefs.dependencies.mgmd.port" title="Permanent link">#</a> { #helm.onlinefs.dependencies.mgmd.port }
:   Type `int`, default `1186`.

`onlinefs.dependencies.mgmd.url` <a class="headerlink" href="#helm.onlinefs.dependencies.mgmd.url" title="Permanent link">#</a> { #helm.onlinefs.dependencies.mgmd.url }
:   Type `string`, default `""`.
    The mgmd URL, if not set the consul DNS name will be used

`onlinefs.dependencies.opensearch.consulServiceName` <a class="headerlink" href="#helm.onlinefs.dependencies.opensearch.consulServiceName" title="Permanent link">#</a> { #helm.onlinefs.dependencies.opensearch.consulServiceName }
:   Type `string`, default `"elastic"`.

`onlinefs.dependencies.opensearch.consulServiceTag` <a class="headerlink" href="#helm.onlinefs.dependencies.opensearch.consulServiceTag" title="Permanent link">#</a> { #helm.onlinefs.dependencies.opensearch.consulServiceTag }
:   Type `string`, default `"rest"`.

`onlinefs.dependencies.opensearch.port` <a class="headerlink" href="#helm.onlinefs.dependencies.opensearch.port" title="Permanent link">#</a> { #helm.onlinefs.dependencies.opensearch.port }
:   Type `int`, default `9200`.

</div>

## deployment { #helm-values-onlinefs-deployment }

??? example "Defaults as YAML"

    ```yaml
    onlinefs:
      deployment:
        env:
          JAVA_OPTS: -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:9029
        name: onlinefs-deployment
        ports:
          debug: 9029
          monitor: 12800
        replicas: 1
        resources:
          limits:
            cpu: '4'
            memory: 4096Mi
          requests:
            cpu: '2'
            memory: 1024Mi
        strategy: {}
        vectordb:
          enabled: true
    ```

<div class="hops-values" markdown>

`onlinefs.deployment.env.JAVA_OPTS` <a class="headerlink" href="#helm.onlinefs.deployment.env.JAVA_OPTS" title="Permanent link">#</a> { #helm.onlinefs.deployment.env.JAVA_OPTS }
:   Type `string`, default `"-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:9029"`.

`onlinefs.deployment.name` <a class="headerlink" href="#helm.onlinefs.deployment.name" title="Permanent link">#</a> { #helm.onlinefs.deployment.name }
:   Type `string`, default `"onlinefs-deployment"`.

`onlinefs.deployment.ports.debug` <a class="headerlink" href="#helm.onlinefs.deployment.ports.debug" title="Permanent link">#</a> { #helm.onlinefs.deployment.ports.debug }
:   Type `int`, default `9029`.

`onlinefs.deployment.ports.monitor` <a class="headerlink" href="#helm.onlinefs.deployment.ports.monitor" title="Permanent link">#</a> { #helm.onlinefs.deployment.ports.monitor }
:   Type `int`, default `12800`.

`onlinefs.deployment.replicas` <a class="headerlink" href="#helm.onlinefs.deployment.replicas" title="Permanent link">#</a> { #helm.onlinefs.deployment.replicas }
:   Type `int`, default `1`.
    Number of replicas. Not rendered while hpa.enabled is true: the HPA then owns spec.replicas and this value is its minReplicas. Turning the HPA on for a running release drops the Deployment to 1 once, until the HPA scales it back up.

`onlinefs.deployment.resources.limits.cpu` <a class="headerlink" href="#helm.onlinefs.deployment.resources.limits.cpu" title="Permanent link">#</a> { #helm.onlinefs.deployment.resources.limits.cpu }
:   Type `string`, default `"4"`.

`onlinefs.deployment.resources.limits.memory` <a class="headerlink" href="#helm.onlinefs.deployment.resources.limits.memory" title="Permanent link">#</a> { #helm.onlinefs.deployment.resources.limits.memory }
:   Type `string`, default `"4096Mi"`.

`onlinefs.deployment.resources.requests.cpu` <a class="headerlink" href="#helm.onlinefs.deployment.resources.requests.cpu" title="Permanent link">#</a> { #helm.onlinefs.deployment.resources.requests.cpu }
:   Type `string`, default `"2"`.

`onlinefs.deployment.resources.requests.memory` <a class="headerlink" href="#helm.onlinefs.deployment.resources.requests.memory" title="Permanent link">#</a> { #helm.onlinefs.deployment.resources.requests.memory }
:   Type `string`, default `"1024Mi"`.

`onlinefs.deployment.strategy` <a class="headerlink" href="#helm.onlinefs.deployment.strategy" title="Permanent link">#</a> { #helm.onlinefs.deployment.strategy }
:   Type `object`, default `{}`.
    spec.strategy of the Deployment, rendered as given when set. Left empty, two or more replicas roll out by terminating a pod before creating its replacement (maxSurge 0, maxUnavailable 1), so an upgrade completes on a node pool with no room for an extra pod, and a single replica keeps the Kubernetes default. Set it explicitly for a single-replica install whose node pool cannot fit a surge pod, or to keep surge-first behaviour on an install with spare capacity that would rather not drop a consumer during a rollout.

`onlinefs.deployment.vectordb.enabled` <a class="headerlink" href="#helm.onlinefs.deployment.vectordb.enabled" title="Permanent link">#</a> { #helm.onlinefs.deployment.vectordb.enabled }
:   Type `bool`, default `true`.

</div>

## rbac { #helm-values-onlinefs-rbac }

??? example "Defaults as YAML"

    ```yaml
    onlinefs:
      rbac:
        annotations: {}
        create: true
        extraRoleRules: []
        name: onlinefs-role
        useExistingRole: false
    ```

<div class="hops-values" markdown>

`onlinefs.rbac.annotations` <a class="headerlink" href="#helm.onlinefs.rbac.annotations" title="Permanent link">#</a> { #helm.onlinefs.rbac.annotations }
:   Type `object`, default `{}`.
    rbac annotations

`onlinefs.rbac.create` <a class="headerlink" href="#helm.onlinefs.rbac.create" title="Permanent link">#</a> { #helm.onlinefs.rbac.create }
:   Type `bool`, default `true`.

`onlinefs.rbac.extraRoleRules` <a class="headerlink" href="#helm.onlinefs.rbac.extraRoleRules" title="Permanent link">#</a> { #helm.onlinefs.rbac.extraRoleRules }
:   Type `list`, default `[]`.

`onlinefs.rbac.name` <a class="headerlink" href="#helm.onlinefs.rbac.name" title="Permanent link">#</a> { #helm.onlinefs.rbac.name }
:   Type `string`, default `"onlinefs-role"`.

`onlinefs.rbac.useExistingRole` <a class="headerlink" href="#helm.onlinefs.rbac.useExistingRole" title="Permanent link">#</a> { #helm.onlinefs.rbac.useExistingRole }
:   Type `bool`, default `false`.

</div>

## service { #helm-values-onlinefs-service }

??? example "Defaults as YAML"

    ```yaml
    onlinefs:
      service:
        debug:
          annotations:
            consul.hashicorp.com/service-name: onlinefs
            consul.hashicorp.com/service-tags: debug
          name: onlinefs-debug
          port: 9029
        monitoring:
          annotations:
            consul.hashicorp.com/service-name: onlinefs
            consul.hashicorp.com/service-tags: monitor
            prometheus.io/path: /metrics
            prometheus.io/port: 12800
            prometheus.io/scheme: http
            prometheus.io/scrape: 'true'
          name: onlinefs-monitor
          port: 12800
    ```

<div class="hops-values" markdown>

`onlinefs.service.debug.annotations."consul.hashicorp.com/service-name"` <a class="headerlink" href="#helm.onlinefs.service.debug.annotations.consul.hashicorp.com-service-name" title="Permanent link">#</a> { #helm.onlinefs.service.debug.annotations.consul.hashicorp.com-service-name }
:   Type `string`, default `"onlinefs"`.

`onlinefs.service.debug.annotations."consul.hashicorp.com/service-tags"` <a class="headerlink" href="#helm.onlinefs.service.debug.annotations.consul.hashicorp.com-service-tags" title="Permanent link">#</a> { #helm.onlinefs.service.debug.annotations.consul.hashicorp.com-service-tags }
:   Type `string`, default `"debug"`.

`onlinefs.service.debug.name` <a class="headerlink" href="#helm.onlinefs.service.debug.name" title="Permanent link">#</a> { #helm.onlinefs.service.debug.name }
:   Type `string`, default `"onlinefs-debug"`.

`onlinefs.service.debug.port` <a class="headerlink" href="#helm.onlinefs.service.debug.port" title="Permanent link">#</a> { #helm.onlinefs.service.debug.port }
:   Type `int`, default `9029`.

`onlinefs.service.monitoring.annotations."consul.hashicorp.com/service-name"` <a class="headerlink" href="#helm.onlinefs.service.monitoring.annotations.consul.hashicorp.com-service-name" title="Permanent link">#</a> { #helm.onlinefs.service.monitoring.annotations.consul.hashicorp.com-service-name }
:   Type `string`, default `"onlinefs"`.

`onlinefs.service.monitoring.annotations."consul.hashicorp.com/service-tags"` <a class="headerlink" href="#helm.onlinefs.service.monitoring.annotations.consul.hashicorp.com-service-tags" title="Permanent link">#</a> { #helm.onlinefs.service.monitoring.annotations.consul.hashicorp.com-service-tags }
:   Type `string`, default `"monitor"`.

`onlinefs.service.monitoring.annotations."prometheus.io/path"` <a class="headerlink" href="#helm.onlinefs.service.monitoring.annotations.prometheus.io-path" title="Permanent link">#</a> { #helm.onlinefs.service.monitoring.annotations.prometheus.io-path }
:   Type `string`, default `"/metrics"`.

`onlinefs.service.monitoring.annotations."prometheus.io/port"` <a class="headerlink" href="#helm.onlinefs.service.monitoring.annotations.prometheus.io-port" title="Permanent link">#</a> { #helm.onlinefs.service.monitoring.annotations.prometheus.io-port }
:   Type `int`, default `12800`.

`onlinefs.service.monitoring.annotations."prometheus.io/scheme"` <a class="headerlink" href="#helm.onlinefs.service.monitoring.annotations.prometheus.io-scheme" title="Permanent link">#</a> { #helm.onlinefs.service.monitoring.annotations.prometheus.io-scheme }
:   Type `string`, default `"http"`.

`onlinefs.service.monitoring.annotations."prometheus.io/scrape"` <a class="headerlink" href="#helm.onlinefs.service.monitoring.annotations.prometheus.io-scrape" title="Permanent link">#</a> { #helm.onlinefs.service.monitoring.annotations.prometheus.io-scrape }
:   Type `string`, default `"true"`.

`onlinefs.service.monitoring.name` <a class="headerlink" href="#helm.onlinefs.service.monitoring.name" title="Permanent link">#</a> { #helm.onlinefs.service.monitoring.name }
:   Type `string`, default `"onlinefs-monitor"`.

`onlinefs.service.monitoring.port` <a class="headerlink" href="#helm.onlinefs.service.monitoring.port" title="Permanent link">#</a> { #helm.onlinefs.service.monitoring.port }
:   Type `int`, default `12800`.

</div>

<!-- END GENERATED VALUES -->
