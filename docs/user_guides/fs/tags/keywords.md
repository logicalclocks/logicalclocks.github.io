# Keywords { #keywords-guide }

## Introduction

A keyword is a single free-form word attached to a feature group, a feature view or a training dataset.
Keywords need no schema and no administrator: any project member with write access can invent one and attach it.

That is the difference from [tags][tags-guide], and it decides which to reach for.
A tag is validated against a schema and is the right tool for governance, where the set of allowed keys and values has to be agreed in advance.
A keyword is the right tool for discovery, where the point is to label something now and find it later.

Keywords apply to feature groups, feature views and training datasets only.
Jobs, apps, models and deployments take tags but not keywords, so a keyword filter never matches them.

## Read the keywords of an artifact

=== "Python"

    ```python
    fg = fs.get_feature_group("transactions_4h_aggs_fraud_batch_fg", version=1)

    fg.get_keywords()
    # ['fraud', 'aggregations', 'hourly']
    ```

To see when each keyword was attached, use `get_keywords_metadata()`, which returns a dict of keyword to attachment time:

=== "Python"

    ```python
    for keyword, attached in fg.get_keywords_metadata().items():
        print(keyword, attached)
    ```

The attachment time is an aware UTC `datetime`, or `None` when it is unknown.
It is `None` for keywords attached before the cluster began recording attachment times, so `None` does not mean the keyword is new.

## Add, replace and delete keywords

Three methods change the keyword set, and they differ in what they do to the keywords already there.

`add_keywords()` adds to the set and leaves the rest alone.
It accepts one keyword or a list:

=== "Python"

    ```python
    fg.add_keywords("fraud")
    fg.add_keywords(["aggregations", "hourly"])
    ```

`set_keywords()` replaces the whole set.
Anything not in the list you pass is removed, so use it when you intend the artifact to end up with exactly these keywords and nothing else:

=== "Python"

    ```python
    fg.set_keywords(["fraud", "hourly"])
    ```

`delete_keyword()` removes a single keyword:

=== "Python"

    ```python
    fg.delete_keyword("hourly")
    ```

All three return the resulting keyword set, so a read-back is not needed to see the effect.

The same methods exist on feature views.
A training dataset's keywords are reached through its feature view, because a training dataset is identified by the feature view it was created from plus its own version:

=== "Python"

    ```python
    fv = fs.get_feature_view("fraud_detection", version=1)

    fv.add_training_dataset_keywords(1, "baseline")
    fv.get_training_dataset_keywords(1)
    fv.delete_training_dataset_keyword(1, "baseline")
    ```

## The cluster vocabulary

Keywords are free-form, which makes them prone to near-duplicates: `fraud`, `Fraud` and `fraud_detection` are three separate keywords that fragment the same idea.
To let you reuse a word someone has already chosen, the feature store can list every keyword in use:

=== "Python"

    ```python
    fs.get_all_keywords()
    ```

The vocabulary is cluster-wide rather than project-scoped, so it shows words in use in projects you are not a member of.
Only the words are returned, never which artifact or project they came from, so this discloses no artifact you could not otherwise see.

## Command line

The CLI covers the same operations:

```bash
# feature group keywords
hops fg keywords transactions_fg --version 1
hops fg add-keyword transactions_fg fraud --version 1
hops fg remove-keyword transactions_fg fraud --version 1

# feature view keywords
hops fv keywords fraud_detection --version 1
hops fv add-keyword fraud_detection baseline --version 1
hops fv remove-keyword fraud_detection baseline --version 1

# training dataset keywords, addressed by feature view name and td version
hops td keywords fraud_detection 1 --fv-version 1
hops td add-keyword fraud_detection 1 baseline --fv-version 1
hops td remove-keyword fraud_detection 1 baseline --fv-version 1
```

The listing commands show the attachment time next to each keyword.

!!! warning "The `*-keyword` commands changed meaning"
    They used to operate on tags, which are name and value pairs.
    They now operate on keywords, which are plain labels, and tags moved to `hops fg tags`, `hops fg add-tag` and `hops fg remove-tag`.
    A script that passed a tag value to `add-keyword` needs to move to `add-tag`, because a keyword has no value to pass.
    The commands print this notice to stderr when they run.

## Searching by keyword

Keywords are indexed, and can be filtered on directly rather than only matched as free text.
See the [tag and keyword search guide][search-with-tags-and-keywords].
