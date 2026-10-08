# Kueue values { #helm-values-hw-kueue }

Values under `hw-kueue` configure Kueue, the job queueing controller, and the queues Hopsworks schedules jobs with.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.2.0-alpha-1791469719` (Hopsworks `5.2.0`)._

Deployed according to the first of these values that is set: [`global._hopsworks.kueue.enabled`](global.md#helm.global._hopsworks.kueue.enabled), [`global._hopsworks.full_platform`](global.md#helm.global._hopsworks.full_platform).

!!! info "Upstream charts"

    - Values under `hw-kueue.kueue` go to [`kueue` 0.12.2](https://github.com/kubernetes-sigs/kueue/blob/v0.12.2/charts/kueue/README.md) from `https://repo.hops.works/master/kueue/`.

    Only the values Hopsworks sets under `hw-kueue.kueue` are listed on this page.
    Any other value of the chart can be set there too; the link opens its documentation for the version Hopsworks pins.

## General { #helm-values-hw-kueue-general }

??? example "Defaults as YAML"

    ```yaml
    hw-kueue:
      fullnameOverride: kueue
      hopsworkslib: {}
      imagePullPolicy: Always
      kueue:
        controllerManager:
          featureGates:
          - enabled: false
            name: TopologyAwareScheduling
          imagePullSecrets: []
          livenessProbe:
            failureThreshold: 3
            initialDelaySeconds: 15
            periodSeconds: 20
            successThreshold: 1
            timeoutSeconds: 1
          manager:
            containerSecurityContext:
              allowPrivilegeEscalation: false
              capabilities:
                drop:
                - ALL
            image:
              pullPolicy: Always
              repository: docker.hops.works/registry.k8s.io/kueue/kueue
            podAnnotations: {}
            podSecurityContext:
              runAsNonRoot: true
              seccompProfile:
                type: RuntimeDefault
            resources:
              limits:
                cpu: '2'
                memory: 512Mi
              requests:
                cpu: 500m
                memory: 512Mi
          podDisruptionBudget:
            enabled: false
            minAvailable: 1
          readinessProbe:
            failureThreshold: 3
            initialDelaySeconds: 5
            periodSeconds: 10
            successThreshold: 1
            timeoutSeconds: 1
          replicas: 1
          topologySpreadConstraints: []
        enableCertManager: false
        enableKueueViz: false
        enablePrometheus: false
        enableVisibilityAPF: false
        enableVisibilityServerAuth: true
        fullnameOverride: kueue
        kubernetesClusterDomain: cluster.local
        metrics:
          prometheusNamespace: monitoring
          serviceMonitor:
            tlsConfig:
              insecureSkipVerify: true
        metricsService:
          annotations: {}
          ports:
          - name: metrics
            port: 8443
            protocol: TCP
            targetPort: 8443
          type: ClusterIP
        nameOverride: kueue
        webhookService:
          ipDualStack:
            enabled: false
            ipFamilies:
            - IPv6
            - IPv4
            ipFamilyPolicy: PreferDualStack
          ports:
          - port: 443
            protocol: TCP
            targetPort: 9443
          type: ClusterIP
      nameOverride: kueue
      resourceFlavours:
      - annotations: {}
        labels: {}
        name: default-flavor
        spec:
          nodeLabels:
            cloud.provider.com/region: europe
          nodeTaints: {}
          tolerations: {}
          topologyName: default
      topologies:
      - levels:
        - nodeLabel: cloud.provider.com/region
        - nodeLabel: cloud.provider.com/zone
        - nodeLabel: kubernetes.io/hostname
        name: default
    ```

<div class="hops-values" markdown>

`hw-kueue` <a class="headerlink" href="#helm.hw-kueue" title="Permanent link">#</a> { #helm.hw-kueue }
:   Type `object`, default `{}`.
    override hw-kueue values

`hw-kueue.fullnameOverride` <a class="headerlink" href="#helm.hw-kueue.fullnameOverride" title="Permanent link">#</a> { #helm.hw-kueue.fullnameOverride }
:   Type `string`, default `"kueue"`.

`hw-kueue.hopsworkslib` <a class="headerlink" href="#helm.hw-kueue.hopsworkslib" title="Permanent link">#</a> { #helm.hw-kueue.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`hw-kueue.imagePullPolicy` <a class="headerlink" href="#helm.hw-kueue.imagePullPolicy" title="Permanent link">#</a> { #helm.hw-kueue.imagePullPolicy }
:   Type `string`, default `"Always"`.

`hw-kueue.kueue` <a class="headerlink" href="#helm.hw-kueue.kueue" title="Permanent link">#</a> { #helm.hw-kueue.kueue }
:   Type `object`, passed to the [`kueue` 0.12.2](https://github.com/kubernetes-sigs/kueue/blob/v0.12.2/charts/kueue/README.md) chart, whose other values are documented there.
    override kueue values

    ??? note "Default"

        ```yaml
        controllerManager:
          featureGates:
          - enabled: false
            name: TopologyAwareScheduling
          imagePullSecrets: []
          livenessProbe:
            failureThreshold: 3
            initialDelaySeconds: 15
            periodSeconds: 20
            successThreshold: 1
            timeoutSeconds: 1
          manager:
            containerSecurityContext:
              allowPrivilegeEscalation: false
              capabilities:
                drop:
                - ALL
            image:
              pullPolicy: Always
              repository: docker.hops.works/registry.k8s.io/kueue/kueue
            podAnnotations: {}
            podSecurityContext:
              runAsNonRoot: true
              seccompProfile:
                type: RuntimeDefault
            resources:
              limits:
                cpu: '2'
                memory: 512Mi
              requests:
                cpu: 500m
                memory: 512Mi
          podDisruptionBudget:
            enabled: false
            minAvailable: 1
          readinessProbe:
            failureThreshold: 3
            initialDelaySeconds: 5
            periodSeconds: 10
            successThreshold: 1
            timeoutSeconds: 1
          replicas: 1
          topologySpreadConstraints: []
        enableCertManager: false
        enableKueueViz: false
        enablePrometheus: false
        enableVisibilityAPF: false
        enableVisibilityServerAuth: true
        fullnameOverride: kueue
        kubernetesClusterDomain: cluster.local
        metrics:
          prometheusNamespace: monitoring
          serviceMonitor:
            tlsConfig:
              insecureSkipVerify: true
        metricsService:
          annotations: {}
          ports:
          - name: metrics
            port: 8443
            protocol: TCP
            targetPort: 8443
          type: ClusterIP
        nameOverride: kueue
        webhookService:
          ipDualStack:
            enabled: false
            ipFamilies:
            - IPv6
            - IPv4
            ipFamilyPolicy: PreferDualStack
          ports:
          - port: 443
            protocol: TCP
            targetPort: 9443
          type: ClusterIP
        ```

`hw-kueue.nameOverride` <a class="headerlink" href="#helm.hw-kueue.nameOverride" title="Permanent link">#</a> { #helm.hw-kueue.nameOverride }
:   Type `string`, default `"kueue"`.

`hw-kueue.resourceFlavours` <a class="headerlink" href="#helm.hw-kueue.resourceFlavours" title="Permanent link">#</a> { #helm.hw-kueue.resourceFlavours }
:   Type `list`.
    List of ResourceFlavors

    ??? note "Default"

        ```yaml
        - annotations: {}
          labels: {}
          name: default-flavor
          spec:
            nodeLabels:
              cloud.provider.com/region: europe
            nodeTaints: {}
            tolerations: {}
            topologyName: default
        ```

`hw-kueue.topologies[0].levels[0].nodeLabel` <a class="headerlink" href="#helm.hw-kueue.topologies.0.levels.0.nodeLabel" title="Permanent link">#</a> { #helm.hw-kueue.topologies.0.levels.0.nodeLabel }
:   Type `string`, default `"cloud.provider.com/region"`.

`hw-kueue.topologies[0].levels[1].nodeLabel` <a class="headerlink" href="#helm.hw-kueue.topologies.0.levels.1.nodeLabel" title="Permanent link">#</a> { #helm.hw-kueue.topologies.0.levels.1.nodeLabel }
:   Type `string`, default `"cloud.provider.com/zone"`.

`hw-kueue.topologies[0].levels[2].nodeLabel` <a class="headerlink" href="#helm.hw-kueue.topologies.0.levels.2.nodeLabel" title="Permanent link">#</a> { #helm.hw-kueue.topologies.0.levels.2.nodeLabel }
:   Type `string`, default `"kubernetes.io/hostname"`.

`hw-kueue.topologies[0].name` <a class="headerlink" href="#helm.hw-kueue.topologies.0.name" title="Permanent link">#</a> { #helm.hw-kueue.topologies.0.name }
:   Type `string`, default `"default"`.

</div>

## clusterQueues { #helm-values-hw-kueue-clusterqueues }

??? example "Defaults as YAML"

    ```yaml
    hw-kueue:
      clusterQueues:
      - annotations: {}
        labels: {}
        name: other
        spec:
          cohort: cluster
          fairSharing:
            weight: '1'
          namespaceSelector: {}
          queueingStrategy: BestEffortFIFO
          resourceGroups:
          - coveredResources:
            - cpu
            - memory
            - pods
            - nvidia.com/gpu
            flavors:
            - name: default-flavor
              resources:
              - name: cpu
                nominalQuota: 0
              - name: memory
                nominalQuota: 0
              - name: pods
                nominalQuota: 0
              - name: nvidia.com/gpu
                nominalQuota: 0
    ```

<div class="hops-values" markdown>

`hw-kueue.clusterQueues[0].annotations` <a class="headerlink" href="#helm.hw-kueue.clusterQueues.0.annotations" title="Permanent link">#</a> { #helm.hw-kueue.clusterQueues.0.annotations }
:   Type `object`, default `{}`.

`hw-kueue.clusterQueues[0].labels` <a class="headerlink" href="#helm.hw-kueue.clusterQueues.0.labels" title="Permanent link">#</a> { #helm.hw-kueue.clusterQueues.0.labels }
:   Type `object`, default `{}`.

`hw-kueue.clusterQueues[0].name` <a class="headerlink" href="#helm.hw-kueue.clusterQueues.0.name" title="Permanent link">#</a> { #helm.hw-kueue.clusterQueues.0.name }
:   Type `string`, default `"other"`.

`hw-kueue.clusterQueues[0].spec.cohort` <a class="headerlink" href="#helm.hw-kueue.clusterQueues.0.spec.cohort" title="Permanent link">#</a> { #helm.hw-kueue.clusterQueues.0.spec.cohort }
:   Type `string`, default `"cluster"`.

`hw-kueue.clusterQueues[0].spec.fairSharing.weight` <a class="headerlink" href="#helm.hw-kueue.clusterQueues.0.spec.fairSharing.weight" title="Permanent link">#</a> { #helm.hw-kueue.clusterQueues.0.spec.fairSharing.weight }
:   Type `string`, default `"1"`.

`hw-kueue.clusterQueues[0].spec.namespaceSelector` <a class="headerlink" href="#helm.hw-kueue.clusterQueues.0.spec.namespaceSelector" title="Permanent link">#</a> { #helm.hw-kueue.clusterQueues.0.spec.namespaceSelector }
:   Type `object`, default `{}`.

`hw-kueue.clusterQueues[0].spec.queueingStrategy` <a class="headerlink" href="#helm.hw-kueue.clusterQueues.0.spec.queueingStrategy" title="Permanent link">#</a> { #helm.hw-kueue.clusterQueues.0.spec.queueingStrategy }
:   Type `string`, default `"BestEffortFIFO"`.

`hw-kueue.clusterQueues[0].spec.resourceGroups[0].coveredResources[0]` <a class="headerlink" href="#helm.hw-kueue.clusterQueues.0.spec.resourceGroups.0.coveredResources.0" title="Permanent link">#</a> { #helm.hw-kueue.clusterQueues.0.spec.resourceGroups.0.coveredResources.0 }
:   Type `string`, default `"cpu"`.

`hw-kueue.clusterQueues[0].spec.resourceGroups[0].coveredResources[1]` <a class="headerlink" href="#helm.hw-kueue.clusterQueues.0.spec.resourceGroups.0.coveredResources.1" title="Permanent link">#</a> { #helm.hw-kueue.clusterQueues.0.spec.resourceGroups.0.coveredResources.1 }
:   Type `string`, default `"memory"`.

`hw-kueue.clusterQueues[0].spec.resourceGroups[0].coveredResources[2]` <a class="headerlink" href="#helm.hw-kueue.clusterQueues.0.spec.resourceGroups.0.coveredResources.2" title="Permanent link">#</a> { #helm.hw-kueue.clusterQueues.0.spec.resourceGroups.0.coveredResources.2 }
:   Type `string`, default `"pods"`.

`hw-kueue.clusterQueues[0].spec.resourceGroups[0].coveredResources[3]` <a class="headerlink" href="#helm.hw-kueue.clusterQueues.0.spec.resourceGroups.0.coveredResources.3" title="Permanent link">#</a> { #helm.hw-kueue.clusterQueues.0.spec.resourceGroups.0.coveredResources.3 }
:   Type `string`, default `"nvidia.com/gpu"`.

`hw-kueue.clusterQueues[0].spec.resourceGroups[0].flavors[0].name` <a class="headerlink" href="#helm.hw-kueue.clusterQueues.0.spec.resourceGroups.0.flavors.0.name" title="Permanent link">#</a> { #helm.hw-kueue.clusterQueues.0.spec.resourceGroups.0.flavors.0.name }
:   Type `string`, default `"default-flavor"`.

`hw-kueue.clusterQueues[0].spec.resourceGroups[0].flavors[0].resources[0].name` <a class="headerlink" href="#helm.hw-kueue.clusterQueues.0.spec.resourceGroups.0.flavors.0.resources.0.name" title="Permanent link">#</a> { #helm.hw-kueue.clusterQueues.0.spec.resourceGroups.0.flavors.0.resources.0.name }
:   Type `string`, default `"cpu"`.

`hw-kueue.clusterQueues[0].spec.resourceGroups[0].flavors[0].resources[0].nominalQuota` <a class="headerlink" href="#helm.hw-kueue.clusterQueues.0.spec.resourceGroups.0.flavors.0.resources.0.nominalQuota" title="Permanent link">#</a> { #helm.hw-kueue.clusterQueues.0.spec.resourceGroups.0.flavors.0.resources.0.nominalQuota }
:   Type `int`, default `0`.

`hw-kueue.clusterQueues[0].spec.resourceGroups[0].flavors[0].resources[1].name` <a class="headerlink" href="#helm.hw-kueue.clusterQueues.0.spec.resourceGroups.0.flavors.0.resources.1.name" title="Permanent link">#</a> { #helm.hw-kueue.clusterQueues.0.spec.resourceGroups.0.flavors.0.resources.1.name }
:   Type `string`, default `"memory"`.

`hw-kueue.clusterQueues[0].spec.resourceGroups[0].flavors[0].resources[1].nominalQuota` <a class="headerlink" href="#helm.hw-kueue.clusterQueues.0.spec.resourceGroups.0.flavors.0.resources.1.nominalQuota" title="Permanent link">#</a> { #helm.hw-kueue.clusterQueues.0.spec.resourceGroups.0.flavors.0.resources.1.nominalQuota }
:   Type `int`, default `0`.

`hw-kueue.clusterQueues[0].spec.resourceGroups[0].flavors[0].resources[2].name` <a class="headerlink" href="#helm.hw-kueue.clusterQueues.0.spec.resourceGroups.0.flavors.0.resources.2.name" title="Permanent link">#</a> { #helm.hw-kueue.clusterQueues.0.spec.resourceGroups.0.flavors.0.resources.2.name }
:   Type `string`, default `"pods"`.

`hw-kueue.clusterQueues[0].spec.resourceGroups[0].flavors[0].resources[2].nominalQuota` <a class="headerlink" href="#helm.hw-kueue.clusterQueues.0.spec.resourceGroups.0.flavors.0.resources.2.nominalQuota" title="Permanent link">#</a> { #helm.hw-kueue.clusterQueues.0.spec.resourceGroups.0.flavors.0.resources.2.nominalQuota }
:   Type `int`, default `0`.

`hw-kueue.clusterQueues[0].spec.resourceGroups[0].flavors[0].resources[3].name` <a class="headerlink" href="#helm.hw-kueue.clusterQueues.0.spec.resourceGroups.0.flavors.0.resources.3.name" title="Permanent link">#</a> { #helm.hw-kueue.clusterQueues.0.spec.resourceGroups.0.flavors.0.resources.3.name }
:   Type `string`, default `"nvidia.com/gpu"`.

`hw-kueue.clusterQueues[0].spec.resourceGroups[0].flavors[0].resources[3].nominalQuota` <a class="headerlink" href="#helm.hw-kueue.clusterQueues.0.spec.resourceGroups.0.flavors.0.resources.3.nominalQuota" title="Permanent link">#</a> { #helm.hw-kueue.clusterQueues.0.spec.resourceGroups.0.flavors.0.resources.3.nominalQuota }
:   Type `int`, default `0`.

</div>

## cohorts { #helm-values-hw-kueue-cohorts }

??? example "Defaults as YAML"

    ```yaml
    hw-kueue:
      cohorts:
      - annotations: {}
        labels: {}
        name: cluster
        spec:
          resourceGroups:
          - coveredResources:
            - cpu
            - memory
            - pods
            - nvidia.com/gpu
            flavors:
            - name: default-flavor
              resources:
              - name: cpu
                nominalQuota: 100
              - name: memory
                nominalQuota: 200Gi
              - name: pods
                nominalQuota: 100
              - name: nvidia.com/gpu
                nominalQuota: 50
    ```

<div class="hops-values" markdown>

`hw-kueue.cohorts[0].annotations` <a class="headerlink" href="#helm.hw-kueue.cohorts.0.annotations" title="Permanent link">#</a> { #helm.hw-kueue.cohorts.0.annotations }
:   Type `object`, default `{}`.

`hw-kueue.cohorts[0].labels` <a class="headerlink" href="#helm.hw-kueue.cohorts.0.labels" title="Permanent link">#</a> { #helm.hw-kueue.cohorts.0.labels }
:   Type `object`, default `{}`.

`hw-kueue.cohorts[0].name` <a class="headerlink" href="#helm.hw-kueue.cohorts.0.name" title="Permanent link">#</a> { #helm.hw-kueue.cohorts.0.name }
:   Type `string`, default `"cluster"`.

`hw-kueue.cohorts[0].spec.resourceGroups[0].coveredResources[0]` <a class="headerlink" href="#helm.hw-kueue.cohorts.0.spec.resourceGroups.0.coveredResources.0" title="Permanent link">#</a> { #helm.hw-kueue.cohorts.0.spec.resourceGroups.0.coveredResources.0 }
:   Type `string`, default `"cpu"`.

`hw-kueue.cohorts[0].spec.resourceGroups[0].coveredResources[1]` <a class="headerlink" href="#helm.hw-kueue.cohorts.0.spec.resourceGroups.0.coveredResources.1" title="Permanent link">#</a> { #helm.hw-kueue.cohorts.0.spec.resourceGroups.0.coveredResources.1 }
:   Type `string`, default `"memory"`.

`hw-kueue.cohorts[0].spec.resourceGroups[0].coveredResources[2]` <a class="headerlink" href="#helm.hw-kueue.cohorts.0.spec.resourceGroups.0.coveredResources.2" title="Permanent link">#</a> { #helm.hw-kueue.cohorts.0.spec.resourceGroups.0.coveredResources.2 }
:   Type `string`, default `"pods"`.

`hw-kueue.cohorts[0].spec.resourceGroups[0].coveredResources[3]` <a class="headerlink" href="#helm.hw-kueue.cohorts.0.spec.resourceGroups.0.coveredResources.3" title="Permanent link">#</a> { #helm.hw-kueue.cohorts.0.spec.resourceGroups.0.coveredResources.3 }
:   Type `string`, default `"nvidia.com/gpu"`.

`hw-kueue.cohorts[0].spec.resourceGroups[0].flavors[0].name` <a class="headerlink" href="#helm.hw-kueue.cohorts.0.spec.resourceGroups.0.flavors.0.name" title="Permanent link">#</a> { #helm.hw-kueue.cohorts.0.spec.resourceGroups.0.flavors.0.name }
:   Type `string`, default `"default-flavor"`.

`hw-kueue.cohorts[0].spec.resourceGroups[0].flavors[0].resources[0].name` <a class="headerlink" href="#helm.hw-kueue.cohorts.0.spec.resourceGroups.0.flavors.0.resources.0.name" title="Permanent link">#</a> { #helm.hw-kueue.cohorts.0.spec.resourceGroups.0.flavors.0.resources.0.name }
:   Type `string`, default `"cpu"`.

`hw-kueue.cohorts[0].spec.resourceGroups[0].flavors[0].resources[0].nominalQuota` <a class="headerlink" href="#helm.hw-kueue.cohorts.0.spec.resourceGroups.0.flavors.0.resources.0.nominalQuota" title="Permanent link">#</a> { #helm.hw-kueue.cohorts.0.spec.resourceGroups.0.flavors.0.resources.0.nominalQuota }
:   Type `int`, default `100`.

`hw-kueue.cohorts[0].spec.resourceGroups[0].flavors[0].resources[1].name` <a class="headerlink" href="#helm.hw-kueue.cohorts.0.spec.resourceGroups.0.flavors.0.resources.1.name" title="Permanent link">#</a> { #helm.hw-kueue.cohorts.0.spec.resourceGroups.0.flavors.0.resources.1.name }
:   Type `string`, default `"memory"`.

`hw-kueue.cohorts[0].spec.resourceGroups[0].flavors[0].resources[1].nominalQuota` <a class="headerlink" href="#helm.hw-kueue.cohorts.0.spec.resourceGroups.0.flavors.0.resources.1.nominalQuota" title="Permanent link">#</a> { #helm.hw-kueue.cohorts.0.spec.resourceGroups.0.flavors.0.resources.1.nominalQuota }
:   Type `string`, default `"200Gi"`.

`hw-kueue.cohorts[0].spec.resourceGroups[0].flavors[0].resources[2].name` <a class="headerlink" href="#helm.hw-kueue.cohorts.0.spec.resourceGroups.0.flavors.0.resources.2.name" title="Permanent link">#</a> { #helm.hw-kueue.cohorts.0.spec.resourceGroups.0.flavors.0.resources.2.name }
:   Type `string`, default `"pods"`.

`hw-kueue.cohorts[0].spec.resourceGroups[0].flavors[0].resources[2].nominalQuota` <a class="headerlink" href="#helm.hw-kueue.cohorts.0.spec.resourceGroups.0.flavors.0.resources.2.nominalQuota" title="Permanent link">#</a> { #helm.hw-kueue.cohorts.0.spec.resourceGroups.0.flavors.0.resources.2.nominalQuota }
:   Type `int`, default `100`.

`hw-kueue.cohorts[0].spec.resourceGroups[0].flavors[0].resources[3].name` <a class="headerlink" href="#helm.hw-kueue.cohorts.0.spec.resourceGroups.0.flavors.0.resources.3.name" title="Permanent link">#</a> { #helm.hw-kueue.cohorts.0.spec.resourceGroups.0.flavors.0.resources.3.name }
:   Type `string`, default `"nvidia.com/gpu"`.

`hw-kueue.cohorts[0].spec.resourceGroups[0].flavors[0].resources[3].nominalQuota` <a class="headerlink" href="#helm.hw-kueue.cohorts.0.spec.resourceGroups.0.flavors.0.resources.3.nominalQuota" title="Permanent link">#</a> { #helm.hw-kueue.cohorts.0.spec.resourceGroups.0.flavors.0.resources.3.nominalQuota }
:   Type `int`, default `50`.

</div>

## installJob { #helm-values-hw-kueue-installjob }

??? example "Defaults as YAML"

    ```yaml
    hw-kueue:
      installJob:
        configMapMountPath: /mnt/kueue-resources
        configMapName: kueue-objects-install-job-resources
        name: kueue-obj
        resources:
          limits:
            cpu: 100m
            memory: 250Mi
          requests:
            cpu: 100m
            memory: 250Mi
        ttlSecondsAfterFinished: null
    ```

<div class="hops-values" markdown>

`hw-kueue.installJob.configMapMountPath` <a class="headerlink" href="#helm.hw-kueue.installJob.configMapMountPath" title="Permanent link">#</a> { #helm.hw-kueue.installJob.configMapMountPath }
:   Type `string`, default `"/mnt/kueue-resources"`.

`hw-kueue.installJob.configMapName` <a class="headerlink" href="#helm.hw-kueue.installJob.configMapName" title="Permanent link">#</a> { #helm.hw-kueue.installJob.configMapName }
:   Type `string`, default `"kueue-objects-install-job-resources"`.

`hw-kueue.installJob.name` <a class="headerlink" href="#helm.hw-kueue.installJob.name" title="Permanent link">#</a> { #helm.hw-kueue.installJob.name }
:   Type `string`, default `"kueue-obj"`.
    install job name

`hw-kueue.installJob.resources.limits.cpu` <a class="headerlink" href="#helm.hw-kueue.installJob.resources.limits.cpu" title="Permanent link">#</a> { #helm.hw-kueue.installJob.resources.limits.cpu }
:   Type `string`, default `"100m"`.

`hw-kueue.installJob.resources.limits.memory` <a class="headerlink" href="#helm.hw-kueue.installJob.resources.limits.memory" title="Permanent link">#</a> { #helm.hw-kueue.installJob.resources.limits.memory }
:   Type `string`, default `"250Mi"`.

`hw-kueue.installJob.resources.requests.cpu` <a class="headerlink" href="#helm.hw-kueue.installJob.resources.requests.cpu" title="Permanent link">#</a> { #helm.hw-kueue.installJob.resources.requests.cpu }
:   Type `string`, default `"100m"`.

`hw-kueue.installJob.resources.requests.memory` <a class="headerlink" href="#helm.hw-kueue.installJob.resources.requests.memory" title="Permanent link">#</a> { #helm.hw-kueue.installJob.resources.requests.memory }
:   Type `string`, default `"250Mi"`.

`hw-kueue.installJob.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.hw-kueue.installJob.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.hw-kueue.installJob.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    TTL in seconds for the install-kueue-object Job. Overrides global default.

</div>

## managerConfig { #helm-values-hw-kueue-managerconfig }

??? example "Defaults as YAML"

    ```yaml
    hw-kueue:
      managerConfig:
        clientConnection:
          burst: 100
          qps: 50
        controller:
          groupKindConcurrency:
            ClusterQueue.kueue.x-k8s.io: 1
            Job.batch: 5
            LocalQueue.kueue.x-k8s.io: 1
            Pod: 5
            ResourceFlavor.kueue.x-k8s.io: 1
            Workload.kueue.x-k8s.io: 5
        excludedNamespaces:
        - kube-system
        - kueue-system
        - kyverno
        fairSharing:
          enable: true
          preemptionStrategies:
          - LessThanOrEqualToFinalShare
          - LessThanInitialShare
        health:
          healthProbeBindAddress: 8081
        integrations:
          frameworks:
          - batch/job
          - kubeflow.org/mpijob
          - ray.io/rayjob
          - ray.io/raycluster
          - jobset.x-k8s.io/jobset
          - kubeflow.org/paddlejob
          - kubeflow.org/pytorchjob
          - kubeflow.org/tfjob
          - kubeflow.org/xgboostjob
          - workload.codeflare.dev/appwrapper
          - pod
          - deployment
          - statefulset
        leaderElection:
          leaderElect: true
          resourceName: c1f6bfd2.kueue.x-k8s.io
        manageJobsWithoutQueueName: false
        metrics:
          bindAddress: 8443
        webhook:
          port: 9443
    ```

<div class="hops-values" markdown>

`hw-kueue.managerConfig.clientConnection.burst` <a class="headerlink" href="#helm.hw-kueue.managerConfig.clientConnection.burst" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.clientConnection.burst }
:   Type `int`, default `100`.

`hw-kueue.managerConfig.clientConnection.qps` <a class="headerlink" href="#helm.hw-kueue.managerConfig.clientConnection.qps" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.clientConnection.qps }
:   Type `int`, default `50`.

`hw-kueue.managerConfig.controller.groupKindConcurrency."ClusterQueue.kueue.x-k8s.io"` <a class="headerlink" href="#helm.hw-kueue.managerConfig.controller.groupKindConcurrency.ClusterQueue.kueue.x-k8s.io" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.controller.groupKindConcurrency.ClusterQueue.kueue.x-k8s.io }
:   Type `int`, default `1`.

`hw-kueue.managerConfig.controller.groupKindConcurrency."Job.batch"` <a class="headerlink" href="#helm.hw-kueue.managerConfig.controller.groupKindConcurrency.Job.batch" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.controller.groupKindConcurrency.Job.batch }
:   Type `int`, default `5`.

`hw-kueue.managerConfig.controller.groupKindConcurrency."LocalQueue.kueue.x-k8s.io"` <a class="headerlink" href="#helm.hw-kueue.managerConfig.controller.groupKindConcurrency.LocalQueue.kueue.x-k8s.io" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.controller.groupKindConcurrency.LocalQueue.kueue.x-k8s.io }
:   Type `int`, default `1`.

`hw-kueue.managerConfig.controller.groupKindConcurrency."ResourceFlavor.kueue.x-k8s.io"` <a class="headerlink" href="#helm.hw-kueue.managerConfig.controller.groupKindConcurrency.ResourceFlavor.kueue.x-k8s.io" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.controller.groupKindConcurrency.ResourceFlavor.kueue.x-k8s.io }
:   Type `int`, default `1`.

`hw-kueue.managerConfig.controller.groupKindConcurrency."Workload.kueue.x-k8s.io"` <a class="headerlink" href="#helm.hw-kueue.managerConfig.controller.groupKindConcurrency.Workload.kueue.x-k8s.io" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.controller.groupKindConcurrency.Workload.kueue.x-k8s.io }
:   Type `int`, default `5`.

`hw-kueue.managerConfig.controller.groupKindConcurrency.Pod` <a class="headerlink" href="#helm.hw-kueue.managerConfig.controller.groupKindConcurrency.Pod" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.controller.groupKindConcurrency.Pod }
:   Type `int`, default `5`.

`hw-kueue.managerConfig.excludedNamespaces[0]` <a class="headerlink" href="#helm.hw-kueue.managerConfig.excludedNamespaces.0" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.excludedNamespaces.0 }
:   Type `string`, default `"kube-system"`.

`hw-kueue.managerConfig.excludedNamespaces[1]` <a class="headerlink" href="#helm.hw-kueue.managerConfig.excludedNamespaces.1" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.excludedNamespaces.1 }
:   Type `string`, default `"kueue-system"`.

`hw-kueue.managerConfig.excludedNamespaces[2]` <a class="headerlink" href="#helm.hw-kueue.managerConfig.excludedNamespaces.2" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.excludedNamespaces.2 }
:   Type `string`, default `"kyverno"`.

`hw-kueue.managerConfig.fairSharing.enable` <a class="headerlink" href="#helm.hw-kueue.managerConfig.fairSharing.enable" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.fairSharing.enable }
:   Type `bool`, default `true`.

`hw-kueue.managerConfig.fairSharing.preemptionStrategies[0]` <a class="headerlink" href="#helm.hw-kueue.managerConfig.fairSharing.preemptionStrategies.0" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.fairSharing.preemptionStrategies.0 }
:   Type `string`, default `"LessThanOrEqualToFinalShare"`.

`hw-kueue.managerConfig.fairSharing.preemptionStrategies[1]` <a class="headerlink" href="#helm.hw-kueue.managerConfig.fairSharing.preemptionStrategies.1" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.fairSharing.preemptionStrategies.1 }
:   Type `string`, default `"LessThanInitialShare"`.

`hw-kueue.managerConfig.health.healthProbeBindAddress` <a class="headerlink" href="#helm.hw-kueue.managerConfig.health.healthProbeBindAddress" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.health.healthProbeBindAddress }
:   Type `int`, default `8081`.

`hw-kueue.managerConfig.integrations.frameworks[0]` <a class="headerlink" href="#helm.hw-kueue.managerConfig.integrations.frameworks.0" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.integrations.frameworks.0 }
:   Type `string`, default `"batch/job"`.

`hw-kueue.managerConfig.integrations.frameworks[10]` <a class="headerlink" href="#helm.hw-kueue.managerConfig.integrations.frameworks.10" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.integrations.frameworks.10 }
:   Type `string`, default `"pod"`.

`hw-kueue.managerConfig.integrations.frameworks[11]` <a class="headerlink" href="#helm.hw-kueue.managerConfig.integrations.frameworks.11" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.integrations.frameworks.11 }
:   Type `string`, default `"deployment"`.

`hw-kueue.managerConfig.integrations.frameworks[12]` <a class="headerlink" href="#helm.hw-kueue.managerConfig.integrations.frameworks.12" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.integrations.frameworks.12 }
:   Type `string`, default `"statefulset"`.

`hw-kueue.managerConfig.integrations.frameworks[1]` <a class="headerlink" href="#helm.hw-kueue.managerConfig.integrations.frameworks.1" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.integrations.frameworks.1 }
:   Type `string`, default `"kubeflow.org/mpijob"`.

`hw-kueue.managerConfig.integrations.frameworks[2]` <a class="headerlink" href="#helm.hw-kueue.managerConfig.integrations.frameworks.2" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.integrations.frameworks.2 }
:   Type `string`, default `"ray.io/rayjob"`.

`hw-kueue.managerConfig.integrations.frameworks[3]` <a class="headerlink" href="#helm.hw-kueue.managerConfig.integrations.frameworks.3" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.integrations.frameworks.3 }
:   Type `string`, default `"ray.io/raycluster"`.

`hw-kueue.managerConfig.integrations.frameworks[4]` <a class="headerlink" href="#helm.hw-kueue.managerConfig.integrations.frameworks.4" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.integrations.frameworks.4 }
:   Type `string`, default `"jobset.x-k8s.io/jobset"`.

`hw-kueue.managerConfig.integrations.frameworks[5]` <a class="headerlink" href="#helm.hw-kueue.managerConfig.integrations.frameworks.5" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.integrations.frameworks.5 }
:   Type `string`, default `"kubeflow.org/paddlejob"`.

`hw-kueue.managerConfig.integrations.frameworks[6]` <a class="headerlink" href="#helm.hw-kueue.managerConfig.integrations.frameworks.6" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.integrations.frameworks.6 }
:   Type `string`, default `"kubeflow.org/pytorchjob"`.

`hw-kueue.managerConfig.integrations.frameworks[7]` <a class="headerlink" href="#helm.hw-kueue.managerConfig.integrations.frameworks.7" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.integrations.frameworks.7 }
:   Type `string`, default `"kubeflow.org/tfjob"`.

`hw-kueue.managerConfig.integrations.frameworks[8]` <a class="headerlink" href="#helm.hw-kueue.managerConfig.integrations.frameworks.8" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.integrations.frameworks.8 }
:   Type `string`, default `"kubeflow.org/xgboostjob"`.

`hw-kueue.managerConfig.integrations.frameworks[9]` <a class="headerlink" href="#helm.hw-kueue.managerConfig.integrations.frameworks.9" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.integrations.frameworks.9 }
:   Type `string`, default `"workload.codeflare.dev/appwrapper"`.

`hw-kueue.managerConfig.leaderElection.leaderElect` <a class="headerlink" href="#helm.hw-kueue.managerConfig.leaderElection.leaderElect" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.leaderElection.leaderElect }
:   Type `bool`, default `true`.

`hw-kueue.managerConfig.leaderElection.resourceName` <a class="headerlink" href="#helm.hw-kueue.managerConfig.leaderElection.resourceName" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.leaderElection.resourceName }
:   Type `string`, default `"c1f6bfd2.kueue.x-k8s.io"`.

`hw-kueue.managerConfig.manageJobsWithoutQueueName` <a class="headerlink" href="#helm.hw-kueue.managerConfig.manageJobsWithoutQueueName" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.manageJobsWithoutQueueName }
:   Type `bool`, default `false`.

`hw-kueue.managerConfig.metrics.bindAddress` <a class="headerlink" href="#helm.hw-kueue.managerConfig.metrics.bindAddress" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.metrics.bindAddress }
:   Type `int`, default `8443`.

`hw-kueue.managerConfig.webhook.port` <a class="headerlink" href="#helm.hw-kueue.managerConfig.webhook.port" title="Permanent link">#</a> { #helm.hw-kueue.managerConfig.webhook.port }
:   Type `int`, default `9443`.

</div>

## rbac { #helm-values-hw-kueue-rbac }

??? example "Defaults as YAML"

    ```yaml
    hw-kueue:
      rbac:
        clusterqueue:
          enabled: true
        cohort:
          enabled: true
        localqueue:
          enabled: true
        resourceFlavors:
          enabled: true
        topologies:
          enabled: true
        workload:
          enabled: true
    ```

<div class="hops-values" markdown>

`hw-kueue.rbac.clusterqueue.enabled` <a class="headerlink" href="#helm.hw-kueue.rbac.clusterqueue.enabled" title="Permanent link">#</a> { #helm.hw-kueue.rbac.clusterqueue.enabled }
:   Type `bool`, default `true`.

`hw-kueue.rbac.cohort.enabled` <a class="headerlink" href="#helm.hw-kueue.rbac.cohort.enabled" title="Permanent link">#</a> { #helm.hw-kueue.rbac.cohort.enabled }
:   Type `bool`, default `true`.

`hw-kueue.rbac.localqueue.enabled` <a class="headerlink" href="#helm.hw-kueue.rbac.localqueue.enabled" title="Permanent link">#</a> { #helm.hw-kueue.rbac.localqueue.enabled }
:   Type `bool`, default `true`.

`hw-kueue.rbac.resourceFlavors.enabled` <a class="headerlink" href="#helm.hw-kueue.rbac.resourceFlavors.enabled" title="Permanent link">#</a> { #helm.hw-kueue.rbac.resourceFlavors.enabled }
:   Type `bool`, default `true`.

`hw-kueue.rbac.topologies.enabled` <a class="headerlink" href="#helm.hw-kueue.rbac.topologies.enabled" title="Permanent link">#</a> { #helm.hw-kueue.rbac.topologies.enabled }
:   Type `bool`, default `true`.

`hw-kueue.rbac.workload.enabled` <a class="headerlink" href="#helm.hw-kueue.rbac.workload.enabled" title="Permanent link">#</a> { #helm.hw-kueue.rbac.workload.enabled }
:   Type `bool`, default `true`.

</div>

<!-- END GENERATED VALUES -->
