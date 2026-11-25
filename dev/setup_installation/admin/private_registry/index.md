# Private registries and air-gapped installs { #private-registry }

## Introduction

The Hopsworks chart pulls every image from `docker.hops.works` by default.
This guide installs it from your own registry instead, for a cluster without internet access or one that may pull only from an approved registry.
It assumes the cluster's nodes can pull from that registry without image pull secrets, for example from Amazon ECR through the node IAM role.

## How the chart names images { #private-registry-names }

Every image the chart uses, including those of the third-party components it installs, is published under `docker.hops.works` at a fixed path, for example `docker.hops.works/hopsworks/rondb:<tag>` or `docker.hops.works/quay.io/jetstack/cert-manager-controller:<tag>`.
Your registry holds the same images at the same paths, so `docker.hops.works/<path>` becomes `<registry>/<path>`.

The Hopsworks images take their registry from `global._hopsworks.imageRegistry`.
The third-party charts that the Hopsworks chart includes, such as Consul, Prometheus, Grafana, Strimzi, Superset, Trino and KEDA, take their registry or repository from their own values.
The chart package includes `values.airgap.yaml`, which sets all of them to a placeholder registry, `private-docker.dev-cloud.hopsworks.ai:4443`.
Download the chart version you install and write a copy of that file with your registry in its place:

```bash
helm pull hopsworks/hopsworks --version VERSION --untar
sed 's#private-docker.dev-cloud.hopsworks.ai:4443#REGISTRY#g' hopsworks/values.airgap.yaml > values.registry.yaml
```

`REGISTRY` is the registry address with any path prefix, for example `111122223333.dkr.ecr.eu-west-1.amazonaws.com/hopsworks-mirror`.
Take `values.airgap.yaml` from the chart version you install, because a release can add images and the values that name them.

Then fill your registry, either by copying the images ([Images to mirror][private-registry-images]) or, on Amazon ECR, through a pull through cache ([Pull-through cache on Amazon ECR][private-registry-ecr-pull-through]), and install ([Install][private-registry-install]).

## Images to mirror { #private-registry-images }

Render the unpacked chart with your values file, such as `values.aws.yaml` from the AWS getting started guide, and the registry file, and list every image under your registry:

```bash
helm template hopsworks ./hopsworks --namespace hopsworks --skip-tests --values values.aws.yaml --values values.registry.yaml > rendered.yaml
grep -oE 'REGISTRY/[A-Za-z0-9._/-]+[:@][A-Za-z0-9._:-]+' rendered.yaml | sort -u > images.txt
helm show values hopsworks/charts/kserve --jsonpath '{.istio.istioctl.targetVersion}'
```

The list covers the images that an install and the platform's workloads pull, including those started later, such as the base images of jobs and notebooks and the Kafka brokers.
Add `REGISTRY/istio/pilot` and `REGISTRY/istio/proxyv2`, tagged with the Istio version that the last command prints, because the Istio installation names them only when it runs.

Copy each image from `docker.hops.works` to the same path in your registry, for example with [crane](https://github.com/google/go-containerregistry/blob/main/cmd/crane/README.md), and record every image that fails:

```bash
while read -r image; do
  crane copy "docker.hops.works/${image#REGISTRY/}" "$image" || echo "$image" >> not-copied.txt
done < images.txt
```

Check `not-copied.txt` before installing.
It can list images that Hopsworks never starts, such as the Strimzi operator's defaults for other Kafka versions, which are not published.
Copy any other entry again, because a pod whose image is missing cannot start.
Mirror again from a render of the new chart version before each upgrade, because an upgrade pulls the images of the new release.

Kueue, when enabled, is installed outside the Hopsworks chart with its own images and chart, which [Kueue outside the Hopsworks namespace][kueue-external] lists.

## Pull-through cache on Amazon ECR { #private-registry-ecr-pull-through }

On Amazon ECR, a pull through cache replaces the copy step.
Hopsworks publishes its images to Amazon ECR Public under `public.ecr.aws/c8w3j7u1`, at the same paths as on `docker.hops.works`.
Create a cache rule with that upstream, choosing your own repository prefix in place of `hopsworks-mirror`:

```bash
aws ecr create-pull-through-cache-rule --ecr-repository-prefix hopsworks-mirror --upstream-registry ecr-public --upstream-registry-url public.ecr.aws --upstream-repository-prefix c8w3j7u1 --region REGION --profile PROFILE
```

Use `ECR_AWS_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/hopsworks-mirror` as `REGISTRY` when you write `values.registry.yaml`.
Amazon ECR creates a repository and caches an image the first time a node pulls it, so the node role needs `ecr:CreateRepository` and `ecr:BatchImportUpstreamImage` on `arn:aws:ecr:REGION:ECR_AWS_ACCOUNT_ID:repository/hopsworks-mirror/*`, besides the read access of `AmazonEC2ContainerRegistryReadOnly`.
Amazon ECR fetches the images from Amazon ECR Public itself, so the nodes pull from your registry only.
When the nodes reach Amazon ECR through VPC endpoints, [AWS requires](https://docs.aws.amazon.com/AmazonECR/latest/userguide/vpc-endpoints.html#ecr-vpc-endpoint-considerations) an internet route from the VPC, such as a NAT gateway, for the first pull of each image through the cache.
On a VPC without one, pull every image in the list from [Images to mirror][private-registry-images] once through the cache from a machine with internet access before installing.

## Install { #private-registry-install }

Install from the unpacked chart with the same values files:

```bash
helm install hopsworks ./hopsworks --namespace hopsworks --values values.aws.yaml --values values.registry.yaml --timeout=3600s
```
