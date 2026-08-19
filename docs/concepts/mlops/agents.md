# Agents and LLM Systems

Agentic workflows are one of the four classes of AI system, alongside real-time, batch, and stream processing.
Context engineering for an agent follows many of the same principles as feature engineering for a classical ML model, and the feature store is where the context comes from.

## The feature store as a retrieval source

An LLM system retrieves the context it needs at inference time, and the feature store is a natural source for that context.
Precomputed features are retrieved by entity ID, and embeddings are retrieved from a vector index by similarity search.
The key requirement is that the entity IDs are provided in the user query, as part of the deployment API, so the system knows whose features to retrieve.
This is retrieval-augmented generation (RAG) with a feature store: structured features by key, unstructured context by similarity.

--8<-- "concepts/mlops/agents/the-feature-store-as-a-retrieval-source.html"

## Workflow or agent

An LLM workflow has a control flow the developer designs: the steps and their order are fixed, and the LLM fills in each step.
An agent decides its own control flow: the LLM chooses which steps to run and in what order, calling tools as it goes.
A workflow is more predictable, an agent is more flexible, and most production systems start as workflows.

## MCP and A2A

Two protocols connect the moving parts.
MCP (Model Context Protocol) is how an agent calls its tools, the intra-agent interface to data sources and functions, including a feature store.
A2A (Agent-to-Agent) is how agents talk to each other, the inter-agent interface.

See the [agent guides](../../user_guides/agents/index.md) for how to build and deploy agents and agent tasks on Hopsworks.
