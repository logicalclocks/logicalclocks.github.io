# Helm chart values reference

This section lists every value you can configure when deploying Hopsworks with the Hopsworks Helm chart, with one page per top-level key.
It is generated from the `README.md` files of the chart and its subcharts, and for RonDB from the `values.schema.json` of the RonDB chart that Hopsworks pins.
On a released version of the docs it matches the Hopsworks Helm chart for that release; on the development docs it reflects the latest chart published to the development channel.

You set these values in the `values.<cloud>.yaml` file that you pass to `helm install`.
For a guided, end-to-end setup, follow one of the cloud installation guides, such as the [AWS getting started guide][aws-getting-started-with-eks].
Only a small subset of these values is needed for a typical install: "Common values" below lists the ones the cloud installation guides set, and the pages are the exhaustive reference.

"All values" lists the pages.
Each page states when its subchart is deployed: when the condition names several values, Helm uses the first one that is set.
"Upstream charts" are the charts a subchart installs from other Helm repositories, and each link opens a chart's documentation for the version Hopsworks pins.
A page lists only the values Hopsworks sets for its upstream charts, except the RonDB page, which lists all of the RonDB chart's values.
A default is the value Hopsworks deploys: the root chart's settings for a subchart are applied over the subchart's own defaults.
Every value has its own link (the `#` next to its key), and each section has its defaults as a values file under "Defaults as YAML".

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.2.0-alpha-1791640691` (Hopsworks `5.2.0`)._

## Common values { #helm-values-common }

| Value | What it sets |
| --- | --- |
| [`global._hopsworks.cloudProvider`](global.md#helm.global._hopsworks.cloudProvider) | The cloud the cluster runs on; HopsFS, Consul and Hopsworks configure themselves from it. |
| [`global._hopsworks.storageClassName`](global.md#helm.global._hopsworks.storageClassName) | The storage class of every persistent volume. |
| [`global._hopsworks.imageRegistry`](global.md#helm.global._hopsworks.imageRegistry) | The registry the Hopsworks images are pulled from. |
| [`global._hopsworks.imagePullSecrets`](global.md#helm.global._hopsworks.imagePullSecrets) | The pull secrets for that registry. |
| [`global._hopsworks.managedDockerRegistery`](global.md#helm.global._hopsworks.managedDockerRegistery) | Use the cloud provider's container registry for the images Hopsworks builds for users. |
| [`global._hopsworks.managedObjectStorage`](global.md#helm.global._hopsworks.managedObjectStorage) | Use a cloud bucket for HopsFS data and for the RonDB and OpenSearch backups. |
| [`global._hopsworks.minio.enabled`](global.md#helm.global._hopsworks.minio.enabled) | Deploy MinIO in the cluster; turn it off when a cloud bucket is used. |
| [`global._hopsworks.externalLoadBalancers.enabled`](global.md#helm.global._hopsworks.externalLoadBalancers.enabled) | Expose services through LoadBalancer Services. |
| [`hopsworks.ingress.host`](hopsworks.md#helm.hopsworks.ingress.host) | The host name of the Hopsworks UI and API. |
| [`hopsworks.ingress.ingressClassName`](hopsworks.md#helm.hopsworks.ingress.ingressClassName) | The ingress controller that serves it. |
| [`hopsworks.velero.backup.enabled`](hopsworks.md#helm.hopsworks.velero.backup.enabled) | Back up Kubernetes resources with Velero, which needs its own install. |
| [`rondb.rondb.clusterSize`](rondb.md#helm.rondb.rondb.clusterSize) | The size of the RonDB cluster: data replicas, node groups, MySQL and REST API servers. |

## All values { #helm-values-pages }

| Values | Upstream charts | Keys |
| --- | --- | --- |
| [`global`][helm-values-global] |  | 145 |
| [`airflow`][helm-values-airflow] |  | 151 |
| [`arrowflight`][helm-values-arrowflight] |  | 46 |
| [`certs-operator`][helm-values-certs-operator] |  | 29 |
| [`consul`][helm-values-consul] | [`consul` 1.8.16](https://artifacthub.io/packages/helm/hashicorp/consul/1.8.16) | 24 |
| [`docker-registry`][helm-values-docker-registry] |  | 90 |
| [`grafana`][helm-values-grafana] | [`grafana` 7.0.17](https://artifacthub.io/packages/helm/grafana/grafana/7.0.17) | 7 |
| [`hive`][helm-values-hive] |  | 78 |
| [`hopsfs`][helm-values-hopsfs] |  | 221 |
| [`hopsfs-csi`][helm-values-hopsfs-csi] |  | 29 |
| [`hopsworks`][helm-values-hopsworks] |  | 935 |
| [`hw-kueue`][helm-values-hw-kueue] | [`kueue` 0.12.2](https://github.com/kubernetes-sigs/kueue/blob/v0.12.2/charts/kueue/README.md) | 94 |
| [`hw-kyverno`][helm-values-hw-kyverno] |  | 58 |
| [`judge`][helm-values-judge] |  | 23 |
| [`kafka`][helm-values-kafka] | [`strimzi-kafka-operator` 1.2.0](https://artifacthub.io/packages/helm/strimzi/strimzi-kafka-operator/1.2.0) | 102 |
| [`kserve`][helm-values-kserve] |  | 266 |
| [`minio`][helm-values-minio] |  | 42 |
| [`olk`][helm-values-olk] | [`prometheus-elasticsearch-exporter` 5.8.0](https://artifacthub.io/packages/helm/prometheus-community/prometheus-elasticsearch-exporter/5.8.0) | 164 |
| [`onlinefs`][helm-values-onlinefs] |  | 93 |
| [`prometheus`][helm-values-prometheus] | [`prometheus` 25.20.2](https://artifacthub.io/packages/helm/prometheus-community/prometheus/25.20.2), [`prometheus-adapter` 4.11.0](https://artifacthub.io/packages/helm/prometheus-community/prometheus-adapter/4.11.0) | 9 |
| [`ray`][helm-values-ray] | [`kuberay-operator` 1.4.0](https://artifacthub.io/packages/helm/kuberay-operator/kuberay-operator/1.4.0) | 2 |
| [`rondb`][helm-values-rondb] | [`rondb` 26.2.21](https://github.com/logicalclocks/rondb-helm/blob/v26.2.21/values.schema.json) | 464 |
| [`spark`][helm-values-spark] | [`spark-operator` 2.5.1](https://github.com/kubeflow/spark-operator/blob/v2.5.1/charts/spark-operator-chart/README.md) | 160 |
| [`superset`][helm-values-superset] | [`mysql` 12.3.5](https://artifacthub.io/packages/helm/bitnami/mysql/12.3.5), [`superset` 0.15.0](https://artifacthub.io/packages/helm/superset/superset/0.15.0) | 25 |
| [`trino`][helm-values-trino] | [`trino` 1.41.0](https://artifacthub.io/packages/helm/trino/trino/1.41.0) | 38 |
| [`vpa`][helm-values-vpa] |  | 18 |

## Other values { #helm-values-other }

??? example "Defaults as YAML"

    ```yaml
    hopsworkslib: {}
    ```

<div class="hops-values" markdown>

`hopsworkslib` <a class="headerlink" href="#helm.hopsworkslib" title="Permanent link">#</a> { #helm.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

</div>

<!-- END GENERATED VALUES -->
