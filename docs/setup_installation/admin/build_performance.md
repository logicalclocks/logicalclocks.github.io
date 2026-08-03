# Python Environment Build Performance

## Introduction

Every change to a project's Python environment produces a new container image. By default each build starts a private BuildKit daemon inside its own Kubernetes Job, on an `emptyDir`. That daemon re-pulls and re-unpacks the base image every time, and nothing it downloads survives the build.

This guide covers the settings that change that: a long-lived BuildKit daemon, the package cache shared between builds, the toolchain caches a custom-command build can request, and layer reuse.

All of these are off or conservative by default. Turn them on deliberately.

## Prerequisites

An administrator account on a Hopsworks cluster, and Helm access to the deployment for the daemon itself.

## Persistent BuildKit daemon

The daemon is deployed by the Helm chart and is disabled by default:

```yaml
hopsworks:
  buildkitd:
    enabled: true
```

Enabling it deploys a StatefulSet with its own state volume. Once it is running, the chart also points the backend at it: `docker_operations_buildkit_addr` and the client TLS settings are filled in from `buildkitd.name`, `buildkitd.port`, `buildkitd.replicas` and `buildkitd.tls`. You do not set those variables yourself unless you are pointing builds at a daemon the chart does not manage.

### Sizing the state volume

```yaml
hopsworks:
  buildkitd:
    storage: 100Gi
    gc:
      totalKeepBytes: "80GB"
      cacheMountKeepBytes: "30GB"
      cacheMountKeepDuration: "168h"
```

`totalKeepBytes` must stay well above the total unpacked size of every base image in use. Below that, each build evicts the base image the next one needs and the daemon is slower than no daemon at all.

Package caches get their own budget so that downloads cannot evict base image snapshots.

!!! warning
    `gc.keySyntax` selects which GC key names to emit. BuildKit replaced `keepBytes` with `maxUsedSpace` in later releases, and an unknown key makes the daemon refuse to start. Set it to match the BuildKit version you deploy.

### Client certificates

```yaml
hopsworks:
  buildkitd:
    tls:
      enabled: true
```

On by default, and only worth turning off on a single-trust-zone installation.

This is not defence in depth. `buildctl` over TCP is unauthenticated, and BuildKit gives `RUN` steps host networking, so a custom-command script reaches the daemon on both the service address and `127.0.0.1` whatever pod network rules are in place. Client certificates are what stops it. The client key is mounted in the build Job's pod rather than in the `RUN` step's filesystem, so a build step cannot present it.

Note that this authenticates but does not authorize: any certificate the Hopsworks CA issued is accepted. Separating tenants at the daemon level still requires a daemon per trust zone.

### Replicas

```yaml
hopsworks:
  buildkitd:
    replicas: 3
```

Each replica gets its own state volume, and a project is pinned to one of them by id so it keeps hitting the daemon that already unpacked its base image. This adds throughput; it is not what separates tenants, and a project is not failed over to another replica.

## Package cache

```
docker_operations_buildkit_cache_scope
```

| Value | Behaviour |
| --- | --- |
| `shared` | Default. Builds resolving through the same package-index configuration share one cache. |
| `project` | Each project gets its own cache. No sharing at all. |
| `off` | No cache mount. |

A cache only survives between builds if the daemon does, so this pairs with `buildkitd.enabled`.

`shared` is scoped by index configuration rather than by a single cluster-wide identifier. Two projects resolving through the same configuration share, which is the point; a project configured against a different private index gets a different cache, so it cannot receive an artifact fetched under someone else's credentials. Where the index configuration is cluster-wide, which is the normal setup, every project shares.

Choose `project` if you want no sharing between projects under any circumstances.

## Layer reuse

Two separate things decide whether a build step's *result* can be reused, as opposed to its downloads.

### Dependency locking

```
docker_operations_lock_dependencies
```

Off by default. When on, a `pip`, wheel or requirements install first resolves the complete dependency set with a hash per artifact, then installs only from that lock. This makes the resolved set reconstructible and fails the build if an index serves different bytes for a version it already served.

A pinned version alone is not enough for a step's result to be reusable: `pandas==1.0.0` says nothing about the versions its transitive and build dependencies resolve to. Only a lock pins that, which is why locking is what allows the install layer to be reused.

!!! warning
    Locking requires `uv` in the base image. A build on an image without it fails with a message naming the base image, rather than silently installing without a lock. Git installs are never locked: a git reference has no artifact hash to generate.

### Custom commands

A custom-command layer is never reused by default, because the script can fetch anything and nothing declares what. See [Custom Commands](../../user_guides/projects/python/custom_commands.md) for the two directives a build can use, and:

```
docker_operations_allow_hermetic_custom_commands
```

Off by default. This decides whether a build's own assertion that its script fetches nothing mutable is allowed to control cache reuse. Only the script's author knows whether it is true; only you decide whether that claim counts.

## Cache keys and credentials

BuildKit deliberately leaves the contents of build secrets out of a step's cache key. That keeps credentials out of the image, but on its own it means a rotated credential still matches the layer built with the old one, and two projects whose builds differ only by their index credentials produce the same key.

Hopsworks adds an opaque tag to every reusable step covering the project it belongs to and the credential material it mounts, so a layer is never reused across projects and rotating a credential invalidates reuse. The tag is derived under the installation's own key and is not reversible into the credentials.

If that key cannot be read, steps that consume credentials are marked uncacheable rather than reused. Builds get slower; they do not cross a trust boundary.

## Registry trust

When the daemon pulls from a registry served with a private CA, it needs that CA. A per-build daemon inherits it from the build Job's pod; the shared daemon is a separate pod and does not. The chart configures trust for the cluster's own registry automatically. For any additional registry served over plain HTTP or with a certificate the daemon cannot verify:

```yaml
hopsworks:
  buildkitd:
    insecureRegistries:
      - my-registry.example.com:5000
```

## Measuring

The backend logs where the time in a build actually goes:

```
Build docker-build-xxxxxx: context packaged in N ms, uploaded in N ms
Built <image> in N ms (1 region job(s))
Registered <image>: metadata read N ms, database registration N ms (metadata read from the image)
```

A slow environment build is either compilation, image transfer, or orchestration, and those have different fixes. Read the split rather than the total before changing any of the settings above.
