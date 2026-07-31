# Streaming Feature Pipelines

A streaming feature pipeline processes an unbounded stream of events and keeps features fresh in near real-time, instead of running on a schedule over a batch of data.
The same pipeline must also be able to run over historical data, to backfill a feature group when it is first created or after a schema change.
This backfill-and-incremental duality is a defining property of a feature pipeline, not an afterthought.

## Feature freshness

Feature freshness is the total time from when an event is first read by a feature pipeline to when the resulting feature is available to an inference pipeline.
For interactive, real-time systems it is often the freshness of a feature, not the latency of the model, that decides whether a prediction is useful.

<figure class="hops-diagram">
<svg viewBox="0 0 1000 300" role="img" aria-label="A streaming feature pipeline reads an unbounded event stream, aggregates it over tumbling windows, and writes fresh features to the online store. Feature freshness is the total time from when an event is read to when its feature is available to an inference pipeline." xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="sf-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/>
    </marker>
  </defs>

  <text class="d-t d-cap d-cap-ext" x="22" y="36">Event stream</text>
  <rect class="d-panel-ext" x="16" y="44" width="600" height="104" rx="12"/>

  <rect class="d-box" x="40" y="58" width="176" height="60" rx="6" stroke-dasharray="4 3"/>
  <rect class="d-box" x="224" y="58" width="176" height="60" rx="6" stroke-dasharray="4 3"/>
  <rect class="d-box" x="408" y="58" width="176" height="60" rx="6" stroke-dasharray="4 3"/>
  <text class="d-t d-sub" x="128" y="52" text-anchor="middle">tumbling window</text>
  <text class="d-t d-sub" x="312" y="52" text-anchor="middle">tumbling window</text>
  <text class="d-t d-sub" x="496" y="52" text-anchor="middle">tumbling window</text>

  <path class="d-flow" d="M40 132 H600" marker-end="url(#sf-arrow)"/>
  <path class="d-flow" d="M60 132 V112 M84 132 V104 M108 132 V116 M132 132 V100 M156 132 V110 M180 132 V106 M244 132 V108 M268 132 V116 M292 132 V102 M316 132 V112 M340 132 V106 M364 132 V110 M428 132 V104 M452 132 V114 M476 132 V100 M500 132 V110 M524 132 V108 M548 132 V116"/>
  <text class="d-t d-sub" x="596" y="146" text-anchor="end">time</text>

  <path class="d-flow" d="M616 96 H700" marker-end="url(#sf-arrow)"/>
  <text class="d-t d-sub" x="658" y="88" text-anchor="middle">aggregate</text>
  <rect class="d-box-own" x="700" y="66" width="184" height="60" rx="8"/>
  <text class="d-t" x="792" y="92" text-anchor="middle">Online store</text>
  <text class="d-t d-sub" x="792" y="110" text-anchor="middle">fresh features</text>

  <text class="d-t d-cap" x="22" y="204">Feature freshness</text>
  <rect class="d-band" x="16" y="214" width="868" height="62" rx="10"/>
  <path class="d-flow" d="M92 245 H778" marker-start="url(#sf-arrow)" marker-end="url(#sf-arrow)"/>
  <text class="d-t d-sub" x="435" y="238" text-anchor="middle">total time from event read to feature available</text>
  <circle cx="80" cy="245" r="4" fill="#41b7dc"/>
  <text class="d-t d-sub" x="80" y="268" text-anchor="middle">event read</text>
  <circle cx="792" cy="245" r="4" fill="#21b182"/>
  <text class="d-t d-sub" x="792" y="268" text-anchor="middle">available to inference</text>
</svg>
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
