# Feedback On What An Agent Answered

## Introduction

A trace says what an agent did.
Feedback says whether it was any good, and that judgement has to come from a person.

Hopsworks records two kinds of verdict against a turn.
A **reviewer** is a project member looking at traces in the UI or through the API, and their verdict is an assessment.
An **end user** is whoever was talking to the agent, and their verdict is a report from the person the answer was for.

Both are filed against the turn's `trace_id`, which is what lets a verdict become a test case later.
Feedback is the input to [failure analysis and to regression suites][what-feedback-is-for], so the fields below are not a form for its own sake.

## Giving a verdict as a reviewer

```python
import hopsworks


project = hopsworks.login()
agents = project.get_agent_serving()
agent = agents.get_agent("support_agent")

reply = agent.chat("where is order 4182?")

agent.give_feedback(
    reply.trace_id,
    "negative",
    issue_category="wrong_answer",
    corrected_answer="It shipped on Tuesday and arrives Thursday.",
    note="Answered from nothing, the order lookup was never called.",
)
```

A verdict is `positive`, `negative` or `false_alarm`.

`false_alarm` is its own verdict rather than a flavour of either.
It means something flagged this turn and the flag was wrong, which is the signal that calibrates detectors and judges: a turn a machine called bad and a person called fine.
It is not an endorsement, so it does not count as positive, and it is not a complaint, so a review queue shows it as what it is.

!!! warning "A verdict is replaced whole, not patched"
    Giving a verdict again replaces your previous one, so a field left out is cleared rather than kept.
    Re-saving a correction without the note that came with it drops the note.

One verdict exists per reviewer per trace.
Two reviewers disagreeing keep two rows, because disagreement is signal, and each can only change their own.

### The fields, and what each one is for

| Field | What it is for |
| --- | --- |
| `issue_category` | What kind of failure it was: `wrong_answer`, `missing_info`, `wrong_tool`, `refused`, `unsafe`, `other` |
| `corrected_answer` | What the agent should have said, which is what a regression task is built from |
| `expected_tool_behavior` | Which tools it should have called, and how |
| `note` | Free text for a person reading the queue |

Those are the values the Feedback tab offers.
The API takes any string up to 64 characters, so a verdict sent from Python with a category of its own is stored as written and groups as its own category.

## Taking a verdict back

```python
agent.retract_feedback(reply.trace_id)
```

A reviewer retracts their own verdict.
An end user's can be retracted on their behalf by naming them, which is what a "delete my feedback" request in your own application calls.

```python
agent.retract_feedback(reply.trace_id, reviewer="user:alice")
```

Naming another project member's account is refused: their verdict is theirs alone.

## Letting an end user give a verdict

A chat UI built on the agent's endpoint has the gateway, the serving credential and the `trace_id` on every reply, and nothing else.
It has no Hopsworks address, and its users need no Hopsworks account.
So the agent relays the verdict itself, on the route its manifest advertises as `endpoints.feedback`.

```http
POST /v1/feedback
{
  "trace_id": "<the trace_id of the reply>",
  "verdict": "negative",
  "issue_category": "wrong_tool",
  "corrected_answer": "It should have looked the order up first.",
  "note": "Told me to check my email, which has nothing in it.",
  "subject": "alice"
}
```

A client that kept no trace id can send `conversation_id` instead, and the latest turn of that conversation is rated.

`subject` is who is speaking, asserted by the client the same way a chat request asserts it.
The row lands under the reviewer `user:<subject>`, or `user:anonymous` without one.
That naming is what keeps the two kinds apart: an end user's verdict never collides with a project member's account, it shows as **user** in the Feedback tab, and it reaches failure analysis as a signal to triage rather than as a verdict that closes the trace.

!!! note "A verdict can arrive before its own trace"
    A verdict given the moment a reply lands can beat the trace into the store, because the turn's span closes after the reply and the collector batches before writing.
    The relay retries for about seven and a half seconds and then refuses, so an ordinary fast thumbs down is recorded, but a trace held up by a busy collector or a slow write is not.
    Keep a refused submission and retry it rather than treating it as recorded.

The relay runs on the deployment's own credential, the same way an agent reaches the feature store.
Outside a deployment the route answers `503`, because there is nothing to relay to.

## Reading the feedback

```python
# everything that needs attention, newest first
for row in agent.all_feedback(verdict="negative"):
    print(row.reviewer, row.verdict, row.issue_category, row.corrected_answer)

# one trace
agent.trace_feedback(reply.trace_id)

# one person's verdicts
agent.all_feedback(reviewer="user:alice")
```

`verdict="negative"` means everything that is not an endorsement, so it includes false alarms.
That is deliberate: it is the queue a review process works through, and a false alarm is often a mislabelled complaint worth reading.
Each row still reads back as the verdict it was given, so a false alarm is never counted as a complaint.

In the UI, the deployment's **Feedback** tab is the same list, filtered by verdict and by reviewer, with the correction and the category beside each row.

## What feedback is for

Three things read it.

**Failure analysis** triages each verdict into a structured proposal: a category, a failure summary, and a rubric or expected tool behaviour drafted from the correction.
Recurring failures are grouped under one signature so a pattern is one item rather than forty.

**Regression suites** are built from the corrections.
A negative verdict with a corrected answer is exactly a test case: the question the agent was asked, and what it should have said.
Promoting one adds it to the deployment's standing suite, so the failure is checked on every later run.

**Calibration** compares what a model proposed with what a reviewer decided, which is how you find out whether the triage is worth trusting before you let it queue work.

!!! api "API reference"

    - <code class="doc-symbol doc-symbol-method"></code> [`Project.get_agent_serving`][hopsworks_common.project.Project.get_agent_serving]

    <a class="hops-api-cta" href="../../../../python-api/hopsworks/">Browse the full Python API :material-arrow-right:</a>
