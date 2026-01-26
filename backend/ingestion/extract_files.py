import os

IGNORED_DIRS = {'.git', 'node_modules', 'dist', 'build', '.next', '__pycache__', 'venv', '.cache','.vscode'}
ALLOWED_EXT = {'.md', '.py', '.js', '.ts', '.go', '.java', '.cpp', '.c', '.html', '.css', '.json', '.yaml','.jsx','.tsx','.ipynb'}

def extract_repo_files(repo_path):
    extracted_files = []

    for root, dirs, files in os.walk(repo_path):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for file in files:
            _, ext = os.path.splitext(file)
            if ext.lower() in ALLOWED_EXT:
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    extracted_files.append({
                        "file_path": full_path,
                        "extension": ext.lower(),
                        "content": content
                    })
                except Exception as e:
                    print(f"Error reading {full_path}: {e}")

    return extracted_files
