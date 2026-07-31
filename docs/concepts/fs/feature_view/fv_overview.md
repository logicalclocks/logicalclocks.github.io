# Feature Views

A feature view is a logical view over (or interface to) a set of features that may come from different feature groups.
You create a feature view by selecting features, starting from a root feature group and following foreign keys to join in features from other feature groups.
When the feature view has a label for supervised learning, the root feature group is the label feature group, the one feature group that holds the labels.
Features are reachable by graph traversal: any feature group joined to the root can, in turn, have foreign keys to further feature groups whose features you can also select.
A feature view does not have a primary key of its own; it has serving keys, the foreign keys of its label feature group, which you provide to retrieve feature vectors.
In the illustration below, we can see that features are joined together from the two feature groups: seller_delivery_time_monthly and the seller_reviews_quarterly.
You can also see that features in the feature view inherit not only the feature type from their feature groups, but also whether they are the primary key and/or the event_time.
The image also includes transformation functions that are applied to individual features.
Transformation functions are a part of the feature types included in the feature view.
That is, a feature in a feature view is not only defined by its data type (int, string, etc) or its feature type (categorical, numerical, embedding), but also by its transformation.

<figure class="hops-diagram">
<svg viewBox="0 0 1000 380" role="img" aria-label="Two feature groups, seller_delivery_time_monthly and seller_reviews_quarterly, join into a feature view whose columns inherit their feature types and transformation functions." xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="fv-simple-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/></marker></defs>

  <text class="d-t" x="249" y="24" text-anchor="middle">seller_delivery_time_monthly_feature_group</text>
  <rect class="d-box" x="40" y="38" width="418" height="120" rx="8"/>
  <rect class="d-box-own" x="40" y="38" width="418" height="30" rx="8"/>
  <path class="d-flow" d="M141 38 V158"/>
  <path class="d-flow" d="M253 38 V158"/>
  <path class="d-flow" d="M40 98 H458"/>
  <path class="d-flow" d="M40 128 H458"/>
  <text class="d-t" x="90" y="58" text-anchor="middle">seller_id</text>
  <text class="d-t" x="197" y="58" text-anchor="middle">event_time</text>
  <text class="d-t" x="356" y="58" text-anchor="middle">avg_deliver_time_hrs</text>
  <text class="d-sub" x="90" y="87" text-anchor="middle" font-size="11">1112</text>
  <text class="d-sub" x="197" y="87" text-anchor="middle" font-size="11">oct-22</text>
  <text class="d-sub" x="356" y="87" text-anchor="middle" font-size="11">72</text>
  <text class="d-sub" x="90" y="117" text-anchor="middle" font-size="11">1112</text>
  <text class="d-sub" x="197" y="117" text-anchor="middle" font-size="11">nov-22</text>
  <text class="d-sub" x="356" y="117" text-anchor="middle" font-size="11">104</text>
  <text class="d-sub" x="90" y="147" text-anchor="middle" font-size="11">1112</text>
  <text class="d-sub" x="197" y="147" text-anchor="middle" font-size="11">dec-22</text>
  <text class="d-sub" x="356" y="147" text-anchor="middle" font-size="11">88</text>

  <text class="d-t" x="749" y="24" text-anchor="middle">seller_reviews_quarterly_feature_group</text>
  <rect class="d-box" x="540" y="38" width="418" height="90" rx="8"/>
  <rect class="d-box-own" x="540" y="38" width="418" height="30" rx="8"/>
  <path class="d-flow" d="M637 38 V128"/>
  <path class="d-flow" d="M745 38 V128"/>
  <path class="d-flow" d="M913 38 V128"/>
  <path class="d-flow" d="M540 98 H958"/>
  <text class="d-t" x="588" y="58" text-anchor="middle">seller_id</text>
  <text class="d-t" x="691" y="58" text-anchor="middle">event_time</text>
  <text class="d-t" x="829" y="58" text-anchor="middle">avg_review_score</text>
  <text class="d-t" x="936" y="58" text-anchor="middle">...</text>
  <text class="d-sub" x="588" y="87" text-anchor="middle" font-size="11">1112</text>
  <text class="d-sub" x="691" y="87" text-anchor="middle" font-size="11">oct-22</text>
  <text class="d-sub" x="829" y="87" text-anchor="middle" font-size="11">3.4</text>
  <text class="d-sub" x="936" y="87" text-anchor="middle" font-size="11">...</text>
  <text class="d-sub" x="588" y="117" text-anchor="middle" font-size="11">1112</text>
  <text class="d-sub" x="691" y="117" text-anchor="middle" font-size="11">dec-22</text>
  <text class="d-sub" x="829" y="117" text-anchor="middle" font-size="11">2.8</text>
  <text class="d-sub" x="936" y="117" text-anchor="middle" font-size="11">...</text>

  <path class="d-flow" d="M40 150 C 12 210, 16 316, 138 322" marker-end="url(#fv-simple-arrow)"/>
  <path class="d-flow" d="M958 120 C 992 200, 986 316, 830 322" marker-end="url(#fv-simple-arrow)"/>

  <text class="d-t" x="484" y="248" text-anchor="middle">seller_delivery_time_monthly_feature_view</text>
  <rect class="d-box" x="140" y="260" width="688" height="102" rx="8"/>
  <rect class="d-box-own" x="140" y="260" width="688" height="34" rx="8"/>
  <rect class="d-box-own" x="554" y="294" width="176" height="68"/>
  <path class="d-flow" d="M259 260 V362"/>
  <path class="d-flow" d="M361 260 V362"/>
  <path class="d-flow" d="M553 260 V362"/>
  <path class="d-flow" d="M731 260 V362"/>
  <path class="d-flow" d="M140 294 H828"/>
  <path class="d-flow" d="M140 328 H828"/>
  <text class="d-t" x="199" y="282" text-anchor="middle">seller_id</text>
  <text class="d-t" x="310" y="282" text-anchor="middle">event_time</text>
  <text class="d-t" x="457" y="282" text-anchor="middle">avg_deliver_time_hrs</text>
  <text class="d-t" x="642" y="282" text-anchor="middle">avg_review_score</text>
  <text class="d-t" x="780" y="282" text-anchor="middle">...</text>
  <text class="d-sub" x="199" y="315" text-anchor="middle" font-size="11">[PRIMARY_KEY]</text>
  <text class="d-sub" x="310" y="315" text-anchor="middle" font-size="11">[EVT_TIME]</text>
  <text class="d-sub" x="457" y="315" text-anchor="middle" font-size="11">[LABEL]</text>
  <text class="d-sub" x="642" y="315" text-anchor="middle" font-size="11">[NUMERICAL]</text>
  <text class="d-sub" x="457" y="349" text-anchor="middle" font-size="11">&lt;&lt;label_encoder&gt;&gt;</text>
  <text class="d-sub" x="642" y="349" text-anchor="middle" font-size="11">&lt;&lt;standard_scalar&gt;&gt;</text>
</svg>
</figure>

Feature views can also include:

- the label for the supervised ML problem
- transformation functions that should be applied to specified features consistently between training and serving
- the ability to create training data
- the ability to retrieve a feature vector with the most recent feature values

In the flow chart below, we can see the decisions that can be taken when creating (1) a feature view, and (2) creating training data with the feature view.

<figure class="hops-diagram">
<svg viewBox="0 0 1000 490" role="img" aria-label="A feature view is created by selecting features and a label from two feature groups and adding transformations, then generates training_data_v1, while the same feature view serves feature vectors retrieved by primary key." xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="fv-flow-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/></marker></defs>

  <rect class="d-box-own" x="60" y="26" width="210" height="44" rx="8"/>
  <text class="d-t" x="165" y="53" text-anchor="middle">product_feature_group</text>
  <rect class="d-box-own" x="330" y="26" width="230" height="44" rx="8"/>
  <text class="d-t" x="445" y="53" text-anchor="middle">order_weekly_feature_group</text>
  <path class="d-flow" d="M270 48 H330" stroke-dasharray="4 4"/>

  <path class="d-flow" d="M300 70 V208" marker-end="url(#fv-flow-arrow)"/>
  <text class="d-t" x="300" y="100" text-anchor="middle">select features</text>
  <text class="d-sub" x="300" y="118" text-anchor="middle" font-size="11">(product_id, category, ..., sold_previous_week, sales)</text>
  <text class="d-t" x="300" y="152" text-anchor="middle">select label = sales</text>
  <text class="d-t" x="300" y="192" text-anchor="middle">add transformations = { (normalize(), sales), (normalize(), sold_previous_week) }</text>

  <rect class="d-box-own" x="180" y="214" width="240" height="48" rx="8"/>
  <text class="d-t" x="300" y="243" text-anchor="middle">product_sales_feature_view</text>

  <path class="d-flow" d="M300 262 V416" marker-end="url(#fv-flow-arrow)"/>
  <text class="d-t" x="300" y="292" text-anchor="middle">Training data as DataFrames or Files?</text>
  <text class="d-t" x="300" y="328" text-anchor="middle">(start_time, end_time)</text>
  <text class="d-t" x="300" y="364" text-anchor="middle">filter (category_name == perfumaria)</text>
  <text class="d-t" x="300" y="400" text-anchor="middle">splits = { ('train', 80%), ('validation', 10%), ('test', 10%) }</text>

  <rect class="d-box-own" x="180" y="422" width="240" height="48" rx="8"/>
  <text class="d-t" x="300" y="451" text-anchor="middle">product_sales_training_data_v1</text>

  <path class="d-flow" d="M676 238 H424" marker-end="url(#fv-flow-arrow)"/>
  <text class="d-t" x="550" y="214" text-anchor="middle">Retrieve with primary key</text>
  <text class="d-sub" x="550" y="230" text-anchor="middle" font-size="11">(product_id=222)</text>

  <rect class="d-box" x="680" y="196" width="280" height="56" rx="8"/>
  <rect class="d-box-own" x="680" y="196" width="280" height="28" rx="8"/>
  <path class="d-flow" d="M791 196 V252"/>
  <path class="d-flow" d="M863 196 V252"/>
  <path class="d-flow" d="M680 224 H960"/>
  <text class="d-sub" x="735" y="215" text-anchor="middle" font-size="11">category</text>
  <text class="d-sub" x="827" y="215" text-anchor="middle" font-size="11">name</text>
  <text class="d-sub" x="911" y="215" text-anchor="middle" font-size="11">sold_prev_week</text>
  <text class="d-sub" x="735" y="243" text-anchor="middle" font-size="11">perfumes</text>
  <text class="d-sub" x="827" y="243" text-anchor="middle" font-size="11">d'odour</text>
  <text class="d-sub" x="911" y="243" text-anchor="middle" font-size="11">44</text>

  <rect class="d-box-own" x="700" y="270" width="240" height="40" rx="8"/>
  <text class="d-t" x="820" y="295" text-anchor="middle">product_sales_feature_vector</text>
</svg>
</figure>

We can see here how the feature view is a representation for a model in the feature store - the same feature view is used to retrieve feature vectors for operational model that was created with training data from this feature view.
As such, you can see that the most common use case for creating a feature view is to define the features that will be used in a model.
In this way, feature views enable features from different feature groups to be reused across different models, and if features are stored untransformed in feature groups, they become even more reusable, as different feature views can apply different transformations to the same feature.
