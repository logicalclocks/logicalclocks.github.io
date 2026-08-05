# Offline API

The feature view provides an *Offline API* for

- creating training data
- creating batch (scoring) data

## Training Data

Training data is created using a feature view.
You can create training data as either:

- in-memory Pandas/Polars DataFrames, useful when you have a small amount of training data;
- materialized training data in files, in a file format of your choice (such as .tfrecord, .csv, or .parquet).

You can apply filters when creating training data from a feature view:

- start-time and end-time, for example, to create the train-set from an earlier time range, and the test-set from a later (unseen) time range;
- feature value features, for example, only train a model on customers from a particular country.

Note that filters are not applied when retrieving feature vectors using feature views, as we only look up features for a specific entity, like a customer.
In this case, the application should know that predictions for this customer should be made on the model trained on customers in USA, for example.

Materialized training data is immutable: once created, a training dataset version is not appended to or modified.
To retrain on new data, create a new training dataset version.
If the new data needs to be computed continuously, for example a daily batch for a time-series model, do that computation once in a [derived feature group][assign-parents-to-a-feature-group] that is kept up to date as new data arrives, and create a new training dataset version from it whenever you need updated data.

### Point-in-time Correct Training Data

When you create training data from features in different feature groups, it is possible that the feature groups are updated at different cadences.
For example, maybe one feature group is updated hourly, while another feature group is updated daily.
It is very complex to write code that joins features together from such feature groups and ensures there is no data leakage in the resultant training data.
Hopsworks hides this complexity by performing the point-in-time JOIN transparently, similar to the illustration below:

<figure class="hops-diagram">
<svg viewBox="0 0 1000 560" role="img" aria-label="A point-in-time correct join builds training data by combining two feature groups through a feature view, with green tracing the columns that originate from the reviews feature group into the resulting training dataset." xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="fvt-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/>
    </marker>
  </defs>

  <!-- feature group A: delivery time (neutral) -->
  <text class="d-t d-sub" x="40" y="46">seller_delivery_time_monthly_feature_group</text>
  <rect class="d-box" x="40" y="54" width="340" height="120" rx="8"/>
  <rect class="d-band" x="40" y="54" width="340" height="30" rx="8"/>
  <path class="d-flow" d="M130 54 V174 M230 54 V174" opacity=".4"/>
  <path class="d-flow" d="M40 84 H380 M40 114 H380 M40 144 H380" opacity=".4"/>
  <text class="d-t d-sub" x="85" y="73" text-anchor="middle">seller_id</text>
  <text class="d-t d-sub" x="180" y="73" text-anchor="middle">event_time</text>
  <text class="d-t d-sub" x="305" y="73" text-anchor="middle">deliver_time_hrs</text>
  <text class="d-t" x="85" y="104" text-anchor="middle">1112</text>
  <text class="d-t" x="180" y="104" text-anchor="middle">oct-22</text>
  <text class="d-t" x="305" y="104" text-anchor="middle">72</text>
  <text class="d-t" x="85" y="134" text-anchor="middle">1112</text>
  <text class="d-t" x="180" y="134" text-anchor="middle">nov-22</text>
  <text class="d-t" x="305" y="134" text-anchor="middle">104</text>
  <text class="d-t" x="85" y="164" text-anchor="middle">1112</text>
  <text class="d-t" x="180" y="164" text-anchor="middle">dec-22</text>
  <text class="d-t" x="305" y="164" text-anchor="middle">88</text>

  <!-- feature group B: reviews (owned, green) -->
  <text class="d-t d-sub" x="580" y="46">seller_reviews_quarterly_feature_group</text>
  <rect class="d-box-own" x="580" y="54" width="380" height="90" rx="8"/>
  <rect class="d-band" x="580" y="54" width="380" height="30" rx="8"/>
  <path class="d-flow" d="M670 54 V144 M770 54 V144 M920 54 V144" opacity=".4"/>
  <path class="d-flow" d="M580 84 H960 M580 114 H960" opacity=".4"/>
  <text class="d-t d-sub" x="625" y="73" text-anchor="middle">seller_id</text>
  <text class="d-t d-sub" x="720" y="73" text-anchor="middle">event_time</text>
  <text class="d-t d-sub" x="845" y="73" text-anchor="middle">avg_review_score</text>
  <text class="d-t d-sub" x="940" y="73" text-anchor="middle">...</text>
  <text class="d-t" x="625" y="104" text-anchor="middle">1112</text>
  <text class="d-t" x="720" y="104" text-anchor="middle">oct-22</text>
  <text class="d-t" x="845" y="104" text-anchor="middle">3.4</text>
  <text class="d-t" x="940" y="104" text-anchor="middle">...</text>
  <text class="d-t" x="625" y="134" text-anchor="middle">1112</text>
  <text class="d-t" x="720" y="134" text-anchor="middle">dec-22</text>
  <text class="d-t" x="845" y="134" text-anchor="middle">2.8</text>
  <text class="d-t" x="940" y="134" text-anchor="middle">...</text>

  <!-- joins into the feature view -->
  <path class="d-flow" d="M85 174 C 60 224, 150 280, 233 280" marker-end="url(#fvt-arrow)"/>
  <path class="d-flow" d="M940 144 C 992 214, 850 280, 767 280" marker-end="url(#fvt-arrow)"/>

  <!-- feature view (schema; avg_review_score column traced green) -->
  <text class="d-t d-sub" x="235" y="252">seller_delivery_time_monthly_feature_view</text>
  <rect class="d-box" x="235" y="260" width="530" height="40" rx="8"/>
  <rect class="d-box-own" x="575" y="260" width="190" height="40" rx="8"/>
  <path class="d-flow" d="M325 260 V300 M425 260 V300 M575 260 V300 M725 260 V300" opacity=".4"/>
  <text class="d-t d-sub" x="280" y="284" text-anchor="middle">seller_id</text>
  <text class="d-t d-sub" x="375" y="284" text-anchor="middle">event_time</text>
  <text class="d-t d-sub" x="500" y="284" text-anchor="middle">avg_deliver_time</text>
  <text class="d-t d-sub" x="650" y="284" text-anchor="middle">avg_review_score</text>
  <text class="d-t d-sub" x="745" y="284" text-anchor="middle">...</text>

  <!-- feature view produces training data -->
  <path class="d-flow" d="M500 300 V404" marker-end="url(#fvt-arrow)"/>

  <!-- training data (avg_review_score column traced green) -->
  <text class="d-t d-sub" x="250" y="402">seller_delivery_time_monthly_training_data.csv</text>
  <rect class="d-box" x="250" y="410" width="570" height="120" rx="8"/>
  <rect class="d-box-own" x="630" y="410" width="190" height="120" rx="8"/>
  <rect class="d-band" x="250" y="410" width="570" height="30" rx="8"/>
  <path class="d-flow" d="M340 410 V530 M440 410 V530 M630 410 V530 M780 410 V530" opacity=".4"/>
  <path class="d-flow" d="M250 440 H820 M250 470 H820 M250 500 H820" opacity=".4"/>
  <text class="d-t d-sub" x="295" y="429" text-anchor="middle">seller_id</text>
  <text class="d-t d-sub" x="390" y="429" text-anchor="middle">event_time</text>
  <text class="d-t d-sub" x="535" y="429" text-anchor="middle">deliver_time_hrs [LABEL]</text>
  <text class="d-t d-sub" x="705" y="429" text-anchor="middle">avg_review_score</text>
  <text class="d-t d-sub" x="800" y="429" text-anchor="middle">...</text>
  <text class="d-t" x="295" y="460" text-anchor="middle">1112</text>
  <text class="d-t" x="390" y="460" text-anchor="middle">oct-22</text>
  <text class="d-t" x="535" y="460" text-anchor="middle">72</text>
  <text class="d-t" x="705" y="460" text-anchor="middle">3.4</text>
  <text class="d-t" x="295" y="490" text-anchor="middle">1112</text>
  <text class="d-t" x="390" y="490" text-anchor="middle">nov-22</text>
  <text class="d-t" x="535" y="490" text-anchor="middle">104</text>
  <text class="d-t" x="705" y="490" text-anchor="middle">3.4</text>
  <text class="d-t" x="295" y="520" text-anchor="middle">1112</text>
  <text class="d-t" x="390" y="520" text-anchor="middle">nov-22</text>
  <text class="d-t" x="535" y="520" text-anchor="middle">88</text>
  <text class="d-t" x="705" y="520" text-anchor="middle">2.8</text>

  <!-- point-in-time correct join marker over the data rows -->
  <path class="d-flow" d="M244 440 H236 V530 H244"/>
  <text class="d-t d-sub" x="40" y="481">Point-in-Time</text>
  <text class="d-t d-sub" x="40" y="497">Correct JOIN</text>
</svg>
</figure>

Hopsworks uses the event_time columns on both feature groups to determine the most recent (but not newer) feature values that are joined together with the feature values from the feature group containing the label.
That is, the features in the feature group containing the label are the observation times for the features in the resulting training data, and we want feature values from the other feature groups that have the most recent timestamps, but not newer than the timestamp in the label-containing feature group.

<figure class="hops-diagram">
<svg viewBox="0 0 1000 420" role="img" aria-label="Point-in-time correct join. Each label row defines an observation time. For every observation time, the join picks the most recent row in each feature group whose event_time is at or before that observation time. Rows with a later event_time are excluded, so no future information leaks into the training data." xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="pit-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/>
    </marker>
    <marker id="pit-arrow-alert" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path class="d-alert" d="M0 0 L10 5 L0 10 z" fill-opacity=".8"/>
    </marker>
  </defs>

  <!-- observation-time guides -->
  <path class="d-flow" d="M440 54 V390" stroke-dasharray="3 4"/>
  <path class="d-flow" d="M800 54 V390" stroke-dasharray="3 4"/>

  <!-- feature group A -->
  <text class="d-t d-cap d-cap-fs" x="20" y="56">Feature group customer_profile, credit_score</text>
  <rect class="d-band" x="16" y="64" width="964" height="58" rx="10"/>
  <rect class="d-box" x="144" y="70" width="112" height="44" rx="6"/>
  <text class="d-t" x="200" y="90" text-anchor="middle">712</text>
  <text class="d-t d-sub" x="200" y="107" text-anchor="middle">Mar 10 06:00</text>
  <rect class="d-box-own" x="304" y="70" width="112" height="44" rx="6"/>
  <text class="d-t" x="360" y="90" text-anchor="middle">715</text>
  <text class="d-t d-sub" x="360" y="107" text-anchor="middle">Mar 11 06:00</text>
  <g opacity=".45">
    <rect class="d-box" x="464" y="70" width="112" height="44" rx="6"/>
    <text class="d-t" x="520" y="90" text-anchor="middle">730</text>
    <text class="d-t d-sub" x="520" y="107" text-anchor="middle">Mar 13 06:00</text>
  </g>
  <rect class="d-box-own" x="644" y="70" width="112" height="44" rx="6"/>
  <text class="d-t" x="700" y="90" text-anchor="middle">731</text>
  <text class="d-t d-sub" x="700" y="107" text-anchor="middle">Mar 14 06:00</text>
  <rect class="d-box" x="844" y="70" width="112" height="44" rx="6"/>
  <text class="d-t" x="900" y="90" text-anchor="middle">740</text>
  <text class="d-t d-sub" x="900" y="107" text-anchor="middle">Mar 16 06:00</text>

  <!-- labels / spine -->
  <text class="d-t d-cap d-cap-ext" x="20" y="176">Labels, spine of the join</text>
  <rect class="d-band" x="16" y="184" width="964" height="58" rx="10"/>
  <rect class="d-box-ext" x="384" y="190" width="112" height="44" rx="6"/>
  <text class="d-t" x="440" y="210" text-anchor="middle">fraud = 1</text>
  <text class="d-t d-sub" x="440" y="227" text-anchor="middle">Mar 12 10:00</text>
  <rect class="d-box-ext" x="744" y="190" width="112" height="44" rx="6"/>
  <text class="d-t" x="800" y="210" text-anchor="middle">fraud = 0</text>
  <text class="d-t d-sub" x="800" y="227" text-anchor="middle">Mar 15 09:00</text>

  <!-- feature group B -->
  <text class="d-t d-cap d-cap-fs" x="20" y="296">Feature group transactions_7d, amount_sum</text>
  <rect class="d-band" x="16" y="304" width="964" height="58" rx="10"/>
  <rect class="d-box" x="184" y="310" width="112" height="44" rx="6"/>
  <text class="d-t" x="240" y="330" text-anchor="middle">1 204</text>
  <text class="d-t d-sub" x="240" y="347" text-anchor="middle">Mar 10 12:00</text>
  <rect class="d-box-own" x="314" y="310" width="112" height="44" rx="6"/>
  <text class="d-t" x="370" y="330" text-anchor="middle">1 318</text>
  <text class="d-t d-sub" x="370" y="347" text-anchor="middle">Mar 11 12:00</text>
  <g opacity=".45">
    <rect class="d-box" x="504" y="310" width="112" height="44" rx="6"/>
    <text class="d-t" x="560" y="330" text-anchor="middle">2 090</text>
    <text class="d-t d-sub" x="560" y="347" text-anchor="middle">Mar 13 12:00</text>
  </g>
  <rect class="d-box-own" x="634" y="310" width="112" height="44" rx="6"/>
  <text class="d-t" x="690" y="330" text-anchor="middle">1 877</text>
  <text class="d-t d-sub" x="690" y="347" text-anchor="middle">Mar 14 00:00</text>
  <rect class="d-box" x="834" y="310" width="112" height="44" rx="6"/>
  <text class="d-t" x="890" y="330" text-anchor="middle">2 431</text>
  <text class="d-t d-sub" x="890" y="347" text-anchor="middle">Mar 16 00:00</text>

  <!-- lookups for the first observation time -->
  <path class="d-flow" d="M414 188 C 396 164, 380 140, 368 120" stroke-dasharray="4 3" marker-end="url(#pit-arrow)"/>
  <path class="d-flow" d="M414 236 C 396 260, 384 288, 374 304" stroke-dasharray="4 3" marker-end="url(#pit-arrow)"/>
  <path class="d-alert-line" d="M470 188 C 486 168, 498 142, 506 120" stroke-opacity=".7" stroke-dasharray="4 3" marker-end="url(#pit-arrow-alert)"/>
  <path class="d-alert-line" d="M470 236 C 490 258, 502 286, 512 304" stroke-opacity=".7" stroke-dasharray="4 3" marker-end="url(#pit-arrow-alert)"/>
  <text class="d-alert" x="536" y="150" font-size="11">excluded, newer than the label</text>
  <text class="d-alert" x="536" y="278" font-size="11">excluded, newer than the label</text>

  <!-- lookups for the second observation time -->
  <path class="d-flow" d="M774 188 C 756 164, 728 138, 712 120" stroke-dasharray="4 3" marker-end="url(#pit-arrow)"/>
  <path class="d-flow" d="M774 236 C 754 260, 722 288, 706 304" stroke-dasharray="4 3" marker-end="url(#pit-arrow)"/>

  <!-- time axis -->
  <path class="d-flow" d="M120 390 H966" marker-end="url(#pit-arrow)"/>
  <text class="d-t d-sub" x="960" y="382" text-anchor="end">time</text>
  <text class="d-t d-sub" x="446" y="50">observation time</text>
</svg>
</figure>

#### Spine Groups

The left side of the point-in-time join is typically the set of training entities/primary key values for which the relevant features need to be retrieved.
This left side of the join can also be replaced by a [spine group](../feature_group/spine_group.md).
When using feature groups also so save labels/prediction targets, it can happen that you end up with the same entity multiple times in the training dataset depending on the cadence at which the label group was updated and the length of the event time interval
that is being used to generate the training dataset.
This can lead to bias in the training dataset and should be avoided.
To avoid this kind of situation, users can either narrow down the event time interval during training dataset creation or use a spine
in order to precisely define the entities to be included in the training dataset.
This is just one example where spines are helpful.

### Splitting Training Data

You can create random train/validation/test splits of your training data using the Hopsworks API.
You can also time-based splits with the Hopsworks API.

### Evaluation Sets

Test data can also be split into evaluation sets to help evaluate a model for potential bias.
First, you have to identify the classes of samples that could be at risk of bias, and generate *evaluation sets* from your unseen test set - one evaluation set for each group of samples at risk of bias.
For example, if you have a feature group of users, where one of the features is gender, and you want to evaluate the risk of bias due to gender, you can use filters to generate 3 evaluation sets from your test set - one for male, female, and non-binary.
Then you score your model against all 3 evaluation sets to ensure that the prediction performance is comparable and non-biased across all 3 gender.

## Batch (Scoring) Data

Batch data for scoring models is created using a feature view.
Similar to training data, you can create batch data as either:

- in-memory Pandas/Polars DataFrames, useful when you have a small amount of data to score;
- materialized data in files, in a file format of your choice (such as .tfrecord, .csv, or .parquet)

Batch data requires specification of a `start_time` for the start of the batch scoring data.
You can also specify the `end_time` (default is the current date).

<figure class="hops-diagram">
<svg viewBox="0 0 1000 230" role="img" aria-label="A feature view spans a single timeline from which one training dataset version and successive daily batch scoring datasets are created." xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="bsd-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/>
    </marker>
  </defs>

  <!-- feature view spanning the timeline -->
  <rect class="d-panel-fs" x="16" y="20" width="968" height="110" rx="12"/>
  <text class="d-t" x="500" y="50" text-anchor="middle">FeatureView</text>
  <path class="d-flow" d="M60 92 H940" marker-end="url(#bsd-arrow)"/>
  <text class="d-t d-sub" x="500" y="114" text-anchor="middle">Time</text>

  <!-- ranges carved out of the same timeline -->
  <path class="d-flow" d="M40 145 v8 M40 153 H470 M470 145 v8 M255 153 v8"/>
  <path class="d-flow" d="M490 145 v8 M490 153 H720 M720 145 v8 M605 153 v8"/>
  <path class="d-flow" d="M740 145 v8 M740 153 H970 M970 145 v8 M855 153 v8"/>

  <text class="d-t" x="255" y="188" text-anchor="middle">TrainingData v1</text>
  <text class="d-t" x="605" y="188" text-anchor="middle">Batch Scoring Data</text>
  <text class="d-t d-sub" x="605" y="205" text-anchor="middle">2022/03/30</text>
  <text class="d-t" x="855" y="188" text-anchor="middle">Batch Scoring Data</text>
  <text class="d-t d-sub" x="855" y="205" text-anchor="middle">2022/03/31</text>
</svg>
</figure>

### Spine Dataframes

Similar to training dataset generation, it might be helpful to specify a spine when retrieving features for batch inference.
The only difference in this case is that the spine dataframe doesn't
need to contain the label, as this will be the output of the inference pipeline.
A typical use case is the handling of opt-ins, where certain customers have to be excluded from an inference pipeline due to a missing marketing opt-in.
