---
description: Admin guide to the Cluster Settings Costs page, which shows the Kubernetes cost of each namespace or department as computed by OpenCost.
---

# Costs { #cluster-costs }

## Introduction { #costs-introduction }

The _Costs_ page under _Cluster Settings_ shows what the cluster cost over the last hour, day, week, month or year, grouped by Kubernetes namespace or by department.
Each Hopsworks project runs in its own namespace, so a namespace row is the cost of that project's jobs, notebooks, deployments, apps and storage.
The page is available to administrators only.

The cost model is [OpenCost](https://opencost.io/), which runs in its own namespace and reads the Prometheus bundled with the Hopsworks chart.
Hopsworks calls OpenCost from the backend on behalf of administrators and keeps a daily history of the results; the browser never calls OpenCost.

Prices come from OpenCost's pricing configuration.
Without your own prices, OpenCost uses its on-premises default prices, so the numbers show relative cost between namespaces rather than what you pay.
The currency shown next to each amount is a label only: it does not convert anything, and it should name the currency of the prices you configure.

## Prerequisites { #costs-prerequisites }

- An administrator account on the Hopsworks cluster.
- `kubectl` and `helm` access to the Kubernetes cluster that runs Hopsworks, to install OpenCost and to upgrade the Hopsworks chart.
- The examples below assume Hopsworks is installed in namespace `hopsworks` and OpenCost goes into namespace `opencost`.

## Step 1: Install OpenCost { #costs-install-opencost }

OpenCost 1.121.3 does not authenticate its read API and listens on port 9003 on every interface.
Anyone who can reach that port can read the cost of every namespace, so OpenCost is installed behind a `kube-rbac-proxy` sidecar:

- The sidecar listens on HTTPS port 9443 and forwards only `/allocation/compute` to OpenCost on `127.0.0.1:9003`.
- It accepts only service-account tokens issued for the `opencost` audience, and checks each request with a TokenReview and a SubjectAccessReview for `get services/proxy opencost` in namespace `opencost`.
- Only the Hopsworks service account, `hopsworks-service-account`, is granted that permission.
- A NetworkPolicy allows port 9003 only from the Hopsworks Prometheus server and port 9443 only from the Hopsworks pods.
- The OpenCost UI and MCP server are disabled, because both serve the same data without authentication.

The steps below create these objects by hand and install the published chart `opencost/opencost` version 2.5.33 (OpenCost 1.121.3).

### Create the TLS certificate { #costs-tls-certificate }

Set the namespace Hopsworks runs in and the name of its Helm release; every command below uses them.
The Hopsworks Prometheus Service is named after the release, `<release>-prometheus-server`.

```bash
HOPSWORKS_NAMESPACE=hopsworks
HOPSWORKS_RELEASE=hopsworks
```

Create a self-signed certificate for the OpenCost Service and store it in Secret `opencost-tls`.
Then publish only the certificate, without its key, as ConfigMap `opencost-ca` in the Hopsworks namespace, where the Hopsworks pods read it to verify OpenCost.

```bash
kubectl create namespace opencost

openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 -nodes -days 3650 \
  -keyout tls.key -out tls.crt -subj "/CN=opencost.opencost.svc" \
  -addext "subjectAltName=DNS:opencost.opencost.svc,DNS:opencost.opencost.svc.cluster.local"
kubectl -n opencost create secret tls opencost-tls --cert=tls.crt --key=tls.key

kubectl -n "$HOPSWORKS_NAMESPACE" create configmap opencost-ca --from-file=ca.crt=tls.crt
rm tls.key tls.crt
```

### Create the proxy configuration, RBAC and NetworkPolicy { #costs-rbac-networkpolicy }

Apply the proxy configuration, its RBAC, the RoleBinding that lets Hopsworks read OpenCost, and the NetworkPolicy.
The shell fills in `$HOPSWORKS_NAMESPACE`:

```bash
cat <<EOF | kubectl apply -f -
# Every request the proxy accepts is checked as "get services/proxy opencost".
apiVersion: v1
kind: ConfigMap
metadata:
  name: opencost-kube-rbac-proxy
  namespace: opencost
data:
  config.yaml: |
    authorization:
      resourceAttributes:
        namespace: opencost
        apiVersion: v1
        resource: services
        subresource: proxy
        name: opencost
---
# The proxy validates tokens and permissions through the Kubernetes API.
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: opencost-kube-rbac-proxy
rules:
  - apiGroups: [authentication.k8s.io]
    resources: [tokenreviews]
    verbs: [create]
  - apiGroups: [authorization.k8s.io]
    resources: [subjectaccessreviews]
    verbs: [create]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: opencost-kube-rbac-proxy
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: opencost-kube-rbac-proxy
subjects:
  - kind: ServiceAccount
    name: opencost
    namespace: opencost
---
# Hopsworks may read OpenCost through the proxy.
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: opencost-reader
  namespace: opencost
rules:
  - apiGroups: [""]
    resources: [services/proxy]
    resourceNames: [opencost]
    verbs: [get]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: opencost-reader
  namespace: opencost
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: opencost-reader
subjects:
  - kind: ServiceAccount
    name: hopsworks-service-account
    namespace: $HOPSWORKS_NAMESPACE
---
# 9003 only from the Hopsworks Prometheus server, 9443 only from the Hopsworks pods.
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: opencost-ingress
  namespace: opencost
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: opencost
  policyTypes: [Ingress]
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: $HOPSWORKS_NAMESPACE
          podSelector:
            matchLabels:
              app.kubernetes.io/name: prometheus
              app.kubernetes.io/component: server
      ports: [{port: 9003}]
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: $HOPSWORKS_NAMESPACE
          podSelector:
            matchLabels:
              app.kubernetes.io/name: hopsworks
      ports: [{port: 9443}]
EOF
```

The NetworkPolicy takes effect only on a CNI that enforces NetworkPolicy.
On a CNI that does not (for example plain flannel), port 9003 stays reachable from any pod by pod IP; port 9443 is authenticated either way.

### Install the OpenCost chart { #costs-opencost-chart }

Save the following values as `opencost-values.yaml`.
They point OpenCost at the Hopsworks Prometheus, add the `kube-rbac-proxy` sidecar on port 9443, disable the UI and MCP server, and set the prices.

```yaml
# The Hopsworks Prometheus keeps pods carrying these annotations; OpenCost's
# allocation queries read back the cost metrics it exports itself.
podAnnotations:
  prometheus.io/scrape: "true"
  prometheus.io/port: "9003"
  prometheus.io/path: /metrics

podSecurityContext:
  runAsNonRoot: true
  seccompProfile:
    type: RuntimeDefault

opencost:
  exporter:
    # Any name; OpenCost uses it when Prometheus metrics carry no cluster id.
    defaultClusterId: hopsworks
    securityContext:
      allowPrivilegeEscalation: false
      capabilities:
        drop: [ALL]
  prometheus:
    internal:
      enabled: true
      # serviceName and namespaceName are set on the helm command below.
      port: 80
  ui:
    enabled: false
  mcp:
    enabled: false
  extraContainers:
    - name: kube-rbac-proxy
      image: quay.io/brancz/kube-rbac-proxy:v0.18.0
      args:
        - --secure-listen-address=0.0.0.0:9443
        - --upstream=http://127.0.0.1:9003/
        - --tls-cert-file=/etc/opencost-tls/tls.crt
        - --tls-private-key-file=/etc/opencost-tls/tls.key
        - --auth-token-audiences=opencost
        - --allow-paths=/allocation/compute
        - --config-file=/etc/kube-rbac-proxy/config.yaml
      ports:
        - name: https-auth
          containerPort: 9443
          protocol: TCP
      volumeMounts:
        - name: opencost-tls
          mountPath: /etc/opencost-tls
          readOnly: true
        - name: kube-rbac-proxy-config
          mountPath: /etc/kube-rbac-proxy
          readOnly: true
      resources:
        requests:
          cpu: 10m
          memory: 32Mi
        limits:
          memory: 128Mi
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        runAsNonRoot: true
        capabilities:
          drop: [ALL]
  # Hourly prices in the currency you display. These are OpenCost's on-prem defaults.
  customPricing:
    enabled: true
    provider: custom
    costModel:
      description: On-prem pricing (OpenCost defaults)
      CPU: 0.031611
      spotCPU: 0.006655
      RAM: 0.004237
      spotRAM: 0.000892
      GPU: 0.95
      storage: 0.00005479452
      zoneNetworkEgress: 0.01
      regionNetworkEgress: 0.01
      internetNetworkEgress: 0.12

service:
  extraPorts:
    - name: https-auth
      port: 9443
      targetPort: 9443

extraVolumes:
  - name: opencost-tls
    secret:
      secretName: opencost-tls
  - name: kube-rbac-proxy-config
    configMap:
      name: opencost-kube-rbac-proxy
```

To price the cluster at your own rates, replace the numbers under `opencost.customPricing.costModel`.

```bash
helm repo add opencost https://opencost.github.io/opencost-helm-chart
helm repo update opencost
helm upgrade --install opencost opencost/opencost \
  --namespace opencost \
  --version 2.5.33 \
  --values opencost-values.yaml \
  --set-string opencost.prometheus.internal.serviceName="$HOPSWORKS_RELEASE-prometheus-server" \
  --set-string opencost.prometheus.internal.namespaceName="$HOPSWORKS_NAMESPACE" \
  --wait --timeout 10m
```

OpenCost's API is now at `https://opencost.opencost.svc.cluster.local:9443`.
The OpenCost pod runs two containers, the exporter and the proxy:

```bash
kubectl -n opencost get pods -l app.kubernetes.io/name=opencost
```

```text
NAME                        READY   STATUS    RESTARTS   AGE
opencost-<suffix>           2/2     Running   0          2m
```

Check that OpenCost refuses unauthenticated reads, from a throwaway pod in another namespace:

```bash
kubectl run -n default opencost-probe --rm -i --restart=Never --image=curlimages/curl -- \
  curl -sk -m 5 -o /dev/null -w '%{http_code}\n' \
  https://opencost.opencost.svc.cluster.local:9443/allocation/compute
```

It prints `401`, or times out where the CNI enforces the NetworkPolicy.
The same request to `http://opencost.opencost.svc.cluster.local:9003/allocation/compute` must time out.
If it answers, the CNI does not enforce the NetworkPolicy, and every pod in the cluster can read every namespace's costs on that port.

The end-to-end check is the _Costs_ page after [Step 2][costs-enable-hopsworks]: if a piece is missing, the page names it, see [Troubleshooting][costs-troubleshooting].

### Air-gapped clusters { #costs-air-gapped }

Mirror the two images the install pulls into your registry, from `docker.hops.works` or from their origin:

- `docker.hops.works/ghcr.io/opencost/opencost:1.121.3` (origin `ghcr.io/opencost/opencost:1.121.3`), the OpenCost exporter.
- `docker.hops.works/quay.io/brancz/kube-rbac-proxy:v0.18.0` (origin `quay.io/brancz/kube-rbac-proxy:v0.18.0`), the proxy sidecar.

The OpenCost UI image (`ghcr.io/opencost/opencost-ui`) is not needed, because the UI is disabled.

Download the chart on a machine with internet access and install it from the archive:

```bash
helm pull opencost/opencost --version 2.5.33
helm upgrade --install opencost ./opencost-2.5.33.tgz \
  --namespace opencost \
  --values opencost-values.yaml \
  --set opencost.exporter.image.registry=<your-registry> \
  --set opencost.exporter.image.repository=<path>/opencost \
  --set opencost.exporter.image.tag=1.121.3 \
  --set-string opencost.prometheus.internal.serviceName="$HOPSWORKS_RELEASE-prometheus-server" \
  --set-string opencost.prometheus.internal.namespaceName="$HOPSWORKS_NAMESPACE" \
  --wait --timeout 10m
```

Setting `image.tag` replaces the chart's pinned reference, `1.121.3@sha256:4cdd173253e5abba048dfe2cfa968707a5b59d774157d5356940d0d923a6c281`, so the digest is no longer checked.
Mirror that digest to keep the same image.

Point the sidecar `image` under `opencost.extraContainers` in `opencost-values.yaml` at your mirror of `kube-rbac-proxy` as well.

## Step 2: Enable Costs in Hopsworks { #costs-enable-hopsworks }

Set `hopsworks.opencost.enabled` to `true` in the values of the Hopsworks Helm chart and upgrade the release:

```yaml
hopsworks:
  opencost:
    enabled: true
```

This does two things:

- It sets the cluster configuration variable `enable_opencost` to `true`, which adds _Costs_ to the _Cluster Settings_ sidebar and starts the daily cost history.
- It mounts a projected volume on the Hopsworks server pods (`hopsworks-instance` and `hopsworks-admin`) at `/var/run/secrets/opencost`, holding a service-account token for the `opencost` audience (`token`, 3600 seconds, rotated by the kubelet) and the `ca.crt` key of ConfigMap `opencost-ca`.

The token is valid for OpenCost only: its audience is `opencost`, so the Kubernetes API does not accept it.
The ConfigMap is optional in the volume, so the pods start without it, but the _Costs_ page reports a missing certificate until it exists.

The settings are these Helm values:

| Helm value | Default | Meaning |
| --- | --- | --- |
| `hopsworks.opencost.enabled` | `false` | Sets `enable_opencost` and mounts the credentials volume. |
| `hopsworks.opencost.caConfigMapName` | `opencost-ca` | ConfigMap in the Hopsworks namespace whose `ca.crt` key holds the OpenCost certificate. |
| `hopsworks.variables.opencost_api_url` | `https://opencost.opencost.svc.cluster.local:9443` | OpenCost API URL, in the form `https://host:port` with no path. Plain `http` is refused, because the token would cross the network in cleartext. |
| `hopsworks.variables.opencost_currency` | `USD` | Currency label shown next to every amount. Display only. |
| `hopsworks.variables.opencost_history_retention_days` | `400` | Days of daily namespace cost history kept in the database. |

Set these in the Helm values, not in the [Cluster Configuration][cluster-configuration] page.
The chart writes `enable_opencost` and the `opencost_*` variables into the database on every install and upgrade, so a change made in the UI is reset by the next `helm upgrade`.

## Step 3: View the costs { #costs-view }

Click on your name in the top right corner of the navigation bar, choose _Cluster Settings_, then choose _Costs_ in the left sidebar.
The page URL keeps the window, the grouping and the chart view (`?window=MONTH&group=department&view=workload`), so a view can be shared as a link.

### Toolbar { #costs-toolbar }

- **Window**: _Last hour_, _Last day_, _Last week_ (the default), _Last month_ or _Last year_.
- **Group by**: _Namespace_ or _Department_.
- **Export CSV**: downloads the table, including the CPU core-hours and RAM GiB-hours requested and used behind each efficiency.
- **Refresh**: fetches the window again.

### Summary { #costs-summary }

The summary bar above the chart shows:

- **Total**: the cost of the whole cluster over the window, idle capacity included.
- **Idle**: the cost of node capacity no pod requested.
- **GPU workloads** and **CPU workloads**: the cost of the workloads in each class, as defined in [GPU and CPU workloads][costs-gpu-cpu-workloads].
- **Efficiency**: the cost-weighted efficiency of all namespaces, see [Efficiency][costs-efficiency].
- **Window**: the start and end of the window in UTC.
- **Coverage**: shown only when some buckets of the window have no data, for example "Data for 5 of 7 days".

When some buckets have no data, a notice above the chart says where the data starts and why the earlier buckets are empty.

### Cost over time { #costs-chart }

The chart stacks the cost of each bucket of the window: 10-minute intervals for the last hour, hours for the last day, days for the last week and month, and calendar months for the last year.
All times are UTC, and the bucket that has not ended yet is marked _in progress_.

- **By namespace** (or **By department**): the 8 most expensive namespaces or departments of the window, then _Other_, then _Idle_. In the department grouping, _Not a project_ is its own series. A namespace keeps one colour across all buckets.
- **By workload**: GPU workloads, CPU workloads, Idle and Unmounted.

A bucket without data has no bar and a _No data_ band, because its cost is unknown, which is different from a cost of zero.

### Table { #costs-table }

The table lists one row per namespace (or department), sorted by total cost, most expensive first:

| Column | Content |
| --- | --- |
| Namespace or Department | The namespace, or the department name. |
| Department | Namespace grouping only: the department of the namespace's project, or a dash when the namespace belongs to no project or is shared by projects of different departments. |
| Namespaces | Department grouping only: how many namespaces the row sums. |
| CPU, GPU, RAM, Storage, Network | The cost of each resource. GPU is the cost of the GPUs alone. |
| Other | Load balancers, shared and external costs. |
| Total | The sum of the cost columns. |
| GPU workloads, CPU workloads | The row's total split by workload class. They add up to Total for namespace, department and Not a project rows; Idle capacity and Unmounted volumes have no workloads, so these columns show a dash there and are 0 in the API. |
| Share | The row's total as a fraction of the window's total. |
| Efficiency | Used over requested CPU and RAM, see [Efficiency][costs-efficiency]. |

Three rows are not projects:

- **Idle capacity**: node capacity that no pod requested.
- **Unmounted volumes**: persistent volumes and load balancers that no pod uses.
- **Not a project** (department grouping only): namespaces that belong to no project, such as the Hopsworks namespace, `kube-system`, `opencost` and the namespaces of deleted projects, plus namespaces shared by projects of different departments.

When the table is narrower than about 1150 pixels, the GPU, Network and Other columns are hidden.
Below about 900 pixels, Department and the workload columns are hidden too.
All columns are in the CSV export.

### Departments { #costs-departments }

The department grouping sums each namespace into the department of the project that uses it.

- The project's current department is used for the whole window, so a project moved to another department takes its past cost with it.
- A project without a department is counted in the default department.
- The totals are the same in both groupings for the same window.

## Step 4: Read the costs from Python or the CLI { #costs-python-cli }

The Python API and the `hops` CLI return the same data as the page.
The account must be a platform administrator; an API key needs the `ADMIN` scope.

```python
import hopsworks


hopsworks.login()
costs_api = hopsworks.get_costs_api()

costs = costs_api.get_namespace_costs("month")
print(costs.total_cost, costs.currency)
print(costs.coverage.observed_buckets, "of", costs.coverage.total_buckets, "buckets")

df = costs.to_pandas()
print(df[["namespace", "department_name", "total_cost", "share"]])

departments = costs_api.get_department_costs("week")
for row in departments.items:
    if row.kind == "DEPARTMENT":
        print(row.department_name, row.namespace_count, row.total_cost)
```

The window is one of `hour`, `day`, `week` (the default), `month` or `year`.
Each row has a `kind`: `NAMESPACE`, `DEPARTMENT`, `UNASSIGNED` (Not a project), `IDLE` or `UNMOUNTED`.

The CLI prints the table, a coverage line when some buckets have no data, and the totals:

```bash
hops admin costs --window month
hops admin costs --window week --by department
hops admin costs --window day --json
```

`--window` takes the same values as the Python API, `--by` takes `namespace` (the default) or `department`, and `--json` prints the full response.
The last two lines of the table output have this form:

```text
Total <total> <currency>, idle <idle>, efficiency <efficiency>, <window> from <start> to <end> (UTC)
GPU workloads: <gpu workloads> | CPU workloads: <cpu workloads>
```

The REST API is under `/hopsworks-api/api/admin/costs`, for platform administrators, with a session or an API key with the `ADMIN` scope:

```text
GET /hopsworks-api/api/admin/costs/namespaces?window=<HOUR|DAY|WEEK|MONTH|YEAR>
GET /hopsworks-api/api/admin/costs/departments?window=<HOUR|DAY|WEEK|MONTH|YEAR>
```

`window` defaults to `WEEK`.
Both answer the JSON the Python API reads: `window`, `start`, `end`, `currency`, `coverage`, `totals`, `items` and `buckets`.
A field without a value is left out of the JSON rather than sent as `null`.
An unknown window answers HTTP 400, and a caller who is not an administrator HTTP 403.
Cost tracking turned off answers HTTP 404 with error code 100083, and OpenCost unreachable HTTP 503 with error code 100081.

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-function"></code> [`hopsworks.get_costs_api`][hopsworks.get_costs_api]
    - <code class="doc-symbol doc-symbol-class"></code> [`CostsApi`][hopsworks_common.core.costs_api.CostsApi]
        - <code class="doc-symbol doc-symbol-method"></code> [`get_namespace_costs`][hopsworks_common.core.costs_api.CostsApi.get_namespace_costs]
        - <code class="doc-symbol doc-symbol-method"></code> [`get_department_costs`][hopsworks_common.core.costs_api.CostsApi.get_department_costs]
    - <code class="doc-symbol doc-symbol-class"></code> [`NamespaceCosts`][hopsworks_common.cost.NamespaceCosts]
        - <code class="doc-symbol doc-symbol-method"></code> [`to_pandas`][hopsworks_common.cost.NamespaceCosts.to_pandas]
    - <code class="doc-symbol doc-symbol-class"></code> [`CostRow`][hopsworks_common.cost.CostRow]
    - <code class="doc-symbol doc-symbol-docs"></code> [OpenCost docs](https://opencost.io/docs/)

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>

### Project costs for data owners { #costs-project-data-owners }

A project's data owners can read the cost of that project without being platform administrators, see [Project costs][project-costs-introduction].

## How the costs are computed { #costs-computation }

### History and retention { #costs-history }

OpenCost stores nothing itself: it recomputes costs from Prometheus, which keeps 7 days of metrics.
The last hour and the last day are computed by OpenCost on request.
Hopsworks stores the cost of each namespace for every complete UTC day, checking once an hour, and keeps those days for `opencost_history_retention_days` (400 by default).
The last week, month and year are read from the stored days, and OpenCost computes only the days not stored yet, usually today.

The stored days are rows of the Hopsworks database table `hopsworks.namespace_daily_cost` (one row per namespace and day), so they are included in RonDB backups and restored with the cluster.
Reinstalling or upgrading OpenCost loses no history and needs nothing copied back: OpenCost has no store of its own, and Hopsworks serves the stored days without it.
While OpenCost is not installed, the last week, month and year show the stored days, and the last hour and day say that OpenCost is not reachable.
Losing Prometheus data loses only the days not stored yet: today, and yesterday until two hours after midnight UTC.

History starts when OpenCost and Hopsworks with Costs enabled are both installed.
A day is stored only while Prometheus still holds it, so a day is lost if Hopsworks is down for longer than 7 days after it.

### Coverage { #costs-coverage }

A bucket without any data, for example before OpenCost was installed, is reported as unobserved and is not counted as zero cost.
The totals and the table cover the observed buckets only, and the coverage line says how many buckets that is.

### Data freshness { #costs-freshness }

Completed hourly and 10-minute buckets are cached for up to one hour, and the current bucket is refreshed live, about every 30 seconds.
Hopsworks therefore shows what OpenCost has computed within a minute, and the cost of finished periods at most an hour late.
A workload that just started can still take up to 5 minutes to appear, because OpenCost samples Prometheus every 5 minutes.
Hopsworks fills this cache in the background every 10 minutes, so a page load normally only waits for the current bucket, under a second.
Right after Hopsworks restarts, the first load of the Last day and Last week windows can take up to about 15 seconds, until the first background fill a minute after start.

### Efficiency { #costs-efficiency }

CPU efficiency is CPU core-hours used divided by CPU core-hours requested, and RAM efficiency is the same for RAM byte-hours.
The Efficiency column weights CPU and RAM efficiency by their cost.
It shows:

- `No requests` when the namespace used CPU and RAM without requesting any, where OpenCost would report 100%.
- A dash for idle capacity, unmounted volumes, and namespaces that requested nothing.

An efficiency above 100% means pods used more than they requested.
Month and year efficiencies are computed from the summed hours of the stored days, not averaged from daily percentages.

### GPU and CPU workloads { #costs-gpu-cpu-workloads }

A workload is a Kubernetes controller: a Job, Deployment, StatefulSet, SparkApplication, DaemonSet and so on.
In each hour, or each 10-minute interval in the last hour, a workload that requested GPU-hours is a GPU workload, and every other workload is a CPU workload.
The class takes the workload's whole cost, including its CPU, RAM, storage and network, so GPU workloads is larger than the GPU column, which is the cost of the GPUs alone.
A workload can be a GPU workload in one hour and a CPU workload in the next.
In a day, month or year it is split between the two classes by the hours in which it requested a GPU.

Pods without a controller share one workload per namespace and are classified together.
Hopsworks jobs, notebooks, deployments and apps all have controllers.

### Limitations { #costs-limitations }

- OpenCost samples Prometheus every 5 minutes.
  A pod that starts and finishes between two samples, such as a job that runs for 30 seconds, may get no cost at all.
- Costs can be slightly negative on a fresh OpenCost install, because of OpenCost's adjustments; they are shown as they are.
- Costs follow OpenCost's pricing configuration.
  Change the prices in the OpenCost values and the currency label in `opencost_currency` together.

## Troubleshooting { #costs-troubleshooting }

When Hopsworks cannot read OpenCost, the page shows _OpenCost is not available_ with the cause, and the API returns HTTP 503 with error code 100081.
Every cause starts with `OpenCost is not reachable at <url>:`, followed by one of the details below.

| Message | Cause and fix |
| --- | --- |
| A connection error, such as `UnknownHostException` or `ConnectException` | OpenCost is not running, or `opencost_api_url` does not point at the proxy. Check the OpenCost pod and the URL, and on an enforcing CNI check that the NetworkPolicy admits the Hopsworks pods on 9443. |
| `OpenCost asked for a token (401), and there is none at /var/run/secrets/opencost/token` | The credentials volume is not mounted. Set `hopsworks.opencost.enabled: true` and upgrade the Hopsworks chart. |
| `OpenCost rejected Hopsworks' token (401): it must be a service-account token for the opencost audience` | The proxy's `--auth-token-audiences` does not match the token's audience `opencost`. |
| `The token at /var/run/secrets/opencost/token is not for the opencost audience, so it is not sent` | Something other than the chart's credentials volume is mounted there. Hopsworks sends only tokens for the `opencost` audience. |
| `OpenCost denied Hopsworks (403): check the opencost-reader RoleBinding in the OpenCost namespace` | The `opencost-reader` RoleBinding is missing or names another service account or namespace. |
| `No OpenCost certificate at /var/run/secrets/opencost/ca.crt: ...` | ConfigMap `opencost-ca` with key `ca.crt` is missing from the Hopsworks namespace. Recreate it as in [Recreate the certificate ConfigMap][costs-recreate-ca]. Right after OpenCost is reinstalled this message is expected for about a minute, until the kubelet updates the file in the Hopsworks pods. |
| `OpenCost has no /allocation/compute at this URL (404)` | `opencost_api_url` points at something other than OpenCost. |
| `OpenCost rejected the query: ...` | OpenCost answered HTTP 400 to the query Hopsworks built, usually because its version is not the one this guide installs. |
| `opencost_api_url is misconfigured: expected https://host:port, got ...` | The URL is not `https`, or has a path, query or credentials in it. |

A page that loads but shows no namespaces at all usually means OpenCost reads the wrong Prometheus.
Check that `opencost.prometheus.internal.serviceName` and `namespaceName` name the Hopsworks Prometheus Service, `<release>-prometheus-server` in the Hopsworks namespace.

### Recreate the certificate ConfigMap { #costs-recreate-ca }

Recreate `opencost-ca` from the certificate the proxy already serves, so that it matches the running proxy:

```bash
kubectl -n opencost get secret opencost-tls -o jsonpath='{.data.tls\.crt}' | base64 -d > ca.crt
kubectl -n "$HOPSWORKS_NAMESPACE" create configmap opencost-ca --from-file=ca.crt
rm ca.crt
```

A new certificate from [Create the TLS certificate][costs-tls-certificate] does not match the running proxy unless Secret `opencost-tls` is replaced too and OpenCost restarted.

### Cost tracking turned off { #costs-turned-off }

When `enable_opencost` is `false`, _Costs_ is not in the sidebar, the page says _Cost tracking with OpenCost is not enabled on this cluster_, and the API returns HTTP 404 with error code 100083.
Set `hopsworks.opencost.enabled: true` and upgrade the Hopsworks chart.
