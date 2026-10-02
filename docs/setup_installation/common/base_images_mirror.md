---
description: The base image repositories a mirror or air-gapped registry must hold for Hopsworks, the registry features they need, and what to mirror before upgrading to per-type base image repositories.
---

# Base images in mirror registries

Hopsworks runs Python jobs, Jupyter notebooks, terminals, model deployments and environment builds on a set of base images.
On every install and upgrade, the chart's `preset-images` Job copies each base image from a source registry into the cluster registry.
The source is `<imageRegistry>/hopsworks`, which is `docker.hops.works/hopsworks` by default, or `hopsworks.dockerRegistry.preset.alternativeRegistry` when it is set.
If the cluster cannot reach `docker.hops.works`, for example in an air-gapped data centre, the source must be a mirror that holds every base image listed on this page before you install or upgrade.

## Base image repository layout

Each base image type is its own repository below `hopsworks-base`, tagged with the Hopsworks base image version:

```text
<mirror>/hopsworks/hopsworks-base/<type>:<version>
```

`<version>` is the chart value `hopsworks.variables.base_image_version`.
Every image of one chart version carries the same version tag.

Point the chart at the mirror in your values file:

```yaml
hopsworks:
  dockerRegistry:
    preset:
      alternativeRegistry: "<mirror>/hopsworks"
```

The preset Job pulls `<alternativeRegistry>/hopsworks-base/<type>:<version>`, so the value includes every path segment in front of `hopsworks-base`.
Keeping the `hopsworks` segment lets the mirror use the same paths as `docker.hops.works`.

The cluster registry receives the same layout: `<cluster registry>[/<namespace>]/hopsworks-base/<type>:<version>`.

## Base image types

The chart copies these base image types.
The Ray and terminal types are copied only when the feature is enabled, but enabling it later is a Helm upgrade that copies them, so they must be in the mirror by then.

| Base image type | Copied |
| --- | --- |
| `agent-job` | always |
| `dbt-pipeline` | always |
| `dlthub-ingestion-pipeline` | always |
| `internal-base` | always |
| `internal-ml-base` | always |
| `minimal-inference-pipeline` | always |
| `pandas-inference-pipeline` | always |
| `pandas-training-pipeline` | always |
| `python-agent-pipeline` | always |
| `python-app-pipeline` | always |
| `python-feature-pipeline` | always |
| `spark-feature-pipeline` | always |
| `tensorflow-inference-pipeline` | always |
| `tensorflow-training-pipeline` | always |
| `torch-inference-pipeline` | always |
| `torch-training-pipeline` | always |
| `ray-training-pipeline` | Ray enabled |
| `ray-tensorflow-training-pipeline` | Ray enabled |
| `ray-torch-training-pipeline` | Ray enabled |
| `terminal-server` | terminals enabled |
| `terminal-gpu` | terminals enabled |
| `terminal-spark` | terminals enabled |

Ray is enabled by `global._hopsworks.ray.enabled` or `hopsworks.variables.ray_enabled`, and terminals by `hopsworks.terminal.enabled`.

The list can change between chart versions, so read the exact source images for your chart version and values from the preset Job's configuration:

```bash
helm template hopsworks hopsworks/hopsworks --version CHART_VERSION --values values.yaml \
  --kube-version KUBERNETES_VERSION \
  --set hopsworks.velero.enforcePrerequisiteCheck=false \
  --show-only charts/hopsworks/templates/presetconfigmap.yaml \
  | grep -o '"url":"[^"]*"'
```

Each `url` is one image the preset Job pulls, including any `hopsworks.dockerRegistry.preset.extra_images` you configured.
`--kube-version` is needed because `helm template` does not contact the cluster and otherwise checks the chart's supported Kubernetes range against its own default.
The Velero prerequisite check is disabled for the same reason: it looks up the Velero installation in the cluster.

## Mirror the base images

Copy each type from `docker.hops.works` to the mirror, for example with [crane](https://github.com/google/go-containerregistry/tree/main/cmd/crane):

```bash
VERSION=BASE_IMAGE_VERSION
for type in BASE_IMAGE_TYPES; do
  crane copy "docker.hops.works/hopsworks/hopsworks-base/${type}:${VERSION}" \
    "<mirror>/hopsworks/hopsworks-base/${type}:${VERSION}"
done
```

Replace BASE_IMAGE_VERSION with `hopsworks.variables.base_image_version` and BASE_IMAGE_TYPES with the space-separated types from the table above.

## Nested repository names

`hopsworks/hopsworks-base/<type>` is a nested repository name, so both the mirror and the cluster registry must accept a `/` inside repository names.
Registries that restrict nesting cannot hold the base images:

- Docker Hub repository names below a namespace contain only lowercase letters, digits, `-` and `_`, so `hopsworks-base/<type>` cannot be one.
- GitLab allows two path levels below a project, so `hopsworks-base/<type>` fits directly below a project and `hopsworks/hopsworks-base/<type>` does not.
- Quay accepts nested names only with `FEATURE_EXTENDED_REPOSITORY_NAMES` enabled.
- Amazon ECR accepts nested names but does not create a repository on push unless a repository creation template matches it; see [Step 1.2 of the AWS guide][step-12-create-the-ecr-repositories].

## Upgrading from the single-repository layout

Earlier releases stored every base image as a tag of one repository, `hopsworks-base:<type>-<version>`.
The preset Job of a release with per-type repositories pulls only the new paths and has no fallback to the old tags.

Before upgrading to such a release:

1. Mirror `<mirror>/hopsworks/hopsworks-base/<type>:<version>` for every type the new chart version copies.
   Until an image is in the mirror, its preset pod keeps retrying, and pods that need the image wait in `ImagePullBackOff`.
2. On Amazon ECR, create the repository creation template, or the repositories, before the upgrade as described in [Step 1.2 of the AWS guide][step-12-create-the-ecr-repositories].
   Without them, every push of the preset Job to a new repository fails.
3. Keep the old tags in the mirror and in the cluster registry.
   Pods started before the upgrade reference `hopsworks-base:<type>-<version>` and pull it again when they are rescheduled, and `helm rollback` returns to those tags.

Project environments are copies made when they were created, so they do not need the base images of either layout to keep working.
