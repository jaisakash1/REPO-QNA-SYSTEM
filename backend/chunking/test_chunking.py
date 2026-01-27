# from backend.ingestion.pipeline import ingest_repo
# from backend.chunking.save_chunks import save_chunks

# url = "https://github.com/jaisakash1/UIDAI"

# data = ingest_repo(url)
# chunks = data["chunks"]
# print("Repo:", data["repo_name"])
# print("Total files extracted:", len(data["files"]))
# print("Total chunks created:", len(chunks))
# print("\nSample Chunk:", chunks[0])

# save_path = save_chunks(data["repo_name"], chunks)
# print("Chunks saved at:", save_path)


from backend.ingestion.pipeline import ingest_repo
from backend.chunking.save_chunks import save_chunks
from backend.chunking.chunk_resolver import resolve_chunks
# from chunking.save_chunks import save_chunks

# Test repo URL
url = "https://github.com/jaisakash1/NutriFit"

# Step 1: Ingest repo (clone + read files)
data = ingest_repo(url)

repo_name = data["repo_name"]
files = data["files"]

print(f"[✓] Repo ingested: {repo_name}")
print(f"[✓] Total files extracted: {len(files)}")

# Step 2: Resolve chunks (functions + fallback)
chunks = resolve_chunks(repo_name, files)

print(f"[✓] Total chunks created: {len(chunks)}")

# Step 3: Print a sample chunk
if chunks:
    print("\n--- Sample Chunk ---")
    print(chunks[0])

# Step 4: Save chunks to disk
save_path = save_chunks(repo_name, chunks)
print(f"[✓] Chunks saved at: {save_path}")