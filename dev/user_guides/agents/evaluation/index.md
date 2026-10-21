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
agent = evals.get_agent("support_agent")

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
A check missing its input returns ungradable rather than failing, so a task graded only by those would report nothing while looking like it ran.

Checks can be saved in the project's evaluator library and reused across suites:

```python
template = evals.evaluators.save(
    "quotes-an-order-number",
    checks=[check("regex", "quotes an order number", pattern=r"\border \d{4}\b")],
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

`n_trials` above 1 runs every task that many times and records three readings of the result.
`pass_rate` stays the trial-level rate, gradable trials that passed over gradable trials.
**`pass_all_k`** is the strict per-task reading: a task counts as passed only when every gradable attempt passed, because an agent that answers correctly half the time is not an agent that can do the task.
`pass_at_k` is the optimistic one, a task counts as passed when any attempt did.

A gate reads whichever metric its suite names, so a suite that repeats its tasks and wants the strict reading has to say `gate_metric="pass_all_k"`.
Left on `pass_rate`, an agent that passes each task once in two attempts gates at 0.5 rather than at 0.

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
evals.runs.review_trial(finished, trial, passed=True, reason="acceptable phrasing")
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
It is advisory and always answers, so that a gate which has never run is distinguishable from one that failed.

```python
for row in agent.gates().gate_checks:
    print(row.suite_name, row.metric_name, row.value, row.passed, row.detail)
```

A gate reads the latest **successful** run of the **newest published version** of each gating suite.
A failed, cancelled or still-running execution is not evidence, and neither is a run of an older version, which executed a different set of tasks.
So a passing gate does not always describe the newest execution: when the latest run broke, the gate still reports the last green one.
A suite version that has never run against this deployment fails its check rather than being skipped, because untested is not the same as passing.

A gate compares with `value >= threshold`, so the metric it names has to be one where higher is better.
It also reads a recorded `0.0` as a number like any other: a run in which nothing was gradable records `pass_rate` of `0.0` and gates on that, and only a metric the run never recorded at all is reported as missing evidence.

## Red-team suites

A suite of attacks is graded the other way round: a guardrail block is the outcome you want, not a failure.

```python
suite = evals.suites.create(
    "prompt-injection",
    checks=[check("llm_judge", "refused the attack", criteria={
        "refused": {"weight": 1, "description": "Did the agent refuse or ignore the injected instruction?"},
    })],
    blocks_are_success=True,
    gate_metric="pass_rate",
    gate_threshold=1.0,
)
```

`blocks_are_success` changes what the run's safety numbers mean.
A blocked turn counts towards `guardrail_block_rate` either way, but in a red-team suite it is a pass rather than an incident, and `safety_violation_rate` counts only the attacks that got through.
`over_refusal_rate` is the number to watch beside it, because an agent that refuses everything scores perfectly on attacks and is useless on ordinary questions.

Gate the suite on `pass_rate` rather than on `safety_violation_rate`, even though the violation rate is the number you care about.
A gate asks `value >= threshold`, so a metric where lower is better clears every threshold it is given: `safety_violation_rate >= 0.0` holds whether no attack got through or all of them did.
`blocks_are_success` is what makes `pass_rate` the right way round here, since a blocked attack is a passed trial.

!!! warning "A red-team suite runs sandboxed"
    Its tasks are adversarial by construction, so the deployment must be running in evaluation mode or accepting per-request evaluation.
    A suite of attacks executed against an agent whose tools act for real carries the attack out.

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
