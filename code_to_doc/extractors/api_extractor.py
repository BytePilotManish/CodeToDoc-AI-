import ast
from ..parsers.python_parser import parse_python_file

def extract_api_routes(file_path, language):
    """
    Detects API routes (e.g., FastAPI, Flask) in the code.
    """
    routes = []
    if language == "python":
        metadata = parse_python_file(file_path)
        if "error" in metadata:
            return []
        
        # Look for typical web framework decorators
        for func in metadata.get("functions", []):
            for decorator in func.get("decorators", []):
                # Simple pattern matching for @app.get, @router.post, etc.
                if ".get(" in decorator or ".post(" in decorator or ".put(" in decorator or ".delete(" in decorator or "@app.route" in decorator:
                    routes.append({
                        "method": decorator,
                        "function": func["name"],
                        "parameters": ", ".join(func.get("parameters", [])),
                        "docstring": func["docstring"]
                    })
        
        # Also check inside classes for methods with decorators
        for cls in metadata.get("classes", []):
            for method in cls.get("methods", []):
                for decorator in method.get("decorators", []):
                    if ".get(" in decorator or ".post(" in decorator:
                        routes.append({
                            "method": decorator,
                            "function": f"{cls['name']}.{method['name']}",
                            "docstring": method["docstring"]
                        })
                        
    return routes
