# Model Serving Ingress Gateway { #model-serving-ingress-gateway }

## Introduction

Inference requests to KServe model deployments enter through the Istio ingress gateway, the `istio-ingressgateway` Service in the Hopsworks namespace.
It routes on the path: `/v1/<project namespace>/<deployment>/...` reaches that deployment.
By default the chart creates the Service with three node ports, 32080 (HTTP), 32443 (HTTPS) and 32021 (status):

- as a `NodePort` Service when the chart's external load balancers are unmanaged;
- as a `LoadBalancer` Service otherwise.

`kserve.istio.gateways.ingress.serviceType` sets the type instead.
Leave it empty to keep the default.

| `serviceType` | Service type | Node ports |
| --- | --- | --- |
| `""` (default) | `NodePort` or `LoadBalancer`, as above | 32080, 32443, 32021 |
| `ClusterIP` | `ClusterIP` | none |
| `NodePort` | `NodePort` | 32080, 32443, 32021 |
| `LoadBalancer` | `LoadBalancer` | 32080, 32443, 32021 |

The values are listed in [KServe values][helm-values-kserve].

## Where clients send inference requests { #model-serving-gateway-endpoints }

The Hopsworks backend tells clients where the gateway is:

- `KUBE_CLUSTER`: the gateway's ClusterIP, for clients inside the cluster.
- `LOAD_BALANCER`: the host in `kube_knative_lb_domain` on HTTPS port 443 when that variable is set, otherwise the address of the gateway's load balancer, if it has one.

The Python client in a cluster pod calls the gateway directly.
Outside the cluster it calls the `LOAD_BALANCER` endpoint.
Without one, it sends requests to REST deployments through the Hopsworks REST API, which forwards them to the gateway.
The REST API does not forward gRPC, so a gRPC deployment can be called from outside the cluster only through a `LOAD_BALANCER` endpoint that carries gRPC to the gateway.

The client reads the endpoints once, on its first inference request, and keeps them until the Python process ends.

## Namespaces without NodePort or LoadBalancer Services { #model-serving-gateway-clusterip }

A namespace whose ResourceQuota sets `services.nodeports: 0` and `services.loadbalancers: 0` rejects the default gateway Service, and the install fails in the `istioctl-install-job` hook:

```text
services "istio-ingressgateway" is forbidden: exceeded quota: ..., requested: services.loadbalancers=1,services.nodeports=3, ...
```

Install with a ClusterIP gateway:

```yaml
kserve:
  istio:
    gateways:
      ingress:
        serviceType: ClusterIP
```

The other Services the chart creates must not need node ports or load balancers either:

- The bundled container registry is a `NodePort` Service, because the kubelet pulls from it through the node port.
  Use a managed registry, `global._hopsworks.managedDockerRegistery`.
- The external load balancers of RonDB, Kafka, OpenSearch, HopsFS, Hive Metastore, Trino and Arrow Flight are `LoadBalancer` Services.
  Turn them off, which also removes access to these services from outside the cluster:

```yaml
global:
  _hopsworks:
    externalLoadBalancers:
      enabled: false
rondb:
  rondb:
    meta:
      mysqld:
        externalLoadBalancer:
          enabled: false
      rdrs:
        externalLoadBalancer:
          enabled: false
```

The RonDB lines are needed because the chart's root values set these two from `global._hopsworks.externalLoadBalancers.enabled` when the file is read, so overriding the global value later does not reach them.

With a ClusterIP gateway the backend advertises only `KUBE_CLUSTER`.
Clients outside the cluster send requests to REST deployments through the Hopsworks REST API, unless an address in front of the gateway is set up, as described below.
gRPC deployments cannot be called from outside the cluster without such an address.

### Unmanaged load balancers on AWS { #model-serving-gateway-aws }

With unmanaged load balancers on AWS, the chart binds the gateway to the target groups in `global.unmanagedLoadBalancers.istio`.
Their targets reach the gateway through its node ports, so the chart refuses `serviceType: ClusterIP` there:

```text
istio.gateways.ingress.serviceType ClusterIP cannot be used with unmanaged load balancers on AWS: the istio target groups reach the ingress gateway through its node ports
```

## Direct inference from outside the cluster { #model-serving-gateway-external-host }

To let clients outside the cluster call the gateway directly, put a host in front of it and set `kube_knative_lb_domain` to that host.
The host must serve HTTPS on port 443 and forward to the gateway's `http2` port (80) with the path unchanged.

On OpenShift, an edge Route does this for REST deployments:

```bash
oc -n <namespace> create route edge istio-inference \
  --service=istio-ingressgateway \
  --port=http2 \
  --hostname=inference-hopsworks.apps.<cluster domain>
```

The Route carries HTTP/1.1 to the gateway, since the gateway's ports declare no `h2c` application protocol, so it does not carry gRPC.

Check it with a REST deployment and an API key with the `SERVING` scope.
The model name in the path is the deployment name:

```bash
curl -H "Authorization: ApiKey <api key>" \
  -H "Content-Type: application/json" \
  -d '{"instances": [[5.1, 3.5, 1.4, 0.2]]}' \
  https://inference-hopsworks.apps.<cluster domain>/v1/<project namespace>/<deployment>/v1/models/<deployment>:predict
```

Then set `kube_knative_lb_domain` to the host, without a scheme, on the configuration page described in [Cluster Configuration][cluster-configuration].
The backend advertises the host as the `LOAD_BALANCER` endpoint on HTTPS 443 at once, without a restart.
Python clients started afterwards call it directly; running ones keep the endpoints they read first.

## Changing the type of an existing gateway { #model-serving-gateway-change }

`helm upgrade` with a new `serviceType` changes the existing Service in place, in the `istioctl-install-job` hook.
The ClusterIP stays the same and the gateway pods are not restarted, so running deployments keep serving without a redeploy.

After a switch away from `LoadBalancer`, clients outside the cluster keep calling the old load balancer address until three things are done, in this order:

1. If `kube_knative_lb_domain` names the old load balancer, point it at the new host in front of the gateway, or clear it to use the REST API.
   The backend advertises this variable whatever the Service type is.
2. Restart `hopsworks-instance`.
   The backend keeps the gateway's addresses in memory until it restarts, so without a restart it keeps advertising the old load balancer address.
   Read the replica count first, since the Deployment returns to it:

    ```bash
    REPLICAS=$(kubectl -n <namespace> get deployment hopsworks-instance -o jsonpath='{.spec.replicas}')
    kubectl -n <namespace> scale deployment hopsworks-instance --replicas=0
    kubectl -n <namespace> wait pod -l app=hopsworks-instance --for=delete --timeout=10m
    kubectl -n <namespace> scale deployment hopsworks-instance --replicas="$REPLICAS"
    ```

3. Restart the Python processes that already sent inference requests, such as notebook kernels and long-running jobs.
   The client keeps the endpoints it read first until its process ends.

A ResourceQuota rejects only creates and updates that raise its usage, and the switch to `ClusterIP` lowers it, so the quota can be added before or after the upgrade.
