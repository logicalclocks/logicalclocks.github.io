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

Set `tagLifecycle.writeWindow.enabled=false` to skip it, only if you are taking the write window yourself.

After the upgrade the cluster keeps reading dataset tags from the extended attributes and writes them to both stores.
Nothing is lost while you stay in that state, and you can stay in it indefinitely.

## Per-file tags are frozen

Tags could previously be attached to any file or directory inside a dataset.
Attaching a new tag to a path inside a dataset is now rejected with HTTP 400.
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
Rolling back is therefore not made safe; it is refused.

`tagLifecycle.admissionPolicy.enabled=true` installs a `ValidatingAdmissionPolicy` that refuses to admit an API pod below the current capability epoch.
It is **off by default**, because turning it on means an emergency downgrade requires restoring the pre-cut-over database and deleting the policy, in that order.
A cluster that never cuts over never needs it.

The cut-over refuses to run while the policy is absent, and the operator who accepts the risk says so explicitly with `tagLifecycle.cutover.acceptUnfencedRollback=true`, which is rendered into the Job and logged with the decision.

## The cut-over

The cut-over moves the canonical store from the extended attributes to the database.
It is a scheduled maintenance action, not an administrative call to make at an arbitrary moment: dataset tag **writes** are refused with a retryable HTTP 503 from the start of the window until it commits.
Dataset tag **reads** are never interrupted, and nothing else on the cluster is affected.

The window is about five minutes on a three-node cluster, dominated by the API restart.
The verification over several hundred datasets takes seconds.

Run it by setting `tagLifecycle.cutover.run=true` on a `helm upgrade`.
The value is off by default and the Job runs once per upgrade that sets it.

!!! note "Helm 4 needs `--force-conflicts`"
    Under Helm 4, pass `--force-conflicts` to the upgrade.
    Server-side apply refuses fields owned by other field managers, which a running cluster always has, and without the flag the upgrade fails before any hook runs.
    This is a pre-existing Helm 4 behaviour, not specific to the cut-over.

The Job:

1. Reads the cut-over status while the cluster is up.
   A database that is already canonical exits immediately, so the Job is safe to leave enabled across upgrades, and a window an earlier attempt left open is resumed at the final sweep rather than opened twice.
2. Reads the admission policy and its binding from the Kubernetes API and checks the whole contract: that it denies rather than warns, that it fails closed, that it selects this namespace and both API deployments, and that it names the current epoch.
   A policy with the right name but any of those wrong is not a fence.
3. Refuses to start unless the rolling upgrade has been activated, the background migration of existing tags reports done, and no tag was quarantined for failing validation.
4. Records the current replica counts, scales both API deployments to zero, and waits until their pods are gone.
   At that instant every write that was in flight has either reached the file system or never will, so nothing is left to drain.
5. Sets the state to `cutting_over` while nothing is running, then restores the replica counts.
   The API comes back refusing dataset tag writes with `CUTOVER_IN_PROGRESS`.
6. Runs a final migration pass and then a verification, and stops if the verification reports any difference between the two stores.
7. Commits.
   Every precondition is checked again inside the transaction that publishes the new state.

If the Job stops at step 6, the cluster stays in `cutting_over` with reads unaffected.
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
Readers holding a cached copy of the cluster state for up to one cache interval would otherwise read a store that had already been emptied, so the extended attributes are removed no earlier than one full cache interval afterwards, and only after the verification has passed.

Removing them is the point of no return for a downgrade, so keep them until the release is known good.
