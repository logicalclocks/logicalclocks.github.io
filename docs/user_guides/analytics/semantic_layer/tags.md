---
description: How to attach schematised tags to semantic projects, tag metrics in their definitions, filter metrics by tag, and require tags with mandatory tags.
---

# Semantic Layer Tags { #semantic-tags }

Semantic projects carry schematised tags, attached through the API, the CLI or the UI like the tags of a feature group.
Metrics carry tags in their definitions, so a metric's tags change with its YAML and are checked when it compiles.
Both use the tag schemas an administrator defines under `Cluster settings` > `Tag schemas`, described in [Tags][tags-guide].

Schematised tags are a Hopsworks Enterprise feature.
On other editions a semantic project lists no tags, refuses to attach one, and a compile skips the check of metric tags.

The examples use two tag schemas: `ownership`, an object with `owner` and `certified` properties, and `domain`, a string.

## Tag a semantic project { #semantic-tags-projects }

=== "CLI"

    ```bash
    hops semantic tag set sales ownership '{"owner": "finance", "certified": true}'
    hops semantic tag set sales domain sales
    hops semantic tag list sales
    hops semantic tag get sales ownership
    hops semantic tag delete sales domain
    ```

=== "Python"

    ```python
    import hopsworks


    project = hopsworks.login()
    sales = project.get_semantic_layer_api().get_project("sales")
    sales.add_tag("ownership", {"owner": "finance", "certified": True})
    print(sales.get_tag("ownership"))
    print(sales.get_tags())
    sales.delete_tag("ownership")
    ```

`tag set` takes the value as JSON, or as a plain string when it does not parse as JSON.
Data owners and data scientists attach and remove tags; every member of the project reads them.
The semantic project's overview in the UI has a **Tags** card to add, edit and remove them.

Tags can also be attached when the semantic project is created, in the same request:

=== "CLI"

    ```bash
    hops semantic create sales --path Resources/semantic/sales \
      --tag 'ownership={"owner": "finance", "certified": true}' --tag domain=sales
    ```

=== "Python"

    ```python
    import hopsworks


    project = hopsworks.login()
    sl = project.get_semantic_layer_api()
    sales = sl.create_project(
        "sales",
        "Resources/semantic/sales",
        tags={"ownership": {"owner": "finance", "certified": True}, "domain": "sales"},
    )
    ```

`hops semantic init` takes the same `--tag NAME=VALUE` options.

## Tag a metric { #semantic-tags-metrics }

A metric sets its tags in `config.meta.hopsworks.tags`, a map of tag schema name to value:

```yaml
metrics:
  - name: revenue
    label: Revenue
    type: simple
    type_params:
      measure: revenue
    config:
      meta:
        hopsworks:
          tags:
            ownership: {"owner": "finance", "certified": true}
            domain: "sales"
```

The value is any YAML value, checked against its schema as JSON.
Hopsworks checks every metric's tags before it stores a build, and each problem is an error at the metric and its file:

| Rule | When |
| --- | --- |
| `METRIC_TAGS_NOT_A_MAP` | `tags` is not a map of schema name to value. |
| `METRIC_TAG_UNKNOWN_SCHEMA` | A tag names no tag schema. |
| `METRIC_TAG_INVALID_VALUE` | A value does not match its schema. |
| `METRIC_TAG_MANDATORY_MISSING` | A metric lacks a tag that a mandatory tag rule for metrics requires. |

An error makes the build `INVALID`, so the last valid build keeps answering queries until the tags are fixed.
A metric's tags change only with a new build: edit the YAML and compile.

A [saved query][semantic-saved-queries-define] sets its tags the same way, and they are checked against their schemas under `SAVED_QUERY_TAGS_NOT_A_MAP`, `SAVED_QUERY_TAG_UNKNOWN_SCHEMA` and `SAVED_QUERY_TAG_INVALID_VALUE`.
Mandatory tag rules do not apply to saved queries.

## Find metrics by tag { #semantic-tags-filter }

=== "CLI"

    ```bash
    hops semantic metrics sales --tag ownership
    hops semantic metrics sales --tag ownership --tag domain
    ```

=== "Python"

    ```python
    import hopsworks


    project = hopsworks.login()
    sales = project.get_semantic_layer_api().get_project("sales")
    for metric in sales.list_metrics(tag="ownership"):
        print(metric.name, metric.tags)
    ```

`--tag` and `tag=` keep the metrics whose definitions set every named schema.
`hops semantic metrics` lists the schemas each metric sets under `TAGS`, and `SemanticMetric.tags` holds the values.
The REST API takes the same filter, `GET /semantic-layer/v1/projects/<id>/metrics?tag=ownership`, repeated for several schemas.
In the UI, the **Metrics** card shows a **Tags** column and a filter by tag schema when any metric is tagged.

## Mandatory tags { #semantic-tags-mandatory }

An administrator makes a tag schema mandatory for **Semantic projects**, for **Metrics**, or both, among the artifact types of a mandatory tag rule, cluster-wide or for one project, as described in [Mandatory Tags][mandatory-tags-guide].
The two types are offered while the semantic layer is on.

| Rule for | Enforced |
| --- | --- |
| Semantic projects | A create without the tag is refused before anything is written, so pass it in the create: `--tag`, `tags=`, or the tag fields of the **New semantic project** dialog. Setting several tags at once is checked the same way. |
| Metrics | A metric without the tag is a `METRIC_TAG_MANDATORY_MISSING` error at compile, so the build is `INVALID` and the last valid build keeps answering queries. |

A semantic project created before its rule stays valid, and its page lists the missing tags.
A new rule for metrics is checked by the next build of each semantic project, which a change to its files or feature groups makes; the builds that answer queries keep answering them.

## Search { #semantic-tags-search }

```bash
hops search --type semantic_project sales
hops search --type metric revenue
```

Search finds semantic projects by name, with their root path, and metrics by name, label and description, with their semantic project.
Both carry their tags in the search index, so the tag filters of `hops search --tag` and of the search box in the UI header apply to them, as described in [Search][search-guide].
