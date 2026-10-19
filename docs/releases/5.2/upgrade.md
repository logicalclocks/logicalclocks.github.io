# Upgrading to Hopsworks 5.2 { #upgrading-to-5-2 }

Upgrade from 5.1, then follow the steps of each 5.2 release after yours, oldest first.
Act on the breaking changes of every release you upgrade across too; [the release notes][hopsworks-5-2] list them per release.
Releases without steps are not listed here.

## From 5.1 { #upgrading-to-5-2-0 }

### Before the upgrade

1. Required: back up the cluster as described in [Disaster recovery](https://docs.hopsworks.ai/5.1/setup_installation/admin/ha-dr/dr/#backup), and check that the backup completed, because the Kafka and OpenSearch migrations can't be undone.
2. Required if you run satellite clusters: put central and its satellites all under Helm or all under ArgoCD, upgrade every satellite to 5.1, and then upgrade every satellite to 5.2 before central.
3. Required: act on the breaking changes of [5.2.0][hopsworks-5-2-0], and if you upgrade with `--reuse-values`, use `--reset-then-reuse-values` instead, because `--reuse-values` keeps the 5.1 defaults.
4. Required: run the Kafka checks in [Before upgrading: Kafka][helm-upgrade-kafka] and prepare as in [Before you start][docs-kafka4-before].
5. Required on a cluster installed before 5.1: plan the OpenSearch outage, and raise `olk.opensearch.indexUpgrade.activeDeadlineSeconds` (3600) for large indices, as in [OpenSearch 3.8.0][helm-upgrade-opensearch].
   Don't use `olk.opensearch.indexUpgrade.enabled: false` as a dry run, because the Kafka migration runs before it.
6. Required if you pull images from a private registry: mirror the new images, and start from the 5.2 [`values.airgap.yaml`][helm-airgap], which sets the registry of each subchart, including the new HopsFS CSI driver and KEDA.
7. Required if you deploy with ArgoCD: sync with `global._hopsworks.mode: upgrade`, without which the Kafka migration, the OpenSearch index pass and the move of the Trino users to HopsFS don't run, and set `trino.auth.adminUserPwd` and `trino.auth.monitoringUserPwd` to the current Trino passwords unless `trino.auth.createSecrets` is `false` ([values][values-trino-auth]).
8. Required if your values set `trino.trino.auth.passwordAuthSecret` or `groupsAuthSecret`: copy those Secrets to `trino-password-file` and `trino-groups-file`, and remove the values.
9. Required if you changed the terminal session length in the admin UI: set `hopsworks.terminal.sessionHours` ([upgrade guide][helm-upgrade-terminal]).

### Upgrade

1. Required: run `helm upgrade`, whose Kafka migration can't be undone, with a `--timeout` of at least three times `kafka.migrationJob.timeoutSeconds` (1800) and at least `olk.opensearch.indexUpgrade.activeDeadlineSeconds` (3600); if it times out, run it again, and it resumes ([what to expect][docs-kafka4-expect]).
2. Required if you deploy with ArgoCD: when the first sync stops at the `strimzi-crd-upgrade` hook, invalidate the cluster cache, hard-refresh the Application and sync again, and add the `ignoreDifferences` entry for the Kafka CRD ([what to expect][docs-kafka4-expect]).
3. Optional, with Helm 4: pass `--server-side=true` to keep the replica counts of HPA-managed workloads ([Helm 4 notes][helm4-replicas]).

### After the upgrade

1. Required on a cluster installed before 5.1: re-ingest the feature groups with embeddings written during the OpenSearch outage ([upgrade guide][helm-upgrade-opensearch]).
2. Required if 5.1 ran with server-side apply: hand the `rss-configuration` ConfigMap back to Helm ([Helm 4 notes][helm4-rss]).
3. Optional: verify [Kafka][docs-kafka4-verify] and [OpenSearch][helm-upgrade-opensearch].
4. Optional, if you manage the Trino authentication Secrets yourself: delete `trino-password-file` and `trino-groups-file`, which Trino no longer reads.
5. Optional: move the cluster to Kubernetes 1.37; under ArgoCD before 3.5 with server-side apply, see [Kubernetes 1.37][helm-upgrade-k8s137] first.

## To 5.2.1 { #upgrading-to-5-2-1 }

### Before the upgrade

1. Required: update your values for the breaking changes of [5.2.1][hopsworks-5-2-1], and upgrade with `--reset-then-reuse-values` instead of `--reuse-values`, which keeps the previous chart's defaults, such as the `olk.opensearch.indexUpgrade.enabled` of 5.2.0, and fails the values schema.
2. Required if you upgrade from 5.1 and the cluster was installed before 5.1: get the OpenSearch report by running the upgrade with `--set olk.opensearch.indexUpgrade.mode=report`, and raise `olk.opensearch.indexUpgrade.activeDeadlineSeconds` above its estimate if needed ([upgrade steps][docs-os-steps]).
3. Required if the report warns that an embedding index stays blocked for more than about 45 seconds: turn vector ingestion off on your 5.1 release with `onlinefs.deployment.vectordb.enabled: false`, wait for OnlineFS to roll, and keep it off in the upgrade ([upgrade steps][docs-os-steps]).

### Upgrade

1. Required if you upgrade from 5.1: give `helm upgrade` a `--timeout` at least as long as `olk.opensearch.indexUpgrade.activeDeadlineSeconds`, and if it times out, check with `kubectl get jobs -n hopsworks -l component=opensearch-index-upgrade` that the index pass has finished before you run it again, because a retry starts a second run beside it ([if the hook fails][docs-os-hook-fails]).

### After the upgrade

1. Required: check that an OpenSearch pod logged `Security configuration applied`, or apply it by hand, because that is what takes away the restricted members' read access ([security configuration][docs-os-security]).
2. Required if restricted users were granted access or feature groups were shared on 5.1.0, 5.1.1 or 5.2.0 before the last OpenSearch restart: revoke and grant again, or unshare and share again, because the OpenSearch roles behind them are gone ([security configuration][docs-os-security]).
3. Required if the upgrade from 5.1 copied indices: turn vector ingestion back on, or insert again the rows OnlineFS marked failed, attach again the ISM policies of the copied indices, and take a new snapshot ([upgrade steps][docs-os-steps]).

[docs-os-security]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade_opensearch/#security-configuration
[docs-os-steps]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade_opensearch/#opensearch-upgrade-steps
[docs-os-hook-fails]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade_opensearch/#opensearch-hook-fails
[docs-kafka4-expect]: https://docs.hopsworks.ai/5.2/setup_installation/admin/kafka4/#what-to-expect
[docs-kafka4-before]: https://docs.hopsworks.ai/5.2/setup_installation/admin/kafka4/#before-you-start
[docs-kafka4-verify]: https://docs.hopsworks.ai/5.2/setup_installation/admin/kafka4/#verify
[values-trino-auth]: https://docs.hopsworks.ai/5.2/setup_installation/common/helm_chart_values/trino/#helm.trino.auth.adminUserPwd
[helm-upgrade-kafka]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/UPGRADE.md#before-upgrading-kafka
[helm-upgrade-opensearch]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/UPGRADE.md#opensearch-380
[helm-upgrade-k8s137]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/UPGRADE.md#kubernetes-137
[helm-upgrade-terminal]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/UPGRADE.md#terminal-session-length
[helm4-replicas]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/HELM4_MIGRATION.md#1-specreplicas-on-hpa-managed-workloads
[helm4-rss]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/HELM4_MIGRATION.md#2-rss-configmap-rss-configuration
[helm-airgap]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/values.airgap.yaml
