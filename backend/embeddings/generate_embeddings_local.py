import os
import pickle
from sentence_transformers import SentenceTransformer
import os
import pickle
import time
import numpy as np
# import google.generativeai as genai
from dotenv import load_dotenv

# Load env variables (ensures GEMINI_API_KEY is loaded)
load_dotenv()

# Configure the API globally
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

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


import os
import pickle
import time
import google.generativeai as genai
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Configure the API globally
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_gemini_embedding(text, task_type="retrieval_document"):
    try:
        # Switching to the stable, generally available model
        # If this still fails, you can try "models/embedding-001" (the older legacy model)
        model_name = "models/gemini-embedding-001"
        
        result = genai.embed_content(
            model=model_name,
            content=text,
            task_type=task_type,
            title=None 
        )
        return result['embedding']
    except Exception as e:
        if "429" in str(e):
            print("[-] Quota exhausted — stopping requests temporarily.")
            return None
        # Print the specific error to help debug
        print(f"[-] Error embedding chunk with model '{model_name}': {e}")
        return None
    
def generate_embeddings_local(chunks, repo_name, save_path="data/embeddings"):
    os.makedirs(save_path, exist_ok=True)
    
    print("[+] Generating embeddings using Gemini API...")

    vectors = []
    metadata = []

    for i, chunk in enumerate(chunks):
        # 1. Skip empty content immediately to prevent API errors
        if not chunk["content"] or not chunk["content"].strip():
            continue

        vec = get_gemini_embedding(chunk["content"], task_type="retrieval_document")
        
        # 2. If embedding failed (None), skip this chunk
        if vec is None:
            continue
            
        vectors.append(vec)
        metadata.append(chunk) # Store metadata matching the vector
        
        # Rate limit safety
        time.sleep(0.05) 

    # 3. CRITICAL FIX: If no vectors were generated, stop here.
    if not vectors:
        print("[-] Error: No embeddings were generated. Check API Key or Input Data.")
        return [], []

    # Save vectors + metadata
    with open(f"{save_path}/{repo_name}_vectors.pkl", "wb") as f:
        pickle.dump(vectors, f)

    with open(f"{save_path}/{repo_name}_metadata.pkl", "wb") as f:
        pickle.dump(metadata, f)

    return vectors, metadata