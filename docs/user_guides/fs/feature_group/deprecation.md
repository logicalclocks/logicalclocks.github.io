---
description: Documentation on how to deprecate a feature group in Hopsworks.
---

# How to deprecate a Feature Group

### Introduction

To discourage the usage of specific feature groups it is possible to deprecate them.
When a feature group is deprecated, user will be warned when they try to use it or use a feature view that depends on it.

In this guide you will learn how to deprecate a feature group within Hopsworks, showing examples in HSFS APIs as well as the user interface.

## Prerequisites

Before you begin this guide it is expected that there is an existing feature group in your project.
You can familiarize yourself with [the creation of a feature group](./create.md) in the user guide.

## Deprecate using the HSFS APIs

### Retrieve the feature group

To deprecate a feature group using the HSFS APIs you need to provide a [Feature Group](../../../concepts/fs/feature_group/fg_overview.md).

=== "Python"

    ```python
    fg = fs.get_feature_group(name="feature_group_name", version=feature_group_version)
    ```

### Deprecate Feature Group

Feature group deprecation occurs by calling the `update_deprecated` method on the feature group.

=== "Python"

    ```python
    fg.update_deprecated()
    ```

Users can also un-deprecate the feature group if need be, by setting the `deprecate` parameter to False.

=== "Python"

    ```python
    fg.update_deprecated(deprecate=False)
    ```

## Deprecate using the UI

You can deprecate/de-deprecate feature groups through the UI.
For this, navigate to the `Feature Groups` section and select a feature group.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/feature_group/feature_group_list.png" alt="List of Feature Groups">
  </figure>
</p>

Subsequently, make sure that the necessary feature group version is picked.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/feature_group/feature_group_version.png" alt="Feature Group version selection">
  </figure>
</p>

Finally, click on the button with three vertical dots in the right corner and select `Deprecate`.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/feature_group/feature_group_deprecate.png" alt="Deprecate Feature Group">
  </figure>
</p>

The Feature group can be de-deprecated by selecting the `Undeprecate` option on a deprecated feature group.
