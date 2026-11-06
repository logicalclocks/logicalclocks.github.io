# LLM Gateway values { #helm-values-hw-envoy-ai-gateway }

Values under `hw-envoy-gateway.aiGateway` configure the LLM Gateway controller, its mutating webhook and the hook that applies its CustomResourceDefinitions.
They ship in the `hw-envoy-gateway` subchart, whose other values are listed in [Envoy Gateway values][helm-values-hw-envoy-gateway], and are used when `global._hopsworks.envoyGateway.aiGateway.enabled` is true (off by default).
The AI Gateway itself, its policies and its tracing are configured under `kserve.envoyGateway.aiGateway` in [KServe values][helm-values-kserve], and the trace collector and table under `hopsworks.agentRouter` in [Hopsworks values][helm-values-hopsworks].
See [LLM Gateway][llm-gateway] for what the feature installs and what the cluster needs.

<!-- BEGIN GENERATED VALUES -->

_The values table is generated from the Hopsworks Helm chart during the documentation build._

<!-- END GENERATED VALUES -->
