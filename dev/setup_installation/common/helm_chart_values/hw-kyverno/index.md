# Kyverno values { #helm-values-hw-kyverno }

Values under `hw-kyverno` configure the Kyverno cluster policies and the policy exceptions Hopsworks workloads need.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.2.0-alpha-1791283744` (Hopsworks `5.2.0`)._

Deployed according to the first of these values that is set: [`global._hopsworks.kyverno.enabled`](global.md#helm.global._hopsworks.kyverno.enabled), [`global._hopsworks.full_platform`](global.md#helm.global._hopsworks.full_platform).

## General { #helm-values-hw-kyverno-general }

??? example "Defaults as YAML"

    ```yaml
    hw-kyverno:
      hopsworkslib: {}
    ```

<div class="hops-values" markdown>

`hw-kyverno` <a class="headerlink" href="#helm.hw-kyverno" title="Permanent link">#</a> { #helm.hw-kyverno }
:   Type `object`, default `{}`.
    override hw-kyverno values

`hw-kyverno.hopsworkslib` <a class="headerlink" href="#helm.hw-kyverno.hopsworkslib" title="Permanent link">#</a> { #helm.hw-kyverno.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

</div>

## policies { #helm-values-hw-kyverno-policies }

??? example "Defaults as YAML"

    ```yaml
    hw-kyverno:
      policies:
        addCertificatesVolume:
          autogenControllers: DaemonSet,Deployment,Job,StatefulSet
          cacertsConfigMap: ca-pemstore
          enabled: false
          envs: []
          extraAnnotations: []
          hopsworksProjectLabelKey: hopsworks.ai/project
          initContainers:
            extraAnnotations: []
            labels: []
          labels:
          - key: job-type
            value: check-image-exist
          - key: job-type
            value: tag
          - key: job-type
            value: list-tags
          - key: job-type
            value: docker-build
          - key: job-type
            value: delete
          - key: job-type
            value: git-command
          mountPath: ''
        prohibitHostPath:
          enabled: false
    ```

<div class="hops-values" markdown>

`hw-kyverno.policies` <a class="headerlink" href="#helm.hw-kyverno.policies" title="Permanent link">#</a> { #helm.hw-kyverno.policies }
:   Type `object`.
    Configuration for Hopsworks Kyverno policies and exceptions

    ??? note "Default"

        ```yaml
        addCertificatesVolume:
          autogenControllers: DaemonSet,Deployment,Job,StatefulSet
          cacertsConfigMap: ca-pemstore
          enabled: false
          envs: []
          extraAnnotations: []
          hopsworksProjectLabelKey: hopsworks.ai/project
          initContainers:
            extraAnnotations: []
            labels: []
          labels:
          - key: job-type
            value: check-image-exist
          - key: job-type
            value: tag
          - key: job-type
            value: list-tags
          - key: job-type
            value: docker-build
          - key: job-type
            value: delete
          - key: job-type
            value: git-command
          mountPath: ''
        prohibitHostPath:
          enabled: false
        ```

`hw-kyverno.policies.addCertificatesVolume` <a class="headerlink" href="#helm.hw-kyverno.policies.addCertificatesVolume" title="Permanent link">#</a> { #helm.hw-kyverno.policies.addCertificatesVolume }
:   Type `object`.
    Configuration to add custom certificates to pods as a mounted volume

    ??? note "Default"

        ```yaml
        autogenControllers: DaemonSet,Deployment,Job,StatefulSet
        cacertsConfigMap: ca-pemstore
        enabled: false
        envs: []
        extraAnnotations: []
        hopsworksProjectLabelKey: hopsworks.ai/project
        initContainers:
          extraAnnotations: []
          labels: []
        labels:
        - key: job-type
          value: check-image-exist
        - key: job-type
          value: tag
        - key: job-type
          value: list-tags
        - key: job-type
          value: docker-build
        - key: job-type
          value: delete
        - key: job-type
          value: git-command
        mountPath: ''
        ```

`hw-kyverno.policies.addCertificatesVolume.autogenControllers` <a class="headerlink" href="#helm.hw-kyverno.policies.addCertificatesVolume.autogenControllers" title="Permanent link">#</a> { #helm.hw-kyverno.policies.addCertificatesVolume.autogenControllers }
:   Type `string`, default `"DaemonSet,Deployment,Job,StatefulSet"`.
    the list of controllers separated by comma to generate the policy for

`hw-kyverno.policies.addCertificatesVolume.cacertsConfigMap` <a class="headerlink" href="#helm.hw-kyverno.policies.addCertificatesVolume.cacertsConfigMap" title="Permanent link">#</a> { #helm.hw-kyverno.policies.addCertificatesVolume.cacertsConfigMap }
:   Type `string`, default `"ca-pemstore"`.
    The name of the configmap containing the certificates. The configmap should contains the ca-certificates.crt trusted by the user to replace the whole /etc/ssl/certs. It should also include the root certificate(s) if any defined for OAUTH or LDAP identity providers. Also, if using a hosted object storage with a custom CA, it should includes the java/cacerts to trust that object storage host and that require updating the hopsfs.namenode.jvmOpts = "-Djavax.net.ssl.trustStore=/etc/ssl/certs/my-cacerts -Djavax.net.ssl.trustStorePassword=changeit" and similarly for the hopsfs.datanode.jvmOpts.

`hw-kyverno.policies.addCertificatesVolume.enabled` <a class="headerlink" href="#helm.hw-kyverno.policies.addCertificatesVolume.enabled" title="Permanent link">#</a> { #helm.hw-kyverno.policies.addCertificatesVolume.enabled }
:   Type `bool`, default `false`.
    Enable add certificates volume

`hw-kyverno.policies.addCertificatesVolume.envs` <a class="headerlink" href="#helm.hw-kyverno.policies.addCertificatesVolume.envs" title="Permanent link">#</a> { #helm.hw-kyverno.policies.addCertificatesVolume.envs }
:   Type `list`, default `[]`.
    The array of environment variables with their values that you would like to inject to the pods along side the certificates volume.

`hw-kyverno.policies.addCertificatesVolume.extraAnnotations` <a class="headerlink" href="#helm.hw-kyverno.policies.addCertificatesVolume.extraAnnotations" title="Permanent link">#</a> { #helm.hw-kyverno.policies.addCertificatesVolume.extraAnnotations }
:   Type `list`, default `[]`.
    The array of extra annotations to use when filtering which pods to inject the certificates volume into.

`hw-kyverno.policies.addCertificatesVolume.hopsworksProjectLabelKey` <a class="headerlink" href="#helm.hw-kyverno.policies.addCertificatesVolume.hopsworksProjectLabelKey" title="Permanent link">#</a> { #helm.hw-kyverno.policies.addCertificatesVolume.hopsworksProjectLabelKey }
:   Type `string`, default `"hopsworks.ai/project"`.
    the name of the label key to identify hopsworks user project namespaces

`hw-kyverno.policies.addCertificatesVolume.initContainers` <a class="headerlink" href="#helm.hw-kyverno.policies.addCertificatesVolume.initContainers" title="Permanent link">#</a> { #helm.hw-kyverno.policies.addCertificatesVolume.initContainers }
:   Type `object`, default `{"extraAnnotations":[],"labels":[]}`.
    Opt-in for injecting the certificates volume into init containers. When enabled, a second mutate rule is rendered that targets spec.initContainers and is gated by an OR of the dedicated annotation (default kyverno-inject-certs-init=enabled), extraAnnotations, and labels configured below. Pods must opt in via at least one of these matchers.

`hw-kyverno.policies.addCertificatesVolume.initContainers.extraAnnotations` <a class="headerlink" href="#helm.hw-kyverno.policies.addCertificatesVolume.initContainers.extraAnnotations" title="Permanent link">#</a> { #helm.hw-kyverno.policies.addCertificatesVolume.initContainers.extraAnnotations }
:   Type `list`, default `[]`.
    Init-specific extra annotations that opt a pod's init containers into certificate volume injection. ORed with the dedicated init-container annotation and labels below. Defaults to empty so init injection is opt-in by design.

`hw-kyverno.policies.addCertificatesVolume.initContainers.labels` <a class="headerlink" href="#helm.hw-kyverno.policies.addCertificatesVolume.initContainers.labels" title="Permanent link">#</a> { #helm.hw-kyverno.policies.addCertificatesVolume.initContainers.labels }
:   Type `list`, default `[]`.
    Init-specific labels that opt a pod's init containers into certificate volume injection. ORed with the dedicated init-container annotation and extraAnnotations. Defaults to empty so third-party operator-injected init containers are not silently mutated.

`hw-kyverno.policies.addCertificatesVolume.labels` <a class="headerlink" href="#helm.hw-kyverno.policies.addCertificatesVolume.labels" title="Permanent link">#</a> { #helm.hw-kyverno.policies.addCertificatesVolume.labels }
:   Type `list`.
    The array of labels to use when filtering which pods to inject the certificates volume into. The default list includes job-type=check-image-exist, job-type=tag, job-type=list-tags, job-type=docker-build, job-type=delete for docker operations, that is needed if using a registry with custom CA. The default list also includes job-type=git-command for git operations, that is needed if using a git host with custom CA.

    ??? note "Default"

        ```yaml
        - key: job-type
          value: check-image-exist
        - key: job-type
          value: tag
        - key: job-type
          value: list-tags
        - key: job-type
          value: docker-build
        - key: job-type
          value: delete
        - key: job-type
          value: git-command
        ```

`hw-kyverno.policies.addCertificatesVolume.mountPath` <a class="headerlink" href="#helm.hw-kyverno.policies.addCertificatesVolume.mountPath" title="Permanent link">#</a> { #helm.hw-kyverno.policies.addCertificatesVolume.mountPath }
:   Type `string`, default `""`.
    Path to mount the certificates volume

`hw-kyverno.policies.prohibitHostPath` <a class="headerlink" href="#helm.hw-kyverno.policies.prohibitHostPath" title="Permanent link">#</a> { #helm.hw-kyverno.policies.prohibitHostPath }
:   Type `object`, default `{"enabled":false}`.
    Configuration for disabling hostPath volumes in Pods

`hw-kyverno.policies.prohibitHostPath.enabled` <a class="headerlink" href="#helm.hw-kyverno.policies.prohibitHostPath.enabled" title="Permanent link">#</a> { #helm.hw-kyverno.policies.prohibitHostPath.enabled }
:   Type `bool`, default `false`.
    Enable hostPath policy and relevant exceptions

</div>

## policyExceptions { #helm-values-hw-kyverno-policyexceptions }

??? example "Defaults as YAML"

    ```yaml
    hw-kyverno:
      policyExceptions:
        airflow:
          enabled: true
        buildkitd:
          appLabel: buildkitd
          enabled: true
          namePrefix: buildkitd
          rootless: false
        dockerRegistryConfigurer:
          enabled: true
        filebeat:
          enabled: true
        hopsfsCsi:
          enabled: true
        jobs:
          enabled: true
        jupyter:
          enabled: true
        knativeDryRun:
          enabled: true
        opensearch:
          enabled: true
        prometheusNodeExporter:
          enabled: true
        pythonDeployment:
          enabled: true
        pythonapp:
          enabled: true
        rondb:
          enabled: true
        spark:
          enabled: true
          rssAppName: rss-hops
        systemJobs:
          enabled: true
        terminal:
          enabled: true
        trino:
          enabled: true
        vllm:
          enabled: true
    ```

<div class="hops-values" markdown>

`hw-kyverno.policyExceptions` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions }
:   Type `object`.
    Configuration for PolicyExceptions to exempt specific services from Kyverno PSS Restricted policies

    ??? note "Default"

        ```yaml
        airflow:
          enabled: true
        buildkitd:
          appLabel: buildkitd
          enabled: true
          namePrefix: buildkitd
          rootless: false
        dockerRegistryConfigurer:
          enabled: true
        filebeat:
          enabled: true
        hopsfsCsi:
          enabled: true
        jobs:
          enabled: true
        jupyter:
          enabled: true
        knativeDryRun:
          enabled: true
        opensearch:
          enabled: true
        prometheusNodeExporter:
          enabled: true
        pythonDeployment:
          enabled: true
        pythonapp:
          enabled: true
        rondb:
          enabled: true
        spark:
          enabled: true
          rssAppName: rss-hops
        systemJobs:
          enabled: true
        terminal:
          enabled: true
        trino:
          enabled: true
        vllm:
          enabled: true
        ```

`hw-kyverno.policyExceptions.airflow` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.airflow" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.airflow }
:   Type `object`, default `{"enabled":true}`.
    PolicyException for the Airflow Deployments. Under the legacy in-container mount (global._hopsworks.csi.enabled=false) Airflow has a mount-airflow-folders sidecar that requires privileged access for FUSE mounting of HopsFS. This exception is enabled by default and only renders when the airflow service and hw-kyverno are enabled AND the CSI integration is off: with hopsfs-csi the Airflow pods are restricted-compliant and need no exemption.

`hw-kyverno.policyExceptions.airflow.enabled` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.airflow.enabled" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.airflow.enabled }
:   Type `bool`, default `true`.
    Enable PolicyException for airflow-scheduler. Set to false to disable even when airflow service is enabled.

`hw-kyverno.policyExceptions.buildkitd` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.buildkitd" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.buildkitd }
:   Type `object`.
    PolicyException for the persistent BuildKit daemon (global._hopsworks.buildkitd.enabled). The system-jobs exception matches Jobs by job-type label and so never reaches this StatefulSet, which would then be rejected on a Kyverno cluster.

    ??? note "Default"

        ```yaml
        appLabel: buildkitd
        enabled: true
        namePrefix: buildkitd
        rootless: false
        ```

`hw-kyverno.policyExceptions.buildkitd.appLabel` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.buildkitd.appLabel" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.buildkitd.appLabel }
:   Type `string`, default `"buildkitd"`.
    Pod label the exception matches, together with the name prefix below. Tracks hopsworks.buildkitd.name, which is what the StatefulSet sets as its app label.

`hw-kyverno.policyExceptions.buildkitd.enabled` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.buildkitd.enabled" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.buildkitd.enabled }
:   Type `bool`, default `true`.
    Enable PolicyException for the persistent BuildKit daemon. Also gated on global._hopsworks.buildkitd.enabled, which is what turns the daemon itself on, so this defaults true without becoming a standing grant: the exception renders only where the daemon does. Turning it off on a Kyverno cluster that runs the daemon gets it rejected at admission, since the exception grants the rootful union (privileged, host namespaces, uid 0).

`hw-kyverno.policyExceptions.buildkitd.namePrefix` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.buildkitd.namePrefix" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.buildkitd.namePrefix }
:   Type `string`, default `"buildkitd"`.
    Name prefix the exception matches, so the grant is not reachable by anything that merely wears the app label. StatefulSet pods are <name>-<ordinal>.

`hw-kyverno.policyExceptions.buildkitd.rootless` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.buildkitd.rootless" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.buildkitd.rootless }
:   Type `bool`, default `false`.
    Grant only the policies a rootless daemon needs, dropping the privileged-container and host-namespace exceptions. Defaults false, which grants the union, because a rootful daemon set to true is rejected at admission whereas a rootless daemon set to false merely carries two exceptions it does not use. Set true alongside hopsworks.buildkitd.rootless.enabled.

`hw-kyverno.policyExceptions.dockerRegistryConfigurer` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.dockerRegistryConfigurer" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.dockerRegistryConfigurer }
:   Type `object`, default `{"enabled":true}`.
    PolicyException for docker-registry-configurer DaemonSet. This service requires privileged access, hostPID, hostNetwork, and hostPath to configure container runtimes on nodes.

`hw-kyverno.policyExceptions.dockerRegistryConfigurer.enabled` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.dockerRegistryConfigurer.enabled" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.dockerRegistryConfigurer.enabled }
:   Type `bool`, default `true`.
    Enable PolicyException for docker-registry-configurer

`hw-kyverno.policyExceptions.filebeat` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.filebeat" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.filebeat }
:   Type `object`, default `{"enabled":true}`.
    PolicyException for filebeat DaemonSet. Filebeat requires hostNetwork, hostPath volumes, and runs as root to collect logs from all nodes.

`hw-kyverno.policyExceptions.filebeat.enabled` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.filebeat.enabled" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.filebeat.enabled }
:   Type `bool`, default `true`.
    Enable PolicyException for filebeat

`hw-kyverno.policyExceptions.hopsfsCsi` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.hopsfsCsi" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.hopsfsCsi }
:   Type `object`, default `{"enabled":true}`.
    PolicyException for HopsFS CSI node DaemonSet. The csi-hopsfs-node-plugin container requires privileged access, root user, hostPath volumes and Bidirectional mount propagation to publish mounts via kubelet plugin directories. It adds no capability of its own; privileged already implies them.

`hw-kyverno.policyExceptions.hopsfsCsi.enabled` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.hopsfsCsi.enabled" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.hopsfsCsi.enabled }
:   Type `bool`, default `true`.
    Enable PolicyException for HopsFS CSI node DaemonSet

`hw-kyverno.policyExceptions.jobs` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.jobs" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.jobs }
:   Type `object`, default `{"enabled":true}`.
    PolicyException for user jobs. These pods contain a hopsfsmount sidecar that requires privileged access for FUSE mounting of HopsFS.

`hw-kyverno.policyExceptions.jobs.enabled` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.jobs.enabled" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.jobs.enabled }
:   Type `bool`, default `true`.
    Enable PolicyException for user jobs

`hw-kyverno.policyExceptions.jupyter` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.jupyter" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.jupyter }
:   Type `object`, default `{"enabled":true}`.
    PolicyException for Jupyter server deployments. These pods contain a hopsfsmount sidecar that requires privileged access for FUSE mounting of HopsFS.

`hw-kyverno.policyExceptions.jupyter.enabled` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.jupyter.enabled" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.jupyter.enabled }
:   Type `bool`, default `true`.
    Enable PolicyException for Jupyter server deployments

`hw-kyverno.policyExceptions.knativeDryRun` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.knativeDryRun" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.knativeDryRun }
:   Type `object`, default `{"enabled":true}`.
    PolicyException for the throwaway Pod that Knative's webhook dry-run creates to validate a revision's pod spec. It carries no serving labels, so the label-scoped serving exceptions cannot match it, and a hopsfsmount FUSE sidecar makes it fail the restricted policies.

`hw-kyverno.policyExceptions.knativeDryRun.enabled` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.knativeDryRun.enabled" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.knativeDryRun.enabled }
:   Type `bool`, default `true`.
    Enable PolicyException for Knative pod-spec dry-run validation

`hw-kyverno.policyExceptions.opensearch` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.opensearch" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.opensearch }
:   Type `object`, default `{"enabled":true}`.
    PolicyException for opensearch StatefulSet. OpenSearch requires a privileged init container to configure vm.max_map_count kernel parameter. Only needed when olk.opensearch.setVMMaxMapCount is true.

`hw-kyverno.policyExceptions.opensearch.enabled` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.opensearch.enabled" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.opensearch.enabled }
:   Type `bool`, default `true`.
    Enable PolicyException for opensearch

`hw-kyverno.policyExceptions.prometheusNodeExporter` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.prometheusNodeExporter" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.prometheusNodeExporter }
:   Type `object`, default `{"enabled":true}`.
    PolicyException for prometheus-node-exporter DaemonSet. Node exporter requires hostNetwork and hostPath to collect node-level metrics.

`hw-kyverno.policyExceptions.prometheusNodeExporter.enabled` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.prometheusNodeExporter.enabled" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.prometheusNodeExporter.enabled }
:   Type `bool`, default `true`.
    Enable PolicyException for prometheus-node-exporter

`hw-kyverno.policyExceptions.pythonDeployment` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.pythonDeployment" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.pythonDeployment }
:   Type `object`, default `{"enabled":true}`.
    PolicyException for Python (model-server: python) KServe serving deployments. Agent deployments inject a root, privileged hopsfsmount FUSE sidecar (HWORKS-2871) that does not meet the restricted policy requirements.

`hw-kyverno.policyExceptions.pythonDeployment.enabled` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.pythonDeployment.enabled" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.pythonDeployment.enabled }
:   Type `bool`, default `true`.
    Enable PolicyException for Python model serving deployments

`hw-kyverno.policyExceptions.pythonapp` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.pythonapp" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.pythonapp }
:   Type `object`, default `{"enabled":true}`.
    PolicyException for Python app deployments (custom apps, Streamlit, Gradio). These pods contain a hopsfsmount sidecar that requires privileged access for FUSE mounting of HopsFS.

`hw-kyverno.policyExceptions.pythonapp.enabled` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.pythonapp.enabled" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.pythonapp.enabled }
:   Type `bool`, default `true`.
    Enable PolicyException for Python app deployments

`hw-kyverno.policyExceptions.rondb` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.rondb" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.rondb }
:   Type `object`, default `{"enabled":true}`.
    PolicyException for RonDB mysqlds StatefulSet. Mysqlds uses the SYS_NICE capability for process scheduling priority tuning. Only needed when rondb.rondb.meta.mysqld.addSysNiceCapability is true.

`hw-kyverno.policyExceptions.rondb.enabled` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.rondb.enabled" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.rondb.enabled }
:   Type `bool`, default `true`.
    Enable PolicyException for RonDB mysqlds

`hw-kyverno.policyExceptions.spark` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.spark" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.spark }
:   Type `object`, default `{"enabled":true,"rssAppName":"rss-hops"}`.
    PolicyException for Spark-related resources including: (1) Spark driver and executor pods created by spark-operator - these pods have container-level security contexts but lack pod-level security context support in older spark-operator versions, (2) RSS (Remote Shuffle Service) coordinator and shuffle server Deployments/StatefulSets - these are dynamically created by the Uniffle controller with security contexts configured via CRD spec, and (3) the spark-operator Helm hook Job that applies CRDs on install/upgrade - the upstream chart hardcodes its securityContext without runAsNonRoot/seccompProfile and exposes no values to set them.

`hw-kyverno.policyExceptions.spark.enabled` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.spark.enabled" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.spark.enabled }
:   Type `bool`, default `true`.
    Enable PolicyException for Spark-related resources (spark-operator driver/executor pods, RSS coordinator/shuffle server Deployments/StatefulSets, and the spark-operator CRD upgrade hook Job)

`hw-kyverno.policyExceptions.spark.rssAppName` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.spark.rssAppName" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.spark.rssAppName }
:   Type `string`, default `"rss-hops"`.
    The app name of the RemoteShuffleService resource

`hw-kyverno.policyExceptions.systemJobs` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.systemJobs" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.systemJobs }
:   Type `object`, default `{"enabled":true}`.
    PolicyException for Hopsworks system jobs including docker operations (docker-build, check-image-exist, tag, delete, list-tags), image validation (check-image), and conda library operations (list-libraries, export-libraries, conda-search-libraries). These jobs require privileged access to run buildkit/podman for building container images.

`hw-kyverno.policyExceptions.systemJobs.enabled` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.systemJobs.enabled" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.systemJobs.enabled }
:   Type `bool`, default `true`.
    Enable PolicyException for Hopsworks system jobs

`hw-kyverno.policyExceptions.terminal` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.terminal" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.terminal }
:   Type `object`, default `{"enabled":true}`.
    PolicyException for terminal server deployments. These pods contain a hopsfsmount sidecar that requires privileged access for FUSE mounting of HopsFS.

`hw-kyverno.policyExceptions.terminal.enabled` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.terminal.enabled" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.terminal.enabled }
:   Type `bool`, default `true`.
    Enable PolicyException for terminal server deployments

`hw-kyverno.policyExceptions.trino.enabled` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.trino.enabled" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.trino.enabled }
:   Type `bool`, default `true`.
    Enable PolicyException for trino

`hw-kyverno.policyExceptions.vllm` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.vllm" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.vllm }
:   Type `object`, default `{"enabled":true}`.
    PolicyException for vLLM model serving deployments created by KServe. These pods are deployed with default KServe/vLLM configurations that may not meet all restricted policy requirements.

`hw-kyverno.policyExceptions.vllm.enabled` <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.vllm.enabled" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.vllm.enabled }
:   Type `bool`, default `true`.
    Enable PolicyException for vLLM model serving deployments

`hw-kyverno.policyExceptions.trino` <span class="hops-values-deprecated">Deprecated</span> <a class="headerlink" href="#helm.hw-kyverno.policyExceptions.trino" title="Permanent link">#</a> { #helm.hw-kyverno.policyExceptions.trino }
:   Type `object`, default `{"enabled":true}`.
    DEPRECATED and read by nothing. Excepted the Trino pods from the restricted policies while their mount sidecars were privileged root containers; they are unprivileged hopsfs-csi sidecars now and pass the policies as-is. Kept only so an override carried from 5.1 still validates.

</div>

<!-- END GENERATED VALUES -->
