# Operator Notes: Kueue Outside the Hopsworks Namespace

Administrative reference for cluster operators who run Kueue with Hopsworks, install a Hopsworks release that uses Kueue 0.20 (a 5.2.x patch release, or 5.3), or upgrade to one.

With `global._hopsworks.kueue.enabled=true`, Hopsworks releases 4.3 to 5.2 bundle Kueue 0.12.2 in the Hopsworks namespace.
A 5.2.x patch release and 5.3 ship no Kueue: they use Kueue 0.20.3 installed outside the Hopsworks release, and their backend reads Kueue objects as `kueue.x-k8s.io/v1beta2`, which Kueue 0.12 does not serve.
A cluster that runs the bundled Kueue 0.12 therefore moves to a Kueue installed outside the Hopsworks release: release `kueue` in namespace `kueue-system`, installed with `fullnameOverride: kueue`, which Hopsworks uses with `hw-kueue.kueue.enabled=false`.
On Hopsworks 5.1 it moves before the upgrade; on 5.2.0 and 5.2.1, which ship no migration script, it moves as part of the upgrade ([From Hopsworks 5.2.0 or 5.2.1](#from-hopsworks-520-or-521)).
Hopsworks keeps its RBAC bindings to the Kueue roles and keeps queueing jobs through Kueue.

A cluster without Kueue needs nothing.
A fresh install of such a release with Kueue installs Kueue first ([Fresh install](#fresh-install)).

## Fresh install

The Hopsworks chart ships no Kueue, as it ships no Kyverno: install Kueue 0.20.3 first, as release `kueue` in `kueue-system`, then Hopsworks with `global._hopsworks.kueue.enabled=true`.
The chart's `upgrade-kueue.sh` installs it with the SparkApplication integration Hopsworks queues Spark jobs through:

```sh
helm pull --untar <repo>/hopsworks --version <version>
bash hopsworks/charts/hw-kueue/files/upgrade-kueue.sh install
helm install hopsworks hopsworks -n hopsworks --set global._hopsworks.kueue.enabled=true ...
```

It applies the Kueue CRDs itself and installs release `kueue` without them, so uninstalling it never deletes the queues.
With `--gitops` it writes the HelmRelease and the CRDs to commit, as in [Clusters managed by Flux](#clusters-managed-by-flux).
The Hopsworks chart then creates the default queues, ResourceFlavor `default-flavor`, Topology `default`, Cohort `cluster` and ClusterQueue `other`, when they are missing.
The default ResourceFlavor selects nodes labelled `cloud.provider.com/region=europe`; label the nodes, or change `hw-kueue.resourceFlavours`.

With Argo CD, install Kueue as an Application of its own, synced before the Hopsworks one: the chart `kueue` version 0.20.3 from `oci://registry.k8s.io/kueue/charts`, release name `kueue` in `kueue-system`, with these values:

```yaml
fullnameOverride: kueue
controllerManager:
  featureGates:
    - name: SparkApplicationIntegration
      enabled: true
managerConfig:
  controllerManagerConfigYaml: |
    # the chart's default, with sparkoperator.k8s.io/sparkapplication
    # added to integrations.frameworks
```

That chart keeps its CRDs among its templates, so Argo CD upgrades them with a version bump.
Leave the `resources-finalizer.argocd.argoproj.io` finalizer off that Application: deleting it then leaves the CRDs, and every queue, in place.

## Why `helm upgrade` alone cannot do it

- **Kueue 0.12 stores Cohorts and Topologies as `v1alpha1`**, which no Kueue from 0.13 on can read.
  Their CRDs have to be replaced and the objects restored.
- **The Kueue CRDs belong to no Helm release.**
  The bundled chart ships them in its `crds/` directory, which Helm installs once and never upgrades.
- **The new release creates cluster-wide objects under the names the Hopsworks release owns**: the `kueue-*` ClusterRoles, the webhook configurations and the visibility APIService.
  The Hopsworks release has to drop them first.

## What the migration does

Two scripts do the move, each shipped with the release it runs on; run them with `bash`, because `helm package` stores files without the execute bit:

- On Hopsworks 5.1, the 5.1 chart's `charts/hw-kueue/files/migrate-to-external.sh` moves the cluster to Kueue 0.18.1, the last release that serves both `v1beta1` and `v1beta2`, and rewrites every object as `v1beta2`. A 5.1 cluster stays on Kueue 0.18.
- After the Hopsworks upgrade to a release with Kueue 0.20, that chart's `charts/hw-kueue/files/upgrade-kueue.sh` upgrades Kueue to 0.20.3.

Every Kueue object is kept: ClusterQueues, Cohorts, ResourceFlavors, Topologies, LocalQueues, priority classes and Workloads.
`migrate-to-external.sh` runs in phases, and each one is safe to re-run; `all` runs them in order:

| Phase | What it does |
| --- | --- |
| `preflight` | Checks the tools and the release. Refuses admitted, unfinished Workloads unless given `--allow-admitted`. |
| `backup` | Saves every Kueue object, the Kueue CRDs and the release values to `--backup-dir`. |
| `remove-bundled` | Upgrades Hopsworks with Kueue off, which removes the bundled controller, its webhooks and its ClusterRoles. CRDs and queue objects stay. |
| `replace-alpha-crds` | Snapshots the Cohorts, Topologies and ResourceFlavors, then replaces the `v1alpha1` Cohort and Topology CRDs. |
| `install-kueue` | Applies the Kueue 0.18.1 CRDs, installs release `kueue` in `kueue-system` and restores the replaced objects. |
| `migrate-storage` | Rewrites every object at `v1beta2` and prunes the CRDs' stored versions. |
| `enable-hopsworks` | Upgrades Hopsworks with Kueue on and `hw-kueue.kueue.enabled=false`, which a 5.2.x patch release or 5.3 keeps by default. |
| `verify` | Checks the controller, the stored versions, every backed-up queue object and the release values. |
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
- **Kueue images**: both scripts default to the repository `docker.hops.works/registry.k8s.io/kueue/kueue`; `--kueue-image registry.k8s.io/kueue/kueue` takes the upstream images.
- **Airgapped clusters** mirror the images `registry.k8s.io/kueue/kueue:v0.18.1` and `v0.20.3` and the `kueue` 0.18.1 and 0.20.3 charts.
  `--kueue-image` and `--kueue-repo` point each script at the mirror; `--kueue-repo` takes a chart repository URL or an `oci://` path.
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

2. Upgrade Hopsworks to a release with Kueue 0.20, keeping `global._hopsworks.kueue.enabled=true`.
    Kueue 0.18.1 serves `v1beta2`, which its backend reads.

3. Upgrade Kueue to 0.20.3, with the script from the new chart:

    ```sh
    helm pull --untar --untardir new <repo>/hopsworks --version <new version>
    bash new/hopsworks/charts/hw-kueue/files/upgrade-kueue.sh
    ```

    It upgrades release `kueue`, then checks the end state; `upgrade-kueue.sh verify` runs the check on its own.
    Until then Kueue 0.18.1 queues jobs, and Spark jobs run without queueing.

`upgrade-kueue.sh` refuses to run while the Hopsworks release's chart bundles a Kueue older than 0.20, while the release does not use the external Kueue or has not finished deploying, while any Kueue CRD stores a version other than `v1beta2`, and refuses a downgrade.
It applies the Kueue CRDs itself and keeps them out of the release, keeps the `kueue` release's own values, and refuses a manager configuration that is not `config.kueue.x-k8s.io/v1beta2` before it changes anything.
A release that turns `TopologyAwareScheduling` off keeps it off: Kueue 0.20 adds six topology-aware scheduling gates, on by default, that depend on it, and the script turns them off too, since Kueue refuses to start with a gate on whose dependency is off.
It turns on Kueue's SparkApplication integration and drops the `managedFields` entries recorded at `v1beta1`, which Kueue 0.20 can no longer convert.
It takes the chart from `oci://registry.k8s.io/kueue/charts` (`--kueue-repo`), version 0.20.3 (`--kueue-version`).

`--namespace` and `--release` name a Hopsworks release other than `hopsworks` in `hopsworks`; `--help` lists every option.

Both scripts read and upgrade Helm release records, directly or through Flux's helm-controller, which keeps them.
A Hopsworks or Kueue release managed by Argo CD, which renders charts and stores no Helm release, is not supported by either script.

## From Hopsworks 5.2.0 or 5.2.1

Hopsworks 5.2.0 and 5.2.1 bundle Kueue 0.12.2 and ship no migration script.
The 5.1 chart's `migrate-to-external.sh` does the move on them too, run phase by phase: the phases up to `migrate-storage` keep Hopsworks on its current chart, and `enable-hopsworks` upgrades it to the new release.
Hopsworks is never downgraded.

```sh
helm pull --untar --untardir v51 <repo>/hopsworks --version <latest 5.1 version>
M="bash v51/hopsworks/charts/hw-kueue/files/migrate-to-external.sh"
export HELM_EXTRA_ARGS="<the flags you upgrade Hopsworks with>"
export HOPSWORKS_URL=https://<hopsworks host> HOPSWORKS_API_KEY=<admin API key>

# Kueue off, Hopsworks stays on its current version
for phase in preflight backup remove-bundled replace-alpha-crds install-kueue migrate-storage; do
  $M --hopsworks-chart <repo>/hopsworks --hopsworks-version <current 5.2 version> $phase || break
done
# Hopsworks upgraded to the release with Kueue 0.20, on the external Kueue
$M --hopsworks-chart <repo>/hopsworks --hopsworks-version <new version> enable-hopsworks
$M verify

helm pull --untar --untardir new <repo>/hopsworks --version <new version>
bash new/hopsworks/charts/hw-kueue/files/upgrade-kueue.sh
```

`enable-hopsworks` upgrades Hopsworks with `--reset-then-reuse-values`, Kueue on and `hw-kueue.kueue.enabled=false`; Kueue 0.18.1 serves `v1beta2`, which the new backend reads.
From `remove-bundled` until `install-kueue` no Kueue runs, as on 5.1.
With Flux, follow [Clusters managed by Flux](#clusters-managed-by-flux) with the same split: keep the current 5.2 chart version in Step 2, and set the new version in Step 4.

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
It then runs `verify` and `export-queues` (Step 6) and exits.

### Step 5: Upgrade Hopsworks and Kueue

Set the Hopsworks HelmRelease's chart version to a release with Kueue 0.20, keeping the values from Step 4, then commit and push.
Once Flux has upgraded Hopsworks, run the new chart's `upgrade-kueue.sh`:

```sh
helm pull --untar --untardir new <repo>/hopsworks --version <new version>
bash new/hopsworks/charts/hw-kueue/files/upgrade-kueue.sh --gitops \
  --release <release> --namespace <namespace>
```

With `--gitops` it runs no `helm upgrade`.
It applies the 0.20.3 CRDs and writes `./kueue-upgrade/kueue.yaml` (`--out-dir`): the HelmRelease `kueue` for 0.20.3 with the release's values, the chart from `oci://registry.k8s.io/kueue/charts`, the Spark manager configuration and feature gate, and a post-render patch that keeps the chart's CRDs out of the release.
Replace the file you committed in Step 3 with it, add `./kueue-upgrade/kueue-crds.yaml` next to it, then commit and push.
The script continues once Flux runs the 0.20.3 controller with the SparkApplication integration on, then checks the end state.

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
Remove `hw-kueue.clusterQueues`, `cohorts`, `resourceFlavours` and `topologies` from the Hopsworks values: the chart creates those queues only when they are missing, and Git now owns them.
LocalQueues are not exported, because Hopsworks creates and deletes them with projects.

### If a step times out or the script stops

Each step polls every 15 seconds for up to `--timeout`, then stops with `timed out waiting for ...`.
Run the same command again: every phase checks what is already done and continues from there, and the restores are applied only once.
A single phase can also be run on its own, such as `bash hopsworks/charts/hw-kueue/files/migrate-to-external.sh --gitops enable-hopsworks`.

### What the script writes

The script applies the Kueue CRDs itself and the HelmRelease skips them (`crds: Skip` on install and upgrade), so deleting the HelmRelease leaves every queue in place.
The 0.20.3 chart ships its CRDs as templates, which `crds: Skip` does not cover, so the HelmRelease `upgrade-kueue.sh` writes also carries a kustomize post-render patch that removes them from what Flux installs.
`upgrade-kueue.sh` also writes the CRDs it applied to `./kueue-upgrade/kueue-crds.yaml`, annotated `kustomize.toolkit.fluxcd.io/prune: disabled`.
Commit it next to `kueue.yaml`, in place of any Kueue CRDs there: Flux applies CRDs before the objects that use them, so Git can restore Kueue on an empty cluster, and never prunes them, so removing the file does not delete the queues.

## What changes

- **ResourceFlavors lose `topologyName`.**
  Topology-aware scheduling is on by default from Kueue 0.14, and no bundled release used it.
  A cluster that enabled it on purpose needs its own handling before the move.
- **Cohorts get `parentName`** in place of `parent`.
  ClusterQueues keep their quotas, fair sharing, preemption and borrowing settings; Kueue converts `cohort`, `admissionChecks` and the `flavorFungibility` values `Borrow` and `Preempt` to their `v1beta2` forms.
- **Queues are managed with `kubectl`.**
  The chart creates the queues in `hw-kueue.clusterQueues`, `cohorts`, `resourceFlavours` and `topologies` only when they are missing.
  Existing queues are kept as they are, and changing those values has no effect on them.
  Write queue objects as `kueue.x-k8s.io/v1beta2`: Kueue 0.20 serves no other version.
- **Spark jobs are queued, with static executors only.**
  `upgrade-kueue.sh` turns on Kueue's SparkApplication integration, so Spark jobs get quota and queueing.
  Kueue reserves quota for a fixed number of executors, so on a Kueue cluster Spark jobs run static executors.
  A job saved with dynamic allocation, as every Spark job was by default, runs its dynamic-allocation minimum, at least one executor: it is converted and saved at its next start, save, or read of the project default.
  A job that needs more executors sets `spark.executor.instances`.
  `spark.dynamicAllocation.enabled=true` in a job's Spark properties is refused.
  Spark in notebooks is unchanged.
- **Workloads must be ready within 30 minutes.**
  Kueue 0.19 turns `waitForPodsReady` on by default: a workload whose pods are not all ready 30 minutes after admission is evicted and queued again.
- **Ray sidecars count against quota.**
  From Kueue 0.19 the Ray autoscaler and job-submitter sidecars are charged to the head, so a queue sized exactly for its Ray heads may need more CPU and memory.
- **Workloads without a priority class get `default`.**
  From Kueue 0.20 such a workload gets the WorkloadPriorityClass named `default`, when one exists.

## Verify

Each script checks the end state, and runs the check on its own at any time:

```sh
bash hopsworks/charts/hw-kueue/files/migrate-to-external.sh verify   # on 5.1
bash new/hopsworks/charts/hw-kueue/files/upgrade-kueue.sh verify     # after the upgrade to Kueue 0.20
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

- It refuses while the bundled Kueue's controller still runs, while Cohorts are stored as `v1alpha1`, or when no Kueue serving `v1beta2` is installed.
- It refuses `hw-kueue.kueue.enabled=true`: the chart ships no Kueue.

`hw-kueue.enforcePrerequisiteCheck=false` turns the check off, for `helm template`.
