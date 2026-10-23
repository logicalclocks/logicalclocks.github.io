# Operator Notes: Kueue Outside the Hopsworks Namespace

Administrative reference for cluster operators who run Kueue with Hopsworks and upgrade to a Hopsworks release that bundles Kueue 0.20: a 5.2.x patch release, or 5.3.

With `global._hopsworks.kueue.enabled=true`, Hopsworks releases 4.3 to 5.2 bundle Kueue 0.12.2 in the Hopsworks namespace.
Those releases bundle Kueue 0.20.3, and their backend reads Kueue objects as `kueue.x-k8s.io/v1beta2`, which Kueue 0.12 does not serve.
A cluster that runs the bundled Kueue 0.12 therefore moves to a Kueue installed outside the Hopsworks release before that upgrade, while it runs Hopsworks 5.1: release `kueue` in namespace `kueue-system`, installed with `fullnameOverride: kueue`, which Hopsworks uses with `hw-kueue.kueue.enabled=false`.
Hopsworks keeps its RBAC bindings to the Kueue roles and keeps queueing jobs through Kueue.

A cluster without Kueue needs nothing.
A fresh install of such a release gets Kueue 0.20.3 in the Hopsworks namespace, or uses an external Kueue installed first with `hw-kueue.kueue.enabled=false`.

## Why `helm upgrade` alone cannot do it

- **Kueue 0.12 stores Cohorts and Topologies as `v1alpha1`**, which no Kueue from 0.13 on can read.
  Their CRDs have to be replaced and the objects restored.
- **The Kueue CRDs belong to no Helm release.**
  The bundled chart ships them in its `crds/` directory, which Helm installs once and never upgrades.
- **The new release creates cluster-wide objects under the names the Hopsworks release owns**: the `kueue-*` ClusterRoles, the webhook configurations and the visibility APIService.
  The Hopsworks release has to drop them first.

## What the migration does

The 5.1 chart ships `charts/hw-kueue/files/migrate-to-external.sh`; the charts with Kueue 0.20 do not. Use the latest 5.1 chart, whose `--help` lists the `upgrade-kueue` phase. Run the script with `bash`, because `helm package` stores files without the execute bit. The script keeps every Kueue object: ClusterQueues, Cohorts, ResourceFlavors, Topologies, LocalQueues, priority classes and Workloads.
On 5.1 it moves the cluster to Kueue 0.18.1, the last release that serves both `v1beta1` and `v1beta2`, and rewrites every object as `v1beta2`.
After the Hopsworks upgrade to a release with Kueue 0.20, its `upgrade-kueue` phase upgrades Kueue to 0.20.3.
It runs in phases, and each one is safe to re-run; `all` runs every phase except `upgrade-kueue`:

| Phase | What it does |
| --- | --- |
| `preflight` | Checks the tools and the release. Refuses admitted, unfinished Workloads unless given `--allow-admitted`. |
| `backup` | Saves every Kueue object, the Kueue CRDs and the release values to `--backup-dir`. |
| `remove-bundled` | Upgrades Hopsworks with Kueue off, which removes the bundled controller, its webhooks and its ClusterRoles. CRDs and queue objects stay. |
| `replace-alpha-crds` | Snapshots the Cohorts, Topologies and ResourceFlavors, then replaces the `v1alpha1` Cohort and Topology CRDs. |
| `install-kueue` | Applies the Kueue 0.18.1 CRDs, installs release `kueue` in `kueue-system` and restores the replaced objects. |
| `migrate-storage` | Rewrites every object at `v1beta2`, prunes the CRDs' stored versions and drops the `managedFields` entries recorded at older versions. |
| `enable-hopsworks` | Upgrades Hopsworks with Kueue on and `hw-kueue.kueue.enabled=false`. |
| `upgrade-kueue` | Upgrades release `kueue` to Kueue 0.20.3 (`--kueue-target`). Refuses while the Hopsworks release's chart bundles a Kueue older than 0.20, while any Kueue CRD stores a version other than `v1beta2`, while the Hopsworks release does not use the external Kueue or has not finished deploying, and refuses a downgrade. Keeps the `kueue` release's own values, and refuses a manager configuration that is not `config.kueue.x-k8s.io/v1beta2` before it changes anything. Drops the `managedFields` entries recorded at `v1beta1`, which Kueue 0.20 can no longer convert. Takes the chart from `oci://registry.k8s.io/kueue/charts` (`--kueue-target-repo`). |
| `verify` | Checks the controller and its version (0.18.1 before the Hopsworks upgrade, 0.20.3 after), the stored versions, every backed-up queue object and the release values. |
| `export-queues` | Writes the cluster-scoped queue objects as `v1beta2` manifests to `<backup-dir>/gitops/kueue-queues.yaml`, for clusters that keep their queues in Git. |

The script applies the Kueue CRDs itself and installs release `kueue` without them, so `helm uninstall kueue` leaves the CRDs, and every queue, in place.

A failed run resumes by running the same phase again, or `all`.
`--dry-run` prints the commands that change the cluster; with `all` it stops after `remove-bundled`, whose result the later phases depend on.

## Before you start

- **Take a snapshot** and check that it completed: from `replace-alpha-crds` on, rollback is the snapshot.
- **Plan a maintenance window and stop submitting jobs.**
  From `remove-bundled` to `install-kueue` no Kueue runs, so a job created then runs outside quota.
  Workloads already admitted keep running, and Kueue 0.18.1 takes them over.
- **Tools**: `kubectl`, `helm` 3.20 or later, `jq` and `yq` v4.
- **Kueue images**: the default repository is `docker.hops.works/registry.k8s.io/kueue/kueue`. `--kueue-image registry.k8s.io/kueue/kueue` takes the upstream images.
- **Airgapped clusters** mirror the images `registry.k8s.io/kueue/kueue:v0.18.1` and `v0.20.3` (the default repository is `docker.hops.works/registry.k8s.io/kueue/kueue`) and the `kueue` 0.18.1 and 0.20.3 charts; `--kueue-image`, `--kueue-repo` and `--kueue-target-repo` point the script at the mirror.
  `--kueue-repo` (the 0.18.1 chart) and `--kueue-target-repo` (the 0.20.3 chart) take a chart repository URL or an `oci://` path.
- **An admin API key** lets the script refresh Hopsworks' settings after each upgrade.
  Without it Hopsworks picks up the change within 10 minutes, and a project created in those minutes gets its default queue at its first job.

## Run the migration

The move runs in three steps.

1. On Hopsworks 5.1, move the cluster to Kueue 0.18.1:

    ```sh
    helm pull --untar <repo>/hopsworks --version <latest 5.1 version>
    HELM_EXTRA_ARGS="<the flags you upgrade Hopsworks with>" \
    HOPSWORKS_URL=https://<hopsworks host> \
    HOPSWORKS_API_KEY=<admin API key> \
      bash hopsworks/charts/hw-kueue/files/migrate-to-external.sh \
      --hopsworks-chart <repo>/hopsworks --hopsworks-version <latest 5.1 version> all
    ```

    Both Hopsworks upgrades in `all` run `helm upgrade --reset-then-reuse-values` with that chart.
    Pass `--force-conflicts` in `HELM_EXTRA_ARGS` if your upgrades need it.
    `verify` at the end of `all` expects Kueue 0.18.1.
    Jobs can be submitted again once it passes.

2. Upgrade Hopsworks to a release with Kueue 0.20, keeping `global._hopsworks.kueue.enabled=true` and `hw-kueue.kueue.enabled=false`.
    Kueue 0.18.1 serves `v1beta2`, which its backend reads.

3. Upgrade Kueue to 0.20.3, with the script from the 5.1 chart:

    ```sh
    bash hopsworks/charts/hw-kueue/files/migrate-to-external.sh upgrade-kueue
    bash hopsworks/charts/hw-kueue/files/migrate-to-external.sh verify
    ```

    Until then Kueue 0.18.1 queues jobs, and Spark jobs run without queueing.

`--namespace` and `--release` name a Hopsworks release other than `hopsworks` in `hopsworks`; `--help` lists every option.

## Clusters managed by Flux

When Flux manages the Hopsworks release, run the script with `--gitops`.
Flux keeps running throughout: do not suspend any HelmRelease or Kustomization.
The script never runs `helm upgrade`.
At each step that changes a Helm release it prints the change, you commit it to the Git repository Flux reconciles, and the script waits until Flux has applied it.
The kubectl work (backup, CRDs, restores, the storage rewrite, verification) the script does itself.

Without `--gitops`, `preflight` and every step that would run `helm upgrade` refuse on a Flux-managed release, because Flux would undo the upgrade at its next reconcile.

### Before you start with Flux

Everything under [Before you start](#before-you-start) applies, and:

- **Flux 2.3 or later.**
  The files the script writes use `helm.toolkit.fluxcd.io/v2` and `source.toolkit.fluxcd.io/v1`; `flux version` shows the controllers' versions.
- **Write access to the Git repository** that holds the Hopsworks HelmRelease, and a path in it that a Flux Kustomization applies, for the new Kueue release and, at the end, the queues.
- **The Helm release name and namespace of Hopsworks.**
  `flux get helmreleases -A` lists the HelmReleases; the Helm release name is the HelmRelease's `spec.releaseName`, or `<targetNamespace>-<name>` when that is unset, and `helm list -A` shows it.
  Pass both with `--release` and `--namespace` unless they are `hopsworks` and `hopsworks`.
- **Where the HelmRelease takes its values from**: `spec.values`, or a ConfigMap or Secret named in `spec.valuesFrom`.
  The value changes below go there.
- **A terminal that survives a dropped connection**, such as `tmux` or `screen`.
  The script waits for each commit for up to `--timeout`, 60 minutes by default; pass a longer one, such as `--timeout 4h`, when commits go through review.

### Step 1: Start the script

```sh
helm pull --untar <repo>/hopsworks --version <latest 5.1 version>
HOPSWORKS_URL=https://<hopsworks host> \
HOPSWORKS_API_KEY=<admin API key> \
  bash hopsworks/charts/hw-kueue/files/migrate-to-external.sh --gitops \
  --release <release> --namespace <namespace> --backup-dir ./kueue-backup all
```

`--hopsworks-chart` is not needed: Flux upgrades Hopsworks.
The script runs `preflight` and `backup`, then stops at the first change to commit.

### Step 2: Turn off the bundled Kueue

The script prints the change for `remove-bundled`.
In the Hopsworks HelmRelease, set the latest 5.1 chart version, and turn Kueue off in its values:

```yaml
spec:
  chart:
    spec:
      version: "<latest 5.1 version>"
  values:
    global:
      _hopsworks:
        kueue:
          enabled: false
```

Commit and push.
To apply it without waiting for the next sync interval, run `flux reconcile helmrelease <name> -n <namespace> --with-source`.
The script continues once the bundled Kueue controller is gone and the release shows the value.
From here until Step 3 completes no Kueue runs: a job created in that window runs outside quota.

### Step 3: Install Kueue

The script replaces the `v1alpha1` Cohort and Topology CRDs, applies the new Kueue CRDs, and writes `<backup-dir>/gitops/kueue.yaml`: the `kueue-system` namespace, a HelmRepository and a HelmRelease `kueue`.
Copy that file into a path of the Git repository that a Flux Kustomization applies, such as `clusters/<cluster>/kueue/kueue.yaml`, then commit and push.
`flux reconcile kustomization <name> --with-source` applies it at once.

Commit the file only when the script asks for it: the HelmRelease skips the CRDs, which the script applies just before.
The script then waits for the Kueue controller, restores the Cohorts and Topologies, and rewrites every Kueue object at `v1beta2`.

### Step 4: Point Hopsworks at the new Kueue

The script prints the change for `enable-hopsworks`.
In the Hopsworks HelmRelease values:

```yaml
spec:
  values:
    global:
      _hopsworks:
        kueue:
          enabled: true
    hw-kueue:
      kueue:
        enabled: false
```

Commit and push; the script continues once the release shows both values.
It then runs `verify` and `export-queues` (Step 6) against Kueue 0.18.1 and exits.

### Step 5: Upgrade Hopsworks and Kueue

Set the Hopsworks HelmRelease's chart version to a release with Kueue 0.20, keeping the values from Step 4, then commit and push.
Once Flux has upgraded Hopsworks, run the script's last phase:

```sh
bash hopsworks/charts/hw-kueue/files/migrate-to-external.sh --gitops \
  --release <release> --namespace <namespace> --backup-dir ./kueue-backup upgrade-kueue
```

The script applies the 0.20.3 CRDs and rewrites `<backup-dir>/gitops/kueue.yaml` for 0.20.3: the chart from `oci://registry.k8s.io/kueue/charts`, the Spark manager configuration and feature gate, and a post-render patch that keeps the chart's CRDs out of the release.
Replace the file you committed in Step 3 with it, then commit and push.
The script continues once the Kueue controller runs 0.20.3; `verify` then checks the end state.

### Step 6: Verify and move the queues into Git

`verify` checks the end state, then `export-queues` writes `<backup-dir>/gitops/kueue-queues.yaml`: the ResourceFlavors, Topologies, Cohorts, ClusterQueues, AdmissionChecks and WorkloadPriorityClasses as `kueue.x-k8s.io/v1beta2`, with the server-set fields removed.
Commit it under a Flux Kustomization of its own that depends on the one applying `kueue.yaml`:

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: kueue-queues
  namespace: flux-system
spec:
  interval: 10m
  path: ./clusters/<cluster>/kueue-queues
  prune: true
  sourceRef:
    kind: GitRepository
    name: <git repository>
  dependsOn:
    - name: <kustomization applying kueue.yaml>
```

From then on the queues are changed in Git.
With `prune: true`, a queue removed from Git is deleted from the cluster.
Remove `hw-kueue.clusterQueues`, `cohorts`, `resourceFlavours` and `topologies` from the Hopsworks values: with `hw-kueue.kueue.enabled=false` they have no effect.
LocalQueues are not exported, because Hopsworks creates and deletes them with projects.

### If a step times out or the script stops

Each step polls every 15 seconds for up to `--timeout`, then stops with `timed out waiting for ...`.
Run the same command again: every phase checks what is already done and continues from there, and the restores are applied only once.
A single phase can also be run on its own, such as `bash hopsworks/charts/hw-kueue/files/migrate-to-external.sh --gitops enable-hopsworks`.

### What the script writes

The script applies the Kueue CRDs itself and the HelmRelease skips them (`crds: Skip` on install and upgrade), so deleting the HelmRelease leaves every queue in place.
The 0.20.3 chart ships its CRDs as templates, which `crds: Skip` does not cover, so its HelmRelease also carries a kustomize post-render patch that removes them from what Flux installs.

## What changes

- **ResourceFlavors lose `topologyName`.**
  Topology-aware scheduling is on by default from Kueue 0.14, and no bundled release used it.
  A cluster that enabled it on purpose needs its own handling before the move.
- **Cohorts get `parentName`** in place of `parent`.
  ClusterQueues keep their quotas, fair sharing, preemption and borrowing settings; Kueue converts `cohort`, `admissionChecks` and the `flavorFungibility` values `Borrow` and `Preempt` to their `v1beta2` forms.
- **Queues are managed with `kubectl`.**
  With `hw-kueue.kueue.enabled=false` the chart no longer applies `hw-kueue.clusterQueues`, `cohorts`, `resourceFlavours` or `topologies`.
  Queues defined there before the move are kept, but changing those values has no effect.
  Write queue objects as `kueue.x-k8s.io/v1beta2`: Kueue 0.20 serves no other version.
- **Jobs in the Hopsworks namespace are queued.**
  Kueue 0.18 ignores the namespace it runs in, which is now `kueue-system`, so Kueue-labelled jobs in the Hopsworks namespace are queued.
- **Spark jobs are queued, with static executors only.**
  The script turns on Kueue's SparkApplication integration, so Spark jobs get quota and queueing.
  Kueue reserves quota for a fixed number of executors, so Hopsworks refuses a Spark job with dynamic allocation on a Kueue cluster.
  Spark jobs saved before the upgrade have dynamic allocation on: turn it off and set the number of executors before running them.
  Spark in notebooks is unchanged.
- **Workloads must be ready within 30 minutes.**
  Kueue 0.19 turns `waitForPodsReady` on by default: a workload whose pods are not all ready 30 minutes after admission is evicted and queued again.
- **Ray sidecars count against quota.**
  From Kueue 0.19 the Ray autoscaler and job-submitter sidecars are charged to the head, so a queue sized exactly for its Ray heads may need more CPU and memory.
- **Workloads without a priority class get `default`.**
  From Kueue 0.20 such a workload gets the WorkloadPriorityClass named `default`, when one exists.

## Verify

The `verify` phase checks the end state; run it on its own at any time:

```sh
bash hopsworks/charts/hw-kueue/files/migrate-to-external.sh verify
```

To check by hand:

```sh
kubectl -n kueue-system get deployment kueue-controller-manager
kubectl get crd -l app.kubernetes.io/name=kueue -o custom-columns=NAME:.metadata.name,STORED:.status.storedVersions
kubectl get clusterqueues,cohorts,resourceflavors
kubectl get localqueues -A
```

The controller is ready in `kueue-system`, none runs in the Hopsworks namespace, every CRD stores `["v1beta2"]`, and every queue from before the move is listed.

The chart checks the cluster before it renders:

- With `hw-kueue.kueue.enabled=false`, it refuses while the bundled controller still runs, while Cohorts are stored as `v1alpha1`, or when no Kueue serving `v1beta2` is installed.
- With `hw-kueue.kueue.enabled=true`, it refuses when the Kueue CRDs exist and the Hopsworks release does not own them: those of the bundled Kueue 0.12, or those of an external Kueue.

`hw-kueue.enforcePrerequisiteCheck=false` turns the check off, for `helm template`.
