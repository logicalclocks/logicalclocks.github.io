---
description: Give another project read access to a Trino catalog or a feature group through the query engine, at catalog, schema, table or column level, with masked columns.
---

# Sharing Catalogs and Feature Groups

The query engine enforces who can read what, so data one project owns is not visible to another project until it is shared.
Two kinds of share reach the query engine:

- A **catalog share** gives another project read access to one of your Trino catalogs: the whole catalog, one schema, one table, or some columns of a table, optionally with masked values.
- A **feature group share**, made from the feature store, also makes the shared feature group queryable through the query engine in the receiving project.

A share always grants read access, and always to the receiving project's Data Owners and Data Scientists.
Changes take effect within seconds, without restarting the query engine.

## Sharing a catalog

A project catalog is shared by a Data Owner of the project, and a private catalog by its owner, from any of their projects.
A catalog can be shared once it is **Approved**, because a catalog the query engine has not loaded has nothing to share yet.

Click the share icon on the catalog's row in **Query Engine** → **Catalogs** to open its sharing page.
The page lists every share of the catalog, what each one covers, and whether it is live.

<figure>
  <img src="../../../../assets/images/guides/trino/catalog-sharing-page.png" alt="Sharing page of a catalog" />
  <figcaption>A catalog shared whole with one project, and one table with two of its three columns, one of them masked, with another</figcaption>
</figure>

Click **Share**, choose the project, and choose what to share:

- **The whole catalog**: every schema and table in it, including ones created later, optionally with some tables restricted or left out.
- **One schema**: every table in that schema, including ones created later, optionally with some tables restricted or left out.
- **One table**: that table only, optionally narrowed to some of its columns.

<figure>
  <img src="../../../../assets/images/guides/trino/share-dialog-table.png" alt="Sharing one table with some columns" />
  <figcaption>Sharing one table, with one column left out and one column masked</figcaption>
</figure>

The schemas, tables and columns offered are the ones you can see in the catalog yourself, read through the catalog's own connection.

### Sharing some columns of a table

Check **Share only some columns, or mask them** to choose the columns of a table share.
An unchecked column cannot be read by the receiving project, and a query that selects it, or selects `*`, is refused.
The table's other ways of revealing a column are closed too: the connector's hidden columns, such as `$path` and `$partition`, and the table's metadata tables, such as `<table>$partitions`, are denied on a column-restricted share, because the path and partition values of a table partitioned on an unshared column carry that column's values.

The query engine denies the columns that were unchecked when the share was saved.
A column added to the table later is therefore readable until you save the share again.
The sharing page flags such a table with the new column names, and **Exclude them** saves the share again with the new columns left unshared.

<figure>
  <img src="../../../../assets/images/guides/trino/share-edit-columns.png" alt="Editing the columns of a share" />
  <figcaption>Editing a column share: two columns shared, one of them masked, and one left out</figcaption>
</figure>

### Masking a column

A shared column can carry a mask, which replaces the value the receiving project reads.
A mask is one SQL expression over the row, for example `'***'` or `regexp_replace(email, '.+@', '***@')`, and it must return the column's own type.

A mask runs as the person querying, not as you, so it can use only what they can read: the checked columns of the same table.
A mask that refers to an unchecked column, or to another table, is refused when you save the share.
It cannot contain `;` or a comment, and it is limited to 2000 characters.
The mask is checked against the table when the share is saved, so an expression the query engine cannot evaluate is reported then rather than when someone queries the table.

<figure>
  <img src="../../../../assets/images/guides/trino/query-masked-column.png" alt="Querying a masked column" />
  <figcaption>The receiving project reads the masked column as <code>***</code></figcaption>
</figure>

You always read your own catalog unmasked.

### Restricting tables of a schema or catalog share

A schema or catalog share can make exceptions for some of its tables.
Check **Restrict or leave out some tables**, click **Add a table**, and choose the columns to share from it, with masks, the same way as for a table share.
Every other table is shared whole.

- A restricted table shares only its checked columns, and its hidden columns and metadata tables are denied, as on a column-restricted table share.
- A table with no column checked is left out: the receiving project cannot read it, and it is not listed to them.

As with a table share, a column added to a restricted table later is readable until you save the share again, and the sharing page flags it.
Edit the share to add, change or remove its restrictions.

### Shares that overlap

A project holds at most one share of any object in a catalog.
Sharing a table with a project that already has its schema or the whole catalog is refused, and so is sharing a schema or the catalog with a project that already has a share inside it.
To give that project less of one table, restrict the table on the share it already has; to widen a table share into a schema share, revoke the table share first.
Shares of objects that do not contain each other, such as two tables or two schemas, can be held side by side.

### The status of a share

A share is live once the query engine has loaded the rules that include it, which takes a few seconds.
The sharing page shows where each share stands and refreshes itself while a change is being applied.

| Status | Meaning |
| --- | --- |
| Applying | Saved, and being made live. |
| Active | Live: the receiving project can read what it covers. |
| Revoking | Being removed. The receiving project loses access when this finishes. |
| Failed | Could not be made live. The status carries the reason; share it again to retry. |

### Objects that no longer exist

A share names a schema or a table, and the object it names may be dropped at the source later.
The share stays, and the sharing page marks it **Not found**.
If an object with the same name is created again, the share applies to it, so revoke a share whose object is gone for good.

### Revoking a share

Click the delete icon on a share to revoke it.
The receiving project loses access as soon as the revoke is live, within seconds, and the share disappears from the page once it is.
The same object cannot be shared with the same project again until the revoke has finished.

Deleting a catalog revokes all of its shares at once, and so does deleting the receiving project.

### Shares your project received

The **Catalogs** tab lists, under **Shared with this project**, every catalog share your project received, who it comes from, and what it covers.
A shared catalog is queried by its own name, like any other catalog, with the SQL runner or any Trino client.

<figure>
  <img src="../../../../assets/images/guides/trino/received-shares.png" alt="Shares received by a project" />
  <figcaption>A project catalog shared whole, and one table of another user's private catalog</figcaption>
</figure>

## Sharing feature groups through the query engine

A feature group shared with another project, as described in [Sharing a feature group with selected features][sharing-a-feature-group-with-selected-features], is also queryable by that project through the query engine.
Where it is read from depends on whether the whole feature group was shared or a subset of its features.

| Shared | Catalog | Readable |
| --- | --- | --- |
| The whole feature group, or the whole feature store | The catalog named after the feature group's format: `delta`, `hudi`, `iceberg` or `hive` | Every feature |
| A subset of the features | The shared catalog of its format: `delta_shared`, `hudi_shared` or `iceberg_shared` | The shared features only |

The schema is the owning project's feature store, `<project>_featurestore`, and the table is `<feature group>_<version>`.

The share dialog says which catalog the other project will read from, or that the share is not queryable through the query engine.

<figure>
  <img src="../../../../assets/images/guides/trino/fg-share-subset.png" alt="Sharing a subset of a feature group" />
  <figcaption>A subset of the features is read through <code>delta_shared</code></figcaption>
</figure>

### A subset of the features

A subset share is read through the shared catalog of the feature group's format.
The primary key and the event time are always shared, and the receiving project reads the other shared features alongside them.

```sql
SELECT datetime, cc_num, category, amount
FROM delta_shared.fraud_featurestore.transactions_1;
```

<figure>
  <img src="../../../../assets/images/guides/trino/query-shared-features.png" alt="Querying a subset share" />
  <figcaption>Only the shared features are listed, and the preview selects them by name</figcaption>
</figure>

Everything else in the table is denied: the unshared features, the connector's hidden columns such as `$path`, and the table's metadata tables such as `transactions_1$history`.
A query that selects an unshared feature, or selects `*`, is refused.

<figure>
  <img src="../../../../assets/images/guides/trino/query-unshared-feature-denied.png" alt="Querying an unshared feature" />
  <figcaption>Selecting a feature that was not shared is refused</figcaption>
</figure>

The shared catalogs are visible only to projects that received a subset share, and a project sees only the feature groups shared with it there.
A subset share is not readable through the catalog named after the format, and a whole share is not readable through the shared catalog.

Adding features to a shared feature group does not widen the share: a new feature stays unreadable by the receiving project until you share it.
Unsharing the feature group, or deleting it, removes access within seconds.

### Feature groups that are not queryable

Two kinds of feature group cannot be read through the query engine by the receiving project:

- A feature group on an external data source, whether shared whole or in part, because its data does not live in the feature store's tables.
- A subset of a feature group stored as a plain Hive table, without Delta, Hudi or Iceberg, because there is no shared catalog for that format.
  Such a feature group shared whole is read through the `hive` catalog.

The share dialog says so for these feature groups, and the feature group remains shared and readable through the feature store APIs.
