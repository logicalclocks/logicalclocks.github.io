Every project in Hopsworks has its own private assets:

- a Feature Store (including both Online and Offline Stores)
- a Filesystem subtree (all directory and files under /Projects/<project_name>/)
- a private home directory for each member, in the `Users` dataset
- a Model Registry
- Model Deployments
- Kafka topics
- OpenSearch indexes (including KNN indexes - the vector DB)
- a Hive Database

Access control to these assets is controlled using project membership ACLs (access-control lists).
Users in a project who have a *Data Owner* role have read/write access to these assets.
For the files in the project's datasets, users who have a *Data Scientist* role can write to the datasets that are editable by all, which include the datasets Hopsworks creates such as `Resources`, `Jupyter`, `Logs` and `Models`, and can read the feature store and the datasets that are editable by owners.
A member's home directory is open to that member only.
[Project and User Isolation][project-and-user-isolation] explains the dataset permissions and the home directories in detail.

However, it is often desirable to share assets between projects, with read-only, read/write privileges, and to restrict the privileges to specific role (e.g., Data Owners) in the target project.
In Hopsworks, you can explicitly share assets between projects without copying the assets.
Sharing is managed by ACLs in Hopsworks, see example below:
<img src="../../../assets/images/concepts/projects/projects-sharing.svg">
