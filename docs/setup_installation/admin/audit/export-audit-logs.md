# Export Audit Logs

## Introduction

Audit logs can be exported to your storage of preference. In case audit logs have not been configured yet in your Hopsworks cluster, please see [Access Audit Logs](../audit/audit-logs.md).

!!! note 
        As an example, in this guide we will show how to export audit logs to BigQuery using the ```bq``` command-line tool.

## Prerequisites

In order to export audit logs you need SSH access to the Hopsworks cluster.

## Step 1: Create a BigQuery Table

Create a dataset and a table in [BigQuery](https://cloud.google.com/bigquery/docs/datasets#console).

The table schema is shown below.

```
fullname	      mode	    type	    description
pathInfo	      NULLABLE	STRING	
methodName	      NULLABLE	STRING	
caller	          NULLABLE	RECORD	
dateTime	      NULLABLE	TIMESTAMP	bq-datetime
userAgent	      NULLABLE	STRING	
clientIp	      NULLABLE	STRING	
outcome	          NULLABLE	STRING	
parameters	      NULLABLE	STRING	
className	      NULLABLE	STRING	
caller.userId	  NULLABLE	STRING	
caller.email	  NULLABLE	STRING	
caller.username	  NULLABLE	STRING
```

## Step 2: Export Audit Logs to the BigQuery Table

Audit logs can be exported in different formats. For instance, to export audit logs in JSON format set ```audit_log_file_type=io.hops.hopsworks.audit.helper.JSONLogFormatter```.

!!! info
        For more information on how to configure the audit log file type see the ```audit_log_file_type``` configuration variable in [Audit logs](../audit/audit-logs.md#step-1-configure-audit-logs).

To export the audit logs to the BigQuery table created in the previous step, run the following command.

```sh
bq load --project_id <projectId> \
        --source_format=NEWLINE_DELIMITED_JSON \
        <DATASET.TABLE> \
        /srv/hops/domains/domain1/logs/audit/server_audit_log0.log
```

!!! tip
        This command can be configured to run periodically on a given schedule by setting up a cronjob.

## Conclusion

In this guide you showed how you can export audit logs in your Hopsworks cluster to a BigQuery table.