# Prometheus values { #helm-values-prometheus }

Values under `prometheus` configure Prometheus, which collects cluster and service metrics, and the Prometheus adapter, which exposes them to autoscalers.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.2.0-alpha-1791370120` (Hopsworks `5.2.0`)._

Deployed when [`global._hopsworks.full_platform`](global.md#helm.global._hopsworks.full_platform) is `true`.

!!! info "Upstream charts"

    - Values under `prometheus.prometheus` go to [`prometheus` 25.20.2](https://artifacthub.io/packages/helm/prometheus-community/prometheus/25.20.2) from `https://prometheus-community.github.io/helm-charts`.
    - Values under `prometheus.prometheus-adapter` go to [`prometheus-adapter` 4.11.0](https://artifacthub.io/packages/helm/prometheus-community/prometheus-adapter/4.11.0) from `https://prometheus-community.github.io/helm-charts`.

    Only the values Hopsworks sets under `prometheus.prometheus` and `prometheus.prometheus-adapter` are listed on this page.
    Any other value of the charts can be set under the same keys; each link opens the chart's documentation for the version Hopsworks pins.

??? example "Defaults as YAML"

    ```yaml
    prometheus:
      adapter:
        enabled: true
      configAnnotations: {}
      externalLoadBalancer:
        enabled: false
        managed: null
        nodeSelector: {}
      hopsworkslib: {}
      prometheus:
        server:
          persistentVolume:
            enabled: true
            storageClass: null
      prometheus-adapter:
        dnsConfig:
          searches:
          - service.consul
        image:
          pullPolicy: IfNotPresent
          repository: docker.hops.works/prometheus/prometheus-adapter
          tag: 0.12.0-alpine-h1.1
        nameOverride: hopsworks-prometheus-adapter
        nodeSelector: {}
        prometheus:
          path: ''
          port: 9090
          url: http://prometheus.service.consul
        resources:
          limits:
            cpu: 100m
            memory: 70Mi
          requests:
            cpu: 50m
            memory: 40Mi
        rules:
          existing: custom-prometheus-metrics-adapter
        tolerations: []
        topologySpreadConstraints:
        - labelSelector:
            matchLabels:
              app.kubernetes.io/instance: hopsworks
              app.kubernetes.io/name: hopsworks-prometheus-adapter
          maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: ScheduleAnyway
    ```

<div class="hops-values" markdown>

`prometheus` <a class="headerlink" href="#helm.prometheus" title="Permanent link">#</a> { #helm.prometheus }
:   Type `object`.
    override prometheus values

    ??? note "Default"

        ```yaml
        prometheus:
          server:
            persistentVolume:
              enabled: true
              storageClass: null
        ```

`prometheus.adapter.enabled` <a class="headerlink" href="#helm.prometheus.adapter.enabled" title="Permanent link">#</a> { #helm.prometheus.adapter.enabled }
:   Type `bool`, default `true`.

`prometheus.configAnnotations` <a class="headerlink" href="#helm.prometheus.configAnnotations" title="Permanent link">#</a> { #helm.prometheus.configAnnotations }
:   Type `object`, default `{}`.
    alertmanager-tmpl config map annotations 

`prometheus.externalLoadBalancer.enabled` <a class="headerlink" href="#helm.prometheus.externalLoadBalancer.enabled" title="Permanent link">#</a> { #helm.prometheus.externalLoadBalancer.enabled }
:   Type `bool`, default `false`.
    Enable External Load Balancers for Prometheus server. If not set the .global._hopsworks.externalLoadBalancers.enabled will be used instead. If enabled AND you want the LoadBalancer to be **managed** you shall set prometheus.server.service.type: LoadBalancer - NOTE: Consul domain name will be a CNAME to LoadBalancer domain name If enabled AND you want the LoadBalancer to be **unmanged** you shall set prometheus.server.service.type: NodePort - NOTE: This only works in AWS

`prometheus.externalLoadBalancer.managed` <a class="headerlink" href="#helm.prometheus.externalLoadBalancer.managed" title="Permanent link">#</a> { #helm.prometheus.externalLoadBalancer.managed }
:   Type `string`, default `nil`.
    Cloud provider provisions Load Balancers. If not set the .global._hopsworks.externalLoadBalancers.managed will be used instead

`prometheus.externalLoadBalancer.nodeSelector` <a class="headerlink" href="#helm.prometheus.externalLoadBalancer.nodeSelector" title="Permanent link">#</a> { #helm.prometheus.externalLoadBalancer.nodeSelector }
:   Type `object`, default `{}`.
    selector for nodes the load balancer can use to route traffic

`prometheus.hopsworkslib` <a class="headerlink" href="#helm.prometheus.hopsworkslib" title="Permanent link">#</a> { #helm.prometheus.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`prometheus.prometheus` <a class="headerlink" href="#helm.prometheus.prometheus" title="Permanent link">#</a> { #helm.prometheus.prometheus }
:   Type `object`, default check \[values.yaml\](./values.yaml) for more information, passed to the [`prometheus` 25.20.2](https://artifacthub.io/packages/helm/prometheus-community/prometheus/25.20.2) chart, whose other values are documented there.
    override prometheus values

`prometheus.prometheus-adapter` <a class="headerlink" href="#helm.prometheus.prometheus-adapter" title="Permanent link">#</a> { #helm.prometheus.prometheus-adapter }
:   Type `object`, passed to the [`prometheus-adapter` 4.11.0](https://artifacthub.io/packages/helm/prometheus-community/prometheus-adapter/4.11.0) chart, whose other values are documented there.
    override prometheus-adapter values

    ??? note "Default"

        ```yaml
        dnsConfig:
          searches:
          - service.consul
        image:
          pullPolicy: IfNotPresent
          repository: docker.hops.works/prometheus/prometheus-adapter
          tag: 0.12.0-alpine-h1.1
        nameOverride: hopsworks-prometheus-adapter
        nodeSelector: {}
        prometheus:
          path: ''
          port: 9090
          url: http://prometheus.service.consul
        resources:
          limits:
            cpu: 100m
            memory: 70Mi
          requests:
            cpu: 50m
            memory: 40Mi
        rules:
          existing: custom-prometheus-metrics-adapter
        tolerations: []
        topologySpreadConstraints:
        - labelSelector:
            matchLabels:
              app.kubernetes.io/instance: hopsworks
              app.kubernetes.io/name: hopsworks-prometheus-adapter
          maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: ScheduleAnyway
        ```

</div>

<!-- END GENERATED VALUES -->
