# Search { #search-guide }

## Introduction

Hopsworks indexes your artifacts so you can find them by name, description, [tag][tags-guide] or [keyword][keywords-guide].
This guide covers the search UI and the equivalent REST call.
For what search is and how its scope relates to project membership, see the [search concept page][search-concept].

## What you can search

Search returns ten classes of artifact, each on its own tab:

| Tab | What it contains |
| --- | --- |
| All | Every class below, in one view. The default. |
| Feature Groups | Feature groups. |
| Feature Views | Feature views. |
| Training Datasets | Training datasets. |
| Features | Individual features, matched by feature name. |
| Jobs | Jobs, excluding those that are apps. |
| Apps | Jobs of type PythonApp. |
| Models | Models in a model registry. |
| Deployments | Deployments that serve a registered model. |
| Agents | Deployments that serve no registered model. |

Apps and agents are not separate kinds of artifact, which is why they are not separate tabs in the sense the others are.
An app is a job, and an agent is a deployment.
They appear as their own tabs because the question "which agents are tagged for production" is worth asking on its own, and each tab excludes the other: a job that is an app is reported under Apps and not under Jobs.

Each tab shows the number of matches next to its name, so you can see where the results are without visiting every tab.

## Free-text search

The search box at the top of the UI matches names and descriptions, and the content of tags and keywords.
Matches are highlighted in the results, including the tag key and value that matched, so it is clear why a result was returned.

## Search with tags and keywords

Free text cannot express "the tag `data_privacy` has `pii` set to `true`", because it matches text anywhere in the document.
For that, turn on `Search with Tags & Keywords` above the results.

The panel opens beside the results, and has four rows:

- `Selected:` shows every filter currently applied, each removable on its own, with a `Clear search` action for all of them.
- `Tag:` is a three-column browser: pick a tag schema, then a key within it, then a value for that key.
- `Keyword:` takes a keyword and adds it with `Add keyword filter`.
- `Free-text search:` adds words to the free-text part of the query, with `Add` or by pressing Enter.

Filters combine, so a tag filter and a keyword filter together return only artifacts matching both.

### Only what exists is offered

The three tag columns each have a `filter` box, which matters because a cluster can hold more values than are worth scrolling.
Entries that no artifact you can see actually uses are greyed out and cannot be selected, with the hint `No available matching assets in Hopsworks that use this tag/key/value`.

This is drawn from the tags in use on indexed artifacts, not from the schema definitions.
A schema permitting a value nobody has ever attached will show that value as unavailable, which is deliberate: selecting it could only ever return nothing.

The offered vocabulary respects the scope you are searching, so it never reveals a tag value used only in a project you cannot see.

### Clearing a search

`Clear search results` above the results removes every filter and the free-text term, and resets the per-tab counts.
The same action is in the filter panel as `Clear search`, but the panel is closed by default, so the button above the results is the one to reach for after searching from the text box.

## Search from the API

The REST endpoint is per project and takes the class as `docType`:

```bash
curl -H "Authorization: ApiKey $API_KEY" \
  "https://$HOPSWORKS_HOST/hopsworks-api/api/project/$PROJECT_ID/elastic/featurestore?searchTerm=fraud&docType=ALL"
```

`docType` accepts `ALL`, `FEATURE`, `FEATUREGROUP`, `FEATUREVIEW`, `TRAININGDATASET`, `JOB`, `APP`, `MODEL`, `DEPLOYMENT` and `AGENT`, and defaults to `ALL`.
`from` and `size` page the results, with `size` capped at 10000.

Tag and keyword filters are JSON arrays in the `tags` and `keywords` query parameters.
A tag filter names the schema, and optionally a key and a value within it:

```json
[{"name": "data_privacy", "key": "pii", "value": "true"}]
```

A request must carry at least one of `searchTerm`, `tags` or `keywords`.
Without any of them it is rejected with a `422`, because there is no "match everything" search: the result would be every artifact on the cluster.

The response carries one bucket per class, each with its own total, for example `featuregroups` with `featuregroupsTotal` and `apps` with `appsTotal`.

### API key scopes

Search results are filtered to the scopes of the API key you use, so a key cannot discover a class it was not minted for.
A `FEATURESTORE` key sees feature groups, feature views, training datasets and features, `JOB` sees jobs and apps, `MODELREGISTRY` sees models, and `SERVING` sees deployments and agents.

Naming a `docType` the key does not carry the scope for is rejected, rather than returned empty, so a missing scope is distinguishable from a genuinely empty result.
A `docType=ALL` request is instead narrowed to the classes the key does carry, which is what makes `ALL` usable from a single-scope key.

A search made with a JWT, as the UI and the Python client do after logging in, is not scope-restricted; it is limited by project membership alone.

### The tag vocabulary in use

The endpoint behind the greyed-out entries is available directly:

```bash
curl -H "Authorization: ApiKey $API_KEY" \
  "https://$HOPSWORKS_HOST/hopsworks-api/api/project/$PROJECT_ID/elastic/featurestore/tagfacets"
```

It returns the tags, keys and values attached to artifacts within your search scope.

The answer is read from a bounded number of documents, so on a large cluster it can be incomplete.
When it is, the response sets `partial` to `true`, which means the vocabulary shown is a subset and a value missing from it may still exist.
