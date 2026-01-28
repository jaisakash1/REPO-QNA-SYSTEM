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
    
    print("[+] Generating embeddings using Gemini API (Batch Mode)...")

    # --- FIX START: Filter empty chunks first ---
    # We must remove empty strings before batching, or the API fails the whole batch.
    valid_chunks = []
    skipped_count = 0
    
    for c in chunks:
        if c["content"] and c["content"].strip():
            valid_chunks.append(c)
        else:
            skipped_count += 1
            
    print(f"[*] Filtered out {skipped_count} empty chunks. Processing {len(valid_chunks)} valid chunks.")
    # --- FIX END ---

    vectors = []
    metadata = []
    
    BATCH_SIZE = 50 
    
    # Iterate over 'valid_chunks' now, not 'chunks'
    for i in range(0, len(valid_chunks), BATCH_SIZE):
        batch = valid_chunks[i : i + BATCH_SIZE]
        batch_texts = [c["content"] for c in batch]
        
        retries = 3
        for attempt in range(retries):
            try:
                result = genai.embed_content(
                    model="models/gemini-embedding-001",
                    content=batch_texts,
                    task_type="retrieval_document"
                )
                
                batch_embeddings = result['embedding']
                
                vectors.extend(batch_embeddings)
                metadata.extend(batch) 
                
                print(f"   Processed batch {i} to {i + len(batch)}")
                time.sleep(1.5) # Modest sleep to stay safe
                break 

            except Exception as e:
                if "429" in str(e):
                    wait_time = (attempt + 1) * 5
                    print(f"[-] Quota hit. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    # If a different error happens, we print it but don't crash the whole script
                    print(f"[-] Error on batch {i}: {e}")
                    break

    if not vectors:
        print("[-] Error: No embeddings were generated.")
        return [], []

    with open(f"{save_path}/{repo_name}_vectors.pkl", "wb") as f:
        pickle.dump(vectors, f)

    with open(f"{save_path}/{repo_name}_metadata.pkl", "wb") as f:
        pickle.dump(metadata, f)

    print(f"[+] Success! Saved {len(vectors)} embeddings.")
    return vectors, metadata