# Monitoring Live Traffic

## Introduction

An evaluation suite asks an agent questions you wrote.
A monitor grades the questions real users asked.

Production brings its own distribution, and the failures that cost most are usually the ones nobody thought to write a task for.
A monitor reads the traces a deployment recorded, grades a sample of them, and records the result as a run beside the suite runs.

Because production traffic carries no expected answer, a monitor can only use checks that judge an answer on its own terms.
A `contains` check needs to know what the answer should have contained, and a live conversation has nothing to tell it, so those are refused when a monitor is configured rather than silently returning nothing.

This guide follows on from [Evaluating An Agent][evaluating-an-agent].

## Grading a window by hand

```python
import hopsworks
from hopsworks_agents.eval.sdk import check


project = hopsworks.login()
evals = project.get_agent_serving()
agent = evals.get_agent("support_agent")

answered_the_question = evals.evaluators.save(
    "answered-the-question",
    checks=[
        check(
            "llm_judge",
            "answered the question",
            criteria={
                "answered": {
                    "weight": 1,
                    "description": "Does the reply answer what was asked?",
                },
            },
        )
    ],
)

run = evals.runs.sample(agent.id, evaluator=answered_the_question)
finished = evals.runs.wait(run, timeout_s=900)
```

Without a window, a monitor grades what arrived since the last successful sample.
Pass `since` and `until` to grade a specific period instead, as datetimes or epoch milliseconds, which is what you want when investigating a complaint about a particular afternoon.

A suite's checks can be used instead of a saved evaluator, with `evals.runs.sample(agent.id, suite=published)`.
The suite contributes only its checks; its tasks are not used, because a monitor's questions come from the traffic.

## The watermark

Each monitor continues from where it stopped.
A run records the window it covered, and the next run of that monitor starts at the end of the last successful one, which is what makes a schedule grade each turn once instead of re-grading the same day every night.

```python
print(evals.runs.sample_watermark(agent.id))  # where the next sample would start
```

Three properties follow from it being per monitor rather than per deployment.

A failed run does not advance it, so the traces it never reached are graded by the next run rather than skipped.
Another evaluator's runs do not advance it either: two monitors of the same job each cover their own ground, and the one that is behind catches up.
The first run of a new monitor has nothing to continue from, so it starts where the job's schedule was set to begin, or takes a bounded look back when the job was started by hand.

## Sampling

Every graded conversation costs a judge call per evaluator, so a monitor grades a sample rather than everything.

| Setting | Default | What it does |
| --- | --- | --- |
| `sample_ceiling` | 500, maximum 10000 | How many conversations one sample may grade |
| `sample_strategy` | `random` | `random` grades a spread of the window, `oldest` grades the oldest and leaves the rest |
| `shared_sample` | On | Whether every evaluator in one execution grades the same conversations |

`random` is the default for a reason.
`oldest` never skips anything, but on an agent whose traffic outpaces the ceiling it measures an older and older slice of the day while the backlog grows, and the number people read a monitor for is what is happening now.

`shared_sample` off gives each evaluator its own draw: every rate stays a fair sample of the window, but no two of them are about the same conversations, so two judges can no longer be compared on one.

!!! warning "A sample is not a census"
    A monitor's pass rate describes the conversations it graded, not the window.
    The run records `window_conversations` and `sampled_fraction` next to the rate so a reader can tell a rate over the whole window from a rate over two percent of it.

## Running it on a schedule

A monitor that matters runs unattended on the deployment's evaluation job.

```python
job = evals.jobs.ensure_eval_job(agent.id)

evals.jobs.update_eval_job(
    job.name,
    evaluators=[answered_the_question],
    monitor=True,
    sample_ceiling=200,
    sample_strategy="random",
    shared_sample=True,
)
```

Give the job a schedule the way any Hopsworks job gets one, and each fire grades the traffic since the last one.

A scheduled fire runs the monitors only.
Set `suites_on_schedule=True` to have it run the deployment's suites as well, which is off by default because a schedule is about the traffic that changed since the last fire, while a suite asks the same questions every time.
Running the job by hand always runs everything it names.

The settings read back off the job, so a form or a script sees what is actually configured:

```python
stored = evals.jobs.eval_job(agent.id)
print(stored.monitor, stored.sample_ceiling, stored.sample_strategy, stored.evaluators)
```

## Evaluation traffic is not production traffic

An evaluation trial is a turn the agent served, so without care a monitor would grade the suites' own questions and report on itself.
Monitors exclude traffic that an evaluation produced, which is why a run started by a suite never appears in a sample.

The same exclusion is why a monitor's numbers stay comparable across a release: a day with a lot of evaluation activity does not change what the monitor says about real users.

## Reading the result

A monitoring run is a run like any other, so the trials, the metrics and the trace of each graded conversation are read the same way.

```python
for trial in evals.runs.trials(finished):
    print(trial.status, trial.trace_id)

metrics = {m.metric_name: m.metric_value for m in evals.runs.metrics(finished)
           if m.metric_scope == "run"}
print(metrics.get("pass_rate"), metrics.get("window_conversations"))
```

Because each trial names the trace it graded, a failing rate is a list of conversations to open rather than a number to worry about.

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-method"></code> [`Project.get_agent_serving`][hopsworks_common.project.Project.get_agent_serving]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>
