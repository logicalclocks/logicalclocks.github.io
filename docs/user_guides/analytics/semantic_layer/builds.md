---
description: How to register a semantic project, compile it into builds, read its errors, choose FOLLOW or PINNED, promote a build, and test metrics in CI.
---

# Compile and Builds { #semantic-compile-builds }

A semantic project compiles its definitions into builds, and queries are answered from its current build.
This page registers the definitions from [Define metrics][semantic-define-metrics] as the semantic project `sales`, and compiles them.

## Register a semantic project { #semantic-builds-register }

=== "CLI"

    ```bash
    hops semantic create sales --path Resources/semantic/sales
    ```

    ```text
    Created semantic project sales (id=7) on /Projects/demo/Resources/semantic/sales; its first compile runs in the background. Follow it with `hops semantic builds sales`.
    ```

=== "Python"

    ```python
    import hopsworks


    project = hopsworks.login()
    sl = project.get_semantic_layer_api()
    sales = sl.create_project("sales", "Resources/semantic/sales")
    ```

`--path` is relative to the project root; a `/hopsfs/...` path from a terminal and an absolute `/Projects/<project>/...` path work too.
`--format` sets the format, `AUTO` by default, and `--mode` the deployment mode, `FOLLOW` by default.
When the root path is inside a Hopsworks git repository, the semantic project records that repository.

In the UI, open **Semantic Layer** in the project sidebar and click **New semantic project**.
The dialog asks for the **Name**, the **Git repository** or the **Root path** of the definitions, the **Format** and the **Deployment mode**.

Registering starts the first compile in the background.

## When a compile runs { #semantic-builds-triggers }

| Trigger | When |
| --- | --- |
| Explicit | `hops semantic compile`, `SemanticProject.compile()`, or **Compile** on the semantic project's page. |
| Hopsworks git | A clone, pull, checkout, reset or file checkout through Hopsworks git, in the UI or the REST API, on the repository that holds the root path. |
| Staleness check | When a data owner or data scientist lists or queries the semantic project's metrics, Hopsworks checks, at most once every 30 seconds, whether the files or the feature groups they resolve to changed since the last build, and compiles them in the background. |
| Settings | Registering a semantic project, and changing its root path or format. |

The staleness check finds the edits that Hopsworks git does not see: files changed in Jupyter, in a terminal, in the file browser, or pulled with `git` in a terminal.
Compile explicitly to see the result of an edit at once.
The `semantic_layer_staleness_check_seconds` cluster setting changes the interval.

## Compile and read the issues { #semantic-builds-compile }

=== "CLI"

    ```bash
    hops semantic compile sales --wait
    ```

    ```text
    Build 1: VALID (0 errors, 0 warnings)
    ```

=== "Python"

    ```python
    import hopsworks


    project = hopsworks.login()
    sales = project.get_semantic_layer_api().get_project("sales")
    build = sales.compile()
    print(build.id, build.status)
    ```

Without `--wait`, the CLI starts the compile and returns.
`SemanticProject.compile()` waits for the build by default, for up to ten minutes; `compile(wait=False)` returns the build in status `COMPILING`.
The summary line ends with `at commit <sha>` when the build was read from a Hopsworks git repository.

An `INVALID` build lists its issues, one row per issue under the columns `LEVEL`, `RULE`, `LOCATION`, `ELEMENT` and `MESSAGE`.
`LOCATION` is `file:line:column`, with the file relative to the root path.
[Validation rules][semantic-validation-rules] lists every `RULE` and what it reports.
For example, `expr: amount_usd` on the `revenue` measure, a feature `orders` does not have, compiles to:

```text
Build 2: INVALID (1 errors, 0 warnings)
```

The issue is an `EXPR` error at `models/semantic.yml:24:9`, the line of the measure, on the element `semantic_model:orders.measure:revenue`, with a message that starts with `invalid expression 'amount_usd'`.

In Python, a compile that ends `INVALID` or `FAILED` raises `SemanticBuildException`, whose `issues` carry the same fields:

```python
import hopsworks
from hopsworks.client.exceptions import SemanticBuildException


project = hopsworks.login()
sales = project.get_semantic_layer_api().get_project("sales")
try:
    sales.compile()
except SemanticBuildException as err:
    for issue in err.issues:
        print(issue.level, issue.rule, issue.file, issue.line, issue.element)
        print(issue.message)
```

A `WARNING` does not make a build invalid.
A metric of a shape the planner refuses, listed under [Limits][semantic-metric-types-limits], is an `UNSUPPORTED` warning: the build serves the other metrics, and queries of that one are refused.
A `FAILED` compile could not run, for example because the definition files could not be read or the semantic gateway did not answer.
Its build has one `COMPILE_FAILED` error whose message says what stopped it.
When the compile stopped without recording why, for example because its Hopsworks instance restarted, the message says so.
Read that issue, with `hops semantic build` or **View issues**, before compiling again, which retries the build.

## Builds and the current build { #semantic-builds-list }

```bash
hops semantic builds sales      # newest first; * marks the build that answers queries
hops semantic build sales 2     # one build with its issues
hops semantic show sales        # settings, current and latest build, and whether queries are stale
```

The **Builds** card on the semantic project's page lists the same builds, marks the current one **Serving**, and opens a build's issues with **View issues**.

An `INVALID` build never becomes current, so a broken edit does not break queries: they keep the last valid build.
While the newest build is `INVALID`, `FAILED` or still compiling, the answers are stale:

- `hops semantic show` reports `build <id> (stale: the newest compile is invalid or running)`;
- the Python client logs `Semantic project 'sales' answered from build 1, which is older than its newest compile: that compile is invalid or still running.`;
- the UI shows **Not the newest definitions** over the metrics and the query results.

The gateway keeps each caller's view of a semantic project for up to a minute, so a newly current build can take that long to answer queries.

## FOLLOW, PINNED and promote { #semantic-builds-modes }

In `FOLLOW` mode, each new valid build becomes current.
In `PINNED` mode, the current build changes only on a promote.

```bash
hops semantic update sales --mode PINNED
hops semantic compile sales --wait
hops semantic promote sales 3
```

```text
Build 3 now answers queries on sales.
```

```python
import hopsworks


project = hopsworks.login()
sales = project.get_semantic_layer_api().get_project("sales")
sales.update(deployment_mode="PINNED")
sales.promote(3)
```

Only a `VALID` build can be promoted.
A promote also works in `FOLLOW` mode, to roll back to an older valid build until the next valid compile.
On the **Builds** card, **Promote** does the same.

## Test metrics in CI { #semantic-builds-ci }

```bash
hops semantic compile sales --fail-on-error
hops semantic test sales
```

`compile --fail-on-error` waits for the build and exits 1 when it is `INVALID` or `FAILED`.
`test` compiles, then runs every metric once on Trino, limited to one row, and exits 1 when any metric fails.
Each metric runs ungrouped, or grouped by `metric_time` when its queries [must be][semantic-metric-types-requirements]:

```text
Build 1: VALID (0 errors, 0 warnings)
METRIC                       STATUS  DETAIL
---------------------------  ------  ------
revenue                      PASS
orders                       PASS
revenue_per_order            PASS
completed_revenue_per_order  PASS
cancelled_orders             PASS
5 of 5 metrics ran
```

Running each metric catches what only the query engine sees, such as a feature group the caller cannot read.
Each metric reads its whole feature groups once, so pass `--metrics` to test a subset on large data.

`test` runs the metrics on the build it just compiled, so it exits 1 when that build does not answer queries: in `PINNED` mode before the build is promoted.
`test --no-compile` tests the current build instead.

## Change or delete a semantic project { #semantic-builds-update }

```bash
hops semantic update sales --path Resources/semantic/sales_v2
hops semantic delete sales
```

A new root path or format compiles again in the background.
`delete` asks for confirmation unless given `--yes`, deletes the builds and leaves the YAML files in place.

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-method"></code> [`Project.get_semantic_layer_api`][hopsworks_common.project.Project.get_semantic_layer_api]
    - <code class="doc-symbol doc-symbol-class"></code> [`SemanticLayerApi`][hopsworks_common.core.semantic_layer_api.SemanticLayerApi]
        - <code class="doc-symbol doc-symbol-method"></code> [`create_project`][hopsworks_common.core.semantic_layer_api.SemanticLayerApi.create_project]
        - <code class="doc-symbol doc-symbol-method"></code> [`get_project`][hopsworks_common.core.semantic_layer_api.SemanticLayerApi.get_project]
    - <code class="doc-symbol doc-symbol-class"></code> [`SemanticProject`][hopsworks_common.semantic_layer.SemanticProject]
        - <code class="doc-symbol doc-symbol-method"></code> [`compile`][hopsworks_common.semantic_layer.SemanticProject.compile]
        - <code class="doc-symbol doc-symbol-method"></code> [`get_builds`][hopsworks_common.semantic_layer.SemanticProject.get_builds]
        - <code class="doc-symbol doc-symbol-method"></code> [`get_build`][hopsworks_common.semantic_layer.SemanticProject.get_build]
        - <code class="doc-symbol doc-symbol-method"></code> [`promote`][hopsworks_common.semantic_layer.SemanticProject.promote]
        - <code class="doc-symbol doc-symbol-method"></code> [`update`][hopsworks_common.semantic_layer.SemanticProject.update]
    - <code class="doc-symbol doc-symbol-class"></code> [`SemanticBuild`][hopsworks_common.semantic_layer.SemanticBuild]
    - <code class="doc-symbol doc-symbol-class"></code> [`SemanticIssue`][hopsworks_common.semantic_layer.SemanticIssue]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>
