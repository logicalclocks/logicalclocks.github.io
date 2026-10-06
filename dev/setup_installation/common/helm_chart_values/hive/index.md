# Hive values { #helm-values-hive }

Values under `hive` configure the Hive metastore, which holds the table metadata of the offline feature store.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.2.0-alpha-1791295130` (Hopsworks `5.2.0`)._

Deployed when [`global._hopsworks.full_platform`](global.md#helm.global._hopsworks.full_platform) is `true`.

## General { #helm-values-hive-general }

??? example "Defaults as YAML"

    ```yaml
    hive:
      debug: false
      hopsworkslib: {}
      name: hive
    ```

<div class="hops-values" markdown>

`hive` <a class="headerlink" href="#helm.hive" title="Permanent link">#</a> { #helm.hive }
:   Type `object`, default `{}`.
    override hive values

`hive.debug` <a class="headerlink" href="#helm.hive.debug" title="Permanent link">#</a> { #helm.hive.debug }
:   Type `bool`, default `false`.

`hive.hopsworkslib` <a class="headerlink" href="#helm.hive.hopsworkslib" title="Permanent link">#</a> { #helm.hive.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`hive.name` <a class="headerlink" href="#helm.hive.name" title="Permanent link">#</a> { #helm.hive.name }
:   Type `string`, default `"hive"`.

</div>

## externalLoadBalancer { #helm-values-hive-externalloadbalancer }

??? example "Defaults as YAML"

    ```yaml
    hive:
      externalLoadBalancer:
        annotations: {}
        class: null
        enabled: false
        managed: null
        nodeSelector: {}
    ```

<div class="hops-values" markdown>

`hive.externalLoadBalancer.annotations` <a class="headerlink" href="#helm.hive.externalLoadBalancer.annotations" title="Permanent link">#</a> { #helm.hive.externalLoadBalancer.annotations }
:   Type `object`, default `{}`.
    annotations for load balancer

`hive.externalLoadBalancer.class` <a class="headerlink" href="#helm.hive.externalLoadBalancer.class" title="Permanent link">#</a> { #helm.hive.externalLoadBalancer.class }
:   Type `string`, default `nil`.
    load balancer class name

`hive.externalLoadBalancer.enabled` <a class="headerlink" href="#helm.hive.externalLoadBalancer.enabled" title="Permanent link">#</a> { #helm.hive.externalLoadBalancer.enabled }
:   Type `bool`, default `false`.
    Enable External Load Balancer for the Hive Metastore. If not set the .global._hopsworks.externalLoadBalancers.enabled will be used instead

`hive.externalLoadBalancer.managed` <a class="headerlink" href="#helm.hive.externalLoadBalancer.managed" title="Permanent link">#</a> { #helm.hive.externalLoadBalancer.managed }
:   Type `string`, default `nil`.
    Cloud provider provisions Load Balancers. If not set the .global._hopsworks.externalLoadBalancers.managed will be used instead

`hive.externalLoadBalancer.nodeSelector` <a class="headerlink" href="#helm.hive.externalLoadBalancer.nodeSelector" title="Permanent link">#</a> { #helm.hive.externalLoadBalancer.nodeSelector }
:   Type `object`, default `{}`.
    selector for nodes the load balancer can use to route traffic

</div>

## metastore { #helm-values-hive-metastore }

??? example "Defaults as YAML"

    ```yaml
    hive:
      metastore:
        appName: hivemetastore
        config:
          cm_rootdir: ''
          enforce_auth: true
          hopsfs_dir: /apps/hive/warehouse
          hudi_hadoop_version: 1.2.0
          impersonation: hive,glassfish
          mapreduce_input_size: '134217728'
          repl_rootdir: ''
          scratch_dir: /tmp/hive
        configmap:
          name: hivemetastore-configmap
        create_secret: true
        dependencies:
          glassfish:
            consulServiceName: glassfish
            consulServiceTag: hopsworks
            port: 8182
          mysql:
            consulServiceName: mysql
            port: 3306
          namenode:
            consulServiceName: namenode
            consulServiceTag: rpc
            port: 8020
        deployment:
          jvm_resources:
            xms: 2g
            xmx: 2g
          name: hivemetastore-deployment
          probes:
            liveness:
              initialDelaySeconds: 60
              periodSeconds: 10
              tcpSocket:
                port: 9083
              timeoutSeconds: 10
            readiness:
              initialDelaySeconds: 60
              periodSeconds: 10
              tcpSocket:
                port: 9083
              timeoutSeconds: 60
            startup: {}
          rbac:
            annotations: {}
            create: true
            extraRoleRules: []
            name: hivemetastore-role
            useExistingRole: false
          replicas: 1
          resources:
            limits:
              memory: 8192Mi
            requests:
              cpu: '2'
              memory: 6553Mi
          security:
            fsGroup: 1234
            group: hive
            runAsGroup: 1234
            runAsUser: 1516
            user: hive
          serviceAccount:
            annotations: {}
            create: true
            name: hivemetastore-default
        hadoop_user: hive
        image:
          pullPolicy: IfNotPresent
          registry: docker.hops.works
        logLevel: INFO
        migration:
          resources:
            limits:
              cpu: 500m
              memory: 500Mi
            requests:
              cpu: 100m
              memory: 100Mi
        migrationBackOffLimit: 10
        monitoring_port: 18002
        nodeSelector: {}
        podDisruptionBudget:
          enabled: true
          minAvailable: 1
        port: 9083
        protocol: thrift
        service:
          annotations:
            consul.hashicorp.com/service-name: hive
            consul.hashicorp.com/service-tags: metastore,hiveserver2-tls,hiveserver2-plain
          name: metastore
        tolerations: []
        topologySpreadConstraint: {}
    ```

<div class="hops-values" markdown>

`hive.metastore.appName` <a class="headerlink" href="#helm.hive.metastore.appName" title="Permanent link">#</a> { #helm.hive.metastore.appName }
:   Type `string`, default `"hivemetastore"`.

`hive.metastore.config.cm_rootdir` <a class="headerlink" href="#helm.hive.metastore.config.cm_rootdir" title="Permanent link">#</a> { #helm.hive.metastore.config.cm_rootdir }
:   Type `string`, default `""`.

`hive.metastore.config.enforce_auth` <a class="headerlink" href="#helm.hive.metastore.config.enforce_auth" title="Permanent link">#</a> { #helm.hive.metastore.config.enforce_auth }
:   Type `bool`, default `true`.

`hive.metastore.config.hopsfs_dir` <a class="headerlink" href="#helm.hive.metastore.config.hopsfs_dir" title="Permanent link">#</a> { #helm.hive.metastore.config.hopsfs_dir }
:   Type `string`, default `"/apps/hive/warehouse"`.

`hive.metastore.config.hudi_hadoop_version` <a class="headerlink" href="#helm.hive.metastore.config.hudi_hadoop_version" title="Permanent link">#</a> { #helm.hive.metastore.config.hudi_hadoop_version }
:   Type `string`, default `"1.2.0"`.

`hive.metastore.config.impersonation` <a class="headerlink" href="#helm.hive.metastore.config.impersonation" title="Permanent link">#</a> { #helm.hive.metastore.config.impersonation }
:   Type `string`, default `"hive,glassfish"`.

`hive.metastore.config.mapreduce_input_size` <a class="headerlink" href="#helm.hive.metastore.config.mapreduce_input_size" title="Permanent link">#</a> { #helm.hive.metastore.config.mapreduce_input_size }
:   Type `string`, default `"134217728"`.

`hive.metastore.config.repl_rootdir` <a class="headerlink" href="#helm.hive.metastore.config.repl_rootdir" title="Permanent link">#</a> { #helm.hive.metastore.config.repl_rootdir }
:   Type `string`, default `""`.

`hive.metastore.config.scratch_dir` <a class="headerlink" href="#helm.hive.metastore.config.scratch_dir" title="Permanent link">#</a> { #helm.hive.metastore.config.scratch_dir }
:   Type `string`, default `"/tmp/hive"`.

`hive.metastore.configmap.name` <a class="headerlink" href="#helm.hive.metastore.configmap.name" title="Permanent link">#</a> { #helm.hive.metastore.configmap.name }
:   Type `string`, default `"hivemetastore-configmap"`.

`hive.metastore.create_secret` <a class="headerlink" href="#helm.hive.metastore.create_secret" title="Permanent link">#</a> { #helm.hive.metastore.create_secret }
:   Type `bool`, default `true`.
    Create the mysql users secret for hive metastore. If false, you have to create the secret (hive-user-secrets) manually.

`hive.metastore.dependencies.glassfish.consulServiceName` <a class="headerlink" href="#helm.hive.metastore.dependencies.glassfish.consulServiceName" title="Permanent link">#</a> { #helm.hive.metastore.dependencies.glassfish.consulServiceName }
:   Type `string`, default `"glassfish"`.

`hive.metastore.dependencies.glassfish.consulServiceTag` <a class="headerlink" href="#helm.hive.metastore.dependencies.glassfish.consulServiceTag" title="Permanent link">#</a> { #helm.hive.metastore.dependencies.glassfish.consulServiceTag }
:   Type `string`, default `"hopsworks"`.

`hive.metastore.dependencies.glassfish.port` <a class="headerlink" href="#helm.hive.metastore.dependencies.glassfish.port" title="Permanent link">#</a> { #helm.hive.metastore.dependencies.glassfish.port }
:   Type `int`, default `8182`.

`hive.metastore.dependencies.mysql.consulServiceName` <a class="headerlink" href="#helm.hive.metastore.dependencies.mysql.consulServiceName" title="Permanent link">#</a> { #helm.hive.metastore.dependencies.mysql.consulServiceName }
:   Type `string`, default `"mysql"`.

`hive.metastore.dependencies.mysql.port` <a class="headerlink" href="#helm.hive.metastore.dependencies.mysql.port" title="Permanent link">#</a> { #helm.hive.metastore.dependencies.mysql.port }
:   Type `int`, default `3306`.

`hive.metastore.dependencies.namenode.consulServiceName` <a class="headerlink" href="#helm.hive.metastore.dependencies.namenode.consulServiceName" title="Permanent link">#</a> { #helm.hive.metastore.dependencies.namenode.consulServiceName }
:   Type `string`, default `"namenode"`.

`hive.metastore.dependencies.namenode.consulServiceTag` <a class="headerlink" href="#helm.hive.metastore.dependencies.namenode.consulServiceTag" title="Permanent link">#</a> { #helm.hive.metastore.dependencies.namenode.consulServiceTag }
:   Type `string`, default `"rpc"`.

`hive.metastore.dependencies.namenode.port` <a class="headerlink" href="#helm.hive.metastore.dependencies.namenode.port" title="Permanent link">#</a> { #helm.hive.metastore.dependencies.namenode.port }
:   Type `int`, default `8020`.

`hive.metastore.deployment.jvm_resources` <a class="headerlink" href="#helm.hive.metastore.deployment.jvm_resources" title="Permanent link">#</a> { #helm.hive.metastore.deployment.jvm_resources }
:   Type `object`, default `{"xms":"2g","xmx":"2g"}`.
    Xms and Xmx parameters for the Hivemetastore JVM initialization. Notice that, if set, container resources will be ignored and automatically calculated based on the values provided by this property.

`hive.metastore.deployment.jvm_resources.xms` <a class="headerlink" href="#helm.hive.metastore.deployment.jvm_resources.xms" title="Permanent link">#</a> { #helm.hive.metastore.deployment.jvm_resources.xms }
:   Type `string`, default `"2g"`.
    Initial heap size for JVM (e.g., '0.5g', '1g', '1.5g')

`hive.metastore.deployment.jvm_resources.xmx` <a class="headerlink" href="#helm.hive.metastore.deployment.jvm_resources.xmx" title="Permanent link">#</a> { #helm.hive.metastore.deployment.jvm_resources.xmx }
:   Type `string`, default `"2g"`.
    Maximum heap size for JVM (e.g., '0.5g', '1g', '1.5g')

`hive.metastore.deployment.name` <a class="headerlink" href="#helm.hive.metastore.deployment.name" title="Permanent link">#</a> { #helm.hive.metastore.deployment.name }
:   Type `string`, default `"hivemetastore-deployment"`.

`hive.metastore.deployment.probes.liveness.initialDelaySeconds` <a class="headerlink" href="#helm.hive.metastore.deployment.probes.liveness.initialDelaySeconds" title="Permanent link">#</a> { #helm.hive.metastore.deployment.probes.liveness.initialDelaySeconds }
:   Type `int`, default `60`.

`hive.metastore.deployment.probes.liveness.periodSeconds` <a class="headerlink" href="#helm.hive.metastore.deployment.probes.liveness.periodSeconds" title="Permanent link">#</a> { #helm.hive.metastore.deployment.probes.liveness.periodSeconds }
:   Type `int`, default `10`.

`hive.metastore.deployment.probes.liveness.tcpSocket.port` <a class="headerlink" href="#helm.hive.metastore.deployment.probes.liveness.tcpSocket.port" title="Permanent link">#</a> { #helm.hive.metastore.deployment.probes.liveness.tcpSocket.port }
:   Type `int`, default `9083`.

`hive.metastore.deployment.probes.liveness.timeoutSeconds` <a class="headerlink" href="#helm.hive.metastore.deployment.probes.liveness.timeoutSeconds" title="Permanent link">#</a> { #helm.hive.metastore.deployment.probes.liveness.timeoutSeconds }
:   Type `int`, default `10`.

`hive.metastore.deployment.probes.readiness.initialDelaySeconds` <a class="headerlink" href="#helm.hive.metastore.deployment.probes.readiness.initialDelaySeconds" title="Permanent link">#</a> { #helm.hive.metastore.deployment.probes.readiness.initialDelaySeconds }
:   Type `int`, default `60`.

`hive.metastore.deployment.probes.readiness.periodSeconds` <a class="headerlink" href="#helm.hive.metastore.deployment.probes.readiness.periodSeconds" title="Permanent link">#</a> { #helm.hive.metastore.deployment.probes.readiness.periodSeconds }
:   Type `int`, default `10`.

`hive.metastore.deployment.probes.readiness.tcpSocket.port` <a class="headerlink" href="#helm.hive.metastore.deployment.probes.readiness.tcpSocket.port" title="Permanent link">#</a> { #helm.hive.metastore.deployment.probes.readiness.tcpSocket.port }
:   Type `int`, default `9083`.

`hive.metastore.deployment.probes.readiness.timeoutSeconds` <a class="headerlink" href="#helm.hive.metastore.deployment.probes.readiness.timeoutSeconds" title="Permanent link">#</a> { #helm.hive.metastore.deployment.probes.readiness.timeoutSeconds }
:   Type `int`, default `60`.

`hive.metastore.deployment.probes.startup` <a class="headerlink" href="#helm.hive.metastore.deployment.probes.startup" title="Permanent link">#</a> { #helm.hive.metastore.deployment.probes.startup }
:   Type `object`, default `{}`.
    startup probes

`hive.metastore.deployment.rbac.annotations` <a class="headerlink" href="#helm.hive.metastore.deployment.rbac.annotations" title="Permanent link">#</a> { #helm.hive.metastore.deployment.rbac.annotations }
:   Type `object`, default `{}`.
    metrics rbac role annotations

`hive.metastore.deployment.rbac.create` <a class="headerlink" href="#helm.hive.metastore.deployment.rbac.create" title="Permanent link">#</a> { #helm.hive.metastore.deployment.rbac.create }
:   Type `bool`, default `true`.

`hive.metastore.deployment.rbac.extraRoleRules` <a class="headerlink" href="#helm.hive.metastore.deployment.rbac.extraRoleRules" title="Permanent link">#</a> { #helm.hive.metastore.deployment.rbac.extraRoleRules }
:   Type `list`, default `[]`.
    extra rules to attach to metrics acl role

`hive.metastore.deployment.rbac.name` <a class="headerlink" href="#helm.hive.metastore.deployment.rbac.name" title="Permanent link">#</a> { #helm.hive.metastore.deployment.rbac.name }
:   Type `string`, default `"hivemetastore-role"`.

`hive.metastore.deployment.rbac.useExistingRole` <a class="headerlink" href="#helm.hive.metastore.deployment.rbac.useExistingRole" title="Permanent link">#</a> { #helm.hive.metastore.deployment.rbac.useExistingRole }
:   Type `bool`, default `false`.

`hive.metastore.deployment.replicas` <a class="headerlink" href="#helm.hive.metastore.deployment.replicas" title="Permanent link">#</a> { #helm.hive.metastore.deployment.replicas }
:   Type `int`, default `1`.

`hive.metastore.deployment.resources.limits` <a class="headerlink" href="#helm.hive.metastore.deployment.resources.limits" title="Permanent link">#</a> { #helm.hive.metastore.deployment.resources.limits }
:   Type `object`, default `{"memory":"8192Mi"}`.
    resources limits configuration

`hive.metastore.deployment.resources.requests` <a class="headerlink" href="#helm.hive.metastore.deployment.resources.requests" title="Permanent link">#</a> { #helm.hive.metastore.deployment.resources.requests }
:   Type `object`, default `{"cpu":"2","memory":"6553Mi"}`.
    resources requests configuration

`hive.metastore.deployment.security.fsGroup` <a class="headerlink" href="#helm.hive.metastore.deployment.security.fsGroup" title="Permanent link">#</a> { #helm.hive.metastore.deployment.security.fsGroup }
:   Type `int`, default `1234`.

`hive.metastore.deployment.security.group` <a class="headerlink" href="#helm.hive.metastore.deployment.security.group" title="Permanent link">#</a> { #helm.hive.metastore.deployment.security.group }
:   Type `string`, default `"hive"`.

`hive.metastore.deployment.security.runAsGroup` <a class="headerlink" href="#helm.hive.metastore.deployment.security.runAsGroup" title="Permanent link">#</a> { #helm.hive.metastore.deployment.security.runAsGroup }
:   Type `int`, default `1234`.

`hive.metastore.deployment.security.runAsUser` <a class="headerlink" href="#helm.hive.metastore.deployment.security.runAsUser" title="Permanent link">#</a> { #helm.hive.metastore.deployment.security.runAsUser }
:   Type `int`, default `1516`.

`hive.metastore.deployment.security.user` <a class="headerlink" href="#helm.hive.metastore.deployment.security.user" title="Permanent link">#</a> { #helm.hive.metastore.deployment.security.user }
:   Type `string`, default `"hive"`.

`hive.metastore.deployment.serviceAccount.annotations` <a class="headerlink" href="#helm.hive.metastore.deployment.serviceAccount.annotations" title="Permanent link">#</a> { #helm.hive.metastore.deployment.serviceAccount.annotations }
:   Type `object`, default `{}`.
    service account annotations

`hive.metastore.deployment.serviceAccount.create` <a class="headerlink" href="#helm.hive.metastore.deployment.serviceAccount.create" title="Permanent link">#</a> { #helm.hive.metastore.deployment.serviceAccount.create }
:   Type `bool`, default `true`.

`hive.metastore.deployment.serviceAccount.name` <a class="headerlink" href="#helm.hive.metastore.deployment.serviceAccount.name" title="Permanent link">#</a> { #helm.hive.metastore.deployment.serviceAccount.name }
:   Type `string`, default `"hivemetastore-default"`.

`hive.metastore.hadoop_user` <a class="headerlink" href="#helm.hive.metastore.hadoop_user" title="Permanent link">#</a> { #helm.hive.metastore.hadoop_user }
:   Type `string`, default `"hive"`.

`hive.metastore.image.pullPolicy` <a class="headerlink" href="#helm.hive.metastore.image.pullPolicy" title="Permanent link">#</a> { #helm.hive.metastore.image.pullPolicy }
:   Type `string`, default `"IfNotPresent"`.

`hive.metastore.image.registry` <a class="headerlink" href="#helm.hive.metastore.image.registry" title="Permanent link">#</a> { #helm.hive.metastore.image.registry }
:   Type `string`, default `"docker.hops.works"`.

`hive.metastore.logLevel` <a class="headerlink" href="#helm.hive.metastore.logLevel" title="Permanent link">#</a> { #helm.hive.metastore.logLevel }
:   Type `string`, default `"INFO"`.

`hive.metastore.migration.resources.limits.cpu` <a class="headerlink" href="#helm.hive.metastore.migration.resources.limits.cpu" title="Permanent link">#</a> { #helm.hive.metastore.migration.resources.limits.cpu }
:   Type `string`, default `"500m"`.

`hive.metastore.migration.resources.limits.memory` <a class="headerlink" href="#helm.hive.metastore.migration.resources.limits.memory" title="Permanent link">#</a> { #helm.hive.metastore.migration.resources.limits.memory }
:   Type `string`, default `"500Mi"`.

`hive.metastore.migration.resources.requests.cpu` <a class="headerlink" href="#helm.hive.metastore.migration.resources.requests.cpu" title="Permanent link">#</a> { #helm.hive.metastore.migration.resources.requests.cpu }
:   Type `string`, default `"100m"`.

`hive.metastore.migration.resources.requests.memory` <a class="headerlink" href="#helm.hive.metastore.migration.resources.requests.memory" title="Permanent link">#</a> { #helm.hive.metastore.migration.resources.requests.memory }
:   Type `string`, default `"100Mi"`.

`hive.metastore.migrationBackOffLimit` <a class="headerlink" href="#helm.hive.metastore.migrationBackOffLimit" title="Permanent link">#</a> { #helm.hive.metastore.migrationBackOffLimit }
:   Type `int`, default `10`.
    backoffLimit for hive migration job

`hive.metastore.monitoring_port` <a class="headerlink" href="#helm.hive.metastore.monitoring_port" title="Permanent link">#</a> { #helm.hive.metastore.monitoring_port }
:   Type `int`, default `18002`.

`hive.metastore.nodeSelector` <a class="headerlink" href="#helm.hive.metastore.nodeSelector" title="Permanent link">#</a> { #helm.hive.metastore.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

`hive.metastore.podDisruptionBudget.enabled` <a class="headerlink" href="#helm.hive.metastore.podDisruptionBudget.enabled" title="Permanent link">#</a> { #helm.hive.metastore.podDisruptionBudget.enabled }
:   Type `bool`, default `true`.

`hive.metastore.podDisruptionBudget.minAvailable` <a class="headerlink" href="#helm.hive.metastore.podDisruptionBudget.minAvailable" title="Permanent link">#</a> { #helm.hive.metastore.podDisruptionBudget.minAvailable }
:   Type `int`, default `1`.

`hive.metastore.port` <a class="headerlink" href="#helm.hive.metastore.port" title="Permanent link">#</a> { #helm.hive.metastore.port }
:   Type `int`, default `9083`.

`hive.metastore.protocol` <a class="headerlink" href="#helm.hive.metastore.protocol" title="Permanent link">#</a> { #helm.hive.metastore.protocol }
:   Type `string`, default `"thrift"`.

`hive.metastore.service.annotations."consul.hashicorp.com/service-name"` <a class="headerlink" href="#helm.hive.metastore.service.annotations.consul.hashicorp.com-service-name" title="Permanent link">#</a> { #helm.hive.metastore.service.annotations.consul.hashicorp.com-service-name }
:   Type `string`, default `"hive"`.

`hive.metastore.service.annotations."consul.hashicorp.com/service-tags"` <a class="headerlink" href="#helm.hive.metastore.service.annotations.consul.hashicorp.com-service-tags" title="Permanent link">#</a> { #helm.hive.metastore.service.annotations.consul.hashicorp.com-service-tags }
:   Type `string`, default `"metastore,hiveserver2-tls,hiveserver2-plain"`.

`hive.metastore.service.name` <a class="headerlink" href="#helm.hive.metastore.service.name" title="Permanent link">#</a> { #helm.hive.metastore.service.name }
:   Type `string`, default `"metastore"`.

`hive.metastore.tolerations` <a class="headerlink" href="#helm.hive.metastore.tolerations" title="Permanent link">#</a> { #helm.hive.metastore.tolerations }
:   Type `list`, default `[]`.

`hive.metastore.topologySpreadConstraint` <a class="headerlink" href="#helm.hive.metastore.topologySpreadConstraint" title="Permanent link">#</a> { #helm.hive.metastore.topologySpreadConstraint }
:   Type `object`, default `{}`.
    The default topology spread constraint. If not defined the global topology spread constraint would be used instead.

</div>

<!-- END GENERATED VALUES -->
