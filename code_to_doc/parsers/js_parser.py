import re

def parse_js_file(file_path):
    """
    Parses a JavaScript/React file using regex to identify components, functions, and props.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
    except Exception as e:
        return {"error": str(e)}

    metadata = {
        "classes": [],
        "functions": [],
        "components": [],
        "imports": [],
        "hooks": [],
        "routes": [],
        "docstring": None
    }

    # Extract Imports
    import_matches = re.findall(r'import\s+(?:.*?\s+from\s+)?[\'"](.*?)[\'"]', code)
    metadata["imports"] = list(set(import_matches))

    # Extract Hooks (useState, useEffect, etc.)
    hooks = re.findall(r'(use[A-Z][a-zA-Z0-9_]*)', code)
    metadata["hooks"] = list(set(hooks))

    # Extract Routes (Simple path pattern)
    route_matches = re.findall(r'path=["\'](.*?)["\']', code)
    metadata["routes"] = list(set(route_matches))

    # Extract React Components (Functional)
    component_patterns = [
        r'const\s+([A-Z][a-zA-Z0-9_]*)\s*=\s*(?:\([^)]*\)|[a-zA-Z0-9_]+)\s*=>',
        r'function\s+([A-Z][a-zA-Z0-9_]*)\s*\(([^)]*)\)'
    ]
    
    for pattern in component_patterns:
        matches = re.findall(pattern, code)
        for match in matches:
            name = match[0] if isinstance(match, tuple) else match
            props = match[1] if isinstance(match, tuple) and len(match) > 1 else "N/A"
            metadata["components"].append({
                "name": name,
                "props": [p.strip() for p in props.split(',')] if props != "N/A" else [],
                "type": "Functional Component"
            })

    # Extract Regular Functions
    function_matches = re.findall(r'function\s+([a-z][a-zA-Z0-9_]*)\s*\(([^)]*)\)', code)
    for name, params in function_matches:
        metadata["functions"].append({
            "name": name,
            "parameters": [p.strip() for p in params.split(',')],
            "docstring": "No docstring found"
        })

    # Try to find a top-level comment/docstring
    doc_match = re.search(r'/\*\*([\s\S]*?)\*/', code)
    if doc_match:
        metadata["docstring"] = doc_match.group(1).replace('*', '').strip()

    return metadata

