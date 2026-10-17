"""Generate the Upgraded components table of a release page.

Compares the version of every component in hopsworks-helm at a release's tag with an
earlier release, as ``.claude/docs/releases.md`` describes. Fails when a version in
the chart changed that no component below covers, so a new component isn't left out
of the table silently.
"""

import re
import subprocess
from functools import cache
from pathlib import Path
from typing import Annotated

import typer
import yaml
from hopsworks_docs.scripts.shared.docs_root import _DOCS_ROOT


HOPSWORKS = "charts/hopsworks/values.yaml"
KSERVE = "charts/kserve/values.yaml"
PROMETHEUS = "charts/prometheus/values.yaml"
SUPERSET = "charts/superset/values.yaml"
SECTION = "\n## Upgraded components\n"

# Where the chart sets each component's version: "<file>:<key>" in hopsworks-helm,
# "rondb:<key>" in rondb-helm at the tag the rondb dependency names, or
# "upstream:<Chart.yaml>:<dependency>" for the default of an upstream chart. The
# first one set is the version; the rest are other places that set the same version.
COMPONENTS = {
    "Airflow image": ["charts/airflow/Chart.yaml:appVersion"],
    "Alertmanager": [
        f"{PROMETHEUS}:prometheus.alertmanager.image.tag",
        "upstream:charts/prometheus/Chart.yaml:prometheus",
    ],
    "ArrowFlight server": ["charts/arrowflight/Chart.yaml:appVersion"],
    "Base environment images": [f"{HOPSWORKS}:variables.base_image_version"],
    "Brewer": ["charts/brewer/Chart.yaml:appVersion"],
    "BuildKit": [
        f"{HOPSWORKS}:dockerRegistry.buildkit.tag",
        f"{HOPSWORKS}:variables.base_buildkit_image",
    ],
    "cert-manager": [f"{KSERVE}:cert_manager.version"],
    "Certificates operator": ["charts/certs-operator/Chart.yaml:appVersion"],
    "Consul": [
        "charts/consul/values.yaml:consul.global.image",
        "charts/consul/Chart.yaml:appVersion",
    ],
    "consul-k8s": ["charts/consul/values.yaml:consul.global.imageK8S"],
    "Docker registry": ["charts/docker-registry/values.yaml:image.tag"],
    "Filebeat": [
        f"{HOPSWORKS}:image.filebeat.tag",
        "charts/olk/values.yaml:filebeat.image.tag",
    ],
    "Git image": [f"{HOPSWORKS}:variables.git_image_version"],
    "Grafana": [
        "charts/grafana/values.yaml:grafana.image.tag",
        "charts/grafana/Chart.yaml:appVersion",
    ],
    "Hive Metastore": [
        "charts/hive/Chart.yaml:appVersion",
        f"{HOPSWORKS}:variables.hive2_version",
    ],
    "HopsFS CSI driver": [
        "values.yaml:global._hopsworks.csi.image.tag",
        "charts/hopsfs-csi/values.yaml:image.tag",
        "charts/hopsfs-csi/Chart.yaml:appVersion",
    ],
    "HopsFS CSI liveness probe": [
        "charts/hopsfs-csi/values.yaml:sidecars.livenessProbe.tag"
    ],
    "HopsFS CSI node driver registrar": [
        "charts/hopsfs-csi/values.yaml:sidecars.nodeDriverRegistrar.tag"
    ],
    "HopsFS": [
        "charts/hopsfs/values.yaml:image.tag",
        "charts/hopsfs/Chart.yaml:appVersion",
        f"{HOPSWORKS}:variables.hadoop_version",
    ],
    "Hudi bundle of the Hive Metastore": [
        "charts/hive/values.yaml:metastore.config.hudi_hadoop_version"
    ],
    "Image builder": [f"{HOPSWORKS}:imageBuilder.tag"],
    "Inference logger": [f"{KSERVE}:inferenceLogger.tag"],
    "Istio": [
        f"{KSERVE}:istio.istioctl.targetVersion",
        f"{KSERVE}:istio.istioctl.currentVersion",
    ],
    "Kafka": [
        "charts/kafka/values.yaml:cluster.kafka.version",
        f"{HOPSWORKS}:variables.kafka_version",
        "charts/kafka/values.yaml:cluster.kafka.image.tag",
    ],
    "KEDA": ["charts/hw-keda/Chart.yaml:appVersion"],
    "KEDA HTTP add-on": ["vendor/keda-add-ons-http/Chart.yaml:appVersion"],
    "Knative Serving": [f"{KSERVE}:knative.version"],
    "KServe": [
        f"{KSERVE}:kserve.version",
        "charts/kserve/Chart.yaml:appVersion",
        f"{KSERVE}:knative.queueSidecarImage.tag",
        f"{KSERVE}:kserve.agent.tag",
        f"{KSERVE}:kserve.controller.tag",
        f"{KSERVE}:kserve.localmodel.controller.tag",
        f"{KSERVE}:kserve.router.tag",
        f"{KSERVE}:kserve.storage.tag",
    ],
    "KServe utilities": [f"{KSERVE}:kserveUtilsImage.tag"],
    "KubeRay operator": ["charts/ray/values.yaml:kuberay-operator.image.tag"],
    "Logstash": ["charts/olk/values.yaml:logstash.version"],
    "Model serving authenticator": [f"{KSERVE}:servingAuthenticator.tag"],
    "Model serving webhook": [f"{KSERVE}:servingWebhook.tag"],
    "MySQL Connector/J": [f"{HOPSWORKS}:image.admin.mysqlConnectorVersion"],
    "OnlineFS": ["charts/onlinefs/Chart.yaml:appVersion"],
    "OpenSearch": [
        "charts/olk/values.yaml:opensearch.version",
        f"{HOPSWORKS}:variables.elastic_version",
    ],
    "OpenSearch Dashboards": [
        "charts/olk/values.yaml:dashboard.version",
        f"{HOPSWORKS}:variables.kibana_version",
    ],
    "OpenSearch metrics exporter": [
        "charts/olk/values.yaml:prometheus-elasticsearch-exporter.image.tag"
    ],
    "Payara": [
        f"{HOPSWORKS}:payaraVersion",
        f"{HOPSWORKS}:image.worker.tag",
        f"{HOPSWORKS}:image.postInstall.tag",
    ],
    "Prometheus": [
        f"{PROMETHEUS}:prometheus.server.image.tag",
        "upstream:charts/prometheus/Chart.yaml:prometheus",
        "charts/prometheus/Chart.yaml:appVersion",
    ],
    "Prometheus adapter": [f"{PROMETHEUS}:prometheus-adapter.image.tag"],
    "Prometheus config reloader": [
        f"{PROMETHEUS}:prometheus.configmapReload.prometheus.image.tag",
        f"{PROMETHEUS}:prometheus.alertmanager.configmapReload.image.tag",
    ],
    "Prometheus node exporter": [
        f"{PROMETHEUS}:prometheus.prometheus-node-exporter.image.tag"
    ],
    "Pushgateway": [
        f"{PROMETHEUS}:prometheus.prometheus-pushgateway.image.tag",
        "upstream:charts/prometheus/Chart.yaml:prometheus",
    ],
    "Python in the base environments": [
        f"{HOPSWORKS}:variables.docker_base_image_python_version"
    ],
    "Ray": [f"{HOPSWORKS}:variables.ray_version"],
    "Remote shuffle service (Apache Uniffle)": ["charts/spark/values.yaml:rss.version"],
    "Remote shuffle service init image": [
        "charts/spark/values.yaml:rss.image.initImageVersion"
    ],
    "RonDB": ["rondb:images.rondb.tag"],
    "RonDB MySQL metrics exporter": ["rondb:images.mysqldExporter.tag"],
    "scikit-learn model server": [f"{KSERVE}:kserve.servingruntime.sklearnserver.tag"],
    "Spark": [f"{HOPSWORKS}:variables.spark_version"],
    "Storage initializer": [f"{KSERVE}:storageInitializer.tag"],
    "Spark history server": ["charts/spark/values.yaml:historyServer.image.tag"],
    "Spark operator": [
        "charts/spark/values.yaml:spark-operator.image.tag",
        "charts/spark/values.yaml:spark-operator.hook.image.tag",
        "charts/spark/values.yaml:sparkOperatorUpgradeJob.crdImage.tag",
    ],
    "Strimzi": [
        "charts/kafka/values.yaml:strimzi-kafka-operator.defaultImageTag",
        "charts/kafka/Chart.yaml:appVersion",
        "charts/kafka/values.yaml:crdUpgradeJob.image.tag",
    ],
    "Superset": [
        f"{SUPERSET}:superset.image.tag",
        "charts/superset/Chart.yaml:appVersion",
    ],
    "Superset init image": [f"{SUPERSET}:superset.initImage.tag"],
    "Superset MySQL": [f"{SUPERSET}:mysql.image.tag"],
    "Superset MySQL metrics exporter": [f"{SUPERSET}:mysql.metrics.image.tag"],
    "Superset MySQL volume permissions image": [
        f"{SUPERSET}:mysql.volumePermissions.image.tag"
    ],
    "Superset Redis": [f"{SUPERSET}:superset.redis.image.tag"],
    "Superset Redis metrics exporter": [f"{SUPERSET}:superset.redis.metrics.image.tag"],
    "TensorFlow": [f"{HOPSWORKS}:variables.tensorflow_version"],
    "TensorFlow Serving": [
        f"{KSERVE}:kserve.servingruntime.tensorflow.tag",
        f"{HOPSWORKS}:variables.kube_kserve_tensorflow_version",
    ],
    "Toolbox image (hwutils)": [
        "values.yaml:global._hopsworks.toolbox.tag",
        "values.yaml:rondb.rondb.images.toolbox.tag",
        "rondb:images.toolbox.tag",
        "charts/grafana/values.yaml:grafana.downloadDashboardsImage.tag",
    ],
    "Trino": [
        "values.yaml:global._hopsworks.trino.image.tag",
        "charts/trino/values.yaml:trino.image.tag",
        "charts/trino/Chart.yaml:appVersion",
        "charts/trino/values.yaml:trinotest.image.tag",
    ],
    "Trino authentication seeder": ["charts/trino/values.yaml:authSeeder.image.tag"],
    "Trino mountable-secrets sidecar": [
        "values.yaml:global._hopsworks.trino.mountableSecrets.image.tag"
    ],
    "Vertical Pod Autoscaler": ["charts/vpa/values.yaml:imagesTag"],
    "Vertical Pod Autoscaler installer": ["charts/vpa/values.yaml:image.tag"],
    "vLLM": [
        "values.yaml:global._kserve.servingruntime.vllmopenai.tag",
        f"{KSERVE}:kserve.servingruntime.vllmopenai.tag",
        f"{HOPSWORKS}:variables.kube_serving_vllm_versions",
    ],
    "vLLM-Omni": [
        "values.yaml:global._kserve.servingruntime.vllmomni.tag",
        f"{KSERVE}:kserve.servingruntime.vllmomni.tag",
        f"{HOPSWORKS}:variables.kube_serving_vllm_omni_versions",
    ],
}

# The image tag an upstream chart deploys when the chart doesn't set one, by
# (dependency, version).
UPSTREAM_DEFAULTS = {
    ("prometheus", "25.20.2"): {
        "Prometheus": "v2.51.2",
        "Alertmanager": "v0.27.0",
        "Pushgateway": "v1.8.0",
    },
}

# Rebuilt images whose tag doesn't name what they ship (HES-194, HWORKS-2994).
SHIPS = {
    "8.4.5-debian-12-r0-h2": "MySQL 8.4.10",
    "8.4.5-debian-12-r0-h3": "MySQL 8.4.11",
}

# Version-like values that aren't a component's version: the chart versions, the
# application version, which the line under the page title gives, and settings whose
# name only looks like a version, such as the tag history variables.
IGNORED = re.compile(
    r"(^|.*/)Chart\.yaml:(version|apiVersion|kubeVersion|dependencies\[.*\]\.version)"
    r"|(charts/hopsworks/)?Chart\.yaml:appVersion"
    r"|charts/hopsworks/values\.yaml:variables\.tag_history_\w+"
)
VERSION_KEY = re.compile(r"tag|version|image|digest", re.IGNORECASE)
RELEASE = re.compile(r"v(\d+)\.(\d+)\.(\d+)")
UMBRELLA = re.compile(r"charts/([^/]+)/values\.yaml")


def _git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
    ).stdout


@cache
def _load(repo, tag, path):
    """The YAML at ``tag:path`` with every scalar as a string, or None."""
    try:
        text = _git(repo, "show", f"{tag}:{path}")
    except subprocess.CalledProcessError:
        return None
    try:
        # Trailing tabs, as in charts/prometheus/values.yaml at v5.1.0, are invalid YAML.
        return yaml.load(re.sub(r"[ \t]+$", "", text, flags=re.M), yaml.BaseLoader)
    except yaml.YAMLError as error:
        typer.echo(f"Skipped {tag}:{path}: {str(error).splitlines()[0]}", err=True)
        return None


def _lookup(doc, dotted):
    for part in dotted.split("."):
        if not isinstance(doc, dict) or part not in doc:
            return None
        doc = doc[part]
    return doc


def _dependency(helm, tag, chart, name):
    for dependency in (_load(helm, tag, chart) or {}).get("dependencies") or []:
        if dependency["name"] == name:
            return dependency["version"]
    return None


def _value(helm, rondb, tag, ref, component):
    if ref.startswith("upstream:"):
        chart, name = ref.removeprefix("upstream:").rsplit(":", 1)
        version = _dependency(helm, tag, chart, name)
        if version is None:
            return None
        defaults = UPSTREAM_DEFAULTS.get((name, version))
        if defaults is None:
            raise typer.BadParameter(
                f"{tag} deploys {name} {version}; add its default image tags to "
                "UPSTREAM_DEFAULTS in scripts/release_components.py"
            )
        return defaults.get(component)
    if ref.startswith("rondb:"):
        version = _dependency(helm, tag, "charts/rondb/Chart.yaml", "rondb")
        return version and _lookup(
            _load(rondb, f"v{version}", "values.yaml"), ref.removeprefix("rondb:")
        )
    path, key = ref.split(":", 1)
    subchart = UMBRELLA.fullmatch(path)
    if subchart:
        override = _clean(
            _lookup(_load(helm, tag, "values.yaml"), f"{subchart[1]}.{key}")
        )
        if override:
            return override
    return _lookup(_load(helm, tag, path), key)


def _clean(value):
    if not isinstance(value, str) or value in ("", "null", "~"):
        return None
    # A full image reference: keep its tag.
    if "/" in value and ":" in value:
        return value.rpartition(":")[2]
    return value


def _versions(helm, rondb, tag):
    versions = {}
    for component, refs in COMPONENTS.items():
        values = (_clean(_value(helm, rondb, tag, ref, component)) for ref in refs)
        versions[component] = next((v for v in values if v), None)
    return versions


def _flatten(node, prefix=""):
    if isinstance(node, dict):
        for key, value in node.items():
            yield from _flatten(value, f"{prefix}.{key}" if prefix else key)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            name = value.get("name") if isinstance(value, dict) else None
            yield from _flatten(value, f"{prefix}[{name or index}]")
    else:
        yield prefix, node


def _version_values(repo, tag, paths, prefix=""):
    values = {}
    for path in paths:
        for key, value in _flatten(_load(repo, tag, path) or {}):
            leaf = key.rsplit(".", 1)[-1]
            if (
                VERSION_KEY.search(leaf)
                and isinstance(value, str)
                and re.search(r"\d", value)
                and "{{" not in value
            ):
                values[f"{prefix}{path}:{key}"] = value
    return values


def _covered():
    refs = set()
    for component_refs in COMPONENTS.values():
        for ref in component_refs:
            if ref.startswith("rondb:"):
                refs.add(f"rondb:values.yaml:{ref.removeprefix('rondb:')}")
                continue
            refs.add(ref)
            path, key = ref.split(":", 1)
            subchart = UMBRELLA.fullmatch(path)
            if subchart:
                refs.add(f"values.yaml:{subchart[1]}.{key}")
    return refs


def _uncovered(helm, rondb, old, new):
    """Version changes between the two tags that no component covers."""
    changes = []
    covered = _covered()
    charts = {
        tag: [
            path
            for path in _git(helm, "ls-tree", "-r", "--name-only", tag).split()
            if re.search(r"(^|/)(values\.yaml|Chart\.yaml)$", path)
        ]
        for tag in (old, new)
    }
    before = _version_values(helm, old, charts[old])
    after = _version_values(helm, new, charts[new])
    rondb_tags = [
        _dependency(helm, tag, "charts/rondb/Chart.yaml", "rondb") for tag in (old, new)
    ]
    if all(rondb_tags):
        before |= _version_values(rondb, f"v{rondb_tags[0]}", ["values.yaml"], "rondb:")
        after |= _version_values(rondb, f"v{rondb_tags[1]}", ["values.yaml"], "rondb:")
    for key in sorted(before.keys() | after.keys()):
        changed = before.get(key) != after.get(key)
        if changed and key not in covered and not IGNORED.fullmatch(key):
            changes.append(f"{key}: {before.get(key)} -> {after.get(key)}")
    return changes


def _release(tag):
    match = RELEASE.fullmatch(tag)
    if not match:
        raise typer.BadParameter(f"{tag.removeprefix('v')} is not a release X.Y.Z")
    return tuple(int(part) for part in match.groups())


def _baseline(helm, tag):
    """The tag to compare with, and the tags to mark versions that shipped in."""
    tags = sorted(
        (t for t in _git(helm, "tag", "--list", "v*").split() if RELEASE.fullmatch(t)),
        key=_release,
    )
    major, minor, patch = _release(tag)
    if patch:
        older = [
            t
            for t in tags
            if _release(t)[:2] == (major, minor) and _release(t) < (major, minor, patch)
        ]
        return older[-1], []
    previous = max(_release(t)[:2] for t in tags if _release(t) < (major, minor, 0))
    line = [t for t in tags if _release(t)[:2] == previous]
    return line[0], line[1:]


def _cell(version):
    return f"{version} ({SHIPS[version]})" if version in SHIPS else version


def _marker(tag):
    version = tag.removeprefix("v")
    if version.startswith("4."):
        return f" (also in {version})"
    return f" (also in [{version}][hopsworks-{version.replace('.', '-')}])"


def _table(helm, rondb, old, new, markers):
    before, after = _versions(helm, rondb, old), _versions(helm, rondb, new)
    shipped = [(tag, _versions(helm, rondb, tag)) for tag in markers]
    rows = []
    for component in sorted(COMPONENTS, key=str.lower):
        was, now = before[component], after[component]
        if was == now:
            continue
        if not (was and now):
            typer.echo(
                f"Left out {component}: {'new' if now else 'removed'} in {new}",
                err=True,
            )
            continue
        marker = next((tag for tag, v in shipped if v[component] == now), None)
        rows.append(
            f"| {component} | {_cell(was)} | {_cell(now)}{_marker(marker) if marker else ''} |"
        )
    if not rows:
        return "No components were upgraded in this release.\n"
    old, new = old.removeprefix("v"), new.removeprefix("v")
    header = [
        f"| Component | {old} | {new} |",
        f"| --------- | {'-' * len(old)} | {'-' * len(new)} |",
    ]
    return "\n".join(header + rows) + "\n"


def release_components(
    release: Annotated[str, typer.Argument(help="The release, e.g. 5.1.1.")],
    helm: Annotated[
        Path, typer.Option(help="A hopsworks-helm checkout with the release tags.")
    ],
    rondb_helm: Annotated[
        Path, typer.Option(help="A rondb-helm checkout with its release tags.")
    ],
    since: Annotated[
        str | None,
        typer.Option(
            help="The release to compare with. Defaults to the previous patch, or "
            "for an X.Y.0 to the first release of the previous minor version."
        ),
    ] = None,
    write: Annotated[
        bool,
        typer.Option(
            help="Replace the Upgraded components section of the release page."
        ),
    ] = False,
):
    """Print the Upgraded components table of a release page."""
    tag = f"v{release}"
    old, markers = (f"v{since}", []) if since else _baseline(helm, tag)
    uncovered = _uncovered(helm, rondb_helm, old, tag)
    if uncovered:
        typer.echo(
            "These versions changed but no component in scripts/release_components.py "
            "covers them; add each to COMPONENTS or IGNORED:",
            err=True,
        )
        for change in uncovered:
            typer.echo(f"  {change}", err=True)
        raise typer.Exit(1)
    table = _table(helm, rondb_helm, old, tag, markers)
    if not write:
        typer.echo(table, nl=False)
        return
    page = _DOCS_ROOT / "docs" / "releases" / release.split(".")[0] / f"{release}.md"
    head = page.read_text().split(SECTION)[0].rstrip("\n")
    page.write_text(f"{head}\n{SECTION}\n{table}")
    typer.echo(f"Updated {page.relative_to(_DOCS_ROOT)}", err=True)
