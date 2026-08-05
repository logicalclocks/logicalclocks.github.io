# Data Storage and Sharing

Every project in Hopsworks has its own private assets:

- a Feature Store (including both Online and Offline Stores)
- a Filesystem subtree (all directory and files under /Projects/<project_name>/)
- a Model Registry
- Model Deployments
- Kafka topics
- OpenSearch indexes (including kNN indexes, the vector index)
- a Hive Database

Access control to these assets is controlled using project membership ACLs (access-control lists).
Users in a project who have a *Data Owner* role have read/write access to these assets.  Users in a project who have a *Data Scientist* role have mostly read-only access to these assets, with the exception of the ability to write to well-known directories (Resources, Jupyter, Logs).

However, it is often desirable to share assets between projects, with read-only, read/write privileges, and to restrict the privileges to specific role (e.g., Data Owners) in the target project.
In Hopsworks, you can explicitly share assets between projects without copying the assets.
Sharing is managed by ACLs in Hopsworks, see example below:
<figure class="hops-diagram">
<svg viewBox="0 0 1000 560" role="img" aria-label="Two Hopsworks projects, Production and Development, each holding its own ML assets, where the Production feature store is shared read-only with Development and CI/CD writes to both." xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="share-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/></marker></defs>

  <!-- Actors -->
  <rect class="d-box-ext" x="100" y="20" width="200" height="50" rx="8"/>
  <text class="d-t" x="200" y="49" text-anchor="middle">ML Engineers</text>
  <rect class="d-box-ext" x="420" y="20" width="160" height="50" rx="8"/>
  <text class="d-t" x="500" y="49" text-anchor="middle">CI/CD</text>
  <rect class="d-box-ext" x="650" y="15" width="310" height="60" rx="8"/>
  <text class="d-t" x="805" y="42" text-anchor="middle">Data Scientists, Data Engineers,</text>
  <text class="d-t" x="805" y="60" text-anchor="middle">ML Engineers</text>

  <!-- Actor connectors -->
  <path class="d-flow" d="M200 70 V125" marker-end="url(#share-arrow)"/>
  <path class="d-flow" d="M500 70 V98 H255 V125" marker-end="url(#share-arrow)"/>
  <path class="d-flow" d="M500 70 V98 H745 V125" marker-end="url(#share-arrow)"/>
  <path class="d-flow" d="M805 75 V125" marker-end="url(#share-arrow)"/>

  <!-- Project panels -->
  <rect class="d-panel-fs" x="40" y="130" width="430" height="400" rx="14"/>
  <rect class="d-panel-fs" x="530" y="130" width="430" height="400" rx="14"/>
  <text class="d-cap d-cap-fs" x="255" y="118" text-anchor="middle">Production</text>
  <text class="d-cap d-cap-fs" x="745" y="118" text-anchor="middle">Development</text>
  <text class="d-sub" x="255" y="182" text-anchor="middle" font-size="11">ML ASSETS</text>
  <text class="d-sub" x="745" y="182" text-anchor="middle" font-size="11">ML ASSETS</text>

  <!-- Production assets -->
  <rect class="d-box-own" x="90" y="205" width="330" height="46" rx="8"/>
  <text class="d-t" x="255" y="234" text-anchor="middle">Training Data</text>
  <rect class="d-box-own" x="90" y="263" width="330" height="46" rx="8"/>
  <text class="d-t" x="255" y="292" text-anchor="middle">Feature Store</text>
  <rect class="d-box-own" x="90" y="321" width="330" height="46" rx="8"/>
  <text class="d-t" x="255" y="350" text-anchor="middle">Model Registry</text>
  <rect class="d-box-own" x="90" y="379" width="330" height="46" rx="8"/>
  <text class="d-t" x="255" y="408" text-anchor="middle">Model Deployments</text>
  <rect class="d-box-own" x="90" y="437" width="330" height="52" rx="8"/>
  <text class="d-t" x="255" y="459" text-anchor="middle">Vector index</text>
  <text class="d-sub" x="255" y="477" text-anchor="middle" font-size="11">(OpenSearch Index)</text>

  <!-- Development assets -->
  <rect class="d-box-own" x="580" y="205" width="330" height="46" rx="8"/>
  <text class="d-t" x="745" y="234" text-anchor="middle">Training Data</text>
  <rect class="d-box-own" x="580" y="263" width="330" height="46" rx="8"/>
  <text class="d-t" x="745" y="292" text-anchor="middle">Feature Store</text>
  <rect class="d-box-own" x="580" y="321" width="330" height="46" rx="8"/>
  <text class="d-t" x="745" y="350" text-anchor="middle">Model Registry</text>
  <rect class="d-box-own" x="580" y="379" width="330" height="46" rx="8"/>
  <text class="d-t" x="745" y="408" text-anchor="middle">Model Deployments</text>
  <rect class="d-box-own" x="580" y="437" width="330" height="52" rx="8"/>
  <text class="d-t" x="745" y="459" text-anchor="middle">Vector index</text>
  <text class="d-sub" x="745" y="477" text-anchor="middle" font-size="11">(OpenSearch Index)</text>

  <!-- Shared read-only feature store -->
  <text class="d-sub" x="500" y="279" text-anchor="middle" font-size="11">shared read-only</text>
  <path class="d-flow" d="M420 291 H580" marker-end="url(#share-arrow)"/>
</svg>
</figure>
