from  backend.ingestion.pipeline import ingest_repo

if __name__ == "__main__":
    url = "https://github.com/jaisakash1/UIDAI"
    result = ingest_repo(url)

    print("Repo Name:", result["repo_name"])
    print("Total Files Extracted:", len(result["files"]))
    print("\nSample file entry:")
    print(result["files"][0])
