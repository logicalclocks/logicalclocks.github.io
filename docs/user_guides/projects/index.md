# Projects Guides

A project is the unit of ownership and access in Hopsworks: who is in it, what it can reach, and what it shares.
These guides cover signing in, creating and running a project, and the settings that hang off it.

<!-- markdownlint-disable MD030 -->
<div class="grid cards hops-start" markdown>

-   :material-folder-plus-outline:{ .lg .middle } **Start here**

    ---

    Create a project, mint an API key, and connect from any Python environment.

    ```python
    import hopsworks


    project = hopsworks.login()
    fs = project.get_feature_store()
    ```

    [Create a project](project/create_project.md) · [Create an API key](api_key/create_api_key.md) · [Wizard](wizard.md)

</div>
<!-- markdownlint-enable MD030 -->

<div class="hops-task-index" markdown>

<div class="hops-task-group" markdown>
:material-account-key-outline:{ .hops-role-ico } Get in
{ .hops-role-cap }

- [Sign in](auth/login.md)
  Register and log in, or use OAuth2, LDAP or Kerberos when your cluster is configured for it.
- [API keys](api_key/create_api_key.md)
  Authenticate from outside the cluster: laptops, CI, agents.
- [Manage a project](project/create_project.md)
  Create projects and add members with roles.
- [Wizard](wizard.md)
  Scaffold a whole system from a description, in a fresh project.
- [Search](search.md)
  Find feature groups, feature views and models, and follow their lineage.

</div>

<div class="hops-task-group" markdown>
:material-cog-outline:{ .hops-role-ico } Configure
{ .hops-role-cap }

- [Secrets and environment variables](secrets/create_secret.md)
  Store credentials once and read them from notebooks and jobs.
- [Git providers](git/configure_git_provider.md)
  Connect GitHub, GitLab or Bitbucket, then clone and push from the project.
- [Dataset sharing](datasets/sharing.md)
  Share datasets across projects.
- [AWS IAM roles](iam_role/iam_role_chaining.md)
  Assume roles from the project to reach AWS resources.
- [Alerts](alerts/index.md)
  Get notified on job failures, validation results and data shift.

</div>

</div>
