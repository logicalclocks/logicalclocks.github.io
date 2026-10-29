# Envoy Gateway values { #helm-values-hw-envoy-gateway }

Values under `hw-envoy-gateway` configure the Envoy Gateway controller, the Gateway API front door of Standard-mode model deployments, and the hook that applies its CustomResourceDefinitions.
The subchart is installed when `global._hopsworks.envoyGateway.enabled` is true (off by default); the Gateway itself, its policies and its Service are configured under `kserve.envoyGateway` in [KServe values][helm-values-kserve].
Values under `hw-envoy-gateway.aiGateway` configure the Agent Router controller and its CRD hook, installed when `global._hopsworks.envoyGateway.aiGateway.enabled` is also true; its AI Gateway is configured under `kserve.envoyGateway.aiGateway`.
See [Envoy Gateway][envoy-gateway] for what the chart installs and what the cluster needs.
See [Agent Router][agent-router] for the project endpoint it adds on top.

<!-- BEGIN GENERATED VALUES -->

_The values table is generated from the Hopsworks Helm chart during the documentation build._

<!-- END GENERATED VALUES -->
