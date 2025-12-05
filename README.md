# Hopsworks Documentation

This is the source of the Hopsworks Documentation published at <https://docs.hopsworks.ai>.

## Build instructions

We use `mkdocs` together with [`mike`]((https://github.com/jimporter/mike/) for versioning to build the documentation.
We also use this two main mkdocs plugins: [`mkdocstrings`](https://mkdocstrings.github.io/) and [its Python handler](https://mkdocstrings.github.io/python/), and [`mkdocs-material`](https://squidfunk.github.io/mkdocs-material/) as the theme.

**Background about `mike`:**
`mike` builds the documentation and commits it as a new directory to the `gh-pages` branch.
Each directory corresponds to one version of the documentation.
Additionally, `mike` maintains a json in the root of `gh-pages` with the mappings of versions/aliases for each of the directories available.
With aliases, you can define extra names like `dev` or `latest`, to indicate stable and unstable releases.

### Versioning on docs.hopsworks.ai

On docs.hopsworks.ai we implement the following versioning scheme:

- the latest release: rendered with full current version, e.g. **4.4 [latest]** with `latest` alias to indicate that this is the latest stable release.
- previous stable releases: rendered without alias, e.g. **4.3**.

### Step 1

Clone this repository:

```bash
git clone https://github.com/logicalclocks/logicalclocks.github.io.git
```

### Step 2

Create a python virtual environment to build the documentation:

```bash
uv venv
uv pip install -r requirements-docs.txt
# Install hopsworks-api for gathering docstrings for the API reference
uv pip install git+https://github.com/logicalclocks/hopsworks-api.git@main#subdirectory=python
```

Alternatively, you can just activate the virtual environment you use for development of `hopsworks-api` (obtained via `uv sync`), this is the way it is done in the actions.
Namely, in `.github/workflows/mkdocs-release.yml` and `.github/workflows/mkdocs-test.yml`, the `hopsworks-api` repo is cloned, and its uv virtual environment is used with `dev` extra and all development groups.

A callback is set in `hopsworks-api` GitHub Actions, which triggers `.github/workflows/mkdocs-release.yml` on any pushes to release branches (that is, `branch-x.x`).

### Step 3

Build and serve the docs using mike.

```bash
# Use the current version instead of 4.4:
mike deploy 4.4 latest --update-alias
# Next, serve the docs to access them locally:
mike serve
```

**Important**: The first time you serve the docs, you have to choose a default version, as follows:

```bash
mike set-default latest
```

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
