---
description: On-demand feature computation.
---

# On-demand features

Features are defined as on-demand when their value cannot be pre-computed beforehand, rather they need to be computed in real-time during inference.
This is achieved by implementing the on-demand features as a Python function in a Python module.
Also ensure that the same version of the Python module is installed in both the feature and inference pipelines.

In the image below shows an example of a housing price model that demonstrates how to implement an on-demand feature, a zip code (or post code) that is computed using longitude/latitude parameters.
In your online application, longitude and latitude are provided as parameters to the application, and the same python function used to calculate the zip code in the feature pipeline is used to compute the zip code in the Online Inference pipeline.

--8<-- "concepts/fs/feature_group/on_demand_feature/on-demand-features.html"

## Shift left or shift right

Deciding to compute a feature on-demand is a shift-right decision, and it is one of the biggest feature-engineering choices you make.
Shift left means precomputing a feature in a feature pipeline and storing it in the feature store for retrieval.
Shift right means computing it at request time, in an on-demand or model-dependent transformation.

Shift right when the feature depends on request-time input, such as the zip code computed from the longitude and latitude in a request, or when a precomputed value would be too stale to be useful.
Shift left when the feature can be precomputed, to keep inference latency low and avoid repeating the computation on every request.
The trade-off is latency and operational overhead against freshness.
