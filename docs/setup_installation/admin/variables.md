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
