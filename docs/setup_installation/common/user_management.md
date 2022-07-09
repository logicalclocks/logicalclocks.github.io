# User management
In Hopsworks.ai users can be grouped into *organizations* to access the same resources.
When a new user registers with Hopsworks.ai a new organization is created. This user later on can
invite other registered users to their organization so they can share access to the same clusters.

Cloud Accounts configuration is also shared among users of the same organization. So if user Alice has configured
her account with her credentials, all member of her *organization* will automatically deploy clusters in her cloud
account. Credits and cluster usage are also grouped to ease reporting.

## Adding members to an organization
Organization membership can be edited by clicking **Members** on the left of Hopsworks.ai Dashboard page.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/members_empty.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/members_empty.png" alt="Organization membership">
    </a>
    <figcaption>Organization membership</figcaption>
  </figure>
</p>

To add a new member to your organization add the user's email and click **Add**. The invited user will
receive an email with the invitation. You can set the user as administrator by checking the __Admin__ checkbox. More details about organization administrators can be found [here].(#administrator-role)

An invited user **must accept** the invitation to be part of the organization. An invitation will show up on the invitee's Dashboard. The invitee may have to close the __Welcome__ splash screen to be able to see the invitation.
In this example, Alice has invited Bob to her organization, but Bob hasn't accepted
the invitation yet.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/members_invited.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/members_invited.png" alt="Invitation">
    </a>
    <figcaption>Alice has sent the invitation</figcaption>
  </figure>

  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/members_accept.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/members_accept.png" alt="Accept invitation">
    </a>
    <figcaption>Bob's dashboard</figcaption>
  </figure>
</p>

## Sharing resources
Once Bob has accepted the invitation he does **not** have to configure his account, they share the same configuration.
Also, he will be able to view **the same** Dashboard as Alice, so he can start, stop or terminate clusters in the organization.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/alice_dashboard.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/alice_dashboard.png" alt="Alice dashboard">
    </a>
    <figcaption>Alice's dashboard</figcaption>
  </figure>

  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/bob_dashboard.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/bob_dashboard.png" alt="Bob dashboard">
    </a>
    <figcaption>Bob's dashboard</figcaption>
  </figure>
</p>

If Alice had existing clusters running and she had selected [Managed user management](../../aws/cluster_creation/#step-11-user-management-selection)
during cluster creation, an account will be automatically created for Bob on these clusters.

## Removing members from an organization
To remove a member from your organization simply go to **Members** page and click the **Remove** button next to the user you want to remove.
You will **stop** sharing any resource and the user **will be blocked** from any shared cluster.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/members_delete.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/members_delete.png" alt="Delete organization member">
    </a>
    <figcaption>Delete organization member</figcaption>
  </figure>
</p>

## Organization permissions
The owner and the administrators of an organization can set permissions at the organization level. For this got to the members tab, check the checkboxes in the __Member permissions__ section and click on __Update__.

The supported permissions are:

- __Non admin members can invite new members to the organization__. If this permission is enabled, any member of the organization will be able to invite other members to the organization. Note that only the owner and the administrators will be able to invite new members as administrators. If this permission is not enabled only the owner and the administrators can invite new members to the organization.
- __Non admin members can create and terminate clusters__. If this permission is enabled, any member of the organization will be able to create and terminate clusters. If it is not enabled, only the owner and the administrators will be able to create and terminate clusters.
- __Non admin members can open clusters ports__. If this permission is enabled, any member of the organization can open and close [services ports](./services.md) on organization's clusters. If it is not enabled, only the organization owner and administrators will be able to do so.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/members_permissions.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/members_permissions.png" alt="Modify permissions">
    </a>
    <figcaption>Modify permissions</figcaption>
  </figure>
</p>

## Administrator role 
Members of an organization can be set as administrators. This can be done by checking the __admin__ checkbox at the time of invitation or by checking the __admin__ checkbox then clicking the __Update__ button next to a member email.

Administrators can do all the actions described in the [Organization permissions](#organization-permissions) section of this documentation. They can also update the configuration of these permissions and set other users as administrators. Finally, administrators are automatically set as administrators on all the clusters of the organization that have [Managed user enabled](../../aws/cluster_creation/#step-11-user-management-selection) and are version __2.6.0__ or above.

<p align="center">
  <figure>
    <a  href="../../../assets/images/setup_installation/managed/common/members_set_admin.png">
      <img style="border: 1px solid #000" src="../../../assets/images/setup_installation/managed/common/members_set_admin.png" alt="Set a member as admin">
    </a>
    <figcaption>Set a member as admin</figcaption>
  </figure>
</p>