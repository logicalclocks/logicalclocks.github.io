# Helm chart values reference

This section lists every value you can configure when deploying Hopsworks with the Hopsworks Helm chart, with one page per top-level key.
It is generated from the `README.md` files of the chart and its subcharts, and for RonDB from the `values.schema.json` of the RonDB chart that Hopsworks pins.
On a released version of the docs it matches the Hopsworks Helm chart for that release; on the development docs it reflects the latest chart published to the development channel.

You set these values in the `values.<cloud>.yaml` file that you pass to `helm install`.
For a guided, end-to-end setup, follow one of the cloud installation guides, such as the [AWS getting started guide][aws-getting-started-with-eks].
Only a small subset of these values is needed for a typical install: "Common values" below lists the ones the cloud installation guides set, and the pages are the exhaustive reference.

"All values" lists the pages.
Each page states when its subchart is deployed: when the condition names several values, Helm uses the first one that is set.
"Upstream charts" are the charts a subchart installs from other Helm repositories, and each link opens a chart's documentation for the version Hopsworks pins.
A page lists only the values Hopsworks sets for its upstream charts, except the RonDB page, which lists all of the RonDB chart's values.
A default is the value Hopsworks deploys: the root chart's settings for a subchart are applied over the subchart's own defaults.
Every value has its own link (the `#` next to its key), and each section has its defaults as a values file under "Defaults as YAML".

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.2.0-alpha-1791802682` (Hopsworks `5.2.0`)._

## Common values { #helm-values-common }

| Value | What it sets |
| --- | --- |
| [`global._hopsworks.cloudProvider`](global.md#helm.global._hopsworks.cloudProvider) | The cloud the cluster runs on; HopsFS, Consul and Hopsworks configure themselves from it. |
| [`global._hopsworks.storageClassName`](global.md#helm.global._hopsworks.storageClassName) | The storage class of every persistent volume. |
| [`global._hopsworks.imageRegistry`](global.md#helm.global._hopsworks.imageRegistry) | The registry the Hopsworks images are pulled from. |
| [`global._hopsworks.imagePullSecrets`](global.md#helm.global._hopsworks.imagePullSecrets) | The pull secrets for that registry. |
| [`global._hopsworks.managedDockerRegistery`](global.md#helm.global._hopsworks.managedDockerRegistery) | Use the cloud provider's container registry for the images Hopsworks builds for users. |
| [`global._hopsworks.managedObjectStorage`](global.md#helm.global._hopsworks.managedObjectStorage) | Use a cloud bucket for HopsFS data and for the RonDB and OpenSearch backups. |
| [`global._hopsworks.minio.enabled`](global.md#helm.global._hopsworks.minio.enabled) | Deploy MinIO in the cluster; turn it off when a cloud bucket is used. |
| [`global._hopsworks.externalLoadBalancers.enabled`](global.md#helm.global._hopsworks.externalLoadBalancers.enabled) | Expose services through LoadBalancer Services. |
| [`hopsworks.ingress.host`](hopsworks.md#helm.hopsworks.ingress.host) | The host name of the Hopsworks UI and API. |
| [`hopsworks.ingress.ingressClassName`](hopsworks.md#helm.hopsworks.ingress.ingressClassName) | The ingress controller that serves it. |
| [`hopsworks.velero.backup.enabled`](hopsworks.md#helm.hopsworks.velero.backup.enabled) | Back up Kubernetes resources with Velero, which needs its own install. |
| [`rondb.rondb.clusterSize`](rondb.md#helm.rondb.rondb.clusterSize) | The size of the RonDB cluster: data replicas, node groups, MySQL and REST API servers. |

## All values { #helm-values-pages }

| Values | Upstream charts | Keys |
| --- | --- | --- |
| [`global`][helm-values-global] |  | 145 |
| [`airflow`][helm-values-airflow] |  | 151 |
| [`arrowflight`][helm-values-arrowflight] |  | 46 |
| [`certs-operator`][helm-values-certs-operator] |  | 29 |
| [`consul`][helm-values-consul] | [`consul` 1.8.16](https://artifacthub.io/packages/helm/hashicorp/consul/1.8.16) | 24 |
| [`docker-registry`][helm-values-docker-registry] |  | 90 |
| [`grafana`][helm-values-grafana] | [`grafana` 7.0.17](https://artifacthub.io/packages/helm/grafana/grafana/7.0.17) | 7 |
| [`hive`][helm-values-hive] |  | 78 |
| [`hopsfs`][helm-values-hopsfs] |  | 221 |
| [`hopsfs-csi`][helm-values-hopsfs-csi] |  | 29 |
| [`hopsworks`][helm-values-hopsworks] |  | 936 |
| [`hw-kueue`][helm-values-hw-kueue] | [`kueue` 0.12.2](https://github.com/kubernetes-sigs/kueue/blob/v0.12.2/charts/kueue/README.md) | 94 |
| [`hw-kyverno`][helm-values-hw-kyverno] |  | 58 |
| [`judge`][helm-values-judge] |  | 23 |
| [`kafka`][helm-values-kafka] | [`strimzi-kafka-operator` 1.2.0](https://artifacthub.io/packages/helm/strimzi/strimzi-kafka-operator/1.2.0) | 102 |
| [`kserve`][helm-values-kserve] |  | 269 |
| [`minio`][helm-values-minio] |  | 42 |
| [`olk`][helm-values-olk] | [`prometheus-elasticsearch-exporter` 5.8.0](https://artifacthub.io/packages/helm/prometheus-community/prometheus-elasticsearch-exporter/5.8.0) | 164 |
| [`onlinefs`][helm-values-onlinefs] |  | 93 |
| [`prometheus`][helm-values-prometheus] | [`prometheus` 25.20.2](https://artifacthub.io/packages/helm/prometheus-community/prometheus/25.20.2), [`prometheus-adapter` 4.11.0](https://artifacthub.io/packages/helm/prometheus-community/prometheus-adapter/4.11.0) | 9 |
| [`ray`][helm-values-ray] | [`kuberay-operator` 1.4.0](https://artifacthub.io/packages/helm/kuberay-operator/kuberay-operator/1.4.0) | 2 |
| [`rondb`][helm-values-rondb] | [`rondb` 26.2.21](https://github.com/logicalclocks/rondb-helm/blob/v26.2.21/values.schema.json) | 464 |
| [`spark`][helm-values-spark] | [`spark-operator` 2.5.1](https://github.com/kubeflow/spark-operator/blob/v2.5.1/charts/spark-operator-chart/README.md) | 160 |
| [`superset`][helm-values-superset] | [`mysql` 12.3.5](https://artifacthub.io/packages/helm/bitnami/mysql/12.3.5), [`superset` 0.15.0](https://artifacthub.io/packages/helm/superset/superset/0.15.0) | 25 |
| [`trino`][helm-values-trino] | [`trino` 1.41.0](https://artifacthub.io/packages/helm/trino/trino/1.41.0) | 38 |
| [`vpa`][helm-values-vpa] |  | 18 |

## Other values { #helm-values-other }

??? example "Defaults as YAML"

    ```yaml
    hopsworkslib: {}
    hw-keda:
      cleanupOnUninstall:
        deleteCrds: true
        enabled: true
        finalizeTimeoutSeconds: 120
        imagePullPolicy: IfNotPresent
        nodeSelector: {}
        resources:
          limits:
            cpu: 200m
            memory: 256Mi
          requests:
            cpu: 50m
            memory: 64Mi
        tolerations: []
        ttlSecondsAfterFinished: null
      crdUpgradeJob:
        enabled: true
        imagePullPolicy: IfNotPresent
        nodeSelector: {}
        resources:
          limits:
            cpu: 200m
            memory: 256Mi
          requests:
            cpu: 50m
            memory: 64Mi
        tolerations: []
        ttlSecondsAfterFinished: null
      hopsworkslib: {}
      keda:
        certificates:
          autoGenerated: true
          secretName: kedaorg-certs
        crds:
          install: false
        image:
          keda:
            registry: docker.hops.works/ghcr.io
            repository: kedacore/keda
          metricsApiServer:
            registry: docker.hops.works/ghcr.io
            repository: kedacore/keda-metrics-apiserver
          pullPolicy: IfNotPresent
          webhooks:
            registry: docker.hops.works/ghcr.io
            repository: kedacore/keda-admission-webhooks
        networkPolicy:
          enabled: false
        podAnnotations:
          keda:
            prometheus.io/path: /metrics
            prometheus.io/port: '8080'
            prometheus.io/scrape: 'true'
        prometheus:
          operator:
            enabled: true
            port: 8080
        watchNamespace: ''
      keda-add-ons-http:
        crds:
          install: false
        images:
          interceptor: docker.hops.works/ghcr.io/kedacore/http-add-on-interceptor
          operator: docker.hops.works/ghcr.io/kedacore/http-add-on-operator
          scaler: docker.hops.works/ghcr.io/kedacore/http-add-on-scaler
        interceptor:
          pullPolicy: IfNotPresent
          readinessTimeout: 600s
          replicas:
            max: 10
            min: 1
          requestTimeout: 600s
          resources:
            limits:
              cpu: '1'
              memory: 256Mi
            requests:
              cpu: 250m
              memory: 64Mi
          responseHeaderTimeout: 600s
        operator:
          pullPolicy: IfNotPresent
        podSecurityContext:
          fsGroup: 1000
          runAsNonRoot: true
          seccompProfile:
            type: RuntimeDefault
          supplementalGroups:
          - 1000
        scaler:
          pullPolicy: IfNotPresent
          replicas: 1
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
    ```

<div class="hops-values" markdown>

`hopsworkslib` <a class="headerlink" href="#helm.hopsworkslib" title="Permanent link">#</a> { #helm.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`hw-keda` <a class="headerlink" href="#helm.hw-keda" title="Permanent link">#</a> { #helm.hw-keda }
:   Type `object`, default `{}`.
    override hw-keda values

`hw-keda.cleanupOnUninstall` <a class="headerlink" href="#helm.hw-keda.cleanupOnUninstall" title="Permanent link">#</a> { #helm.hw-keda.cleanupOnUninstall }
:   Type `object`.
    uninstall cleanup of what KEDA leaves behind that Helm never tracked. The keda.sh custom resources KServe and Hopsworks created in the project namespaces carry a finalizer only the operator can clear, and Helm deletes the operator before the CRDs, so without this hook every keda.sh CRD stays Terminating, the next install fails on it, and an uninstall that waits for deletion (helm's wait flag, Argo CD) never finishes. It runs pre-delete (deleting the custom resources while the operators can still finalize them) and post-delete (the operator's runtime TLS Secret, leftovers).

    ??? note "Default"

        ```yaml
        deleteCrds: true
        enabled: true
        finalizeTimeoutSeconds: 120
        imagePullPolicy: IfNotPresent
        nodeSelector: {}
        resources:
          limits:
            cpu: 200m
            memory: 256Mi
          requests:
            cpu: 50m
            memory: 64Mi
        tolerations: []
        ttlSecondsAfterFinished: null
        ```

`hw-keda.cleanupOnUninstall.deleteCrds` <a class="headerlink" href="#helm.hw-keda.cleanupOnUninstall.deleteCrds" title="Permanent link">#</a> { #helm.hw-keda.cleanupOnUninstall.deleteCrds }
:   Type `bool`, default `true`.
    also delete the keda.sh, http.keda.sh and eventing.keda.sh CRDs in the post-delete pass. They ship in crds/, which Helm never deletes, so without this an uninstall leaves the CRD definitions on the cluster. Only the definitions: both passes delete every object of those kinds first, whatever this is set to, since objects left under a finalizer with no operator block the CRDs. Off to keep the definitions for a KEDA installed by other means next; the Hopsworks backend recreates its ScaledObjects when a deployment starts

`hw-keda.cleanupOnUninstall.enabled` <a class="headerlink" href="#helm.hw-keda.cleanupOnUninstall.enabled" title="Permanent link">#</a> { #helm.hw-keda.cleanupOnUninstall.enabled }
:   Type `bool`, default `true`.
    enable the KEDA cleanup hook, which runs before the release's resources are deleted (deleting the keda.sh custom resources while their operators can still finalize them, so the CRDs are not left Terminating and an uninstall that waits for deletion, with helm's wait flag or under Argo CD, finishes) and again after (the operator's runtime TLS Secret, anything created in between)

`hw-keda.cleanupOnUninstall.finalizeTimeoutSeconds` <a class="headerlink" href="#helm.hw-keda.cleanupOnUninstall.finalizeTimeoutSeconds" title="Permanent link">#</a> { #helm.hw-keda.cleanupOnUninstall.finalizeTimeoutSeconds }
:   Type `int`, default `120`.
    seconds the pre-delete pass waits for the operators to finalize the deleted custom resources before clearing the finalizers itself

`hw-keda.cleanupOnUninstall.imagePullPolicy` <a class="headerlink" href="#helm.hw-keda.cleanupOnUninstall.imagePullPolicy" title="Permanent link">#</a> { #helm.hw-keda.cleanupOnUninstall.imagePullPolicy }
:   Type `string`, default `"IfNotPresent"`.
    pull policy of the toolbox image the cleanup Job runs; global._hopsworks.imagePullPolicy takes precedence when set

`hw-keda.cleanupOnUninstall.nodeSelector` <a class="headerlink" href="#helm.hw-keda.cleanupOnUninstall.nodeSelector" title="Permanent link">#</a> { #helm.hw-keda.cleanupOnUninstall.nodeSelector }
:   Type `object`, default `{}`.
    nodeSelector of the cleanup Job; falls back to global._hopsworks.nodeSelector

`hw-keda.cleanupOnUninstall.resources` <a class="headerlink" href="#helm.hw-keda.cleanupOnUninstall.resources" title="Permanent link">#</a> { #helm.hw-keda.cleanupOnUninstall.resources }
:   Type `object`.
    resources of the cleanup Job container. kubectl fetches each shipped CRD by name (the biggest, scaledjobs.keda.sh, is 668 KB) and lists the objects under it, never the whole CRD list

    ??? note "Default"

        ```yaml
        limits:
          cpu: 200m
          memory: 256Mi
        requests:
          cpu: 50m
          memory: 64Mi
        ```

`hw-keda.cleanupOnUninstall.tolerations` <a class="headerlink" href="#helm.hw-keda.cleanupOnUninstall.tolerations" title="Permanent link">#</a> { #helm.hw-keda.cleanupOnUninstall.tolerations }
:   Type `list`, default `[]`.
    tolerations of the cleanup Job; fall back to global._hopsworks.tolerations

`hw-keda.cleanupOnUninstall.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.hw-keda.cleanupOnUninstall.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.hw-keda.cleanupOnUninstall.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    TTL in seconds for the cleanup Job. Overrides the global default.

`hw-keda.crdUpgradeJob` <a class="headerlink" href="#helm.hw-keda.crdUpgradeJob" title="Permanent link">#</a> { #helm.hw-keda.crdUpgradeJob }
:   Type `object`.
    the pre-upgrade hook that keeps the KEDA and HTTP add-on CRDs current. They ship in crds/ rather than as templates (the ScaledJob CRD alone is 670 KB, which would put the Helm release secret over its 1 MiB limit), and Helm only creates crds/ on install and never touches it on upgrade, so this Job applies the same CRD files server-side on every upgrade, creating them on a release upgraded from a chart without this subchart and patching them on a KEDA bump.

    ??? note "Default"

        ```yaml
        enabled: true
        imagePullPolicy: IfNotPresent
        nodeSelector: {}
        resources:
          limits:
            cpu: 200m
            memory: 256Mi
          requests:
            cpu: 50m
            memory: 64Mi
        tolerations: []
        ttlSecondsAfterFinished: null
        ```

`hw-keda.crdUpgradeJob.enabled` <a class="headerlink" href="#helm.hw-keda.crdUpgradeJob.enabled" title="Permanent link">#</a> { #helm.hw-keda.crdUpgradeJob.enabled }
:   Type `bool`, default `true`.
    apply the shipped CRDs on upgrade

`hw-keda.crdUpgradeJob.imagePullPolicy` <a class="headerlink" href="#helm.hw-keda.crdUpgradeJob.imagePullPolicy" title="Permanent link">#</a> { #helm.hw-keda.crdUpgradeJob.imagePullPolicy }
:   Type `string`, default `"IfNotPresent"`.
    pull policy of the toolbox image the Job runs; global._hopsworks.imagePullPolicy takes precedence when set

`hw-keda.crdUpgradeJob.nodeSelector` <a class="headerlink" href="#helm.hw-keda.crdUpgradeJob.nodeSelector" title="Permanent link">#</a> { #helm.hw-keda.crdUpgradeJob.nodeSelector }
:   Type `object`, default `{}`.
    nodeSelector of the Job; falls back to global._hopsworks.nodeSelector

`hw-keda.crdUpgradeJob.resources` <a class="headerlink" href="#helm.hw-keda.crdUpgradeJob.resources" title="Permanent link">#</a> { #helm.hw-keda.crdUpgradeJob.resources }
:   Type `object`.
    resources of the Job container

    ??? note "Default"

        ```yaml
        limits:
          cpu: 200m
          memory: 256Mi
        requests:
          cpu: 50m
          memory: 64Mi
        ```

`hw-keda.crdUpgradeJob.tolerations` <a class="headerlink" href="#helm.hw-keda.crdUpgradeJob.tolerations" title="Permanent link">#</a> { #helm.hw-keda.crdUpgradeJob.tolerations }
:   Type `list`, default `[]`.
    tolerations of the Job; fall back to global._hopsworks.tolerations

`hw-keda.crdUpgradeJob.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.hw-keda.crdUpgradeJob.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.hw-keda.crdUpgradeJob.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    TTL in seconds for the CRD upgrade Job. Overrides the global default.

`hw-keda.hopsworkslib` <a class="headerlink" href="#helm.hw-keda.hopsworkslib" title="Permanent link">#</a> { #helm.hw-keda.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`hw-keda.keda` <a class="headerlink" href="#helm.hw-keda.keda" title="Permanent link">#</a> { #helm.hw-keda.keda }
:   Type `object`.
    override keda values. Everything not restated here is the upstream default: <https://github.com/kedacore/charts/blob/main/keda/values.yaml>

    ??? note "Default"

        ```yaml
        certificates:
          autoGenerated: true
          secretName: kedaorg-certs
        crds:
          install: false
        image:
          keda:
            registry: docker.hops.works/ghcr.io
            repository: kedacore/keda
          metricsApiServer:
            registry: docker.hops.works/ghcr.io
            repository: kedacore/keda-metrics-apiserver
          pullPolicy: IfNotPresent
          webhooks:
            registry: docker.hops.works/ghcr.io
            repository: kedacore/keda-admission-webhooks
        networkPolicy:
          enabled: false
        podAnnotations:
          keda:
            prometheus.io/path: /metrics
            prometheus.io/port: '8080'
            prometheus.io/scrape: 'true'
        prometheus:
          operator:
            enabled: true
            port: 8080
        watchNamespace: ''
        ```

`hw-keda.keda-add-ons-http` <a class="headerlink" href="#helm.hw-keda.keda-add-ons-http" title="Permanent link">#</a> { #helm.hw-keda.keda-add-ons-http }
:   Type `object`.
    override keda-add-ons-http values (the KEDA HTTP add-on, HWORKS-3113, always installed with KEDA). Everything not restated here is the upstream default: <https://github.com/kedacore/charts/blob/main/http-add-on/values.yaml>

    ??? note "Default"

        ```yaml
        crds:
          install: false
        images:
          interceptor: docker.hops.works/ghcr.io/kedacore/http-add-on-interceptor
          operator: docker.hops.works/ghcr.io/kedacore/http-add-on-operator
          scaler: docker.hops.works/ghcr.io/kedacore/http-add-on-scaler
        interceptor:
          pullPolicy: IfNotPresent
          readinessTimeout: 600s
          replicas:
            max: 10
            min: 1
          requestTimeout: 600s
          resources:
            limits:
              cpu: '1'
              memory: 256Mi
            requests:
              cpu: 250m
              memory: 64Mi
          responseHeaderTimeout: 600s
        operator:
          pullPolicy: IfNotPresent
        podSecurityContext:
          fsGroup: 1000
          runAsNonRoot: true
          seccompProfile:
            type: RuntimeDefault
          supplementalGroups:
          - 1000
        scaler:
          pullPolicy: IfNotPresent
          replicas: 1
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
        ```

</div>

<!-- END GENERATED VALUES -->
