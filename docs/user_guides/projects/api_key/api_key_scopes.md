# API Key Scopes

Every API key carries a set of scopes.
A scope unlocks a group of REST endpoints; a request made with a key that lacks the scope an endpoint requires is rejected before it reaches the endpoint.
Scopes are chosen when a key is created and can be changed later from the key's edit page, without regenerating the secret.
See [How To Create An API Key][how-to-create-an-api-key] for the UI walkthrough.

A scope never grants more than the account itself may do.
Endpoints still check the caller's role in the project, so a Data Scientist's key with the `FEATURESTORE` scope cannot do what a Data Owner's key with the same scope can.

## Scope reference

| Scope | Grants access to |
| --- | --- |
| `FEATURESTORE` | Feature stores and everything inside them: feature groups, feature views, training datasets, data sources and storage connectors, transformation functions, statistics, data validation, feature monitoring, tags, keywords, provenance and feature store search. Also Hopsworks actions and the tag schema catalogue; creating or deleting a tag schema additionally requires the `HOPS_ADMIN` role. |
| `PROJECT` | Project management: list, create, update and delete projects; read project information and client credentials; manage members; project alerts, receivers, routes and silences; cloud role mappings; the operation log; tutorials and product news. |
| `JOB` | Jobs and executions: create, update, schedule, start, stop and delete jobs; read execution logs; default job configurations; job alerts and tags; Python apps; expectation suites and validation reports. |
| `DATASET_VIEW` | Read access to project datasets: list datasets, browse and download files, and use global, project and dataset search. |
| `DATASET_CREATE` | Create datasets and directories, upload files, and copy, move, zip or unzip them. |
| `DATASET_DELETE` | Delete datasets, directories and files. |
| `MODELREGISTRY` | Model registries and models: register, update and delete models; model tags and provenance; Hugging Face imports; generated deployment configurations. |
| `SERVING` | Model deployments: create, start, stop and delete deployments; read deployment logs; send inference requests; deployment tags; OpenTelemetry traces and metrics. |
| `KAFKA` | The project's Kafka topics and schema registry: topics, subjects, schema versions and compatibility settings. Also accepted, as an alternative to `FEATURESTORE` or `PROJECT`, by the few read endpoints a Kafka or OnlineFS client needs, such as listing projects and feature stores. |
| `PYTHON_LIBRARIES` | Python environments: list, create and delete environments; install and uninstall pip, conda and npm packages; search package indexes; environment build commands, history and conflicts. |
| `GIT` | Git repositories in the project: clone, branches, commits, remotes, repository actions and their executions, and the account's Git provider credentials. |
| `TRINO` | The Trino query engine: submit and cancel SQL statements, read query, worker and cluster status, and manage Trino catalogs. |
| `SUPERSET` | Superset dashboards: log in to Superset, list dashboards, create permalinks, make a dashboard public or share it with another project, and delete dashboards. |
| `TERMINAL` | The web terminal: start, extend, stop and inspect terminal sessions, and mint the proxy tokens used to attach to them. |
| `MOUNTABLE_SECRET` | The project's mountable secrets: named bundles of credential files (Oracle wallets, JKS keystores, service account JSON) that a service mounts read-only. Create, list and delete bundles. Contents are never returned. Requires the Data Owner role. |
| `USER` | The account itself: profile, secrets, account environment variables, AI provider settings, and API keys. A key with this scope can create, edit and delete API keys, including keys carrying any other scope the account is allowed to hold, so treat it as equivalent to all of them. |
| `ADMIN` | Cluster administration: the admin API (configuration variables, backups, projects, users, Trino, TTL purge, coding agent configuration, cloud role mappings, search reindexing, the operation log), compute resources and the UI theme. Privileged. |
| `ADMINISTER_USERS` | User administration in the admin API: list, accept, reject, block, modify and delete users, change roles, reset passwords and sync remote groups. Privileged. |
| `ADMINISTER_USERS_REGISTER` | Only the user registration endpoint of the admin API. Privileged. |
| `AUTH` | The JWT service: issue, renew and invalidate tokens and remove signing keys. Privileged, and also available to accounts in the `AGENT` group. |
| `KUBE` | Reserved. No REST endpoint currently accepts it. |
| `SINK` | Reserved for feature groups that ingest from a data source through a DLT sink. No REST endpoint currently accepts it. |

## Privileged scopes

`ADMIN`, `ADMINISTER_USERS`, `ADMINISTER_USERS_REGISTER` and `AUTH` are privileged.
Only accounts with the `HOPS_ADMIN` role can create keys carrying them, because the endpoints they unlock act on the whole cluster rather than on a project the caller is a member of.

## Scopes an account can select

The set of scopes offered when creating or editing a key depends on the account's role.

| Account role | Selectable scopes |
| --- | --- |
| `HOPS_ADMIN` | All scopes. |
| `HOPS_USER` | All unprivileged scopes. |
| `AGENT` | All unprivileged scopes plus `AUTH`. |
| `HOPS_SERVICE_USER` | All unprivileged scopes except `GIT` and `KUBE`. |

The API key form preselects `FEATURESTORE`, `PROJECT`, `JOB`, `DATASET_VIEW`, `DATASET_CREATE`, `DATASET_DELETE`, `KAFKA`, `SERVING`, `MODELREGISTRY`, `USER` and `PYTHON_LIBRARIES`.
Deselect what the key's consumer does not need.

## Scopes of a key created by hops setup

`hops setup` creates its key through the browser token flow rather than the API key form, so the scopes are not chosen interactively.
The key carries every scope a `hops` subcommand needs: `FEATURESTORE`, `PROJECT`, `JOB`, `DATASET_VIEW`, `DATASET_CREATE`, `DATASET_DELETE`, `MODELREGISTRY`, `SERVING`, `USER`, `KAFKA`, `TERMINAL`, `PYTHON_LIBRARIES`, `GIT`, `TRINO` and `SUPERSET`.
A key created by an older release lacks the last six; edit it in the UI to add them, or run `hops setup --force` to mint a new one.

## Scope errors

A request made with a key that lacks the required scope fails with HTTP 403 and error code 320004.
The message names the scope the endpoint accepts.

```json
{
  "errorCode": 320004,
  "usrMsg": "No valid scope found for this invocation. Valid scope for this invocation is: [PYTHON_LIBRARIES]",
  "errorMsg": "No valid scope found for this invocation"
}
```

Add the named scope to the key from the _API_ section of _Account Settings_, or create a new key that has it.
