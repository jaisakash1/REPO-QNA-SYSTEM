import os
import pickle
from sentence_transformers import SentenceTransformer

def generate_embeddings_local(chunks, repo_name, save_path="data/embeddings"):
    os.makedirs(save_path, exist_ok=True)

    print("[+] Loading embedding model: BGE-small-en-v1.5")
    model = SentenceTransformer("BAAI/bge-small-en-v1.5")

    vectors = []
    metadata = []

    for chunk in chunks:
        vec = model.encode(chunk["content"])
        vectors.append(vec)

        metadata.append({
            "chunk_id": chunk["chunk_id"],
            "file_path": chunk["file_path"],
            "start_line": chunk["start_line"],
            "end_line": chunk["end_line"],
            "content": chunk["content"]
        })

    # Save vectors + metadata
    with open(f"{save_path}/{repo_name}_vectors.pkl", "wb") as f:
        pickle.dump(vectors, f)

    with open(f"{save_path}/{repo_name}_metadata.pkl", "wb") as f:
        pickle.dump(metadata, f)

    print("[+] Embeddings saved at:", save_path)
    print("[+] Total vectors:", len(vectors))
    print("[+] Sample vector dimension:", len(vectors[0]) if vectors else 0)

    return vectors, metadata
