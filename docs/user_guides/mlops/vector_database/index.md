# How To Use OpenSearch k-NN plugin

## Introduction

The k-NN plugin enables users to search for the k-nearest neighbors to a query point across an index of vectors. To determine the neighbors, you can specify the space (the distance function) you want to use to measure the distance between points.

Use cases include recommendations (for example, an “other songs you might like” feature in a music application), image recognition, and fraud detection.

!!! notice "Limited to internal Jobs and Notebooks"
Currently it's only possible to configure the opensearch-py client in a job or jupyter notebook running inside the Hopsworks cluster.

## Code

In this guide, you will learn how to create a simple recommendation application, using the `k-NN plugin` in OpenSearch.

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

### Step 3: Create an index

Create an index to use by calling `opensearch_api.get_project_index(..)`.

```python

knn_index_name = opensearch_api.get_project_index("demo_knn_index")

index_body = {
    "settings": {
        "knn": True,
        "knn.algo_param.ef_search": 100,
    },
    "mappings": {
        "properties": {
            "my_vector1": {
                "type": "knn_vector",
                "dimension": 2
            }
        }
    }
}

response = client.indices.create(knn_index_name, body=index_body)

print(response)

```

### Step 4: Bulk ingestion of vectors

Ingest 10 vectors in a bulk fashion to the index. These vectors represent the list of vectors to calculate the similarity for.

```python

from opensearchpy.helpers import bulk
import random

actions = [
    {
        "_index": knn_index_name,
        "_id": count,
        "_source": {
            "my_vector1": [random.uniform(0, 10), random.uniform(0, 10)],
        }
    }
    for count in range(0, 10)
]

bulk(
    client,
    actions,
)

```

### Step 5: Score vector similarity

Score the vector `[2.5, 3]` and find the 3 most similar vectors.

```python

# Define the search request
query = {
    "size": 3,
    "query": {
        "knn": {
            "my_vector1": {
                "vector": [2.5, 3],
                "k": 3
            }
        }
    }
}

# Perform the similarity search
response = client.search(
    body = query,
    index = knn_index_name
)

# Pretty print response
import pprint
pp = pprint.PrettyPrinter()
pp.pprint(response)

```

`Output` from the above script shows the score for each of the three most similar vectors that have been indexed.

`[4.798869166444522, 4.069064892468535]` is the most similar vector to `[2.5, 3]` with a score of `0.1346312`.

```bash

2022-05-30 09:55:50,529 INFO: POST https://10.0.2.15:9200/my_project_demo_knn_index/_search [status:200 request:0.017s]
{'_shards': {'failed': 0, 'skipped': 0, 'successful': 1, 'total': 1},
 'hits': {'hits': [{'_id': '9',
                    '_index': 'my_project_demo_knn_index',
                    '_score': 0.1346312,
                    '_source': {'my_vector1': [4.798869166444522,
                                               4.069064892468535]},
                    '_type': '_doc'},
                   {'_id': '0',
                    '_index': 'my_project_demo_knn_index',
                    '_score': 0.040784083,
                    '_source': {'my_vector1': [6.267438489652193,
                                               6.0538134453735175]},
                    '_type': '_doc'},
                   {'_id': '7',
                    '_index': 'my_project_demo_knn_index',
                    '_score': 0.03222388,
                    '_source': {'my_vector1': [7.973873201006634,
                                               2.7361877621502115]},
                    '_type': '_doc'}],
          'max_score': 0.1346312,
          'total': {'relation': 'eq', 'value': 3}},
 'timed_out': False,
 'took': 9}


```

### API Reference

[k-NN plugin](https://opensearch.org/docs/1.3/search-plugins/knn/knn-index/)

[OpenSearch](https://docs.hopsworks.ai/hopsworks-api/dev/generated/api/open_search/)

## Conclusion

In this guide you learned how to create a simple recommendation application.