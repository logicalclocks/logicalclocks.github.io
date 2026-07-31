# AI Systems

An AI system is a set of independent feature pipelines, training pipelines, and inference pipelines that are connected via a feature store and model registry.
Each pipeline is a separate program with its own inputs and outputs, and the shared data layer is what lets them be developed, run, and scaled independently.

An AI system is defined by how it computes its predictions, not by the type of application that consumes them.
The inference pipeline determines the class of AI system you are building.
There are four classes:

- **Real-time (interactive)**: a client sends a prediction request and an online inference pipeline computes and returns a prediction with low latency.
- **Batch**: an inference pipeline runs on a schedule, scores a set of entities, and writes the predictions to an inference store.
- **Stream processing**: an inference pipeline computes predictions continuously over an event stream.
- **Agentic workflows**: an LLM-driven control flow decides which steps to run, retrieving the context and features it needs from the feature store. See [Agents and LLM Systems](agents.md).

Whatever the class, an AI system is composed of the same parts:

- one or more feature pipeline(s) that keep the feature store up to date,
- a training pipeline that produces a model in the model registry,
- an inference pipeline that reads features and computes predictions,
- a sink for the predictions, either an inference store or a user interface.

The two figures below illustrate the two most common classes, batch and real-time.

## Batch AI systems

In the figure below, feature pipelines update the feature store with new feature data on a schedule (e.g., hourly, daily).
A batch inference pipeline also runs on a schedule, reads batch scoring data from the feature store, computes predictions with an embedded model, and writes those predictions to an inference store.
The inference store is any data store that holds the predictions from batch inference pipelines.
From there, the predictions are consumed by (predictive, prescriptive) analytical reports and/or to AI-enable operational services.

<figure class="hops-diagram">
<svg viewBox="0 0 1000 520" role="img" aria-label="A batch AI system where feature and training pipelines populate the feature store and model registry, a scheduled batch prediction pipeline reads batch data and writes predictions to an inference store consumed by reports and operational services." xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="aps-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/></marker></defs>
  <rect class="d-box-own" x="40" y="40" width="180" height="56" rx="8"/>
  <text class="d-t" x="130" y="73" text-anchor="middle">Models</text>
  <rect class="d-box-own" x="305" y="36" width="160" height="60" rx="8"/>
  <text class="d-t" x="385" y="71" text-anchor="middle">Feature Store</text>
  <rect class="d-box-ext" x="630" y="36" width="140" height="52" rx="8"/>
  <text class="d-t" x="700" y="67" text-anchor="middle">Reports</text>
  <rect class="d-box-ext" x="800" y="36" width="170" height="52" rx="8"/>
  <text class="d-t" x="885" y="67" text-anchor="middle">Operational Services</text>
  <rect class="d-box" x="40" y="410" width="180" height="56" rx="8"/>
  <text class="d-t" x="130" y="443" text-anchor="middle">Training Pipeline</text>
  <rect class="d-box" x="305" y="410" width="160" height="56" rx="8"/>
  <text class="d-t" x="385" y="443" text-anchor="middle">Feature Pipeline</text>
  <rect class="d-box" x="590" y="340" width="200" height="56" rx="8"/>
  <text class="d-t" x="690" y="373" text-anchor="middle">Batch Prediction Pipeline</text>
  <rect class="d-box" x="850" y="340" width="130" height="56" rx="8"/>
  <text class="d-t" x="915" y="365" text-anchor="middle">Database</text>
  <text class="d-sub" x="915" y="381" text-anchor="middle">(Sink)</text>
  <path class="d-flow" d="M385 410 V100" marker-end="url(#aps-arrow)"/>
  <text class="d-sub" x="399" y="250">Write</text>
  <path class="d-flow" d="M110 410 V100" stroke-dasharray="4 3" marker-end="url(#aps-arrow)"/>
  <text class="d-sub" x="124" y="250">Deploy</text>
  <path class="d-flow" d="M330 96 V388 H175 V410" stroke-dasharray="4 3" marker-end="url(#aps-arrow)"/>
  <text class="d-sub" x="344" y="250">Read</text>
  <path class="d-flow" d="M465 70 C620 120 690 210 690 340" marker-end="url(#aps-arrow)"/>
  <text class="d-sub" x="560" y="205">Batch Data</text>
  <path class="d-flow" d="M790 368 H850" marker-end="url(#aps-arrow)"/>
  <path class="d-flow" d="M915 340 V88" marker-end="url(#aps-arrow)"/>
  <text class="d-sub" x="901" y="210" text-anchor="end">Consume predictions</text>
  <path class="d-flow" d="M770 62 H800" marker-start="url(#aps-arrow)" marker-end="url(#aps-arrow)"/>
  <path class="d-flow" d="M40 72 H20 V500 H690 V396" stroke-dasharray="4 3" marker-end="url(#aps-arrow)"/>
</svg>
</figure>

## Real-time AI systems

In the figure below, feature pipelines update the feature store with new feature data on a schedule (e.g., streaming, hourly, daily), and the operational service sends prediction requests to a model deployed on KServe via its secured Istio endpoint.
A deployed model on KServe handles the prediction request by first retrieving pre-computed features from the feature store for the given request, and then building a feature vector that is scored by the model.
The prediction result is returned to the client (the operational service).
KServe logs both the feature values and the prediction results back to Hopsworks for further analysis and to help create new training data.

<figure class="hops-diagram">
<svg viewBox="0 0 1000 500" role="img" aria-label="A real-time AI system where an operational service calls a model deployed on KServe, the model reads pre-engineered features from the feature store, returns a prediction, and logs features and predictions back to the feature store." xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="ops-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/></marker></defs>
  <rect class="d-box-own" x="340" y="40" width="180" height="60" rx="8"/>
  <text class="d-t" x="430" y="76" text-anchor="middle">Models</text>
  <rect class="d-box-own" x="760" y="40" width="180" height="60" rx="8"/>
  <text class="d-t" x="850" y="76" text-anchor="middle">Feature Store</text>
  <rect class="d-box-ext" x="40" y="416" width="190" height="68" rx="8"/>
  <text class="d-t" x="135" y="446" text-anchor="middle">Operational Service</text>
  <text class="d-sub" x="135" y="464" text-anchor="middle">(AI-Enabled Product)</text>
  <rect class="d-box" x="340" y="420" width="180" height="56" rx="8"/>
  <text class="d-t" x="430" y="453" text-anchor="middle">Training Pipeline</text>
  <rect class="d-box" x="760" y="420" width="180" height="56" rx="8"/>
  <text class="d-t" x="850" y="453" text-anchor="middle">Feature Pipeline</text>
  <path class="d-flow" d="M430 40 V16 H850 V40" marker-end="url(#ops-arrow)"/>
  <text class="d-sub" x="640" y="11" text-anchor="middle">Feature/Prediction Logging</text>
  <path class="d-flow" d="M760 80 H524" marker-end="url(#ops-arrow)"/>
  <text class="d-sub" x="642" y="66" text-anchor="middle">Pre-engineered Features</text>
  <path class="d-flow" d="M850 420 V104" marker-end="url(#ops-arrow)"/>
  <text class="d-sub" x="864" y="270">Write</text>
  <path class="d-flow" d="M430 420 V104" stroke-dasharray="4 3" marker-end="url(#ops-arrow)"/>
  <text class="d-sub" x="444" y="270">Deploy</text>
  <path class="d-flow" d="M800 104 V384 H470 V420" stroke-dasharray="4 3" marker-end="url(#ops-arrow)"/>
  <text class="d-sub" x="660" y="372" text-anchor="middle">Read</text>
  <path class="d-flow" d="M135 416 V70 H336" marker-end="url(#ops-arrow)"/>
  <text class="d-sub" x="149" y="250">Istio / KServe</text>
</svg>
</figure>

## MLOps Flywheel

Once you have built your batch or real-time AI system, the MLOps flywheel is the path to building a self-managing system that automatically collects and processes feature logs, prediction logs, and outcomes to help create new training data for models.
This enables a ML flywheel where new training data and insights are generated from your AI system, by feeding logs back into the feature store.
More training data enables the training of better models, and with better models, you should hopefully improve your operational/batch services, so that you attract more clients, who in turn produce more data for training models.
And, thus, the ML flywheel is bootstrapped and leads to a virtuous cycle of more data leading to better models and more models leading to more users, who produce more data, and so on.

<figure class="hops-diagram">
<svg viewBox="0 0 1000 560" role="img" aria-label="The MLOps flywheel where enterprise data and operational services feed a feature pipeline into the feature store, the feature store serves an offline API to the training pipeline and an online API to models, and models drive operational services that generate more data." xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="fw-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/></marker></defs>
  <rect class="d-box-ext" x="350" y="20" width="160" height="52" rx="8" stroke-dasharray="4 3"/>
  <text class="d-t" x="430" y="51" text-anchor="middle">Enterprise Data</text>
  <rect class="d-box-ext" x="40" y="150" width="180" height="72" rx="8"/>
  <text class="d-t" x="130" y="181" text-anchor="middle">Batch /</text>
  <text class="d-t" x="130" y="201" text-anchor="middle">Operational Services</text>
  <rect class="d-box" x="350" y="150" width="160" height="72" rx="8"/>
  <text class="d-t" x="430" y="191" text-anchor="middle">Feature Pipeline</text>
  <rect class="d-box-own" x="760" y="150" width="180" height="72" rx="8"/>
  <text class="d-t" x="850" y="191" text-anchor="middle">Feature Store</text>
  <rect class="d-box-own" x="40" y="470" width="180" height="72" rx="8"/>
  <text class="d-t" x="130" y="511" text-anchor="middle">Models</text>
  <rect class="d-box" x="760" y="470" width="180" height="72" rx="8"/>
  <text class="d-t" x="850" y="511" text-anchor="middle">Training Pipeline</text>
  <path class="d-flow" d="M430 72 V150" marker-end="url(#fw-arrow)"/>
  <path class="d-flow" d="M220 186 H350" marker-end="url(#fw-arrow)"/>
  <path class="d-flow" d="M510 186 H760" marker-end="url(#fw-arrow)"/>
  <path class="d-flow" d="M850 222 V470" marker-end="url(#fw-arrow)"/>
  <text class="d-sub" x="772" y="332" text-anchor="middle">Feature View</text>
  <text class="d-sub" x="772" y="346" text-anchor="middle">Offline API</text>
  <path class="d-flow" d="M760 506 H220" marker-end="url(#fw-arrow)"/>
  <path class="d-flow" d="M770 222 C520 340 360 430 224 486" marker-end="url(#fw-arrow)"/>
  <text class="d-sub" x="404" y="326" text-anchor="middle">Feature View</text>
  <text class="d-sub" x="404" y="340" text-anchor="middle">Online API</text>
  <path class="d-flow" d="M130 470 V222" marker-end="url(#fw-arrow)"/>
</svg>
</figure>
