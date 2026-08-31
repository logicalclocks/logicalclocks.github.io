# Disaster Recovery

## Backup

The state of a Hopsworks cluster is split between data and metadata and distributed across multiple services. This section explains how to take consistent backups for the offline and online feature stores as well as cluster metadata.

In Hopsworks, a consistent backup should back up the following services:

- **RonDB**: cluster metadata and the online feature store data.
- **HopsFS**: offline feature store data plus checkpoints and logs for feature engineering applications.
- **Opensearch**: search metadata, logs, dashboards, and user embeddings.
- **Superset**: dashboards, charts, saved queries, database connections, and users and roles, stored in the Superset metadata database, which is a separate MySQL from RonDB.
- **Kubernetes objects**: cluster credentials, backup metadata, serving metadata, Trino authentication (password and group files plus the admin and monitoring credentials), and project namespaces with service accounts, roles, secrets, and configmaps.
- **Python environments**: custom project environments are stored in your configured container registry. Back up the registry separately. If a project and its environment are deleted, you must recreate the environment after restore.

Besides the above services, Hopsworks uses also Apache Kafka which carries in-flight data heading to the online feature store. In the event of a total cluster loss, running jobs with in-flight data must be replayed.

### Prerequisites

When enabling backup in Hopsworks, cron jobs are configured for RonDB and Opensearch. For HopsFS, backups rely on versioning in the object store. For Kubernetes objects, Hopsworks uses Velero to snapshot the required resources. Before enabling backups:

- Enable versioning on the S3-compatible bucket used for HopsFS.
- Install and configure Velero with the AWS plugin (S3).

#### Install Velero

Velero provides backup and restore for Kubernetes resources. Install it with either the Velero CLI or Helm (Velero docs: [Velero basic install guide](https://velero.io/docs/v1.17/basic-install/)).

- Using the Velero CLI, set up the CRDs and deployment:

```bash
velero install \
    --image velero/velero:v1.17.1 \
    --plugins velero/velero-plugin-for-aws:v1.13.0 \
    --no-default-backup-location \
    --no-secret \
    --use-volume-snapshots=false \
    --wait
```

- Using the Velero Helm chart:

```bash
helm repo add vmware-tanzu https://vmware-tanzu.github.io/helm-charts
helm repo update

helm install velero vmware-tanzu/velero \
  --namespace velero \
  --version 11.2.0 \
  --create-namespace \
  --set "initContainers[0].name=velero-plugin-for-aws" \
  --set "initContainers[0].image=velero/velero-plugin-for-aws:v1.13.0" \
  --set "initContainers[0].volumeMounts[0].mountPath=/target" \
  --set "initContainers[0].volumeMounts[0].name=plugins" \
  --set-json configuration.backupStorageLocation='[]' \
  --set "credentials.useSecret=false" \
  --set "snapshotsEnabled=false" \
  --wait
```

### Configuring Backup

!!! Note
    Backup is only supported for clusters that use S3-compatible object storage.

You can enable backups during installation or a later upgrade. Set the schedule with a cron expression in the values file:

```yaml
global:
  _hopsworks:
    backups:
      enabled: true
      schedule: "@weekly"
```

After configuring backups, go to the cluster settings and open the Backup tab. You should see `enabled` at the top level and for all services if everything is configured correctly.

<figure>
  <img width="800px" src="../../../../assets/images/admin/ha_dr/backup.png" alt="Backup overview page"/>
  <figcaption>Backup overview page</figcaption>
</figure>

If any service is misconfigured, the backup status shows as `partial`. In the example below, Velero is disabled because it was not configured correctly. Fix partial backups before relying on them for recovery.

<figure>
  <img width="800px" src="../../../../assets/images/admin/ha_dr/backup_partial.png" alt="Backup overview page (partial setup)"/>
  <figcaption>Backup overview page (partial setup)</figcaption>
</figure>

#### Cleanup

Use the backup time-to-live (`ttl`) flag to automatically prune backups older than the configured duration.

```yaml
global:
  _hopsworks:
    backups:
      enabled: true
      schedule: "@weekly"
      ttl: 60d
```

For S3 object storage, you can also configure a bucket lifecycle policy to expire old object versions. Example for AWS S3:

```json
{
  "Rules": [
    {
      "ID": "HopsFSBlocksRetentionPolicy",
      "Status": "Enabled",
      "Filter": {},
      "Expiration": {
        "ExpiredObjectDeleteMarker": true
      },
      "NoncurrentVersionExpiration": {
        "NoncurrentDays": 60
      }
    }
  ]
}
```

### Superset { #superset-backup }

Superset stores its state in its own MySQL database, which is separate from RonDB and is therefore not part of the RonDB backup.
When backups are enabled, a `create-superset-backup` cron job takes a logical dump of the Superset database and uploads it to the same object storage as the other backups, under the `superset_backup/<backup-id>/` prefix.
The dump covers the whole `superset` schema, so it includes the database connections (connectors) along with dashboards, charts, saved queries, users and roles.
That includes the connections Hopsworks creates itself, such as the per-project Trino connections, because they are rows in the same database.
Connector credentials are stored encrypted with the Superset secret key, so they are only usable after a restore if that key is restored with the database, which is why the restore verifies it (see [Superset restore][superset-restore]).
Each backup writes two objects: `superset.sql.gz` (the gzipped dump) and `manifest.json` (the dump checksum, the Superset image and schema version, and a fingerprint of the Superset secret key).
The backup is also indexed in the `superset-backups-metadata` ConfigMap, which the Velero backup captures so the index is restored with the cluster.

Superset's Kubernetes Secrets are captured by the Velero backup through the `backup.hops.works/include` label:

- `superset-secret-key`: the Superset secret key.
  It must be restored together with the database, because Superset uses it to encrypt the database-connection passwords stored in the metadata database, so restoring the database with a different secret key leaves those connections undecryptable.
- `superset-mysql-users-secrets`: the Superset MySQL credentials.
- `superset-admin-credentials`: the Superset admin account.

If you provide these Secrets yourself by setting `superset.auth.createSecrets: false`, you must add the label `backup.hops.works/include: "true"` to each of them, because the chart only labels the Secrets it creates and Velero selects Secrets by that label.

To list the Superset backups that were taken, read the metadata ConfigMap:

```bash
kubectl get configmap superset-backups-metadata -n hopsworks -o json \
| jq -r '.data | to_entries[] | select(.value | fromjson | .state == "SUCCESS") | .key' \
| sort -r
```

!!! note
    Backups taken before Superset backup was enabled do not contain Superset.
    Restoring from such a backup recovers the rest of the cluster but not Superset dashboards, charts, or users.

### Trino authentication

Trino authenticates users against a password file and authorizes them against a group file.
Both files, together with the Trino admin and monitoring credentials, live in Kubernetes Secrets that are labelled so the `k8s-backups-main` Velero schedule captures them.
They are therefore included in the Kubernetes-objects backup and no extra configuration is required.

After a restore, Hopsworks rebuilds the Trino password and group files from the restored RonDB state.
The rebuild runs on the primary backend instance shortly after startup and then periodically, so an existing project user can authenticate to Trino and holds exactly the access their restored project role grants.
This means a restore recovers Trino authentication automatically, without an operator step.

!!! note
    This holds for backups taken after this feature was deployed.
    A backup taken before it does not contain the Trino Secrets, because they were not yet labelled for the `k8s-backups-main` schedule, and an existing cluster first has such a backup only after its next backup cycle.
    Restoring from an older backup still recovers all RonDB-derived authentication, because the reconciliation rebuilds the project users, their role groups, and the shared-dataset groups from the restored RonDB state.
    It does not recover the admin and monitoring credential entries: those are re-rendered from the chart values on a fresh install, so any out-of-band rotation of them is lost and Prometheus may need its Trino monitoring credentials re-aligned.

The Trino internal shared secret is deliberately not backed up.
It has no coupling to user state and is regenerated on a fresh install, and restoring an old value onto a running cluster would break Trino internal communication until every Trino pod restarts.
If you set `createSharedSecret: false` and manage this secret yourself, restore it from your own source and then restart all Trino pods together so the coordinator and workers share the same value.

!!! warning
    The backup contains the Trino admin credentials, which are only base64-encoded at the Kubernetes layer.
    Restrict access to the backup object store and enable encryption at rest so the backup does not expose usable credentials.

!!! note
    On ArgoCD-managed clusters with automated self-healing, add `ignoreDifferences` on the `data` field of the four Trino auth Secrets (`trino-password-file`, `trino-groups-file`, `trino-admin-credentials`, `trino-monitoring-credentials`) and set `RespectIgnoreDifferences=true` in the Application sync options.
    Hopsworks writes project users and groups into these Secrets at runtime, so without this ArgoCD reapplies the chart defaults on every sync and overwrites the restored authentication data.

## Restore

Hopsworks supports two restore modes:

- **New cluster restore**: Install a fresh cluster and restore data from a backup during installation.
- **In-place restore**: Restore data onto an existing running cluster via `helm upgrade`.

!!! Note
    Use the exact Hopsworks version that was used to create the backup.

### New Cluster Restore

The new cluster restore process has two phases:

- Restore Kubernetes objects required for the cluster restore.
- Install the cluster with Helm using the correct backup IDs.

#### Restore Kubernetes objects

Restore the Kubernetes objects that were backed up using Velero.

- Ensure that Velero is installed and configured with the AWS plugin as described in the [prerequisites](#prerequisites).
- Set up a [Velero backup storage location](https://velero.io/docs/v1.17/api-types/backupstoragelocation/) to point to the S3 bucket.

  - If you are using AWS S3 and access is controlled by an IAM role:

    ```bash
    kubectl apply -f - <<EOF
    apiVersion: velero.io/v1
    kind: BackupStorageLocation
    metadata:
    name: hopsworks-bsl
    namespace: velero
    spec:
    provider: aws
    config:
        region: REGION
    objectStorage:
        bucket: BUCKET_NAME
        prefix: k8s_backup
    EOF
    ```

  - If you are using an S3-compatible object storage, provide credentials and endpoint:

    ```bash
    cat << EOF > hopsworks-bsl-credentials
    [default]
    aws_access_key_id=YOUR_ACCESS_KEY
    aws_secret_access_key=YOUR_SECRET_KEY
    EOF

    kubectl create secret generic -n velero hopsworks-bsl-credentials --from-file=cloud=hopsworks-bsl-credentials

    kubectl apply -f - <<EOF
    apiVersion: velero.io/v1
    kind: BackupStorageLocation
    metadata:
    name: hopsworks-bsl
    namespace: velero
    spec:
    provider: aws
    config:
        region: REGION
        s3Url: ENDPOINT
    credential:
        key: cloud
        name: hopsworks-bsl-credentials
    objectStorage:
        bucket: BUCKET_NAME
        prefix: k8s_backup
    EOF
    ```

- After the backup storage location becomes available, restore the backups. The following script restores the latest available backup. To restore a specific backup, set `backupName` instead of `scheduleName`.

```bash
echo "=== Waiting for Velero BackupStorageLocation  hopsworks-bsl to become Available ==="
until [ "$(kubectl get backupstoragelocations hopsworks-bsl -n velero -o jsonpath='{.status.phase}' 2>/dev/null)" = "Available" ]; do
  echo "Still waiting..."; sleep 5;
done

echo "=== Waiting for Velero to sync the backups from hopsworks-bsl ==="
until [ "$(kubectl get backups -n velero -ojson | jq -r '[.items[] | select(.spec.storageLocation == "hopsworks-bsl")] | length' 2>/dev/null)" != "0" ]; do
  echo "Still waiting..."; sleep 5;
done


# Restores the latest - if specific backup is needed then backupName instead
echo "=== Creating Velero Restore object for k8s-backups-main ==="
kubectl apply -f - <<EOF
apiVersion: velero.io/v1
kind: Restore
metadata:
  name: k8s-backups-main
  namespace: velero
spec:
  scheduleName: k8s-backups-main
EOF

echo "=== Waiting for Velero restore to finish ==="
until [ "$(kubectl get restore k8s-backups-main -n velero -o jsonpath='{.status.phase}' 2>/dev/null)" = "Completed" ]; do
  echo "Still waiting..."; sleep 5;
done

# Restores the latest - if specific backup is needed then backupName instead
echo "=== Creating Velero Restore object for k8s-backups-users-resources ==="
kubectl apply -f - <<EOF
apiVersion: velero.io/v1
kind: Restore
metadata:
  name: k8s-backups-users-resources
  namespace: velero
spec:
  scheduleName: k8s-backups-users-resources
EOF

echo "=== Waiting for Velero restore to finish ==="
until [ "$(kubectl get restore k8s-backups-users-resources -n velero -o jsonpath='{.status.phase}' 2>/dev/null)" = "Completed" ]; do
  echo "Still waiting..."; sleep 5;
done
```

After the restore completes, verify the restored resources in Kubernetes. RonDB and Opensearch store their backup metadata in the `rondb-backups-metadata` and `opensearch-backups-metadata` configmaps. Use the commands below to list successful backup IDs (newest first) that can be referenced during cluster installation.

```bash
kubectl get configmap rondb-backups-metadata -n hopsworks -o json \
| jq -r '.data | to_entries[] | select(.value | fromjson | .state == "SUCCESS") | .key' \
| sort -nr

kubectl get configmap opensearch-backups-metadata -n hopsworks -o json \
| jq -r '.data | to_entries[] | select(.value | fromjson | .state == "SUCCESS") | .key' \
| sort -nr
```

#### Restore on Cluster installation

To restore a cluster during installation, configure the backup ID in the values YAML file:

```yaml
global:
  _hopsworks:
    backups:
      enabled: true
      schedule: "@weekly"
    restoreFromBackup:
      backupId: "254811200"
```

##### Customizations

!!! Warning
    Even if you override the backup IDs for RonDB and Opensearch, you must still set `.global._hopsworks.restoreFromBackup.backupId` to ensure HopsFS is restored.

To restore a different backup ID for RonDB:

```yaml
global:
  _hopsworks:
    backups:
      enabled: true
      schedule: "@weekly"
    restoreFromBackup:
      backupId: "254811200"

rondb:
  rondb:
    restoreFromBackup:
      backupId: "254811140"
```

To restore a different backup for Opensearch:

```yaml
global:
  _hopsworks:
    backups:
      enabled: true
      schedule: "@weekly"
    restoreFromBackup:
      backupId: "254811200"

olk:
  opensearch:
    restore:
      repositories:
        default:
          snapshots:
            default:
              snapshot_name: "254811140"
```

You can also customize the Opensearch restore process to skip specific indices:

```yaml
global:
  _hopsworks:
    backups:
      enabled: true
      schedule: "@weekly"
    restoreFromBackup:
      backupId: "254811200"

olk:
  opensearch:
    restore:
      repositories:
        default:
          snapshots:
            default:
              snapshot_name: "254811140"
              payload:
                indices: "-myindex"
```

### In-Place Restore

!!! Note
    In-place restore is available from Hopsworks version 4.8.0.

In-place restore allows you to restore data onto an existing running cluster using `helm upgrade`. Unlike a new cluster restore, this does not require provisioning a fresh cluster — the existing stateful services are shut down, wiped if necessary, and restored from backup.

!!! Warning
    In-place restore **replaces all existing data** in the cluster with the backup data. Any data written after the backup was taken will be lost.

!!! Info
    After a fresh install from backup (new cluster restore), in-place restores can only be performed using backups taken **after** that fresh install, because the cluster certificates are regenerated during installation. To restore to a backup that was taken **before** the fresh install, you must perform another new cluster restore from that backup instead of an in-place restore.

#### In-place restore prerequisites

- A running Hopsworks cluster deployed via Helm.
- A previously created backup with a known backup ID.
- Object storage configured and accessible with the backup data.
- Velero installed and configured as described in the [prerequisites](#prerequisites).

#### Identify the backup ID

Get the backup ID from the **Cluster Settings > Backup** tab or by using the following commands.

```bash
# RonDB backup IDs (newest first)
kubectl get configmap rondb-backups-metadata -n hopsworks -o json \
| jq -r '.data | to_entries[] | select(.value | fromjson | .state == "SUCCESS") | .key' \
| sort -nr

# Opensearch backup IDs (newest first)
kubectl get configmap opensearch-backups-metadata -n hopsworks -o json \
| jq -r '.data | to_entries[] | select(.value | fromjson | .state == "SUCCESS") | .key' \
| sort -nr

# Velero backup IDs for the main schedule (newest first)
kubectl get backups -n velero -o json \
| jq -r '[.items[] | select(.spec.storageLocation == "hopsworks-bsl" and .metadata.labels["velero.io/schedule-name"] == "k8s-backups-main" and .status.phase == "Completed")] | sort_by(.status.completionTimestamp) | reverse[] | .metadata.name'

# Velero backup IDs for the users schedule (newest first)
kubectl get backups -n velero -o json \
| jq -r '[.items[] | select(.spec.storageLocation == "hopsworks-bsl" and .metadata.labels["velero.io/schedule-name"] == "k8s-backups-users-resources" and .status.phase == "Completed")] | sort_by(.status.completionTimestamp) | reverse[] | .metadata.name'
```

#### Run the in-place restore

Configure the restore in the values file and run `helm upgrade`:

```yaml
global:
  _hopsworks:
    backups:
      enabled: true
      schedule: "@weekly"
    restoreFromBackup:
      backupId: "254811200"
      inPlace: true
      forceDataClear: true

# Optional: specify Velero backup IDs. If not set, the latest completed backup is used.
hopsworks:
  velero:
    restore:
      mainScheduleBackupId: "k8s-backups-main-20260213T153627Z"
      usersScheduleBackupId: "k8s-backups-users-resources-20260213T153627Z"
```

Then run:

```bash
helm upgrade hopsworks hopsworks/hopsworks --version <CHART_VERSION> \
  --namespace hopsworks \
  -f values.yaml \
  --timeout 1200s
```

You can also pass the restore flags directly on the command line:

```bash
helm upgrade hopsworks hopsworks/hopsworks --version <CHART_VERSION> \
  --namespace hopsworks \
  --set-string global._hopsworks.restoreFromBackup.backupId="254811200" \
  --set global._hopsworks.restoreFromBackup.inPlace=true \
  --set global._hopsworks.restoreFromBackup.forceDataClear=true \
  --set-string hopsworks.velero.restore.mainScheduleBackupId="k8s-backups-main-20260213T153627Z" \
  --set-string hopsworks.velero.restore.usersScheduleBackupId="k8s-backups-users-resources-20260213T153627Z" \
  --timeout 1200s
```

The required flags are:

| Parameter | Description |
| --------- | ----------- |
| `global._hopsworks.restoreFromBackup.backupId` | The backup ID to restore from. |
| `global._hopsworks.restoreFromBackup.inPlace` | Must be `true` to enable in-place restore mode. |
| `global._hopsworks.restoreFromBackup.forceDataClear` | Must be `true` to confirm that existing data will be replaced. This is a safety mechanism to prevent accidental data loss. |

The following flags are optional. If not set, the latest available Velero backup will be used:

| Parameter | Description |
| --------- | ----------- |
| `hopsworks.velero.restore.mainScheduleBackupId` | The Velero backup ID for the main schedule (`k8s-backups-main`). |
| `hopsworks.velero.restore.usersScheduleBackupId` | The Velero backup ID for the users schedule (`k8s-backups-users-resources`). |

!!! Important
    After a successful restore, remove the `restoreFromBackup` blocks from your values file and run `helm upgrade` to apply the change.
    If left in place, these blocks can cause subsequent upgrades to fail or behave unexpectedly.

#### Re-running an in-place restore

In-place restore creates marker resources to prevent accidental re-runs. If you need to run the restore again with the same backup ID, delete the marker resources first:

```bash
# Delete the HopsFS restore job
kubectl delete job hopsfs-inplace-restore-<BACKUP_ID> -n hopsworks --ignore-not-found=true

# Delete the RonDB restore jobs
kubectl delete job restore-native-backup-<BACKUP_ID> -n hopsworks --ignore-not-found=true
kubectl delete job setup-mysqld-dont-remove-<BACKUP_ID> -n hopsworks --ignore-not-found=true

# Delete the Opensearch restore job
kubectl delete job opensearch-restore-default-default-<BACKUP_ID> -n hopsworks --ignore-not-found=true

# Delete the velero restore objects, use the exact backup name or schedule name
kubectl delete restore.velero.io k8s-backups-main -n velero --ignore-not-found=true
kubectl delete restore.velero.io k8s-backups-users-resources -n velero --ignore-not-found=true
```

#### In-place restore customizations

The same customization options for [RonDB and Opensearch](#customizations) backup IDs apply to in-place restore. You can override individual service backup IDs while keeping the global backup ID for HopsFS.

### Superset restore

Superset is restored by reloading its database from a backup (see [Superset backup][superset-backup]).
Because reloading the database requires Superset to be stopped, the chart holds all Superset workloads at zero replicas while the restore flag is set, and a Job reloads and migrates the database.
The restore is a two-step operation: set the flag and let the Job run to `phase=migrated`, then clear the flag so the workloads resume.

Find the Superset backup id to restore:

```bash
kubectl get configmap superset-backups-metadata -n hopsworks -o json \
| jq -r '.data | to_entries[] | select(.value | fromjson | .state == "SUCCESS") | .key' \
| sort -r
```

Set the Superset restore trigger with the id and the name of the Velero Restore that repopulates the Superset Secrets, then run `helm upgrade`:

```yaml
global:
  _hopsworks:
    restoreFromBackup:
      superset:
        enabled: true
        backupId: "20260722215632-2116913658"
        # The Velero Restore (in the velero namespace) that must reach Completed before the
        # database import; it is what puts superset-secret-key back.
        veleroRestoreName: "restore-main-1737455940"
        # Recorded in the audit trail. Set it to a trusted operator/ticket identity; when unset
        # it defaults to helm/<release>@rev<revision>.
        initiatedBy: "ops:HWORKS-2973 alice"
```

```bash
helm upgrade hopsworks hopsworks/hopsworks --version <CHART_VERSION> \
  --namespace hopsworks \
  -f values.yaml \
  --timeout 1200s
```

The `veleroRestoreName` is required.
It names the Velero Restore that repopulates the Superset Secrets, including `superset-secret-key`, which Superset uses to encrypt the database-connection passwords stored in the metadata database.
The restore Job waits for that Velero Restore to reach `Completed` before it imports the database, so the reloaded rows are always decrypted with the secret key they were encrypted with.
For an in-place restore where the live `superset-secret-key` already matches the backup and no Velero Restore is involved, set `acknowledgeNoVeleroBarrier: true` instead of `veleroRestoreName`, and the import is gated on the secret-key fingerprint alone.

While the Superset restore is enabled, the chart renders every Superset workload (node, worker, celerybeat, websocket, flower) at zero replicas and skips the Superset init Job, so nothing serves or writes the metadata database while it is being reloaded.
This zero-replica barrier is declarative: it is the desired state for as long as the flag is set, which is what makes it safe under both Helm and ArgoCD.
The restore Job runs as a single restartable state machine holding a mutual-exclusion Lease: it waits for the Velero Restore to complete, waits for the (barrier-driven) Superset pods to terminate and verifies none remain, flushes the Superset Redis cache, verifies the dump against the manifest (backup id, object path, size, and sha256) and the restored secret-key fingerprint, reloads the database, and migrates the schema forward.
The Job does not scale Superset back up; its terminal state is `migrated`, and the workloads resume declaratively in the next step.
Migration happens inside the restore Job, using the same `superset_bootstrap.sh` and `superset_init.sh` scripts as a normal install, so a backup taken by an older Superset version is upgraded to the running image's schema during the restore itself, not on a later upgrade.
Every transition is recorded in the `superset-restore-state` ConfigMap, which is the durable audit trail: the initiating identity, the attempt count, and one append-only entry per transition (including a `failed` reason on abort) keyed by backup id.
The recorded initiator is deployment metadata, not an authenticated identity.
It defaults to `helm/<release>@rev<revision>`, and under ArgoCD the revision is always `1` because ArgoCD renders with `helm template`, so set `initiatedBy` explicitly and correlate it with the Kubernetes audit log entry for the Helm or ArgoCD change to identify the actor.

The backup and the restore also exclude each other, and so does the normal Superset init Job: all three take the same `superset-backup-restore` Lease before touching the database.
The init Job matters because it runs `superset db upgrade`, and a logical dump taken with `--single-transaction` is not safe against concurrent DDL.

After the restore Job reaches `migrated`, clear the flag and upgrade again to lift the barrier and bring Superset back up:

```yaml
global:
  _hopsworks:
    restoreFromBackup:
      superset:
        enabled: false
```

This is a required step, not just cleanup: it is what restores the Superset workloads to their normal replica counts.
The normal init Job then runs and no-ops against the already-migrated schema.
Confirm the restore reached `migrated` before clearing the flag:

```bash
kubectl get configmap superset-restore-state -n hopsworks -o jsonpath='{.data.phase}'
```

The `superset-restore-state` ConfigMap is the durable record of how far a restore got, and each phase is idempotent, so a re-created Job continues from the recorded phase instead of repeating destructive work.
A re-created Job is not free of side effects in every case: for an incomplete restore it re-runs the phases that had not finished, and for a completed restore it takes a no-op path through every container and exits.
Phase progress only ever moves forward, which is what makes that true: a retry re-verifies that no Superset process is running, because that has to hold on every attempt, but it will not lower a recorded `imported` back to the start and reload the database a second time.
Either way, deleting the Job alone does not re-run a completed restore.

Two ConfigMaps are involved, and the split is deliberate.
`superset-restore-state` holds the execution state, and its `phase` key is the maintenance fence: while it is anything other than `migrated`, scheduled backups refuse to run so they cannot capture a half-restored database.
`superset-restore-audit` holds the append-only audit trail (one immutable `h-*` entry per transition), which is the durable who/when/which-backup record.
Read the audit trail with:

```bash
kubectl get configmap superset-restore-audit -n hopsworks -o json \
| jq -r '.data | to_entries | map(select(.key|startswith("h-"))) | sort_by(.key) | .[].value'
```

Only the audit ConfigMap carries the `backup.hops.works/include` label, so only the trail is captured by the Velero backup, and it survives loss of the namespace or the cluster.
The execution state is deliberately left out of the backup.
It describes an operation against one particular database, so restoring it onto another cluster would be wrong: a restored `phase=migrated` would claim that a restore had already finished against a database that had never received it, and the next restore of that same backup id would take its no-op path and leave the database untouched.
Because the two are separate objects, clearing the state does not touch the trail.

Nothing prunes the trail automatically: entries accumulate across restores, and a ConfigMap is limited to roughly 1 MiB in total, so on a cluster that is restored very frequently the trail should be exported and pruned as part of normal operations.
Export it before pruning, and keep the export wherever your other operational audit records live:

```bash
kubectl get configmap superset-restore-audit -n hopsworks -o json \
| jq '{exported: now|todate, entries: (.data | with_entries(select(.key|startswith("h-"))))}' \
> superset-restore-audit-$(date -u +%Y%m%d).json
```

To re-run the same backup id, reset the restore state but keep the audit trail:

```bash
kubectl delete job superset-restore-<BACKUP_ID> -n hopsworks --ignore-not-found=true
kubectl patch configmap superset-restore-state -n hopsworks --type merge \
  -p '{"data":{"phase":"","restoreId":"","failed":"","attempts":"","initiator":""}}'
```

To restore a different backup, set its backup id and re-run: the state machine only starts a new restore once the previous one has fully completed (phase `migrated`), and it then resets the per-restore state for the new one by itself.

Deleting the `superset-restore-state` ConfigMap outright also works and leaves the audit trail intact, but it lifts the maintenance fence at the same time, so scheduled backups resume immediately.
Only do that after establishing that the database is in a known-good state.
For a failed restore, verify or recover the database before clearing the fence: the fence exists precisely because a half-restored database must not be backed up over a good one.

#### Fresh-cluster restore

On a brand-new cluster the sequence is the same two steps, with `helm install` in place of the first `helm upgrade`:

1. Restore the platform Velero backup so the Superset Secrets (including `superset-secret-key`) exist on the new cluster, and note the name of that Velero `Restore` object.
2. Install (or sync) the chart with the Superset restore flag set and `veleroRestoreName` pointing at that Velero Restore. The barrier keeps Superset at zero replicas while the restore Job reloads and migrates the database into the freshly-created (empty) MySQL.
3. Wait until `superset-restore-state` reaches `phase=migrated`.
4. Clear the flag (`enabled: false`) and upgrade so the barrier lifts and Superset starts against the restored database.

The `veleroRestoreName` requirement is what guarantees the secret-key is in place before the import, so the restored connection passwords decrypt correctly on the new cluster.

#### Limitations

- The Superset restore is a logical reload of the metadata database, not a point-in-time snapshot coordinated with the RonDB or HopsFS backups.
  The Superset backup and the platform backup are taken independently, so a restore recovers each service to its own most recent backup, not to a single consistent instant across services.
- The Superset MySQL credentials (`superset-mysql-users-secrets`) and the admin account (`superset-admin-credentials`) are fixed at install and are captured and restored as-is from the Velero backup.
  Rotating them is not supported for the lifetime of any cluster you intend to restore in place: an in-place restore rolls the Secrets back to the backed-up values, which would then be out of sync with the live MySQL grants written after a rotation.
  If a rotation is unavoidable, treat it as a re-baseline: rotate, then take a fresh backup, and discard backups taken before the rotation.
- Enabling the Superset restore has no effect unless Superset itself is enabled (`global._hopsworks.superset.enabled=true`); the restore reloads the bundled MySQL and flushes Redis, so both must be enabled (the chart rejects the restore at render time if they are not).
- Connectors are restored as rows with their credentials, and the restore verifies that the secret key matches the backup so those credentials remain decryptable.
  What it cannot guarantee is that a credential is still the right one, for connectors whose password is owned by another service.
  The per-project Trino connections are the case that matters: Hopsworks stores each user's Trino password in its own secret store in RonDB, rebuilds the Trino password file from RonDB, and copies that same password into the Superset connection.
  So the Superset side holds a copy, and RonDB is the source of truth.
  If Superset and RonDB are restored to the same point, the copy matches and the connection works.
  If they are restored to different points, and that user's secret was recreated in between (which happens when a user is removed from a project and added again), the restored Superset connection carries a password Trino no longer accepts.
  The certificate material Superset uses to reach Trino is a CA bundle for verifying Trino's server certificate, not a credential, so its reissue by the certs-operator is expected and harmless.
- A stale connector password does not repair itself, because Hopsworks only creates a connection when one is absent and skips when it already exists.
  After a fresh-cluster restore, confirm Trino access by opening a Trino-backed chart or running a query through a per-project Trino connection.
  If a user's Trino connection fails to authenticate, delete that connection in Superset and let Hopsworks recreate it from the current RonDB secret.

#### ArgoCD

The Superset Secrets (`superset-secret-key`, `superset-mysql-users-secrets`, `superset-admin-credentials`) are generated once and preserved across upgrades using a `lookup` that returns nothing during an offline `helm template`.
Under ArgoCD, which renders with `helm template`, a sync can regenerate these Secrets and overwrite the values a Velero restore put back, which would leave the restored database's encrypted connections undecryptable.
Add an `ignoreDifferences` entry so ArgoCD ignores their data, and the `RespectIgnoreDifferences=true` sync option so it does not re-apply the rendered values during sync.
By default `ignoreDifferences` only affects the diff ArgoCD shows; without `RespectIgnoreDifferences=true` a sync still applies the freshly-rendered Secret values and overwrites the restored ones:

```yaml
spec:
  syncPolicy:
    syncOptions:
      - RespectIgnoreDifferences=true
  ignoreDifferences:
    - group: ""
      kind: Secret
      name: superset-secret-key
      jsonPointers: ["/data"]
    - group: ""
      kind: Secret
      name: superset-mysql-users-secrets
      jsonPointers: ["/data"]
    - group: ""
      kind: Secret
      name: superset-admin-credentials
      jsonPointers: ["/data"]
```

The zero-replica writer barrier is ArgoCD-safe by construction: while the restore flag is set, `helm template` renders every Superset workload at zero replicas, so that is the desired state and self-heal maintains it rather than fighting it.
No auto-sync pause is needed during the reload.
The two steps map directly to two syncs: set the flag and sync (the barrier holds Superset at zero while the restore Job reloads and migrates the database), then clear the flag and sync (the workloads return to their normal replica counts).
Do not clear the flag until the restore has reached `phase=migrated`; while the flag remains set, ArgoCD's desired replica count is zero, so Superset cannot resume.
