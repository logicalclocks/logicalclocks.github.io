# Vector Index

A vector index stores embeddings so you can retrieve the items most similar to a query vector, the retrieval half of a recommender or a RAG system.
In Hopsworks, a vector index is a property of an online-enabled feature group: a feature group with an embedding column can be indexed for similarity search, alongside its online and offline stores.

The vector index is backed by OpenSearch, included as a multi-tenant service in projects.
OpenSearch provides the index through its k-NN plugin, which supports several engines for embedding indexes.
Hopsworks creates its indexes on the FAISS engine, which is the default from Hopsworks 5.1.
Earlier releases used the nmslib engine, which OpenSearch has deprecated and which does not accept the filter that Hopsworks 5.1 and later send inside the nearest-neighbor query, so the upgrade to Hopsworks 5.2 recreates those indexes on FAISS.
The [OpenSearch upgrade guide][upgrading-opensearch] describes what that upgrade involves.
Through Hopsworks, OpenSearch also provides enterprise capabilities, including authentication and access control to indexes (an index can be private to a Hopsworks project), filtering, scalability, high availability, and disaster recovery support.
To learn how OpenSearch powers vector similarity search in Hopsworks, you can see [this guide](../../user_guides/fs/vector_similarity_search.md).

--8<-- "concepts/mlops/opensearch/vector-index.html"
