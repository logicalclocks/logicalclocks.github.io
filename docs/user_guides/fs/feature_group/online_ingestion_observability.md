---
description: Documentation on Online ingestion observability in Hopsworks.
---

# Online ingestion observability

## Introduction

Knowing when ingested data becomes available for online serving—and understanding the cause of any ingestion failures—is crucial for users. To address this, the Hopsworks API provides observability features for online ingestion, allowing you to monitor ingestion status and troubleshoot issues.

This guide explains how to use these observability features for online feature groups in Hopsworks, with examples using both the HSFS APIs and the user interface.

## Prerequisites

Before you begin this guide we suggest you read the [Feature Group](../../../concepts/fs/feature_group/fg_overview.md) concept page to understand what a feature group is and how it fits in the ML pipeline.

## Using the Hopsworks API

### Create a Feature Group and Ingest Data

First, create an online-enabled feature group and insert data into it:

=== "Python"

    ```python
    fg = fs.create_feature_group(
        name="feature_group_name",
        version=feature_group_version,
        primary_key=feature_group_primary_keys,
        online_enabled=True
    )

    fg.insert(fg_df)
    ```

### Retrieve Online Ingestion Status

After inserting data, you can monitor the ingestion progress:

**Get the latest ingestion instance**

=== "Python"

    ```python
    oi = fg.get_latest_online_ingestion()
    ```

**Get a specific ingestion by its ID**

=== "Python"

    ```python
    oi = fg.get_online_ingestion(ingestion_id)
    ```

### Use the Online Ingestion Object

The online ingestion object provides methods to track and debug the ingestion process:

**Wait for completion**

Wait for the online ingestion to finish (equivalent to `fg.insert(fg_df, wait=True)`):

=== "Python"

    ```python
    oi.wait_for_completion()
    ```

**Print mini-batch results**

Check the results of the ingestion. If the status is `UPSERTED` and the number of rows matches your data, the ingestion was successful:

=== "Python"

    ```python
    print([result.to_dict() for result in oi.results])
    # Example output: [{'onlineIngestionId': 1, 'status': 'UPSERTED', 'rows': 10}]
    ```

**Print ingestion service logs**

Retrieve logs from the online ingestion service to diagnose any issues:

=== "Python"

    ```python
    oi.print_logs(priority="error", size=5)
    ```

## Using the UI

### Viewing Online Ingestion Status

After inserting data into an online-enabled feature group, you can track the ingestion progress in the `Recent activities` section of the feature group in the Hopsworks UI.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/feature_group/online_ingestion.png" alt="See online ingestion status">
  </figure>
</p>
