# Documentation landing page

This is the source of the landing page for https://docs.hopsworks.ai

## Build instructions
### If you are using Windows machine, please perform next operations in Git Bash or another Bash emulator for Windows.

### Step 1

Create a python 3.8 environment, using a python environment manager of your own choosing. For example `virtualenv` or `anaconda`.

### Step 2

Install the required dependencies to build the documentation in the python environment created in the previous step.

**Note that {PY_ENV} is the path to your python environment.**

```bash
{PY_ENV}/bin/pip3 install 'git+https://github.com/logicalclocks/feature-store-api@master#egg=hsfs[docs]&subdirectory=python'
```

### Step 3

Clone this repository

```bash
git clone https://github.com/logicalclocks/logicalclocks.github.io.git
```

### Step 4

Go inside the cloned repository

```bash
cd logicalclocks.github.io
```

### Step 5

Use mkdocs to build the documentation and serve it locally

```bash
{PY_ENV}/bin/mkdocs serve
```

The documentation should now be available locally on the following URL: http://127.0.0.1:8000/

## Adding new pages

The `mkdocs.yml` file of this repository defines the pages to show in the navigation.
After adding your new page in the docs folder, you also need to add it to this file for it to show up in the navigation.
