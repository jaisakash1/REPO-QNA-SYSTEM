from tree_sitter import Parser
from tree_sitter_languages import get_language

class PythonFunctionChunker:
    def __init__(self):
        self.language = get_language("python")
        self.parser = Parser()
        self.parser.set_language(self.language)

    def parse(self, code: str):
        src = code.encode("utf8")
        tree = self.parser.parse(src)
        return tree, src

    def extract(self, node, src):
        return src[node.start_byte:node.end_byte].decode()

    def collect(self, node, src, out):
        if node.type == "function_definition":
            out.append(self.extract(node, src))
        for child in node.children:
            self.collect(child, src, out)

    def chunk(self, code: str):
        tree, src = self.parse(code)
        chunks = []
        self.collect(tree.root_node, src, chunks)
        return chunks


# Test
code = """
def foo(x, y):
    return x + y

def bar():
    print("Hello")

class A:
    def baz(self, n):
        return n*n
"""


chunker = PythonFunctionChunker()
print(chunker.chunk(code))


# from tree_sitter_languages import get_parser
# p = get_parser("python")
# print(p)