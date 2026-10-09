# Consul values { #helm-values-consul }

Values under `consul` configure Consul, which provides service discovery and DNS between the Hopsworks services.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.1.1` (Hopsworks `5.1.1`)._

Deployed when [`global._hopsworks.full_platform`](global.md#helm.global._hopsworks.full_platform) is `true`.

!!! info "Upstream charts"

    - Values under `consul.consul` go to [`consul` 1.8.16](https://artifacthub.io/packages/helm/hashicorp/consul/1.8.16) from `https://helm.releases.hashicorp.com`.

    Only the values Hopsworks sets under `consul.consul` are listed on this page.
    Any other value of the chart can be set there too; the link opens its documentation for the version Hopsworks pins.

## General { #helm-values-consul-general }

??? example "Defaults as YAML"

    ```yaml
    consul:
      autoConfigureCoreDNS: true
      autoConfigureCoreDNSPort: 53
      autoConfigureJobResources:
        limits:
          cpu: 300m
      autoconfig:
        serviceAccount:
          annotations: {}
        ttlSecondsAfterFinished: null
      cleanupOnUninstall:
        enabled: true
        ttlSecondsAfterFinished: null
      consul:
        client:
          dnsPolicy: ClusterFirstWithHostNet
          hostNetwork: true
        connectInject:
          enabled: false
        dns:
          enabled: true
        global:
          acls:
            manageSystemACLs: true
            nodeSelector: null
            tolerations: ''
          datacenter: dc1
          domain: consul
          enabled: true
          gossipEncryption:
            autoGenerate: true
          image: docker.hops.works/hashicorp/consul:1.16.4-alpine-h1
          imageK8S: docker.hops.works/hashicorp/consul-k8s-control-plane:1.8.16
          logLevel: info
          metrics:
            disableAgentHostName: true
            enableAgentMetrics: true
            enableGatewayMetrics: false
            enabled: true
          name: null
          tls:
            enabled: true
        metrics:
          enabled: true
          rbac:
            annotations: {}
            create: true
            extraRoleRules: []
            name: consul-metrics-role
            useExistingRole: false
          serviceAccount:
            annotations: {}
            create: true
            name: consul-metrics-default
        server:
          connect: false
          enabled: true
          logLevel: info
          nodeSelector: null
          replicas: 3
          resources:
            limits:
              cpu: 100m
              memory: 350Mi
            requests:
              cpu: 100m
              memory: 200Mi
          storageClass: null
          tolerations: ''
          topologySpreadConstraints: |
            - maxSkew: 1
              topologyKey: topology.kubernetes.io/zone
              whenUnsatisfiable: ScheduleAnyway
              labelSelector:
                matchLabels:
                  app: consul
                  component: server
        syncCatalog:
          default: true
          enabled: true
          k8sAllowNamespaces:
          - '*'
          nodeSelector: null
          resources:
            limits:
              cpu: 50m
              memory: 100Mi
            requests:
              cpu: 50m
              memory: 100Mi
          toConsul: true
          toK8S: false
          tolerations: ''
        ui:
          enabled: true
      corednsConfigMapName: coredns
      corednsDeploymentName: coredns
      fullnameOverride: null
      hopsworkslib: {}
      nameOverride: null
      networkPolicy:
        enabled: false
      nodeSelector: {}
      tolerations: []
    ```

<div class="hops-values" markdown>

`consul` <a class="headerlink" href="#helm.consul" title="Permanent link">#</a> { #helm.consul }
:   Type `object`, default `{"consul":{"server":{"storageClass":null}}}`.
    override consul values

`consul.autoConfigureCoreDNS` <a class="headerlink" href="#helm.consul.autoConfigureCoreDNS" title="Permanent link">#</a> { #helm.consul.autoConfigureCoreDNS }
:   Type `bool`, default `true`.

`consul.autoConfigureCoreDNSPort` <a class="headerlink" href="#helm.consul.autoConfigureCoreDNSPort" title="Permanent link">#</a> { #helm.consul.autoConfigureCoreDNSPort }
:   Type `int`, default `53`.

`consul.autoConfigureJobResources` <a class="headerlink" href="#helm.consul.autoConfigureJobResources" title="Permanent link">#</a> { #helm.consul.autoConfigureJobResources }
:   Type `object`, default `{"limits":{"cpu":"300m"}}`.
    resources configuration

`consul.autoConfigureJobResources.limits` <a class="headerlink" href="#helm.consul.autoConfigureJobResources.limits" title="Permanent link">#</a> { #helm.consul.autoConfigureJobResources.limits }
:   Type `object`, default `{"cpu":"300m"}`.
    resource limits configuration

`consul.autoconfig.serviceAccount.annotations` <a class="headerlink" href="#helm.consul.autoconfig.serviceAccount.annotations" title="Permanent link">#</a> { #helm.consul.autoconfig.serviceAccount.annotations }
:   Type `object`, default `{}`.
    service account annotations

`consul.autoconfig.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.consul.autoconfig.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.consul.autoconfig.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    TTL in seconds for the autoconfig coredns Job. Overrides global default.

`consul.cleanupOnUninstall` <a class="headerlink" href="#helm.consul.cleanupOnUninstall" title="Permanent link">#</a> { #helm.consul.cleanupOnUninstall }
:   Type `object`, default `{"enabled":true,"ttlSecondsAfterFinished":null}`.
    post-delete cleanup of Consul runtime leftovers (consul-k8s ACL/gossip secrets, the metrics-acl-token secret, and the upstream install-hook RBAC) that Helm/ArgoCD never tracked and so never prune. Also deletes Consul server PVCs when global._hopsworks.wipeDataOnUninstall is enabled (except hopsworks.ai/keep=true).

`consul.cleanupOnUninstall.enabled` <a class="headerlink" href="#helm.consul.cleanupOnUninstall.enabled" title="Permanent link">#</a> { #helm.consul.cleanupOnUninstall.enabled }
:   Type `bool`, default `true`.
    enable the post-delete Consul cleanup hook

`consul.cleanupOnUninstall.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.consul.cleanupOnUninstall.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.consul.cleanupOnUninstall.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    ttlSecondsAfterFinished for the cleanup Job; null falls through to the global default

`consul.consul` <a class="headerlink" href="#helm.consul.consul" title="Permanent link">#</a> { #helm.consul.consul }
:   Type `object`, passed to the [`consul` 1.8.16](https://artifacthub.io/packages/helm/hashicorp/consul/1.8.16) chart, whose other values are documented there.
    override consul values

    ??? note "Default"

        ```yaml
        client:
          dnsPolicy: ClusterFirstWithHostNet
          hostNetwork: true
        connectInject:
          enabled: false
        dns:
          enabled: true
        global:
          acls:
            manageSystemACLs: true
            nodeSelector: null
            tolerations: ''
          datacenter: dc1
          domain: consul
          enabled: true
          gossipEncryption:
            autoGenerate: true
          image: docker.hops.works/hashicorp/consul:1.16.4-alpine-h1
          imageK8S: docker.hops.works/hashicorp/consul-k8s-control-plane:1.8.16
          logLevel: info
          metrics:
            disableAgentHostName: true
            enableAgentMetrics: true
            enableGatewayMetrics: false
            enabled: true
          name: null
          tls:
            enabled: true
        metrics:
          enabled: true
          rbac:
            annotations: {}
            create: true
            extraRoleRules: []
            name: consul-metrics-role
            useExistingRole: false
          serviceAccount:
            annotations: {}
            create: true
            name: consul-metrics-default
        server:
          connect: false
          enabled: true
          logLevel: info
          nodeSelector: null
          replicas: 3
          resources:
            limits:
              cpu: 100m
              memory: 350Mi
            requests:
              cpu: 100m
              memory: 200Mi
          storageClass: null
          tolerations: ''
          topologySpreadConstraints: |
            - maxSkew: 1
              topologyKey: topology.kubernetes.io/zone
              whenUnsatisfiable: ScheduleAnyway
              labelSelector:
                matchLabels:
                  app: consul
                  component: server
        syncCatalog:
          default: true
          enabled: true
          k8sAllowNamespaces:
          - '*'
          nodeSelector: null
          resources:
            limits:
              cpu: 50m
              memory: 100Mi
            requests:
              cpu: 50m
              memory: 100Mi
          toConsul: true
          toK8S: false
          tolerations: ''
        ui:
          enabled: true
        ```

`consul.corednsConfigMapName` <a class="headerlink" href="#helm.consul.corednsConfigMapName" title="Permanent link">#</a> { #helm.consul.corednsConfigMapName }
:   Type `string`, default `"coredns"`.
    the name of the coredns configmap. This name is only used when global._hopsworks.cloudProvider does not equal to AZURE, OVH, or GCP. For AZURE and OVH, coredns-custom is being used by default and for GCP, kube-dns is being used by default.

`consul.corednsDeploymentName` <a class="headerlink" href="#helm.consul.corednsDeploymentName" title="Permanent link">#</a> { #helm.consul.corednsDeploymentName }
:   Type `string`, default `"coredns"`.
    the name of the coredns deployment. This name is only used when global._hopsworks.cloudProvider does not equal to AZURE, OVH, or GCP.

`consul.fullnameOverride` <a class="headerlink" href="#helm.consul.fullnameOverride" title="Permanent link">#</a> { #helm.consul.fullnameOverride }
:   Type `string`, default `nil`.
    override app fully qualified name 

`consul.hopsworkslib` <a class="headerlink" href="#helm.consul.hopsworkslib" title="Permanent link">#</a> { #helm.consul.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`consul.nameOverride` <a class="headerlink" href="#helm.consul.nameOverride" title="Permanent link">#</a> { #helm.consul.nameOverride }
:   Type `string`, default `nil`.
    override app chart name

`consul.networkPolicy.enabled` <a class="headerlink" href="#helm.consul.networkPolicy.enabled" title="Permanent link">#</a> { #helm.consul.networkPolicy.enabled }
:   Type `bool`, default `false`.

`consul.nodeSelector` <a class="headerlink" href="#helm.consul.nodeSelector" title="Permanent link">#</a> { #helm.consul.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration used for the autoconfig job and register managed docker registry jobs

`consul.tolerations` <a class="headerlink" href="#helm.consul.tolerations" title="Permanent link">#</a> { #helm.consul.tolerations }
:   Type `list`, default `[]`.

</div>

## manualServiceRegistration { #helm-values-consul-manualserviceregistration }

??? example "Defaults as YAML"

    ```yaml
    consul:
      manualServiceRegistration:
        resources:
          limits:
            cpu: 100m
            memory: 100Mi
          requests:
            cpu: 50m
            memory: 30Mi
        ttlSecondsAfterFinished: null
    ```

<div class="hops-values" markdown>

`consul.manualServiceRegistration.resources.limits.cpu` <a class="headerlink" href="#helm.consul.manualServiceRegistration.resources.limits.cpu" title="Permanent link">#</a> { #helm.consul.manualServiceRegistration.resources.limits.cpu }
:   Type `string`, default `"100m"`.

`consul.manualServiceRegistration.resources.limits.memory` <a class="headerlink" href="#helm.consul.manualServiceRegistration.resources.limits.memory" title="Permanent link">#</a> { #helm.consul.manualServiceRegistration.resources.limits.memory }
:   Type `string`, default `"100Mi"`.

`consul.manualServiceRegistration.resources.requests.cpu` <a class="headerlink" href="#helm.consul.manualServiceRegistration.resources.requests.cpu" title="Permanent link">#</a> { #helm.consul.manualServiceRegistration.resources.requests.cpu }
:   Type `string`, default `"50m"`.

`consul.manualServiceRegistration.resources.requests.memory` <a class="headerlink" href="#helm.consul.manualServiceRegistration.resources.requests.memory" title="Permanent link">#</a> { #helm.consul.manualServiceRegistration.resources.requests.memory }
:   Type `string`, default `"30Mi"`.

`consul.manualServiceRegistration.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.consul.manualServiceRegistration.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.consul.manualServiceRegistration.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    TTL in seconds for manual service registration Jobs. Overrides global default.

</div>

<!-- END GENERATED VALUES -->
