# Roles and Permissions { #semantic-roles }

A member's project role decides what they can do with the project's semantic projects.
The built-in roles are Data owner, Data scientist, Observer and Feature store restricted; a [custom project role][custom-project-roles] is a Data owner or Data scientist with some permissions removed.

## What each role can do { #semantic-roles-actions }

| Action | Data owner | Data scientist | Observer | Permission |
| --- | --- | --- | --- | --- |
| List semantic projects, open their overview, builds, metrics, saved queries, dimensions and tags, and read the definition files | Yes | Yes | Yes | _View & query_ |
| [Query metrics][semantic-query-metrics] from the UI, Python, the CLI, [dbt clients][semantic-connect-clients] and [BI tools][semantic-bi-tools] | Yes | Yes | Refused by Trino | _View & query_ |
| Read the [connection details][semantic-connect-details] | Yes | Yes | Yes | _View & query_ |
| Read the [query history][semantic-query-history] | Every member's | Their own | Their own | _View & query_ |
| [Register][semantic-builds-register] a semantic project and change its root path, format and deployment mode | Yes | Yes | No | _Create & edit_ |
| [Compile][semantic-builds-compile] and promote builds | Yes | Yes | No | _Create & edit_ |
| Save and delete definition files in the [editor][semantic-editor] | Yes | Yes | No | _Create & edit_ |
| Create [Superset dashboards][semantic-superset-dashboards] from metrics | Yes | Yes | No | _Create & edit_ |
| Delete a semantic project, whoever owns it | Yes | Yes | No | _Delete_ |
| [Transfer ownership][semantic-builds-owner-transfer] of a semantic project | Yes | No | No | _Create & edit_ |
| [Run an export now][semantic-exports-run] | Yes | No | No | _Run exports_, with _Jobs_ |
| Own a semantic project whose [exports][semantic-exports] run | Yes | No | No | _Run exports_, with _Jobs_ |
| Attach and remove [tags][semantic-tags] | Yes | Yes | No | _Tags_ |

- The Permission column names the _Semantic layer_ permission of a [custom project role][custom-project-roles] that the action needs, except _Jobs_ and _Tags_, which are permissions of their own.
  A custom role that removes the permission is refused with 403, in the UI and over REST, and the UI hides the buttons for it.
- An Observer reads the semantic project, but their metric queries fail, since Trino gives an Observer no access to the project's feature groups.
  Observers have no Superset account, so they get no [semantic connection][semantic-superset-connections] in Superset.
- Feature store restricted members are refused every semantic layer request with 403 `SEMANTIC_LAYER_FORBIDDEN`, since a semantic project reads every feature of a feature group.
- A metric query runs on Trino as the member who asks, so each member sees only the rows and columns their own Trino rules allow, see [Who a query runs as][semantic-overview-identity].

## Owner { #semantic-roles-owner }

The member who registers a semantic project becomes its owner, whatever their role.
The [export][semantic-exports] jobs run as the owner, who must be a Data owner whose role allows _Semantic layer: Run exports_.
A semantic project a Data scientist registers therefore has exports without jobs, with the status `OWNER_NOT_DATA_OWNER`, until a Data owner [transfers it][semantic-builds-owner-transfer] to a Data owner.
Everything else a semantic project does works the same whoever owns it.

## Access to the definition files { #semantic-roles-hopsfs }

Hopsworks reads and writes the definition files as the member who asks, so HopsFS permissions apply on top of the project role, as in the file browser.

| Request | Without HopsFS read access to the root path | Without HopsFS write access |
| --- | --- | --- |
| Compile | 403 `SEMANTIC_LAYER_FORBIDDEN`, `Cannot read the root path ...`; no build is recorded, and the serving build stays as it is | Not needed |
| Open the editor | 403 `SEMANTIC_LAYER_FORBIDDEN`, `Cannot read the files under ...` | The editor is [read only][semantic-editor-read-only] |
| Query metrics, list metrics and saved queries | Not needed: they come from the served build | Not needed |

A member's home folder under `Users/` is readable only by that member.
Keep definitions that several members change in a shared dataset, such as `Resources`, or in a [git repository][semantic-init-repo-new] cloned in the project, so every Data owner and Data scientist can compile them.

## API keys { #semantic-roles-api-keys }

An API key acts with its user's role, and needs:

| Scope | For |
| --- | --- |
| `FEATURESTORE` | Semantic projects, builds, definition files, tags, exports and the query history. |
| `TRINO` | Everything the semantic gateway answers, from listing metrics to running a query, since the gateway connects to Trino as the key's user. |
| `JOB` | Running an export now. |
