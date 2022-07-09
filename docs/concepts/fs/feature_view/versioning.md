Feature views are interfaces, and if there is a change in the interface (the types of the features, the transformations applied to the features), then you need to change the version, to prevent breaking existing clients.

Training datasets are associated with a specific feature view version. Training data also has its own version number (along with the version of its parent feature view). For example, online transformation functions often need training data statistics (e.g., normalizing a numerical feature requires you to divide the feature value by the mean value for that feature in the training dataset). As many training datasets can be created from a feature view, when you initialize the feature view you need to tell it which version of the training data to use - `feature_view.init(1)` means use version 1 of the training data for this feature view.


