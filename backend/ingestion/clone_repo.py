import os
import shutil
import stat
from git import Repo
from urllib.parse import urlparse


def remove_readonly(func, path, excinfo):
    """Handle read-only files on Windows (especially .git folder)"""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def clone_repository(github_url, base_path="data/repos"):
    # Extract repo name from URL
    parsed = urlparse(github_url)
    repo_name = os.path.splitext(os.path.basename(parsed.path))[0]
    
    repo_path = os.path.join(base_path, repo_name)

    # If already exists, remove it to re-ingest fresh
    # Use onerror handler for Windows permission issues with .git folder
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path, onerror=remove_readonly)

    print(f"Cloning repo into: {repo_path}")
    Repo.clone_from(github_url, repo_path)

    return repo_name, repo_path
