# Global values { #helm-values-global }

Values under `global` are shared by every subchart: image registry and pull secrets, storage class, scheduling, cloud provider and which optional services are enabled.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.2.0-alpha-1791549041` (Hopsworks `5.2.0`)._

## General { #helm-values-global-general }

??? example "Defaults as YAML"

    ```yaml
    global:
      _hopsworks:
        airflow:
          enabled: true
          keysSecretName: hopsworks-airflow-keys
        airflowApiKeySecretName: airflow-api-key
        autoscalers: {}
        buildkitd:
          enabled: false
        centralNamespace: hopsworks
        cloudProvider: ''
        consulDomainName: consul
        csi:
          driverName: ''
          enabled: true
          image:
            pullPolicy: IfNotPresent
            repository: hopsworks/hopsfs-csi
            tag: 0.1.0-SNAPSHOT
        executor_uid: 1235
        full_platform: true
        grafana:
          extraDashboardProviders: []
        imagePullPolicy: IfNotPresent
        imagePullSecrets: []
        imageRegistry: docker.hops.works
        initContainerResources:
          runtime:
            limits:
              cpu: 1
              memory: 1Gi
            requests:
              cpu: 250m
              memory: 512Mi
          tool:
            limits:
              cpu: 500m
              memory: 512Mi
            requests:
              cpu: 100m
              memory: 128Mi
          waiter:
            limits:
              cpu: 500m
              memory: 256Mi
            requests:
              cpu: 50m
              memory: 64Mi
        jobs:
          ttlSecondsAfterFinished: 86400
        kafka:
          enabled: true
        kueue:
          enabled: false
        managedObjectStorage:
          enabled: false
          s3: null
        mode: auto
        mysql:
          hopsworksUser: hopsworksroot
          usersSecretname: mysql-users-secrets
        networkPolicy:
          rondbAccessLabels:
            access: mgmd-and-ndbmtd
        nodeSelector: {}
        onlinefs:
          email: onlinefs@hopsworks.ai
          password: onlinefspw
        opensearch:
          enabled: true
        openshift:
          enabled: false
        ray:
          enabled: false
        security:
          tls:
            enabled: true
        securityContextEnabled: true
        serviceAccount:
          annotations: {}
          create: true
          name: hopsworks-service-account
        serviceAccountAnnotations: {}
        skipDatabaseMigration: false
        spark:
          history:
            enabled: true
        storageClassName: null
        superset:
          enabled: true
          mysql:
            enabled: true
          redis:
            enabled: true
        tolerations: []
        toolbox:
          image: hwutils
          tag: 1.10-SNAPSHOT
        topologySpreadConstraint:
          maxSkew: 1
          nodeAffinityPolicy: Honor
          nodeTaintsPolicy: Honor
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: ScheduleAnyway
        vpaEnabled: false
        wipeDataOnUninstall: true
      _kserve:
        servingruntime:
          vllmomni:
            tag: v0.28.0
          vllmopenai:
            tag: v0.28.0
      imageDigests: {}
      unmanagedLoadBalancers: {}
    ```

<div class="hops-values" markdown>

`global._hopsworks.airflow.enabled` <a class="headerlink" href="#helm.global._hopsworks.airflow.enabled" title="Permanent link">#</a> { #helm.global._hopsworks.airflow.enabled }
:   Type `bool`, default `true`.
    Enable or disable the installation of the airflow sub chart

`global._hopsworks.airflow.keysSecretName` <a class="headerlink" href="#helm.global._hopsworks.airflow.keysSecretName" title="Permanent link">#</a> { #helm.global._hopsworks.airflow.keysSecretName }
:   Type `string`, default `"hopsworks-airflow-keys"`.
    Name of the Secret holding the shared-bearer secret that hopsworks-instance uses to call the Airflow `/auth/internal/*` routes. Must match airflow.airflowApi.keysSecretName so the same Secret is mounted on both sides. The default `airflow-webserver-airflow-crypto-material` is the cert-only secret and does NOT contain `internal-shared-secret`, so the hopsworks-instance pod fails to mount on a fresh v3 install.

`global._hopsworks.airflowApiKeySecretName` <a class="headerlink" href="#helm.global._hopsworks.airflowApiKeySecretName" title="Permanent link">#</a> { #helm.global._hopsworks.airflowApiKeySecretName }
:   Type `string`, default `"airflow-api-key"`.

`global._hopsworks.autoscalers` <a class="headerlink" href="#helm.global._hopsworks.autoscalers" title="Permanent link">#</a> { #helm.global._hopsworks.autoscalers }
:   Type `object`, default `{}`.
    Map of autoscaler name to VPA configuration. Each key becomes a VerticalPodAutoscaler resource named <key>-vpa.

`global._hopsworks.buildkitd.enabled` <a class="headerlink" href="#helm.global._hopsworks.buildkitd.enabled" title="Permanent link">#</a> { #helm.global._hopsworks.buildkitd.enabled }
:   Type `bool`, default `false`.

`global._hopsworks.centralNamespace` <a class="headerlink" href="#helm.global._hopsworks.centralNamespace" title="Permanent link">#</a> { #helm.global._hopsworks.centralNamespace }
:   Type `string`, default `"hopsworks"`.
    Namespace to fetch OLK signing key from. Set to null to generate a new key.

`global._hopsworks.cloudProvider` <a class="headerlink" href="#helm.global._hopsworks.cloudProvider" title="Permanent link">#</a> { #helm.global._hopsworks.cloudProvider }
:   Type `string`, default `""`.
    cloud provider (AWS, AZURE, GCP, OVH). It is used by HopsFS, Consul, and Hopsworks. Hopsfs uses it to configure the object storage parameters. Consul uses it to configure coredns accordingly. Hopsworks uses it to determine how to store the users docker images within the same hopsworks-base repo as tags or in different repo per project, If cloud provider is set all the users docker images are stored as tags - it is an AWS limitation where only tags within the repo can share layers.

`global._hopsworks.consulDomainName` <a class="headerlink" href="#helm.global._hopsworks.consulDomainName" title="Permanent link">#</a> { #helm.global._hopsworks.consulDomainName }
:   Type `string`, default `"consul"`.
    The domain name for consul where it will answer DNS queries, e.g. `service-name.service.consul`. If changed, make sure to update consul.consul.global.domain to the same value.

`global._hopsworks.csi` <a class="headerlink" href="#helm.global._hopsworks.csi" title="Permanent link">#</a> { #helm.global._hopsworks.csi }
:   Type `object`.
    HopsFS CSI integration: the hopsfs-csi node plugin FUSE-mounts an inline ephemeral volume on every HopsFS-mounting pod (Hopsworks-generated workloads, Airflow, Trino) and hands the descriptor to an unprivileged `hopsfs-fuse` native sidecar in the pod, so no workload container is privileged. `enabled` installs the hopsfs-csi DaemonSet and CSIDriver and seeds `csi_driver_enabled` to the backend; requires Kubernetes >= 1.29 (native sidecars), which the render enforces with a message naming this value. Set it to false to keep the legacy privileged in-container HopsFS mount everywhere. Known limitation: a crashed `hopsfs-fuse` sidecar leaves that pod's mount dead (I/O fails with ENOTCONN) until the pod is recreated; there is no self-heal. `image` is the ONE place the hopsfs-csi image is named: the node plugin, the Airflow and Trino sidecars and the backend `csi_sidecar_image` variable are all built from `imageRegistry` + this block, because the fusermount3 proxy in the sidecar and the fd server in the plugin are two halves of one protocol and must never drift on a node. Pin a release tag here before GA.

    ??? note "Default"

        ```yaml
        driverName: ''
        enabled: true
        image:
          pullPolicy: IfNotPresent
          repository: hopsworks/hopsfs-csi
          tag: 0.1.0-SNAPSHOT
        ```

`global._hopsworks.csi.driverName` <a class="headerlink" href="#helm.global._hopsworks.csi.driverName" title="Permanent link">#</a> { #helm.global._hopsworks.csi.driverName }
:   Type `string`, default `""`.
    The CSI driver name of this release. Empty (the default) derives `<namespace>.hopsfs.csi.logicalclocks.com` from the release namespace, one name per release, which is what lets two Hopsworks installs share a cluster: kubelet routes CSI calls by driver name alone, so each release gets its own node plugin, socket, registration and CSIDriver object, also on nodes both installs use, and uninstalling one never touches the other's mounts (HWORKS-3297). Kubernetes caps a CSI driver name at 63 characters, so a namespace longer than 34 characters must set a shorter name here. Any name set here must be unique in the cluster: two releases on one name share one socket directory and one kubelet registration on every node they share, so neither is isolated from the other, which is the fault the per-release name removes; that is not a supported setup. Whatever the name, it is computed once (`hopsworkslib.csiDriverName`) for the plugin, the Airflow and Trino volumes and the backend `csi_driver_name` variable, so nothing can drift.

`global._hopsworks.executor_uid` <a class="headerlink" href="#helm.global._hopsworks.executor_uid" title="Permanent link">#</a> { #helm.global._hopsworks.executor_uid }
:   Type `int`, default `1235`.
    User ID for the user running Hopsworks and Airflow containers

`global._hopsworks.full_platform` <a class="headerlink" href="#helm.global._hopsworks.full_platform" title="Permanent link">#</a> { #helm.global._hopsworks.full_platform }
:   Type `bool`, default `true`.
    Flag to indicate if the full platform is installed or just the online feature store infrastructure

`global._hopsworks.grafana.extraDashboardProviders` <a class="headerlink" href="#helm.global._hopsworks.grafana.extraDashboardProviders" title="Permanent link">#</a> { #helm.global._hopsworks.grafana.extraDashboardProviders }
:   Type `list`, default `[]`.
    Extra Grafana dashboard providers, appended to the provider file the grafana chart renders. The dashboards themselves ship in the Grafana image, so this is the way to provision one without rebuilding the image: mount it (for example through `grafana.grafana.dashboardsConfigMaps`, which lands at /var/lib/grafana/dashboards/<key>) and point a provider at the mount path. Entries are Grafana provider objects, so each needs at least `name`, `folder`, `type: file` and `options.path`; provider names must be unique across all providers. Paths under /usr/share/grafana/dashboards are the image's own and are verified by the verify-dashboards init container, so point elsewhere. Setting this changes the provider ConfigMap's content hash, which rolls the Grafana pod.

`global._hopsworks.imagePullPolicy` <a class="headerlink" href="#helm.global._hopsworks.imagePullPolicy" title="Permanent link">#</a> { #helm.global._hopsworks.imagePullPolicy }
:   Type `string`, default `"IfNotPresent"`.

`global._hopsworks.imagePullSecrets` <a class="headerlink" href="#helm.global._hopsworks.imagePullSecrets" title="Permanent link">#</a> { #helm.global._hopsworks.imagePullSecrets }
:   Type `list`, default `[]`.
    image pull secrets to be used by all the subcharts. Notice that for subcharts the have external dependices, you need to update the image pull secrets accordingly in those subcharts

`global._hopsworks.imageRegistry` <a class="headerlink" href="#helm.global._hopsworks.imageRegistry" title="Permanent link">#</a> { #helm.global._hopsworks.imageRegistry }
:   Type `string`, default `"docker.hops.works"`.

`global._hopsworks.initContainerResources` <a class="headerlink" href="#helm.global._hopsworks.initContainerResources" title="Permanent link">#</a> { #helm.global._hopsworks.initContainerResources }
:   Type `object`.
    Resource requests and limits for the chart's init containers, in three tiers by what the container does: `waiter` for shell wait loops, `tool` for file copies and small binaries, `runtime` for anything starting a JVM or a Python interpreter or pulling images. Every init container declares both requests and limits. A namespace `LimitRange` that supplies a `default` limit injects it into any container declaring none, and a pod's effective request is `max(sum of app containers, highest single init container)` where the init term is a floor for the pod's whole lifetime. An init container without resources can therefore pin a node's allocatable to the `LimitRange` default even after it has exited. Retune these if the target namespace has a `LimitRange` whose `min`/`max` would reject the defaults, since an out-of-range explicit value is rejected rather than defaulted.

    ??? note "Default"

        ```yaml
        runtime:
          limits:
            cpu: 1
            memory: 1Gi
          requests:
            cpu: 250m
            memory: 512Mi
        tool:
          limits:
            cpu: 500m
            memory: 512Mi
          requests:
            cpu: 100m
            memory: 128Mi
        waiter:
          limits:
            cpu: 500m
            memory: 256Mi
          requests:
            cpu: 50m
            memory: 64Mi
        ```

`global._hopsworks.jobs` <a class="headerlink" href="#helm.global._hopsworks.jobs" title="Permanent link">#</a> { #helm.global._hopsworks.jobs }
:   Type `object`, default `{"ttlSecondsAfterFinished":86400}`.
    Global configuration for Kubernetes Jobs created by the chart

`global._hopsworks.jobs.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.global._hopsworks.jobs.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.global._hopsworks.jobs.ttlSecondsAfterFinished }
:   Type `int`, default `86400`.
    Time in seconds after a finished Job is eligible for automatic cleanup. Applies to all Jobs unless overridden by a subchart-specific ttlSecondsAfterFinished value.

`global._hopsworks.kafka.enabled` <a class="headerlink" href="#helm.global._hopsworks.kafka.enabled" title="Permanent link">#</a> { #helm.global._hopsworks.kafka.enabled }
:   Type `bool`, default `true`.
    Enable or disable the installation of the kafka sub chart.

`global._hopsworks.kueue.enabled` <a class="headerlink" href="#helm.global._hopsworks.kueue.enabled" title="Permanent link">#</a> { #helm.global._hopsworks.kueue.enabled }
:   Type `bool`, default `false`.

`global._hopsworks.managedObjectStorage` <a class="headerlink" href="#helm.global._hopsworks.managedObjectStorage" title="Permanent link">#</a> { #helm.global._hopsworks.managedObjectStorage }
:   Type `object`, default `{"enabled":false,"s3":null}`.
    Configuration for managed object storage to be used by HopsFS, Opensearch, RonDB, and Hopsworks. Opensearch and RonDB uses this configuration to setup a remote sink for their backup, if a different remote sink is configured on the subchart then it will take precedence. Hopsworks uses the bucket configuration as context cache when building users' docker images, only S3 is supported at the moment.

`global._hopsworks.managedObjectStorage.s3` <a class="headerlink" href="#helm.global._hopsworks.managedObjectStorage.s3" title="Permanent link">#</a> { #helm.global._hopsworks.managedObjectStorage.s3 }
:   Type `string`, default `nil`.
    S3 configuration

`global._hopsworks.mode` <a class="headerlink" href="#helm.global._hopsworks.mode" title="Permanent link">#</a> { #helm.global._hopsworks.mode }
:   Type `string`, default `"auto"`.
    Helm installation model. "auto" lets the chart decide based on the Release.IsInstall value. "install" forces installation mode, while "upgrade" forces upgrade mode.

`global._hopsworks.mysql.hopsworksUser` <a class="headerlink" href="#helm.global._hopsworks.mysql.hopsworksUser" title="Permanent link">#</a> { #helm.global._hopsworks.mysql.hopsworksUser }
:   Type `string`, default `"hopsworksroot"`.

`global._hopsworks.mysql.usersSecretname` <a class="headerlink" href="#helm.global._hopsworks.mysql.usersSecretname" title="Permanent link">#</a> { #helm.global._hopsworks.mysql.usersSecretname }
:   Type `string`, default `"mysql-users-secrets"`.

`global._hopsworks.networkPolicy.rondbAccessLabels.access` <a class="headerlink" href="#helm.global._hopsworks.networkPolicy.rondbAccessLabels.access" title="Permanent link">#</a> { #helm.global._hopsworks.networkPolicy.rondbAccessLabels.access }
:   Type `string`, default `"mgmd-and-ndbmtd"`.

`global._hopsworks.nodeSelector` <a class="headerlink" href="#helm.global._hopsworks.nodeSelector" title="Permanent link">#</a> { #helm.global._hopsworks.nodeSelector }
:   Type `object`, default `{}`.
    Specifies the global nodeSelector settings applied across all subcharts unless explicitly overridden within a specific subchart. This ensures Kubernetes schedules Pods only onto nodes that match all the specified labels. Notice that some subcharts do not use this global variable, and you must manually override those by defining them in the values.yaml file, using anchors if necessary.

`global._hopsworks.onlinefs.email` <a class="headerlink" href="#helm.global._hopsworks.onlinefs.email" title="Permanent link">#</a> { #helm.global._hopsworks.onlinefs.email }
:   Type `string`, default `"onlinefs@hopsworks.ai"`.

`global._hopsworks.onlinefs.password` <a class="headerlink" href="#helm.global._hopsworks.onlinefs.password" title="Permanent link">#</a> { #helm.global._hopsworks.onlinefs.password }
:   Type `string`, default `"onlinefspw"`.

`global._hopsworks.opensearch` <a class="headerlink" href="#helm.global._hopsworks.opensearch" title="Permanent link">#</a> { #helm.global._hopsworks.opensearch }
:   Type `object`, default `{"enabled":true}`.
    Enable or disable the opensearch

`global._hopsworks.opensearch.enabled` <a class="headerlink" href="#helm.global._hopsworks.opensearch.enabled" title="Permanent link">#</a> { #helm.global._hopsworks.opensearch.enabled }
:   Type `bool`, default `true`.
    Enable or disable the opensearch

`global._hopsworks.openshift.enabled` <a class="headerlink" href="#helm.global._hopsworks.openshift.enabled" title="Permanent link">#</a> { #helm.global._hopsworks.openshift.enabled }
:   Type `bool`, default `false`.
    Enable when installing on Openshift platform

`global._hopsworks.ray.enabled` <a class="headerlink" href="#helm.global._hopsworks.ray.enabled" title="Permanent link">#</a> { #helm.global._hopsworks.ray.enabled }
:   Type `bool`, default `false`.

`global._hopsworks.security.tls.enabled` <a class="headerlink" href="#helm.global._hopsworks.security.tls.enabled" title="Permanent link">#</a> { #helm.global._hopsworks.security.tls.enabled }
:   Type `bool`, default `true`.

`global._hopsworks.securityContextEnabled` <a class="headerlink" href="#helm.global._hopsworks.securityContextEnabled" title="Permanent link">#</a> { #helm.global._hopsworks.securityContextEnabled }
:   Type `bool`, default `true`.
    Flag to disable templating SecurityContext for Openshift

`global._hopsworks.serviceAccount.annotations` <a class="headerlink" href="#helm.global._hopsworks.serviceAccount.annotations" title="Permanent link">#</a> { #helm.global._hopsworks.serviceAccount.annotations }
:   Type `object`, default `{}`.
    custom annotations for the Hopsworks service account

`global._hopsworks.serviceAccount.create` <a class="headerlink" href="#helm.global._hopsworks.serviceAccount.create" title="Permanent link">#</a> { #helm.global._hopsworks.serviceAccount.create }
:   Type `bool`, default `true`.

`global._hopsworks.serviceAccount.name` <a class="headerlink" href="#helm.global._hopsworks.serviceAccount.name" title="Permanent link">#</a> { #helm.global._hopsworks.serviceAccount.name }
:   Type `string`, default `"hopsworks-service-account"`.

`global._hopsworks.serviceAccountAnnotations` <a class="headerlink" href="#helm.global._hopsworks.serviceAccountAnnotations" title="Permanent link">#</a> { #helm.global._hopsworks.serviceAccountAnnotations }
:   Type `object`, default `{}`.
    Use it to annotate the serviceAccounts we create for Hopsworks

`global._hopsworks.skipDatabaseMigration` <a class="headerlink" href="#helm.global._hopsworks.skipDatabaseMigration" title="Permanent link">#</a> { #helm.global._hopsworks.skipDatabaseMigration }
:   Type `bool`, default `false`.
    Special flag which MUST be used only for 3.x -> 4.0 migrations (HWORKS-1600)

`global._hopsworks.spark.history.enabled` <a class="headerlink" href="#helm.global._hopsworks.spark.history.enabled" title="Permanent link">#</a> { #helm.global._hopsworks.spark.history.enabled }
:   Type `bool`, default `true`.
    Enable or disable installing of the spark history server

`global._hopsworks.storageClassName` <a class="headerlink" href="#helm.global._hopsworks.storageClassName" title="Permanent link">#</a> { #helm.global._hopsworks.storageClassName }
:   Type `string`, default `nil`.
    global storage class name

`global._hopsworks.superset.enabled` <a class="headerlink" href="#helm.global._hopsworks.superset.enabled" title="Permanent link">#</a> { #helm.global._hopsworks.superset.enabled }
:   Type `bool`, default `true`.
    Enable or disable the installation of the superset sub chart.

`global._hopsworks.superset.mysql.enabled` <a class="headerlink" href="#helm.global._hopsworks.superset.mysql.enabled" title="Permanent link">#</a> { #helm.global._hopsworks.superset.mysql.enabled }
:   Type `bool`, default `true`.
    Enable or disable MySQL for Superset. Must match superset.mysql.enabled for consistent behavior across charts.

`global._hopsworks.superset.redis.enabled` <a class="headerlink" href="#helm.global._hopsworks.superset.redis.enabled" title="Permanent link">#</a> { #helm.global._hopsworks.superset.redis.enabled }
:   Type `bool`, default `true`.
    Enable or disable Redis for Superset. Must match superset.superset.redis.enabled for consistent behavior across charts.

`global._hopsworks.tolerations` <a class="headerlink" href="#helm.global._hopsworks.tolerations" title="Permanent link">#</a> { #helm.global._hopsworks.tolerations }
:   Type `list`, default `[]`.
    Specifies the global tolerations settings applied to all subcharts unless explicitly overridden in a specific subchart. These tolerations allow Kubernetes to schedule Pods on nodes with matching taints, ensuring proper placement based on cluster policies.  Notice that some subcharts do not use this global variable, and you must manually override those by defining them in the values.yaml file, using anchors if necessary.

`global._hopsworks.toolbox.image` <a class="headerlink" href="#helm.global._hopsworks.toolbox.image" title="Permanent link">#</a> { #helm.global._hopsworks.toolbox.image }
:   Type `string`, default `"hwutils"`.

`global._hopsworks.toolbox.tag` <a class="headerlink" href="#helm.global._hopsworks.toolbox.tag" title="Permanent link">#</a> { #helm.global._hopsworks.toolbox.tag }
:   Type `string`, default `"1.10-SNAPSHOT"`.

`global._hopsworks.topologySpreadConstraint` <a class="headerlink" href="#helm.global._hopsworks.topologySpreadConstraint" title="Permanent link">#</a> { #helm.global._hopsworks.topologySpreadConstraint }
:   Type `object`.
    default topology spread constraint. If not defined the global topology spread constraint would be used

    ??? note "Default"

        ```yaml
        maxSkew: 1
        nodeAffinityPolicy: Honor
        nodeTaintsPolicy: Honor
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: ScheduleAnyway
        ```

`global._hopsworks.vpaEnabled` <a class="headerlink" href="#helm.global._hopsworks.vpaEnabled" title="Permanent link">#</a> { #helm.global._hopsworks.vpaEnabled }
:   Type `bool`, default `false`.

`global._hopsworks.wipeDataOnUninstall` <a class="headerlink" href="#helm.global._hopsworks.wipeDataOnUninstall" title="Permanent link">#</a> { #helm.global._hopsworks.wipeDataOnUninstall }
:   Type `bool`, default `true`.
    on uninstall, delete data PVCs left behind by StatefulSets unless the PVC carries the label hopsworks.ai/keep=true. Consumed by subchart post-delete cleanup hooks via the hopsworkslib.wipeDataOnUninstall helper.

`global._kserve` <a class="headerlink" href="#helm.global._kserve" title="Permanent link">#</a> { #helm.global._kserve }
:   Type `object`.
    Global KServe values shared between the kserve and hopsworks subcharts

    ??? note "Default"

        ```yaml
        servingruntime:
          vllmomni:
            tag: v0.28.0
          vllmopenai:
            tag: v0.28.0
        ```

`global._kserve.servingruntime` <a class="headerlink" href="#helm.global._kserve.servingruntime" title="Permanent link">#</a> { #helm.global._kserve.servingruntime }
:   Type `object`, default `{"vllmomni":{"tag":"v0.28.0"},"vllmopenai":{"tag":"v0.28.0"}}`.
    Mirrors the kserve subchart's `kserve.servingruntime` layout. Tags here drive both the kserve ClusterServingRuntime images and the kube_serving_vllm*_versions hopsworks variable seeds.

`global._kserve.servingruntime.vllmomni` <a class="headerlink" href="#helm.global._kserve.servingruntime.vllmomni" title="Permanent link">#</a> { #helm.global._kserve.servingruntime.vllmomni }
:   Type `object`, default `{"tag":"v0.28.0"}`.
    vLLM-Omni runtime image tag. Drives both the kserve ClusterServingRuntime image and the kube_serving_vllm_omni_versions hopsworks variable seed.

`global._kserve.servingruntime.vllmopenai` <a class="headerlink" href="#helm.global._kserve.servingruntime.vllmopenai" title="Permanent link">#</a> { #helm.global._kserve.servingruntime.vllmopenai }
:   Type `object`, default `{"tag":"v0.28.0"}`.
    vLLM-OpenAI runtime image tag. Drives both the kserve ClusterServingRuntime image and the kube_serving_vllm_versions hopsworks variable seed.

`global.imageDigests` <a class="headerlink" href="#helm.global.imageDigests" title="Permanent link">#</a> { #helm.global.imageDigests }
:   Type `object`, default `{}`.
    map image name to sha digest to be used instead of tags for reproducible deployment 

`global.unmanagedLoadBalancers` <a class="headerlink" href="#helm.global.unmanagedLoadBalancers" title="Permanent link">#</a> { #helm.global.unmanagedLoadBalancers }
:   Type `object`, default `{}`.
    Load balancer configuration when using unmanaged LB, in AWS is the TargetGroup ARNs for each service      

</div>

## backups { #helm-values-global-backups }

??? example "Defaults as YAML"

    ```yaml
    global:
      _hopsworks:
        backups:
          enabled: true
          metadataStore:
            configMap:
              opensearch: opensearch-backups-metadata
              ronDB: rondb-backups-metadata
              superset: superset-backups-metadata
          schedule: '@weekly'
          ttl: null
    ```

<div class="hops-values" markdown>

`global._hopsworks.backups` <a class="headerlink" href="#helm.global._hopsworks.backups" title="Permanent link">#</a> { #helm.global._hopsworks.backups }
:   Type `object`.
    enable global backups configuration

    ??? note "Default"

        ```yaml
        enabled: true
        metadataStore:
          configMap:
            opensearch: opensearch-backups-metadata
            ronDB: rondb-backups-metadata
            superset: superset-backups-metadata
        schedule: '@weekly'
        ttl: null
        ```

`global._hopsworks.backups.enabled` <a class="headerlink" href="#helm.global._hopsworks.backups.enabled" title="Permanent link">#</a> { #helm.global._hopsworks.backups.enabled }
:   Type `bool`, default `true`.
    enable global backup

`global._hopsworks.backups.metadataStore` <a class="headerlink" href="#helm.global._hopsworks.backups.metadataStore" title="Permanent link">#</a> { #helm.global._hopsworks.backups.metadataStore }
:   Type `object`.
    backups metadata store

    ??? note "Default"

        ```yaml
        configMap:
          opensearch: opensearch-backups-metadata
          ronDB: rondb-backups-metadata
          superset: superset-backups-metadata
        ```

`global._hopsworks.backups.metadataStore.configMap.opensearch` <a class="headerlink" href="#helm.global._hopsworks.backups.metadataStore.configMap.opensearch" title="Permanent link">#</a> { #helm.global._hopsworks.backups.metadataStore.configMap.opensearch }
:   Type `string`, default `"opensearch-backups-metadata"`.
    name of the configmap to store metadata information about opensearch backups

`global._hopsworks.backups.metadataStore.configMap.ronDB` <a class="headerlink" href="#helm.global._hopsworks.backups.metadataStore.configMap.ronDB" title="Permanent link">#</a> { #helm.global._hopsworks.backups.metadataStore.configMap.ronDB }
:   Type `string`, default `"rondb-backups-metadata"`.
    name of the configmap to store metadata information about rondb backups 

`global._hopsworks.backups.metadataStore.configMap.superset` <a class="headerlink" href="#helm.global._hopsworks.backups.metadataStore.configMap.superset" title="Permanent link">#</a> { #helm.global._hopsworks.backups.metadataStore.configMap.superset }
:   Type `string`, default `"superset-backups-metadata"`.
    name of the configmap to store metadata information about superset backups

`global._hopsworks.backups.schedule` <a class="headerlink" href="#helm.global._hopsworks.backups.schedule" title="Permanent link">#</a> { #helm.global._hopsworks.backups.schedule }
:   Type `string`, default `"@weekly"`.
    cron schedule

`global._hopsworks.backups.ttl` <a class="headerlink" href="#helm.global._hopsworks.backups.ttl" title="Permanent link">#</a> { #helm.global._hopsworks.backups.ttl }
:   Type `string`, default `nil`.
    time to live to control when to clean up backups. It is a number followed by either d (days) or h (hours) suffix.

</div>

## externalLoadBalancers { #helm-values-global-externalloadbalancers }

??? example "Defaults as YAML"

    ```yaml
    global:
      _hopsworks:
        externalLoadBalancers:
          annotations: {}
          class: null
          enabled: true
          managed: true
    ```

<div class="hops-values" markdown>

`global._hopsworks.externalLoadBalancers` <a class="headerlink" href="#helm.global._hopsworks.externalLoadBalancers" title="Permanent link">#</a> { #helm.global._hopsworks.externalLoadBalancers }
:   Type `object`, default `{"annotations":{},"class":null,"enabled":true,"managed":true}`.
    Global load balancer configuration for external access to Hopsworks services: ArrowFlight, Kafka, and MySQL We fallback to this loadBalancerClass if the local loadBalancerClass is not defined

`global._hopsworks.externalLoadBalancers.annotations` <a class="headerlink" href="#helm.global._hopsworks.externalLoadBalancers.annotations" title="Permanent link">#</a> { #helm.global._hopsworks.externalLoadBalancers.annotations }
:   Type `object`, default `{}`.
    Generic annotations attached to LoadBalancer objects

`global._hopsworks.externalLoadBalancers.class` <a class="headerlink" href="#helm.global._hopsworks.externalLoadBalancers.class" title="Permanent link">#</a> { #helm.global._hopsworks.externalLoadBalancers.class }
:   Type `string`, default `nil`.
    Name of the LoadBalancer class

`global._hopsworks.externalLoadBalancers.enabled` <a class="headerlink" href="#helm.global._hopsworks.externalLoadBalancers.enabled" title="Permanent link">#</a> { #helm.global._hopsworks.externalLoadBalancers.enabled }
:   Type `bool`, default `true`.
    Enable LoadBalancer Services

`global._hopsworks.externalLoadBalancers.managed` <a class="headerlink" href="#helm.global._hopsworks.externalLoadBalancers.managed" title="Permanent link">#</a> { #helm.global._hopsworks.externalLoadBalancers.managed }
:   Type `bool`, default `true`.
    Cloud provider provisions Load Balancers

</div>

## externalServices { #helm-values-global-externalservices }

??? example "Defaults as YAML"

    ```yaml
    global:
      _hopsworks:
        externalServices:
          hopsfs:
            external: false
            namenodeAddresses: []
          opensearch:
            addresses: []
            external: false
          prometheus:
            addresses: []
            external: false
          rondb:
            external: false
            mgmdHostname: ''
    ```

<div class="hops-values" markdown>

`global._hopsworks.externalServices` <a class="headerlink" href="#helm.global._hopsworks.externalServices" title="Permanent link">#</a> { #helm.global._hopsworks.externalServices }
:   Type `object`.
    Configuration for when services are external to this Kubernetes installation

    ??? note "Default"

        ```yaml
        hopsfs:
          external: false
          namenodeAddresses: []
        opensearch:
          addresses: []
          external: false
        prometheus:
          addresses: []
          external: false
        rondb:
          external: false
          mgmdHostname: ''
        ```

`global._hopsworks.externalServices.hopsfs` <a class="headerlink" href="#helm.global._hopsworks.externalServices.hopsfs" title="Permanent link">#</a> { #helm.global._hopsworks.externalServices.hopsfs }
:   Type `object`, default `{"external":false,"namenodeAddresses":[]}`.
    HopsFS configuration when it is installed externally

`global._hopsworks.externalServices.hopsfs.external` <a class="headerlink" href="#helm.global._hopsworks.externalServices.hopsfs.external" title="Permanent link">#</a> { #helm.global._hopsworks.externalServices.hopsfs.external }
:   Type `bool`, default `false`.
    Flag to indicate HopsFS is installed externally

`global._hopsworks.externalServices.hopsfs.namenodeAddresses` <a class="headerlink" href="#helm.global._hopsworks.externalServices.hopsfs.namenodeAddresses" title="Permanent link">#</a> { #helm.global._hopsworks.externalServices.hopsfs.namenodeAddresses }
:   Type `list`, default `[]`.
    IP addresses where HopsFS Namenodes are installed

`global._hopsworks.externalServices.opensearch` <a class="headerlink" href="#helm.global._hopsworks.externalServices.opensearch" title="Permanent link">#</a> { #helm.global._hopsworks.externalServices.opensearch }
:   Type `object`, default `{"addresses":[],"external":false}`.
    Opensearch configuration when it is installed externally

`global._hopsworks.externalServices.opensearch.addresses` <a class="headerlink" href="#helm.global._hopsworks.externalServices.opensearch.addresses" title="Permanent link">#</a> { #helm.global._hopsworks.externalServices.opensearch.addresses }
:   Type `list`, default `[]`.
    IP addresses where OpenSearch is installed

`global._hopsworks.externalServices.opensearch.external` <a class="headerlink" href="#helm.global._hopsworks.externalServices.opensearch.external" title="Permanent link">#</a> { #helm.global._hopsworks.externalServices.opensearch.external }
:   Type `bool`, default `false`.
    Flag to indicate Opensearch is installed externally

`global._hopsworks.externalServices.prometheus` <a class="headerlink" href="#helm.global._hopsworks.externalServices.prometheus" title="Permanent link">#</a> { #helm.global._hopsworks.externalServices.prometheus }
:   Type `object`, default `{"addresses":[],"external":false}`.
    prometheus configuration when it is installed externally

`global._hopsworks.externalServices.prometheus.addresses` <a class="headerlink" href="#helm.global._hopsworks.externalServices.prometheus.addresses" title="Permanent link">#</a> { #helm.global._hopsworks.externalServices.prometheus.addresses }
:   Type `list`, default `[]`.
    IP addresses where prometheus is installed

`global._hopsworks.externalServices.prometheus.external` <a class="headerlink" href="#helm.global._hopsworks.externalServices.prometheus.external" title="Permanent link">#</a> { #helm.global._hopsworks.externalServices.prometheus.external }
:   Type `bool`, default `false`.
    Flag to indicate prometheus is installed externally

`global._hopsworks.externalServices.rondb` <a class="headerlink" href="#helm.global._hopsworks.externalServices.rondb" title="Permanent link">#</a> { #helm.global._hopsworks.externalServices.rondb }
:   Type `object`, default `{"external":false,"mgmdHostname":""}`.
    RonDB configuration when it is installed externally

`global._hopsworks.externalServices.rondb.external` <a class="headerlink" href="#helm.global._hopsworks.externalServices.rondb.external" title="Permanent link">#</a> { #helm.global._hopsworks.externalServices.rondb.external }
:   Type `bool`, default `false`.
    Flag to indicate RonDB is installed externally

`global._hopsworks.externalServices.rondb.mgmdHostname` <a class="headerlink" href="#helm.global._hopsworks.externalServices.rondb.mgmdHostname" title="Permanent link">#</a> { #helm.global._hopsworks.externalServices.rondb.mgmdHostname }
:   Type `string`, default `""`.
    Hostname of the machine where RonDB management service is running

</div>

## kyverno { #helm-values-global-kyverno }

??? example "Defaults as YAML"

    ```yaml
    global:
      _hopsworks:
        kyverno:
          enabled: false
          policies:
            addCertificatesVolume:
              enabled: false
              initContainers:
                annotation:
                  key: kyverno-inject-certs-init
                  value: enabled
                enabled: false
              mountPath: /etc/ssl/certs
              preconditions:
                annotation:
                  key: kyverno-inject-certs
                  value: enabled
                enabled: true
    ```

<div class="hops-values" markdown>

`global._hopsworks.kyverno.enabled` <a class="headerlink" href="#helm.global._hopsworks.kyverno.enabled" title="Permanent link">#</a> { #helm.global._hopsworks.kyverno.enabled }
:   Type `bool`, default `false`.
    Enable or disable kyverno policies installation

`global._hopsworks.kyverno.policies.addCertificatesVolume` <a class="headerlink" href="#helm.global._hopsworks.kyverno.policies.addCertificatesVolume" title="Permanent link">#</a> { #helm.global._hopsworks.kyverno.policies.addCertificatesVolume }
:   Type `object`.
    Configuration to add custom certificates to pods as a mounted volume

    ??? note "Default"

        ```yaml
        enabled: false
        initContainers:
          annotation:
            key: kyverno-inject-certs-init
            value: enabled
          enabled: false
        mountPath: /etc/ssl/certs
        preconditions:
          annotation:
            key: kyverno-inject-certs
            value: enabled
          enabled: true
        ```

`global._hopsworks.kyverno.policies.addCertificatesVolume.enabled` <a class="headerlink" href="#helm.global._hopsworks.kyverno.policies.addCertificatesVolume.enabled" title="Permanent link">#</a> { #helm.global._hopsworks.kyverno.policies.addCertificatesVolume.enabled }
:   Type `bool`, default `false`.
    Enable add certificates volume

`global._hopsworks.kyverno.policies.addCertificatesVolume.initContainers` <a class="headerlink" href="#helm.global._hopsworks.kyverno.policies.addCertificatesVolume.initContainers" title="Permanent link">#</a> { #helm.global._hopsworks.kyverno.policies.addCertificatesVolume.initContainers }
:   Type `object`.
    Opt-in for injecting the certificates volume into init containers. The main addCertificatesVolume policy only mutates spec.containers; init containers are intentionally left untouched because they are often injected by third-party operators (Istio, KServe, sidecar injectors) that ship minimal images where overwriting /etc/ssl/certs would break them. When enabled, a second mutate rule is rendered that iterates spec.initContainers and is gated by an OR of the dedicated init-container annotation below and any extraAnnotations / labels configured under the hw-kyverno subchart at policies.addCertificatesVolume.initContainers. The annotation is distinct from preconditions.annotation so authors can opt main containers and init containers in independently.

    ??? note "Default"

        ```yaml
        annotation:
          key: kyverno-inject-certs-init
          value: enabled
        enabled: false
        ```

`global._hopsworks.kyverno.policies.addCertificatesVolume.initContainers.annotation` <a class="headerlink" href="#helm.global._hopsworks.kyverno.policies.addCertificatesVolume.initContainers.annotation" title="Permanent link">#</a> { #helm.global._hopsworks.kyverno.policies.addCertificatesVolume.initContainers.annotation }
:   Type `object`, default `{"key":"kyverno-inject-certs-init","value":"enabled"}`.
    The key and value of the annotation used to opt a pod's init containers into certificate volume injection. Distinct from preconditions.annotation so authors can opt main containers and init containers in independently. A pod opts in by matching any one of: this annotation, an entry in the hw-kyverno subchart's policies.addCertificatesVolume.initContainers.extraAnnotations, or an entry in policies.addCertificatesVolume.initContainers.labels.

`global._hopsworks.kyverno.policies.addCertificatesVolume.initContainers.enabled` <a class="headerlink" href="#helm.global._hopsworks.kyverno.policies.addCertificatesVolume.initContainers.enabled" title="Permanent link">#</a> { #helm.global._hopsworks.kyverno.policies.addCertificatesVolume.initContainers.enabled }
:   Type `bool`, default `false`.
    Render the init-container mutate rule. When false (default), the policy never touches init containers regardless of any annotation, label, or extra annotation set on a pod.

`global._hopsworks.kyverno.policies.addCertificatesVolume.mountPath` <a class="headerlink" href="#helm.global._hopsworks.kyverno.policies.addCertificatesVolume.mountPath" title="Permanent link">#</a> { #helm.global._hopsworks.kyverno.policies.addCertificatesVolume.mountPath }
:   Type `string`, default `"/etc/ssl/certs"`.
    Path to mount the certificates volume

`global._hopsworks.kyverno.policies.addCertificatesVolume.preconditions.annotation` <a class="headerlink" href="#helm.global._hopsworks.kyverno.policies.addCertificatesVolume.preconditions.annotation" title="Permanent link">#</a> { #helm.global._hopsworks.kyverno.policies.addCertificatesVolume.preconditions.annotation }
:   Type `object`, default `{"key":"kyverno-inject-certs","value":"enabled"}`.
    The key and value of the annotation used to inject kyverno certificates. If a pod has this annotation, it will be mutated. There are other options under hw-kyverno subchart to use labels and extra annotations as needed.

`global._hopsworks.kyverno.policies.addCertificatesVolume.preconditions.enabled` <a class="headerlink" href="#helm.global._hopsworks.kyverno.policies.addCertificatesVolume.preconditions.enabled" title="Permanent link">#</a> { #helm.global._hopsworks.kyverno.policies.addCertificatesVolume.preconditions.enabled }
:   Type `bool`, default `true`.
    Enable adding preconditions to the police. If disabled, the policy will apply to all the pods in the installation namespace and the hopsworks projects' namespaces created when crating a project.

</div>

## managedDockerRegistery { #helm-values-global-manageddockerregistery }

??? example "Defaults as YAML"

    ```yaml
    global:
      _hopsworks:
        managedDockerRegistery:
          credHelper:
            enabled: false
            secretName: ''
          domain: ''
          enabled: false
          namespace: ''
          port: null
    ```

<div class="hops-values" markdown>

`global._hopsworks.managedDockerRegistery` <a class="headerlink" href="#helm.global._hopsworks.managedDockerRegistery" title="Permanent link">#</a> { #helm.global._hopsworks.managedDockerRegistery }
:   Type `object`.
    configure managed docker registry for Hopsworks to store the user's docker image

    ??? note "Default"

        ```yaml
        credHelper:
          enabled: false
          secretName: ''
        domain: ''
        enabled: false
        namespace: ''
        port: null
        ```

`global._hopsworks.managedDockerRegistery.credHelper` <a class="headerlink" href="#helm.global._hopsworks.managedDockerRegistery.credHelper" title="Permanent link">#</a> { #helm.global._hopsworks.managedDockerRegistery.credHelper }
:   Type `object`, default `{"enabled":false,"secretName":""}`.
    credentials helper to use for the managed docker registry. We only support cred helpers for [AWS](https://github.com/awslabs/amazon-ecr-credential-helper) and [GCP](https://github.com/GoogleCloudPlatform/docker-credential-gcr)

`global._hopsworks.managedDockerRegistery.credHelper.secretName` <a class="headerlink" href="#helm.global._hopsworks.managedDockerRegistery.credHelper.secretName" title="Permanent link">#</a> { #helm.global._hopsworks.managedDockerRegistery.credHelper.secretName }
:   Type `string`, default `""`.
    the name of the secret to be created with the credentials helper configuration

`global._hopsworks.managedDockerRegistery.domain` <a class="headerlink" href="#helm.global._hopsworks.managedDockerRegistery.domain" title="Permanent link">#</a> { #helm.global._hopsworks.managedDockerRegistery.domain }
:   Type `string`, default `""`.
    the managed docker registry domain name

`global._hopsworks.managedDockerRegistery.namespace` <a class="headerlink" href="#helm.global._hopsworks.managedDockerRegistery.namespace" title="Permanent link">#</a> { #helm.global._hopsworks.managedDockerRegistery.namespace }
:   Type `string`, default `""`.
    the namespace to be used

`global._hopsworks.managedDockerRegistery.port` <a class="headerlink" href="#helm.global._hopsworks.managedDockerRegistery.port" title="Permanent link">#</a> { #helm.global._hopsworks.managedDockerRegistery.port }
:   Type `string`, default `nil`.
    port number for the managed docker registry 

</div>

## minio { #helm-values-global-minio }

??? example "Defaults as YAML"

    ```yaml
    global:
      _hopsworks:
        minio:
          enabled: true
          hopsfs:
            bucket: hopsfs
            enabled: true
          password: minioadmin
          region: eu-west-1
          user: minioadmin
    ```

<div class="hops-values" markdown>

`global._hopsworks.minio.enabled` <a class="headerlink" href="#helm.global._hopsworks.minio.enabled" title="Permanent link">#</a> { #helm.global._hopsworks.minio.enabled }
:   Type `bool`, default `true`.

`global._hopsworks.minio.hopsfs.bucket` <a class="headerlink" href="#helm.global._hopsworks.minio.hopsfs.bucket" title="Permanent link">#</a> { #helm.global._hopsworks.minio.hopsfs.bucket }
:   Type `string`, default `"hopsfs"`.

`global._hopsworks.minio.hopsfs.enabled` <a class="headerlink" href="#helm.global._hopsworks.minio.hopsfs.enabled" title="Permanent link">#</a> { #helm.global._hopsworks.minio.hopsfs.enabled }
:   Type `bool`, default `true`.

`global._hopsworks.minio.password` <a class="headerlink" href="#helm.global._hopsworks.minio.password" title="Permanent link">#</a> { #helm.global._hopsworks.minio.password }
:   Type `string`, default `"minioadmin"`.

`global._hopsworks.minio.region` <a class="headerlink" href="#helm.global._hopsworks.minio.region" title="Permanent link">#</a> { #helm.global._hopsworks.minio.region }
:   Type `string`, default `"eu-west-1"`.

`global._hopsworks.minio.user` <a class="headerlink" href="#helm.global._hopsworks.minio.user" title="Permanent link">#</a> { #helm.global._hopsworks.minio.user }
:   Type `string`, default `"minioadmin"`.

</div>

## restoreFromBackup { #helm-values-global-restorefrombackup }

??? example "Defaults as YAML"

    ```yaml
    global:
      _hopsworks:
        restoreFromBackup:
          backupId: null
          forceDataClear: false
          inPlace: false
          superset:
            activeDeadlineSeconds: 14400
            backupId: null
            enabled: false
            initiatedBy: null
    ```

<div class="hops-values" markdown>

`global._hopsworks.restoreFromBackup` <a class="headerlink" href="#helm.global._hopsworks.restoreFromBackup" title="Permanent link">#</a> { #helm.global._hopsworks.restoreFromBackup }
:   Type `object`.
    restore cluster from a backup id

    ??? note "Default"

        ```yaml
        backupId: null
        forceDataClear: false
        inPlace: false
        superset:
          activeDeadlineSeconds: 14400
          backupId: null
          enabled: false
          initiatedBy: null
        ```

`global._hopsworks.restoreFromBackup.backupId` <a class="headerlink" href="#helm.global._hopsworks.restoreFromBackup.backupId" title="Permanent link">#</a> { #helm.global._hopsworks.restoreFromBackup.backupId }
:   Type `string`, default `nil`.
    the backup id to restore

`global._hopsworks.restoreFromBackup.forceDataClear` <a class="headerlink" href="#helm.global._hopsworks.restoreFromBackup.forceDataClear" title="Permanent link">#</a> { #helm.global._hopsworks.restoreFromBackup.forceDataClear }
:   Type `bool`, default `false`.
    flag to indicate if the data should be forcibly cleared before restore

`global._hopsworks.restoreFromBackup.inPlace` <a class="headerlink" href="#helm.global._hopsworks.restoreFromBackup.inPlace" title="Permanent link">#</a> { #helm.global._hopsworks.restoreFromBackup.inPlace }
:   Type `bool`, default `false`.
    flag to indicate if the restore should be done in-place or to a new cluster

`global._hopsworks.restoreFromBackup.superset` <a class="headerlink" href="#helm.global._hopsworks.restoreFromBackup.superset" title="Permanent link">#</a> { #helm.global._hopsworks.restoreFromBackup.superset }
:   Type `object`.
    Superset database restore (HWORKS-2973). Set enabled and backupId, add values.superset-restore.yaml to hold Superset at zero replicas, and upgrade; when the superset-restore-<backupId> Job has completed, remove the file, set enabled=false and upgrade again.

    ??? note "Default"

        ```yaml
        activeDeadlineSeconds: 14400
        backupId: null
        enabled: false
        initiatedBy: null
        ```

`global._hopsworks.restoreFromBackup.superset.activeDeadlineSeconds` <a class="headerlink" href="#helm.global._hopsworks.restoreFromBackup.superset.activeDeadlineSeconds" title="Permanent link">#</a> { #helm.global._hopsworks.restoreFromBackup.superset.activeDeadlineSeconds }
:   Type `int`, default `14400`.
    activeDeadlineSeconds for the restore Job, bounding the wait for the Superset pods and the secret key, the download and the reload

`global._hopsworks.restoreFromBackup.superset.backupId` <a class="headerlink" href="#helm.global._hopsworks.restoreFromBackup.superset.backupId" title="Permanent link">#</a> { #helm.global._hopsworks.restoreFromBackup.superset.backupId }
:   Type `string`, default `nil`.
    the Superset backup id to restore (a key in the superset-backups-metadata ConfigMap). Required when enabled

`global._hopsworks.restoreFromBackup.superset.enabled` <a class="headerlink" href="#helm.global._hopsworks.restoreFromBackup.superset.enabled" title="Permanent link">#</a> { #helm.global._hopsworks.restoreFromBackup.superset.enabled }
:   Type `bool`, default `false`.
    reload the Superset database from a backup

`global._hopsworks.restoreFromBackup.superset.initiatedBy` <a class="headerlink" href="#helm.global._hopsworks.restoreFromBackup.superset.initiatedBy" title="Permanent link">#</a> { #helm.global._hopsworks.restoreFromBackup.superset.initiatedBy }
:   Type `string`, default `nil`.
    who initiated this restore, recorded in the superset-restore-audit ConfigMap. Defaults to helm/<release>@rev<revision>. Deployment metadata, not an authenticated identity: the Kubernetes audit log has the actor

</div>

## trino { #helm-values-global-trino }

??? example "Defaults as YAML"

    ```yaml
    global:
      _hopsworks:
        trino:
          auth:
            refreshPeriod: 5s
          egressProbe:
            echoUrl: ''
          enabled: true
          files:
            csi:
              defaultPermissions: false
              fdSocketVolume: trino-files-fuse-fd
              sidecarGid: 1000
              sidecarUid: 1000
            mountPath: /opt/hopsworks/trino
            mountWaitSeconds: 300
            storeRoot: /apps/trino
          image:
            tag: 483-v1
          mountRetryTimeLimit: 2m
          mountableSecrets:
            csi:
              defaultPermissions: false
              sidecarGid: 1000
              sidecarUid: 1000
            enabled: true
            image:
              repository: hopsworks/hopsfs-mount
              tag: 3.4.3.3-EE-RC1-1
            mechanism: csi
            mountPath: /opt/hopsworks/mounts
            storeRoot: /apps/mountable-secrets
          testCoordinator:
            enabled: true
          userCatalogShards: 2
    ```

<div class="hops-values" markdown>

`global._hopsworks.trino.auth` <a class="headerlink" href="#helm.global._hopsworks.trino.auth" title="Permanent link">#</a> { #helm.global._hopsworks.trino.auth }
:   Type `object`, default `{"refreshPeriod":"5s"}`.
    How Trino authenticates, now that the password and group files live in HopsFS.

`global._hopsworks.trino.auth.refreshPeriod` <a class="headerlink" href="#helm.global._hopsworks.trino.auth.refreshPeriod" title="Permanent link">#</a> { #helm.global._hopsworks.trino.auth.refreshPeriod }
:   Type `string`, default `"5s"`.
    How often the coordinator re-reads password.db and group.db: the delay before a new project member can log in, and before a removed one is refused.

`global._hopsworks.trino.egressProbe` <a class="headerlink" href="#helm.global._hopsworks.trino.egressProbe" title="Permanent link">#</a> { #helm.global._hopsworks.trino.egressProbe }
:   Type `object`, default `{"echoUrl":""}`.
    Egress-address probe on the Trino pods. An init container prints the address the pod reaches the internet from, and the backend reads it back off the pod log so the catalog dialog can name the addresses to add to an external database's access control list. Nothing is stored: the log lives as long as the pod, and a terminated pod stops being listed.

`global._hopsworks.trino.egressProbe.echoUrl` <a class="headerlink" href="#helm.global._hopsworks.trino.egressProbe.echoUrl" title="Permanent link">#</a> { #helm.global._hopsworks.trino.egressProbe.echoUrl }
:   Type `string`, default `""`.
    URL of a service that echoes the caller's public IP address in its response body. **Empty by default, so the probe is opt-in**: it is the only outbound call this chart makes on its own, and a query engine reaching a third party on every pod start is not a default an on-premise cluster can be given without asking. While empty the init container prints `disabled` and exits without calling anything, the backend reports no addresses, and the catalog dialog tells the user to ask their administrator instead of naming them. Set it to turn the feature on: `https://ifconfig.me` and `https://api.ipify.org` both answer in the required shape, and an internal equivalent is preferable where one exists. The probe never fails a pod and never delays startup by more than its 5 second timeout.

`global._hopsworks.trino.enabled` <a class="headerlink" href="#helm.global._hopsworks.trino.enabled" title="Permanent link">#</a> { #helm.global._hopsworks.trino.enabled }
:   Type `bool`, default `true`.
    Enable or disable the installation of the trino sub chart.

`global._hopsworks.trino.files` <a class="headerlink" href="#helm.global._hopsworks.trino.files" title="Permanent link">#</a> { #helm.global._hopsworks.trino.files }
:   Type `object`.
    Trino's own platform files: password file, group file, access-control rules and user catalogs, as HopsFS files. No enable flag: Trino authenticates nobody without them. Delivered through the hopsfs-csi driver, so Trino requires global._hopsworks.csi.enabled.

    ??? note "Default"

        ```yaml
        csi:
          defaultPermissions: false
          fdSocketVolume: trino-files-fuse-fd
          sidecarGid: 1000
          sidecarUid: 1000
        mountPath: /opt/hopsworks/trino
        mountWaitSeconds: 300
        storeRoot: /apps/trino
        ```

`global._hopsworks.trino.files.csi` <a class="headerlink" href="#helm.global._hopsworks.trino.files.csi" title="Permanent link">#</a> { #helm.global._hopsworks.trino.files.csi }
:   Type `object`.
    Settings for the hopsfs-csi transport, separate from mountableSecrets.csi because the two mounts need separate fd-handoff sockets.

    ??? note "Default"

        ```yaml
        defaultPermissions: false
        fdSocketVolume: trino-files-fuse-fd
        sidecarGid: 1000
        sidecarUid: 1000
        ```

`global._hopsworks.trino.files.csi.defaultPermissions` <a class="headerlink" href="#helm.global._hopsworks.trino.files.csi.defaultPermissions" title="Permanent link">#</a> { #helm.global._hopsworks.trino.files.csi.defaultPermissions }
:   Type `bool`, default `false`.
    FUSE default_permissions. Off: the tree presents as root:root 0750 in the pod and Trino runs as 1000, so a kernel check makes every read EPERM. HopsFS still authorizes server-side as `trino`, and the mount is read-only.

`global._hopsworks.trino.files.csi.fdSocketVolume` <a class="headerlink" href="#helm.global._hopsworks.trino.files.csi.fdSocketVolume" title="Permanent link">#</a> { #helm.global._hopsworks.trino.files.csi.fdSocketVolume }
:   Type `string`, default `"trino-files-fuse-fd"`.
    Name of the pod emptyDir carrying this mount's fd-handoff socket. Must differ from mountableSecrets' `hopsfs-fuse-fd`, or every Trino pod sits in ContainerCreating. Checked by charts/trino.

`global._hopsworks.trino.files.csi.sidecarGid` <a class="headerlink" href="#helm.global._hopsworks.trino.files.csi.sidecarGid" title="Permanent link">#</a> { #helm.global._hopsworks.trino.files.csi.sidecarGid }
:   Type `int`, default `1000`.
    gid counterpart of sidecarUid.

`global._hopsworks.trino.files.csi.sidecarUid` <a class="headerlink" href="#helm.global._hopsworks.trino.files.csi.sidecarUid" title="Permanent link">#</a> { #helm.global._hopsworks.trino.files.csi.sidecarUid }
:   Type `int`, default `1000`.
    uid the node plugin chowns the fd-handoff socket to. Must equal the sidecar's literal runAsUser in charts/trino/values.yaml; charts/trino checks it.

`global._hopsworks.trino.files.mountPath` <a class="headerlink" href="#helm.global._hopsworks.trino.files.mountPath" title="Permanent link">#</a> { #helm.global._hopsworks.trino.files.mountPath }
:   Type `string`, default `"/opt/hopsworks/trino"`.
    Where the tree is mounted in the Trino pods, and the base of the paths in the password, group and access-control properties.

`global._hopsworks.trino.files.mountWaitSeconds` <a class="headerlink" href="#helm.global._hopsworks.trino.files.mountWaitSeconds" title="Permanent link">#</a> { #helm.global._hopsworks.trino.files.mountWaitSeconds }
:   Type `int`, default `300`.
    Seconds wait-trino-files waits for the mount to be served and seeded before failing the init container (kubelet then retries).

`global._hopsworks.trino.files.storeRoot` <a class="headerlink" href="#helm.global._hopsworks.trino.files.storeRoot" title="Permanent link">#</a> { #helm.global._hopsworks.trino.files.storeRoot }
:   Type `string`, default `"/apps/trino"`.
    Where the files live in HopsFS. Preset by charts/hopsfs, passed to the sidecar as `--srcDir` and seeded to the backend as `trino_files_path`. Moving it does not move existing files.

`global._hopsworks.trino.image` <a class="headerlink" href="#helm.global._hopsworks.trino.image" title="Permanent link">#</a> { #helm.global._hopsworks.trino.image }
:   Type `object`, default `{"tag":"483-v1"}`.
    The Trino image this release deploys, restated here for the backend.

`global._hopsworks.trino.image.tag` <a class="headerlink" href="#helm.global._hopsworks.trino.image.tag" title="Permanent link">#</a> { #helm.global._hopsworks.trino.image.tag }
:   Type `string`, default `"483-v1"`.
    The Trino image tag, seeded to the backend as `trino_image_tag` so it can tell when its connector-property table is stale. Duplicates trino.image.tag in charts/trino/values.yaml, which cannot be templated; charts/trino fails the render when they disagree. Bump both.

`global._hopsworks.trino.mountRetryTimeLimit` <a class="headerlink" href="#helm.global._hopsworks.trino.mountRetryTimeLimit" title="Permanent link">#</a> { #helm.global._hopsworks.trino.mountRetryTimeLimit }
:   Type `string`, default `"2m"`.
    `-retryTimeLimit` for both HopsFS sidecars in the Trino pods: how long one filesystem operation blocks while the client retries an unreachable namenode. Effectively a startup setting, since Trino reads an I/O error on its config files as "does not exist" and exits. 2m rides out a namenode container restart (measured 2m14s) and caps the dead time after a namenode pod replacement, which hopsfs-mount does not follow.

`global._hopsworks.trino.mountableSecrets` <a class="headerlink" href="#helm.global._hopsworks.trino.mountableSecrets" title="Permanent link">#</a> { #helm.global._hopsworks.trino.mountableSecrets }
:   Type `object`.
    Per-project credential files (Oracle wallets, keystores) delivered to the Trino pods, so a connector property can name a real directory. Named after the capability rather than the transport. They arrive through the hopsfs-csi driver, like the platform files.

    ??? note "Default"

        ```yaml
        csi:
          defaultPermissions: false
          sidecarGid: 1000
          sidecarUid: 1000
        enabled: true
        image:
          repository: hopsworks/hopsfs-mount
          tag: 3.4.3.3-EE-RC1-1
        mechanism: csi
        mountPath: /opt/hopsworks/mounts
        storeRoot: /apps/mountable-secrets
        ```

`global._hopsworks.trino.mountableSecrets.csi` <a class="headerlink" href="#helm.global._hopsworks.trino.mountableSecrets.csi" title="Permanent link">#</a> { #helm.global._hopsworks.trino.mountableSecrets.csi }
:   Type `object`, default `{"defaultPermissions":false,"sidecarGid":1000,"sidecarUid":1000}`.
    Settings for the hopsfs-csi transport: the identity the node plugin hands the mount to.

`global._hopsworks.trino.mountableSecrets.csi.defaultPermissions` <a class="headerlink" href="#helm.global._hopsworks.trino.mountableSecrets.csi.defaultPermissions" title="Permanent link">#</a> { #helm.global._hopsworks.trino.mountableSecrets.csi.defaultPermissions }
:   Type `bool`, default `false`.
    Whether the kernel checks the file modes hopsfs-mount reports (FUSE default_permissions). Off for this mount: the readers are the Trino containers, whose uid is not a user in the sidecar image, and the tree's owners are backend service users that never resolve there either, so a kernel-side check can only refuse. The mount is read-only at the kernel and bounded to storeRoot, and HopsFS still enforces its own permissions server-side as the authenticated `trino` user, so nothing is lost by turning it off.

`global._hopsworks.trino.mountableSecrets.csi.sidecarGid` <a class="headerlink" href="#helm.global._hopsworks.trino.mountableSecrets.csi.sidecarGid" title="Permanent link">#</a> { #helm.global._hopsworks.trino.mountableSecrets.csi.sidecarGid }
:   Type `int`, default `1000`.
    gid the node plugin records on the FUSE mount and chowns the socket to; the sidecar's runAsGroup, with the same constraints as sidecarUid.

`global._hopsworks.trino.mountableSecrets.csi.sidecarUid` <a class="headerlink" href="#helm.global._hopsworks.trino.mountableSecrets.csi.sidecarUid" title="Permanent link">#</a> { #helm.global._hopsworks.trino.mountableSecrets.csi.sidecarUid }
:   Type `int`, default `1000`.
    uid the node plugin records on the FUSE mount and chowns the fd-handoff socket to. The sidecar in charts/trino/values.yaml MUST run as exactly this uid: runAsUser is an integer the upstream chart does not template, so it is a literal there, restated on OpenShift with an id from the namespace range (values.openshift.yaml), and charts/trino fails the render when the two differ. 1000 is the Trino user, so the pod has one identity.

`global._hopsworks.trino.mountableSecrets.enabled` <a class="headerlink" href="#helm.global._hopsworks.trino.mountableSecrets.enabled" title="Permanent link">#</a> { #helm.global._hopsworks.trino.mountableSecrets.enabled }
:   Type `bool`, default `true`.
    Whether the Trino pods are given the backend-owned /apps/mountable-secrets tree at all. This is trino's own declaration of intent. When false the backend variable mountable_secrets_enabled is unset, the feature is reported unavailable, and the sidecar entries must be removed from charts/trino/values.yaml and the `mountable-secrets` volume restated as an emptyDir (charts/trino fails the render otherwise: neither can be omitted by a conditional, since values.yaml is not templated by Helm, and a CSI volume left behind with no sidecar to serve it is a mount whose every access blocks forever).

`global._hopsworks.trino.mountableSecrets.image.repository` <a class="headerlink" href="#helm.global._hopsworks.trino.mountableSecrets.image.repository" title="Permanent link">#</a> { #helm.global._hopsworks.trino.mountableSecrets.image.repository }
:   Type `string`, default `"hopsworks/hopsfs-mount"`.
    Repository of the small bash image the Trino init containers wait-trino-files and assemble-catalogs run in. The dedicated hopsfs-mount image built in docker-images (90.8 MB); the mount sidecars themselves run global._hopsworks.csi.image.

`global._hopsworks.trino.mountableSecrets.image.tag` <a class="headerlink" href="#helm.global._hopsworks.trino.mountableSecrets.image.tag" title="Permanent link">#</a> { #helm.global._hopsworks.trino.mountableSecrets.image.tag }
:   Type `string`, default `"3.4.3.3-EE-RC1-1"`.
    Tag for the sidecar image, `<artifact version>-<image fix>`. The first half is the hops-fuse-mount artifact version, not the platform version: the image carries the HopsFS FUSE client and nothing else, so it turns over with HopsFS. Keep that half in step with charts/hopsfs image.tag, since the FUSE client should match the HopsFS line it talks to. The second half moves when the image is rebuilt without the artifact changing, a base bump or a security rebuild, so such a rebuild cannot silently replace the bytes behind a tag already deployed. Both halves are pinned here on purpose.

`global._hopsworks.trino.mountableSecrets.mountPath` <a class="headerlink" href="#helm.global._hopsworks.trino.mountableSecrets.mountPath" title="Permanent link">#</a> { #helm.global._hopsworks.trino.mountableSecrets.mountPath }
:   Type `string`, default `"/opt/hopsworks/mounts"`.
    Where the tree is mounted inside the Trino pods. Seeded to the backend as the `trino_mountable_secrets_root` variable and used for the sidecar's mount point, its preStop unmount and the Trino containers' mount, so one value drives both sides. They agreed only by both defaulting to the same literal before, which meant an operator moving the mount left the backend resolving `${HOPSWORKS_MOUNT:...}` under a path nothing was mounted at.

`global._hopsworks.trino.mountableSecrets.storeRoot` <a class="headerlink" href="#helm.global._hopsworks.trino.mountableSecrets.storeRoot" title="Permanent link">#</a> { #helm.global._hopsworks.trino.mountableSecrets.storeRoot }
:   Type `string`, default `"/apps/mountable-secrets"`.
    Where the store lives in HopsFS, the source side of the mount. One value, three consumers: charts/hopsfs presets the directory, the mount sidecar passes it as `--srcDir`, and it is seeded to the backend as the `mountable_secrets_path` variable so the backend writes bundles where the mount reads them. It was a literal in all three places before, agreeing only by coincidence, which is the trap `mountPath` had on the container side. Not a knob to reach for: moving it does not move the bundles already written under the old path, and the tree is backend-owned (payara:hdfs, 0750) rather than operator-managed.

`global._hopsworks.trino.testCoordinator` <a class="headerlink" href="#helm.global._hopsworks.trino.testCoordinator" title="Permanent link">#</a> { #helm.global._hopsworks.trino.testCoordinator }
:   Type `object`, default `{"enabled":true}`.
    Optional dedicated Trino test coordinator used to connection-test user catalogs before they are synced to the production coordinator.

`global._hopsworks.trino.testCoordinator.enabled` <a class="headerlink" href="#helm.global._hopsworks.trino.testCoordinator.enabled" title="Permanent link">#</a> { #helm.global._hopsworks.trino.testCoordinator.enabled }
:   Type `bool`, default `true`.
    Deploy an optional dedicated Trino coordinator (catalog.management=dynamic, writable catalog dir) used to connection-test user catalogs before syncing them to the production coordinator. When true, the backend variable trino_test_coordinator_enabled is set so the "test connection" feature becomes available. Enabled by default; set to false to skip the extra coordinator (the "test connection" action is then reported unavailable).

`global._hopsworks.trino.mountableSecrets.mechanism` <span class="hops-values-deprecated">Deprecated</span> <a class="headerlink" href="#helm.global._hopsworks.trino.mountableSecrets.mechanism" title="Permanent link">#</a> { #helm.global._hopsworks.trino.mountableSecrets.mechanism }
:   Type `string`, default `"csi"`.
    DEPRECATED and read by nothing. Selected between the hopsfs-csi transport and the privileged `hopsfsMount` sidecar; the sidecar is gone and Trino requires global._hopsworks.csi.enabled. Kept only so an override carried from 5.1 still validates.

`global._hopsworks.trino.userCatalogShards` <span class="hops-values-deprecated">Deprecated</span> <a class="headerlink" href="#helm.global._hopsworks.trino.userCatalogShards" title="Permanent link">#</a> { #helm.global._hopsworks.trino.userCatalogShards }
:   Type `int`, default `2`.
    DEPRECATED and read by nothing: user catalogs are HopsFS files now, not sharded Secrets. Kept so an existing override still validates.

</div>

<!-- END GENERATED VALUES -->
