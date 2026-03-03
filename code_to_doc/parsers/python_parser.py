import ast
import os

def parse_python_file(file_path):
    """
    Parses a Python file using AST and extracts classes, functions, and metadata.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
            tree = ast.parse(code)
    except Exception as e:
        return {"error": str(e)}

    metadata = {
        "classes": [],
        "functions": [],
        "imports": [],
        "docstring": ast.get_docstring(tree)
    }

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.ClassDef):
            metadata["classes"].append(extract_class_details(node))
        elif isinstance(node, ast.FunctionDef):
            metadata["functions"].append(extract_function_details(node))
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            metadata["imports"].extend(extract_import_details(node))

    return metadata

def extract_class_details(node):
    """
    Extracts details from an ast.ClassDef node.
    """
    methods = []
    for item in node.body:
        if isinstance(item, ast.FunctionDef):
            methods.append(extract_function_details(item))
            
    return {
        "name": node.name,
        "docstring": ast.get_docstring(node),
        "methods": methods,
        "bases": [ast.dump(b) for b in node.bases]
    }

def extract_function_details(node):
    """
    Extracts details from an ast.FunctionDef node.
    """
    return {
        "name": node.name,
        "parameters": [arg.arg for arg in node.args.args],
        "returns": ast.unparse(node.returns) if hasattr(ast, 'unparse') and node.returns else None,
        "docstring": ast.get_docstring(node),
        "decorators": [ast.unparse(d) if hasattr(ast, 'unparse') else ast.dump(d) for d in node.decorator_list]
    }

def extract_import_details(node):
    """
    Extracts import names from ast.Import or ast.ImportFrom nodes.
    """
    imports = []
    if isinstance(node, ast.Import):
        for alias in node.names:
            imports.append(alias.name)
    elif isinstance(node, ast.ImportFrom):
        module = node.module or ""
        for alias in node.names:
            imports.append(f"{module}.{alias.name}")
    return imports
