# Repository actions
## UI
The operations to perform on the cloned repository can be found in the dropdown as shown below.

<p align="center">
  <figure>
    <a  href="../../../../assets/images/guides/git/repo_actions.gif">
      <img src="../../../../assets/images/guides/git/repo_actions.gif" alt="Repository actions on a repository">
    </a>
    <figcaption>Repository actions</figcaption>
  </figure>
</p>

Note that some repository actions will require the username and token to be configured first depending on the provider. For example to be able to perform a push action in any repository, you must configure the provider for the repository first. To be able to perform a pull action for the for a GitLab repository, you must configure the GitLab first. You will see the dialog below in the case you need to configure the provider first to perform the repository action.

<p align="center">
  <figure>
    <a  href="../../../../assets/images/guides/git/provider_not_configured_for_repo_action.png">
      <img src="../../../../assets/images/guides/git/provider_not_configured_for_repo_action.png" alt="Provider not configured">
    </a>
    <figcaption>Configure provider prompt</figcaption>
  </figure>
</p>

## Code
You can also perform the repository actions through the hopsworks git API in python. 
### Step 1: Get the git API

```python

import hopsworks

connection = hopsworks.connection()

project = connection.get_project()

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
[GitRepo](https://docs.hopsworks.ai/hopsworks-api/dev/generated/api/git_repo/)

