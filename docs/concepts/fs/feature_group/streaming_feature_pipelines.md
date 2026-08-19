# Streaming Feature Pipelines

A streaming feature pipeline processes an unbounded stream of events and keeps features fresh in near real-time, instead of running on a schedule over a batch of data.
The same pipeline must also be able to run over historical data, to backfill a feature group when it is first created or after a schema change.
This backfill-and-incremental duality is a defining property of a feature pipeline, not an afterthought.

## Feature freshness

Feature freshness is the total time from when an event is first read by a feature pipeline to when the resulting feature is available to an inference pipeline.
For interactive, real-time systems it is often the freshness of a feature, not the latency of the model, that decides whether a prediction is useful.

<figure class="hops-diagram hops-viz">
<svg viewBox="0 0 1000 290" role="img" aria-label="Animated diagram of a streaming feature pipeline. Events arrive on an unbounded stream and fall into tumbling windows. As each window closes, its aggregate is upserted into a feature group in the online store and the row lights up with a fresh value. A sweep along the freshness band below measures the total time from event read to feature available to inference." xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="sf-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/>
    </marker>
  </defs>

  <text class="viz-label" x="24" y="28">Event stream</text>

  <text class="viz-meta" x="116" y="44" text-anchor="middle">tumbling window</text>
  <text class="viz-meta" x="316" y="44" text-anchor="middle">tumbling window</text>
  <text class="viz-meta" x="516" y="44" text-anchor="middle">tumbling window</text>
  <rect id="w1" class="viz-window" data-tone="data" x="24" y="52" width="184" height="64" rx="6"/>
  <rect id="w2" class="viz-window" data-tone="data" x="224" y="52" width="184" height="64" rx="6"/>
  <rect id="w3" class="viz-window" data-tone="data" x="424" y="52" width="184" height="64" rx="6"/>

  <path class="viz-edge" d="M24 140 H612" marker-end="url(#sf-arrow)"/>
  <text class="viz-meta" x="608" y="154" text-anchor="end">time</text>
  <g id="ev1" class="viz-fade" style="opacity:0">
    <path class="viz-tick" d="M48 140 V112 M76 140 V104 M104 140 V118 M132 140 V100 M160 140 V110 M188 140 V106"/>
  </g>
  <g id="ev2" class="viz-fade" style="opacity:0">
    <path class="viz-tick" d="M248 140 V108 M276 140 V116 M304 140 V102 M332 140 V112 M360 140 V106 M388 140 V110"/>
  </g>
  <g id="ev3" class="viz-fade" style="opacity:0">
    <path class="viz-tick" d="M448 140 V104 M476 140 V114 M504 140 V100 M532 140 V110 M560 140 V108 M588 140 V116"/>
  </g>

  <g transform="translate(89 120)">
    <g id="p1" class="viz-packet" data-tone="write" style="opacity:0">
      <rect width="54" height="18" rx="3"/>
      <text x="27" y="9" text-anchor="middle">upsert</text>
    </g>
  </g>
  <g transform="translate(289 120)">
    <g id="p2" class="viz-packet" data-tone="write" style="opacity:0">
      <rect width="54" height="18" rx="3"/>
      <text x="27" y="9" text-anchor="middle">upsert</text>
    </g>
  </g>
  <g transform="translate(489 120)">
    <g id="p3" class="viz-packet" data-tone="write" style="opacity:0">
      <rect width="54" height="18" rx="3"/>
      <text x="27" y="9" text-anchor="middle">upsert</text>
    </g>
  </g>

  <rect class="viz-kv-frame" x="660" y="40" width="316" height="130" rx="6"/>
  <rect class="viz-kv-header" x="660" y="40" width="316" height="26"/>
  <text class="viz-kv-title" x="672" y="57">Online store</text>
  <text class="viz-meta" x="964" y="57" text-anchor="end">feature group v1</text>
  <g id="row1" class="viz-kv-entry" data-tone="write">
    <rect class="viz-kv-cell" x="668" y="74" width="300" height="26" rx="3"/>
    <text class="viz-kv-key" x="676" y="91">avg_amt_5m</text>
    <text id="v1" class="viz-kv-val" x="960" y="91" text-anchor="end">–</text>
  </g>
  <g id="row2" class="viz-kv-entry" data-tone="write">
    <rect class="viz-kv-cell" x="668" y="104" width="300" height="26" rx="3"/>
    <text class="viz-kv-key" x="676" y="121">txn_cnt_1h</text>
    <text id="v2" class="viz-kv-val" x="960" y="121" text-anchor="end">–</text>
  </g>
  <g id="row3" class="viz-kv-entry" data-tone="write">
    <rect class="viz-kv-cell" x="668" y="134" width="300" height="26" rx="3"/>
    <text class="viz-kv-key" x="676" y="151">last_country</text>
    <text id="v3" class="viz-kv-val" x="960" y="151" text-anchor="end">–</text>
  </g>

  <text class="viz-label" x="24" y="226">Feature freshness</text>
  <text class="viz-meta" x="964" y="226" text-anchor="end">seconds, end to end</text>
  <rect class="viz-progress-track" x="80" y="244" width="820" height="4" rx="2"/>
  <rect id="ffill" class="viz-progress-fill" data-tone="accent" x="80" y="244" height="4" rx="2" style="width:0px"/>
  <circle id="fdot" class="viz-status-dot" data-tone="accent" cx="80" cy="246" r="5" style="opacity:0"/>
  <text class="viz-meta" x="80" y="270" text-anchor="middle">event read</text>
  <text class="viz-meta" x="900" y="270" text-anchor="middle">available to inference</text>
</svg>
<script type="application/json" data-viz-scene>
{
  "interval": 800,
  "loopDelay": 2400,
  "steps": [
    { "#ev1": {"opacity": 1} },
    { "#w1": {"state": "active"}, "$ms": 500 },
    { "#p1": {"opacity": 1}, "#w1": {"state": "visited"}, "$ms": 500 },
    { "#p1": {"x": 509, "y": -42}, "#fdot": {"opacity": 1}, "$ms": 900 },
    { "#row1": {"state": "active"}, "#p1": {"opacity": 0}, "#v1": {"text": "17.3"}, "#ffill": {"w": 820}, "#fdot": {"x": 820}, "$ms": 1100 },
    { "#row1": {"state": "visited"}, "#ev2": {"opacity": 1} },
    { "#w2": {"state": "active"}, "$ms": 500 },
    { "#p2": {"opacity": 1}, "#w2": {"state": "visited"}, "$ms": 500 },
    { "#p2": {"x": 309, "y": -12}, "$ms": 900 },
    { "#row2": {"state": "active"}, "#p2": {"opacity": 0}, "#v2": {"text": "42"} },
    { "#row2": {"state": "visited"}, "#ev3": {"opacity": 1} },
    { "#w3": {"state": "active"}, "$ms": 500 },
    { "#p3": {"opacity": 1}, "#w3": {"state": "visited"}, "$ms": 500 },
    { "#p3": {"x": 109, "y": 18}, "$ms": 900 },
    { "#row3": {"state": "active"}, "#p3": {"opacity": 0}, "#v3": {"text": "SE"} },
    { "#row3": {"state": "visited"} }
  ]
}
</script>
</figure>

## Windows

Streaming aggregations are computed over windows of the event stream:

- **Tumbling** windows are fixed-size and non-overlapping, so each event falls in exactly one window.
- **Hopping** windows are fixed-size but overlap, advancing by a hop smaller than the window.
- **Rolling** (sliding) windows are recomputed continuously as events arrive.

A watermark tells the pipeline how long to wait for late-arriving events before it closes a window and emits the aggregate.

## Streaming-native or hybrid

A streaming-native pipeline computes all features directly on the stream, a Kappa-style architecture.
A hybrid streaming-batch pipeline splits the work: a streaming job keeps the freshest features up to date while a batch job computes the heavier, less time-sensitive aggregations, a Lambda-style architecture.
Prefer streaming-native where you can, since a single code path is simpler to keep consistent than two.

A streaming feature pipeline can run in four operational modes: real-time processing of live events, stream replay, backfilling from historical data, and stream reprocessing after a logic change.
