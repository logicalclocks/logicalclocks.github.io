# Grafana values { #helm-values-grafana }

Values under `grafana` configure Grafana and the Hopsworks monitoring dashboards.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.2.0-alpha-1791369399` (Hopsworks `5.2.0`)._

Deployed when [`global._hopsworks.full_platform`](global.md#helm.global._hopsworks.full_platform) is `true`.

!!! info "Upstream charts"

    - Values under `grafana.grafana` go to [`grafana` 7.0.17](https://artifacthub.io/packages/helm/grafana/grafana/7.0.17) from `https://grafana.github.io/helm-charts`.

    Only the values Hopsworks sets under `grafana.grafana` are listed on this page.
    Any other value of the chart can be set there too; the link opens its documentation for the version Hopsworks pins.

??? example "Defaults as YAML"

    ```yaml
    grafana:
      dependencies:
        prometheus:
          consulServiceName: prometheus
          consulServiceTag: prometheus
          port: 9090
      grafana:
        dashboardProviders:
          dashboardproviders.yaml:
            apiVersion: 1
            providers:
            - disableDeletion: true
              editable: false
              folder: Apps
              name: Apps
              options:
                path: /usr/share/grafana/dashboards/apps
              type: file
              updateIntervalSeconds: 10
            - disableDeletion: true
              editable: false
              folder: Hops
              name: Hops
              options:
                path: /usr/share/grafana/dashboards/hops
              type: file
              updateIntervalSeconds: 10
            - disableDeletion: false
              editable: false
              folder: RonDB
              name: RonDB
              options:
                path: /usr/share/grafana/dashboards/rondb
              type: file
              updateIntervalSeconds: 10
            - disableDeletion: true
              editable: false
              folder: Overview
              name: Overview
              options:
                path: /usr/share/grafana/dashboards/overview
              type: file
              updateIntervalSeconds: 10
            - disableDeletion: true
              editable: false
              folder: Kubernetes
              name: Kubernetes
              options:
                path: /usr/share/grafana/dashboards/kubernetes
              type: file
              updateIntervalSeconds: 10
            - disableDeletion: true
              editable: false
              folder: ModelServing
              name: ModelServing
              options:
                path: /usr/share/grafana/dashboards/kserve
              type: file
              updateIntervalSeconds: 10
            - disableDeletion: true
              editable: false
              folder: Ray
              name: Ray
              options:
                path: /usr/share/grafana/dashboards/ray
              type: file
              updateIntervalSeconds: 10
            - disableDeletion: true
              editable: false
              folder: RSS
              name: RemoteShuffleService
              options:
                path: /usr/share/grafana/dashboards/rss
              type: file
              updateIntervalSeconds: 10
        dashboardsConfigMaps: {}
        datasources:
          datasources.yaml:
            apiVersion: 1
            datasources:
            - access: proxy
              editable: false
              isDefault: true
              name: Prometheus
              type: prometheus
              url: http://prometheus.prometheus.service.consul:9090
        downloadDashboardsImage:
          pullPolicy: IfNotPresent
          registry: docker.hops.works
          repository: hopsworks/hwutils
          sha: ''
          tag: 1.10-SNAPSHOT
        extraConfigmapMounts:
        - configMap: '{{ include "hopsworks.grafana.conditionalProvidersName" . }}'
          mountPath: /etc/grafana/provisioning/dashboards/hopsworks-dashboardproviders.yaml
          name: hopsworks-dashboardproviders
          readOnly: true
          subPath: providers.yaml
        extraInitContainers:
        - command:
          - /bin/sh
          - -c
          - |
            set -eu
            checked=0
            for f in /etc/grafana/provisioning/dashboards/*.yaml; do
              [ -f "$f" ] || continue
              for p in $(sed -n 's/^[[:space:]]*path:[[:space:]]*//p' "$f"); do
                case "$p" in
                  /usr/share/grafana/dashboards/*) ;;
                  *) echo "skip: $p is delivered by Helm, not by the image"; continue ;;
                esac
                checked=$((checked + 1))
                n=$(find "$p" -name '*.json' 2>/dev/null | wc -l)
                if [ "$n" -eq 0 ]; then
                  echo "FATAL: dashboard provider path $p (declared in $f) holds no dashboards."
                  echo "The Hopsworks dashboards ship inside the Grafana image. This image does not"
                  echo "carry them, so Grafana would start healthy with an empty dashboard list."
                  echo "Use an image built with the dashboards, or override grafana.image.tag."
                  exit 1
                fi
                echo "ok: $p ($n dashboards)"
              done
            done
            if [ "$checked" -eq 0 ]; then
              echo "FATAL: no image dashboard provider paths found in /etc/grafana/provisioning/dashboards."
              echo "The chart always declares providers under /usr/share/grafana/dashboards, so either"
              echo "the provisioning files did not reach this container or every provider was replaced."
              exit 1
            fi
            echo "verified $checked image dashboard provider paths"
          image: '{{ .Values.global.imageRegistry | default .Values.image.registry }}/{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}'
          imagePullPolicy: '{{ .Values.image.pullPolicy }}'
          name: verify-dashboards
          resources:
            limits:
              cpu: 100m
              memory: 64Mi
            requests:
              cpu: 10m
              memory: 32Mi
          securityContext:
            allowPrivilegeEscalation: false
            capabilities:
              drop:
              - ALL
            readOnlyRootFilesystem: true
            seccompProfile:
              type: RuntimeDefault
          volumeMounts:
          - mountPath: /etc/grafana/provisioning/dashboards/dashboardproviders.yaml
            name: config
            subPath: dashboardproviders.yaml
          - mountPath: /etc/grafana/provisioning/dashboards/hopsworks-dashboardproviders.yaml
            name: hopsworks-dashboardproviders
            subPath: providers.yaml
        global:
          imageRegistry: docker.hops.works
        grafana.ini:
          auth:
            disable_login_form: true
            disable_signout_menu: true
          auth.anonymous:
            enabled: false
          auth.basic:
            enabled: false
          auth.proxy:
            auto_sign_up: true
            enable_login_token: false
            enabled: true
            header_name: X-WEBAUTH-USER
            header_property: username
            headers: Name:X-WEBAUTH-NAME Role:X-WEBAUTH-ROLE Email:X-WEBAUTH-EMAIL
            headers_encoded: false
            sync_ttl: '60'
            whitelist: null
          rbac:
            enabled: true
          security:
            admin_password: adminpw
            allow_embedding: true
            strict_transport_security: false
          server:
            enforce_domain: false
            root_url: /hopsworks-api/grafana
          users:
            allow_org_create: false
            allow_sign_up: false
            auto_assign_org: true
            auto_assign_org_id: '1'
            auto_assign_org_role: Viewer
            default_theme: dark
            editors_can_admin: false
            home_page: /dashboards
            verify_email_enabled: false
            viewers_can_edit: false
        image:
          tag: 12.4.9-h10
        nodeSelector: {}
        rbac:
          create: false
        resources:
          limits:
            cpu: 1
            memory: 1000Mi
          requests:
            cpu: 200m
            memory: 200Mi
        service:
          annotations:
            consul.hashicorp.com/service-name: grafana
            consul.hashicorp.com/service-tags: grafana
        tolerations: []
        topologySpreadConstraints:
        - labelSelector:
            matchLabels:
              app.kubernetes.io/instance: hopsworks
              app.kubernetes.io/name: grafana
          maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: ScheduleAnyway
      hopsworkslib: {}
    ```

<div class="hops-values" markdown>

`grafana` <a class="headerlink" href="#helm.grafana" title="Permanent link">#</a> { #helm.grafana }
:   Type `object`, default `{"grafana":{"global":{"imageRegistry":"docker.hops.works"}}}`.
    override grafana values

`grafana.dependencies.prometheus.consulServiceName` <a class="headerlink" href="#helm.grafana.dependencies.prometheus.consulServiceName" title="Permanent link">#</a> { #helm.grafana.dependencies.prometheus.consulServiceName }
:   Type `string`, default `"prometheus"`.

`grafana.dependencies.prometheus.consulServiceTag` <a class="headerlink" href="#helm.grafana.dependencies.prometheus.consulServiceTag" title="Permanent link">#</a> { #helm.grafana.dependencies.prometheus.consulServiceTag }
:   Type `string`, default `"prometheus"`.

`grafana.dependencies.prometheus.port` <a class="headerlink" href="#helm.grafana.dependencies.prometheus.port" title="Permanent link">#</a> { #helm.grafana.dependencies.prometheus.port }
:   Type `int`, default `9090`.

`grafana.grafana` <a class="headerlink" href="#helm.grafana.grafana" title="Permanent link">#</a> { #helm.grafana.grafana }
:   Type `object`, passed to the [`grafana` 7.0.17](https://artifacthub.io/packages/helm/grafana/grafana/7.0.17) chart, whose other values are documented there.
    override grafana values

    ??? note "Default"

        ```yaml
        dashboardProviders:
          dashboardproviders.yaml:
            apiVersion: 1
            providers:
            - disableDeletion: true
              editable: false
              folder: Apps
              name: Apps
              options:
                path: /usr/share/grafana/dashboards/apps
              type: file
              updateIntervalSeconds: 10
            - disableDeletion: true
              editable: false
              folder: Hops
              name: Hops
              options:
                path: /usr/share/grafana/dashboards/hops
              type: file
              updateIntervalSeconds: 10
            - disableDeletion: false
              editable: false
              folder: RonDB
              name: RonDB
              options:
                path: /usr/share/grafana/dashboards/rondb
              type: file
              updateIntervalSeconds: 10
            - disableDeletion: true
              editable: false
              folder: Overview
              name: Overview
              options:
                path: /usr/share/grafana/dashboards/overview
              type: file
              updateIntervalSeconds: 10
            - disableDeletion: true
              editable: false
              folder: Kubernetes
              name: Kubernetes
              options:
                path: /usr/share/grafana/dashboards/kubernetes
              type: file
              updateIntervalSeconds: 10
            - disableDeletion: true
              editable: false
              folder: ModelServing
              name: ModelServing
              options:
                path: /usr/share/grafana/dashboards/kserve
              type: file
              updateIntervalSeconds: 10
            - disableDeletion: true
              editable: false
              folder: Ray
              name: Ray
              options:
                path: /usr/share/grafana/dashboards/ray
              type: file
              updateIntervalSeconds: 10
            - disableDeletion: true
              editable: false
              folder: RSS
              name: RemoteShuffleService
              options:
                path: /usr/share/grafana/dashboards/rss
              type: file
              updateIntervalSeconds: 10
        dashboardsConfigMaps: {}
        datasources:
          datasources.yaml:
            apiVersion: 1
            datasources:
            - access: proxy
              editable: false
              isDefault: true
              name: Prometheus
              type: prometheus
              url: http://prometheus.prometheus.service.consul:9090
        downloadDashboardsImage:
          pullPolicy: IfNotPresent
          registry: docker.hops.works
          repository: hopsworks/hwutils
          sha: ''
          tag: 1.10-SNAPSHOT
        extraConfigmapMounts:
        - configMap: '{{ include "hopsworks.grafana.conditionalProvidersName" . }}'
          mountPath: /etc/grafana/provisioning/dashboards/hopsworks-dashboardproviders.yaml
          name: hopsworks-dashboardproviders
          readOnly: true
          subPath: providers.yaml
        extraInitContainers:
        - command:
          - /bin/sh
          - -c
          - |
            set -eu
            checked=0
            for f in /etc/grafana/provisioning/dashboards/*.yaml; do
              [ -f "$f" ] || continue
              for p in $(sed -n 's/^[[:space:]]*path:[[:space:]]*//p' "$f"); do
                case "$p" in
                  /usr/share/grafana/dashboards/*) ;;
                  *) echo "skip: $p is delivered by Helm, not by the image"; continue ;;
                esac
                checked=$((checked + 1))
                n=$(find "$p" -name '*.json' 2>/dev/null | wc -l)
                if [ "$n" -eq 0 ]; then
                  echo "FATAL: dashboard provider path $p (declared in $f) holds no dashboards."
                  echo "The Hopsworks dashboards ship inside the Grafana image. This image does not"
                  echo "carry them, so Grafana would start healthy with an empty dashboard list."
                  echo "Use an image built with the dashboards, or override grafana.image.tag."
                  exit 1
                fi
                echo "ok: $p ($n dashboards)"
              done
            done
            if [ "$checked" -eq 0 ]; then
              echo "FATAL: no image dashboard provider paths found in /etc/grafana/provisioning/dashboards."
              echo "The chart always declares providers under /usr/share/grafana/dashboards, so either"
              echo "the provisioning files did not reach this container or every provider was replaced."
              exit 1
            fi
            echo "verified $checked image dashboard provider paths"
          image: '{{ .Values.global.imageRegistry | default .Values.image.registry }}/{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}'
          imagePullPolicy: '{{ .Values.image.pullPolicy }}'
          name: verify-dashboards
          resources:
            limits:
              cpu: 100m
              memory: 64Mi
            requests:
              cpu: 10m
              memory: 32Mi
          securityContext:
            allowPrivilegeEscalation: false
            capabilities:
              drop:
              - ALL
            readOnlyRootFilesystem: true
            seccompProfile:
              type: RuntimeDefault
          volumeMounts:
          - mountPath: /etc/grafana/provisioning/dashboards/dashboardproviders.yaml
            name: config
            subPath: dashboardproviders.yaml
          - mountPath: /etc/grafana/provisioning/dashboards/hopsworks-dashboardproviders.yaml
            name: hopsworks-dashboardproviders
            subPath: providers.yaml
        global:
          imageRegistry: docker.hops.works
        grafana.ini:
          auth:
            disable_login_form: true
            disable_signout_menu: true
          auth.anonymous:
            enabled: false
          auth.basic:
            enabled: false
          auth.proxy:
            auto_sign_up: true
            enable_login_token: false
            enabled: true
            header_name: X-WEBAUTH-USER
            header_property: username
            headers: Name:X-WEBAUTH-NAME Role:X-WEBAUTH-ROLE Email:X-WEBAUTH-EMAIL
            headers_encoded: false
            sync_ttl: '60'
            whitelist: null
          rbac:
            enabled: true
          security:
            admin_password: adminpw
            allow_embedding: true
            strict_transport_security: false
          server:
            enforce_domain: false
            root_url: /hopsworks-api/grafana
          users:
            allow_org_create: false
            allow_sign_up: false
            auto_assign_org: true
            auto_assign_org_id: '1'
            auto_assign_org_role: Viewer
            default_theme: dark
            editors_can_admin: false
            home_page: /dashboards
            verify_email_enabled: false
            viewers_can_edit: false
        image:
          tag: 12.4.9-h10
        nodeSelector: {}
        rbac:
          create: false
        resources:
          limits:
            cpu: 1
            memory: 1000Mi
          requests:
            cpu: 200m
            memory: 200Mi
        service:
          annotations:
            consul.hashicorp.com/service-name: grafana
            consul.hashicorp.com/service-tags: grafana
        tolerations: []
        topologySpreadConstraints:
        - labelSelector:
            matchLabels:
              app.kubernetes.io/instance: hopsworks
              app.kubernetes.io/name: grafana
          maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: ScheduleAnyway
        ```

`grafana.hopsworkslib` <a class="headerlink" href="#helm.grafana.hopsworkslib" title="Permanent link">#</a> { #helm.grafana.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`grafana.grafana.dashboardsConfigMaps` <span class="hops-values-deprecated">Deprecated</span> <a class="headerlink" href="#helm.grafana.grafana.dashboardsConfigMaps" title="Permanent link">#</a> { #helm.grafana.grafana.dashboardsConfigMaps }
:   Type `object`, default `{}`.
    DEPRECATED and intentionally empty. The dashboards used to be inlined into nine ConfigMaps here, which put 1.9 MB of JSON into the rendered manifest and so into the 1 MiB Helm release Secret. They now ship in the Grafana image under /usr/share/grafana/dashboards and are provisioned by path. Kept as an empty map rather than removed so that an existing override does not become an unknown key.

</div>

<!-- END GENERATED VALUES -->
