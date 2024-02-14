---
description: Users guide about how to use Hopsworks for vector similarity search 
---

# Introduction
Vector similarity search is a robust technique enabling the retrieval of similar items based on their embeddings or representations. Its applications range across various domains, from recommendation systems to image similarity and beyond. In Hopsworks, this is facilitated through a vector database, such as Opensearch, which efficiently stores and retrieves relevant embeddings. In this guide, we'll walk you through the process of using Hopsworks for vector similarity search step by step.

# Ingesting Data into the Vector Database
Hopsworks provides a user-friendly API for writing data to both online and offline feature stores. The example below illustrates the straightforward process of ingesting data into both the vector database and the offline feature store using a single insert method. 
Currently, Hopsworks supports Opensearch as a vector database. 

First, define the index and embedding features in the vector database. The project index will be used if no index name is provided. 

```aidl
from hsfs import embedding

# Define the index
emb = embedding.EmbeddingIndex(index_name=None)
```

Then, add one or more embedding features to the index. Name and dimension of the embedding features are required for identifying which features should be indexed for k-nearest neighbor (KNN) search. Optionally, you can specify the [similarity function](https://github.com/logicalclocks/feature-store-api/blob/master/python/hsfs/embedding.py#L101).
```aidl
# Define the embedding feature
emb.add_embedding("embedding_heading", len(df["embedding_heading"][0]))
```

Next, create a feature group with the `embedding_index` and ingest data to the feature group. When the `embedding_index` is provided, the vector database is used as online feature store. That is, all the features in the feature group are stored **exclusively** in the vector database. The advantage of storing all features in the vector database is that it enables similarity search, and filtering for all feature values.

```aidl
news_fg = fs.get_or_create_feature_group(
    name=f"news_fg",
    embedding_index=emb,  # Specify the embedding index
    primary_key=["id1"],
    version=version,
    online_enabled=True,
    topic_name=f"news_fg_{version}_onlinefs"
)

# Ingest data into both the vector database and the offline feature store
news_fg.insert(df, write_options={"start_offline_backfill": True})
```

# Querying Similar Embeddings
The read API is designed for ease of use, enabling developers to seamlessly integrate similarity search into their applications. To retrieve features from the vector database, you only need to provide the target embedding as a search query using [`find_neighbors`](https://github.com/logicalclocks/feature-store-api/blob/master/python/hsfs/feature_group.py#L2141). It is also possible to filter features saved in the vector database.

```aidl
# Search neighbor embedding with k=3
news_fg.find_neighbors(model.encode(news_description), k=3)

# Filter and search
news_fg.find_neighbors(model.encode(news_description), k=3, filter=news_fg.newstype == "sports")
```

To retrieve features at a specific time in the past from the offline database for analysis, you can utilize the offline read API to perform time travel.

```aidl
# Time travel and read from the offline feature store
news_fg.as_of(time_in_past).read()
```

## Second Phase Reranking

In some ML applications, second phase reranking of the top k items fetched by first phase filtering is common where extra features are required from other sources after fetching the k nearest items. In practice, it means that an extra step is needed to fetch the features from other feature groups in the online feature store. Hopsworks provides yet another simple read API for this purpose. Users can create a feature view by joining multiple feature groups and fetch all the required features by calling fv.find_neighbors. In the example below, view_cnt from another feature group is also returned to the result.

```aidl
view_fg = fs.get_or_create_feature_group(
    name="view_fg",
    primary_key=["id1"],
    version=version,
    online_enabled=True,
    topic_name=f"view_fg_{version}_onlinefs"
)

fv = fs.get_or_create_feature_view(
    "news_cnt", version=version,
    query=news_fg.select(["date", "heading", "newstype"]).join(view_fg.select(["view_cnt"])))

fv.find_neighbors(model.encode(news_description), k=5)
```

It is also possible to get back feature vector by providing the primary keys, but it is not recommended as explained in the next section. The client fetches feature vector from the vector store and the online store for `news_fg` and `view_fg` respectively.
```aidl
fv.get_feature_vectors({"id1": 1})
```

# Best Practices
1. Choose the appropriate online feature stores 

There are 2 types of online feature stores in Hopsworks: online store (RonDB) and vector store (Opensearch). Online store is designed for retrieving feature vectors efficiently with low latency. Vector store is designed for finding similar embedding efficiently. If similarity search is not required, using online store is recommended for low latency retrieval of feature values including embedding.

2. Choose the features to store in vector store

While it is possible to update feature value in vector store, updating feature value in online store is more efficient. If you have features which are frequently being updated and do not require for filtering, consider storing them separately in a different feature group. As shown in the previous example, `view_cnt` is updated frequently and stored separately. You can then get all the required features by using feature view.

# Next step
Explore the [notebook example](https://github.com/kennethmhc/news-search-knn-demo/blob/main/news-search-knn-demo.ipynb), demonstrating how to use Hopsworks for implementing a news search application. You can search for news using natural language in the application, powered by the Hopsworks vector database.