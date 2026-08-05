# CI/CD Support

You can setup traditional development, staging, and production environment in Hopsworks using Projects.
A project enables you provide access control for the different environments - just like a GitHub repository, owners of projects can add and remove members of projects and assign different roles to project members - the "data owner" role can write to feature store, while a "data scientist" can only read from the feature store and create training data.

## Dev, Staging, Prod

You can create dev, staging, and prod projects - either on the same cluster, but mostly commonly, with production on its own cluster:

<figure class="hops-diagram">
<svg viewBox="0 0 1000 370" role="img" aria-label="Production, main, and development git branches each write to their own Hopsworks feature store, and features are promoted upward from dev to staging to production." xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="dsp-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/></marker></defs>
  <rect class="d-panel-fs" x="620" y="30" width="360" height="320" rx="12"/>
  <text class="d-cap d-cap-fs" x="800" y="22" text-anchor="middle">Hopsworks</text>
  <rect class="d-box" x="40" y="50" width="380" height="64" rx="8"/>
  <text class="d-t" x="230" y="88" text-anchor="middle">Production Branch</text>
  <rect class="d-box" x="40" y="160" width="380" height="64" rx="8"/>
  <text class="d-t" x="230" y="198" text-anchor="middle">Main Branch</text>
  <rect class="d-box" x="40" y="270" width="380" height="64" rx="8"/>
  <text class="d-t" x="230" y="308" text-anchor="middle">Development Branch</text>
  <rect class="d-box-own" x="650" y="50" width="290" height="64" rx="8"/>
  <text class="d-t" x="795" y="78" text-anchor="middle">Production</text>
  <text class="d-t" x="795" y="98" text-anchor="middle">Feature Store</text>
  <rect class="d-box-own" x="650" y="160" width="290" height="64" rx="8"/>
  <text class="d-t" x="795" y="188" text-anchor="middle">Staging</text>
  <text class="d-t" x="795" y="208" text-anchor="middle">Feature Store</text>
  <rect class="d-box-own" x="650" y="270" width="290" height="64" rx="8"/>
  <text class="d-t" x="795" y="298" text-anchor="middle">Dev</text>
  <text class="d-t" x="795" y="318" text-anchor="middle">Feature Store</text>
  <path class="d-flow" d="M420 82 H650" marker-end="url(#dsp-arrow)"/>
  <path class="d-flow" d="M420 192 H650" marker-end="url(#dsp-arrow)"/>
  <path class="d-flow" d="M420 302 H650" marker-end="url(#dsp-arrow)"/>
  <path class="d-flow" d="M795 270 V226" marker-end="url(#dsp-arrow)"/>
  <path class="d-flow" d="M795 160 V116" marker-end="url(#dsp-arrow)"/>
</svg>
</figure>

## Versioning

Automated promotion across dev, staging, and prod relies on every ML asset being versioned.
Hopsworks versions feature groups, feature views, training data, and models, while deployments stay mutable behind the deployment API.
See [Versioning](../fs/feature_group/versioning.md) for what is versioned and how.

## Pytest for feature logic and feature pipeline tests

Pytest and Great Expectations can be used for testing feature pipelines.
Pytest is used to test feature logic and for end-to-end feature pipeline tests, while Great Expectations is used for data validation tests.
Here, we can see how a feature pipeline test uses sample data to compute features and validate they have been written successfully, first to a development feature store, and then they can be pushed to a staging feature store, before finally being promoted to production.
<figure class="hops-diagram">
<svg viewBox="0 0 1000 300" role="img" aria-label="A pull request triggers Jenkins PyTest on the main branch to run unit and end-to-end tests, compute features from subsampled data, validate them, and write to the Hopsworks staging feature store." xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="fpt-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/></marker></defs>
  <rect class="d-panel-ext" x="250" y="40" width="530" height="230" rx="12"/>
  <text class="d-cap d-cap-ext" x="515" y="32" text-anchor="middle">Main Branch</text>
  <rect class="d-panel-fs" x="810" y="40" width="170" height="230" rx="12"/>
  <text class="d-cap d-cap-fs" x="895" y="32" text-anchor="middle">Hopsworks</text>
  <text class="d-sub" x="105" y="72" text-anchor="middle">Pull Request Trigger</text>
  <rect class="d-box-ext" x="30" y="90" width="150" height="90" rx="8"/>
  <text class="d-t" x="105" y="130" text-anchor="middle">Jenkins</text>
  <text class="d-sub" x="105" y="150" text-anchor="middle">PyTest</text>
  <rect class="d-box" x="300" y="95" width="130" height="42" rx="6"/>
  <text class="d-t" x="365" y="121" text-anchor="middle">A.unit-test</text>
  <rect class="d-box" x="300" y="153" width="130" height="42" rx="6"/>
  <text class="d-t" x="365" y="179" text-anchor="middle">B.e2e-test</text>
  <rect class="d-box" x="480" y="110" width="120" height="52" rx="6"/>
  <text class="d-t" x="540" y="132" text-anchor="middle">Feature</text>
  <text class="d-t" x="540" y="150" text-anchor="middle">engineering</text>
  <rect class="d-box" x="630" y="110" width="120" height="52" rx="6"/>
  <text class="d-t" x="690" y="132" text-anchor="middle">Data Validation</text>
  <text class="d-t" x="690" y="150" text-anchor="middle">test</text>
  <rect class="d-box" x="480" y="200" width="120" height="46" rx="6"/>
  <text class="d-t" x="540" y="219" text-anchor="middle">Subsampled</text>
  <text class="d-t" x="540" y="237" text-anchor="middle">Data</text>
  <rect class="d-box-own" x="830" y="105" width="130" height="64" rx="8"/>
  <text class="d-t" x="895" y="133" text-anchor="middle">Staging</text>
  <text class="d-t" x="895" y="153" text-anchor="middle">Feature Store</text>
  <path class="d-flow" d="M180 135 H250" marker-end="url(#fpt-arrow)"/>
  <path class="d-flow" d="M430 116 C455 116 455 136 480 136" marker-end="url(#fpt-arrow)"/>
  <path class="d-flow" d="M430 174 C455 174 455 136 480 136" marker-end="url(#fpt-arrow)"/>
  <path class="d-flow" d="M540 162 V200"/>
  <path class="d-flow" d="M600 136 H630" marker-end="url(#fpt-arrow)"/>
  <path class="d-flow" d="M750 136 H830" marker-end="url(#fpt-arrow)"/>
</svg>
</figure>
