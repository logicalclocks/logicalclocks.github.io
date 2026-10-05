# Helm chart values reference

This page lists every value you can configure when deploying Hopsworks with the Hopsworks Helm chart.
It is generated from the `README.md` files of the chart and its subcharts.
On a released version of the docs it matches the Hopsworks Helm chart for that release; on the development docs it reflects the latest chart published to the development channel.

You set these values in the `values.<cloud>.yaml` file that you pass to `helm install`.
For a guided, end-to-end setup, follow one of the cloud installation guides, such as the [AWS getting started guide][aws-getting-started-with-eks].
Only a small subset of these values is needed for a typical install; the table below is the exhaustive reference.

## Configuration values

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.2.0-alpha-1791182654` (Hopsworks `5.2.0`)._

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| global._hopsworks.airflow.enabled | bool | `true` | Enable or disable the installation of the airflow sub chart |
| global._hopsworks.airflow.keysSecretName | string | `"hopsworks-airflow-keys"` | Name of the Secret holding the shared-bearer secret that hopsworks-instance uses to call the Airflow `/auth/internal/*` routes. Must match airflow.airflowApi.keysSecretName so the same Secret is mounted on both sides. The default `airflow-webserver-airflow-crypto-material` is the cert-only secret and does NOT contain `internal-shared-secret`, so the hopsworks-instance pod fails to mount on a fresh v3 install. |
| global._hopsworks.airflowApiKeySecretName | string | `"airflow-api-key"` |  |
| global._hopsworks.autoscalers | object | `{}` | Map of autoscaler name to VPA configuration. Each key becomes a VerticalPodAutoscaler resource named <key>-vpa. |
| global._hopsworks.backups | object | `{"enabled":true,"metadataStore":{"configMap":{"opensearch":"opensearch-backups-metadata","ronDB":"rondb-backups-metadata","superset":"superset-backups-metadata"}},"schedule":"@weekly","ttl":null}` | enable global backups configuration |
| global._hopsworks.backups.enabled | bool | `true` | enable global backup |
| global._hopsworks.backups.metadataStore | object | `{"configMap":{"opensearch":"opensearch-backups-metadata","ronDB":"rondb-backups-metadata","superset":"superset-backups-metadata"}}` | backups metadata store |
| global._hopsworks.backups.metadataStore.configMap.opensearch | string | `"opensearch-backups-metadata"` | name of the configmap to store metadata information about opensearch backups |
| global._hopsworks.backups.metadataStore.configMap.ronDB | string | `"rondb-backups-metadata"` | name of the configmap to store metadata information about rondb backups  |
| global._hopsworks.backups.metadataStore.configMap.superset | string | `"superset-backups-metadata"` | name of the configmap to store metadata information about superset backups |
| global._hopsworks.backups.schedule | string | `"@weekly"` | cron schedule |
| global._hopsworks.backups.ttl | string | `nil` | time to live to control when to clean up backups. It is a number followed by either d (days) or h (hours) suffix. |
| global._hopsworks.buildkitd.enabled | bool | `false` |  |
| global._hopsworks.centralNamespace | string | `"hopsworks"` | Namespace to fetch OLK signing key from. Set to null to generate a new key. |
| global._hopsworks.cloudProvider | string | `""` | cloud provider (AWS, AZURE, GCP, OVH). It is used by HopsFS, Consul, and Hopsworks. Hopsfs uses it to configure the object storage parameters. Consul uses it to configure coredns accordingly. Hopsworks uses it to determine how to store the users docker images within the same hopsworks-base repo as tags or in different repo per project, If cloud provider is set all the users docker images are stored as tags - it is an AWS limitation where only tags within the repo can share layers. |
| global._hopsworks.consulDomainName | string | `"consul"` | The domain name for consul where it will answer DNS queries, e.g. `service-name.service.consul`. If changed, make sure to update consul.consul.global.domain to the same value. |
| global._hopsworks.csi | object | `{"driverName":"","enabled":true,"image":{"pullPolicy":"IfNotPresent","repository":"hopsworks/hopsfs-csi","tag":"0.1.0-SNAPSHOT"}}` | HopsFS CSI integration: the hopsfs-csi node plugin FUSE-mounts an inline ephemeral volume on every HopsFS-mounting pod (Hopsworks-generated workloads, Airflow, Trino) and hands the descriptor to an unprivileged `hopsfs-fuse` native sidecar in the pod, so no workload container is privileged. `enabled` installs the hopsfs-csi DaemonSet and CSIDriver and seeds `csi_driver_enabled` to the backend; requires Kubernetes >= 1.29 (native sidecars), which the render enforces with a message naming this value. Set it to false to keep the legacy privileged in-container HopsFS mount everywhere. Known limitation: a crashed `hopsfs-fuse` sidecar leaves that pod's mount dead (I/O fails with ENOTCONN) until the pod is recreated; there is no self-heal. `image` is the ONE place the hopsfs-csi image is named: the node plugin, the Airflow and Trino sidecars and the backend `csi_sidecar_image` variable are all built from `imageRegistry` + this block, because the fusermount3 proxy in the sidecar and the fd server in the plugin are two halves of one protocol and must never drift on a node. Pin a release tag here before GA. |
| global._hopsworks.csi.driverName | string | `""` | The CSI driver name of this release. Empty (the default) derives `<namespace>.hopsfs.csi.logicalclocks.com` from the release namespace, one name per release, which is what lets two Hopsworks installs share a cluster: kubelet routes CSI calls by driver name alone, so each release gets its own node plugin, socket, registration and CSIDriver object, also on nodes both installs use, and uninstalling one never touches the other's mounts (HWORKS-3297). Kubernetes caps a CSI driver name at 63 characters, so a namespace longer than 34 characters must set a shorter name here. Any name set here must be unique in the cluster: two releases on one name share one socket directory and one kubelet registration on every node they share, so neither is isolated from the other, which is the fault the per-release name removes; that is not a supported setup. Whatever the name, it is computed once (`hopsworkslib.csiDriverName`) for the plugin, the Airflow and Trino volumes and the backend `csi_driver_name` variable, so nothing can drift. |
| global._hopsworks.executor_uid | int | `1235` | User ID for the user running Hopsworks and Airflow containers |
| global._hopsworks.externalLoadBalancers | object | `{"annotations":{},"class":null,"enabled":true,"managed":true}` | Global load balancer configuration for external access to Hopsworks services: ArrowFlight, Kafka, and MySQL We fallback to this loadBalancerClass if the local loadBalancerClass is not defined |
| global._hopsworks.externalLoadBalancers.annotations | object | `{}` | Generic annotations attached to LoadBalancer objects |
| global._hopsworks.externalLoadBalancers.class | string | `nil` | Name of the LoadBalancer class |
| global._hopsworks.externalLoadBalancers.enabled | bool | `true` | Enable LoadBalancer Services |
| global._hopsworks.externalLoadBalancers.managed | bool | `true` | Cloud provider provisions Load Balancers |
| global._hopsworks.externalServices | object | `{"hopsfs":{"external":false,"namenodeAddresses":[]},"opensearch":{"addresses":[],"external":false},"prometheus":{"addresses":[],"external":false},"rondb":{"external":false,"mgmdHostname":""}}` | Configuration for when services are external to this Kubernetes installation |
| global._hopsworks.externalServices.hopsfs | object | `{"external":false,"namenodeAddresses":[]}` | HopsFS configuration when it is installed externally |
| global._hopsworks.externalServices.hopsfs.external | bool | `false` | Flag to indicate HopsFS is installed externally |
| global._hopsworks.externalServices.hopsfs.namenodeAddresses | list | `[]` | IP addresses where HopsFS Namenodes are installed |
| global._hopsworks.externalServices.opensearch | object | `{"addresses":[],"external":false}` | Opensearch configuration when it is installed externally |
| global._hopsworks.externalServices.opensearch.addresses | list | `[]` | IP addresses where OpenSearch is installed |
| global._hopsworks.externalServices.opensearch.external | bool | `false` | Flag to indicate Opensearch is installed externally |
| global._hopsworks.externalServices.prometheus | object | `{"addresses":[],"external":false}` | prometheus configuration when it is installed externally |
| global._hopsworks.externalServices.prometheus.addresses | list | `[]` | IP addresses where prometheus is installed |
| global._hopsworks.externalServices.prometheus.external | bool | `false` | Flag to indicate prometheus is installed externally |
| global._hopsworks.externalServices.rondb | object | `{"external":false,"mgmdHostname":""}` | RonDB configuration when it is installed externally |
| global._hopsworks.externalServices.rondb.external | bool | `false` | Flag to indicate RonDB is installed externally |
| global._hopsworks.externalServices.rondb.mgmdHostname | string | `""` | Hostname of the machine where RonDB management service is running |
| global._hopsworks.full_platform | bool | `true` | Flag to indicate if the full platform is installed or just the online feature store infrastructure |
| global._hopsworks.grafana.extraDashboardProviders | list | `[]` | Extra Grafana dashboard providers, appended to the provider file the grafana chart renders. The dashboards themselves ship in the Grafana image, so this is the way to provision one without rebuilding the image: mount it (for example through `grafana.grafana.dashboardsConfigMaps`, which lands at /var/lib/grafana/dashboards/<key>) and point a provider at the mount path. Entries are Grafana provider objects, so each needs at least `name`, `folder`, `type: file` and `options.path`; provider names must be unique across all providers. Paths under /usr/share/grafana/dashboards are the image's own and are verified by the verify-dashboards init container, so point elsewhere. Setting this changes the provider ConfigMap's content hash, which rolls the Grafana pod. |
| global._hopsworks.imagePullPolicy | string | `"IfNotPresent"` |  |
| global._hopsworks.imagePullSecrets | list | `[]` | image pull secrets to be used by all the subcharts. Notice that for subcharts the have external dependices, you need to update the image pull secrets accordingly in those subcharts |
| global._hopsworks.imageRegistry | string | `"docker.hops.works"` |  |
| global._hopsworks.initContainerResources | object | `{"runtime":{"limits":{"cpu":1,"memory":"1Gi"},"requests":{"cpu":"250m","memory":"512Mi"}},"tool":{"limits":{"cpu":"500m","memory":"512Mi"},"requests":{"cpu":"100m","memory":"128Mi"}},"waiter":{"limits":{"cpu":"500m","memory":"256Mi"},"requests":{"cpu":"50m","memory":"64Mi"}}}` | Resource requests and limits for the chart's init containers, in three tiers by what the container does: `waiter` for shell wait loops, `tool` for file copies and small binaries, `runtime` for anything starting a JVM or a Python interpreter or pulling images. Every init container declares both requests and limits. A namespace `LimitRange` that supplies a `default` limit injects it into any container declaring none, and a pod's effective request is `max(sum of app containers, highest single init container)` where the init term is a floor for the pod's whole lifetime. An init container without resources can therefore pin a node's allocatable to the `LimitRange` default even after it has exited. Retune these if the target namespace has a `LimitRange` whose `min`/`max` would reject the defaults, since an out-of-range explicit value is rejected rather than defaulted. |
| global._hopsworks.jobs | object | `{"ttlSecondsAfterFinished":86400}` | Global configuration for Kubernetes Jobs created by the chart |
| global._hopsworks.jobs.ttlSecondsAfterFinished | int | `86400` | Time in seconds after a finished Job is eligible for automatic cleanup. Applies to all Jobs unless overridden by a subchart-specific ttlSecondsAfterFinished value. |
| global._hopsworks.kafka.enabled | bool | `true` | Enable or disable the installation of the kafka sub chart. |
| global._hopsworks.kueue.enabled | bool | `false` |  |
| global._hopsworks.kyverno.enabled | bool | `false` | Enable or disable kyverno policies installation |
| global._hopsworks.kyverno.policies.addCertificatesVolume | object | `{"enabled":false,"initContainers":{"annotation":{"key":"kyverno-inject-certs-init","value":"enabled"},"enabled":false},"mountPath":"/etc/ssl/certs","preconditions":{"annotation":{"key":"kyverno-inject-certs","value":"enabled"},"enabled":true}}` | Configuration to add custom certificates to pods as a mounted volume |
| global._hopsworks.kyverno.policies.addCertificatesVolume.enabled | bool | `false` | Enable add certificates volume |
| global._hopsworks.kyverno.policies.addCertificatesVolume.initContainers | object | `{"annotation":{"key":"kyverno-inject-certs-init","value":"enabled"},"enabled":false}` | Opt-in for injecting the certificates volume into init containers. The main addCertificatesVolume policy only mutates spec.containers; init containers are intentionally left untouched because they are often injected by third-party operators (Istio, KServe, sidecar injectors) that ship minimal images where overwriting /etc/ssl/certs would break them. When enabled, a second mutate rule is rendered that iterates spec.initContainers and is gated by an OR of the dedicated init-container annotation below and any extraAnnotations / labels configured under the hw-kyverno subchart at policies.addCertificatesVolume.initContainers. The annotation is distinct from preconditions.annotation so authors can opt main containers and init containers in independently. |
| global._hopsworks.kyverno.policies.addCertificatesVolume.initContainers.annotation | object | `{"key":"kyverno-inject-certs-init","value":"enabled"}` | The key and value of the annotation used to opt a pod's init containers into certificate volume injection. Distinct from preconditions.annotation so authors can opt main containers and init containers in independently. A pod opts in by matching any one of: this annotation, an entry in the hw-kyverno subchart's policies.addCertificatesVolume.initContainers.extraAnnotations, or an entry in policies.addCertificatesVolume.initContainers.labels. |
| global._hopsworks.kyverno.policies.addCertificatesVolume.initContainers.enabled | bool | `false` | Render the init-container mutate rule. When false (default), the policy never touches init containers regardless of any annotation, label, or extra annotation set on a pod. |
| global._hopsworks.kyverno.policies.addCertificatesVolume.mountPath | string | `"/etc/ssl/certs"` | Path to mount the certificates volume |
| global._hopsworks.kyverno.policies.addCertificatesVolume.preconditions.annotation | object | `{"key":"kyverno-inject-certs","value":"enabled"}` | The key and value of the annotation used to inject kyverno certificates. If a pod has this annotation, it will be mutated. There are other options under hw-kyverno subchart to use labels and extra annotations as needed. |
| global._hopsworks.kyverno.policies.addCertificatesVolume.preconditions.enabled | bool | `true` | Enable adding preconditions to the police. If disabled, the policy will apply to all the pods in the installation namespace and the hopsworks projects' namespaces created when crating a project. |
| global._hopsworks.managedDockerRegistery | object | `{"credHelper":{"enabled":false,"secretName":""},"domain":"","enabled":false,"namespace":"","port":null}` | configure managed docker registry for Hopsworks to store the user's docker image |
| global._hopsworks.managedDockerRegistery.credHelper | object | `{"enabled":false,"secretName":""}` | credentials helper to use for the managed docker registry. We only support cred helpers for [AWS](https://github.com/awslabs/amazon-ecr-credential-helper) and [GCP](https://github.com/GoogleCloudPlatform/docker-credential-gcr) |
| global._hopsworks.managedDockerRegistery.credHelper.secretName | string | `""` | the name of the secret to be created with the credentials helper configuration |
| global._hopsworks.managedDockerRegistery.domain | string | `""` | the managed docker registry domain name |
| global._hopsworks.managedDockerRegistery.namespace | string | `""` | the namespace to be used |
| global._hopsworks.managedDockerRegistery.port | string | `nil` | port number for the managed docker registry  |
| global._hopsworks.managedObjectStorage | object | `{"enabled":false,"s3":null}` | Configuration for managed object storage to be used by HopsFS, Opensearch, RonDB, and Hopsworks. Opensearch and RonDB uses this configuration to setup a remote sink for their backup, if a different remote sink is configured on the subchart then it will take precedence. Hopsworks uses the bucket configuration as context cache when building users' docker images, only S3 is supported at the moment. |
| global._hopsworks.managedObjectStorage.s3 | string | `nil` | S3 configuration |
| global._hopsworks.minio.enabled | bool | `true` |  |
| global._hopsworks.minio.hopsfs.bucket | string | `"hopsfs"` |  |
| global._hopsworks.minio.hopsfs.enabled | bool | `true` |  |
| global._hopsworks.minio.password | string | `"minioadmin"` |  |
| global._hopsworks.minio.region | string | `"eu-west-1"` |  |
| global._hopsworks.minio.user | string | `"minioadmin"` |  |
| global._hopsworks.mode | string | `"auto"` | Helm installation model. "auto" lets the chart decide based on the Release.IsInstall value. "install" forces installation mode, while "upgrade" forces upgrade mode. |
| global._hopsworks.mysql.hopsworksUser | string | `"hopsworksroot"` |  |
| global._hopsworks.mysql.usersSecretname | string | `"mysql-users-secrets"` |  |
| global._hopsworks.networkPolicy.rondbAccessLabels.access | string | `"mgmd-and-ndbmtd"` |  |
| global._hopsworks.nodeSelector | object | `{}` | Specifies the global nodeSelector settings applied across all subcharts unless explicitly overridden within a specific subchart. This ensures Kubernetes schedules Pods only onto nodes that match all the specified labels. Notice that some subcharts do not use this global variable, and you must manually override those by defining them in the values.yaml file, using anchors if necessary. |
| global._hopsworks.onlinefs.email | string | `"onlinefs@hopsworks.ai"` |  |
| global._hopsworks.onlinefs.password | string | `"onlinefspw"` |  |
| global._hopsworks.opensearch | object | `{"enabled":true}` | Enable or disable the opensearch |
| global._hopsworks.opensearch.enabled | bool | `true` | Enable or disable the opensearch |
| global._hopsworks.openshift.enabled | bool | `false` | Enable when installing on Openshift platform |
| global._hopsworks.ray.enabled | bool | `false` |  |
| global._hopsworks.restoreFromBackup | object | `{"backupId":null,"forceDataClear":false,"inPlace":false,"superset":{"activeDeadlineSeconds":14400,"backupId":null,"enabled":false,"initiatedBy":null}}` | restore cluster from a backup id |
| global._hopsworks.restoreFromBackup.backupId | string | `nil` | the backup id to restore |
| global._hopsworks.restoreFromBackup.forceDataClear | bool | `false` | flag to indicate if the data should be forcibly cleared before restore |
| global._hopsworks.restoreFromBackup.inPlace | bool | `false` | flag to indicate if the restore should be done in-place or to a new cluster |
| global._hopsworks.restoreFromBackup.superset | object | `{"activeDeadlineSeconds":14400,"backupId":null,"enabled":false,"initiatedBy":null}` | Superset database restore (HWORKS-2973). Set enabled and backupId, add values.superset-restore.yaml to hold Superset at zero replicas, and upgrade; when the superset-restore-<backupId> Job has completed, remove the file, set enabled=false and upgrade again. |
| global._hopsworks.restoreFromBackup.superset.activeDeadlineSeconds | int | `14400` | activeDeadlineSeconds for the restore Job, bounding the wait for the Superset pods and the secret key, the download and the reload |
| global._hopsworks.restoreFromBackup.superset.backupId | string | `nil` | the Superset backup id to restore (a key in the superset-backups-metadata ConfigMap). Required when enabled |
| global._hopsworks.restoreFromBackup.superset.enabled | bool | `false` | reload the Superset database from a backup |
| global._hopsworks.restoreFromBackup.superset.initiatedBy | string | `nil` | who initiated this restore, recorded in the superset-restore-audit ConfigMap. Defaults to helm/<release>@rev<revision>. Deployment metadata, not an authenticated identity: the Kubernetes audit log has the actor |
| global._hopsworks.security.tls.enabled | bool | `true` |  |
| global._hopsworks.securityContextEnabled | bool | `true` | Flag to disable templating SecurityContext for Openshift |
| global._hopsworks.serviceAccount.annotations | object | `{}` | custom annotations for the Hopsworks service account |
| global._hopsworks.serviceAccount.create | bool | `true` |  |
| global._hopsworks.serviceAccount.name | string | `"hopsworks-service-account"` |  |
| global._hopsworks.serviceAccountAnnotations | object | `{}` | Use it to annotate the serviceAccounts we create for Hopsworks |
| global._hopsworks.skipDatabaseMigration | bool | `false` | Special flag which MUST be used only for 3.x -> 4.0 migrations (HWORKS-1600) |
| global._hopsworks.spark.history.enabled | bool | `true` | Enable or disable installing of the spark history server |
| global._hopsworks.storageClassName | string | `nil` | global storage class name |
| global._hopsworks.superset.enabled | bool | `true` | Enable or disable the installation of the superset sub chart. |
| global._hopsworks.superset.mysql.enabled | bool | `true` | Enable or disable MySQL for Superset. Must match superset.mysql.enabled for consistent behavior across charts. |
| global._hopsworks.superset.redis.enabled | bool | `true` | Enable or disable Redis for Superset. Must match superset.superset.redis.enabled for consistent behavior across charts. |
| global._hopsworks.tolerations | list | `[]` | Specifies the global tolerations settings applied to all subcharts unless explicitly overridden in a specific subchart. These tolerations allow Kubernetes to schedule Pods on nodes with matching taints, ensuring proper placement based on cluster policies.  Notice that some subcharts do not use this global variable, and you must manually override those by defining them in the values.yaml file, using anchors if necessary. |
| global._hopsworks.toolbox.image | string | `"hwutils"` |  |
| global._hopsworks.toolbox.tag | string | `"1.10-SNAPSHOT"` |  |
| global._hopsworks.topologySpreadConstraint | object | `{"maxSkew":1,"nodeAffinityPolicy":"Honor","nodeTaintsPolicy":"Honor","topologyKey":"topology.kubernetes.io/zone","whenUnsatisfiable":"ScheduleAnyway"}` | default topology spread constraint. If not defined the global topology spread constraint would be used |
| global._hopsworks.trino.auth | object | `{"refreshPeriod":"5s"}` | How Trino authenticates, now that the password and group files live in HopsFS. |
| global._hopsworks.trino.auth.refreshPeriod | string | `"5s"` | How often the coordinator re-reads password.db and group.db: the delay before a new project member can log in, and before a removed one is refused. |
| global._hopsworks.trino.egressProbe | object | `{"echoUrl":""}` | Egress-address probe on the Trino pods. An init container prints the address the pod reaches the internet from, and the backend reads it back off the pod log so the catalog dialog can name the addresses to add to an external database's access control list. Nothing is stored: the log lives as long as the pod, and a terminated pod stops being listed. |
| global._hopsworks.trino.egressProbe.echoUrl | string | `""` | URL of a service that echoes the caller's public IP address in its response body. **Empty by default, so the probe is opt-in**: it is the only outbound call this chart makes on its own, and a query engine reaching a third party on every pod start is not a default an on-premise cluster can be given without asking. While empty the init container prints `disabled` and exits without calling anything, the backend reports no addresses, and the catalog dialog tells the user to ask their administrator instead of naming them. Set it to turn the feature on: `https://ifconfig.me` and `https://api.ipify.org` both answer in the required shape, and an internal equivalent is preferable where one exists. The probe never fails a pod and never delays startup by more than its 5 second timeout. |
| global._hopsworks.trino.enabled | bool | `true` | Enable or disable the installation of the trino sub chart. |
| global._hopsworks.trino.files | object | `{"csi":{"defaultPermissions":false,"fdSocketVolume":"trino-files-fuse-fd","sidecarGid":1000,"sidecarUid":1000},"mountPath":"/opt/hopsworks/trino","mountWaitSeconds":300,"storeRoot":"/apps/trino"}` | Trino's own platform files: password file, group file, access-control rules and user catalogs, as HopsFS files. No enable flag: Trino authenticates nobody without them. Delivered through the hopsfs-csi driver, so Trino requires global._hopsworks.csi.enabled. |
| global._hopsworks.trino.files.csi | object | `{"defaultPermissions":false,"fdSocketVolume":"trino-files-fuse-fd","sidecarGid":1000,"sidecarUid":1000}` | Settings for the hopsfs-csi transport, separate from mountableSecrets.csi because the two mounts need separate fd-handoff sockets. |
| global._hopsworks.trino.files.csi.defaultPermissions | bool | `false` | FUSE default_permissions. Off: the tree presents as root:root 0750 in the pod and Trino runs as 1000, so a kernel check makes every read EPERM. HopsFS still authorizes server-side as `trino`, and the mount is read-only. |
| global._hopsworks.trino.files.csi.fdSocketVolume | string | `"trino-files-fuse-fd"` | Name of the pod emptyDir carrying this mount's fd-handoff socket. Must differ from mountableSecrets' `hopsfs-fuse-fd`, or every Trino pod sits in ContainerCreating. Checked by charts/trino. |
| global._hopsworks.trino.files.csi.sidecarGid | int | `1000` | gid counterpart of sidecarUid. |
| global._hopsworks.trino.files.csi.sidecarUid | int | `1000` | uid the node plugin chowns the fd-handoff socket to. Must equal the sidecar's literal runAsUser in charts/trino/values.yaml; charts/trino checks it. |
| global._hopsworks.trino.files.mountPath | string | `"/opt/hopsworks/trino"` | Where the tree is mounted in the Trino pods, and the base of the paths in the password, group and access-control properties. |
| global._hopsworks.trino.files.mountWaitSeconds | int | `300` | Seconds wait-trino-files waits for the mount to be served and seeded before failing the init container (kubelet then retries). |
| global._hopsworks.trino.files.storeRoot | string | `"/apps/trino"` | Where the files live in HopsFS. Preset by charts/hopsfs, passed to the sidecar as `--srcDir` and seeded to the backend as `trino_files_path`. Moving it does not move existing files. |
| global._hopsworks.trino.image | object | `{"tag":"483-v1"}` | The Trino image this release deploys, restated here for the backend. |
| global._hopsworks.trino.image.tag | string | `"483-v1"` | The Trino image tag, seeded to the backend as `trino_image_tag` so it can tell when its connector-property table is stale. Duplicates trino.image.tag in charts/trino/values.yaml, which cannot be templated; charts/trino fails the render when they disagree. Bump both. |
| global._hopsworks.trino.mountRetryTimeLimit | string | `"2m"` | `-retryTimeLimit` for both HopsFS sidecars in the Trino pods: how long one filesystem operation blocks while the client retries an unreachable namenode. Effectively a startup setting, since Trino reads an I/O error on its config files as "does not exist" and exits. 2m rides out a namenode container restart (measured 2m14s) and caps the dead time after a namenode pod replacement, which hopsfs-mount does not follow. |
| global._hopsworks.trino.mountableSecrets | object | `{"csi":{"defaultPermissions":false,"sidecarGid":1000,"sidecarUid":1000},"enabled":true,"image":{"repository":"hopsworks/hopsfs-mount","tag":"3.4.3.3-EE-RC0-1"},"mechanism":"csi","mountPath":"/opt/hopsworks/mounts","storeRoot":"/apps/mountable-secrets"}` | Per-project credential files (Oracle wallets, keystores) delivered to the Trino pods, so a connector property can name a real directory. Named after the capability rather than the transport. They arrive through the hopsfs-csi driver, like the platform files. |
| global._hopsworks.trino.mountableSecrets.csi | object | `{"defaultPermissions":false,"sidecarGid":1000,"sidecarUid":1000}` | Settings for the hopsfs-csi transport: the identity the node plugin hands the mount to. |
| global._hopsworks.trino.mountableSecrets.csi.defaultPermissions | bool | `false` | Whether the kernel checks the file modes hopsfs-mount reports (FUSE default_permissions). Off for this mount: the readers are the Trino containers, whose uid is not a user in the sidecar image, and the tree's owners are backend service users that never resolve there either, so a kernel-side check can only refuse. The mount is read-only at the kernel and bounded to storeRoot, and HopsFS still enforces its own permissions server-side as the authenticated `trino` user, so nothing is lost by turning it off. |
| global._hopsworks.trino.mountableSecrets.csi.sidecarGid | int | `1000` | gid the node plugin records on the FUSE mount and chowns the socket to; the sidecar's runAsGroup, with the same constraints as sidecarUid. |
| global._hopsworks.trino.mountableSecrets.csi.sidecarUid | int | `1000` | uid the node plugin records on the FUSE mount and chowns the fd-handoff socket to. The sidecar in charts/trino/values.yaml MUST run as exactly this uid: runAsUser is an integer the upstream chart does not template, so it is a literal there, restated on OpenShift with an id from the namespace range (values.openshift.yaml), and charts/trino fails the render when the two differ. 1000 is the Trino user, so the pod has one identity. |
| global._hopsworks.trino.mountableSecrets.enabled | bool | `true` | Whether the Trino pods are given the backend-owned /apps/mountable-secrets tree at all. This is trino's own declaration of intent. When false the backend variable mountable_secrets_enabled is unset, the feature is reported unavailable, and the sidecar entries must be removed from charts/trino/values.yaml and the `mountable-secrets` volume restated as an emptyDir (charts/trino fails the render otherwise: neither can be omitted by a conditional, since values.yaml is not templated by Helm, and a CSI volume left behind with no sidecar to serve it is a mount whose every access blocks forever). |
| global._hopsworks.trino.mountableSecrets.image.repository | string | `"hopsworks/hopsfs-mount"` | Repository of the small bash image the Trino init containers wait-trino-files and assemble-catalogs run in. The dedicated hopsfs-mount image built in docker-images (90.8 MB); the mount sidecars themselves run global._hopsworks.csi.image. |
| global._hopsworks.trino.mountableSecrets.image.tag | string | `"3.4.3.3-EE-RC0-1"` | Tag for the sidecar image, `<artifact version>-<image fix>`. The first half is the hops-fuse-mount artifact version, not the platform version: the image carries the HopsFS FUSE client and nothing else, so it turns over with HopsFS. Keep that half in step with charts/hopsfs image.tag, since the FUSE client should match the HopsFS line it talks to. The second half moves when the image is rebuilt without the artifact changing, a base bump or a security rebuild, so such a rebuild cannot silently replace the bytes behind a tag already deployed. Both halves are pinned here on purpose. |
| global._hopsworks.trino.mountableSecrets.mechanism | string | `"csi"` | DEPRECATED and read by nothing. Selected between the hopsfs-csi transport and the privileged `hopsfsMount` sidecar; the sidecar is gone and Trino requires global._hopsworks.csi.enabled. Kept only so an override carried from 5.1 still validates. |
| global._hopsworks.trino.mountableSecrets.mountPath | string | `"/opt/hopsworks/mounts"` | Where the tree is mounted inside the Trino pods. Seeded to the backend as the `trino_mountable_secrets_root` variable and used for the sidecar's mount point, its preStop unmount and the Trino containers' mount, so one value drives both sides. They agreed only by both defaulting to the same literal before, which meant an operator moving the mount left the backend resolving `${HOPSWORKS_MOUNT:...}` under a path nothing was mounted at. |
| global._hopsworks.trino.mountableSecrets.storeRoot | string | `"/apps/mountable-secrets"` | Where the store lives in HopsFS, the source side of the mount. One value, three consumers: charts/hopsfs presets the directory, the mount sidecar passes it as `--srcDir`, and it is seeded to the backend as the `mountable_secrets_path` variable so the backend writes bundles where the mount reads them. It was a literal in all three places before, agreeing only by coincidence, which is the trap `mountPath` had on the container side. Not a knob to reach for: moving it does not move the bundles already written under the old path, and the tree is backend-owned (payara:hdfs, 0750) rather than operator-managed. |
| global._hopsworks.trino.testCoordinator | object | `{"enabled":true}` | Optional dedicated Trino test coordinator used to connection-test user catalogs before they are synced to the production coordinator. |
| global._hopsworks.trino.testCoordinator.enabled | bool | `true` | Deploy an optional dedicated Trino coordinator (catalog.management=dynamic, writable catalog dir) used to connection-test user catalogs before syncing them to the production coordinator. When true, the backend variable trino_test_coordinator_enabled is set so the "test connection" feature becomes available. Enabled by default; set to false to skip the extra coordinator (the "test connection" action is then reported unavailable). |
| global._hopsworks.trino.userCatalogShards | int | `2` | DEPRECATED and read by nothing: user catalogs are HopsFS files now, not sharded Secrets. Kept so an existing override still validates. |
| global._hopsworks.vpaEnabled | bool | `false` |  |
| global._hopsworks.wipeDataOnUninstall | bool | `true` | on uninstall, delete data PVCs left behind by StatefulSets unless the PVC carries the label hopsworks.ai/keep=true. Consumed by subchart post-delete cleanup hooks via the hopsworkslib.wipeDataOnUninstall helper. |
| global._kserve | object | `{"servingruntime":{"vllmomni":{"tag":"v0.28.0"},"vllmopenai":{"tag":"v0.28.0"}}}` | Global KServe values shared between the kserve and hopsworks subcharts |
| global._kserve.servingruntime | object | `{"vllmomni":{"tag":"v0.28.0"},"vllmopenai":{"tag":"v0.28.0"}}` | Mirrors the kserve subchart's `kserve.servingruntime` layout. Tags here drive both the kserve ClusterServingRuntime images and the kube_serving_vllm*_versions hopsworks variable seeds. |
| global._kserve.servingruntime.vllmomni | object | `{"tag":"v0.28.0"}` | vLLM-Omni runtime image tag. Drives both the kserve ClusterServingRuntime image and the kube_serving_vllm_omni_versions hopsworks variable seed. |
| global._kserve.servingruntime.vllmopenai | object | `{"tag":"v0.28.0"}` | vLLM-OpenAI runtime image tag. Drives both the kserve ClusterServingRuntime image and the kube_serving_vllm_versions hopsworks variable seed. |
| global.imageDigests | object | `{}` | map image name to sha digest to be used instead of tags for reproducible deployment  |
| global.unmanagedLoadBalancers | object | `{}` | Load balancer configuration when using unmanaged LB, in AWS is the TargetGroup ARNs for each service       |
| airflow | object | `{"csi":{}}` | override airflow values |
| arrowflight | object | `{}` | override arrow flight values |
| certs-operator | object | `{}` | override certs-operator values |
| consul | object | `{"consul":{"server":{"storageClass":null}}}` | override consul values |
| docker-registry | object | `{"storageClassName":null}` | override docker-registry values |
| grafana | object | `{"grafana":{"global":{"imageRegistry":"docker.hops.works"}}}` | override grafana values |
| hive | object | `{}` | override hive values |
| hopsfs | object | `{"datanode":{"count":5,"storage":{"size":"100Gi","storageClassName":null}},"namenode":{"resources":{"limits":{"memory":"2048Mi"},"requests":{"memory":"1024Mi"}}},"objectStorage":{"enabled":true}}` | override hopsfs values |
| hopsfs-csi | object | `{}` | override hopsfs-csi values. Defaults live in charts/hopsfs-csi/values.yaml; the image comes from global._hopsworks.csi.image and global._hopsworks.imageRegistry, not from here. |
| hopsworks | object | `{"lb":{"names":{"mysqld":"mysqld-external","rdrs":"rdrs-external"}},"replicaCount":{"worker":2},"resources":{"admin":{"auto_jvm":true,"jvm":{"memory":{"buffer":2048,"compressedClassSpaceSize":512,"heap":4096,"metaspace":2048,"nonMethodCodeHeapSize":5,"nonProfiledCodeHeapSize":48,"profiledCodeHeapSize":48}}},"worker":{"auto_jvm":true,"jvm":{"memory":{"buffer":3072,"compressedClassSpaceSize":512,"heap":4096,"metaspace":2048,"nonMethodCodeHeapSize":5,"nonProfiledCodeHeapSize":48,"profiledCodeHeapSize":48}}}},"variables":{"kube_kserve_installed":true,"kube_serving_vllm_omni_versions":"v0.28.0","kube_serving_vllm_versions":"v0.28.0"}}` | override hopsworks values |
| hopsworkslib | object | `{}` | override hopsworkslib values |
| hw-kueue | object | `{}` | override hw-kueue values |
| hw-kyverno | object | `{}` | override hw-kyverno values |
| judge | object | `{}` | override judge values |
| kafka | object | `{"cluster":{"kafka":{"storageClassName":null},"zookeeper":{"storageClassName":null}},"strimzi-kafka-operator":{"defaultImageRegistry":"docker.hops.works"}}` | override kafka values |
| kserve | object | `{"kserve":{"servingruntime":{"vllmomni":{"imageRegistry":"","tag":"v0.28.0"},"vllmopenai":{"imageRegistry":"","tag":"v0.28.0"}}}}` | override kserve values |
| kserve.kserve.servingruntime.vllmomni.imageRegistry | string | `""` | Registry override for the vllm-omni image. Empty falls back to `global._hopsworks.imageRegistry`. |
| kserve.kserve.servingruntime.vllmopenai.imageRegistry | string | `""` | Registry override for the vllm-openai image. Empty falls back to `global._hopsworks.imageRegistry`. |
| minio | object | `{"replicas":2,"resources":{"limits":{"cpu":"4","memory":"8Gi"}},"storage":"100Gi"}` | override minio values       |
| olk | object | `{"opensearch":{"storageClassName":null}}` | override olk values |
| onlinefs | object | `{"debug":false}` | override onlinefs values |
| prometheus | object | `{"prometheus":{"server":{"persistentVolume":{"enabled":true,"storageClass":null}}}}` | override prometheus values |
| ray | object | `{}` | override ray values |
| rondb | object | `{"rondb":{"clusterSize":{"activeDataReplicas":2,"maxNumMySQLServers":1,"maxNumRdrs":2,"minNumMySQLServers":1,"minNumRdrs":1,"numNodeGroups":1},"enableSecurityContext":true,"images":{"mysqldExporter":{"registry":"docker.hops.works"},"rondb":{"registry":"docker.hops.works"},"toolbox":{"name":"hwutils","registry":"docker.hops.works","tag":"1.10-SNAPSHOT"}},"meta":{"mysqld":{"externalLoadBalancer":{"annotations":{},"class":null,"enabled":true,"name":"mysqld-external"}},"rdrs":{"externalLoadBalancer":{"annotations":{},"class":null,"enabled":true,"name":"rdrs-external"},"statefulSet":{"endToEndTls":{"enabled":true}}}},"mysql":{"credentialsSecretName":"mysql-users-secrets","exporter":{"enabled":true},"users":[{"host":"%","privileges":[{"database":"*","privileges":["ALL"],"table":"*","withGrantOption":true}],"username":"hopsworksroot"}]},"networkPolicy":{"mgmds":{"ingressSelectors":[{"podSelector":{"matchLabels":{"access":"mgmd-and-ndbmtd"}}}]},"ndbmtds":{"ingressSelectors":[{"podSelector":{"matchLabels":{"access":"mgmd-and-ndbmtd"}}}]}},"resources":{"requests":{"storage":{"classes":{"binlogFiles":null,"default":null,"diskColumns":null}}}},"serviceAccountAnnotations":{}}}` | override rondb values |
| spark | object | `{}` | override sparkt values |
| superset | object | `{"mysql":{"enabled":true},"superset":{"redis":{"enabled":true}}}` | override  superset values |
| trino | object | `{}` | override  trino values |
| vpa | object | `{}` | override vpa values |
| airflow.airflowApi.basePath | string | `"/hopsworks-api/airflow"` |  |
| airflow.airflowApi.bundleRoot | string | `"/opt/airflow/hopsworks-bundle/dags"` |  |
| airflow.airflowApi.corsAllowedOrigins | string | `""` |  |
| airflow.airflowApi.jwtAlgorithm | string | `"RS256"` |  |
| airflow.airflowApi.jwtAudience | string | `"hopsworks-airflow"` |  |
| airflow.airflowApi.jwtExpirationSeconds | int | `3600` |  |
| airflow.airflowApi.jwtPrivateKeyPath | string | `"/etc/airflow/keys/api-server-private.pem"` |  |
| airflow.airflowApi.jwtPublicKeyPath | string | `"/etc/airflow/keys/api-server-public.pem"` |  |
| airflow.airflowApi.keysSecretName | string | `"hopsworks-airflow-keys"` |  |
| airflow.airflowApi.schedulerPrivateKeyPath | string | `"/etc/airflow/keys/scheduler-private.pem"` |  |
| airflow.airflowApi.schedulerPublicKeyPath | string | `"/etc/airflow/keys/scheduler-public.pem"` |  |
| airflow.appName | string | `"airflow"` | app name label |
| airflow.bidirectional_mount | string | `"mounted"` | the name of bidirectional mount |
| airflow.cleanupOnUninstall | object | `{"enabled":true,"ttlSecondsAfterFinished":null}` | post-delete cleanup of Airflow leftovers. The keys Secret (airflowApi.keysSecretName) is created by the keys-bootstrap pre-install hook via kubectl, so Helm/ArgoCD never track it; this deletes it by name on uninstall. |
| airflow.cleanupOnUninstall.enabled | bool | `true` | enable the post-delete Airflow keys-Secret cleanup hook |
| airflow.cleanupOnUninstall.ttlSecondsAfterFinished | string | `nil` | ttlSecondsAfterFinished for the cleanup Job; null falls through to the global default |
| airflow.common.celery.broker_url | string | `"rdis://:6379/0"` |  |
| airflow.common.celery.celery_app_name | string | `"airflow.executors.celery_executor"` |  |
| airflow.common.celery.default_queue | string | `"default"` |  |
| airflow.common.celery.flower_port | int | `5555` |  |
| airflow.common.celery.flower_url_prefix | string | `"http://localhost/hopsworks-api/flower"` |  |
| airflow.common.celery.worker_concurrency | int | `8` |  |
| airflow.common.celery.worker_log_server_port | int | `8793` |  |
| airflow.common.core_config.airflow_home | string | `"/airflow"` |  |
| airflow.common.core_config.base_log_folder | string | `"/airflow/logs"` |  |
| airflow.common.core_config.dag_concurrency | int | `16` |  |
| airflow.common.core_config.dagbag_import_timeout | int | `60` |  |
| airflow.common.core_config.dags_are_paused_at_creation | bool | `true` |  |
| airflow.common.core_config.dags_folder | string | `"/airflow/dags"` |  |
| airflow.common.core_config.default_timezone | string | `"utc"` |  |
| airflow.common.core_config.donot_pickle | bool | `false` |  |
| airflow.common.core_config.executor | string | `"LocalExecutor"` |  |
| airflow.common.core_config.fernet_key | string | `"G3jB5--jCQpRYp7hwUtpfQ_S8zLRbRMwX8tr3dehnNU="` |  |
| airflow.common.core_config.hostname_callable | string | `"airflow.utils.net.get_host_ip_address"` |  |
| airflow.common.core_config.load_examples | bool | `false` |  |
| airflow.common.core_config.logging_config_class | string | `"log_config.LOGGING_CONFIG"` |  |
| airflow.common.core_config.max_active_runs_per_dag | int | `16` |  |
| airflow.common.core_config.non_pooled_task_slot_count | int | `128` |  |
| airflow.common.core_config.parallelism | int | `32` |  |
| airflow.common.core_config.plugins_folder | string | `"/airflow/plugins"` |  |
| airflow.common.core_config.sql_alchemy_max_overflow | int | `30` | We set it high, not unlimited to account for memory leaks |
| airflow.common.core_config.sql_alchemy_pool_pre_ping | bool | `true` |  |
| airflow.common.core_config.sql_alchemy_pool_recycle | int | `3600` |  |
| airflow.common.core_config.sql_alchemy_pool_size | int | `10` |  |
| airflow.common.group | string | `"airflow"` |  |
| airflow.common.namenode_cluster_ip_name | string | `"namenode-cluster-ip"` |  |
| airflow.common.smtp.smtp_host | string | `"localhost"` |  |
| airflow.common.smtp.smtp_mail_from | string | `"admin@kth.se"` |  |
| airflow.common.smtp.smtp_password | string | `"admin"` |  |
| airflow.common.smtp.smtp_port | int | `25` |  |
| airflow.common.smtp.smtp_ssl | bool | `false` |  |
| airflow.common.smtp.smtp_starttls | bool | `true` |  |
| airflow.common.smtp.smtp_user | string | `"admin@kth.se"` |  |
| airflow.common.user | string | `"airflow"` |  |
| airflow.csi | object | `{"clientCertificateSecretKey":"","clientKeySecretKey":"","defaultPermissions":true,"fallbackGroup":"airflow","fallbackUser":"airflow","imageTag":"","rootCABundleSecretKey":"","secretName":"","sidecarGid":1508,"sidecarResources":{"limits":{"cpu":"1","memory":"1024Mi"},"requests":{"cpu":"200m","memory":"256Mi"}},"sidecarUid":1512}` | CSI settings for the unprivileged HopsFS FUSE sidecar. When `tls=true`, the default secret selectors target the Airflow CSI-specific HopsworksCert secret. |
| airflow.csi.clientCertificateSecretKey | string | `""` | override the client certificate bundle file name inside the mounted TLS secret |
| airflow.csi.clientKeySecretKey | string | `""` | override the client key file name inside the mounted TLS secret |
| airflow.csi.defaultPermissions | bool | `true` | enable the kernel-side default_permissions check on the fuse mount; set false on OpenShift, where workload uids are arbitrary and can never match the owners hopsfs-mount reports (HDFS permissions are still enforced server-side) |
| airflow.csi.imageTag | string | `""` | override the tag of the hopsfs-csi image run as the unprivileged FUSE sidecar. Empty (the default) takes global._hopsworks.csi.image.tag, the one place the hopsfs-csi image is named, so the sidecar and the node plugin it fetches the mount from cannot drift; set only to test a sidecar build against a deployed plugin |
| airflow.csi.rootCABundleSecretKey | string | `""` | override the root CA bundle file name inside the mounted TLS secret |
| airflow.csi.secretName | string | `""` | override the Secret holding the PEM TLS material mounted into the FUSE sidecar (defaults to the csi HopsworksCert secret) |
| airflow.csi.sidecarGid | int | `1508` | gid recorded on the fuse mount; matches the airflow group precreated in the hopsfs-csi image |
| airflow.csi.sidecarResources | object | `{"limits":{"cpu":"1","memory":"1024Mi"},"requests":{"cpu":"200m","memory":"256Mi"}}` | resources for the unprivileged FUSE sidecar. All four slots are set on purpose: a namespace LimitRange fills any missing one with its own default, which for a limit-less request is rejected at admission when the default falls below the request (see HWORKS-3086). |
| airflow.csi.sidecarUid | int | `1512` | uid recorded on the fuse mount and used to run the sidecar; matches the airflow user precreated in the hopsfs-csi image |
| airflow.dagProcessor.deployment.replicas | int | `1` |  |
| airflow.dagProcessor.name | string | `"airflow-dag-processor"` |  |
| airflow.dagProcessor.nodeSelector | object | `{}` |  |
| airflow.dagProcessor.probe.failureThreshold | int | `20` |  |
| airflow.dagProcessor.probe.initialDelaySeconds | int | `30` |  |
| airflow.dagProcessor.probe.periodSeconds | int | `10` |  |
| airflow.dagProcessor.probe.timeoutSeconds | int | `10` |  |
| airflow.dagProcessor.refreshIntervalSeconds | int | `5` |  |
| airflow.dagProcessor.resources.limits.memory | string | `"2000Mi"` |  |
| airflow.dagProcessor.resources.requests.cpu | string | `"200m"` |  |
| airflow.dagProcessor.resources.requests.memory | string | `"500Mi"` |  |
| airflow.dagProcessor.securityContext.runAsGroup | int | `1508` |  |
| airflow.dagProcessor.securityContext.runAsNonRoot | bool | `true` |  |
| airflow.dagProcessor.securityContext.runAsUser | int | `1512` |  |
| airflow.dagProcessor.tolerations | list | `[]` |  |
| airflow.debug | bool | `false` | enable or disable debug logging for hopsfs |
| airflow.dependencies.hopsworks | object | `{"consulServiceName":"glassfish","consulServiceTag":"hopsworks","port":8182}` | hopsworks consul service |
| airflow.dependencies.mysql | object | `{"consulServiceName":"mysql","ddlConsulServiceName":"mysqlddl","port":3306}` | mysql consul service |
| airflow.dependencies.namenode | object | `{"consulServiceName":"namenode","port":8020}` | namenode consul service. This uses a headless ClusterIP underneath with `publishNotReadyAddresses: true` |
| airflow.hopsfs_bin_url | string | `nil` | url to download a patched hopsfs mount for testing and development |
| airflow.hopsworks | object | `{"caBundlePath":"/etc/airflow/ca/hopsworks-ca.crt","enableApiKeyFallback":true,"hwJwtCacheTtlSeconds":60,"internalClientCn":"hopsworks-ee.hopsworks.svc","manifestPath":"/shared-volume/hopsfs/.airflow/manifest.json","membershipCacheTtlSeconds":60,"url":""}` | Hopsworks-specific Airflow 3 configuration. |
| airflow.hopsworkslib | object | `{}` | override hopsworkslib values |
| airflow.image | object | `{"pullPolicy":"IfNotPresent","registry":"docker.hops.works"}` | image configuration. The image tag is the .Chart.AppVersion  |
| airflow.migrationBackOffLimit | int | `10` | backoffLimit for airflow migration job |
| airflow.migrationJobTtlSecondsAfterFinished | string | `nil` | TTL in seconds for the migrate-airflow Job. Overrides global default. |
| airflow.orphanCleanup | object | `{"schedule":"42 2 * * *"}` | periodic cleanup of orphaned Airflow rows. The metadata tables live in RonDB without enforced foreign keys (NDB cannot carry FKs on the blob/text tables), so a CronJob restores the dropped ON DELETE CASCADE semantics by deleting children whose parent `airflow db clean` removed. Gated by the airflow subchart's own enable condition in the umbrella `Chart.yaml` (`global._hopsworks.airflow.enabled,global._hopsworks.full_platform`): if airflow is disabled, this CronJob is not rendered. |
| airflow.reset_db_if_error | bool | `false` | if true, will reset the database and create a new one in case of error. In Airflow 3 the db-reset job runs unconditionally before migrate; this key is retained for backwards compatibility but the v3 chart ignores it. |
| airflow.scheduler.config.dag_dir_list_interval | int | `40` |  |
| airflow.scheduler.config.job_heartbeat_sec | int | `5` |  |
| airflow.scheduler.config.max_threads | int | `2` |  |
| airflow.scheduler.config.min_file_process_interval | int | `10` |  |
| airflow.scheduler.config.print_stats_interval | int | `600` |  |
| airflow.scheduler.config.scheduler_zombie_task_threshold | int | `300` |  |
| airflow.scheduler.deployment.replicas | int | `1` |  |
| airflow.scheduler.is_tls | bool | `false` |  |
| airflow.scheduler.name | string | `"airflow-scheduler"` |  |
| airflow.scheduler.nodeSelector | object | `{}` | node selector configuration |
| airflow.scheduler.podDisruptionBudget.enabled | bool | `true` |  |
| airflow.scheduler.podDisruptionBudget.minAvailable | int | `1` |  |
| airflow.scheduler.probe.failureThreshold | int | `20` |  |
| airflow.scheduler.probe.initialDelaySeconds | int | `30` |  |
| airflow.scheduler.probe.periodSeconds | int | `10` |  |
| airflow.scheduler.probe.timeoutSeconds | int | `10` |  |
| airflow.scheduler.probeCheckWebserver | bool | `true` |  |
| airflow.scheduler.probeCommand | string | `"set -e && pgrep -f \"airflow scheduler\""` | The probe here will be concatenated with sleeping for the heartbeat time and then trying to reach the webserver. If the webserver is not reachable the scheduler should be restarted  https://hopsworks.atlassian.net/browse/HWORKS-1915 The scheduler goes to a non consistent state, then the health check of the webserver returns scheduler non-healthy and it fails |
| airflow.scheduler.resources.limits | object | `{"memory":"2000Mi"}` | resources limits configuration |
| airflow.scheduler.resources.requests | object | `{"cpu":"1","memory":"1000Mi"}` | resources requests configuration |
| airflow.scheduler.securityContext.runAsGroup | int | `1508` |  |
| airflow.scheduler.securityContext.runAsNonRoot | bool | `true` |  |
| airflow.scheduler.securityContext.runAsUser | int | `1512` |  |
| airflow.scheduler.service.annotations."consul.hashicorp.com/service-name" | string | `"airflow"` |  |
| airflow.scheduler.service.annotations."consul.hashicorp.com/service-tags" | string | `"scheduler"` |  |
| airflow.scheduler.tolerations | list | `[]` |  |
| airflow.scheduler.topologySpreadConstraint | object | `{}` | The default topology spread constraint. If not defined the global topology spread constraint would be used instead. |
| airflow.serviceAccount.annotations | object | `{}` | service account annotations |
| airflow.serviceAccountName | string | `"airflow"` | service account name |
| airflow.tls | bool | `true` | enable or disable TLS |
| airflow.webserver.config.authenticate | bool | `true` |  |
| airflow.webserver.config.expose_config | bool | `true` |  |
| airflow.webserver.config.rbac | bool | `true` |  |
| airflow.webserver.config.secret_key | string | `"temporary_key"` |  |
| airflow.webserver.config.web_server_host | string | `"0.0.0.0"` |  |
| airflow.webserver.config.web_server_port | int | `12358` |  |
| airflow.webserver.config.web_server_worker_timeout | int | `120` |  |
| airflow.webserver.config.worker_class | string | `"sync"` |  |
| airflow.webserver.config.workers | int | `2` |  |
| airflow.webserver.configHelm.base_path | string | `"/hopsworks-api/airflow"` |  |
| airflow.webserver.deployment.replicas | int | `1` |  |
| airflow.webserver.forwardedAllowIps | string | `"10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"` |  |
| airflow.webserver.heartbeat | int | `30` |  |
| airflow.webserver.is_tls | bool | `false` |  |
| airflow.webserver.name | string | `"airflow-webserver"` |  |
| airflow.webserver.nodeSelector | object | `{}` | node selector configuration |
| airflow.webserver.podDisruptionBudget.enabled | bool | `true` |  |
| airflow.webserver.podDisruptionBudget.minAvailable | int | `1` |  |
| airflow.webserver.probe.failureThreshold | int | `10` |  |
| airflow.webserver.probe.initialDelaySeconds | int | `60` |  |
| airflow.webserver.probe.periodSeconds | int | `5` |  |
| airflow.webserver.probe.timeoutSeconds | int | `10` |  |
| airflow.webserver.resources.limits | object | `{"memory":"2000Mi"}` | resources limits configuration |
| airflow.webserver.resources.requests | object | `{"cpu":"100m","memory":"1000Mi"}` | resources requests configuration |
| airflow.webserver.securityContext.runAsGroup | int | `1508` |  |
| airflow.webserver.securityContext.runAsUser | int | `1512` |  |
| airflow.webserver.service.annotations | object | `{"consul.hashicorp.com/service-name":"airflow","consul.hashicorp.com/service-port":"server","consul.hashicorp.com/service-tags":"ui"}` | annotations on the airflow-webserver Service; the map is open, so an operator can add their own |
| airflow.webserver.tolerations | list | `[]` |  |
| airflow.webserver.topologySpreadConstraint | object | `{}` | The default topology spread constraint. If not defined the global topology spread constraint would be used instead. |
| arrowflight.appName | string | `"arrowflight"` |  |
| arrowflight.common.monitoring_port | int | `12810` |  |
| arrowflight.common.port | int | `5005` |  |
| arrowflight.configmap.name | string | `"arrowflight-configmap"` |  |
| arrowflight.deployment.annotations."prometheus.io/path" | string | `"/metrics"` |  |
| arrowflight.deployment.annotations."prometheus.io/port" | string | `"12810"` |  |
| arrowflight.deployment.annotations."prometheus.io/scheme" | string | `"http"` |  |
| arrowflight.deployment.annotations."prometheus.io/scrape" | string | `"true"` |  |
| arrowflight.deployment.name | string | `"arrowflight-deployment"` |  |
| arrowflight.deployment.replicas | int | `1` | Number of replicas. Not rendered while the HPA is active (hpa.enabled and no VPA on this Deployment): the HPA then owns spec.replicas and this value is its minReplicas. Turning the HPA on for a running release drops the Deployment to 1 once, until the HPA scales it back up. |
| arrowflight.deployment.resources.limits | object | `{"memory":"8192Mi"}` | resources limits configuration |
| arrowflight.deployment.resources.requests | object | `{"cpu":"2","memory":"6553Mi"}` | resources requests configuration |
| arrowflight.deployment.security.runAsGroup | int | `1520` |  |
| arrowflight.deployment.security.runAsUser | int | `1525` |  |
| arrowflight.deployment.server.hopsfs_query_mode | string | `"view"` |  |
| arrowflight.deployment.server.memory_limit | string | `"6"` |  |
| arrowflight.deployment.server.queue_timeout | string | `"600"` |  |
| arrowflight.externalLoadBalancer.annotations | object | `{}` | annotations for load balancer |
| arrowflight.externalLoadBalancer.class | string | `nil` | load balancer class name |
| arrowflight.externalLoadBalancer.enabled | string | `nil` | Enable External Load Balancers for Arrowflight server. If not set the .global._hopsworks.externalLoadBalancers.enabled will be used instead |
| arrowflight.externalLoadBalancer.managed | string | `nil` | Cloud provider provisions Load Balancers. If not set the .global._hopsworks.externalLoadBalancers.managed will be used instead |
| arrowflight.externalLoadBalancer.nodeSelector | object | `{}` | selector for nodes the load balancer can use to route traffic |
| arrowflight.hopsworkslib | object | `{}` | override hopsworkslib values |
| arrowflight.hpa.enabled | bool | `true` | Autoscale the Deployment with an HPA (suppressed when a VPA targets it). While active, deployment.replicas is not rendered and the HPA owns spec.replicas. |
| arrowflight.hpa.flyingduck_queue_time_avg | int | `27` |  |
| arrowflight.hpa.flyingduck_request_queue_gauge | int | `2` |  |
| arrowflight.hpa.maxReplicas | int | `3` |  |
| arrowflight.image | object | `{"pullPolicy":"IfNotPresent","registry":"docker.hops.works"}` | image configuration. The image tag is the .Chart.AppVersion  |
| arrowflight.nodeSelector | object | `{}` | node selector configuration |
| arrowflight.podDisruptionBudget.enabled | bool | `true` |  |
| arrowflight.podDisruptionBudget.minAvailable | int | `1` |  |
| arrowflight.service.annotations."consul.hashicorp.com/service-name" | string | `"flyingduck"` |  |
| arrowflight.service.annotations."consul.hashicorp.com/service-port" | string | `"server"` |  |
| arrowflight.service.annotations."consul.hashicorp.com/service-tags" | string | `"server"` |  |
| arrowflight.service.annotations."prometheus.io/path" | string | `"/metrics"` |  |
| arrowflight.service.annotations."prometheus.io/port" | string | `"12810"` |  |
| arrowflight.service.annotations."prometheus.io/scheme" | string | `"http"` |  |
| arrowflight.service.annotations."prometheus.io/scrape" | string | `"true"` |  |
| arrowflight.service.name | string | `"arrowflight-server"` |  |
| arrowflight.spillVolume | object | `{"size":"20Gi","storageClassName":null}` | storage configuration for the ephemeral volume used by DuckDB for spilling on disk during query execution for spilling on disk during query execution for spilling on disk during query execution |
| arrowflight.spillVolume.size | string | `"20Gi"` | size of the ephemeral volume |
| arrowflight.spillVolume.storageClassName | string | `nil` | storage class name. If null, the default storage class will be used |
| arrowflight.tolerations | list | `[]` |  |
| arrowflight.topologySpreadConstraint | object | `{}` | The default topology spread constraint. If not defined the global topology spread constraint would be used instead. |
| certs-operator.controller.manager.resources.limits.cpu | string | `"500m"` |  |
| certs-operator.controller.manager.resources.limits.memory | string | `"128Mi"` |  |
| certs-operator.controller.manager.resources.requests.cpu | string | `"10m"` |  |
| certs-operator.controller.manager.resources.requests.memory | string | `"64Mi"` |  |
| certs-operator.controller.manager.watchNamespaces | string | `nil` | Comma separated list of Namespaces to restrict certs-operator to watch for. If not set it will watch all Namespaces. |
| certs-operator.controller.serviceAccount.annotations | object | `{}` | service account annotations |
| certs-operator.dependencies.ca.apiKeySecretKey | string | `"key"` |  |
| certs-operator.dependencies.ca.apiKeySecretName | string | `"hopsworks-api-key-auth"` |  |
| certs-operator.dependencies.ca.authMethod | string | `"api_key"` |  |
| certs-operator.dependencies.ca.consulServiceName | string | `"glassfish"` |  |
| certs-operator.dependencies.ca.consulServiceTag | string | `"ca"` |  |
| certs-operator.dependencies.ca.httpScheme | string | `"https"` |  |
| certs-operator.dependencies.ca.httpTimeout | string | `"60s"` |  |
| certs-operator.dependencies.ca.password | string | `"adminpw"` |  |
| certs-operator.dependencies.ca.port | int | `8182` |  |
| certs-operator.dependencies.ca.user | string | `"agent@hops.io"` |  |
| certs-operator.fullnameOverride | string | `nil` | override app fully qualified name  |
| certs-operator.gracefulCertTeardown | object | `{"enabled":true,"timeoutSeconds":120,"ttlSecondsAfterFinished":null}` | ordered, narrow-RBAC teardown of HopsworksCerts on uninstall: a pre-delete hook deletes the certs while the certs-operator is still alive (so it releases its own finalizers), and a post-delete hook force-clears any finalizers left behind on runtimes that drop pre-delete hooks (ArgoCD < 3.3). Independent of the `wipe` job. |
| certs-operator.gracefulCertTeardown.enabled | bool | `true` | enable the ordered HopsworksCert teardown hooks on uninstall |
| certs-operator.gracefulCertTeardown.timeoutSeconds | int | `120` | seconds the pre-delete drain waits for the operator to finalize the certs before deferring to the post-delete backstop |
| certs-operator.gracefulCertTeardown.ttlSecondsAfterFinished | string | `nil` | ttlSecondsAfterFinished for the teardown Jobs; null falls through to the global default |
| certs-operator.hopsworkslib | object | `{}` | override hopsworkslib values |
| certs-operator.nameOverride | string | `nil` | override app chart name |
| certs-operator.nodeSelector | object | `{}` | node selector configuration |
| certs-operator.serviceAccount.create | bool | `false` |  |
| certs-operator.serviceAccount.name | string | `""` |  |
| certs-operator.tolerations | list | `[]` |  |
| certs-operator.topologySpreadConstraint | object | `{}` | The default topology spread constraint. If not defined the global topology spread constraint would be used instead. |
| consul.autoConfigureCoreDNS | bool | `true` |  |
| consul.autoConfigureCoreDNSPort | int | `53` |  |
| consul.autoConfigureJobResources | object | `{"limits":{"cpu":"300m"}}` | resources configuration |
| consul.autoConfigureJobResources.limits | object | `{"cpu":"300m"}` | resource limits configuration |
| consul.autoconfig.serviceAccount.annotations | object | `{}` | service account annotations |
| consul.autoconfig.ttlSecondsAfterFinished | string | `nil` | TTL in seconds for the autoconfig coredns Job. Overrides global default. |
| consul.cleanupOnUninstall | object | `{"enabled":true,"ttlSecondsAfterFinished":null}` | post-delete cleanup of Consul runtime leftovers (consul-k8s ACL/gossip secrets, the metrics-acl-token secret, and the upstream install-hook RBAC) that Helm/ArgoCD never tracked and so never prune. Also deletes Consul server PVCs when global._hopsworks.wipeDataOnUninstall is enabled (except hopsworks.ai/keep=true). |
| consul.cleanupOnUninstall.enabled | bool | `true` | enable the post-delete Consul cleanup hook |
| consul.cleanupOnUninstall.ttlSecondsAfterFinished | string | `nil` | ttlSecondsAfterFinished for the cleanup Job; null falls through to the global default |
| consul.consul | object | `{"client":{"dnsPolicy":"ClusterFirstWithHostNet","hostNetwork":true},"connectInject":{"enabled":false},"dns":{"enabled":true},"global":{"acls":{"manageSystemACLs":true,"nodeSelector":null,"tolerations":""},"datacenter":"dc1","domain":"consul","enabled":true,"gossipEncryption":{"autoGenerate":true},"image":"docker.hops.works/hashicorp/consul:1.16.4-alpine-h1","imageK8S":"docker.hops.works/hashicorp/consul-k8s-control-plane:1.8.16","logLevel":"info","metrics":{"disableAgentHostName":true,"enableAgentMetrics":true,"enableGatewayMetrics":false,"enabled":true},"name":null,"tls":{"enabled":true}},"metrics":{"enabled":true,"rbac":{"annotations":{},"create":true,"extraRoleRules":[],"name":"consul-metrics-role","useExistingRole":false},"serviceAccount":{"annotations":{},"create":true,"name":"consul-metrics-default"}},"server":{"connect":false,"enabled":true,"logLevel":"info","nodeSelector":null,"replicas":3,"resources":{"limits":{"cpu":"100m","memory":"350Mi"},"requests":{"cpu":"100m","memory":"200Mi"}},"storageClass":null,"tolerations":"","topologySpreadConstraints":"- maxSkew: 1\n  topologyKey: topology.kubernetes.io/zone\n  whenUnsatisfiable: ScheduleAnyway\n  labelSelector:\n    matchLabels:\n      app: consul\n      component: server\n"},"syncCatalog":{"default":true,"enabled":true,"k8sAllowNamespaces":["*"],"nodeSelector":null,"resources":{"limits":{"cpu":"50m","memory":"100Mi"},"requests":{"cpu":"50m","memory":"100Mi"}},"toConsul":true,"toK8S":false,"tolerations":""},"ui":{"enabled":true}}` | override consul values |
| consul.corednsConfigMapName | string | `"coredns"` | the name of the coredns configmap. This name is only used when global._hopsworks.cloudProvider does not equal to AZURE, OVH, or GCP. For AZURE and OVH, coredns-custom is being used by default and for GCP, kube-dns is being used by default. |
| consul.corednsDeploymentName | string | `"coredns"` | the name of the coredns deployment. This name is only used when global._hopsworks.cloudProvider does not equal to AZURE, OVH, or GCP. |
| consul.fullnameOverride | string | `nil` | override app fully qualified name  |
| consul.hopsworkslib | object | `{}` | override hopsworkslib values |
| consul.manualServiceRegistration.resources.limits.cpu | string | `"100m"` |  |
| consul.manualServiceRegistration.resources.limits.memory | string | `"100Mi"` |  |
| consul.manualServiceRegistration.resources.requests.cpu | string | `"50m"` |  |
| consul.manualServiceRegistration.resources.requests.memory | string | `"30Mi"` |  |
| consul.manualServiceRegistration.ttlSecondsAfterFinished | string | `nil` | TTL in seconds for manual service registration Jobs. Overrides global default. |
| consul.nameOverride | string | `nil` | override app chart name |
| consul.networkPolicy.enabled | bool | `false` |  |
| consul.nodeSelector | object | `{}` | node selector configuration used for the autoconfig job and register managed docker registry jobs |
| consul.tolerations | list | `[]` |  |
| docker-registry.affinity | object | `{}` | affinity configuration |
| docker-registry.appName | string | `"docker-registry"` |  |
| docker-registry.config\[0\].name | string | `"REGISTRY_STORAGE_DELETE_ENABLED"` |  |
| docker-registry.config\[0\].value | string | `"true"` |  |
| docker-registry.config\[10\].name | string | `"REGISTRY_STORAGE_S3_V4AUTH"` |  |
| docker-registry.config\[10\].value | string | `"true"` |  |
| docker-registry.config\[11\].name | string | `"REGISTRY_STORAGE_S3_FORCEPATHSTYLE"` |  |
| docker-registry.config\[11\].value | string | `"true"` |  |
| docker-registry.config\[12\].name | string | `"REGISTRY_STORAGE_S3_LOGLEVEL"` |  |
| docker-registry.config\[12\].value | string | `"debug"` |  |
| docker-registry.config\[13\].name | string | `"REGISTRY_STORAGE_S3_CHUNKSIZE"` |  |
| docker-registry.config\[13\].value | string | `"209715200"` |  |
| docker-registry.config\[14\].name | string | `"REGISTRY_HTTP_DRAINTIMEOUT"` |  |
| docker-registry.config\[14\].value | string | `"10m"` |  |
| docker-registry.config\[15\].name | string | `"REGISTRY_VALIDATION_DISABLED"` |  |
| docker-registry.config\[15\].value | string | `"true"` |  |
| docker-registry.config\[16\].name | string | `"REGISTRY_STORAGE_REDIRECT_DISABLE"` |  |
| docker-registry.config\[16\].value | string | `"true"` |  |
| docker-registry.config\[17\].name | string | `"REGISTRY_LOG_LEVEL"` |  |
| docker-registry.config\[17\].value | string | `"info"` |  |
| docker-registry.config\[18\].name | string | `"REGISTRY_HTTP_HEADERS"` |  |
| docker-registry.config\[18\].value | string | `"{X-Content-Type-Options: [nosniff]}"` |  |
| docker-registry.config\[1\].name | string | `"REGISTRY_STORAGE_CACHE_BLOBDESCRIPTOR"` |  |
| docker-registry.config\[1\].value | string | `"inmemory"` |  |
| docker-registry.config\[2\].name | string | `"REGISTRY_STORAGE_CACHE_BLOBDESCRIPTORSIZE"` |  |
| docker-registry.config\[2\].value | string | `"10"` |  |
| docker-registry.config\[3\].name | string | `"REGISTRY_STORAGE"` |  |
| docker-registry.config\[3\].value | string | `"s3"` |  |
| docker-registry.config\[4\].name | string | `"REGISTRY_STORAGE_S3_ACCESSKEY"` |  |
| docker-registry.config\[4\].value | string | `"minioadmin"` |  |
| docker-registry.config\[5\].name | string | `"REGISTRY_STORAGE_S3_SECRETKEY"` |  |
| docker-registry.config\[5\].value | string | `"minioadmin"` |  |
| docker-registry.config\[6\].name | string | `"REGISTRY_STORAGE_S3_REGION"` |  |
| docker-registry.config\[6\].value | string | `"eu-west-1"` |  |
| docker-registry.config\[7\].name | string | `"REGISTRY_STORAGE_S3_BUCKET"` |  |
| docker-registry.config\[7\].value | string | `"public"` |  |
| docker-registry.config\[8\].name | string | `"REGISTRY_STORAGE_S3_ROOTDIRECTORY"` |  |
| docker-registry.config\[8\].value | string | `"/"` |  |
| docker-registry.config\[9\].name | string | `"REGISTRY_STORAGE_S3_SECURE"` |  |
| docker-registry.config\[9\].value | string | `"false"` |  |
| docker-registry.debug | bool | `false` |  |
| docker-registry.dependencies.objectStorage.consulServiceName | string | `"minio"` |  |
| docker-registry.dependencies.objectStorage.port | int | `9000` |  |
| docker-registry.enabled | bool | `true` |  |
| docker-registry.hopsworkslib | object | `{}` | override hopsworkslib values |
| docker-registry.hpa.enabled | bool | `true` | Autoscale the registry with an HPA (suppressed when a VPA targets it). While active, replicas is not rendered and the HPA owns spec.replicas. |
| docker-registry.hpa.maxReplicas | int | `4` |  |
| docker-registry.hpa.minReplicas | int | `1` |  |
| docker-registry.hpa.targetCPUUtilizationPercentage | int | `60` |  |
| docker-registry.hpa.targetMemoryUtilizationPercentage | int | `60` |  |
| docker-registry.image.name | string | `"registry"` |  |
| docker-registry.image.pullPolicy | string | `"IfNotPresent"` |  |
| docker-registry.image.registry | string | `"docker.hops.works"` |  |
| docker-registry.image.tag | string | `"3.1.1"` | Distribution v3. The chart configures the registry only through `REGISTRY_*` environment variables and mounts no config file, so v3's new default config path does not affect it. |
| docker-registry.nodeSelector | object | `{}` | node selector configuration |
| docker-registry.podDisruptionBudget.enabled | bool | `true` |  |
| docker-registry.podDisruptionBudget.minAvailable | int | `1` |  |
| docker-registry.replicas | int | `1` | Number of replicas. Not rendered while the HPA is active (hpa.enabled and no VPA on the registry): the HPA then owns spec.replicas, starting from hpa.minReplicas. Turning the HPA on for a running release drops the StatefulSet to 1 once, until the HPA scales it back up. |
| docker-registry.resources.limits.cpu | string | `"2"` |  |
| docker-registry.resources.limits.memory | string | `"10G"` |  |
| docker-registry.resources.requests.cpu | string | `"2"` |  |
| docker-registry.resources.requests.memory | string | `"4G"` |  |
| docker-registry.security.secret | string | `"docker"` |  |
| docker-registry.security.tls.enabled | bool | `true` |  |
| docker-registry.service.headless.name | string | `"registry-headless"` |  |
| docker-registry.service.monitoringPort | int | `5001` | Port of the registry's debug server. Serves `/metrics`, and also `/debug/pprof`, which is why its Service is ClusterIP. |
| docker-registry.service.nodePort.annotations."consul.hashicorp.com/service-name" | string | `"registry"` |  |
| docker-registry.service.port | int | `30443` |  |
| docker-registry.storage | string | `nil` | storage class name. Set if the REGISTRY_STORAGE is not S3 |
| docker-registry.storageClassName | string | `nil` | storage class name |
| docker-registry.tamperContainerEngine.containerdConfigFile | string | `"config.toml"` |  |
| docker-registry.tamperContainerEngine.defaultServer | string | `nil` | default server to use in container engine. Change it to docker.hops.works if needed |
| docker-registry.tamperContainerEngine.enabled | bool | `true` |  |
| docker-registry.tamperContainerEngine.fallbackTo | string | `"https://docker.hops.works"` |  |
| docker-registry.tamperContainerEngine.patchEngine | bool | `true` |  |
| docker-registry.tamperContainerEngine.patchEtcHosts | bool | `true` |  |
| docker-registry.tamperContainerEngine.patchOS | bool | `true` |  |
| docker-registry.tamperContainerEngine.registryProtocol | string | `"https"` |  |
| docker-registry.tamperContainerEngine.rollbackChangesIfDeleted | bool | `true` |  |
| docker-registry.tamperContainerEngine.tolerations\[0\].effect | string | `"NoSchedule"` |  |
| docker-registry.tamperContainerEngine.tolerations\[0\].operator | string | `"Exists"` |  |
| docker-registry.tamperContainerEngine.tolerations\[1\].key | string | `"CriticalAddonsOnly"` |  |
| docker-registry.tamperContainerEngine.tolerations\[1\].operator | string | `"Exists"` |  |
| docker-registry.tamperContainerEngine.tolerations\[2\].effect | string | `"NoExecute"` |  |
| docker-registry.tamperContainerEngine.tolerations\[2\].operator | string | `"Exists"` |  |
| docker-registry.tamperContainerEngine.trustCA | string | `"USE_ROOT_HOPSWORKS_CA"` |  |
| docker-registry.tamperContainerEngine.verifyTLS | bool | `true` |  |
| docker-registry.tamperContainerEngine.waitBeforeReset | int | `0` |  |
| docker-registry.tolerations | list | `[]` |  |
| grafana.dependencies.prometheus.consulServiceName | string | `"prometheus"` |  |
| grafana.dependencies.prometheus.consulServiceTag | string | `"prometheus"` |  |
| grafana.dependencies.prometheus.port | int | `9090` |  |
| grafana.grafana | object | `{"dashboardProviders":{"dashboardproviders.yaml":{"apiVersion":1,"providers":[{"disableDeletion":true,"editable":false,"folder":"Apps","name":"Apps","options":{"path":"/usr/share/grafana/dashboards/apps"},"type":"file","updateIntervalSeconds":10},{"disableDeletion":true,"editable":false,"folder":"Hops","name":"Hops","options":{"path":"/usr/share/grafana/dashboards/hops"},"type":"file","updateIntervalSeconds":10},{"disableDeletion":false,"editable":false,"folder":"RonDB","name":"RonDB","options":{"path":"/usr/share/grafana/dashboards/rondb"},"type":"file","updateIntervalSeconds":10},{"disableDeletion":true,"editable":false,"folder":"Overview","name":"Overview","options":{"path":"/usr/share/grafana/dashboards/overview"},"type":"file","updateIntervalSeconds":10},{"disableDeletion":true,"editable":false,"folder":"Kubernetes","name":"Kubernetes","options":{"path":"/usr/share/grafana/dashboards/kubernetes"},"type":"file","updateIntervalSeconds":10},{"disableDeletion":true,"editable":false,"folder":"ModelServing","name":"ModelServing","options":{"path":"/usr/share/grafana/dashboards/kserve"},"type":"file","updateIntervalSeconds":10},{"disableDeletion":true,"editable":false,"folder":"Ray","name":"Ray","options":{"path":"/usr/share/grafana/dashboards/ray"},"type":"file","updateIntervalSeconds":10},{"disableDeletion":true,"editable":false,"folder":"RSS","name":"RemoteShuffleService","options":{"path":"/usr/share/grafana/dashboards/rss"},"type":"file","updateIntervalSeconds":10}]}},"dashboardsConfigMaps":{},"datasources":{"datasources.yaml":{"apiVersion":1,"datasources":[{"access":"proxy","editable":false,"isDefault":true,"name":"Prometheus","type":"prometheus","url":"http://prometheus.prometheus.service.consul:9090"}]}},"downloadDashboardsImage":{"pullPolicy":"IfNotPresent","registry":"docker.hops.works","repository":"hopsworks/hwutils","sha":"","tag":"1.10-SNAPSHOT"},"extraConfigmapMounts":[{"configMap":"{{ include \"hopsworks.grafana.conditionalProvidersName\" . }}","mountPath":"/etc/grafana/provisioning/dashboards/hopsworks-dashboardproviders.yaml","name":"hopsworks-dashboardproviders","readOnly":true,"subPath":"providers.yaml"}],"extraInitContainers":[{"command":["/bin/sh","-c","set -eu\nchecked=0\nfor f in /etc/grafana/provisioning/dashboards/*.yaml; do\n  [ -f \"$f\" ] || continue\n  for p in $(sed -n 's/^[[:space:]]*path:[[:space:]]*//p' \"$f\"); do\n    case \"$p\" in\n      /usr/share/grafana/dashboards/*) ;;\n      *) echo \"skip: $p is delivered by Helm, not by the image\"; continue ;;\n    esac\n    checked=$((checked + 1))\n    n=$(find \"$p\" -name '*.json' 2>/dev/null | wc -l)\n    if [ \"$n\" -eq 0 ]; then\n      echo \"FATAL: dashboard provider path $p (declared in $f) holds no dashboards.\"\n      echo \"The Hopsworks dashboards ship inside the Grafana image. This image does not\"\n      echo \"carry them, so Grafana would start healthy with an empty dashboard list.\"\n      echo \"Use an image built with the dashboards, or override grafana.image.tag.\"\n      exit 1\n    fi\n    echo \"ok: $p ($n dashboards)\"\n  done\ndone\nif [ \"$checked\" -eq 0 ]; then\n  echo \"FATAL: no image dashboard provider paths found in /etc/grafana/provisioning/dashboards.\"\n  echo \"The chart always declares providers under /usr/share/grafana/dashboards, so either\"\n  echo \"the provisioning files did not reach this container or every provider was replaced.\"\n  exit 1\nfi\necho \"verified $checked image dashboard provider paths\"\n"],"image":"{{ .Values.global.imageRegistry | default .Values.image.registry }}/{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}","imagePullPolicy":"{{ .Values.image.pullPolicy }}","name":"verify-dashboards","resources":{"limits":{"cpu":"100m","memory":"64Mi"},"requests":{"cpu":"10m","memory":"32Mi"}},"securityContext":{"allowPrivilegeEscalation":false,"capabilities":{"drop":["ALL"]},"readOnlyRootFilesystem":true,"seccompProfile":{"type":"RuntimeDefault"}},"volumeMounts":[{"mountPath":"/etc/grafana/provisioning/dashboards/dashboardproviders.yaml","name":"config","subPath":"dashboardproviders.yaml"},{"mountPath":"/etc/grafana/provisioning/dashboards/hopsworks-dashboardproviders.yaml","name":"hopsworks-dashboardproviders","subPath":"providers.yaml"}]}],"global":{"imageRegistry":"docker.hops.works"},"grafana.ini":{"auth":{"disable_login_form":true,"disable_signout_menu":true},"auth.anonymous":{"enabled":false},"auth.basic":{"enabled":false},"auth.proxy":{"auto_sign_up":true,"enable_login_token":false,"enabled":true,"header_name":"X-WEBAUTH-USER","header_property":"username","headers":"Name:X-WEBAUTH-NAME Role:X-WEBAUTH-ROLE Email:X-WEBAUTH-EMAIL","headers_encoded":false,"sync_ttl":"60","whitelist":null},"rbac":{"enabled":true},"security":{"admin_password":"adminpw","allow_embedding":true,"strict_transport_security":false},"server":{"enforce_domain":false,"root_url":"/hopsworks-api/grafana"},"users":{"allow_org_create":false,"allow_sign_up":false,"auto_assign_org":true,"auto_assign_org_id":"1","auto_assign_org_role":"Viewer","default_theme":"dark","editors_can_admin":false,"home_page":"/dashboards","verify_email_enabled":false,"viewers_can_edit":false}},"image":{"tag":"12.4.9-h10"},"nodeSelector":{},"rbac":{"create":false},"resources":{"limits":{"cpu":1,"memory":"1000Mi"},"requests":{"cpu":"200m","memory":"200Mi"}},"service":{"annotations":{"consul.hashicorp.com/service-name":"grafana","consul.hashicorp.com/service-tags":"grafana"}},"tolerations":[],"topologySpreadConstraints":[{"labelSelector":{"matchLabels":{"app.kubernetes.io/instance":"hopsworks","app.kubernetes.io/name":"grafana"}},"maxSkew":1,"topologyKey":"topology.kubernetes.io/zone","whenUnsatisfiable":"ScheduleAnyway"}]}` | override grafana values |
| grafana.grafana.dashboardsConfigMaps | object | `{}` | DEPRECATED and intentionally empty. The dashboards used to be inlined into nine ConfigMaps here, which put 1.9 MB of JSON into the rendered manifest and so into the 1 MiB Helm release Secret. They now ship in the Grafana image under /usr/share/grafana/dashboards and are provisioned by path. Kept as an empty map rather than removed so that an existing override does not become an unknown key. |
| grafana.hopsworkslib | object | `{}` | override hopsworkslib values |
| hive.debug | bool | `false` |  |
| hive.externalLoadBalancer.annotations | object | `{}` | annotations for load balancer |
| hive.externalLoadBalancer.class | string | `nil` | load balancer class name |
| hive.externalLoadBalancer.enabled | bool | `false` | Enable External Load Balancer for the Hive Metastore. If not set the .global._hopsworks.externalLoadBalancers.enabled will be used instead |
| hive.externalLoadBalancer.managed | string | `nil` | Cloud provider provisions Load Balancers. If not set the .global._hopsworks.externalLoadBalancers.managed will be used instead |
| hive.externalLoadBalancer.nodeSelector | object | `{}` | selector for nodes the load balancer can use to route traffic |
| hive.hopsworkslib | object | `{}` | override hopsworkslib values |
| hive.metastore.appName | string | `"hivemetastore"` |  |
| hive.metastore.config.cm_rootdir | string | `""` |  |
| hive.metastore.config.enforce_auth | bool | `true` |  |
| hive.metastore.config.hopsfs_dir | string | `"/apps/hive/warehouse"` |  |
| hive.metastore.config.hudi_hadoop_version | string | `"1.2.0"` |  |
| hive.metastore.config.impersonation | string | `"hive,glassfish"` |  |
| hive.metastore.config.mapreduce_input_size | string | `"134217728"` |  |
| hive.metastore.config.repl_rootdir | string | `""` |  |
| hive.metastore.config.scratch_dir | string | `"/tmp/hive"` |  |
| hive.metastore.configmap.name | string | `"hivemetastore-configmap"` |  |
| hive.metastore.create_secret | bool | `true` | Create the mysql users secret for hive metastore. If false, you have to create the secret (hive-user-secrets) manually. |
| hive.metastore.dependencies.glassfish.consulServiceName | string | `"glassfish"` |  |
| hive.metastore.dependencies.glassfish.consulServiceTag | string | `"hopsworks"` |  |
| hive.metastore.dependencies.glassfish.port | int | `8182` |  |
| hive.metastore.dependencies.mysql.consulServiceName | string | `"mysql"` |  |
| hive.metastore.dependencies.mysql.port | int | `3306` |  |
| hive.metastore.dependencies.namenode.consulServiceName | string | `"namenode"` |  |
| hive.metastore.dependencies.namenode.consulServiceTag | string | `"rpc"` |  |
| hive.metastore.dependencies.namenode.port | int | `8020` |  |
| hive.metastore.deployment.jvm_resources | object | `{"xms":"2g","xmx":"2g"}` | Xms and Xmx parameters for the Hivemetastore JVM initialization. Notice that, if set, container resources will be ignored and automatically calculated based on the values provided by this property. |
| hive.metastore.deployment.jvm_resources.xms | string | `"2g"` | Initial heap size for JVM (e.g., '0.5g', '1g', '1.5g') |
| hive.metastore.deployment.jvm_resources.xmx | string | `"2g"` | Maximum heap size for JVM (e.g., '0.5g', '1g', '1.5g') |
| hive.metastore.deployment.name | string | `"hivemetastore-deployment"` |  |
| hive.metastore.deployment.probes.liveness.initialDelaySeconds | int | `60` |  |
| hive.metastore.deployment.probes.liveness.periodSeconds | int | `10` |  |
| hive.metastore.deployment.probes.liveness.tcpSocket.port | int | `9083` |  |
| hive.metastore.deployment.probes.liveness.timeoutSeconds | int | `10` |  |
| hive.metastore.deployment.probes.readiness.initialDelaySeconds | int | `60` |  |
| hive.metastore.deployment.probes.readiness.periodSeconds | int | `10` |  |
| hive.metastore.deployment.probes.readiness.tcpSocket.port | int | `9083` |  |
| hive.metastore.deployment.probes.readiness.timeoutSeconds | int | `60` |  |
| hive.metastore.deployment.probes.startup | object | `{}` | startup probes |
| hive.metastore.deployment.rbac.annotations | object | `{}` | metrics rbac role annotations |
| hive.metastore.deployment.rbac.create | bool | `true` |  |
| hive.metastore.deployment.rbac.extraRoleRules | list | `[]` | extra rules to attach to metrics acl role |
| hive.metastore.deployment.rbac.name | string | `"hivemetastore-role"` |  |
| hive.metastore.deployment.rbac.useExistingRole | bool | `false` |  |
| hive.metastore.deployment.replicas | int | `1` |  |
| hive.metastore.deployment.resources.limits | object | `{"memory":"8192Mi"}` | resources limits configuration |
| hive.metastore.deployment.resources.requests | object | `{"cpu":"2","memory":"6553Mi"}` | resources requests configuration |
| hive.metastore.deployment.security.fsGroup | int | `1234` |  |
| hive.metastore.deployment.security.group | string | `"hive"` |  |
| hive.metastore.deployment.security.runAsGroup | int | `1234` |  |
| hive.metastore.deployment.security.runAsUser | int | `1516` |  |
| hive.metastore.deployment.security.user | string | `"hive"` |  |
| hive.metastore.deployment.serviceAccount.annotations | object | `{}` | service account annotations |
| hive.metastore.deployment.serviceAccount.create | bool | `true` |  |
| hive.metastore.deployment.serviceAccount.name | string | `"hivemetastore-default"` |  |
| hive.metastore.hadoop_user | string | `"hive"` |  |
| hive.metastore.image.pullPolicy | string | `"IfNotPresent"` |  |
| hive.metastore.image.registry | string | `"docker.hops.works"` |  |
| hive.metastore.logLevel | string | `"INFO"` |  |
| hive.metastore.migration.resources.limits.cpu | string | `"500m"` |  |
| hive.metastore.migration.resources.limits.memory | string | `"500Mi"` |  |
| hive.metastore.migration.resources.requests.cpu | string | `"100m"` |  |
| hive.metastore.migration.resources.requests.memory | string | `"100Mi"` |  |
| hive.metastore.migrationBackOffLimit | int | `10` | backoffLimit for hive migration job |
| hive.metastore.monitoring_port | int | `18002` |  |
| hive.metastore.nodeSelector | object | `{}` | node selector configuration |
| hive.metastore.podDisruptionBudget.enabled | bool | `true` |  |
| hive.metastore.podDisruptionBudget.minAvailable | int | `1` |  |
| hive.metastore.port | int | `9083` |  |
| hive.metastore.protocol | string | `"thrift"` |  |
| hive.metastore.service.annotations."consul.hashicorp.com/service-name" | string | `"hive"` |  |
| hive.metastore.service.annotations."consul.hashicorp.com/service-tags" | string | `"metastore,hiveserver2-tls,hiveserver2-plain"` |  |
| hive.metastore.service.name | string | `"metastore"` |  |
| hive.metastore.tolerations | list | `[]` |  |
| hive.metastore.topologySpreadConstraint | object | `{}` | The default topology spread constraint. If not defined the global topology spread constraint would be used instead. |
| hive.name | string | `"hive"` |  |
| hopsfs.bypassBucketValidation | bool | `false` | Do not run HopsFS bucket validation pre-install, pre-upgrade Job |
| hopsfs.cleanupOnUninstall | object | `{"enabled":true,"ttlSecondsAfterFinished":null}` | post-delete cleanup of HopsFS leftovers. The datanode StatefulSet PVC survives uninstall; this deletes it by its labels (app=hopsfs, service=datanode), but only when global._hopsworks.wipeDataOnUninstall is enabled and never for PVCs labelled hopsworks.ai/keep=true. |
| hopsfs.cleanupOnUninstall.enabled | bool | `true` | enable the post-delete HopsFS data-PVC cleanup hook (also requires global._hopsworks.wipeDataOnUninstall) |
| hopsfs.cleanupOnUninstall.ttlSecondsAfterFinished | string | `nil` | ttlSecondsAfterFinished for the cleanup Job; null falls through to the global default |
| hopsfs.client.failureReplacementPolicy | string | `"NEVER"` |  |
| hopsfs.client.locateFollowingBlockRetries | int | `10` |  |
| hopsfs.dataDir | string | `"/srv/hops/hopsdata/hdfs"` |  |
| hopsfs.datanode.count | int | `1` |  |
| hopsfs.datanode.dataPort | int | `50010` |  |
| hopsfs.datanode.gracefulDrain.enabled | bool | `true` | Enable the preStop drain hook when async cloud upload is on. Set false to opt out even when async is enabled; risks data loss under non-empty upload backlog. |
| hopsfs.datanode.gracefulDrain.terminationGracePeriodSecs | string | `nil` | Explicit override for the pod terminationGracePeriodSeconds. When null, defaults to the calculated drain timeout. |
| hopsfs.datanode.gracefulDrain.timeoutSecs | string | `nil` | Explicit override for the dfsadmin -timeout passed to the preStop drain RPC. When null, calculated from queueCapacity, blockSizeMiB, and uploadThroughputMiBps. |
| hopsfs.datanode.gracefulDrain.uploadThroughputMiBps | int | `35` | Operator estimate of per-DN S3 upload throughput in MiB/s. Drives the calculated drain timeout when timeoutSecs is null. |
| hopsfs.datanode.httpPort | int | `50075` |  |
| hopsfs.datanode.httpsPort | int | `50475` |  |
| hopsfs.datanode.ipcPort | int | `50020` |  |
| hopsfs.datanode.jvmOpts | string | `""` |  |
| hopsfs.datanode.loadBalancer.annotations | object | `{}` | annotations for load balancer |
| hopsfs.datanode.loadBalancer.enabled | string | `nil` | Enable External Load Balancers for datanode. If not set the .global._hopsworks.externalLoadBalancers.enabled will be used instead |
| hopsfs.datanode.loadBalancer.loadBalancerClass | string | `nil` | load balancer class name |
| hopsfs.datanode.loadBalancer.managed | string | `nil` | Cloud provider provisions Load Balancers. If not set the .global._hopsworks.externalLoadBalancers.managed will be used instead |
| hopsfs.datanode.monitoringPort | int | `50076` |  |
| hopsfs.datanode.nodeSelector | object | `{}` | node selector configuration |
| hopsfs.datanode.podDisruptionBudget.enabled | bool | `true` | Enable the DataNode PodDisruptionBudget. When enabled, the PDB hardcodes maxUnavailable=1 to prevent concurrent DN unavailability from exhausting HDFS client pipeline-recovery retries and failing in-flight writes. Not operator-tunable; this applies independently of async cloud upload. |
| hopsfs.datanode.podDisruptionBudget.minAvailable | int | `1` | DEPRECATED. The DN PDB no longer uses minAvailable; the template hardcodes maxUnavailable=1. Retained only so existing values overrides do not fail schema validation on upgrade. |
| hopsfs.datanode.resources.limits.cpu | string | `"4"` |  |
| hopsfs.datanode.resources.limits.memory | string | `"2048Mi"` |  |
| hopsfs.datanode.resources.requests.cpu | string | `"1"` |  |
| hopsfs.datanode.resources.requests.memory | string | `"500Mi"` |  |
| hopsfs.datanode.rpcHandlerCount | int | `20` |  |
| hopsfs.datanode.storage.size | string | `"100Gi"` |  |
| hopsfs.datanode.storage.storageClassName | string | `nil` | storage class name to request for volumes attached to the data nodes |
| hopsfs.datanode.tls.extraDnsNames | list | `[]` | Additional DNS names to add as SAN to Datanode x.509 certificate |
| hopsfs.datanode.tls.extraIpAddresses | list | `[]` | Additional IP addresses to add as SAN to Datanode x.509 certificate |
| hopsfs.datanode.tolerations | list | `[]` |  |
| hopsfs.datanode.topologySpreadConstraint | object | `{}` | The default topology spread constraint. If not defined the global topology spread constraint would be used instead. |
| hopsfs.datanode.xmx | int | `1024` |  |
| hopsfs.dependencies.glassfish.consulServiceName | string | `"glassfish"` |  |
| hopsfs.dependencies.glassfish.consulServiceTag | string | `"ca"` |  |
| hopsfs.dependencies.glassfish.port | int | `8182` |  |
| hopsfs.dependencies.mgmd.consulServiceName | string | `"mgmd"` |  |
| hopsfs.dependencies.mgmd.port | int | `1186` |  |
| hopsfs.dependencies.mysql.consulServiceName | string | `"mysql"` |  |
| hopsfs.dependencies.mysql.port | int | `3306` |  |
| hopsfs.dependencies.objectStorage.consulServiceName | string | `"minio"` |  |
| hopsfs.dependencies.objectStorage.port | int | `9000` |  |
| hopsfs.hopsworkslib | object | `{}` | override hopsworkslib values |
| hopsfs.image.name | string | `"hopsfs"` |  |
| hopsfs.image.pullPolicy | string | `"IfNotPresent"` |  |
| hopsfs.image.registry | string | `""` | Override the full registry+path prefix (must end with /). When set (non-empty), takes precedence over global._hopsworks.imageRegistry, bypassing the hardcoded /hopsworks/ segment. Use for custom HopsFS images at non-standard paths, e.g. "docker.hops.works/dev/salman/". Leave empty to use global._hopsworks.imageRegistry + "/hopsworks/". |
| hopsfs.image.tag | string | `"3.4.3.3-EE-RC0"` |  |
| hopsfs.log4j.console_logger_level | string | `"INFO"` | Log level threshold for Console appender. Defaults to root_level_logger if not specified. |
| hopsfs.log4j.enable_audit_log | bool | `true` |  |
| hopsfs.log4j.level | string | `"INFO"` | Backward compatibility field. Not used by log4j configuration. |
| hopsfs.log4j.rfa_logger_level | string | `"INFO"` | Log level threshold for Rolling File Appender. Defaults to root_level_logger if not specified. |
| hopsfs.log4j.rfa_max_backup_index | int | `10` | Maximum number of backup log files to keep |
| hopsfs.log4j.rfa_max_file_size | string | `"256MB"` | Maximum size of each log file before rotation (e.g., 256MB, 1GB) |
| hopsfs.log4j.root_level_logger | string | `"INFO"` | Root logger level - acts as a global minimum level for all appenders |
| hopsfs.namenode.acls.enabled | bool | `true` |  |
| hopsfs.namenode.auditLog.enableListOperation | bool | `false` |  |
| hopsfs.namenode.auditLog.enableStatOperation | bool | `false` |  |
| hopsfs.namenode.blockSizeMiB | int | `128` | HDFS block size in MiB. Templated into dfs.blocksize. Also drives the calculated DN graceful-drain timeout. |
| hopsfs.namenode.blockreportExecutorCount | int | `40` |  |
| hopsfs.namenode.clusterIp.name | string | `"namenode-cluster-ip"` |  |
| hopsfs.namenode.count | int | `1` |  |
| hopsfs.namenode.customConfig | object | `{}` | Set/Override hdfs-site.xml properties. Each entry in this map will template a <property></property> entry at the bottom of the hdfs-site.xml. The name of the property is the map entry key and the value of the property is the value of the map entry key. |
| hopsfs.namenode.dirs\[0\].group | string | `"hdfs"` |  |
| hopsfs.namenode.dirs\[0\].mode | int | `1775` |  |
| hopsfs.namenode.dirs\[0\].owner | string | `"payara"` |  |
| hopsfs.namenode.dirs\[0\].path | string | `"/Projects"` |  |
| hopsfs.namenode.dirs\[1\].group | string | `"hadoop"` |  |
| hopsfs.namenode.dirs\[1\].mode | int | `1775` |  |
| hopsfs.namenode.dirs\[1\].owner | string | `"hdfs"` |  |
| hopsfs.namenode.dirs\[1\].path | string | `"/user"` |  |
| hopsfs.namenode.dirs\[2\].group | string | `"hadoop"` |  |
| hopsfs.namenode.dirs\[2\].mode | int | `1775` |  |
| hopsfs.namenode.dirs\[2\].owner | string | `"hdfs"` |  |
| hopsfs.namenode.dirs\[2\].path | string | `"/apps"` |  |
| hopsfs.namenode.dirs\[3\].group | string | `"hadoop"` |  |
| hopsfs.namenode.dirs\[3\].mode | int | `1775` |  |
| hopsfs.namenode.dirs\[3\].owner | string | `"hdfs"` |  |
| hopsfs.namenode.dirs\[3\].path | string | `"/tmp"` |  |
| hopsfs.namenode.dirs\[4\].group | string | `"hadoop"` |  |
| hopsfs.namenode.dirs\[4\].mode | int | `1777` |  |
| hopsfs.namenode.dirs\[4\].owner | string | `"hive"` |  |
| hopsfs.namenode.dirs\[4\].path | string | `"/tmp/hive"` |  |
| hopsfs.namenode.httpPort | int | `50070` |  |
| hopsfs.namenode.httpsPort | int | `50470` |  |
| hopsfs.namenode.jvmOpts | string | `""` |  |
| hopsfs.namenode.loadBalancer.annotations | object | `{}` | annotations for load balancer |
| hopsfs.namenode.loadBalancer.enabled | string | `nil` | Enable External Load Balancers for namenode. If not set the .global._hopsworks.externalLoadBalancers.enabled will be used instead |
| hopsfs.namenode.loadBalancer.loadBalancerClass | string | `nil` | load balancer class name |
| hopsfs.namenode.loadBalancer.managed | string | `nil` | Cloud provider provisions Load Balancers. If not set the .global._hopsworks.externalLoadBalancers.managed will be used instead |
| hopsfs.namenode.maxBlocksPerFile | int | `10240` | Maximum number of blocks per file |
| hopsfs.namenode.maxDirectMemorySize | int | `1024` |  |
| hopsfs.namenode.maxDirectoryItems | int | `131072` | Maximum number of items (files and directories) allowed in a directory |
| hopsfs.namenode.monitoringPort | int | `50071` |  |
| hopsfs.namenode.nodeSelector | object | `{}` | node selector configuration |
| hopsfs.namenode.numBlockReplicas | int | `1` |  |
| hopsfs.namenode.podDisruptionBudget.enabled | bool | `true` |  |
| hopsfs.namenode.podDisruptionBudget.minAvailable | int | `1` |  |
| hopsfs.namenode.quotaEnabled | bool | `true` |  |
| hopsfs.namenode.resources.limits.cpu | string | `"4"` |  |
| hopsfs.namenode.resources.limits.memory | string | `"2560Mi"` |  |
| hopsfs.namenode.resources.requests.cpu | string | `"1"` |  |
| hopsfs.namenode.resources.requests.memory | string | `"1024Mi"` |  |
| hopsfs.namenode.rpcHandlerCount | int | `120` |  |
| hopsfs.namenode.rpcPort | int | `8020` |  |
| hopsfs.namenode.service.annotations."consul.hashicorp.com/service-name" | string | `"namenode"` |  |
| hopsfs.namenode.service.annotations."consul.hashicorp.com/service-port" | string | `"rpc"` |  |
| hopsfs.namenode.service.annotations."consul.hashicorp.com/service-tags" | string | `"rpc,http"` |  |
| hopsfs.namenode.service.annotations."prometheus.io/path" | string | `"/metrics"` |  |
| hopsfs.namenode.service.annotations."prometheus.io/port" | int | `50071` |  |
| hopsfs.namenode.service.annotations."prometheus.io/scheme" | string | `"http"` |  |
| hopsfs.namenode.service.annotations."prometheus.io/scrape" | string | `"true"` |  |
| hopsfs.namenode.service.name | string | `"namenode"` |  |
| hopsfs.namenode.setupBackOffLimit | int | `10` | Back off limit for database migration job. Default to be 10, i.e. 34 minutes, 30 seconds |
| hopsfs.namenode.startupProbe.failureThreshold | int | `50` |  |
| hopsfs.namenode.startupProbe.initialDelaySeconds | int | `10` |  |
| hopsfs.namenode.startupProbe.periodSeconds | int | `15` |  |
| hopsfs.namenode.startupProbe.timeoutSeconds | int | `10` |  |
| hopsfs.namenode.stoCleanFaildOpsDelay | int | `600000` |  |
| hopsfs.namenode.stoCleanSlowOpsDelay | int | `900000` |  |
| hopsfs.namenode.subtreeExecutorCount | int | `40` |  |
| hopsfs.namenode.tls.extraDnsNames | list | `[]` | Additional DNS names to add as SAN to Datanode x.509 certificate |
| hopsfs.namenode.tls.extraIpAddresses | list | `[]` | Additional IP addresses to add as SAN to Datanode x.509 certificate |
| hopsfs.namenode.tolerations | list | `[]` |  |
| hopsfs.namenode.topologySpreadConstraint | object | `{}` | The default topology spread constraint. If not defined the global topology spread constraint would be used instead. |
| hopsfs.namenode.txRetryCount | int | `10` |  |
| hopsfs.namenode.users\[0\].gid | int | `1508` |  |
| hopsfs.namenode.users\[0\].group | string | `"airflow"` |  |
| hopsfs.namenode.users\[0\].mode | int | `1750` |  |
| hopsfs.namenode.users\[0\].name | string | `"airflow"` |  |
| hopsfs.namenode.users\[0\].uid | int | `1512` |  |
| hopsfs.namenode.users\[1\].extra_folders\[0\] | string | `"/user/spark/applicationHistory"` |  |
| hopsfs.namenode.users\[1\].extra_folders\[1\] | string | `"/user/spark/eventlog"` |  |
| hopsfs.namenode.users\[1\].extra_folders\[2\] | string | `"/user/spark/share"` |  |
| hopsfs.namenode.users\[1\].extra_folders\[3\] | string | `"/user/spark/spark-warehouse"` |  |
| hopsfs.namenode.users\[1\].group | string | `"hadoop"` |  |
| hopsfs.namenode.users\[1\].mode | int | `1777` |  |
| hopsfs.namenode.users\[1\].name | string | `"spark"` |  |
| hopsfs.namenode.users\[1\].uid | int | `1505` |  |
| hopsfs.namenode.users\[2\].extra_folders\[0\] | string | `"/apps/hive"` |  |
| hopsfs.namenode.users\[2\].extra_folders\[1\] | string | `"/apps/hive/warehouse"` |  |
| hopsfs.namenode.users\[2\].group | string | `"hadoop"` |  |
| hopsfs.namenode.users\[2\].mode | int | `1755` |  |
| hopsfs.namenode.users\[2\].name | string | `"hive"` |  |
| hopsfs.namenode.users\[3\].group | string | `"hdfs"` |  |
| hopsfs.namenode.users\[3\].mode | int | `1750` |  |
| hopsfs.namenode.users\[3\].name | string | `"payara"` |  |
| hopsfs.namenode.users\[4\].extra_folders\[0\] | string | `"/user/ray/applications"` |  |
| hopsfs.namenode.users\[4\].group | string | `"hadoop"` |  |
| hopsfs.namenode.users\[4\].mode | int | `1750` |  |
| hopsfs.namenode.users\[4\].name | string | `"ray"` |  |
| hopsfs.namenode.users\[5\].group | string | `"hdfs"` |  |
| hopsfs.namenode.users\[5\].mode | int | `1750` |  |
| hopsfs.namenode.users\[5\].name | string | `"trino"` |  |
| hopsfs.namenode.xattrs.enabled | bool | `true` |  |
| hopsfs.namenode.xattrs.maxXAttrSize | int | `1039755` |  |
| hopsfs.namenode.xattrs.maxXAttrsPerInode | int | `32` |  |
| hopsfs.namenode.xmx | int | `1024` |  |
| hopsfs.nuke_db_in_retry | bool | `false` |  |
| hopsfs.objectStorage.asyncUpload.enabled | bool | `false` | Enable async cloud upload. dfs.cloud.async.upload.enabled (shared NN + DN scope) |
| hopsfs.objectStorage.azure.storage.account | string | `"hopsfsdatastore"` |  |
| hopsfs.objectStorage.azure.storage.container | string | `"hopsfs"` |  |
| hopsfs.objectStorage.azure.storage.enableSoftDeletes | bool | `false` |  |
| hopsfs.objectStorage.azure.storage.identityClientId | string | `"9cf39842-07c7-444a-8a44-63ee91411b70"` |  |
| hopsfs.objectStorage.azure.storage.softDeletesRetentionDays | int | `90` |  |
| hopsfs.objectStorage.blockReportDelay | int | `21600000` | dfs.cloud.block.report.delay |
| hopsfs.objectStorage.datanode.asyncUpload.queueCapacity | int | `1000` | Bounded async-upload queue size; overflow triggers sync fallback. dfs.cloud.dn.async.upload.queue.capacity |
| hopsfs.objectStorage.datanode.asyncUpload.retryCount | int | `3` | Retry attempts before re-enqueueing a failed upload at queue tail. dfs.cloud.dn.async.upload.retry.count |
| hopsfs.objectStorage.datanode.asyncUpload.retryIntervalMs | int | `30000` | Base backoff in ms between retries (exponential, capped at 5 min). dfs.cloud.dn.async.upload.retry.interval.ms |
| hopsfs.objectStorage.datanode.asyncUpload.threads | int | `8` | Async-upload worker pool size. dfs.cloud.dn.async.upload.threads |
| hopsfs.objectStorage.datanode.cache.bypass | bool | `false` |  |
| hopsfs.objectStorage.datanode.cache.deleteActivationPercentage | int | `70` |  |
| hopsfs.objectStorage.datanode.cache.deleteWait | int | `1200000` | Minimum block file age in milliseconds before a cached block is eligible for deletion. Prevents removing newly downloaded blocks that may still be served to remote clients. dfs.dn.cloud.cache.delete.wait |
| hopsfs.objectStorage.datanode.maxUploadThreads | int | `20` |  |
| hopsfs.objectStorage.enabled | bool | `true` |  |
| hopsfs.objectStorage.gcs.bucket.enableVersioning | bool | `true` |  |
| hopsfs.objectStorage.gcs.bucket.location | string | `"europe-north1"` |  |
| hopsfs.objectStorage.gcs.bucket.name | string | `"hopsfs"` |  |
| hopsfs.objectStorage.markBlocksCorruptOrMissingAfter | int | `3600000` | dfs.cloud.mark.blocks.corrupt.or.missing.after |
| hopsfs.objectStorage.numCommittedAllowed | int | `1` | When using cloud storage, setting this to 1 allows NN to verify a block on cloud instead of waiting for DN signal. |
| hopsfs.objectStorage.provider | string | `""` | object storage provicer, possible values are \["S3", "AZURE", "GCS"\] |
| hopsfs.objectStorage.restoreFromBackup | string | `nil` | restore from backup flag which instructs HopsFS to roll backed deleted blocks |
| hopsfs.objectStorage.s3.bucket.aclBucketOwnerFullControl | bool | `false` |  |
| hopsfs.objectStorage.s3.bucket.encryption.bucketKeyEnabled | bool | `true` |  |
| hopsfs.objectStorage.s3.bucket.encryption.enabled | bool | `false` |  |
| hopsfs.objectStorage.s3.bucket.encryption.mode | string | `"SSE-KMS"` | s3 encryption mode, possible values are \[SSE-S3, SSE-KMS\] |
| hopsfs.objectStorage.s3.bucket.encryption.userKeyARN | string | `""` |  |
| hopsfs.objectStorage.s3.bucket.name | string | `""` |  |
| hopsfs.objectStorage.s3.bucket.versioning | string | `nil` | versioning is enabled or disabled. If global backup is enabled then versioning will be set to be enabled by default unless overriden on the HopsFS subchart.  |
| hopsfs.objectStorage.s3.bypassGovernanceRetention | bool | `false` |  |
| hopsfs.objectStorage.s3.credentialsSecret | object | `{"access_key_id":"","name":"","secret_key_id":""}` | credentials secret configuration. If not defined the global._hopsworks.managedObjectStorage.s3.secret configuration will be used instead |
| hopsfs.objectStorage.s3.credentialsSecret.access_key_id | string | `""` | Defaults to access-key-id |
| hopsfs.objectStorage.s3.credentialsSecret.name | string | `""` | Default to aws-credentials |
| hopsfs.objectStorage.s3.credentialsSecret.secret_key_id | string | `""` | Defaults to secret-access-key |
| hopsfs.objectStorage.s3.disableCertChecking | bool | `false` | disable TLS certificate checking for the S3 endpoint (useful with self-signed certs / MinIO) |
| hopsfs.objectStorage.s3.disableChecksumValidation | bool | `false` | disable client-side checksum validation for S3 objects |
| hopsfs.objectStorage.s3.endpoint | string | `nil` | s3 provider endpoint |
| hopsfs.objectStorage.s3.region | string | `""` |  |
| hopsfs.objectStorage.s3.signingRegion | string | `nil` | s3 provider signing region |
| hopsfs.objectStorage.storeSmallFilesInDB | bool | `false` |  |
| hopsfs.parallel_preset | int | `3` |  |
| hopsfs.presetJob.clientRetryCount | int | `10` |  |
| hopsfs.presetJob.clientRetryIntervalSeconds | int | `10` |  |
| hopsfs.presetJob.runIndex | int | `0` | Index to make job names unique if necessary |
| hopsfs.presetJob.ttlSecondsAfterFinished | string | `nil` | TTL in seconds for the namenode-preset-folders Job. Overrides global default. |
| hopsfs.security.fsGroup | int | `1234` |  |
| hopsfs.security.runAsGroup | int | `1234` |  |
| hopsfs.security.runAsUser | int | `1506` |  |
| hopsfs.security.securityActions.maxConnectionsPerRoute | int | `30` | Maximum number of concurrent HTTP connections to Hopsworks CA. Currently used only by WebHDFS |
| hopsfs.security.tde | object | `{"enabled":false,"kmsUri":""}` | Configuration for Transparent Data Encryption |
| hopsfs.security.tde.enabled | bool | `false` | Flag to enable encryption-at-rest |
| hopsfs.security.tde.kmsUri | string | `""` | KMS URI when encryption-at-rest is enabled ie http://10.1.1.2:9600 |
| hopsfs.security.tls.enabled | bool | `true` |  |
| hopsfs.serviceAccount.annotations | object | `{}` | service account annotations |
| hopsfs.setupJob.timeoutMinutes | int | `25` |  |
| hopsfs-csi.cleanupOnUninstall | object | `{"enabled":true,"ttlSecondsAfterFinished":null}` | post-delete cleanup of what `helm uninstall` does not own: the CSIDriver object (a pre-install hook, HWORKS-3285) and, on OpenShift, the node plugin's SCC. Best effort: a failed delete is logged, not a failed uninstall. The CSIDriver is cluster-scoped and shared by every release of this chart in the cluster, so it is deleted only when its Helm annotations name the uninstalled release and no other release's node plugin pods exist. The hw-kyverno PolicyException for the plugin, if enabled, is still left behind. A reinstall does not depend on this hook. |
| hopsfs-csi.cleanupOnUninstall.enabled | bool | `true` | enable the post-delete cleanup hook |
| hopsfs-csi.cleanupOnUninstall.ttlSecondsAfterFinished | int or null | `nil` | TTL of the finished hook Job; null falls through to the global default |
| hopsfs-csi.fullnameOverride | string | `"hopsfs-csi"` | override the full chart name |
| hopsfs-csi.hopsworkslib | object | `{}` | override hopsworkslib values |
| hopsfs-csi.image | object | `{"pullPolicy":"IfNotPresent","registry":"docker.hops.works","repository":"hopsworks/hopsfs-csi","tag":"0.1.0-SNAPSHOT"}` | The hopsfs-csi image, run by the node plugin. The same image is the workload FUSE sidecar (Hopsworks-generated pods, Airflow, Trino): the fusermount3 proxy in the sidecar and the fd server in the plugin are two halves of one protocol, so the two ends must never drift on a node. Under the umbrella chart every field here is overridden by the single `global._hopsworks.csi.image` block (and `global._hopsworks.imageRegistry` for the registry), which is also what the sidecars and the Hopsworks `csi_sidecar_image` variable are seeded from. The chart is only installed through the umbrella, so set the global rather than these. |
| hopsfs-csi.nameOverride | string | `"hopsfs-csi"` | override the chart name |
| hopsfs-csi.node.kubeletRootDir | string | `"/var/lib/kubelet"` |  |
| hopsfs-csi.node.priorityClassName | string | `"system-node-critical"` | priorityClassName of the node plugin pods. system-node-critical so a full node never evicts the plugin (a node without it cannot start any CSI-mounted pod) and so it is scheduled before the workloads that depend on it. |
| hopsfs-csi.node.resources.limits.cpu | string | `"500m"` |  |
| hopsfs-csi.node.resources.limits.memory | string | `"256Mi"` |  |
| hopsfs-csi.node.resources.requests.cpu | string | `"50m"` |  |
| hopsfs-csi.node.resources.requests.memory | string | `"64Mi"` |  |
| hopsfs-csi.node.serviceAccount.create | bool | `true` |  |
| hopsfs-csi.node.serviceAccount.name | string | `"hopsfs-csi-node-sa"` |  |
| hopsfs-csi.node.terminationGracePeriodSeconds | int | `300` | How long kubelet lets a stopping plugin pod run before killing it. When the plugin is removed together with the pods that mount through it (helm uninstall, namespace delete), it keeps serving kubelet's unmounts until none is left and exits then, so this is only ever used up when a consumer is itself stuck; a plugin that is merely being replaced (rollout, eviction) exits at once. Set it above the longest terminationGracePeriodSeconds of any HopsFS-mounting pod, or those pods hang in Terminating after the plugin is gone (HWORKS-3287). |
| hopsfs-csi.nodeSelector | object | `{}` | nodeSelector of the node plugin DaemonSet. Deliberately NOT inherited from global._hopsworks.nodeSelector: that selector pins the Hopsworks services to their nodes, while the plugin must run on every node a HopsFS-mounting pod can land on (job and GPU pools included), or those pods hang in ContainerCreating. Set it only to keep the plugin off nodes that will never run such a pod. |
| hopsfs-csi.openshift | object | `{"csiEphemeralVolumeProfile":"restricted","existingSecurityContextConstraints":{"check":{"enabled":true,"ttlSecondsAfterFinished":null},"name":""},"securityContextConstraints":false}` | OpenShift-only settings of the node plugin: the CSI Volume Admission profile label on the CSIDriver and whether to ship a SecurityContextConstraints for the plugin's service account. |
| hopsfs-csi.openshift.csiEphemeralVolumeProfile | string | `"restricted"` | OpenShift CSI Volume Admission profile for inline ephemeral volumes, emitted as the security.openshift.io/csi-ephemeral-volume-profile label on the CSIDriver. Must be one of restricted, baseline or privileged and must not be empty on OpenShift: an absent label makes the CSIInlineVolumeSecurity admission plugin require enforce=privileged of every namespace that mounts the driver, which rejects every Airflow and Trino pod. `restricted` is correct for this driver (see templates/csidriver.yaml for why) and the label is inert off OpenShift. |
| hopsfs-csi.openshift.existingSecurityContextConstraints | object | `{"check":{"enabled":true,"ttlSecondsAfterFinished":null},"name":""}` | Let the cluster administrators own the node plugin's SCC instead of this chart. Off by default: the chart ships the SCC (securityContextConstraints above). Setting `name` to the SCC the administrators created turns the shipped one off, whatever securityContextConstraints and global._hopsworks.openshift.enabled say, keeps the post-delete cleanup off it, and adds a pre-install/pre-upgrade hook Job that fails the release early, with the reason in its log, when that SCC is missing or does not admit the plugin. Without the check a wrong SCC leaves the DaemonSet with no pods and every CSI-mounted workload in ContainerCreating, with no event naming the cause. The Job runs a PodSecurityPolicySubjectReview of the exact DaemonSet pod template for the plugin's service account (users, groups and RBAC `use` grants all count; the account need not exist yet), and a server-side dry-run create of a representative HopsFS-mounting workload pod in the release namespace: the unprivileged FUSE sidecar at global._hopsworks.executor_uid plus an inline csi volume of this driver, which also exercises the CSI Volume Admission plugin against the CSIDriver's profile label (HWORKS-3285) and restricted-v2's uid range. The reference manifest to hand to the administrators is the chart's own: `helm template . --set hopsfs-csi.openshift.securityContextConstraints=true --show-only charts/hopsfs-csi/templates/scc.yaml`; whatever they derive from it has to grant `system:serviceaccount:<release namespace>:hopsfs-csi-node-sa`. |
| hopsfs-csi.openshift.existingSecurityContextConstraints.check | object | `{"enabled":true,"ttlSecondsAfterFinished":null}` | the pre-install/pre-upgrade admission check, run only when `name` is set |
| hopsfs-csi.openshift.existingSecurityContextConstraints.check.enabled | bool | `true` | run the check. Off only to install against an SCC the OpenShift review API cannot evaluate; the install then fails late, in the DaemonSet, if the SCC is wrong. |
| hopsfs-csi.openshift.existingSecurityContextConstraints.check.ttlSecondsAfterFinished | int or null | `nil` | TTL of the finished hook Job; null falls through to the global default |
| hopsfs-csi.openshift.existingSecurityContextConstraints.name | string | `""` | name of the administrator-created SecurityContextConstraints; empty, the default, means the chart ships its own |
| hopsfs-csi.openshift.securityContextConstraints | bool | `false` | Ship a SecurityContextConstraints granting the node plugin's service account what the DaemonSet needs on OpenShift (privileged, hostPath volumes, Bidirectional mount propagation, root); without it restricted-v2 rejects the plugin pod and every CSI-mounted workload sits in ContainerCreating. Rendered when this is true or global._hopsworks.openshift.enabled is true. Cluster-scoped and named after the release so two installs do not collide. Off, together with the global, when existingSecurityContextConstraints.name is set. |
| hopsfs-csi.sidecars | object | `{"livenessProbe":{"pullPolicy":"IfNotPresent","repository":"registry.k8s.io/sig-storage/livenessprobe","resources":{"limits":{"cpu":"100m","memory":"128Mi"},"requests":{"cpu":"10m","memory":"64Mi"}},"tag":"v2.16.0"},"nodeDriverRegistrar":{"pullPolicy":"IfNotPresent","repository":"registry.k8s.io/sig-storage/csi-node-driver-registrar","resources":{"limits":{"cpu":"400m","memory":"512Mi"},"requests":{"cpu":"40m","memory":"128Mi"}},"tag":"v2.14.0"},"registry":"docker.hops.works"}` | The sig-storage helper containers next to the node plugin. |
| hopsfs-csi.sidecars.registry | string | `"docker.hops.works"` | The mirror the sig-storage images are pulled from (they keep their upstream registry.k8s.io/... path under it). Overridden by global._hopsworks.imageRegistry under the umbrella chart, so an air-gapped install only sets the global. |
| hopsfs-csi.tolerations | list | `[{"operator":"Exists"}]` | tolerations of the node plugin DaemonSet. `operator: Exists` tolerates every taint for the reason above; narrow it only together with nodeSelector. |
| hopsworks.agent_email | string | `"agent@hops.io"` |  |
| hopsworks.agent_password | string | `"admin"` |  |
| hopsworks.buildkitd.gc.cacheMountKeepBytes | string | `"20GiB"` | Budget for package cache mounts, kept separate so they cannot evict base image snapshots. Scale by the number of projects that build custom environments, not by total projects. Every size here is binary and comparable to buildkitd.storage, since the two are weighed against each other. Spell it "GiB" and not the Kubernetes "Gi": BuildKit parses these with docker/go-units, which rejects a bare "Gi" and refuses to start the daemon. |
| hopsworks.buildkitd.gc.cacheMountKeepDuration | string | `"168h"` |  |
| hopsworks.buildkitd.gc.keySyntax | string | `"maxUsedSpace"` | Which GC key names to emit: "keepBytes" for BuildKit up to ~v0.16, "maxUsedSpace" for later releases. Must match the deployed BuildKit, and getting it wrong is silent rather than loud: v0.31.2 still accepts keepBytes, but maps it to reservedSpace, which is a floor and not a ceiling (cmd/buildkitd/config: "Deprecated: use ReservedSpace instead"). Emitting keepBytes against a modern daemon therefore turns the budget below into an amount that is guaranteed to be kept rather than never exceeded, and the state volume fills. Explicit rather than inferred from the tag, because the tag can point at a mirror of any version. Constrained by the schema: a typo used to fall through to the maxUsedSpace branch silently, which is the failure this key exists to prevent. |
| hopsworks.buildkitd.gc.minFreeSpace | string | `"10GiB"` | Free space the collector tries to leave on the volume, never going below what the policies above guarantee. The only budget here expressed against actual free space rather than against BuildKit's accounting of its own records, so it is the backstop for the daemon's other state on the volume, which no gcpolicy covers. Empty omits it. |
| hopsworks.buildkitd.gc.totalKeepBytes | string | `"60GiB"` | Total retained. Must stay well above the unpacked size of every base image served, and together with cacheMountKeepBytes must leave headroom under buildkitd.storage. GC is reactive, so a burst overshoots the threshold before collection catches up, and a full state volume gives ENOSPC on snapshot writes: on a ReadWriteOnce PVC recovery is volume expansion or deleting the PVC and cold-starting every base image snapshot and cache. |
| hopsworks.buildkitd.image | string | `""` | Daemon image name. Empty falls back to dockerRegistry.buildkit.image. |
| hopsworks.buildkitd.insecureRegistries | list | `[]` | Registries the daemon should treat as insecure, e.g. the in-cluster registry when it is served over plain HTTP. |
| hopsworks.buildkitd.maxParallelism | int | `4` | Concurrent build steps the daemon will run. Bounds peak memory at roughly this many per-build peaks, so overload becomes slow instead of an OOMKill that fails every in-flight build. It does not bound the number of build Jobs: further builds still hold a client pod and a blocked backend thread, so this protects the daemon rather than the cluster. Size it against memory, not CPU. BuildKit's own documented example, and conservative against a heavy wheel or CUDA build peaking near 2Gi. |
| hopsworks.buildkitd.name | string | `"buildkitd"` |  |
| hopsworks.buildkitd.nodeSelector | object | `{}` |  |
| hopsworks.buildkitd.podAnnotations | object | `{}` | Extra annotations on the daemon pod. Exists mainly for CRI-O's workload activation route: when a node scopes allowed_annotations to a \[crio.runtime.workloads.*\] table rather than a runtime handler, the pod must carry that workload's activation_annotation for the device annotation to be honoured. See values.rhel8.yaml. |
| hopsworks.buildkitd.port | int | `1234` |  |
| hopsworks.buildkitd.priorityClass.create | bool | `true` | Create a priority class for shared Hopsworks services that user workloads depend on. The daemon needs one: it is now the pod that does the building, while its own build Jobs run at docker_operations_buildkit_priority_class. Without it the daemon sits at priority 0 and a burst of build Jobs can preempt the very daemon they are about to talk to, which fails every in-flight build including the ones that displaced it. Turning this off is only safe if the build Jobs are left at priority 0 too. |
| hopsworks.buildkitd.priorityClass.value | int | `1000000` | Must not be below the build Jobs' priority (docker_operations_buildkit_priority_class, 0 by default): the scheduler only preempts a lower priority, so a daemon below its own clients can be evicted by a burst of build Jobs. |
| hopsworks.buildkitd.priorityClassName | string | `""` | Priority class for the daemon. Empty uses the chart's own core-service class when priorityClass.create is on, which is the default; set a name to override it, or disable creation and leave this empty to run at priority 0 as before. |
| hopsworks.buildkitd.registry | string | `""` | Registry for the daemon image. Empty uses the chart's usual registry. Set this when the daemon runs a different BuildKit version from the per-build image, which is mirrored separately. |
| hopsworks.buildkitd.replicas | int | `1` | Each replica gets its own ReadWriteOnce state volume. Projects are pinned to a replica by id, so a project keeps hitting the daemon that already unpacked its base image. The address and replica count are filled in from here.  Pinning is what makes the cache useful and is also why this is not failover: a project is not retried against another replica, and a project that builds far more than the others stays on the one daemon. |
| hopsworks.buildkitd.resources | object | `{"limits":{"cpu":"8","memory":"16Gi"},"requests":{"cpu":"8","memory":"16Gi"}}` | Requests equal limits, so the daemon is Guaranteed rather than Burstable. It is the shared build bottleneck for every project, and node-pressure eviction ranks by QoS class first and then by usage above request: Burstable with a 2 CPU request and an 8 CPU limit made it both first to evict and capped at 2 CPUs of sustained capacity on a contended node, which is the opposite of what the spread suggested. Raise both together on a dedicated builder node. |
| hopsworks.buildkitd.rootless.deviceInjection | string | `"none"` | How the daemon is given /dev/fuse, which fuse-overlayfs needs. Kubernetes has no portable PodSpec equivalent of docker --device, so this is necessarily runtime-specific.    none          no device. The daemon must then use the native snapshotter, which copies                 whole layers instead of stacking them: correct, much slower, much larger.   crio          adds the io.kubernetes.cri-o.Devices annotation, which CRI-O honours.   devicePlugin  requests devicePluginResource below, for a device plugin or CDI that                 advertises /dev/fuse on upstream Kubernetes.  A plain hostPath is deliberately not offered. It makes the device node visible and leaves every open returning EPERM, which looks like it works right up until a build runs. Measured on a containerd cluster: the node appears as crw-rw-rw- and the open fails.  Asking for the fuse-overlayfs snapshotter with this set to none is refused at template time rather than deployed, since the daemon would either fail to start or quietly do something else. Nothing here is exercised on an enforcing-SELinux node yet; expect to need a matching SCC or policy there. |
| hopsworks.buildkitd.rootless.devicePluginResource | string | `"github.com/fuse"` | Resource requested when deviceInjection is devicePlugin. The name comes from whichever plugin or CDI provider is installed; there is no standard one. Must be a qualified extended-resource name (domain/name): an empty value would render a resources entry Kubernetes rejects, so the chart refuses it. |
| hopsworks.buildkitd.rootless.enabled | bool | `false` | Run the daemon as an unprivileged user instead of as root with privileged: true.  Off by default. Switching an existing install is a one-way, disruptive change: the rootless daemon keeps its state in its own subdirectory of the volume, so it starts cold and unpacks every base image again, and the rootful tree stays on the volume taking space until the volume is replaced. Switching back has the mirror-image cost. Size buildkitd.storage for one tree, not two, and give the StatefulSet a fresh volume when the extra copy does not fit.  What it costs, and this is more than a performance note. The daemon loses the process sandbox for RUN steps (--oci-worker-no-process-sandbox), which is the price of not needing privileged. A RUN step then shares the daemon's PID namespace at the same uid, so it can signal and potentially ptrace the daemon, and through /proc/<pid>/root reach the daemon's mount namespace, where the mTLS private key is. One daemon also holds every project's build state and cache.  So this mode is for a single trust zone only. Do not enable it where concurrent projects are mutually untrusted. Losing the daemon to a build step is an accepted denial of service; the credential reachability is what bounds where the mode may be used.  It buys back: no host root, no privileged container, and no hostPID, which also means a daemon cannot outlive its container and strand the state lock.  Requires a kernel that supports the configured snapshotter unprivileged. Rootless overlayfs needs 5.11 or later; below that, set variables.docker_operations_oci_worker_snapshotter to "native" and expect slower builds.  fuse-overlayfs is the faster fallback on those kernels, and it needs the daemon to actually hold /dev/fuse. See deviceInjection below: a hostPath is not enough, because access is governed by the container's device cgroup rather than by the filesystem. |
| hopsworks.buildkitd.rootless.preflight | bool | `true` | Run a preflight check before the daemon starts, so a node that cannot support the requested configuration fails at once and says why, rather than degrading silently. Verifies node-level facts: unprivileged user namespaces, and kernel FUSE support when the configuration actually uses FUSE (fuse-overlayfs, or any device injection). The /dev/fuse open check is not here: it runs in the daemon container's own entrypoint, because a device plugin allocates per container and the device never reaches an init container. Only meaningful when rootless is on. |
| hopsworks.buildkitd.rootless.tagSuffix | string | `"-rootless"` | Appended to the daemon image tag when rootless is on, since upstream ships the rootless daemon as a separate image variant. An explicit buildkitd.tag overrides this. |
| hopsworks.buildkitd.rootless.user | int | `1000` | uid and gid the rootless image runs as, and the pod's fsGroup, which is what makes the state volume and the certificate mount readable without an init container that chowns the whole volume. |
| hopsworks.buildkitd.serviceAccountName | string | `""` | Service account for the daemon pod. Empty runs it as the namespace default with no token mounted, which is what it needs to build. Set it only to give the daemon a cloud identity of its own, for instance an IRSA-annotated account so a registry cache export can reach S3.  The daemon's identity is not the build pod's. Builds run as hopsworks-default, so an annotation applied through defaultServiceAccount.annotations reaches them and not this StatefulSet. That distinction only appears once the daemon moves out of the build pod, and it is the reason an S3 exporter that worked daemonless can stop working here. |
| hopsworks.buildkitd.storage | string | `"100Gi"` | Must comfortably exceed the total unpacked size of the base images in use, plus the package cache. Below that, each build evicts the base image the next one needs and the cache is slower than none. |
| hopsworks.buildkitd.storageClassName | string | `""` |  |
| hopsworks.buildkitd.tag | string | `""` | Daemon image tag. Empty falls back to dockerRegistry.buildkit.tag. |
| hopsworks.buildkitd.tls.enabled | bool | `true` | Require client certificates. On by default, and only worth turning off on a single-tenant install: buildctl over TCP is otherwise unauthenticated, and buildkitd gives RUN steps host networking, so a build step reaches the daemon on both the service address and 127.0.0.1 and the NetworkPolicy below does not contain it. Verified on a cluster: with mTLS the connection is closed before the API answers, and the client key lives in the build job pod rather than the RUN filesystem, so user code cannot present it. |
| hopsworks.buildkitd.tls.locality | string | `"buildkitd"` |  |
| hopsworks.buildkitd.tolerations | list | `[]` |  |
| hopsworks.cleanupOnUninstall | object | `{"enabled":true,"ttlSecondsAfterFinished":null}` | post-delete cleanup of Hopsworks runtime leftovers (CA/setup-script Secrets & ConfigMaps annotated hopsworks.ai/project, plus the sql-dml/sql-grants/flyway-config hook ConfigMaps) that Helm/ArgoCD never tracked and so never prune. |
| hopsworks.cleanupOnUninstall.enabled | bool | `true` | enable the post-delete Hopsworks cleanup hook |
| hopsworks.cleanupOnUninstall.ttlSecondsAfterFinished | string | `nil` | ttlSecondsAfterFinished for the cleanup Job; null falls through to the global default |
| hopsworks.create_certificate.add | list | `[]` | the following list is used to add additional certificates to trust. Notice this wont work in air gapped. An example   - name: azure    url: https://cacerts.digicert.com/DigiCertAssuredIDRootG2.crt    alias: digicertglobalrootg2 |
| hopsworks.create_certificate.auto_generate | bool | `true` |  |
| hopsworks.create_certificate.cn | string | `"hopsworks.local.ai"` |  |
| hopsworks.create_certificate.configmap | string | `"payara-cacerts"` |  |
| hopsworks.create_certificate.enabled | bool | `false` |  |
| hopsworks.create_certificate.secretName | string | `"hopsworks-tls"` |  |
| hopsworks.create_certificate.trustManager.aliasPrefix | string | `"trust-manager"` |  |
| hopsworks.create_certificate.trustManager.configMapName | string | `""` |  |
| hopsworks.create_certificate.trustManager.enabled | bool | `false` |  |
| hopsworks.create_certificate.trustManager.key | string | `"ca-bundle.crt"` |  |
| hopsworks.create_secrets | bool | `true` | If false, you have to create the secret for the hopsworks users (hopsworks-users-secrets) manually. If false and ldap/kerberos is enabled, the secret for ldap credentials must be created manually as well. |
| hopsworks.ddlConfigmapName | string | `"sql-ddl"` |  |
| hopsworks.defaultServiceAccount.annotations | object | `{}` | annotations |
| hopsworks.defaultServiceAccount.create | bool | `true` |  |
| hopsworks.dependencies.logstash.consulServiceName | string | `"logstash"` |  |
| hopsworks.dependencies.logstash.port | int | `5044` |  |
| hopsworks.dependencies.mysql.consulServiceName | string | `"mysql"` |  |
| hopsworks.dependencies.mysql.consulServiceTag | string | `"onlinefs"` |  |
| hopsworks.dependencies.mysql.port | int | `3306` |  |
| hopsworks.dependencies.objectStorage.consulServiceName | string | `"minio"` |  |
| hopsworks.dependencies.objectStorage.port | int | `9000` |  |
| hopsworks.dependencies.registry.consulServiceName | string | `"registry"` |  |
| hopsworks.dependencies.registry.port | int | `30443` |  |
| hopsworks.dockerImage.apt.sources | list | `[]` | The sources will be injected in case the user wants to use a proxy repo. |
| hopsworks.dockerImage.conda.default_mirrors | list | `[]` | the following mirrors will be injected in case the user wants to use a custom registry |
| hopsworks.dockerImage.conda.envs_dirs\[0\] | string | `"/envs"` |  |
| hopsworks.dockerImage.conda.pkgs_dirs\[0\] | string | `"/pkgs"` |  |
| hopsworks.dockerImage.conda.proxy.enabled | bool | `false` |  |
| hopsworks.dockerImage.conda.proxy.protocol | string | `"http"` |  |
| hopsworks.dockerImage.conda.proxy.url | string | `"http://proxy:3128"` |  |
| hopsworks.dockerImage.conda.repo_data_ttl | int | `43200` |  |
| hopsworks.dockerImage.conda.ssl_verify | string | `"True"` |  |
| hopsworks.dockerImage.conda.use_defaults | bool | `true` |  |
| hopsworks.dockerImage.configMap.name | string | `"docker-images-config"` |  |
| hopsworks.dockerImage.packageAuth | object | `{"caCertsConfigMap":"","secretName":""}` | Optional Secret with credentials for authenticated pip/apt mirrors. The Secret must be created out-of-band in the Hopsworks release namespace and may contain any of the following keys (both optional):   netrc         -- mounted at $HOME/package-auth/netrc,         staged as .netrc                    into env-build contexts (used by pip/conda).   apt-auth.conf -- mounted at $HOME/package-auth/apt-auth.conf, staged as                    /etc/apt/auth.conf.d/hopsworks.conf in env-build contexts. When the Secret is absent the env-build proceeds against anonymous mirrors. |
| hopsworks.dockerImage.packageAuth.caCertsConfigMap | string | `""` | Optional ConfigMap of trusted CA certificates to install into env-build Docker RUN steps. Each key in the ConfigMap is treated as a .crt / PEM file, bind-mounted into /usr/local/share/ca-certificates/ and installed via `update-ca-certificates` at the start of the RUN. Also exported as REQUESTS_CA_BUNDLE / SSL_CERT_FILE so pip/conda honour it. Leave empty to skip CA injection. |
| hopsworks.dockerImage.packageAuth.secretName | string | `""` | Name of an optional Secret in the Hopsworks release namespace containing credentials for authenticated pip/apt mirrors. Leave empty to skip credential injection. |
| hopsworks.dockerImage.pypi | object | `{"global_parameters":null,"pythonDownloads":"never"}` | pypi configurations global_parameters:   trusted-host: pypi.org   index-url: "https://pypi.org/simple"   extra-index-url: "https://pypi.org/simple"   proxy: "http://proxy:3128" Written verbatim to pip.conf, and translated into uv's own format in uv.toml because uv reads neither pip.conf nor PIP_INDEX_URL. These keys translate: trusted-host, proxy, index-url, extra-index-url, find-links, no-index, no-cache-dir, cache-dir, keyring-provider, index-strategy, require-hashes, pre. Anything else reaches pip only, and is listed in a comment at the end of uv.toml. timeout, retries, cert and client-cert have no uv equivalent; add trust roots through dockerImage.caCertsConfigMap instead of cert, which uv does honour. index-strategy is uv-only: pip searches every index and takes the highest version, while uv stops at the first index carrying the package. Set it to unsafe-best-match for pip's behaviour, at the cost of uv's dependency-confusion protection. |
| hopsworks.dockerImage.pypi.global_parameters | string | `nil` | pypi global parameters |
| hopsworks.dockerImage.pypi.pythonDownloads | string | `"never"` | uv's python-downloads. "never" is the default and the air-gap-safe value: an environment build installs against an interpreter the base image already has, so a request uv cannot satisfy locally means a broken base image, and the alternative to failing is uv silently fetching a standalone interpreter from GitHub. Relax this only on a cluster that is meant to reach the internet and wants uv to manage interpreters. |
| hopsworks.dockerRegistry.buildkit.image | string | `"moby/buildkit"` |  |
| hopsworks.dockerRegistry.buildkit.tag | string | `"v0.32.2"` | Do not go below v0.31.2. Earlier releases carry published advisories, two of which matter more with the persistent daemon: a Git URL subdirectory path traversal, reachable because a library can be installed from a user-supplied Git URL, and a state-directory escape via a custom frontend, whose blast radius is every project once one daemon holds the state for all of them. Both fixed in v0.28.1; v0.31.2 also covers a Seccomp/AppArmor bypass, an unbounded-parsing DoS and a command injection through Git bundle checkout. A per-build daemon is affected the same way, so this is not a reason to leave the persistent one off.  Most of what a scanner reports on this image is the four `buildkit-cni-*` plugins, which no BuildKit release refreshes and which never run here: the image ships no CNI config, so buildkitd falls back to host networking.  The rootless variant is a separate image, used only when buildkitd.rootless.enabled is on. Both move together.  Moving this pin means revisiting buildkitd.gc.keySyntax, which is version dependent. |
| hopsworks.dockerRegistry.preset.affinity | object | `{}` | affinity configuration |
| hopsworks.dockerRegistry.preset.alternativeRegistry | string | `nil` | Alternative registry URL for base images. It will override any other global registry URL configuration. |
| hopsworks.dockerRegistry.preset.configMapName | string | `"docker-images-preset-config"` |  |
| hopsworks.dockerRegistry.preset.enabled | bool | `true` |  |
| hopsworks.dockerRegistry.preset.env | list | `[]` | Additional env vars to be set in the preset docker images (e.g. Proxy configuration) |
| hopsworks.dockerRegistry.preset.extra_images | list | `[]` |  |
| hopsworks.dockerRegistry.preset.maxPushRetries | int | `5` |  |
| hopsworks.dockerRegistry.preset.nodeSelector | object | `{}` | node selector configuration |
| hopsworks.dockerRegistry.preset.parallelPushes | int | `1` |  |
| hopsworks.dockerRegistry.preset.parallelism | int | `3` |  |
| hopsworks.dockerRegistry.preset.resources.limits.cpu | string | `"1"` |  |
| hopsworks.dockerRegistry.preset.resources.limits.memory | string | `"3G"` |  |
| hopsworks.dockerRegistry.preset.resources.requests.cpu | string | `"100m"` |  |
| hopsworks.dockerRegistry.preset.resources.requests.memory | string | `"500Mi"` |  |
| hopsworks.dockerRegistry.preset.restartPolicy | string | `"OnFailure"` |  |
| hopsworks.dockerRegistry.preset.retry | int | `50` |  |
| hopsworks.dockerRegistry.preset.runIndex | int | `0` | Index to make job names unique if necessary |
| hopsworks.dockerRegistry.preset.secrets | list | `[]` |  |
| hopsworks.dockerRegistry.preset.serviceAccount.annotations | object | `{}` | service account annotations |
| hopsworks.dockerRegistry.preset.timeout | int | `3600` |  |
| hopsworks.dockerRegistry.preset.tolerations | list | `[]` |  |
| hopsworks.dockerRegistry.preset.ttlSecondsAfterFinished | string | `nil` | TTL in seconds for the preset-images Job. Overrides global default. |
| hopsworks.dockerRegistry.preset.usePullPush | bool | `true` |  |
| hopsworks.dockerRegistry.security.password | string | `nil` | user password |
| hopsworks.dockerRegistry.security.trust_registry | bool | `true` |  |
| hopsworks.dockerRegistry.security.user | string | `nil` | user name |
| hopsworks.dropDatabase | bool | `false` | Should not be changed here. Leave this as a conscious choice for the user when installing. If set to true will drop databases when helm uninstall. |
| hopsworks.envs.admin | object | `{}` | admin environment variables |
| hopsworks.envs.postInstall.ASADMIN_DEPLOY_TIMEOUT_SEC | int | `900` | Timeout (seconds) for the asadmin deploy command. Raise it if a legitimate EAR deploy exceeds 15 minutes, but keep query + deploy timeouts well under the sidecar's 30-minute heartbeat window. |
| hopsworks.envs.postInstall.ASADMIN_TIMEOUT_SEC | int | `120` | Timeout (seconds) for the admin sidecar's short asadmin calls (list-*, delete-instance), so one stuck call cannot hang its loop. The long-running deploy uses ASADMIN_DEPLOY_TIMEOUT_SEC instead. |
| hopsworks.envs.postInstall.CLEANUP_INTERVAL_SEC | int | `120` |  |
| hopsworks.envs.postInstall.DEBUG | string | `"true"` |  |
| hopsworks.envs.postInstall.DEPLOY_RETRIES | int | `3` | Deprecated. No longer consumed by the admin sidecar. Use DEPLOY_RETRY_INTERVAL_SEC to control the sleep between deploy attempts. Kept for backward compatibility; will be removed in a future major version. |
| hopsworks.envs.postInstall.DEPLOY_RETRY_INTERVAL_SEC | int | `30` | Sleep (seconds) between deploy attempts in the admin sidecar. Pacing only; the sidecar keeps retrying across cycles. |
| hopsworks.envs.postInstall.INITIAL_DELAY_SEC | int | `60` |  |
| hopsworks.envs.postInstall.REGISTER_WAIT_SEC | int | `240` |  |
| hopsworks.flyway.replaceDDL | string | `""` |  |
| hopsworks.flywayconfigmapName | string | `"flyway-config"` |  |
| hopsworks.fullnameOverride | string | `nil` | override app fully qualified name |
| hopsworks.hopsfsMount.enabled | bool | `true` |  |
| hopsworks.hopsfsMount.mountPath | string | `"/hopsfs"` |  |
| hopsworks.hopsworksAdmin | object | `{"hopsworks_ear_download_url":null,"hopsworks_front_download_url":null,"hopsworks_realm_download_url":null,"mysql_connector_download_url":null}` | override hopsworks admin artifacts |
| hopsworks.hopsworksAdmin.hopsworks_ear_download_url | string | `nil` | use custom hopsworks ear |
| hopsworks.hopsworksAdmin.hopsworks_front_download_url | string | `nil` | use custom hopsworks front end |
| hopsworks.hopsworksAdmin.hopsworks_realm_download_url | string | `nil` | use custom hopsworks realm jar file |
| hopsworks.hopsworksAdmin.mysql_connector_download_url | string | `nil` | use custom mysql connector |
| hopsworks.hopsworksCA.affinity | object | `{"podAntiAffinity":{"requiredDuringSchedulingIgnoredDuringExecution":[{"labelSelector":{"matchExpressions":[{"key":"app","operator":"In","values":["hopsworks-ca"]}]},"topologyKey":"kubernetes.io/hostname"}]}}` | Ensure we send them to different machines |
| hopsworks.hopsworksCA.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution | list | `[{"labelSelector":{"matchExpressions":[{"key":"app","operator":"In","values":["hopsworks-ca"]}]},"topologyKey":"kubernetes.io/hostname"}]` | podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution configuration |
| hopsworks.hopsworksCA.apiKey.secret_name | string | `"hopsworks-api-key-auth"` |  |
| hopsworks.hopsworksCA.auto_jvm | bool | `true` |  |
| hopsworks.hopsworksCA.ca_count | int | `1` | Number of hopsworks-ca replicas. Not rendered while hpa.ca.enabled is true; same rule as replicaCount.worker. |
| hopsworks.hopsworksCA.containerPort | int | `8182` |  |
| hopsworks.hopsworksCA.download_url | string | `nil` | use custom hopsworks ca war |
| hopsworks.hopsworksCA.extraJavaToolOptions | string | `""` |  |
| hopsworks.hopsworksCA.image.pullPolicy | string | `"IfNotPresent"` |  |
| hopsworks.hopsworksCA.image.tag | string | `nil` | image tag. If not defined, the .Chart.AppVersion will be used |
| hopsworks.hopsworksCA.internalCert.subject.locality | string | `"glassfishinternal"` |  |
| hopsworks.hopsworksCA.internalCert.subject.organization | int | `0` |  |
| hopsworks.hopsworksCA.jvm.garbageCollector | string | `""` |  |
| hopsworks.hopsworksCA.jvm.memory.buffer | int | `256` |  |
| hopsworks.hopsworksCA.jvm.memory.compressedClassSpaceSize | int | `256` |  |
| hopsworks.hopsworksCA.jvm.memory.heap | int | `1024` |  |
| hopsworks.hopsworksCA.jvm.memory.metaspace | int | `1024` |  |
| hopsworks.hopsworksCA.jvm.memory.nonMethodCodeHeapSize | int | `5` |  |
| hopsworks.hopsworksCA.jvm.memory.nonProfiledCodeHeapSize | int | `48` |  |
| hopsworks.hopsworksCA.jvm.memory.profiledCodeHeapSize | int | `48` |  |
| hopsworks.hopsworksCA.livenessProbe.failureThreshold | int | `3` |  |
| hopsworks.hopsworksCA.livenessProbe.httpGet.path | string | `"/hopsworks-ca/v2/certificate/crl/intermediate"` |  |
| hopsworks.hopsworksCA.livenessProbe.httpGet.port | int | `8182` |  |
| hopsworks.hopsworksCA.livenessProbe.httpGet.scheme | string | `"HTTPS"` |  |
| hopsworks.hopsworksCA.livenessProbe.initialDelaySeconds | int | `600` |  |
| hopsworks.hopsworksCA.livenessProbe.periodSeconds | int | `20` |  |
| hopsworks.hopsworksCA.livenessProbe.timeoutSeconds | int | `60` |  |
| hopsworks.hopsworksCA.name | string | `"hopsworks-ca"` |  |
| hopsworks.hopsworksCA.readinessProbe.httpGet.path | string | `"/hopsworks-ca/v2/certificate/ready"` |  |
| hopsworks.hopsworksCA.readinessProbe.httpGet.port | int | `8182` |  |
| hopsworks.hopsworksCA.readinessProbe.httpGet.scheme | string | `"HTTPS"` |  |
| hopsworks.hopsworksCA.readinessProbe.initialDelaySeconds | int | `60` |  |
| hopsworks.hopsworksCA.readinessProbe.periodSeconds | int | `10` |  |
| hopsworks.hopsworksCA.replaceEntryPoint | bool | `false` |  |
| hopsworks.hopsworksCA.resources.limits.cpu | string | `"2000m"` |  |
| hopsworks.hopsworksCA.resources.limits.memory | string | `"2048Mi"` |  |
| hopsworks.hopsworksCA.resources.requests.cpu | string | `"1000m"` |  |
| hopsworks.hopsworksCA.resources.requests.memory | string | `"2048Mi"` |  |
| hopsworks.hopsworksCA.securityContext | object | `{}` | security context |
| hopsworks.hopsworksCA.service.annotations."consul.hashicorp.com/service-name" | string | `"glassfish"` |  |
| hopsworks.hopsworksCA.service.annotations."consul.hashicorp.com/service-tags" | string | `"ca"` |  |
| hopsworks.hopsworksCA.service.name | string | `"hopsworks-ca"` |  |
| hopsworks.hopsworksCA.service.port | int | `8182` |  |
| hopsworks.hopsworksCA.setupJob.backoffLimit | int | `10` |  |
| hopsworks.hopsworksCA.shutdownWait | int | `30` |  |
| hopsworks.hopsworksCA.startWaitTimeout | int | `300` |  |
| hopsworks.hopsworkslib | object | `{}` | override hopsworkslib values |
| hopsworks.hpa.ca.enabled | bool | `false` | Autoscale hopsworks-ca. While enabled, hopsworksCA.ca_count is not rendered and the HPA owns spec.replicas. |
| hopsworks.hpa.ca.maxReplicas | int | `3` |  |
| hopsworks.hpa.ca.targetCPUUtilizationPercentage | int | `80` |  |
| hopsworks.hpa.ca.targetMemoryUtilizationPercentage | int | `95` |  |
| hopsworks.hpa.worker.enabled | bool | `false` | Autoscale the Payara workers. While enabled, replicaCount.worker is not rendered and the HPA owns spec.replicas. |
| hopsworks.hpa.worker.maxReplicas | int | `3` |  |
| hopsworks.hpa.worker.targetCPUUtilizationPercentage | int | `80` |  |
| hopsworks.hpa.worker.targetMemoryUtilizationPercentage | int | `95` |  |
| hopsworks.image.admin.imageName | string | `"hopsworks"` |  |
| hopsworks.image.admin.mysqlConnectorVersion | string | `"8.0.21.1"` |  |
| hopsworks.image.admin.mysqlStorageImageName | string | `"hopsworks-mysql-connector"` |  |
| hopsworks.image.admin.pullPolicy | string | `"IfNotPresent"` |  |
| hopsworks.image.admin.tag | string | `nil` | image tag. If not defined, the .Chart.AppVersion will be used |
| hopsworks.image.filebeat.imageName | string | `"filebeat"` |  |
| hopsworks.image.filebeat.tag | string | `"8.19.21"` |  |
| hopsworks.image.migration.pullPolicy | string | `"IfNotPresent"` |  |
| hopsworks.image.migration.tag | string | `nil` | image tag. If not defined, the .Chart.AppVersion will be used |
| hopsworks.image.postInstall.pullPolicy | string | `"IfNotPresent"` | pull policy for the admin sidecar's payara-node image. admindeployment.yaml already read this key before it was declared here, and its fallback cannot reach global._hopsworks.imagePullPolicy, so the sidecar was pinned to IfNotPresent with no way to override it. |
| hopsworks.image.postInstall.tag | string | `"6.2025.11-jdk21.0"` |  |
| hopsworks.image.registry | string | `nil` | image registry. If not defined, the global._hopsworks.imageRegistry will be used instead |
| hopsworks.image.worker.pullPolicy | string | `"IfNotPresent"` |  |
| hopsworks.image.worker.tag | string | `"6.2025.11-jdk21.0"` |  |
| hopsworks.imageBuilder.image | string | `"image-builder"` |  |
| hopsworks.imageBuilder.tag | string | `"0.2"` | 0.2 is a floor, not a preference. The OpenShift build path passes package-index credentials to buildah as -s id=NAME,src=PATH, and build-and-push.sh only learned that option in 0.2. Against 0.1 the script's getopts rejects it and every environment build on OpenShift fails, so this tag and the backend's docker_operations_image_builder_image move together. |
| hopsworks.imageBuilderServiceAccount | object | `{"annotations":{},"create":true,"name":"image-builder"}` | Configuration for the Service Account running all user environment Image Building Jobs |
| hopsworks.ingress.annotations | object | `{"nginx.ingress.kubernetes.io/affinity":"cookie","nginx.ingress.kubernetes.io/affinity-mode":"persistent","nginx.ingress.kubernetes.io/proxy-body-size":"0","nginx.ingress.kubernetes.io/proxy-redirect-from":"http:","nginx.ingress.kubernetes.io/proxy-redirect-to":"https:","nginx.ingress.kubernetes.io/session-cookie-expires":"5259600","nginx.ingress.kubernetes.io/session-cookie-max-age":"5259600","nginx.ingress.kubernetes.io/ssl-redirect":"true"}` | ingress annotations |
| hopsworks.ingress.enabled | bool | `true` |  |
| hopsworks.ingress.extraLabels | object | `{}` | ingress extra labels |
| hopsworks.ingress.extraPaths | list | `[]` |  |
| hopsworks.ingress.host | string | `"hopsworks.ai.local"` |  |
| hopsworks.ingress.hosts | list | `["hopsworks.ai.local"]` | ingress hosts configuration |
| hopsworks.ingress.ingressClassName | string | `"nginx"` |  |
| hopsworks.ingress.path | string | `"/"` |  |
| hopsworks.ingress.pathType | string | `"Prefix"` |  |
| hopsworks.ingress.secretName | string | `"hopsworks-ingress-crypto-material"` |  |
| hopsworks.ingress.servicePort | int | `28080` |  |
| hopsworks.ingress.sslPassthrough | bool | `false` |  |
| hopsworks.ingress.tls | list | `[{"hosts":["hopsworks.ai.local"],"secretName":"hopsworks-ingress-crypto-material"}]` | ingress tls configuration per host |
| hopsworks.instanceconfigmapName | string | `"instance-config"` |  |
| hopsworks.jupyter.notebookConfig.allowOrigin | string | `"${conf.allowOrigin}"` |  |
| hopsworks.jupyter.notebookConfig.enableDownloads | bool | `true` | Set to false to disable file downloads from the Jupyter UI. |
| hopsworks.jupyter.notebookConfig.enableUploads | bool | `true` | Set to false to disable file uploads from the Jupyter UI and reject base64 file uploads via the Contents API. Kernel/terminal file writes are unaffected. Requires JupyterLab >= 4.5. |
| hopsworks.lb.names.mysqld | string | `"mysqld-external"` |  |
| hopsworks.lb.names.rdrs | string | `"rdrs-external"` |  |
| hopsworks.lb.serviceAccount.annotations | object | `{}` | annotations |
| hopsworks.nameOverride | string | `nil` | override app chart name |
| hopsworks.nodeSelector | object | `{}` | node selector configuration |
| hopsworks.objectStorageEnvInformation | string | `nil` | override object storage list of of environment variables |
| hopsworks.opensearchReindex.enabled | bool | `true` | Rebuild the featurestore search index after an upgrade, when what the index holds has changed since its last rebuild. The hook keys its request with the index generation, featurestore-index-5.1, which the chart bumps only with a change to what the backend indexes: a generation already rebuilt is answered with that run, so patch upgrades and ArgoCD syncs do not rebuild again, and a cluster that missed the rebuild gets it on its next upgrade. Runs requested by earlier charts carry no key, so the first upgrade with this chart rebuilds once. The rebuild runs in the backend after the upgrade and takes hours on a large cluster, with search incomplete until it finishes; its progress shows under Cluster Settings > Service Operations > OpenSearch Index Commands. A failed hook Job is removed after global._hopsworks.jobs.ttlSecondsAfterFinished in the default mode, or when the hook next renders; with global._hopsworks.mode set, as under ArgoCD, delete post-upgrade-opensearch-reindex-job by hand if you turn this off after a failed attempt. |
| hopsworks.payara.adminpwKeyName | string | `"admin_password"` |  |
| hopsworks.payara.adminuser | string | `"admin"` |  |
| hopsworks.payara.config | string | `"hopsworks-config"` |  |
| hopsworks.payara.debug | bool | `false` |  |
| hopsworks.payara.deploymentGroup | string | `"hopsworks-dg"` |  |
| hopsworks.payara.disableMetricsServiceLogs | bool | `false` |  |
| hopsworks.payara.disableXmlValidation | bool | `true` |  |
| hopsworks.payara.encryptionpwKeyName | string | `"encryption_master_password"` |  |
| hopsworks.payara.http.keep_alive_timeout | int | `30` |  |
| hopsworks.payara.httpListener1Enabled | bool | `true` |  |
| hopsworks.payara.httpthreadpool.idletimeout | int | `900` | The maximum amount of time that a thread can remain idle in the pool. After this time expires, the thread is removed from the pool. |
| hopsworks.payara.httpthreadpool.maxqueuesize | int | `4096` | The maximum number of threads in the queue. A value of -1 indicates that there is no limit to the queue size. |
| hopsworks.payara.httpthreadpool.maxthreadpoolsize | int | `200` |  |
| hopsworks.payara.httpthreadpool.minthreadpoolsize | int | `5` |  |
| hopsworks.payara.kerberos.enabled | bool | `false` |  |
| hopsworks.payara.kerberos.keyTabName | string | `"service.keytab"` | kerberos service principal keytab name. |
| hopsworks.payara.kerberos.keyTabPath | string | `"/etc/security/keytabs"` | kerberos service principal keytab file path. |
| hopsworks.payara.kerberos.keyTabPrincipal | string | `"HTTP/hopsworks.cluster.local@EXAMPLE.COM"` | kerberos service principal name. This name is created by combining the string HTTP with the hostname 'HTTP@host_name'. The host name is the DNS name by which browsers contact the Web server. Use the fully qualified host name. |
| hopsworks.payara.kerberos.keyTabSecretName | string | `"keytab-secret"` | keytab secret name. |
| hopsworks.payara.kerberos.krb5ConfigName | string | `"server-krb5-config"` | krb5.conf config map name. |
| hopsworks.payara.ldap.enabled | bool | `false` |  |
| hopsworks.payara.ldap.factory_class | string | `"com.sun.jndi.ldap.LdapCtxFactory"` | Factory class for resource; implements javax.naming.spi.ObjectFactory. |
| hopsworks.payara.ldap.jndilookupname | string | `"dc=example,dc=com"` | Name used by the application to find the resource. |
| hopsworks.payara.ldap.property.additional_props\[0\].key | string | `"hopsworks\\.ldap\\.basedn"` |  |
| hopsworks.payara.ldap.property.additional_props\[0\].value | string | `"dc=example,dc=com"` |  |
| hopsworks.payara.ldap.property.attributes_binary | string | `"entryUUID"` | The binary unique identifier that will be used in subsequent logins to identify the user. |
| hopsworks.payara.ldap.property.provider_url | string | `"ldap://192.168.200.104:389"` |  |
| hopsworks.payara.ldap.property.referral | string | `"ignore"` | Whether to follow or ignore an alternate location in which an LDAP request may be processed. |
| hopsworks.payara.ldap.property.security.authentication | string | `"simple"` |  |
| hopsworks.payara.ldap.property.security.credentials.secret_key | string | `"credentials"` |  |
| hopsworks.payara.ldap.property.security.credentials.secret_name | string | `"ldap-credentials-secret"` |  |
| hopsworks.payara.ldap.property.security.principal | string | `"cn=admin,dc=example,dc=com"` |  |
| hopsworks.payara.ldap.res_type | string | `"javax.naming.ldap.LdapContext"` | Resource Type. Enter a fully qualified type following the format xxx.xxx (for example, javax.jms.Topic) |
| hopsworks.payara.mail.email | string | `"smtp@gmail.com"` |  |
| hopsworks.payara.mail.from | string | `"admin@hopsworks.ai"` |  |
| hopsworks.payara.mail.password.secret_key | string | `"payara-mail-password"` |  |
| hopsworks.payara.mail.smtp | string | `"smtp.gmail.com"` |  |
| hopsworks.payara.mail.smtp_port | string | `"587"` |  |
| hopsworks.payara.mail.smtp_ssl_port | string | `"465"` |  |
| hopsworks.payara.oauth.clients | list | `[]` | oauth clients |
| hopsworks.payara.oauth.enabled | bool | `false` |  |
| hopsworks.payara.postbootCommands | string | `"/opt/payara/k8s/commands/post-boot-commands.asadmin"` |  |
| hopsworks.payara.prebootCommands | string | `"/opt/payara/k8s/commands/pre-boot-commands.asadmin"` |  |
| hopsworks.payara.uniformLogFormatter | bool | `false` |  |
| hopsworks.payara.versionUpgrade | string | `nil` | is Payara version upgrade. If null, auto detect based on current and target version |
| hopsworks.payara.websocketProxy | object | `{"grizzlyWorkerPoolMaxSize":200,"heartbeatIntervalMs":20000,"incomingBufferBytes":33554432,"maxSessionsPerApp":500,"sessionIdleTimeoutMs":0}` | Tyrus WebSocket-proxy tuning (jupyter / terminal / python-app). These five values are the single source of truth: post-boot-commands.txt passes each as a JVM system property (-D) which hopsworks-ee reads (WebSocketProxyConfig). |
| hopsworks.payara.websocketProxy.grizzlyWorkerPoolMaxSize | int | `200` | Upper bound on the shared Tyrus/Grizzly client transport worker pool. Bounded to 1..Integer.MAX_VALUE (read via Integer.getInteger). |
| hopsworks.payara.websocketProxy.heartbeatIntervalMs | int | `20000` | Interval, in milliseconds, of the Tyrus per-session heartbeat on the inbound (browser) WebSocket leg. The browser hop traverses ingress-nginx, whose proxy_read_timeout (default 60s) reaps a WebSocket idle for that long; Tyrus emits an unsolicited pong every interval to keep it warm. Keep below the ingress timeout. 0 disables. Read via Long.getLong, so only a non-negative lower bound is enforced. |
| hopsworks.payara.websocketProxy.incomingBufferBytes | int | `33554432` | Max size, in bytes, of a single received WebSocket frame on the upstream leg — the ceiling a large Jupyter cell output must fit under. Grown on demand, not pre-allocated. Keep at or above jupyter's iopub rate-limit budget. Bounded to 1..Integer.MAX_VALUE (read via Integer.getInteger). |
| hopsworks.payara.websocketProxy.maxSessionsPerApp | int | `500` | Max concurrent inbound WebSocket proxy sessions per pod (jupyter, terminal and python-app share this budget). The next upgrade past the cap is closed with 1013 TRY_AGAIN_LATER, protecting the pod from connection-driven OOM. Read via Integer.getInteger in hopsworks-ee, so values outside the int range would be silently ignored — bounded to 1..Integer.MAX_VALUE here. |
| hopsworks.payara.websocketProxy.sessionIdleTimeoutMs | int | `0` | Per-session idle timeout in milliseconds. 0 disables the idle reaper (proxy sessions are legitimately long-lived). Read via Long.getLong, so only a non-negative lower bound is enforced. |
| hopsworks.payaraVersion | string | `"6.2025.11-jdk21.0"` |  |
| hopsworks.payaraconfigmapName | string | `"post-boot-commands"` |  |
| hopsworks.podAnnotations | object | `{}` | pod annotations |
| hopsworks.podDisruptionBudget.hopsworksCA.enabled | bool | `true` |  |
| hopsworks.podDisruptionBudget.hopsworksCA.minAvailable | int | `1` |  |
| hopsworks.podDisruptionBudget.worker.enabled | bool | `true` |  |
| hopsworks.podDisruptionBudget.worker.minAvailable | int | `1` |  |
| hopsworks.podLabels | object | `{}` | pod labels |
| hopsworks.probs.admin.livenessProbe | object | `{"exec":{"command":["/bin/sh","/opt/payara/k8s/ready.sh"]},"failureThreshold":10,"periodSeconds":60,"timeoutSeconds":30}` | liveness probe. Restarts the DAS if it stays unresponsive for ~10 minutes (10 x 60s); without it a hung DAS is never restarted. The long window is deliberate: it must not fire on slowness, and each run costs an asadmin JVM inside the DAS container. Set to null to disable. If you override with httpGet/tcpSocket, also set `exec: null` (Helm merges maps; a probe allows only one handler). |
| hopsworks.probs.admin.livenessProbe.exec | object | `{"command":["/bin/sh","/opt/payara/k8s/ready.sh"]}` | exec probe handler. Set to null when overriding the probe with httpGet/tcpSocket (Helm merges maps; a probe allows only one handler). |
| hopsworks.probs.admin.readinessProbe | object | `{"exec":{"command":["/bin/sh","/opt/payara/k8s/ready.sh"]},"initialDelaySeconds":90,"periodSeconds":10,"timeoutSeconds":30}` | readiness probe. Controls the admin pod's Ready state and so the hopsworks-admin Service endpoint that workers use to reach the DAS. ready.sh only checks that the DAS admin interface responds. Short 10s period on purpose — this is the probe that must react fast; liveness samples slower. If you override with httpGet/tcpSocket, also set `exec: null`. |
| hopsworks.probs.admin.readinessProbe.exec | object | `{"command":["/bin/sh","/opt/payara/k8s/ready.sh"]}` | exec probe handler. Set to null when overriding the probe with httpGet/tcpSocket (Helm merges maps; a probe allows only one handler). |
| hopsworks.probs.admin.startupProbe | object | `{"exec":{"command":["/bin/sh","/opt/payara/k8s/ready.sh"]},"failureThreshold":180,"periodSeconds":10,"timeoutSeconds":30}` | startup probe. Gives the DAS up to 30 minutes (180 x 10s) to boot before liveness starts counting. Generous on purpose: container start includes artifact downloads, and a kill mid-download starts them over. Set to null to disable. If you override with httpGet/tcpSocket, also set `exec: null`. |
| hopsworks.probs.admin.startupProbe.exec | object | `{"command":["/bin/sh","/opt/payara/k8s/ready.sh"]}` | exec probe handler. Set to null when overriding the probe with httpGet/tcpSocket (Helm merges maps; a probe allows only one handler). |
| hopsworks.probs.worker.livenessProbe.failureThreshold | int | `3` |  |
| hopsworks.probs.worker.livenessProbe.httpGet.path | string | `"/hopsworks-api/api/variables/versions"` |  |
| hopsworks.probs.worker.livenessProbe.httpGet.port | int | `8182` |  |
| hopsworks.probs.worker.livenessProbe.httpGet.scheme | string | `"HTTPS"` |  |
| hopsworks.probs.worker.livenessProbe.initialDelaySeconds | int | `150` |  |
| hopsworks.probs.worker.livenessProbe.periodSeconds | int | `20` |  |
| hopsworks.probs.worker.livenessProbe.timeoutSeconds | int | `20` |  |
| hopsworks.probs.worker.readinessProbe.httpGet.path | string | `"/hopsworks-api/api/variables/versions"` |  |
| hopsworks.probs.worker.readinessProbe.httpGet.port | int | `8182` |  |
| hopsworks.probs.worker.readinessProbe.httpGet.scheme | string | `"HTTPS"` |  |
| hopsworks.probs.worker.readinessProbe.initialDelaySeconds | int | `150` |  |
| hopsworks.probs.worker.readinessProbe.periodSeconds | int | `10` |  |
| hopsworks.probs.worker.startupProbe.failureThreshold | int | `10` |  |
| hopsworks.probs.worker.startupProbe.httpGet.path | string | `"/health"` |  |
| hopsworks.probs.worker.startupProbe.httpGet.port | int | `8182` |  |
| hopsworks.probs.worker.startupProbe.httpGet.scheme | string | `"HTTPS"` |  |
| hopsworks.probs.worker.startupProbe.initialDelaySeconds | int | `150` |  |
| hopsworks.probs.worker.startupProbe.periodSeconds | int | `10` |  |
| hopsworks.rbac.annotations | object | `{}` | annotations |
| hopsworks.rbac.create | bool | `true` |  |
| hopsworks.rbac.extraRoleRules\[0\].apiGroups\[0\] | string | `"discovery.k8s.io"` |  |
| hopsworks.rbac.extraRoleRules\[0\].resources\[0\] | string | `"endpointslices"` |  |
| hopsworks.rbac.extraRoleRules\[0\].verbs\[0\] | string | `"get"` |  |
| hopsworks.rbac.extraRoleRules\[0\].verbs\[1\] | string | `"list"` |  |
| hopsworks.rbac.extraRoleRules\[1\].apiGroups\[0\] | string | `"sparkoperator.k8s.io"` |  |
| hopsworks.rbac.extraRoleRules\[1\].resources\[0\] | string | `"sparkapplications"` |  |
| hopsworks.rbac.extraRoleRules\[1\].verbs\[0\] | string | `"*"` |  |
| hopsworks.rbac.extraRoleRules\[2\].apiGroups\[0\] | string | `"ray.io"` |  |
| hopsworks.rbac.extraRoleRules\[2\].resources\[0\] | string | `"rayjobs"` |  |
| hopsworks.rbac.extraRoleRules\[2\].resources\[1\] | string | `"rayclusters"` |  |
| hopsworks.rbac.extraRoleRules\[2\].verbs\[0\] | string | `"*"` |  |
| hopsworks.rbac.extraRoleRules\[3\].apiGroups\[0\] | string | `"serving.knative.dev"` |  |
| hopsworks.rbac.extraRoleRules\[3\].resources\[0\] | string | `"services"` |  |
| hopsworks.rbac.extraRoleRules\[3\].verbs\[0\] | string | `"*"` |  |
| hopsworks.rbac.extraRoleRules\[4\].apiGroups\[0\] | string | `"serving.kserve.io"` |  |
| hopsworks.rbac.extraRoleRules\[4\].resources\[0\] | string | `"inferenceservices"` |  |
| hopsworks.rbac.extraRoleRules\[4\].resources\[1\] | string | `"clusterservingruntimes"` |  |
| hopsworks.rbac.extraRoleRules\[4\].verbs\[0\] | string | `"*"` |  |
| hopsworks.rbac.extraRoleRules\[5\].apiGroups\[0\] | string | `"scheduling.k8s.io"` |  |
| hopsworks.rbac.extraRoleRules\[5\].resources\[0\] | string | `"priorityclasses"` |  |
| hopsworks.rbac.extraRoleRules\[5\].verbs\[0\] | string | `"get"` |  |
| hopsworks.rbac.extraRoleRules\[5\].verbs\[1\] | string | `"list"` |  |
| hopsworks.rbac.extraRoleRules\[6\].apiGroups\[0\] | string | `"metrics.k8s.io"` |  |
| hopsworks.rbac.extraRoleRules\[6\].resources\[0\] | string | `"nodes"` |  |
| hopsworks.rbac.extraRoleRules\[6\].resources\[1\] | string | `"pods"` |  |
| hopsworks.rbac.extraRoleRules\[6\].verbs\[0\] | string | `"get"` |  |
| hopsworks.rbac.extraRoleRules\[6\].verbs\[1\] | string | `"list"` |  |
| hopsworks.rbac.extraRoleRules\[7\].apiGroups\[0\] | string | `""` |  |
| hopsworks.rbac.extraRoleRules\[7\].resources\[0\] | string | `"resourcequotas"` |  |
| hopsworks.rbac.extraRoleRules\[7\].verbs\[0\] | string | `"get"` |  |
| hopsworks.rbac.extraRoleRules\[7\].verbs\[1\] | string | `"list"` |  |
| hopsworks.rbac.useExistingRole | bool | `false` |  |
| hopsworks.replicaCount.worker | int | `2` | Number of Payara worker replicas. Not rendered while hpa.worker.enabled is true: the HPA then owns spec.replicas and this value is its minReplicas. Turning the HPA on for a running release drops the workers to 1 once, until the HPA scales them back up. |
| hopsworks.resources.admin.auto_jvm | bool | `true` |  |
| hopsworks.resources.admin.container.limits.cpu | string | `"2000m"` |  |
| hopsworks.resources.admin.container.limits.memory | string | `"2048Mi"` |  |
| hopsworks.resources.admin.container.requests.cpu | string | `"1000m"` |  |
| hopsworks.resources.admin.container.requests.memory | string | `"2048Mi"` |  |
| hopsworks.resources.admin.extraJavaToolOptions | string | `""` |  |
| hopsworks.resources.admin.jvm.garbageCollector | string | `""` |  |
| hopsworks.resources.admin.jvm.memory.buffer | int | `256` |  |
| hopsworks.resources.admin.jvm.memory.compressedClassSpaceSize | int | `512` |  |
| hopsworks.resources.admin.jvm.memory.heap | int | `2048` |  |
| hopsworks.resources.admin.jvm.memory.metaspace | int | `1024` |  |
| hopsworks.resources.admin.jvm.memory.nonMethodCodeHeapSize | int | `5` |  |
| hopsworks.resources.admin.jvm.memory.nonProfiledCodeHeapSize | int | `48` |  |
| hopsworks.resources.admin.jvm.memory.profiledCodeHeapSize | int | `48` |  |
| hopsworks.resources.adminSidecar | object | `{"requests":{"cpu":"200m","memory":"256Mi"}}` | Admin side car resources |
| hopsworks.resources.worker.auto_jvm | bool | `true` |  |
| hopsworks.resources.worker.container.limits.cpu | string | `"4000m"` |  |
| hopsworks.resources.worker.container.limits.memory | string | `"8Gi"` |  |
| hopsworks.resources.worker.container.requests.cpu | string | `"2000m"` |  |
| hopsworks.resources.worker.container.requests.memory | string | `"2048Mi"` |  |
| hopsworks.resources.worker.extraJavaToolOptions | string | `""` |  |
| hopsworks.resources.worker.jvm.garbageCollector | string | `""` |  |
| hopsworks.resources.worker.jvm.memory.buffer | int | `2048` |  |
| hopsworks.resources.worker.jvm.memory.compressedClassSpaceSize | int | `512` |  |
| hopsworks.resources.worker.jvm.memory.heap | int | `4096` |  |
| hopsworks.resources.worker.jvm.memory.metaspace | int | `1024` |  |
| hopsworks.resources.worker.jvm.memory.nonMethodCodeHeapSize | int | `5` |  |
| hopsworks.resources.worker.jvm.memory.nonProfiledCodeHeapSize | int | `48` |  |
| hopsworks.resources.worker.jvm.memory.profiledCodeHeapSize | int | `48` |  |
| hopsworks.securityContext | object | `{}` | custom security context for hopsworks admin and workers |
| hopsworks.service.admin.annotations."consul.hashicorp.com/service-name" | string | `"glassfish"` |  |
| hopsworks.service.admin.annotations."consul.hashicorp.com/service-tags" | string | `"admin"` |  |
| hopsworks.service.admin.name | string | `"admin"` |  |
| hopsworks.service.admin.port | int | `4848` |  |
| hopsworks.service.admin.type | string | `"ClusterIP"` |  |
| hopsworks.service.worker.external.http.port | int | `28080` |  |
| hopsworks.service.worker.external.http.type | string | `"ClusterIP"` |  |
| hopsworks.service.worker.external.https.nodePort | string | `nil` | Explicit nodePort for the https service when type is NodePort. Null lets Kubernetes allocate one from the cluster's node-port range. |
| hopsworks.service.worker.external.https.port | int | `28181` |  |
| hopsworks.service.worker.external.https.type | string | `"ClusterIP"` |  |
| hopsworks.service.worker.internal.annotations."consul.hashicorp.com/service-name" | string | `"glassfish"` |  |
| hopsworks.service.worker.internal.annotations."consul.hashicorp.com/service-tags" | string | `"hopsworks"` |  |
| hopsworks.service.worker.internal.annotations."prometheus.io/path" | string | `"/metrics"` |  |
| hopsworks.service.worker.internal.annotations."prometheus.io/port" | int | `8182` |  |
| hopsworks.service.worker.internal.annotations."prometheus.io/scheme" | string | `"https"` |  |
| hopsworks.service.worker.internal.annotations."prometheus.io/scrape" | string | `"true"` |  |
| hopsworks.service.worker.internal.port | int | `8182` |  |
| hopsworks.service.worker.internal.type | string | `"ClusterIP"` |  |
| hopsworks.setAdminHighPriority | bool | `true` |  |
| hopsworks.sparkConfigmapName | string | `"spark"` |  |
| hopsworks.sqldmlconfigmapName | string | `"sql-dml"` |  |
| hopsworks.sqlgrantsconfigmapName | string | `"sql-grants"` |  |
| hopsworks.templatesconfigmapName | string | `"hopsworks-templates"` |  |
| hopsworks.terminal.enabled | bool | `false` |  |
| hopsworks.terminal.oomGuard | bool | `true` | In-image memory guard: kills the hungriest process in a terminal pod before the kernel group-OOM-kills the whole session (cgroup v2 only). False sets HOPS_OOM_GUARD_DISABLE=1 on new terminal pods. |
| hopsworks.terminal.proxyPodAppLabels | string | `"hopsworks-instance,hopsworks-admin"` | Comma-separated `app` label values of the Payara pods allowed to reach a terminal pod's WebSocket port (the per-namespace terminal-isolation NetworkPolicy). Must match the chart's pod labels or every terminal is unreachable. |
| hopsworks.terminal.proxyTokenTtlMs | string | `"60000"` | Milliseconds a CLI terminal-attach proxy token stays valid before its single WebSocket handshake. |
| hopsworks.terminal.teleportCleanerIntervalMs | string | `"86400000"` | Milliseconds between teleport reaper sweeps (applied at Payara start). Quoted like the other *_ms settings: a bare integer this large renders as 8.64e+07 in the DML. |
| hopsworks.terminal.teleportTtlDays | int | `7` | Days a staged hops-session teleport file (transcript, manifest, baton) survives in a user's HopsFS home before the reaper deletes it; 0 or less disables the reaper. |
| hopsworks.tests.backupRestore.enabled | bool | `false` |  |
| hopsworks.tests.backupRestore.mode | string | `"seed"` |  |
| hopsworks.tests.end2end.e2eProjectNamespace | string | `""` | Pre-created namespace for the end2end test project on clusters that use pre-created namespaces (OpenShift/OKD). Empty on kubeadm (namespace is derived from the project name). |
| hopsworks.tests.end2end.enabled | bool | `false` |  |
| hopsworks.tests.end2end.itProjectNamespace | string | `""` | Pre-created namespace for the canonical IT test project on clusters that use pre-created namespaces (OpenShift/OKD). Empty on kubeadm. |
| hopsworks.tests.integration.isolatedTests | list | `[]` |  |
| hopsworks.tests.integration.parallelism | int | `8` |  |
| hopsworks.tests.integration.tests | list | `[]` |  |
| hopsworks.tests.loadtests.bigquery_client_id | string | `""` |  |
| hopsworks.tests.loadtests.bigquery_private_key | string | `""` |  |
| hopsworks.tests.loadtests.bigquery_private_key_id | string | `""` |  |
| hopsworks.tests.loadtests.client_version | string | `"master"` |  |
| hopsworks.tests.loadtests.connectors | string | `""` |  |
| hopsworks.tests.loadtests.enabled | bool | `false` |  |
| hopsworks.tests.loadtests.exclude | list | `[]` |  |
| hopsworks.tests.loadtests.gpu_available | bool | `false` |  |
| hopsworks.tests.loadtests.job_name | string | `""` |  |
| hopsworks.tests.loadtests.load_tests_image | string | `""` |  |
| hopsworks.tests.loadtests.mongodb_pass | string | `""` |  |
| hopsworks.tests.loadtests.mongodb_user | string | `""` |  |
| hopsworks.tests.loadtests.namespaceProvisionerConfigMap | string | `""` | ConfigMap providing a `provision.sh` that creates the namespace backing a project, mounted at /opt/namespace-provisioner and run once per project. Needed where namespaces must exist before the project (`variables.kube_skip_namespace_creation`). |
| hopsworks.tests.loadtests.oracle_pass | string | `""` |  |
| hopsworks.tests.loadtests.oracle_user | string | `""` |  |
| hopsworks.tests.loadtests.parallelism | int | `1` |  |
| hopsworks.tests.loadtests.project_cleanup | bool | `true` |  |
| hopsworks.tests.loadtests.rds_pass | string | `""` |  |
| hopsworks.tests.loadtests.rds_user | string | `""` |  |
| hopsworks.tests.loadtests.redshift_pass | string | `""` |  |
| hopsworks.tests.loadtests.redshift_user | string | `""` |  |
| hopsworks.tests.loadtests.resources | object | `{}` | load tests job resources |
| hopsworks.tests.loadtests.retries | int | `1` |  |
| hopsworks.tests.loadtests.s3_access_key | string | `""` |  |
| hopsworks.tests.loadtests.s3_secret_key | string | `""` |  |
| hopsworks.tests.loadtests.serviceAccountName | string | `""` | Service account for the test pods. Empty uses the namespace default. |
| hopsworks.tests.loadtests.snowflake_pass | string | `""` |  |
| hopsworks.tests.loadtests.snowflake_url | string | `""` |  |
| hopsworks.tests.loadtests.snowflake_user | string | `""` |  |
| hopsworks.tests.loadtests.test_prefix | string | `""` |  |
| hopsworks.tests.loadtests.tests | list | `[]` |  |
| hopsworks.tests.loadtests.timeout_per_test | string | `"100"` |  |
| hopsworks.tests.loadtests.unity_catalog_access_token | string | `""` |  |
| hopsworks.tests.loadtests.unity_catalog_account_host | string | `""` |  |
| hopsworks.tests.loadtests.unity_catalog_account_id | string | `""` |  |
| hopsworks.tests.loadtests.unity_catalog_aws_region | string | `""` |  |
| hopsworks.tests.loadtests.unity_catalog_client_id | string | `""` |  |
| hopsworks.tests.loadtests.unity_catalog_client_secret | string | `""` |  |
| hopsworks.tests.loadtests.unity_catalog_default_catalog | string | `""` |  |
| hopsworks.tests.loadtests.unity_catalog_workspace_url | string | `""` |  |
| hopsworks.tolerations | list | `[]` |  |
| hopsworks.topologySpreadConstraint | object | `{}` | The default topology spread constraint. If not defined the global topology spread constraint would be used instead. |
| hopsworks.updateLoadBalancerDomains | object | `{"resources":{"limits":{"cpu":"50m","memory":"50M"},"requests":{"cpu":"20m","memory":"20M"}}}` | update_load_balancer_domains Job configuration |
| hopsworks.updateLoadBalancerDomains.resources | object | `{"limits":{"cpu":"50m","memory":"50M"},"requests":{"cpu":"20m","memory":"20M"}}` | resource limits configuration |
| hopsworks.variables.admin_email | string | `"admin@hopsworks.ai"` |  |
| hopsworks.variables.admin_password | string | `"admin"` |  |
| hopsworks.variables.agent_deployment_otel_cpu | string | `"0.5"` |  |
| hopsworks.variables.agent_deployment_otel_enabled | string | `"true"` |  |
| hopsworks.variables.agent_deployment_otel_image | string | `"otlp-sidecar"` |  |
| hopsworks.variables.agent_deployment_otel_memory_mb | string | `"1024"` |  |
| hopsworks.variables.agent_jobs_enabled | string | `"true"` |  |
| hopsworks.variables.airflow_dir | string | `"/srv/hops/airflow"` |  |
| hopsworks.variables.airflow_enabled | bool | `true` |  |
| hopsworks.variables.airflow_user | string | `"airflow"` |  |
| hopsworks.variables.airflow_user_email | string | `"airflow@hopsworks.ai"` |  |
| hopsworks.variables.alert_email_addrs | string | `""` |  |
| hopsworks.variables.anaconda_dir | string | `"/"` |  |
| hopsworks.variables.anaconda_enabled | string | `"true"` |  |
| hopsworks.variables.anaconda_env | string | `""` |  |
| hopsworks.variables.anaconda_user | string | `"anaconda"` |  |
| hopsworks.variables.application_certificate_validity_period | string | `"3650d"` |  |
| hopsworks.variables.apply_hopsfsmount_apparmor_profile_kube | string | `"false"` |  |
| hopsworks.variables.async_services_timer_batch_size | string | `"1000"` |  |
| hopsworks.variables.async_services_timer_delete_history_after_days | string | `"7"` |  |
| hopsworks.variables.async_services_timer_enabled | string | `"true"` |  |
| hopsworks.variables.async_services_timer_interval_ms | string | `"15000"` |  |
| hopsworks.variables.audit_log_count | string | `"10"` |  |
| hopsworks.variables.audit_log_file_format | string | `"server_audit_log%g.log"` |  |
| hopsworks.variables.audit_log_file_path | string | `"/audit-logs"` |  |
| hopsworks.variables.audit_log_file_type | string | `"io.hops.hopsworks.audit.helper.JSONLogFormatter"` |  |
| hopsworks.variables.audit_log_size_limit | string | `"256000000"` |  |
| hopsworks.variables.base_buildkit_image | string | `"docker.hops.works/hopsworks/moby/buildkit:v0.32.2-rootless"` |  |
| hopsworks.variables.base_image_name | string | `"hopsworks-base"` |  |
| hopsworks.variables.base_image_version | string | `"5.2.0-SNAPSHOT"` |  |
| hopsworks.variables.cert_mater_delay | string | `"3m"` |  |
| hopsworks.variables.certs_dir | string | `"/srv/hops/certs-dir"` |  |
| hopsworks.variables.check_nodemanagers_status | string | `""` |  |
| hopsworks.variables.client_path | string | `"/srv/hops/clients-3.4.3"` |  |
| hopsworks.variables.cloud | string | `""` |  |
| hopsworks.variables.command_agent_home_batch | string | `"20"` |  |
| hopsworks.variables.command_agent_home_claim_lease_as_ms | string | `"600000"` |  |
| hopsworks.variables.command_agent_home_migration_period_as_ms | string | `"3600000"` |  |
| hopsworks.variables.command_agent_home_process_timer_period_as_ms | string | `"5000"` |  |
| hopsworks.variables.command_agent_home_retry_backoff_base_as_ms | string | `"10000"` |  |
| hopsworks.variables.command_agent_home_retry_backoff_max_as_ms | string | `"600000"` |  |
| hopsworks.variables.command_search_fs_history_clean_period_as_ms | string | `"3600000"` |  |
| hopsworks.variables.command_search_fs_history_enable | string | `"false"` |  |
| hopsworks.variables.command_search_fs_history_window_as_s | string | `"3600"` |  |
| hopsworks.variables.command_search_fs_process_timer_period_as_ms | string | `"1000"` |  |
| hopsworks.variables.command_search_fs_reindex_queue_wait_as_ms | string | `"1800000"` | How long a featurestore search reindex run waits for the search command queue to empty and for the featurestore index template to be installed before it is aborted, in milliseconds. The reindex empties the index first, so it only starts on an empty queue, and the template gives the new index its mappings. A run aborted this way is reported under Cluster Settings > Service Operations > OpenSearch Index Commands, where it can be requested again. |
| hopsworks.variables.command_search_fs_retry_per_clean_interval | string | `"5"` |  |
| hopsworks.variables.conda_default_repo | string | `"defaults"` |  |
| hopsworks.variables.default_jupyter_environment | string | `"pandas-training-pipeline"` |  |
| hopsworks.variables.default_python_job_environment | string | `"pandas-training-pipeline"` |  |
| hopsworks.variables.disable_password_login | string | `"false"` |  |
| hopsworks.variables.disable_registration | string | `"false"` |  |
| hopsworks.variables.dlt_schema_fetch_job_deadline_seconds | string | `"1800"` | activeDeadlineSeconds for dlthub schema-fetch Kubernetes Jobs. Kills schema-fetch pods that never get to run (unschedulable, volume mount failures), which would otherwise be reported as in-progress forever. |
| hopsworks.variables.docker_base_image_python_version | string | `"3.13"` |  |
| hopsworks.variables.docker_cgroup_cpu_period | string | `"100000"` |  |
| hopsworks.variables.docker_cgroup_enabled | string | `"false"` |  |
| hopsworks.variables.docker_cgroup_parent | string | `"docker.slice"` |  |
| hopsworks.variables.docker_job_mounts_allowed | string | `"false"` |  |
| hopsworks.variables.docker_job_mounts_list | string | `""` |  |
| hopsworks.variables.docker_job_uid_strict | string | `"true"` |  |
| hopsworks.variables.docker_mounts | string | `"/srv/hops/hadoop/etc/hadoop,/srv/hops/spark,/srv/hops/flink,/srv/hops/apache-livy"` |  |
| hopsworks.variables.docker_operations_allow_hermetic_custom_commands | string | `"false"` | Whether a custom-commands build may declare itself hermetic, with HOPSWORKS_BUILD_HERMETIC=true in its environment file, and so keep its layer cache. Custom command layers are never reused otherwise, because the script can fetch anything and nothing declares what. Only the script's author knows whether that is true of their script, and only the operator decides whether that claim is allowed to control cache reuse. |
| hopsworks.variables.docker_operations_backoff_limit | string | `"0"` |  |
| hopsworks.variables.docker_operations_build_metadata | string | `"true"` | Capture the package list, environment export and pip check inside the image build so one post-build job reads them instead of three recomputing them. Images built before this existed fall back to the job-based path automatically. |
| hopsworks.variables.docker_operations_buildkit_addr | string | `""` | Address of the persistent BuildKit daemon, e.g. tcp://buildkitd-0.buildkitd.hopsworks.svc.cluster.local:1234. Empty starts a private daemon inside each build job, which re-pulls and re-unpacks the base image every time. Leave empty and set global._hopsworks.buildkitd.enabled: the address of the daemon the chart deploys is filled in from buildkitd.name, buildkitd.port and the release namespace. Only set this to point builds at a daemon the chart does not manage. The example is a full pod DNS name rather than a short one because the client verifies the hostname it dials against the certificate: the chart's SANs cover the service and the per-pod names, not a bare "buildkitd", so a short-name address fails verification with mTLS on. |
| hopsworks.variables.docker_operations_buildkit_backoff_limit | string | `"0"` |  |
| hopsworks.variables.docker_operations_buildkit_cache_scope | string | `"shared"` | Scope of the package cache shared between builds: "off", "project" or "shared". Constrained by a pattern rather than an enum: helm-schema infers type: string from the non-empty default and then refuses enum and type together, while pattern coexists with it and rejects the same set of values. The backend still validates at runtime and falls back to "off", since an operator can set this in the variables table without going through the chart. "project" is safe for multi-tenant here because users cannot inject Dockerfile directives: the Dockerfile is generated by the backend, and custom commands supply a shell script that runs inside a RUN. "shared" gives every project one cache and is single-trust-zone only.  This is also the off switch for the toolchain caches a custom-commands build can ask for with HOPSWORKS_BUILD_CACHE (uv, pip, ccache, sccache, maven, gradle, cargo, npm, go). Those are always scoped to the project whatever this is set to, since a script controls what goes into them. Anything other than "off" enables them.  "shared" is the default because the package cache is scoped by index configuration, not by a single cluster-wide id: builds that resolve through the same configuration share, and a project using different index credentials gets a different cache. Every reusable build step also carries a per-project cache-key tag, so a layer is never reused across projects and rotating a credential invalidates reuse, which BuildKit does not do on its own because it leaves secret contents out of cache keys. |
| hopsworks.variables.docker_operations_buildkit_extra_args | string | `""` | Extra arguments appended to every buildctl invocation.  Empty by default. This previously shipped an S3 --export-cache/--import-cache pair. BuildKit resolves S3 credentials at the daemon rather than at the client, so whether it worked depended entirely on what identity the daemon had. On an EKS install with defaultServiceAccount annotations wired for IRSA (see values.aws.yaml) the daemonless build pod carried a web-identity token and the exporter worked. On a cluster with no AWS identity it could not: observed as "no EC2 IMDS role found ... context deadline exceeded" on every build, costing an IMDS timeout per build while caching nothing, with ignore-error hiding the failure rather than avoiding it.  Defaulting it empty therefore removes a remote cache that some installs did have. That is deliberate, because it failed closed and expensively everywhere else, but it is a behaviour change on upgrade rather than the removal of something inert.  Before re-enabling it, give the daemon real credentials and confirm the cache is actually being read. With the daemon enabled it is no longer the build pod, so the build pod's identity no longer applies to it: set buildkitd.serviceAccountName to an account carrying the cloud identity you want the exporter to use. A persistent daemon already avoids the base image re-pull this was reaching for, and does so without leaving the cluster. |
| hopsworks.variables.docker_operations_buildkit_limit_cpu | string | `"2"` |  |
| hopsworks.variables.docker_operations_buildkit_limit_memory | string | `"4G"` |  |
| hopsworks.variables.docker_operations_buildkit_priority_class | string | `""` |  |
| hopsworks.variables.docker_operations_buildkit_replicas | string | `"1"` | Replica count behind a "%d" placeholder in docker_operations_buildkit_addr, e.g. tcp://buildkitd-%d.buildkitd.hopsworks.svc.cluster.local:1234 with replicas 3. Filled in from buildkitd.replicas unless set here.  This spreads load and cache state across daemons. It is not high availability: a project is pinned to one replica by id and is not retried against another, so a project whose daemon is down waits for it to come back. It is not what separates tenants either; that is mTLS plus the per-project cache key. |
| hopsworks.variables.docker_operations_buildkit_request_cpu | string | `"200m"` |  |
| hopsworks.variables.docker_operations_buildkit_request_memory | string | `"500Mi"` |  |
| hopsworks.variables.docker_operations_buildkit_storage | string | `"70Gi"` |  |
| hopsworks.variables.docker_operations_buildkit_tls_locality | string | `"buildkitd"` | Certificate locality, which is what names the key and certificate files inside that Secret. Must match buildkitd.tls.locality, and is filled in from it. |
| hopsworks.variables.docker_operations_buildkit_tls_secret | string | `""` | Secret holding the client certificate the build job presents to the persistent daemon. Empty means the client sends none, which only works against a daemon that requires no client certificate. Filled in from buildkitd.tls when that is enabled. |
| hopsworks.variables.docker_operations_cert_name | string | `"kagent_certificate_bundle.pem"` |  |
| hopsworks.variables.docker_operations_context_orphan_minutes | string | `"120"` | Age in minutes after which a build context in S3 whose build no longer exists is deleted. Covers builds that died with Payara or their node, which the per-build cleanup cannot. |
| hopsworks.variables.docker_operations_default_service_account | string | `"default"` |  |
| hopsworks.variables.docker_operations_delete_jobs_add_description_if_fails | bool | `false` |  |
| hopsworks.variables.docker_operations_delete_jobs_on_completion | string | `"true"` |  |
| hopsworks.variables.docker_operations_docker_context_builder | string | `"AUTO"` |  |
| hopsworks.variables.docker_operations_docker_context_builder_s3_bucket | string | `"${env:S3_BUCKET}"` |  |
| hopsworks.variables.docker_operations_docker_context_builder_s3_endpoint | string | `"${env:S3_ENDPOINT}"` |  |
| hopsworks.variables.docker_operations_docker_context_builder_s3_region | string | `"${env:S3_REGION}"` |  |
| hopsworks.variables.docker_operations_hopsworks_ca_secret_name | string | `"docker-registry-crypto-material"` |  |
| hopsworks.variables.docker_operations_image_pull_secrets | string | `""` |  |
| hopsworks.variables.docker_operations_lock_dependencies | string | `"false"` | Resolve a full dependency set with per-artifact hashes and install only from it. Makes the resolved set reconstructible and fails the build if an index serves different bytes for a version it already served. Needs uv in the base image; builds without it fall back. |
| hopsworks.variables.docker_operations_managed_docker_secrets | string | `""` |  |
| hopsworks.variables.docker_operations_multi_region_copy | string | `"false"` | On a multi-region install, copy the built image to the secondary region instead of running the build again there. Building twice does the work twice and is not guaranteed to land the same image: a custom command or an unpinned package can resolve differently between the two runs, leaving the regions with different content under one tag. Off by default because the copy needs pull and push credentials for both registries in a single job. |
| hopsworks.variables.docker_operations_oci_worker_snapshotter | string | `"auto"` |  |
| hopsworks.variables.docker_operations_push_insecure | string | `"false"` |  |
| hopsworks.variables.docker_operations_registry_container | string | `"docker"` |  |
| hopsworks.variables.docker_operations_registry_http | string | `"false"` |  |
| hopsworks.variables.docker_operations_registry_pod | string | `"docker-registry-0"` |  |
| hopsworks.variables.docker_operations_suspend_jobs | string | `"false"` |  |
| hopsworks.variables.docker_operations_timeout_check_minutes | string | `"15"` |  |
| hopsworks.variables.docker_operations_timeout_delete_minutes | string | `"5"` |  |
| hopsworks.variables.docker_operations_timeout_export_minutes | string | `"15"` |  |
| hopsworks.variables.docker_operations_timeout_listing_minutes | string | `"15"` |  |
| hopsworks.variables.docker_operations_timeout_minutes_buildkit | string | `"120"` |  |
| hopsworks.variables.docker_operations_timeout_tag_minutes | string | `"5"` |  |
| hopsworks.variables.download_allowed | string | `"true"` |  |
| hopsworks.variables.elastic_dir | string | `"/srv/hops/elastic"` |  |
| hopsworks.variables.elastic_https_enabled | string | `"true"` |  |
| hopsworks.variables.elastic_jwt_enabled | string | `"true"` |  |
| hopsworks.variables.elastic_jwt_exp_ms | string | `"1800000"` |  |
| hopsworks.variables.elastic_jwt_url_parameter | string | `"jt"` |  |
| hopsworks.variables.elastic_logs_index_expiration | string | `"604800000"` |  |
| hopsworks.variables.elastic_opendistro_security_enabled | string | `"true"` |  |
| hopsworks.variables.elastic_user | string | `"elastic"` |  |
| hopsworks.variables.elastic_version | string | `"2.19.5"` |  |
| hopsworks.variables.enable_adls_storage_connectors | string | `"false"` |  |
| hopsworks.variables.enable_bigquery_storage_connectors | string | `"true"` |  |
| hopsworks.variables.enable_bring_your_own_kafka | string | `"false"` |  |
| hopsworks.variables.enable_feature_monitoring | string | `"true"` |  |
| hopsworks.variables.enable_fix_receivers_timer | string | `"true"` |  |
| hopsworks.variables.enable_gcs_storage_connectors | string | `"true"` |  |
| hopsworks.variables.enable_jupyter_python_kernel_non_kubernetes | string | `"false"` |  |
| hopsworks.variables.enable_kafka_storage_connectors | string | `"true"` |  |
| hopsworks.variables.enable_metadata_designer | string | `""` |  |
| hopsworks.variables.enable_opensearch_storage_connectors | string | `"true"` |  |
| hopsworks.variables.enable_read_only_git_repositories | string | `"false"` |  |
| hopsworks.variables.enable_redshift_storage_connectors | string | `"true"` |  |
| hopsworks.variables.enable_snowflake_storage_connectors | string | `"true"` |  |
| hopsworks.variables.enable_user_search | string | `"true"` |  |
| hopsworks.variables.epipe_version | string | `"0.20.0"` |  |
| hopsworks.variables.executions_cleaner_batch_size | string | `"50"` |  |
| hopsworks.variables.executions_cleaner_interval_ms | string | `"600000"` |  |
| hopsworks.variables.executions_per_job_limit | string | `"10000"` |  |
| hopsworks.variables.feature_monitoring_max_num_features | string | `"15"` |  |
| hopsworks.variables.featurestore_asof_spine_max_bytes | string | `"1073741824"` |  |
| hopsworks.variables.featurestore_asof_spine_max_columns | string | `"256"` |  |
| hopsworks.variables.featurestore_asof_spine_max_file_age_ms | string | `"86400000"` |  |
| hopsworks.variables.featurestore_asof_spine_max_rows | string | `"1000000"` |  |
| hopsworks.variables.featurestore_db_admin_user | string | `"featurestore_admin_user"` |  |
| hopsworks.variables.featurestore_default_quota | string | `"-1L"` |  |
| hopsworks.variables.featurestore_default_storage_format | string | `"PARQUET"` |  |
| hopsworks.variables.featurestore_metrics_enabled | string | `"true"` |  |
| hopsworks.variables.featurestore_metrics_online_ingestion_enabled | string | `"false"` |  |
| hopsworks.variables.featurestore_online_enabled | string | `"true"` |  |
| hopsworks.variables.featurestore_online_tablespace | string | `""` |  |
| hopsworks.variables.file_preview_image_size | string | `"10000000"` |  |
| hopsworks.variables.file_preview_txt_size | string | `"100"` |  |
| hopsworks.variables.flink_dir | string | `"/srv/hops/flink"` |  |
| hopsworks.variables.flink_user | string | `"flink"` |  |
| hopsworks.variables.flink_version | string | `"1.17.1.0"` |  |
| hopsworks.variables.fs_job_activity_time | string | `"5m"` |  |
| hopsworks.variables.fs_storage_connector_session_duration | string | `"3600"` |  |
| hopsworks.variables.git_bitbucket_http_proxy | string | `""` | Proxy for git traffic to BitBucket over HTTP. Empty means a direct connection. |
| hopsworks.variables.git_bitbucket_https_proxy | string | `""` | Proxy for git traffic to BitBucket over HTTPS. Empty means a direct connection. |
| hopsworks.variables.git_command_timeout_minutes | string | `"60"` |  |
| hopsworks.variables.git_custom_ca_configmap | string | `""` | Name of a ConfigMap holding CA certificates that git operations should trust in addition to the public anchors the git image already ships, so repositories on a self-hosted GitLab / GitHub Enterprise / BitBucket behind a private CA can be cloned and pushed to over HTTPS. The ConfigMap must exist in **every project namespace**, since git runs there, and is expected to be distributed by the platform rather than by this chart. Leave empty to trust only the public anchors. Applies to HTTPS remotes only; SSH host-key verification is unaffected. This value is seeded on every install and upgrade, so edits made in the admin UI do not survive a `helm upgrade` -- configure it here. |
| hopsworks.variables.git_custom_ca_configmap_key | string | `"ca-bundle.crt"` | Key within `git_custom_ca_configmap` holding the certificates. One key, which may hold several concatenated PEM certificates; an admin with several providers puts all their CAs in it. Ignored when `git_custom_ca_configmap` is empty, and must not be blank when it is set. |
| hopsworks.variables.git_disable_tls_verification | string | `"false"` | Disable TLS certificate verification for **all** git remotes, public ones included. Connections can then be intercepted without detection, so prefer naming the CA to trust in `git_custom_ca_configmap`; this exists for deployments where that is not workable. Applies cluster-wide, not per provider. Seeded on every install and upgrade, like the other git variables. |
| hopsworks.variables.git_github_http_proxy | string | `""` | Proxy for git traffic to GitHub over HTTP, e.g. `http://proxy.corp:3128`. Empty means a direct connection. Configured per provider because a deployment may reach each of them by a different route. Traffic between the git container and Hopsworks itself never goes through these proxies. Seeded on every install and upgrade, like the other git variables. |
| hopsworks.variables.git_github_https_proxy | string | `""` | Proxy for git traffic to GitHub over HTTPS. This is the one that matters in practice, since Hopsworks drives git over HTTPS remotes. |
| hopsworks.variables.git_gitlab_http_proxy | string | `""` | Proxy for git traffic to GitLab over HTTP. Empty means a direct connection. |
| hopsworks.variables.git_gitlab_https_proxy | string | `""` | Proxy for git traffic to GitLab over HTTPS. Empty means a direct connection. |
| hopsworks.variables.git_image_version | string | `"1.6-SNAPSHOT"` |  |
| hopsworks.variables.grafana_version | string | `"9.3.16"` |  |
| hopsworks.variables.ha_enabled | string | `"true"` |  |
| hopsworks.variables.hadoop_dir | string | `"/srv/hops/hadoop"` |  |
| hopsworks.variables.hadoop_version | string | `"3.4.3.3-EE-RC0"` |  |
| hopsworks.variables.hdfs_base_storage_policy | string | `"CLOUD"` |  |
| hopsworks.variables.hdfs_default_quota | string | `"-1L"` |  |
| hopsworks.variables.hdfs_log_storage_policy | string | `"CLOUD"` |  |
| hopsworks.variables.hdfs_user | string | `"hdfs"` |  |
| hopsworks.variables.hdfscontentsmanager_base_hopsfs_client | string | `"libhdfs-go"` |  |
| hopsworks.variables.hive2_version | string | `"4.1.0.0-v1"` |  |
| hopsworks.variables.hive_conf_path | string | `"/srv/hops/apache-hive/conf"` |  |
| hopsworks.variables.hive_superuser | string | `"hive"` |  |
| hopsworks.variables.hive_warehouse | string | `"/apps/hive/warehouse"` |  |
| hopsworks.variables.hiveserver_ext_hostname | string | `""` |  |
| hopsworks.variables.hiveserver_ssl_hostname | string | `""` |  |
| hopsworks.variables.hops_db | string | `"hops"` |  |
| hopsworks.variables.hops_rpc_tls | string | `"true"` |  |
| hopsworks.variables.hopsexamples_version | string | `""` |  |
| hopsworks.variables.hopsfsmount_apparmor_profile | string | `""` |  |
| hopsworks.variables.hopsfsmount_log_level | string | `"warn"` |  |
| hopsworks.variables.hopsfsmount_nn_connections | string | `"4"` |  |
| hopsworks.variables.hopsworks_analytics | bool | `false` | When true, the backend creates a reserved 'hopsworks_analytics' project whose members are the cluster admins (HOPS_ADMIN), and attaches a read-only SQL (MySQL) data source onto the local 'hopsworks' database (user hopsworks_analytics_ro_user) to the 'hopsworks_analytics' project itself. Clearing it withdraws the read-only database account, so the two keys must stay required together. Enabling this on a cluster with create_secrets=false additionally requires adding a key named after hopsworks_analytics_ro_user to the hand-created hopsworks-users-secrets, holding the read-only account's password.  This value is the only supported switch. The read-only account, its password and the grants are provisioned by the chart, so flipping the 'hopsworks_analytics' row from the admin variables page creates the project and its members but no data source, and the next upgrade sets the row back to this value.  What the read-only account can read: a curated SELECT allow-list of metadata tables (see roTables in dml/grants.sql.template), not the whole database and never feature data. Several of those tables carry user identities as email addresses: project.username, project_team.team_member, jobs.creator, executions.user and dataset_request.user_email. Anyone with the shared Superset connection, which is every active HOPS_ADMIN, can read them, and the dashboard setup can sample rows from mounted tables into the configured model provider. Treat the account as exposing cluster users' addresses to cluster admins and to that provider. |
| hopsworks.variables.hopsworks_analytics_coding_agent | string | `"claude"` | Which coding agent the Setup Analytics wizard runs: "claude" (Claude Code), "codex" (OpenAI Codex CLI), "copilot" (GitHub Copilot CLI) or "opencode". The wizard uses this without asking, so setting it is how a cluster standardises on one agent; an advanced option in the wizard lets a user run a different one for their own session, which does not write back here. All four are installed in the terminal image under exactly these command names, so the value is the command. Constrained by a pattern rather than an enum for the reason given on docker_operations_package_cache_scope. The frontend falls back to "claude" when the row is missing or holds a value it does not recognise. |
| hopsworks.variables.hopsworks_analytics_ro_user | string | `"hopsworks_ro"` |  |
| hopsworks.variables.hopsworks_analytics_ro_user_adopt_existing | bool | `false` | Take over a database account that already exists under hopsworks_analytics_ro_user but was not created by this chart. Off by default, and the install fails with the account name rather than adopting it, because adoption rewrites the account's password, strips its privileges and replaces them with the analytics allow-list. Set it to true only when that account is yours to hand over. The chart records the account it provisioned in the hopsworks_analytics_ro_user_managed variable and withdraws only that one. |
| hopsworks.variables.hopsworks_analytics_setup_repo | string | `"https://github.com/logicalclocks/okr-dashboards"` | Repository the Setup Analytics wizard clones when the terminal image does not already carry it, so a cluster that cannot reach github.com can point the flow at a reachable mirror instead of failing in the Terminal with a git error. The checkout directory is derived from the last path segment. Constrained to characters that cannot change the meaning of the shell line the URL is spliced into; the frontend falls back to the default when the row is missing or fails that check. |
| hopsworks.variables.hopsworks_db | string | `"hopsworks"` |  |
| hopsworks.variables.hopsworks_dir | string | `"/srv/hops/domains/domain1"` |  |
| hopsworks.variables.hopsworks_enterprise | string | `"true"` |  |
| hopsworks.variables.hopsworks_mysql_user | string | `"hopsworks"` |  |
| hopsworks.variables.hopsworks_public_proxy_url | string | `""` |  |
| hopsworks.variables.hopsworks_rest_log_level | string | `"TEST"` |  |
| hopsworks.variables.hopsworks_user | string | `"payara"` |  |
| hopsworks.variables.hw_group_mapping_sync_enabled | string | `"false"` |  |
| hopsworks.variables.ingestion_job_cores | string | `"1.0"` |  |
| hopsworks.variables.ingestion_job_gpus | string | `"0"` |  |
| hopsworks.variables.ingestion_job_memory | string | `"2048"` |  |
| hopsworks.variables.java_home | string | `""` |  |
| hopsworks.variables.job_name_validation_regex | string | `"^[a-zA-Z0-9_\\-]+$"` |  |
| hopsworks.variables.jupyter_allow_no_limit_shutdown | bool | `true` |  |
| hopsworks.variables.jupyter_dir | string | `"/srv/hops/jupyter"` |  |
| hopsworks.variables.jupyter_group | string | `"hadoop"` |  |
| hopsworks.variables.jupyter_hour_shutdown_options | string | `"8,24,72"` |  |
| hopsworks.variables.jupyter_origin_scheme | string | `"https"` |  |
| hopsworks.variables.jupyter_shell_command | string | `"[\"/bin/bash\", \"--login\", \"-c\", \"cd -L $JUPYTER_DATA_DIR || true && exec bash\"]"` |  |
| hopsworks.variables.jupyter_shutdown_timer_interval | string | `"1m"` |  |
| hopsworks.variables.jupyter_spark_notebook_server_memory_floor_mb | string | `"512"` |  |
| hopsworks.variables.jupyter_ws_ping_interval | string | `"10s"` |  |
| hopsworks.variables.jwt_exp_leeway_sec | string | `"900"` |  |
| hopsworks.variables.jwt_issuer | string | `"hopsworks@logicalclocks.com"` |  |
| hopsworks.variables.jwt_lifetime_ms | string | `"86400000"` |  |
| hopsworks.variables.jwt_signature_algorithm | string | `"HS512"` |  |
| hopsworks.variables.jwt_signing_key_name | string | `"apiKey"` |  |
| hopsworks.variables.kafka_installed | bool | `true` |  |
| hopsworks.variables.kafka_max_num_topics | string | `"100"` |  |
| hopsworks.variables.kafka_num_partitions | string | `"1"` |  |
| hopsworks.variables.kafka_num_replicas | string | `"1"` |  |
| hopsworks.variables.kafka_user | string | `"kafka"` |  |
| hopsworks.variables.kafka_version | string | `"4.3.1"` |  |
| hopsworks.variables.kibana_https_enabled | string | `"true"` |  |
| hopsworks.variables.kibana_multi_tenancy_enabled | string | `"true"` |  |
| hopsworks.variables.kibana_version | string | `"2.19.5"` |  |
| hopsworks.variables.kube_api_max_attempts | string | `"20"` |  |
| hopsworks.variables.kube_hopsworks_default_service_account | string | `"hopsworks-default"` |  |
| hopsworks.variables.kube_knative_domain_name | string | `"hopsworks.ai"` |  |
| hopsworks.variables.kube_knative_lb_domain | string | `""` |  |
| hopsworks.variables.kube_kserve_installed | bool | `true` |  |
| hopsworks.variables.kube_kserve_tensorflow_version | string | `"2.20.0"` |  |
| hopsworks.variables.kube_node_taints_monitor_interval | string | `"10m"` |  |
| hopsworks.variables.kube_scheduling_hopsfsmount_cpu_limits | int | `-1` |  |
| hopsworks.variables.kube_scheduling_hopsfsmount_cpu_requests | int | `1` |  |
| hopsworks.variables.kube_scheduling_hopsfsmount_memory_limits_mb | int | `1024` |  |
| hopsworks.variables.kube_scheduling_jobinit_cpu_limits | int | `-1` |  |
| hopsworks.variables.kube_scheduling_jobinit_cpu_requests | float | `0.5` |  |
| hopsworks.variables.kube_scheduling_jobinit_memory_limits_mb | int | `512` |  |
| hopsworks.variables.kube_scheduling_jobinit_memory_requests_mb | int | `256` |  |
| hopsworks.variables.kube_serving_max_num_instances | string | `"10"` |  |
| hopsworks.variables.kube_serving_min_num_instances | string | `"-1"` |  |
| hopsworks.variables.kube_serving_vllm_omni_versions | string | `"v0.28.0"` |  |
| hopsworks.variables.kube_serving_vllm_versions | string | `"v0.28.0"` |  |
| hopsworks.variables.kube_skip_namespace_creation | bool | `false` |  |
| hopsworks.variables.kube_tainted_nodes | string | `""` |  |
| hopsworks.variables.kube_type | string | `"kube_cluster"` |  |
| hopsworks.variables.kube_user_workload_tolerations | string | `""` | Kubernetes tolerations applied to all user-triggered compute pods. Comma-separated entries of the form key\[=value\]\[:effect\] matching kubectl taint grammar. Effect is optional (empty matches any effect). Example: 'nvidia.com/gpu=true:NoSchedule,dedicated=tenant-a:NoSchedule' |
| hopsworks.variables.kubernetes_installed | string | `"true"` |  |
| hopsworks.variables.kueue_project_default_cluster_queue | string | `"other"` |  |
| hopsworks.variables.kueue_project_default_local_queue | string | `"other"` |  |
| hopsworks.variables.kueue_system_jobs_cluster_queue | string | `""` |  |
| hopsworks.variables.kueue_system_jobs_local_queue | string | `""` |  |
| hopsworks.variables.ldap_account_status | string | `"2"` |  |
| hopsworks.variables.ldap_attr_binary | string | `"java.naming.ldap.attributes.binary"` |  |
| hopsworks.variables.ldap_dyn_group_target | string | `"memberOf"` |  |
| hopsworks.variables.ldap_group_dn | string | `""` |  |
| hopsworks.variables.ldap_group_mapping | string | `"ANY_GROUP->HOPS_USER"` |  |
| hopsworks.variables.ldap_group_mapping_sync_enabled | string | `"false"` |  |
| hopsworks.variables.ldap_group_mapping_sync_interval | string | `"0"` |  |
| hopsworks.variables.ldap_group_search_filter | string | `"member=%d"` |  |
| hopsworks.variables.ldap_group_target | string | `"cn"` |  |
| hopsworks.variables.ldap_groups_search_filter | string | `"(&(objectCategory=group)(cn=%c))"` |  |
| hopsworks.variables.ldap_krb_dyn_grp_search_filter | string | `""` |  |
| hopsworks.variables.ldap_krb_search_filter | string | `"krbPrincipalName=%s"` |  |
| hopsworks.variables.ldap_user_dn | string | `""` |  |
| hopsworks.variables.ldap_user_email | string | `"mail"` |  |
| hopsworks.variables.ldap_user_givenName | string | `"givenName"` |  |
| hopsworks.variables.ldap_user_id | string | `"uid"` |  |
| hopsworks.variables.ldap_user_search_filter | string | `"uid=%s"` |  |
| hopsworks.variables.ldap_user_surname | string | `"sn"` |  |
| hopsworks.variables.library_install_timeout_minutes | string | `"60"` |  |
| hopsworks.variables.lifecycle_webhook_cluster_id | string | `""` | clusterId added to the lifecycle webhook envelope. Omitted when unset. |
| hopsworks.variables.lifecycle_webhook_secret | string | `""` | HMAC-SHA256 signing key for the lifecycle webhook (X-Hopsworks-Signature). Empty sends unsigned. Seeded hidden. |
| hopsworks.variables.lifecycle_webhook_url | string | `""` | Receiver URL for user/project/membership lifecycle events (HTTP POST, at-least-once). Empty disables it. Usable on standalone clusters, not SAAS-only. |
| hopsworks.variables.livy_startup_timeout | string | `"240"` |  |
| hopsworks.variables.livy_version | string | `"0.8.4-incubating-SNAPSHOT-bin"` |  |
| hopsworks.variables.loadbalancer_external_domain_feature_query | string | `nil` | The domain name of the external load balancer for arrowflight. If the load balancer is pre-provisioned then set the domain here, otherwise the hopsworks-update-lb-domains job will discover the domain name and set automatically |
| hopsworks.variables.loadbalancer_external_domain_mysqld | string | `nil` | The domain name of the external load balancer for mysqld. If the load balancer is pre-provisioned then set the domain here, otherwise the hopsworks-update-lb-domains job will discover the domain name and set automatically |
| hopsworks.variables.loadbalancer_external_domain_online_store_rest_server | string | `nil` | The domain name of the external load balancer for RDRS. If the load balancer is pre-provisioned then set the domain here, otherwise the hopsworks-update-lb-domains job will discover the domain name and set automatically |
| hopsworks.variables.loadbalancer_external_domain_opensearch | string | `nil` | The domain name of the external load balancer for opensearch. If the load balancer is pre-provisioned then set the domain here, otherwise the hopsworks-update-lb-domains job will discover the domain name and set automatically |
| hopsworks.variables.loadbalancer_external_domain_trino | string | `nil` | The domain name of the external load balancer for Trino. If the load balancer is pre-provisioned then set the domain here, otherwise the hopsworks-update-lb-domains job will discover the domain name and set automatically |
| hopsworks.variables.localhost | string | `"false"` |  |
| hopsworks.variables.log_history_limit | string | `"30"` | Cap on entries kept in the Log History UI (serving/agent deployments, Jupyter). Archives beyond this count are deleted after each archive, oldest first. A value <= 0 disables rotation. |
| hopsworks.variables.logstash_ip | string | `""` |  |
| hopsworks.variables.logstash_port | string | `""` |  |
| hopsworks.variables.logstash_port_beam_jobserver_local | string | `""` |  |
| hopsworks.variables.logstash_port_serving | string | `""` |  |
| hopsworks.variables.logstash_port_sklearn_serving | string | `""` |  |
| hopsworks.variables.logstash_port_tf_serving | string | `""` |  |
| hopsworks.variables.logstash_version | string | `"7.16.3"` |  |
| hopsworks.variables.managed_cloud_redirect_uri | string | `""` |  |
| hopsworks.variables.managed_docker_registry | string | `"false"` |  |
| hopsworks.variables.management_mode | string | `""` | SAAS bridge: 'STANDALONE' (default, stock Hopsworks) or 'SAAS_MANAGED' (auth and project quota delegated to hopsworks-saas). Unset falls back to STANDALONE. |
| hopsworks.variables.max_allowed_long_running_http_requests | string | `"50"` |  |
| hopsworks.variables.max_concurrent_base_sync_ops | string | `"5"` |  |
| hopsworks.variables.max_env_yml_byte_size | string | `"20000"` |  |
| hopsworks.variables.max_num_proj_per_user | string | `"10"` |  |
| hopsworks.variables.max_status_poll_retry | string | `"5"` |  |
| hopsworks.variables.mount_hopsfs_in_python_job | bool | `true` | Deprecated. Python Apps always mount HopsFS; this remains only for legacy Python jobs. |
| hopsworks.variables.mount_hopsfs_ray_job_container | string | `"true"` |  |
| hopsworks.variables.mr_user | string | `"mapred"` |  |
| hopsworks.variables.multiregion_watchdog_enabled | string | `"false"` |  |
| hopsworks.variables.multiregion_watchdog_interval | string | `"5s"` |  |
| hopsworks.variables.multiregion_watchdog_region | string | `""` |  |
| hopsworks.variables.multiregion_watchdog_url | string | `""` |  |
| hopsworks.variables.mysql_dir | string | `"/srv/hops/mysql"` |  |
| hopsworks.variables.ndb_dir | string | `"/srv/hop/mysql-cluster"` |  |
| hopsworks.variables.ndb_user | string | `""` |  |
| hopsworks.variables.ndb_version | string | `"21.04.15"` |  |
| hopsworks.variables.ndbinfo_db | string | `"ndbinfo"` |  |
| hopsworks.variables.news_webflow_api_key | string | `"dcc84358bfd37ffc68dbf18c68f74f478ff160d2286094077a9415ee03fbc805"` |  |
| hopsworks.variables.news_webflow_api_url | string | `"https://api.webflow.com/v2/collections/66bdd44475e24741477e1ae3/items"` |  |
| hopsworks.variables.notebook_converter_job_timeout_sec | string | `"300"` |  |
| hopsworks.variables.npm_registry_url | string | `""` | Registry npm package installs resolve from, applied as `npm config set registry <url>` in the environment build so the built image also resolves from it at runtime. Empty leaves npm on its compiled-in default (registry.npmjs.org). |
| hopsworks.variables.oauth_account_status | string | `"1"` |  |
| hopsworks.variables.oauth_group_mapping | string | `""` |  |
| hopsworks.variables.oauth_group_mapping_enabled | string | `"false"` |  |
| hopsworks.variables.oauth_group_mapping_sync_enabled | string | `"false"` |  |
| hopsworks.variables.oauth_logout_redirect_uri | string | `"hopsworks/"` |  |
| hopsworks.variables.oauth_redirect_uri | string | `"hopsworks/callback"` |  |
| hopsworks.variables.onlinefs_service_thread_number | string | `"10"` |  |
| hopsworks.variables.onlinefs_user_email | string | `"onlinefs@hopsworks.ai"` |  |
| hopsworks.variables.onlinefs_user_password | string | `"onlinefspw"` |  |
| hopsworks.variables.opensearch_default_embedding_index | string | `""` |  |
| hopsworks.variables.opensearch_index_mapping_limit | string | `"1000"` |  |
| hopsworks.variables.opensearch_num_default_embedding_index | string | `"1"` |  |
| hopsworks.variables.payara_dir | string | `"/opt/payara/appserver/glassfish/domains/domain1"` |  |
| hopsworks.variables.pki_ca_configuration | string | `"{\"rootCA\":{},\"intermediateCA\":{},\"kubernetesCA\":{\"subjectAlternativeName\":{\"dns\":[\"hopsworks0.logicalclocks.com\",\"hops-kubernetes\",\"hops-kubernetes.default\",\"hops-kubernetes.default.svc\",\"hops-kubernetes.default.svc.cluster\",\"hops-kubernetes.default.svc.cluster.local\",\"*.hops-system.svc\"],\"ip\":[\"10.244.0.1\",\"192.168.30.101\",\"127.0.0.1\",\"10.96.0.10\",\"10.96.0.1\"]}}}"` |  |
| hopsworks.variables.platform_intelligence_llm_api_key | string | `""` |  |
| hopsworks.variables.platform_intelligence_llm_base_url | string | `""` |  |
| hopsworks.variables.platform_intelligence_llm_model | string | `""` |  |
| hopsworks.variables.preinstalled_python_lib_names | string | `"pydoop, pyspark, jupyterlab, sparkmagic, hdfscontents, pyjks, hops-apache-beam, pyopenssl"` |  |
| hopsworks.variables.project_namespace_labels | string | `""` |  |
| hopsworks.variables.project_namespace_network_policy_allowed_namespaces | string | `""` |  |
| hopsworks.variables.project_namespace_network_policy_enabled | bool | `true` |  |
| hopsworks.variables.project_namespace_network_policy_reconcile_interval | string | `"1m"` |  |
| hopsworks.variables.prometheus_port | string | `"9089"` |  |
| hopsworks.variables.provenance_archive_delay | string | `"86400"` |  |
| hopsworks.variables.provenance_archive_size | string | `"10"` |  |
| hopsworks.variables.provenance_cleaner_period | string | `"3600"` |  |
| hopsworks.variables.provenance_graph_max_size | string | `"10000"` |  |
| hopsworks.variables.provenance_type | string | `"FULL"` |  |
| hopsworks.variables.public_https_port | string | `""` |  |
| hopsworks.variables.pushgateway_cleaner_batch_size | string | `"100"` |  |
| hopsworks.variables.pushgateway_group_ttl_minutes | string | `"15"` |  |
| hopsworks.variables.pushgateway_monitor_interval_ms | string | `"300000"` |  |
| hopsworks.variables.py4j_archive | string | `""` |  |
| hopsworks.variables.pypi_indexer_timer_enabled | string | `"true"` |  |
| hopsworks.variables.pypi_indexer_timer_interval | string | `"1d"` |  |
| hopsworks.variables.pypi_rest_endpoint | string | `"https://pypi.org/pypi/{package}/json"` |  |
| hopsworks.variables.pypi_simple_endpoint | string | `"https://pypi.org/simple/"` |  |
| hopsworks.variables.python_job_cores | string | `"1.0"` |  |
| hopsworks.variables.python_job_gpus | string | `"0"` |  |
| hopsworks.variables.python_job_kube_waiting_timeout_ms | string | `"300000"` |  |
| hopsworks.variables.python_job_memory | string | `"2048"` |  |
| hopsworks.variables.python_library_updates_monitor_interval | string | `"1d"` |  |
| hopsworks.variables.python_pod_kill_grace_period_seconds | string | `"60"` |  |
| hopsworks.variables.pythonapp_cores | string | `"1.0"` |  |
| hopsworks.variables.pythonapp_gpus | string | `"0"` |  |
| hopsworks.variables.pythonapp_memory | string | `"2048"` |  |
| hopsworks.variables.quotas_featuregroups_online_disabled | string | `"-1"` |  |
| hopsworks.variables.quotas_featuregroups_online_enabled | string | `"-1"` |  |
| hopsworks.variables.quotas_max_parallel_executions | string | `"-1"` |  |
| hopsworks.variables.quotas_model_deployments_running | string | `"-1"` |  |
| hopsworks.variables.quotas_model_deployments_total | string | `"-1"` |  |
| hopsworks.variables.quotas_training_datasets | string | `"-1"` |  |
| hopsworks.variables.ray_cluster_max_worker_replicas | string | `"20"` |  |
| hopsworks.variables.ray_cluster_shutdown_after_completion | string | `"true"` |  |
| hopsworks.variables.ray_cluster_start_wait_time_seconds | string | `"360"` |  |
| hopsworks.variables.ray_cluster_termination_grace_period_seconds | string | `"10"` |  |
| hopsworks.variables.ray_enabled | bool | `false` | ray_enabled indicates if hopsworks configurations for ray should be applied |
| hopsworks.variables.ray_job_driver_cores | string | `"1.0"` |  |
| hopsworks.variables.ray_job_driver_gpus | string | `"0"` |  |
| hopsworks.variables.ray_job_driver_memory | string | `"4096"` |  |
| hopsworks.variables.ray_job_pod_kill_grace_period_seconds | string | `"300"` |  |
| hopsworks.variables.ray_job_worker_cores | string | `"1.0"` |  |
| hopsworks.variables.ray_job_worker_gpus | string | `"0"` |  |
| hopsworks.variables.ray_job_worker_memory | string | `"4096"` |  |
| hopsworks.variables.ray_materialization_dir | string | `"/srv/hops/ray/job"` |  |
| hopsworks.variables.ray_version | string | `"2.58.0"` |  |
| hopsworks.variables.recovery_path | string | `""` |  |
| hopsworks.variables.reject_remote_user_no_group | string | `"false"` |  |
| hopsworks.variables.remote_auth_need_consent | string | `"true"` |  |
| hopsworks.variables.requests_verify | string | `"true"` |  |
| hopsworks.variables.reserved_project_names | string | `"hopsworks,information_schema,airflow,glassfish_timers,grafana,hops,metastore,mysql,ndbinfo,performance_schema,sqoop,sys,base,python37,python38,python39,python310,filebeat,airflow,git,onlinefs,sklearnserver,rondb_replication,default,kube-system,kube-public,kube-node-lease,kube_system,kube_public,kube_node_lease"` |  |
| hopsworks.variables.rmyarn_user | string | `"rmyarn"` |  |
| hopsworks.variables.rondb_quotas | string | `""` | RONDB quotas in csv format. e.g `rate-per-sec=1000,max-transaction-size=100`. Refer to https://docs.rondb.com/rondb_rate_limits_quotas/ for the full list of arguments and their definitions. |
| hopsworks.variables.rondb_usage_cache_ttl_seconds | string | `"60"` | How often (seconds) the cached RonDB per-database memory usage snapshot is refreshed. The backing ndbinfo scan costs the same for one database as for all, so one snapshot serves every project. |
| hopsworks.variables.rondb_usage_query_timeout_seconds | string | `"10"` | Query timeout (seconds) for the ndbinfo memory usage scan. Scan duration grows with the cluster's table count; raise this on large clusters if usage stops showing in the project quotas UI. |
| hopsworks.variables.saas_entry_point_url | string | `""` | SAAS bridge: auth entry-point URL the frontend redirects to when management_mode is SAAS_MANAGED. Ignored in STANDALONE. |
| hopsworks.variables.scikit_learn_version | string | `"1.3.2"` |  |
| hopsworks.variables.service_jwt_exp_leeway_sec | string | `"172800000"` |  |
| hopsworks.variables.service_jwt_lifetime_ms | string | `"604800000"` |  |
| hopsworks.variables.service_key_rotation_enabled | string | `"false"` |  |
| hopsworks.variables.service_key_rotation_interval | string | `"2d"` |  |
| hopsworks.variables.serving_allow_stop_after_seconds | string | `"30"` |  |
| hopsworks.variables.serving_connection_pool_size | string | `"40"` |  |
| hopsworks.variables.serving_feature_log_materialization_cron | string | `"0 0 0 * * ? *"` |  |
| hopsworks.variables.serving_feature_log_materialization_row_limit | string | `"50000000"` |  |
| hopsworks.variables.serving_feature_log_online_ttl_hours | string | `"30"` |  |
| hopsworks.variables.serving_feature_logger_batch_bytes | string | `"1048576"` |  |
| hopsworks.variables.serving_feature_logger_batch_seconds | string | `"5"` |  |
| hopsworks.variables.serving_feature_logger_client_pool_size | string | `"3"` |  |
| hopsworks.variables.serving_feature_logger_client_req_timeout_seconds | string | `"3"` |  |
| hopsworks.variables.serving_feature_logger_flush_bytes | string | `"1048576"` |  |
| hopsworks.variables.serving_feature_logger_flush_interval_seconds | string | `"300"` |  |
| hopsworks.variables.serving_feature_logger_max_buffer_bytes | string | `"67108864"` |  |
| hopsworks.variables.serving_feature_logger_max_event_bytes | string | `"8388608"` |  |
| hopsworks.variables.serving_feature_logger_max_event_rows | string | `"512"` |  |
| hopsworks.variables.serving_feature_logger_queue_size | string | `"1000"` |  |
| hopsworks.variables.serving_feature_logger_shutdown_seconds | string | `"20"` |  |
| hopsworks.variables.serving_feature_logging_transport | string | `"realtime"` |  |
| hopsworks.variables.serving_max_route_connections | string | `"10"` |  |
| hopsworks.variables.serving_redeploy_not_found_after_seconds | string | `"120"` |  |
| hopsworks.variables.serving_state_manager_batch_size | string | `"25"` |  |
| hopsworks.variables.serving_state_manager_enabled | string | `"true"` |  |
| hopsworks.variables.serving_state_manager_interval_ms | string | `"300000"` |  |
| hopsworks.variables.spark_dir | string | `"/srv/hops/spark"` |  |
| hopsworks.variables.spark_executor_min_memory | string | `"1024"` |  |
| hopsworks.variables.spark_hops_utils_dir | string | `"/srv/hops/artifacts"` |  |
| hopsworks.variables.spark_job_driver_cores | string | `"1.0"` |  |
| hopsworks.variables.spark_job_driver_memory | string | `"2048"` |  |
| hopsworks.variables.spark_job_executor_cores | string | `"1.0"` |  |
| hopsworks.variables.spark_job_executor_memory | string | `"4096"` |  |
| hopsworks.variables.spark_launcher_sa_annotations | string | `""` |  |
| hopsworks.variables.spark_pod_kill_grace_period_seconds | string | `"1200"` |  |
| hopsworks.variables.spark_remove_job_when_completed | string | `"true"` |  |
| hopsworks.variables.spark_ui_logs_offset | string | `"512000"` |  |
| hopsworks.variables.spark_user | string | `"spark"` |  |
| hopsworks.variables.spark_version | string | `"4.1.3.0"` |  |
| hopsworks.variables.srvmanager_password | string | `"srvmanagerpwd"` |  |
| hopsworks.variables.staging_dir | string | `"/srv/hops/staging"` |  |
| hopsworks.variables.statistics_cleaner_batch_size | string | `"1000"` |  |
| hopsworks.variables.statistics_cleaner_interval_ms | string | `"900000"` |  |
| hopsworks.variables.streamlit_sharing | bool | `false` |  |
| hopsworks.variables.sudoers_dir | string | `"/srv/hops/sbin"` |  |
| hopsworks.variables.superset_admin_roles | string | `"Admin"` |  |
| hopsworks.variables.superset_proxy_connect_timeout_ms | string | `"10000"` |  |
| hopsworks.variables.superset_proxy_connection_request_timeout_ms | string | `"10000"` |  |
| hopsworks.variables.superset_proxy_max_connections | string | `"50"` |  |
| hopsworks.variables.superset_proxy_read_timeout_ms | string | `"180000"` |  |
| hopsworks.variables.superset_user_roles | string | `"Gamma,sql_lab,Dataset"` |  |
| hopsworks.variables.support_email_addr | string | `"support@hopsworks.ai"` |  |
| hopsworks.variables.tag_history_archive_max_events | string | `"20000"` | Largest number of tag history events an archive flip will write, one per tag key of every existing attachment. Turning archiving on or off writes them in a single transaction, which cannot be split without losing the baseline it exists to record, so the work is bounded by NDB's MaxNoOfConcurrentOperations and the request timeout rather than by paging. Counted in events because an attachment with several keys is several rows; a limit on attachments alone did not bound the work. Above this the call is refused with the count and this limit instead of rolling back with no readable cause. Raise it alongside MaxNoOfConcurrentOperations. |
| hopsworks.variables.tag_history_cleaner_batch_size | string | `"1000"` | Rows deleted per transaction by the tag history retention sweep. Bounded so a large sweep is a series of short transactions rather than one that runs into NDB's MaxNoOfConcurrentOperations. |
| hopsworks.variables.tag_history_cleaner_interval_ms | string | `"86400000"` | How often the tag history retention sweep runs, in milliseconds. Values below 60000 are refused and fall back to 24h. |
| hopsworks.variables.tag_history_retention_days | string | `"0"` | How many days of tag history to keep. tag_history is append-only and nothing else bounds it: clearing a schema's archive flag stops new rows but deletes none, so without retention the only way to reclaim the space is by hand. "0" keeps everything, which is the default because deleting analytics history as a side effect of an upgrade would surprise everyone reporting on it. Set a number of days to bound it. |
| hopsworks.variables.tensorboard_max_last_accessed | string | `"1140000"` |  |
| hopsworks.variables.tensorboard_max_reload_threads | string | `"1"` |  |
| hopsworks.variables.tensorflow_version | string | `"2.20.0"` |  |
| hopsworks.variables.testconnector_image_version | string | `"1.0"` |  |
| hopsworks.variables.tf_spark_connector_version | string | `""` |  |
| hopsworks.variables.trino_default_catalog | string | `"hive"` |  |
| hopsworks.variables.trino_events_cleaner_batch_size | string | `"1000"` |  |
| hopsworks.variables.trino_events_delete_after_days | string | `"61"` |  |
| hopsworks.variables.twofactor_auth | string | `"false"` |  |
| hopsworks.variables.twofactor_excluded_groups | string | `"AGENT;CLUSTER_AGENT"` |  |
| hopsworks.variables.unix_usernames_conf | string | `"{\\\"glassfish\\\":\\\"glassfish\\\",\\\"hdfs\\\":\\\"hdfs\\\",\\\"rmyarn\\\":\\\"rmyarn\\\",\\\"yarn\\\":\\\"yarn\\\",\\\"hive\\\":\\\"hive\\\",\\\"livy\\\":\\\"livy\\\",\\\"flink\\\":\\\"flink\\\",\\\"consul\\\":\\\"consul\\\",\\\"hopsmon\\\":\\\"hopsmon\\\",\\\"zookeeper\\\":\\\"zookeeper\\\",\\\"onlinefs\\\":\\\"onlinefs\\\",\\\"elastic\\\":\\\"elastic\\\",\\\"kagent\\\":\\\"kagent\\\",\\\"mysql\\\":\\\"mysql\\\",\\\"airflow\\\":\\\"airflow\\\"}"` |  |
| hopsworks.variables.upload_chunk_size | string | `"10485760"` |  |
| hopsworks.variables.upload_policy | string | `"enabled"` | Who may upload files into the cluster. `enabled` allows any user with write access to the destination dataset, `admins_only` restricts uploads to members of `HOPS_ADMIN`, `disabled` blocks everyone including administrators. Applies to the web UI and to clients such as the Python SDK. Unrecognised values fall back to `enabled`. Note that this governs uploading new files only: operations on files already in the cluster filesystem, such as installing a python library from an existing path, are unaffected. |
| hopsworks.variables.user_cert_valid_days | string | `"12"` |  |
| hopsworks.variables.verification_path | string | `"hopsworks-api/api/auth/verify"` |  |
| hopsworks.variables.yarn_default_payment_type | string | `"NOLIMIT"` |  |
| hopsworks.variables.yarn_default_quota | string | `"60000000"` |  |
| hopsworks.variables.yarn_user | string | `"yarn"` |  |
| hopsworks.variables.zookeeper_version | string | `"3.7.1"` |  |
| hopsworks.velero.backup | object | `{"dynamicNamespaceFilter":{"enabled":true,"schedule":"@hourly"},"enabled":null,"excludedNamespaces":["kube-system","kube-public","kube-node-lease","argocd","default","ingress-nginx"],"includedNamespaces":[],"mainScheduleName":"k8s-backups-main","schedule":null,"storageLocation":{"create":true,"name":"hopsworks-bsl","s3ForcePathStyle":null,"storagePrefix":"k8s_backup"},"ttl":null,"usersScheduleName":"k8s-backups-users-resources"}` | backup configuration |
| hopsworks.velero.backup.dynamicNamespaceFilter | object | `{"enabled":true,"schedule":"@hourly"}` | Configure cron job to dynamically list the project namespaces and update the users backup schedule, and to discover satellite namespaces (labeled hopsworks.ai/onlinefs-cluster) and update the main backup schedule. If includedNamespaces is defined then this is disabled by default. |
| hopsworks.velero.backup.enabled | string | `nil` | Enable or disable velero for taking backups |
| hopsworks.velero.backup.excludedNamespaces | list | `["kube-system","kube-public","kube-node-lease","argocd","default","ingress-nginx"]` | array of namespaces to exclude their resources in the backup. for ArgoCD, explicitly include all non-user namespaces since reconciliation makes dynamicNamespaceFilter ineffective. |
| hopsworks.velero.backup.includedNamespaces | list | `[]` | array of namespaces to include their resources in the backup |
| hopsworks.velero.backup.mainScheduleName | string | `"k8s-backups-main"` | The name of the main backup schedule that backs up the generated secrets from the cluster, the backups metadata configmaps, and serving configmaps and secrets. |
| hopsworks.velero.backup.schedule | string | `nil` | Backup schedule |
| hopsworks.velero.backup.storageLocation | object | `{"create":true,"name":"hopsworks-bsl","s3ForcePathStyle":null,"storagePrefix":"k8s_backup"}` | The storage backup location configuration |
| hopsworks.velero.backup.storageLocation.create | bool | `true` | create a backup storage location. If disabled, we expect a backup storage location that exists with the name velero.backup.storageLocation.name. |
| hopsworks.velero.backup.storageLocation.name | string | `"hopsworks-bsl"` | storage backup location name. If create is enabled, we will create a new backup storage location otherwise we expect that the backup storage location to exist. |
| hopsworks.velero.backup.storageLocation.s3ForcePathStyle | string | `nil` | Force S3 path-style addressing for the velero backup storage location. When unset (null), defaults to true for MinIO and unset for managed S3. Set explicitly to true for S3-compatible object storage that does not support virtual-hosted-style addressing (e.g. evroc, Ceph RadosGW). |
| hopsworks.velero.backup.storageLocation.storagePrefix | string | `"k8s_backup"` | The storage prefix to store the backups under in the configured bucket |
| hopsworks.velero.backup.ttl | string | `nil` | The amount of time before backups created on this schedule are eligible for garbage collection. If not specified, a default value of 30 days will be used. The value must be a Go-style duration using hour/minute/second units (e.g. 24h, 168h, or 24h0m0s). Calendar units such as "d" or "w" are not supported. |
| hopsworks.velero.backup.usersScheduleName | string | `"k8s-backups-users-resources"` | The name of the users backup schedule that backs up the users' resources in their project namespaces. |
| hopsworks.velero.deploymentName | string | `"velero"` | The name of the velero deployment |
| hopsworks.velero.enforcePrerequisiteCheck | bool | `true` | When enabled, Helm will verify that the required Velero CRDs and Deployment already exist in the cluster using `lookup` and fail if they are missing. Disable this for offline rendering with `helm template`. |
| hopsworks.velero.namespace | string | `"velero"` | The velero namespace. It should be on a different namespace other than the Hopsworks install namespace to avoid accidentaly deleting the Hopsworks namespace when uninstalling velero. |
| hopsworks.velero.restore.mainScheduleBackupId | string | `nil` | The backup ID used for the restore operation of the main schedule. If unset, the latest backup from the main schedule will be used. This parameter is primarily used internally by the Helm chart during in-place restores, but also serves to record which backup ID was restored. |
| hopsworks.velero.restore.usersScheduleBackupId | string | `nil` | The backup ID used for the restore operation of the users schedule. If unset, the latest backup from the users schedule will be used. This parameter is primarily used internally by the Helm chart during in-place restores, but also serves to record which backup ID was restored. |
| hopsworks.velero.ttlSecondsAfterFinished | string | `nil` | TTL in seconds for the velero-create-cloud-credentials Job. Overrides global default. |
| hopsworks.volumeMounts.admin | list | `[]` |  |
| hopsworks.volumeMounts.migrate | list | `[]` |  |
| hopsworks.volumeMounts.worker | list | `[]` |  |
| hopsworks.volumes.admin | list | `[]` |  |
| hopsworks.volumes.migrate | list | `[]` |  |
| hopsworks.volumes.worker | list | `[]` |  |
| hopsworks.wipeWhenUninstall\[0\].apiGroup | string | `"remoteshuffleservices.uniffle.apache.org"` |  |
| hopsworks.wipeWhenUninstall\[0\].resources\[0\] | string | `"remoteshuffleservices"` |  |
| hopsworks.wipeWhenUninstall\[10\].apiGroup | string | `"admissionregistration.k8s.io"` |  |
| hopsworks.wipeWhenUninstall\[10\].resources\[0\] | string | `"mutatingwebhookconfigurations"` |  |
| hopsworks.wipeWhenUninstall\[10\].resources\[1\] | string | `"validatingwebhookconfigurations"` |  |
| hopsworks.wipeWhenUninstall\[11\].apiGroup | string | `""` |  |
| hopsworks.wipeWhenUninstall\[11\].resources\[0\] | string | `"secrets"` |  |
| hopsworks.wipeWhenUninstall\[11\].resources\[1\] | string | `"serviceaccounts"` |  |
| hopsworks.wipeWhenUninstall\[11\].resources\[2\] | string | `"configmaps"` |  |
| hopsworks.wipeWhenUninstall\[11\].resources\[3\] | string | `"persistentvolumeclaims"` |  |
| hopsworks.wipeWhenUninstall\[11\].resources\[4\] | string | `"persistentvolumes"` |  |
| hopsworks.wipeWhenUninstall\[11\].resources\[5\] | string | `"pods"` |  |
| hopsworks.wipeWhenUninstall\[11\].resources\[6\] | string | `"services"` |  |
| hopsworks.wipeWhenUninstall\[11\].resources\[7\] | string | `"endpoints"` |  |
| hopsworks.wipeWhenUninstall\[11\].resources\[8\] | string | `"namespaces"` |  |
| hopsworks.wipeWhenUninstall\[1\].apiGroup | string | `"sparkapplications.sparkoperator.k8s.io"` |  |
| hopsworks.wipeWhenUninstall\[1\].resources\[0\] | string | `"sparkapplications"` |  |
| hopsworks.wipeWhenUninstall\[2\].apiGroup | string | `"hopsworkscerts.certs.hopsworks.ai"` |  |
| hopsworks.wipeWhenUninstall\[2\].resources\[0\] | string | `"hopsworkscerts"` |  |
| hopsworks.wipeWhenUninstall\[3\].apiGroup | string | `"certs.hopsworks.ai"` |  |
| hopsworks.wipeWhenUninstall\[3\].resources\[0\] | string | `"hopsworkscerts"` |  |
| hopsworks.wipeWhenUninstall\[4\].apiGroup | string | `"batch"` |  |
| hopsworks.wipeWhenUninstall\[4\].resources\[0\] | string | `"jobs"` |  |
| hopsworks.wipeWhenUninstall\[4\].resources\[1\] | string | `"cronjobs"` |  |
| hopsworks.wipeWhenUninstall\[5\].apiGroup | string | `"apps"` |  |
| hopsworks.wipeWhenUninstall\[5\].resources\[0\] | string | `"deployments"` |  |
| hopsworks.wipeWhenUninstall\[5\].resources\[1\] | string | `"statefulsets"` |  |
| hopsworks.wipeWhenUninstall\[5\].resources\[2\] | string | `"daemonsets"` |  |
| hopsworks.wipeWhenUninstall\[6\].apiGroup | string | `"rbac.authorization.k8s.io"` |  |
| hopsworks.wipeWhenUninstall\[6\].resources\[0\] | string | `"roles"` |  |
| hopsworks.wipeWhenUninstall\[6\].resources\[1\] | string | `"rolebindings"` |  |
| hopsworks.wipeWhenUninstall\[6\].resources\[2\] | string | `"clusterroles"` |  |
| hopsworks.wipeWhenUninstall\[6\].resources\[3\] | string | `"clusterrolebindings"` |  |
| hopsworks.wipeWhenUninstall\[7\].apiGroup | string | `"networking.k8s.io"` |  |
| hopsworks.wipeWhenUninstall\[7\].resources\[0\] | string | `"networkpolicies"` |  |
| hopsworks.wipeWhenUninstall\[7\].resources\[1\] | string | `"ingresses"` |  |
| hopsworks.wipeWhenUninstall\[8\].apiGroup | string | `"storage.k8s.io"` |  |
| hopsworks.wipeWhenUninstall\[8\].resources\[0\] | string | `"storageclasses"` |  |
| hopsworks.wipeWhenUninstall\[9\].apiGroup | string | `"scheduling.k8s.io"` |  |
| hopsworks.wipeWhenUninstall\[9\].resources\[0\] | string | `"priorityclasses"` |  |
| hw-kueue.clusterQueues\[0\].annotations | object | `{}` |  |
| hw-kueue.clusterQueues\[0\].labels | object | `{}` |  |
| hw-kueue.clusterQueues\[0\].name | string | `"other"` |  |
| hw-kueue.clusterQueues\[0\].spec.cohort | string | `"cluster"` |  |
| hw-kueue.clusterQueues\[0\].spec.fairSharing.weight | string | `"1"` |  |
| hw-kueue.clusterQueues\[0\].spec.namespaceSelector | object | `{}` |  |
| hw-kueue.clusterQueues\[0\].spec.queueingStrategy | string | `"BestEffortFIFO"` |  |
| hw-kueue.clusterQueues\[0\].spec.resourceGroups\[0\].coveredResources\[0\] | string | `"cpu"` |  |
| hw-kueue.clusterQueues\[0\].spec.resourceGroups\[0\].coveredResources\[1\] | string | `"memory"` |  |
| hw-kueue.clusterQueues\[0\].spec.resourceGroups\[0\].coveredResources\[2\] | string | `"pods"` |  |
| hw-kueue.clusterQueues\[0\].spec.resourceGroups\[0\].coveredResources\[3\] | string | `"nvidia.com/gpu"` |  |
| hw-kueue.clusterQueues\[0\].spec.resourceGroups\[0\].flavors\[0\].name | string | `"default-flavor"` |  |
| hw-kueue.clusterQueues\[0\].spec.resourceGroups\[0\].flavors\[0\].resources\[0\].name | string | `"cpu"` |  |
| hw-kueue.clusterQueues\[0\].spec.resourceGroups\[0\].flavors\[0\].resources\[0\].nominalQuota | int | `0` |  |
| hw-kueue.clusterQueues\[0\].spec.resourceGroups\[0\].flavors\[0\].resources\[1\].name | string | `"memory"` |  |
| hw-kueue.clusterQueues\[0\].spec.resourceGroups\[0\].flavors\[0\].resources\[1\].nominalQuota | int | `0` |  |
| hw-kueue.clusterQueues\[0\].spec.resourceGroups\[0\].flavors\[0\].resources\[2\].name | string | `"pods"` |  |
| hw-kueue.clusterQueues\[0\].spec.resourceGroups\[0\].flavors\[0\].resources\[2\].nominalQuota | int | `0` |  |
| hw-kueue.clusterQueues\[0\].spec.resourceGroups\[0\].flavors\[0\].resources\[3\].name | string | `"nvidia.com/gpu"` |  |
| hw-kueue.clusterQueues\[0\].spec.resourceGroups\[0\].flavors\[0\].resources\[3\].nominalQuota | int | `0` |  |
| hw-kueue.cohorts\[0\].annotations | object | `{}` |  |
| hw-kueue.cohorts\[0\].labels | object | `{}` |  |
| hw-kueue.cohorts\[0\].name | string | `"cluster"` |  |
| hw-kueue.cohorts\[0\].spec.resourceGroups\[0\].coveredResources\[0\] | string | `"cpu"` |  |
| hw-kueue.cohorts\[0\].spec.resourceGroups\[0\].coveredResources\[1\] | string | `"memory"` |  |
| hw-kueue.cohorts\[0\].spec.resourceGroups\[0\].coveredResources\[2\] | string | `"pods"` |  |
| hw-kueue.cohorts\[0\].spec.resourceGroups\[0\].coveredResources\[3\] | string | `"nvidia.com/gpu"` |  |
| hw-kueue.cohorts\[0\].spec.resourceGroups\[0\].flavors\[0\].name | string | `"default-flavor"` |  |
| hw-kueue.cohorts\[0\].spec.resourceGroups\[0\].flavors\[0\].resources\[0\].name | string | `"cpu"` |  |
| hw-kueue.cohorts\[0\].spec.resourceGroups\[0\].flavors\[0\].resources\[0\].nominalQuota | int | `100` |  |
| hw-kueue.cohorts\[0\].spec.resourceGroups\[0\].flavors\[0\].resources\[1\].name | string | `"memory"` |  |
| hw-kueue.cohorts\[0\].spec.resourceGroups\[0\].flavors\[0\].resources\[1\].nominalQuota | string | `"200Gi"` |  |
| hw-kueue.cohorts\[0\].spec.resourceGroups\[0\].flavors\[0\].resources\[2\].name | string | `"pods"` |  |
| hw-kueue.cohorts\[0\].spec.resourceGroups\[0\].flavors\[0\].resources\[2\].nominalQuota | int | `100` |  |
| hw-kueue.cohorts\[0\].spec.resourceGroups\[0\].flavors\[0\].resources\[3\].name | string | `"nvidia.com/gpu"` |  |
| hw-kueue.cohorts\[0\].spec.resourceGroups\[0\].flavors\[0\].resources\[3\].nominalQuota | int | `50` |  |
| hw-kueue.fullnameOverride | string | `"kueue"` |  |
| hw-kueue.hopsworkslib | object | `{}` | override hopsworkslib values |
| hw-kueue.imagePullPolicy | string | `"Always"` |  |
| hw-kueue.installJob.configMapMountPath | string | `"/mnt/kueue-resources"` |  |
| hw-kueue.installJob.configMapName | string | `"kueue-objects-install-job-resources"` |  |
| hw-kueue.installJob.name | string | `"kueue-obj"` | install job name |
| hw-kueue.installJob.resources.limits.cpu | string | `"100m"` |  |
| hw-kueue.installJob.resources.limits.memory | string | `"250Mi"` |  |
| hw-kueue.installJob.resources.requests.cpu | string | `"100m"` |  |
| hw-kueue.installJob.resources.requests.memory | string | `"250Mi"` |  |
| hw-kueue.installJob.ttlSecondsAfterFinished | string | `nil` | TTL in seconds for the install-kueue-object Job. Overrides global default. |
| hw-kueue.kueue | object | `{"controllerManager":{"featureGates":[{"enabled":false,"name":"TopologyAwareScheduling"}],"imagePullSecrets":[],"livenessProbe":{"failureThreshold":3,"initialDelaySeconds":15,"periodSeconds":20,"successThreshold":1,"timeoutSeconds":1},"manager":{"containerSecurityContext":{"allowPrivilegeEscalation":false,"capabilities":{"drop":["ALL"]}},"image":{"pullPolicy":"Always","repository":"docker.hops.works/registry.k8s.io/kueue/kueue"},"podAnnotations":{},"podSecurityContext":{"runAsNonRoot":true,"seccompProfile":{"type":"RuntimeDefault"}},"resources":{"limits":{"cpu":"2","memory":"512Mi"},"requests":{"cpu":"500m","memory":"512Mi"}}},"podDisruptionBudget":{"enabled":false,"minAvailable":1},"readinessProbe":{"failureThreshold":3,"initialDelaySeconds":5,"periodSeconds":10,"successThreshold":1,"timeoutSeconds":1},"replicas":1,"topologySpreadConstraints":[]},"enableCertManager":false,"enableKueueViz":false,"enablePrometheus":false,"enableVisibilityAPF":false,"enableVisibilityServerAuth":true,"fullnameOverride":"kueue","kubernetesClusterDomain":"cluster.local","metrics":{"prometheusNamespace":"monitoring","serviceMonitor":{"tlsConfig":{"insecureSkipVerify":true}}},"metricsService":{"annotations":{},"ports":[{"name":"metrics","port":8443,"protocol":"TCP","targetPort":8443}],"type":"ClusterIP"},"nameOverride":"kueue","webhookService":{"ipDualStack":{"enabled":false,"ipFamilies":["IPv6","IPv4"],"ipFamilyPolicy":"PreferDualStack"},"ports":[{"port":443,"protocol":"TCP","targetPort":9443}],"type":"ClusterIP"}}` | override kueue values |
| hw-kueue.managerConfig.clientConnection.burst | int | `100` |  |
| hw-kueue.managerConfig.clientConnection.qps | int | `50` |  |
| hw-kueue.managerConfig.controller.groupKindConcurrency."ClusterQueue.kueue.x-k8s.io" | int | `1` |  |
| hw-kueue.managerConfig.controller.groupKindConcurrency."Job.batch" | int | `5` |  |
| hw-kueue.managerConfig.controller.groupKindConcurrency."LocalQueue.kueue.x-k8s.io" | int | `1` |  |
| hw-kueue.managerConfig.controller.groupKindConcurrency."ResourceFlavor.kueue.x-k8s.io" | int | `1` |  |
| hw-kueue.managerConfig.controller.groupKindConcurrency."Workload.kueue.x-k8s.io" | int | `5` |  |
| hw-kueue.managerConfig.controller.groupKindConcurrency.Pod | int | `5` |  |
| hw-kueue.managerConfig.excludedNamespaces\[0\] | string | `"kube-system"` |  |
| hw-kueue.managerConfig.excludedNamespaces\[1\] | string | `"kueue-system"` |  |
| hw-kueue.managerConfig.excludedNamespaces\[2\] | string | `"kyverno"` |  |
| hw-kueue.managerConfig.fairSharing.enable | bool | `true` |  |
| hw-kueue.managerConfig.fairSharing.preemptionStrategies\[0\] | string | `"LessThanOrEqualToFinalShare"` |  |
| hw-kueue.managerConfig.fairSharing.preemptionStrategies\[1\] | string | `"LessThanInitialShare"` |  |
| hw-kueue.managerConfig.health.healthProbeBindAddress | int | `8081` |  |
| hw-kueue.managerConfig.integrations.frameworks\[0\] | string | `"batch/job"` |  |
| hw-kueue.managerConfig.integrations.frameworks\[10\] | string | `"pod"` |  |
| hw-kueue.managerConfig.integrations.frameworks\[11\] | string | `"deployment"` |  |
| hw-kueue.managerConfig.integrations.frameworks\[12\] | string | `"statefulset"` |  |
| hw-kueue.managerConfig.integrations.frameworks\[1\] | string | `"kubeflow.org/mpijob"` |  |
| hw-kueue.managerConfig.integrations.frameworks\[2\] | string | `"ray.io/rayjob"` |  |
| hw-kueue.managerConfig.integrations.frameworks\[3\] | string | `"ray.io/raycluster"` |  |
| hw-kueue.managerConfig.integrations.frameworks\[4\] | string | `"jobset.x-k8s.io/jobset"` |  |
| hw-kueue.managerConfig.integrations.frameworks\[5\] | string | `"kubeflow.org/paddlejob"` |  |
| hw-kueue.managerConfig.integrations.frameworks\[6\] | string | `"kubeflow.org/pytorchjob"` |  |
| hw-kueue.managerConfig.integrations.frameworks\[7\] | string | `"kubeflow.org/tfjob"` |  |
| hw-kueue.managerConfig.integrations.frameworks\[8\] | string | `"kubeflow.org/xgboostjob"` |  |
| hw-kueue.managerConfig.integrations.frameworks\[9\] | string | `"workload.codeflare.dev/appwrapper"` |  |
| hw-kueue.managerConfig.leaderElection.leaderElect | bool | `true` |  |
| hw-kueue.managerConfig.leaderElection.resourceName | string | `"c1f6bfd2.kueue.x-k8s.io"` |  |
| hw-kueue.managerConfig.manageJobsWithoutQueueName | bool | `false` |  |
| hw-kueue.managerConfig.metrics.bindAddress | int | `8443` |  |
| hw-kueue.managerConfig.webhook.port | int | `9443` |  |
| hw-kueue.nameOverride | string | `"kueue"` |  |
| hw-kueue.rbac.clusterqueue.enabled | bool | `true` |  |
| hw-kueue.rbac.cohort.enabled | bool | `true` |  |
| hw-kueue.rbac.localqueue.enabled | bool | `true` |  |
| hw-kueue.rbac.resourceFlavors.enabled | bool | `true` |  |
| hw-kueue.rbac.topologies.enabled | bool | `true` |  |
| hw-kueue.rbac.workload.enabled | bool | `true` |  |
| hw-kueue.resourceFlavours | list | `[{"annotations":{},"labels":{},"name":"default-flavor","spec":{"nodeLabels":{"cloud.provider.com/region":"europe"},"nodeTaints":{},"tolerations":{},"topologyName":"default"}}]` | List of ResourceFlavors |
| hw-kueue.topologies\[0\].levels\[0\].nodeLabel | string | `"cloud.provider.com/region"` |  |
| hw-kueue.topologies\[0\].levels\[1\].nodeLabel | string | `"cloud.provider.com/zone"` |  |
| hw-kueue.topologies\[0\].levels\[2\].nodeLabel | string | `"kubernetes.io/hostname"` |  |
| hw-kueue.topologies\[0\].name | string | `"default"` |  |
| hw-kyverno.hopsworkslib | object | `{}` | override hopsworkslib values |
| hw-kyverno.policies | object | `{"addCertificatesVolume":{"autogenControllers":"DaemonSet,Deployment,Job,StatefulSet","cacertsConfigMap":"ca-pemstore","enabled":false,"envs":[],"extraAnnotations":[],"hopsworksProjectLabelKey":"hopsworks.ai/project","initContainers":{"extraAnnotations":[],"labels":[]},"labels":[{"key":"job-type","value":"check-image-exist"},{"key":"job-type","value":"tag"},{"key":"job-type","value":"list-tags"},{"key":"job-type","value":"docker-build"},{"key":"job-type","value":"delete"},{"key":"job-type","value":"git-command"}],"mountPath":""},"prohibitHostPath":{"enabled":false}}` | Configuration for Hopsworks Kyverno policies and exceptions |
| hw-kyverno.policies.addCertificatesVolume | object | `{"autogenControllers":"DaemonSet,Deployment,Job,StatefulSet","cacertsConfigMap":"ca-pemstore","enabled":false,"envs":[],"extraAnnotations":[],"hopsworksProjectLabelKey":"hopsworks.ai/project","initContainers":{"extraAnnotations":[],"labels":[]},"labels":[{"key":"job-type","value":"check-image-exist"},{"key":"job-type","value":"tag"},{"key":"job-type","value":"list-tags"},{"key":"job-type","value":"docker-build"},{"key":"job-type","value":"delete"},{"key":"job-type","value":"git-command"}],"mountPath":""}` | Configuration to add custom certificates to pods as a mounted volume |
| hw-kyverno.policies.addCertificatesVolume.autogenControllers | string | `"DaemonSet,Deployment,Job,StatefulSet"` | the list of controllers separated by comma to generate the policy for |
| hw-kyverno.policies.addCertificatesVolume.cacertsConfigMap | string | `"ca-pemstore"` | The name of the configmap containing the certificates. The configmap should contains the ca-certificates.crt trusted by the user to replace the whole /etc/ssl/certs. It should also include the root certificate(s) if any defined for OAUTH or LDAP identity providers. Also, if using a hosted object storage with a custom CA, it should includes the java/cacerts to trust that object storage host and that require updating the hopsfs.namenode.jvmOpts = "-Djavax.net.ssl.trustStore=/etc/ssl/certs/my-cacerts -Djavax.net.ssl.trustStorePassword=changeit" and similarly for the hopsfs.datanode.jvmOpts. |
| hw-kyverno.policies.addCertificatesVolume.enabled | bool | `false` | Enable add certificates volume |
| hw-kyverno.policies.addCertificatesVolume.envs | list | `[]` | The array of environment variables with their values that you would like to inject to the pods along side the certificates volume. |
| hw-kyverno.policies.addCertificatesVolume.extraAnnotations | list | `[]` | The array of extra annotations to use when filtering which pods to inject the certificates volume into. |
| hw-kyverno.policies.addCertificatesVolume.hopsworksProjectLabelKey | string | `"hopsworks.ai/project"` | the name of the label key to identify hopsworks user project namespaces |
| hw-kyverno.policies.addCertificatesVolume.initContainers | object | `{"extraAnnotations":[],"labels":[]}` | Opt-in for injecting the certificates volume into init containers. When enabled, a second mutate rule is rendered that targets spec.initContainers and is gated by an OR of the dedicated annotation (default kyverno-inject-certs-init=enabled), extraAnnotations, and labels configured below. Pods must opt in via at least one of these matchers. |
| hw-kyverno.policies.addCertificatesVolume.initContainers.extraAnnotations | list | `[]` | Init-specific extra annotations that opt a pod's init containers into certificate volume injection. ORed with the dedicated init-container annotation and labels below. Defaults to empty so init injection is opt-in by design. |
| hw-kyverno.policies.addCertificatesVolume.initContainers.labels | list | `[]` | Init-specific labels that opt a pod's init containers into certificate volume injection. ORed with the dedicated init-container annotation and extraAnnotations. Defaults to empty so third-party operator-injected init containers are not silently mutated. |
| hw-kyverno.policies.addCertificatesVolume.labels | list | `[{"key":"job-type","value":"check-image-exist"},{"key":"job-type","value":"tag"},{"key":"job-type","value":"list-tags"},{"key":"job-type","value":"docker-build"},{"key":"job-type","value":"delete"},{"key":"job-type","value":"git-command"}]` | The array of labels to use when filtering which pods to inject the certificates volume into. The default list includes job-type=check-image-exist, job-type=tag, job-type=list-tags, job-type=docker-build, job-type=delete for docker operations, that is needed if using a registry with custom CA. The default list also includes job-type=git-command for git operations, that is needed if using a git host with custom CA. |
| hw-kyverno.policies.addCertificatesVolume.mountPath | string | `""` | Path to mount the certificates volume |
| hw-kyverno.policies.prohibitHostPath | object | `{"enabled":false}` | Configuration for disabling hostPath volumes in Pods |
| hw-kyverno.policies.prohibitHostPath.enabled | bool | `false` | Enable hostPath policy and relevant exceptions |
| hw-kyverno.policyExceptions | object | `{"airflow":{"enabled":true},"buildkitd":{"appLabel":"buildkitd","enabled":true,"namePrefix":"buildkitd","rootless":false},"dockerRegistryConfigurer":{"enabled":true},"filebeat":{"enabled":true},"hopsfsCsi":{"enabled":true},"jobs":{"enabled":true},"jupyter":{"enabled":true},"knativeDryRun":{"enabled":true},"opensearch":{"enabled":true},"prometheusNodeExporter":{"enabled":true},"pythonDeployment":{"enabled":true},"pythonapp":{"enabled":true},"rondb":{"enabled":true},"spark":{"enabled":true,"rssAppName":"rss-hops"},"systemJobs":{"enabled":true},"terminal":{"enabled":true},"trino":{"enabled":true},"vllm":{"enabled":true}}` | Configuration for PolicyExceptions to exempt specific services from Kyverno PSS Restricted policies |
| hw-kyverno.policyExceptions.airflow | object | `{"enabled":true}` | PolicyException for the Airflow Deployments. Under the legacy in-container mount (global._hopsworks.csi.enabled=false) Airflow has a mount-airflow-folders sidecar that requires privileged access for FUSE mounting of HopsFS. This exception is enabled by default and only renders when the airflow service and hw-kyverno are enabled AND the CSI integration is off: with hopsfs-csi the Airflow pods are restricted-compliant and need no exemption. |
| hw-kyverno.policyExceptions.airflow.enabled | bool | `true` | Enable PolicyException for airflow-scheduler. Set to false to disable even when airflow service is enabled. |
| hw-kyverno.policyExceptions.buildkitd | object | `{"appLabel":"buildkitd","enabled":true,"namePrefix":"buildkitd","rootless":false}` | PolicyException for the persistent BuildKit daemon (global._hopsworks.buildkitd.enabled). The system-jobs exception matches Jobs by job-type label and so never reaches this StatefulSet, which would then be rejected on a Kyverno cluster. |
| hw-kyverno.policyExceptions.buildkitd.appLabel | string | `"buildkitd"` | Pod label the exception matches, together with the name prefix below. Tracks hopsworks.buildkitd.name, which is what the StatefulSet sets as its app label. |
| hw-kyverno.policyExceptions.buildkitd.enabled | bool | `true` | Enable PolicyException for the persistent BuildKit daemon. Also gated on global._hopsworks.buildkitd.enabled, which is what turns the daemon itself on, so this defaults true without becoming a standing grant: the exception renders only where the daemon does. Turning it off on a Kyverno cluster that runs the daemon gets it rejected at admission, since the exception grants the rootful union (privileged, host namespaces, uid 0). |
| hw-kyverno.policyExceptions.buildkitd.namePrefix | string | `"buildkitd"` | Name prefix the exception matches, so the grant is not reachable by anything that merely wears the app label. StatefulSet pods are <name>-<ordinal>. |
| hw-kyverno.policyExceptions.buildkitd.rootless | bool | `false` | Grant only the policies a rootless daemon needs, dropping the privileged-container and host-namespace exceptions. Defaults false, which grants the union, because a rootful daemon set to true is rejected at admission whereas a rootless daemon set to false merely carries two exceptions it does not use. Set true alongside hopsworks.buildkitd.rootless.enabled. |
| hw-kyverno.policyExceptions.dockerRegistryConfigurer | object | `{"enabled":true}` | PolicyException for docker-registry-configurer DaemonSet. This service requires privileged access, hostPID, hostNetwork, and hostPath to configure container runtimes on nodes. |
| hw-kyverno.policyExceptions.dockerRegistryConfigurer.enabled | bool | `true` | Enable PolicyException for docker-registry-configurer |
| hw-kyverno.policyExceptions.filebeat | object | `{"enabled":true}` | PolicyException for filebeat DaemonSet. Filebeat requires hostNetwork, hostPath volumes, and runs as root to collect logs from all nodes. |
| hw-kyverno.policyExceptions.filebeat.enabled | bool | `true` | Enable PolicyException for filebeat |
| hw-kyverno.policyExceptions.hopsfsCsi | object | `{"enabled":true}` | PolicyException for HopsFS CSI node DaemonSet. The csi-hopsfs-node-plugin container requires privileged access, root user, hostPath volumes and Bidirectional mount propagation to publish mounts via kubelet plugin directories. It adds no capability of its own; privileged already implies them. |
| hw-kyverno.policyExceptions.hopsfsCsi.enabled | bool | `true` | Enable PolicyException for HopsFS CSI node DaemonSet |
| hw-kyverno.policyExceptions.jobs | object | `{"enabled":true}` | PolicyException for user jobs. These pods contain a hopsfsmount sidecar that requires privileged access for FUSE mounting of HopsFS. |
| hw-kyverno.policyExceptions.jobs.enabled | bool | `true` | Enable PolicyException for user jobs |
| hw-kyverno.policyExceptions.jupyter | object | `{"enabled":true}` | PolicyException for Jupyter server deployments. These pods contain a hopsfsmount sidecar that requires privileged access for FUSE mounting of HopsFS. |
| hw-kyverno.policyExceptions.jupyter.enabled | bool | `true` | Enable PolicyException for Jupyter server deployments |
| hw-kyverno.policyExceptions.knativeDryRun | object | `{"enabled":true}` | PolicyException for the throwaway Pod that Knative's webhook dry-run creates to validate a revision's pod spec. It carries no serving labels, so the label-scoped serving exceptions cannot match it, and a hopsfsmount FUSE sidecar makes it fail the restricted policies. |
| hw-kyverno.policyExceptions.knativeDryRun.enabled | bool | `true` | Enable PolicyException for Knative pod-spec dry-run validation |
| hw-kyverno.policyExceptions.opensearch | object | `{"enabled":true}` | PolicyException for opensearch StatefulSet. OpenSearch requires a privileged init container to configure vm.max_map_count kernel parameter. Only needed when olk.opensearch.setVMMaxMapCount is true. |
| hw-kyverno.policyExceptions.opensearch.enabled | bool | `true` | Enable PolicyException for opensearch |
| hw-kyverno.policyExceptions.prometheusNodeExporter | object | `{"enabled":true}` | PolicyException for prometheus-node-exporter DaemonSet. Node exporter requires hostNetwork and hostPath to collect node-level metrics. |
| hw-kyverno.policyExceptions.prometheusNodeExporter.enabled | bool | `true` | Enable PolicyException for prometheus-node-exporter |
| hw-kyverno.policyExceptions.pythonDeployment | object | `{"enabled":true}` | PolicyException for Python (model-server: python) KServe serving deployments. Agent deployments inject a root, privileged hopsfsmount FUSE sidecar (HWORKS-2871) that does not meet the restricted policy requirements. |
| hw-kyverno.policyExceptions.pythonDeployment.enabled | bool | `true` | Enable PolicyException for Python model serving deployments |
| hw-kyverno.policyExceptions.pythonapp | object | `{"enabled":true}` | PolicyException for Python app deployments (custom apps, Streamlit, Gradio). These pods contain a hopsfsmount sidecar that requires privileged access for FUSE mounting of HopsFS. |
| hw-kyverno.policyExceptions.pythonapp.enabled | bool | `true` | Enable PolicyException for Python app deployments |
| hw-kyverno.policyExceptions.rondb | object | `{"enabled":true}` | PolicyException for RonDB mysqlds StatefulSet. Mysqlds uses the SYS_NICE capability for process scheduling priority tuning. Only needed when rondb.rondb.meta.mysqld.addSysNiceCapability is true. |
| hw-kyverno.policyExceptions.rondb.enabled | bool | `true` | Enable PolicyException for RonDB mysqlds |
| hw-kyverno.policyExceptions.spark | object | `{"enabled":true,"rssAppName":"rss-hops"}` | PolicyException for Spark-related resources including: (1) Spark driver and executor pods created by spark-operator - these pods have container-level security contexts but lack pod-level security context support in older spark-operator versions, (2) RSS (Remote Shuffle Service) coordinator and shuffle server Deployments/StatefulSets - these are dynamically created by the Uniffle controller with security contexts configured via CRD spec, and (3) the spark-operator Helm hook Job that applies CRDs on install/upgrade - the upstream chart hardcodes its securityContext without runAsNonRoot/seccompProfile and exposes no values to set them. |
| hw-kyverno.policyExceptions.spark.enabled | bool | `true` | Enable PolicyException for Spark-related resources (spark-operator driver/executor pods, RSS coordinator/shuffle server Deployments/StatefulSets, and the spark-operator CRD upgrade hook Job) |
| hw-kyverno.policyExceptions.spark.rssAppName | string | `"rss-hops"` | The app name of the RemoteShuffleService resource |
| hw-kyverno.policyExceptions.systemJobs | object | `{"enabled":true}` | PolicyException for Hopsworks system jobs including docker operations (docker-build, check-image-exist, tag, delete, list-tags), image validation (check-image), and conda library operations (list-libraries, export-libraries, conda-search-libraries). These jobs require privileged access to run buildkit/podman for building container images. |
| hw-kyverno.policyExceptions.systemJobs.enabled | bool | `true` | Enable PolicyException for Hopsworks system jobs |
| hw-kyverno.policyExceptions.terminal | object | `{"enabled":true}` | PolicyException for terminal server deployments. These pods contain a hopsfsmount sidecar that requires privileged access for FUSE mounting of HopsFS. |
| hw-kyverno.policyExceptions.terminal.enabled | bool | `true` | Enable PolicyException for terminal server deployments |
| hw-kyverno.policyExceptions.trino | object | `{"enabled":true}` | DEPRECATED and read by nothing. Excepted the Trino pods from the restricted policies while their mount sidecars were privileged root containers; they are unprivileged hopsfs-csi sidecars now and pass the policies as-is. Kept only so an override carried from 5.1 still validates. |
| hw-kyverno.policyExceptions.trino.enabled | bool | `true` | Enable PolicyException for trino |
| hw-kyverno.policyExceptions.vllm | object | `{"enabled":true}` | PolicyException for vLLM model serving deployments created by KServe. These pods are deployed with default KServe/vLLM configurations that may not meet all restricted policy requirements. |
| hw-kyverno.policyExceptions.vllm.enabled | bool | `true` | Enable PolicyException for vLLM model serving deployments |
| judge.enabled | bool | `false` |  |
| judge.hopsworkslib | object | `{}` | override hopsworkslib values |
| judge.image.name | string | `"/hopsworks/nginx"` |  |
| judge.image.pullPolicy | string | `"IfNotPresent"` |  |
| judge.image.registry | string | `"test-registry:6000"` |  |
| judge.image.tag | string | `"stable-bookworm"` |  |
| judge.ingress.annotations | object | `{}` | ingress annotations |
| judge.ingress.className | string | `"nginx"` | Name of the class implementing the Ingress controller |
| judge.ingress.host | string | `"judge.hopsworks.ai"` | Rule for host based routing |
| judge.nodeSelector | object | `{}` | This ensures that Kubernetes schedules pods only onto nodes that match all the specified labels. |
| judge.port | int | `8080` | Port Judge will be listening on internally |
| judge.regions.active | string | `"eu"` | Active region identifier |
| judge.regions.replica | string | `"us"` | Replica region identifier |
| judge.replicaCount | int | `1` |  |
| judge.resources.limits.cpu | string | `"10m"` |  |
| judge.resources.limits.memory | string | `"70M"` |  |
| judge.resources.requests.cpu | string | `"5m"` |  |
| judge.resources.requests.memory | string | `"50M"` |  |
| judge.serviceAccount.name | string | `"hopsworks-judge"` |  |
| judge.serviceName | string | `"hopsworks-judge"` |  |
| judge.tolerations | list | `[]` | These tolerations allow Kubernetes to schedule pods on nodes with matching taints, ensuring proper placement based on cluster policies. |
| judge.topologySpreadConstraint | object | `{}` | The default topology spread constraint. If not defined the global topology spread constraint would be used instead. |
| kafka.appName | string | `"kafka"` |  |
| kafka.cleanupOnUninstall | object | `{"enabled":true,"ttlSecondsAfterFinished":null}` | post-delete cleanup of Kafka leftovers. Strimzi's Kafka/Zookeeper StatefulSet PVCs survive uninstall; this deletes them by the strimzi.io/cluster label, but only when global._hopsworks.wipeDataOnUninstall is enabled and never for PVCs labelled hopsworks.ai/keep=true. |
| kafka.cleanupOnUninstall.enabled | bool | `true` | enable the post-delete Kafka data-PVC cleanup hook (also requires global._hopsworks.wipeDataOnUninstall) |
| kafka.cleanupOnUninstall.ttlSecondsAfterFinished | string | `nil` | ttlSecondsAfterFinished for the cleanup Job; null falls through to the global default |
| kafka.cluster.clientsCa.validityDays | int | `365` | Validity in days of the KafkaUser certificates Strimzi issues under the clients CA. Applies at the next issuance; already-issued certificates keep their dates. |
| kafka.cluster.clusterCa.validityDays | int | `365` | Validity in days of the certificates Strimzi issues under the cluster CA (brokers, ZooKeeper, entity operator). Applies at the next issuance; already-issued certificates keep their dates. |
| kafka.cluster.entityOperator | object | `{}` | entity operator configuration for the cluster  |
| kafka.cluster.kafka.authorizer.authorizerClass | string | `"io.hops.kafka.HopsAclAuthorizer"` |  |
| kafka.cluster.kafka.authorizer.principalBuilderClass | string | `"io.hops.kafka.HopsPrincipalBuilder"` |  |
| kafka.cluster.kafka.authorizer.superUsers | list | `[]` |  |
| kafka.cluster.kafka.authorizer.type | string | `"custom"` |  |
| kafka.cluster.kafka.config.database.name | string | `"hopsworks"` |  |
| kafka.cluster.kafka.config.log.retention.bytes | int | `-1` | The maximum size of the log before deleting it. |
| kafka.cluster.kafka.config.log.retention.checkIntervalMs | int | `300000` | The interval at which log segments are checked for deletion. |
| kafka.cluster.kafka.config.log.retention.hours | int | `168` | The number of hours to keep a log segment before deleting it. |
| kafka.cluster.kafka.dependencies.glassfish.consulServiceName | string | `"glassfish"` |  |
| kafka.cluster.kafka.dependencies.glassfish.consulServiceTag | string | `"hopsworks"` |  |
| kafka.cluster.kafka.dependencies.mysql.consulServiceName | string | `"mysql"` |  |
| kafka.cluster.kafka.dependencies.mysql.port | int | `3306` |  |
| kafka.cluster.kafka.dependencies.onlinefs.consulServiceName | string | `"onlinefs"` |  |
| kafka.cluster.kafka.externalLoadBalancer.annotations | object | `{}` | load balancer annotations |
| kafka.cluster.kafka.externalLoadBalancer.class | string | `nil` | load balancer class name |
| kafka.cluster.kafka.externalLoadBalancer.dns | string | `""` | In case of unmanaged Load Balancers this is the advertised host for the brokers |
| kafka.cluster.kafka.externalLoadBalancer.enabled | string | `nil` | Enable External Load Balancers for Kafka cluster. If not set the .global._hopsworks.externalLoadBalancers.enabled will be used instead |
| kafka.cluster.kafka.externalLoadBalancer.finalizers | list | `[]` | A list of finalizers which will be configured for the services created for the external listener. |
| kafka.cluster.kafka.externalLoadBalancer.managed | string | `nil` | Cloud provider provisions Load Balancers. If not set the .global._hopsworks.externalLoadBalancers.managed will be used instead |
| kafka.cluster.kafka.externalLoadBalancer.nodeSelector | object | `{}` | selector for nodes the load balancer can use to route traffic |
| kafka.cluster.kafka.externalLoadBalancer.startingAdvertisedPort | int | `9093` | In case of unmanaged Load Balancers this is the starting advertised port for the brokers   |
| kafka.cluster.kafka.image | object | `{"name":"kafka","tag":"1.2.0-kafka-4.3.1-h1"}` | a tag docker.hops.works does not carry, because only the `-h<N>` builds are published there. So clearing it also means pointing `strimzi-kafka-operator.defaultImageRegistry` at `quay.io` (or mirroring the plain upstream tags), and the same applies to the operator's Kafka Exporter and Cruise Control defaults if those are ever turned on. |
| kafka.cluster.kafka.jvmOptions | object | `{}` | jvm options |
| kafka.cluster.kafka.nodeSelector | object | `{}` | node selector configuration |
| kafka.cluster.kafka.podAntiAffinity.required | bool | `false` |  |
| kafka.cluster.kafka.podSecurityContext | object | `{"fsGroup":1001,"runAsGroup":1001,"runAsNonRoot":true,"runAsUser":1001,"seccompProfile":{"type":"RuntimeDefault"}}` | Pod-level security context for Kafka pods |
| kafka.cluster.kafka.quotas.defaults.consumerByteRate | int | `9223372036854775807` | Deprecated and no longer honoured. |
| kafka.cluster.kafka.quotas.defaults.enabled | bool | `false` | Deprecated and no longer honoured. Use `quotas.kafka.*` with `type: kafka`, or `quotas.strimzi.*` with `type: strimzi`. Fails the render when combined with `type: kafka`; ignored under `type: strimzi`. |
| kafka.cluster.kafka.quotas.defaults.producerByteRate | int | `1048576` | Deprecated and no longer honoured. |
| kafka.cluster.kafka.quotas.defaults.requestPercentage | int | `100` | Deprecated and no longer honoured. |
| kafka.cluster.kafka.quotas.kafka.consumerByteRate | string | `nil` | Built-in plugin only. Default bytes/sec each client may fetch from each broker. Per broker. Unset = none. |
| kafka.cluster.kafka.quotas.kafka.controllerMutationRate | string | `nil` | Built-in plugin only. Default ceiling on partition create/delete mutations per second, per broker. Unset = none. |
| kafka.cluster.kafka.quotas.kafka.producerByteRate | string | `nil` | Built-in plugin only. Default bytes/sec each client may publish to each broker. Per broker. Unset = none. |
| kafka.cluster.kafka.quotas.kafka.requestPercentage | string | `nil` | Built-in plugin only. Default ceiling on each client's CPU use, as a percentage of a broker's network and I/O threads. Unset = none. |
| kafka.cluster.kafka.quotas.minAvailableBytesPerVolume | int | 0 | Strimzi plugin only. Halt producers when available bytes per broker volume falls below this value; 0 = disabled |
| kafka.cluster.kafka.quotas.minAvailableRatioPerVolume | float | `0.01` | Strimzi plugin only. Halt producers when available ratio per broker volume falls below this value (0.0-1.0) |
| kafka.cluster.kafka.quotas.strimzi.consumerByteRate | string | `nil` | Strimzi plugin only. Per-broker consumer byte-rate shared between all non-excluded clients on that broker. Unset = unlimited. |
| kafka.cluster.kafka.quotas.strimzi.excludedPrincipals | list | `[]` | Strimzi plugin only. Principals exempt from the rates above, each prefixed `User:`. Strimzi prepends its own broker and cruise-control principals. A superUser is exempt from ACLs but NOT from quotas, so without an entry here the platform's own clients are throttled by a rate meant for tenants. VERIFY ON THE CLUSTER; do not assume an entry took effect. Strimzi joins this list with ';' and the plugin splits on ';' with no escaping, so a principal whose own name contains ';' cannot be expressed. `authorizer.principalBuilderClass` decides the form: the default Kafka builder yields the certificate DN, which is expressible; this chart's default io.hops.kafka.HopsPrincipalBuilder yields the CN with every differing subject-alternative -name appended and ';'-joined, which is not. The chart fails the render on an entry that lacks the `User:` prefix or contains ';' rather than rendering an exemption that cannot match. Measured on 5.0: onlinefs stayed capped at the configured rate with its entry present. Confirm with kafka-consumer-perf-test.sh. |
| kafka.cluster.kafka.quotas.strimzi.producerByteRate | string | `nil` | Strimzi plugin only. Per-broker producer byte-rate shared between all non-excluded clients on that broker. Unset = unlimited. |
| kafka.cluster.kafka.quotas.type | string | `"strimzi"` | Quota plugin: "strimzi" or "kafka". "strimzi" installs Strimzi's StaticQuotaCallback - a storage guard plus per-broker rates shared between clients, with an exclusion list. "kafka" leaves Kafka's built-in plugin in place - per-user, per-broker limits resolved from config entities, and the only mode in which a KafkaUser's spec.quotas is enforced. Enabling one disables the other. |
| kafka.cluster.kafka.quotas.window.num | int | `11` | Applies under both plugins. Number of samples retained for the quota rate calculation. |
| kafka.cluster.kafka.quotas.window.sizeSeconds | int | `1` | Applies under both plugins. Duration of each quota sample window in seconds. |
| kafka.cluster.kafka.replicas | int | `1` |  |
| kafka.cluster.kafka.resources | object | `{}` | Resources of the broker pods. Applied through the broker KafkaNodePool; the v1 Kafka API has no spec.kafka.resources. |
| kafka.cluster.kafka.securityContext | object | `{"allowPrivilegeEscalation":false,"capabilities":{"drop":["ALL"]},"runAsGroup":1001,"runAsNonRoot":true,"runAsUser":1001,"seccompProfile":{"type":"RuntimeDefault"}}` | Container-level security context for Kafka containers |
| kafka.cluster.kafka.services.brokers.annotations."consul.hashicorp.com/service-name" | string | `"kafka"` |  |
| kafka.cluster.kafka.services.brokers.annotations."consul.hashicorp.com/service-port" | int | `9092` |  |
| kafka.cluster.kafka.services.brokers.annotations."consul.hashicorp.com/service-tags" | string | `"broker"` |  |
| kafka.cluster.kafka.services.pods.annotations."prometheus.io/path" | string | `"/metrics"` |  |
| kafka.cluster.kafka.services.pods.annotations."prometheus.io/port" | int | `9404` |  |
| kafka.cluster.kafka.services.pods.annotations."prometheus.io/scheme" | string | `"http"` |  |
| kafka.cluster.kafka.services.pods.annotations."prometheus.io/scrape" | string | `"true"` |  |
| kafka.cluster.kafka.storageClassName | string | `nil` | storage class name |
| kafka.cluster.kafka.storageSize | string | `"30Gi"` |  |
| kafka.cluster.kafka.tolerations | list | `[]` |  |
| kafka.cluster.kafka.topologySpreadConstraint | object | `{}` | The default topology spread constraint. If not defined the global topology spread constraint would be used instead. |
| kafka.cluster.kafka.version | string | `"4.3.1"` |  |
| kafka.cluster.name | string | `"kafka-cluster"` |  |
| kafka.cluster.tlscerts.annotations."certs.hopsworks.ai/owned-by" | string | `"deployment-strimzi-cluster-operator"` |  |
| kafka.cluster.zookeeper | object | `{"nodeSelector":{},"podAntiAffinity":{"required":false},"podSecurityContext":{"fsGroup":1001,"runAsGroup":1001,"runAsNonRoot":true,"runAsUser":1001,"seccompProfile":{"type":"RuntimeDefault"}},"replicas":1,"resources":{"limits":{"cpu":"2","memory":"3Gi"},"requests":{"cpu":"200m","memory":"1Gi"}},"securityContext":{"allowPrivilegeEscalation":false,"capabilities":{"drop":["ALL"]},"runAsGroup":1001,"runAsNonRoot":true,"runAsUser":1001,"seccompProfile":{"type":"RuntimeDefault"}},"services":{"client":{"annotations":{"consul.hashicorp.com/service-name":"zookeeper","consul.hashicorp.com/service-tags":"client"}}},"storageClassName":null,"storageSize":"5Gi","tolerations":[],"topologySpreadConstraint":{}}` | Sizing and scheduling for the KRaft **controller pool**, despite the name. No ZooKeeper ensemble is deployed any more - Strimzi 1.x has no `.spec.zookeeper` - but controllers replace that ensemble one-for-one, so `kafka.controllerConfig` keeps reading these values: a 3-node quorum stays a 3-node quorum with the same storage, resources, scheduling and security context, and no values change is needed. The key keeps its name because renaming it would break every existing values file. |
| kafka.cluster.zookeeper.nodeSelector | object | `{}` | node selector configuration |
| kafka.cluster.zookeeper.podSecurityContext | object | `{"fsGroup":1001,"runAsGroup":1001,"runAsNonRoot":true,"runAsUser":1001,"seccompProfile":{"type":"RuntimeDefault"}}` | Pod-level security context for Zookeeper pods |
| kafka.cluster.zookeeper.resources | object | `{"limits":{"cpu":"2","memory":"3Gi"},"requests":{"cpu":"200m","memory":"1Gi"}}` | resources configuration |
| kafka.cluster.zookeeper.securityContext | object | `{"allowPrivilegeEscalation":false,"capabilities":{"drop":["ALL"]},"runAsGroup":1001,"runAsNonRoot":true,"runAsUser":1001,"seccompProfile":{"type":"RuntimeDefault"}}` | Container-level security context for Zookeeper containers |
| kafka.cluster.zookeeper.storageClassName | string | `nil` | storage class name |
| kafka.cluster.zookeeper.topologySpreadConstraint | object | `{}` | The default topology spread constraint. If not defined the global topology spread constraint would be used instead. |
| kafka.configmap.name | string | `"kafka-configmap"` |  |
| kafka.crdUpgradeJob.enabled | bool | `true` | Run the Job that keeps the Strimzi CRDs in step with the operator this chart deploys, and preflights the KRaft migration. It runs pre-install and pre-upgrade: Helm applies the operator subchart's `crds/` on install only and skips any CRD that already exists, so every other path goes through here. A cluster whose objects are still stored as `v1beta2` is converted first (through the 0.51.0 bundle in `image`), which leaves both API versions served until the next upgrade renders `v1` and finishes the move to the 1.2.0 bundle. A failed *refresh* is not fatal by itself - it repairs rather than gates, so a failed apply warns and lets the upgrade continue - but the Job then refuses the upgrade when the live CRDs are too old for the Kafka resource this chart renders. The preflight checks are fatal: they only fire on states that would corrupt or roll back a cluster. |
| kafka.crdUpgradeJob.image | object | `{"name":"crds","tag":"1.2.0-h1"}` | Image carrying the CRD bundles the Job applies: `strimzi-crds-<version>.yaml` for the Strimzi version this chart depends on, and the 0.51.0 bundle a cluster still storing `v1beta2` is converted through (Kubernetes refuses to drop a version still listed in a CRD's `status.storedVersions`, and 0.51.0 is the last Strimzi release to serve both). Built by `strimzi-crds` in the docker-images repo and pulled from the operator's `defaultImageRegistry`/`defaultImageRepository` like the broker image, so an airgapped install mirrors it with the rest (`vendor_images.sh` includes it). The tag's Strimzi part must match the dependency version: the Job refuses the upgrade when the bundle it needs is not in the image. |
| kafka.crdUpgradeJob.name | string | `"strimzi-crd-upgrade"` |  |
| kafka.crdUpgradeJob.nodeSelector | object | `{}` | node selector configuration |
| kafka.crdUpgradeJob.resources | object | `{"limits":{"cpu":"500m","memory":"512Mi"},"requests":{"cpu":"100m","memory":"128Mi"}}` | resources configuration. Both halves are set deliberately: a namespace LimitRange defaults per resource, so a container that declares only requests still has limits injected - at whatever the operator's default is, which is high enough on some clusters to exhaust a ResourceQuota or stop the pod scheduling outright. The Job runs kubectl over about 1 MB of CRD YAML, so it is sized like the `tool` tier of hopsworkslib.initContainerResources. |
| kafka.crdUpgradeJob.serviceAccount.annotations | object | `{}` | service account annotations |
| kafka.crdUpgradeJob.tolerations | list | `[]` |  |
| kafka.crdUpgradeJob.ttlSecondsAfterFinished | string | `nil` | ttlSecondsAfterFinished for the Job; null falls through to the global default |
| kafka.hopsworkslib | object | `{}` | override hopsworkslib values |
| kafka.metrics.configMapKey | string | `"kafka-metrics-config"` |  |
| kafka.metrics.enabled | bool | `true` |  |
| kafka.metrics.type | string | `"jmxPrometheusExporter"` |  |
| kafka.migrationJob.enabled | bool | `true` | Run the pre-upgrade Job that carries a ZooKeeper-based cluster to KRaft before the rest of the upgrade is applied. It exits immediately on a cluster that is already on KRaft, so leaving it on costs one short Job per upgrade. Turning it off on a cluster that still needs migrating does not make the upgrade work - it makes it fail later, in the preflight, because the Strimzi this chart ships cannot serve a ZooKeeper cluster at all. |
| kafka.migrationJob.name | string | `"kafka-kraft-migration"` |  |
| kafka.migrationJob.nodeSelector | object | `{}` | node selector configuration |
| kafka.migrationJob.resources | object | `{"limits":{"cpu":"500m","memory":"512Mi"},"requests":{"cpu":"100m","memory":"128Mi"}}` | resources configuration. Requests and limits both set, for the reason given on `crdUpgradeJob.resources`. This one only polls kubectl in a sleep loop. |
| kafka.migrationJob.serviceAccount.annotations | object | `{}` | service account annotations |
| kafka.migrationJob.timeoutSeconds | int | `1800` | How long to wait, in seconds, for Strimzi to reach KRaftPostMigration and then KRaft. Each wait gets this budget separately. On timeout the Job fails and so does the upgrade, but the cluster is not stranded: the operator keeps migrating regardless of this Job, so the next upgrade picks up wherever it got to. |
| kafka.migrationJob.tolerations | list | `[]` |  |
| kafka.migrationJob.ttlSecondsAfterFinished | string | `nil` | ttlSecondsAfterFinished for the Job; null falls through to the global default |
| kafka.strimzi-kafka-operator | object | `{"createGlobalResources":true,"defaultImageRegistry":"docker.hops.works","defaultImageRepository":"strimzi","defaultImageTag":"1.2.0","enabled":true,"extraEnvs":[{"name":"HOPSWORKS_FIRST_STRIMZICA_CA_CERT","valueFrom":{"secretKeyRef":{"key":"ca.crt","name":"kafka-cluster-cluster-ca-cert"}}},{"name":"HOPSWORKS_FIRST_STRIMZICA_CLIENT_CERT","valueFrom":{"secretKeyRef":{"key":"ca.crt","name":"kafka-cluster-clients-ca-cert"}}},{"name":"HOPSWORKS_FIRST_STRIMZICA_CLIENT_CA","valueFrom":{"secretKeyRef":{"key":"ca.key","name":"kafka-cluster-clients-ca"}}},{"name":"HOPSWORKS_FIRST_STRIMZICA_CA","valueFrom":{"secretKeyRef":{"key":"ca.key","name":"kafka-cluster-cluster-ca"}}}],"nodeSelector":{},"podSecurityContext":{"fsGroup":1000,"runAsGroup":1000,"runAsNonRoot":true,"runAsUser":1000,"seccompProfile":{"type":"RuntimeDefault"}},"securityContext":{"allowPrivilegeEscalation":false,"capabilities":{"drop":["ALL"]},"runAsGroup":1000,"runAsNonRoot":true,"runAsUser":1000,"seccompProfile":{"type":"RuntimeDefault"}},"tolerations":[],"watchAnyNamespace":false}` | override values for strimzi operator |
| kafka.topics | list | `[]` | A list of topics to provision in the Kafka cluster. |
| kafka.users | list | `[]` | A list of user to provision in the Kafka cluster. |
| kserve.activator.minReplicas | int | `1` |  |
| kserve.activator.podDisruptionBudget.enabled | bool | `true` |  |
| kserve.activator.podDisruptionBudget.minAvailable | int | `1` |  |
| kserve.activator.serviceAccount.annotations | object | `{}` | service account annotations |
| kserve.cainjector.serviceAccount.annotations | object | `{}` | service account annotations |
| kserve.cert_manager.enabled | bool | `true` |  |
| kserve.cert_manager.jobResources.cainjector | object | `{"limits":{"cpu":"200m"}}` | cainjector resources configuration |
| kserve.cert_manager.jobResources.cainjector.limits | object | `{"cpu":"200m"}` | cainjector resources limits configuration |
| kserve.cert_manager.jobResources.controller | object | `{"limits":{"cpu":"500m","memory":"2Gi"}}` | controller resources configuration |
| kserve.cert_manager.jobResources.webhook | object | `{"limits":{"cpu":"200m"}}` | webhook resources configuration |
| kserve.cert_manager.jobResources.webhook.limits | object | `{"cpu":"200m"}` | webhook resources limits configuration |
| kserve.cert_manager.nodeSelector | object | `{}` | node selector configuration |
| kserve.cert_manager.tolerations | list | `[]` |  |
| kserve.cert_manager.topologySpreadConstraint | object | `{}` | The default topology spread constraint. If not defined the global topology spread constraint would be used instead. |
| kserve.cert_manager.version | string | `"v1.21.1"` | cert-manager version. v1.21 is the line whose supported Kubernetes range (1.33-1.36) covers this chart's kubeVersion window (1.34-1.36); kserve-deps.env pins v1.17 (KServe CI), which is EOL and tops out at Kubernetes 1.33. |
| kserve.cleanupOnUninstall | object | `{"enabled":true,"ttlSecondsAfterFinished":null}` | post-delete cleanup of Istio/KServe leftovers (cert-manager-issued webhook cert Secrets, plus the istiod CA Secret and CA/leader-election ConfigMaps) that are created at runtime and so are never tracked or pruned by Helm/ArgoCD. |
| kserve.cleanupOnUninstall.enabled | bool | `true` | enable the post-delete Istio/KServe cleanup hook |
| kserve.cleanupOnUninstall.ttlSecondsAfterFinished | string | `nil` | ttlSecondsAfterFinished for the cleanup Job; null falls through to the global default |
| kserve.crdUpgradeJob.name | string | `"kserve-crd-upgrade"` |  |
| kserve.crdUpgradeJob.nodeSelector | object | `{}` | node selector configuration |
| kserve.crdUpgradeJob.resources | object | `{"requests":{"cpu":"100m","memory":"128Mi"}}` | resources configuration |
| kserve.crdUpgradeJob.serviceAccount.annotations | object | `{}` | service account annotations |
| kserve.crdUpgradeJob.tolerations | list | `[]` |  |
| kserve.dependencies.hopsworks.consulServiceName | string | `"glassfish"` |  |
| kserve.dependencies.hopsworks.consulServiceTag | string | `"hopsworks"` |  |
| kserve.dependencies.hopsworks.port | int | `8182` |  |
| kserve.dependencies.registry.consulServiceName | string | `"registry"` |  |
| kserve.dependencies.registry.port | int | `30443` |  |
| kserve.dependencies.registry.registryProtocol | string | `"https"` |  |
| kserve.hopsworkslib | object | `{}` | override hopsworkslib values |
| kserve.inferenceLogger.capabilities | object | `{}` | Map of verified full image references with digests to protocol tokens. Empty keeps legacy transport. |
| kserve.inferenceLogger.digest | string | `""` | Immutable sha256 digest. When set, takes precedence over tag. |
| kserve.inferenceLogger.image | string | `"hopsworks/inference-logger"` |  |
| kserve.inferenceLogger.limits.assemblyWorkers | int | `2` |  |
| kserve.inferenceLogger.limits.maxBatchRows | int | `512` |  |
| kserve.inferenceLogger.limits.maxBufferBytes | int | `134217728` |  |
| kserve.inferenceLogger.limits.maxDecodedBytes | int | `33554432` |  |
| kserve.inferenceLogger.limits.maxEventBytes | int | `8388608` |  |
| kserve.inferenceLogger.limits.maxInflightEvents | int | `16` |  |
| kserve.inferenceLogger.limits.maxQueuedRows | int | `1000` |  |
| kserve.inferenceLogger.limits.producerWorkers | int | `2` |  |
| kserve.inferenceLogger.limits.shutdownSeconds | int | `15` |  |
| kserve.inferenceLogger.metrics.additionalLabels | object | `{}` |  |
| kserve.inferenceLogger.metrics.enabled | bool | `false` | Create a PodMonitor when its CRD is available. KServe's existing scrape configuration is preserved. |
| kserve.inferenceLogger.metrics.interval | string | `"30s"` |  |
| kserve.inferenceLogger.metrics.port | int | `9098` |  |
| kserve.inferenceLogger.resources.limits.cpu | string | `"1"` |  |
| kserve.inferenceLogger.resources.limits.memory | string | `"1Gi"` |  |
| kserve.inferenceLogger.resources.requests.cpu | string | `"0.1"` |  |
| kserve.inferenceLogger.resources.requests.memory | string | `"128Mi"` |  |
| kserve.inferenceLogger.tag | string | `"5.2.0-SNAPSHOT"` |  |
| kserve.istio.crdClassInstallServiceAccount.apiGroups\[0\] | string | `"networking.istio.io"` |  |
| kserve.istio.crdClassInstallServiceAccount.apiGroups\[1\] | string | `"security.istio.io"` |  |
| kserve.istio.crdClassInstallServiceAccount.apiGroups\[2\] | string | `"rbac.istio.io"` |  |
| kserve.istio.crdClassInstallServiceAccount.apiGroups\[3\] | string | `"authentication.istio.io"` |  |
| kserve.istio.crdClassInstallServiceAccount.name | string | `"istio-crd-class-install-sa"` |  |
| kserve.istio.crdClassInstallServiceAccount.resources\[0\] | string | `"*"` |  |
| kserve.istio.crdClassInstallServiceAccount.verbs\[0\] | string | `"get"` |  |
| kserve.istio.crdClassInstallServiceAccount.verbs\[1\] | string | `"list"` |  |
| kserve.istio.crdClassInstallServiceAccount.verbs\[2\] | string | `"watch"` |  |
| kserve.istio.crdClassInstallServiceAccount.verbs\[3\] | string | `"create"` |  |
| kserve.istio.crdClassInstallServiceAccount.verbs\[4\] | string | `"update"` |  |
| kserve.istio.crdClassInstallServiceAccount.verbs\[5\] | string | `"patch"` |  |
| kserve.istio.crdClassInstallServiceAccount.verbs\[6\] | string | `"delete"` |  |
| kserve.istio.envoyFilter.corsAllowedOrigins | list | `["https://hopsworks.ai.local"]` | List of allowed origins for CORS requests. Defaults to the hopsworks ingress host. Update this when changing hopsworks.ingress.host. An empty list disables adding CORS headers (no CORS configuration will be applied). CORS responses for the listed origins are configured to allow credentials by default. Use \["*"\] to allow all origins (not recommended with credentials). |
| kserve.istio.envoyFilter.jobName | string | `"envoyfilterjob"` |  |
| kserve.istio.envoyFilter.resources | object | `{"limits":{"cpu":"200m"}}` | resources configuration |
| kserve.istio.envoyFilter.resources.limits | object | `{"cpu":"200m"}` | resources limits configuration |
| kserve.istio.gateways.clusterLocal.podDisruptionBudget.enabled | bool | `true` |  |
| kserve.istio.gateways.clusterLocal.podDisruptionBudget.minAvailable | int | `1` |  |
| kserve.istio.gateways.clusterLocal.replicaCount | int | `1` |  |
| kserve.istio.gateways.http10 | bool | `false` | Deprecated, use gateways.ingress.http10 instead. Still honoured: HTTP/1.0 is enabled when either this or gateways.ingress.http10 is true. |
| kserve.istio.gateways.ingress.http10 | bool | `false` | Allow HTTP/1.0 requests through the ingress gateway |
| kserve.istio.gateways.ingress.http2Port | int | `32080` |  |
| kserve.istio.gateways.ingress.httpsPort | int | `32443` |  |
| kserve.istio.gateways.ingress.name | string | `"istio-ingressgateway"` |  |
| kserve.istio.gateways.ingress.podDisruptionBudget.enabled | bool | `true` |  |
| kserve.istio.gateways.ingress.podDisruptionBudget.minAvailable | int | `1` |  |
| kserve.istio.gateways.ingress.replicaCount | int | `1` |  |
| kserve.istio.gateways.ingress.statusPort | int | `32021` |  |
| kserve.istio.gateways.jobName | string | `"gateway-operator-job"` |  |
| kserve.istio.gateways.operatorConfigFileName | string | `"istiooperator.yaml"` |  |
| kserve.istio.gateways.operatorConfigMountPath | string | `"/tmp"` |  |
| kserve.istio.ingressClass.enabled | bool | `true` | Whether to create a cluster-scoped `IngressClass` named after `name` below, for KServe Standard-mode InferenceServices (`serving.kserve.io/deploymentMode: Standard`). KServe's controller writes this class name into the `spec.ingressClassName` of the `networking.k8s.io/v1` Ingress objects it creates for those InferenceServices. |
| kserve.istio.ingressClass.name | string | `"istio"` | Name of the IngressClass. Must match `kserve.controller.gateway.ingressGateway.className`, which is what KServe reads from the `inferenceservice-config` ConfigMap to populate `spec.ingressClassName`. |
| kserve.istio.istioctl.currentVersion | string | `"1.29.7"` |  |
| kserve.istio.istioctl.installJobName | string | `"istioctl-install-job"` |  |
| kserve.istio.istioctl.jobRetries | int | `4` |  |
| kserve.istio.istioctl.name | string | `"istioctl"` |  |
| kserve.istio.istioctl.readinessTimeout | string | `"15m0s"` |  |
| kserve.istio.istioctl.resources | object | `{"requests":{"cpu":"200m","memory":"256Mi"}}` | resources configuration |
| kserve.istio.istioctl.serviceAccount.annotations | object | `{}` | service account annotations |
| kserve.istio.istioctl.targetVersion | string | `"1.29.7"` |  |
| kserve.istio.istioctl.uninstallJobName | string | `"istioctl-uninstall-job"` |  |
| kserve.istio.nodeSelector | object | `{}` | node selector configuration |
| kserve.istio.pilot.podDisruptionBudget.enabled | bool | `true` |  |
| kserve.istio.pilot.podDisruptionBudget.minAvailable | int | `1` |  |
| kserve.istio.pilot.replicaCount | int | `1` |  |
| kserve.istio.tolerations | list | `[]` |  |
| kserve.istioCRD.serviceAccount.annotations | object | `{}` | service account annotations |
| kserve.knative.autoscaler.scaleToZeroGracePeriod | string | `"30s"` |  |
| kserve.knative.autoscaler.scaleToZeroPodRetentionPeriod | string | `"0s"` |  |
| kserve.knative.configFeatures.affinity | string | `"enabled"` |  |
| kserve.knative.configFeatures.emptyDir | string | `"enabled"` |  |
| kserve.knative.configFeatures.initContainers | string | `"enabled"` |  |
| kserve.knative.configFeatures.nodeSelectors | string | `"enabled"` |  |
| kserve.knative.configFeatures.priorityClassName | string | `"enabled"` |  |
| kserve.knative.configFeatures.securePodDefaults | string | `"disabled"` | Knative "secure-pod-defaults" feature flag. Keep "disabled" so the HopsFS FUSE sidecar (runs as root/privileged) keeps working once Knative flips its built-in default from "disabled" to "AllowRootBounded" (planned ~1.22). Possible values are "disabled", "AllowRootBounded" or "enabled". |
| kserve.knative.configFeatures.securityContext | string | `"enabled"` |  |
| kserve.knative.configFeatures.tolerations | string | `"enabled"` |  |
| kserve.knative.configFeatures.volumesCsi | string | `"enabled"` | Knative "kubernetes.podspec-volumes-csi" feature gate, "disabled" by default in Knative. With the HopsFS CSI driver on (csi_driver_enabled), the backend gives Knative-mode agent and Python deployments the same inline csi: HopsFS volume plus unprivileged hopsfs-fuse sidecar that Jupyter, jobs, terminals and RawDeployment serving use, instead of the legacy root and privileged hopsfsmount container (HWORKS-3312). Knative's Revision validation only lets a csi: volume source through when this gate is enabled; with it disabled those deployments are rejected at admission. Possible values are "disabled" or "enabled". |
| kserve.knative.configFeatures.volumesMountPropagation | string | `"enabled"` | Knative "kubernetes.podspec-volumes-mount-propagation" feature gate. The gate does not exist in Knative 1.13 (there was nothing to set) and defaults to "disabled" in 1.21. No Hopsworks serving path depends on it: the backend omits mountPropagation from InferenceService containers and the model-serving-webhook injects HostToContainer onto the pod, after Knative admission. It is enabled purely as headroom, so that an InferenceService carrying a permitted mountPropagation is not rejected. It does not rescue a spec written by a pre-upgrade backend: those set Bidirectional on the HopsFS mount plus privileged on the sidecar, and Knative rejects both however this gate is set (it accepts only None and HostToContainer). Possible values are "disabled" or "enabled". |
| kserve.knative.deployment.progressDeadline | string | `"1800s"` |  |
| kserve.knative.domainName | string | `"hopsworks.ai"` |  |
| kserve.knative.gateways.jobName | string | `"knative-gateways-job"` |  |
| kserve.knative.gateways.resources | object | `{"limits":{"cpu":"400m"}}` | resources configuration |
| kserve.knative.gateways.resources.limits | object | `{"cpu":"400m"}` | resources limits configuration |
| kserve.knative.http.enabled | bool | `true` |  |
| kserve.knative.https.credentialsName | string | `""` |  |
| kserve.knative.https.enabled | bool | `false` |  |
| kserve.knative.imageRegistry | string | `""` | Registry prefix for the seven upstream Knative images (serving controller, activator, autoscaler, webhook, queue; net-istio controller, webhook), which the chart references as <registry>/gcr.io/knative-releases/knative.dev/<component>:<version>. Empty means global._hopsworks.imageRegistry. Set it to pull a staged Knative build from another path without moving every other image, the same way servingruntime.*.imageRegistry does. |
| kserve.knative.initialDelaySeconds | int | `180` |  |
| kserve.knative.netIstioController.resources.limits.cpu | string | `"300m"` |  |
| kserve.knative.netIstioController.resources.limits.memory | string | `"400Mi"` |  |
| kserve.knative.netIstioController.resources.requests.cpu | string | `"30m"` |  |
| kserve.knative.netIstioController.resources.requests.memory | string | `"40Mi"` |  |
| kserve.knative.nodeSelector | object | `{}` | node selector configuration |
| kserve.knative.peerAuthenticationsJob.name | string | `"knative-serving-peer-authentications-job"` |  |
| kserve.knative.peerAuthenticationsJob.resources | object | `{}` | resources configuration |
| kserve.knative.queueSidecarImage.name | string | `"kserve/qpext"` |  |
| kserve.knative.queueSidecarImage.tag | string | `"v0.21.0"` |  |
| kserve.knative.registryCertMount.certFileName | string | `"ca.crt"` |  |
| kserve.knative.registryCertMount.external | bool | `false` |  |
| kserve.knative.registryCertMount.mountDir | string | `"/etc/registry_certs"` |  |
| kserve.knative.registryCertMount.volumeName | string | `"registry-certs"` |  |
| kserve.knative.serviceAccount.annotations | object | `{}` | service account annotations |
| kserve.knative.serviceAnnotations."prometheus.io/path" | string | `"/metrics"` |  |
| kserve.knative.serviceAnnotations."prometheus.io/port" | int | `9090` |  |
| kserve.knative.serviceAnnotations."prometheus.io/scheme" | string | `"http"` |  |
| kserve.knative.serviceAnnotations."prometheus.io/scrape" | string | `"true"` |  |
| kserve.knative.tolerations | list | `[]` |  |
| kserve.knative.topologySpreadConstraint | object | `{}` | The default topology spread constraint. If not defined the global topology spread constraint would be used instead. |
| kserve.knative.validatingWebhookDeleteJobName | string | `"knative-serving-validating-webhook-delete-job"` |  |
| kserve.knative.validatingWebhookName | string | `"validation.webhook.serving.knative.dev"` |  |
| kserve.knative.version | string | `"v1.23.0"` |  |
| kserve.kserve.agent.image | string | `"kserve/agent"` |  |
| kserve.kserve.agent.tag | string | `"v0.21.0"` |  |
| kserve.kserve.controller.affinity | object | `{}` | A Kubernetes Affinity, if required. For more information, see [Affinity v1 core](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#affinity-v1-core).  For example:   affinity:     nodeAffinity:      requiredDuringSchedulingIgnoredDuringExecution:        nodeSelectorTerms:        - matchExpressions:          - key: foo.bar.com/role            operator: In            values:            - master |
| kserve.kserve.controller.annotations | object | `{}` | Optional additional annotations to add to the controller deployment. |
| kserve.kserve.controller.containerSecurityContext | object | `{"allowPrivilegeEscalation":false,"capabilities":{"drop":["ALL"]},"privileged":false,"readOnlyRootFilesystem":true,"runAsNonRoot":true,"seccompProfile":{"type":"RuntimeDefault"}}` | Container Security Context to be set on the controller component container. For more information, see [Configure a Security Context for a Pod or Container](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/). |
| kserve.kserve.controller.deploymentMode | string | `"Knative"` | KServe deployment mode: "Knative" (formerly "Serverless"), "Standard" (formerly "RawDeployment"). |
| kserve.kserve.controller.gateway.additionalIngressDomains | list | `[]` | Optional additional domains for ingress routing. |
| kserve.kserve.controller.gateway.disableIngressCreation | bool | `false` | Whether to disable ingress creation for RawDeployment mode. |
| kserve.kserve.controller.gateway.disableIstioVirtualHost | bool | `false` | DisableIstioVirtualHost controls whether to use istio as network layer for top level component routing or path based routing. This configuration is only applicable for Serverless mode, when disabled Istio is no longer required. |
| kserve.kserve.controller.gateway.domain | string | `""` | Ingress domain for RawDeployment mode, for Serverless it is configured in Knative. Empty falls back to `knative.domainName` so Standard-mode InferenceService hosts match Knative-mode hosts. If set explicitly it must stay aligned with `knative.domainName`: the gateway's authority rewrite and the model-serving authenticator only know that domain. |
| kserve.kserve.controller.gateway.domainTemplate | string | `"{{ .Name }}.{{ .Namespace }}.{{ .IngressDomain }}"` | Ingress domain template for RawDeployment mode, for Serverless mode it is configured in Knative. Dot-separated to match the `<name>.<namespace>.<domain>` host format Knative-mode uses. |
| kserve.kserve.controller.gateway.ingressGateway.className | string | `"istio"` |  |
| kserve.kserve.controller.gateway.ingressGateway.enableGatewayApi | bool | `false` | Whether to use the Gateway API for ingress routing instead of Kubernetes Ingress. Kept false for the Knative + Istio network layer. |
| kserve.kserve.controller.gateway.ingressGateway.gateway | string | `"knative-ingress-gateway"` |  |
| kserve.kserve.controller.gateway.localGateway.gateway | string | `"knative-local-gateway"` | localGateway specifies the gateway which handles the network traffic within the cluster. |
| kserve.kserve.controller.gateway.localGateway.gatewayService | string | `"knative-local-gateway"` | localGatewayService specifies the hostname of the local gateway service. |
| kserve.kserve.controller.gateway.localGateway.knativeGatewayService | string | `""` | knativeLocalGatewayService specifies the hostname of the Knative's local gateway service. When unset, the value of "localGatewayService" will be used. When enabling strict mTLS in Istio, KServe local gateway should be created and pointed to the Knative local gateway. |
| kserve.kserve.controller.gateway.urlScheme | string | `"http"` | HTTP endpoint url scheme. |
| kserve.kserve.controller.image | string | `"kserve/kserve-controller"` | KServe controller container image name. Mirrored from upstream kserve/kserve-controller (the Hopsworks idempotency patch is upstream as of 0.19, so the controller is no longer built from the fork). |
| kserve.kserve.controller.knativeAddressableResolver | object | `{"enabled":false}` | Indicates whether to create an addressable resolver ClusterRole for Knative Eventing. This ClusterRole grants the necessary permissions for the Knative's DomainMapping reconciler to resolve InferenceService addressables. |
| kserve.kserve.controller.labels | object | `{}` | Optional additional labels to add to the controller deployment. |
| kserve.kserve.controller.nodeSelector | object | `{}` | The nodeSelector on Pods tells Kubernetes to schedule Pods on the nodes with matching labels. For more information, see [Assigning Pods to Nodes](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/).  |
| kserve.kserve.controller.podAnnotations | object | `{}` | Optional additional labels to add to the controller Pods. |
| kserve.kserve.controller.podDisruptionBudget.enabled | bool | `true` |  |
| kserve.kserve.controller.podDisruptionBudget.minAvailable | int | `1` |  |
| kserve.kserve.controller.podLabels | object | `{}` | Optional additional labels to add to the controller Pods. |
| kserve.kserve.controller.rbacProxy.resources.limits.cpu | string | `"100m"` |  |
| kserve.kserve.controller.rbacProxy.resources.limits.memory | string | `"300Mi"` |  |
| kserve.kserve.controller.rbacProxy.resources.requests.cpu | string | `"100m"` |  |
| kserve.kserve.controller.rbacProxy.resources.requests.memory | string | `"300Mi"` |  |
| kserve.kserve.controller.rbacProxy.securityContext | object | `{"allowPrivilegeEscalation":false,"capabilities":{"drop":["ALL"]},"privileged":false,"readOnlyRootFilesystem":true,"runAsNonRoot":true,"seccompProfile":{"type":"RuntimeDefault"}}` | security context configuration |
| kserve.kserve.controller.rbacProxyImage | string | `"quay.io/brancz/kube-rbac-proxy:v0.18.0"` | KServe controller manager rbac proxy container image |
| kserve.kserve.controller.replicaCount | int | `1` |  |
| kserve.kserve.controller.resources | object | `{"limits":{"cpu":"100m","memory":"300Mi"},"requests":{"cpu":"100m","memory":"300Mi"}}` | Resources to provide to the kserve controller pod.  For example:  requests:    cpu: 10m    memory: 32Mi  For more information, see [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/). |
| kserve.kserve.controller.securityContext | object | `{"runAsNonRoot":true,"seccompProfile":{"type":"RuntimeDefault"}}` | Pod Security Context. For more information, see [Configure a Security Context for a Pod or Container](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/). |
| kserve.kserve.controller.serviceAccount.annotations | object | `{}` | service account annotations |
| kserve.kserve.controller.tag | string | `"v0.21.0"` | KServe controller container image tag. |
| kserve.kserve.controller.tolerations | list | `[]` | A list of Kubernetes Tolerations, if required. For more information, see [Toleration v1 core](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#toleration-v1-core).  For example:   tolerations:   - key: foo.bar.com/role     operator: Equal     value: master     effect: NoSchedule |
| kserve.kserve.controller.topologySpreadConstraint | object | `{}` | The default topology spread constraint. If not defined the global topology spread constraint would be used instead only if topologySpreadConstraints list is empty. |
| kserve.kserve.controller.topologySpreadConstraints | list | `[]` | A list of Kubernetes TopologySpreadConstraints, if required. For more information, see \[Topology spread constraint v1 core\](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#topologyspreadconstraint-v1-core  For example:   topologySpreadConstraints:   - maxSkew: 2     topologyKey: topology.kubernetes.io/zone     whenUnsatisfiable: ScheduleAnyway     labelSelector:       matchLabels:         app.kubernetes.io/instance: kserve-controller-manager         app.kubernetes.io/component: controller |
| kserve.kserve.localmodel.controller.image | string | `"kserve/kserve-localmodel-controller"` |  |
| kserve.kserve.localmodel.controller.tag | string | `"v0.21.0"` |  |
| kserve.kserve.localmodel.enabled | bool | `false` | Feeds the `localModel` block of `inferenceservice-config` only and must stay false: the chart ships no localmodel controller (the dormant copy vendored with 0.19 was removed with 0.21; the feature arrives with the upstream kserve-localmodel charts). Rendering fails on `true` so an old values file cannot enable the feature with no controller behind it. `controller` and `serviceAccount` are kept for values compatibility and render nothing. |
| kserve.kserve.localmodel.jobNamespace | string | `"kserve-localmodel-jobs"` |  |
| kserve.kserve.localmodel.securityContext | object | `{"FSGroup":1000}` | security context configuration |
| kserve.kserve.localmodel.serviceAccount.annotations | object | `{}` | service account annotations |
| kserve.kserve.metricsaggregator.enableMetricAggregation | string | `"true"` | configures metric aggregation annotation. This adds the annotation serving.kserve.io/enable-metric-aggregation to every service with the specified boolean value. If true enables metric aggregation in queue-proxy by setting env vars in the queue proxy container to configure scraping ports. |
| kserve.kserve.metricsaggregator.enablePrometheusScraping | string | `"true"` | If true, prometheus annotations are added to the pod to scrape the metrics. If serving.kserve.io/enable-metric-aggregation is false, the prometheus port is set with the default prometheus scraping port 9090, otherwise the prometheus port annotation is set with the metric aggregation port. |
| kserve.kserve.nodeSelector | object | `{}` | node selector configuration |
| kserve.kserve.router.image | string | `"kserve/router"` |  |
| kserve.kserve.router.tag | string | `"v0.21.0"` |  |
| kserve.kserve.serviceAccount.annotations | object | `{}` | service account annotations |
| kserve.kserve.servingruntime.modelNamePlaceholder | string | `"{{.Name}}"` |  |
| kserve.kserve.servingruntime.sklearnserver.image | string | `"hopsworks/sklearnserver"` |  |
| kserve.kserve.servingruntime.sklearnserver.tag | string | `"0.21.0"` |  |
| kserve.kserve.servingruntime.tensorflow.image | string | `"tensorflow/serving"` |  |
| kserve.kserve.servingruntime.tensorflow.tag | string | `"2.20.0"` |  |
| kserve.kserve.servingruntime.vllmomni | object | `{"env":[],"image":"vllm/vllm-omni","imageRegistry":"","tag":"v0.28.0"}` | backs the `vllm-omni` ClusterServingRuntime (vLLM-Omni) |
| kserve.kserve.servingruntime.vllmomni.env | list | `[]` | Additional environment variables for vllm-omni container |
| kserve.kserve.servingruntime.vllmomni.imageRegistry | string | `""` | Registry override for the vllm-omni image. Empty falls back to the global image registry (`global._hopsworks.imageRegistry`). |
| kserve.kserve.servingruntime.vllmopenai | object | `{"env":[],"image":"vllm/vllm-openai","imageRegistry":"","tag":"v0.28.0"}` | backs the `vllm-openai` ClusterServingRuntime (standard vLLM) |
| kserve.kserve.servingruntime.vllmopenai.env | list | `[]` | Additional environment variables for vllm-openai container |
| kserve.kserve.servingruntime.vllmopenai.imageRegistry | string | `""` | Registry override for the vllm-openai image. Empty falls back to the global image registry (`global._hopsworks.imageRegistry`). |
| kserve.kserve.storage.caBundleConfigMapName | string | `""` | Mounted CA bundle config map name for storage initializer. |
| kserve.kserve.storage.caBundleVolumeMountPath | string | `"/etc/ssl/custom-certs"` | Mounted path for CA bundle config map. |
| kserve.kserve.storage.cpuModelcar | string | `"10m"` | Model sidecar cpu requirement. |
| kserve.kserve.storage.enableModelcar | bool | `false` | Flag for enabling model sidecar feature. |
| kserve.kserve.storage.image | string | `"hopsworks/storage-initializer"` |  |
| kserve.kserve.storage.memoryModelcar | string | `"15Mi"` | Model sidecar memory requirement. |
| kserve.kserve.storage.resources | object | `{"limits":{"cpu":"1","memory":"1Gi"},"requests":{"cpu":"100m","memory":"100Mi"}}` | Requests and limits KServe gives the storage-initializer init container it injects for storageUri models (the `storageInitializer` block of `inferenceservice-config`). |
| kserve.kserve.storage.resources.limits | object | `{"cpu":"1","memory":"1Gi"}` | cpu and memory are read by the templates; other resource names pass through to the ClusterStorageContainer. |
| kserve.kserve.storage.resources.requests | object | `{"cpu":"100m","memory":"100Mi"}` | cpu and memory are read by the templates; other resource names pass through to the ClusterStorageContainer. |
| kserve.kserve.storage.s3 | object | `{"CABundle":"","accessKeyIdName":"AWS_ACCESS_KEY_ID","endpoint":"","region":"","secretAccessKeyName":"AWS_SECRET_ACCESS_KEY","useAnonymousCredential":"","useHttps":"","useVirtualBucket":"","verifySSL":""}` | Configurations for S3 storage |
| kserve.kserve.storage.s3.CABundle | string | `""` | The path to the certificate bundle to use for HTTPS certificate validation. |
| kserve.kserve.storage.s3.accessKeyIdName | string | `"AWS_ACCESS_KEY_ID"` | AWS S3 static access key id. |
| kserve.kserve.storage.s3.endpoint | string | `""` | AWS S3 endpoint. |
| kserve.kserve.storage.s3.region | string | `""` | Default region name of AWS S3. |
| kserve.kserve.storage.s3.secretAccessKeyName | string | `"AWS_SECRET_ACCESS_KEY"` | AWS S3 static secret access key. |
| kserve.kserve.storage.s3.useAnonymousCredential | string | `""` | Whether to use anonymous credentials to download the model or not, default to false. |
| kserve.kserve.storage.s3.useHttps | string | `""` | Whether to use secured https or http to download models, allowed values are 0 and 1 and default to 1. |
| kserve.kserve.storage.s3.useVirtualBucket | string | `""` | Whether to use virtual bucket or not, default to false. |
| kserve.kserve.storage.s3.verifySSL | string | `""` | Whether to verify the tls/ssl certificate, default to true. |
| kserve.kserve.storage.storageSecretNameAnnotation | string | `"serving.kserve.io/secretName"` | Storage secret name reference for storage initializer. |
| kserve.kserve.storage.storageSpecSecretName | string | `"storage-config"` | Storage spec secret name. |
| kserve.kserve.storage.tag | string | `"5.2.0-SNAPSHOT"` | Hopsworks-built storage initializer tag. Pinned to the Hopsworks version (matching storageInitializer.tag and what the model-serving-webhook publishes), not the KServe version anchor. |
| kserve.kserve.storage.uidModelcar | int | `1010` | UID under which the modelcar process and the main container run. Some clusters require root (0). |
| kserve.kserve.tolerations | list | `[]` |  |
| kserve.kserve.topologySpreadConstraint | object | `{}` | The default topology spread constraint. If not defined the global topology spread constraint would be used instead only if topologySpreadConstraints list is empty. |
| kserve.kserve.version | string | `"v0.21.0"` |  |
| kserve.kserveUtilsImage.name | string | `"hopsworks/kserve-utils"` |  |
| kserve.kserveUtilsImage.tag | string | `"0.1.11"` |  |
| kserve.manager.serviceAccount.annotations | object | `{}` | service account annotations |
| kserve.servingAuthenticator.image | string | `"hopsworks/model-serving-authenticator"` |  |
| kserve.servingAuthenticator.name | string | `"model-serving-authenticator"` |  |
| kserve.servingAuthenticator.podDisruptionBudget.enabled | bool | `true` |  |
| kserve.servingAuthenticator.podDisruptionBudget.minAvailable | int | `1` |  |
| kserve.servingAuthenticator.replicaCount | int | `1` |  |
| kserve.servingAuthenticator.requireExternalUserLoginAfterHours | int | `720` | Number of hours after which external users are required to sign in to Hopsworks to refresh their external user groups. Allowed values are -1, 0 and greater than 0, where -1 skips the periodic sign-in requirement and 0 disables external access completely. |
| kserve.servingAuthenticator.serviceAccount.annotations | object | `{}` | service account annotations |
| kserve.servingAuthenticator.tag | string | `"5.2.0-SNAPSHOT"` |  |
| kserve.servingTerminationGracePeriodSeconds | int | `120` | Grace period in seconds the model-serving-webhook stamps onto every serving pod, replacing the value Knative derives from the revision timeout. Must cover the in-pod log archive a disk-logging component uploads to the project's Logs dataset as it terminates (roughly fifteen seconds including SDK import and login). A ceiling, not a delay: a pod with nothing to archive exits as soon as its containers do. |
| kserve.servingWebhook.ephemeralVolume | object | `{"accessModes":["ReadWriteOnce"],"enabled":false,"storageClassName":"","storageSize":"60Gi"}` | Configuration for ephemeral volumes in LLM deployments |
| kserve.servingWebhook.ephemeralVolume.accessModes | list | `["ReadWriteOnce"]` | Access modes for the ephemeral volume |
| kserve.servingWebhook.ephemeralVolume.enabled | bool | `false` | Enable ephemeral volume injection for LLM deployments |
| kserve.servingWebhook.ephemeralVolume.storageClassName | string | `""` | Storage class name for the ephemeral volume |
| kserve.servingWebhook.ephemeralVolume.storageSize | string | `"60Gi"` | Storage size for the ephemeral volume |
| kserve.servingWebhook.image | string | `"hopsworks/model-serving-webhook"` |  |
| kserve.servingWebhook.name | string | `"model-serving-webhook"` |  |
| kserve.servingWebhook.podDisruptionBudget.enabled | bool | `true` |  |
| kserve.servingWebhook.podDisruptionBudget.minAvailable | int | `1` |  |
| kserve.servingWebhook.replicaCount | int | `1` |  |
| kserve.servingWebhook.serviceAccount.annotations | object | `{}` | service account annotations |
| kserve.servingWebhook.tag | string | `"5.2.0-SNAPSHOT"` |  |
| kserve.servingWebhook.ttlSecondsAfterFinished | string | `nil` | TTL in seconds for the serving-mwh Job. Overrides global default. |
| kserve.storageInitializer.image | string | `"hopsworks/storage-initializer"` |  |
| kserve.storageInitializer.tag | string | `"5.2.0-SNAPSHOT"` |  |
| kserve.webhook.minReplicas | int | `1` |  |
| kserve.webhook.podDisruptionBudget.enabled | bool | `true` |  |
| kserve.webhook.podDisruptionBudget.minAvailable | int | `1` |  |
| kserve.webhook.serviceAccount.annotations | object | `{}` | service account annotations |
| minio.add_node_port | bool | `false` |  |
| minio.affinity | object | `{}` | affinity configuration |
| minio.buckets\[0\].name | string | `"hopsworks"` |  |
| minio.cleanupOnUninstall | object | `{"enabled":true,"ttlSecondsAfterFinished":null}` | post-delete cleanup of MinIO leftovers. The MinIO StatefulSet PVC survives uninstall; this deletes it by label (app=minio), but only when global._hopsworks.wipeDataOnUninstall is enabled and never for PVCs labelled hopsworks.ai/keep=true. |
| minio.cleanupOnUninstall.enabled | bool | `true` | enable the post-delete MinIO data-PVC cleanup hook (also requires global._hopsworks.wipeDataOnUninstall) |
| minio.cleanupOnUninstall.ttlSecondsAfterFinished | string | `nil` | ttlSecondsAfterFinished for the cleanup Job; null falls through to the global default |
| minio.deployment.env.MINIO_REGION | string | `"eu-west-1"` |  |
| minio.deployment.env.MINIO_ROOT_PASSWORD | string | `"minioadmin"` |  |
| minio.deployment.env.MINIO_ROOT_USER | string | `"minioadmin"` |  |
| minio.deployment.extra_envs | object | `{"MINIO_PROMETHEUS_AUTH_TYPE":"public"}` | extra envs |
| minio.deployment.ports.console | int | `9001` |  |
| minio.deployment.ports.http | int | `9000` |  |
| minio.deploymentName | string | `"minio"` |  |
| minio.enabled | bool | `true` |  |
| minio.hopsworkslib | object | `{}` | override hopsworkslib values |
| minio.image.name | string | `"minio"` |  |
| minio.image.pullPolicy | string | `"IfNotPresent"` |  |
| minio.image.registry | string | `"docker.hops.works"` |  |
| minio.image.tag | string | `"RELEASE.2024-03-26T22-10-45Z-cpuv1"` |  |
| minio.nodeSelector | object | `{}` | node selector configuration |
| minio.podDisruptionBudget.enabled | bool | `true` |  |
| minio.podDisruptionBudget.minAvailable | int | `1` |  |
| minio.protocol | string | `"http"` |  |
| minio.publicBuckets\[0\].name | string | `"public"` |  |
| minio.publicBuckets\[1\].name | string | `"buildkit"` |  |
| minio.replicas | int | `2` |  |
| minio.resources.limits.cpu | string | `"2"` |  |
| minio.resources.limits.memory | string | `"4Gi"` |  |
| minio.resources.requests.cpu | string | `"1"` |  |
| minio.resources.requests.memory | string | `"4Gi"` |  |
| minio.service.annotations."consul.hashicorp.com/service-name" | string | `"minio"` |  |
| minio.service.annotations."consul.hashicorp.com/service-port" | string | `"http"` |  |
| minio.service.name | string | `"minio"` |  |
| minio.service.ports.console | int | `9001` |  |
| minio.service.ports.http | int | `9000` |  |
| minio.storage | string | `"100Gi"` |  |
| minio.storageClassName | string | `nil` | storage class name |
| minio.tests.minioBackup.bucket | string | `""` |  |
| minio.tests.minioBackup.enabled | bool | `false` |  |
| minio.tests.minioBackup.subfolder | string | `""` |  |
| minio.tolerations | list | `[]` |  |
| olk.appName | string | `"elk"` |  |
| olk.cleanupOnUninstall | object | `{"enabled":true,"ttlSecondsAfterFinished":null}` | post-delete cleanup of OLK leftovers. Always deletes the signingjwt Secret (created centrally, or copied in satellite; not Helm-tracked). Also deletes the OpenSearch StatefulSet PVC by label (app=opensearch) when global._hopsworks.wipeDataOnUninstall is enabled, except PVCs labelled hopsworks.ai/keep=true. |
| olk.cleanupOnUninstall.enabled | bool | `true` | enable the post-delete OLK cleanup hook (signingjwt Secret always; OpenSearch PVC additionally requires global._hopsworks.wipeDataOnUninstall) |
| olk.cleanupOnUninstall.ttlSecondsAfterFinished | string | `nil` | ttlSecondsAfterFinished for the cleanup Job; null falls through to the global default |
| olk.dashboard.config.basePath | string | `"/hopsworks-api/kibana"` |  |
| olk.dashboard.config.index | string | `".kibana"` |  |
| olk.dashboard.config.name | string | `"dashboard-config"` |  |
| olk.dashboard.deleteKibanaIndexIfPrevious | bool | `false` |  |
| olk.dashboard.export | bool | `false` |  |
| olk.dashboard.jwt.roles_key | string | `"roles"` |  |
| olk.dashboard.jwt.subject_key | string | `"sub"` |  |
| olk.dashboard.jwt.url_parameter | string | `"jt"` |  |
| olk.dashboard.name | string | `"opensearch-dashboard"` |  |
| olk.dashboard.nodeSelector | object | `{}` | node selector configuration |
| olk.dashboard.port | int | `5601` |  |
| olk.dashboard.resources.limits.cpu | string | `"200m"` |  |
| olk.dashboard.resources.limits.memory | string | `"1Gi"` |  |
| olk.dashboard.resources.requests.cpu | string | `"50m"` |  |
| olk.dashboard.resources.requests.memory | string | `"512Mi"` |  |
| olk.dashboard.security.cookie_ttl | int | `1800000` |  |
| olk.dashboard.security.session_ttl | int | `3600000` |  |
| olk.dashboard.security_context.fsGroup | int | `1000` |  |
| olk.dashboard.security_context.runAsGroup | int | `1000` |  |
| olk.dashboard.security_context.runAsNonRoot | bool | `true` |  |
| olk.dashboard.security_context.runAsUser | int | `1000` |  |
| olk.dashboard.service.annotations."consul.hashicorp.com/service-name" | string | `"kibana"` |  |
| olk.dashboard.shard_timeout | int | `10000` |  |
| olk.dashboard.startup_timeout | int | `5000` |  |
| olk.dashboard.tolerations | list | `[]` |  |
| olk.dashboard.topologySpreadConstraint | object | `{}` | The default topology spread constraint. If not defined the global topology spread constraint would be used instead. |
| olk.dashboard.version | string | `"2.19.6.7"` |  |
| olk.filebeat.config.name | string | `"filebeat-config"` |  |
| olk.filebeat.enabled | bool | `true` |  |
| olk.filebeat.extraNamespaces | list | `[]` | extra namespaces to process their container logs. By default the release name space and the Hopsworks project namespaces are whitelisted. |
| olk.filebeat.fullnameOverride | string | `nil` | full name override |
| olk.filebeat.image.tag | string | `"8.19.21"` |  |
| olk.filebeat.kubernetesMetadata.cronjob | bool|null | `nil` | attach kubernetes.cronjob.name; unset leaves filebeat's default |
| olk.filebeat.kubernetesMetadata.deployment | bool|null | `nil` | attach kubernetes.deployment.name; unset leaves filebeat's default |
| olk.filebeat.kubernetesMetadata.extraNamespaceLabels | list | `[]` | extra namespace labels to keep, appended to logFilteringNamespaceLabels |
| olk.filebeat.kubernetesMetadata.extraNodeLabels | list | `[]` | extra node labels to keep, appended to logFilteringNodeLabels |
| olk.filebeat.kubernetesMetadata.extraPodLabels | list | `[]` | extra pod labels to keep, appended to logFilteringPodLabels |
| olk.filebeat.kubernetesMetadata.logFilteringNamespaceLabels | list | `["hopsworks.ai/project","hopsworks.ai/onlinefs-cluster"]` | namespace labels Hopsworks' log filtering reads |
| olk.filebeat.kubernetesMetadata.logFilteringNodeLabels | list | `["kubernetes.io/hostname"]` | node labels Hopsworks' log filtering reads |
| olk.filebeat.kubernetesMetadata.logFilteringPodLabels | list | `["name","app","app.kubernetes.io/name","service","rondbService","component","user","job-type","job-id","job-name","execution","jupyter","jupyter-id","jupyter-settings-id","kernel-id","spark-role","spark-app-selector","sparkoperator.k8s.io/launched-by-spark-operator","serving.hops.works/id","serving.hops.works/name","serving.hops.works/tool","serving.hops.works/model-name","serving.hops.works/model-version","serving.hops.works/model-server","serving.hops.works/project-id"]` | pod labels Hopsworks' log filtering reads |
| olk.filebeat.kubernetesMetadata.namespaceAnnotations | list | `[]` | namespace annotations to keep. Empty collects none. |
| olk.filebeat.kubernetesMetadata.nodeAnnotations | list | `[]` | node annotations to keep. Empty collects none. |
| olk.filebeat.kubernetesMetadata.podAnnotations | list | `[]` | pod annotations to keep. Empty collects none, filebeat's default. |
| olk.filebeat.logs_locations\[0\].addKubernetesMetadata | bool | `true` | attach Kubernetes pod/namespace/node metadata to logs from this location, using the label whitelists in filebeat.kubernetesMetadata |
| olk.filebeat.logs_locations\[0\].glob | string | `"/*.log"` |  |
| olk.filebeat.logs_locations\[0\].logtype | string | `"log"` |  |
| olk.filebeat.logs_locations\[0\].mountPaths\[0\] | string | `"/var/log/containers"` |  |
| olk.filebeat.logs_locations\[0\].mountPaths\[1\] | string | `"/var/log/pods"` |  |
| olk.filebeat.logs_locations\[0\].name | string | `"containerd"` |  |
| olk.filebeat.logs_locations\[0\].path | string | `"/var/log/containers"` |  |
| olk.filebeat.logs_locations\[0\].processors | list | `[]` | extra processors for this location, appended after the metadata processor. Each entry is itself a list. |
| olk.filebeat.name | string | `"filebeat"` |  |
| olk.filebeat.resources.limits | object | `{"memory":"400Mi"}` | resources limits configuration |
| olk.filebeat.resources.requests.cpu | string | `"100m"` |  |
| olk.filebeat.resources.requests.memory | string | `"200Mi"` |  |
| olk.filebeat.serviceAccount.annotations | object | `{}` | service account annotations |
| olk.filebeat.terminationgraceperiod | int | `30` |  |
| olk.filebeat.tolerations | list | `[{"effect":"NoSchedule","operator":"Exists"}]` | tolerations for filebeat daemonset |
| olk.hopsworkslib | object | `{}` | override hopsworkslib values |
| olk.image.registry | string | `"docker.hops.works"` |  |
| olk.logstash.additional_audit_outputs | string | `""` |  |
| olk.logstash.batch_delay | int | `100` |  |
| olk.logstash.batch_size | int | `100` |  |
| olk.logstash.config.name | string | `"logstash-config"` |  |
| olk.logstash.debug | bool | `false` |  |
| olk.logstash.extendServicesPipeline | list | `[]` | extend the services pipeline to collect logs for other services besides the default. You need to define the kuberentes label key and value to identifiy the service. The serviceLabelValue will be used as the service name, and you can add extra mutation logic to rename some of the fields of the service log.  |
| olk.logstash.extraPipelines | list | `[]` | logstash extraPipelines |
| olk.logstash.extraServices | list | `[]` | logstash extraServices |
| olk.logstash.extraVolumeMounts | list | `[]` |  |
| olk.logstash.extraVolumes | list | `[]` |  |
| olk.logstash.hpa.enabled | bool | `false` | Autoscale Logstash. While enabled, logstash.replicas is not rendered and the HPA owns spec.replicas. |
| olk.logstash.hpa.maxReplicas | int | `3` |  |
| olk.logstash.hpa.targetCPUUtilizationPercentage | int | `80` |  |
| olk.logstash.hpa.targetMemoryUtilizationPercentage | int | `80` |  |
| olk.logstash.index_pattern | string | `".services-%{+YYYY.MM.dd}"` |  |
| olk.logstash.name | string | `"logstash"` |  |
| olk.logstash.nodeSelector | object | `{}` | node selector configuration |
| olk.logstash.plugins | list | `[]` |  |
| olk.logstash.podDisruptionBudget.enabled | bool | `true` |  |
| olk.logstash.podDisruptionBudget.minAvailable | int | `1` |  |
| olk.logstash.port | int | `5044` |  |
| olk.logstash.replicas | int | `1` | Number of Logstash replicas. Not rendered while logstash.hpa.enabled is true: the HPA then owns spec.replicas and this value is its minReplicas. Turning the HPA on for a running release drops Logstash to 1 once, until the HPA scales it back up. |
| olk.logstash.resources | object | `{"requests":{"cpu":"200m","memory":"2048Mi"}}` | resources configuration |
| olk.logstash.security_context.fsGroup | int | `1000` |  |
| olk.logstash.security_context.runAsGroup | int | `1000` |  |
| olk.logstash.security_context.runAsNonRoot | bool | `true` |  |
| olk.logstash.security_context.runAsUser | int | `1000` |  |
| olk.logstash.service.annotations."consul.hashicorp.com/service-name" | string | `"logstash"` |  |
| olk.logstash.service.annotations."consul.hashicorp.com/service-tags" | string | `"jupyter,pythonjobs"` |  |
| olk.logstash.service.type | string | `"ClusterIP"` |  |
| olk.logstash.tolerations | list | `[]` |  |
| olk.logstash.topologySpreadConstraint | object | `{}` | The default topology spread constraint. If not defined the global topology spread constraint would be used instead. |
| olk.logstash.version | string | `"7.17.29.6"` |  |
| olk.logstash.workers | int | `4` |  |
| olk.opensearch.audit.enable_rest | bool | `true` | Audit the REST layer (plugins.security.audit.config.enable_rest). Only applies when audit.enabled is true. |
| olk.opensearch.audit.enable_transport | bool | `false` | Audit the transport layer (plugins.security.audit.config.enable_transport). Only applies when audit.enabled is true. |
| olk.opensearch.audit.enabled | bool | `false` | Enable OpenSearch security audit logging to an in-cluster `security-auditlog-*` index. Disabled by default. When enabled, the chart also installs an ISM policy that deletes these daily indices after `audit.retentionDays`, so they don't grow unbounded. On single-node clusters the audit index stays yellow (its replica cannot be allocated; harmless); on multi-node it is green. |
| olk.opensearch.audit.retentionDays | int | `7` | Days to retain `security-auditlog-*` indices before ISM deletes them. Only applies when audit.enabled is true, and bounds the otherwise-unbounded daily audit index growth. NOTE: the `security-auditlog-retention` ISM policy is created once and never updated, so changing this value on an existing cluster has no effect on its own; to apply a new value, delete that ISM policy so it is recreated with the new setting on the next sync. |
| olk.opensearch.backup.enabled | string | `nil` |  |
| olk.opensearch.backup.repositories | object | `{}` | backup repository configuration |
| olk.opensearch.backup.ttl | string | `nil` | time to live to control when to clean up backups. It is a number followed by either d (days) or h (hours) suffix. |
| olk.opensearch.config.name | string | `"opensearch-config"` |  |
| olk.opensearch.cors.allow_origin | string | `"*"` |  |
| olk.opensearch.externalLoadBalancer.annotations | object | `{}` | load balancer annotations |
| olk.opensearch.externalLoadBalancer.class | string | `nil` | load balancer class name |
| olk.opensearch.externalLoadBalancer.enabled | string | `nil` | Enable External Load Balancers for Opensearch. If not set the .global._hopsworks.externalLoadBalancers.enabled will be used instead |
| olk.opensearch.externalLoadBalancer.managed | string | `nil` | Cloud provider provisions Load Balancers. If not set the .global._hopsworks.externalLoadBalancers.managed will be used instead |
| olk.opensearch.externalLoadBalancer.nodeSelector | object | `{}` | selector for nodes the load balancer can use to route traffic |
| olk.opensearch.jvmOpts | string | `""` | JVM Options to provide to Opensearch |
| olk.opensearch.knn.cache_expire | bool | `true` |  |
| olk.opensearch.knn.circuit_breaker.percent | float | `0.75` |  |
| olk.opensearch.knn.circuit_breaker.triggered | bool | `true` |  |
| olk.opensearch.knn.index_threads | int | `1` |  |
| olk.opensearch.knn.memory.circuit_breaker.limit | string | `"50%"` |  |
| olk.opensearch.mandatoryIndices\[0\] | string | `"projects"` |  |
| olk.opensearch.mandatoryIndices\[1\] | string | `"featurestore"` |  |
| olk.opensearch.max_shards_per_node | int | `3000` |  |
| olk.opensearch.memory.xms | string | `"2g"` |  |
| olk.opensearch.memory.xmx | string | `"2g"` |  |
| olk.opensearch.name | string | `"opensearch"` |  |
| olk.opensearch.nodeSelector | object | `{}` | node selector configuration |
| olk.opensearch.plugins | list | `[]` |  |
| olk.opensearch.podDisruptionBudget.enabled | bool | `true` |  |
| olk.opensearch.podDisruptionBudget.minAvailable | int | `1` |  |
| olk.opensearch.port | int | `9200` |  |
| olk.opensearch.protocol | string | `"https"` |  |
| olk.opensearch.replicas | int | `1` |  |
| olk.opensearch.resources.limits | object | `{"memory":"4000Mi"}` | resources limits configuration |
| olk.opensearch.resources.requests.cpu | string | `"100m"` |  |
| olk.opensearch.resources.requests.memory | string | `"2000Mi"` |  |
| olk.opensearch.restore.enabled | string | `nil` | If true an initial job will be created to restore the data from the backup. Backup jobs will bypass creating snapshots while this job is running. |
| olk.opensearch.restore.list_snapshots | bool | `true` |  |
| olk.opensearch.restore.pause_backup_while_restoring | string | `"SKIP"` | If set, the backup jobs will be paused while the restore job is running. Values are SKIP or PAUSE, in case none, the backup will wait for the restore to finish |
| olk.opensearch.restore.repositories | object | `{}` | restore repositories configuration |
| olk.opensearch.security.admin_locality | string | `"elkadmin"` |  |
| olk.opensearch.security.create_secret | bool | `true` | Create the opensearch-users-secrets secret with the opensearch internal users passwords  |
| olk.opensearch.security.default_tenant | string | `"Private"` | Default OpenSearch tenant for Dashboards users. A non-empty value suppresses the OpenSearch Dashboards 2.x "Select your tenant" popup (the plugin only prompts when the reported default_tenant is empty). Hopsworks links open Dashboards with the Private tenant, so "Private" matches that and keeps multitenancy/index-pattern isolation intact. Set to "" to restore the popup / leave the default tenant unset. |
| olk.opensearch.security.extraDnsNames | list | `[]` | Additional DNS names to add as SAN to Datanode x.509 certificate |
| olk.opensearch.security.extraIpAddresses | list | `[]` | Additional IP addresses to add as SAN to Datanode x.509 certificate |
| olk.opensearch.security.locality | string | `"elastic"` |  |
| olk.opensearch.security.multitenancy_enabled | bool | `true` |  |
| olk.opensearch.service.annotations."consul.hashicorp.com/service-name" | string | `"elastic"` |  |
| olk.opensearch.service.annotations."consul.hashicorp.com/service-port" | string | `"http"` |  |
| olk.opensearch.service.annotations."consul.hashicorp.com/service-tags" | string | `"rest"` |  |
| olk.opensearch.service.headlessName | string | `"opensearch-headless"` |  |
| olk.opensearch.serviceAccount.annotations | object | `{}` | service account annotations |
| olk.opensearch.serviceAccountName | string | `"opensearch"` |  |
| olk.opensearch.setVMMaxMapCount | bool | `true` | https://docs.opensearch.org/2.19/install-and-configure/install-opensearch/index/#important-settings |
| olk.opensearch.storageClassName | string | `nil` | storage class name |
| olk.opensearch.storage_size | string | `"20Gi"` |  |
| olk.opensearch.tolerations | list | `[]` |  |
| olk.opensearch.topologySpreadConstraint | object | `{}` | The default topology spread constraint. If not defined the global topology spread constraint would be used instead. |
| olk.opensearch.transport_port | int | `9300` |  |
| olk.opensearch.ttlSecondsAfterFinished | string | `nil` | TTL in seconds for the create-repos Job. Overrides global default. |
| olk.opensearch.version | string | `"2.19.6.3"` |  |
| olk.prometheus-elasticsearch-exporter | object | `{"es":{"sslSkipVerify":true,"uri":"https://elastic_exporter:elastic_exporterpw@{{ include \"olk.exporter.opensearchHost\" . }}:9200"},"image":{"registry":"docker.hops.works","repository":"prometheus/elasticsearch-exporter","tag":"1.11.0-alpine-h1.1"},"nodeSelector":{},"resources":{"limits":{"cpu":"800m","memory":"200Mi"},"requests":{"cpu":"300m","memory":"128Mi"}},"service":{"annotations":{"prometheus.io/path":"/metrics","prometheus.io/port":"9108","prometheus.io/scheme":"http","prometheus.io/scrape":"true"},"httpPort":9108},"tolerations":[]}` | override prometheus elasticsearch exporter values |
| onlinefs.apiKey.email | string | `"onlinefs@hopsworks.ai"` |  |
| onlinefs.apiKey.password | string | `"onlinefspw"` |  |
| onlinefs.apiKey.secret_name | string | `"onlinefs-api-key-auth"` |  |
| onlinefs.appName | string | `"onlinefs"` |  |
| onlinefs.configmap.name | string | `"onlinefs-configmap"` |  |
| onlinefs.configmapOverrides.kafka | object | `{}` | Extra properties to add or overwrite in onlinefs-kafka.properties |
| onlinefs.configmapOverrides.kafkaVectorDb | object | `{}` | Extra properties to add or overwrite in onlinefs-kafka-vector-db.properties |
| onlinefs.configmapOverrides.log4j | object | `{}` | Extra properties to add or overwrite in log4j.properties |
| onlinefs.configmapOverrides.onlinefssite.hopsworks.tokenLocation | string | `"/onlinefs/etc/token"` |  |
| onlinefs.configmapOverrides.onlinefssite.kafkaConsumer.pollTimeoutMs | int | `1000` |  |
| onlinefs.configmapOverrides.onlinefssite.kafkaConsumer.topicList | string | `""` |  |
| onlinefs.configmapOverrides.onlinefssite.kafkaConsumer.topicPattern | string | `".*_onlinefs"` |  |
| onlinefs.configmapOverrides.onlinefssite.rondb.batchSize | int | `300` |  |
| onlinefs.configmapOverrides.onlinefssite.rondb.maxCachedInstances | int | `1024` |  |
| onlinefs.configmapOverrides.onlinefssite.rondb.maxCachedSessions | int | `20` |  |
| onlinefs.configmapOverrides.onlinefssite.rondb.maxTransactions | int | `1024` |  |
| onlinefs.configmapOverrides.onlinefssite.rondb.poolSize | int | `1` |  |
| onlinefs.configmapOverrides.onlinefssite.rondb.reconnectTimeout | int | `5` |  |
| onlinefs.configmapOverrides.onlinefssite.rondb.useDynamicObjectCache | bool | `false` |  |
| onlinefs.configmapOverrides.onlinefssite.rondb.useSessionCache | bool | `false` |  |
| onlinefs.configmapOverrides.onlinefssite.service.featureGroupCacheExpire | int | `30` |  |
| onlinefs.configmapOverrides.onlinefssite.service.featureStoreCacheExpire | int | `30` |  |
| onlinefs.configmapOverrides.onlinefssite.service.featureViewCacheExpire | int | `10` |  |
| onlinefs.configmapOverrides.onlinefssite.service.getSessionRetrySleepMs | int | `100` |  |
| onlinefs.configmapOverrides.onlinefssite.service.maxBlacklistSize | int | `100` |  |
| onlinefs.configmapOverrides.onlinefssite.service.maxFeatureGroupCacheSize | int | `1000` |  |
| onlinefs.configmapOverrides.onlinefssite.service.maxFeatureStoreCacheSize | int | `1000` |  |
| onlinefs.configmapOverrides.onlinefssite.service.maxFeatureViewCacheSize | int | `1000` |  |
| onlinefs.configmapOverrides.onlinefssite.service.pauseRetrySleepMs | int | `5000` |  |
| onlinefs.configmapOverrides.onlinefssite.service.ronDbThreadNumber | int | `10` |  |
| onlinefs.configmapOverrides.onlinefssite.service.threadNumber | int | `10` |  |
| onlinefs.configmapOverrides.onlinefssite.service.vectorDbThreadNumber | int | `10` |  |
| onlinefs.configmapOverrides.producer | object | `{}` | Extra properties to add or overwrite in producer.properties |
| onlinefs.debug | bool | `false` |  |
| onlinefs.dependencies.glassfish.consulServiceName | string | `"glassfish"` |  |
| onlinefs.dependencies.glassfish.consulServiceTag | string | `"hopsworks"` |  |
| onlinefs.dependencies.glassfish.port | int | `8182` |  |
| onlinefs.dependencies.kafka.consulServiceName | string | `"kafka"` |  |
| onlinefs.dependencies.kafka.consulServiceTag | string | `"broker"` |  |
| onlinefs.dependencies.kafka.port | int | `9092` |  |
| onlinefs.dependencies.kafka.securityProtocol | string | `"SSL"` | Kafka security.protocol. PLAINTEXT or SSL |
| onlinefs.dependencies.kafka.url | string | `""` | The Kafka Brokers URL (can be comma-separated urls with port or a single url), if not set the consul DNS name will be used |
| onlinefs.dependencies.mgmd.consulServiceName | string | `"mgmd"` |  |
| onlinefs.dependencies.mgmd.port | int | `1186` |  |
| onlinefs.dependencies.mgmd.url | string | `""` | The mgmd URL, if not set the consul DNS name will be used |
| onlinefs.dependencies.opensearch.consulServiceName | string | `"elastic"` |  |
| onlinefs.dependencies.opensearch.consulServiceTag | string | `"rest"` |  |
| onlinefs.dependencies.opensearch.port | int | `9200` |  |
| onlinefs.deployment.env.JAVA_OPTS | string | `"-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:9029"` |  |
| onlinefs.deployment.name | string | `"onlinefs-deployment"` |  |
| onlinefs.deployment.ports.debug | int | `9029` |  |
| onlinefs.deployment.ports.monitor | int | `12800` |  |
| onlinefs.deployment.replicas | int | `1` | Number of replicas. Not rendered while hpa.enabled is true: the HPA then owns spec.replicas and this value is its minReplicas. Turning the HPA on for a running release drops the Deployment to 1 once, until the HPA scales it back up. |
| onlinefs.deployment.resources.limits.cpu | string | `"4"` |  |
| onlinefs.deployment.resources.limits.memory | string | `"4096Mi"` |  |
| onlinefs.deployment.resources.requests.cpu | string | `"2"` |  |
| onlinefs.deployment.resources.requests.memory | string | `"1024Mi"` |  |
| onlinefs.deployment.strategy | object | `{}` | spec.strategy of the Deployment, rendered as given when set. Left empty, two or more replicas roll out by terminating a pod before creating its replacement (maxSurge 0, maxUnavailable 1), so an upgrade completes on a node pool with no room for an extra pod, and a single replica keeps the Kubernetes default. Set it explicitly for a single-replica install whose node pool cannot fit a surge pod, or to keep surge-first behaviour on an install with spare capacity that would rather not drop a consumer during a rollout. |
| onlinefs.deployment.vectordb.enabled | bool | `true` |  |
| onlinefs.hopsworkslib | object | `{}` | override hopsworkslib values |
| onlinefs.hpa.enabled | bool | `false` | Autoscale the Deployment with an HPA. While enabled, deployment.replicas is not rendered and the HPA owns spec.replicas. |
| onlinefs.hpa.maxReplicas | int | `5` |  |
| onlinefs.hpa.targetCPUUtilizationPercentage | int | `80` |  |
| onlinefs.hpa.targetMemoryUtilizationPercentage | int | `80` |  |
| onlinefs.nodeSelector | object | `{}` | node selector configuration |
| onlinefs.podDisruptionBudget.enabled | bool | `true` |  |
| onlinefs.podDisruptionBudget.minAvailable | int | `1` |  |
| onlinefs.rbac.annotations | object | `{}` | rbac annotations |
| onlinefs.rbac.create | bool | `true` |  |
| onlinefs.rbac.extraRoleRules | list | `[]` |  |
| onlinefs.rbac.name | string | `"onlinefs-role"` |  |
| onlinefs.rbac.useExistingRole | bool | `false` |  |
| onlinefs.service.debug.annotations."consul.hashicorp.com/service-name" | string | `"onlinefs"` |  |
| onlinefs.service.debug.annotations."consul.hashicorp.com/service-tags" | string | `"debug"` |  |
| onlinefs.service.debug.name | string | `"onlinefs-debug"` |  |
| onlinefs.service.debug.port | int | `9029` |  |
| onlinefs.service.monitoring.annotations."consul.hashicorp.com/service-name" | string | `"onlinefs"` |  |
| onlinefs.service.monitoring.annotations."consul.hashicorp.com/service-tags" | string | `"monitor"` |  |
| onlinefs.service.monitoring.annotations."prometheus.io/path" | string | `"/metrics"` |  |
| onlinefs.service.monitoring.annotations."prometheus.io/port" | int | `12800` |  |
| onlinefs.service.monitoring.annotations."prometheus.io/scheme" | string | `"http"` |  |
| onlinefs.service.monitoring.annotations."prometheus.io/scrape" | string | `"true"` |  |
| onlinefs.service.monitoring.name | string | `"onlinefs-monitor"` |  |
| onlinefs.service.monitoring.port | int | `12800` |  |
| onlinefs.serviceAccount.annotations | object | `{}` | service account annotations |
| onlinefs.serviceAccount.create | bool | `true` |  |
| onlinefs.serviceAccount.name | string | `"onlinefs-default"` |  |
| onlinefs.setupBackOffLimit | int | `10` |  |
| onlinefs.tlscerts.commonName | string | `""` |  |
| onlinefs.tlscerts.locality | string | `"onlinefs"` |  |
| onlinefs.tolerations | list | `[]` |  |
| onlinefs.topologySpreadConstraint | object | `{}` | The default topology spread constraint. If not defined the global topology spread constraint would be used instead. |
| prometheus.adapter.enabled | bool | `true` |  |
| prometheus.configAnnotations | object | `{}` | alertmanager-tmpl config map annotations  |
| prometheus.externalLoadBalancer.enabled | bool | `false` | Enable External Load Balancers for Prometheus server. If not set the .global._hopsworks.externalLoadBalancers.enabled will be used instead. If enabled AND you want the LoadBalancer to be **managed** you shall set prometheus.server.service.type: LoadBalancer - NOTE: Consul domain name will be a CNAME to LoadBalancer domain name If enabled AND you want the LoadBalancer to be **unmanged** you shall set prometheus.server.service.type: NodePort - NOTE: This only works in AWS |
| prometheus.externalLoadBalancer.managed | string | `nil` | Cloud provider provisions Load Balancers. If not set the .global._hopsworks.externalLoadBalancers.managed will be used instead |
| prometheus.externalLoadBalancer.nodeSelector | object | `{}` | selector for nodes the load balancer can use to route traffic |
| prometheus.hopsworkslib | object | `{}` | override hopsworkslib values |
| prometheus.prometheus | object | check \[values.yaml\](./values.yaml) for more information | override prometheus values |
| prometheus.prometheus-adapter | object | `{"dnsConfig":{"searches":["service.consul"]},"image":{"pullPolicy":"IfNotPresent","repository":"docker.hops.works/prometheus/prometheus-adapter","tag":"0.12.0-alpine-h1.1"},"nameOverride":"hopsworks-prometheus-adapter","nodeSelector":{},"prometheus":{"path":"","port":9090,"url":"http://prometheus.service.consul"},"resources":{"limits":{"cpu":"100m","memory":"70Mi"},"requests":{"cpu":"50m","memory":"40Mi"}},"rules":{"existing":"custom-prometheus-metrics-adapter"},"tolerations":[],"topologySpreadConstraints":[{"labelSelector":{"matchLabels":{"app.kubernetes.io/instance":"hopsworks","app.kubernetes.io/name":"hopsworks-prometheus-adapter"}},"maxSkew":1,"topologyKey":"topology.kubernetes.io/zone","whenUnsatisfiable":"ScheduleAnyway"}]}` | override prometheus-adapter values |
| ray.kuberay-operator | object | `{"batchScheduler":{"enabled":false,"name":""},"crNamespacedRbacEnable":true,"env":null,"featureGates":[{"enabled":false,"name":"RayClusterStatusConditions"}],"fullnameOverride":"kuberay-operator","image":{"pullPolicy":"IfNotPresent","repository":"docker.hops.works/hopsworks/kuberay-operator","tag":"1.4.0-h1"},"leaderElectionEnabled":true,"livenessProbe":{"failureThreshold":5,"initialDelaySeconds":10,"periodSeconds":5},"logging":{"baseDir":"","fileEncoder":"","fileName":"","stdoutEncoder":""},"nameOverride":"kuberay-operator","podSecurityContext":{},"rbacEnable":true,"readinessProbe":{"failureThreshold":5,"initialDelaySeconds":10,"periodSeconds":5},"resources":{"limits":{"cpu":"100m","memory":"512Mi"}},"securityContext":{"allowPrivilegeEscalation":false,"capabilities":{"drop":["ALL"]},"readOnlyRootFilesystem":true,"runAsNonRoot":true,"seccompProfile":{"type":"RuntimeDefault"}},"service":{"port":8080,"type":"ClusterIP"},"serviceAccount":{"create":true,"name":"kuberay-operator"},"singleNamespaceInstall":false}` | override kuberay-operator values |
| rondb.rondb | object | `{"backups":{"enabled":null,"pathPrefix":"rondb_backup"},"clusterSize":{"activeDataReplicas":1,"maxNumMySQLServers":5,"maxNumRdrs":2,"minNumMySQLServers":1,"minNumRdrs":1,"numNodeGroups":1},"images":{"mysqldExporter":{"registry":"docker.hops.works","repository":"hopsworks"},"rondb":{"registry":"docker.hops.works","repository":"hopsworks"},"toolbox":{"registry":"docker.hops.works","repository":"hopsworks"}},"meta":{"ddlMySQLd":{"clusterIp":{"annotations":{"consul.hashicorp.com/service-name":"mysqlddl","consul.hashicorp.com/service-tags":"onlinefs"}},"enabled":true,"statefulSet":{"endToEndTls":{"enabled":false,"filenames":{"ca":"hops_root_ca.pem","cert":"mysqlddl_certificate_bundle.pem","key":"mysqlddl_priv.pem"},"secretName":"mysqlddl-crypto-material","supplyOwnSecret":true}}},"mgmd":{"headlessClusterIp":{"annotations":{"consul.hashicorp.com/service-name":"mgmd"}}},"mysqld":{"clusterIp":{"annotations":{"consul.hashicorp.com/service-name":"mysql","consul.hashicorp.com/service-tags":"onlinefs"}},"statefulSet":{"endToEndTls":{"enabled":false,"filenames":{"ca":"hops_root_ca.pem","cert":"mysql_certificate_bundle.pem","key":"mysql_priv.pem"},"secretName":"mysqld-crypto-material","supplyOwnSecret":true}}},"rdrs":{"clusterIp":{"annotations":{"consul.hashicorp.com/service-name":"rdrs","prometheus.io/path":"/metrics","prometheus.io/port":"4406","prometheus.io/scheme":"https","prometheus.io/scrape":"true"}},"headlessClusterIpName":"rdrs-cluster-ip","ingress":{"enabled":false},"statefulSet":{"endToEndTls":{"enabled":true,"filenames":{"ca":"hops_root_ca.pem","cert":"mysql_certificate_bundle.pem","key":"mysql_priv.pem"},"secretName":"rdrs-crypto-material","supplyOwnSecret":true}}}},"mysql":{"clusterUser":"bench","exporter":{"enabled":true},"users":[{"host":"%","privileges":[{"database":"*","privileges":["ALL"],"table":"*","withGrantOption":true}],"username":"hopsworksroot"}]},"restoreFromBackup":{"backupId":null,"pathPrefix":"rondb_backup"}}` | override rondb values |
| spark.cleanupOnUninstall | object | `{"enabled":true,"ttlSecondsAfterFinished":null}` | post-delete cleanup of Spark/RSS leftovers: the spark-operator and rss-webhook TLS Secrets (generated at runtime by the operators, not Helm-tracked), and the rss shuffle-server data PVCs. PVCs are only deleted when global._hopsworks.wipeDataOnUninstall is enabled and never for PVCs labelled hopsworks.ai/keep=true. |
| spark.cleanupOnUninstall.enabled | bool | `true` | enable the post-delete Spark/RSS cleanup hook |
| spark.cleanupOnUninstall.ttlSecondsAfterFinished | string | `nil` | ttlSecondsAfterFinished for the cleanup Job; null falls through to the global default |
| spark.dependencies.hive.consulServiceName | string | `"hive"` |  |
| spark.dependencies.hive.consulServiceTag | string | `"metastore"` |  |
| spark.dependencies.hive.port | int | `9083` |  |
| spark.dependencies.namenode.consulServiceName | string | `"namenode"` |  |
| spark.dependencies.namenode.consulServiceTag | string | `"rpc"` |  |
| spark.dependencies.namenode.port | int | `8020` |  |
| spark.dependencies.prometheusPushgateway.consulServiceName | string | `"prometheus"` |  |
| spark.dependencies.prometheusPushgateway.consulServiceTag | string | `"pushgateway"` |  |
| spark.dependencies.prometheusPushgateway.port | int | `9091` |  |
| spark.dependencies.prometheusPushgateway.protocol | string | `"http"` |  |
| spark.historyServer | object | `{"certsDir":"/srv/hops/super_crypto/spark","cleaner":{"enabled":true,"interval":"1d","maxAge":"7d"},"deploymentName":"spark-history-server-deployment","hadoopHome":"/srv/hops/hadoop","image":{"pullPolicy":"Always","repository":"sparkhistoryserver","tag":"4.1.3.0"},"name":"spark-history-server","nodeSelector":{},"probes":{"liveness":{"failureThreshold":10,"httpGet":{"path":"/","port":"http","scheme":"HTTPS"},"initialDelaySeconds":8,"periodSeconds":5,"timeoutSeconds":10},"readiness":{"failureThreshold":10,"httpGet":{"path":"/","port":"http","scheme":"HTTPS"},"initialDelaySeconds":8,"periodSeconds":5,"timeoutSeconds":10}},"replicaCount":1,"resources":{"limits":{"cpu":"2000m","memory":"3Gi"},"requests":{"cpu":"500m","memory":"1Gi"}},"service":{"annotations":{"consul.hashicorp.com/service-name":"sparkhistoryserver"},"externalPort":80,"internalPort":18080,"name":"sparkhistoryserver","type":"ClusterIP"},"sparkHome":"/srv/hops/spark","tolerations":[],"topologySpreadConstraint":{}}` | The configuration for the Spark history server |
| spark.historyServer.nodeSelector | object | `{}` | node selector configuration |
| spark.historyServer.topologySpreadConstraint | object | `{}` | The default topology spread constraint. If not defined the global topology spread constraint would be used instead. |
| spark.hopsworkslib | object | `{}` | override hopsworkslib values |
| spark.rss | object | `{"appName":"rss-hops","configDir":"/data/rssadmin/rss/conf","configmap":{"name":"rss-configuration"},"controller":{"containerPort":9876,"image":"rss-controller","replicas":1,"resources":{"limits":{"cpu":"1","memory":"512Mi"},"requests":{"cpu":"100m","memory":"150Mi"}},"serviceAccount":{"annotations":{}}},"coordinator":{"count":2,"dynamicClientConfigMapName":"rss-dynamic-client-configuration","dynamicClientConfigMountPath":"/tmp","httpPort":19996,"labels":{"role":"rss-hops-coordinator"},"replicas":1,"resources":{"limits":{"cpu":"500m","memory":"2Gi"},"requests":{"cpu":"500m"}},"rpcPort":19997,"xmxSizeMemoryExtraPercentage":30},"dashboard":{"enabled":false,"httpPort":19997,"name":"uniffle-dashboard","resources":{"limits":{"cpu":"500m","memory":"2Gi"},"requests":{"cpu":"250m"}},"xmxSizeMemoryExtraPercentage":30},"dynamicClient":{"readBufferSize":"14m","storageType":"MEMORY_LOCALFILE"},"fullnameOverride":null,"image":{"image":"rss","initImage":"hops-rss-init","initImageVersion":"0.9.2","pullPolicy":"Always"},"namespaceSelector":"","nodeSelector":{},"resources":{"jobs":{"limits":{"cpu":"200m"}},"rss":{"limits":{"cpu":"500m","memory":"1Gi"}}},"serviceAccount":{"annotations":{}},"shuffleServer":{"bufferCapacity":-1,"bufferCapacityRatio":0.6,"diskCapacity":-1,"diskCapacityRatio":0.8,"httpPort":19998,"nettyPort":20000,"readBufferCapacity":-1,"readBufferCapacityRatio":0.1,"replicas":3,"resources":{"limits":{"cpu":"2000m","memory":"3Gi"},"requests":{"cpu":"200m"}},"rpcPort":19999,"upgradeStrategy":"FullUpgrade"},"storage":{"size":"10Gi","storageClassName":null,"volumeNameTemplate":"rss-storage"},"tolerations":[],"topologySpreadConstraint":{},"ttlSecondsAfterFinished":null,"version":"0.11.1","webhook":{"app":"rss-webhook","resources":{"limits":{"cpu":"1","memory":"512Mi"},"requests":{"cpu":"100m","memory":"150Mi"}},"service":{"name":"rss-webhook","port":443,"targetPort":9876}},"webhookName":"rss-webhook"}` | The configuration for the uniffle remote shuffle service |
| spark.rss.controller.serviceAccount.annotations | object | `{}` | service account annotations |
| spark.rss.coordinator.resources.requests | object | `{"cpu":"500m"}` | memory is set to be equal to the limit  |
| spark.rss.dashboard.resources.requests | object | `{"cpu":"250m"}` | memory is set to be equal to the limit  |
| spark.rss.fullnameOverride | string | `nil` | fullnameOverride |
| spark.rss.namespaceSelector | string | `""` | Label selector (key=value or key1=value1,key2=value2) for namespaces this instance should manage. Only events from matching namespaces will be processed by the controller and webhook. If empty, all namespaces are managed. |
| spark.rss.nodeSelector | object | `{}` | node selector configuration |
| spark.rss.resources.jobs | object | `{"limits":{"cpu":"200m"}}` | jobs resources |
| spark.rss.resources.rss | object | `{"limits":{"cpu":"500m","memory":"1Gi"}}` | rss resources |
| spark.rss.serviceAccount.annotations | object | `{}` | service account annotations |
| spark.rss.shuffleServer.resources.requests | object | `{"cpu":"200m"}` | memory is set to be equal to the limit  |
| spark.rss.storage.storageClassName | string | `nil` | storage class name to request for volumes attached to rss |
| spark.rss.topologySpreadConstraint | object | `{}` | The default topology spread constraint. If not defined the global topology spread constraint would be used instead. |
| spark.rss.ttlSecondsAfterFinished | string | `nil` | TTL in seconds for the rss-config Job. Overrides global default. |
| spark.rss.webhookName | string | `"rss-webhook"` | Name of the MutatingWebhookConfiguration and ValidatingWebhookConfiguration. Override when running multiple instances on the same cluster to avoid name collisions. |
| spark.spark-operator | object | `{"certManager":{"duration":"","enable":false,"issuerRef":{},"renewBefore":""},"commonLabels":{},"controller":{"affinity":{},"annotations":{},"batchScheduler":{"default":"","enable":false,"kubeSchedulerNames":[]},"driverPodCreationGracePeriod":"10s","env":[],"envFrom":[],"labels":{},"leaderElection":{"enable":true},"logLevel":"info","maxTrackedExecutorPerApp":1000,"nodeSelector":{},"podDisruptionBudget":{"enable":false,"minAvailable":1},"podSecurityContext":{"fsGroup":185},"pprof":{"enable":false,"port":6060,"portName":"pprof"},"priorityClassName":"","rbac":{"annotations":{},"create":true},"replicas":1,"resources":{"requests":{"cpu":"300m","memory":"512Mi"}},"securityContext":{"allowPrivilegeEscalation":false,"capabilities":{"drop":["ALL"]},"privileged":false,"readOnlyRootFilesystem":true,"runAsNonRoot":true,"seccompProfile":{"type":"RuntimeDefault"}},"serviceAccount":{"annotations":{},"automountServiceAccountToken":true,"create":true,"name":""},"sidecars":[],"tolerations":[],"topologySpreadConstraints":[],"uiIngress":{"annotations":{},"enable":false,"ingressClassName":"","tls":[],"urlFormat":""},"uiService":{"enable":true},"volumeMounts":[{"mountPath":"/tmp","name":"tmp","readOnly":false}],"volumes":[{"emptyDir":{"sizeLimit":"1Gi"},"name":"tmp"}],"workers":10,"workqueueRateLimiter":{"bucketQPS":50,"bucketSize":500,"maxDelay":{"duration":"6h","enable":true}}},"fullnameOverride":"","hook":{"affinity":{},"image":{"registry":"docker.hops.works","repository":"hopsworks/spark-operator-crds","tag":"2.5.1-h1-1.9"},"nodeSelector":{},"tolerations":[],"upgradeCrd":true},"image":{"pullPolicy":"IfNotPresent","pullSecrets":[],"registry":"docker.hops.works","repository":"hopsworks/spark-operator","tag":"2.5.1-h1"},"nameOverride":"","podSecurityContext":{"fsGroup":185,"runAsGroup":185,"runAsNonRoot":true,"runAsUser":185,"seccompProfile":{"type":"RuntimeDefault"}},"prometheus":{"metrics":{"enable":true,"endpoint":"/metrics","jobStartLatencyBuckets":"30,60,90,120,150,180,210,240,270,300","port":8080,"portName":"metrics","prefix":""},"podMonitor":{"create":false,"jobLabel":"spark-operator-podmonitor","labels":{},"podMetricsEndpoint":{"interval":"5s","scheme":"http"}}},"securityContext":{"allowPrivilegeEscalation":false,"capabilities":{"drop":["ALL"]},"runAsGroup":185,"runAsNonRoot":true,"runAsUser":185,"seccompProfile":{"type":"RuntimeDefault"}},"spark":{"jobNamespaces":[],"rbac":{"annotations":{},"create":true},"serviceAccount":{"annotations":{},"automountServiceAccountToken":true,"create":true,"name":""}},"webhook":{"affinity":{},"annotations":{},"enable":true,"env":[],"envFrom":[],"failurePolicy":"Fail","labels":{},"leaderElection":{"enable":true},"logLevel":"info","nodeSelector":{},"podDisruptionBudget":{"enable":false,"minAvailable":1},"podSecurityContext":{"fsGroup":185},"port":9443,"portName":"webhook","priorityClassName":"","rbac":{"annotations":{},"create":true},"replicas":1,"resourceQuotaEnforcement":{"enable":false},"resources":{"requests":{"cpu":"300m","memory":"512Mi"}},"securityContext":{"allowPrivilegeEscalation":false,"capabilities":{"drop":["ALL"]},"privileged":false,"readOnlyRootFilesystem":true,"runAsNonRoot":true,"seccompProfile":{"type":"RuntimeDefault"}},"serviceAccount":{"annotations":{},"automountServiceAccountToken":true,"create":true,"name":""},"sidecars":[],"timeoutSeconds":10,"tolerations":[],"topologySpreadConstraints":[],"volumeMounts":[{"mountPath":"/etc/k8s-webhook-server/serving-certs","name":"serving-certs","readOnly":false,"subPath":"serving-certs"},{"mountPath":"/tmp","name":"tmp"}],"volumes":[{"emptyDir":{"sizeLimit":"500Mi"},"name":"serving-certs"},{"emptyDir":{},"name":"tmp"}]}}` | override spark operator values |
| spark.spark-operator.certManager.duration | string | `2160h` (90 days) will be used if not specified. | The duration of the certificate validity (e.g. `2160h`). See [cert-manager.io/v1.Certificate](https://cert-manager.io/docs/reference/api-docs/#cert-manager.io/v1.Certificate). |
| spark.spark-operator.certManager.enable | bool | `false` | Specifies whether to use [cert-manager](https://cert-manager.io) to generate certificate for webhook. `webhook.enable` must be set to `true` to enable cert-manager. |
| spark.spark-operator.certManager.issuerRef | object | A self-signed issuer will be created and used if not specified. | The reference to the issuer. |
| spark.spark-operator.certManager.renewBefore | string | 1/3 of issued certificate’s lifetime. | The duration before the certificate expiration to renew the certificate (e.g. `720h`). See [cert-manager.io/v1.Certificate](https://cert-manager.io/docs/reference/api-docs/#cert-manager.io/v1.Certificate). |
| spark.spark-operator.commonLabels | object | `{}` | Common labels to add to the resources. |
| spark.spark-operator.controller.affinity | object | `{}` | Affinity for controller pods. |
| spark.spark-operator.controller.annotations | object | `{}` | Extra annotations for controller pods. |
| spark.spark-operator.controller.batchScheduler.default | string | `""` | Default batch scheduler to be used if not specified by the user. If specified, this value must be either "volcano" or "yunikorn". Specifying any other value will cause the controller to error on startup. |
| spark.spark-operator.controller.batchScheduler.enable | bool | `false` | Specifies whether to enable batch scheduler for spark jobs scheduling. If enabled, users can specify batch scheduler name in spark application. |
| spark.spark-operator.controller.batchScheduler.kubeSchedulerNames | list | `[]` | Specifies a list of kube-scheduler names for scheduling Spark pods. |
| spark.spark-operator.controller.driverPodCreationGracePeriod | string | `"10s"` | Grace period after a successful spark-submit when driver pod not found errors will be retried. Useful if the driver pod can take some time to be created. |
| spark.spark-operator.controller.env | list | `[]` | Environment variables for controller containers. |
| spark.spark-operator.controller.envFrom | list | `[]` | Environment variable sources for controller containers. |
| spark.spark-operator.controller.labels | object | `{}` | Extra labels for controller pods. |
| spark.spark-operator.controller.leaderElection.enable | bool | `true` | Specifies whether to enable leader election for controller. |
| spark.spark-operator.controller.logLevel | string | `"info"` | Configure the verbosity of logging, can be one of `debug`, `info`, `error`. |
| spark.spark-operator.controller.maxTrackedExecutorPerApp | int | `1000` | Specifies the maximum number of Executor pods that can be tracked by the controller per SparkApplication. |
| spark.spark-operator.controller.nodeSelector | object | `{}` | Node selector for controller pods. |
| spark.spark-operator.controller.podDisruptionBudget.enable | bool | `false` | Specifies whether to create pod disruption budget for controller. Ref: [Specifying a Disruption Budget for your Application](https://kubernetes.io/docs/tasks/run-application/configure-pdb/) |
| spark.spark-operator.controller.podDisruptionBudget.minAvailable | int | `1` | The number of pods that must be available. Require `controller.replicas` to be greater than 1 |
| spark.spark-operator.controller.podSecurityContext | object | `{"fsGroup":185}` | Security context for controller pods. |
| spark.spark-operator.controller.pprof.enable | bool | `false` | Specifies whether to enable pprof. |
| spark.spark-operator.controller.pprof.port | int | `6060` | Specifies pprof port. |
| spark.spark-operator.controller.pprof.portName | string | `"pprof"` | Specifies pprof service port name. |
| spark.spark-operator.controller.priorityClassName | string | `""` | Priority class for controller pods. |
| spark.spark-operator.controller.rbac.annotations | object | `{}` | Extra annotations for the controller RBAC resources. |
| spark.spark-operator.controller.rbac.create | bool | `true` | Specifies whether to create RBAC resources for the controller. |
| spark.spark-operator.controller.replicas | int | `1` | Number of replicas of controller. |
| spark.spark-operator.controller.resources | object | `{"requests":{"cpu":"300m","memory":"512Mi"}}` | Pod resource requests and limits for controller containers. Note, that each job submission will spawn a JVM within the controller pods using "/usr/local/openjdk-11/bin/java -Xmx128m". Kubernetes may kill these Java processes at will to enforce resource limits. When that happens, you will see the following error: 'failed to run spark-submit for SparkApplication \[...\]: signal: killed' - when this happens, you may want to increase memory limits. |
| spark.spark-operator.controller.securityContext | object | `{"allowPrivilegeEscalation":false,"capabilities":{"drop":["ALL"]},"privileged":false,"readOnlyRootFilesystem":true,"runAsNonRoot":true,"seccompProfile":{"type":"RuntimeDefault"}}` | Security context for controller containers. |
| spark.spark-operator.controller.serviceAccount.annotations | object | `{}` | Extra annotations for the controller service account. |
| spark.spark-operator.controller.serviceAccount.automountServiceAccountToken | bool | `true` | Auto-mount service account token to the controller pods. |
| spark.spark-operator.controller.serviceAccount.create | bool | `true` | Specifies whether to create a service account for the controller. |
| spark.spark-operator.controller.serviceAccount.name | string | `""` | Optional name for the controller service account. |
| spark.spark-operator.controller.sidecars | list | `[]` | Sidecar containers for controller pods. |
| spark.spark-operator.controller.tolerations | list | `[]` | List of node taints to tolerate for controller pods. |
| spark.spark-operator.controller.topologySpreadConstraints | list | `[]` | Topology spread constraints rely on node labels to identify the topology domain(s) that each Node is in. Ref: [Pod Topology Spread Constraints](https://kubernetes.io/docs/concepts/workloads/pods/pod-topology-spread-constraints/). The labelSelector field in topology spread constraint will be set to the selector labels for controller pods if not specified. |
| spark.spark-operator.controller.uiIngress.annotations | object | `{}` | Optionally set default ingress annotations for the Spark UI's ingress. `ingressAnnotations` in the SparkApplication spec overrides this. |
| spark.spark-operator.controller.uiIngress.enable | bool | `false` | Specifies whether to create ingress for Spark web UI. `controller.uiService.enable` must be `true` to enable ingress. |
| spark.spark-operator.controller.uiIngress.ingressClassName | string | `""` | Optionally set the ingressClassName. |
| spark.spark-operator.controller.uiIngress.tls | list | `[]` | Optionally set default TLS configuration for the Spark UI's ingress. `ingressTLS` in the SparkApplication spec overrides this. |
| spark.spark-operator.controller.uiIngress.urlFormat | string | `""` | Ingress URL format. Required if `controller.uiIngress.enable` is true. |
| spark.spark-operator.controller.uiService.enable | bool | `true` | Specifies whether to create service for Spark web UI. |
| spark.spark-operator.controller.volumeMounts | list | `[{"mountPath":"/tmp","name":"tmp","readOnly":false}]` | Volume mounts for controller containers. |
| spark.spark-operator.controller.volumes | list | `[{"emptyDir":{"sizeLimit":"1Gi"},"name":"tmp"}]` | Volumes for controller pods. |
| spark.spark-operator.controller.workers | int | `10` | Reconcile concurrency, higher values might increase memory usage. |
| spark.spark-operator.controller.workqueueRateLimiter.bucketQPS | int | `50` | Specifies the average rate of items process by the workqueue rate limiter. |
| spark.spark-operator.controller.workqueueRateLimiter.bucketSize | int | `500` | Specifies the maximum number of items that can be in the workqueue at any given time. |
| spark.spark-operator.controller.workqueueRateLimiter.maxDelay.duration | string | `"6h"` | Specifies the maximum delay duration for the workqueue rate limiter. |
| spark.spark-operator.controller.workqueueRateLimiter.maxDelay.enable | bool | `true` | Specifies whether to enable max delay for the workqueue rate limiter. This is useful to avoid losing events when the workqueue is full. |
| spark.spark-operator.fullnameOverride | string | `""` | String to fully override release name. |
| spark.spark-operator.hook.affinity | object | `{}` | Affinity for the Helm hook Job. |
| spark.spark-operator.hook.image.registry | string | `"docker.hops.works"` | Image registry. |
| spark.spark-operator.hook.image.repository | string | `"hopsworks/spark-operator-crds"` | Image repository. |
| spark.spark-operator.hook.image.tag | string | If not set, the chart appVersion will be used. | Image tag. |
| spark.spark-operator.hook.nodeSelector | object | `{}` | Node selector for the Helm hook Job. |
| spark.spark-operator.hook.tolerations | list | `[]` | List of node taints to tolerate for the Helm hook Job. |
| spark.spark-operator.hook.upgradeCrd | bool | `true` | Whether to create a Helm pre-install/pre-upgrade hook Job to update CRDs. |
| spark.spark-operator.image.pullPolicy | string | `"IfNotPresent"` | Image pull policy. |
| spark.spark-operator.image.pullSecrets | list | `[]` | Image pull secrets for private image registry. |
| spark.spark-operator.image.registry | string | `"docker.hops.works"` | Image registry. |
| spark.spark-operator.image.repository | string | `"hopsworks/spark-operator"` | Image repository. |
| spark.spark-operator.image.tag | string | If not set, the chart appVersion will be used. | Image tag. |
| spark.spark-operator.nameOverride | string | `""` | String to partially override release name. |
| spark.spark-operator.podSecurityContext | object | `{"fsGroup":185,"runAsGroup":185,"runAsNonRoot":true,"runAsUser":185,"seccompProfile":{"type":"RuntimeDefault"}}` | Pod-level security context for spark-operator |
| spark.spark-operator.prometheus.metrics.enable | bool | `true` | Specifies whether to enable prometheus metrics scraping. |
| spark.spark-operator.prometheus.metrics.endpoint | string | `"/metrics"` | Metrics serving endpoint. |
| spark.spark-operator.prometheus.metrics.jobStartLatencyBuckets | string | `"30,60,90,120,150,180,210,240,270,300"` | Job Start Latency histogram buckets. Specified in seconds. |
| spark.spark-operator.prometheus.metrics.port | int | `8080` | Metrics port. |
| spark.spark-operator.prometheus.metrics.portName | string | `"metrics"` | Metrics port name. |
| spark.spark-operator.prometheus.metrics.prefix | string | `""` | Metrics prefix, will be added to all exported metrics. |
| spark.spark-operator.prometheus.podMonitor.create | bool | `false` | Specifies whether to create pod monitor. Note that prometheus metrics should be enabled as well. |
| spark.spark-operator.prometheus.podMonitor.jobLabel | string | `"spark-operator-podmonitor"` | The label to use to retrieve the job name from |
| spark.spark-operator.prometheus.podMonitor.labels | object | `{}` | Pod monitor labels |
| spark.spark-operator.prometheus.podMonitor.podMetricsEndpoint | object | `{"interval":"5s","scheme":"http"}` | Prometheus metrics endpoint properties. `metrics.portName` will be used as a port |
| spark.spark-operator.securityContext | object | `{"allowPrivilegeEscalation":false,"capabilities":{"drop":["ALL"]},"runAsGroup":185,"runAsNonRoot":true,"runAsUser":185,"seccompProfile":{"type":"RuntimeDefault"}}` | Container-level security context for spark-operator |
| spark.spark-operator.spark.jobNamespaces | list | `[]` | List of namespaces where to run spark jobs. If empty string is included, all namespaces will be allowed. Make sure the namespaces have already existed. |
| spark.spark-operator.spark.rbac.annotations | object | `{}` | Optional annotations for the spark application RBAC resources. |
| spark.spark-operator.spark.rbac.create | bool | `true` | Specifies whether to create RBAC resources for spark applications. |
| spark.spark-operator.spark.serviceAccount.annotations | object | `{}` | Optional annotations for the spark service account. |
| spark.spark-operator.spark.serviceAccount.automountServiceAccountToken | bool | `true` | Auto-mount service account token to the spark applications pods. |
| spark.spark-operator.spark.serviceAccount.create | bool | `true` | Specifies whether to create a service account for spark applications. |
| spark.spark-operator.spark.serviceAccount.name | string | `""` | Optional name for the spark service account. |
| spark.spark-operator.webhook.affinity | object | `{}` | Affinity for webhook pods. |
| spark.spark-operator.webhook.annotations | object | `{}` | Extra annotations for webhook pods. |
| spark.spark-operator.webhook.enable | bool | `true` | Specifies whether to enable webhook. |
| spark.spark-operator.webhook.env | list | `[]` | Environment variables for webhook containers. |
| spark.spark-operator.webhook.envFrom | list | `[]` | Environment variable sources for webhook containers. |
| spark.spark-operator.webhook.failurePolicy | string | `"Fail"` | Specifies how unrecognized errors are handled. Available options are `Ignore` or `Fail`. |
| spark.spark-operator.webhook.labels | object | `{}` | Extra labels for webhook pods. |
| spark.spark-operator.webhook.leaderElection.enable | bool | `true` | Specifies whether to enable leader election for webhook. |
| spark.spark-operator.webhook.logLevel | string | `"info"` | Configure the verbosity of logging, can be one of `debug`, `info`, `error`. |
| spark.spark-operator.webhook.nodeSelector | object | `{}` | Node selector for webhook pods. |
| spark.spark-operator.webhook.podDisruptionBudget.enable | bool | `false` | Specifies whether to create pod disruption budget for webhook. Ref: [Specifying a Disruption Budget for your Application](https://kubernetes.io/docs/tasks/run-application/configure-pdb/) |
| spark.spark-operator.webhook.podDisruptionBudget.minAvailable | int | `1` | The number of pods that must be available. Require `webhook.replicas` to be greater than 1 |
| spark.spark-operator.webhook.podSecurityContext | object | `{"fsGroup":185}` | Security context for webhook pods. |
| spark.spark-operator.webhook.port | int | `9443` | Specifies webhook port. |
| spark.spark-operator.webhook.portName | string | `"webhook"` | Specifies webhook service port name. |
| spark.spark-operator.webhook.priorityClassName | string | `""` | Priority class for webhook pods. |
| spark.spark-operator.webhook.rbac.annotations | object | `{}` | Extra annotations for the webhook RBAC resources. |
| spark.spark-operator.webhook.rbac.create | bool | `true` | Specifies whether to create RBAC resources for the webhook. |
| spark.spark-operator.webhook.replicas | int | `1` | Number of replicas of webhook server. |
| spark.spark-operator.webhook.resourceQuotaEnforcement.enable | bool | `false` | Specifies whether to enable the ResourceQuota enforcement for SparkApplication resources. |
| spark.spark-operator.webhook.resources | object | `{"requests":{"cpu":"300m","memory":"512Mi"}}` | Pod resource requests and limits for webhook pods. |
| spark.spark-operator.webhook.securityContext | object | `{"allowPrivilegeEscalation":false,"capabilities":{"drop":["ALL"]},"privileged":false,"readOnlyRootFilesystem":true,"runAsNonRoot":true,"seccompProfile":{"type":"RuntimeDefault"}}` | Security context for webhook containers. |
| spark.spark-operator.webhook.serviceAccount.annotations | object | `{}` | Extra annotations for the webhook service account. |
| spark.spark-operator.webhook.serviceAccount.automountServiceAccountToken | bool | `true` | Auto-mount service account token to the webhook pods. |
| spark.spark-operator.webhook.serviceAccount.create | bool | `true` | Specifies whether to create a service account for the webhook. |
| spark.spark-operator.webhook.serviceAccount.name | string | `""` | Optional name for the webhook service account. |
| spark.spark-operator.webhook.sidecars | list | `[]` | Sidecar containers for webhook pods. |
| spark.spark-operator.webhook.timeoutSeconds | int | `10` | Specifies the timeout seconds of the webhook, the value must be between 1 and 30. |
| spark.spark-operator.webhook.tolerations | list | `[]` | List of node taints to tolerate for webhook pods. |
| spark.spark-operator.webhook.topologySpreadConstraints | list | `[]` | Topology spread constraints rely on node labels to identify the topology domain(s) that each Node is in. Ref: [Pod Topology Spread Constraints](https://kubernetes.io/docs/concepts/workloads/pods/pod-topology-spread-constraints/). The labelSelector field in topology spread constraint will be set to the selector labels for webhook pods if not specified. |
| spark.spark-operator.webhook.volumeMounts | list | `[{"mountPath":"/etc/k8s-webhook-server/serving-certs","name":"serving-certs","readOnly":false,"subPath":"serving-certs"},{"mountPath":"/tmp","name":"tmp"}]` | Volume mounts for webhook containers. |
| spark.spark-operator.webhook.volumes | list | `[{"emptyDir":{"sizeLimit":"500Mi"},"name":"serving-certs"},{"emptyDir":{},"name":"tmp"}]` | Volumes for webhook pods. |
| spark.sparkJobDebugLevel | string | `"INFO"` |  |
| spark.sparkOperatorUpgradeJob | object | `{"crdImage":{"repository":"spark-operator-crds","tag":"2.2.1-1.4"},"imagePullPolicy":"Always","leaderElectionLockName":"spark-operator-lock","leaderElectionLockNamespace":"","name":"spark-operator-upgrade-job","nodeSelector":{},"podMonitorName":"spark-operator-podmonitor","resources":{"limits":{"cpu":"200m","memory":"200M"},"requests":{"cpu":"100m","memory":"100M"}},"serviceAccount":{"annotations":{}},"sparkJobNamespace":"","tolerations":[]}` | Job configuration to clean up old spark-operator resources before upgrading. |
| spark.sparkOperatorUpgradeJob.crdImage | object | `{"repository":"spark-operator-crds","tag":"2.2.1-1.4"}` | Image for the pre-upgrade Job. Must ship the spark-operator CRDs at `/opt/spark-operator-crds/` and provide `bash` and `kubectl`. |
| spark.sparkOperatorUpgradeJob.leaderElectionLockName | string | `"spark-operator-lock"` | Leader election lease name used by the old chart (only if replicaCount > 1). |
| spark.sparkOperatorUpgradeJob.leaderElectionLockNamespace | string | `""` | Optional leader election lease namespace (defaults to release namespace). |
| spark.sparkOperatorUpgradeJob.nodeSelector | object | `{}` | node selector configuration |
| spark.sparkOperatorUpgradeJob.podMonitorName | string | `"spark-operator-podmonitor"` | PodMonitor name used by the old chart (only if enabled). |
| spark.sparkOperatorUpgradeJob.serviceAccount.annotations | object | `{}` | service account annotations |
| spark.sparkOperatorUpgradeJob.sparkJobNamespace | string | `""` | Namespace where spark app RBAC/SA were created by the old chart. |
| spark.sql | object | `{"ansiEnabled":false}` | Spark SQL defaults applied cluster-wide through `spark-defaults.conf`. |
| spark.sql.ansiEnabled | bool | `false` | Whether to enable ANSI SQL mode (`spark.sql.ansi.enabled`). Spark 4 changed the upstream default to `true`, which turns arithmetic overflow and invalid casts into runtime errors instead of returning `null`. Hopsworks pins it to `false` so SQL that ran on Spark 3.x keeps the same semantics after the upgrade. Set to `true` to opt in to standards-compliant behavior cluster-wide; individual jobs can still override `spark.sql.ansi.enabled` themselves. |
| superset.auth.adminUserSecret | string | `"superset-admin-credentials"` |  |
| superset.auth.adminUsername | string | `"adminuser"` |  |
| superset.auth.createSecretEnvs | bool | `true` |  |
| superset.auth.createSecrets | bool | `true` |  |
| superset.auth.mysqlUserSecretName | string | `"superset-mysql-users-secrets"` |  |
| superset.auth.secretKeySecretName | string | `"superset-secret-key"` |  |
| superset.backups | object | `{"activeDeadlineSeconds":3600,"backoffLimit":1,"enabled":true,"pathPrefix":"superset_backup","schedule":null,"tmpSizeLimit":"2Gi","ttl":null,"ttlSecondsAfterFinished":null}` | Superset MySQL backup (HWORKS-2973): a scheduled logical mysqldump of the `superset` schema to the platform object store (same bucket as the other backups), plus an authoritative manifest and a Velero-captured metadata index. Rendered only when global._hopsworks.backups.enabled is true and an object store is configured. |
| superset.backups.activeDeadlineSeconds | int | `3600` | activeDeadlineSeconds for the backup Job; bounds a hung run so it cannot block later schedules under concurrencyPolicy Forbid, and bounds the dump and upload |
| superset.backups.backoffLimit | int | `1` | backoffLimit for the backup Job |
| superset.backups.enabled | bool | `true` | enable the scheduled Superset database backup CronJob |
| superset.backups.pathPrefix | string | `"superset_backup"` | object-path prefix within the backup bucket |
| superset.backups.schedule | string | `nil` | backup schedule (cron or @weekly). null inherits global._hopsworks.backups.schedule, else @weekly |
| superset.backups.tmpSizeLimit | string | `"2Gi"` | size limit for the temporary dump volume and the container ephemeral-storage request/limit |
| superset.backups.ttl | string | `nil` | retention (Go duration, e.g. 60d) for pruning whole backup sets older than the value. null inherits the global setting |
| superset.backups.ttlSecondsAfterFinished | string | `nil` | ttlSecondsAfterFinished for finished backup Job pods (removes the pod, and its node-local dump scratch, after completion). null falls through to the global default |
| superset.cleanupOnUninstall | object | `{"enabled":true,"ttlSecondsAfterFinished":null}` | post-delete cleanup of the Superset MySQL data PVC for existing clusters whose StatefulSet predates the persistentVolumeClaimRetentionPolicy fix. Gated by global._hopsworks.wipeDataOnUninstall and honors the hopsworks.ai/keep=true label, like the other data-PVC teardowns. New clusters clean up natively via the retention policy (which deletes unconditionally). |
| superset.cleanupOnUninstall.enabled | bool | `true` | enable the post-delete Superset MySQL PVC cleanup hook (also requires global._hopsworks.wipeDataOnUninstall) |
| superset.cleanupOnUninstall.ttlSecondsAfterFinished | string | `nil` | ttlSecondsAfterFinished for the cleanup Job; null falls through to the global default |
| superset.hopsworkslib | object | `{}` | override hopsworkslib values |
| superset.imageRegistry | string | `"docker.hops.works/superset"` |  |
| superset.mysql | object | `{"architecture":"standalone","auth":{"createDatabase":true,"customPasswordFiles":{},"database":"superset","existingSecret":"superset-mysql-users-secrets","password":"temp-value","replicationPassword":"","replicationUser":"replicator","rootPassword":"temp-value","usePasswordFiles":false,"username":"superset"},"enabled":true,"global":{"security":{"allowInsecureImages":true}},"image":{"digest":"","pullPolicy":"IfNotPresent","registry":"docker.hops.works/superset","repository":"mysql","tag":"8.4.11-ubuntu24.04-h4"},"metrics":{"enabled":true,"image":{"digest":"","pullPolicy":"IfNotPresent","registry":"docker.hops.works/superset","repository":"mysqld-exporter","tag":"0.20.0-alpine-h1.1"},"resources":{"limits":{"cpu":"100m","memory":"64Mi"},"requests":{"cpu":"50m","memory":"64Mi"}},"service":{"annotations":{"prometheus.io/port":"{{ .Values.metrics.service.port }}","prometheus.io/scrape":"true"}}},"primary":{"persistentVolumeClaimRetentionPolicy":{"enabled":true,"whenDeleted":"Delete","whenScaled":"Retain"}},"volumePermissions":{"enabled":false,"image":{"digest":"","pullPolicy":"IfNotPresent","registry":"docker.hops.works/superset","repository":"os-shell","tag":"12-alpine-h1.1"}}}` | override superset mysql values |
| superset.superset | object | `{"_publicRoleDefaultName":"Public","allowAnonymousAccess":true,"configOverrides":{"feature_flags":"FEATURE_FLAGS = {\"ALERT_REPORTS\": True, \"DASHBOARD_RBAC\": True}\n","flask_app_configuration":"from flask import session\nfrom flask import Flask\nfrom datetime import timedelta\n\ndef make_session_permanent():\n    '''\n    Enable maxAge for the cookie 'session'\n    '''\n    session.permanent = True\n\n# Set up max age of session to 24 hours\nPERMANENT_SESSION_LIFETIME = timedelta(hours=24) # (default: \"31 days\")\nSESSION_REFRESH_EACH_REQUEST = True # Default: True\ndef FLASK_APP_MUTATOR(app: Flask) -> None:\n    app.before_request_funcs.setdefault(None, []).append(make_session_permanent)\n","mysql":"SQLALCHEMY_DATABASE_URI = f\"mysql+mysqldb://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}\"\n","proxyConfig":"ENABLE_PROXY_FIX = True\nAPP_ICON = \"/hopsworks-api/superset/static/assets/images/superset-logo-horiz.png\"\nLOGO_TARGET_PATH = \"/hopsworks-api/superset/superset/welcome/\"\n{{- if .Values.init.loadExamples }}\nPREVENT_UNSAFE_DB_CONNECTIONS = False\n{{- else }}\nPREVENT_UNSAFE_DB_CONNECTIONS = True\n{{- end }}\n","public_role":"{{- if .Values.publicRoleLike }}\nPUBLIC_ROLE_LIKE = {{ .Values.publicRoleLike | quote }}\n{{- end }}\n{{- if .Values.allowAnonymousAccess }}\nAUTH_ROLE_PUBLIC = {{ .Values._publicRoleDefaultName | quote }}\n{{- end }}\n"},"extraEnv":{"SUPERSET_APP_ROOT":"/hopsworks-api/superset"},"extraEnvRaw":[{"name":"SUPERSET_USER","valueFrom":{"secretKeyRef":{"key":"username","name":"superset-admin-credentials"}}},{"name":"SUPERSET_PASS","valueFrom":{"secretKeyRef":{"key":"password","name":"superset-admin-credentials"}}},{"name":"DB_PASS","valueFrom":{"secretKeyRef":{"key":"mysql-password","name":"superset-mysql-users-secrets"}}},{"name":"SUPERSET_SECRET_KEY","valueFrom":{"secretKeyRef":{"key":"secret-key","name":"superset-secret-key"}}}],"extraRoles":[{"name":"Dataset","permissions":[["can_duplicate","Dataset"],["can_write","Dataset"],["can_get_or_create_dataset","Dataset"],["can_warm_up_cache","Dataset"]]}],"extraVolumeMounts":[{"mountPath":"/srv/hops/super_crypto/superset","name":"super-crypto-material","readOnly":true}],"extraVolumes":[{"name":"super-crypto-material","secret":{"optional":true,"secretName":"hopsworks-superset-crypto-material"}}],"fullnameOverride":"hopsworks-superset","image":{"pullPolicy":"IfNotPresent","repository":"docker.hops.works/hopsworks/superset","tag":"6.0.0p4.4"},"init":{"adminUser":{"email":"admin@superset.com","firstname":"Superset","lastname":"Admin","password":"$SUPERSET_PASS","username":"$SUPERSET_USER"},"command":["/bin/sh","-c","{{- if ((((.Values.global | default dict)._hopsworks | default dict).restoreFromBackup | default dict).superset | default dict).enabled }}\necho \"Superset restore in progress (global._hopsworks.restoreFromBackup.superset.enabled): skipping init so no schema work runs while the database is reloaded. It runs on the upgrade that clears the flag.\"; exit 0\n{{- end }}\n. {{ .Values.configMountPath }}/superset_bootstrap.sh; . {{ .Values.configMountPath }}/superset_init.sh;\n{{- if .Values.extraRoles }}\n{{- range $role := .Values.extraRoles }}\npython /scripts/create_role.py --role-name {{ $role.name }} --permissions '{{ $role.permissions | toJson | b64enc }}';\n{{- end }}\n{{- end }}\n{{- if and .Values.publicRolePermissions (eq .Values.publicRoleLike .Values._publicRoleDefaultName) }}\npython /scripts/create_role.py --role-name {{ .Values._publicRoleDefaultName }} --permissions '{{ .Values.publicRolePermissions | toJson | b64enc }}';\n{{- end }}\n"],"containerSecurityContext":{"allowPrivilegeEscalation":false,"capabilities":{"drop":["ALL"]}},"initContainers":[{"command":["/bin/sh","-c","dockerize -wait \"tcp://$DB_HOST:$DB_PORT\" -timeout 120s"],"envFrom":[{"secretRef":{"name":"{{ tpl .Values.envFromSecret . }}"}}],"image":"{{ .Values.initImage.repository }}:{{ .Values.initImage.tag }}","imagePullPolicy":"{{ .Values.initImage.pullPolicy }}","name":"wait-for-database","resources":{"limits":{"cpu":"500m","memory":"256Mi"},"requests":{"cpu":"250m","memory":"128Mi"}},"securityContext":{"allowPrivilegeEscalation":false,"capabilities":{"drop":["ALL"]}}}],"loadExamples":false,"podSecurityContext":{"runAsNonRoot":true,"seccompProfile":{"type":"RuntimeDefault"}}},"initImage":{"pullPolicy":"IfNotPresent","repository":"docker.hops.works/superset/dockerize","tag":"0.14.0-alpine-h1.1"},"postgresql":{"enabled":false},"publicRoleLike":"Public","publicRolePermissions":[["can_read","Dashboard"],["can_read","Chart"],["can_dashboard","Superset"],["can_slice","Superset"],["can_explore_json","Superset"],["can_dashboard_permalink","Superset"],["can_read","DashboardPermalinkRestApi"],["can_read","DashboardFilterStateRestApi"],["can_write","DashboardFilterStateRestApi"],["can_time_range","Api"],["can_query_form_data","Api"],["can_query","Api"],["can_read","CssTemplate"],["can_read","Theme"],["can_read","EmbeddedDashboard"],["can_read","CurrentUserRestApi"],["can_get","Datasource"],["can_external_metadata","Datasource"],["can_read","Annotation"],["can_read","AnnotationLayerRestApi"],["can_read","ExplorePermalinkRestApi"]],"redis":{"enabled":true,"image":{"registry":"docker.hops.works/superset","repository":"redis","tag":"7.4.11-alpine-h1"},"master":{"configuration":"maxmemory 256mb\nmaxmemory-policy allkeys-lru","containerSecurityContext":{"allowPrivilegeEscalation":false,"capabilities":{"drop":["ALL"]},"enabled":true,"readOnlyRootFilesystem":true,"runAsGroup":1001,"runAsNonRoot":true,"runAsUser":1001,"seLinuxOptions":{},"seccompProfile":{"type":"RuntimeDefault"}},"podSecurityContext":{"enabled":true,"fsGroup":1001,"fsGroupChangePolicy":"Always","runAsNonRoot":true,"runAsUser":1001,"seccompProfile":{"type":"RuntimeDefault"},"supplementalGroups":[],"sysctls":[]},"resources":{"limits":{"cpu":"500m","memory":"384Mi"},"requests":{"cpu":"100m","memory":"384Mi"}}},"metrics":{"containerSecurityContext":{"allowPrivilegeEscalation":false,"capabilities":{"drop":["ALL"]},"enabled":true,"readOnlyRootFilesystem":true,"runAsGroup":1001,"runAsNonRoot":true,"runAsUser":1001,"seLinuxOptions":{},"seccompProfile":{"type":"RuntimeDefault"}},"enabled":true,"image":{"digest":"","pullPolicy":"IfNotPresent","registry":"docker.hops.works/superset","repository":"redis-exporter","tag":"1.90.0-alpine-h1.1"},"resources":{"limits":{"cpu":"100m","memory":"64Mi"},"requests":{"cpu":"50m","memory":"64Mi"}},"service":{"annotations":{"prometheus.io/port":"{{ .Values.metrics.service.port }}","prometheus.io/scrape":"true"}}}},"runAsUser":1000,"secretEnv":{"create":false},"service":{"annotations":{"consul.hashicorp.com/service-name":"superset","consul.hashicorp.com/service-tags":"app"}},"supersetNode":{"connections":{"db_host":"{{ .Release.Name }}-mysql","db_name":"superset","db_pass":"superset","db_port":"3306","db_type":"mysql","db_user":"superset"},"containerSecurityContext":{"allowPrivilegeEscalation":false,"capabilities":{"drop":["ALL"]}},"initContainers":[{"command":["/bin/sh","-c","dockerize -wait \"tcp://$DB_HOST:$DB_PORT\" -timeout 120s"],"envFrom":[{"secretRef":{"name":"{{ tpl .Values.envFromSecret . }}"}}],"image":"{{ .Values.initImage.repository }}:{{ .Values.initImage.tag }}","imagePullPolicy":"{{ .Values.initImage.pullPolicy }}","name":"wait-for-db","resources":{"limits":{"cpu":"500m","memory":"256Mi"},"requests":{"cpu":"250m","memory":"128Mi"}},"securityContext":{"allowPrivilegeEscalation":false,"capabilities":{"drop":["ALL"]}}}],"livenessProbe":{"failureThreshold":3,"httpGet":{"path":"/hopsworks-api/superset/health","port":"http"},"initialDelaySeconds":15,"periodSeconds":15,"successThreshold":1,"timeoutSeconds":1},"podSecurityContext":{"runAsNonRoot":true,"seccompProfile":{"type":"RuntimeDefault"}},"readinessProbe":{"failureThreshold":3,"httpGet":{"path":"/hopsworks-api/superset/health","port":"http"},"initialDelaySeconds":15,"periodSeconds":15,"successThreshold":1,"timeoutSeconds":1},"replicas":{"enabled":true,"replicaCount":1},"startupProbe":{"failureThreshold":60,"httpGet":{"path":"/hopsworks-api/superset/health","port":"http"},"initialDelaySeconds":15,"periodSeconds":5,"successThreshold":1,"timeoutSeconds":1}},"supersetWorker":{"command":["/bin/sh","-c",". {{ .Values.configMountPath }}/superset_bootstrap.sh; celery --app=superset.tasks.celery_app:app worker --pool=prefork -O fair -c 4"],"containerSecurityContext":{"allowPrivilegeEscalation":false,"capabilities":{"drop":["ALL"]}},"initContainers":[{"command":["/bin/sh","-c","dockerize -wait \"tcp://$DB_HOST:$DB_PORT\" -wait \"tcp://$REDIS_HOST:$REDIS_PORT\" -timeout 120s"],"envFrom":[{"secretRef":{"name":"{{ tpl .Values.envFromSecret . }}"}}],"image":"{{ .Values.initImage.repository }}:{{ .Values.initImage.tag }}","imagePullPolicy":"{{ .Values.initImage.pullPolicy }}","name":"wait-for-db-redis","resources":{"limits":{"cpu":"500m","memory":"256Mi"},"requests":{"cpu":"250m","memory":"128Mi"}},"securityContext":{"allowPrivilegeEscalation":false,"capabilities":{"drop":["ALL"]}}}],"podSecurityContext":{"runAsNonRoot":true,"seccompProfile":{"type":"RuntimeDefault"}},"replicas":{"enabled":false},"resources":{"limits":{"cpu":"500m","memory":"1024Mi"},"requests":{"cpu":"500m","memory":"1024Mi"}}}}` | override superset values |
| superset.superset.fullnameOverride | string | `"hopsworks-superset"` | Provide a name to override the full names of resources |
| superset.superset.runAsUser | int | `1000` | User ID directive. This user must have enough permissions to run the bootstrap script Running containers as root is not recommended in production. Change this to another UID - e.g. 1000 to be more secure |
| trino.auth.adminUserPwd | string | `""` | Plaintext password for `adminUsername`, read by the backend and bcrypted into password.db by the seeder Job. Empty generates one on first install and reuses it from the existing Secret; empty in a non-auto mode fails the render, since the existing Secret cannot be read back. |
| trino.auth.adminUserPwdHash | string | `nil` | DEPRECATED, read by nothing: the seeder derives the hash from `adminUserPwd`. Kept so an existing override still validates. |
| trino.auth.adminUsername | string | `"trino"` | Trino admin username. Should not be changed. Used in hadoop.proxyuser.trino |
| trino.auth.createSecrets | bool | `true` | If createSecrets is false, you must manually create the following Kubernetes Secrets:   1. trino-admin-credentials (keys `username`, `password`): the backend's principal.   2. trino-monitoring-credentials (same keys): the principal Prometheus scrapes with. The seeder Job bcrypts both into password.db in HopsFS. Label both `backup.hops.works/include: "true"` so Velero captures them. In any non-auto `global._hopsworks.mode` (ArgoCD) the existing Secret cannot be read back, so the render fails unless both passwords below are set or this is false. |
| trino.auth.createSharedSecret | bool | `true` | If `createSharedSecret` is set to `false`, you must generate an `internal-communication.shared-secret` value and store it in a Kubernetes Secret named `trino-internal-secret` under the key `shared-secret`. trino-internal-secret is intentionally NOT captured by the Velero backup (it has no coupling to user state and is regenerated on a fresh install). With createSharedSecret=false it is operator-managed, so disaster recovery must restore it from an independent source, followed by a coordinated restart of all Trino pods so coordinator and workers share the same value. |
| trino.auth.monitoringUser | string | `"prometheus"` | Username used by Prometheus for scraping Trino metrics. If you override this value, you MUST also:   1. Update Trino access control to grant this user the required permissions      (e.g. adjust `accessControl.rules.rules.json` accordingly).   2. Update the Prometheus scrape configuration so that the same username is used:      set `.Values.prometheus.prometheus.serverFiles.prometheus.yml.scrape_configs[*].basic_auth.username`      for the scrape job with `job_name: "trino"` to match this value. |
| trino.auth.monitoringUserPwd | string | `""` | Plaintext password for `monitoringUser`, read by Prometheus and bcrypted into password.db. Generated like `adminUserPwd`. |
| trino.auth.monitoringUserPwdHash | string | `nil` | DEPRECATED, read by nothing, like `adminUserPwdHash`. |
| trino.authSeeder | object | `{"image":{"name":"hopsfs","registry":"","tag":"3.4.3.3-EE-RC0"},"ttlSecondsAfterFinished":3600,"waitSeconds":600}` | The Job that seeds password.db and group.db into HopsFS, and the pre-upgrade hook that migrates them from the legacy Secrets. Not optional: Trino cannot start without them. |
| trino.authSeeder.image | object | `{"name":"hopsfs","registry":"","tag":"3.4.3.3-EE-RC0"}` | The HopsFS client image. The seeder writes with `hdfs dfs`; the trino-files mount is read-only. |
| trino.authSeeder.image.name | string | `"hopsfs"` | Image name. |
| trino.authSeeder.image.registry | string | `""` | Full registry+path prefix, ending with `/`. Empty uses `global._hopsworks.imageRegistry` plus `/hopsworks/`, matching charts/hopsfs. |
| trino.authSeeder.image.tag | string | `"3.4.3.3-EE-RC0"` | Image tag. Keep in step with `hopsfs.image.tag` in charts/hopsfs/values.yaml. |
| trino.authSeeder.ttlSecondsAfterFinished | int | `3600` | Seconds to keep the finished Jobs; their logs record what was seeded. |
| trino.authSeeder.waitSeconds | int | `600` | Seconds the seeder waits for HopsFS before failing. |
| trino.catalogsConfigmapName | string | `"hopsworks-trino-catalogs"` |  |
| trino.dependencies.hive.consulServiceName | string | `"hive"` |  |
| trino.dependencies.hive.consulServiceTag | string | `"metastore"` |  |
| trino.dependencies.hive.port | int | `9083` |  |
| trino.dependencies.mysql.consulServiceName | string | `"mysql"` |  |
| trino.dependencies.mysql.port | int | `3306` |  |
| trino.externalLoadBalancer.annotations | object | `{}` | annotations for load balancer |
| trino.externalLoadBalancer.class | string | `nil` | load balancer class name |
| trino.externalLoadBalancer.enabled | string | `nil` | Enable External Load Balancers for the Trino coordinator/service. If not set the .global._hopsworks.externalLoadBalancers.enabled will be used instead |
| trino.externalLoadBalancer.managed | string | `nil` | Cloud provider provisions Load Balancers. If not set the .global._hopsworks.externalLoadBalancers.managed will be used instead |
| trino.externalLoadBalancer.nodeSelector | object | `{}` | selector for nodes the load balancer can use to route traffic |
| trino.hopsworkslib | object | `{}` | override hopsworkslib values |
| trino.trino | object | check \[values.yaml\](./values.yaml) for more information | override trino values |
| trino.trino.coordinator.additionalJVMConfig | list | `["--add-opens=java.base/java.nio=ALL-UNNAMED"]` | add-opens for java.nio, and the failure is a CONFIGURATION error raised while the catalog is being loaded. On this coordinator that is fatal rather than local, because Trino runs catalog.management=static and exits when a catalog file fails to load -- so one project's Snowflake catalog would stop the whole cluster from starting. Set here rather than left to the operator because the connector is in TRINO_CONNECTORS, i.e. the backend offers it to every project. Other Arrow-based connectors need the same opens, so this is not Snowflake-specific. |
| trino.trino.image.registry | string | `"docker.hops.works"` | Image registry, defaults to empty, which results in DockerHub usage |
| trino.trino.image.repository | string | `"hopsworks/trino"` | Repository location of the Trino image, typically `organization/imagename` |
| trino.trino.image.tag | string | `"483-v1"` | Image tag for the Trino image. This value is explicitly pinned here and overrides any defaulting to `appVersion` from Chart.yaml. |
| trino.trino.initContainers.coordinator\[2\].name | string | `"mountable-secrets"` | readOnly is not optional. Without it the query engine gains a write channel into HopsFS as the trino service user; the volume's readOnly makes the kernel refuse writes too. --srcDir bounds what the mount exposes to the backend-owned tree; the mount authenticates as trino, which is in the hdfs superuser group, so srcDir is the only thing containing it.  No preStop unmount: the node plugin owns the mount and unmounts it in NodeUnpublishVolume, and hopsfs-sidecar.sh exits on SIGTERM, so the container terminates cleanly on its own. |
| trino.trino.initContainers.worker\[1\].name | string | `"mountable-secrets"` | readOnly is not optional. Without it the query engine gains a write channel into HopsFS as the trino service user; the volume's readOnly makes the kernel refuse writes too. --srcDir bounds what the mount exposes to the backend-owned tree; the mount authenticates as trino, which is in the hdfs superuser group, so srcDir is the only thing containing it.  No preStop unmount: the node plugin owns the mount and unmounts it in NodeUnpublishVolume, and hopsfs-sidecar.sh exits on SIGTERM, so the container terminates cleanly on its own. |
| trino.trinotest | object | check \[values.yaml\](./values.yaml) for more information | override trinotest values. Rendered only when global._hopsworks.trino.testCoordinator.enabled is true (see Chart.yaml). An optional single-node coordinator running catalog.management=dynamic with a WRITABLE catalog dir, used by the backend to connection-test user catalogs (CREATE CATALOG / SHOW SCHEMAS / DROP CATALOG) before they are synced to the production coordinator. Mirrors the production coordinator's image, certs, TLS, and PASSWORD auth so the backend's admin credentials and discovery work identically. |
| trino.trinotest.initContainers.coordinator\[2\].name | string | `"mountable-secrets"` | readOnly is not optional. Without it the query engine gains a write channel into HopsFS as the trino service user; the volume's readOnly makes the kernel refuse writes too. --srcDir bounds what the mount exposes to the backend-owned tree; the mount authenticates as trino, which is in the hdfs superuser group, so srcDir is the only thing containing it.  No preStop unmount: the node plugin owns the mount and unmounts it in NodeUnpublishVolume, and hopsfs-sidecar.sh exits on SIGTERM, so the container terminates cleanly on its own. |
| vpa.allowOnlyOneReplica | bool | `true` | If true the vpa updater is configured to update resources even when only one replica is running |
| vpa.cleanupOnUninstall | object | `{"enabled":true,"ttlSecondsAfterFinished":null}` | post-delete cleanup of the VPA ConfigMap. cm.yaml defines `vpa` as a Helm hook with no delete-policy, so Helm never removes it; this deletes it by name on uninstall. |
| vpa.cleanupOnUninstall.enabled | bool | `true` | enable the post-delete VPA ConfigMap cleanup hook |
| vpa.cleanupOnUninstall.ttlSecondsAfterFinished | string | `nil` | ttlSecondsAfterFinished for the cleanup Job; null falls through to the global default |
| vpa.enablePrometheusRecommender | bool | `true` | If true the recommender will be connected to prometheus |
| vpa.enablePrometheusScrapper | bool | `true` | If true the vpa metrics will be connected to prometheus |
| vpa.enabled | bool | `true` |  |
| vpa.hopsworkslib | object | `{}` | override hopsworkslib values |
| vpa.image.name | string | `"k8s-vpa"` |  |
| vpa.image.tag | string | `"1.7.1-2"` | Installer toolbox version. Independent of imagesTag. |
| vpa.imagesTag | string | `"1.7.1"` | Upstream VPA release. Selects the admission-controller, recommender and updater images, and must match the VPA version the installer image was built from. Not tied to image.tag. |
| vpa.installController | bool | `true` | If true, install the VPA controller (CRDs, admission controller, recommender, updater). Set to false if VPA is already installed in the cluster. |
| vpa.recommenderSettings | object | `{"inRecommendationBoundsEvictionLifetimeThreshold":"12h","podUpdateThreshold":"0.1"}` | Recommender settings https://github.com/kubernetes/autoscaler/blob/5cd491a5a18b4b93f742351e3ebb195e358d2ea3/vertical-pod-autoscaler/pkg/updater/priority/update_priority_calculator.go#L36 |
| vpa.recommenderSettings.inRecommendationBoundsEvictionLifetimeThreshold | string | `"12h"` | The default value is 12h. This is the time needed to do a downscale |
| vpa.recommenderSettings.podUpdateThreshold | string | `"0.1"` | The default value is 0.1 Set to 0 to always update even if the recommendation is in bounds Notice it needs to be an string |
| vpa.teardownWhenInstalling | bool | `true` | If true, the vpa will be deleted if already installed |
| vpa.teardownWhenUninstall | bool | `true` | if true, the vpa will be deleted if already installed when doing helm uninstall |

<!-- END GENERATED VALUES -->
