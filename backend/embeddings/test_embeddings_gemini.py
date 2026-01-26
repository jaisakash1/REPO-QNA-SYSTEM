from dotenv import load_dotenv
from backend.ingestion.pipeline import ingest_repo
from backend.embeddings.generate_embeddings import generate_embeddings_langchain

load_dotenv()  # loads GEMINI_API_KEY

url = "https://github.com/jaisakash1/UIDAI"

data = ingest_repo(url)
chunks = data["chunks"]

vectors, metadata = generate_embeddings_langchain(chunks, data["repo_name"])

print("Total chunks:", len(chunks))
print("Vector dimension:", len(vectors[0]))
