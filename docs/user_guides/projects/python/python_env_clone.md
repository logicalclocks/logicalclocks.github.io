# How To Clone Python Environment

### Introduction

Cloning an environment in Hopsworks means creating a copy of one of the base environments. The base environments are immutable, meaning that it is required to clone an environment before you can make any change to it, such as installing your own libraries. This ensures that the project maintains a set of stable environments that are tested with the capabilities of the platform, meanwhile through cloning, allowing users to further customize an environment without affecting the base environments.

In this guide, you will learn how to clone an environment.

## Step 1: Select an environment

Under the `Project settings` section you can find the `Python environment` setting.

First select an environment, for example the `python-feature-pipeline`.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/python/clone_env_1.png" alt="">
    <figcaption>Select a base environment</figcaption>
  </figure>
</p>

## Step 2: Clone environment

The environment can now be cloned by clicking `Clone env` and entering a name and description. The interface will show `Syncing packages` while creating the environment.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/python/clone_env_2.png" alt="Create environment">
    <figcaption>Clone a base environment</figcaption>
  </figure>
</p>

## Step 3: Environment is now ready

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/python/clone_env_3.png" alt="">
    <figcaption>Environment is now cloned</figcaption>
  </figure>
</p>

!!! notice "What does the CUSTOM mean?"
    Notice that the cloned environment is tagged as `CUSTOM`, it means that it is a base environment which has been cloned.

!!! notice "Base environment also marked"
    When you select a `CUSTOM` environment the base environment it was cloned from is also shown.

## Concerning upgrades

!!! warning "Please note"
    The base environments are automatically upgraded when Hopsworks is upgraded and application code should keep functioning provided that no breaking changes were made in the upgraded version of the environment. A `CUSTOM` environment is not automatically upgraded and the users is recommended to reapply the modifications to a base environment if they encounter issues after an upgrade.

## Next steps

In this guide you learned how to clone a new environment. The next step is to [install](python_install.md) a library in the environment.
