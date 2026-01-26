from .clone_repo import clone_repository
from .extract_files import extract_repo_files
from backend.chunking.pipeline import create_chunks

def ingest_repo(github_url):
    repo_name, repo_path = clone_repository(github_url)
    extracted_files = extract_repo_files(repo_path)
    
    chunks = create_chunks(repo_name, extracted_files)

    return {
        "repo_name": repo_name,
        "files": extracted_files,
        "chunks": chunks
    }
