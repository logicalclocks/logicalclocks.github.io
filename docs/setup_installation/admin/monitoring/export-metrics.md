# Exporting Hopsworks metrics

## Introduction
Hopsworks services produce metrics which are centrally gathered by [Prometheus](https://prometheus.io/) and visualized in [Grafana](../grafana).
Although the system is self-contained, it is possible for another *federated* Prometheus instance to scrape these metrics or directly push them to another system.
This is useful if you have a centralized monitoring system with already configured alerts.

## Prerequisites
In order to configure Prometheus to export metrics you need to have the right to change the remote Prometheus configuration.

## Exporting metrics
Prometheus can be configured to export metrics to another Prometheus instance (cross-service federation) or to a custom service which knows how to handle them.

### Prometheus federation
Prometheus servers can be federated to scale better or to just clone all metrics (cross-service federation).

In the guide below we assume **Prometheus A** is the service running in Hopsworks and **Prometheus B** is the server you want to clone metrics to.

#### Step 1
**Prometheus B** needs to be able to connect to TCP port `9090` of **Prometheus A** to scrape metrics. If you have any firewall (or Security Group) in place, allow ingress for that port.

#### Step 2
The next step is to expose **Prometheus A** running inside Hopsworks Kubernetes cluster. If **Prometheus B** has direct access to **Prometheus A** then you can skip this step.

We will create a Kubernetes *Service* of type *LoadBalancer* to expose port `9090`

!!!Warning
    If you need to apply custom **annotations**, then modify the Manifest below
    The example below assumes Hopsworks is **installed** at Namespace *hopsworks*

```bash
kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: prometheus-external
  namespace: hopsworks
  labels:
    app: prometheus
spec:
  type: LoadBalancer
  selector:
    app.kubernetes.io/name: prometheus
    app.kubernetes.io/component: server
  ports:
    - protocol: TCP
      port: 9090
      targetPort: 9090
EOF
```

Then we need to find the External IP address of the newly created Service

```bash
export NAMESPACE=hopsworks
kubectl -n $NAMESPACE get svc prometheus-external -ojsonpath='{.status.loadBalancer.ingress[0].ip}'
```

!!!Warning
    It will take a few seconds until an IP address is assigned to the Service

We will use this IP address in Step 2

#### Step 2
Edit the configuration file of **Prometheus B** server and append the following Job under `scrape_configs`

!!! note
    Replace IP_ADDRESS with the IP address from Step 1 or the IP address of Prometheus service if it is directly accessible.
    The snippet below assumes Hopsworks services runs at Namespace **hopsworks**

```yaml
- job_name: 'federate'
  scrape_interval: 15s

  honor_labels: true
  metrics_path: '/federate'

  params:
    'match[]':
      - '{namespace="hopsworks"}'

  static_configs:
    - targets:
      - 'IP_ADDRESS:9090'
```

The configuration above will scrape for services metrics under the *hopsworks* Namespace. If you want to additionally
scrape *user application* metrics then append `'{job="pushgateway"}'` to the matchers, for example:

```yaml
  params:
    'match[]':
      - '{namespace="hopsworks"}'
      - '{job="pushgateway"}'
```

Depending on the Prometheus setup you might need to restart **Prometheus B** service to pick up the new configuration.
For more details on federation visit Prometheus [documentation](https://prometheus.io/docs/prometheus/latest/federation/#cross-service-federation)

### Custom service
Prometheus can push metrics to another custom resource via HTTP. The custom service is responsible for handling the received metrics.
To push metrics with this method we use the `remote_write` configuration.

We will only give a sample configuration as `remote_write` is extensively documented in Prometheus [documentation](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write)
In the example below we push metrics to a custom service listening on port 9096 which transforms the metrics and forwards them.

#### Step 1
First we need to identify the name of the *ConfigMap* storing the Prometheus configuration. The guide assumes Hopsworks runs at
`hopsworks` Namespace.

```bash
export NAMESPACE=hopsworks
configMapName=$(kubectl -n ${NAMESPACE} get configmap -l app.kubernetes.io/name=prometheus,app.kubernetes.io/component=server -ojsonpath='{.items[0].metadata.name}')
```

#### Step 2
Using the name of the ConfigMap from Step 1 edit the configuration

```bash
kubectl -n ${NAMESPACE} edit configmap ${configMapName}
```

Find the key `prometheus.yml` and add the following

```yaml
remote_write:
  - url: "http://localhost:9096"
    queue_config:
      capacity: 10000
      max_samples_per_send: 5000
      batch_send_deadline: 60s
```

Save your changes, Prometheus will automatically reload the new configuration.