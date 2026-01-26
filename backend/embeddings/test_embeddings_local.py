from backend.ingestion.pipeline import ingest_repo
from backend.embeddings.generate_embeddings_local import generate_embeddings_local

if __name__ == "__main__":
    url = "https://github.com/jaisakash1/UIDAI"

    print("[+] Ingesting repo...")
    data = ingest_repo(url)

    print("[+] Generating embeddings...")
    vectors, metadata = generate_embeddings_local(data["chunks"], data["repo_name"])

    print("\n=== TEST RESULT ===")
    print("Repo:", data["repo_name"])
    print("Total chunks:", len(data["chunks"]))
    print("Embeddings generated:", len(vectors))
    print("Vector sample length:", len(vectors[0]) if vectors else "N/A")

    print("\n=== SAMPLE METADATA ===")
    print(metadata[0])
