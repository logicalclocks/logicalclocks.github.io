# Data Validation, Statistics, and Alerts

Hopsworks supports monitoring, validation, and alerting for features:

- transparently compute statistics over features on writing to a feature group;
- validation of data written to feature groups using Great Expectations
- alerting users when there was a problem writing or update features.

## Statistics

When you create a Feature Group in Hopsworks, you can configure it to compute statistics over the features inserted into the Feature Group by setting the `statistics_config` dict parameter, see [Feature Group Statistics](../../../user_guides/fs/feature_group/statistics.md) for details.
Every time you write to the Feature Group, new statistics will be computed over all of the data in the Feature Group.

## Data Validation

You can define expectation suites in Great Expectations and associate them with feature groups.
When you write to a feature group, the expectations are executed, then you can define a policy on the feature group for what to do if any expectation fails.

<figure class="hops-diagram">
<svg viewBox="0 0 1000 410" role="img" aria-label="On fg.insert, HSFS runs Great Expectations to compute metrics, profile statistics, and validate the feature group expectation suite, surfacing a quality report and feature metrics in the Hopsworks UI." xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="fgexp-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/></marker></defs>

  <rect class="d-panel-ext" x="290" y="88" width="440" height="282" rx="12"/>
  <text class="d-cap d-cap-ext" x="510" y="392" text-anchor="middle">GREAT EXPECTATIONS</text>
  <rect class="d-panel-fs" x="770" y="88" width="210" height="282" rx="12"/>
  <text class="d-cap d-cap-fs" x="875" y="392" text-anchor="middle">HOPSWORKS UI</text>

  <rect class="d-box-ext" x="20" y="270" width="70" height="48" rx="8"/>
  <text class="d-t" x="55" y="299" text-anchor="middle">User</text>

  <rect class="d-box" x="110" y="140" width="130" height="200" rx="8"/>
  <text class="d-t" x="175" y="168" text-anchor="middle">HSFS</text>
  <text class="d-sub" x="175" y="222" text-anchor="middle" font-size="11">Apache Spark</text>
  <text class="d-sub" x="175" y="288" text-anchor="middle" font-size="11">Python</text>

  <rect class="d-box-own" x="330" y="20" width="360" height="48" rx="8"/>
  <text class="d-t" x="510" y="49" text-anchor="middle">Feature Group Expectation Suite</text>

  <rect class="d-box-own" x="330" y="120" width="160" height="64" rx="8"/>
  <text class="d-t" x="410" y="157" text-anchor="middle">Profiler</text>

  <rect class="d-box-own" x="540" y="120" width="160" height="64" rx="8"/>
  <text class="d-t" x="620" y="149" text-anchor="middle">Expectation</text>
  <text class="d-t" x="620" y="167" text-anchor="middle">Validation</text>

  <rect class="d-box" x="320" y="250" width="380" height="90" rx="8"/>
  <rect class="d-box" x="350" y="262" width="320" height="36" rx="6" fill="none" stroke-dasharray="4 3"/>
  <text class="d-t" x="510" y="285" text-anchor="middle">Metrics Computation</text>
  <text class="d-sub" x="510" y="325" text-anchor="middle" font-size="11">Pandas or Spark</text>

  <rect class="d-box-own" x="790" y="120" width="170" height="64" rx="8"/>
  <text class="d-t" x="875" y="149" text-anchor="middle">Feature Group</text>
  <text class="d-t" x="875" y="167" text-anchor="middle">Quality Report</text>

  <rect class="d-box-own" x="790" y="250" width="170" height="64" rx="8"/>
  <text class="d-t" x="875" y="287" text-anchor="middle">Feature Metrics</text>

  <path class="d-flow" d="M90 294 H110" marker-end="url(#fgexp-arrow)"/>
  <text class="d-sub" x="100" y="285" text-anchor="middle" font-size="11">fg.insert(df)</text>
  <path class="d-flow" d="M240 295 H320" marker-end="url(#fgexp-arrow)"/>
  <path class="d-flow" d="M410 250 V184" marker-end="url(#fgexp-arrow)"/>
  <path class="d-flow" d="M410 120 V68" marker-end="url(#fgexp-arrow)"/>
  <path class="d-flow" d="M620 120 V68" marker-end="url(#fgexp-arrow)"/>
  <path class="d-flow" d="M620 184 V250" marker-end="url(#fgexp-arrow)"/>
  <path class="d-flow" d="M700 152 H790" marker-end="url(#fgexp-arrow)"/>
  <path class="d-flow" d="M700 282 H790" marker-end="url(#fgexp-arrow)"/>
</svg>
</figure>

## Alerting

Hopsworks also supports alerts, that can be triggered when there are problems in your feature pipelines, for example, when a write fails due to an error or a failed expectation.
You can send alerts to different alerting endpoints, such as email or Slack, that can be configured in the Hopsworks UI.
For example, you can send a slack message if features being written to a feature group are missing some input data.
