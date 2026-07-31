# Development Inside Hopsworks


Hopsworks provides a complete self-service development environment for feature engineering and model training.
You can develop programs as Jupyter notebooks or jobs, customize the bundled FTI (feature, training and inference pipeline) python environments, you can manage your source code with Git, and you can orchestrate jobs with Airflow.

<figure class="hops-diagram">
<svg viewBox="0 0 1000 600" role="img" aria-label="Developers reach Hopsworks from remote clients, local IDEs, and CI/CD, and use its built-in library management, source control, notebooks, jobs, workflows, and logging and monitoring." xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="dev-inside-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/></marker></defs>

  <rect class="d-panel-fs" x="290" y="100" width="690" height="470" rx="16"/>
  <text class="d-cap d-cap-fs" x="635" y="88" text-anchor="middle">Development and Jobs with Hopsworks</text>

  <rect class="d-box-ext" x="20" y="135" width="165" height="90" rx="8"/>
  <text class="d-t" x="102" y="185" text-anchor="middle">User</text>
  <rect class="d-box-ext" x="20" y="280" width="165" height="90" rx="8"/>
  <text class="d-t" x="102" y="330" text-anchor="middle">PyCharm / IntelliJ</text>
  <rect class="d-box-ext" x="20" y="425" width="165" height="90" rx="8"/>
  <text class="d-t" x="102" y="463" text-anchor="middle">CI/CD</text>
  <text class="d-sub" x="102" y="485" text-anchor="middle">GitHub Actions, Jenkins</text>

  <path class="d-flow" d="M185 180 H290" marker-end="url(#dev-inside-arrow)"/>
  <text class="d-sub" x="237" y="171" text-anchor="middle">Develop Remote,</text>
  <text class="d-sub" x="237" y="185" text-anchor="middle">Run Remote</text>
  <path class="d-flow" d="M185 325 H290" marker-end="url(#dev-inside-arrow)"/>
  <text class="d-sub" x="237" y="316" text-anchor="middle">Develop Local,</text>
  <text class="d-sub" x="237" y="330" text-anchor="middle">Run Remote</text>
  <path class="d-flow" d="M185 470 H290" marker-end="url(#dev-inside-arrow)"/>
  <text class="d-sub" x="237" y="466" text-anchor="middle">CI/CD Pipelines</text>

  <rect class="d-box-own" x="310" y="135" width="270" height="90" rx="8"/>
  <text class="d-t" x="445" y="173" text-anchor="middle">Install Libraries</text>
  <text class="d-sub" x="445" y="195" text-anchor="middle">Conda, PyPI, Docker</text>
  <rect class="d-box-own" x="710" y="135" width="255" height="90" rx="8"/>
  <text class="d-t" x="837" y="173" text-anchor="middle">Source Code Control</text>
  <text class="d-sub" x="837" y="195" text-anchor="middle">GitHub, GitLab, Bitbucket</text>

  <rect class="d-api" x="310" y="280" width="270" height="90" rx="8"/>
  <text class="d-t" x="445" y="318" text-anchor="middle">Jobs</text>
  <text class="d-sub" x="445" y="340" text-anchor="middle">Python, Spark, Flink</text>
  <rect class="d-box-own" x="710" y="280" width="255" height="90" rx="8"/>
  <text class="d-t" x="837" y="318" text-anchor="middle">Notebooks</text>
  <text class="d-sub" x="837" y="340" text-anchor="middle">Jupyter</text>

  <rect class="d-box-own" x="310" y="425" width="270" height="90" rx="8"/>
  <text class="d-t" x="445" y="463" text-anchor="middle">Workflows</text>
  <text class="d-sub" x="445" y="485" text-anchor="middle">Apache Airflow</text>
  <rect class="d-box-own" x="710" y="425" width="255" height="90" rx="8"/>
  <text class="d-t" x="837" y="463" text-anchor="middle">Logs &amp; Monitoring</text>
  <text class="d-sub" x="837" y="485" text-anchor="middle">OpenSearch, Grafana, Prometheus</text>

  <path class="d-flow" d="M710 325 H580" marker-end="url(#dev-inside-arrow)"/>
  <text class="d-sub" x="645" y="318" text-anchor="middle">Notebook-as-Job</text>
  <path class="d-flow" d="M445 425 V370" marker-end="url(#dev-inside-arrow)"/>
  <text class="d-sub" x="518" y="402" text-anchor="middle">orchestrate</text>
  <path class="d-flow" d="M500 370 L760 425" stroke-dasharray="5 4"/>
</svg>
</figure>

## Jupyter Notebooks

Hopsworks provides a Jupyter notebook development environment for programs written in Python, Spark, Flink, and SparkSQL.
You can also develop in your IDE (PyCharm, IntelliJ, etc), test locally, and then run your programs as Jobs in Hopsworks.
Jupyter notebooks can also be run as Jobs.

## Source Code Control

Hopsworks provides source code control support using Git (GitHub, GitLab or BitBucket).
You can securely check out code into your project and commit and push updates to your code to your source code repository.

## FTI Pipeline Environments

Hopsworks postulates that building ML systems following the FTI pipeline architecture is best practice.
This architecture consists of three independently developed and operated ML pipelines:

- Feature pipeline: takes as input raw data that it transforms into features (and labels)
- Training pipeline: takes as input features (and labels) and outputs a trained model
- Inference pipeline: takes new feature data and a trained model and makes predictions

In order to facilitate the development of these pipelines Hopsworks bundles several python environments containing necessary dependencies.
Each of these environments may then also be customized further by cloning it and installing additional dependencies from PyPi, Conda channels, Wheel files, GitHub repos or a custom Dockerfile.
Internal compute such as Jobs and Jupyter is run in one of these environments and changes are applied transparently when you install new libraries using our APIs.
That is, there is no need to write a Dockerfile, users install libraries directly in one or more of the environments.
You can setup custom development and production environments by creating separate projects or creating multiple clones of an environment within the same project.

## Jobs

In Hopsworks, a Job is a schedulable program that is allocated compute and memory resources.
You can run a Job in Hopsworks:

- From the UI
- Programmatically with the Hopsworks SDK (Python, Java) or REST API
- From Airflow programs (either inside our outside Hopsworks)
- From your IDE using a plugin ([PyCharm/IntelliJ plugin](https://plugins.jetbrains.com/plugin/15537-hopsworks))

## Orchestration

Airflow comes out-of-the box with Hopsworks, but you can also use an external Airflow cluster (with the Hopsworks Job operator) if you have one.
Airflow can be used to schedule the execution of Jobs, individually or as part of Airflow DAGs.
