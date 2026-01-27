"""
Utility to fetch actual source code from saved chunks.
"""
import os
import json


# Cache for loaded chunks to avoid repeated file reads
_chunks_cache = {}


def load_chunks_for_repo(repo_name: str, chunks_path: str = "data/chunks") -> dict:
    """
    Load saved chunks for a repository and index by file_path + line range.
    
    Returns a dict keyed by (file_path, start_line, end_line) -> chunk content
    """
    global _chunks_cache
    
    if repo_name in _chunks_cache:
        return _chunks_cache[repo_name]
    
    file_path = os.path.join(chunks_path, f"{repo_name}_chunks.json")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            chunks = json.load(f)
        
        # Index chunks for quick lookup
        indexed = {}
        for chunk in chunks:
            key = (chunk["file_path"], chunk["start_line"], chunk["end_line"])
            indexed[key] = chunk.get("content", "")
        
        _chunks_cache[repo_name] = indexed
        return indexed
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"Error loading chunks: {e}")
        return {}


def get_code_from_chunks(repo_name: str, file_path: str, start_line: int, end_line: int) -> str:
    """
    Get code content from saved chunks.
    
    Args:
        repo_name: Name of the repository
        file_path: Path to the file (as stored in chunk metadata)
        start_line: Starting line number
        end_line: Ending line number
    
    Returns:
        The code content from the saved chunk
    """
    chunks = load_chunks_for_repo(repo_name)
    
    # Try exact match first
    key = (file_path, start_line, end_line)
    if key in chunks:
        return chunks[key]
    
    # If not found, fall back to reading from file
    return get_code_from_file(file_path, start_line, end_line)


def get_code_from_file(file_path: str, start_line: int, end_line: int, base_path: str = "data/repos") -> str:
    """
    Read specific lines from a file (fallback method).
    
    Args:
        file_path: Relative path to the file (e.g., "NutriFit/backend/app.js")
        start_line: Starting line number (1-indexed)
        end_line: Ending line number (1-indexed, inclusive)
        base_path: Base directory where repos are stored
    
    Returns:
        The code content from start_line to end_line
    """
    # file_path from chunks is relative like "data/repos/NutriFit/..."
    # We need to handle both cases
    if file_path.startswith("data/repos"):
        full_path = file_path
    else:
        full_path = os.path.join(base_path, file_path)
    
    try:
        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        
        # Convert to 0-indexed
        start_idx = max(0, start_line - 1)
        end_idx = min(len(lines), end_line)
        
        return "".join(lines[start_idx:end_idx])
    except FileNotFoundError:
        return f"[File not found: {full_path}]"
    except Exception as e:
        return f"[Error reading file: {str(e)}]"


def clear_cache():
    """Clear the chunks cache."""
    global _chunks_cache
    _chunks_cache = {}
