# Kueue values { #helm-values-hw-kueue }

Values under `hw-kueue` configure Kueue, the job queueing controller, and the queues Hopsworks schedules jobs with.
With `kueue.enabled=false` Hopsworks uses a Kueue installed outside its release; [Kueue outside the Hopsworks namespace](../../admin/kueue_external.md) covers moving an existing cluster there.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.3.0-alpha-1793026678` (Hopsworks `5.3.0`)._

Deployed according to the first of these values that is set: [`global._hopsworks.kueue.enabled`](global.md#helm.global._hopsworks.kueue.enabled), [`global._hopsworks.full_platform`](global.md#helm.global._hopsworks.full_platform).

## General { #helm-values-hw-kueue-general }

??? example "Defaults as YAML"

    ```yaml
    hw-kueue:
      enforcePrerequisiteCheck: true
      fullnameOverride: kueue
      hopsworkslib: {}
      imagePullPolicy: Always
      kueue:
        enabled: false
      kueueApiVersion: v1beta2
      kueueNamespace: kueue-system
      resourceFlavours:
      - annotations: {}
        labels: {}
        name: default-flavor
        spec:
          nodeLabels:
            cloud.provider.com/region: europe
          nodeTaints: {}
          tolerations: {}
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

`hw-kueue.enforcePrerequisiteCheck` <a class="headerlink" href="#helm.hw-kueue.enforcePrerequisiteCheck" title="Permanent link">#</a> { #helm.hw-kueue.enforcePrerequisiteCheck }
:   Type `bool`, default `true`.
    Refuse to render while the bundled Kueue 0.12 or its v1alpha1 storage is still on the cluster, or when no Kueue serving kueue.x-k8s.io/v1beta2 is installed. Set false for helm template.

`hw-kueue.fullnameOverride` <a class="headerlink" href="#helm.hw-kueue.fullnameOverride" title="Permanent link">#</a> { #helm.hw-kueue.fullnameOverride }
:   Type `string`, default `"kueue"`.
    Name prefix of the objects of release kueue, the Kueue Hopsworks uses (installed with fullnameOverride kueue): the Hopsworks bindings name its ClusterRoles.

`hw-kueue.hopsworkslib` <a class="headerlink" href="#helm.hw-kueue.hopsworkslib" title="Permanent link">#</a> { #helm.hw-kueue.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`hw-kueue.imagePullPolicy` <a class="headerlink" href="#helm.hw-kueue.imagePullPolicy" title="Permanent link">#</a> { #helm.hw-kueue.imagePullPolicy }
:   Type `string`, default `"Always"`.

`hw-kueue.kueue` <a class="headerlink" href="#helm.hw-kueue.kueue" title="Permanent link">#</a> { #helm.hw-kueue.kueue }
:   Type `object`, default `{"enabled":false}`.
    This chart ships no Kueue. kueue.enabled stays false, as the 5.1 chart's migrate-to-external.sh and files/upgrade-kueue.sh check it; true is refused.

`hw-kueue.kueueApiVersion` <a class="headerlink" href="#helm.hw-kueue.kueueApiVersion" title="Permanent link">#</a> { #helm.hw-kueue.kueueApiVersion }
:   Type `string`, default `"v1beta2"`.
    The kueue.x-k8s.io version the backend of this chart reads. Read by files/upgrade-kueue.sh to tell this chart from 5.2.1 and earlier; do not change.

`hw-kueue.kueueNamespace` <a class="headerlink" href="#helm.hw-kueue.kueueNamespace" title="Permanent link">#</a> { #helm.hw-kueue.kueueNamespace }
:   Type `string`, default `"kueue-system"`.
    Namespace of release kueue; the queue Job waits for its webhook there.

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
