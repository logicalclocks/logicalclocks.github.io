---
description: How to scaffold a semantic project from feature groups with hops semantic init, in a HopsFS folder or a new private GitHub repository.
---

# Get Started with hops semantic init { #semantic-init }

`hops semantic init` writes a dbt project with one semantic model per feature group, registers it as a semantic project, and compiles it.
Run it where the `hops` CLI is connected to the project, such as the [project terminal][terminal].

## Scaffold from feature groups { #semantic-init-from-fg }

```bash
hops semantic init sales --from-fg orders --from-fg customers
```

```text
Created semantic project sales on /Projects/demo/Resources/semantic/sales.
```

The build of the first compile follows, as [`hops semantic compile --wait`][semantic-builds-compile] prints it, then the next step:

```text
Uncomment the metrics to serve in models/semantic.yml, then run `hops semantic compile sales --wait`.
```

`--from-fg` takes a feature group at its latest version, or `<name>:<version>`, and repeats.
The files go to `Resources/semantic/<name>`, or to `--path`, which must not exist yet:

```text
Resources/semantic/sales/
├── dbt_project.yml
└── models/
    └── semantic.yml
```

For the `orders` and `customers` feature groups of [Define metrics][semantic-define-metrics], `models/semantic.yml` is:

```yaml
version: 2

semantic_models:

  - name: orders
    model: ref('orders')
    config:
      meta:
        hopsworks:
          feature_group: orders
          version: 1
    defaults:
      agg_time_dimension: order_ts
    entities:
      - name: order
        type: primary
        expr: order_id
      - name: customer
        type: foreign
        expr: customer_id
    dimensions:
      - name: order_ts
        type: time
        expr: order_ts
        type_params:
          time_granularity: day
      - name: status
        type: categorical
        expr: status
    measures:
      - name: orders_count
        agg: count
        expr: order_id
        description: "Rows of feature group orders."
      - name: amount
        agg: sum
        expr: amount

  - name: customers
    model: ref('customers')
    config:
      meta:
        hopsworks:
          feature_group: customers
          version: 1
    entities:
      - name: customer
        type: primary
        expr: customer_id
    dimensions:
      - name: country
        type: categorical
        expr: country
    # No measures: the feature group has no event time, and every measure needs a time dimension.

# One simple metric per measure. Uncomment the ones to serve, with the `metrics:` line, give them
# labels and descriptions, then run `hops semantic compile sales --wait`.
# A metric carries schematised tags in config.meta.hopsworks.tags, tag schema name to value.
# metrics:
#   - name: orders_count
#     label: Orders count
#     type: simple
#     type_params:
#       measure: orders_count
#   - name: amount
#     label: Amount
#     type: simple
#     type_params:
#       measure: amount
```

Each feature group becomes a semantic model:

- its version is pinned in `config.meta.hopsworks`, so a new feature group version changes no metric until the YAML does;
- a single-column primary key is the primary entity, and a feature with the name of another scaffolded feature group's single-column primary key is a foreign entity, which joins the two;
- a `timestamp` or `date` event time is the time dimension, at day grain;
- string features are categorical dimensions;
- the measures are a row count, and a sum per numeric feature that is not a key.

A feature group without a timestamp or date event time gets no measures, since every measure needs a time dimension; it still serves dimensions to the other models.
The metrics are written commented out, one per measure: uncomment the ones to serve, add labels, descriptions, ratios and derived metrics, and compile.
Edit the files in the [project terminal][terminal] under `/hopsfs/Resources/semantic/sales`, in Jupyter, or in the file browser.

A new scaffold without `--from-fg` writes an empty `models/semantic.yml` and does not wait for a compile, since a project with no semantic model does not compile: the compile that registration starts in the background ends `INVALID` until you add one.
With `--repo <url>`, `init` registers the repository's definitions as they are and waits for their compile.

| Option | Meaning |
| --- | --- |
| `--from-fg <fg>[:<version>]` | A feature group to scaffold a semantic model for; repeatable. |
| `--path` | The HopsFS folder to write the scaffold to, `Resources/semantic/<name>` by default. |
| `--repo new` or `--repo <url>` | Keep the definitions in a git repository, see below. |
| `--format` | `DBT` by default for a scaffold, `AUTO` for an existing repository. |
| `--mode` | `FOLLOW` (default) or `PINNED`. |
| `--tag NAME=VALUE` | A tag to attach to the semantic project, the value JSON or a plain string; repeatable. |
| `--yes` | With `--repo new`, skip the two confirmations. |

When `init` waits for the first build, with `--from-fg` or `--repo <url>`, it exits 1 if that build is not `VALID`. A new scaffold without `--from-fg` does not wait, so its exit status says nothing about the build.

## Scaffold into a new GitHub repository { #semantic-init-repo-new }

```bash
hops semantic init sales --from-fg orders --from-fg customers --repo new
```

With `--repo new`, `init`:

1. checks that the GitHub CLI is logged in, with `gh auth status`;
2. creates the private repository `hops-semantic-<name>` under your GitHub account, or `hops-semantic-<name>-2` and so on when the name is taken;
3. commits the scaffold and pushes it;
4. registers your GitHub CLI token, `gh auth token`, as your GitHub git provider in Hopsworks, when you have none, since Hopsworks clones a private repository with that token;
5. clones the repository through Hopsworks git into `Resources/semantic/<repository>`;
6. registers the semantic project on the clone, and compiles it.

`init` asks before it creates the repository and before it registers the token, unless given `--yes`.
In a Hopsworks terminal, `github-login` logs the GitHub CLI in.

The clone is a Hopsworks git repository, so a pull through Hopsworks git compiles the semantic project, and each build records its commit.
Push changes to GitHub, then pull them through Hopsworks git, in the UI or with the API.
[How To Clone a Git Repository][how-to-clone-a-git-repository] and [How To Configure a Git Provider][how-to-configure-a-git-provider] cover Hopsworks git.

In the UI, **New semantic project** offers **A new GitHub repository** when the terminal is enabled and its GitHub CLI is logged in.
It runs `hops semantic init <name> --repo new --yes` in a terminal tab, and the semantic project appears in the list once `init` registers it.

## Register an existing repository { #semantic-init-repo-url }

```bash
hops semantic init sales --repo https://github.com/acme/metrics.git
```

`init` clones the repository through Hopsworks git into `Resources/semantic/`, registers the clone as the semantic project, and compiles it.
The repository is registered as it is, so `--from-fg` and `--path` are refused.
A private repository needs a git provider for its host in your Hopsworks account.
