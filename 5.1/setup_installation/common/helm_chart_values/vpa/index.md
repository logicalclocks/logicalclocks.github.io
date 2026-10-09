# Vertical Pod Autoscaler values { #helm-values-vpa }

Values under `vpa` configure the Vertical Pod Autoscaler: its admission controller, recommender and updater.

<!-- BEGIN GENERATED VALUES -->

_Generated from the Hopsworks Helm chart `5.1.1` (Hopsworks `5.1.1`)._

Deployed according to the first of these values that is set: [`global._hopsworks.vpaEnabled`](global.md#helm.global._hopsworks.vpaEnabled), [`global._hopsworks.full_platform`](global.md#helm.global._hopsworks.full_platform).

??? example "Defaults as YAML"

    ```yaml
    vpa:
      allowOnlyOneReplica: true
      cleanupOnUninstall:
        enabled: true
        ttlSecondsAfterFinished: null
      enablePrometheusRecommender: true
      enablePrometheusScrapper: true
      enabled: true
      hopsworkslib: {}
      image:
        name: k8s-vpa
        tag: 1.7.1-2
      imagesTag: 1.7.1
      installController: true
      recommenderSettings:
        inRecommendationBoundsEvictionLifetimeThreshold: 12h
        podUpdateThreshold: '0.1'
      teardownWhenInstalling: true
      teardownWhenUninstall: true
    ```

<div class="hops-values" markdown>

`vpa` <a class="headerlink" href="#helm.vpa" title="Permanent link">#</a> { #helm.vpa }
:   Type `object`, default `{}`.
    override vpa values

`vpa.allowOnlyOneReplica` <a class="headerlink" href="#helm.vpa.allowOnlyOneReplica" title="Permanent link">#</a> { #helm.vpa.allowOnlyOneReplica }
:   Type `bool`, default `true`.
    If true the vpa updater is configured to update resources even when only one replica is running

`vpa.cleanupOnUninstall` <a class="headerlink" href="#helm.vpa.cleanupOnUninstall" title="Permanent link">#</a> { #helm.vpa.cleanupOnUninstall }
:   Type `object`, default `{"enabled":true,"ttlSecondsAfterFinished":null}`.
    post-delete cleanup of the VPA ConfigMap. cm.yaml defines `vpa` as a Helm hook with no delete-policy, so Helm never removes it; this deletes it by name on uninstall.

`vpa.cleanupOnUninstall.enabled` <a class="headerlink" href="#helm.vpa.cleanupOnUninstall.enabled" title="Permanent link">#</a> { #helm.vpa.cleanupOnUninstall.enabled }
:   Type `bool`, default `true`.
    enable the post-delete VPA ConfigMap cleanup hook

`vpa.cleanupOnUninstall.ttlSecondsAfterFinished` <a class="headerlink" href="#helm.vpa.cleanupOnUninstall.ttlSecondsAfterFinished" title="Permanent link">#</a> { #helm.vpa.cleanupOnUninstall.ttlSecondsAfterFinished }
:   Type `string`, default `nil`.
    ttlSecondsAfterFinished for the cleanup Job; null falls through to the global default

`vpa.enablePrometheusRecommender` <a class="headerlink" href="#helm.vpa.enablePrometheusRecommender" title="Permanent link">#</a> { #helm.vpa.enablePrometheusRecommender }
:   Type `bool`, default `true`.
    If true the recommender will be connected to prometheus

`vpa.enablePrometheusScrapper` <a class="headerlink" href="#helm.vpa.enablePrometheusScrapper" title="Permanent link">#</a> { #helm.vpa.enablePrometheusScrapper }
:   Type `bool`, default `true`.
    If true the vpa metrics will be connected to prometheus

`vpa.enabled` <a class="headerlink" href="#helm.vpa.enabled" title="Permanent link">#</a> { #helm.vpa.enabled }
:   Type `bool`, default `true`.

`vpa.hopsworkslib` <a class="headerlink" href="#helm.vpa.hopsworkslib" title="Permanent link">#</a> { #helm.vpa.hopsworkslib }
:   Type `object`, default `{}`.
    override hopsworkslib values

`vpa.image.name` <a class="headerlink" href="#helm.vpa.image.name" title="Permanent link">#</a> { #helm.vpa.image.name }
:   Type `string`, default `"k8s-vpa"`.

`vpa.image.tag` <a class="headerlink" href="#helm.vpa.image.tag" title="Permanent link">#</a> { #helm.vpa.image.tag }
:   Type `string`, default `"1.7.1-2"`.
    Installer toolbox version. Independent of imagesTag.

`vpa.imagesTag` <a class="headerlink" href="#helm.vpa.imagesTag" title="Permanent link">#</a> { #helm.vpa.imagesTag }
:   Type `string`, default `"1.7.1"`.
    Upstream VPA release. Selects the admission-controller, recommender and updater images, and must match the VPA version the installer image was built from. Not tied to image.tag.

`vpa.installController` <a class="headerlink" href="#helm.vpa.installController" title="Permanent link">#</a> { #helm.vpa.installController }
:   Type `bool`, default `true`.
    If true, install the VPA controller (CRDs, admission controller, recommender, updater). Set to false if VPA is already installed in the cluster.

`vpa.recommenderSettings` <a class="headerlink" href="#helm.vpa.recommenderSettings" title="Permanent link">#</a> { #helm.vpa.recommenderSettings }
:   Type `object`.
    Recommender settings <https://github.com/kubernetes/autoscaler/blob/5cd491a5a18b4b93f742351e3ebb195e358d2ea3/vertical-pod-autoscaler/pkg/updater/priority/update_priority_calculator.go#L36>

    ??? note "Default"

        ```yaml
        inRecommendationBoundsEvictionLifetimeThreshold: 12h
        podUpdateThreshold: '0.1'
        ```

`vpa.recommenderSettings.inRecommendationBoundsEvictionLifetimeThreshold` <a class="headerlink" href="#helm.vpa.recommenderSettings.inRecommendationBoundsEvictionLifetimeThreshold" title="Permanent link">#</a> { #helm.vpa.recommenderSettings.inRecommendationBoundsEvictionLifetimeThreshold }
:   Type `string`, default `"12h"`.
    The default value is 12h. This is the time needed to do a downscale

`vpa.recommenderSettings.podUpdateThreshold` <a class="headerlink" href="#helm.vpa.recommenderSettings.podUpdateThreshold" title="Permanent link">#</a> { #helm.vpa.recommenderSettings.podUpdateThreshold }
:   Type `string`, default `"0.1"`.
    The default value is 0.1 Set to 0 to always update even if the recommendation is in bounds Notice it needs to be an string

`vpa.teardownWhenInstalling` <a class="headerlink" href="#helm.vpa.teardownWhenInstalling" title="Permanent link">#</a> { #helm.vpa.teardownWhenInstalling }
:   Type `bool`, default `true`.
    If true, the vpa will be deleted if already installed

`vpa.teardownWhenUninstall` <a class="headerlink" href="#helm.vpa.teardownWhenUninstall" title="Permanent link">#</a> { #helm.vpa.teardownWhenUninstall }
:   Type `bool`, default `true`.
    if true, the vpa will be deleted if already installed when doing helm uninstall

</div>

<!-- END GENERATED VALUES -->
