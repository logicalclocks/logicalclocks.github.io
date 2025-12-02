# Configure LDAP/Kerberos group to project mapping

## Introduction

A group-to-project mapping lets you automatically add all members of an LDAP group to a project, eliminating the need to add each user individually.
To create a mapping, you simply select the LDAP group, choose the project it should be linked to, and assign the role that its members will have within that project.

Once a mapping is created, project membership is controlled through LDAP group membership.
Any updates made to the LDAP group—such as adding or removing users—will automatically be reflected in Hopsworks.
For example, if a user is removed from the LDAP group, they will also be removed from the corresponding project.

## Prerequisites

1. A server configured with LDAP or Kerberos. See [Server Configuration for Kerberos](./configure-server.md#step-2-server-configuration-for-kerberos) and [Server Configuration for LDAP](./configure-server.md#step-1-server-configuration-for-ldap) for instructions on how to do this.
2. LDAP group mapping sync enabled. This can be done by setting the variable ```ldap_group_mapping_sync_enabled=true```.

See [Cluster Configuration](../variables.md) on how to change variable values in Hopsworks.
<figure>
 <a  href="../../../../assets/images/admin/project-mapping/configuration-variables.png">
   <img src="../../../../assets/images/admin/project-mapping/configuration-variables.png" alt="Enable ldap mapping" />
 </a>
 <figcaption>Enable ldap mapping</figcaption>
</figure>

If you can not find the variable ```ldap_group_mapping_sync_enabled``` create it by clicking on **New variable**.

<figure>
 <a  href="../../../../assets/images/admin/project-mapping/configuration-ldap-mapping.png">
   <img src="../../../../assets/images/admin/project-mapping/configuration-ldap-mapping.png" alt="Create ldap mapping enabled variable" />
 </a>
 <figcaption>Create ldap mapping enabled variable</figcaption>
</figure>

### Step 1: Create a mapping

To create a mapping go to **Cluster Settings** by clicking on your name in the top right corner of the navigation bar and choosing *Cluster Settings* from the dropdown menu.
In the *Project mapping* tab, you can create a new mapping by clicking on *Create new mapping*.

<figure>
 <a  href="../../../../assets/images/admin/project-mapping/project-mapping-empty.png">
   <img src="../../../../assets/images/admin/project-mapping/project-mapping-empty.png" alt="Project mapping tab" />
 </a>
 <figcaption>Project mapping</figcaption>
</figure>

This will take you to the create mapping page shown below
<figure>
 <a  href="../../../../assets/images/admin/project-mapping/create-ldap-mapping.png">
   <img src="../../../../assets/images/admin/project-mapping/create-ldap-mapping.png" alt="Create mapping" />
 </a>
 <figcaption>Create mapping</figcaption>
</figure>

Here you can choose from your LDAP groups and map them to a project from the *Project* drop down list.
You can also choose the *Project role* users will be assigned when they are added to the project.

Finally, click on *Create mapping* and go back to mappings. You should see the newly created mapping(s) as shown below.

<figure>
 <a  href="../../../../assets/images/admin/project-mapping/group-to-project-mappings.png">
   <img src="../../../../assets/images/admin/project-mapping/group-to-project-mappings.png" alt="Project mappings" />
 </a>
 <figcaption>Project mappings</figcaption>
</figure>

!!!Note
    If there are no groups in the *Remote group* drop down list check if **ldap_groups_search_filter** is correct by using the value in ```ldapsearch``` replacing ```%c``` with ```*```, as shown in the example below.

    ```ldapsearch -LLL -H ldap:/// -b '<base dn>' -D '<user dn>' -w <password> '(&(objectClass=groupOfNames)(cn=*))'```

    This should return all the groups in your LDAP.
    See [Cluster Configuration](../variables.md) on how to find and update the value of this variable.

### Step 2: Edit a mapping

From the list of mappings click on the edit button (:material-pencil:).
This will open a popup that will allow you to change the *remote group*, *project name*, and *project role* of a mapping.

<figure>
 <a  href="../../../../assets/images/admin/project-mapping/edit-mapping.png">
   <img src="../../../../assets/images/admin/project-mapping/edit-mapping.png" alt="Edit mapping" />
 </a>
 <figcaption>Edit mapping</figcaption>
</figure>

!!! Warning
    Updating a mapping's *remote group* or *project name* will remove all members of the previous group from the project.

### Step 3: Delete a mapping

To delete a mapping click on the delete button.

!!! Warning
    Deleting a mapping will remove all members of that group from the project.

### Step 4: Configure sync interval

After configuring all the group mappings users will be added to or removed from the projects in the mapping when they login to Hopsworks.
It is also possible to synchronize mappings without requiring users to log out.
This can be done by setting ```ldap_group_mapping_sync_interval``` to an interval greater or equal to 2 minutes.
If ```ldap_group_mapping_sync_interval``` is set group mapping sync will run periodically based on the interval and
add or remove users from projects.
