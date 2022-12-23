# Configure LDAP/Kerberos group to project mapping
 
## Introduction
A group to project mapping allows you to add members of your LDAP group to a project without having to
add each user manually. 
 
## Prerequisites
A server configured with LDAP or Kerberos. See [Server Configuration for Kerberos](../configure-server/#server-configuration-for-kerberos) and
[Server Configuration for LDAP](../configure-server/#server-configuration-for-ldap) for instructions on how to do this.
 
### Step 1: Create a mapping
To create a mapping go to **Cluster Settings** by clicking on your name in the top right
corner of the navigation bar and choosing *Cluster Settings* from the dropdown menu.
In the _Project mapping_ tab, you can create a new mapping by clicking on _Create new mapping_.
 
<figure>
 <a  href="../../../assets/images/admin/project-mapping/project-mapping-empty.png">
   <img src="../../../assets/images/admin/project-mapping/project-mapping-empty.png" alt="Project mapping tab" />
 </a>
 <figcaption>Project mapping</figcaption>
</figure>
 
This will take you to the create mapping page shown below
<figure>
 <a  href="../../../assets/images/admin/project-mapping/create-mapping.png">
   <img src="../../../assets/images/admin/project-mapping/create-mapping.png" alt="Create mapping" />
 </a>
 <figcaption>Create mapping</figcaption>
</figure>
 
Here you can choose multiple Remote groups from your LDAP groups and map them to a project from the _Project_ drop down list.
You can also choose the _Project role_ users will be assigned when they are added to the project.
 
Finally, click on _Create mapping_ and go back to mappings. You should see the newly created mapping(s) as shown below.
 
<figure>
 <a  href="../../../assets/images/admin/project-mapping/project-mappings.png">
   <img src="../../../assets/images/admin/project-mapping/project-mappings.png" alt="Project mappings" />
 </a>
 <figcaption>Project mappings</figcaption>
</figure>
 
!!!Note
    If there are no groups in the _Remote group_ drop down list check if **ldap_groups_search_filter** is correct by using the value
    in ```ldapsearch``` replacing ```%c``` with ```*```, as shown in the example below.
    
    ```ldapsearch -LLL -H ldap:/// -b '<base dn>' -D '<user dn>' -w <password> '(&(objectClass=groupOfNames)(cn=*))'```

    This should return all the groups in your LDAP. 
    
    See [Cluster Configuration](../variables.md) on how to find and update the value of this variable.
  
### Step 2: Edit a mapping
 
From the list of mappings click on the edit button (:material-pencil:). This will make the row editable and allow you to change
the _remote group_, _project name_, and _project role_ of a mapping.
 
<figure>
 <a  href="../../../assets/images/admin/project-mapping/edit-mapping.png">
   <img src="../../../assets/images/admin/project-mapping/edit-mapping.png" alt="Edit mapping" />
 </a>
 <figcaption>Edit mapping</figcaption>
</figure>
 
!!!Warning
    Updating a mapping's _remote group_ or _project name_ will remove all members of the previous group from the project.
 
### Step 3: Delete a mapping
 
To delete a mapping click on the delete button.
 
!!!Warning
    Deleting a mapping will remove all members of that group from the project.
