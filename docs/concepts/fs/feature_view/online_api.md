# Online API

The Feature View provides an Online API to return an individual feature vector, or a batch of feature vectors, containing the latest feature values.
To retrieve a feature vector, a client provides the feature view's serving keys.
The serving keys are the foreign keys of the feature view's label feature group; a feature view does not have a primary key of its own.
For example, if a feature view is built from the `customer_profile` and `customer_purchases` feature groups joined on `customer_id`, then `customer_id` is the serving key you provide to retrieve a feature vector.

## Feature Vectors

A feature vector is a row of features (without the primary key(s) and event timestamp):

<figure class="hops-diagram">
<svg viewBox="0 0 1000 340" role="img" aria-label="A feature vector is a single row whose cells (location_id, temperature, rainfall) each come from either the app session or the feature store." xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="fv-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/></marker></defs>
  <text class="d-t" x="500" y="40" text-anchor="middle">feature vector</text>
  <text class="d-t" x="233" y="76" text-anchor="middle">location_id</text>
  <text class="d-t" x="500" y="76" text-anchor="middle">temperature</text>
  <text class="d-t" x="767" y="76" text-anchor="middle">rainfall</text>
  <rect class="d-box" x="100" y="90" width="800" height="64" rx="8"/>
  <path class="d-flow" d="M367 90 V154"/>
  <path class="d-flow" d="M633 90 V154"/>
  <text class="d-t" x="233" y="128" text-anchor="middle">9844-3333</text>
  <text class="d-t" x="500" y="128" text-anchor="middle">12.45</text>
  <text class="d-t" x="767" y="128" text-anchor="middle">44</text>
  <path class="d-flow" d="M233 154 V228" marker-end="url(#fv-arrow)"/>
  <path class="d-flow" d="M500 154 V228" marker-end="url(#fv-arrow)"/>
  <path class="d-flow" d="M767 154 V228" marker-end="url(#fv-arrow)"/>
  <rect class="d-box-ext" x="123" y="230" width="220" height="80" rx="8"/>
  <text class="d-t" x="233" y="266" text-anchor="middle">Primary Key from</text>
  <text class="d-t" x="233" y="288" text-anchor="middle">app session</text>
  <rect class="d-box-own" x="390" y="230" width="220" height="80" rx="8"/>
  <text class="d-t" x="500" y="266" text-anchor="middle">From</text>
  <text class="d-t" x="500" y="288" text-anchor="middle">feature store</text>
  <rect class="d-box-own" x="657" y="230" width="220" height="80" rx="8"/>
  <text class="d-t" x="767" y="266" text-anchor="middle">From</text>
  <text class="d-t" x="767" y="288" text-anchor="middle">feature store</text>
</svg>
</figure>

It may be the case that for any given feature vector, not all features will come pre-engineered from the feature store.
Some features will be provided by the client (or at least the raw data to compute the feature will come from the client).
We call these 'passed' features and, similar to precomputed features from the feature store, they can also be transformed by the Hopsworks client in the method:

- feature_view.get_feature_vector(entry, passed_features={...})

When you call `get_feature_vector`, Hopsworks builds the vector in a fixed order:

1. retrieve the precomputed features from the online store using the serving keys,
2. merge in any passed features,
3. compute on-demand transformations (ODTs),
4. compute model-dependent transformations (MDTs),
5. drop the index and helper columns,
6. return the feature vector.

This ordering is the composition constraint: on-demand transformations run before model-dependent ones, which are always last, just before the model is called.
