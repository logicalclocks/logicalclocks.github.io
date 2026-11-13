---
description: How to turn on the Hopsworks Semantic Layer with Helm, what runs where, the semantic gateway's values, its memory and time limits, the cluster variables, the endpoints for clients outside the cluster, and the storage of the query history.
---

# Semantic Layer { #semantic-admin }

The Semantic Layer compiles metric definitions written in YAML over feature groups, answers metric queries over REST and Arrow Flight SQL, and answers metadata over GraphQL.
This page turns it on and configures it; [Semantic Layer Guides][semantic-layer-guides] cover its use.

## Turn it on { #semantic-admin-enable }

```yaml
global:
  _hopsworks:
    semanticLayer:
      enabled: true
```

`global._hopsworks.semanticLayer.enabled`, `false` by default, installs:

- the `semantic-gateway` subchart, the semantic gateway;
- the Ingresses that route `/semantic-layer/` and `/semantic-layer/api/graphql` on the Hopsworks ingress hosts to the gateway;
- the backend and UI side: the cluster variable `semantic_layer_enabled` is `true`, and projects show **Semantic Layer** in their sidebar.

While it is off, the semantic layer endpoints answer 404 `SEMANTIC_LAYER_DISABLED`.
Queries run on Trino, so Trino must be installed too.

## What runs where { #semantic-admin-components }

| Component | Runs in | Does |
| --- | --- | --- |
| Control plane | Hopsworks (Payara) | Semantic projects and their builds, sessions for the gateway, the definitions editor, tags, metric exports and their jobs, the query history and its cleaner. Its tables are in the `hopsworks` database in RonDB, and the compiled definitions of each build are files in the project's directory in HopsFS, which only Hopsworks reads and writes and which go with the project. |
| Semantic gateway | The Deployment `semantic-gateway`, 2 replicas by default | Compiles the definitions for the control plane, plans metric queries, runs them on Trino as the caller, and serves REST, GraphQL, Arrow Flight SQL, the BI tables and the result cache. It keeps no state of its own beyond memory. |
| Trino | The `trino` chart | Runs the SQL the gateway plans, as the caller's own Trino user, see [Who a query runs as][semantic-overview-identity]. |
| Export jobs | Python jobs in each project, in the `python-feature-pipeline` environment | Write saved queries into feature groups, see [Metric exports][semantic-exports]. |
| Superset | The `superset` chart | Dashboards from metrics: each member's database connection of a project reads the gateway's Arrow Flight SQL port inside the cluster, at `semantic-gateway.<namespace>.svc.cluster.local:18446`, see [Dashboards in Superset][semantic-superset-dashboards]. |

The gateway's Service, `semantic-gateway`, has four ports:

| Port | Name | Serves |
| --- | --- | --- |
| 18443 | `public` | REST and GraphQL, behind the Ingresses. |
| 18444 | `internal` | Compile and validation requests from Payara; the NetworkPolicy admits only the Payara pods. |
| 18445 | `metrics` | Prometheus metrics, in the release namespace. |
| 18446 | `flight` | Arrow Flight SQL. The Service keeps this port when `flightPort`, the port of the container and of the external load balancer, changes. |

All but `metrics` serve TLS with a certificate from the cluster's CA, the HopsworksCert `semantic-gateway`.
Prometheus and the gateway's probes read `metrics` over plain HTTP.

## Endpoints for clients outside the cluster { #semantic-admin-endpoints }

| Client | Reaches the gateway through | Configured by |
| --- | --- | --- |
| Python, the CLI, the UI, REST | `https://<hopsworks host>/semantic-layer/` | Nothing more: the Ingress on the Hopsworks ingress hosts. |
| GraphQL, dbt-sl-sdk metadata | `https://<hopsworks host>/semantic-layer/api/graphql` | Nothing more. |
| Arrow Flight SQL: dbt-sl-sdk queries, ADBC, JDBC, BI tools | `grpc+tls://<load balancer>:18446` | `semantic-gateway.externalLoadBalancer`, see [The Flight SQL load balancer][semantic-connect-admin-lb]. |
| dbt's Tableau and Power BI connectors | Port 443 of one host, Flight SQL and `/api/graphql` | `hopsworks.semanticLayer.dbtCompatibleLayout`, see [The dbt-compatible endpoint layout][semantic-bi-dbt-layout]. |

```yaml
semantic-gateway:
  externalLoadBalancer:
    enabled: true
    hostname: semantic.hopsworks.example.com
  signingKey:
    existingSecret: semantic-gateway-signing-key

hopsworks:
  variables:
    loadbalancer_external_domain_semantic_gateway: semantic.hopsworks.example.com
  semanticLayer:
    dbtCompatibleLayout:
      enabled: true
      host: semantic.example.com
      tlsSecret: semantic-example-com-tls
```

Set `externalLoadBalancer.hostname` at install: the gateway's certificate takes its names then, and keeps them on an upgrade unless the HopsworksCert `semantic-gateway` is deleted first.
The gateway signs query handles with a key from a Secret; [The signing key][semantic-connect-admin-signing-key] covers creating and rotating it.

## Semantic gateway values { #semantic-admin-gateway-values }

Under `semantic-gateway:`:

| Value | Default | Meaning |
| --- | --- | --- |
| `replicas` | `2` | Replicas of the Deployment; not rendered while `hpa.enabled`, which then uses it as its minimum. |
| `hpa.enabled`, `hpa.maxReplicas`, `hpa.targetCPUUtilizationPercentage` | `false`, `4`, `80` | Autoscale the Deployment on CPU. |
| `podDisruptionBudget.enabled`, `podDisruptionBudget.minAvailable` | `true`, `1` | Keep replicas available through voluntary disruptions, with more than one replica. |
| `resources` | requests `500m`, `4Gi`; limits `2`, `4Gi` | Resources of the gateway container, see [Memory][semantic-admin-memory]. |
| `jvmOptions` | `-XX:MaxRAMPercentage=50` | JVM options, as `JAVA_TOOL_OPTIONS`. |
| `queryTimeoutSeconds` | `300` | Seconds a query runs on Trino before the gateway cancels it. The Ingress read timeouts must not be shorter. |
| `queryConcurrency` | `16` | Queries a replica runs at once; a query that finds no slot within 30 seconds gets 503. |
| `maxRows`, `maxJsonRows` | `1000000`, `100000` | Rows of an Arrow result and of a JSON result. |
| `sessionCacheSeconds` | `60` | Seconds a replica keeps a caller's session before it asks Hopsworks again. |
| `buildCacheEntries` | `100` | Compiled builds a replica keeps in memory. |
| `flightPort` | `18446` | The Arrow Flight SQL port of the gateway and of its external load balancer; change `hopsworks.variables.semantic_gateway_flight_port` with it. Superset and other clients inside the cluster keep using port 18446 of the Service. |
| `biTables.enabled` | `true` | Serve semantic projects as tables over Flight SQL, see [Connect BI tools][semantic-bi-admin]. Experimental. |
| `handleTtlSeconds` | `3600` | Seconds a Flight ticket or prepared statement stays valid. |
| `cache.maxBytes`, `cache.ttlSeconds`, `cache.entryMaxBytes`, `cache.dataVersionSeconds` | `268435456`, `300`, `8388608`, `30` | The [result cache][semantic-result-cache-admin]. |
| `arrowMemoryLimitBytes` | `null` | Arrow buffers a replica's queries hold at once; null is half the JVM heap. |
| `signingKey.existingSecret` | `null` | The Secret with the handle signing key, see [The signing key][semantic-connect-admin-signing-key]. |
| `externalLoadBalancer.*` | | The Flight SQL load balancer: `enabled`, `class`, `annotations`, `managed`, `nodePort`, `nodeSelector`, `hostname`. |
| `networkPolicy.enabled` | `true` | Restrict the gateway's traffic to Payara, Trino and DNS, and its internal and metrics ports to Payara and the release namespace. |
| `image.registry`, `image.repository`, `image.tag`, `image.pullPolicy` | `null`, `hopsworks/semantic-gateway`, `null`, `null` | The gateway image; the tag defaults to the chart's version. |
| `nodeSelector`, `tolerations`, `topologySpreadConstraint` | empty | Scheduling; the global values apply when empty. |

Under `hopsworks.semanticLayer`:

| Value | Default | Meaning |
| --- | --- | --- |
| `ingress.annotations` | HTTPS backend, 300 second timeouts | Annotations of the Ingress for `/semantic-layer/`. Keep the read timeout at least `semantic-gateway.queryTimeoutSeconds`. |
| `graphqlIngress.annotations` | as above | Annotations of the Ingress for `/semantic-layer/api/graphql`. |
| `dbtCompatibleLayout.enabled`, `.host`, `.tlsSecret`, `.timeoutSeconds` | `false`, `""`, `null`, `300` | [The dbt-compatible endpoint layout][semantic-bi-dbt-layout]. |

## Memory { #semantic-admin-memory }

The defaults add up as follows, per replica:

| Part | Size | Set by |
| --- | --- | --- |
| Container memory limit | 4 GiB | `resources.limits.memory` |
| JVM heap | 2 GiB, half the limit | `-XX:MaxRAMPercentage=50` in `jvmOptions` |
| Arrow buffers of the queries in flight, outside the heap | 1 GiB, half the heap | `arrowMemoryLimitBytes` |
| Result cache, on the heap | 256 MiB | `cache.maxBytes` |
| Query history waiting to be sent, on the heap | 64 MiB | |
| JSON and CSV answers, on the heap | 64 MiB per query slot, 16 slots: 1 GiB | `maxJsonBytes`, `queryConcurrency` |
| The JVM's own memory: classes, threads, buffers | The rest of the limit, about 1 GiB | |

The result cache, the history queue and one JSON answer per query slot take 1,344 MiB at the defaults, which fits the 2 GiB heap.
The gateway checks this sum against its heap when it starts, and refuses to start with a message that names the values when the sum is larger: raise `resources.limits.memory` with `cache.maxBytes`, `maxJsonBytes` or `queryConcurrency`.
A gateway whose heap runs out exits, and Kubernetes restarts the pod.

## Time limits and shutdown { #semantic-admin-time-limits }

| Value | Default | Meaning |
| --- | --- | --- |
| `httpRequestTimeoutSeconds` | `120` | Seconds a REST or GraphQL client has to send its request, from its first byte through the TLS handshake to the end of the body. A slower client loses its connection. |
| `httpResponseTimeoutSeconds` | `null` | Seconds an answer may take, from the end of the request to the last byte sent, the query included. Null is twice `queryTimeoutSeconds` plus the 30 seconds a query waits for a slot, plus 240: 900 at the defaults. The gateway refuses to start with a value below `queryTimeoutSeconds` plus 30. |
| `shutdownGraceSeconds` | `45` | Seconds the requests in flight get to finish when the pod is stopped. |

When a pod is stopped, as in a rolling update or a scale-down, the gateway stops accepting connections and Arrow Flight SQL calls, lets the requests in flight finish for `shutdownGraceSeconds`, sends the query history it holds, and exits.
A request still running then loses its connection, and a client sends it again to reach another replica.
Keep the pod's `terminationGracePeriodSeconds` longer than `shutdownGraceSeconds` plus 10 seconds for the history.
A gateway that cannot open one of its ports when it starts exits, so a pod that runs is serving on every port.

## Cluster variables { #semantic-admin-variables }

Set under `hopsworks.variables` at install, or changed later on the [Cluster Configuration][cluster-configuration] page:

| Variable | Default | Meaning |
| --- | --- | --- |
| `semantic_layer_enabled` | `"false"` | The backend and UI side; `true` while `global._hopsworks.semanticLayer.enabled`. Set it alone only for a gateway that runs elsewhere. |
| `semantic_layer_gateway_internal_url` | `""` | Where Payara sends compile requests; empty is the gateway's internal port in the release namespace. |
| `semantic_layer_gateway_cluster_url` | `""` | The gateway's public port for callers inside the cluster; empty is the `semantic-gateway` Service in the release namespace. |
| `superset_semantic_enabled` | `"true"` | The members' semantic connections in Superset and dashboards from metrics. |
| `semantic_layer_staleness_check_seconds` | `"30"` | How often, at most, a query checks whether a semantic project's files or feature groups changed, and compiles it. |
| `semantic_layer_builds_retained` | `"20"` | Builds kept per semantic project. |
| `semantic_gateway_flight_port` | `"18446"` | The Flight SQL port the connection details carry. |
| `loadbalancer_external_domain_semantic_gateway` | `null` | The Flight SQL load balancer's name in the connection details; set it to `semantic-gateway.externalLoadBalancer.hostname`. |
| `semantic_query_strip_details_after_days` | `"7"` | Days after which a record loses its request, SQL and error. |
| `semantic_query_cleaner_batch_size` | `"1000"` | Records the hourly cleaner strips per statement. |

## Query history storage { #semantic-admin-history-storage }

The [query history][semantic-query-history] is the table `hopsworks.semantic_query`, in RonDB's disk tablespace `ts_1`, so the history takes little DataMemory.
Its keys, its indexed columns and the start time stay in memory; the request, the SQL and the error are on disk.
Disk columns have a fixed width, so each record reserves about 13,000 bytes of `ts_1`, and the default 2 GB data file holds about 150,000 records, next to the other tables that store columns on disk, such as feature groups with disk columns.

A record expires 30 days after its query started, by a time to live in the table's definition: RonDB stops returning it, and purges it.
At about 150,000 records per 2 GB, the history alone needs more than the default data file on a cluster that runs more than 5,000 metric queries a day: add room to `ts_1`, or shorten the time to live.
Every query is recorded, those answered from the result cache included, so count each chart refresh of a Superset dashboard.

Check the free space from a MySQL server of RonDB:

```sql
SELECT FILE_NAME,
       FREE_EXTENTS * EXTENT_SIZE / 1024 / 1024 AS free_mb,
       TOTAL_EXTENTS * EXTENT_SIZE / 1024 / 1024 AS total_mb
FROM INFORMATION_SCHEMA.FILES
WHERE TABLESPACE_NAME = 'ts_1' AND FILE_TYPE = 'DATAFILE';
```

Add a data file to `ts_1`, with a name no other data file has:

```sql
ALTER TABLESPACE ts_1 ADD DATAFILE 'ts_1_data_file_1.dat' INITIAL_SIZE = 1G ENGINE ndbcluster;
```

Change the time to live, in seconds, such as 14 days:

```sql
ALTER TABLE hopsworks.semantic_query COMMENT = 'NDB_TABLE=TTL=1209600@started';
```

When `ts_1` has no free extent, the history records that do not fit are lost, and the gateway counts them in `semantic_query_records_dropped_total`; queries keep running.
The `LowDiskDataFileExtents` alert fires when less than 20% of `ts_1` has been free for 5 minutes.

## Monitoring { #semantic-admin-monitoring }

The gateway's metrics port reports, among others:

| Metric | Meaning |
| --- | --- |
| `semantic_gateway_cache_hits_total`, `semantic_gateway_cache_misses_total` | Queries answered from the result cache, and cacheable queries that ran on Trino. |
| `semantic_query_records_sent_total` | Query history records sent to Hopsworks. |
| `semantic_query_records_dropped_total{reason}` | History records lost: `full`, `oversized`, `credential`, `failed` or `rejected`. |

The [result cache][semantic-result-cache-admin] lists its other metrics.
