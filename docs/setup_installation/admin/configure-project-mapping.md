# Configure group to project mapping

## Introduction

A group-to-project mapping lets you automatically add all members of a Hopsworks group to a project, eliminating the need to add each user individually. To create a mapping, you simply select a Hopsworks group, choose the project it should be linked to, and assign the role that its members will have within that project.

Once a mapping is created, project membership is controlled through Hopsworks group membership. Any updates made to the Hopsworks group—such as adding or removing users—will automatically be reflected in the project membership. For example, if a user is removed from the Hopsworks group, they will also be removed from the corresponding project.

## Prerequisites

1. Hopsworks group mapping sync enabled. This can be done by setting the variable ```hw_group_mapping_sync_enabled=true```.
See [Cluster Configuration](./variables.md) on how to change variable values in Hopsworks.

<figure>
 <a  href="../../../../assets/images/admin/project-mapping/configuration-variables.png">
   <img src="../../../../assets/images/admin/project-mapping/configuration-variables.png" alt="Enable Hopsworks mapping" />
 </a>
 <figcaption>Enable Hopsworks mapping</figcaption>
</figure>

If you can not find the variable ```hw_group_mapping_sync_enabled``` create it by clicking on **New variable**.

<figure>
 <a  href="../../../../assets/images/admin/project-mapping/configuration-hw-mapping.png">
   <img src="../../../../assets/images/admin/project-mapping/configuration-hw-mapping.png" alt="Create Hopsworks mapping enabled variable" />
 </a>
 <figcaption>Create Hopsworks group mapping enabled variable</figcaption>
</figure>

### Step 1: Create a mapping

To create a mapping go to **Cluster Settings** by clicking on your name in the top right
corner of the navigation bar and choosing *Cluster Settings* from the dropdown menu.
In the *Project mapping* tab, you can create a new mapping by clicking on *Create new mapping*.

<figure>
 <a  href="../../../../assets/images/admin/project-mapping/project-mapping-empty.png">
   <img src="../../../../assets/images/admin/project-mapping/project-mapping-empty.png" alt="Project mapping tab" />
 </a>
 <figcaption>Project mapping</figcaption>
</figure>

This will take you to the create mapping page shown below
<figure>
 <a  href="../../../../assets/images/admin/project-mapping/create-hw-mapping.png">
   <img src="../../../../assets/images/admin/project-mapping/create-hw-mapping.png" alt="Create mapping" />
 </a>
 <figcaption>Create mapping</figcaption>
</figure>

Here you can enter your Hopsworks group and map it to a project from the *Project* drop down list.
You can also choose the *Project role* users will be assigned when they are added to the project.

Finally, click on *Create mapping* and go back to mappings. You should see the newly created mapping(s) as shown below.

<figure>
 <a  href="../../../../assets/images/admin/project-mapping/group-to-project-mappings.png">
   <img src="../../../../assets/images/admin/project-mapping/group-to-project-mappings.png" alt="Project mappings" />
 </a>
 <figcaption>Project mappings</figcaption>
</figure>

### Step 2: Edit a mapping

From the list of mappings click on the edit button (:material-pencil:). This will open a popup that will allow you to change the *group*, *project name*, and *project role* of a mapping.

<figure>
 <a  href="../../../../assets/images/admin/project-mapping/edit-hw-mapping.png">
   <img src="../../../../assets/images/admin/project-mapping/edit-hw-mapping.png" alt="Edit mapping" />
 </a>
 <figcaption>Edit mapping</figcaption>
</figure>

!!!Warning
    Updating a mapping's *group* or *project name* will remove all members of the previous group from the project.

### Step 3: Delete a mapping

To delete a mapping click on the delete button.

!!!Warning
    Deleting a mapping will remove all members of that group from the project.
