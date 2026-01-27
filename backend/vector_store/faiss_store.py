import os
import pickle
import faiss
import numpy as np

def create_faiss_index(repo_name, vectors, metadata, save_path="vector_store"):
    os.makedirs(save_path, exist_ok=True)

    # Convert vectors → numpy array (float32 required by FAISS)
    vec_array = np.array(vectors).astype("float32")

    dim = vec_array.shape[1]  # embedding dimension

    index = faiss.IndexFlatL2(dim)
    index.add(vec_array)

    # Save index
    faiss.write_index(index, f"{save_path}/{repo_name}_faiss.index")

    # Save metadata (pickle)
    with open(f"{save_path}/{repo_name}_metadata.pkl", "wb") as f:
        pickle.dump(metadata, f)

    print("[+] Saved FAISS index and metadata")
    print("[+] Total vectors indexed:", index.ntotal)

    return index
def load_faiss_index(repo_name, load_path="vector_store"):
    index = faiss.read_index(f"{load_path}/{repo_name}_faiss.index")

    with open(f"{load_path}/{repo_name}_metadata.pkl", "rb") as f:
        metadata = pickle.load(f)

    return index, metadata
    
def search_similar(repo_name, query_text, top_k=20, load_path="vector_store"):
    from sentence_transformers import SentenceTransformer
    import numpy as np

    # Load index + metadata
    index, metadata = load_faiss_index(repo_name, load_path)

    # Load same embedding model for query
    model = SentenceTransformer("BAAI/bge-small-en-v1.5")

    # Convert query → embedding
    query_vec = model.encode(query_text).astype("float32").reshape(1, -1)

    # Search
    distances, indices = index.search(query_vec, top_k)

    # Return top results with metadata
    results = []
    for idx, dist in zip(indices[0], distances[0]):
        if idx < len(metadata):
            results.append({
                "distance": float(dist),
                "chunk": metadata[idx]
            })

    return results