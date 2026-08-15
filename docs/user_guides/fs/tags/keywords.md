# Keywords

## Introduction

A keyword is a single user-defined word attached to a feature group, feature view or training dataset.
Keywords are free text with no schema behind them, which makes them the lighter alternative to [tags][tags-guide]: use a keyword to make an artifact easier to find, and a tag when the metadata has to be structured and validated.

Keywords are indexed for free-text search alongside names, descriptions and tags.
They can also be used as a filter in the search API.

Keywords are not available on models, deployments, jobs or datasets.
A keyword filter passed to a job or dataset search therefore matches nothing.

## Read the keywords of an artifact

=== "Python"

    ```python
    fg = fs.get_feature_group("transactions_4h_aggs_fraud_batch_fg", version=1)

    fg.get_keywords()  # ["fraud", "eu_region"]
    ```

Keywords record the time they were added, from the release that introduced this guide onwards.

=== "Python"

    ```python
    for keyword, added in fg.get_keywords_metadata().items():
        print(keyword, added)
    ```

`added` is `None` for keywords attached before that release, and against an older backend that does not report the time.

## Add, replace and delete keywords

=== "Python"

    ```python
    # Add to the existing set
    fg.add_keywords("pii")
    fg.add_keywords(["fraud", "eu_region"])

    # Replace the whole set
    fg.set_keywords(["fraud", "pii"])

    # Remove one
    fg.delete_keyword("pii")
    ```

Each of these returns the resulting set of keywords.

!!! warning "add_keywords is not atomic"
    `add_keywords` reads the current set, adds to it, and writes the whole set back.
    Two calls running at the same time can therefore lose one of the additions.
    Use `set_keywords` when the caller already knows the full set it wants.

The same five methods are available on `FeatureView` and `TrainingDataset`.
On a feature view, the training datasets it owns are reached through the `*_training_dataset_keywords` variants, which take the training dataset version as their first argument.

=== "Python"

    ```python
    fv = fs.get_feature_view("transactions_fv", version=1)

    fv.get_training_dataset_keywords(1)
    fv.add_training_dataset_keywords(1, "backfill")
    ```

## The cluster vocabulary

`get_all_keywords` returns every keyword used on the cluster, not only those in the current project.
Use it to offer autocompletion, or to check whether a word is already in use before introducing a variant of it.

=== "Python"

    ```python
    fs.get_all_keywords()
    ```

## Command line

```bash
hops fg keywords transactions_4h_aggs_fraud_batch_fg
hops fg add-keyword transactions_4h_aggs_fraud_batch_fg fraud
hops fg remove-keyword transactions_4h_aggs_fraud_batch_fg fraud
```

The same three commands exist for feature views (`hops fv`) and training datasets (`hops td`).

!!! warning "`--value` on the keyword commands is being removed"
    `--value` used to make `hops fg add-keyword` write a tag rather than a keyword.
    It is now rejected with a message naming `hops fg add-tag` as the replacement, and it is removed in the following release.
    Attach a tag with the tag commands, described in the [Tags][tags-guide] guide.
