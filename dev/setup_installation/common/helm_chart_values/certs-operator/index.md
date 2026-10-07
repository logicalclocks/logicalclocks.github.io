# Certs operator values { #helm-values-certs-operator }

Values under `certs-operator` configure the operator that issues the TLS certificates of the Hopsworks services and removes them on uninstall.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.2.0-alpha-1791370120` (Hopsworks `5.2.0`)._

Deployed when [`global._hopsworks.full_platform`](global.md#helm.global._hopsworks.full_platform) is `true`.

## General { #helm-values-certs-operator-general }

??? example "Defaults as YAML"

    ```yaml
    certs-operator:
      fullnameOverride: null
      gracefulCertTeardown:
        enabled: true
        timeoutSeconds: 120
        ttlSecondsAfterFinished: null
      hopsworkslib: {}
      nameOverride: null
      nodeSelector: {}
      serviceAccount:
        create: false
        name: ''
      tolerations: []
      topologySpreadConstraint: {}
    ```

<div class="hops-values" markdown>

`certs-operator` <a class="headerlink" href="#helm.certs-operator" title="Permanent link">#</a> { #helm.certs-operator }
:   Type `object`, default `{}`.
    override certs-operator values

`certs-operator.fullnameOverride` <a class="headerlink" href="#helm.certs-operator.fullnameOverride" title="Permanent link">#</a> { #helm.certs-operator.fullnameOverride }
:   Type `string`, default `nil`.
    override app fully qualified name 

`certs-operator.gracefulCertTeardown` <a class="headerlink" href="#helm.certs-operator.gracefulCertTeardown" title="Permanent link">#</a> { #helm.certs-operator.gracefulCertTeardown }
:   Type `object`, default `{"enabled":true,"timeoutSeconds":120,"ttlSecondsAfterFinished":null}`.
    ordered, narrow-RBAC teardown of HopsworksCerts on uninstall: a pre-delete hook deletes the certs while the certs-operator is still alive (so it releases its own finalizers), and a post-delete hook force-clears any finalizers left behind on runtimes that drop pre-delete hooks (ArgoCD < 3.3). Independent of the `wipe` job.

`certs-operator.gracefulCertTeardown.enabled` <a class="headerlink" href="#helm.certs-operator.gracefulCertTeardown.enabled" title="Permanent link">#</a> { #helm.certs-operator.gracefulCertTeardown.enabled }
:   Type `bool`, default `true`.
    enable the ordered HopsworksCert teardown hooks on uninstall

`certs-operator.gracefulCertTeardown.timeoutSeconds` <a class="headerlink" href="#helm.certs-operator.gracefulCertTeardown.timeoutSeconds" title="Permanent link">#</a> { #helm.certs-operator.gracefulCertTeardown.timeoutSeconds }
:   Type `int`, default `120`.
    seconds the pre-delete drain waits for the operator to finalize the certs before deferring to the post-delete backstop

`certs-operator.gracefulCertTeardown.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.certs-operator.gracefulCertTeardown.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.certs-operator.gracefulCertTeardown.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    ttlSecondsAfterFinished for the teardown Jobs; null falls through to the global default

`certs-operator.hopsworkslib` <a class="headerlink" href="#helm.certs-operator.hopsworkslib" title="Permanent link">#</a> { #helm.certs-operator.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`certs-operator.nameOverride` <a class="headerlink" href="#helm.certs-operator.nameOverride" title="Permanent link">#</a> { #helm.certs-operator.nameOverride }
:   Type `string`, default `nil`.
    override app chart name

`certs-operator.nodeSelector` <a class="headerlink" href="#helm.certs-operator.nodeSelector" title="Permanent link">#</a> { #helm.certs-operator.nodeSelector }
:   Type `object`, default `{}`.
    node selector configuration

`certs-operator.serviceAccount.create` <a class="headerlink" href="#helm.certs-operator.serviceAccount.create" title="Permanent link">#</a> { #helm.certs-operator.serviceAccount.create }
:   Type `bool`, default `false`.

`certs-operator.serviceAccount.name` <a class="headerlink" href="#helm.certs-operator.serviceAccount.name" title="Permanent link">#</a> { #helm.certs-operator.serviceAccount.name }
:   Type `string`, default `""`.

`certs-operator.tolerations` <a class="headerlink" href="#helm.certs-operator.tolerations" title="Permanent link">#</a> { #helm.certs-operator.tolerations }
:   Type `list`, default `[]`.

`certs-operator.topologySpreadConstraint` <a class="headerlink" href="#helm.certs-operator.topologySpreadConstraint" title="Permanent link">#</a> { #helm.certs-operator.topologySpreadConstraint }
:   Type `object`, default `{}`.
    The default topology spread constraint. If not defined the global topology spread constraint would be used instead.

</div>

## controller { #helm-values-certs-operator-controller }

??? example "Defaults as YAML"

    ```yaml
    certs-operator:
      controller:
        manager:
          resources:
            limits:
              cpu: 500m
              memory: 128Mi
            requests:
              cpu: 10m
              memory: 64Mi
          watchNamespaces: null
        serviceAccount:
          annotations: {}
    ```

<div class="hops-values" markdown>

`certs-operator.controller.manager.resources.limits.cpu` <a class="headerlink" href="#helm.certs-operator.controller.manager.resources.limits.cpu" title="Permanent link">#</a> { #helm.certs-operator.controller.manager.resources.limits.cpu }
:   Type `string`, default `"500m"`.

`certs-operator.controller.manager.resources.limits.memory` <a class="headerlink" href="#helm.certs-operator.controller.manager.resources.limits.memory" title="Permanent link">#</a> { #helm.certs-operator.controller.manager.resources.limits.memory }
:   Type `string`, default `"128Mi"`.

`certs-operator.controller.manager.resources.requests.cpu` <a class="headerlink" href="#helm.certs-operator.controller.manager.resources.requests.cpu" title="Permanent link">#</a> { #helm.certs-operator.controller.manager.resources.requests.cpu }
:   Type `string`, default `"10m"`.

`certs-operator.controller.manager.resources.requests.memory` <a class="headerlink" href="#helm.certs-operator.controller.manager.resources.requests.memory" title="Permanent link">#</a> { #helm.certs-operator.controller.manager.resources.requests.memory }
:   Type `string`, default `"64Mi"`.

`certs-operator.controller.manager.watchNamespaces` <a class="headerlink" href="#helm.certs-operator.controller.manager.watchNamespaces" title="Permanent link">#</a> { #helm.certs-operator.controller.manager.watchNamespaces }
:   Type `string`, default `nil`.
    Comma separated list of Namespaces to restrict certs-operator to watch for. If not set it will watch all Namespaces.

`certs-operator.controller.serviceAccount.annotations` <a class="headerlink" href="#helm.certs-operator.controller.serviceAccount.annotations" title="Permanent link">#</a> { #helm.certs-operator.controller.serviceAccount.annotations }
:   Type `object`, default `{}`.
    service account annotations

</div>

## dependencies { #helm-values-certs-operator-dependencies }

??? example "Defaults as YAML"

    ```yaml
    certs-operator:
      dependencies:
        ca:
          apiKeySecretKey: key
          apiKeySecretName: hopsworks-api-key-auth
          authMethod: api_key
          consulServiceName: glassfish
          consulServiceTag: ca
          httpScheme: https
          httpTimeout: 60s
          password: adminpw
          port: 8182
          user: agent@hops.io
    ```

<div class="hops-values" markdown>

`certs-operator.dependencies.ca.apiKeySecretKey` <a class="headerlink" href="#helm.certs-operator.dependencies.ca.apiKeySecretKey" title="Permanent link">#</a> { #helm.certs-operator.dependencies.ca.apiKeySecretKey }
:   Type `string`, default `"key"`.

`certs-operator.dependencies.ca.apiKeySecretName` <a class="headerlink" href="#helm.certs-operator.dependencies.ca.apiKeySecretName" title="Permanent link">#</a> { #helm.certs-operator.dependencies.ca.apiKeySecretName }
:   Type `string`, default `"hopsworks-api-key-auth"`.

`certs-operator.dependencies.ca.authMethod` <a class="headerlink" href="#helm.certs-operator.dependencies.ca.authMethod" title="Permanent link">#</a> { #helm.certs-operator.dependencies.ca.authMethod }
:   Type `string`, default `"api_key"`.

`certs-operator.dependencies.ca.consulServiceName` <a class="headerlink" href="#helm.certs-operator.dependencies.ca.consulServiceName" title="Permanent link">#</a> { #helm.certs-operator.dependencies.ca.consulServiceName }
:   Type `string`, default `"glassfish"`.

`certs-operator.dependencies.ca.consulServiceTag` <a class="headerlink" href="#helm.certs-operator.dependencies.ca.consulServiceTag" title="Permanent link">#</a> { #helm.certs-operator.dependencies.ca.consulServiceTag }
:   Type `string`, default `"ca"`.

`certs-operator.dependencies.ca.httpScheme` <a class="headerlink" href="#helm.certs-operator.dependencies.ca.httpScheme" title="Permanent link">#</a> { #helm.certs-operator.dependencies.ca.httpScheme }
:   Type `string`, default `"https"`.

`certs-operator.dependencies.ca.httpTimeout` <a class="headerlink" href="#helm.certs-operator.dependencies.ca.httpTimeout" title="Permanent link">#</a> { #helm.certs-operator.dependencies.ca.httpTimeout }
:   Type `string`, default `"60s"`.

`certs-operator.dependencies.ca.password` <a class="headerlink" href="#helm.certs-operator.dependencies.ca.password" title="Permanent link">#</a> { #helm.certs-operator.dependencies.ca.password }
:   Type `string`, default `"adminpw"`.

`certs-operator.dependencies.ca.port` <a class="headerlink" href="#helm.certs-operator.dependencies.ca.port" title="Permanent link">#</a> { #helm.certs-operator.dependencies.ca.port }
:   Type `int`, default `8182`.

`certs-operator.dependencies.ca.user` <a class="headerlink" href="#helm.certs-operator.dependencies.ca.user" title="Permanent link">#</a> { #helm.certs-operator.dependencies.ca.user }
:   Type `string`, default `"agent@hops.io"`.

</div>

<!-- END GENERATED VALUES -->
