Hopsworks supports free-text search for ML assets:

* features,
* feature groups,
* feature views,
* training data,
* models, and
* deployments.

You can use the search bar at the top of your project to free-text search for the names or descriptions of any ML asset. You can also search using keywords or tags that are attached to an ML asset.
A keyword is a single user-defined word attached to an ML asset. Keywords can be used to help it make it easier to find ML assets or understand the context in which they should be used (for example, *PII* could be used to indicate that the ML asset is based on personally identifiable information.

However, it may be preferable to have a stronger governance framework for ML assets than keywords alone. For this, you can define a *schematized tag*, defining a list of key/value tags along with a type for a value. In the figure below, you can see an example of a schematized tag with two key/value pairs: *pii* of type boolean (indicating if this feature group contains PII data), and *owner* of type string (indicating who the owner of the data in this feature group is). Note there is also a keyword defined for this feature group called *eu_region*, indicating the data has its origins in the EU.


<img src="../../../assets/images/concepts/projects/tags-keywords.png">


## Lineage

Hopsworks tracks lineage in two separate ways:
* implicit
* explicit

Implicit provenance means that the user doesn't have to change his code and the system will determine links between different artifacts based on their usage(read/write) within the context of the same application. 

Explicit provenance has the user, explicitly marking the links between artifacts by performing additional method calls within their code.

Both of the approache have pros and cons. Implicit provenance may add links where there might be none, because maybe the mechanisms are not fine grained enough. For example, you read two feature groups and write two feature groups. 
Depending on how fine grained the system is and where in the stack the tracking is being done, there might be links added between both read feature groups and both written feature groups, so four links, even though maybe there should only be two links. Perfect implicit provenance would have all components track all interactions and report them in a way that can be easily combined. If this is not possible, you might want to modify some core components, such as the file system and resource manager and collect imperfect implicit provenance from these, such as we do at Hopsworks. 
Explicit provenance, however relies on the user remembering to mark each link and to delete the call when the link is removed at a later time. 

The aim, however, it to combine both mechanism and try to get a view as good as possible of the actions happening in the system. The implicit provenance can act as a sort of a reminder to the user abut their explicit calls. For example, you have marked feature group X as a source of a link, but you no longer read it in the code, but we see in previous version of the code you did read it -  did you maybe forgot to remove the explicit provenance call.

Hopsworks tracks the lineage (or provenance) of ML assets:
* feature groups:
	- external feature groups
    - cached feature groups
    - streaming feature groups
* feature views
* training datasets
* models

<img src="../../../assets/images/concepts/projects/provenance.png">