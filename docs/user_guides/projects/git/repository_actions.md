# Repository actions

## Introduction

This section explains the git operations or commands you can perform on hopsworks git repositories. These commands include commit, pull, push, create branches and many more.

!!! notice "Repository permissions"
    Git repositories are private. Only the owner of the repository can perform git actions on the repository such as commit, push, pull e.t.c.

## UI

The operations to perform on the cloned repository can be found in the dropdown as shown below.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/git/repo_actions.gif" alt="Repository actions on a repository">
    <figcaption>Repository actions</figcaption>
  </figure>
</p>

Note that some repository actions will require the username and token to be configured first depending on the provider. For example to be able to perform a push action in any repository, you must configure the provider for the repository first. To be able to perform a pull action for the for a GitLab repository, you must configure the GitLab provider first. You will see the dialog below in the case you need to configure the provider first to perform the repository action.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/git/provider_not_configured_for_repo_action.png" alt="Provider not configured">
    <figcaption>Configure provider prompt</figcaption>
  </figure>
</p>

## Read only repositories

In read only repositories, the following actions are disabled: commit, push and file checkout. The read only property can be enabled or disabled in the Cluster settings > Configuration, by updating the `enable_read_only_git_repositories` variable to true or false. Note that you need administrator privileges to update this property.

## Code

You can also perform the repository actions using the hopsworks git API in python.

### Step 1: Get the git API

```python

import hopsworks

project = hopsworks.login()

git_api = project.get_git_api()

```

### Step 2: Get the git repository

```python
git_repo = git_api.get_repo(REPOSITORY_NAME)

```

### Step 3: Perform the git repository action e.g commit

```python
git_repo = git_api.commit("Test commit")

```

### API Reference

Api reference for repository actions is available here:
[GitRepo](<https://docs.hopsworks.ai/hopsworks-api/{{{> hopsworks_version }}}/generated/api/git_repo/)
