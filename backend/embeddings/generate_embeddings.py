import os
import pickle
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def generate_embeddings_langchain(chunks, repo_name, save_path="data/embeddings"):
    os.makedirs(save_path, exist_ok=True)

    # Initialize Gemini Embedding Model
    embeddings = GoogleGenerativeAIEmbeddings(
        model="text/embedding-004",   # official embedding model
        google_api_key=os.getenv("GEMINI_API_KEY")  # must be set
    )

    vectors = []
    metadata = []

    for chunk in chunks:
        vector = embeddings.embed_query(chunk["content"])  # Single text → embedding
        vectors.append(vector)

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

    return vectors, metadata
