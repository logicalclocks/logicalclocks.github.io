Hopsworks provides project-level multi-tenancy, a data mesh enabling technology. Think of it as a Github repository for your teams and ML assets. More specifically, a project is a sandbox for team members, ML assets (features, training data, models, vector database, model deployments), and optionally feature pipelines and training pipelines. The ML assets can only be accessed by project members, and there is role-based access control (RBAC) for project members within a project.

<img src="../../../assets/images/concepts/projects/projects-simple.svg">

## Dev/Staging/Prod for Data 
Projects enable you to define devlopment, staging, and even production projects on the same cluster. Often, companies deploy production projects on dedicated clusters, but development projects and staging projects on a shared cluster. This way, projects can be easily used to implement CI/CD workflows.


## Data Mesh of Feature Stores
Projects enable you to move beyond the traditional dev/staging/prod ownership model for data. Different teams or lines of business can have their own private feature stores, you can mix them with a group-wide feature store, and feature stores can be securely shared between teams/organizations. Effectively, you can have decentralized ownership of feature stores, with domain-specific projects, and each project managing its own feature pipelines. Hopsworks provides data/feature sharing support between these self-service projects. 


## Audit Logs with REST API
Hopsworks stores audit logs for all calls on its REST API in its file system, HopsFS. The audit log can be used to analyze the historical usage of services by users.


