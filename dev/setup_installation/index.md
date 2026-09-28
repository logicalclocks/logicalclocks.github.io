# Setup and Administration

Hopsworks runs on Kubernetes, on a cloud provider or on your own hardware.
This section covers installing the platform and administering it afterwards.
For the client libraries, see the [Client Installation](../user_guides/client_installation/index.md) guide.

<!-- markdownlint-disable MD030 -->
<div class="grid cards hops-start" markdown>

-   :material-kubernetes:{ .lg .middle } **Start here**

    ---

    Pick your environment and follow its getting started guide.
    Each one takes you from an empty account to a running cluster with a first project.

    [AWS](aws/getting_started.md) · [Azure](azure/getting_started.md) · [GCP](gcp/getting_started.md) · [On-prem](on_prem/contact_hopsworks.md)

</div>
<!-- markdownlint-enable MD030 -->

<div class="hops-task-index" markdown>

<div class="hops-task-group" markdown>
:material-cloud-outline:{ .hops-role-ico } Install
{ .hops-role-cap }

- [AWS, Azure, GCP](aws/getting_started.md)
  Managed Kubernetes on each cloud, with the storage and network the cluster needs.
- [On-prem](on_prem/contact_hopsworks.md)
  Your own Kubernetes, optionally with an external Kafka cluster.
- [Cluster configuration](admin/variables.md)
  Configuration variables, with the full reference and build performance notes.

</div>

<div class="hops-task-group" markdown>
:material-account-group-outline:{ .hops-role-ico } Users and access
{ .hops-role-cap }

- [Users and projects](admin/user.md)
  Approve users, assign roles, manage projects and quotas.
- [Authentication](admin/auth.md)
  OAuth2 identity providers, LDAP and Kerberos, with project mapping.
- [IAM role chaining](admin/roleChaining.md)
  Let projects assume AWS roles.

</div>

<div class="hops-task-group" markdown>
:material-shield-check-outline:{ .hops-role-ico } Operate
{ .hops-role-cap }

- [Monitoring](admin/monitoring/grafana.md)
  Service dashboards, exported metrics and service logs.
- [High availability and disaster recovery](admin/ha-dr/intro.md)
  Replicated services and backup, restore procedures.
- [Audit and operations](admin/audit/audit-logs.md)
  Access audit logs, service operations, search index.
- [Alerts, Trino, Superset](admin/alert.md)
  Cluster-wide alert receivers and the analytics services.

</div>

</div>
