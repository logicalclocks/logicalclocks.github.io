---
description: Put the Hopsworks services behind one AWS Network Load Balancer that you create yourself, with a target group per service
---

# Shared load balancers on AWS { #shared-load-balancers }

## Introduction

By default the chart asks the AWS Load Balancer Controller for one load balancer per exposed service, as the [AWS getting started guide][aws-getting-started-with-eks] describes.
This guide puts the services behind one Network Load Balancer (NLB) that you create outside the chart: one address for clients, and a load balancer that your own infrastructure tooling owns.
The chart then creates no load balancers.
It binds each service to a target group of your NLB with a `TargetGroupBinding`, and the AWS Load Balancer Controller registers the nodes in it.

The Hopsworks UI and REST API stay behind the Ingress and its application load balancer.

## Create the load balancer { #shared-load-balancers-aws }

Create one internal NLB in the cluster's subnets, with a TCP listener and a target group for each service you expose.
Every target group has target type `instance`, protocol TCP, and the listener's port.

| Service | Listener port | Key under `global.unmanagedLoadBalancers` |
| --- | --- | --- |
| Model serving, HTTP | 80 | `istio.http` |
| Model serving, HTTPS | 443 | `istio.https` |
| Model serving, health | 15021 | `istio.status` |
| Online feature store REST API | 4406 | `rdrs.http` |
| Online feature store MySQL | 3306 | `mysqld` |
| Hopsworks Query Service | 5005 | `arrowflight` |
| OpenSearch | 9200 | `opensearch` |
| Trino | 8443 | `trino` |
| Prometheus, when exposed | 9089 | `prometheus` |
| Hive metastore, when exposed | 9083 | `metastore` |
| Kafka, one listener per broker | 9093 and upward | `kafka` |

Kafka clients connect to each broker directly, so every broker needs a listener and a target group of its own: broker 0 on port 9093, broker 1 on 9094, and so on.

The traffic passes two sets of security group rules.
The NLB's security group admits the clients on the listener ports and allows traffic out to the nodes, which the health checks use too.
The nodes' security group admits the NLB's security group on the node port range.
For an NLB without a security group, the nodes' security group admits the NLB's private addresses on the node port range, for the health checks, and the clients' addresses as well while client IP preservation is on, the default for instance targets.

## Values { #shared-load-balancers-values }

Pass the values below in a file of their own after the values of the [AWS getting started guide][aws-getting-started-with-eks]: the chart creates the bindings only with `global._hopsworks.cloudProvider: AWS`, which those values set.
`managed: false` makes the chart create node port Services and bindings in place of load balancers, and each `targetGroupId` is the Amazon Resource Name (ARN) of a target group:

```yaml
global:
  _hopsworks:
    externalLoadBalancers:
      enabled: true
      managed: false
      class: service.k8s.aws/nlb
  unmanagedLoadBalancers:
    istio:
      http:
        targetGroupId: TARGET_GROUP_ARN
      https:
        targetGroupId: TARGET_GROUP_ARN
      status:
        targetGroupId: TARGET_GROUP_ARN
    rdrs:
      http:
        targetGroupId: TARGET_GROUP_ARN
      grpc:
        targetGroupId: ""
    mysqld:
      targetGroupId: TARGET_GROUP_ARN
    arrowflight:
      targetGroupId: TARGET_GROUP_ARN
    opensearch:
      targetGroupId: TARGET_GROUP_ARN
    trino:
      targetGroupId: TARGET_GROUP_ARN
    kafka:
      targetGroupIds:
        - TARGET_GROUP_ARN_OF_BROKER_0

rondb:
  rondb:
    meta:
      mysqld:
        externalLoadBalancer:
          enabled: true
          managed: false
          class: service.k8s.aws/nlb
      rdrs:
        externalLoadBalancer:
          enabled: true
          managed: false
          class: service.k8s.aws/nlb

kafka:
  cluster:
    kafka:
      externalLoadBalancer:
        managed: false
        dns: NLB_DNS_NAME
        finalizers: []

hopsfs:
  namenode:
    loadBalancer:
      enabled: false
  datanode:
    loadBalancer:
      enabled: false
```

- Every service whose load balancer is enabled needs its key, or the chart fails to render.
  To leave a service out, turn its load balancer off with the `externalLoadBalancer.enabled` value of its chart, listed in the [AWS getting started guide][aws-getting-started-with-eks], and drop its key, listener and target group.
  Model serving has no switch of its own: its three bindings follow `global._hopsworks.externalLoadBalancers.enabled`.
- A key needs every entry shown under it: `istio` takes all three, and `rdrs` both `http` and `grpc`.
  `rdrs.grpc` stays empty, because the chart binds only the HTTP port of the REST API, so the NLB needs no gRPC listener.
- From 5.3, a semantic layer gateway that is exposed takes a listener on port 18446 and the key `semanticGateway.targetGroupId`, with the two host name settings described in [Flight SQL load balancer][semantic-connect-admin-lb].
- Prometheus and the Hive metastore are not exposed by default.
  To expose them, also set `prometheus.externalLoadBalancer.enabled: true` with `prometheus.prometheus.server.service.type: NodePort`, or `hive.externalLoadBalancer.enabled: true`, and add their keys.
- `kafka.targetGroupIds` lists one ARN per broker, in broker order, so it has as many entries as `kafka.cluster.kafka.replicas`.
- The RonDB load balancers do not read `global._hopsworks.externalLoadBalancers`, so they repeat its settings.
- `kafka.cluster.kafka.externalLoadBalancer.dns` is the address the brokers advertise to clients: the DNS name of the NLB.
  Broker 0 advertises port 9093, broker 1 port 9094, matching the listeners above.
- `finalizers: []` removes the finalizer that the AWS getting started guide sets on Kafka's load balancers, which applies only to load balancers the chart creates.
- The chart has no binding for the HopsFS NameNode and DataNode, so their load balancers are turned off, and clients outside the cluster cannot reach HopsFS directly with this setup.

## Addresses that Hopsworks gives to clients { #shared-load-balancers-addresses }

Hopsworks tells its clients where to reach these services.
With load balancers the chart creates, it reads their addresses from the Services.
With a shared NLB there is nothing to read, so set the NLB's DNS name:

```yaml
hopsworks:
  variables:
    loadbalancer_external_domain_feature_query: NLB_DNS_NAME
    loadbalancer_external_domain_mysqld: NLB_DNS_NAME
    loadbalancer_external_domain_online_store_rest_server: NLB_DNS_NAME
    loadbalancer_external_domain_opensearch: NLB_DNS_NAME
    loadbalancer_external_domain_trino: NLB_DNS_NAME
```

Set the variable of every service you expose.
Without it, clients are not told where the service is.
Model serving is the exception: its variable, `kube_knative_lb_domain`, takes a host that serves HTTPS on port 443, which the NLB's TCP listeners do not, as described in [Direct inference from outside the cluster][model-serving-gateway-external-host].
Without that host, clients outside the cluster call REST deployments through the Hopsworks REST API.
On 5.2, the install also waits for the address of every exposed service whose `loadbalancer_external_domain_*` variable is empty, which a shared NLB never provides, until it times out.

## Check { #shared-load-balancers-check }

After the install, the release's namespace holds one binding per bound service port and per Kafka broker, and the target group of each binding reports healthy targets:

```bash
kubectl get targetgroupbindings -n NAMESPACE
aws elbv2 describe-target-health --target-group-arn TARGET_GROUP_ARN
```
