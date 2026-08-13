# How To Install Python Libraries

## Introduction

Hopsworks comes with several prepackaged Python environments that contain libraries for data engineering, machine learning, and more general data science use-cases.
Hopsworks also offers the ability to install additional packages from various sources, such as using the pip or conda package managers and public or private git repository.

In this guide, you will learn how to install Python packages using these different options.

- PyPi, using pip package manager
- A conda channel, using conda package manager
- Packages contained in .whl format
- A public or private git repository
- A requirements.txt file to install multiple libraries at the same time using pip
- npm packages, installed globally in the environment image and on `PATH` for jobs, Jupyter and
  the terminal

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
    If you are installing from a git repository which is not GitHub or GitLab simply supply the access token in the URL.
    Keep in mind that in this case the access token may be visible in logs for other users in the same project to see.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/python/install_git.gif" alt="Installing library from git repo">
    <figcaption>Installing library from git repo</figcaption>
  </figure>
</p>

#### npm packages

Environments also carry npm packages, installed globally in the image so they are on `PATH` for
jobs, Jupyter and the terminal. This is how you get a CLI tool or a JavaScript dependency into an
environment.

Open the **Installed npm Libraries** tab beside the Python one and use **Install npm package**.
Installed npm packages are listed there and can be uninstalled the same way, so an environment
records what it carries rather than accumulating changes nobody can see.

What the platform accepts:

| | |
| --- | --- |
| Versions | An exact version such as `1.3.0`, or a dist-tag such as `latest`. Ranges like `^1.0.0` are refused, because they are not reproducible. |
| Scoped names | Supported, for example `@tsconfig/node20`. |
| Flags | A fixed set: `--ignore-scripts`, `--legacy-peer-deps`, `--no-audit`, `--no-fund`, `--no-optional`, `--strict-peer-deps`. Anything else is refused and the message lists what is allowed. |

Installing by dist-tag records the version the tag resolved to once the build finishes, so `latest`
becomes the concrete version in the listing rather than staying as `latest`.

A package the base image already ships cannot be installed over, and cannot be uninstalled. Clone
an environment and install your own version there instead.

Packages come from the registry the cluster is configured to use. Ask your administrator if you
need an internal registry; it is a cluster-wide setting rather than a per-environment one.

!!! note "Same name in both ecosystems"
    A name can exist on both PyPI and npm. The two are tracked separately, so installing `requests`
    from npm does not touch the Python package of the same name, and each is listed under its own
    tab.

## Going Further

Now you can use the library in a [Jupyter notebook](../jupyter/python_notebook.md) or a [Job](../jobs/python_job.md).
