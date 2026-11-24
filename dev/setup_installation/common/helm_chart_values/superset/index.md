# Superset values { #helm-values-superset }

Values under `superset` configure Apache Superset, the BI dashboards over feature store data.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.3.0-alpha-1795511784` (Hopsworks `5.3.0`)._

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
          tag: 8.4.13-ubuntu24.04-h2
        metrics:
          enabled: true
          image:
            digest: ''
            pullPolicy: IfNotPresent
            registry: docker.hops.works/superset
            repository: mysqld-exporter
            tag: 0.20.0-alpine-h3.2
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
            tag: 12-alpine-h3.1
      superset:
        redis:
          enabled: true
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
          tag: 8.4.13-ubuntu24.04-h2
        metrics:
          enabled: true
          image:
            digest: ''
            pullPolicy: IfNotPresent
            registry: docker.hops.works/superset
            repository: mysqld-exporter
            tag: 0.20.0-alpine-h3.2
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
            tag: 12-alpine-h3.1
        ```

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

## mcp { #helm-values-superset-mcp }

??? example "Defaults as YAML"

    ```yaml
    superset:
      mcp:
        enabled: true
        jwtSecret: null
        port: 5008
        replicas: 1
        resources:
          limits:
            cpu: '1'
            memory: 2Gi
          requests:
            cpu: 100m
            memory: 1Gi
    ```

<div class="hops-values" markdown>

`superset.mcp` <a class="headerlink" href="#helm.superset.mcp" title="Permanent link">#</a> { #helm.superset.mcp }
:   Type `object`.
    Superset's MCP service, which the hops CLI calls to generate charts. Authenticated with JWTs Hopsworks mints per call for the caller's project Superset user

    ??? note "Default"

        ```yaml
        enabled: true
        jwtSecret: null
        port: 5008
        replicas: 1
        resources:
          limits:
            cpu: '1'
            memory: 2Gi
          requests:
            cpu: 100m
            memory: 1Gi
        ```

`superset.mcp.enabled` <a class="headerlink" href="#helm.superset.mcp.enabled" title="Permanent link">#</a> { #helm.superset.mcp.enabled }
:   Type `bool`, default `true`.
    run the MCP service

`superset.mcp.jwtSecret` <a class="headerlink" href="#helm.superset.mcp.jwtSecret" title="Permanent link">#</a> { #helm.superset.mcp.jwtSecret }
:   Type `string`, default `nil`.
    JWT signing secret. Leave null to generate it once and keep it; a value set here replaces the key, on install and upgrade alike. Set it when the chart is rendered without cluster access (global._hopsworks.mode not auto, as under ArgoCD), or the MCP service is not rendered

`superset.mcp.port` <a class="headerlink" href="#helm.superset.mcp.port" title="Permanent link">#</a> { #helm.superset.mcp.port }
:   Type `int`, default `5008`.
    Port the MCP container listens on. Its Service, which the SDK and the CLI call, stays on 5008.

`superset.mcp.replicas` <a class="headerlink" href="#helm.superset.mcp.replicas" title="Permanent link">#</a> { #helm.superset.mcp.replicas }
:   Type `int`, default `1`.
    MCP service replicas

`superset.mcp.resources` <a class="headerlink" href="#helm.superset.mcp.resources" title="Permanent link">#</a> { #helm.superset.mcp.resources }
:   Type `object`, default `{"limits":{"cpu":"1","memory":"2Gi"},"requests":{"cpu":"100m","memory":"1Gi"}}`.
    MCP service container resources

</div>

## superset { #helm-values-superset-superset }

??? example "Defaults as YAML"

    ```yaml
    superset:
      superset:
        _publicRoleDefaultName: Public
        allowAnonymousAccess: true
        configOverrides:
          databaseInitialization: |
            # Only the initialization Job creates security tables.
            FAB_CREATE_DB = os.getenv("SUPERSET_INIT_DB", "false").lower() == "true"
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
          mcp: |
            # Read only by the MCP service (templates/mcp.yaml), the one pod with MCP_JWT_SECRET. Without
            # it the service refuses to start rather than serve unauthenticated.
            MCP_AUTH_ENABLED = True
            MCP_JWT_ALGORITHM = "HS256"
            MCP_JWT_SECRET = os.getenv("MCP_JWT_SECRET")
            MCP_JWT_ISSUER = "hopsworks"
            MCP_JWT_AUDIENCE = "superset-mcp"
            MCP_DEV_USERNAME = None
            # Set only in the MCP pod, which serves HTTPS with them (templates/mcp.yaml).
            MCP_SSL_CERTFILE = os.getenv("MCP_SSL_CERTFILE")
            MCP_SSL_KEYFILE = os.getenv("MCP_SSL_KEYFILE")
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
          security_manager: |
            import hashlib
            import inspect
            import logging

            from flask import g
            from flask_appbuilder.security.sqla.models import (
                assoc_group_role,
                assoc_permissionview_role,
                assoc_user_group,
                assoc_user_role,
            )
            from sqlalchemy import select
            from superset.security import SupersetSecurityManager
            from superset.utils.core import get_user_id

            # A security manager set by an earlier override stays the base class.
            _security_manager = globals().get("CUSTOM_SECURITY_MANAGER") or SupersetSecurityManager

            class HopsworksSecurityManager(_security_manager):
                def user_view_menu_names(self, permission_name):
                    """The names Superset's lookup returns, read from the same tables in the same request.

                    Superset tests the user's roles with a correlated EXISTS on every granted permission,
                    so MySQL reads all of ab_permission_view_role on each call, and a request makes
                    several. Hopsworks adds a role and its grants per project member, so that table grows
                    with the cluster. Here the user's role ids are read first and passed as literals,
                    which lets MySQL start from idx_role_id and read only the user's grants.
                    """
                    if g.user.is_anonymous or self.is_guest_user():
                        return super().user_view_menu_names(permission_name)
                    user_id = get_user_id()
                    role_ids = self.session.execute(
                        select(assoc_user_role.c.role_id)
                        .where(assoc_user_role.c.user_id == user_id)
                        .union(
                            select(assoc_group_role.c.role_id)
                            .join(assoc_user_group, assoc_user_group.c.group_id == assoc_group_role.c.group_id)
                            .where(assoc_user_group.c.user_id == user_id)
                        )
                    ).scalars().all()
                    role_ids = [role_id for role_id in role_ids if role_id is not None]
                    if not role_ids:
                        return set()
                    rows = (
                        self.session.query(self.viewmenu_model.name)
                        .join(self.permissionview_model)
                        .join(self.permission_model)
                        .join(assoc_permissionview_role)
                        .filter(self.permission_model.name == permission_name)
                        .filter(assoc_permissionview_role.c.role_id.in_(role_ids))
                    ).all()
                    return {row.name for row in rows}

            # sha256 of the lookup's source in each Superset release the override was compared with
            # (tests/superset-init/compare_permission_lookup.py). Any other source keeps Superset's own
            # lookup: an upgrade that changes who may read what never runs the older rule.
            _COMPARED_LOOKUPS = {
                "b2c316a97189a650972199e72a5c85a288c0df026381c8efdfb617296e5cb84e",  # 6.1.0
                "b6f3a09a472e511f5e1505896d1e082a8090a2b5f12f850df7a10011d9847ef4",  # 7.0.0rc2
            }
            try:
                _lookup = inspect.getsource(_security_manager.user_view_menu_names)
            except (OSError, TypeError):
                _lookup = ""
            if hashlib.sha256(_lookup.encode()).hexdigest() in _COMPARED_LOOKUPS:
                CUSTOM_SECURITY_MANAGER = HopsworksSecurityManager
            else:
                logging.getLogger("hopsworks").warning(
                    "Superset's permission lookup differs from the releases the Hopsworks lookup was "
                    "compared with: Superset's own lookup is in use, which is slow on a cluster with "
                    "many project members."
                )
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
          tag: 6.1.0.1
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
          enabled: false
          initContainers:
          - command:
            - /bin/sh
            - -c
            - |
              until dockerize -wait "tcp://$DB_HOST:$DB_PORT" -timeout 120s; do
                echo "Waiting for the Superset database at $DB_HOST:$DB_PORT"
                sleep 5
              done
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
          resources:
            limits:
              cpu: '1'
              memory: 2Gi
            requests:
              cpu: 250m
              memory: 512Mi
        initImage:
          pullPolicy: IfNotPresent
          repository: docker.hops.works/superset/dockerize
          tag: 0.14.0-alpine-h3.2
        initialization:
          enabled: true
          timeoutSeconds: 1800
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
            tag: 7.4.11-alpine-h4
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
              tag: 1.90.0-alpine-h3.1
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
        serviceAccount:
          create: true
        supersetCeleryBeat:
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
          - command:
            - /bin/bash
            - -c
            - |
              {{- if .Values.initialization.enabled }}
              exec kubectl wait --namespace {{ .Release.Namespace | quote }} \
                --for=condition=complete --timeout={{ .Values.initialization.timeoutSeconds }}s \
                job/{{ include "superset.initialization.jobName" . }}
              {{- end }}
            image: '{{- $image := include "hopsworkslib.toolboxImage" . -}}{{ $image }}{{ include "hopsworkslib.imageDigest" (dict "global" .Values.global "entry" $image) }}'
            imagePullPolicy: '{{ include "hopsworkslib.imagePullPolicy" . | default "IfNotPresent" }}'
            name: wait-for-initialization
            resources:
              limits:
                cpu: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.limits.cpu }}'
                memory: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.limits.memory }}'
              requests:
                cpu: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.requests.cpu }}'
                memory: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.requests.memory }}'
            securityContext:
              allowPrivilegeEscalation: false
              capabilities:
                drop:
                - ALL
          podSecurityContext:
            runAsNonRoot: true
            seccompProfile:
              type: RuntimeDefault
          resources:
            limits:
              cpu: 250m
              memory: 768Mi
            requests:
              cpu: 100m
              memory: 768Mi
        supersetCeleryFlower:
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
          - command:
            - /bin/bash
            - -c
            - |
              {{- if .Values.initialization.enabled }}
              exec kubectl wait --namespace {{ .Release.Namespace | quote }} \
                --for=condition=complete --timeout={{ .Values.initialization.timeoutSeconds }}s \
                job/{{ include "superset.initialization.jobName" . }}
              {{- end }}
            image: '{{- $image := include "hopsworkslib.toolboxImage" . -}}{{ $image }}{{ include "hopsworkslib.imageDigest" (dict "global" .Values.global "entry" $image) }}'
            imagePullPolicy: '{{ include "hopsworkslib.imagePullPolicy" . | default "IfNotPresent" }}'
            name: wait-for-initialization
            resources:
              limits:
                cpu: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.limits.cpu }}'
                memory: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.limits.memory }}'
              requests:
                cpu: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.requests.cpu }}'
                memory: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.requests.memory }}'
            securityContext:
              allowPrivilegeEscalation: false
              capabilities:
                drop:
                - ALL
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
          - command:
            - /bin/bash
            - -c
            - |
              {{- if .Values.initialization.enabled }}
              exec kubectl wait --namespace {{ .Release.Namespace | quote }} \
                --for=condition=complete --timeout={{ .Values.initialization.timeoutSeconds }}s \
                job/{{ include "superset.initialization.jobName" . }}
              {{- end }}
            image: '{{- $image := include "hopsworkslib.toolboxImage" . -}}{{ $image }}{{ include "hopsworkslib.imageDigest" (dict "global" .Values.global "entry" $image) }}'
            imagePullPolicy: '{{ include "hopsworkslib.imagePullPolicy" . | default "IfNotPresent" }}'
            name: wait-for-initialization
            resources:
              limits:
                cpu: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.limits.cpu }}'
                memory: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.limits.memory }}'
              requests:
                cpu: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.requests.cpu }}'
                memory: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.requests.memory }}'
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
          - command:
            - /bin/bash
            - -c
            - |
              {{- if .Values.initialization.enabled }}
              exec kubectl wait --namespace {{ .Release.Namespace | quote }} \
                --for=condition=complete --timeout={{ .Values.initialization.timeoutSeconds }}s \
                job/{{ include "superset.initialization.jobName" . }}
              {{- end }}
            image: '{{- $image := include "hopsworkslib.toolboxImage" . -}}{{ $image }}{{ include "hopsworkslib.imageDigest" (dict "global" .Values.global "entry" $image) }}'
            imagePullPolicy: '{{ include "hopsworkslib.imagePullPolicy" . | default "IfNotPresent" }}'
            name: wait-for-initialization
            resources:
              limits:
                cpu: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.limits.cpu }}'
                memory: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.limits.memory }}'
              requests:
                cpu: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.requests.cpu }}'
                memory: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.requests.memory }}'
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
              memory: 2048Mi
            requests:
              cpu: 500m
              memory: 2048Mi
    ```

<div class="hops-values" markdown>

`superset.superset` <a class="headerlink" href="#helm.superset.superset" title="Permanent link">#</a> { #helm.superset.superset }
:   Type `object`, passed to the [`superset` 0.15.0](https://artifacthub.io/packages/helm/superset/superset/0.15.0) chart, whose other values are documented there.
    override superset values

    ??? note "Default"

        ```yaml
        _publicRoleDefaultName: Public
        allowAnonymousAccess: true
        configOverrides:
          databaseInitialization: |
            # Only the initialization Job creates security tables.
            FAB_CREATE_DB = os.getenv("SUPERSET_INIT_DB", "false").lower() == "true"
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
          mcp: |
            # Read only by the MCP service (templates/mcp.yaml), the one pod with MCP_JWT_SECRET. Without
            # it the service refuses to start rather than serve unauthenticated.
            MCP_AUTH_ENABLED = True
            MCP_JWT_ALGORITHM = "HS256"
            MCP_JWT_SECRET = os.getenv("MCP_JWT_SECRET")
            MCP_JWT_ISSUER = "hopsworks"
            MCP_JWT_AUDIENCE = "superset-mcp"
            MCP_DEV_USERNAME = None
            # Set only in the MCP pod, which serves HTTPS with them (templates/mcp.yaml).
            MCP_SSL_CERTFILE = os.getenv("MCP_SSL_CERTFILE")
            MCP_SSL_KEYFILE = os.getenv("MCP_SSL_KEYFILE")
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
          security_manager: |
            import hashlib
            import inspect
            import logging

            from flask import g
            from flask_appbuilder.security.sqla.models import (
                assoc_group_role,
                assoc_permissionview_role,
                assoc_user_group,
                assoc_user_role,
            )
            from sqlalchemy import select
            from superset.security import SupersetSecurityManager
            from superset.utils.core import get_user_id

            # A security manager set by an earlier override stays the base class.
            _security_manager = globals().get("CUSTOM_SECURITY_MANAGER") or SupersetSecurityManager

            class HopsworksSecurityManager(_security_manager):
                def user_view_menu_names(self, permission_name):
                    """The names Superset's lookup returns, read from the same tables in the same request.

                    Superset tests the user's roles with a correlated EXISTS on every granted permission,
                    so MySQL reads all of ab_permission_view_role on each call, and a request makes
                    several. Hopsworks adds a role and its grants per project member, so that table grows
                    with the cluster. Here the user's role ids are read first and passed as literals,
                    which lets MySQL start from idx_role_id and read only the user's grants.
                    """
                    if g.user.is_anonymous or self.is_guest_user():
                        return super().user_view_menu_names(permission_name)
                    user_id = get_user_id()
                    role_ids = self.session.execute(
                        select(assoc_user_role.c.role_id)
                        .where(assoc_user_role.c.user_id == user_id)
                        .union(
                            select(assoc_group_role.c.role_id)
                            .join(assoc_user_group, assoc_user_group.c.group_id == assoc_group_role.c.group_id)
                            .where(assoc_user_group.c.user_id == user_id)
                        )
                    ).scalars().all()
                    role_ids = [role_id for role_id in role_ids if role_id is not None]
                    if not role_ids:
                        return set()
                    rows = (
                        self.session.query(self.viewmenu_model.name)
                        .join(self.permissionview_model)
                        .join(self.permission_model)
                        .join(assoc_permissionview_role)
                        .filter(self.permission_model.name == permission_name)
                        .filter(assoc_permissionview_role.c.role_id.in_(role_ids))
                    ).all()
                    return {row.name for row in rows}

            # sha256 of the lookup's source in each Superset release the override was compared with
            # (tests/superset-init/compare_permission_lookup.py). Any other source keeps Superset's own
            # lookup: an upgrade that changes who may read what never runs the older rule.
            _COMPARED_LOOKUPS = {
                "b2c316a97189a650972199e72a5c85a288c0df026381c8efdfb617296e5cb84e",  # 6.1.0
                "b6f3a09a472e511f5e1505896d1e082a8090a2b5f12f850df7a10011d9847ef4",  # 7.0.0rc2
            }
            try:
                _lookup = inspect.getsource(_security_manager.user_view_menu_names)
            except (OSError, TypeError):
                _lookup = ""
            if hashlib.sha256(_lookup.encode()).hexdigest() in _COMPARED_LOOKUPS:
                CUSTOM_SECURITY_MANAGER = HopsworksSecurityManager
            else:
                logging.getLogger("hopsworks").warning(
                    "Superset's permission lookup differs from the releases the Hopsworks lookup was "
                    "compared with: Superset's own lookup is in use, which is slow on a cluster with "
                    "many project members."
                )
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
          tag: 6.1.0.1
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
          enabled: false
          initContainers:
          - command:
            - /bin/sh
            - -c
            - |
              until dockerize -wait "tcp://$DB_HOST:$DB_PORT" -timeout 120s; do
                echo "Waiting for the Superset database at $DB_HOST:$DB_PORT"
                sleep 5
              done
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
          resources:
            limits:
              cpu: '1'
              memory: 2Gi
            requests:
              cpu: 250m
              memory: 512Mi
        initImage:
          pullPolicy: IfNotPresent
          repository: docker.hops.works/superset/dockerize
          tag: 0.14.0-alpine-h3.2
        initialization:
          enabled: true
          timeoutSeconds: 1800
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
            tag: 7.4.11-alpine-h4
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
              tag: 1.90.0-alpine-h3.1
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
        serviceAccount:
          create: true
        supersetCeleryBeat:
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
          - command:
            - /bin/bash
            - -c
            - |
              {{- if .Values.initialization.enabled }}
              exec kubectl wait --namespace {{ .Release.Namespace | quote }} \
                --for=condition=complete --timeout={{ .Values.initialization.timeoutSeconds }}s \
                job/{{ include "superset.initialization.jobName" . }}
              {{- end }}
            image: '{{- $image := include "hopsworkslib.toolboxImage" . -}}{{ $image }}{{ include "hopsworkslib.imageDigest" (dict "global" .Values.global "entry" $image) }}'
            imagePullPolicy: '{{ include "hopsworkslib.imagePullPolicy" . | default "IfNotPresent" }}'
            name: wait-for-initialization
            resources:
              limits:
                cpu: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.limits.cpu }}'
                memory: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.limits.memory }}'
              requests:
                cpu: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.requests.cpu }}'
                memory: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.requests.memory }}'
            securityContext:
              allowPrivilegeEscalation: false
              capabilities:
                drop:
                - ALL
          podSecurityContext:
            runAsNonRoot: true
            seccompProfile:
              type: RuntimeDefault
          resources:
            limits:
              cpu: 250m
              memory: 768Mi
            requests:
              cpu: 100m
              memory: 768Mi
        supersetCeleryFlower:
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
          - command:
            - /bin/bash
            - -c
            - |
              {{- if .Values.initialization.enabled }}
              exec kubectl wait --namespace {{ .Release.Namespace | quote }} \
                --for=condition=complete --timeout={{ .Values.initialization.timeoutSeconds }}s \
                job/{{ include "superset.initialization.jobName" . }}
              {{- end }}
            image: '{{- $image := include "hopsworkslib.toolboxImage" . -}}{{ $image }}{{ include "hopsworkslib.imageDigest" (dict "global" .Values.global "entry" $image) }}'
            imagePullPolicy: '{{ include "hopsworkslib.imagePullPolicy" . | default "IfNotPresent" }}'
            name: wait-for-initialization
            resources:
              limits:
                cpu: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.limits.cpu }}'
                memory: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.limits.memory }}'
              requests:
                cpu: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.requests.cpu }}'
                memory: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.requests.memory }}'
            securityContext:
              allowPrivilegeEscalation: false
              capabilities:
                drop:
                - ALL
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
          - command:
            - /bin/bash
            - -c
            - |
              {{- if .Values.initialization.enabled }}
              exec kubectl wait --namespace {{ .Release.Namespace | quote }} \
                --for=condition=complete --timeout={{ .Values.initialization.timeoutSeconds }}s \
                job/{{ include "superset.initialization.jobName" . }}
              {{- end }}
            image: '{{- $image := include "hopsworkslib.toolboxImage" . -}}{{ $image }}{{ include "hopsworkslib.imageDigest" (dict "global" .Values.global "entry" $image) }}'
            imagePullPolicy: '{{ include "hopsworkslib.imagePullPolicy" . | default "IfNotPresent" }}'
            name: wait-for-initialization
            resources:
              limits:
                cpu: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.limits.cpu }}'
                memory: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.limits.memory }}'
              requests:
                cpu: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.requests.cpu }}'
                memory: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.requests.memory }}'
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
          - command:
            - /bin/bash
            - -c
            - |
              {{- if .Values.initialization.enabled }}
              exec kubectl wait --namespace {{ .Release.Namespace | quote }} \
                --for=condition=complete --timeout={{ .Values.initialization.timeoutSeconds }}s \
                job/{{ include "superset.initialization.jobName" . }}
              {{- end }}
            image: '{{- $image := include "hopsworkslib.toolboxImage" . -}}{{ $image }}{{ include "hopsworkslib.imageDigest" (dict "global" .Values.global "entry" $image) }}'
            imagePullPolicy: '{{ include "hopsworkslib.imagePullPolicy" . | default "IfNotPresent" }}'
            name: wait-for-initialization
            resources:
              limits:
                cpu: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.limits.cpu }}'
                memory: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.limits.memory }}'
              requests:
                cpu: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.requests.cpu }}'
                memory: '{{ (include "hopsworkslib.initContainerResources" (dict "Values" .Values) | fromYaml).resources.requests.memory }}'
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
              memory: 2048Mi
            requests:
              cpu: 500m
              memory: 2048Mi
        ```

`superset.superset.fullnameOverride` <a class="headerlink" href="#helm.superset.superset.fullnameOverride" title="Permanent link">#</a> { #helm.superset.superset.fullnameOverride }
:   Type `string`, default `"hopsworks-superset"`.
    Provide a name to override the full names of resources

`superset.superset.init.enabled` <a class="headerlink" href="#helm.superset.superset.init.enabled" title="Permanent link">#</a> { #helm.superset.superset.init.enabled }
:   Type `bool`, default `false`.
    The upstream hook stays disabled; use initialization.enabled to control the parent Job.

`superset.superset.initialization` <a class="headerlink" href="#helm.superset.superset.initialization" title="Permanent link">#</a> { #helm.superset.superset.initialization }
:   Type `object`, default `{"enabled":true,"timeoutSeconds":1800}`.
    Metadata initialization Job and runtime startup gates, shared by Helm, Argo CD and Flux.

`superset.superset.initialization.enabled` <a class="headerlink" href="#helm.superset.superset.initialization.enabled" title="Permanent link">#</a> { #helm.superset.superset.initialization.enabled }
:   Type `bool`, default `true`.
    Disable only when the metadata database is initialized outside this chart.

`superset.superset.initialization.timeoutSeconds` <a class="headerlink" href="#helm.superset.superset.initialization.timeoutSeconds" title="Permanent link">#</a> { #helm.superset.superset.initialization.timeoutSeconds }
:   Type `int`, default `1800`.
    Timeout for runtime startup gates and initialization Lease acquisition, in seconds.

`superset.superset.runAsUser` <a class="headerlink" href="#helm.superset.superset.runAsUser" title="Permanent link">#</a> { #helm.superset.superset.runAsUser }
:   Type `int`, default `1000`.
    User ID directive. This user must have enough permissions to run the bootstrap script Running containers as root is not recommended in production. Change this to another UID - e.g. 1000 to be more secure

`superset.superset.serviceAccount.create` <a class="headerlink" href="#helm.superset.superset.serviceAccount.create" title="Permanent link">#</a> { #helm.superset.superset.serviceAccount.create }
:   Type `bool`, default `true`.
    Create a ServiceAccount for Superset, so the initialization Role is not bound to the namespace's `default` account.

</div>

<!-- END GENERATED VALUES -->
