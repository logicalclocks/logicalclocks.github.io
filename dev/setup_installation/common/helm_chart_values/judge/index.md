# Judge values { #helm-values-judge }

Values under `judge` configure Judge, the active cluster arbitrator service.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.2.0-alpha-1791557095` (Hopsworks `5.2.0`)._

Deployed when [`global._hopsworks.full_platform`](global.md#helm.global._hopsworks.full_platform) is `true`.

??? example "Defaults as YAML"

    ```yaml
    judge:
      enabled: false
      hopsworkslib: {}
      image:
        name: /hopsworks/nginx
        pullPolicy: IfNotPresent
        registry: test-registry:6000
        tag: stable-bookworm
      ingress:
        annotations: {}
        className: nginx
        host: judge.hopsworks.ai
      nodeSelector: {}
      port: 8080
      regions:
        active: eu
        replica: us
      replicaCount: 1
      resources:
        limits:
          cpu: 10m
          memory: 70M
        requests:
          cpu: 5m
          memory: 50M
      serviceAccount:
        name: hopsworks-judge
      serviceName: hopsworks-judge
      tolerations: []
      topologySpreadConstraint: {}
    ```

<div class="hops-values" markdown>

`judge` <a class="headerlink" href="#helm.judge" title="Permanent link">#</a> { #helm.judge }
:   Type `object`, default `{}`.
    override judge values

`judge.enabled` <a class="headerlink" href="#helm.judge.enabled" title="Permanent link">#</a> { #helm.judge.enabled }
:   Type `bool`, default `false`.

`judge.hopsworkslib` <a class="headerlink" href="#helm.judge.hopsworkslib" title="Permanent link">#</a> { #helm.judge.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`judge.image.name` <a class="headerlink" href="#helm.judge.image.name" title="Permanent link">#</a> { #helm.judge.image.name }
:   Type `string`, default `"/hopsworks/nginx"`.

`judge.image.pullPolicy` <a class="headerlink" href="#helm.judge.image.pullPolicy" title="Permanent link">#</a> { #helm.judge.image.pullPolicy }
:   Type `string`, default `"IfNotPresent"`.

`judge.image.registry` <a class="headerlink" href="#helm.judge.image.registry" title="Permanent link">#</a> { #helm.judge.image.registry }
:   Type `string`, default `"test-registry:6000"`.

`judge.image.tag` <a class="headerlink" href="#helm.judge.image.tag" title="Permanent link">#</a> { #helm.judge.image.tag }
:   Type `string`, default `"stable-bookworm"`.

`judge.ingress.annotations` <a class="headerlink" href="#helm.judge.ingress.annotations" title="Permanent link">#</a> { #helm.judge.ingress.annotations }
:   Type `object`, default `{}`.
    ingress annotations

`judge.ingress.className` <a class="headerlink" href="#helm.judge.ingress.className" title="Permanent link">#</a> { #helm.judge.ingress.className }
:   Type `string`, default `"nginx"`.
    Name of the class implementing the Ingress controller

`judge.ingress.host` <a class="headerlink" href="#helm.judge.ingress.host" title="Permanent link">#</a> { #helm.judge.ingress.host }
:   Type `string`, default `"judge.hopsworks.ai"`.
    Rule for host based routing

`judge.nodeSelector` <a class="headerlink" href="#helm.judge.nodeSelector" title="Permanent link">#</a> { #helm.judge.nodeSelector }
:   Type `object`, default `{}`.
    This ensures that Kubernetes schedules pods only onto nodes that match all the specified labels.

`judge.port` <a class="headerlink" href="#helm.judge.port" title="Permanent link">#</a> { #helm.judge.port }
:   Type `int`, default `8080`.
    Port Judge will be listening on internally

`judge.regions.active` <a class="headerlink" href="#helm.judge.regions.active" title="Permanent link">#</a> { #helm.judge.regions.active }
:   Type `string`, default `"eu"`.
    Active region identifier

`judge.regions.replica` <a class="headerlink" href="#helm.judge.regions.replica" title="Permanent link">#</a> { #helm.judge.regions.replica }
:   Type `string`, default `"us"`.
    Replica region identifier

`judge.replicaCount` <a class="headerlink" href="#helm.judge.replicaCount" title="Permanent link">#</a> { #helm.judge.replicaCount }
:   Type `int`, default `1`.

`judge.resources.limits.cpu` <a class="headerlink" href="#helm.judge.resources.limits.cpu" title="Permanent link">#</a> { #helm.judge.resources.limits.cpu }
:   Type `string`, default `"10m"`.

`judge.resources.limits.memory` <a class="headerlink" href="#helm.judge.resources.limits.memory" title="Permanent link">#</a> { #helm.judge.resources.limits.memory }
:   Type `string`, default `"70M"`.

`judge.resources.requests.cpu` <a class="headerlink" href="#helm.judge.resources.requests.cpu" title="Permanent link">#</a> { #helm.judge.resources.requests.cpu }
:   Type `string`, default `"5m"`.

`judge.resources.requests.memory` <a class="headerlink" href="#helm.judge.resources.requests.memory" title="Permanent link">#</a> { #helm.judge.resources.requests.memory }
:   Type `string`, default `"50M"`.

`judge.serviceAccount.name` <a class="headerlink" href="#helm.judge.serviceAccount.name" title="Permanent link">#</a> { #helm.judge.serviceAccount.name }
:   Type `string`, default `"hopsworks-judge"`.

`judge.serviceName` <a class="headerlink" href="#helm.judge.serviceName" title="Permanent link">#</a> { #helm.judge.serviceName }
:   Type `string`, default `"hopsworks-judge"`.

`judge.tolerations` <a class="headerlink" href="#helm.judge.tolerations" title="Permanent link">#</a> { #helm.judge.tolerations }
:   Type `list`, default `[]`.
    These tolerations allow Kubernetes to schedule pods on nodes with matching taints, ensuring proper placement based on cluster policies.

`judge.topologySpreadConstraint` <a class="headerlink" href="#helm.judge.topologySpreadConstraint" title="Permanent link">#</a> { #helm.judge.topologySpreadConstraint }
:   Type `object`, default `{}`.
    The default topology spread constraint. If not defined the global topology spread constraint would be used instead.

</div>

<!-- END GENERATED VALUES -->
