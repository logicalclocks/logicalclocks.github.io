---
description: On-demand feature computation.
---

# On-demand features

Features are defined as on-demand when their value cannot be pre-computed beforehand, rather they need to be computed in real-time during inference.
This is achieved by implementing the on-demand features as a Python function in a Python module.
Also ensure that the same version of the Python module is installed in both the feature and inference pipelines.

In the image below shows an example of a housing price model that demonstrates how to implement an on-demand feature, a zip code (or post code) that is computed using longitude/latitude parameters.
In your online application, longitude and latitude are provided as parameters to the application, and the same python function used to calculate the zip code in the feature pipeline is used to compute the zip code in the Online Inference pipeline.

<figure class="hops-diagram">
<svg viewBox="0 0 1000 630" role="img" aria-label="The same on-demand Python function computes the zipcode feature from longitude and latitude in both the feature pipeline and the online inference pipeline, where it is merged with precomputed features from the feature store." xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="odf-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/></marker></defs>

  <text class="d-t" x="20" y="34">On-demand feature function</text>
  <rect class="d-box" x="20" y="42" width="960" height="92" rx="8"/>
  <text class="d-sub" x="36" y="68" font-size="11">def coord2zipcode(x):</text>
  <text class="d-sub" x="36" y="92" font-size="11">    geolocator = geopy.Nominatim(user_agent="house_profile_1")</text>
  <text class="d-sub" x="36" y="116" font-size="11">    return geolocator.reverse("{}, {}".format(x['latitude'], x['longitude']))</text>

  <path class="d-flow" d="M90 440 V136" marker-end="url(#odf-arrow)"/>
  <path class="d-flow" d="M205 136 V440" marker-end="url(#odf-arrow)"/>
  <path class="d-flow" d="M745 440 V136" marker-end="url(#odf-arrow)"/>
  <path class="d-flow" d="M835 136 V440" marker-end="url(#odf-arrow)"/>

  <rect class="d-box" x="15" y="300" width="150" height="30" rx="15"/>
  <text class="d-sub" x="90" y="320" text-anchor="middle" font-size="11">X['longitude', 'latitude']</text>
  <rect class="d-box" x="175" y="300" width="60" height="30" rx="15"/>
  <text class="d-sub" x="205" y="320" text-anchor="middle" font-size="11">zipcode</text>
  <rect class="d-box" x="670" y="300" width="150" height="30" rx="15"/>
  <text class="d-sub" x="745" y="320" text-anchor="middle" font-size="11">X['longitude', 'latitude']</text>
  <rect class="d-box" x="800" y="300" width="70" height="30" rx="15"/>
  <text class="d-sub" x="835" y="320" text-anchor="middle" font-size="11">zipcode</text>

  <rect class="d-box" x="20" y="440" width="200" height="64" rx="8"/>
  <text class="d-t" x="120" y="477" text-anchor="middle">feature_pipeline.py</text>
  <rect class="d-box-ext" x="60" y="560" width="110" height="44" rx="8"/>
  <text class="d-sub" x="115" y="587" text-anchor="middle" font-size="11">housing.csv</text>
  <path class="d-flow" d="M115 560 V508" marker-end="url(#odf-arrow)"/>

  <rect class="d-panel-fs" x="250" y="400" width="250" height="200" rx="12"/>
  <text class="d-cap d-cap-fs" x="320" y="434" text-anchor="middle">Feature Group</text>
  <text class="d-cap d-cap-fs" x="442" y="434" text-anchor="middle">Feature View</text>
  <rect class="d-box-own" x="270" y="450" width="100" height="44" rx="8"/>
  <text class="d-t" x="320" y="477" text-anchor="middle">house_arch</text>
  <rect class="d-box-own" x="270" y="510" width="100" height="44" rx="8"/>
  <text class="d-t" x="320" y="537" text-anchor="middle">zipcodes</text>
  <rect class="d-box-own" x="400" y="470" width="85" height="74" rx="8"/>
  <text class="d-t" x="442" y="511" text-anchor="middle">house_profile</text>

  <path class="d-flow" d="M220 472 H266" marker-end="url(#odf-arrow)"/>
  <path class="d-flow" d="M220 496 H243 V532 H266" marker-end="url(#odf-arrow)"/>
  <path class="d-flow" d="M370 472 H385 V495 H396" marker-end="url(#odf-arrow)"/>
  <path class="d-flow" d="M370 532 H385 V520 H396" marker-end="url(#odf-arrow)"/>

  <rect class="d-box" x="720" y="440" width="130" height="64" rx="8"/>
  <text class="d-t" x="785" y="477" text-anchor="middle">predictor.py</text>
  <rect class="d-box-ext" x="870" y="440" width="120" height="64" rx="8"/>
  <text class="d-t" x="930" y="468" text-anchor="middle">Online</text>
  <text class="d-t" x="930" y="490" text-anchor="middle">Application</text>
  <path class="d-flow" d="M870 472 H853" marker-end="url(#odf-arrow)"/>

  <path class="d-flow" d="M720 485 H489" marker-end="url(#odf-arrow)"/>
  <text class="d-sub" x="595" y="470" text-anchor="middle" font-size="11">get_feature_vector(.., passed_features={"zipcode": zipcode})</text>
  <text class="d-sub" x="595" y="502" text-anchor="middle" font-size="11">merge on-demand 'zipcode' feature with</text>
  <text class="d-sub" x="595" y="518" text-anchor="middle" font-size="11">precomputed features from feature store</text>
</svg>
</figure>

## Shift left or shift right

Deciding to compute a feature on-demand is a shift-right decision, and it is one of the biggest feature-engineering choices you make.
Shift left means precomputing a feature in a feature pipeline and storing it in the feature store for retrieval.
Shift right means computing it at request time, in an on-demand or model-dependent transformation.

Shift right when the feature depends on request-time input, such as the zip code computed from the longitude and latitude in a request, or when a precomputed value would be too stale to be useful.
Shift left when the feature can be precomputed, to keep inference latency low and avoid repeating the computation on every request.
The trade-off is latency and operational overhead against freshness.
