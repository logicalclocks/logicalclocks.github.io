---
description: Documentation on how to configure external access to a model deployment
---

# How To Configure External Access To A Model Deployment { #serving-external-access }

## Introduction

Hopsworks supports **role-based access control (RBAC)** for project members within a project, where a project ML assets can only be accessed by Hopsworks users that are members of that project (See [governance](../../../concepts/projects/governance.md)).

However, there are cases where you might want to grant ==external users== with access to specific model deployments without them having to register into Hopsworks or to join the project which will give them access to all project ML assets.
For these cases, Hopsworks supports fine-grained access control to model deployments based on ==user groups== managed by an external Identity Provider.

!!! info "Authentication methods"
    Hopsworks can be configured to use different types of authentication methods including OAuth2, LDAP and Kerberos.
    See the [Authentication Methods Guide](../../../setup_installation/admin/auth.md) for more information.

## Web UI (for Hopsworks users)

### Step 1: Navigate to a model deployment

If you have at least one model deployment already created, navigate to the model deployments page by clicking on the `Deployments` tab on the navigation menu on the left.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployments_tab_sidebar_with_list.png" alt="Deployments navigation tab">
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

## Web UI (for external users)

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
    API keys are set in the `authorization` header following the format `ApiKey <api-key-value>`

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployment_external_api_key.png" alt="Get API key">
    <figcaption>Get API key</figcaption>
  </figure>
</p>

### Step 4: Send inference requests

The URI path for sending inference requests depends on the type of model deployment.
For example, LLM deployments typically use `/chat/completions`, while traditional model deployments use `/predict`.
You can find the exact URI path for each deployment on its model deployment card.

For detailed instructions on constructing requests and handling authentication, refer to the [REST API Guide](rest-api.md).

!!! tip "Code snippets"
    For clients sending inference requests using libraries similar to curl or OpenAI API-compatible libraries (e.g., LangChain), you can find code snippet examples by clicking on the `Curl >_` and `LangChain >_` buttons.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/mlops/serving/deployment_external_code_snippets.png" alt="Deployment endpoint">
    <figcaption>Deployment endpoint</figcaption>
  </figure>
</p>

## LLM deployments and the LLM Gateway

On a cluster where the [LLM Gateway][llm-gateway] is enabled, the groups granted on an LLM deployment also let external users call it through the project's LLM Gateway, `<inference endpoint>/v1/<project>/v1/`, with the deployment name as the request's `model`.
An external user can use only the deployments granted to them there, with these operations only:

- Chat completions, `/v1/chat/completions`
- Completions, `/v1/completions`
- Embeddings, `/v1/embeddings`
- Responses, `/v1/responses`
- Anthropic messages, `/anthropic/v1/messages`

Listing the project's models, and every other path, is refused with `403`.
The LLM Gateway serves only the deployments described under [LLM Gateway][rest-api-llm-gateway]; the others stay on their own path.
A Data Owner can turn the LLM Gateway off for the project or for one deployment, which leaves the deployment's own path as it is.
A Data Owner can also turn direct access off, see [Turning direct access off][rest-api-direct-access].

### Sharing with projects { #serving-sharing }

A vLLM deployment that the LLM Gateway serves can also be shared with other projects of the cluster.
Members of those projects call it through the owning project's LLM Gateway with their own API keys, as described under [Coding agents][coding-agents-access].
They run inference with the five operations listed above, for the deployment's own `model` only.
They cannot list models, see or manage the deployment, or call its direct route, and each request is attributed to them in the owning project's usage.

Three mechanisms grant access to a deployment, each to a different kind of caller:

| Mechanism | Who it grants | Routes |
| --- | --- | --- |
| Project membership | Members of the owning project | LLM Gateway and direct |
| External access groups | External users in the listed groups | LLM Gateway and direct |
| Sharing with projects | Members of the projects it is shared with | LLM Gateway only |

Data Owners of the owning project decide, per deployment.
In the deployment's Overview, the **Sharing** card has:

- the **All projects** switch, which shares the deployment with every project of the cluster;
- with the switch off, a list of project names, which shares it with the members of those projects only.

Project members see the card, and only Data Owners change it.
It is hidden when the deployment is not served by the LLM Gateway or when an administrator turned sharing off for the cluster, see [Access to the LLM Gateway][llm-gateway-access].

With the Python client, `Deployment` reads and changes the same state:

```python
deployment = ms.get_deployment("my_llm_deployment")

print(deployment.shared_with)  # {'all_projects': True, 'projects': []}

# Restrict it to two projects
deployment.unshare(all_projects=True)
deployment.share_with(projects=["analytics", "research"])
print(deployment.shared_with)  # {'all_projects': False, 'projects': [...]}
```

A new LLM deployment is shared with all projects by default.
A deployment created before the upgrade that introduced sharing stays project-only until a Data Owner shares it.
A choice a Data Owner made, including switching **All projects** off, is kept when the deployment leaves and joins the LLM Gateway again.

To keep a deployment reachable only through the LLM Gateway, turn off its [direct access][rest-api-direct-access].

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-class"></code> [`Deployment`][hsml.deployment.Deployment]
        - <code class="doc-symbol doc-symbol-method"></code> [`shared_with`][hsml.deployment.Deployment.shared_with]
        - <code class="doc-symbol doc-symbol-method"></code> [`share_with`][hsml.deployment.Deployment.share_with]
        - <code class="doc-symbol doc-symbol-method"></code> [`unshare`][hsml.deployment.Deployment.unshare]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>

### Limits and traces of the LLM Gateway

An administrator can set token and request limits on the LLM Gateway, per project, per user and per deployment, as described under [Rate limits and token quotas][llm-gateway-rate-limits].
The limits that apply to a project are shown, read-only, in the project settings, and a request over a limit gets `429`.

When an administrator has turned [tracing][llm-gateway-tracing] on, members with the role Data Owner or Data Scientist see the project's request traces under LLM Gateway in the project settings, with a filter on the deployment, and one deployment's traces in its Overview.
Prompts and responses are not stored in them unless an administrator turned that on too.

## Refreshing External User Groups

Every time an external user signs in to Hopsworks using a pre-configured [authentication method](../../../setup_installation/admin/auth.md), Hopsworks fetches the external user groups and updates the internal state accordingly.
Given that groups can be added/removed from users at any time by the Identity Provider, Hopsworks needs to periodically fetch the external user groups to keep the state updated.

Therefore, external users that want to access model deployments are **required to login periodically** to ensure they are still part of the allowed groups.
The timespan between logins is controlled by the configuration parameter `requireExternalUserLoginAfterHours` available during the Hopsworks installation and upgrade.

The `requireExternalUserLoginAfterHours` configuration parameter controls the ==number of hours== after which external users are required to sign in to Hopsworks to refresh their external user groups.

!!! info "Configuring `requireExternalUserLoginAfterHours`"
    Allowed values are -1, 0 and greater than 0, where -1 disables the periodic login requirement and 0 disables external access completely for every model deployment.
