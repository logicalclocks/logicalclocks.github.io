# Trino values { #helm-values-trino }

Values under `trino` configure Trino, the SQL query engine, and its test coordinator for user catalogs.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.2.0-alpha-1791477965` (Hopsworks `5.2.0`)._

Deployed according to the first of these values that is set: [`global._hopsworks.trino.enabled`](global.md#helm.global._hopsworks.trino.enabled), [`global._hopsworks.full_platform`](global.md#helm.global._hopsworks.full_platform).

!!! info "Upstream charts"

    - Values under `trino.trino` go to [`trino` 1.41.0](https://artifacthub.io/packages/helm/trino/trino/1.41.0) from `https://trinodb.github.io/charts`.
    - Values under `trino.trinotest` go to [`trino` 1.41.0](https://artifacthub.io/packages/helm/trino/trino/1.41.0) from `https://trinodb.github.io/charts`.

    Only the values Hopsworks sets under `trino.trino` and `trino.trinotest` are listed on this page.
    Any other value of the charts can be set under the same keys; each link opens the chart's documentation for the version Hopsworks pins.

## General { #helm-values-trino-general }

??? example "Defaults as YAML"

    ```yaml
    trino:
      catalogsConfigmapName: hopsworks-trino-catalogs
      hopsworkslib: {}
      trinotest:
        initContainers:
          coordinator:
          - null
          - null
          - name: mountable-secrets
    ```

<div class="hops-values" markdown>

`trino` <a class="headerlink" href="#helm.trino" title="Permanent link">#</a> { #helm.trino }
:   Type `object`, default `{}`.
    override trino values

`trino.catalogsConfigmapName` <a class="headerlink" href="#helm.trino.catalogsConfigmapName" title="Permanent link">#</a> { #helm.trino.catalogsConfigmapName }
:   Type `string`, default `"hopsworks-trino-catalogs"`.

`trino.hopsworkslib` <a class="headerlink" href="#helm.trino.hopsworkslib" title="Permanent link">#</a> { #helm.trino.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`trino.trinotest` <a class="headerlink" href="#helm.trino.trinotest" title="Permanent link">#</a> { #helm.trino.trinotest }
:   Type `object`, default check \[values.yaml\](./values.yaml) for more information, passed to the [`trino` 1.41.0](https://artifacthub.io/packages/helm/trino/trino/1.41.0) chart, whose other values are documented there.
    override trinotest values. Rendered only when global._hopsworks.trino.testCoordinator.enabled is true (see Chart.yaml). An optional single-node coordinator running catalog.management=dynamic with a WRITABLE catalog dir, used by the backend to connection-test user catalogs (CREATE CATALOG / SHOW SCHEMAS / DROP CATALOG) before they are synced to the production coordinator. Mirrors the production coordinator's image, certs, TLS, and PASSWORD auth so the backend's admin credentials and discovery work identically.

`trino.trinotest.initContainers.coordinator[2].name` <a class="headerlink" href="#helm.trino.trinotest.initContainers.coordinator.2.name" title="Permanent link">#</a> { #helm.trino.trinotest.initContainers.coordinator.2.name }
:   Type `string`, default `"mountable-secrets"`.
    readOnly is not optional. Without it the query engine gains a write channel into HopsFS as the trino service user; the volume's readOnly makes the kernel refuse writes too. --srcDir bounds what the mount exposes to the backend-owned tree; the mount authenticates as trino, which is in the hdfs superuser group, so srcDir is the only thing containing it.  No preStop unmount: the node plugin owns the mount and unmounts it in NodeUnpublishVolume, and hopsfs-sidecar.sh exits on SIGTERM, so the container terminates cleanly on its own.

</div>

## auth { #helm-values-trino-auth }

??? example "Defaults as YAML"

    ```yaml
    trino:
      auth:
        adminUserPwd: ''
        adminUserPwdHash: null
        adminUsername: trino
        createSecrets: true
        createSharedSecret: true
        monitoringUser: prometheus
        monitoringUserPwd: ''
        monitoringUserPwdHash: null
    ```

<div class="hops-values" markdown>

`trino.auth.adminUserPwd` <a class="headerlink" href="#helm.trino.auth.adminUserPwd" title="Permanent link">#</a> { #helm.trino.auth.adminUserPwd }
:   Type `string`, default `""`.
    Plaintext password for `adminUsername`, read by the backend and bcrypted into password.db by the seeder Job. Empty generates one on first install and reuses it from the existing Secret; empty in a non-auto mode fails the render, since the existing Secret cannot be read back.

`trino.auth.adminUsername` <a class="headerlink" href="#helm.trino.auth.adminUsername" title="Permanent link">#</a> { #helm.trino.auth.adminUsername }
:   Type `string`, default `"trino"`.
    Trino admin username. Should not be changed. Used in hadoop.proxyuser.trino

`trino.auth.createSecrets` <a class="headerlink" href="#helm.trino.auth.createSecrets" title="Permanent link">#</a> { #helm.trino.auth.createSecrets }
:   Type `bool`, default `true`.
    If createSecrets is false, you must manually create the following Kubernetes Secrets:   1. trino-admin-credentials (keys `username`, `password`): the backend's principal.   2. trino-monitoring-credentials (same keys): the principal Prometheus scrapes with. The seeder Job bcrypts both into password.db in HopsFS. Label both `backup.hops.works/include: "true"` so Velero captures them. In any non-auto `global._hopsworks.mode` (ArgoCD) the existing Secret cannot be read back, so the render fails unless both passwords below are set or this is false.

`trino.auth.createSharedSecret` <a class="headerlink" href="#helm.trino.auth.createSharedSecret" title="Permanent link">#</a> { #helm.trino.auth.createSharedSecret }
:   Type `bool`, default `true`.
    If `createSharedSecret` is set to `false`, you must generate an `internal-communication.shared-secret` value and store it in a Kubernetes Secret named `trino-internal-secret` under the key `shared-secret`. trino-internal-secret is intentionally NOT captured by the Velero backup (it has no coupling to user state and is regenerated on a fresh install). With createSharedSecret=false it is operator-managed, so disaster recovery must restore it from an independent source, followed by a coordinated restart of all Trino pods so coordinator and workers share the same value.

`trino.auth.monitoringUser` <a class="headerlink" href="#helm.trino.auth.monitoringUser" title="Permanent link">#</a> { #helm.trino.auth.monitoringUser }
:   Type `string`, default `"prometheus"`.
    Username used by Prometheus for scraping Trino metrics. If you override this value, you MUST also:   1. Update Trino access control to grant this user the required permissions      (e.g. adjust `accessControl.rules.rules.json` accordingly).   2. Update the Prometheus scrape configuration so that the same username is used:      set `.Values.prometheus.prometheus.serverFiles.prometheus.yml.scrape_configs[*].basic_auth.username`      for the scrape job with `job_name: "trino"` to match this value.

`trino.auth.monitoringUserPwd` <a class="headerlink" href="#helm.trino.auth.monitoringUserPwd" title="Permanent link">#</a> { #helm.trino.auth.monitoringUserPwd }
:   Type `string`, default `""`.
    Plaintext password for `monitoringUser`, read by Prometheus and bcrypted into password.db. Generated like `adminUserPwd`.

`trino.auth.adminUserPwdHash` <span class="hops-values-deprecated">Deprecated</span> <a class="headerlink" href="#helm.trino.auth.adminUserPwdHash" title="Permanent link">#</a> { #helm.trino.auth.adminUserPwdHash }
:   Type `string`, default `nil`.
    DEPRECATED, read by nothing: the seeder derives the hash from `adminUserPwd`. Kept so an existing override still validates.

`trino.auth.monitoringUserPwdHash` <span class="hops-values-deprecated">Deprecated</span> <a class="headerlink" href="#helm.trino.auth.monitoringUserPwdHash" title="Permanent link">#</a> { #helm.trino.auth.monitoringUserPwdHash }
:   Type `string`, default `nil`.
    DEPRECATED, read by nothing, like `adminUserPwdHash`.

</div>

## authSeeder { #helm-values-trino-authseeder }

??? example "Defaults as YAML"

    ```yaml
    trino:
      authSeeder:
        image:
          name: hopsfs
          registry: ''
          tag: 3.4.3.3-EE-RC1
        ttlSecondsAfterFinished: 3600
        waitSeconds: 600
    ```

<div class="hops-values" markdown>

`trino.authSeeder` <a class="headerlink" href="#helm.trino.authSeeder" title="Permanent link">#</a> { #helm.trino.authSeeder }
:   Type `object`.
    The Job that seeds password.db and group.db into HopsFS, and the pre-upgrade hook that migrates them from the legacy Secrets. Not optional: Trino cannot start without them.

    ??? note "Default"

        ```yaml
        image:
          name: hopsfs
          registry: ''
          tag: 3.4.3.3-EE-RC1
        ttlSecondsAfterFinished: 3600
        waitSeconds: 600
        ```

`trino.authSeeder.image` <a class="headerlink" href="#helm.trino.authSeeder.image" title="Permanent link">#</a> { #helm.trino.authSeeder.image }
:   Type `object`, default `{"name":"hopsfs","registry":"","tag":"3.4.3.3-EE-RC1"}`.
    The HopsFS client image. The seeder writes with `hdfs dfs`; the trino-files mount is read-only.

`trino.authSeeder.image.name` <a class="headerlink" href="#helm.trino.authSeeder.image.name" title="Permanent link">#</a> { #helm.trino.authSeeder.image.name }
:   Type `string`, default `"hopsfs"`.
    Image name.

`trino.authSeeder.image.registry` <a class="headerlink" href="#helm.trino.authSeeder.image.registry" title="Permanent link">#</a> { #helm.trino.authSeeder.image.registry }
:   Type `string`, default `""`.
    Full registry+path prefix, ending with `/`. Empty uses `global._hopsworks.imageRegistry` plus `/hopsworks/`, matching charts/hopsfs.

`trino.authSeeder.image.tag` <a class="headerlink" href="#helm.trino.authSeeder.image.tag" title="Permanent link">#</a> { #helm.trino.authSeeder.image.tag }
:   Type `string`, default `"3.4.3.3-EE-RC1"`.
    Image tag. Keep in step with `hopsfs.image.tag` in charts/hopsfs/values.yaml.

`trino.authSeeder.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.trino.authSeeder.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.trino.authSeeder.ttlSecondsAfterFinished }
:   Type `int`, default `3600`.
    Seconds to keep the finished Jobs; their logs record what was seeded.

`trino.authSeeder.waitSeconds` <a class="headerlink" href="#helm.trino.authSeeder.waitSeconds" title="Permanent link">#</a> { #helm.trino.authSeeder.waitSeconds }
:   Type `int`, default `600`.
    Seconds the seeder waits for HopsFS before failing.

</div>

## dependencies { #helm-values-trino-dependencies }

??? example "Defaults as YAML"

    ```yaml
    trino:
      dependencies:
        hive:
          consulServiceName: hive
          consulServiceTag: metastore
          port: 9083
        mysql:
          consulServiceName: mysql
          port: 3306
    ```

<div class="hops-values" markdown>

`trino.dependencies.hive.consulServiceName` <a class="headerlink" href="#helm.trino.dependencies.hive.consulServiceName" title="Permanent link">#</a> { #helm.trino.dependencies.hive.consulServiceName }
:   Type `string`, default `"hive"`.

`trino.dependencies.hive.consulServiceTag` <a class="headerlink" href="#helm.trino.dependencies.hive.consulServiceTag" title="Permanent link">#</a> { #helm.trino.dependencies.hive.consulServiceTag }
:   Type `string`, default `"metastore"`.

`trino.dependencies.hive.port` <a class="headerlink" href="#helm.trino.dependencies.hive.port" title="Permanent link">#</a> { #helm.trino.dependencies.hive.port }
:   Type `int`, default `9083`.

`trino.dependencies.mysql.consulServiceName` <a class="headerlink" href="#helm.trino.dependencies.mysql.consulServiceName" title="Permanent link">#</a> { #helm.trino.dependencies.mysql.consulServiceName }
:   Type `string`, default `"mysql"`.

`trino.dependencies.mysql.port` <a class="headerlink" href="#helm.trino.dependencies.mysql.port" title="Permanent link">#</a> { #helm.trino.dependencies.mysql.port }
:   Type `int`, default `3306`.

</div>

## externalLoadBalancer { #helm-values-trino-externalloadbalancer }

??? example "Defaults as YAML"

    ```yaml
    trino:
      externalLoadBalancer:
        annotations: {}
        class: null
        enabled: null
        managed: null
        nodePort: null
        nodeSelector: {}
    ```

<div class="hops-values" markdown>

`trino.externalLoadBalancer.annotations` <a class="headerlink" href="#helm.trino.externalLoadBalancer.annotations" title="Permanent link">#</a> { #helm.trino.externalLoadBalancer.annotations }
:   Type `object`, default `{}`.
    annotations for load balancer

`trino.externalLoadBalancer.class` <a class="headerlink" href="#helm.trino.externalLoadBalancer.class" title="Permanent link">#</a> { #helm.trino.externalLoadBalancer.class }
:   Type `string`, default `nil`.
    load balancer class name

`trino.externalLoadBalancer.enabled` <a class="headerlink" href="#helm.trino.externalLoadBalancer.enabled" title="Permanent link">#</a> { #helm.trino.externalLoadBalancer.enabled }
:   Type `string`, default `nil`.
    Enable External Load Balancers for the Trino coordinator/service. If not set the .global._hopsworks.externalLoadBalancers.enabled will be used instead

`trino.externalLoadBalancer.managed` <a class="headerlink" href="#helm.trino.externalLoadBalancer.managed" title="Permanent link">#</a> { #helm.trino.externalLoadBalancer.managed }
:   Type `string`, default `nil`.
    Cloud provider provisions Load Balancers. If not set the .global._hopsworks.externalLoadBalancers.managed will be used instead

`trino.externalLoadBalancer.nodePort` <a class="headerlink" href="#helm.trino.externalLoadBalancer.nodePort" title="Permanent link">#</a> { #helm.trino.externalLoadBalancer.nodePort }
:   Type `string`, default `nil`.
    Explicit nodePort for the external service when the load balancer is unmanaged (managed: false), so a load balancer outside Kubernetes can target a fixed port. Null lets Kubernetes allocate one from the cluster's node-port range; a set value must lie in that range (30000-32767 by default), which the API server enforces at install.

`trino.externalLoadBalancer.nodeSelector` <a class="headerlink" href="#helm.trino.externalLoadBalancer.nodeSelector" title="Permanent link">#</a> { #helm.trino.externalLoadBalancer.nodeSelector }
:   Type `object`, default `{}`.
    selector for nodes the load balancer can use to route traffic

</div>

## trino { #helm-values-trino-trino }

??? example "Defaults as YAML"

    ```yaml
    trino:
      trino:
        coordinator:
          additionalJVMConfig:
          - --add-opens=java.base/java.nio=ALL-UNNAMED
        image:
          registry: docker.hops.works
          repository: hopsworks/trino
          tag: 483-v1
        initContainers:
          coordinator:
          - null
          - null
          - name: mountable-secrets
          worker:
          - null
          - name: mountable-secrets
    ```

<div class="hops-values" markdown>

`trino.trino` <a class="headerlink" href="#helm.trino.trino" title="Permanent link">#</a> { #helm.trino.trino }
:   Type `object`, default check \[values.yaml\](./values.yaml) for more information, passed to the [`trino` 1.41.0](https://artifacthub.io/packages/helm/trino/trino/1.41.0) chart, whose other values are documented there.
    override trino values

`trino.trino.coordinator.additionalJVMConfig` <a class="headerlink" href="#helm.trino.trino.coordinator.additionalJVMConfig" title="Permanent link">#</a> { #helm.trino.trino.coordinator.additionalJVMConfig }
:   Type `list`, default `["--add-opens=java.base/java.nio=ALL-UNNAMED"]`.
    add-opens for java.nio, and the failure is a CONFIGURATION error raised while the catalog is being loaded. On this coordinator that is fatal rather than local, because Trino runs catalog.management=static and exits when a catalog file fails to load -- so one project's Snowflake catalog would stop the whole cluster from starting. Set here rather than left to the operator because the connector is in TRINO_CONNECTORS, i.e. the backend offers it to every project. Other Arrow-based connectors need the same opens, so this is not Snowflake-specific.

`trino.trino.image.registry` <a class="headerlink" href="#helm.trino.trino.image.registry" title="Permanent link">#</a> { #helm.trino.trino.image.registry }
:   Type `string`, default `"docker.hops.works"`.
    Image registry, defaults to empty, which results in DockerHub usage

`trino.trino.image.repository` <a class="headerlink" href="#helm.trino.trino.image.repository" title="Permanent link">#</a> { #helm.trino.trino.image.repository }
:   Type `string`, default `"hopsworks/trino"`.
    Repository location of the Trino image, typically `organization/imagename`

`trino.trino.image.tag` <a class="headerlink" href="#helm.trino.trino.image.tag" title="Permanent link">#</a> { #helm.trino.trino.image.tag }
:   Type `string`, default `"483-v1"`.
    Image tag for the Trino image. This value is explicitly pinned here and overrides any defaulting to `appVersion` from Chart.yaml.

`trino.trino.initContainers.coordinator[2].name` <a class="headerlink" href="#helm.trino.trino.initContainers.coordinator.2.name" title="Permanent link">#</a> { #helm.trino.trino.initContainers.coordinator.2.name }
:   Type `string`, default `"mountable-secrets"`.
    readOnly is not optional. Without it the query engine gains a write channel into HopsFS as the trino service user; the volume's readOnly makes the kernel refuse writes too. --srcDir bounds what the mount exposes to the backend-owned tree; the mount authenticates as trino, which is in the hdfs superuser group, so srcDir is the only thing containing it.  No preStop unmount: the node plugin owns the mount and unmounts it in NodeUnpublishVolume, and hopsfs-sidecar.sh exits on SIGTERM, so the container terminates cleanly on its own.

`trino.trino.initContainers.worker[1].name` <a class="headerlink" href="#helm.trino.trino.initContainers.worker.1.name" title="Permanent link">#</a> { #helm.trino.trino.initContainers.worker.1.name }
:   Type `string`, default `"mountable-secrets"`.
    readOnly is not optional. Without it the query engine gains a write channel into HopsFS as the trino service user; the volume's readOnly makes the kernel refuse writes too. --srcDir bounds what the mount exposes to the backend-owned tree; the mount authenticates as trino, which is in the hdfs superuser group, so srcDir is the only thing containing it.  No preStop unmount: the node plugin owns the mount and unmounts it in NodeUnpublishVolume, and hopsfs-sidecar.sh exits on SIGTERM, so the container terminates cleanly on its own.

</div>

<!-- END GENERATED VALUES -->
