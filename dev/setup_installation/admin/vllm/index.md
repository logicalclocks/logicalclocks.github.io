# vLLM serving runtimes { #vllm-admin }

Hopsworks serves vLLM deployments with two KServe runtimes: `vllm-openai` for the standard **vLLM** variant and `vllm-omni` for **vLLM-Omni**.
Both run the upstream vLLM images unchanged, and the Hopsworks Helm chart sets one default image tag for each.
vLLM-Omni is enabled by default and can be [disabled][vllm-disable-omni] per cluster.

For choosing the variant and image version of a deployment, see [vLLM variant and image version][vllm-variant-and-image-version].

## Image tags { #vllm-image-tags }

Each runtime has an image tag, which the runtime starts by default, and a list of advertised tags, which users can choose from:

| Runtime | Image tag | Advertised tags |
| --- | --- | --- |
| `vllm-openai` | `kserve.kserve.servingruntime.vllmopenai.tag` | `hopsworks.variables.kube_serving_vllm_versions` |
| `vllm-omni` | `kserve.kserve.servingruntime.vllmomni.tag` | `hopsworks.variables.kube_serving_vllm_omni_versions` |

The advertised tags are a comma-separated list.
Users choose from them in the UI and with `vllm_image_tag` in the Python client, and a deployment that names no tag gets the highest of them.
By default the chart advertises only the image tag of each runtime.

Set the keys in the table to change them.
The chart's `global._kserve.servingruntime.vllmopenai.tag` and `global._kserve.servingruntime.vllmomni.tag` only fill in these keys' defaults inside the chart, so setting them in your own values changes nothing.

```yaml
kserve:
  kserve:
    servingruntime:
      vllmopenai:
        tag: "v0.34.0"
hopsworks:
  variables:
    kube_serving_vllm_versions: "v0.34.0,v0.32.0"
```

The advertised tags are returned by the REST API:

```bash
curl -H "authorization: ApiKey <api_key>" \
  "https://<HOPSWORKS_HOST>/hopsworks-api/api/project/<project_id>/serving/vllmImageTags"
```

```json
{"items": [
  {"variant": "VLLM", "tags": ["v0.34.0", "v0.32.0"], "defaultTag": "v0.34.0"},
  {"variant": "VLLM_OMNI", "tags": ["v0.32.0"], "defaultTag": "v0.32.0"}
]}
```

Each deployment stores its tag and keeps it when the chart's tag changes, through upgrades, restarts and edits that leave the tag unchanged.
A deployment also keeps its stored tag after the tag is no longer advertised.
Users must pick an advertised tag only when they create a deployment or change its tag, so moving an existing deployment to a new tag is an edit of that deployment.

A deployment runs `<registry>/vllm/vllm-openai:<deployment tag>` or `<registry>/vllm/vllm-omni:<deployment tag>`.
With `kserve.kserve.servingruntime.vllmopenai.cpu.enabled: true`, the `vllm-openai` runtime runs `<registry>/vllm/vllm-openai-cpu:<deployment tag>` instead, with the same tag.
The registry is `kserve.kserve.servingruntime.vllmopenai.imageRegistry` or `kserve.kserve.servingruntime.vllmomni.imageRegistry`, and `global._hopsworks.imageRegistry` when that is empty.
Every tag that deployments use must exist in that registry, so keep the old tags when you mirror a new one.

## Disable vLLM-Omni { #vllm-disable-omni }

Set this value on the Hopsworks chart and run `helm upgrade`:

```yaml
global:
  _kserve:
    servingruntime:
      vllmomni:
        enabled: false
```

With vLLM-Omni disabled:

- The chart renders no `vllm-omni` ClusterServingRuntime and no longer references the `vllm/vllm-omni` image.
- The chart sets `kube_serving_vllm_omni_versions` to an empty list.
- The UI does not offer vLLM-Omni for new deployments, and `ms.get_vllm_image_tags(variant="VLLM_OMNI")` returns an empty list.
- Hopsworks refuses to create, update or start a vLLM-Omni deployment, or to roll a deployment back to a vLLM-Omni version, with error code `240080`.
- Stopping and deleting vLLM-Omni deployments still works, and an existing vLLM-Omni deployment can be switched to the vLLM variant.

Disabling vLLM-Omni does not stop deployments that are running or remove images the nodes have already pulled.
Stop or delete the vLLM-Omni deployments before you disable it.
Hopsworks does not start them again while vLLM-Omni is disabled.

With ArgoCD, the `vllm-omni` ClusterServingRuntime is removed only when the sync prunes resources.

The Helm value is the persistent setting.
An administrator can also change `kube_serving_vllm_omni_versions` in the [cluster configuration][cluster-configuration], which takes effect at once, but the next `helm upgrade` sets it back from the chart.

To enable vLLM-Omni again, set `enabled: true`, the default, and run `helm upgrade`.
