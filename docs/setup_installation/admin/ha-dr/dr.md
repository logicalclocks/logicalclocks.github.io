# Disaster Recovery

## Backup
The state of a Hopsworks cluster is split between data and metadata and distributed across multiple services. This section explains how to take consistent backups for the offline and online feature stores as well as cluster metadata.

In Hopsworks, a consistent backup should back up the following services:

* **RonDB**: cluster metadata and the online feature store data.
* **HopsFS**: offline feature store data plus checkpoints and logs for feature engineering applications.
* **Opensearch**: search metadata, logs, dashboards, and user embeddings.
* **Kubernetes objects**: cluster credentials, backup metadata, serving metadata, and project namespaces with service accounts, roles, secrets, and configmaps.

Besides the above services, Hopsworks uses also Apache Kafka which carries in-flight data heading to the online feature store. In the event of a total cluster loss, running jobs with in-flight data must be replayed.

### Prerequisites
When enabling backup in Hopsworks, cron jobs are configured for RonDB and Opensearch. For HopsFS, backups rely on versioning in the object store. For Kubernetes objects, Hopsworks uses Velero to snapshot the required resources. Before enabling backups:

- Enable versioning on the S3-compatible bucket used for HopsFS.
- Install and configure Velero with the AWS plugin (S3).

#### Install Velero
Velero provides backup and restore for Kubernetes resources. Install it with either the Velero CLI or Helm (Velero docs [here](https://velero.io/docs/v1.17/basic-install/)).

- Using the Velero CLI, set up the CRDs and deployment:
```bash
velero install \
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

## Restore
!!! Note
    Restore is only supported in a newly created cluster; in-place restore is not supported.

The restore process has two phases:

- Restore Kubernetes objects required for the cluster restore.
- Install the cluster with Helm using the correct backup IDs.

### Restore Kubernetes objects
Restore the Kubernetes objects that were backed up using Velero.

- Ensure that Velero is installed and configured with the AWS plugin as described in the [prerequisites](#prerequisites).
- Set up a [Velero backup storage location](https://velero.io/docs/v1.17/api-types/backupstoragelocation/) to point to the S3 bucket.
    - If you are using AWS S3:
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
    cat << EOF > bsl-credentials
    [default]
    aws_access_key_id=YOUR_ACCESS_KEY
    aws_secret_access_key=YOUR_SECRET_KEY
    EOF

    kubectl create secret generic -n velero bsl-credentials --from-file=cloud=bsl-credentials

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
        name: bsl-credentials
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
RESTORE_SUFFIX=$(date +%s)
kubectl apply -f - <<EOF
apiVersion: velero.io/v1
kind: Restore
metadata:
  name: k8s-backups-main-restore-$RESTORE_SUFFIX
  namespace: velero
spec:
  scheduleName: k8s-backups-main
EOF

echo "=== Waiting for Velero restore to finish ==="
until [ "$(kubectl get restore k8s-backups-main-restore-$RESTORE_SUFFIX -n velero -o jsonpath='{.status.phase}' 2>/dev/null)" = "Completed" ]; do
  echo "Still waiting..."; sleep 5;
done

# Restores the latest - if specific backup is needed then backupName instead
echo "=== Creating Velero Restore object for k8s-backups-users-resources ==="
kubectl apply -f - <<EOF
apiVersion: velero.io/v1
kind: Restore
metadata:
  name: k8s-backups-users-resources-restore-$RESTORE_SUFFIX 
  namespace: velero
spec:
  scheduleName: k8s-backups-users-resources
EOF

echo "=== Waiting for Velero restore to finish ==="
until [ "$(kubectl get restore k8s-backups-users-resources-restore-$RESTORE_SUFFIX -n velero -o jsonpath='{.status.phase}' 2>/dev/null)" = "Completed" ]; do
  echo "Still waiting..."; sleep 5;
done
```

### Restore on Cluster installation 
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

#### Customizations
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
