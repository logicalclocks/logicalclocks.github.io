# KServe values { #helm-values-kserve }

Values under `kserve` configure KServe and Knative Serving, which run model deployments.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.2.0-alpha-1791461629` (Hopsworks `5.2.0`)._

Deployed according to the first of these values that is set: [`hopsworks.variables.kube_kserve_installed`](hopsworks.md#helm.hopsworks.variables.kube_kserve_installed), [`global._hopsworks.full_platform`](global.md#helm.global._hopsworks.full_platform).

## General { #helm-values-kserve-general }

??? example "Defaults as YAML"

    ```yaml
    kserve:
      activator:
        minReplicas: 1
        podDisruptionBudget:
          enabled: true
          minAvailable: 1
        serviceAccount:
          annotations: {}
      cainjector:
        serviceAccount:
          annotations: {}
      cleanupOnUninstall:
        enabled: true
        ttlSecondsAfterFinished: null
      hopsworkslib: {}
      istioCRD:
        serviceAccount:
          annotations: {}
      kserve:
        servingruntime:
          vllmomni:
            imageRegistry: ''
            tag: v0.28.0
          vllmopenai:
            imageRegistry: ''
            tag: v0.28.0
      kserveUtilsImage:
        name: hopsworks/kserve-utils
        tag: 0.1.11
      manager:
        serviceAccount:
          annotations: {}
      servingTerminationGracePeriodSeconds: 120
      storageInitializer:
        image: hopsworks/storage-initializer
        tag: 5.2.0-SNAPSHOT
      webhook:
        minReplicas: 1
        podDisruptionBudget:
          enabled: true
          minAvailable: 1
        serviceAccount:
          annotations: {}
    ```

<div class="hops-values" markdown>

`kserve` <a class="headerlink" href="#helm.kserve" title="Permanent link">#</a> { #helm.kserve }
:   Type `object`.
    override kserve values

    ??? note "Default"

        ```yaml
        kserve:
          servingruntime:
            vllmomni:
              imageRegistry: ''
              tag: v0.28.0
            vllmopenai:
              imageRegistry: ''
              tag: v0.28.0
        ```

`kserve.activator.minReplicas` <a class="headerlink" href="#helm.kserve.activator.minReplicas" title="Permanent link">#</a> { #helm.kserve.activator.minReplicas }
:   Type `int`, default `1`.

`kserve.activator.podDisruptionBudget.enabled` <a class="headerlink" href="#helm.kserve.activator.podDisruptionBudget.enabled" title="Permanent link">#</a> { #helm.kserve.activator.podDisruptionBudget.enabled }
:   Type `bool`, default `true`.

`kserve.activator.podDisruptionBudget.minAvailable` <a class="headerlink" href="#helm.kserve.activator.podDisruptionBudget.minAvailable" title="Permanent link">#</a> { #helm.kserve.activator.podDisruptionBudget.minAvailable }
:   Type `int`, default `1`.

`kserve.activator.serviceAccount.annotations` <a class="headerlink" href="#helm.kserve.activator.serviceAccount.annotations" title="Permanent link">#</a> { #helm.kserve.activator.serviceAccount.annotations }
:   Type `object`, default `{}`.
    service account annotations

`kserve.cainjector.serviceAccount.annotations` <a class="headerlink" href="#helm.kserve.cainjector.serviceAccount.annotations" title="Permanent link">#</a> { #helm.kserve.cainjector.serviceAccount.annotations }
:   Type `object`, default `{}`.
    service account annotations

`kserve.cleanupOnUninstall` <a class="headerlink" href="#helm.kserve.cleanupOnUninstall" title="Permanent link">#</a> { #helm.kserve.cleanupOnUninstall }
:   Type `object`, default `{"enabled":true,"ttlSecondsAfterFinished":null}`.
    post-delete cleanup of Istio/KServe leftovers (cert-manager-issued webhook cert Secrets, plus the istiod CA Secret and CA/leader-election ConfigMaps) that are created at runtime and so are never tracked or pruned by Helm/ArgoCD.

`kserve.cleanupOnUninstall.enabled` <a class="headerlink" href="#helm.kserve.cleanupOnUninstall.enabled" title="Permanent link">#</a> { #helm.kserve.cleanupOnUninstall.enabled }
:   Type `bool`, default `true`.
    enable the post-delete Istio/KServe cleanup hook

`kserve.cleanupOnUninstall.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.kserve.cleanupOnUninstall.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.kserve.cleanupOnUninstall.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    ttlSecondsAfterFinished for the cleanup Job; null falls through to the global default

`kserve.hopsworkslib` <a class="headerlink" href="#helm.kserve.hopsworkslib" title="Permanent link">#</a> { #helm.kserve.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`kserve.istioCRD.serviceAccount.annotations` <a class="headerlink" href="#helm.kserve.istioCRD.serviceAccount.annotations" title="Permanent link">#</a> { #helm.kserve.istioCRD.serviceAccount.annotations }
:   Type `object`, default `{}`.
    service account annotations

`kserve.kserveUtilsImage.name` <a class="headerlink" href="#helm.kserve.kserveUtilsImage.name" title="Permanent link">#</a> { #helm.kserve.kserveUtilsImage.name }
:   Type `string`, default `"hopsworks/kserve-utils"`.

`kserve.kserveUtilsImage.tag` <a class="headerlink" href="#helm.kserve.kserveUtilsImage.tag" title="Permanent link">#</a> { #helm.kserve.kserveUtilsImage.tag }
:   Type `string`, default `"0.1.11"`.

`kserve.manager.serviceAccount.annotations` <a class="headerlink" href="#helm.kserve.manager.serviceAccount.annotations" title="Permanent link">#</a> { #helm.kserve.manager.serviceAccount.annotations }
:   Type `object`, default `{}`.
    service account annotations

`kserve.servingTerminationGracePeriodSeconds` <a class="headerlink" href="#helm.kserve.servingTerminationGracePeriodSeconds" title="Permanent link">#</a> { #helm.kserve.servingTerminationGracePeriodSeconds }
:   Type `int`, default `120`.
    Grace period in seconds the model-serving-webhook stamps onto every serving pod, replacing the value Knative derives from the revision timeout. Must cover the in-pod log archive a disk-logging component uploads to the project's Logs dataset as it terminates (roughly fifteen seconds including SDK import and login). A ceiling, not a delay: a pod with nothing to archive exits as soon as its containers do.

`kserve.storageInitializer.image` <a class="headerlink" href="#helm.kserve.storageInitializer.image" title="Permanent link">#</a> { #helm.kserve.storageInitializer.image }
:   Type `string`, default `"hopsworks/storage-initializer"`.

`kserve.storageInitializer.tag` <a class="headerlink" href="#helm.kserve.storageInitializer.tag" title="Permanent link">#</a> { #helm.kserve.storageInitializer.tag }
:   Type `string`, default `"5.2.0-SNAPSHOT"`.

`kserve.webhook.minReplicas` <a class="headerlink" href="#helm.kserve.webhook.minReplicas" title="Permanent link">#</a> { #helm.kserve.webhook.minReplicas }
:   Type `int`, default `1`.

`kserve.webhook.podDisruptionBudget.enabled` <a class="headerlink" href="#helm.kserve.webhook.podDisruptionBudget.enabled" title="Permanent link">#</a> { #helm.kserve.webhook.podDisruptionBudget.enabled }
:   Type `bool`, default `true`.

`kserve.webhook.podDisruptionBudget.minAvailable` <a class="headerlink" href="#helm.kserve.webhook.podDisruptionBudget.minAvailable" title="Permanent link">#</a> { #helm.kserve.webhook.podDisruptionBudget.minAvailable }
:   Type `int`, default `1`.

`kserve.webhook.serviceAccount.annotations` <a class="headerlink" href="#helm.kserve.webhook.serviceAccount.annotations" title="Permanent link">#</a> { #helm.kserve.webhook.serviceAccount.annotations }
:   Type `object`, default `{}`.
    service account annotations

</div>

## cert_manager { #helm-values-kserve-cert_manager }

??? example "Defaults as YAML"

    ```yaml
    kserve:
      cert_manager:
        enabled: true
        jobResources:
          cainjector:
            limits:
              cpu: 200m
          controller:
            limits:
              cpu: 500m
              memory: 2Gi
          webhook:
            limits:
              cpu: 200m
        nodeSelector: {}
        tolerations: []
        topologySpreadConstraint: {}
        version: v1.21.1
    ```

<div class="hops-values" markdown>

`kserve.cert_manager.enabled` <a class="headerlink" href="#helm.kserve.cert_manager.enabled" title="Permanent link">#</a> { #helm.kserve.cert_manager.enabled }
:   Type `bool`, default `true`.

`kserve.cert_manager.jobResources.cainjector` <a class="headerlink" href="#helm.kserve.cert_manager.jobResources.cainjector" title="Permanent link">#</a> { #helm.kserve.cert_manager.jobResources.cainjector }
:   Type `object`, default `{"limits":{"cpu":"200m"}}`.
    cainjector resources configuration

`kserve.cert_manager.jobResources.cainjector.limits` <a class="headerlink" href="#helm.kserve.cert_manager.jobResources.cainjector.limits" title="Permanent link">#</a> { #helm.kserve.cert_manager.jobResources.cainjector.limits }
:   Type `object`, default `{"cpu":"200m"}`.
    cainjector resources limits configuration

`kserve.cert_manager.jobResources.controller` <a class="headerlink" href="#helm.kserve.cert_manager.jobResources.controller" title="Permanent link">#</a> { #helm.kserve.cert_manager.jobResources.controller }
:   Type `object`, default `{"limits":{"cpu":"500m","memory":"2Gi"}}`.
    controller resources configuration

`kserve.cert_manager.jobResources.webhook` <a class="headerlink" href="#helm.kserve.cert_manager.jobResources.webhook" title="Permanent link">#</a> { #helm.kserve.cert_manager.jobResources.webhook }
:   Type `object`, default `{"limits":{"cpu":"200m"}}`.
    webhook resources configuration

`kserve.cert_manager.jobResources.webhook.limits` <a class="headerlink" href="#helm.kserve.cert_manager.jobResources.webhook.limits" title="Permanent link">#</a> { #helm.kserve.cert_manager.jobResources.webhook.limits }
:   Type `object`, default `{"cpu":"200m"}`.
    webhook resources limits configuration

`kserve.cert_manager.nodeSelector` <a class="headerlink" href="#helm.kserve.cert_manager.nodeSelector" title="Permanent link">#</a> { #helm.kserve.cert_manager.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

`kserve.cert_manager.tolerations` <a class="headerlink" href="#helm.kserve.cert_manager.tolerations" title="Permanent link">#</a> { #helm.kserve.cert_manager.tolerations }
:   Type `list`, default `[]`.

`kserve.cert_manager.topologySpreadConstraint` <a class="headerlink" href="#helm.kserve.cert_manager.topologySpreadConstraint" title="Permanent link">#</a> { #helm.kserve.cert_manager.topologySpreadConstraint }
:   Type `object`, default `{}`.
    The default topology spread constraint. If not defined the global topology spread constraint would be used instead.

`kserve.cert_manager.version` <a class="headerlink" href="#helm.kserve.cert_manager.version" title="Permanent link">#</a> { #helm.kserve.cert_manager.version }
:   Type `string`, default `"v1.21.1"`.
    cert-manager version. v1.21 supports Kubernetes 1.33-1.36; kserve-deps.env pins v1.17 (KServe CI), which is EOL and tops out at Kubernetes 1.33.

</div>

## crdUpgradeJob { #helm-values-kserve-crdupgradejob }

??? example "Defaults as YAML"

    ```yaml
    kserve:
      crdUpgradeJob:
        name: kserve-crd-upgrade
        nodeSelector: {}
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
        serviceAccount:
          annotations: {}
        tolerations: []
    ```

<div class="hops-values" markdown>

`kserve.crdUpgradeJob.name` <a class="headerlink" href="#helm.kserve.crdUpgradeJob.name" title="Permanent link">#</a> { #helm.kserve.crdUpgradeJob.name }
:   Type `string`, default `"kserve-crd-upgrade"`.

`kserve.crdUpgradeJob.nodeSelector` <a class="headerlink" href="#helm.kserve.crdUpgradeJob.nodeSelector" title="Permanent link">#</a> { #helm.kserve.crdUpgradeJob.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

`kserve.crdUpgradeJob.resources` <a class="headerlink" href="#helm.kserve.crdUpgradeJob.resources" title="Permanent link">#</a> { #helm.kserve.crdUpgradeJob.resources }
:   Type `object`, default `{"requests":{"cpu":"100m","memory":"128Mi"}}`.
    resources configuration

`kserve.crdUpgradeJob.serviceAccount.annotations` <a class="headerlink" href="#helm.kserve.crdUpgradeJob.serviceAccount.annotations" title="Permanent link">#</a> { #helm.kserve.crdUpgradeJob.serviceAccount.annotations }
:   Type `object`, default `{}`.
    service account annotations

`kserve.crdUpgradeJob.tolerations` <a class="headerlink" href="#helm.kserve.crdUpgradeJob.tolerations" title="Permanent link">#</a> { #helm.kserve.crdUpgradeJob.tolerations }
:   Type `list`, default `[]`.

</div>

## dependencies { #helm-values-kserve-dependencies }

??? example "Defaults as YAML"

    ```yaml
    kserve:
      dependencies:
        hopsworks:
          consulServiceName: glassfish
          consulServiceTag: hopsworks
          port: 8182
        registry:
          consulServiceName: registry
          port: 30443
          registryProtocol: https
    ```

<div class="hops-values" markdown>

`kserve.dependencies.hopsworks.consulServiceName` <a class="headerlink" href="#helm.kserve.dependencies.hopsworks.consulServiceName" title="Permanent link">#</a> { #helm.kserve.dependencies.hopsworks.consulServiceName }
:   Type `string`, default `"glassfish"`.

`kserve.dependencies.hopsworks.consulServiceTag` <a class="headerlink" href="#helm.kserve.dependencies.hopsworks.consulServiceTag" title="Permanent link">#</a> { #helm.kserve.dependencies.hopsworks.consulServiceTag }
:   Type `string`, default `"hopsworks"`.

`kserve.dependencies.hopsworks.port` <a class="headerlink" href="#helm.kserve.dependencies.hopsworks.port" title="Permanent link">#</a> { #helm.kserve.dependencies.hopsworks.port }
:   Type `int`, default `8182`.

`kserve.dependencies.registry.consulServiceName` <a class="headerlink" href="#helm.kserve.dependencies.registry.consulServiceName" title="Permanent link">#</a> { #helm.kserve.dependencies.registry.consulServiceName }
:   Type `string`, default `"registry"`.

`kserve.dependencies.registry.port` <a class="headerlink" href="#helm.kserve.dependencies.registry.port" title="Permanent link">#</a> { #helm.kserve.dependencies.registry.port }
:   Type `int`, default `30443`.

`kserve.dependencies.registry.registryProtocol` <a class="headerlink" href="#helm.kserve.dependencies.registry.registryProtocol" title="Permanent link">#</a> { #helm.kserve.dependencies.registry.registryProtocol }
:   Type `string`, default `"https"`.

</div>

## inferenceLogger { #helm-values-kserve-inferencelogger }

??? example "Defaults as YAML"

    ```yaml
    kserve:
      inferenceLogger:
        capabilities: {}
        digest: ''
        image: hopsworks/inference-logger
        limits:
          assemblyWorkers: 2
          maxBatchRows: 512
          maxBufferBytes: 134217728
          maxDecodedBytes: 33554432
          maxEventBytes: 8388608
          maxInflightEvents: 16
          maxQueuedRows: 1000
          producerWorkers: 2
          shutdownSeconds: 15
        metrics:
          additionalLabels: {}
          enabled: false
          interval: 30s
          port: 9098
        resources:
          limits:
            cpu: '1'
            memory: 1Gi
          requests:
            cpu: '0.1'
            memory: 128Mi
        tag: 5.2.0-SNAPSHOT
    ```

<div class="hops-values" markdown>

`kserve.inferenceLogger.capabilities` <a class="headerlink" href="#helm.kserve.inferenceLogger.capabilities" title="Permanent link">#</a> { #helm.kserve.inferenceLogger.capabilities }
:   Type `object`, default `{}`.
    Map of verified full image references with digests to protocol tokens. Empty keeps legacy transport.

`kserve.inferenceLogger.digest` <a class="headerlink" href="#helm.kserve.inferenceLogger.digest" title="Permanent link">#</a> { #helm.kserve.inferenceLogger.digest }
:   Type `string`, default `""`.
    Immutable sha256 digest. When set, takes precedence over tag.

`kserve.inferenceLogger.image` <a class="headerlink" href="#helm.kserve.inferenceLogger.image" title="Permanent link">#</a> { #helm.kserve.inferenceLogger.image }
:   Type `string`, default `"hopsworks/inference-logger"`.

`kserve.inferenceLogger.limits.assemblyWorkers` <a class="headerlink" href="#helm.kserve.inferenceLogger.limits.assemblyWorkers" title="Permanent link">#</a> { #helm.kserve.inferenceLogger.limits.assemblyWorkers }
:   Type `int`, default `2`.

`kserve.inferenceLogger.limits.maxBatchRows` <a class="headerlink" href="#helm.kserve.inferenceLogger.limits.maxBatchRows" title="Permanent link">#</a> { #helm.kserve.inferenceLogger.limits.maxBatchRows }
:   Type `int`, default `512`.

`kserve.inferenceLogger.limits.maxBufferBytes` <a class="headerlink" href="#helm.kserve.inferenceLogger.limits.maxBufferBytes" title="Permanent link">#</a> { #helm.kserve.inferenceLogger.limits.maxBufferBytes }
:   Type `int`, default `134217728`.

`kserve.inferenceLogger.limits.maxDecodedBytes` <a class="headerlink" href="#helm.kserve.inferenceLogger.limits.maxDecodedBytes" title="Permanent link">#</a> { #helm.kserve.inferenceLogger.limits.maxDecodedBytes }
:   Type `int`, default `33554432`.

`kserve.inferenceLogger.limits.maxEventBytes` <a class="headerlink" href="#helm.kserve.inferenceLogger.limits.maxEventBytes" title="Permanent link">#</a> { #helm.kserve.inferenceLogger.limits.maxEventBytes }
:   Type `int`, default `8388608`.

`kserve.inferenceLogger.limits.maxInflightEvents` <a class="headerlink" href="#helm.kserve.inferenceLogger.limits.maxInflightEvents" title="Permanent link">#</a> { #helm.kserve.inferenceLogger.limits.maxInflightEvents }
:   Type `int`, default `16`.

`kserve.inferenceLogger.limits.maxQueuedRows` <a class="headerlink" href="#helm.kserve.inferenceLogger.limits.maxQueuedRows" title="Permanent link">#</a> { #helm.kserve.inferenceLogger.limits.maxQueuedRows }
:   Type `int`, default `1000`.

`kserve.inferenceLogger.limits.producerWorkers` <a class="headerlink" href="#helm.kserve.inferenceLogger.limits.producerWorkers" title="Permanent link">#</a> { #helm.kserve.inferenceLogger.limits.producerWorkers }
:   Type `int`, default `2`.

`kserve.inferenceLogger.limits.shutdownSeconds` <a class="headerlink" href="#helm.kserve.inferenceLogger.limits.shutdownSeconds" title="Permanent link">#</a> { #helm.kserve.inferenceLogger.limits.shutdownSeconds }
:   Type `int`, default `15`.

`kserve.inferenceLogger.metrics.additionalLabels` <a class="headerlink" href="#helm.kserve.inferenceLogger.metrics.additionalLabels" title="Permanent link">#</a> { #helm.kserve.inferenceLogger.metrics.additionalLabels }
:   Type `object`, default `{}`.

`kserve.inferenceLogger.metrics.enabled` <a class="headerlink" href="#helm.kserve.inferenceLogger.metrics.enabled" title="Permanent link">#</a> { #helm.kserve.inferenceLogger.metrics.enabled }
:   Type `bool`, default `false`.
    Create a PodMonitor when its CRD is available. KServe's existing scrape configuration is preserved.

`kserve.inferenceLogger.metrics.interval` <a class="headerlink" href="#helm.kserve.inferenceLogger.metrics.interval" title="Permanent link">#</a> { #helm.kserve.inferenceLogger.metrics.interval }
:   Type `string`, default `"30s"`.

`kserve.inferenceLogger.metrics.port` <a class="headerlink" href="#helm.kserve.inferenceLogger.metrics.port" title="Permanent link">#</a> { #helm.kserve.inferenceLogger.metrics.port }
:   Type `int`, default `9098`.

`kserve.inferenceLogger.resources.limits.cpu` <a class="headerlink" href="#helm.kserve.inferenceLogger.resources.limits.cpu" title="Permanent link">#</a> { #helm.kserve.inferenceLogger.resources.limits.cpu }
:   Type `string`, default `"1"`.

`kserve.inferenceLogger.resources.limits.memory` <a class="headerlink" href="#helm.kserve.inferenceLogger.resources.limits.memory" title="Permanent link">#</a> { #helm.kserve.inferenceLogger.resources.limits.memory }
:   Type `string`, default `"1Gi"`.

`kserve.inferenceLogger.resources.requests.cpu` <a class="headerlink" href="#helm.kserve.inferenceLogger.resources.requests.cpu" title="Permanent link">#</a> { #helm.kserve.inferenceLogger.resources.requests.cpu }
:   Type `string`, default `"0.1"`.

`kserve.inferenceLogger.resources.requests.memory` <a class="headerlink" href="#helm.kserve.inferenceLogger.resources.requests.memory" title="Permanent link">#</a> { #helm.kserve.inferenceLogger.resources.requests.memory }
:   Type `string`, default `"128Mi"`.

`kserve.inferenceLogger.tag` <a class="headerlink" href="#helm.kserve.inferenceLogger.tag" title="Permanent link">#</a> { #helm.kserve.inferenceLogger.tag }
:   Type `string`, default `"5.2.0-SNAPSHOT"`.

</div>

## istio { #helm-values-kserve-istio }

??? example "Defaults as YAML"

    ```yaml
    kserve:
      istio:
        crdClassInstallServiceAccount:
          apiGroups:
          - networking.istio.io
          - security.istio.io
          - rbac.istio.io
          - authentication.istio.io
          name: istio-crd-class-install-sa
          resources:
          - '*'
          verbs:
          - get
          - list
          - watch
          - create
          - update
          - patch
          - delete
        envoyFilter:
          corsAllowedOrigins:
          - https://hopsworks.ai.local
          jobName: envoyfilterjob
          resources:
            limits:
              cpu: 200m
        gateways:
          clusterLocal:
            podDisruptionBudget:
              enabled: true
              minAvailable: 1
            replicaCount: 1
          http10: false
          ingress:
            http10: false
            http2Port: 32080
            httpsPort: 32443
            name: istio-ingressgateway
            podDisruptionBudget:
              enabled: true
              minAvailable: 1
            replicaCount: 1
            statusPort: 32021
          jobName: gateway-operator-job
          operatorConfigFileName: istiooperator.yaml
          operatorConfigMountPath: /tmp
        ingressClass:
          enabled: true
          name: istio
        istioctl:
          currentVersion: 1.29.7
          installJobName: istioctl-install-job
          jobRetries: 4
          name: istioctl
          readinessTimeout: 15m0s
          resources:
            requests:
              cpu: 200m
              memory: 256Mi
          serviceAccount:
            annotations: {}
          targetVersion: 1.29.7
          uninstallJobName: istioctl-uninstall-job
        nodeSelector: {}
        pilot:
          podDisruptionBudget:
            enabled: true
            minAvailable: 1
          replicaCount: 1
        tolerations: []
    ```

<div class="hops-values" markdown>

`kserve.istio.crdClassInstallServiceAccount.apiGroups[0]` <a class="headerlink" href="#helm.kserve.istio.crdClassInstallServiceAccount.apiGroups.0" title="Permanent link">#</a> { #helm.kserve.istio.crdClassInstallServiceAccount.apiGroups.0 }
:   Type `string`, default `"networking.istio.io"`.

`kserve.istio.crdClassInstallServiceAccount.apiGroups[1]` <a class="headerlink" href="#helm.kserve.istio.crdClassInstallServiceAccount.apiGroups.1" title="Permanent link">#</a> { #helm.kserve.istio.crdClassInstallServiceAccount.apiGroups.1 }
:   Type `string`, default `"security.istio.io"`.

`kserve.istio.crdClassInstallServiceAccount.apiGroups[2]` <a class="headerlink" href="#helm.kserve.istio.crdClassInstallServiceAccount.apiGroups.2" title="Permanent link">#</a> { #helm.kserve.istio.crdClassInstallServiceAccount.apiGroups.2 }
:   Type `string`, default `"rbac.istio.io"`.

`kserve.istio.crdClassInstallServiceAccount.apiGroups[3]` <a class="headerlink" href="#helm.kserve.istio.crdClassInstallServiceAccount.apiGroups.3" title="Permanent link">#</a> { #helm.kserve.istio.crdClassInstallServiceAccount.apiGroups.3 }
:   Type `string`, default `"authentication.istio.io"`.

`kserve.istio.crdClassInstallServiceAccount.name` <a class="headerlink" href="#helm.kserve.istio.crdClassInstallServiceAccount.name" title="Permanent link">#</a> { #helm.kserve.istio.crdClassInstallServiceAccount.name }
:   Type `string`, default `"istio-crd-class-install-sa"`.

`kserve.istio.crdClassInstallServiceAccount.resources[0]` <a class="headerlink" href="#helm.kserve.istio.crdClassInstallServiceAccount.resources.0" title="Permanent link">#</a> { #helm.kserve.istio.crdClassInstallServiceAccount.resources.0 }
:   Type `string`, default `"*"`.

`kserve.istio.crdClassInstallServiceAccount.verbs[0]` <a class="headerlink" href="#helm.kserve.istio.crdClassInstallServiceAccount.verbs.0" title="Permanent link">#</a> { #helm.kserve.istio.crdClassInstallServiceAccount.verbs.0 }
:   Type `string`, default `"get"`.

`kserve.istio.crdClassInstallServiceAccount.verbs[1]` <a class="headerlink" href="#helm.kserve.istio.crdClassInstallServiceAccount.verbs.1" title="Permanent link">#</a> { #helm.kserve.istio.crdClassInstallServiceAccount.verbs.1 }
:   Type `string`, default `"list"`.

`kserve.istio.crdClassInstallServiceAccount.verbs[2]` <a class="headerlink" href="#helm.kserve.istio.crdClassInstallServiceAccount.verbs.2" title="Permanent link">#</a> { #helm.kserve.istio.crdClassInstallServiceAccount.verbs.2 }
:   Type `string`, default `"watch"`.

`kserve.istio.crdClassInstallServiceAccount.verbs[3]` <a class="headerlink" href="#helm.kserve.istio.crdClassInstallServiceAccount.verbs.3" title="Permanent link">#</a> { #helm.kserve.istio.crdClassInstallServiceAccount.verbs.3 }
:   Type `string`, default `"create"`.

`kserve.istio.crdClassInstallServiceAccount.verbs[4]` <a class="headerlink" href="#helm.kserve.istio.crdClassInstallServiceAccount.verbs.4" title="Permanent link">#</a> { #helm.kserve.istio.crdClassInstallServiceAccount.verbs.4 }
:   Type `string`, default `"update"`.

`kserve.istio.crdClassInstallServiceAccount.verbs[5]` <a class="headerlink" href="#helm.kserve.istio.crdClassInstallServiceAccount.verbs.5" title="Permanent link">#</a> { #helm.kserve.istio.crdClassInstallServiceAccount.verbs.5 }
:   Type `string`, default `"patch"`.

`kserve.istio.crdClassInstallServiceAccount.verbs[6]` <a class="headerlink" href="#helm.kserve.istio.crdClassInstallServiceAccount.verbs.6" title="Permanent link">#</a> { #helm.kserve.istio.crdClassInstallServiceAccount.verbs.6 }
:   Type `string`, default `"delete"`.

`kserve.istio.envoyFilter.corsAllowedOrigins` <a class="headerlink" href="#helm.kserve.istio.envoyFilter.corsAllowedOrigins" title="Permanent link">#</a> { #helm.kserve.istio.envoyFilter.corsAllowedOrigins }
:   Type `list`, default `["https://hopsworks.ai.local"]`.
    List of allowed origins for CORS requests. Defaults to the hopsworks ingress host. Update this when changing hopsworks.ingress.host. An empty list disables adding CORS headers (no CORS configuration will be applied). CORS responses for the listed origins are configured to allow credentials by default. Use \["*"\] to allow all origins (not recommended with credentials).

`kserve.istio.envoyFilter.jobName` <a class="headerlink" href="#helm.kserve.istio.envoyFilter.jobName" title="Permanent link">#</a> { #helm.kserve.istio.envoyFilter.jobName }
:   Type `string`, default `"envoyfilterjob"`.

`kserve.istio.envoyFilter.resources` <a class="headerlink" href="#helm.kserve.istio.envoyFilter.resources" title="Permanent link">#</a> { #helm.kserve.istio.envoyFilter.resources }
:   Type `object`, default `{"limits":{"cpu":"200m"}}`.
    resources configuration

`kserve.istio.envoyFilter.resources.limits` <a class="headerlink" href="#helm.kserve.istio.envoyFilter.resources.limits" title="Permanent link">#</a> { #helm.kserve.istio.envoyFilter.resources.limits }
:   Type `object`, default `{"cpu":"200m"}`.
    resources limits configuration

`kserve.istio.gateways.clusterLocal.podDisruptionBudget.enabled` <a class="headerlink" href="#helm.kserve.istio.gateways.clusterLocal.podDisruptionBudget.enabled" title="Permanent link">#</a> { #helm.kserve.istio.gateways.clusterLocal.podDisruptionBudget.enabled }
:   Type `bool`, default `true`.

`kserve.istio.gateways.clusterLocal.podDisruptionBudget.minAvailable` <a class="headerlink" href="#helm.kserve.istio.gateways.clusterLocal.podDisruptionBudget.minAvailable" title="Permanent link">#</a> { #helm.kserve.istio.gateways.clusterLocal.podDisruptionBudget.minAvailable }
:   Type `int`, default `1`.

`kserve.istio.gateways.clusterLocal.replicaCount` <a class="headerlink" href="#helm.kserve.istio.gateways.clusterLocal.replicaCount" title="Permanent link">#</a> { #helm.kserve.istio.gateways.clusterLocal.replicaCount }
:   Type `int`, default `1`.

`kserve.istio.gateways.ingress.http10` <a class="headerlink" href="#helm.kserve.istio.gateways.ingress.http10" title="Permanent link">#</a> { #helm.kserve.istio.gateways.ingress.http10 }
:   Type `bool`, default `false`.
    Allow HTTP/1.0 requests through the ingress gateway

`kserve.istio.gateways.ingress.http2Port` <a class="headerlink" href="#helm.kserve.istio.gateways.ingress.http2Port" title="Permanent link">#</a> { #helm.kserve.istio.gateways.ingress.http2Port }
:   Type `int`, default `32080`.

`kserve.istio.gateways.ingress.httpsPort` <a class="headerlink" href="#helm.kserve.istio.gateways.ingress.httpsPort" title="Permanent link">#</a> { #helm.kserve.istio.gateways.ingress.httpsPort }
:   Type `int`, default `32443`.

`kserve.istio.gateways.ingress.name` <a class="headerlink" href="#helm.kserve.istio.gateways.ingress.name" title="Permanent link">#</a> { #helm.kserve.istio.gateways.ingress.name }
:   Type `string`, default `"istio-ingressgateway"`.

`kserve.istio.gateways.ingress.podDisruptionBudget.enabled` <a class="headerlink" href="#helm.kserve.istio.gateways.ingress.podDisruptionBudget.enabled" title="Permanent link">#</a> { #helm.kserve.istio.gateways.ingress.podDisruptionBudget.enabled }
:   Type `bool`, default `true`.

`kserve.istio.gateways.ingress.podDisruptionBudget.minAvailable` <a class="headerlink" href="#helm.kserve.istio.gateways.ingress.podDisruptionBudget.minAvailable" title="Permanent link">#</a> { #helm.kserve.istio.gateways.ingress.podDisruptionBudget.minAvailable }
:   Type `int`, default `1`.

`kserve.istio.gateways.ingress.replicaCount` <a class="headerlink" href="#helm.kserve.istio.gateways.ingress.replicaCount" title="Permanent link">#</a> { #helm.kserve.istio.gateways.ingress.replicaCount }
:   Type `int`, default `1`.

`kserve.istio.gateways.ingress.statusPort` <a class="headerlink" href="#helm.kserve.istio.gateways.ingress.statusPort" title="Permanent link">#</a> { #helm.kserve.istio.gateways.ingress.statusPort }
:   Type `int`, default `32021`.

`kserve.istio.gateways.jobName` <a class="headerlink" href="#helm.kserve.istio.gateways.jobName" title="Permanent link">#</a> { #helm.kserve.istio.gateways.jobName }
:   Type `string`, default `"gateway-operator-job"`.

`kserve.istio.gateways.operatorConfigFileName` <a class="headerlink" href="#helm.kserve.istio.gateways.operatorConfigFileName" title="Permanent link">#</a> { #helm.kserve.istio.gateways.operatorConfigFileName }
:   Type `string`, default `"istiooperator.yaml"`.

`kserve.istio.gateways.operatorConfigMountPath` <a class="headerlink" href="#helm.kserve.istio.gateways.operatorConfigMountPath" title="Permanent link">#</a> { #helm.kserve.istio.gateways.operatorConfigMountPath }
:   Type `string`, default `"/tmp"`.

`kserve.istio.ingressClass.enabled` <a class="headerlink" href="#helm.kserve.istio.ingressClass.enabled" title="Permanent link">#</a> { #helm.kserve.istio.ingressClass.enabled }
:   Type `bool`, default `true`.
    Whether to create a cluster-scoped `IngressClass` named after `name` below, for KServe Standard-mode InferenceServices (`serving.kserve.io/deploymentMode: Standard`). KServe's controller writes this class name into the `spec.ingressClassName` of the `networking.k8s.io/v1` Ingress objects it creates for those InferenceServices.

`kserve.istio.ingressClass.name` <a class="headerlink" href="#helm.kserve.istio.ingressClass.name" title="Permanent link">#</a> { #helm.kserve.istio.ingressClass.name }
:   Type `string`, default `"istio"`.
    Name of the IngressClass. Must match `kserve.controller.gateway.ingressGateway.className`, which is what KServe reads from the `inferenceservice-config` ConfigMap to populate `spec.ingressClassName`.

`kserve.istio.istioctl.currentVersion` <a class="headerlink" href="#helm.kserve.istio.istioctl.currentVersion" title="Permanent link">#</a> { #helm.kserve.istio.istioctl.currentVersion }
:   Type `string`, default `"1.29.7"`.

`kserve.istio.istioctl.installJobName` <a class="headerlink" href="#helm.kserve.istio.istioctl.installJobName" title="Permanent link">#</a> { #helm.kserve.istio.istioctl.installJobName }
:   Type `string`, default `"istioctl-install-job"`.

`kserve.istio.istioctl.jobRetries` <a class="headerlink" href="#helm.kserve.istio.istioctl.jobRetries" title="Permanent link">#</a> { #helm.kserve.istio.istioctl.jobRetries }
:   Type `int`, default `4`.

`kserve.istio.istioctl.name` <a class="headerlink" href="#helm.kserve.istio.istioctl.name" title="Permanent link">#</a> { #helm.kserve.istio.istioctl.name }
:   Type `string`, default `"istioctl"`.

`kserve.istio.istioctl.readinessTimeout` <a class="headerlink" href="#helm.kserve.istio.istioctl.readinessTimeout" title="Permanent link">#</a> { #helm.kserve.istio.istioctl.readinessTimeout }
:   Type `string`, default `"15m0s"`.

`kserve.istio.istioctl.resources` <a class="headerlink" href="#helm.kserve.istio.istioctl.resources" title="Permanent link">#</a> { #helm.kserve.istio.istioctl.resources }
:   Type `object`, default `{"requests":{"cpu":"200m","memory":"256Mi"}}`.
    resources configuration

`kserve.istio.istioctl.serviceAccount.annotations` <a class="headerlink" href="#helm.kserve.istio.istioctl.serviceAccount.annotations" title="Permanent link">#</a> { #helm.kserve.istio.istioctl.serviceAccount.annotations }
:   Type `object`, default `{}`.
    service account annotations

`kserve.istio.istioctl.targetVersion` <a class="headerlink" href="#helm.kserve.istio.istioctl.targetVersion" title="Permanent link">#</a> { #helm.kserve.istio.istioctl.targetVersion }
:   Type `string`, default `"1.29.7"`.

`kserve.istio.istioctl.uninstallJobName` <a class="headerlink" href="#helm.kserve.istio.istioctl.uninstallJobName" title="Permanent link">#</a> { #helm.kserve.istio.istioctl.uninstallJobName }
:   Type `string`, default `"istioctl-uninstall-job"`.

`kserve.istio.nodeSelector` <a class="headerlink" href="#helm.kserve.istio.nodeSelector" title="Permanent link">#</a> { #helm.kserve.istio.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

`kserve.istio.pilot.podDisruptionBudget.enabled` <a class="headerlink" href="#helm.kserve.istio.pilot.podDisruptionBudget.enabled" title="Permanent link">#</a> { #helm.kserve.istio.pilot.podDisruptionBudget.enabled }
:   Type `bool`, default `true`.

`kserve.istio.pilot.podDisruptionBudget.minAvailable` <a class="headerlink" href="#helm.kserve.istio.pilot.podDisruptionBudget.minAvailable" title="Permanent link">#</a> { #helm.kserve.istio.pilot.podDisruptionBudget.minAvailable }
:   Type `int`, default `1`.

`kserve.istio.pilot.replicaCount` <a class="headerlink" href="#helm.kserve.istio.pilot.replicaCount" title="Permanent link">#</a> { #helm.kserve.istio.pilot.replicaCount }
:   Type `int`, default `1`.

`kserve.istio.tolerations` <a class="headerlink" href="#helm.kserve.istio.tolerations" title="Permanent link">#</a> { #helm.kserve.istio.tolerations }
:   Type `list`, default `[]`.

`kserve.istio.gateways.http10` <span class="hops-values-deprecated">Deprecated</span> <a class="headerlink" href="#helm.kserve.istio.gateways.http10" title="Permanent link">#</a> { #helm.kserve.istio.gateways.http10 }
:   Type `bool`, default `false`.
    Deprecated, use gateways.ingress.http10 instead. Still honoured: HTTP/1.0 is enabled when either this or gateways.ingress.http10 is true.

</div>

## knative { #helm-values-kserve-knative }

??? example "Defaults as YAML"

    ```yaml
    kserve:
      knative:
        autoscaler:
          scaleToZeroGracePeriod: 30s
          scaleToZeroPodRetentionPeriod: 0s
        configFeatures:
          affinity: enabled
          emptyDir: enabled
          initContainers: enabled
          nodeSelectors: enabled
          priorityClassName: enabled
          securePodDefaults: disabled
          securityContext: enabled
          tolerations: enabled
          volumesCsi: enabled
          volumesMountPropagation: enabled
        deployment:
          progressDeadline: 1800s
        domainName: hopsworks.ai
        gateways:
          jobName: knative-gateways-job
          resources:
            limits:
              cpu: 400m
        http:
          enabled: true
        https:
          credentialsName: ''
          enabled: false
        imageRegistry: ''
        initialDelaySeconds: 180
        netIstioController:
          resources:
            limits:
              cpu: 300m
              memory: 400Mi
            requests:
              cpu: 30m
              memory: 40Mi
        nodeSelector: {}
        peerAuthenticationsJob:
          name: knative-serving-peer-authentications-job
          resources: {}
        queueSidecarImage:
          name: kserve/qpext
          tag: v0.21.0
        registryCertMount:
          certFileName: ca.crt
          external: false
          mountDir: /etc/registry_certs
          volumeName: registry-certs
        serviceAccount:
          annotations: {}
        serviceAnnotations:
          prometheus.io/path: /metrics
          prometheus.io/port: 9090
          prometheus.io/scheme: http
          prometheus.io/scrape: 'true'
        tolerations: []
        topologySpreadConstraint: {}
        validatingWebhookDeleteJobName: knative-serving-validating-webhook-delete-job
        validatingWebhookName: validation.webhook.serving.knative.dev
        version: v1.23.0
    ```

<div class="hops-values" markdown>

`kserve.knative.autoscaler.scaleToZeroGracePeriod` <a class="headerlink" href="#helm.kserve.knative.autoscaler.scaleToZeroGracePeriod" title="Permanent link">#</a> { #helm.kserve.knative.autoscaler.scaleToZeroGracePeriod }
:   Type `string`, default `"30s"`.

`kserve.knative.autoscaler.scaleToZeroPodRetentionPeriod` <a class="headerlink" href="#helm.kserve.knative.autoscaler.scaleToZeroPodRetentionPeriod" title="Permanent link">#</a> { #helm.kserve.knative.autoscaler.scaleToZeroPodRetentionPeriod }
:   Type `string`, default `"0s"`.

`kserve.knative.configFeatures.affinity` <a class="headerlink" href="#helm.kserve.knative.configFeatures.affinity" title="Permanent link">#</a> { #helm.kserve.knative.configFeatures.affinity }
:   Type `string`, default `"enabled"`.

`kserve.knative.configFeatures.emptyDir` <a class="headerlink" href="#helm.kserve.knative.configFeatures.emptyDir" title="Permanent link">#</a> { #helm.kserve.knative.configFeatures.emptyDir }
:   Type `string`, default `"enabled"`.

`kserve.knative.configFeatures.initContainers` <a class="headerlink" href="#helm.kserve.knative.configFeatures.initContainers" title="Permanent link">#</a> { #helm.kserve.knative.configFeatures.initContainers }
:   Type `string`, default `"enabled"`.

`kserve.knative.configFeatures.nodeSelectors` <a class="headerlink" href="#helm.kserve.knative.configFeatures.nodeSelectors" title="Permanent link">#</a> { #helm.kserve.knative.configFeatures.nodeSelectors }
:   Type `string`, default `"enabled"`.

`kserve.knative.configFeatures.priorityClassName` <a class="headerlink" href="#helm.kserve.knative.configFeatures.priorityClassName" title="Permanent link">#</a> { #helm.kserve.knative.configFeatures.priorityClassName }
:   Type `string`, default `"enabled"`.

`kserve.knative.configFeatures.securePodDefaults` <a class="headerlink" href="#helm.kserve.knative.configFeatures.securePodDefaults" title="Permanent link">#</a> { #helm.kserve.knative.configFeatures.securePodDefaults }
:   Type `string`, default `"disabled"`.
    Knative "secure-pod-defaults" feature flag. Keep "disabled" so the HopsFS FUSE sidecar (runs as root/privileged) keeps working once Knative flips its built-in default from "disabled" to "AllowRootBounded" (planned ~1.22). Possible values are "disabled", "AllowRootBounded" or "enabled".

`kserve.knative.configFeatures.securityContext` <a class="headerlink" href="#helm.kserve.knative.configFeatures.securityContext" title="Permanent link">#</a> { #helm.kserve.knative.configFeatures.securityContext }
:   Type `string`, default `"enabled"`.

`kserve.knative.configFeatures.tolerations` <a class="headerlink" href="#helm.kserve.knative.configFeatures.tolerations" title="Permanent link">#</a> { #helm.kserve.knative.configFeatures.tolerations }
:   Type `string`, default `"enabled"`.

`kserve.knative.configFeatures.volumesCsi` <a class="headerlink" href="#helm.kserve.knative.configFeatures.volumesCsi" title="Permanent link">#</a> { #helm.kserve.knative.configFeatures.volumesCsi }
:   Type `string`, default `"enabled"`.
    Knative "kubernetes.podspec-volumes-csi" feature gate, "disabled" by default in Knative. With the HopsFS CSI driver on (csi_driver_enabled), the backend gives Knative-mode agent and Python deployments the same inline csi: HopsFS volume plus unprivileged hopsfs-fuse sidecar that Jupyter, jobs, terminals and RawDeployment serving use, instead of the legacy root and privileged hopsfsmount container (HWORKS-3312). Knative's Revision validation only lets a csi: volume source through when this gate is enabled; with it disabled those deployments are rejected at admission. Possible values are "disabled" or "enabled".

`kserve.knative.configFeatures.volumesMountPropagation` <a class="headerlink" href="#helm.kserve.knative.configFeatures.volumesMountPropagation" title="Permanent link">#</a> { #helm.kserve.knative.configFeatures.volumesMountPropagation }
:   Type `string`, default `"enabled"`.
    Knative "kubernetes.podspec-volumes-mount-propagation" feature gate. The gate does not exist in Knative 1.13 (there was nothing to set) and defaults to "disabled" in 1.21. No Hopsworks serving path depends on it: the backend omits mountPropagation from InferenceService containers and the model-serving-webhook injects HostToContainer onto the pod, after Knative admission. It is enabled purely as headroom, so that an InferenceService carrying a permitted mountPropagation is not rejected. It does not rescue a spec written by a pre-upgrade backend: those set Bidirectional on the HopsFS mount plus privileged on the sidecar, and Knative rejects both however this gate is set (it accepts only None and HostToContainer). Possible values are "disabled" or "enabled".

`kserve.knative.deployment.progressDeadline` <a class="headerlink" href="#helm.kserve.knative.deployment.progressDeadline" title="Permanent link">#</a> { #helm.kserve.knative.deployment.progressDeadline }
:   Type `string`, default `"1800s"`.

`kserve.knative.domainName` <a class="headerlink" href="#helm.kserve.knative.domainName" title="Permanent link">#</a> { #helm.kserve.knative.domainName }
:   Type `string`, default `"hopsworks.ai"`.

`kserve.knative.gateways.jobName` <a class="headerlink" href="#helm.kserve.knative.gateways.jobName" title="Permanent link">#</a> { #helm.kserve.knative.gateways.jobName }
:   Type `string`, default `"knative-gateways-job"`.

`kserve.knative.gateways.resources` <a class="headerlink" href="#helm.kserve.knative.gateways.resources" title="Permanent link">#</a> { #helm.kserve.knative.gateways.resources }
:   Type `object`, default `{"limits":{"cpu":"400m"}}`.
    resources configuration

`kserve.knative.gateways.resources.limits` <a class="headerlink" href="#helm.kserve.knative.gateways.resources.limits" title="Permanent link">#</a> { #helm.kserve.knative.gateways.resources.limits }
:   Type `object`, default `{"cpu":"400m"}`.
    resources limits configuration

`kserve.knative.http.enabled` <a class="headerlink" href="#helm.kserve.knative.http.enabled" title="Permanent link">#</a> { #helm.kserve.knative.http.enabled }
:   Type `bool`, default `true`.

`kserve.knative.https.credentialsName` <a class="headerlink" href="#helm.kserve.knative.https.credentialsName" title="Permanent link">#</a> { #helm.kserve.knative.https.credentialsName }
:   Type `string`, default `""`.

`kserve.knative.https.enabled` <a class="headerlink" href="#helm.kserve.knative.https.enabled" title="Permanent link">#</a> { #helm.kserve.knative.https.enabled }
:   Type `bool`, default `false`.

`kserve.knative.imageRegistry` <a class="headerlink" href="#helm.kserve.knative.imageRegistry" title="Permanent link">#</a> { #helm.kserve.knative.imageRegistry }
:   Type `string`, default `""`.
    Registry prefix for the seven upstream Knative images (serving controller, activator, autoscaler, webhook, queue; net-istio controller, webhook), which the chart references as <registry>/gcr.io/knative-releases/knative.dev/<component>:<version>. Empty means global._hopsworks.imageRegistry. Set it to pull a staged Knative build from another path without moving every other image, the same way servingruntime.*.imageRegistry does.

`kserve.knative.initialDelaySeconds` <a class="headerlink" href="#helm.kserve.knative.initialDelaySeconds" title="Permanent link">#</a> { #helm.kserve.knative.initialDelaySeconds }
:   Type `int`, default `180`.

`kserve.knative.netIstioController.resources.limits.cpu` <a class="headerlink" href="#helm.kserve.knative.netIstioController.resources.limits.cpu" title="Permanent link">#</a> { #helm.kserve.knative.netIstioController.resources.limits.cpu }
:   Type `string`, default `"300m"`.

`kserve.knative.netIstioController.resources.limits.memory` <a class="headerlink" href="#helm.kserve.knative.netIstioController.resources.limits.memory" title="Permanent link">#</a> { #helm.kserve.knative.netIstioController.resources.limits.memory }
:   Type `string`, default `"400Mi"`.

`kserve.knative.netIstioController.resources.requests.cpu` <a class="headerlink" href="#helm.kserve.knative.netIstioController.resources.requests.cpu" title="Permanent link">#</a> { #helm.kserve.knative.netIstioController.resources.requests.cpu }
:   Type `string`, default `"30m"`.

`kserve.knative.netIstioController.resources.requests.memory` <a class="headerlink" href="#helm.kserve.knative.netIstioController.resources.requests.memory" title="Permanent link">#</a> { #helm.kserve.knative.netIstioController.resources.requests.memory }
:   Type `string`, default `"40Mi"`.

`kserve.knative.nodeSelector` <a class="headerlink" href="#helm.kserve.knative.nodeSelector" title="Permanent link">#</a> { #helm.kserve.knative.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

`kserve.knative.peerAuthenticationsJob.name` <a class="headerlink" href="#helm.kserve.knative.peerAuthenticationsJob.name" title="Permanent link">#</a> { #helm.kserve.knative.peerAuthenticationsJob.name }
:   Type `string`, default `"knative-serving-peer-authentications-job"`.

`kserve.knative.peerAuthenticationsJob.resources` <a class="headerlink" href="#helm.kserve.knative.peerAuthenticationsJob.resources" title="Permanent link">#</a> { #helm.kserve.knative.peerAuthenticationsJob.resources }
:   Type `object`, default `{}`.
    resources configuration

`kserve.knative.queueSidecarImage.name` <a class="headerlink" href="#helm.kserve.knative.queueSidecarImage.name" title="Permanent link">#</a> { #helm.kserve.knative.queueSidecarImage.name }
:   Type `string`, default `"kserve/qpext"`.

`kserve.knative.queueSidecarImage.tag` <a class="headerlink" href="#helm.kserve.knative.queueSidecarImage.tag" title="Permanent link">#</a> { #helm.kserve.knative.queueSidecarImage.tag }
:   Type `string`, default `"v0.21.0"`.

`kserve.knative.registryCertMount.certFileName` <a class="headerlink" href="#helm.kserve.knative.registryCertMount.certFileName" title="Permanent link">#</a> { #helm.kserve.knative.registryCertMount.certFileName }
:   Type `string`, default `"ca.crt"`.

`kserve.knative.registryCertMount.external` <a class="headerlink" href="#helm.kserve.knative.registryCertMount.external" title="Permanent link">#</a> { #helm.kserve.knative.registryCertMount.external }
:   Type `bool`, default `false`.

`kserve.knative.registryCertMount.mountDir` <a class="headerlink" href="#helm.kserve.knative.registryCertMount.mountDir" title="Permanent link">#</a> { #helm.kserve.knative.registryCertMount.mountDir }
:   Type `string`, default `"/etc/registry_certs"`.

`kserve.knative.registryCertMount.volumeName` <a class="headerlink" href="#helm.kserve.knative.registryCertMount.volumeName" title="Permanent link">#</a> { #helm.kserve.knative.registryCertMount.volumeName }
:   Type `string`, default `"registry-certs"`.

`kserve.knative.serviceAccount.annotations` <a class="headerlink" href="#helm.kserve.knative.serviceAccount.annotations" title="Permanent link">#</a> { #helm.kserve.knative.serviceAccount.annotations }
:   Type `object`, default `{}`.
    service account annotations

`kserve.knative.serviceAnnotations."prometheus.io/path"` <a class="headerlink" href="#helm.kserve.knative.serviceAnnotations.prometheus.io-path" title="Permanent link">#</a> { #helm.kserve.knative.serviceAnnotations.prometheus.io-path }
:   Type `string`, default `"/metrics"`.

`kserve.knative.serviceAnnotations."prometheus.io/port"` <a class="headerlink" href="#helm.kserve.knative.serviceAnnotations.prometheus.io-port" title="Permanent link">#</a> { #helm.kserve.knative.serviceAnnotations.prometheus.io-port }
:   Type `int`, default `9090`.

`kserve.knative.serviceAnnotations."prometheus.io/scheme"` <a class="headerlink" href="#helm.kserve.knative.serviceAnnotations.prometheus.io-scheme" title="Permanent link">#</a> { #helm.kserve.knative.serviceAnnotations.prometheus.io-scheme }
:   Type `string`, default `"http"`.

`kserve.knative.serviceAnnotations."prometheus.io/scrape"` <a class="headerlink" href="#helm.kserve.knative.serviceAnnotations.prometheus.io-scrape" title="Permanent link">#</a> { #helm.kserve.knative.serviceAnnotations.prometheus.io-scrape }
:   Type `string`, default `"true"`.

`kserve.knative.tolerations` <a class="headerlink" href="#helm.kserve.knative.tolerations" title="Permanent link">#</a> { #helm.kserve.knative.tolerations }
:   Type `list`, default `[]`.

`kserve.knative.topologySpreadConstraint` <a class="headerlink" href="#helm.kserve.knative.topologySpreadConstraint" title="Permanent link">#</a> { #helm.kserve.knative.topologySpreadConstraint }
:   Type `object`, default `{}`.
    The default topology spread constraint. If not defined the global topology spread constraint would be used instead.

`kserve.knative.validatingWebhookDeleteJobName` <a class="headerlink" href="#helm.kserve.knative.validatingWebhookDeleteJobName" title="Permanent link">#</a> { #helm.kserve.knative.validatingWebhookDeleteJobName }
:   Type `string`, default `"knative-serving-validating-webhook-delete-job"`.

`kserve.knative.validatingWebhookName` <a class="headerlink" href="#helm.kserve.knative.validatingWebhookName" title="Permanent link">#</a> { #helm.kserve.knative.validatingWebhookName }
:   Type `string`, default `"validation.webhook.serving.knative.dev"`.

`kserve.knative.version` <a class="headerlink" href="#helm.kserve.knative.version" title="Permanent link">#</a> { #helm.kserve.knative.version }
:   Type `string`, default `"v1.23.0"`.

</div>

## kserve { #helm-values-kserve-kserve }

??? example "Defaults as YAML"

    ```yaml
    kserve:
      kserve:
        agent:
          image: kserve/agent
          tag: v0.21.0
        controller:
          affinity: {}
          annotations: {}
          containerSecurityContext:
            allowPrivilegeEscalation: false
            capabilities:
              drop:
              - ALL
            privileged: false
            readOnlyRootFilesystem: true
            runAsNonRoot: true
            seccompProfile:
              type: RuntimeDefault
          deploymentMode: Knative
          gateway:
            additionalIngressDomains: []
            disableIngressCreation: false
            disableIstioVirtualHost: false
            domain: ''
            domainTemplate: '{{ .Name }}.{{ .Namespace }}.{{ .IngressDomain }}'
            ingressGateway:
              className: istio
              enableGatewayApi: false
              gateway: knative-ingress-gateway
            localGateway:
              gateway: knative-local-gateway
              gatewayService: knative-local-gateway
              knativeGatewayService: ''
            urlScheme: http
          image: kserve/kserve-controller
          knativeAddressableResolver:
            enabled: false
          labels: {}
          nodeSelector: {}
          podAnnotations: {}
          podDisruptionBudget:
            enabled: true
            minAvailable: 1
          podLabels: {}
          rbacProxy:
            resources:
              limits:
                cpu: 100m
                memory: 300Mi
              requests:
                cpu: 100m
                memory: 300Mi
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
          rbacProxyImage: quay.io/brancz/kube-rbac-proxy:v0.18.0
          replicaCount: 1
          resources:
            limits:
              cpu: 100m
              memory: 300Mi
            requests:
              cpu: 100m
              memory: 300Mi
          securityContext:
            runAsNonRoot: true
            seccompProfile:
              type: RuntimeDefault
          serviceAccount:
            annotations: {}
          tag: v0.21.0
          tolerations: []
          topologySpreadConstraint: {}
          topologySpreadConstraints: []
        localmodel:
          controller:
            image: kserve/kserve-localmodel-controller
            tag: v0.21.0
          enabled: false
          jobNamespace: kserve-localmodel-jobs
          securityContext:
            FSGroup: 1000
          serviceAccount:
            annotations: {}
        metricsaggregator:
          enableMetricAggregation: 'true'
          enablePrometheusScraping: 'true'
        nodeSelector: {}
        router:
          image: kserve/router
          tag: v0.21.0
        serviceAccount:
          annotations: {}
        servingruntime:
          modelNamePlaceholder: '{{.Name}}'
          sklearnserver:
            image: hopsworks/sklearnserver
            tag: 0.21.0
          tensorflow:
            image: tensorflow/serving
            tag: 2.20.0
          vllmomni:
            env: []
            image: vllm/vllm-omni
            imageRegistry: ''
            tag: v0.28.0
          vllmopenai:
            env: []
            image: vllm/vllm-openai
            imageRegistry: ''
            tag: v0.28.0
        storage:
          caBundleConfigMapName: ''
          caBundleVolumeMountPath: /etc/ssl/custom-certs
          cpuModelcar: 10m
          enableModelcar: false
          image: hopsworks/storage-initializer
          memoryModelcar: 15Mi
          resources:
            limits:
              cpu: '1'
              memory: 1Gi
            requests:
              cpu: 100m
              memory: 100Mi
          s3:
            CABundle: ''
            accessKeyIdName: AWS_ACCESS_KEY_ID
            endpoint: ''
            region: ''
            secretAccessKeyName: AWS_SECRET_ACCESS_KEY
            useAnonymousCredential: ''
            useHttps: ''
            useVirtualBucket: ''
            verifySSL: ''
          storageSecretNameAnnotation: serving.kserve.io/secretName
          storageSpecSecretName: storage-config
          tag: 5.2.0-SNAPSHOT
          uidModelcar: 1010
        tolerations: []
        topologySpreadConstraint: {}
        version: v0.21.0
    ```

<div class="hops-values" markdown>

`kserve.kserve.agent.image` <a class="headerlink" href="#helm.kserve.kserve.agent.image" title="Permanent link">#</a> { #helm.kserve.kserve.agent.image }
:   Type `string`, default `"kserve/agent"`.

`kserve.kserve.agent.tag` <a class="headerlink" href="#helm.kserve.kserve.agent.tag" title="Permanent link">#</a> { #helm.kserve.kserve.agent.tag }
:   Type `string`, default `"v0.21.0"`.

`kserve.kserve.controller.affinity` <a class="headerlink" href="#helm.kserve.kserve.controller.affinity" title="Permanent link">#</a> { #helm.kserve.kserve.controller.affinity }
:   Type `object`, default `{}`.
    A Kubernetes Affinity, if required. For more information, see [Affinity v1 core](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#affinity-v1-core).  For example:   affinity:     nodeAffinity:      requiredDuringSchedulingIgnoredDuringExecution:        nodeSelectorTerms:        - matchExpressions:          - key: foo.bar.com/role            operator: In            values:            - master

`kserve.kserve.controller.annotations` <a class="headerlink" href="#helm.kserve.kserve.controller.annotations" title="Permanent link">#</a> { #helm.kserve.kserve.controller.annotations }
:   Type `object`, default `{}`.
    Optional additional annotations to add to the controller deployment.

`kserve.kserve.controller.containerSecurityContext` <a class="headerlink" href="#helm.kserve.kserve.controller.containerSecurityContext" title="Permanent link">#</a> { #helm.kserve.kserve.controller.containerSecurityContext }
:   Type `object`.
    Container Security Context to be set on the controller component container. For more information, see [Configure a Security Context for a Pod or Container](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/).

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

`kserve.kserve.controller.deploymentMode` <a class="headerlink" href="#helm.kserve.kserve.controller.deploymentMode" title="Permanent link">#</a> { #helm.kserve.kserve.controller.deploymentMode }
:   Type `string`, default `"Knative"`.
    KServe deployment mode: "Knative" (formerly "Serverless"), "Standard" (formerly "RawDeployment").

`kserve.kserve.controller.gateway.additionalIngressDomains` <a class="headerlink" href="#helm.kserve.kserve.controller.gateway.additionalIngressDomains" title="Permanent link">#</a> { #helm.kserve.kserve.controller.gateway.additionalIngressDomains }
:   Type `list`, default `[]`.
    Optional additional domains for ingress routing.

`kserve.kserve.controller.gateway.disableIngressCreation` <a class="headerlink" href="#helm.kserve.kserve.controller.gateway.disableIngressCreation" title="Permanent link">#</a> { #helm.kserve.kserve.controller.gateway.disableIngressCreation }
:   Type `bool`, default `false`.
    Whether to disable ingress creation for RawDeployment mode.

`kserve.kserve.controller.gateway.disableIstioVirtualHost` <a class="headerlink" href="#helm.kserve.kserve.controller.gateway.disableIstioVirtualHost" title="Permanent link">#</a> { #helm.kserve.kserve.controller.gateway.disableIstioVirtualHost }
:   Type `bool`, default `false`.
    DisableIstioVirtualHost controls whether to use istio as network layer for top level component routing or path based routing. This configuration is only applicable for Serverless mode, when disabled Istio is no longer required.

`kserve.kserve.controller.gateway.domain` <a class="headerlink" href="#helm.kserve.kserve.controller.gateway.domain" title="Permanent link">#</a> { #helm.kserve.kserve.controller.gateway.domain }
:   Type `string`, default `""`.
    Ingress domain for RawDeployment mode, for Serverless it is configured in Knative. Empty falls back to `knative.domainName` so Standard-mode InferenceService hosts match Knative-mode hosts. If set explicitly it must stay aligned with `knative.domainName`: the gateway's authority rewrite and the model-serving authenticator only know that domain.

`kserve.kserve.controller.gateway.domainTemplate` <a class="headerlink" href="#helm.kserve.kserve.controller.gateway.domainTemplate" title="Permanent link">#</a> { #helm.kserve.kserve.controller.gateway.domainTemplate }
:   Type `string`, default `"{{ .Name }}.{{ .Namespace }}.{{ .IngressDomain }}"`.
    Ingress domain template for RawDeployment mode, for Serverless mode it is configured in Knative. Dot-separated to match the `<name>.<namespace>.<domain>` host format Knative-mode uses.

`kserve.kserve.controller.gateway.ingressGateway.className` <a class="headerlink" href="#helm.kserve.kserve.controller.gateway.ingressGateway.className" title="Permanent link">#</a> { #helm.kserve.kserve.controller.gateway.ingressGateway.className }
:   Type `string`, default `"istio"`.

`kserve.kserve.controller.gateway.ingressGateway.enableGatewayApi` <a class="headerlink" href="#helm.kserve.kserve.controller.gateway.ingressGateway.enableGatewayApi" title="Permanent link">#</a> { #helm.kserve.kserve.controller.gateway.ingressGateway.enableGatewayApi }
:   Type `bool`, default `false`.
    Whether to use the Gateway API for ingress routing instead of Kubernetes Ingress. Kept false for the Knative + Istio network layer.

`kserve.kserve.controller.gateway.ingressGateway.gateway` <a class="headerlink" href="#helm.kserve.kserve.controller.gateway.ingressGateway.gateway" title="Permanent link">#</a> { #helm.kserve.kserve.controller.gateway.ingressGateway.gateway }
:   Type `string`, default `"knative-ingress-gateway"`.

`kserve.kserve.controller.gateway.localGateway.gateway` <a class="headerlink" href="#helm.kserve.kserve.controller.gateway.localGateway.gateway" title="Permanent link">#</a> { #helm.kserve.kserve.controller.gateway.localGateway.gateway }
:   Type `string`, default `"knative-local-gateway"`.
    localGateway specifies the gateway which handles the network traffic within the cluster.

`kserve.kserve.controller.gateway.localGateway.gatewayService` <a class="headerlink" href="#helm.kserve.kserve.controller.gateway.localGateway.gatewayService" title="Permanent link">#</a> { #helm.kserve.kserve.controller.gateway.localGateway.gatewayService }
:   Type `string`, default `"knative-local-gateway"`.
    localGatewayService specifies the hostname of the local gateway service.

`kserve.kserve.controller.gateway.localGateway.knativeGatewayService` <a class="headerlink" href="#helm.kserve.kserve.controller.gateway.localGateway.knativeGatewayService" title="Permanent link">#</a> { #helm.kserve.kserve.controller.gateway.localGateway.knativeGatewayService }
:   Type `string`, default `""`.
    knativeLocalGatewayService specifies the hostname of the Knative's local gateway service. When unset, the value of "localGatewayService" will be used. When enabling strict mTLS in Istio, KServe local gateway should be created and pointed to the Knative local gateway.

`kserve.kserve.controller.gateway.urlScheme` <a class="headerlink" href="#helm.kserve.kserve.controller.gateway.urlScheme" title="Permanent link">#</a> { #helm.kserve.kserve.controller.gateway.urlScheme }
:   Type `string`, default `"http"`.
    HTTP endpoint url scheme.

`kserve.kserve.controller.image` <a class="headerlink" href="#helm.kserve.kserve.controller.image" title="Permanent link">#</a> { #helm.kserve.kserve.controller.image }
:   Type `string`, default `"kserve/kserve-controller"`.
    KServe controller container image name. Mirrored from upstream kserve/kserve-controller (the Hopsworks idempotency patch is upstream as of 0.19, so the controller is no longer built from the fork).

`kserve.kserve.controller.knativeAddressableResolver` <a class="headerlink" href="#helm.kserve.kserve.controller.knativeAddressableResolver" title="Permanent link">#</a> { #helm.kserve.kserve.controller.knativeAddressableResolver }
:   Type `object`, default `{"enabled":false}`.
    Indicates whether to create an addressable resolver ClusterRole for Knative Eventing. This ClusterRole grants the necessary permissions for the Knative's DomainMapping reconciler to resolve InferenceService addressables.

`kserve.kserve.controller.labels` <a class="headerlink" href="#helm.kserve.kserve.controller.labels" title="Permanent link">#</a> { #helm.kserve.kserve.controller.labels }
:   Type `object`, default `{}`.
    Optional additional labels to add to the controller deployment.

`kserve.kserve.controller.nodeSelector` <a class="headerlink" href="#helm.kserve.kserve.controller.nodeSelector" title="Permanent link">#</a> { #helm.kserve.kserve.controller.nodeSelector }
:   Type `object`, default `{}`.
    The nodeSelector on Pods tells Kubernetes to schedule Pods on the nodes with matching labels. For more information, see [Assigning Pods to Nodes](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/). 

`kserve.kserve.controller.podAnnotations` <a class="headerlink" href="#helm.kserve.kserve.controller.podAnnotations" title="Permanent link">#</a> { #helm.kserve.kserve.controller.podAnnotations }
:   Type `object`, default `{}`.
    Optional additional labels to add to the controller Pods.

`kserve.kserve.controller.podDisruptionBudget.enabled` <a class="headerlink" href="#helm.kserve.kserve.controller.podDisruptionBudget.enabled" title="Permanent link">#</a> { #helm.kserve.kserve.controller.podDisruptionBudget.enabled }
:   Type `bool`, default `true`.

`kserve.kserve.controller.podDisruptionBudget.minAvailable` <a class="headerlink" href="#helm.kserve.kserve.controller.podDisruptionBudget.minAvailable" title="Permanent link">#</a> { #helm.kserve.kserve.controller.podDisruptionBudget.minAvailable }
:   Type `int`, default `1`.

`kserve.kserve.controller.podLabels` <a class="headerlink" href="#helm.kserve.kserve.controller.podLabels" title="Permanent link">#</a> { #helm.kserve.kserve.controller.podLabels }
:   Type `object`, default `{}`.
    Optional additional labels to add to the controller Pods.

`kserve.kserve.controller.rbacProxy.resources.limits.cpu` <a class="headerlink" href="#helm.kserve.kserve.controller.rbacProxy.resources.limits.cpu" title="Permanent link">#</a> { #helm.kserve.kserve.controller.rbacProxy.resources.limits.cpu }
:   Type `string`, default `"100m"`.

`kserve.kserve.controller.rbacProxy.resources.limits.memory` <a class="headerlink" href="#helm.kserve.kserve.controller.rbacProxy.resources.limits.memory" title="Permanent link">#</a> { #helm.kserve.kserve.controller.rbacProxy.resources.limits.memory }
:   Type `string`, default `"300Mi"`.

`kserve.kserve.controller.rbacProxy.resources.requests.cpu` <a class="headerlink" href="#helm.kserve.kserve.controller.rbacProxy.resources.requests.cpu" title="Permanent link">#</a> { #helm.kserve.kserve.controller.rbacProxy.resources.requests.cpu }
:   Type `string`, default `"100m"`.

`kserve.kserve.controller.rbacProxy.resources.requests.memory` <a class="headerlink" href="#helm.kserve.kserve.controller.rbacProxy.resources.requests.memory" title="Permanent link">#</a> { #helm.kserve.kserve.controller.rbacProxy.resources.requests.memory }
:   Type `string`, default `"300Mi"`.

`kserve.kserve.controller.rbacProxy.securityContext` <a class="headerlink" href="#helm.kserve.kserve.controller.rbacProxy.securityContext" title="Permanent link">#</a> { #helm.kserve.kserve.controller.rbacProxy.securityContext }
:   Type `object`.
    security context configuration

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

`kserve.kserve.controller.rbacProxyImage` <a class="headerlink" href="#helm.kserve.kserve.controller.rbacProxyImage" title="Permanent link">#</a> { #helm.kserve.kserve.controller.rbacProxyImage }
:   Type `string`, default `"quay.io/brancz/kube-rbac-proxy:v0.18.0"`.
    KServe controller manager rbac proxy container image

`kserve.kserve.controller.replicaCount` <a class="headerlink" href="#helm.kserve.kserve.controller.replicaCount" title="Permanent link">#</a> { #helm.kserve.kserve.controller.replicaCount }
:   Type `int`, default `1`.

`kserve.kserve.controller.resources` <a class="headerlink" href="#helm.kserve.kserve.controller.resources" title="Permanent link">#</a> { #helm.kserve.kserve.controller.resources }
:   Type `object`.
    Resources to provide to the kserve controller pod.  For example:  requests:    cpu: 10m    memory: 32Mi  For more information, see [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/).

    ??? note "Default"

        ```yaml
        limits:
          cpu: 100m
          memory: 300Mi
        requests:
          cpu: 100m
          memory: 300Mi
        ```

`kserve.kserve.controller.securityContext` <a class="headerlink" href="#helm.kserve.kserve.controller.securityContext" title="Permanent link">#</a> { #helm.kserve.kserve.controller.securityContext }
:   Type `object`, default `{"runAsNonRoot":true,"seccompProfile":{"type":"RuntimeDefault"}}`.
    Pod Security Context. For more information, see [Configure a Security Context for a Pod or Container](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/).

`kserve.kserve.controller.serviceAccount.annotations` <a class="headerlink" href="#helm.kserve.kserve.controller.serviceAccount.annotations" title="Permanent link">#</a> { #helm.kserve.kserve.controller.serviceAccount.annotations }
:   Type `object`, default `{}`.
    service account annotations

`kserve.kserve.controller.tag` <a class="headerlink" href="#helm.kserve.kserve.controller.tag" title="Permanent link">#</a> { #helm.kserve.kserve.controller.tag }
:   Type `string`, default `"v0.21.0"`.
    KServe controller container image tag.

`kserve.kserve.controller.tolerations` <a class="headerlink" href="#helm.kserve.kserve.controller.tolerations" title="Permanent link">#</a> { #helm.kserve.kserve.controller.tolerations }
:   Type `list`, default `[]`.
    A list of Kubernetes Tolerations, if required. For more information, see [Toleration v1 core](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#toleration-v1-core).  For example:   tolerations:   - key: foo.bar.com/role     operator: Equal     value: master     effect: NoSchedule

`kserve.kserve.controller.topologySpreadConstraint` <a class="headerlink" href="#helm.kserve.kserve.controller.topologySpreadConstraint" title="Permanent link">#</a> { #helm.kserve.kserve.controller.topologySpreadConstraint }
:   Type `object`, default `{}`.
    The default topology spread constraint. If not defined the global topology spread constraint would be used instead only if topologySpreadConstraints list is empty.

`kserve.kserve.controller.topologySpreadConstraints` <a class="headerlink" href="#helm.kserve.kserve.controller.topologySpreadConstraints" title="Permanent link">#</a> { #helm.kserve.kserve.controller.topologySpreadConstraints }
:   Type `list`, default `[]`.
    A list of Kubernetes TopologySpreadConstraints, if required. For more information, see \[Topology spread constraint v1 core\](<https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#topologyspreadconstraint-v1-core>  For example:   topologySpreadConstraints:   - maxSkew: 2     topologyKey: topology.kubernetes.io/zone     whenUnsatisfiable: ScheduleAnyway     labelSelector:       matchLabels:         app.kubernetes.io/instance: kserve-controller-manager         app.kubernetes.io/component: controller

`kserve.kserve.localmodel.controller.image` <a class="headerlink" href="#helm.kserve.kserve.localmodel.controller.image" title="Permanent link">#</a> { #helm.kserve.kserve.localmodel.controller.image }
:   Type `string`, default `"kserve/kserve-localmodel-controller"`.

`kserve.kserve.localmodel.controller.tag` <a class="headerlink" href="#helm.kserve.kserve.localmodel.controller.tag" title="Permanent link">#</a> { #helm.kserve.kserve.localmodel.controller.tag }
:   Type `string`, default `"v0.21.0"`.

`kserve.kserve.localmodel.enabled` <a class="headerlink" href="#helm.kserve.kserve.localmodel.enabled" title="Permanent link">#</a> { #helm.kserve.kserve.localmodel.enabled }
:   Type `bool`, default `false`.
    Feeds the `localModel` block of `inferenceservice-config` only and must stay false: the chart ships no localmodel controller (the dormant copy vendored with 0.19 was removed with 0.21; the feature arrives with the upstream kserve-localmodel charts). Rendering fails on `true` so an old values file cannot enable the feature with no controller behind it. `controller` and `serviceAccount` are kept for values compatibility and render nothing.

`kserve.kserve.localmodel.jobNamespace` <a class="headerlink" href="#helm.kserve.kserve.localmodel.jobNamespace" title="Permanent link">#</a> { #helm.kserve.kserve.localmodel.jobNamespace }
:   Type `string`, default `"kserve-localmodel-jobs"`.

`kserve.kserve.localmodel.securityContext` <a class="headerlink" href="#helm.kserve.kserve.localmodel.securityContext" title="Permanent link">#</a> { #helm.kserve.kserve.localmodel.securityContext }
:   Type `object`, default `{"FSGroup":1000}`.
    security context configuration

`kserve.kserve.localmodel.serviceAccount.annotations` <a class="headerlink" href="#helm.kserve.kserve.localmodel.serviceAccount.annotations" title="Permanent link">#</a> { #helm.kserve.kserve.localmodel.serviceAccount.annotations }
:   Type `object`, default `{}`.
    service account annotations

`kserve.kserve.metricsaggregator.enableMetricAggregation` <a class="headerlink" href="#helm.kserve.kserve.metricsaggregator.enableMetricAggregation" title="Permanent link">#</a> { #helm.kserve.kserve.metricsaggregator.enableMetricAggregation }
:   Type `string`, default `"true"`.
    configures metric aggregation annotation. This adds the annotation serving.kserve.io/enable-metric-aggregation to every service with the specified boolean value. If true enables metric aggregation in queue-proxy by setting env vars in the queue proxy container to configure scraping ports.

`kserve.kserve.metricsaggregator.enablePrometheusScraping` <a class="headerlink" href="#helm.kserve.kserve.metricsaggregator.enablePrometheusScraping" title="Permanent link">#</a> { #helm.kserve.kserve.metricsaggregator.enablePrometheusScraping }
:   Type `string`, default `"true"`.
    If true, prometheus annotations are added to the pod to scrape the metrics. If serving.kserve.io/enable-metric-aggregation is false, the prometheus port is set with the default prometheus scraping port 9090, otherwise the prometheus port annotation is set with the metric aggregation port.

`kserve.kserve.nodeSelector` <a class="headerlink" href="#helm.kserve.kserve.nodeSelector" title="Permanent link">#</a> { #helm.kserve.kserve.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

`kserve.kserve.router.image` <a class="headerlink" href="#helm.kserve.kserve.router.image" title="Permanent link">#</a> { #helm.kserve.kserve.router.image }
:   Type `string`, default `"kserve/router"`.

`kserve.kserve.router.tag` <a class="headerlink" href="#helm.kserve.kserve.router.tag" title="Permanent link">#</a> { #helm.kserve.kserve.router.tag }
:   Type `string`, default `"v0.21.0"`.

`kserve.kserve.serviceAccount.annotations` <a class="headerlink" href="#helm.kserve.kserve.serviceAccount.annotations" title="Permanent link">#</a> { #helm.kserve.kserve.serviceAccount.annotations }
:   Type `object`, default `{}`.
    service account annotations

`kserve.kserve.servingruntime.modelNamePlaceholder` <a class="headerlink" href="#helm.kserve.kserve.servingruntime.modelNamePlaceholder" title="Permanent link">#</a> { #helm.kserve.kserve.servingruntime.modelNamePlaceholder }
:   Type `string`, default `"{{.Name}}"`.

`kserve.kserve.servingruntime.sklearnserver.image` <a class="headerlink" href="#helm.kserve.kserve.servingruntime.sklearnserver.image" title="Permanent link">#</a> { #helm.kserve.kserve.servingruntime.sklearnserver.image }
:   Type `string`, default `"hopsworks/sklearnserver"`.

`kserve.kserve.servingruntime.sklearnserver.tag` <a class="headerlink" href="#helm.kserve.kserve.servingruntime.sklearnserver.tag" title="Permanent link">#</a> { #helm.kserve.kserve.servingruntime.sklearnserver.tag }
:   Type `string`, default `"0.21.0"`.

`kserve.kserve.servingruntime.tensorflow.image` <a class="headerlink" href="#helm.kserve.kserve.servingruntime.tensorflow.image" title="Permanent link">#</a> { #helm.kserve.kserve.servingruntime.tensorflow.image }
:   Type `string`, default `"tensorflow/serving"`.

`kserve.kserve.servingruntime.tensorflow.tag` <a class="headerlink" href="#helm.kserve.kserve.servingruntime.tensorflow.tag" title="Permanent link">#</a> { #helm.kserve.kserve.servingruntime.tensorflow.tag }
:   Type `string`, default `"2.20.0"`.

`kserve.kserve.servingruntime.vllmomni` <a class="headerlink" href="#helm.kserve.kserve.servingruntime.vllmomni" title="Permanent link">#</a> { #helm.kserve.kserve.servingruntime.vllmomni }
:   Type `object`, default `{"env":[],"image":"vllm/vllm-omni","imageRegistry":"","tag":"v0.28.0"}`.
    backs the `vllm-omni` ClusterServingRuntime (vLLM-Omni)

`kserve.kserve.servingruntime.vllmomni.env` <a class="headerlink" href="#helm.kserve.kserve.servingruntime.vllmomni.env" title="Permanent link">#</a> { #helm.kserve.kserve.servingruntime.vllmomni.env }
:   Type `list`, default `[]`.
    Additional environment variables for vllm-omni container

`kserve.kserve.servingruntime.vllmomni.imageRegistry` <a class="headerlink" href="#helm.kserve.kserve.servingruntime.vllmomni.imageRegistry" title="Permanent link">#</a> { #helm.kserve.kserve.servingruntime.vllmomni.imageRegistry }
:   Type `string`, default `""`.
    Registry override for the vllm-omni image. Empty falls back to `global._hopsworks.imageRegistry`.

`kserve.kserve.servingruntime.vllmopenai` <a class="headerlink" href="#helm.kserve.kserve.servingruntime.vllmopenai" title="Permanent link">#</a> { #helm.kserve.kserve.servingruntime.vllmopenai }
:   Type `object`, default `{"env":[],"image":"vllm/vllm-openai","imageRegistry":"","tag":"v0.28.0"}`.
    backs the `vllm-openai` ClusterServingRuntime (standard vLLM)

`kserve.kserve.servingruntime.vllmopenai.env` <a class="headerlink" href="#helm.kserve.kserve.servingruntime.vllmopenai.env" title="Permanent link">#</a> { #helm.kserve.kserve.servingruntime.vllmopenai.env }
:   Type `list`, default `[]`.
    Additional environment variables for vllm-openai container

`kserve.kserve.servingruntime.vllmopenai.imageRegistry` <a class="headerlink" href="#helm.kserve.kserve.servingruntime.vllmopenai.imageRegistry" title="Permanent link">#</a> { #helm.kserve.kserve.servingruntime.vllmopenai.imageRegistry }
:   Type `string`, default `""`.
    Registry override for the vllm-openai image. Empty falls back to `global._hopsworks.imageRegistry`.

`kserve.kserve.storage.caBundleConfigMapName` <a class="headerlink" href="#helm.kserve.kserve.storage.caBundleConfigMapName" title="Permanent link">#</a> { #helm.kserve.kserve.storage.caBundleConfigMapName }
:   Type `string`, default `""`.
    Mounted CA bundle config map name for storage initializer.

`kserve.kserve.storage.caBundleVolumeMountPath` <a class="headerlink" href="#helm.kserve.kserve.storage.caBundleVolumeMountPath" title="Permanent link">#</a> { #helm.kserve.kserve.storage.caBundleVolumeMountPath }
:   Type `string`, default `"/etc/ssl/custom-certs"`.
    Mounted path for CA bundle config map.

`kserve.kserve.storage.cpuModelcar` <a class="headerlink" href="#helm.kserve.kserve.storage.cpuModelcar" title="Permanent link">#</a> { #helm.kserve.kserve.storage.cpuModelcar }
:   Type `string`, default `"10m"`.
    Model sidecar cpu requirement.

`kserve.kserve.storage.enableModelcar` <a class="headerlink" href="#helm.kserve.kserve.storage.enableModelcar" title="Permanent link">#</a> { #helm.kserve.kserve.storage.enableModelcar }
:   Type `bool`, default `false`.
    Flag for enabling model sidecar feature.

`kserve.kserve.storage.image` <a class="headerlink" href="#helm.kserve.kserve.storage.image" title="Permanent link">#</a> { #helm.kserve.kserve.storage.image }
:   Type `string`, default `"hopsworks/storage-initializer"`.

`kserve.kserve.storage.memoryModelcar` <a class="headerlink" href="#helm.kserve.kserve.storage.memoryModelcar" title="Permanent link">#</a> { #helm.kserve.kserve.storage.memoryModelcar }
:   Type `string`, default `"15Mi"`.
    Model sidecar memory requirement.

`kserve.kserve.storage.resources` <a class="headerlink" href="#helm.kserve.kserve.storage.resources" title="Permanent link">#</a> { #helm.kserve.kserve.storage.resources }
:   Type `object`.
    Requests and limits KServe gives the storage-initializer init container it injects for storageUri models (the `storageInitializer` block of `inferenceservice-config`).

    ??? note "Default"

        ```yaml
        limits:
          cpu: '1'
          memory: 1Gi
        requests:
          cpu: 100m
          memory: 100Mi
        ```

`kserve.kserve.storage.resources.limits` <a class="headerlink" href="#helm.kserve.kserve.storage.resources.limits" title="Permanent link">#</a> { #helm.kserve.kserve.storage.resources.limits }
:   Type `object`, default `{"cpu":"1","memory":"1Gi"}`.
    cpu and memory are read by the templates; other resource names pass through to the ClusterStorageContainer.

`kserve.kserve.storage.resources.requests` <a class="headerlink" href="#helm.kserve.kserve.storage.resources.requests" title="Permanent link">#</a> { #helm.kserve.kserve.storage.resources.requests }
:   Type `object`, default `{"cpu":"100m","memory":"100Mi"}`.
    cpu and memory are read by the templates; other resource names pass through to the ClusterStorageContainer.

`kserve.kserve.storage.s3` <a class="headerlink" href="#helm.kserve.kserve.storage.s3" title="Permanent link">#</a> { #helm.kserve.kserve.storage.s3 }
:   Type `object`.
    Configurations for S3 storage

    ??? note "Default"

        ```yaml
        CABundle: ''
        accessKeyIdName: AWS_ACCESS_KEY_ID
        endpoint: ''
        region: ''
        secretAccessKeyName: AWS_SECRET_ACCESS_KEY
        useAnonymousCredential: ''
        useHttps: ''
        useVirtualBucket: ''
        verifySSL: ''
        ```

`kserve.kserve.storage.s3.CABundle` <a class="headerlink" href="#helm.kserve.kserve.storage.s3.CABundle" title="Permanent link">#</a> { #helm.kserve.kserve.storage.s3.CABundle }
:   Type `string`, default `""`.
    The path to the certificate bundle to use for HTTPS certificate validation.

`kserve.kserve.storage.s3.accessKeyIdName` <a class="headerlink" href="#helm.kserve.kserve.storage.s3.accessKeyIdName" title="Permanent link">#</a> { #helm.kserve.kserve.storage.s3.accessKeyIdName }
:   Type `string`, default `"AWS_ACCESS_KEY_ID"`.
    AWS S3 static access key id.

`kserve.kserve.storage.s3.endpoint` <a class="headerlink" href="#helm.kserve.kserve.storage.s3.endpoint" title="Permanent link">#</a> { #helm.kserve.kserve.storage.s3.endpoint }
:   Type `string`, default `""`.
    AWS S3 endpoint.

`kserve.kserve.storage.s3.region` <a class="headerlink" href="#helm.kserve.kserve.storage.s3.region" title="Permanent link">#</a> { #helm.kserve.kserve.storage.s3.region }
:   Type `string`, default `""`.
    Default region name of AWS S3.

`kserve.kserve.storage.s3.secretAccessKeyName` <a class="headerlink" href="#helm.kserve.kserve.storage.s3.secretAccessKeyName" title="Permanent link">#</a> { #helm.kserve.kserve.storage.s3.secretAccessKeyName }
:   Type `string`, default `"AWS_SECRET_ACCESS_KEY"`.
    AWS S3 static secret access key.

`kserve.kserve.storage.s3.useAnonymousCredential` <a class="headerlink" href="#helm.kserve.kserve.storage.s3.useAnonymousCredential" title="Permanent link">#</a> { #helm.kserve.kserve.storage.s3.useAnonymousCredential }
:   Type `string`, default `""`.
    Whether to use anonymous credentials to download the model or not, default to false.

`kserve.kserve.storage.s3.useHttps` <a class="headerlink" href="#helm.kserve.kserve.storage.s3.useHttps" title="Permanent link">#</a> { #helm.kserve.kserve.storage.s3.useHttps }
:   Type `string`, default `""`.
    Whether to use secured https or http to download models, allowed values are 0 and 1 and default to 1.

`kserve.kserve.storage.s3.useVirtualBucket` <a class="headerlink" href="#helm.kserve.kserve.storage.s3.useVirtualBucket" title="Permanent link">#</a> { #helm.kserve.kserve.storage.s3.useVirtualBucket }
:   Type `string`, default `""`.
    Whether to use virtual bucket or not, default to false.

`kserve.kserve.storage.s3.verifySSL` <a class="headerlink" href="#helm.kserve.kserve.storage.s3.verifySSL" title="Permanent link">#</a> { #helm.kserve.kserve.storage.s3.verifySSL }
:   Type `string`, default `""`.
    Whether to verify the tls/ssl certificate, default to true.

`kserve.kserve.storage.storageSecretNameAnnotation` <a class="headerlink" href="#helm.kserve.kserve.storage.storageSecretNameAnnotation" title="Permanent link">#</a> { #helm.kserve.kserve.storage.storageSecretNameAnnotation }
:   Type `string`, default `"serving.kserve.io/secretName"`.
    Storage secret name reference for storage initializer.

`kserve.kserve.storage.storageSpecSecretName` <a class="headerlink" href="#helm.kserve.kserve.storage.storageSpecSecretName" title="Permanent link">#</a> { #helm.kserve.kserve.storage.storageSpecSecretName }
:   Type `string`, default `"storage-config"`.
    Storage spec secret name.

`kserve.kserve.storage.tag` <a class="headerlink" href="#helm.kserve.kserve.storage.tag" title="Permanent link">#</a> { #helm.kserve.kserve.storage.tag }
:   Type `string`, default `"5.2.0-SNAPSHOT"`.
    Hopsworks-built storage initializer tag. Pinned to the Hopsworks version (matching storageInitializer.tag and what the model-serving-webhook publishes), not the KServe version anchor.

`kserve.kserve.storage.uidModelcar` <a class="headerlink" href="#helm.kserve.kserve.storage.uidModelcar" title="Permanent link">#</a> { #helm.kserve.kserve.storage.uidModelcar }
:   Type `int`, default `1010`.
    UID under which the modelcar process and the main container run. Some clusters require root (0).

`kserve.kserve.tolerations` <a class="headerlink" href="#helm.kserve.kserve.tolerations" title="Permanent link">#</a> { #helm.kserve.kserve.tolerations }
:   Type `list`, default `[]`.

`kserve.kserve.topologySpreadConstraint` <a class="headerlink" href="#helm.kserve.kserve.topologySpreadConstraint" title="Permanent link">#</a> { #helm.kserve.kserve.topologySpreadConstraint }
:   Type `object`, default `{}`.
    The default topology spread constraint. If not defined the global topology spread constraint would be used instead only if topologySpreadConstraints list is empty.

`kserve.kserve.version` <a class="headerlink" href="#helm.kserve.kserve.version" title="Permanent link">#</a> { #helm.kserve.kserve.version }
:   Type `string`, default `"v0.21.0"`.

</div>

## servingAuthenticator { #helm-values-kserve-servingauthenticator }

??? example "Defaults as YAML"

    ```yaml
    kserve:
      servingAuthenticator:
        image: hopsworks/model-serving-authenticator
        name: model-serving-authenticator
        podDisruptionBudget:
          enabled: true
          minAvailable: 1
        replicaCount: 1
        requireExternalUserLoginAfterHours: 720
        serviceAccount:
          annotations: {}
        tag: 5.2.0-SNAPSHOT
    ```

<div class="hops-values" markdown>

`kserve.servingAuthenticator.image` <a class="headerlink" href="#helm.kserve.servingAuthenticator.image" title="Permanent link">#</a> { #helm.kserve.servingAuthenticator.image }
:   Type `string`, default `"hopsworks/model-serving-authenticator"`.

`kserve.servingAuthenticator.name` <a class="headerlink" href="#helm.kserve.servingAuthenticator.name" title="Permanent link">#</a> { #helm.kserve.servingAuthenticator.name }
:   Type `string`, default `"model-serving-authenticator"`.

`kserve.servingAuthenticator.podDisruptionBudget.enabled` <a class="headerlink" href="#helm.kserve.servingAuthenticator.podDisruptionBudget.enabled" title="Permanent link">#</a> { #helm.kserve.servingAuthenticator.podDisruptionBudget.enabled }
:   Type `bool`, default `true`.

`kserve.servingAuthenticator.podDisruptionBudget.minAvailable` <a class="headerlink" href="#helm.kserve.servingAuthenticator.podDisruptionBudget.minAvailable" title="Permanent link">#</a> { #helm.kserve.servingAuthenticator.podDisruptionBudget.minAvailable }
:   Type `int`, default `1`.

`kserve.servingAuthenticator.replicaCount` <a class="headerlink" href="#helm.kserve.servingAuthenticator.replicaCount" title="Permanent link">#</a> { #helm.kserve.servingAuthenticator.replicaCount }
:   Type `int`, default `1`.

`kserve.servingAuthenticator.requireExternalUserLoginAfterHours` <a class="headerlink" href="#helm.kserve.servingAuthenticator.requireExternalUserLoginAfterHours" title="Permanent link">#</a> { #helm.kserve.servingAuthenticator.requireExternalUserLoginAfterHours }
:   Type `int`, default `720`.
    Number of hours after which external users are required to sign in to Hopsworks to refresh their external user groups. Allowed values are -1, 0 and greater than 0, where -1 skips the periodic sign-in requirement and 0 disables external access completely.

`kserve.servingAuthenticator.serviceAccount.annotations` <a class="headerlink" href="#helm.kserve.servingAuthenticator.serviceAccount.annotations" title="Permanent link">#</a> { #helm.kserve.servingAuthenticator.serviceAccount.annotations }
:   Type `object`, default `{}`.
    service account annotations

`kserve.servingAuthenticator.tag` <a class="headerlink" href="#helm.kserve.servingAuthenticator.tag" title="Permanent link">#</a> { #helm.kserve.servingAuthenticator.tag }
:   Type `string`, default `"5.2.0-SNAPSHOT"`.

</div>

## servingWebhook { #helm-values-kserve-servingwebhook }

??? example "Defaults as YAML"

    ```yaml
    kserve:
      servingWebhook:
        ephemeralVolume:
          accessModes:
          - ReadWriteOnce
          enabled: false
          storageClassName: ''
          storageSize: 60Gi
        image: hopsworks/model-serving-webhook
        name: model-serving-webhook
        podDisruptionBudget:
          enabled: true
          minAvailable: 1
        replicaCount: 1
        serviceAccount:
          annotations: {}
        tag: 5.2.0-SNAPSHOT
        ttlSecondsAfterFinished: null
    ```

<div class="hops-values" markdown>

`kserve.servingWebhook.ephemeralVolume` <a class="headerlink" href="#helm.kserve.servingWebhook.ephemeralVolume" title="Permanent link">#</a> { #helm.kserve.servingWebhook.ephemeralVolume }
:   Type `object`.
    Configuration for ephemeral volumes in LLM deployments

    ??? note "Default"

        ```yaml
        accessModes:
        - ReadWriteOnce
        enabled: false
        storageClassName: ''
        storageSize: 60Gi
        ```

`kserve.servingWebhook.ephemeralVolume.accessModes` <a class="headerlink" href="#helm.kserve.servingWebhook.ephemeralVolume.accessModes" title="Permanent link">#</a> { #helm.kserve.servingWebhook.ephemeralVolume.accessModes }
:   Type `list`, default `["ReadWriteOnce"]`.
    Access modes for the ephemeral volume

`kserve.servingWebhook.ephemeralVolume.enabled` <a class="headerlink" href="#helm.kserve.servingWebhook.ephemeralVolume.enabled" title="Permanent link">#</a> { #helm.kserve.servingWebhook.ephemeralVolume.enabled }
:   Type `bool`, default `false`.
    Enable ephemeral volume injection for LLM deployments

`kserve.servingWebhook.ephemeralVolume.storageClassName` <a class="headerlink" href="#helm.kserve.servingWebhook.ephemeralVolume.storageClassName" title="Permanent link">#</a> { #helm.kserve.servingWebhook.ephemeralVolume.storageClassName }
:   Type `string`, default `""`.
    Storage class name for the ephemeral volume

`kserve.servingWebhook.ephemeralVolume.storageSize` <a class="headerlink" href="#helm.kserve.servingWebhook.ephemeralVolume.storageSize" title="Permanent link">#</a> { #helm.kserve.servingWebhook.ephemeralVolume.storageSize }
:   Type `string`, default `"60Gi"`.
    Storage size for the ephemeral volume

`kserve.servingWebhook.image` <a class="headerlink" href="#helm.kserve.servingWebhook.image" title="Permanent link">#</a> { #helm.kserve.servingWebhook.image }
:   Type `string`, default `"hopsworks/model-serving-webhook"`.

`kserve.servingWebhook.name` <a class="headerlink" href="#helm.kserve.servingWebhook.name" title="Permanent link">#</a> { #helm.kserve.servingWebhook.name }
:   Type `string`, default `"model-serving-webhook"`.

`kserve.servingWebhook.podDisruptionBudget.enabled` <a class="headerlink" href="#helm.kserve.servingWebhook.podDisruptionBudget.enabled" title="Permanent link">#</a> { #helm.kserve.servingWebhook.podDisruptionBudget.enabled }
:   Type `bool`, default `true`.

`kserve.servingWebhook.podDisruptionBudget.minAvailable` <a class="headerlink" href="#helm.kserve.servingWebhook.podDisruptionBudget.minAvailable" title="Permanent link">#</a> { #helm.kserve.servingWebhook.podDisruptionBudget.minAvailable }
:   Type `int`, default `1`.

`kserve.servingWebhook.replicaCount` <a class="headerlink" href="#helm.kserve.servingWebhook.replicaCount" title="Permanent link">#</a> { #helm.kserve.servingWebhook.replicaCount }
:   Type `int`, default `1`.

`kserve.servingWebhook.serviceAccount.annotations` <a class="headerlink" href="#helm.kserve.servingWebhook.serviceAccount.annotations" title="Permanent link">#</a> { #helm.kserve.servingWebhook.serviceAccount.annotations }
:   Type `object`, default `{}`.
    service account annotations

`kserve.servingWebhook.tag` <a class="headerlink" href="#helm.kserve.servingWebhook.tag" title="Permanent link">#</a> { #helm.kserve.servingWebhook.tag }
:   Type `string`, default `"5.2.0-SNAPSHOT"`.

`kserve.servingWebhook.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.kserve.servingWebhook.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.kserve.servingWebhook.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    TTL in seconds for the serving-mwh Job. Overrides global default.

</div>

<!-- END GENERATED VALUES -->
