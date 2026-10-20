---
description: Turning feedback into fixes - a model triaging each verdict into a proposal, recurring failures grouped into clusters, promotion into a regression suite, and the calibration that says whether to trust any of it.
---

# From Feedback To A Regression Suite

## Introduction

Feedback arrives as prose about one turn.
A regression suite needs a question, an expectation and a check.
Failure analysis is the step between: a job reads the verdicts nobody has triaged yet and drafts a structured proposal for each one, so a reviewer decides rather than writes.

The reviewer decides. The model drafts.
That order is the whole design, and the calibration numbers at the end of this page are how you find out whether the drafting is worth reading.

This guide follows on from [Feedback On What An Agent Answered][feedback-on-what-an-agent-answered].

## Running the analysis

The analysis runs on its own job, one per deployment.

```python
import hopsworks


project = hopsworks.login()
evals = project.get_agent_serving()
agent = evals.get_agent("support_agent")

job = evals.jobs.ensure_review_job(agent.id)
evals.jobs.update_review_job(
    job.name,
    provider="openai",
    budget_calls=25,
)

run = evals.runs.wait(evals.jobs.analyse(job), timeout_s=900)
```

Like a monitor, the analysis continues from where it last stopped, so each verdict is triaged once.
`budget_calls` caps how many model calls one run may spend; what the budget does not reach waits for the next run rather than being skipped.

A judge is needed, and any OpenAI-compatible endpoint will do, including one you host yourself.
Point it at your own model server with `provider="custom"` and a `base_url`, which needs no credential when the endpoint wants none.

## What a proposal contains

```python
proposals = agent.triage(agent.all_feedback(verdict="negative"))

for proposal in proposals:
    print(proposal.category, proposal.failure_summary)
    print(proposal.proposed_rubric, proposal.proposed_expected_tool_behavior)
    print(proposal.correction_status, proposal.needs_human, proposal.confidence)
```

Each proposal turns one verdict into the parts a task is built from.

| Field | What it is |
| --- | --- |
| `category` | The failure kind, from the same enumeration a reviewer picks from |
| `failure_summary` | What went wrong, in one line |
| `failure_signature` | A normalised phrase used to group this with the same failure elsewhere |
| `proposed_rubric` | What a judge should grade a future answer against |
| `proposed_expected_tool_behavior` | Which tools should have been called, and how |
| `correction_status` | Whether the reviewer's correction is usable as an expectation, or too thin to be |
| `needs_human` | The model's own statement that this one should not be automated |

`correction_status` is worth reading before anything else.
A reviewer's correction is often a comment rather than an answer, and a task built from "this is wrong" tests nothing.

## Recurring failures become clusters

Forty complaints about one bug should be one item of work.
Proposals sharing a failure signature are grouped, and each cluster carries a representative trace: the one a reviewer should open.

```python
for cluster in agent.clusters():
    print(cluster.label, cluster.size, cluster.representative_trace_id)

agent.rename_cluster(cluster, "Order lookup skipped for numeric queries")
```

A cluster can be dismissed when it is not a bug, with a reason that stays on the record: `working_as_intended`, `duplicate_of`, `cannot_reproduce` or `out_of_scope`.
Dismissing is reversible, and a dismissed cluster stops competing for attention without its evidence being deleted.

## Promoting a failure into a suite

Promotion is the point of the whole path: the failure becomes a task, and the task runs on every later evaluation.

```python
task = agent.promote_cluster(cluster)
evals.tasks.add_to_suite(task, suite)
```

The question comes from the representative trace and the expectation from the reviewer's correction, so the new task asks exactly what the user asked and expects what the reviewer said should have happened.
Every member of the cluster is marked as covered by that task, which is what stops the same failure being promoted twice.

A single trace can be promoted on its own in the same way, and a multi-turn conversation keeps its turns, because a failure that only appears on the third turn cannot be reproduced by asking the third question alone.

```python
task = evals.tasks.promote(trace_id, category="wrong_tool")
```

Promoting into the deployment's standing regression suite is one call, and it handles the suite's versioning for you:

```python
evals.suites.add_to_regressions(agent.id, task)
```

A published suite cannot change, so adding to a standing suite opens a new draft version, carries the existing tasks into it, adds the new one and publishes it.

## Calibration

A model proposing categories is only useful if its proposals survive contact with a reviewer.
Every decision is recorded for exactly that reason.

```python
agent.decide_triage(proposal, "accepted")
agent.decide_triage(proposal, "edited", category="wrong_tool")
agent.decide_triage(proposal, "rejected")

print(agent.calibration())
```

`accepted`, `edited` and `rejected` are the three decisions, and the difference between what was proposed and what was decided is the calibration data.
A high acceptance rate is what justifies letting the analysis queue work automatically; a low one means the proposals are drafts for a person and nothing more.

This is also why a rejected proposal is kept rather than deleted.
An analysis whose mistakes disappear cannot be measured.

!!! warning "Analysis is not a verdict"
    A proposal never closes a trace and never marks feedback as handled on its own.
    Nothing a model produced here becomes a test case until a person promotes it.

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-method"></code> [`Project.get_agent_serving`][hopsworks_common.project.Project.get_agent_serving]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>
