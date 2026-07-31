# Versioning

Hopsworks versions the ML assets that make up an AI system, so that a model in production is reproducible and clients are protected from breaking changes.
Feature groups, feature views, training data, and models are versioned; deployments are the one asset that is not.

## Feature group schema versioning

The schema of feature groups is versioned.
If you make a breaking change to the schema of a feature group, you need to increment the version of the feature group, and then backfill the new feature group.
A breaking schema change is when you:

- drop a column from the schema
- add a new feature without any default value for the new feature
- change how a feature is computed, such that, for training models, the data for the old feature is not compatible with the data for the new feature.
  For example, if you have an embedding as a feature and change the algorithm to compute that embedding, you probably should not mix feature values computed with the old embedding model with feature values computed with the new embedding model.

<img src="../../../../assets/images/concepts/fs/schema-versioning.svg">

## Feature group data versioning

Data versioning of a feature group tracks updates to the feature group, so that you can recover the state of the feature group at a given point-in-time in the past.

<img src="../../../../assets/images/concepts/fs/data-versioning.svg">

There are two points in time you can travel back to, and they answer different questions.
As-of ingestion time reads the data as it had been written by a given moment, which gives reproducible training data.
As-of event time reads the data as it was true in the world at a given moment, which gives point-in-time correct training data with no future leakage.

## Feature view and training data versioning

Feature views are interfaces, and if there is a change in the interface (the types of the features, the transformations applied to the features), then you need to change the version, to prevent breaking existing clients.

Training datasets are associated with a specific feature view version, and each training dataset also has its own version number.
For example, online transformation functions often need training data statistics (e.g., normalizing a numerical feature requires you to divide the feature value by the mean value for that feature in the training dataset).
As many training datasets can be created from a feature view, when you initialize the feature view you need to tell it which version of the training data to use: `feature_view.init(1)` means use version 1 of the training data for this feature view.

<figure class="hops-diagram">
<svg viewBox="0 0 1000 344" role="img" aria-label="Grid of feature view versions as columns and training dataset versions as rows. Each cell holds the model trained on that combination. Feature view version 1 has training datasets 1 and 2, feature view version 2 restarts its training dataset numbering at 1, and one cell has no training dataset yet." xmlns="http://www.w3.org/2000/svg">
  <rect class="d-box-own" x="300" y="36" width="330" height="56" rx="8"/>
  <text class="d-t" x="465" y="60" text-anchor="middle">Feature view v1</text>
  <text class="d-t d-sub" x="465" y="79" text-anchor="middle">schema and transformations as first published</text>
  <rect class="d-box-own" x="650" y="36" width="330" height="56" rx="8"/>
  <text class="d-t" x="815" y="60" text-anchor="middle">Feature view v2</text>
  <text class="d-t d-sub" x="815" y="79" text-anchor="middle">breaking change to the interface</text>

  <text class="d-t" x="20" y="152">Training dataset v1</text>
  <text class="d-t" x="20" y="236">Training dataset v2</text>

  <rect class="d-box" x="300" y="112" width="330" height="72" rx="8"/>
  <text class="d-t" x="465" y="145" text-anchor="middle">fraud_model v1</text>
  <text class="d-t d-sub" x="465" y="164" text-anchor="middle">first model in production</text>
  <rect class="d-box" x="650" y="112" width="330" height="72" rx="8"/>
  <text class="d-t" x="815" y="145" text-anchor="middle">fraud_model v3</text>
  <text class="d-t d-sub" x="815" y="164" text-anchor="middle">retrained after the interface change</text>

  <rect class="d-box" x="300" y="196" width="330" height="72" rx="8"/>
  <text class="d-t" x="465" y="229" text-anchor="middle">fraud_model v2</text>
  <text class="d-t d-sub" x="465" y="248" text-anchor="middle">retrained on a later time range</text>
  <g opacity=".5">
    <rect class="d-box" x="650" y="196" width="330" height="72" rx="8" stroke-dasharray="5 4"/>
    <text class="d-t d-sub" x="815" y="238" text-anchor="middle">no training dataset created yet</text>
  </g>

  <rect class="d-band" x="16" y="286" width="964" height="44" rx="10"/>
  <text class="d-t" x="40" y="313">A model is pinned to one feature view version and one training dataset version, and reads the statistics of that training dataset when it serves.</text>
</svg>
</figure>

## Models and deployments

A model has its own version in the model registry.
A deployment, however, is not versioned: it is the one mutable asset.
A new deployment gets a new name, upgrades and rollbacks are done with blue/green deployments, and clients depend on the [deployment API](../../mlops/serving.md), not on a deployment version number.
A model deployment is also tightly coupled to the versioned feature views that supply its pre-computed features, so versioning the model alone is not enough.
