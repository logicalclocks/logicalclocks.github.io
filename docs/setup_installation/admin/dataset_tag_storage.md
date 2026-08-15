# Dataset Tag Storage

## Introduction

Tags attached to a dataset used to be stored as HopsFS extended attributes.
They are now rows in the Hopsworks database.
The move makes dataset tags searchable, countable when an administrator asks what still references a tag schema, and deleted in the same transaction as the dataset they belong to.

Nothing about this is visible to a project member: the same tags are read and written through the same API either way.
It is visible to an administrator, because moving the store on a running cluster is a one-way step that has to be taken deliberately, and because tags attached to individual files inside a dataset do not move.

This page covers what an upgrade does on its own, what the cut-over is, and how to run it.

## What the upgrade does on its own

The upgrade that introduces this feature applies a database migration that audits the tag tables for duplicates and then adds unique keys over them.
A tag or keyword write landing between the audit and the index creation can be the row that makes the index creation fail, so the chart stops those writes for the length of the migration.

A pre-upgrade hook scales both Payara deployments to zero, waits until their pods are gone, runs the migration, and leaves the deployments at zero for the upgrade's own apply to bring back on the new image.
The hook fires on the one upgrade that applies the migration and on no other.
It is measured at 70 seconds against a database holding a million tag values.

Two failure paths are deliberately different.
A refusal by the pre-migration audit happens before any schema change, so the original replica counts are restored and the upgrade aborts with the cluster running as it was.
A failure after the schema change has begun leaves the cluster scaled to zero, because starting the old nodes over a half-applied schema is worse than an outage.

Set `hopsworks.tagLifecycle.writeWindow.enabled=false` only if you are taking the write window yourself. Routing traffic away at a load balancer is not enough, because internal clients still reach the API pods directly.
The chart holds you to it: with the write window disabled, a pre-upgrade check refuses the one upgrade that applies the migration while any API pod is running or a HorizontalPodAutoscaler targets the API deployments.

After the upgrade the cluster keeps reading dataset tags from the extended attributes and writes them to both stores.
Nothing is lost while you stay in that state, and you can stay in it indefinitely.

## Per-file tags are frozen

Tags could previously be attached to any file or directory inside a dataset.
Attaching a new tag to a path inside a dataset is now rejected with HTTP 400 and error code 370013.
Per-file tags were stored outside the database, could not be searched or counted, and would have made the cut-over unbounded.

Tags that were already attached to such paths remain readable and deletable, and the file browser keeps showing them.
They are not migrated, and they are the reason the tag schema usage report states that its counts cover database-backed references only.

## The activation gate

Two operations are only safe once every node in the cluster runs the new code: replacing a cluster-wide mandatory tag policy, and the dataset tag cut-over.
Both are refused with HTTP 503 and `ACTIVATION_PENDING` while a rolling upgrade is in progress.

The chart's post-upgrade hook verifies against the Kubernetes API that every pod serving the Hopsworks API belongs to the new rollout, then activates the lifecycle.
Activation is what the refusal waits for; no timer and no node decides it for itself.
A fresh install is activated by the post-install hook instead, since there is no old node to wait for.

Check the state at any time:

```bash
curl -s -H "Authorization: ApiKey $API_KEY" \
  https://<cluster>/hopsworks-api/api/admin/tag-lifecycle
```

## Fencing a rollback

Once the database is the canonical store for dataset tags, a node running the previous release writes extended attributes that nothing reads any more, and those writes are lost silently.
Rolling back is therefore refused rather than made safe.

`hopsworks.tagLifecycle.admissionPolicy.enabled=true` installs a `ValidatingAdmissionPolicy` that refuses to admit an API pod below the current capability epoch.
It is **off by default**, because turning it on means an emergency downgrade requires restoring the pre-cut-over database and deleting the policy, in that order.
A cluster that never cuts over never needs it.

The cut-over refuses to run while the policy is absent, and the operator who accepts the risk says so explicitly with `hopsworks.tagLifecycle.cutover.acceptUnfencedRollback=true`, which is rendered into the Job and logged with the decision.

A fresh installation is database-canonical from the start, so it sits past the same boundary without ever running a cut-over.
**Downgrading any database-canonical cluster below this release without restoring (or reinstalling) its database is unsupported**, and a fresh installation is such a cluster from day one.
Doing it anyway has the same consequence a post-cut-over rollback has: dataset tags written to the database become invisible to the old code, and tags written to extended attributes during the downgrade are silently ignored when you upgrade again.
Enable the admission policy on a fresh installation if pods from an older release must be refused rather than merely unsupported; the installation records `rollbackFenced=false` in its activation audit when you do not.

## The cut-over

The cut-over moves the canonical store from the extended attributes to the database.
Schedule it as a maintenance action: dataset tag **writes** are refused with a retryable HTTP 503 from the start of the window until it commits.
The quiesce itself is a short full outage: both API deployments are scaled to zero for the restart, and nothing answers while they are down.
Once the pods are back, reads of dataset tags and everything else serve normally for the rest of the window, and no stored data is touched at any point.

The window is about five minutes on a three-node cluster, dominated by the API restart.
The verification over several hundred datasets takes seconds.

If a HorizontalPodAutoscaler targets either API deployment, the Job refuses to start: an autoscaler scales the deployment back up while the cut-over needs it at zero, and a pod it starts can write extended attributes after the flip.
Delete or suspend it for the window, and pause any GitOps reconciliation that owns the replica counts, for the same reason.

Run it by setting `hopsworks.tagLifecycle.cutover.run=true` on a `helm upgrade`.
The value is off by default and the Job runs once per upgrade that sets it.
These settings belong to the `hopsworks` subchart, so the `hopsworks.` prefix is part of the key: the umbrella chart's schema rejects a bare `tagLifecycle` with `additional properties 'tagLifecycle' not allowed`.

!!! note "Helm 4 needs `--force-conflicts`"
    Under Helm 4, pass `--force-conflicts` to the upgrade.
    Server-side apply refuses fields owned by other field managers, which a running cluster always has, and without the flag the upgrade fails before any hook runs.
    This is a pre-existing Helm 4 behaviour, not specific to the cut-over.

The Job:

1. Recovers first: if a previous attempt was killed after scaling the deployments down, the replica counts it recorded in a ConfigMap are restored before anything waits on the API.
   Both deployments at zero with no record is a zero somebody else owns, and the Job refuses with the manual commands printed.
2. Reads the cut-over status while the cluster is up.
   A database that is already canonical exits immediately, so the Job is safe to leave enabled across upgrades, and a window an earlier attempt left open is resumed at the final sweep rather than opened twice.
3. Reads the admission policy and its binding from the Kubernetes API and checks the whole contract: that it denies rather than warns, that it fails closed, that it matches pod creation in this namespace for both API deployments, and that its expression is exactly the one this chart installs for the current epoch.
   A policy with the right name but any of those wrong is not a fence.
4. Refuses to start unless the rolling upgrade has been activated, the background migration of existing tags reports done, no tag was quarantined for failing validation, and no HorizontalPodAutoscaler targets the API deployments.

    A quarantined tag is one whose value could not be migrated: its schema is gone, it no longer
    validates, or it is longer than the store accepts. The value is left where it is and recorded with
    a digest, a length and a reason, so nothing is destroyed by a failed migration. Resolve each one by
    correcting the value or the schema, or waive it to accept losing that value:

    ```bash
    curl -X PUT "https://<cluster>/hopsworks-api/api/admin/dataset-tags/quarantine/<id>/waive?expectedDigest=<digest>" \
      -H "Authorization: ApiKey <key>"
    ```

    The digest is required and comes from reading the record first. A waiver applies to the value that
    was inspected and to no other: if the value changes before the waiver is granted the request is
    refused with `409`, and if it changes afterwards the waiver is dropped and the record comes back for
    review. That is deliberate, because a waiver authorises destroying one specific value.
5. Records the current replica counts in a ConfigMap, scales both API deployments to zero, and waits until their pods are gone.
   At that instant every write that was in flight has either reached the file system or never will, so nothing is left to drain.
6. Sets the state to `cutting_over` in a single transaction while nothing is running, then restores the replica counts.
   The API comes back refusing dataset tag writes with `CUTOVER_IN_PROGRESS`.
7. Runs a final migration pass and then a verification, and stops if the verification reports any difference between the two stores.
8. Checks the fence again and commits.
   Every precondition is checked once more inside the transaction that publishes the new state, including that no migration pass finished after the verification started.

If the Job stops at step 7 or 8, the cluster stays in `cutting_over` with reads unaffected.
Investigate the reported differences, then either fix them and re-run the Job (it resumes the open window), or abort:

```bash
curl -s -X POST -H "Authorization: ApiKey $API_KEY" \
  https://<cluster>/hopsworks-api/api/admin/dataset-tags/cutover/abort
```

Aborting returns the cluster to the extended attributes and resumes writes.
It is never blocked on anything: getting out of a paused state must not itself require the state to be healthy.

Ask what the cluster thinks at any point:

```bash
curl -s -H "Authorization: ApiKey $API_KEY" \
  https://<cluster>/hopsworks-api/api/admin/dataset-tags/cutover
```

The response reports the current state, when the window opened, and what would block a commit right now.

!!! warning "Do not edit the state directly"
    Setting the canonical store through the cluster variables endpoint is refused in both directions, and the error names the cut-over endpoints.
    A direct database edit bypasses every check here, as it always has.

## After the cut-over

The extended attributes are left in place after the cut-over.
Readers holding a cached copy of the cluster state would otherwise read a store that had already been emptied, so the extended attributes are removed no earlier than one full settings-cache interval afterwards, which is ten minutes, and only after the verification has passed.

Removing them is the point of no return for a downgrade, so keep them until the release is known good.

### Removing the extended attributes

When you are ready, start a cleanup pass:

```bash
curl -X POST -u <admin> \
  https://<cluster>/hopsworks-api/api/admin/dataset-tags/clean
```

It answers with a run id. Poll it:

```bash
curl -u <admin> \
  https://<cluster>/hopsworks-api/api/admin/dataset-tags/clean/<runId>
```

A dataset is cleaned only when all four of these hold, and the run reports which one refused for each dataset it skips:

| Gate | Meaning |
| --- | --- |
| No unwaived quarantine record | Nothing in the attribute failed to migrate. Waive a record only after reading it (see below) |
| The snapshot is from the accepted verification | This dataset was covered by the verification the commit accepted |
| The attribute still matches that snapshot | Nothing has written the attribute since it was verified |
| The index has caught up | The search document reflects the projection, so nothing is lost by deleting the attribute |

A skipped dataset is not a failure, and the pass is safe to re-run: gates two and four clear on their own once a queued search-index rewrite drains, and quarantine records are cleared by waiving them.

### Recovering a cleanup run whose pod is gone

A cleanup pass deletes from HopsFS, which no database transaction can fence, so a run whose worker stopped responding is never taken over automatically.
Its claim is held until you confirm that worker is gone, and the run reports which pod holds it.

Read the run, take the `worker` field, confirm that pod no longer exists, then hand the run to a new worker by echoing that name back:

```bash
curl -X POST -u <admin> \
  "https://<cluster>/hopsworks-api/api/admin/dataset-tags/clean/<runId>/resume?holderFenced=true&expectedWorker=<pod>"
```

The echo is checked against the recorded name in the same statement that transfers ownership, so a wrong name moves nothing and a second operator repeating a name that has already been used is refused.
The run keeps its cursor, so it continues rather than starting over.
A run recorded before this release has no worker name; omit `expectedWorker` for it, and confirm it is safe by scaling the API to zero first.

### Reviewing a quarantined value

A tag that could not be migrated is quarantined rather than dropped, recorded by name, reason, byte length and digest, never by value.

```bash
curl -u <admin> \
  "https://<cluster>/hopsworks-api/api/admin/dataset-tags/quarantine?limit=100"
```

Waiving one authorises deleting that value, so it is granted against the digest you read:

```bash
curl -X PUT -u <admin> \
  "https://<cluster>/hopsworks-api/api/admin/dataset-tags/quarantine/<id>/waive?waived=true&expectedDigest=<digest>"
```

If a later pass replaced the payload, the digest no longer matches and the request is refused with HTTP 409 so you can read the new value before deciding.
Pass `waived=false` to clear a waiver, which needs no digest.
