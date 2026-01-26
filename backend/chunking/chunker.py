import math

def chunk_content(content, file_path, repo_name, chunk_size=800, overlap=100):
    """
    Splits content into overlapping chunks with line number tracking.
    """
    lines = content.split('\n')
    total_lines = len(lines)

    chunks = []
    start = 0
    chunk_index = 0

    while start < total_lines:
        end = min(start + chunk_size, total_lines)
        chunk_lines = lines[start:end]

        chunk_text = "\n".join(chunk_lines)

        chunk_id = f"{repo_name}_{chunk_index}"

        chunks.append({
            "chunk_id": chunk_id,
            "repo_name": repo_name,
            "file_path": file_path,
            "content": chunk_text,
            "start_line": start,
            "end_line": end
        })

        chunk_index += 1
        start = end - overlap  # move back for overlap

    return chunks
