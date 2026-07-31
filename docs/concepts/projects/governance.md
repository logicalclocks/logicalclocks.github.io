# Projects and Governance

Hopsworks provides project-level multi-tenancy, a data mesh enabling technology.
Think of it as a GitHub repository for your teams and ML assets.
More specifically, a project is a sandbox for team members, ML assets (features, training data, models, vector index, model deployments), and optionally feature pipelines and training pipelines.
The ML assets can only be accessed by project members, and there is role-based access control (RBAC) for project members within a project.

<figure class="hops-diagram">
<svg viewBox="0 0 1000 580" role="img" aria-label="Two Hopsworks projects, a production project and a development project, each a sandbox holding the same ML assets, accessed by different team members and fed by a shared CI/CD system." xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="gov-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/></marker></defs>

  <rect class="d-box-ext" x="150" y="20" width="200" height="48" rx="8"/>
  <text class="d-t" x="250" y="49" text-anchor="middle">ML Engineers</text>

  <rect class="d-box-ext" x="430" y="20" width="140" height="48" rx="8"/>
  <text class="d-t" x="500" y="49" text-anchor="middle">CI/CD</text>

  <rect class="d-box-ext" x="580" y="14" width="340" height="60" rx="8"/>
  <text class="d-t" x="750" y="40" text-anchor="middle">Data Scientists, Data Engineers,</text>
  <text class="d-t" x="750" y="58" text-anchor="middle">ML Engineers</text>

  <path class="d-flow" d="M250 68 V150" marker-end="url(#gov-arrow)"/>
  <path class="d-flow" d="M750 74 V150" marker-end="url(#gov-arrow)"/>
  <path class="d-flow" d="M500 68 V110 H400 V150" marker-end="url(#gov-arrow)"/>
  <path class="d-flow" d="M500 68 V110 H600 V150" marker-end="url(#gov-arrow)"/>

  <rect class="d-panel-fs" x="40" y="150" width="420" height="410" rx="16"/>
  <text class="d-cap d-cap-fs" x="250" y="180" text-anchor="middle">Production</text>
  <text class="d-t" x="250" y="210" text-anchor="middle">ML assets</text>
  <rect class="d-box-own" x="130" y="228" width="240" height="42" rx="8"/>
  <text class="d-t" x="250" y="254" text-anchor="middle">Training Data</text>
  <rect class="d-box-own" x="130" y="282" width="240" height="42" rx="8"/>
  <text class="d-t" x="250" y="308" text-anchor="middle">Feature Store</text>
  <rect class="d-box-own" x="130" y="336" width="240" height="42" rx="8"/>
  <text class="d-t" x="250" y="362" text-anchor="middle">Model Registry</text>
  <rect class="d-box-own" x="130" y="390" width="240" height="42" rx="8"/>
  <text class="d-t" x="250" y="416" text-anchor="middle">Model Deployments</text>
  <rect class="d-box-own" x="130" y="444" width="240" height="52" rx="8"/>
  <text class="d-t" x="250" y="466" text-anchor="middle">Vector index</text>
  <text class="d-sub" x="250" y="484" text-anchor="middle">(OpenSearch Index)</text>

  <rect class="d-panel-fs" x="540" y="150" width="420" height="410" rx="16"/>
  <text class="d-cap d-cap-fs" x="750" y="180" text-anchor="middle">Development</text>
  <text class="d-t" x="750" y="210" text-anchor="middle">ML assets</text>
  <rect class="d-box-own" x="630" y="228" width="240" height="42" rx="8"/>
  <text class="d-t" x="750" y="254" text-anchor="middle">Training Data</text>
  <rect class="d-box-own" x="630" y="282" width="240" height="42" rx="8"/>
  <text class="d-t" x="750" y="308" text-anchor="middle">Feature Store</text>
  <rect class="d-box-own" x="630" y="336" width="240" height="42" rx="8"/>
  <text class="d-t" x="750" y="362" text-anchor="middle">Model Registry</text>
  <rect class="d-box-own" x="630" y="390" width="240" height="42" rx="8"/>
  <text class="d-t" x="750" y="416" text-anchor="middle">Model Deployments</text>
  <rect class="d-box-own" x="630" y="444" width="240" height="52" rx="8"/>
  <text class="d-t" x="750" y="466" text-anchor="middle">Vector index</text>
  <text class="d-sub" x="750" y="484" text-anchor="middle">(OpenSearch Index)</text>
</svg>
</figure>

## Dev/Staging/Prod for Data

Projects enable you to define development, staging, and even production projects on the same cluster.
Often, companies deploy production projects on dedicated clusters, but development projects and staging projects on a shared cluster.
This way, projects can be easily used to implement CI/CD workflows.

## Data Mesh of Feature Stores

Projects enable you to move beyond the traditional dev/staging/prod ownership model for data.
Different teams or lines of business can have their own private feature stores, you can mix them with a group-wide feature store, and feature stores can be securely shared between teams/organizations.
Effectively, you can have decentralized ownership of feature stores, with domain-specific projects, and each project managing its own feature pipelines.
Hopsworks provides data/feature sharing support between these self-service projects.

## Audit Logs with REST API

Hopsworks stores audit logs for all calls on its REST API in its file system, HopsFS.
The audit log can be used to analyze the historical usage of services by users.
