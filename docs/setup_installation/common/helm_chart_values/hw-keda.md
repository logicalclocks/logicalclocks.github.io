# KEDA values { #helm-values-hw-keda }

Values under `hw-keda` configure KEDA and its HTTP add-on, the autoscaler of Standard-mode model deployments: it scales them on CPU and memory, on the requests at the gateway and on the vLLM engine metrics, and scales them to zero when idle.
The subchart is installed when `hopsworks.variables.kube_keda_installed` is true (the default), which also tells the Hopsworks backend to offer KEDA-backed scaling; without it, Standard-mode deployments fall back to KServe's own Horizontal Pod Autoscaler on CPU and memory.
See [How To Configure Scaling For A Deployment][how-to-configure-scaling-for-a-deployment] for what deployments can do with it.

<!-- BEGIN GENERATED VALUES -->

_The values table is generated from the Hopsworks Helm chart during the documentation build._

<!-- END GENERATED VALUES -->
