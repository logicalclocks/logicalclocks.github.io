# Concepts

This section explains what Hopsworks is and why it is built the way it is.
It is reference and explanation, not step-by-step instructions.
For the how-to, see the [Guides](../user_guides/index.md).

## Start here

Read the [FTI Pipeline Architecture](fti.md) first.
It is the one idea the rest of this section builds on: every AI system decomposes into feature, training, and inference pipelines, connected through a feature store and a model registry.
Once you have that model, the other pages are the parts of it.

## Reading path

- [Hopsworks Platform](hopsworks.md): the components of the platform and how they fit together.
- [FTI Pipeline Architecture](fti.md): the architecture all AI systems share, and the four classes of AI system.
- **Feature Store**: how feature pipelines write feature data ([feature groups](fs/feature_group/fg_overview.md)) and how training and inference pipelines read it ([feature views](fs/feature_view/fv_overview.md)).
- **Projects**: the multi-tenant unit that owns your data and ML assets, with governance, sharing, and lineage.
- **MLOps**: training, the model registry, serving, and monitoring, the inference side of an AI system.
- **Development**: building and running pipelines inside and outside Hopsworks.

## How the section is organised

The Feature Store pages follow the write path then the read path: you write features to feature groups, and you read them through feature views.
The MLOps pages follow a model from training through registration, serving, and monitoring.
Projects and Development cut across both.
