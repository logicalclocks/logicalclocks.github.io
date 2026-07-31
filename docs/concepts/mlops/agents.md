# Agents and LLM Systems

Agentic workflows are one of the four classes of AI system, alongside real-time, batch, and stream processing.
Context engineering for an agent follows many of the same principles as feature engineering for a classical ML model, and the feature store is where the context comes from.

## The feature store as a retrieval source

An LLM system retrieves the context it needs at inference time, and the feature store is a natural source for that context.
Precomputed features are retrieved by entity ID, and embeddings are retrieved from a vector index by similarity search.
The key requirement is that the entity IDs are provided in the user query, as part of the deployment API, so the system knows whose features to retrieve.
This is retrieval-augmented generation (RAG) with a feature store: structured features by key, unstructured context by similarity.

<figure class="hops-diagram">
<svg viewBox="0 0 1000 300" role="img" aria-label="A user query carrying an entity ID reaches the deployment API, which retrieves precomputed features by key and similar embeddings from the vector index in the feature store. The assembled context is passed to an LLM, which returns a response." xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="ag-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity=".4"/>
    </marker>
  </defs>

  <rect class="d-box-ext" x="16" y="60" width="152" height="64" rx="8"/>
  <text class="d-t" x="92" y="88" text-anchor="middle">User query</text>
  <text class="d-t d-sub" x="92" y="106" text-anchor="middle">entity ID + prompt</text>

  <path class="d-flow" d="M168 92 H206" marker-end="url(#ag-arrow)"/>

  <rect class="d-api" x="206" y="60" width="152" height="64" rx="8"/>
  <text class="d-t" x="282" y="88" text-anchor="middle">Deployment API</text>
  <text class="d-t d-sub" x="282" y="106" text-anchor="middle">the versioned contract</text>

  <path class="d-flow" d="M358 92 H396" marker-end="url(#ag-arrow)"/>

  <text class="d-t d-cap d-cap-fs" x="402" y="36">Feature store</text>
  <rect class="d-panel-fs" x="396" y="44" width="300" height="152" rx="12"/>
  <rect class="d-box-own" x="412" y="64" width="268" height="52" rx="6"/>
  <text class="d-t" x="546" y="86" text-anchor="middle">Precomputed features</text>
  <text class="d-t d-sub" x="546" y="104" text-anchor="middle">retrieved by entity ID</text>
  <rect class="d-box-own" x="412" y="126" width="268" height="52" rx="6"/>
  <text class="d-t" x="546" y="148" text-anchor="middle">Vector index</text>
  <text class="d-t d-sub" x="546" y="166" text-anchor="middle">retrieved by similarity</text>

  <path class="d-flow" d="M546 196 V226" marker-end="url(#ag-arrow)"/>
  <text class="d-t d-sub" x="576" y="216" text-anchor="start">retrieve</text>

  <rect class="d-box" x="452" y="226" width="188" height="52" rx="8"/>
  <text class="d-t" x="546" y="256" text-anchor="middle">Assembled context</text>

  <path class="d-flow" d="M640 252 H700" marker-end="url(#ag-arrow)"/>
  <rect class="d-box" x="700" y="226" width="104" height="52" rx="8"/>
  <text class="d-t" x="752" y="256" text-anchor="middle">LLM</text>

  <path class="d-flow" d="M804 252 H844" marker-end="url(#ag-arrow)"/>
  <rect class="d-box-ext" x="844" y="226" width="140" height="52" rx="8"/>
  <text class="d-t" x="914" y="256" text-anchor="middle">Response</text>
</svg>
</figure>

## Workflow or agent

An LLM workflow has a control flow the developer designs: the steps and their order are fixed, and the LLM fills in each step.
An agent decides its own control flow: the LLM chooses which steps to run and in what order, calling tools as it goes.
A workflow is more predictable, an agent is more flexible, and most production systems start as workflows.

## MCP and A2A

Two protocols connect the moving parts.
MCP (Model Context Protocol) is how an agent calls its tools, the intra-agent interface to data sources and functions, including a feature store.
A2A (Agent-to-Agent) is how agents talk to each other, the inter-agent interface.

See the [agent guides](../../user_guides/agents/index.md) for how to build and deploy agents and agent tasks on Hopsworks.
