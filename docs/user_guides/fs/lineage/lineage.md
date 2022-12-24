# Lineage

## Introduction 

Hopsworks feature store enables users to track lineage between feature groups, feature views and training dataset. Tracking lineage allows users to determine where/if a feature group is being used. You can track if feature groups are being used to create additional (derived) feature groups; or which which feature view they are being used in and to generate which training dataset.

You can visualize lineage information by using the UI or the Feature Store APIs.

## Step 1: Feature group lineage

### Assign parents to a feature group

When creating a feature group, it is possible to specify a list of feature groups used to derive features. For example, you could have an external feature group defined over a Snowflake or Redshift fact table, which you use to compute the features and save it in a new feature group. You can set the external feature group as parent of the feature group you are creating:

...

Another use case is when you have a feature group containing features with daily resolution and you are using the content of that feature group to populate a second feature group with monthly resolution: 

...

### List feature group parents

You can query the lineage of a feature group using the UI and the APIs. From the APIs you can list the parent feature groups by doing:

....

You can visualize and browse the feature groups 

## Step 2: Feature view lineage

You don't have to do anything 

## Step 3: Training dataset lineage