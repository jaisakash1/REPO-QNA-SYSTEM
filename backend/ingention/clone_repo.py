import os
import shutil
from git import Repo
from urllib.parse import urlparse

def clone_repository(github_url, base_path="data/repos"):
    # Extract repo name from URL
    parsed = urlparse(github_url)
    repo_name = os.path.splitext(os.path.basename(parsed.path))[0]
    
    repo_path = os.path.join(base_path, repo_name)

    # If already exists, remove it to re-ingest fresh
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)

    print(f"Cloning repo into: {repo_path}")
    Repo.clone_from(github_url, repo_path)

    return repo_name, repo_path
