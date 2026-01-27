from backend.vector_store.faiss_store import search_similar

repo_name = "VideoStream"  # or whatever your repo is
query = "comment and tweet implementation"

results = search_similar(repo_name, query)

print("Top Matches:")
for r in results:
    print("- file:", r["chunk"]["file_path"])
    print("  lines:", r["chunk"]["start_line"], "-", r["chunk"]["end_line"])
    print("  distance:", r["distance"])
    print()
