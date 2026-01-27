

import os
from backend.parsing.language_map import LANGUAGE_BY_EXTENSION
from backend.parsing.function_extractor import extract_functions
from backend.parsing.fallback_chunker import compute_fallback_chunks

def resolve_chunks(repo_name, files):
    all_chunks = []

    for f in files:
        file_path = f["file_path"]
        content = f["content"]

        ext = os.path.splitext(file_path)[1]
        language = LANGUAGE_BY_EXTENSION.get(ext)

        if language:
            funcs, ranges = extract_functions(content, file_path, repo_name, language)
            fallback = compute_fallback_chunks(content, file_path, repo_name, ranges)
            all_chunks.extend(funcs)
            all_chunks.extend(fallback)
        else:
            from backend.chunking.chunker import chunk_content
            all_chunks.extend(chunk_content(content, file_path, repo_name))

    return all_chunks
