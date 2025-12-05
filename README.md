# Hopsworks Documentation

This is the source of the Hopsworks Documentation published at <https://docs.hopsworks.ai>.

## Build instructions

### Step 1: Setup python environment

Create a python 3.10 environment, using a python environment manager of your own choosing. For example `virtualenv` or `anaconda`.

### Step 2

Clone this repository

```bash
git clone https://github.com/logicalclocks/logicalclocks.github.io.git
```

### Step 3

Install the required dependencies to build the documentation in the python environment created in the previous step.

**Note that {PY_ENV} is the path to your python environment.**

```bash
cd logicalclocks.github.io
{PY_ENV}/bin/pip3 install -r requirements-docs.txt
```

### Step 4

Use mkdocs to build the documentation and serve it locally

```bash
{PY_ENV}/bin/mkdocs serve
```

The documentation should now be available locally on the following URL: <http://127.0.0.1:8000/>

## Adding new pages

The `mkdocs.yml` file of this repository defines the pages to show in the navigation.
After adding your new page in the docs folder, you also need to add it to this file for it to show up in the navigation.

## Checking links

``` bash
# run the server
mkdocs serve  > /dev/null 2>&1 &
SERVER_PID=$!
echo "mk server in PID $SERVER_PID"
# Give enough time for serving
sleep 30
echo "Launching linkchecker"
linkchecker http://127.0.0.1:8000/

# If ok just kill the server
kill -9 $SERVER_PID
```

## Setup and Build Documentation

We use `mkdocs` together with `mike` ([for versioning](https://github.com/jimporter/mike/)) to build the documentation and a plugin called `keras-autodoc` to auto generate Python API documentation from docstrings.

**Background about `mike`:**
`mike` builds the documentation and commits it as a new directory to the gh-pages branch.
Each directory corresponds to one version of the documentation.
Additionally, `mike` maintains a json in the root of gh-pages with the mappings of versions/aliases for each of the directories available.
With aliases you can define extra names like `dev` or `latest`, to indicate stable and unstable releases.

### Versioning on docs.hopsworks.ai

On docs.hopsworks.ai we implement the following versioning scheme:

- current master branches (e.g. of hopsworks corresponding to master of Hopsworks): rendered as current Hopsworks snapshot version, e.g. **4.0.0-SNAPSHOT [dev]**, where `dev` is an alias to indicate that this is an unstable version.
- the latest release: rendered with full current version, e.g. **3.8.0 [latest]** with `latest` alias to indicate that this is the latest stable release.
- previous stable releases: rendered without alias, e.g. **3.4.4**.

### 4. Build Instructions

For this you can either checkout and make a local copy of the `upstream/gh-pages` branch, where `mike` maintains the current state of docs.hopsworks.ai, or just build documentation for the branch you are updating:

Building *one* branch:

Checkout your dev branch with modified docs:

```bash
git checkout [dev-branch]
```

Generate API docs if necessary:

```bash
python auto_doc.py
```

Build docs with a version and alias

```bash
mike deploy [version] [alias] --update-alias

# for example, if you are updating documentation to be merged to master,
# which will become the new SNAPSHOT version:
mike deploy 4.0.0-SNAPSHOT dev --update-alias

# if you are updating docs of the latest stable release branch
mike deploy [version] latest --update-alias

# if you are updating docs of a previous stable release branch
mike deploy [version]
```

If no gh-pages branch existed in your local repository, this will have created it.

**Important**: If no previous docs were built, you will have to choose a version as default to be loaded as index, as follows

```bash
mike set-default [version-or-alias]
```

You can now checkout the gh-pages branch and serve:

```bash
git checkout gh-pages
mike serve
```

You can also list all available versions/aliases:

```bash
mike list
```

Delete and reset your local gh-pages branch:

```bash
mike delete --all

# or delete single version
mike delete [version-or-alias]
```