from tree_sitter import Parser
from tree_sitter_languages import get_language

class JSFunctionChunker:
    def __init__(self):
        self.language = get_language("javascript")
        self.parser = Parser()
        self.parser.set_language(self.language)

    def parse(self, code: str):
        src = code.encode("utf8")
        tree = self.parser.parse(src)
        return tree, src

    def extract(self, node, src):
        return src[node.start_byte:node.end_byte].decode()

    def collect(self, node, src, out):
        # Standard function declaration:  function foo() {}
        valid = {
            "function_declaration",
            "function",
            "arrow_function",
            "method_definition"
        }
        if node.type in valid and node.child_count > 0:
            out.append(self.extract(node, src))


        # Recursively check children
        for child in node.children:
            self.collect(child, src, out)

    def chunk(self, code: str):
        tree, src = self.parse(code)
        chunks = []
        self.collect(tree.root_node, src, chunks)
        return chunks


# Test usage
if __name__ == "__main__":
    js_code = """
function foo(x) {
  return x + 1;
}

const bar = function(y) { 
  return y * 2 
}

const baz = (z) => {
  console.log(z)
}

class A {
  hello() {
    console.log("Hello")
  }
}
"""

    chunker = JSFunctionChunker()
    chunks = chunker.chunk(js_code)

    print("=== JS FUNCTION CHUNKS ===")
    for i, c in enumerate(chunks, 1):
        print(f"\n--- Function #{i} ---\n{c}")
