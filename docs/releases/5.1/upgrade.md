# Upgrading to Hopsworks 5.1 { #upgrading-to-5-1 }

Upgrade from 5.0, then follow the steps of each 5.1 release after yours, oldest first.
Act on the breaking changes of every release you upgrade across too; [Hopsworks 5.1][hopsworks-5-1] lists them per release.
Releases without steps are not listed here.

## From 5.0 { #upgrading-to-5-1-0 }

### Before the upgrade

1. Required if you run a 5.0 release before 5.0.13: follow the steps of the 5.0 releases after yours in [Upgrading to Hopsworks 5.0][upgrading-to-5-0], because 5.1.0 includes their changes.
2. Required: back up the cluster as described in [Disaster recovery](https://docs.hopsworks.ai/5.0/setup_installation/admin/ha-dr/dr/), because the upgrade migrates the Hive Metastore schema from 3.0 to 4.1 and OpenSearch from 1.3 to 2.19, which can't be rolled back.
3. Required: check that the cluster runs Kubernetes 1.34 or later.

    ```sh
    kubectl version
    ```

4. Required: update your values for the breaking changes of [5.1.0][hopsworks-5-1-0].
   To find the removed settings in the values of the current release, run:

    ```sh
    helm get values <release-name> -n <namespace> -o yaml | grep -n -E 'brewer|hive_default_quota|enable_conda_install|jupyter_spark_driver_memory_overhead_factor|disable_hostname'
    ```

5. Required if you upgrade with `--reuse-values`: use `--reset-then-reuse-values` instead, because `--reuse-values` keeps the defaults of the 5.0 chart, such as `brewer`, which the values schema rejects.
6. Required: check that `hopsworks.variables.admin_email` and `hopsworks.variables.admin_password` in your values, or their defaults if unset, sign in to the Hopsworks admin account.
   The post-upgrade search index rebuild signs in with them and fails the `helm upgrade` when it can't, and its retries can lock the account; if password login is disabled, upgrade to [5.1.1][hopsworks-5-1-1] instead.
7. Required: set `olk.opensearch.knn.circuit_breaker.triggered: false` and `olk.opensearch.knn.circuit_breaker.percent: 75`, or upgrade to [5.1.1][hopsworks-5-1-1] instead, where these are the defaults.
   With the 5.1.0 defaults, OpenSearch drops unflushed vectors and rejects vector writes for about two minutes on its first start on 5.1; inserting the rows again restores lost vectors.
8. Optional, if you upgrade from 5.0.13: upgrade to [5.1.1][hopsworks-5-1-1] instead, because 5.1.0 ships an older RonDB chart without `rondb.rondb.rdrs.probes`, so the RonDB REST server restarts again during a data node failure.

### After the upgrade

1. Optional: check that OpenSearch runs 2.19 and is healthy, as in step 2 of [Upgrading OpenSearch](https://docs.hopsworks.ai/5.2/setup_installation/admin/upgrade_opensearch/#upgrade-steps).
2. Optional, if you manage the Trino authentication Secrets yourself (`trino.auth.createSecrets: false`) and use Velero: label them so backups include them.

    ```sh
    kubectl label secret -n <namespace> trino-admin-credentials trino-monitoring-credentials trino-password-file trino-groups-file backup.hops.works/include=true
    ```

## To 5.1.1 { #upgrading-to-5-1-1 }

### Before the upgrade

1. Required if you upgrade with `helm upgrade --reuse-values`, or with values that set `olk.opensearch.knn.circuit_breaker.triggered: true` or `olk.opensearch.knn.circuit_breaker.percent: 0.75`: set them to `false` and `75`.
   `--reuse-values` keeps the defaults of the previous chart; `--reset-then-reuse-values` doesn't.
