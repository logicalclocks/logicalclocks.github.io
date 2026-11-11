# LLM Gateway values { #helm-values-hw-envoy-ai-gateway }

Values under `hw-envoy-gateway.aiGateway` configure the LLM Gateway controller, its mutating webhook and the hook that applies its CustomResourceDefinitions.
They ship in the `hw-envoy-gateway` subchart, whose other values are listed in [Envoy Gateway values][helm-values-hw-envoy-gateway], and are used when `global._hopsworks.envoyGateway.aiGateway.enabled` is true (off by default).
The AI Gateway itself, its policies and its tracing are configured under `kserve.envoyGateway.aiGateway` in [KServe values][helm-values-kserve], and the trace collector and table under `hopsworks.agentRouter` in [Hopsworks values][helm-values-hopsworks].
See [LLM Gateway][llm-gateway] for what the feature installs and what the cluster needs.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.3.0-alpha-1794391025` (Hopsworks `5.3.0`)._

## aiGateway { #helm-values-hw-envoy-ai-gateway-aigateway }

??? example "Defaults as YAML"

    ```yaml
    hw-envoy-gateway:
      aiGateway:
        controller:
          image:
            registry: ''
            repository: envoyproxy/ai-gateway-controller
            tag: v1.2.0
          imagePullPolicy: IfNotPresent
          logLevel: info
          nodeSelector: {}
          replicas: 1
          resources:
            limits:
              cpu: '1'
              memory: 512Mi
            requests:
              cpu: 100m
              memory: 128Mi
          runAsGroup: 1000
          runAsUser: 1000
          serviceAccount:
            annotations: {}
          tolerations: []
        crdImage:
          name: envoy-ai-gateway-crds
          registry: ''
          tag: v1.2.0-h1
        extProc:
          image:
            registry: ''
            repository: envoyproxy/ai-gateway-extproc
            tag: v1.2.0
          imagePullPolicy: IfNotPresent
          logLevel: info
        rateLimit:
          image:
            registry: ''
            repository: envoyproxy/ratelimit
            tag: 0482748e
          imagePullPolicy: IfNotPresent
          nodeSelector: {}
          platformAssignedIds: false
          redis:
            image:
              registry: ''
              repository: superset/redis
              tag: 7.4.11-alpine-h4
            imagePullPolicy: IfNotPresent
            maxMemory: 128mb
            nodeSelector: {}
            podDisruptionBudget:
              minAvailable: 0
            resources:
              limits:
                cpu: 500m
                memory: 192Mi
              requests:
                cpu: 50m
                memory: 192Mi
            runAsGroup: 1001
            runAsUser: 1001
            tolerations: []
          replicas: 1
          resources:
            limits:
              cpu: '1'
              memory: 512Mi
            requests:
              cpu: 100m
              memory: 128Mi
          tolerations: []
        requestHeaderAttributes:
          metrics: x-hopsworks-user:hopsworks.user
          span: agent-session-id:session.id,x-hopsworks-user:hopsworks.user,x-hopsworks-project-id:hopsworks.project.id
    ```

<div class="hops-values" markdown>

`hw-envoy-gateway.aiGateway` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway }
:   Type `object`.
    the LLM Gateway controller, Agent Router (previously Envoy AI Gateway): it turns AIGatewayRoutes into the routes and the ext_proc sidecar of the AI Gateway in the kserve subchart. Rendered only with global._hopsworks.envoyGateway.aiGateway.enabled, which also wires it into the Envoy Gateway configuration. The templates are vendored from the upstream ai-gateway-helm chart (see UPSTREAM.md); its CRDs are applied by a hook Job from crdImage.

    ??? note "Default"

        ```yaml
        controller:
          image:
            registry: ''
            repository: envoyproxy/ai-gateway-controller
            tag: v1.2.0
          imagePullPolicy: IfNotPresent
          logLevel: info
          nodeSelector: {}
          replicas: 1
          resources:
            limits:
              cpu: '1'
              memory: 512Mi
            requests:
              cpu: 100m
              memory: 128Mi
          runAsGroup: 1000
          runAsUser: 1000
          serviceAccount:
            annotations: {}
          tolerations: []
        crdImage:
          name: envoy-ai-gateway-crds
          registry: ''
          tag: v1.2.0-h1
        extProc:
          image:
            registry: ''
            repository: envoyproxy/ai-gateway-extproc
            tag: v1.2.0
          imagePullPolicy: IfNotPresent
          logLevel: info
        rateLimit:
          image:
            registry: ''
            repository: envoyproxy/ratelimit
            tag: 0482748e
          imagePullPolicy: IfNotPresent
          nodeSelector: {}
          platformAssignedIds: false
          redis:
            image:
              registry: ''
              repository: superset/redis
              tag: 7.4.11-alpine-h4
            imagePullPolicy: IfNotPresent
            maxMemory: 128mb
            nodeSelector: {}
            podDisruptionBudget:
              minAvailable: 0
            resources:
              limits:
                cpu: 500m
                memory: 192Mi
              requests:
                cpu: 50m
                memory: 192Mi
            runAsGroup: 1001
            runAsUser: 1001
            tolerations: []
          replicas: 1
          resources:
            limits:
              cpu: '1'
              memory: 512Mi
            requests:
              cpu: 100m
              memory: 128Mi
          tolerations: []
        requestHeaderAttributes:
          metrics: x-hopsworks-user:hopsworks.user
          span: agent-session-id:session.id,x-hopsworks-user:hopsworks.user,x-hopsworks-project-id:hopsworks.project.id
        ```

`hw-envoy-gateway.aiGateway.controller` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.controller" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.controller }
:   Type `object`.
    the controller (the ai-gateway-controller Deployment). It reconciles the AIGatewayRoutes the backend writes, answers Envoy Gateway's extension-manager calls on port 1063 and injects the ext_proc sidecar into the AI Gateway's Envoy pods through a mutating webhook.

    ??? note "Default"

        ```yaml
        image:
          registry: ''
          repository: envoyproxy/ai-gateway-controller
          tag: v1.2.0
        imagePullPolicy: IfNotPresent
        logLevel: info
        nodeSelector: {}
        replicas: 1
        resources:
          limits:
            cpu: '1'
            memory: 512Mi
          requests:
            cpu: 100m
            memory: 128Mi
        runAsGroup: 1000
        runAsUser: 1000
        serviceAccount:
          annotations: {}
        tolerations: []
        ```

`hw-envoy-gateway.aiGateway.controller.image` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.controller.image" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.controller.image }
:   Type `object`, default `{"registry":"","repository":"envoyproxy/ai-gateway-controller","tag":"v1.2.0"}`.
    the controller image, a mirror of the Docker Hub image envoyproxy/ai-gateway-controller under the Hopsworks registry at the same path. The tag is the upstream Agent Router release (Chart.yaml annotation hopsworks.ai/agent-router-version) and equals extProc.image.tag.

`hw-envoy-gateway.aiGateway.controller.image.registry` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.controller.image.registry" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.controller.image.registry }
:   Type `string`, default `""`.
    registry prefix; empty means global._hopsworks.imageRegistry

`hw-envoy-gateway.aiGateway.controller.imagePullPolicy` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.controller.imagePullPolicy" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.controller.imagePullPolicy }
:   Type `string`, default `"IfNotPresent"`.
    pull policy of the controller image; global._hopsworks.imagePullPolicy takes precedence when set

`hw-envoy-gateway.aiGateway.controller.logLevel` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.controller.logLevel" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.controller.logLevel }
:   Type `string`, default `"info"`.
    log level of the controller

`hw-envoy-gateway.aiGateway.controller.nodeSelector` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.controller.nodeSelector" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.controller.nodeSelector }
:   Type `object`, default `{}`.
    nodeSelector of the controller; falls back to global._hopsworks.nodeSelector

`hw-envoy-gateway.aiGateway.controller.replicas` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.controller.replicas" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.controller.replicas }
:   Type `int`, default `1`.
    replicas of the controller. Leader election is on, so more than one is safe.

`hw-envoy-gateway.aiGateway.controller.resources` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.controller.resources" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.controller.resources }
:   Type `object`.
    resources of the controller container

    ??? note "Default"

        ```yaml
        limits:
          cpu: '1'
          memory: 512Mi
        requests:
          cpu: 100m
          memory: 128Mi
        ```

`hw-envoy-gateway.aiGateway.controller.runAsGroup` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.controller.runAsGroup" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.controller.runAsGroup }
:   Type `int`, default `1000`.
    group id (and fsGroup) of the controller pod, as runAsUser

`hw-envoy-gateway.aiGateway.controller.runAsUser` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.controller.runAsUser" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.controller.runAsUser }
:   Type `int`, default `1000`.
    user id of the controller pod when global._hopsworks.securityContextEnabled is on. Upstream pins 65532, the image's own user; the default here is the chart-wide 1000, as for the Envoy Gateway controller.

`hw-envoy-gateway.aiGateway.controller.serviceAccount.annotations` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.controller.serviceAccount.annotations" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.controller.serviceAccount.annotations }
:   Type `object`, default `{}`.
    annotations of the controller's service account, merged over global._hopsworks.serviceAccountAnnotations

`hw-envoy-gateway.aiGateway.controller.tolerations` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.controller.tolerations" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.controller.tolerations }
:   Type `list`, default `[]`.
    tolerations of the controller; fall back to global._hopsworks.tolerations

`hw-envoy-gateway.aiGateway.crdImage` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.crdImage" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.crdImage }
:   Type `object`, default `{"name":"envoy-ai-gateway-crds","registry":"","tag":"v1.2.0-h1"}`.
    the image that carries the six LLM Gateway CRDs (docker-images envoy-ai-gateway-crds, on the hwutils toolbox image). They are 2 MB and cannot ship in the chart (the release Secret cap, see crdImage above), so a second install and upgrade hook applies them server-side. The tag starts with the upstream Agent Router release followed by an image revision.

`hw-envoy-gateway.aiGateway.crdImage.registry` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.crdImage.registry" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.crdImage.registry }
:   Type `string`, default `""`.
    registry prefix; empty means global._hopsworks.imageRegistry plus the hopsworks project

`hw-envoy-gateway.aiGateway.extProc` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.extProc" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.extProc }
:   Type `object`.
    the ext_proc sidecar the controller injects into the AI Gateway's Envoy pods. Only its image and log level are set here, as controller arguments; its resources and, on OpenShift, its security context come from the GatewayConfig the kserve subchart applies (kserve.envoyGateway.aiGateway.extProc).

    ??? note "Default"

        ```yaml
        image:
          registry: ''
          repository: envoyproxy/ai-gateway-extproc
          tag: v1.2.0
        imagePullPolicy: IfNotPresent
        logLevel: info
        ```

`hw-envoy-gateway.aiGateway.extProc.image` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.extProc.image" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.extProc.image }
:   Type `object`, default `{"registry":"","repository":"envoyproxy/ai-gateway-extproc","tag":"v1.2.0"}`.
    the ext_proc image, a mirror of the Docker Hub image envoyproxy/ai-gateway-extproc under the Hopsworks registry at the same path. No pod of the release runs it before the first AIGatewayRoute exists, so the image-list action reads it from the controller's arguments.

`hw-envoy-gateway.aiGateway.extProc.image.registry` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.extProc.image.registry" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.extProc.image.registry }
:   Type `string`, default `""`.
    registry prefix; empty means global._hopsworks.imageRegistry

`hw-envoy-gateway.aiGateway.extProc.imagePullPolicy` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.extProc.imagePullPolicy" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.extProc.imagePullPolicy }
:   Type `string`, default `"IfNotPresent"`.
    pull policy of the ext_proc image

`hw-envoy-gateway.aiGateway.extProc.logLevel` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.extProc.logLevel" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.extProc.logLevel }
:   Type `string`, default `"info"`.
    log level of the ext_proc sidecar

`hw-envoy-gateway.aiGateway.rateLimit` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.rateLimit" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.rateLimit }
:   Type `object`.
    the global rate limit of the AI Gateway: the rate limit service Envoy Gateway deploys on demand (rateLimit and rateLimitDeployment in its configuration) and the Redis it counts in. Limits are written per project by the Hopsworks backend as BackendTrafficPolicies. Without Redis or the service, requests pass unlimited (fail open, Envoy Gateway's default): a limit is a guard against runaway use, not a security boundary.

    ??? note "Default"

        ```yaml
        image:
          registry: ''
          repository: envoyproxy/ratelimit
          tag: 0482748e
        imagePullPolicy: IfNotPresent
        nodeSelector: {}
        platformAssignedIds: false
        redis:
          image:
            registry: ''
            repository: superset/redis
            tag: 7.4.11-alpine-h4
          imagePullPolicy: IfNotPresent
          maxMemory: 128mb
          nodeSelector: {}
          podDisruptionBudget:
            minAvailable: 0
          resources:
            limits:
              cpu: 500m
              memory: 192Mi
            requests:
              cpu: 50m
              memory: 192Mi
          runAsGroup: 1001
          runAsUser: 1001
          tolerations: []
        replicas: 1
        resources:
          limits:
            cpu: '1'
            memory: 512Mi
          requests:
            cpu: 100m
            memory: 128Mi
        tolerations: []
        ```

`hw-envoy-gateway.aiGateway.rateLimit.image` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.rateLimit.image" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.rateLimit.image }
:   Type `object`, default `{"registry":"","repository":"envoyproxy/ratelimit","tag":"0482748e"}`.
    the rate limit service image, a mirror of the Docker Hub image envoyproxy/ratelimit under the Hopsworks registry at the same path. The tag is the one Envoy Gateway v1.9.2 defaults to. Envoy Gateway creates the Deployment and Service (envoy-ratelimit) itself, from this and the settings below, once the first policy refers to it.

`hw-envoy-gateway.aiGateway.rateLimit.image.registry` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.rateLimit.image.registry" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.rateLimit.image.registry }
:   Type `string`, default `""`.
    registry prefix; empty means global._hopsworks.imageRegistry

`hw-envoy-gateway.aiGateway.rateLimit.imagePullPolicy` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.rateLimit.imagePullPolicy" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.rateLimit.imagePullPolicy }
:   Type `string`, default `"IfNotPresent"`.
    pull policy of the rate limit image; global._hopsworks.imagePullPolicy takes precedence when set

`hw-envoy-gateway.aiGateway.rateLimit.nodeSelector` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.rateLimit.nodeSelector" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.rateLimit.nodeSelector }
:   Type `object`, default `{}`.
    nodeSelector of the rate limit pod; falls back to global._hopsworks.nodeSelector

`hw-envoy-gateway.aiGateway.rateLimit.platformAssignedIds` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.rateLimit.platformAssignedIds" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.rateLimit.platformAssignedIds }
:   Type `bool`, default `false`.
    leave the user and group ids of the rate limit pod to the platform. Envoy Gateway runs it as 65534, which OpenShift's restricted-v2 refuses unless the namespace range holds it; values.openshift.yaml turns this on.

`hw-envoy-gateway.aiGateway.rateLimit.redis` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.rateLimit.redis" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.rateLimit.redis }
:   Type `object`.
    the Redis the rate limit service counts in: a Deployment and a Service in the release namespace, with no persistence. Every counter key carries an expiry, so a restart only resets the current windows.

    ??? note "Default"

        ```yaml
        image:
          registry: ''
          repository: superset/redis
          tag: 7.4.11-alpine-h4
        imagePullPolicy: IfNotPresent
        maxMemory: 128mb
        nodeSelector: {}
        podDisruptionBudget:
          minAvailable: 0
        resources:
          limits:
            cpu: 500m
            memory: 192Mi
          requests:
            cpu: 50m
            memory: 192Mi
        runAsGroup: 1001
        runAsUser: 1001
        tolerations: []
        ```

`hw-envoy-gateway.aiGateway.rateLimit.redis.image` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.rateLimit.redis.image" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.rateLimit.redis.image }
:   Type `object`, default `{"registry":"","repository":"superset/redis","tag":"7.4.11-alpine-h4"}`.
    the Redis image, the one Superset runs (docker-images superset/redis, upstream alpine Redis) under the Hopsworks registry. The entrypoint is upstream's; only its arguments are set.

`hw-envoy-gateway.aiGateway.rateLimit.redis.image.registry` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.rateLimit.redis.image.registry" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.rateLimit.redis.image.registry }
:   Type `string`, default `""`.
    registry prefix; empty means global._hopsworks.imageRegistry

`hw-envoy-gateway.aiGateway.rateLimit.redis.imagePullPolicy` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.rateLimit.redis.imagePullPolicy" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.rateLimit.redis.imagePullPolicy }
:   Type `string`, default `"IfNotPresent"`.
    pull policy of the Redis image; global._hopsworks.imagePullPolicy takes precedence when set

`hw-envoy-gateway.aiGateway.rateLimit.redis.maxMemory` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.rateLimit.redis.maxMemory" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.rateLimit.redis.maxMemory }
:   Type `string`, default `"128mb"`.
    `maxmemory` of Redis. Keep it below the memory limit: the policy evicts keys that have an expiry, soonest first, and writes fail once only keys without one are left.

`hw-envoy-gateway.aiGateway.rateLimit.redis.nodeSelector` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.rateLimit.redis.nodeSelector" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.rateLimit.redis.nodeSelector }
:   Type `object`, default `{}`.
    nodeSelector of the Redis pod; falls back to global._hopsworks.nodeSelector

`hw-envoy-gateway.aiGateway.rateLimit.redis.podDisruptionBudget` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.rateLimit.redis.podDisruptionBudget" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.rateLimit.redis.podDisruptionBudget }
:   Type `object`, default `{"minAvailable":0}`.
    PodDisruptionBudget of the Redis pod; minAvailable 0 renders none

`hw-envoy-gateway.aiGateway.rateLimit.redis.resources` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.rateLimit.redis.resources" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.rateLimit.redis.resources }
:   Type `object`.
    resources of the Redis container

    ??? note "Default"

        ```yaml
        limits:
          cpu: 500m
          memory: 192Mi
        requests:
          cpu: 50m
          memory: 192Mi
        ```

`hw-envoy-gateway.aiGateway.rateLimit.redis.runAsGroup` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.rateLimit.redis.runAsGroup" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.rateLimit.redis.runAsGroup }
:   Type `int`, default `1001`.
    group id (and fsGroup) of the Redis pod, as runAsUser

`hw-envoy-gateway.aiGateway.rateLimit.redis.runAsUser` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.rateLimit.redis.runAsUser" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.rateLimit.redis.runAsUser }
:   Type `int`, default `1001`.
    user id of the Redis pod when global._hopsworks.securityContextEnabled is on; the image's own redis user is 999, the Superset Redis runs as 1001

`hw-envoy-gateway.aiGateway.rateLimit.redis.tolerations` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.rateLimit.redis.tolerations" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.rateLimit.redis.tolerations }
:   Type `list`, default `[]`.
    tolerations of the Redis pod; fall back to global._hopsworks.tolerations

`hw-envoy-gateway.aiGateway.rateLimit.replicas` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.rateLimit.replicas" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.rateLimit.replicas }
:   Type `int`, default `1`.
    replicas of the rate limit service. The counters live in Redis, so more than one is safe.

`hw-envoy-gateway.aiGateway.rateLimit.resources` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.rateLimit.resources" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.rateLimit.resources }
:   Type `object`.
    resources of the rate limit container

    ??? note "Default"

        ```yaml
        limits:
          cpu: '1'
          memory: 512Mi
        requests:
          cpu: 100m
          memory: 128Mi
        ```

`hw-envoy-gateway.aiGateway.rateLimit.tolerations` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.rateLimit.tolerations" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.rateLimit.tolerations }
:   Type `list`, default `[]`.
    tolerations of the rate limit pod; fall back to global._hopsworks.tolerations

`hw-envoy-gateway.aiGateway.requestHeaderAttributes` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.requestHeaderAttributes" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.requestHeaderAttributes }
:   Type `object`.
    the arguments of the controller that attribute traces and metrics to the caller. Each entry is `<request header>:<attribute>`; the ext_proc sidecar copies the header's value onto the span (spanRequestHeaderAttributes) or onto the gen_ai metrics as a label (metricsRequestHeaderAttributes). The headers are set by model-serving-authenticator. Metric labels multiply the series, so the metrics list holds only the user, whose values are bounded by the project members.

    ??? note "Default"

        ```yaml
        metrics: x-hopsworks-user:hopsworks.user
        span: agent-session-id:session.id,x-hopsworks-user:hopsworks.user,x-hopsworks-project-id:hopsworks.project.id
        ```

`hw-envoy-gateway.aiGateway.requestHeaderAttributes.metrics` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.requestHeaderAttributes.metrics" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.requestHeaderAttributes.metrics }
:   Type `string`, default `"x-hopsworks-user:hopsworks.user"`.
    metric labels, comma-separated; empty drops the flag

`hw-envoy-gateway.aiGateway.requestHeaderAttributes.span` <a class="headerlink" href="#helm.hw-envoy-gateway.aiGateway.requestHeaderAttributes.span" title="Permanent link">#</a> { #helm.hw-envoy-gateway.aiGateway.requestHeaderAttributes.span }
:   Type `string`.
    span attributes, comma-separated

    ??? note "Default"

        ```yaml
        agent-session-id:session.id,x-hopsworks-user:hopsworks.user,x-hopsworks-project-id:hopsworks.project.id
        ```

</div>

<!-- END GENERATED VALUES -->
