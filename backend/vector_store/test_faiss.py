from backend.vector_store.faiss_store import create_faiss_index
from backend.embeddings.generate_embeddings_local import generate_embeddings_local
from backend.ingestion.pipeline import ingest_repo

# Ingest and chunk
url = "https://github.com/jaisakash1/NutriFit"
data = ingest_repo(url)
chunks = data["chunks"]

# Embed
vectors, metadata = generate_embeddings_local(chunks, data["repo_name"])

# Create FAISS index
create_faiss_index(data["repo_name"], vectors, metadata)
