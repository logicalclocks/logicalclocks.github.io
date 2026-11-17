# How To Read the Cost of a Project

## Introduction { #project-costs-introduction }

In this guide, you will learn how a project's data owners read the Kubernetes cost of their project from Python, the `hops` CLI or the REST API.
Each project runs in its own Kubernetes namespace, and the cost of that namespace is computed by OpenCost.
Cost tracking must be enabled on the cluster by an administrator, see [Costs][costs-introduction].

## Prerequisites { #project-costs-prerequisites }

- You are a data owner of the project.
  Data scientists, observers and members of other projects get HTTP 403.
- An API key needs the `PROJECT` scope.
- With cost tracking off the API answers HTTP 404 with error code 100083.
- When OpenCost is not reachable the API answers HTTP 503 with error code 100081 and a general message; a cluster administrator sees the cause on the _Costs_ page.

## Step 1: Read the cost from Python { #project-costs-python }

```python
import hopsworks


project = hopsworks.login()
costs = hopsworks.get_costs_api().get_project_costs("month")
print(costs.total_cost, costs.currency)

for bucket in costs.buckets:
    if not bucket.observed:
        print(bucket.start, "no data")
        continue
    print(bucket.start, sum(row.total_cost for row in bucket.items))

other = hopsworks.get_costs_api().get_project_costs("week", project="fraud_detection")
```

The window is one of `hour`, `day`, `week` (the default), `month` or `year`, and `project` defaults to the project logged in to.
The response has the shape of the administrators' namespace view with the project's own row alone: no other project, no idle capacity or unmounted volumes, and no share.
Its totals are the project's, and the coverage is the cluster's, so a bucket with data and no row is one in which the project cost nothing, while a bucket without data is unknown cost.

## Step 2: Read the cost from the CLI { #project-costs-cli }

```bash
hops project costs --window month
hops project costs --window week --project fraud_detection --json
```

The command prints the table for the active project, or for the one named with `--project`, then a coverage line when some buckets have no data, and the totals.

## Step 3: Read the cost from the REST API { #project-costs-rest }

```text
GET /hopsworks-api/api/project/<project id>/costs?window=<HOUR|DAY|WEEK|MONTH|YEAR>
```

A project that runs in a pre-created namespace shared with other projects answers HTTP 409 with error code 100084, because OpenCost cannot split that namespace's cost between the projects.
A project created with the name of a deleted project gets its namespace, and with it the deleted project's cost history.

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-function"></code> [`hopsworks.get_costs_api`][hopsworks.get_costs_api]
    - <code class="doc-symbol doc-symbol-class"></code> [`CostsApi`][hopsworks_common.core.costs_api.CostsApi]
        - <code class="doc-symbol doc-symbol-method"></code> [`get_project_costs`][hopsworks_common.core.costs_api.CostsApi.get_project_costs]
    - <code class="doc-symbol doc-symbol-class"></code> [`NamespaceCosts`][hopsworks_common.cost.NamespaceCosts]
    - <code class="doc-symbol doc-symbol-class"></code> [`CostRow`][hopsworks_common.cost.CostRow]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>
