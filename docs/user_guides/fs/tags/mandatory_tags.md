# Mandatory Tags

## Introduction

Mandatory tags let a Hopsworks administrator require that specific tag schemas are populated on artifacts.
They build on top of [tags][tags] and are used to enforce governance rules, such as requiring every model to declare a data owner before it is promoted.

A mandatory tag is a tag schema that has been marked as required for one or more artifact types.
The supported artifact types are feature groups, feature views, training datasets, models and deployments.

## Prerequisites

A mandatory tag references an existing tag schema.
Define the tag schema first, as described in [Tags][tags], before marking it mandatory.

Only administrators can configure mandatory tags.
Attaching the tag values afterwards is done by any project member with write access to the artifact.

## Configure mandatory tags

Mandatory tags are configured in two scopes.

- Cluster-wide mandatory tags apply to every project on the cluster.
  They are configured by an administrator in the `Cluster settings` > `Tag schemas` section.
- Project-specific mandatory tags apply only to a single project.
  They are configured in the project's `Project Settings` > `Governance Policies` section.

For each mandatory tag you select the artifact types it applies to.
A tag schema can be mandatory for any combination of feature groups, feature views, training datasets, models and deployments.
For example, a `data_owner` schema can be marked mandatory for models and deployments only, leaving feature store artifacts unaffected.

## Missing mandatory tags on models and deployments

When a mandatory tag has not yet been set on a model or a deployment, Hopsworks surfaces it as a missing mandatory tag rather than blocking the artifact from existing.
The list of missing mandatory tags is available on the model and deployment objects through the `missing_mandatory_tags` property, and is shown on the artifact page in the UI.

=== "Model (Python)"

    ```python
    mr = project.get_model_registry()
    model = mr.get_model("fraud_model", version=1)

    # Names of mandatory tags that are required for this model but not yet set
    missing = [tag["name"] for tag in model.missing_mandatory_tags]

    # Set the missing tag to clear the warning
    if "data_owner" in missing:
        model.add_tag("data_owner", "email@hopsworks.ai")
    ```

=== "Deployment (Python)"

    ```python
    ms = project.get_model_serving()
    deployment = ms.get_deployment("fraudmodeldeployment")

    missing = [tag["name"] for tag in deployment.missing_mandatory_tags]
    ```

After the tag is set, it no longer appears in `missing_mandatory_tags`.
