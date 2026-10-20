---
description: Evaluating an agent deployment - suites of tasks graded by checks, published versions, runs and trials, the metrics a gate reads, and what counts as a failure.
---

# Evaluating An Agent

## Introduction

An evaluation asks a deployed agent a set of questions and grades what it answers.
Three things make it up.

A **task** is one question, with what you expect of it.
A **check** is how an answer is graded, and the suite owns the checks so every task in it is measured the same way.
A **suite** is the set of tasks plus those checks, published as a version so a result keeps meaning what it meant.

Running a suite produces a **run**, and one graded attempt at one task is a **trial**.

This guide assumes a deployment that speaks the chat contract, see [The Chat Contract For Conversational Agents][the-chat-contract-for-conversational-agents].

## Writing a suite

```python
import hopsworks
from hopsworks_agents.eval.sdk import check


project = hopsworks.login()
evals = project.get_agent_serving()

suite = evals.suites.create(
    "order-questions",
    checks=[check("contains", "says the order number")],
    gate_metric="pass_rate",
    gate_threshold=0.9,
)

task = evals.tasks.create("where is order 4182?")
evals.tasks.add_to_suite(task, suite, expectations={"says the order number": "4182"})

published = evals.suites.publish(suite)
```

A suite is a draft until it is published, and publishing freezes it.
Its tasks, its checks and its gate threshold stop changing, which is what lets two runs of the same version be compared.
Editing a published suite means a new version, with `evals.suites.new_version(...)`, and tasks are carried into it with `evals.suites.copy_tasks(...)`.

!!! warning "A check's settings belong in its config"
    Use the `check(...)` helper rather than writing the dictionary by hand.
    Settings given beside `type` are dropped, so a regex with its pattern in the wrong place is saved as a regex with no pattern and refused when a task joins the suite.

### The checks

| Check | Grades |
| --- | --- |
| `exact_match`, `contains`, `regex` | The answer's text against what the task expects |
| `json_schema` | That the answer parses and carries the required keys |
| `tool_call`, `tool_order`, `tool_arguments`, `no_unnecessary_tools` | Which tools ran, in what order, with what arguments |
| `no_tool_error`, `tool_retries`, `tool_latency` | How the tools behaved |
| `tool_result_used` | That the answer actually used what a tool returned |
| `llm_judge`, `tool_arguments_judge`, `pairwise` | A model's judgement against a rubric, or against a reference answer |
| `sql_state` | The state of the world after the agent acted |
| `human_review` | Nothing automatic: it defers to a person |

A check that needs something from the task, such as the answer a `contains` looks for or the rubric a judge grades against, refuses the task when it joins the suite rather than failing silently at run time.
A check missing its input does not fail, it returns ungradable, so a task graded only by those would report nothing while looking like it ran.

Checks can be saved in the project's evaluator library and reused across suites:

```python
template = evals.evaluators.save(
    "answers-in-kind",
    checks=[check("regex", "answers in kind", pattern=r"^traced: ")],
)
```

Applying a saved evaluator copies its checks into the suite, so a published suite keeps meaning what it meant even if the library entry changes later.

## Running a suite

```python
run = evals.runs.start(published, agent.id)
finished = evals.runs.wait(run, timeout_s=900)

print(finished.status)
for trial in evals.runs.trials(finished):
    print(trial.task_id, trial.status, trial.trace_id)
```

A run is recorded before it starts, so a start that fails leaves something to retry rather than nothing.
One run executes at a time per deployment: a second run asked for while one is going is queued rather than started beside it, because two runs grading the same agent at once make the history read as two overlapping answers to one question.

Each trial names the trace it produced, which is how a failure is read afterwards.
Without that, a report says a task failed and nothing more.

### Repeating a task

```python
run = evals.runs.start(published, agent.id, n_trials=2)
```

`n_trials` above 1 runs every task that many times, and the gate reads **pass^k**: a task counts as passed only when every gradable attempt passed.
An agent that answers correctly half the time is not an agent that can do the task.
`pass_at_k` is recorded beside it, so the gap between the optimistic and the strict reading is visible rather than chosen for you.

## What counts as a failure

A trial's status separates a bad answer from a broken pipeline.

| Status | Meaning | In the denominator |
| --- | --- | --- |
| `PASSED` | Every check that graded it passed | Yes |
| `FAILED` | A check graded it and it did not pass | Yes |
| `AGENT_ERROR`, `TOOL_ERROR`, `TIMEOUT`, `INVALID_OUTPUT` | The agent failed the task | Yes |
| `INFRA_ERROR`, `EVALUATOR_ERROR`, `TRACE_MISSING` | The harness failed, not the agent | No |
| `AWAITING_REVIEW` | A check deferred to a person who has not answered yet | No |

The split is the point of the table.
An agent that returns a 500 has failed that task, so it counts: leaving it out is how a deployment that crashes on everything reports a perfect pass rate over the one task it managed.
A judge that could not run, by contrast, says nothing about the agent, so counting it either way would answer a question nobody asked.

`AWAITING_REVIEW` is settled by recording the verdict:

```python
evals.runs.review_trial(trial, passed=True, note="acceptable phrasing")
```

The run's metrics are recomputed when a reviewed trial settles, so a gate that was undecided becomes decided.

## Metrics and gates

```python
metrics = {m.metric_name: m.metric_value for m in evals.runs.metrics(finished)
           if m.metric_scope == "run"}
print(metrics["pass_rate"], metrics["pass_all_k"])
```

Metrics are recorded per run, per evaluator and per task, so a report can rank what is flaky without re-deriving it.

A **gate** is the suite's own bar, frozen with the version: a metric and a threshold.
It is advisory and always answers, which matters more than it sounds: a gate that reported "never run" would be indistinguishable from a gate that failed.

```python
for row in agent.gates().gate_checks:
    print(row.suite_name, row.metric_name, row.value, row.passed, row.detail)
```

A gate reads the latest run of each published suite the deployment has.
When a run graded nothing, the gate says so in its detail rather than inventing a pass.

## Comparing runs

```python
history = evals.runs.failure_history(agent.id)
for suite in history:
    print(suite.suite_name, suite.new_failures, suite.regressions, suite.fixed, suite.persistent)
```

A trend is between runs that graded something: a run that died carries no verdicts, so comparing against it would read every failure as new and every standing failure as absent.

Cases are matched across runs by the question they ask rather than by row id, so a new version of a suite that copies its tasks keeps its history instead of reporting every carried-over case as new.

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-method"></code> [`Project.get_agent_serving`][hopsworks_common.project.Project.get_agent_serving]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>
