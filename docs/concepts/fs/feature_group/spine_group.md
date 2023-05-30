---
description: Explanation of the Spine concept in feature pipelines and training dataset creation.
---

# Spine Group

It is possible to maintain labels or prediction events among the regular features in a regular feature group
with a feature pipeline updating the labels at a specific cadence.

Often times, however, it is more convenient to provide the training events or entities in a Dataframe when reading
feature data from the feature store through a feature view. We call such a Dataframe a Spine as it is the structure around which
the training data or batch data is built.
In order to retrieve the correct feature values for the entities in the Dataframe, using
a point-in-time correct join, some additional metadata apart from the Dataframe schema is necessary. Namely, the information about which
columns define the **primary key**, and which column indicates the **event time** at which the label was valid.
The spine Dataframe together with this additional metadata is what we call a **Spine Group**.

For example, in the following spine, we want to retrieve the features for the three locations, no later than the event time of each of the rainfall
measurements, which is our prediction target:

| location_id | event_time       | rainfall (label) |
| ----------- | ---------------- | -----------------|
| 1           | 2022-06-01 13:11 | 44               |
| 2           | 2022-06-01 09:14 | 5                |
| 3           | 2022-06-01 06:36 | 2                |

A Spine Group does not materialize any data to the feature store itself, and always needs to be provided when retrieving features from the [offline API](../feature_view/offline_api.md).
You can think of it as a place holder or a temporary feature group, to be replaced by a Dataframe in point in time joins.

When using the [online API](../feature_view/online_api.md), it is not necessary to provide the spine, since the online feature store contains only the latest feature values, and therefore
no point in time join is required, the label is not required, as the inference pipelien is going to compute the prediciton
and the primary key values are specified when calling the online API.
