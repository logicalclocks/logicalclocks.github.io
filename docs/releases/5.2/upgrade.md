# Upgrading to Hopsworks 5.2 { #upgrading-to-5-2 }

Upgrade from 5.1, then follow the steps of each 5.2 release after yours, oldest first.
Act on the breaking changes of every release you upgrade across too; [Hopsworks 5.2][hopsworks-5-2] lists them per release.
Releases without steps are not listed here.

## From 5.1 { #upgrading-to-5-2-0 }

The chart's [upgrade guide][helm-upgrade-guide] describes these steps in more detail.

### Before the upgrade

1. Required if you run 5.1.0: follow [To 5.1.1][upgrading-to-5-1-1], because 5.2.0 includes the changes of 5.1.1.
2. Required: back up the cluster as described in [Disaster recovery](https://docs.hopsworks.ai/5.1/setup_installation/admin/ha-dr/dr/), because the Kafka and OpenSearch migrations can't be undone.
3. Required: upgrade every satellite to 5.1, and then to 5.2 before central.
4. Required: update your values for the breaking changes of [5.2.0][hopsworks-5-2-0], and upgrade with `--reset-then-reuse-values` instead of `--reuse-values`, which keeps the 5.1 defaults.
5. Required: run the Kafka checks in [Before upgrading: Kafka][helm-upgrade-kafka] and prepare as in [Before you start][docs-kafka4-before].
6. Required on a cluster installed before 5.1: plan the OpenSearch outage and timeout as in [Upgrading OpenSearch][docs-os-index-pass].
   Don't use `olk.opensearch.indexUpgrade.enabled: false` as a dry run, because the Kafka migration runs before it.
7. Required if you pull images from a private registry: mirror the new images, and start from the 5.2 [`values.airgap.yaml`][helm-airgap], which sets the registry of each subchart, including the new HopsFS CSI driver and KEDA.
8. Required if you deploy with ArgoCD: set `trino.auth.adminUserPwd` and `trino.auth.monitoringUserPwd` to the current Trino passwords, and sync with `global._hopsworks.mode: upgrade`, so that the Trino users move to HopsFS ([values][values-trino-auth]).
9. Required if your values set `trino.trino.auth.passwordAuthSecret` or `groupsAuthSecret`: copy those Secrets to `trino-password-file` and `trino-groups-file`, and remove the values.
10. Required if you changed the terminal session length in the admin UI: set `hopsworks.terminal.sessionHours` ([chart upgrade guide][helm-upgrade-terminal]).

### Upgrade

1. Required: run `helm upgrade` with a `--timeout` that covers the Kafka migration and the OpenSearch index pass; if it times out, run it again, and it resumes ([what to expect][docs-kafka4-expect]).
2. Required if you deploy with ArgoCD: when the first sync stops after the Kafka migration, invalidate the cluster cache and sync again, and add the `ignoreDifferences` entry for the Kafka CRD ([what to expect][docs-kafka4-expect]).
3. Optional, with Helm 4: pass `--server-side=true` to keep the replica counts of HPA-managed workloads ([Helm 4 notes][helm4-replicas]).

### After the upgrade

1. Required on a cluster installed before 5.1: re-ingest the feature groups with embeddings written during the OpenSearch outage ([plan for an outage][docs-os-outage]).
2. Required if 5.1 ran with server-side apply: hand the `rss-configuration` ConfigMap back to Helm ([Helm 4 notes][helm4-rss]).
3. Optional: verify [Kafka][docs-kafka4-verify] and [OpenSearch][docs-os-steps].
4. Optional, if you manage the Trino authentication Secrets yourself: delete `trino-password-file` and `trino-groups-file`, which Trino no longer reads.
5. Optional: move the cluster to Kubernetes 1.37; under ArgoCD before 3.5 with server-side apply, see [Kubernetes 1.37][helm-upgrade-k8s137] first.

[docs-kafka4-before]: https://docs.hopsworks.ai/5.2/setup_installation/admin/kafka4/#before-you-start
[docs-kafka4-expect]: https://docs.hopsworks.ai/5.2/setup_installation/admin/kafka4/#what-to-expect
[docs-kafka4-verify]: https://docs.hopsworks.ai/5.2/setup_installation/admin/kafka4/#verify
[docs-os-index-pass]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade_opensearch/#the-index-pass-on-51x-to-52x
[docs-os-outage]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade_opensearch/#plan-for-an-outage
[docs-os-steps]: https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade_opensearch/#upgrade-steps
[helm-airgap]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/values.airgap.yaml
[helm-upgrade-guide]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/UPGRADE.md#51x-to-52x
[helm-upgrade-k8s137]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/UPGRADE.md#kubernetes-137
[helm-upgrade-kafka]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/UPGRADE.md#before-upgrading-kafka
[helm-upgrade-terminal]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/UPGRADE.md#terminal-session-length
[helm4-replicas]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/HELM4_MIGRATION.md#1-specreplicas-on-hpa-managed-workloads
[helm4-rss]: https://github.com/logicalclocks/hopsworks-helm/blob/v5.2.0/HELM4_MIGRATION.md#2-rss-configmap-rss-configuration
[values-trino-auth]: https://docs.hopsworks.ai/5.2/setup_installation/common/helm_chart_values/trino/#helm.trino.auth.adminUserPwd
