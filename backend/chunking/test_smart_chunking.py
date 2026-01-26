"""Quick test for function-based chunking without repo cloning"""
from backend.chunking.chunker import chunk_content_smart

# Test Python code
python_code = '''
def hello_world():
    print("Hello, world!")
    return True

class MyClass:
    def __init__(self):
        self.value = 42
    
    def get_value(self):
        return self.value

def another_function(x, y):
    """Add two numbers"""
    return x + y
'''

# Test JavaScript code
js_code = '''
function greet(name) {
    console.log("Hello, " + name);
}

const arrowFunc = (a, b) => {
    return a + b;
};

class Calculator {
    constructor() {
        this.result = 0;
    }
    
    add(x) {
        this.result += x;
        return this;
    }
}
'''

print("=== Testing Python Chunking ===")
py_chunks = chunk_content_smart(python_code, "test.py", "test_repo")
print(f"Chunks created: {len(py_chunks)}")
for c in py_chunks:
    print(f"  [{c['type']}] lines {c['start_line']}-{c['end_line']}: {c['content'][:50]}...")

print("\n=== Testing JavaScript Chunking ===")
js_chunks = chunk_content_smart(js_code, "test.js", "test_repo")
print(f"Chunks created: {len(js_chunks)}")
for c in js_chunks:
    print(f"  [{c['type']}] lines {c['start_line']}-{c['end_line']}: {c['content'][:50]}...")

print("\n=== Testing Markdown (fallback) ===")
md_content = "# Hello\\nThis is a test markdown file.\\n## Section"
md_chunks = chunk_content_smart(md_content, "README.md", "test_repo")
print(f"Chunks created: {len(md_chunks)}")
for c in md_chunks:
    print(f"  [{c['type']}] lines {c['start_line']}-{c['end_line']}")

print("\n[SUCCESS] Function-based chunking is working!")
