# How To Install Python Libraries

## Introduction

Hopsworks comes with several prepackaged Python environments that contain libraries for data engineering, machine learning, and more general data science use-cases. Hopsworks also offers the ability to install additional packages from various sources, such as using the pip or conda package managers and public or private git repository.

In this guide, you will learn how to install Python packages using these different options.

* PyPi, using pip package manager
* A conda channel, using conda package manager
* Packages contained in .whl format
* A public or private git repository
* A requirements.txt file to install multiple libraries at the same time using pip

!!! notice "Notice"
    If your libraries require installing some extra OS-Level packages, refer to the guide custom commands guide on how to install OS-Level packages.

## Prerequisites

In order to install a custom dependency one of the base environments must first be cloned, follow [this guide](python_env_clone.md) for that.

### Step 1: Go to environments page

Under the `Project settings` section select the `Python environment` setting.

### Step 2: Select a CUSTOM environment

Select the environment that you have previously cloned and want to modify.

### Step 3: Installation options

#### Name and version

Enter the name and, optionally, the desired version to install.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/python/install_name_version.gif" alt="Installing library by name and version">
    <figcaption>Installing library by name and version</figcaption>
  </figure>
</p>

#### Search

Enter the search term and select a library and version to install.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/python/install_search.gif" alt="Installing library using search">
    <figcaption>Installing library using search</figcaption>
  </figure>
</p>

#### Distribution (.whl, .egg..)

Install a python package by uploading the corresponding package file and selecting it in the file browser.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/python/install_dep.gif" alt="Installing library from file">
    <figcaption>Installing library from file</figcaption>
  </figure>
</p>

#### Git source

The URL you should provide is the same as you would enter on the command line using `pip install git+{repo_url}`, where `repo_url` is the part that you enter in `Git URL`.

For example to install matplotlib 3.7.2, the following are correct inputs:

`matplotlib @ git+https://github.com/matplotlib/matplotlib@v3.7.2`

`git+https://github.com/matplotlib/matplotlib@v3.7.2`

In the case of a private git repository, also select whether it is a GitHub or GitLab repository and the preconfigured access token for the repository.

!!! notice "Keep your secrets safe"
    If you are installing from a git repository which is not GitHub or GitLab simply supply the access token in the URL. Keep in mind that in this case the access token may be visible in logs for other users in the same project to see.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/python/install_git.gif" alt="Installing library from git repo">
    <figcaption>Installing library from git repo</figcaption>
  </figure>
</p>

## Going Further

Now you can use the library in a [Jupyter notebook](../jupyter/python_notebook.md) or a [Job](../jobs/python_job.md).
