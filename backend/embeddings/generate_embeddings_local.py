import os
import pickle
from sentence_transformers import SentenceTransformer
import os
import pickle
import time
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv

# Load env variables (ensures GEMINI_API_KEY is loaded)
load_dotenv()

# Configure the API globally
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# def generate_embeddings_local(chunks, repo_name, save_path="data/embeddings"):
#     os.makedirs(save_path, exist_ok=True)

#     # print("[+] Loading embedding model: BGE-small-en-")
#     # model = SentenceTransformer("BAAI/bge-small-en-v1.5")

#     # model = SentenceTransformer("BAAI/bge-base-en-v1.5")
#     model = SentenceTransformer('all-MiniLM-L6-v2')




#     vectors = []
#     metadata = []

#     for chunk in chunks:
#         vec = model.encode(chunk["content"])
#         vectors.append(vec)

#         metadata.append({
#             "chunk_id": chunk["chunk_id"],
#             "file_path": chunk["file_path"],
#             "start_line": chunk["start_line"],
#             "end_line": chunk["end_line"],
#             "content": chunk["content"]
#         })

#     # Save vectors + metadata
#     with open(f"{save_path}/{repo_name}_vectors.pkl", "wb") as f:
#         pickle.dump(vectors, f)

#     with open(f"{save_path}/{repo_name}_metadata.pkl", "wb") as f:
#         pickle.dump(metadata, f)

#     print("[+] Embeddings saved at:", save_path)
#     print("[+] Total vectors:", len(vectors))
#     print("[+] Sample vector dimension:", len(vectors[0]) if vectors else 0)

#     return vectors, metadata

def get_gemini_embedding(text, task_type="retrieval_document"):
    """Helper function to get embedding with error handling"""
    try:
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type=task_type
        )
        return result['embedding']
    except Exception as e:
        print(f"Error embedding text: {e}")
        return None

def generate_embeddings_local(chunks, repo_name, save_path="data/embeddings"):
    os.makedirs(save_path, exist_ok=True)
    
    print("[+] Generating embeddings using Gemini API...")

    vectors = []
    metadata = []

    for i, chunk in enumerate(chunks):
        # --- CHANGED: Use Gemini for Document Embedding ---
        vec = get_gemini_embedding(chunk["content"], task_type="retrieval_document")
        
        if vec is None:
            continue # Skip failed chunks
            
        vectors.append(vec)

        metadata.append({
            "chunk_id": chunk["chunk_id"],
            "file_path": chunk["file_path"],
            "start_line": chunk["start_line"],
            "end_line": chunk["end_line"],
            "content": chunk["content"]
        })
        
        # Optional: Print progress every 10 chunks
        if i % 10 == 0:
            print(f"Processed {i}/{len(chunks)} chunks")
        
        # Tiny sleep to be safe with free tier limits
        time.sleep(0.05) 
    # --------------------------------------------------

    # Save vectors + metadata
    with open(f"{save_path}/{repo_name}_vectors.pkl", "wb") as f:
        pickle.dump(vectors, f)

    with open(f"{save_path}/{repo_name}_metadata.pkl", "wb") as f:
        pickle.dump(metadata, f)

    print("[+] Embeddings saved at:", save_path)
    print("[+] Total vectors:", len(vectors))
    # Note: Gemini embedding dimension is 768, unlike MiniLM's 384
    print("[+] Sample vector dimension:", len(vectors[0]) if vectors else 0)

    return vectors, metadata