# Function/class node types for different languages
FUNCTION_NODES = {
    # Python
    "function_definition",
    "class_definition",
    # JavaScript/TypeScript
    "function_declaration",
    "arrow_function",
    "method_definition",
    "class_declaration",
    # Java
    "method_declaration",
    "constructor_declaration",
    "class_declaration",
    # Go
    "function_declaration",
    "method_declaration",
    # C/C++
    "function_definition",
    # Rust
    "function_item",
    "impl_item",
    # Ruby
    "method",
    "class",
    # PHP
    "function_definition",
    "method_declaration",
    "class_declaration",
}


def extract_code_units(code, parser, file_path, repo_name):
    """
    Parse code using tree-sitter and extract function/class definitions as chunks.
    Each function/class becomes its own chunk regardless of line count.
    """
    tree = parser.parse(bytes(code, "utf8"))
    root = tree.root_node
    
    lines = code.splitlines()
    units = []
    idx = 0

    def traverse(node):
        nonlocal idx

        node_type = node.type

        if node_type in FUNCTION_NODES:
            start = node.start_point[0]
            end = node.end_point[0]
            content = "\n".join(lines[start:end+1])

            units.append({
                "chunk_id": f"{repo_name}_{idx}",
                "repo_name": repo_name,
                "file_path": file_path,
                "type": node_type,
                "content": content,
                "start_line": start,
                "end_line": end,
            })
            idx += 1
            # Don't traverse into children of functions (avoid nested function duplication)
            return

        for child in node.children:
            traverse(child)

    traverse(root)
    return units
