---
description: Collect a support archive or configure and use the Hopsworks admin debug terminal.
---

# Cluster diagnostics { #hopsworks-cluster-diagnostics }

Open **Cluster Settings** > **Overview** as a Hopsworks administrator.
Use **Collect logs** for a support archive and **Debug terminal** for an interactive diagnostic session when the terminal is enabled.

## Collect a support archive { #hopsworks-collect-logs }

1. Choose **Collect logs** in the Overview header.
2. Select the time window and enable **RonDB logs** if the investigation needs them and the option is available.
3. Choose **Collect** and review the collection status.
4. Choose **Download** when the archive is ready.
   If the bundle is partial, review the reads the collector could not perform.

The cluster shares one bundle across administrators.
Coordinate with other administrators before canceling a collection or deleting an archive.
Download the bundle before it expires.
If the collection exceeds the size limit, select a shorter time window and retry.
The defaults are a two-hour pod lifetime, including collection and download, and a 2 GiB size limit.
Set `hopsworks.adminDebug.sessionHours` and `hopsworks.adminDebug.bundleMaxSize` in Helm to change those limits.

Collection runs in a dedicated pod using the Hopsworks service account.
For a custom role, check that the account can list and create pods, `get`, `watch` and `delete` the `admin-log-bundle` pod, read pod logs, and use the `pods/exec` subresource for archive status and download.
The collector's permissions determine which additional Kubernetes objects it can include.

Treat the archive as sensitive.
It contains logs and resource descriptions from the Hopsworks namespace and `kube-system`, events from every namespace, and node descriptions, which list every pod on the node, project pods included.
Resource descriptions show literal environment values, and logs hold whatever applications wrote, credentials included.
Review the archive before sharing it and use your organization's secure support channel.

## Configure the debug terminal { #hopsworks-configure-debug-terminal }

The terminal is off by default.
Enable it in the Hopsworks Helm values and keep the service account name empty to run the shell without a Kubernetes service account token.

```yaml
hopsworks:
  adminDebug:
    enabled: true
    serviceAccountName: ""
    mysqlTables: false
```

To provide Kubernetes access from the shell, deploy a dedicated service account in the Hopsworks release namespace and set `hopsworks.adminDebug.serviceAccountName` to its name.
Grant that account only the permissions you intend to give everyone who uses the debug terminal.
End existing debug sessions before changing this setting, then roll out both the Hopsworks admin and instance deployments before opening new sessions.

The terminal's database account can read RonDB's `ndbinfo` diagnostics.
Set `hopsworks.adminDebug.mysqlTables: true` to also allow reads from selected Hopsworks metadata and HopsFS size tables.
Turning that setting off withdraws the extra table grants on upgrade.
The [RonDB overview][cluster-overview-rondb] is available for checking node capacity and table allocation with the default terminal settings.

## Start and stop a debug session { #hopsworks-use-debug-terminal }

1. In **Overview**, choose **Debug terminal** from the sidebar.
2. Choose a session length and select **Start debug terminal**.
3. Use `hw-help` in the shell to list the available diagnostic commands.
4. Stop the session from the page when you finish.

Each administrator has a separate session pod with a maximum lifetime set by `hopsworks.adminDebug.sessionHours`, two hours by default.
The shell can reconnect while the session is still running.
Terminal output is audited, so keep secrets out of commands and output.

For deployment prerequisites, see [Debug terminal credentials on upgrade][upgrade-debug-terminal-credentials].
