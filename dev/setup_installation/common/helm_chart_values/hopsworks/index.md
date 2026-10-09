# Hopsworks values { #helm-values-hopsworks }

Values under `hopsworks` configure the Hopsworks backend: the Payara worker and admin deployments, ingress, the certificate authority, database migrations and backups.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.2.0-alpha-1791567888` (Hopsworks `5.2.0`)._

Deployed when [`global._hopsworks.full_platform`](global.md#helm.global._hopsworks.full_platform) is `true`.

## General { #helm-values-hopsworks-general }

??? example "Defaults as YAML"

    ```yaml
    hopsworks:
      agent_email: agent@hops.io
      agent_password: admin
      cleanupOnUninstall:
        enabled: true
        ttlSecondsAfterFinished: null
      create_secrets: true
      ddlConfigmapName: sql-ddl
      defaultServiceAccount:
        annotations: {}
        create: true
      dropDatabase: false
      flyway:
        replaceDDL: ''
      flywayconfigmapName: flyway-config
      fullnameOverride: null
      hopsfsMount:
        enabled: true
        mountPath: /hopsfs
      hopsworkslib: {}
      imageBuilder:
        image: image-builder
        tag: '0.2'
      imageBuilderServiceAccount:
        annotations: {}
        create: true
        name: image-builder
      instanceconfigmapName: instance-config
      jupyter:
        notebookConfig:
          allowOrigin: ${conf.allowOrigin}
          enableDownloads: true
          enableUploads: true
      lb:
        names:
          mysqld: mysqld-external
          rdrs: rdrs-external
        serviceAccount:
          annotations: {}
      nameOverride: null
      nodeSelector: {}
      objectStorageEnvInformation: null
      opensearchReindex:
        enabled: true
      payaraVersion: 6.2025.11-jdk21.0
      payaraconfigmapName: post-boot-commands
      podAnnotations: {}
      podDisruptionBudget:
        hopsworksCA:
          enabled: true
          minAvailable: 1
        worker:
          enabled: true
          minAvailable: 1
      podLabels: {}
      replicaCount:
        worker: 2
      resources:
        admin:
          auto_jvm: true
          jvm:
            memory:
              buffer: 2048
              compressedClassSpaceSize: 512
              heap: 4096
              metaspace: 2048
              nonMethodCodeHeapSize: 5
              nonProfiledCodeHeapSize: 48
              profiledCodeHeapSize: 48
        worker:
          auto_jvm: true
          jvm:
            memory:
              buffer: 3072
              compressedClassSpaceSize: 512
              heap: 4096
              metaspace: 2048
              nonMethodCodeHeapSize: 5
              nonProfiledCodeHeapSize: 48
              profiledCodeHeapSize: 48
      securityContext: {}
      setAdminHighPriority: true
      sparkConfigmapName: spark
      sqldmlconfigmapName: sql-dml
      sqlgrantsconfigmapName: sql-grants
      templatesconfigmapName: hopsworks-templates
      tolerations: []
      topologySpreadConstraint: {}
      updateLoadBalancerDomains:
        resources:
          limits:
            cpu: 50m
            memory: 50M
          requests:
            cpu: 20m
            memory: 20M
      variables:
        kube_kserve_installed: true
        kube_serving_vllm_omni_versions: v0.28.0
        kube_serving_vllm_versions: v0.28.0
      volumeMounts:
        admin: []
        migrate: []
        worker: []
      volumes:
        admin: []
        migrate: []
        worker: []
    ```

<div class="hops-values" markdown>

`hopsworks` <a class="headerlink" href="#helm.hopsworks" title="Permanent link">#</a> { #helm.hopsworks }
:   Type `object`.
    override hopsworks values

    ??? note "Default"

        ```yaml
        lb:
          names:
            mysqld: mysqld-external
            rdrs: rdrs-external
        replicaCount:
          worker: 2
        resources:
          admin:
            auto_jvm: true
            jvm:
              memory:
                buffer: 2048
                compressedClassSpaceSize: 512
                heap: 4096
                metaspace: 2048
                nonMethodCodeHeapSize: 5
                nonProfiledCodeHeapSize: 48
                profiledCodeHeapSize: 48
          worker:
            auto_jvm: true
            jvm:
              memory:
                buffer: 3072
                compressedClassSpaceSize: 512
                heap: 4096
                metaspace: 2048
                nonMethodCodeHeapSize: 5
                nonProfiledCodeHeapSize: 48
                profiledCodeHeapSize: 48
        variables:
          kube_kserve_installed: true
          kube_serving_vllm_omni_versions: v0.28.0
          kube_serving_vllm_versions: v0.28.0
        ```

`hopsworks.agent_email` <a class="headerlink" href="#helm.hopsworks.agent_email" title="Permanent link">#</a> { #helm.hopsworks.agent_email }
:   Type `string`, default `"agent@hops.io"`.

`hopsworks.agent_password` <a class="headerlink" href="#helm.hopsworks.agent_password" title="Permanent link">#</a> { #helm.hopsworks.agent_password }
:   Type `string`, default `"admin"`.

`hopsworks.cleanupOnUninstall` <a class="headerlink" href="#helm.hopsworks.cleanupOnUninstall" title="Permanent link">#</a> { #helm.hopsworks.cleanupOnUninstall }
:   Type `object`, default `{"enabled":true,"ttlSecondsAfterFinished":null}`.
    post-delete cleanup of Hopsworks runtime leftovers (CA/setup-script Secrets & ConfigMaps annotated hopsworks.ai/project, plus the sql-dml/sql-grants/flyway-config hook ConfigMaps) that Helm/ArgoCD never tracked and so never prune.

`hopsworks.cleanupOnUninstall.enabled` <a class="headerlink" href="#helm.hopsworks.cleanupOnUninstall.enabled" title="Permanent link">#</a> { #helm.hopsworks.cleanupOnUninstall.enabled }
:   Type `bool`, default `true`.
    enable the post-delete Hopsworks cleanup hook

`hopsworks.cleanupOnUninstall.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.hopsworks.cleanupOnUninstall.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.hopsworks.cleanupOnUninstall.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    ttlSecondsAfterFinished for the cleanup Job; null falls through to the global default

`hopsworks.create_secrets` <a class="headerlink" href="#helm.hopsworks.create_secrets" title="Permanent link">#</a> { #helm.hopsworks.create_secrets }
:   Type `bool`, default `true`.
    If false, you have to create the secret for the hopsworks users (hopsworks-users-secrets) manually. If false and ldap/kerberos is enabled, the secret for ldap credentials must be created manually as well.

`hopsworks.ddlConfigmapName` <a class="headerlink" href="#helm.hopsworks.ddlConfigmapName" title="Permanent link">#</a> { #helm.hopsworks.ddlConfigmapName }
:   Type `string`, default `"sql-ddl"`.

`hopsworks.defaultServiceAccount.annotations` <a class="headerlink" href="#helm.hopsworks.defaultServiceAccount.annotations" title="Permanent link">#</a> { #helm.hopsworks.defaultServiceAccount.annotations }
:   Type `object`, default `{}`.
    annotations

`hopsworks.defaultServiceAccount.create` <a class="headerlink" href="#helm.hopsworks.defaultServiceAccount.create" title="Permanent link">#</a> { #helm.hopsworks.defaultServiceAccount.create }
:   Type `bool`, default `true`.

`hopsworks.dropDatabase` <a class="headerlink" href="#helm.hopsworks.dropDatabase" title="Permanent link">#</a> { #helm.hopsworks.dropDatabase }
:   Type `bool`, default `false`.
    Should not be changed here. Leave this as a conscious choice for the user when installing. If set to true will drop databases when helm uninstall.

`hopsworks.flyway.replaceDDL` <a class="headerlink" href="#helm.hopsworks.flyway.replaceDDL" title="Permanent link">#</a> { #helm.hopsworks.flyway.replaceDDL }
:   Type `string`, default `""`.

`hopsworks.flywayconfigmapName` <a class="headerlink" href="#helm.hopsworks.flywayconfigmapName" title="Permanent link">#</a> { #helm.hopsworks.flywayconfigmapName }
:   Type `string`, default `"flyway-config"`.

`hopsworks.fullnameOverride` <a class="headerlink" href="#helm.hopsworks.fullnameOverride" title="Permanent link">#</a> { #helm.hopsworks.fullnameOverride }
:   Type `string`, default `nil`.
    override app fully qualified name

`hopsworks.hopsfsMount.enabled` <a class="headerlink" href="#helm.hopsworks.hopsfsMount.enabled" title="Permanent link">#</a> { #helm.hopsworks.hopsfsMount.enabled }
:   Type `bool`, default `true`.

`hopsworks.hopsfsMount.mountPath` <a class="headerlink" href="#helm.hopsworks.hopsfsMount.mountPath" title="Permanent link">#</a> { #helm.hopsworks.hopsfsMount.mountPath }
:   Type `string`, default `"/hopsfs"`.

`hopsworks.hopsworkslib` <a class="headerlink" href="#helm.hopsworks.hopsworkslib" title="Permanent link">#</a> { #helm.hopsworks.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`hopsworks.imageBuilder.image` <a class="headerlink" href="#helm.hopsworks.imageBuilder.image" title="Permanent link">#</a> { #helm.hopsworks.imageBuilder.image }
:   Type `string`, default `"image-builder"`.

`hopsworks.imageBuilder.tag` <a class="headerlink" href="#helm.hopsworks.imageBuilder.tag" title="Permanent link">#</a> { #helm.hopsworks.imageBuilder.tag }
:   Type `string`, default `"0.2"`.
    0.2 is a floor, not a preference. The OpenShift build path passes package-index credentials to buildah as -s id=NAME,src=PATH, and build-and-push.sh only learned that option in 0.2. Against 0.1 the script's getopts rejects it and every environment build on OpenShift fails, so this tag and the backend's docker_operations_image_builder_image move together.

`hopsworks.imageBuilderServiceAccount` <a class="headerlink" href="#helm.hopsworks.imageBuilderServiceAccount" title="Permanent link">#</a> { #helm.hopsworks.imageBuilderServiceAccount }
:   Type `object`, default `{"annotations":{},"create":true,"name":"image-builder"}`.
    Configuration for the Service Account running all user environment Image Building Jobs

`hopsworks.instanceconfigmapName` <a class="headerlink" href="#helm.hopsworks.instanceconfigmapName" title="Permanent link">#</a> { #helm.hopsworks.instanceconfigmapName }
:   Type `string`, default `"instance-config"`.

`hopsworks.jupyter.notebookConfig.allowOrigin` <a class="headerlink" href="#helm.hopsworks.jupyter.notebookConfig.allowOrigin" title="Permanent link">#</a> { #helm.hopsworks.jupyter.notebookConfig.allowOrigin }
:   Type `string`, default `"${conf.allowOrigin}"`.

`hopsworks.jupyter.notebookConfig.enableDownloads` <a class="headerlink" href="#helm.hopsworks.jupyter.notebookConfig.enableDownloads" title="Permanent link">#</a> { #helm.hopsworks.jupyter.notebookConfig.enableDownloads }
:   Type `bool`, default `true`.
    Set to false to disable file downloads from the Jupyter UI.

`hopsworks.jupyter.notebookConfig.enableUploads` <a class="headerlink" href="#helm.hopsworks.jupyter.notebookConfig.enableUploads" title="Permanent link">#</a> { #helm.hopsworks.jupyter.notebookConfig.enableUploads }
:   Type `bool`, default `true`.
    Set to false to disable file uploads from the Jupyter UI and reject base64 file uploads via the Contents API. Kernel/terminal file writes are unaffected. Requires JupyterLab >= 4.5.

`hopsworks.lb.names.mysqld` <a class="headerlink" href="#helm.hopsworks.lb.names.mysqld" title="Permanent link">#</a> { #helm.hopsworks.lb.names.mysqld }
:   Type `string`, default `"mysqld-external"`.

`hopsworks.lb.names.rdrs` <a class="headerlink" href="#helm.hopsworks.lb.names.rdrs" title="Permanent link">#</a> { #helm.hopsworks.lb.names.rdrs }
:   Type `string`, default `"rdrs-external"`.

`hopsworks.lb.serviceAccount.annotations` <a class="headerlink" href="#helm.hopsworks.lb.serviceAccount.annotations" title="Permanent link">#</a> { #helm.hopsworks.lb.serviceAccount.annotations }
:   Type `object`, default `{}`.
    annotations

`hopsworks.nameOverride` <a class="headerlink" href="#helm.hopsworks.nameOverride" title="Permanent link">#</a> { #helm.hopsworks.nameOverride }
:   Type `string`, default `nil`.
    override app chart name

`hopsworks.nodeSelector` <a class="headerlink" href="#helm.hopsworks.nodeSelector" title="Permanent link">#</a> { #helm.hopsworks.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

`hopsworks.objectStorageEnvInformation` <a class="headerlink" href="#helm.hopsworks.objectStorageEnvInformation" title="Permanent link">#</a> { #helm.hopsworks.objectStorageEnvInformation }
:   Type `string`, default `nil`.
    override object storage list of of environment variables

`hopsworks.opensearchReindex.enabled` <a class="headerlink" href="#helm.hopsworks.opensearchReindex.enabled" title="Permanent link">#</a> { #helm.hopsworks.opensearchReindex.enabled }
:   Type `bool`, default `true`.
    Rebuild the featurestore search index after an upgrade, when what the index holds has changed since its last rebuild. The hook keys its request with the index generation, featurestore-index-5.1, which the chart bumps only with a change to what the backend indexes: a generation already rebuilt is answered with that run, so patch upgrades and ArgoCD syncs do not rebuild again, and a cluster that missed the rebuild gets it on its next upgrade. Runs requested by earlier charts carry no key, so the first upgrade with this chart rebuilds once. The rebuild runs in the backend after the upgrade and takes hours on a large cluster, with search incomplete until it finishes; its progress shows under Cluster Settings > Service Operations > OpenSearch Index Commands. A failed hook Job is removed after global._hopsworks.jobs.ttlSecondsAfterFinished in the default mode, or when the hook next renders; with global._hopsworks.mode set, as under ArgoCD, delete post-upgrade-opensearch-reindex-job by hand if you turn this off after a failed attempt.

`hopsworks.payaraVersion` <a class="headerlink" href="#helm.hopsworks.payaraVersion" title="Permanent link">#</a> { #helm.hopsworks.payaraVersion }
:   Type `string`, default `"6.2025.11-jdk21.0"`.

`hopsworks.payaraconfigmapName` <a class="headerlink" href="#helm.hopsworks.payaraconfigmapName" title="Permanent link">#</a> { #helm.hopsworks.payaraconfigmapName }
:   Type `string`, default `"post-boot-commands"`.

`hopsworks.podAnnotations` <a class="headerlink" href="#helm.hopsworks.podAnnotations" title="Permanent link">#</a> { #helm.hopsworks.podAnnotations }
:   Type `object`, default `{}`.
    pod annotations

`hopsworks.podDisruptionBudget.hopsworksCA.enabled` <a class="headerlink" href="#helm.hopsworks.podDisruptionBudget.hopsworksCA.enabled" title="Permanent link">#</a> { #helm.hopsworks.podDisruptionBudget.hopsworksCA.enabled }
:   Type `bool`, default `true`.

`hopsworks.podDisruptionBudget.hopsworksCA.minAvailable` <a class="headerlink" href="#helm.hopsworks.podDisruptionBudget.hopsworksCA.minAvailable" title="Permanent link">#</a> { #helm.hopsworks.podDisruptionBudget.hopsworksCA.minAvailable }
:   Type `int`, default `1`.

`hopsworks.podDisruptionBudget.worker.enabled` <a class="headerlink" href="#helm.hopsworks.podDisruptionBudget.worker.enabled" title="Permanent link">#</a> { #helm.hopsworks.podDisruptionBudget.worker.enabled }
:   Type `bool`, default `true`.

`hopsworks.podDisruptionBudget.worker.minAvailable` <a class="headerlink" href="#helm.hopsworks.podDisruptionBudget.worker.minAvailable" title="Permanent link">#</a> { #helm.hopsworks.podDisruptionBudget.worker.minAvailable }
:   Type `int`, default `1`.

`hopsworks.podLabels` <a class="headerlink" href="#helm.hopsworks.podLabels" title="Permanent link">#</a> { #helm.hopsworks.podLabels }
:   Type `object`, default `{}`.
    pod labels

`hopsworks.replicaCount.worker` <a class="headerlink" href="#helm.hopsworks.replicaCount.worker" title="Permanent link">#</a> { #helm.hopsworks.replicaCount.worker }
:   Type `int`, default `2`.
    Number of Payara worker replicas. Not rendered while hpa.worker.enabled is true: the HPA then owns spec.replicas and this value is its minReplicas. Turning the HPA on for a running release drops the workers to 1 once, until the HPA scales them back up.

`hopsworks.securityContext` <a class="headerlink" href="#helm.hopsworks.securityContext" title="Permanent link">#</a> { #helm.hopsworks.securityContext }
:   Type `object`, default `{}`.
    custom security context for hopsworks admin and workers

`hopsworks.setAdminHighPriority` <a class="headerlink" href="#helm.hopsworks.setAdminHighPriority" title="Permanent link">#</a> { #helm.hopsworks.setAdminHighPriority }
:   Type `bool`, default `true`.

`hopsworks.sparkConfigmapName` <a class="headerlink" href="#helm.hopsworks.sparkConfigmapName" title="Permanent link">#</a> { #helm.hopsworks.sparkConfigmapName }
:   Type `string`, default `"spark"`.

`hopsworks.sqldmlconfigmapName` <a class="headerlink" href="#helm.hopsworks.sqldmlconfigmapName" title="Permanent link">#</a> { #helm.hopsworks.sqldmlconfigmapName }
:   Type `string`, default `"sql-dml"`.

`hopsworks.sqlgrantsconfigmapName` <a class="headerlink" href="#helm.hopsworks.sqlgrantsconfigmapName" title="Permanent link">#</a> { #helm.hopsworks.sqlgrantsconfigmapName }
:   Type `string`, default `"sql-grants"`.

`hopsworks.templatesconfigmapName` <a class="headerlink" href="#helm.hopsworks.templatesconfigmapName" title="Permanent link">#</a> { #helm.hopsworks.templatesconfigmapName }
:   Type `string`, default `"hopsworks-templates"`.

`hopsworks.tolerations` <a class="headerlink" href="#helm.hopsworks.tolerations" title="Permanent link">#</a> { #helm.hopsworks.tolerations }
:   Type `list`, default `[]`.

`hopsworks.topologySpreadConstraint` <a class="headerlink" href="#helm.hopsworks.topologySpreadConstraint" title="Permanent link">#</a> { #helm.hopsworks.topologySpreadConstraint }
:   Type `object`, default `{}`.
    The default topology spread constraint. If not defined the global topology spread constraint would be used instead.

`hopsworks.updateLoadBalancerDomains` <a class="headerlink" href="#helm.hopsworks.updateLoadBalancerDomains" title="Permanent link">#</a> { #helm.hopsworks.updateLoadBalancerDomains }
:   Type `object`.
    update_load_balancer_domains Job configuration

    ??? note "Default"

        ```yaml
        resources:
          limits:
            cpu: 50m
            memory: 50M
          requests:
            cpu: 20m
            memory: 20M
        ```

`hopsworks.updateLoadBalancerDomains.resources` <a class="headerlink" href="#helm.hopsworks.updateLoadBalancerDomains.resources" title="Permanent link">#</a> { #helm.hopsworks.updateLoadBalancerDomains.resources }
:   Type `object`.
    resource limits configuration

    ??? note "Default"

        ```yaml
        limits:
          cpu: 50m
          memory: 50M
        requests:
          cpu: 20m
          memory: 20M
        ```

`hopsworks.volumeMounts.admin` <a class="headerlink" href="#helm.hopsworks.volumeMounts.admin" title="Permanent link">#</a> { #helm.hopsworks.volumeMounts.admin }
:   Type `list`, default `[]`.

`hopsworks.volumeMounts.migrate` <a class="headerlink" href="#helm.hopsworks.volumeMounts.migrate" title="Permanent link">#</a> { #helm.hopsworks.volumeMounts.migrate }
:   Type `list`, default `[]`.

`hopsworks.volumeMounts.worker` <a class="headerlink" href="#helm.hopsworks.volumeMounts.worker" title="Permanent link">#</a> { #helm.hopsworks.volumeMounts.worker }
:   Type `list`, default `[]`.

`hopsworks.volumes.admin` <a class="headerlink" href="#helm.hopsworks.volumes.admin" title="Permanent link">#</a> { #helm.hopsworks.volumes.admin }
:   Type `list`, default `[]`.

`hopsworks.volumes.migrate` <a class="headerlink" href="#helm.hopsworks.volumes.migrate" title="Permanent link">#</a> { #helm.hopsworks.volumes.migrate }
:   Type `list`, default `[]`.

`hopsworks.volumes.worker` <a class="headerlink" href="#helm.hopsworks.volumes.worker" title="Permanent link">#</a> { #helm.hopsworks.volumes.worker }
:   Type `list`, default `[]`.

</div>

## buildkitd { #helm-values-hopsworks-buildkitd }

??? example "Defaults as YAML"

    ```yaml
    hopsworks:
      buildkitd:
        gc:
          cacheMountKeepBytes: 20GiB
          cacheMountKeepDuration: 168h
          keySyntax: maxUsedSpace
          minFreeSpace: 10GiB
          totalKeepBytes: 60GiB
        image: ''
        insecureRegistries: []
        maxParallelism: 4
        name: buildkitd
        nodeSelector: {}
        podAnnotations: {}
        port: 1234
        priorityClass:
          create: true
          value: 1000000
        priorityClassName: ''
        registry: ''
        replicas: 1
        resources:
          limits:
            cpu: '8'
            memory: 16Gi
          requests:
            cpu: '8'
            memory: 16Gi
        rootless:
          deviceInjection: none
          devicePluginResource: github.com/fuse
          enabled: false
          preflight: true
          tagSuffix: -rootless
          user: 1000
        serviceAccountName: ''
        storage: 100Gi
        storageClassName: ''
        tag: ''
        tls:
          enabled: true
          locality: buildkitd
        tolerations: []
    ```

<div class="hops-values" markdown>

`hopsworks.buildkitd.gc.cacheMountKeepBytes` <a class="headerlink" href="#helm.hopsworks.buildkitd.gc.cacheMountKeepBytes" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.gc.cacheMountKeepBytes }
:   Type `string`, default `"20GiB"`.
    Budget for package cache mounts, kept separate so they cannot evict base image snapshots. Scale by the number of projects that build custom environments, not by total projects. Every size here is binary and comparable to buildkitd.storage, since the two are weighed against each other. Spell it "GiB" and not the Kubernetes "Gi": BuildKit parses these with docker/go-units, which rejects a bare "Gi" and refuses to start the daemon.

`hopsworks.buildkitd.gc.cacheMountKeepDuration` <a class="headerlink" href="#helm.hopsworks.buildkitd.gc.cacheMountKeepDuration" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.gc.cacheMountKeepDuration }
:   Type `string`, default `"168h"`.

`hopsworks.buildkitd.gc.keySyntax` <a class="headerlink" href="#helm.hopsworks.buildkitd.gc.keySyntax" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.gc.keySyntax }
:   Type `string`, default `"maxUsedSpace"`.
    Which GC key names to emit: "keepBytes" for BuildKit up to ~v0.16, "maxUsedSpace" for later releases. Must match the deployed BuildKit, and getting it wrong is silent rather than loud: v0.31.2 still accepts keepBytes, but maps it to reservedSpace, which is a floor and not a ceiling (cmd/buildkitd/config: "Deprecated: use ReservedSpace instead"). Emitting keepBytes against a modern daemon therefore turns the budget below into an amount that is guaranteed to be kept rather than never exceeded, and the state volume fills. Explicit rather than inferred from the tag, because the tag can point at a mirror of any version. Constrained by the schema: a typo used to fall through to the maxUsedSpace branch silently, which is the failure this key exists to prevent.

`hopsworks.buildkitd.gc.minFreeSpace` <a class="headerlink" href="#helm.hopsworks.buildkitd.gc.minFreeSpace" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.gc.minFreeSpace }
:   Type `string`, default `"10GiB"`.
    Free space the collector tries to leave on the volume, never going below what the policies above guarantee. The only budget here expressed against actual free space rather than against BuildKit's accounting of its own records, so it is the backstop for the daemon's other state on the volume, which no gcpolicy covers. Empty omits it.

`hopsworks.buildkitd.gc.totalKeepBytes` <a class="headerlink" href="#helm.hopsworks.buildkitd.gc.totalKeepBytes" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.gc.totalKeepBytes }
:   Type `string`, default `"60GiB"`.
    Total retained. Must stay well above the unpacked size of every base image served, and together with cacheMountKeepBytes must leave headroom under buildkitd.storage. GC is reactive, so a burst overshoots the threshold before collection catches up, and a full state volume gives ENOSPC on snapshot writes: on a ReadWriteOnce PVC recovery is volume expansion or deleting the PVC and cold-starting every base image snapshot and cache.

`hopsworks.buildkitd.image` <a class="headerlink" href="#helm.hopsworks.buildkitd.image" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.image }
:   Type `string`, default `""`.
    Daemon image name. Empty falls back to dockerRegistry.buildkit.image.

`hopsworks.buildkitd.insecureRegistries` <a class="headerlink" href="#helm.hopsworks.buildkitd.insecureRegistries" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.insecureRegistries }
:   Type `list`, default `[]`.
    Registries the daemon should treat as insecure, e.g. the in-cluster registry when it is served over plain HTTP.

`hopsworks.buildkitd.maxParallelism` <a class="headerlink" href="#helm.hopsworks.buildkitd.maxParallelism" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.maxParallelism }
:   Type `int`, default `4`.
    Concurrent build steps the daemon will run. Bounds peak memory at roughly this many per-build peaks, so overload becomes slow instead of an OOMKill that fails every in-flight build. It does not bound the number of build Jobs: further builds still hold a client pod and a blocked backend thread, so this protects the daemon rather than the cluster. Size it against memory, not CPU. BuildKit's own documented example, and conservative against a heavy wheel or CUDA build peaking near 2Gi.

`hopsworks.buildkitd.name` <a class="headerlink" href="#helm.hopsworks.buildkitd.name" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.name }
:   Type `string`, default `"buildkitd"`.

`hopsworks.buildkitd.nodeSelector` <a class="headerlink" href="#helm.hopsworks.buildkitd.nodeSelector" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.nodeSelector }
:   Type `object`, default `{}`.

`hopsworks.buildkitd.podAnnotations` <a class="headerlink" href="#helm.hopsworks.buildkitd.podAnnotations" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.podAnnotations }
:   Type `object`, default `{}`.
    Extra annotations on the daemon pod. Exists mainly for CRI-O's workload activation route: when a node scopes allowed_annotations to a \[crio.runtime.workloads.*\] table rather than a runtime handler, the pod must carry that workload's activation_annotation for the device annotation to be honoured. See values.rhel8.yaml.

`hopsworks.buildkitd.port` <a class="headerlink" href="#helm.hopsworks.buildkitd.port" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.port }
:   Type `int`, default `1234`.

`hopsworks.buildkitd.priorityClass.create` <a class="headerlink" href="#helm.hopsworks.buildkitd.priorityClass.create" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.priorityClass.create }
:   Type `bool`, default `true`.
    Create a priority class for shared Hopsworks services that user workloads depend on. The daemon needs one: it is now the pod that does the building, while its own build Jobs run at docker_operations_buildkit_priority_class. Without it the daemon sits at priority 0 and a burst of build Jobs can preempt the very daemon they are about to talk to, which fails every in-flight build including the ones that displaced it. Turning this off is only safe if the build Jobs are left at priority 0 too.

`hopsworks.buildkitd.priorityClass.value` <a class="headerlink" href="#helm.hopsworks.buildkitd.priorityClass.value" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.priorityClass.value }
:   Type `int`, default `1000000`.
    Must not be below the build Jobs' priority (docker_operations_buildkit_priority_class, 0 by default): the scheduler only preempts a lower priority, so a daemon below its own clients can be evicted by a burst of build Jobs.

`hopsworks.buildkitd.priorityClassName` <a class="headerlink" href="#helm.hopsworks.buildkitd.priorityClassName" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.priorityClassName }
:   Type `string`, default `""`.
    Priority class for the daemon. Empty uses the chart's own core-service class when priorityClass.create is on, which is the default; set a name to override it, or disable creation and leave this empty to run at priority 0 as before.

`hopsworks.buildkitd.registry` <a class="headerlink" href="#helm.hopsworks.buildkitd.registry" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.registry }
:   Type `string`, default `""`.
    Registry for the daemon image. Empty uses the chart's usual registry. Set this when the daemon runs a different BuildKit version from the per-build image, which is mirrored separately.

`hopsworks.buildkitd.replicas` <a class="headerlink" href="#helm.hopsworks.buildkitd.replicas" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.replicas }
:   Type `int`, default `1`.
    Each replica gets its own ReadWriteOnce state volume. Projects are pinned to a replica by id, so a project keeps hitting the daemon that already unpacked its base image. The address and replica count are filled in from here.  Pinning is what makes the cache useful and is also why this is not failover: a project is not retried against another replica, and a project that builds far more than the others stays on the one daemon.

`hopsworks.buildkitd.resources` <a class="headerlink" href="#helm.hopsworks.buildkitd.resources" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.resources }
:   Type `object`, default `{"limits":{"cpu":"8","memory":"16Gi"},"requests":{"cpu":"8","memory":"16Gi"}}`.
    Requests equal limits, so the daemon is Guaranteed rather than Burstable. It is the shared build bottleneck for every project, and node-pressure eviction ranks by QoS class first and then by usage above request: Burstable with a 2 CPU request and an 8 CPU limit made it both first to evict and capped at 2 CPUs of sustained capacity on a contended node, which is the opposite of what the spread suggested. Raise both together on a dedicated builder node.

`hopsworks.buildkitd.rootless.deviceInjection` <a class="headerlink" href="#helm.hopsworks.buildkitd.rootless.deviceInjection" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.rootless.deviceInjection }
:   Type `string`, default `"none"`.
    How the daemon is given /dev/fuse, which fuse-overlayfs needs. Kubernetes has no portable PodSpec equivalent of docker --device, so this is necessarily runtime-specific.    none          no device. The daemon must then use the native snapshotter, which copies                 whole layers instead of stacking them: correct, much slower, much larger.   crio          adds the io.kubernetes.cri-o.Devices annotation, which CRI-O honours.   devicePlugin  requests devicePluginResource below, for a device plugin or CDI that                 advertises /dev/fuse on upstream Kubernetes.  A plain hostPath is deliberately not offered. It makes the device node visible and leaves every open returning EPERM, which looks like it works right up until a build runs. Measured on a containerd cluster: the node appears as crw-rw-rw- and the open fails.  Asking for the fuse-overlayfs snapshotter with this set to none is refused at template time rather than deployed, since the daemon would either fail to start or quietly do something else. Nothing here is exercised on an enforcing-SELinux node yet; expect to need a matching SCC or policy there.

`hopsworks.buildkitd.rootless.devicePluginResource` <a class="headerlink" href="#helm.hopsworks.buildkitd.rootless.devicePluginResource" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.rootless.devicePluginResource }
:   Type `string`, default `"github.com/fuse"`.
    Resource requested when deviceInjection is devicePlugin. The name comes from whichever plugin or CDI provider is installed; there is no standard one. Must be a qualified extended-resource name (domain/name): an empty value would render a resources entry Kubernetes rejects, so the chart refuses it.

`hopsworks.buildkitd.rootless.enabled` <a class="headerlink" href="#helm.hopsworks.buildkitd.rootless.enabled" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.rootless.enabled }
:   Type `bool`, default `false`.
    Run the daemon as an unprivileged user instead of as root with privileged: true.  Off by default. Switching an existing install is a one-way, disruptive change: the rootless daemon keeps its state in its own subdirectory of the volume, so it starts cold and unpacks every base image again, and the rootful tree stays on the volume taking space until the volume is replaced. Switching back has the mirror-image cost. Size buildkitd.storage for one tree, not two, and give the StatefulSet a fresh volume when the extra copy does not fit.  What it costs, and this is more than a performance note. The daemon loses the process sandbox for RUN steps (--oci-worker-no-process-sandbox), which is the price of not needing privileged. A RUN step then shares the daemon's PID namespace at the same uid, so it can signal and potentially ptrace the daemon, and through /proc/<pid>/root reach the daemon's mount namespace, where the mTLS private key is. One daemon also holds every project's build state and cache.  So this mode is for a single trust zone only. Do not enable it where concurrent projects are mutually untrusted. Losing the daemon to a build step is an accepted denial of service; the credential reachability is what bounds where the mode may be used.  It buys back: no host root, no privileged container, and no hostPID, which also means a daemon cannot outlive its container and strand the state lock.  Requires a kernel that supports the configured snapshotter unprivileged. Rootless overlayfs needs 5.11 or later; below that, set variables.docker_operations_oci_worker_snapshotter to "native" and expect slower builds.  fuse-overlayfs is the faster fallback on those kernels, and it needs the daemon to actually hold /dev/fuse. See deviceInjection below: a hostPath is not enough, because access is governed by the container's device cgroup rather than by the filesystem.

`hopsworks.buildkitd.rootless.preflight` <a class="headerlink" href="#helm.hopsworks.buildkitd.rootless.preflight" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.rootless.preflight }
:   Type `bool`, default `true`.
    Run a preflight check before the daemon starts, so a node that cannot support the requested configuration fails at once and says why, rather than degrading silently. Verifies node-level facts: unprivileged user namespaces, and kernel FUSE support when the configuration actually uses FUSE (fuse-overlayfs, or any device injection). The /dev/fuse open check is not here: it runs in the daemon container's own entrypoint, because a device plugin allocates per container and the device never reaches an init container. Only meaningful when rootless is on.

`hopsworks.buildkitd.rootless.tagSuffix` <a class="headerlink" href="#helm.hopsworks.buildkitd.rootless.tagSuffix" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.rootless.tagSuffix }
:   Type `string`, default `"-rootless"`.
    Appended to the daemon image tag when rootless is on, since upstream ships the rootless daemon as a separate image variant. An explicit buildkitd.tag overrides this.

`hopsworks.buildkitd.rootless.user` <a class="headerlink" href="#helm.hopsworks.buildkitd.rootless.user" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.rootless.user }
:   Type `int`, default `1000`.
    uid and gid the rootless image runs as, and the pod's fsGroup, which is what makes the state volume and the certificate mount readable without an init container that chowns the whole volume.

`hopsworks.buildkitd.serviceAccountName` <a class="headerlink" href="#helm.hopsworks.buildkitd.serviceAccountName" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.serviceAccountName }
:   Type `string`, default `""`.
    Service account for the daemon pod. Empty runs it as the namespace default with no token mounted, which is what it needs to build. Set it only to give the daemon a cloud identity of its own, for instance an IRSA-annotated account so a registry cache export can reach S3.  The daemon's identity is not the build pod's. Builds run as hopsworks-default, so an annotation applied through defaultServiceAccount.annotations reaches them and not this StatefulSet. That distinction only appears once the daemon moves out of the build pod, and it is the reason an S3 exporter that worked daemonless can stop working here.

`hopsworks.buildkitd.storage` <a class="headerlink" href="#helm.hopsworks.buildkitd.storage" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.storage }
:   Type `string`, default `"100Gi"`.
    Must comfortably exceed the total unpacked size of the base images in use, plus the package cache. Below that, each build evicts the base image the next one needs and the cache is slower than none.

`hopsworks.buildkitd.storageClassName` <a class="headerlink" href="#helm.hopsworks.buildkitd.storageClassName" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.storageClassName }
:   Type `string`, default `""`.

`hopsworks.buildkitd.tag` <a class="headerlink" href="#helm.hopsworks.buildkitd.tag" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.tag }
:   Type `string`, default `""`.
    Daemon image tag. Empty falls back to dockerRegistry.buildkit.tag.

`hopsworks.buildkitd.tls.enabled` <a class="headerlink" href="#helm.hopsworks.buildkitd.tls.enabled" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.tls.enabled }
:   Type `bool`, default `true`.
    Require client certificates. On by default, and only worth turning off on a single-tenant install: buildctl over TCP is otherwise unauthenticated, and buildkitd gives RUN steps host networking, so a build step reaches the daemon on both the service address and 127.0.0.1 and the NetworkPolicy below does not contain it. Verified on a cluster: with mTLS the connection is closed before the API answers, and the client key lives in the build job pod rather than the RUN filesystem, so user code cannot present it.

`hopsworks.buildkitd.tls.locality` <a class="headerlink" href="#helm.hopsworks.buildkitd.tls.locality" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.tls.locality }
:   Type `string`, default `"buildkitd"`.

`hopsworks.buildkitd.tolerations` <a class="headerlink" href="#helm.hopsworks.buildkitd.tolerations" title="Permanent link">#</a> { #helm.hopsworks.buildkitd.tolerations }
:   Type `list`, default `[]`.

</div>

## create_certificate { #helm-values-hopsworks-create_certificate }

??? example "Defaults as YAML"

    ```yaml
    hopsworks:
      create_certificate:
        add: []
        auto_generate: true
        cn: hopsworks.local.ai
        configmap: payara-cacerts
        enabled: false
        secretName: hopsworks-tls
        trustManager:
          aliasPrefix: trust-manager
          configMapName: ''
          enabled: false
          key: ca-bundle.crt
    ```

<div class="hops-values" markdown>

`hopsworks.create_certificate.add` <a class="headerlink" href="#helm.hopsworks.create_certificate.add" title="Permanent link">#</a> { #helm.hopsworks.create_certificate.add }
:   Type `list`, default `[]`.
    the following list is used to add additional certificates to trust. Notice this wont work in air gapped. An example   - name: azure    url: <https://cacerts.digicert.com/DigiCertAssuredIDRootG2.crt>    alias: digicertglobalrootg2

`hopsworks.create_certificate.auto_generate` <a class="headerlink" href="#helm.hopsworks.create_certificate.auto_generate" title="Permanent link">#</a> { #helm.hopsworks.create_certificate.auto_generate }
:   Type `bool`, default `true`.

`hopsworks.create_certificate.cn` <a class="headerlink" href="#helm.hopsworks.create_certificate.cn" title="Permanent link">#</a> { #helm.hopsworks.create_certificate.cn }
:   Type `string`, default `"hopsworks.local.ai"`.

`hopsworks.create_certificate.configmap` <a class="headerlink" href="#helm.hopsworks.create_certificate.configmap" title="Permanent link">#</a> { #helm.hopsworks.create_certificate.configmap }
:   Type `string`, default `"payara-cacerts"`.

`hopsworks.create_certificate.enabled` <a class="headerlink" href="#helm.hopsworks.create_certificate.enabled" title="Permanent link">#</a> { #helm.hopsworks.create_certificate.enabled }
:   Type `bool`, default `false`.

`hopsworks.create_certificate.secretName` <a class="headerlink" href="#helm.hopsworks.create_certificate.secretName" title="Permanent link">#</a> { #helm.hopsworks.create_certificate.secretName }
:   Type `string`, default `"hopsworks-tls"`.

`hopsworks.create_certificate.trustManager.aliasPrefix` <a class="headerlink" href="#helm.hopsworks.create_certificate.trustManager.aliasPrefix" title="Permanent link">#</a> { #helm.hopsworks.create_certificate.trustManager.aliasPrefix }
:   Type `string`, default `"trust-manager"`.

`hopsworks.create_certificate.trustManager.configMapName` <a class="headerlink" href="#helm.hopsworks.create_certificate.trustManager.configMapName" title="Permanent link">#</a> { #helm.hopsworks.create_certificate.trustManager.configMapName }
:   Type `string`, default `""`.

`hopsworks.create_certificate.trustManager.enabled` <a class="headerlink" href="#helm.hopsworks.create_certificate.trustManager.enabled" title="Permanent link">#</a> { #helm.hopsworks.create_certificate.trustManager.enabled }
:   Type `bool`, default `false`.

`hopsworks.create_certificate.trustManager.key` <a class="headerlink" href="#helm.hopsworks.create_certificate.trustManager.key" title="Permanent link">#</a> { #helm.hopsworks.create_certificate.trustManager.key }
:   Type `string`, default `"ca-bundle.crt"`.

</div>

## dependencies { #helm-values-hopsworks-dependencies }

??? example "Defaults as YAML"

    ```yaml
    hopsworks:
      dependencies:
        logstash:
          consulServiceName: logstash
          port: 5044
        mysql:
          consulServiceName: mysql
          consulServiceTag: onlinefs
          port: 3306
        objectStorage:
          consulServiceName: minio
          port: 9000
        registry:
          consulServiceName: registry
          port: 30443
    ```

<div class="hops-values" markdown>

`hopsworks.dependencies.logstash.consulServiceName` <a class="headerlink" href="#helm.hopsworks.dependencies.logstash.consulServiceName" title="Permanent link">#</a> { #helm.hopsworks.dependencies.logstash.consulServiceName }
:   Type `string`, default `"logstash"`.

`hopsworks.dependencies.logstash.port` <a class="headerlink" href="#helm.hopsworks.dependencies.logstash.port" title="Permanent link">#</a> { #helm.hopsworks.dependencies.logstash.port }
:   Type `int`, default `5044`.

`hopsworks.dependencies.mysql.consulServiceName` <a class="headerlink" href="#helm.hopsworks.dependencies.mysql.consulServiceName" title="Permanent link">#</a> { #helm.hopsworks.dependencies.mysql.consulServiceName }
:   Type `string`, default `"mysql"`.

`hopsworks.dependencies.mysql.consulServiceTag` <a class="headerlink" href="#helm.hopsworks.dependencies.mysql.consulServiceTag" title="Permanent link">#</a> { #helm.hopsworks.dependencies.mysql.consulServiceTag }
:   Type `string`, default `"onlinefs"`.

`hopsworks.dependencies.mysql.port` <a class="headerlink" href="#helm.hopsworks.dependencies.mysql.port" title="Permanent link">#</a> { #helm.hopsworks.dependencies.mysql.port }
:   Type `int`, default `3306`.

`hopsworks.dependencies.objectStorage.consulServiceName` <a class="headerlink" href="#helm.hopsworks.dependencies.objectStorage.consulServiceName" title="Permanent link">#</a> { #helm.hopsworks.dependencies.objectStorage.consulServiceName }
:   Type `string`, default `"minio"`.

`hopsworks.dependencies.objectStorage.port` <a class="headerlink" href="#helm.hopsworks.dependencies.objectStorage.port" title="Permanent link">#</a> { #helm.hopsworks.dependencies.objectStorage.port }
:   Type `int`, default `9000`.

`hopsworks.dependencies.registry.consulServiceName` <a class="headerlink" href="#helm.hopsworks.dependencies.registry.consulServiceName" title="Permanent link">#</a> { #helm.hopsworks.dependencies.registry.consulServiceName }
:   Type `string`, default `"registry"`.

`hopsworks.dependencies.registry.port` <a class="headerlink" href="#helm.hopsworks.dependencies.registry.port" title="Permanent link">#</a> { #helm.hopsworks.dependencies.registry.port }
:   Type `int`, default `30443`.

</div>

## dockerImage { #helm-values-hopsworks-dockerimage }

??? example "Defaults as YAML"

    ```yaml
    hopsworks:
      dockerImage:
        apt:
          sources: []
        conda:
          default_mirrors: []
          envs_dirs:
          - /envs
          pkgs_dirs:
          - /pkgs
          proxy:
            enabled: false
            protocol: http
            url: http://proxy:3128
          repo_data_ttl: 43200
          ssl_verify: 'True'
          use_defaults: true
        configMap:
          name: docker-images-config
        packageAuth:
          caCertsConfigMap: ''
          secretName: ''
        pypi:
          global_parameters: null
          pythonDownloads: never
    ```

<div class="hops-values" markdown>

`hopsworks.dockerImage.apt.sources` <a class="headerlink" href="#helm.hopsworks.dockerImage.apt.sources" title="Permanent link">#</a> { #helm.hopsworks.dockerImage.apt.sources }
:   Type `list`, default `[]`.
    The sources will be injected in case the user wants to use a proxy repo.

`hopsworks.dockerImage.conda.default_mirrors` <a class="headerlink" href="#helm.hopsworks.dockerImage.conda.default_mirrors" title="Permanent link">#</a> { #helm.hopsworks.dockerImage.conda.default_mirrors }
:   Type `list`, default `[]`.
    the following mirrors will be injected in case the user wants to use a custom registry

`hopsworks.dockerImage.conda.envs_dirs[0]` <a class="headerlink" href="#helm.hopsworks.dockerImage.conda.envs_dirs.0" title="Permanent link">#</a> { #helm.hopsworks.dockerImage.conda.envs_dirs.0 }
:   Type `string`, default `"/envs"`.

`hopsworks.dockerImage.conda.pkgs_dirs[0]` <a class="headerlink" href="#helm.hopsworks.dockerImage.conda.pkgs_dirs.0" title="Permanent link">#</a> { #helm.hopsworks.dockerImage.conda.pkgs_dirs.0 }
:   Type `string`, default `"/pkgs"`.

`hopsworks.dockerImage.conda.proxy.enabled` <a class="headerlink" href="#helm.hopsworks.dockerImage.conda.proxy.enabled" title="Permanent link">#</a> { #helm.hopsworks.dockerImage.conda.proxy.enabled }
:   Type `bool`, default `false`.

`hopsworks.dockerImage.conda.proxy.protocol` <a class="headerlink" href="#helm.hopsworks.dockerImage.conda.proxy.protocol" title="Permanent link">#</a> { #helm.hopsworks.dockerImage.conda.proxy.protocol }
:   Type `string`, default `"http"`.

`hopsworks.dockerImage.conda.proxy.url` <a class="headerlink" href="#helm.hopsworks.dockerImage.conda.proxy.url" title="Permanent link">#</a> { #helm.hopsworks.dockerImage.conda.proxy.url }
:   Type `string`, default `"http://proxy:3128"`.

`hopsworks.dockerImage.conda.repo_data_ttl` <a class="headerlink" href="#helm.hopsworks.dockerImage.conda.repo_data_ttl" title="Permanent link">#</a> { #helm.hopsworks.dockerImage.conda.repo_data_ttl }
:   Type `int`, default `43200`.

`hopsworks.dockerImage.conda.ssl_verify` <a class="headerlink" href="#helm.hopsworks.dockerImage.conda.ssl_verify" title="Permanent link">#</a> { #helm.hopsworks.dockerImage.conda.ssl_verify }
:   Type `string`, default `"True"`.

`hopsworks.dockerImage.conda.use_defaults` <a class="headerlink" href="#helm.hopsworks.dockerImage.conda.use_defaults" title="Permanent link">#</a> { #helm.hopsworks.dockerImage.conda.use_defaults }
:   Type `bool`, default `true`.

`hopsworks.dockerImage.configMap.name` <a class="headerlink" href="#helm.hopsworks.dockerImage.configMap.name" title="Permanent link">#</a> { #helm.hopsworks.dockerImage.configMap.name }
:   Type `string`, default `"docker-images-config"`.

`hopsworks.dockerImage.packageAuth` <a class="headerlink" href="#helm.hopsworks.dockerImage.packageAuth" title="Permanent link">#</a> { #helm.hopsworks.dockerImage.packageAuth }
:   Type `object`, default `{"caCertsConfigMap":"","secretName":""}`.
    Optional Secret with credentials for authenticated pip/apt mirrors. The Secret must be created out-of-band in the Hopsworks release namespace and may contain any of the following keys (both optional):   netrc         -- mounted at $HOME/package-auth/netrc,         staged as .netrc                    into env-build contexts (used by pip/conda).   apt-auth.conf -- mounted at $HOME/package-auth/apt-auth.conf, staged as                    /etc/apt/auth.conf.d/hopsworks.conf in env-build contexts. When the Secret is absent the env-build proceeds against anonymous mirrors.

`hopsworks.dockerImage.packageAuth.caCertsConfigMap` <a class="headerlink" href="#helm.hopsworks.dockerImage.packageAuth.caCertsConfigMap" title="Permanent link">#</a> { #helm.hopsworks.dockerImage.packageAuth.caCertsConfigMap }
:   Type `string`, default `""`.
    Optional ConfigMap of trusted CA certificates to install into env-build Docker RUN steps. Each key in the ConfigMap is treated as a .crt / PEM file, bind-mounted into /usr/local/share/ca-certificates/ and installed via `update-ca-certificates` at the start of the RUN. Also exported as REQUESTS_CA_BUNDLE / SSL_CERT_FILE so pip/conda honour it. Leave empty to skip CA injection.

`hopsworks.dockerImage.packageAuth.secretName` <a class="headerlink" href="#helm.hopsworks.dockerImage.packageAuth.secretName" title="Permanent link">#</a> { #helm.hopsworks.dockerImage.packageAuth.secretName }
:   Type `string`, default `""`.
    Name of an optional Secret in the Hopsworks release namespace containing credentials for authenticated pip/apt mirrors. Leave empty to skip credential injection.

`hopsworks.dockerImage.pypi` <a class="headerlink" href="#helm.hopsworks.dockerImage.pypi" title="Permanent link">#</a> { #helm.hopsworks.dockerImage.pypi }
:   Type `object`, default `{"global_parameters":null,"pythonDownloads":"never"}`.
    pypi configurations global_parameters:   trusted-host: pypi.org   index-url: "<https://pypi.org/simple>"   extra-index-url: "<https://pypi.org/simple>"   proxy: "<http://proxy:3128>" Written verbatim to pip.conf, and translated into uv's own format in uv.toml because uv reads neither pip.conf nor PIP_INDEX_URL. These keys translate: trusted-host, proxy, index-url, extra-index-url, find-links, no-index, no-cache-dir, cache-dir, keyring-provider, index-strategy, require-hashes, pre. Anything else reaches pip only, and is listed in a comment at the end of uv.toml. timeout, retries, cert and client-cert have no uv equivalent; add trust roots through dockerImage.caCertsConfigMap instead of cert, which uv does honour. index-strategy is uv-only: pip searches every index and takes the highest version, while uv stops at the first index carrying the package. Set it to unsafe-best-match for pip's behaviour, at the cost of uv's dependency-confusion protection.

`hopsworks.dockerImage.pypi.global_parameters` <a class="headerlink" href="#helm.hopsworks.dockerImage.pypi.global_parameters" title="Permanent link">#</a> { #helm.hopsworks.dockerImage.pypi.global_parameters }
:   Type `string`, default `nil`.
    pypi global parameters

`hopsworks.dockerImage.pypi.pythonDownloads` <a class="headerlink" href="#helm.hopsworks.dockerImage.pypi.pythonDownloads" title="Permanent link">#</a> { #helm.hopsworks.dockerImage.pypi.pythonDownloads }
:   Type `string`, default `"never"`.
    uv's python-downloads. "never" is the default and the air-gap-safe value: an environment build installs against an interpreter the base image already has, so a request uv cannot satisfy locally means a broken base image, and the alternative to failing is uv silently fetching a standalone interpreter from GitHub. Relax this only on a cluster that is meant to reach the internet and wants uv to manage interpreters.

</div>

## dockerRegistry { #helm-values-hopsworks-dockerregistry }

??? example "Defaults as YAML"

    ```yaml
    hopsworks:
      dockerRegistry:
        buildkit:
          image: moby/buildkit
          tag: v0.32.2
        preset:
          affinity: {}
          alternativeRegistry: null
          configMapName: docker-images-preset-config
          enabled: true
          env: []
          extra_images: []
          maxPushRetries: 5
          nodeSelector: {}
          parallelPushes: 1
          parallelism: 3
          resources:
            limits:
              cpu: '1'
              memory: 3G
            requests:
              cpu: 100m
              memory: 500Mi
          restartPolicy: OnFailure
          retry: 50
          runIndex: 0
          secrets: []
          serviceAccount:
            annotations: {}
          timeout: 3600
          tolerations: []
          ttlSecondsAfterFinished: null
          usePullPush: true
        security:
          password: null
          trust_registry: true
          user: null
    ```

<div class="hops-values" markdown>

`hopsworks.dockerRegistry.buildkit.image` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.buildkit.image" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.buildkit.image }
:   Type `string`, default `"moby/buildkit"`.

`hopsworks.dockerRegistry.buildkit.tag` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.buildkit.tag" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.buildkit.tag }
:   Type `string`, default `"v0.32.2"`.
    Do not go below v0.31.2. Earlier releases carry published advisories, two of which matter more with the persistent daemon: a Git URL subdirectory path traversal, reachable because a library can be installed from a user-supplied Git URL, and a state-directory escape via a custom frontend, whose blast radius is every project once one daemon holds the state for all of them. Both fixed in v0.28.1; v0.31.2 also covers a Seccomp/AppArmor bypass, an unbounded-parsing DoS and a command injection through Git bundle checkout. A per-build daemon is affected the same way, so this is not a reason to leave the persistent one off.  Most of what a scanner reports on this image is the four `buildkit-cni-*` plugins, which no BuildKit release refreshes and which never run here: the image ships no CNI config, so buildkitd falls back to host networking.  The rootless variant is a separate image, used only when buildkitd.rootless.enabled is on. Both move together.  Moving this pin means revisiting buildkitd.gc.keySyntax, which is version dependent.

`hopsworks.dockerRegistry.preset.affinity` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.preset.affinity" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.preset.affinity }
:   Type `object`, default `{}`.
    affinity configuration

`hopsworks.dockerRegistry.preset.alternativeRegistry` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.preset.alternativeRegistry" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.preset.alternativeRegistry }
:   Type `string`, default `nil`.
    Alternative registry URL for base images. It will override any other global registry URL configuration.

`hopsworks.dockerRegistry.preset.configMapName` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.preset.configMapName" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.preset.configMapName }
:   Type `string`, default `"docker-images-preset-config"`.

`hopsworks.dockerRegistry.preset.enabled` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.preset.enabled" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.preset.enabled }
:   Type `bool`, default `true`.

`hopsworks.dockerRegistry.preset.env` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.preset.env" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.preset.env }
:   Type `list`, default `[]`.
    Additional env vars to be set in the preset docker images (e.g. Proxy configuration)

`hopsworks.dockerRegistry.preset.extra_images` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.preset.extra_images" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.preset.extra_images }
:   Type `list`, default `[]`.

`hopsworks.dockerRegistry.preset.maxPushRetries` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.preset.maxPushRetries" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.preset.maxPushRetries }
:   Type `int`, default `5`.

`hopsworks.dockerRegistry.preset.nodeSelector` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.preset.nodeSelector" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.preset.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

`hopsworks.dockerRegistry.preset.parallelPushes` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.preset.parallelPushes" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.preset.parallelPushes }
:   Type `int`, default `1`.

`hopsworks.dockerRegistry.preset.parallelism` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.preset.parallelism" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.preset.parallelism }
:   Type `int`, default `3`.

`hopsworks.dockerRegistry.preset.resources.limits.cpu` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.preset.resources.limits.cpu" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.preset.resources.limits.cpu }
:   Type `string`, default `"1"`.

`hopsworks.dockerRegistry.preset.resources.limits.memory` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.preset.resources.limits.memory" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.preset.resources.limits.memory }
:   Type `string`, default `"3G"`.

`hopsworks.dockerRegistry.preset.resources.requests.cpu` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.preset.resources.requests.cpu" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.preset.resources.requests.cpu }
:   Type `string`, default `"100m"`.

`hopsworks.dockerRegistry.preset.resources.requests.memory` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.preset.resources.requests.memory" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.preset.resources.requests.memory }
:   Type `string`, default `"500Mi"`.

`hopsworks.dockerRegistry.preset.restartPolicy` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.preset.restartPolicy" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.preset.restartPolicy }
:   Type `string`, default `"OnFailure"`.

`hopsworks.dockerRegistry.preset.retry` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.preset.retry" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.preset.retry }
:   Type `int`, default `50`.

`hopsworks.dockerRegistry.preset.runIndex` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.preset.runIndex" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.preset.runIndex }
:   Type `int`, default `0`.
    Index to make job names unique if necessary

`hopsworks.dockerRegistry.preset.secrets` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.preset.secrets" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.preset.secrets }
:   Type `list`, default `[]`.

`hopsworks.dockerRegistry.preset.serviceAccount.annotations` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.preset.serviceAccount.annotations" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.preset.serviceAccount.annotations }
:   Type `object`, default `{}`.
    service account annotations

`hopsworks.dockerRegistry.preset.timeout` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.preset.timeout" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.preset.timeout }
:   Type `int`, default `3600`.

`hopsworks.dockerRegistry.preset.tolerations` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.preset.tolerations" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.preset.tolerations }
:   Type `list`, default `[]`.

`hopsworks.dockerRegistry.preset.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.preset.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.preset.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    TTL in seconds for the preset-images Job. Overrides global default.

`hopsworks.dockerRegistry.preset.usePullPush` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.preset.usePullPush" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.preset.usePullPush }
:   Type `bool`, default `true`.

`hopsworks.dockerRegistry.security.password` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.security.password" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.security.password }
:   Type `string`, default `nil`.
    user password

`hopsworks.dockerRegistry.security.trust_registry` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.security.trust_registry" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.security.trust_registry }
:   Type `bool`, default `true`.

`hopsworks.dockerRegistry.security.user` <a class="headerlink" href="#helm.hopsworks.dockerRegistry.security.user" title="Permanent link">#</a> { #helm.hopsworks.dockerRegistry.security.user }
:   Type `string`, default `nil`.
    user name

</div>

## envs { #helm-values-hopsworks-envs }

??? example "Defaults as YAML"

    ```yaml
    hopsworks:
      envs:
        admin: {}
        postInstall:
          ASADMIN_DEPLOY_TIMEOUT_SEC: 900
          ASADMIN_TIMEOUT_SEC: 120
          CLEANUP_INTERVAL_SEC: 120
          DEBUG: 'true'
          DEPLOY_RETRIES: 3
          DEPLOY_RETRY_INTERVAL_SEC: 30
          INITIAL_DELAY_SEC: 60
          REGISTER_WAIT_SEC: 240
    ```

<div class="hops-values" markdown>

`hopsworks.envs.admin` <a class="headerlink" href="#helm.hopsworks.envs.admin" title="Permanent link">#</a> { #helm.hopsworks.envs.admin }
:   Type `object`, default `{}`.
    admin environment variables

`hopsworks.envs.postInstall.ASADMIN_DEPLOY_TIMEOUT_SEC` <a class="headerlink" href="#helm.hopsworks.envs.postInstall.ASADMIN_DEPLOY_TIMEOUT_SEC" title="Permanent link">#</a> { #helm.hopsworks.envs.postInstall.ASADMIN_DEPLOY_TIMEOUT_SEC }
:   Type `int`, default `900`.
    Timeout (seconds) for the asadmin deploy command. Raise it if a legitimate EAR deploy exceeds 15 minutes, but keep query + deploy timeouts well under the sidecar's 30-minute heartbeat window.

`hopsworks.envs.postInstall.ASADMIN_TIMEOUT_SEC` <a class="headerlink" href="#helm.hopsworks.envs.postInstall.ASADMIN_TIMEOUT_SEC" title="Permanent link">#</a> { #helm.hopsworks.envs.postInstall.ASADMIN_TIMEOUT_SEC }
:   Type `int`, default `120`.
    Timeout (seconds) for the admin sidecar's short asadmin calls (list-*, delete-instance), so one stuck call cannot hang its loop. The long-running deploy uses ASADMIN_DEPLOY_TIMEOUT_SEC instead.

`hopsworks.envs.postInstall.CLEANUP_INTERVAL_SEC` <a class="headerlink" href="#helm.hopsworks.envs.postInstall.CLEANUP_INTERVAL_SEC" title="Permanent link">#</a> { #helm.hopsworks.envs.postInstall.CLEANUP_INTERVAL_SEC }
:   Type `int`, default `120`.

`hopsworks.envs.postInstall.DEBUG` <a class="headerlink" href="#helm.hopsworks.envs.postInstall.DEBUG" title="Permanent link">#</a> { #helm.hopsworks.envs.postInstall.DEBUG }
:   Type `string`, default `"true"`.

`hopsworks.envs.postInstall.DEPLOY_RETRY_INTERVAL_SEC` <a class="headerlink" href="#helm.hopsworks.envs.postInstall.DEPLOY_RETRY_INTERVAL_SEC" title="Permanent link">#</a> { #helm.hopsworks.envs.postInstall.DEPLOY_RETRY_INTERVAL_SEC }
:   Type `int`, default `30`.
    Sleep (seconds) between deploy attempts in the admin sidecar. Pacing only; the sidecar keeps retrying across cycles.

`hopsworks.envs.postInstall.INITIAL_DELAY_SEC` <a class="headerlink" href="#helm.hopsworks.envs.postInstall.INITIAL_DELAY_SEC" title="Permanent link">#</a> { #helm.hopsworks.envs.postInstall.INITIAL_DELAY_SEC }
:   Type `int`, default `60`.

`hopsworks.envs.postInstall.REGISTER_WAIT_SEC` <a class="headerlink" href="#helm.hopsworks.envs.postInstall.REGISTER_WAIT_SEC" title="Permanent link">#</a> { #helm.hopsworks.envs.postInstall.REGISTER_WAIT_SEC }
:   Type `int`, default `240`.

`hopsworks.envs.postInstall.DEPLOY_RETRIES` <span class="hops-values-deprecated">Deprecated</span> <a class="headerlink" href="#helm.hopsworks.envs.postInstall.DEPLOY_RETRIES" title="Permanent link">#</a> { #helm.hopsworks.envs.postInstall.DEPLOY_RETRIES }
:   Type `int`, default `3`.
    Deprecated. No longer consumed by the admin sidecar. Use DEPLOY_RETRY_INTERVAL_SEC to control the sleep between deploy attempts. Kept for backward compatibility; will be removed in a future major version.

</div>

## hopsworksAdmin { #helm-values-hopsworks-hopsworksadmin }

??? example "Defaults as YAML"

    ```yaml
    hopsworks:
      hopsworksAdmin:
        hopsworks_ear_download_url: null
        hopsworks_front_download_url: null
        hopsworks_realm_download_url: null
        mysql_connector_download_url: null
    ```

<div class="hops-values" markdown>

`hopsworks.hopsworksAdmin` <a class="headerlink" href="#helm.hopsworks.hopsworksAdmin" title="Permanent link">#</a> { #helm.hopsworks.hopsworksAdmin }
:   Type `object`.
    override hopsworks admin artifacts

    ??? note "Default"

        ```yaml
        hopsworks_ear_download_url: null
        hopsworks_front_download_url: null
        hopsworks_realm_download_url: null
        mysql_connector_download_url: null
        ```

`hopsworks.hopsworksAdmin.hopsworks_ear_download_url` <a class="headerlink" href="#helm.hopsworks.hopsworksAdmin.hopsworks_ear_download_url" title="Permanent link">#</a> { #helm.hopsworks.hopsworksAdmin.hopsworks_ear_download_url }
:   Type `string`, default `nil`.
    use custom hopsworks ear

`hopsworks.hopsworksAdmin.hopsworks_front_download_url` <a class="headerlink" href="#helm.hopsworks.hopsworksAdmin.hopsworks_front_download_url" title="Permanent link">#</a> { #helm.hopsworks.hopsworksAdmin.hopsworks_front_download_url }
:   Type `string`, default `nil`.
    use custom hopsworks front end

`hopsworks.hopsworksAdmin.hopsworks_realm_download_url` <a class="headerlink" href="#helm.hopsworks.hopsworksAdmin.hopsworks_realm_download_url" title="Permanent link">#</a> { #helm.hopsworks.hopsworksAdmin.hopsworks_realm_download_url }
:   Type `string`, default `nil`.
    use custom hopsworks realm jar file

`hopsworks.hopsworksAdmin.mysql_connector_download_url` <a class="headerlink" href="#helm.hopsworks.hopsworksAdmin.mysql_connector_download_url" title="Permanent link">#</a> { #helm.hopsworks.hopsworksAdmin.mysql_connector_download_url }
:   Type `string`, default `nil`.
    use custom mysql connector

</div>

## hopsworksCA { #helm-values-hopsworks-hopsworksca }

??? example "Defaults as YAML"

    ```yaml
    hopsworks:
      hopsworksCA:
        affinity:
          podAntiAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - hopsworks-ca
              topologyKey: kubernetes.io/hostname
        apiKey:
          secret_name: hopsworks-api-key-auth
        auto_jvm: true
        ca_count: 1
        containerPort: 8182
        download_url: null
        extraJavaToolOptions: ''
        image:
          pullPolicy: IfNotPresent
          tag: null
        internalCert:
          subject:
            locality: glassfishinternal
            organization: 0
        jvm:
          garbageCollector: ''
          memory:
            buffer: 256
            compressedClassSpaceSize: 256
            heap: 1024
            metaspace: 1024
            nonMethodCodeHeapSize: 5
            nonProfiledCodeHeapSize: 48
            profiledCodeHeapSize: 48
        livenessProbe:
          failureThreshold: 3
          httpGet:
            path: /hopsworks-ca/v2/certificate/crl/intermediate
            port: 8182
            scheme: HTTPS
          initialDelaySeconds: 600
          periodSeconds: 20
          timeoutSeconds: 60
        name: hopsworks-ca
        readinessProbe:
          httpGet:
            path: /hopsworks-ca/v2/certificate/ready
            port: 8182
            scheme: HTTPS
          initialDelaySeconds: 60
          periodSeconds: 10
        replaceEntryPoint: false
        resources:
          limits:
            cpu: 2000m
            memory: 2048Mi
          requests:
            cpu: 1000m
            memory: 2048Mi
        securityContext: {}
        service:
          annotations:
            consul.hashicorp.com/service-name: glassfish
            consul.hashicorp.com/service-tags: ca
          name: hopsworks-ca
          port: 8182
        setupJob:
          backoffLimit: 10
        shutdownWait: 30
        startWaitTimeout: 300
    ```

<div class="hops-values" markdown>

`hopsworks.hopsworksCA.affinity` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.affinity" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.affinity }
:   Type `object`.
    Ensure we send them to different machines

    ??? note "Default"

        ```yaml
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - hopsworks-ca
            topologyKey: kubernetes.io/hostname
        ```

`hopsworks.hopsworksCA.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution }
:   Type `list`.
    podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution configuration

    ??? note "Default"

        ```yaml
        - labelSelector:
            matchExpressions:
            - key: app
              operator: In
              values:
              - hopsworks-ca
          topologyKey: kubernetes.io/hostname
        ```

`hopsworks.hopsworksCA.apiKey.secret_name` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.apiKey.secret_name" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.apiKey.secret_name }
:   Type `string`, default `"hopsworks-api-key-auth"`.

`hopsworks.hopsworksCA.auto_jvm` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.auto_jvm" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.auto_jvm }
:   Type `bool`, default `true`.

`hopsworks.hopsworksCA.ca_count` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.ca_count" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.ca_count }
:   Type `int`, default `1`.
    Number of hopsworks-ca replicas. Not rendered while hpa.ca.enabled is true; same rule as replicaCount.worker.

`hopsworks.hopsworksCA.containerPort` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.containerPort" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.containerPort }
:   Type `int`, default `8182`.

`hopsworks.hopsworksCA.download_url` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.download_url" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.download_url }
:   Type `string`, default `nil`.
    use custom hopsworks ca war

`hopsworks.hopsworksCA.extraJavaToolOptions` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.extraJavaToolOptions" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.extraJavaToolOptions }
:   Type `string`, default `""`.

`hopsworks.hopsworksCA.image.pullPolicy` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.image.pullPolicy" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.image.pullPolicy }
:   Type `string`, default `"IfNotPresent"`.

`hopsworks.hopsworksCA.image.tag` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.image.tag" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.image.tag }
:   Type `string`, default `nil`.
    image tag. If not defined, the .Chart.AppVersion will be used

`hopsworks.hopsworksCA.internalCert.subject.locality` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.internalCert.subject.locality" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.internalCert.subject.locality }
:   Type `string`, default `"glassfishinternal"`.

`hopsworks.hopsworksCA.internalCert.subject.organization` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.internalCert.subject.organization" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.internalCert.subject.organization }
:   Type `int`, default `0`.

`hopsworks.hopsworksCA.jvm.garbageCollector` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.jvm.garbageCollector" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.jvm.garbageCollector }
:   Type `string`, default `""`.

`hopsworks.hopsworksCA.jvm.memory.buffer` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.jvm.memory.buffer" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.jvm.memory.buffer }
:   Type `int`, default `256`.

`hopsworks.hopsworksCA.jvm.memory.compressedClassSpaceSize` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.jvm.memory.compressedClassSpaceSize" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.jvm.memory.compressedClassSpaceSize }
:   Type `int`, default `256`.

`hopsworks.hopsworksCA.jvm.memory.heap` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.jvm.memory.heap" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.jvm.memory.heap }
:   Type `int`, default `1024`.

`hopsworks.hopsworksCA.jvm.memory.metaspace` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.jvm.memory.metaspace" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.jvm.memory.metaspace }
:   Type `int`, default `1024`.

`hopsworks.hopsworksCA.jvm.memory.nonMethodCodeHeapSize` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.jvm.memory.nonMethodCodeHeapSize" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.jvm.memory.nonMethodCodeHeapSize }
:   Type `int`, default `5`.

`hopsworks.hopsworksCA.jvm.memory.nonProfiledCodeHeapSize` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.jvm.memory.nonProfiledCodeHeapSize" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.jvm.memory.nonProfiledCodeHeapSize }
:   Type `int`, default `48`.

`hopsworks.hopsworksCA.jvm.memory.profiledCodeHeapSize` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.jvm.memory.profiledCodeHeapSize" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.jvm.memory.profiledCodeHeapSize }
:   Type `int`, default `48`.

`hopsworks.hopsworksCA.livenessProbe.failureThreshold` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.livenessProbe.failureThreshold" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.livenessProbe.failureThreshold }
:   Type `int`, default `3`.

`hopsworks.hopsworksCA.livenessProbe.httpGet.path` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.livenessProbe.httpGet.path" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.livenessProbe.httpGet.path }
:   Type `string`, default `"/hopsworks-ca/v2/certificate/crl/intermediate"`.

`hopsworks.hopsworksCA.livenessProbe.httpGet.port` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.livenessProbe.httpGet.port" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.livenessProbe.httpGet.port }
:   Type `int`, default `8182`.

`hopsworks.hopsworksCA.livenessProbe.httpGet.scheme` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.livenessProbe.httpGet.scheme" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.livenessProbe.httpGet.scheme }
:   Type `string`, default `"HTTPS"`.

`hopsworks.hopsworksCA.livenessProbe.initialDelaySeconds` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.livenessProbe.initialDelaySeconds" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.livenessProbe.initialDelaySeconds }
:   Type `int`, default `600`.

`hopsworks.hopsworksCA.livenessProbe.periodSeconds` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.livenessProbe.periodSeconds" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.livenessProbe.periodSeconds }
:   Type `int`, default `20`.

`hopsworks.hopsworksCA.livenessProbe.timeoutSeconds` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.livenessProbe.timeoutSeconds" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.livenessProbe.timeoutSeconds }
:   Type `int`, default `60`.

`hopsworks.hopsworksCA.name` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.name" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.name }
:   Type `string`, default `"hopsworks-ca"`.

`hopsworks.hopsworksCA.readinessProbe.httpGet.path` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.readinessProbe.httpGet.path" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.readinessProbe.httpGet.path }
:   Type `string`, default `"/hopsworks-ca/v2/certificate/ready"`.

`hopsworks.hopsworksCA.readinessProbe.httpGet.port` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.readinessProbe.httpGet.port" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.readinessProbe.httpGet.port }
:   Type `int`, default `8182`.

`hopsworks.hopsworksCA.readinessProbe.httpGet.scheme` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.readinessProbe.httpGet.scheme" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.readinessProbe.httpGet.scheme }
:   Type `string`, default `"HTTPS"`.

`hopsworks.hopsworksCA.readinessProbe.initialDelaySeconds` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.readinessProbe.initialDelaySeconds" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.readinessProbe.initialDelaySeconds }
:   Type `int`, default `60`.

`hopsworks.hopsworksCA.readinessProbe.periodSeconds` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.readinessProbe.periodSeconds" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.readinessProbe.periodSeconds }
:   Type `int`, default `10`.

`hopsworks.hopsworksCA.replaceEntryPoint` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.replaceEntryPoint" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.replaceEntryPoint }
:   Type `bool`, default `false`.

`hopsworks.hopsworksCA.resources.limits.cpu` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.resources.limits.cpu" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.resources.limits.cpu }
:   Type `string`, default `"2000m"`.

`hopsworks.hopsworksCA.resources.limits.memory` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.resources.limits.memory" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.resources.limits.memory }
:   Type `string`, default `"2048Mi"`.

`hopsworks.hopsworksCA.resources.requests.cpu` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.resources.requests.cpu" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.resources.requests.cpu }
:   Type `string`, default `"1000m"`.

`hopsworks.hopsworksCA.resources.requests.memory` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.resources.requests.memory" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.resources.requests.memory }
:   Type `string`, default `"2048Mi"`.

`hopsworks.hopsworksCA.securityContext` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.securityContext" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.securityContext }
:   Type `object`, default `{}`.
    security context

`hopsworks.hopsworksCA.service.annotations."consul.hashicorp.com/service-name"` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.service.annotations.consul.hashicorp.com-service-name" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.service.annotations.consul.hashicorp.com-service-name }
:   Type `string`, default `"glassfish"`.

`hopsworks.hopsworksCA.service.annotations."consul.hashicorp.com/service-tags"` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.service.annotations.consul.hashicorp.com-service-tags" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.service.annotations.consul.hashicorp.com-service-tags }
:   Type `string`, default `"ca"`.

`hopsworks.hopsworksCA.service.name` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.service.name" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.service.name }
:   Type `string`, default `"hopsworks-ca"`.

`hopsworks.hopsworksCA.service.port` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.service.port" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.service.port }
:   Type `int`, default `8182`.

`hopsworks.hopsworksCA.setupJob.backoffLimit` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.setupJob.backoffLimit" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.setupJob.backoffLimit }
:   Type `int`, default `10`.

`hopsworks.hopsworksCA.shutdownWait` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.shutdownWait" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.shutdownWait }
:   Type `int`, default `30`.

`hopsworks.hopsworksCA.startWaitTimeout` <a class="headerlink" href="#helm.hopsworks.hopsworksCA.startWaitTimeout" title="Permanent link">#</a> { #helm.hopsworks.hopsworksCA.startWaitTimeout }
:   Type `int`, default `300`.

</div>

## hpa { #helm-values-hopsworks-hpa }

??? example "Defaults as YAML"

    ```yaml
    hopsworks:
      hpa:
        ca:
          enabled: false
          maxReplicas: 3
          targetCPUUtilizationPercentage: 80
          targetMemoryUtilizationPercentage: 95
        worker:
          enabled: false
          maxReplicas: 3
          targetCPUUtilizationPercentage: 80
          targetMemoryUtilizationPercentage: 95
    ```

<div class="hops-values" markdown>

`hopsworks.hpa.ca.enabled` <a class="headerlink" href="#helm.hopsworks.hpa.ca.enabled" title="Permanent link">#</a> { #helm.hopsworks.hpa.ca.enabled }
:   Type `bool`, default `false`.
    Autoscale hopsworks-ca. While enabled, hopsworksCA.ca_count is not rendered and the HPA owns spec.replicas.

`hopsworks.hpa.ca.maxReplicas` <a class="headerlink" href="#helm.hopsworks.hpa.ca.maxReplicas" title="Permanent link">#</a> { #helm.hopsworks.hpa.ca.maxReplicas }
:   Type `int`, default `3`.

`hopsworks.hpa.ca.targetCPUUtilizationPercentage` <a class="headerlink" href="#helm.hopsworks.hpa.ca.targetCPUUtilizationPercentage" title="Permanent link">#</a> { #helm.hopsworks.hpa.ca.targetCPUUtilizationPercentage }
:   Type `int`, default `80`.

`hopsworks.hpa.ca.targetMemoryUtilizationPercentage` <a class="headerlink" href="#helm.hopsworks.hpa.ca.targetMemoryUtilizationPercentage" title="Permanent link">#</a> { #helm.hopsworks.hpa.ca.targetMemoryUtilizationPercentage }
:   Type `int`, default `95`.

`hopsworks.hpa.worker.enabled` <a class="headerlink" href="#helm.hopsworks.hpa.worker.enabled" title="Permanent link">#</a> { #helm.hopsworks.hpa.worker.enabled }
:   Type `bool`, default `false`.
    Autoscale the Payara workers. While enabled, replicaCount.worker is not rendered and the HPA owns spec.replicas.

`hopsworks.hpa.worker.maxReplicas` <a class="headerlink" href="#helm.hopsworks.hpa.worker.maxReplicas" title="Permanent link">#</a> { #helm.hopsworks.hpa.worker.maxReplicas }
:   Type `int`, default `3`.

`hopsworks.hpa.worker.targetCPUUtilizationPercentage` <a class="headerlink" href="#helm.hopsworks.hpa.worker.targetCPUUtilizationPercentage" title="Permanent link">#</a> { #helm.hopsworks.hpa.worker.targetCPUUtilizationPercentage }
:   Type `int`, default `80`.

`hopsworks.hpa.worker.targetMemoryUtilizationPercentage` <a class="headerlink" href="#helm.hopsworks.hpa.worker.targetMemoryUtilizationPercentage" title="Permanent link">#</a> { #helm.hopsworks.hpa.worker.targetMemoryUtilizationPercentage }
:   Type `int`, default `95`.

</div>

## image { #helm-values-hopsworks-image }

??? example "Defaults as YAML"

    ```yaml
    hopsworks:
      image:
        admin:
          imageName: hopsworks
          mysqlConnectorVersion: 8.0.21.1
          mysqlStorageImageName: hopsworks-mysql-connector
          pullPolicy: IfNotPresent
          tag: null
        filebeat:
          imageName: filebeat
          tag: 8.19.21
        migration:
          pullPolicy: IfNotPresent
          tag: null
        postInstall:
          pullPolicy: IfNotPresent
          tag: 6.2025.11-jdk21.0
        registry: null
        worker:
          pullPolicy: IfNotPresent
          tag: 6.2025.11-jdk21.0
    ```

<div class="hops-values" markdown>

`hopsworks.image.admin.imageName` <a class="headerlink" href="#helm.hopsworks.image.admin.imageName" title="Permanent link">#</a> { #helm.hopsworks.image.admin.imageName }
:   Type `string`, default `"hopsworks"`.

`hopsworks.image.admin.mysqlConnectorVersion` <a class="headerlink" href="#helm.hopsworks.image.admin.mysqlConnectorVersion" title="Permanent link">#</a> { #helm.hopsworks.image.admin.mysqlConnectorVersion }
:   Type `string`, default `"8.0.21.1"`.

`hopsworks.image.admin.mysqlStorageImageName` <a class="headerlink" href="#helm.hopsworks.image.admin.mysqlStorageImageName" title="Permanent link">#</a> { #helm.hopsworks.image.admin.mysqlStorageImageName }
:   Type `string`, default `"hopsworks-mysql-connector"`.

`hopsworks.image.admin.pullPolicy` <a class="headerlink" href="#helm.hopsworks.image.admin.pullPolicy" title="Permanent link">#</a> { #helm.hopsworks.image.admin.pullPolicy }
:   Type `string`, default `"IfNotPresent"`.

`hopsworks.image.admin.tag` <a class="headerlink" href="#helm.hopsworks.image.admin.tag" title="Permanent link">#</a> { #helm.hopsworks.image.admin.tag }
:   Type `string`, default `nil`.
    image tag. If not defined, the .Chart.AppVersion will be used

`hopsworks.image.filebeat.imageName` <a class="headerlink" href="#helm.hopsworks.image.filebeat.imageName" title="Permanent link">#</a> { #helm.hopsworks.image.filebeat.imageName }
:   Type `string`, default `"filebeat"`.

`hopsworks.image.filebeat.tag` <a class="headerlink" href="#helm.hopsworks.image.filebeat.tag" title="Permanent link">#</a> { #helm.hopsworks.image.filebeat.tag }
:   Type `string`, default `"8.19.21"`.

`hopsworks.image.migration.pullPolicy` <a class="headerlink" href="#helm.hopsworks.image.migration.pullPolicy" title="Permanent link">#</a> { #helm.hopsworks.image.migration.pullPolicy }
:   Type `string`, default `"IfNotPresent"`.

`hopsworks.image.migration.tag` <a class="headerlink" href="#helm.hopsworks.image.migration.tag" title="Permanent link">#</a> { #helm.hopsworks.image.migration.tag }
:   Type `string`, default `nil`.
    image tag. If not defined, the .Chart.AppVersion will be used

`hopsworks.image.postInstall.pullPolicy` <a class="headerlink" href="#helm.hopsworks.image.postInstall.pullPolicy" title="Permanent link">#</a> { #helm.hopsworks.image.postInstall.pullPolicy }
:   Type `string`, default `"IfNotPresent"`.
    pull policy for the admin sidecar's payara-node image. admindeployment.yaml already read this key before it was declared here, and its fallback cannot reach global._hopsworks.imagePullPolicy, so the sidecar was pinned to IfNotPresent with no way to override it.

`hopsworks.image.postInstall.tag` <a class="headerlink" href="#helm.hopsworks.image.postInstall.tag" title="Permanent link">#</a> { #helm.hopsworks.image.postInstall.tag }
:   Type `string`, default `"6.2025.11-jdk21.0"`.

`hopsworks.image.registry` <a class="headerlink" href="#helm.hopsworks.image.registry" title="Permanent link">#</a> { #helm.hopsworks.image.registry }
:   Type `string`, default `nil`.
    image registry. If not defined, the global._hopsworks.imageRegistry will be used instead

`hopsworks.image.worker.pullPolicy` <a class="headerlink" href="#helm.hopsworks.image.worker.pullPolicy" title="Permanent link">#</a> { #helm.hopsworks.image.worker.pullPolicy }
:   Type `string`, default `"IfNotPresent"`.

`hopsworks.image.worker.tag` <a class="headerlink" href="#helm.hopsworks.image.worker.tag" title="Permanent link">#</a> { #helm.hopsworks.image.worker.tag }
:   Type `string`, default `"6.2025.11-jdk21.0"`.

</div>

## ingress { #helm-values-hopsworks-ingress }

??? example "Defaults as YAML"

    ```yaml
    hopsworks:
      ingress:
        annotations:
          nginx.ingress.kubernetes.io/affinity: cookie
          nginx.ingress.kubernetes.io/affinity-mode: persistent
          nginx.ingress.kubernetes.io/proxy-body-size: '0'
          nginx.ingress.kubernetes.io/proxy-redirect-from: 'http:'
          nginx.ingress.kubernetes.io/proxy-redirect-to: 'https:'
          nginx.ingress.kubernetes.io/session-cookie-expires: '5259600'
          nginx.ingress.kubernetes.io/session-cookie-max-age: '5259600'
          nginx.ingress.kubernetes.io/ssl-redirect: 'true'
        enabled: true
        extraLabels: {}
        extraPaths: []
        host: hopsworks.ai.local
        hosts:
        - hopsworks.ai.local
        ingressClassName: nginx
        path: /
        pathType: Prefix
        secretName: hopsworks-ingress-crypto-material
        servicePort: 28080
        sslPassthrough: false
        tls:
        - hosts:
          - hopsworks.ai.local
          secretName: hopsworks-ingress-crypto-material
    ```

<div class="hops-values" markdown>

`hopsworks.ingress.annotations` <a class="headerlink" href="#helm.hopsworks.ingress.annotations" title="Permanent link">#</a> { #helm.hopsworks.ingress.annotations }
:   Type `object`.
    ingress annotations

    ??? note "Default"

        ```yaml
        nginx.ingress.kubernetes.io/affinity: cookie
        nginx.ingress.kubernetes.io/affinity-mode: persistent
        nginx.ingress.kubernetes.io/proxy-body-size: '0'
        nginx.ingress.kubernetes.io/proxy-redirect-from: 'http:'
        nginx.ingress.kubernetes.io/proxy-redirect-to: 'https:'
        nginx.ingress.kubernetes.io/session-cookie-expires: '5259600'
        nginx.ingress.kubernetes.io/session-cookie-max-age: '5259600'
        nginx.ingress.kubernetes.io/ssl-redirect: 'true'
        ```

`hopsworks.ingress.enabled` <a class="headerlink" href="#helm.hopsworks.ingress.enabled" title="Permanent link">#</a> { #helm.hopsworks.ingress.enabled }
:   Type `bool`, default `true`.

`hopsworks.ingress.extraLabels` <a class="headerlink" href="#helm.hopsworks.ingress.extraLabels" title="Permanent link">#</a> { #helm.hopsworks.ingress.extraLabels }
:   Type `object`, default `{}`.
    ingress extra labels

`hopsworks.ingress.extraPaths` <a class="headerlink" href="#helm.hopsworks.ingress.extraPaths" title="Permanent link">#</a> { #helm.hopsworks.ingress.extraPaths }
:   Type `list`, default `[]`.

`hopsworks.ingress.host` <a class="headerlink" href="#helm.hopsworks.ingress.host" title="Permanent link">#</a> { #helm.hopsworks.ingress.host }
:   Type `string`, default `"hopsworks.ai.local"`.

`hopsworks.ingress.hosts` <a class="headerlink" href="#helm.hopsworks.ingress.hosts" title="Permanent link">#</a> { #helm.hopsworks.ingress.hosts }
:   Type `list`, default `["hopsworks.ai.local"]`.
    ingress hosts configuration

`hopsworks.ingress.ingressClassName` <a class="headerlink" href="#helm.hopsworks.ingress.ingressClassName" title="Permanent link">#</a> { #helm.hopsworks.ingress.ingressClassName }
:   Type `string`, default `"nginx"`.

`hopsworks.ingress.path` <a class="headerlink" href="#helm.hopsworks.ingress.path" title="Permanent link">#</a> { #helm.hopsworks.ingress.path }
:   Type `string`, default `"/"`.

`hopsworks.ingress.pathType` <a class="headerlink" href="#helm.hopsworks.ingress.pathType" title="Permanent link">#</a> { #helm.hopsworks.ingress.pathType }
:   Type `string`, default `"Prefix"`.

`hopsworks.ingress.secretName` <a class="headerlink" href="#helm.hopsworks.ingress.secretName" title="Permanent link">#</a> { #helm.hopsworks.ingress.secretName }
:   Type `string`, default `"hopsworks-ingress-crypto-material"`.

`hopsworks.ingress.servicePort` <a class="headerlink" href="#helm.hopsworks.ingress.servicePort" title="Permanent link">#</a> { #helm.hopsworks.ingress.servicePort }
:   Type `int`, default `28080`.

`hopsworks.ingress.sslPassthrough` <a class="headerlink" href="#helm.hopsworks.ingress.sslPassthrough" title="Permanent link">#</a> { #helm.hopsworks.ingress.sslPassthrough }
:   Type `bool`, default `false`.

`hopsworks.ingress.tls` <a class="headerlink" href="#helm.hopsworks.ingress.tls" title="Permanent link">#</a> { #helm.hopsworks.ingress.tls }
:   Type `list`.
    ingress tls configuration per host

    ??? note "Default"

        ```yaml
        - hosts:
          - hopsworks.ai.local
          secretName: hopsworks-ingress-crypto-material
        ```

</div>

## payara { #helm-values-hopsworks-payara }

??? example "Defaults as YAML"

    ```yaml
    hopsworks:
      payara:
        adminpwKeyName: admin_password
        adminuser: admin
        config: hopsworks-config
        debug: false
        deploymentGroup: hopsworks-dg
        disableMetricsServiceLogs: false
        disableXmlValidation: true
        encryptionpwKeyName: encryption_master_password
        http:
          keep_alive_timeout: 30
        httpListener1Enabled: true
        httpthreadpool:
          idletimeout: 900
          maxqueuesize: 4096
          maxthreadpoolsize: 200
          minthreadpoolsize: 5
        kerberos:
          enabled: false
          keyTabName: service.keytab
          keyTabPath: /etc/security/keytabs
          keyTabPrincipal: HTTP/hopsworks.cluster.local@EXAMPLE.COM
          keyTabSecretName: keytab-secret
          krb5ConfigName: server-krb5-config
        ldap:
          enabled: false
          factory_class: com.sun.jndi.ldap.LdapCtxFactory
          jndilookupname: dc=example,dc=com
          property:
            additional_props:
            - key: hopsworks\.ldap\.basedn
              value: dc=example,dc=com
            attributes_binary: entryUUID
            provider_url: ldap://192.168.200.104:389
            referral: ignore
            security:
              authentication: simple
              credentials:
                secret_key: credentials
                secret_name: ldap-credentials-secret
              principal: cn=admin,dc=example,dc=com
          res_type: javax.naming.ldap.LdapContext
        mail:
          email: smtp@gmail.com
          from: admin@hopsworks.ai
          password:
            secret_key: payara-mail-password
          smtp: smtp.gmail.com
          smtp_port: '587'
          smtp_ssl_port: '465'
        oauth:
          clients: []
          enabled: false
        postbootCommands: /opt/payara/k8s/commands/post-boot-commands.asadmin
        prebootCommands: /opt/payara/k8s/commands/pre-boot-commands.asadmin
        uniformLogFormatter: false
        versionUpgrade: null
        websocketProxy:
          grizzlyWorkerPoolMaxSize: 200
          heartbeatIntervalMs: 20000
          incomingBufferBytes: 33554432
          maxSessionsPerApp: 500
          sessionIdleTimeoutMs: 0
    ```

<div class="hops-values" markdown>

`hopsworks.payara.adminpwKeyName` <a class="headerlink" href="#helm.hopsworks.payara.adminpwKeyName" title="Permanent link">#</a> { #helm.hopsworks.payara.adminpwKeyName }
:   Type `string`, default `"admin_password"`.

`hopsworks.payara.adminuser` <a class="headerlink" href="#helm.hopsworks.payara.adminuser" title="Permanent link">#</a> { #helm.hopsworks.payara.adminuser }
:   Type `string`, default `"admin"`.

`hopsworks.payara.config` <a class="headerlink" href="#helm.hopsworks.payara.config" title="Permanent link">#</a> { #helm.hopsworks.payara.config }
:   Type `string`, default `"hopsworks-config"`.

`hopsworks.payara.debug` <a class="headerlink" href="#helm.hopsworks.payara.debug" title="Permanent link">#</a> { #helm.hopsworks.payara.debug }
:   Type `bool`, default `false`.

`hopsworks.payara.deploymentGroup` <a class="headerlink" href="#helm.hopsworks.payara.deploymentGroup" title="Permanent link">#</a> { #helm.hopsworks.payara.deploymentGroup }
:   Type `string`, default `"hopsworks-dg"`.

`hopsworks.payara.disableMetricsServiceLogs` <a class="headerlink" href="#helm.hopsworks.payara.disableMetricsServiceLogs" title="Permanent link">#</a> { #helm.hopsworks.payara.disableMetricsServiceLogs }
:   Type `bool`, default `false`.

`hopsworks.payara.disableXmlValidation` <a class="headerlink" href="#helm.hopsworks.payara.disableXmlValidation" title="Permanent link">#</a> { #helm.hopsworks.payara.disableXmlValidation }
:   Type `bool`, default `true`.

`hopsworks.payara.encryptionpwKeyName` <a class="headerlink" href="#helm.hopsworks.payara.encryptionpwKeyName" title="Permanent link">#</a> { #helm.hopsworks.payara.encryptionpwKeyName }
:   Type `string`, default `"encryption_master_password"`.

`hopsworks.payara.http.keep_alive_timeout` <a class="headerlink" href="#helm.hopsworks.payara.http.keep_alive_timeout" title="Permanent link">#</a> { #helm.hopsworks.payara.http.keep_alive_timeout }
:   Type `int`, default `30`.

`hopsworks.payara.httpListener1Enabled` <a class="headerlink" href="#helm.hopsworks.payara.httpListener1Enabled" title="Permanent link">#</a> { #helm.hopsworks.payara.httpListener1Enabled }
:   Type `bool`, default `true`.

`hopsworks.payara.httpthreadpool.idletimeout` <a class="headerlink" href="#helm.hopsworks.payara.httpthreadpool.idletimeout" title="Permanent link">#</a> { #helm.hopsworks.payara.httpthreadpool.idletimeout }
:   Type `int`, default `900`.
    The maximum amount of time that a thread can remain idle in the pool. After this time expires, the thread is removed from the pool.

`hopsworks.payara.httpthreadpool.maxqueuesize` <a class="headerlink" href="#helm.hopsworks.payara.httpthreadpool.maxqueuesize" title="Permanent link">#</a> { #helm.hopsworks.payara.httpthreadpool.maxqueuesize }
:   Type `int`, default `4096`.
    The maximum number of threads in the queue. A value of -1 indicates that there is no limit to the queue size.

`hopsworks.payara.httpthreadpool.maxthreadpoolsize` <a class="headerlink" href="#helm.hopsworks.payara.httpthreadpool.maxthreadpoolsize" title="Permanent link">#</a> { #helm.hopsworks.payara.httpthreadpool.maxthreadpoolsize }
:   Type `int`, default `200`.

`hopsworks.payara.httpthreadpool.minthreadpoolsize` <a class="headerlink" href="#helm.hopsworks.payara.httpthreadpool.minthreadpoolsize" title="Permanent link">#</a> { #helm.hopsworks.payara.httpthreadpool.minthreadpoolsize }
:   Type `int`, default `5`.

`hopsworks.payara.kerberos.enabled` <a class="headerlink" href="#helm.hopsworks.payara.kerberos.enabled" title="Permanent link">#</a> { #helm.hopsworks.payara.kerberos.enabled }
:   Type `bool`, default `false`.

`hopsworks.payara.kerberos.keyTabName` <a class="headerlink" href="#helm.hopsworks.payara.kerberos.keyTabName" title="Permanent link">#</a> { #helm.hopsworks.payara.kerberos.keyTabName }
:   Type `string`, default `"service.keytab"`.
    kerberos service principal keytab name.

`hopsworks.payara.kerberos.keyTabPath` <a class="headerlink" href="#helm.hopsworks.payara.kerberos.keyTabPath" title="Permanent link">#</a> { #helm.hopsworks.payara.kerberos.keyTabPath }
:   Type `string`, default `"/etc/security/keytabs"`.
    kerberos service principal keytab file path.

`hopsworks.payara.kerberos.keyTabPrincipal` <a class="headerlink" href="#helm.hopsworks.payara.kerberos.keyTabPrincipal" title="Permanent link">#</a> { #helm.hopsworks.payara.kerberos.keyTabPrincipal }
:   Type `string`, default `"HTTP/hopsworks.cluster.local@EXAMPLE.COM"`.
    kerberos service principal name. This name is created by combining the string HTTP with the hostname 'HTTP@host_name'. The host name is the DNS name by which browsers contact the Web server. Use the fully qualified host name.

`hopsworks.payara.kerberos.keyTabSecretName` <a class="headerlink" href="#helm.hopsworks.payara.kerberos.keyTabSecretName" title="Permanent link">#</a> { #helm.hopsworks.payara.kerberos.keyTabSecretName }
:   Type `string`, default `"keytab-secret"`.
    keytab secret name.

`hopsworks.payara.kerberos.krb5ConfigName` <a class="headerlink" href="#helm.hopsworks.payara.kerberos.krb5ConfigName" title="Permanent link">#</a> { #helm.hopsworks.payara.kerberos.krb5ConfigName }
:   Type `string`, default `"server-krb5-config"`.
    krb5.conf config map name.

`hopsworks.payara.ldap.enabled` <a class="headerlink" href="#helm.hopsworks.payara.ldap.enabled" title="Permanent link">#</a> { #helm.hopsworks.payara.ldap.enabled }
:   Type `bool`, default `false`.

`hopsworks.payara.ldap.factory_class` <a class="headerlink" href="#helm.hopsworks.payara.ldap.factory_class" title="Permanent link">#</a> { #helm.hopsworks.payara.ldap.factory_class }
:   Type `string`, default `"com.sun.jndi.ldap.LdapCtxFactory"`.
    Factory class for resource; implements javax.naming.spi.ObjectFactory.

`hopsworks.payara.ldap.jndilookupname` <a class="headerlink" href="#helm.hopsworks.payara.ldap.jndilookupname" title="Permanent link">#</a> { #helm.hopsworks.payara.ldap.jndilookupname }
:   Type `string`, default `"dc=example,dc=com"`.
    Name used by the application to find the resource.

`hopsworks.payara.ldap.property.additional_props[0].key` <a class="headerlink" href="#helm.hopsworks.payara.ldap.property.additional_props.0.key" title="Permanent link">#</a> { #helm.hopsworks.payara.ldap.property.additional_props.0.key }
:   Type `string`, default `"hopsworks\\.ldap\\.basedn"`.

`hopsworks.payara.ldap.property.additional_props[0].value` <a class="headerlink" href="#helm.hopsworks.payara.ldap.property.additional_props.0.value" title="Permanent link">#</a> { #helm.hopsworks.payara.ldap.property.additional_props.0.value }
:   Type `string`, default `"dc=example,dc=com"`.

`hopsworks.payara.ldap.property.attributes_binary` <a class="headerlink" href="#helm.hopsworks.payara.ldap.property.attributes_binary" title="Permanent link">#</a> { #helm.hopsworks.payara.ldap.property.attributes_binary }
:   Type `string`, default `"entryUUID"`.
    The binary unique identifier that will be used in subsequent logins to identify the user.

`hopsworks.payara.ldap.property.provider_url` <a class="headerlink" href="#helm.hopsworks.payara.ldap.property.provider_url" title="Permanent link">#</a> { #helm.hopsworks.payara.ldap.property.provider_url }
:   Type `string`, default `"ldap://192.168.200.104:389"`.

`hopsworks.payara.ldap.property.referral` <a class="headerlink" href="#helm.hopsworks.payara.ldap.property.referral" title="Permanent link">#</a> { #helm.hopsworks.payara.ldap.property.referral }
:   Type `string`, default `"ignore"`.
    Whether to follow or ignore an alternate location in which an LDAP request may be processed.

`hopsworks.payara.ldap.property.security.authentication` <a class="headerlink" href="#helm.hopsworks.payara.ldap.property.security.authentication" title="Permanent link">#</a> { #helm.hopsworks.payara.ldap.property.security.authentication }
:   Type `string`, default `"simple"`.

`hopsworks.payara.ldap.property.security.credentials.secret_key` <a class="headerlink" href="#helm.hopsworks.payara.ldap.property.security.credentials.secret_key" title="Permanent link">#</a> { #helm.hopsworks.payara.ldap.property.security.credentials.secret_key }
:   Type `string`, default `"credentials"`.

`hopsworks.payara.ldap.property.security.credentials.secret_name` <a class="headerlink" href="#helm.hopsworks.payara.ldap.property.security.credentials.secret_name" title="Permanent link">#</a> { #helm.hopsworks.payara.ldap.property.security.credentials.secret_name }
:   Type `string`, default `"ldap-credentials-secret"`.

`hopsworks.payara.ldap.property.security.principal` <a class="headerlink" href="#helm.hopsworks.payara.ldap.property.security.principal" title="Permanent link">#</a> { #helm.hopsworks.payara.ldap.property.security.principal }
:   Type `string`, default `"cn=admin,dc=example,dc=com"`.

`hopsworks.payara.ldap.res_type` <a class="headerlink" href="#helm.hopsworks.payara.ldap.res_type" title="Permanent link">#</a> { #helm.hopsworks.payara.ldap.res_type }
:   Type `string`, default `"javax.naming.ldap.LdapContext"`.
    Resource Type. Enter a fully qualified type following the format xxx.xxx (for example, javax.jms.Topic)

`hopsworks.payara.mail.email` <a class="headerlink" href="#helm.hopsworks.payara.mail.email" title="Permanent link">#</a> { #helm.hopsworks.payara.mail.email }
:   Type `string`, default `"smtp@gmail.com"`.

`hopsworks.payara.mail.from` <a class="headerlink" href="#helm.hopsworks.payara.mail.from" title="Permanent link">#</a> { #helm.hopsworks.payara.mail.from }
:   Type `string`, default `"admin@hopsworks.ai"`.

`hopsworks.payara.mail.password.secret_key` <a class="headerlink" href="#helm.hopsworks.payara.mail.password.secret_key" title="Permanent link">#</a> { #helm.hopsworks.payara.mail.password.secret_key }
:   Type `string`, default `"payara-mail-password"`.

`hopsworks.payara.mail.smtp` <a class="headerlink" href="#helm.hopsworks.payara.mail.smtp" title="Permanent link">#</a> { #helm.hopsworks.payara.mail.smtp }
:   Type `string`, default `"smtp.gmail.com"`.

`hopsworks.payara.mail.smtp_port` <a class="headerlink" href="#helm.hopsworks.payara.mail.smtp_port" title="Permanent link">#</a> { #helm.hopsworks.payara.mail.smtp_port }
:   Type `string`, default `"587"`.

`hopsworks.payara.mail.smtp_ssl_port` <a class="headerlink" href="#helm.hopsworks.payara.mail.smtp_ssl_port" title="Permanent link">#</a> { #helm.hopsworks.payara.mail.smtp_ssl_port }
:   Type `string`, default `"465"`.

`hopsworks.payara.oauth.clients` <a class="headerlink" href="#helm.hopsworks.payara.oauth.clients" title="Permanent link">#</a> { #helm.hopsworks.payara.oauth.clients }
:   Type `list`, default `[]`.
    oauth clients

`hopsworks.payara.oauth.enabled` <a class="headerlink" href="#helm.hopsworks.payara.oauth.enabled" title="Permanent link">#</a> { #helm.hopsworks.payara.oauth.enabled }
:   Type `bool`, default `false`.

`hopsworks.payara.postbootCommands` <a class="headerlink" href="#helm.hopsworks.payara.postbootCommands" title="Permanent link">#</a> { #helm.hopsworks.payara.postbootCommands }
:   Type `string`, default `"/opt/payara/k8s/commands/post-boot-commands.asadmin"`.

`hopsworks.payara.prebootCommands` <a class="headerlink" href="#helm.hopsworks.payara.prebootCommands" title="Permanent link">#</a> { #helm.hopsworks.payara.prebootCommands }
:   Type `string`, default `"/opt/payara/k8s/commands/pre-boot-commands.asadmin"`.

`hopsworks.payara.uniformLogFormatter` <a class="headerlink" href="#helm.hopsworks.payara.uniformLogFormatter" title="Permanent link">#</a> { #helm.hopsworks.payara.uniformLogFormatter }
:   Type `bool`, default `false`.

`hopsworks.payara.versionUpgrade` <a class="headerlink" href="#helm.hopsworks.payara.versionUpgrade" title="Permanent link">#</a> { #helm.hopsworks.payara.versionUpgrade }
:   Type `string`, default `nil`.
    is Payara version upgrade. If null, auto detect based on current and target version

`hopsworks.payara.websocketProxy` <a class="headerlink" href="#helm.hopsworks.payara.websocketProxy" title="Permanent link">#</a> { #helm.hopsworks.payara.websocketProxy }
:   Type `object`.
    Tyrus WebSocket-proxy tuning (jupyter / terminal / python-app). These five values are the single source of truth: post-boot-commands.txt passes each as a JVM system property (-D) which hopsworks-ee reads (WebSocketProxyConfig).

    ??? note "Default"

        ```yaml
        grizzlyWorkerPoolMaxSize: 200
        heartbeatIntervalMs: 20000
        incomingBufferBytes: 33554432
        maxSessionsPerApp: 500
        sessionIdleTimeoutMs: 0
        ```

`hopsworks.payara.websocketProxy.grizzlyWorkerPoolMaxSize` <a class="headerlink" href="#helm.hopsworks.payara.websocketProxy.grizzlyWorkerPoolMaxSize" title="Permanent link">#</a> { #helm.hopsworks.payara.websocketProxy.grizzlyWorkerPoolMaxSize }
:   Type `int`, default `200`.
    Upper bound on the shared Tyrus/Grizzly client transport worker pool. Bounded to 1..Integer.MAX_VALUE (read via Integer.getInteger).

`hopsworks.payara.websocketProxy.heartbeatIntervalMs` <a class="headerlink" href="#helm.hopsworks.payara.websocketProxy.heartbeatIntervalMs" title="Permanent link">#</a> { #helm.hopsworks.payara.websocketProxy.heartbeatIntervalMs }
:   Type `int`, default `20000`.
    Interval, in milliseconds, of the Tyrus per-session heartbeat on the inbound (browser) WebSocket leg. The browser hop traverses ingress-nginx, whose proxy_read_timeout (default 60s) reaps a WebSocket idle for that long; Tyrus emits an unsolicited pong every interval to keep it warm. Keep below the ingress timeout. 0 disables. Read via Long.getLong, so only a non-negative lower bound is enforced.

`hopsworks.payara.websocketProxy.incomingBufferBytes` <a class="headerlink" href="#helm.hopsworks.payara.websocketProxy.incomingBufferBytes" title="Permanent link">#</a> { #helm.hopsworks.payara.websocketProxy.incomingBufferBytes }
:   Type `int`, default `33554432`.
    Max size, in bytes, of a single received WebSocket frame on the upstream leg — the ceiling a large Jupyter cell output must fit under. Grown on demand, not pre-allocated. Keep at or above jupyter's iopub rate-limit budget. Bounded to 1..Integer.MAX_VALUE (read via Integer.getInteger).

`hopsworks.payara.websocketProxy.maxSessionsPerApp` <a class="headerlink" href="#helm.hopsworks.payara.websocketProxy.maxSessionsPerApp" title="Permanent link">#</a> { #helm.hopsworks.payara.websocketProxy.maxSessionsPerApp }
:   Type `int`, default `500`.
    Max concurrent inbound WebSocket proxy sessions per pod (jupyter, terminal and python-app share this budget). The next upgrade past the cap is closed with 1013 TRY_AGAIN_LATER, protecting the pod from connection-driven OOM. Read via Integer.getInteger in hopsworks-ee, so values outside the int range would be silently ignored — bounded to 1..Integer.MAX_VALUE here.

`hopsworks.payara.websocketProxy.sessionIdleTimeoutMs` <a class="headerlink" href="#helm.hopsworks.payara.websocketProxy.sessionIdleTimeoutMs" title="Permanent link">#</a> { #helm.hopsworks.payara.websocketProxy.sessionIdleTimeoutMs }
:   Type `int`, default `0`.
    Per-session idle timeout in milliseconds. 0 disables the idle reaper (proxy sessions are legitimately long-lived). Read via Long.getLong, so only a non-negative lower bound is enforced.

</div>

## probs { #helm-values-hopsworks-probs }

??? example "Defaults as YAML"

    ```yaml
    hopsworks:
      probs:
        admin:
          livenessProbe:
            exec:
              command:
              - /bin/sh
              - /opt/payara/k8s/ready.sh
            failureThreshold: 10
            periodSeconds: 60
            timeoutSeconds: 30
          readinessProbe:
            exec:
              command:
              - /bin/sh
              - /opt/payara/k8s/ready.sh
            initialDelaySeconds: 90
            periodSeconds: 10
            timeoutSeconds: 30
          startupProbe:
            exec:
              command:
              - /bin/sh
              - /opt/payara/k8s/ready.sh
            failureThreshold: 180
            periodSeconds: 10
            timeoutSeconds: 30
        worker:
          livenessProbe:
            failureThreshold: 3
            httpGet:
              path: /hopsworks-api/api/variables/versions
              port: 8182
              scheme: HTTPS
            initialDelaySeconds: 150
            periodSeconds: 20
            timeoutSeconds: 20
          readinessProbe:
            httpGet:
              path: /hopsworks-api/api/variables/versions
              port: 8182
              scheme: HTTPS
            initialDelaySeconds: 150
            periodSeconds: 10
          startupProbe:
            failureThreshold: 10
            httpGet:
              path: /health
              port: 8182
              scheme: HTTPS
            initialDelaySeconds: 150
            periodSeconds: 10
    ```

<div class="hops-values" markdown>

`hopsworks.probs.admin.livenessProbe` <a class="headerlink" href="#helm.hopsworks.probs.admin.livenessProbe" title="Permanent link">#</a> { #helm.hopsworks.probs.admin.livenessProbe }
:   Type `object`.
    liveness probe. Restarts the DAS if it stays unresponsive for ~10 minutes (10 x 60s); without it a hung DAS is never restarted. The long window is deliberate: it must not fire on slowness, and each run costs an asadmin JVM inside the DAS container. Set to null to disable. If you override with httpGet/tcpSocket, also set `exec: null` (Helm merges maps; a probe allows only one handler).

    ??? note "Default"

        ```yaml
        exec:
          command:
          - /bin/sh
          - /opt/payara/k8s/ready.sh
        failureThreshold: 10
        periodSeconds: 60
        timeoutSeconds: 30
        ```

`hopsworks.probs.admin.livenessProbe.exec` <a class="headerlink" href="#helm.hopsworks.probs.admin.livenessProbe.exec" title="Permanent link">#</a> { #helm.hopsworks.probs.admin.livenessProbe.exec }
:   Type `object`, default `{"command":["/bin/sh","/opt/payara/k8s/ready.sh"]}`.
    exec probe handler. Set to null when overriding the probe with httpGet/tcpSocket (Helm merges maps; a probe allows only one handler).

`hopsworks.probs.admin.readinessProbe` <a class="headerlink" href="#helm.hopsworks.probs.admin.readinessProbe" title="Permanent link">#</a> { #helm.hopsworks.probs.admin.readinessProbe }
:   Type `object`.
    readiness probe. Controls the admin pod's Ready state and so the hopsworks-admin Service endpoint that workers use to reach the DAS. ready.sh only checks that the DAS admin interface responds. Short 10s period on purpose — this is the probe that must react fast; liveness samples slower. If you override with httpGet/tcpSocket, also set `exec: null`.

    ??? note "Default"

        ```yaml
        exec:
          command:
          - /bin/sh
          - /opt/payara/k8s/ready.sh
        initialDelaySeconds: 90
        periodSeconds: 10
        timeoutSeconds: 30
        ```

`hopsworks.probs.admin.readinessProbe.exec` <a class="headerlink" href="#helm.hopsworks.probs.admin.readinessProbe.exec" title="Permanent link">#</a> { #helm.hopsworks.probs.admin.readinessProbe.exec }
:   Type `object`, default `{"command":["/bin/sh","/opt/payara/k8s/ready.sh"]}`.
    exec probe handler. Set to null when overriding the probe with httpGet/tcpSocket (Helm merges maps; a probe allows only one handler).

`hopsworks.probs.admin.startupProbe` <a class="headerlink" href="#helm.hopsworks.probs.admin.startupProbe" title="Permanent link">#</a> { #helm.hopsworks.probs.admin.startupProbe }
:   Type `object`.
    startup probe. Gives the DAS up to 30 minutes (180 x 10s) to boot before liveness starts counting. Generous on purpose: container start includes artifact downloads, and a kill mid-download starts them over. Set to null to disable. If you override with httpGet/tcpSocket, also set `exec: null`.

    ??? note "Default"

        ```yaml
        exec:
          command:
          - /bin/sh
          - /opt/payara/k8s/ready.sh
        failureThreshold: 180
        periodSeconds: 10
        timeoutSeconds: 30
        ```

`hopsworks.probs.admin.startupProbe.exec` <a class="headerlink" href="#helm.hopsworks.probs.admin.startupProbe.exec" title="Permanent link">#</a> { #helm.hopsworks.probs.admin.startupProbe.exec }
:   Type `object`, default `{"command":["/bin/sh","/opt/payara/k8s/ready.sh"]}`.
    exec probe handler. Set to null when overriding the probe with httpGet/tcpSocket (Helm merges maps; a probe allows only one handler).

`hopsworks.probs.worker.livenessProbe.failureThreshold` <a class="headerlink" href="#helm.hopsworks.probs.worker.livenessProbe.failureThreshold" title="Permanent link">#</a> { #helm.hopsworks.probs.worker.livenessProbe.failureThreshold }
:   Type `int`, default `3`.

`hopsworks.probs.worker.livenessProbe.httpGet.path` <a class="headerlink" href="#helm.hopsworks.probs.worker.livenessProbe.httpGet.path" title="Permanent link">#</a> { #helm.hopsworks.probs.worker.livenessProbe.httpGet.path }
:   Type `string`, default `"/hopsworks-api/api/variables/versions"`.

`hopsworks.probs.worker.livenessProbe.httpGet.port` <a class="headerlink" href="#helm.hopsworks.probs.worker.livenessProbe.httpGet.port" title="Permanent link">#</a> { #helm.hopsworks.probs.worker.livenessProbe.httpGet.port }
:   Type `int`, default `8182`.

`hopsworks.probs.worker.livenessProbe.httpGet.scheme` <a class="headerlink" href="#helm.hopsworks.probs.worker.livenessProbe.httpGet.scheme" title="Permanent link">#</a> { #helm.hopsworks.probs.worker.livenessProbe.httpGet.scheme }
:   Type `string`, default `"HTTPS"`.

`hopsworks.probs.worker.livenessProbe.initialDelaySeconds` <a class="headerlink" href="#helm.hopsworks.probs.worker.livenessProbe.initialDelaySeconds" title="Permanent link">#</a> { #helm.hopsworks.probs.worker.livenessProbe.initialDelaySeconds }
:   Type `int`, default `150`.

`hopsworks.probs.worker.livenessProbe.periodSeconds` <a class="headerlink" href="#helm.hopsworks.probs.worker.livenessProbe.periodSeconds" title="Permanent link">#</a> { #helm.hopsworks.probs.worker.livenessProbe.periodSeconds }
:   Type `int`, default `20`.

`hopsworks.probs.worker.livenessProbe.timeoutSeconds` <a class="headerlink" href="#helm.hopsworks.probs.worker.livenessProbe.timeoutSeconds" title="Permanent link">#</a> { #helm.hopsworks.probs.worker.livenessProbe.timeoutSeconds }
:   Type `int`, default `20`.

`hopsworks.probs.worker.readinessProbe.httpGet.path` <a class="headerlink" href="#helm.hopsworks.probs.worker.readinessProbe.httpGet.path" title="Permanent link">#</a> { #helm.hopsworks.probs.worker.readinessProbe.httpGet.path }
:   Type `string`, default `"/hopsworks-api/api/variables/versions"`.

`hopsworks.probs.worker.readinessProbe.httpGet.port` <a class="headerlink" href="#helm.hopsworks.probs.worker.readinessProbe.httpGet.port" title="Permanent link">#</a> { #helm.hopsworks.probs.worker.readinessProbe.httpGet.port }
:   Type `int`, default `8182`.

`hopsworks.probs.worker.readinessProbe.httpGet.scheme` <a class="headerlink" href="#helm.hopsworks.probs.worker.readinessProbe.httpGet.scheme" title="Permanent link">#</a> { #helm.hopsworks.probs.worker.readinessProbe.httpGet.scheme }
:   Type `string`, default `"HTTPS"`.

`hopsworks.probs.worker.readinessProbe.initialDelaySeconds` <a class="headerlink" href="#helm.hopsworks.probs.worker.readinessProbe.initialDelaySeconds" title="Permanent link">#</a> { #helm.hopsworks.probs.worker.readinessProbe.initialDelaySeconds }
:   Type `int`, default `150`.

`hopsworks.probs.worker.readinessProbe.periodSeconds` <a class="headerlink" href="#helm.hopsworks.probs.worker.readinessProbe.periodSeconds" title="Permanent link">#</a> { #helm.hopsworks.probs.worker.readinessProbe.periodSeconds }
:   Type `int`, default `10`.

`hopsworks.probs.worker.startupProbe.failureThreshold` <a class="headerlink" href="#helm.hopsworks.probs.worker.startupProbe.failureThreshold" title="Permanent link">#</a> { #helm.hopsworks.probs.worker.startupProbe.failureThreshold }
:   Type `int`, default `10`.

`hopsworks.probs.worker.startupProbe.httpGet.path` <a class="headerlink" href="#helm.hopsworks.probs.worker.startupProbe.httpGet.path" title="Permanent link">#</a> { #helm.hopsworks.probs.worker.startupProbe.httpGet.path }
:   Type `string`, default `"/health"`.

`hopsworks.probs.worker.startupProbe.httpGet.port` <a class="headerlink" href="#helm.hopsworks.probs.worker.startupProbe.httpGet.port" title="Permanent link">#</a> { #helm.hopsworks.probs.worker.startupProbe.httpGet.port }
:   Type `int`, default `8182`.

`hopsworks.probs.worker.startupProbe.httpGet.scheme` <a class="headerlink" href="#helm.hopsworks.probs.worker.startupProbe.httpGet.scheme" title="Permanent link">#</a> { #helm.hopsworks.probs.worker.startupProbe.httpGet.scheme }
:   Type `string`, default `"HTTPS"`.

`hopsworks.probs.worker.startupProbe.initialDelaySeconds` <a class="headerlink" href="#helm.hopsworks.probs.worker.startupProbe.initialDelaySeconds" title="Permanent link">#</a> { #helm.hopsworks.probs.worker.startupProbe.initialDelaySeconds }
:   Type `int`, default `150`.

`hopsworks.probs.worker.startupProbe.periodSeconds` <a class="headerlink" href="#helm.hopsworks.probs.worker.startupProbe.periodSeconds" title="Permanent link">#</a> { #helm.hopsworks.probs.worker.startupProbe.periodSeconds }
:   Type `int`, default `10`.

</div>

## rbac { #helm-values-hopsworks-rbac }

??? example "Defaults as YAML"

    ```yaml
    hopsworks:
      rbac:
        annotations: {}
        create: true
        extraRoleRules:
        - apiGroups:
          - discovery.k8s.io
          resources:
          - endpointslices
          verbs:
          - get
          - list
        - apiGroups:
          - sparkoperator.k8s.io
          resources:
          - sparkapplications
          verbs:
          - '*'
        - apiGroups:
          - ray.io
          resources:
          - rayjobs
          - rayclusters
          verbs:
          - '*'
        - apiGroups:
          - serving.knative.dev
          resources:
          - services
          verbs:
          - '*'
        - apiGroups:
          - serving.kserve.io
          resources:
          - inferenceservices
          - clusterservingruntimes
          verbs:
          - '*'
        - apiGroups:
          - scheduling.k8s.io
          resources:
          - priorityclasses
          verbs:
          - get
          - list
        - apiGroups:
          - metrics.k8s.io
          resources:
          - nodes
          - pods
          verbs:
          - get
          - list
        - apiGroups:
          - ''
          resources:
          - resourcequotas
          verbs:
          - get
          - list
        useExistingRole: false
    ```

<div class="hops-values" markdown>

`hopsworks.rbac.annotations` <a class="headerlink" href="#helm.hopsworks.rbac.annotations" title="Permanent link">#</a> { #helm.hopsworks.rbac.annotations }
:   Type `object`, default `{}`.
    annotations

`hopsworks.rbac.create` <a class="headerlink" href="#helm.hopsworks.rbac.create" title="Permanent link">#</a> { #helm.hopsworks.rbac.create }
:   Type `bool`, default `true`.

`hopsworks.rbac.extraRoleRules[0].apiGroups[0]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.0.apiGroups.0" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.0.apiGroups.0 }
:   Type `string`, default `"discovery.k8s.io"`.

`hopsworks.rbac.extraRoleRules[0].resources[0]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.0.resources.0" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.0.resources.0 }
:   Type `string`, default `"endpointslices"`.

`hopsworks.rbac.extraRoleRules[0].verbs[0]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.0.verbs.0" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.0.verbs.0 }
:   Type `string`, default `"get"`.

`hopsworks.rbac.extraRoleRules[0].verbs[1]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.0.verbs.1" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.0.verbs.1 }
:   Type `string`, default `"list"`.

`hopsworks.rbac.extraRoleRules[1].apiGroups[0]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.1.apiGroups.0" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.1.apiGroups.0 }
:   Type `string`, default `"sparkoperator.k8s.io"`.

`hopsworks.rbac.extraRoleRules[1].resources[0]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.1.resources.0" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.1.resources.0 }
:   Type `string`, default `"sparkapplications"`.

`hopsworks.rbac.extraRoleRules[1].verbs[0]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.1.verbs.0" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.1.verbs.0 }
:   Type `string`, default `"*"`.

`hopsworks.rbac.extraRoleRules[2].apiGroups[0]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.2.apiGroups.0" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.2.apiGroups.0 }
:   Type `string`, default `"ray.io"`.

`hopsworks.rbac.extraRoleRules[2].resources[0]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.2.resources.0" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.2.resources.0 }
:   Type `string`, default `"rayjobs"`.

`hopsworks.rbac.extraRoleRules[2].resources[1]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.2.resources.1" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.2.resources.1 }
:   Type `string`, default `"rayclusters"`.

`hopsworks.rbac.extraRoleRules[2].verbs[0]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.2.verbs.0" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.2.verbs.0 }
:   Type `string`, default `"*"`.

`hopsworks.rbac.extraRoleRules[3].apiGroups[0]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.3.apiGroups.0" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.3.apiGroups.0 }
:   Type `string`, default `"serving.knative.dev"`.

`hopsworks.rbac.extraRoleRules[3].resources[0]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.3.resources.0" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.3.resources.0 }
:   Type `string`, default `"services"`.

`hopsworks.rbac.extraRoleRules[3].verbs[0]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.3.verbs.0" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.3.verbs.0 }
:   Type `string`, default `"*"`.

`hopsworks.rbac.extraRoleRules[4].apiGroups[0]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.4.apiGroups.0" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.4.apiGroups.0 }
:   Type `string`, default `"serving.kserve.io"`.

`hopsworks.rbac.extraRoleRules[4].resources[0]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.4.resources.0" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.4.resources.0 }
:   Type `string`, default `"inferenceservices"`.

`hopsworks.rbac.extraRoleRules[4].resources[1]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.4.resources.1" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.4.resources.1 }
:   Type `string`, default `"clusterservingruntimes"`.

`hopsworks.rbac.extraRoleRules[4].verbs[0]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.4.verbs.0" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.4.verbs.0 }
:   Type `string`, default `"*"`.

`hopsworks.rbac.extraRoleRules[5].apiGroups[0]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.5.apiGroups.0" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.5.apiGroups.0 }
:   Type `string`, default `"scheduling.k8s.io"`.

`hopsworks.rbac.extraRoleRules[5].resources[0]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.5.resources.0" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.5.resources.0 }
:   Type `string`, default `"priorityclasses"`.

`hopsworks.rbac.extraRoleRules[5].verbs[0]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.5.verbs.0" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.5.verbs.0 }
:   Type `string`, default `"get"`.

`hopsworks.rbac.extraRoleRules[5].verbs[1]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.5.verbs.1" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.5.verbs.1 }
:   Type `string`, default `"list"`.

`hopsworks.rbac.extraRoleRules[6].apiGroups[0]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.6.apiGroups.0" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.6.apiGroups.0 }
:   Type `string`, default `"metrics.k8s.io"`.

`hopsworks.rbac.extraRoleRules[6].resources[0]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.6.resources.0" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.6.resources.0 }
:   Type `string`, default `"nodes"`.

`hopsworks.rbac.extraRoleRules[6].resources[1]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.6.resources.1" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.6.resources.1 }
:   Type `string`, default `"pods"`.

`hopsworks.rbac.extraRoleRules[6].verbs[0]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.6.verbs.0" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.6.verbs.0 }
:   Type `string`, default `"get"`.

`hopsworks.rbac.extraRoleRules[6].verbs[1]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.6.verbs.1" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.6.verbs.1 }
:   Type `string`, default `"list"`.

`hopsworks.rbac.extraRoleRules[7].apiGroups[0]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.7.apiGroups.0" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.7.apiGroups.0 }
:   Type `string`, default `""`.

`hopsworks.rbac.extraRoleRules[7].resources[0]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.7.resources.0" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.7.resources.0 }
:   Type `string`, default `"resourcequotas"`.

`hopsworks.rbac.extraRoleRules[7].verbs[0]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.7.verbs.0" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.7.verbs.0 }
:   Type `string`, default `"get"`.

`hopsworks.rbac.extraRoleRules[7].verbs[1]` <a class="headerlink" href="#helm.hopsworks.rbac.extraRoleRules.7.verbs.1" title="Permanent link">#</a> { #helm.hopsworks.rbac.extraRoleRules.7.verbs.1 }
:   Type `string`, default `"list"`.

`hopsworks.rbac.useExistingRole` <a class="headerlink" href="#helm.hopsworks.rbac.useExistingRole" title="Permanent link">#</a> { #helm.hopsworks.rbac.useExistingRole }
:   Type `bool`, default `false`.

</div>

## resources { #helm-values-hopsworks-resources }

??? example "Defaults as YAML"

    ```yaml
    hopsworks:
      resources:
        admin:
          auto_jvm: true
          container:
            limits:
              cpu: 2000m
              memory: 2048Mi
            requests:
              cpu: 1000m
              memory: 2048Mi
          extraJavaToolOptions: ''
          jvm:
            garbageCollector: ''
            memory:
              buffer: 2048
              compressedClassSpaceSize: 512
              heap: 4096
              metaspace: 2048
              nonMethodCodeHeapSize: 5
              nonProfiledCodeHeapSize: 48
              profiledCodeHeapSize: 48
        adminSidecar:
          requests:
            cpu: 200m
            memory: 256Mi
        worker:
          auto_jvm: true
          container:
            limits:
              cpu: 4000m
              memory: 8Gi
            requests:
              cpu: 2000m
              memory: 2048Mi
          extraJavaToolOptions: ''
          jvm:
            garbageCollector: ''
            memory:
              buffer: 3072
              compressedClassSpaceSize: 512
              heap: 4096
              metaspace: 2048
              nonMethodCodeHeapSize: 5
              nonProfiledCodeHeapSize: 48
              profiledCodeHeapSize: 48
    ```

<div class="hops-values" markdown>

`hopsworks.resources.admin.auto_jvm` <a class="headerlink" href="#helm.hopsworks.resources.admin.auto_jvm" title="Permanent link">#</a> { #helm.hopsworks.resources.admin.auto_jvm }
:   Type `bool`, default `true`.

`hopsworks.resources.admin.container.limits.cpu` <a class="headerlink" href="#helm.hopsworks.resources.admin.container.limits.cpu" title="Permanent link">#</a> { #helm.hopsworks.resources.admin.container.limits.cpu }
:   Type `string`, default `"2000m"`.

`hopsworks.resources.admin.container.limits.memory` <a class="headerlink" href="#helm.hopsworks.resources.admin.container.limits.memory" title="Permanent link">#</a> { #helm.hopsworks.resources.admin.container.limits.memory }
:   Type `string`, default `"2048Mi"`.

`hopsworks.resources.admin.container.requests.cpu` <a class="headerlink" href="#helm.hopsworks.resources.admin.container.requests.cpu" title="Permanent link">#</a> { #helm.hopsworks.resources.admin.container.requests.cpu }
:   Type `string`, default `"1000m"`.

`hopsworks.resources.admin.container.requests.memory` <a class="headerlink" href="#helm.hopsworks.resources.admin.container.requests.memory" title="Permanent link">#</a> { #helm.hopsworks.resources.admin.container.requests.memory }
:   Type `string`, default `"2048Mi"`.

`hopsworks.resources.admin.extraJavaToolOptions` <a class="headerlink" href="#helm.hopsworks.resources.admin.extraJavaToolOptions" title="Permanent link">#</a> { #helm.hopsworks.resources.admin.extraJavaToolOptions }
:   Type `string`, default `""`.

`hopsworks.resources.admin.jvm.garbageCollector` <a class="headerlink" href="#helm.hopsworks.resources.admin.jvm.garbageCollector" title="Permanent link">#</a> { #helm.hopsworks.resources.admin.jvm.garbageCollector }
:   Type `string`, default `""`.

`hopsworks.resources.admin.jvm.memory.buffer` <a class="headerlink" href="#helm.hopsworks.resources.admin.jvm.memory.buffer" title="Permanent link">#</a> { #helm.hopsworks.resources.admin.jvm.memory.buffer }
:   Type `int`, default `2048`.

`hopsworks.resources.admin.jvm.memory.compressedClassSpaceSize` <a class="headerlink" href="#helm.hopsworks.resources.admin.jvm.memory.compressedClassSpaceSize" title="Permanent link">#</a> { #helm.hopsworks.resources.admin.jvm.memory.compressedClassSpaceSize }
:   Type `int`, default `512`.

`hopsworks.resources.admin.jvm.memory.heap` <a class="headerlink" href="#helm.hopsworks.resources.admin.jvm.memory.heap" title="Permanent link">#</a> { #helm.hopsworks.resources.admin.jvm.memory.heap }
:   Type `int`, default `4096`.

`hopsworks.resources.admin.jvm.memory.metaspace` <a class="headerlink" href="#helm.hopsworks.resources.admin.jvm.memory.metaspace" title="Permanent link">#</a> { #helm.hopsworks.resources.admin.jvm.memory.metaspace }
:   Type `int`, default `2048`.

`hopsworks.resources.admin.jvm.memory.nonMethodCodeHeapSize` <a class="headerlink" href="#helm.hopsworks.resources.admin.jvm.memory.nonMethodCodeHeapSize" title="Permanent link">#</a> { #helm.hopsworks.resources.admin.jvm.memory.nonMethodCodeHeapSize }
:   Type `int`, default `5`.

`hopsworks.resources.admin.jvm.memory.nonProfiledCodeHeapSize` <a class="headerlink" href="#helm.hopsworks.resources.admin.jvm.memory.nonProfiledCodeHeapSize" title="Permanent link">#</a> { #helm.hopsworks.resources.admin.jvm.memory.nonProfiledCodeHeapSize }
:   Type `int`, default `48`.

`hopsworks.resources.admin.jvm.memory.profiledCodeHeapSize` <a class="headerlink" href="#helm.hopsworks.resources.admin.jvm.memory.profiledCodeHeapSize" title="Permanent link">#</a> { #helm.hopsworks.resources.admin.jvm.memory.profiledCodeHeapSize }
:   Type `int`, default `48`.

`hopsworks.resources.adminSidecar` <a class="headerlink" href="#helm.hopsworks.resources.adminSidecar" title="Permanent link">#</a> { #helm.hopsworks.resources.adminSidecar }
:   Type `object`, default `{"requests":{"cpu":"200m","memory":"256Mi"}}`.
    Admin side car resources

`hopsworks.resources.worker.auto_jvm` <a class="headerlink" href="#helm.hopsworks.resources.worker.auto_jvm" title="Permanent link">#</a> { #helm.hopsworks.resources.worker.auto_jvm }
:   Type `bool`, default `true`.

`hopsworks.resources.worker.container.limits.cpu` <a class="headerlink" href="#helm.hopsworks.resources.worker.container.limits.cpu" title="Permanent link">#</a> { #helm.hopsworks.resources.worker.container.limits.cpu }
:   Type `string`, default `"4000m"`.

`hopsworks.resources.worker.container.limits.memory` <a class="headerlink" href="#helm.hopsworks.resources.worker.container.limits.memory" title="Permanent link">#</a> { #helm.hopsworks.resources.worker.container.limits.memory }
:   Type `string`, default `"8Gi"`.

`hopsworks.resources.worker.container.requests.cpu` <a class="headerlink" href="#helm.hopsworks.resources.worker.container.requests.cpu" title="Permanent link">#</a> { #helm.hopsworks.resources.worker.container.requests.cpu }
:   Type `string`, default `"2000m"`.

`hopsworks.resources.worker.container.requests.memory` <a class="headerlink" href="#helm.hopsworks.resources.worker.container.requests.memory" title="Permanent link">#</a> { #helm.hopsworks.resources.worker.container.requests.memory }
:   Type `string`, default `"2048Mi"`.

`hopsworks.resources.worker.extraJavaToolOptions` <a class="headerlink" href="#helm.hopsworks.resources.worker.extraJavaToolOptions" title="Permanent link">#</a> { #helm.hopsworks.resources.worker.extraJavaToolOptions }
:   Type `string`, default `""`.

`hopsworks.resources.worker.jvm.garbageCollector` <a class="headerlink" href="#helm.hopsworks.resources.worker.jvm.garbageCollector" title="Permanent link">#</a> { #helm.hopsworks.resources.worker.jvm.garbageCollector }
:   Type `string`, default `""`.

`hopsworks.resources.worker.jvm.memory.buffer` <a class="headerlink" href="#helm.hopsworks.resources.worker.jvm.memory.buffer" title="Permanent link">#</a> { #helm.hopsworks.resources.worker.jvm.memory.buffer }
:   Type `int`, default `3072`.

`hopsworks.resources.worker.jvm.memory.compressedClassSpaceSize` <a class="headerlink" href="#helm.hopsworks.resources.worker.jvm.memory.compressedClassSpaceSize" title="Permanent link">#</a> { #helm.hopsworks.resources.worker.jvm.memory.compressedClassSpaceSize }
:   Type `int`, default `512`.

`hopsworks.resources.worker.jvm.memory.heap` <a class="headerlink" href="#helm.hopsworks.resources.worker.jvm.memory.heap" title="Permanent link">#</a> { #helm.hopsworks.resources.worker.jvm.memory.heap }
:   Type `int`, default `4096`.

`hopsworks.resources.worker.jvm.memory.metaspace` <a class="headerlink" href="#helm.hopsworks.resources.worker.jvm.memory.metaspace" title="Permanent link">#</a> { #helm.hopsworks.resources.worker.jvm.memory.metaspace }
:   Type `int`, default `2048`.

`hopsworks.resources.worker.jvm.memory.nonMethodCodeHeapSize` <a class="headerlink" href="#helm.hopsworks.resources.worker.jvm.memory.nonMethodCodeHeapSize" title="Permanent link">#</a> { #helm.hopsworks.resources.worker.jvm.memory.nonMethodCodeHeapSize }
:   Type `int`, default `5`.

`hopsworks.resources.worker.jvm.memory.nonProfiledCodeHeapSize` <a class="headerlink" href="#helm.hopsworks.resources.worker.jvm.memory.nonProfiledCodeHeapSize" title="Permanent link">#</a> { #helm.hopsworks.resources.worker.jvm.memory.nonProfiledCodeHeapSize }
:   Type `int`, default `48`.

`hopsworks.resources.worker.jvm.memory.profiledCodeHeapSize` <a class="headerlink" href="#helm.hopsworks.resources.worker.jvm.memory.profiledCodeHeapSize" title="Permanent link">#</a> { #helm.hopsworks.resources.worker.jvm.memory.profiledCodeHeapSize }
:   Type `int`, default `48`.

</div>

## service { #helm-values-hopsworks-service }

??? example "Defaults as YAML"

    ```yaml
    hopsworks:
      service:
        admin:
          annotations:
            consul.hashicorp.com/service-name: glassfish
            consul.hashicorp.com/service-tags: admin
          name: admin
          port: 4848
          type: ClusterIP
        worker:
          external:
            http:
              port: 28080
              type: ClusterIP
            https:
              nodePort: null
              port: 28181
              type: ClusterIP
          internal:
            annotations:
              consul.hashicorp.com/service-name: glassfish
              consul.hashicorp.com/service-tags: hopsworks
              prometheus.io/path: /metrics
              prometheus.io/port: 8182
              prometheus.io/scheme: https
              prometheus.io/scrape: 'true'
            port: 8182
            type: ClusterIP
    ```

<div class="hops-values" markdown>

`hopsworks.service.admin.annotations."consul.hashicorp.com/service-name"` <a class="headerlink" href="#helm.hopsworks.service.admin.annotations.consul.hashicorp.com-service-name" title="Permanent link">#</a> { #helm.hopsworks.service.admin.annotations.consul.hashicorp.com-service-name }
:   Type `string`, default `"glassfish"`.

`hopsworks.service.admin.annotations."consul.hashicorp.com/service-tags"` <a class="headerlink" href="#helm.hopsworks.service.admin.annotations.consul.hashicorp.com-service-tags" title="Permanent link">#</a> { #helm.hopsworks.service.admin.annotations.consul.hashicorp.com-service-tags }
:   Type `string`, default `"admin"`.

`hopsworks.service.admin.name` <a class="headerlink" href="#helm.hopsworks.service.admin.name" title="Permanent link">#</a> { #helm.hopsworks.service.admin.name }
:   Type `string`, default `"admin"`.

`hopsworks.service.admin.port` <a class="headerlink" href="#helm.hopsworks.service.admin.port" title="Permanent link">#</a> { #helm.hopsworks.service.admin.port }
:   Type `int`, default `4848`.

`hopsworks.service.admin.type` <a class="headerlink" href="#helm.hopsworks.service.admin.type" title="Permanent link">#</a> { #helm.hopsworks.service.admin.type }
:   Type `string`, default `"ClusterIP"`.

`hopsworks.service.worker.external.http.port` <a class="headerlink" href="#helm.hopsworks.service.worker.external.http.port" title="Permanent link">#</a> { #helm.hopsworks.service.worker.external.http.port }
:   Type `int`, default `28080`.

`hopsworks.service.worker.external.http.type` <a class="headerlink" href="#helm.hopsworks.service.worker.external.http.type" title="Permanent link">#</a> { #helm.hopsworks.service.worker.external.http.type }
:   Type `string`, default `"ClusterIP"`.

`hopsworks.service.worker.external.https.nodePort` <a class="headerlink" href="#helm.hopsworks.service.worker.external.https.nodePort" title="Permanent link">#</a> { #helm.hopsworks.service.worker.external.https.nodePort }
:   Type `string`, default `nil`.
    Explicit nodePort for the https service when type is NodePort. Null lets Kubernetes allocate one from the cluster's node-port range; a set value must lie in that range (30000-32767 by default), which the API server enforces at install.

`hopsworks.service.worker.external.https.port` <a class="headerlink" href="#helm.hopsworks.service.worker.external.https.port" title="Permanent link">#</a> { #helm.hopsworks.service.worker.external.https.port }
:   Type `int`, default `28181`.

`hopsworks.service.worker.external.https.type` <a class="headerlink" href="#helm.hopsworks.service.worker.external.https.type" title="Permanent link">#</a> { #helm.hopsworks.service.worker.external.https.type }
:   Type `string`, default `"ClusterIP"`.

`hopsworks.service.worker.internal.annotations."consul.hashicorp.com/service-name"` <a class="headerlink" href="#helm.hopsworks.service.worker.internal.annotations.consul.hashicorp.com-service-name" title="Permanent link">#</a> { #helm.hopsworks.service.worker.internal.annotations.consul.hashicorp.com-service-name }
:   Type `string`, default `"glassfish"`.

`hopsworks.service.worker.internal.annotations."consul.hashicorp.com/service-tags"` <a class="headerlink" href="#helm.hopsworks.service.worker.internal.annotations.consul.hashicorp.com-service-tags" title="Permanent link">#</a> { #helm.hopsworks.service.worker.internal.annotations.consul.hashicorp.com-service-tags }
:   Type `string`, default `"hopsworks"`.

`hopsworks.service.worker.internal.annotations."prometheus.io/path"` <a class="headerlink" href="#helm.hopsworks.service.worker.internal.annotations.prometheus.io-path" title="Permanent link">#</a> { #helm.hopsworks.service.worker.internal.annotations.prometheus.io-path }
:   Type `string`, default `"/metrics"`.

`hopsworks.service.worker.internal.annotations."prometheus.io/port"` <a class="headerlink" href="#helm.hopsworks.service.worker.internal.annotations.prometheus.io-port" title="Permanent link">#</a> { #helm.hopsworks.service.worker.internal.annotations.prometheus.io-port }
:   Type `int`, default `8182`.

`hopsworks.service.worker.internal.annotations."prometheus.io/scheme"` <a class="headerlink" href="#helm.hopsworks.service.worker.internal.annotations.prometheus.io-scheme" title="Permanent link">#</a> { #helm.hopsworks.service.worker.internal.annotations.prometheus.io-scheme }
:   Type `string`, default `"https"`.

`hopsworks.service.worker.internal.annotations."prometheus.io/scrape"` <a class="headerlink" href="#helm.hopsworks.service.worker.internal.annotations.prometheus.io-scrape" title="Permanent link">#</a> { #helm.hopsworks.service.worker.internal.annotations.prometheus.io-scrape }
:   Type `string`, default `"true"`.

`hopsworks.service.worker.internal.port` <a class="headerlink" href="#helm.hopsworks.service.worker.internal.port" title="Permanent link">#</a> { #helm.hopsworks.service.worker.internal.port }
:   Type `int`, default `8182`.

`hopsworks.service.worker.internal.type` <a class="headerlink" href="#helm.hopsworks.service.worker.internal.type" title="Permanent link">#</a> { #helm.hopsworks.service.worker.internal.type }
:   Type `string`, default `"ClusterIP"`.

</div>

## terminal { #helm-values-hopsworks-terminal }

??? example "Defaults as YAML"

    ```yaml
    hopsworks:
      terminal:
        enabled: false
        oomGuard: true
        proxyPodAppLabels: hopsworks-instance,hopsworks-admin
        proxyTokenTtlMs: '60000'
        teleportCleanerIntervalMs: '86400000'
        teleportTtlDays: 7
    ```

<div class="hops-values" markdown>

`hopsworks.terminal.enabled` <a class="headerlink" href="#helm.hopsworks.terminal.enabled" title="Permanent link">#</a> { #helm.hopsworks.terminal.enabled }
:   Type `bool`, default `false`.

`hopsworks.terminal.oomGuard` <a class="headerlink" href="#helm.hopsworks.terminal.oomGuard" title="Permanent link">#</a> { #helm.hopsworks.terminal.oomGuard }
:   Type `bool`, default `true`.
    In-image memory guard: kills the hungriest process in a terminal pod before the kernel group-OOM-kills the whole session (cgroup v2 only). False sets HOPS_OOM_GUARD_DISABLE=1 on new terminal pods.

`hopsworks.terminal.proxyPodAppLabels` <a class="headerlink" href="#helm.hopsworks.terminal.proxyPodAppLabels" title="Permanent link">#</a> { #helm.hopsworks.terminal.proxyPodAppLabels }
:   Type `string`, default `"hopsworks-instance,hopsworks-admin"`.
    Comma-separated `app` label values of the Payara pods allowed to reach a terminal pod's WebSocket port (the per-namespace terminal-isolation NetworkPolicy). Must match the chart's pod labels or every terminal is unreachable.

`hopsworks.terminal.proxyTokenTtlMs` <a class="headerlink" href="#helm.hopsworks.terminal.proxyTokenTtlMs" title="Permanent link">#</a> { #helm.hopsworks.terminal.proxyTokenTtlMs }
:   Type `string`, default `"60000"`.
    Milliseconds a CLI terminal-attach proxy token stays valid before its single WebSocket handshake.

`hopsworks.terminal.teleportCleanerIntervalMs` <a class="headerlink" href="#helm.hopsworks.terminal.teleportCleanerIntervalMs" title="Permanent link">#</a> { #helm.hopsworks.terminal.teleportCleanerIntervalMs }
:   Type `string`, default `"86400000"`.
    Milliseconds between teleport reaper sweeps (applied at Payara start). Quoted like the other *_ms settings: a bare integer this large renders as 8.64e+07 in the DML.

`hopsworks.terminal.teleportTtlDays` <a class="headerlink" href="#helm.hopsworks.terminal.teleportTtlDays" title="Permanent link">#</a> { #helm.hopsworks.terminal.teleportTtlDays }
:   Type `int`, default `7`.
    Days a staged hops-session teleport file (transcript, manifest, baton) survives in a user's HopsFS home before the reaper deletes it; 0 or less disables the reaper.

</div>

## variables { #helm-values-hopsworks-variables }

??? example "Defaults as YAML"

    ```yaml
    hopsworks:
      variables:
        admin_email: admin@hopsworks.ai
        admin_password: admin
        agent_deployment_otel_cpu: '0.5'
        agent_deployment_otel_enabled: 'true'
        agent_deployment_otel_image: otlp-sidecar
        agent_deployment_otel_memory_mb: '1024'
        agent_jobs_enabled: 'true'
        airflow_dir: /srv/hops/airflow
        airflow_enabled: true
        airflow_user: airflow
        airflow_user_email: airflow@hopsworks.ai
        alert_email_addrs: ''
        anaconda_dir: /
        anaconda_enabled: 'true'
        anaconda_env: ''
        anaconda_user: anaconda
        application_certificate_validity_period: 3650d
        apply_hopsfsmount_apparmor_profile_kube: 'false'
        async_services_timer_batch_size: '1000'
        async_services_timer_delete_history_after_days: '7'
        async_services_timer_enabled: 'true'
        async_services_timer_interval_ms: '15000'
        audit_log_count: '10'
        audit_log_file_format: server_audit_log%g.log
        audit_log_file_path: /audit-logs
        audit_log_file_type: io.hops.hopsworks.audit.helper.JSONLogFormatter
        audit_log_size_limit: '256000000'
        base_buildkit_image: docker.hops.works/hopsworks/moby/buildkit:v0.32.2-rootless
        base_image_name: hopsworks-base
        base_image_version: 5.2.0-SNAPSHOT
        cert_mater_delay: 3m
        certs_dir: /srv/hops/certs-dir
        check_nodemanagers_status: ''
        client_path: /srv/hops/clients-3.4.3
        cloud: ''
        command_agent_home_batch: '20'
        command_agent_home_claim_lease_as_ms: '600000'
        command_agent_home_migration_period_as_ms: '3600000'
        command_agent_home_process_timer_period_as_ms: '5000'
        command_agent_home_retry_backoff_base_as_ms: '10000'
        command_agent_home_retry_backoff_max_as_ms: '600000'
        command_search_fs_history_clean_period_as_ms: '3600000'
        command_search_fs_history_enable: 'false'
        command_search_fs_history_window_as_s: '3600'
        command_search_fs_process_timer_period_as_ms: '1000'
        command_search_fs_reindex_queue_wait_as_ms: '1800000'
        command_search_fs_retry_per_clean_interval: '5'
        conda_default_repo: defaults
        default_jupyter_environment: pandas-training-pipeline
        default_python_job_environment: pandas-training-pipeline
        disable_password_login: 'false'
        disable_registration: 'false'
        dlt_schema_fetch_job_deadline_seconds: '1800'
        docker_base_image_python_version: '3.13'
        docker_cgroup_cpu_period: '100000'
        docker_cgroup_enabled: 'false'
        docker_cgroup_parent: docker.slice
        docker_job_mounts_allowed: 'false'
        docker_job_mounts_list: ''
        docker_job_uid_strict: 'true'
        docker_mounts: /srv/hops/hadoop/etc/hadoop,/srv/hops/spark,/srv/hops/flink,/srv/hops/apache-livy
        docker_operations_allow_hermetic_custom_commands: 'false'
        docker_operations_backoff_limit: '0'
        docker_operations_build_metadata: 'true'
        docker_operations_buildkit_addr: ''
        docker_operations_buildkit_backoff_limit: '0'
        docker_operations_buildkit_cache_scope: shared
        docker_operations_buildkit_extra_args: ''
        docker_operations_buildkit_limit_cpu: '2'
        docker_operations_buildkit_limit_memory: 4G
        docker_operations_buildkit_priority_class: ''
        docker_operations_buildkit_replicas: '1'
        docker_operations_buildkit_request_cpu: 200m
        docker_operations_buildkit_request_memory: 500Mi
        docker_operations_buildkit_storage: 70Gi
        docker_operations_buildkit_tls_locality: buildkitd
        docker_operations_buildkit_tls_secret: ''
        docker_operations_cert_name: kagent_certificate_bundle.pem
        docker_operations_context_orphan_minutes: '120'
        docker_operations_default_service_account: default
        docker_operations_delete_jobs_add_description_if_fails: false
        docker_operations_delete_jobs_on_completion: 'true'
        docker_operations_docker_context_builder: AUTO
        docker_operations_docker_context_builder_s3_bucket: ${env:S3_BUCKET}
        docker_operations_docker_context_builder_s3_endpoint: ${env:S3_ENDPOINT}
        docker_operations_docker_context_builder_s3_region: ${env:S3_REGION}
        docker_operations_hopsworks_ca_secret_name: docker-registry-crypto-material
        docker_operations_image_pull_secrets: ''
        docker_operations_lock_dependencies: 'false'
        docker_operations_managed_docker_secrets: ''
        docker_operations_multi_region_copy: 'false'
        docker_operations_oci_worker_snapshotter: auto
        docker_operations_push_insecure: 'false'
        docker_operations_registry_container: docker
        docker_operations_registry_http: 'false'
        docker_operations_registry_pod: docker-registry-0
        docker_operations_suspend_jobs: 'false'
        docker_operations_timeout_check_minutes: '15'
        docker_operations_timeout_delete_minutes: '5'
        docker_operations_timeout_export_minutes: '15'
        docker_operations_timeout_listing_minutes: '15'
        docker_operations_timeout_minutes_buildkit: '120'
        docker_operations_timeout_tag_minutes: '5'
        download_allowed: 'true'
        elastic_dir: /srv/hops/elastic
        elastic_https_enabled: 'true'
        elastic_jwt_enabled: 'true'
        elastic_jwt_exp_ms: '1800000'
        elastic_jwt_url_parameter: jt
        elastic_logs_index_expiration: '604800000'
        elastic_opendistro_security_enabled: 'true'
        elastic_user: elastic
        elastic_version: 3.8.0
        enable_adls_storage_connectors: 'false'
        enable_bigquery_storage_connectors: 'true'
        enable_bring_your_own_kafka: 'false'
        enable_elasticsearch_storage_connectors: 'true'
        enable_feature_monitoring: 'true'
        enable_fix_receivers_timer: 'true'
        enable_gcs_storage_connectors: 'true'
        enable_jupyter_python_kernel_non_kubernetes: 'false'
        enable_kafka_storage_connectors: 'true'
        enable_metadata_designer: ''
        enable_opensearch_storage_connectors: 'true'
        enable_read_only_git_repositories: 'false'
        enable_redshift_storage_connectors: 'true'
        enable_snowflake_storage_connectors: 'true'
        enable_user_search: 'true'
        epipe_version: 0.20.0
        executions_cleaner_batch_size: '50'
        executions_cleaner_interval_ms: '600000'
        executions_per_job_limit: '10000'
        feature_monitoring_max_num_features: '15'
        featurestore_asof_spine_max_bytes: '1073741824'
        featurestore_asof_spine_max_columns: '256'
        featurestore_asof_spine_max_file_age_ms: '86400000'
        featurestore_asof_spine_max_rows: '1000000'
        featurestore_db_admin_user: featurestore_admin_user
        featurestore_default_quota: -1L
        featurestore_default_storage_format: PARQUET
        featurestore_metrics_enabled: 'true'
        featurestore_metrics_online_ingestion_enabled: 'false'
        featurestore_online_enabled: 'true'
        featurestore_online_tablespace: ''
        file_preview_image_size: '10000000'
        file_preview_txt_size: '100'
        flink_dir: /srv/hops/flink
        flink_user: flink
        flink_version: 1.17.1.0
        fs_job_activity_time: 5m
        fs_storage_connector_session_duration: '3600'
        git_bitbucket_http_proxy: ''
        git_bitbucket_https_proxy: ''
        git_command_timeout_minutes: '60'
        git_custom_ca_configmap: ''
        git_custom_ca_configmap_key: ca-bundle.crt
        git_disable_tls_verification: 'false'
        git_github_http_proxy: ''
        git_github_https_proxy: ''
        git_gitlab_http_proxy: ''
        git_gitlab_https_proxy: ''
        git_image_version: 1.6-SNAPSHOT
        grafana_version: 9.3.16
        ha_enabled: 'true'
        hadoop_dir: /srv/hops/hadoop
        hadoop_version: 3.4.3.3-EE-RC1
        hdfs_base_storage_policy: CLOUD
        hdfs_default_quota: -1L
        hdfs_log_storage_policy: CLOUD
        hdfs_user: hdfs
        hdfscontentsmanager_base_hopsfs_client: libhdfs-go
        hive2_version: 4.1.0.0-v1
        hive_conf_path: /srv/hops/apache-hive/conf
        hive_superuser: hive
        hive_warehouse: /apps/hive/warehouse
        hiveserver_ext_hostname: ''
        hiveserver_ssl_hostname: ''
        hops_db: hops
        hops_rpc_tls: 'true'
        hopsexamples_version: ''
        hopsfsmount_apparmor_profile: ''
        hopsfsmount_log_level: warn
        hopsfsmount_nn_connections: '4'
        hopsworks_analytics: false
        hopsworks_analytics_coding_agent: claude
        hopsworks_analytics_ro_user: hopsworks_ro
        hopsworks_analytics_ro_user_adopt_existing: false
        hopsworks_analytics_setup_repo: https://github.com/logicalclocks/okr-dashboards
        hopsworks_db: hopsworks
        hopsworks_dir: /srv/hops/domains/domain1
        hopsworks_enterprise: 'true'
        hopsworks_mysql_user: hopsworks
        hopsworks_public_proxy_url: ''
        hopsworks_rest_log_level: TEST
        hopsworks_user: payara
        hw_group_mapping_sync_enabled: 'false'
        ingestion_job_cores: '1.0'
        ingestion_job_gpus: '0'
        ingestion_job_memory: '2048'
        java_home: ''
        job_name_validation_regex: ^[a-zA-Z0-9_\-]+$
        jupyter_allow_no_limit_shutdown: true
        jupyter_dir: /srv/hops/jupyter
        jupyter_group: hadoop
        jupyter_hour_shutdown_options: 8,24,72
        jupyter_origin_scheme: https
        jupyter_shell_command: '["/bin/bash", "--login", "-c", "cd -L $JUPYTER_DATA_DIR || true && exec bash"]'
        jupyter_shutdown_timer_interval: 1m
        jupyter_spark_notebook_server_memory_floor_mb: '512'
        jupyter_ws_ping_interval: 10s
        jwt_exp_leeway_sec: '900'
        jwt_issuer: hopsworks@logicalclocks.com
        jwt_lifetime_ms: '86400000'
        jwt_signature_algorithm: HS512
        jwt_signing_key_name: apiKey
        kafka_installed: true
        kafka_max_num_topics: '100'
        kafka_num_partitions: '1'
        kafka_num_replicas: '1'
        kafka_user: kafka
        kafka_version: 4.3.1
        kibana_https_enabled: 'true'
        kibana_multi_tenancy_enabled: 'true'
        kibana_version: 3.8.0
        kube_api_max_attempts: '20'
        kube_hopsworks_default_service_account: hopsworks-default
        kube_knative_domain_name: hopsworks.ai
        kube_knative_lb_domain: ''
        kube_kserve_installed: true
        kube_kserve_tensorflow_version: 2.20.0
        kube_node_taints_monitor_interval: 10m
        kube_scheduling_hopsfsmount_cpu_limits: -1
        kube_scheduling_hopsfsmount_cpu_requests: 1
        kube_scheduling_hopsfsmount_memory_limits_mb: 1024
        kube_scheduling_jobinit_cpu_limits: -1
        kube_scheduling_jobinit_cpu_requests: 0.5
        kube_scheduling_jobinit_memory_limits_mb: 512
        kube_scheduling_jobinit_memory_requests_mb: 256
        kube_serving_max_num_instances: '10'
        kube_serving_min_num_instances: '-1'
        kube_serving_vllm_omni_versions: v0.28.0
        kube_serving_vllm_versions: v0.28.0
        kube_skip_namespace_creation: false
        kube_tainted_nodes: ''
        kube_type: kube_cluster
        kube_user_workload_tolerations: ''
        kubernetes_installed: 'true'
        kueue_project_default_cluster_queue: other
        kueue_project_default_local_queue: other
        kueue_system_jobs_cluster_queue: ''
        kueue_system_jobs_local_queue: ''
        ldap_account_status: '2'
        ldap_attr_binary: java.naming.ldap.attributes.binary
        ldap_dyn_group_target: memberOf
        ldap_group_dn: ''
        ldap_group_mapping: ANY_GROUP->HOPS_USER
        ldap_group_mapping_sync_enabled: 'false'
        ldap_group_mapping_sync_interval: '0'
        ldap_group_search_filter: member=%d
        ldap_group_target: cn
        ldap_groups_search_filter: (&(objectCategory=group)(cn=%c))
        ldap_krb_dyn_grp_search_filter: ''
        ldap_krb_search_filter: krbPrincipalName=%s
        ldap_user_dn: ''
        ldap_user_email: mail
        ldap_user_givenName: givenName
        ldap_user_id: uid
        ldap_user_search_filter: uid=%s
        ldap_user_surname: sn
        library_install_timeout_minutes: '60'
        lifecycle_webhook_cluster_id: ''
        lifecycle_webhook_secret: ''
        lifecycle_webhook_url: ''
        livy_startup_timeout: '240'
        livy_version: 0.8.4-incubating-SNAPSHOT-bin
        loadbalancer_external_domain_datanode: null
        loadbalancer_external_domain_feature_query: null
        loadbalancer_external_domain_mysqld: null
        loadbalancer_external_domain_namenode: null
        loadbalancer_external_domain_online_store_rest_server: null
        loadbalancer_external_domain_opensearch: null
        loadbalancer_external_domain_trino: null
        localhost: 'false'
        log_history_limit: '30'
        logstash_ip: ''
        logstash_port: ''
        logstash_port_beam_jobserver_local: ''
        logstash_port_serving: ''
        logstash_port_sklearn_serving: ''
        logstash_port_tf_serving: ''
        logstash_version: 7.16.3
        managed_cloud_redirect_uri: ''
        managed_docker_registry: 'false'
        management_mode: ''
        max_allowed_long_running_http_requests: '50'
        max_concurrent_base_sync_ops: '5'
        max_env_yml_byte_size: '20000'
        max_num_proj_per_user: '10'
        max_status_poll_retry: '5'
        mount_hopsfs_in_python_job: true
        mount_hopsfs_ray_job_container: 'true'
        mr_user: mapred
        multiregion_watchdog_enabled: 'false'
        multiregion_watchdog_interval: 5s
        multiregion_watchdog_region: ''
        multiregion_watchdog_url: ''
        mysql_dir: /srv/hops/mysql
        ndb_dir: /srv/hop/mysql-cluster
        ndb_user: ''
        ndb_version: 21.04.15
        ndbinfo_db: ndbinfo
        news_webflow_api_key: dcc84358bfd37ffc68dbf18c68f74f478ff160d2286094077a9415ee03fbc805
        news_webflow_api_url: https://api.webflow.com/v2/collections/66bdd44475e24741477e1ae3/items
        notebook_converter_job_timeout_sec: '300'
        npm_registry_url: ''
        oauth_account_status: '1'
        oauth_group_mapping: ''
        oauth_group_mapping_enabled: 'false'
        oauth_group_mapping_sync_enabled: 'false'
        oauth_logout_redirect_uri: hopsworks/
        oauth_redirect_uri: hopsworks/callback
        onlinefs_service_thread_number: '10'
        onlinefs_user_email: onlinefs@hopsworks.ai
        onlinefs_user_password: onlinefspw
        opensearch_default_embedding_index: ''
        opensearch_index_mapping_limit: '1000'
        opensearch_num_default_embedding_index: '1'
        payara_dir: /opt/payara/appserver/glassfish/domains/domain1
        pki_ca_configuration: '{"rootCA":{},"intermediateCA":{},"kubernetesCA":{"subjectAlternativeName":{"dns":["hopsworks0.logicalclocks.com","hops-kubernetes","hops-kubernetes.default","hops-kubernetes.default.svc","hops-kubernetes.default.svc.cluster","hops-kubernetes.default.svc.cluster.local","*.hops-system.svc"],"ip":["10.244.0.1","192.168.30.101","127.0.0.1","10.96.0.10","10.96.0.1"]}}}'
        platform_intelligence_llm_api_key: ''
        platform_intelligence_llm_base_url: ''
        platform_intelligence_llm_model: ''
        preinstalled_python_lib_names: pydoop, pyspark, jupyterlab, sparkmagic, hdfscontents, pyjks, hops-apache-beam, pyopenssl
        project_namespace_labels: ''
        project_namespace_network_policy_allowed_namespaces: ''
        project_namespace_network_policy_enabled: true
        project_namespace_network_policy_reconcile_interval: 1m
        prometheus_port: '9089'
        provenance_archive_delay: '86400'
        provenance_archive_size: '10'
        provenance_cleaner_period: '3600'
        provenance_graph_max_size: '10000'
        provenance_type: FULL
        public_https_port: ''
        pushgateway_cleaner_batch_size: '100'
        pushgateway_group_ttl_minutes: '15'
        pushgateway_monitor_interval_ms: '300000'
        py4j_archive: ''
        pypi_indexer_timer_enabled: 'true'
        pypi_indexer_timer_interval: 1d
        pypi_rest_endpoint: https://pypi.org/pypi/{package}/json
        pypi_simple_endpoint: https://pypi.org/simple/
        python_job_cores: '1.0'
        python_job_gpus: '0'
        python_job_kube_waiting_timeout_ms: '300000'
        python_job_memory: '2048'
        python_library_updates_monitor_interval: 1d
        python_pod_kill_grace_period_seconds: '60'
        pythonapp_cores: '1.0'
        pythonapp_gpus: '0'
        pythonapp_memory: '2048'
        quotas_featuregroups_online_disabled: '-1'
        quotas_featuregroups_online_enabled: '-1'
        quotas_max_parallel_executions: '-1'
        quotas_model_deployments_running: '-1'
        quotas_model_deployments_total: '-1'
        quotas_training_datasets: '-1'
        ray_cluster_max_worker_replicas: '20'
        ray_cluster_shutdown_after_completion: 'true'
        ray_cluster_start_wait_time_seconds: '360'
        ray_cluster_termination_grace_period_seconds: '10'
        ray_enabled: false
        ray_job_driver_cores: '1.0'
        ray_job_driver_gpus: '0'
        ray_job_driver_memory: '4096'
        ray_job_pod_kill_grace_period_seconds: '300'
        ray_job_worker_cores: '1.0'
        ray_job_worker_gpus: '0'
        ray_job_worker_memory: '4096'
        ray_materialization_dir: /srv/hops/ray/job
        ray_version: 2.58.0
        recovery_path: ''
        reject_remote_user_no_group: 'false'
        remote_auth_need_consent: 'true'
        requests_verify: 'true'
        reserved_project_names: hopsworks,information_schema,airflow,glassfish_timers,grafana,hops,metastore,mysql,ndbinfo,performance_schema,sqoop,sys,base,python37,python38,python39,python310,filebeat,airflow,git,onlinefs,sklearnserver,rondb_replication,default,kube-system,kube-public,kube-node-lease,kube_system,kube_public,kube_node_lease
        rmyarn_user: rmyarn
        rondb_quotas: ''
        rondb_usage_cache_ttl_seconds: '60'
        rondb_usage_query_timeout_seconds: '10'
        saas_entry_point_url: ''
        scikit_learn_version: 1.3.2
        service_jwt_exp_leeway_sec: '172800000'
        service_jwt_lifetime_ms: '604800000'
        service_key_rotation_enabled: 'false'
        service_key_rotation_interval: 2d
        serving_allow_stop_after_seconds: '30'
        serving_connection_pool_size: '40'
        serving_feature_log_materialization_cron: 0 0 0 * * ? *
        serving_feature_log_materialization_row_limit: '50000000'
        serving_feature_log_online_ttl_hours: '30'
        serving_feature_logger_batch_bytes: '1048576'
        serving_feature_logger_batch_seconds: '5'
        serving_feature_logger_client_pool_size: '3'
        serving_feature_logger_client_req_timeout_seconds: '3'
        serving_feature_logger_flush_bytes: '1048576'
        serving_feature_logger_flush_interval_seconds: '300'
        serving_feature_logger_max_buffer_bytes: '67108864'
        serving_feature_logger_max_event_bytes: '8388608'
        serving_feature_logger_max_event_rows: '512'
        serving_feature_logger_queue_size: '1000'
        serving_feature_logger_shutdown_seconds: '20'
        serving_feature_logging_transport: realtime
        serving_max_route_connections: '10'
        serving_redeploy_not_found_after_seconds: '120'
        serving_state_manager_batch_size: '25'
        serving_state_manager_enabled: 'true'
        serving_state_manager_interval_ms: '300000'
        spark_dir: /srv/hops/spark
        spark_executor_min_memory: '1024'
        spark_hops_utils_dir: /srv/hops/artifacts
        spark_job_driver_cores: '1.0'
        spark_job_driver_memory: '2048'
        spark_job_executor_cores: '1.0'
        spark_job_executor_memory: '4096'
        spark_launcher_sa_annotations: ''
        spark_pod_kill_grace_period_seconds: '1200'
        spark_remove_job_when_completed: 'true'
        spark_ui_logs_offset: '512000'
        spark_user: spark
        spark_version: 4.1.3.0
        srvmanager_password: srvmanagerpwd
        staging_dir: /srv/hops/staging
        statistics_cleaner_batch_size: '1000'
        statistics_cleaner_interval_ms: '900000'
        streamlit_sharing: false
        sudoers_dir: /srv/hops/sbin
        superset_admin_roles: Admin
        superset_proxy_connect_timeout_ms: '10000'
        superset_proxy_connection_request_timeout_ms: '10000'
        superset_proxy_max_connections: '50'
        superset_proxy_read_timeout_ms: '180000'
        superset_user_roles: Gamma,sql_lab,Dataset
        support_email_addr: support@hopsworks.ai
        tag_history_archive_max_events: '20000'
        tag_history_cleaner_batch_size: '1000'
        tag_history_cleaner_interval_ms: '86400000'
        tag_history_retention_days: '0'
        tensorboard_max_last_accessed: '1140000'
        tensorboard_max_reload_threads: '1'
        tensorflow_version: 2.20.0
        testconnector_image_version: '1.0'
        tf_spark_connector_version: ''
        trino_default_catalog: delta
        trino_events_cleaner_batch_size: '1000'
        trino_events_delete_after_days: '61'
        twofactor_auth: 'false'
        twofactor_excluded_groups: AGENT;CLUSTER_AGENT
        unix_usernames_conf: '{\"glassfish\":\"glassfish\",\"hdfs\":\"hdfs\",\"rmyarn\":\"rmyarn\",\"yarn\":\"yarn\",\"hive\":\"hive\",\"livy\":\"livy\",\"flink\":\"flink\",\"consul\":\"consul\",\"hopsmon\":\"hopsmon\",\"zookeeper\":\"zookeeper\",\"onlinefs\":\"onlinefs\",\"elastic\":\"elastic\",\"kagent\":\"kagent\",\"mysql\":\"mysql\",\"airflow\":\"airflow\"}'
        upload_chunk_size: '10485760'
        upload_policy: enabled
        user_cert_valid_days: '12'
        verification_path: hopsworks-api/api/auth/verify
        yarn_default_payment_type: NOLIMIT
        yarn_default_quota: '60000000'
        yarn_user: yarn
        zookeeper_version: 3.7.1
    ```

<div class="hops-values" markdown>

`hopsworks.variables.admin_email` <a class="headerlink" href="#helm.hopsworks.variables.admin_email" title="Permanent link">#</a> { #helm.hopsworks.variables.admin_email }
:   Type `string`, default `"admin@hopsworks.ai"`.

`hopsworks.variables.admin_password` <a class="headerlink" href="#helm.hopsworks.variables.admin_password" title="Permanent link">#</a> { #helm.hopsworks.variables.admin_password }
:   Type `string`, default `"admin"`.

`hopsworks.variables.agent_deployment_otel_cpu` <a class="headerlink" href="#helm.hopsworks.variables.agent_deployment_otel_cpu" title="Permanent link">#</a> { #helm.hopsworks.variables.agent_deployment_otel_cpu }
:   Type `string`, default `"0.5"`.

`hopsworks.variables.agent_deployment_otel_enabled` <a class="headerlink" href="#helm.hopsworks.variables.agent_deployment_otel_enabled" title="Permanent link">#</a> { #helm.hopsworks.variables.agent_deployment_otel_enabled }
:   Type `string`, default `"true"`.

`hopsworks.variables.agent_deployment_otel_image` <a class="headerlink" href="#helm.hopsworks.variables.agent_deployment_otel_image" title="Permanent link">#</a> { #helm.hopsworks.variables.agent_deployment_otel_image }
:   Type `string`, default `"otlp-sidecar"`.

`hopsworks.variables.agent_deployment_otel_memory_mb` <a class="headerlink" href="#helm.hopsworks.variables.agent_deployment_otel_memory_mb" title="Permanent link">#</a> { #helm.hopsworks.variables.agent_deployment_otel_memory_mb }
:   Type `string`, default `"1024"`.

`hopsworks.variables.agent_jobs_enabled` <a class="headerlink" href="#helm.hopsworks.variables.agent_jobs_enabled" title="Permanent link">#</a> { #helm.hopsworks.variables.agent_jobs_enabled }
:   Type `string`, default `"true"`.

`hopsworks.variables.airflow_dir` <a class="headerlink" href="#helm.hopsworks.variables.airflow_dir" title="Permanent link">#</a> { #helm.hopsworks.variables.airflow_dir }
:   Type `string`, default `"/srv/hops/airflow"`.

`hopsworks.variables.airflow_enabled` <a class="headerlink" href="#helm.hopsworks.variables.airflow_enabled" title="Permanent link">#</a> { #helm.hopsworks.variables.airflow_enabled }
:   Type `bool`, default `true`.

`hopsworks.variables.airflow_user` <a class="headerlink" href="#helm.hopsworks.variables.airflow_user" title="Permanent link">#</a> { #helm.hopsworks.variables.airflow_user }
:   Type `string`, default `"airflow"`.

`hopsworks.variables.airflow_user_email` <a class="headerlink" href="#helm.hopsworks.variables.airflow_user_email" title="Permanent link">#</a> { #helm.hopsworks.variables.airflow_user_email }
:   Type `string`, default `"airflow@hopsworks.ai"`.

`hopsworks.variables.alert_email_addrs` <a class="headerlink" href="#helm.hopsworks.variables.alert_email_addrs" title="Permanent link">#</a> { #helm.hopsworks.variables.alert_email_addrs }
:   Type `string`, default `""`.

`hopsworks.variables.anaconda_dir` <a class="headerlink" href="#helm.hopsworks.variables.anaconda_dir" title="Permanent link">#</a> { #helm.hopsworks.variables.anaconda_dir }
:   Type `string`, default `"/"`.

`hopsworks.variables.anaconda_enabled` <a class="headerlink" href="#helm.hopsworks.variables.anaconda_enabled" title="Permanent link">#</a> { #helm.hopsworks.variables.anaconda_enabled }
:   Type `string`, default `"true"`.

`hopsworks.variables.anaconda_env` <a class="headerlink" href="#helm.hopsworks.variables.anaconda_env" title="Permanent link">#</a> { #helm.hopsworks.variables.anaconda_env }
:   Type `string`, default `""`.

`hopsworks.variables.anaconda_user` <a class="headerlink" href="#helm.hopsworks.variables.anaconda_user" title="Permanent link">#</a> { #helm.hopsworks.variables.anaconda_user }
:   Type `string`, default `"anaconda"`.

`hopsworks.variables.application_certificate_validity_period` <a class="headerlink" href="#helm.hopsworks.variables.application_certificate_validity_period" title="Permanent link">#</a> { #helm.hopsworks.variables.application_certificate_validity_period }
:   Type `string`, default `"3650d"`.

`hopsworks.variables.apply_hopsfsmount_apparmor_profile_kube` <a class="headerlink" href="#helm.hopsworks.variables.apply_hopsfsmount_apparmor_profile_kube" title="Permanent link">#</a> { #helm.hopsworks.variables.apply_hopsfsmount_apparmor_profile_kube }
:   Type `string`, default `"false"`.

`hopsworks.variables.async_services_timer_batch_size` <a class="headerlink" href="#helm.hopsworks.variables.async_services_timer_batch_size" title="Permanent link">#</a> { #helm.hopsworks.variables.async_services_timer_batch_size }
:   Type `string`, default `"1000"`.

`hopsworks.variables.async_services_timer_delete_history_after_days` <a class="headerlink" href="#helm.hopsworks.variables.async_services_timer_delete_history_after_days" title="Permanent link">#</a> { #helm.hopsworks.variables.async_services_timer_delete_history_after_days }
:   Type `string`, default `"7"`.

`hopsworks.variables.async_services_timer_enabled` <a class="headerlink" href="#helm.hopsworks.variables.async_services_timer_enabled" title="Permanent link">#</a> { #helm.hopsworks.variables.async_services_timer_enabled }
:   Type `string`, default `"true"`.

`hopsworks.variables.async_services_timer_interval_ms` <a class="headerlink" href="#helm.hopsworks.variables.async_services_timer_interval_ms" title="Permanent link">#</a> { #helm.hopsworks.variables.async_services_timer_interval_ms }
:   Type `string`, default `"15000"`.

`hopsworks.variables.audit_log_count` <a class="headerlink" href="#helm.hopsworks.variables.audit_log_count" title="Permanent link">#</a> { #helm.hopsworks.variables.audit_log_count }
:   Type `string`, default `"10"`.

`hopsworks.variables.audit_log_file_format` <a class="headerlink" href="#helm.hopsworks.variables.audit_log_file_format" title="Permanent link">#</a> { #helm.hopsworks.variables.audit_log_file_format }
:   Type `string`, default `"server_audit_log%g.log"`.

`hopsworks.variables.audit_log_file_path` <a class="headerlink" href="#helm.hopsworks.variables.audit_log_file_path" title="Permanent link">#</a> { #helm.hopsworks.variables.audit_log_file_path }
:   Type `string`, default `"/audit-logs"`.

`hopsworks.variables.audit_log_file_type` <a class="headerlink" href="#helm.hopsworks.variables.audit_log_file_type" title="Permanent link">#</a> { #helm.hopsworks.variables.audit_log_file_type }
:   Type `string`, default `"io.hops.hopsworks.audit.helper.JSONLogFormatter"`.

`hopsworks.variables.audit_log_size_limit` <a class="headerlink" href="#helm.hopsworks.variables.audit_log_size_limit" title="Permanent link">#</a> { #helm.hopsworks.variables.audit_log_size_limit }
:   Type `string`, default `"256000000"`.

`hopsworks.variables.base_buildkit_image` <a class="headerlink" href="#helm.hopsworks.variables.base_buildkit_image" title="Permanent link">#</a> { #helm.hopsworks.variables.base_buildkit_image }
:   Type `string`, default `"docker.hops.works/hopsworks/moby/buildkit:v0.32.2-rootless"`.

`hopsworks.variables.base_image_name` <a class="headerlink" href="#helm.hopsworks.variables.base_image_name" title="Permanent link">#</a> { #helm.hopsworks.variables.base_image_name }
:   Type `string`, default `"hopsworks-base"`.

`hopsworks.variables.base_image_version` <a class="headerlink" href="#helm.hopsworks.variables.base_image_version" title="Permanent link">#</a> { #helm.hopsworks.variables.base_image_version }
:   Type `string`, default `"5.2.0-SNAPSHOT"`.

`hopsworks.variables.cert_mater_delay` <a class="headerlink" href="#helm.hopsworks.variables.cert_mater_delay" title="Permanent link">#</a> { #helm.hopsworks.variables.cert_mater_delay }
:   Type `string`, default `"3m"`.

`hopsworks.variables.certs_dir` <a class="headerlink" href="#helm.hopsworks.variables.certs_dir" title="Permanent link">#</a> { #helm.hopsworks.variables.certs_dir }
:   Type `string`, default `"/srv/hops/certs-dir"`.

`hopsworks.variables.check_nodemanagers_status` <a class="headerlink" href="#helm.hopsworks.variables.check_nodemanagers_status" title="Permanent link">#</a> { #helm.hopsworks.variables.check_nodemanagers_status }
:   Type `string`, default `""`.

`hopsworks.variables.client_path` <a class="headerlink" href="#helm.hopsworks.variables.client_path" title="Permanent link">#</a> { #helm.hopsworks.variables.client_path }
:   Type `string`, default `"/srv/hops/clients-3.4.3"`.

`hopsworks.variables.cloud` <a class="headerlink" href="#helm.hopsworks.variables.cloud" title="Permanent link">#</a> { #helm.hopsworks.variables.cloud }
:   Type `string`, default `""`.

`hopsworks.variables.command_agent_home_batch` <a class="headerlink" href="#helm.hopsworks.variables.command_agent_home_batch" title="Permanent link">#</a> { #helm.hopsworks.variables.command_agent_home_batch }
:   Type `string`, default `"20"`.

`hopsworks.variables.command_agent_home_claim_lease_as_ms` <a class="headerlink" href="#helm.hopsworks.variables.command_agent_home_claim_lease_as_ms" title="Permanent link">#</a> { #helm.hopsworks.variables.command_agent_home_claim_lease_as_ms }
:   Type `string`, default `"600000"`.

`hopsworks.variables.command_agent_home_migration_period_as_ms` <a class="headerlink" href="#helm.hopsworks.variables.command_agent_home_migration_period_as_ms" title="Permanent link">#</a> { #helm.hopsworks.variables.command_agent_home_migration_period_as_ms }
:   Type `string`, default `"3600000"`.

`hopsworks.variables.command_agent_home_process_timer_period_as_ms` <a class="headerlink" href="#helm.hopsworks.variables.command_agent_home_process_timer_period_as_ms" title="Permanent link">#</a> { #helm.hopsworks.variables.command_agent_home_process_timer_period_as_ms }
:   Type `string`, default `"5000"`.

`hopsworks.variables.command_agent_home_retry_backoff_base_as_ms` <a class="headerlink" href="#helm.hopsworks.variables.command_agent_home_retry_backoff_base_as_ms" title="Permanent link">#</a> { #helm.hopsworks.variables.command_agent_home_retry_backoff_base_as_ms }
:   Type `string`, default `"10000"`.

`hopsworks.variables.command_agent_home_retry_backoff_max_as_ms` <a class="headerlink" href="#helm.hopsworks.variables.command_agent_home_retry_backoff_max_as_ms" title="Permanent link">#</a> { #helm.hopsworks.variables.command_agent_home_retry_backoff_max_as_ms }
:   Type `string`, default `"600000"`.

`hopsworks.variables.command_search_fs_history_clean_period_as_ms` <a class="headerlink" href="#helm.hopsworks.variables.command_search_fs_history_clean_period_as_ms" title="Permanent link">#</a> { #helm.hopsworks.variables.command_search_fs_history_clean_period_as_ms }
:   Type `string`, default `"3600000"`.

`hopsworks.variables.command_search_fs_history_enable` <a class="headerlink" href="#helm.hopsworks.variables.command_search_fs_history_enable" title="Permanent link">#</a> { #helm.hopsworks.variables.command_search_fs_history_enable }
:   Type `string`, default `"false"`.

`hopsworks.variables.command_search_fs_history_window_as_s` <a class="headerlink" href="#helm.hopsworks.variables.command_search_fs_history_window_as_s" title="Permanent link">#</a> { #helm.hopsworks.variables.command_search_fs_history_window_as_s }
:   Type `string`, default `"3600"`.

`hopsworks.variables.command_search_fs_process_timer_period_as_ms` <a class="headerlink" href="#helm.hopsworks.variables.command_search_fs_process_timer_period_as_ms" title="Permanent link">#</a> { #helm.hopsworks.variables.command_search_fs_process_timer_period_as_ms }
:   Type `string`, default `"1000"`.

`hopsworks.variables.command_search_fs_reindex_queue_wait_as_ms` <a class="headerlink" href="#helm.hopsworks.variables.command_search_fs_reindex_queue_wait_as_ms" title="Permanent link">#</a> { #helm.hopsworks.variables.command_search_fs_reindex_queue_wait_as_ms }
:   Type `string`, default `"1800000"`.
    How long a featurestore search reindex run waits for the search command queue to empty and for the featurestore index template to be installed before it is aborted, in milliseconds. The reindex empties the index first, so it only starts on an empty queue, and the template gives the new index its mappings. A run aborted this way is reported under Cluster Settings > Service Operations > OpenSearch Index Commands, where it can be requested again.

`hopsworks.variables.command_search_fs_retry_per_clean_interval` <a class="headerlink" href="#helm.hopsworks.variables.command_search_fs_retry_per_clean_interval" title="Permanent link">#</a> { #helm.hopsworks.variables.command_search_fs_retry_per_clean_interval }
:   Type `string`, default `"5"`.

`hopsworks.variables.conda_default_repo` <a class="headerlink" href="#helm.hopsworks.variables.conda_default_repo" title="Permanent link">#</a> { #helm.hopsworks.variables.conda_default_repo }
:   Type `string`, default `"defaults"`.

`hopsworks.variables.default_jupyter_environment` <a class="headerlink" href="#helm.hopsworks.variables.default_jupyter_environment" title="Permanent link">#</a> { #helm.hopsworks.variables.default_jupyter_environment }
:   Type `string`, default `"pandas-training-pipeline"`.

`hopsworks.variables.default_python_job_environment` <a class="headerlink" href="#helm.hopsworks.variables.default_python_job_environment" title="Permanent link">#</a> { #helm.hopsworks.variables.default_python_job_environment }
:   Type `string`, default `"pandas-training-pipeline"`.

`hopsworks.variables.disable_password_login` <a class="headerlink" href="#helm.hopsworks.variables.disable_password_login" title="Permanent link">#</a> { #helm.hopsworks.variables.disable_password_login }
:   Type `string`, default `"false"`.

`hopsworks.variables.disable_registration` <a class="headerlink" href="#helm.hopsworks.variables.disable_registration" title="Permanent link">#</a> { #helm.hopsworks.variables.disable_registration }
:   Type `string`, default `"false"`.

`hopsworks.variables.dlt_schema_fetch_job_deadline_seconds` <a class="headerlink" href="#helm.hopsworks.variables.dlt_schema_fetch_job_deadline_seconds" title="Permanent link">#</a> { #helm.hopsworks.variables.dlt_schema_fetch_job_deadline_seconds }
:   Type `string`, default `"1800"`.
    activeDeadlineSeconds for dlthub schema-fetch Kubernetes Jobs. Kills schema-fetch pods that never get to run (unschedulable, volume mount failures), which would otherwise be reported as in-progress forever.

`hopsworks.variables.docker_base_image_python_version` <a class="headerlink" href="#helm.hopsworks.variables.docker_base_image_python_version" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_base_image_python_version }
:   Type `string`, default `"3.13"`.

`hopsworks.variables.docker_cgroup_cpu_period` <a class="headerlink" href="#helm.hopsworks.variables.docker_cgroup_cpu_period" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_cgroup_cpu_period }
:   Type `string`, default `"100000"`.

`hopsworks.variables.docker_cgroup_enabled` <a class="headerlink" href="#helm.hopsworks.variables.docker_cgroup_enabled" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_cgroup_enabled }
:   Type `string`, default `"false"`.

`hopsworks.variables.docker_cgroup_parent` <a class="headerlink" href="#helm.hopsworks.variables.docker_cgroup_parent" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_cgroup_parent }
:   Type `string`, default `"docker.slice"`.

`hopsworks.variables.docker_job_mounts_allowed` <a class="headerlink" href="#helm.hopsworks.variables.docker_job_mounts_allowed" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_job_mounts_allowed }
:   Type `string`, default `"false"`.

`hopsworks.variables.docker_job_mounts_list` <a class="headerlink" href="#helm.hopsworks.variables.docker_job_mounts_list" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_job_mounts_list }
:   Type `string`, default `""`.

`hopsworks.variables.docker_job_uid_strict` <a class="headerlink" href="#helm.hopsworks.variables.docker_job_uid_strict" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_job_uid_strict }
:   Type `string`, default `"true"`.

`hopsworks.variables.docker_mounts` <a class="headerlink" href="#helm.hopsworks.variables.docker_mounts" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_mounts }
:   Type `string`.

    ??? note "Default"

        ```yaml
        /srv/hops/hadoop/etc/hadoop,/srv/hops/spark,/srv/hops/flink,/srv/hops/apache-livy
        ```

`hopsworks.variables.docker_operations_allow_hermetic_custom_commands` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_allow_hermetic_custom_commands" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_allow_hermetic_custom_commands }
:   Type `string`, default `"false"`.
    Whether a custom-commands build may declare itself hermetic, with HOPSWORKS_BUILD_HERMETIC=true in its environment file, and so keep its layer cache. Custom command layers are never reused otherwise, because the script can fetch anything and nothing declares what. Only the script's author knows whether that is true of their script, and only the operator decides whether that claim is allowed to control cache reuse.

`hopsworks.variables.docker_operations_backoff_limit` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_backoff_limit" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_backoff_limit }
:   Type `string`, default `"0"`.

`hopsworks.variables.docker_operations_build_metadata` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_build_metadata" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_build_metadata }
:   Type `string`, default `"true"`.
    Capture the package list, environment export and pip check inside the image build so one post-build job reads them instead of three recomputing them. Images built before this existed fall back to the job-based path automatically.

`hopsworks.variables.docker_operations_buildkit_addr` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_buildkit_addr" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_buildkit_addr }
:   Type `string`, default `""`.
    Address of the persistent BuildKit daemon, e.g. tcp://buildkitd-0.buildkitd.hopsworks.svc.cluster.local:1234. Empty starts a private daemon inside each build job, which re-pulls and re-unpacks the base image every time. Leave empty and set global._hopsworks.buildkitd.enabled: the address of the daemon the chart deploys is filled in from buildkitd.name, buildkitd.port and the release namespace. Only set this to point builds at a daemon the chart does not manage. The example is a full pod DNS name rather than a short one because the client verifies the hostname it dials against the certificate: the chart's SANs cover the service and the per-pod names, not a bare "buildkitd", so a short-name address fails verification with mTLS on.

`hopsworks.variables.docker_operations_buildkit_backoff_limit` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_buildkit_backoff_limit" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_buildkit_backoff_limit }
:   Type `string`, default `"0"`.

`hopsworks.variables.docker_operations_buildkit_cache_scope` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_buildkit_cache_scope" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_buildkit_cache_scope }
:   Type `string`, default `"shared"`.
    Scope of the package cache shared between builds: "off", "project" or "shared". Constrained by a pattern rather than an enum: helm-schema infers type: string from the non-empty default and then refuses enum and type together, while pattern coexists with it and rejects the same set of values. The backend still validates at runtime and falls back to "off", since an operator can set this in the variables table without going through the chart. "project" is safe for multi-tenant here because users cannot inject Dockerfile directives: the Dockerfile is generated by the backend, and custom commands supply a shell script that runs inside a RUN. "shared" gives every project one cache and is single-trust-zone only.  This is also the off switch for the toolchain caches a custom-commands build can ask for with HOPSWORKS_BUILD_CACHE (uv, pip, ccache, sccache, maven, gradle, cargo, npm, go). Those are always scoped to the project whatever this is set to, since a script controls what goes into them. Anything other than "off" enables them.  "shared" is the default because the package cache is scoped by index configuration, not by a single cluster-wide id: builds that resolve through the same configuration share, and a project using different index credentials gets a different cache. Every reusable build step also carries a per-project cache-key tag, so a layer is never reused across projects and rotating a credential invalidates reuse, which BuildKit does not do on its own because it leaves secret contents out of cache keys.

`hopsworks.variables.docker_operations_buildkit_extra_args` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_buildkit_extra_args" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_buildkit_extra_args }
:   Type `string`, default `""`.
    Extra arguments appended to every buildctl invocation.  Empty by default. This previously shipped an S3 --export-cache/--import-cache pair. BuildKit resolves S3 credentials at the daemon rather than at the client, so whether it worked depended entirely on what identity the daemon had. On an EKS install with defaultServiceAccount annotations wired for IRSA (see values.aws.yaml) the daemonless build pod carried a web-identity token and the exporter worked. On a cluster with no AWS identity it could not: observed as "no EC2 IMDS role found ... context deadline exceeded" on every build, costing an IMDS timeout per build while caching nothing, with ignore-error hiding the failure rather than avoiding it.  Defaulting it empty therefore removes a remote cache that some installs did have. That is deliberate, because it failed closed and expensively everywhere else, but it is a behaviour change on upgrade rather than the removal of something inert.  Before re-enabling it, give the daemon real credentials and confirm the cache is actually being read. With the daemon enabled it is no longer the build pod, so the build pod's identity no longer applies to it: set buildkitd.serviceAccountName to an account carrying the cloud identity you want the exporter to use. A persistent daemon already avoids the base image re-pull this was reaching for, and does so without leaving the cluster.

`hopsworks.variables.docker_operations_buildkit_limit_cpu` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_buildkit_limit_cpu" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_buildkit_limit_cpu }
:   Type `string`, default `"2"`.

`hopsworks.variables.docker_operations_buildkit_limit_memory` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_buildkit_limit_memory" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_buildkit_limit_memory }
:   Type `string`, default `"4G"`.

`hopsworks.variables.docker_operations_buildkit_priority_class` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_buildkit_priority_class" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_buildkit_priority_class }
:   Type `string`, default `""`.

`hopsworks.variables.docker_operations_buildkit_replicas` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_buildkit_replicas" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_buildkit_replicas }
:   Type `string`, default `"1"`.
    Replica count behind a "%d" placeholder in docker_operations_buildkit_addr, e.g. tcp://buildkitd-%d.buildkitd.hopsworks.svc.cluster.local:1234 with replicas 3. Filled in from buildkitd.replicas unless set here.  This spreads load and cache state across daemons. It is not high availability: a project is pinned to one replica by id and is not retried against another, so a project whose daemon is down waits for it to come back. It is not what separates tenants either; that is mTLS plus the per-project cache key.

`hopsworks.variables.docker_operations_buildkit_request_cpu` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_buildkit_request_cpu" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_buildkit_request_cpu }
:   Type `string`, default `"200m"`.

`hopsworks.variables.docker_operations_buildkit_request_memory` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_buildkit_request_memory" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_buildkit_request_memory }
:   Type `string`, default `"500Mi"`.

`hopsworks.variables.docker_operations_buildkit_storage` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_buildkit_storage" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_buildkit_storage }
:   Type `string`, default `"70Gi"`.

`hopsworks.variables.docker_operations_buildkit_tls_locality` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_buildkit_tls_locality" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_buildkit_tls_locality }
:   Type `string`, default `"buildkitd"`.
    Certificate locality, which is what names the key and certificate files inside that Secret. Must match buildkitd.tls.locality, and is filled in from it.

`hopsworks.variables.docker_operations_buildkit_tls_secret` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_buildkit_tls_secret" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_buildkit_tls_secret }
:   Type `string`, default `""`.
    Secret holding the client certificate the build job presents to the persistent daemon. Empty means the client sends none, which only works against a daemon that requires no client certificate. Filled in from buildkitd.tls when that is enabled.

`hopsworks.variables.docker_operations_cert_name` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_cert_name" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_cert_name }
:   Type `string`, default `"kagent_certificate_bundle.pem"`.

`hopsworks.variables.docker_operations_context_orphan_minutes` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_context_orphan_minutes" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_context_orphan_minutes }
:   Type `string`, default `"120"`.
    Age in minutes after which a build context in S3 whose build no longer exists is deleted. Covers builds that died with Payara or their node, which the per-build cleanup cannot.

`hopsworks.variables.docker_operations_default_service_account` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_default_service_account" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_default_service_account }
:   Type `string`, default `"default"`.

`hopsworks.variables.docker_operations_delete_jobs_add_description_if_fails` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_delete_jobs_add_description_if_fails" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_delete_jobs_add_description_if_fails }
:   Type `bool`, default `false`.

`hopsworks.variables.docker_operations_delete_jobs_on_completion` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_delete_jobs_on_completion" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_delete_jobs_on_completion }
:   Type `string`, default `"true"`.

`hopsworks.variables.docker_operations_docker_context_builder` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_docker_context_builder" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_docker_context_builder }
:   Type `string`, default `"AUTO"`.

`hopsworks.variables.docker_operations_docker_context_builder_s3_bucket` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_docker_context_builder_s3_bucket" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_docker_context_builder_s3_bucket }
:   Type `string`, default `"${env:S3_BUCKET}"`.

`hopsworks.variables.docker_operations_docker_context_builder_s3_endpoint` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_docker_context_builder_s3_endpoint" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_docker_context_builder_s3_endpoint }
:   Type `string`, default `"${env:S3_ENDPOINT}"`.

`hopsworks.variables.docker_operations_docker_context_builder_s3_region` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_docker_context_builder_s3_region" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_docker_context_builder_s3_region }
:   Type `string`, default `"${env:S3_REGION}"`.

`hopsworks.variables.docker_operations_hopsworks_ca_secret_name` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_hopsworks_ca_secret_name" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_hopsworks_ca_secret_name }
:   Type `string`, default `"docker-registry-crypto-material"`.

`hopsworks.variables.docker_operations_image_pull_secrets` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_image_pull_secrets" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_image_pull_secrets }
:   Type `string`, default `""`.

`hopsworks.variables.docker_operations_lock_dependencies` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_lock_dependencies" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_lock_dependencies }
:   Type `string`, default `"false"`.
    Resolve a full dependency set with per-artifact hashes and install only from it. Makes the resolved set reconstructible and fails the build if an index serves different bytes for a version it already served. Needs uv in the base image; builds without it fall back.

`hopsworks.variables.docker_operations_managed_docker_secrets` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_managed_docker_secrets" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_managed_docker_secrets }
:   Type `string`, default `""`.

`hopsworks.variables.docker_operations_multi_region_copy` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_multi_region_copy" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_multi_region_copy }
:   Type `string`, default `"false"`.
    On a multi-region install, copy the built image to the secondary region instead of running the build again there. Building twice does the work twice and is not guaranteed to land the same image: a custom command or an unpinned package can resolve differently between the two runs, leaving the regions with different content under one tag. Off by default because the copy needs pull and push credentials for both registries in a single job.

`hopsworks.variables.docker_operations_oci_worker_snapshotter` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_oci_worker_snapshotter" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_oci_worker_snapshotter }
:   Type `string`, default `"auto"`.

`hopsworks.variables.docker_operations_push_insecure` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_push_insecure" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_push_insecure }
:   Type `string`, default `"false"`.

`hopsworks.variables.docker_operations_registry_container` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_registry_container" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_registry_container }
:   Type `string`, default `"docker"`.

`hopsworks.variables.docker_operations_registry_http` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_registry_http" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_registry_http }
:   Type `string`, default `"false"`.

`hopsworks.variables.docker_operations_registry_pod` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_registry_pod" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_registry_pod }
:   Type `string`, default `"docker-registry-0"`.

`hopsworks.variables.docker_operations_suspend_jobs` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_suspend_jobs" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_suspend_jobs }
:   Type `string`, default `"false"`.

`hopsworks.variables.docker_operations_timeout_check_minutes` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_timeout_check_minutes" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_timeout_check_minutes }
:   Type `string`, default `"15"`.

`hopsworks.variables.docker_operations_timeout_delete_minutes` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_timeout_delete_minutes" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_timeout_delete_minutes }
:   Type `string`, default `"5"`.

`hopsworks.variables.docker_operations_timeout_export_minutes` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_timeout_export_minutes" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_timeout_export_minutes }
:   Type `string`, default `"15"`.

`hopsworks.variables.docker_operations_timeout_listing_minutes` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_timeout_listing_minutes" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_timeout_listing_minutes }
:   Type `string`, default `"15"`.

`hopsworks.variables.docker_operations_timeout_minutes_buildkit` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_timeout_minutes_buildkit" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_timeout_minutes_buildkit }
:   Type `string`, default `"120"`.

`hopsworks.variables.docker_operations_timeout_tag_minutes` <a class="headerlink" href="#helm.hopsworks.variables.docker_operations_timeout_tag_minutes" title="Permanent link">#</a> { #helm.hopsworks.variables.docker_operations_timeout_tag_minutes }
:   Type `string`, default `"5"`.

`hopsworks.variables.download_allowed` <a class="headerlink" href="#helm.hopsworks.variables.download_allowed" title="Permanent link">#</a> { #helm.hopsworks.variables.download_allowed }
:   Type `string`, default `"true"`.

`hopsworks.variables.elastic_dir` <a class="headerlink" href="#helm.hopsworks.variables.elastic_dir" title="Permanent link">#</a> { #helm.hopsworks.variables.elastic_dir }
:   Type `string`, default `"/srv/hops/elastic"`.

`hopsworks.variables.elastic_https_enabled` <a class="headerlink" href="#helm.hopsworks.variables.elastic_https_enabled" title="Permanent link">#</a> { #helm.hopsworks.variables.elastic_https_enabled }
:   Type `string`, default `"true"`.

`hopsworks.variables.elastic_jwt_enabled` <a class="headerlink" href="#helm.hopsworks.variables.elastic_jwt_enabled" title="Permanent link">#</a> { #helm.hopsworks.variables.elastic_jwt_enabled }
:   Type `string`, default `"true"`.

`hopsworks.variables.elastic_jwt_exp_ms` <a class="headerlink" href="#helm.hopsworks.variables.elastic_jwt_exp_ms" title="Permanent link">#</a> { #helm.hopsworks.variables.elastic_jwt_exp_ms }
:   Type `string`, default `"1800000"`.

`hopsworks.variables.elastic_jwt_url_parameter` <a class="headerlink" href="#helm.hopsworks.variables.elastic_jwt_url_parameter" title="Permanent link">#</a> { #helm.hopsworks.variables.elastic_jwt_url_parameter }
:   Type `string`, default `"jt"`.

`hopsworks.variables.elastic_logs_index_expiration` <a class="headerlink" href="#helm.hopsworks.variables.elastic_logs_index_expiration" title="Permanent link">#</a> { #helm.hopsworks.variables.elastic_logs_index_expiration }
:   Type `string`, default `"604800000"`.

`hopsworks.variables.elastic_opendistro_security_enabled` <a class="headerlink" href="#helm.hopsworks.variables.elastic_opendistro_security_enabled" title="Permanent link">#</a> { #helm.hopsworks.variables.elastic_opendistro_security_enabled }
:   Type `string`, default `"true"`.

`hopsworks.variables.elastic_user` <a class="headerlink" href="#helm.hopsworks.variables.elastic_user" title="Permanent link">#</a> { #helm.hopsworks.variables.elastic_user }
:   Type `string`, default `"elastic"`.

`hopsworks.variables.elastic_version` <a class="headerlink" href="#helm.hopsworks.variables.elastic_version" title="Permanent link">#</a> { #helm.hopsworks.variables.elastic_version }
:   Type `string`, default `"3.8.0"`.

`hopsworks.variables.enable_adls_storage_connectors` <a class="headerlink" href="#helm.hopsworks.variables.enable_adls_storage_connectors" title="Permanent link">#</a> { #helm.hopsworks.variables.enable_adls_storage_connectors }
:   Type `string`, default `"false"`.

`hopsworks.variables.enable_bigquery_storage_connectors` <a class="headerlink" href="#helm.hopsworks.variables.enable_bigquery_storage_connectors" title="Permanent link">#</a> { #helm.hopsworks.variables.enable_bigquery_storage_connectors }
:   Type `string`, default `"true"`.

`hopsworks.variables.enable_bring_your_own_kafka` <a class="headerlink" href="#helm.hopsworks.variables.enable_bring_your_own_kafka" title="Permanent link">#</a> { #helm.hopsworks.variables.enable_bring_your_own_kafka }
:   Type `string`, default `"false"`.

`hopsworks.variables.enable_elasticsearch_storage_connectors` <a class="headerlink" href="#helm.hopsworks.variables.enable_elasticsearch_storage_connectors" title="Permanent link">#</a> { #helm.hopsworks.variables.enable_elasticsearch_storage_connectors }
:   Type `string`, default `"true"`.

`hopsworks.variables.enable_feature_monitoring` <a class="headerlink" href="#helm.hopsworks.variables.enable_feature_monitoring" title="Permanent link">#</a> { #helm.hopsworks.variables.enable_feature_monitoring }
:   Type `string`, default `"true"`.

`hopsworks.variables.enable_fix_receivers_timer` <a class="headerlink" href="#helm.hopsworks.variables.enable_fix_receivers_timer" title="Permanent link">#</a> { #helm.hopsworks.variables.enable_fix_receivers_timer }
:   Type `string`, default `"true"`.

`hopsworks.variables.enable_gcs_storage_connectors` <a class="headerlink" href="#helm.hopsworks.variables.enable_gcs_storage_connectors" title="Permanent link">#</a> { #helm.hopsworks.variables.enable_gcs_storage_connectors }
:   Type `string`, default `"true"`.

`hopsworks.variables.enable_jupyter_python_kernel_non_kubernetes` <a class="headerlink" href="#helm.hopsworks.variables.enable_jupyter_python_kernel_non_kubernetes" title="Permanent link">#</a> { #helm.hopsworks.variables.enable_jupyter_python_kernel_non_kubernetes }
:   Type `string`, default `"false"`.

`hopsworks.variables.enable_kafka_storage_connectors` <a class="headerlink" href="#helm.hopsworks.variables.enable_kafka_storage_connectors" title="Permanent link">#</a> { #helm.hopsworks.variables.enable_kafka_storage_connectors }
:   Type `string`, default `"true"`.

`hopsworks.variables.enable_metadata_designer` <a class="headerlink" href="#helm.hopsworks.variables.enable_metadata_designer" title="Permanent link">#</a> { #helm.hopsworks.variables.enable_metadata_designer }
:   Type `string`, default `""`.

`hopsworks.variables.enable_opensearch_storage_connectors` <a class="headerlink" href="#helm.hopsworks.variables.enable_opensearch_storage_connectors" title="Permanent link">#</a> { #helm.hopsworks.variables.enable_opensearch_storage_connectors }
:   Type `string`, default `"true"`.

`hopsworks.variables.enable_read_only_git_repositories` <a class="headerlink" href="#helm.hopsworks.variables.enable_read_only_git_repositories" title="Permanent link">#</a> { #helm.hopsworks.variables.enable_read_only_git_repositories }
:   Type `string`, default `"false"`.

`hopsworks.variables.enable_redshift_storage_connectors` <a class="headerlink" href="#helm.hopsworks.variables.enable_redshift_storage_connectors" title="Permanent link">#</a> { #helm.hopsworks.variables.enable_redshift_storage_connectors }
:   Type `string`, default `"true"`.

`hopsworks.variables.enable_snowflake_storage_connectors` <a class="headerlink" href="#helm.hopsworks.variables.enable_snowflake_storage_connectors" title="Permanent link">#</a> { #helm.hopsworks.variables.enable_snowflake_storage_connectors }
:   Type `string`, default `"true"`.

`hopsworks.variables.enable_user_search` <a class="headerlink" href="#helm.hopsworks.variables.enable_user_search" title="Permanent link">#</a> { #helm.hopsworks.variables.enable_user_search }
:   Type `string`, default `"true"`.

`hopsworks.variables.epipe_version` <a class="headerlink" href="#helm.hopsworks.variables.epipe_version" title="Permanent link">#</a> { #helm.hopsworks.variables.epipe_version }
:   Type `string`, default `"0.20.0"`.

`hopsworks.variables.executions_cleaner_batch_size` <a class="headerlink" href="#helm.hopsworks.variables.executions_cleaner_batch_size" title="Permanent link">#</a> { #helm.hopsworks.variables.executions_cleaner_batch_size }
:   Type `string`, default `"50"`.

`hopsworks.variables.executions_cleaner_interval_ms` <a class="headerlink" href="#helm.hopsworks.variables.executions_cleaner_interval_ms" title="Permanent link">#</a> { #helm.hopsworks.variables.executions_cleaner_interval_ms }
:   Type `string`, default `"600000"`.

`hopsworks.variables.executions_per_job_limit` <a class="headerlink" href="#helm.hopsworks.variables.executions_per_job_limit" title="Permanent link">#</a> { #helm.hopsworks.variables.executions_per_job_limit }
:   Type `string`, default `"10000"`.

`hopsworks.variables.feature_monitoring_max_num_features` <a class="headerlink" href="#helm.hopsworks.variables.feature_monitoring_max_num_features" title="Permanent link">#</a> { #helm.hopsworks.variables.feature_monitoring_max_num_features }
:   Type `string`, default `"15"`.

`hopsworks.variables.featurestore_asof_spine_max_bytes` <a class="headerlink" href="#helm.hopsworks.variables.featurestore_asof_spine_max_bytes" title="Permanent link">#</a> { #helm.hopsworks.variables.featurestore_asof_spine_max_bytes }
:   Type `string`, default `"1073741824"`.

`hopsworks.variables.featurestore_asof_spine_max_columns` <a class="headerlink" href="#helm.hopsworks.variables.featurestore_asof_spine_max_columns" title="Permanent link">#</a> { #helm.hopsworks.variables.featurestore_asof_spine_max_columns }
:   Type `string`, default `"256"`.

`hopsworks.variables.featurestore_asof_spine_max_file_age_ms` <a class="headerlink" href="#helm.hopsworks.variables.featurestore_asof_spine_max_file_age_ms" title="Permanent link">#</a> { #helm.hopsworks.variables.featurestore_asof_spine_max_file_age_ms }
:   Type `string`, default `"86400000"`.

`hopsworks.variables.featurestore_asof_spine_max_rows` <a class="headerlink" href="#helm.hopsworks.variables.featurestore_asof_spine_max_rows" title="Permanent link">#</a> { #helm.hopsworks.variables.featurestore_asof_spine_max_rows }
:   Type `string`, default `"1000000"`.

`hopsworks.variables.featurestore_db_admin_user` <a class="headerlink" href="#helm.hopsworks.variables.featurestore_db_admin_user" title="Permanent link">#</a> { #helm.hopsworks.variables.featurestore_db_admin_user }
:   Type `string`, default `"featurestore_admin_user"`.

`hopsworks.variables.featurestore_default_quota` <a class="headerlink" href="#helm.hopsworks.variables.featurestore_default_quota" title="Permanent link">#</a> { #helm.hopsworks.variables.featurestore_default_quota }
:   Type `string`, default `"-1L"`.

`hopsworks.variables.featurestore_default_storage_format` <a class="headerlink" href="#helm.hopsworks.variables.featurestore_default_storage_format" title="Permanent link">#</a> { #helm.hopsworks.variables.featurestore_default_storage_format }
:   Type `string`, default `"PARQUET"`.

`hopsworks.variables.featurestore_metrics_enabled` <a class="headerlink" href="#helm.hopsworks.variables.featurestore_metrics_enabled" title="Permanent link">#</a> { #helm.hopsworks.variables.featurestore_metrics_enabled }
:   Type `string`, default `"true"`.

`hopsworks.variables.featurestore_metrics_online_ingestion_enabled` <a class="headerlink" href="#helm.hopsworks.variables.featurestore_metrics_online_ingestion_enabled" title="Permanent link">#</a> { #helm.hopsworks.variables.featurestore_metrics_online_ingestion_enabled }
:   Type `string`, default `"false"`.

`hopsworks.variables.featurestore_online_enabled` <a class="headerlink" href="#helm.hopsworks.variables.featurestore_online_enabled" title="Permanent link">#</a> { #helm.hopsworks.variables.featurestore_online_enabled }
:   Type `string`, default `"true"`.

`hopsworks.variables.featurestore_online_tablespace` <a class="headerlink" href="#helm.hopsworks.variables.featurestore_online_tablespace" title="Permanent link">#</a> { #helm.hopsworks.variables.featurestore_online_tablespace }
:   Type `string`, default `""`.

`hopsworks.variables.file_preview_image_size` <a class="headerlink" href="#helm.hopsworks.variables.file_preview_image_size" title="Permanent link">#</a> { #helm.hopsworks.variables.file_preview_image_size }
:   Type `string`, default `"10000000"`.

`hopsworks.variables.file_preview_txt_size` <a class="headerlink" href="#helm.hopsworks.variables.file_preview_txt_size" title="Permanent link">#</a> { #helm.hopsworks.variables.file_preview_txt_size }
:   Type `string`, default `"100"`.

`hopsworks.variables.flink_dir` <a class="headerlink" href="#helm.hopsworks.variables.flink_dir" title="Permanent link">#</a> { #helm.hopsworks.variables.flink_dir }
:   Type `string`, default `"/srv/hops/flink"`.

`hopsworks.variables.flink_user` <a class="headerlink" href="#helm.hopsworks.variables.flink_user" title="Permanent link">#</a> { #helm.hopsworks.variables.flink_user }
:   Type `string`, default `"flink"`.

`hopsworks.variables.flink_version` <a class="headerlink" href="#helm.hopsworks.variables.flink_version" title="Permanent link">#</a> { #helm.hopsworks.variables.flink_version }
:   Type `string`, default `"1.17.1.0"`.

`hopsworks.variables.fs_job_activity_time` <a class="headerlink" href="#helm.hopsworks.variables.fs_job_activity_time" title="Permanent link">#</a> { #helm.hopsworks.variables.fs_job_activity_time }
:   Type `string`, default `"5m"`.

`hopsworks.variables.fs_storage_connector_session_duration` <a class="headerlink" href="#helm.hopsworks.variables.fs_storage_connector_session_duration" title="Permanent link">#</a> { #helm.hopsworks.variables.fs_storage_connector_session_duration }
:   Type `string`, default `"3600"`.

`hopsworks.variables.git_bitbucket_http_proxy` <a class="headerlink" href="#helm.hopsworks.variables.git_bitbucket_http_proxy" title="Permanent link">#</a> { #helm.hopsworks.variables.git_bitbucket_http_proxy }
:   Type `string`, default `""`.
    Proxy for git traffic to BitBucket over HTTP. Empty means a direct connection.

`hopsworks.variables.git_bitbucket_https_proxy` <a class="headerlink" href="#helm.hopsworks.variables.git_bitbucket_https_proxy" title="Permanent link">#</a> { #helm.hopsworks.variables.git_bitbucket_https_proxy }
:   Type `string`, default `""`.
    Proxy for git traffic to BitBucket over HTTPS. Empty means a direct connection.

`hopsworks.variables.git_command_timeout_minutes` <a class="headerlink" href="#helm.hopsworks.variables.git_command_timeout_minutes" title="Permanent link">#</a> { #helm.hopsworks.variables.git_command_timeout_minutes }
:   Type `string`, default `"60"`.

`hopsworks.variables.git_custom_ca_configmap` <a class="headerlink" href="#helm.hopsworks.variables.git_custom_ca_configmap" title="Permanent link">#</a> { #helm.hopsworks.variables.git_custom_ca_configmap }
:   Type `string`, default `""`.
    Name of a ConfigMap holding CA certificates that git operations should trust in addition to the public anchors the git image already ships, so repositories on a self-hosted GitLab / GitHub Enterprise / BitBucket behind a private CA can be cloned and pushed to over HTTPS. The ConfigMap must exist in **every project namespace**, since git runs there, and is expected to be distributed by the platform rather than by this chart. Leave empty to trust only the public anchors. Applies to HTTPS remotes only; SSH host-key verification is unaffected. This value is seeded on every install and upgrade, so edits made in the admin UI do not survive a `helm upgrade` -- configure it here.

`hopsworks.variables.git_custom_ca_configmap_key` <a class="headerlink" href="#helm.hopsworks.variables.git_custom_ca_configmap_key" title="Permanent link">#</a> { #helm.hopsworks.variables.git_custom_ca_configmap_key }
:   Type `string`, default `"ca-bundle.crt"`.
    Key within `git_custom_ca_configmap` holding the certificates. One key, which may hold several concatenated PEM certificates; an admin with several providers puts all their CAs in it. Ignored when `git_custom_ca_configmap` is empty, and must not be blank when it is set.

`hopsworks.variables.git_disable_tls_verification` <a class="headerlink" href="#helm.hopsworks.variables.git_disable_tls_verification" title="Permanent link">#</a> { #helm.hopsworks.variables.git_disable_tls_verification }
:   Type `string`, default `"false"`.
    Disable TLS certificate verification for **all** git remotes, public ones included. Connections can then be intercepted without detection, so prefer naming the CA to trust in `git_custom_ca_configmap`; this exists for deployments where that is not workable. Applies cluster-wide, not per provider. Seeded on every install and upgrade, like the other git variables.

`hopsworks.variables.git_github_http_proxy` <a class="headerlink" href="#helm.hopsworks.variables.git_github_http_proxy" title="Permanent link">#</a> { #helm.hopsworks.variables.git_github_http_proxy }
:   Type `string`, default `""`.
    Proxy for git traffic to GitHub over HTTP, e.g. `http://proxy.corp:3128`. Empty means a direct connection. Configured per provider because a deployment may reach each of them by a different route. Traffic between the git container and Hopsworks itself never goes through these proxies. Seeded on every install and upgrade, like the other git variables.

`hopsworks.variables.git_github_https_proxy` <a class="headerlink" href="#helm.hopsworks.variables.git_github_https_proxy" title="Permanent link">#</a> { #helm.hopsworks.variables.git_github_https_proxy }
:   Type `string`, default `""`.
    Proxy for git traffic to GitHub over HTTPS. This is the one that matters in practice, since Hopsworks drives git over HTTPS remotes.

`hopsworks.variables.git_gitlab_http_proxy` <a class="headerlink" href="#helm.hopsworks.variables.git_gitlab_http_proxy" title="Permanent link">#</a> { #helm.hopsworks.variables.git_gitlab_http_proxy }
:   Type `string`, default `""`.
    Proxy for git traffic to GitLab over HTTP. Empty means a direct connection.

`hopsworks.variables.git_gitlab_https_proxy` <a class="headerlink" href="#helm.hopsworks.variables.git_gitlab_https_proxy" title="Permanent link">#</a> { #helm.hopsworks.variables.git_gitlab_https_proxy }
:   Type `string`, default `""`.
    Proxy for git traffic to GitLab over HTTPS. Empty means a direct connection.

`hopsworks.variables.git_image_version` <a class="headerlink" href="#helm.hopsworks.variables.git_image_version" title="Permanent link">#</a> { #helm.hopsworks.variables.git_image_version }
:   Type `string`, default `"1.6-SNAPSHOT"`.

`hopsworks.variables.grafana_version` <a class="headerlink" href="#helm.hopsworks.variables.grafana_version" title="Permanent link">#</a> { #helm.hopsworks.variables.grafana_version }
:   Type `string`, default `"9.3.16"`.

`hopsworks.variables.ha_enabled` <a class="headerlink" href="#helm.hopsworks.variables.ha_enabled" title="Permanent link">#</a> { #helm.hopsworks.variables.ha_enabled }
:   Type `string`, default `"true"`.

`hopsworks.variables.hadoop_dir` <a class="headerlink" href="#helm.hopsworks.variables.hadoop_dir" title="Permanent link">#</a> { #helm.hopsworks.variables.hadoop_dir }
:   Type `string`, default `"/srv/hops/hadoop"`.

`hopsworks.variables.hadoop_version` <a class="headerlink" href="#helm.hopsworks.variables.hadoop_version" title="Permanent link">#</a> { #helm.hopsworks.variables.hadoop_version }
:   Type `string`, default `"3.4.3.3-EE-RC1"`.

`hopsworks.variables.hdfs_base_storage_policy` <a class="headerlink" href="#helm.hopsworks.variables.hdfs_base_storage_policy" title="Permanent link">#</a> { #helm.hopsworks.variables.hdfs_base_storage_policy }
:   Type `string`, default `"CLOUD"`.

`hopsworks.variables.hdfs_default_quota` <a class="headerlink" href="#helm.hopsworks.variables.hdfs_default_quota" title="Permanent link">#</a> { #helm.hopsworks.variables.hdfs_default_quota }
:   Type `string`, default `"-1L"`.

`hopsworks.variables.hdfs_log_storage_policy` <a class="headerlink" href="#helm.hopsworks.variables.hdfs_log_storage_policy" title="Permanent link">#</a> { #helm.hopsworks.variables.hdfs_log_storage_policy }
:   Type `string`, default `"CLOUD"`.

`hopsworks.variables.hdfs_user` <a class="headerlink" href="#helm.hopsworks.variables.hdfs_user" title="Permanent link">#</a> { #helm.hopsworks.variables.hdfs_user }
:   Type `string`, default `"hdfs"`.

`hopsworks.variables.hdfscontentsmanager_base_hopsfs_client` <a class="headerlink" href="#helm.hopsworks.variables.hdfscontentsmanager_base_hopsfs_client" title="Permanent link">#</a> { #helm.hopsworks.variables.hdfscontentsmanager_base_hopsfs_client }
:   Type `string`, default `"libhdfs-go"`.

`hopsworks.variables.hive2_version` <a class="headerlink" href="#helm.hopsworks.variables.hive2_version" title="Permanent link">#</a> { #helm.hopsworks.variables.hive2_version }
:   Type `string`, default `"4.1.0.0-v1"`.

`hopsworks.variables.hive_conf_path` <a class="headerlink" href="#helm.hopsworks.variables.hive_conf_path" title="Permanent link">#</a> { #helm.hopsworks.variables.hive_conf_path }
:   Type `string`, default `"/srv/hops/apache-hive/conf"`.

`hopsworks.variables.hive_superuser` <a class="headerlink" href="#helm.hopsworks.variables.hive_superuser" title="Permanent link">#</a> { #helm.hopsworks.variables.hive_superuser }
:   Type `string`, default `"hive"`.

`hopsworks.variables.hive_warehouse` <a class="headerlink" href="#helm.hopsworks.variables.hive_warehouse" title="Permanent link">#</a> { #helm.hopsworks.variables.hive_warehouse }
:   Type `string`, default `"/apps/hive/warehouse"`.

`hopsworks.variables.hiveserver_ext_hostname` <a class="headerlink" href="#helm.hopsworks.variables.hiveserver_ext_hostname" title="Permanent link">#</a> { #helm.hopsworks.variables.hiveserver_ext_hostname }
:   Type `string`, default `""`.

`hopsworks.variables.hiveserver_ssl_hostname` <a class="headerlink" href="#helm.hopsworks.variables.hiveserver_ssl_hostname" title="Permanent link">#</a> { #helm.hopsworks.variables.hiveserver_ssl_hostname }
:   Type `string`, default `""`.

`hopsworks.variables.hops_db` <a class="headerlink" href="#helm.hopsworks.variables.hops_db" title="Permanent link">#</a> { #helm.hopsworks.variables.hops_db }
:   Type `string`, default `"hops"`.

`hopsworks.variables.hops_rpc_tls` <a class="headerlink" href="#helm.hopsworks.variables.hops_rpc_tls" title="Permanent link">#</a> { #helm.hopsworks.variables.hops_rpc_tls }
:   Type `string`, default `"true"`.

`hopsworks.variables.hopsexamples_version` <a class="headerlink" href="#helm.hopsworks.variables.hopsexamples_version" title="Permanent link">#</a> { #helm.hopsworks.variables.hopsexamples_version }
:   Type `string`, default `""`.

`hopsworks.variables.hopsfsmount_apparmor_profile` <a class="headerlink" href="#helm.hopsworks.variables.hopsfsmount_apparmor_profile" title="Permanent link">#</a> { #helm.hopsworks.variables.hopsfsmount_apparmor_profile }
:   Type `string`, default `""`.

`hopsworks.variables.hopsfsmount_log_level` <a class="headerlink" href="#helm.hopsworks.variables.hopsfsmount_log_level" title="Permanent link">#</a> { #helm.hopsworks.variables.hopsfsmount_log_level }
:   Type `string`, default `"warn"`.

`hopsworks.variables.hopsfsmount_nn_connections` <a class="headerlink" href="#helm.hopsworks.variables.hopsfsmount_nn_connections" title="Permanent link">#</a> { #helm.hopsworks.variables.hopsfsmount_nn_connections }
:   Type `string`, default `"4"`.

`hopsworks.variables.hopsworks_analytics` <a class="headerlink" href="#helm.hopsworks.variables.hopsworks_analytics" title="Permanent link">#</a> { #helm.hopsworks.variables.hopsworks_analytics }
:   Type `bool`, default `false`.
    When true, the backend creates a reserved 'hopsworks_analytics' project whose members are the cluster admins (HOPS_ADMIN), and attaches a read-only SQL (MySQL) data source onto the local 'hopsworks' database (user hopsworks_analytics_ro_user) to the 'hopsworks_analytics' project itself. Clearing it withdraws the read-only database account, so the two keys must stay required together. Enabling this on a cluster with create_secrets=false additionally requires adding a key named after hopsworks_analytics_ro_user to the hand-created hopsworks-users-secrets, holding the read-only account's password.  This value is the only supported switch. The read-only account, its password and the grants are provisioned by the chart, so flipping the 'hopsworks_analytics' row from the admin variables page creates the project and its members but no data source, and the next upgrade sets the row back to this value.  What the read-only account can read: a curated SELECT allow-list of metadata tables (see roTables in dml/grants.sql.template), not the whole database and never feature data. Several of those tables carry user identities as email addresses: project.username, project_team.team_member, jobs.creator, executions.user and dataset_request.user_email. Anyone with the shared Superset connection, which is every active HOPS_ADMIN, can read them, and the dashboard setup can sample rows from mounted tables into the configured model provider. Treat the account as exposing cluster users' addresses to cluster admins and to that provider.

`hopsworks.variables.hopsworks_analytics_coding_agent` <a class="headerlink" href="#helm.hopsworks.variables.hopsworks_analytics_coding_agent" title="Permanent link">#</a> { #helm.hopsworks.variables.hopsworks_analytics_coding_agent }
:   Type `string`, default `"claude"`.
    Which coding agent the Setup Analytics wizard runs: "claude" (Claude Code), "codex" (OpenAI Codex CLI), "copilot" (GitHub Copilot CLI) or "opencode". The wizard uses this without asking, so setting it is how a cluster standardises on one agent; an advanced option in the wizard lets a user run a different one for their own session, which does not write back here. All four are installed in the terminal image under exactly these command names, so the value is the command. Constrained by a pattern rather than an enum for the reason given on docker_operations_package_cache_scope. The frontend falls back to "claude" when the row is missing or holds a value it does not recognise.

`hopsworks.variables.hopsworks_analytics_ro_user` <a class="headerlink" href="#helm.hopsworks.variables.hopsworks_analytics_ro_user" title="Permanent link">#</a> { #helm.hopsworks.variables.hopsworks_analytics_ro_user }
:   Type `string`, default `"hopsworks_ro"`.

`hopsworks.variables.hopsworks_analytics_ro_user_adopt_existing` <a class="headerlink" href="#helm.hopsworks.variables.hopsworks_analytics_ro_user_adopt_existing" title="Permanent link">#</a> { #helm.hopsworks.variables.hopsworks_analytics_ro_user_adopt_existing }
:   Type `bool`, default `false`.
    Take over a database account that already exists under hopsworks_analytics_ro_user but was not created by this chart. Off by default, and the install fails with the account name rather than adopting it, because adoption rewrites the account's password, strips its privileges and replaces them with the analytics allow-list. Set it to true only when that account is yours to hand over. The chart records the account it provisioned in the hopsworks_analytics_ro_user_managed variable and withdraws only that one.

`hopsworks.variables.hopsworks_analytics_setup_repo` <a class="headerlink" href="#helm.hopsworks.variables.hopsworks_analytics_setup_repo" title="Permanent link">#</a> { #helm.hopsworks.variables.hopsworks_analytics_setup_repo }
:   Type `string`, default `"https://github.com/logicalclocks/okr-dashboards"`.
    Repository the Setup Analytics wizard clones when the terminal image does not already carry it, so a cluster that cannot reach github.com can point the flow at a reachable mirror instead of failing in the Terminal with a git error. The checkout directory is derived from the last path segment. Constrained to characters that cannot change the meaning of the shell line the URL is spliced into; the frontend falls back to the default when the row is missing or fails that check.

`hopsworks.variables.hopsworks_db` <a class="headerlink" href="#helm.hopsworks.variables.hopsworks_db" title="Permanent link">#</a> { #helm.hopsworks.variables.hopsworks_db }
:   Type `string`, default `"hopsworks"`.

`hopsworks.variables.hopsworks_dir` <a class="headerlink" href="#helm.hopsworks.variables.hopsworks_dir" title="Permanent link">#</a> { #helm.hopsworks.variables.hopsworks_dir }
:   Type `string`, default `"/srv/hops/domains/domain1"`.

`hopsworks.variables.hopsworks_enterprise` <a class="headerlink" href="#helm.hopsworks.variables.hopsworks_enterprise" title="Permanent link">#</a> { #helm.hopsworks.variables.hopsworks_enterprise }
:   Type `string`, default `"true"`.

`hopsworks.variables.hopsworks_mysql_user` <a class="headerlink" href="#helm.hopsworks.variables.hopsworks_mysql_user" title="Permanent link">#</a> { #helm.hopsworks.variables.hopsworks_mysql_user }
:   Type `string`, default `"hopsworks"`.

`hopsworks.variables.hopsworks_public_proxy_url` <a class="headerlink" href="#helm.hopsworks.variables.hopsworks_public_proxy_url" title="Permanent link">#</a> { #helm.hopsworks.variables.hopsworks_public_proxy_url }
:   Type `string`, default `""`.

`hopsworks.variables.hopsworks_rest_log_level` <a class="headerlink" href="#helm.hopsworks.variables.hopsworks_rest_log_level" title="Permanent link">#</a> { #helm.hopsworks.variables.hopsworks_rest_log_level }
:   Type `string`, default `"TEST"`.

`hopsworks.variables.hopsworks_user` <a class="headerlink" href="#helm.hopsworks.variables.hopsworks_user" title="Permanent link">#</a> { #helm.hopsworks.variables.hopsworks_user }
:   Type `string`, default `"payara"`.

`hopsworks.variables.hw_group_mapping_sync_enabled` <a class="headerlink" href="#helm.hopsworks.variables.hw_group_mapping_sync_enabled" title="Permanent link">#</a> { #helm.hopsworks.variables.hw_group_mapping_sync_enabled }
:   Type `string`, default `"false"`.

`hopsworks.variables.ingestion_job_cores` <a class="headerlink" href="#helm.hopsworks.variables.ingestion_job_cores" title="Permanent link">#</a> { #helm.hopsworks.variables.ingestion_job_cores }
:   Type `string`, default `"1.0"`.

`hopsworks.variables.ingestion_job_gpus` <a class="headerlink" href="#helm.hopsworks.variables.ingestion_job_gpus" title="Permanent link">#</a> { #helm.hopsworks.variables.ingestion_job_gpus }
:   Type `string`, default `"0"`.

`hopsworks.variables.ingestion_job_memory` <a class="headerlink" href="#helm.hopsworks.variables.ingestion_job_memory" title="Permanent link">#</a> { #helm.hopsworks.variables.ingestion_job_memory }
:   Type `string`, default `"2048"`.

`hopsworks.variables.java_home` <a class="headerlink" href="#helm.hopsworks.variables.java_home" title="Permanent link">#</a> { #helm.hopsworks.variables.java_home }
:   Type `string`, default `""`.

`hopsworks.variables.job_name_validation_regex` <a class="headerlink" href="#helm.hopsworks.variables.job_name_validation_regex" title="Permanent link">#</a> { #helm.hopsworks.variables.job_name_validation_regex }
:   Type `string`, default `"^[a-zA-Z0-9_\\-]+$"`.

`hopsworks.variables.jupyter_allow_no_limit_shutdown` <a class="headerlink" href="#helm.hopsworks.variables.jupyter_allow_no_limit_shutdown" title="Permanent link">#</a> { #helm.hopsworks.variables.jupyter_allow_no_limit_shutdown }
:   Type `bool`, default `true`.

`hopsworks.variables.jupyter_dir` <a class="headerlink" href="#helm.hopsworks.variables.jupyter_dir" title="Permanent link">#</a> { #helm.hopsworks.variables.jupyter_dir }
:   Type `string`, default `"/srv/hops/jupyter"`.

`hopsworks.variables.jupyter_group` <a class="headerlink" href="#helm.hopsworks.variables.jupyter_group" title="Permanent link">#</a> { #helm.hopsworks.variables.jupyter_group }
:   Type `string`, default `"hadoop"`.

`hopsworks.variables.jupyter_hour_shutdown_options` <a class="headerlink" href="#helm.hopsworks.variables.jupyter_hour_shutdown_options" title="Permanent link">#</a> { #helm.hopsworks.variables.jupyter_hour_shutdown_options }
:   Type `string`, default `"8,24,72"`.

`hopsworks.variables.jupyter_origin_scheme` <a class="headerlink" href="#helm.hopsworks.variables.jupyter_origin_scheme" title="Permanent link">#</a> { #helm.hopsworks.variables.jupyter_origin_scheme }
:   Type `string`, default `"https"`.

`hopsworks.variables.jupyter_shell_command` <a class="headerlink" href="#helm.hopsworks.variables.jupyter_shell_command" title="Permanent link">#</a> { #helm.hopsworks.variables.jupyter_shell_command }
:   Type `string`.

    ??? note "Default"

        ```yaml
        '["/bin/bash", "--login", "-c", "cd -L $JUPYTER_DATA_DIR || true && exec bash"]'
        ```

`hopsworks.variables.jupyter_shutdown_timer_interval` <a class="headerlink" href="#helm.hopsworks.variables.jupyter_shutdown_timer_interval" title="Permanent link">#</a> { #helm.hopsworks.variables.jupyter_shutdown_timer_interval }
:   Type `string`, default `"1m"`.

`hopsworks.variables.jupyter_spark_notebook_server_memory_floor_mb` <a class="headerlink" href="#helm.hopsworks.variables.jupyter_spark_notebook_server_memory_floor_mb" title="Permanent link">#</a> { #helm.hopsworks.variables.jupyter_spark_notebook_server_memory_floor_mb }
:   Type `string`, default `"512"`.

`hopsworks.variables.jupyter_ws_ping_interval` <a class="headerlink" href="#helm.hopsworks.variables.jupyter_ws_ping_interval" title="Permanent link">#</a> { #helm.hopsworks.variables.jupyter_ws_ping_interval }
:   Type `string`, default `"10s"`.

`hopsworks.variables.jwt_exp_leeway_sec` <a class="headerlink" href="#helm.hopsworks.variables.jwt_exp_leeway_sec" title="Permanent link">#</a> { #helm.hopsworks.variables.jwt_exp_leeway_sec }
:   Type `string`, default `"900"`.

`hopsworks.variables.jwt_issuer` <a class="headerlink" href="#helm.hopsworks.variables.jwt_issuer" title="Permanent link">#</a> { #helm.hopsworks.variables.jwt_issuer }
:   Type `string`, default `"hopsworks@logicalclocks.com"`.

`hopsworks.variables.jwt_lifetime_ms` <a class="headerlink" href="#helm.hopsworks.variables.jwt_lifetime_ms" title="Permanent link">#</a> { #helm.hopsworks.variables.jwt_lifetime_ms }
:   Type `string`, default `"86400000"`.

`hopsworks.variables.jwt_signature_algorithm` <a class="headerlink" href="#helm.hopsworks.variables.jwt_signature_algorithm" title="Permanent link">#</a> { #helm.hopsworks.variables.jwt_signature_algorithm }
:   Type `string`, default `"HS512"`.

`hopsworks.variables.jwt_signing_key_name` <a class="headerlink" href="#helm.hopsworks.variables.jwt_signing_key_name" title="Permanent link">#</a> { #helm.hopsworks.variables.jwt_signing_key_name }
:   Type `string`, default `"apiKey"`.

`hopsworks.variables.kafka_installed` <a class="headerlink" href="#helm.hopsworks.variables.kafka_installed" title="Permanent link">#</a> { #helm.hopsworks.variables.kafka_installed }
:   Type `bool`, default `true`.

`hopsworks.variables.kafka_max_num_topics` <a class="headerlink" href="#helm.hopsworks.variables.kafka_max_num_topics" title="Permanent link">#</a> { #helm.hopsworks.variables.kafka_max_num_topics }
:   Type `string`, default `"100"`.

`hopsworks.variables.kafka_num_partitions` <a class="headerlink" href="#helm.hopsworks.variables.kafka_num_partitions" title="Permanent link">#</a> { #helm.hopsworks.variables.kafka_num_partitions }
:   Type `string`, default `"1"`.

`hopsworks.variables.kafka_num_replicas` <a class="headerlink" href="#helm.hopsworks.variables.kafka_num_replicas" title="Permanent link">#</a> { #helm.hopsworks.variables.kafka_num_replicas }
:   Type `string`, default `"1"`.

`hopsworks.variables.kafka_user` <a class="headerlink" href="#helm.hopsworks.variables.kafka_user" title="Permanent link">#</a> { #helm.hopsworks.variables.kafka_user }
:   Type `string`, default `"kafka"`.

`hopsworks.variables.kafka_version` <a class="headerlink" href="#helm.hopsworks.variables.kafka_version" title="Permanent link">#</a> { #helm.hopsworks.variables.kafka_version }
:   Type `string`, default `"4.3.1"`.

`hopsworks.variables.kibana_https_enabled` <a class="headerlink" href="#helm.hopsworks.variables.kibana_https_enabled" title="Permanent link">#</a> { #helm.hopsworks.variables.kibana_https_enabled }
:   Type `string`, default `"true"`.

`hopsworks.variables.kibana_multi_tenancy_enabled` <a class="headerlink" href="#helm.hopsworks.variables.kibana_multi_tenancy_enabled" title="Permanent link">#</a> { #helm.hopsworks.variables.kibana_multi_tenancy_enabled }
:   Type `string`, default `"true"`.

`hopsworks.variables.kibana_version` <a class="headerlink" href="#helm.hopsworks.variables.kibana_version" title="Permanent link">#</a> { #helm.hopsworks.variables.kibana_version }
:   Type `string`, default `"3.8.0"`.

`hopsworks.variables.kube_api_max_attempts` <a class="headerlink" href="#helm.hopsworks.variables.kube_api_max_attempts" title="Permanent link">#</a> { #helm.hopsworks.variables.kube_api_max_attempts }
:   Type `string`, default `"20"`.

`hopsworks.variables.kube_hopsworks_default_service_account` <a class="headerlink" href="#helm.hopsworks.variables.kube_hopsworks_default_service_account" title="Permanent link">#</a> { #helm.hopsworks.variables.kube_hopsworks_default_service_account }
:   Type `string`, default `"hopsworks-default"`.

`hopsworks.variables.kube_knative_domain_name` <a class="headerlink" href="#helm.hopsworks.variables.kube_knative_domain_name" title="Permanent link">#</a> { #helm.hopsworks.variables.kube_knative_domain_name }
:   Type `string`, default `"hopsworks.ai"`.

`hopsworks.variables.kube_knative_lb_domain` <a class="headerlink" href="#helm.hopsworks.variables.kube_knative_lb_domain" title="Permanent link">#</a> { #helm.hopsworks.variables.kube_knative_lb_domain }
:   Type `string`, default `""`.

`hopsworks.variables.kube_kserve_installed` <a class="headerlink" href="#helm.hopsworks.variables.kube_kserve_installed" title="Permanent link">#</a> { #helm.hopsworks.variables.kube_kserve_installed }
:   Type `bool`, default `true`.

`hopsworks.variables.kube_kserve_tensorflow_version` <a class="headerlink" href="#helm.hopsworks.variables.kube_kserve_tensorflow_version" title="Permanent link">#</a> { #helm.hopsworks.variables.kube_kserve_tensorflow_version }
:   Type `string`, default `"2.20.0"`.

`hopsworks.variables.kube_node_taints_monitor_interval` <a class="headerlink" href="#helm.hopsworks.variables.kube_node_taints_monitor_interval" title="Permanent link">#</a> { #helm.hopsworks.variables.kube_node_taints_monitor_interval }
:   Type `string`, default `"10m"`.

`hopsworks.variables.kube_scheduling_hopsfsmount_cpu_limits` <a class="headerlink" href="#helm.hopsworks.variables.kube_scheduling_hopsfsmount_cpu_limits" title="Permanent link">#</a> { #helm.hopsworks.variables.kube_scheduling_hopsfsmount_cpu_limits }
:   Type `int`, default `-1`.

`hopsworks.variables.kube_scheduling_hopsfsmount_cpu_requests` <a class="headerlink" href="#helm.hopsworks.variables.kube_scheduling_hopsfsmount_cpu_requests" title="Permanent link">#</a> { #helm.hopsworks.variables.kube_scheduling_hopsfsmount_cpu_requests }
:   Type `int`, default `1`.

`hopsworks.variables.kube_scheduling_hopsfsmount_memory_limits_mb` <a class="headerlink" href="#helm.hopsworks.variables.kube_scheduling_hopsfsmount_memory_limits_mb" title="Permanent link">#</a> { #helm.hopsworks.variables.kube_scheduling_hopsfsmount_memory_limits_mb }
:   Type `int`, default `1024`.

`hopsworks.variables.kube_scheduling_jobinit_cpu_limits` <a class="headerlink" href="#helm.hopsworks.variables.kube_scheduling_jobinit_cpu_limits" title="Permanent link">#</a> { #helm.hopsworks.variables.kube_scheduling_jobinit_cpu_limits }
:   Type `int`, default `-1`.

`hopsworks.variables.kube_scheduling_jobinit_cpu_requests` <a class="headerlink" href="#helm.hopsworks.variables.kube_scheduling_jobinit_cpu_requests" title="Permanent link">#</a> { #helm.hopsworks.variables.kube_scheduling_jobinit_cpu_requests }
:   Type `float`, default `0.5`.

`hopsworks.variables.kube_scheduling_jobinit_memory_limits_mb` <a class="headerlink" href="#helm.hopsworks.variables.kube_scheduling_jobinit_memory_limits_mb" title="Permanent link">#</a> { #helm.hopsworks.variables.kube_scheduling_jobinit_memory_limits_mb }
:   Type `int`, default `512`.

`hopsworks.variables.kube_scheduling_jobinit_memory_requests_mb` <a class="headerlink" href="#helm.hopsworks.variables.kube_scheduling_jobinit_memory_requests_mb" title="Permanent link">#</a> { #helm.hopsworks.variables.kube_scheduling_jobinit_memory_requests_mb }
:   Type `int`, default `256`.

`hopsworks.variables.kube_serving_max_num_instances` <a class="headerlink" href="#helm.hopsworks.variables.kube_serving_max_num_instances" title="Permanent link">#</a> { #helm.hopsworks.variables.kube_serving_max_num_instances }
:   Type `string`, default `"10"`.

`hopsworks.variables.kube_serving_min_num_instances` <a class="headerlink" href="#helm.hopsworks.variables.kube_serving_min_num_instances" title="Permanent link">#</a> { #helm.hopsworks.variables.kube_serving_min_num_instances }
:   Type `string`, default `"-1"`.

`hopsworks.variables.kube_serving_vllm_omni_versions` <a class="headerlink" href="#helm.hopsworks.variables.kube_serving_vllm_omni_versions" title="Permanent link">#</a> { #helm.hopsworks.variables.kube_serving_vllm_omni_versions }
:   Type `string`, default `"v0.28.0"`.

`hopsworks.variables.kube_serving_vllm_versions` <a class="headerlink" href="#helm.hopsworks.variables.kube_serving_vllm_versions" title="Permanent link">#</a> { #helm.hopsworks.variables.kube_serving_vllm_versions }
:   Type `string`, default `"v0.28.0"`.

`hopsworks.variables.kube_skip_namespace_creation` <a class="headerlink" href="#helm.hopsworks.variables.kube_skip_namespace_creation" title="Permanent link">#</a> { #helm.hopsworks.variables.kube_skip_namespace_creation }
:   Type `bool`, default `false`.

`hopsworks.variables.kube_tainted_nodes` <a class="headerlink" href="#helm.hopsworks.variables.kube_tainted_nodes" title="Permanent link">#</a> { #helm.hopsworks.variables.kube_tainted_nodes }
:   Type `string`, default `""`.

`hopsworks.variables.kube_type` <a class="headerlink" href="#helm.hopsworks.variables.kube_type" title="Permanent link">#</a> { #helm.hopsworks.variables.kube_type }
:   Type `string`, default `"kube_cluster"`.

`hopsworks.variables.kube_user_workload_tolerations` <a class="headerlink" href="#helm.hopsworks.variables.kube_user_workload_tolerations" title="Permanent link">#</a> { #helm.hopsworks.variables.kube_user_workload_tolerations }
:   Type `string`, default `""`.
    Kubernetes tolerations applied to all user-triggered compute pods. Comma-separated entries of the form key\[=value\]\[:effect\] matching kubectl taint grammar. Effect is optional (empty matches any effect). Example: 'nvidia.com/gpu=true:NoSchedule,dedicated=tenant-a:NoSchedule'

`hopsworks.variables.kubernetes_installed` <a class="headerlink" href="#helm.hopsworks.variables.kubernetes_installed" title="Permanent link">#</a> { #helm.hopsworks.variables.kubernetes_installed }
:   Type `string`, default `"true"`.

`hopsworks.variables.kueue_project_default_cluster_queue` <a class="headerlink" href="#helm.hopsworks.variables.kueue_project_default_cluster_queue" title="Permanent link">#</a> { #helm.hopsworks.variables.kueue_project_default_cluster_queue }
:   Type `string`, default `"other"`.

`hopsworks.variables.kueue_project_default_local_queue` <a class="headerlink" href="#helm.hopsworks.variables.kueue_project_default_local_queue" title="Permanent link">#</a> { #helm.hopsworks.variables.kueue_project_default_local_queue }
:   Type `string`, default `"other"`.

`hopsworks.variables.kueue_system_jobs_cluster_queue` <a class="headerlink" href="#helm.hopsworks.variables.kueue_system_jobs_cluster_queue" title="Permanent link">#</a> { #helm.hopsworks.variables.kueue_system_jobs_cluster_queue }
:   Type `string`, default `""`.

`hopsworks.variables.kueue_system_jobs_local_queue` <a class="headerlink" href="#helm.hopsworks.variables.kueue_system_jobs_local_queue" title="Permanent link">#</a> { #helm.hopsworks.variables.kueue_system_jobs_local_queue }
:   Type `string`, default `""`.

`hopsworks.variables.ldap_account_status` <a class="headerlink" href="#helm.hopsworks.variables.ldap_account_status" title="Permanent link">#</a> { #helm.hopsworks.variables.ldap_account_status }
:   Type `string`, default `"2"`.

`hopsworks.variables.ldap_attr_binary` <a class="headerlink" href="#helm.hopsworks.variables.ldap_attr_binary" title="Permanent link">#</a> { #helm.hopsworks.variables.ldap_attr_binary }
:   Type `string`, default `"java.naming.ldap.attributes.binary"`.

`hopsworks.variables.ldap_dyn_group_target` <a class="headerlink" href="#helm.hopsworks.variables.ldap_dyn_group_target" title="Permanent link">#</a> { #helm.hopsworks.variables.ldap_dyn_group_target }
:   Type `string`, default `"memberOf"`.

`hopsworks.variables.ldap_group_dn` <a class="headerlink" href="#helm.hopsworks.variables.ldap_group_dn" title="Permanent link">#</a> { #helm.hopsworks.variables.ldap_group_dn }
:   Type `string`, default `""`.

`hopsworks.variables.ldap_group_mapping` <a class="headerlink" href="#helm.hopsworks.variables.ldap_group_mapping" title="Permanent link">#</a> { #helm.hopsworks.variables.ldap_group_mapping }
:   Type `string`, default `"ANY_GROUP->HOPS_USER"`.

`hopsworks.variables.ldap_group_mapping_sync_enabled` <a class="headerlink" href="#helm.hopsworks.variables.ldap_group_mapping_sync_enabled" title="Permanent link">#</a> { #helm.hopsworks.variables.ldap_group_mapping_sync_enabled }
:   Type `string`, default `"false"`.

`hopsworks.variables.ldap_group_mapping_sync_interval` <a class="headerlink" href="#helm.hopsworks.variables.ldap_group_mapping_sync_interval" title="Permanent link">#</a> { #helm.hopsworks.variables.ldap_group_mapping_sync_interval }
:   Type `string`, default `"0"`.

`hopsworks.variables.ldap_group_search_filter` <a class="headerlink" href="#helm.hopsworks.variables.ldap_group_search_filter" title="Permanent link">#</a> { #helm.hopsworks.variables.ldap_group_search_filter }
:   Type `string`, default `"member=%d"`.

`hopsworks.variables.ldap_group_target` <a class="headerlink" href="#helm.hopsworks.variables.ldap_group_target" title="Permanent link">#</a> { #helm.hopsworks.variables.ldap_group_target }
:   Type `string`, default `"cn"`.

`hopsworks.variables.ldap_groups_search_filter` <a class="headerlink" href="#helm.hopsworks.variables.ldap_groups_search_filter" title="Permanent link">#</a> { #helm.hopsworks.variables.ldap_groups_search_filter }
:   Type `string`, default `"(&(objectCategory=group)(cn=%c))"`.

`hopsworks.variables.ldap_krb_dyn_grp_search_filter` <a class="headerlink" href="#helm.hopsworks.variables.ldap_krb_dyn_grp_search_filter" title="Permanent link">#</a> { #helm.hopsworks.variables.ldap_krb_dyn_grp_search_filter }
:   Type `string`, default `""`.

`hopsworks.variables.ldap_krb_search_filter` <a class="headerlink" href="#helm.hopsworks.variables.ldap_krb_search_filter" title="Permanent link">#</a> { #helm.hopsworks.variables.ldap_krb_search_filter }
:   Type `string`, default `"krbPrincipalName=%s"`.

`hopsworks.variables.ldap_user_dn` <a class="headerlink" href="#helm.hopsworks.variables.ldap_user_dn" title="Permanent link">#</a> { #helm.hopsworks.variables.ldap_user_dn }
:   Type `string`, default `""`.

`hopsworks.variables.ldap_user_email` <a class="headerlink" href="#helm.hopsworks.variables.ldap_user_email" title="Permanent link">#</a> { #helm.hopsworks.variables.ldap_user_email }
:   Type `string`, default `"mail"`.

`hopsworks.variables.ldap_user_givenName` <a class="headerlink" href="#helm.hopsworks.variables.ldap_user_givenName" title="Permanent link">#</a> { #helm.hopsworks.variables.ldap_user_givenName }
:   Type `string`, default `"givenName"`.

`hopsworks.variables.ldap_user_id` <a class="headerlink" href="#helm.hopsworks.variables.ldap_user_id" title="Permanent link">#</a> { #helm.hopsworks.variables.ldap_user_id }
:   Type `string`, default `"uid"`.

`hopsworks.variables.ldap_user_search_filter` <a class="headerlink" href="#helm.hopsworks.variables.ldap_user_search_filter" title="Permanent link">#</a> { #helm.hopsworks.variables.ldap_user_search_filter }
:   Type `string`, default `"uid=%s"`.

`hopsworks.variables.ldap_user_surname` <a class="headerlink" href="#helm.hopsworks.variables.ldap_user_surname" title="Permanent link">#</a> { #helm.hopsworks.variables.ldap_user_surname }
:   Type `string`, default `"sn"`.

`hopsworks.variables.library_install_timeout_minutes` <a class="headerlink" href="#helm.hopsworks.variables.library_install_timeout_minutes" title="Permanent link">#</a> { #helm.hopsworks.variables.library_install_timeout_minutes }
:   Type `string`, default `"60"`.

`hopsworks.variables.lifecycle_webhook_cluster_id` <a class="headerlink" href="#helm.hopsworks.variables.lifecycle_webhook_cluster_id" title="Permanent link">#</a> { #helm.hopsworks.variables.lifecycle_webhook_cluster_id }
:   Type `string`, default `""`.
    clusterId added to the lifecycle webhook envelope. Omitted when unset.

`hopsworks.variables.lifecycle_webhook_secret` <a class="headerlink" href="#helm.hopsworks.variables.lifecycle_webhook_secret" title="Permanent link">#</a> { #helm.hopsworks.variables.lifecycle_webhook_secret }
:   Type `string`, default `""`.
    HMAC-SHA256 signing key for the lifecycle webhook (X-Hopsworks-Signature). Empty sends unsigned. Seeded hidden.

`hopsworks.variables.lifecycle_webhook_url` <a class="headerlink" href="#helm.hopsworks.variables.lifecycle_webhook_url" title="Permanent link">#</a> { #helm.hopsworks.variables.lifecycle_webhook_url }
:   Type `string`, default `""`.
    Receiver URL for user/project/membership lifecycle events (HTTP POST, at-least-once). Empty disables it. Usable on standalone clusters, not SAAS-only.

`hopsworks.variables.livy_startup_timeout` <a class="headerlink" href="#helm.hopsworks.variables.livy_startup_timeout" title="Permanent link">#</a> { #helm.hopsworks.variables.livy_startup_timeout }
:   Type `string`, default `"240"`.

`hopsworks.variables.livy_version` <a class="headerlink" href="#helm.hopsworks.variables.livy_version" title="Permanent link">#</a> { #helm.hopsworks.variables.livy_version }
:   Type `string`, default `"0.8.4-incubating-SNAPSHOT-bin"`.

`hopsworks.variables.loadbalancer_external_domain_datanode` <a class="headerlink" href="#helm.hopsworks.variables.loadbalancer_external_domain_datanode" title="Permanent link">#</a> { #helm.hopsworks.variables.loadbalancer_external_domain_datanode }
:   Type `string`, default `nil`.
    The domain name of the external load balancer for the HopsFS datanodes. If the load balancer is pre-provisioned then set the domain here, otherwise the hopsworks-update-lb-domains job will discover the domain name and set automatically

`hopsworks.variables.loadbalancer_external_domain_feature_query` <a class="headerlink" href="#helm.hopsworks.variables.loadbalancer_external_domain_feature_query" title="Permanent link">#</a> { #helm.hopsworks.variables.loadbalancer_external_domain_feature_query }
:   Type `string`, default `nil`.
    The domain name of the external load balancer for arrowflight. If the load balancer is pre-provisioned then set the domain here, otherwise the hopsworks-update-lb-domains job will discover the domain name and set automatically

`hopsworks.variables.loadbalancer_external_domain_mysqld` <a class="headerlink" href="#helm.hopsworks.variables.loadbalancer_external_domain_mysqld" title="Permanent link">#</a> { #helm.hopsworks.variables.loadbalancer_external_domain_mysqld }
:   Type `string`, default `nil`.
    The domain name of the external load balancer for mysqld. If the load balancer is pre-provisioned then set the domain here, otherwise the hopsworks-update-lb-domains job will discover the domain name and set automatically

`hopsworks.variables.loadbalancer_external_domain_namenode` <a class="headerlink" href="#helm.hopsworks.variables.loadbalancer_external_domain_namenode" title="Permanent link">#</a> { #helm.hopsworks.variables.loadbalancer_external_domain_namenode }
:   Type `string`, default `nil`.
    The domain name of the external load balancer for the HopsFS namenode. If the load balancer is pre-provisioned then set the domain here, otherwise the hopsworks-update-lb-domains job will discover the domain name and set automatically

`hopsworks.variables.loadbalancer_external_domain_online_store_rest_server` <a class="headerlink" href="#helm.hopsworks.variables.loadbalancer_external_domain_online_store_rest_server" title="Permanent link">#</a> { #helm.hopsworks.variables.loadbalancer_external_domain_online_store_rest_server }
:   Type `string`, default `nil`.
    The domain name of the external load balancer for RDRS. If the load balancer is pre-provisioned then set the domain here, otherwise the hopsworks-update-lb-domains job will discover the domain name and set automatically

`hopsworks.variables.loadbalancer_external_domain_opensearch` <a class="headerlink" href="#helm.hopsworks.variables.loadbalancer_external_domain_opensearch" title="Permanent link">#</a> { #helm.hopsworks.variables.loadbalancer_external_domain_opensearch }
:   Type `string`, default `nil`.
    The domain name of the external load balancer for opensearch. If the load balancer is pre-provisioned then set the domain here, otherwise the hopsworks-update-lb-domains job will discover the domain name and set automatically

`hopsworks.variables.loadbalancer_external_domain_trino` <a class="headerlink" href="#helm.hopsworks.variables.loadbalancer_external_domain_trino" title="Permanent link">#</a> { #helm.hopsworks.variables.loadbalancer_external_domain_trino }
:   Type `string`, default `nil`.
    The domain name of the external load balancer for Trino. If the load balancer is pre-provisioned then set the domain here, otherwise the hopsworks-update-lb-domains job will discover the domain name and set automatically

`hopsworks.variables.localhost` <a class="headerlink" href="#helm.hopsworks.variables.localhost" title="Permanent link">#</a> { #helm.hopsworks.variables.localhost }
:   Type `string`, default `"false"`.

`hopsworks.variables.log_history_limit` <a class="headerlink" href="#helm.hopsworks.variables.log_history_limit" title="Permanent link">#</a> { #helm.hopsworks.variables.log_history_limit }
:   Type `string`, default `"30"`.
    Cap on entries kept in the Log History UI (serving/agent deployments, Jupyter). Archives beyond this count are deleted after each archive, oldest first. A value <= 0 disables rotation.

`hopsworks.variables.logstash_ip` <a class="headerlink" href="#helm.hopsworks.variables.logstash_ip" title="Permanent link">#</a> { #helm.hopsworks.variables.logstash_ip }
:   Type `string`, default `""`.

`hopsworks.variables.logstash_port` <a class="headerlink" href="#helm.hopsworks.variables.logstash_port" title="Permanent link">#</a> { #helm.hopsworks.variables.logstash_port }
:   Type `string`, default `""`.

`hopsworks.variables.logstash_port_beam_jobserver_local` <a class="headerlink" href="#helm.hopsworks.variables.logstash_port_beam_jobserver_local" title="Permanent link">#</a> { #helm.hopsworks.variables.logstash_port_beam_jobserver_local }
:   Type `string`, default `""`.

`hopsworks.variables.logstash_port_serving` <a class="headerlink" href="#helm.hopsworks.variables.logstash_port_serving" title="Permanent link">#</a> { #helm.hopsworks.variables.logstash_port_serving }
:   Type `string`, default `""`.

`hopsworks.variables.logstash_port_sklearn_serving` <a class="headerlink" href="#helm.hopsworks.variables.logstash_port_sklearn_serving" title="Permanent link">#</a> { #helm.hopsworks.variables.logstash_port_sklearn_serving }
:   Type `string`, default `""`.

`hopsworks.variables.logstash_port_tf_serving` <a class="headerlink" href="#helm.hopsworks.variables.logstash_port_tf_serving" title="Permanent link">#</a> { #helm.hopsworks.variables.logstash_port_tf_serving }
:   Type `string`, default `""`.

`hopsworks.variables.logstash_version` <a class="headerlink" href="#helm.hopsworks.variables.logstash_version" title="Permanent link">#</a> { #helm.hopsworks.variables.logstash_version }
:   Type `string`, default `"7.16.3"`.

`hopsworks.variables.managed_cloud_redirect_uri` <a class="headerlink" href="#helm.hopsworks.variables.managed_cloud_redirect_uri" title="Permanent link">#</a> { #helm.hopsworks.variables.managed_cloud_redirect_uri }
:   Type `string`, default `""`.

`hopsworks.variables.managed_docker_registry` <a class="headerlink" href="#helm.hopsworks.variables.managed_docker_registry" title="Permanent link">#</a> { #helm.hopsworks.variables.managed_docker_registry }
:   Type `string`, default `"false"`.

`hopsworks.variables.management_mode` <a class="headerlink" href="#helm.hopsworks.variables.management_mode" title="Permanent link">#</a> { #helm.hopsworks.variables.management_mode }
:   Type `string`, default `""`.
    SAAS bridge: 'STANDALONE' (default, stock Hopsworks) or 'SAAS_MANAGED' (auth and project quota delegated to hopsworks-saas). Unset falls back to STANDALONE.

`hopsworks.variables.max_allowed_long_running_http_requests` <a class="headerlink" href="#helm.hopsworks.variables.max_allowed_long_running_http_requests" title="Permanent link">#</a> { #helm.hopsworks.variables.max_allowed_long_running_http_requests }
:   Type `string`, default `"50"`.

`hopsworks.variables.max_concurrent_base_sync_ops` <a class="headerlink" href="#helm.hopsworks.variables.max_concurrent_base_sync_ops" title="Permanent link">#</a> { #helm.hopsworks.variables.max_concurrent_base_sync_ops }
:   Type `string`, default `"5"`.

`hopsworks.variables.max_env_yml_byte_size` <a class="headerlink" href="#helm.hopsworks.variables.max_env_yml_byte_size" title="Permanent link">#</a> { #helm.hopsworks.variables.max_env_yml_byte_size }
:   Type `string`, default `"20000"`.

`hopsworks.variables.max_num_proj_per_user` <a class="headerlink" href="#helm.hopsworks.variables.max_num_proj_per_user" title="Permanent link">#</a> { #helm.hopsworks.variables.max_num_proj_per_user }
:   Type `string`, default `"10"`.

`hopsworks.variables.max_status_poll_retry` <a class="headerlink" href="#helm.hopsworks.variables.max_status_poll_retry" title="Permanent link">#</a> { #helm.hopsworks.variables.max_status_poll_retry }
:   Type `string`, default `"5"`.

`hopsworks.variables.mount_hopsfs_ray_job_container` <a class="headerlink" href="#helm.hopsworks.variables.mount_hopsfs_ray_job_container" title="Permanent link">#</a> { #helm.hopsworks.variables.mount_hopsfs_ray_job_container }
:   Type `string`, default `"true"`.

`hopsworks.variables.mr_user` <a class="headerlink" href="#helm.hopsworks.variables.mr_user" title="Permanent link">#</a> { #helm.hopsworks.variables.mr_user }
:   Type `string`, default `"mapred"`.

`hopsworks.variables.multiregion_watchdog_enabled` <a class="headerlink" href="#helm.hopsworks.variables.multiregion_watchdog_enabled" title="Permanent link">#</a> { #helm.hopsworks.variables.multiregion_watchdog_enabled }
:   Type `string`, default `"false"`.

`hopsworks.variables.multiregion_watchdog_interval` <a class="headerlink" href="#helm.hopsworks.variables.multiregion_watchdog_interval" title="Permanent link">#</a> { #helm.hopsworks.variables.multiregion_watchdog_interval }
:   Type `string`, default `"5s"`.

`hopsworks.variables.multiregion_watchdog_region` <a class="headerlink" href="#helm.hopsworks.variables.multiregion_watchdog_region" title="Permanent link">#</a> { #helm.hopsworks.variables.multiregion_watchdog_region }
:   Type `string`, default `""`.

`hopsworks.variables.multiregion_watchdog_url` <a class="headerlink" href="#helm.hopsworks.variables.multiregion_watchdog_url" title="Permanent link">#</a> { #helm.hopsworks.variables.multiregion_watchdog_url }
:   Type `string`, default `""`.

`hopsworks.variables.mysql_dir` <a class="headerlink" href="#helm.hopsworks.variables.mysql_dir" title="Permanent link">#</a> { #helm.hopsworks.variables.mysql_dir }
:   Type `string`, default `"/srv/hops/mysql"`.

`hopsworks.variables.ndb_dir` <a class="headerlink" href="#helm.hopsworks.variables.ndb_dir" title="Permanent link">#</a> { #helm.hopsworks.variables.ndb_dir }
:   Type `string`, default `"/srv/hop/mysql-cluster"`.

`hopsworks.variables.ndb_user` <a class="headerlink" href="#helm.hopsworks.variables.ndb_user" title="Permanent link">#</a> { #helm.hopsworks.variables.ndb_user }
:   Type `string`, default `""`.

`hopsworks.variables.ndb_version` <a class="headerlink" href="#helm.hopsworks.variables.ndb_version" title="Permanent link">#</a> { #helm.hopsworks.variables.ndb_version }
:   Type `string`, default `"21.04.15"`.

`hopsworks.variables.ndbinfo_db` <a class="headerlink" href="#helm.hopsworks.variables.ndbinfo_db" title="Permanent link">#</a> { #helm.hopsworks.variables.ndbinfo_db }
:   Type `string`, default `"ndbinfo"`.

`hopsworks.variables.news_webflow_api_key` <a class="headerlink" href="#helm.hopsworks.variables.news_webflow_api_key" title="Permanent link">#</a> { #helm.hopsworks.variables.news_webflow_api_key }
:   Type `string`, default `"dcc84358bfd37ffc68dbf18c68f74f478ff160d2286094077a9415ee03fbc805"`.

`hopsworks.variables.news_webflow_api_url` <a class="headerlink" href="#helm.hopsworks.variables.news_webflow_api_url" title="Permanent link">#</a> { #helm.hopsworks.variables.news_webflow_api_url }
:   Type `string`, default `"https://api.webflow.com/v2/collections/66bdd44475e24741477e1ae3/items"`.

`hopsworks.variables.notebook_converter_job_timeout_sec` <a class="headerlink" href="#helm.hopsworks.variables.notebook_converter_job_timeout_sec" title="Permanent link">#</a> { #helm.hopsworks.variables.notebook_converter_job_timeout_sec }
:   Type `string`, default `"300"`.

`hopsworks.variables.npm_registry_url` <a class="headerlink" href="#helm.hopsworks.variables.npm_registry_url" title="Permanent link">#</a> { #helm.hopsworks.variables.npm_registry_url }
:   Type `string`, default `""`.
    Registry npm package installs resolve from, applied as `npm config set registry <url>` in the environment build so the built image also resolves from it at runtime. Empty leaves npm on its compiled-in default (registry.npmjs.org).

`hopsworks.variables.oauth_account_status` <a class="headerlink" href="#helm.hopsworks.variables.oauth_account_status" title="Permanent link">#</a> { #helm.hopsworks.variables.oauth_account_status }
:   Type `string`, default `"1"`.

`hopsworks.variables.oauth_group_mapping` <a class="headerlink" href="#helm.hopsworks.variables.oauth_group_mapping" title="Permanent link">#</a> { #helm.hopsworks.variables.oauth_group_mapping }
:   Type `string`, default `""`.

`hopsworks.variables.oauth_group_mapping_enabled` <a class="headerlink" href="#helm.hopsworks.variables.oauth_group_mapping_enabled" title="Permanent link">#</a> { #helm.hopsworks.variables.oauth_group_mapping_enabled }
:   Type `string`, default `"false"`.

`hopsworks.variables.oauth_group_mapping_sync_enabled` <a class="headerlink" href="#helm.hopsworks.variables.oauth_group_mapping_sync_enabled" title="Permanent link">#</a> { #helm.hopsworks.variables.oauth_group_mapping_sync_enabled }
:   Type `string`, default `"false"`.

`hopsworks.variables.oauth_logout_redirect_uri` <a class="headerlink" href="#helm.hopsworks.variables.oauth_logout_redirect_uri" title="Permanent link">#</a> { #helm.hopsworks.variables.oauth_logout_redirect_uri }
:   Type `string`, default `"hopsworks/"`.

`hopsworks.variables.oauth_redirect_uri` <a class="headerlink" href="#helm.hopsworks.variables.oauth_redirect_uri" title="Permanent link">#</a> { #helm.hopsworks.variables.oauth_redirect_uri }
:   Type `string`, default `"hopsworks/callback"`.

`hopsworks.variables.onlinefs_service_thread_number` <a class="headerlink" href="#helm.hopsworks.variables.onlinefs_service_thread_number" title="Permanent link">#</a> { #helm.hopsworks.variables.onlinefs_service_thread_number }
:   Type `string`, default `"10"`.

`hopsworks.variables.onlinefs_user_email` <a class="headerlink" href="#helm.hopsworks.variables.onlinefs_user_email" title="Permanent link">#</a> { #helm.hopsworks.variables.onlinefs_user_email }
:   Type `string`, default `"onlinefs@hopsworks.ai"`.

`hopsworks.variables.onlinefs_user_password` <a class="headerlink" href="#helm.hopsworks.variables.onlinefs_user_password" title="Permanent link">#</a> { #helm.hopsworks.variables.onlinefs_user_password }
:   Type `string`, default `"onlinefspw"`.

`hopsworks.variables.opensearch_default_embedding_index` <a class="headerlink" href="#helm.hopsworks.variables.opensearch_default_embedding_index" title="Permanent link">#</a> { #helm.hopsworks.variables.opensearch_default_embedding_index }
:   Type `string`, default `""`.

`hopsworks.variables.opensearch_index_mapping_limit` <a class="headerlink" href="#helm.hopsworks.variables.opensearch_index_mapping_limit" title="Permanent link">#</a> { #helm.hopsworks.variables.opensearch_index_mapping_limit }
:   Type `string`, default `"1000"`.

`hopsworks.variables.opensearch_num_default_embedding_index` <a class="headerlink" href="#helm.hopsworks.variables.opensearch_num_default_embedding_index" title="Permanent link">#</a> { #helm.hopsworks.variables.opensearch_num_default_embedding_index }
:   Type `string`, default `"1"`.

`hopsworks.variables.payara_dir` <a class="headerlink" href="#helm.hopsworks.variables.payara_dir" title="Permanent link">#</a> { #helm.hopsworks.variables.payara_dir }
:   Type `string`, default `"/opt/payara/appserver/glassfish/domains/domain1"`.

`hopsworks.variables.pki_ca_configuration` <a class="headerlink" href="#helm.hopsworks.variables.pki_ca_configuration" title="Permanent link">#</a> { #helm.hopsworks.variables.pki_ca_configuration }
:   Type `string`.

    ??? note "Default"

        ```yaml
        '{"rootCA":{},"intermediateCA":{},"kubernetesCA":{"subjectAlternativeName":{"dns":["hopsworks0.logicalclocks.com","hops-kubernetes","hops-kubernetes.default","hops-kubernetes.default.svc","hops-kubernetes.default.svc.cluster","hops-kubernetes.default.svc.cluster.local","*.hops-system.svc"],"ip":["10.244.0.1","192.168.30.101","127.0.0.1","10.96.0.10","10.96.0.1"]}}}'
        ```

`hopsworks.variables.platform_intelligence_llm_api_key` <a class="headerlink" href="#helm.hopsworks.variables.platform_intelligence_llm_api_key" title="Permanent link">#</a> { #helm.hopsworks.variables.platform_intelligence_llm_api_key }
:   Type `string`, default `""`.

`hopsworks.variables.platform_intelligence_llm_base_url` <a class="headerlink" href="#helm.hopsworks.variables.platform_intelligence_llm_base_url" title="Permanent link">#</a> { #helm.hopsworks.variables.platform_intelligence_llm_base_url }
:   Type `string`, default `""`.

`hopsworks.variables.platform_intelligence_llm_model` <a class="headerlink" href="#helm.hopsworks.variables.platform_intelligence_llm_model" title="Permanent link">#</a> { #helm.hopsworks.variables.platform_intelligence_llm_model }
:   Type `string`, default `""`.

`hopsworks.variables.preinstalled_python_lib_names` <a class="headerlink" href="#helm.hopsworks.variables.preinstalled_python_lib_names" title="Permanent link">#</a> { #helm.hopsworks.variables.preinstalled_python_lib_names }
:   Type `string`.

    ??? note "Default"

        ```yaml
        pydoop, pyspark, jupyterlab, sparkmagic, hdfscontents, pyjks, hops-apache-beam, pyopenssl
        ```

`hopsworks.variables.project_namespace_labels` <a class="headerlink" href="#helm.hopsworks.variables.project_namespace_labels" title="Permanent link">#</a> { #helm.hopsworks.variables.project_namespace_labels }
:   Type `string`, default `""`.

`hopsworks.variables.project_namespace_network_policy_allowed_namespaces` <a class="headerlink" href="#helm.hopsworks.variables.project_namespace_network_policy_allowed_namespaces" title="Permanent link">#</a> { #helm.hopsworks.variables.project_namespace_network_policy_allowed_namespaces }
:   Type `string`, default `""`.

`hopsworks.variables.project_namespace_network_policy_enabled` <a class="headerlink" href="#helm.hopsworks.variables.project_namespace_network_policy_enabled" title="Permanent link">#</a> { #helm.hopsworks.variables.project_namespace_network_policy_enabled }
:   Type `bool`, default `true`.

`hopsworks.variables.project_namespace_network_policy_reconcile_interval` <a class="headerlink" href="#helm.hopsworks.variables.project_namespace_network_policy_reconcile_interval" title="Permanent link">#</a> { #helm.hopsworks.variables.project_namespace_network_policy_reconcile_interval }
:   Type `string`, default `"1m"`.

`hopsworks.variables.prometheus_port` <a class="headerlink" href="#helm.hopsworks.variables.prometheus_port" title="Permanent link">#</a> { #helm.hopsworks.variables.prometheus_port }
:   Type `string`, default `"9089"`.

`hopsworks.variables.provenance_archive_delay` <a class="headerlink" href="#helm.hopsworks.variables.provenance_archive_delay" title="Permanent link">#</a> { #helm.hopsworks.variables.provenance_archive_delay }
:   Type `string`, default `"86400"`.

`hopsworks.variables.provenance_archive_size` <a class="headerlink" href="#helm.hopsworks.variables.provenance_archive_size" title="Permanent link">#</a> { #helm.hopsworks.variables.provenance_archive_size }
:   Type `string`, default `"10"`.

`hopsworks.variables.provenance_cleaner_period` <a class="headerlink" href="#helm.hopsworks.variables.provenance_cleaner_period" title="Permanent link">#</a> { #helm.hopsworks.variables.provenance_cleaner_period }
:   Type `string`, default `"3600"`.

`hopsworks.variables.provenance_graph_max_size` <a class="headerlink" href="#helm.hopsworks.variables.provenance_graph_max_size" title="Permanent link">#</a> { #helm.hopsworks.variables.provenance_graph_max_size }
:   Type `string`, default `"10000"`.

`hopsworks.variables.provenance_type` <a class="headerlink" href="#helm.hopsworks.variables.provenance_type" title="Permanent link">#</a> { #helm.hopsworks.variables.provenance_type }
:   Type `string`, default `"FULL"`.

`hopsworks.variables.public_https_port` <a class="headerlink" href="#helm.hopsworks.variables.public_https_port" title="Permanent link">#</a> { #helm.hopsworks.variables.public_https_port }
:   Type `string`, default `""`.

`hopsworks.variables.pushgateway_cleaner_batch_size` <a class="headerlink" href="#helm.hopsworks.variables.pushgateway_cleaner_batch_size" title="Permanent link">#</a> { #helm.hopsworks.variables.pushgateway_cleaner_batch_size }
:   Type `string`, default `"100"`.

`hopsworks.variables.pushgateway_group_ttl_minutes` <a class="headerlink" href="#helm.hopsworks.variables.pushgateway_group_ttl_minutes" title="Permanent link">#</a> { #helm.hopsworks.variables.pushgateway_group_ttl_minutes }
:   Type `string`, default `"15"`.

`hopsworks.variables.pushgateway_monitor_interval_ms` <a class="headerlink" href="#helm.hopsworks.variables.pushgateway_monitor_interval_ms" title="Permanent link">#</a> { #helm.hopsworks.variables.pushgateway_monitor_interval_ms }
:   Type `string`, default `"300000"`.

`hopsworks.variables.py4j_archive` <a class="headerlink" href="#helm.hopsworks.variables.py4j_archive" title="Permanent link">#</a> { #helm.hopsworks.variables.py4j_archive }
:   Type `string`, default `""`.

`hopsworks.variables.pypi_indexer_timer_enabled` <a class="headerlink" href="#helm.hopsworks.variables.pypi_indexer_timer_enabled" title="Permanent link">#</a> { #helm.hopsworks.variables.pypi_indexer_timer_enabled }
:   Type `string`, default `"true"`.

`hopsworks.variables.pypi_indexer_timer_interval` <a class="headerlink" href="#helm.hopsworks.variables.pypi_indexer_timer_interval" title="Permanent link">#</a> { #helm.hopsworks.variables.pypi_indexer_timer_interval }
:   Type `string`, default `"1d"`.

`hopsworks.variables.pypi_rest_endpoint` <a class="headerlink" href="#helm.hopsworks.variables.pypi_rest_endpoint" title="Permanent link">#</a> { #helm.hopsworks.variables.pypi_rest_endpoint }
:   Type `string`, default `"https://pypi.org/pypi/{package}/json"`.

`hopsworks.variables.pypi_simple_endpoint` <a class="headerlink" href="#helm.hopsworks.variables.pypi_simple_endpoint" title="Permanent link">#</a> { #helm.hopsworks.variables.pypi_simple_endpoint }
:   Type `string`, default `"https://pypi.org/simple/"`.

`hopsworks.variables.python_job_cores` <a class="headerlink" href="#helm.hopsworks.variables.python_job_cores" title="Permanent link">#</a> { #helm.hopsworks.variables.python_job_cores }
:   Type `string`, default `"1.0"`.

`hopsworks.variables.python_job_gpus` <a class="headerlink" href="#helm.hopsworks.variables.python_job_gpus" title="Permanent link">#</a> { #helm.hopsworks.variables.python_job_gpus }
:   Type `string`, default `"0"`.

`hopsworks.variables.python_job_kube_waiting_timeout_ms` <a class="headerlink" href="#helm.hopsworks.variables.python_job_kube_waiting_timeout_ms" title="Permanent link">#</a> { #helm.hopsworks.variables.python_job_kube_waiting_timeout_ms }
:   Type `string`, default `"300000"`.

`hopsworks.variables.python_job_memory` <a class="headerlink" href="#helm.hopsworks.variables.python_job_memory" title="Permanent link">#</a> { #helm.hopsworks.variables.python_job_memory }
:   Type `string`, default `"2048"`.

`hopsworks.variables.python_library_updates_monitor_interval` <a class="headerlink" href="#helm.hopsworks.variables.python_library_updates_monitor_interval" title="Permanent link">#</a> { #helm.hopsworks.variables.python_library_updates_monitor_interval }
:   Type `string`, default `"1d"`.

`hopsworks.variables.python_pod_kill_grace_period_seconds` <a class="headerlink" href="#helm.hopsworks.variables.python_pod_kill_grace_period_seconds" title="Permanent link">#</a> { #helm.hopsworks.variables.python_pod_kill_grace_period_seconds }
:   Type `string`, default `"60"`.

`hopsworks.variables.pythonapp_cores` <a class="headerlink" href="#helm.hopsworks.variables.pythonapp_cores" title="Permanent link">#</a> { #helm.hopsworks.variables.pythonapp_cores }
:   Type `string`, default `"1.0"`.

`hopsworks.variables.pythonapp_gpus` <a class="headerlink" href="#helm.hopsworks.variables.pythonapp_gpus" title="Permanent link">#</a> { #helm.hopsworks.variables.pythonapp_gpus }
:   Type `string`, default `"0"`.

`hopsworks.variables.pythonapp_memory` <a class="headerlink" href="#helm.hopsworks.variables.pythonapp_memory" title="Permanent link">#</a> { #helm.hopsworks.variables.pythonapp_memory }
:   Type `string`, default `"2048"`.

`hopsworks.variables.quotas_featuregroups_online_disabled` <a class="headerlink" href="#helm.hopsworks.variables.quotas_featuregroups_online_disabled" title="Permanent link">#</a> { #helm.hopsworks.variables.quotas_featuregroups_online_disabled }
:   Type `string`, default `"-1"`.

`hopsworks.variables.quotas_featuregroups_online_enabled` <a class="headerlink" href="#helm.hopsworks.variables.quotas_featuregroups_online_enabled" title="Permanent link">#</a> { #helm.hopsworks.variables.quotas_featuregroups_online_enabled }
:   Type `string`, default `"-1"`.

`hopsworks.variables.quotas_max_parallel_executions` <a class="headerlink" href="#helm.hopsworks.variables.quotas_max_parallel_executions" title="Permanent link">#</a> { #helm.hopsworks.variables.quotas_max_parallel_executions }
:   Type `string`, default `"-1"`.

`hopsworks.variables.quotas_model_deployments_running` <a class="headerlink" href="#helm.hopsworks.variables.quotas_model_deployments_running" title="Permanent link">#</a> { #helm.hopsworks.variables.quotas_model_deployments_running }
:   Type `string`, default `"-1"`.

`hopsworks.variables.quotas_model_deployments_total` <a class="headerlink" href="#helm.hopsworks.variables.quotas_model_deployments_total" title="Permanent link">#</a> { #helm.hopsworks.variables.quotas_model_deployments_total }
:   Type `string`, default `"-1"`.

`hopsworks.variables.quotas_training_datasets` <a class="headerlink" href="#helm.hopsworks.variables.quotas_training_datasets" title="Permanent link">#</a> { #helm.hopsworks.variables.quotas_training_datasets }
:   Type `string`, default `"-1"`.

`hopsworks.variables.ray_cluster_max_worker_replicas` <a class="headerlink" href="#helm.hopsworks.variables.ray_cluster_max_worker_replicas" title="Permanent link">#</a> { #helm.hopsworks.variables.ray_cluster_max_worker_replicas }
:   Type `string`, default `"20"`.

`hopsworks.variables.ray_cluster_shutdown_after_completion` <a class="headerlink" href="#helm.hopsworks.variables.ray_cluster_shutdown_after_completion" title="Permanent link">#</a> { #helm.hopsworks.variables.ray_cluster_shutdown_after_completion }
:   Type `string`, default `"true"`.

`hopsworks.variables.ray_cluster_start_wait_time_seconds` <a class="headerlink" href="#helm.hopsworks.variables.ray_cluster_start_wait_time_seconds" title="Permanent link">#</a> { #helm.hopsworks.variables.ray_cluster_start_wait_time_seconds }
:   Type `string`, default `"360"`.

`hopsworks.variables.ray_cluster_termination_grace_period_seconds` <a class="headerlink" href="#helm.hopsworks.variables.ray_cluster_termination_grace_period_seconds" title="Permanent link">#</a> { #helm.hopsworks.variables.ray_cluster_termination_grace_period_seconds }
:   Type `string`, default `"10"`.

`hopsworks.variables.ray_enabled` <a class="headerlink" href="#helm.hopsworks.variables.ray_enabled" title="Permanent link">#</a> { #helm.hopsworks.variables.ray_enabled }
:   Type `bool`, default `false`.
    ray_enabled indicates if hopsworks configurations for ray should be applied

`hopsworks.variables.ray_job_driver_cores` <a class="headerlink" href="#helm.hopsworks.variables.ray_job_driver_cores" title="Permanent link">#</a> { #helm.hopsworks.variables.ray_job_driver_cores }
:   Type `string`, default `"1.0"`.

`hopsworks.variables.ray_job_driver_gpus` <a class="headerlink" href="#helm.hopsworks.variables.ray_job_driver_gpus" title="Permanent link">#</a> { #helm.hopsworks.variables.ray_job_driver_gpus }
:   Type `string`, default `"0"`.

`hopsworks.variables.ray_job_driver_memory` <a class="headerlink" href="#helm.hopsworks.variables.ray_job_driver_memory" title="Permanent link">#</a> { #helm.hopsworks.variables.ray_job_driver_memory }
:   Type `string`, default `"4096"`.

`hopsworks.variables.ray_job_pod_kill_grace_period_seconds` <a class="headerlink" href="#helm.hopsworks.variables.ray_job_pod_kill_grace_period_seconds" title="Permanent link">#</a> { #helm.hopsworks.variables.ray_job_pod_kill_grace_period_seconds }
:   Type `string`, default `"300"`.

`hopsworks.variables.ray_job_worker_cores` <a class="headerlink" href="#helm.hopsworks.variables.ray_job_worker_cores" title="Permanent link">#</a> { #helm.hopsworks.variables.ray_job_worker_cores }
:   Type `string`, default `"1.0"`.

`hopsworks.variables.ray_job_worker_gpus` <a class="headerlink" href="#helm.hopsworks.variables.ray_job_worker_gpus" title="Permanent link">#</a> { #helm.hopsworks.variables.ray_job_worker_gpus }
:   Type `string`, default `"0"`.

`hopsworks.variables.ray_job_worker_memory` <a class="headerlink" href="#helm.hopsworks.variables.ray_job_worker_memory" title="Permanent link">#</a> { #helm.hopsworks.variables.ray_job_worker_memory }
:   Type `string`, default `"4096"`.

`hopsworks.variables.ray_materialization_dir` <a class="headerlink" href="#helm.hopsworks.variables.ray_materialization_dir" title="Permanent link">#</a> { #helm.hopsworks.variables.ray_materialization_dir }
:   Type `string`, default `"/srv/hops/ray/job"`.

`hopsworks.variables.ray_version` <a class="headerlink" href="#helm.hopsworks.variables.ray_version" title="Permanent link">#</a> { #helm.hopsworks.variables.ray_version }
:   Type `string`, default `"2.58.0"`.

`hopsworks.variables.recovery_path` <a class="headerlink" href="#helm.hopsworks.variables.recovery_path" title="Permanent link">#</a> { #helm.hopsworks.variables.recovery_path }
:   Type `string`, default `""`.

`hopsworks.variables.reject_remote_user_no_group` <a class="headerlink" href="#helm.hopsworks.variables.reject_remote_user_no_group" title="Permanent link">#</a> { #helm.hopsworks.variables.reject_remote_user_no_group }
:   Type `string`, default `"false"`.

`hopsworks.variables.remote_auth_need_consent` <a class="headerlink" href="#helm.hopsworks.variables.remote_auth_need_consent" title="Permanent link">#</a> { #helm.hopsworks.variables.remote_auth_need_consent }
:   Type `string`, default `"true"`.

`hopsworks.variables.requests_verify` <a class="headerlink" href="#helm.hopsworks.variables.requests_verify" title="Permanent link">#</a> { #helm.hopsworks.variables.requests_verify }
:   Type `string`, default `"true"`.

`hopsworks.variables.reserved_project_names` <a class="headerlink" href="#helm.hopsworks.variables.reserved_project_names" title="Permanent link">#</a> { #helm.hopsworks.variables.reserved_project_names }
:   Type `string`.

    ??? note "Default"

        ```yaml
        hopsworks,information_schema,airflow,glassfish_timers,grafana,hops,metastore,mysql,ndbinfo,performance_schema,sqoop,sys,base,python37,python38,python39,python310,filebeat,airflow,git,onlinefs,sklearnserver,rondb_replication,default,kube-system,kube-public,kube-node-lease,kube_system,kube_public,kube_node_lease
        ```

`hopsworks.variables.rmyarn_user` <a class="headerlink" href="#helm.hopsworks.variables.rmyarn_user" title="Permanent link">#</a> { #helm.hopsworks.variables.rmyarn_user }
:   Type `string`, default `"rmyarn"`.

`hopsworks.variables.rondb_quotas` <a class="headerlink" href="#helm.hopsworks.variables.rondb_quotas" title="Permanent link">#</a> { #helm.hopsworks.variables.rondb_quotas }
:   Type `string`, default `""`.
    RONDB quotas in csv format. e.g `rate-per-sec=1000,max-transaction-size=100`. Refer to <https://docs.rondb.com/rondb_rate_limits_quotas/> for the full list of arguments and their definitions.

`hopsworks.variables.rondb_usage_cache_ttl_seconds` <a class="headerlink" href="#helm.hopsworks.variables.rondb_usage_cache_ttl_seconds" title="Permanent link">#</a> { #helm.hopsworks.variables.rondb_usage_cache_ttl_seconds }
:   Type `string`, default `"60"`.
    How often (seconds) the cached RonDB per-database memory usage snapshot is refreshed. The backing ndbinfo scan costs the same for one database as for all, so one snapshot serves every project.

`hopsworks.variables.rondb_usage_query_timeout_seconds` <a class="headerlink" href="#helm.hopsworks.variables.rondb_usage_query_timeout_seconds" title="Permanent link">#</a> { #helm.hopsworks.variables.rondb_usage_query_timeout_seconds }
:   Type `string`, default `"10"`.
    Query timeout (seconds) for the ndbinfo memory usage scan. Scan duration grows with the cluster's table count; raise this on large clusters if usage stops showing in the project quotas UI.

`hopsworks.variables.saas_entry_point_url` <a class="headerlink" href="#helm.hopsworks.variables.saas_entry_point_url" title="Permanent link">#</a> { #helm.hopsworks.variables.saas_entry_point_url }
:   Type `string`, default `""`.
    SAAS bridge: auth entry-point URL the frontend redirects to when management_mode is SAAS_MANAGED. Ignored in STANDALONE.

`hopsworks.variables.scikit_learn_version` <a class="headerlink" href="#helm.hopsworks.variables.scikit_learn_version" title="Permanent link">#</a> { #helm.hopsworks.variables.scikit_learn_version }
:   Type `string`, default `"1.3.2"`.

`hopsworks.variables.service_jwt_exp_leeway_sec` <a class="headerlink" href="#helm.hopsworks.variables.service_jwt_exp_leeway_sec" title="Permanent link">#</a> { #helm.hopsworks.variables.service_jwt_exp_leeway_sec }
:   Type `string`, default `"172800000"`.

`hopsworks.variables.service_jwt_lifetime_ms` <a class="headerlink" href="#helm.hopsworks.variables.service_jwt_lifetime_ms" title="Permanent link">#</a> { #helm.hopsworks.variables.service_jwt_lifetime_ms }
:   Type `string`, default `"604800000"`.

`hopsworks.variables.service_key_rotation_enabled` <a class="headerlink" href="#helm.hopsworks.variables.service_key_rotation_enabled" title="Permanent link">#</a> { #helm.hopsworks.variables.service_key_rotation_enabled }
:   Type `string`, default `"false"`.

`hopsworks.variables.service_key_rotation_interval` <a class="headerlink" href="#helm.hopsworks.variables.service_key_rotation_interval" title="Permanent link">#</a> { #helm.hopsworks.variables.service_key_rotation_interval }
:   Type `string`, default `"2d"`.

`hopsworks.variables.serving_allow_stop_after_seconds` <a class="headerlink" href="#helm.hopsworks.variables.serving_allow_stop_after_seconds" title="Permanent link">#</a> { #helm.hopsworks.variables.serving_allow_stop_after_seconds }
:   Type `string`, default `"30"`.

`hopsworks.variables.serving_connection_pool_size` <a class="headerlink" href="#helm.hopsworks.variables.serving_connection_pool_size" title="Permanent link">#</a> { #helm.hopsworks.variables.serving_connection_pool_size }
:   Type `string`, default `"40"`.

`hopsworks.variables.serving_feature_log_materialization_cron` <a class="headerlink" href="#helm.hopsworks.variables.serving_feature_log_materialization_cron" title="Permanent link">#</a> { #helm.hopsworks.variables.serving_feature_log_materialization_cron }
:   Type `string`, default `"0 0 0 * * ? *"`.

`hopsworks.variables.serving_feature_log_materialization_row_limit` <a class="headerlink" href="#helm.hopsworks.variables.serving_feature_log_materialization_row_limit" title="Permanent link">#</a> { #helm.hopsworks.variables.serving_feature_log_materialization_row_limit }
:   Type `string`, default `"50000000"`.

`hopsworks.variables.serving_feature_log_online_ttl_hours` <a class="headerlink" href="#helm.hopsworks.variables.serving_feature_log_online_ttl_hours" title="Permanent link">#</a> { #helm.hopsworks.variables.serving_feature_log_online_ttl_hours }
:   Type `string`, default `"30"`.

`hopsworks.variables.serving_feature_logger_batch_bytes` <a class="headerlink" href="#helm.hopsworks.variables.serving_feature_logger_batch_bytes" title="Permanent link">#</a> { #helm.hopsworks.variables.serving_feature_logger_batch_bytes }
:   Type `string`, default `"1048576"`.

`hopsworks.variables.serving_feature_logger_batch_seconds` <a class="headerlink" href="#helm.hopsworks.variables.serving_feature_logger_batch_seconds" title="Permanent link">#</a> { #helm.hopsworks.variables.serving_feature_logger_batch_seconds }
:   Type `string`, default `"5"`.

`hopsworks.variables.serving_feature_logger_client_pool_size` <a class="headerlink" href="#helm.hopsworks.variables.serving_feature_logger_client_pool_size" title="Permanent link">#</a> { #helm.hopsworks.variables.serving_feature_logger_client_pool_size }
:   Type `string`, default `"3"`.

`hopsworks.variables.serving_feature_logger_client_req_timeout_seconds` <a class="headerlink" href="#helm.hopsworks.variables.serving_feature_logger_client_req_timeout_seconds" title="Permanent link">#</a> { #helm.hopsworks.variables.serving_feature_logger_client_req_timeout_seconds }
:   Type `string`, default `"3"`.

`hopsworks.variables.serving_feature_logger_flush_bytes` <a class="headerlink" href="#helm.hopsworks.variables.serving_feature_logger_flush_bytes" title="Permanent link">#</a> { #helm.hopsworks.variables.serving_feature_logger_flush_bytes }
:   Type `string`, default `"1048576"`.

`hopsworks.variables.serving_feature_logger_flush_interval_seconds` <a class="headerlink" href="#helm.hopsworks.variables.serving_feature_logger_flush_interval_seconds" title="Permanent link">#</a> { #helm.hopsworks.variables.serving_feature_logger_flush_interval_seconds }
:   Type `string`, default `"300"`.

`hopsworks.variables.serving_feature_logger_max_buffer_bytes` <a class="headerlink" href="#helm.hopsworks.variables.serving_feature_logger_max_buffer_bytes" title="Permanent link">#</a> { #helm.hopsworks.variables.serving_feature_logger_max_buffer_bytes }
:   Type `string`, default `"67108864"`.

`hopsworks.variables.serving_feature_logger_max_event_bytes` <a class="headerlink" href="#helm.hopsworks.variables.serving_feature_logger_max_event_bytes" title="Permanent link">#</a> { #helm.hopsworks.variables.serving_feature_logger_max_event_bytes }
:   Type `string`, default `"8388608"`.

`hopsworks.variables.serving_feature_logger_max_event_rows` <a class="headerlink" href="#helm.hopsworks.variables.serving_feature_logger_max_event_rows" title="Permanent link">#</a> { #helm.hopsworks.variables.serving_feature_logger_max_event_rows }
:   Type `string`, default `"512"`.

`hopsworks.variables.serving_feature_logger_queue_size` <a class="headerlink" href="#helm.hopsworks.variables.serving_feature_logger_queue_size" title="Permanent link">#</a> { #helm.hopsworks.variables.serving_feature_logger_queue_size }
:   Type `string`, default `"1000"`.

`hopsworks.variables.serving_feature_logger_shutdown_seconds` <a class="headerlink" href="#helm.hopsworks.variables.serving_feature_logger_shutdown_seconds" title="Permanent link">#</a> { #helm.hopsworks.variables.serving_feature_logger_shutdown_seconds }
:   Type `string`, default `"20"`.

`hopsworks.variables.serving_feature_logging_transport` <a class="headerlink" href="#helm.hopsworks.variables.serving_feature_logging_transport" title="Permanent link">#</a> { #helm.hopsworks.variables.serving_feature_logging_transport }
:   Type `string`, default `"realtime"`.

`hopsworks.variables.serving_max_route_connections` <a class="headerlink" href="#helm.hopsworks.variables.serving_max_route_connections" title="Permanent link">#</a> { #helm.hopsworks.variables.serving_max_route_connections }
:   Type `string`, default `"10"`.

`hopsworks.variables.serving_redeploy_not_found_after_seconds` <a class="headerlink" href="#helm.hopsworks.variables.serving_redeploy_not_found_after_seconds" title="Permanent link">#</a> { #helm.hopsworks.variables.serving_redeploy_not_found_after_seconds }
:   Type `string`, default `"120"`.

`hopsworks.variables.serving_state_manager_batch_size` <a class="headerlink" href="#helm.hopsworks.variables.serving_state_manager_batch_size" title="Permanent link">#</a> { #helm.hopsworks.variables.serving_state_manager_batch_size }
:   Type `string`, default `"25"`.

`hopsworks.variables.serving_state_manager_enabled` <a class="headerlink" href="#helm.hopsworks.variables.serving_state_manager_enabled" title="Permanent link">#</a> { #helm.hopsworks.variables.serving_state_manager_enabled }
:   Type `string`, default `"true"`.

`hopsworks.variables.serving_state_manager_interval_ms` <a class="headerlink" href="#helm.hopsworks.variables.serving_state_manager_interval_ms" title="Permanent link">#</a> { #helm.hopsworks.variables.serving_state_manager_interval_ms }
:   Type `string`, default `"300000"`.

`hopsworks.variables.spark_dir` <a class="headerlink" href="#helm.hopsworks.variables.spark_dir" title="Permanent link">#</a> { #helm.hopsworks.variables.spark_dir }
:   Type `string`, default `"/srv/hops/spark"`.

`hopsworks.variables.spark_executor_min_memory` <a class="headerlink" href="#helm.hopsworks.variables.spark_executor_min_memory" title="Permanent link">#</a> { #helm.hopsworks.variables.spark_executor_min_memory }
:   Type `string`, default `"1024"`.

`hopsworks.variables.spark_hops_utils_dir` <a class="headerlink" href="#helm.hopsworks.variables.spark_hops_utils_dir" title="Permanent link">#</a> { #helm.hopsworks.variables.spark_hops_utils_dir }
:   Type `string`, default `"/srv/hops/artifacts"`.

`hopsworks.variables.spark_job_driver_cores` <a class="headerlink" href="#helm.hopsworks.variables.spark_job_driver_cores" title="Permanent link">#</a> { #helm.hopsworks.variables.spark_job_driver_cores }
:   Type `string`, default `"1.0"`.

`hopsworks.variables.spark_job_driver_memory` <a class="headerlink" href="#helm.hopsworks.variables.spark_job_driver_memory" title="Permanent link">#</a> { #helm.hopsworks.variables.spark_job_driver_memory }
:   Type `string`, default `"2048"`.

`hopsworks.variables.spark_job_executor_cores` <a class="headerlink" href="#helm.hopsworks.variables.spark_job_executor_cores" title="Permanent link">#</a> { #helm.hopsworks.variables.spark_job_executor_cores }
:   Type `string`, default `"1.0"`.

`hopsworks.variables.spark_job_executor_memory` <a class="headerlink" href="#helm.hopsworks.variables.spark_job_executor_memory" title="Permanent link">#</a> { #helm.hopsworks.variables.spark_job_executor_memory }
:   Type `string`, default `"4096"`.

`hopsworks.variables.spark_launcher_sa_annotations` <a class="headerlink" href="#helm.hopsworks.variables.spark_launcher_sa_annotations" title="Permanent link">#</a> { #helm.hopsworks.variables.spark_launcher_sa_annotations }
:   Type `string`, default `""`.

`hopsworks.variables.spark_pod_kill_grace_period_seconds` <a class="headerlink" href="#helm.hopsworks.variables.spark_pod_kill_grace_period_seconds" title="Permanent link">#</a> { #helm.hopsworks.variables.spark_pod_kill_grace_period_seconds }
:   Type `string`, default `"1200"`.

`hopsworks.variables.spark_remove_job_when_completed` <a class="headerlink" href="#helm.hopsworks.variables.spark_remove_job_when_completed" title="Permanent link">#</a> { #helm.hopsworks.variables.spark_remove_job_when_completed }
:   Type `string`, default `"true"`.

`hopsworks.variables.spark_ui_logs_offset` <a class="headerlink" href="#helm.hopsworks.variables.spark_ui_logs_offset" title="Permanent link">#</a> { #helm.hopsworks.variables.spark_ui_logs_offset }
:   Type `string`, default `"512000"`.

`hopsworks.variables.spark_user` <a class="headerlink" href="#helm.hopsworks.variables.spark_user" title="Permanent link">#</a> { #helm.hopsworks.variables.spark_user }
:   Type `string`, default `"spark"`.

`hopsworks.variables.spark_version` <a class="headerlink" href="#helm.hopsworks.variables.spark_version" title="Permanent link">#</a> { #helm.hopsworks.variables.spark_version }
:   Type `string`, default `"4.1.3.0"`.

`hopsworks.variables.srvmanager_password` <a class="headerlink" href="#helm.hopsworks.variables.srvmanager_password" title="Permanent link">#</a> { #helm.hopsworks.variables.srvmanager_password }
:   Type `string`, default `"srvmanagerpwd"`.

`hopsworks.variables.staging_dir` <a class="headerlink" href="#helm.hopsworks.variables.staging_dir" title="Permanent link">#</a> { #helm.hopsworks.variables.staging_dir }
:   Type `string`, default `"/srv/hops/staging"`.

`hopsworks.variables.statistics_cleaner_batch_size` <a class="headerlink" href="#helm.hopsworks.variables.statistics_cleaner_batch_size" title="Permanent link">#</a> { #helm.hopsworks.variables.statistics_cleaner_batch_size }
:   Type `string`, default `"1000"`.

`hopsworks.variables.statistics_cleaner_interval_ms` <a class="headerlink" href="#helm.hopsworks.variables.statistics_cleaner_interval_ms" title="Permanent link">#</a> { #helm.hopsworks.variables.statistics_cleaner_interval_ms }
:   Type `string`, default `"900000"`.

`hopsworks.variables.streamlit_sharing` <a class="headerlink" href="#helm.hopsworks.variables.streamlit_sharing" title="Permanent link">#</a> { #helm.hopsworks.variables.streamlit_sharing }
:   Type `bool`, default `false`.

`hopsworks.variables.sudoers_dir` <a class="headerlink" href="#helm.hopsworks.variables.sudoers_dir" title="Permanent link">#</a> { #helm.hopsworks.variables.sudoers_dir }
:   Type `string`, default `"/srv/hops/sbin"`.

`hopsworks.variables.superset_admin_roles` <a class="headerlink" href="#helm.hopsworks.variables.superset_admin_roles" title="Permanent link">#</a> { #helm.hopsworks.variables.superset_admin_roles }
:   Type `string`, default `"Admin"`.

`hopsworks.variables.superset_proxy_connect_timeout_ms` <a class="headerlink" href="#helm.hopsworks.variables.superset_proxy_connect_timeout_ms" title="Permanent link">#</a> { #helm.hopsworks.variables.superset_proxy_connect_timeout_ms }
:   Type `string`, default `"10000"`.

`hopsworks.variables.superset_proxy_connection_request_timeout_ms` <a class="headerlink" href="#helm.hopsworks.variables.superset_proxy_connection_request_timeout_ms" title="Permanent link">#</a> { #helm.hopsworks.variables.superset_proxy_connection_request_timeout_ms }
:   Type `string`, default `"10000"`.

`hopsworks.variables.superset_proxy_max_connections` <a class="headerlink" href="#helm.hopsworks.variables.superset_proxy_max_connections" title="Permanent link">#</a> { #helm.hopsworks.variables.superset_proxy_max_connections }
:   Type `string`, default `"50"`.

`hopsworks.variables.superset_proxy_read_timeout_ms` <a class="headerlink" href="#helm.hopsworks.variables.superset_proxy_read_timeout_ms" title="Permanent link">#</a> { #helm.hopsworks.variables.superset_proxy_read_timeout_ms }
:   Type `string`, default `"180000"`.

`hopsworks.variables.superset_user_roles` <a class="headerlink" href="#helm.hopsworks.variables.superset_user_roles" title="Permanent link">#</a> { #helm.hopsworks.variables.superset_user_roles }
:   Type `string`, default `"Gamma,sql_lab,Dataset"`.

`hopsworks.variables.support_email_addr` <a class="headerlink" href="#helm.hopsworks.variables.support_email_addr" title="Permanent link">#</a> { #helm.hopsworks.variables.support_email_addr }
:   Type `string`, default `"support@hopsworks.ai"`.

`hopsworks.variables.tag_history_archive_max_events` <a class="headerlink" href="#helm.hopsworks.variables.tag_history_archive_max_events" title="Permanent link">#</a> { #helm.hopsworks.variables.tag_history_archive_max_events }
:   Type `string`, default `"20000"`.
    Largest number of tag history events an archive flip will write, one per tag key of every existing attachment. Turning archiving on or off writes them in a single transaction, which cannot be split without losing the baseline it exists to record, so the work is bounded by NDB's MaxNoOfConcurrentOperations and the request timeout rather than by paging. Counted in events because an attachment with several keys is several rows; a limit on attachments alone did not bound the work. Above this the call is refused with the count and this limit instead of rolling back with no readable cause. Raise it alongside MaxNoOfConcurrentOperations.

`hopsworks.variables.tag_history_cleaner_batch_size` <a class="headerlink" href="#helm.hopsworks.variables.tag_history_cleaner_batch_size" title="Permanent link">#</a> { #helm.hopsworks.variables.tag_history_cleaner_batch_size }
:   Type `string`, default `"1000"`.
    Rows deleted per transaction by the tag history retention sweep. Bounded so a large sweep is a series of short transactions rather than one that runs into NDB's MaxNoOfConcurrentOperations.

`hopsworks.variables.tag_history_cleaner_interval_ms` <a class="headerlink" href="#helm.hopsworks.variables.tag_history_cleaner_interval_ms" title="Permanent link">#</a> { #helm.hopsworks.variables.tag_history_cleaner_interval_ms }
:   Type `string`, default `"86400000"`.
    How often the tag history retention sweep runs, in milliseconds. Values below 60000 are refused and fall back to 24h.

`hopsworks.variables.tag_history_retention_days` <a class="headerlink" href="#helm.hopsworks.variables.tag_history_retention_days" title="Permanent link">#</a> { #helm.hopsworks.variables.tag_history_retention_days }
:   Type `string`, default `"0"`.
    How many days of tag history to keep. tag_history is append-only and nothing else bounds it: clearing a schema's archive flag stops new rows but deletes none, so without retention the only way to reclaim the space is by hand. "0" keeps everything, which is the default because deleting analytics history as a side effect of an upgrade would surprise everyone reporting on it. Set a number of days to bound it.

`hopsworks.variables.tensorboard_max_last_accessed` <a class="headerlink" href="#helm.hopsworks.variables.tensorboard_max_last_accessed" title="Permanent link">#</a> { #helm.hopsworks.variables.tensorboard_max_last_accessed }
:   Type `string`, default `"1140000"`.

`hopsworks.variables.tensorboard_max_reload_threads` <a class="headerlink" href="#helm.hopsworks.variables.tensorboard_max_reload_threads" title="Permanent link">#</a> { #helm.hopsworks.variables.tensorboard_max_reload_threads }
:   Type `string`, default `"1"`.

`hopsworks.variables.tensorflow_version` <a class="headerlink" href="#helm.hopsworks.variables.tensorflow_version" title="Permanent link">#</a> { #helm.hopsworks.variables.tensorflow_version }
:   Type `string`, default `"2.20.0"`.

`hopsworks.variables.testconnector_image_version` <a class="headerlink" href="#helm.hopsworks.variables.testconnector_image_version" title="Permanent link">#</a> { #helm.hopsworks.variables.testconnector_image_version }
:   Type `string`, default `"1.0"`.

`hopsworks.variables.tf_spark_connector_version` <a class="headerlink" href="#helm.hopsworks.variables.tf_spark_connector_version" title="Permanent link">#</a> { #helm.hopsworks.variables.tf_spark_connector_version }
:   Type `string`, default `""`.

`hopsworks.variables.trino_default_catalog` <a class="headerlink" href="#helm.hopsworks.variables.trino_default_catalog" title="Permanent link">#</a> { #helm.hopsworks.variables.trino_default_catalog }
:   Type `string`, default `"delta"`.

`hopsworks.variables.trino_events_cleaner_batch_size` <a class="headerlink" href="#helm.hopsworks.variables.trino_events_cleaner_batch_size" title="Permanent link">#</a> { #helm.hopsworks.variables.trino_events_cleaner_batch_size }
:   Type `string`, default `"1000"`.

`hopsworks.variables.trino_events_delete_after_days` <a class="headerlink" href="#helm.hopsworks.variables.trino_events_delete_after_days" title="Permanent link">#</a> { #helm.hopsworks.variables.trino_events_delete_after_days }
:   Type `string`, default `"61"`.

`hopsworks.variables.twofactor_auth` <a class="headerlink" href="#helm.hopsworks.variables.twofactor_auth" title="Permanent link">#</a> { #helm.hopsworks.variables.twofactor_auth }
:   Type `string`, default `"false"`.

`hopsworks.variables.twofactor_excluded_groups` <a class="headerlink" href="#helm.hopsworks.variables.twofactor_excluded_groups" title="Permanent link">#</a> { #helm.hopsworks.variables.twofactor_excluded_groups }
:   Type `string`, default `"AGENT;CLUSTER_AGENT"`.

`hopsworks.variables.unix_usernames_conf` <a class="headerlink" href="#helm.hopsworks.variables.unix_usernames_conf" title="Permanent link">#</a> { #helm.hopsworks.variables.unix_usernames_conf }
:   Type `string`.

    ??? note "Default"

        ```yaml
        '{\"glassfish\":\"glassfish\",\"hdfs\":\"hdfs\",\"rmyarn\":\"rmyarn\",\"yarn\":\"yarn\",\"hive\":\"hive\",\"livy\":\"livy\",\"flink\":\"flink\",\"consul\":\"consul\",\"hopsmon\":\"hopsmon\",\"zookeeper\":\"zookeeper\",\"onlinefs\":\"onlinefs\",\"elastic\":\"elastic\",\"kagent\":\"kagent\",\"mysql\":\"mysql\",\"airflow\":\"airflow\"}'
        ```

`hopsworks.variables.upload_chunk_size` <a class="headerlink" href="#helm.hopsworks.variables.upload_chunk_size" title="Permanent link">#</a> { #helm.hopsworks.variables.upload_chunk_size }
:   Type `string`, default `"10485760"`.

`hopsworks.variables.upload_policy` <a class="headerlink" href="#helm.hopsworks.variables.upload_policy" title="Permanent link">#</a> { #helm.hopsworks.variables.upload_policy }
:   Type `string`, default `"enabled"`.
    Who may upload files into the cluster. `enabled` allows any user with write access to the destination dataset, `admins_only` restricts uploads to members of `HOPS_ADMIN`, `disabled` blocks everyone including administrators. Applies to the web UI and to clients such as the Python SDK. Unrecognised values fall back to `enabled`. Note that this governs uploading new files only: operations on files already in the cluster filesystem, such as installing a python library from an existing path, are unaffected.

`hopsworks.variables.user_cert_valid_days` <a class="headerlink" href="#helm.hopsworks.variables.user_cert_valid_days" title="Permanent link">#</a> { #helm.hopsworks.variables.user_cert_valid_days }
:   Type `string`, default `"12"`.

`hopsworks.variables.verification_path` <a class="headerlink" href="#helm.hopsworks.variables.verification_path" title="Permanent link">#</a> { #helm.hopsworks.variables.verification_path }
:   Type `string`, default `"hopsworks-api/api/auth/verify"`.

`hopsworks.variables.yarn_default_payment_type` <a class="headerlink" href="#helm.hopsworks.variables.yarn_default_payment_type" title="Permanent link">#</a> { #helm.hopsworks.variables.yarn_default_payment_type }
:   Type `string`, default `"NOLIMIT"`.

`hopsworks.variables.yarn_default_quota` <a class="headerlink" href="#helm.hopsworks.variables.yarn_default_quota" title="Permanent link">#</a> { #helm.hopsworks.variables.yarn_default_quota }
:   Type `string`, default `"60000000"`.

`hopsworks.variables.yarn_user` <a class="headerlink" href="#helm.hopsworks.variables.yarn_user" title="Permanent link">#</a> { #helm.hopsworks.variables.yarn_user }
:   Type `string`, default `"yarn"`.

`hopsworks.variables.zookeeper_version` <a class="headerlink" href="#helm.hopsworks.variables.zookeeper_version" title="Permanent link">#</a> { #helm.hopsworks.variables.zookeeper_version }
:   Type `string`, default `"3.7.1"`.

`hopsworks.variables.mount_hopsfs_in_python_job` <span class="hops-values-deprecated">Deprecated</span> <a class="headerlink" href="#helm.hopsworks.variables.mount_hopsfs_in_python_job" title="Permanent link">#</a> { #helm.hopsworks.variables.mount_hopsfs_in_python_job }
:   Type `bool`, default `true`.
    Deprecated. Python Apps always mount HopsFS; this remains only for legacy Python jobs.

</div>

## velero { #helm-values-hopsworks-velero }

??? example "Defaults as YAML"

    ```yaml
    hopsworks:
      velero:
        backup:
          dynamicNamespaceFilter:
            enabled: true
            schedule: '@hourly'
          enabled: null
          excludedNamespaces:
          - kube-system
          - kube-public
          - kube-node-lease
          - argocd
          - default
          - ingress-nginx
          includedNamespaces: []
          mainScheduleName: k8s-backups-main
          schedule: null
          storageLocation:
            create: true
            name: hopsworks-bsl
            s3ForcePathStyle: null
            storagePrefix: k8s_backup
          ttl: null
          usersScheduleName: k8s-backups-users-resources
        deploymentName: velero
        enforcePrerequisiteCheck: true
        namespace: velero
        restore:
          mainScheduleBackupId: null
          usersScheduleBackupId: null
        ttlSecondsAfterFinished: null
    ```

<div class="hops-values" markdown>

`hopsworks.velero.backup` <a class="headerlink" href="#helm.hopsworks.velero.backup" title="Permanent link">#</a> { #helm.hopsworks.velero.backup }
:   Type `object`.
    backup configuration

    ??? note "Default"

        ```yaml
        dynamicNamespaceFilter:
          enabled: true
          schedule: '@hourly'
        enabled: null
        excludedNamespaces:
        - kube-system
        - kube-public
        - kube-node-lease
        - argocd
        - default
        - ingress-nginx
        includedNamespaces: []
        mainScheduleName: k8s-backups-main
        schedule: null
        storageLocation:
          create: true
          name: hopsworks-bsl
          s3ForcePathStyle: null
          storagePrefix: k8s_backup
        ttl: null
        usersScheduleName: k8s-backups-users-resources
        ```

`hopsworks.velero.backup.dynamicNamespaceFilter` <a class="headerlink" href="#helm.hopsworks.velero.backup.dynamicNamespaceFilter" title="Permanent link">#</a> { #helm.hopsworks.velero.backup.dynamicNamespaceFilter }
:   Type `object`, default `{"enabled":true,"schedule":"@hourly"}`.
    Configure cron job to dynamically list the project namespaces and update the users backup schedule, and to discover satellite namespaces (labeled hopsworks.ai/onlinefs-cluster) and update the main backup schedule. If includedNamespaces is defined then this is disabled by default.

`hopsworks.velero.backup.enabled` <a class="headerlink" href="#helm.hopsworks.velero.backup.enabled" title="Permanent link">#</a> { #helm.hopsworks.velero.backup.enabled }
:   Type `string`, default `nil`.
    Enable or disable velero for taking backups

`hopsworks.velero.backup.excludedNamespaces` <a class="headerlink" href="#helm.hopsworks.velero.backup.excludedNamespaces" title="Permanent link">#</a> { #helm.hopsworks.velero.backup.excludedNamespaces }
:   Type `list`.
    array of namespaces to exclude their resources in the backup. for ArgoCD, explicitly include all non-user namespaces since reconciliation makes dynamicNamespaceFilter ineffective.

    ??? note "Default"

        ```yaml
        - kube-system
        - kube-public
        - kube-node-lease
        - argocd
        - default
        - ingress-nginx
        ```

`hopsworks.velero.backup.includedNamespaces` <a class="headerlink" href="#helm.hopsworks.velero.backup.includedNamespaces" title="Permanent link">#</a> { #helm.hopsworks.velero.backup.includedNamespaces }
:   Type `list`, default `[]`.
    array of namespaces to include their resources in the backup

`hopsworks.velero.backup.mainScheduleName` <a class="headerlink" href="#helm.hopsworks.velero.backup.mainScheduleName" title="Permanent link">#</a> { #helm.hopsworks.velero.backup.mainScheduleName }
:   Type `string`, default `"k8s-backups-main"`.
    The name of the main backup schedule that backs up the generated secrets from the cluster, the backups metadata configmaps, and serving configmaps and secrets.

`hopsworks.velero.backup.schedule` <a class="headerlink" href="#helm.hopsworks.velero.backup.schedule" title="Permanent link">#</a> { #helm.hopsworks.velero.backup.schedule }
:   Type `string`, default `nil`.
    Backup schedule

`hopsworks.velero.backup.storageLocation` <a class="headerlink" href="#helm.hopsworks.velero.backup.storageLocation" title="Permanent link">#</a> { #helm.hopsworks.velero.backup.storageLocation }
:   Type `object`.
    The storage backup location configuration

    ??? note "Default"

        ```yaml
        create: true
        name: hopsworks-bsl
        s3ForcePathStyle: null
        storagePrefix: k8s_backup
        ```

`hopsworks.velero.backup.storageLocation.create` <a class="headerlink" href="#helm.hopsworks.velero.backup.storageLocation.create" title="Permanent link">#</a> { #helm.hopsworks.velero.backup.storageLocation.create }
:   Type `bool`, default `true`.
    create a backup storage location. If disabled, we expect a backup storage location that exists with the name velero.backup.storageLocation.name.

`hopsworks.velero.backup.storageLocation.name` <a class="headerlink" href="#helm.hopsworks.velero.backup.storageLocation.name" title="Permanent link">#</a> { #helm.hopsworks.velero.backup.storageLocation.name }
:   Type `string`, default `"hopsworks-bsl"`.
    storage backup location name. If create is enabled, we will create a new backup storage location otherwise we expect that the backup storage location to exist.

`hopsworks.velero.backup.storageLocation.s3ForcePathStyle` <a class="headerlink" href="#helm.hopsworks.velero.backup.storageLocation.s3ForcePathStyle" title="Permanent link">#</a> { #helm.hopsworks.velero.backup.storageLocation.s3ForcePathStyle }
:   Type `string`, default `nil`.
    Force S3 path-style addressing for the velero backup storage location. When unset (null), defaults to true for MinIO and unset for managed S3. Set explicitly to true for S3-compatible object storage that does not support virtual-hosted-style addressing (e.g. evroc, Ceph RadosGW).

`hopsworks.velero.backup.storageLocation.storagePrefix` <a class="headerlink" href="#helm.hopsworks.velero.backup.storageLocation.storagePrefix" title="Permanent link">#</a> { #helm.hopsworks.velero.backup.storageLocation.storagePrefix }
:   Type `string`, default `"k8s_backup"`.
    The storage prefix to store the backups under in the configured bucket

`hopsworks.velero.backup.ttl` <a class="headerlink" href="#helm.hopsworks.velero.backup.ttl" title="Permanent link">#</a> { #helm.hopsworks.velero.backup.ttl }
:   Type `string`, default `nil`.
    The amount of time before backups created on this schedule are eligible for garbage collection. If not specified, a default value of 30 days will be used. The value must be a Go-style duration using hour/minute/second units (e.g. 24h, 168h, or 24h0m0s). Calendar units such as "d" or "w" are not supported.

`hopsworks.velero.backup.usersScheduleName` <a class="headerlink" href="#helm.hopsworks.velero.backup.usersScheduleName" title="Permanent link">#</a> { #helm.hopsworks.velero.backup.usersScheduleName }
:   Type `string`, default `"k8s-backups-users-resources"`.
    The name of the users backup schedule that backs up the users' resources in their project namespaces.

`hopsworks.velero.deploymentName` <a class="headerlink" href="#helm.hopsworks.velero.deploymentName" title="Permanent link">#</a> { #helm.hopsworks.velero.deploymentName }
:   Type `string`, default `"velero"`.
    The name of the velero deployment

`hopsworks.velero.enforcePrerequisiteCheck` <a class="headerlink" href="#helm.hopsworks.velero.enforcePrerequisiteCheck" title="Permanent link">#</a> { #helm.hopsworks.velero.enforcePrerequisiteCheck }
:   Type `bool`, default `true`.
    When enabled, Helm will verify that the required Velero CRDs and Deployment already exist in the cluster using `lookup` and fail if they are missing. Disable this for offline rendering with `helm template`.

`hopsworks.velero.namespace` <a class="headerlink" href="#helm.hopsworks.velero.namespace" title="Permanent link">#</a> { #helm.hopsworks.velero.namespace }
:   Type `string`, default `"velero"`.
    The velero namespace. It should be on a different namespace other than the Hopsworks install namespace to avoid accidentaly deleting the Hopsworks namespace when uninstalling velero.

`hopsworks.velero.restore.mainScheduleBackupId` <a class="headerlink" href="#helm.hopsworks.velero.restore.mainScheduleBackupId" title="Permanent link">#</a> { #helm.hopsworks.velero.restore.mainScheduleBackupId }
:   Type `string`, default `nil`.
    The backup ID used for the restore operation of the main schedule. If unset, the latest backup from the main schedule will be used. This parameter is primarily used internally by the Helm chart during in-place restores, but also serves to record which backup ID was restored.

`hopsworks.velero.restore.usersScheduleBackupId` <a class="headerlink" href="#helm.hopsworks.velero.restore.usersScheduleBackupId" title="Permanent link">#</a> { #helm.hopsworks.velero.restore.usersScheduleBackupId }
:   Type `string`, default `nil`.
    The backup ID used for the restore operation of the users schedule. If unset, the latest backup from the users schedule will be used. This parameter is primarily used internally by the Helm chart during in-place restores, but also serves to record which backup ID was restored.

`hopsworks.velero.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.hopsworks.velero.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.hopsworks.velero.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    TTL in seconds for the velero-create-cloud-credentials Job. Overrides global default.

</div>

## wipeWhenUninstall { #helm-values-hopsworks-wipewhenuninstall }

??? example "Defaults as YAML"

    ```yaml
    hopsworks:
      wipeWhenUninstall:
      - apiGroup: remoteshuffleservices.uniffle.apache.org
        resources:
        - remoteshuffleservices
      - apiGroup: sparkapplications.sparkoperator.k8s.io
        resources:
        - sparkapplications
      - apiGroup: hopsworkscerts.certs.hopsworks.ai
        resources:
        - hopsworkscerts
      - apiGroup: certs.hopsworks.ai
        resources:
        - hopsworkscerts
      - apiGroup: batch
        resources:
        - jobs
        - cronjobs
      - apiGroup: apps
        resources:
        - deployments
        - statefulsets
        - daemonsets
      - apiGroup: rbac.authorization.k8s.io
        resources:
        - roles
        - rolebindings
        - clusterroles
        - clusterrolebindings
      - apiGroup: networking.k8s.io
        resources:
        - networkpolicies
        - ingresses
      - apiGroup: storage.k8s.io
        resources:
        - storageclasses
      - apiGroup: scheduling.k8s.io
        resources:
        - priorityclasses
      - apiGroup: admissionregistration.k8s.io
        resources:
        - mutatingwebhookconfigurations
        - validatingwebhookconfigurations
      - apiGroup: ''
        resources:
        - secrets
        - serviceaccounts
        - configmaps
        - persistentvolumeclaims
        - persistentvolumes
        - pods
        - services
        - endpoints
        - namespaces
    ```

<div class="hops-values" markdown>

`hopsworks.wipeWhenUninstall[0].apiGroup` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.0.apiGroup" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.0.apiGroup }
:   Type `string`, default `"remoteshuffleservices.uniffle.apache.org"`.

`hopsworks.wipeWhenUninstall[0].resources[0]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.0.resources.0" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.0.resources.0 }
:   Type `string`, default `"remoteshuffleservices"`.

`hopsworks.wipeWhenUninstall[10].apiGroup` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.10.apiGroup" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.10.apiGroup }
:   Type `string`, default `"admissionregistration.k8s.io"`.

`hopsworks.wipeWhenUninstall[10].resources[0]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.10.resources.0" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.10.resources.0 }
:   Type `string`, default `"mutatingwebhookconfigurations"`.

`hopsworks.wipeWhenUninstall[10].resources[1]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.10.resources.1" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.10.resources.1 }
:   Type `string`, default `"validatingwebhookconfigurations"`.

`hopsworks.wipeWhenUninstall[11].apiGroup` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.11.apiGroup" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.11.apiGroup }
:   Type `string`, default `""`.

`hopsworks.wipeWhenUninstall[11].resources[0]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.11.resources.0" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.11.resources.0 }
:   Type `string`, default `"secrets"`.

`hopsworks.wipeWhenUninstall[11].resources[1]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.11.resources.1" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.11.resources.1 }
:   Type `string`, default `"serviceaccounts"`.

`hopsworks.wipeWhenUninstall[11].resources[2]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.11.resources.2" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.11.resources.2 }
:   Type `string`, default `"configmaps"`.

`hopsworks.wipeWhenUninstall[11].resources[3]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.11.resources.3" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.11.resources.3 }
:   Type `string`, default `"persistentvolumeclaims"`.

`hopsworks.wipeWhenUninstall[11].resources[4]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.11.resources.4" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.11.resources.4 }
:   Type `string`, default `"persistentvolumes"`.

`hopsworks.wipeWhenUninstall[11].resources[5]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.11.resources.5" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.11.resources.5 }
:   Type `string`, default `"pods"`.

`hopsworks.wipeWhenUninstall[11].resources[6]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.11.resources.6" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.11.resources.6 }
:   Type `string`, default `"services"`.

`hopsworks.wipeWhenUninstall[11].resources[7]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.11.resources.7" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.11.resources.7 }
:   Type `string`, default `"endpoints"`.

`hopsworks.wipeWhenUninstall[11].resources[8]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.11.resources.8" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.11.resources.8 }
:   Type `string`, default `"namespaces"`.

`hopsworks.wipeWhenUninstall[1].apiGroup` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.1.apiGroup" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.1.apiGroup }
:   Type `string`, default `"sparkapplications.sparkoperator.k8s.io"`.

`hopsworks.wipeWhenUninstall[1].resources[0]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.1.resources.0" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.1.resources.0 }
:   Type `string`, default `"sparkapplications"`.

`hopsworks.wipeWhenUninstall[2].apiGroup` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.2.apiGroup" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.2.apiGroup }
:   Type `string`, default `"hopsworkscerts.certs.hopsworks.ai"`.

`hopsworks.wipeWhenUninstall[2].resources[0]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.2.resources.0" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.2.resources.0 }
:   Type `string`, default `"hopsworkscerts"`.

`hopsworks.wipeWhenUninstall[3].apiGroup` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.3.apiGroup" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.3.apiGroup }
:   Type `string`, default `"certs.hopsworks.ai"`.

`hopsworks.wipeWhenUninstall[3].resources[0]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.3.resources.0" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.3.resources.0 }
:   Type `string`, default `"hopsworkscerts"`.

`hopsworks.wipeWhenUninstall[4].apiGroup` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.4.apiGroup" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.4.apiGroup }
:   Type `string`, default `"batch"`.

`hopsworks.wipeWhenUninstall[4].resources[0]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.4.resources.0" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.4.resources.0 }
:   Type `string`, default `"jobs"`.

`hopsworks.wipeWhenUninstall[4].resources[1]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.4.resources.1" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.4.resources.1 }
:   Type `string`, default `"cronjobs"`.

`hopsworks.wipeWhenUninstall[5].apiGroup` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.5.apiGroup" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.5.apiGroup }
:   Type `string`, default `"apps"`.

`hopsworks.wipeWhenUninstall[5].resources[0]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.5.resources.0" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.5.resources.0 }
:   Type `string`, default `"deployments"`.

`hopsworks.wipeWhenUninstall[5].resources[1]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.5.resources.1" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.5.resources.1 }
:   Type `string`, default `"statefulsets"`.

`hopsworks.wipeWhenUninstall[5].resources[2]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.5.resources.2" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.5.resources.2 }
:   Type `string`, default `"daemonsets"`.

`hopsworks.wipeWhenUninstall[6].apiGroup` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.6.apiGroup" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.6.apiGroup }
:   Type `string`, default `"rbac.authorization.k8s.io"`.

`hopsworks.wipeWhenUninstall[6].resources[0]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.6.resources.0" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.6.resources.0 }
:   Type `string`, default `"roles"`.

`hopsworks.wipeWhenUninstall[6].resources[1]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.6.resources.1" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.6.resources.1 }
:   Type `string`, default `"rolebindings"`.

`hopsworks.wipeWhenUninstall[6].resources[2]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.6.resources.2" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.6.resources.2 }
:   Type `string`, default `"clusterroles"`.

`hopsworks.wipeWhenUninstall[6].resources[3]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.6.resources.3" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.6.resources.3 }
:   Type `string`, default `"clusterrolebindings"`.

`hopsworks.wipeWhenUninstall[7].apiGroup` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.7.apiGroup" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.7.apiGroup }
:   Type `string`, default `"networking.k8s.io"`.

`hopsworks.wipeWhenUninstall[7].resources[0]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.7.resources.0" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.7.resources.0 }
:   Type `string`, default `"networkpolicies"`.

`hopsworks.wipeWhenUninstall[7].resources[1]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.7.resources.1" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.7.resources.1 }
:   Type `string`, default `"ingresses"`.

`hopsworks.wipeWhenUninstall[8].apiGroup` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.8.apiGroup" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.8.apiGroup }
:   Type `string`, default `"storage.k8s.io"`.

`hopsworks.wipeWhenUninstall[8].resources[0]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.8.resources.0" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.8.resources.0 }
:   Type `string`, default `"storageclasses"`.

`hopsworks.wipeWhenUninstall[9].apiGroup` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.9.apiGroup" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.9.apiGroup }
:   Type `string`, default `"scheduling.k8s.io"`.

`hopsworks.wipeWhenUninstall[9].resources[0]` <a class="headerlink" href="#helm.hopsworks.wipeWhenUninstall.9.resources.0" title="Permanent link">#</a> { #helm.hopsworks.wipeWhenUninstall.9.resources.0 }
:   Type `string`, default `"priorityclasses"`.

</div>

<!-- END GENERATED VALUES -->
