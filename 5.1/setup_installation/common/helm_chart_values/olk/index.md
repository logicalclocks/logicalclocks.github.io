# OpenSearch values { #helm-values-olk }

Values under `olk` configure OpenSearch, OpenSearch Dashboards, Logstash and Filebeat, which provide search, the vector index and service logs.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.1.0` (Hopsworks `5.1.0`)._

Deployed when [`global._hopsworks.opensearch.enabled`](global.md#helm.global._hopsworks.opensearch.enabled) is `true`.

!!! info "Upstream charts"

    - Values under `olk.prometheus-elasticsearch-exporter` go to [`prometheus-elasticsearch-exporter` 5.8.0](https://artifacthub.io/packages/helm/prometheus-community/prometheus-elasticsearch-exporter/5.8.0) from `https://prometheus-community.github.io/helm-charts`.

    Only the values Hopsworks sets under `olk.prometheus-elasticsearch-exporter` are listed on this page.
    Any other value of the chart can be set there too; the link opens its documentation for the version Hopsworks pins.

## General { #helm-values-olk-general }

??? example "Defaults as YAML"

    ```yaml
    olk:
      appName: elk
      cleanupOnUninstall:
        enabled: true
        ttlSecondsAfterFinished: null
      hopsworkslib: {}
      image:
        registry: docker.hops.works
      opensearch:
        storageClassName: null
      prometheus-elasticsearch-exporter:
        es:
          sslSkipVerify: true
          uri: https://elastic_exporter:elastic_exporterpw@{{ include "olk.exporter.opensearchHost" . }}:9200
        image:
          registry: docker.hops.works
          repository: prometheus/elasticsearch-exporter
          tag: 1.11.0-alpine-h1.1
        nodeSelector: {}
        resources:
          limits:
            cpu: 800m
            memory: 200Mi
          requests:
            cpu: 300m
            memory: 128Mi
        service:
          annotations:
            prometheus.io/path: /metrics
            prometheus.io/port: '9108'
            prometheus.io/scheme: http
            prometheus.io/scrape: 'true'
          httpPort: 9108
        tolerations: []
    ```

<div class="hops-values" markdown>

`olk` <a class="headerlink" href="#helm.olk" title="Permanent link">#</a> { #helm.olk }
:   Type `object`, default `{"opensearch":{"storageClassName":null}}`.
    override olk values

`olk.appName` <a class="headerlink" href="#helm.olk.appName" title="Permanent link">#</a> { #helm.olk.appName }
:   Type `string`, default `"elk"`.

`olk.cleanupOnUninstall` <a class="headerlink" href="#helm.olk.cleanupOnUninstall" title="Permanent link">#</a> { #helm.olk.cleanupOnUninstall }
:   Type `object`, default `{"enabled":true,"ttlSecondsAfterFinished":null}`.
    post-delete cleanup of OLK leftovers. Always deletes the signingjwt Secret (created centrally, or copied in satellite; not Helm-tracked). Also deletes the OpenSearch StatefulSet PVC by label (app=opensearch) when global._hopsworks.wipeDataOnUninstall is enabled, except PVCs labelled hopsworks.ai/keep=true.

`olk.cleanupOnUninstall.enabled` <a class="headerlink" href="#helm.olk.cleanupOnUninstall.enabled" title="Permanent link">#</a> { #helm.olk.cleanupOnUninstall.enabled }
:   Type `bool`, default `true`.
    enable the post-delete OLK cleanup hook (signingjwt Secret always; OpenSearch PVC additionally requires global._hopsworks.wipeDataOnUninstall)

`olk.cleanupOnUninstall.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.olk.cleanupOnUninstall.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.olk.cleanupOnUninstall.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    ttlSecondsAfterFinished for the cleanup Job; null falls through to the global default

`olk.hopsworkslib` <a class="headerlink" href="#helm.olk.hopsworkslib" title="Permanent link">#</a> { #helm.olk.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`olk.image.registry` <a class="headerlink" href="#helm.olk.image.registry" title="Permanent link">#</a> { #helm.olk.image.registry }
:   Type `string`, default `"docker.hops.works"`.

`olk.prometheus-elasticsearch-exporter` <a class="headerlink" href="#helm.olk.prometheus-elasticsearch-exporter" title="Permanent link">#</a> { #helm.olk.prometheus-elasticsearch-exporter }
:   Type `object`, passed to the [`prometheus-elasticsearch-exporter` 5.8.0](https://artifacthub.io/packages/helm/prometheus-community/prometheus-elasticsearch-exporter/5.8.0) chart, whose other values are documented there.
    override prometheus elasticsearch exporter values

    ??? note "Default"

        ```yaml
        es:
          sslSkipVerify: true
          uri: https://elastic_exporter:elastic_exporterpw@{{ include "olk.exporter.opensearchHost" . }}:9200
        image:
          registry: docker.hops.works
          repository: prometheus/elasticsearch-exporter
          tag: 1.11.0-alpine-h1.1
        nodeSelector: {}
        resources:
          limits:
            cpu: 800m
            memory: 200Mi
          requests:
            cpu: 300m
            memory: 128Mi
        service:
          annotations:
            prometheus.io/path: /metrics
            prometheus.io/port: '9108'
            prometheus.io/scheme: http
            prometheus.io/scrape: 'true'
          httpPort: 9108
        tolerations: []
        ```

</div>

## dashboard { #helm-values-olk-dashboard }

??? example "Defaults as YAML"

    ```yaml
    olk:
      dashboard:
        config:
          basePath: /hopsworks-api/kibana
          index: .kibana
          name: dashboard-config
        deleteKibanaIndexIfPrevious: false
        export: false
        jwt:
          roles_key: roles
          subject_key: sub
          url_parameter: jt
        name: opensearch-dashboard
        nodeSelector: {}
        port: 5601
        resources:
          limits:
            cpu: 200m
            memory: 1Gi
          requests:
            cpu: 50m
            memory: 512Mi
        security:
          cookie_ttl: 1800000
          session_ttl: 3600000
        security_context:
          fsGroup: 1000
          runAsGroup: 1000
          runAsNonRoot: true
          runAsUser: 1000
        service:
          annotations:
            consul.hashicorp.com/service-name: kibana
        shard_timeout: 10000
        startup_timeout: 5000
        tolerations: []
        topologySpreadConstraint: {}
        version: 2.19.6.7
    ```

<div class="hops-values" markdown>

`olk.dashboard.config.basePath` <a class="headerlink" href="#helm.olk.dashboard.config.basePath" title="Permanent link">#</a> { #helm.olk.dashboard.config.basePath }
:   Type `string`, default `"/hopsworks-api/kibana"`.

`olk.dashboard.config.index` <a class="headerlink" href="#helm.olk.dashboard.config.index" title="Permanent link">#</a> { #helm.olk.dashboard.config.index }
:   Type `string`, default `".kibana"`.

`olk.dashboard.config.name` <a class="headerlink" href="#helm.olk.dashboard.config.name" title="Permanent link">#</a> { #helm.olk.dashboard.config.name }
:   Type `string`, default `"dashboard-config"`.

`olk.dashboard.deleteKibanaIndexIfPrevious` <a class="headerlink" href="#helm.olk.dashboard.deleteKibanaIndexIfPrevious" title="Permanent link">#</a> { #helm.olk.dashboard.deleteKibanaIndexIfPrevious }
:   Type `bool`, default `false`.

`olk.dashboard.export` <a class="headerlink" href="#helm.olk.dashboard.export" title="Permanent link">#</a> { #helm.olk.dashboard.export }
:   Type `bool`, default `false`.

`olk.dashboard.jwt.roles_key` <a class="headerlink" href="#helm.olk.dashboard.jwt.roles_key" title="Permanent link">#</a> { #helm.olk.dashboard.jwt.roles_key }
:   Type `string`, default `"roles"`.

`olk.dashboard.jwt.subject_key` <a class="headerlink" href="#helm.olk.dashboard.jwt.subject_key" title="Permanent link">#</a> { #helm.olk.dashboard.jwt.subject_key }
:   Type `string`, default `"sub"`.

`olk.dashboard.jwt.url_parameter` <a class="headerlink" href="#helm.olk.dashboard.jwt.url_parameter" title="Permanent link">#</a> { #helm.olk.dashboard.jwt.url_parameter }
:   Type `string`, default `"jt"`.

`olk.dashboard.name` <a class="headerlink" href="#helm.olk.dashboard.name" title="Permanent link">#</a> { #helm.olk.dashboard.name }
:   Type `string`, default `"opensearch-dashboard"`.

`olk.dashboard.nodeSelector` <a class="headerlink" href="#helm.olk.dashboard.nodeSelector" title="Permanent link">#</a> { #helm.olk.dashboard.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

`olk.dashboard.port` <a class="headerlink" href="#helm.olk.dashboard.port" title="Permanent link">#</a> { #helm.olk.dashboard.port }
:   Type `int`, default `5601`.

`olk.dashboard.resources.limits.cpu` <a class="headerlink" href="#helm.olk.dashboard.resources.limits.cpu" title="Permanent link">#</a> { #helm.olk.dashboard.resources.limits.cpu }
:   Type `string`, default `"200m"`.

`olk.dashboard.resources.limits.memory` <a class="headerlink" href="#helm.olk.dashboard.resources.limits.memory" title="Permanent link">#</a> { #helm.olk.dashboard.resources.limits.memory }
:   Type `string`, default `"1Gi"`.

`olk.dashboard.resources.requests.cpu` <a class="headerlink" href="#helm.olk.dashboard.resources.requests.cpu" title="Permanent link">#</a> { #helm.olk.dashboard.resources.requests.cpu }
:   Type `string`, default `"50m"`.

`olk.dashboard.resources.requests.memory` <a class="headerlink" href="#helm.olk.dashboard.resources.requests.memory" title="Permanent link">#</a> { #helm.olk.dashboard.resources.requests.memory }
:   Type `string`, default `"512Mi"`.

`olk.dashboard.security.cookie_ttl` <a class="headerlink" href="#helm.olk.dashboard.security.cookie_ttl" title="Permanent link">#</a> { #helm.olk.dashboard.security.cookie_ttl }
:   Type `int`, default `1800000`.

`olk.dashboard.security.session_ttl` <a class="headerlink" href="#helm.olk.dashboard.security.session_ttl" title="Permanent link">#</a> { #helm.olk.dashboard.security.session_ttl }
:   Type `int`, default `3600000`.

`olk.dashboard.security_context.fsGroup` <a class="headerlink" href="#helm.olk.dashboard.security_context.fsGroup" title="Permanent link">#</a> { #helm.olk.dashboard.security_context.fsGroup }
:   Type `int`, default `1000`.

`olk.dashboard.security_context.runAsGroup` <a class="headerlink" href="#helm.olk.dashboard.security_context.runAsGroup" title="Permanent link">#</a> { #helm.olk.dashboard.security_context.runAsGroup }
:   Type `int`, default `1000`.

`olk.dashboard.security_context.runAsNonRoot` <a class="headerlink" href="#helm.olk.dashboard.security_context.runAsNonRoot" title="Permanent link">#</a> { #helm.olk.dashboard.security_context.runAsNonRoot }
:   Type `bool`, default `true`.

`olk.dashboard.security_context.runAsUser` <a class="headerlink" href="#helm.olk.dashboard.security_context.runAsUser" title="Permanent link">#</a> { #helm.olk.dashboard.security_context.runAsUser }
:   Type `int`, default `1000`.

`olk.dashboard.service.annotations."consul.hashicorp.com/service-name"` <a class="headerlink" href="#helm.olk.dashboard.service.annotations.consul.hashicorp.com-service-name" title="Permanent link">#</a> { #helm.olk.dashboard.service.annotations.consul.hashicorp.com-service-name }
:   Type `string`, default `"kibana"`.

`olk.dashboard.shard_timeout` <a class="headerlink" href="#helm.olk.dashboard.shard_timeout" title="Permanent link">#</a> { #helm.olk.dashboard.shard_timeout }
:   Type `int`, default `10000`.

`olk.dashboard.startup_timeout` <a class="headerlink" href="#helm.olk.dashboard.startup_timeout" title="Permanent link">#</a> { #helm.olk.dashboard.startup_timeout }
:   Type `int`, default `5000`.

`olk.dashboard.tolerations` <a class="headerlink" href="#helm.olk.dashboard.tolerations" title="Permanent link">#</a> { #helm.olk.dashboard.tolerations }
:   Type `list`, default `[]`.

`olk.dashboard.topologySpreadConstraint` <a class="headerlink" href="#helm.olk.dashboard.topologySpreadConstraint" title="Permanent link">#</a> { #helm.olk.dashboard.topologySpreadConstraint }
:   Type `object`, default `{}`.
    The default topology spread constraint. If not defined the global topology spread constraint would be used instead.

`olk.dashboard.version` <a class="headerlink" href="#helm.olk.dashboard.version" title="Permanent link">#</a> { #helm.olk.dashboard.version }
:   Type `string`, default `"2.19.6.7"`.

</div>

## filebeat { #helm-values-olk-filebeat }

??? example "Defaults as YAML"

    ```yaml
    olk:
      filebeat:
        config:
          name: filebeat-config
        enabled: true
        extraNamespaces: []
        fullnameOverride: null
        image:
          tag: 8.19.21
        kubernetesMetadata:
          cronjob: null
          deployment: null
          extraNamespaceLabels: []
          extraNodeLabels: []
          extraPodLabels: []
          logFilteringNamespaceLabels:
          - hopsworks.ai/project
          - hopsworks.ai/onlinefs-cluster
          logFilteringNodeLabels:
          - kubernetes.io/hostname
          logFilteringPodLabels:
          - name
          - app
          - app.kubernetes.io/name
          - service
          - rondbService
          - component
          - user
          - job-type
          - job-id
          - job-name
          - execution
          - jupyter
          - jupyter-id
          - jupyter-settings-id
          - kernel-id
          - spark-role
          - spark-app-selector
          - sparkoperator.k8s.io/launched-by-spark-operator
          - serving.hops.works/id
          - serving.hops.works/name
          - serving.hops.works/tool
          - serving.hops.works/model-name
          - serving.hops.works/model-version
          - serving.hops.works/model-server
          - serving.hops.works/project-id
          namespaceAnnotations: []
          nodeAnnotations: []
          podAnnotations: []
        logs_locations:
        - addKubernetesMetadata: true
          glob: /*.log
          logtype: log
          mountPaths:
          - /var/log/containers
          - /var/log/pods
          name: containerd
          path: /var/log/containers
          processors: []
        name: filebeat
        resources:
          limits:
            memory: 400Mi
          requests:
            cpu: 100m
            memory: 200Mi
        serviceAccount:
          annotations: {}
        terminationgraceperiod: 30
        tolerations:
        - effect: NoSchedule
          operator: Exists
    ```

<div class="hops-values" markdown>

`olk.filebeat.config.name` <a class="headerlink" href="#helm.olk.filebeat.config.name" title="Permanent link">#</a> { #helm.olk.filebeat.config.name }
:   Type `string`, default `"filebeat-config"`.

`olk.filebeat.enabled` <a class="headerlink" href="#helm.olk.filebeat.enabled" title="Permanent link">#</a> { #helm.olk.filebeat.enabled }
:   Type `bool`, default `true`.

`olk.filebeat.extraNamespaces` <a class="headerlink" href="#helm.olk.filebeat.extraNamespaces" title="Permanent link">#</a> { #helm.olk.filebeat.extraNamespaces }
:   Type `list`, default `[]`.
    extra namespaces to process their container logs. By default the release name space and the Hopsworks project namespaces are whitelisted.

`olk.filebeat.fullnameOverride` <a class="headerlink" href="#helm.olk.filebeat.fullnameOverride" title="Permanent link">#</a> { #helm.olk.filebeat.fullnameOverride }
:   Type `string`, default `nil`.
    full name override

`olk.filebeat.image.tag` <a class="headerlink" href="#helm.olk.filebeat.image.tag" title="Permanent link">#</a> { #helm.olk.filebeat.image.tag }
:   Type `string`, default `"8.19.21"`.

`olk.filebeat.kubernetesMetadata.cronjob` <a class="headerlink" href="#helm.olk.filebeat.kubernetesMetadata.cronjob" title="Permanent link">#</a> { #helm.olk.filebeat.kubernetesMetadata.cronjob }
:   Type `bool|null`, default `nil`.
    attach kubernetes.cronjob.name; unset leaves filebeat's default

`olk.filebeat.kubernetesMetadata.deployment` <a class="headerlink" href="#helm.olk.filebeat.kubernetesMetadata.deployment" title="Permanent link">#</a> { #helm.olk.filebeat.kubernetesMetadata.deployment }
:   Type `bool|null`, default `nil`.
    attach kubernetes.deployment.name; unset leaves filebeat's default

`olk.filebeat.kubernetesMetadata.extraNamespaceLabels` <a class="headerlink" href="#helm.olk.filebeat.kubernetesMetadata.extraNamespaceLabels" title="Permanent link">#</a> { #helm.olk.filebeat.kubernetesMetadata.extraNamespaceLabels }
:   Type `list`, default `[]`.
    extra namespace labels to keep, appended to logFilteringNamespaceLabels

`olk.filebeat.kubernetesMetadata.extraNodeLabels` <a class="headerlink" href="#helm.olk.filebeat.kubernetesMetadata.extraNodeLabels" title="Permanent link">#</a> { #helm.olk.filebeat.kubernetesMetadata.extraNodeLabels }
:   Type `list`, default `[]`.
    extra node labels to keep, appended to logFilteringNodeLabels

`olk.filebeat.kubernetesMetadata.extraPodLabels` <a class="headerlink" href="#helm.olk.filebeat.kubernetesMetadata.extraPodLabels" title="Permanent link">#</a> { #helm.olk.filebeat.kubernetesMetadata.extraPodLabels }
:   Type `list`, default `[]`.
    extra pod labels to keep, appended to logFilteringPodLabels

`olk.filebeat.kubernetesMetadata.logFilteringNamespaceLabels` <a class="headerlink" href="#helm.olk.filebeat.kubernetesMetadata.logFilteringNamespaceLabels" title="Permanent link">#</a> { #helm.olk.filebeat.kubernetesMetadata.logFilteringNamespaceLabels }
:   Type `list`, default `["hopsworks.ai/project","hopsworks.ai/onlinefs-cluster"]`.
    namespace labels Hopsworks' log filtering reads

`olk.filebeat.kubernetesMetadata.logFilteringNodeLabels` <a class="headerlink" href="#helm.olk.filebeat.kubernetesMetadata.logFilteringNodeLabels" title="Permanent link">#</a> { #helm.olk.filebeat.kubernetesMetadata.logFilteringNodeLabels }
:   Type `list`, default `["kubernetes.io/hostname"]`.
    node labels Hopsworks' log filtering reads

`olk.filebeat.kubernetesMetadata.logFilteringPodLabels` <a class="headerlink" href="#helm.olk.filebeat.kubernetesMetadata.logFilteringPodLabels" title="Permanent link">#</a> { #helm.olk.filebeat.kubernetesMetadata.logFilteringPodLabels }
:   Type `list`.
    pod labels Hopsworks' log filtering reads

    ??? note "Default"

        ```yaml
        - name
        - app
        - app.kubernetes.io/name
        - service
        - rondbService
        - component
        - user
        - job-type
        - job-id
        - job-name
        - execution
        - jupyter
        - jupyter-id
        - jupyter-settings-id
        - kernel-id
        - spark-role
        - spark-app-selector
        - sparkoperator.k8s.io/launched-by-spark-operator
        - serving.hops.works/id
        - serving.hops.works/name
        - serving.hops.works/tool
        - serving.hops.works/model-name
        - serving.hops.works/model-version
        - serving.hops.works/model-server
        - serving.hops.works/project-id
        ```

`olk.filebeat.kubernetesMetadata.namespaceAnnotations` <a class="headerlink" href="#helm.olk.filebeat.kubernetesMetadata.namespaceAnnotations" title="Permanent link">#</a> { #helm.olk.filebeat.kubernetesMetadata.namespaceAnnotations }
:   Type `list`, default `[]`.
    namespace annotations to keep. Empty collects none.

`olk.filebeat.kubernetesMetadata.nodeAnnotations` <a class="headerlink" href="#helm.olk.filebeat.kubernetesMetadata.nodeAnnotations" title="Permanent link">#</a> { #helm.olk.filebeat.kubernetesMetadata.nodeAnnotations }
:   Type `list`, default `[]`.
    node annotations to keep. Empty collects none.

`olk.filebeat.kubernetesMetadata.podAnnotations` <a class="headerlink" href="#helm.olk.filebeat.kubernetesMetadata.podAnnotations" title="Permanent link">#</a> { #helm.olk.filebeat.kubernetesMetadata.podAnnotations }
:   Type `list`, default `[]`.
    pod annotations to keep. Empty collects none, filebeat's default.

`olk.filebeat.logs_locations[0].addKubernetesMetadata` <a class="headerlink" href="#helm.olk.filebeat.logs_locations.0.addKubernetesMetadata" title="Permanent link">#</a> { #helm.olk.filebeat.logs_locations.0.addKubernetesMetadata }
:   Type `bool`, default `true`.
    attach Kubernetes pod/namespace/node metadata to logs from this location, using the label whitelists in filebeat.kubernetesMetadata

`olk.filebeat.logs_locations[0].glob` <a class="headerlink" href="#helm.olk.filebeat.logs_locations.0.glob" title="Permanent link">#</a> { #helm.olk.filebeat.logs_locations.0.glob }
:   Type `string`, default `"/*.log"`.

`olk.filebeat.logs_locations[0].logtype` <a class="headerlink" href="#helm.olk.filebeat.logs_locations.0.logtype" title="Permanent link">#</a> { #helm.olk.filebeat.logs_locations.0.logtype }
:   Type `string`, default `"log"`.

`olk.filebeat.logs_locations[0].mountPaths[0]` <a class="headerlink" href="#helm.olk.filebeat.logs_locations.0.mountPaths.0" title="Permanent link">#</a> { #helm.olk.filebeat.logs_locations.0.mountPaths.0 }
:   Type `string`, default `"/var/log/containers"`.

`olk.filebeat.logs_locations[0].mountPaths[1]` <a class="headerlink" href="#helm.olk.filebeat.logs_locations.0.mountPaths.1" title="Permanent link">#</a> { #helm.olk.filebeat.logs_locations.0.mountPaths.1 }
:   Type `string`, default `"/var/log/pods"`.

`olk.filebeat.logs_locations[0].name` <a class="headerlink" href="#helm.olk.filebeat.logs_locations.0.name" title="Permanent link">#</a> { #helm.olk.filebeat.logs_locations.0.name }
:   Type `string`, default `"containerd"`.

`olk.filebeat.logs_locations[0].path` <a class="headerlink" href="#helm.olk.filebeat.logs_locations.0.path" title="Permanent link">#</a> { #helm.olk.filebeat.logs_locations.0.path }
:   Type `string`, default `"/var/log/containers"`.

`olk.filebeat.logs_locations[0].processors` <a class="headerlink" href="#helm.olk.filebeat.logs_locations.0.processors" title="Permanent link">#</a> { #helm.olk.filebeat.logs_locations.0.processors }
:   Type `list`, default `[]`.
    extra processors for this location, appended after the metadata processor. Each entry is itself a list.

`olk.filebeat.name` <a class="headerlink" href="#helm.olk.filebeat.name" title="Permanent link">#</a> { #helm.olk.filebeat.name }
:   Type `string`, default `"filebeat"`.

`olk.filebeat.resources.limits` <a class="headerlink" href="#helm.olk.filebeat.resources.limits" title="Permanent link">#</a> { #helm.olk.filebeat.resources.limits }
:   Type `object`, default `{"memory":"400Mi"}`.
    resources limits configuration

`olk.filebeat.resources.requests.cpu` <a class="headerlink" href="#helm.olk.filebeat.resources.requests.cpu" title="Permanent link">#</a> { #helm.olk.filebeat.resources.requests.cpu }
:   Type `string`, default `"100m"`.

`olk.filebeat.resources.requests.memory` <a class="headerlink" href="#helm.olk.filebeat.resources.requests.memory" title="Permanent link">#</a> { #helm.olk.filebeat.resources.requests.memory }
:   Type `string`, default `"200Mi"`.

`olk.filebeat.serviceAccount.annotations` <a class="headerlink" href="#helm.olk.filebeat.serviceAccount.annotations" title="Permanent link">#</a> { #helm.olk.filebeat.serviceAccount.annotations }
:   Type `object`, default `{}`.
    service account annotations

`olk.filebeat.terminationgraceperiod` <a class="headerlink" href="#helm.olk.filebeat.terminationgraceperiod" title="Permanent link">#</a> { #helm.olk.filebeat.terminationgraceperiod }
:   Type `int`, default `30`.

`olk.filebeat.tolerations` <a class="headerlink" href="#helm.olk.filebeat.tolerations" title="Permanent link">#</a> { #helm.olk.filebeat.tolerations }
:   Type `list`, default `[{"effect":"NoSchedule","operator":"Exists"}]`.
    tolerations for filebeat daemonset

</div>

## logstash { #helm-values-olk-logstash }

??? example "Defaults as YAML"

    ```yaml
    olk:
      logstash:
        additional_audit_outputs: ''
        batch_delay: 100
        batch_size: 100
        config:
          name: logstash-config
        debug: false
        extendServicesPipeline: []
        extraPipelines: []
        extraServices: []
        extraVolumeMounts: []
        extraVolumes: []
        hpa:
          enabled: false
          maxReplicas: 3
          targetCPUUtilizationPercentage: 80
          targetMemoryUtilizationPercentage: 80
        index_pattern: .services-%{+YYYY.MM.dd}
        name: logstash
        nodeSelector: {}
        plugins: []
        podDisruptionBudget:
          enabled: true
          minAvailable: 1
        port: 5044
        replicas: 1
        resources:
          requests:
            cpu: 200m
            memory: 2048Mi
        security_context:
          fsGroup: 1000
          runAsGroup: 1000
          runAsNonRoot: true
          runAsUser: 1000
        service:
          annotations:
            consul.hashicorp.com/service-name: logstash
            consul.hashicorp.com/service-tags: jupyter,pythonjobs
          type: ClusterIP
        tolerations: []
        topologySpreadConstraint: {}
        version: 7.17.29.6
        workers: 4
    ```

<div class="hops-values" markdown>

`olk.logstash.additional_audit_outputs` <a class="headerlink" href="#helm.olk.logstash.additional_audit_outputs" title="Permanent link">#</a> { #helm.olk.logstash.additional_audit_outputs }
:   Type `string`, default `""`.

`olk.logstash.batch_delay` <a class="headerlink" href="#helm.olk.logstash.batch_delay" title="Permanent link">#</a> { #helm.olk.logstash.batch_delay }
:   Type `int`, default `100`.

`olk.logstash.batch_size` <a class="headerlink" href="#helm.olk.logstash.batch_size" title="Permanent link">#</a> { #helm.olk.logstash.batch_size }
:   Type `int`, default `100`.

`olk.logstash.config.name` <a class="headerlink" href="#helm.olk.logstash.config.name" title="Permanent link">#</a> { #helm.olk.logstash.config.name }
:   Type `string`, default `"logstash-config"`.

`olk.logstash.debug` <a class="headerlink" href="#helm.olk.logstash.debug" title="Permanent link">#</a> { #helm.olk.logstash.debug }
:   Type `bool`, default `false`.

`olk.logstash.extendServicesPipeline` <a class="headerlink" href="#helm.olk.logstash.extendServicesPipeline" title="Permanent link">#</a> { #helm.olk.logstash.extendServicesPipeline }
:   Type `list`, default `[]`.
    extend the services pipeline to collect logs for other services besides the default. You need to define the kuberentes label key and value to identifiy the service. The serviceLabelValue will be used as the service name, and you can add extra mutation logic to rename some of the fields of the service log. 

`olk.logstash.extraPipelines` <a class="headerlink" href="#helm.olk.logstash.extraPipelines" title="Permanent link">#</a> { #helm.olk.logstash.extraPipelines }
:   Type `list`, default `[]`.
    logstash extraPipelines

`olk.logstash.extraServices` <a class="headerlink" href="#helm.olk.logstash.extraServices" title="Permanent link">#</a> { #helm.olk.logstash.extraServices }
:   Type `list`, default `[]`.
    logstash extraServices

`olk.logstash.extraVolumeMounts` <a class="headerlink" href="#helm.olk.logstash.extraVolumeMounts" title="Permanent link">#</a> { #helm.olk.logstash.extraVolumeMounts }
:   Type `list`, default `[]`.

`olk.logstash.extraVolumes` <a class="headerlink" href="#helm.olk.logstash.extraVolumes" title="Permanent link">#</a> { #helm.olk.logstash.extraVolumes }
:   Type `list`, default `[]`.

`olk.logstash.hpa.enabled` <a class="headerlink" href="#helm.olk.logstash.hpa.enabled" title="Permanent link">#</a> { #helm.olk.logstash.hpa.enabled }
:   Type `bool`, default `false`.

`olk.logstash.hpa.maxReplicas` <a class="headerlink" href="#helm.olk.logstash.hpa.maxReplicas" title="Permanent link">#</a> { #helm.olk.logstash.hpa.maxReplicas }
:   Type `int`, default `3`.

`olk.logstash.hpa.targetCPUUtilizationPercentage` <a class="headerlink" href="#helm.olk.logstash.hpa.targetCPUUtilizationPercentage" title="Permanent link">#</a> { #helm.olk.logstash.hpa.targetCPUUtilizationPercentage }
:   Type `int`, default `80`.

`olk.logstash.hpa.targetMemoryUtilizationPercentage` <a class="headerlink" href="#helm.olk.logstash.hpa.targetMemoryUtilizationPercentage" title="Permanent link">#</a> { #helm.olk.logstash.hpa.targetMemoryUtilizationPercentage }
:   Type `int`, default `80`.

`olk.logstash.index_pattern` <a class="headerlink" href="#helm.olk.logstash.index_pattern" title="Permanent link">#</a> { #helm.olk.logstash.index_pattern }
:   Type `string`, default `".services-%{+YYYY.MM.dd}"`.

`olk.logstash.name` <a class="headerlink" href="#helm.olk.logstash.name" title="Permanent link">#</a> { #helm.olk.logstash.name }
:   Type `string`, default `"logstash"`.

`olk.logstash.nodeSelector` <a class="headerlink" href="#helm.olk.logstash.nodeSelector" title="Permanent link">#</a> { #helm.olk.logstash.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

`olk.logstash.plugins` <a class="headerlink" href="#helm.olk.logstash.plugins" title="Permanent link">#</a> { #helm.olk.logstash.plugins }
:   Type `list`, default `[]`.

`olk.logstash.podDisruptionBudget.enabled` <a class="headerlink" href="#helm.olk.logstash.podDisruptionBudget.enabled" title="Permanent link">#</a> { #helm.olk.logstash.podDisruptionBudget.enabled }
:   Type `bool`, default `true`.

`olk.logstash.podDisruptionBudget.minAvailable` <a class="headerlink" href="#helm.olk.logstash.podDisruptionBudget.minAvailable" title="Permanent link">#</a> { #helm.olk.logstash.podDisruptionBudget.minAvailable }
:   Type `int`, default `1`.

`olk.logstash.port` <a class="headerlink" href="#helm.olk.logstash.port" title="Permanent link">#</a> { #helm.olk.logstash.port }
:   Type `int`, default `5044`.

`olk.logstash.replicas` <a class="headerlink" href="#helm.olk.logstash.replicas" title="Permanent link">#</a> { #helm.olk.logstash.replicas }
:   Type `int`, default `1`.

`olk.logstash.resources` <a class="headerlink" href="#helm.olk.logstash.resources" title="Permanent link">#</a> { #helm.olk.logstash.resources }
:   Type `object`, default `{"requests":{"cpu":"200m","memory":"2048Mi"}}`.
    resources configuration

`olk.logstash.security_context.fsGroup` <a class="headerlink" href="#helm.olk.logstash.security_context.fsGroup" title="Permanent link">#</a> { #helm.olk.logstash.security_context.fsGroup }
:   Type `int`, default `1000`.

`olk.logstash.security_context.runAsGroup` <a class="headerlink" href="#helm.olk.logstash.security_context.runAsGroup" title="Permanent link">#</a> { #helm.olk.logstash.security_context.runAsGroup }
:   Type `int`, default `1000`.

`olk.logstash.security_context.runAsNonRoot` <a class="headerlink" href="#helm.olk.logstash.security_context.runAsNonRoot" title="Permanent link">#</a> { #helm.olk.logstash.security_context.runAsNonRoot }
:   Type `bool`, default `true`.

`olk.logstash.security_context.runAsUser` <a class="headerlink" href="#helm.olk.logstash.security_context.runAsUser" title="Permanent link">#</a> { #helm.olk.logstash.security_context.runAsUser }
:   Type `int`, default `1000`.

`olk.logstash.service.annotations."consul.hashicorp.com/service-name"` <a class="headerlink" href="#helm.olk.logstash.service.annotations.consul.hashicorp.com-service-name" title="Permanent link">#</a> { #helm.olk.logstash.service.annotations.consul.hashicorp.com-service-name }
:   Type `string`, default `"logstash"`.

`olk.logstash.service.annotations."consul.hashicorp.com/service-tags"` <a class="headerlink" href="#helm.olk.logstash.service.annotations.consul.hashicorp.com-service-tags" title="Permanent link">#</a> { #helm.olk.logstash.service.annotations.consul.hashicorp.com-service-tags }
:   Type `string`, default `"jupyter,pythonjobs"`.

`olk.logstash.service.type` <a class="headerlink" href="#helm.olk.logstash.service.type" title="Permanent link">#</a> { #helm.olk.logstash.service.type }
:   Type `string`, default `"ClusterIP"`.

`olk.logstash.tolerations` <a class="headerlink" href="#helm.olk.logstash.tolerations" title="Permanent link">#</a> { #helm.olk.logstash.tolerations }
:   Type `list`, default `[]`.

`olk.logstash.topologySpreadConstraint` <a class="headerlink" href="#helm.olk.logstash.topologySpreadConstraint" title="Permanent link">#</a> { #helm.olk.logstash.topologySpreadConstraint }
:   Type `object`, default `{}`.
    The default topology spread constraint. If not defined the global topology spread constraint would be used instead.

`olk.logstash.version` <a class="headerlink" href="#helm.olk.logstash.version" title="Permanent link">#</a> { #helm.olk.logstash.version }
:   Type `string`, default `"7.17.29.6"`.

`olk.logstash.workers` <a class="headerlink" href="#helm.olk.logstash.workers" title="Permanent link">#</a> { #helm.olk.logstash.workers }
:   Type `int`, default `4`.

</div>

## opensearch { #helm-values-olk-opensearch }

??? example "Defaults as YAML"

    ```yaml
    olk:
      opensearch:
        audit:
          enable_rest: true
          enable_transport: false
          enabled: false
          retentionDays: 7
        backup:
          enabled: null
          repositories: {}
          ttl: null
        config:
          name: opensearch-config
        cors:
          allow_origin: '*'
        externalLoadBalancer:
          annotations: {}
          class: null
          enabled: null
          managed: null
          nodeSelector: {}
        jvmOpts: ''
        knn:
          cache_expire: true
          circuit_breaker:
            percent: 0.75
            triggered: true
          index_threads: 1
          memory:
            circuit_breaker:
              limit: 50%
        mandatoryIndices:
        - projects
        - featurestore
        max_shards_per_node: 3000
        memory:
          xms: 2g
          xmx: 2g
        name: opensearch
        nodeSelector: {}
        plugins: []
        podDisruptionBudget:
          enabled: true
          minAvailable: 1
        port: 9200
        protocol: https
        replicas: 1
        resources:
          limits:
            memory: 4000Mi
          requests:
            cpu: 100m
            memory: 2000Mi
        restore:
          enabled: null
          list_snapshots: true
          pause_backup_while_restoring: SKIP
          repositories: {}
        security:
          admin_locality: elkadmin
          create_secret: true
          default_tenant: Private
          extraDnsNames: []
          extraIpAddresses: []
          locality: elastic
          multitenancy_enabled: true
        service:
          annotations:
            consul.hashicorp.com/service-name: elastic
            consul.hashicorp.com/service-port: http
            consul.hashicorp.com/service-tags: rest
          headlessName: opensearch-headless
        serviceAccount:
          annotations: {}
        serviceAccountName: opensearch
        setVMMaxMapCount: true
        storageClassName: null
        storage_size: 20Gi
        tolerations: []
        topologySpreadConstraint: {}
        transport_port: 9300
        ttlSecondsAfterFinished: null
        version: 2.19.6.3
    ```

<div class="hops-values" markdown>

`olk.opensearch.audit.enable_rest` <a class="headerlink" href="#helm.olk.opensearch.audit.enable_rest" title="Permanent link">#</a> { #helm.olk.opensearch.audit.enable_rest }
:   Type `bool`, default `true`.
    Audit the REST layer (plugins.security.audit.config.enable_rest). Only applies when audit.enabled is true.

`olk.opensearch.audit.enable_transport` <a class="headerlink" href="#helm.olk.opensearch.audit.enable_transport" title="Permanent link">#</a> { #helm.olk.opensearch.audit.enable_transport }
:   Type `bool`, default `false`.
    Audit the transport layer (plugins.security.audit.config.enable_transport). Only applies when audit.enabled is true.

`olk.opensearch.audit.enabled` <a class="headerlink" href="#helm.olk.opensearch.audit.enabled" title="Permanent link">#</a> { #helm.olk.opensearch.audit.enabled }
:   Type `bool`, default `false`.
    Enable OpenSearch security audit logging to an in-cluster `security-auditlog-*` index. Disabled by default. When enabled, the chart also installs an ISM policy that deletes these daily indices after `audit.retentionDays`, so they don't grow unbounded. On single-node clusters the audit index stays yellow (its replica cannot be allocated; harmless); on multi-node it is green.

`olk.opensearch.audit.retentionDays` <a class="headerlink" href="#helm.olk.opensearch.audit.retentionDays" title="Permanent link">#</a> { #helm.olk.opensearch.audit.retentionDays }
:   Type `int`, default `7`.
    Days to retain `security-auditlog-*` indices before ISM deletes them. Only applies when audit.enabled is true, and bounds the otherwise-unbounded daily audit index growth. NOTE: the `security-auditlog-retention` ISM policy is created once and never updated, so changing this value on an existing cluster has no effect on its own; to apply a new value, delete that ISM policy so it is recreated with the new setting on the next sync.

`olk.opensearch.backup.enabled` <a class="headerlink" href="#helm.olk.opensearch.backup.enabled" title="Permanent link">#</a> { #helm.olk.opensearch.backup.enabled }
:   Type `string`, default `nil`.

`olk.opensearch.backup.repositories` <a class="headerlink" href="#helm.olk.opensearch.backup.repositories" title="Permanent link">#</a> { #helm.olk.opensearch.backup.repositories }
:   Type `object`, default `{}`.
    backup repository configuration

`olk.opensearch.backup.ttl` <a class="headerlink" href="#helm.olk.opensearch.backup.ttl" title="Permanent link">#</a> { #helm.olk.opensearch.backup.ttl }
:   Type `string`, default `nil`.
    time to live to control when to clean up backups. It is a number followed by either d (days) or h (hours) suffix.

`olk.opensearch.config.name` <a class="headerlink" href="#helm.olk.opensearch.config.name" title="Permanent link">#</a> { #helm.olk.opensearch.config.name }
:   Type `string`, default `"opensearch-config"`.

`olk.opensearch.cors.allow_origin` <a class="headerlink" href="#helm.olk.opensearch.cors.allow_origin" title="Permanent link">#</a> { #helm.olk.opensearch.cors.allow_origin }
:   Type `string`, default `"*"`.

`olk.opensearch.externalLoadBalancer.annotations` <a class="headerlink" href="#helm.olk.opensearch.externalLoadBalancer.annotations" title="Permanent link">#</a> { #helm.olk.opensearch.externalLoadBalancer.annotations }
:   Type `object`, default `{}`.
    load balancer annotations

`olk.opensearch.externalLoadBalancer.class` <a class="headerlink" href="#helm.olk.opensearch.externalLoadBalancer.class" title="Permanent link">#</a> { #helm.olk.opensearch.externalLoadBalancer.class }
:   Type `string`, default `nil`.
    load balancer class name

`olk.opensearch.externalLoadBalancer.enabled` <a class="headerlink" href="#helm.olk.opensearch.externalLoadBalancer.enabled" title="Permanent link">#</a> { #helm.olk.opensearch.externalLoadBalancer.enabled }
:   Type `string`, default `nil`.
    Enable External Load Balancers for Opensearch. If not set the .global._hopsworks.externalLoadBalancers.enabled will be used instead

`olk.opensearch.externalLoadBalancer.managed` <a class="headerlink" href="#helm.olk.opensearch.externalLoadBalancer.managed" title="Permanent link">#</a> { #helm.olk.opensearch.externalLoadBalancer.managed }
:   Type `string`, default `nil`.
    Cloud provider provisions Load Balancers. If not set the .global._hopsworks.externalLoadBalancers.managed will be used instead

`olk.opensearch.externalLoadBalancer.nodeSelector` <a class="headerlink" href="#helm.olk.opensearch.externalLoadBalancer.nodeSelector" title="Permanent link">#</a> { #helm.olk.opensearch.externalLoadBalancer.nodeSelector }
:   Type `object`, default `{}`.
    selector for nodes the load balancer can use to route traffic

`olk.opensearch.jvmOpts` <a class="headerlink" href="#helm.olk.opensearch.jvmOpts" title="Permanent link">#</a> { #helm.olk.opensearch.jvmOpts }
:   Type `string`, default `""`.
    JVM Options to provide to Opensearch

`olk.opensearch.knn.cache_expire` <a class="headerlink" href="#helm.olk.opensearch.knn.cache_expire" title="Permanent link">#</a> { #helm.olk.opensearch.knn.cache_expire }
:   Type `bool`, default `true`.

`olk.opensearch.knn.circuit_breaker.percent` <a class="headerlink" href="#helm.olk.opensearch.knn.circuit_breaker.percent" title="Permanent link">#</a> { #helm.olk.opensearch.knn.circuit_breaker.percent }
:   Type `float`, default `0.75`.

`olk.opensearch.knn.circuit_breaker.triggered` <a class="headerlink" href="#helm.olk.opensearch.knn.circuit_breaker.triggered" title="Permanent link">#</a> { #helm.olk.opensearch.knn.circuit_breaker.triggered }
:   Type `bool`, default `true`.

`olk.opensearch.knn.index_threads` <a class="headerlink" href="#helm.olk.opensearch.knn.index_threads" title="Permanent link">#</a> { #helm.olk.opensearch.knn.index_threads }
:   Type `int`, default `1`.

`olk.opensearch.knn.memory.circuit_breaker.limit` <a class="headerlink" href="#helm.olk.opensearch.knn.memory.circuit_breaker.limit" title="Permanent link">#</a> { #helm.olk.opensearch.knn.memory.circuit_breaker.limit }
:   Type `string`, default `"50%"`.

`olk.opensearch.mandatoryIndices[0]` <a class="headerlink" href="#helm.olk.opensearch.mandatoryIndices.0" title="Permanent link">#</a> { #helm.olk.opensearch.mandatoryIndices.0 }
:   Type `string`, default `"projects"`.

`olk.opensearch.mandatoryIndices[1]` <a class="headerlink" href="#helm.olk.opensearch.mandatoryIndices.1" title="Permanent link">#</a> { #helm.olk.opensearch.mandatoryIndices.1 }
:   Type `string`, default `"featurestore"`.

`olk.opensearch.max_shards_per_node` <a class="headerlink" href="#helm.olk.opensearch.max_shards_per_node" title="Permanent link">#</a> { #helm.olk.opensearch.max_shards_per_node }
:   Type `int`, default `3000`.

`olk.opensearch.memory.xms` <a class="headerlink" href="#helm.olk.opensearch.memory.xms" title="Permanent link">#</a> { #helm.olk.opensearch.memory.xms }
:   Type `string`, default `"2g"`.

`olk.opensearch.memory.xmx` <a class="headerlink" href="#helm.olk.opensearch.memory.xmx" title="Permanent link">#</a> { #helm.olk.opensearch.memory.xmx }
:   Type `string`, default `"2g"`.

`olk.opensearch.name` <a class="headerlink" href="#helm.olk.opensearch.name" title="Permanent link">#</a> { #helm.olk.opensearch.name }
:   Type `string`, default `"opensearch"`.

`olk.opensearch.nodeSelector` <a class="headerlink" href="#helm.olk.opensearch.nodeSelector" title="Permanent link">#</a> { #helm.olk.opensearch.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

`olk.opensearch.plugins` <a class="headerlink" href="#helm.olk.opensearch.plugins" title="Permanent link">#</a> { #helm.olk.opensearch.plugins }
:   Type `list`, default `[]`.

`olk.opensearch.podDisruptionBudget.enabled` <a class="headerlink" href="#helm.olk.opensearch.podDisruptionBudget.enabled" title="Permanent link">#</a> { #helm.olk.opensearch.podDisruptionBudget.enabled }
:   Type `bool`, default `true`.

`olk.opensearch.podDisruptionBudget.minAvailable` <a class="headerlink" href="#helm.olk.opensearch.podDisruptionBudget.minAvailable" title="Permanent link">#</a> { #helm.olk.opensearch.podDisruptionBudget.minAvailable }
:   Type `int`, default `1`.

`olk.opensearch.port` <a class="headerlink" href="#helm.olk.opensearch.port" title="Permanent link">#</a> { #helm.olk.opensearch.port }
:   Type `int`, default `9200`.

`olk.opensearch.protocol` <a class="headerlink" href="#helm.olk.opensearch.protocol" title="Permanent link">#</a> { #helm.olk.opensearch.protocol }
:   Type `string`, default `"https"`.

`olk.opensearch.replicas` <a class="headerlink" href="#helm.olk.opensearch.replicas" title="Permanent link">#</a> { #helm.olk.opensearch.replicas }
:   Type `int`, default `1`.

`olk.opensearch.resources.limits` <a class="headerlink" href="#helm.olk.opensearch.resources.limits" title="Permanent link">#</a> { #helm.olk.opensearch.resources.limits }
:   Type `object`, default `{"memory":"4000Mi"}`.
    resources limits configuration

`olk.opensearch.resources.requests.cpu` <a class="headerlink" href="#helm.olk.opensearch.resources.requests.cpu" title="Permanent link">#</a> { #helm.olk.opensearch.resources.requests.cpu }
:   Type `string`, default `"100m"`.

`olk.opensearch.resources.requests.memory` <a class="headerlink" href="#helm.olk.opensearch.resources.requests.memory" title="Permanent link">#</a> { #helm.olk.opensearch.resources.requests.memory }
:   Type `string`, default `"2000Mi"`.

`olk.opensearch.restore.enabled` <a class="headerlink" href="#helm.olk.opensearch.restore.enabled" title="Permanent link">#</a> { #helm.olk.opensearch.restore.enabled }
:   Type `string`, default `nil`.
    If true an initial job will be created to restore the data from the backup. Backup jobs will bypass creating snapshots while this job is running.

`olk.opensearch.restore.list_snapshots` <a class="headerlink" href="#helm.olk.opensearch.restore.list_snapshots" title="Permanent link">#</a> { #helm.olk.opensearch.restore.list_snapshots }
:   Type `bool`, default `true`.

`olk.opensearch.restore.pause_backup_while_restoring` <a class="headerlink" href="#helm.olk.opensearch.restore.pause_backup_while_restoring" title="Permanent link">#</a> { #helm.olk.opensearch.restore.pause_backup_while_restoring }
:   Type `string`, default `"SKIP"`.
    If set, the backup jobs will be paused while the restore job is running. Values are SKIP or PAUSE, in case none, the backup will wait for the restore to finish

`olk.opensearch.restore.repositories` <a class="headerlink" href="#helm.olk.opensearch.restore.repositories" title="Permanent link">#</a> { #helm.olk.opensearch.restore.repositories }
:   Type `object`, default `{}`.
    restore repositories configuration

`olk.opensearch.security.admin_locality` <a class="headerlink" href="#helm.olk.opensearch.security.admin_locality" title="Permanent link">#</a> { #helm.olk.opensearch.security.admin_locality }
:   Type `string`, default `"elkadmin"`.

`olk.opensearch.security.create_secret` <a class="headerlink" href="#helm.olk.opensearch.security.create_secret" title="Permanent link">#</a> { #helm.olk.opensearch.security.create_secret }
:   Type `bool`, default `true`.
    Create the opensearch-users-secrets secret with the opensearch internal users passwords 

`olk.opensearch.security.default_tenant` <a class="headerlink" href="#helm.olk.opensearch.security.default_tenant" title="Permanent link">#</a> { #helm.olk.opensearch.security.default_tenant }
:   Type `string`, default `"Private"`.
    Default OpenSearch tenant for Dashboards users. A non-empty value suppresses the OpenSearch Dashboards 2.x "Select your tenant" popup (the plugin only prompts when the reported default_tenant is empty). Hopsworks links open Dashboards with the Private tenant, so "Private" matches that and keeps multitenancy/index-pattern isolation intact. Set to "" to restore the popup / leave the default tenant unset.

`olk.opensearch.security.extraDnsNames` <a class="headerlink" href="#helm.olk.opensearch.security.extraDnsNames" title="Permanent link">#</a> { #helm.olk.opensearch.security.extraDnsNames }
:   Type `list`, default `[]`.
    Additional DNS names to add as SAN to Datanode x.509 certificate

`olk.opensearch.security.extraIpAddresses` <a class="headerlink" href="#helm.olk.opensearch.security.extraIpAddresses" title="Permanent link">#</a> { #helm.olk.opensearch.security.extraIpAddresses }
:   Type `list`, default `[]`.
    Additional IP addresses to add as SAN to Datanode x.509 certificate

`olk.opensearch.security.locality` <a class="headerlink" href="#helm.olk.opensearch.security.locality" title="Permanent link">#</a> { #helm.olk.opensearch.security.locality }
:   Type `string`, default `"elastic"`.

`olk.opensearch.security.multitenancy_enabled` <a class="headerlink" href="#helm.olk.opensearch.security.multitenancy_enabled" title="Permanent link">#</a> { #helm.olk.opensearch.security.multitenancy_enabled }
:   Type `bool`, default `true`.

`olk.opensearch.service.annotations."consul.hashicorp.com/service-name"` <a class="headerlink" href="#helm.olk.opensearch.service.annotations.consul.hashicorp.com-service-name" title="Permanent link">#</a> { #helm.olk.opensearch.service.annotations.consul.hashicorp.com-service-name }
:   Type `string`, default `"elastic"`.

`olk.opensearch.service.annotations."consul.hashicorp.com/service-port"` <a class="headerlink" href="#helm.olk.opensearch.service.annotations.consul.hashicorp.com-service-port" title="Permanent link">#</a> { #helm.olk.opensearch.service.annotations.consul.hashicorp.com-service-port }
:   Type `string`, default `"http"`.

`olk.opensearch.service.annotations."consul.hashicorp.com/service-tags"` <a class="headerlink" href="#helm.olk.opensearch.service.annotations.consul.hashicorp.com-service-tags" title="Permanent link">#</a> { #helm.olk.opensearch.service.annotations.consul.hashicorp.com-service-tags }
:   Type `string`, default `"rest"`.

`olk.opensearch.service.headlessName` <a class="headerlink" href="#helm.olk.opensearch.service.headlessName" title="Permanent link">#</a> { #helm.olk.opensearch.service.headlessName }
:   Type `string`, default `"opensearch-headless"`.

`olk.opensearch.serviceAccount.annotations` <a class="headerlink" href="#helm.olk.opensearch.serviceAccount.annotations" title="Permanent link">#</a> { #helm.olk.opensearch.serviceAccount.annotations }
:   Type `object`, default `{}`.
    service account annotations

`olk.opensearch.serviceAccountName` <a class="headerlink" href="#helm.olk.opensearch.serviceAccountName" title="Permanent link">#</a> { #helm.olk.opensearch.serviceAccountName }
:   Type `string`, default `"opensearch"`.

`olk.opensearch.setVMMaxMapCount` <a class="headerlink" href="#helm.olk.opensearch.setVMMaxMapCount" title="Permanent link">#</a> { #helm.olk.opensearch.setVMMaxMapCount }
:   Type `bool`, default `true`.
    <https://docs.opensearch.org/2.19/install-and-configure/install-opensearch/index/#important-settings>

`olk.opensearch.storageClassName` <a class="headerlink" href="#helm.olk.opensearch.storageClassName" title="Permanent link">#</a> { #helm.olk.opensearch.storageClassName }
:   Type `string`, default `nil`.
    storage class name

`olk.opensearch.storage_size` <a class="headerlink" href="#helm.olk.opensearch.storage_size" title="Permanent link">#</a> { #helm.olk.opensearch.storage_size }
:   Type `string`, default `"20Gi"`.

`olk.opensearch.tolerations` <a class="headerlink" href="#helm.olk.opensearch.tolerations" title="Permanent link">#</a> { #helm.olk.opensearch.tolerations }
:   Type `list`, default `[]`.

`olk.opensearch.topologySpreadConstraint` <a class="headerlink" href="#helm.olk.opensearch.topologySpreadConstraint" title="Permanent link">#</a> { #helm.olk.opensearch.topologySpreadConstraint }
:   Type `object`, default `{}`.
    The default topology spread constraint. If not defined the global topology spread constraint would be used instead.

`olk.opensearch.transport_port` <a class="headerlink" href="#helm.olk.opensearch.transport_port" title="Permanent link">#</a> { #helm.olk.opensearch.transport_port }
:   Type `int`, default `9300`.

`olk.opensearch.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.olk.opensearch.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.olk.opensearch.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    TTL in seconds for the create-repos Job. Overrides global default.

`olk.opensearch.version` <a class="headerlink" href="#helm.olk.opensearch.version" title="Permanent link">#</a> { #helm.olk.opensearch.version }
:   Type `string`, default `"2.19.6.3"`.

</div>

<!-- END GENERATED VALUES -->
