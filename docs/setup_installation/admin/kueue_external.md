# Operator Notes: Kueue Outside the Hopsworks Namespace

Administrative reference for cluster operators who run Kueue with Hopsworks and want to move it out of the Hopsworks release.

With `global._hopsworks.kueue.enabled=true`, every Hopsworks release from 4.3 bundles Kueue 0.12.2 in the Hopsworks namespace.
From 5.3, `hw-kueue.kueue.enabled=false` makes Hopsworks use a Kueue installed outside its release instead: release `kueue` in namespace `kueue-system`, installed with `fullnameOverride: kueue`.
Hopsworks keeps its RBAC bindings to the Kueue roles and keeps queueing jobs through Kueue.

The move is optional.
A cluster that keeps the bundled Kueue needs nothing.
A fresh install that wants an external Kueue installs it first and sets `hw-kueue.kueue.enabled=false`; this page is for clusters that already run the bundled one.

## Why `helm upgrade` alone cannot do it

- **Kueue 0.12 stores Cohorts and Topologies as `v1alpha1`**, which no Kueue from 0.13 on can read.
  Their CRDs have to be replaced and the objects restored.
- **The Kueue CRDs belong to no Helm release.**
  The bundled chart ships them in its `crds/` directory, which Helm installs once and never upgrades.
- **The new release creates cluster-wide objects under the names the Hopsworks release owns**: the `kueue-*` ClusterRoles, the webhook configurations and the visibility APIService.
  The Hopsworks release has to drop them first.

## What the migration does

The chart ships `charts/hw-kueue/files/migrate-to-external.sh`, which moves the cluster to Kueue 0.18.1 and keeps every Kueue object: ClusterQueues, Cohorts, ResourceFlavors, Topologies, LocalQueues, priority classes and Workloads.
It runs in phases, and each one is safe to re-run:

| Phase | What it does |
| --- | --- |
| `preflight` | Checks the tools and the release. Refuses admitted, unfinished Workloads unless given `--allow-admitted`. |
| `backup` | Saves every Kueue object, the Kueue CRDs and the release values to `--backup-dir`. |
| `remove-bundled` | Upgrades Hopsworks with Kueue off, which removes the bundled controller, its webhooks and its ClusterRoles. CRDs and queue objects stay. |
| `replace-alpha-crds` | Snapshots the Cohorts, Topologies and ResourceFlavors, then replaces the `v1alpha1` Cohort and Topology CRDs. |
| `install-kueue` | Applies the Kueue 0.18.1 CRDs, installs release `kueue` in `kueue-system` and restores the replaced objects. |
| `migrate-storage` | Rewrites every object at `v1beta2` and prunes the CRDs' stored versions. |
| `enable-hopsworks` | Upgrades Hopsworks with Kueue on and `hw-kueue.kueue.enabled=false`. |
| `verify` | Checks the controller, the stored versions, every backed-up queue object and the release values. |

A failed run resumes by running the same phase again, or `all`.
`--dry-run` prints the commands that change the cluster; with `all` it stops after `remove-bundled`, whose result the later phases depend on.

## Before you start

- **Take a snapshot** and check that it completed: from `replace-alpha-crds` on, rollback is the snapshot.
- **Plan a maintenance window and stop submitting jobs.**
  From `remove-bundled` to `install-kueue` no Kueue runs, so a job created then runs outside quota.
  Workloads already admitted keep running, and Kueue 0.18.1 takes them over.
- **Tools**: `kubectl`, `helm` 3.20 or later, `jq` and `yq` v4.
- **Airgapped clusters** mirror `registry.k8s.io/kueue/kueue:v0.18.1` (the default image is `docker.hops.works/registry.k8s.io/kueue/kueue:v0.18.1`) and the `kueue` 0.18.1 chart; `--kueue-image` and `--kueue-repo` point the script at the mirror.
- **An admin API key** lets the script refresh Hopsworks' settings after each upgrade.
  Without it Hopsworks picks up the change within 10 minutes, and a project created in those minutes gets its default queue at its first job.

## Run the migration

```sh
helm pull --untar <repo>/hopsworks --version <5.3 version>
HELM_EXTRA_ARGS="<the flags you upgrade Hopsworks with>" \
HOPSWORKS_URL=https://<hopsworks host> \
HOPSWORKS_API_KEY=<admin API key> \
  hopsworks/charts/hw-kueue/files/migrate-to-external.sh \
  --hopsworks-chart <repo>/hopsworks --hopsworks-version <5.3 version> all
```

Both Hopsworks upgrades run `helm upgrade --reset-then-reuse-values` with that chart, so the Hopsworks upgrade to 5.3 happens inside the window.
Pass `--force-conflicts` in `HELM_EXTRA_ARGS` if your upgrades need it.
`--namespace` and `--release` name a Hopsworks release other than `hopsworks` in `hopsworks`; `--help` lists every option.

## What changes

- **ResourceFlavors lose `topologyName`.**
  Topology-aware scheduling is on by default from Kueue 0.14, and no bundled release used it.
  A cluster that enabled it on purpose needs its own handling before the move.
- **Cohorts get `parentName`** in place of `parent`.
  ClusterQueues keep their quotas, fair sharing, preemption and borrowing settings; Kueue converts `cohort`, `admissionChecks` and the `flavorFungibility` values `Borrow` and `Preempt` to their `v1beta2` forms.
- **Queues are managed with `kubectl`.**
  With `hw-kueue.kueue.enabled=false` the chart no longer applies `hw-kueue.clusterQueues`, `cohorts`, `resourceFlavours` or `topologies`.
  Queues defined there before the move are kept, but changing those values has no effect.
- **Jobs in the Hopsworks namespace are queued.**
  Kueue 0.18 ignores the namespace it runs in, which is now `kueue-system`, so Kueue-labelled jobs in the Hopsworks namespace are queued.
- **The project queue utilisation view fails** until the Hopsworks backend reads Cohorts at `v1beta1`: `GET /project/{id}/kube/queueutilization` returns an error after the move.
  Job submission, project queues and quotas are not affected.

## Verify

The `verify` phase checks the end state; run it on its own at any time:

```sh
hopsworks/charts/hw-kueue/files/migrate-to-external.sh verify
```

To check by hand:

```sh
kubectl -n kueue-system get deployment kueue-controller-manager
kubectl get crd -l app.kubernetes.io/name=kueue -o custom-columns=NAME:.metadata.name,STORED:.status.storedVersions
kubectl get clusterqueues,cohorts,resourceflavors
kubectl get localqueues -A
```

The controller is ready in `kueue-system`, none runs in the Hopsworks namespace, every CRD stores `["v1beta2"]`, and every queue from before the move is listed.

With `hw-kueue.kueue.enabled=false` the chart refuses to render while the bundled controller still runs, while Cohorts are stored as `v1alpha1`, or when no Kueue serving `v1beta2` is installed.
`hw-kueue.enforcePrerequisiteCheck=false` turns the check off, for `helm template`.
