import os
import pickle
import torch
from transformers import RobertaTokenizer, RobertaModel

def generate_embeddings_unixcoder(chunks, repo_name, save_path="data/embeddings"):
    os.makedirs(save_path, exist_ok=True)

    print("[+] Loading UniXcoder model...")
    tokenizer = RobertaTokenizer.from_pretrained("microsoft/unixcoder-base")
    model = RobertaModel.from_pretrained("microsoft/unixcoder-base")
    model.eval()

    vectors = []
    metadata = []

    for chunk in chunks:
        # Tokenize with truncation (UniXcoder supports ~512 tokens)
        inputs = tokenizer(chunk["content"], truncation=True, max_length=512, return_tensors="pt")

        with torch.no_grad():
            outputs = model(**inputs)
            # Mean pooling
            vec = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

        vectors.append(vec)

        metadata.append({
            "chunk_id": chunk["chunk_id"],
            "file_path": chunk["file_path"],
            "start_line": chunk["start_line"],
            "end_line": chunk["end_line"],
            "content": chunk["content"]
        })

    with open(f"{save_path}/{repo_name}_vectors.pkl", "wb") as f:
        pickle.dump(vectors, f)

    with open(f"{save_path}/{repo_name}_metadata.pkl", "wb") as f:
        pickle.dump(metadata, f)

    print("[+] UniXcoder embeddings saved at:", save_path)
    print("[+] Total vectors:", len(vectors))
    print("[+] Vector dimension:", len(vectors[0]) if vectors else 0)

    return vectors, metadata
