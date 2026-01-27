# parsing/function_extractor.py

from .parser_pool import get_parser
from .node_types import FUNCTION_NODE_TYPES

def extract_functions(content, file_path, repo_name, language):
    parser = get_parser(language)
    src = content.encode("utf8")
    tree = parser.parse(src)
    root = tree.root_node

    functions = []
    used_line_ranges = []
    valid_types = FUNCTION_NODE_TYPES.get(language, [])

    def extract_text(node):
        return src[node.start_byte:node.end_byte].decode("utf8")

    def visit(node):
        if node.type in valid_types and node.child_count > 0:
            code = extract_text(node)
            start_line = node.start_point[0]
            end_line = node.end_point[0]

            functions.append({
                "chunk_id": f"{repo_name}_{file_path}_{start_line}",
                "repo_name": repo_name,
                "file_path": file_path,
                "content": code,
                "start_line": start_line,
                "end_line": end_line,
                "language": language,
                "type": "function"
            })

            used_line_ranges.append((start_line, end_line))

        for child in node.children:
            visit(child)

    visit(root)
    return functions, used_line_ranges
