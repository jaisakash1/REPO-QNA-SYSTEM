from backend.chunking.chunker import chunk_content

def compute_fallback_chunks(content, file_path, repo_name, used_ranges, chunk_size=800, overlap=100):
    lines = content.split("\n")
    total = len(lines)
    covered = [False] * total

    for start, end in used_ranges:
        for i in range(start, min(end+1, total)):
            covered[i] = True

    fallback_blocks = []
    start_line = None
    current = []

    for i, line in enumerate(lines):
        if covered[i]:
            if current:
                fallback_blocks.append((current, start_line))
                current = []
                start_line = None
            continue

        if start_line is None:
            start_line = i
        current.append(line)

    if current:
        fallback_blocks.append((current, start_line))

    fallback_chunks = []
    for block, block_start in fallback_blocks:
        block_text = "\n".join(block)
        chunks = chunk_content(
            content=block_text,
            file_path=file_path,
            repo_name=repo_name,
            chunk_size=chunk_size,
            overlap=overlap
        )
        fallback_chunks.extend(chunks)

    return fallback_chunks
