# Dedicated node pools { #dedicated-node-pools }

## Introduction

This guide pins the Hopsworks services to dedicated node pools.
The example uses three pools:

- **Head** nodes run the platform services.
- **Database** nodes run the RonDB data nodes and nothing else.
- **Worker** nodes run user workloads, such as jobs and notebooks, and the image preset of the internal docker registry.

The head and database nodes are tainted, so only pods that tolerate the taint schedule there.
The worker nodes are labelled but not tainted, so user workloads, which carry no toleration, land on them.

The values below pin every Hopsworks workload, the installation and upgrade Jobs included, with three exceptions that schedule on the worker nodes:

- The Consul chart's TLS and gossip encryption setup Jobs, which run on every install and upgrade, and its TLS cleanup Job, which runs on uninstall; that chart takes no placement settings for them.
- The Kueue controller, when Kueue is enabled, whose chart takes no placement settings.
- The installation and maintenance Jobs of the Hopsworks subcharts before 5.2.2, which do not read the global settings there.

The DaemonSets (Filebeat, the HopsFS CSI node plugin and the registry configurer) tolerate every taint and run on all nodes.

## Label and taint the nodes

```bash
kubectl label nodes head-node-1 head-node-n node=Head
kubectl taint nodes head-node-1 head-node-n node=Head:NoSchedule
kubectl label nodes db-node-1 db-node-n node=RonDB
kubectl taint nodes db-node-1 db-node-n node=RonDB:NoSchedule
kubectl label nodes worker-node-1 worker-node-n node=Worker
```

## Values

`global._hopsworks.nodeSelector` and `global._hopsworks.tolerations` apply to every Hopsworks subchart that reads the globals, so they send the platform services to the head nodes.
The upstream charts listed after them do not read the globals and get the same settings directly, through YAML anchors:

- RonDB takes a setting per node type, which sends its data nodes (`ndbmtd`) to the database nodes and every other type to the head nodes.
- Consul takes its `nodeSelector` and `tolerations` as multi-line strings rather than as YAML.
- The Superset chart's top-level settings apply to its web, worker and init pods, and its MySQL and Redis take their own.
- KEDA's top-level settings apply to its operator, metrics server and webhooks, and its HTTP add-on takes one setting per component.
- Trino takes a setting for the coordinator and the workers, and another for the coordinator that tests user catalogs.

```yaml
global:
  _hopsworks:
    nodeSelector: &nodeSelector
      node: Head
    tolerations: &tolerations
      - key: "node"
        operator: "Equal"
        value: "Head"
        effect: "NoSchedule"

rondb:
  rondb:
    nodeSelector:
      mgmd: *nodeSelector
      mysqld: *nodeSelector
      rdrs: *nodeSelector
      backup: *nodeSelector
      ndbmtd:
        node: RonDB
    tolerations:
      mgmd: *tolerations
      mysqld: *tolerations
      rdrs: *tolerations
      backup: *tolerations
      ndbmtd:
        - key: "node"
          operator: "Equal"
          value: "RonDB"
          effect: "NoSchedule"

hopsworks:
  dockerRegistry:
    preset:
      nodeSelector:
        node: Worker

consul:
  consul:
    global:
      acls:
        nodeSelector: |
          node: Head
        tolerations: |
          - key: "node"
            operator: "Equal"
            value: "Head"
            effect: "NoSchedule"
    server:
      nodeSelector: |
        node: Head
      tolerations: |
        - key: "node"
          operator: "Equal"
          value: "Head"
          effect: "NoSchedule"
    syncCatalog:
      nodeSelector: |
        node: Head
      tolerations: |
        - key: "node"
          operator: "Equal"
          value: "Head"
          effect: "NoSchedule"

kafka:
  strimzi-kafka-operator:
    nodeSelector: *nodeSelector
    tolerations: *tolerations

olk:
  prometheus-elasticsearch-exporter:
    nodeSelector: *nodeSelector
    tolerations: *tolerations

grafana:
  grafana:
    nodeSelector: *nodeSelector
    tolerations: *tolerations

prometheus:
  prometheus:
    server:
      nodeSelector: *nodeSelector
      tolerations: *tolerations
    alertmanager:
      nodeSelector: *nodeSelector
      tolerations: *tolerations
    prometheus-pushgateway:
      nodeSelector: *nodeSelector
      tolerations: *tolerations
    kube-state-metrics:
      nodeSelector: *nodeSelector
      tolerations: *tolerations
  prometheus-adapter:
    nodeSelector: *nodeSelector
    tolerations: *tolerations

spark:
  spark-operator:
    webhook:
      nodeSelector: *nodeSelector
      tolerations: *tolerations
    controller:
      nodeSelector: *nodeSelector
      tolerations: *tolerations
    sparkOperatorUpgradeJob:
      nodeSelector: *nodeSelector
      tolerations: *tolerations
    hook:
      nodeSelector: *nodeSelector
      tolerations: *tolerations
  historyServer:
    nodeSelector: *nodeSelector
    tolerations: *tolerations

trino:
  trino:
    coordinator:
      nodeSelector: *nodeSelector
      tolerations: *tolerations
    worker:
      nodeSelector: *nodeSelector
      tolerations: *tolerations
  trinotest:
    coordinator:
      nodeSelector: *nodeSelector
      tolerations: *tolerations

superset:
  superset:
    nodeSelector: *nodeSelector
    tolerations: *tolerations
    redis:
      master:
        nodeSelector: *nodeSelector
        tolerations: *tolerations
  mysql:
    primary:
      nodeSelector: *nodeSelector
      tolerations: *tolerations

hw-keda:
  keda:
    nodeSelector: *nodeSelector
    tolerations: *tolerations
  keda-add-ons-http:
    operator:
      nodeSelector: *nodeSelector
      tolerations: *tolerations
    interceptor:
      nodeSelector: *nodeSelector
      tolerations: *tolerations
    scaler:
      nodeSelector: *nodeSelector
      tolerations: *tolerations

ray:
  kuberay-operator:
    nodeSelector: *nodeSelector
    tolerations: *tolerations
```

A subchart setting overrides the global one, so the same pattern moves a single service to another pool.
