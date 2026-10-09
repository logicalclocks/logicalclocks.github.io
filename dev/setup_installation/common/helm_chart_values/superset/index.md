# Superset values { #helm-values-superset }

Values under `superset` configure Apache Superset, the BI dashboards over feature store data.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.2.0-alpha-1791557095` (Hopsworks `5.2.0`)._

Deployed according to the first of these values that is set: [`global._hopsworks.superset.enabled`](global.md#helm.global._hopsworks.superset.enabled), [`global._hopsworks.full_platform`](global.md#helm.global._hopsworks.full_platform).

!!! info "Upstream charts"

    - Values under `superset.mysql` go to [`mysql` 12.3.5](https://artifacthub.io/packages/helm/bitnami/mysql/12.3.5) from `oci://registry-1.docker.io/bitnamicharts`.
    - Values under `superset.superset` go to [`superset` 0.15.0](https://artifacthub.io/packages/helm/superset/superset/0.15.0) from `https://apache.github.io/superset`.

    Only the values Hopsworks sets under `superset.mysql` and `superset.superset` are listed on this page.
    Any other value of the charts can be set under the same keys; each link opens the chart's documentation for the version Hopsworks pins.

## General { #helm-values-superset-general }

??? example "Defaults as YAML"

    ```yaml
    superset:
      cleanupOnUninstall:
        enabled: true
        ttlSecondsAfterFinished: null
      hopsworkslib: {}
      imageRegistry: docker.hops.works/superset
      mysql:
        architecture: standalone
        auth:
          createDatabase: true
          customPasswordFiles: {}
          database: superset
          existingSecret: superset-mysql-users-secrets
          password: temp-value
          replicationPassword: ''
          replicationUser: replicator
          rootPassword: temp-value
          usePasswordFiles: false
          username: superset
        enabled: true
        global:
          security:
            allowInsecureImages: true
        image:
          digest: ''
          pullPolicy: IfNotPresent
          registry: docker.hops.works/superset
          repository: mysql
          tag: 8.4.11-ubuntu24.04-h4
        metrics:
          enabled: true
          image:
            digest: ''
            pullPolicy: IfNotPresent
            registry: docker.hops.works/superset
            repository: mysqld-exporter
            tag: 0.20.0-alpine-h1.1
          resources:
            limits:
              cpu: 100m
              memory: 64Mi
            requests:
              cpu: 50m
              memory: 64Mi
          service:
            annotations:
              prometheus.io/port: '{{ .Values.metrics.service.port }}'
              prometheus.io/scrape: 'true'
        primary:
          persistentVolumeClaimRetentionPolicy:
            enabled: true
            whenDeleted: Delete
            whenScaled: Retain
        volumePermissions:
          enabled: false
          image:
            digest: ''
            pullPolicy: IfNotPresent
            registry: docker.hops.works/superset
            repository: os-shell
            tag: 12-alpine-h1.1
      superset:
        _publicRoleDefaultName: Public
        allowAnonymousAccess: true
        configOverrides:
          feature_flags: |
            FEATURE_FLAGS = {"ALERT_REPORTS": True, "DASHBOARD_RBAC": True}
          flask_app_configuration: |
            from flask import session
            from flask import Flask
            from datetime import timedelta

            def make_session_permanent():
                '''
                Enable maxAge for the cookie 'session'
                '''
                session.permanent = True

            # Set up max age of session to 24 hours
            PERMANENT_SESSION_LIFETIME = timedelta(hours=24) # (default: "31 days")
            SESSION_REFRESH_EACH_REQUEST = True # Default: True
            def FLASK_APP_MUTATOR(app: Flask) -> None:
                app.before_request_funcs.setdefault(None, []).append(make_session_permanent)
          mysql: |
            SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
          proxyConfig: |
            ENABLE_PROXY_FIX = True
            APP_ICON = "/hopsworks-api/superset/static/assets/images/superset-logo-horiz.png"
            LOGO_TARGET_PATH = "/hopsworks-api/superset/superset/welcome/"
            {{- if .Values.init.loadExamples }}
            PREVENT_UNSAFE_DB_CONNECTIONS = False
            {{- else }}
            PREVENT_UNSAFE_DB_CONNECTIONS = True
            {{- end }}
          public_role: |
            {{- if .Values.publicRoleLike }}
            PUBLIC_ROLE_LIKE = {{ .Values.publicRoleLike | quote }}
            {{- end }}
            {{- if .Values.allowAnonymousAccess }}
            AUTH_ROLE_PUBLIC = {{ .Values._publicRoleDefaultName | quote }}
            {{- end }}
        extraEnv:
          SUPERSET_APP_ROOT: /hopsworks-api/superset
        extraEnvRaw:
        - name: SUPERSET_USER
          valueFrom:
            secretKeyRef:
              key: username
              name: superset-admin-credentials
        - name: SUPERSET_PASS
          valueFrom:
            secretKeyRef:
              key: password
              name: superset-admin-credentials
        - name: DB_PASS
          valueFrom:
            secretKeyRef:
              key: mysql-password
              name: superset-mysql-users-secrets
        - name: SUPERSET_SECRET_KEY
          valueFrom:
            secretKeyRef:
              key: secret-key
              name: superset-secret-key
        extraRoles:
        - name: Dataset
          permissions:
          - - can_duplicate
            - Dataset
          - - can_write
            - Dataset
          - - can_get_or_create_dataset
            - Dataset
          - - can_warm_up_cache
            - Dataset
        extraVolumeMounts:
        - mountPath: /srv/hops/super_crypto/superset
          name: super-crypto-material
          readOnly: true
        extraVolumes:
        - name: super-crypto-material
          secret:
            optional: true
            secretName: hopsworks-superset-crypto-material
        fullnameOverride: hopsworks-superset
        image:
          pullPolicy: IfNotPresent
          repository: docker.hops.works/hopsworks/superset
          tag: 6.0.0p4.4
        init:
          adminUser:
            email: admin@superset.com
            firstname: Superset
            lastname: Admin
            password: $SUPERSET_PASS
            username: $SUPERSET_USER
          command:
          - /bin/sh
          - -c
          - |
            {{- if ((((.Values.global | default dict)._hopsworks | default dict).restoreFromBackup | default dict).superset | default dict).enabled }}
            echo "Superset restore in progress (global._hopsworks.restoreFromBackup.superset.enabled): skipping init so no schema work runs while the database is reloaded. It runs on the upgrade that clears the flag."; exit 0
            {{- end }}
            . {{ .Values.configMountPath }}/superset_bootstrap.sh; . {{ .Values.configMountPath }}/superset_init.sh;
            {{- if .Values.extraRoles }}
            {{- range $role := .Values.extraRoles }}
            python /scripts/create_role.py --role-name {{ $role.name }} --permissions '{{ $role.permissions | toJson | b64enc }}';
            {{- end }}
            {{- end }}
            {{- if and .Values.publicRolePermissions (eq .Values.publicRoleLike .Values._publicRoleDefaultName) }}
            python /scripts/create_role.py --role-name {{ .Values._publicRoleDefaultName }} --permissions '{{ .Values.publicRolePermissions | toJson | b64enc }}';
            {{- end }}
          containerSecurityContext:
            allowPrivilegeEscalation: false
            capabilities:
              drop:
              - ALL
          initContainers:
          - command:
            - /bin/sh
            - -c
            - dockerize -wait "tcp://$DB_HOST:$DB_PORT" -timeout 120s
            envFrom:
            - secretRef:
                name: '{{ tpl .Values.envFromSecret . }}'
            image: '{{ .Values.initImage.repository }}:{{ .Values.initImage.tag }}'
            imagePullPolicy: '{{ .Values.initImage.pullPolicy }}'
            name: wait-for-database
            resources:
              limits:
                cpu: 500m
                memory: 256Mi
              requests:
                cpu: 250m
                memory: 128Mi
            securityContext:
              allowPrivilegeEscalation: false
              capabilities:
                drop:
                - ALL
          loadExamples: false
          podSecurityContext:
            runAsNonRoot: true
            seccompProfile:
              type: RuntimeDefault
        initImage:
          pullPolicy: IfNotPresent
          repository: docker.hops.works/superset/dockerize
          tag: 0.14.0-alpine-h1.1
        postgresql:
          enabled: false
        publicRoleLike: Public
        publicRolePermissions:
        - - can_read
          - Dashboard
        - - can_read
          - Chart
        - - can_dashboard
          - Superset
        - - can_slice
          - Superset
        - - can_explore_json
          - Superset
        - - can_dashboard_permalink
          - Superset
        - - can_read
          - DashboardPermalinkRestApi
        - - can_read
          - DashboardFilterStateRestApi
        - - can_write
          - DashboardFilterStateRestApi
        - - can_time_range
          - Api
        - - can_query_form_data
          - Api
        - - can_query
          - Api
        - - can_read
          - CssTemplate
        - - can_read
          - Theme
        - - can_read
          - EmbeddedDashboard
        - - can_read
          - CurrentUserRestApi
        - - can_get
          - Datasource
        - - can_external_metadata
          - Datasource
        - - can_read
          - Annotation
        - - can_read
          - AnnotationLayerRestApi
        - - can_read
          - ExplorePermalinkRestApi
        redis:
          enabled: true
          image:
            registry: docker.hops.works/superset
            repository: redis
            tag: 7.4.11-alpine-h1
          master:
            configuration: |-
              maxmemory 256mb
              maxmemory-policy allkeys-lru
            containerSecurityContext:
              allowPrivilegeEscalation: false
              capabilities:
                drop:
                - ALL
              enabled: true
              readOnlyRootFilesystem: true
              runAsGroup: 1001
              runAsNonRoot: true
              runAsUser: 1001
              seLinuxOptions: {}
              seccompProfile:
                type: RuntimeDefault
            podSecurityContext:
              enabled: true
              fsGroup: 1001
              fsGroupChangePolicy: Always
              runAsNonRoot: true
              runAsUser: 1001
              seccompProfile:
                type: RuntimeDefault
              supplementalGroups: []
              sysctls: []
            resources:
              limits:
                cpu: 500m
                memory: 384Mi
              requests:
                cpu: 100m
                memory: 384Mi
          metrics:
            containerSecurityContext:
              allowPrivilegeEscalation: false
              capabilities:
                drop:
                - ALL
              enabled: true
              readOnlyRootFilesystem: true
              runAsGroup: 1001
              runAsNonRoot: true
              runAsUser: 1001
              seLinuxOptions: {}
              seccompProfile:
                type: RuntimeDefault
            enabled: true
            image:
              digest: ''
              pullPolicy: IfNotPresent
              registry: docker.hops.works/superset
              repository: redis-exporter
              tag: 1.90.0-alpine-h1.1
            resources:
              limits:
                cpu: 100m
                memory: 64Mi
              requests:
                cpu: 50m
                memory: 64Mi
            service:
              annotations:
                prometheus.io/port: '{{ .Values.metrics.service.port }}'
                prometheus.io/scrape: 'true'
        runAsUser: 1000
        secretEnv:
          create: false
        service:
          annotations:
            consul.hashicorp.com/service-name: superset
            consul.hashicorp.com/service-tags: app
        supersetNode:
          connections:
            db_host: '{{ .Release.Name }}-mysql'
            db_name: superset
            db_pass: superset
            db_port: '3306'
            db_type: mysql
            db_user: superset
          containerSecurityContext:
            allowPrivilegeEscalation: false
            capabilities:
              drop:
              - ALL
          initContainers:
          - command:
            - /bin/sh
            - -c
            - dockerize -wait "tcp://$DB_HOST:$DB_PORT" -timeout 120s
            envFrom:
            - secretRef:
                name: '{{ tpl .Values.envFromSecret . }}'
            image: '{{ .Values.initImage.repository }}:{{ .Values.initImage.tag }}'
            imagePullPolicy: '{{ .Values.initImage.pullPolicy }}'
            name: wait-for-db
            resources:
              limits:
                cpu: 500m
                memory: 256Mi
              requests:
                cpu: 250m
                memory: 128Mi
            securityContext:
              allowPrivilegeEscalation: false
              capabilities:
                drop:
                - ALL
          livenessProbe:
            failureThreshold: 3
            httpGet:
              path: /hopsworks-api/superset/health
              port: http
            initialDelaySeconds: 15
            periodSeconds: 15
            successThreshold: 1
            timeoutSeconds: 1
          podSecurityContext:
            runAsNonRoot: true
            seccompProfile:
              type: RuntimeDefault
          readinessProbe:
            failureThreshold: 3
            httpGet:
              path: /hopsworks-api/superset/health
              port: http
            initialDelaySeconds: 15
            periodSeconds: 15
            successThreshold: 1
            timeoutSeconds: 1
          replicas:
            enabled: true
            replicaCount: 1
          startupProbe:
            failureThreshold: 60
            httpGet:
              path: /hopsworks-api/superset/health
              port: http
            initialDelaySeconds: 15
            periodSeconds: 5
            successThreshold: 1
            timeoutSeconds: 1
        supersetWorker:
          command:
          - /bin/sh
          - -c
          - . {{ .Values.configMountPath }}/superset_bootstrap.sh; celery --app=superset.tasks.celery_app:app worker --pool=prefork -O fair -c 4
          containerSecurityContext:
            allowPrivilegeEscalation: false
            capabilities:
              drop:
              - ALL
          initContainers:
          - command:
            - /bin/sh
            - -c
            - dockerize -wait "tcp://$DB_HOST:$DB_PORT" -wait "tcp://$REDIS_HOST:$REDIS_PORT" -timeout 120s
            envFrom:
            - secretRef:
                name: '{{ tpl .Values.envFromSecret . }}'
            image: '{{ .Values.initImage.repository }}:{{ .Values.initImage.tag }}'
            imagePullPolicy: '{{ .Values.initImage.pullPolicy }}'
            name: wait-for-db-redis
            resources:
              limits:
                cpu: 500m
                memory: 256Mi
              requests:
                cpu: 250m
                memory: 128Mi
            securityContext:
              allowPrivilegeEscalation: false
              capabilities:
                drop:
                - ALL
          podSecurityContext:
            runAsNonRoot: true
            seccompProfile:
              type: RuntimeDefault
          replicas:
            enabled: false
          resources:
            limits:
              cpu: 500m
              memory: 1024Mi
            requests:
              cpu: 500m
              memory: 1024Mi
    ```

<div class="hops-values" markdown>

`superset` <a class="headerlink" href="#helm.superset" title="Permanent link">#</a> { #helm.superset }
:   Type `object`, default `{"mysql":{"enabled":true},"superset":{"redis":{"enabled":true}}}`.
    override superset values

`superset.cleanupOnUninstall` <a class="headerlink" href="#helm.superset.cleanupOnUninstall" title="Permanent link">#</a> { #helm.superset.cleanupOnUninstall }
:   Type `object`, default `{"enabled":true,"ttlSecondsAfterFinished":null}`.
    post-delete cleanup of the Superset MySQL data PVC for existing clusters whose StatefulSet predates the persistentVolumeClaimRetentionPolicy fix. Gated by global._hopsworks.wipeDataOnUninstall and honors the hopsworks.ai/keep=true label, like the other data-PVC teardowns. New clusters clean up natively via the retention policy (which deletes unconditionally).

`superset.cleanupOnUninstall.enabled` <a class="headerlink" href="#helm.superset.cleanupOnUninstall.enabled" title="Permanent link">#</a> { #helm.superset.cleanupOnUninstall.enabled }
:   Type `bool`, default `true`.
    enable the post-delete Superset MySQL PVC cleanup hook (also requires global._hopsworks.wipeDataOnUninstall)

`superset.cleanupOnUninstall.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.superset.cleanupOnUninstall.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.superset.cleanupOnUninstall.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    ttlSecondsAfterFinished for the cleanup Job; null falls through to the global default

`superset.hopsworkslib` <a class="headerlink" href="#helm.superset.hopsworkslib" title="Permanent link">#</a> { #helm.superset.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`superset.imageRegistry` <a class="headerlink" href="#helm.superset.imageRegistry" title="Permanent link">#</a> { #helm.superset.imageRegistry }
:   Type `string`, default `"docker.hops.works/superset"`.

`superset.mysql` <a class="headerlink" href="#helm.superset.mysql" title="Permanent link">#</a> { #helm.superset.mysql }
:   Type `object`, passed to the [`mysql` 12.3.5](https://artifacthub.io/packages/helm/bitnami/mysql/12.3.5) chart, whose other values are documented there.
    override superset mysql values

    ??? note "Default"

        ```yaml
        architecture: standalone
        auth:
          createDatabase: true
          customPasswordFiles: {}
          database: superset
          existingSecret: superset-mysql-users-secrets
          password: temp-value
          replicationPassword: ''
          replicationUser: replicator
          rootPassword: temp-value
          usePasswordFiles: false
          username: superset
        enabled: true
        global:
          security:
            allowInsecureImages: true
        image:
          digest: ''
          pullPolicy: IfNotPresent
          registry: docker.hops.works/superset
          repository: mysql
          tag: 8.4.11-ubuntu24.04-h4
        metrics:
          enabled: true
          image:
            digest: ''
            pullPolicy: IfNotPresent
            registry: docker.hops.works/superset
            repository: mysqld-exporter
            tag: 0.20.0-alpine-h1.1
          resources:
            limits:
              cpu: 100m
              memory: 64Mi
            requests:
              cpu: 50m
              memory: 64Mi
          service:
            annotations:
              prometheus.io/port: '{{ .Values.metrics.service.port }}'
              prometheus.io/scrape: 'true'
        primary:
          persistentVolumeClaimRetentionPolicy:
            enabled: true
            whenDeleted: Delete
            whenScaled: Retain
        volumePermissions:
          enabled: false
          image:
            digest: ''
            pullPolicy: IfNotPresent
            registry: docker.hops.works/superset
            repository: os-shell
            tag: 12-alpine-h1.1
        ```

`superset.superset` <a class="headerlink" href="#helm.superset.superset" title="Permanent link">#</a> { #helm.superset.superset }
:   Type `object`, passed to the [`superset` 0.15.0](https://artifacthub.io/packages/helm/superset/superset/0.15.0) chart, whose other values are documented there.
    override superset values

    ??? note "Default"

        ```yaml
        _publicRoleDefaultName: Public
        allowAnonymousAccess: true
        configOverrides:
          feature_flags: |
            FEATURE_FLAGS = {"ALERT_REPORTS": True, "DASHBOARD_RBAC": True}
          flask_app_configuration: |
            from flask import session
            from flask import Flask
            from datetime import timedelta

            def make_session_permanent():
                '''
                Enable maxAge for the cookie 'session'
                '''
                session.permanent = True

            # Set up max age of session to 24 hours
            PERMANENT_SESSION_LIFETIME = timedelta(hours=24) # (default: "31 days")
            SESSION_REFRESH_EACH_REQUEST = True # Default: True
            def FLASK_APP_MUTATOR(app: Flask) -> None:
                app.before_request_funcs.setdefault(None, []).append(make_session_permanent)
          mysql: |
            SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
          proxyConfig: |
            ENABLE_PROXY_FIX = True
            APP_ICON = "/hopsworks-api/superset/static/assets/images/superset-logo-horiz.png"
            LOGO_TARGET_PATH = "/hopsworks-api/superset/superset/welcome/"
            {{- if .Values.init.loadExamples }}
            PREVENT_UNSAFE_DB_CONNECTIONS = False
            {{- else }}
            PREVENT_UNSAFE_DB_CONNECTIONS = True
            {{- end }}
          public_role: |
            {{- if .Values.publicRoleLike }}
            PUBLIC_ROLE_LIKE = {{ .Values.publicRoleLike | quote }}
            {{- end }}
            {{- if .Values.allowAnonymousAccess }}
            AUTH_ROLE_PUBLIC = {{ .Values._publicRoleDefaultName | quote }}
            {{- end }}
        extraEnv:
          SUPERSET_APP_ROOT: /hopsworks-api/superset
        extraEnvRaw:
        - name: SUPERSET_USER
          valueFrom:
            secretKeyRef:
              key: username
              name: superset-admin-credentials
        - name: SUPERSET_PASS
          valueFrom:
            secretKeyRef:
              key: password
              name: superset-admin-credentials
        - name: DB_PASS
          valueFrom:
            secretKeyRef:
              key: mysql-password
              name: superset-mysql-users-secrets
        - name: SUPERSET_SECRET_KEY
          valueFrom:
            secretKeyRef:
              key: secret-key
              name: superset-secret-key
        extraRoles:
        - name: Dataset
          permissions:
          - - can_duplicate
            - Dataset
          - - can_write
            - Dataset
          - - can_get_or_create_dataset
            - Dataset
          - - can_warm_up_cache
            - Dataset
        extraVolumeMounts:
        - mountPath: /srv/hops/super_crypto/superset
          name: super-crypto-material
          readOnly: true
        extraVolumes:
        - name: super-crypto-material
          secret:
            optional: true
            secretName: hopsworks-superset-crypto-material
        fullnameOverride: hopsworks-superset
        image:
          pullPolicy: IfNotPresent
          repository: docker.hops.works/hopsworks/superset
          tag: 6.0.0p4.4
        init:
          adminUser:
            email: admin@superset.com
            firstname: Superset
            lastname: Admin
            password: $SUPERSET_PASS
            username: $SUPERSET_USER
          command:
          - /bin/sh
          - -c
          - |
            {{- if ((((.Values.global | default dict)._hopsworks | default dict).restoreFromBackup | default dict).superset | default dict).enabled }}
            echo "Superset restore in progress (global._hopsworks.restoreFromBackup.superset.enabled): skipping init so no schema work runs while the database is reloaded. It runs on the upgrade that clears the flag."; exit 0
            {{- end }}
            . {{ .Values.configMountPath }}/superset_bootstrap.sh; . {{ .Values.configMountPath }}/superset_init.sh;
            {{- if .Values.extraRoles }}
            {{- range $role := .Values.extraRoles }}
            python /scripts/create_role.py --role-name {{ $role.name }} --permissions '{{ $role.permissions | toJson | b64enc }}';
            {{- end }}
            {{- end }}
            {{- if and .Values.publicRolePermissions (eq .Values.publicRoleLike .Values._publicRoleDefaultName) }}
            python /scripts/create_role.py --role-name {{ .Values._publicRoleDefaultName }} --permissions '{{ .Values.publicRolePermissions | toJson | b64enc }}';
            {{- end }}
          containerSecurityContext:
            allowPrivilegeEscalation: false
            capabilities:
              drop:
              - ALL
          initContainers:
          - command:
            - /bin/sh
            - -c
            - dockerize -wait "tcp://$DB_HOST:$DB_PORT" -timeout 120s
            envFrom:
            - secretRef:
                name: '{{ tpl .Values.envFromSecret . }}'
            image: '{{ .Values.initImage.repository }}:{{ .Values.initImage.tag }}'
            imagePullPolicy: '{{ .Values.initImage.pullPolicy }}'
            name: wait-for-database
            resources:
              limits:
                cpu: 500m
                memory: 256Mi
              requests:
                cpu: 250m
                memory: 128Mi
            securityContext:
              allowPrivilegeEscalation: false
              capabilities:
                drop:
                - ALL
          loadExamples: false
          podSecurityContext:
            runAsNonRoot: true
            seccompProfile:
              type: RuntimeDefault
        initImage:
          pullPolicy: IfNotPresent
          repository: docker.hops.works/superset/dockerize
          tag: 0.14.0-alpine-h1.1
        postgresql:
          enabled: false
        publicRoleLike: Public
        publicRolePermissions:
        - - can_read
          - Dashboard
        - - can_read
          - Chart
        - - can_dashboard
          - Superset
        - - can_slice
          - Superset
        - - can_explore_json
          - Superset
        - - can_dashboard_permalink
          - Superset
        - - can_read
          - DashboardPermalinkRestApi
        - - can_read
          - DashboardFilterStateRestApi
        - - can_write
          - DashboardFilterStateRestApi
        - - can_time_range
          - Api
        - - can_query_form_data
          - Api
        - - can_query
          - Api
        - - can_read
          - CssTemplate
        - - can_read
          - Theme
        - - can_read
          - EmbeddedDashboard
        - - can_read
          - CurrentUserRestApi
        - - can_get
          - Datasource
        - - can_external_metadata
          - Datasource
        - - can_read
          - Annotation
        - - can_read
          - AnnotationLayerRestApi
        - - can_read
          - ExplorePermalinkRestApi
        redis:
          enabled: true
          image:
            registry: docker.hops.works/superset
            repository: redis
            tag: 7.4.11-alpine-h1
          master:
            configuration: |-
              maxmemory 256mb
              maxmemory-policy allkeys-lru
            containerSecurityContext:
              allowPrivilegeEscalation: false
              capabilities:
                drop:
                - ALL
              enabled: true
              readOnlyRootFilesystem: true
              runAsGroup: 1001
              runAsNonRoot: true
              runAsUser: 1001
              seLinuxOptions: {}
              seccompProfile:
                type: RuntimeDefault
            podSecurityContext:
              enabled: true
              fsGroup: 1001
              fsGroupChangePolicy: Always
              runAsNonRoot: true
              runAsUser: 1001
              seccompProfile:
                type: RuntimeDefault
              supplementalGroups: []
              sysctls: []
            resources:
              limits:
                cpu: 500m
                memory: 384Mi
              requests:
                cpu: 100m
                memory: 384Mi
          metrics:
            containerSecurityContext:
              allowPrivilegeEscalation: false
              capabilities:
                drop:
                - ALL
              enabled: true
              readOnlyRootFilesystem: true
              runAsGroup: 1001
              runAsNonRoot: true
              runAsUser: 1001
              seLinuxOptions: {}
              seccompProfile:
                type: RuntimeDefault
            enabled: true
            image:
              digest: ''
              pullPolicy: IfNotPresent
              registry: docker.hops.works/superset
              repository: redis-exporter
              tag: 1.90.0-alpine-h1.1
            resources:
              limits:
                cpu: 100m
                memory: 64Mi
              requests:
                cpu: 50m
                memory: 64Mi
            service:
              annotations:
                prometheus.io/port: '{{ .Values.metrics.service.port }}'
                prometheus.io/scrape: 'true'
        runAsUser: 1000
        secretEnv:
          create: false
        service:
          annotations:
            consul.hashicorp.com/service-name: superset
            consul.hashicorp.com/service-tags: app
        supersetNode:
          connections:
            db_host: '{{ .Release.Name }}-mysql'
            db_name: superset
            db_pass: superset
            db_port: '3306'
            db_type: mysql
            db_user: superset
          containerSecurityContext:
            allowPrivilegeEscalation: false
            capabilities:
              drop:
              - ALL
          initContainers:
          - command:
            - /bin/sh
            - -c
            - dockerize -wait "tcp://$DB_HOST:$DB_PORT" -timeout 120s
            envFrom:
            - secretRef:
                name: '{{ tpl .Values.envFromSecret . }}'
            image: '{{ .Values.initImage.repository }}:{{ .Values.initImage.tag }}'
            imagePullPolicy: '{{ .Values.initImage.pullPolicy }}'
            name: wait-for-db
            resources:
              limits:
                cpu: 500m
                memory: 256Mi
              requests:
                cpu: 250m
                memory: 128Mi
            securityContext:
              allowPrivilegeEscalation: false
              capabilities:
                drop:
                - ALL
          livenessProbe:
            failureThreshold: 3
            httpGet:
              path: /hopsworks-api/superset/health
              port: http
            initialDelaySeconds: 15
            periodSeconds: 15
            successThreshold: 1
            timeoutSeconds: 1
          podSecurityContext:
            runAsNonRoot: true
            seccompProfile:
              type: RuntimeDefault
          readinessProbe:
            failureThreshold: 3
            httpGet:
              path: /hopsworks-api/superset/health
              port: http
            initialDelaySeconds: 15
            periodSeconds: 15
            successThreshold: 1
            timeoutSeconds: 1
          replicas:
            enabled: true
            replicaCount: 1
          startupProbe:
            failureThreshold: 60
            httpGet:
              path: /hopsworks-api/superset/health
              port: http
            initialDelaySeconds: 15
            periodSeconds: 5
            successThreshold: 1
            timeoutSeconds: 1
        supersetWorker:
          command:
          - /bin/sh
          - -c
          - . {{ .Values.configMountPath }}/superset_bootstrap.sh; celery --app=superset.tasks.celery_app:app worker --pool=prefork -O fair -c 4
          containerSecurityContext:
            allowPrivilegeEscalation: false
            capabilities:
              drop:
              - ALL
          initContainers:
          - command:
            - /bin/sh
            - -c
            - dockerize -wait "tcp://$DB_HOST:$DB_PORT" -wait "tcp://$REDIS_HOST:$REDIS_PORT" -timeout 120s
            envFrom:
            - secretRef:
                name: '{{ tpl .Values.envFromSecret . }}'
            image: '{{ .Values.initImage.repository }}:{{ .Values.initImage.tag }}'
            imagePullPolicy: '{{ .Values.initImage.pullPolicy }}'
            name: wait-for-db-redis
            resources:
              limits:
                cpu: 500m
                memory: 256Mi
              requests:
                cpu: 250m
                memory: 128Mi
            securityContext:
              allowPrivilegeEscalation: false
              capabilities:
                drop:
                - ALL
          podSecurityContext:
            runAsNonRoot: true
            seccompProfile:
              type: RuntimeDefault
          replicas:
            enabled: false
          resources:
            limits:
              cpu: 500m
              memory: 1024Mi
            requests:
              cpu: 500m
              memory: 1024Mi
        ```

`superset.superset.fullnameOverride` <a class="headerlink" href="#helm.superset.superset.fullnameOverride" title="Permanent link">#</a> { #helm.superset.superset.fullnameOverride }
:   Type `string`, default `"hopsworks-superset"`.
    Provide a name to override the full names of resources

`superset.superset.runAsUser` <a class="headerlink" href="#helm.superset.superset.runAsUser" title="Permanent link">#</a> { #helm.superset.superset.runAsUser }
:   Type `int`, default `1000`.
    User ID directive. This user must have enough permissions to run the bootstrap script Running containers as root is not recommended in production. Change this to another UID - e.g. 1000 to be more secure

</div>

## auth { #helm-values-superset-auth }

??? example "Defaults as YAML"

    ```yaml
    superset:
      auth:
        adminUserSecret: superset-admin-credentials
        adminUsername: adminuser
        createSecretEnvs: true
        createSecrets: true
        mysqlUserSecretName: superset-mysql-users-secrets
        secretKeySecretName: superset-secret-key
    ```

<div class="hops-values" markdown>

`superset.auth.adminUserSecret` <a class="headerlink" href="#helm.superset.auth.adminUserSecret" title="Permanent link">#</a> { #helm.superset.auth.adminUserSecret }
:   Type `string`, default `"superset-admin-credentials"`.

`superset.auth.adminUsername` <a class="headerlink" href="#helm.superset.auth.adminUsername" title="Permanent link">#</a> { #helm.superset.auth.adminUsername }
:   Type `string`, default `"adminuser"`.

`superset.auth.createSecretEnvs` <a class="headerlink" href="#helm.superset.auth.createSecretEnvs" title="Permanent link">#</a> { #helm.superset.auth.createSecretEnvs }
:   Type `bool`, default `true`.

`superset.auth.createSecrets` <a class="headerlink" href="#helm.superset.auth.createSecrets" title="Permanent link">#</a> { #helm.superset.auth.createSecrets }
:   Type `bool`, default `true`.

`superset.auth.mysqlUserSecretName` <a class="headerlink" href="#helm.superset.auth.mysqlUserSecretName" title="Permanent link">#</a> { #helm.superset.auth.mysqlUserSecretName }
:   Type `string`, default `"superset-mysql-users-secrets"`.

`superset.auth.secretKeySecretName` <a class="headerlink" href="#helm.superset.auth.secretKeySecretName" title="Permanent link">#</a> { #helm.superset.auth.secretKeySecretName }
:   Type `string`, default `"superset-secret-key"`.

</div>

## backups { #helm-values-superset-backups }

??? example "Defaults as YAML"

    ```yaml
    superset:
      backups:
        activeDeadlineSeconds: 3600
        backoffLimit: 1
        enabled: true
        pathPrefix: superset_backup
        schedule: null
        tmpSizeLimit: 2Gi
        ttl: null
        ttlSecondsAfterFinished: null
    ```

<div class="hops-values" markdown>

`superset.backups` <a class="headerlink" href="#helm.superset.backups" title="Permanent link">#</a> { #helm.superset.backups }
:   Type `object`.
    Superset MySQL backup (HWORKS-2973): a scheduled logical mysqldump of the `superset` schema to the platform object store (same bucket as the other backups), plus an authoritative manifest and a Velero-captured metadata index. Rendered only when global._hopsworks.backups.enabled is true and an object store is configured.

    ??? note "Default"

        ```yaml
        activeDeadlineSeconds: 3600
        backoffLimit: 1
        enabled: true
        pathPrefix: superset_backup
        schedule: null
        tmpSizeLimit: 2Gi
        ttl: null
        ttlSecondsAfterFinished: null
        ```

`superset.backups.activeDeadlineSeconds` <a class="headerlink" href="#helm.superset.backups.activeDeadlineSeconds" title="Permanent link">#</a> { #helm.superset.backups.activeDeadlineSeconds }
:   Type `int`, default `3600`.
    activeDeadlineSeconds for the backup Job; bounds a hung run so it cannot block later schedules under concurrencyPolicy Forbid, and bounds the dump and upload

`superset.backups.backoffLimit` <a class="headerlink" href="#helm.superset.backups.backoffLimit" title="Permanent link">#</a> { #helm.superset.backups.backoffLimit }
:   Type `int`, default `1`.
    backoffLimit for the backup Job

`superset.backups.enabled` <a class="headerlink" href="#helm.superset.backups.enabled" title="Permanent link">#</a> { #helm.superset.backups.enabled }
:   Type `bool`, default `true`.
    enable the scheduled Superset database backup CronJob

`superset.backups.pathPrefix` <a class="headerlink" href="#helm.superset.backups.pathPrefix" title="Permanent link">#</a> { #helm.superset.backups.pathPrefix }
:   Type `string`, default `"superset_backup"`.
    object-path prefix within the backup bucket

`superset.backups.schedule` <a class="headerlink" href="#helm.superset.backups.schedule" title="Permanent link">#</a> { #helm.superset.backups.schedule }
:   Type `string`, default `nil`.
    backup schedule (cron or @weekly). null inherits global._hopsworks.backups.schedule, else @weekly

`superset.backups.tmpSizeLimit` <a class="headerlink" href="#helm.superset.backups.tmpSizeLimit" title="Permanent link">#</a> { #helm.superset.backups.tmpSizeLimit }
:   Type `string`, default `"2Gi"`.
    size limit for the temporary dump volume and the container ephemeral-storage request/limit

`superset.backups.ttl` <a class="headerlink" href="#helm.superset.backups.ttl" title="Permanent link">#</a> { #helm.superset.backups.ttl }
:   Type `string`, default `nil`.
    retention (Go duration, e.g. 60d) for pruning whole backup sets older than the value. null inherits the global setting

`superset.backups.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.superset.backups.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.superset.backups.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    ttlSecondsAfterFinished for finished backup Job pods (removes the pod, and its node-local dump scratch, after completion). null falls through to the global default

</div>

<!-- END GENERATED VALUES -->
