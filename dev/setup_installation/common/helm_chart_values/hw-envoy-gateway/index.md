# Envoy Gateway values { #helm-values-hw-envoy-gateway }

Values under `hw-envoy-gateway` configure the Envoy Gateway controller, the Gateway API front door of Standard-mode model deployments, and the hook that applies its CustomResourceDefinitions.
The subchart is installed when `global._hopsworks.envoyGateway.enabled` is true (off by default); the Gateway itself, its policies and its Service are configured under `kserve.envoyGateway` in [KServe values][helm-values-kserve].
See [Envoy Gateway][envoy-gateway] for what the chart installs and what the cluster needs.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.3.0-alpha-1793348603` (Hopsworks `5.3.0`)._

Deployed according to the first of these values that is set: `global._hopsworks.envoyGateway.enabled`, [`global._hopsworks.full_platform`](global.md#helm.global._hopsworks.full_platform).

## General { #helm-values-hw-envoy-gateway-general }

??? example "Defaults as YAML"

    ```yaml
    hw-envoy-gateway:
      crdImage:
        name: envoy-gateway-crds
        registry: ''
        tag: v1.9.2-h1
      envoyProxy:
        image:
          registry: ''
          repository: envoyproxy/envoy
          tag: distroless-v1.39.1
      gatewayApiCrds:
        enabled: true
      gatewayClass:
        controllerName: ''
      hopsworkslib: {}
    ```

<div class="hops-values" markdown>

`hw-envoy-gateway` <a class="headerlink" href="#helm.hw-envoy-gateway" title="Permanent link">#</a> { #helm.hw-envoy-gateway }
:   Type `object`, default `{}`.
    override hw-envoy-gateway values

`hw-envoy-gateway.crdImage` <a class="headerlink" href="#helm.hw-envoy-gateway.crdImage" title="Permanent link">#</a> { #helm.hw-envoy-gateway.crdImage }
:   Type `object`, default `{"name":"envoy-gateway-crds","registry":"","tag":"v1.9.2-h1"}`.
    the image that carries the Envoy Gateway and Gateway API CRDs (docker-images envoy-gateway-crds, on the hwutils toolbox image). The CRDs cannot ship in the chart: they are 3.8 MB and Helm keeps the chart files in a release Secret capped at 1 MiB, so the install and upgrade hook applies them from this image with server-side apply, the way the Istio CRDs are applied from the istioctl image. The tag starts with the Envoy Gateway release (Chart.yaml appVersion) followed by an image revision.

`hw-envoy-gateway.crdImage.registry` <a class="headerlink" href="#helm.hw-envoy-gateway.crdImage.registry" title="Permanent link">#</a> { #helm.hw-envoy-gateway.crdImage.registry }
:   Type `string`, default `""`.
    registry prefix; empty means global._hopsworks.imageRegistry plus the hopsworks project

`hw-envoy-gateway.envoyProxy` <a class="headerlink" href="#helm.hw-envoy-gateway.envoyProxy" title="Permanent link">#</a> { #helm.hw-envoy-gateway.envoyProxy }
:   Type `object`.
    the Envoy data plane image the controller deploys for every Gateway, a mirror of the Docker Hub image envoyproxy/envoy at the same path. The tag is the default of this Envoy Gateway release.

    ??? note "Default"

        ```yaml
        image:
          registry: ''
          repository: envoyproxy/envoy
          tag: distroless-v1.39.1
        ```

`hw-envoy-gateway.envoyProxy.image.registry` <a class="headerlink" href="#helm.hw-envoy-gateway.envoyProxy.image.registry" title="Permanent link">#</a> { #helm.hw-envoy-gateway.envoyProxy.image.registry }
:   Type `string`, default `""`.
    registry prefix; empty means global._hopsworks.imageRegistry

`hw-envoy-gateway.gatewayApiCrds` <a class="headerlink" href="#helm.hw-envoy-gateway.gatewayApiCrds" title="Permanent link">#</a> { #helm.hw-envoy-gateway.gatewayApiCrds }
:   Type `object`, default `{"enabled":true}`.
    the Gateway API CRDs (gateway.networking.k8s.io). Off on a cluster whose platform owns them: OpenShift 4.19 and later (the Ingress Operator manages them and refuses foreign copies) and GKE. The hook then applies the Envoy Gateway CRDs only and checks the Gateway API ones exist.

`hw-envoy-gateway.gatewayClass` <a class="headerlink" href="#helm.hw-envoy-gateway.gatewayClass" title="Permanent link">#</a> { #helm.hw-envoy-gateway.gatewayClass }
:   Type `object`, default `{"controllerName":""}`.
    the GatewayClass this chart creates. Its name is release-prefixed (hopsworkslib.moduleFullname of "envoy-gateway") and the kserve subchart's Gateway refers to it the same way.

`hw-envoy-gateway.gatewayClass.controllerName` <a class="headerlink" href="#helm.hw-envoy-gateway.gatewayClass.controllerName" title="Permanent link">#</a> { #helm.hw-envoy-gateway.gatewayClass.controllerName }
:   Type `string`, default `""`.
    the controller name the GatewayClass and the controller agree on. Empty means gateway.envoyproxy.io/hopsworks-<release namespace>: Envoy Gateway manages every GatewayClass with its controller name, so each release needs its own, distinct from the upstream default as well so that an Envoy Gateway a customer runs for other purposes never programs the Hopsworks class. Immutable on an existing GatewayClass.

`hw-envoy-gateway.hopsworkslib` <a class="headerlink" href="#helm.hw-envoy-gateway.hopsworkslib" title="Permanent link">#</a> { #helm.hw-envoy-gateway.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

</div>

## certgen { #helm-values-hw-envoy-gateway-certgen }

??? example "Defaults as YAML"

    ```yaml
    hw-envoy-gateway:
      certgen:
        imagePullPolicy: IfNotPresent
        nodeSelector: {}
        resources:
          limits:
            cpu: 500m
            memory: 256Mi
          requests:
            cpu: 50m
            memory: 64Mi
        tolerations: []
        ttlSecondsAfterFinished: null
    ```

<div class="hops-values" markdown>

`hw-envoy-gateway.certgen` <a class="headerlink" href="#helm.hw-envoy-gateway.certgen" title="Permanent link">#</a> { #helm.hw-envoy-gateway.certgen }
:   Type `object`.
    the certgen hook, which creates the controller's and the proxies' xDS certificates on install and leaves them alone on upgrade (verified: a repeated upgrade keeps the Secrets' resourceVersion)

    ??? note "Default"

        ```yaml
        imagePullPolicy: IfNotPresent
        nodeSelector: {}
        resources:
          limits:
            cpu: 500m
            memory: 256Mi
          requests:
            cpu: 50m
            memory: 64Mi
        tolerations: []
        ttlSecondsAfterFinished: null
        ```

`hw-envoy-gateway.certgen.imagePullPolicy` <a class="headerlink" href="#helm.hw-envoy-gateway.certgen.imagePullPolicy" title="Permanent link">#</a> { #helm.hw-envoy-gateway.certgen.imagePullPolicy }
:   Type `string`, default `"IfNotPresent"`.
    pull policy of the certgen container; global._hopsworks.imagePullPolicy takes precedence when set

`hw-envoy-gateway.certgen.nodeSelector` <a class="headerlink" href="#helm.hw-envoy-gateway.certgen.nodeSelector" title="Permanent link">#</a> { #helm.hw-envoy-gateway.certgen.nodeSelector }
:   Type `object`, default `{}`.
    nodeSelector of the certgen Job; falls back to global._hopsworks.nodeSelector

`hw-envoy-gateway.certgen.resources` <a class="headerlink" href="#helm.hw-envoy-gateway.certgen.resources" title="Permanent link">#</a> { #helm.hw-envoy-gateway.certgen.resources }
:   Type `object`.
    resources of the certgen container

    ??? note "Default"

        ```yaml
        limits:
          cpu: 500m
          memory: 256Mi
        requests:
          cpu: 50m
          memory: 64Mi
        ```

`hw-envoy-gateway.certgen.tolerations` <a class="headerlink" href="#helm.hw-envoy-gateway.certgen.tolerations" title="Permanent link">#</a> { #helm.hw-envoy-gateway.certgen.tolerations }
:   Type `list`, default `[]`.
    tolerations of the certgen Job; fall back to global._hopsworks.tolerations

`hw-envoy-gateway.certgen.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.hw-envoy-gateway.certgen.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.hw-envoy-gateway.certgen.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    TTL in seconds for the certgen Job. Overrides the global default.

</div>

## cleanupOnUninstall { #helm-values-hw-envoy-gateway-cleanuponuninstall }

??? example "Defaults as YAML"

    ```yaml
    hw-envoy-gateway:
      cleanupOnUninstall:
        deleteCrds: false
        enabled: true
        imagePullPolicy: IfNotPresent
        nodeSelector: {}
        resources:
          limits:
            cpu: 500m
            memory: 256Mi
          requests:
            cpu: 50m
            memory: 64Mi
        tolerations: []
        ttlSecondsAfterFinished: null
    ```

<div class="hops-values" markdown>

`hw-envoy-gateway.cleanupOnUninstall` <a class="headerlink" href="#helm.hw-envoy-gateway.cleanupOnUninstall" title="Permanent link">#</a> { #helm.hw-envoy-gateway.cleanupOnUninstall }
:   Type `object`.
    uninstall cleanup of what the controller leaves behind that Helm never tracked: the Envoy proxy Deployments and Services it created for the Gateways (the controller is deleted with the release and cannot remove them any more), the finalizer it holds on the GatewayClass while Gateways exist, and the certificate Secrets certgen wrote at install time. Runs post-delete only: Argo CD runs pre-delete hooks only from 3.3.

    ??? note "Default"

        ```yaml
        deleteCrds: false
        enabled: true
        imagePullPolicy: IfNotPresent
        nodeSelector: {}
        resources:
          limits:
            cpu: 500m
            memory: 256Mi
          requests:
            cpu: 50m
            memory: 64Mi
        tolerations: []
        ttlSecondsAfterFinished: null
        ```

`hw-envoy-gateway.cleanupOnUninstall.deleteCrds` <a class="headerlink" href="#helm.hw-envoy-gateway.cleanupOnUninstall.deleteCrds" title="Permanent link">#</a> { #helm.hw-envoy-gateway.cleanupOnUninstall.deleteCrds }
:   Type `bool`, default `false`.
    also delete the Envoy Gateway CRDs and, when gatewayApiCrds.enabled and this chart installed them, the Gateway API CRDs. Off by default, which keeps the definitions the way a chart's crds/ directory would, for an Envoy Gateway installed by other means next; the objects stored under them (routes, policies) go with their namespaces.

`hw-envoy-gateway.cleanupOnUninstall.enabled` <a class="headerlink" href="#helm.hw-envoy-gateway.cleanupOnUninstall.enabled" title="Permanent link">#</a> { #helm.hw-envoy-gateway.cleanupOnUninstall.enabled }
:   Type `bool`, default `true`.
    enable the cleanup hook

`hw-envoy-gateway.cleanupOnUninstall.imagePullPolicy` <a class="headerlink" href="#helm.hw-envoy-gateway.cleanupOnUninstall.imagePullPolicy" title="Permanent link">#</a> { #helm.hw-envoy-gateway.cleanupOnUninstall.imagePullPolicy }
:   Type `string`, default `"IfNotPresent"`.
    pull policy of the toolbox image the cleanup Job runs; global._hopsworks.imagePullPolicy takes precedence when set

`hw-envoy-gateway.cleanupOnUninstall.nodeSelector` <a class="headerlink" href="#helm.hw-envoy-gateway.cleanupOnUninstall.nodeSelector" title="Permanent link">#</a> { #helm.hw-envoy-gateway.cleanupOnUninstall.nodeSelector }
:   Type `object`, default `{}`.
    nodeSelector of the cleanup Job; falls back to global._hopsworks.nodeSelector

`hw-envoy-gateway.cleanupOnUninstall.resources` <a class="headerlink" href="#helm.hw-envoy-gateway.cleanupOnUninstall.resources" title="Permanent link">#</a> { #helm.hw-envoy-gateway.cleanupOnUninstall.resources }
:   Type `object`.
    resources of the cleanup Job container

    ??? note "Default"

        ```yaml
        limits:
          cpu: 500m
          memory: 256Mi
        requests:
          cpu: 50m
          memory: 64Mi
        ```

`hw-envoy-gateway.cleanupOnUninstall.tolerations` <a class="headerlink" href="#helm.hw-envoy-gateway.cleanupOnUninstall.tolerations" title="Permanent link">#</a> { #helm.hw-envoy-gateway.cleanupOnUninstall.tolerations }
:   Type `list`, default `[]`.
    tolerations of the cleanup Job; fall back to global._hopsworks.tolerations

`hw-envoy-gateway.cleanupOnUninstall.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.hw-envoy-gateway.cleanupOnUninstall.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.hw-envoy-gateway.cleanupOnUninstall.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    TTL in seconds for the cleanup Job. Overrides the global default.

</div>

## controller { #helm-values-hw-envoy-gateway-controller }

??? example "Defaults as YAML"

    ```yaml
    hw-envoy-gateway:
      controller:
        image:
          registry: ''
          repository: envoyproxy/gateway
          tag: v1.9.2
        imagePullPolicy: IfNotPresent
        logLevel: info
        nodeSelector: {}
        podDisruptionBudget:
          minAvailable: 0
        replicas: 1
        resources:
          limits:
            cpu: '1'
            memory: 1Gi
          requests:
            cpu: 100m
            memory: 256Mi
        serviceAccount:
          annotations: {}
        tolerations: []
    ```

<div class="hops-values" markdown>

`hw-envoy-gateway.controller` <a class="headerlink" href="#helm.hw-envoy-gateway.controller" title="Permanent link">#</a> { #helm.hw-envoy-gateway.controller }
:   Type `object`.
    the Envoy Gateway controller (the envoy-gateway Deployment). It programs the Envoy proxies the kserve subchart's Gateway asks for and runs in the release namespace, watching every namespace, because the HTTPRoutes KServe creates live in the project namespaces.

    ??? note "Default"

        ```yaml
        image:
          registry: ''
          repository: envoyproxy/gateway
          tag: v1.9.2
        imagePullPolicy: IfNotPresent
        logLevel: info
        nodeSelector: {}
        podDisruptionBudget:
          minAvailable: 0
        replicas: 1
        resources:
          limits:
            cpu: '1'
            memory: 1Gi
          requests:
            cpu: 100m
            memory: 256Mi
        serviceAccount:
          annotations: {}
        tolerations: []
        ```

`hw-envoy-gateway.controller.image` <a class="headerlink" href="#helm.hw-envoy-gateway.controller.image" title="Permanent link">#</a> { #helm.hw-envoy-gateway.controller.image }
:   Type `object`, default `{"registry":"","repository":"envoyproxy/gateway","tag":"v1.9.2"}`.
    the controller image, a mirror of the Docker Hub image envoyproxy/gateway under the Hopsworks registry at the same path (docker.hops.works/envoyproxy/gateway). The same image runs the certgen hook and the shutdown-manager sidecar of every Envoy pod. The tag is the Envoy Gateway release (Chart.yaml appVersion).

`hw-envoy-gateway.controller.image.registry` <a class="headerlink" href="#helm.hw-envoy-gateway.controller.image.registry" title="Permanent link">#</a> { #helm.hw-envoy-gateway.controller.image.registry }
:   Type `string`, default `""`.
    registry prefix; empty means global._hopsworks.imageRegistry

`hw-envoy-gateway.controller.imagePullPolicy` <a class="headerlink" href="#helm.hw-envoy-gateway.controller.imagePullPolicy" title="Permanent link">#</a> { #helm.hw-envoy-gateway.controller.imagePullPolicy }
:   Type `string`, default `"IfNotPresent"`.
    pull policy of the controller image; global._hopsworks.imagePullPolicy takes precedence when set

`hw-envoy-gateway.controller.logLevel` <a class="headerlink" href="#helm.hw-envoy-gateway.controller.logLevel" title="Permanent link">#</a> { #helm.hw-envoy-gateway.controller.logLevel }
:   Type `string`, default `"info"`.
    log level of the controller

`hw-envoy-gateway.controller.nodeSelector` <a class="headerlink" href="#helm.hw-envoy-gateway.controller.nodeSelector" title="Permanent link">#</a> { #helm.hw-envoy-gateway.controller.nodeSelector }
:   Type `object`, default `{}`.
    nodeSelector of the controller; falls back to global._hopsworks.nodeSelector

`hw-envoy-gateway.controller.podDisruptionBudget` <a class="headerlink" href="#helm.hw-envoy-gateway.controller.podDisruptionBudget" title="Permanent link">#</a> { #helm.hw-envoy-gateway.controller.podDisruptionBudget }
:   Type `object`, default `{"minAvailable":0}`.
    PodDisruptionBudget of the controller; minAvailable 0 renders none

`hw-envoy-gateway.controller.replicas` <a class="headerlink" href="#helm.hw-envoy-gateway.controller.replicas" title="Permanent link">#</a> { #helm.hw-envoy-gateway.controller.replicas }
:   Type `int`, default `1`.
    replicas of the controller. One is enough: the proxies keep serving while it restarts, and leader election covers more.

`hw-envoy-gateway.controller.resources` <a class="headerlink" href="#helm.hw-envoy-gateway.controller.resources" title="Permanent link">#</a> { #helm.hw-envoy-gateway.controller.resources }
:   Type `object`.
    resources of the controller container

    ??? note "Default"

        ```yaml
        limits:
          cpu: '1'
          memory: 1Gi
        requests:
          cpu: 100m
          memory: 256Mi
        ```

`hw-envoy-gateway.controller.serviceAccount.annotations` <a class="headerlink" href="#helm.hw-envoy-gateway.controller.serviceAccount.annotations" title="Permanent link">#</a> { #helm.hw-envoy-gateway.controller.serviceAccount.annotations }
:   Type `object`, default `{}`.
    annotations of the controller's service account, merged over global._hopsworks.serviceAccountAnnotations

`hw-envoy-gateway.controller.tolerations` <a class="headerlink" href="#helm.hw-envoy-gateway.controller.tolerations" title="Permanent link">#</a> { #helm.hw-envoy-gateway.controller.tolerations }
:   Type `list`, default `[]`.
    tolerations of the controller; fall back to global._hopsworks.tolerations

</div>

## crdInstallJob { #helm-values-hw-envoy-gateway-crdinstalljob }

??? example "Defaults as YAML"

    ```yaml
    hw-envoy-gateway:
      crdInstallJob:
        imagePullPolicy: IfNotPresent
        nodeSelector: {}
        resources:
          limits:
            cpu: 500m
            memory: 256Mi
          requests:
            cpu: 50m
            memory: 64Mi
        tolerations: []
        ttlSecondsAfterFinished: null
    ```

<div class="hops-values" markdown>

`hw-envoy-gateway.crdInstallJob` <a class="headerlink" href="#helm.hw-envoy-gateway.crdInstallJob" title="Permanent link">#</a> { #helm.hw-envoy-gateway.crdInstallJob }
:   Type `object`.
    the pre-install and pre-upgrade hook that applies the CRDs from crdImage. Server-side apply creates or patches as needed, so it is idempotent and safe under Argo CD, where the hook becomes a PreSync on every sync.

    ??? note "Default"

        ```yaml
        imagePullPolicy: IfNotPresent
        nodeSelector: {}
        resources:
          limits:
            cpu: 500m
            memory: 256Mi
          requests:
            cpu: 50m
            memory: 64Mi
        tolerations: []
        ttlSecondsAfterFinished: null
        ```

`hw-envoy-gateway.crdInstallJob.imagePullPolicy` <a class="headerlink" href="#helm.hw-envoy-gateway.crdInstallJob.imagePullPolicy" title="Permanent link">#</a> { #helm.hw-envoy-gateway.crdInstallJob.imagePullPolicy }
:   Type `string`, default `"IfNotPresent"`.
    pull policy of the CRD image; global._hopsworks.imagePullPolicy takes precedence when set

`hw-envoy-gateway.crdInstallJob.nodeSelector` <a class="headerlink" href="#helm.hw-envoy-gateway.crdInstallJob.nodeSelector" title="Permanent link">#</a> { #helm.hw-envoy-gateway.crdInstallJob.nodeSelector }
:   Type `object`, default `{}`.
    nodeSelector of the Job; falls back to global._hopsworks.nodeSelector

`hw-envoy-gateway.crdInstallJob.resources` <a class="headerlink" href="#helm.hw-envoy-gateway.crdInstallJob.resources" title="Permanent link">#</a> { #helm.hw-envoy-gateway.crdInstallJob.resources }
:   Type `object`.
    resources of the Job container

    ??? note "Default"

        ```yaml
        limits:
          cpu: 500m
          memory: 256Mi
        requests:
          cpu: 50m
          memory: 64Mi
        ```

`hw-envoy-gateway.crdInstallJob.tolerations` <a class="headerlink" href="#helm.hw-envoy-gateway.crdInstallJob.tolerations" title="Permanent link">#</a> { #helm.hw-envoy-gateway.crdInstallJob.tolerations }
:   Type `list`, default `[]`.
    tolerations of the Job; fall back to global._hopsworks.tolerations

`hw-envoy-gateway.crdInstallJob.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.hw-envoy-gateway.crdInstallJob.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.hw-envoy-gateway.crdInstallJob.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    TTL in seconds for the CRD install Job. Overrides the global default.

</div>

<!-- END GENERATED VALUES -->
