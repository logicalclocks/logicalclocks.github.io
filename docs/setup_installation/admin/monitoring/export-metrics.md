# Exporting Hopsworks metrics

## Introduction
Hopsworks services produce metrics which are centrally gathered by [Prometheus](https://prometheus.io/) and visualized in [Grafana](../grafana).
Although the system is self-contained, it is possible to export these metrics to third-party services or another Prometheus instance.

## Prerequisites
In order to configure Prometheus to export metrics you need `root` SSH access to either Hopsworks or to the target server depending on the export method you choose below.

## Exporting metrics
Prometheus can be configured to export metrics to another Prometheus instance (cross-service federation) or to a custom service which knows how to handle them.

### Prometheus federation
Prometheus servers can be federated to scale better or to just clone all metrics (cross-service federation). Prometheus federation is well [documented](https://prometheus.io/docs/prometheus/latest/federation/#cross-service-federation)
but there are some specificities to Hopsworks.

In the guide below we assume **Prometheus A** is the service running in Hopsworks and **Prometheus B** is the server you want to clone metrics to.

#### Step 1
**Prometheus B** needs to be able to connect to TCP port `9089` of **Prometheus B** to scrape metrics. If you have any firewall (or Security Group) in place, allow ingress for that port.

#### Step 2
SSH into **Prometheus B** server, edit Prometheus configuration file and add the following under the `scrape_configs`

!!! note
    Replace IP_ADDRESS with the actual address of Hopsworks server

```yaml
- job_name: 'federate'
    scrape_interval: 15s

    honor_labels: true
    metrics_path: '/federate'

    params:
      'match[]':
        - '{job="airflow"}'
        - '{job="pushgateway"}'
        - '{job="hadoop"}'
        - '{job="hopsworks"}'

    static_configs:
      - targets:
        - 'IP_ADDRESS:9089'
```

These are the basic labels gathered by Hopsworks.

* If your Hopsworks cluster runs **without** Kubernetes append `'{job="cadvisor"}'` to `match[]` list

* If your Hopsworks cluster runs **with** Kubernetes append the following labels to `match[]`
    * `'{job=~"knative.+"}'`
    * `'{job="kubernetes-cadvisor"}'`
    * `'{job="istio-envoy"}'`
    * `'{job="kube-state-metrics"}'`
    * `'{job="cadvisor"}'`
    * `'{job="cadvisor"}'`
    * `'{job="cadvisor"}'`

#### Step 3
Finally restart Prometheus service with `sudo systemctl restart prometheus`

### Custom service
Prometheus can push metrics to another custom resource via HTTP. The custom service is responsible for handling the received metrics.
To push metrics with this method we use the `remote_write` configuration.


We will only give a sample configuration as `remote_write` is extensively documented in Prometheus [documentation](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write)
In the example below we push metrics to a custom service listening on port 9096 which transforms the metrics and forwards them.

```yaml
remote_write:
  - url: "http://localhost:9096"
    queue_config:
      capacity: 10000
      max_samples_per_send: 5000
      batch_send_deadline: 60s
```

## Conclusion
In this guide we showed how you can push metrics outside of Hopsworks cluster using two methods, (a) federated Prometheus or (b) remote write to a custom service. This configuration is useful if you
already have a centralized monitoring system with alerts already configured.