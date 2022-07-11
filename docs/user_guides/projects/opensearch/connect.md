# How To Connect To OpenSearch

## Introduction

Text here

!!! notice "Limited to internal Jobs and Notebooks"
    Currently it's only possible to configure the opensearch-py client in a job or jupyter notebook running inside the Hopsworks cluster.


## Code

In this guide, you will learn how to connect to the OpenSearch cluster using an [opensearch-py](https://opensearch.org/docs/1.3/clients/python/) client. 

### Step 1: Get the OpenSearch API

```python

import hopsworks

connection = hopsworks.connection()

project = connection.get_project()

opensearch_api = project.get_opensearch_api()

```

### Step 2: Configure the opensearch-py client

```python

from opensearchpy import OpenSearch

client = OpenSearch(**opensearch_api.get_default_py_config())

```

### API Reference

[OpenSearch](https://docs.hopsworks.ai/hopsworks-api/dev/generated/api/open_search/)

## Conclusion

In this guide you learned how to connect to the OpenSearch cluster. You can now use the client to interact directly with the OpenSearch cluster, such as [vector database](../../mlops/vector_database/index.md).
