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
        
        # Calculate next start position with overlap
        # Ensure we always advance by at least 1 line to prevent infinite loop
        next_start = end - overlap
        if next_start <= start:
            # If overlap would cause no progress, just move to end
            next_start = end
        start = next_start

    return chunks
