

import pickle
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer, CrossEncoder

def load_faiss_index(repo_name, load_path="vector_store"):
    index = faiss.read_index(f"{load_path}/{repo_name}_faiss.index")
    with open(f"{load_path}/{repo_name}_metadata.pkl", "rb") as f:
        metadata = pickle.load(f)
    return index, metadata

def search_similar(repo_name, query_text, top_k=50, final_k=5, load_path="vector_store"):
    # Keep raw query for reranker
    raw_query = query_text

    # Load index + metadata
    index, metadata = load_faiss_index(repo_name, load_path)

    # Load embedding model
    # embed_model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    embed_model = SentenceTransformer("BAAI/bge-base-en-v1.5")

    # Instruction tuning for BGE
    embed_query = "query: " + raw_query

    # Query embedding
    query_vec = embed_model.encode(embed_query).astype("float32")

    # Normalize for cosine
    query_vec = query_vec / np.linalg.norm(query_vec)
    query_vec = query_vec.reshape(1, -1)

    # Vector search
    scores, indices = index.search(query_vec, top_k)

    retrieved = []
    for idx, score in zip(indices[0], scores[0]):
        if idx < len(metadata):
            content = metadata[idx]["content"]
            if len(content) < 50:  # skip tiny chunks
                continue
            retrieved.append({
                "cosine_score": float(score),
                "chunk": metadata[idx]
            })

    # --- 🔥 Cross-Encoder Reranking (Deep Relevance) ---
    reranker = CrossEncoder("amberoad/bert-multilingual-passage-reranking-msmarco")

    # Use raw query & "passage:" format
    pairs = [(raw_query, f"passage: {r['chunk']['content']}") for r in retrieved]

    rerank_scores = reranker.predict(pairs)

    for i, r in enumerate(retrieved):
        score = rerank_scores[i]
        if isinstance(score, (list, tuple, np.ndarray)):
            score = score[0]
        r["rerank_score"] = float(score)

    # Sort by rerank score (DESC)
    reranked = sorted(retrieved, key=lambda x: x["rerank_score"], reverse=True)

    return reranked[:final_k]
