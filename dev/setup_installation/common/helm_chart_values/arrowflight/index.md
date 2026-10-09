# Arrow Flight values { #helm-values-arrowflight }

Values under `arrowflight` configure the Arrow Flight server, which serves fast reads of feature groups and training datasets.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.2.0-alpha-1791544196` (Hopsworks `5.2.0`)._

Deployed when [`global._hopsworks.full_platform`](global.md#helm.global._hopsworks.full_platform) is `true`.

## General { #helm-values-arrowflight-general }

??? example "Defaults as YAML"

    ```yaml
    arrowflight:
      appName: arrowflight
      common:
        monitoring_port: 12810
        port: 5005
      configmap:
        name: arrowflight-configmap
      hopsworkslib: {}
      hpa:
        enabled: true
        flyingduck_queue_time_avg: 27
        flyingduck_request_queue_gauge: 2
        maxReplicas: 3
      image:
        pullPolicy: IfNotPresent
        registry: docker.hops.works
      nodeSelector: {}
      podDisruptionBudget:
        enabled: true
        minAvailable: 1
      spillVolume:
        size: 20Gi
        storageClassName: null
      tolerations: []
      topologySpreadConstraint: {}
    ```

<div class="hops-values" markdown>

`arrowflight` <a class="headerlink" href="#helm.arrowflight" title="Permanent link">#</a> { #helm.arrowflight }
:   Type `object`, default `{}`.
    override arrow flight values

`arrowflight.appName` <a class="headerlink" href="#helm.arrowflight.appName" title="Permanent link">#</a> { #helm.arrowflight.appName }
:   Type `string`, default `"arrowflight"`.

`arrowflight.common.monitoring_port` <a class="headerlink" href="#helm.arrowflight.common.monitoring_port" title="Permanent link">#</a> { #helm.arrowflight.common.monitoring_port }
:   Type `int`, default `12810`.

`arrowflight.common.port` <a class="headerlink" href="#helm.arrowflight.common.port" title="Permanent link">#</a> { #helm.arrowflight.common.port }
:   Type `int`, default `5005`.

`arrowflight.configmap.name` <a class="headerlink" href="#helm.arrowflight.configmap.name" title="Permanent link">#</a> { #helm.arrowflight.configmap.name }
:   Type `string`, default `"arrowflight-configmap"`.

`arrowflight.hopsworkslib` <a class="headerlink" href="#helm.arrowflight.hopsworkslib" title="Permanent link">#</a> { #helm.arrowflight.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`arrowflight.hpa.enabled` <a class="headerlink" href="#helm.arrowflight.hpa.enabled" title="Permanent link">#</a> { #helm.arrowflight.hpa.enabled }
:   Type `bool`, default `true`.
    Autoscale the Deployment with an HPA (suppressed when a VPA targets it). While active, deployment.replicas is not rendered and the HPA owns spec.replicas.

`arrowflight.hpa.flyingduck_queue_time_avg` <a class="headerlink" href="#helm.arrowflight.hpa.flyingduck_queue_time_avg" title="Permanent link">#</a> { #helm.arrowflight.hpa.flyingduck_queue_time_avg }
:   Type `int`, default `27`.

`arrowflight.hpa.flyingduck_request_queue_gauge` <a class="headerlink" href="#helm.arrowflight.hpa.flyingduck_request_queue_gauge" title="Permanent link">#</a> { #helm.arrowflight.hpa.flyingduck_request_queue_gauge }
:   Type `int`, default `2`.

`arrowflight.hpa.maxReplicas` <a class="headerlink" href="#helm.arrowflight.hpa.maxReplicas" title="Permanent link">#</a> { #helm.arrowflight.hpa.maxReplicas }
:   Type `int`, default `3`.

`arrowflight.image` <a class="headerlink" href="#helm.arrowflight.image" title="Permanent link">#</a> { #helm.arrowflight.image }
:   Type `object`, default `{"pullPolicy":"IfNotPresent","registry":"docker.hops.works"}`.
    image configuration. The image tag is the .Chart.AppVersion 

`arrowflight.nodeSelector` <a class="headerlink" href="#helm.arrowflight.nodeSelector" title="Permanent link">#</a> { #helm.arrowflight.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

`arrowflight.podDisruptionBudget.enabled` <a class="headerlink" href="#helm.arrowflight.podDisruptionBudget.enabled" title="Permanent link">#</a> { #helm.arrowflight.podDisruptionBudget.enabled }
:   Type `bool`, default `true`.

`arrowflight.podDisruptionBudget.minAvailable` <a class="headerlink" href="#helm.arrowflight.podDisruptionBudget.minAvailable" title="Permanent link">#</a> { #helm.arrowflight.podDisruptionBudget.minAvailable }
:   Type `int`, default `1`.

`arrowflight.spillVolume` <a class="headerlink" href="#helm.arrowflight.spillVolume" title="Permanent link">#</a> { #helm.arrowflight.spillVolume }
:   Type `object`, default `{"size":"20Gi","storageClassName":null}`.
    storage configuration for the ephemeral volume used by DuckDB for spilling on disk during query execution for spilling on disk during query execution for spilling on disk during query execution

`arrowflight.spillVolume.size` <a class="headerlink" href="#helm.arrowflight.spillVolume.size" title="Permanent link">#</a> { #helm.arrowflight.spillVolume.size }
:   Type `string`, default `"20Gi"`.
    size of the ephemeral volume

`arrowflight.spillVolume.storageClassName` <a class="headerlink" href="#helm.arrowflight.spillVolume.storageClassName" title="Permanent link">#</a> { #helm.arrowflight.spillVolume.storageClassName }
:   Type `string`, default `nil`.
    storage class name. If null, the default storage class will be used

`arrowflight.tolerations` <a class="headerlink" href="#helm.arrowflight.tolerations" title="Permanent link">#</a> { #helm.arrowflight.tolerations }
:   Type `list`, default `[]`.

`arrowflight.topologySpreadConstraint` <a class="headerlink" href="#helm.arrowflight.topologySpreadConstraint" title="Permanent link">#</a> { #helm.arrowflight.topologySpreadConstraint }
:   Type `object`, default `{}`.
    The default topology spread constraint. If not defined the global topology spread constraint would be used instead.

</div>

## deployment { #helm-values-arrowflight-deployment }

??? example "Defaults as YAML"

    ```yaml
    arrowflight:
      deployment:
        annotations:
          prometheus.io/path: /metrics
          prometheus.io/port: '12810'
          prometheus.io/scheme: http
          prometheus.io/scrape: 'true'
        name: arrowflight-deployment
        replicas: 1
        resources:
          limits:
            memory: 8192Mi
          requests:
            cpu: '2'
            memory: 6553Mi
        security:
          runAsGroup: 1520
          runAsUser: 1525
        server:
          hopsfs_query_mode: view
          memory_limit: '6'
          queue_timeout: '600'
    ```

<div class="hops-values" markdown>

`arrowflight.deployment.annotations."prometheus.io/path"` <a class="headerlink" href="#helm.arrowflight.deployment.annotations.prometheus.io-path" title="Permanent link">#</a> { #helm.arrowflight.deployment.annotations.prometheus.io-path }
:   Type `string`, default `"/metrics"`.

`arrowflight.deployment.annotations."prometheus.io/port"` <a class="headerlink" href="#helm.arrowflight.deployment.annotations.prometheus.io-port" title="Permanent link">#</a> { #helm.arrowflight.deployment.annotations.prometheus.io-port }
:   Type `string`, default `"12810"`.

`arrowflight.deployment.annotations."prometheus.io/scheme"` <a class="headerlink" href="#helm.arrowflight.deployment.annotations.prometheus.io-scheme" title="Permanent link">#</a> { #helm.arrowflight.deployment.annotations.prometheus.io-scheme }
:   Type `string`, default `"http"`.

`arrowflight.deployment.annotations."prometheus.io/scrape"` <a class="headerlink" href="#helm.arrowflight.deployment.annotations.prometheus.io-scrape" title="Permanent link">#</a> { #helm.arrowflight.deployment.annotations.prometheus.io-scrape }
:   Type `string`, default `"true"`.

`arrowflight.deployment.name` <a class="headerlink" href="#helm.arrowflight.deployment.name" title="Permanent link">#</a> { #helm.arrowflight.deployment.name }
:   Type `string`, default `"arrowflight-deployment"`.

`arrowflight.deployment.replicas` <a class="headerlink" href="#helm.arrowflight.deployment.replicas" title="Permanent link">#</a> { #helm.arrowflight.deployment.replicas }
:   Type `int`, default `1`.
    Number of replicas. Not rendered while the HPA is active (hpa.enabled and no VPA on this Deployment): the HPA then owns spec.replicas and this value is its minReplicas. Turning the HPA on for a running release drops the Deployment to 1 once, until the HPA scales it back up.

`arrowflight.deployment.resources.limits` <a class="headerlink" href="#helm.arrowflight.deployment.resources.limits" title="Permanent link">#</a> { #helm.arrowflight.deployment.resources.limits }
:   Type `object`, default `{"memory":"8192Mi"}`.
    resources limits configuration

`arrowflight.deployment.resources.requests` <a class="headerlink" href="#helm.arrowflight.deployment.resources.requests" title="Permanent link">#</a> { #helm.arrowflight.deployment.resources.requests }
:   Type `object`, default `{"cpu":"2","memory":"6553Mi"}`.
    resources requests configuration

`arrowflight.deployment.security.runAsGroup` <a class="headerlink" href="#helm.arrowflight.deployment.security.runAsGroup" title="Permanent link">#</a> { #helm.arrowflight.deployment.security.runAsGroup }
:   Type `int`, default `1520`.

`arrowflight.deployment.security.runAsUser` <a class="headerlink" href="#helm.arrowflight.deployment.security.runAsUser" title="Permanent link">#</a> { #helm.arrowflight.deployment.security.runAsUser }
:   Type `int`, default `1525`.

`arrowflight.deployment.server.hopsfs_query_mode` <a class="headerlink" href="#helm.arrowflight.deployment.server.hopsfs_query_mode" title="Permanent link">#</a> { #helm.arrowflight.deployment.server.hopsfs_query_mode }
:   Type `string`, default `"view"`.

`arrowflight.deployment.server.memory_limit` <a class="headerlink" href="#helm.arrowflight.deployment.server.memory_limit" title="Permanent link">#</a> { #helm.arrowflight.deployment.server.memory_limit }
:   Type `string`, default `"6"`.

`arrowflight.deployment.server.queue_timeout` <a class="headerlink" href="#helm.arrowflight.deployment.server.queue_timeout" title="Permanent link">#</a> { #helm.arrowflight.deployment.server.queue_timeout }
:   Type `string`, default `"600"`.

</div>

## externalLoadBalancer { #helm-values-arrowflight-externalloadbalancer }

??? example "Defaults as YAML"

    ```yaml
    arrowflight:
      externalLoadBalancer:
        annotations: {}
        class: null
        enabled: null
        managed: null
        nodePort: null
        nodeSelector: {}
    ```

<div class="hops-values" markdown>

`arrowflight.externalLoadBalancer.annotations` <a class="headerlink" href="#helm.arrowflight.externalLoadBalancer.annotations" title="Permanent link">#</a> { #helm.arrowflight.externalLoadBalancer.annotations }
:   Type `object`, default `{}`.
    annotations for load balancer

`arrowflight.externalLoadBalancer.class` <a class="headerlink" href="#helm.arrowflight.externalLoadBalancer.class" title="Permanent link">#</a> { #helm.arrowflight.externalLoadBalancer.class }
:   Type `string`, default `nil`.
    load balancer class name

`arrowflight.externalLoadBalancer.enabled` <a class="headerlink" href="#helm.arrowflight.externalLoadBalancer.enabled" title="Permanent link">#</a> { #helm.arrowflight.externalLoadBalancer.enabled }
:   Type `string`, default `nil`.
    Enable External Load Balancers for Arrowflight server. If not set the .global._hopsworks.externalLoadBalancers.enabled will be used instead

`arrowflight.externalLoadBalancer.managed` <a class="headerlink" href="#helm.arrowflight.externalLoadBalancer.managed" title="Permanent link">#</a> { #helm.arrowflight.externalLoadBalancer.managed }
:   Type `string`, default `nil`.
    Cloud provider provisions Load Balancers. If not set the .global._hopsworks.externalLoadBalancers.managed will be used instead

`arrowflight.externalLoadBalancer.nodePort` <a class="headerlink" href="#helm.arrowflight.externalLoadBalancer.nodePort" title="Permanent link">#</a> { #helm.arrowflight.externalLoadBalancer.nodePort }
:   Type `string`, default `nil`.
    Explicit nodePort for the external service when the load balancer is unmanaged (managed: false), so a load balancer outside Kubernetes can target a fixed port. Null lets Kubernetes allocate one from the cluster's node-port range; a set value must lie in that range (30000-32767 by default), which the API server enforces at install.

`arrowflight.externalLoadBalancer.nodeSelector` <a class="headerlink" href="#helm.arrowflight.externalLoadBalancer.nodeSelector" title="Permanent link">#</a> { #helm.arrowflight.externalLoadBalancer.nodeSelector }
:   Type `object`, default `{}`.
    selector for nodes the load balancer can use to route traffic

</div>

## service { #helm-values-arrowflight-service }

??? example "Defaults as YAML"

    ```yaml
    arrowflight:
      service:
        annotations:
          consul.hashicorp.com/service-name: flyingduck
          consul.hashicorp.com/service-port: server
          consul.hashicorp.com/service-tags: server
          prometheus.io/path: /metrics
          prometheus.io/port: '12810'
          prometheus.io/scheme: http
          prometheus.io/scrape: 'true'
        name: arrowflight-server
    ```

<div class="hops-values" markdown>

`arrowflight.service.annotations."consul.hashicorp.com/service-name"` <a class="headerlink" href="#helm.arrowflight.service.annotations.consul.hashicorp.com-service-name" title="Permanent link">#</a> { #helm.arrowflight.service.annotations.consul.hashicorp.com-service-name }
:   Type `string`, default `"flyingduck"`.

`arrowflight.service.annotations."consul.hashicorp.com/service-port"` <a class="headerlink" href="#helm.arrowflight.service.annotations.consul.hashicorp.com-service-port" title="Permanent link">#</a> { #helm.arrowflight.service.annotations.consul.hashicorp.com-service-port }
:   Type `string`, default `"server"`.

`arrowflight.service.annotations."consul.hashicorp.com/service-tags"` <a class="headerlink" href="#helm.arrowflight.service.annotations.consul.hashicorp.com-service-tags" title="Permanent link">#</a> { #helm.arrowflight.service.annotations.consul.hashicorp.com-service-tags }
:   Type `string`, default `"server"`.

`arrowflight.service.annotations."prometheus.io/path"` <a class="headerlink" href="#helm.arrowflight.service.annotations.prometheus.io-path" title="Permanent link">#</a> { #helm.arrowflight.service.annotations.prometheus.io-path }
:   Type `string`, default `"/metrics"`.

`arrowflight.service.annotations."prometheus.io/port"` <a class="headerlink" href="#helm.arrowflight.service.annotations.prometheus.io-port" title="Permanent link">#</a> { #helm.arrowflight.service.annotations.prometheus.io-port }
:   Type `string`, default `"12810"`.

`arrowflight.service.annotations."prometheus.io/scheme"` <a class="headerlink" href="#helm.arrowflight.service.annotations.prometheus.io-scheme" title="Permanent link">#</a> { #helm.arrowflight.service.annotations.prometheus.io-scheme }
:   Type `string`, default `"http"`.

`arrowflight.service.annotations."prometheus.io/scrape"` <a class="headerlink" href="#helm.arrowflight.service.annotations.prometheus.io-scrape" title="Permanent link">#</a> { #helm.arrowflight.service.annotations.prometheus.io-scrape }
:   Type `string`, default `"true"`.

`arrowflight.service.name` <a class="headerlink" href="#helm.arrowflight.service.name" title="Permanent link">#</a> { #helm.arrowflight.service.name }
:   Type `string`, default `"arrowflight-server"`.

</div>

<!-- END GENERATED VALUES -->
