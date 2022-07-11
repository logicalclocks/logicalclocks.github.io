Every project in Hopsworks has its own private assets:

 * a Feature Store (including both Online and Offline Stores)
 * a Filesystem subtree (all directory and files under /Projects/<project_name>/)
 * a Model Registry
 * Model Deployments
 * Kafka topics
 * OpenSearch indexes (including KNN indexes - the vector DB)
 * a Hive Database

Access control to these assets is controlled using project membership ACLs (access-control lists). Users in a project who have a *Data Owner* role have read/write access to these assets.  Users in a project who have a *Data Scientist* role have mostly read-only access to these assets, with the exception of the ability to write to well-known directories (Resources, Jupyter, Logs). 

However, it is often desirable to share assets between projects, with read-only, read/write privileges, and to restrict the privileges to specific role (e.g., Data Owners) in the target project. In Hopsworks, you can explicity share assets between projects without copying the assets. Sharing is managed by ACLs in Hopsworks, see example below:
<img src="../../../assets/images/concepts/projects/projects-sharing.svg">

