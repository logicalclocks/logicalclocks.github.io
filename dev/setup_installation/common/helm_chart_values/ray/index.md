# Ray values { #helm-values-ray }

Values under `ray` configure the KubeRay operator, which runs the Ray clusters behind Ray jobs and notebooks.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.2.0-alpha-1791370120` (Hopsworks `5.2.0`)._

Deployed according to the first of these values that is set: [`global._hopsworks.ray.enabled`](global.md#helm.global._hopsworks.ray.enabled), [`global._hopsworks.full_platform`](global.md#helm.global._hopsworks.full_platform).

!!! info "Upstream charts"

    - Values under `ray.kuberay-operator` go to [`kuberay-operator` 1.4.0](https://artifacthub.io/packages/helm/kuberay-operator/kuberay-operator/1.4.0) from `https://ray-project.github.io/kuberay-helm/`.

    Only the values Hopsworks sets under `ray.kuberay-operator` are listed on this page.
    Any other value of the chart can be set there too; the link opens its documentation for the version Hopsworks pins.

??? example "Defaults as YAML"

    ```yaml
    ray:
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
          tag: 1.4.0-h1
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

`ray.kuberay-operator` <a class="headerlink" href="#helm.ray.kuberay-operator" title="Permanent link">#</a> { #helm.ray.kuberay-operator }
:   Type `object`, passed to the [`kuberay-operator` 1.4.0](https://artifacthub.io/packages/helm/kuberay-operator/kuberay-operator/1.4.0) chart, whose other values are documented there.
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
          tag: 1.4.0-h1
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

<!-- END GENERATED VALUES -->
