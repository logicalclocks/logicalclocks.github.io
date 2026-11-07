---
description: How the semantic gateway caches metric query results, what invalidates a cached result, how fresh a cached answer is, and how to skip the cache.
---

# Result Cache { #semantic-result-cache }

Each replica of the semantic gateway keeps the results of metric queries in memory, and answers a repeated query from there instead of running it on Trino.
A cached result is never served after a feature group it read has a new commit, or once the project can no longer read that feature group, within the bounds under [Freshness][semantic-result-cache-freshness].

## What is cached { #semantic-result-cache-what }

The cache holds the results of the queries that run on Trino, from every surface of the gateway:

| Surface | Cached |
| --- | --- |
| REST | `query`, as JSON and as Arrow, and `dimension-values`: the Python client, the `hops` CLI, the query workbench in the UI, the agent tools and Superset charts. |
| Arrow Flight SQL | `semantic_layer.query(...)` and `semantic_layer.dimension_values(...)`: dbt-sl-sdk queries, ADBC and JDBC. |
| GraphQL | `createQuery` and `createDimensionValuesQuery`. |

Listings of metrics, dimensions, entities and saved queries, and the SQL of a query, come from the build without running anything, so they are not cached.

A result is cached under a key made of:

- the surface, so a JSON and an Arrow answer to one query are two entries;
- the build that planned the query, so a newly served build starts with no entries;
- the request as the surface received it, and any SQL around a dbt JDBC call;
- the row cap of the answer;
- the caller's Trino user, `<project>__<user>`, so two users never share an entry;
- the time of the latest commit of every feature group the query reads, the time spine included.

Each replica keeps its own cache: a repeated query that reaches another replica runs on Trino.
A replica keeps up to 256 MiB of results, each for up to 300 seconds, and drops the least recently used first when it is full.

## What invalidates a result { #semantic-result-cache-invalidation }

Before it answers from the cache, the gateway asks Hopsworks, with the caller's credential, for each feature group the build reads: the time of its latest commit, and whether the project can still read it.

| Change | Effect |
| --- | --- |
| A write that records a commit on a feature group, such as `fg.insert(df)` | The commit time changes the key, so the next query runs on Trino. |
| A newly served build, after a compile or a promote | The build id changes the key. |
| A feature group deleted, or no longer shared with the project | The query runs on Trino, which refuses it or reads what the project can still read. |
| A member removed from the project | The member's queries are refused. |
| 300 seconds since the result was cached | The entry is dropped. |

## Freshness { #semantic-result-cache-freshness }

A replica reuses Hopsworks' answer on commits and access for 30 seconds per caller, semantic project and build, and a caller's session for 60 seconds.

| After | A cached result can still be served for up to |
| --- | --- |
| A new commit on a feature group the query reads | 30 seconds |
| A share revoked, or a feature group deleted | 30 seconds |
| A member removed, or a role changed | 60 seconds |

A query that runs on Trino reads the data and the access of that moment, as without a cache.

## What is never cached { #semantic-result-cache-never }

- A query over a feature group shared with the project with only some of its features: the shared features can change without a commit, so Hopsworks reports it as not readable for the cache, and every such query runs on Trino.
- A query over a feature group without commits, such as one without time travel or an external feature group: it has no commit time to key on.
- A result larger than 8 MiB: it streams to the client and is not kept.
- A query while Hopsworks cannot answer for commits and access: it runs on Trino.
- The runs of [metric exports][semantic-exports], which always read the data as it is.

A JSON answer of the REST `query` endpoint says in its `X-Semantic-Cache` header whether the cache answered it:

| Value | Meaning |
| --- | --- |
| `hit` | The gateway pod answered from its cache. |
| `miss` | The query ran on Trino, and the pod keeps its result when it fits in the cache. |
| `bypass` | The query ran on Trino without the cache: `"cache": false`, or a feature group whose version Hopsworks could not tell. |

Each gateway pod has its own cache, so with several pods a repeated query can be a `miss` on a pod that has not run it yet.

## Skip the cache { #semantic-result-cache-skip }

Each surface takes an option that runs the query on Trino and leaves the cache as it is:

| Client | Option |
| --- | --- |
| Python | `sales.query(..., read_cache=False)` |
| CLI | `hops semantic query sales --metrics revenue --no-cache` |
| REST | `"cache": false` in the `query` or `dimension-values` body |
| GraphQL | `createQuery(..., readCache: false)` |
| dbt's JDBC dialect | `{{ semantic_layer.query(..., read_cache=False) }}` |
| dbt-sl-sdk | `client.query(..., read_cache=False)` |

```bash
hops semantic query sales --metrics revenue --group-by customer__country --no-cache
```

```text
customer__country  revenue
-----------------  -------
SE                 190.75
US                 125.75
DE                 75.5
```

## For administrators { #semantic-result-cache-admin }

| `semantic-gateway` value | Default | Meaning |
| --- | --- | --- |
| `cache.maxBytes` | `268435456` | The results a replica keeps, in bytes. |
| `cache.ttlSeconds` | `300` | How long a result is served from the cache. |
| `cache.entryMaxBytes` | `8388608` | The largest result the cache keeps. |
| `cache.dataVersionSeconds` | `30` | How long a replica reuses Hopsworks' answer on commits and access, which bounds how long a cached result outlives a commit or a revoked share. |

The gateway's metrics port reports the cache:

| Metric | Meaning |
| --- | --- |
| `semantic_gateway_cache_hits_total` | Queries answered from the cache. |
| `semantic_gateway_cache_misses_total` | Cacheable queries that ran on Trino. |
| `semantic_gateway_cache_evictions_total` | Results dropped to make room. |
| `semantic_gateway_cache_bytes` | The bytes the cache holds. |
| `semantic_gateway_data_version_lookups_total` | Questions to Hopsworks on commits and access. |

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-class"></code> [`SemanticProject`][hopsworks_common.semantic_layer.SemanticProject]
        - <code class="doc-symbol doc-symbol-method"></code> [`query`][hopsworks_common.semantic_layer.SemanticProject.query]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>
