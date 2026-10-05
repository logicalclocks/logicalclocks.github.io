# Helm chart values reference

This section lists every value you can configure when deploying Hopsworks with the Hopsworks Helm chart, with one page per top-level key.
It is generated from the `README.md` files of the chart and its subcharts, and for RonDB from the `values.schema.json` of the RonDB chart that Hopsworks pins.
On a released version of the docs it matches the Hopsworks Helm chart for that release; on the development docs it reflects the latest chart published to the development channel.

You set these values in the `values.<cloud>.yaml` file that you pass to `helm install`.
For a guided, end-to-end setup, follow one of the cloud installation guides, such as the [AWS getting started guide][aws-getting-started-with-eks].
Only a small subset of these values is needed for a typical install: "Common values" below lists the ones the cloud installation guides set, and the pages are the exhaustive reference.

"All values" lists the pages.
Each page states when its subchart is deployed: when the condition names several values, Helm uses the first one that is set.
"Upstream charts" are the third-party charts a subchart installs; their own values are documented upstream, and the link opens the version Hopsworks pins.
Every value has its own link (the `#` next to its key), and each section has its defaults as a values file under "Defaults as YAML".

<!-- BEGIN GENERATED VALUES -->
_The values tables are generated from the Hopsworks Helm chart during the documentation build._
_To preview them locally, run `uv run --extra cli hopsworks-docs gen-helm-values --chart <path-to-hopsworks-helm>`._
<!-- END GENERATED VALUES -->
