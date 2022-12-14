# User permissions

## Introduction

Permissions allow only authorized users to enact changes on the Hopsworks platform. This can be beneficial when working in a group on a single project or when sharing multiple projects. To make this process as fast/simple as possible Hopsworks provides users with preset roles to pick from.


## Project member roles

Project members can be assigned to 2 different roles, depending on the privileges necessary for him/her to fulfill their needs.

<p align="center">
  <figure>
    <img src="../../../../assets/images/guides/project/members_list.png" alt="List of project members with their role">
  </figure>
</p>

### Data owner

Data owners hold the highest authority in the project, having full control of its contents.

Capable of:
- Sharing project
- Managing project and its members
- Working with all feature store abstractions (such as Feature groups, Feature views, Storage connectors, etc.)

It is worth mentioning that the project's creator (aka. `author`) is a special type of `Data owner`. He is the only user capable of deleting the project and it is impossible to change his role to `Data scientist`.

### Data scientist

Data scientists can be viewed as the users of data.

Capable of:
- Managing self-made Feature views/Training datasets
- Using previously created feature store abstractions


## Project members in a shared feature store

The projects can be shared exclusively using `read-only` permission. This means that a member is not capable of enacting any changes on the shared project, without also being a part of that project.


## Conclusion

Properly set up permissions can help a user avoid permisong changes that they should not be capable of doing on the project. Therefore, the member's role should be picked, based on the expected usage, and when in doubt pick the role with the least privileges. The members' role can be revised if there is no need for it.
