# Create An Application in Azure Active Directory.

## Introduction
This example uses Azure Active Directory as the identity provider, but the same can be done with any identity provider 
supporting OAuth2 OpenID Connect protocol.

## Prerequisites
Azure account.

### Step 1: Register Hopsworks as an application in your identity provider

To use OAuth2 in Hopsworks you first need to create and configure an OAuth client in your identity provider. We will take the example of Azure AD for the remaining of this documentation, but equivalent steps can be taken on other identity providers.

Navigate to the [Microsoft Azure Portal](https://portal.azure.com) and authenticate. Navigate to [Azure Active Directory](https://portal.azure.com/#blade/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/Overview). Click on [App Registrations](https://portal.azure.com/#blade/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/RegisteredApps). Click on *New Registration*.

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../../assets/images/admin/oauth2/sso/create_application.png" alt="Create application">
    <figcaption>Create application</figcaption>
  </figure>
</p>

Enter a name for the client such as *hopsworks_oauth_client*. Verify the Supported account type is set to *Accounts in this organizational directory only*. And Click Register.

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../../assets/images/admin/oauth2/sso/name_application.png" alt="Name application">
    <figcaption>Name application</figcaption>
  </figure>
</p>

### Step 2: Get the necessary fields for client registration
In the Overview section, copy the *Application (client) ID field*. We will use it in 
[Identity Provider registration](../create-client) under the name *Client id*.

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../../assets/images/admin/oauth2/sso/client_id.png" alt="Copy client ID">
    <figcaption>Copy client ID</figcaption>
  </figure>
</p>

Click on *Endpoints* and copy the *OpenId Connect metadata document* endpoint excluding the *.well-known/openid-configuration* part. 
We will use it in [Identity Provider registration](../create-client) under the name *Connection URL*.

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../../assets/images/admin/oauth2/sso/endpoint.png" alt="Endpoint">
    <figcaption>Endpoint</figcaption>
  </figure>
</p>

!!! note
    If you have multiple tenants in your Azure Active Directory, the `OpenID Connect metadata document` endpoint might use `organizations`  instead of a specific tenant ID. In such cases, replace `organizations`  with your actual tenant ID to target a specific directory.

    example:

      ```
      https://login.microsoftonline.com/organizations/oauth2/v2.0 --> https://login.microsoftonline.com/<YOUR_TENANT_ID>/oauth2/v2.0
      ```

Click on *Certificates & secrets*, then Click on *New client secret*.

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../../assets/images/admin/oauth2/sso/new_client_secret.png" alt="New client secret">
    <figcaption>New client secret</figcaption>
  </figure>
</p>

Add a *description* of the secret. Select an expiration period. And, Click *Add*.

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../../assets/images/admin/oauth2/sso/new_client_secret_config.png" alt="Client secret creation">
    <figcaption>Client secret creation</figcaption>
  </figure>
</p>

Copy the secret. This will be used in [Identity Provider registration](../create-client) under the name 
*Client Secret*.

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../../assets/images/admin/oauth2/sso/copy_secret.png" alt="Client secret creation">
    <figcaption>Client secret creation</figcaption>
  </figure>
</p>

Click on *Authentication*. Then click on *Add a platform*

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../../assets/images/admin/oauth2/sso/add_platform.png" alt="Add a platform">
    <figcaption>Add a platform</figcaption>
  </figure>
</p>

In *Configure platforms* click on *Web*.

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../../assets/images/admin/oauth2/sso/add_platform_web.png" alt="Configure platform: Web">
    <figcaption>Configure platform: Web</figcaption>
  </figure>
</p>

Enter the *Redirect URI* and click on *Configure*. The redirect URI is *HOPSWORKS-URI/callback* with *HOPSWORKS-URI* the URI of your Hopsworks cluster.

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../../assets/images/admin/oauth2/sso/add_platform_redirect.png" alt="Configure platform: Redirect">
    <figcaption>Configure platform: Redirect</figcaption>
  </figure>
</p>
