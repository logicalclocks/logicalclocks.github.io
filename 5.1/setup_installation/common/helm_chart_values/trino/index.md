# Trino values { #helm-values-trino }

Values under `trino` configure Trino, the SQL query engine, and its test coordinator for user catalogs.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.1.0` (Hopsworks `5.1.0`)._

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
        accessControl:
          configFile: rules.json
          refreshPeriod: 10s
          rules:
            rules.json: |-
              {
                "catalogs": [
                  {
                    "group": "admin",
                    "catalog": ".*",
                    "allow": "owner"
                  },
                  {
                    "catalog": "system",
                    "allow": "none"
                  }
                ],
                "schemas": [
                  {
                    "group": "admin",
                    "schema": ".*",
                    "owner": true
                  }
                ],
                "tables": [
                  {
                    "group": "admin",
                    "privileges": [
                      "SELECT",
                      "INSERT",
                      "DELETE",
                      "UPDATE",
                      "OWNERSHIP"
                    ]
                  }
                ],
                "queries": [
                  {
                    "group": "admin",
                    "allow": ["execute", "kill", "view"]
                  }
                ]
              }
          type: configmap
        additionalCatalogs: {}
        additionalConfigProperties:
        - internal-communication.shared-secret=${ENV:TRINO_SHARED_SECRET}
        - http-server.process-forwarded=true
        - catalog.management=dynamic
        auth:
          groupsAuthSecret: trino-groups-file
          passwordAuthSecret: trino-password-file
          refreshPeriod: 5s
        catalogs: []
        coordinator:
          additionalJVMConfig:
          - --add-opens=java.base/java.nio=ALL-UNNAMED
          additionalVolumeMounts:
          - mountPath: /certs
            name: certs
            readOnly: true
          - mountPath: /etc/trino/catalog
            name: catalog-volume
          - mountPath: /opt/hopsworks/mounts
            mountPropagation: HostToContainer
            name: mountable-secrets
            readOnly: true
          additionalVolumes:
          - emptyDir: {}
            name: certs
          - emptyDir: {}
            name: catalog-volume
          - emptyDir: {}
            name: mountable-secrets
          config:
            nodeScheduler:
              includeCoordinator: true
          configMounts:
          - configMap: hopsfs-config
            name: hdfs-site
            path: /etc/hadoop/hdfs-site.xml
            subPath: hdfs-site.xml
          - configMap: hopsfs-config
            name: core-site
            path: /etc/hadoop/core-site.xml
            subPath: core-site.xml
          secretMounts:
          - name: super-crypto-kstore
            path: /srv/hops/super_crypto/trino
            secretName: hopsworks-trino-test-crypto-material
        coordinatorNameOverride: hopsworks-trino-test-coordinator
        env:
        - name: SSL_CERT_KEY_PASSWORD
          valueFrom:
            secretKeyRef:
              key: trino__passwd
              name: hopsworks-trino-test-crypto-material
        - name: TRINO_SHARED_SECRET
          valueFrom:
            secretKeyRef:
              key: shared-secret
              name: trino-internal-secret
        image:
          pullPolicy: IfNotPresent
          registry: docker.hops.works
          repository: hopsworks/trino
          tag: 480-v10
        initContainers:
          coordinator:
          - command:
            - /bin/sh
            - -c
            - |
              # Never hang and never fail. This is an init container, so it runs before Trino, and a
              # probe that exists to improve an error message must not be able to delay or block the
              # query engine. Both outcomes are swallowed and the line is always printed.
              URL='{{ .Values.global._hopsworks.trino.egressProbe.echoUrl }}'
              if [ -z "$URL" ]; then
                echo "trino-egress-address=disabled"
                exit 0
              fi
              echo "trino-egress-address=$(curl -s --max-time 5 "$URL" || echo unknown)"
            image: '{{ .Values.image.registry }}/{{ .Values.image.repository }}:{{ .Values.image.tag }}'
            imagePullPolicy: IfNotPresent
            name: egress-probe
            resources:
              limits:
                cpu: 500m
                memory: 256Mi
              requests:
                cpu: 10m
                memory: 32Mi
            securityContext:
              allowPrivilegeEscalation: false
              capabilities:
                drop:
                - ALL
          - command:
            - sh
            - -c
            - cat /srv/hops/super_crypto/trino/trino_priv.pem /srv/hops/super_crypto/trino/trino_certificate_bundle.pem > /certs/keystore.pem
            image: '{{ .Values.image.registry }}/hopsworks/hwutils:{{ .Values.global._hopsworks.toolbox.tag }}'
            imagePullPolicy: IfNotPresent
            name: init-coordinator-cert
            resources:
              limits:
                cpu: 500m
                memory: 256Mi
              requests:
                cpu: 50m
                memory: 64Mi
            securityContext:
              allowPrivilegeEscalation: false
              capabilities:
                drop:
                - ALL
            volumeMounts:
            - mountPath: /certs
              name: certs
            - mountPath: /srv/hops/super_crypto/trino
              name: super-crypto-kstore
          - command:
            - /bin/bash
            - -c
            - |
              set -euo pipefail
              export HADOOP_CONF_DIR=/etc/hadoop
              CERTS=/srv/hops/super_crypto/trino
              mkdir -p {{ .Values.global._hopsworks.trino.mountableSecrets.mountPath }} /tmp/.hopsfs-mount-staging
              # Foreground: this is a sidecar, it must not exit. No startupProbe gates Trino on the
              # mount, deliberately: a mount that never comes up must not keep the query engine down.
              # A catalog whose bundle is missing fails its own connection instead.
              exec hopsfs-mount \
                --logLevel warning \
                --stageDir /tmp/.hopsfs-mount-staging \
                --readOnly \
                --srcDir {{ .Values.global._hopsworks.trino.mountableSecrets.storeRoot }} \
                --hopsFSUserName trino \
                -allowOther=true \
                -tls \
                -rootCABundle "$CERTS/hops_root_ca.pem" \
                -clientCertificate "$CERTS/trino_certificate_bundle.pem" \
                -clientKey "$CERTS/trino_priv.pem" \
                namenode.service.{{ .Values.global._hopsworks.consulDomainName | default "consul" }}:8020 \
                {{ .Values.global._hopsworks.trino.mountableSecrets.mountPath }}
            image: '{{ $img := printf "%s/%s:%s" .Values.image.registry .Values.global._hopsworks.trino.mountableSecrets.image.repository .Values.global._hopsworks.trino.mountableSecrets.image.tag }}{{ $img }}{{ include "hopsworkslib.imageDigest" (dict "global" .Values.global "entry" $img) }}'
            imagePullPolicy: IfNotPresent
            lifecycle:
              preStop:
                exec:
                  command:
                  - /bin/bash
                  - -c
                  - umount -l {{ .Values.global._hopsworks.trino.mountableSecrets.mountPath }} || true
            name: mountable-secrets
            resources:
              limits:
                cpu: 500m
                memory: 512Mi
              requests:
                cpu: 100m
                memory: 128Mi
            restartPolicy: Always
            securityContext:
              privileged: true
              runAsGroup: 0
              runAsNonRoot: false
              runAsUser: 0
            volumeMounts:
            - mountPath: '{{ .Values.global._hopsworks.trino.mountableSecrets.mountPath }}'
              mountPropagation: Bidirectional
              name: mountable-secrets
            - mountPath: /srv/hops/super_crypto/trino
              name: super-crypto-kstore
            - mountPath: /etc/hadoop/core-site.xml
              name: core-site
              subPath: core-site.xml
            - mountPath: /etc/hadoop/hdfs-site.xml
              name: hdfs-site
              subPath: hdfs-site.xml
        nameOverride: hopsworks-trino-test
        securityContext:
          runAsGroup: 1000
          runAsNonRoot: true
          runAsUser: 1000
          seccompProfile:
            type: RuntimeDefault
        server:
          config:
            authenticationType: PASSWORD
            https:
              enabled: true
              keystore:
                path: /certs/keystore.pem
              port: 8443
          workers: 0
        service:
          type: ClusterIP
        serviceAccount:
          annotations: {}
          create: true
          name: hopsworks-trino-test
        workerNameOverride: hopsworks-trino-test-worker
    ```

<div class="hops-values" markdown>

`trino` <a class="headerlink" href="#helm.trino" title="Permanent link">#</a> { #helm.trino }
:   Type `object`, default `{}`.
    override  trino values

`trino.catalogsConfigmapName` <a class="headerlink" href="#helm.trino.catalogsConfigmapName" title="Permanent link">#</a> { #helm.trino.catalogsConfigmapName }
:   Type `string`, default `"hopsworks-trino-catalogs"`.

`trino.hopsworkslib` <a class="headerlink" href="#helm.trino.hopsworkslib" title="Permanent link">#</a> { #helm.trino.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`trino.trinotest` <a class="headerlink" href="#helm.trino.trinotest" title="Permanent link">#</a> { #helm.trino.trinotest }
:   Type `object`, passed to the [`trino` 1.41.0](https://artifacthub.io/packages/helm/trino/trino/1.41.0) chart, whose other values are documented there.
    override trinotest values. Rendered only when global._hopsworks.trino.testCoordinator.enabled is true (see Chart.yaml). An optional single-node coordinator running catalog.management=dynamic with a WRITABLE catalog dir, used by the backend to connection-test user catalogs (CREATE CATALOG / SHOW SCHEMAS / DROP CATALOG) before they are synced to the production coordinator. Mirrors the production coordinator's image, certs, TLS, and PASSWORD auth so the backend's admin credentials and discovery work identically.

    ??? note "Default"

        ```yaml
        accessControl:
          configFile: rules.json
          refreshPeriod: 10s
          rules:
            rules.json: |-
              {
                "catalogs": [
                  {
                    "group": "admin",
                    "catalog": ".*",
                    "allow": "owner"
                  },
                  {
                    "catalog": "system",
                    "allow": "none"
                  }
                ],
                "schemas": [
                  {
                    "group": "admin",
                    "schema": ".*",
                    "owner": true
                  }
                ],
                "tables": [
                  {
                    "group": "admin",
                    "privileges": [
                      "SELECT",
                      "INSERT",
                      "DELETE",
                      "UPDATE",
                      "OWNERSHIP"
                    ]
                  }
                ],
                "queries": [
                  {
                    "group": "admin",
                    "allow": ["execute", "kill", "view"]
                  }
                ]
              }
          type: configmap
        additionalCatalogs: {}
        additionalConfigProperties:
        - internal-communication.shared-secret=${ENV:TRINO_SHARED_SECRET}
        - http-server.process-forwarded=true
        - catalog.management=dynamic
        auth:
          groupsAuthSecret: trino-groups-file
          passwordAuthSecret: trino-password-file
          refreshPeriod: 5s
        catalogs: []
        coordinator:
          additionalJVMConfig:
          - --add-opens=java.base/java.nio=ALL-UNNAMED
          additionalVolumeMounts:
          - mountPath: /certs
            name: certs
            readOnly: true
          - mountPath: /etc/trino/catalog
            name: catalog-volume
          - mountPath: /opt/hopsworks/mounts
            mountPropagation: HostToContainer
            name: mountable-secrets
            readOnly: true
          additionalVolumes:
          - emptyDir: {}
            name: certs
          - emptyDir: {}
            name: catalog-volume
          - emptyDir: {}
            name: mountable-secrets
          config:
            nodeScheduler:
              includeCoordinator: true
          configMounts:
          - configMap: hopsfs-config
            name: hdfs-site
            path: /etc/hadoop/hdfs-site.xml
            subPath: hdfs-site.xml
          - configMap: hopsfs-config
            name: core-site
            path: /etc/hadoop/core-site.xml
            subPath: core-site.xml
          secretMounts:
          - name: super-crypto-kstore
            path: /srv/hops/super_crypto/trino
            secretName: hopsworks-trino-test-crypto-material
        coordinatorNameOverride: hopsworks-trino-test-coordinator
        env:
        - name: SSL_CERT_KEY_PASSWORD
          valueFrom:
            secretKeyRef:
              key: trino__passwd
              name: hopsworks-trino-test-crypto-material
        - name: TRINO_SHARED_SECRET
          valueFrom:
            secretKeyRef:
              key: shared-secret
              name: trino-internal-secret
        image:
          pullPolicy: IfNotPresent
          registry: docker.hops.works
          repository: hopsworks/trino
          tag: 480-v10
        initContainers:
          coordinator:
          - command:
            - /bin/sh
            - -c
            - |
              # Never hang and never fail. This is an init container, so it runs before Trino, and a
              # probe that exists to improve an error message must not be able to delay or block the
              # query engine. Both outcomes are swallowed and the line is always printed.
              URL='{{ .Values.global._hopsworks.trino.egressProbe.echoUrl }}'
              if [ -z "$URL" ]; then
                echo "trino-egress-address=disabled"
                exit 0
              fi
              echo "trino-egress-address=$(curl -s --max-time 5 "$URL" || echo unknown)"
            image: '{{ .Values.image.registry }}/{{ .Values.image.repository }}:{{ .Values.image.tag }}'
            imagePullPolicy: IfNotPresent
            name: egress-probe
            resources:
              limits:
                cpu: 500m
                memory: 256Mi
              requests:
                cpu: 10m
                memory: 32Mi
            securityContext:
              allowPrivilegeEscalation: false
              capabilities:
                drop:
                - ALL
          - command:
            - sh
            - -c
            - cat /srv/hops/super_crypto/trino/trino_priv.pem /srv/hops/super_crypto/trino/trino_certificate_bundle.pem > /certs/keystore.pem
            image: '{{ .Values.image.registry }}/hopsworks/hwutils:{{ .Values.global._hopsworks.toolbox.tag }}'
            imagePullPolicy: IfNotPresent
            name: init-coordinator-cert
            resources:
              limits:
                cpu: 500m
                memory: 256Mi
              requests:
                cpu: 50m
                memory: 64Mi
            securityContext:
              allowPrivilegeEscalation: false
              capabilities:
                drop:
                - ALL
            volumeMounts:
            - mountPath: /certs
              name: certs
            - mountPath: /srv/hops/super_crypto/trino
              name: super-crypto-kstore
          - command:
            - /bin/bash
            - -c
            - |
              set -euo pipefail
              export HADOOP_CONF_DIR=/etc/hadoop
              CERTS=/srv/hops/super_crypto/trino
              mkdir -p {{ .Values.global._hopsworks.trino.mountableSecrets.mountPath }} /tmp/.hopsfs-mount-staging
              # Foreground: this is a sidecar, it must not exit. No startupProbe gates Trino on the
              # mount, deliberately: a mount that never comes up must not keep the query engine down.
              # A catalog whose bundle is missing fails its own connection instead.
              exec hopsfs-mount \
                --logLevel warning \
                --stageDir /tmp/.hopsfs-mount-staging \
                --readOnly \
                --srcDir {{ .Values.global._hopsworks.trino.mountableSecrets.storeRoot }} \
                --hopsFSUserName trino \
                -allowOther=true \
                -tls \
                -rootCABundle "$CERTS/hops_root_ca.pem" \
                -clientCertificate "$CERTS/trino_certificate_bundle.pem" \
                -clientKey "$CERTS/trino_priv.pem" \
                namenode.service.{{ .Values.global._hopsworks.consulDomainName | default "consul" }}:8020 \
                {{ .Values.global._hopsworks.trino.mountableSecrets.mountPath }}
            image: '{{ $img := printf "%s/%s:%s" .Values.image.registry .Values.global._hopsworks.trino.mountableSecrets.image.repository .Values.global._hopsworks.trino.mountableSecrets.image.tag }}{{ $img }}{{ include "hopsworkslib.imageDigest" (dict "global" .Values.global "entry" $img) }}'
            imagePullPolicy: IfNotPresent
            lifecycle:
              preStop:
                exec:
                  command:
                  - /bin/bash
                  - -c
                  - umount -l {{ .Values.global._hopsworks.trino.mountableSecrets.mountPath }} || true
            name: mountable-secrets
            resources:
              limits:
                cpu: 500m
                memory: 512Mi
              requests:
                cpu: 100m
                memory: 128Mi
            restartPolicy: Always
            securityContext:
              privileged: true
              runAsGroup: 0
              runAsNonRoot: false
              runAsUser: 0
            volumeMounts:
            - mountPath: '{{ .Values.global._hopsworks.trino.mountableSecrets.mountPath }}'
              mountPropagation: Bidirectional
              name: mountable-secrets
            - mountPath: /srv/hops/super_crypto/trino
              name: super-crypto-kstore
            - mountPath: /etc/hadoop/core-site.xml
              name: core-site
              subPath: core-site.xml
            - mountPath: /etc/hadoop/hdfs-site.xml
              name: hdfs-site
              subPath: hdfs-site.xml
        nameOverride: hopsworks-trino-test
        securityContext:
          runAsGroup: 1000
          runAsNonRoot: true
          runAsUser: 1000
          seccompProfile:
            type: RuntimeDefault
        server:
          config:
            authenticationType: PASSWORD
            https:
              enabled: true
              keystore:
                path: /certs/keystore.pem
              port: 8443
          workers: 0
        service:
          type: ClusterIP
        serviceAccount:
          annotations: {}
          create: true
          name: hopsworks-trino-test
        workerNameOverride: hopsworks-trino-test-worker
        ```

`trino.trinotest.initContainers.coordinator[2].name` <a class="headerlink" href="#helm.trino.trinotest.initContainers.coordinator.2.name" title="Permanent link">#</a> { #helm.trino.trinotest.initContainers.coordinator.2.name }
:   Type `string`, default `"mountable-secrets"`.
    readOnly is not optional. Without it the query engine gains a write channel into HopsFS as the trino service user. --srcDir bounds what the mount exposes to the backend-owned tree; the mount authenticates as trino, which is in the hdfs superuser group, so srcDir is the only thing containing it.  The preStop unmount is also not optional. Without it the container cannot terminate, the pod ends 0/2 Error, `kubectl delete pod` hangs, and force-deleting leaks fuse.hopsfs mounts onto the node that must then be cleared by hand with nsenter.

</div>

## auth { #helm-values-trino-auth }

??? example "Defaults as YAML"

    ```yaml
    trino:
      auth:
        adminUserPwd: Tr1n0_Admin_ChangeMe_!2345
        adminUserPwdHash: $2y$10$wu8UEOW.3A9rBautqh98zuwZTxgM85QhS8Mfl8hDKcLazIy0LpWfK
        adminUsername: trino
        createSecrets: true
        createSharedSecret: true
        monitoringUser: prometheus
        monitoringUserPwd: Tr1n0_Monitoring_ChangeMe_!2345
        monitoringUserPwdHash: $2y$10$tE7wiYz2XqiIg.E9DlqTfuqBqnQa42cqYog6frsxd5yj5WOH0r802
    ```

<div class="hops-values" markdown>

`trino.auth.adminUserPwd` <a class="headerlink" href="#helm.trino.auth.adminUserPwd" title="Permanent link">#</a> { #helm.trino.auth.adminUserPwd }
:   Type `string`, default `"Tr1n0_Admin_ChangeMe_!2345"`.

`trino.auth.adminUserPwdHash` <a class="headerlink" href="#helm.trino.auth.adminUserPwdHash" title="Permanent link">#</a> { #helm.trino.auth.adminUserPwdHash }
:   Type `string`, default `"$2y$10$wu8UEOW.3A9rBautqh98zuwZTxgM85QhS8Mfl8hDKcLazIy0LpWfK"`.

`trino.auth.adminUsername` <a class="headerlink" href="#helm.trino.auth.adminUsername" title="Permanent link">#</a> { #helm.trino.auth.adminUsername }
:   Type `string`, default `"trino"`.
    Trino admin username. Should not be changed. Used in hadoop.proxyuser.trino

`trino.auth.createSecrets` <a class="headerlink" href="#helm.trino.auth.createSecrets" title="Permanent link">#</a> { #helm.trino.auth.createSecrets }
:   Type `bool`, default `true`.
    If createSecrets is false, you must manually create the following Kubernetes Secrets:   1. trino-admin-credentials, plus the password-file and group-file Secrets used by Trino's      password-file authentication. By default, these are named `trino-password-file` and      `trino-groups-file`, but their names are configurable via      `.Values.trino.auth.passwordAuthSecret` and `.Values.trino.auth.groupsAuthSecret`.   2. trino-monitoring-credentials using the monitoring username/password defined below. Passwords stored in the password-file Secret (default: `trino-password-file`) must be securely hashed using bcrypt or PBKDF2. See <https://trino.io/docs/current/security/password-file.html#password-files> for details. When createSecrets is false, add the label `backup.hops.works/include: "true"` to the manually created trino-admin-credentials, trino-monitoring-credentials, password-file and group-file Secrets, otherwise the built-in Velero backup schedule does not capture them and Trino authentication cannot be restored. ArgoCD: the password-file and group-file Secrets are mutated at runtime (Hopsworks writes project users/groups into them). On ArgoCD-managed installs, and required when automated selfHeal is enabled, set ignoreDifferences on /data for the four Trino auth Secrets and `RespectIgnoreDifferences=true` in the Application syncPolicy, or ArgoCD will overwrite the runtime-managed data with the chart defaults on every sync. trino-internal-secret is also non-deterministic under ArgoCD: the template falls back to a fresh `randBytes` value whenever the lookup cannot read the existing Secret (every `helm template` / non-auto render), so ArgoCD would rotate it on each sync and churn Trino's internal TLS. It is deliberately excluded from the backup (safely regenerated on a fresh install); if ArgoCD manages it, give it the same ignoreDifferences on /data, or set `createSharedSecret: false` and manage it from an external DR source.

`trino.auth.createSharedSecret` <a class="headerlink" href="#helm.trino.auth.createSharedSecret" title="Permanent link">#</a> { #helm.trino.auth.createSharedSecret }
:   Type `bool`, default `true`.
    If `createSharedSecret` is set to `false`, you must generate an `internal-communication.shared-secret` value and store it in a Kubernetes Secret named `trino-internal-secret` under the key `shared-secret`. trino-internal-secret is intentionally NOT captured by the Velero backup (it has no coupling to user state and is regenerated on a fresh install). With createSharedSecret=false it is operator-managed, so disaster recovery must restore it from an independent source, followed by a coordinated restart of all Trino pods so coordinator and workers share the same value.

`trino.auth.monitoringUser` <a class="headerlink" href="#helm.trino.auth.monitoringUser" title="Permanent link">#</a> { #helm.trino.auth.monitoringUser }
:   Type `string`, default `"prometheus"`.
    Username used by Prometheus for scraping Trino metrics. If you override this value, you MUST also:   1. Update Trino access control to grant this user the required permissions      (e.g. adjust `accessControl.rules.rules.json` accordingly).   2. Update the Prometheus scrape configuration so that the same username is used:      set `.Values.prometheus.prometheus.serverFiles.prometheus.yml.scrape_configs[*].basic_auth.username`      for the scrape job with `job_name: "trino"` to match this value.

`trino.auth.monitoringUserPwd` <a class="headerlink" href="#helm.trino.auth.monitoringUserPwd" title="Permanent link">#</a> { #helm.trino.auth.monitoringUserPwd }
:   Type `string`, default `"Tr1n0_Monitoring_ChangeMe_!2345"`.

`trino.auth.monitoringUserPwdHash` <a class="headerlink" href="#helm.trino.auth.monitoringUserPwdHash" title="Permanent link">#</a> { #helm.trino.auth.monitoringUserPwdHash }
:   Type `string`, default `"$2y$10$tE7wiYz2XqiIg.E9DlqTfuqBqnQa42cqYog6frsxd5yj5WOH0r802"`.

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

`trino.externalLoadBalancer.nodeSelector` <a class="headerlink" href="#helm.trino.externalLoadBalancer.nodeSelector" title="Permanent link">#</a> { #helm.trino.externalLoadBalancer.nodeSelector }
:   Type `object`, default `{}`.
    selector for nodes the load balancer can use to route traffic

</div>

## trino { #helm-values-trino-trino }

??? example "Defaults as YAML"

    ```yaml
    trino:
      trino:
        accessControl:
          configFile: rules.json
          refreshPeriod: 10s
          rules:
            rules.json: |-
              {
                "system_information": [
                  {
                    "user": "prometheus",
                    "allow": ["read"]
                  }
                ],
                "catalogs": [
                  {
                    "group": "admin",
                    "catalog": ".*",
                    "allow": "all"
                  },
                  {
                    "catalog": "tpch",
                    "allow": "read-only"
                  },
                  {
                    "catalog": "tpcds",
                    "allow": "read-only"
                  },
                  {
                    "catalog": "iceberg",
                    "allow": "all"
                  },
                  {
                    "catalog": "delta",
                    "allow": "all"
                  },
                  {
                    "catalog": "hive",
                    "allow": "all"
                  },
                  {
                    "catalog": "hudi",
                    "allow": "all"
                  },
                  {
                    "group": "(.*)__data_owner",
                    "catalog": "$1__.*",
                    "allow": "all"
                  },
                  {
                    "group": "(.*)__data_scientist",
                    "catalog": "$1__.*",
                    "allow": "read-only"
                  },
                  {
                    "group": "(.*)__shared__(.*)",
                    "catalog": "$1__$2",
                    "allow": "read-only"
                  },
                  {
                    "catalog": "system",
                    "allow": "read-only"
                  }
                ],
                "schemas": [
                  {
                    "group": "admin",
                    "schema": ".*",
                    "owner": true
                  },
                  {
                    "group": "(.*)__data_owner",
                    "schema": "($1|$1_featurestore)",
                    "owner": true
                  },
                  {
                    "group": "(.*)__data_owner",
                    "catalog": "$1__.*",
                    "schema": ".*",
                    "owner": true
                  }
                ],
                "tables": [
                  {
                    "group": "admin",
                    "privileges": [
                      "SELECT",
                      "INSERT",
                      "DELETE",
                      "UPDATE",
                      "OWNERSHIP",
                      "GRANT_SELECT"
                    ]
                  },
                  {
                    "group": "(.*)__data_owner",
                    "schema": "($1|$1_featurestore)",
                    "privileges": ["SELECT", "INSERT", "DELETE", "UPDATE", "OWNERSHIP"]
                  },
                  {
                    "group": "(.*)__data_owner",
                    "catalog": "$1__.*",
                    "schema": ".*",
                    "privileges": ["SELECT", "INSERT", "DELETE", "UPDATE", "OWNERSHIP"]
                  },
                  {
                    "group": "(.*)__data_scientist",
                    "schema": "($1|$1_featurestore)",
                    "privileges": ["SELECT"]
                  },
                  {
                    "group": "(.*)__data_scientist",
                    "catalog": "$1__.*",
                    "schema": ".*",
                    "privileges": ["SELECT"]
                  },
                  {
                    "group": "(.*)__shared_hivedb",
                    "schema": "$1",
                    "privileges": ["SELECT"]
                  },
                  {
                    "group": "(.*)__shared_featurestore",
                    "schema": "$1_featurestore",
                    "privileges": ["SELECT"]
                  },
                  {
                    "catalog": "tpch",
                    "privileges": ["SELECT"]
                  },
                  {
                    "catalog": "tpcds",
                    "privileges": ["SELECT"]
                  },
                  {
                    "catalog": "system",
                    "schema": "metadata",
                    "privileges": ["SELECT"]
                  }
                ],
                "queries": [
                  {
                    "group": "admin",
                    "allow": ["execute", "kill", "view"]
                  },
                  {
                    "group": "(.*)__data_owner",
                    "queryOwner": "$1__.*",
                    "allow": ["kill", "view"]
                  },
                  {
                    "user": "(.*)__.*",
                    "queryOwner": "$1__.*",
                    "allow": ["view"]
                  },
                  {
                    "allow": ["execute"]
                  }
                ]
              }
          type: configmap
        additionalCatalogs: {}
        additionalConfigProperties:
        - internal-communication.shared-secret=${ENV:TRINO_SHARED_SECRET}
        - http-server.process-forwarded=true
        - event-listener.config-files=etc/mysql-event-listener.properties
        auth:
          groupsAuthSecret: trino-groups-file
          passwordAuthSecret: trino-password-file
          refreshPeriod: 5s
        catalogs: []
        configMounts: []
        coordinator:
          additionalConfigFiles:
            mysql-event-listener.properties: |
              event-listener.name=mysql
              mysql-event-listener.db.url={{ include "trino.mysql.eventListener.db.url" . }}
          additionalJVMConfig:
          - --add-opens=java.base/java.nio=ALL-UNNAMED
          additionalVolumeMounts:
          - mountPath: /certs
            name: certs
            readOnly: true
          - mountPath: /opt/hopsworks/mounts
            mountPropagation: HostToContainer
            name: mountable-secrets
            readOnly: true
          - mountPath: /etc/trino/catalog
            name: catalog-volume
          additionalVolumes:
          - emptyDir: {}
            name: certs
          - emptyDir: {}
            name: mountable-secrets
          - name: catalog-volume
            projected:
              sources:
              - configMap:
                  name: hopsworks-trino-catalogs
              - secret:
                  name: hopsworks-trino-catalogs-user-0
                  optional: true
              - secret:
                  name: hopsworks-trino-catalogs-user-1
                  optional: true
          configMounts:
          - configMap: hopsfs-config
            name: hdfs-site
            path: /etc/hadoop/hdfs-site.xml
            subPath: hdfs-site.xml
          - configMap: hopsfs-config
            name: core-site
            path: /etc/hadoop/core-site.xml
            subPath: core-site.xml
          secretMounts:
          - name: super-crypto-kstore
            path: /srv/hops/super_crypto/trino
            secretName: hopsworks-trino-crypto-material
        coordinatorNameOverride: hopsworks-trino-coordinator
        defaultCatalogs:
          delta.properties: |
            connector.name=delta_lake
            fs.hadoop.enabled=true
            hive.config.resources=/etc/hadoop/hdfs-site.xml,/etc/hadoop/core-site.xml
            hive.metastore.username=trino
            hive.metastore.uri=thrift://{{ include "trino.consul.hiveMetastoreAddress" . }}
            hive.metastore.thrift.client.ssl.enabled=true
            hive.metastore.thrift.client.ssl.key=/srv/hops/super_crypto/trino/trino__kstore.jks
            hive.metastore.thrift.client.ssl.key-password=${ENV:SSL_CERT_KEY_PASSWORD}
            hive.metastore.thrift.client.ssl.trust-certificate=/srv/hops/super_crypto/trino/trino__tstore.jks
            hive.metastore.thrift.client.ssl.trust-certificate-password=${ENV:SSL_CERT_KEY_PASSWORD}
            hive.hdfs.impersonation.enabled=true
            delta.enable-non-concurrent-writes=true
          hive.properties: |
            connector.name=hive
            fs.hadoop.enabled=true
            hive.config.resources=/etc/hadoop/hdfs-site.xml,/etc/hadoop/core-site.xml
            hive.metastore.username=trino
            hive.metastore.uri=thrift://{{ include "trino.consul.hiveMetastoreAddress" . }}
            hive.metastore.thrift.client.ssl.enabled=true
            hive.metastore.thrift.client.ssl.key=/srv/hops/super_crypto/trino/trino__kstore.jks
            hive.metastore.thrift.client.ssl.key-password=${ENV:SSL_CERT_KEY_PASSWORD}
            hive.metastore.thrift.client.ssl.trust-certificate=/srv/hops/super_crypto/trino/trino__tstore.jks
            hive.metastore.thrift.client.ssl.trust-certificate-password=${ENV:SSL_CERT_KEY_PASSWORD}
            hive.hdfs.impersonation.enabled=true
          hudi.properties: |
            connector.name=hudi
            fs.hadoop.enabled=true
            hive.config.resources=/etc/hadoop/hdfs-site.xml,/etc/hadoop/core-site.xml
            hive.metastore.username=trino
            hive.metastore.uri=thrift://{{ include "trino.consul.hiveMetastoreAddress" . }}
            hive.metastore.thrift.client.ssl.enabled=true
            hive.metastore.thrift.client.ssl.key=/srv/hops/super_crypto/trino/trino__kstore.jks
            hive.metastore.thrift.client.ssl.key-password=${ENV:SSL_CERT_KEY_PASSWORD}
            hive.metastore.thrift.client.ssl.trust-certificate=/srv/hops/super_crypto/trino/trino__tstore.jks
            hive.metastore.thrift.client.ssl.trust-certificate-password=${ENV:SSL_CERT_KEY_PASSWORD}
            hive.hdfs.impersonation.enabled=true
          iceberg.properties: |
            connector.name=iceberg
            fs.hadoop.enabled=true
            hive.config.resources=/etc/hadoop/hdfs-site.xml,/etc/hadoop/core-site.xml
            hive.metastore.username=trino
            hive.metastore.uri=thrift://{{ include "trino.consul.hiveMetastoreAddress" . }}
            hive.metastore.thrift.client.ssl.enabled=true
            hive.metastore.thrift.client.ssl.key=/srv/hops/super_crypto/trino/trino__kstore.jks
            hive.metastore.thrift.client.ssl.key-password=${ENV:SSL_CERT_KEY_PASSWORD}
            hive.metastore.thrift.client.ssl.trust-certificate=/srv/hops/super_crypto/trino/trino__tstore.jks
            hive.metastore.thrift.client.ssl.trust-certificate-password=${ENV:SSL_CERT_KEY_PASSWORD}
            iceberg.catalog.type=hive_metastore
            iceberg.file-format=PARQUET
            iceberg.compression-codec=ZSTD
            iceberg.hive-catalog.locking-enabled=false
            hive.hdfs.impersonation.enabled=true
        env:
        - name: SSL_CERT_KEY_PASSWORD
          valueFrom:
            secretKeyRef:
              key: trino__passwd
              name: hopsworks-trino-crypto-material
        - name: HOPS_USE_LOGIN_USER
          value: 'true'
        - name: TRINO_SHARED_SECRET
          valueFrom:
            secretKeyRef:
              key: shared-secret
              name: trino-internal-secret
        - name: MYSQL_DB
          value: hopsworks
        - name: MYSQL_USER
          value: hopsworksroot
        - name: MYSQL_PASSWORD
          valueFrom:
            secretKeyRef:
              key: hopsworksroot
              name: mysql-users-secrets
        envFrom:
        - configMapRef:
            name: '{{ .Values.nameOverride }}-mysql-conn-env'
        eventListenerProperties: []
        image:
          pullPolicy: IfNotPresent
          registry: docker.hops.works
          repository: hopsworks/trino
          tag: 480-v10
        initContainers:
          coordinator:
          - command:
            - /bin/sh
            - -c
            - |
              # Never hang and never fail. This is an init container, so it runs before Trino, and a
              # probe that exists to improve an error message must not be able to delay or block the
              # query engine. Both outcomes are swallowed and the line is always printed.
              URL='{{ .Values.global._hopsworks.trino.egressProbe.echoUrl }}'
              if [ -z "$URL" ]; then
                echo "trino-egress-address=disabled"
                exit 0
              fi
              echo "trino-egress-address=$(curl -s --max-time 5 "$URL" || echo unknown)"
            image: '{{ .Values.image.registry }}/{{ .Values.image.repository }}:{{ .Values.image.tag }}'
            imagePullPolicy: IfNotPresent
            name: egress-probe
            resources:
              limits:
                cpu: 500m
                memory: 256Mi
              requests:
                cpu: 10m
                memory: 32Mi
            securityContext:
              allowPrivilegeEscalation: false
              capabilities:
                drop:
                - ALL
          - command:
            - sh
            - -c
            - cat /srv/hops/super_crypto/trino/trino_priv.pem /srv/hops/super_crypto/trino/trino_certificate_bundle.pem > /certs/keystore.pem
            image: '{{ .Values.image.registry }}/hopsworks/hwutils:{{ .Values.global._hopsworks.toolbox.tag }}'
            imagePullPolicy: IfNotPresent
            name: init-coordinator-cert
            resources:
              limits:
                cpu: 500m
                memory: 256Mi
              requests:
                cpu: 50m
                memory: 64Mi
            securityContext:
              allowPrivilegeEscalation: false
              capabilities:
                drop:
                - ALL
            volumeMounts:
            - mountPath: /certs
              name: certs
            - mountPath: /srv/hops/super_crypto/trino
              name: super-crypto-kstore
          - command:
            - /bin/bash
            - -c
            - |
              set -euo pipefail
              export HADOOP_CONF_DIR=/etc/hadoop
              CERTS=/srv/hops/super_crypto/trino
              mkdir -p {{ .Values.global._hopsworks.trino.mountableSecrets.mountPath }} /tmp/.hopsfs-mount-staging
              # Foreground: this is a sidecar, it must not exit. No startupProbe gates Trino on the
              # mount, deliberately: a mount that never comes up must not keep the query engine down.
              # A catalog whose bundle is missing fails its own connection instead.
              exec hopsfs-mount \
                --logLevel warning \
                --stageDir /tmp/.hopsfs-mount-staging \
                --readOnly \
                --srcDir {{ .Values.global._hopsworks.trino.mountableSecrets.storeRoot }} \
                --hopsFSUserName trino \
                -allowOther=true \
                -tls \
                -rootCABundle "$CERTS/hops_root_ca.pem" \
                -clientCertificate "$CERTS/trino_certificate_bundle.pem" \
                -clientKey "$CERTS/trino_priv.pem" \
                namenode.service.{{ .Values.global._hopsworks.consulDomainName | default "consul" }}:8020 \
                {{ .Values.global._hopsworks.trino.mountableSecrets.mountPath }}
            image: '{{ $img := printf "%s/%s:%s" .Values.image.registry .Values.global._hopsworks.trino.mountableSecrets.image.repository .Values.global._hopsworks.trino.mountableSecrets.image.tag }}{{ $img }}{{ include "hopsworkslib.imageDigest" (dict "global" .Values.global "entry" $img) }}'
            imagePullPolicy: IfNotPresent
            lifecycle:
              preStop:
                exec:
                  command:
                  - /bin/bash
                  - -c
                  - umount -l {{ .Values.global._hopsworks.trino.mountableSecrets.mountPath }} || true
            name: mountable-secrets
            resources:
              limits:
                cpu: 500m
                memory: 512Mi
              requests:
                cpu: 100m
                memory: 128Mi
            restartPolicy: Always
            securityContext:
              privileged: true
              runAsGroup: 0
              runAsNonRoot: false
              runAsUser: 0
            volumeMounts:
            - mountPath: '{{ .Values.global._hopsworks.trino.mountableSecrets.mountPath }}'
              mountPropagation: Bidirectional
              name: mountable-secrets
            - mountPath: /srv/hops/super_crypto/trino
              name: super-crypto-kstore
            - mountPath: /etc/hadoop/core-site.xml
              name: core-site
              subPath: core-site.xml
            - mountPath: /etc/hadoop/hdfs-site.xml
              name: hdfs-site
              subPath: hdfs-site.xml
          worker:
          - command:
            - /bin/sh
            - -c
            - |
              # Never hang and never fail. This is an init container, so it runs before Trino, and a
              # probe that exists to improve an error message must not be able to delay or block the
              # query engine. Both outcomes are swallowed and the line is always printed.
              URL='{{ .Values.global._hopsworks.trino.egressProbe.echoUrl }}'
              if [ -z "$URL" ]; then
                echo "trino-egress-address=disabled"
                exit 0
              fi
              echo "trino-egress-address=$(curl -s --max-time 5 "$URL" || echo unknown)"
            image: '{{ .Values.image.registry }}/{{ .Values.image.repository }}:{{ .Values.image.tag }}'
            imagePullPolicy: IfNotPresent
            name: egress-probe
            resources:
              limits:
                cpu: 500m
                memory: 256Mi
              requests:
                cpu: 10m
                memory: 32Mi
            securityContext:
              allowPrivilegeEscalation: false
              capabilities:
                drop:
                - ALL
          - command:
            - /bin/bash
            - -c
            - |
              set -euo pipefail
              export HADOOP_CONF_DIR=/etc/hadoop
              CERTS=/srv/hops/super_crypto/trino
              mkdir -p {{ .Values.global._hopsworks.trino.mountableSecrets.mountPath }} /tmp/.hopsfs-mount-staging
              # Foreground: this is a sidecar, it must not exit. No startupProbe gates Trino on the
              # mount, deliberately: a mount that never comes up must not keep the query engine down.
              # A catalog whose bundle is missing fails its own connection instead.
              exec hopsfs-mount \
                --logLevel warning \
                --stageDir /tmp/.hopsfs-mount-staging \
                --readOnly \
                --srcDir {{ .Values.global._hopsworks.trino.mountableSecrets.storeRoot }} \
                --hopsFSUserName trino \
                -allowOther=true \
                -tls \
                -rootCABundle "$CERTS/hops_root_ca.pem" \
                -clientCertificate "$CERTS/trino_certificate_bundle.pem" \
                -clientKey "$CERTS/trino_priv.pem" \
                namenode.service.{{ .Values.global._hopsworks.consulDomainName | default "consul" }}:8020 \
                {{ .Values.global._hopsworks.trino.mountableSecrets.mountPath }}
            image: '{{ $img := printf "%s/%s:%s" .Values.image.registry .Values.global._hopsworks.trino.mountableSecrets.image.repository .Values.global._hopsworks.trino.mountableSecrets.image.tag }}{{ $img }}{{ include "hopsworkslib.imageDigest" (dict "global" .Values.global "entry" $img) }}'
            imagePullPolicy: IfNotPresent
            lifecycle:
              preStop:
                exec:
                  command:
                  - /bin/bash
                  - -c
                  - umount -l {{ .Values.global._hopsworks.trino.mountableSecrets.mountPath }} || true
            name: mountable-secrets
            resources:
              limits:
                cpu: 500m
                memory: 512Mi
              requests:
                cpu: 100m
                memory: 128Mi
            restartPolicy: Always
            securityContext:
              privileged: true
              runAsGroup: 0
              runAsNonRoot: false
              runAsUser: 0
            volumeMounts:
            - mountPath: '{{ .Values.global._hopsworks.trino.mountableSecrets.mountPath }}'
              mountPropagation: Bidirectional
              name: mountable-secrets
            - mountPath: /srv/hops/super_crypto/trino
              name: super-crypto-kstore
            - mountPath: /etc/hadoop/core-site.xml
              name: core-site
              subPath: core-site.xml
            - mountPath: /etc/hadoop/hdfs-site.xml
              name: hdfs-site
              subPath: hdfs-site.xml
        moreCatalogs:
          tpcds.properties: |
            connector.name=tpcds
            tpcds.splits-per-node=4
          tpch.properties: |
            connector.name=tpch
            tpch.splits-per-node=4
        nameOverride: hopsworks-trino
        securityContext:
          runAsGroup: 1000
          runAsNonRoot: true
          runAsUser: 1000
          seccompProfile:
            type: RuntimeDefault
        server:
          config:
            authenticationType: PASSWORD
            https:
              enabled: true
              keystore:
                path: /certs/keystore.pem
              port: 8443
          coordinatorExtraConfig: |
            web-ui.preview.enabled=true
        service:
          coordinator:
            annotations:
              consul.hashicorp.com/service-name: trino
              consul.hashicorp.com/service-port: '8443'
              consul.hashicorp.com/service-tags: coordinator
              prometheus.io/path: /metrics
              prometheus.io/port: '8443'
              prometheus.io/scheme: https
              prometheus.io/scrape: 'true'
          type: ClusterIP
        serviceAccount:
          annotations: {}
          create: true
          name: hopsworks-trino
        worker:
          additionalConfigFiles:
            mysql-event-listener.properties: |
              event-listener.name=mysql
              mysql-event-listener.db.url={{ include "trino.mysql.eventListener.db.url" . }}
          additionalJVMConfig:
          - --add-opens=java.base/java.nio=ALL-UNNAMED
          additionalVolumeMounts:
          - mountPath: /etc/trino/catalog
            name: catalog-volume
          - mountPath: /opt/hopsworks/mounts
            mountPropagation: HostToContainer
            name: mountable-secrets
            readOnly: true
          additionalVolumes:
          - name: catalog-volume
            projected:
              sources:
              - configMap:
                  name: hopsworks-trino-catalogs
              - secret:
                  name: hopsworks-trino-catalogs-user-0
                  optional: true
              - secret:
                  name: hopsworks-trino-catalogs-user-1
                  optional: true
          - emptyDir: {}
            name: mountable-secrets
          configMounts:
          - configMap: hopsfs-config
            name: hdfs-site
            path: /etc/hadoop/hdfs-site.xml
            subPath: hdfs-site.xml
          - configMap: hopsfs-config
            name: core-site
            path: /etc/hadoop/core-site.xml
            subPath: core-site.xml
          secretMounts:
          - name: super-crypto-kstore
            path: /srv/hops/super_crypto/trino
            secretName: hopsworks-trino-crypto-material
        workerNameOverride: hopsworks-trino-worker
    ```

<div class="hops-values" markdown>

`trino.trino` <a class="headerlink" href="#helm.trino.trino" title="Permanent link">#</a> { #helm.trino.trino }
:   Type `object`, passed to the [`trino` 1.41.0](https://artifacthub.io/packages/helm/trino/trino/1.41.0) chart, whose other values are documented there.
    override trino values

    ??? note "Default"

        ```yaml
        accessControl:
          configFile: rules.json
          refreshPeriod: 10s
          rules:
            rules.json: |-
              {
                "system_information": [
                  {
                    "user": "prometheus",
                    "allow": ["read"]
                  }
                ],
                "catalogs": [
                  {
                    "group": "admin",
                    "catalog": ".*",
                    "allow": "all"
                  },
                  {
                    "catalog": "tpch",
                    "allow": "read-only"
                  },
                  {
                    "catalog": "tpcds",
                    "allow": "read-only"
                  },
                  {
                    "catalog": "iceberg",
                    "allow": "all"
                  },
                  {
                    "catalog": "delta",
                    "allow": "all"
                  },
                  {
                    "catalog": "hive",
                    "allow": "all"
                  },
                  {
                    "catalog": "hudi",
                    "allow": "all"
                  },
                  {
                    "group": "(.*)__data_owner",
                    "catalog": "$1__.*",
                    "allow": "all"
                  },
                  {
                    "group": "(.*)__data_scientist",
                    "catalog": "$1__.*",
                    "allow": "read-only"
                  },
                  {
                    "group": "(.*)__shared__(.*)",
                    "catalog": "$1__$2",
                    "allow": "read-only"
                  },
                  {
                    "catalog": "system",
                    "allow": "read-only"
                  }
                ],
                "schemas": [
                  {
                    "group": "admin",
                    "schema": ".*",
                    "owner": true
                  },
                  {
                    "group": "(.*)__data_owner",
                    "schema": "($1|$1_featurestore)",
                    "owner": true
                  },
                  {
                    "group": "(.*)__data_owner",
                    "catalog": "$1__.*",
                    "schema": ".*",
                    "owner": true
                  }
                ],
                "tables": [
                  {
                    "group": "admin",
                    "privileges": [
                      "SELECT",
                      "INSERT",
                      "DELETE",
                      "UPDATE",
                      "OWNERSHIP",
                      "GRANT_SELECT"
                    ]
                  },
                  {
                    "group": "(.*)__data_owner",
                    "schema": "($1|$1_featurestore)",
                    "privileges": ["SELECT", "INSERT", "DELETE", "UPDATE", "OWNERSHIP"]
                  },
                  {
                    "group": "(.*)__data_owner",
                    "catalog": "$1__.*",
                    "schema": ".*",
                    "privileges": ["SELECT", "INSERT", "DELETE", "UPDATE", "OWNERSHIP"]
                  },
                  {
                    "group": "(.*)__data_scientist",
                    "schema": "($1|$1_featurestore)",
                    "privileges": ["SELECT"]
                  },
                  {
                    "group": "(.*)__data_scientist",
                    "catalog": "$1__.*",
                    "schema": ".*",
                    "privileges": ["SELECT"]
                  },
                  {
                    "group": "(.*)__shared_hivedb",
                    "schema": "$1",
                    "privileges": ["SELECT"]
                  },
                  {
                    "group": "(.*)__shared_featurestore",
                    "schema": "$1_featurestore",
                    "privileges": ["SELECT"]
                  },
                  {
                    "catalog": "tpch",
                    "privileges": ["SELECT"]
                  },
                  {
                    "catalog": "tpcds",
                    "privileges": ["SELECT"]
                  },
                  {
                    "catalog": "system",
                    "schema": "metadata",
                    "privileges": ["SELECT"]
                  }
                ],
                "queries": [
                  {
                    "group": "admin",
                    "allow": ["execute", "kill", "view"]
                  },
                  {
                    "group": "(.*)__data_owner",
                    "queryOwner": "$1__.*",
                    "allow": ["kill", "view"]
                  },
                  {
                    "user": "(.*)__.*",
                    "queryOwner": "$1__.*",
                    "allow": ["view"]
                  },
                  {
                    "allow": ["execute"]
                  }
                ]
              }
          type: configmap
        additionalCatalogs: {}
        additionalConfigProperties:
        - internal-communication.shared-secret=${ENV:TRINO_SHARED_SECRET}
        - http-server.process-forwarded=true
        - event-listener.config-files=etc/mysql-event-listener.properties
        auth:
          groupsAuthSecret: trino-groups-file
          passwordAuthSecret: trino-password-file
          refreshPeriod: 5s
        catalogs: []
        configMounts: []
        coordinator:
          additionalConfigFiles:
            mysql-event-listener.properties: |
              event-listener.name=mysql
              mysql-event-listener.db.url={{ include "trino.mysql.eventListener.db.url" . }}
          additionalJVMConfig:
          - --add-opens=java.base/java.nio=ALL-UNNAMED
          additionalVolumeMounts:
          - mountPath: /certs
            name: certs
            readOnly: true
          - mountPath: /opt/hopsworks/mounts
            mountPropagation: HostToContainer
            name: mountable-secrets
            readOnly: true
          - mountPath: /etc/trino/catalog
            name: catalog-volume
          additionalVolumes:
          - emptyDir: {}
            name: certs
          - emptyDir: {}
            name: mountable-secrets
          - name: catalog-volume
            projected:
              sources:
              - configMap:
                  name: hopsworks-trino-catalogs
              - secret:
                  name: hopsworks-trino-catalogs-user-0
                  optional: true
              - secret:
                  name: hopsworks-trino-catalogs-user-1
                  optional: true
          configMounts:
          - configMap: hopsfs-config
            name: hdfs-site
            path: /etc/hadoop/hdfs-site.xml
            subPath: hdfs-site.xml
          - configMap: hopsfs-config
            name: core-site
            path: /etc/hadoop/core-site.xml
            subPath: core-site.xml
          secretMounts:
          - name: super-crypto-kstore
            path: /srv/hops/super_crypto/trino
            secretName: hopsworks-trino-crypto-material
        coordinatorNameOverride: hopsworks-trino-coordinator
        defaultCatalogs:
          delta.properties: |
            connector.name=delta_lake
            fs.hadoop.enabled=true
            hive.config.resources=/etc/hadoop/hdfs-site.xml,/etc/hadoop/core-site.xml
            hive.metastore.username=trino
            hive.metastore.uri=thrift://{{ include "trino.consul.hiveMetastoreAddress" . }}
            hive.metastore.thrift.client.ssl.enabled=true
            hive.metastore.thrift.client.ssl.key=/srv/hops/super_crypto/trino/trino__kstore.jks
            hive.metastore.thrift.client.ssl.key-password=${ENV:SSL_CERT_KEY_PASSWORD}
            hive.metastore.thrift.client.ssl.trust-certificate=/srv/hops/super_crypto/trino/trino__tstore.jks
            hive.metastore.thrift.client.ssl.trust-certificate-password=${ENV:SSL_CERT_KEY_PASSWORD}
            hive.hdfs.impersonation.enabled=true
            delta.enable-non-concurrent-writes=true
          hive.properties: |
            connector.name=hive
            fs.hadoop.enabled=true
            hive.config.resources=/etc/hadoop/hdfs-site.xml,/etc/hadoop/core-site.xml
            hive.metastore.username=trino
            hive.metastore.uri=thrift://{{ include "trino.consul.hiveMetastoreAddress" . }}
            hive.metastore.thrift.client.ssl.enabled=true
            hive.metastore.thrift.client.ssl.key=/srv/hops/super_crypto/trino/trino__kstore.jks
            hive.metastore.thrift.client.ssl.key-password=${ENV:SSL_CERT_KEY_PASSWORD}
            hive.metastore.thrift.client.ssl.trust-certificate=/srv/hops/super_crypto/trino/trino__tstore.jks
            hive.metastore.thrift.client.ssl.trust-certificate-password=${ENV:SSL_CERT_KEY_PASSWORD}
            hive.hdfs.impersonation.enabled=true
          hudi.properties: |
            connector.name=hudi
            fs.hadoop.enabled=true
            hive.config.resources=/etc/hadoop/hdfs-site.xml,/etc/hadoop/core-site.xml
            hive.metastore.username=trino
            hive.metastore.uri=thrift://{{ include "trino.consul.hiveMetastoreAddress" . }}
            hive.metastore.thrift.client.ssl.enabled=true
            hive.metastore.thrift.client.ssl.key=/srv/hops/super_crypto/trino/trino__kstore.jks
            hive.metastore.thrift.client.ssl.key-password=${ENV:SSL_CERT_KEY_PASSWORD}
            hive.metastore.thrift.client.ssl.trust-certificate=/srv/hops/super_crypto/trino/trino__tstore.jks
            hive.metastore.thrift.client.ssl.trust-certificate-password=${ENV:SSL_CERT_KEY_PASSWORD}
            hive.hdfs.impersonation.enabled=true
          iceberg.properties: |
            connector.name=iceberg
            fs.hadoop.enabled=true
            hive.config.resources=/etc/hadoop/hdfs-site.xml,/etc/hadoop/core-site.xml
            hive.metastore.username=trino
            hive.metastore.uri=thrift://{{ include "trino.consul.hiveMetastoreAddress" . }}
            hive.metastore.thrift.client.ssl.enabled=true
            hive.metastore.thrift.client.ssl.key=/srv/hops/super_crypto/trino/trino__kstore.jks
            hive.metastore.thrift.client.ssl.key-password=${ENV:SSL_CERT_KEY_PASSWORD}
            hive.metastore.thrift.client.ssl.trust-certificate=/srv/hops/super_crypto/trino/trino__tstore.jks
            hive.metastore.thrift.client.ssl.trust-certificate-password=${ENV:SSL_CERT_KEY_PASSWORD}
            iceberg.catalog.type=hive_metastore
            iceberg.file-format=PARQUET
            iceberg.compression-codec=ZSTD
            iceberg.hive-catalog.locking-enabled=false
            hive.hdfs.impersonation.enabled=true
        env:
        - name: SSL_CERT_KEY_PASSWORD
          valueFrom:
            secretKeyRef:
              key: trino__passwd
              name: hopsworks-trino-crypto-material
        - name: HOPS_USE_LOGIN_USER
          value: 'true'
        - name: TRINO_SHARED_SECRET
          valueFrom:
            secretKeyRef:
              key: shared-secret
              name: trino-internal-secret
        - name: MYSQL_DB
          value: hopsworks
        - name: MYSQL_USER
          value: hopsworksroot
        - name: MYSQL_PASSWORD
          valueFrom:
            secretKeyRef:
              key: hopsworksroot
              name: mysql-users-secrets
        envFrom:
        - configMapRef:
            name: '{{ .Values.nameOverride }}-mysql-conn-env'
        eventListenerProperties: []
        image:
          pullPolicy: IfNotPresent
          registry: docker.hops.works
          repository: hopsworks/trino
          tag: 480-v10
        initContainers:
          coordinator:
          - command:
            - /bin/sh
            - -c
            - |
              # Never hang and never fail. This is an init container, so it runs before Trino, and a
              # probe that exists to improve an error message must not be able to delay or block the
              # query engine. Both outcomes are swallowed and the line is always printed.
              URL='{{ .Values.global._hopsworks.trino.egressProbe.echoUrl }}'
              if [ -z "$URL" ]; then
                echo "trino-egress-address=disabled"
                exit 0
              fi
              echo "trino-egress-address=$(curl -s --max-time 5 "$URL" || echo unknown)"
            image: '{{ .Values.image.registry }}/{{ .Values.image.repository }}:{{ .Values.image.tag }}'
            imagePullPolicy: IfNotPresent
            name: egress-probe
            resources:
              limits:
                cpu: 500m
                memory: 256Mi
              requests:
                cpu: 10m
                memory: 32Mi
            securityContext:
              allowPrivilegeEscalation: false
              capabilities:
                drop:
                - ALL
          - command:
            - sh
            - -c
            - cat /srv/hops/super_crypto/trino/trino_priv.pem /srv/hops/super_crypto/trino/trino_certificate_bundle.pem > /certs/keystore.pem
            image: '{{ .Values.image.registry }}/hopsworks/hwutils:{{ .Values.global._hopsworks.toolbox.tag }}'
            imagePullPolicy: IfNotPresent
            name: init-coordinator-cert
            resources:
              limits:
                cpu: 500m
                memory: 256Mi
              requests:
                cpu: 50m
                memory: 64Mi
            securityContext:
              allowPrivilegeEscalation: false
              capabilities:
                drop:
                - ALL
            volumeMounts:
            - mountPath: /certs
              name: certs
            - mountPath: /srv/hops/super_crypto/trino
              name: super-crypto-kstore
          - command:
            - /bin/bash
            - -c
            - |
              set -euo pipefail
              export HADOOP_CONF_DIR=/etc/hadoop
              CERTS=/srv/hops/super_crypto/trino
              mkdir -p {{ .Values.global._hopsworks.trino.mountableSecrets.mountPath }} /tmp/.hopsfs-mount-staging
              # Foreground: this is a sidecar, it must not exit. No startupProbe gates Trino on the
              # mount, deliberately: a mount that never comes up must not keep the query engine down.
              # A catalog whose bundle is missing fails its own connection instead.
              exec hopsfs-mount \
                --logLevel warning \
                --stageDir /tmp/.hopsfs-mount-staging \
                --readOnly \
                --srcDir {{ .Values.global._hopsworks.trino.mountableSecrets.storeRoot }} \
                --hopsFSUserName trino \
                -allowOther=true \
                -tls \
                -rootCABundle "$CERTS/hops_root_ca.pem" \
                -clientCertificate "$CERTS/trino_certificate_bundle.pem" \
                -clientKey "$CERTS/trino_priv.pem" \
                namenode.service.{{ .Values.global._hopsworks.consulDomainName | default "consul" }}:8020 \
                {{ .Values.global._hopsworks.trino.mountableSecrets.mountPath }}
            image: '{{ $img := printf "%s/%s:%s" .Values.image.registry .Values.global._hopsworks.trino.mountableSecrets.image.repository .Values.global._hopsworks.trino.mountableSecrets.image.tag }}{{ $img }}{{ include "hopsworkslib.imageDigest" (dict "global" .Values.global "entry" $img) }}'
            imagePullPolicy: IfNotPresent
            lifecycle:
              preStop:
                exec:
                  command:
                  - /bin/bash
                  - -c
                  - umount -l {{ .Values.global._hopsworks.trino.mountableSecrets.mountPath }} || true
            name: mountable-secrets
            resources:
              limits:
                cpu: 500m
                memory: 512Mi
              requests:
                cpu: 100m
                memory: 128Mi
            restartPolicy: Always
            securityContext:
              privileged: true
              runAsGroup: 0
              runAsNonRoot: false
              runAsUser: 0
            volumeMounts:
            - mountPath: '{{ .Values.global._hopsworks.trino.mountableSecrets.mountPath }}'
              mountPropagation: Bidirectional
              name: mountable-secrets
            - mountPath: /srv/hops/super_crypto/trino
              name: super-crypto-kstore
            - mountPath: /etc/hadoop/core-site.xml
              name: core-site
              subPath: core-site.xml
            - mountPath: /etc/hadoop/hdfs-site.xml
              name: hdfs-site
              subPath: hdfs-site.xml
          worker:
          - command:
            - /bin/sh
            - -c
            - |
              # Never hang and never fail. This is an init container, so it runs before Trino, and a
              # probe that exists to improve an error message must not be able to delay or block the
              # query engine. Both outcomes are swallowed and the line is always printed.
              URL='{{ .Values.global._hopsworks.trino.egressProbe.echoUrl }}'
              if [ -z "$URL" ]; then
                echo "trino-egress-address=disabled"
                exit 0
              fi
              echo "trino-egress-address=$(curl -s --max-time 5 "$URL" || echo unknown)"
            image: '{{ .Values.image.registry }}/{{ .Values.image.repository }}:{{ .Values.image.tag }}'
            imagePullPolicy: IfNotPresent
            name: egress-probe
            resources:
              limits:
                cpu: 500m
                memory: 256Mi
              requests:
                cpu: 10m
                memory: 32Mi
            securityContext:
              allowPrivilegeEscalation: false
              capabilities:
                drop:
                - ALL
          - command:
            - /bin/bash
            - -c
            - |
              set -euo pipefail
              export HADOOP_CONF_DIR=/etc/hadoop
              CERTS=/srv/hops/super_crypto/trino
              mkdir -p {{ .Values.global._hopsworks.trino.mountableSecrets.mountPath }} /tmp/.hopsfs-mount-staging
              # Foreground: this is a sidecar, it must not exit. No startupProbe gates Trino on the
              # mount, deliberately: a mount that never comes up must not keep the query engine down.
              # A catalog whose bundle is missing fails its own connection instead.
              exec hopsfs-mount \
                --logLevel warning \
                --stageDir /tmp/.hopsfs-mount-staging \
                --readOnly \
                --srcDir {{ .Values.global._hopsworks.trino.mountableSecrets.storeRoot }} \
                --hopsFSUserName trino \
                -allowOther=true \
                -tls \
                -rootCABundle "$CERTS/hops_root_ca.pem" \
                -clientCertificate "$CERTS/trino_certificate_bundle.pem" \
                -clientKey "$CERTS/trino_priv.pem" \
                namenode.service.{{ .Values.global._hopsworks.consulDomainName | default "consul" }}:8020 \
                {{ .Values.global._hopsworks.trino.mountableSecrets.mountPath }}
            image: '{{ $img := printf "%s/%s:%s" .Values.image.registry .Values.global._hopsworks.trino.mountableSecrets.image.repository .Values.global._hopsworks.trino.mountableSecrets.image.tag }}{{ $img }}{{ include "hopsworkslib.imageDigest" (dict "global" .Values.global "entry" $img) }}'
            imagePullPolicy: IfNotPresent
            lifecycle:
              preStop:
                exec:
                  command:
                  - /bin/bash
                  - -c
                  - umount -l {{ .Values.global._hopsworks.trino.mountableSecrets.mountPath }} || true
            name: mountable-secrets
            resources:
              limits:
                cpu: 500m
                memory: 512Mi
              requests:
                cpu: 100m
                memory: 128Mi
            restartPolicy: Always
            securityContext:
              privileged: true
              runAsGroup: 0
              runAsNonRoot: false
              runAsUser: 0
            volumeMounts:
            - mountPath: '{{ .Values.global._hopsworks.trino.mountableSecrets.mountPath }}'
              mountPropagation: Bidirectional
              name: mountable-secrets
            - mountPath: /srv/hops/super_crypto/trino
              name: super-crypto-kstore
            - mountPath: /etc/hadoop/core-site.xml
              name: core-site
              subPath: core-site.xml
            - mountPath: /etc/hadoop/hdfs-site.xml
              name: hdfs-site
              subPath: hdfs-site.xml
        moreCatalogs:
          tpcds.properties: |
            connector.name=tpcds
            tpcds.splits-per-node=4
          tpch.properties: |
            connector.name=tpch
            tpch.splits-per-node=4
        nameOverride: hopsworks-trino
        securityContext:
          runAsGroup: 1000
          runAsNonRoot: true
          runAsUser: 1000
          seccompProfile:
            type: RuntimeDefault
        server:
          config:
            authenticationType: PASSWORD
            https:
              enabled: true
              keystore:
                path: /certs/keystore.pem
              port: 8443
          coordinatorExtraConfig: |
            web-ui.preview.enabled=true
        service:
          coordinator:
            annotations:
              consul.hashicorp.com/service-name: trino
              consul.hashicorp.com/service-port: '8443'
              consul.hashicorp.com/service-tags: coordinator
              prometheus.io/path: /metrics
              prometheus.io/port: '8443'
              prometheus.io/scheme: https
              prometheus.io/scrape: 'true'
          type: ClusterIP
        serviceAccount:
          annotations: {}
          create: true
          name: hopsworks-trino
        worker:
          additionalConfigFiles:
            mysql-event-listener.properties: |
              event-listener.name=mysql
              mysql-event-listener.db.url={{ include "trino.mysql.eventListener.db.url" . }}
          additionalJVMConfig:
          - --add-opens=java.base/java.nio=ALL-UNNAMED
          additionalVolumeMounts:
          - mountPath: /etc/trino/catalog
            name: catalog-volume
          - mountPath: /opt/hopsworks/mounts
            mountPropagation: HostToContainer
            name: mountable-secrets
            readOnly: true
          additionalVolumes:
          - name: catalog-volume
            projected:
              sources:
              - configMap:
                  name: hopsworks-trino-catalogs
              - secret:
                  name: hopsworks-trino-catalogs-user-0
                  optional: true
              - secret:
                  name: hopsworks-trino-catalogs-user-1
                  optional: true
          - emptyDir: {}
            name: mountable-secrets
          configMounts:
          - configMap: hopsfs-config
            name: hdfs-site
            path: /etc/hadoop/hdfs-site.xml
            subPath: hdfs-site.xml
          - configMap: hopsfs-config
            name: core-site
            path: /etc/hadoop/core-site.xml
            subPath: core-site.xml
          secretMounts:
          - name: super-crypto-kstore
            path: /srv/hops/super_crypto/trino
            secretName: hopsworks-trino-crypto-material
        workerNameOverride: hopsworks-trino-worker
        ```

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
:   Type `string`, default `"480-v10"`.
    Image tag for the Trino image. This value is explicitly pinned here and overrides any defaulting to `appVersion` from Chart.yaml.

`trino.trino.initContainers.coordinator[2].name` <a class="headerlink" href="#helm.trino.trino.initContainers.coordinator.2.name" title="Permanent link">#</a> { #helm.trino.trino.initContainers.coordinator.2.name }
:   Type `string`, default `"mountable-secrets"`.
    readOnly is not optional. Without it the query engine gains a write channel into HopsFS as the trino service user. --srcDir bounds what the mount exposes to the backend-owned tree; the mount authenticates as trino, which is in the hdfs superuser group, so srcDir is the only thing containing it.  The preStop unmount is also not optional. Without it the container cannot terminate, the pod ends 0/2 Error, `kubectl delete pod` hangs, and force-deleting leaks fuse.hopsfs mounts onto the node that must then be cleared by hand with nsenter.

`trino.trino.initContainers.worker[1].name` <a class="headerlink" href="#helm.trino.trino.initContainers.worker.1.name" title="Permanent link">#</a> { #helm.trino.trino.initContainers.worker.1.name }
:   Type `string`, default `"mountable-secrets"`.
    readOnly is not optional. Without it the query engine gains a write channel into HopsFS as the trino service user. --srcDir bounds what the mount exposes to the backend-owned tree; the mount authenticates as trino, which is in the hdfs superuser group, so srcDir is the only thing containing it.  The preStop unmount is also not optional. Without it the container cannot terminate, the pod ends 0/2 Error, `kubectl delete pod` hangs, and force-deleting leaks fuse.hopsfs mounts onto the node that must then be cleared by hand with nsenter.

</div>

<!-- END GENERATED VALUES -->
