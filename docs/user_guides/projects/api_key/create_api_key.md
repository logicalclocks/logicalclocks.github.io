# How To Create An API Key

## Introduction

An API key allows a user or a program to make API calls without having to authenticate with a username and password.
To access an endpoint using an API key, a client should send the access token using the ApiKey authentication scheme.

The API Key can now be used when connecting to your Hopsworks instance using the `hopsworks`, `hsfs` or `hsml` python library or set in the `ApiKey` header for the REST API.

```bash
GET /resource HTTP/1.1
Host: server.hopsworks.ai
Authorization: ApiKey <api_key>
```

## UI

In this guide, you will learn how to create an API key.

### Step 1: Navigate to API Keys

In the _Account Settings_ page you can find the _API_ section showing a list of all API keys. 
The table shows each key's name, scope, prefix, creation date, last modification date, and expiration date. 
Keys with no expiration show _Never_ in the expiration column.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/api_key/api_keys.png" alt="API Keys">
    <figcaption>List of API Keys</figcaption>
  </figure>
</p>

### Step 2: Create an API Key

Click `New API key`, enter a name, optionally set an expiration, select the required scopes, and click `Create API key`.

**Expiration options:**

| Option | Description |
| -------- | ------------- |
| No expiration | The key never expires (default). |
| 7 / 30 / 60 / 90 days | The key expires the selected number of days from now. |
| Custom | Pick a specific date using the date picker. |

To change the expiration date of an existing key you must regenerate it — expiration cannot be updated after creation.

Copy the key value and save it in a secure location, such as a password manager. 
It will not be shown again.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/api_key/create_api_key.gif" alt="Create API Key">
    <figcaption>Create new API Key</figcaption>
  </figure>
</p>

## Login with API Key using SDK

In this guide you learned how to create an API Key.
You can now use the API Key to [login][hopsworks.login] using the `hopsworks` python SDK.
