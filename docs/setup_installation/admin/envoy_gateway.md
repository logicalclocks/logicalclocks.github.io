---
description: Serve Standard-mode model deployments through the Kubernetes Gateway API on Envoy Gateway, next to Istio, how to turn it on, the images it needs, its cluster requirements and how to remove it
---

# Envoy Gateway { #envoy-gateway }

From 5.3, Hopsworks can route Standard-mode model deployments through the Kubernetes Gateway API, on Envoy Gateway.
KServe builds its Standard mode and its generative AI features (`LLMInferenceService`, llm-d, the agent router) on the Gateway API, so this is the path those features follow.

Nothing changes for the clients of your deployments.
Istio stays the front door, with the same endpoint, ports and URLs, and forwards Standard-mode traffic to Envoy Gateway inside the cluster.
Knative-mode deployments keep running through Istio as before.

--8<-- "setup_installation/admin/envoy_gateway/traffic.html"

!!! info "Off by default"

    An upgrade to 5.3 that does not turn the feature on routes nothing differently.
    API keys are checked by `model-serving-authenticator` on both paths, so access rules stay the same.

## Turn it on { #envoy-gateway-enable }

Two values in `global._hopsworks.envoyGateway` control the feature:

- `enabled` installs Envoy Gateway and its Gateway, without moving any traffic.
- `kserveStandardMode` moves the Standard-mode deployments to it, and is `true` by default.

=== "New installation"

    Set `enabled`, and both steps happen in one install:

    ```yaml
    global:
      _hopsworks:
        envoyGateway:
          enabled: true
    ```

=== "Cluster with running deployments"

    Turn it on in two upgrades, so that you can check the Gateway before any deployment moves:

    ```yaml
    global:
      _hopsworks:
        envoyGateway:
          enabled: true
          kserveStandardMode: false # set to true in the second upgrade
    ```

    Follow [Envoy Gateway][upgrade-envoy-gateway] in the upgrade guide, which lists the checks before, between and after the two upgrades.
    Each deployment moves once its new routes are accepted, without a restart and without failed requests.

All values are listed in [Envoy Gateway values][helm-values-hw-envoy-gateway], and the Gateway's own settings under `kserve.envoyGateway` in [KServe values][helm-values-kserve].

## What gets installed { #envoy-gateway-components }

- The Envoy Gateway 1.9 controller, in the Hopsworks namespace (the `hw-envoy-gateway` subchart).
- The Gateway `kserve-ingress-gateway` and the Envoy proxies behind it, with a policy that checks every request's API key.
- The CustomResourceDefinitions (CRDs) of Envoy Gateway and of the Gateway API, as described in [CustomResourceDefinitions][envoy-gateway-crds].

When the deployments move, the KServe controller restarts once.
The deployments themselves are not restarted.

## Images { #envoy-gateway-images }

| Image | Used for |
| ----- | -------- |
| `docker.hops.works/envoyproxy/gateway` | The controller, the certificate setup and a sidecar of each proxy |
| `docker.hops.works/envoyproxy/envoy` | The Envoy proxies |
| `docker.hops.works/hopsworks/envoy-gateway-crds` | Installing the CRDs |

On an airgapped cluster, mirror the three images and point the chart at your registry, as the chart's `values.airgap.yaml` shows:

```yaml
hw-envoy-gateway:
  controller:
    image:
      registry: <your registry>
  envoyProxy:
    image:
      registry: <your registry>
  crdImage:
    registry: <your registry>/hopsworks
```

## CustomResourceDefinitions { #envoy-gateway-crds }

The chart installs the CRDs it needs during each install and upgrade.
The Gateway API CRDs are shared by the whole cluster, so the chart treats them carefully:

- It installs them when the cluster has none, and updates them only when it installed them itself.
- It leaves a newer or experimental set installed by someone else as it is.
- It stops the install or upgrade when someone else installed an older set, because only that owner can upgrade it.

To see which Gateway API CRDs a cluster has:

```bash
kubectl get crd gateways.gateway.networking.k8s.io -o jsonpath='{.metadata.annotations}'
```

!!! tip "OpenShift and GKE"

    On OpenShift 4.19 and later, and on GKE, the platform provides the Gateway API CRDs.
    Set `hw-envoy-gateway.gatewayApiCrds.enabled: false` so the chart uses them; `values.openshift.yaml` already does.
    This setup is verified on OKD 4.21.

## Cluster requirements { #envoy-gateway-requirements }

- **Permissions.**
  The chart grants the Hopsworks backend what it needs.
  If you install with `rbac.useExistingRole`, add the permissions below to your role.
- **OpenShift.**
  The Envoy Gateway pods run with the user and group ids the platform assigns, which `values.openshift.yaml` sets up.
- **Isolation.**
  Only the namespaces of your Hopsworks installation can attach routes to its Gateway, and each installation's controller manages only its own Gateway.
  Hopsworks labels those namespaces itself, so there is nothing to configure.

??? note "Permissions for `rbac.useExistingRole`"

    Add to the existing backend role:

    | API group | Resources | Verbs |
    | --------- | --------- | ----- |
    | `gateway.networking.k8s.io` | `httproutes`, `referencegrants` | `get`, `list`, `watch`, `create`, `update`, `patch`, `delete` |
    | `gateway.networking.k8s.io` | `gateways` | `get`, `list`, `watch` |
    | `gateway.envoyproxy.io` | `securitypolicies` | `get`, `list`, `watch`, `create`, `update`, `patch`, `delete` |
    | `""` | `namespaces` | `get`, `patch` |
    | `discovery.k8s.io` | `endpointslices` | `get`, `list` |

    Add them before you turn the feature on.
    With the feature off, Hopsworks works without them.

??? note "Expose the Gateway directly"

    By default the Gateway is reachable only inside the cluster, through Istio.
    To reach it directly as well, set `kserve.envoyGateway.service.type` to `NodePort`, with ports under `kserve.envoyGateway.service.nodePorts` that differ from Istio's, or to `LoadBalancer`.
    This needs `model-serving-authenticator` 5.3 or later, and is not supported yet on AWS with unmanaged load balancers.

    On the Gateway itself, a path must name the project exactly as its namespace or as its name, and the deployment exactly as its name.
    For project `My_Proj`, `/v1/my-proj/mstd/...` and `/v1/My_Proj/mstd/...` work, while `/v1/MY_PROJ/mstd/...` gets a 404.
    Istio accepts any capitalization of the project and any separator, so this only matters for clients that call the Gateway directly.

## Turn it off or uninstall { #envoy-gateway-uninstall }

To turn the feature off, upgrade twice in the reverse order.
First set `kserveStandardMode: false`, which moves the deployments back to Istio without restarting them.
Once `kubectl get ingress -A -l serving.kserve.io/inferenceservice` lists every ready Standard-mode deployment again, set `enabled: false`, which removes Envoy Gateway.

!!! warning "Use `helm upgrade`, not `helm rollback`"

    The Gateway objects are created and removed by install and upgrade hooks, which `helm rollback` does not run, so a rollback would leave them and the Envoy proxies behind.
    If that happened, upgrade again with `enabled: false`, which removes them.

Uninstalling Hopsworks with the feature on removes the Envoy proxies, the Gateway objects and the routes.
The CRDs stay, because other software on the cluster may use the Gateway API ones; set `hw-envoy-gateway.cleanupOnUninstall.deleteCrds` to remove them too.

??? note "What stays after turning the feature off"

    `enabled: false` leaves the GatewayClass `<release>-envoy-gateway`, the CRDs and the certificate Secrets `envoy-gateway`, `envoy`, `envoy-rate-limit` and `envoy-oidc-hmac`.
    They do nothing on their own, and are reused if you turn the feature on again.
    Once the feature is off, uninstalling Hopsworks leaves them too.

    To remove them, delete the Gateway API CRDs only if the chart installed them, and nothing else on the cluster uses them, because deleting a CRD deletes every object of its kind:

    ```bash
    kubectl delete gatewayclass <release>-envoy-gateway
    kubectl delete secret -n <namespace> envoy-gateway envoy envoy-rate-limit envoy-oidc-hmac
    kubectl get crd -o name | grep 'gateway.envoyproxy.io' | xargs kubectl delete
    # The Gateway API CRDs, only if this prints envoy-gateway-crd-install:
    kubectl get crd gateways.gateway.networking.k8s.io -o jsonpath='{.metadata.managedFields[*].manager}'
    kubectl get crd -o name | grep 'gateway.networking.k8s.io' | xargs kubectl delete
    ```
