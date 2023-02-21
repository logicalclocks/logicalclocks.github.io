# How to manage your managed.hopsworks.ai account

### Introduction
[Managed.hopsworks.ai](https://managed.hopsworks.ai) is our managed platform for running Hopsworks and the Feature Store in the cloud. On this page, you will get an overview of the [managed.hopsworks.ai](https://managed.hopsworks.ai) page.

## How to get to the settings page and what does it look like.
From the [managed.hopsworks.ai](https://managed.hopsworks.ai) [landing page](./dashboard.md), you can access the setting page by clicking on __Settings__ on the top left.

The settings page contains a menu on the left. The remaining of the page display information depending on the section you have selected in the menu.

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/settings/settings.png" alt="Getting to the settings page">
    <figcaption>Getting to the settings page</figcaption>
  </figure>
</p>

## Manage the connection to your cloud accounts under Cloud Accounts
The landing section of the settings page is the __Cloud Accounts__ section. On this page you can edit the link between [managed.hopsworks.ai](https://managed.hopsworks.ai) and your cloud provider by clicking on the __Edit__ button (1). You can delete the link and remove any access from [managed.hopsworks.ai](https://managed.hopsworks.ai) to your cloud manager by clicking on the __Delete__ button (2). Or, you can configure a new connection with a cloud provider by clicking on the __Configure__ button (3).

For more details about setting up a connection with a cloud provider see the getting started pages for:

- [AWS](../aws/getting_started.md)
- [Azure](../azure/getting_started.md)
- [GCP](../gcp/getting_started.md)

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/settings/cloud_accounts.png" alt="Cloud accounts management">
    <figcaption>Cloud accounts management</figcaption>
  </figure>
</p>

## Manage your personal information under Profile
The __Profile__ section is where you can edit your personal information such as name, phone number, company, etc.

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/settings/profile.png" alt="Profile management">
    <figcaption>Profile</figcaption>
  </figure>
</p>

## Change your password and configure multi-factor authentication under the Security section
### Change your password
To change your password, go to the security section, enter your current password in the __Current password__ field (1), enter the new password in the __New password__ field (2), and click on __Save__ (3).

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/settings/change_password.png" alt="Change password">
    <figcaption>Change password</figcaption>
  </figure>
</p>

### Set up multi-factor authentication.
To set up multi-factor authentication, go to the security section, scan the QR code (1) with your authenticator app (example: [Google Authenticator](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2&hl=en&gl=US)). Then enter the security code provided by the authenticator app in the __Security code__ field (2) and click on __Enable TOTP__ (3).

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/settings/mfa.png" alt="Enable MFA">
    <figcaption>Enable MFA</figcaption>
  </figure>
</p>

## Create and manage API keys under the API keys section
The API key section is where you create or delete your [managed.hopsworks.ai](https://managed.hopsworks.ai) API keys. More details about the API keys can be found in the [API keys documentation](./api_key.md)

<p align="center">
  <figure>
    <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/api_key/api-key-2.png" alt="Generate API Key">
    <figcaption>Generate an API Key</figcaption>
  </figure>
</p>

## Conclusion
You now know where and how to update your profile, cloud accounts, and API keys.

To keep familiarizing with [managed.hopsworks.ai](https://managed.hopsworks.ai) check the [dashboard documentation](./dashboard.md)