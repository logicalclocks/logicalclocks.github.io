# RonDB values { #helm-values-rondb }

Values under `rondb` configure RonDB, the online feature store database, installed from the RonDB Helm chart.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.2.0-alpha-1791477965` (Hopsworks `5.2.0`)._

Always deployed.

!!! info "Upstream charts"

    - Values under `rondb.rondb` go to [`rondb` 26.2.21](https://github.com/logicalclocks/rondb-helm/blob/v26.2.21/values.schema.json) from `https://logicalclocks.github.io/rondb-helm/`, and all of them are listed under [`rondb` chart values](#helm-values-rondb-rondb).

??? example "Defaults as YAML"

    ```yaml
    rondb:
      rondb:
        backups:
          enabled: null
          pathPrefix: rondb_backup
        clusterSize:
          activeDataReplicas: 2
          maxNumMySQLServers: 1
          maxNumRdrs: 2
          minNumMySQLServers: 1
          minNumRdrs: 1
          numNodeGroups: 1
        enableSecurityContext: true
        images:
          mysqldExporter:
            registry: docker.hops.works
            repository: hopsworks
          rondb:
            registry: docker.hops.works
            repository: hopsworks
          toolbox:
            name: hwutils
            registry: docker.hops.works
            repository: hopsworks
            tag: 1.10-SNAPSHOT
        meta:
          ddlMySQLd:
            clusterIp:
              annotations:
                consul.hashicorp.com/service-name: mysqlddl
                consul.hashicorp.com/service-tags: onlinefs
            enabled: true
            statefulSet:
              endToEndTls:
                enabled: false
                filenames:
                  ca: hops_root_ca.pem
                  cert: mysqlddl_certificate_bundle.pem
                  key: mysqlddl_priv.pem
                secretName: mysqlddl-crypto-material
                supplyOwnSecret: true
          mgmd:
            headlessClusterIp:
              annotations:
                consul.hashicorp.com/service-name: mgmd
          mysqld:
            clusterIp:
              annotations:
                consul.hashicorp.com/service-name: mysql
                consul.hashicorp.com/service-tags: onlinefs
            externalLoadBalancer:
              annotations: {}
              class: null
              enabled: true
              name: mysqld-external
            statefulSet:
              endToEndTls:
                enabled: false
                filenames:
                  ca: hops_root_ca.pem
                  cert: mysql_certificate_bundle.pem
                  key: mysql_priv.pem
                secretName: mysqld-crypto-material
                supplyOwnSecret: true
          rdrs:
            clusterIp:
              annotations:
                consul.hashicorp.com/service-name: rdrs
                prometheus.io/path: /metrics
                prometheus.io/port: '4406'
                prometheus.io/scheme: https
                prometheus.io/scrape: 'true'
            externalLoadBalancer:
              annotations: {}
              class: null
              enabled: true
              name: rdrs-external
            headlessClusterIpName: rdrs-cluster-ip
            ingress:
              enabled: false
            statefulSet:
              endToEndTls:
                enabled: true
                filenames:
                  ca: hops_root_ca.pem
                  cert: mysql_certificate_bundle.pem
                  key: mysql_priv.pem
                secretName: rdrs-crypto-material
                supplyOwnSecret: true
        mysql:
          clusterUser: bench
          credentialsSecretName: mysql-users-secrets
          exporter:
            enabled: true
          users:
          - host: '%'
            privileges:
            - database: '*'
              privileges:
              - ALL
              table: '*'
              withGrantOption: true
            username: hopsworksroot
        networkPolicy:
          mgmds:
            ingressSelectors:
            - podSelector:
                matchLabels:
                  access: mgmd-and-ndbmtd
          ndbmtds:
            ingressSelectors:
            - podSelector:
                matchLabels:
                  access: mgmd-and-ndbmtd
        resources:
          requests:
            storage:
              classes:
                binlogFiles: null
                default: null
                diskColumns: null
        restoreFromBackup:
          backupId: null
          pathPrefix: rondb_backup
        serviceAccountAnnotations: {}
    ```

<div class="hops-values" markdown>

`rondb` <a class="headerlink" href="#helm.rondb" title="Permanent link">#</a> { #helm.rondb }
:   Type `object`.
    override rondb values

    ??? note "Default"

        ```yaml
        rondb:
          clusterSize:
            activeDataReplicas: 2
            maxNumMySQLServers: 1
            maxNumRdrs: 2
            minNumMySQLServers: 1
            minNumRdrs: 1
            numNodeGroups: 1
          enableSecurityContext: true
          images:
            mysqldExporter:
              registry: docker.hops.works
            rondb:
              registry: docker.hops.works
            toolbox:
              name: hwutils
              registry: docker.hops.works
              tag: 1.10-SNAPSHOT
          meta:
            mysqld:
              externalLoadBalancer:
                annotations: {}
                class: null
                enabled: true
                name: mysqld-external
            rdrs:
              externalLoadBalancer:
                annotations: {}
                class: null
                enabled: true
                name: rdrs-external
              statefulSet:
                endToEndTls:
                  enabled: true
          mysql:
            credentialsSecretName: mysql-users-secrets
            exporter:
              enabled: true
            users:
            - host: '%'
              privileges:
              - database: '*'
                privileges:
                - ALL
                table: '*'
                withGrantOption: true
              username: hopsworksroot
          networkPolicy:
            mgmds:
              ingressSelectors:
              - podSelector:
                  matchLabels:
                    access: mgmd-and-ndbmtd
            ndbmtds:
              ingressSelectors:
              - podSelector:
                  matchLabels:
                    access: mgmd-and-ndbmtd
          resources:
            requests:
              storage:
                classes:
                  binlogFiles: null
                  default: null
                  diskColumns: null
          serviceAccountAnnotations: {}
        ```

`rondb.rondb` <a class="headerlink" href="#helm.rondb.rondb" title="Permanent link">#</a> { #helm.rondb.rondb }
:   Type `object`, passed to the [`rondb` 26.2.21](https://github.com/logicalclocks/rondb-helm/blob/v26.2.21/values.schema.json) chart, whose values are listed under [`rondb` chart values](#helm-values-rondb-rondb).
    override rondb values

    ??? note "Default"

        ```yaml
        meta:
          mgmd:
            headlessClusterIp:
              annotations:
                consul.hashicorp.com/service-name: mgmd
          mysqld:
            statefulSet:
              endToEndTls:
                enabled: false
                secretName: mysqld-crypto-material
                supplyOwnSecret: true
                filenames:
                  ca: hops_root_ca.pem
                  cert: mysql_certificate_bundle.pem
                  key: mysql_priv.pem
            clusterIp:
              annotations:
                consul.hashicorp.com/service-name: mysql
                consul.hashicorp.com/service-tags: onlinefs
            externalLoadBalancer:
              name: mysqld-external
              enabled: true
              class: null
              annotations: {}
          ddlMySQLd:
            enabled: true
            statefulSet:
              endToEndTls:
                enabled: false
                secretName: mysqlddl-crypto-material
                supplyOwnSecret: true
                filenames:
                  ca: hops_root_ca.pem
                  cert: mysqlddl_certificate_bundle.pem
                  key: mysqlddl_priv.pem
            clusterIp:
              annotations:
                consul.hashicorp.com/service-name: mysqlddl
                consul.hashicorp.com/service-tags: onlinefs
          rdrs:
            statefulSet:
              endToEndTls:
                enabled: true
                secretName: rdrs-crypto-material
                supplyOwnSecret: true
                filenames:
                  ca: hops_root_ca.pem
                  cert: mysql_certificate_bundle.pem
                  key: mysql_priv.pem
            clusterIp:
              annotations:
                consul.hashicorp.com/service-name: rdrs
                prometheus.io/path: /metrics
                prometheus.io/port: '4406'
                prometheus.io/scheme: https
                prometheus.io/scrape: 'true'
            headlessClusterIpName: rdrs-cluster-ip
            ingress:
              enabled: false
            externalLoadBalancer:
              name: rdrs-external
              enabled: true
              class: null
              annotations: {}
        images:
          rondb:
            registry: docker.hops.works
            repository: hopsworks
          toolbox:
            registry: docker.hops.works
            repository: hopsworks
            name: hwutils
            tag: 1.10-SNAPSHOT
          mysqldExporter:
            registry: docker.hops.works
            repository: hopsworks
        mysql:
          clusterUser: bench
          exporter:
            enabled: true
          users:
          - username: hopsworksroot
            host: '%'
            privileges:
            - database: '*'
              table: '*'
              withGrantOption: true
              privileges:
              - ALL
          credentialsSecretName: mysql-users-secrets
        clusterSize:
          activeDataReplicas: 2
          numNodeGroups: 1
          minNumMySQLServers: 1
          maxNumMySQLServers: 1
          minNumRdrs: 1
          maxNumRdrs: 2
        restoreFromBackup:
          backupId: null
          pathPrefix: rondb_backup
        backups:
          enabled: null
          pathPrefix: rondb_backup
        enableSecurityContext: true
        serviceAccountAnnotations: {}
        resources:
          requests:
            storage:
              classes:
                default: null
                diskColumns: null
                binlogFiles: null
        networkPolicy:
          mgmds:
            ingressSelectors:
            - podSelector:
                matchLabels:
                  access: mgmd-and-ndbmtd
          ndbmtds:
            ingressSelectors:
            - podSelector:
                matchLabels:
                  access: mgmd-and-ndbmtd
        ```

</div>

## `rondb` chart values { #helm-values-rondb-rondb }

These are the values of the [`rondb` 26.2.21](https://github.com/logicalclocks/rondb-helm/blob/v26.2.21/values.schema.json) chart, set under `rondb.rondb`.
The defaults are what Hopsworks deploys: the chart's own, with the `rondb` and `rondb.rondb` overrides above applied.
Where Hopsworks overrides a value, the entry also gives the chart's own default.

### General { #helm-values-rondb-rondb-general }

??? example "Defaults as YAML"

    ```yaml
    rondb:
      rondb:
        createPriorityClass: true
        enableSecurityContext: true
        forceNodeGroupChange: false
        imagePullPolicy: IfNotPresent
        imagePullSecrets: []
        isMultiNodeCluster: true
        mgmdPreUpgradeRolloutTimeout: 5m
        mode: ''
        priorityClass: rondb-high-priority
        serviceAccountAnnotations: {}
        skipMgmdPreUpgradeRollout: false
        staticCpuManagerPolicy: false
        tls:
          caSecretName: null
    ```

<div class="hops-values" markdown>

`rondb.rondb.createPriorityClass` <a class="headerlink" href="#helm.rondb.rondb.createPriorityClass" title="Permanent link">#</a> { #helm.rondb.rondb.createPriorityClass }
:   Type `boolean`, default `true`.
    Flag to disable the creation of PriorityClass in case it was created beforehand

`rondb.rondb.enableSecurityContext` <a class="headerlink" href="#helm.rondb.rondb.enableSecurityContext" title="Permanent link">#</a> { #helm.rondb.rondb.enableSecurityContext }
:   Type `boolean`, default `true`.

`rondb.rondb.forceNodeGroupChange` <a class="headerlink" href="#helm.rondb.rondb.forceNodeGroupChange" title="Permanent link">#</a> { #helm.rondb.rondb.forceNodeGroupChange }
:   Type `boolean`, default `false`.
    Skip the pre-upgrade immutability gate on clusterSize.numNodeGroups. RonDB still cannot add or remove node groups online, so an upgrade that changes numNodeGroups under this flag will break the cluster.

`rondb.rondb.imagePullPolicy` <a class="headerlink" href="#helm.rondb.rondb.imagePullPolicy" title="Permanent link">#</a> { #helm.rondb.rondb.imagePullPolicy }
:   Type `string`, default `"IfNotPresent"`.
    The Kubernetes image pull policy

`rondb.rondb.imagePullSecrets` <a class="headerlink" href="#helm.rondb.rondb.imagePullSecrets" title="Permanent link">#</a> { #helm.rondb.rondb.imagePullSecrets }
:   Type `array`, default `[]`.

`rondb.rondb.imagePullSecrets[].name` <a class="headerlink" href="#helm.rondb.rondb.imagePullSecrets.name" title="Permanent link">#</a> { #helm.rondb.rondb.imagePullSecrets.name }
:   Type `string`.
    The name of the Secret

`rondb.rondb.isMultiNodeCluster` <a class="headerlink" href="#helm.rondb.rondb.isMultiNodeCluster" title="Permanent link">#</a> { #helm.rondb.rondb.isMultiNodeCluster }
:   Type `boolean`, default `true`.
    Whether the Kubernetes cluster has multiple nodes; this will affect affinities and add requirements to scheduling.

`rondb.rondb.mgmdPreUpgradeRolloutTimeout` <a class="headerlink" href="#helm.rondb.rondb.mgmdPreUpgradeRolloutTimeout" title="Permanent link">#</a> { #helm.rondb.rondb.mgmdPreUpgradeRolloutTimeout }
:   Type `string`, default `"5m"`.
    Timeout for `kubectl rollout status` inside the MGMd pre-upgrade hook (per attempt). Default 5m. Note: Helm's default `helm upgrade --timeout` is also 5m and bounds the whole upgrade including this hook — operators running with that default may see Helm's outer timeout fire first with a generic 'timed out waiting for the condition' message instead of this hook's specific diagnostic. Set Helm's `--timeout` higher (e.g. 15m) on slow networks or large image pulls.

`rondb.rondb.mode` <a class="headerlink" href="#helm.rondb.rondb.mode" title="Permanent link">#</a> { #helm.rondb.rondb.mode }
:   Type `enum`, default `""`.
    Mode of operation for the Helmchart. 'install' will always treat the deployment as a new installation, 'upgrade' will always treat it as an upgrade. 'auto' will treat it as an install if no previous release is found, otherwise as an upgrade. This flag is unset by default. When specified, it takes precedence over the value defined in .Values.global._hopsworks.mode One of: `"install"`, `"upgrade"`, `"auto"`, `""`.

`rondb.rondb.priorityClass` <a class="headerlink" href="#helm.rondb.rondb.priorityClass" title="Permanent link">#</a> { #helm.rondb.rondb.priorityClass }
:   Type `string`, default `"rondb-high-priority"`.

`rondb.rondb.serviceAccountAnnotations` <a class="headerlink" href="#helm.rondb.rondb.serviceAccountAnnotations" title="Permanent link">#</a> { #helm.rondb.rondb.serviceAccountAnnotations }
:   Type `object`, default `{}`.

`rondb.rondb.skipMgmdPreUpgradeRollout` <a class="headerlink" href="#helm.rondb.rondb.skipMgmdPreUpgradeRollout" title="Permanent link">#</a> { #helm.rondb.rondb.skipMgmdPreUpgradeRollout }
:   Type `boolean`, default `false`.
    If true, skip the pre-upgrade hook that rolls MGMd to the target image and config before the rest of the chart upgrades. The hook exists to keep at least one ArbitrationRank=1 node reachable while the API tier (mysqld, rdrs) is also rolling, preventing data-node arbitration loss (NDB Error 2305) on chart-wide upgrades. Set this to true only as an escape hatch if the hook itself is misbehaving on your cluster.

`rondb.rondb.staticCpuManagerPolicy` <a class="headerlink" href="#helm.rondb.rondb.staticCpuManagerPolicy" title="Permanent link">#</a> { #helm.rondb.rondb.staticCpuManagerPolicy }
:   Type `boolean`, default `false`.
    Whether the Kubernetes cluster has been configured with a static CPU manager policy. This is an optimization for RonDB data nodes. These have a scheduler which executes jobs within hundreds of microseconds (very quick). If the data nodes are pinned to CPUs, they can run CPU spnning to avoid context switching inbetween jobs.

`rondb.rondb.tls` <a class="headerlink" href="#helm.rondb.rondb.tls" title="Permanent link">#</a> { #helm.rondb.rondb.tls }
:   Type `object`.
    General settings how to use encrypted TLS connections with RonDB APIs (MySQL & RDRS).

`rondb.rondb.tls.caSecretName` <a class="headerlink" href="#helm.rondb.rondb.tls.caSecretName" title="Permanent link">#</a> { #helm.rondb.rondb.tls.caSecretName }
:   Type `string|null`, default `null`.
    User-provided TLS Secret. This can be used by the cert-manager as a base to sign further certificates. If not supplied, cert-manager will use a self-signed CA certificate.

</div>

### backups { #helm-values-rondb-rondb-backups }

??? example "Defaults as YAML"

    ```yaml
    rondb:
      rondb:
        backups:
          enabled: null
          metadataConfigmapName: null
          objectStorageProvider: s3
          pathPrefix: rondb_backup
          s3:
            bucketName: null
            endpoint: null
            keyCredentialsSecret:
              key: null
              name: null
            provider: null
            region: null
            secretCredentialsSecret:
              key: null
              name: null
            serverSideEncryption: null
          schedule: null
          ttl: null
    ```

<div class="hops-values" markdown>

`rondb.rondb.backups` <a class="headerlink" href="#helm.rondb.rondb.backups" title="Permanent link">#</a> { #helm.rondb.rondb.backups }
:   Type `object`.
    Whether, how and how often to run regular backups on the cluster

`rondb.rondb.backups.enabled` <a class="headerlink" href="#helm.rondb.rondb.backups.enabled" title="Permanent link">#</a> { #helm.rondb.rondb.backups.enabled }
:   Type `boolean|null`, default `null`.

`rondb.rondb.backups.metadataConfigmapName` <a class="headerlink" href="#helm.rondb.rondb.backups.metadataConfigmapName" title="Permanent link">#</a> { #helm.rondb.rondb.backups.metadataConfigmapName }
:   Type `string|null`, default `null`.
    The name of the configmap to be used to store the backups metadata information.

`rondb.rondb.backups.objectStorageProvider` <a class="headerlink" href="#helm.rondb.rondb.backups.objectStorageProvider" title="Permanent link">#</a> { #helm.rondb.rondb.backups.objectStorageProvider }
:   Type `enum`, default `"s3"`.
    One of: `"s3"`.

`rondb.rondb.backups.pathPrefix` <a class="headerlink" href="#helm.rondb.rondb.backups.pathPrefix" title="Permanent link">#</a> { #helm.rondb.rondb.backups.pathPrefix }
:   Type `string`, default `"rondb_backup"`.
    Prefix of RonDB backup in the configured bucket

`rondb.rondb.backups.s3` <a class="headerlink" href="#helm.rondb.rondb.backups.s3" title="Permanent link">#</a> { #helm.rondb.rondb.backups.s3 }
:   Type `object`.

`rondb.rondb.backups.s3.bucketName` <a class="headerlink" href="#helm.rondb.rondb.backups.s3.bucketName" title="Permanent link">#</a> { #helm.rondb.rondb.backups.s3.bucketName }
:   Type `string|null`, default `null`.

`rondb.rondb.backups.s3.endpoint` <a class="headerlink" href="#helm.rondb.rondb.backups.s3.endpoint" title="Permanent link">#</a> { #helm.rondb.rondb.backups.s3.endpoint }
:   Type `string|null`, default `null`.

`rondb.rondb.backups.s3.keyCredentialsSecret` <a class="headerlink" href="#helm.rondb.rondb.backups.s3.keyCredentialsSecret" title="Permanent link">#</a> { #helm.rondb.rondb.backups.s3.keyCredentialsSecret }
:   Type `object`.

`rondb.rondb.backups.s3.keyCredentialsSecret.key` <a class="headerlink" href="#helm.rondb.rondb.backups.s3.keyCredentialsSecret.key" title="Permanent link">#</a> { #helm.rondb.rondb.backups.s3.keyCredentialsSecret.key }
:   Type `string|null`, default `null`.
    Key in the Secret

`rondb.rondb.backups.s3.keyCredentialsSecret.name` <a class="headerlink" href="#helm.rondb.rondb.backups.s3.keyCredentialsSecret.name" title="Permanent link">#</a> { #helm.rondb.rondb.backups.s3.keyCredentialsSecret.name }
:   Type `string|null`, default `null`.
    Name of the Secret

`rondb.rondb.backups.s3.provider` <a class="headerlink" href="#helm.rondb.rondb.backups.s3.provider" title="Permanent link">#</a> { #helm.rondb.rondb.backups.s3.provider }
:   Type `string|null`, default `null`.

`rondb.rondb.backups.s3.region` <a class="headerlink" href="#helm.rondb.rondb.backups.s3.region" title="Permanent link">#</a> { #helm.rondb.rondb.backups.s3.region }
:   Type `string|null`, default `null`.

`rondb.rondb.backups.s3.secretCredentialsSecret` <a class="headerlink" href="#helm.rondb.rondb.backups.s3.secretCredentialsSecret" title="Permanent link">#</a> { #helm.rondb.rondb.backups.s3.secretCredentialsSecret }
:   Type `object`.

`rondb.rondb.backups.s3.secretCredentialsSecret.key` <a class="headerlink" href="#helm.rondb.rondb.backups.s3.secretCredentialsSecret.key" title="Permanent link">#</a> { #helm.rondb.rondb.backups.s3.secretCredentialsSecret.key }
:   Type `string|null`, default `null`.
    Key in the Secret

`rondb.rondb.backups.s3.secretCredentialsSecret.name` <a class="headerlink" href="#helm.rondb.rondb.backups.s3.secretCredentialsSecret.name" title="Permanent link">#</a> { #helm.rondb.rondb.backups.s3.secretCredentialsSecret.name }
:   Type `string|null`, default `null`.
    Name of the Secret

`rondb.rondb.backups.s3.serverSideEncryption` <a class="headerlink" href="#helm.rondb.rondb.backups.s3.serverSideEncryption" title="Permanent link">#</a> { #helm.rondb.rondb.backups.s3.serverSideEncryption }
:   Type `enum`, default `null`.
    One of: `"aws:kms"`, `"aws:kms:dsse"`, `"AES256"`, `null`.

`rondb.rondb.backups.schedule` <a class="headerlink" href="#helm.rondb.rondb.backups.schedule" title="Permanent link">#</a> { #helm.rondb.rondb.backups.schedule }
:   Type `string|null`, default `null`.
    Cron schedule for backups

`rondb.rondb.backups.ttl` <a class="headerlink" href="#helm.rondb.rondb.backups.ttl" title="Permanent link">#</a> { #helm.rondb.rondb.backups.ttl }
:   Type `string|null`, default `null`, pattern `^\d+[dh]$`.
    time to live to control when to clean up backups. It is a number followed by either d (days) or h (hours) suffix.

</div>

### benchmarking { #helm-values-rondb-rondb-benchmarking }

??? example "Defaults as YAML"

    ```yaml
    rondb:
      rondb:
        benchmarking:
          dbt2:
            numWarehouses: 4
            runMulti: |-
              # NUM_MYSQL_SERVERS  NUM_WAREHOUSES  NUM_TERMINALS
              2 1 1
              2 2 1
              2 2 2
            runSingle: |-
              # NUM_MYSQL_SERVERS  NUM_WAREHOUSES  NUM_TERMINALS
              1 1 1
              1 2 1
              1 4 1
              1 4 2
          enabled: false
          sysbench:
            minimizeBandwidth: false
            rows: 100000
            threadCountsToRun: 1;2;4;8;12;16;24;32;64
          type: sysbench
          ycsb:
            schemata: CREATE TABLE IF NOT EXISTS ycsb.usertable (YCSB_KEY VARCHAR(255) PRIMARY KEY, FIELD0 varbinary(4096));
    ```

<div class="hops-values" markdown>

`rondb.rondb.benchmarking` <a class="headerlink" href="#helm.rondb.rondb.benchmarking" title="Permanent link">#</a> { #helm.rondb.rondb.benchmarking }
:   Type `object`.
    Whether, which and how to run a benchmarking job on the cluster

`rondb.rondb.benchmarking.dbt2` <a class="headerlink" href="#helm.rondb.rondb.benchmarking.dbt2" title="Permanent link">#</a> { #helm.rondb.rondb.benchmarking.dbt2 }
:   Type `object`.
    Configuration of DBT2 benchmarking job

`rondb.rondb.benchmarking.dbt2.numWarehouses` <a class="headerlink" href="#helm.rondb.rondb.benchmarking.dbt2.numWarehouses" title="Permanent link">#</a> { #helm.rondb.rondb.benchmarking.dbt2.numWarehouses }
:   Type `integer`, default `4`, minimum `1`.

`rondb.rondb.benchmarking.dbt2.runMulti` <a class="headerlink" href="#helm.rondb.rondb.benchmarking.dbt2.runMulti" title="Permanent link">#</a> { #helm.rondb.rondb.benchmarking.dbt2.runMulti }
:   Type `string`, default `"# NUM_MYSQL_SERVERS  NUM_WAREHOUSES  NUM_TERMINALS\n2 1 1\n2 2 1\n2 2 2"`.
    Table with columns: NUM_MYSQL_SERVERS, NUM_WAREHOUSES, NUM_TERMINALS

`rondb.rondb.benchmarking.dbt2.runSingle` <a class="headerlink" href="#helm.rondb.rondb.benchmarking.dbt2.runSingle" title="Permanent link">#</a> { #helm.rondb.rondb.benchmarking.dbt2.runSingle }
:   Type `string`.
    Table with columns: NUM_MYSQL_SERVERS, NUM_WAREHOUSES, NUM_TERMINALS

    ??? note "Default"

        ```yaml
        |-
          # NUM_MYSQL_SERVERS  NUM_WAREHOUSES  NUM_TERMINALS
          1 1 1
          1 2 1
          1 4 1
          1 4 2
        ```

`rondb.rondb.benchmarking.enabled` <a class="headerlink" href="#helm.rondb.rondb.benchmarking.enabled" title="Permanent link">#</a> { #helm.rondb.rondb.benchmarking.enabled }
:   Type `boolean`, default `false`.
    Whether to run a benchmarking job on the cluster

`rondb.rondb.benchmarking.sysbench` <a class="headerlink" href="#helm.rondb.rondb.benchmarking.sysbench" title="Permanent link">#</a> { #helm.rondb.rondb.benchmarking.sysbench }
:   Type `object`.
    Configuration of Sysbench benchmarking job

`rondb.rondb.benchmarking.sysbench.minimizeBandwidth` <a class="headerlink" href="#helm.rondb.rondb.benchmarking.sysbench.minimizeBandwidth" title="Permanent link">#</a> { #helm.rondb.rondb.benchmarking.sysbench.minimizeBandwidth }
:   Type `boolean`, default `false`.
    Whether to use filters to minimize bandwidth usage. This can be useful in cloud environments where bandwidth is expensive.

`rondb.rondb.benchmarking.sysbench.rows` <a class="headerlink" href="#helm.rondb.rondb.benchmarking.sysbench.rows" title="Permanent link">#</a> { #helm.rondb.rondb.benchmarking.sysbench.rows }
:   Type `integer`, default `100000`.

`rondb.rondb.benchmarking.sysbench.threadCountsToRun` <a class="headerlink" href="#helm.rondb.rondb.benchmarking.sysbench.threadCountsToRun" title="Permanent link">#</a> { #helm.rondb.rondb.benchmarking.sysbench.threadCountsToRun }
:   Type `string`, default `"1;2;4;8;12;16;24;32;64"`.
    Semi-colon-separated list of thread counts to run

`rondb.rondb.benchmarking.type` <a class="headerlink" href="#helm.rondb.rondb.benchmarking.type" title="Permanent link">#</a> { #helm.rondb.rondb.benchmarking.type }
:   Type `enum`, default `"sysbench"`.
    Which benchmarking job to run. 'Multi' refers to multiple MySQLd servers to run against One of: `"sysbench"`, `"dbt2_single"`, `"dbt2_multi"`, `"ycsb"`.

`rondb.rondb.benchmarking.ycsb` <a class="headerlink" href="#helm.rondb.rondb.benchmarking.ycsb" title="Permanent link">#</a> { #helm.rondb.rondb.benchmarking.ycsb }
:   Type `object`.
    Configuration of YCSB benchmarking job

`rondb.rondb.benchmarking.ycsb.schemata` <a class="headerlink" href="#helm.rondb.rondb.benchmarking.ycsb.schemata" title="Permanent link">#</a> { #helm.rondb.rondb.benchmarking.ycsb.schemata }
:   Type `string`.
    MySQL table schema to use for YCSB. NOTE: The `ycsb` database is pre-created.

    ??? note "Default"

        ```yaml
        CREATE TABLE IF NOT EXISTS ycsb.usertable (YCSB_KEY VARCHAR(255) PRIMARY KEY, FIELD0 varbinary(4096));
        ```

</div>

### clusterSize { #helm-values-rondb-rondb-clustersize }

??? example "Defaults as YAML"

    ```yaml
    rondb:
      rondb:
        clusterSize:
          activeDataReplicas: 2
          maxNumMySQLServers: 1
          maxNumRdrs: 2
          minNumMySQLServers: 1
          minNumRdrs: 1
          numNodeGroups: 1
    ```

<div class="hops-values" markdown>

`rondb.rondb.clusterSize` <a class="headerlink" href="#helm.rondb.rondb.clusterSize" title="Permanent link">#</a> { #helm.rondb.rondb.clusterSize }
:   Type `object`.
    Horizontal cluster size

`rondb.rondb.clusterSize.activeDataReplicas` <a class="headerlink" href="#helm.rondb.rondb.clusterSize.activeDataReplicas" title="Permanent link">#</a> { #helm.rondb.rondb.clusterSize.activeDataReplicas }
:   Type `integer`, default `2`, minimum `1`, maximum `3`.
    How many replicas each node group has. When descreasing this value, try going down by 1 at a time. Too many nodes leaving at once can cause issues with leader elections.

`rondb.rondb.clusterSize.maxNumMySQLServers` <a class="headerlink" href="#helm.rondb.rondb.clusterSize.maxNumMySQLServers" title="Permanent link">#</a> { #helm.rondb.rondb.clusterSize.maxNumMySQLServers }
:   Type `integer`, default `1`, Hopsworks overrides the `rondb` chart default `5`, minimum `1`.
    The maximum amount of MySQL servers we will auto-scale to. It is represented as number of slots in RonDB's config.ini. Changing this will only take effect if the ConfigMap for config.ini is updated and the MGMd is restarted.

`rondb.rondb.clusterSize.maxNumRdrs` <a class="headerlink" href="#helm.rondb.rondb.clusterSize.maxNumRdrs" title="Permanent link">#</a> { #helm.rondb.rondb.clusterSize.maxNumRdrs }
:   Type `integer`, default `2`, minimum `0`.

`rondb.rondb.clusterSize.minNumMySQLServers` <a class="headerlink" href="#helm.rondb.rondb.clusterSize.minNumMySQLServers" title="Permanent link">#</a> { #helm.rondb.rondb.clusterSize.minNumMySQLServers }
:   Type `integer`, default `1`, minimum `1`.
    A minimum amount of MySQL servers

`rondb.rondb.clusterSize.minNumRdrs` <a class="headerlink" href="#helm.rondb.rondb.clusterSize.minNumRdrs" title="Permanent link">#</a> { #helm.rondb.rondb.clusterSize.minNumRdrs }
:   Type `integer`, default `1`, minimum `0`.

`rondb.rondb.clusterSize.numNodeGroups` <a class="headerlink" href="#helm.rondb.rondb.clusterSize.numNodeGroups" title="Permanent link">#</a> { #helm.rondb.rondb.clusterSize.numNodeGroups }
:   Type `integer`, default `1`, minimum `1`.
    Number of RonDB node groups. Immutable after install — RonDB has no online add/remove. Changing it requires uninstall and reinstall with restoreFromBackup.backupId. Set `mode: upgrade` for ArgoCD or other template-only renderers so the immutability check runs as an in-cluster Job.

</div>

### globalReplication { #helm-values-rondb-rondb-globalreplication }

??? example "Defaults as YAML"

    ```yaml
    rondb:
      rondb:
        globalReplication:
          clusterNumber: 1
          primary:
            binlogFilename: binlog
            enabled: false
            expireBinlogsDays: 1.5
            ignoreDatabases: []
            includeDatabases: []
            logReplicaUpdates: false
            maxNumBinlogServers: 2
            numBinlogServers: 2
          secondary:
            enabled: false
            replicateFrom:
              binlogServerHosts: []
              clusterNumber: 2
              ignoreDatabases: []
              ignoreTables: []
              includeDatabases: []
              includeTables: []
              useTlsConnection: false
    ```

<div class="hops-values" markdown>

`rondb.rondb.globalReplication` <a class="headerlink" href="#helm.rondb.rondb.globalReplication" title="Permanent link">#</a> { #helm.rondb.rondb.globalReplication }
:   Type `object`.

`rondb.rondb.globalReplication.clusterNumber` <a class="headerlink" href="#helm.rondb.rondb.globalReplication.clusterNumber" title="Permanent link">#</a> { #helm.rondb.rondb.globalReplication.clusterNumber }
:   Type `number`, default `1`.
    Determines the offset for global server IDs

`rondb.rondb.globalReplication.primary` <a class="headerlink" href="#helm.rondb.rondb.globalReplication.primary" title="Permanent link">#</a> { #helm.rondb.rondb.globalReplication.primary }
:   Type `object`.

`rondb.rondb.globalReplication.primary.binlogFilename` <a class="headerlink" href="#helm.rondb.rondb.globalReplication.primary.binlogFilename" title="Permanent link">#</a> { #helm.rondb.rondb.globalReplication.primary.binlogFilename }
:   Type `string`, default `"binlog"`.

`rondb.rondb.globalReplication.primary.enabled` <a class="headerlink" href="#helm.rondb.rondb.globalReplication.primary.enabled" title="Permanent link">#</a> { #helm.rondb.rondb.globalReplication.primary.enabled }
:   Type `boolean`, default `false`.
    Specifies if the primary replication is enabled. This will actually create the binary log servers. Can be activated after an initial start.

`rondb.rondb.globalReplication.primary.expireBinlogsDays` <a class="headerlink" href="#helm.rondb.rondb.globalReplication.primary.expireBinlogsDays" title="Permanent link">#</a> { #helm.rondb.rondb.globalReplication.primary.expireBinlogsDays }
:   Type `number`, default `1.5`.

`rondb.rondb.globalReplication.primary.ignoreDatabases` <a class="headerlink" href="#helm.rondb.rondb.globalReplication.primary.ignoreDatabases" title="Permanent link">#</a> { #helm.rondb.rondb.globalReplication.primary.ignoreDatabases }
:   Type `array`, default `[]`.

`rondb.rondb.globalReplication.primary.includeDatabases` <a class="headerlink" href="#helm.rondb.rondb.globalReplication.primary.includeDatabases" title="Permanent link">#</a> { #helm.rondb.rondb.globalReplication.primary.includeDatabases }
:   Type `array`, default `[]`.

`rondb.rondb.globalReplication.primary.logReplicaUpdates` <a class="headerlink" href="#helm.rondb.rondb.globalReplication.primary.logReplicaUpdates" title="Permanent link">#</a> { #helm.rondb.rondb.globalReplication.primary.logReplicaUpdates }
:   Type `boolean`, default `false`.

`rondb.rondb.globalReplication.primary.maxNumBinlogServers` <a class="headerlink" href="#helm.rondb.rondb.globalReplication.primary.maxNumBinlogServers" title="Permanent link">#</a> { #helm.rondb.rondb.globalReplication.primary.maxNumBinlogServers }
:   Type `number`, default `2`.
    Don't change this value. Determines how many binlog servers we can scale out to. Used to determine the server IDs for global replication. Even if replication is disabled, potential binlog servers will be written into the config.ini.

`rondb.rondb.globalReplication.primary.numBinlogServers` <a class="headerlink" href="#helm.rondb.rondb.globalReplication.primary.numBinlogServers" title="Permanent link">#</a> { #helm.rondb.rondb.globalReplication.primary.numBinlogServers }
:   Type `number`, default `2`.
    The current number of binlog servers, given global Replication is enabled.

`rondb.rondb.globalReplication.secondary` <a class="headerlink" href="#helm.rondb.rondb.globalReplication.secondary" title="Permanent link">#</a> { #helm.rondb.rondb.globalReplication.secondary }
:   Type `object`.

`rondb.rondb.globalReplication.secondary.enabled` <a class="headerlink" href="#helm.rondb.rondb.globalReplication.secondary.enabled" title="Permanent link">#</a> { #helm.rondb.rondb.globalReplication.secondary.enabled }
:   Type `boolean`, default `false`.

`rondb.rondb.globalReplication.secondary.replicateFrom` <a class="headerlink" href="#helm.rondb.rondb.globalReplication.secondary.replicateFrom" title="Permanent link">#</a> { #helm.rondb.rondb.globalReplication.secondary.replicateFrom }
:   Type `object`.
    RonDB clusters to replicate from. RonDB supports merge-replicating from multiple clusters, but we only support replicating from one cluster

`rondb.rondb.globalReplication.secondary.replicateFrom.binlogServerHosts` <a class="headerlink" href="#helm.rondb.rondb.globalReplication.secondary.replicateFrom.binlogServerHosts" title="Permanent link">#</a> { #helm.rondb.rondb.globalReplication.secondary.replicateFrom.binlogServerHosts }
:   Type `array`, default `[]`.
    Hostnames of the binlog server to replicate from. The binlog servers have headless ClusterIPs and one LoadBalancer *per* binlog server. If we replicate across different K8s clusters, we can reference the External IPs of the binlog servers' LoadBalancers here.

`rondb.rondb.globalReplication.secondary.replicateFrom.clusterNumber` <a class="headerlink" href="#helm.rondb.rondb.globalReplication.secondary.replicateFrom.clusterNumber" title="Permanent link">#</a> { #helm.rondb.rondb.globalReplication.secondary.replicateFrom.clusterNumber }
:   Type `number`, default `2`.
    A helper to understand from which serverIds to replicate from

`rondb.rondb.globalReplication.secondary.replicateFrom.ignoreDatabases` <a class="headerlink" href="#helm.rondb.rondb.globalReplication.secondary.replicateFrom.ignoreDatabases" title="Permanent link">#</a> { #helm.rondb.rondb.globalReplication.secondary.replicateFrom.ignoreDatabases }
:   Type `array`, default `[]`.

`rondb.rondb.globalReplication.secondary.replicateFrom.ignoreTables` <a class="headerlink" href="#helm.rondb.rondb.globalReplication.secondary.replicateFrom.ignoreTables" title="Permanent link">#</a> { #helm.rondb.rondb.globalReplication.secondary.replicateFrom.ignoreTables }
:   Type `array`, default `[]`.

`rondb.rondb.globalReplication.secondary.replicateFrom.includeDatabases` <a class="headerlink" href="#helm.rondb.rondb.globalReplication.secondary.replicateFrom.includeDatabases" title="Permanent link">#</a> { #helm.rondb.rondb.globalReplication.secondary.replicateFrom.includeDatabases }
:   Type `array`, default `[]`.

`rondb.rondb.globalReplication.secondary.replicateFrom.includeTables` <a class="headerlink" href="#helm.rondb.rondb.globalReplication.secondary.replicateFrom.includeTables" title="Permanent link">#</a> { #helm.rondb.rondb.globalReplication.secondary.replicateFrom.includeTables }
:   Type `array`, default `[]`.

`rondb.rondb.globalReplication.secondary.replicateFrom.useTlsConnection` <a class="headerlink" href="#helm.rondb.rondb.globalReplication.secondary.replicateFrom.useTlsConnection" title="Permanent link">#</a> { #helm.rondb.rondb.globalReplication.secondary.replicateFrom.useTlsConnection }
:   Type `boolean`, default `false`.
    Enable this for an encrypted replication channel. Important if the binlog server requires TLS connections

</div>

### images { #helm-values-rondb-rondb-images }

??? example "Defaults as YAML"

    ```yaml
    rondb:
      rondb:
        images:
          dataValidation:
            name: python
            registry: docker.io
            repository: ''
            tag: 3.12-slim
          mysqldExporter:
            name: mysqld_exporter
            registry: docker.hops.works
            repository: hopsworks
            tag: 0.11.5
          rondb:
            name: rondb
            registry: docker.hops.works
            repository: hopsworks
            tag: 26.02.11
          toolbox:
            name: hwutils
            registry: docker.hops.works
            repository: hopsworks
            tag: 1.10-SNAPSHOT
          upgrade2410revokegrants:
            name: rondb
            registry: docker.io
            repository: hopsworks
            tag: 22.10.13-0.7
    ```

<div class="hops-values" markdown>

`rondb.rondb.images` <a class="headerlink" href="#helm.rondb.rondb.images" title="Permanent link">#</a> { #helm.rondb.rondb.images }
:   Type `object`.
    Information for Docker images used in the cluster

`rondb.rondb.images.dataValidation` <a class="headerlink" href="#helm.rondb.rondb.images.dataValidation" title="Permanent link">#</a> { #helm.rondb.rondb.images.dataValidation }
:   Type `object`.

`rondb.rondb.images.dataValidation.name` <a class="headerlink" href="#helm.rondb.rondb.images.dataValidation.name" title="Permanent link">#</a> { #helm.rondb.rondb.images.dataValidation.name }
:   Type `string`, default `"python"`.

`rondb.rondb.images.dataValidation.registry` <a class="headerlink" href="#helm.rondb.rondb.images.dataValidation.registry" title="Permanent link">#</a> { #helm.rondb.rondb.images.dataValidation.registry }
:   Type `string`, default `"docker.io"`.

`rondb.rondb.images.dataValidation.repository` <a class="headerlink" href="#helm.rondb.rondb.images.dataValidation.repository" title="Permanent link">#</a> { #helm.rondb.rondb.images.dataValidation.repository }
:   Type `string`, default `""`.

`rondb.rondb.images.dataValidation.tag` <a class="headerlink" href="#helm.rondb.rondb.images.dataValidation.tag" title="Permanent link">#</a> { #helm.rondb.rondb.images.dataValidation.tag }
:   Type `string`, default `"3.12-slim"`.

`rondb.rondb.images.mysqldExporter` <a class="headerlink" href="#helm.rondb.rondb.images.mysqldExporter" title="Permanent link">#</a> { #helm.rondb.rondb.images.mysqldExporter }
:   Type `object`.

`rondb.rondb.images.mysqldExporter.name` <a class="headerlink" href="#helm.rondb.rondb.images.mysqldExporter.name" title="Permanent link">#</a> { #helm.rondb.rondb.images.mysqldExporter.name }
:   Type `string`, default `"mysqld_exporter"`.

`rondb.rondb.images.mysqldExporter.registry` <a class="headerlink" href="#helm.rondb.rondb.images.mysqldExporter.registry" title="Permanent link">#</a> { #helm.rondb.rondb.images.mysqldExporter.registry }
:   Type `string`, default `"docker.hops.works"`.

`rondb.rondb.images.mysqldExporter.repository` <a class="headerlink" href="#helm.rondb.rondb.images.mysqldExporter.repository" title="Permanent link">#</a> { #helm.rondb.rondb.images.mysqldExporter.repository }
:   Type `string`, default `"hopsworks"`.

`rondb.rondb.images.mysqldExporter.tag` <a class="headerlink" href="#helm.rondb.rondb.images.mysqldExporter.tag" title="Permanent link">#</a> { #helm.rondb.rondb.images.mysqldExporter.tag }
:   Type `string`, default `"0.11.5"`.

`rondb.rondb.images.rondb` <a class="headerlink" href="#helm.rondb.rondb.images.rondb" title="Permanent link">#</a> { #helm.rondb.rondb.images.rondb }
:   Type `object`.

`rondb.rondb.images.rondb.name` <a class="headerlink" href="#helm.rondb.rondb.images.rondb.name" title="Permanent link">#</a> { #helm.rondb.rondb.images.rondb.name }
:   Type `string`, default `"rondb"`.

`rondb.rondb.images.rondb.registry` <a class="headerlink" href="#helm.rondb.rondb.images.rondb.registry" title="Permanent link">#</a> { #helm.rondb.rondb.images.rondb.registry }
:   Type `string`, default `"docker.hops.works"`, Hopsworks overrides the `rondb` chart default `"docker.io"`.

`rondb.rondb.images.rondb.repository` <a class="headerlink" href="#helm.rondb.rondb.images.rondb.repository" title="Permanent link">#</a> { #helm.rondb.rondb.images.rondb.repository }
:   Type `string`, default `"hopsworks"`.

`rondb.rondb.images.rondb.tag` <a class="headerlink" href="#helm.rondb.rondb.images.rondb.tag" title="Permanent link">#</a> { #helm.rondb.rondb.images.rondb.tag }
:   Type `string`, default `"26.02.11"`.
    The version of RonDB to use; This should always be equivalent to .Chart.AppVersion

`rondb.rondb.images.toolbox` <a class="headerlink" href="#helm.rondb.rondb.images.toolbox" title="Permanent link">#</a> { #helm.rondb.rondb.images.toolbox }
:   Type `object`.

`rondb.rondb.images.toolbox.name` <a class="headerlink" href="#helm.rondb.rondb.images.toolbox.name" title="Permanent link">#</a> { #helm.rondb.rondb.images.toolbox.name }
:   Type `string`, default `"hwutils"`.

`rondb.rondb.images.toolbox.registry` <a class="headerlink" href="#helm.rondb.rondb.images.toolbox.registry" title="Permanent link">#</a> { #helm.rondb.rondb.images.toolbox.registry }
:   Type `string`, default `"docker.hops.works"`, Hopsworks overrides the `rondb` chart default `"docker.io"`.

`rondb.rondb.images.toolbox.repository` <a class="headerlink" href="#helm.rondb.rondb.images.toolbox.repository" title="Permanent link">#</a> { #helm.rondb.rondb.images.toolbox.repository }
:   Type `string`, default `"hopsworks"`.

`rondb.rondb.images.toolbox.tag` <a class="headerlink" href="#helm.rondb.rondb.images.toolbox.tag" title="Permanent link">#</a> { #helm.rondb.rondb.images.toolbox.tag }
:   Type `string`, default `"1.10-SNAPSHOT"`, Hopsworks overrides the `rondb` chart default `"1.7"`.

`rondb.rondb.images.upgrade2410revokegrants` <a class="headerlink" href="#helm.rondb.rondb.images.upgrade2410revokegrants" title="Permanent link">#</a> { #helm.rondb.rondb.images.upgrade2410revokegrants }
:   Type `object`.

`rondb.rondb.images.upgrade2410revokegrants.name` <a class="headerlink" href="#helm.rondb.rondb.images.upgrade2410revokegrants.name" title="Permanent link">#</a> { #helm.rondb.rondb.images.upgrade2410revokegrants.name }
:   Type `string`, default `"rondb"`.

`rondb.rondb.images.upgrade2410revokegrants.registry` <a class="headerlink" href="#helm.rondb.rondb.images.upgrade2410revokegrants.registry" title="Permanent link">#</a> { #helm.rondb.rondb.images.upgrade2410revokegrants.registry }
:   Type `string`, default `"docker.io"`.

`rondb.rondb.images.upgrade2410revokegrants.repository` <a class="headerlink" href="#helm.rondb.rondb.images.upgrade2410revokegrants.repository" title="Permanent link">#</a> { #helm.rondb.rondb.images.upgrade2410revokegrants.repository }
:   Type `string`, default `"hopsworks"`.

`rondb.rondb.images.upgrade2410revokegrants.tag` <a class="headerlink" href="#helm.rondb.rondb.images.upgrade2410revokegrants.tag" title="Permanent link">#</a> { #helm.rondb.rondb.images.upgrade2410revokegrants.tag }
:   Type `string`, default `"22.10.13-0.7"`.
    The version of RonDB to use when revoking bogus user privilege to upgrade from 22.10 to 24.10

</div>

### meta { #helm-values-rondb-rondb-meta }

??? example "Defaults as YAML"

    ```yaml
    rondb:
      rondb:
        meta:
          binlogServers:
            externalLoadBalancers:
              annotations: {}
              class: null
              enabled: true
              namePrefix: binlog-server
              port: 3306
            headlessClusterIp:
              name: headless-binlog-servers
              port: 3306
            statefulSet:
              endToEndTls:
                enabled: false
                filenames:
                  ca: null
                  cert: tls.crt
                  key: tls.key
                secretName: binlog-end-to-end-tls
                supplyOwnSecret: false
              name: mysqld-binlog-servers
          ddlMySQLd:
            addSysNiceCapability: true
            clusterIp:
              annotations:
                consul.hashicorp.com/service-name: mysqlddl
                consul.hashicorp.com/service-tags: onlinefs
              name: ddl-mysqld
              port: 3306
            enabled: true
            headlessClusterIp:
              name: headless-ddl-mysqld
              port: 3306
            statefulSet:
              endToEndTls:
                enabled: false
                filenames:
                  ca: hops_root_ca.pem
                  cert: mysqlddl_certificate_bundle.pem
                  key: mysqlddl_priv.pem
                secretName: mysqlddl-crypto-material
                supplyOwnSecret: true
              name: ddl-mysqld
          mgmd:
            headlessClusterIp:
              annotations:
                consul.hashicorp.com/service-name: mgmd
              name: headless-mgmds
              port: 1186
            statefulSetName: mgmds
          mysqld:
            addSysNiceCapability: true
            clusterIp:
              annotations:
                consul.hashicorp.com/service-name: mysql
                consul.hashicorp.com/service-tags: onlinefs
              name: mysqld
              port: 3306
            exporter:
              metricsPort: 9104
            externalLoadBalancer:
              annotations: {}
              class: null
              enabled: true
              managed: true
              name: mysqld-external
              nodePort: null
              nodeSelector: {}
              port: 3306
            headlessClusterIp:
              name: headless-mysqlds
              port: 3306
            statefulSet:
              endToEndTls:
                enabled: false
                filenames:
                  ca: hops_root_ca.pem
                  cert: mysql_certificate_bundle.pem
                  key: mysql_priv.pem
                secretName: mysqld-crypto-material
                supplyOwnSecret: true
              name: mysqlds
          ndbmtd:
            statefulSet:
              podAnnotations: {}
          rdrs:
            clusterIp:
              annotations:
                consul.hashicorp.com/service-name: rdrs
                prometheus.io/path: /metrics
                prometheus.io/port: '4406'
                prometheus.io/scheme: https
                prometheus.io/scrape: 'true'
              name: rdrs
            externalLoadBalancer:
              annotations: {}
              class: null
              enabled: true
              managed: true
              name: rdrs-external
              nodePort: null
              nodeSelector: {}
            headlessClusterIpName: rdrs-cluster-ip
            ingress:
              class: nginx
              dnsNames: []
              enabled: false
              tls:
                enabled: true
                ipAddresses: []
              useDefaultBackend: true
            statefulSet:
              endToEndTls:
                enabled: true
                filenames:
                  ca: hops_root_ca.pem
                  cert: mysql_certificate_bundle.pem
                  key: mysql_priv.pem
                secretName: rdrs-crypto-material
                supplyOwnSecret: true
              name: rdrs
          replicaAppliers:
            headlessClusterIp:
              name: headless-replica-appliers
              port: 3306
            statefulSet:
              endToEndTls:
                enabled: false
                filenames:
                  ca: null
                  cert: tls.crt
                  key: tls.key
                secretName: replica-applier-end-to-end-tls
                supplyOwnSecret: false
              name: mysqld-replica-appliers
    ```

<div class="hops-values" markdown>

`rondb.rondb.meta` <a class="headerlink" href="#helm.rondb.rondb.meta" title="Permanent link">#</a> { #helm.rondb.rondb.meta }
:   Type `object`.

`rondb.rondb.meta.binlogServers` <a class="headerlink" href="#helm.rondb.rondb.meta.binlogServers" title="Permanent link">#</a> { #helm.rondb.rondb.meta.binlogServers }
:   Type `object`.

`rondb.rondb.meta.binlogServers.externalLoadBalancers` <a class="headerlink" href="#helm.rondb.rondb.meta.binlogServers.externalLoadBalancers" title="Permanent link">#</a> { #helm.rondb.rondb.meta.binlogServers.externalLoadBalancers }
:   Type `object`.
    One LoadBalancer per binlog server; Creating an (alternative) Ingress per binlog server is difficult

`rondb.rondb.meta.binlogServers.externalLoadBalancers.annotations` <a class="headerlink" href="#helm.rondb.rondb.meta.binlogServers.externalLoadBalancers.annotations" title="Permanent link">#</a> { #helm.rondb.rondb.meta.binlogServers.externalLoadBalancers.annotations }
:   Type `object`, default `{}`.
    Cloud provider load balancer specific annotations.

`rondb.rondb.meta.binlogServers.externalLoadBalancers.class` <a class="headerlink" href="#helm.rondb.rondb.meta.binlogServers.externalLoadBalancers.class" title="Permanent link">#</a> { #helm.rondb.rondb.meta.binlogServers.externalLoadBalancers.class }
:   Type `string|null`, default `null`.

`rondb.rondb.meta.binlogServers.externalLoadBalancers.enabled` <a class="headerlink" href="#helm.rondb.rondb.meta.binlogServers.externalLoadBalancers.enabled" title="Permanent link">#</a> { #helm.rondb.rondb.meta.binlogServers.externalLoadBalancers.enabled }
:   Type `boolean`, default `true`.

`rondb.rondb.meta.binlogServers.externalLoadBalancers.namePrefix` <a class="headerlink" href="#helm.rondb.rondb.meta.binlogServers.externalLoadBalancers.namePrefix" title="Permanent link">#</a> { #helm.rondb.rondb.meta.binlogServers.externalLoadBalancers.namePrefix }
:   Type `string`, default `"binlog-server"`.

`rondb.rondb.meta.binlogServers.externalLoadBalancers.port` <a class="headerlink" href="#helm.rondb.rondb.meta.binlogServers.externalLoadBalancers.port" title="Permanent link">#</a> { #helm.rondb.rondb.meta.binlogServers.externalLoadBalancers.port }
:   Type `integer`, default `3306`.
    Port to expose the service on

`rondb.rondb.meta.binlogServers.headlessClusterIp` <a class="headerlink" href="#helm.rondb.rondb.meta.binlogServers.headlessClusterIp" title="Permanent link">#</a> { #helm.rondb.rondb.meta.binlogServers.headlessClusterIp }
:   Type `object`.

`rondb.rondb.meta.binlogServers.headlessClusterIp.name` <a class="headerlink" href="#helm.rondb.rondb.meta.binlogServers.headlessClusterIp.name" title="Permanent link">#</a> { #helm.rondb.rondb.meta.binlogServers.headlessClusterIp.name }
:   Type `string`, default `"headless-binlog-servers"`.

`rondb.rondb.meta.binlogServers.headlessClusterIp.port` <a class="headerlink" href="#helm.rondb.rondb.meta.binlogServers.headlessClusterIp.port" title="Permanent link">#</a> { #helm.rondb.rondb.meta.binlogServers.headlessClusterIp.port }
:   Type `integer`, default `3306`.

`rondb.rondb.meta.binlogServers.statefulSet` <a class="headerlink" href="#helm.rondb.rondb.meta.binlogServers.statefulSet" title="Permanent link">#</a> { #helm.rondb.rondb.meta.binlogServers.statefulSet }
:   Type `object`.

`rondb.rondb.meta.binlogServers.statefulSet.endToEndTls` <a class="headerlink" href="#helm.rondb.rondb.meta.binlogServers.statefulSet.endToEndTls" title="Permanent link">#</a> { #helm.rondb.rondb.meta.binlogServers.statefulSet.endToEndTls }
:   Type `object`.

`rondb.rondb.meta.binlogServers.statefulSet.endToEndTls.enabled` <a class="headerlink" href="#helm.rondb.rondb.meta.binlogServers.statefulSet.endToEndTls.enabled" title="Permanent link">#</a> { #helm.rondb.rondb.meta.binlogServers.statefulSet.endToEndTls.enabled }
:   default `false`.
    Whether to use end-to-end encryption for MySQL binlog server Pods. This is recommended for high-security use cases. For MySQLds this is especially recommended since they use raw TCP connections and thereby by-pass TLS Ingress-rules. Otherwise, Ingress-TCP can also be configured directly via the Ingress controller (not in this Helmchart).

`rondb.rondb.meta.binlogServers.statefulSet.endToEndTls.filenames` <a class="headerlink" href="#helm.rondb.rondb.meta.binlogServers.statefulSet.endToEndTls.filenames" title="Permanent link">#</a> { #helm.rondb.rondb.meta.binlogServers.statefulSet.endToEndTls.filenames }
:   Type `object`.

`rondb.rondb.meta.binlogServers.statefulSet.endToEndTls.filenames.ca` <a class="headerlink" href="#helm.rondb.rondb.meta.binlogServers.statefulSet.endToEndTls.filenames.ca" title="Permanent link">#</a> { #helm.rondb.rondb.meta.binlogServers.statefulSet.endToEndTls.filenames.ca }
:   Type `string|null`, default `null`.
    Name of the CA file in the Secret. ONLY overwrite this if you're not using standard TLS Secrets.

`rondb.rondb.meta.binlogServers.statefulSet.endToEndTls.filenames.cert` <a class="headerlink" href="#helm.rondb.rondb.meta.binlogServers.statefulSet.endToEndTls.filenames.cert" title="Permanent link">#</a> { #helm.rondb.rondb.meta.binlogServers.statefulSet.endToEndTls.filenames.cert }
:   Type `string`, default `"tls.crt"`.
    Name of the certificate file in the Secret. ONLY overwrite this if you're not using standard TLS Secrets.

`rondb.rondb.meta.binlogServers.statefulSet.endToEndTls.filenames.key` <a class="headerlink" href="#helm.rondb.rondb.meta.binlogServers.statefulSet.endToEndTls.filenames.key" title="Permanent link">#</a> { #helm.rondb.rondb.meta.binlogServers.statefulSet.endToEndTls.filenames.key }
:   Type `string`, default `"tls.key"`.
    Name of the key file in the Secret. ONLY overwrite this if you're not using standard TLS Secrets.

`rondb.rondb.meta.binlogServers.statefulSet.endToEndTls.secretName` <a class="headerlink" href="#helm.rondb.rondb.meta.binlogServers.statefulSet.endToEndTls.secretName" title="Permanent link">#</a> { #helm.rondb.rondb.meta.binlogServers.statefulSet.endToEndTls.secretName }
:   Type `string`, default `"binlog-end-to-end-tls"`.
    Name of the TLS Secret

`rondb.rondb.meta.binlogServers.statefulSet.endToEndTls.supplyOwnSecret` <a class="headerlink" href="#helm.rondb.rondb.meta.binlogServers.statefulSet.endToEndTls.supplyOwnSecret" title="Permanent link">#</a> { #helm.rondb.rondb.meta.binlogServers.statefulSet.endToEndTls.supplyOwnSecret }
:   default `false`.
    Whether the Helmchart user will create a TLS Secret outside of this Helmchart. Otherwise we rely on cert-manager to create one.

`rondb.rondb.meta.binlogServers.statefulSet.name` <a class="headerlink" href="#helm.rondb.rondb.meta.binlogServers.statefulSet.name" title="Permanent link">#</a> { #helm.rondb.rondb.meta.binlogServers.statefulSet.name }
:   Type `string`, default `"mysqld-binlog-servers"`.

`rondb.rondb.meta.ddlMySQLd` <a class="headerlink" href="#helm.rondb.rondb.meta.ddlMySQLd" title="Permanent link">#</a> { #helm.rondb.rondb.meta.ddlMySQLd }
:   Type `object`.

`rondb.rondb.meta.ddlMySQLd.addSysNiceCapability` <a class="headerlink" href="#helm.rondb.rondb.meta.ddlMySQLd.addSysNiceCapability" title="Permanent link">#</a> { #helm.rondb.rondb.meta.ddlMySQLd.addSysNiceCapability }
:   Type `boolean`, default `true`.

`rondb.rondb.meta.ddlMySQLd.clusterIp` <a class="headerlink" href="#helm.rondb.rondb.meta.ddlMySQLd.clusterIp" title="Permanent link">#</a> { #helm.rondb.rondb.meta.ddlMySQLd.clusterIp }
:   Type `object`.

`rondb.rondb.meta.ddlMySQLd.clusterIp.annotations` <a class="headerlink" href="#helm.rondb.rondb.meta.ddlMySQLd.clusterIp.annotations" title="Permanent link">#</a> { #helm.rondb.rondb.meta.ddlMySQLd.clusterIp.annotations }
:   Type `object`, Hopsworks overrides the `rondb` chart default `{}`.

    ??? note "Default"

        ```yaml
        consul.hashicorp.com/service-name: mysqlddl
        consul.hashicorp.com/service-tags: onlinefs
        ```

`rondb.rondb.meta.ddlMySQLd.clusterIp.name` <a class="headerlink" href="#helm.rondb.rondb.meta.ddlMySQLd.clusterIp.name" title="Permanent link">#</a> { #helm.rondb.rondb.meta.ddlMySQLd.clusterIp.name }
:   Type `string`, default `"ddl-mysqld"`.

`rondb.rondb.meta.ddlMySQLd.clusterIp.port` <a class="headerlink" href="#helm.rondb.rondb.meta.ddlMySQLd.clusterIp.port" title="Permanent link">#</a> { #helm.rondb.rondb.meta.ddlMySQLd.clusterIp.port }
:   Type `integer`, default `3306`.

`rondb.rondb.meta.ddlMySQLd.enabled` <a class="headerlink" href="#helm.rondb.rondb.meta.ddlMySQLd.enabled" title="Permanent link">#</a> { #helm.rondb.rondb.meta.ddlMySQLd.enabled }
:   Type `boolean`, default `true`, Hopsworks overrides the `rondb` chart default `false`.
    Whether to deploy the DDL MySQLd StatefulSet and reserve its NDB node slot.

`rondb.rondb.meta.ddlMySQLd.headlessClusterIp` <a class="headerlink" href="#helm.rondb.rondb.meta.ddlMySQLd.headlessClusterIp" title="Permanent link">#</a> { #helm.rondb.rondb.meta.ddlMySQLd.headlessClusterIp }
:   Type `object`.

`rondb.rondb.meta.ddlMySQLd.headlessClusterIp.name` <a class="headerlink" href="#helm.rondb.rondb.meta.ddlMySQLd.headlessClusterIp.name" title="Permanent link">#</a> { #helm.rondb.rondb.meta.ddlMySQLd.headlessClusterIp.name }
:   Type `string`, default `"headless-ddl-mysqld"`.

`rondb.rondb.meta.ddlMySQLd.headlessClusterIp.port` <a class="headerlink" href="#helm.rondb.rondb.meta.ddlMySQLd.headlessClusterIp.port" title="Permanent link">#</a> { #helm.rondb.rondb.meta.ddlMySQLd.headlessClusterIp.port }
:   Type `integer`, default `3306`.

`rondb.rondb.meta.ddlMySQLd.statefulSet` <a class="headerlink" href="#helm.rondb.rondb.meta.ddlMySQLd.statefulSet" title="Permanent link">#</a> { #helm.rondb.rondb.meta.ddlMySQLd.statefulSet }
:   Type `object`.

`rondb.rondb.meta.ddlMySQLd.statefulSet.endToEndTls` <a class="headerlink" href="#helm.rondb.rondb.meta.ddlMySQLd.statefulSet.endToEndTls" title="Permanent link">#</a> { #helm.rondb.rondb.meta.ddlMySQLd.statefulSet.endToEndTls }
:   Type `object`.

`rondb.rondb.meta.ddlMySQLd.statefulSet.endToEndTls.enabled` <a class="headerlink" href="#helm.rondb.rondb.meta.ddlMySQLd.statefulSet.endToEndTls.enabled" title="Permanent link">#</a> { #helm.rondb.rondb.meta.ddlMySQLd.statefulSet.endToEndTls.enabled }
:   Type `boolean`, default `false`.
    Whether to use end-to-end encryption for DDL MySQL server Pods.

`rondb.rondb.meta.ddlMySQLd.statefulSet.endToEndTls.filenames` <a class="headerlink" href="#helm.rondb.rondb.meta.ddlMySQLd.statefulSet.endToEndTls.filenames" title="Permanent link">#</a> { #helm.rondb.rondb.meta.ddlMySQLd.statefulSet.endToEndTls.filenames }
:   Type `object`.

`rondb.rondb.meta.ddlMySQLd.statefulSet.endToEndTls.filenames.ca` <a class="headerlink" href="#helm.rondb.rondb.meta.ddlMySQLd.statefulSet.endToEndTls.filenames.ca" title="Permanent link">#</a> { #helm.rondb.rondb.meta.ddlMySQLd.statefulSet.endToEndTls.filenames.ca }
:   Type `string|null`, default `"hops_root_ca.pem"`, Hopsworks overrides the `rondb` chart default `null`.
    Name of the CA file in the Secret. ONLY overwrite this if you're not using standard TLS Secrets.

`rondb.rondb.meta.ddlMySQLd.statefulSet.endToEndTls.filenames.cert` <a class="headerlink" href="#helm.rondb.rondb.meta.ddlMySQLd.statefulSet.endToEndTls.filenames.cert" title="Permanent link">#</a> { #helm.rondb.rondb.meta.ddlMySQLd.statefulSet.endToEndTls.filenames.cert }
:   Type `string`, default `"mysqlddl_certificate_bundle.pem"`, Hopsworks overrides the `rondb` chart default `"tls.crt"`.
    Name of the certificate file in the Secret. ONLY overwrite this if you're not using standard TLS Secrets.

`rondb.rondb.meta.ddlMySQLd.statefulSet.endToEndTls.filenames.key` <a class="headerlink" href="#helm.rondb.rondb.meta.ddlMySQLd.statefulSet.endToEndTls.filenames.key" title="Permanent link">#</a> { #helm.rondb.rondb.meta.ddlMySQLd.statefulSet.endToEndTls.filenames.key }
:   Type `string`, default `"mysqlddl_priv.pem"`, Hopsworks overrides the `rondb` chart default `"tls.key"`.
    Name of the key file in the Secret. ONLY overwrite this if you're not using standard TLS Secrets.

`rondb.rondb.meta.ddlMySQLd.statefulSet.endToEndTls.secretName` <a class="headerlink" href="#helm.rondb.rondb.meta.ddlMySQLd.statefulSet.endToEndTls.secretName" title="Permanent link">#</a> { #helm.rondb.rondb.meta.ddlMySQLd.statefulSet.endToEndTls.secretName }
:   Type `string`, default `"mysqlddl-crypto-material"`, Hopsworks overrides the `rondb` chart default `"ddl-mysqld-end-to-end-tls"`.
    Name of the TLS Secret

`rondb.rondb.meta.ddlMySQLd.statefulSet.endToEndTls.supplyOwnSecret` <a class="headerlink" href="#helm.rondb.rondb.meta.ddlMySQLd.statefulSet.endToEndTls.supplyOwnSecret" title="Permanent link">#</a> { #helm.rondb.rondb.meta.ddlMySQLd.statefulSet.endToEndTls.supplyOwnSecret }
:   Type `boolean`, default `true`, Hopsworks overrides the `rondb` chart default `false`.
    Whether the Helmchart user will create a TLS Secret outside of this Helmchart. Otherwise we rely on cert-manager to create one.

`rondb.rondb.meta.ddlMySQLd.statefulSet.name` <a class="headerlink" href="#helm.rondb.rondb.meta.ddlMySQLd.statefulSet.name" title="Permanent link">#</a> { #helm.rondb.rondb.meta.ddlMySQLd.statefulSet.name }
:   Type `string`, default `"ddl-mysqld"`.

`rondb.rondb.meta.mgmd` <a class="headerlink" href="#helm.rondb.rondb.meta.mgmd" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mgmd }
:   Type `object`.

`rondb.rondb.meta.mgmd.headlessClusterIp` <a class="headerlink" href="#helm.rondb.rondb.meta.mgmd.headlessClusterIp" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mgmd.headlessClusterIp }
:   Type `object`.

`rondb.rondb.meta.mgmd.headlessClusterIp.annotations` <a class="headerlink" href="#helm.rondb.rondb.meta.mgmd.headlessClusterIp.annotations" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mgmd.headlessClusterIp.annotations }
:   Type `object`, default `{"consul.hashicorp.com/service-name":"mgmd"}`, Hopsworks overrides the `rondb` chart default `{}`.

`rondb.rondb.meta.mgmd.headlessClusterIp.name` <a class="headerlink" href="#helm.rondb.rondb.meta.mgmd.headlessClusterIp.name" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mgmd.headlessClusterIp.name }
:   Type `string`, default `"headless-mgmds"`.

`rondb.rondb.meta.mgmd.headlessClusterIp.port` <a class="headerlink" href="#helm.rondb.rondb.meta.mgmd.headlessClusterIp.port" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mgmd.headlessClusterIp.port }
:   Type `integer`, default `1186`.

`rondb.rondb.meta.mgmd.statefulSetName` <a class="headerlink" href="#helm.rondb.rondb.meta.mgmd.statefulSetName" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mgmd.statefulSetName }
:   Type `string`, default `"mgmds"`.

`rondb.rondb.meta.mysqld` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld }
:   Type `object`.

`rondb.rondb.meta.mysqld.addSysNiceCapability` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.addSysNiceCapability" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.addSysNiceCapability }
:   Type `boolean`, default `true`.

`rondb.rondb.meta.mysqld.clusterIp` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.clusterIp" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.clusterIp }
:   Type `object`.

`rondb.rondb.meta.mysqld.clusterIp.annotations` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.clusterIp.annotations" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.clusterIp.annotations }
:   Type `object`, Hopsworks overrides the `rondb` chart default `{}`.

    ??? note "Default"

        ```yaml
        consul.hashicorp.com/service-name: mysql
        consul.hashicorp.com/service-tags: onlinefs
        ```

`rondb.rondb.meta.mysqld.clusterIp.name` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.clusterIp.name" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.clusterIp.name }
:   Type `string`, default `"mysqld"`.

`rondb.rondb.meta.mysqld.clusterIp.port` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.clusterIp.port" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.clusterIp.port }
:   Type `integer`, default `3306`.

`rondb.rondb.meta.mysqld.exporter` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.exporter" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.exporter }
:   Type `object`.
    Configuration for mysqld exporter

`rondb.rondb.meta.mysqld.exporter.metricsPort` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.exporter.metricsPort" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.exporter.metricsPort }
:   Type `integer`, default `9104`.

`rondb.rondb.meta.mysqld.externalLoadBalancer` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.externalLoadBalancer" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.externalLoadBalancer }
:   Type `object`.
    Configuration for load balancer service to be used for external access

`rondb.rondb.meta.mysqld.externalLoadBalancer.annotations` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.externalLoadBalancer.annotations" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.externalLoadBalancer.annotations }
:   Type `object`, default `{}`.
    Cloud provider load balancer specific annotations.

`rondb.rondb.meta.mysqld.externalLoadBalancer.class` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.externalLoadBalancer.class" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.externalLoadBalancer.class }
:   Type `string|null`, default `null`.

`rondb.rondb.meta.mysqld.externalLoadBalancer.enabled` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.externalLoadBalancer.enabled" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.externalLoadBalancer.enabled }
:   Type `boolean`, default `true`, Hopsworks overrides the `rondb` chart default `false`.

`rondb.rondb.meta.mysqld.externalLoadBalancer.managed` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.externalLoadBalancer.managed" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.externalLoadBalancer.managed }
:   Type `boolean`, default `true`.
    LoadBalancer is managed by provider

`rondb.rondb.meta.mysqld.externalLoadBalancer.name` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.externalLoadBalancer.name" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.externalLoadBalancer.name }
:   Type `string`, default `"mysqld-external"`.

`rondb.rondb.meta.mysqld.externalLoadBalancer.nodePort` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.externalLoadBalancer.nodePort" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.externalLoadBalancer.nodePort }
:   Type `integer|null`, default `null`, minimum `1`, maximum `65535`.
    Explicit nodePort for the service when the load balancer is unmanaged (managed: false), so a load balancer outside Kubernetes can target a fixed port. Null lets Kubernetes allocate one from the cluster's node-port range.

`rondb.rondb.meta.mysqld.externalLoadBalancer.nodeSelector` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.externalLoadBalancer.nodeSelector" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.externalLoadBalancer.nodeSelector }
:   Type `object`, default `{}`.
    selector for nodes the load balancer can use to route traffic

`rondb.rondb.meta.mysqld.externalLoadBalancer.port` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.externalLoadBalancer.port" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.externalLoadBalancer.port }
:   Type `integer`, default `3306`.
    Port to expose the service on

`rondb.rondb.meta.mysqld.headlessClusterIp` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.headlessClusterIp" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.headlessClusterIp }
:   Type `object`.

`rondb.rondb.meta.mysqld.headlessClusterIp.name` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.headlessClusterIp.name" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.headlessClusterIp.name }
:   Type `string`, default `"headless-mysqlds"`.

`rondb.rondb.meta.mysqld.headlessClusterIp.port` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.headlessClusterIp.port" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.headlessClusterIp.port }
:   Type `integer`, default `3306`.

`rondb.rondb.meta.mysqld.statefulSet` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.statefulSet" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.statefulSet }
:   Type `object`.

`rondb.rondb.meta.mysqld.statefulSet.endToEndTls` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.statefulSet.endToEndTls" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.statefulSet.endToEndTls }
:   Type `object`.

`rondb.rondb.meta.mysqld.statefulSet.endToEndTls.enabled` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.statefulSet.endToEndTls.enabled" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.statefulSet.endToEndTls.enabled }
:   default `false`.
    Whether to use end-to-end encryption for MySQLd Pods. This is recommended for high-security use cases. For MySQLds this is especially recommended since they use raw TCP connections and thereby by-pass TLS Ingress-rules. Otherwise, Ingress-TCP can also be configured directly via the Ingress controller (not in this Helmchart).

`rondb.rondb.meta.mysqld.statefulSet.endToEndTls.filenames` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.statefulSet.endToEndTls.filenames" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.statefulSet.endToEndTls.filenames }
:   Type `object`.

`rondb.rondb.meta.mysqld.statefulSet.endToEndTls.filenames.ca` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.statefulSet.endToEndTls.filenames.ca" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.statefulSet.endToEndTls.filenames.ca }
:   Type `string|null`, default `"hops_root_ca.pem"`, Hopsworks overrides the `rondb` chart default `null`.
    Name of the CA file in the Secret. ONLY overwrite this if you're not using standard TLS Secrets.

`rondb.rondb.meta.mysqld.statefulSet.endToEndTls.filenames.cert` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.statefulSet.endToEndTls.filenames.cert" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.statefulSet.endToEndTls.filenames.cert }
:   Type `string`, default `"mysql_certificate_bundle.pem"`, Hopsworks overrides the `rondb` chart default `"tls.crt"`.
    Name of the certificate file in the Secret. ONLY overwrite this if you're not using standard TLS Secrets.

`rondb.rondb.meta.mysqld.statefulSet.endToEndTls.filenames.key` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.statefulSet.endToEndTls.filenames.key" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.statefulSet.endToEndTls.filenames.key }
:   Type `string`, default `"mysql_priv.pem"`, Hopsworks overrides the `rondb` chart default `"tls.key"`.
    Name of the key file in the Secret. ONLY overwrite this if you're not using standard TLS Secrets.

`rondb.rondb.meta.mysqld.statefulSet.endToEndTls.secretName` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.statefulSet.endToEndTls.secretName" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.statefulSet.endToEndTls.secretName }
:   Type `string`, default `"mysqld-crypto-material"`, Hopsworks overrides the `rondb` chart default `"mysqld-end-to-end-tls"`.
    Name of the TLS Secret

`rondb.rondb.meta.mysqld.statefulSet.endToEndTls.supplyOwnSecret` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.statefulSet.endToEndTls.supplyOwnSecret" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.statefulSet.endToEndTls.supplyOwnSecret }
:   default `true`, Hopsworks overrides the `rondb` chart default `false`.
    Whether the Helmchart user will create a TLS Secret outside of this Helmchart. Otherwise we rely on cert-manager to create one.

`rondb.rondb.meta.mysqld.statefulSet.name` <a class="headerlink" href="#helm.rondb.rondb.meta.mysqld.statefulSet.name" title="Permanent link">#</a> { #helm.rondb.rondb.meta.mysqld.statefulSet.name }
:   Type `string`, default `"mysqlds"`.

`rondb.rondb.meta.ndbmtd` <a class="headerlink" href="#helm.rondb.rondb.meta.ndbmtd" title="Permanent link">#</a> { #helm.rondb.rondb.meta.ndbmtd }
:   Type `object`.

`rondb.rondb.meta.ndbmtd.statefulSet` <a class="headerlink" href="#helm.rondb.rondb.meta.ndbmtd.statefulSet" title="Permanent link">#</a> { #helm.rondb.rondb.meta.ndbmtd.statefulSet }
:   Type `object`.

`rondb.rondb.meta.ndbmtd.statefulSet.podAnnotations` <a class="headerlink" href="#helm.rondb.rondb.meta.ndbmtd.statefulSet.podAnnotations" title="Permanent link">#</a> { #helm.rondb.rondb.meta.ndbmtd.statefulSet.podAnnotations }
:   Type `object`, default `{}`.

`rondb.rondb.meta.rdrs` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs }
:   Type `object`.

`rondb.rondb.meta.rdrs.clusterIp` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.clusterIp" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.clusterIp }
:   Type `object`.

`rondb.rondb.meta.rdrs.clusterIp.annotations` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.clusterIp.annotations" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.clusterIp.annotations }
:   Type `object`.

    ??? note "Default"

        ```yaml
        consul.hashicorp.com/service-name: rdrs
        prometheus.io/path: /metrics
        prometheus.io/port: '4406'
        prometheus.io/scheme: https
        prometheus.io/scrape: 'true'
        ```

`rondb.rondb.meta.rdrs.clusterIp.name` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.clusterIp.name" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.clusterIp.name }
:   Type `string`, default `"rdrs"`.

`rondb.rondb.meta.rdrs.externalLoadBalancer` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.externalLoadBalancer" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.externalLoadBalancer }
:   Type `object`.
    Configuration for load balancer service to be used for external access

`rondb.rondb.meta.rdrs.externalLoadBalancer.annotations` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.externalLoadBalancer.annotations" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.externalLoadBalancer.annotations }
:   Type `object`, default `{}`.
    Cloud provider load balancer specific annotations.

`rondb.rondb.meta.rdrs.externalLoadBalancer.class` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.externalLoadBalancer.class" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.externalLoadBalancer.class }
:   Type `string|null`, default `null`.

`rondb.rondb.meta.rdrs.externalLoadBalancer.enabled` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.externalLoadBalancer.enabled" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.externalLoadBalancer.enabled }
:   Type `boolean`, default `true`, Hopsworks overrides the `rondb` chart default `false`.

`rondb.rondb.meta.rdrs.externalLoadBalancer.managed` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.externalLoadBalancer.managed" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.externalLoadBalancer.managed }
:   Type `boolean`, default `true`.
    LoadBalancer is managed by provider

`rondb.rondb.meta.rdrs.externalLoadBalancer.name` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.externalLoadBalancer.name" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.externalLoadBalancer.name }
:   Type `string`, default `"rdrs-external"`.

`rondb.rondb.meta.rdrs.externalLoadBalancer.nodePort` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.externalLoadBalancer.nodePort" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.externalLoadBalancer.nodePort }
:   Type `integer|null`, default `null`, minimum `1`, maximum `65535`.
    Explicit nodePort for the service when the load balancer is unmanaged (managed: false), so a load balancer outside Kubernetes can target a fixed port. Null lets Kubernetes allocate one from the cluster's node-port range.

`rondb.rondb.meta.rdrs.externalLoadBalancer.nodeSelector` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.externalLoadBalancer.nodeSelector" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.externalLoadBalancer.nodeSelector }
:   Type `object`, default `{}`.
    selector for nodes the load balancer can use to route traffic

`rondb.rondb.meta.rdrs.headlessClusterIpName` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.headlessClusterIpName" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.headlessClusterIpName }
:   Type `string`, default `"rdrs-cluster-ip"`.

`rondb.rondb.meta.rdrs.ingress` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.ingress" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.ingress }
:   Type `object`.
    Configuration of Ingress for RDRS

`rondb.rondb.meta.rdrs.ingress.class` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.ingress.class" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.ingress.class }
:   Type `string`, default `"nginx"`.

`rondb.rondb.meta.rdrs.ingress.dnsNames` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.ingress.dnsNames" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.ingress.dnsNames }
:   Type `array`, default `[]`, example `"rondb.com"`.

`rondb.rondb.meta.rdrs.ingress.enabled` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.ingress.enabled" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.ingress.enabled }
:   Type `boolean`, default `false`.

`rondb.rondb.meta.rdrs.ingress.tls` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.ingress.tls" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.ingress.tls }
:   Type `object`.

`rondb.rondb.meta.rdrs.ingress.tls.enabled` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.ingress.tls.enabled" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.ingress.tls.enabled }
:   Type `boolean`, default `true`.
    WARN: Nginx-ingress will always use encryption even if this is disabled. By enabling this, we simply have more control over the TLS Secret. The TLS Secrets are placed onto the Ingress controller instance. Ingress TLS is currently only supported with cert-manager (RonDB-standalone)

`rondb.rondb.meta.rdrs.ingress.tls.ipAddresses` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.ingress.tls.ipAddresses" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.ingress.tls.ipAddresses }
:   Type `array`, default `[]`, example `"127.0.0.1"`.

`rondb.rondb.meta.rdrs.ingress.useDefaultBackend` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.ingress.useDefaultBackend" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.ingress.useDefaultBackend }
:   Type `boolean`, default `true`.
    Whether to use the RDRS as a default backend for the Ingress; this makes it reachable without specifying a subdomain; i.e. an IP can be used instead.

`rondb.rondb.meta.rdrs.statefulSet` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.statefulSet" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.statefulSet }
:   Type `object`.

`rondb.rondb.meta.rdrs.statefulSet.endToEndTls` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.statefulSet.endToEndTls" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.statefulSet.endToEndTls }
:   Type `object`.

`rondb.rondb.meta.rdrs.statefulSet.endToEndTls.enabled` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.statefulSet.endToEndTls.enabled" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.statefulSet.endToEndTls.enabled }
:   default `true`, Hopsworks overrides the `rondb` chart default `false`.
    Whether to use end-to-end encryption for RDRS Pods. This is recommended for high-security use cases.

`rondb.rondb.meta.rdrs.statefulSet.endToEndTls.filenames` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.statefulSet.endToEndTls.filenames" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.statefulSet.endToEndTls.filenames }
:   Type `object`.

`rondb.rondb.meta.rdrs.statefulSet.endToEndTls.filenames.ca` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.statefulSet.endToEndTls.filenames.ca" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.statefulSet.endToEndTls.filenames.ca }
:   Type `string|null`, default `"hops_root_ca.pem"`, Hopsworks overrides the `rondb` chart default `null`.
    Name of the CA file in the Secret. ONLY overwrite this if you're not using standard TLS Secrets.

`rondb.rondb.meta.rdrs.statefulSet.endToEndTls.filenames.cert` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.statefulSet.endToEndTls.filenames.cert" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.statefulSet.endToEndTls.filenames.cert }
:   Type `string`, default `"mysql_certificate_bundle.pem"`, Hopsworks overrides the `rondb` chart default `"tls.crt"`.
    Name of the certificate file in the Secret. ONLY overwrite this if you're not using standard TLS Secrets.

`rondb.rondb.meta.rdrs.statefulSet.endToEndTls.filenames.key` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.statefulSet.endToEndTls.filenames.key" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.statefulSet.endToEndTls.filenames.key }
:   Type `string`, default `"mysql_priv.pem"`, Hopsworks overrides the `rondb` chart default `"tls.key"`.
    Name of the key file in the Secret. ONLY overwrite this if you're not using standard TLS Secrets.

`rondb.rondb.meta.rdrs.statefulSet.endToEndTls.secretName` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.statefulSet.endToEndTls.secretName" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.statefulSet.endToEndTls.secretName }
:   Type `string`, default `"rdrs-crypto-material"`, Hopsworks overrides the `rondb` chart default `"rdrs-end-to-end-tls"`.
    Name of the TLS Secret

`rondb.rondb.meta.rdrs.statefulSet.endToEndTls.supplyOwnSecret` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.statefulSet.endToEndTls.supplyOwnSecret" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.statefulSet.endToEndTls.supplyOwnSecret }
:   default `true`, Hopsworks overrides the `rondb` chart default `false`.
    Whether the Helmchart user will create a TLS Secret outside of this Helmchart. Otherwise we rely on cert-manager to create one.

`rondb.rondb.meta.rdrs.statefulSet.name` <a class="headerlink" href="#helm.rondb.rondb.meta.rdrs.statefulSet.name" title="Permanent link">#</a> { #helm.rondb.rondb.meta.rdrs.statefulSet.name }
:   Type `string`, default `"rdrs"`.

`rondb.rondb.meta.replicaAppliers` <a class="headerlink" href="#helm.rondb.rondb.meta.replicaAppliers" title="Permanent link">#</a> { #helm.rondb.rondb.meta.replicaAppliers }
:   Type `object`.

`rondb.rondb.meta.replicaAppliers.headlessClusterIp` <a class="headerlink" href="#helm.rondb.rondb.meta.replicaAppliers.headlessClusterIp" title="Permanent link">#</a> { #helm.rondb.rondb.meta.replicaAppliers.headlessClusterIp }
:   Type `object`.

`rondb.rondb.meta.replicaAppliers.headlessClusterIp.name` <a class="headerlink" href="#helm.rondb.rondb.meta.replicaAppliers.headlessClusterIp.name" title="Permanent link">#</a> { #helm.rondb.rondb.meta.replicaAppliers.headlessClusterIp.name }
:   Type `string`, default `"headless-replica-appliers"`.

`rondb.rondb.meta.replicaAppliers.headlessClusterIp.port` <a class="headerlink" href="#helm.rondb.rondb.meta.replicaAppliers.headlessClusterIp.port" title="Permanent link">#</a> { #helm.rondb.rondb.meta.replicaAppliers.headlessClusterIp.port }
:   Type `integer`, default `3306`.

`rondb.rondb.meta.replicaAppliers.statefulSet` <a class="headerlink" href="#helm.rondb.rondb.meta.replicaAppliers.statefulSet" title="Permanent link">#</a> { #helm.rondb.rondb.meta.replicaAppliers.statefulSet }
:   Type `object`.

`rondb.rondb.meta.replicaAppliers.statefulSet.endToEndTls` <a class="headerlink" href="#helm.rondb.rondb.meta.replicaAppliers.statefulSet.endToEndTls" title="Permanent link">#</a> { #helm.rondb.rondb.meta.replicaAppliers.statefulSet.endToEndTls }
:   Type `object`.

`rondb.rondb.meta.replicaAppliers.statefulSet.endToEndTls.enabled` <a class="headerlink" href="#helm.rondb.rondb.meta.replicaAppliers.statefulSet.endToEndTls.enabled" title="Permanent link">#</a> { #helm.rondb.rondb.meta.replicaAppliers.statefulSet.endToEndTls.enabled }
:   default `false`.
    Whether to use end-to-end encryption for MySQL replica applier Pods. This is recommended for high-security use cases. For MySQLds this is especially recommended since they use raw TCP connections and thereby by-pass TLS Ingress-rules. Otherwise, Ingress-TCP can also be configured directly via the Ingress controller (not in this Helmchart).

`rondb.rondb.meta.replicaAppliers.statefulSet.endToEndTls.filenames` <a class="headerlink" href="#helm.rondb.rondb.meta.replicaAppliers.statefulSet.endToEndTls.filenames" title="Permanent link">#</a> { #helm.rondb.rondb.meta.replicaAppliers.statefulSet.endToEndTls.filenames }
:   Type `object`.

`rondb.rondb.meta.replicaAppliers.statefulSet.endToEndTls.filenames.ca` <a class="headerlink" href="#helm.rondb.rondb.meta.replicaAppliers.statefulSet.endToEndTls.filenames.ca" title="Permanent link">#</a> { #helm.rondb.rondb.meta.replicaAppliers.statefulSet.endToEndTls.filenames.ca }
:   Type `string|null`, default `null`.
    Name of the CA file in the Secret. ONLY overwrite this if you're not using standard TLS Secrets.

`rondb.rondb.meta.replicaAppliers.statefulSet.endToEndTls.filenames.cert` <a class="headerlink" href="#helm.rondb.rondb.meta.replicaAppliers.statefulSet.endToEndTls.filenames.cert" title="Permanent link">#</a> { #helm.rondb.rondb.meta.replicaAppliers.statefulSet.endToEndTls.filenames.cert }
:   Type `string`, default `"tls.crt"`.
    Name of the certificate file in the Secret. ONLY overwrite this if you're not using standard TLS Secrets.

`rondb.rondb.meta.replicaAppliers.statefulSet.endToEndTls.filenames.key` <a class="headerlink" href="#helm.rondb.rondb.meta.replicaAppliers.statefulSet.endToEndTls.filenames.key" title="Permanent link">#</a> { #helm.rondb.rondb.meta.replicaAppliers.statefulSet.endToEndTls.filenames.key }
:   Type `string`, default `"tls.key"`.
    Name of the key file in the Secret. ONLY overwrite this if you're not using standard TLS Secrets.

`rondb.rondb.meta.replicaAppliers.statefulSet.endToEndTls.secretName` <a class="headerlink" href="#helm.rondb.rondb.meta.replicaAppliers.statefulSet.endToEndTls.secretName" title="Permanent link">#</a> { #helm.rondb.rondb.meta.replicaAppliers.statefulSet.endToEndTls.secretName }
:   Type `string`, default `"replica-applier-end-to-end-tls"`.
    Name of the TLS Secret

`rondb.rondb.meta.replicaAppliers.statefulSet.endToEndTls.supplyOwnSecret` <a class="headerlink" href="#helm.rondb.rondb.meta.replicaAppliers.statefulSet.endToEndTls.supplyOwnSecret" title="Permanent link">#</a> { #helm.rondb.rondb.meta.replicaAppliers.statefulSet.endToEndTls.supplyOwnSecret }
:   default `false`.
    Whether the Helmchart user will create a TLS Secret outside of this Helmchart. Otherwise we rely on cert-manager to create one.

`rondb.rondb.meta.replicaAppliers.statefulSet.name` <a class="headerlink" href="#helm.rondb.rondb.meta.replicaAppliers.statefulSet.name" title="Permanent link">#</a> { #helm.rondb.rondb.meta.replicaAppliers.statefulSet.name }
:   Type `string`, default `"mysqld-replica-appliers"`.

</div>

### mysql { #helm-values-rondb-rondb-mysql }

??? example "Defaults as YAML"

    ```yaml
    rondb:
      rondb:
        mysql:
          clusterUser: bench
          config:
            maxConnectErrors: '9223372036854775807'
            maxConnections: 512
            maxPreparedStmtCount: 65530
          credentialsSecretName: mysql-users-secrets
          exporter:
            enabled: true
            maxOpenConnections: 1
            maxUserConnections: 3
            username: exporter
          force2410UserGrantMigration: false
          sqlInitContent: {}
          supplyOwnSecret: false
          users:
          - host: '%'
            privileges:
            - database: '*'
              privileges:
              - ALL
              table: '*'
              withGrantOption: true
            username: hopsworksroot
    ```

<div class="hops-values" markdown>

`rondb.rondb.mysql` <a class="headerlink" href="#helm.rondb.rondb.mysql" title="Permanent link">#</a> { #helm.rondb.rondb.mysql }
:   Type `object`.
    How to initialize MySQL

`rondb.rondb.mysql.clusterUser` <a class="headerlink" href="#helm.rondb.rondb.mysql.clusterUser" title="Permanent link">#</a> { #helm.rondb.rondb.mysql.clusterUser }
:   Type `string`, default `"bench"`, Hopsworks overrides the `rondb` chart default `"helm"`.
    The MySQL user for K8s probes, benchmarks and for the standard my.cnf file.

`rondb.rondb.mysql.config` <a class="headerlink" href="#helm.rondb.rondb.mysql.config" title="Permanent link">#</a> { #helm.rondb.rondb.mysql.config }
:   Type `object`.
    MySQL configuration options

`rondb.rondb.mysql.config.maxConnectErrors` <a class="headerlink" href="#helm.rondb.rondb.mysql.config.maxConnectErrors" title="Permanent link">#</a> { #helm.rondb.rondb.mysql.config.maxConnectErrors }
:   Type `string`, default `"9223372036854775807"`.
    Maximum number of connection errors before the MySQL server blocks the host.

`rondb.rondb.mysql.config.maxConnections` <a class="headerlink" href="#helm.rondb.rondb.mysql.config.maxConnections" title="Permanent link">#</a> { #helm.rondb.rondb.mysql.config.maxConnections }
:   Type `integer`, default `512`.
    Maximum number of connections to the MySQL server.

`rondb.rondb.mysql.config.maxPreparedStmtCount` <a class="headerlink" href="#helm.rondb.rondb.mysql.config.maxPreparedStmtCount" title="Permanent link">#</a> { #helm.rondb.rondb.mysql.config.maxPreparedStmtCount }
:   Type `integer`, default `65530`.
    Maximum number of prepared statements.

`rondb.rondb.mysql.credentialsSecretName` <a class="headerlink" href="#helm.rondb.rondb.mysql.credentialsSecretName" title="Permanent link">#</a> { #helm.rondb.rondb.mysql.credentialsSecretName }
:   Type `string`, default `"mysql-users-secrets"`, Hopsworks overrides the `rondb` chart default `"mysql-passwords"`.
    Secret name for MySQL users' passwords

`rondb.rondb.mysql.exporter` <a class="headerlink" href="#helm.rondb.rondb.mysql.exporter" title="Permanent link">#</a> { #helm.rondb.rondb.mysql.exporter }
:   Type `object`.
    MySQL exporter configuration

`rondb.rondb.mysql.exporter.enabled` <a class="headerlink" href="#helm.rondb.rondb.mysql.exporter.enabled" title="Permanent link">#</a> { #helm.rondb.rondb.mysql.exporter.enabled }
:   Type `boolean`, default `true`, Hopsworks overrides the `rondb` chart default `false`.

`rondb.rondb.mysql.exporter.maxOpenConnections` <a class="headerlink" href="#helm.rondb.rondb.mysql.exporter.maxOpenConnections" title="Permanent link">#</a> { #helm.rondb.rondb.mysql.exporter.maxOpenConnections }
:   Type `integer`, default `1`, minimum `1`.
    Maximum number of open connections to the database per scrape. 1 (default) serializes all collectors onto a single connection; higher values let independent collectors run concurrently but may incur higher load on the database. Should not exceed maxUserConnections.

`rondb.rondb.mysql.exporter.maxUserConnections` <a class="headerlink" href="#helm.rondb.rondb.mysql.exporter.maxUserConnections" title="Permanent link">#</a> { #helm.rondb.rondb.mysql.exporter.maxUserConnections }
:   Type `integer`, default `3`.

`rondb.rondb.mysql.exporter.username` <a class="headerlink" href="#helm.rondb.rondb.mysql.exporter.username" title="Permanent link">#</a> { #helm.rondb.rondb.mysql.exporter.username }
:   Type `string`, default `"exporter"`.

`rondb.rondb.mysql.force2410UserGrantMigration` <a class="headerlink" href="#helm.rondb.rondb.mysql.force2410UserGrantMigration" title="Permanent link">#</a> { #helm.rondb.rondb.mysql.force2410UserGrantMigration }
:   Type `boolean`, default `false`.
    Whether to force the execution of the 24.10 user privilege migration job that revokes the SET_USER_ID privilege from users that should not have it. This is useful when the automatic detection fails.

`rondb.rondb.mysql.sqlInitContent` <a class="headerlink" href="#helm.rondb.rondb.mysql.sqlInitContent" title="Permanent link">#</a> { #helm.rondb.rondb.mysql.sqlInitContent }
:   Type `object`, default `{}`, example `{"createMyUser":"CREATE USER foo IF NOT EXISTS;"}`.
    SQL to run *only once* at cluster startup. Try to make these scripts idempotent, in case they are re-run by accident. Do so by e.g. using `IF NOT EXISTS` in the SQL commands.

`rondb.rondb.mysql.supplyOwnSecret` <a class="headerlink" href="#helm.rondb.rondb.mysql.supplyOwnSecret" title="Permanent link">#</a> { #helm.rondb.rondb.mysql.supplyOwnSecret }
:   Type `boolean`, default `false`.
    If set to false, the Helmchart will auto-generate MySQL passwords. When running Global Replication as a secondary cluster, this should be set to true. Otherwise, the replication of ALTER root password will fail the cluster.

`rondb.rondb.mysql.users` <a class="headerlink" href="#helm.rondb.rondb.mysql.users" title="Permanent link">#</a> { #helm.rondb.rondb.mysql.users }
:   Type `array`, Hopsworks overrides the `rondb` chart default `[]`.
    A list of MySQL users and their privileges.

    ??? note "Default"

        ```yaml
        - username: hopsworksroot
          host: '%'
          privileges:
          - database: '*'
            table: '*'
            withGrantOption: true
            privileges:
            - ALL
        ```

`rondb.rondb.mysql.users[].existingSecret` <a class="headerlink" href="#helm.rondb.rondb.mysql.users.existingSecret" title="Permanent link">#</a> { #helm.rondb.rondb.mysql.users.existingSecret }
:   Type `object`.
    Reference to a pre-created Kubernetes Secret holding this user's password. When set, the Helmchart does not generate or store a password for this user in mysql.credentialsSecretName; the referenced Secret must exist in the release namespace before install/upgrade.

`rondb.rondb.mysql.users[].existingSecret.key` <a class="headerlink" href="#helm.rondb.rondb.mysql.users.existingSecret.key" title="Permanent link">#</a> { #helm.rondb.rondb.mysql.users.existingSecret.key }
:   Type `string`.
    Key within the Secret whose value is the user's password.

`rondb.rondb.mysql.users[].existingSecret.name` <a class="headerlink" href="#helm.rondb.rondb.mysql.users.existingSecret.name" title="Permanent link">#</a> { #helm.rondb.rondb.mysql.users.existingSecret.name }
:   Type `string`.
    Name of the Kubernetes Secret containing the user's password.

`rondb.rondb.mysql.users[].existingSecret.rotationId` <a class="headerlink" href="#helm.rondb.rondb.mysql.users.existingSecret.rotationId" title="Permanent link">#</a> { #helm.rondb.rondb.mysql.users.existingSecret.rotationId }
:   Type `string`.
    Opaque rotation marker. Bump this (e.g. to a date or counter) whenever the Secret's password is rotated. It participates in the user-setup Job's name, forcing a re-run that converges the MySQL password to the Secret (ALTER USER). Required for rotation under Argo CD / template-only rendering, where the release revision is constant; plain `helm upgrade` re-runs the Job on every upgrade regardless.

`rondb.rondb.mysql.users[].host` <a class="headerlink" href="#helm.rondb.rondb.mysql.users.host" title="Permanent link">#</a> { #helm.rondb.rondb.mysql.users.host }
:   Type `string`, example `"%"`.
    The host from which the MySQL user can connect.

`rondb.rondb.mysql.users[].privileges` <a class="headerlink" href="#helm.rondb.rondb.mysql.users.privileges" title="Permanent link">#</a> { #helm.rondb.rondb.mysql.users.privileges }
:   Type `array`.
    Privileges assigned to the MySQL user.

`rondb.rondb.mysql.users[].privileges[].database` <a class="headerlink" href="#helm.rondb.rondb.mysql.users.privileges.database" title="Permanent link">#</a> { #helm.rondb.rondb.mysql.users.privileges.database }
:   Type `string`, example `"*"`.
    The MySQL database to which the privileges apply.

`rondb.rondb.mysql.users[].privileges[].privileges` <a class="headerlink" href="#helm.rondb.rondb.mysql.users.privileges.privileges" title="Permanent link">#</a> { #helm.rondb.rondb.mysql.users.privileges.privileges }
:   Type `array`.

`rondb.rondb.mysql.users[].privileges[].table` <a class="headerlink" href="#helm.rondb.rondb.mysql.users.privileges.table" title="Permanent link">#</a> { #helm.rondb.rondb.mysql.users.privileges.table }
:   Type `string`, example `"*"`.
    The MySQL table to which the privileges apply.

`rondb.rondb.mysql.users[].privileges[].withGrantOption` <a class="headerlink" href="#helm.rondb.rondb.mysql.users.privileges.withGrantOption" title="Permanent link">#</a> { #helm.rondb.rondb.mysql.users.privileges.withGrantOption }
:   Type `boolean`, default `false`.
    Whether the user has the GRANT OPTION privilege.

`rondb.rondb.mysql.users[].username` <a class="headerlink" href="#helm.rondb.rondb.mysql.users.username" title="Permanent link">#</a> { #helm.rondb.rondb.mysql.users.username }
:   Type `string`.
    The username of the MySQL database user.

</div>

### ndbmtdSequencedRollout { #helm-values-rondb-rondb-ndbmtdsequencedrollout }

??? example "Defaults as YAML"

    ```yaml
    rondb:
      rondb:
        ndbmtdSequencedRollout:
          enabled: false
          perGroupStallTimeoutMinutes: 0
          reconcileIntervalMinutes: 3
          suspendWhenIdle: true
    ```

<div class="hops-values" markdown>

`rondb.rondb.ndbmtdSequencedRollout` <a class="headerlink" href="#helm.rondb.rondb.ndbmtdSequencedRollout" title="Permanent link">#</a> { #helm.rondb.rondb.ndbmtdSequencedRollout }
:   Type `object`.
    Sequenced (one node group at a time) data node rollouts during upgrades. When enabled, the node-group StatefulSets render updateStrategy.rollingUpdate.partition equal to their replica count, so 'helm upgrade' lands new pod templates without restarting anything; a rollout CronJob then unfreezes one node group at a time, waiting for each to converge (all pods on the new revision and ready) before the next. This bounds upgrade exposure to a single node group and stops a bad rollout at the first group. Only takes effect with more than one node group (clusterSize.numNodeGroups > 1): with a single group there is nothing to sequence across and the chart behaves exactly as if disabled. Not applied during in-place restores or on externally managed clusters. Argo CD users with selfHeal enabled must add ignoreDifferences for .spec.updateStrategy.rollingUpdate.partition on node-group-* StatefulSets.

`rondb.rondb.ndbmtdSequencedRollout.enabled` <a class="headerlink" href="#helm.rondb.rondb.ndbmtdSequencedRollout.enabled" title="Permanent link">#</a> { #helm.rondb.rondb.ndbmtdSequencedRollout.enabled }
:   Type `boolean`, default `false`.
    Enable the partition freeze and the rollout CronJob (they always render together). With this on, a successful 'helm upgrade' means the new specs are recorded and the rollout is in progress; completion is observable on the StatefulSets (updateRevision == currentRevision on every node group) rather than in the release status. Disabling the flag removes the partition field, so any still-pending update then rolls all node groups concurrently (the pre-feature behavior) - disable during a quiet period or after confirming no update is pending.

`rondb.rondb.ndbmtdSequencedRollout.perGroupStallTimeoutMinutes` <a class="headerlink" href="#helm.rondb.rondb.ndbmtdSequencedRollout.perGroupStallTimeoutMinutes" title="Permanent link">#</a> { #helm.rondb.rondb.ndbmtdSequencedRollout.perGroupStallTimeoutMinutes }
:   Type `integer`, default `0`, minimum `0`.
    Minutes an unfrozen node group may stay unconverged before the rollout CronJob reports a stall (logged on every run) and pauses; no further groups are unfrozen while the stalled group keeps trying. Note the next 'helm upgrade' (e.g. a fixed image) re-freezes every group, the stalled one included (Helm restores the rendered partition over the live value); the CronJob then delivers the fix by unfreezing the broken group again on the next run, in preference to healthy ones, and the StatefulSet controller replaces its dead pod. This is an alerting threshold - nothing is killed when it fires. 0 derives it from activeDataReplicas x timeoutsMinutes.ndbmtdStartupProbe plus 30 minutes slack.

`rondb.rondb.ndbmtdSequencedRollout.reconcileIntervalMinutes` <a class="headerlink" href="#helm.rondb.rondb.ndbmtdSequencedRollout.reconcileIntervalMinutes" title="Permanent link">#</a> { #helm.rondb.rondb.ndbmtdSequencedRollout.reconcileIntervalMinutes }
:   Type `integer`, default `3`, minimum `1`, maximum `30`.
    How often the rollout CronJob runs, in minutes. Each run re-freezes converged node groups and unfreezes at most one pending group, so this adds at most one interval of latency per node-group boundary - noise against recovery times measured in hours.

`rondb.rondb.ndbmtdSequencedRollout.suspendWhenIdle` <a class="headerlink" href="#helm.rondb.rondb.ndbmtdSequencedRollout.suspendWhenIdle" title="Permanent link">#</a> { #helm.rondb.rondb.ndbmtdSequencedRollout.suspendWhenIdle }
:   Type `boolean`, default `true`.
    When a run finds every node group converged and frozen, the rollout CronJob suspends itself so nothing at all runs while idle. Any 'helm upgrade' or 'helm rollback' turns it back on: the chart renders suspend: false and Helm resets live fields to their rendered values. Only takes effect when 'mode' is unset or 'auto' (plain Helm or Flux); when 'mode' is set - the Argo CD convention - the CronJob stays always-on, because Argo's sync would either keep re-enabling it (saving nothing) or, with ignoreDifferences on the CronJob's .spec.suspend, never re-enable it. WARNING: while suspended, a node-group spec change applied outside Helm (plain kubectl) stays frozen until the next helm operation or a manual wake: kubectl patch cronjob rondb-ndbmtd-sequenced-rollout --type merge -p '{"spec":{"suspend":false}}'. Pair with a revision-age alert (kube_statefulset_status_update_revision != kube_statefulset_status_current_revision with an age threshold) as the safety net. Set false to keep the CronJob always running.

</div>

### ndbmtdSettleWait { #helm-values-rondb-rondb-ndbmtdsettlewait }

??? example "Defaults as YAML"

    ```yaml
    rondb:
      rondb:
        ndbmtdSettleWait:
          fallbackSeconds: 15
          maxWaitSeconds: 30
          probeTimeoutSeconds: 5
          quietSeconds: 8
    ```

<div class="hops-values" markdown>

`rondb.rondb.ndbmtdSettleWait` <a class="headerlink" href="#helm.rondb.rondb.ndbmtdSettleWait" title="Permanent link">#</a> { #helm.rondb.rondb.ndbmtdSettleWait }
:   Type `object`.
    Pre-start settle wait for data nodes, protecting rolling restarts. During a roll, Kubernetes deletes a node group's second pod only after observing the first replacement Ready; that observation spread (measured 2.6-10.4s and set by the kubelet/API-server publication cycle, which the chart cannot tune) can overlap the window in which an earlier replacement has connected to the cluster but not yet reached the phase-110 restart barrier, killing it with error 2308 ('Another node failed during system restart'). Before starting the kernel on a non-initial start, the entrypoint polls the MGMd once a second and proceeds only once no data node has departed the cluster for quietSeconds (nodes reconnecting do not reset the timer: only a departing peer endangers a climbing node, and during a round every replacement's reconnect would otherwise extend the wait to its cap), so the node begins its climb only after the deletion wave has passed. The wait is bounded by maxWaitSeconds and never blocks a start: an unreachable or hanging MGMd degrades to a fixed fallbackSeconds sleep. Skipped entirely on initial starts.

`rondb.rondb.ndbmtdSettleWait.fallbackSeconds` <a class="headerlink" href="#helm.rondb.rondb.ndbmtdSettleWait.fallbackSeconds" title="Permanent link">#</a> { #helm.rondb.rondb.ndbmtdSettleWait.fallbackSeconds }
:   Type `integer`, default `15`, minimum `0`.
    Fixed sleep used instead of the adaptive wait when the MGMd never answers: 3 consecutive failed probes (unreachable, hanging, or empty output) with no successful probe in this wait. A transient MGMd outage after a successful probe does not trigger the fallback - the wait keeps retrying under maxWaitSeconds, with failed probes resetting the quiet timer.

`rondb.rondb.ndbmtdSettleWait.maxWaitSeconds` <a class="headerlink" href="#helm.rondb.rondb.ndbmtdSettleWait.maxWaitSeconds" title="Permanent link">#</a> { #helm.rondb.rondb.ndbmtdSettleWait.maxWaitSeconds }
:   Type `integer`, default `30`, minimum `0`.
    Cap on the whole settle wait, including the final quietSeconds of quiet. 0 disables the settle wait entirely.

`rondb.rondb.ndbmtdSettleWait.probeTimeoutSeconds` <a class="headerlink" href="#helm.rondb.rondb.ndbmtdSettleWait.probeTimeoutSeconds" title="Permanent link">#</a> { #helm.rondb.rondb.ndbmtdSettleWait.probeTimeoutSeconds }
:   Type `integer`, default `5`, minimum `1`.
    Timeout for each ndb_mgm membership probe.

`rondb.rondb.ndbmtdSettleWait.quietSeconds` <a class="headerlink" href="#helm.rondb.rondb.ndbmtdSettleWait.quietSeconds" title="Permanent link">#</a> { #helm.rondb.rondb.ndbmtdSettleWait.quietSeconds }
:   Type `integer`, default `8`, minimum `1`.
    Seconds without any data-node departure before the node starts (arrivals are ignored). Must exceed the largest gap between consecutive pod deletions within a rollout round, or the wait provides no protection. The default of 8 is calibrated to ONE measured cluster (max 7.4s gap over 66 rolls at 10 node groups on MicroK8s); the gap is set by the control plane's readiness-observation latency, not by RonDB, so it MUST be re-derived on a different control plane, larger cluster, or slower hardware - measure the deletion-timestamp gaps within one rollout round and set this above the maximum.

</div>

### networkPolicy { #helm-values-rondb-rondb-networkpolicy }

??? example "Defaults as YAML"

    ```yaml
    rondb:
      rondb:
        networkPolicy:
          mgmds:
            enabled: true
            ingressSelectors:
            - podSelector:
                matchLabels:
                  access: mgmd-and-ndbmtd
          ndbmtds:
            enabled: true
            ingressSelectors:
            - podSelector:
                matchLabels:
                  access: mgmd-and-ndbmtd
    ```

<div class="hops-values" markdown>

`rondb.rondb.networkPolicy` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy }
:   Type `object`.

`rondb.rondb.networkPolicy.mgmds` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.mgmds" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.mgmds }
:   Type `object`.

`rondb.rondb.networkPolicy.mgmds.enabled` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.mgmds.enabled" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.mgmds.enabled }
:   Type `boolean`, default `true`.
    Whether to limit ingress for MGMd pods

`rondb.rondb.networkPolicy.mgmds.ingressSelectors` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.mgmds.ingressSelectors" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.mgmds.ingressSelectors }
:   Type `array`, default `[{"podSelector":{"matchLabels":{"access":"mgmd-and-ndbmtd"}}}]`, Hopsworks overrides the `rondb` chart default `[]`.

`rondb.rondb.networkPolicy.mgmds.ingressSelectors[].namespaceSelector` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.mgmds.ingressSelectors.namespaceSelector" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.mgmds.ingressSelectors.namespaceSelector }
:   Type `object`.

`rondb.rondb.networkPolicy.mgmds.ingressSelectors[].namespaceSelector.matchExpressions` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.mgmds.ingressSelectors.namespaceSelector.matchExpressions" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.mgmds.ingressSelectors.namespaceSelector.matchExpressions }
:   Type `array`, default `[]`.

`rondb.rondb.networkPolicy.mgmds.ingressSelectors[].namespaceSelector.matchExpressions[].key` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.mgmds.ingressSelectors.namespaceSelector.matchExpressions.key" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.mgmds.ingressSelectors.namespaceSelector.matchExpressions.key }
:   Type `string`.

`rondb.rondb.networkPolicy.mgmds.ingressSelectors[].namespaceSelector.matchExpressions[].operator` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.mgmds.ingressSelectors.namespaceSelector.matchExpressions.operator" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.mgmds.ingressSelectors.namespaceSelector.matchExpressions.operator }
:   Type `string`.

`rondb.rondb.networkPolicy.mgmds.ingressSelectors[].namespaceSelector.matchExpressions[].values` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.mgmds.ingressSelectors.namespaceSelector.matchExpressions.values" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.mgmds.ingressSelectors.namespaceSelector.matchExpressions.values }
:   Type `array`.

`rondb.rondb.networkPolicy.mgmds.ingressSelectors[].namespaceSelector.matchLabels` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.mgmds.ingressSelectors.namespaceSelector.matchLabels" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.mgmds.ingressSelectors.namespaceSelector.matchLabels }
:   Type `object`, default `{}`, example `{"app":"rondb"}`.

`rondb.rondb.networkPolicy.mgmds.ingressSelectors[].podSelector` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.mgmds.ingressSelectors.podSelector" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.mgmds.ingressSelectors.podSelector }
:   Type `object`.

`rondb.rondb.networkPolicy.mgmds.ingressSelectors[].podSelector.matchExpressions` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.mgmds.ingressSelectors.podSelector.matchExpressions" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.mgmds.ingressSelectors.podSelector.matchExpressions }
:   Type `array`, default `[]`.

`rondb.rondb.networkPolicy.mgmds.ingressSelectors[].podSelector.matchExpressions[].key` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.mgmds.ingressSelectors.podSelector.matchExpressions.key" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.mgmds.ingressSelectors.podSelector.matchExpressions.key }
:   Type `string`.

`rondb.rondb.networkPolicy.mgmds.ingressSelectors[].podSelector.matchExpressions[].operator` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.mgmds.ingressSelectors.podSelector.matchExpressions.operator" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.mgmds.ingressSelectors.podSelector.matchExpressions.operator }
:   Type `string`.

`rondb.rondb.networkPolicy.mgmds.ingressSelectors[].podSelector.matchExpressions[].values` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.mgmds.ingressSelectors.podSelector.matchExpressions.values" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.mgmds.ingressSelectors.podSelector.matchExpressions.values }
:   Type `array`.

`rondb.rondb.networkPolicy.mgmds.ingressSelectors[].podSelector.matchLabels` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.mgmds.ingressSelectors.podSelector.matchLabels" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.mgmds.ingressSelectors.podSelector.matchLabels }
:   Type `object`, default `{}`, example `{"app":"rondb"}`.

`rondb.rondb.networkPolicy.ndbmtds` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.ndbmtds" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.ndbmtds }
:   Type `object`.

`rondb.rondb.networkPolicy.ndbmtds.enabled` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.ndbmtds.enabled" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.ndbmtds.enabled }
:   Type `boolean`, default `true`.
    Whether to limit ingress for data node pods. If there is an empty API slot in the config.ini, any host can connect to them.

`rondb.rondb.networkPolicy.ndbmtds.ingressSelectors` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.ndbmtds.ingressSelectors" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.ndbmtds.ingressSelectors }
:   Type `array`, default `[{"podSelector":{"matchLabels":{"access":"mgmd-and-ndbmtd"}}}]`, Hopsworks overrides the `rondb` chart default `[]`.

`rondb.rondb.networkPolicy.ndbmtds.ingressSelectors[].namespaceSelector` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.ndbmtds.ingressSelectors.namespaceSelector" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.ndbmtds.ingressSelectors.namespaceSelector }
:   Type `object`.

`rondb.rondb.networkPolicy.ndbmtds.ingressSelectors[].namespaceSelector.matchExpressions` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.ndbmtds.ingressSelectors.namespaceSelector.matchExpressions" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.ndbmtds.ingressSelectors.namespaceSelector.matchExpressions }
:   Type `array`, default `[]`.

`rondb.rondb.networkPolicy.ndbmtds.ingressSelectors[].namespaceSelector.matchExpressions[].key` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.ndbmtds.ingressSelectors.namespaceSelector.matchExpressions.key" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.ndbmtds.ingressSelectors.namespaceSelector.matchExpressions.key }
:   Type `string`.

`rondb.rondb.networkPolicy.ndbmtds.ingressSelectors[].namespaceSelector.matchExpressions[].operator` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.ndbmtds.ingressSelectors.namespaceSelector.matchExpressions.operator" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.ndbmtds.ingressSelectors.namespaceSelector.matchExpressions.operator }
:   Type `string`.

`rondb.rondb.networkPolicy.ndbmtds.ingressSelectors[].namespaceSelector.matchExpressions[].values` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.ndbmtds.ingressSelectors.namespaceSelector.matchExpressions.values" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.ndbmtds.ingressSelectors.namespaceSelector.matchExpressions.values }
:   Type `array`.

`rondb.rondb.networkPolicy.ndbmtds.ingressSelectors[].namespaceSelector.matchLabels` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.ndbmtds.ingressSelectors.namespaceSelector.matchLabels" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.ndbmtds.ingressSelectors.namespaceSelector.matchLabels }
:   Type `object`, default `{}`, example `{"app":"rondb"}`.

`rondb.rondb.networkPolicy.ndbmtds.ingressSelectors[].podSelector` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.ndbmtds.ingressSelectors.podSelector" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.ndbmtds.ingressSelectors.podSelector }
:   Type `object`.

`rondb.rondb.networkPolicy.ndbmtds.ingressSelectors[].podSelector.matchExpressions` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.ndbmtds.ingressSelectors.podSelector.matchExpressions" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.ndbmtds.ingressSelectors.podSelector.matchExpressions }
:   Type `array`, default `[]`.

`rondb.rondb.networkPolicy.ndbmtds.ingressSelectors[].podSelector.matchExpressions[].key` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.ndbmtds.ingressSelectors.podSelector.matchExpressions.key" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.ndbmtds.ingressSelectors.podSelector.matchExpressions.key }
:   Type `string`.

`rondb.rondb.networkPolicy.ndbmtds.ingressSelectors[].podSelector.matchExpressions[].operator` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.ndbmtds.ingressSelectors.podSelector.matchExpressions.operator" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.ndbmtds.ingressSelectors.podSelector.matchExpressions.operator }
:   Type `string`.

`rondb.rondb.networkPolicy.ndbmtds.ingressSelectors[].podSelector.matchExpressions[].values` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.ndbmtds.ingressSelectors.podSelector.matchExpressions.values" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.ndbmtds.ingressSelectors.podSelector.matchExpressions.values }
:   Type `array`.

`rondb.rondb.networkPolicy.ndbmtds.ingressSelectors[].podSelector.matchLabels` <a class="headerlink" href="#helm.rondb.rondb.networkPolicy.ndbmtds.ingressSelectors.podSelector.matchLabels" title="Permanent link">#</a> { #helm.rondb.rondb.networkPolicy.ndbmtds.ingressSelectors.podSelector.matchLabels }
:   Type `object`, default `{}`, example `{"app":"rondb"}`.

</div>

### nodeSelector { #helm-values-rondb-rondb-nodeselector }

??? example "Defaults as YAML"

    ```yaml
    rondb:
      rondb:
        nodeSelector:
          backup: {}
          mgmd: {}
          mysqld: {}
          ndbmtd: {}
          rdrs: {}
    ```

<div class="hops-values" markdown>

`rondb.rondb.nodeSelector` <a class="headerlink" href="#helm.rondb.rondb.nodeSelector" title="Permanent link">#</a> { #helm.rondb.rondb.nodeSelector }
:   Type `object`.
    This ensures that Kubernetes schedules pods only onto nodes that match all the specified labels.

`rondb.rondb.nodeSelector.backup` <a class="headerlink" href="#helm.rondb.rondb.nodeSelector.backup" title="Permanent link">#</a> { #helm.rondb.rondb.nodeSelector.backup }
:   Type `object`, default `{}`.

`rondb.rondb.nodeSelector.mgmd` <a class="headerlink" href="#helm.rondb.rondb.nodeSelector.mgmd" title="Permanent link">#</a> { #helm.rondb.rondb.nodeSelector.mgmd }
:   Type `object`, default `{}`.

`rondb.rondb.nodeSelector.mysqld` <a class="headerlink" href="#helm.rondb.rondb.nodeSelector.mysqld" title="Permanent link">#</a> { #helm.rondb.rondb.nodeSelector.mysqld }
:   Type `object`, default `{}`.

`rondb.rondb.nodeSelector.ndbmtd` <a class="headerlink" href="#helm.rondb.rondb.nodeSelector.ndbmtd" title="Permanent link">#</a> { #helm.rondb.rondb.nodeSelector.ndbmtd }
:   Type `object`, default `{}`.

`rondb.rondb.nodeSelector.rdrs` <a class="headerlink" href="#helm.rondb.rondb.nodeSelector.rdrs" title="Permanent link">#</a> { #helm.rondb.rondb.nodeSelector.rdrs }
:   Type `object`, default `{}`.

</div>

### podDisruptionBudget { #helm-values-rondb-rondb-poddisruptionbudget }

??? example "Defaults as YAML"

    ```yaml
    rondb:
      rondb:
        podDisruptionBudget:
          mysqld:
            enabled: true
            minAvailable: 1
          ndbmtd:
            enabled: true
            minAvailable: 1
          rdrs:
            enabled: true
            minAvailable: 1
    ```

<div class="hops-values" markdown>

`rondb.rondb.podDisruptionBudget` <a class="headerlink" href="#helm.rondb.rondb.podDisruptionBudget" title="Permanent link">#</a> { #helm.rondb.rondb.podDisruptionBudget }
:   Type `object`.
    PodDisruptionBudget configuration per service. Ensures pod availability during voluntary disruptions like node drains and EKS node group upgrades. For single-replica deployments (effective replicas == 1), the PDB is not created even if minAvailable is 1, to avoid blocking node drains. For multi-replica deployments (effective replicas > 1), template rendering will fail if minAvailable is greater than or equal to the effective replica count, because such a PDB would prevent voluntary disruptions. The effective replica count used in these checks is the configured minimum replica count for each service (for example, clusterSize.minNumMySQLServers / clusterSize.minNumRdrs), not any dynamically autoscaled replica count at runtime.

`rondb.rondb.podDisruptionBudget.mysqld` <a class="headerlink" href="#helm.rondb.rondb.podDisruptionBudget.mysqld" title="Permanent link">#</a> { #helm.rondb.rondb.podDisruptionBudget.mysqld }
:   Type `object`.

`rondb.rondb.podDisruptionBudget.mysqld.enabled` <a class="headerlink" href="#helm.rondb.rondb.podDisruptionBudget.mysqld.enabled" title="Permanent link">#</a> { #helm.rondb.rondb.podDisruptionBudget.mysqld.enabled }
:   Type `boolean`, default `true`.

`rondb.rondb.podDisruptionBudget.mysqld.minAvailable` <a class="headerlink" href="#helm.rondb.rondb.podDisruptionBudget.mysqld.minAvailable" title="Permanent link">#</a> { #helm.rondb.rondb.podDisruptionBudget.mysqld.minAvailable }
:   Type `integer`, default `1`, minimum `1`.

`rondb.rondb.podDisruptionBudget.ndbmtd` <a class="headerlink" href="#helm.rondb.rondb.podDisruptionBudget.ndbmtd" title="Permanent link">#</a> { #helm.rondb.rondb.podDisruptionBudget.ndbmtd }
:   Type `object`.

`rondb.rondb.podDisruptionBudget.ndbmtd.enabled` <a class="headerlink" href="#helm.rondb.rondb.podDisruptionBudget.ndbmtd.enabled" title="Permanent link">#</a> { #helm.rondb.rondb.podDisruptionBudget.ndbmtd.enabled }
:   Type `boolean`, default `true`.

`rondb.rondb.podDisruptionBudget.ndbmtd.minAvailable` <a class="headerlink" href="#helm.rondb.rondb.podDisruptionBudget.ndbmtd.minAvailable" title="Permanent link">#</a> { #helm.rondb.rondb.podDisruptionBudget.ndbmtd.minAvailable }
:   Type `integer`, default `1`, minimum `1`.

`rondb.rondb.podDisruptionBudget.rdrs` <a class="headerlink" href="#helm.rondb.rondb.podDisruptionBudget.rdrs" title="Permanent link">#</a> { #helm.rondb.rondb.podDisruptionBudget.rdrs }
:   Type `object`.

`rondb.rondb.podDisruptionBudget.rdrs.enabled` <a class="headerlink" href="#helm.rondb.rondb.podDisruptionBudget.rdrs.enabled" title="Permanent link">#</a> { #helm.rondb.rondb.podDisruptionBudget.rdrs.enabled }
:   Type `boolean`, default `true`.

`rondb.rondb.podDisruptionBudget.rdrs.minAvailable` <a class="headerlink" href="#helm.rondb.rondb.podDisruptionBudget.rdrs.minAvailable" title="Permanent link">#</a> { #helm.rondb.rondb.podDisruptionBudget.rdrs.minAvailable }
:   Type `integer`, default `1`, minimum `1`.

</div>

### rdrs { #helm-values-rondb-rondb-rdrs }

??? example "Defaults as YAML"

    ```yaml
    rondb:
      rondb:
        rdrs:
          externalMetadataCluster:
            mgmds: []
            slotsPerNode: 1
          hpa:
            additionalMetrics: []
          maxKeepaliveRequests: 0
          probePort:
            enabled: true
            port: 4407
          probes:
            liveness:
              failureThreshold: 12
              initialDelaySeconds: 5
              periodSeconds: 10
              timeoutSeconds: 5
            readiness:
              failureThreshold: 3
              initialDelaySeconds: 5
              periodSeconds: 5
              timeoutSeconds: 3
            startup:
              failureThreshold: 11
              initialDelaySeconds: 5
              periodSeconds: 5
              timeoutSeconds: 2
          security:
            apiKey:
              cacheRefreshIntervalMS: 180000
          ttlPurge:
            activeWindow: null
            enable: null
          uploadPath: /tmp/rdrs-uploads
    ```

<div class="hops-values" markdown>

`rondb.rondb.rdrs` <a class="headerlink" href="#helm.rondb.rondb.rdrs" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs }
:   Type `object`.

`rondb.rondb.rdrs.externalMetadataCluster` <a class="headerlink" href="#helm.rondb.rondb.rdrs.externalMetadataCluster" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.externalMetadataCluster }
:   Type `object`.
    RDRSs will always be in the cluster of the data, not the metadata

`rondb.rondb.rdrs.externalMetadataCluster.mgmds` <a class="headerlink" href="#helm.rondb.rondb.rdrs.externalMetadataCluster.mgmds" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.externalMetadataCluster.mgmds }
:   Type `array`, default `[]`.

`rondb.rondb.rdrs.externalMetadataCluster.mgmds[].ip` <a class="headerlink" href="#helm.rondb.rondb.rdrs.externalMetadataCluster.mgmds.ip" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.externalMetadataCluster.mgmds.ip }
:   Type `string`.

`rondb.rondb.rdrs.externalMetadataCluster.mgmds[].port` <a class="headerlink" href="#helm.rondb.rondb.rdrs.externalMetadataCluster.mgmds.port" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.externalMetadataCluster.mgmds.port }
:   Type `integer`, default `1186`.

`rondb.rondb.rdrs.externalMetadataCluster.slotsPerNode` <a class="headerlink" href="#helm.rondb.rondb.rdrs.externalMetadataCluster.slotsPerNode" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.externalMetadataCluster.slotsPerNode }
:   Type `integer`, default `1`, minimum `1`, maximum `1`.

`rondb.rondb.rdrs.hpa` <a class="headerlink" href="#helm.rondb.rondb.rdrs.hpa" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.hpa }
:   Type `object`.
    Horizontal Pod Autoscaler for RDRS

`rondb.rondb.rdrs.hpa.additionalMetrics` <a class="headerlink" href="#helm.rondb.rondb.rdrs.hpa.additionalMetrics" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.hpa.additionalMetrics }
:   Type `array`, default `[]`.
    Additional metrics to use for the HPA. This is useful for custom metrics that are not supported by default.

`rondb.rondb.rdrs.maxKeepaliveRequests` <a class="headerlink" href="#helm.rondb.rondb.rdrs.maxKeepaliveRequests" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.maxKeepaliveRequests }
:   Type `integer`, default `0`, minimum `0`, maximum `4294967295`, example `1000`.
    Maximum number of requests served on one keep-alive connection to the RDRS main port; after it the connection is closed gracefully (Connection: close). 0 (the default) disables the limit. A Kubernetes Service balances per TCP connection, so long-lived connections keep the skew that builds up after a rolling restart; bounding their lifetime lets clients re-balance. Each reconnect costs a TCP+TLS handshake: use a high value (1000 recommended, not below 500) and only where post-restart skew is observed. Does not apply to the probe port. Requires an RDRS image with REST.MaxKeepaliveRequests support (releases 26.02.11 and newer on the 26.02 line); at 0 the key is not emitted, so older images keep working.

`rondb.rondb.rdrs.probePort` <a class="headerlink" href="#helm.rondb.rondb.rdrs.probePort" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.probePort }
:   Type `object`.
    Dedicated RDRS probe listener. It serves only the ping and health endpoints, from its own thread, so Kubernetes probes keep being answered while every worker thread is blocked on data-node operations (a stalled data node otherwise fails the liveness probe of all RDRS pods at once). The probe port performs NO authentication, regardless of the PingRequiresAuth/HealthRequiresAuth settings. It is not published as a port of any Service or Ingress, but like any pod port it is reachable via pod IPs and the headless Service's DNS records; where isolation is required, enforce it with a NetworkPolicy. Requires an RDRS image with REST.ProbePort support (releases 26.02.11 and newer on the 26.02 line): older images reject the unknown config keys at startup, so set enabled to false for pinned older images. Trade-off: the probe port answers as long as the process lives, so an RDRS whose worker threads are permanently wedged is not restarted by liveness.

`rondb.rondb.rdrs.probePort.enabled` <a class="headerlink" href="#helm.rondb.rondb.rdrs.probePort.enabled" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.probePort.enabled }
:   Type `boolean`, default `true`.
    Serve ping/health on the dedicated probe port and point the startup, liveness and readiness probes at it (ping answers 503 until the main port accepts connections, so startup semantics are unchanged). false emits no probe configuration keys and points all probes back at the main port: the escape hatch for pinned RDRS images that predate REST.ProbePort.

`rondb.rondb.rdrs.probePort.port` <a class="headerlink" href="#helm.rondb.rondb.rdrs.probePort.port" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.probePort.port }
:   Type `integer`, default `4407`, minimum `1`, maximum `65535`.
    TCP port of the dedicated probe listener. Must differ from the main REST port (4406).

`rondb.rondb.rdrs.probes` <a class="headerlink" href="#helm.rondb.rondb.rdrs.probes" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.probes }
:   Type `object`.
    Timings of the RDRS container probes; the HTTP path, port and scheme are set by the chart. When installed through the Hopsworks chart, the path is rondb.rondb.rdrs.probes. A probe gives up after roughly (failureThreshold - 1) * periodSeconds + timeoutSeconds of consecutive failures.

`rondb.rondb.rdrs.probes.liveness` <a class="headerlink" href="#helm.rondb.rondb.rdrs.probes.liveness" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.probes.liveness }
:   Type `object`.
    Checks /ping and restarts RDRS when it keeps failing. With rdrs.probePort.enabled (the default) /ping is answered from the dedicated probe thread, which keeps responding through data-node failures, so the defaults are ample. With probePort.enabled=false /ping shares the worker threads: while a failed data node has not yet been declared dead, requests touching it block and /ping cannot answer. Detection takes ~25 seconds per data node, so in that mode size (failureThreshold - 1) * periodSeconds + timeoutSeconds above ~25 seconds per data node that can go silent at once, plus ~40 seconds. The defaults give ~115 seconds; restarting the data nodes of 8 node groups in parallel needs failureThreshold 30 (~295 seconds).

`rondb.rondb.rdrs.probes.liveness.failureThreshold` <a class="headerlink" href="#helm.rondb.rondb.rdrs.probes.liveness.failureThreshold" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.probes.liveness.failureThreshold }
:   Type `integer`, default `12`, minimum `1`.

`rondb.rondb.rdrs.probes.liveness.initialDelaySeconds` <a class="headerlink" href="#helm.rondb.rondb.rdrs.probes.liveness.initialDelaySeconds" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.probes.liveness.initialDelaySeconds }
:   Type `integer`, default `5`, minimum `0`.

`rondb.rondb.rdrs.probes.liveness.periodSeconds` <a class="headerlink" href="#helm.rondb.rondb.rdrs.probes.liveness.periodSeconds" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.probes.liveness.periodSeconds }
:   Type `integer`, default `10`, minimum `1`.

`rondb.rondb.rdrs.probes.liveness.timeoutSeconds` <a class="headerlink" href="#helm.rondb.rondb.rdrs.probes.liveness.timeoutSeconds" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.probes.liveness.timeoutSeconds }
:   Type `integer`, default `5`, minimum `1`.

`rondb.rondb.rdrs.probes.readiness` <a class="headerlink" href="#helm.rondb.rondb.rdrs.probes.readiness" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.probes.readiness }
:   Type `object`.
    Checks /health. A pod that keeps failing is removed from the Service after ~13 to 18 seconds with the defaults; connections it already holds stay open. More than one failure is required so that a single slow check under load does not take the pod out of the Service.

`rondb.rondb.rdrs.probes.readiness.failureThreshold` <a class="headerlink" href="#helm.rondb.rondb.rdrs.probes.readiness.failureThreshold" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.probes.readiness.failureThreshold }
:   Type `integer`, default `3`, minimum `1`.

`rondb.rondb.rdrs.probes.readiness.initialDelaySeconds` <a class="headerlink" href="#helm.rondb.rondb.rdrs.probes.readiness.initialDelaySeconds" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.probes.readiness.initialDelaySeconds }
:   Type `integer`, default `5`, minimum `0`.

`rondb.rondb.rdrs.probes.readiness.periodSeconds` <a class="headerlink" href="#helm.rondb.rondb.rdrs.probes.readiness.periodSeconds" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.probes.readiness.periodSeconds }
:   Type `integer`, default `5`, minimum `1`.

`rondb.rondb.rdrs.probes.readiness.timeoutSeconds` <a class="headerlink" href="#helm.rondb.rondb.rdrs.probes.readiness.timeoutSeconds" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.probes.readiness.timeoutSeconds }
:   Type `integer`, default `3`, minimum `1`.

`rondb.rondb.rdrs.probes.startup` <a class="headerlink" href="#helm.rondb.rondb.rdrs.probes.startup" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.probes.startup }
:   Type `object`.
    Checks /ping until RDRS first answers; liveness and readiness only start after it passes. RDRS opens its port once it has preloaded its caches from RonDB, about 25 seconds with a few hundred feature views. Raise failureThreshold if that preload takes longer than the ~57 seconds allowed.

`rondb.rondb.rdrs.probes.startup.failureThreshold` <a class="headerlink" href="#helm.rondb.rondb.rdrs.probes.startup.failureThreshold" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.probes.startup.failureThreshold }
:   Type `integer`, default `11`, minimum `1`.

`rondb.rondb.rdrs.probes.startup.initialDelaySeconds` <a class="headerlink" href="#helm.rondb.rondb.rdrs.probes.startup.initialDelaySeconds" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.probes.startup.initialDelaySeconds }
:   Type `integer`, default `5`, minimum `0`.

`rondb.rondb.rdrs.probes.startup.periodSeconds` <a class="headerlink" href="#helm.rondb.rondb.rdrs.probes.startup.periodSeconds" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.probes.startup.periodSeconds }
:   Type `integer`, default `5`, minimum `1`.

`rondb.rondb.rdrs.probes.startup.timeoutSeconds` <a class="headerlink" href="#helm.rondb.rondb.rdrs.probes.startup.timeoutSeconds" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.probes.startup.timeoutSeconds }
:   Type `integer`, default `2`, minimum `1`.

`rondb.rondb.rdrs.security` <a class="headerlink" href="#helm.rondb.rondb.rdrs.security" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.security }
:   Type `object`.

`rondb.rondb.rdrs.security.apiKey` <a class="headerlink" href="#helm.rondb.rondb.rdrs.security.apiKey" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.security.apiKey }
:   Type `object`.

`rondb.rondb.rdrs.security.apiKey.cacheRefreshIntervalMS` <a class="headerlink" href="#helm.rondb.rondb.rdrs.security.apiKey.cacheRefreshIntervalMS" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.security.apiKey.cacheRefreshIntervalMS }
:   Type `integer`, default `180000`, minimum `1000`.
    How often the API key cache refreshes project associations from the database (in milliseconds). Lower values reduce staleness when project memberships change but increase database load.

`rondb.rondb.rdrs.ttlPurge` <a class="headerlink" href="#helm.rondb.rondb.rdrs.ttlPurge" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.ttlPurge }
:   Type `object`.
    TTL purge worker settings of every RDRS pod, rendered as the TTLPurge section of rest_api.json. The section is rendered only when at least one field is set, because RDRS older than RonDB 26.02.9 rejects the TTLPurge key and does not start. Changes reach running pods only when they restart; a cluster-wide window in the mysql.ttl_purge_ctrl table takes precedence over activeWindow and needs no restart. When installed through the Hopsworks chart, the path is rondb.rondb.rdrs.ttlPurge. Unknown fields fail the render, so a misspelled field cannot silently leave purging running around the clock.

`rondb.rondb.rdrs.ttlPurge.activeWindow` <a class="headerlink" href="#helm.rondb.rondb.rdrs.ttlPurge.activeWindow" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.ttlPurge.activeWindow }
:   Type `string|null`, default `null`, pattern `^$|^([01][0-9]|2[0-3]):[0-5][0-9]-([01][0-9]|2[0-3]):[0-5][0-9]$`.
    Daily UTC window during which the TTL purge worker deletes expired rows, formatted "HH:MM-HH:MM" (e.g. "03:00-05:00"); it wraps past midnight when start > end (e.g. "23:00-02:00"). Start and end must differ. When null or empty, purging runs around the clock. A valid window in mysql.ttl_purge_ctrl (ctrl_id 2/3) takes precedence.

`rondb.rondb.rdrs.ttlPurge.enable` <a class="headerlink" href="#helm.rondb.rondb.rdrs.ttlPurge.enable" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.ttlPurge.enable }
:   Type `boolean|null`, default `null`.
    Whether the RDRS pods run the TTL purge worker, which deletes expired rows of TTL tables. When null, RDRS decides (enabled). Can still be changed per pod at runtime through PUT /0.1.0/ttl-purge/config, until the pod restarts.

`rondb.rondb.rdrs.uploadPath` <a class="headerlink" href="#helm.rondb.rondb.rdrs.uploadPath" title="Permanent link">#</a> { #helm.rondb.rondb.rdrs.uploadPath }
:   Type `string`, default `"/tmp/rdrs-uploads"`.
    Writable directory where RDRS buffers HTTP request bodies larger than 64KiB. The container's working directory is not writable (RDRS runs as uid 1000): without this, every startup logs 256 'Permission denied' errors and oversized bodies are silently read as empty. Requires an RDRS image with REST.UploadPath support (releases 26.02.11 and newer on the 26.02 line); set to the empty string for pinned older images, which reject the unknown key.

</div>

### resources { #helm-values-rondb-rondb-resources }

??? example "Defaults as YAML"

    ```yaml
    rondb:
      rondb:
        resources:
          limits:
            cpus:
              benchs: 2
              mgmds: 0.2
              mysqldExporters: 0.2
              mysqlds: 2
              ndbmtds: 2
              rdrs: 2
              restore: 1
            memory:
              benchsMiB: 500
              mysqldExportersMiB: 100
              mysqldMiB: 1400
              ndbmtdsMiB: 5000
              rdrsMiB: 500
          requests:
            cpus:
              benchs: 1
              mgmds: 0.2
              mysqldExporters: 0.02
              mysqlds: 1
              rdrs: 1
            memory:
              benchsMiB: 100
              mysqldExportersMiB: 50
              mysqldMiB: 650
              rdrsMiB: 100
            storage:
              binlogGiB: 4
              classes:
                binlogFiles: null
                default: null
                diskColumns: null
                mgmd: null
              diskColumnGiB: 2
              logGiB: 2
              mgmdGiB: 1
              ndbmtdGiB: 30
              redoLogGiB: 4
              relayLogGiB: 2
              undoLogsGiB: 4
    ```

<div class="hops-values" markdown>

`rondb.rondb.resources` <a class="headerlink" href="#helm.rondb.rondb.resources" title="Permanent link">#</a> { #helm.rondb.rondb.resources }
:   Type `object`.
    Vertical cluster size

`rondb.rondb.resources.limits` <a class="headerlink" href="#helm.rondb.rondb.resources.limits" title="Permanent link">#</a> { #helm.rondb.rondb.resources.limits }
:   Type `object`.
    Kubernetes resource limits

`rondb.rondb.resources.limits.cpus` <a class="headerlink" href="#helm.rondb.rondb.resources.limits.cpus" title="Permanent link">#</a> { #helm.rondb.rondb.resources.limits.cpus }
:   Type `object`.
    CPU resources per RonDB service type

`rondb.rondb.resources.limits.cpus.benchs` <a class="headerlink" href="#helm.rondb.rondb.resources.limits.cpus.benchs" title="Permanent link">#</a> { #helm.rondb.rondb.resources.limits.cpus.benchs }
:   Type `number`, default `2`.

`rondb.rondb.resources.limits.cpus.mgmds` <a class="headerlink" href="#helm.rondb.rondb.resources.limits.cpus.mgmds" title="Permanent link">#</a> { #helm.rondb.rondb.resources.limits.cpus.mgmds }
:   Type `number`, default `0.2`.

`rondb.rondb.resources.limits.cpus.mysqldExporters` <a class="headerlink" href="#helm.rondb.rondb.resources.limits.cpus.mysqldExporters" title="Permanent link">#</a> { #helm.rondb.rondb.resources.limits.cpus.mysqldExporters }
:   Type `number`, default `0.2`.

`rondb.rondb.resources.limits.cpus.mysqlds` <a class="headerlink" href="#helm.rondb.rondb.resources.limits.cpus.mysqlds" title="Permanent link">#</a> { #helm.rondb.rondb.resources.limits.cpus.mysqlds }
:   Type `number`, default `2`.

`rondb.rondb.resources.limits.cpus.ndbmtds` <a class="headerlink" href="#helm.rondb.rondb.resources.limits.cpus.ndbmtds" title="Permanent link">#</a> { #helm.rondb.rondb.resources.limits.cpus.ndbmtds }
:   Type `number`, default `2`.

`rondb.rondb.resources.limits.cpus.rdrs` <a class="headerlink" href="#helm.rondb.rondb.resources.limits.cpus.rdrs" title="Permanent link">#</a> { #helm.rondb.rondb.resources.limits.cpus.rdrs }
:   Type `number`, default `2`.

`rondb.rondb.resources.limits.cpus.restore` <a class="headerlink" href="#helm.rondb.rondb.resources.limits.cpus.restore" title="Permanent link">#</a> { #helm.rondb.rondb.resources.limits.cpus.restore }
:   Type `number`, default `1`.

`rondb.rondb.resources.limits.memory` <a class="headerlink" href="#helm.rondb.rondb.resources.limits.memory" title="Permanent link">#</a> { #helm.rondb.rondb.resources.limits.memory }
:   Type `object`.
    Memory resources per RonDB service type

`rondb.rondb.resources.limits.memory.benchsMiB` <a class="headerlink" href="#helm.rondb.rondb.resources.limits.memory.benchsMiB" title="Permanent link">#</a> { #helm.rondb.rondb.resources.limits.memory.benchsMiB }
:   Type `integer`, default `500`.

`rondb.rondb.resources.limits.memory.mysqldExportersMiB` <a class="headerlink" href="#helm.rondb.rondb.resources.limits.memory.mysqldExportersMiB" title="Permanent link">#</a> { #helm.rondb.rondb.resources.limits.memory.mysqldExportersMiB }
:   Type `integer`, default `100`.

`rondb.rondb.resources.limits.memory.mysqldMiB` <a class="headerlink" href="#helm.rondb.rondb.resources.limits.memory.mysqldMiB" title="Permanent link">#</a> { #helm.rondb.rondb.resources.limits.memory.mysqldMiB }
:   Type `integer`, default `1400`.
    This can usually be kept at the default independent of the load

`rondb.rondb.resources.limits.memory.ndbmtdsMiB` <a class="headerlink" href="#helm.rondb.rondb.resources.limits.memory.ndbmtdsMiB" title="Permanent link">#</a> { #helm.rondb.rondb.resources.limits.memory.ndbmtdsMiB }
:   Type `integer`, default `5000`, minimum `2800`.
    It is recommended to keep this above 5GiB, otherwise some memory parts will be configured manually.

`rondb.rondb.resources.limits.memory.rdrsMiB` <a class="headerlink" href="#helm.rondb.rondb.resources.limits.memory.rdrsMiB" title="Permanent link">#</a> { #helm.rondb.rondb.resources.limits.memory.rdrsMiB }
:   Type `integer`, default `500`.

`rondb.rondb.resources.requests` <a class="headerlink" href="#helm.rondb.rondb.resources.requests" title="Permanent link">#</a> { #helm.rondb.rondb.resources.requests }
:   Type `object`.
    Kubernetes resource requests; Note that data nodes will only apply limits, not requests

`rondb.rondb.resources.requests.cpus` <a class="headerlink" href="#helm.rondb.rondb.resources.requests.cpus" title="Permanent link">#</a> { #helm.rondb.rondb.resources.requests.cpus }
:   Type `object`.
    CPU resources per RonDB service type

`rondb.rondb.resources.requests.cpus.benchs` <a class="headerlink" href="#helm.rondb.rondb.resources.requests.cpus.benchs" title="Permanent link">#</a> { #helm.rondb.rondb.resources.requests.cpus.benchs }
:   Type `number`, default `1`.

`rondb.rondb.resources.requests.cpus.mgmds` <a class="headerlink" href="#helm.rondb.rondb.resources.requests.cpus.mgmds" title="Permanent link">#</a> { #helm.rondb.rondb.resources.requests.cpus.mgmds }
:   Type `number`, default `0.2`.

`rondb.rondb.resources.requests.cpus.mysqldExporters` <a class="headerlink" href="#helm.rondb.rondb.resources.requests.cpus.mysqldExporters" title="Permanent link">#</a> { #helm.rondb.rondb.resources.requests.cpus.mysqldExporters }
:   Type `number`, default `0.02`.

`rondb.rondb.resources.requests.cpus.mysqlds` <a class="headerlink" href="#helm.rondb.rondb.resources.requests.cpus.mysqlds" title="Permanent link">#</a> { #helm.rondb.rondb.resources.requests.cpus.mysqlds }
:   Type `number`, default `1`.

`rondb.rondb.resources.requests.cpus.rdrs` <a class="headerlink" href="#helm.rondb.rondb.resources.requests.cpus.rdrs" title="Permanent link">#</a> { #helm.rondb.rondb.resources.requests.cpus.rdrs }
:   Type `number`, default `1`.

`rondb.rondb.resources.requests.memory` <a class="headerlink" href="#helm.rondb.rondb.resources.requests.memory" title="Permanent link">#</a> { #helm.rondb.rondb.resources.requests.memory }
:   Type `object`.
    Memory resources per RonDB service type

`rondb.rondb.resources.requests.memory.benchsMiB` <a class="headerlink" href="#helm.rondb.rondb.resources.requests.memory.benchsMiB" title="Permanent link">#</a> { #helm.rondb.rondb.resources.requests.memory.benchsMiB }
:   Type `integer`, default `100`.

`rondb.rondb.resources.requests.memory.mysqldExportersMiB` <a class="headerlink" href="#helm.rondb.rondb.resources.requests.memory.mysqldExportersMiB" title="Permanent link">#</a> { #helm.rondb.rondb.resources.requests.memory.mysqldExportersMiB }
:   Type `integer`, default `50`.

`rondb.rondb.resources.requests.memory.mysqldMiB` <a class="headerlink" href="#helm.rondb.rondb.resources.requests.memory.mysqldMiB" title="Permanent link">#</a> { #helm.rondb.rondb.resources.requests.memory.mysqldMiB }
:   Type `integer`, default `650`.
    This can usually be kept at the default independent of the load

`rondb.rondb.resources.requests.memory.rdrsMiB` <a class="headerlink" href="#helm.rondb.rondb.resources.requests.memory.rdrsMiB" title="Permanent link">#</a> { #helm.rondb.rondb.resources.requests.memory.rdrsMiB }
:   Type `integer`, default `100`.

`rondb.rondb.resources.requests.storage` <a class="headerlink" href="#helm.rondb.rondb.resources.requests.storage" title="Permanent link">#</a> { #helm.rondb.rondb.resources.requests.storage }
:   Type `object`.
    Volume specifications

`rondb.rondb.resources.requests.storage.binlogGiB` <a class="headerlink" href="#helm.rondb.rondb.resources.requests.storage.binlogGiB" title="Permanent link">#</a> { #helm.rondb.rondb.resources.requests.storage.binlogGiB }
:   Type `integer`, default `4`, minimum `1`.
    Keep in mind that this size needs to survive the retention period of the binlog files

`rondb.rondb.resources.requests.storage.classes` <a class="headerlink" href="#helm.rondb.rondb.resources.requests.storage.classes" title="Permanent link">#</a> { #helm.rondb.rondb.resources.requests.storage.classes }
:   Type `object`.
    Storage classes

`rondb.rondb.resources.requests.storage.classes.binlogFiles` <a class="headerlink" href="#helm.rondb.rondb.resources.requests.storage.classes.binlogFiles" title="Permanent link">#</a> { #helm.rondb.rondb.resources.requests.storage.classes.binlogFiles }
:   Type `string|null`, default `null`.
    Storage class name for MySQLd binlog volumes in global replication

`rondb.rondb.resources.requests.storage.classes.default` <a class="headerlink" href="#helm.rondb.rondb.resources.requests.storage.classes.default" title="Permanent link">#</a> { #helm.rondb.rondb.resources.requests.storage.classes.default }
:   Type `string|null`, default `null`.
    Default storage class name for all volumes

`rondb.rondb.resources.requests.storage.classes.diskColumns` <a class="headerlink" href="#helm.rondb.rondb.resources.requests.storage.classes.diskColumns" title="Permanent link">#</a> { #helm.rondb.rondb.resources.requests.storage.classes.diskColumns }
:   Type `string|null`, default `null`.
    Storage class name for the data node disk columns volume

`rondb.rondb.resources.requests.storage.classes.mgmd` <a class="headerlink" href="#helm.rondb.rondb.resources.requests.storage.classes.mgmd" title="Permanent link">#</a> { #helm.rondb.rondb.resources.requests.storage.classes.mgmd }
:   Type `string|null`, default `null`.
    Storage class name for Management server

`rondb.rondb.resources.requests.storage.diskColumnGiB` <a class="headerlink" href="#helm.rondb.rondb.resources.requests.storage.diskColumnGiB" title="Permanent link">#</a> { #helm.rondb.rondb.resources.requests.storage.diskColumnGiB }
:   Type `integer`, default `2`, minimum `1`.
    This depends on how much data the user is expecting to place on disk

`rondb.rondb.resources.requests.storage.logGiB` <a class="headerlink" href="#helm.rondb.rondb.resources.requests.storage.logGiB" title="Permanent link">#</a> { #helm.rondb.rondb.resources.requests.storage.logGiB }
:   Type `integer`, default `2`.

`rondb.rondb.resources.requests.storage.mgmdGiB` <a class="headerlink" href="#helm.rondb.rondb.resources.requests.storage.mgmdGiB" title="Permanent link">#</a> { #helm.rondb.rondb.resources.requests.storage.mgmdGiB }
:   Type `integer`, default `1`, minimum `1`.
    The size of the statefulSet persistent volume for the RonDB management node. It will be used in new installations or in case of lookup function failing during upgrade in argo deployments.

`rondb.rondb.resources.requests.storage.ndbmtdGiB` <a class="headerlink" href="#helm.rondb.rondb.resources.requests.storage.ndbmtdGiB" title="Permanent link">#</a> { #helm.rondb.rondb.resources.requests.storage.ndbmtdGiB }
:   Type `integer`, default `30`, minimum `0`.
    The size of the statefulSet persistent volume for the RonDB data nodes. It will be used in new installations or in case of lookup function failing during upgrade in argo deployments.

`rondb.rondb.resources.requests.storage.redoLogGiB` <a class="headerlink" href="#helm.rondb.rondb.resources.requests.storage.redoLogGiB" title="Permanent link">#</a> { #helm.rondb.rondb.resources.requests.storage.redoLogGiB }
:   Type `integer`, default `4`, minimum `2`, maximum `64`.
    64GiB is recommended for optimal performance

`rondb.rondb.resources.requests.storage.relayLogGiB` <a class="headerlink" href="#helm.rondb.rondb.resources.requests.storage.relayLogGiB" title="Permanent link">#</a> { #helm.rondb.rondb.resources.requests.storage.relayLogGiB }
:   Type `integer`, default `2`, minimum `1`.

`rondb.rondb.resources.requests.storage.undoLogsGiB` <a class="headerlink" href="#helm.rondb.rondb.resources.requests.storage.undoLogsGiB" title="Permanent link">#</a> { #helm.rondb.rondb.resources.requests.storage.undoLogsGiB }
:   Type `integer`, default `4`, minimum `1`, maximum `128`.
    64GiB is recommended for good performance

</div>

### restoreFromBackup { #helm-values-rondb-rondb-restorefrombackup }

??? example "Defaults as YAML"

    ```yaml
    rondb:
      rondb:
        restoreFromBackup:
          backupId: null
          excludeDatabases: []
          excludeTables: []
          forceDataClear: null
          inPlace: null
          objectStorageProvider: s3
          pathPrefix: rondb_backup
          s3:
            bucketName: null
            endpoint: null
            keyCredentialsSecret:
              key: null
              name: null
            provider: null
            region: null
            secretCredentialsSecret:
              key: null
              name: null
            serverSideEncryption: null
    ```

<div class="hops-values" markdown>

`rondb.rondb.restoreFromBackup` <a class="headerlink" href="#helm.rondb.rondb.restoreFromBackup" title="Permanent link">#</a> { #helm.rondb.rondb.restoreFromBackup }
:   Type `object`.
    Whether to restore a backup on the cluster

`rondb.rondb.restoreFromBackup.backupId` <a class="headerlink" href="#helm.rondb.rondb.restoreFromBackup.backupId" title="Permanent link">#</a> { #helm.rondb.rondb.restoreFromBackup.backupId }
:   Type `string|null`, default `null`.
    The native backup ID for the backup to restore

`rondb.rondb.restoreFromBackup.excludeDatabases` <a class="headerlink" href="#helm.rondb.rondb.restoreFromBackup.excludeDatabases" title="Permanent link">#</a> { #helm.rondb.rondb.restoreFromBackup.excludeDatabases }
:   Type `array`, default `[]`.
    Which databases to exclude from the native backup

`rondb.rondb.restoreFromBackup.excludeTables` <a class="headerlink" href="#helm.rondb.rondb.restoreFromBackup.excludeTables" title="Permanent link">#</a> { #helm.rondb.rondb.restoreFromBackup.excludeTables }
:   Type `array`, default `[]`.
    Which tables to exclude from the native backup. Use the format: database.table

`rondb.rondb.restoreFromBackup.forceDataClear` <a class="headerlink" href="#helm.rondb.rondb.restoreFromBackup.forceDataClear" title="Permanent link">#</a> { #helm.rondb.rondb.restoreFromBackup.forceDataClear }
:   Type `boolean|null`, default `null`.
    Confirm that existing data will be destroyed during in-place restore.

`rondb.rondb.restoreFromBackup.inPlace` <a class="headerlink" href="#helm.rondb.rondb.restoreFromBackup.inPlace" title="Permanent link">#</a> { #helm.rondb.rondb.restoreFromBackup.inPlace }
:   Type `boolean|null`, default `null`.
    Enable in-place restore on existing cluster. Requires forceDataClear=true.

`rondb.rondb.restoreFromBackup.objectStorageProvider` <a class="headerlink" href="#helm.rondb.rondb.restoreFromBackup.objectStorageProvider" title="Permanent link">#</a> { #helm.rondb.rondb.restoreFromBackup.objectStorageProvider }
:   Type `enum`, default `"s3"`.
    One of: `"s3"`.

`rondb.rondb.restoreFromBackup.pathPrefix` <a class="headerlink" href="#helm.rondb.rondb.restoreFromBackup.pathPrefix" title="Permanent link">#</a> { #helm.rondb.rondb.restoreFromBackup.pathPrefix }
:   Type `string`, default `"rondb_backup"`.
    Prefix of RonDB backup in the configured bucket

`rondb.rondb.restoreFromBackup.s3` <a class="headerlink" href="#helm.rondb.rondb.restoreFromBackup.s3" title="Permanent link">#</a> { #helm.rondb.rondb.restoreFromBackup.s3 }
:   Type `object`.

`rondb.rondb.restoreFromBackup.s3.bucketName` <a class="headerlink" href="#helm.rondb.rondb.restoreFromBackup.s3.bucketName" title="Permanent link">#</a> { #helm.rondb.rondb.restoreFromBackup.s3.bucketName }
:   Type `string|null`, default `null`.

`rondb.rondb.restoreFromBackup.s3.endpoint` <a class="headerlink" href="#helm.rondb.rondb.restoreFromBackup.s3.endpoint" title="Permanent link">#</a> { #helm.rondb.rondb.restoreFromBackup.s3.endpoint }
:   Type `string|null`, default `null`.

`rondb.rondb.restoreFromBackup.s3.keyCredentialsSecret` <a class="headerlink" href="#helm.rondb.rondb.restoreFromBackup.s3.keyCredentialsSecret" title="Permanent link">#</a> { #helm.rondb.rondb.restoreFromBackup.s3.keyCredentialsSecret }
:   Type `object`.

`rondb.rondb.restoreFromBackup.s3.keyCredentialsSecret.key` <a class="headerlink" href="#helm.rondb.rondb.restoreFromBackup.s3.keyCredentialsSecret.key" title="Permanent link">#</a> { #helm.rondb.rondb.restoreFromBackup.s3.keyCredentialsSecret.key }
:   Type `string|null`, default `null`.
    Key in the Secret

`rondb.rondb.restoreFromBackup.s3.keyCredentialsSecret.name` <a class="headerlink" href="#helm.rondb.rondb.restoreFromBackup.s3.keyCredentialsSecret.name" title="Permanent link">#</a> { #helm.rondb.rondb.restoreFromBackup.s3.keyCredentialsSecret.name }
:   Type `string|null`, default `null`.
    Name of the Secret

`rondb.rondb.restoreFromBackup.s3.provider` <a class="headerlink" href="#helm.rondb.rondb.restoreFromBackup.s3.provider" title="Permanent link">#</a> { #helm.rondb.rondb.restoreFromBackup.s3.provider }
:   Type `string|null`, default `null`.

`rondb.rondb.restoreFromBackup.s3.region` <a class="headerlink" href="#helm.rondb.rondb.restoreFromBackup.s3.region" title="Permanent link">#</a> { #helm.rondb.rondb.restoreFromBackup.s3.region }
:   Type `string|null`, default `null`.

`rondb.rondb.restoreFromBackup.s3.secretCredentialsSecret` <a class="headerlink" href="#helm.rondb.rondb.restoreFromBackup.s3.secretCredentialsSecret" title="Permanent link">#</a> { #helm.rondb.rondb.restoreFromBackup.s3.secretCredentialsSecret }
:   Type `object`.

`rondb.rondb.restoreFromBackup.s3.secretCredentialsSecret.key` <a class="headerlink" href="#helm.rondb.rondb.restoreFromBackup.s3.secretCredentialsSecret.key" title="Permanent link">#</a> { #helm.rondb.rondb.restoreFromBackup.s3.secretCredentialsSecret.key }
:   Type `string|null`, default `null`.
    Key in the Secret

`rondb.rondb.restoreFromBackup.s3.secretCredentialsSecret.name` <a class="headerlink" href="#helm.rondb.rondb.restoreFromBackup.s3.secretCredentialsSecret.name" title="Permanent link">#</a> { #helm.rondb.rondb.restoreFromBackup.s3.secretCredentialsSecret.name }
:   Type `string|null`, default `null`.
    Name of the Secret

`rondb.rondb.restoreFromBackup.s3.serverSideEncryption` <a class="headerlink" href="#helm.rondb.rondb.restoreFromBackup.s3.serverSideEncryption" title="Permanent link">#</a> { #helm.rondb.rondb.restoreFromBackup.s3.serverSideEncryption }
:   Type `enum`, default `null`.
    One of: `"aws:kms"`, `"aws:kms:dsse"`, `"AES256"`, `null`.

</div>

### rondbConfig { #helm-values-rondb-rondb-rondbconfig }

??? example "Defaults as YAML"

    ```yaml
    rondb:
      rondb:
        rondbConfig:
          ActivateRateLimits: 0
          BackupLogBufferSize: 16M
          DataMemory: null
          DiskPageBufferMemory: null
          EmptyApiSlots: 8
          FullRestartLogs: null
          HeartbeatIntervalDbApi: 5000
          HeartbeatIntervalDbDb: 5000
          InitialTablespaceSizeGiB: -1
          LongMessageBuffer: null
          MaxDMLOperationsPerTransaction: 32768
          MaxDiskWriteSpeed: null
          MaxNoOfAttributes: null
          MaxNoOfConcurrentOperations: 65536
          MaxNoOfSchemaObjects: null
          MaxNoOfTables: null
          MaxNoOfTriggers: null
          MaxRRGroupSize: null
          MySQLdSlotsPerNode: 4
          OsCpuOverhead: null
          OsStaticOverhead: null
          PartitionsPerNode: null
          RdrsMetadataSlotsPerNode: 1
          RdrsSlotsPerNode: 1
          RedoBuffer: null
          ReplicationMemory: null
          ReservedConcurrentOperations: null
          SchemaMemory: null
          SharedGlobalMemory: null
          TimeBetweenGlobalCheckpoints: null
          TotalMemoryConfig: null
          TransactionDeadlockDetectionTimeout: 1500
          TransactionInactiveTimeout: 15000
          TransactionMemory: null
          UseOnlyIPv4: null
          UseTcInRRGroup: null
    ```

<div class="hops-values" markdown>

`rondb.rondb.rondbConfig` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig }
:   Type `object`.
    Configurations for RonDB's config.ini. Memory configurations are in binary SI units (i.e. 1G = 1GiB = 1024MiB).

`rondb.rondb.rondbConfig.ActivateRateLimits` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.ActivateRateLimits" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.ActivateRateLimits }
:   Type `integer`, default `0`, minimum `0`, maximum `1`.
    Activate rate limits handling

`rondb.rondb.rondbConfig.BackupLogBufferSize` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.BackupLogBufferSize" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.BackupLogBufferSize }
:   Type `string`, default `"16M"`.
    Buffer that records writes occurring during an online backup; the backup aborts if it fills. Default 16M; increase (e.g. 256M) for write-heavy clusters. See <https://docs.rondb.com/rondb_backup/>.

`rondb.rondb.rondbConfig.DataMemory` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.DataMemory" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.DataMemory }
:   Type `string|null`, default `null`, example `"4G"`.
    Memory available for storing in-memory database records on each data node, in bytes (with optional binary SI suffix, e.g. '4G'). When unset, RonDB's AutomaticMemoryConfig sizes this from the container's memory; only set explicitly to override automatic sizing. Only applied if explicitly set.

`rondb.rondb.rondbConfig.DiskPageBufferMemory` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.DiskPageBufferMemory" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.DiskPageBufferMemory }
:   Type `string|null`, default `null`.
    DiskPageBufferMemory are used by disk columns. This is the page cache that contains disk pages when they are in memory. By default it is not defined.

`rondb.rondb.rondbConfig.EmptyApiSlots` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.EmptyApiSlots" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.EmptyApiSlots }
:   Type `integer`, default `8`, minimum `1`.
    We need at least 1 for the MySQLd setup job. Otherwise this is for services that are not handled here, e.g. HopsFS

`rondb.rondb.rondbConfig.FullRestartLogs` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.FullRestartLogs" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.FullRestartLogs }
:   Type `boolean|null`, default `null`.
    Enable full restart logs (RonDB-specific). RonDB's release-build default is false.

`rondb.rondb.rondbConfig.HeartbeatIntervalDbApi` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.HeartbeatIntervalDbApi" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.HeartbeatIntervalDbApi }
:   Type `integer`, default `5000`.
    Each data node sends heartbeat signals to each MySQL server (SQL node) to ensure that it remains in contact. If a MySQL server fails to send a heartbeat in time it is declared “dead,” in which case all ongoing transactions are completed and all resources released. The SQL node cannot reconnect until all activities initiated by the previous MySQL instance have been completed. The three-heartbeat criteria for this determination are the same as described for HeartbeatIntervalDbDb.

`rondb.rondb.rondbConfig.HeartbeatIntervalDbDb` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.HeartbeatIntervalDbDb" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.HeartbeatIntervalDbDb }
:   Type `integer`, default `5000`.
    One of the primary methods of discovering failed nodes is by the use of heartbeats. This parameter states how often heartbeat signals are sent and how often to expect to receive them. Heartbeats cannot be disabled. After missing four heartbeat intervals in a row, the node is declared dead. Thus, the maximum time for discovering a failure through the heartbeat mechanism is five times the heartbeat interval.

`rondb.rondb.rondbConfig.InitialTablespaceSizeGiB` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.InitialTablespaceSizeGiB" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.InitialTablespaceSizeGiB }
:   Type `integer`, default `-1`.
    InitialTableSpace size in GiB. By default, it is set to -1, which enforces the initial tablespace to use the entire diskColumnGiB space. If set to 0, the same behaviour applies and the diskColumnGiB is used.

`rondb.rondb.rondbConfig.LongMessageBuffer` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.LongMessageBuffer" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.LongMessageBuffer }
:   Type `string|null`, default `null`, example `"64M"`.
    Internal buffer used for passing long messages within and between nodes, in bytes (with optional binary SI suffix). NDB's built-in default is 64M. Only applied if explicitly set.

`rondb.rondb.rondbConfig.MaxDMLOperationsPerTransaction` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.MaxDMLOperationsPerTransaction" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.MaxDMLOperationsPerTransaction }
:   Type `integer`, default `32768`, minimum `32`, maximum `4294967039`.

`rondb.rondb.rondbConfig.MaxDiskWriteSpeed` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.MaxDiskWriteSpeed" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.MaxDiskWriteSpeed }
:   Type `string|null`, default `null`, example `"20M"`.
    Maximum disk write speed (bytes/sec, total across all ldm threads) used by local checkpoints during normal operation, i.e. when no node is restarting. The adaptive algorithm may write more slowly than this ceiling based on CPU usage and REDO log IO lag, but will not exceed it. Only applied if explicitly set; otherwise RonDB's built-in default is used. See <https://docs.rondb.com/rondb_advanced_fs_config/>.

`rondb.rondb.rondbConfig.MaxNoOfAttributes` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.MaxNoOfAttributes" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.MaxNoOfAttributes }
:   Type `integer|null`, default `null`.

`rondb.rondb.rondbConfig.MaxNoOfConcurrentOperations` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.MaxNoOfConcurrentOperations" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.MaxNoOfConcurrentOperations }
:   Type `integer`, default `65536`, minimum `32`, maximum `4294967039`.

`rondb.rondb.rondbConfig.MaxNoOfSchemaObjects` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.MaxNoOfSchemaObjects" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.MaxNoOfSchemaObjects }
:   Type `integer|null`, default `null`, minimum `20320`, maximum `200000`.
    Maximum total number of schema objects (tables, ordered indexes, unique hash indexes, etc.) that a data node may allocate. Increase this when the application needs more than the default cap of 20,320 table objects. Only applied if explicitly set; otherwise RonDB's built-in default is used. See <https://docs.rondb.com/automatic_memory_config/>.

`rondb.rondb.rondbConfig.MaxNoOfTables` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.MaxNoOfTables" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.MaxNoOfTables }
:   Type `integer|null`, default `null`.

`rondb.rondb.rondbConfig.MaxNoOfTriggers` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.MaxNoOfTriggers" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.MaxNoOfTriggers }
:   Type `integer|null`, default `null`.

`rondb.rondb.rondbConfig.MaxRRGroupSize` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.MaxRRGroupSize" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.MaxRRGroupSize }
:   Type `integer|null`, default `null`, minimum `8`, maximum `32`.
    Max size of a Round Robin (RR) group. RonDB default is 8; allowed range is 8 to 32.

`rondb.rondb.rondbConfig.MySQLdSlotsPerNode` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.MySQLdSlotsPerNode" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.MySQLdSlotsPerNode }
:   Type `integer`, default `4`, minimum `1`, maximum `4`.

`rondb.rondb.rondbConfig.OsCpuOverhead` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.OsCpuOverhead" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.OsCpuOverhead }
:   Type `string|null`, default `null`, example `"100M"`.
    Additional OS memory overhead for the RonDB datanode containers. This is multiplied by the number of CPUs. Also only set this if the container has less than 5GiB of memory.

`rondb.rondb.rondbConfig.OsStaticOverhead` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.OsStaticOverhead" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.OsStaticOverhead }
:   Type `string|null`, default `null`, example `"1400M"`.
    Memory overhead for the RonDB datanode containers. Only set this if the container has less than 5GiB of memory.

`rondb.rondb.rondbConfig.PartitionsPerNode` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.PartitionsPerNode" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.PartitionsPerNode }
:   Type `integer|null`, default `null`.
    Number of partitions per data node used when creating new tables. When null, RonDB chooses based on AutomaticThreadConfig / NumCPUs (typically the number of LDM threads). Only affects tables created after the change; existing tables are not repartitioned.

`rondb.rondb.rondbConfig.RdrsMetadataSlotsPerNode` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.RdrsMetadataSlotsPerNode" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.RdrsMetadataSlotsPerNode }
:   Type `integer`, default `1`, minimum `1`, maximum `1`.
    We use additional cluster connections for metadata

`rondb.rondb.rondbConfig.RdrsSlotsPerNode` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.RdrsSlotsPerNode" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.RdrsSlotsPerNode }
:   Type `integer`, default `1`, minimum `1`, maximum `1`.
    The number of cluster connections we support via the RDRS

`rondb.rondb.rondbConfig.RedoBuffer` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.RedoBuffer" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.RedoBuffer }
:   Type `string|null`, default `null`.

`rondb.rondb.rondbConfig.ReplicationMemory` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.ReplicationMemory" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.ReplicationMemory }
:   Type `string|null`, default `null`.

`rondb.rondb.rondbConfig.ReservedConcurrentOperations` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.ReservedConcurrentOperations" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.ReservedConcurrentOperations }
:   Type `integer|null`, default `null`.

`rondb.rondb.rondbConfig.SchemaMemory` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.SchemaMemory" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.SchemaMemory }
:   Type `string|null`, default `null`.

`rondb.rondb.rondbConfig.SharedGlobalMemory` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.SharedGlobalMemory" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.SharedGlobalMemory }
:   Type `string|null`, default `null`.

`rondb.rondb.rondbConfig.TimeBetweenGlobalCheckpoints` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.TimeBetweenGlobalCheckpoints" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.TimeBetweenGlobalCheckpoints }
:   Type `integer|null`, default `null`, minimum `20`, maximum `32000`, example `2000`.
    Time in milliseconds between group commits of transactions to disk. RonDB's built-in default is 2000 ms. Only applied if explicitly set.

`rondb.rondb.rondbConfig.TotalMemoryConfig` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.TotalMemoryConfig" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.TotalMemoryConfig }
:   Type `string|null`, default `null`.
    The total memory configured by RonDB datanode. By default it is not defined and memory is calculated automatically.

`rondb.rondb.rondbConfig.TransactionDeadlockDetectionTimeout` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.TransactionDeadlockDetectionTimeout" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.TransactionDeadlockDetectionTimeout }
:   Type `integer`, default `1500`.
    Time transaction can spend executing within data node

`rondb.rondb.rondbConfig.TransactionInactiveTimeout` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.TransactionInactiveTimeout" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.TransactionInactiveTimeout }
:   Type `integer`, default `15000`.
    Milliseconds that application waits before executing another part of transaction

`rondb.rondb.rondbConfig.TransactionMemory` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.TransactionMemory" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.TransactionMemory }
:   Type `string|null`, default `null`.

`rondb.rondb.rondbConfig.UseOnlyIPv4` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.UseOnlyIPv4" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.UseOnlyIPv4 }
:   Type `boolean|null`, default `null`.
    When true, restricts all RonDB cluster connections to IPv4 sockets only. Applied under both \[NDBD DEFAULT\] and \[MYSQLD DEFAULT\] so it covers data nodes, MySQLds (including binlog/replica appliers/DDL), RDRS, and other API clients. Introduced in RonDB 21.04.5 for Dolphin SuperSockets compatibility.

`rondb.rondb.rondbConfig.UseTcInRRGroup` <a class="headerlink" href="#helm.rondb.rondb.rondbConfig.UseTcInRRGroup" title="Permanent link">#</a> { #helm.rondb.rondb.rondbConfig.UseTcInRRGroup }
:   Type `boolean|null`, default `null`.
    When true, each recv thread distributes connections only to TC threads within the same Round Robin (RR) group; when false, it distributes them across all TC threads. RonDB default is true.

</div>

### terminationGracePeriodSeconds { #helm-values-rondb-rondb-terminationgraceperiodseconds }

??? example "Defaults as YAML"

    ```yaml
    rondb:
      rondb:
        terminationGracePeriodSeconds:
          binlogServers: 30
          mgmds: 30
          mysqlds: 30
          ndbmtds: 300
          rdrs: 30
          replicaAppliers: 30
    ```

<div class="hops-values" markdown>

`rondb.rondb.terminationGracePeriodSeconds` <a class="headerlink" href="#helm.rondb.rondb.terminationGracePeriodSeconds" title="Permanent link">#</a> { #helm.rondb.rondb.terminationGracePeriodSeconds }
:   Type `object|integer`, minimum `10`.
    Pod terminationGracePeriodSeconds per RonDB service type. The chart's daemons stop on SIGTERM, so this is a ceiling, not a wait: a pod is removed as soon as its processes have exited. The legacy integer form (charts up to 26.2.19) still validates (minimum 10) and keeps its meaning: it overrides the data nodes only, every other component keeps 30. Helm drops null keys before schema validation: a null whole key falls back to the defaults, a null component key is rejected (all six keys are required; partial values files still work because Helm merges in the chart defaults).

`rondb.rondb.terminationGracePeriodSeconds.binlogServers` <a class="headerlink" href="#helm.rondb.rondb.terminationGracePeriodSeconds.binlogServers" title="Permanent link">#</a> { #helm.rondb.rondb.terminationGracePeriodSeconds.binlogServers }
:   Type `integer`, default `30`, minimum `10`.
    Binlog server MySQLds; see mysqlds.

`rondb.rondb.terminationGracePeriodSeconds.mgmds` <a class="headerlink" href="#helm.rondb.rondb.terminationGracePeriodSeconds.mgmds" title="Permanent link">#</a> { #helm.rondb.rondb.terminationGracePeriodSeconds.mgmds }
:   Type `integer`, default `30`, minimum `10`.
    MGMd stops within seconds; this matches the Kubernetes default.

`rondb.rondb.terminationGracePeriodSeconds.mysqlds` <a class="headerlink" href="#helm.rondb.rondb.terminationGracePeriodSeconds.mysqlds" title="Permanent link">#</a> { #helm.rondb.rondb.terminationGracePeriodSeconds.mysqlds }
:   Type `integer`, default `30`, minimum `10`.
    Used by MySQLds and DDL MySQLds; mysqld stops within seconds under no load, but allow time for open transactions to close.

`rondb.rondb.terminationGracePeriodSeconds.ndbmtds` <a class="headerlink" href="#helm.rondb.rondb.terminationGracePeriodSeconds.ndbmtds" title="Permanent link">#</a> { #helm.rondb.rondb.terminationGracePeriodSeconds.ndbmtds }
:   Type `integer`, default `300`, minimum `30`.
    Data nodes run a managed stop on SIGTERM: deactivate through the MGMd, then node shutdown with handover. Large nodes additionally need roughly 2 minutes per TB of data node memory for the kernel to tear the process down, so raise this for nodes above 1TB. Stops of several data nodes serialize at the MGMd. When deleting the entire cluster the MGMd may already be gone; data nodes then retry the deactivate for up to 60s before stopping directly.

`rondb.rondb.terminationGracePeriodSeconds.rdrs` <a class="headerlink" href="#helm.rondb.rondb.terminationGracePeriodSeconds.rdrs" title="Permanent link">#</a> { #helm.rondb.rondb.terminationGracePeriodSeconds.rdrs }
:   Type `integer`, default `30`, minimum `10`.
    RDRS stops within a few seconds; this matches the Kubernetes default.

`rondb.rondb.terminationGracePeriodSeconds.replicaAppliers` <a class="headerlink" href="#helm.rondb.rondb.terminationGracePeriodSeconds.replicaAppliers" title="Permanent link">#</a> { #helm.rondb.rondb.terminationGracePeriodSeconds.replicaAppliers }
:   Type `integer`, default `30`, minimum `10`.
    Replica applier pods: the controller container stops its run_applier.sh worker on SIGTERM, the pod's mysqld receives SIGTERM directly.

</div>

### timeoutsMinutes { #helm-values-rondb-rondb-timeoutsminutes }

??? example "Defaults as YAML"

    ```yaml
    rondb:
      rondb:
        timeoutsMinutes:
          mysqldStartupProbe: 20
          ndbmtdStartupProbe: 240
          restoreNativeBackup: 120
          singleSetupMySQLds: 5
    ```

<div class="hops-values" markdown>

`rondb.rondb.timeoutsMinutes` <a class="headerlink" href="#helm.rondb.rondb.timeoutsMinutes" title="Permanent link">#</a> { #helm.rondb.rondb.timeoutsMinutes }
:   Type `object`.
    Using minutes for easier template addition

`rondb.rondb.timeoutsMinutes.mysqldStartupProbe` <a class="headerlink" href="#helm.rondb.rondb.timeoutsMinutes.mysqldStartupProbe" title="Permanent link">#</a> { #helm.rondb.rondb.timeoutsMinutes.mysqldStartupProbe }
:   Type `integer`, default `20`, minimum `1`.
    Maximum time a MySQLd pod (mysqld, ddl mysqld, binlog server, replica applier) is given to start up before Kubernetes restarts its container.

`rondb.rondb.timeoutsMinutes.ndbmtdStartupProbe` <a class="headerlink" href="#helm.rondb.rondb.timeoutsMinutes.ndbmtdStartupProbe" title="Permanent link">#</a> { #helm.rondb.rondb.timeoutsMinutes.ndbmtdStartupProbe }
:   Type `integer`, default `240`, minimum `1`.
    Maximum time a ndbmtd pod is given to start up before Kubernetes restarts its container. Node restarts with a lot of data to restore can take long. Must clear the worst-case data reload of the largest supported cluster - a node killed mid-recovery restarts from scratch and loops forever.

`rondb.rondb.timeoutsMinutes.restoreNativeBackup` <a class="headerlink" href="#helm.rondb.rondb.timeoutsMinutes.restoreNativeBackup" title="Permanent link">#</a> { #helm.rondb.rondb.timeoutsMinutes.restoreNativeBackup }
:   Type `integer`, default `120`.
    This does not include *downloading* the native backups. IMPORTANT; Restoring native backups is NOT done in parallel yet; TODO: Make this dependent on amount of data

`rondb.rondb.timeoutsMinutes.singleSetupMySQLds` <a class="headerlink" href="#helm.rondb.rondb.timeoutsMinutes.singleSetupMySQLds" title="Permanent link">#</a> { #helm.rondb.rondb.timeoutsMinutes.singleSetupMySQLds }
:   Type `integer`, default `5`.
    This includes the time to start a single MySQLd pod, restoring MySQL metadata and running user-defined MySQL init scripts.

</div>

### tolerations { #helm-values-rondb-rondb-tolerations }

??? example "Defaults as YAML"

    ```yaml
    rondb:
      rondb:
        tolerations:
          backup: []
          mgmd: []
          mysqld: []
          ndbmtd: []
          rdrs: []
    ```

<div class="hops-values" markdown>

`rondb.rondb.tolerations` <a class="headerlink" href="#helm.rondb.rondb.tolerations" title="Permanent link">#</a> { #helm.rondb.rondb.tolerations }
:   Type `object`.
    These tolerations allow Kubernetes to schedule pods on nodes with matching taints, ensuring proper placement based on cluster policies.

`rondb.rondb.tolerations.backup` <a class="headerlink" href="#helm.rondb.rondb.tolerations.backup" title="Permanent link">#</a> { #helm.rondb.rondb.tolerations.backup }
:   Type `array`, default `[]`.

`rondb.rondb.tolerations.mgmd` <a class="headerlink" href="#helm.rondb.rondb.tolerations.mgmd" title="Permanent link">#</a> { #helm.rondb.rondb.tolerations.mgmd }
:   Type `array`, default `[]`.

`rondb.rondb.tolerations.mysqld` <a class="headerlink" href="#helm.rondb.rondb.tolerations.mysqld" title="Permanent link">#</a> { #helm.rondb.rondb.tolerations.mysqld }
:   Type `array`, default `[]`.

`rondb.rondb.tolerations.ndbmtd` <a class="headerlink" href="#helm.rondb.rondb.tolerations.ndbmtd" title="Permanent link">#</a> { #helm.rondb.rondb.tolerations.ndbmtd }
:   Type `array`, default `[]`.

`rondb.rondb.tolerations.rdrs` <a class="headerlink" href="#helm.rondb.rondb.tolerations.rdrs" title="Permanent link">#</a> { #helm.rondb.rondb.tolerations.rdrs }
:   Type `array`, default `[]`.

</div>

<!-- END GENERATED VALUES -->
