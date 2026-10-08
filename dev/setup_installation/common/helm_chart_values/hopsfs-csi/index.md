# HopsFS CSI driver values { #helm-values-hopsfs-csi }

Values under `hopsfs-csi` configure the CSI driver that mounts HopsFS into pods.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.2.0-alpha-1791461629` (Hopsworks `5.2.0`)._

Deployed when `global._hopsworks.csi.enabled` is `true`.

## General { #helm-values-hopsfs-csi-general }

??? example "Defaults as YAML"

    ```yaml
    hopsfs-csi:
      cleanupOnUninstall:
        enabled: true
        ttlSecondsAfterFinished: null
      fullnameOverride: hopsfs-csi
      hopsworkslib: {}
      image:
        pullPolicy: IfNotPresent
        registry: docker.hops.works
        repository: hopsworks/hopsfs-csi
        tag: 0.1.0-SNAPSHOT
      nameOverride: hopsfs-csi
      nodeSelector: {}
      sidecars:
        livenessProbe:
          pullPolicy: IfNotPresent
          repository: registry.k8s.io/sig-storage/livenessprobe
          resources:
            limits:
              cpu: 100m
              memory: 128Mi
            requests:
              cpu: 10m
              memory: 64Mi
          tag: v2.16.0
        nodeDriverRegistrar:
          pullPolicy: IfNotPresent
          repository: registry.k8s.io/sig-storage/csi-node-driver-registrar
          resources:
            limits:
              cpu: 400m
              memory: 512Mi
            requests:
              cpu: 40m
              memory: 128Mi
          tag: v2.14.0
        registry: docker.hops.works
      tolerations:
      - operator: Exists
    ```

<div class="hops-values" markdown>

`hopsfs-csi` <a class="headerlink" href="#helm.hopsfs-csi" title="Permanent link">#</a> { #helm.hopsfs-csi }
:   Type `object`, default `{}`.
    override hopsfs-csi values. Defaults live in charts/hopsfs-csi/values.yaml; the image comes from global._hopsworks.csi.image and global._hopsworks.imageRegistry, not from here.

`hopsfs-csi.cleanupOnUninstall` <a class="headerlink" href="#helm.hopsfs-csi.cleanupOnUninstall" title="Permanent link">#</a> { #helm.hopsfs-csi.cleanupOnUninstall }
:   Type `object`, default `{"enabled":true,"ttlSecondsAfterFinished":null}`.
    post-delete cleanup of what `helm uninstall` does not own: the CSIDriver object (a pre-install hook, HWORKS-3285) and, on OpenShift, the node plugin's SCC. Best effort: a failed delete is logged, not a failed uninstall. The CSIDriver is cluster-scoped and shared by every release of this chart in the cluster, so it is deleted only when its Helm annotations name the uninstalled release and no other release's node plugin pods exist. The hw-kyverno PolicyException for the plugin, if enabled, is still left behind. A reinstall does not depend on this hook.

`hopsfs-csi.cleanupOnUninstall.enabled` <a class="headerlink" href="#helm.hopsfs-csi.cleanupOnUninstall.enabled" title="Permanent link">#</a> { #helm.hopsfs-csi.cleanupOnUninstall.enabled }
:   Type `bool`, default `true`.
    enable the post-delete cleanup hook

`hopsfs-csi.cleanupOnUninstall.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.hopsfs-csi.cleanupOnUninstall.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.hopsfs-csi.cleanupOnUninstall.ttlSecondsAfterFinished }
:   Type `int or null`, default `nil`.
    TTL of the finished hook Job; null falls through to the global default

`hopsfs-csi.fullnameOverride` <a class="headerlink" href="#helm.hopsfs-csi.fullnameOverride" title="Permanent link">#</a> { #helm.hopsfs-csi.fullnameOverride }
:   Type `string`, default `"hopsfs-csi"`.
    override the full chart name

`hopsfs-csi.hopsworkslib` <a class="headerlink" href="#helm.hopsfs-csi.hopsworkslib" title="Permanent link">#</a> { #helm.hopsfs-csi.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`hopsfs-csi.image` <a class="headerlink" href="#helm.hopsfs-csi.image" title="Permanent link">#</a> { #helm.hopsfs-csi.image }
:   Type `object`.
    The hopsfs-csi image, run by the node plugin. The same image is the workload FUSE sidecar (Hopsworks-generated pods, Airflow, Trino): the fusermount3 proxy in the sidecar and the fd server in the plugin are two halves of one protocol, so the two ends must never drift on a node. Under the umbrella chart every field here is overridden by the single `global._hopsworks.csi.image` block (and `global._hopsworks.imageRegistry` for the registry), which is also what the sidecars and the Hopsworks `csi_sidecar_image` variable are seeded from. The chart is only installed through the umbrella, so set the global rather than these.

    ??? note "Default"

        ```yaml
        pullPolicy: IfNotPresent
        registry: docker.hops.works
        repository: hopsworks/hopsfs-csi
        tag: 0.1.0-SNAPSHOT
        ```

`hopsfs-csi.nameOverride` <a class="headerlink" href="#helm.hopsfs-csi.nameOverride" title="Permanent link">#</a> { #helm.hopsfs-csi.nameOverride }
:   Type `string`, default `"hopsfs-csi"`.
    override the chart name

`hopsfs-csi.nodeSelector` <a class="headerlink" href="#helm.hopsfs-csi.nodeSelector" title="Permanent link">#</a> { #helm.hopsfs-csi.nodeSelector }
:   Type `object`, default `{}`.
    nodeSelector of the node plugin DaemonSet. Deliberately NOT inherited from global._hopsworks.nodeSelector: that selector pins the Hopsworks services to their nodes, while the plugin must run on every node a HopsFS-mounting pod can land on (job and GPU pools included), or those pods hang in ContainerCreating. Set it only to keep the plugin off nodes that will never run such a pod.

`hopsfs-csi.sidecars` <a class="headerlink" href="#helm.hopsfs-csi.sidecars" title="Permanent link">#</a> { #helm.hopsfs-csi.sidecars }
:   Type `object`.
    The sig-storage helper containers next to the node plugin.

    ??? note "Default"

        ```yaml
        livenessProbe:
          pullPolicy: IfNotPresent
          repository: registry.k8s.io/sig-storage/livenessprobe
          resources:
            limits:
              cpu: 100m
              memory: 128Mi
            requests:
              cpu: 10m
              memory: 64Mi
          tag: v2.16.0
        nodeDriverRegistrar:
          pullPolicy: IfNotPresent
          repository: registry.k8s.io/sig-storage/csi-node-driver-registrar
          resources:
            limits:
              cpu: 400m
              memory: 512Mi
            requests:
              cpu: 40m
              memory: 128Mi
          tag: v2.14.0
        registry: docker.hops.works
        ```

`hopsfs-csi.sidecars.registry` <a class="headerlink" href="#helm.hopsfs-csi.sidecars.registry" title="Permanent link">#</a> { #helm.hopsfs-csi.sidecars.registry }
:   Type `string`, default `"docker.hops.works"`.
    The mirror the sig-storage images are pulled from (they keep their upstream registry.k8s.io/... path under it). Overridden by global._hopsworks.imageRegistry under the umbrella chart, so an air-gapped install only sets the global.

`hopsfs-csi.tolerations` <a class="headerlink" href="#helm.hopsfs-csi.tolerations" title="Permanent link">#</a> { #helm.hopsfs-csi.tolerations }
:   Type `list`, default `[{"operator":"Exists"}]`.
    tolerations of the node plugin DaemonSet. `operator: Exists` tolerates every taint for the reason above; narrow it only together with nodeSelector.

</div>

## node { #helm-values-hopsfs-csi-node }

??? example "Defaults as YAML"

    ```yaml
    hopsfs-csi:
      node:
        kubeletRootDir: /var/lib/kubelet
        priorityClassName: system-node-critical
        resources:
          limits:
            cpu: 500m
            memory: 256Mi
          requests:
            cpu: 50m
            memory: 64Mi
        serviceAccount:
          create: true
          name: hopsfs-csi-node-sa
        terminationGracePeriodSeconds: 300
    ```

<div class="hops-values" markdown>

`hopsfs-csi.node.kubeletRootDir` <a class="headerlink" href="#helm.hopsfs-csi.node.kubeletRootDir" title="Permanent link">#</a> { #helm.hopsfs-csi.node.kubeletRootDir }
:   Type `string`, default `"/var/lib/kubelet"`.

`hopsfs-csi.node.priorityClassName` <a class="headerlink" href="#helm.hopsfs-csi.node.priorityClassName" title="Permanent link">#</a> { #helm.hopsfs-csi.node.priorityClassName }
:   Type `string`, default `"system-node-critical"`.
    priorityClassName of the node plugin pods. system-node-critical so a full node never evicts the plugin (a node without it cannot start any CSI-mounted pod) and so it is scheduled before the workloads that depend on it.

`hopsfs-csi.node.resources.limits.cpu` <a class="headerlink" href="#helm.hopsfs-csi.node.resources.limits.cpu" title="Permanent link">#</a> { #helm.hopsfs-csi.node.resources.limits.cpu }
:   Type `string`, default `"500m"`.

`hopsfs-csi.node.resources.limits.memory` <a class="headerlink" href="#helm.hopsfs-csi.node.resources.limits.memory" title="Permanent link">#</a> { #helm.hopsfs-csi.node.resources.limits.memory }
:   Type `string`, default `"256Mi"`.

`hopsfs-csi.node.resources.requests.cpu` <a class="headerlink" href="#helm.hopsfs-csi.node.resources.requests.cpu" title="Permanent link">#</a> { #helm.hopsfs-csi.node.resources.requests.cpu }
:   Type `string`, default `"50m"`.

`hopsfs-csi.node.resources.requests.memory` <a class="headerlink" href="#helm.hopsfs-csi.node.resources.requests.memory" title="Permanent link">#</a> { #helm.hopsfs-csi.node.resources.requests.memory }
:   Type `string`, default `"64Mi"`.

`hopsfs-csi.node.serviceAccount.create` <a class="headerlink" href="#helm.hopsfs-csi.node.serviceAccount.create" title="Permanent link">#</a> { #helm.hopsfs-csi.node.serviceAccount.create }
:   Type `bool`, default `true`.

`hopsfs-csi.node.serviceAccount.name` <a class="headerlink" href="#helm.hopsfs-csi.node.serviceAccount.name" title="Permanent link">#</a> { #helm.hopsfs-csi.node.serviceAccount.name }
:   Type `string`, default `"hopsfs-csi-node-sa"`.

`hopsfs-csi.node.terminationGracePeriodSeconds` <a class="headerlink" href="#helm.hopsfs-csi.node.terminationGracePeriodSeconds" title="Permanent link">#</a> { #helm.hopsfs-csi.node.terminationGracePeriodSeconds }
:   Type `int`, default `300`.
    How long kubelet lets a stopping plugin pod run before killing it. When the plugin is removed together with the pods that mount through it (helm uninstall, namespace delete), it keeps serving kubelet's unmounts until none is left and exits then, so this is only ever used up when a consumer is itself stuck; a plugin that is merely being replaced (rollout, eviction) exits at once. Set it above the longest terminationGracePeriodSeconds of any HopsFS-mounting pod, or those pods hang in Terminating after the plugin is gone (HWORKS-3287).

</div>

## openshift { #helm-values-hopsfs-csi-openshift }

??? example "Defaults as YAML"

    ```yaml
    hopsfs-csi:
      openshift:
        csiEphemeralVolumeProfile: restricted
        existingSecurityContextConstraints:
          check:
            enabled: true
            ttlSecondsAfterFinished: null
          name: ''
        securityContextConstraints: false
    ```

<div class="hops-values" markdown>

`hopsfs-csi.openshift` <a class="headerlink" href="#helm.hopsfs-csi.openshift" title="Permanent link">#</a> { #helm.hopsfs-csi.openshift }
:   Type `object`.
    OpenShift-only settings of the node plugin: the CSI Volume Admission profile label on the CSIDriver and whether to ship a SecurityContextConstraints for the plugin's service account.

    ??? note "Default"

        ```yaml
        csiEphemeralVolumeProfile: restricted
        existingSecurityContextConstraints:
          check:
            enabled: true
            ttlSecondsAfterFinished: null
          name: ''
        securityContextConstraints: false
        ```

`hopsfs-csi.openshift.csiEphemeralVolumeProfile` <a class="headerlink" href="#helm.hopsfs-csi.openshift.csiEphemeralVolumeProfile" title="Permanent link">#</a> { #helm.hopsfs-csi.openshift.csiEphemeralVolumeProfile }
:   Type `string`, default `"restricted"`.
    OpenShift CSI Volume Admission profile for inline ephemeral volumes, emitted as the security.openshift.io/csi-ephemeral-volume-profile label on the CSIDriver. Must be one of restricted, baseline or privileged and must not be empty on OpenShift: an absent label makes the CSIInlineVolumeSecurity admission plugin require enforce=privileged of every namespace that mounts the driver, which rejects every Airflow and Trino pod. `restricted` is correct for this driver (see templates/csidriver.yaml for why) and the label is inert off OpenShift.

`hopsfs-csi.openshift.existingSecurityContextConstraints` <a class="headerlink" href="#helm.hopsfs-csi.openshift.existingSecurityContextConstraints" title="Permanent link">#</a> { #helm.hopsfs-csi.openshift.existingSecurityContextConstraints }
:   Type `object`, default `{"check":{"enabled":true,"ttlSecondsAfterFinished":null},"name":""}`.
    Let the cluster administrators own the node plugin's SCC instead of this chart. Off by default: the chart ships the SCC (securityContextConstraints above). Setting `name` to the SCC the administrators created turns the shipped one off, whatever securityContextConstraints and global._hopsworks.openshift.enabled say, keeps the post-delete cleanup off it, and adds a pre-install/pre-upgrade hook Job that fails the release early, with the reason in its log, when that SCC is missing or does not admit the plugin. Without the check a wrong SCC leaves the DaemonSet with no pods and every CSI-mounted workload in ContainerCreating, with no event naming the cause. The Job runs a PodSecurityPolicySubjectReview of the exact DaemonSet pod template for the plugin's service account (users, groups and RBAC `use` grants all count; the account need not exist yet), and a server-side dry-run create of a representative HopsFS-mounting workload pod in the release namespace: the unprivileged FUSE sidecar at global._hopsworks.executor_uid plus an inline csi volume of this driver, which also exercises the CSI Volume Admission plugin against the CSIDriver's profile label (HWORKS-3285) and restricted-v2's uid range. The reference manifest to hand to the administrators is the chart's own: `helm template . --set hopsfs-csi.openshift.securityContextConstraints=true --show-only charts/hopsfs-csi/templates/scc.yaml`; whatever they derive from it has to grant `system:serviceaccount:<release namespace>:hopsfs-csi-node-sa`.

`hopsfs-csi.openshift.existingSecurityContextConstraints.check` <a class="headerlink" href="#helm.hopsfs-csi.openshift.existingSecurityContextConstraints.check" title="Permanent link">#</a> { #helm.hopsfs-csi.openshift.existingSecurityContextConstraints.check }
:   Type `object`, default `{"enabled":true,"ttlSecondsAfterFinished":null}`.
    the pre-install/pre-upgrade admission check, run only when `name` is set

`hopsfs-csi.openshift.existingSecurityContextConstraints.check.enabled` <a class="headerlink" href="#helm.hopsfs-csi.openshift.existingSecurityContextConstraints.check.enabled" title="Permanent link">#</a> { #helm.hopsfs-csi.openshift.existingSecurityContextConstraints.check.enabled }
:   Type `bool`, default `true`.
    run the check. Off only to install against an SCC the OpenShift review API cannot evaluate; the install then fails late, in the DaemonSet, if the SCC is wrong.

`hopsfs-csi.openshift.existingSecurityContextConstraints.check.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.hopsfs-csi.openshift.existingSecurityContextConstraints.check.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.hopsfs-csi.openshift.existingSecurityContextConstraints.check.ttlSecondsAfterFinished }
:   Type `int or null`, default `nil`.
    TTL of the finished hook Job; null falls through to the global default

`hopsfs-csi.openshift.existingSecurityContextConstraints.name` <a class="headerlink" href="#helm.hopsfs-csi.openshift.existingSecurityContextConstraints.name" title="Permanent link">#</a> { #helm.hopsfs-csi.openshift.existingSecurityContextConstraints.name }
:   Type `string`, default `""`.
    name of the administrator-created SecurityContextConstraints; empty, the default, means the chart ships its own

`hopsfs-csi.openshift.securityContextConstraints` <a class="headerlink" href="#helm.hopsfs-csi.openshift.securityContextConstraints" title="Permanent link">#</a> { #helm.hopsfs-csi.openshift.securityContextConstraints }
:   Type `bool`, default `false`.
    Ship a SecurityContextConstraints granting the node plugin's service account what the DaemonSet needs on OpenShift (privileged, hostPath volumes, Bidirectional mount propagation, root); without it restricted-v2 rejects the plugin pod and every CSI-mounted workload sits in ContainerCreating. Rendered when this is true or global._hopsworks.openshift.enabled is true. Cluster-scoped and named after the release so two installs do not collide. Off, together with the global, when existingSecurityContextConstraints.name is set.

</div>

<!-- END GENERATED VALUES -->
