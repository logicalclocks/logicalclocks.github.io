# Semantic gateway values { #helm-values-semantic-gateway }

Values under `semantic-gateway` configure the service that runs semantic layer queries on Trino and serves the REST, Arrow Flight SQL and GraphQL APIs.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.3.0-alpha-1795776041` (Hopsworks `5.3.0`)._

Deployed according to the first of these values that is set: [`global._hopsworks.semanticLayer.enabled`](global.md#helm.global._hopsworks.semanticLayer.enabled), [`global._hopsworks.full_platform`](global.md#helm.global._hopsworks.full_platform).

## General { #helm-values-semantic-gateway-general }

??? example "Defaults as YAML"

    ```yaml
    semantic-gateway:
      arrowMemoryLimitBytes: null
      biTables:
        enabled: true
      buildCacheEntries: 100
      cache:
        dataVersionSeconds: 30
        entryMaxBytes: 8388608
        maxBytes: 268435456
        ttlSeconds: 300
      cors:
        allowedOrigins: []
      dependencies:
        hopsworks:
          consulServiceName: glassfish
          consulServiceTag: hopsworks
          podLabels:
          - app: hopsworks-instance
          - app: hopsworks-admin
          port: 8182
        trino:
          consulServiceName: trino
          consulServiceTag: coordinator
          podLabels:
            app.kubernetes.io/component: coordinator
            app.kubernetes.io/name: hopsworks-trino
          port: 8443
      flight:
        maxHeaderBytes: 65536
        maxMessageBytes: 4194304
        queuedCalls: 256
        threads: 64
      flightPort: 18446
      graphql:
        maxFields: 500
      handleTtlSeconds: 3600
      hopsworkslib: {}
      hpa:
        enabled: false
        maxReplicas: 4
        targetCPUUtilizationPercentage: 80
      httpRequestTimeoutSeconds: 120
      httpResponseTimeoutSeconds: null
      image:
        pullPolicy: null
        registry: null
        repository: hopsworks/semantic-gateway
        tag: null
      jvmOptions: -XX:MaxRAMPercentage=50
      maxJsonBytes: 67108864
      maxJsonRows: 100000
      maxRows: 1000000
      networkPolicy:
        enabled: true
      nodeSelector: {}
      podDisruptionBudget:
        enabled: true
        minAvailable: 1
      queryConcurrency: 16
      queryTimeoutSeconds: 300
      replicas: 2
      resources:
        limits:
          cpu: '2'
          memory: 4Gi
        requests:
          cpu: 500m
          memory: 4Gi
      security:
        runAsGroup: 1000
        runAsUser: 1000
      sessionCacheSeconds: 60
      shutdownGraceSeconds: 45
      signingKey:
        existingSecret: null
      tolerations: []
      topologySpreadConstraint: {}
    ```

<div class="hops-values" markdown>

`semantic-gateway` <a class="headerlink" href="#helm.semantic-gateway" title="Permanent link">#</a> { #helm.semantic-gateway }
:   Type `object`, default `{}`.
    override semantic-gateway values

`semantic-gateway.arrowMemoryLimitBytes` <a class="headerlink" href="#helm.semantic-gateway.arrowMemoryLimitBytes" title="Permanent link">#</a> { #helm.semantic-gateway.arrowMemoryLimitBytes }
:   Type `string`, default `nil`.
    bytes of Arrow buffers the queries of a replica hold at once (ARROW_MEMORY_LIMIT_BYTES); a query that needs more fails. Null leaves the gateway's default, half the JVM heap (1 GiB with the default memory limit). The buffers sit outside the heap, so heap + this + the JVM's own memory must fit the memory limit (resources.limits)

`semantic-gateway.biTables.enabled` <a class="headerlink" href="#helm.semantic-gateway.biTables.enabled" title="Permanent link">#</a> { #helm.semantic-gateway.biTables.enabled }
:   Type `bool`, default `true`.
    show each semantic project over Flight SQL as tables (a metrics table and one per saved query) and translate BI tools' SQL over them into metric queries (BI_TABLES_ENABLED). Experimental

`semantic-gateway.buildCacheEntries` <a class="headerlink" href="#helm.semantic-gateway.buildCacheEntries" title="Permanent link">#</a> { #helm.semantic-gateway.buildCacheEntries }
:   Type `int`, default `100`.
    compiled builds each replica keeps in memory (BUILD_CACHE_ENTRIES)

`semantic-gateway.cache.dataVersionSeconds` <a class="headerlink" href="#helm.semantic-gateway.cache.dataVersionSeconds" title="Permanent link">#</a> { #helm.semantic-gateway.cache.dataVersionSeconds }
:   Type `int`, default `30`.
    seconds a replica reuses the backend's answer on the feature group data versions and access a build reads (DATA_VERSION_CACHE_SECONDS). Bounds how long a cached result outlives a new commit or a revoked share

`semantic-gateway.cache.entryMaxBytes` <a class="headerlink" href="#helm.semantic-gateway.cache.entryMaxBytes" title="Permanent link">#</a> { #helm.semantic-gateway.cache.entryMaxBytes }
:   Type `int`, default `8388608`.
    largest result, in bytes, the cache keeps (CACHE_ENTRY_MAX_BYTES). A larger result still streams to the client, uncached

`semantic-gateway.cache.maxBytes` <a class="headerlink" href="#helm.semantic-gateway.cache.maxBytes" title="Permanent link">#</a> { #helm.semantic-gateway.cache.maxBytes }
:   Type `int`, default `268435456`.
    bytes of query results each replica keeps in its result cache (CACHE_MAX_BYTES), on the heap (resources.limits)

`semantic-gateway.cache.ttlSeconds` <a class="headerlink" href="#helm.semantic-gateway.cache.ttlSeconds" title="Permanent link">#</a> { #helm.semantic-gateway.cache.ttlSeconds }
:   Type `int`, default `300`.
    seconds a cached result is served before the query runs on Trino again (CACHE_TTL_SECONDS)

`semantic-gateway.cors.allowedOrigins` <a class="headerlink" href="#helm.semantic-gateway.cors.allowedOrigins" title="Permanent link">#</a> { #helm.semantic-gateway.cors.allowedOrigins }
:   Type `list`, default `[]`.
    Browser origins whose pages may call the GraphQL API (CORS_ALLOWED_ORIGINS), such as a spreadsheet add-in's, for example <https://addin.example.com>; "*" allows any. Requests authenticate with the Authorization header, never cookies. None by default

`semantic-gateway.dependencies.hopsworks` <a class="headerlink" href="#helm.semantic-gateway.dependencies.hopsworks" title="Permanent link">#</a> { #helm.semantic-gateway.dependencies.hopsworks }
:   Type `object`.
    Payara, reached for sessions and build artifacts (HOPSWORKS_URL). The NetworkPolicy admits its pods to the internal port and lets the gateway reach them

    ??? note "Default"

        ```yaml
        consulServiceName: glassfish
        consulServiceTag: hopsworks
        podLabels:
        - app: hopsworks-instance
        - app: hopsworks-admin
        port: 8182
        ```

`semantic-gateway.dependencies.hopsworks.podLabels` <a class="headerlink" href="#helm.semantic-gateway.dependencies.hopsworks.podLabels" title="Permanent link">#</a> { #helm.semantic-gateway.dependencies.hopsworks.podLabels }
:   Type `list`, default `[{"app":"hopsworks-instance"},{"app":"hopsworks-admin"}]`.
    label sets of the Payara pods, one podSelector each

`semantic-gateway.dependencies.trino` <a class="headerlink" href="#helm.semantic-gateway.dependencies.trino" title="Permanent link">#</a> { #helm.semantic-gateway.dependencies.trino }
:   Type `object`.
    the Trino coordinator, reached over JDBC with TLS (TRINO_URL). The NetworkPolicy lets the gateway reach its pods

    ??? note "Default"

        ```yaml
        consulServiceName: trino
        consulServiceTag: coordinator
        podLabels:
          app.kubernetes.io/component: coordinator
          app.kubernetes.io/name: hopsworks-trino
        port: 8443
        ```

`semantic-gateway.dependencies.trino.podLabels` <a class="headerlink" href="#helm.semantic-gateway.dependencies.trino.podLabels" title="Permanent link">#</a> { #helm.semantic-gateway.dependencies.trino.podLabels }
:   Type `object`.
    labels of the Trino coordinator pods

    ??? note "Default"

        ```yaml
        app.kubernetes.io/component: coordinator
        app.kubernetes.io/name: hopsworks-trino
        ```

`semantic-gateway.flight.maxHeaderBytes` <a class="headerlink" href="#helm.semantic-gateway.flight.maxHeaderBytes" title="Permanent link">#</a> { #helm.semantic-gateway.flight.maxHeaderBytes }
:   Type `int`, default `65536`.
    largest header list, in bytes, a Flight SQL call may send (FLIGHT_MAX_HEADER_BYTES)

`semantic-gateway.flight.maxMessageBytes` <a class="headerlink" href="#helm.semantic-gateway.flight.maxMessageBytes" title="Permanent link">#</a> { #helm.semantic-gateway.flight.maxMessageBytes }
:   Type `int`, default `4194304`.
    largest request message, in bytes, a Flight SQL call may send (FLIGHT_MAX_MESSAGE_BYTES)

`semantic-gateway.flight.queuedCalls` <a class="headerlink" href="#helm.semantic-gateway.flight.queuedCalls" title="Permanent link">#</a> { #helm.semantic-gateway.flight.queuedCalls }
:   Type `int`, default `256`.
    Flight SQL calls waiting for a free thread (FLIGHT_QUEUED_CALLS). A call past the threads and this queue is refused at once

`semantic-gateway.flight.threads` <a class="headerlink" href="#helm.semantic-gateway.flight.threads" title="Permanent link">#</a> { #helm.semantic-gateway.flight.threads }
:   Type `int`, default `64`.
    Flight SQL calls a replica runs at once (FLIGHT_THREADS)

`semantic-gateway.flightPort` <a class="headerlink" href="#helm.semantic-gateway.flightPort" title="Permanent link">#</a> { #helm.semantic-gateway.flightPort }
:   Type `int`, default `18446`.
    Port of the Arrow Flight SQL server (FLIGHT_PORT), which dbt's JDBC dialect, ADBC and dbt-sl-sdk clients query, and of externalLoadBalancer, which serves it outside the cluster. hopsworks.variables.semantic_gateway_flight_port tells those clients the port, so change both together. Inside the cluster the ClusterIP Service serves it at 18446 whatever this is.

`semantic-gateway.graphql.maxFields` <a class="headerlink" href="#helm.semantic-gateway.graphql.maxFields" title="Permanent link">#</a> { #helm.semantic-gateway.graphql.maxFields }
:   Type `int`, default `500`.
    most fields a GraphQL operation may select, each alias counted (GRAPHQL_MAX_FIELDS). A larger operation is refused before it runs

`semantic-gateway.handleTtlSeconds` <a class="headerlink" href="#helm.semantic-gateway.handleTtlSeconds" title="Permanent link">#</a> { #helm.semantic-gateway.handleTtlSeconds }
:   Type `int`, default `3600`.
    seconds a signed handle (a Flight ticket, a prepared statement) stays valid after the gateway issues it (HANDLE_TTL_SECONDS)

`semantic-gateway.hopsworkslib` <a class="headerlink" href="#helm.semantic-gateway.hopsworkslib" title="Permanent link">#</a> { #helm.semantic-gateway.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`semantic-gateway.hpa.enabled` <a class="headerlink" href="#helm.semantic-gateway.hpa.enabled" title="Permanent link">#</a> { #helm.semantic-gateway.hpa.enabled }
:   Type `bool`, default `false`.
    Autoscale the Deployment on CPU with an HPA. While enabled, replicas is not rendered and the HPA owns spec.replicas.

`semantic-gateway.hpa.maxReplicas` <a class="headerlink" href="#helm.semantic-gateway.hpa.maxReplicas" title="Permanent link">#</a> { #helm.semantic-gateway.hpa.maxReplicas }
:   Type `int`, default `4`.
    most replicas the HPA scales to

`semantic-gateway.hpa.targetCPUUtilizationPercentage` <a class="headerlink" href="#helm.semantic-gateway.hpa.targetCPUUtilizationPercentage" title="Permanent link">#</a> { #helm.semantic-gateway.hpa.targetCPUUtilizationPercentage }
:   Type `int`, default `80`.
    average CPU utilization, in percent of the request, the HPA keeps the replicas at

`semantic-gateway.httpRequestTimeoutSeconds` <a class="headerlink" href="#helm.semantic-gateway.httpRequestTimeoutSeconds" title="Permanent link">#</a> { #helm.semantic-gateway.httpRequestTimeoutSeconds }
:   Type `int`, default `120`.
    Seconds a client has to send an HTTP request, from its first byte through the TLS handshake to the end of the body (HTTP_REQUEST_TIMEOUT_SECONDS)

`semantic-gateway.httpResponseTimeoutSeconds` <a class="headerlink" href="#helm.semantic-gateway.httpResponseTimeoutSeconds" title="Permanent link">#</a> { #helm.semantic-gateway.httpResponseTimeoutSeconds }
:   Type `string`, default `nil`.
    Seconds an HTTP answer may take, from the request read to its last byte written, the query and a slow reader included (HTTP_RESPONSE_TIMEOUT_SECONDS). Null leaves the gateway's default, 2 x (queryTimeoutSeconds + 30) + 240, which is 900 with the default queryTimeoutSeconds and follows it. The gateway refuses to start with less than queryTimeoutSeconds + 30

`semantic-gateway.image.pullPolicy` <a class="headerlink" href="#helm.semantic-gateway.image.pullPolicy" title="Permanent link">#</a> { #helm.semantic-gateway.image.pullPolicy }
:   Type `string`, default `nil`.
    image pull policy. If not set, global._hopsworks.imagePullPolicy, then IfNotPresent

`semantic-gateway.image.registry` <a class="headerlink" href="#helm.semantic-gateway.image.registry" title="Permanent link">#</a> { #helm.semantic-gateway.image.registry }
:   Type `string`, default `nil`.
    image registry. If not set, global._hopsworks.imageRegistry is used

`semantic-gateway.image.repository` <a class="headerlink" href="#helm.semantic-gateway.image.repository" title="Permanent link">#</a> { #helm.semantic-gateway.image.repository }
:   Type `string`, default `"hopsworks/semantic-gateway"`.
    image repository. The image is built from hopsworks-ee

`semantic-gateway.image.tag` <a class="headerlink" href="#helm.semantic-gateway.image.tag" title="Permanent link">#</a> { #helm.semantic-gateway.image.tag }
:   Type `string`, default `nil`.
    image tag. If not set, the chart's appVersion, the Hopsworks version the gateway is built with

`semantic-gateway.jvmOptions` <a class="headerlink" href="#helm.semantic-gateway.jvmOptions" title="Permanent link">#</a> { #helm.semantic-gateway.jvmOptions }
:   Type `string`, default `"-XX:MaxRAMPercentage=50"`.
    JVM options of the gateway, passed as JAVA_TOOL_OPTIONS. -XX:MaxRAMPercentage=50 makes the heap half the memory limit, leaving the other half for the Arrow buffers and the JVM's own memory (resources.limits). The image adds -XX:+ExitOnOutOfMemoryError, so the pod restarts on an OutOfMemoryError whatever this holds

`semantic-gateway.maxJsonBytes` <a class="headerlink" href="#helm.semantic-gateway.maxJsonBytes" title="Permanent link">#</a> { #helm.semantic-gateway.maxJsonBytes }
:   Type `int`, default `67108864`.
    most bytes, counted as JSON text, a JSON or CSV query result holds (MAX_JSON_BYTES). A larger result is refused with 413. Each query slot may hold one on the heap, so queryConcurrency x maxJsonBytes must fit the heap with the cache (resources.limits)

`semantic-gateway.maxJsonRows` <a class="headerlink" href="#helm.semantic-gateway.maxJsonRows" title="Permanent link">#</a> { #helm.semantic-gateway.maxJsonRows }
:   Type `int`, default `100000`.
    most rows a JSON query result holds (MAX_JSON_ROWS), which the gateway keeps in memory whole. A larger result is cut off and flagged as truncated

`semantic-gateway.maxRows` <a class="headerlink" href="#helm.semantic-gateway.maxRows" title="Permanent link">#</a> { #helm.semantic-gateway.maxRows }
:   Type `int`, default `1000000`.
    most rows an Arrow query result streams (MAX_ROWS). A larger result is cut off, and the X-Semantic-Max-Rows header lets the client tell

`semantic-gateway.networkPolicy.enabled` <a class="headerlink" href="#helm.semantic-gateway.networkPolicy.enabled" title="Permanent link">#</a> { #helm.semantic-gateway.networkPolicy.enabled }
:   Type `bool`, default `true`.
    restrict the gateway's traffic: the internal port to the Payara pods, the metrics port to the release namespace, egress to DNS, Payara and Trino

`semantic-gateway.nodeSelector` <a class="headerlink" href="#helm.semantic-gateway.nodeSelector" title="Permanent link">#</a> { #helm.semantic-gateway.nodeSelector }
:   Type `object`, default `{}`.
    node selector. If empty, global._hopsworks.nodeSelector is used

`semantic-gateway.podDisruptionBudget.enabled` <a class="headerlink" href="#helm.semantic-gateway.podDisruptionBudget.enabled" title="Permanent link">#</a> { #helm.semantic-gateway.podDisruptionBudget.enabled }
:   Type `bool`, default `true`.
    keep minAvailable replicas through voluntary disruptions. Rendered only with more than one replica

`semantic-gateway.podDisruptionBudget.minAvailable` <a class="headerlink" href="#helm.semantic-gateway.podDisruptionBudget.minAvailable" title="Permanent link">#</a> { #helm.semantic-gateway.podDisruptionBudget.minAvailable }
:   Type `int`, default `1`.
    replicas kept available. Must be less than replicas

`semantic-gateway.queryConcurrency` <a class="headerlink" href="#helm.semantic-gateway.queryConcurrency" title="Permanent link">#</a> { #helm.semantic-gateway.queryConcurrency }
:   Type `int`, default `16`.
    queries each replica runs at once (QUERY_CONCURRENCY). A query that finds no free slot within 30 s is refused with 503. Each slot may hold a JSON answer of maxJsonBytes on the heap (resources.limits)

`semantic-gateway.queryTimeoutSeconds` <a class="headerlink" href="#helm.semantic-gateway.queryTimeoutSeconds" title="Permanent link">#</a> { #helm.semantic-gateway.queryTimeoutSeconds }
:   Type `int`, default `300`.
    seconds a query may run on Trino before the gateway cancels it (QUERY_TIMEOUT_SECONDS), counted after the up to 30 s it may wait for a slot. The read and send timeouts of the Ingresses in front of the gateway (hopsworks.semanticLayer) must exceed this plus 30, or nginx answers 504 for a query that then succeeds: raise them with it

`semantic-gateway.replicas` <a class="headerlink" href="#helm.semantic-gateway.replicas" title="Permanent link">#</a> { #helm.semantic-gateway.replicas }
:   Type `int`, default `2`.
    Number of replicas. Not rendered while the HPA is enabled: the HPA then owns spec.replicas and this value is its minReplicas.

`semantic-gateway.resources.limits` <a class="headerlink" href="#helm.semantic-gateway.resources.limits" title="Permanent link">#</a> { #helm.semantic-gateway.resources.limits }
:   Type `object`, default `{"cpu":"2","memory":"4Gi"}`.
    resource limits of the gateway container. With the defaults, the 4Gi memory limit is a 2 GiB heap (jvmOptions), 1 GiB of Arrow buffers outside the heap (arrowMemoryLimitBytes) and 1 GiB for the JVM's own memory (metaspace, thread stacks, gRPC buffers). The heap holds the result cache (cache.maxBytes, 256 MiB), the query history queue (64 MiB) and a JSON answer in each query slot (queryConcurrency x maxJsonBytes, 16 x 64 MiB): 1344 MiB, leaving the rest of the heap for compiled builds and the queries' working memory. The gateway refuses to start when cache.maxBytes + 64 MiB + queryConcurrency x maxJsonBytes exceeds the heap, so raising queryConcurrency, maxJsonBytes or cache.maxBytes past that needs a larger memory limit, in requests and limits together

`semantic-gateway.resources.requests` <a class="headerlink" href="#helm.semantic-gateway.resources.requests" title="Permanent link">#</a> { #helm.semantic-gateway.resources.requests }
:   Type `object`, default `{"cpu":"500m","memory":"4Gi"}`.
    resource requests of the gateway container. Keep the memory request equal to the limit: the JVM sizes itself from the limit

`semantic-gateway.security.runAsGroup` <a class="headerlink" href="#helm.semantic-gateway.security.runAsGroup" title="Permanent link">#</a> { #helm.semantic-gateway.security.runAsGroup }
:   Type `int`, default `1000`.
    group the gateway runs as

`semantic-gateway.security.runAsUser` <a class="headerlink" href="#helm.semantic-gateway.security.runAsUser" title="Permanent link">#</a> { #helm.semantic-gateway.security.runAsUser }
:   Type `int`, default `1000`.
    user the gateway runs as

`semantic-gateway.sessionCacheSeconds` <a class="headerlink" href="#helm.semantic-gateway.sessionCacheSeconds" title="Permanent link">#</a> { #helm.semantic-gateway.sessionCacheSeconds }
:   Type `int`, default `60`.
    seconds the gateway keeps a caller's session, fetched from the backend, before it asks again (SESSION_CACHE_SECONDS)

`semantic-gateway.shutdownGraceSeconds` <a class="headerlink" href="#helm.semantic-gateway.shutdownGraceSeconds" title="Permanent link">#</a> { #helm.semantic-gateway.shutdownGraceSeconds }
:   Type `int`, default `45`.
    Seconds requests in flight get to finish when a pod stops (SHUTDOWN_GRACE_SECONDS); the gateway accepts no new ones meanwhile, and flushes its query history for up to 10 s more. The pod's terminationGracePeriodSeconds is this plus 30, which also covers the 5 s the pod keeps serving while it is removed from the Service endpoints

`semantic-gateway.signingKey.existingSecret` <a class="headerlink" href="#helm.semantic-gateway.signingKey.existingSecret" title="Permanent link">#</a> { #helm.semantic-gateway.signingKey.existingSecret }
:   Type `string`, default `nil`.
    Secret holding the key the gateway signs handles (Flight tickets, prepared statements) with, under `current`, and optionally a key it also accepts, under `previous`. Null: the chart creates the Secret semantic-gateway-signing with a random `current` and keeps both keys across upgrades by reading it back, which needs global._hopsworks.mode auto; any other mode (ArgoCD) fails the render until this names a Secret you create. Rotate in two rollouts: first add the new key as `previous`, then make it `current` and the old key `previous`. After each edit of the Secret, roll the pods: a helm upgrade does it for the Secret the chart created, whose keys the pods carry a checksum of; for an existingSecret, restart the Deployment. Handles signed with the old key stay valid until they expire (handleTtlSeconds).

`semantic-gateway.tolerations` <a class="headerlink" href="#helm.semantic-gateway.tolerations" title="Permanent link">#</a> { #helm.semantic-gateway.tolerations }
:   Type `list`, default `[]`.
    tolerations. If empty, global._hopsworks.tolerations is used

`semantic-gateway.topologySpreadConstraint` <a class="headerlink" href="#helm.semantic-gateway.topologySpreadConstraint" title="Permanent link">#</a> { #helm.semantic-gateway.topologySpreadConstraint }
:   Type `object`, default `{}`.
    The default topology spread constraint. If not defined the global topology spread constraint would be used instead.

</div>

## externalLoadBalancer { #helm-values-semantic-gateway-externalloadbalancer }

??? example "Defaults as YAML"

    ```yaml
    semantic-gateway:
      externalLoadBalancer:
        annotations: {}
        class: null
        enabled: null
        hostname: null
        managed: null
        nodePort: null
        nodeSelector: {}
    ```

<div class="hops-values" markdown>

`semantic-gateway.externalLoadBalancer.annotations` <a class="headerlink" href="#helm.semantic-gateway.externalLoadBalancer.annotations" title="Permanent link">#</a> { #helm.semantic-gateway.externalLoadBalancer.annotations }
:   Type `object`, default `{}`.
    annotations of the external Service, merged over global._hopsworks.externalLoadBalancers.annotations

`semantic-gateway.externalLoadBalancer.class` <a class="headerlink" href="#helm.semantic-gateway.externalLoadBalancer.class" title="Permanent link">#</a> { #helm.semantic-gateway.externalLoadBalancer.class }
:   Type `string`, default `nil`.
    load balancer class name. If not set, global._hopsworks.externalLoadBalancers.class is used

`semantic-gateway.externalLoadBalancer.enabled` <a class="headerlink" href="#helm.semantic-gateway.externalLoadBalancer.enabled" title="Permanent link">#</a> { #helm.semantic-gateway.externalLoadBalancer.enabled }
:   Type `string`, default `nil`.
    Expose the Arrow Flight SQL port outside the cluster on the Service semantic-gateway-external. If not set, global._hopsworks.externalLoadBalancers.enabled is used

`semantic-gateway.externalLoadBalancer.hostname` <a class="headerlink" href="#helm.semantic-gateway.externalLoadBalancer.hostname" title="Permanent link">#</a> { #helm.semantic-gateway.externalLoadBalancer.hostname }
:   Type `string`, default `nil`.
    DNS name, or IP address, clients reach the load balancer at. Added to the gateway's certificate, which clients check the name against; set hopsworks.variables.loadbalancer_external_domain_semantic_gateway to the same name so the connection details Hopsworks hands out use it. Set it at install: the certificate's names cannot change later unless the HopsworksCert semantic-gateway is deleted before the upgrade.

`semantic-gateway.externalLoadBalancer.managed` <a class="headerlink" href="#helm.semantic-gateway.externalLoadBalancer.managed" title="Permanent link">#</a> { #helm.semantic-gateway.externalLoadBalancer.managed }
:   Type `string`, default `nil`.
    Cloud provider provisions the load balancer (a LoadBalancer Service). False makes it a NodePort Service for a load balancer outside Kubernetes, which on AWS a TargetGroupBinding attaches to global.unmanagedLoadBalancers.semanticGateway.targetGroupId. If not set, global._hopsworks.externalLoadBalancers.managed is used

`semantic-gateway.externalLoadBalancer.nodePort` <a class="headerlink" href="#helm.semantic-gateway.externalLoadBalancer.nodePort" title="Permanent link">#</a> { #helm.semantic-gateway.externalLoadBalancer.nodePort }
:   Type `string`, default `nil`.
    Explicit nodePort for the external Service when the load balancer is unmanaged (managed: false), so a load balancer outside Kubernetes can target a fixed port. Null lets Kubernetes allocate one from the cluster's node-port range; a set value must lie in that range (30000-32767 by default), which the API server enforces at install.

`semantic-gateway.externalLoadBalancer.nodeSelector` <a class="headerlink" href="#helm.semantic-gateway.externalLoadBalancer.nodeSelector" title="Permanent link">#</a> { #helm.semantic-gateway.externalLoadBalancer.nodeSelector }
:   Type `object`, default `{}`.
    selector for nodes the AWS TargetGroupBinding routes traffic to

</div>

<!-- END GENERATED VALUES -->
