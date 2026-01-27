from tree_sitter_languages import get_parser

parser = get_parser("python")
tree = parser.parse(b"def foo(): pass")
print(tree)