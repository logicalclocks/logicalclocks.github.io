# Write APIs

You write to feature groups, and read from feature views.

There are 3 APIs for writing to feature groups, as shown in the table below:

| | Stream API | Batch API | Connector API |
| --- | --- | --- | --- |
| Python | X | - | - |
| Spark | X | X | - |
| Flink | X | - | - |
| External Table | - | - | X |

## Stream API

The Stream API is the only API for Python and Flink clients, and is
the preferred API for Spark, as it ensures consistent features between offline and online feature stores.
The Stream API first writes data to be ingested to a Kafka topic, and then Hopsworks ensures that the data is synchronized to the Online and Offline Feature Groups through the OnlineFS service and Hudi DeltaStreamer jobs, respectively.
The Kafka transport delivers at-least-once, and Hopsworks upgrades this to exactly-once through idempotent writes to the online feature group (only the latest values of features are stored there, and duplicates in Kafka only cause idempotent updates) and duplicate removal by Apache Hudi for the offline feature group.

<figure class="hops-diagram">
<svg viewBox="0 0 1000 440" role="img" aria-label="The Stream API sends fg.insert data through the HSFS clients into Kafka, which writes to the online feature store on RonDB via the Online FS path and to the offline feature store on Hudi via the Delta Streamer path under a common schema." xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="stream-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/></marker></defs>
  <text class="d-sub" x="557" y="30" text-anchor="middle">Common Schema</text>
  <path class="d-flow" d="M300 42 H815" stroke-dasharray="2 6"/>
  <path class="d-flow" d="M300 42 V90" stroke-dasharray="2 6"/>
  <path class="d-flow" d="M520 42 V222" stroke-dasharray="2 6"/>
  <path class="d-flow" d="M815 42 V90" stroke-dasharray="2 6"/>
  <path class="d-flow" d="M815 210 V270" stroke-dasharray="2 6"/>
  <rect class="d-box-ext" x="20" y="222" width="110" height="56" rx="8"/>
  <text class="d-t" x="75" y="248" text-anchor="middle">User /</text>
  <text class="d-t" x="75" y="266" text-anchor="middle">Application</text>
  <rect class="d-box" x="210" y="90" width="180" height="225" rx="10"/>
  <text class="d-t" x="300" y="115" text-anchor="middle">HSFS</text>
  <rect class="d-box" x="235" y="132" width="130" height="32" rx="6"/>
  <text class="d-t" x="300" y="153" text-anchor="middle">pandas</text>
  <rect class="d-box" x="235" y="176" width="130" height="32" rx="6"/>
  <text class="d-t" x="300" y="197" text-anchor="middle">Spark</text>
  <rect class="d-box" x="235" y="220" width="130" height="32" rx="6"/>
  <text class="d-sub" x="300" y="240" text-anchor="middle">Spark Streaming</text>
  <rect class="d-box" x="235" y="264" width="130" height="32" rx="6"/>
  <text class="d-t" x="300" y="285" text-anchor="middle">Python</text>
  <rect class="d-box" x="460" y="222" width="120" height="56" rx="8"/>
  <text class="d-t" x="520" y="254" text-anchor="middle">Kafka</text>
  <rect class="d-panel-fs" x="750" y="90" width="230" height="120" rx="12"/>
  <text class="d-cap d-cap-fs" x="865" y="112" text-anchor="middle">ONLINE FEATURE STORE</text>
  <rect class="d-box-own" x="800" y="130" width="130" height="54" rx="8"/>
  <text class="d-t" x="865" y="161" text-anchor="middle">RonDB</text>
  <rect class="d-panel-fs" x="750" y="270" width="230" height="140" rx="12"/>
  <text class="d-cap d-cap-fs" x="865" y="292" text-anchor="middle">OFFLINE FEATURE STORE</text>
  <rect class="d-box-own" x="790" y="312" width="150" height="64" rx="8"/>
  <text class="d-t" x="865" y="342" text-anchor="middle">Hudi</text>
  <text class="d-sub" x="865" y="362" text-anchor="middle">(S3, ADLS, GCS, HopsFS)</text>
  <text class="d-sub" x="170" y="242" text-anchor="middle">fg.insert(df)</text>
  <path class="d-flow" d="M130 250 H210" marker-end="url(#stream-arrow)"/>
  <path class="d-flow" d="M390 250 H460" marker-end="url(#stream-arrow)"/>
  <path class="d-flow" d="M580 250 C665 250 665 157 750 157" marker-end="url(#stream-arrow)"/>
  <path class="d-flow" d="M580 250 C665 250 665 344 750 344" marker-end="url(#stream-arrow)"/>
  <text class="d-sub" x="665" y="178" text-anchor="middle">Online FS</text>
  <text class="d-sub" x="665" y="192" text-anchor="middle">&lt;at-most-once&gt;</text>
  <text class="d-sub" x="665" y="318" text-anchor="middle">Delta Streamer</text>
  <text class="d-sub" x="665" y="332" text-anchor="middle">&lt;at-most-once&gt;</text>
</svg>
</figure>

## Batch API

For very large updates to feature groups, such as when you are backfilling large amounts of data to an offline feature group, it is often preferential to write directly to the Hudi tables in Hopsworks, instead of via Kafka - thus reducing write amplification.
Spark clients can write directly to Hudi tables on Hopsworks with Hopsworks libraries and certificates using a HDFS API.
This requires network connectivity between the Spark clients and the datanodes in Hopsworks.

<figure class="hops-diagram">
<svg viewBox="0 0 1000 460" role="img" aria-label="The Batch API sends fg.insert data through the Spark client in HSFS, routing the online path through Kafka to the online feature store on RonDB and writing large offline updates directly via HDFS to the offline feature store on Hudi under a common schema." xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="batch-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/></marker></defs>
  <text class="d-sub" x="557" y="30" text-anchor="middle">Common Schema</text>
  <path class="d-flow" d="M300 42 H815" stroke-dasharray="2 6"/>
  <path class="d-flow" d="M300 42 V150" stroke-dasharray="2 6"/>
  <path class="d-flow" d="M520 42 V172" stroke-dasharray="2 6"/>
  <path class="d-flow" d="M815 42 V90" stroke-dasharray="2 6"/>
  <path class="d-flow" d="M815 210 V300" stroke-dasharray="2 6"/>
  <rect class="d-box-ext" x="20" y="227" width="110" height="56" rx="8"/>
  <text class="d-t" x="75" y="253" text-anchor="middle">User /</text>
  <text class="d-t" x="75" y="271" text-anchor="middle">Application</text>
  <rect class="d-box" x="210" y="150" width="180" height="210" rx="10"/>
  <text class="d-t" x="300" y="180" text-anchor="middle">HSFS</text>
  <rect class="d-box" x="235" y="235" width="130" height="60" rx="8"/>
  <text class="d-t" x="300" y="270" text-anchor="middle">Spark</text>
  <rect class="d-box" x="460" y="172" width="120" height="56" rx="8"/>
  <text class="d-t" x="520" y="204" text-anchor="middle">Kafka</text>
  <rect class="d-panel-fs" x="750" y="90" width="230" height="120" rx="12"/>
  <text class="d-cap d-cap-fs" x="865" y="112" text-anchor="middle">ONLINE FEATURE STORE</text>
  <rect class="d-box-own" x="800" y="130" width="130" height="54" rx="8"/>
  <text class="d-t" x="865" y="161" text-anchor="middle">RonDB</text>
  <rect class="d-panel-fs" x="750" y="300" width="230" height="130" rx="12"/>
  <text class="d-cap d-cap-fs" x="865" y="322" text-anchor="middle">OFFLINE FEATURE STORE</text>
  <rect class="d-box-own" x="790" y="342" width="150" height="64" rx="8"/>
  <text class="d-t" x="865" y="372" text-anchor="middle">Hudi</text>
  <text class="d-sub" x="865" y="392" text-anchor="middle">(S3, ADLS, GCS, HopsFS)</text>
  <text class="d-sub" x="170" y="247" text-anchor="middle">fg.insert(df)</text>
  <path class="d-flow" d="M130 255 H210" marker-end="url(#batch-arrow)"/>
  <path class="d-flow" d="M390 210 C425 210 425 200 460 200" marker-end="url(#batch-arrow)"/>
  <path class="d-flow" d="M580 200 C665 200 690 157 750 157" marker-end="url(#batch-arrow)"/>
  <path class="d-flow" d="M390 320 C560 320 590 365 750 365" marker-end="url(#batch-arrow)"/>
  <text class="d-sub" x="665" y="178" text-anchor="middle">Online FS</text>
  <text class="d-sub" x="665" y="192" text-anchor="middle">&lt;at-most-once&gt;</text>
  <text class="d-sub" x="618" y="334" text-anchor="middle">HDFS</text>
</svg>
</figure>

## Connector API

Hopsworks supports external tables as feature groups.
You can mount a table from an external database as an offline feature group using the Connector API: you create an external table using the connector, without ingesting the data into Hopsworks.
This enables you to use features from your external data source (Snowflake, Redshift, Delta Lake, etc) as you would any feature in an offline feature group in Hopsworks.
You can, for example, join features from different feature groups (external or not) together to create feature views and training data for models.

See [External Feature Groups](external_fg.md) for the full list of supported data sources.
