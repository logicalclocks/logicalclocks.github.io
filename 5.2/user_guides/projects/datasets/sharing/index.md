# Sharing A Dataset

## Introduction

Besides [sharing feature groups and feature views][sharing], you can share any dataset in your project's file browser (`Resources`, `Models`, `Jupyter`, etc.) with another project.
This grants the target project's members read (or write) access to that directory, without exposing the rest of your project.

!!! warning "Requires the Data owner role"
    Only a [Data owner][data-owner] in the project the dataset lives in can share or unshare a dataset, because sharing exposes project data to members outside the project.

!!! note "Feature store datasets are always read-only"
    Feature store datasets can only be shared as `READ_ONLY`.
    To grant richer access to feature store data, use [feature store / feature group sharing][sharing] instead.

## UI

In the `Files` view, select the dataset (top-level folder) you want to share and choose `Share` from its context menu.
Choose the target project and the permission to grant, then confirm.

To revoke a share later, choose `Unshare` on the same dataset and select the project to remove.

## Python SDK

```python
import hopsworks


project = hopsworks.login()
dataset_api = project.get_dataset_api()

# Share a dataset with another project (read-only by default)
dataset_api.share("Resources/my_dir", target_project="other_project")

# Or grant write access
dataset_api.share(
    "Resources/my_dir", target_project="other_project", permission="EDITABLE"
)

# Revoke a share
dataset_api.unshare("Resources/my_dir", target_project="other_project")
```
