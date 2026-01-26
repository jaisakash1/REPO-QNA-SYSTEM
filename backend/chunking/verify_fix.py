"""Test to verify the infinite loop fix in chunker.py"""
from backend.chunking.chunker import chunk_content

# Test case 1: Small file with overlap larger than remaining content
# This was the scenario causing infinite loop
print("Test 1: Overlap larger than remaining lines")
content = "\n".join([f"line{i}" for i in range(10)])
result = chunk_content(content, "test.py", "test_repo", chunk_size=3, overlap=2)
print(f"  Chunks created: {len(result)}")
for c in result:
    print(f"  Chunk {c['chunk_id']}: lines {c['start_line']}-{c['end_line']}")

# Test case 2: Edge case - very small file
print("\nTest 2: Very small file (fewer lines than chunk_size)")
content = "line1\nline2"
result = chunk_content(content, "test.py", "test_repo", chunk_size=800, overlap=100)
print(f"  Chunks created: {len(result)}")

# Test case 3: Standard case
print("\nTest 3: Standard file (850 lines - original failing case)")
content = "\n".join([f"line{i}" for i in range(850)])
result = chunk_content(content, "test.py", "test_repo", chunk_size=800, overlap=100)
print(f"  Chunks created: {len(result)}")
for c in result:
    print(f"  Chunk {c['chunk_id']}: lines {c['start_line']}-{c['end_line']}")

print("\n[SUCCESS] All tests passed! No infinite loop detected.")
