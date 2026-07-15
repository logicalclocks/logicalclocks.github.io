# Mandatory Tags

## Introduction

Mandatory tags let a Hopsworks administrator require that specific tag schemas are populated on artifacts.
They build on top of [tags](tags.md) and are used to enforce governance rules, such as requiring every model to declare a data owner.

A mandatory tag is a tag schema that has been marked as required for one or more artifact types.
The supported artifact types are feature groups, feature views, training datasets, models and deployments.

## Prerequisites

A mandatory tag references an existing tag schema.
Define the tag schema first, as described in the [Tags](tags.md) guide, before marking it mandatory.

Only administrators can configure mandatory tags.
Attaching the tag values afterwards is done by any project member with write access to the artifact.

## Configure mandatory tags

Mandatory tags are configured in two scopes.

- Cluster-wide mandatory tags apply to every project on the cluster.
  They are configured by an administrator in the `Cluster settings` > `Tag schemas` section.

    <img src="../../../../assets/images/guides/tags/cluster_wide_mandatory_tags.png" alt="Configure cluster-wide mandatory tags under Cluster settings, Tag Schemas">

- Project-specific mandatory tags apply only to a single project.
  They are configured by an administrator in the `Cluster settings` > `Projects` section, by selecting the project.

    <img src="../../../../assets/images/guides/tags/project_mandatory_tags.png" alt="Configure project-specific mandatory tags under Cluster settings, Projects, by editing a project">

For each mandatory tag you select the artifact types it applies to.
A tag schema can be mandatory for any combination of feature groups, feature views, training datasets, models and deployments.
For example, a `data_owner` schema can be marked mandatory for models and deployments only, leaving feature groups, feature views and training datasets unaffected.

## Enforcement per artifact type

All five artifact types, feature groups, feature views, training datasets, models and deployments, enforce mandatory tags the same way.

The create request is validated against the configured mandatory tags.
If any mandatory tag is missing from the tags provided at creation, the artifact is not created and the request is rejected with an HTTP 400 error that lists the missing tag names.
The bulk tag endpoint applies the same validation.

An artifact created before a tag was marked mandatory stays valid and is not deleted.
The missing tag is surfaced on read through the `missing_mandatory_tags` property, described in [Missing mandatory tags on pre-existing artifacts](#missing-mandatory-tags-on-pre-existing-artifacts), and on the artifact page in the UI.

## Attach mandatory tags at creation

Pass the mandatory tag values in the `tags` argument of the create call so the create request carries them and passes validation.
The `tags` argument takes the same shape as feature group tags: a `{"name": ..., "value": ...}` dictionary, a list of such dictionaries, or `Tag` objects, where the value is a single primitive or a dictionary matching the tag schema.

=== "Feature Group (Python)"

    ```python
    fs = project.get_feature_store()

    # data_owner is mandatory for feature groups; pass it at creation
    fg = fs.create_feature_group(
        name="transactions",
        version=1,
        primary_key=["id"],
        tags=[{"name": "data_owner", "value": "email@hopsworks.ai"}],
    )
    fg.insert(df)
    ```

=== "Feature View (Python)"

    ```python
    fs = project.get_feature_store()
    fg = fs.get_feature_group("transactions", version=1)

    # data_owner is mandatory for feature views; pass it at creation
    fv = fs.create_feature_view(
        name="transactions_fv",
        version=1,
        query=fg.select_all(),
        tags=[{"name": "data_owner", "value": "email@hopsworks.ai"}],
    )
    ```

=== "Training Dataset (Python)"

    ```python
    fs = project.get_feature_store()
    fv = fs.get_feature_view("transactions_fv", version=1)

    # data_owner is mandatory for training datasets; pass it at creation
    td_version, td_job = fv.create_training_data(
        tags=[{"name": "data_owner", "value": "email@hopsworks.ai"}],
    )
    ```

=== "Model (Python)"

    ```python
    mr = project.get_model_registry()

    # data_owner is mandatory for models; pass it at creation
    model = mr.python.create_model(
        name="fraud_model",
        metrics={"accuracy": 0.94},
        tags=[{"name": "data_owner", "value": "email@hopsworks.ai"}],
    )
    model.save("/path/to/model_artifacts")

    # Deploy the model; pass the mandatory deployment tag on the deploy call
    deployment = model.deploy(
        name="fraudmodeldeployment",
        tags=[{"name": "data_owner", "value": "email@hopsworks.ai"}],
    )
    ```

=== "Deployment (Python)"

    ```python
    ms = project.get_model_serving()

    # Build a predictor for an already-saved model
    predictor = ms.create_predictor(model)

    # data_owner is mandatory for deployments; pass it at creation
    deployment = ms.create_deployment(
        predictor,
        name="fraudmodeldeployment",
        tags=[{"name": "data_owner", "value": "email@hopsworks.ai"}],
    )
    deployment.save()
    ```

Omitting a mandatory tag from the `tags` argument rejects the create request with an HTTP 400 error that lists the missing tag names.

## Missing mandatory tags on pre-existing artifacts

Marking a tag mandatory does not retroactively reject artifacts that already exist without it.
An artifact created before the tag became mandatory stays valid, and Hopsworks surfaces the gap on read rather than deleting the artifact.

Fetching such an artifact emits a Python `UserWarning` listing the missing tag names.
The same list is available on the fetched object through the `missing_mandatory_tags` property and is shown on the artifact page in the UI.
The property is populated when the object is fetched from the backend and reflects the state at fetch time.
Adding a tag does not update the property on the object in hand, so fetch the artifact again to see the updated list.

=== "Model (Python)"

    ```python
    mr = project.get_model_registry()

    # If data_owner is mandatory but was never set on this model,
    # the fetch emits: UserWarning: Missing mandatory tags: ['data_owner']
    model = mr.get_model("fraud_model", version=1)

    # Names of mandatory tags that are required for this model but not yet set
    missing = [tag["name"] for tag in model.missing_mandatory_tags]

    # Set the missing tag
    if "data_owner" in missing:
        model.add_tag("data_owner", "email@hopsworks.ai")

    # missing_mandatory_tags reflects the state at fetch time,
    # so fetch the model again to see the updated list (no warning now)
    model = mr.get_model("fraud_model", version=1)
    print(model.missing_mandatory_tags)  # []
    ```

=== "Deployment (Python)"

    ```python
    ms = project.get_model_serving()

    # If data_owner is mandatory but was never set on this deployment,
    # the fetch emits: UserWarning: Missing mandatory tags: ['data_owner']
    deployment = ms.get_deployment("fraudmodeldeployment")

    missing = [tag["name"] for tag in deployment.missing_mandatory_tags]

    # Set the missing tag
    if "data_owner" in missing:
        deployment.add_tag("data_owner", "email@hopsworks.ai")

    # Fetch the deployment again to see the updated list (no warning now)
    deployment = ms.get_deployment("fraudmodeldeployment")
    print(deployment.missing_mandatory_tags)  # []
    ```

After the tag is set, it no longer appears in `missing_mandatory_tags` on the next fetch, and the fetch no longer warns.
