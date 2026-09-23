# Cluster Configuration

## Introduction

Whether you run Hopsworks on-premise, or on the cloud using kubernetes, it is possible to change a variety of configurations on the cluster, changing its default behaviour.
This section is not going into detail for every setting, since every Hopsworks cluster comes with a robust default setup.
However, this guide is to explain where to find the configurations and if necessary, how to change them.

!!! note
    In most cases you will be only be prompted to change these configurations by a Hopsworks Solutions Engineer or similar.

## Prerequisites

An administrator account on a Hopsworks cluster.

### Step 1: The configuration page

You can find the configuration page by navigating in the UI:

1. Click on your user name in the top right corner, then select *Cluster Settings*.
2. Among the cluster settings, you will find a tab *Configuration*

<figure>
  <img src="../../../assets/images/admin/variables/configuration.png" alt="Configuration Settings" />
  <figcaption>Configuration settings</figcaption>
</figure>

### Step 2: Editing existing configurations

To edit an existing configuration, simply find the property using the search field, then click the *edit* button to change the value of the setting or its visibility.
Once you have made the change, don't forget to click *save* to persist the changes.

#### Visibility

The visibility setting indicates whether a setting can be read only by **Hops Admins** or also by simple **Hops Users**, that is everyone.
Additionally, you can also allow to read the setting even when **not authenticated**.
If the setting contains a password or sensitive information, you can also hide the value so it's not shown in the UI.

### Step 3: Adding a new configuration

In rare cases it might be necessary to add additional configurations.

To do so, click on *New Variable*, where you can then configure the new setting with a key, value and visibility.
Once you have set the desired properties, you can persist them by clicking *Create Configuration*

<figure>
  <img src="../../../assets/images/admin/variables/new-variable.png" alt="Adding a new configuration property" />
  <figcaption>Adding a new configuration property</figcaption>
</figure>

## Restricting file uploads

The `upload_policy` configuration controls who may upload files into the cluster.
Uploads are otherwise available to every user with write access to a dataset, so this setting exists for clusters that ingest data only through governed pipelines, or that have to limit what enters the platform.

| Value | Who may upload |
| ----- | -------------- |
| `enabled` | Any user with write access to the destination dataset. This is the default, so an existing cluster is unaffected until the value is changed. |
| `admins_only` | Only members of the `HOPS_ADMIN` group. |
| `disabled` | Nobody, administrators included. |

The policy is enforced by the backend, so it applies to the Hopsworks UI and to clients such as the Python API alike.
A refused upload returns HTTP 403.
In the UI the upload controls are disabled instead, so a blocked user is told before starting an upload rather than watching it fail.

You can set the value from the *Configuration* page described above, or at deploy time through the `hopsworks.variables.upload_policy` value of the Helm chart.
A value set in the Helm chart is reapplied on every upgrade, so a change made from the Configuration page holds until the cluster is next upgraded.
Any value other than the three above is treated as `enabled`, so that a typo cannot block uploads without anyone noticing.

This setting governs uploading new files into the cluster, and nothing else.
It does not restrict operations that only reference files already in the cluster filesystem, such as installing a Python library from a requirements file that is already in a project, because no file is transferred in that case.
It also does not remove files that were uploaded before the value was changed.
