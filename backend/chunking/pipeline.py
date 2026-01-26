from .chunker import chunk_content

def create_chunks(repo_name, files):
    all_chunks = []

    for f in files:
        file_chunks = chunk_content(
            content=f["content"],
            file_path=f["file_path"],
            repo_name=repo_name,
            chunk_size=800,
            overlap=100
        )
        all_chunks.extend(file_chunks)

    return all_chunks
