You can setup traditional development, staging, and production environment in Hopsworks using Projects.
A project enables you provide access control for the different environments - just like a GitHub repository, owners of projects can add and remove members of projects and assign different roles to project members - the "data owner" role can write to feature store, while a "data scientist" can only read from the feature store and create training data.


##Dev, Staging, Prod
You can create dev, staging, and prod projects - either on the same cluster, but mostly commonly, with production on its own cluster:

<img src="../../../assets/images/concepts/projects/dev-staging-prod.svg">

##Versioning

Hopsworks supports the versioning of ML assets, including:

* Feature Groups: the version of its schema - breaking schema changes require a new version and backfilling the new version;
* Feature Views:  the version of its schema, and breaking schema changes only require a new version;
* Models: the version of a model;
* Deployments: the version of the deployment of a model - a model with the same version can be found in >1 deployment.


##Pytest for feature logic and feature pipeline tests

Pytest and Great Expectations can be used for testing feature pipelines. Pytest is used to test feature logic and for end-to-end feature pipeline tests, while Great Expectations is used for data validation tests. 
Here, we can see how a feature pipeline test uses sample data to compute features and validate they have been written successfully, first to a development feature store, and then they can be pushed to a staging feature store, before finally being promoted to production.
<img src="../../../assets/images/concepts/projects/feature-pipeline-tests.svg">
