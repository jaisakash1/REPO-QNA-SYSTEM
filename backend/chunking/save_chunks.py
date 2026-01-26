import json
import os

def save_chunks(repo_name, chunks, base_path="data/chunks"):
    os.makedirs(base_path, exist_ok=True)
    file_path = os.path.join(base_path, f"{repo_name}_chunks.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    return file_path
