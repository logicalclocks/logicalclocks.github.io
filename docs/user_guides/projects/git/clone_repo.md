# How To Clone a Git Repository

## Introduction

Repositories are cloned and managed within the scope of a project. The content of the repository will reside on the Hopsworks File System. The content of the repository can be edited from Jupyter notebooks and can for example be used to configure Jobs.
Repositories can be managed from the Git section in the project settings. The Git overview in the project settings provides a list of repositories currently cloned within the project, the location of their content as well which branch and commit their HEAD is currently at.

!!! warning "Beta"
    The feature is currently in Beta and will be improved in the upcoming releases.

## Prerequisites

- For cloning a private repository, you should configure a [Git Provider](configure_git_provider.md) with your git credentials. You can clone a GitHub and GitLab public repository without configuring the provider. However, for BitBucket you always need to configure the username and password to clone a repository.

- The token permission should grant access to public and private repositories including read and write access to code and commit statuses.

## UI

### Step 1: Navigate to repositories

In the `Project settings` page you can find the `Git` section.

This page lists all the cloned git repositories under `Repositories`, while operations performed on those repositories, e.g `push`/`pull`/`commit` are listed under `Git Executions`.

<p align="center">
  <figure>
    <a  href="../../../../assets/images/guides/git/repository_overview.png">
      <img src="../../../../assets/images/guides/git/repository_overview.png" alt="Repository overview">
    </a>
    <figcaption>Git repository overview</figcaption>
  </figure>
</p>

### Step 2: Clone a repository

To clone a new repository, click on the `Clone repository` button on the Git overview page.

<p align="center">
  <figure>
    <a  href="../../../../assets/images/guides/git/clone_repo_dialog.png">
      <img src="../../../../assets/images/guides/git/clone_repo_dialog.png" alt="Clone a repository">
    </a>
    <figcaption>Git clone</figcaption>
  </figure>
</p>

You should first choose the git provider e.g., GitHub, GitLab or BitBucket. If you are cloning a private repository, remember to configure the username and password for the provder first in [Git Provider](configure_git_provider.md). The clone dialog also asks you to specify the URL of the repository to clone. The supported protocol is HTTPS. As an example, if the repository is hosted on GitHub, the URL should look like: `https://github.com/logicalclocks/hops-examples.git`.

Then specify which branch you want to clone. By default the `main` branch will be used, however a different branch or commit can be specified by selecting `Clone from a specific branch`.

You can select the folder, within your project, in which the repository should be cloned. By default, the repository is going to be cloned within the `Jupyter` dataset. However, by clicking on the location button, a different location can be selected.

Finally, click on the `Clone repository` button to trigger the cloning of the repository.

### Step 3: Track progress of the clone

The progress of the git clone can be tracked under `Git Executions`.

<p align="center">
  <figure>
    <a  href="../../../../assets/images/guides/git/repo_cloning.png">
      <img src="../../../../assets/images/guides/git/repo_cloning.png" alt="Clone a repository">
    </a>
    <figcaption>Track progress of clone</figcaption>
  </figure>
</p>

### Step 4: Browse repository files

In the `File browser` page you can now browse the files of the cloned repository. In the figure below, the repository is located in `Jupyter/hops-examples` directory.

<p align="center">
  <figure>
    <a  href="../../../../assets/images/guides/git/browse_repo_files.png">
      <img src="../../../../assets/images/guides/git/browse_repo_files.png" alt="Browse repository files">
    </a>
    <figcaption>Browse repository files</figcaption>
  </figure>
</p>

## Code
You can also clone a repository through the hopsworks git API in python.
q
### Step 1: Get the git API

```python

import hopsworks

connection = hopsworks.connection()

project = connection.get_project()

git_api = project.get_git_api()

```

### Step 2: Clone the repository

```python

REPO_URL="https://github.com/logicalclocks/hops-examples.git" # git repository
HOPSWORKS_FOLDER="Jupyter" # path in hopsworks filesystem to clone to
PROVIDER="GitHub"
BRANCH="master" # optional branch to clone

examples_repo = git_api.clone(REPO_URL, HOPSWORKS_FOLDER, PROVIDER, branch=BRANCH)

```

A notebook for managing git can be found [here](https://github.com/logicalclocks/hops-examples/blob/master/notebooks/services/git.ipynb).

## Errors and Troubleshooting
###     Invalid credentials
This might happen when the credentials entered for the provider are incorrect. Try the following:

- Confirm that the settings for the provider ( in Account Settings > Git providers) are correct. You must enter both your Git provider username and token.
- Confirm that you have selected the correct Git provider when cloning the repository.
- Ensure your personal access token or app password has the correct repository access rights.
- Ensure your personal access token or app password has not expired.

### Timeout errors
Cloning a large repo or checking out a large branch may hit timeout errors. You can try again later if the system was under heavy load at the time.

### Symlink errors
Git repositories with symlinks are not yet supported, therefore cloning repositories with symlinks will fail. You can create a separate branch to remove the symlinks, and clone from this branch.

## Conclusion

In this guide you learned how to clone a Git repository. You can now start [Jupyter](../jupyter/python_notebook.md) from the cloned git repository path to work with the files.