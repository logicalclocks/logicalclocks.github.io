A feature view is a logical view over (or interface to) a set of features that may come from different feature groups. You create a feature view by joining together features from existing feature groups. In the illustration below, we can see that features are joined together from the two feature groups: seller_delivery_time_monthly and the seller_reviews_quarterly. You can also see that features in the feature view inherit not only the feature type from their feature groups, but also whether they are the primary key and/or the event_time. The image also includes transformation functions that are applied to individual features. Transformation functions are a part of the feature types included in the feature view. That is, a feature in a feature view is not only defined by its data type (int, string, etc) or its feature type (categorical, numerical, embedding), but also by its transformation. 

<img src="../../../../assets/images/concepts/fs/feature-view-simple.svg">


Feature views can also include:

 - the label for the supervised ML problem 
 - transformation functions that should be applied to specified features consistently between training and serving
 - the ability to create training data
 - the ability to retrieve a feature vector with the most recent feature values

In the flow chart below, we can see the decisions that can be taken when creating (1) a feature view, and (2) creating training data with the feature view.

<img src="../../../../assets/images/concepts/fs/feature-view-flowchart.svg">

We can see here how the feature view is a representation for a model in the feature store - the same feature view is used to retrieve feature vectors for operational model that was created with training data from this feature view. As such, you can see that the most common use case for creating a feature view is to define the features that will be used in a model. In this way, feature views enable features from different feature groups to be reused across different models, and if features are stored untransfromed in feature groups, they become even more reusable, as different feature views can apply different transformations to the same feature.
