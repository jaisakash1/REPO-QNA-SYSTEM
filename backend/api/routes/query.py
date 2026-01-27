"""
Query endpoint - searches for similar code chunks
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import traceback

router = APIRouter()


class QueryRequest(BaseModel):
    repo_name: str
    query: str
    top_k: Optional[int] = 8


class CodeResult(BaseModel):
    file_path: str
    start_line: int
    end_line: int
    distance: float
    code: str
    language: str


class QueryResponse(BaseModel):
    success: bool
    query: str
    results: List[CodeResult]


def detect_language(file_path: str) -> str:
    """Detect programming language from file extension"""
    ext_map = {
        ".py": "python",
        ".js": "javascript",
        ".jsx": "jsx",
        ".ts": "typescript",
        ".tsx": "tsx",
        ".java": "java",
        ".cpp": "cpp",
        ".c": "c",
        ".h": "c",
        ".hpp": "cpp",
        ".cs": "csharp",
        ".go": "go",
        ".rs": "rust",
        ".rb": "ruby",
        ".php": "php",
        ".html": "html",
        ".css": "css",
        ".scss": "scss",
        ".json": "json",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".md": "markdown",
        ".sql": "sql",
        ".sh": "bash",
        ".bash": "bash",
        ".xml": "xml",
    }
    import os
    ext = os.path.splitext(file_path)[1].lower()
    return ext_map.get(ext, "plaintext")


@router.post("/query", response_model=QueryResponse)
async def query_repository(request: QueryRequest):
    """
    Query a repository for similar code chunks:
    1. Search FAISS index for similar chunks
    2. Retrieve actual source code from stored files
    3. Return results with code content
    """
    try:
        from backend.vector_store.faiss_store import search_similar
        from backend.api.utils.code_fetcher import get_code_from_chunks
        
        # Search for similar chunks
        print(f"[*] Searching for: {request.query}")
        results = search_similar(request.repo_name, request.query, top_k=request.top_k)
        
        # Build response with actual code
        code_results = []
        for r in results:
            chunk = r["chunk"]
            file_path = chunk["file_path"]
            start_line = chunk["start_line"]
            end_line = chunk["end_line"]
            
            # Get code from saved chunks (or fallback to file)
            code = get_code_from_chunks(request.repo_name, file_path, start_line, end_line)
            language = detect_language(file_path)
            
            code_results.append(CodeResult(
                file_path=file_path,
                start_line=start_line,
                end_line=end_line,
                distance=r["distance"],
                code=code,
                language=language
            ))
        
        return QueryResponse(
            success=True,
            query=request.query,
            results=code_results
        )
        
    except FileNotFoundError:
        raise HTTPException(
            status_code=404, 
            detail=f"Repository '{request.repo_name}' not found. Please ingest it first."
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/repos")
async def list_repositories():
    """List all available repositories that have been ingested"""
    import os
    import glob
    
    repos = []
    
    # Check vector_store for indexed repos
    index_files = glob.glob("vector_store/*_faiss.index")
    for f in index_files:
        repo_name = os.path.basename(f).replace("_faiss.index", "")
        repos.append(repo_name)
    
    return {"repos": repos}
