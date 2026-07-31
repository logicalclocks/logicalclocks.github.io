# External Feature Groups

External feature groups are offline feature groups where their data is stored in an external table.
An external table requires a data source, defined with the [Connector API](write_apis.md#connector-api) (or more typically in the user interface), to enable Hopsworks to retrieve data from the external table.
An external feature group doesn't allow for offline data ingestion or modification; instead, it includes a user-defined SQL string for retrieving data.
You can also perform SQL operations, including projections, aggregations, and so on.
The SQL query is executed on-demand when Hopsworks retrieves data from the external Feature Group, for example, when creating training data using features in the external table.

In the image below, we can see that Hopsworks currently supports a large number of data sources, including any JDBC-enabled source, Snowflake, Data Lake, Redshift, BigQuery, Databricks Unity Catalog (Delta tables on Databricks on AWS only), S3, ADLS, GCS, SQL, and Kafka.

<figure class="hops-diagram">
<svg viewBox="0 0 1000 500" role="img" aria-label="External data sources connect through the Hopsworks Connector API in HSFS to an external feature group in the offline feature store." xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="fg-conn-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/></marker></defs>
  <rect class="d-panel-ext" x="30" y="44" width="300" height="422" rx="14"/>
  <text class="d-cap d-cap-ext" x="180" y="74" text-anchor="middle">Data sources</text>
  <rect class="d-box-ext" x="52" y="92" width="256" height="26" rx="6"/>
  <text class="d-t" x="180" y="109" text-anchor="middle">JDBC</text>
  <rect class="d-box-ext" x="52" y="125" width="256" height="26" rx="6"/>
  <text class="d-t" x="180" y="142" text-anchor="middle">Snowflake</text>
  <rect class="d-box-ext" x="52" y="158" width="256" height="26" rx="6"/>
  <text class="d-t" x="180" y="175" text-anchor="middle">Data Lake</text>
  <rect class="d-box-ext" x="52" y="191" width="256" height="26" rx="6"/>
  <text class="d-t" x="180" y="208" text-anchor="middle">Redshift</text>
  <rect class="d-box-ext" x="52" y="224" width="256" height="26" rx="6"/>
  <text class="d-t" x="180" y="241" text-anchor="middle">BigQuery</text>
  <rect class="d-box-ext" x="52" y="257" width="256" height="26" rx="6"/>
  <text class="d-t" x="180" y="274" text-anchor="middle">Databricks Unity Catalog</text>
  <rect class="d-box-ext" x="52" y="290" width="256" height="26" rx="6"/>
  <text class="d-t" x="180" y="307" text-anchor="middle">S3</text>
  <rect class="d-box-ext" x="52" y="323" width="256" height="26" rx="6"/>
  <text class="d-t" x="180" y="340" text-anchor="middle">ADLS</text>
  <rect class="d-box-ext" x="52" y="356" width="256" height="26" rx="6"/>
  <text class="d-t" x="180" y="373" text-anchor="middle">GCS</text>
  <rect class="d-box-ext" x="52" y="389" width="256" height="26" rx="6"/>
  <text class="d-t" x="180" y="406" text-anchor="middle">SQL</text>
  <rect class="d-box-ext" x="52" y="422" width="256" height="26" rx="6"/>
  <text class="d-t" x="180" y="439" text-anchor="middle">Kafka</text>
  <path class="d-flow" d="M330 138 C 400 138 400 256 460 256" marker-end="url(#fg-conn-arrow)"/>
  <path class="d-flow" d="M330 256 H460" marker-end="url(#fg-conn-arrow)"/>
  <path class="d-flow" d="M330 374 C 400 374 400 256 460 256" marker-end="url(#fg-conn-arrow)"/>
  <rect class="d-box" x="430" y="185" width="250" height="150" rx="10"/>
  <text class="d-sub" x="555" y="210" text-anchor="middle">HSFS</text>
  <rect class="d-api" x="460" y="228" width="190" height="62" rx="8"/>
  <text class="d-t" x="555" y="264" text-anchor="middle">Connector API</text>
  <path class="d-flow" d="M680 260 H752" marker-end="url(#fg-conn-arrow)"/>
  <rect class="d-panel-fs" x="730" y="185" width="240" height="150" rx="12"/>
  <text class="d-cap d-cap-fs" x="850" y="212" text-anchor="middle">Offline feature store</text>
  <rect class="d-box-own" x="752" y="232" width="196" height="58" rx="8"/>
  <text class="d-t" x="850" y="266" text-anchor="middle">External feature group</text>
</svg>
</figure>
