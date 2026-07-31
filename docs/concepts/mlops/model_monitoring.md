Model monitoring lets you track how a deployed model behaves in production by comparing the data it serves against the data it was trained on.

When a model runs in production, the statistical properties of its inputs and predictions can drift away from those of the training data.
This degrades model quality silently, without any error being raised.
Model monitoring detects this drift early so you can decide whether to retrain the model.

## How it works

Model monitoring builds on two existing Hopsworks capabilities:

- **Feature logging**: a model deployment logs the features it serves and its predictions to the feature view's logging feature group through the Feature View logging APIs.
  See the [Feature Logging guide](../../user_guides/fs/feature_view/feature_logging.md).
- **Feature monitoring**: Hopsworks computes statistics over windows of feature data and compares them against a reference, optionally raising alerts on significant shifts.
  See the [Feature Monitoring concept](../fs/feature_view/feature_monitoring.md).

!!! info "Feature logging vs. the inference logger"
    Hopsworks provides two separate inference logging mechanisms.
    The [inference logger](../../user_guides/mlops/serving/inference-logger.md) stores the model inputs and predictions from inference requests and responses into Kafka, for later consumption and analysis.
    [Feature logging](../../user_guides/fs/feature_view/feature_logging.md) supports more fine-grained logging of inference logs and features, enabling feature monitoring and model monitoring.
    Model monitoring relies on feature logging, not on the inference logger.

A model monitoring configuration is a feature monitoring configuration over the logging feature group, filtered to a single model and version.
The detection window covers the recently served inference data, and the reference defaults to the training dataset version that was used to train that model.
By comparing the two, on a scalar metric or on the whole feature distribution, Hopsworks detects feature drift over time.
This comparison detects drift, not skew: offline-online feature skew is a difference in the transformation code between the offline and inference pipelines, so it is invisible to a distribution comparison and is prevented, not monitored.

<figure class="hops-diagram">
<svg viewBox="0 0 1000 420" role="img" aria-label="Drift detection over time. The training dataset distribution is the reference on the left. A detection window slides forward over the logged inference data and its distribution is compared against the reference. The resulting distance is plotted over time and crosses the alert threshold when the served data drifts away from the training data." xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="mm-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/>
    </marker>
  </defs>

  <!-- reference: training data distribution -->
  <text class="d-t d-cap d-cap-fs" x="22" y="40">Reference</text>
  <rect class="d-panel-fs" x="16" y="52" width="204" height="140" rx="12"/>
  <rect class="d-box-own" x="36" y="152" width="17" height="16" rx="2"/>
  <rect class="d-box-own" x="57" y="134" width="17" height="34" rx="2"/>
  <rect class="d-box-own" x="78" y="110" width="17" height="58" rx="2"/>
  <rect class="d-box-own" x="99" y="88" width="17" height="80" rx="2"/>
  <rect class="d-box-own" x="120" y="88" width="17" height="80" rx="2"/>
  <rect class="d-box-own" x="141" y="110" width="17" height="58" rx="2"/>
  <rect class="d-box-own" x="162" y="134" width="17" height="34" rx="2"/>
  <rect class="d-box-own" x="183" y="152" width="17" height="16" rx="2"/>
  <text class="d-t d-sub" x="118" y="184" text-anchor="middle">training dataset v1</text>

  <!-- logged inference data over time -->
  <text class="d-t d-cap d-cap-ext" x="278" y="40">Logged inference data</text>
  <rect class="d-panel-ext" x="272" y="52" width="708" height="140" rx="12"/>
  <path class="d-flow" d="M296 172 H964"/>
  <path class="d-flow" d="M300 172 V148 M322 172 V142 M344 172 V152 M366 172 V144 M388 172 V150 M410 172 V140 M432 172 V154 M454 172 V146 M476 172 V142 M498 172 V150 M520 172 V144 M542 172 V152 M564 172 V146 M586 172 V140 M608 172 V148 M630 172 V152 M652 172 V142 M674 172 V146 M696 172 V150 M718 172 V144 M740 172 V148 M762 172 V138 M784 172 V142 M806 172 V134 M828 172 V136 M850 172 V128 M872 172 V130 M894 172 V122 M916 172 V126 M938 172 V118 M960 172 V122"/>
  <rect class="d-box" x="470" y="66" width="150" height="114" rx="8" stroke-dasharray="4 3"/>
  <text class="d-t d-sub" x="545" y="86" text-anchor="middle">earlier window</text>
  <rect class="d-box-own" x="800" y="66" width="160" height="114" rx="8"/>
  <text class="d-t d-sub" x="880" y="86" text-anchor="middle">detection window</text>
  <path class="d-flow" d="M634 104 H792" stroke-dasharray="4 3" marker-end="url(#mm-arrow)"/>
  <text class="d-t d-sub" x="713" y="98" text-anchor="middle">slides forward</text>

  <!-- comparison connector -->
  <path class="d-flow" d="M118 194 V212 H840 V184" stroke-dasharray="4 3" marker-end="url(#mm-arrow)"/>
  <text class="d-t d-sub" x="480" y="206" text-anchor="middle">compare the two distributions</text>

  <!-- drift metric over time -->
  <text class="d-t d-cap" x="272" y="248">Drift metric, distance from the reference</text>
  <path class="d-flow" d="M300 262 V376"/>
  <path class="d-flow" d="M300 376 H962" marker-end="url(#mm-arrow)"/>
  <path class="d-flow" d="M880 194 V270" stroke-dasharray="3 4"/>
  <path d="M300 296 H962" fill="none" stroke="#eb5757" stroke-width="1.5" stroke-dasharray="6 4" stroke-opacity=".85"/>
  <text x="306" y="290" font-size="11" fill="#eb5757">alert threshold</text>
  <path class="d-flow" d="M320 358 L400 354 L480 348 L560 344 L640 336 L720 324 L800 308 L880 282 L940 264" stroke-width="2" stroke-opacity=".6"/>
  <circle cx="320" cy="358" r="3" fill="currentColor" fill-opacity=".45"/>
  <circle cx="400" cy="354" r="3" fill="currentColor" fill-opacity=".45"/>
  <circle cx="480" cy="348" r="3" fill="currentColor" fill-opacity=".45"/>
  <circle cx="560" cy="344" r="3" fill="currentColor" fill-opacity=".45"/>
  <circle cx="640" cy="336" r="3" fill="currentColor" fill-opacity=".45"/>
  <circle cx="720" cy="324" r="3" fill="currentColor" fill-opacity=".45"/>
  <circle cx="800" cy="308" r="3" fill="currentColor" fill-opacity=".45"/>
  <circle cx="880" cy="282" r="4" fill="#eb5757"/>
  <circle cx="940" cy="264" r="4" fill="#eb5757"/>
  <text x="956" y="252" font-size="11" fill="#eb5757" text-anchor="end">drift alert</text>
  <text class="d-t d-sub" x="958" y="392" text-anchor="end">time</text>
</svg>
</figure>

## Where to configure it

Because monitoring is anchored on the feature view that backs the model, you can configure model monitoring from whichever entity is most convenient:

- a **model deployment**, when operating a model in production.
- a **model** in the model registry.
- a **feature view**, when working directly with the feature data.

All three resolve to the same underlying configuration.

!!! info "Model Monitoring Guide"
    More information can be found in the [Model Monitoring guide](../../user_guides/mlops/model_monitoring/index.md).
