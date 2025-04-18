---
description: "Documentation on the Hopsworks capabilities to discover machine-learning assets"
---

## Search

Hopsworks supports free-text search to discover machine-learning assets:

* features
* feature groups
* feature views
* training data

You can use the search bar at the top of your project to free-text search for the names or descriptions of any ML asset. You can also search using keywords or tags that are attached to an ML asset.

You can search for assets within a specific project or across all projects in a Hopsworks deployment, including those you are not a member of. This allows for easier discoverability and reusability of assets within an organization. 
To avoid users gaining unauthorized access to data, if a search result is in a project you are **not** a member of, the information displayed is limited to: names, descriptions, tags, asset creator and create date. If the search result is within a project you are a member of, you are also able to inspect recent activities on the asset as well as statistics.

## Tags

A keyword is a single user-defined word attached to an ML asset. Keywords can be used to help it make it easier to find ML assets or understand the context in which they should be used, for example, *PII* could be used to indicate that the ML asset is based on personally identifiable information.

However, it may be preferable to have a stronger governance framework for ML assets than keywords alone. For this, you can define a *schematized tag*, defining a list of key/value tags along with a type for a value. In the figure below, you can see an example of a schematized tag with two key/value pairs: *pii* of type boolean (indicating if this feature group contains PII data), and *owner* of type string (indicating who the owner of the data in this feature group is). Note there is also a keyword defined for this feature group called *eu_region*, indicating the data has its origins in the EU.


<img src="../../../assets/images/concepts/projects/tags-keywords.png">


## Lineage

Hopsworks tracks the lineage (or provenance) of ML assets automatically for you. You can see what features are used in which feature view or training dataset. You can see what training dataset was used to train a given model. For assets that are managed outside of Hopsworks, there is support for the explicit definition of lineage dependencies.

<img src="../../../assets/images/concepts/projects/provenance.png">