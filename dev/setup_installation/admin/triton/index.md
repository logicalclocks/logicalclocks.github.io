# Triton Inference Server { #triton-admin }

Hopsworks can serve model deployments with NVIDIA Triton Inference Server on KServe.
Triton is off by default and is enabled per cluster through the Hopsworks Helm chart.
Hopsworks ships the Triton serving runtime but no Triton image, so the administrator configures the image the runtime starts.
The image and its licence are the customer's responsibility.

With Triton off, the chart renders no Triton runtime and the `kube_serving_triton_versions` variable is empty.
The UI then does not offer the Triton model server, `ms.get_triton_image_tags()` returns an empty list, and the API rejects Triton deployments.

For packaging and deploying Triton models, see the [Triton guide][triton-model-guide].

## Enable Triton

Set these values on the Hopsworks chart and run `helm upgrade`:

```yaml
global:
  _kserve:
    servingruntime:
      tritonserver:
        enabled: true
        imageRegistry: nvcr.io
        image: nvidia/tritonserver
        tag: "26.09-py3"
```

| Value | Default | Meaning |
| --- | --- | --- |
| `enabled` | `false` | Renders the `kserve-tritonserver` ClusterServingRuntime and advertises the image tags to Hopsworks |
| `imageRegistry` | empty | Registry of the Triton image; required when enabled |
| `image` | empty | Repository of the Triton image; required when enabled |
| `tag` | empty | Tag of the Triton image; required when enabled |
| `extraTags` | `[]` | Further tags deployments may use, see [Image tags][triton-image-tags] |
| `imagePullSecrets` | `[]` | Pull secrets for the Triton runtime only; empty uses `global._hopsworks.imagePullSecrets` |
| `env` | `[]` | Extra environment variables of the Triton container, as `name` and `value` pairs |

With `enabled: true`, `helm upgrade` fails with a message naming the value when `imageRegistry`, `image` or `tag` is empty.
There is no default image.

The values are listed with the other global values in the [global Helm values][helm-values-global].

## Image tags { #triton-image-tags }

The chart sets the `kube_serving_triton_versions` Hopsworks variable to `tag` plus `extraTags`, as a comma-separated list.
These are the tags users can choose for a Triton deployment, in the UI and with `triton_image_tag` in the Python client.
A deployment that names no tag gets the highest of them.

```yaml
global:
  _kserve:
    servingruntime:
      tritonserver:
        tag: "26.09-py3"
        extraTags:
          - "26.06-py3"
```

The advertised tags are returned by the REST API:

```bash
curl -H "authorization: ApiKey <api_key>" \
  "https://<HOPSWORKS_HOST>/hopsworks-api/api/project/<project_id>/serving/tritonImageTags"
```

```json
{"tags": ["26.09-py3", "26.06-py3"], "defaultTag": "26.09-py3"}
```

Each deployment stores its tag and keeps it when `tag` changes, so changing `tag` never moves an existing deployment to another Triton release.
A deployment also keeps its stored tag after the tag is no longer advertised, through restarts and edits that leave the tag unchanged.
Users must pick an advertised tag only when they create a deployment or change its tag.

A deployment runs `<imageRegistry>/<image>:<deployment tag>`, so every tag that deployments use must exist in the configured repository.
Keep the old tags in the repository when you change `imageRegistry` or `image`.

Triton images cannot be pinned by digest in `global.imageDigests`: KServe does not change the tag of an image that carries a digest, so every deployment would run the pinned image whatever its tag.
`helm upgrade` fails when `global.imageDigests` names a Triton image.

## Pull secret { #triton-pull-secret }

A registry that requires credentials needs an image pull secret, for example an NVIDIA AI Enterprise image on `nvcr.io`, which takes an NGC API key.
Name the secret on the Triton runtime:

```yaml
global:
  _kserve:
    servingruntime:
      tritonserver:
        imagePullSecrets:
          - name: ngc-pull
```

Kubernetes looks up an image pull secret in the namespace of the pod, and Triton predictors run in the namespace of their project.
The secret therefore has to exist in every project namespace that runs Triton deployments.

Hopsworks copies the secrets named in the `docker_operations_image_pull_secrets` variable from the Hopsworks namespace into the namespace of each project it creates.
Create the secret in the Hopsworks namespace and add its name to the variable:

```bash
kubectl -n hopsworks create secret docker-registry ngc-pull \
  --docker-server=nvcr.io \
  --docker-username='$oauthtoken' \
  --docker-password='<NGC API key>'
```

```yaml
hopsworks:
  variables:
    docker_operations_image_pull_secrets: "ngc-pull"
```

Projects created before that do not get the secret.
Create it in each of their namespaces with the same `kubectl` command and `-n <project namespace>`.

## Kyverno

On a cluster that enforces Kyverno's restricted policies (`global._hopsworks.kyverno.enabled`), Kyverno rejects the predictor pods of a Triton image that does not pass them.
Such an image needs a policy exception:

```yaml
hw-kyverno:
  policyExceptions:
    triton:
      enabled: true
```

The exception applies to pods labelled `serving.hops.works/model-server: triton`, which Hopsworks sets on Triton predictors.

## Knative

In Knative mode, Knative resolves the image tag to a digest before it creates a revision.
When the Knative controller cannot resolve the tag, for example because it cannot authenticate to the registry or verify its TLS certificate, the deployment fails before a pod is created.
Registries listed in `registries-skipping-tag-resolving` of Knative's `config-deployment` ConfigMap skip this step.
The chart adds the Triton `imageRegistry` to that list.

Check the list on a running cluster:

```bash
kubectl -n hopsworks get configmap config-deployment \
  -o jsonpath='{.data.registries-skipping-tag-resolving}'
```

## Image contract { #triton-image-contract }

The `kserve-tritonserver` runtime starts the configured image as follows.
An image that meets these requirements needs no Hopsworks components: Hopsworks places the model files, certificates and API key in the pod itself.

- **Command.** Hopsworks sets the container's arguments and keeps the image's entrypoint, so the entrypoint must run its arguments as a command, as NVIDIA's `/opt/nvidia/nvidia_entrypoint.sh` does, or the image must have no entrypoint.
  `tritonserver` must be on the `PATH`.
  The arguments are:

    ```text
    tritonserver --model-store=/mnt/models --http-port=8080 --grpc-port=9000 --model-control-mode=none --allow-metrics=true --metrics-port=8002
    ```

    An image whose entrypoint is `tritonserver` itself would receive `tritonserver` again as its first argument, so give such an image an entrypoint script that runs its arguments.

- **Ports.** HTTP on 8080 (Open Inference Protocol REST), gRPC on 9000 (Open Inference Protocol gRPC, served as h2c), and Prometheus metrics on 8002 at `/metrics`.
  In Standard mode, Prometheus scrapes port 8002.
- **Model files.** Before Triton starts, Hopsworks copies the model version's files to `/mnt/models/<deployment-name>/`, so the model repository holds one model named after the deployment.
- **User.** With `global._hopsworks.securityContextEnabled`, the container runs as a non-root user (UID 1000, GID 1000) with privilege escalation disabled and all capabilities dropped, so the image must work as that user.
- **Shared memory.** Hopsworks mounts a memory-backed volume at `/dev/shm`, used by the Python backend; it counts against the memory of the deployment.
- **Backends.** The image contains the Triton backends the models need, for example `onnxruntime`, `pytorch`, `tensorrt`, `openvino` or `python`.
  A Python backend model needs a packed environment with the Python version of the image's Python backend, see [Python backend][triton-python-backend].
- **GPUs.** The runtime requests no GPU; a deployment gets GPUs from its own resource configuration.

Hopsworks tests the runtime with NVIDIA's public `nvcr.io/nvidia/tritonserver:<yy.mm>-py3` images, unmodified.
NVIDIA publishes no CPU-only image; its images run models on the CPU on nodes without a GPU.
NVIDIA's `26.09-py3` image is 8.4 GiB compressed for amd64, so a Knative deployment that scales up from zero on a node without the image waits for the pull.
