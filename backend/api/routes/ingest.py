"""
Ingest endpoint - processes GitHub repositories
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import traceback
import shutil
import stat
import os

from backend.ingestion.pipeline import ingest_repo
from backend.chunking.chunk_resolver import resolve_chunks
from backend.chunking.save_chunks import save_chunks
from backend.embeddings.generate_embeddings_local import generate_embeddings_local
from backend.vector_store.faiss_store import create_faiss_index

router = APIRouter()


class IngestRequest(BaseModel):
    url: str


class IngestResponse(BaseModel):
    success: bool
    repo_name: str
    message: str
    chunk_count: int
    already_indexed: bool = False


def remove_readonly(func, path, excinfo):
    """Handle read-only files on Windows (especially .git folder)"""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def cleanup_repo(repo_name: str, repos_path: str = "data/repos"):
    """Delete the cloned repository after processing to save disk space."""
    repo_path = os.path.join(repos_path, repo_name)
    try:
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path, onerror=remove_readonly)
            print(f"[+] Cleaned up repository: {repo_path}")
    except Exception as e:
        print(f"[!] Warning: Could not delete repo {repo_path}: {e}")


def is_repo_indexed(repo_name: str) -> tuple[bool, int]:
    """Check if a repository is already indexed."""
    faiss_path = f"vector_store/{repo_name}_faiss.index"
    chunks_path = f"data/chunks/{repo_name}_chunks.json"
    
    if os.path.exists(faiss_path) and os.path.exists(chunks_path):
        # Count chunks
        import json
        try:
            with open(chunks_path, "r", encoding="utf-8") as f:
                chunks = json.load(f)
            return True, len(chunks)
        except:
            return False, 0
    return False, 0


def get_repo_name_from_url(github_url: str) -> str:
    """Extract repo name from GitHub URL."""
    from urllib.parse import urlparse
    parsed = urlparse(github_url)
    return os.path.splitext(os.path.basename(parsed.path))[0]


@router.post("/ingest", response_model=IngestResponse)
async def ingest_repository(request: IngestRequest):
    """
    Ingest a GitHub repository:
    1. Check if already indexed (skip if yes)
    2. Clone the repository
    3. Extract and chunk files
    4. Generate embeddings
    5. Create FAISS index
    6. Save chunks for later code retrieval
    7. Delete cloned repo (chunks contain the code)
    """
    # First, check if repo is already indexed
    repo_name = get_repo_name_from_url(request.url)
    indexed, chunk_count = is_repo_indexed(repo_name)
    
    if indexed:
        print(f"[*] Repository '{repo_name}' is already indexed with {chunk_count} chunks")
        return IngestResponse(
            success=True,
            repo_name=repo_name,
            message=f"Repository '{repo_name}' is already indexed. Ready for queries!",
            chunk_count=chunk_count,
            already_indexed=True
        )
    
    # Not indexed, proceed with full processing
    try:
        
        # Step 1: Ingest repo (clone + extract files)
        print(f"[*] Ingesting repository: {request.url}")
        data = ingest_repo(request.url)
        repo_name = data["repo_name"]
        files = data["files"]
        
        # Step 2: Resolve chunks (AST-based + fallback)
        print(f"[*] Resolving chunks for {repo_name}")
        chunks = resolve_chunks(repo_name, files)
        
        # Step 3: Save chunks for later code retrieval
        print(f"[*] Saving {len(chunks)} chunks")
        save_chunks(repo_name, chunks)
        
        # Step 4: Generate embeddings
        print(f"[*] Generating embeddings")
        vectors, metadata = generate_embeddings_local(chunks, repo_name)
        
        # Step 5: Create FAISS index
        print(f"[*] Creating FAISS index")
        create_faiss_index(repo_name, vectors, metadata)
        
        # Step 6: Cleanup - delete cloned repo to save disk space
        print(f"[*] Cleaning up cloned repository")
        cleanup_repo(repo_name)
        
        return IngestResponse(
            success=True,
            repo_name=repo_name,
            message=f"Successfully processed repository '{repo_name}'",
            chunk_count=len(chunks),
            already_indexed=False
        )
        
    except Exception as e:
        traceback.print_exc()
        # Try to cleanup even on error
        if repo_name:
            cleanup_repo(repo_name)
        raise HTTPException(status_code=500, detail=str(e))
