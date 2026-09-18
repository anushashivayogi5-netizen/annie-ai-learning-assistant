import faiss
import numpy as np


def create_vector_index(embeddings):
    embeddings_array = np.array(embeddings).astype("float32")

    dimension = embeddings_array.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings_array)

    return index


def search_similar_chunks(index, query_embedding, top_k=3):
    query_array = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(query_array, top_k)

    return distances[0], indices[0]