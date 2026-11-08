---
description: How to turn on the Hopsworks Semantic Layer with Helm, what runs where, the semantic gateway's values, the cluster variables, the endpoints for clients outside the cluster, and the storage of the query history.
---

# Semantic Layer { #semantic-admin }

The Semantic Layer compiles metric definitions written in YAML over feature groups, and answers metric queries over REST, GraphQL and Arrow Flight SQL.
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
| Control plane | Hopsworks (Payara) | Semantic projects and their builds, sessions for the gateway, the definitions editor, tags, metric exports and their jobs, the query history and its cleaner. Its tables are in the `hopsworks` database in RonDB. |
| Semantic gateway | The Deployment `semantic-gateway`, 2 replicas by default | Compiles the definitions for the control plane, plans metric queries, runs them on Trino as the caller, and serves REST, GraphQL, Arrow Flight SQL, the BI tables and the result cache. It keeps no state of its own beyond memory. |
| Trino | The `trino` chart | Runs the SQL the gateway plans, as the caller's own Trino user. |
| Export jobs | Python jobs in each project, in the `python-feature-pipeline` environment | Write saved queries into feature groups, see [Metric exports][semantic-exports]. |
| Superset | The `superset` chart | Dashboards from metrics on Superset 7.0, see [Dashboards in Superset][semantic-superset-dashboards]. |

The gateway's Service, `semantic-gateway`, has four ports:

| Port | Name | Serves |
| --- | --- | --- |
| 18443 | `public` | REST and GraphQL, behind the Ingresses. |
| 18444 | `internal` | Compile and validation requests from Payara; the NetworkPolicy admits only the Payara pods. |
| 18445 | `metrics` | Prometheus metrics, in the release namespace. |
| 18446 | `flight` | Arrow Flight SQL, `flightPort`. |

All of them serve TLS with a certificate from the cluster's CA, the HopsworksCert `semantic-gateway`.

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
| `resources` | requests `500m`, `2Gi`; limits `2`, `2Gi` | Resources of the gateway container. |
| `jvmOptions` | `-XX:MaxRAMPercentage=75` | JVM options, as `JAVA_TOOL_OPTIONS`. |
| `queryTimeoutSeconds` | `300` | Seconds a query runs on Trino before the gateway cancels it. The Ingress read timeouts must not be shorter. |
| `queryConcurrency` | `16` | Queries a replica runs at once; a query that finds no slot within 30 seconds gets 503. |
| `maxRows`, `maxJsonRows` | `1000000`, `100000` | Rows of an Arrow result and of a JSON result. |
| `sessionCacheSeconds` | `60` | Seconds a replica keeps a caller's session before it asks Hopsworks again. |
| `buildCacheEntries` | `100` | Compiled builds a replica keeps in memory. |
| `flightPort` | `18446` | The Arrow Flight SQL port; change `hopsworks.variables.semantic_gateway_flight_port` with it. |
| `biTables.enabled` | `true` | Serve semantic projects as tables over Flight SQL, see [Connect BI tools][semantic-bi-admin]. Experimental. |
| `handleTtlSeconds` | `3600` | Seconds a Flight ticket, prepared statement or GraphQL query id stays valid. |
| `cache.maxBytes`, `cache.ttlSeconds`, `cache.entryMaxBytes`, `cache.dataVersionSeconds` | `268435456`, `300`, `8388608`, `30` | The [result cache][semantic-result-cache-admin]. |
| `graphql.resultMaxBytes`, `graphql.storeMaxBytes`, `graphql.resultTtlSeconds` | `67108864`, `536870912`, `600` | GraphQL results a replica stores for polling. |
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
| `graphqlIngress.annotations` | as above, with `upstream-hash-by: "$http_authorization"` | Annotations of the Ingress for `/semantic-layer/api/graphql`. Keep `upstream-hash-by`, which sends the polls of a GraphQL query to the replica that holds its result. |
| `dbtCompatibleLayout.enabled`, `.host`, `.tlsSecret`, `.timeoutSeconds` | `false`, `""`, `null`, `300` | [The dbt-compatible endpoint layout][semantic-bi-dbt-layout]. |

## Cluster variables { #semantic-admin-variables }

Set under `hopsworks.variables` at install, or changed later on the [Cluster Configuration][cluster-configuration] page:

| Variable | Default | Meaning |
| --- | --- | --- |
| `semantic_layer_enabled` | `"false"` | The backend and UI side; `true` while `global._hopsworks.semanticLayer.enabled`. Set it alone only for a gateway that runs elsewhere. |
| `semantic_layer_gateway_internal_url` | `""` | Where Payara sends compile requests; empty is the gateway's internal port in the release namespace. |
| `semantic_layer_gateway_cluster_url` | `""` | Where Superset's semantic layer extension calls the gateway; empty is the gateway's public port. |
| `superset_semantic_enabled` | `"true"` | Dashboards from metrics on Superset 7.0. |
| `semantic_layer_staleness_check_seconds` | `"30"` | How often, at most, a query checks whether a semantic project's files or feature groups changed, and compiles it. |
| `semantic_layer_builds_retained` | `"20"` | Builds kept per semantic project. |
| `semantic_gateway_flight_port` | `"18446"` | The Flight SQL port the connection details carry. |
| `loadbalancer_external_domain_semantic_gateway` | `null` | The Flight SQL load balancer's name in the connection details; set it to `semantic-gateway.externalLoadBalancer.hostname`. |
| `semantic_query_delete_after_days` | `"30"` | Days a query history record is kept. |
| `semantic_query_strip_details_after_days` | `"7"` | Days after which a record loses its request, SQL and error. |
| `semantic_query_cleaner_batch_size` | `"1000"` | Records the hourly cleaner deletes or strips per statement. |

## Query history storage { #semantic-admin-history-storage }

The [query history][semantic-query-history] is the table `hopsworks.semantic_query`, in RonDB's disk tablespace `ts_1`, so the history takes little DataMemory.
Its keys and indexed columns stay in memory; the request, the SQL and the error are on disk.
Disk columns have a fixed width, so each record reserves about 13,000 bytes of `ts_1`, and the default 2 GB data file holds about 150,000 records, next to the other tables that store columns on disk, such as feature groups with disk columns.

Size `ts_1` for the queries the retention keeps: about 150,000 queries per 2 GB, within `semantic_query_delete_after_days`.
A shorter retention keeps fewer records.
Check the free space from a MySQL server of RonDB:

```sql
SELECT FILE_NAME,
       FREE_EXTENTS * EXTENT_SIZE / 1024 / 1024 AS free_mb,
       TOTAL_EXTENTS * EXTENT_SIZE / 1024 / 1024 AS total_mb
FROM INFORMATION_SCHEMA.FILES
WHERE TABLESPACE_NAME = 'ts_1' AND FILE_TYPE = 'DATAFILE';
```

and add a data file, with a name no other data file has:

```sql
ALTER TABLESPACE ts_1 ADD DATAFILE 'ts_1_data_file_1.dat' INITIAL_SIZE = 1G ENGINE ndbcluster;
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
