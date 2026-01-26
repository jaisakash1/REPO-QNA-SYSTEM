from tree_sitter_languages import get_parser

# Extension → Tree-Sitter language mappings
LANGUAGE_MAP = {
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".py": "python",
    ".go": "go",
    ".java": "java",
    ".c": "c",
    ".h": "c",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".hpp": "cpp",
    ".rs": "rust",
    ".php": "php",
    ".rb": "ruby",
    ".css": "css",
    ".html": "html",
    ".cs": "c_sharp",
    ".sql": "sql",
    ".toml": "toml",
    ".yaml": "yaml",
    ".yml": "yaml",
}

# Cache for parsers
PARSERS = {}


def get_parser_for_ext(ext):
    """
    Get a tree-sitter parser for the given file extension.
    Returns None if the extension is not supported.
    """
    lang = LANGUAGE_MAP.get(ext.lower())
    
    if not lang:
        return None

    if lang not in PARSERS:
        try:
            PARSERS[lang] = get_parser(lang)
        except Exception as e:
            print(f"[!] Failed to load parser for {lang}: {e}")
            return None

    return PARSERS[lang]
