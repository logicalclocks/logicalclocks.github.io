# Ray values { #helm-values-ray }

Values under `ray` configure the KubeRay operator, which runs the Ray clusters behind Ray jobs and notebooks.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.3.0-alpha-1795867152` (Hopsworks `5.3.0`)._

Deployed according to the first of these values that is set: [`global._hopsworks.ray.enabled`](global.md#helm.global._hopsworks.ray.enabled), [`global._hopsworks.full_platform`](global.md#helm.global._hopsworks.full_platform).

!!! info "Upstream charts"

    - Values under `ray.kuberay-operator` go to [`kuberay-operator` 1.7.3](https://artifacthub.io/packages/helm/kuberay-operator/kuberay-operator/1.7.3) from `https://ray-project.github.io/kuberay-helm/`.

    Only the values Hopsworks sets under `ray.kuberay-operator` are listed on this page.
    Any other value of the chart can be set there too; the link opens its documentation for the version Hopsworks pins.

## General { #helm-values-ray-general }

??? example "Defaults as YAML"

    ```yaml
    ray:
      hopsworkslib: {}
      kuberay-operator:
        batchScheduler:
          enabled: false
          name: ''
        crNamespacedRbacEnable: true
        env: null
        featureGates:
        - enabled: false
          name: RayClusterStatusConditions
        fullnameOverride: kuberay-operator
        image:
          pullPolicy: IfNotPresent
          repository: docker.hops.works/hopsworks/kuberay-operator
          tag: 1.7.3-h1
        leaderElectionEnabled: true
        livenessProbe:
          failureThreshold: 5
          initialDelaySeconds: 10
          periodSeconds: 5
        logging:
          baseDir: ''
          fileEncoder: ''
          fileName: ''
          stdoutEncoder: ''
        nameOverride: kuberay-operator
        podSecurityContext: {}
        rbacEnable: true
        readinessProbe:
          failureThreshold: 5
          initialDelaySeconds: 10
          periodSeconds: 5
        resources:
          limits:
            cpu: 100m
            memory: 512Mi
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          seccompProfile:
            type: RuntimeDefault
        service:
          port: 8080
          type: ClusterIP
        serviceAccount:
          create: true
          name: kuberay-operator
        singleNamespaceInstall: false
    ```

<div class="hops-values" markdown>

`ray` <a class="headerlink" href="#helm.ray" title="Permanent link">#</a> { #helm.ray }
:   Type `object`, default `{}`.
    override ray values

`ray.hopsworkslib` <a class="headerlink" href="#helm.ray.hopsworkslib" title="Permanent link">#</a> { #helm.ray.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`ray.kuberay-operator` <a class="headerlink" href="#helm.ray.kuberay-operator" title="Permanent link">#</a> { #helm.ray.kuberay-operator }
:   Type `object`, passed to the [`kuberay-operator` 1.7.3](https://artifacthub.io/packages/helm/kuberay-operator/kuberay-operator/1.7.3) chart, whose other values are documented there.
    override kuberay-operator values

    ??? note "Default"

        ```yaml
        batchScheduler:
          enabled: false
          name: ''
        crNamespacedRbacEnable: true
        env: null
        featureGates:
        - enabled: false
          name: RayClusterStatusConditions
        fullnameOverride: kuberay-operator
        image:
          pullPolicy: IfNotPresent
          repository: docker.hops.works/hopsworks/kuberay-operator
          tag: 1.7.3-h1
        leaderElectionEnabled: true
        livenessProbe:
          failureThreshold: 5
          initialDelaySeconds: 10
          periodSeconds: 5
        logging:
          baseDir: ''
          fileEncoder: ''
          fileName: ''
          stdoutEncoder: ''
        nameOverride: kuberay-operator
        podSecurityContext: {}
        rbacEnable: true
        readinessProbe:
          failureThreshold: 5
          initialDelaySeconds: 10
          periodSeconds: 5
        resources:
          limits:
            cpu: 100m
            memory: 512Mi
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          seccompProfile:
            type: RuntimeDefault
        service:
          port: 8080
          type: ClusterIP
        serviceAccount:
          create: true
          name: kuberay-operator
        singleNamespaceInstall: false
        ```

</div>

## crdUpgradeJob { #helm-values-ray-crdupgradejob }

??? example "Defaults as YAML"

    ```yaml
    ray:
      crdUpgradeJob:
        enabled: true
        image:
          name: kuberay-crds
          registry: ''
          tag: 1.7.3-h1
        imagePullPolicy: IfNotPresent
        nodeSelector: {}
        resources:
          limits:
            cpu: 200m
            memory: 512Mi
          requests:
            cpu: 50m
            memory: 64Mi
        tolerations: []
        ttlSecondsAfterFinished: null
    ```

<div class="hops-values" markdown>

`ray.crdUpgradeJob` <a class="headerlink" href="#helm.ray.crdUpgradeJob" title="Permanent link">#</a> { #helm.ray.crdUpgradeJob }
:   Type `object`.
    the pre-install and pre-upgrade hook that keeps the KubeRay CRDs current. They ship in the kuberay-operator dependency's crds/, which Helm never touches on upgrade and Helm 3 skips on install for a CRD that already exists, so this Job applies the pinned release's CRDs server-side on every install and upgrade: it creates them in a release that enables Ray on an upgrade, and patches them on a KubeRay bump and on a reinstall over the CRDs an earlier release left behind. It reads them from the kuberay-crds image (`image`), not a hook ConfigMap: Helm stores every hook manifest in the release Secret, which Kubernetes caps at 1 MiB, and the CRDs are 4 MB.

    ??? note "Default"

        ```yaml
        enabled: true
        image:
          name: kuberay-crds
          registry: ''
          tag: 1.7.3-h1
        imagePullPolicy: IfNotPresent
        nodeSelector: {}
        resources:
          limits:
            cpu: 200m
            memory: 512Mi
          requests:
            cpu: 50m
            memory: 64Mi
        tolerations: []
        ttlSecondsAfterFinished: null
        ```

`ray.crdUpgradeJob.enabled` <a class="headerlink" href="#helm.ray.crdUpgradeJob.enabled" title="Permanent link">#</a> { #helm.ray.crdUpgradeJob.enabled }
:   Type `bool`, default `true`.
    apply the pinned KubeRay release's CRDs on install and upgrade

`ray.crdUpgradeJob.image` <a class="headerlink" href="#helm.ray.crdUpgradeJob.image" title="Permanent link">#</a> { #helm.ray.crdUpgradeJob.image }
:   Type `object`, default `{"name":"kuberay-crds","registry":"","tag":"1.7.3-h1"}`.
    the image that carries the CRDs (docker-images kuberay-crds: the files and a static busybox on scratch, no tools), in the directory kuberay-operator-<version>. An init container copies them out and the Job's toolbox container checks every file's sha256 against this chart's files/kuberay-crds.sha256 before applying anything, so the tag must be the build for this chart's KubeRay version.

`ray.crdUpgradeJob.image.name` <a class="headerlink" href="#helm.ray.crdUpgradeJob.image.name" title="Permanent link">#</a> { #helm.ray.crdUpgradeJob.image.name }
:   Type `string`, default `"kuberay-crds"`.
    image name

`ray.crdUpgradeJob.image.registry` <a class="headerlink" href="#helm.ray.crdUpgradeJob.image.registry" title="Permanent link">#</a> { #helm.ray.crdUpgradeJob.image.registry }
:   Type `string`, default `""`.
    registry and repository prefix of the image; empty means global._hopsworks.imageRegistry followed by /hopsworks

`ray.crdUpgradeJob.image.tag` <a class="headerlink" href="#helm.ray.crdUpgradeJob.image.tag" title="Permanent link">#</a> { #helm.ray.crdUpgradeJob.image.tag }
:   Type `string`, default `"1.7.3-h1"`.
    image tag, <kuberay>-h<revision>

`ray.crdUpgradeJob.imagePullPolicy` <a class="headerlink" href="#helm.ray.crdUpgradeJob.imagePullPolicy" title="Permanent link">#</a> { #helm.ray.crdUpgradeJob.imagePullPolicy }
:   Type `string`, default `"IfNotPresent"`.
    pull policy of the Job's toolbox and kuberay-crds images; global._hopsworks.imagePullPolicy takes precedence when set

`ray.crdUpgradeJob.nodeSelector` <a class="headerlink" href="#helm.ray.crdUpgradeJob.nodeSelector" title="Permanent link">#</a> { #helm.ray.crdUpgradeJob.nodeSelector }
:   Type `object`, default `{}`.
    nodeSelector of the Job; falls back to global._hopsworks.nodeSelector

`ray.crdUpgradeJob.resources` <a class="headerlink" href="#helm.ray.crdUpgradeJob.resources" title="Permanent link">#</a> { #helm.ray.crdUpgradeJob.resources }
:   Type `object`.
    resources of the Job container

    ??? note "Default"

        ```yaml
        limits:
          cpu: 200m
          memory: 512Mi
        requests:
          cpu: 50m
          memory: 64Mi
        ```

`ray.crdUpgradeJob.tolerations` <a class="headerlink" href="#helm.ray.crdUpgradeJob.tolerations" title="Permanent link">#</a> { #helm.ray.crdUpgradeJob.tolerations }
:   Type `list`, default `[]`.
    tolerations of the Job; fall back to global._hopsworks.tolerations

`ray.crdUpgradeJob.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.ray.crdUpgradeJob.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.ray.crdUpgradeJob.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    TTL in seconds for the CRD upgrade Job. Overrides the global default.

</div>

<!-- END GENERATED VALUES -->
