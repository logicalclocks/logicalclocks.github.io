# Model Training

A training pipeline is a program that orchestrates the training of a machine learning model, reading features and labels from the feature store as training data.
Hopsworks supports running model training pipelines on any Python environment, whether on an external Python client or on a Hopsworks cluster.
The outputs of a training pipeline are typically experiment results, including logs, and possibly a trained model.
You can plugin your own experimentation tracking platform or model registry, or you can use Hopsworks.

A training pipeline typically runs five steps: select a feature view and a training dataset version, train the model, evaluate it, validate it, and register it in the model registry if it passes.

## Evaluation and validation

Model evaluation and model validation are not the same thing.
Evaluation measures the model's performance on a held-out test set, using metrics such as accuracy or AUC.
Validation is a pass/fail gate: the model is run against evaluation data, including bias slices of the holdout built with feature-view filters and training helper columns (a column such as gender used to slice results but dropped before training), and only a model that passes is registered.
The output of validation is a model validation scorecard, and it is what decides whether the model reaches the registry.

## Training Pipelines on Hopsworks

If you train models with Hopsworks, you can setup CI/CD pipelines as shown below, where the experiments are tracked by Hopsworks, and any model created is published to a model registry.
Each project has its own private model registry, so when you are working in a development project, you typically publish models to your project's private development registry, and if all model validation tests pass, and the model performance is good enough, the same training pipeline can be submitted via a CI/CD pipeline (e.g., GitHub push request) to a staging project, and the same procedure can be repeated to push the training pipeline to a production project.

<figure class="hops-diagram">
<svg viewBox="0 0 1000 516" role="img" aria-label="Two CI/CD training pipelines, a main branch and a development branch, each running unit and end-to-end tests before model training and validation against training data and evaluation sets, publishing to a Hopsworks experiment tracking and model registry." xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="tp-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/></marker></defs>

  <!-- Hopsworks panel (owned registries, both rows) -->
  <rect class="d-panel-fs" x="768" y="58" width="214" height="356" rx="12"/>
  <text class="d-cap d-cap-fs" x="875" y="80" text-anchor="middle">Hopsworks</text>

  <!-- ===== MAIN BRANCH (row 1, center y=120) ===== -->
  <rect class="d-band" x="195" y="54" width="525" height="132" rx="10"/>
  <text class="d-cap" x="212" y="76">Main Branch</text>

  <text class="d-sub" x="95" y="76" text-anchor="middle">Pull Request Trigger</text>
  <rect class="d-box-ext" x="25" y="93" width="140" height="54" rx="8"/>
  <text class="d-t" x="95" y="118" text-anchor="middle">Jenkins</text>
  <text class="d-sub" x="95" y="134" text-anchor="middle">PyTest</text>

  <rect class="d-box" x="212" y="88" width="128" height="26" rx="6"/>
  <text class="d-t" x="276" y="105" text-anchor="middle">A.unit-test</text>
  <rect class="d-box" x="212" y="124" width="128" height="26" rx="6"/>
  <text class="d-t" x="276" y="141" text-anchor="middle">B.e2e-test</text>

  <rect class="d-box" x="372" y="93" width="140" height="54" rx="8"/>
  <text class="d-t" x="442" y="124" text-anchor="middle">Model Training</text>

  <rect class="d-box" x="548" y="93" width="150" height="54" rx="8"/>
  <text class="d-t" x="623" y="116" text-anchor="middle">Model Validation</text>
  <text class="d-t" x="623" y="134" text-anchor="middle">Tests</text>

  <rect class="d-box-own" x="785" y="90" width="180" height="66" rx="8"/>
  <text class="d-t" x="875" y="112" text-anchor="middle">Experiment Tracking</text>
  <text class="d-t" x="875" y="130" text-anchor="middle">Model Registry</text>
  <text class="d-sub" x="875" y="146" text-anchor="middle">&lt;Staging / Prod&gt;</text>

  <rect class="d-box-own" x="372" y="200" width="140" height="44" rx="8"/>
  <text class="d-t" x="442" y="227" text-anchor="middle">Training Data</text>
  <rect class="d-box-own" x="548" y="200" width="150" height="44" rx="8"/>
  <text class="d-t" x="623" y="220" text-anchor="middle">Evaluation</text>
  <text class="d-t" x="623" y="235" text-anchor="middle">Sets</text>

  <path class="d-flow" d="M165 120 C190 120 190 105 212 105"/>
  <path class="d-flow" d="M165 120 C190 120 190 141 212 141"/>
  <path class="d-flow" d="M340 105 C356 105 356 114 372 114"/>
  <path class="d-flow" d="M340 141 C356 141 356 126 372 126"/>
  <path class="d-flow" d="M512 120 H548" marker-end="url(#tp-arrow)"/>
  <path class="d-flow" d="M698 120 H785" marker-end="url(#tp-arrow)"/>
  <path class="d-flow" d="M442 147 V200"/>
  <path class="d-flow" d="M623 147 V200"/>

  <!-- ===== DEVELOPMENT BRANCH (row 2, center y=372) ===== -->
  <rect class="d-band" x="195" y="306" width="525" height="132" rx="10"/>
  <text class="d-cap" x="212" y="328">Development Branch</text>

  <text class="d-sub" x="95" y="328" text-anchor="middle">Manual Testing</text>
  <rect class="d-box-ext" x="25" y="345" width="140" height="54" rx="8"/>
  <text class="d-t" x="95" y="376" text-anchor="middle">PyTest</text>

  <rect class="d-box" x="212" y="340" width="128" height="26" rx="6"/>
  <text class="d-t" x="276" y="357" text-anchor="middle">A.unit-test</text>
  <rect class="d-box" x="212" y="376" width="128" height="26" rx="6"/>
  <text class="d-t" x="276" y="393" text-anchor="middle">B.e2e-test</text>

  <rect class="d-box" x="372" y="345" width="140" height="54" rx="8"/>
  <text class="d-t" x="442" y="376" text-anchor="middle">Model Training</text>

  <rect class="d-box" x="548" y="345" width="150" height="54" rx="8"/>
  <text class="d-t" x="623" y="368" text-anchor="middle">Model Validation</text>
  <text class="d-t" x="623" y="386" text-anchor="middle">Tests</text>

  <rect class="d-box-own" x="785" y="342" width="180" height="66" rx="8"/>
  <text class="d-t" x="875" y="364" text-anchor="middle">Experiment Tracking</text>
  <text class="d-t" x="875" y="382" text-anchor="middle">Model Registry</text>
  <text class="d-sub" x="875" y="398" text-anchor="middle">&lt;Dev&gt;</text>

  <rect class="d-box-own" x="372" y="452" width="140" height="44" rx="8"/>
  <text class="d-t" x="442" y="479" text-anchor="middle">Training Data</text>
  <rect class="d-box-own" x="548" y="452" width="150" height="44" rx="8"/>
  <text class="d-t" x="623" y="472" text-anchor="middle">Evaluation</text>
  <text class="d-t" x="623" y="487" text-anchor="middle">Sets</text>

  <path class="d-flow" d="M165 372 C190 372 190 357 212 357"/>
  <path class="d-flow" d="M165 372 C190 372 190 393 212 393"/>
  <path class="d-flow" d="M340 357 C356 357 356 366 372 366"/>
  <path class="d-flow" d="M340 393 C356 393 356 378 372 378"/>
  <path class="d-flow" d="M512 372 H548" marker-end="url(#tp-arrow)"/>
  <path class="d-flow" d="M698 372 H785" marker-end="url(#tp-arrow)"/>
  <path class="d-flow" d="M442 399 V452"/>
  <path class="d-flow" d="M623 399 V452"/>
</svg>
</figure>

Hopsworks [Model Registry](registry.md) and [Model Serving](serving.md) capabilities can then be used to build a batch or online prediction service using the model.
