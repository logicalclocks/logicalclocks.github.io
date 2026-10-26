# How-To set up an Outlook Data Source { #data-source-outlook }

## Introduction

An Outlook data source is one Microsoft 365 (Exchange Online) or Outlook.com mailbox, read through [Microsoft Graph](https://learn.microsoft.com/graph/api/resources/mail-api-overview) with the `Mail.Read` permission.
It holds the mailbox address and the credentials of an app registration in Microsoft Entra ID: a refresh token granted by the mailbox's owner, or a client secret of an app that a tenant administrator allowed to read the tenant's mail.

An Outlook data source works like a [Gmail data source][data-source-gmail].
A sync job copies the mailbox into a Delta feature group, on demand, hourly or daily, and writes the attachments as files in the project.
The feature group has the same columns as a Gmail data source's, so you read and search both the same way.
This page describes what differs from Gmail; the [Gmail page][data-source-gmail] describes the feature group, the attachments, the loading strategies and the DuckDB search in full.

## Prerequisites

You need the email address of the mailbox and an app registration, created in the [Microsoft Entra admin center](https://entra.microsoft.com/) under `Identity` > `Applications` > `App registrations` > `New registration`.
Note its **Application (client) ID** and its **Directory (tenant) ID**.

### Delegated access with a refresh token

Use this for your own mailbox, on Outlook.com or in a Microsoft 365 organization.

1. Register the app.
    For an Outlook.com mailbox, pick the supported account types `Accounts in any organizational directory and personal Microsoft accounts`.
    Add a redirect URI of platform `Web`, `http://localhost`.
2. Under `API permissions`, add the Microsoft Graph delegated permissions `Mail.Read` and `offline_access`.
3. Under `Certificates & secrets`, add a client secret and copy its **value**.
4. Open this address in a browser, with your client ID, and sign in as the owner of the mailbox:

    ```text
    https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=<client id>&response_type=code&redirect_uri=http://localhost&response_mode=query&scope=offline_access%20https://graph.microsoft.com/Mail.Read
    ```

    The browser is sent to `http://localhost/?code=...`, which shows nothing; copy the `code` parameter from the address bar.
5. Exchange the code for tokens within a few minutes:

    ```bash
    curl -s https://login.microsoftonline.com/common/oauth2/v2.0/token \
        -d client_id=<client id> -d client_secret=<client secret> \
        -d grant_type=authorization_code -d redirect_uri=http://localhost \
        -d scope="offline_access https://graph.microsoft.com/Mail.Read" \
        --data-urlencode code=<code>
    ```

    Copy the **refresh token** from the response.

The tenant is `common` here.
For a work mailbox, you can use your tenant ID instead, in both addresses and in the data source.
An app registered as a public client, with `Allow public client flows` turned on, needs no client secret; leave it out of the token request and the data source.

Microsoft replaces the refresh token each time Hopsworks uses it, and Hopsworks stores the new one.
A refresh token that is not used for 90 days expires, so a data source whose sync job runs at least that often keeps working.
Revoking the app's consent, or changing the account's password, revokes the token.

### App-only access with client credentials

Use this for mailboxes of a Microsoft 365 organization that you administer, such as a shared support mailbox.

1. Register the app with the supported account types `Accounts in this organizational directory only`.
2. Under `API permissions`, add the Microsoft Graph application permission `Mail.Read`, and click `Grant admin consent`.
3. Under `Certificates & secrets`, add a client secret and copy its **value**.

!!! warning
    The application permission `Mail.Read` lets the app read every mailbox in the organization.
    The data source reads only the mailbox it names, but anyone holding the client secret can read the others.
    Limit the app to the mailboxes it needs with [Exchange Online RBAC for Applications](https://learn.microsoft.com/exchange/permissions-exo/application-rbac), and keep the secret out of shared datasets.

## Creation in the UI

Head to the `Data Sources` view, click `New data source`, and pick the `Outlook` card under `API & SaaS`.

1. Give the data source a **name** and an optional **description**.
2. Enter the **Mailbox**, the email address to read.
3. Under **Authentication**, pick `Delegated (OAuth refresh token)` or `App-only (client credentials)`.
4. Enter the **Tenant ID**: empty for `common` with delegated access, and your tenant's ID or domain, such as `contoso.onmicrosoft.com`, for app-only access.
5. Enter the **Client ID**, the **Client secret** and, for delegated access, the **Refresh token**.
6. Click `Test connection`.
    Hopsworks requests an access token and reads the Inbox, and answers with the mailbox and the Inbox's number of messages, such as `Connected to alice@contoso.com (1234 messages in Inbox)`.
    When Microsoft refuses the credentials, the error carries Microsoft's reason, such as `invalid_grant` for an expired or revoked refresh token.
7. Save the data source.

## Creation with the Python SDK

```python
import hopsworks
from hsfs.storage_connector import OutlookConnector


project = hopsworks.login()
fs = project.get_feature_store()

outlook = OutlookConnector(
    id=None,
    name="support_outlook",
    featurestore_id=fs.id,
    mailbox="support@contoso.com",
    auth_type="CLIENT_CREDENTIALS",
    tenant_id="contoso.onmicrosoft.com",
    client_id="00000000-0000-0000-0000-000000000000",
    client_secret="...",
)
outlook.save()
```

For delegated access, pass `auth_type="OAUTH"` and `refresh_token`; `tenant_id` then defaults to `common`.

## Creation with the CLI

```bash
hops datasource create outlook support_outlook \
    --mailbox support@contoso.com --auth-type CLIENT_CREDENTIALS \
    --tenant-id contoso.onmicrosoft.com \
    --client-id 00000000-0000-0000-0000-000000000000 \
    --client-secret - < secret.txt
```

A secret option given as `-` reads one line from standard input, and each option also reads the environment variable `HOPSWORKS_DS_OUTLOOK_<OPTION>`, such as `HOPSWORKS_DS_OUTLOOK_REFRESH_TOKEN`.
For delegated access, use `--auth-type OAUTH --refresh-token -`.

## Credentials

The credentials are write-only.
Hopsworks never returns the client secret or the refresh token: reading the data source back returns `credentials_set`, the `tenant_id` and the `client_id`.
When you edit the data source, leave a secret field empty to keep the stored value.

To call Microsoft Graph from your own code, ask the data source for a short-lived access token.
`token.user_path` is the mailbox's path in Graph: `me` for delegated access, and `users/<mailbox>` for app-only access.

```python
import hopsworks
import requests


project = hopsworks.login()
fs = project.get_feature_store()

outlook = fs.get_data_source("support_outlook").storage_connector
token = outlook.get_access_token()
inbox = requests.get(
    f"https://graph.microsoft.com/v1.0/{token.user_path}/mailFolders/inbox",
    headers={"Authorization": f"Bearer {token.token}"},
    timeout=60,
).json()
```

## Sync jobs

Sync jobs of an Outlook data source behave as those of a [Gmail data source][data-source-gmail]: the feature group's name, schema and `day` partitions, the attachments directory, the loading strategies, the backfill that upserts as it goes, the hourly runs that wait for it, and the retries while throttled.
Two sync jobs cannot write the same feature group or overlapping attachment directories, whether they copy Gmail or Outlook.
The differences:

- **Feature group name:** `jim@outlook.com` becomes `jim_outlooks`, and `support@contoso.com` becomes `support_contosos`.
- **Default attachments directory:** `Resources/outlook/<feature group>`.
- **Messages selected:** by folder; there is no search query.
    A message in any chosen folder is copied, and a chosen folder's subfolders are copied only when chosen too.
    Without chosen folders, every folder but Deleted Items, Junk Email, Drafts and Outbox is copied.
    Drafts are never copied.
- **Incremental runs:** each run copies the messages whose `receivedDateTime` is after the previous run's.
- **Throttling:** Microsoft Graph allows 4 concurrent requests per mailbox and 10,000 requests per 10 minutes per app and mailbox.
    A throttled run honours Graph's `Retry-After` and retries until Graph serves it, and never fails because of throttling.
- **Moves:** a message moved to another folder keeps its `message_id`, so it is never copied twice, but its `labels` keep the folder it was in when it was copied until a full load.

| Column | Outlook content |
| --- | --- |
| `message_id` | The message's immutable Graph id, the primary key |
| `thread_id` | Its conversation id |
| `history_id` | Its change key |
| `internal_date` | `receivedDateTime`, when it reached the mailbox, in UTC to the second; the event time and the `day` partition |
| `labels` | The path of its folder, such as `Inbox` or `Inbox/Projects`, then its categories |
| `snippet` | Graph's body preview |
| `size_estimate` | The size of its MIME source in bytes |

The other columns are parsed from the message's MIME source, exactly as for Gmail.

### Configure a sync job in the UI

Open the data source from the `Data Sources` view and click `Configure sync job` in its `Sync jobs` card.
The dialog is the Gmail one, with the job name defaulting to `<data source name>_outlook_sync`, no search query, and **Folders** in place of mailboxes, picked from the mailbox's folders.

### Configure a sync job with the Python SDK

```python
import hopsworks


project = hopsworks.login()
fs = project.get_feature_store()

outlook = fs.get_data_source("support_outlook").storage_connector
folders = outlook.get_folders()  # folder paths by id
inbox = [folder_id for folder_id, path in folders.items() if path == "Inbox"]
job = outlook.sync(
    folders=inbox,
    initial_value="2026-01-01",
    schedule="hourly",
)
```

`sync` takes the arguments of `GmailConnector.sync`, with `folders` in place of `query` and `labels`.
`list_sync_jobs`, `get_sync_job` and `delete_sync_job` work as for Gmail; a job's `labels` hold its folder ids.

### Configure a sync job with the CLI

```bash
hops datasource labels support_outlook
hops datasource sync support_outlook --label <folder id> --start-date 2026-01-01 --schedule hourly
hops datasource sync-jobs support_outlook
```

`hops datasource labels` lists the ids and paths of the mailbox's folders, and `--label` takes a folder id.
`--query` is refused for an Outlook data source.

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-class"></code> [`OutlookConnector`][hsfs.storage_connector.OutlookConnector]
        - <code class="doc-symbol doc-symbol-method"></code> [`get_access_token`][hsfs.storage_connector.OutlookConnector.get_access_token]
        - <code class="doc-symbol doc-symbol-method"></code> [`get_folders`][hsfs.storage_connector.OutlookConnector.get_folders]
        - <code class="doc-symbol doc-symbol-method"></code> [`sync`][hsfs.storage_connector.OutlookConnector.sync]
    - <code class="doc-symbol doc-symbol-class"></code> [`MailSyncJobConfig`][hsfs.storage_connector.MailSyncJobConfig]

    <a class="hops-api-cta" href="../../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>

## Read the emails

Read the feature group like any other, or search it with DuckDB in a terminal as described for [Gmail][data-source-gmail].
The `hops-email-search` skill of the coding agents in a terminal works on both.

## Delete the data source

Deleting an Outlook data source deletes its sync jobs and their schedules.
The feature groups and the attachment files stay.
