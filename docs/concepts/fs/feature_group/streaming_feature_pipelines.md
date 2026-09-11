# Streaming Feature Pipelines

A streaming feature pipeline processes an unbounded stream of events and keeps features fresh in near real-time, instead of running on a schedule over a batch of data.
The same pipeline must also be able to run over historical data, to backfill a feature group when it is first created or after a schema change.
This backfill-and-incremental duality is a defining property of a feature pipeline, not an afterthought.

## Feature freshness

Feature freshness is the total time from when an event is first read by a feature pipeline to when the resulting feature is available to an inference pipeline.
For interactive, real-time systems it is often the freshness of a feature, not the latency of the model, that decides whether a prediction is useful.

--8<-- "concepts/fs/feature_group/streaming_feature_pipelines/freshness.html"

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
