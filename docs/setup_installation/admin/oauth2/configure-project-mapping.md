# Configure OAuth2 group to project mapping

## Introduction
A group-to-project mapping lets you automatically add all members of an OAuth2 group to a project, eliminating the need to add each user individually. To create a mapping, you simply select an OAuth2 group, choose the project it should be linked to, and assign the role that its members will have within that project.

Once a mapping is created, project membership is controlled through OAuth2 group membership. Any updates made to the OAuth2 group—such as adding or removing users—will automatically be reflected in Hopsworks. For example, if a user is removed from the OAuth2 group, they will also be removed from the corresponding project.

## Prerequisites
1. A server configured with OAuth2. See [Register Identity Provider in Hopsworks](./create-client.md) for instructions on how to do this.
2. OAuth2 group mapping sync enabled. This can be done by setting the variable ```oauth_group_mapping_sync_enabled=true```.
See [Cluster Configuration](../variables.md) on how to change variable values in Hopsworks.
<figure>
 <a  href="../../../../assets/images/admin/project-mapping/configuration-variables.png">
   <img src="../../../../assets/images/admin/project-mapping/configuration-variables.png" alt="Enable OAuth2 mapping" />
 </a>
 <figcaption>Enable OAuth2 mapping</figcaption>
</figure>

If you can not find the variable ```oauth_group_mapping_sync_enabled``` create it by clicking on **New variable**.

<figure>
 <a  href="../../../../assets/images/admin/project-mapping/configuration-oauth-mapping.png">
   <img src="../../../../assets/images/admin/project-mapping/configuration-oauth-mapping.png" alt="Create OAuth2 mapping enabled variable" />
 </a>
 <figcaption>Create OAuth2 mapping enabled variable</figcaption>
</figure>

### Step 1: Create a mapping
To create a mapping go to **Cluster Settings** by clicking on your name in the top right
corner of the navigation bar and choosing *Cluster Settings* from the dropdown menu.
In the _Project mapping_ tab, you can create a new mapping by clicking on _Create new mapping_.

<figure>
 <a  href="../../../../assets/images/admin/project-mapping/project-mapping-empty.png">
   <img src="../../../../assets/images/admin/project-mapping/project-mapping-empty.png" alt="Project mapping tab" />
 </a>
 <figcaption>Project mapping</figcaption>
</figure>

This will take you to the create mapping page shown below
<figure>
 <a  href="../../../../assets/images/admin/project-mapping/create-oauth-mapping.png">
   <img src="../../../../assets/images/admin/project-mapping/create-oauth-mapping.png" alt="Create mapping" />
 </a>
 <figcaption>Create mapping</figcaption>
</figure>

Here you can enter your OAuth2 group and map it to a project from the _Project_ drop down list.
You can also choose the _Project role_ users will be assigned when they are added to the project.

Finally, click on _Create mapping_ and go back to mappings. You should see the newly created mapping(s) as shown below.

<figure>
 <a  href="../../../../assets/images/admin/project-mapping/group-to-project-mappings.png">
   <img src="../../../../assets/images/admin/project-mapping/group-to-project-mappings.png" alt="Project mappings" />
 </a>
 <figcaption>Project mappings</figcaption>
</figure>

!!!Note
    Make sure the group names from your OAuth2 provider match the one you entered above.

    If your identity provider uses a claim name other than ```groups``` or ```roles``` to represent group information, be sure to specify that claim name in the **Group Claim** field when setting up your identity provider.

### Step 2: Edit a mapping

From the list of mappings click on the edit button (:material-pencil:). This will open a popup that will allow you to change the _remote group_, _project name_, and _project role_ of a mapping.

<figure>
 <a  href="../../../../assets/images/admin/project-mapping/edit-mapping.png">
   <img src="../../../../assets/images/admin/project-mapping/edit-mapping.png" alt="Edit mapping" />
 </a>
 <figcaption>Edit mapping</figcaption>
</figure>

!!!Warning
    Updating a mapping's _remote group_ or _project name_ will remove all members of the previous group from the project.

### Step 3: Delete a mapping

To delete a mapping click on the delete button.

!!!Warning
    Deleting a mapping will remove all members of that group from the project.