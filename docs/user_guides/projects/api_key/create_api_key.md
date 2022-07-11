# How To Create An API Key

## Introduction

An API key allows a user or a program to make API calls without having to authenticate with a username and password. To access an endpoint using an API key, a client should send the access token using the ApiKey authentication scheme.

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

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/api_key/api_keys.png" alt="API Keys">
    <figcaption>List of API Keys</figcaption>
  </figure>
</p>

### Step 2: Create an API Key

Click `New Api key`, select the required scopes and create it by clicking `Create Api Key`.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/api_key/create_api_key.gif" alt="Create API Key">
    <figcaption>Create new API Key</figcaption>
  </figure>
</p>

## Conclusion

In this guide you learned how to create an API Key.