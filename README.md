# Documentation landing page

This is the source of the landing page for https://docs.hopsworks.ai

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

The documentation should now be available locally on the following URL: http://127.0.0.1:8000/

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


## Maintenance
Always update the robot.txt to desintex previous versions of hopsworks documentation (located in doc/robots.txt) 

