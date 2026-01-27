import os
import pickle
import faiss
import numpy as np

def create_faiss_index(repo_name, vectors, metadata, save_path="vector_store"):
    os.makedirs(save_path, exist_ok=True)

    vec_array = np.array(vectors).astype("float32")

    # Normalize for cosine similarity
    norms = np.linalg.norm(vec_array, axis=1, keepdims=True)
    vec_array = vec_array / norms

    dim = vec_array.shape[1]

    # FAISS cosine search uses Inner Product (IP)
    index = faiss.IndexFlatIP(dim)
    index.add(vec_array)

    faiss.write_index(index, f"{save_path}/{repo_name}_faiss.index")

    with open(f"{save_path}/{repo_name}_metadata.pkl", "wb") as f:
        pickle.dump(metadata, f)

    print("[FAISS] Saved cosine index with metadata")

    return index
