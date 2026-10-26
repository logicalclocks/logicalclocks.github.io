# Operator Notes: Kafka 4 and KRaft in Hopsworks 5.2 { #kafka4-kraft-upgrade }

Administrative reference for cluster operators upgrading a self-managed Hopsworks cluster to 5.2.

Hopsworks 5.2 moves the bundled Kafka from Strimzi 0.45 with Kafka 3.9 to Strimzi 1.2 with Kafka 4.3.1.
Kafka 4 has no ZooKeeper, so an existing cluster is migrated to KRaft as part of the upgrade.
The chart performs that migration itself; this page covers what to prepare, what to expect and how to verify the result.

A fresh 5.2 install needs none of this: it starts on KRaft.

## What the upgrade does

Two pre-upgrade hooks run before any new component is applied:

1. `kafka-kraft-migration` carries the cluster from ZooKeeper to KRaft under the operator that is still running.
   It has to run before anything is applied, because the migration needs an operator that understands ZooKeeper, and that is the one the previous release left running.
   It adds the KRaft node pools, annotates the cluster for migration, waits for the metadata to move, and finalises.
   On a cluster already on KRaft it exits in seconds.
2. `strimzi-crd-upgrade` converts the Strimzi custom resources from the `v1beta2` API to `v1` and brings the CRDs up to the new operator's version.

The release then replaces the operator with Strimzi 1.2 and rolls the brokers to Kafka 4.3.1.

## What to expect

- **The upgrade blocks while the migration runs.**
  The hook waits three times, each bounded by `kafka.migrationJob.timeoutSeconds` (default 1800), so the worst case is 3 x that value.
  Helm's `--timeout` applies to each hook on its own: give it at least that budget plus room for the rest of the release.
  On timeout the hook fails rather than hangs, and re-running the upgrade resumes from wherever the operator got to.
- **Broker pods are replaced about seven times**: during the migration, when the finalised cluster drops its ZooKeeper-era settings, and when the brokers move to Kafka 4.3.1.
  The controller pods are replaced twice.
  Strimzi replaces pods rather than restarting containers, so `restartCount` stays 0 throughout; watch pod names and ages instead.
  A single-broker cluster is unavailable for the duration of each replacement, and OnlineFS catches up afterwards; clusters with a replication factor above 1 roll without interruption.
- **ZooKeeper and the new controllers run side by side** until the migration is finalised.
  The controller pool inherits its sizing from the ZooKeeper settings, so the namespace needs headroom for both during the upgrade.
- **Finalising KRaft is irreversible.**
  Once the cluster reports `PreKRaft` or `KRaft`, ZooKeeper is gone.
  Strimzi can roll back a migration before that point, but only with ZooKeeper support, which the Strimzi that 5.2 ships does not have, so the chart cannot drive that rollback.
  Do not `helm rollback` after the migration has started, and do not run this upgrade with `--atomic`, which performs that rollback for you the moment a hook times out: the earlier revision puts the ZooKeeper-shaped Kafka resource back against a cluster that may already have finalised KRaft.
  Re-run the upgrade instead.
- **One `helm upgrade` migrates the cluster and its CRDs.**
  The `strimzi-crd-upgrade` hook converts the resources still stored as `v1beta2` through the 0.51.0 CRDs, then applies the 1.2.0 CRDs in the same upgrade, as described in [Strimzi CRDs][kafka4-strimzi-crds].
- **ArgoCD needs one manual step**, and every Application needs an `ignoreDifferences` entry for the Kafka CRD, as described in [Under ArgoCD][kafka4-argocd].

## Before you start { #kafka4-before-you-start }

Run these read-only checks first.
The upgrade refuses, or waits until it times out, on each problem they find.

1. **The Strimzi CRDs**, once per Kubernetes cluster:

    ```sh
    kubectl get crd kafkas.kafka.strimzi.io -o json | jq -r '
      if any(.spec.versions[]; .name == "v1" and .served) then "converted"
      elif any(.spec.versions[]; .name == "v1beta2" and (.schema.openAPIV3Schema.properties.status.properties | has("kafkaMetadataState"))) then "ok"
      else "strimzi-0.39" end'
    ```

    - `ok`: nothing to do; go on with checks 2 to 4.
    - `converted`: an earlier 5.2 upgrade converted the CRDs, which it does only once every Kafka on the Kubernetes cluster is on KRaft.
      Nothing to do, and checks 2 to 4 do not apply: the state field is gone, and the operator may already be 1.2.
    - `strimzi-0.39`: the CRDs cannot report the migration state, so the migration hook refuses rather than guess.
      A cluster has these when it was first installed on Hopsworks 4.3, 4.5 or a 4.4 release before 4.4.19, and has been upgraded with `helm upgrade` or ArgoCD since.
      Apply the Strimzi 0.45.2 CRDs, then wait until check 2 shows a state.
      Without `--force-conflicts` the apply is refused on the fields their earlier installer owns:

        ```sh
        kubectl apply --server-side --force-conflicts -f \
          https://github.com/strimzi/strimzi-kafka-operator/releases/download/0.45.2/strimzi-crds-0.45.2.yaml
        ```

        Do not apply the 5.2 chart's own CRDs for that: the apiserver rejects them while `v1beta2` is still a stored version.
        An airgapped cluster has to mirror that bundle too; the `strimzi/crds` image carries only the 0.51.0 and 1.2.0 bundles.

2. **Every Kafka**, in all namespaces, because the central cluster's operator also runs the satellites':

    ```sh
    kubectl get kafkas.v1beta2.kafka.strimzi.io -A -o json | jq -r '.items[] |
      "\(.metadata.namespace)/\(.metadata.name): state=\(.status.kafkaMetadataState // "<none>") ready=\([.status.conditions[]? | select(.type == "Ready") | .status] | first // "no") generation=\(.metadata.generation)/\(.status.observedGeneration // "?")"'
    ```

    Each line should read `state=ZooKeeper ready=True` with the two generation numbers equal, or `state=KRaft` for a satellite already on 5.2.

    - `state=<none>`: the operator has not written the state yet, or check 1 printed `strimzi-0.39`.
      Wait for the operator to reconcile.
    - `state=KRaftMigration`, `KRaftDualWriting` or `KRaftPostMigration`: an earlier 5.2 attempt is still migrating.
      Run that release's upgrade again.
    - `ready` other than `True`, or two different generations: fix the Kafka first, because the migration waits for Ready at each step.

3. **The operator**: one `strimzi-cluster-operator`, Ready, on 0.45.x.
    It runs the migration before the upgrade replaces it.

    ```sh
    kubectl get deploy -A --field-selector metadata.name=strimzi-cluster-operator \
      -o 'custom-columns=NAMESPACE:.metadata.namespace,READY:.status.readyReplicas,IMAGE:.spec.template.spec.containers[0].image'
    ```

4. **Capacity**: until the migration is finalised, each Kafka runs its ZooKeeper and a set of KRaft controllers with ZooKeeper's replicas, resources, storage size and storage class.
    Leave room for that many more pods and persistent volumes.

Then:

- **Airgapped clusters** mirror three images with the rest: `strimzi/operator`, `strimzi/kafka` and `strimzi/crds`.
  The chart's `vendor_images.sh` includes them; nothing is fetched from the internet during the upgrade.
- **A satellite cluster that shares the central operator** is upgraded before central.
  The CRD conversion re-stores every Kafka resource on the Kubernetes cluster, and a satellite still on ZooKeeper would lose its ZooKeeper configuration in the process.
  The conversion refuses while any other Kafka is not on KRaft, so the wrong order fails safely, but it blocks central's upgrade until the satellite is done.
- **Record the topics**, so you can confirm nothing was lost:

    ```sh
    kubectl exec -n <namespace> <cluster>-kafka-0 -c kafka -- bash -c '
    topics=$(ls /var/lib/kafka/data-0/kafka-log0 | grep -E -- "-[0-9]+$" | grep -v "^__cluster_metadata" | sed -E "s/-[0-9]+$//" | sort -u)
    printf "%s\n" "$topics"
    printf "%s\n" "$topics" | wc -l'
    ```

## Strimzi CRDs { #kafka4-strimzi-crds }

Strimzi 1.2 stores its resources as `kafka.strimzi.io/v1`.
The `strimzi-crd-upgrade` hook converts CRDs that still store `v1beta2` through the 0.51.0 CRDs, then applies the 1.2.0 CRDs with `v1beta2` still served.

Under Helm, `v1beta2` stays served on that Kubernetes cluster afterwards.
Helm builds a release's current objects from the manifest it stored, so a release stored at `v1beta2`, such as a satellite upgraded to 5.2 before central, can only be upgraded while that version is served.
ArgoCD renders every sync afresh and applies the `v1`-only CRDs in its Sync phase.

Central and its satellites must be all under Helm or all under ArgoCD before central's first 5.2 upgrade; a mix of the two is not supported.
With central under ArgoCD, its first 5.2 sync drops `v1beta2`, and a satellite managed by Helm and stored at `v1beta2` cannot be upgraded after it.

Helm 4 applies a chart's `crds/` on every `helm install`, over the CRDs already on the Kubernetes cluster, before it validates values or runs any hook.
Install onto a Kubernetes cluster that already has the Strimzi CRDs, such as a reinstall of central or a second installation, with `--skip-crds`; the hook applies them.
An install that ran without it and then failed can leave `v1beta2` unserved.
Fix the cause and install again: the pre-install hook finds the `hopsworks.ai/strimzi-v1beta2-served` annotation on the Kafka CRD and serves `v1beta2` again.
If Helm recorded the failed release, remove it first with `helm uninstall --no-hooks <release> -n <namespace>` and the cleanup in [What stays][uninstall-leftovers].
An uninstall with hooks runs the failed release's cleanup Job, which on a Kubernetes cluster with another installation also deletes that installation's project namespaces, as described in [Before you uninstall][uninstall-before].

A Kubernetes cluster upgraded with a 5.2 pre-release chart can be left on the 0.51.0 CRDs.
The Strimzi operator then logs `Kafka <name> in namespace <namespace> was MODIFIED` every few seconds for each Kafka and runs at its CPU limit.
Upgrading central with 5.2.0 or later applies the 1.2.0 CRDs and ends it.
To check, run the following; `false` means the Kubernetes cluster still has the 0.51.0 CRDs:

```sh
kubectl get crd kafkas.kafka.strimzi.io -o yaml \
  | yq '.spec.versions[] | select(.name == "v1") | .schema.openAPIV3Schema.properties.status.properties | has("clusterSecurity")'
```

## Under ArgoCD { #kafka4-argocd }

The first sync after the chart bump does not finish on its own, and finishing it is a manual step.
ArgoCD renders the manifest once, before its PreSync hooks run, from the APIs the cluster serves at that moment, so on a 5.1 cluster the Kafka resources render at `v1beta2`.
After the CRD conversion, the Sync phase would apply the new operator's CRDs, which serve `v1` only, and replace the operator under a Kafka resource it cannot reconcile.
The `strimzi-crd-upgrade` hook therefore stops the sync after the conversion, and the cluster stays on the operator that understands it until a sync renders at `v1`.

1. **Bump the Application to the 5.2 chart and let it sync.**
    The PreSync hooks migrate the cluster to KRaft and convert the CRDs, then `strimzi-crd-upgrade` stops the sync with a message that says why.
    The operation shows as failed on that hook, the previous operator keeps running, and the cluster is healthy: nothing needs to be undone.
    ArgoCD retries the operation under the Application's retry policy; each retry re-runs the hooks, which are idempotent and take a minute or two, and stops at the same message.

2. **Invalidate ArgoCD's cluster cache.**
    The cache refreshes by itself only when a CRD is created or deleted, or on its periodic resync, and does not notice that a CRD's served versions changed: on ArgoCD 3.4.5 every retry rendered `v1beta2` again.
    In the UI: Settings, Clusters, the cluster, Invalidate Cache.
    The `argocd` CLI has no command for it; use the API, or restart the application controller:

    ```sh
    curl -k -X POST "$ARGOCD_URL/api/v1/clusters/https%3A%2F%2Fkubernetes.default.svc/invalidate-cache?id.type=server" \
      -H "Authorization: Bearer $ARGOCD_TOKEN" -H "Content-Type: application/json" -d '{}'
    ```

3. **Hard-refresh the Application**, with Refresh, Hard in the UI, or:

    ```sh
    argocd app get hopsworks --hard-refresh
    ```

    The Kafka resources now show at `v1` and OutOfSync, with no ComparisonError on the Application.

4. **Sync**, with the Sync button or `argocd app sync hopsworks`.
    Auto-sync does not retry a revision whose last attempt failed, so this sync is manual.
    It applies the 1.2.0 CRDs, the operator and the `v1` resources, upgrades Kafka, and runs the PostSync hooks.

5. **Give the Application an `ignoreDifferences` entry for the Kafka CRD**, on a fresh install as much as on an upgrade.
    Upstream's 1.2.0 Kafka CRD declares an empty `properties: {}` map under `status.clusterSecurity`, and the apiserver drops an empty map when it stores a CRD, so the live object never matches the render.
    Without the entry the Application never reaches Synced, and selfHeal re-applies that one CRD every five minutes.
    The entry matches nothing on 5.1.x, so you can add it before the upgrade.
    `helm upgrade` is not affected.

    ```yaml
    spec:
      ignoreDifferences:
        - group: apiextensions.k8s.io
          kind: CustomResourceDefinition
          name: kafkas.kafka.strimzi.io
          jqPathExpressions:
            - .spec.versions[].schema.openAPIV3Schema.properties.status.properties.clusterSecurity.properties
    ```

    The annotation `argocd.argoproj.io/compare-options: ServerSideDiff=true` on the Application also settles it, but it changes how every resource in the Application is compared and takes effect only after a hard refresh, so prefer the narrower entry.

The sync blocks while the migration hook runs, for the same reason a `helm upgrade` does: PreSync hooks finish before the Sync phase starts.
The rendered manifest never mentions ZooKeeper or the migration annotation, because by the time the Sync phase applies it the cluster is already on KRaft.

## Verify

```sh
kubectl get strimzipodset <cluster>-zookeeper -n <namespace> --ignore-not-found
kubectl get pods -n <namespace> -l strimzi.io/name=<cluster>-zookeeper
kubectl get pods -n <namespace> -l strimzi.io/controller-role=true
```

Nothing for the first two, at least one controller pod for the third, and the same topic list as before.

Two checks look right but say nothing:

- **StatefulSets.**
  Strimzi has run every node pool in a StrimziPodSet since 0.35, so `kubectl get sts | grep zookeeper` returns nothing even on a live ZooKeeper cluster.
  The ZooKeeper StrimziPodSet is what the operator creates only while ZooKeeper is real, and removes when the migration finalises.
- **The `strimzi.io/kraft` annotation.**
  The chart renders it, so it says what was asked for, not what happened.

Read `.status.kafkaMetadataState` only while the upgrade runs, when the CRDs are still `v1beta2`, and expect exactly `KRaft`; a half-finished migration counts as not migrated:

```sh
kubectl get kafka <cluster> -n <namespace> -o jsonpath='{.status.kafkaMetadataState}'
```

The field exists in the `v1beta2` status schema only.
Once `strimzi-crd-upgrade` has moved the stored version to `v1`, the field is pruned and a fully migrated cluster reports it empty.

If the upgrade fails part-way, re-run it.
The hook's log names what it was waiting for and the last state it saw, a timeout corrupts nothing because the operator migrates on its own schedule, and the re-run resumes from the live state.
The one state the hook refuses outright is a cluster whose CRDs are too old to report `.status.kafkaMetadataState`, which is the `strimzi-0.39` case of [check 1][kafka4-before-you-start].
Strimzi would read the migration annotation on such a cluster as already migrated and start the brokers on KRaft without copying the ZooKeeper metadata, so the hook stops instead.

## Client compatibility {#kafka4-client-compatibility}

Kafka 4 dropped support for old protocol versions ([KIP-896](https://cwiki.apache.org/confluence/display/KAFKA/KIP-896%3A+Remove+old+client+protocol+API+versions+in+Kafka+4.0)).
The 4.3.1 brokers accept Java clients from 2.1 and librdkafka-based clients (Python, Go, .NET) from 1.8.2.
The clients shipped with Hopsworks 5.2 are within those ranges; check any producer or consumer you build against the cluster yourself.

The same cut applies the other way round for a [bring-your-own Kafka cluster][external-kafka-cluster]: Hopsworks 5.2 connects with kafka-clients 4.3.1, so the external brokers must run Kafka 2.1 or newer.
