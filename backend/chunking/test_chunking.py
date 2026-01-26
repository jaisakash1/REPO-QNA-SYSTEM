from backend.ingestion.pipeline import ingest_repo
from backend.chunking.save_chunks import save_chunks

url = "https://github.com/jaisakash1/UIDAI"

data = ingest_repo(url)
chunks = data["chunks"]
print("Repo:", data["repo_name"])
print("Total files extracted:", len(data["files"]))
print("Total chunks created:", len(chunks))
print("\nSample Chunk:", chunks[0])

save_path = save_chunks(data["repo_name"], chunks)
print("Chunks saved at:", save_path)
