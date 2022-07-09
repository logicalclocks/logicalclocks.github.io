# How To Recreate Python Environment

### Introduction

Sometimes it may be desirable to recreate the python environment to start from the same state the python environment was created with.

In this guide, you will learn how to recreate the python environment.

!!! warning "Keep in mind"
    There may be Jobs or Jupyter notebooks that depend on additional libraries that have been installed. It is recommended to first [export the environment](python_env_export.md) to save a snapshot of all libraries currently installed and their versions.

## Step 1: Remove the environment

Under the `Project settings` section you can find the `Python libraries` setting.

First click `Remove env`.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/python/remove_env.png" alt="Remove environment">
    <figcaption>Remove environment</figcaption>
  </figure>
</p>

## Step 2: Create new environment

After removing the environment, simply recreate it by clicking `Create Environment`.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/python/create_env.png" alt="Create environment">
    <figcaption>Create environment</figcaption>
  </figure>
</p>

## Conclusion

In this guide you learned how to recreate your python environment.