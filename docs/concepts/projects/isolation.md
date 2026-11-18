# Project and User Isolation

Hopsworks keeps work apart at two levels.
A **project** is a sandbox for a team: its data, models and services belong to its members, and people outside the project reach them only when a Data owner shares them.
Inside a project, members share the project's datasets according to their role, and each member also has a **home directory** that no other member can open.

--8<-- "concepts/projects/isolation/two-levels.html"

## At a glance

| What | Inside the project | From other projects |
| --- | --- | --- |
| Datasets, models and the feature store | Members, as their role and the dataset's permission allow | Only when shared with their project |
| Home directories | Only the member it belongs to | Never |

## Project sandbox { #project-sandbox }

A project groups everything a team needs to build an AI system: feature groups, training data, models, deployments, jobs, notebooks and files.
The sandbox makes sure that all of it stays inside the project.

### Membership opens the project

You reach a project's resources only as a member of the project.
The UI, the REST API and the Python client all check your membership first, and refuse the request if you are not a member.
Once you are in, your role decides what you can do, see [the project roles][how-to-manage-members-to-a-project].
Platform administrators manage projects from the administration pages, which have their own access rules.

### One identity per project

When you join a project, Hopsworks gives you a separate identity in that project.
Everything you start in the project runs with it, from notebooks and jobs to the terminal, and the files you create there belong to it.

If you are a member of two projects, you have two separate identities.
Being a member of both does not let a notebook or job in one project read the files of the other: those files must first be shared with the project it runs in.

### Files and datasets

Each project has its own directory in HopsFS, `/Projects/<project>`.
The directories directly under it are the project's datasets.
Nobody outside the project can read or write a dataset unless it is shared with their project.

Inside the project, each dataset has a permission that decides what each role can do with its files:

| Dataset permission | Data owners | Data scientists | Observers |
| --- | --- | --- | --- |
| Editable by all | Read and write | Read and write | Read |
| Editable by owners | Read and write | Read | Read |
| Read only | Read | Read | Read |

The datasets Hopsworks creates for you, such as `Resources`, `Jupyter`, `Logs` and `Models`, are editable by all.
The `Users` dataset is the exception, with rules of its own, see [User home directories][user-home-directories].
The feature store is editable by owners: Data scientists read its files, and Data owners write them.
Members with the Feature store restricted role get no access to the feature store's files, and a [custom role][custom-project-roles] has the file access of the role it is based on.

Data owners choose the permission of the datasets they create, and can change it later.
The permissions of the datasets Hopsworks creates are fixed.

### Compute and services

Each project gets its own Kubernetes namespace, and the notebooks, jobs, terminals and model deployments of the project run in it.
A network policy stops pods in other project namespaces from opening connections to the pods of your project.
It is on by default, and platform administrators configure it when they install Hopsworks.

The other services keep a separate space per project as well:

- The offline and online feature stores are databases of their own for each project.
- A Kafka topic belongs to the project that created it.
- OpenSearch indexes, including the vector index, are kept per project.
- A Trino catalog belongs either to the project or, for a [private catalog][private-catalogs], to the user who created it.
- A secret is either private to you or visible to the members of one project.

### Sharing across projects { #sharing-across-projects }

The only way across the project boundary is a share a Data owner creates on purpose:

- **Share a dataset** with another project, read-only or editable, see [Sharing A Dataset][sharing-a-dataset].
- **Share the feature store** with another project, always read-only, see [Sharing the entire feature store][sharing-the-entire-feature-store].
- **Publish a dataset** to the whole cluster, which makes it read-only and lets any project import it.

The members of the receiving project get access as soon as the share is created, as far as their role allows, and so does anyone who joins that project later.
Members with the Feature store restricted role do not get access to shared feature stores or feature groups.
Revoking the share removes the access again.
[Data Storage and Sharing][data-storage-and-sharing] shows how shares look across projects.

## User home directories { #user-home-directories }

A project is shared by a team, but some files belong to one person: notebooks in progress, an SSH key, the settings and logins of coding agents, the credentials of a data source.
Since Hopsworks 5.0, every member has a private home directory in each project for these.

### Where to find it

Your home directory is `/Projects/<project>/Users/<username>`, in the project's `Users` dataset, for example `/Projects/fraud_detection/Users/alice`.

- In the file browser, open the `Users` dataset: you see your own home directory, and not those of other members.
- In a [terminal][terminal], your home directory is mounted at `/hopsfs/Users/<username>`, and the shell starts there.
- In the Python client, [`Project.home_path`][hopsworks_common.project.Project.home_path] returns its path in HopsFS.

```python
import hopsworks


project = hopsworks.login()

# For example /Projects/fraud_detection/Users/alice
print(project.home_path)
```

Hopsworks also uses your home directory as the default place for your own work.
Jupyter, Git and the web terminal start there.
Coding agents keep their settings and logins in `.claude` and `.codex`, and read the instructions Hopsworks writes into `AGENTS.md`.
Your `.ssh` directory and your `.bashrc` live there too.

### Who can open it

Only you.
Other members, the Data owners and the project owner included, cannot list, read, change, move or delete anything in your home directory.
This holds everywhere: in the file browser, the REST API, the Python client and search, and in the notebooks, jobs and terminals other members run.

The `Users` dataset is managed by Hopsworks:

- Hopsworks creates a home directory when a member joins and hands it over or deletes it when they leave.
  Nobody can rename or delete one directly, or create anything next to the home directories.
- The `Users` dataset cannot be shared with another project or published to the cluster.

!!! tip "Sharing a file with your team"
    To give teammates a file from your home directory, copy it into a project dataset such as `Resources`.

### When it is created

- The project owner's home directory is created with the project.
- A member's home directory is created when they join the project.
  The files Hopsworks prepares in it, for coding agents and the shell, follow in the background within moments.
- Service accounts, such as the ones Hopsworks adds for the online feature store and model serving, do not get one.
- Projects created before Hopsworks 5.0 get the `Users` dataset and a home directory for every member automatically after the upgrade.

### When a member leaves

Removing a member hands their home directory, with everything in it, to a Data owner of the project, or deletes it if you ask for that.
The removed member loses access to it, as they do to the rest of the project.
The Data owner who takes it over finds it in the `Users` dataset under the removed member's name, next to their own, and from then on it is private to them.
If the removed member joins again later, they get a new home directory, and the files they left stay with the Data owner who took them over.
[What happens to a removed member's files][what-happens-to-a-removed-members-files] describes the hand-over.

### Good to know

- Files in home directories count towards the storage quota of the project.
- Home directories keep the members of a project apart, but not from the platform itself: Hopsworks creates and maintains them, and an operator with administrative access to HopsFS can reach them.
  Keep passwords and tokens in [secrets][how-to-create-a-secret] rather than in files.
