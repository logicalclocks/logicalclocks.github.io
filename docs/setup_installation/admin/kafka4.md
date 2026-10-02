# Operator Notes: Kafka 4 and KRaft in Hopsworks 5.2

Administrative reference for cluster operators upgrading a self-managed Hopsworks cluster to 5.2.

Hopsworks 5.2 moves the bundled Kafka from Strimzi 0.45 with Kafka 3.9 to Strimzi 1.2 with
Kafka 4.3.1. Kafka 4 has no ZooKeeper, so an existing cluster is migrated to KRaft as part of the
upgrade. The chart performs that migration itself; this page covers what to prepare and what to
expect. The mechanics, the failure modes and the verification steps are documented in the
[chart README](https://github.com/logicalclocks/hopsworks-helm/blob/main/README.md#migrating-kafka-from-zookeeper-to-kraft).

A fresh 5.2 install needs none of this: it starts on KRaft.

## What the upgrade does

Two pre-upgrade hooks run before any new component is applied:

1. `kafka-kraft-migration` carries the cluster from ZooKeeper to KRaft under the operator that is
   still running: it adds the KRaft node pools, annotates the cluster for migration, waits for
   the metadata to move, and finalises.
2. `strimzi-crd-upgrade` converts the Strimzi custom resources from the `v1beta2` API to `v1`
   and brings the CRDs up to the new operator's version.

The release then replaces the operator with Strimzi 1.2 and rolls the brokers to Kafka 4.3.1.

## What to expect

- **The upgrade blocks while the migration runs.** The hook waits three times, each bounded by
  `kafka.migrationJob.timeoutSeconds` (default 1800), so the worst case is 3 x that value.
  Helm's `--timeout` applies to each hook on its own: give it at least that budget plus room
  for the rest of the release. On timeout the hook fails rather than hangs, and re-running the
  upgrade resumes from wherever the operator got to.
- **Broker pods are replaced about seven times**: during the migration, when the finalised
  cluster drops its ZooKeeper-era settings, and when the brokers move to Kafka 4.3.1. A
  single-broker cluster is unavailable for the duration of each replacement; clusters with a
  replication factor above 1 roll without interruption.
- **ZooKeeper and the new controllers run side by side** until the migration is finalised. The
  controller pool inherits its sizing from the ZooKeeper settings, so the namespace needs
  headroom for both during the upgrade.
- **Finalising KRaft is irreversible.** Do not `helm rollback` after the migration has started,
  and do not run this upgrade with `--atomic`, which performs that rollback for you the moment
  a hook times out. Re-run the upgrade instead.
- **Helm needs one `helm upgrade`.** The Strimzi CRDs finish moving on the upgrade after this
  one, and the cluster is fully functional in between.
- **ArgoCD needs one manual step.** ArgoCD renders the chart from its cached list of cluster
  APIs before the hooks run, so the first sync converts the CRDs and then stops on purpose with
  a message in the `strimzi-crd-upgrade` Job. Then: invalidate the cluster cache
  (Settings > Clusters > the cluster > Invalidate Cache), hard-refresh the Application, and
  sync again. The second sync completes the upgrade.

## Before you start

- **Airgapped clusters** mirror three images with the rest: `strimzi/operator`,
  `strimzi/kafka` and `strimzi/crds`. The chart's `vendor_images.sh` includes them; nothing is
  fetched from the internet during the upgrade.
- **A satellite cluster that shares the central operator** is upgraded before central.
- **Clusters first installed on Hopsworks 4.3 or 4.5** still run Strimzi 0.39 CRDs and need the
  0.45.2 CRD bundle applied by hand before the upgrade; the chart README has the command and
  the reason.
- **Record the topics**, so you can confirm nothing was lost:

```sh
kubectl exec -n <namespace> <cluster>-kafka-0 -c kafka -- bash -c '
topics=$(ls /var/lib/kafka/data-0/kafka-log0 | grep -E -- "-[0-9]+$" | grep -v "^__cluster_metadata" | sed -E "s/-[0-9]+$//" | sort -u)
printf "%s\n" "$topics"
printf "%s\n" "$topics" | wc -l'
```

## Verify

```sh
kubectl get strimzipodset <cluster>-zookeeper -n <namespace> --ignore-not-found
kubectl get pods -n <namespace> -l strimzi.io/name=<cluster>-zookeeper
kubectl get pods -n <namespace> -l strimzi.io/controller-role=true
```

Nothing for the first two, at least one controller pod for the third, and the same topic list
as before. The chart README explains what to do if the upgrade fails part-way.

## Client compatibility

Kafka 4 dropped support for old protocol versions
([KIP-896](https://cwiki.apache.org/confluence/display/KAFKA/KIP-896%3A+Remove+old+client+protocol+API+versions+in+Kafka+4.0)).
The 4.3.1 brokers accept Java clients from 2.1 and librdkafka-based clients (Python, Go, .NET)
from 1.8.2. The clients shipped with Hopsworks 5.2 are within those ranges; check any producer
or consumer you build against the cluster yourself.

The same cut applies the other way round for a
[bring-your-own Kafka cluster](../on_prem/external_kafka_cluster.md): Hopsworks 5.2 connects
with kafka-clients 4.3.1, so the external brokers must run Kafka 2.1 or newer.
