---
description: Documentation on how to configure external access to a model deployment
---

# How To Configure External Access To A Model Deployment

## Introduction

Hopsworks supports role-based access control (RBAC) for project members within a project, where a project ML assets can only be accessed by Hopsworks users that are members of that project (See [governance](../../../concepts/projects/governance.md)).

However, there are cases where you might want to grant ==external users== with access to specific model deployments without them having to register into Hopsworks or to join the project which will give them access to all project ML assets.
For these cases, Hopsworks supports fine-grained access control to model deployments based on ==user groups== managed by an external Identity Provider.

!!! info "Authentication methods"
    Hopsworks can be configured to use different types of authentication methods including OAuth2, LDAP and Kerberos.
    See the [Authentication Methods Guide](../../../setup_installation/admin/auth.md) for more information.

## GUI (for Hopsworks users)

### Step 1: Navigate to a model deployment

If you have at least one model deployment already created, navigate to the model deployments page by clicking on the `Deployments` tab on the navigation menu on the left.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployments_tab_sidebar_with_list.svg" alt="Deployments navigation tab">
    <figcaption>Deployments navigation tab</figcaption>
  </figure>
</p>

Once in the model deployments page, find the model deployment you want to configure external access and click on the name of the deployment to open the model deployment overview page.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployment_overview.png" alt="Deployment overview">
    <figcaption>Deployment overview</figcaption>
  </figure>
</p>

### Step 2: Go to External Access

You can find the external access configuration by clicking on `External access` on the navigation menu on the left or scrolling down to the external access section.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployment_external_access.png" alt="Deployment external access">
    <figcaption>External access configuration</figcaption>
  </figure>
</p>

### Step 3: Add or remove user groups

In this section, you can add and remove user groups by clicking on `edit external user groups` and typing the group name in the **text-free** input field or **selecting** one of the existing ones in the dropdown list.
After that, click on the `save` button to persist the changes.

!!! Warn "Case sensitivity"
    Inference requests are authorized using a ==case-sensitive exact match== between the group names of the user making the request and the group names granted access to the model deployment.
    Therefore, a user assigned to the group `lab1` won't have access to a model deployment accessible by group `LAB1`.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployment_external_access_edit.png" alt="Deployment external access">
    <figcaption>External access configuration</figcaption>
  </figure>
</p>

## GUI (for external users)

### Step 1: Login with the external identity provider

Navigate to Hopsworks, and click on the `Login with` button to sign in using the configured external identity provider (e.g., Keycloak in this example).

<p align="center">
  <figure>
    <img style="max-width: 50%" src="../../../../assets/images/guides/mlops/serving/login_external_idp.png" alt="Login external identity provider">
    <figcaption>Login with External Identity Provider</figcaption>
  </figure>
</p>

### Step 2: Explore the model deployments you are granted access to

Once you sign in to Hopsworks, you can see the list of model deployments you are granted access to based on your assigned groups.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployment_external_list.png" alt="Deployments list">
    <figcaption>Deployments with external access</figcaption>
  </figure>
</p>

### Step 2: Inspect your current groups

You can find the current groups you are assigned to at the top of the page.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployment_external_groups.png" alt="External user groups">
    <figcaption>External user groups</figcaption>
  </figure>
</p>

### Step 3: Get an API key

Inference requests to model deployments are authenticated and authorized based on your external user and user groups.
You can create API keys to authenticate your inference requests by clicking on the `Create API Key` button.

!!! info "Authorization header"
    API keys are set in the `Authorization` header following the format `ApiKey <api-key-value>`

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployment_external_api_key.png" alt="Get API key">
    <figcaption>Get API key</figcaption>
  </figure>
</p>

### Step 4: Send inference requests

Depending on the type of model deployment, the URI of the model server can differ (e.g., `/chat/completions` for LLM deployments or `/predict` for traditional model deployments).
You can find the corresponding URI on every model deployment card.

In addition to the `Authorization` header containing the API key, the `Host` header needs to be set according to the model deployment where the inference requests are sent to.
This header is used by the ingress to route the inference requests to the corresponding model deployment.
You can find the `Host` header value in the model deployment card.

!!! tip "Code snippets"
    For clients sending inference requests using libraries similar to curl or OpenAI API-compatible libraries (e.g., LangChain), you can find code snippet examples by clicking on the `Curl >_` and `LangChain >_` buttons.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployment_external_code_snippets.png" alt="Deployment endpoint">
    <figcaption>Deployment endpoint</figcaption>
  </figure>
</p>

## Refreshing External User Groups

Every time an external user signs in to Hopsworks using a pre-configured [authentication method](../../../setup_installation/admin/auth.md), Hopsworks fetches the external user groups and updates the internal state accordingly.
Given that groups can be added/removed from users at any time by the Identity Provider, Hopsworks needs to periodically fetch the external user groups to keep the state updated.

Therefore, external users that want to access model deployments are **required to login periodically** to ensure they are still part of the allowed groups.
The timespan between logins is controlled by the configuration parameter `requireExternalUserLoginAfterHours` available during the Hopsworks installation and upgrade.

The `requireExternalUserLoginAfterHours` configuration parameter controls the ==number of hours== after which external users are required to sign in to Hopsworks to refresh their external user groups.

!!! info "Configuring `requireExternalUserLoginAfterHours`"
    Allowed values are -1, 0 and greater than 0, where -1 disables the periodic login requirement and 0 disables external access completely for every model deployment.
