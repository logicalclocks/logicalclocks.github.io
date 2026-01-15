# How To Manage Members To A Project

## Introduction

In this guide, you will learn how to add new members to your project and understand the different roles available within a project.

## Step 1: View the members list

Navigate to the `Project settings` page and locate the `General` section, which displays the current members of the project.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/project/members/members_list.png" alt="List of project members">
    <figcaption>List of project members</figcaption>
  </figure>
</p>

## Step 2: Add a new member

Click `Add members` to open a dialog where you can invite users. Select one or more users to invite.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/project/members/add_new_member.png" alt="Add new member dialog">
    <figcaption>Add new member dialog</figcaption>
  </figure>
</p>

Each member can be assigned one of three roles, depending on the level of access they need.

### Data owner

Data owners hold the highest authority in the project, with full control over its contents.

They can:

- Share the project with other projects
- Manage project settings and members
- Create, read, update, and delete all feature store resources (feature groups, feature views, training datasets, etc.)

!!! note "Project author"
    The project creator is a special type of Data owner. Only the creator can delete the project, and their role cannot be changed.

### Data scientist

Data scientists are consumers and creators of feature views and training datasets.

They can:

- Create feature views and training datasets using existing feature groups
- Manage the feature views and training datasets they have created
- Read feature groups created by Data owners

### Feature store restricted

Feature store restricted users have the most limited access, designed for users who only need to consume specific features that have been explicitly [shared](../../fs/sharing/sharing.md) with them.

They can:

- Access and use feature groups that have been explicitly shared with them
- Create feature views and training datasets using shared features

## Step 3: Confirm member invitation

The invited user will now appear in the members list and will have immediate access to the project based on their assigned role.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/project/members/member_invited.png" alt="Member added to project">
    <figcaption>List of project members</figcaption>
  </figure>
</p>

## Step 4: Manage members

To change a member's role or remove them from the project, click the `Manage members` button. From there, you can modify roles or delete members as needed.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/project/members/manage_members.png" alt="Manage project members dialog">
    <figcaption>Managing members of project</figcaption>
  </figure>
</p>
