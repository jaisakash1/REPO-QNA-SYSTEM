# parsing/node_types.py

FUNCTION_NODE_TYPES = {
    "python": ["function_definition"],
    "javascript": ["function_declaration", "function", "arrow_function", "method_definition"],
    "typescript": ["function_declaration", "function", "arrow_function", "method_definition"],
    "java": ["method_declaration", "constructor_declaration"],
    "kotlin": ["function_declaration"],
    "swift": ["function_declaration"],
    "c_sharp": ["method_declaration"],
    "go": ["function_declaration", "method_declaration"],
    "php": ["function_definition", "method_declaration"],
    "ruby": ["method", "singleton_method"],
    "c": ["function_definition"],
    "cpp": ["function_definition"]
}
