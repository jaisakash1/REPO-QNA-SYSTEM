import os
import pickle
import faiss
import numpy as np
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

def get_gemini_embedding(text, task_type="retrieval_document"):
    """Helper function to get embedding with error handling"""
    try:
        result = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type=task_type
        )
        return result['embedding']
    except Exception as e:
        print(f"Error embedding text: {e}")
        return None

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
    
# def search_similar(repo_name, query_text, top_k=8, load_path="vector_store"):
#     from sentence_transformers import SentenceTransformer
#     import numpy as np

#     # Load index + metadata
#     index, metadata = load_faiss_index(repo_name, load_path)

#     # Load same embedding model for query
#     model = SentenceTransformer("BAAI/bge-base-en-v1.5")

#     # Convert query → embedding
#     query_vec = model.encode(query_text).astype("float32").reshape(1, -1)

#     # Search
#     distances, indices = index.search(query_vec, top_k)

#     # Return top results with metadata
#     results = []
#     for idx, dist in zip(indices[0], distances[0]):
#         if idx < len(metadata):
#             results.append({
#                 "distance": float(dist),
#                 "chunk": metadata[idx]
#             })

#     return results


# best result down
# def search_similar(repo_name, query_text, top_k=8, load_path="vector_store"):
#     from sentence_transformers import SentenceTransformer
#     import numpy as np

#     index, metadata = load_faiss_index(repo_name, load_path)
#     # model = SentenceTransformer("BAAI/bge-base-en-v1.5")
#     model = SentenceTransformer('all-MiniLM-L6-v2')
    
#     query_vec = model.encode(query_text).astype("float32").reshape(1, -1)

#     valid_results = []
#     search_batch = top_k  # how many to fetch per FAISS search
#     offset = 0            # how far into results we are

#     while len(valid_results) < top_k:
#         distances, indices = index.search(query_vec, search_batch + offset)

#         # If no more results available
#         if len(indices[0]) <= offset:
#             break

#         for idx, dist in zip(indices[0][offset:], distances[0][offset:]):
#             if idx >= len(metadata):
#                 continue

#             chunk = metadata[idx]
#             start = chunk.get("start_line", 0)
#             end = chunk.get("end_line", 0)
#             line_length = end - start

#             # Skip chunks with <10 lines
#             if line_length < 10:
#                 continue

#             valid_results.append({
#                 "distance": float(dist),
#                 "chunk": chunk
#             })

#             if len(valid_results) == top_k:
#                 break

#         offset += search_batch  # move deeper for next loop

#     return valid_results

def search_similar(repo_name, query_text, top_k=8, load_path="vector_store"):
    # Load index (assuming load_faiss_index is defined elsewhere in your file)
    index, metadata = load_faiss_index(repo_name, load_path)
    
    # --- CHANGED: Use Gemini for Query Embedding ---
    query_vec_list = get_gemini_embedding(query_text, task_type="retrieval_query")
    
    if query_vec_list is None:
        print("Failed to generate query embedding.")
        return []

    # Convert to numpy array for FAISS
    query_vec = np.array(query_vec_list).astype("float32").reshape(1, -1)
    # -----------------------------------------------

    valid_results = []
    search_batch = top_k  # how many to fetch per FAISS search
    offset = 0            # how far into results we are

    # Safety check: Ensure index exists
    if index is None: 
        return []

    while len(valid_results) < top_k:
        distances, indices = index.search(query_vec, search_batch + offset)

        # If no more results available
        if len(indices[0]) <= offset:
            break

        for idx, dist in zip(indices[0][offset:], distances[0][offset:]):
            if idx >= len(metadata):
                continue

            chunk = metadata[idx]
            start = chunk.get("start_line", 0)
            end = chunk.get("end_line", 0)
            line_length = end - start

            # Skip chunks with <10 lines
            if line_length < 10:
                continue

            valid_results.append({
                "distance": float(dist),
                "chunk": chunk
            })

            if len(valid_results) == top_k:
                break

        offset += search_batch  # move deeper for next loop

    return valid_results