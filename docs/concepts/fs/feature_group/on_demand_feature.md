---
description: On-demand feature computation.
---

# On-demand features

Features are defined as on-demand when their value cannot be pre-computed beforehand, rather they need to be computed in real-time during inference. This is achieved by implementing the on-demand features as a Python function in a Python module. Also ensure that the same version of the Python module is installed in both the feature and inference pipelines.

In the image below shows an example of a housing price model that demonstrates how to implement an on-demand feature, a zip code (or post code) that is computed using longitude/latitude parameters. In your online application, longitude and latitude are provided as parameters to the application, and the same python function used to calculate the zip code in the feature pipeline is used to compute the zip code in the Online Inference pipeline.

<img src="../../../../assets/images/concepts/fs/on-demand-feature.png">
