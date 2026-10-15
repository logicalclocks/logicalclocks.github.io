# Upgrading to Hopsworks 5.0 { #upgrading-to-5-0 }

Upgrade from 4.8, then follow the steps of each 5.0 release after yours, oldest first.
Act on the breaking changes of every release you upgrade across too; [Hopsworks 5.0][hopsworks-5-0] lists them per release.
Releases without steps are not listed here.

## From 4.8 { #upgrading-to-5-0-0 }

### Before the upgrade

1. Required if you run 4.8.13 or later, or use Airflow with more than one MySQL server: upgrade to the latest 5.0 release instead of 5.0.0.
   5.0.0 doesn't install on Kubernetes 1.35 or 1.36, which 4.8.13 supports; it ships older RonDB and image builds than 4.8.14 and later; and its Airflow migration loses tables with more than one MySQL server.
2. Required: back up the cluster as described in [Disaster recovery](https://docs.hopsworks.ai/5.0/setup_installation/admin/ha-dr/dr/), because the upgrade drops the Airflow database and migrates the HopsFS and Hive Metastore schemas, which can't be rolled back.
3. Required: update your values for the breaking changes of [5.0.0][hopsworks-5-0-0].
   To find the removed settings in the values of the current release, run the command below, and also check whether they set `superset.mysql.enabled` or `superset.superset.redis.enabled` to `false`.

    ```sh
    helm get values <release-name> -n <namespace> -o yaml | grep -n -E 'jupyter_shell_command|dlthub_image_name|executorService'
    ```

4. Optional, if you use Airflow: write down the Variables and Connections you created in Airflow, and any DAG run history you need.
5. Optional, if you use Airflow: back up `Projects/<project>/Airflow/` of each project in HopsFS, to keep the Airflow 1.10 versions of your DAG files.

### After the upgrade

1. Required, if you use Airflow: port your Airflow 1.10 DAGs to Airflow 3, and regenerate the DAGs created in the Hopsworks UI, as described in [Airflow 3 in Hopsworks](https://docs.hopsworks.ai/5.0/user_guides/projects/airflow/airflow3_upgrade/).

## To 5.0.13 { #upgrading-to-5-0-13 }

### Before the upgrade

1. Required if Airflow or its migration Job failed after an earlier 5.0 upgrade on a cluster with more than one MySQL server: drop the `airflow` database on every MySQL server, which can't be undone, then run the upgrade.
2. Required if a release ran with `kafka.cluster.kafka.quotas.defaults.enabled: true`: check for the client-id default quota that the removed Job wrote, because the upgrade leaves it in Kafka.
   It is enforced on clusters first installed on Hopsworks 4.3 or 4.5, and on other clusters as soon as you switch to `type: kafka`.
   Run the command with the client configuration of a Kafka superuser:

    ```sh
    kafka-configs.sh --bootstrap-server <bootstrap-server> --command-config <client-config> --describe --entity-type clients
    ```

### After the upgrade

1. Optional: remove the leftover client-id default quota.

    ```sh
    kafka-configs.sh --bootstrap-server <bootstrap-server> --command-config <client-config> \
      --entity-type clients --entity-default --alter \
      --delete-config producer_byte_rate,consumer_byte_rate,request_percentage
    ```
