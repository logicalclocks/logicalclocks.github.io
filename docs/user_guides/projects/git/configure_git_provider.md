# How To Configure a Git Provider

## Introduction

When you perform Git operations on Hopsworks that need to interact with the remote repository, Hopsworks relies on the Git HTTPS protocol to perform those operations. Authentication with the remote repository happens through a token generated by the Git repository hosting service (GitHub, GitLab, BitBucket).

!!! warning "Beta"
    The feature is currently in Beta and will be improved in the upcoming releases.

!!! notice "Tokens are personal"
    The tokens are personal to each user. When you perform operations on a repository, your token is going to be used, even though the repository might belong to a different user.

## UI

Documentation on how to generate a token for the supported Git hosting services is available here:

- [GitHub](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [GitLab](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html)
- [BitBucket](https://confluence.atlassian.com/bitbucketserver/http-access-tokens-939515499.html)

### Step 1: Navigate to Git Providers

In the `Account Settings` page you can find the `Git Providers` section. The Git provider section displays which providers have been already configured and can be used to clone new repositories.

<p align="center">
  <figure>
    <a  href="../../../../assets/images/guides/git/git_provider_not_configured.png">
      <img src="../../../../assets/images/guides/git/git_provider_not_configured.png" alt="Git provider configuration list">
    </a>
    <figcaption>Git provider configuration list</figcaption>
  </figure>
</p>

### Step 2: Configure a provider

Click on `Edit Configuration` to change a provider username or token, or to configure a new provider.

Tick the checkbox next to the provider you want to configure and insert the username and the token to use for that provider.

<p align="center">
  <figure>
    <a  href="../../../../assets/images/guides/git/configure_git_provider.png">
      <img src="../../../../assets/images/guides/git/configure_git_provider.png" alt="Git provider configuration">
    </a>
    <figcaption>Git provider configuration</figcaption>
  </figure>
</p>

Click `Create Configuration` to save the configuration.

### Step 3: Provider is configured

The configured provider should now be marked as configured.

<p align="center">
  <figure>
    <a  href="../../../../assets/images/guides/git/git_provider_configured.png">
      <img src="../../../../assets/images/guides/git/git_provider_configured.png" alt="Git provider configured">
    </a>
    <figcaption>Git provider configured</figcaption>
  </figure>
</p>

## Code

### Step 1: Get the git API

This snippet assumes the python script is in the current working directory and named `script.py`. It will upload the python script to run to the `Resources` dataset.

```python

import hopsworks

connection = hopsworks.connection()

project = connection.get_project()

git_api = project.get_git_api()

```

### Step 2: Configure git provider

```python

PROVIDER="GitHub"
GITHUB_USER="my_user"
API_TOKEN="my_token"

git_api.set_provider(PROVIDER, GITHUB_USER, API_TOKEN)

```

### API Reference

[GitProvider](https://docs.hopsworks.ai/hopsworks-api/dev/generated/api/git_provider/)

## Conclusion

In this guide you learned how configure your git provider credentials. You can now use the credentials to [clone a repository](clone_repo.md) from the configured provider.