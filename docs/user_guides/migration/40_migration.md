# 4.0 Migration Guide

## Breaking Changes

With the release of Hopsworks 4.0, a number of necessary breaking
changes have been put in place to improve the overall experience of
using the Hopsworks platform. These breaking changes can be categorized
in the following areas:

- Python API

- Multi-Environment Docker Images

- On-Demand Transformation Functions

### Python API

A number of significant changes have been made in the Python API
Hopsworks 4.0. Previously, in Hopsworks 3.X, there were 3 python
libraries used (“hopsworks”, “hsfs” & “hsml”) to develop feature,
training & inference pipelines, with the 4.0 release there is now
one single “hopsworks” python library that can should be used. For
backwards compatibility, it will still be possible to import both
the “hsfs” & “hsml” libraries but these are now effectively aliases
to the “hopsworks” python library and their use going forward should
be considered as deprecated.

Another significant change in the Hopsworks Python API is the use of
optional extras to allow a developer to easily import exactly what is
needed as part of their work. The main ones are great-expectations and
polars. It is arguable whether this is a breaking change but it is
important to note depending on how a particular pipeline has been
written which may encounter a problem when executing using Hopsworks
4.0.

Finally, there are a number of relatively small breaking changes and
deprecated methods to improve the developer experience, these include:

- connection.init() is now considered deprecated

- When loading arrow_flight_client, an OptionalDependencyNotFoundError can be now thrown providing more detailed information on the error than the previous ModuleNotFoundError in 3.X.

- DatasetApi's zip and unzip will now return False when a timeout is exceeded instead of previously throwing an Exception

### Multi-Environment Docker Images

As part of the Hopsworks 4.0 release, an engineering team using
Hopsworks can now customize the docker images that they use for their
feature, training and inference pipelines. By adding this flexibility,
a set of breaking changes are necessary. Instead of having one common
docker image for fti pipelines, with the release of 4.0 a number of
specific docker images are provided to allow an engineering team using
Hopsworks to install exactly what they need to get their feature,
training and inference pipelines up and running. This breaking change
will require existing customers running Hopsworks 3.X to test their
existing pipelines using Hopsworks 4.0 before upgrading their
production environments.

### On-Demand Transformation Functions

A number of changes have been made to transformation functions in the
last releases of Hopsworks. With 4.0, On-Demand Transformation Functions
are now better supported which has resulted in some breaking changes.
The following is how transformation functions were used in previous
versions of Hopsworks and the how transformation functions are used
in the 4.0 release.

=== "Pre-4.0"
    ```python
 #################################################

# Creating transformation funciton Hopsworks 3.8#

 #################################################

# Define custom transformation function

 def add_one(feature):
  return feature + 1

# Create transformation function

 add_one = fs.create_transformation_function(add_one,
  output_type=int,
        version=1,
    )

# Save transformation function

 add_one.save()

# Retrieve transformation function

 scaler = fs.get_transformation_function(
  name="add_one",
  version=1,
 )

# Create feature view

 feature_view = fs.get_or_create_feature_view(
  name='serving_fv',
  version=1,
  query=selected_features,

# Apply your custom transformation functions to the feature `feature_1`

  transformation_functions={
   "feature_1": add_one,
  },
  labels=['target'],
 )
    ```

=== "4.0"
    ```python
 #################################################

# Creating transformation funciton Hopsworks 4.0#

 #################################################

# Define custom transformation function

 @hopsworks.udf(int)
 def add_one(feature):
  return feature + 1

# Create feature view

 feature_view = fs.get_or_create_feature_view(
  name='serving_fv',
  version=1,
  query=selected_features,

# Apply the custom transformation functions defined to the feature `feature_1`

  transformation_functions=[
   add_one("feature_1"),
  ],
  labels=['target'],
 )
    ```

Note that the number of lines of code required has been significantly
reduced using the “@hopsworks.udf” python decorator.
