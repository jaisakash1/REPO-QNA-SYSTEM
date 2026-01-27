# from backend.vector_store.faiss_store import search_similar

# repo_name = "NutriFit"  # or whatever your repo is
# query = "diet planning implementation"

# results = search_similar(repo_name, query)

# print("Top Matches:")
# for r in results:
#     print("- file:", r["chunk"]["file_path"])
#     print("  lines:", r["chunk"]["start_line"], "-", r["chunk"]["end_line"])
#     print("  distance:", r["distance"])
#     print()



# backend/vector_store/test_query.py

from backend.vector_store.faiss_store import search_similar

repo_name = "NutriFit"
query =  "query:how does this implemtn reminder and email service feature"

results = search_similar(repo_name, query)

print("Top Results:\n")
# for r in results:
#     print(f"[Score: {r['rerank_score']:.4f}] File: {r['chunk']['file_path']} Lines {r['chunk']['start_line']}-{r['chunk']['end_line']}\n")
# print("Top Matches:")
for r in results:
    print("- file:", r["chunk"]["file_path"])
    print("  lines:", r["chunk"]["start_line"], "-", r["chunk"]["end_line"])
    print("  distance:", r["distance"])
    print()