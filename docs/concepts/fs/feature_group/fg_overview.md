# Features and Feature Groups

As a programmer, you can consider a feature, in machine learning, to be a variable associated with some entity that contains a value that is useful for helping train a model to solve a prediction problem.
That is, the feature is just a variable with predictive power for a machine learning problem, or task.

A feature group is a table of features.
Each feature group has a primary key, and optionally an event_time column (indicating when the features in that row were observed), a partition key, and foreign keys that point to the primary keys of other feature groups.
These are index columns, not features: they identify and join rows, and they are excluded when you select the features for a model.
A feature group stores untransformed feature data, so the same feature can be reused across models that each transform it differently.

??? note "Partitioning"
    The partition key determines how the feature group rows are laid out on disk, so that queries using the partition key read only the data they need.
    For example, if the partition key is the day and you have hundreds of days of data, a query for a given day or a range of days reads only those days from disk.

<figure class="hops-diagram">
<svg viewBox="0 0 1000 260" role="img" aria-label="A feature group is a table whose primary key, event_time and partition_key are index columns while temperature and rainfall are the reusable features, with a single row highlighted." xmlns="http://www.w3.org/2000/svg">
  <text class="d-t" x="460" y="28" text-anchor="middle">Columns</text>
  <path class="d-flow" d="M44 60 C44 50 49 50 54 50 H452 C458 50 458 42 460 42 C462 42 462 50 468 50 H866 C871 50 876 50 876 60"/>
  <text class="d-sub" x="124" y="82" text-anchor="middle">Primary Key</text>
  <text class="d-sub" x="292" y="82" text-anchor="middle">event_time</text>
  <text class="d-sub" x="460" y="82" text-anchor="middle">partition_key</text>
  <text class="d-sub" x="628" y="82" text-anchor="middle">Feature</text>
  <text class="d-sub" x="796" y="82" text-anchor="middle">Feature</text>
  <rect class="d-box" x="44" y="92" width="160" height="34" rx="6"/>
  <rect class="d-box" x="212" y="92" width="160" height="34" rx="6"/>
  <rect class="d-box" x="380" y="92" width="160" height="34" rx="6"/>
  <rect class="d-box-own" x="548" y="92" width="160" height="34" rx="6"/>
  <rect class="d-box-own" x="716" y="92" width="160" height="34" rx="6"/>
  <text class="d-t" x="124" y="114" text-anchor="middle">location_id</text>
  <text class="d-t" x="292" y="114" text-anchor="middle">event_time</text>
  <text class="d-t" x="460" y="114" text-anchor="middle">day</text>
  <text class="d-t" x="628" y="114" text-anchor="middle">temperature</text>
  <text class="d-t" x="796" y="114" text-anchor="middle">rainfall</text>
  <rect class="d-box" x="44" y="132" width="160" height="32" rx="6"/>
  <rect class="d-box" x="212" y="132" width="160" height="32" rx="6"/>
  <rect class="d-box" x="380" y="132" width="160" height="32" rx="6"/>
  <rect class="d-box" x="548" y="132" width="160" height="32" rx="6"/>
  <rect class="d-box" x="716" y="132" width="160" height="32" rx="6"/>
  <text class="d-sub" x="124" y="152" text-anchor="middle">9844-3333</text>
  <text class="d-sub" x="292" y="152" text-anchor="middle">2022-06-01 13:11</text>
  <text class="d-sub" x="460" y="152" text-anchor="middle">2022-06-01</text>
  <text class="d-sub" x="628" y="152" text-anchor="middle">12.45</text>
  <text class="d-sub" x="796" y="152" text-anchor="middle">44</text>
  <rect class="d-box" x="44" y="168" width="160" height="32" rx="6"/>
  <rect class="d-box" x="212" y="168" width="160" height="32" rx="6"/>
  <rect class="d-box" x="380" y="168" width="160" height="32" rx="6"/>
  <rect class="d-box" x="548" y="168" width="160" height="32" rx="6"/>
  <rect class="d-box" x="716" y="168" width="160" height="32" rx="6"/>
  <text class="d-sub" x="124" y="188" text-anchor="middle">6783-9832</text>
  <text class="d-sub" x="292" y="188" text-anchor="middle">2022-06-01 09:14</text>
  <text class="d-sub" x="460" y="188" text-anchor="middle">2022-06-01</text>
  <text class="d-sub" x="628" y="188" text-anchor="middle">22.84</text>
  <text class="d-sub" x="796" y="188" text-anchor="middle">5</text>
  <rect class="d-box" x="44" y="204" width="160" height="32" rx="6"/>
  <rect class="d-box" x="212" y="204" width="160" height="32" rx="6"/>
  <rect class="d-box" x="380" y="204" width="160" height="32" rx="6"/>
  <rect class="d-box" x="548" y="204" width="160" height="32" rx="6"/>
  <rect class="d-box" x="716" y="204" width="160" height="32" rx="6"/>
  <text class="d-sub" x="124" y="224" text-anchor="middle">7538-1231</text>
  <text class="d-sub" x="292" y="224" text-anchor="middle">2022-06-01 06:34</text>
  <text class="d-sub" x="460" y="224" text-anchor="middle">2022-06-01</text>
  <text class="d-sub" x="628" y="224" text-anchor="middle">31.04</text>
  <text class="d-sub" x="796" y="224" text-anchor="middle">2</text>
  <rect class="d-flow" x="40" y="201" width="840" height="38" rx="8" fill="none"/>
  <text class="d-t" x="936" y="224" text-anchor="middle">Row</text>
</svg>
</figure>

## Online and offline Storage

Feature groups can be stored in a low-latency "online" database and/or in low cost, high throughput "offline" storage, typically a data lake or data warehouse.
A feature group with an embedding column can also have a vector index, for similarity search from inference pipelines and agents.

<figure class="hops-diagram">
<svg viewBox="0 0 1000 380" role="img" aria-label="The feature_group_v1 feature group is served online as the latest feature values and stored offline as the historical feature values." xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="fs2-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/></marker></defs>
  <rect class="d-box-own" x="30" y="155" width="190" height="60" rx="8"/>
  <text class="d-t" x="125" y="190" text-anchor="middle">feature_group_v1</text>
  <path class="d-flow" d="M220 175 C300 150 350 100 438 95" marker-end="url(#fs2-arrow)"/>
  <path class="d-flow" d="M220 195 C300 220 350 285 438 290" marker-end="url(#fs2-arrow)"/>
  <text class="d-sub" x="330" y="118" text-anchor="middle">online</text>
  <text class="d-sub" x="330" y="256" text-anchor="middle">offline</text>
  <text class="d-t" x="447" y="34" text-anchor="start">feature_group_v1</text>
  <text class="d-sub" x="600" y="34" text-anchor="start">latest feature values</text>
  <rect class="d-box-own" x="447" y="44" width="160" height="30" rx="6"/>
  <rect class="d-box-own" x="620" y="44" width="160" height="30" rx="6"/>
  <rect class="d-box-own" x="793" y="44" width="160" height="30" rx="6"/>
  <text class="d-t" x="527" y="64" text-anchor="middle">location_id</text>
  <text class="d-t" x="700" y="64" text-anchor="middle">temperature</text>
  <text class="d-t" x="873" y="64" text-anchor="middle">rainfall</text>
  <rect class="d-box" x="447" y="78" width="160" height="30" rx="6"/>
  <rect class="d-box" x="620" y="78" width="160" height="30" rx="6"/>
  <rect class="d-box" x="793" y="78" width="160" height="30" rx="6"/>
  <text class="d-sub" x="527" y="98" text-anchor="middle">9844-3333</text>
  <text class="d-sub" x="700" y="98" text-anchor="middle">12.45</text>
  <text class="d-sub" x="873" y="98" text-anchor="middle">44</text>
  <rect class="d-box" x="447" y="112" width="160" height="30" rx="6"/>
  <rect class="d-box" x="620" y="112" width="160" height="30" rx="6"/>
  <rect class="d-box" x="793" y="112" width="160" height="30" rx="6"/>
  <text class="d-sub" x="527" y="132" text-anchor="middle">...</text>
  <text class="d-sub" x="700" y="132" text-anchor="middle">...</text>
  <text class="d-sub" x="873" y="132" text-anchor="middle">...</text>
  <text class="d-t" x="441" y="180" text-anchor="start">feature_group_v1</text>
  <text class="d-sub" x="595" y="180" text-anchor="start">historical feature values</text>
  <rect class="d-box-own" x="441" y="190" width="122" height="30" rx="6"/>
  <rect class="d-box-own" x="573" y="190" width="122" height="30" rx="6"/>
  <rect class="d-box-own" x="705" y="190" width="122" height="30" rx="6"/>
  <rect class="d-box-own" x="837" y="190" width="122" height="30" rx="6"/>
  <text class="d-t" x="502" y="210" text-anchor="middle">location_id</text>
  <text class="d-t" x="634" y="210" text-anchor="middle">event_time</text>
  <text class="d-t" x="766" y="210" text-anchor="middle">temperature</text>
  <text class="d-t" x="898" y="210" text-anchor="middle">rainfall</text>
  <rect class="d-box" x="441" y="224" width="122" height="30" rx="6"/>
  <rect class="d-box" x="573" y="224" width="122" height="30" rx="6"/>
  <rect class="d-box" x="705" y="224" width="122" height="30" rx="6"/>
  <rect class="d-box" x="837" y="224" width="122" height="30" rx="6"/>
  <text class="d-sub" x="502" y="244" text-anchor="middle">9844-3333</text>
  <text class="d-sub" x="634" y="244" text-anchor="middle">2022-01-01</text>
  <text class="d-sub" x="766" y="244" text-anchor="middle">12.45</text>
  <text class="d-sub" x="898" y="244" text-anchor="middle">44</text>
  <rect class="d-box" x="441" y="258" width="122" height="30" rx="6"/>
  <rect class="d-box" x="573" y="258" width="122" height="30" rx="6"/>
  <rect class="d-box" x="705" y="258" width="122" height="30" rx="6"/>
  <rect class="d-box" x="837" y="258" width="122" height="30" rx="6"/>
  <text class="d-sub" x="502" y="278" text-anchor="middle">9844-3333</text>
  <text class="d-sub" x="634" y="278" text-anchor="middle">2021-01-01</text>
  <text class="d-sub" x="766" y="278" text-anchor="middle">14.45</text>
  <text class="d-sub" x="898" y="278" text-anchor="middle">34</text>
  <rect class="d-box" x="441" y="292" width="122" height="30" rx="6"/>
  <rect class="d-box" x="573" y="292" width="122" height="30" rx="6"/>
  <rect class="d-box" x="705" y="292" width="122" height="30" rx="6"/>
  <rect class="d-box" x="837" y="292" width="122" height="30" rx="6"/>
  <text class="d-sub" x="502" y="312" text-anchor="middle">9844-3333</text>
  <text class="d-sub" x="634" y="312" text-anchor="middle">2020-01-01</text>
  <text class="d-sub" x="766" y="312" text-anchor="middle">13.12</text>
  <text class="d-sub" x="898" y="312" text-anchor="middle">55</text>
  <rect class="d-box" x="441" y="326" width="122" height="30" rx="6"/>
  <rect class="d-box" x="573" y="326" width="122" height="30" rx="6"/>
  <rect class="d-box" x="705" y="326" width="122" height="30" rx="6"/>
  <rect class="d-box" x="837" y="326" width="122" height="30" rx="6"/>
  <text class="d-sub" x="502" y="346" text-anchor="middle">...</text>
  <text class="d-sub" x="634" y="346" text-anchor="middle">...</text>
  <text class="d-sub" x="766" y="346" text-anchor="middle">...</text>
  <text class="d-sub" x="898" y="346" text-anchor="middle">...</text>
</svg>
</figure>

### Online Storage

By default, the online store keeps only the latest values of features for a feature group.
It serves those precomputed features to models at runtime, and is backed by [RonDB](https://www.rondb.com), a low latency, high throughput, high availability data store.
By including an event_time column and a time-to-live (TTL), the online store can instead keep many rows per entity, which is what shift-right on-demand aggregations need.

### Offline Storage

The offline store stores the historical values of features for a feature group so that it may store much more data than the online store.
Offline feature groups are used, typically, to create training data for models, but also to retrieve data for batch scoring of models.

In most cases, offline data is stored in Hopsworks, but through the implementation of data sources, it can reside in an external file system.
The externally stored data can be managed by Hopsworks by defining ordinary feature groups or it can be used for reading only by defining [External Feature Group](external_fg.md).
