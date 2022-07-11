# How To Install Python Libraries

## Introduction

The prepackaged python environment in Hopsworks contains a large number of libraries for data engineering, machine learning and more general data science development. But in some cases users want to install additional packages for their applications.

In this guide, you will learn how to install Python packages using these different options.

* PyPi, using pip package manager
* A conda channel, using conda package manager
* Packages saved in certain file formats, currently we support .whl or .egg
* A public or private git repository
* A requirements.txt file to install multiple libraries at the same time using pip
* An environment.yml file to install multiple libraries at the same time using conda and pip

Under the `Project settings` section you can find the `Python libraries` setting.

### Name and version

Enter the name and, optionally, the desired version to install.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/python/install_name_version.gif" alt="Installing library by name and version">
    <figcaption>Installing library by name and version</figcaption>
  </figure>
</p>

### Search

Enter the search term and select a library and version to install.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/python/install_search.gif" alt="Installing library using search">
    <figcaption>Installing library using search</figcaption>
  </figure>
</p>

### Distribution (.whl, .egg..)

Install a python package by uploading the corresponding package file and selecting it in the file browser.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/python/install_dep.gif" alt="Installing library from file">
    <figcaption>Installing library from file</figcaption>
  </figure>
</p>

### Git source

To install from a git repository simply provide the repository URL. The URL you should provide is the same as you would enter on the command line using `pip install git+{repo_url}`.
In the case of a private git repository, also select whether it is a GitHub or GitLab repository and the preconfigured access token for the repository.

**Note**: If you are installing from a git repository which is not GitHub or GitLab simply supply the access token in the URL. Keep in mind that in this case the access token may be visible in logs for other users in the same project to see.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/python/install_git.gif" alt="Installing library from git repo">
    <figcaption>Installing library from git repo</figcaption>
  </figure>
</p>


## Conclusion

In this guide you learned how to install python libraries. Now you can use the library in a [Jupyter notebook](../jupyter/python_notebook.md) or a [Job](../jobs/python_job.md).
