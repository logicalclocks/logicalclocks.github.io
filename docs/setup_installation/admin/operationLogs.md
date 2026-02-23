---
description: Guide on how to manage async service operations as a Hopsworks administrator
---

# Service Operations

Service Operations provides a centralized view of asynchronous operations executed across Hopsworks services. Operations are handled by a timer-based system that manages execution, retries, and tracking across multiple service handlers.

## Overview

Asynchronous operations in Hopsworks are processed by background timers rather than executing immediately. Each operation can be handled by multiple services, with each service registering its own handler. The Service Operations interface allows administrators to:

- Monitor ongoing and completed operations
- View operation status per service
- Track retry attempts and failures
- Reset failed operations
- View operation history

<figure>
  <img src="../../../assets/images/admin/operation-logs/operation-logs.png" alt="Service Operations" />
  <figcaption>Service Operations</figcaption>
</figure>

## Operation Status

Each operation displays status information for every service that has registered a handler. The status table shows:

- **Operation ID**: Unique identifier for the operation
- **Service**: The service handling this operation
- **Status**: Current state (pending, running, completed, failed)
- **Retry count**: Number of retry attempts made
- **Last execution**: Timestamp of the most recent execution attempt

Click on an operation to view detailed status messages and execution logs.

<figure>
  <img src="../../../assets/images/admin/operation-logs/operation-logs-msg.png" alt="Service Operations status message" />
  <figcaption>Service Operations status message</figcaption>
</figure>

## Retry Mechanism

When an operation fails for a service, the system automatically retries using exponential backoff:

- **Exponential backoff**: Retry intervals increase exponentially (e.g., 1 min, 2 min, 4 min, 8 min, etc.)
- **Daily limit**: Operations are retried up to a maximum number of times per day
- **Successful operations**: Automatically removed from the active list and moved to history

This approach prevents overwhelming services with continuous retries while allowing temporary failures to resolve automatically.

## Resetting Backoff

For operations with more than 10 retry attempts, administrators can manually reset the backoff:

1. Locate the failed operation in the Service Operations list
2. Click on the operation to view details
3. If the retry count exceeds 10, a "Reset Backoff" button will be available
4. Click to reset the backoff to its initial value

This allows the operation to retry sooner after you've resolved the underlying issue.

## Operation History

Completed and failed operations are retained in the system for a configurable number of days. After the retention period expires, operations are automatically purged from history. This keeps the operation log manageable while preserving recent historical data for troubleshooting and auditing.


## Configuration

Service Operations behavior can be customized through cluster configuration variables. To modify these settings, navigate to **Cluster Settings** → **Configuration** and search for the variable name.

**Available Variables:**

- **async_services_timer_enabled**: Enable or disable the async services timer (default: `true`)
- **async_services_timer_interval_ms**: Timer execution interval in milliseconds (default: `15000` = 15 seconds)
- **async_services_timer_delete_history_after_days**: Days to retain operation history (default: `7`)
- **async_services_timer_batch_size**: Maximum operations processed per timer execution (default: `1000`)

Adjust these values to balance system responsiveness, resource usage, and historical data retention.

## Best Practices

- **Monitor regularly**: Check Service Operations to identify recurring failures
- **Investigate failures**: Click on failed operations to review error messages and identify root causes
- **Reset when appropriate**: Use backoff reset after fixing issues to speed up recovery
- **Configure retention**: Set operation history retention based on compliance and troubleshooting needs
- **Track patterns**: Look for patterns in failures that may indicate systemic issues