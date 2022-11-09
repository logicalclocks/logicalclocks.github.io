# Export Audit Logs

## Introduction

In this guide we will use a bash script to export audit logs to BigQuery.


## Prerequisites
To follow this guide you need ssh access to the Hopsworks cluster.

## Step 1: Create BigQuery Table
Create a dataset and a table in [BigQuery](https://cloud.google.com/bigquery/docs/datasets#console).

The table schema is shown below.

```
fullname	      mode	    type	   description
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

To export the audit logs in json format set ```audit_log_file_type=io.hops.hopsworks.audit.helper.JSONLogFormatter```.

See [Audit Logs](audit-logs.md) for more information on how to configure audit log file type.

Run the bash script below to export the audit log to the BigQuery table created in step 1.

```sh
bq load --project_id <projectId> \
        --source_format=NEWLINE_DELIMITED_JSON \
        <DATASET.TABLE> \
        /srv/hops/domains/domain1/logs/audit/server_audit_log0.log
```

The above command can be configured to run periodically on a given schedule by setting up a cronjob.

## Conclusion

In this guide you learned how to export audit logs to BigQuery.